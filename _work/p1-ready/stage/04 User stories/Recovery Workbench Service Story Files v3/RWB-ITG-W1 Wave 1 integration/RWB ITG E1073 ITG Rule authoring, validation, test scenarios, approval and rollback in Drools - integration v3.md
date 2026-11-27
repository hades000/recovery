# RWB-ITG-E1073-ITG Rule authoring, validation, test scenarios, approval and rollback in Drools — integration

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The two rwb-source-data job operations are no longer consumed: they list and rerun only rwb-source-data runs and are published by RWB-P1-AD018-CON (RD-P1-012). Findings RWB-ITG-E1073-ITG#1.
- AC2 now proves the JOB-20 run from the `rulePackagePromote` Schedule in rwb-decision. Finding RWB-ITG-E1073-ITG#2.
- The DP-05 row follows the ACE rule: ACE data only through the rwb-source-data contract. Finding RWB-ITG-E1073-ITG#3.
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-073 for the wave-1 integration epic. Rule governance (authoring, the load checks, the 50-scenario gate, four-eyes approval, effective dating and one-call rollback) is central in rwb-decision (P7) while evaluation is local in the one service that owns each model (DP-04), so the Quartz effective-date job becomes the 00:01 Temporal Schedule JOB-20 that publishes EV-30 `rwb.decision.RulePackageInForce.v1`, and the monolith rule-package paths become the `/api/recovery/decision/v1/admin/rule-versions` family. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-ITG-E1073-ITG-L285, X20 RWB-ITG-E1073-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 41 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1073-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-073 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1073-ITG-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E2041-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E1073-ITG-23) |
| Integration dependencies | RWB-P3-E1073-APP, RWB-P7-E1073-APP, RWB-P6-E1073-APP, RWB-P2-E1073-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015, FR-PLT-020) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-012 |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead**, I want **the rule-package life of wave 1 exercised end to end on the real services: rwb-decision authoring a version from the workbook, refusing it whole on any failed check, running at least rules.testcases.min (50) scenarios, taking the four-eyes approval, dating it in force at 00:01 through JOB-20 and publishing EV-30, with each wave-1 service that evaluates the model verifying the checksum and swapping it atomically, and one-call rollback**, so that **a rule change reaches production as tested, approved, dated data with the version stamped on every answer, and a wrong version leaves in one call without a software release**.

### 2. Business rationale

Collection and recovery rules live in procedure documents, and audit found the procedure not followed because the rules were not in the system (CTL-08). RWB-E1-073 carries the control to Drools in the monolith: the workbook is the source of the decision table, the engine compiles it, a scenario set gates the load, Risk signs it, and a rollback takes one call. The measure is that every version in force has a passing scenario set and a checksum, and that a wrong version leaves production in one call.

In the target the story splits along the service boundary. Governance is central in rwb-decision (P7): the registry, the authoring workbook, the compile, schema, overlap, unreachable row, default row and scenario checks, the four-eyes approval, the effective date and the version audit all live there (Arch v5 slide 27; Temporal design slide 15; R-PREC default ruling "rule package registry → P7"). Evaluation is local: each model has exactly one owning service, which holds an approved copy, verifies the checksum and swaps it in atomically, keeping the last good model when a load fails, and runs the rules inside an activity under 300 ms (Arch v5 slide 27; DP-04). JOB-20 became a Temporal Schedule in rwb-decision that promotes at 00:01 and publishes EV-30 on `rwb.decision.events.v1` (Arch v5 slides 43 and 44; Temporal design slide 15), and the consumers are the services that evaluate a package (Arch v5 slide 43 row 30). None of that is proven by a single service story: a version approved by its own author, a load stored after a failed check, a promotion that publishes no event, a service that runs a stale or a half-loaded model, a rollback that no consumer follows and an answer that names no version are failures that only appear across services. This story builds and runs the harness that proves those properties together, on the real services and the real topic, and it provides no operation of its own.

Delivery ownership and capability ownership differ for this legacy story. The story set stays as the split plan gives it, with RWB-E1-073 primary P3 and this integration story one of its parts. The capability owner of the rule registry and its endpoints is P7 rwb-decision, and the capability owner of the embedded Drools kit is PLT.

### 3. Preconditions

- The wave-1 services of this story are deployed in DEV and SIT, each with its own schema and login: `rwb_decision`, `rwb_case`, `rwb_comms` and `rwb_integration` (Arch v5 slide 41, wave 1).
- rwb-decision holds the rule registry of DP-04: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` in `rwb_decision`, with the version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (RWB-P7-E1073-APP; Ownership Map rows rule_package, rule_package_version, rule_row and rule_test_case).
- The four rule-version admin paths are deployed on the rwb-decision base `/api/recovery/decision/v1` by RWB-P7-E1073-APP; the Ownership Map gives them to P7 with the basis ASM-0040, and the legacy paths `/admin/rule-packages/{packageCode}/versions` and `/admin/rule-package-versions/{id}/...` have no target under that name.
- The embedded Drools kit of DP-04 is in the three evaluating services (rwb-case, rwb-comms, rwb-integration), with `EvaluateRules` and `RecordAndApply` on each service's own queue (RWB-PLT-E1072-CON; Temporal design slides 11, 12 and 14).
- The schedule `rulePackagePromote` (JOB-20) is registered on queue `rwb-decision` and can be started once by the harness with the input the cadence uses (RWB-P7-E1073-APP; Arch v5 slide 44).
- The topic `rwb.decision.events.v1` exists with its retry and `.dlt` topics, and each evaluating service has an inbox table `processed_event` in its own schema (RWB-PLT-EVT; DP-03, DP-14).
- rwb-access answers `POST /api/recovery/access/v1/authorise` and holds the test roles RW-COE, RW-RISK, RW-AUDIT and RW-PHONECOL with their Rules and parameters letters (RWB-P4-E1073-APP).
- Package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows in DEV and SIT, and open synthetic cases exist for the dry run, created through the rwb-case path in the DEV data set (RWB-P3-E1073-APP).
- The 50-scenario gate is the platform setting `rules.testcases.min` (50) read through the parameters contract of rwb-case, never a value in the harness code (DP-06; ASM-0555).
- The package code and version label that rwb-comms and rwb-integration each evaluate, the owner and path of the model fetch, and the prefix and path family of the refusal are Not specified in the source documents (GAP-0383; ASM-0555; ASM-0556).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the four integration services and is run when they are in DEV; a fake is never used in their place.

### 4. Flow

1. Pipeline and harness: reads the service list, the package codes, the version labels, the topics and the queue from configuration, and runs the preflight of section 13; a missing registry table, admin path, inbox table, topic, task queue or Schedule stops the run before any test.
2. Harness: uploads the workbook of package ALLOCATION version "ALLOC-2026.12" (26 rows, 50 passing scenarios) with valid from 2026-12-15 as the loader U-41 holding RW-COE, through `POST /api/recovery/decision/v1/admin/rule-versions`, and checks the access letter with the rwb-access authorise call.
3. rwb-decision: parses the Rows and Tests tabs, generates the DRL, compiles it, runs the schema, overlap, unreachable row and default row checks, runs the scenario set against the same evaluator as production, records the SHA-256 checksum of the workbook and the emitted model, and stores the version LOADED with the workbook reference, the DRL, the test result and the dry-run counts; it writes the change-log entry.
4. rwb-decision: on any failed check refuses the load whole and names every failed row, cell or scenario; no version row and no workbook object is written and the version in force does not change.
5. Harness: runs the refusal set of section 5 against the same path — overlap, scenario, schema, unreachable row, default row, compile, an empty file, a repeated version label, a valid from before today — and asserts the code, the message and that the version in force is untouched.
6. Harness: has U-41 call approve on its own version and asserts the refusal, then has the approver U-51 holding RW-RISK approve it; the version becomes APPROVED with the approver and the approval time in the change log.
7. Harness: starts the `rulePackagePromote` Schedule once with the business date 2026-12-15; rwb-decision moves "ALLOC-2026.12" to IN_FORCE and "ALLOC-2026.11" to SUPERSEDED in one transaction and publishes one `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`.
8. Each evaluating service: reads the event once through its inbox, fetches the model, verifies the SHA-256 checksum, and swaps the copy atomically; a failed verification keeps the last good model.
9. Harness: drives a real decision in each evaluating service on a synthetic case, asserts that the answer names the package code, the version and the rule ID, that the evaluation ran inside the activity under 300 ms, and that `RecordAndApply` wrote the version on the decision record in the same transaction as the state change.
10. Harness: has U-41 call rollback once for the version in force with a reason; rwb-decision restores the earlier version in one transaction, marks the replaced version ROLLED_BACK and publishes one event; the evaluating services answer with the restored version after the next event, and a case decided under the rolled-back version keeps that version on its decision record.
11. Harness: asserts that a version in state IN_FORCE has no update path, reconciles the counts — one upload, one version, one approval, one promotion, one event, one swap per service — and writes the run report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two rows match the same case at the same row order | Load refused; both row IDs named | MSG-P3-027 | AC1 |
| X2 | A scenario result differs from the expected result | Load refused; failing scenario IDs named | MSG-P3-027 | AC1 |
| X3 | A required column is missing or a value is outside its list | Load refused; row and column named | MSG-P3-027 | AC1 |
| X4 | A row can never match because an earlier row covers it | Load refused; row named | MSG-P3-027 | AC1 |
| X5 | The allocation package has no default row | Load refused | MSG-P3-027 | AC1 |
| X6 | The approver is the author | Approval refused; the version stays LOADED | MSG-P7-002 | AC2 |
| X7 | Rollback with no earlier version | Refused; the version stays in force | MSG-P3-015 | AC4 |
| X8 | The same package code and version label are loaded twice | Refused with 409 | MSG-GEN-004 | AC1 |
| X9 | Valid from before today | Refused with 422 | MSG-GEN-003 | AC1 |
| X10 | An empty file | Refused with 422 | MSG-GEN-001 | AC6 |
| X11 | A role without Rules and parameters C loads a file | Refused with 403 | MSG-P4-002 | AC7 |
| X12 | The generated DRL does not compile | Load refused; row and cell named; no version row and no workbook object | MSG-P3-027 | AC1 |
| X13 | A scenario of an in-force package fails in the pipeline | The build fails; the merge is blocked | MSG-P3-027 | AC8 |
| X14 | A published version fails the checksum verification in an evaluating service | The service keeps the last good model, answers with it, and the failed load is in the run report | None | AC3 |
| X15 | The promote run finds no approved version whose valid from is reached | No event is published and the version in force does not change | None | AC2 |

X1 to X13 are the exception paths of the legacy story carried onto the real services; X14 is the local-load failure of DP-04 made observable; X15 is the promote run with nothing to promote.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the four integration services, the registry, the topic and the Schedule, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, retry counts and report layout are configuration; the package codes, version labels, message IDs, checks and version states are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: a load refused whole, an approval that needs a second person, a promotion that publishes its event, a checksum-verified atomic swap and a rollback every consumer follows |
| Estimable | One harness project, five test classes, seven fixtures, one Schedule trigger and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a version state, an event, a response code and message, a load duration, a decision record |

### 7. Acceptance criteria

```gherkin
Feature: Rule authoring, validation, scenarios, approval and rollback in Drools, proven across the wave-1 services

  Background:
    Given the environment is DEV with synthetic data
    Given rwb-decision holds the rule registry in schema rwb_decision with queue rwb-decision
    Given the wave-1 evaluating services rwb-case, rwb-comms and rwb-integration run with their own schemas and logins
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given loader test user "U-41" holds RW-COE and approver test user "U-51" holds RW-RISK
    # Test data: rule IDs ALLOC-014, ALLOC-032 and ALLOC-041 appear in no current source document and are marked as test data until RWB-P3-E1073-APP supplies them (CG-ALL-456, CG-ALL-457, CG-ALL-458)

  Scenario: AC1 The upload, the checks and the 50-scenario gate refuse a bad version whole (new, D-RCV-60)
    Given a workbook for package ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 scenarios that pass every check
    When U-41 uploads it to POST /api/recovery/decision/v1/admin/rule-versions with valid from 2026-12-15
    Then version "ALLOC-2026.12" is stored LOADED with the workbook reference, the generated DRL and the SHA-256 checksum
    Then the version carries the test result "50 of 50 scenarios passed" and the dry-run counts of the open cases whose result would change, by product, queue and rule
    When rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12
    Then the load is refused with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032"
    When scenarios "TA-07" and "TA-19" return "MTG-CEN-CO" where "MTG-BKK-CO" is expected
    Then the load is refused with MSG-P3-027 for the scenario check naming "TA-07" and "TA-19"
    When row 9 carries the value "QUICK" that is not in its list, row "ALLOC-041" can never match, the allocation rows have no default row, and a cell at row 14 has a condition with no value
    Then the load is refused with MSG-P3-027 for the schema, unreachable row, default row and compile checks, naming each row and cell
    Then in every one of those refusals no version row and no workbook object is written, and version "ALLOC-2026.11" stays in force
    When a workbook with version label "ALLOC-2026.12" for package ALLOCATION is uploaded again
    Then the call is refused with 409 and MSG-GEN-004
    When U-41 uploads version "ALLOC-2026.14" with valid from 2026-11-01 on 2026-12-10
    Then the call is refused with 422 and MSG-GEN-003 for valid from

  Scenario: AC2 Four-eyes approval and effective dating promote the version at 00:01 and publish RulePackageInForce (new, D-RCV-60)
    Given version "ALLOC-2026.12" of package ALLOCATION is LOADED and U-41 is its author
    When U-41 calls POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then the call is refused with MSG-P7-002 and the version stays LOADED
    When U-51 calls the same path
    Then the version is APPROVED with approver U-51 and the approval time in the change log
    When the rulePackagePromote Schedule runs as JOB-20 at 00:01 on 2026-12-15 on queue rwb-decision
    Then "ALLOC-2026.12" is IN_FORCE and "ALLOC-2026.11" is SUPERSEDED in one transaction
    Then exactly one event rwb.decision.RulePackageInForce.v1 is on rwb.decision.events.v1, naming package ALLOCATION, version "ALLOC-2026.12", its SHA-256 checksum and valid from 2026-12-15
    Then the promote run is an action of the Schedule rulePackagePromote on queue rwb-decision, read through the Temporal client, and the harness calls no job operation of rwb-source-data
    When the promote run runs again with no approved version whose valid from is reached
    Then no second event is published and the version in force does not change

  Scenario: AC3 Each evaluating service verifies the checksum and swaps the model atomically, keeping the last good model (new, D-RCV-60)
    Given rwb-decision has published RulePackageInForce for package ALLOCATION version "ALLOC-2026.12"
    Then each of the three evaluating services reads the event once through its inbox processed_event and fetches the model
    Then each service verifies the SHA-256 checksum before it swaps the copy in
    Then the swap is atomic: an answer at the moment of the swap names "ALLOC-2026.12" or "ALLOC-2026.11", never a partially loaded model
    When the same event is delivered a second time
    Then nothing is loaded twice and every answer still names exactly one version
    When a published version fails the checksum verification in rwb-case
    Then rwb-case keeps the last good model "ALLOC-2026.11", answers with it, and the failed load appears in the run report
    Then the model fetch path and its owner are Not specified in the source documents (GAP-0383; ASM-0556)

  Scenario: AC4 One call at rwb-decision rolls back and the evaluating services follow on the next RulePackageInForce (new, D-RCV-60)
    Given version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it
    When U-41 calls POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback once with a reason
    Then "ALLOC-2026.12" is in force again in one transaction and version 7 is ROLLED_BACK with the reason, U-41, the time and the checksum in the change log
    Then exactly one RulePackageInForce names the restored version
    Then each evaluating service answers with "ALLOC-2026.12" after that event and no service uses "ALLOC-2026.13" on a new decision
    Then a case decided under version 7 keeps rule version "ALLOC-2026.13" on its decision record
    When rollback is called for package TRANSFER version "TRF-2026.11", which has no earlier version
    Then the call is refused with MSG-P3-015 and "TRF-2026.11" stays in force
    Then a version in state IN_FORCE is never edited: no update path exists for it on the registry or through the model fetch

  Scenario: AC5 Evaluation stays local to the owning service, inside an activity and under 300 ms, and every answer names the version (new, D-RCV-60)
    Given package ALLOCATION version "ALLOC-2026.12" is in force in the three evaluating services
    When a case reaches allocation in rwb-case and the workflow asks for the answer
    Then the evaluation runs in the EvaluateRules activity on queue rwb-case and no call goes to a shared rule server
    Then the answer names package ALLOCATION, version "ALLOC-2026.12", rule ID "ALLOC-014" and its outputs, and RecordAndApply writes that version on the decision record in the same transaction as the state change
    Then 200 fixture evaluations each complete inside the 300 ms activity budget
    Then a version is never recompiled per call and the model cache holds at most the configured number of versions (20, as recorded in RWB-E1-073)
    When the same package is evaluated in rwb-comms and in rwb-integration
    Then each service evaluates the copy it holds in its own schema and no service reads another service's rule tables

  Scenario: AC6 An empty workbook is refused with 422 and MSG-GEN-001 and no version is stored (new, D-RCV-60)
    When U-41 uploads a workbook with no rows for package ALLOCATION to POST /api/recovery/decision/v1/admin/rule-versions
    Then the call is refused with 422 and MSG-GEN-001
    Then no version row and no workbook object is written and version "ALLOC-2026.11" stays in force

  Scenario: AC7 A role without Rules and parameters C is refused when it loads a file (new, D-RCV-60)
    When RW-CASEOWN loads a file to POST /api/recovery/decision/v1/admin/rule-versions
    Then the call is refused with 403 and MSG-P4-002
    Then no version row and no workbook object is written

  Scenario: AC8 A scenario of an in-force package that fails in the pipeline blocks the merge (new, D-RCV-60)
    When a scenario of the in-force package ALLOCATION fails in the pipeline
    Then the build fails and the merge is blocked with MSG-P3-027
    Then version "ALLOC-2026.11" stays in force

  Scenario: AC9 A retried or timed-out EvaluateRules activity gives one answer that names the version (new, D-RCV-60)
    Given package ALLOCATION version "ALLOC-2026.12" is in force in rwb-case
    When a case reaches allocation in rwb-case and the EvaluateRules activity times out
    Then the workflow retries the activity and the retried answer names package ALLOCATION and version "ALLOC-2026.12"
    Then RecordAndApply writes that version on the decision record once, in the same transaction as the state change
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version passes the Drools compile, schema, overlap, unreachable row, default row and scenario checks before it is stored, and the dry run is recorded for the approver | REQ-CWC-014; D-RCV-36 T4 |
| BR2 | A load with any failed check is refused in full: no version row, no workbook object, and the version in force does not change | Reference data change process, step 3; CTL-08 |
| BR3 | First match: RuleSet = package code, each row is one rule with NAME = rule ID, rows share one activation-group, salience comes from row order and the default row is last; exactly one row decides | D-RCV-36 T5 |
| BR4 | The allocation package always has a default row | REQ-CWC-008 |
| BR5 | A version takes effect on its valid from date after approval; open cases keep the version they were decided under | R-UNI-38 |
| BR6 | The author cannot approve; RW-RISK signs rule package changes | Separation of duty table; CTL-08 |
| BR7 | Rollback returns the previous version in one call and one transaction, and the version it replaces is ROLLED_BACK with its reason | REQ-CWC-013; FEAT-CWC-15 |
| BR8 | Every load, approval, promotion and rollback is in the change log with author, approver, time, checksum and test result | REQ-CWC-013; FSD A2.14 |
| BR9 | The template is the Drools XLS decision-table format, one workbook per package with Rows and Tests tabs; the generated DRL and the workbook are stored with the version, and the version label is a cell in the workbook | D-RCV-36 T3, T4 |
| BR10 | A load carries at least rules.testcases.min scenarios (50, an assumed value; the parameter catalogue that holds it is Not specified in the source documents (GAP-2460)) from the Tests tab, every scenario runs through the same RuleEvaluator as production, and the stored checksum is the SHA-256 of the workbook and of the emitted model | REQ-CWC-014; D-RCV-36 T4 |
| BR11 | Every in-force package's scenarios run in every build through RuleScenarioBuildGate, and a failing scenario fails the build | D-RCV-36 T4; REQ-CWC-014 |
| BR12 | Governance is central in rwb-decision (authoring, checks, approval, effective dating, version audit) and evaluation is local in the one service that owns each model, inside an activity and under 300 ms; there is no shared rule server on the hot path | Arch v5 slide 27; Temporal design slide 15; DP-04 |
| BR13 | On RulePackageInForce each evaluating service fetches the model, verifies the checksum and swaps it atomically, keeping the last good model when a load fails, and a model is never recompiled per call | Arch v5 slide 27; Temporal design slides 11 and 15; DP-04 |
| BR14 | JOB-20 is a Temporal Schedule in rwb-decision that promotes at 00:01 and publishes exactly one `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` per promoted version | Arch v5 slides 43 and 44 (JOB-20); Temporal design slide 15 |
| BR15 | A version in state IN_FORCE is never edited; a change is a new version, and rollback moves the pointer and writes the reason | RWB-E1-073 section 17; R-UNI-38 |

### 9. State transitions

None for a case status. This story changes no case status of its own; it asserts the states below across the services.

| From | Event | Condition | To |
|---|---|---|---|
| None | Upload through the admin path | Every check passes | LOADED |
| None | Upload through the admin path | Any check fails, including the compile, the scenario set, a repeated version label or a valid from before today | REFUSED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | Promote at 00:01 (JOB-20) | Valid from reached | IN_FORCE; the previous version SUPERSEDED |
| IN_FORCE | Rollback | An earlier version exists and a reason is given | ROLLED_BACK; the earlier version IN_FORCE again |
| IN_FORCE | Rollback | No earlier version | Unchanged; refused with MSG-P3-015 |

The local copy and the run states the harness observes:

| Item | States |
|---|---|
| Local model copy (each evaluating service) | Not loaded; verified and in use; replaced on the next RulePackageInForce; last good model kept after a failed verification |
| Evaluation | Answered by the version in force at the moment of the activity; the answer names the package code and the version |
| Promote run | Started at 00:01, completed with one event per promoted version, or completed with nothing to promote and no event |
| Harness run | Not started, running, passed, failed with the failing criterion named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the Schedule trigger and the run report |
| rwb-decision owner (RWB-P7-E1073-APP) | Owns the registry, the checks, the approval, the effective date, the promote run, the rollback and the model fetch |
| rwb-case owner (RWB-P3-E1073-APP) | Owns the ALLOCATION evaluation, the local copy and its two activities |
| rwb-comms owner (RWB-P6-E1073-APP) and rwb-integration owner (RWB-P2-E1073-APP) | Own the local copy and the evaluation of the package each service is assigned |
| rwb-access owner (RWB-P4-E1073-APP) | Owns the Rules and parameters right check and its refusal |
| RW-COE | Loads a package version and calls rollback (Rules and parameters CRUD) |
| RW-RISK | Approves a version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT | Reads versions, scenarios, dry-run counts and the change log (Rules and parameters R) |
| RW-REFADM | Prepares load files; may not approve |
| SY-RULES | Evaluates the draft and the version in force for scenarios, the dry run and production |
| SY-CASEWF | Applies the approved decision; no admin right |
| RW-TRIBE | Builds and runs RuleScenarioBuildGate; no production data in the build |
| No role | May edit a version in state IN_FORCE, approve its own version, or read a version without Rules and parameters R |
| No delegation of authority level applies | A rule package version is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 to DF-REF-278 | `rule_package` (rwb_decision) | all fields | Read |
| DF-REF-279 | `rule_package_version` (rwb_decision) | id | Read |
| DF-REF-280 | `rule_package_version` (rwb_decision) | package_id | Read |
| DF-REF-281 | `rule_package_version` (rwb_decision) | version_label | Read |
| DF-REF-282 | `rule_package_version` (rwb_decision) | status | Read |
| DF-REF-283 | `rule_package_version` (rwb_decision) | source_blob_ref | Read |
| DF-REF-284 | `rule_package_version` (rwb_decision) | drl_source | Read |
| DF-REF-285 | `rule_package_version` (rwb_decision) | checksum | Read |
| DF-REF-286, DF-REF-287 | `rule_package_version` (rwb_decision) | valid_from, valid_to | Read |
| DF-REF-288 | `rule_package_version` (rwb_decision) | author | Read |
| DF-REF-289 | `rule_package_version` (rwb_decision) | approver | Read |
| DF-REF-290, DF-REF-291 | `rule_package_version` (rwb_decision) | loaded_at, approved_at | Read |
| DF-REF-292 | `rule_package_version` (rwb_decision) | test_result | Read |
| DF-REF-293 | `rule_package_version` (rwb_decision) | dry_run_counts | Read |
| DF-REF-294 | `rule_package_version` (rwb_decision) | rollback_of | Read |
| DF-REF-296 to DF-REF-298 | `rule_row` (rwb_decision) | package_version_id, drools_rule_name, outputs | Read |
| DF-REF-001 to DF-REF-015 | `rule_row` (rwb_decision) | all rule fields | Read |
| DF-REF-052 to DF-REF-054 | `rule_row` (rwb_decision) | rule_table, row_order, target_queue_code | Read |
| DF-REF-185 to DF-REF-197 | `rule_test_case` (rwb_decision) | all fields | Read |
| DF-REF-299 | `rule_test_case` (rwb_decision) | package_version_id | Read |
| DF-CAS-003 | `recovery_case` (rwb_case, through the case contract) | product_group | Read |
| DF-CAS-010 | `recovery_case` (rwb_case, through the case contract) | queue_id | Read |
| DF-CAS-012 | `recovery_case` (rwb_case, through the case contract) | region_code | Read |
| DF-CAS-015 | `recovery_case` (rwb_case, through the case contract) | exposure_band | Read |
| DF-CAS-019 | `recovery_case` (rwb_case, through the case contract) | deviation_open | Read |
| Not specified in the source documents (DOR-RWB-ITG-E1073-ITG-7) | `processed_event` (each evaluating service schema) | CloudEvents id, consumer group, processed at | Read |
| Not specified in the source documents (DOR-RWB-ITG-E1073-ITG-7) | decision record (each evaluating service schema) | rule ID, rule version, answer | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-073. The registry tables belong to rwb_decision (Ownership Map, P7 under ASM-0069; OQ-P7-04 stays open until the P7 technical specification carries them); the harness owns no table, writes nothing directly and reads the registry only through the admin paths. The case fields of the dry run are read by rwb-decision through the rwb-case contract, never from `rwb_case` directly (DP-01, DP-05). The package code each of rwb-comms and rwb-integration evaluates is Not specified in the source documents (GAP-0383; ASM-0556).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation. Every path in this section is owned by another service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-versions` | P7 rwb-decision (Ownership Map, basis ASM-0040) | Lists versions of a package with state, valid from, author, approver, checksum, test result and dry-run counts |
| POST | `/api/recovery/decision/v1/admin/rule-versions` | P7 rwb-decision (ASM-0040) | Uploads the workbook with the valid from and returns the version LOADED with its checks, test result and dry-run counts |
| POST | `/api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` | P7 rwb-decision (ASM-0040) | Four-eyes approval; refuses when the approver is the author |
| POST | `/api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback` | P7 rwb-decision (ASM-0040) | One-call rollback with a reason; restores the earlier version |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision (path named on Arch v5 slide 27; not in the Ownership Map or API Specification v5, GAP-0383; ASM-0556) | Fetches the model of a package version for an evaluating service, with its checksum |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Rules and parameters right check for the loader, the approver and the refusal |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service. The promote run is started through the Temporal client on queue `rwb-decision`, not through a REST path. JOB-20 is a job of rwb-decision, so no job operation of rwb-source-data is called: `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` of rwb-source-data list and rerun only rwb-source-data runs (RD-P1-012). The legacy paths `/admin/rule-packages/{packageCode}/versions`, `/admin/rule-package-versions/{id}/approve`, `/admin/rule-package-versions/{id}/rollback` and the separate dry-run read have no target under those names: the dry-run counts ride on the version representation of the two rwb-decision reads above.

#### 12.3 Events published

None. The harness publishes no business event. The one event asserted in this story is produced by rwb-decision and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | Produced by P7 rwb-decision at the 00:01 promote run (JOB-20); consumed by the evaluating services, which in this story are P3 rwb-case, P6 rwb-comms and P2 rwb-integration; observed by the harness | CloudEvents 1.0 binary mode, exactly one event per promoted version, inbox dedupe in `processed_event`, retry 1 min, 10 min, 1 h then `.dlt` |

Arch v5 slide 43 row 30 names rwb-case, rwb-valuation, rwb-treatment and rwb-payment as the consumers; of those, rwb-case is wave 1, and rwb-comms and rwb-integration are the other two wave-1 services this story exercises as evaluators (I list). The event payload and the message prefix of the refusal are Not specified in the source documents (GAP-0383; ASM-0556); under that assumption the event carries the package code, the version label, the SHA-256 checksum and the valid from, and nothing else.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| Promote run started by the `rulePackagePromote` Schedule | Run | `rwb-decision` | Input the business date; output the promoted package code, the version label and the event id of the one `rwb.decision.RulePackageInForce.v1` it published. The workflow and activity names inside rwb-decision are owned by RWB-P7-E1073-APP |
| `EvaluateRules` | Activity | `rwb-case`, `rwb-comms`, `rwb-integration` | Input packageCode, facts and onDate; output `RuleResult` (packageCode, packageVersion, ruleId, outputs); Drools is called inside the activity and never in workflow code (Temporal design slides 12 and 14) |
| `RecordAndApply` | Activity | `rwb-case`, `rwb-comms`, `rwb-integration` | Writes the decision record with the rule ID and the version, the state change and the outbox row in one transaction in the service's own schema (Temporal design slide 14) |

The harness drives these and asserts their output; it registers no workflow and no activity of its own.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| `rulePackagePromote` | Daily at 00:01, overlap policy SKIP, catch-up window | Registered by the rwb-decision release (RWB-P7-E1073-APP); started once by the harness through the Temporal client with the same input the cadence uses | JOB-20 Rule promote (Arch v5 slide 44; Temporal design slide 15) |

#### 12.7 Tables owned

None. The harness owns no table. The registry tables it exercises belong to rwb_decision, and the decision record, the inbox and the local model copy belong to each evaluating service schema; section 11 lists them with their owners.

#### 12.8 Contract fakes

None. This is the integration level: the real registry, the real topic, the real Schedule and the real evaluating services replace the contract fakes of the app stories.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6 | Four rule-version admin paths and the model fetch on rwb-decision and the authorise call on rwb-access; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 1 event type | `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`, one per promoted version, deduped in each consumer's inbox |
| Temporal | None | 1 Schedule, 2 activities | `rulePackagePromote` at 00:01 on `rwb-decision`; `EvaluateRules` and `RecordAndApply` on each evaluating service's queue |
| File | None | None | The workbook travels as the multipart body of the upload call, not as a File call type |

### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/rule-governance`, with the five test classes `RuleLoadChecksIT`, `ApprovalAndPromotionIT`, `ModelSwapIT`, `RollbackIT` and `LocalEvaluationIT`, the fixture workbooks and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| WorkbookFixture | Service | Builds the 26-row, 50-scenario workbook and the refusal workbooks deterministically, with the row IDs, the version label and the expected SHA-256 |
| VersionProbe | Service | Calls the four admin paths and asserts the state, the author, the approver, the checksum, the test result and the dry-run counts |
| EventProbe | Service | Subscribes to `rwb.decision.events.v1` and asserts exactly one `RulePackageInForce` per promotion, its fields and the absence of an event on a promotion with nothing to promote |
| ModelProbe | Service | Reads the model each evaluating service holds and asserts the checksum, the swapped version and the last good model after a failed verification |
| EvaluationProbe | Service | Drives one decision per evaluating service, reads the `EvaluateRules` answer and the decision record, and times the activity against the 300 ms budget |
| RollbackDriver | Service | Calls rollback once with a reason, then asserts the restored version, the ROLLED_BACK state, the event and the answer of each evaluating service |
| RefusalProbe | Service | Runs the refusal set of section 5 and asserts the code, the message and the unchanged version in force |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The harness writes nothing to any schema; `rule_package_version` and the local model copy are written by the owning services through their own paths, and the harness reads them through the contracts.

**Configuration and reference data**

- The service list, the package codes, the version labels "ALLOC-2026.11", "ALLOC-2026.12", "ALLOC-2026.13" and "TRF-2026.11", the topics and the queue, all as configuration.
- The valid from dates 2026-12-15 and 2026-12-10, the 26 rows, the 50 scenarios and the scenario IDs "TA-07" and "TA-19", as fixture data.
- `rules.testcases.min` = 50 and the model cache size 20, read through the parameters contract of rwb-case (DP-06).
- The test roles RW-COE, RW-RISK, RW-AUDIT and RW-PHONECOL with their Rules and parameters letters, from rwb-access.
- The scratch business date for the promote run, the 300 ms activity budget and the 2 s client budget.

**Pattern application**

Every pattern in "Patterns applied" is listed below with the legacy marker, the microservice pattern and the dependency the DP table adds. DP-05 and DP-07 apply through the dry run, the parameters and the reference-data reads of the load checks; DP-19 applies to the Epic 8 admin screen, and the harness renders nothing, calling the services directly.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C Not specified in the source documents (CG-ALL-455) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract only; only rwb-source-data reads `recovery.v_ace_*` (D-RCV-60) and this story reads no ACE data | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C and X dependencies the DPs name stay with the service, platform and operations stories this harness proves; this story carries no H, C or X dependency and its I list names the four services whose behaviour it exercises (Template and Rules §R5.4: I never blocks a build).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Workbook ALLOC-2026.12 | 26 rows, 50 passing scenarios, valid from 2026-12-15, one SHA-256 checksum | AC1, AC2, TC-E1-073-01-ITG |
| Overlap pair | Rows "ALLOC-031" and "ALLOC-032" at row order 12, same product group and region | AC1, TC-E1-073-02-ITG |
| Failing scenarios | "TA-07" and "TA-19" returning "MTG-CEN-CO" for the expected "MTG-BKK-CO" | AC1, TC-E1-073-03-ITG |
| Version chain | Versions 6 and 7, "ALLOC-2026.12" and "ALLOC-2026.13", and package TRANSFER with "TRF-2026.11" only | AC2, AC4, TC-E1-073-04-ITG, TC-E1-073-09-ITG |
| Bad cells and rows | Row 9 value "QUICK", the "ALLOC-040" and "ALLOC-041" pair, no default row, and a condition cell with no value at row 14 | AC1, TC-E1-073-05-ITG to TC-E1-073-07-ITG, TC-E1-073-13-ITG |
| Corrupt model | A published version whose object does not match its stored checksum | AC3, TC-ITG-E1073-03 |
| Role set | U-41 RW-COE, U-51 RW-RISK, U-6104 RW-PHONECOL with Rules and parameters "-" | AC1, AC2, TC-E1-073-16-ITG to TC-E1-073-20-ITG |

**Run order.** Preflight; the upload and the whole refusal set (AC1); the author refusal, the approval and the 00:01 promotion (AC2); the three swaps, the repeated delivery and the corrupt model (AC3); the rollback and the following event (AC4); the timed local evaluations (AC5); cleanup of the DEV fixtures, with the version in force left as it was at the start. A failing step stops the run and the report names the criterion, the service and the evidence.

**Done when.** The 25 test cases of section 16 pass on the real services in DEV and SIT, ALLOCATION loads with 26 rows and 50 scenarios, is approved by a second person, takes effect at 00:01 with exactly one event, is evaluated by the three services under 300 ms with the version on every answer, rolls back in one call and is followed by every evaluator, and every refusal of section 5 leaves the version in force untouched.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A reference data or rule version load fails a check (schema, valid from in the past, duplicate key, removed product with open cases, overlap, unreachable or default row, test cases), or no version is in force for a table an engine needs (RWB-E1-073, RWB-E1-043, RWB-E1-025) | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Empty file or no rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version label already loaded, or version not LOADED | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The seven texts are copied unchanged from RWB-E1-073, except MSG-P3-027, which is copied from Error and Message Standard v4; the story adds no message text. For MSG-P3-027 the {table} value is the package code and the {check} value is compile, schema, overlap, unreachable row, default row or scenario; a failed check is identified by row IDs, cells or scenario IDs only, never by a case fact or a person. For MSG-P3-015 the {table} value is the package code. The refusing service in the target is rwb-decision (P7) while the refusal keeps the legacy identifier MSG-P3-027; the message prefix and the path family of the refusal are Not specified in the source documents (GAP-0383; ASM-0556). Report lines of the harness are for developers and are not part of the message standard.

### 15. Screens and states

No screen in this story, and the harness renders nothing: the admin paths are called directly and are the only authoring surface it uses. SCR-39 Rules and parameters and the rule package administration screen (Epic 8, FEAT-ADM-02) are out of scope here, and so is the rule change audit report of RWB-E2-041. The stories that serve the rule version list define its states, and the harness renders and tests none of them:

| Screen | State | What it shows |
|---|---|---|
| SCR-39 Rules and parameters | Loading | The version list state Loading (RWB-P7-E1073-APP) |
| SCR-39 Rules and parameters | Empty | "No versions of this package." (RWB-P7-E1073-APP) |
| SCR-39 Rules and parameters | Error | The problem text (RWB-P7-E1073-APP) |
| SCR-39 Rules and parameters | No access | A role without Rules and parameters R may not read a version (section 10) |

The version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, the local copy states and the promote and run states of section 9 are the states the harness observes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-073-16-ITG | legacy access (X11), BR6 | Integration | RW-CASEOWN calls POST `/admin/rule-versions` for ALLOCATION; refused with MSG-P4-002 |
| TC-E1-073-20-ITG | legacy access (X11) | Integration | A role without Rules and parameters R reads the dry-run counts of version 7; refused with MSG-P4-002 |
| TC-E1-073-01-ITG | legacy AC1, BR1, BR5, BR8 | Integration | ALLOCATION version with 26 rows, 50 passing scenarios and a checksum |
| TC-E1-073-02-ITG | legacy AC2, BR3 | Integration | Rows ALLOC-031 and ALLOC-032 at row order 12 |
| TC-E1-073-03-ITG | legacy AC3, BR1, BR10 | Integration | Scenarios TA-07 and TA-19 failing |
| TC-E1-073-04-ITG | legacy AC4, BR5, BR7 | Integration | Versions 6 and 7 |
| TC-E1-073-05-ITG | legacy AC5, BR1 | Integration | Row 9 with value QUICK |
| TC-E1-073-06-ITG | legacy AC6, BR1 | Integration; run by RWB-P3-E1073-APP | Rows ALLOC-040 and ALLOC-041 |
| TC-E1-073-07-ITG | legacy AC7, BR4 | Integration; run by RWB-P3-E1073-APP | No default row |
| TC-E1-073-08-ITG | legacy AC8, BR6 | Integration; run by RWB-P3-E1073-APP | Load and approval by U-41 |
| TC-E1-073-09-ITG | legacy AC9, BR7 | Integration; run by RWB-P3-E1073-APP | TRANSFER with one version |
| TC-E1-073-10-ITG | legacy AC10 | Integration; run by RWB-P3-E1073-APP | Label ALLOC-2026.12 twice |
| TC-E1-073-11-ITG | legacy AC11 | Integration; run by RWB-P3-E1073-APP | Valid from 2026-11-01 |
| TC-E1-073-12-ITG | legacy AC12 | Integration; run by RWB-P3-E1073-APP | Template with no rows |
| TC-E1-073-13-ITG | legacy AC13, BR1, BR9 | Integration; run by RWB-P3-E1073-APP | Condition cell exposure_band >= with no value at row 14 |
| TC-E1-073-14-ITG | legacy AC14, BR11 | Integration; run by RWB-P3-E1073-APP | Fact mapping changed so TA-07 returns MTG-CEN-CO |
| TC-E1-073-15-ITG | legacy AC15, BR8, BR9 | Integration; run by RWB-P3-E1073-APP | Workbook ALLOCATION-2026.12.xlsx and its SHA-256 |
| TC-E1-073-17-ITG | legacy access (X11) | Integration | RW-CASEOWN calls GET `/admin/rule-versions`; refused with MSG-P4-002 |
| TC-E1-073-18-ITG | legacy access (X11), BR6 | Integration | RW-COE calls approve without Rules and parameters A; refused with MSG-P4-002 |
| TC-E1-073-19-ITG | legacy access (X11), BR7 | Integration | RW-RISK calls rollback without Rules and parameters U; refused with MSG-P4-002 |
| TC-ITG-E1073-01 | AC1, BR1, BR2, BR9 | Integration | The 26-row 50-scenario workbook and the eight refusals of section 5, each leaving the version in force untouched |
| TC-ITG-E1073-02 | AC2, BR5, BR6, BR14 | End to end | A LOADED version, the author's approve call, the approver's approve call, the 00:01 promote run and an empty promote run |
| TC-ITG-E1073-03 | AC3, BR10, BR13 | Integration | One publication, three evaluators, one repeated delivery and one model whose checksum does not match |
| TC-ITG-E1073-04 | AC4, BR7, BR8, BR15 | End to end | Versions 6 and 7 in force in turn, one rollback, one event and the answer of each evaluator |
| TC-ITG-E1073-05 | AC5, BR3, BR12, BR13 | Component | ALLOCATION facts MORTGAGE and BKK; 200 evaluations timed against the 300 ms budget |
| TC-ITG-E1073-06 | Section 12 contract | Contract | Each admin path, the rwb.decision.RulePackageInForce.v1 event and the EvaluateRules and RecordAndApply activities checked against their section 12 contract |
| TC-ITG-E1073-07 | AC6, X10 | Integration | Workbook with no rows for ALLOCATION to POST `/admin/rule-versions`; refused with 422 and MSG-GEN-001 |
| TC-ITG-E1073-08 | AC7, X11 | Integration | RW-CASEOWN loads a file to POST `/admin/rule-versions`; refused with 403 and MSG-P4-002 |
| TC-ITG-E1073-09 | AC8, X13, BR11 | Integration | A scenario of the in-force package ALLOCATION fails in the pipeline; the merge is blocked with MSG-P3-027 |
| TC-ITG-E1073-10 | AC9 | Integration | The EvaluateRules activity of a case in rwb-case times out and is retried; one answer and one decision record write for ALLOC-2026.12 |

AC2 gained a Then in version 3 (the Schedule action read through the Temporal client). Test Cases v9: TC-E1-073-02-ITG, TC-ITG-E1073-02.

The legacy acceptance criteria of RWB-E1-073 are owned by RWB-P3-E1073-APP (AC1 to AC15); RWB-P7-E1073-APP, RWB-P6-E1073-APP and RWB-P2-E1073-APP own no legacy criterion of this key and carry only the contract, load or evaluation parts of sections 12 and 13, so a legacy copy names them as `legacy ACn, BRm` in the Covers column: the numbers belong to the owning APP story, not to this one. The legacy test case IDs are kept as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC5 carry TC-ITG-E1073-01 to TC-ITG-E1073-05. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID for the legacy copies.

### 17. Guardrails

- No business value in code: rows, conditions, target queues, scenarios, package codes, version labels, the test count and the cache size are data, read through the parameters and reference-data contracts (DP-06, DP-07).
- No personal data in events, workflow inputs, logs, fixtures or the report: package codes, version labels, row IDs, scenario IDs, rule IDs, codes and hashes only; scenarios use synthetic case facts and the dry run reports counts.
- Each service writes only its own schema and reads no other service's tables (DP-01); the harness writes nothing and reads the registry only through the admin paths, and the dry run reads case fields through the rwb-case contract.
- One evaluator serves the load checks, the scenarios, the dry run and production; no check uses a second engine.
- The approver is never the author; the service checks it, not only the screen (BR6).
- A version in state IN_FORCE is never edited: a change is a new version, and rollback moves the pointer and writes the reason (BR15); the harness asserts the absence of an update path instead of relying on the review.
- Evaluation stays inside the activity and never in workflow code, so a replay reuses the recorded answer; the model name and version are written on the decision record (BR12, BR13).
- One topic and one event type carry the promotion (BR14); a service that publishes its own promotion event on its own topic fails the run.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or production and never writes a live database. The harness never uses production data and never points at a production namespace.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | The four rwb-decision admin paths, the version states, `rulePackagePromote`, MSG-P3-015 | TC-E1-073-01-ITG, TC-E1-073-04-ITG, TC-E1-073-08-ITG, TC-E1-073-09-ITG, TC-E1-073-10-ITG, TC-E1-073-11-ITG, TC-E1-073-15-ITG, TC-ITG-E1073-02, TC-ITG-E1073-04 |
| REQ-CWC-014 | Schema, overlap, unreachable, default, compile and scenario checks | The upload check set, `rules.testcases.min`, MSG-P3-027, RuleScenarioBuildGate | TC-E1-073-02-ITG, TC-E1-073-03-ITG, TC-E1-073-05-ITG, TC-E1-073-06-ITG, TC-E1-073-07-ITG, TC-E1-073-12-ITG, TC-E1-073-13-ITG, TC-E1-073-14-ITG, TC-ITG-E1073-01 |
| REQ-DRI-004 | Epic 1 records for case creation, assignment and transfer use versioned rules | `rwb.decision.RulePackageInForce.v1`, the local model copy, `EvaluateRules`, `RecordAndApply` | TC-E1-073-01-ITG, TC-E1-073-04-ITG, TC-E1-073-15-ITG, TC-ITG-E1073-02, TC-ITG-E1073-03, TC-ITG-E1073-05 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | The default row check, rule ID "ALLOC-014", the first-match semantics of `EvaluateRules` | TC-E1-073-07-ITG, TC-ITG-E1073-05 |

### 19. Out of scope

- The registry, the authoring checks, the approval and effective-date logic, the promote run, the rollback and the model fetch (RWB-P7-E1073-APP).
- The rule package contract published to the evaluating services and the AsyncAPI document of `rwb.decision.events.v1` (the contract story of the wave; this harness uses the real services and no fake).
- The registry schema, the Flyway sequence and the grants (RWB-P7-E1073-APP with the per-service DB stories).
- The ALLOCATION evaluation and the local copy in rwb-case (RWB-P3-E1073-APP), in rwb-comms (RWB-P6-E1073-APP) and in rwb-integration (RWB-P2-E1073-APP).
- The Rules and parameters right model and its refusal (RWB-P4-E1073-APP); this story exercises the refusal and owns none of it.
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (RWB-E2-042).
- The decision log store, the hash chain and the 02:00 chain check (RWB-ITG-E1008-ITG, RWB-TE-008).
- The change checklist and the rule change audit report (RWB-E2-041).
- The rule package administration screen SCR-39 and the admin screen of Epic 8 (FEAT-ADM-02).
- Loading the other 448 routing rules (later epics; DL24). Assumption on DL24, taken on its recommended option A: the rules component loads the allocation, assignment and transfer rules only in Epic 1, and the route decision goes live in a later epic.
- The package code each of rwb-comms and rwb-integration evaluates, and the prefix and path family of the refusal, until they are published (GAP-0383).

### 20. Remaining delivery steps

- Size the story (squad; DOR-RWB-ITG-E1073-ITG-16).
- Sign the epic design (solution architect).
- Fix the contract version the harness builds against (contract owners of the consumed services; DOR-RWB-ITG-E1073-ITG-23).
- Complete the contract stories listed in the header and publish their contracts (owning service teams).
- Load the synthetic test data and the in-force version ALLOC-2026.11 in DEV and SIT (QA with rwb-decision and rwb-case teams).
- Pending: package code and version label evaluated by rwb-comms and rwb-integration, model fetch owner and refusal path family, owner solution architect, tracked as GAP-0383.
