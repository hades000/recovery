# RWB-P7-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1073-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-073 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-P |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; small, fits within two weeks |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1073-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E1-073, holding the rule-package registry, the workbook upload and parse, the compile and load checks, the at-least-50-scenario runner, the case-fact dry run, the four-eyes approval, the dated promotion at 00:01 under JOB-20, the one-call rollback and one hash-chained decision record per state change. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1073-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 31 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE) and a risk and model risk officer (RW-RISK)**, I want **the rule-package registry of rwb-decision to take a Drools workbook, parse its Rows and Tests tabs, generate and compile the DRL, run the schema, overlap, unreachable-row, default-row, compile and at-least-50-scenario checks, refuse a load whole when any check fails, record the dry run over the open cases, store the version LOADED with its workbook, DRL and SHA-256, take a four-eyes approval the author cannot give, promote the version at 00:01 on its valid-from date and announce it, roll back in one call with a reason, and record every state change once in the hash-chained decision log**, so that **a rule change reaches the owning services as tested, approved, dated data with a version stamped on it, and a wrong version leaves production in one call without a software release**.

Inside `rwb-decision` this is the registry and its governance:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1` (DP-13), topic `rwb.decision.events.v1` (DP-14), task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- What moves here: the whole authoring path of the legacy monolith — the workbook and its Rows and Tests tabs with their row numbers and the version-label cell, the generated DRL, the compile check, the four table checks, the scenario runner at `rules.testcases.min` (50), the dry run over open cases, the `rule_package_version` row with its workbook reference, DRL, SHA-256, dates, author and approver, the four-eyes approval, the six version states, the dated promotion that was a Quartz job, and the one-call rollback.
- The values are unchanged: package codes ALLOCATION and TRANSFER; version labels `ALLOC-2026.11`, `ALLOC-2026.12`, `ALLOC-2026.13`, `ALLOC-2026.14` and `TRF-2026.11`; rule IDs `ALLOC-031`, `ALLOC-032`, `ALLOC-040`, `ALLOC-041`; scenario IDs `TA-07` and `TA-19`; queues `MTG-BKK-CO` and `MTG-CEN-CO`; row 9's reason `QUICK`; 24 and 26 rows; 50 scenarios; valid from 2026-12-15; the SHA-256 example `9f2c...e1b4`; roles RW-COE, RW-RISK, RW-AUDIT and RW-REFADM; synthetic users U-41 and U-51.
- One thing does not move: evaluation. The KieBase, first-match semantics, the 300 ms budget and the LRU cache of 20 stay in the owning service, which fetches a version and verifies its checksum before it swaps it in (DP-04, ADR-017). This story compiles a workbook to prove it compiles, runs the stored scenario set through the same evaluator contract the owning services use, and then serves rows and states. No working memory survives a call here.

### 2. Business rationale

Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). A bad row can move every case that reaches it, so a load must be refused whole, a scenario must fail the build, and a rollback must take one call. In the target the rule is still data, but the data is owned and versioned in one service and evaluated in another, and both mechanisms changed: the model is no longer read from one shared schema, and the change log is no longer one table written by one writer (ADR-017, ADR-022).

That split creates two new ways to lose the control. A service can run a version this service never promoted, and a promotion can happen with no approver and no record. This story closes both: the version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are held and moved only here, and every move appends one entry to the hash-chained decision log before the state is used.

It meets REQ-CWC-013 (validated load with a version, no release, rollback by one call), REQ-CWC-014 (schema, overlap, unreachable row, default row and scenario checks), REQ-DRI-004 (Epic 1 records use versioned rules) and REQ-CWC-008 (the allocation package always has a default row), and follows D-RCV-36 T3, T4, T5 and T8. This is the secondary slice of RWB-E1-073: the run and the case-side checks of the legacy monolith stay with rwb-case, the lists come from their own owners, and the evaluator stays in the service that owns the model.

### 3. Preconditions

- The `rwb_decision` baseline is in place from the service template: schema, login, base, topic, task queue and chart, and the four registry tables `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case`. Their physical columns are Not specified in the source documents (GAP-2457; ASM-4086).
- `decision_log_entry` exists with `chain_seq`, `prev_hash`, `entry_hash` and `corrects_entry_id`, the chain lock and the append-only grant, and RWB-P7-E1008-APP serves the append (DP-03).
- The record library of RWB-PLT-E1027-CON is published: the record shape, the envelope, the idempotency key and the transaction rule, with its fake.
- The embedded Drools kit of RWB-PLT-E1072-CON is published: the compiler, the first-match evaluation and the scenario entry point the owning services use, with its fake. The `drools.kiebase.cache.max = 20` setting is the kit's and is not held here.
- RWB-P3-E1073-CON, contract version v1 (path `/api/recovery/case/v1/cases`), is published: the paged read of open case facts (product group, queue, region, exposure band and the deviation flag) with its error envelope and its fake. The operation is Not specified in the source documents (GAP-2458; ASM-4087).
- Parameters and lists are read through the platform clients of DP-06 and DP-07; `rules.testcases.min` is 50 (assumed in the legacy and not in any catalogue, GAP-2460; ASM-4089).
- The Blob container `rule-packages` exists with write and read rights for this login only, write-once objects and versioning on.
- The workflow kit, namespace `rwb-recovery` and task queue `rwb-decision` are provisioned, so JOB-20 can run as a Temporal Schedule (DP-10).
- RW-COE holds Rules and parameters C and RW-RISK holds Rules and parameters A; no one holds both (separation of duty), and RW-AUDIT holds R.
- The Drools XLS template is agreed: one workbook per package, a Rows tab and a Tests tab, RuleSet = package code, one row per rule with NAME = rule ID, and the default row last.
- Synthetic facts for the tests: package ALLOCATION "ALLOC-2026.11" in force with 24 rows, the draft "ALLOC-2026.12" with 26 rows and 50 scenarios, business date 2026-12-10.
- Build sequence: this slice builds against the platform contracts and the fakes of section 12.8; no dependency row changes (GAP-2437).

### 4. Flow

1. RW-COE fills the package workbook (Rows and Tests) for ALLOCATION, version `ALLOC-2026.12`, valid from 2026-12-15, with at least 50 scenarios.
2. RW-COE calls `POST /api/recovery/decision/v1/admin/rule-packages/ALLOCATION/versions` with the file, the valid-from date and an Idempotency-Key.
3. `RuleWorkbookParser` reads both tabs, keeps row numbers and the version label, and generates the DRL; an empty workbook is refused at this point.
4. `DroolsCompileCheck` compiles the generated DRL through the kit; a compile error refuses the load and names the row and the cell.
5. `RuleLoadValidator` runs the schema check against the lists, then overlap, unreachable rows and the default row.
6. `RuleScenarioRunner` runs at least `rules.testcases.min` scenarios (50) from the Tests tab through the evaluator contract and compares each result with its expected queue or outcome.
7. `RuleDryRun` asks RWB-P3-E1073-CON for the open case facts and counts the cases whose result would change, by product, queue and rule.
8. `RulePackageVersionService` refuses the load whole on any failed check, naming every failed row, cell or scenario; otherwise it stores the version LOADED with the Blob workbook, the DRL, the checksum, the test result and the dry-run counts, and appends the decision record in the same transaction.
9. RW-RISK approves through the approve operation; the call is refused when the approver is the author, and the version stays LOADED.
10. At 00:01 daily, JOB-20 starts the effective-date workflow: every APPROVED version whose valid-from date has arrived becomes IN_FORCE, the version it replaces becomes SUPERSEDED in the same transaction, and the announcement is published.
11. RW-COE calls rollback with a reason when a version is wrong; the previous version is in force again in one transaction, and the rollback is recorded with the reason.
12. Any time: the version list is read per package code, with state, dates, author, approver, checksum, test result and dry-run counts; the stored scenario set of an in-force version is served to the pipeline gate that asserts it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two rows match the same case at the same row order | Load refused; both row IDs named | MSG-P3-027 | AC2 |
| X2 | A scenario result differs from its expected result | Load refused; the failing scenario IDs named | MSG-P3-027 | AC4 |
| X3 | A required column is missing, or a value is outside its list | Load refused; row and column named | MSG-P3-027 | AC2 |
| X4 | A row can never match because an earlier row covers it | Load refused; the row named | MSG-P3-027 | AC2 |
| X5 | The allocation package has no default row | Load refused | MSG-P3-027 | AC2 |
| X6 | The generated DRL does not compile | Load refused; row and cell named; no version row and no Blob object | MSG-P3-027 | AC3 |
| X7 | The approver is the author | Approval refused; the version stays LOADED | MSG-P7-002 | AC6 |
| X8 | Rollback with no earlier version | Refused; the version stays in force | MSG-P3-015 | AC8 |
| X9 | The same package code and version label are already loaded | Refused with 409 | MSG-GEN-004 | AC3 |
| X10 | Valid from before today | Refused with 422 | MSG-GEN-003 | AC3 |
| X11 | An empty workbook | Refused with 422; no version row written | MSG-GEN-001 | AC3 |
| X12 | A role without Rules and parameters C, A or R calls a registry operation | Refused with 403; nothing changes | MSG-P4-002 | AC10 |
| X13 | Fewer scenarios than `rules.testcases.min` in the Tests tab | Load refused before any scenario runs | MSG-P3-027 | AC4 |

A refused load leaves the registry exactly as it was: no version row, no rule row, no test case and no Blob object, and the version in force stays in force. The compile check and the other MSG-P3-027 checks are raised by the owning service that loads the version in force; the message ID stays MSG-P3-027, the registry and its approval are P7 rwb-decision, and RWB-E1-073 keeps the run book. The {table} value of MSG-P3-027 is the package code and the {check} value is compile, schema, overlap, unreachable row, default row or scenario; the RFC 9457 detail names row IDs, cells or scenario IDs only — never a case fact and never a person.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Works on the four registry tables, the ledger append of RWB-P7-E1008-APP, the compiler of RWB-PLT-E1072-CON and the case-fact read of RWB-P3-E1073-CON; it changes no evaluator and no case |
| Negotiable | The checks are fixed; package codes, rows, scenarios, version labels and dates are data |
| Valuable | A rule change takes a load, an approval and a dated start instead of a release, and a wrong version leaves in one call |
| Estimable | One parser, one compile check, one validator, one scenario runner, one dry run, one version service, six endpoints, one Schedule |
| Small | Fits three weeks with its tests, as the secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one test in section 16, on workbook fixtures and the two contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Rule authoring, validation, test scenarios, approval and rollback in Drools

  Background:
    Given the loader U-41 holds Rules and parameters C and the approver U-51 holds Rules and parameters A
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows and a passing scenario set
    Given the business date is 2026-12-10

  Scenario: AC1 A valid workbook is stored LOADED with its workbook, DRL, checksum, test result and dry run (new, D-RCV-60)
    Given a workbook for package ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 scenarios that pass every check
    When U-41 loads it with valid from 2026-12-15 and U-51 approves it
    Then version "ALLOC-2026.12" is stored LOADED with source_blob_ref, the generated drl_source and checksum "9f2c...e1b4"
    Then test_result records "50 of 50 scenarios passed" and dry_run_counts records the open, changed, by-product, by-queue and by-rule counts
    Then the version is APPROVED with approver U-51 and approved_at, and version "ALLOC-2026.11" stays in force until 2026-12-15
    Then no code was released and no owning service was redeployed

  Scenario: AC2 The schema, overlap, unreachable-row and default-row checks refuse the load whole (new, D-RCV-60)
    Given rows "ALLOC-031" and "ALLOC-032" (test data) both match product group "MORTGAGE" and region "BKK" at row order 12
    Given the rwb-case contract mock returns the assignment-reason list without the value "QUICK", which row 9 carries
    Given row "ALLOC-040" (test data) matches product group "SSME" in any region at row order 5 and row "ALLOC-041" (test data) matches "SSME" and region "NE3" at row order 6
    Given the allocation rows have no last row that matches every case
    When validation runs on that one workbook
    Then the load is refused with 422 and MSG-P3-027 naming the overlap "ALLOC-031" and "ALLOC-032", row 9 and its column, the unreachable row "ALLOC-041" and the default row check
    Then no rule_package_version row, no rule_row, no rule_test_case and no Blob object is written
    Then version "ALLOC-2026.11" stays in force and one decision record holds the refusal with its failed checks

  Scenario: AC3 A compile error, an empty workbook, a repeated label and a past date are refused before anything is stored (new, D-RCV-60)
    Given the workbook for package ALLOCATION version "ALLOC-2026.14" has the condition cell "exposure_band >= " with no value at row 14
    When U-41 loads it
    Then the compile check fails and the load is refused with MSG-P3-027 naming row 14 and the cell
    Then no rule_package_version row is written and no Blob object is stored, and version "ALLOC-2026.13" stays in force
    When a file carrying version label "ALLOC-2026.12" for package ALLOCATION is loaded while "ALLOC-2026.12" is loaded
    Then the load is refused with 409 and MSG-GEN-004
    When U-41 loads a template with no rows
    Then the load is refused with 422 and MSG-GEN-001 for rows
    When U-41 loads version "ALLOC-2026.14" with valid from 2026-11-01 on 2026-12-10
    Then the load is refused with 422 and MSG-GEN-003 for valid from

  Scenario: AC4 At least 50 scenarios run through the same evaluator contract, and a failing scenario refuses the load (new, D-RCV-60)
    Given the 50 scenarios of the Tests tab with their expected queues
    Given scenarios "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO"
    When the scenario set runs through the evaluator contract of RWB-PLT-E1072-CON
    Then the load is refused with MSG-P3-027 naming "TA-07" and "TA-19"
    Then a Tests tab with fewer scenarios than the parameter rules.testcases.min is refused before any scenario runs; the value is read through the parameters contract of rwb-case
    Then every scenario runs through the same evaluator contract an owning service uses, and this service keeps no working memory afterwards

  Scenario: AC5 The dry run counts the open cases whose result would change, by product, queue and rule (new, D-RCV-60)
    Given the rwb-case contract mock returns the open cases with product group, queue, region, exposure band and the deviation flag
    When the draft "ALLOC-2026.12" is evaluated against every open case
    Then the dry-run report carries openCases, changedCases and counts by product, by queue and by rule
    Then those counts are written to dry_run_counts and are shown to the approver before the approval call
    Then the report holds counts and rule identities only: no case number, no amount and no other case fact is stored

  Scenario: AC6 The author cannot approve, and a different approver can (new, D-RCV-60)
    Given U-41 loaded version "ALLOC-2026.12"
    When U-41 calls approve on it
    Then the call is refused with 409 and MSG-P7-002 and the version stays LOADED
    When U-51, who loaded nothing, holds Rules and parameters A and calls approve on the same version
    Then the version is APPROVED with approver U-51 and approved_at, and one decision record holds the approval
    Then the author of a version is never its approver, and the check is in the service and not only on the screen

  Scenario: AC7 Every APPROVED version whose valid-from date has arrived is in force at 00:01 and is announced (new, D-RCV-60)
    Given version "ALLOC-2026.12" is APPROVED with valid from 2026-12-15 and version "ALLOC-2026.11" is in force
    When JOB-20, a Temporal Schedule in rwb-decision, runs at 00:01 on 2026-12-15
    Then "ALLOC-2026.12" is IN_FORCE and "ALLOC-2026.11" is SUPERSEDED in one transaction
    Then rwb.decision.RulePackageInForce.v1 (EV-30) is published on rwb.decision.events.v1 keyed by the package code
    Then a run on 2026-12-14 changes no state, and a version that is not APPROVED is never promoted

  Scenario: AC8 One rollback call returns the previous version, and open cases keep the version they were decided under (new, D-RCV-60)
    Given version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it
    When U-41 calls rollback once for version 7 with a reason
    Then version 6 is in force and version 7 is ROLLED_BACK, in one transaction
    Then the decision record holds U-41, the time and the reason
    Then a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision log entry
    Given package TRANSFER holds only version "TRF-2026.11"
    When rollback is called for "TRF-2026.11"
    Then the call is refused with 409 and MSG-P3-015 and "TRF-2026.11" stays in force

  Scenario: AC9 Every load, refusal, approval, promotion and rollback is one hash-chained decision record (new, D-RCV-60)
    Given a load, a refusal, an approval, a promotion and a rollback of package ALLOCATION in one week
    When each state change completes
    Then each has exactly one decision_log_entry whose chain_seq, prev_hash and entry_hash hold in sequence
    Then the entries carry the author, the approver, the time, the checksum, the test result and the package version identity
    Then no entry holds a case fact, a customer name or the workbook content
    Then a repeated call with the same Idempotency-Key, or a retried approval, adds no second entry

  Scenario: AC10 A role without Rules and parameters C, A or R is refused with 403 and nothing changes (new, D-RCV-60)
    Given RW-CASEOWN holds no Rules and parameters right on the registry
    When RW-CASEOWN calls a registry operation of rwb-decision
    Then the call is refused with 403 and MSG-P4-002 and nothing changes

  Scenario: AC11 A role holding none of Rules and parameters C, A or R is refused on every registry operation with 403 and nothing changes (new, D-RCV-60)
    Given RW-CASEOWN holds none of Rules and parameters C, A or R on the registry
    When RW-CASEOWN calls any registry operation of rwb-decision
    Then the call is refused with 403 and MSG-P4-002 for each operation and nothing changes

  Scenario: AC12 The provided operations answer 401 without a valid login and 404 for an unknown package, with 403 as in AC10 and AC11 (new, D-RCV-60)
    Given a caller with no valid login
    When the caller calls a provided registry operation
    Then the call is refused with 401 and nothing changes
    Given a caller holding Rules and parameters R
    When the caller calls the version list of a package code that is not in the registry
    Then the call is refused with 404 and the message Not specified in the source documents (NEWAC-RWB-P7-E1073-APP-AC17)
```

The nine criteria AC1 to AC9 are new and test only this deliverable, with the legacy values copied unchanged; AC10 is new and tests the access refusal of X12 in this deliverable. The legacy criteria of RWB-E1-073 are owned across services: the case-side dry-run facts and the run of a package belong to rwb-case (RWB-P3-E1073-APP and RWB-P3-E1073-CON), the evaluator and its 300 ms budget to the owning service through RWB-PLT-E1072-CON, the lists to their owners under DP-07, and the cross-service proof to RWB-ITG-E1073-ITG. The legacy test cases this story answers are listed in section 16. The five legacy operations and their authority checks run in rwb-decision, as the Ownership Map gives them, and the rights stay rows of the rwb-access role model. The registry, its versions, the four-eyes approval and the rule package endpoints are owned by P7 rwb-decision, and the embedded Drools kit RWB-PLT-E1072-CON is owned by PLT. AC11 and AC12 are new and test the access refusal of X12 for any registry operation and the 401 and 404 answers of the provided operations.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A version passes the compile, schema, overlap, unreachable-row, default-row and scenario checks before it is stored; the dry run is recorded for the approver | REQ-CWC-014; D-RCV-36 T4 |
| BR2 | A load with any failed check is refused in full: no version row, no rule row, no test case and no Blob object | Reference data change process step 3; CTL-08 |
| BR3 | First match: RuleSet = package code, one row per rule with NAME = rule ID, rows share one activation group, salience comes from row order, the default row is last, and exactly one row decides | D-RCV-36 T5 |
| BR4 | The allocation package always has a default row | REQ-CWC-008 |
| BR5 | A version takes effect on its valid-from date after approval; open cases keep the version they were decided under | R-UNI-38 |
| BR6 | The author cannot approve; RW-RISK signs rule package changes, and the service checks it | Separation of duty table; CTL-08 |
| BR7 | Rollback returns the previous version in one call and one transaction, with a reason | REQ-CWC-013; FEAT-CWC-15 |
| BR8 | Every load, refusal, approval, promotion and rollback is one decision record with author, approver, time, checksum and test result | REQ-CWC-013; FSD A2.14; DP-03 |
| BR9 | The template is the Drools XLS decision-table format, one workbook per package with Rows and Tests tabs; the generated DRL is stored with the workbook and its SHA-256 | D-RCV-36 T3, T4 |
| BR10 | A load carries at least `rules.testcases.min` scenarios (50, assumed) from the Tests tab, and every scenario runs through the same evaluator contract as production | REQ-CWC-014; D-RCV-36 T4 |
| BR11 | Only a version in force is ever served to an owning service or handed to the pipeline gate, and only when its recomputed SHA-256 matches the recorded one | DP-04; ADR-017 |

How the rules hold in `rwb-decision`: BR1, BR2 and BR10 run in the pipeline of one call, so a refused check writes nothing. BR3 is the workbook template and the generated DRL, and the service never reorders a row. BR4 is a check on the ALLOCATION package and is a row of the workbook, not a constant. BR5 and BR7 run in two transactions: the promotion at 00:01 and the rollback, each moving two version rows and appending one record. BR6 runs before the state moves, on the stored author. BR8 runs in the ledger append of RWB-P7-E1008-APP, in the same transaction as the state change. BR9 runs in the parser, which stores the workbook and the DRL together. BR11 runs in the serving read, which recomputes the checksum and refuses a version that is not in force.

### 9. State transitions

None for a case: this story changes no case status (TSD P7 T4, "No case state machine of its own"). It moves a rule package version.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | LOADED |
| None | Load | Any check fails, including the compile | REFUSED |
| LOADED | Approve | The approver holds Rules and parameters A and is not the author | APPROVED |
| LOADED | Approve | The approver is the author | No change; refusal recorded |
| APPROVED | JOB-20 at 00:01 | The valid-from date has arrived | IN_FORCE; the previous version SUPERSEDED |
| IN_FORCE | Rollback | An earlier version exists and a reason is given | ROLLED_BACK; the earlier version IN_FORCE |
| IN_FORCE | Rollback | No earlier version exists | No change; refusal recorded |
| Any state | Any operation | The caller's role holds no right for it | No change; refusal recorded |

Every arrow is one transaction and one decision record. A version in force is never edited: a correction is a new load with a new label, and a rollback moves the pointer and writes the reason.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a package version and calls rollback (Rules and parameters C) |
| RW-RISK, risk and model risk officer | Approves a version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT, internal audit | Reads versions, scenario results, dry-run counts and the decision records (R) |
| RW-REFADM, reference data administrator | Prepares load files; may not approve |
| RW-PLATADM, platform administrator | Operates JOB-20 and reads the promotion result and the incidents |
| SY-RULES, rules component | Runs the compile and the scenarios through the published evaluator contract on request |
| SY-CASEWF, case workflow module | Applies the approved version in its own service; holds no endpoint right here |
| RW-TRIBE, tribe lead and squad members | Runs the pipeline gate against the stored scenario set; no production data in a build |
| No delegation of authority level applies | A rule package version is not a credit decision |

The role codes are rows of the role model in `rwb_access` (TSD P7 T6.1) and are not fixed in code. DP-08 is not in this slice's pattern set: the authorisation decision is the cached permission decision the service template holds from rwb-access, and the refusal shapes are 401 without a session and 403 with MSG-P4-002 for a role without the right. Each REST operation calls the rwb-access authorise check before the state moves; its name is Not specified in the source documents (DOR-RWB-P7-E1073-APP-6).

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-REF-274 to DF-REF-278 | rule_package | all fields | Read |
| DF-REF-279 to DF-REF-295 | rule_package_version | id, package_id, version_label, status, source_blob_ref, drl_source, checksum, valid_from, valid_to, author, approver, loaded_at, approved_at, test_result, dry_run_counts, rollback_of | Write |
| DF-REF-296 to DF-REF-298, DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054 | rule_row | package_version_id, drools_rule_name, outputs, the rule fields, rule_table, row_order, target_queue_code | Write |
| DF-REF-185 to DF-REF-197, DF-REF-299 | rule_test_case | all fields, package_version_id | Write |
| DF-DEC-001, DF-DEC-003, DF-DEC-012, DF-DEC-016, DF-DEC-030 | decision_log_entry | id, decision_code, final_call, decided_at, actor_user_id | Write, through the ledger of RWB-P7-E1008-APP |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id, rule_version (the package identity: label and version label) | Write |
| DF-DEC-008 | decision_log_entry | inputs_ref (the workbook reference and the dry-run report reference) | Write |
| DF-DEC-014, DF-DEC-015 | decision_log_entry | actions (check results, test result, counts), outcome (the state reached) | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-031 | decision_log_entry | prev_hash, entry_hash, chain_seq, idempotency_key | Write |
| DF-CAS-003, DF-CAS-010, DF-CAS-012, DF-CAS-015, DF-CAS-019 | through the rwb-case contract of RWB-P3-E1073-CON | product group, queue, region, exposure band, deviation flag | Read only, for the dry run; never stored |

Field IDs are those of the Logical Data Model and Data Dictionary and legacy section 11. `rule_package_version.change_checklist` (DF-REF-295) is written by RWB-P7-E2041-APP before an approval, not here. No case fact is stored in `rwb_decision`: the dry run reads them, counts them and writes counts only (DP-01). The physical columns of the four registry tables are Not specified in the source documents (GAP-2457; ASM-4086).

### 12. Contract

The base is `/api/recovery/decision/v1` (DP-13), the topic is `rwb.decision.events.v1` (DP-14), the task queue is `rwb-decision` and the schema is `rwb_decision`.

#### 12.1 REST operations provided

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| POST | `/admin/rule-packages/{packageCode}/versions` | Load a package version: multipart workbook, valid-from date, Idempotency-Key; answers the version LOADED or REFUSED | Rules and parameters, right C |
| GET | `/admin/rule-packages/{packageCode}/versions` | List the versions of a package with state, dates, author, approver, checksum, test result and dry-run counts; query `status` | Rules and parameters, right R |
| GET | `/admin/rule-packages` | List the packages of the registry with their version in force | Rules and parameters, right R |
| POST | `/admin/rule-package-versions/{versionId}/approve` | Approve a LOADED version, with Idempotency-Key; refused when the caller is the author | Rules and parameters, right A |
| POST | `/admin/rule-package-versions/{versionId}/rollback` | Return an earlier version to force, with `{ reason }` and Idempotency-Key; refused when none exists | Rules and parameters, right U |
| GET | `/admin/rule-package-versions/{versionId}/dry-run` | The stored dry-run report; query `onDate` (default today) | Rules and parameters, right R |

These are the five operations of legacy section 12 with the per-service base of DP-13, plus the package list the registry needs to be readable as a registry. The refusal shapes are 401, 403 with MSG-P4-002, 404 for an unknown package code, version or dry-run report, 409 for a repeated label (MSG-GEN-004), a foreign approver (MSG-P7-002), a wrong state (MSG-GEN-004) or no earlier version (MSG-P3-015), 422 for a failed check (MSG-P3-027), an empty workbook (MSG-GEN-001) or a date order (MSG-GEN-003), and 503. A repeat of the load is refused on the package code and the version label, an approval on the version ID, and a rollback on the `Idempotency-Key` header.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | rwb-case (P3), under RWB-P3-E1073-CON | The paged open case facts of the dry run: product group, queue, region, exposure band and the deviation flag | One hop, 2 s (DP-11) |

The read is paged and filtered by status, so a dry run over the open book is bounded and resumable. The operation is Not specified in the source documents (GAP-2458; ASM-4087). The parameters of the platform client (DP-06) and the lists of the reference-data client (DP-07) are library reads of the service template and are not counted here.

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| rwb.decision.RulePackageInForce.v1 | `rwb.decision.events.v1` | The package code | Kafka Catalog v1 EV-30 fields: versionid, packagecode, packageversion, validfrom, approvedby; identifiers and facts only |

#### 12.4 Events consumed

None. The registry is fed by its own endpoints and by its Schedule; no other service pushes a rule change into it.

#### 12.5 Workflows and activities

| Name | Kind | Queue | What it does |
|---|---|---|---|
| RulePackageEffectiveDateWorkflow | Workflow | `rwb-decision` | Starts at 00:01, reads the versions due that night, promotes each and asks the activity to announce it |
| PromoteDueRulePackageVersions | Activity | `rwb-decision` | Moves each APPROVED version whose valid-from date has arrived to IN_FORCE, supersedes the version it replaces, appends the decision record and writes the outbox row in one transaction |

#### 12.6 Schedules

| Job | When | Queue | Mechanism |
|---|---|---|---|
| JOB-20 Rule promote | 00:01 daily, Asia/Bangkok | `rwb-decision` | Temporal Schedule starting RulePackageEffectiveDateWorkflow (DP-10) |

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `rule_package` | P7 (rwb_decision) | The package registry: one row per package code |
| `rule_package_version` | P7 (rwb_decision) | The version and its state, workbook reference, DRL, checksum, dates, author, approver, test result and dry-run counts |
| `rule_row` | P7 (rwb_decision) | The parsed rows of a version, written on a load and read for the model and the gate |
| `rule_test_case` | P7 (rwb_decision) | The parsed scenarios of a version, with their expected queue or outcome |
| `decision_log_entry` | P7 (rwb_decision), appended through RWB-P7-E1008-APP | One entry per state change of a version |
| `approval` | P7 (rwb_decision) | Not written by this story: a rule package version is approved by its own state (RWB-P7-E2013-APP) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |
| Blob container `rule-packages` | P7, path `{packageCode}/{versionLabel}.xlsx` | The workbook as a write-once claim-check behind `source_blob_ref` |

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case contract fake (RWB-P3-E1073-CON) | The paged open-case fact read | A page of open cases with product group, queue, region, band and the deviation flag; an empty page; a not-found; a slow answer past 2 s |
| Drools kit fake (RWB-PLT-E1072-CON) | The compiler and the scenario entry point | A workbook that compiles; the row-14 condition cell with no value; a scenario set whose `TA-07` and `TA-19` return `MTG-CEN-CO` instead of `MTG-BKK-CO` |
| Decision-record fixture (RWB-PLT-E1027-CON) | The record envelope | One record per state change; a duplicate call with the same Idempotency-Key |
| Reference-data client stub (DP-07) | The lists of the schema check | The assignment-reason list with and without the value `QUICK` |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 6 provided, 1 consumed | The six registry operations on `/api/recovery/decision/v1`; one 2 s hop for the dry-run case facts |
| Kafka | 1 published, none consumed | `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`, keyed by the package code |
| Temporal | 1 Schedule, 1 workflow, 1 activity | JOB-20 at 00:01 on queue `rwb-decision`; RulePackageEffectiveDateWorkflow and PromoteDueRulePackageVersions |
| File | 1 read, 1 write | The xlsx workbook uploaded and parsed; the workbook and the DRL stored in Blob and read back for the checksum |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, modules `rulepackage` (registry, store, states) and `rulepackageadmin` (the six endpoints). The legacy story put the controller in the access module's package `recovery.accessadmin.rulepackages` and the checks in `recovery.casewf.rules`; the Ownership Map gives these operations to P7, so the whole path sits here (GAP-2461; ASM-4090).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleWorkbookParser | Service | Reads the Rows and Tests tabs, keeps row numbers, reads the version label, generates the DRL; refuses an empty workbook |
| DroolsCompileCheck | Service | Compiles the generated DRL through the kit and reports the row and cell of a compile error |
| RuleLoadValidator | Service | Schema, overlap, unreachable-row and default-row checks, each naming its rows and cells |
| RuleScenarioRunner | Service | Runs at least `rules.testcases.min` scenarios through the evaluator contract and compares each expected result |
| RuleDryRun | Service | Reads the open case facts through RWB-P3-E1073-CON and counts the cases whose result would change, by product, queue and rule |
| RulePackageVersionService | Service | Stores the version LOADED with the Blob workbook, DRL, checksum, test result and counts; the approval check; the promotion and the rollback in one transaction each; the record append |
| RulePackageController | Controller | The six operations of section 12, with the refusal shapes and the problem responses |
| RulePackageEffectiveDateWorkflow | Schedule workflow | Runs at 00:01, promotes the versions due and publishes the announcement |

**Database and migrations**

- Writes `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case`; reads `decision_log_entry` through the ledger append and writes no row of it directly.
- The load writes a version, its rows and its scenarios in one transaction; the promotion and the rollback each update two version rows in one transaction.
- Per-service migration of DP-15: `V1073_1__rule_package_registry.sql` adds the unique key on package and version label, the index on state and valid-from for the 00:01 read, and the index on package and loaded_at. No row is seeded and no other schema is touched.
- Blob: container `rule-packages`, path `{packageCode}/{versionLabel}.xlsx`, write-once with the checksum in the object metadata.

**Configuration and reference data**

- No business value is written in code: package codes, rows, conditions, target queues, scenarios and the test count are data.
- `rules.testcases.min` is read as a parameter through the client of DP-06; 50 stands as assumed (GAP-2460; ASM-4089).
- The schema-check lists come through the reference-data client of DP-07; the lists used by the legacy story through the old P4 list interface are now rows of that contract.
- Two settings only: the 00:01 time of the Schedule and the Blob container name.
- The legacy feature flag `rwb.p3.drools` becomes a row of the platform flag library (R5.3 default ruling), not a property in code: off, the six operations answer 404 and JOB-20 does not run, and no version changes state.

**Build steps**

1. `RuleWorkbookParser` with a valid file, an empty file and a missing Tests tab; tests for AC1 and AC3.
2. `DroolsCompileCheck` with the row-14 condition cell; test for AC3.
3. `RuleLoadValidator`: the schema check against the lists, then overlap and unreachable rows, then the default row; test for AC2.
4. `RuleScenarioRunner` through the evaluator contract, with the scenario count guard and the two failing scenarios; test for AC4.
5. `RuleDryRun` against the case-fact fake, with counts by product, queue and rule written to `dry_run_counts`; test for AC5.
6. `RulePackageVersionService`: store, Blob, checksum, approval with the author check, the repeated label and the past date; tests for AC1, AC3, AC6 and AC9.
7. The workflow and JOB-20 with the promotion, the supersede, the announcement and the rollback; tests for AC7 and AC8.
8. The six endpoints with their access checks; component tests TC-E1-073-16 to TC-E1-073-20.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P3-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no build dependency of its own (metadata "Depends on (build)" = None) and builds against the `rwb_decision` baseline, the ledger of RWB-P7-E1008-APP and the RWB-P3-E1073-CON fake. The platform H rows and the C rows above are the dependencies the patterns add; they are held by the platform and contract stories and are not repeated in the metadata rows, which name the one contract dependency of the legacy key. DP-01, DP-13, DP-14 and DP-15 are the target shape itself: own schema, own base, own topic and own migration, with the workbook in Blob and no table of another service read. DP-04 is the split: the kit is embedded here only to compile and to run scenarios, and the owning services hold the evaluation. DP-03 is the record: one append per state change, with no second writer. DP-10 replaces the Quartz effective-date job with a Schedule and no `job_catalog` row. DP-05, DP-06 and DP-07 are prohibitions: no ACE view, no parameter and no list value in this service's code. DP-11 is the one 2 s hop of the dry run. DP-19 is the gateway-bff route behind the version list, which serves no screen of its own until Epic 8.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E1073-CON and RWB-PLT-E1072-CON stay green, and a SIT week shows a load refused whole on each check, a version approved by a foreign approver, a version in force at 00:01 with its announcement, one rollback in one call, and one decision record per state change with an unbroken chain.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A package version check fails | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Empty workbook or no rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | The version label is already loaded, or the version is not in the state the call needs | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | The caller's role holds no right for the operation | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {table} value is the package code and the {check} value is compile, schema, overlap, unreachable row, default row or scenario; the RFC 9457 detail names the row IDs, cells or scenario IDs only — never a case fact and never a person. For MSG-P3-015 the {table} value is the package code. For MSG-P4-002 the {action} value is "load a rule package version", "approve a rule package version", "roll back a rule package version" or "read the rule packages". Every error is an RFC 9457 problem response with `messageId` and `detail` filled; the reads answer 401 without a session, 403 for a role without the right, 404 for an unknown package code or version, and 503 with the same problem shape when the registry or the Blob store is unavailable.

SCR-39 states: empty and loading, the Empty and Loading wording of the version list below; error, the 503 problem shape above; no access, the 403 MSG-P4-002 refusal above.

Personal data: no case fact, customer name or person's name is carried in a rule package version; the fields classed as personal data in P2 are Not specified in the source documents (DOR-RWB-P7-E1073-APP-11).

### 15. Screens and states

No new screen. Rule packages are loaded by file and read through the version list read; the administration screen SCR-39 Rules and parameters comes in Epic 8 ("by file load before"), through the gateway-bff composite route (DP-19). The version list shows the state LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK or REFUSED, with the valid-from date, the author, the approver, the checksum and the test result, and its states are Loading, Results, Empty ("No versions of this package."), Error with the problem text and No access, whose wording is Not specified in the source documents (CG-ALL-7031). The dry-run report is shown to the approver as counts by product, queue and rule before the approval call. The rule change audit report is RWB-P7-E2041-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-073-01 | AC1, BR1, BR5, BR8 (legacy AC1): a valid workbook is stored LOADED and then APPROVED, and takes effect on its date | End to end | ALLOCATION version with 26 rows, 50 passing scenarios and checksum `9f2c...e1b4`; valid from 2026-12-15 |
| TC-E1-073-02 | AC2, BR3 (legacy AC2): the overlap check refuses the load and names both rows | End to end | Rows `ALLOC-031` and `ALLOC-032` at row order 12, product group `MORTGAGE`, region `BKK` |
| TC-E1-073-03 | AC4, BR1, BR10 (legacy AC3): the scenario check refuses the load and names the failing scenarios | End to end | Scenarios `TA-07` and `TA-19` expecting `MTG-BKK-CO` with rows returning `MTG-CEN-CO` |
| TC-E1-073-04 | AC8, BR5, BR7 (legacy AC4): one rollback call returns the earlier version and the entry keeps the old label | End to end | Versions 6 and 7: `ALLOC-2026.12` and `ALLOC-2026.13`; a case allocated under version 7 |
| TC-E1-073-05 | AC2, BR1 (legacy AC5): the schema check refuses a value outside its list | End to end | Row 9 with assignment reason `QUICK`; the list from the reference-data stub |
| TC-E1-073-06 | AC2, BR1 (legacy AC6): the unreachable-row check refuses the covered row | End to end | Rows `ALLOC-040` (order 5) and `ALLOC-041` (order 6, region `NE3`) |
| TC-E1-073-07 | AC2, BR4 (legacy AC7): the default-row check refuses a package with no default row | End to end | ALLOCATION rows with no last row matching every case |
| TC-E1-073-08 | AC6, BR6 (legacy AC8): the author cannot approve and the version stays LOADED | End to end | U-41 loads `ALLOC-2026.12` and calls approve; U-51 then approves it |
| TC-E1-073-09 | AC8, BR7 (legacy AC9): rollback with no earlier version is refused | End to end | Package TRANSFER with only `TRF-2026.11` |
| TC-E1-073-10 | AC3 (legacy AC10): the same package and label loaded twice is refused | End to end | Version label `ALLOC-2026.12` loaded twice; 409 MSG-GEN-004 |
| TC-E1-073-11 | AC3 (legacy AC11): valid from before today is refused | End to end | Valid from 2026-11-01 loaded on 2026-12-10; 422 MSG-GEN-003 |
| TC-E1-073-12 | AC3 (legacy AC12): an empty workbook is refused | End to end | Template with no rows; 422 MSG-GEN-001 |
| TC-E1-073-13 | AC3, BR1, BR9 (legacy AC13): a compile error refuses the load with no version row and no Blob object | End to end | Condition cell `exposure_band >= ` with no value at row 14, version `ALLOC-2026.14`; `ALLOC-2026.13` stays in force |
| TC-E1-073-14 | AC4, BR10, BR11 (legacy AC14): the pipeline gate fails on a scenario of an in-force version | Component | Fact mapping changed so `TA-07` returns `MTG-CEN-CO`; `ALLOC-2026.13` in force with 50 scenarios |
| TC-E1-073-15 | AC1, AC9, BR8, BR9 (legacy AC15): the checksum is on the version, in the Blob metadata and in the record | End to end | Workbook `ALLOCATION-2026.12.xlsx`; SHA-256 `9f2c...e1b4`; a later download compared |
| TC-E1-073-16 | AC2, AC3, BR2: RW-CASEOWN calls the load and is refused with no version row written (legacy access case) | Component | RW-CASEOWN calls `POST /admin/rule-packages/ALLOCATION/versions`; 403 MSG-P4-002 |
| TC-E1-073-17 | AC1: RW-CASEOWN calls the version list and is refused (legacy access case) | Component | RW-CASEOWN calls `GET /admin/rule-packages/ALLOCATION/versions`; 403 MSG-P4-002 |
| TC-E1-073-18 | AC6, BR6: RW-COE calls approve without Rules and parameters A and is refused (legacy access case) | Component | RW-COE holds C only; 403 MSG-P4-002; the version stays LOADED |
| TC-E1-073-19 | AC8, BR7: RW-RISK calls rollback without Rules and parameters U and is refused (legacy access case) | Component | RW-RISK holds A only; 403 MSG-P4-002; the version stays in force |
| TC-E1-073-20 | AC5: a role without Rules and parameters R calls the dry run and is refused (legacy access case) | Component | A role holding no R on Rules and parameters; 403 MSG-P4-002 |
| TC-E1-073-21 | AC1, AC7 (contract): the operations, the events and the activities of section 12 hold the published contract | Component | Base `/api/recovery/decision/v1`; topic `rwb.decision.events.v1`; task queue `rwb-decision`; schema `rwb_decision` |
| TC-E1-073-22 | BR2 (boundary, ASM-3438): this story writes only the tables of section 12.7 it owns and does not write approval | Component | Tables of section 12.7 with owner P7 (rwb_decision); `approval` not written by this story |
| TC-E1-073-23 | AC10: a role without Rules and parameters C, A or R is refused on a registry operation with 403 and nothing changes | Component | A role holding no C, A or R on Rules and parameters; 403 MSG-P4-002 |
| TC-E1-073-24 | AC11: a role holding none of Rules and parameters C, A or R is refused on every registry operation with 403 and nothing changes | Component | RW-CASEOWN calls a registry operation of rwb-decision; 403 MSG-P4-002 |
| TC-E1-073-25 | AC12: a call with no valid login is refused with 401, and a version list of an unknown package code with 404 | Component | No valid login on a registry operation; unknown package code; 401 and 404 messages Not specified in the source documents (NEWAC-RWB-P7-E1073-APP-AC17) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end and Access to Component. Every legacy test case of RWB-E1-073 is listed above. The `-ITG` copies belong to RWB-ITG-E1073-ITG, which proves the same values across rwb-decision, rwb-case and the owning services end to end.

### 17. Guardrails

- No business value in code: rows, conditions, target queues, scenarios, package codes and the test count are data. No rule form, prefix, queue code or 50 appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests: a scenario uses synthetic case facts, the dry run reports counts only, and the workbook holds rule values and no customer record.
- No cross-schema read (DP-01): `rwb_decision` reads no `rwb_case` table and no table of another service, and the dry-run facts arrive through the contract of RWB-P3-E1073-CON.
- ACE data only through the owner's contract or `v_ace_*` views, and this service reads neither.
- One evaluator for the compile, the scenarios, the dry run and production: the same kit contract, and no second engine in this service.
- The approver is never the author: the service checks it, not only the screen.
- A version in force is never edited: a correction is a new load, and a rollback moves the pointer and writes the reason.
- The pipeline gate reads the stored scenario set and a Testcontainers database; it never connects to SIT, UAT or PROD and never writes a live registry.
- No topic name is typed in code (DP-14), and the announcement is keyed by the package code.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14, FEAT-CWC-15 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-08, TC-E1-073-09, TC-E1-073-10, TC-E1-073-11, TC-E1-073-15 |
| REQ-CWC-014 | Schema, overlap, unreachable, default, compile and scenario checks | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | None | TC-E1-073-02, TC-E1-073-03, TC-E1-073-05, TC-E1-073-06, TC-E1-073-07, TC-E1-073-12, TC-E1-073-13, TC-E1-073-14 |
| REQ-DRI-004 | Epic 1 records for case creation, assignment and transfer use versioned rules | Epic 1, 3.3; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38 | TC-E1-073-01, TC-E1-073-04, TC-E1-073-15 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-41 | TC-E1-073-07 |

FEAT-CWC-14, FEAT-CWC-15 and FEAT-DRI-07 are carried by the case module and by the rules component; this slice answers them for the registry that holds and releases each version.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-073; story RWB-P7-E1073-APP; contract RWB-P3-E1073-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| The 15 legacy criteria AC1 to AC15 and their values | Sections 7 (AC1 to AC9), 16; the split is recorded in section 19 |
| The five legacy endpoints under `/api/recovery/v1` | Metadata; section 12.1 (per-service base, DP-13) |
| Rule package version fields DF-REF-274 to DF-REF-299 | Section 11 |
| MSG-P3-027, MSG-P3-015, MSG-P7-002, MSG-GEN-001, MSG-GEN-003, MSG-GEN-004, MSG-P4-002 | Section 14, and the exception paths |
| Version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED | Sections 8 (BR5, BR7), 9, 15 |
| The Quartz effective-date job at 00:01 | Sections 4, 12.5, 12.6 (DP-10) |
| Blob container `rule-packages`, path `{packageCode}/{versionLabel}.xlsx` | Sections 3, 12.7, 13 |
| Synthetic values: U-41, U-51, `ALLOC-2026.12`, `TA-07`, `MTG-BKK-CO`, 50 scenarios, 2026-12-15 | Sections 3, 7, 16 |
| Legacy test cases TC-E1-073-01 to TC-E1-073-20 | Section 16 |

### 19. Out of scope

- The evaluator itself: the KieBase, first-match evaluation, the 300 ms budget and the LRU cache of 20 stay in the owning service through RWB-PLT-E1072-CON (DP-04).
- The case-side facts of the dry run: the open-case read, the case status, queue, owner and stage (RWB-P3-E1073-APP and RWB-P3-E1073-CON).
- The collection of the allocation records into the ledger and the serving of a compiled model to an owning service: RWB-P7-E1020-APP. JOB-20 described here is the one Schedule that moves any package version to in force.
- The change checklist and the rule change audit report (RWB-P7-E2041-APP), and the general ledger, its read and its chain check job (RWB-P7-E1008-APP, RWB-P7-E1027-APP).
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (RWB-P7-E2042-APP), and loading the other routing rules in later epics.
- The reference-data loads of queues and lists, which belong to their owners under DP-07.
- The administration screen for rule packages (Epic 8, FEAT-ADM-02) and the gateway-bff composite route behind it (DP-19).
- The wiring of the pipeline gate and its release manifest: the CI pipeline and the platform stories. This service serves the stored scenario set and the state the gate asserts against.
- The values of `rules.testcases.min` beyond the assumed 50 (GAP-2460; ASM-4089).
