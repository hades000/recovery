# RWB-P3-E3013-APP Check encumbrance and eligibility before negotiation

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E3013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P3-AS |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E3013-APP-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P3-E3013-APP-14) |
| Depends on (build) | None |
| Contract dependencies | RWB-S2-E3013-CON; contract version Not specified in the source documents (DOR-RWB-P3-E3013-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-013 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E3013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 18 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the encumbrance and eligibility answer of a deed-in-lieu check applied to my case by the case workflow — the case moved to EARLY_READINESS_CHECK or held in COLLATERAL_RELEASE_REQUESTED, the early-readiness or title task raised with its due date from the rule's timer spec, and one decision record naming the rule and the package version written in the same transaction** so that **a deed in lieu is never negotiated on an asset that cannot transfer, and the case itself shows why it moved and when the next step is due**.

### 2. Business rationale

A deed in lieu transfers an asset, so the encumbrance and title position has to be known before the offer is negotiated. The legacy story ran the encumbrance and title checks early in the deed-in-lieu route, so that a sale officer does not negotiate a release on an asset that cannot transfer, and it recorded the result with its rule version. When the title documents are missing, the legacy story raises a task to re-create the title set before release and keeps the case where it is; when the route is approved, it prioritises the lead and starts the early readiness checks.

In the target the same journey is cut across services. rwb-treatment (S2) owns the treatment, the deed-in-lieu agreement and the check itself: it reads the collateral, the collateral detail and the non-performing-asset data it needs and evaluates the SET and DIL rule packages in its own service, so the check answer is produced where the treatment lives. rwb-case (P3) owns the case of record: the case state, the task, its due date and the local decision record. This story is the case side of that split. It receives the RuleResult of R-DIL-01 or R-SET-22 through the contract of RWB-S2-E3013-CON, applies the outcome as a state move and a task, holds the due date as a durable timer of `CaseWorkflow`, writes the decision record with the rule ID and the package version in the same `rwb_case` transaction, and publishes CaseStateChanged. It reads no treatment row, no collateral view and no ACE data itself: the check belongs to S2 and the ACE collateral views belong to P1 rwb-source-data.

What the case keeps is small on purpose. The answer is not copied into `rwb_case`: only the outcome code, the check reference and the decision record ID of the record written with the move are stored, so a later reader can find the evidence in the ledger without a second copy of the check in a second schema. That boundary is DP-01 (never read another service's tables) and DP-05 (ACE data only through the owner's contract or the service's own views) applied to a service that owns neither the check nor the collateral.

The realignment work is therefore: the monolith's in-process call from the deed-in-lieu flow to the encumbrance and title check and to the case state move becomes a contract (DP-13 renames the base to `/api/recovery/case/v1` and the S2 contract carries the answer), the state move becomes one `rwb_case` transaction with its outbox rows and its decision record, the due date becomes a durable timer instead of a scheduler row, and the check state becomes a read-only part of the case record composed at the edge by gateway-bff (DP-19) rather than a second screen reading a second database.

### 3. Preconditions

- RWB-S2-E3013-CON is published: the check-answer resource of rwb-treatment (S2) with its rule ID, its package version, its outcome code, its check reference and its task instruction, its error envelope and its contract fake. The method, the path and the field names of that operation are Not specified in the source documents (GAP-0736; ASM-1316); the S2 contract story fixes them, and this story builds against that contract and its fake and never against rwb-treatment, the treatment tables or an ACE view.
- The `rwb_case` schema baseline and the case of record exist from the Epic 1 case story (RWB-P3-E1018-APP): `recovery_case`, `task`, `timer`, `assignment`, `queue`, `outbox_event`, `processed_event` and `idempotency_key`.
- `CaseWorkflow` (parent, workflow ID = case ID, one per case) runs on task queue `rwb-case` in namespace `rwb-recovery` from the reference workflow story (RWB-P3-E2043-APP), with the workflow kit of the platform contract stories.
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published by the platform contract story of DP-03, and the library writes the record in the caller's transaction.
- The case can already hold the deed-in-lieu route: the route decision moved the case to ROUTE_APPROVED_DIL, and the release request moved it to COLLATERAL_RELEASE_REQUESTED, by the route and treatment stories of this epic.
- Packages SET and DIL are in force for the business date with rows R-SET-22 and R-DIL-01, each row carrying its action text, its owner role and its timer spec; the version in force per environment is the version the answer carries.
- The properties of the check, its batch size and its timeout are the business of rwb-treatment; the only local parameter this story would need is the name of the timeout of the call, and that name is Not specified in the source documents (GAP-0736; ASM-1319), so the platform contract default of one hop and 2 s is used.

### 4. Flow

1. The deed-in-lieu route reaches the point where the encumbrance and eligibility check decides the next step: R-DIL-01 on an approved route, R-SET-22 on a release request.
2. The case router of rwb-case signals `CaseWorkflow` (workflow ID = case-{caseId}) for the case; the parent workflow already holds the case from entry to closure and starts the treatment stage as a child on queue `rwb-treatment`.
3. `CaseWorkflow` runs its `EvaluateAndApply` step for the case. The step calls the rwb-treatment check-answer operation of RWB-S2-E3013-CON for the case: one hop, 2 s, breaker; the call is recorded in the workflow history, so a replay reuses the same answer and never asks twice.
4. The answer names the rule ID (R-DIL-01 or R-SET-22), the package version, the outcome code, the check reference and the task instruction. An answer that names neither rule is rejected as not this story's answer and no state, task or record is written.
5. R-DIL-01 on a case in ROUTE_APPROVED_DIL: the case moves to EARLY_READINESS_CHECK, and the early-readiness task is raised for role RW-RESTRUCT with its `due_at` from the timer spec of the rule row that fired.
6. R-SET-22 on a case in COLLATERAL_RELEASE_REQUESTED with the title documents missing: a task is raised to re-create the title set before release, and the case stays in COLLATERAL_RELEASE_REQUESTED.
7. `EvaluateAndApply` writes, in one `rwb_case` transaction: the case state and `rule_version`, the task row with its `task_code` and `due_at`, the `timer` projection row of that due date, the three check columns (outcome code, check reference, decision record ID) and the local decision record naming the rule ID and the package version, hash-linked to the previous record; and it inserts CaseStateChanged and DecisionRecorded in the outbox.
8. A failed write rolls the whole transaction back, so the state does not move, no task exists and no decision record exists: the user sees MSG-P7-003 and the step is retried with the same answer.
9. `CaseWorkflow` holds the due date of the raised task as a durable timer of the workflow kit and raises TimerBreached through its own state when the timer passes; no Quartz row and no five-minute timer check is involved.
10. A repeated answer for the case — the same check reference with the same outcome code — is absorbed by the inbox row and the idempotency key: no second state change, no second task, no second decision record and no second event.
11. `NoPackageInForce` in the answer is a refusal, never a default move: MSG-P3-027 names the package, the case keeps its state and no task is raised.
12. The case owner and the restructuring officer see the check state on SCR-16 and SCR-14 through the gateway-bff composite route, which composes it from the existing case read and the treatment stage answer in one hop each, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer names no rule ID, or names a rule other than R-DIL-01 or R-SET-22 | The answer is not applied; no state, task, record or event is written; the step fails with the contract error and the case keeps its state | MSG-GEN-001 | AC3 |
| X2 | The rwb-treatment operation does not answer within 2 seconds or is unavailable | No state change and no task; the step is retried with the same answer on the workflow retry policy; the case keeps its state | MSG-GEN-001 | AC3 |
| X3 | The answer carries the same check reference and outcome code twice | The inbox row and the idempotency key absorb the repeat; no second state change, task, record or event | None | AC4 |
| X4 | No SET or DIL version is in force for the business date | `NoPackageInForce`; MSG-P3-027 names the package and the business date; the case keeps its state and no task is raised | MSG-P3-027 | AC5 |
| X5 | The local decision-record write fails during the apply | The transaction rolls back: the state, the check columns, the task and the timer do not move; the user sees MSG-P7-003 | MSG-P7-003 | AC6 |
| X6 | A role without Treatment and offer R reads the check state | Refused; nothing is returned and nothing is written | MSG-P4-002 | AC7 |
| X7 | A user reads the check state of a case outside their scope | Refused with 404; nothing is returned and nothing is written | MSG-P4-003 | AC7 |
| X8 | `CaseWorkflow` is replayed after a worker restart | The recorded answer is reused; no second call to rwb-treatment and no second write | None | AC4 |

The retry policy of a failed step is the platform policy (1 s initial interval, back-off 2, 10 attempts), and `NoPackageInForce` is non-retryable. A rejection under X1 or X2 is a contract failure between two services and is counted in the step metrics of rwb-case; the check itself and its data quality remain the exception of rwb-treatment, which owns the treatment and the collateral read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-S2-E3013-CON contract fake and the platform workflow and decision-record kits; no work order sits inside another team's lane |
| Negotiable | The rule rows, the timer specs, the package versions and the outcome codes are data of the packages and of the S2 contract; the story fixes the case-side behaviour only |
| Valuable | A deed in lieu is not negotiated on an asset that cannot transfer, and the early-readiness work is on the right desk with a due date the case holds |
| Estimable | One step of one workflow, one client, one comparator, one apply service, one migration, one read-only screen field |
| Small | Fits two weeks with its tests |
| Testable | Each of the eight criteria of section 7 is one automated test; the cross-service answer is stubbed in the rwb-treatment contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Check encumbrance and eligibility before negotiation (case side)

  Background:
    Given case "RW-2026-000313" is open with synthetic account "A-0313"
    Given package "DIL" version "DIL-2026.12" is in force with row R-DIL-01
    Given package "SET" version "SET-2026.12" is in force with row R-SET-22

  Scenario: AC1 Route approved moves the case to the early readiness check (new, D-RCV-60)
    Given the case is in state "ROUTE_APPROVED_DIL"
    Given the rwb-treatment contract mock returns the R-DIL-01 answer for "RW-2026-000313" with package version "DIL-2026.12" and check reference "CHK-SYN-0313"
    When the CaseWorkflow EvaluateAndApply step runs for case "RW-2026-000313" on 2026-12-15
    Then the case moves to "EARLY_READINESS_CHECK" by R-DIL-01
    Then the early-readiness task is raised for role "RW-RESTRUCT" with its due date from the timer spec of row R-DIL-01 of version "DIL-2026.12"
    Then CaseWorkflow holds that due date as a durable timer and no Quartz row and no timer check job is written
    Then one decision record names R-DIL-01 and package version "DIL-2026.12"
    Then rwb.case.CaseStateChanged.v1 is published with fromRouteState "ROUTE_APPROVED_DIL" and toRouteState "EARLY_READINESS_CHECK"

  Scenario: AC2 Title documents missing holds the case and raises a task (new, D-RCV-60)
    Given the case is in state "COLLATERAL_RELEASE_REQUESTED"
    Given the rwb-treatment contract mock returns the R-SET-22 answer that the title documents of the asset are missing
    When the CaseWorkflow EvaluateAndApply step runs for the case
    Then a task is raised to re-create the title set before release
    Then the case stays in "COLLATERAL_RELEASE_REQUESTED"
    Then the task carries its due date from the timer spec of row R-SET-22 of version "SET-2026.12" and CaseWorkflow holds it as a durable timer
    Then one decision record names R-SET-22 and package version "SET-2026.12"
    Then no release is requested and no state moves to release

  Scenario: AC3 The check answer is not copied into rwb_case (new, D-RCV-60)
    Given the rwb-treatment contract mock returns the R-DIL-01 answer with outcome code "ELIGIBLE" and check reference "CHK-SYN-0313"
    When the CaseWorkflow EvaluateAndApply step applies the answer
    Then rwb_case stores only the outcome code "ELIGIBLE", the check reference "CHK-SYN-0313" and the ID of the decision record written in the same transaction
    Then no collateral value, no title document number, no plot number and no asset field is written to rwb_case
    Then the step reads no row of the treatment table and no v_ace_collateral, v_ace_collateral_detail or v_ace_npa_asset view (DP-01, DP-05)
    Then the answer body is held only in the decision record and in the workflow history

  Scenario: AC4 A repeated answer changes nothing (new, D-RCV-60)
    Given the step has already applied the answer with check reference "CHK-SYN-0313" for the case
    When the same answer with the same check reference arrives again for the case
    Then the inbox row and the idempotency key absorb the repeat
    Then no second state change, no second task, no second decision record and no second event is written
    Then the case state, the check columns and the durable timer are unchanged
    Then the repeat is counted once in the step summary

  Scenario: AC5 No rule package version is in force (new, D-RCV-60)
    Given the rwb-treatment contract mock returns the NoPackageInForce answer for package "DIL" on 2026-12-15
    When the CaseWorkflow EvaluateAndApply step runs for the case
    Then NoPackageInForce is raised with MSG-P3-027 for package "DIL" and the business date 2026-12-15
    Then the case stays in "ROUTE_APPROVED_DIL"
    Then no task, no timer, no check column and no decision record is written
    Then no CaseStateChanged event is published

  Scenario: AC6 The decision record cannot be written (new, D-RCV-60)
    Given the local decision-record store is unavailable
    When the CaseWorkflow EvaluateAndApply step applies the R-DIL-01 answer
    Then the transaction rolls back and nothing moves: state, check columns, task, timer and outbox row are unchanged
    Then the user sees MSG-P7-003
    Then the retried step with the same answer writes one decision record and one state change

  Scenario: AC7 The check state read is refused without the right or outside the scope (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Treatment and offer R
    Given the rwb-access contract mock returns no Treatment and offer R for role "RW-REFADM"
    When "U-5001" opens the check state of case "RW-2026-000313"
    Then the read is refused with status 403 and MSG-P4-002
    Given a case owner whose scope is "Own" and a case owned by another person
    When that case owner opens the same check state
    Then the response is 404 with MSG-P4-003
    Then the read writes nothing and raises no event

  Scenario: AC8 The check state shows on SCR-16 and SCR-14, read only (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-16 Deed in lieu and SCR-14 Treatment record for case "RW-2026-000313"
    Given the case holds check state "EARLY_READINESS_CHECK" and outcome code "ELIGIBLE"
    When the restructuring officer opens SCR-16
    Then the check state, the outcome code and the due date of the early-readiness task are shown read only
    Then the browser calls one composite route and no owner service directly
    Then no screen call writes a state, a task, a timer, a decision record or an event
```

AC1 to AC8 are new for the rwb-case slice: the four legacy criteria of RWB-E3-013 are proved end to end by RWB-ITG-E3013-ITG and by the S2 slice RWB-S2-E3013-APP, so this story owns no legacy criterion and copies none. The package version labels "DIL-2026.12" and "SET-2026.12", the check reference "CHK-SYN-0313", the outcome code "ELIGIBLE" and the case ID are synthetic test fixtures of the same kind as the legacy "SYN" values; the version in force, the outcome code and the check reference of a real case come from the S2 answer and the rwb-decision registry (GAP-0736; ASM-1321).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The encumbrance and eligibility check is run before a deed in lieu is negotiated, so that a release is not negotiated on an asset that cannot transfer | FEAT-TRT-13; legacy RWB-E3-013 AC1 |
| BR2 | An approved deed-in-lieu route prioritises the lead and starts the early readiness checks; rwb-case starts them on the route approval, never on a batch, schedule or AceDataReady signal | R-DIL-01; legacy RWB-E3-013 AC3 |
| BR3 | When the title documents are missing, CaseWorkflow raises on the reported request a task to re-create the title set before release, on the 5-day clock of R-SET-22, and the case stays in COLLATERAL_RELEASE_REQUESTED | R-SET-22; legacy RWB-E3-013 AC2 |
| BR4 | The check answer is applied by the case workflow that owns the case state; rwb-treatment owns the check, its data and its rule evaluation | RWB-S2-E3013-CON; DP-05; ASM-1316 |
| BR5 | The result is written to the decision record with the rule ID and the rule version; the decision code is the rule ID and the version the evaluated package returned | legacy RWB-E3-013 AC1; DP-03 |
| BR6 | A decision that cannot be recorded does not proceed: the record, the state move, the task and the outbox row are one transaction, and the user sees MSG-P7-003 | Principle 5; legacy RWB-E3-013 AC4; DP-03 |
| BR7 | `NoPackageInForce` is a refusal, never a default move: no state change, no task, MSG-P3-027 | legacy RWB-E3-013 AC1, AC3 read with the platform rule refusal |
| BR8 | A repeated answer for the same check reference changes nothing and raises no second event | legacy RWB-E3-013 AC1; inbox and idempotency key |
| BR9 | The answer is not copied into `rwb_case`: only the outcome code, the check reference and the decision record ID are stored, and collateral and title fields are never read from the treatment tables or from an ACE view | DP-01, DP-05 |
| BR10 | The task due date is the timer spec of the rule row that fired, held as a durable timer of `CaseWorkflow`, not as a scheduler row | R-DIL-01, R-SET-22 timer spec; ASM-1318; platform workflow kit |
| BR11 | Reading the check state requires Treatment and offer R and the caller's scope; a read writes nothing | legacy RWB-E3-013 permission check; MSG-P4-002, MSG-P4-003 |
| BR12 | The case state values of this story are ROUTE_APPROVED_DIL, EARLY_READINESS_CHECK and COLLATERAL_RELEASE_REQUESTED, as named by R-DIL-01 and R-SET-22; no code invents a further state | legacy RWB-E3-013 AC2, AC3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ROUTE_APPROVED_DIL | EARLY_READINESS_CHECK | R-DIL-01 fires on the approved route of the deed in lieu | EARLY_READINESS_CHECK |
| COLLATERAL_RELEASE_REQUESTED | TITLE_SET_RECREATE | R-SET-22 fires and the title documents are missing | COLLATERAL_RELEASE_REQUESTED (no change; task and timer raised) |
| ROUTE_APPROVED_DIL | NoPackageInForce | no SET or DIL version is in force | ROUTE_APPROVED_DIL (no change) |
| Any of the above | apply failed | the decision record cannot be written | unchanged (the whole transaction rolls back) |

These are the case states named by R-DIL-01 and R-SET-22 in the legacy story; on `recovery_case` the state is held in `route_state` (DF-CAS-007) as the sibling rwb-case stories hold it. The case status stays "In progress", and the story writes no stage code and no closure. The legacy AC2 wording — "the case moves to COLLATERAL_RELEASE_REQUESTED" from a case already in COLLATERAL_RELEASE_REQUESTED — is read as the case staying in that state with a task raised, which is the only reading that keeps the release from proceeding on a missing title set.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (its own login, one per service) | Runs the `EvaluateAndApply` step, writes the case state, the task, the timer, the check columns and the decision record |
| rwb-treatment service identity (S2) | Owns the check, reads the collateral data it is entitled to, evaluates SET and DIL, and answers the check result through its contract; never writes the case state |
| CaseWorkflow | Holds the durable timer of the task due date and raises TimerBreached through its own state; moves no state by itself |
| Decision-record library identity | Writes the local decision record and its outbox row in the caller's transaction (DP-03) |
| RW-RESTRUCT, restructuring officer | Receives the early-readiness task and reads the check state on cases in scope (Treatment and offer R) |
| RW-CASEOWN, case owner | Reads the check state on cases in scope and sees the task and its due date (Treatment and offer R) |
| RW-LEGAL, legal officer | Reads the check state on the deed-in-lieu cases in scope (Treatment and offer R) |
| RW-TEAMMGR, team manager | Reassigns a task of the check and reads the cases of the team (Treatment and offer R) |
| RW-REFADM, reference-data administrator | Holds no Treatment and offer R; refused on the read with MSG-P4-002 |

The check is not re-run from the case side by any role: a person who needs a new check asks rwb-treatment, which owns the treatment and the check reference.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more; `route_state` (DF-CAS-007) carries the state this story moves | Read; `route_state` and `rule_version` written |
| DF-CAS-007 | recovery_case | route_state (the case state of section 9) | Write |
| DF-CAS-021 | recovery_case | rule_version (the package version that fired) | Write |
| DF-WRK-017 to DF-WRK-026 | task | id, case_id, task_code, element_type, discretion, status and 4 more; the task of AC1 and AC2 with its `due_at` | Write |
| DF-WRK-009 to DF-WRK-016 | assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more; the placement of the raised task | Write |
| DF-WRK-030, DF-WRK-031, DF-WRK-035 | timer | timer_type, started_at, status; the screen projection of the due date behind the timers read | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, in rwb_case) and decision_log_entry (rwb_decision) | all fields | Write locally in the same transaction; the central entry is sealed by rwb-decision |
| DF-TRT-001 to DF-TRT-014 | treatment (rwb_treatment, owner S2) | the treatment and deed-in-lieu agreement of the case | Not read and not written: the check answer is a contract field, and the treatment belongs to S2 (DP-01) |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral (read by S2/P1, not by rwb-case) | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and 2 more | Not read: ACE data reaches the case only through rwb-treatment's answer or the P1 contract (DP-05) |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail (read by S2/P1, not by rwb-case) | asset_key, title_doc_no, plot_no, area_text, province, lien_rank and 6 more | Not read; the missing-title outcome arrives as the R-SET-22 answer |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (read by S2/P1, not by rwb-case) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read |

Three columns are added to `recovery_case` for the case-side record of the check (`check_ref`, `check_outcome_code`, `decision_record_id`); their field IDs in the Logical Data Model and Data Dictionary are Not specified in the source documents (GAP-0736; ASM-1320), so the table above cites the existing entity range and the three columns by name.

The answer fields themselves — the rule ID, the package version, the outcome code, the check reference and the task instruction — are read from the rwb-treatment contract and are stored only as the outcome code, the check reference and the decision record ID. No collateral row, title document row, plot row or asset row is written into `rwb_case`, and no foreign key crosses a schema (DP-01).

### 12. Contract

Encumbrance and title statuses are values of the ACE read: they are never a column of rwb_treatment and never derived in code.

#### 12.1 REST operations provided

None. This story adds no person-facing operation and no new path: the check state is shown on SCR-16 and SCR-14 from the existing case read `GET /api/recovery/case/v1/cases/{caseId}` of rwb-case, composed by the gateway-bff composite route (DP-19), and the state move writes nothing that a caller posts. The legacy deed-in-lieu read of the treatment record on the old base becomes rwb-treatment's `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (DP-13), owned by S2 and not by this story.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| — | Not specified in the source documents (GAP-0736; ASM-1316) | rwb-treatment (S2) | The encumbrance and eligibility check answer of RWB-S2-E3013-CON for the case: the rule ID (R-DIL-01 or R-SET-22), the package version, the outcome code, the check reference and the task instruction; built against the contract and its fake | One hop, 2 s, breaker |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Treatment and offer R right, the Case record right and the scope before a person read, cached by the guard library | One hop, 2 s |

The check-answer operation is the only service call of this story; its method, its path and its field names are fixed by RWB-S2-E3013-CON, and rwb-case makes no call to rwb-source-data, to an ACE view or to rwb-decision for this check.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | caseId | caseId, decisionLogEntryId, fromState, ruleId (R-DIL-01 or R-SET-22), toState |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, rule ID, package version, business date |

Both are written to the outbox in the same `rwb_case` transaction as the state move and relayed with the CloudEvents envelope; no personal data is carried and the account number is not in any payload.

#### 12.4 Events consumed

None. The check answer arrives by a REST call inside the workflow step (12.2), so this story consumes no event and opens no consumer of its own; the inbox row is used only to deduplicate a repeated answer (AC4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case-{caseId}) | `rwb-case` | Holds the case from entry to closure, runs the step for the check answer, and waits on the durable timer of the task due date |
| EvaluateAndApply | Step of CaseWorkflow (in-workflow, no separate activity) | `rwb-case` | Calls the S2 check-answer operation, rejects an answer that names neither rule, applies the state move or the hold, and writes the task, the timer, the check columns, the decision record and the outbox rows in one transaction |
| durable timer | Timer of CaseWorkflow | `rwb-case` | Holds the due date of the early-readiness task or of the title task and raises TimerBreached through the workflow state |

No other activity is added. The rule evaluation is not done here: it is S2's, and this story only applies the answer it receives.

#### 12.6 Schedules

None. The step is started by the case workflow on the deed-in-lieu route, not by a Schedule, and no Quartz row and no timer check job is created.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The story adds `check_ref`, `check_outcome_code` and `decision_record_id`, and writes `route_state`, `rule_version` and the status of the case |
| task | P3 (rwb_case) | The early-readiness task of R-DIL-01 and the title task of R-SET-22, with `task_code` and `due_at` |
| timer | P3 (rwb_case) | The screen projection of the due date; the clock itself is the durable timer of CaseWorkflow |
| outbox_event | PLT library, created in rwb_case | The published events of 12.3, written in the same transaction |
| processed_event | PLT library, created in rwb_case | The inbox row that absorbs a repeated answer |
| idempotency_key | PLT library, created in rwb_case | The key of the answer: case ID, check reference and outcome code |
| decision_record | P3 (rwb_case) | The local decision record of the move or hold, hash-linked, written in the same transaction (DP-03) |

Treatment rows are S2's and the collateral, collateral-detail and NPA rows are ACE's, read by S2 and by P1: rwb-case holds no copy, no foreign key and no cross-schema join (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-treatment WireMock | The S2 contract of RWB-S2-E3013-CON | The R-DIL-01 answer with package version "DIL-2026.12"; the R-SET-22 missing-title answer with package version "SET-2026.12"; a delayed answer beyond 2 s; the `NoPackageInForce` answer; an unreadable answer (no rule ID) |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Treatment and offer R, refusing it for RW-REFADM, and excluding a case from an Own scope |
| gateway-bff composite route (WireMock) | The DP-19 route of SCR-16 and SCR-14 | The composed read-only check state of AC8 |
| rwb-source-data WireMock | The rwb-source-data contract, the only reader of ACE views (P1 and S2 reach ACE through it) | The ACE-derived facts that AC3 needs, as the contract returns them; no v_ace_collateral, v_ace_collateral_detail or v_ace_npa_asset row is set up directly |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | No operation provided; the S2 check answer and the P4 authorise consumed; one hop, 2 s |
| Kafka | 2 published, 0 consumed | `rwb.case.events.v1` and `rwb.decision-record.v1` published through the outbox |
| Temporal | 1 workflow | CaseWorkflow, with the EvaluateAndApply step and the durable timer; no new activity |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `encumbrance`, Java package `th.co.scb.ace.workbench.recovery.case.encumbrance`; front end `src/modules/recovery/case/EncumbranceCheckState.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/<service>` base of the monolith | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the schema rule behind the store boundary of 12.7 and AC3 (no read of another service's table); it adds no dependency and is not a pattern change of this story. DP-05 resolves to no ACE view and no rwb-source-data call here: rwb-case reads no collateral, no collateral detail and no NPA row, because the check and its data belong to rwb-treatment and the ACE views belong to rwb-source-data. The H and C dependencies this table adds are held by the platform contract stories and are not repeated in the metadata rows, which carry only the contract dependency of the legacy read: RWB-S2-E3013-CON (ASM-1317).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CheckAnswerClient | Client | Calls the rwb-treatment check-answer operation with one hop, the 2 s timeout and a breaker; rejects an answer that names neither R-DIL-01 nor R-SET-22 |
| CheckAnswerComparator | Service | Builds the idempotency key from case ID, check reference and outcome code and reports a repeat so nothing is written twice |
| CheckOutcomeApplier | Service | Maps the answer to the case-side outcome: the move to EARLY_READINESS_CHECK by R-DIL-01, the hold in COLLATERAL_RELEASE_REQUESTED with the title task by R-SET-22, and the refusal on `NoPackageInForce` |
| CaseCheckRepository | Repository | Writes `route_state`, `rule_version`, `check_ref`, `check_outcome_code` and `decision_record_id` in schema `rwb_case` only |
| TaskTimerWriter | Service | Writes the task row with its `task_code` and `due_at` from the rule's timer spec, the assignment and the `timer` projection, and signals the due date to CaseWorkflow |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the rule ID and the package version, hash-linked, in the same transaction (DP-03) |
| CaseCheckEventPublisher | Outbox adapter | Inserts CaseStateChanged and DecisionRecorded in the outbox in the same transaction |
| EncumbranceCheckState | React component | Shows the check state, the outcome code and the task due date on SCR-16 and SCR-14, read only |

**Database and migrations**

- Migration `V3013_1__encumbrance_check.sql` adds `check_ref` varchar(40), `check_outcome_code` varchar(20) and `decision_record_id` uuid to `recovery_case`, nullable, with no database constraint on the outcome code (the list is validated by the contract of S2).
- No new table: the task, the timer, the assignment, the outbox, the inbox, the idempotency and the decision-record tables already exist in `rwb_case`.
- One index for the read of a case by its check reference: `ix_recovery_case_check_ref ON recovery_case (check_ref) WHERE check_ref IS NOT NULL`.
- The migration runs in the rwb-case Flyway sequence of the service's own schema; no other schema is touched.

**Configuration and reference data**

- The rule rows R-DIL-01 and R-SET-22, their action text, their owner role and their timer spec are the data of packages DIL and SET and are owned by rwb-decision with RW-COE as their author; this story reads none of them directly and receives the timer spec in the answer (ASM-1316).
- No parameter and no list of values is added by this story; the check's own parameters belong to rwb-treatment.
- The role that holds the early-readiness task is the owner role the rule row names, RW-RESTRUCT for R-DIL-01.

**Build steps**

1. `CheckAnswerClient` against the RWB-S2-E3013-CON fake, with the 2 s timeout, the breaker and the rejection of an answer that names neither rule; tests for AC3 and AC1.
2. `CheckAnswerComparator` and the idempotency key; test for AC4.
3. `CheckOutcomeApplier` with the two outcomes and the refusal; tests for AC1, AC2 and AC5.
4. `CaseCheckRepository` and `DecisionRecordWriter` in one transaction with the outbox rows; test for AC6.
5. `TaskTimerWriter` with the due date from the timer spec, the assignment and the signal to CaseWorkflow; tests for AC1 and AC2.
6. Register `EvaluateAndApply` into CaseWorkflow for the deed-in-lieu route and run a replay test, so the recorded answer is reused; test for AC4.
7. The access check and the scope on the read path, with the existing case read; test for AC7.
8. `EncumbranceCheckState` and the composite-route contract test; test for AC8.

**Feature switch.** None is named in the legacy story. The step is reached only when the case is on the deed-in-lieu route and the S2 check answer exists for the case, so the route itself is the switch; a check that has not been run raises no task and moves no state.

**Done when.** The tests in section 16 pass, the RWB-S2-E3013-CON contract tests stay green, every apply of this story leaves one decision record naming its rule ID and its package version, and no case in the SIT run is released on an asset whose title answer said the documents are missing.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-002 | The payoff shown on the deed-in-lieu screen is from an earlier date | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-001 | An offer below the floor is submitted | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | An offer with an end date is shown | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A required field is missing, or the check answer cannot be used | Enter {field}. |
| MSG-P3-027 | No SET or DIL version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without Treatment and offer R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A case outside the caller's scope | This case is not in your scope. |

MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the messages of the S2 check and offer screens and are listed here because the legacy story carries them; the case side renders none of them, and the check state is read only on the case screens. For MSG-P3-027 in this story, {check} is "no package in force" and {table} names the package code "DIL" or "SET" only, never a case fact. MSG-GEN-001 is used on the contract path only where the answer is unusable; the case screens add no field of their own.

### 15. Screens and states

| Screen | States shown for this story |
|---|---|
| SCR-16 Deed in lieu | The check state and the outcome code of the case, and the due date of the early-readiness task, read only; the screen keeps its own states Checks, appraisal, approved and transferred from S2; empty, loading, error and no access: Not specified in the source documents (CG-ALL-4462) |
| SCR-14 Treatment record | The same check state on the case record of the deed in lieu, read only; the screen keeps its own states Draft, submitted, approved, booked and broken from S2; empty, loading, error and no access: Not specified in the source documents (CG-ALL-4461) |

Both screens are served by the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of rwb-treatment, one hop each, read only (DP-19); the browser calls no owner service directly. The screen writes nothing: a person who needs the check repeated asks rwb-treatment, and a person who needs the task closed does it on the task, not on the check state. The full read-only case record view, the timer section and the deviation flag remain with RWB-P3-E1023-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-013-01 | AC1, AC3, AC4, AC8 | Component | rwb-treatment stub returns the R-DIL-01 answer with version "DIL-2026.12" and check reference "CHK-SYN-0313"; case in ROUTE_APPROVED_DIL |
| TC-E3-013-02 | AC2 | Component | rwb-treatment stub returns the R-SET-22 missing-title answer; case in COLLATERAL_RELEASE_REQUESTED |
| TC-E3-013-03 | AC1, AC5 | Component | rwb-treatment stub returns `NoPackageInForce` for package "DIL" on 2026-12-15; case in ROUTE_APPROVED_DIL |
| TC-E3-013-04 | AC6 | Component | The local decision-record store is stopped; the R-DIL-01 answer is applied |
| TC-E3-013-05 | AC7 (Access) | Component | RW-REFADM without Treatment and offer R; a case owner with scope Own and a case of another owner |
| TC-E3-013-06 | AC6 (NFR) | NFR | The decision-record write is forced to fail on the R-DIL-01 move; state, task, timer and outbox row unchanged |
| TC-E3-013-07 | Section 12 operations, events and activities | Contract | Provider contract check against RWB-S2-E3013-CON |
| TC-E3-013-08 | Section 12.7 tables | Component | Boundary values of the columns that section 12.7 names for each table |

The legacy levels map System to Component, Access to Component and Resilience to NFR, because the cross-service behaviour of this key is proved by the integration story. The `-ITG` copy of each case is held by RWB-ITG-E3013-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the rule IDs, the package versions, the outcome codes, the timer specs, the states and the owner role are data of the packages and of the S2 contract, not constants.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs, check references and rule IDs, never account numbers, names or identity numbers; the workflow payloads pass the payload codec.
- No read of another service's tables and no ACE view: the check answer comes from the rwb-treatment contract, the rights from rwb-access, and `rwb_case` holds no foreign key into another schema (DP-01, DP-05).
- One owner of the check: the encumbrance and title check is run only by rwb-treatment; rwb-case applies the answer and never re-evaluates a rule or re-reads collateral for it.
- A read of the check state writes nothing and raises no event.
- The decision record is written in the same transaction as the state move; a failed write rolls the whole apply back (MSG-P7-003).
- `NoPackageInForce` is never caught and turned into a default move.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None in the source: RWB-E3-013 carries no requirement ID in Epics 3 to 8 v3 (GAP-0736; ASM-1316) | The encumbrance and title checks are run early, so a deed in lieu is not negotiated on an asset that cannot transfer | Epics 3 to 8 v3, RWB-E3-013, module S2 TDR, settlement and deed in lieu | FEAT-TRT-13 | See module (Epics 3 to 8 v3, RWB-E3-013); not named in the source documents | R-DIL-01, R-SET-22 | TC-E3-013-01, TC-E3-013-02, TC-E3-013-03, TC-E3-013-04 |
| None in the source (GAP-0736; ASM-1316) | The result is written with the rule version, and a decision that cannot be recorded does not proceed | Epics 3 to 8 v3, RWB-E3-013; Template and Rules §R5.5 DP-03 | FEAT-TRT-13 | See module | R-DIL-01, R-SET-22 | TC-E3-013-01, TC-E3-013-05, TC-E3-013-06 |
| None in the source (GAP-0736; ASM-1316) | Treatment and offer R is required to read the check state, and the read is scoped | Epics 3 to 8 v3, RWB-E3-013 permission checks | FEAT-TRT-13 | See module | R-DIL-01, R-SET-22 | TC-E3-013-05 |

The Epics 3 to 8 story RWB-E3-013 carries no requirement ID, so this table traces to the feature, the two rules and the test cases instead; the requirement IDs are added when the BRD for EP03 is produced (C1).

### 19. Out of scope

- The encumbrance and eligibility check itself, the treatment record, the deed-in-lieu agreement and the rule evaluation of SET and DIL (rwb-treatment, RWB-S2-E3013-APP).
- The ACE collateral, collateral-detail and NPA views and the contract that serves them (rwb-source-data, P1).
- The offer, the floor, the payoff figure and the message set of the offer screens (S2).
- The negotiation and approval of the deed in lieu, and the asset transfer and registration (S2 and the asset stories).
- The rights, the roles and the scope data themselves (P4 access stories).
- The gateway-bff composite route implementation (the platform DP-19 story).
- The full read-only case record view, the timer section and the deviation flag (RWB-P3-E1023-APP).
- The rule authoring, approval and promotion of packages SET and DIL (RWB-P3-E2041-APP, RWB-P3-E2042-APP).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
