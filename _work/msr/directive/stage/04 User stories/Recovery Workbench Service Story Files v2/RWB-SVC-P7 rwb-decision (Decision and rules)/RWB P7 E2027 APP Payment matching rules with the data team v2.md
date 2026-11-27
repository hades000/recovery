# RWB-P7-E2027-APP Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-AH |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E2027-APP-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2027-CON, version Not specified in the source documents (DOR-RWB-P7-E2027-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CHO-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-027 for rwb-decision, the rule registry and the PAYMENT_MATCH governance of the matching rules. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2027-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (39 resolved, 31 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the PAYMENT_MATCH rule package held and governed in the rwb-decision registry — the package row, its version rows, the parsed row catalogue and its test cases, with the load of a workbook version and every check on it, the four-eyes approval, the promotion at 00:01 and the one-call rollback, each written as a decision record and readable through the decision log**, so that **a matching rule changes as approved, dated data that every consuming service can name, and no version reaches a payment run without at least 50 passing test cases and a second pair of eyes**.

Inside `rwb-decision` this is the registry and governance half of the legacy story RWB-E2-027:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` for the decision records every governance action writes (DP-03).
- One deliverable and nothing else: the PAYMENT_MATCH package in the rule registry and its governance — the `rule_package` row, the `rule_package_version` rows "PM-2026.12" and "PM-2027.01" and the refused "PM-2027.02", the parsed `rule_row` catalogue (EXACT at row order 1, PARTIAL at 2, WINDOW at 3), the `rule_test_case` set of at least 50 cases (58 for the package), the load with its compile, schema, overlap, unreachable row, default row and scenario checks and its dry run, the four-eyes approval, the promotion at 00:01, the one-call rollback, and one decision record for each of those actions, read through `GET /api/recovery/decision/v1/decision-log`.
- The match stays with `rwb-payment` (P8, RWB-P8-E2027-APP): JOB-07 and its event-started workflow, the `RuleEvaluator` call, the fired row, the proceeds row, the posting file, the exception list and the D5 entry a match writes. This story never matches a payment, writes no proceeds row and reads no ACE view.
- The workbook and its Rows and Tests tabs stay with `rwb-case` (P3, RWB-P3-E2042-APP and the authoring pipeline RWB-P3-E1073-APP), with the parameters and the reference data those stories publish (DP-06, DP-07); this story receives the workbook at the load operation and resolves no rule value of its own.
- The session, the role, the right and the delegation of authority stay with `rwb-access` (P4, RWB-P4-E2027-APP); the installment shortfall a PARTIAL match passes to the plan stays with `rwb-treatment` (S2, RWB-S2-E2027-APP).
- The registry is rwb-decision's under the R-PREC default ruling: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 rows (ASM-2293), and the generic scaffold of RWB-P7-E2042-APP — the four tables, their Flyway baseline and the shared operation signatures — is reused and not rebuilt (ASM-2295). Every consuming service holds only an evaluated copy (DP-04).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1290; ASM-2289); this story uses the phrase "the rwb-decision login (DP-02)" and never the shared monolith login.

The legacy rule change of RWB-E2-027 is carried into the registry unchanged: the same package code PAYMENT_MATCH, the same three rows and their row order, the same thresholds as row columns, the same "the author cannot approve" rule, the same dated version in force, and the same refusal of an invalid load in full.

### 2. Business rationale

The matching rules of RWB-E2-027 are the reason a short or a late installment matches without a person. In the monolith they were a table read by code; the two rules that were missing, PARTIAL and WINDOW, could only arrive as a change to the matching class. D-RCV-36 T10 retires `payment_match_rule` and makes the match type, the amount tolerance, the window, the grace and the partial floor columns of a decision table, so a change of a threshold is a change of data, not code. That only works if the data is governed: tested, approved by a second pair of eyes, dated, promoted and reversible in one call.

Governance is central and evaluation is local (Arch v5 slide 27; ADR-017). rwb-decision owns the registry — the packages, their versions, the parsed rows and the test cases — and publishes `RulePackageInForce` when an approved version reaches its valid-from date. The owning service loads the model, verifies the checksum and swaps it in (DP-04). Without the registry there is no answer to the two questions an audit asks of every match: which rule fired, and under which approved version.

This story is the rwb-decision half of that split for RWB-E2-027. rwb-case writes the PAYMENT_MATCH workbook and its Tests tab, rwb-payment runs JOB-07 against the version in force, and this story holds the package, proves at load that the rows are consistent and that at least 50 test cases pass, takes the approval from a role other than the author, promotes the version at 00:01, rolls it back in one call when it must, and records every one of those actions in the decision log. It is what makes the measure of RWB-E2-027 true: every match names its rule and its package version, and no version reaches a run untested or unapproved.

The realignment changes the mechanism, not the business rule:

1. The reference rule tables of the monolith become `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` in `rwb_decision`, with no other service reading them (DP-01). The 448 route-set rows and the other packages are not this story's; PAYMENT_MATCH is.
2. The version label and the valid-from date become the identity of a version, and the version in force on a business date is a lookup and never a default (BR6, BR10).
3. The load checks of the legacy version load become the registry's own pipeline — compile, schema, overlap, unreachable row, default row, at least 50 scenarios and the dry run — and a failure refuses the whole load (BR3).
4. The approval becomes a four-eyes operation of the service: RW-RISK approves, the author cannot, and the approval is not a credit decision of the delegation of authority (ASM-2294).
5. The nightly copy to the data lake is gone (DP-17); the announcement of a version in force is `rwb.decision.RulePackageInForce.v1`, and each governance action writes a local decision record that is published on `rwb.decision-record.v1` (DP-03).
6. The Quartz job that promoted a version becomes the JOB-20 Temporal Schedule at 00:01 on the `rwb-decision` queue (DP-10), which this story registers the package with and does not create (ASM-2296).

This story meets REQ-CHO-009 on the governance side and carries the rule-version half of R-UNI-38 and R-UNI-41: an earlier decision keeps the version it was taken under, and no version in force is a refusal and never a default match.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P8-E2027-CON | The published rwb-payment contract: what a match entry names — decision code D5, the rule ID of the fired row and the package version in force on the business date — and the decision read the rollback criterion uses. This registry serves that contract; the match itself is not built here. Faked, one hop, 2 s (DP-11) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one record per governance action, written in the same transaction as the action |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): the compile of the workbook to a KieBase, the checksum, first-match semantics and the `NoPackageInForce` outcome, used at load and at promotion and never at evaluation |
| RWB-PLT-E1071-CON | The Temporal workflow kit in namespace `rwb-recovery` (DP-10): the JOB-20 rule-promote Schedule runs on it; this story starts no workflow of its own |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the rwb-case parameters contract (DP-06): `rules.testcases.min` = 50 (Temporal and Drools slide 15 notes) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the rwb-case reference-data contract (DP-07): LOV-DECISION and the version-state vocabulary with the version in force |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic and event names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19); no screen of this story is served through it, the Epic 8 screen is |
| RWB-P7-E2042-APP, RWB-P7-E1073-APP | The registry scaffold and the authoring pipeline of rwb-decision: the four tables, their baseline, the shared operation signatures and the workbook checks. Reused where they have landed and built against their published set and fake (ASM-2295); no build dependency of this story |

Build-against set: the platform and rwb-case contracts of the DP table are the preconditions in the table above, built against their published set and fake. The metadata rows stay as the WP fixes them (Depends on (build) None; Contract dependencies RWB-P8-E2027-CON only). To be confirmed at the wave 2 planning gate that no H chain is missing from the wave 2 lane plan.

Business preconditions carried from RWB-E2-027:

- The package code PAYMENT_MATCH exists with owner role RW-COE, and version "PM-2026.12" is in force from 2026-12-01 with the EXACT, WINDOW and PARTIAL rows of section 7 (legacy sections 3 and 7).
- The PAYMENT_MATCH workbook holds the Rows tab (RuleSet = package code, NAME = rule ID, default row last) and the Tests tab with at least 50 test cases; the package carries 58 (RWB-P3-E2042-APP AC2; `rules.testcases.min` = 50). The 58 is the count of the Tests tab and is copied from the E2-042 package of the same code.
- Version "PM-2027.01" is authored with valid from 2027-01-01 and changes WINDOW to 5 days after the due date (legacy AC3); version "PM-2027.02" is authored with rows WINDOW and PARTIAL both at row order 2 and a PARTIAL tolerance of 120 (legacy AC6).
- RW-COE holds Rules and parameters C, RW-RISK holds Rules and parameters A and RW-AUDIT holds Rules and parameters R (legacy section 10 and section 12).
- The rwb-decision login (DP-02) is in the platform secret store; its name is Not specified in the source documents (GAP-1290; ASM-2289).
- Synthetic data only: the test cases, the dry run and the evidence of this story hold package codes, version labels, rule IDs, row orders, thresholds, dates, amounts and payment codes of the legacy story, never a real account, customer or payment (legacy section 17).
- The three LOV-MATCH-TYPE codes are carried as the match_type column of the PAYMENT_MATCH package: rwb-decision (P7) holds them and rwb-payment (P8) reads them (GAP-0218).
- The PAYMENT_MATCH package, its rows and its versions are held by rwb-decision (P7); the match and the proceeds row stay with rwb-payment (P8). rwb-treatment evaluates the version in force for the plan consequence its treatment row needs, takes the breach threshold from the row outputs, and publishes rwb.treatment.TreatmentClosed.v1 once for a breached plan. The completed-plan closure is left to the plan story.

### 4. Flow

1. RW-COE: authors the PAYMENT_MATCH workbook in rwb-case with its Rows and Tests tabs (RWB-P3-E2042-APP), stores it write-once with its SHA-256, and calls the load operation of rwb-decision with the workbook and the valid-from date.
2. rwb-decision `RuleVersionService`: reads the parameter `rules.testcases.min` through DP-06, parses the Rows tab into `rule_row` candidates and the Tests tab into `rule_test_case` candidates, and compiles the workbook to a KieBase through the embedded Drools kit (DP-04).
3. rwb-decision `RuleCheckPipeline`: runs the compile check, the schema check on the condition and output columns, the overlap check, the unreachable row check, the default row check and the scenario check against at least `rules.testcases.min` = 50 test cases, then the dry run; any failure refuses the whole load with MSG-P3-027 and writes nothing.
4. rwb-decision `RuleVersionService`, one transaction: writes the `rule_package_version` row with status LOADED, the workbook reference, the generated DRL, the checksum, the valid-from date, the author, the test result and the dry-run counts; writes the `rule_row` rows and the `rule_test_case` rows of the version; writes the decision record of the load (DP-03); and returns 201 with the version.
5. RW-RISK: approves the version through the approve operation. The service refuses the call when the approver is the author (MSG-P7-002), and otherwise moves the version to APPROVED, records the approver and the approval time, and writes the decision record of the approval.
6. JOB-20: the rule-promote Temporal Schedule runs at 00:01 on the `rwb-decision` queue (Arch v5 slide 44; DP-10). It promotes every APPROVED version whose valid-from date has arrived to IN_FORCE, supersedes the version it replaces, writes the decision record of the promotion and publishes `rwb.decision.RulePackageInForce.v1` with the fields of Kafka Catalog v1 EV-30: the package code, the package version, the version ID, the valid-from date and the approver. A version whose valid-from date has not arrived is not promoted.
7. The consuming service (rwb-payment for PAYMENT_MATCH) consumes the event, fetches the model and swaps it in (the event carries no checksum; checksum verification is Not specified in the source documents (CG-ALL-7322)); this story builds none of that (DP-04, RWB-P8-E2027-APP).
8. RW-COE: when a version in force must be withdrawn, calls the rollback operation once for the version. The service moves the pointer to the version in force before it, marks the rolled-back version ROLLED_BACK, keeps every earlier decision on the version it was taken under, and writes the decision record of the rollback. A rollback with no earlier version is refused with MSG-P3-015.
9. RW-AUDIT or any role with the decision-log read: reads the governance actions through `GET /api/recovery/decision/v1/decision-log` by package, date and actor, and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, with its inputs reference, rule ID, rule version, actor, final call, decided time, previous hash and entry hash.
10. Nothing in this story matches a payment, writes a proceeds row, calls rwb-treatment or changes a case status: the registry and its governance are the whole deliverable.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A version is loaded with two rows of the same row order (named priority in the TSD), or a tolerance above 100 | The load is refused in full with 422; no version row, no rule row and no test-case row is written; "PM-2026.12" stays in force | MSG-P3-027 | AC3, TC-E2-027-06 |
| X2 | The Tests tab holds fewer than `rules.testcases.min` cases, or a case fails | The load is refused with 422, the failing check and the failing case IDs named; no version is created | MSG-P3-027 | AC4 |
| X3 | The author of the version calls approve | The call is refused; the version stays LOADED and no approval is recorded | MSG-P7-002 | AC5 |
| X4 | The decision record of an action cannot be written | Nothing is committed: no version row, no status change, no promotion, no rollback, no event; an incident is raised and the action is retried by its caller | MSG-P7-003 | AC10, TC-E2-027-07, TC-E2-027-13 |
| X5 | A rollback is called for the only version the package has, or for a version that was never in force | The call is refused; the version in force stays in force and nothing is written | MSG-P3-015 | AC8 |
| X6 | A version label that already exists for the package is loaded again | The load is refused with 409; the version already held is untouched | MSG-GEN-004 | AC11, TC-E2-027-06 |
| X7 | An empty workbook, or a workbook without validFrom, is loaded | The load is refused with 422 and the missing field named; nothing is written | MSG-GEN-001 | AC12, TC-E2-027-06 |
| X8 | The caller holds no right for the operation, or the version is outside the caller's scope | 403 with MSG-P4-002; nothing is read, written or promoted | MSG-P4-002 | AC13, TC-E2-027-11, TC-E2-027-12 |
| X9 | No version has a valid-from date on or before the business date, so no version is in force for it | The registry answers that no version is in force for that date; the consuming service raises `NoPackageInForce` and reports MSG-P3-027; no default version is ever substituted | MSG-P3-027 | AC14, TC-E2-027-10 |

A stale version row at commit, matched on its `version` column, is MSG-GEN-004 and the action is retried, never applied twice. The version row, its rule rows, its test-case rows and its decision record are always written together, so a version cannot exist without its record and no promotion can announce a version that was not recorded.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P8-E2027-CON, the platform contracts of its DP table, the registry scaffold of RWB-P7-E2042-APP and the fakes; it matches no payment and rebuilds no authoring pipeline |
| Negotiable | The version labels, the valid-from dates, the row values, the test cases and the message texts are data and registry rows; the story fixes only the checks, the four-eyes rule, the promotion and the rollback semantics |
| Valuable | A matching rule changes as approved, dated data with at least 50 passing cases and two pairs of eyes, and every change is explainable from the decision log |
| Estimable | One controller pair, one check pipeline, one test-case runner, one approval, one promotion handler, one rollback, one repository and one record writer |
| Small | Fits two weeks with its tests |
| Testable | Each criterion is a load, an approval, a promotion, a rollback or a read, with a fixed Given, When and Then and a recorded result |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given the rwb-access contract mock returns RW-COE holding Rules and parameters C, RW-RISK holding Rules and parameters A and RW-AUDIT holding Rules and parameters R
    Given the rwb-case contract mock returns rules.testcases.min 50 and the LOV-DECISION list with its version
    Given PAYMENT_MATCH package version "PM-2026.12" is in force from 2026-12-01 with rows:
      | rule_id | row_order | match_type | amount_tolerance_pct | window_days_before | window_days_after | partial_floor_pct |
      | EXACT   | 1         | EXACT      | 0                    | 10                 | 0                 |                   |
      | PARTIAL | 2         | PARTIAL    | 0                    | 10                 | 3                 | 90                |
      | WINDOW  | 3         | WINDOW     | 0                    | 10                 | 3                 |                   |
    Given case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15

  Scenario: AC1 The PAYMENT_MATCH package and the version in force (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-AUDIT holding Rules and parameters R
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages
    Then the answer holds PAYMENT_MATCH with owner role RW-COE
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer holds version "PM-2026.12" with status "IN_FORCE", valid from 2026-12-01, its checksum and its test result "58 of 58 test cases passed"
    And no other PAYMENT_MATCH version is in force on 2026-12-01
    And the registry holds the three rule rows EXACT at row order 1, PARTIAL at 2 and WINDOW at 3 (GAP-3180) under version "PM-2026.12"

  Scenario: AC2 A valid version is loaded and tested (new, D-RCV-60)
    Given the rwb-case contract mock returns the PAYMENT_MATCH workbook version "PM-2027.01" with 3 rows, 58 test cases in its Tests tab and valid from 2027-01-01, changing WINDOW to 5 days after
    When RW-COE loads it with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions and validFrom 2027-01-01
    Then the compile, schema, overlap, unreachable row and default row checks pass
    And the answer is 201 with versionLabel "PM-2027.01", status "LOADED", validFrom 2027-01-01, the author, the checksum, testResult total 58, passed 58, failed 0 and the dry run counts
    And the registry holds 58 rule_test_case rows under version "PM-2027.01" with their expected and actual result
    And the decision record of the load is written before the version row commits

  Scenario: AC3 An invalid version is refused in full (new, D-RCV-60)
    Given the rwb-case contract mock returns the PAYMENT_MATCH workbook version "PM-2027.02" whose rows "WINDOW" and "PARTIAL" both have row order 2 and whose "PARTIAL" row has tolerance 120
    When RW-COE loads it with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer is 422 with MSG-P3-027 for the schema check naming "PARTIAL" and the tolerance column
    And no version row, no rule row and no test-case row is written for "PM-2027.02"
    And "PM-2026.12" stays in force

  Scenario: AC4 A version below the test-case minimum is refused (new, D-RCV-60)
    Given the rwb-case contract mock returns rules.testcases.min 50
    Given the rwb-case contract mock returns a PAYMENT_MATCH workbook whose version label is Not specified in the source documents (GAP-1290; ASM-2289) and whose Tests tab holds 49 test cases
    When RW-COE loads it with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer is 422 with MSG-P3-027 for the scenario check
    And no version is created and "PM-2026.12" stays in force

  Scenario: AC5 The author cannot approve and a second role does (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-COE holding Rules and parameters C and RW-RISK holding Rules and parameters A
    Given PAYMENT_MATCH version "PM-2027.01" is "LOADED" with valid from 2027-01-01
    When RW-COE calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve
    Then the call is refused with MSG-P7-002 and the version stays "LOADED"
    When RW-RISK calls the same operation with a distinct user reference
    Then the version is "APPROVED" with RW-RISK as approver and the approval time
    And the decision record of the approval names the package "PAYMENT_MATCH", the version "PM-2027.01" and the approver

  Scenario: AC6 An approved version is promoted at 00:01 on its valid-from date (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2027.01" is "APPROVED" with valid from 2027-01-01
    When the JOB-20 rule promote Schedule runs at 00:01 on 2027-01-01
    Then version "PM-2027.01" is "IN_FORCE" and version "PM-2026.12" is "SUPERSEDED"
    And rwb.decision.RulePackageInForce.v1 is published on rwb.decision.events.v1 with packageCode "PAYMENT_MATCH", packageVersion "PM-2027.01", the version ID, validFrom 2027-01-01 and the approver
    And the decision record of the promotion names the package, the version and the rwb-decision service identity
    And version "PM-2027.01" is not promoted by a run of the Schedule before 2027-01-01

  Scenario: AC7 Rollback moves the pointer to the previous version (new, D-RCV-60)
    Given the rwb-payment contract mock returns the D5 entry of payment "PAY-91003" with rule "WINDOW" and rule version "PM-2027.01"
    Given PAYMENT_MATCH version "PM-2027.01" is "IN_FORCE" from 2027-01-01 and version "PM-2026.12" was in force before it
    When RW-COE calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback once for "PM-2027.01"
    Then version "PM-2026.12" is "IN_FORCE" and version "PM-2027.01" is "ROLLED_BACK"
    And the change report holds the rollback with the role that called it, the time and the reason
    And the D5 entry of "PAY-91003" keeps rule version "PM-2027.01"
    And the decision record of the rollback names the package, the two versions and the reason

  Scenario: AC8 A rollback with no earlier version is refused (new, D-RCV-60)
    Given PAYMENT_MATCH holds only version "PM-2026.12" and it is "IN_FORCE" from 2026-12-01
    When RW-COE calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback once for "PM-2026.12"
    Then the call is refused with MSG-P3-015
    And "PM-2026.12" stays "IN_FORCE" and no rollback is recorded

  Scenario: AC9 Every governance action is a decision record the log returns (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2027.01" was loaded, approved and promoted on 2027-01-01
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with ruleId "PAYMENT_MATCH" from 2027-01-01 to 2027-01-01
    Then the answer is 200 with the entries of the load, the approval and the promotion
    And each entry holds inputsRef, ruleId "PAYMENT_MATCH", ruleVersion "PM-2027.01", the actor, the decision code of the LOV-DECISION list, finalCall and decidedAt
    When RW-AUDIT reads one of them with GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the answer holds that entry's prevHash, entryHash, actions and outcome

  Scenario: AC10 A governance action whose decision record cannot be written is not taken (new, D-RCV-60)
    Given the decision log write is forced to fail
    When RW-COE loads the PAYMENT_MATCH workbook version "PM-2027.01" with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions and validFrom 2027-01-01
    Then the answer is 503 with MSG-P7-003
    And no version row, no status change, no promotion, no rollback and no event is written
    And an incident is raised and the action is retried by its caller

  Scenario: AC11 A version label already loaded is refused (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2026.12" is "IN_FORCE" from 2026-12-01
    When RW-COE loads a PAYMENT_MATCH workbook with the version label "PM-2026.12" with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer is 409 with MSG-GEN-004
    And the version already held is untouched

  Scenario: AC12 An empty workbook or one without validFrom is refused (new, D-RCV-60)
    Given the rwb-case contract mock returns a PAYMENT_MATCH workbook that is empty or has no validFrom
    When RW-COE loads it with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer is 422 with MSG-GEN-001 naming the missing field
    And nothing is written

  Scenario: AC13 A caller with no right for the operation is refused (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-CASEOWN holding no Rules and parameters right
    When RW-CASEOWN calls POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer is 403 with MSG-P4-002
    And nothing is read, written or promoted

  Scenario: AC14 No version in force on the business date is refused, never defaulted (new, D-RCV-60)
    Given no PAYMENT_MATCH version has a valid-from date on or before a business date before 2026-12-01
    When the consuming service asks the registry for the version in force on that business date
    Then the registry answers that no version is in force for that date
    And the consuming service raises NoPackageInForce and reports MSG-P3-027
    And no default version is substituted

  Scenario: AC15 A version status is one of the six registry states (new, D-RCV-60)
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then every version holds a status of LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK or REFUSED
    And no other status value is written

  Scenario: AC16 No operation other than a load writes a rule row or a test case (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2027.01" is "LOADED" with its rule rows and test cases
    When RW-RISK calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve for "PM-2027.01"
    Then the rule rows and test cases of "PM-2027.01" are unchanged
    And only the load writes rule_row and rule_test_case rows

  Scenario: AC17 The decision code and rule ID of a governance record are reference values (new, D-RCV-60)
    Given the rwb-case contract mock returns the LOV-DECISION list with its version
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with ruleId "PAYMENT_MATCH" from 2027-01-01 to 2027-01-01
    Then every entry holds a decision code of the LOV-DECISION list and the ruleId of its package

  Scenario: AC18 An error answer of 401 or 404 is given as the provided operations define it (new, D-RCV-60)
    Given the caller holds no session
    When RW-COE calls POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions with no session
    Then the answer is 401 with Not specified in the source documents (NEWAC-RWB-P7-E2027-APP-AC18)
    And nothing is read, written or promoted
    When RW-COE calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback for a versionId that does not exist
    Then the answer is 404 with Not specified in the source documents (NEWAC-RWB-P7-E2027-APP-AC18)
    And nothing is written

  Scenario: AC19 A replayed write with the same idempotency key is applied once (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2027.01" was loaded with the idempotency key Not specified in the source documents (NEWAC-RWB-P7-E2027-APP-AC19)
    When RW-COE repeats the same POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions with that idempotency key
    Then the registry holds one version row for "PM-2027.01" and no second rule row, test-case row or decision record is written
```

The nineteen criteria are new under D-RCV-60 and they test only the registry and its governance. None of them matches a payment: AC7 reads the D5 entry of "PAY-91003" from a contract fake, and every other value is the legacy story's. The legacy criteria of RWB-E2-027 stay with the other slices of the key — the match with RWB-P8-E2027-APP, the workbook with RWB-P3-E2042-APP, the rights with RWB-P4-E2027-APP, the shortfall with RWB-S2-E2027-APP — and the cross-service journey with RWB-ITG-E2027-ITG (ASM-2289).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The registry is rwb-decision's, and a version is never edited in place: a change is a new version, and a rollback moves a pointer | Arch v5 slides 27 and 41; ASM-2293; DP-01 |
| BR2 | Every version is loaded from the Drools XLS workbook through the load operation, and the version row holds the workbook reference, the generated DRL, the SHA-256 and the valid-from date | Temporal and Drools slide 15 and its notes |
| BR3 | The load checks are compile, schema, overlap, unreachable row, default row, at least `rules.testcases.min` = 50 scenarios and the dry run; any failure refuses the load in full | Temporal and Drools slide 15; legacy BR7; AC-P7-007-01 |
| BR4 | First match wins, the default row is last, and the PAYMENT_MATCH row order is EXACT 1, PARTIAL 2, WINDOW 3 (GAP-3180; legacy order EXACT, WINDOW, PARTIAL) | legacy BR1; D-RCV-36 T5 |
| BR5 | The author of a version cannot approve it; the approver is RW-RISK, and the two are distinct users holding Rules and parameters C and A | Temporal and Drools slide 15; legacy section 10; ASM-2294 |
| BR6 | A version is in force from its valid-from date; JOB-20 promotes an APPROVED version at 00:01, supersedes the version it replaces and publishes `RulePackageInForce` | Arch v5 slides 14, 27 and 44; Temporal and Drools slide 15 |
| BR7 | A rollback is one call and puts the version in force before the rolled-back one in force; a decision taken under the rolled-back version keeps that version on its record | FSD P7 AC-ALT-P7-007-02; legacy BR6 |
| BR8 | Every governance action — load, approve, promote, roll back — writes its decision record in the same transaction, and an action whose record cannot be written is not taken | FSD P7 VR-P7-001-2 and principle 5; legacy BR8; ASM-2297 |
| BR9 | The match type, row order, amount tolerance, window, grace and partial floor are columns of the rule rows, not code; the rows are the PAYMENT_MATCH package fetched from rwb-decision, and any parameter row that holds these values is read through the rwb-case contract (GAP-1628) | legacy BR10; D-RCV-36 T10 |
| BR10 | No version in force on the business date is `NoPackageInForce` and MSG-P3-027, never a default version | legacy BR9; D-RCV-36 T3 |
| BR11 | The version states are LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, and no other value is written | Temporal and Drools slide 15 notes; TSD P7 v2 T3.1 |
| BR12 | No user, role or code writes `rule_row` or `rule_test_case` except through a load; the parsed rows and the test cases are derived from the workbook of the version | Temporal and Drools slide 15 T4 and T6; AC-P7-007-01 |
| BR13 | The decision code, the rule ID and the rule version of a governance record are values of the LOV-DECISION list and of the package, never a constant of the code | TSD P7 v2 T3.1 `decision_log_entry`; ASM-2289 |

### 9. State transitions

This story changes no case status and no plan state. It owns the state of a package version.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A workbook is loaded | Every check passes and the decision record is written | LOADED |
| (none) | A workbook is loaded | A check fails, the label exists, or the record cannot be written | (no row is created); the earlier version in force keeps its state |
| LOADED | Approve | The caller is not the author and holds Rules and parameters A | APPROVED |
| LOADED | Approve | The caller is the author | LOADED (refused, MSG-P7-002) |
| APPROVED | JOB-20 at 00:01 | The valid-from date has arrived | IN_FORCE; the version it replaces becomes SUPERSEDED |
| APPROVED | JOB-20 at 00:01 | The valid-from date has not arrived | APPROVED (unchanged) |
| IN_FORCE | Rollback, one call | A version was in force before it | ROLLED_BACK; the previous version becomes IN_FORCE |
| IN_FORCE | Rollback, one call | No version was in force before it | IN_FORCE (refused, MSG-P3-015) |
| IN_FORCE | A newer version is promoted | The newer version reaches its valid-from date | SUPERSEDED |

The case and plan transitions of RWB-E2-027 — `PLAN_RUNNING` on `PAYMENT_RECEIVED` under R-RES-26 and `PLAN_CURE_PERIOD` on `PAYMENT_RECEIVED_LATE` under R-RES-28 — are rwb-case's and rwb-payment's, and this story neither raises nor observes them. The matching read is taken from RWB-P8-E2027-CON as published; a plan breach writes the plan state with outcome BROKEN and outcome_at on the standard state column, and the plan check is one durable workflow timer with the 30-day cure period (GAP-1880). The RES rule set is evaluated in rwb-treatment with the package in force from this service; CURE_PERIOD_DAYS and restructure.max_breaks are read from the rwb-case parameters contract; no plan event is published in wave 2, and the package code and parameter keys stay open items of the contract freeze (GAP-2706).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a PAYMENT_MATCH workbook version, runs the dry run, calls the rollback, and reads the registry and the decision log (Rules and parameters C and R) |
| RW-RISK, risk and model risk officer | Approves a loaded version (Rules and parameters A); may not be the author of the version |
| RW-AUDIT, internal audit | Reads the package, the versions, the test results and the governance decision records (Rules and parameters R) |
| RW-DATASTEW, data steward and data product owner | Reads the versions and their valid-from dates (Rules and parameters R) |
| The rwb-decision service identity | Runs the checks, the dry run, the promotion handler and the rollback, and writes the decision records |
| SY-DECLOG, decision log writer | Supplies the hash-chained record write of DP-03 |
| SY-RULES, Drools evaluator | Compiles the workbook and supplies first-match semantics and the checksum through the embedded kit at load (DP-04); it evaluates nothing in this story |
| RW-CASEOWN and any role without a Rules and parameters right | Refused with MSG-P4-002 on every operation of section 12.1 |
| No delegation of authority level applies | A package version is not a credit decision; the approval is four eyes and not a DoA level |

Separation of duty: the analyst who loads a version does not approve it, and RW-RISK approves with a distinct user reference (BR5; legacy section 10). No person is named anywhere; the actors are roles and service identities.

Every operation of section 12.1 passes an rwb-access authorise check (DP-08) before its handler runs. The check reads the Rules and parameters right of the caller; a caller without that right is refused with MSG-P4-002.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 to DF-REF-278 | rule_package (P7) | id, package_code, title, owner_role, hit_policy | Write the PAYMENT_MATCH package row on first use; read |
| DF-REF-279 to DF-REF-294 | rule_package_version (P7) | id, version label, status, source_blob_ref, drl_source, checksum, valid_from, valid_to, author, approver, test_result, dry_run_counts | Write; read |
| DF-REF-002, DF-REF-003 | rule_row (P7) | rule_id, rule_version | Write at load; read |
| DF-REF-296 to DF-REF-298 | rule_row (P7) | package_version_id, drools_rule_name, outputs | Write at load; read |
| DF-REF-008, DF-REF-010, DF-REF-011 | rule_row (P7) | action_text, owner_role, timer_spec | Write at load when the row carries them; read |
| DF-REF-185 to DF-REF-197, DF-REF-299 | rule_test_case (P7) | test case, expected result, actual result | Write at load; read |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031 | decision_log_entry (P7) | id, decision_code, rule_id, rule_version, inputs_ref, recommendation, approver_user_id, final_call, actions, outcome, decided_at, chain_seq, prev_hash, entry_hash, actor_user_id, idempotency_key | Write one row per governance action (DP-03); read through the decision log |
| DF-ACE-043, DF-ACE-044, DF-ACE-045, DF-ACE-046 | v_ace_payment | payment_code, account_key, payment_date, payment_amount | Not read here: they reach this story only as the decision record a match wrote, through RWB-P8-E2027-CON |
| DF-FIN-002, DF-FIN-003, DF-FIN-004, DF-FIN-006, DF-FIN-008 | proceeds (P8) | case_id, treatment_id, payment_code, amount, matched_to | Not read and not written here: `proceeds` is rwb-payment's |

The four registry tables and `decision_log_entry` are rwb-decision's and no other service reads them (DP-01; ASM-2293). The field IDs of the registry tables are those of the Logical Data Model and Data Dictionary v9 (CG-ALL-7319), with RWB-P3-E2042-APP's citation to be confirmed; the decision-entry field IDs are those of TSD P7 v2 T3.1. No new field is added by this story, except the two unique keys of section 13, which are constraints and not fields. `payment_match_rule` and DF-REF-261 to DF-REF-273 are retired and appear in this story only as the assertion that no version may recreate them (D-RCV-36 T10).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The six rule-package and rule-version paths are the ownership map's P7 paths; the two decision-log paths are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1 on the service base. The load and version-list request and answer shapes are the legacy section 12 shapes; the rollback request body, the dry-run body beyond `testResult` and `dryRunCounts`, and the decision code of a governance entry are Not specified in the source documents (GAP-1290; ASM-2289).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/rule-packages` | List the packages of the registry with their code and owner role; 200 with the package list | Rules and parameters R | Not applicable, read only |
| POST | `/admin/rule-packages/{packageCode}/versions` | Load a workbook version: multipart `file` (xlsx with the Rows and Tests tabs) and `validFrom`; run the checks and the dry run; 201 with the version | Rules and parameters C | Package code and version label; a repeated label is 409 with MSG-GEN-004 |
| GET | `/admin/rule-packages/{packageCode}/versions` | List the versions of a package with status, valid-from and valid-to dates, author, approver, checksum, test result and dry-run counts; 200 | Rules and parameters R | Not applicable, read only |
| GET | `/admin/rule-package-versions/{versionId}/dry-run` | Read the dry-run counts and the per-test-case result of a version | Rules and parameters R | Not applicable, read only |
| POST | `/admin/rule-package-versions/{versionId}/approve` | Approve a loaded version with four eyes; 200 with the version at APPROVED | Rules and parameters A | Idempotency-Key header; the author's call is refused with MSG-P7-002 |
| POST | `/admin/rule-package-versions/{versionId}/rollback` | Roll a version in force back to the version before it in one call; 200 with the two versions | Rules and parameters C | Idempotency-Key header; a second call for the same version finds it no longer in force |
| GET | `/decision-log` | Read the governance decision records by case, decision, rule, approver and date range; 200 with the page | Decision log R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | Read one decision record with its inputs reference, versions, actor, final call, actions, outcome and hashes; 200 | Decision log R, scope applied | Not applicable, read only |

The version body carries `versionId`, `packageCode`, `versionLabel`, `status`, `validFrom`, `validTo`, `author`, `approver`, `checksum`, `testResult` (`total`, `passed`, `failed`, `failedScenarioIds`) and `dryRunCounts`. Errors: 401 no session (messageId Not specified in the source documents (CG-ALL-7320)); 403 the role lacks the right (MSG-P4-002); 404 an unknown package code or version (messageId Not specified in the source documents (CG-ALL-7320)); 409 the version label exists (MSG-GEN-004) or the version is not in the state the call needs; 422 a check failed (MSG-P3-027 with the check, row and column in the problem detail) or a required field is missing (MSG-GEN-001); 503 the decision record could not be written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set. No promote operation is published: the promotion is JOB-20's Schedule of 12.6.

The version states, the check names and the match types are values of the registry and of the reference lists of DP-07, never constants of the code; the value set of the version states is the one Temporal and Drools slide 15 gives. The four `/admin/rule-versions` paths the ownership map also gives P7 are legacy paths with no target story: this story and the P7 registry stories serve the `/admin/rule-packages` and `/admin/rule-package-versions` families only (GAP-1293; ASM-2292).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case, on RWB-P3-E1042-CON | `rules.testcases.min` = 50 for the scenario check (DP-06); faked, one hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION and the version-state list with the version in force (DP-07); faked |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access, on RWB-P4-E1037-CON | The caller's role, scope and Rules and parameters right behind every operation of 12.1; the guard reads this answer and the operation declares the right it needs; faked |

The parameters and the reference lists are read through their client libraries and also over these two operations; neither is resolved into a rule value here. They are served in this story by the rwb-case parameters and reference-data fake of 12.8, and the session read by the rwb-access fake; the rwb-payment contract fake, the Drools kit fake and the decision-record library fake complete the fake set of 12.8. The contract dependency recorded on the story is RWB-P8-E2027-CON: rwb-payment's contract fixes what a match entry names, and this registry is what it names. The platform and published contracts the DP table adds are listed in section 13 and carried in the gap of GAP-1291.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 | packageCode | package code, package version, version ID, valid-from date, approver (Kafka Catalog v1 EV-30 fields packagecode, packageversion, versionid, validfrom, approvedby) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by this service | entryId | the hash-chained record of a governance action: decision code, rule ID (the package code), rule version, inputs reference, actor, final call, decided at |

Both are written to the outbox in the same transaction as the action and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform. `RulePackageInForce` is consumed by the owning services that hold an evaluated copy — for PAYMENT_MATCH that is rwb-payment — and by gateway-bff for its cache refresh (Arch v5 slides 20, 43 and 44). No event carries a name, an e-mail address, a mobile number or an account number.

#### 12.4 Events consumed

None. This story consumes no Kafka event: the workbook arrives through the load operation, the approval through its operation, and the promotion is the Schedule of 12.6. `ApprovalRequested` (EV-09) is not raised by a package-version approval, because that approval is not an item routed by the delegation of authority (BR5; ASM-2294).

#### 12.5 Workflows and activities

None of this story's own. The load, the approve and the rollback are synchronous REST operations; the promotion is the JOB-20 Temporal Schedule of 12.6 and not a workflow; and the embedded Drools kit is called in process at load and never inside a workflow. This story registers nothing on the `rwb-decision` task queue, starts no workflow and adds no activity, and the matching window of JOB-07 is rwb-payment's and not this story's (DP-10; ASM-2296).

#### 12.6 Schedules

| Schedule | When | Mechanism | Owner and this story's part |
|---|---|---|---|
| JOB-20 Rule promote | 00:01 | A Temporal Schedule on the `rwb-decision` queue that promotes every APPROVED version whose valid-from date has arrived to IN_FORCE, supersedes the version it replaces, writes the decision record and publishes `rwb.decision.RulePackageInForce.v1` (Arch v5 slide 44; Temporal and Drools slide 15) | P7 rwb-decision, shared rule-registry infrastructure. This story registers PAYMENT_MATCH with its valid-from date and asserts the promotion in AC6; it creates no Schedule and no new trigger (ASM-2296) |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `rule_package` | P7 (`rwb_decision`) | The PAYMENT_MATCH package row, its title, its owner role RW-COE and its hit policy |
| `rule_package_version` | P7 (`rwb_decision`) | The version, its status, workbook reference, generated DRL, checksum, valid-from and valid-to dates, author, approver, test result and dry-run counts |
| `rule_row` | P7 (`rwb_decision`) | The parsed, queryable catalogue of a version: rule ID, row order, the condition and output columns, action text, owner role and timer spec |
| `rule_test_case` | P7 (`rwb_decision`) | The test cases of a version with their expected and actual result |
| `decision_log_entry` | P7 (`rwb_decision`) | One append-only, hash-chained record per governance action |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects of the service |

Not owned and not read: `proceeds`, `treatment` and `v_ace_payment` (P8, S2 and P1); `parameter_value`, `reference_row` and `lov_value` (P3); `approval` is P7 but is not used by a package-version approval (BR5). No foreign key crosses a schema and no other service reads these five tables (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-payment contract fake | RWB-P8-E2027-CON | The D5 entry of "PAY-91003" with rule "WINDOW" and version "PM-2027.01", and the D5 entry of "PAY-91001" with rule "EXACT" and version "PM-2026.12", so AC7 can assert that an earlier decision keeps its version; the proceeds read is never called |
| rwb-case authoring fake | RWB-P3-E2042-APP and RWB-P3-E1073-APP | The PAYMENT_MATCH workbook of "PM-2027.01" with 3 rows and 58 test cases, the "PM-2027.02" variant with duplicate row order 2 and tolerance 120, a 49-case variant for AC4, an empty file for X7, and a repeated label for X6 |
| rwb-case parameters and reference-data fake | RWB-P3-E1042-CON, RWB-P3-E1043-CON | `rules.testcases.min` = 50; LOV-DECISION and the version-state list with their versions |
| rwb-access fake | RWB-P4-E2027-APP | `GET /me/session` for RW-COE with Rules and parameters C, RW-RISK with A, RW-AUDIT with R, and RW-CASEOWN refused with MSG-P4-002 |
| Drools kit fake | RWB-PLT-E1072-CON | The compile of a valid workbook, the checksum of the model, first-match semantics with the default row last, a compile failure and a checksum mismatch |
| decision-record library fake | RWB-PLT-E1027-CON | The append and the hash chain, the `DecisionRecorded` outbox row, and a forced failure for the 503 and MSG-P7-003 cases |

Each fake is replaced by the real contract or the real library as its story lands, without a change to the scenarios. The fakes carry synthetic package codes, version labels, rule IDs and payment codes only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 8, consumed 3 | The package read, the version list, the load, the dry run, the approve, the rollback and the two decision-log reads provided; the parameters, the reference list and the session read consumed, one hop and 2 s |
| Kafka | Published 2 event types, consumed 0 | `rwb.decision.events.v1` with `RulePackageInForce`, and `rwb.decision-record.v1` with `DecisionRecorded` |
| Temporal | None | The promotion is the shared JOB-20 Schedule; this story registers no workflow, activity or Schedule |
| File | 1 input | The PAYMENT_MATCH xlsx workbook with its Rows and Tests tabs, uploaded per version and stored write-once; no runtime file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `rules/registry`, Java package `th.co.scb.ace.workbench.recovery.decision.rules.registry`.

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

How this story applies each row. **DP-01**: the four registry tables and `decision_log_entry` sit in `rwb_decision`; the story reads no schema of another service and no service reads its tables — the rows travel as the model, the catalog and the event. **DP-03**: the load, the approval, the promotion and the rollback each write one local decision record in the same transaction and publish `DecisionRecorded` on `rwb.decision-record.v1`; a record that cannot be written stops the action (BR8). **DP-04**: the load and the promotion use the embedded kit for the compile, the checksum and first-match semantics, and the registry supplies the package to the consuming services; the C dependency RWB-P7-E1073-CON is this service's own rule-package contract story and is built against its published set, because the kit lives in the platform library and the contract story is consumed, not rebuilt. **DP-05**: no ACE view is read by this story; the payment facts reach it only through the decision entry a match wrote, and the registry never sees `v_ace_payment`. **DP-06**: `rules.testcases.min` = 50 is read as a parameter for the scenario check and is never a constant. **DP-07**: LOV-DECISION and the version-state list are read as reference data with the version in force; the match types and thresholds stay row columns and are never reference data (BR9). **DP-10**: the promotion is the JOB-20 Temporal Schedule at 00:01 and this story creates no workflow and no Schedule; the matching window of JOB-07 is rwb-payment's, so no job of the matching run appears here. **DP-11**: the three consumed operations are called once, one hop, on the owner's base with a 2 s timeout and a breaker; the legacy in-process calls to the parameter, the list and the access check become those published calls. **DP-13**: every path of section 12 uses `/api/recovery/decision/v1`; no monolith base appears. **DP-14**: the topic is `rwb.decision.events.v1`, the event is `rwb.decision.RulePackageInForce.v1`, and the shared decision-record topic keeps its platform name. **DP-15**: this story owns its migration in the `rwb_decision` Flyway sequence and touches no other schema. **DP-19**: no screen is built here; the Epic 8 screen reads these operations through the gateway-bff composite route and this story adds no route.

The platform H dependencies of the table — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — and the C dependencies C RWB-P7-E1073-CON, C RWB-P3-E1042-CON and C RWB-P3-E1043-CON are the DP-added dependencies that are **not** in the metadata rows, which name None and RWB-P8-E2027-CON. They are recorded in GAP-1291 and ASM-2290: they are platform contracts of wave 0 and published contracts of rwb-case and of this service, none of them blocks the build, and an APP story builds against the published set and its fake. DP-04 also brings this service's own rule-package contract story C RWB-P7-E1073-CON, and DP-06 and DP-07 bring the parameters and reference-data contracts of rwb-case.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RulePackageController | Controller | `GET /admin/rule-packages` and the version list, with the guard, the scope and the problem mapping |
| RuleVersionController | Controller | The multipart load, the dry run, the approve and the rollback, with the Idempotency-Key and the 201, 200, 409 and 422 answers |
| RuleVersionService | Service | Orders the load in one transaction: parse, check, dry run, version row, rule rows, test cases, decision record |
| WorkbookParser | Service | Reads the Rows tab into `rule_row` candidates (RuleSet = package code, NAME = rule ID, default row last) and the Tests tab into `rule_test_case` candidates; rejects an empty or malformed workbook with MSG-GEN-001 |
| RuleCheckPipeline | Service | Compile, schema, overlap, unreachable row, default row and scenario checks through the embedded kit; refuses the whole load with MSG-P3-027 and names the check, the row, the column and the failing case IDs |
| TestCaseRunner | Service | Runs the Tests tab against the compiled model, counts total, passed and failed, and records the expected and actual result of every case |
| DryRunService | Service | Runs the dry run over the test cases and stores the counts and the per-case result of the version |
| ApprovalService | Service | Refuses the author with MSG-P7-002, moves LOADED to APPROVED with the approver and the time, and writes the decision record |
| PromotionService | Schedule handler | On the JOB-20 run, promotes every APPROVED version whose valid-from date has arrived, supersedes its predecessor, writes the record and publishes `RulePackageInForce` |
| RollbackService | Service | Moves the pointer to the previous version in one call, marks the rolled-back version ROLLED_BACK, refuses a version with no predecessor with MSG-P3-015, and writes the record |
| RuleRegistryRepository | Repository | The four tables in `rwb_decision`, with the optimistic lock and the unique keys of the migration |
| DecisionLogController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the decision-log read, the scope and the hashes |
| DecisionRecordWriter | Service | The local record and its outbox row in the same transaction as the action (DP-03) |
| ParameterClient, ReferenceDataClient, SessionClient | Clients | The three consumed operations of 12.2, one hop with a 2 s timeout and a breaker |
| PaymentContractFakeAdapter | Test adapter | The rwb-payment contract fake of 12.8, replaced by the contract test of RWB-P8-E2027-CON when it lands |

**Database and migrations**

- Writes `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `decision_log_entry` and the library objects, all in schema `rwb_decision`; reads no other schema.
- One migration in the per-service Flyway sequence of DP-15, `V2027_1__decision_payment_match_governance.sql`, adds the unique key of the version label within a package (`ux_rule_package_version_label`) and the unique key of the row order within a version (`ux_rule_row_version_row_order`), so a repeated label and a duplicate row order are refused by the database as well as by the checks; it adds no column to the four tables and writes no seed row.
- The tables and their baseline are RWB-P7-E2042-APP's; where they have not landed, this story's migration is reconciled with that baseline at the first joint environment (ASM-2295). The PAYMENT_MATCH package row is written on the first load if it is absent, with owner role RW-COE.
- Update a version with `WHERE id = ? AND version = ?`; zero rows updated is MSG-GEN-004 and the action is retried, never applied twice.

**Configuration and reference data**

- `rules.testcases.min` = 50 through the parameters contract of DP-06; the PAYMENT_MATCH Tests tab holds 58 cases, so the check passes with 8 to spare (RWB-P3-E2042-APP AC2).
- The PAYMENT_MATCH version labels, valid-from dates and rows are the legacy values: "PM-2026.12" from 2026-12-01 with EXACT 1, PARTIAL 2, WINDOW 3; "PM-2027.01" from 2027-01-01 with WINDOW at 5 days after; "PM-2027.02" refused. RWB-P3-E2042-APP and RWB-P7-E2042-APP hold the same package under the label "PMT-2026.12" from 2026-12-15 — a conflict recorded in GAP-1292 and GAP-1297, resolved here: one package code holds one version row, PM-2026.12 from 2026-12-01 is the value in force, and PMT-2026.12 from 2026-12-15 is reconciled to it with the owner of RWB-E2-027 before SIT (ASM-2291).
- LOV-DECISION and the version-state list are read through DP-07 with the version in force; no decision code and no state is a constant in code. The decision code of a governance entry is Not specified in the source documents (GAP-1290; ASM-2289).
- The owner role RW-COE and the approver role RW-RISK are rows of the access model, received from the session read and the parameters; the author and the approver must be distinct user references (ASM-2294).
- The checksum and the workbook reference are stored with the version and published on `RulePackageInForce`; a version is never edited in place (BR1, BR2).

**Build steps**

1. `RuleRegistryRepository` and the migration's two unique keys; test that a repeated label and a duplicate row order are refused by the constraint.
2. `WorkbookParser` and `TestCaseRunner` over the Rows and Tests tabs; tests for AC2 and for X7.
3. `RuleCheckPipeline` with the six checks and the dry run, and the refusal in full with MSG-P3-027; tests for AC3, AC4, X1 and X2.
4. `RuleVersionService` with the single transaction and `DecisionRecordWriter`, and the fail-closed behaviour of X4; tests for AC2, TC-E2-027-07 and TC-E2-027-13.
5. `ApprovalService` with the four-eyes rule and the LOADED to APPROVED transition; tests for AC5 and X3.
6. `PromotionService` on the JOB-20 run, with effective dating, the supersede step and the `RulePackageInForce` outbox row; tests for AC6 and X9.
7. `RollbackService` with the one-call rollback, the previous-version pointer and the MSG-P3-015 refusal; tests for AC7 and AC8.
8. `DecisionLogController` and the read of the governance records, with the scope and the hashes; test for AC9.
9. The privacy test: the workbook, the rows, the test cases, the records and the two event payloads hold package codes, version labels, rule IDs, thresholds, dates, amounts and payment codes only, and no name, e-mail address, mobile number, national identity number or account number.

**Feature switch.** The legacy flag `rwb.p3.drools` is kept as the legacy reference and is read in the target as a parameter through DP-06. Off: the load, the approve and the rollback operations answer as unavailable and no version reaches IN_FORCE, while the registry and the decision log stay readable and the version already in force keeps running. The exact answer with the switch off is Not specified in the source documents (GAP-1290; ASM-2289).

**Done when.** The tests in section 16 pass; a SIT environment shows "PM-2026.12" IN_FORCE from 2026-12-01 with 58 of 58 test cases, "PM-2027.02" refused in full with MSG-P3-027, the author's approve refused with MSG-P7-002, "PM-2027.01" promoted at 00:01 with one `RulePackageInForce` event, one rollback that returns "PM-2026.12" to IN_FORCE with the earlier entry still naming "PM-2027.01", and one decision record per action, each returned by the decision-log read.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P3-027 | A load check fails, or no version is in force on the business date | The {table} load was refused: {check}. The version in force is unchanged. | This story, on the load and the version list |
| MSG-P7-002 | The author of a version calls approve | You prepared this decision, so you cannot approve it. | This story, on the approve |
| MSG-P3-015 | A rollback is called for a version with no predecessor | There is no earlier version of {table} to return to. | This story, on the rollback |
| MSG-GEN-001 | An empty workbook, or a missing validFrom, is loaded | Enter {field}. | This story, on the load |
| MSG-GEN-004 | The version label is already loaded, or the version changed at commit | Someone else changed this record. Reload it to see their change. | This story, on the load and the update |
| MSG-P7-003 | The decision record of an action cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every governance action |
| MSG-P4-002 | The role holds no right for the operation, or the version is outside its scope | You cannot {action} here. Your role does not include it. | This story, through the session read |

For MSG-P3-027 the {check} value is compile, schema, overlap, unreachable row, default row, scenario or package in force, and {table} names the rule table or the package code only, never a payment or a person; the row ID, the column and the test-case ID go in the problem detail of 12.1. MSG-P3-027 is copied from Error and Message Standard v4 section 4; the other texts above are copied unchanged from the legacy story and FSD P7 v3 A2.7; the text of MSG-P3-015 is copied from Error and Message Standard v4 section 4. Thai text for each message follows decision DL10. Open decision DL10 is recorded with assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863. Open decision DL24 has no assumption: Not specified in the source documents (DOR-RWB-P7-E2027-APP-18).

### 15. Screens and states

No screen is built in this story. The registry is read through the operations of section 12.1, and SCR-39 Rules and parameters (Epic 8) shows the PAYMENT_MATCH versions with their status, their valid-from date, their test result and their rollback. SCR-40 holds no payment matching table, because the match type and the thresholds are row columns of the package and never reference data (legacy section 15; BR9). The gateway-bff composite route of DP-19 is not extended here.

| Where | State | What the caller sees |
|---|---|---|
| The version list | LOADED | The version, its author, the checksum, the test result and the dry-run counts; not in force |
| The version list | APPROVED | The version and its approver; waiting for its valid-from date |
| The version list | IN_FORCE | The version, its valid-from date and its checksum, and the version it superseded |
| The version list | SUPERSEDED, ROLLED_BACK | The version, the date it stopped being in force and, for a rollback, the reason of the change report |
| The version list | REFUSED, or no row | The refusal with MSG-P3-027 and the check that failed; the version in force is unchanged |
| The decision-log read | Read | The governance record with its inputs reference, rule ID, rule version, actor, final call, decided time and hashes |
| SCR-39 Rules and parameters (Epic 8) | List | The same version list and states; this story feeds the states and the Epic 8 story builds the screen |
| SCR-39 Rules and parameters (Epic 8) | Empty | Not specified in the source documents (CG-ALL-7331) |
| SCR-39 Rules and parameters (Epic 8) | Loading | Not specified in the source documents (CG-ALL-7331) |
| SCR-39 Rules and parameters (Epic 8) | Error | Not specified in the source documents (CG-ALL-7331) |
| SCR-39 Rules and parameters (Epic 8) | No access | Not specified in the source documents (CG-ALL-7331) |
| SCR-40 | Empty | Not specified in the source documents (CG-ALL-7332) |
| SCR-40 | Loading | Not specified in the source documents (CG-ALL-7332) |
| SCR-40 | Error | Not specified in the source documents (CG-ALL-7332) |
| SCR-40 | No access | Not specified in the source documents (CG-ALL-7332) |
| SCR-28 Proceeds matching (P8) | Matched | The rule ID and the package version from the D5 entry of the match; the screen and the match are rwb-payment's |
| SCR-28 Proceeds matching (P8) | Empty | Not specified in the source documents (CG-ALL-7330) |
| SCR-28 Proceeds matching (P8) | Loading | Not specified in the source documents (CG-ALL-7330) |
| SCR-28 Proceeds matching (P8) | Error | Not specified in the source documents (CG-ALL-7330) |
| SCR-28 Proceeds matching (P8) | No access | Not specified in the source documents (CG-ALL-7330) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01 | AC1, BR2, BR6 | Component | PAY-91001 12,500.00; PAYMENT_MATCH version PM-2026.12 |
| TC-E2-027-02 | AC2, BR4 | Component | PAY-91002 11,875.00 |
| TC-E2-027-03 | AC3, BR6 | Contract | PM-2027.01 from 2027-01-01; PAY-91003 4 days late |
| TC-E2-027-04 | AC4, BR3, BR5 | Component | PAY-91004 3 days late, PAY-91005 4 days late |
| TC-E2-027-05 | AC5, BR4, BR5 | Component | PAY-91006 10,000.00 |
| TC-E2-027-06 | AC6, BR7 | Component | PM-2027.02 with duplicate row order and tolerance 120 |
| TC-E2-027-07 | AC7, BR8 | Contract | Decision log stubbed unavailable |
| TC-E2-027-08 | AC8, BR2 | Component | PAY-91007 13,000.00 |
| TC-E2-027-09 | AC9, BR1 | Component | PAY-91008 matched by two rows |
| TC-E2-027-10 | AC10, BR9 (run by RWB-P8-E2027-APP) | Component | No PAYMENT_MATCH version in force on 2027-02-01 |
| TC-E2-027-11 | Access | Contract | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-027-12 | Access | Contract | RW-CASEOWN calls POST /admin/rule-packages/PAYMENT_MATCH/versions; refused with MSG-P4-002 |
| TC-E2-027-13 | Principle 5 | NFR | Decision log write forced to fail for 50 payments; no proceeds row written |
| TC-E2-027-14 | §12.7 tables, boundary | Component | Not specified in the source documents (DOR-RWB-P7-E2027-APP-12) |
| TC-E2-027-15 | AC10, BR8 | Contract | Decision log write forced to fail for PM-2027.01 |
| TC-E2-027-16 | AC11, BR2 | Component | PM-2026.12 loaded again |
| TC-E2-027-17 | AC12, BR2 | Component | Empty workbook; workbook without validFrom |
| TC-E2-027-18 | AC13, Access | Contract | RW-CASEOWN without the Rules and parameters right calls POST /admin/rule-packages/PAYMENT_MATCH/versions; refused with MSG-P4-002 |
| TC-E2-027-19 | AC14, BR10 | Component | No PAYMENT_MATCH version valid on a business date before 2026-12-01 |
| TC-E2-027-20 | AC15, BR11 | Component | Version statuses of PAYMENT_MATCH |
| TC-E2-027-21 | AC16, BR12 | Component | PM-2027.01 LOADED with its rule rows and test cases |
| TC-E2-027-22 | AC17, BR13 | Contract | Decision log entries of PAYMENT_MATCH |
| TC-E2-027-23 | AC18, Access | Contract | Call with no session; rollback of a versionId that does not exist |
| TC-E2-027-24 | AC19, BR8 | Contract | PM-2027.01 loaded again with the same idempotency key |

The Covers column keeps the legacy criterion and rule labels of RWB-E2-027 that the case was written for — the ACn and BRn of the legacy story, not the numbers of sections 7 and 8 of this story — and the Data column keeps the legacy data. Rows TC-E2-027-14 to TC-E2-027-24 are added for this story: they cover AC10 to AC19 and the rules of section 8 of this story, and the boundary of the section 12.7 tables. The P7 copy of each case proves the registry half: the version, its row and its test cases for the ten match cases, the refusal and the four-eyes rule for the invalid-load case, the record write and the read for the record cases, and the rights on the operations of this story for the two access cases. The match itself, the proceeds and the exception list are RWB-P8-E2027-APP's, and the `-ITG` copies of all twenty-four cases belong to RWB-ITG-E2027-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the legacy level System maps to Component or Contract here, Access to Contract and Resilience to NFR.

### 17. Guardrails

- No business value in code: the match type, the row order, the amount tolerance, the window, the grace and the partial floor are columns of the PAYMENT_MATCH rows, and `rules.testcases.min` is a parameter.
- No personal data in logs, events, workflow history, test cases or prompts: the rows, the test cases and the records hold package codes, version labels, rule IDs, thresholds, dates, amounts and payment codes only.
- No read of another service's tables, and no other service reads `rwb_decision` (DP-01): the parameters, the reference lists and the session arrive on their operations, and the payment facts arrive only as the decision entry a match wrote.
- The decision record is written before the action commits; no version exists, no version is approved, promoted or rolled back without its record (BR8).
- One registry, one evaluator: the registry governs and the consuming service evaluates through its embedded Drools kit; this story never evaluates a package for a business decision and never reads a workbook at runtime.
- A version is never edited in place: a change is a new version, and a rollback moves the pointer; the workbook and the DRL are stored write-once with their checksum.
- The version states are the six of BR11 and the check names are the seven of BR3; no other value is written and none is a constant of the code.
- No secret in a workbook, a test case or the run material: the rwb-decision login (DP-02) and the certificate come from the platform secret store, and the test data is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list — governed here by the approved and dated package version that decides the match | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01 to TC-E2-027-24 |

- ADR-017: embedded Drools per service and the rule registry in rwb-decision — Arch v5 slide 27; this story is the registry half for PAYMENT_MATCH.
- D-RCV-36 T3 to T7 and T10: authoring, test, four-eyes approval, effective dating, version audit and the retirement of `payment_match_rule` — inherited through the registry, not rebuilt here.
- D-RCV-60: the realignment that splits RWB-E2-027 into the P7, P8, P3, P4, S2 and ITG stories; the P7 slice is this story.
- RWB-P7-E2042-APP and RWB-P7-E1073-APP: the registry scaffold and the authoring pipeline this story uses and does not rebuild.

### 19. Out of scope

- The match, the proceeds, the posting file, the exception list and JOB-07 (RWB-P8-E2027-APP, P8).
- The PAYMENT_MATCH workbook and its Rows and Tests tabs, the write-once Blob store, the model cache and the checksum-verified swap (RWB-P3-E2042-APP, RWB-P3-E2042-INF, RWB-P3-E1073-APP).
- The session, the roles, the rights and the delegation of authority (RWB-P4-E2027-APP, P4); the installment shortfall on the plan (RWB-S2-E2027-APP, S2).
- The generic registry scaffold of rwb-decision — the four tables' baseline, the shared operation signatures beyond the PAYMENT_MATCH behaviour, and the seeding of the other packages (RWB-P7-E2042-APP; RWB-P7-E1073-APP).
- The other packages of the route set and the remaining 448 routing rules (Epic 3, RWB-P7-E1073-APP; DL24).
- The Epic 8 rules and parameters screen SCR-39 and the administration screens (Epic 8); the proceeds screen SCR-28 (P8).
- The recovery agent that works the exception list (Epic 4) and the reconciliation of the payment against the case balance in policy order (FEAT-PAY-10, Epic 4).
- The real cross-service proof of the load, the approval, the promotion, the rollback and the decision entry across the five services (RWB-ITG-E2027-ITG).
- The retired `payment_match_rule` table and its reference loads (D-RCV-36 T10): this story never creates it and never reads it in any schema; the rows load only through the PAYMENT_MATCH rule package endpoints (GAP-3179).
