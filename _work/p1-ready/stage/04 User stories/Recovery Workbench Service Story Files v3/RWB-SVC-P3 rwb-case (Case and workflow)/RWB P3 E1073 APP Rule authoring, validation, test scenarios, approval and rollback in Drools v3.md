# RWB-P3-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1073-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Capability owner | P7 rwb-decision for the rule-package and rule-version registry and its endpoints; PLT for the embedded Drools kit |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-073 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E1073-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E1073-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| Contract version | v1 (the /v1 path of DP-13: /api/recovery/<short>/v1) |
| Readiness decisions | RD-P1-008 |
| External dependencies | RWB-P3-E1073-INF |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-011, FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: updated the section 16 reference to Recovery Workbench Test Cases v9.

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-073 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1073-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 37 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the rwb-case side of the rule change journey: the case fact mapping that every package reads, the rule version pinned on the case and on each decision record, the scenario gate that runs each in-force package's scenarios against those case facts in every build, and the rwb-decision authoring, approval, rollback and dry-run operations consumed behind their contract mock**, so that **a rule change goes from template to production without a code release, every case decision names the rule ID and the package version that made it, and rwb-case holds only an evaluated copy of an approved table**.

This story owns the case-side half of RWB-E1-073 only. The registry half — `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the workbook object in Blob, the load checks, the scenario runner, the four-eyes approval, the dated promotion and the one-call rollback — is owned by P7 rwb-decision under ASM-0069 and is consumed here through the rwb-decision contract and its fake. rwb-case writes no rule table and reads none (DP-01, DP-04). RWB-ITG-E1073-ITG proves the whole journey across the services; this story builds only what rwb-case must do for that journey.

### 2. Business rationale

Collection and recovery rules lived in procedure documents, and audit found the procedure not followed because the rules were not in the system (control CTL-08). The legacy story carried the control into Drools inside one monolith: the workbook, the compile, the schema, overlap, unreachable row, default row and scenario checks, the four-eyes approval, the dated promotion, the rollback and the change log all sat in the case module and wrote `rule_package_version`.

In the target, governance is central in rwb-decision (P7) and evaluation is local to the service that owns the decision (Arch v5 slides 27 and 41; Temporal and Drools design slides 15 and 16; ADR-017; DP-04). That split leaves rwb-case with exactly four duties, and this story builds them: it owns the case fact mapping that each package reads, so a decision is reproducible from the case; it pins the rule ID and the package version label on the case (DF-CAS-021) and on every decision record it writes (DP-03), so an approval found later still explains the outcome and an open case keeps the version it was decided under (R-UNI-38); it runs `RuleScenarioBuildGate` over the case facts in every build, so a change to the fact mapping that moves a scenario fails the build before it merges (legacy AC14); and it consumes the rwb-decision authoring, approval, rollback and dry-run operations as its published contract, never as local code.

This story meets REQ-CWC-013 (a validated load with a version, no release, rollback by one call), REQ-CWC-014 (schema, overlap, unreachable row, default row, compile and scenario checks before a version takes effect), REQ-DRI-004 (Epic 1 records use versioned rules) and REQ-CWC-008 (the allocation package always has a default row), at the case side of the journey. The measure is that every case decision in the SIT run names its rule ID and package version, the five in-force Epic 1 packages run their scenarios in every build against the case facts, and a wrong version leaves production in one call made in rwb-decision.

The registry, the workbook object and the promotion are not restated as this service's. This story declares no package operation of its own, holds no `rule_package_version` row and registers no Schedule; the reading of each legacy criterion that names one of those is set out in sections 8, 9, 11, 12 and 19 (GAP-0699; ASM-1246).

### 3. Preconditions

- RWB-P3-E1073-CON is published: the five consumed authoring and model operations with their paths, rights, error codes and the 2 s client budget, the model and catalog reads, the `RulePackageInForce` consumption contract, the `EvaluateRules` activity contract with `RuleResult` and `NoPackageInForce`, the cache and atomic-swap rules, the nine contract tables and the contract fakes.
- RWB-PLT-E1072-CON is published: the embedded Drools kit, with one KieBase per package version, first-match semantics, the cache bound, the checksum check and the `NoPackageInForce` outcome (DP-04).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the event-started workflow and the activity contracts of the kit (DP-10).
- RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the parameters contract and the reference-data contract of rwb-case, with the client library (DP-06, DP-07). `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20 are read through the parameters contract, never from code.
- RWB-PLT-E1047-CON and RWB-PLT-E1044-CON are published: the naming library and the per-service Flyway sequence (DP-14, DP-15). RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19).
- The package set the case side evaluates is the five Epic 1 package codes of the legacy story: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (TSD P3 v3 T2.2). Their versions and labels are rwb-decision rows and are read through its contract.
- The rule tables rule_package, rule_package_version, rule_row and rule_test_case are owned by rwb-decision (P7 rwb_decision); this service holds only the evaluated copy (DP-04), never the governance record.
- Package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows, loaded by "U-41" and approved by "U-51", asserted against the rwb-decision contract mock. This ALLOCATION set is synthetic fixture data in the test environment until the reference data names the assigned package.
- The users "U-41" (RW-COE) and "U-51" (RW-RISK) exist in rwb-access with the Rules and parameters rights of the legacy story; one person may not hold both (separation of duty).
- The release manifest `config/rule-packages.lock` lists the package code and the version label in force for each environment; it is generated at release and read by the build gate only.
- The `rwb_case` schema and its migrations are in place, including `recovery_case.rule_version` (DF-CAS-021) and the decision-record and outbox objects the platform library creates.
- RWB-P3-E1073-INF is tracked as an external dependency: the pinned base image, the toolkit, the heap for the KieBase cache and the one-hop path to rwb-decision.
- No build dependency on a non-contract story: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. rwb-decision: RW-COE loads a workbook through the load operation; the compile, schema, overlap, unreachable row, default row and scenario checks run there, the dry run is recorded, and RW-RISK approves the version. Steps 1 and 2 are P7's and are exercised here through the contract or its fake.
2. rwb-decision: at 00:01 on the valid-from date the promotion Schedule JOB-20 moves the APPROVED version to IN_FORCE, the previous version to SUPERSEDED, and publishes `rwb.decision.RulePackageInForce.v1`.
3. rwb-case: the case router consumes the event through its inbox, and the next evaluation of that package code fetches the version in force and verifies its checksum (RWB-P3-E2042-APP).
4. rwb-case: an event, a timer or a task reaches a case. The CaseWorkflow calls the `EvaluateRules` activity with the package code, the case facts and the business date.
5. CaseFactMapper: projects the facts of the case into the mapping declared in section 11 — product group, region code, exposure band, stage code, route code, queue, deviation flag and the entry values — reading only `rwb_case` rows through the case repository. No personal data enters the fact object.
6. The embedded Drools kit evaluates the version in force on the business date and returns `RuleResult(packageCode, packageVersion, ruleId, outputs)`; a package with no version in force raises `NoPackageInForce`, which is not retried.
7. RuleVersionPin: hands the `ruleId` and the `packageVersion` of the result to the record writer and to the case row, so no caller composes a label itself (BR6, BR7).
8. The RecordAndApply activity writes, in one `rwb_case` transaction, the local decision record with `rule_id` and the package version label, the state change, `recovery_case.rule_version` and the outbox row; a failed write moves nothing (DP-03).
9. rwb-case: an open case keeps the version it was decided under (R-UNI-38). A newer version in force changes the next decision only; it never rewrites a decision already taken or the version an open case keeps.
10. Build: `RuleScenarioBuildGate` loads the in-force package versions named by `config/rule-packages.lock` into an isolated Testcontainers database and runs every scenario of each package through the same evaluator and the same case fact mapping; a failing scenario fails the build and blocks the merge.
11. Build: a change to CaseFactMapper that moves a scenario result is a build failure, and the failure names the scenario, the package code and the version label (legacy AC14).
12. RW-COE, with RW-RISK, drives the authoring, approval, rollback and dry-run operations through the Workbench; each call is one hop to rwb-decision inside the 2 s budget, and this service stores no copy of a version row.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two rows of a workbook match the same case at the same row order | rwb-decision refuses the load whole and names both row IDs; no version is created and the version in force keeps running | MSG-P3-027 | AC2 |
| X2 | A scenario result differs from the expected result at load | rwb-decision refuses the load and names the failing scenario IDs; nothing reaches rwb-case | MSG-P3-027 | AC3 |
| X3 | A required column is missing or a value is outside its list | rwb-decision refuses the load and names the row and the column | MSG-P3-027 | AC5 |
| X4 | A row can never match because an earlier row covers it | rwb-decision refuses the load and names the row | MSG-P3-027 | AC6 |
| X5 | The allocation workbook has no default row | rwb-decision refuses the load | MSG-P3-027 | AC7 |
| X6 | The approver is the author | rwb-decision refuses the approval and the version stays LOADED | MSG-P7-002 | AC8 |
| X7 | Rollback with no earlier version | rwb-decision refuses the call and the version stays in force | MSG-P3-015 | AC9 |
| X8 | The same package code and version label are loaded twice | rwb-decision answers 409 | MSG-GEN-004 | AC10 |
| X9 | Valid from before today | rwb-decision answers 422 | MSG-GEN-003 | AC11 |
| X10 | An empty workbook file | rwb-decision answers 422 | MSG-GEN-001 | AC12 |
| X11 | The generated DRL of a workbook does not compile | rwb-decision refuses the load, names the row and the cell, writes no version row and stores no Blob object; the version in force stays | MSG-P3-027 | AC13 |
| X12 | A scenario of an in-force package fails in the pipeline because the case fact mapping changed | `RuleScenarioBuildGate` fails the build, names the scenario, the package code and the version label, and the merge is blocked | MSG-P3-027 | AC14 |
| X13 | No version of a package is in force on the business date | `EvaluateRules` fails at once with `NoPackageInForce`, non-retryable; no record and no state change; the case waits and the stuck-case scan raises it | MSG-P3-027 | AC16, BR10, TC-E1-073-01 |
| X14 | A role without Rules and parameters calls an authoring operation | rwb-decision answers 403 through the authorise contract; nothing changes | MSG-P4-002 | AC17, TC-E1-073-16 |
| X15 | rwb-decision does not answer inside the 2 s budget | The call answers 503 to the reader; the evaluation is retried on the activity retry policy and the model in force stays cached | None | AC18, BR11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E1073-CON, the platform contract stories and the rwb-decision fake; the registry, the workbook object and the promotion are P7's and never block the build |
| Negotiable | The fact-mapping columns, the scenario fixture and the gate output are agreed with the consumers; the version pin, the refusal and the `NoPackageInForce` outcome are fixed by R-UNI-38 and DP-04 |
| Valuable | A rule change reaches production without a release, every case decision names the version that made it, and a fact-mapping change that moves a scenario cannot merge |
| Estimable | One fact mapper, one version pin, one build gate with its fixture, one consumed client and the contract tests |
| Small | Fits one sprint with its tests |
| Testable | Every criterion is a component, contract or pipeline test; every P7 answer is stubbed in the contract fake and every gate run is on a Testcontainers database |

### 7. Acceptance criteria

```gherkin
Feature: Rule authoring, validation, test scenarios, approval and rollback in Drools

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given the rwb-decision contract mock returns package ALLOCATION version "ALLOC-2026.11" in force with 24 rows
    Given rules.testcases.min is 50 and the business date is 2026-12-10

  Scenario: AC1 Valid load (legacy RWB-E1-073 AC1)
    Given the rwb-decision contract mock returns version "ALLOC-2026.12" loaded by U-41 with the workbook checksum and "50 of 50 scenarios passed", approved by U-51 and in force from 2026-12-15
    Given a workbook for package ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 scenarios that pass every check
    When U-41 loads it with valid from 2026-12-15 and U-51 approves it
    Then version "ALLOC-2026.12" is in force from 2026-12-15
    Then the change log records author U-41, approver U-51, the load and approval times, the workbook checksum, "50 of 50 scenarios passed" and the dry run count

  Scenario: AC2 Overlap refused (legacy RWB-E1-073 AC2)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032", with version "ALLOC-2026.11" still in force
    Given rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032"
    Then version "ALLOC-2026.11" stays in force

  Scenario: AC3 Scenarios (legacy RWB-E1-073 AC3)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for the scenario check naming "TA-07" and "TA-19"
    Given the 50 scenarios with expected queues
    Given scenarios "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO"
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the scenario check naming "TA-07" and "TA-19"

  Scenario: AC4 Rollback (legacy RWB-E1-073 AC4)
    Given the rwb-decision contract mock returns version 6, "ALLOC-2026.12", in force again after one rollback of version 7, with the change log rollback entry and the decision_log_entry of the case allocated under version 7 keeping rule version "ALLOC-2026.13"
    Given version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it
    When U-41 calls rollback once for version 7
    Then version 6 is in force
    Then the change log holds the rollback with U-41, the time and the reason
    Then a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision_log_entry

  Scenario: AC5 Schema error (legacy RWB-E1-073 AC5)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for the schema check naming row 9 and its column
    Given row 9 has assignment reason "QUICK" that is not in its list
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the schema check naming row 9 and its column

  Scenario: AC6 Unreachable row (legacy RWB-E1-073 AC6)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for the unreachable row check naming "ALLOC-041"
    Given row "ALLOC-040" matches product group "SSME" in any region at row order 5
    Given row "ALLOC-041" matches product group "SSME" and region "NE3" at row order 6
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the unreachable row check naming "ALLOC-041"

  Scenario: AC7 Missing default (legacy RWB-E1-073 AC7)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for the default row check
    Given the allocation rows have no last row that matches every case
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the default row check

  Scenario: AC8 Author cannot approve (legacy RWB-E1-073 AC8)
    Given the rwb-decision contract mock returns the approve call refused with MSG-P7-002 and version "ALLOC-2026.12" still LOADED
    Given U-41 loaded version "ALLOC-2026.12"
    When U-41 calls approve
    Then the system refuses the call with MSG-P7-002
    Then the version stays LOADED

  Scenario: AC9 Rollback with no earlier version (legacy RWB-E1-073 AC9)
    Given the rwb-decision contract mock returns the rollback call refused with MSG-P3-015 and "TRF-2026.11" still in force
    Given package TRANSFER has only version "TRF-2026.11"
    When rollback is called for "TRF-2026.11"
    Then the system refuses the call with MSG-P3-015
    Then "TRF-2026.11" stays in force

  Scenario: AC10 Same version loaded twice (legacy RWB-E1-073 AC10)
    Given the rwb-decision contract mock returns 409 with MSG-GEN-004 for the second load of version label "ALLOC-2026.12"
    Given version "ALLOC-2026.12" of package ALLOCATION is loaded
    When a file with version label "ALLOC-2026.12" for package ALLOCATION is loaded again
    Then the system refuses the load with 409 and MSG-GEN-004

  Scenario: AC11 Valid from in the past (legacy RWB-E1-073 AC11)
    Given the rwb-decision contract mock returns 422 with MSG-GEN-003 for valid from
    When U-41 loads version "ALLOC-2026.14" with valid from 2026-11-01 on 2026-12-10
    Then the system refuses the load with 422 and MSG-GEN-003 for valid from

  Scenario: AC12 Empty file (legacy RWB-E1-073 AC12)
    Given the rwb-decision contract mock returns 422 with MSG-GEN-001 for rows
    When U-41 loads a template with no rows
    Then the system refuses the load with 422 and MSG-GEN-001 for rows

  Scenario: AC13 Compile error (legacy RWB-E1-073 AC13)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for the compile check naming row 14 and the cell, and no version row and no Blob object written
    Given the workbook for package ALLOCATION version "ALLOC-2026.14" has the condition cell "exposure_band >= " with no value at row 14
    When U-41 loads it
    Then DroolsCompileCheck fails and the load is refused with MSG-P3-027 for the compile check naming row 14 and the cell
    Then no rule_package_version row is written and no Blob object is stored
    Then version "ALLOC-2026.13" stays in force

  Scenario: AC14 Build gate fails on a scenario (legacy RWB-E1-073 AC14)
    Given the rwb-decision contract mock returns package ALLOCATION version "ALLOC-2026.13" in force with 50 scenarios
    Given package ALLOCATION version "ALLOC-2026.13" is in force with 50 scenarios
    Given a build changes the case fact mapping so that scenario "TA-07" returns "MTG-CEN-CO" instead of "MTG-BKK-CO"
    When RuleScenarioBuildGate runs in the pipeline
    Then the build fails with MSG-P3-027 for the scenario check naming "TA-07" and version "ALLOC-2026.13"
    Then the merge is blocked

  Scenario: AC15 Change log records the checksum (legacy RWB-E1-073 AC15)
    Given the rwb-decision contract mock returns the change log entry holding the SHA-256 "9f2c...e1b4" of the workbook, with the same checksum on rule_package_version.checksum and in the Blob object metadata, and a later download giving the same checksum
    Given the workbook file "ALLOCATION-2026.12.xlsx" for package ALLOCATION version "ALLOC-2026.12"
    When U-41 loads it and the load succeeds
    Then the change log entry holds the SHA-256 checksum "9f2c...e1b4" of the workbook
    Then the same checksum is on rule_package_version.checksum and in the Blob object metadata
    Then a later download of the workbook gives the same checksum

  Scenario: AC16 No version in force on the business date (new, D-RCV-60)
    Given no version of package ALLOCATION is in force on the business date (date not specified in the source documents (DOR-RWB-P3-E1073-APP-3)) in the rwb-decision contract mock
    Given a case is open on package ALLOCATION with no version in force
    When EvaluateRules runs for the case
    Then EvaluateRules fails at once with NoPackageInForce, which is not retryable
    Then no decision_log_entry is written and no case state changes
    Then the stuck-case scan raises the case with MSG-P3-027

  Scenario: AC17 Authoring refused for a role without rights (new, D-RCV-60)
    Given the rwb-decision contract mock returns 403 with MSG-P4-002 for the load call from a role without Rules and parameters
    Given RW-CASEOWN does not hold Rules and parameters
    When RW-CASEOWN calls the load of ALLOCATION
    Then the system refuses the call with 403 and MSG-P4-002
    Then nothing changes

  Scenario: AC18 Registry does not answer inside the budget (new, D-RCV-60)
    Given the rwb-decision contract mock does not answer inside the 2 s budget on the model fetch
    Given the model of package ALLOCATION version "ALLOC-2026.11" is cached and in force
    When EvaluateRules reads the model
    Then the call answers 503 to the reader
    Then the evaluation is retried on the activity retry policy
    Then the cached model in force stays in use

  Scenario: AC19 Load refused in full on any failed check (new, D-RCV-60)
    Given the rwb-decision contract mock returns the load refused with MSG-P3-027 for a failed check
    Given a workbook for package ALLOCATION version "ALLOC-2026.12" has a failed check
    When U-41 loads it
    Then the system refuses the whole load with MSG-P3-027
    Then no partial version reaches rwb-case and version "ALLOC-2026.11" stays in force
```

The new criteria AC16 to AC19 cover exceptions X13 to X15 and rule BR2 (DOR-RWB-P3-E1073-APP-3 and -4). These fifteen criteria are the legacy acceptance of the whole authoring journey and are copied unchanged apart from the origin tag, the rwb-decision contract mock line and the case-fact wording of AC14. The rule IDs ALLOC-032, ALLOC-040 and ALLOC-041 in these criteria are test data, not taken from a source document. The split they hide is this. The load, the compile, the schema, overlap, unreachable row, default row and scenario checks, the dry run, the four-eyes approval, the promotion at 00:01, the rollback by one call, the `rule_package_version` row and the Blob object are P7 rwb-decision and are faked for every criterion here; this story consumes them through the operations of section 12.2 and asserts only what it receives. The case-side half is P3's and is what this story builds: the case fact mapping of section 11, the pin of `rule_id`, the package version label and `recovery_case.rule_version` (DP-03, DP-04, BR7), the `RuleScenarioBuildGate` over those facts (AC14), the `NoPackageInForce` refusal (MSG-P3-027) and the rule that an open case keeps the version it was decided under (R-UNI-38). Where a criterion speaks of a version in force, this story reads the version through the rwb-decision contract and never from a local table.

```gherkin
Feature: Activity retry and timeout in Drools

  Scenario: AC20 Activity retried and timed out (new, D-RCV-60)
    Given the rwb-decision contract mock does not answer inside the 2 s budget on the model fetch on every attempt
    Given the model of package ALLOCATION version ALLOC-2026.11 is cached and in force
    When EvaluateRules runs for a case on package ALLOCATION
    Then the evaluation activity is retried on the activity retry policy
    Then when the retry policy is exhausted the activity fails with a timeout
    Then no decision_log_entry is written and no case state changes
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version passes the compile, schema, overlap, unreachable row, default row and scenario checks before it is stored, and the dry run is recorded for the approver; the checks are rwb-decision's and are asserted here through the contract | REQ-CWC-014; D-RCV-36 T4; ASM-0069 |
| BR2 | A load with any failed check is refused in full; no partial version reaches this service | Reference data change process, step 3; CTL-08 |
| BR3 | First match: RuleSet = package code, each row is one rule with NAME = rule ID, rows share one activation-group, salience comes from row order and the default row is last; exactly one row decides | D-RCV-36 T5 |
| BR4 | The allocation package always has a default row | REQ-CWC-008 |
| BR5 | A version takes effect on its valid-from date after approval, promoted at 00:01 by the rwb-decision Schedule JOB-20; an open case keeps the version it was decided under | R-UNI-38; Arch v5 slide 44 |
| BR6 | The author cannot approve; RW-RISK signs rule package changes and the check is rwb-decision's | Separation of duty table; CTL-08 |
| BR7 | Every case decision record pins the rule ID and the package version label, written in the same transaction as the state change and the case row, and `recovery_case.rule_version` carries the version of the decision in force | DP-03; D-RCV-36 T5; Architecture v5 slide 28 |
| BR8 | Every load, approval and rollback is in the change log with author, approver, time, checksum and test result; the log is rwb-decision's and this service writes no row of it | REQ-CWC-013; FSD A2.14 |
| BR9 | The workbook is the Drools XLS decision-table format, one workbook per package with a Rows and a Tests tab, and the generated DRL is stored with the workbook; rwb-case reads neither at run time | D-RCV-36 T3, T4; DP-04 |
| BR10 | A load carries at least `rules.testcases.min` scenarios (50) from the Tests tab, and every scenario runs through the same RuleEvaluator as production | REQ-CWC-014; Arch v5 slide 27; D-RCV-36 T4 |
| BR11 | Every in-force package's scenarios run in every build through `RuleScenarioBuildGate`, over the case fact mapping of this service, and a failing scenario fails the build and blocks the merge | D-RCV-36 T4; REQ-CWC-014 |
| BR12 | The case fact mapping reads only `rwb_case` rows and carries no personal data; a package row that names a fact this mapping does not supply fails the gate rather than defaulting | DP-01; Template and Rules §R7.2 s17 |
| BR13 | No code in rwb-case writes or reads `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case`; the label on a case and on a record is a value, not a foreign key | ASM-0069; DP-01; DP-04 |
| BR14 | A package version that is not in force is never used: the evaluation fails with `NoPackageInForce` and nothing is written | R-UNI-38; DP-04; MSG-P3-027 |

BR1, BR2, BR6 and BR8 are implemented in P7 rwb-decision under ASM-0069 and are asserted here only through the consumed operations and the fake. BR3 to BR5, BR7 and BR9 to BR14 are the rules this story builds and tests at the case side.

### 9. State transitions

None. This story changes no case status. The states of a rule package version are rwb-decision's (legacy section 9) and are shown here only to fix what rwb-case observes through the contract.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | LOADED |
| None | Load | Any check fails, including the compile | REFUSED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | RULE_PACKAGE_EFFECTIVE (the 00:01 Schedule JOB-20 in rwb-decision) | Valid from reached | IN_FORCE; previous SUPERSEDED |
| IN_FORCE | Rollback | Earlier version exists | ROLLED_BACK; previous IN_FORCE |

The case side is a pin, not a move. A decision already taken keeps its `rule_version`; an open case keeps the version it was decided under (R-UNI-38) until its next decision. No case row is rewritten by a promotion, a rollback or a refusal. rwb-case registers no Schedule and holds no job row for the promotion: JOB-20 is rwb-decision's (Arch v5 slide 44; DP-10).

| From | Event | Condition | To |
|---|---|---|---|
| No version cached | Evaluation with no version in force | `NoPackageInForce` raised, non-retryable | Unchanged; the caller reports MSG-P3-027 |
| Version pinned on a case | A newer version becomes in force | The newer version is promoted in rwb-decision | The case keeps its pinned version until its next decision |
| Version pinned on a case | The next decision of that case | A version is in force on the business date | The next decision pins the version in force |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a package version, calls the dry run and calls the rollback through the rwb-decision operations (Rules and parameters CRUD); reads the version list |
| RW-RISK, risk and model risk officer | Approves a version (Rules and parameters A); may not hold RW-COE, and the author cannot approve |
| RW-AUDIT, internal audit | Reads versions, scenario results, dry-run counts and the change log (Rules and parameters R) |
| RW-REFADM | Prepares load files; may not approve |
| SY-RULES, Drools evaluator | Evaluates the version in force inside the `EvaluateRules` activity and hands its rule ID and version to the record writer |
| SY-CASEWF, case workflow | Applies the decision; no authoring right and no endpoint right |
| RW-TRIBE, tribe lead and squad members | Builds and runs `RuleScenarioBuildGate`; no SIT, UAT or PROD data in the build |
| The rwb-case service identity | Reads the case facts for the mapping and writes the pin; calls no authoring operation from a workflow |
| No delegation of authority level applies | A rule package version is not a credit decision |

The rights behind the consumed operations are rwb-access's and are answered through the authorise contract (DP-08) as declared in RWB-P3-E1073-CON; this story re-implements none of them.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-003 | recovery_case | product_group | Read, into the fact mapping |
| DF-CAS-006 | recovery_case | stage_code | Read, into the fact mapping |
| DF-CAS-008 | recovery_case | route_code | Read, into the fact mapping |
| DF-CAS-010 | recovery_case | queue_id | Read, into the fact mapping |
| DF-CAS-012 | recovery_case | region_code | Read, into the fact mapping |
| DF-CAS-014 | recovery_case | dpd_at_entry | Read, into the fact mapping |
| DF-CAS-015 | recovery_case | exposure_band | Read, into the fact mapping |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Read, into the fact mapping |
| DF-CAS-019 | recovery_case | deviation_open | Read, into the fact mapping |
| DF-CAS-021 | recovery_case | rule_version | Write, the package version of the decision in force |
| DF-WRK-002 | queue | queue_code | Read, into the fact mapping as the current queue |
| DF-CAS-024 to DF-CAS-029 | case_account | the account link of the case | Read, counted by the mapping and never carried into the fact object |
| DF-REF-275 | rule_package (P7) | package_code | Read through the rwb-decision contract only |
| DF-REF-281 | rule_package_version (P7) | version_label | Read through the rwb-decision contract, and written to the case and the record as a value |
| DF-REF-282 | rule_package_version (P7) | status | Read through the rwb-decision contract |
| DF-REF-285 | rule_package_version (P7) | checksum | Read through the rwb-decision contract; compared on the model fetch |
| DF-REF-286, DF-REF-287 | rule_package_version (P7) | valid_from, valid_to | Read through the rwb-decision contract |
| DF-REF-292, DF-REF-293 | rule_package_version (P7) | test_result, dry_run_counts | Read through the rwb-decision contract |
| DF-DEC-004 | decision_log_entry | rule_id | Written by the local record library |
| DF-DEC-005 | decision_log_entry | rule_version | Written by the local record library |
| DF-CAS-060, DF-CAS-061 | case_entry_exclusion | rule_id and rule_version of an exclusion | Written by the entry path of RWB-P3-E1018-APP, read here for the gate fixture |

The case fact mapping is the named set of facts a package reads, and it is the contract this story owns: `productGroup`, `regionCode`, `exposureBand`, `stageCode`, `routeCode`, `queueCode`, `deviationOpen`, `dpdAtEntry`, `totalOutstandingAtEntry` and `businessDate`. Every package row that names a condition column outside this set fails `RuleScenarioBuildGate`; the mapping is extended only with a story that owns the field. No personal data enters the object: no name, address, identity number or contact point.

rwb-case writes no rule table and holds no `rule_package_version` row: the label on the case and on the record is a value, not a foreign key (DP-01, ASM-0069). The property types, lengths and required flags of the model and catalog resources the consumed operations return are Not specified in the source documents (GAP-0700; ASM-1247); RWB-P3-E1073-CON fixes the element names and leaves the types to the review with the rwb-decision owner. Field IDs are those of the Logical Data Model and Data Dictionary. The case read that feeds the dry run is taken through RWB-P3-E1073-CON as given, and the fake answers both ways until that contract states whether it publishes the case reads (GAP-1330).

### 12. Contract

#### 12.1 REST operations provided

None. This story serves no new business operation. The case fact mapping is internal, the version pin is a column of the case and of the record, and the scenario gate runs in the pipeline. The case read that shows the pinned version is `GET /api/recovery/case/v1/cases/{caseId}` of RWB-P3-E1023-CON and is unchanged here.

#### 12.2 REST operations consumed

Base `/api/recovery/decision/v1`; owner P7 rwb-decision for every row. One hop, 2 s client budget, a breaker per operation (DP-11, ADR-020).

| Method | Path | Used for | Answers | Owner / service |
|---|---|---|---|---|
| POST | `/admin/rule-packages/{packageCode}/versions` | The multipart load of a workbook with `validFrom` (AC1, AC4, AC10, AC11, AC12, AC13, AC15) | 201, 401, 403, 404, 409, 422, 503 | P7 rwb-decision |
| GET | `/admin/rule-packages/{packageCode}/versions` | The version list, the status of each version and the checksum of the one in force (AC1, AC2, AC8, AC9) | 200, 401, 403, 404, 503 | P7 rwb-decision |
| POST | `/admin/rule-package-versions/{versionId}/approve` | The four-eyes approval and its refusal (AC1, AC8) | 200, 401, 403, 404, 409, 503 | P7 rwb-decision |
| POST | `/admin/rule-package-versions/{versionId}/rollback` | The one-call rollback with a required reason (AC4, AC9) | 200, 401, 403, 404, 409, 422, 503 | P7 rwb-decision |
| GET | `/admin/rule-package-versions/{versionId}/dry-run` | The dry-run counts a load records for the approver (AC1) | 200, 401, 403, 404, 409, 503 | P7 rwb-decision |
| GET | `/rule-models/{packageCode}/{version}` | The compiled model, its version label and its SHA-256, on the fetch that verifies the checksum | 200, 401, 403, 404, 503 | P7 rwb-decision |
| GET | `/rule-catalog/{ruleId}?packageVersion=` | `action_text`, `owner_role`, `timer_spec`, `target_queue_code` and `outputs` of one row by rule ID and version | 200, 401, 403, 404, 503 | P7 rwb-decision |

Every operation is attributed to rwb-decision and none is declared as provided by rwb-case. The five authoring operations are called by RW-COE, RW-RISK and RW-AUDIT through the Workbench and never from a workflow. The path set and the field-level shape of the two reads are Not specified in the source documents (GAP-0700; ASM-1247); RWB-P3-E1073-CON publishes the declared shape, its rights and its error codes, and the fake is written to it.

#### 12.3 Events published

None. This story publishes no event type. The shared ledger event `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library of DP-03 when a decision is taken in rwb-case; its schema is unchanged by this story and is the one declared in RWB-P3-E1018-CON.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | The case router, inbox dedupe; refreshes the evaluated copy for that package code so the next evaluation reads the version in force |

The event is consumed by the model-cache path of RWB-P3-E2042-APP; this story only names it so that the scenario gate and the evaluation read the same package set. rwb-case publishes nothing on the topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Carries the case from entry to closure and asks the rules at each decision |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Calls the embedded Drools kit with a package code, the case facts of section 11 and the business date; returns `RuleResult(packageCode, packageVersion, ruleId, outputs)` or raises `NoPackageInForce` |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record with the pinned rule ID and version, the state change, `recovery_case.rule_version` and the outbox row in one transaction |

The workflow and activity pattern, the `CaseEvent` signal and the retry policy are RWB-P3-E2043-CON; the rule-evaluation contract of `EvaluateRules` is RWB-P3-E1073-CON. This story implements the fact mapping and the pin inside those contracts and adds no fourth activity.

#### 12.6 Schedules

None. The 00:01 promotion is the Temporal Schedule JOB-20 in rwb-decision, and rwb-case registers no Schedule for a rule package (Arch v5 slide 44; DP-10). The legacy Quartz job `RulePackageEffectiveDateJob` and its `job_catalog` row have no target in this service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case header and its facts; `rule_version` (DF-CAS-021) is written by the pin |
| queue | P3 (rwb_case) | The queue code a row names and the case sits in; read |
| case_account | P3 (rwb_case) | The account link of a case; read by the mapping, never carried into the fact object |
| case_entry_exclusion | P3 (rwb_case) | The rule ID and rule version of an exclusion, read for the gate fixture |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The outbox, inbox and idempotency envelope (DP-09) |

No rule table is named as owned. `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` are rwb-decision's (ASM-0069; DP-01) and are read only through the operations of 12.2. rwb-case holds no workbook object and no `job_catalog` row.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock | The P7 contract | ALLOCATION "ALLOC-2026.11" in force with 24 rows, loaded by "U-41" and approved by "U-51"; "ALLOC-2026.12" loaded with 26 rows and 50 passing scenarios, valid from 2026-12-15, checksum "9f2c...e1b4", approved on 2026-12-02, with dry-run counts; "ALLOC-2026.13" as version 7 in force and "ALLOC-2026.12" as version 6 in force before it, plus the rollback answer; "ALLOC-2026.14" refused at the compile check naming row 14; TRANSFER "TRF-2026.11" as the only version; the overlap, schema, unreachable row, default row and scenario refusals with MSG-P3-027; 409 with MSG-GEN-004; 422 with MSG-GEN-003 and MSG-GEN-001; 409 with MSG-P7-002; 200 with MSG-P3-015 for the refused rollback; a model and a catalog answer for R-ALLOC-014 with the checksum; one slow answer |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Rules and parameters CRUD to RW-COE and A to RW-RISK, R to RW-AUDIT, and refusing RW-CASEOWN with MSG-P4-002 |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 7 consumed | The five authoring operations and the two reads of rwb-decision; one hop, 2 s timeout, a breaker per operation |
| Kafka | None published, 1 consumed | `rwb.decision.events.v1` for RulePackageInForce |
| Temporal | 1 workflow, 2 activities | CaseWorkflow; EvaluateRules and RecordAndApply, both from the kit of RWB-P3-E2043-CON |
| File | None at run time | The build gate reads the release manifest `config/rule-packages.lock` and a synthetic workbook fixture inside the pipeline; no workbook is exchanged at run time |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `rules`, Java package `th.co.scb.ace.workbench.recovery.case.rules`.

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

DP-04 and DP-10 are the patterns this story serves: the evaluated copy is local, and the dated promotion that the legacy Quartz job performed is a Temporal Schedule in rwb-decision, so no job row and no trigger exist here.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseFactMapper | Service | Projects the facts of section 11 from `rwb_case` rows into the object a package reads; refuses a package row that names a fact outside the mapping |
| RuleVersionPin | Service | Takes `ruleId` and `packageVersion` from `RuleResult` and hands them to the record writer and to `recovery_case.rule_version`; no caller builds a label |
| PinnedVersionRead | Service | Answers the pinned version of a case and the version now in force, so a reader sees both after a promotion |
| RuleScenarioBuildGate | Build gate | Loads the in-force package versions of `config/rule-packages.lock`, runs every scenario through the evaluator and the `CaseFactMapper`, and fails the build on a difference |
| CaseFactScenarioFixture | Test fixture | The synthetic case facts of the gate: product group, region, exposure band, stage, route, queue, deviation flag and the entry values; no production data |
| ScenarioResultComparator | Service | Compares each expected queue or outcome with the result and names the scenario, the package code and the version label on a difference |
| RulePackageAuthoringClient | Client | The five consumed authoring operations with the 2 s budget, the breaker and the error mapping of section 14 |
| RuleModelCatalogClient | Client | The model and catalog reads, with the checksum comparison and the 404 answer |
| DroolsEvaluationAdapter | Service | The only caller of the embedded Drools kit inside `EvaluateRules`; raises `NoPackageInForce` |
| RuleSetParameterReader | Service | Reads `rules.testcases.min`, `drools.kiebase.cache.max` and the package code list through the parameters contract |

**Database and migrations**

- No new table and no new column is required: `recovery_case.rule_version` (DF-CAS-021) and the decision-record and outbox objects already exist in `rwb_case` (DP-03).
- One migration `V1073_1__rule_version_index.sql` adds an index on `recovery_case (rule_version, status)` and on the decision record `(rule_version, decided_at)`, so the pinned-version read answers inside the 2 s budget.
- No seed row: the five package codes and their versions are rwb-decision rows, seeded by RWB-P7-E1073-APP (ASM-0069).

**Configuration and reference data**

- `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20 through the parameters contract (DP-06); the values are never Java constants.
- The package code list of the case side — ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER — is a parameter, not a constant (DP-06).
- `config/rule-packages.lock` is the release manifest the gate reads: package code and version label in force per environment.
- The status values and product groups used by the mapping come from LOV-CASE-STATUS and LOV-PRODUCT through the reference-data contract (DP-07).

**Build steps**

1. CaseFactMapper with the ten facts, the read of `rwb_case` rows and the refusal of an unknown condition column; unit tests for BR12 and X13.
2. RuleVersionPin and the one-transaction write with the record library; tests for BR7 and the pin after a promotion.
3. PinnedVersionRead, so a promotion or a rollback changes the next decision only; tests for BR5 and X13.
4. RulePackageAuthoringClient over the five operations with the error mapping; contract tests for AC2, AC5 to AC13 and X14, X15.
5. RuleModelCatalogClient over the two reads with the checksum comparison and the 404 answer; contract tests for AC1 and AC15.
6. DroolsEvaluationAdapter inside `EvaluateRules`, returning the rule ID and package version of the version in force; tests for BR14 and `NoPackageInForce`.
7. CaseFactScenarioFixture and ScenarioResultComparator; tests for AC3.
8. RuleScenarioBuildGate over the release manifest and a Testcontainers database, with the five package versions and their scenarios; test for AC14.
9. RuleSetParameterReader and the package code list; tests for BR10 and the parameter switch.
10. Contract-fake run: every rwb-decision and rwb-access answer of section 12.8 stubbed, so the story builds and its tests run before P7 and P4 land.

**Feature switch.** The legacy flag name `rwb.p3.drools` is kept as the legacy reference and read as a parameter through the parameters contract. Off: the gate runs nothing, the evaluation path returns `NoPackageInForce` with MSG-P3-027 for every package, and nothing else changes; the pin and the case reads are unaffected.

**Done when.** The tests in section 16 pass, every case decision record of the SIT run names its rule ID and package version, the five in-force Epic 1 packages run their scenarios in every build against the case facts, a changed fact mapping fails the gate, and no open case has been re-pointed by a promotion or a rollback.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A package version check fails, or no version is in force for a package | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Empty file or no rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version label already loaded, or version not LOADED | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without the right calls an authoring operation | You cannot {action} here. Your role does not include it. |

The texts are the agreed texts of the legacy story and of the message catalogue; this story adds no message and changes no text. Where the text of MSG-P3-027 in the Error and Message Standard v4 differs from the row above, the Error and Message Standard v4 text governs. For MSG-P3-027 the `{check}` value is compile, schema, overlap, unreachable row, default row, scenario or package in force, and the `{detail}` names row IDs, cells, scenario IDs, rule IDs, package codes and version labels only, never a case fact or a person. For MSG-P3-015 the `{table}` value is the package code. The consumed operations carry these messages; rwb-case re-states none of them.

### 15. Screens and states

No screen in this story. Rule packages are loaded by file and read through the version list, and SCR-39 Rules and parameters of Epic 8 (FEAT-ADM-02) shows the same versions. The version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are rwb-decision's and are read from the version list; the case-side surfaces are the pinned version on the case record of RWB-P3-E1023-CON and the build-gate report. The rule change audit report is RWB-P3-E2041-APP.

| Screen | State | What this story answers |
|---|---|---|
| SCR-39 Rules and parameters (Epic 8) | Version list | The versions, their status, their valid-from date and their checksum, read through the version list |
| SCR-39 Rules and parameters (Epic 8) | Empty | Not specified in the source documents (CG-ALL-3923) |
| SCR-39 Rules and parameters (Epic 8) | Loading | Not specified in the source documents (CG-ALL-3923) |
| SCR-39 Rules and parameters (Epic 8) | Error | Not specified in the source documents (CG-ALL-3923) |
| SCR-39 Rules and parameters (Epic 8) | No access | Not specified in the source documents (CG-ALL-3923) |
| Case record view (RWB-P3-E1023-CON) | Decision in force | The rule ID and the package version label of the last decision, and the version an open case keeps after a promotion |
| No screen | Build gate | The scenario, the package code and the version label that failed, and the merge blocked |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-073-16 | Access; BR13 | Component | RW-CASEOWN calls the load of ALLOCATION; refused with MSG-P4-002 |
| TC-E1-073-21 | AC16; BR14; X13 | Component | No version of ALLOCATION is in force on the business date; EvaluateRules fails with NoPackageInForce |
| TC-E1-073-22 | AC17; X14 | Component | RW-CASEOWN without the Rules and parameters right calls the load of ALLOCATION; refused with 403 and MSG-P4-002 |
| TC-E1-073-23 | AC18; BR11; X15 | Component | The model fetch does not answer inside 2 s; 503 to the reader and the cached model in force stays in use |
| TC-E1-073-24 | AC19; BR2 | Component | A load with a failed check is refused in full with MSG-P3-027; no partial version reaches rwb-case |
| TC-E1-073-25 | AC20; X15 | Component | Model fetch times out on every attempt; the activity retries on the retry policy, then fails with a timeout and no decision_log_entry is written |
| TC-E1-073-20 | Access; BR13 | Component | A role without Rules and parameters R calls the dry run; refused with MSG-P4-002 |
| TC-E1-073-01 | AC1, BR1, BR5, BR7, BR8 | End to end | ALLOCATION version with 26 rows, 50 passing scenarios and a checksum |
| TC-E1-073-02 | AC2, BR3 | End to end | Rows ALLOC-031 and ALLOC-032 at row order 12 |
| TC-E1-073-03 | AC3, BR1, BR10 | End to end | Scenarios TA-07 and TA-19 failing |
| TC-E1-073-04 | AC4, BR5, BR7 | End to end | Versions 6 and 7, and the decision log entry that keeps ALLOC-2026.13 |
| TC-E1-073-05 | AC5, BR1 | End to end | Row 9 with value QUICK |
| TC-E1-073-06 | AC6, BR1 | End to end | Rows ALLOC-040 and ALLOC-041 |
| TC-E1-073-07 | AC7, BR4 | End to end | No default row |
| TC-E1-073-08 | AC8, BR6 | End to end | Load and approval by U-41 |
| TC-E1-073-09 | AC9, BR5 | End to end | TRANSFER with one version |
| TC-E1-073-10 | AC10 | End to end | Label ALLOC-2026.12 twice |
| TC-E1-073-11 | AC11 | End to end | Valid from 2026-11-01 on 2026-12-10 |
| TC-E1-073-12 | AC12 | End to end | Template with no rows |
| TC-E1-073-13 | AC13, BR1, BR9 | End to end | Condition cell exposure_band >= with no value at row 14 |
| TC-E1-073-14 | AC14, BR11, BR12 | End to end | Fact mapping changed so TA-07 returns MTG-CEN-CO |
| TC-E1-073-15 | AC15, BR8, BR9 | End to end | Workbook ALLOCATION-2026.12.xlsx and its SHA-256 |
| TC-E1-073-17 | Access; BR13 | Component | RW-CASEOWN calls the version list of ALLOCATION; refused with MSG-P4-002 |
| TC-E1-073-18 | Access; BR6 | Component | RW-COE calls approve without Rules and parameters A; refused with MSG-P4-002 |
| TC-E1-073-19 | Access; BR5 | Component | RW-RISK calls rollback without Rules and parameters U; refused with MSG-P4-002 |

The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. The Level column maps the legacy System level to End to end and the legacy Access level to Component. Every test runs against the rwb-decision fake for the registry half and against `rwb_case` for the case-side half; TC-E1-073-16 to TC-E1-073-20 run against the rwb-access fake. The real cross-service proof is RWB-ITG-E1073-ITG.

### 17. Guardrails

- No business value in code: rows, conditions, target queues, scenarios, the test count and the cache bound are data and configuration, read through the parameters and reference-data contracts.
- No personal data in logs, metrics, tests, workflow history or the fact object: the mapping carries codes and amounts only, the scenarios use synthetic case facts, and the dry run reports counts.
- No read of another service's tables: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` come only through the rwb-decision contract, and `rwb_case` holds no foreign key into `rwb_decision` (DP-01; ASM-0069).
- One evaluator: the package versions are evaluated only through the embedded Drools kit inside the `EvaluateRules` activity; no code reads a workbook, a generated DRL or a rule table (DP-04).
- Every case decision record pins the rule ID and the package version label in the same transaction as the state change; a refused or failed write moves nothing (DP-03; R-UNI-39).
- A decision already taken is never changed, and the version an open case keeps is never rewritten; a rollback is one call in rwb-decision that names the version it returns to.
- The approver is never the author; the check is rwb-decision's and is asserted here through the fake, not re-implemented.
- The build gate reads the release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD and never writes a live database.
- One hop only, a 2 s timeout and a breaker per downstream; a caller never chains two services (DP-11; ADR-020).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14, FEAT-CWC-15 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-08, TC-E1-073-09, TC-E1-073-10, TC-E1-073-11, TC-E1-073-15 |
| REQ-CWC-014 | Schema, overlap, unreachable, default, compile and scenario checks | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | None | TC-E1-073-02, TC-E1-073-03, TC-E1-073-05, TC-E1-073-06, TC-E1-073-07, TC-E1-073-12, TC-E1-073-13, TC-E1-073-14 |
| REQ-DRI-004 | Epic 1 records for case creation, assignment and transfer use versioned rules | Epic 1, 3.3; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-15 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-41 | TC-E1-073-07 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | Arch v5 slide 27; D-RCV-36 T3 to T6; D-RCV-60 | FEAT-CWC-14, FEAT-DRI-07 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-14 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Ownership Map v1; D-RCV-60 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | None | TC-E1-073-16 to TC-E1-073-20 |

### 19. Out of scope

- The registry half of the legacy story: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the workbook object in Blob, the load checks, the scenario runner, the four-eyes approval, the dated promotion and the one-call rollback (RWB-P7-E1073-APP; ASM-0069).
- The 00:01 promotion Schedule JOB-20 and the publication of RulePackageInForce in rwb-decision.
- The model cache, the atomic swap, the checksum verification of a fetched model and the catalog read client of the Epic 2 packages (RWB-P3-E2042-APP).
- The workflow and activity pattern, the `CaseEvent` signal and the retry policy (RWB-P3-E2043-CON).
- The rule change audit report and the case-side audit read (RWB-P3-E2041-APP).
- The case record view that shows the pinned version and the queue case list (RWB-P3-E1023-CON; RWB-P3-E2011-CON).
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH and the UNIVERSAL package (RWB-P3-E2042-APP; Epic 3; DL24).
- The reference data loads for queues and lists (RWB-P3-E1043-APP).
- The administration screen for rule packages, SCR-39 and FEAT-ADM-02 (Epic 8).
- The base image, the toolkit, the heap for the KieBase cache and the one-hop path to rwb-decision (RWB-P3-E1073-INF); the workbook container and its immutability policy (RWB-P3-E2042-INF).
- The real cross-service proof of the load, the approval, the promotion, the pin and the rollback (RWB-ITG-E1073-ITG).
- The property types, lengths and required flags of the model and catalog resources and the operational values of the deployment story, which are Not specified in the source documents (GAP-0700; ASM-1247).
