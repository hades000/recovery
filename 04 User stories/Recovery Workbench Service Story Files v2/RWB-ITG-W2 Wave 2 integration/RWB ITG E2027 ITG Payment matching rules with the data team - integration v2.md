# RWB-ITG-E2027-ITG Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2027-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2027-CON |
| Contract version | v1 on the five owner bases of section 12.2 (`/api/recovery/<short>/v1`) |
| Integration dependencies | RWB-P3-E2042-APP, RWB-P8-E2027-APP, RWB-P4-E2027-APP, RWB-S2-E2027-APP, RWB-P7-E2027-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-CHO-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-027 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E2027-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (38 resolved, 22 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a repeatable cross-service journey harness for the PAYMENT_MATCH matching journey, with the fired rule row, the package version, the decision ledger entry and the proceeds outcome of one business date captured as evidence against the wave 2 release**, so that **the matching journey is proven end to end across rwb-payment, rwb-decision, rwb-case, rwb-access and rwb-treatment before the app stories of RWB-E2-027 are signed off**.

This is the wave 2 **integration harness** for legacy RWB-E2-027. It builds no production endpoint, no screen, no table and no migration. It exercises the published operations of the five services involved: rwb-payment (P8) for the proceeds and the match, rwb-decision (P7) for the rule-package registry and the central decision ledger, rwb-case (P3) for the case, the account and the plan, through the rule-package authoring story RWB-P3-E2042-APP, rwb-access (P4) for the session and the rights, and rwb-treatment (S2) for the installment shortfall. Contract fakes stand in for each service until its I story lands. The story owns a seed pack, an evidence pack and a pass or fail gate, and nothing else.

The rule package is the unit under test. The harness loads PAYMENT_MATCH version "PM-2026.12", runs the journey against the ALS payment fixture for one business date, and asserts that one rule row, one package version and one ledger entry agree on every match across the five services.

### 2. Business rationale

RWB-E2-027 splits into five app stories and this integration story. The app stories build the rule-package authoring operation and the registry in rwb-decision, the matching activity and the proceeds in rwb-payment, the session and rights in rwb-access, the case and plan read in rwb-case, and the installment shortfall in rwb-treatment. None of them can prove on its own that **one rule row, one package version and one ledger entry agree across five services on one business date**: rwb-payment fires row "PARTIAL" of version "PM-2026.12", writes decision code "D5" with rule "PARTIAL" and version "PM-2026.12", passes the shortfall to rwb-treatment, and the proceeds entry, the decision entry and the plan shortfall all name the same package version. That proof is this story.

The journey is the one the business cares about. A payment arrives in the ACE payment view for the business date, JOB-07 matches it against the running plan by the rule rows in force, the short and late installments match without a person, and anything that matches no row is on the exception list with a reason (REQ-CHO-009, control CTL-41). The measure is the P8 measure "receipts matched the same day": every match names its rule and its package version, and every unmatched receipt carries a reason. The harness runs that measure on synthetic data, on one business date, and produces evidence that can be re-run for any build.

The architecture changes the path, not the business. The monolith ran one matcher inside one module against one rule table. In the target:

- The rule registry, the rule rows and the rule test cases are owned by rwb-decision (P7), and the evaluator is the embedded Drools kit inside the owning service (DP-04, ADR-017). rwb-payment loads the version on `RulePackageInForce` (JOB-20), verifies the checksum and swaps it in.
- The decision record is written by rwb-payment in its own schema in the same transaction as the state change, then collected into the central ledger in rwb-decision (DP-03, ADR-022), and published on `rwb.decision-record.v1`.
- ACE payment and account data are read through rwb-source-data's contract or through rwb-payment's own ACE views (DP-05); nothing reads another service's tables (DP-01).
- Parameters and reference data come from rwb-case (DP-06, DP-07); the match type, row order, tolerance, window, grace and partial floor stay columns of the rule rows, never code and never a reference table (D-RCV-36 T10).
- JOB-07 is an event-started workflow in rwb-payment, started by `AceDataReady`, with activity `matchPayments` (DP-10, Arch v5 slide 44), not a Quartz job.
- Every call is one hop on the owner's base with a 2 s timeout (DP-11), every path is `/api/recovery/<short>/v1` (DP-13), every topic is `rwb.<short>.events.v1` (DP-14), every service keeps its own Flyway sequence (DP-15), and the screen path runs through gateway-bff (DP-19).

The harness is the place where those boundaries are exercised together, so a broken boundary is found in SIT and not by a payment that silently matches the wrong installment.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the Kafka topics of the five services and the shared topic `rwb.decision-record.v1`, and the Temporal namespace `rwb-recovery` with queue `rwb-payment`. The harness environment, its seeding mechanism and its evidence format: Not specified in the source documents (GAP-0409; ASM-0584).
- The five integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P3-E2042-APP (rwb-case, the rule-package authoring operation), RWB-P8-E2027-APP (rwb-payment), RWB-P4-E2027-APP (rwb-access), RWB-S2-E2027-APP (rwb-treatment) and RWB-P7-E2027-APP (rwb-decision).
- PAYMENT_MATCH package version "PM-2026.12" is in force from 2026-12-01 with the EXACT, WINDOW and PARTIAL rows of section 7, loaded through the rwb-decision rule-package operation and approved by RW-RISK (legacy sections 3 and 7 Background). The rows are tried in the order EXACT, then PARTIAL, then WINDOW, as the Temporal and Drools design gives it; this replaces the RWB-E2-027 order EXACT, WINDOW, PARTIAL, and the decision and rules lead confirms it with Credit Administration and carries it in the PAYMENT_MATCH scenario set (GAP-3180).
- "PM-2026.12" from 2026-12-01 is read as the one version in force for PAYMENT_MATCH. RWB-E2-042 records the same package as "PMT-2026.12" from 2026-12-15; the rule owner RW-COE, with the P7 and P3 solution architects, reconciles the two to one version row, one label and one valid-from date before the package is promoted in SIT (GAP-1292, GAP-1297, GAP-2506).
- Case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15 (legacy section 7 Background).
- The decision entry of every match carries decision code "D5" and names the rule ID (EXACT, WINDOW or PARTIAL) and the package version in force on the business date (legacy BR6).
- The test user holds RW-CREDITAD or another role with Write-off and posting R; the author of a package version holds RW-COE with Rules and parameters C and the approver holds RW-RISK with Rules and parameters A (legacy section 10).
- Synthetic payments only: no real account, customer or payment data enters the harness or its evidence (legacy section 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the five contracts it is about to exercise.
2. Harness: seeds case "RC-2026-000555", account "A-0555", plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15, and loads PAYMENT_MATCH version "PM-2026.12" through `POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions`, then confirms it is in force through `GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions`.
3. Harness: calls the P4 session operation `GET /api/recovery/access/v1/me/session` for the test user and records the role, the scope and the Write-off and posting right it will exercise.
4. Harness: calls the P3 case operation `GET /api/recovery/case/v1/cases/{caseId}` and records the case state, the account and the running plan the journey starts from.
5. Harness: loads the ALS payment fixture for the business date — for the exact, partial, late, below-the-floor, overpayment and two-row cases of section 7 — and records the fixture file hash and the payment codes it contains.
6. Harness: opens the JOB-07 window by publishing the `AceDataReady` event for the business date on `rwb.source-data.events.v1` and records the workflow ID of the event-started JOB-07 run it starts in rwb-payment.
7. Harness: reads the proceeds through `GET /api/recovery/payment/v1/proceeds`, matched and unmatched, and records the payment code, the amount, the matched-to value and the treatment ID of each row (AC1, AC2, AC4, AC5, AC8, AC9).
8. Harness: reads the decision log entries through `GET /api/recovery/decision/v1/decision-log` and records the decision code, the rule ID, the package version and the inputs reference of each entry (AC1, AC2, AC3, AC4, AC9).
9. Harness: reads the treatment shortfall through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and records installment amount, due date and installment shortfall (AC2).
10. Harness: asserts the package version on each entry — the version in force on the business date, and the earlier version on an earlier match (AC3) — and marks the scenario failed when any entry names another version or none.
11. Harness: subscribes to `rwb.payment.events.v1` and to `rwb.decision-record.v1` for the run window with its own consumer group and asserts `ProceedsMatched`, `PaymentMissed` and `DecisionRecorded` for the case and the business date.
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate, attaches the report to the wave 2 release record and releases the run lock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | The payment is unmatched, carries MSG-P8-001 in the run summary and appears on the exception list | MSG-P8-001 | AC5 |
| X2 | A late payment outside the window | The payment is unmatched with a decision entry under R-UNI-03 and appears on the exception list | MSG-P8-001 | AC4 |
| X3 | A package version is loaded with two rows of the same row order or a tolerance above 100 | The load is refused in full with status 422 and "PM-2026.12" stays in force; the harness asserts the refusal and never lets the bad version into the run | MSG-P3-027 | AC11 |
| X4 | The decision log write fails for a match | No proceeds row is written, the run summary shows MSG-P7-003, an incident is raised under R-UNI-39 and the next run matches the payment; the scenario passes only when the proceeds read confirms no row | MSG-P7-003 | AC12 |
| X5 | A payment above the installment by more than the tolerance | The payment is unmatched and appears in the unmatched proceeds read | MSG-P8-001 | AC8 |
| X6 | Two rows would match the same payment | The row with the lower row order decides and exactly one decision entry is written | None | AC9 |
| X7 | No PAYMENT_MATCH version is in force on the business date | The run of JOB-07 stops, no payment is matched and no proceeds row is written; the harness records the refusal and fails the gate for that business date | MSG-P3-027 | AC13; TC-E2-027-16-ITG |
| X8 | The seed pack cannot be loaded, another run holds the environment lock, or the evidence pack cannot be attached to the release record | The run refuses to start and names the missing seed item or the lock holder, or is marked failed with the local evidence file kept for rerun; no scenario is reported as passed | None | AC14; TC-E2-027-17-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the five published contracts or their fakes, the ALS payment fixture and the JOB-07 window; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded case, the fixture payments and the expected rule IDs are data files, never code |
| Valuable | The matching journey is proven once across five services, with the rule row and the package version agreeing on every entry |
| Estimable | One journey runner, one fake set, one seed pack, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a scenario with a fixed Given, When and Then and a recorded result |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given PAYMENT_MATCH package version "PM-2026.12" is in force from 2026-12-01 with rows:
      | rule_id | row_order | match_type | amount_tolerance_pct | window_days_before | window_days_after | partial_floor_pct |
      | EXACT   | 1         | EXACT      | 0                    | 10                 | 0                 |                   |
      | PARTIAL | 2         | PARTIAL    | 0                    | 10                 | 3                 | 90                |
      | WINDOW  | 3         | WINDOW     | 0                    | 10                 | 3                 |                   |
    # Row order EXACT, PARTIAL, WINDOW follows the Temporal and Drools design and replaces the RWB-E2-027 order EXACT, WINDOW, PARTIAL (GAP-3180).
    Given case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15

  Scenario: AC1 Exact match (legacy RWB-E2-027 AC1)
    Given the ALS load for 2026-12-14 holds payment "PAY-91001" of 12,500.00 THB on the plan account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91001" to "INSTALLMENT" for "T-0701" in that run
    Then the decision log entry for the match has decision code "D5", rule "EXACT" and rule version "PM-2026.12"

  Scenario: AC2 Partial (legacy RWB-E2-027 AC2)
    Given the ALS load for 2026-12-14 holds payment "PAY-91002" of 11,875.00 THB on account "A-0555", 5 percent short
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91002" to "INSTALLMENT" for "T-0701" with rule "PARTIAL"
    Then the system calls treatmentApi.recordInstallmentPaid with amount 11,875.00 and shortfall 625.00
    Then plan "T-0701" shows a shortfall of 625.00 THB for due date 2026-12-15

  Scenario: AC3 Rule change (legacy RWB-E2-027 AC3)
    Given PAYMENT_MATCH version "PM-2027.01" is loaded and approved with valid from 2027-01-01, changing WINDOW to 5 days after
    Given the ALS load for 2027-01-04 holds payment "PAY-91003" of 12,500.00 THB on account "A-0555" for due date 2026-12-31, 4 days late
    When JOB-07 runs on 2027-01-05
    Then the system matches "PAY-91003" to "INSTALLMENT" with rule "WINDOW"
    Then the decision log entry has rule version "PM-2027.01"
    Then the match of "PAY-91001" keeps rule version "PM-2026.12"

  Scenario: AC4 Late payment inside and outside the window (legacy RWB-E2-027 AC4)
    Given the ALS load for 2026-12-18 holds payment "PAY-91004" of 12,500.00 THB on account "A-0555", 3 days after due date 2026-12-15
    Given the same load holds payment "PAY-91005" of 12,500.00 THB on account "A-0666" of plan "T-0702", 4 days after its due date 2026-12-14
    When JOB-07 runs on 2026-12-19
    Then the system matches "PAY-91004" with rule "WINDOW" and P3 receives PAYMENT_RECEIVED_LATE under R-RES-28
    Then the system matches "PAY-91005" to "UNMATCHED" with a decision log entry under rule "R-UNI-03"

  Scenario: AC5 Partial below the floor (legacy RWB-E2-027 AC5)
    Given the ALS load for 2026-12-14 holds payment "PAY-91006" of 10,000.00 THB on account "A-0555", 80 percent of the installment
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91006" to "UNMATCHED"
    Then the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14

  Scenario: AC8 Overpayment beyond the tolerance (legacy RWB-E2-027 AC8)
    Given the ALS load for 2026-12-14 holds payment "PAY-91007" of 13,000.00 THB on account "A-0555"
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91007" to "UNMATCHED" and appears in GET /proceeds?matched=false

  Scenario: AC9 Lowest row order decides (legacy RWB-E2-027 AC9)
    Given the ALS load for 2026-12-14 holds payment "PAY-91008" of 12,500.00 THB on account "A-0555", which both "EXACT" and "WINDOW" match
    When JOB-07 runs on 2026-12-15
    Then the system matches "PAY-91008" with rule "EXACT"
    Then the system writes one decision log entry for "PAY-91008"

  Scenario: AC11 Package refused on duplicate row order or tolerance above 100 (exception X3) (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2027.02" is loaded with two rows of the same row order and a tolerance of 120
    When the version-load check runs
    Then the load is refused in full with status 422 and MSG-P3-027
    Then "PM-2026.12" stays in force and the bad version is not used by JOB-07

  Scenario: AC12 Decision log write fails (exception X4) (new, D-RCV-60)
    Given the ALS load for 2026-12-14 holds payment "PAY-91001" of 12,500.00 THB on account "A-0555" and the decision log is unavailable
    When JOB-07 runs on 2026-12-15
    Then no proceeds row is written for "PAY-91001"
    Then the run summary shows MSG-P7-003 and an incident is raised under R-UNI-39
    Then the next run matches "PAY-91001" to "INSTALLMENT"

  Scenario: AC13 No version in force (exception X7) (new, D-RCV-60)
    Given no PAYMENT_MATCH version is in force on 2027-02-01
    When JOB-07 runs on 2027-02-01
    Then the run stops, no payment is matched and no proceeds row is written
    Then the harness records the refusal with MSG-P3-027 and the business date gate fails for 2027-02-01

  Scenario: AC14 Environment not ready (exception X8) (new, D-RCV-60)
    Given the seed pack cannot be loaded, or another run holds the environment lock, or the evidence pack cannot be attached
    When the harness starts the run
    Then the run refuses to start and names the missing seed item or the lock holder, or is marked failed with the local evidence file kept
    Then no scenario is reported as passed

  Scenario: AC15 Thresholds are read from the package row (legacy RWB-E2-027 BR10) (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2026.12" is in force with the rows of the Background
    When JOB-07 runs on 2026-12-15 for the payments of the Background
    Then the tolerance, window, grace and partial floor used for each match are the values of the row that fired
    Then no threshold is held in the harness code or in a reference table

  Scenario: AC16 Duplicate delivery of a consumed event (new, D-RCV-60)
    Given the ALS load for 2026-12-14 holds payment "PAY-91001" of 12,500.00 THB on account "A-0555" and JOB-07 has consumed it on 2026-12-15
    When the "ProceedsMatched" event of that match is delivered again
    Then no second match is made for "PAY-91001"
    Then exactly one decision log entry exists for "PAY-91001"

  Scenario: AC17 Consumed call fails or does not answer (new, D-RCV-60)
    Given the ALS load for 2026-12-14 holds payment "PAY-91002" of 11,875.00 THB on account "A-0555" and the call to treatmentApi.recordInstallmentPaid fails or does not answer
    When JOB-07 runs on 2026-12-15
    Then the failed call is shown in the run summary
    Then the scenario is not reported as passed

  Scenario: AC18 Disallowed status change is refused (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2026.12" is in force
    When a status change is requested that the status model does not allow
    Then the change is refused
    Then "PM-2026.12" stays in force
```

AC6, AC7 and AC10 are owned by the app stories of this legacy key and are cited only through their test cases, TC-E2-027-06-ITG, TC-E2-027-07-ITG and TC-E2-027-10-ITG. The AC6 package load is read through the rwb-decision contract mock (C RWB-P7-E1073-CON).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Rows are tried in row order and the first row that matches decides (first match) | D-RCV-36 T5; ADR-012 |
| BR2 | EXACT: plan account, amount within the tolerance, date inside the window before the due date | R-RES-26 |
| BR3 | WINDOW: as EXACT, with the window extended after the due date; a late match is a late payment for the plan | R-RES-28 |
| BR4 | PARTIAL: amount at or above the partial floor and below the installment; the shortfall is held on the plan | R-SET-15 pattern; REQ-CHO-009 |
| BR5 | A payment no row matches is held on the exception list | R-UNI-03; CTL-41 |
| BR6 | Each match decision is written to the decision log with the rule ID (EXACT, WINDOW or PARTIAL) and the package version in force on the business date; earlier matches keep their version | R-UNI-38; Principle 5; D-RCV-36 T5, T7 |
| BR7 | A package version with any invalid row is refused in full by the version-load check | Reference data change process, step 3; CTL-08 |
| BR8 | A match that cannot be written to the decision log is not made | Principle 5; R-UNI-39 |
| BR9 | No PAYMENT_MATCH version in force is a refusal (NoPackageInForce), never a default match | D-RCV-36 T3; R-UNI-41 |
| BR10 | The tolerance, window, grace and partial floor are condition and output columns of the PAYMENT_MATCH rows, not code and not a reference table | D-RCV-36 T10; REQ-CHO-009 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and never restates a threshold in its own code; every threshold is read from the row the package fired.

### 9. State transitions

None for the case. This story does not change a case status. rwb-treatment holds the plan state (PLAN_RUNNING, PLAN_CURE_PERIOD, PLAN_BROKEN, BACK_TO_ROUTE_DECISION) on the standard `state` column of the treatment row, from the match consequence read that RWB-P8-E2027-CON is to publish (section 12.2). On a breach it writes outcome BROKEN and `outcome_at`, and stamps the rule ID and package version on its local decision record; the decision code of a plan-breach record: Not specified in the source documents (GAP-1880). The plan check is one durable timer of the workflow with the 30-day cure period of the design. The harness observes these transitions:

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (R-RES-26) |
| PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | PLAN_RUNNING (R-RES-28) |

The package version moves LOADED to APPROVED to IN_FORCE, or to REFUSED, through the rwb-decision rule-package operations; the harness drives the first three and asserts REFUSED for the invalid version of X3.

The harness adds a run state of its own only: Not started, Seeding, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads the matched and unmatched receipts and the exception list in the evidence (Write-off and posting CRUA); owns the matching values |
| RW-COE, center of excellence analyst | Authors the PARTIAL and WINDOW rows and loads the package version the harness seeds (Rules and parameters C) |
| RW-RISK | Approves the seeded package version (Rules and parameters A) |
| RW-FINANCE, Finance and CFO delegate | Reads the matches in the evidence (Write-off and posting RA) |
| SY-RULES, Drools evaluator | Supplies the fired rule ID and the package version through the rwb-payment contract |
| SY-DECLOG, decision log writer | Supplies the D5 entries the harness asserts, through rwb-decision's contract only |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent would (Write-off and posting R, TSD P8 T6.1), not exercised here |
| RW-TRIBE, squad members and the QA team | Run the harness, keep the fake mappings, the seed pack and the evidence, read reports |
| Integration lead | Agrees the ALS payment fixture, the JOB-07 window control and the contract versions with the five service teams |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

Separation of duty: the analyst who loads a version does not approve it; RW-RISK approves and the author cannot. The harness seeds both steps with two distinct test users and never with one.

Access profile: the capability areas are the LOV-CAPABILITY values `WRITE_OFF_AND_POSTING` and `RULES_AND_PARAMETERS` (TSD P4), and the access matrix versions are "PM-2026.11" and "PM-2026.12" (FSD P4 AC-P4-004-01); these are matrix versions, not PAYMENT_MATCH package versions. The four role letters in the table above are unchanged. The parameter set of the access profile and the database login name are open, to be confirmed with the security administrator before the wave 2 test set is signed: Not specified in the source documents (GAP-2311).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043 | v_ace_payment | payment_code | Read through the P8 proceeds operation |
| DF-ACE-044 | v_ace_payment | account_key | Read through the P8 proceeds operation |
| DF-ACE-045 | v_ace_payment | payment_date | Read through the P8 proceeds operation |
| DF-ACE-046 | v_ace_payment | payment_amount | Read through the P8 proceeds operation |
| DF-ACE-028 | v_ace_account | next_installment_date | Read through the P3 case operation |
| DF-TRT-001 | treatment | id | Read through the S2 treatment operation |
| DF-TRT-031 | treatment | installment_amount | Read through the S2 treatment operation |
| DF-TRT-033 | treatment | installment_shortfall | Read through the S2 treatment operation; written by rwb-payment through the same contract, never by the harness |
| DF-FIN-002 | proceeds | case_id | Read through the P8 proceeds operation; written by rwb-payment, never by the harness |
| DF-FIN-003 | proceeds | treatment_id | Read through the P8 proceeds operation |
| DF-FIN-004 | proceeds | payment_code | Read through the P8 proceeds operation |
| DF-FIN-006 | proceeds | amount | Read through the P8 proceeds operation |
| DF-FIN-008 | proceeds | matched_to | Read through the P8 proceeds operation |
| DF-REF-275 | rule_package | package_code | Read through the P7 rule-package operations |
| DF-REF-281 | rule_package_version | version_label | Read through the P7 rule-package operations |
| DF-REF-282 | rule_package_version | status | Read through the P7 rule-package operations |
| DF-REF-286, DF-REF-287 | rule_package_version | valid_from, valid_to | Read through the P7 rule-package operations |
| DF-REF-002 | rule_row | rule_id | Read through the P7 rule-package operations |
| DF-REF-003 | rule_row | rule_version | Read through the P7 rule-package operations |
| DF-REF-296 | rule_row | package_version_id | Read through the P7 rule-package operations |
| DF-REF-297 | rule_row | drools_rule_name | Read through the P7 rule-package operations |
| DF-REF-298 | rule_row | outputs | Read through the P7 rule-package operations |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation |

The harness owns no table (DP-01). It seeds and reads through the published operations only, and its own evidence holds identifiers, statuses, amounts and timestamps of synthetic data, never personal data. The tolerance, window, grace and partial floor are row columns of the PAYMENT_MATCH package; the harness reads no payment_match_rule row, because that table is retired (D-RCV-36 T10). No service schema holds a match rule table: the PAYMENT_MATCH package is the only home of the rows, loaded through the rule-package operations. The target name of the ordering column of those rows is row order; its legacy and TSD name is priority. Field IDs are those of the Logical Data Model, Data Dictionary and Physical Schema v7.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | Reads the matched and unmatched proceeds of the business date with their payment code, amount, treatment and matched-to value (AC1, AC2, AC4, AC5, AC8, AC9) |
| POST | `/api/recovery/payment/v1/proceeds/{proceedsId}/match` | P8 rwb-payment | Drives the manual match path only as a negative control for the access refusal; the automatic journey never calls it (TC-E2-027-11-ITG) |
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | Loads PAYMENT_MATCH version "PM-2026.12" and the invalid version of X3; asserts status 201 and 422 with MSG-P3-027 (AC3, X3) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | Confirms the version in force and its valid-from date before the run (AC3, X7) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the D5 entry, the rule ID and the package version of every match (AC1, AC2, AC3, AC4, AC9) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Reads the installment amount, the due date and the installment shortfall held on the plan (AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case state, the account and the running plan the journey starts from |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout and the breaker of DP-11, and the load POST carries an Idempotency-Key per version label. The rule-package and rule-package-version operations belong to P7 rwb-decision, on the `/admin/rule-packages` and `/admin/rule-package-versions` paths under `/api/recovery/decision/v1`, so the harness loads through the rule-package-version operation of rwb-decision; the exact routed path of the load in SIT: Not specified in the source documents (GAP-0409; ASM-0584). The legacy section 12 attribution to P4 under the monolith base is not used, and `/admin/rule-versions` is a legacy path with no target story (GAP-1293).

The rule-evaluation result that rwb-payment consumes is published in RWB-P8-E2027-CON as `packageCode`, `versionInForce`, `ruleId`, `rowOrder` and `outputs`, with the NoPackageInForce outcome; the harness asserts the rule ID and the package version through the decision log. The operation name of the version-in-force read: Not specified in the source documents (GAP-1359). `treatmentApi.recordInstallmentPaid` in AC2 and AC17 is the legacy in-process name of the installment-paid operation of rwb-treatment, whose target operation name is: Not specified in the source documents (GAP-2507). Both names stay placeholders until their owners publish them.

The match consequence that rwb-treatment reads from rwb-payment is to be published as one read in RWB-P8-E2027-CON that returns, for a case, a plan and a business date, the payment code, the installment due date, the match type, the rule ID, the package code and version and the shortfall, at major version 1. Its operation name, path and payload member names: Not specified in the source documents (GAP-2705). The harness observes the result through the treatment read above.

#### 12.3 Events published

None. The harness publishes no Kafka event of its own; its fixture publishes `AceDataReady` through the rwb-source-data test profile only, and the evidence goes to the release record through the pipeline integration.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | P8 rwb-payment | Asserts the match reached the topic inside the run window, with the case and the business date (AC1, AC2, AC9) |
| `rwb.payment.PaymentMissed.v1` | `rwb.payment.events.v1` | P8 rwb-payment | Asserts the unmatched outcome and the reason path for the late and below-the-floor payments (AC4, AC5, AC8) |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Opens the JOB-07 window and starts the event-started workflow (DP-10) |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Asserts that the seeded version was promoted and is the version the owning service swapped in (AC3) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts the decision record of each match reached the shared topic, alongside the ledger read of 12.2 (DP-03) |

Consumers dedupe through their own inbox table; the harness consumes with its own group and never asserts a producer's outbox row. `DecisionRecorded` is read only, as the ledger acknowledgement of a record written locally; the harness registers no second writer of it (GAP-2506).

The working payload fields of the three rwb-payment events are those of RWB-P8-E2027-CON, identifiers and facts only, to be confirmed with the consumers named in the event catalogue: `TreatmentBooked` carries `treatmentid`, `bookingref` and `businessdate`; `PaymentMissed` carries `treatmentid`, `duedate` and `amountdue`; `ProceedsMatched` carries `caseid`, `proceedsid` and `amount`. The harness consumes `PaymentMissed` and `ProceedsMatched` of these three.

#### 12.5 Workflows and activities

JOB-07 Payment matching is exercised, not built: an event-started workflow on queue `rwb-payment`, started by `AceDataReady` for the business date, with activity `matchPayments` in rwb-payment. The harness records the workflow ID, the business date and the outcome of the run, and asserts the proceeds and decision outcomes afterwards.

JOB-11 Outbox sender is observed: the harness waits for the relay window and reads the events of 12.4 off the topics; it does not assert the relay's own schedule or state.

No workflow is built, no activity is added and no schedule is created by this story. The workflow and its activity belong to RWB-P8-E2027-APP; the load, approve and promote path belongs to RWB-P3-E2042-APP and RWB-P7-E2027-APP.

#### 12.6 Schedules

None. JOB-20 Rule promote (00:01 in rwb-decision) is the mechanism that puts a version in force; the harness waits for its window and asserts the `RulePackageInForce` event, and adds no Schedule of its own.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-payment | `GET /api/recovery/payment/v1/proceeds`, `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match` | OpenAPI of P8 | The matched and unmatched proceeds of the business date, with payment code, amount, matched-to value and treatment; 403 with MSG-P4-002 for the access refusal |
| WireMock rwb-decision | `POST` and `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`, `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | 201 with the loaded version, 422 with MSG-P3-027 for the invalid version, 409 with MSG-GEN-004 for a repeated label, 422 with MSG-GEN-001 for an empty file, and the D5 entries with rule and version; 503 for the decision-store failure |
| WireMock rwb-treatment | `GET /api/recovery/treatment/v1/treatments/{treatmentId}` | OpenAPI of S2 | The installment amount, the due date and the installment shortfall of the plan |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | The case state, the account and the running plan, including the plan route state |
| WireMock rwb-access | `GET /api/recovery/access/v1/me/session` | OpenAPI of P4 | The role, the scope and the Write-off and posting right, including the refusal for RW-CASEOWN (MSG-P4-002) |
| ALS payment fixture | The payment side of the journey | The rwb-source-data payments contract, not in this workspace | One file per business date holding the payment codes, dates and amounts of section 7; replayed through the rwb-source-data test profile so `AceDataReady` opens the window |
| JOB-07 window control | The window and the workflow start | The Temporal namespace `rwb-recovery` and queue `rwb-payment` | Starts or withholds the JOB-07 run for the business date, so a scenario can assert a stopped run as in X7 |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. The fixture file format, the JOB-07 window control and the evidence format: Not specified in the source documents (GAP-0409; ASM-0584).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop on the owner's base with the 2 s timeout of DP-11 |
| Kafka | 5 events consumed across `rwb.payment.events.v1`, `rwb.source-data.events.v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1`; none published by the harness |
| Temporal | Observed only: JOB-07 Payment matching on queue `rwb-payment` and JOB-11 Outbox sender; no workflow, activity or schedule added |
| File | One ALS payment fixture per business date; no other file |

### 13. Solution plan

**Package.** Folder `integration/recovery-payment-matching` in the ACE repository, package `<ACE base package>.recovery.integration.paymentmatching`. Not part of any deployed service, and it owns no schema, table or migration (DP-01, DP-15).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness owns no table and reads no schema; every read is an operation of 12.2 |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The D5 entry is read through rwb-decision and `DecisionRecorded` is read on the shared topic |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON | The package is loaded and read through rwb-decision; the fired row and the version are asserted, never the workbook or the DRL |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | Payments and accounts are asserted only through the P8 and P3 operations; the harness reads no ACE view |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | Any parameter the journey needs is seeded through the P3 contract as data, never as a constant in the harness |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | Match types EXACT, WINDOW and PARTIAL and the plan route states are reference data of the seed pack |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-07 is started by `AceDataReady` and observed on queue `rwb-payment`; the harness adds no Schedule and no workflow |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | Each consumed operation is called once with a 2 s timeout, and the load POST carries an Idempotency-Key |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON | The harness subscribes to the owner's topics only, plus the shared `rwb.decision-record.v1` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The harness owns no table and runs no migration; the seed goes through the operations, not the schemas |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the real screens use, on the same bases |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the five I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date, with the run lock and the build ID |
| FakeRegistry | Configuration | WireMock mappings for the five services, one set per contract version |
| PaymentFixturePack | Data | The ALS payment fixture per business date, with the payment codes, dates and amounts of section 7 |
| PackageFixture | Data | The PAYMENT_MATCH workbook of "PM-2026.12", the "PM-2027.01" variant of AC3 and the invalid "PM-2027.02" variant of X3, with their valid-from dates |
| MatchAssertion | Service | Reads the proceeds through rwb-payment and compares the matched-to value, the amount and the treatment |
| DecisionAssertion | Service | Reads the decision log and the shared topic and compares the decision code, the rule ID and the package version |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the request, the response, the proceeds, the decision entry, the treatment shortfall and the event journal |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached to the release record |

**Environment and test data.** SIT, the wave 2 harness profile, one business date per run, synthetic payments only. The seeded values are the legacy section 7 Background and the payment codes the scenarios name; no other value is added and no real account or customer appears. The environment, the fixture format and the evidence format: Not specified in the source documents (GAP-0409; ASM-0584).

**Build steps**

1. Write the seed pack with case "RC-2026-000555", account "A-0555" and plan "T-0701", and test that a bad seed stops the run (X8).
2. Write PackageFixture and the load step: load "PM-2026.12" through the P7 operation, confirm it is in force, and assert the refusal of "PM-2027.02" with MSG-P3-027 (X3).
3. Write FakeRegistry with the five WireMock mapping sets, including the 403 with MSG-P4-002 for RW-CASEOWN.
4. Write PaymentFixturePack for the business dates of section 7 and the JOB-07 window control, and assert that `AceDataReady` starts the workflow on queue `rwb-payment`.
5. Write JourneyRunner for AC1, AC2 and AC5 and assert the proceeds through P8, the D5 entry through P7 and the shortfall through S2.
6. Add AC4 and AC8 with the unmatched path, the exception list and `PaymentMissed`; add AC9 with the two-row payment and the single decision entry.
7. Add AC3 with the two approved versions, the business date boundary and the version kept on the earlier match.
8. Write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the seven scenarios on the release build.

**Feature switch.** `rwb.payments.matching-rules` is on in the harness profile, as the legacy story sets it; with it off, the journey falls back to the EXACT row only and AC2, AC4, AC5 and AC9 are expected to fail, which the gate reports rather than hides. The load operation is behind `rwb.p3.drools` in the target and is exercised through rwb-decision's operation.

**Operations values and secrets.** The harness fixes no numeric operations value of the matching service. The alert thresholds, the rule-cache staleness window and warm-up timeout, the outbox-lag and dead-letter limits, the worker pool and consumer concurrency sizes, the canary percentage and the probe timings are chart values of the three values files of RWB-P8-E2027-OPS, held as placeholders (Not specified in the source documents (GAP-1361)) and closed with the DL11 decisions before UAT. Every secret and the workload identity are referenced by role, including the rwb-payment login (DP-02); their names are to be recorded in the platform secret-store catalogue (Not specified in the source documents (GAP-2508)).

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all fifteen owned scenarios, every decision entry names a rule ID and the package version in force, and each fake has been replaced by the real service where its I story has landed in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P3-027 | A package version check fails, or no version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-GEN-001 | An empty file is loaded | Enter {field}. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, scenario or package in force, and {table} names the table only, never a payment or a person. Thai text follows DL10, under assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863, which the programme directive confirms; the decision stays open. The harness asserts these messages and never rewrites them; its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-28 Proceeds matching (states Loading; matched; unmatched; no access: a role without the Write-off and posting right is answered with MSG-P4-002; empty and error: Not specified in the source documents (CG-ALL-724)) shows, for each matched receipt, the rule ID and the package version from its decision log entry, and for each unmatched receipt the reason. SCR-39 Rules and parameters (version list states Loading; Results; Empty "No versions of this package."; Error with the problem text, as in RWB-P7-E1073-APP; no access: a role without the Rules and parameters right is answered with MSG-P4-002) shows the PAYMENT_MATCH versions with their status and valid-from date.

No screen is built by this story. The harness drives the operations behind those screens — the proceeds read of rwb-payment, the decision log read of rwb-decision and the version list of rwb-decision — and asserts the matched, unmatched and Loading states through the contracts. The screens themselves belong to RWB-P8-E2027-APP and the Epic 8 story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01-ITG | AC1, BR2, BR6, BR10 | Integration | PAY-91001 12,500.00; PAYMENT_MATCH version PM-2026.12 |
| TC-E2-027-02-ITG | AC2, BR4 | Integration | PAY-91002 11,875.00 |
| TC-E2-027-03-ITG | AC3, BR6 | Integration | PM-2027.01 from 2027-01-01; PAY-91003 4 days late |
| TC-E2-027-04-ITG | AC4, BR3, BR5 | Integration | PAY-91004 3 days late, PAY-91005 4 days late |
| TC-E2-027-05-ITG | AC5, BR4, BR5 | Integration | PAY-91006 10,000.00 |
| TC-E2-027-06-ITG | AC6 (run by app story of RWB-E2-027), BR7 | Integration | PM-2027.02 with duplicate row order and tolerance 120 |
| TC-E2-027-07-ITG | AC7 (run by app story of RWB-E2-027), BR8 | Integration | Decision log stubbed unavailable |
| TC-E2-027-08-ITG | AC8, BR2 | Integration | PAY-91007 13,000.00 |
| TC-E2-027-09-ITG | AC9, BR1 | Integration | PAY-91008 matched by two rows |
| TC-E2-027-10-ITG | AC10 (run by app story of RWB-E2-027), BR9 | Integration | No PAYMENT_MATCH version in force on 2027-02-01 |
| TC-E2-027-11-ITG | Access | Component | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-027-12-ITG | Access | Component | RW-CASEOWN calls POST /admin/rule-packages/PAYMENT_MATCH/versions; refused with MSG-P4-002 |
| TC-E2-027-13-ITG | Principle 5 | NFR | Decision log write forced to fail for 50 payments; no proceeds row written |
| TC-E2-027-14-ITG | AC11, BR7 | Integration | PM-2027.02 with two rows of the same row order and tolerance 120 |
| TC-E2-027-15-ITG | AC12, BR8 | Integration | Decision log stubbed unavailable |
| TC-E2-027-16-ITG | AC13, BR9 | Integration | No PAYMENT_MATCH version in force on 2027-02-01 |
| TC-E2-027-17-ITG | AC14 | Integration | Seed pack not loadable, environment lock held, evidence pack not attachable |
| TC-E2-027-18-ITG | AC15, BR10 | Integration | PM-2026.12 rows read for tolerance, window, grace and partial floor |
| TC-E2-027-19-ITG | AC16 | Integration | Consumed payment event for PAY-91001 delivered again |
| TC-E2-027-20-ITG | AC17 | Integration | treatmentApi.recordInstallmentPaid for PAY-91002 fails or does not answer |
| TC-E2-027-21-ITG | AC18 | Component | Status change not allowed by the status model on PM-2026.12 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app story's case, run across the five contracts, the ALS payment fixture and the JOB-07 window. The app stories keep the unit and component copies of the same cases, and the full test with its Given, When and Then stays under the same test case ID in the test-case workbook.

### 17. Guardrails

- No business value in code: match type, row order, tolerance, window, grace and partial floor are columns of the PAYMENT_MATCH rule rows, and the seed pack holds values, not the harness.
- No personal data in logs, events, workflow inputs, evidence or prompts: the entries hold payment code, amount, dates and rule ID only, and the fixture is synthetic.
- No other service's tables and no schema of the harness's own (DP-01); ACE payment and account data only through the rwb-source-data contract or the owning service's views (DP-05).
- The decision entry is written before the proceeds row; no match exists without its entry, and the harness fails a scenario that shows a proceeds row with no D5 entry.
- One evaluator: the matching engine calls RuleEvaluator, and the harness reads no workbook, DRL source or rule row directly.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration. The harness never runs against UAT or production, and an exception is never added to a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01-ITG, TC-E2-027-02-ITG, TC-E2-027-03-ITG, TC-E2-027-04-ITG, TC-E2-027-05-ITG, TC-E2-027-06-ITG, TC-E2-027-07-ITG, TC-E2-027-08-ITG, TC-E2-027-09-ITG, TC-E2-027-10-ITG, TC-E2-027-11-ITG, TC-E2-027-12-ITG, TC-E2-027-13-ITG, TC-E2-027-14-ITG, TC-E2-027-15-ITG, TC-E2-027-16-ITG, TC-E2-027-17-ITG, TC-E2-027-18-ITG, TC-E2-027-19-ITG, TC-E2-027-20-ITG, TC-E2-027-21-ITG |

### 19. Out of scope

- Settlement matching and partial settlement installments (FEAT-PAY-03, Epic 4).
- Manual matching from SCR-28, the P8 match operation (Epic 4), exercised here only as a negative access control.
- Direct interfaces to ALS, GL, ATS, AMIS or the LED portal, including the auto-debit and LED routes: outside the 19 services until an interface is named (GAP-1631). The ALS position is read through the rwb-source-data contract after the next completed ACE batch, ledger postings go out through rwb-integration, and the officer books into ALS.
- The reconciliation agent that works the exception list (Epic 4).
- Applying proceeds to the case balance in policy order (FEAT-PAY-10, Epic 4).
- Authoring the PAYMENT_MATCH rows, their scenarios and their approval (RWB-E2-042, RWB-E1-073).
- The retired payment_match_rule table and its reference loads (D-RCV-36 T10).
- Production code of any service: the endpoint, the screen, the table and the migration of rwb-payment, rwb-decision, rwb-case, rwb-access and rwb-treatment.

The harness covers the items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
