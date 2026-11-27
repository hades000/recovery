# RWB-P3-E2042-APP Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2042-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P3-E2042-APP-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1073-APP |
| Depends on (build) | RWB-P3-E2042-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1073-APP |
| Contract dependencies | None |
| Contract version | v1 (path prefix /api/recovery/decision/v1) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P3-E2042-APP-22) |
| Integration dependencies | None |
| External dependencies | RWB-P3-E2042-INF, RWB-P3-E2042-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E2042-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 32 cross-document, 8 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH workbooks and their Tests tabs authored as write-once configuration artefacts in the `rule-packages` Blob container, and each version in force fetched from rwb-decision's `GET /rule-models/{packageCode}/{version}`, verified against its SHA-256, built into one KieBase per version (cache max 20) and swapped in atomically inside the EvaluateRules activity of rwb-case**, so that **every Epic 2 decision this service takes is made by an approved, dated package version that rwb-case holds only as an evaluated copy, and no workbook, DRL source or rule table is ever read by service code**.

### 2. Business rationale

Epic 2 rules lived in three places in the monolith: reference rule rows, the `payment_match_rule` table and the `BookingMatchRules` class. D-RCV-36 T10 retires the table, and D-RCV-36 T3 to T6 move authoring, testing and effective dating into one governance path. In the target that governance is central in rwb-decision (P7): the three package codes, their versions, their rule rows and their test cases are registry rows there, published as a model over REST and announced by RulePackageInForce (Arch v5 slides 27, 41 and 44; Temporal and Drools slides 15 and 16). Evaluation stays local to the owning service (Arch v5 slide 27), so rwb-case keeps only the evaluated copy: it authors the workbooks, fetches the model, verifies the checksum and swaps it in (DP-04).

This story is the rwb-case half of that split. It fixes the three authoring artefacts (38 rows and 62 scenarios for RESTRUCTURE, 3 rows and 58 scenarios for PAYMENT_MATCH, 21 rows and 54 scenarios for BOOKING_MATCH — 174 scenarios in all, every package at or above `rules.testcases.min` = 50), the model cache and its swap rule, the catalog read, and the schema assertion that `rwb_case` has no `payment_match_rule` table and no column of DF-REF-261 to DF-REF-273. It meets REQ-CWC-013 and REQ-CWC-014 and gives RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 one catalog row set to read, by rule ID and package version. No source names the rwb-comms package; it is Not specified in the source documents (GAP-2395). The PAYMENT_MATCH match order is the one the Drools design sets (GAP-3180), and this key carries the version label PMT-2026.12 valid from 2026-12-15; its reconciliation with the RWB-E2-027 value (PM-2026.12 valid from 2026-12-01) is open before SIT. The match rows live only in the PAYMENT_MATCH package and no match rule table is created.

The measure is that the three versions are fetched, verified and in force as evaluated copies, 174 scenarios pass in every build, and a migrated database holds 93 tables with no `payment_match_rule`.

### 3. Preconditions

- RWB-P3-E2042-CON is published: the authoring contract of the Rows and Tests tabs, the Blob naming and metadata contract, the five consumed rwb-decision operations, the RulePackageInForce consumption contract, the EvaluateRules activity contract and the contract fakes.
- RWB-P7-E2042-APP is done: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` in schema `rwb_decision`, the three package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH seeded with owner role RW-COE, and the admin operations that load, list, approve and roll back a version (ASM-0069).
- RWB-PLT-E1072-CON is published: the embedded Drools kit, with one KieBase per package version, first-match semantics, a cache of at most 20 versions, the checksum check and the `NoPackageInForce` outcome (DP-04).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the event-started workflow and the activity contracts of the kit (DP-10).
- RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the parameters contract and the reference-data contract of rwb-case, with the client library (DP-06, DP-07).
- RWB-PLT-E1047-CON and RWB-PLT-E1044-CON are published: the naming library and the per-service Flyway sequence (DP-14, DP-15). RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19).
- RWB-P3-E1073-APP is done: the rwb-case rule authoring pipeline — workbook template, compile, the load checks, the scenario runner, `RuleScenarioBuildGate` and the one-call rollback path.
- The three version labels are agreed on 16 November 2026: "RES-2026.12", "PMT-2026.12" and "BKG-2026.12", all valid from 2026-12-15 (the valid-from date is the legacy assumption and is copied unchanged). The scenario counts are agreed: 62, 58 and 54, all at or above `rules.testcases.min` = 50.
- The Blob container `rule-packages` exists, write-once, with the rwb-case workload identity holding read on that container only (RWB-P3-E2042-INF).
- The rwb-case login (DP-02) and the rwb-decision mTLS certificate are in the platform secret store; the per-service login name is Not specified in the source documents (GAP-0722; ASM-1269).

### 4. Flow

1. Center of excellence analyst: reads the current Epic 2 rules from the rwb-decision catalog, the retired `payment_match_rule` rows of the monolith and the `BookingMatchRules` behaviour, and writes one workbook per package in the Drools XLS decision-table template.
2. Center of excellence analyst: fills the Rows tab (RuleSet = package code, NAME = rule ID, default row last) and the Tests tab with 62, 58 and 54 scenarios; stores the workbook under `RESTRUCTURE/RES-2026.12.xlsx`, `PAYMENT_MATCH/PMT-2026.12.xlsx` and `BOOKING_MATCH/BKG-2026.12.xlsx` in the write-once container, with the SHA-256 in the object metadata.
3. Center of excellence analyst: loads each workbook through the rwb-decision admin operation `POST /admin/rule-packages/{packageCode}/versions` with valid from 2026-12-15; rwb-decision runs the compile, schema, overlap, unreachable row, default row and at least 50 scenario checks and its dry run.
4. Risk officer: approves each version through `POST /admin/rule-package-versions/{versionId}/approve`; the author cannot approve.
5. rwb-decision: the promotion Schedule JOB-20 runs at 00:01, moves each APPROVED version to IN_FORCE, and publishes `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` with the package code, the version label, the checksum and the valid-from date.
6. rwb-case: the case router consumes the event through its inbox (one action per event) and starts `RuleModelSwap` on task queue `rwb-case` for the package code and version label.
7. RulePackageClient: calls `GET /api/recovery/decision/v1/rule-models/{packageCode}/{version}` inside the `swapRuleModel` activity, compares the returned SHA-256 with the checksum in the event and with the metadata of the Blob object, and hands the model to the cache only on a match.
8. ModelCache: builds one KieBase for the package version, stores it against the package code, and swaps the pointer atomically so a running evaluation keeps the KieBase it started with; a version not in force is evicted least-recently-used when the cache is at its maximum of 20.
9. EvaluateRules activity: evaluates a package code on the facts and the business date and returns `RuleResult(packageCode, packageVersion, ruleId, outputs)`; the package version is the one in force on the business date, or the one the case was decided under (R-UNI-38).
10. RuleCatalogClient: answers the catalog read through `GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` for action_text, owner_role, timer_spec and outputs; rwb-case reads no rule row from a table.
11. Build: `RuleScenarioBuildGate` runs the 174 scenarios of the three in-force versions, and `PaymentMatchRuleAbsentCheck` asserts on a Testcontainers database that the migrated schema holds 93 tables, that no table named `payment_match_rule` exists, and that no column of DF-REF-261 to DF-REF-273 exists.
12. Any release migration that creates `payment_match_rule` fails the build; the migration script that drops a table left by an earlier DEV or SIT build runs before the gate.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The SHA-256 of the fetched model differs from the checksum in the event | The KieBase is not built and the pointer is not swapped; the model in force stays; the checksum mismatch is counted and alerted | None | AC1, AC6 |
| X2 | The model operation does not answer inside the 2 s budget, or answers 404 for the announced version | The swap retries on the activity retry policy; after the last attempt the model in force stays and the swap is alerted as failed | None | AC2, AC6 |
| X3 | No version is in force for a package on the business date | `NoPackageInForce` is raised; the activity fails without a retry and the caller reports MSG-P3-027; no default decision is taken | MSG-P3-027 | AC4, AC5 |
| X4 | The cache holds 20 versions and a further version is requested | The least recently used version that is not in force is evicted; a version in force is never evicted | None | AC1 |
| X5 | The same RulePackageInForce event arrives twice | The inbox drops the second event; no second fetch, no second swap and no second KieBase | None | AC3 |
| X6 | A release migration creates `payment_match_rule` | The schema gate fails and the build is blocked before the artefact is published | None | AC6 |
| X7 | Service code reads a workbook, a DRL source or a rule table directly | The architecture boundary test fails the build; the only reads allowed are the model operation, the catalog operation and the version list | None | AC5 |
| X8 | A catalog read names a rule ID or package version that is not held | The read answers 404 from rwb-decision; the caller records the missing rule ID for the package and takes no decision from a partial row | MSG-P3-027 | AC5 |
| X9 | A workbook holds fewer than 50 scenarios, or a scenario fails at load | The load is refused by rwb-decision with the failing scenario IDs named; no version is created and the version in force keeps running | MSG-P3-027 | AC1 |
| X10 | The Blob object is overwritten or its metadata checksum is missing | The write-once policy refuses the overwrite; a missing checksum stops the verification step and the swap is refused | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E2042-CON, the platform contract stories and RWB-P3-E1073-APP. The rwb-decision answers come from its contract fake; the registry itself is RWB-P7-E2042-APP |
| Negotiable | Rows, scenarios, package codes, version labels and the cache bound are data and configuration; the checksum rule, the atomic swap and the schema assertion are fixed |
| Valuable | Every Epic 2 rule this service evaluates comes from one approved, dated, checksum-verified package version, and `payment_match_rule` can never come back |
| Estimable | Three workbooks and their Tests tabs, one client, one cache, one swap workflow, one catalog client, one schema gate and one seed-free migration |
| Small | Fits two weeks with its tests |
| Testable | Each criterion is a cache test, a checksum test, a catalog test, a schema test on a Testcontainers database or a scenario run in the build |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages in Drools

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given the rwb-decision contract mock returns RW-COE as the owner role of the three packages and RW-RISK as the approver role
    Given package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE
    Given the rwb-decision contract mock returns package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH seeded with owner role RW-COE
    Given rules.testcases.min is 50 and the business date is 2026-12-10

  Scenario: AC1 RESTRUCTURE package (legacy RWB-E2-042 AC1)
    Given the rwb-decision contract mock returns package code "RESTRUCTURE" with version "RES-2026.12", 38 rule rows, 62 test cases and its checksum
    Given a RESTRUCTURE workbook version "RES-2026.12" with 38 rows and 62 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the compile, schema, overlap, unreachable row and default row checks pass
    Then the test result is "62 of 62 scenarios passed"
    When U-51 approves it
    Then version "RES-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds 38 rows under version "RES-2026.12", including R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC2 PAYMENT_MATCH package (legacy RWB-E2-042 AC2)
    Given the rwb-decision contract mock returns package code "PAYMENT_MATCH" with version "PMT-2026.12", 3 rule rows, 58 test cases and its checksum
    Given a PAYMENT_MATCH workbook version "PMT-2026.12" with 3 rows and 58 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the test result is "58 of 58 scenarios passed"
    When U-51 approves it
    Then version "PMT-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds the rows EXACT, WINDOW and PARTIAL under version "PMT-2026.12"

  Scenario: AC3 BOOKING_MATCH package (legacy RWB-E2-042 AC3)
    Given the rwb-decision contract mock returns package code "BOOKING_MATCH" with version "BKG-2026.12", 21 rule rows, 54 test cases and its checksum
    Given a BOOKING_MATCH workbook version "BKG-2026.12" with 21 rows and 54 scenarios
    When U-41 loads it with valid from 2026-12-15
    Then the test result is "54 of 54 scenarios passed"
    When U-51 approves it
    Then version "BKG-2026.12" is APPROVED and in force from 2026-12-15
    Then rule_row holds 21 rows under version "BKG-2026.12" and the comparison evaluator of RWB-E2-007 is no longer used

  Scenario: AC4 PAYMENT_MATCH keeps the priority order of RWB-E2-027 (legacy RWB-E2-042 AC4)
    Given the rwb-decision contract mock returns package code "PAYMENT_MATCH" version "PMT-2026.12" in force on 2026-12-15 with its checksum
    Given PAYMENT_MATCH version "PMT-2026.12" is in force on 2026-12-15
    When Not specified in the source documents (CG-ALL-4395) matches payments for that date
    Then the rows are tried in the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3
    Then payment "PAY-91008" of 12,500.00 THB that both EXACT and WINDOW match is decided by EXACT
    Then payment "PAY-91002" of 11,875.00 THB is decided by PARTIAL with a shortfall of 625.00 THB
    Then the decision log entry names rule "R-RES-26" and rule version "PMT-2026.12"
    Then the order matches RWB-E2-027 BR1 and its "PM-2026.12" row order

  Scenario: AC5 RESTRUCTURE rows feed RWB-E2-035 (legacy RWB-E2-042 AC5)
    Given the rwb-decision contract mock returns package code "RESTRUCTURE" version "RES-2026.12" in force on 2026-12-15, and rule row "R-RES-04" with action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days"
    Given RESTRUCTURE version "RES-2026.12" is in force on 2026-12-15
    When SY-RULES evaluates R-RES-04 for case "RW-2026-000777"
    Then RuleCatalog.row("R-RES-04", "RES-2026.12") returns action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days"
    Then every route-set row that RWB-E2-035 reads carries the three fields
    Then RWB-E2-035 sets the next action, the owner and the due date from these values

  Scenario: AC6 payment_match_rule is not created (legacy RWB-E2-042 AC6)
    Given a database migrated from empty with the release migrations on 2026-12-10
    When the schema check runs
    Then no table named payment_match_rule exists
    Then no column of DF-REF-261 to DF-REF-273 exists
    Then the table count is 93
    Then the build fails if any migration in the release creates payment_match_rule

  Scenario: AC7 rwb-case holds only evaluated copies and writes no rule governance rows (BR6, BR8, BR10, BR11, BR13) (new, D-RCV-60)
    Given rwb-case holds package "PAYMENT_MATCH" version "PMT-2026.12" in force on 2026-12-15
    When rwb-case builds the KieBase and stores it in the cache
    Then the RuleSet of the workbook is "PAYMENT_MATCH" and the version label is "PMT-2026.12"
    Then the cache keeps at most 20 KieBase instances, one per package version, and no KieBase is edited in place
    Then an open case keeps the package version it was decided under when a newer version reaches its valid-from date
    Given the fetched model for "PAYMENT_MATCH" version "PMT-2026.12" has a SHA-256 that differs from the announced checksum
    When rwb-case verifies the model before use
    Then the KieBase is not used, the last good model stays in force and the package is alerted
    Then no code in rwb-case writes rule_package, rule_package_version, rule_row or rule_test_case

  Scenario: AC8 an activity that is retried or times out does not record a decision (new, D-RCV-60)
    Given the EvaluateRules activity for case Not specified in the source documents (NEWAC-RWB-P3-E2042-APP-AC8) is started against package "RESTRUCTURE" version "RES-2026.12"
    When the activity fails and is retried
    Then the retry runs against the same package version and the case keeps its decided version
    When the activity exceeds its timeout
    Then the timed-out attempt is not recorded as a decision and the activity is retried

  Scenario: AC9 a status change the model does not allow is refused (new, D-RCV-60)
    Given package version "PMT-2026.12" is APPROVED and in force on 2026-12-15
    When a status change to a state that the model does not allow is requested for that version
    Then the change is refused and version "PMT-2026.12" stays APPROVED
    Then the refusal is recorded and no rule_row is changed
```

The six criteria above are the legacy criteria of RWB-E2-042 and they carry their values unchanged. The split is this: the three packages are governed and stored in rwb-decision, which owns `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the load and approve operations and the 00:01 promotion (ASM-0069; Arch v5 slides 41 and 44; Temporal and Drools slides 15 and 16). The registry, its seeding and JOB-20 are carried by RWB-P7-E2042-APP; AC1 to AC3 are proved here against the rwb-decision contract mock and in the real service by RWB-ITG-E2042-ITG (GAP-0721). rwb-case authors the three workbooks and their Tests tabs, fetches the model over `GET /rule-models/{packageCode}/{version}`, verifies the SHA-256, builds and swaps one KieBase per version and reads `rule_row` only through the catalog. Every statement above about a registry row, an approval or a version in force is therefore proved against the rwb-decision contract mock in this story, and re-proved against the real service by RWB-ITG-E2042-ITG. What this story owns and proves on its own artefacts is the write-once workbook, the checksum-verified model cache with its atomic swap and last-good-model rule, the catalog read, and the schema assertion that `rwb_case` never holds `payment_match_rule`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each Epic 2 package is authored in the Drools XLS decision-table template; the workbook is stored write-once in Blob `rule-packages`, and governance — load, checks, scenarios, approval, effective dating — is rwb-decision's only | D-RCV-36 T3, T4; ASM-0069 |
| BR2 | Each package version carries at least `rules.testcases.min` (50) scenarios, and every scenario passes before the version may be approved | REQ-CWC-014; D-RCV-36 T4 |
| BR3 | PAYMENT_MATCH has one row per match type, and the row order is EXACT then WINDOW then PARTIAL, as in RWB-E2-027 | R-RES-26; D-RCV-36 T10 |
| BR4 | RESTRUCTURE route-set rows carry action_text, owner_role and timer_spec; RWB-E2-035 reads them only from the catalog, by rule ID and package version | D-RCV-36 T6; FEAT-CWC-28 |
| BR5 | `payment_match_rule` is not created in `rwb_case`, and DF-REF-261 to DF-REF-273 stay retired; no code, rule row, migration or test reads or writes them | D-RCV-36 T10 |
| BR6 | The package code is the RuleSet of the workbook; the version labels are RES-, PMT- and BKG-yyyy.MM | D-RCV-36 T5 |
| BR7 | First match wins: exactly one row decides, and the default row is last | D-RCV-36 T5 |
| BR8 | An open case keeps the package version it was decided under when a newer version reaches its valid-from date | R-UNI-38 |
| BR9 | `RuleScenarioBuildGate` runs every in-force package's scenarios in every build | REQ-CWC-014; D-RCV-36 T4 |
| BR10 | rwb-case holds only an evaluated copy: one KieBase per package version, at most 20 in the cache, never recompiled per call and never edited in place | Arch v5 slide 27; DP-04; Temporal and Drools slide 16 |
| BR11 | The SHA-256 of the fetched model is verified against the announced checksum before the KieBase is used; on a mismatch or a failed build the last good model stays in force and the package is alerted | Arch v5 slides 11 and 27; DP-04 |
| BR12 | rwb-case reads no workbook, DRL source or rule table: the only reads are the model operation, the catalog operation and the version list | D-RCV-36 T3, T6; DP-04 |
| BR13 | No code in rwb-case writes `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case`; those rows are written by rwb-decision only | ASM-0069; DP-01 |

### 9. State transitions

This story changes no case status. It adds the model-cache states that rwb-case observes for a package version.

| From | Event | Condition | To |
|---|---|---|---|
| Not cached | RulePackageInForce, or the first evaluation of a package | The checksum verifies and the KieBase builds | In force (cached) |
| In force (cached) | RulePackageInForce for a newer version | The checksum verifies and the swap succeeds | New version in force (cached); the earlier version is kept until it is evicted or superseded |
| In force (cached) | RulePackageInForce for a newer version | The checksum does not verify, the model is not served, or the KieBase does not build | The earlier version stays in force; the failure is counted and alerted |
| In force (cached) | No version in force on the business date | The evaluation raises `NoPackageInForce` once | Unchanged; the caller reports MSG-P3-027 |
| In force (cached) | The cache is at its maximum of 20 | A version that is not in force is the least recently used | Evicted; a later event or evaluation caches it again |
| In force (cached) | A newer version becomes the one in force | The swap has succeeded | Superseded in the cache; still held while the cases decided under it are open |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Authors the three workbooks and their Tests tabs, and loads them through the rwb-decision admin operation |
| RW-RISK, risk and model risk officer | Approves a package version in rwb-decision; may not hold RW-COE, and the author cannot approve |
| The rwb-case service identity | Fetches the model, verifies the checksum, builds and swaps the KieBase, reads the catalog and evicts an unused version |
| SY-RULES, Drools evaluator | Evaluates the packages inside the EvaluateRules activity only |
| The build pipeline, no user role | Runs `RuleScenarioBuildGate` and `PaymentMatchRuleAbsentCheck` against a Testcontainers database; no SIT, UAT or PROD data |
| RW-AUDIT, internal audit | Reads the version list, the rule rows and the scenario results through the rwb-decision operations |
| No delegation of authority level applies | A rule package version is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| Not specified in the source documents (DOR-RWB-P3-E2042-APP-7) | Blob object `rule-packages` | package code, version label, SHA-256, author role, authored date, environment | Write, once; read on the swap |
| DF-REF-274 to DF-REF-278 | rule_package (P7) | id, package_code, title, owner_role, hit_policy | Read only, through the version list |
| DF-REF-279 to DF-REF-294 | rule_package_version (P7) | version label, status, source_blob_ref, checksum, valid_from, test_result, dry_run_counts | Read only; the checksum and the valid-from date are read on the swap |
| DF-REF-296 to DF-REF-298 | rule_row (P7) | package_version_id, drools_rule_name, outputs | Read only, through the catalog |
| DF-REF-008 | rule_row (P7) | action_text | Read, by RWB-E2-035 |
| DF-REF-010 | rule_row (P7) | owner_role | Read, by RWB-E2-035 |
| DF-REF-011 | rule_row (P7) | timer_spec | Read, by RWB-E2-035 |
| DF-REF-185 to DF-REF-197, DF-REF-299 | rule_test_case (P7) | test case, expected and actual result | Read only, through the version list |
| Not specified in the source documents (DOR-RWB-P3-E2042-APP-7) | Model cache (in memory) | package code, version label, checksum, KieBase, loaded at, hit count, last used at | Write and read, in memory only |

The four registry tables are rwb-decision's and this story writes none of their rows (ASM-0069; DP-01). No new field ID is added for the cache, which is in memory and holds no case data. `payment_match_rule` and DF-REF-261 to DF-REF-273 are retired and appear in this story only as the assertion that they do not exist. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None. This story serves no new business operation. The three package codes and their versions are read through rwb-decision's operations, and the model cache is internal to rwb-case; no cache read is published.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | rwb-decision (P7) | The compiled model, its version label and its SHA-256, on the swap and on a first evaluation (DP-04) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | rwb-decision (P7) | action_text, owner_role, timer_spec and outputs of one rule row by rule ID and package version (AC5) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | rwb-decision (P7) | The version list and the checksum of the version in force | One hop, 2 s (DP-11) |
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | rwb-decision (P7) | The multipart load of a workbook with validFrom; rwb-decision owns the operation, this story calls it (AC1 to AC3) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | rwb-decision (P7) | The four-eyes approval of a loaded version (AC1 to AC3) | One hop, 2 s (DP-11) |

The five operations are rwb-decision's; this story consumes them and never defines them. A checksum mismatch is carried in the model response and compared locally.

#### 12.3 Events published

None. The model swap records no decision and publishes no event. The local decision-record library of DP-03 is part of the build and publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` when a decision is taken in rwb-case; this story adds no event type to it.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 | Case router, inbox dedupe, `signalWithStart` of `RuleModelSwap` for the package code and version label; the swap fetches, verifies and swaps the model |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| RuleModelSwap | Workflow started by RulePackageInForce, workflow ID = `rule-model-swap-{packageCode}-{version}` | `rwb-case` | One swap per package code and version label: fetch, verify, build, swap, record the outcome |
| swapRuleModel | Activity | `rwb-case` | Calls the model operation, verifies the SHA-256, builds the KieBase and swaps the pointer atomically; keeps the last good model on failure |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Calls the embedded Drools kit with a package code, the facts and the business date; the only place a rule is evaluated (DP-04) |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record, the state change and the outbox rows in one transaction (DP-03) |

#### 12.6 Schedules

None. The 00:01 promotion is the Temporal Schedule JOB-20 in rwb-decision and is out of scope here (Arch v5 slide 44; the OPS story of this key). The swap is event-started, not scheduled.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | Read by the evaluation for the facts of the case; no column added |
| timer | P3 (rwb_case) | Read for the due dates a route-set row sets; no column added |
| queue | P3 (rwb_case) | Read for the target queue a rule row names; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects of the event consumer (DP-09) |

No table is created and no column is added by this story. `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are rwb-decision's and are never read directly (ASM-0069; DP-01). `payment_match_rule` does not exist.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock | The P7 contract | `GET /rule-models/{packageCode}/{version}` for RES-2026.12, PMT-2026.12 and BKG-2026.12 with their SHA-256, one answer with a wrong checksum and one 404; `GET /rule-catalog/{ruleId}?packageVersion=` for R-RES-04, R-RES-25, R-RES-26, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02; the version list; the load and approve answers 201, 409 and 422 |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Rules and parameters rights to RW-COE and RW-RISK and refusing a role without them |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 5 consumed | The model, the catalog, the version list, the load and the approve operations; one hop, 2 s timeout |
| Kafka | None published, 1 consumed | `rwb.decision.events.v1` for RulePackageInForce |
| Temporal | 1 workflow, 3 activities | RuleModelSwap; swapRuleModel, EvaluateRules, RecordAndApply |
| File | 3 configuration workbooks | The three xlsx workbooks and their Tests tabs, uploaded once per version and stored write-once; no runtime file exchange |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `rules`, Java package `th.co.scb.ace.workbench.recovery.case.rules.epic2`.

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
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Epic2PackageWorkbooks | Configuration | The three xlsx workbooks and their Tests tabs, owned by RW-COE, stored write-once with the SHA-256 in the object metadata |
| RulePackageClient | Client | Calls the model operation and the version list; compares the returned SHA-256 with the event checksum and the Blob metadata; never retries a checksum mismatch |
| ModelCache | Service | One KieBase per package version, at most 20 versions, least-recently-used eviction that never evicts a version in force, atomic pointer swap |
| RuleModelSwap | Workflow | One swap per package code and version label, started by RulePackageInForce through the inbox |
| SwapRuleModelActivity | Activity | Runs the fetch, the checksum check, the build and the swap, and records the outcome in logs and metrics |
| RuleCatalogClient | Client | Calls the catalog operation for action_text, owner_role, timer_spec and outputs by rule ID and package version |
| Epic2Evaluator | Service | The only caller of the embedded Drools kit inside the EvaluateRules activity; returns `RuleResult(packageCode, packageVersion, ruleId, outputs)` |
| PaymentMatchOrderCheck | Validator extension | BR3: one row per match type and the order EXACT, WINDOW, PARTIAL, checked at load in rwb-decision through the authoring pipeline of RWB-P3-E1073-APP |
| RestructureCatalogCheck | Validator extension | BR4: action_text, owner_role and timer_spec present on every route-set row, checked at load through the same pipeline |
| PaymentMatchRuleAbsentCheck | Schema gate | Fails the build when `payment_match_rule`, or any column of DF-REF-261 to DF-REF-273, exists in a migrated database |
| RuleScenarioBuildGate | Build gate (existing) | Runs the 174 scenarios of the three in-force versions |
| Epic2LoadRunbook | Run book | The load order, the approver, the valid-from date and the rollback for each package |

**Blob and migrations**

- Blob paths `RESTRUCTURE/RES-2026.12.xlsx`, `PAYMENT_MATCH/PMT-2026.12.xlsx` and `BOOKING_MATCH/BKG-2026.12.xlsx`; write-once, the SHA-256 in the object metadata, no public access (RWB-P3-E2042-INF).
- No migration creates `payment_match_rule`. One migration runs `DROP TABLE IF EXISTS payment_match_rule` with its indexes, for DEV and SIT databases created before D-RCV-36 T10, after the load runbook has archived the rows to a CSV. No migration in the release creates the table.
- No seed migration: the three package codes are rwb-decision rows, seeded by RWB-P7-E2042-APP (ASM-0069).
- The four registry tables rule_package, rule_package_version, rule_row and rule_test_case sit in schema rwb_decision under the P7 reading recorded here; the P3 and P4 declarations are not built here, and the P7 TSD is asked to add them at its next version (GAP-1301).
- The schema gate asserts 93 tables on a Testcontainers database migrated from empty.

**Configuration and reference data**

- The three workbooks and their Tests tabs (RW-COE), with version labels and the valid-from date 2026-12-15 copied from the legacy story.
- `rules.testcases.min` = 50 through the parameters contract of rwb-case (DP-06).
- The cache bound of 20 versions through the embedded Drools kit configuration (DP-04); the stories of this key never hard-code it.
- Harness values (repository, SIT environment, seeding set, evidence format and retention, pass or fail gate, fake response bodies) are held as data in the harness pack and agreed at the wave 2 entry check; Not specified in the source documents (GAP-0421) until then.

**Build steps**

1. Author the three workbooks and the 174 scenarios; store them write-once in Blob and record the SHA-256 in the metadata (AC1 to AC3, X9, X10).
2. RulePackageClient over the model and version operations, with the checksum comparison and the 404 answer; unit tests for X1, X2 and X8.
3. ModelCache with one KieBase per version, the bound of 20, the least-recently-used eviction and the atomic swap; tests for X1, X2 and X4.
4. RuleModelSwap and SwapRuleModelActivity, started by RulePackageInForce through the inbox with dedupe; tests for X3, X5 and X2.
5. RuleCatalogClient with the 2 s budget and the missing-row answer; tests for AC5 and X8.
6. Epic2Evaluator inside the EvaluateRules activity, returning the rule ID and the package version of the version in force and honouring R-UNI-38; tests for AC4 and AC5.
7. PaymentMatchOrderCheck and RestructureCatalogCheck wired into the authoring pipeline of RWB-P3-E1073-APP; tests for AC2, AC4 and AC5.
8. PaymentMatchRuleAbsentCheck and the table count assertion on a Testcontainers database; test for AC6.
9. Run `RuleScenarioBuildGate` over the three versions and add the lock manifest entries; test for AC1 to AC3.
10. Write the load runbook with the rollback step for each package.

**Feature switch.** The legacy flag name `rwb.p3.drools` is kept as the legacy reference; in the target the switch is a parameter read through the parameters contract. Off: the model cache loads nothing, the swap workflow does not start, and every evaluation returns `NoPackageInForce` with MSG-P3-027; nothing else changes. The switch-off answer is Not specified in the source documents (GAP-1302) while the flag is off.

**Done when.** The tests in section 16 pass, the three versions are fetched, verified and cached in SIT with 174 passing scenarios, a swap on a checksum mismatch leaves the model in force untouched, and the migrated schema holds 93 tables with no `payment_match_rule`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A workbook check fails, or no version is in force for a package | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-001 | An empty workbook | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-P4-002 | A role without the right calls a package operation | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is compile, schema, overlap, unreachable row, default row or scenario; the match order and the catalog completeness are part of the schema check, and the {detail} names row IDs, cells, rule IDs, package codes and version labels only, never a case fact or a person. This story adds no message and changes no text. A checksum mismatch, a failed build and a refused overwrite are operator conditions: they carry the package code, the version label and the expected and computed checksum to the log and the dashboard of RWB-P3-E2042-OPS, and produce no user-facing message.

### 15. Screens and states

No screen in this story. The three versions are read through rwb-decision's version list, and SCR-39 Rules and parameters shows the same versions in Epic 8. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-4396). The states LOADED, APPROVED, IN_FORCE, SUPERSEDED and REFUSED are rwb-decision's and are read from the version list; the model-cache states of section 9 are internal to rwb-case and are exposed only as the readiness signal and the metrics of RWB-P3-E2042-OPS.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01 | AC1, BR2, BR7, BR9 | End to end | RESTRUCTURE RES-2026.12, 38 rows, 62 scenarios, checksum verified |
| TC-E2-042-02 | AC2, BR2, BR3 | End to end | PAYMENT_MATCH PMT-2026.12, 3 rows, 58 scenarios |
| TC-E2-042-03 | AC3, BR2, BR7 | End to end | BOOKING_MATCH BKG-2026.12, 21 rows, 54 scenarios |
| TC-E2-042-04 | AC4, BR3, BR7 | End to end | PAY-91008 matched by EXACT and WINDOW; PAY-91002 5 percent short |
| TC-E2-042-05 | AC5, BR4, BR12 | End to end | R-RES-04 and the route-set rows of RES-2026.12 read through the catalog |
| TC-E2-042-06 | AC6, BR5 | Component | Migrated database on Testcontainers, table count 93, no payment_match_rule |
| TC-E2-042-07 | BR10, BR11, BR12 | Component | Contract test of the operations, events and activities of §12 against their published contracts |
| TC-E2-042-08 | Not specified in the source documents (DOR-RWB-P3-E2042-APP-12) | Component | Boundary test of the tables of §12.7: recovery_case, timer, queue, outbox_event, processed_event, idempotency_key |
| TC-E2-042-09 | BR6 | Component | RuleSet of each workbook is the package code; version labels RES-, PMT- and BKG-yyyy.MM |
| TC-E2-042-10 | BR8 | End to end | Open case keeps the package version it was decided under when a newer version reaches its valid-from date |
| TC-E2-042-11 | BR10, BR11 | Component | One KieBase per package version, at most 20 in the cache; a checksum mismatch keeps the last good model in force |
| TC-E2-042-12 | BR13 | Component | No rwb-case code writes rule_package, rule_package_version, rule_row or rule_test_case |
| TC-E2-042-13 | AC7, BR6, BR8, BR10, BR11, BR13 | Component | PAYMENT_MATCH PMT-2026.12 in cache; checksum mismatch; no write to rule tables |
| TC-E2-042-14 | AC8 | Component | EvaluateRules activity on RESTRUCTURE RES-2026.12, retried and timed out |
| TC-E2-042-15 | AC9 | Component | PMT-2026.12 APPROVED; disallowed status change requested |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end and Schema to Component. The cache, checksum and eviction tests of BR10 and BR11 are Component tests added to the same test cases, and the real cross-service proof is RWB-ITG-E2042-ITG.

### 17. Guardrails

- No business value in code. Rows, conditions, match types, tolerances, windows, action text, owner roles and timers are data in the workbooks and the registry; the cache bound and the timeouts are configuration.
- No personal data in logs, metrics, tests, workflow history or prompts. Scenarios use synthetic case facts and payment codes; the swap log carries package codes, version labels and checksums only.
- No read of another service's tables: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are read only through the rwb-decision operations, and `rwb_case` holds no foreign key into `rwb_decision` (DP-01).
- One evaluator: the three packages are evaluated only through the embedded Drools kit inside an activity, on the version in force fetched from rwb-decision; no code reads a workbook, a DRL source or a rule table (D-RCV-36 T3, T6; DP-04).
- Every fetched model is checksum-verified before use, and a version is never edited in place: a change is a new version and a rollback moves the pointer in rwb-decision.
- `payment_match_rule` is never created, and DF-REF-261 to DF-REF-273 are never referenced, by a migration, a test, a query or a document in the service.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD.
- No secret in a workbook, a value file or a runbook: the Blob identity and the rwb-decision certificate come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | Epic 1, 4; Program, 5.3 (legacy pointer Epic 1, 3.3; Epic 2, 3.2 and 3.8 is stale against BRD Epic 1 v4 and Epic 2 v2) | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38; R-RES-26 | TC-E2-042-01, TC-E2-042-02, TC-E2-042-03, TC-E2-042-06 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | Epic 1, 4; Program, 5.3 (legacy pointer Epic 1, 3.3; Epic 2, 3.2 and 3.8 is stale against BRD Epic 1 v4 and Epic 2 v2) | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26; R-RES-04 | TC-E2-042-01 to TC-E2-042-05 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | Arch v5 slide 27; decision D-RCV-36 T3 to T6; D-RCV-60 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E2-042-01, TC-E2-042-03, TC-E2-042-05 |
| D-RCV-36 T10 | `payment_match_rule` is retired and PAYMENT_MATCH replaces it | Arch v5 slide 27 notes; D-RCV-60 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26 | TC-E2-042-02, TC-E2-042-04, TC-E2-042-06 |

### 19. Out of scope

- The registry itself: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the three package rows, the admin operations, the approval and the one-call rollback (RWB-P7-E2042-APP; ASM-0069).
- The 00:01 promotion Schedule JOB-20 and the RulePackageInForce publication (rwb-decision).
- The load checks, the scenario runner and the workbook template as engineering (RWB-P3-E1073-APP).
- The evaluation of the three packages in the engines that own those decisions: PAYMENT_MATCH in JOB-07 (RWB-E2-027 and the rwb-payment stories), BOOKING_MATCH in the booking confirmation (RWB-E2-007), RESTRUCTURE in the treatment stage (RWB-E2-002, RWB-E2-004, RWB-E2-035).
- The remaining 448 routing rules and the UNIVERSAL package (Epic 3; DL24).
- The rules and parameters screen (SCR-39, Epic 8).
- The Blob container, the identity, the certificate and the sizing (RWB-P3-E2042-INF); the Helm values, the consumer group, the dashboards, the alerts and the runbook (RWB-P3-E2042-OPS).
- The real cross-service proof of the load, the approval, the promotion and the swap (RWB-ITG-E2042-ITG).
