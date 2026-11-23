# RWB-P8-E2027-APP Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E2027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P8-C |
| Ready to start | After RWB-P8-E2008-APP |
| Depends on (build) | RWB-P8-E2027-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P8-E2008-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2042-CON |
| Integration dependencies | None |
| External dependencies | RWB-P8-E2027-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032) |
| Status | Draft (realignment v1) |

### 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the matching rules for amount, date window and partial payments held as rows of the PAYMENT_MATCH rule package, the package read from rwb-decision's registry and evaluated in this service by the embedded Drools kit in row order, each match recorded as a local decision record that names the rule ID and the package version in force and then written to `proceeds` in `rwb_payment`, with the exception list for what does not match**, so that **most payments match without a person, the rest are listed, and every match can be explained by the row and the approved version that decided it**.

This story is the rwb-payment half of the legacy key RWB-E2-027. It runs inside:

- service `rwb-payment`, schema `rwb_payment`, REST base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the event names `rwb.payment.<Event>.v1`, Temporal task queue `rwb-payment` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.payment` (DP-01, DP-13, DP-14);
- the tables this service owns: `proceeds` only, plus the library objects `decision_record`, `outbox_event`, `processed_event` and `idempotency_key` created in `rwb_payment` by its own Flyway sequence (DP-03, DP-15);
- the rule registry of `rwb-decision` (`rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`) as a **read-only source**: this service holds only a local evaluated copy of the model, verifies its checksum and swaps it in on `RulePackageInForce` (DP-04; ASM-4148).

What stays outside this story:

- the registry and the governance of a package version — the load, its checks, the four-eyes approval, the 00:01 promotion, the one-call rollback and the version states — with `rwb-decision` (P7, RWB-P7-E2027-APP);
- the PAYMENT_MATCH workbook, its Rows and Tests tabs and the authoring pipeline, with `rwb-case` (P3, RWB-P3-E2042-APP and RWB-P3-E1073-APP);
- the session, the role and the right behind every operation, with `rwb-access` (P4);
- the installment shortfall that a PARTIAL match passes to the plan, with `rwb-treatment` (S2);
- the manual match `POST /proceeds/{proceedsId}/match` and the settlement, auction and enforcement proceeds, which are the Epic 4 stories of this service (RWB-P8-E4043-APP, RWB-P8-E4044-APP).

The legacy rule behaviour is carried unchanged: the same package code PAYMENT_MATCH, the same three rows and their row order, the same condition and output columns, the same first-match-wins rule, the same dated version in force, the same refusal of an invalid version load in full, the same "no version in force is a refusal and never a default match", and the same rule that a match whose decision record cannot be written is not made.

### 2. Business rationale

The exact rule of RWB-E2-008 leaves short and late installments on the exception list, and a person matches them by hand each morning. RWB-E2-027 adds the PARTIAL and WINDOW rows of the PAYMENT_MATCH package, applies the rows in row order, records each match with the rule ID and the package version, and lets Credit Administration change a window or a tolerance through a new approved version with no code release. The match type, the amount tolerance, the window, the grace and the partial floor are columns of the decision table, not code and not a reference table (D-RCV-36 T10): this story reads them from the evaluated model and carries no threshold of its own.

The realignment changes the mechanism, not the business rule:

1. The matching code of the monolith becomes the `matchPayments` activity of an event-started workflow on task queue `rwb-payment` (DP-10): JOB-07 starts from `AceDataReady` (EV-26) instead of a Quartz trigger on a shared table (Arch v5 slide 44).
2. `RuleEvaluator` of the monolith becomes the embedded Drools kit (DP-04): one `KieBase` per package version, held in an LRU cache of at most 20, never recompiled per call; the package arrives from rwb-decision's registry and its checksum is verified before the swap.
3. The decision log write becomes the local decision-record library on the shared topic `rwb.decision-record.v1` (DP-03): the record is written in the same transaction as the `proceeds` row, chained to the record before it, and rwb-decision collects it into the central ledger.
4. `recovery.proceeds` becomes `proceeds` in `rwb_payment` (DP-01), and the ACE payment and account facts arrive through `v_ace_payment` and `v_ace_account` under the P1 contract and this service's own views (DP-05), never by a join to another module's tables.
5. `/api/recovery/v1` becomes `/api/recovery/payment/v1` (DP-13), and the payment events are published on `rwb.payment.events.v1` under the naming library (DP-14) with the outbox relay and the CloudEvents 1.0 envelope of the platform library.
6. The parameters and the reference lists that select a match type, a version label or a date boundary are read through the rwb-case contracts (DP-06, DP-07), and the screen that lists the matches and the exceptions is composed by the gateway-bff route behind SCR-28 (DP-19).
7. Every cross-module call is one hop against a published contract with a 2 s budget and a breaker (DP-11).

This story serves REQ-CHO-009 and the rule-version half of R-UNI-38 and R-UNI-41: an earlier decision keeps the version it was taken under, and no version in force is a refusal.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P8-E2027-CON | The published contract of this service for this key: the `Proceeds` element, the two operations, the three event envelopes and the rule-evaluation result this service consumes from rwb-decision. Faked until it is published (DP-11) |
| RWB-P8-E2008-APP | JOB-07, the `proceeds` table, the exception list and the exact-match run of RWB-E2-008 are live; this story replaces the single exact row with the evaluated package |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): the compile of a workbook to a `KieBase`, the checksum, first-match semantics with the default row last, and the `NoPackageInForce` outcome |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one record in the caller's transaction, hash-chained |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | The parameters and reference-data client libraries (DP-06, DP-07) |
| RWB-PLT-E1071-CON | The Temporal workflow kit in namespace `rwb-recovery` (DP-10): the event-started workflow, its retry policy and its activity registration |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic, the retry topic, the `.dlt` topic and the event names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): SCR-28 is composed there; this story serves its data and builds no screen |
| RWB-P3-E2042-CON | The rwb-case authoring contract: the workbook and its Tests tab whose rows this service consumes as an evaluated model (C) |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | The rwb-case parameters and reference-data contracts (C): LOV-MATCH, LOV-MATCH-TYPE and the version label in force |

Business preconditions carried from RWB-E2-027:

- RWB-E2-008 is done: JOB-07, the `proceeds` table and the exception list are live, and a PAYMENT_MATCH version with the EXACT row in force decides the exact matches.
- The PAYMENT_MATCH package holds the EXACT, WINDOW and PARTIAL rows in the Drools template with at least 50 scenarios, authored and approved (RWB-E2-042, RWB-E1-073; in the target RWB-P3-E2042-APP and RWB-P7-E2027-APP).
- The decision-record library accepts a D5 entry with a rule ID and a rule version.
- PAYMENT_MATCH version "PM-2026.12" is in force from 2026-12-01 with the EXACT, WINDOW and PARTIAL rows of section 7. It was loaded and approved in the registry (RWB-P7-E2027-APP). The label is read as the one version in force for that date; the "PMT-2026.12" label carried by RWB-P3-E2042-APP is the same package and must be reconciled to one version row before SIT (GAP-2506; ASM-4150).
- The reader holds RW-CREDITAD or another role with Write-off and posting R.
- TreatmentApi records an installment shortfall (RWB-E2-004; in the target the rwb-treatment contract).
- Synthetic data only: payment codes, account keys, case references, plan references, amounts, dates, version labels and rule IDs of the legacy story; no real customer, account or payment.

### 4. Flow

1. `rwb-source-data` publishes `AceDataReady` (EV-26) for the business date; the workflow kit starts the JOB-07 workflow on task queue `rwb-payment`, which runs the `matchPayments` activity (Arch v5 slide 44; DP-10).
2. `PaymentMatchFactsBuilder` reads the payments of the business date through the P1 contract and this service's `v_ace_payment` view, the accounts and the next installment date through `v_ace_account`, and the running plans and their installments through the rwb-treatment contract; it builds one fact set per running plan of the case.
3. `RuleVersionResolver` asks rwb-decision's registry for the PAYMENT_MATCH version in force on the business date, fetches the model of that version, and verifies its checksum against the registry answer before it is used. The resolved version label is held for the whole run, so every match of the run names the same version (DP-04; ASM-4148).
4. The embedded Drools kit evaluates the facts against the evaluated copy of the package. The model fires one row — the first match in row order (EXACT, then WINDOW, then PARTIAL) — and the result names the rule ID, the row order, the package code and the package version (BR1).
5. `MatchDecisionWriter` builds the D5 decision record with the case, the plan, the payment code, the amount, the due date, the rule ID and the package version, and writes it through the local decision-record library in the same transaction as the `proceeds` row (DP-03; BR6, BR8).
6. In that same transaction the service writes the `proceeds` row: case, treatment, payment code, source, amount, received date and `matched_to` (DP-01).
7. For a PARTIAL match, `MatchOutcomeReader` calls the rwb-treatment contract to record the installment paid and the shortfall on the plan.
8. The service writes `ProceedsMatched` (EV-25) to its outbox in the same transaction; for a payment no row matches it writes the `proceeds` row with `matched_to` UNMATCHED, its D5 record under R-UNI-03 and the exception-list entry, and for a plan with no payment in the window it writes `PaymentMissed` (EV-12). The outbox relay publishes to `rwb.payment.events.v1` with the CloudEvents 1.0 envelope.
9. Credit Administration reads matched and unmatched receipts on SCR-28 through the gateway-bff route, each matched receipt with its rule ID and package version from the local decision record.
10. The `confirmBookings` and `postProceeds` activities of the service are the booking and posting steps of this service and are not extended by this story.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | Unmatched; exception list | MSG-P8-001 | AC5 (owned by RWB-P8-E2008-APP for the exact rule, by this story for the evaluated row) |
| X2 | A late payment one day past the window | Unmatched; exception list | MSG-P8-001 | AC4 (not owned by this split; the row is evaluated here) |
| X3 | A package version load with two rows of the same row order or a tolerance above 100 | The load is refused in full by the registry; "PM-2026.12" stays in force | MSG-P3-027 | AC6 |
| X4 | The decision record cannot be written for a match | No `proceeds` row is written; the payment is picked up by the next run; incident | MSG-P7-003 | AC7 |
| X5 | A payment above the installment by more than the tolerance | Unmatched; exception list | MSG-P8-001 | AC8 (not owned by this split) |
| X6 | Two rows would match | The row with the lower row order decides; one record only | None | AC9 (not owned by this split) |
| X7 | No PAYMENT_MATCH version is in force on the business date | The run stops; no payment is matched and no `proceeds` row is written; no default version is substituted | MSG-P3-027 | AC10 |
| X8 | The fetched model fails its checksum | The local cache keeps the last good model of the version in force; the mismatch is counted and alerted; no match is taken on the unverified model | None | AC10, TC-E2-027-13 |
| X9 | The `AceDataReady` event of the business date is repeated | The inbox dedupes on the event ID; the run writes no second `proceeds` row and no second event | None | TC-E2-027-01 |
| X10 | The rwb-treatment contract does not answer within 2 s | The activity retries on the kit policy; after the last attempt the payment stays unmatched with its reason and the run summary names it | MSG-P8-001 | TC-E2-027-02 |

A stale `proceeds` row at commit is a conflict and the transaction rolls back, so a payment cannot be matched twice by two runs of the same business date.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P8-E2027-CON, RWB-P8-E2008-APP and the platform contracts of its DP table; reads no registry table and writes no other schema |
| Negotiable | The thresholds, the row order, the match types, the version labels, the message texts and the alert thresholds are rule rows, parameters, reference rows or chart values; the story fixes only the evaluation, the record and the write order |
| Valuable | Short and late installments match without a person, and every match names the rule and the approved version that decided it |
| Estimable | One facts builder, one version resolver, one evaluator call, one match writer, one outcome mapper, one event writer and one migration |
| Small | Fits two weeks with its tests |
| Testable | Each criterion is a run of JOB-07 on a fixed business date with a fixed package version and a fixed payment set |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given PAYMENT_MATCH package version "PM-2026.12" is in force from 2026-12-01 with rows:
      | rule_id | row_order | match_type | amount_tolerance_pct | window_days_before | window_days_after | partial_floor_pct |
      | EXACT   | 1         | EXACT      | 0                    | 10                 | 0                 |                   |
      | WINDOW  | 2         | WINDOW     | 0                    | 10                 | 3                 |                   |
      | PARTIAL | 3         | PARTIAL    | 0                    | 10                 | 3                 | 90                |
    Given case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15

  Scenario: AC6 Invalid package version refused (legacy RWB-E2-027 AC6)
    Given the rwb-decision contract mock returns the refused schema check naming "PARTIAL" and the tolerance column
    Given a PAYMENT_MATCH workbook for version "PM-2027.02" where rows "WINDOW" and "PARTIAL" both have row order 2 and "PARTIAL" has tolerance 120
    When it is loaded through POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the response is status 422 with MSG-P3-027 for the schema check naming "PARTIAL" and the tolerance column
    Then the system refuses the load in full and "PM-2026.12" stays in force

  Scenario: AC7 Decision log write fails (legacy RWB-E2-027 AC7)
    Given the decision log store is unavailable during JOB-07 on 2026-12-15
    When "PAY-91001" is matched
    Then the system writes no proceeds row for "PAY-91001"
    Then the run summary shows MSG-P7-003 for "PAY-91001"
    Then the system raises an incident under rule R-UNI-39
    Then the next run of JOB-07 for 2026-12-14 matches "PAY-91001"

  Scenario: AC10 No PAYMENT_MATCH version in force (legacy RWB-E2-027 AC10)
    Given the rwb-decision contract mock returns NoPackageInForce for business date 2027-02-01
    Given no PAYMENT_MATCH package version is in force on 2027-02-01
    When JOB-07 runs for business date 2027-02-01
    Then RuleEvaluator.evaluate("PAYMENT_MATCH", facts, 2027-02-01) throws NoPackageInForce
    Then the run stops with MSG-P3-027 for the package in force check
    Then no payment is matched and no proceeds row is written for 2027-02-01
```

The three criteria are the legacy criteria of RWB-E2-027 AC6, AC7 and AC10 copied word for word, with one leading `Given` added to AC6 and to AC10 because the cross-service part they exercise is mocked here: the load and its checks belong to rwb-decision (P7) and the version-in-force lookup belongs to the registry contract of RWB-P8-E2027-CON. The load path in AC6 is written on the target base of its owner, `/api/recovery/decision/v1`, because DP-13 gives every service its own base and the load and its checks are rwb-decision's operation; every other word and every value of the three criteria is the legacy one, and this story builds neither the load nor its checks (GAP-2506; ASM-4148). The other seven legacy criteria of RWB-E2-027 stay with the slices that own them: AC1, AC2, AC4, AC5, AC8 and AC9 with RWB-P8-E2008-APP, AC3 with RWB-P7-E2027-APP, and the cross-service journey with the wave 2 harness.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Rows are tried in row order and the first row that matches decides (first match); the default row is always last | D-RCV-36 T5; ADR-012; legacy BR1 |
| BR2 | EXACT: plan account, amount within the tolerance, date inside the window before the due date | R-RES-26; legacy BR2 |
| BR3 | WINDOW: as EXACT with the window extended after the due date; a late match is a late payment for the plan | R-RES-28; legacy BR3 |
| BR4 | PARTIAL: amount at or above the partial floor and below the installment; the shortfall is held on the plan | R-SET-15 pattern; REQ-CHO-009; legacy BR4 |
| BR5 | A payment no row matches is held on the exception list | R-UNI-03; CTL-41; legacy BR5 |
| BR6 | Each match decision is written to the local decision record with the rule ID (EXACT, WINDOW or PARTIAL) and the package version in force on the business date; earlier matches keep their version | R-UNI-38; D-RCV-36 T5, T7; legacy BR6 |
| BR7 | A package version with any invalid row is refused in full by the registry and never reaches this service | Reference data change process step 3; CTL-08; legacy BR7 |
| BR8 | A match whose decision record cannot be written is not made: the record and the `proceeds` row commit together or not at all | Principle 5; R-UNI-39; legacy BR8; DP-03 |
| BR9 | No version in force is a refusal (`NoPackageInForce`), never a default match | D-RCV-36 T3; R-UNI-41; legacy BR9 |
| BR10 | The tolerance, window, grace and partial floor are condition and output columns of the PAYMENT_MATCH rows, not code and not a reference table | D-RCV-36 T10; REQ-CHO-009; legacy BR10 |
| BR11 | The match type, the row order and the thresholds are read from the evaluated model only; this service reads no workbook, no `drl_source` and no `rule_row` | DP-04; Temporal and Drools slide 15 |
| BR12 | The package version is resolved once per run from the business date and is named on every record of that run; the model is verified by its checksum before it is used and the last good model is kept on a failure | DP-04; Temporal and Drools slide 15 notes; AC10 |
| BR13 | `proceeds` lives in `rwb_payment` and no other service reads or writes it; the ACE facts arrive through `v_ace_*` views and the P1 contract only | DP-01, DP-05; Ownership Map row `proceeds` (owner P8); Architecture v5 slide 17 |
| BR14 | The registers of a match — the case ID, the payment code, the amount, the due date, the rule ID and the rule version — carry no personal data | Architecture v5 slide 42 notes; Template and Rules §R7.2 s17 |

### 9. State transitions

This story changes no case status. It owns the state of a `proceeds` row.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | `matchPayments` runs | The decision record commits with the row | MATCHED (INSTALLMENT) |
| (none) | `matchPayments` runs | No row matches | UNMATCHED, with its reason and its record |
| (none) | `matchPayments` runs | The decision record cannot be written | No row is written; the payment is retried by the next run |
| (none) | `matchPayments` runs | No version is in force for the business date | No row is written for any payment of that date; the run stops |

The plan route states the results feed stay with rwb-case (P3):

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | PLAN_RUNNING (R-RES-26) |
| PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | PLAN_RUNNING (R-RES-28) |

The package version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are rwb-decision's and are read here only through the registry answer.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads matches and the exception list (Write-off and posting CRUA); owns the matching values through the package rows |
| RW-COE, center of excellence analyst | Authors the PARTIAL and WINDOW rows and loads the version (Rules and parameters C); loads nothing through this service |
| RW-RISK, risk and model risk officer | Approves the package version (Rules and parameters A); calls the rollback in rwb-decision |
| RW-FINANCE, Finance and CFO delegate | Reads matches (Write-off and posting RA) |
| The rwb-payment service identity | Runs the JOB-07 workflow and its activities, writes the records and the rows, publishes the events |
| SY-RULES, Drools evaluator | Evaluates the evaluated copy of the package inside the activity and names the rule and the version |
| SY-DECLOG, decision record writer | Supplies the hash-chained local record of DP-03 |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent (Epic 4) |
| RW-CASEOWN and any role without the Write-off and posting right | Refused with MSG-P4-002 on the read operation of section 12.1 |

Separation of duty stays in rwb-decision: the analyst who loads a version does not approve it and RW-RISK approves. No person is named anywhere; the actors are roles and service identities.

### 11. Data

| BR Field ID | Entity | Field | Read or write | Owner |
|---|---|---|---|---|
| DF-FIN-001 to DF-FIN-009 | proceeds | id, case_id, treatment_id, account_payment_id, source, amount, received_date, matched_to, posting_ref | Write and read | P8 (`rwb_payment`) |
| DF-DEC-001 to DF-DEC-031 | decision_record | id, decision_code, rule_id, rule_version, inputs_ref, recommendation, final_call, outcome, decided_at, chain_seq, prev_hash, entry_hash, actor_user_id, idempotency_key | Write one record per match (DP-03) | PLT library, created in `rwb_payment` |
| DF-ACE-043, DF-ACE-044, DF-ACE-045, DF-ACE-046 | v_ace_payment | payment_code, account_key, payment_date, payment_amount | Read | P1 contract; view in this service |
| DF-ACE-028 | v_ace_account | next_installment_date | Read | P1 contract; view in this service |
| DF-TRT-001, DF-TRT-031, DF-TRT-033 | treatment | id, installment_amount, installment_shortfall | Read; the shortfall written through the rwb-treatment contract | S2 |
| DF-REF-274 to DF-REF-278 | rule_package | id, package_code, title, owner_role, hit_policy | Not read as a table: the package code arrives on the registry answer | P7 |
| DF-REF-279 to DF-REF-294 | rule_package_version | id, version label, status, checksum, valid_from, valid_to | Not read as a table: the version in force and its checksum arrive on the registry operation | P7 |
| DF-REF-002, DF-REF-003, DF-REF-296 to DF-REF-298 | rule_row | rule_id, rule_version, package_version_id, drools_rule_name, outputs | Not read: the rows are evaluated from the model, never queried | P7 |

`payment_match_rule` (DF-REF-261 to DF-REF-273) is retired and is neither created nor read (D-RCV-36 T10). The name the sources give the ordering column is not stable: RWB-E2-027 and the FSD exceptions call it row order while TSD P8 T3.1 carries `priority` (DF-REF-270); the target reads it as the row-order column of the rule row and keeps the legacy word in the scenarios (GAP-2506; ASM-4149). No new table and no new column is added to `proceeds` by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-payment` (P8); base `/api/recovery/payment/v1` (DP-13).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | List receipts with their match status, the rule that matched and the package version, for the matched and unmatched lists of SCR-28; 200 with `ProceedsPage` (API-P8-001, TSD P8 v2 T-A.2) | Write-off and posting R, scope applied | Not applicable, read only |
| POST | `/proceeds/{proceedsId}/match` | Match a receipt to a case and an account by hand; 200 with `Proceeds` (API-P8-002). Declared here as the operation of this service; its behaviour is the Epic 4 story RWB-P8-E4043-APP | Write-off and posting U, scope applied | `Idempotency-Key` header required |

The two paths are the ownership map's P8 paths; the query of `GET /proceeds` is `matched`, `from`, `to`, `page` and `size`, and the errors are 401, 403, 404, 409, 422 and 503 with one RFC 9457 problem response and one message ID each. The request and answer shapes are fixed by RWB-P8-E2027-CON and are consumed here, not redefined.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions` | P7 rwb-decision | The version in force on the business date and its checksum; one hop, 2 s, faked (DP-11) |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The model of the version in force, fetched once per version and verified by its checksum (DP-04; Temporal and Drools slide 15 notes) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameters of the matching run, through the client library (DP-06); faked |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-MATCH, LOV-MATCH-TYPE and the version label list (DP-07); faked |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's role, scope and Write-off and posting right behind `GET /proceeds`; faked |
| POST | The installment-paid operation of rwb-treatment (operation name Not specified in the source documents (GAP-2506; ASM-4148)) | S2 rwb-treatment | Records the installment paid and the shortfall of a PARTIAL match; faked |

Every row is one hop with a 2 s budget and a breaker. The rwb-decision rows are the C row of DP-04 (`RWB-P7-E1073-CON`) and of the registry story (`RWB-P7-E2027-APP`); neither is in this story's contract-dependency row, which carries the three rwb-case contracts (GAP-2506; ASM-4148).

#### 12.3 Events published

| Event | Topic | Key | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | caseId | case ID, proceeds ID, payment code, treatment ID, source, amount, matched-to, rule ID, rule version, received date |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | caseId | case ID, treatment ID, due date, amount due, business date |
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | caseId | case ID, treatment ID, booking reference, amount, booking date |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | caseId | the local decision record: entry ID, decision code D5, rule ID, rule version, inputs reference, final call, decided at |

Every event is written to the service's outbox in the same transaction as the state change and relayed with the CloudEvents 1.0 envelope, keyed by `caseId`, by the platform outbox relay (RWB-PLT-TE006-CON; DP-09 is the platform pattern and is not a pattern of this key's table). The topic name and the event names follow the naming library (DP-14); the `.retry` and `.dlt` topics are provisioned by RWB-P8-E2027-OPS. No event carries a name, an e-mail address, a mobile number, a national identity number or an account number.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in this story |
|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts the JOB-07 workflow and fixes the business date (DP-10); deduped by the inbox |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | Refreshes the running plans and their installments the matching facts use |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Refreshes the evaluated copy of PAYMENT_MATCH: fetch, verify the checksum, swap atomically |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | all 19 services | The ledger acknowledgement of a local record; this service registers no second writer for it (GAP-2506; ASM-4151) |
| `rwb.debtsale.LotAwarded.v1` (EV-23) | `rwb.debtsale.events.v1` | S6 rwb-debtsale | Names the lot a debt-sale receipt belongs to; consumed by the Epic 4 proceeds stories and declared here for the interface of the service |
| `rwb.asset.AssetSold.v1` | `rwb.asset.events.v1` | S5 rwb-asset | Names the asset sale a receipt belongs to; consumed by the Epic 4 proceeds stories and declared here for the interface of the service |

The inbox of the service dedupes every event on its ID, so a repeated `AceDataReady` starts no second run and a repeated `RulePackageInForce` performs no second swap.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Use in this story |
|---|---|---|---|
| JOB-07 payment matching | Event-started workflow, started by `AceDataReady` | `rwb-payment` in namespace `rwb-recovery` | One run per business date; the workflow that hosts the matching (DP-10; Arch v5 slide 44) |
| `matchPayments` | Activity | `rwb-payment` | Builds the facts, resolves the version, evaluates, writes the record and the row, writes the outbox events |
| `confirmBookings` | Activity | `rwb-payment` | JOB-08 booking confirmation; declared, not extended here |
| `postProceeds` | Activity | `rwb-payment` | The saga step of the settlement and sale flows; declared, not extended here |

The workflow is deterministic: the Drools evaluation runs only inside the activity, so a replay reuses the recorded result and never recompiles a model. The retry policy is the kit's (1 s initial interval, back-off 2, 10 attempts) and `NoPackageInForce` is non-retryable.

#### 12.6 Schedules

None. JOB-07 and JOB-08 are event-started workflows triggered by `AceDataReady`, not Schedules (Arch v5 slide 44). The only Schedule of this key is the 00:01 rule promote of rwb-decision (JOB-20) and it is not registered, retimed or duplicated here.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | One row per receipt and its match |
| `decision_record` | PLT library, created in `rwb_payment` | The local hash-chained decision record of each match (DP-03) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_payment` | Outbox, inbox and idempotency objects of the service |

Not owned and not read as tables: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` (P7, reached only through the registry operations of 12.2), `treatment` (S2), `recovery_case` (P3) and `decision_log_entry` (P7). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision registry fake | RWB-P8-E2027-CON and RWB-P7-E2027-APP | The version in force "PM-2026.12" with its checksum, the model of that version, the refused schema check of AC6, and `NoPackageInForce` for 2027-02-01 |
| rwb-case parameters and reference-data fake | RWB-P3-E1042-CON, RWB-P3-E1043-CON | The matching parameters, LOV-MATCH, LOV-MATCH-TYPE and the version label list |
| rwb-treatment fake | RWB-P8-E2027-CON | The installment-paid answer with the shortfall, a timeout and a refusal |
| rwb-access fake | RWB-P4-E1037-CON | A session with Write-off and posting R and one without it |
| Drools kit fake | RWB-PLT-E1072-CON | First-match semantics with the default row last, a checksum mismatch and a cold cache |
| decision-record library fake | RWB-PLT-E1027-CON | A healthy append with its chain link, and a forced failure for AC7 and TC-E2-027-13 |

Each fake is replaced by the real contract as its story lands, without a change to the scenarios. The fakes carry synthetic payment codes, account keys, case and plan references only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 6 | `GET /proceeds` and the declared manual match on `/api/recovery/payment/v1`; the registry version list and model fetch, the parameters, the reference list, the session and the treatment installment-paid call, one hop and 2 s each |
| Kafka | Published 3 event types plus the shared record, consumed 6 | `rwb.payment.events.v1` with `ProceedsMatched`, `PaymentMissed` and `TreatmentBooked`; `rwb.decision-record.v1` with `DecisionRecorded`; `AceDataReady`, `TreatmentApproved`, `RulePackageInForce`, `DecisionRecorded`, `LotAwarded` and `AssetSold` consumed |
| Temporal | 1 event-started workflow, 4 activities, 0 Schedules | The JOB-07 workflow and `matchPayments`, with `confirmBookings` and `postProceeds` declared, on `rwb-payment` |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `matching`, Java package `th.co.scb.ace.workbench.recovery.payment.matching`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How this story applies each row. **DP-01**: `proceeds` and the four library objects sit in `rwb_payment`; the matching facts of the plan arrive on the rwb-treatment contract and the ACE facts through this service's views, never by a join to another schema. **DP-03**: each match writes one local record in the transaction that writes the row, chained to the record before it, and publishes `DecisionRecorded` on the shared topic; a record that cannot be written stops the match (BR8). **DP-04**: the model is fetched from rwb-decision, verified by its checksum and evaluated by the embedded kit, held per version in an LRU cache of at most 20; the story reads no `rule_row` and no workbook, and the C row `RWB-P7-E1073-CON` is built against its published set and its fake. **DP-05**: `v_ace_payment` and `v_ace_account` are the SELECT-only views of this service and the payment set of the business date is read through the P1 contract. **DP-06**: the matching parameters — the run window, the batch readiness and the feature switch values — are read as parameters, never as constants. **DP-07**: LOV-MATCH, LOV-MATCH-TYPE and the version label list are reference rows with their version; the thresholds stay rule-row columns and are never reference data (BR10). **DP-10**: JOB-07 is the event-started workflow of task queue `rwb-payment` started by `AceDataReady`, and no Schedule and no shared Quartz table is registered. **DP-11**: the six consumed operations of 12.2 are one hop on the owner's base with a 2 s timeout and a breaker; the legacy in-process `TreatmentApi` and `RuleEvaluator` calls become the treatment contract and the embedded kit. **DP-13**: every path of section 12 uses `/api/recovery/payment/v1`; no monolith base appears in the code or the tests. **DP-14**: the topic is `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the events are `rwb.payment.<Event>.v1`, taken from the naming library and never hand-written. **DP-15**: one Flyway sequence in `rwb_payment` adds the evaluated-model cache metadata and the indexes of the matching read, and no other schema is touched. **DP-19**: SCR-28 is composed by the gateway-bff route and this story serves its data; no screen template and no `ace-web` page is built here.

The platform H dependencies of the table — `RWB-PLT-E1027-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1044-CON` and `RWB-PLT-N001-CON` — are the DP-added dependencies and are all listed in the metadata row. The C dependencies of DP-04 (`RWB-P7-E1073-CON`) and of the registry story are **not** in the metadata C row, which carries the three rwb-case contracts; the absence is recorded in GAP-2506 and ASM-4148, and none of them blocks the build because an APP story builds against the published set and its fake (Template and Rules §R5.4).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ProceedsController | Controller | `GET /proceeds` with the session read, the scope and the problem mapping; the manual match path is declared and served by the Epic 4 story |
| PaymentMatchFactsBuilder | Service | Builds the facts of the payment, the account, the installment and the business date |
| RuleVersionResolver | Service | Resolves the PAYMENT_MATCH version in force, fetches the model, verifies the checksum, keeps the last good model |
| PaymentMatcher | Service | Calls the embedded kit for PAYMENT_MATCH, applies the fired row, returns the rule ID, the row order and the version |
| MatchDecisionWriter | Service | Builds the D5 record with the rule ID, the package version and the inputs, and writes it through the library before the row |
| MatchOutcomeReader | Service | Maps the result outputs to the `proceeds` row and to the shortfall passed to rwb-treatment |
| ProceedsRepository | Repository | `proceeds` in `rwb_payment`, with the optimistic lock and the unique key on payment code and business date |
| PaymentEventWriter | Service | Writes `ProceedsMatched`, `PaymentMissed` and `TreatmentBooked` to the outbox in the same transaction |
| MatchPaymentsActivity | Activity | The JOB-07 step that orders the components and the transaction |
| ModelRefreshHandler | Consumer and workflow | Consumes `RulePackageInForce`, fetches, verifies and swaps the evaluated copy atomically |
| ParameterClient, ReferenceDataClient, SessionClient, TreatmentClient | Clients | The six consumed operations of 12.2, one hop with a 2 s timeout and a breaker |

**Database and migrations**

- Writes `proceeds`, `decision_record`, `outbox_event`, `processed_event` and `idempotency_key`, all in schema `rwb_payment`; reads no other schema.
- One migration in the per-service Flyway sequence of DP-15, `V2027_2__payment_matching_rules.sql`: the unique key of a payment code within a business date on `proceeds`, the index of the matched and unmatched read, and the model-cache metadata table of the evaluated copy. It creates no table of rwb-decision and no `payment_match_rule`.
- Updates a `proceeds` row with `WHERE id = ? AND version = ?`; zero rows updated is a conflict and the run retries, never writes twice.
- The tables of RWB-P8-E2008-APP are reused and not rebuilt; this story adds no column to `proceeds` beyond the ones section 11 lists.

**Configuration and reference data**

- The PAYMENT_MATCH version labels, the valid-from dates and the rows are the legacy values: "PM-2026.12" from 2026-12-01 with EXACT 1, WINDOW 2 and PARTIAL 3; "PM-2027.01" from 2027-01-01 with WINDOW at 5 days after; "PM-2027.02" refused in full. The rows are registry data of rwb-decision and are never seeded here (GAP-2506; ASM-4150).
- The model cache bound of 20, the warm-up list of PAYMENT_MATCH and the warm-up timeout are values of the chart of RWB-P8-E2027-OPS, not constants of the code.
- The version label in force, the match types and the source and match-to lists are read through DP-07 with the version in force; no list value is a constant of the code.
- The feature switch `rwb.p8.matching-rules` is read as a parameter through DP-06. Off: JOB-07 matches on the EXACT row only, as in RWB-P8-E2008-APP, and no new version is swapped in.

**Build steps**

1. `PaymentMatchFactsBuilder` and `ProceedsRepository`, with the unique key of the migration; unit-test the facts of the legacy payments and the duplicate-run case (X9).
2. `RuleVersionResolver` with the version lookup, the checksum verification and the last-good-model rule; test the cold cache and the checksum mismatch (X8, AC10).
3. `PaymentMatcher` on the embedded kit with first-match semantics; test the fired row and the row order.
4. `MatchDecisionWriter` with the write-before-row order and the fail-closed behaviour; test AC7 and TC-E2-027-13.
5. `MatchOutcomeReader` and the treatment call, with the timeout and the retry path (X10).
6. `MatchPaymentsActivity` and the JOB-07 workflow registration on `rwb-payment`, started by `AceDataReady`; test the repeated event and the missing event.
7. `ModelRefreshHandler` for `RulePackageInForce`, with the atomic swap and the checksum check.
8. The privacy test: no record, event or log line carries a name, an e-mail address, a mobile number or an account number.

**Done when.** The tests in section 16 pass; a synthetic month of 1,000 payments runs with every record naming a rule ID and a package version; "PM-2027.02" is refused in full with MSG-P3-027; no version in force on 2027-02-01 stops the run with MSG-P3-027 and writes no row; and a forced record failure writes no `proceeds` row.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P8-001 | The run summary holds unmatched payments | {count} payments for {date} matched no plan and are on the exception list. | This story, on the run summary and the exception read |
| MSG-P3-027 | A package version check fails, or no version is in force | The rule version was refused at the {check} check: {detail}. | This story on the version-in-force check; rwb-decision on the load |
| MSG-GEN-001 | An empty file is loaded | Enter {field}. | rwb-decision, named only |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. | rwb-decision, named only |
| MSG-P7-003 | The decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, through the record library |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. | This story, through the session read |

For MSG-P3-027 the {check} value is compile, schema, scenario or package in force, and {detail} names the row ID, the column or the package code only, never a payment or a person. The texts are copied unchanged from the legacy story; Thai text follows DL10.

### 15. Screens and states

SCR-28 Proceeds matching is composed by the gateway-bff route (DP-19) in its loading, matched and unmatched states, and this story serves its data through `GET /proceeds`. For each matched receipt the screen shows the rule ID and the package version from the local decision record; for each unmatched receipt it shows the reason. PAYMENT_MATCH versions show on SCR-39 Rules and parameters (Epic 8) and on rwb-decision's version list; SCR-40 holds no payment matching table, because the match types and the thresholds are rule-row columns and never reference data.

| Where | State | What the caller sees |
|---|---|---|
| SCR-28 matched | Matched | The receipt, the plan, the rule ID and the package version that decided |
| SCR-28 unmatched | Unmatched | The receipt, its amount and the reason it matched no row |
| The run summary | Stopped, no version in force | MSG-P3-027 with the package in force check and the business date |
| The run summary | Record failure | MSG-P7-003 for the payment codes whose record could not be written |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01 | AC1, BR2, BR6 — AC1 is not owned by this split (RWB-P8-E2008-APP owns the exact match; this story proves the row is evaluated) | Component | PAY-91001 12,500.00; PAYMENT_MATCH version PM-2026.12 |
| TC-E2-027-02 | AC2, BR4 — AC2 is not owned by this split (RWB-P8-E2008-APP owns the partial match) | Component | PAY-91002 11,875.00 |
| TC-E2-027-03 | AC3, BR6 — AC3 is not owned by this split (RWB-P7-E2027-APP owns the version load and the dated version) | Component | PM-2027.01 from 2027-01-01; PAY-91003 4 days late |
| TC-E2-027-04 | AC4, BR3, BR5 — AC4 is not owned by this split (RWB-P8-E2008-APP owns the window cases) | Component | PAY-91004 3 days late, PAY-91005 4 days late |
| TC-E2-027-05 | AC5, BR4, BR5 — AC5 is not owned by this split (RWB-P8-E2008-APP owns the partial-floor case) | Component | PAY-91006 10,000.00 |
| TC-E2-027-06 | AC6, BR7 — owned here | Component | PM-2027.02 with duplicate row order and tolerance 120, through the rwb-decision registry fake |
| TC-E2-027-07 | AC7, BR8 — owned here | Component | Decision record library forced to fail during the JOB-07 run |
| TC-E2-027-08 | AC8, BR2 — AC8 is not owned by this split (RWB-P8-E2008-APP owns the overpayment case) | Component | PAY-91007 13,000.00 |
| TC-E2-027-09 | AC9, BR1 — AC9 is not owned by this split (RWB-P8-E2008-APP owns the row-order case; this story proves one row fires and one record is written) | Component | PAY-91008 matched by two rows |
| TC-E2-027-10 | AC10, BR9 — owned here | Component | No PAYMENT_MATCH version in force on 2027-02-01 |
| TC-E2-027-11 | Access — the read operation of this story is `GET /proceeds`, so the case is executed here | Contract | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-027-12 | Access — the load operation is rwb-decision's, so the case is executed there and this story proves the refusal reaches the caller | Contract | RW-CASEOWN calls POST /admin/rule-packages/PAYMENT_MATCH/versions; refused with MSG-P4-002 |
| TC-E2-027-13 | Principle 5 — owned here | NFR | Decision record write forced to fail for 50 payments; no proceeds row written |

The Covers column keeps the legacy criterion and rule labels of RWB-E2-027 that each case was written for — the ACn and BRn of the legacy story, not the numbers of sections 7 and 8 of this story — and names where a legacy criterion is not owned by this split. The legacy level `System` maps to `Component`, `Access` to `Contract` and `Resilience` to `NFR` (Template and Rules §R7.2 s16). The `-ITG` copies of all thirteen cases belong to the wave 2 harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the match type, the row order, the amount tolerance, the window, the grace and the partial floor are columns of the PAYMENT_MATCH rule rows; no threshold, no window and no floor is a constant, a default or a reference-table value.
- No personal data in logs, events, workflow inputs, test data or prompts: the records and the event payloads hold payment codes, case and plan references, amounts, dates, rule IDs and version labels only.
- ACE data only through the owner's contract or this service's `v_ace_*` views: no other module's table is read and no cross-schema foreign key exists (DP-01, DP-05).
- One evaluator, no direct read: the matching engine calls the embedded kit and reads no workbook, no `drl_source` and no `rule_row`; the registry is reached only through the operations of 12.2 (DP-04).
- The record is written before the row: no match exists without its local decision record, and a failed record leaves the payment unmatched with MSG-P7-003 (BR8).
- The package version in force is chosen once per run from the business date; no match is made without a version in force and no default version is ever substituted (BR9, BR12).
- The model is verified by its checksum before it is used; a mismatch keeps the last good model and alerts (X8).
- One base, one topic, one queue and one login per service; the topic, the retry topic and the `.dlt` topic come from the naming library and never from a literal (DP-13, DP-14).
- No secret in code, a test, a values file or a log: the rwb-payment login (DP-02), the Kafka credential and the Temporal material come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list — decided here by the evaluated PAYMENT_MATCH rows of the version in force | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01 to TC-E2-027-13 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-027, disposition Split (rework) |
| Legacy criteria | AC6, AC7 and AC10 owned word for word here; AC1, AC2, AC4, AC5, AC8 and AC9 with RWB-P8-E2008-APP; AC3 with RWB-P7-E2027-APP |
| Feature and screen | FEAT-OCC-10, FEAT-PAY-01; SCR-28 Proceeds matching through the gateway-bff route |
| Rules | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41; the PAYMENT_MATCH rows EXACT, WINDOW and PARTIAL |
| Decoupling patterns | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Architecture decisions | ADR-012 (embedded Drools and versioned packages, amended), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox), ADR-016 (Temporal replaces Quartz), ADR-017 (embedded Drools per service, registry in rwb-decision), ADR-020 (contract-first REST), ADR-022 (local decision record) |

### 19. Out of scope

- The registry and the governance of a package version — the load, its seven checks, the four-eyes approval, the 00:01 promotion, the one-call rollback and the version states: rwb-decision (P7), RWB-P7-E2027-APP.
- The PAYMENT_MATCH workbook, its Rows and Tests tabs and the authoring pipeline: rwb-case (P3), RWB-P3-E2042-APP and RWB-P3-E1073-APP.
- The session, the roles, the rights and the delegation of authority: rwb-access (P4).
- The installment shortfall on the plan and the plan route states: rwb-treatment (S2) and rwb-case (P3).
- The manual match `POST /proceeds/{proceedsId}/match` and its screen flow, the settlement payment matching, the auction and enforcement proceeds, the application of proceeds to the case balance in policy order and the reconciliation agent: the Epic 4 stories of this service (RWB-P8-E4043-APP, RWB-P8-E4044-APP, RWB-P8-E4049-APP).
- The booking confirmation and the posting file (JOB-08, `confirmBookings`, `postProceeds`) beyond their declaration in 12.5.
- The deployment of this capability — the topics, the worker pool, the alerts, the canary gate, the rollback and the rule-cache refresh runbook: RWB-P8-E2027-OPS.
- The contract document, its schemas, its Idempotency-Key rule, its error envelope and its fakes: RWB-P8-E2027-CON.
- The real cross-service proof of the match, the record, the event and the version across rwb-payment, rwb-decision, rwb-case, rwb-treatment and rwb-access: the wave 2 harness.
- The retired `payment_match_rule` table and its reference loads (D-RCV-36 T10): this story never creates it and never reads it.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
