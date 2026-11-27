# RWB-P4-E8008-APP Move an approval limit

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BB |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8008-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-008 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E8008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst**, I want **one approval limit moved on the delegation of authority table as a new version of that one limit, dated from the day it takes effect and approved by Risk before it decides anything, with the row in force left untouched until that approval**, so that **a limit changes without a code release, the approvers who use it see exactly one limit in force on any date, and the move, its author and its approver are in the decision record**.

Inside `rwb-access` this is the limit-change capability of the legacy story RWB-E8-008:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the write `PATCH /api/recovery/access/v1/doa-limits/{delegationLimitId}`, which moves one limit and answers the move; and the write `POST /api/recovery/access/v1/doa-limits/{delegationLimitId}/approve`, which puts the moved version in force from its own `valid_from`, closes the row it supersedes, publishes `rwb.access.DoaLimitChanged.v1` and answers the limit.
- The `delegation_limit` table is this service's own (ownership map; ASM-0070). The whole-version load of a DoA version, its approval and its rollback are RWB-P4-E1038-APP's, and the lookup `GET /api/recovery/access/v1/doa-limits` is RWB-P4-E2013-APP's. This story neither loads a version nor answers a routing question, and it adds no operation to either of them.
- A move is not an edit of the row in force: it writes a **new** `delegation_limit` row that carries the next `limit_version` of the same limit in state `PENDING_APPROVAL`, and the row it moves stays exactly as it is and keeps deciding approvals until the approval step (BR1, ASM-1574).
- Every move and every approval appends one entry to the local decision-record chain of the library of DP-03, in the same transaction as the write it records, hash-linked to the entry before it and published as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`. The central ledger `decision_log_entry` stays in `rwb-decision` (P7) and is never read or written here.
- `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` is the one business event of the capability (Architecture v5 slide 14 and slide 41: `DoaLimitChanged` is one of the two events of `rwb-access`). Its payload carries the limit, the version, the decision code, the level, the product group, the effective date and the reason, and no holder or substitute reference and no personal data (BR9, ASM-1576).
- The move sits on the screen SCR-41 Delegation of authority through the gateway-bff composite route of DP-19; this story renders no screen of its own and adds no panel.
- This story starts no workflow and owns no Schedule: the approval is synchronous and the four-eyes rule is a right, not a state, and the six-monthly access review list (JOB-18) is another story's.

The lifecycle state set of a moved row is Not specified in the source documents (GAP-0869; ASM-1574): the three states this story fixes are `PENDING_APPROVAL`, `IN_FORCE` and `SUPERSEDED`, held in the standard `state` column of TSD P4 v3 T3.0, and the DoA version load of RWB-P4-E1038-APP keeps its own version states.

### 2. Business rationale

The delegation of authority table is the control that decides who may approve what. It is also the control that goes stale first: a limit moves because Risk changed its mind, not because a release is due. Today the change is a document edit and a release, the legacy story carries it as one administration journey alongside the rule versions (FEAT-ADM-03, RWB-E8-008), and the metric the FSD sets for it is blunt: rule and limit changes made without a code release, 100 percent, measured monthly on the decision record (FSD P4 v3 A2.19.1).

The target makes that possible only if a move is a versioned, dated, approved change of data. The Temporal and Drools design says it in one line: delegation limits are held as versioned reference data and follow the same approve-and-date discipline as the Drools packages, so that a case routed before a change keeps the version it was routed under and a case routed after it is answered by the new one (Temporal and Drools design, DoA section). The worked example is the same settlement case under two versions: THB 2.4m at 20 percent loss routes to L6 under DOA-2026.11 and to L5 from 2 January 2027 under DOA-2027.01, the L6 limit being THB 100m, so that the same case at THB 120m moves to L5 under either version. No code change, no release: the business changed a table and set a date.

This story meets REQ-ACA-004 (the delegation of authority table is held as reference data and sets every approval limit), supports REQ-DRI-010 (thresholds, limits and names are versioned and change without a code release) and REQ-ACA-013 (the administration surface for delegation is available to the security administrator), and it carries FEAT-ADM-03. It is the write side of a table the lookup of RWB-P4-E2013-APP reads and the whole-version load of RWB-P4-E1038-APP seeds.

The one rule that makes a move safe is the sequence, not the form: the moved row must not be able to decide anything before Risk has approved it, and the row it replaces must not disappear while it still decides. That is why the move writes a new row in `PENDING_APPROVAL` and why the supersede is written at the approval and not at the move.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8008-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two writes, the `DoaLimitMove` and `DoaLimit` schemas, the state set, the `rwb.access.DoaLimitChanged.v1` declaration and the contract fakes. This story builds against it and changes no schema |
| RWB-P4-E1038-APP (same service, its own story) | `delegation_limit`, its migration and its per-service Flyway sequence, the load of version DOA-2026.11 with 218 rows (109 MORTGAGE and 109 SSME), the load gate of a whole version, the approval of a version and its rollback. This story moves one row of a version that story loaded; it adds no load path and no rollback |
| RWB-P4-E2013-APP (same service, its own story) | The lookup `GET /api/recovery/access/v1/doa-limits` that reads the version in force for a date. This story must leave that answer correct while a move is pending, and it writes no lookup of its own |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a move and of an approval, hash-linked, in the transaction that writes the row |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the move bounds and the six-monthly review flag, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-41 Delegation of authority and calls the two writes, one hop each |

Business preconditions carried from RWB-E8-008 and from the delegation design:

- Delegation version DOA-2026.11 is in force from 30 November 2026 with 218 rows, and item 2.1.1 at level L4 is two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit (FSD P4 v3 A2.6.4.1).
- The levels are L1 to L6 of LOV-APPROVAL-LEVEL, and the levels L1 to L3 are committee levels whose resolution is recorded in `rwb-decision`; this story moves a limit at any level and resolves no committee (FSD P4 v3 A2.6; TSD P4 v3 T3.2).
- The rights in force are those of TSD P4 v3 T6.1: RW-COE holds `CRUD` in Rules and parameters, RW-RISK holds `RA`, and RW-PRODHEAD holds `R` only. A move needs U and an approval needs A (BR4).
- The author of a move is the person reference in the session and the approver must be a different person holding A; the legacy permission table gives the C letter to RW-COE and the A letter to RW-RISK (legacy RWB-E8-008 permission checks; TSD P4 v3 T6.1).
- The parameter rows that bound a move (`principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`) and the six-monthly review flag of the DoA review are Not specified in the source documents (GAP-0869; ASM-1574): the names are fixed by RWB-P4-E8008-CON and the values are rows, so this story holds no bound and no default.

### 4. Flow

1. The center of excellence analyst opens SCR-41 Delegation of authority, panel limits, through the gateway-bff composite route (DP-19). The route reads the version in force through the lookup of RWB-P4-E2013-APP and shows the rows of that version with their level, product group, decision code and limits.
2. The analyst edits one row and submits it. The route calls `PATCH /api/recovery/access/v1/doa-limits/{delegationLimitId}` on `rwb-access` with the body `principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`, `validFrom` and `reason`, the `Idempotency-Key` of the submission and the `version` of the row the screen read.
3. `DoaLimitMoveController` validates the request: `validFrom` and `reason` are required and an empty one is 422 with MSG-GEN-001 naming the field; `validFrom` may not be before the `valid_from` of the row in force; the four amounts are optional but at least one must differ from the row in force; a value that is not a number of the DF-REF-020, DF-REF-021, DF-REF-022 or DF-REF-058 shape is 422 with MSG-GEN-001.
4. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters U. A caller without that letter is refused with 403 and MSG-P4-002, and nothing is written: no row and no entry (BR4, AC3).
5. `DelegationLimitRepository` reads the row named by the path and its version. A row that is not the one in force for the date of the move, or whose `version` is not the one the caller sent, is refused with 409 and MSG-GEN-004, and the caller reloads the screen (BR6).
6. `DoaLimitMoveService` computes the next `limit_version` of the limit and writes a **new** `delegation_limit` row in the same table and the same schema: the same `decision_code`, `approval_level`, `product_group`, `regulation_item`, `applies_when`, `holder_user_id`, `substitute_user_id`, `max_delay_count`, `min_price_pct_principal`, `min_received_pct` and `max_term_years` as the row it moves; the moved `principal_limit`, `loss_pct_limit`, `min_price_pct_fmv` and `max_loss_amount`; the submitted `valid_from`; `limit_version` next; `state` `PENDING_APPROVAL`; `is_active` true; `version` 1; and the author reference in `created_by` and `updated_by`. The row it moves is not touched (BR1, BR2).
7. The move is appended to the local decision-record chain of DP-03 in the same transaction as the row: one entry with the record code of a limit move, the limit and its version, the moved fields with their old and new values, the author reference, the reason and the time, and no holder or substitute reference (BR7).
8. The answer is `moveId`, `delegationLimitId`, `limitVersion`, `state` `PENDING_APPROVAL`, `validFrom` and `approverRole` `RW-RISK`. `moveId` is the identifier of the move, and the pending row is read back by the limit and its version when the approver opens it.
9. The approver working under RW-RISK opens the same panel, which reads the pending version of the limit and calls `POST /api/recovery/access/v1/doa-limits/{delegationLimitId}/approve` with `Idempotency-Key` and the `version` of the pending row.
10. `DoaLimitApprovalService` authorises Rules and parameters A through the same own authorise call. A caller without A is refused with 403 and MSG-P4-002; a caller who is the author of the move is refused with 403 and MSG-P7-002 (BR3, AC5).
11. In one transaction the service sets the pending row `IN_FORCE` with `valid_from` the submitted date, sets `valid_to` of the row it supersedes to the day before that date, sets that row's `state` to `SUPERSEDED`, appends the approval to the local chain with the approver reference, the limit, the version, the decision code, the level and the date, and stages `rwb.access.DoaLimitChanged.v1` in the outbox with the payload of section 12.3 (BR8, BR9).
12. The answer is the limit with its new `limitVersion`, `state` `IN_FORCE`, `validFrom`, `validTo`, `approvalLevel`, `productGroup`, `decisionCode`, the moved amounts, `approvedByRole` `RW-RISK` and `approvedAt`.
13. Where the move or the approval cannot be recorded, nothing is written and the call fails with 503 and MSG-P7-003: a limit change that is not in the decision record cannot be defended later, and a half-written pair of rows would leave two limits in force (BR7, BR10; legacy RWB-E8-008 AC2).
14. The same `Idempotency-Key` replayed answers the first answer and writes no second row and no second entry: the key row is written in the same transaction (BR11).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `validFrom` is empty, or `reason` is empty | 422 naming the field, no row and no entry | MSG-GEN-001 | AC1 |
| X2 | `validFrom` is before the `valid_from` of the row in force | 422 naming `validFrom`, no row and no entry | MSG-GEN-001 | AC1 |
| X3 | No amount differs from the row in force | 422 naming the first amount field, no row and no entry | MSG-GEN-001 | AC1 |
| X4 | The caller holds no Rules and parameters U, or no A on the approval | 403, no row, no entry, nothing changed | MSG-P4-002 | AC3 |
| X5 | The caller's session has ended | 401, no row and no entry | MSG-P4-001 | AC3 |
| X6 | The row moved is no longer the one in force, or the `version` sent is stale | 409, no row and no entry; the screen reloads | MSG-GEN-004 | AC4 |
| X7 | The approver is the author of the move | 403, no row changes state, no entry, no event | MSG-P7-002 | AC5 |
| X8 | The move or the approval cannot be recorded in the local chain | 503 and no write at all; the rows keep the state they had | MSG-P7-003 | AC2 |
| X9 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; no second row, no second entry and no second event | None | AC1 |
| X10 | A second move is submitted while one version of the same limit is `PENDING_APPROVAL` | 409, no second pending row; the pending version is answered for the approver | MSG-GEN-004 | AC4 |

No exception path of this story changes a case, a task or a role: this service writes one row version of its own table and closes the one it supersedes, and the case, the approval record and the decision task are `rwb-case`'s and `rwb-decision`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8008-CON and its fakes; `delegation_limit` and its load are RWB-P4-E1038-APP's and the lookup is RWB-P4-E2013-APP's, so this story is two writes over one table |
| Negotiable | The bounds, the six-monthly review flag and the reason codes are rows and reference values; the state names and the event payload are fixed by the contract and reviewed with Risk |
| Valuable | One limit moves on a date by approval with no release, and the row in force keeps deciding until the approval |
| Estimable | One controller, two services, one repository, one record appender, one event publisher, five fakes and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule and no screen of its own |
| Testable | Each owned criterion has a test case in section 16, the four-eyes rule is provable with two users, and the two-version answer is provable with a fixed clock |

### 7. Acceptance criteria

```gherkin
Feature: Move an approval limit

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force from 30 November 2026 with 218 rows, 109 for MORTGAGE and 109 for SSME
    Given test user "U-3101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS"
    Given test user "U-3102" holds RW-RISK with "RA" in "RULES_AND_PARAMETERS"
    Given test user "U-3103" holds RW-PRODHEAD with "R" only in "RULES_AND_PARAMETERS"

  Scenario: AC1 Move an approval limit (legacy RWB-E8-008 AC1)
    Given the rwb-case contract mock returns parameter version "PAR-2026.11" in force with the move bounds
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then changes a delegated limit, with Risk approving and the change versioned
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-008 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller with the product head right only is refused (new, D-RCV-60)
    Given test user "U-3103" holds RW-PRODHEAD with "R" only and holds no U letter in "RULES_AND_PARAMETERS"
    When "U-3103" calls PATCH /api/recovery/access/v1/doa-limits/{delegationLimitId} for the L6 row of item 2.1.1 MORTGAGE with principalLimit 100,000,000.00 and validFrom 2027-01-01
    Then the response is 403 with message MSG-P4-002 and no move is answered
    Then no row of delegation_limit is written and no decision-record entry is appended

  Scenario: AC4 A move is a new row version and the row in force keeps deciding (new, D-RCV-60)
    Given the L6 row of item 2.1.1 MORTGAGE carries principal limit 100,000,000.00 and loss limit 30.00 percent in version "DOA-2026.11"
    When "U-3101" moves that row with principalLimit 120,000,000.00 and validFrom 2027-01-01
    Then the response is 200 with state "PENDING_APPROVAL", limitVersion next to "DOA-2026.11" and approverRole "RW-RISK"
    Then the row of "DOA-2026.11" is unchanged and still readable, and GET /api/recovery/access/v1/doa-limits answers its delegationLimitId and limitVersion "DOA-2026.11" for the same case on 15 December 2026
    When "U-3102" holding RW-RISK approves the move
    Then the moved row is "IN_FORCE" from 2027-01-01 and the row of "DOA-2026.11" carries valid_to 2026-12-31 and state "SUPERSEDED"
    Then GET /api/recovery/access/v1/doa-limits answers the moved row with its next limitVersion for the same case on 2 January 2027

  Scenario: AC5 The author cannot approve and the approval publishes one change (new, D-RCV-60)
    Given "U-3101" moved the L6 row of item 2.1.1 MORTGAGE to principalLimit 120,000,000.00 from 2027-01-01
    When "U-3101" calls POST /api/recovery/access/v1/doa-limits/{delegationLimitId}/approve on that move
    Then the response is 403 with message MSG-P7-002 and the moved row stays "PENDING_APPROVAL"
    Then no event is published and no approval entry is appended
    When "U-3102" holding RW-RISK calls the same approve on that move
    Then the response is 200 with state "IN_FORCE" and approvedByRole "RW-RISK"
    Then exactly one message is published on rwb.access.events.v1 as rwb.access.DoaLimitChanged.v1 with delegationLimitId, limitVersion, decisionCode "D6.4", approvalLevel "L6", productGroup "MORTGAGE", effectiveFrom 2027-01-01 and the reason
    Then the payload carries no holder reference and no substitute reference
```

AC1 and AC2 are the two criteria of RWB-E8-008, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the parameters mock, so the move is provable while the parameters contract is still a fake. AC3 to AC5 are new under D-RCV-60 and test only what this story adds.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A move writes a new `delegation_limit` row with the next `limit_version` in state `PENDING_APPROVAL`; the row in force is not changed by the move | RWB-E8-008 AC1; FSD P4 v3 A2.19; ASM-1574 |
| BR2 | A new row keeps the decision code, the level, the product group, the regulation item, the holder, the substitute and the other conditions of the row it moves; only the four amounts and `valid_from` are moved | TSD P4 v3 T3.1 DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 |
| BR3 | The author of a move cannot approve it; an approval by the author is refused with MSG-P7-002 | TSD P4 v3 T6.3; legacy AC-EXC-P4-006-02; MSG-P7-002 |
| BR4 | A move needs Rules and parameters U and an approval needs Rules and parameters A; RW-COE holds CRUD, RW-RISK holds RA and RW-PRODHEAD holds R only | TSD P4 v3 T6.1; legacy RWB-E8-008 permission checks |
| BR5 | The approval puts the moved row `IN_FORCE` from its own `valid_from` and closes the row it supersedes, so exactly one version of a limit is in force on any date | FSD P4 v3 A2.6.4.2; Temporal and Drools design; ASM-1574 |
| BR6 | A row that is not the one in force, or a stale `version`, is refused with 409 and MSG-GEN-004; the move is never applied to a row the caller did not read | TSD P4 v3 T3.0 (`version` is the optimistic lock) |
| BR7 | Every move and every approval appends one entry to the local decision-record chain of DP-03 in the same transaction as the row; an action that cannot be recorded is not taken | R-UNI-39; legacy RWB-E8-008 AC2; DP-03 |
| BR8 | The superseded row carries `valid_to` the day before the `valid_from` of the row that supersedes it, and its state becomes `SUPERSEDED` | FSD P4 v3 A2.6.4.2; ASM-1575 |
| BR9 | The approval publishes exactly one `rwb.access.DoaLimitChanged.v1` carrying the limit, the version, the decision code, the level, the product group, the effective date and the reason, and no holder or substitute reference | Architecture v5 slide 14 and slide 41; ASM-1576 |
| BR10 | No business value in code: the four amounts, the dates, the levels, the product groups and the decision codes are rows and reference values with a version | BR-P4-019; FSD P4 v3 A2.19.3.1; REQ-DRI-010 |
| BR11 | A request is idempotent by `Idempotency-Key`: a replay answers the first answer and writes no second row, no second entry and no second event | Architecture v5 slide 42; DP-09 |
| BR12 | The calendar of a move is data: `valid_from` is submitted and the effective date is that value, so a change takes effect on a date and not at a release | Temporal and Drools design; FSD P4 v3 A2.19.1 |
| BR13 | The record of a move and of an approval carries references, codes, versions, amounts and times only: no name, no e-mail address and no personal field | NFR-040; Principle 5 |
| BR14 | The seven-item change checklist of TSD P4 v3 T6.3 belongs to a rule package version and to the whole-version DoA load; a single move carries its reason and its approver and no checklist | TSD P4 v3 T6.3; FSD P4 v3 A2.19 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are one insert of a copy of the row with four amounts and one date replaced; the row it moves is not updated by the move statement, so the version in force cannot change by accident.
- BR3 is the comparison of the approver reference with `created_by` of the pending row, before anything is written; the refusal is a 403 and not a silent no-op.
- BR4 is two calls to the own authorise operation, one with U and one with A; the letters come from `permission` rows and never from a role name in code.
- BR5 and BR8 are one transaction: `valid_from` of the new row, `valid_to` of the old row and its state, so no reader ever sees two rows in force for the same date or none.
- BR6 is the `version` column of the standard record columns used as an optimistic lock, and the state check on the row the path names.
- BR7 is the record appender of DP-03 inside the transaction; a failure rolls the row back, which is why AC2 sees nothing change.
- BR9 is the outbox row of DP-09 written in the approval transaction; the publisher sends it after commit and the payload has no holder field, so the event cannot leak the person references the row holds.
- BR11 is the `idempotency_key` row written in the transaction of the first answer; a replay returns the stored answer.
- BR14 is a negative rule: a move is refused with MSG-GEN-001 on an empty `reason`, and no checklist field exists on it.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No pending version | A move is submitted | U held, the row is in force, the request valid | New row `PENDING_APPROVAL`, the moved row unchanged |
| No pending version | A move is submitted | U absent, or the request invalid, or a stale version | Nothing written; 403 or 422 or 409 |
| `PENDING_APPROVAL` | Approval by a person holding A other than the author | The pending row is current | `IN_FORCE` from `valid_from`; the superseded row `SUPERSEDED` with `valid_to` the day before |
| `PENDING_APPROVAL` | Approval by the author | The approver is `created_by` | Refused 403 with MSG-P7-002; no change |
| `PENDING_APPROVAL` | Approval by a caller without A | No A letter in the area | Refused 403 with MSG-P4-002; no change |
| `PENDING_APPROVAL` | The record cannot be written | The chain write fails | No change; 503 with MSG-P7-003 |
| `PENDING_APPROVAL` | A second move of the same limit | One version is already pending | Refused 409 with MSG-GEN-004 |
| `IN_FORCE` | A later approved move of the same limit | Its `valid_from` is reached | `SUPERSEDED` with `valid_to` the day before |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A move, a refusal of an approval, or an approval | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `rwb.access.events.v1` | An approval | Exactly one `rwb.access.DoaLimitChanged.v1`, from the outbox of the approving transaction |

A move never deletes a row and never rewrites history: a superseded row keeps its amounts, its holder, its version and its dates, so a case routed under it can still be defended.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Center of excellence analyst (RW-COE) | Submit a move with Rules and parameters U; the author of the move (FSD P4 v3 A2.19.3.3) |
| Risk and model risk officer (RW-RISK) | Approve a move with Rules and parameters A; never the author of the same move (TSD P4 v3 T6.1, T6.3) |
| Product head (RW-PRODHEAD) | Reads the table through the lookup with R only; a move is refused with 403 and MSG-P4-002 |
| Security administrator (RW-SECADM) | Holds CRUDA in Platform administration and R in Rules and parameters; this story gives no write path to that right, and the DoA version load is RWB-P4-E1038-APP's |
| Internal audit (RW-AUDIT) and Compliance and PDPA officer (RW-COMPLY) | Read the entries through the access log of `rwb-access` and the central ledger of `rwb-decision`; they approve nothing here |
| The gateway-bff route | Calls the two writes on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` of the submission unchanged |
| `rwb-access` itself | Reads and writes `delegation_limit` in its own schema, reads `role` and `permission`, and writes its own chain and outbox |
| RWB-P4-E1038-APP (same service) | Owns the table's migration, the load of a whole version, the approval of a version and the rollback; this story adds no path of that kind |
| RWB-P4-E2013-APP (same service) | Owns the lookup `GET /doa-limits`; this story must leave its answer correct and calls it not at all |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right and to MSG-P7-002 for an approval by the author, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a stale version and 503 with MSG-P7-003 for a record that cannot be written. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-016 | `delegation_limit` | id | Read: the row the path names and the row in force. Write: the new row's own id |
| DF-REF-017 | `delegation_limit` | decision_code | Read; copied to the new row |
| DF-REF-018 | `delegation_limit` | approval_level | Read; copied to the new row; carried in the event |
| DF-REF-019 | `delegation_limit` | product_group | Read; copied to the new row; carried in the event |
| DF-REF-020 | `delegation_limit` | principal_limit | Read and write: the moved principal limit |
| DF-REF-021 | `delegation_limit` | loss_pct_limit | Read and write: the moved loss percentage limit |
| DF-REF-022 | `delegation_limit` | min_price_pct_fmv | Read and write: the moved sale price floor |
| DF-REF-023 | `delegation_limit` | holder_user_id | Read; copied to the new row; never in the event |
| DF-REF-024 | `delegation_limit` | substitute_user_id | Read; copied to the new row; never in the event |
| DF-REF-025 | `delegation_limit` | valid_from | Read and write: the submitted effective date |
| DF-REF-026 | `delegation_limit` | valid_to | Write on approval: the day before the new `valid_from`, on the superseded row |
| DF-REF-055 | `delegation_limit` | limit_version | Read; write: the next version of the limit |
| DF-REF-056 | `delegation_limit` | regulation_item | Read; copied to the new row |
| DF-REF-057 | `delegation_limit` | applies_when | Read; copied to the new row |
| DF-REF-058 | `delegation_limit` | max_loss_amount | Read and write: the moved maximum loss amount |
| DF-REF-059 | `delegation_limit` | max_delay_count | Read; copied to the new row |
| DF-REF-060 | `delegation_limit` | min_price_pct_principal | Read; copied to the new row |
| DF-REF-061 | `delegation_limit` | min_received_pct | Read; copied to the new row |
| DF-REF-062 | `delegation_limit` | max_term_years | Read; copied to the new row |
| TSD P4 v3 T3.0 | `delegation_limit` | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write: `state` `PENDING_APPROVAL` then `IN_FORCE`, `version` 1 on the new row and the optimistic lock on the row read, the author reference in `created_by` and the approver reference in `updated_by` |
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the caller's role and its class |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the U and A letters in Rules and parameters |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the entry of a move and of an approval: `decision_code` DF-DEC-003, `inputs_ref` DF-DEC-008 with the limit, the version, the moved fields, the author and approver references and the reason, `case_id` DF-DEC-002 empty, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write |
| (outbox) | `outbox_event` in `rwb_access` | the `rwb.access.DoaLimitChanged.v1` row of an approval and the record row of each entry | Write |
| (idempotency) | `idempotency_key` in `rwb_access` | the key of a move and of an approval, with the stored answer | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `case`, `task`, `approval`, `decision_log_entry`, `rule_package_version` or `lov_value` is read or written: the case and its task are `rwb-case`'s (P3), the approval record and the central ledger are `rwb-decision`'s (P7), the rule registry is P7's and the list values are P3 reference data, and no foreign key crosses a schema (DP-01). The holder and substitute references of a row are user references and stay inside `rwb_access`; the event carries neither (BR9). Field IDs are those of the Logical Data Model and Data Dictionary v9.

The names and types of the request and answer fields, the `limit_version` scheme (whether the next version of a limit is a sequence of the limit or a label built from the DoA version and a suffix), and the record code of a move are Not specified in the source documents (GAP-0869; ASM-1574): the schema of RWB-P4-E8008-CON fixes them and this story reads and writes them as that contract publishes them.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| PATCH | `/api/recovery/access/v1/doa-limits/{delegationLimitId}` | P4 `rwb-access` | Path: `delegationLimitId`. Body: `principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`, `validFrom`, `reason`, `version` | `moveId`, `delegationLimitId`, `limitVersion`, `state` `PENDING_APPROVAL`, `validFrom`, `approverRole` `RW-RISK` | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters U, scope applied | `Idempotency-Key` required; a replay answers the first answer |
| POST | `/api/recovery/access/v1/doa-limits/{delegationLimitId}/approve` | P4 `rwb-access` | Path: `delegationLimitId`. Body: `limitVersion`, `version`, `decision` | The limit: `moveId`, `delegationLimitId`, `limitVersion`, `state` `IN_FORCE`, `validFrom`, `validTo`, `decisionCode`, `approvalLevel`, `productGroup`, `principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`, `approvedByRole` `RW-RISK`, `approvedAt` | 401 (MSG-P4-001); 403 (MSG-P4-002, MSG-P7-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters A, and the approver is not the author | `Idempotency-Key` required; a replay answers the first answer and publishes no second event |

Both operations sit on the base `/api/recovery/access/v1` of DP-13 and address the limit by `delegationLimitId`, the identity every version of the limit carries. The move is answered with its own `moveId`, and the approval path names the same `delegationLimitId`, so the approver approves the pending version of the limit and no other version can be approved by mistake. This pair of operations is absent from Recovery Workbench API Specification v4, which declares no delegation-of-authority operation at all; the delegation lookup itself is named only in Architecture v5 slide 14 and in API Specification v3 (GAP-0869; ASM-1574); the contract review confirms or renames the two paths and the field names before they are frozen.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters U check behind the move and the A check behind the approval, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The move bounds and the six-monthly review flag, as parameter rows with the version in force (DP-06) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the parameter read is cached for the life of the request. No operation of `rwb-decision`, `rwb-case` or `rwb-document` beyond the parameters read is called, and the lookup `GET /api/recovery/access/v1/doa-limits` is not called by the writes of this story.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 | `delegationLimitId` | `delegationLimitId`, `limitVersion`, `decisionCode`, `approvalLevel`, `productGroup`, `effectiveFrom`, `reason` |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a move and of an approval |

CloudEvents 1.0 envelope, from the outbox of the transaction that writes the row. The payload of `DoaLimitChanged` carries no holder reference, no substitute reference, no name, no e-mail address and no personal field, and no case id: a consumer learns that the limit of a level and a product group changed from a date, and asks the lookup for the holder it needs (BR9). `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and is not published here.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and a move of its own table needs no subscription. The `processed_event` table is written by no part of this story.

#### 12.5 Workflows and activities

None. The approval is synchronous and the four-eyes rule is a right, not a state: this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. `ApprovalWorkflow` of the workflow kit belongs to `rwb-decision` (P7) and is not used for an administration change of this service.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP; a move takes effect from its `valid_from` and needs no timer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `delegation_limit` | P4 (`rwb_access`) | Read: the row in force and its version. Write: one new row per move, and on approval its state and `valid_to`, plus the `valid_to` and state of the row it supersedes. Created and loaded by RWB-P4-E1038-APP |
| `role` | P4 (`rwb_access`) | Read only: the caller's role and class |
| `permission` | P4 (`rwb_access`) | Read only: the U and A letters in Rules and parameters |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of a move and of an approval |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The `DoaLimitChanged` row and the record rows of the entries; the idempotency row of both writes; no inbox row, because no event is consumed (DP-09) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger entry is P7's and the local record goes on `rwb.decision-record.v1` |

`lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so the values it validates (the decision code, the level and the product group of the row it moves) are taken from the row in force and not from a list read (GAP-0869; ASM-1574). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| authorise fake | RWB-P4-E1037-CON, RWB-P4-E8008-CON | The granted answer for RW-COE with U and for RW-RISK with A, and the refused answer with MSG-P4-002 for RW-PRODHEAD with R only |
| parameters fake | RWB-P3-E1042-CON | The move bounds and the six-monthly review flag at version PAR-2026.11 |
| decision-record fake | RWB-PLT-E1027-CON | The append of a move and of an approval, the hash-link check, the replay of an `Idempotency-Key`, and the forced failure AC2 needs |
| DoA fixture | RWB-P4-E8008-CON, seeded by RWB-P4-E1038-APP | DOA-2026.11 with the L6 row of item 2.1.1 MORTGAGE at principal 100,000,000.00 and loss 30.00 percent, and the same limit at principal 120,000,000.00 from 2027-01-01 as the moved version |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-41 with the limits panel, the move form and the pending-approval state |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the move and the approval); consumed 2 | Base `/api/recovery/access/v1`; one hop, 2 s timeout |
| Kafka | Published 2 event types; consumed 0 | `rwb.access.events.v1` for `DoaLimitChanged`, and `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | No file input and no file output; the DoA workbook load is RWB-P4-E1038-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/doa`, Java package `th.co.scb.ace.workbench.recovery.access.doa.limit`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process write of the single `delegation_limit` table of the monolith (DP-01 and DP-13: a row version of the service's own table, addressed on the service's own base) and the ace-web screen that performed the edit in process (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. The reference-data list check of the values a row carries would need DP-07 and `RWB-P3-E1043-CON`, neither of which this story's metadata carries, so the values are taken from the row in force and the point is raised as the key's gap (GAP-0869; ASM-1574).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DoaLimitMoveController | Controller | `PATCH /doa-limits/{delegationLimitId}`: validation, the RFC 9457 problem responses, the `Idempotency-Key` read, the 409 on a stale version |
| DoaLimitApprovalController | Controller | `POST /doa-limits/{delegationLimitId}/approve`: validation, the four-eyes refusal, the 409 on a stale or non-pending version |
| DoaLimitMoveService | Service | The new row of BR1 and BR2, the next `limit_version`, the one-pending-version check and the answer of the move |
| DoaLimitApprovalService | Service | BR5 and BR8: `IN_FORCE` from `valid_from`, the superseded row's `valid_to` and state, the approver in `updated_by` |
| DelegationLimitRepository | Repository | The row in force and its version, the pending version of a limit, the insert of a new row and the two updates of an approval; no delete method |
| PermissionReader | Service | The `role` and `permission` rows of the caller and the U and A letters in Rules and parameters |
| DoaChangeEventPublisher | Service | The `rwb.access.DoaLimitChanged.v1` row in the outbox of the approving transaction, with the payload of section 12.3 and no holder field |
| DecisionRecordAppender | Service | The entry of a move and of an approval with its outbox row, in the transaction that writes the row (DP-03, DP-09) |
| CaseDataClient | Client | The parameters read of DP-06, one hop, 2 s timeout, cached |

**Database and migrations**

- This story adds no table: `delegation_limit` and its per-service Flyway sequence are RWB-P4-E1038-APP's (DP-15), and this story reads and writes rows of it. If the SIT query plan needs an index for the version-in-force window or for the pending version of a limit, the index is added to that story's migration with the agreement of its owner, not to a new one here.
- Two states must not be producible by a bug: no reader may see two rows in force for the same limit and date, and no limit may have two pending versions. The first is a partial unique constraint on the limit and its window, or a checked update, and is agreed with RWB-P4-E1038-APP's migration; the second is a check inside the move transaction on the pending row.
- The insert of a new row is a plain insert; the approval is two updates in one transaction. There is no delete statement in the repository, so a superseded row can never be removed.
- The record row, the outbox row and the idempotency row commit with the write they belong to; a failure rolls all of them back and the call fails with MSG-P7-003.

**Configuration and reference data**

- The move bounds (`principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`) and the six-monthly review flag are parameter rows of `rwb-case` read through DP-06 with the version in force; no bound is a constant in code (BR10). Their names are fixed by RWB-P4-E8008-CON.
- The levels (L1 to L6), the product groups and the decision codes are values of the row in force and of the version loaded by RWB-P4-E1038-APP; this story copies them and validates nothing against a list of its own (section 12.7; GAP-0869).
- No amount, date, level or product group is a constant in code or in a test fixture outside the seeded DoA fixture of section 12.8.

**Build steps**

1. `DelegationLimitRepository` with the row-in-force read, the pending-version read, the insert and the two updates; test that a move leaves the row in force untouched and that the repository has no delete.
2. `DoaLimitMoveService` with the new row of BR1 and BR2 and the next `limit_version`; test that every condition of the moved row is copied and only the four amounts and `valid_from` differ (AC1, AC4).
3. `PermissionReader` and the U check; test the refusal of AC3 with no row and no entry.
4. `DoaLimitApprovalService` with the transaction of BR5 and BR8 and the four-eyes refusal; test AC5 and the window of AC4 on a fixed clock.
5. `DoaChangeEventPublisher` and `DecisionRecordAppender` in the same transaction; test that exactly one event leaves the outbox per approval and that neither the event nor the entry carries a holder or substitute reference.
6. The forced failure of AC2 on both writes: 503, MSG-P7-003 and no change to any row.
7. `CaseDataClient` over the parameters fake, so the story builds before `rwb-case` is in the environment; test that a changed bound is data and needs no build.
8. The contract-fake run of both writes through the gateway-bff fake, so SCR-41 can be demonstrated while the route is being built.
9. The stale-version and second-move tests of X6 and X10, and the idempotent replay test of X9.

**Feature switch.** The two writes are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. A move that has not been approved changes nothing a reader sees, so no switch is needed to hold it back; the contract declares no 404 branch and adds no parameter.

**Done when.** The tests in section 16 pass; a move of the L6 row of item 2.1.1 MORTGAGE answers a pending version with its date and `approverRole`; the row of DOA-2026.11 still answers the lookup until the approval; an approval by RW-RISK puts the new version in force from its `valid_from`, closes the old row the day before and publishes one `rwb.access.DoaLimitChanged.v1`; an approval by the author is refused with MSG-P7-002; a caller with R only is refused with MSG-P4-002; and a forced failure of the record leaves every row as it was with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both writes |
| MSG-P4-002 | The caller holds no Rules and parameters U on the move, or no A on the approval | You cannot {action} here. Your role does not include it. | This story, on both writes |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, in the answer of both writes |
| MSG-GEN-001 | A required field is empty, a date is before the row in force, or an amount is not of its shape | Enter {field}. | This story, on both writes |
| MSG-GEN-004 | The `version` sent is stale, the row is no longer in force, or a version is already pending | Someone else changed this record. Reload it to see their change. | This story, on both writes |
| MSG-P7-002 | The approver is the author of the move | Not specified in the source documents (GAP-0869; ASM-1574) | This story, on the approval |
| MSG-P7-003 | The move or the approval cannot be recorded, or the event cannot be staged | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both writes |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts, and MSG-GEN-004 is the platform text. MSG-P7-002 is the TSD P4 v3 T6.3 four-eyes rule and its text is Not specified in the source documents (GAP-0869; ASM-1574); the message catalogue supplies it and the contract of RWB-P4-E8008-CON carries its `messageId` only.

### 15. Screens and states

The move is one panel of SCR-41 Delegation of authority, served by the gateway-bff composite route of DP-19, which reads the version in force through the lookup of RWB-P4-E2013-APP and calls the two writes of this story, one hop each.

| Screen | State | What it shows |
|---|---|---|
| SCR-41 Delegation of authority | Limits, list | The rows of the version in force with their decision code, level, product group and limits, paged |
| SCR-41 Delegation of authority | Move, form | One row opened for a move with the four amounts, `validFrom` and `reason`; the bounds come from the parameters read |
| SCR-41 Delegation of authority | Move, pending approval | The moved version with its `limitVersion`, `state` `PENDING_APPROVAL`, `validFrom` and `approverRole` `RW-RISK`, and the row in force shown beside it and unchanged |
| SCR-41 Delegation of authority | Move, approved | The moved version `IN_FORCE` from its date and the superseded row with its `valid_to` and state |
| SCR-41 Delegation of authority | Move, stale | The 409 of X6 with MSG-GEN-004 and a reload action |
| SCR-41 Delegation of authority | Move, refused | The MSG-P4-002 refusal for a role without U, and the MSG-P7-002 refusal for an approval by the author |
| SCR-41 Delegation of authority | Move, not recorded | The MSG-P7-003 refusal with every row as it was |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority although the limit move sits on the second only; the rule-version work of the same legacy key is RWB-E8-007's and RWB-P4-AD011-APP's. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work, and this story renders no screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-008-01 | AC1, BR1, BR2, BR12 | Contract | A move of the L6 row of item 2.1.1 MORTGAGE with the parameters at version PAR-2026.11: a new row with the next `limit_version`, the moved amounts and `validFrom`, and the row in force unchanged |
| TC-E8-008-02 | AC2, BR7 | Component | The record store forced to fail during a move and during an approval: 503, MSG-P7-003 and no row changed |
| TC-E8-008-03 | AC3, BR4 | Component | A caller with RW-PRODHEAD and R only: 403, MSG-P4-002, no row and no entry |
| TC-E8-008-04 | AC2, BR7 | NFR | The record append inside the transaction of the move and of the approval, with the outbox and idempotency rows, and the rollback when the append does not commit |
| TC-E8-008-05 | AC4, BR5, BR6, BR8 | Component | DOA-2026.11 in force and the moved version from 2027-01-01: the lookup answers the old row until the approval and the new version after it, on a fixed clock |
| TC-E8-008-06 | AC5, BR3, BR9, BR11 | Component | The approval by the author refused with MSG-P7-002, the approval by RW-RISK with exactly one `DoaLimitChanged` and no holder field, and the replay of one `Idempotency-Key` |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-008-01 for AC1, TC-E8-008-02 for AC2, TC-E8-008-03 for the access refusal of the legacy `Access` test and TC-E8-008-04 for the forced record failure of the legacy `Principle 5` test; two rows are added for AC4 and AC5. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. No `-ITG` id appears in this table, because no integration story is split from this key.

### 17. Guardrails

- No business value in code: the four amounts, the dates, the levels, the product groups and the decision codes are rows and values with a version, and the bounds are parameter rows (BR10). A test proves that a changed bound or a new row needs no build.
- No personal data anywhere: the writes take user references, the answers carry references, codes, versions, amounts and times, the entries and the event carry no name, no e-mail address and no personal field, and the event carries neither the holder nor the substitute reference (BR9, BR13).
- No read of another service's tables (DP-01): `case` and `task` are `rwb-case`'s, `approval`, `decision_log_entry` and the rule registry are `rwb-decision`'s, and the list values are P3 reference data. No join crosses a schema.
- ACE data only through the owner's contract or the service's own `v_ace_*` views: this story reads no ACE data; the group-to-role mapping is the service baseline's.
- One writer for a limit: this story writes `delegation_limit` only through the move and the approval, and no other path of the service edits a row in place. The repository has no delete method, so a superseded row is never removed.
- No write without its record: the row, the entry and the outbox row commit together, and the write is withheld with MSG-P7-003 when the record cannot be written (BR7, R-UNI-39).
- No version jumped silently: a move writes a new version and never edits the one in force, so a case routed before a change keeps the version it was routed under.
- Exactly one row in force on any date: the approval closes the superseded row at the day before the new `valid_from` in the same transaction, so no reader sees two limits or none (BR5, BR8).
- A refused caller learns nothing about the data: the refusal names the missing right or the four-eyes rule and nothing else, and no limit amount, holder or substitute is returned in a refusal.
- Idempotent by key: a retried submission with the same `Idempotency-Key` answers the first answer and publishes no second event.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit | Program, Access and audit | FEAT-ACA-06, FEAT-ADM-03 | 20 Administer access and audit | BR1, BR2, BR5, BR8 | TC-E8-008-01, TC-E8-008-05 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Program, Data and reporting | FEAT-ADM-03 | 20 Administer access and audit | BR10, BR12 | TC-E8-008-01, TC-E8-008-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 BRD | FEAT-ADM-03 | 20 Administer access and audit | BR3, BR4, BR6 | TC-E8-008-03, TC-E8-008-06 |

The requirement IDs are taken from the FSD feature table and the Program BRD under the fill order of Template and Rules §R7.3, which is the order the Work Package directs; the Work Package itself carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 move a delegated limit, with Risk approving and the change versioned, written to the decision log with the rule version | Sections 4, 7, 8, 12.1, 13 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 16 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 10, 12.1, 14 |
| MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The endpoints of the legacy story: the rule-version paths that are P7's and not built here | Section 19 |
| Legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried to SCR-41 Delegation of authority |
| TC-E8-008-01 to TC-E8-008-04 | Section 16 |
| Rule IDs R-UNI-39, BR-P4-019, VR-P4-019-1 | Sections 2, 8, 14, 17 |
| Field IDs DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062, DF-REF-034 to DF-REF-044, DF-DEC-001 to DF-DEC-018 | Section 11 |
| Legacy key RWB-E8-008, story RWB-P4-E8008-APP, contract RWB-P4-E8008-CON | Metadata, sections 3, 12 |
| The DoA versions DOA-2026.11 and DOA-2027.01, the L6 THB 100m and THB 120m example | Sections 2, 3, 12.8 |

### 19. Out of scope

- The whole-version load of a DoA version, its approval, its rollback and its load gate: RWB-P4-E1038-APP. This story moves one row of a version that story loaded.
- The lookup `GET /api/recovery/access/v1/doa-limits` and the authority decision behind `POST /authorise`: RWB-P4-E2013-APP. This story calls neither; it must simply leave the lookup's answer correct.
- The rule-change request and the rule-version paths of the same legacy key, which are `rwb-decision`'s (P7) and RWB-E8-007's.
- The approval record, the approval queue and the escalation of an approval: `rwb-decision` (P7); a limit move is approved synchronously on its own panel and starts no workflow.
- The case, its task and its status: `rwb-case` (P3).
- The six-monthly access review list and its Schedule (JOB-18): RWB-P4-AD008-APP.
- The screen SCR-41 Delegation of authority itself, its other panels and its composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The report of limit changes in `rwb-reporting` and the monthly measure of changes made without a release.
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
