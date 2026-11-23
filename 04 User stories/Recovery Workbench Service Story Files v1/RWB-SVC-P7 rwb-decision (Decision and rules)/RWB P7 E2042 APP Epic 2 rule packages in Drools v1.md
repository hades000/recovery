# RWB-P7-E2042-APP Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2042-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-AO |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-013, REQ-CWC-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for rwb-decision, the rule registry and the governance of the three Epic 2 packages. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE), a risk and model risk officer (RW-RISK) and the rwb-decision service that owns the rule registry**, I want **the three Epic 2 package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH held in schema `rwb_decision` as `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` rows, seeded with owner role RW-COE and hit policy FIRST, loaded through one admin operation that runs the six checks plus the two Epic 2 checks and the at-least-50-scenario check and the dry run, approved four-eyes by RW-RISK with the author refused, promoted at 00:01 on the valid-from date, rolled back in one call, and read back with their versions and dry-run counts**, so that **every Epic 2 decision in the target is made by an approved, dated registry version whose rows and test cases are provably the ones RW-COE loaded, and no version can reach an engine untested, unapproved or re-created from a retired table**.

Inside `rwb-decision` this is the registry and governance half of the legacy story RWB-E2-042:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` on which every governance action writes a decision record (DP-03).
- The registry: the three `rule_package` rows (DF-REF-274 to DF-REF-278) with owner role RW-COE and hit policy FIRST, the `rule_package_version` rows (DF-REF-279 to DF-REF-294) "RES-2026.12", "PMT-2026.12" and "BKG-2026.12", the parsed `rule_row` catalogue (DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054, DF-REF-296 to DF-REF-298) and the `rule_test_case` rows (DF-REF-185 to DF-REF-197, DF-REF-299).
- The load operation for one workbook version, with the six checks of the registry — compile, schema, overlap, unreachable row, default row and scenario — plus the two Epic 2 checks that the legacy story adds: the PAYMENT_MATCH match order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3, and the RESTRUCTURE route-set completeness of `action_text`, `owner_role` and `timer_spec` on every route-set row. The manifest of the load — the workbook reference, the generated DRL, the SHA-256, the valid-from date, the test result and the dry-run counts — is stored on the version row.
- The at-least-50-scenario check against `rules.testcases.min`, read as a parameter (DP-06), and the dry run, with the counts stored in `dry_run_counts` and returned by the dry-run read.
- The version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, and the promotion at 00:01 by the JOB-20 Schedule, which publishes `rwb.decision.RulePackageInForce.v1` with the package, the version, the checksum and the valid-from date.
- The four-eyes approval by RW-RISK, with the author of a version refused whatever right the author holds, and the one-call rollback that moves the pointer to the version in force before the rolled-back one.
- The reads: the package list, the version list and the dry-run counts, plus the two decision-log reads that return the governance records of a load, an approval, a promotion and a rollback.
- The assertion that `payment_match_rule` and DF-REF-261 to DF-REF-273 exist nowhere in `rwb_decision`: no table, no column, no rule row and no migration of this schema. The 93-table count of the legacy criterion is the monolith schema's and belongs to the story that owns that schema, not to this one.

Not this story, and stated again in section 6 and section 19:

- The workbook authoring, the Rows and Tests tabs, the write-once Blob object, the model cache, the checksum-verified swap and `RuleScenarioBuildGate` are **RWB-P3-E2042-APP** and **RWB-P3-E1073-APP**. This story receives a workbook at the load and runs the registry's own pipeline; it authors no workbook, stores no Blob object, caches no KieBase and runs no build gate.
- The screens, the roles, the permission matrix and the delegation of authority are **RWB-P4-E2042-APP** and **RWB-P4-E1037-CON**. This story declares the right each operation needs and names the roles as actors; it holds no role row and builds no screen.
- The notices a rule change must not raise are **RWB-P6-E2042-APP**; the cross-service proof of a load, an approval, a promotion, a swap and a record is **RWB-ITG-E2042-ITG**. Every criterion of this story is proved against the registry alone or through a contract fake.

The four registry tables and `decision_log_entry` are P7's under the R-PREC default ruling and ASM-0069, although TSD P4 v3 T3.1 and TSD P3 v3 declare the same tables for those modules and TSD P7 v2 T3.1 does not list them; the ruling is recorded in GAP-1301 and ASM-2311 and is not settled silently here. The database login used by the capability is the per-service login of DP-02, written only as "the rwb-decision login (DP-02)"; its name is Not specified in the source documents (GAP-1299; ASM-2309), and the shared monolith login appears nowhere in this story.

### 2. Business rationale

Epic 2 rules lived in three places in the monolith: reference rule rows, the `payment_match_rule` table and the `BookingMatchRules` class. A change of a match type, a tolerance, a window or a route-set field was a code change, tested by whoever wrote the class, and the only record of what decided a case was a rule ID with no version beside it. D-RCV-36 T3 to T6 put authoring, testing, four-eyes approval, effective dating and version audit into one governance path, and D-RCV-36 T10 retired `payment_match_rule` so that PAYMENT_MATCH is a package like every other decision table. Architecture v5 keeps that governance central in rwb-decision (slides 14, 27 and 41) and keeps evaluation local to the one service that owns each model (DP-04, ADR-017). The registry is therefore not a convenience: it is the only place in the target where an answer to "which version decided this, who approved it and what did it say" exists.

The registry also has to be mechanically trustworthy: a version is a workbook compiled to a KieBase with a checksum, and the checksum only means something if the row set and the test-case set that produced it are the ones the approver saw. That is why the load writes the version, its `rule_row` rows, its `rule_test_case` rows and its decision record in one transaction, and why a failed check refuses the load in full rather than storing a partial version.

This story is the rwb-decision half of the RWB-E2-042 split. It fixes the three package rows and their owner role and hit policy; the six checks plus the two Epic 2 checks; the 50-scenario gate and the dry run; the four-eyes approval and its separation of duty; the 00:01 promotion and its event; the one-call rollback; the version and dry-run reads; and the assertion that the retired table and its thirteen field IDs cannot reappear in `rwb_decision`. It meets REQ-CWC-013 and REQ-CWC-014 and gives RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 one registry to name, by rule ID and package version.

The measure is registry-shaped: three package rows with owner role RW-COE and hit policy FIRST; three versions at 38 rows and 62 scenarios, 3 rows and 58 scenarios and 21 rows and 54 scenarios — 174 scenarios in all, each package at or above `rules.testcases.min` = 50; one refusal in full for every failed check; one approval by a role other than the author; one promotion event per package at 00:01; one rollback that restores the previous version in one call; and no `payment_match_rule` table and no column of DF-REF-261 to DF-REF-273 anywhere in `rwb_decision`. The whole-schema 93-table count is the P3 story's assertion on `rwb_case`, not this story's on `rwb_decision`.

The realignment changes the mechanism, not the business rule:

1. The single recovery schema becomes `rwb_decision`, with the four registry tables, `decision_log_entry` and the library objects inside it and no other service reading them (DP-01); the DF-REF field IDs are unchanged.
2. The monolith loader becomes the rwb-decision admin operations under `/api/recovery/decision/v1` (DP-13), and the workbook arrives as the multipart body of the load.
3. The six legacy checks become `RuleCheckPipeline`, and the two Epic 2 checks become extensions of the schema check, so a version is refused in full and never stored half-checked.
4. `rules.testcases.min` becomes a parameter read through DP-06 instead of a configuration property.
5. The author and the approver become user references on the version row, and separation of duty becomes a service rule: the author's approve call is refused with MSG-P7-002.
6. The Quartz effective-date job becomes the JOB-20 Temporal Schedule at 00:01 on the `rwb-decision` queue (DP-10), and the announcement becomes `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` (DP-14).
7. The nightly copy of the decision log to the data lake is gone; each governance action writes a local decision record on `rwb.decision-record.v1` (DP-03, ADR-022).
8. The retired table and its field IDs stay retired: `payment_match_rule` is never created in `rwb_decision`, and the schema check fails the build if a migration tries.

The business outcome is unchanged and easier to audit: a rule change is data, it is tested, approved by a second person and dated, it takes effect without a release, it rolls back in one call, and every answer names the version that made it (R-UNI-38). What the target adds is that the evidence of all of that sits in one schema that this service writes and no other service reads.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2042-CON | The published contract of the legacy key: the workbook Rows and Tests schema (RuleSet = package code, NAME = rule ID, the default row last), the Blob object naming and metadata, the five consumed rwb-decision operations, the `RulePackageInForce` consumption contract, the `EvaluateRules` activity contract with `RuleResult` and `NoPackageInForce`, the cache and swap rules, and the rwb-decision and rwb-access fakes. This story provides the registry side of that contract; it does not restate the workbook or the cache |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one hash-chained record per governance action, written in the same transaction as the action |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): the compile of the workbook to a KieBase, the checksum, first-match semantics and the `NoPackageInForce` outcome. Used at load and at promotion, never to evaluate a business decision for a case |
| RWB-PLT-E1071-CON | The Temporal workflow kit in namespace `rwb-recovery` (DP-10): the JOB-20 rule-promote Schedule runs on it. This story starts no workflow of its own |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the rwb-case parameters contract (DP-06): `rules.testcases.min` = 50 |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the rwb-case reference-data contract (DP-07): LOV-DECISION and the version-state vocabulary with the version in force |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic, event and queue names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15): the `rwb_decision` baseline and the two migrations of section 13 |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the Epic 8 screen reads the registry through it; this story serves no screen |
| RWB-P7-E1073-CON, RWB-P7-E1073-APP | This service's own rule-package contract and authoring-pipeline stories: the model and catalog reads another service calls, the workbook template and the shared check signatures. Reused where they have landed and built against their published set and fake; no build dependency of this story (DP-04) |
| RWB-P3-E2042-APP, RWB-P3-E1073-APP | The workbook authoring pipeline, the write-once Blob store, the model cache and `RuleScenarioBuildGate`. This story receives their workbooks at the load operation and proves the registry half; it builds none of the P3 artefacts |
| RWB-P4-E2042-APP, RWB-P4-E1037-CON | The roles, the permission matrix and the authorise answer behind every operation of section 12.1. This story declares the right and names the roles; it holds no role row |

The DP-added H and C dependencies above — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, and C RWB-P7-E1073-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON — are not repeated in the metadata rows, which name Depends on (build) None and Contract dependencies RWB-P3-E2042-CON. They are platform contracts of wave 0 and published contracts that an APP story builds against as fakes, so none blocks this story and Ready to start stays Day 1 (GAP-1296; ASM-2306).

Business preconditions carried from RWB-E2-042:

- The three package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are not yet seeded; this story seeds them in `rule_package` with owner role RW-COE and hit policy FIRST. The five Epic 1 package codes are already seeded by the registry baseline and are not touched.
- The three version labels are agreed on 16 November 2026: "RES-2026.12" with 38 rows and 62 scenarios, "PMT-2026.12" with 3 rows and 58 scenarios and "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-15 (the valid-from date is the legacy assumption and is copied unchanged). Every package is at or above `rules.testcases.min` = 50, and 174 scenarios pass in all.
- The PAYMENT_MATCH rows are EXACT at row order 1, WINDOW at 2 and PARTIAL at 3, and R-RES-26 is the rule the three rows belong to. The RESTRUCTURE row set includes R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, and R-RES-04 carries action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days".
- The business date of the run is 2026-12-10; the loader is "U-41" holding RW-COE and the approver is "U-51" holding RW-RISK, and they are two different people. The rights are Rules and parameters C for RW-COE, A for RW-RISK and R for RW-AUDIT.
- The rwb-decision login (DP-02) is in the platform secret store, with the migration role and the application role kept apart; its name is Not specified in the source documents (GAP-1299; ASM-2309).
- The PAYMENT_MATCH label of this key is "PMT-2026.12" valid from 2026-12-15, while RWB-E2-027 and its P7 story hold the same package as "PM-2026.12" valid from 2026-12-01. The conflict is GAP-1297 and is not settled here; ASM-2307 pins this key to the legacy value and requires one reconciled version row before SIT.
- The legacy flag `rwb.p3.drools` is on in DEV and SIT; in the target it is read as a parameter through DP-06 and is not a code constant.
- Synthetic data only: package codes, version labels, rule IDs, row orders, thresholds, dates and payment codes of the legacy story. No real account, customer, party or payment appears in a load, a test or a record.

### 4. Flow

1. The release applies the `rwb_decision` baseline and then `V2_042_1__epic2_rule_packages.sql`, which inserts RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH into `rule_package` with their title, owner role RW-COE and hit policy FIRST (DF-REF-274 to DF-REF-278). The migration writes no `rule_package_version`, no `rule_row` and no `rule_test_case` row: the versions come from the load.
2. Center of excellence analyst: loads a workbook version through `POST /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` as multipart with `file` (xlsx with the Rows and Tests tabs) and `validFrom`, taken from the workbook RWB-P3-E2042-APP authored and stored write-once.
3. `RuleVersionController`: authenticates the session, checks the Rules and parameters C right through the guard of the P4 story, validates the multipart body and the package code, and answers 404 for an unknown code, 422 with MSG-GEN-001 for an empty file and MSG-GEN-003 for a `validFrom` before the business date, and 409 with MSG-GEN-004 when the label already exists for the package.
4. `WorkbookParser`: reads the Rows tab into `rule_row` candidates (RuleSet = the package code, NAME = the rule ID, the condition and output columns of the package, the default row last) and the Tests tab into `rule_test_case` candidates. A malformed or empty workbook is refused before any check runs.
5. `RuleCheckPipeline`: compiles the workbook through the embedded Drools kit (DP-04) and runs the six checks in order — compile, schema, overlap, unreachable row, default row and scenario. Each failure refuses the whole load with MSG-P3-027 and names the check, the row, the column or the failing test-case IDs, never a case fact.
6. `Epic2CheckExtensions`, called from the schema check: `PaymentMatchOrderCheck` proves that PAYMENT_MATCH has one row per match type and the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3; `RestructureCatalogCheck` proves that every RESTRUCTURE route-set row carries a non-empty `action_text`, `owner_role` and `timer_spec`. A violation refuses the load in the same way as any other schema failure.
7. `TestCaseRunner` and `DryRunService`: run the Tests tab against the compiled model, count total, passed and failed, refuse the load when `total` is below `rules.testcases.min` read through DP-06, and run the dry run over the test cases and the business date. The counts are stored in `dry_run_counts` and returned by the dry-run read; their breakdown is Not specified in the source documents (GAP-1302; ASM-2312).
8. `RuleVersionService`, one transaction: writes the `rule_package_version` row with status LOADED, the workbook reference, the generated DRL, the SHA-256, the valid-from date, the author, the test result and the dry-run counts (DF-REF-279 to DF-REF-294); writes the `rule_row` and `rule_test_case` rows of the version; writes the decision record of the load through `DecisionRecordWriter` (DP-03); and returns 201 with the version. A failure of any of these writes rolls the whole load back, so a version can never exist without its rows or its record.
9. Risk officer: approves the version through `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve`. `ApprovalService` compares the caller reference with the author on the version and refuses with MSG-P7-002 when they are equal, whatever right the caller holds. Otherwise it moves the version to APPROVED, records the approver and the approval time, and writes the decision record of the approval. No approval item of the delegation of authority is raised, because a package version is not a credit decision.
10. JOB-20: the rule-promote Temporal Schedule runs at 00:01 on the `rwb-decision` queue (Arch v5 slide 44; DP-10). `PromotionService` promotes every APPROVED version whose valid-from date has arrived to IN_FORCE, marks the version it replaces SUPERSEDED, writes the decision record of the promotion and publishes `rwb.decision.RulePackageInForce.v1` with the package code, the version label, the version ID, the checksum and the valid-from date. A version whose date has not arrived is not promoted.
11. Center of excellence analyst: when a version in force must be withdrawn, calls `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback` once. `RollbackService` moves the pointer to the version in force before the rolled-back one, marks the rolled-back version ROLLED_BACK, keeps every earlier decision on the version it was taken under, and writes the decision record of the rollback. A rollback with no predecessor is refused with MSG-P3-015 and writes nothing.
12. Internal audit or any role with the decision-log read: reads the package list, the version list, the dry-run counts and the governance records through the operations of section 12.1, and proves from `GET /api/recovery/decision/v1/decision-log` that the load, the approval, the promotion and the rollback each left one hash-chained record.

Nothing in this flow evaluates a package for a case, matches a payment, sets a case state, reads an ACE view or writes a row outside `rwb_decision`: the registry and its governance are the whole deliverable.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required part of the load is missing: no file, no `validFrom`, or an empty workbook | 422 before any check runs; no version row, rule row or test case is written | MSG-GEN-001 | AC2, AC4 |
| X2 | `validFrom` is before the business date of the run | 422 and no version row; the label is not consumed | MSG-GEN-003 | AC2 |
| X3 | The version label already exists for the package, or the version row changed at commit | 409; the version already held is untouched and the action is retried, never applied twice | MSG-GEN-004 | AC2, AC3 |
| X4 | A compile, schema, overlap, unreachable-row or default-row check fails | The load is refused in full with 422; the check, the row and the column are named; no version, rule row or test case exists | MSG-P3-027 | AC2, AC3 |
| X5 | A PAYMENT_MATCH row carries a match type outside EXACT, WINDOW and PARTIAL | The schema check refuses the load and names the row and the cell | MSG-P3-027 | AC3 |
| X6 | The PAYMENT_MATCH row order puts PARTIAL before WINDOW, or repeats a row order | The schema check refuses the load and names the priority cells | MSG-P3-027 | AC3 |
| X7 | A RESTRUCTURE route-set row has an empty `action_text`, `owner_role` or `timer_spec` | The schema check refuses the load and names the row and the column; no engine can later read a partial route-set row | MSG-P3-027 | AC2 |
| X8 | The Tests tab holds fewer than `rules.testcases.min` cases, or a case fails | The scenario check refuses the load and names the shortfall or the failing test-case IDs | MSG-P3-027 | AC4 |
| X9 | The dry run cannot complete on the business date | The load is refused and nothing is written; the version in force keeps running | MSG-P3-027 | AC4 |
| X10 | The author of a version calls approve | 403; the version stays LOADED with no approver and no approval time | MSG-P7-002 | AC5 |
| X11 | A rollback is called for a version with no predecessor, or for a version that was never in force | 409 or 422 as the operation decides; the version in force stays in force and nothing is written | MSG-P3-015 | AC7 |
| X12 | The decision record of a load, an approval, a promotion or a rollback cannot be written | Nothing is committed: no version row, no state change, no promotion and no event; an incident is raised and the caller retries | MSG-P7-003 | AC2, AC5, AC6, AC7 |
| X13 | A migration of `rwb_decision` creates `payment_match_rule`, or a column of DF-REF-261 to DF-REF-273 | The registry schema check fails and the build is blocked before the artefact is published | None | AC9 |
| X14 | The caller holds no Rules and parameters right for the operation, or the version is outside the caller's scope | 403 through the guard of the P4 story; nothing is read, written, promoted or rolled back | MSG-P4-002 | AC1, AC8 |

A stale version row at commit, matched on its `version` column, is MSG-GEN-004 and the action is retried, never applied twice. The version row, its rule rows, its test cases and its decision record are always written together, so a version cannot exist without its record and no promotion can announce a version that was not recorded.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E2042-CON, the platform contracts of its DP table and the registry scaffold of its own service; the P3 authoring pipeline, the model cache and the build gate are consumed as published contracts and fakes, and the P4 rights answer is declared but not built here |
| Negotiable | The version labels, the valid-from dates, the row values, the titles, the test cases and the message texts are data and registry rows; the story fixes only the checks, the four-eyes rule, the promotion, the rollback and the absence of the retired table |
| Valuable | Three Epic 2 packages become approved, dated, reversible registry data with 174 passing scenarios, and every change is explainable from the decision log |
| Estimable | One controller pair, one load service, one parser, one check pipeline with two Epic 2 extensions, one test-case runner, one dry run, one approval, one promotion handler, one rollback, one repository, one record writer and one schema check |
| Small | Fits two weeks with its tests. It authors no workbook, stores no Blob object, caches no KieBase, runs no build gate, builds no screen and raises no notice |
| Testable | Each criterion is a load, an approval, a promotion, a rollback, a read or a schema check, with a fixed Given, When and Then and a recorded result. The cross-service journey is not claimed here; it is RWB-ITG-E2042-ITG's |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages in the rwb-decision registry

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK, and they are two different people
    Given the rwb-case parameters contract mock returns rules.testcases.min 50
    Given the rwb-case reference-data contract mock returns LOV-DECISION and the version-state list with their versions in force
    Given the business date is 2026-12-10
    Given the rwb_decision schema is migrated from empty with the rwb-decision Flyway sequence

  Scenario: AC1 The three Epic 2 package codes are seeded with owner role RW-COE and hit policy FIRST (new, D-RCV-60)
    When V2_042_1__epic2_rule_packages.sql runs
    Then rule_package holds exactly RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH with owner_role "RW-COE" and hit_policy "FIRST"
    Then each row carries a title, whose text is Not specified in the source documents (GAP-1302; ASM-2312)
    Then no fourth Epic 2 package exists and the five Epic 1 package codes are unchanged
    Then the seed writes no rule_package_version, rule_row or rule_test_case row
    Then a caller without Rules and parameters R is refused the package read with MSG-P4-002

  Scenario: AC2 A RESTRUCTURE version loads through the six checks and the route-set completeness check (new, D-RCV-60)
    Given a RESTRUCTURE workbook version "RES-2026.12" with 38 rows and 62 scenarios and valid from 2026-12-15
    When U-41 loads it with POST /api/recovery/decision/v1/admin/rule-packages/RESTRUCTURE/versions
    Then the compile, schema, overlap, unreachable row, default row and scenario checks pass
    Then the route-set completeness check passes because every route-set row carries action_text, owner_role and timer_spec
    Then the test result is "62 of 62 scenarios passed"
    Then the answer is 201 with status LOADED, the checksum, the test result and the dry-run counts
    Then rule_row holds 38 rows under version "RES-2026.12", including R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02
    Then one decision record of the load is written before the version row commits
    Given a second RESTRUCTURE workbook "RES-2026.13" whose row R-RES-04 has an empty timer_spec
    When U-41 loads it
    Then the load is refused with 422 and MSG-P3-027 at the schema check, naming R-RES-04 and the timer column
    Then no version row, rule row or test case is written for "RES-2026.13" and "RES-2026.12" keeps its state

  Scenario: AC3 The PAYMENT_MATCH match order is checked at load and a wrong order is refused in full (new, D-RCV-60)
    Given a PAYMENT_MATCH workbook version "PMT-2026.12" with 3 rows and 58 scenarios, the rows EXACT at row order 1, WINDOW at 2 and PARTIAL at 3
    When U-41 loads it with POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the match-order check passes: one row per match type and the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3
    Then the version is LOADED with the test result "58 of 58 scenarios passed"
    Given a second PAYMENT_MATCH workbook "PMT-2026.13" whose PARTIAL row is at row order 2 and whose WINDOW row is at row order 3
    When U-41 loads it
    Then the load is refused with 422 and MSG-P3-027 at the schema check, naming the priority cells of the two rows
    Then no version row, rule row or test case is written for "PMT-2026.13" and "PMT-2026.12" keeps its state
    Then a repeat load of "PMT-2026.12" is refused with 409 and MSG-GEN-004

  Scenario: AC4 The at-least-50-scenario check and the dry run (new, D-RCV-60)
    Given a RESTRUCTURE workbook version "RES-2026.13" whose Tests tab holds 49 scenarios
    When U-41 loads it
    Then the load is refused with 422 and MSG-P3-027 at the scenario check, naming the shortfall against rules.testcases.min 50
    Then no version is created
    Given a BOOKING_MATCH workbook version "BKG-2026.12" with 21 rows and 54 scenarios and valid from 2026-12-15
    When U-41 loads it
    Then the scenario check passes with 54 at or above rules.testcases.min 50
    Then the dry run completes on business date 2026-12-10 and its counts are stored in dry_run_counts, whose breakdown is Not specified in the source documents (GAP-1302; ASM-2312)
    Then the version is LOADED with the test result "54 of 54 scenarios passed"

  Scenario: AC5 The author cannot approve and RW-RISK does (new, D-RCV-60)
    Given version "RES-2026.12" is LOADED and authored by U-41
    Given U-41 also holds a role that carries the Rules and parameters A right
    When U-41 calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve
    Then the call is refused with MSG-P7-002 and the version stays LOADED with no approver and no approval time
    When U-51 calls the same operation for the same version
    Then the version is APPROVED with approver U-51 and the approval time
    Then the decision record of the approval names the package "RESTRUCTURE", the version "RES-2026.12" and the approver
    Then no approval item of the delegation of authority is raised by the package-version approval

  Scenario: AC6 The promotion runs at 00:01 on the valid-from date and publishes one event per package (new, D-RCV-60)
    Given "RES-2026.12" is APPROVED with valid from 2026-12-15 and version "RES-2026.11" is IN_FORCE
    When the JOB-20 rule promote Schedule runs at 00:01 on 2026-12-14
    Then version "RES-2026.12" stays APPROVED and "RES-2026.11" stays IN_FORCE
    When the JOB-20 rule promote Schedule runs at 00:01 on 2026-12-15 on queue rwb-decision
    Then version "RES-2026.12" is IN_FORCE and version "RES-2026.11" is SUPERSEDED
    Then one rwb.decision.RulePackageInForce.v1 per promoted package is on rwb.decision.events.v1 with packageCode, versionLabel, versionId, checksum and validFrom
    Then the decision record of the promotion names the package, the version and the rwb-decision service identity
    Then no version, rule row or test case is edited by the promotion

  Scenario: AC7 The one-call rollback restores the previous version and earlier decisions keep their version (new, D-RCV-60)
    Given "RES-2026.12" is IN_FORCE from 2026-12-15 and "RES-2026.11" was in force before it
    Given a decision record of case "RW-2026-000777" names rule version "RES-2026.12"
    When U-41 calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback once for "RES-2026.12"
    Then version "RES-2026.11" is IN_FORCE and version "RES-2026.12" is ROLLED_BACK
    Then the decision record of case "RW-2026-000777" still names rule version "RES-2026.12"
    Then the decision record of the rollback names the two versions and the reason
    Then a second call for the same version finds it no longer in force and applies nothing
    Given PAYMENT_MATCH holds only version "PMT-2026.12" and it is IN_FORCE
    When U-41 calls the rollback once for "PMT-2026.12"
    Then the call is refused with MSG-P3-015 and "PMT-2026.12" stays IN_FORCE

  Scenario: AC8 The version list and the dry-run counts are readable and change nothing (new, D-RCV-60)
    Given "RES-2026.12" is IN_FORCE from 2026-12-15 with its checksum, its test result and its dry-run counts
    Given "PMT-2026.12" is LOADED with its author, its checksum, its test result and its dry-run counts
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages
    Then the answer holds RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH with owner role RW-COE and no fourth Epic 2 package
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages/RESTRUCTURE/versions
    Then the answer holds "RES-2026.12" with status IN_FORCE, the valid-from date, the checksum, testResult total 62, passed 62, failed 0 and the dry-run counts
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run
    Then the answer holds the dry-run counts and the per-test-case result of the version
    Then the two reads change no version state and write no row

  Scenario: AC9 payment_match_rule and DF-REF-261 to DF-REF-273 exist nowhere in rwb_decision (new, D-RCV-60)
    Given a database migrated from empty with the rwb-decision migrations of the release
    When the registry schema check runs against rwb_decision
    Then no table named payment_match_rule exists in rwb_decision
    Then no column of DF-REF-261 to DF-REF-273 exists in any rwb_decision table
    Then the check fails the build when any rwb_decision migration in the release creates payment_match_rule or one of those columns
    Then the check reads only rwb_decision and no other schema
    Then the 93-table count of the legacy criterion is not asserted here, because it is the monolith schema's and RWB-P3-E2042-APP's
```

The nine criteria are new under D-RCV-60 and they test only the registry and its governance. No legacy criterion is restated: AC1 to AC6 of RWB-E2-042 belong to RWB-P3-E2042-APP, which also owns the workbook, the Blob store, the model cache and the build gate. The values inside the new criteria are the legacy values — the package codes, the labels, the row and scenario counts, the valid-from date, the rule IDs and the three route-set fields — so the registry is proved against the same data the legacy story used, without reopening a legacy criterion.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The registry is `rwb-decision`'s: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` sit in `rwb_decision`, no other service reads them, and a version is never edited in place — a change is a new version and a rollback moves a pointer | Arch v5 slides 14, 27 and 41; R-PREC default ruling; ASM-0069; DP-01 |
| BR2 | Every Epic 2 version is loaded from a Drools XLS workbook through the load operation only; the version row holds the workbook reference, the generated DRL, the SHA-256 and the valid-from date | D-RCV-36 T3, T4; Temporal and Drools slides 15 and 16 |
| BR3 | The load checks are compile, schema, overlap, unreachable row, default row and scenario; the two Epic 2 checks run inside the schema check; the dry run runs after them; any failure refuses the load in full | Temporal and Drools slide 15 and its notes; FSD P7 v3 A2.7 |
| BR4 | PAYMENT_MATCH has one row per match type, and the row order is EXACT priority 1, WINDOW priority 2, PARTIAL priority 3, as in RWB-E2-027 | R-RES-26; D-RCV-36 T10; legacy BR3 |
| BR5 | Every RESTRUCTURE route-set row carries `action_text`, `owner_role` and `timer_spec`, and the engine reads them only from the registry, by rule ID and package version | D-RCV-36 T6; FEAT-CWC-28; legacy BR4 |
| BR6 | Each package version carries at least `rules.testcases.min` scenarios — 50 — and every scenario passes before the version may be approved | REQ-CWC-014; D-RCV-36 T4; legacy BR2 |
| BR7 | The author of a version cannot approve it; the approver is RW-RISK and must be a different user reference, and a package-version approval is not a delegation-of-authority decision | D-RCV-36 T4; Temporal and Drools slide 15; legacy section 10 |
| BR8 | A version is in force from its valid-from date; JOB-20 promotes an APPROVED version at 00:01, supersedes the version it replaces, and publishes `rwb.decision.RulePackageInForce.v1` | Arch v5 slides 14, 27 and 44; Temporal and Drools slide 15 |
| BR9 | A rollback is one call and puts the version in force before the rolled-back one back in force; an earlier decision keeps the version it was taken under | FSD P7 v3 AC-ALT-P7-007-02; R-UNI-38; legacy BR8 |
| BR10 | The version states are LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, and no other value is written | Temporal and Drools slide 15 notes |
| BR11 | Every governance action — load, approve, promote, roll back — writes one hash-chained decision record in the same transaction, and an action whose record cannot be written is not taken | FSD P7 v3 VR-P7-001-2 and principle 5; R-UNI-39; DP-03; legacy BR9 |
| BR12 | The operations declare Rules and parameters C, A, R and U; a caller without the right is refused, and no role row is held in `rwb_decision` | TSD P4 v3 T6.1; RWB-P4-E2042-APP; legacy section 10 |
| BR13 | No business value is code: the package rows, the version labels, the valid-from dates, the row order, the thresholds, `action_text`, `owner_role`, `timer_spec` and `rules.testcases.min` are rows and parameters | Template and Rules §R7.2 s17; legacy section 17; DP-06, DP-07 |
| BR14 | `payment_match_rule` is never created in `rwb_decision`; DF-REF-261 to DF-REF-273 stay retired and no migration, rule row, test or query references them | D-RCV-36 T10; legacy BR5 |
| BR15 | The registry is read, not evaluated: this story never evaluates a package for a case, never caches a KieBase and never reads another service's schema | Arch v5 slide 27; DP-04; DP-05 |

### 9. State transitions

This story changes no case status and no plan state. It owns the lifecycle of a package version and the registry row it belongs to.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The seed migration runs | The package code is not held | `rule_package` row exists with owner role RW-COE and hit policy FIRST |
| (none) | A workbook is loaded | Every check passes, the scenario gate passes, the dry run completes and the record is written | LOADED |
| (none) | A workbook is loaded | A check fails, the scenario gate fails, the dry run fails, the label exists, or the record cannot be written | No row is created; the earlier version in force keeps its state |
| LOADED | Approve | The caller is not the author and holds Rules and parameters A | APPROVED |
| LOADED | Approve | The caller is the author, whatever right the caller holds | LOADED (refused, MSG-P7-002) |
| APPROVED | JOB-20 at 00:01 | The valid-from date has arrived | IN_FORCE; the version it replaces becomes SUPERSEDED |
| APPROVED | JOB-20 at 00:01 | The valid-from date has not arrived | APPROVED (unchanged) |
| IN_FORCE | Rollback, one call | A version was in force before it | ROLLED_BACK; the previous version becomes IN_FORCE |
| IN_FORCE | Rollback, one call | No version was in force before it | IN_FORCE (refused, MSG-P3-015) |
| IN_FORCE | A newer version is promoted | The newer version reaches its valid-from date | SUPERSEDED |
| Any | A schema check at build time | A migration creates `payment_match_rule` or a column of DF-REF-261 to DF-REF-273 | Build blocked; no row changes |

A refused load or approval leaves every row exactly as it was before the call, and a version in force changes only through the promotion the Schedule runs and announces. The case transitions of RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 are those stories' and are neither raised nor observed here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Seeds nothing by hand (the migration does); loads a version under Rules and parameters C, runs and reads the dry run under R, calls the rollback under U, and reads the registry and the decision log under R |
| RW-RISK, risk and model risk officer | Approves a loaded version under Rules and parameters A; may not be the author of that version, and the author's own call is refused whatever right the author holds |
| RW-AUDIT, internal audit | Reads the packages, the versions, the row counts, the test results, the dry-run counts and the governance records under Rules and parameters R; changes nothing |
| RW-REFADM, reference data administrator | Prepares the change checklist and the load file; holds no C, U or A, so it uploads nothing, approves nothing and rolls nothing back |
| RW-CASEOWN, RW-TEAMMGR and any role without a Rules and parameters right | Refused with MSG-P4-002 on every operation of section 12.1 |
| The rwb-decision service identity | Runs the checks, the dry run, the promotion handler, the rollback and the schema check; writes the decision records and the `RulePackageInForce` outbox row |
| SY-RULES, Drools evaluator | Compiles the workbook and supplies first-match semantics and the checksum through the embedded kit at load (DP-04); it evaluates no case decision in this story |
| The build pipeline, no user role | Runs the registry schema check on a Testcontainers database and the unit and contract tests; it never connects to SIT, UAT or PROD |
| No delegation of authority level applies | A rule package version is not a credit decision; the approval is four eyes and not a DoA level, so no `approval` row and no `ApprovalRequested` event is raised by it |

Separation of duty is a service rule, not a convention: the analyst who loaded a version never approves it, and RW-RISK approves with a distinct user reference (BR7). The roles and rights are answered by the guard of RWB-P4-E1037-CON and the matrix of RWB-P4-E2042-APP; this story names them and holds no role row. The database login is the per-service login of DP-02, written as "the rwb-decision login (DP-02)"; its name is Not specified in the source documents (GAP-1299; ASM-2309). No person is named anywhere: the actors are roles and service identities.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package (P7) | id | Write, seed |
| DF-REF-275 | rule_package (P7) | package_code | Write, seed |
| DF-REF-276 | rule_package (P7) | title | Write, seed; the title text is Not specified in the source documents (GAP-1302; ASM-2312) |
| DF-REF-277 | rule_package (P7) | owner_role | Write, seed: RW-COE |
| DF-REF-278 | rule_package (P7) | hit_policy | Write, seed: FIRST |
| DF-REF-279 | rule_package_version (P7) | id | Write; read |
| DF-REF-280 | rule_package_version (P7) | package_id | Write; read |
| DF-REF-281 | rule_package_version (P7) | version_label | Write; read |
| DF-REF-282 | rule_package_version (P7) | status | Write; read |
| DF-REF-283 | rule_package_version (P7) | source_blob_ref | Write; read |
| DF-REF-284 | rule_package_version (P7) | drl_source | Write |
| DF-REF-285 | rule_package_version (P7) | checksum | Write; read and published on the event |
| DF-REF-286 | rule_package_version (P7) | valid_from | Write; read and published on the event |
| DF-REF-287 | rule_package_version (P7) | valid_to | Write; read |
| DF-REF-288 | rule_package_version (P7) | author | Write; read |
| DF-REF-289 | rule_package_version (P7) | approver | Write; read |
| DF-REF-290 | rule_package_version (P7) | loaded_at | Write; read |
| DF-REF-291 | rule_package_version (P7) | approved_at | Write; read |
| DF-REF-292 | rule_package_version (P7) | test_result | Write; read |
| DF-REF-293 | rule_package_version (P7) | dry_run_counts | Write; read |
| DF-REF-294 | rule_package_version (P7) | rollback_of | Write; read |
| DF-REF-295 | rule_package_version (P7) | change_checklist | Not read and not written: the change checklist is RWB-E2-041's |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | all rule fields | Write at load; read |
| DF-REF-052 to DF-REF-054 | rule_row (P7) | rule_table, row_order, target_queue_code | Write at load; read |
| DF-REF-008 | rule_row (P7) | action_text | Write at load; read by RWB-E2-035 through the catalog |
| DF-REF-010 | rule_row (P7) | owner_role | Write at load; read by RWB-E2-035 through the catalog |
| DF-REF-011 | rule_row (P7) | timer_spec | Write at load; read by RWB-E2-035 through the catalog |
| DF-REF-296 | rule_row (P7) | package_version_id | Write at load; read |
| DF-REF-297 | rule_row (P7) | drools_rule_name | Write at load; read |
| DF-REF-298 | rule_row (P7) | outputs | Write at load; read |
| DF-REF-185 to DF-REF-197 | rule_test_case (P7) | all fields | Write at load; read |
| DF-REF-299 | rule_test_case (P7) | package_version_id | Write at load; read |
| DF-DEC-001 to DF-DEC-031 | decision_log_entry (P7) | the record of a load, an approval, a promotion or a rollback | Write one row per governance action (DP-03); read through the decision log |
| (outbox) | outbox_event in `rwb_decision` | the `DecisionRecorded` and `RulePackageInForce` rows | Write in the same transaction as the action |
| (inbox) | processed_event in `rwb_decision` | the dedupe row of any consumed event | This story consumes no event, so no row is written |
| DF-ACE-* | ACE views | — | Not read: no ACE view is read by this story (DP-05) |
| DF-REF-261 to DF-REF-273 | payment_match_rule (retired) | — | Not created, not read and not written; the absence is asserted by AC9 |

The four registry tables and `decision_log_entry` are rwb-decision's and no other service reads them (DP-01; ASM-0069). The field IDs of the registry are those of the Logical Data Model and Data Dictionary v8, as RWB-P3-E2042-APP and the legacy story cite them; the decision-entry IDs are those of TSD P7 v2 T3.1. The registry tables are absent from TSD P7 v2 T3.1 and are declared for P4 and P3 in their own TSDs; the ownership conflict is GAP-1301 and the ruling applied is ASM-2311. The decision code of a governance entry is resolved from LOV-DECISION read through DP-07, and its value is Not specified in the source documents (GAP-1298; ASM-2308); the field itself is DF-DEC-003. No new field is added by this story, except the four unique keys of section 13, which are constraints and not fields.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The six admin paths are the rule-package family of the ownership map with the target base of DP-13; the two decision-log paths are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1 on the same base. The load and version-list request and answer shapes are the legacy section 12 shapes; the rollback body, the dry-run breakdown, the title text and the decision code of a governance entry are Not specified in the source documents (GAP-1298 and GAP-1302; ASM-2308 and ASM-2312).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/rule-packages` | List the packages of the registry with their code, title, owner role and hit policy; 200 with the package list | Rules and parameters R | Not applicable, read only |
| POST | `/admin/rule-packages/{packageCode}/versions` | Load a workbook version: multipart `file` (xlsx with the Rows and Tests tabs) and `validFrom`; run the six checks, the two Epic 2 checks, the scenario gate and the dry run; 201 with the version | Rules and parameters C | Package code and version label; a repeated label is 409 with MSG-GEN-004 |
| GET | `/admin/rule-packages/{packageCode}/versions` | List the versions of a package with status, valid-from and valid-to dates, author, approver, checksum, test result and dry-run counts; 200 | Rules and parameters R | Not applicable, read only |
| GET | `/admin/rule-package-versions/{versionId}/dry-run` | Read the dry-run counts and the per-test-case result of a version | Rules and parameters R | Not applicable, read only |
| POST | `/admin/rule-package-versions/{versionId}/approve` | Approve a loaded version with four eyes; 200 with the version at APPROVED | Rules and parameters A | Idempotency-Key header; the author's call is refused with MSG-P7-002 |
| POST | `/admin/rule-package-versions/{versionId}/rollback` | Roll a version in force back to the version before it in one call; 200 with the two versions | Rules and parameters U | Idempotency-Key header; a second call for the same version finds it no longer in force |
| GET | `/decision-log` | Read the governance decision records by case, decision, rule, approver and date range; 200 with the page | Decision log R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | Read one decision record with its inputs reference, versions, actor, final call, actions, outcome and hashes; 200 | Decision log R, scope applied | Not applicable, read only |

The version body carries `versionId`, `packageCode`, `versionLabel`, `status`, `validFrom`, `validTo`, `author`, `approver`, `checksum`, `testResult` (`total`, `passed`, `failed`, `failedScenarioIds`) and `dryRunCounts`. The version label and the package code are the identity of a version; the label alone is not unique across packages. Errors: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 an unknown package code or version; 409 the label exists (MSG-GEN-004) or the version is not in the state the call needs; 422 a check failed (MSG-P3-027 with the check, the row, the column and the failing test-case IDs in the problem detail), an empty file (MSG-GEN-001), a `validFrom` order (MSG-GEN-003) or a rollback with no predecessor (MSG-P3-015); 503 the decision record could not be written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

No promote operation is published: the promotion is JOB-20's Schedule of 12.6. The model read `GET /rule-models/{packageCode}/{version}` and the catalog read `GET /rule-catalog/{ruleId}?packageVersion=` that a consuming service uses are the P7 rule-package contract story RWB-P7-E1073-CON's; this story supplies the rows they serve and does not duplicate their paths. The version states and the check names are values of the registry and of the reference lists of DP-07, never constants of the code.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case, on RWB-P3-E1042-CON | `rules.testcases.min` = 50 for the scenario gate (DP-06); faked, one hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION and the version-state list with the version in force (DP-07); faked, one hop, 2 s |

The roles, the rights and the session behind section 12.1 are answered by the guard of RWB-P4-E1037-CON and the matrix of RWB-P4-E2042-APP; this story declares the right each operation needs and does not build the authority. No ACE view and no other service schema is read (DP-05).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 | packageCode | package code, version label, package version ID, checksum, valid-from date, promoted at |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by this service | entryId | the hash-chained record of a governance action: the decision code from LOV-DECISION, rule ID (the package code), rule version (the version label), inputs reference, actor, final call, decided at |

Both rows are written to the outbox in the same transaction as the action and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform. `RulePackageInForce` is consumed by the owning services that hold an evaluated copy and by gateway-bff for its cache refresh (Arch v5 slides 20 and 43). No event carries a name, an e-mail address, a mobile number, an account number or a case fact.

#### 12.4 Events consumed

None. This story consumes no Kafka event: the workbook arrives through the load operation, the approval through its operation, and the promotion is the Schedule of 12.6. `ApprovalRequested` (EV-09) is not raised by a package-version approval, because that approval is not an item routed by the delegation of authority.

#### 12.5 Workflows and activities

None of this story's own. The load, the approve, the rollback and the reads are synchronous REST operations; the promotion is the JOB-20 Temporal Schedule of 12.6 and not a workflow; the embedded Drools kit is called in process at load and at promotion and never evaluates a case decision. This story registers nothing on the `rwb-decision` task queue, starts no workflow and adds no activity. The `RuleModelSwap` and `EvaluateRules` activities of the consuming services are theirs and are described in RWB-P3-E2042-CON.

#### 12.6 Schedules

| Schedule | When | Mechanism | Owner and this story's part |
|---|---|---|---|
| JOB-20 Rule promote | 00:01 | A Temporal Schedule on the `rwb-decision` queue that promotes every APPROVED version whose valid-from date has arrived to IN_FORCE, supersedes the version it replaces, writes the decision record and publishes `rwb.decision.RulePackageInForce.v1` (Arch v5 slide 44; Temporal and Drools slide 15) | P7 rwb-decision. This story implements the promotion handler and sits in the run; the Schedule itself is the workflow-kit registration of RWB-PLT-E1071-CON (DP-10) |

JOB-14, the 02:00 hash-chain check, is the decision-log story's and is not registered here. JOB-21, the stuck-workflow scan, is the platform's. No other Schedule is added by this story.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `rule_package` | P7 (`rwb_decision`) | The three Epic 2 package rows: code, title, owner role RW-COE and hit policy FIRST |
| `rule_package_version` | P7 (`rwb_decision`) | The version, its state, workbook reference, generated DRL, checksum, valid-from and valid-to dates, author, approver, test result, dry-run counts and rollback pointer |
| `rule_row` | P7 (`rwb_decision`) | The parsed, queryable catalogue of a version: rule ID, row order, condition and output columns, action text, owner role, timer spec and target queue code |
| `rule_test_case` | P7 (`rwb_decision`) | The test cases of a version with their expected and actual result |
| `decision_log_entry` | P7 (`rwb_decision`) | One append-only, hash-chained record per governance action |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects of the service (DP-09) |
| `approval` | P7 (`rwb_decision`) | Not read and not written: a package-version approval is four eyes and not a DoA approval (BR7) |

Not owned and not read: `recovery_case`, `task`, `timer` and `queue` (P3); `role`, `permission` and `delegation_limit` (P4); `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row` and `lov_value` (P3, read through DP-06 and DP-07); `document*` and `retention_rule` (P5); `proceeds` (P8); `write_off` (S7); `agent_*` (P10). No foreign key crosses a schema and no other service reads these six tables (DP-01). The four registry tables are declared for P4 and P3 in TSD P4 v3 T3.1 and TSD P3 v3 and are absent from TSD P7 v2 T3.1; the R-PREC default ruling and ASM-0069 put them in P7, recorded in GAP-1301 and ASM-2311. `payment_match_rule` does not exist in `rwb_decision`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case parameters and reference-data fake | RWB-P3-E1042-CON, RWB-P3-E1043-CON | `rules.testcases.min` = 50; LOV-DECISION and the version-state list with their versions; a `rules.testcases.min` of 60 to prove the gate reads the parameter rather than a constant |
| rwb-case authoring fake | RWB-P3-E2042-APP, RWB-P3-E1073-APP | The three workbooks of "RES-2026.12" (38 rows, 62 scenarios), "PMT-2026.12" (3 rows, 58 scenarios) and "BKG-2026.12" (21 rows, 54 scenarios); a RESTRUCTURE variant with a blank `timer_spec`; a PAYMENT_MATCH variant with PARTIAL at row order 2; a 49-scenario variant; an empty file; a repeated label; a `validFrom` before the business date |
| Drools kit fake | RWB-PLT-E1072-CON | The compile of a valid workbook, the checksum of the model, first-match semantics with the default row last, a compile failure and a checksum mismatch |
| decision-record library fake | RWB-PLT-E1027-CON | The append and the hash chain, the `DecisionRecorded` outbox row and a forced failure for the 503 and MSG-P7-003 cases |
| rwb-access guard fake | RWB-P4-E1037-CON, RWB-P4-E2042-APP | RW-COE with Rules and parameters C, R and U; RW-RISK with A; RW-AUDIT with R; RW-CASEOWN refused with MSG-P4-002 |
| workflow-kit fake | RWB-PLT-E1071-CON | The JOB-20 Schedule tick at 00:01 for 2026-12-14 and 2026-12-15 and the task-queue binding of `rwb-decision` |

Each fake is replaced by the real contract or library as its story lands, without a change to the scenarios. The fakes carry synthetic package codes, version labels, rule IDs and user references only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 8, consumed 2 | The package list, the load, the version list, the dry run, the approve, the rollback and the two decision-log reads provided; the parameters and the reference list consumed, one hop and 2 s |
| Kafka | Published 2 event types, consumed 0 | `rwb.decision.events.v1` with `RulePackageInForce`, and `rwb.decision-record.v1` with `DecisionRecorded` |
| Temporal | None | The promotion is the shared JOB-20 Schedule; this story registers no workflow and no activity |
| File | 3 inputs | The three xlsx workbooks with their Rows and Tests tabs, uploaded once per version as the body of the load; no runtime file exchange |

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
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How this story applies each row. **DP-01**: the four registry tables and `decision_log_entry` sit in `rwb_decision`; the story reads no schema of another service and no other service reads its tables — the rows travel as the model, the catalog and the event. **DP-03**: the load, the approval, the promotion and the rollback each write one local decision record and its outbox row in the same transaction; a record that cannot be written stops the action (BR11). **DP-04**: the load and the promotion use the embedded kit for the compile, the checksum and first-match semantics, and the registry supplies the package to the consuming services; the kit is a platform library and this story embeds it, while the consuming service's cache and swap are RWB-P3-E2042-APP's and are not rebuilt here. **DP-05**: no ACE view is read; the registry sees no customer, account or payment fact, and the dry-run counts carry no case identifier. **DP-06**: `rules.testcases.min` = 50 is read as a parameter and is never a constant, and the flag `rwb.p3.drools` is read the same way. **DP-07**: LOV-DECISION and the version-state list are read as reference data with the version in force; the match types, the row order, the thresholds and the three route-set fields stay row columns and are never reference data (BR13). **DP-10**: the promotion is the JOB-20 Temporal Schedule at 00:01, and this story implements its handler and registers no workflow of its own. **DP-13**: every path of section 12 uses `/api/recovery/decision/v1`; the monolith base appears nowhere. **DP-14**: the topic is `rwb.decision.events.v1`, the event is `rwb.decision.RulePackageInForce.v1`, and the queue is `rwb-decision` in namespace `rwb-recovery`. **DP-15**: the `rwb_decision` baseline, `V2_042_1__epic2_rule_packages.sql` and `V2_042_2__registry_constraints.sql` sit in this service's own Flyway sequence. **DP-19**: no screen is served here; SCR-39 reads the registry through gateway-bff in Epic 8, and the record of the route is the platform contract, not code of this story.

The platform H dependencies of the table — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — and the C dependencies C RWB-P7-E1073-CON, C RWB-P3-E1042-CON and C RWB-P3-E1043-CON are the DP-added dependencies that are **not** in the metadata rows, which name None and RWB-P3-E2042-CON. They are recorded in GAP-1296 and ASM-2306: they are platform contracts of wave 0 and published contracts of rwb-case and of this service, none of them blocks the build, and an APP story builds against the published set and its fake. **Ready to start therefore stays Day 1**: no DP-added H dependency is a same-lane story behind this one, and the only C dependency of the metadata is a published contract with a fake (R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RulePackageController | Controller | `GET /admin/rule-packages`: the guard, the scope, the package list and the problem mapping |
| RuleVersionController | Controller | The multipart load, the version list, the dry-run read, the approve and the rollback, with the Idempotency-Key and the 201, 200, 400, 404, 409 and 422 answers |
| RuleVersionService | Service | Orders the load in one transaction: parse, check, dry run, version row, rule rows, test cases, decision record |
| WorkbookParser | Service | Reads the Rows tab into `rule_row` candidates (RuleSet = package code, NAME = rule ID, default row last) and the Tests tab into `rule_test_case` candidates; rejects an empty or malformed workbook with MSG-GEN-001 |
| RuleCheckPipeline | Service | Compile, schema, overlap, unreachable row, default row and scenario checks in order; refuses the whole load with MSG-P3-027 and names the check, the row, the column and the failing test-case IDs |
| PaymentMatchOrderCheck | Validator extension | BR4: one row per match type and the order EXACT 1, WINDOW 2, PARTIAL 3; called from the schema check, not from a separate path |
| RestructureCatalogCheck | Validator extension | BR5: a non-empty `action_text`, `owner_role` and `timer_spec` on every RESTRUCTURE route-set row; called from the schema check |
| TestCaseRunner | Service | Runs the Tests tab against the compiled model, counts total, passed and failed, and records the expected and actual result of every case |
| DryRunService | Service | Runs the dry run on the business date, stores the counts in `dry_run_counts` and serves the per-case result of the dry-run read |
| ApprovalService | Service | Refuses the author with MSG-P7-002, moves LOADED to APPROVED with the approver and the time, writes the record |
| PromotionService | Schedule handler | On the JOB-20 run, promotes every APPROVED version whose valid-from date has arrived, supersedes its predecessor, writes the record and publishes `RulePackageInForce` |
| RollbackService | Service | Moves the pointer to the previous version in one call, marks the rolled-back version ROLLED_BACK, refuses a version with no predecessor with MSG-P3-015, writes the record |
| RuleRegistryRepository | Repository | The four tables in `rwb_decision`, the optimistic lock and the four unique keys of the migrations |
| DecisionLogController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the decision-log read, the scope and the hashes |
| DecisionRecordWriter | Service | The local record and its outbox row in the same transaction as the action (DP-03) |
| RegistrySchemaCheck | Schema gate | BR14: fails the build when `payment_match_rule`, or a column of DF-REF-261 to DF-REF-273, exists in the migrated `rwb_decision` |
| ParameterClient, ReferenceDataClient | Clients | The two consumed operations of 12.2, one hop with a 2 s timeout and a breaker |

**Database and migrations**

- Writes `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `decision_log_entry` and the library objects, all in schema `rwb_decision`; reads no other schema.
- `V2_042_1__epic2_rule_packages.sql` inserts the three `rule_package` rows (DF-REF-274 to DF-REF-278) with owner role RW-COE and hit policy FIRST. It is idempotent on `package_code` and writes no version, rule row or test case.
- `V2_042_2__registry_constraints.sql` adds the unique keys `ux_rule_package_code` (`package_code`), `ux_rule_package_version_label` (`package_id`, `version_label`), `ux_rule_row_version_order` (`package_version_id`, `row_order`) and `ux_rule_test_case_version` (`package_version_id`, `test_case_id`), so a repeated label, a duplicate row order and a duplicate test case are refused by the database as well as by the checks. It adds no column and writes no seed row.
- No migration of `rwb_decision` creates `payment_match_rule` and none adds a column of DF-REF-261 to DF-REF-273. There is no DROP of the table here: it never existed in this schema, and the drop of the monolith table is the schema owner's story, not this service's.
- An update of a version uses `WHERE id = ? AND version = ?`; zero rows updated is MSG-GEN-004 and the action is retried, never applied twice.

**Configuration and reference data**

- `rules.testcases.min` = 50 through the parameters contract of DP-06; the three Tests tabs hold 62, 58 and 54 cases, so each check passes with 12, 8 and 4 to spare.
- The three version labels, the row counts, the scenario counts and the valid-from date are the legacy values: "RES-2026.12" with 38 rows and 62 scenarios, "PMT-2026.12" with 3 rows and 58 scenarios and "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-15. RWB-E2-027 and its P7 story hold the same PAYMENT_MATCH package under "PM-2026.12" from 2026-12-01; the conflict is GAP-1297, and ASM-2307 pins this key to the legacy label and requires one reconciled version row before SIT.
- LOV-DECISION and the version-state list are read through DP-07 with the version in force; no decision code and no state is a constant in code. The decision code of a governance entry is Not specified in the source documents (GAP-1298; ASM-2308).
- The owner role RW-COE and the approver role RW-RISK are rows of the access model; the author and the approver must be distinct user references (BR7). The title of each package is Not specified in the source documents (GAP-1302; ASM-2312); the seed writes the package code as the title until RW-COE supplies one.
- The dry-run counts are stored and served, but their breakdown is Not specified in the source documents (GAP-1302; ASM-2312); the tests assert presence and stability, not a business number.
- The login phrase is "the rwb-decision login (DP-02)"; the name is Not specified in the source documents (GAP-1299; ASM-2309).

**Build steps**

1. `RuleRegistryRepository`, the schema baseline and the two migrations; test the four unique keys and the idempotent seed (AC1).
2. `WorkbookParser` and `TestCaseRunner` over the Rows and Tests tabs; tests for the malformed and empty workbook of X1, the default row of X4 and the 49-case variant of AC4.
3. `RuleCheckPipeline` with the six checks; tests for the compile, overlap and unreachable-row refusals of X4 and for the default-row refusal.
4. `PaymentMatchOrderCheck` and `RestructureCatalogCheck` wired into the schema check; tests for AC2's blank `timer_spec` and AC3's wrong order and unknown match type.
5. `DryRunService` and the scenario gate over `rules.testcases.min` read through DP-06; tests for AC4 and for a changed parameter value.
6. `RuleVersionService` with the single transaction and `DecisionRecordWriter`; tests for the load of AC2, AC3 and AC4 and for the fail-closed 503 of X12.
7. `ApprovalService` with the four-eyes rule and the LOADED to APPROVED transition; tests for AC5 and X10.
8. `PromotionService` on the JOB-20 run, with effective dating, the supersede step and the `RulePackageInForce` outbox row; tests for AC6, including a run before the date.
9. `RollbackService` with the one-call rollback, the previous-version pointer and the MSG-P3-015 refusal; tests for AC7.
10. `DecisionLogController` and the two reads; test for AC8 and for the record of every action.
11. `RegistrySchemaCheck` on a Testcontainers database migrated from empty; test for AC9, including a deliberately bad migration that creates the table and one that adds a retired column.
12. The privacy test: the workbooks, the rows, the test cases, the records and the two event payloads hold package codes, version labels, rule IDs, thresholds, dates and payment codes only, and no name, e-mail address, mobile number, national identity number or account number.

**Feature switch.** The legacy flag `rwb.p3.drools` is kept as the legacy reference and is read in the target as a parameter through DP-06. Off: the load, the approve and the rollback operations answer as unavailable, no version reaches IN_FORCE, and the registry and the decision log stay readable so the version already in force keeps running. The exact answer with the switch off is Not specified in the source documents (GAP-1302; ASM-2312).

**Done when.** The tests in section 16 pass; a SIT environment shows the three package rows with owner role RW-COE and hit policy FIRST; "RES-2026.12", "PMT-2026.12" and "BKG-2026.12" LOADED with 62, 58 and 54 passing scenarios; one refusal in full for a wrong match order and for a blank route-set field; the author's approve refused with MSG-P7-002 and RW-RISK's approve recorded; the three versions IN_FORCE from 2026-12-15 with one `RulePackageInForce` event each; one rollback that restores the previous version and leaves earlier decisions on the version they were taken under; and a migrated `rwb_decision` with no `payment_match_rule` table and no column of DF-REF-261 to DF-REF-273.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P3-027 | A workbook check fails, including the match order and the catalog completeness | The rule version was refused at the {check} check: {detail}. | This story, on the load and the version list |
| MSG-P7-002 | The author of a version calls approve | You prepared this decision, so you cannot approve it. | This story, on the approve |
| MSG-P3-015 | A rollback is called for a version with no predecessor | Not specified in the source documents (GAP-1302; ASM-2312) | This story, on the rollback |
| MSG-GEN-001 | An empty workbook, or a missing `validFrom` or required part | Enter {field}. | This story, on the load |
| MSG-GEN-003 | `validFrom` is before the business date | {field} cannot be before {other}. | This story, on the load |
| MSG-GEN-004 | The version label is already loaded, or the version changed at commit | Someone else changed this record. Reload it to see their change. | This story, on the load and the update |
| MSG-P7-003 | The decision record of an action cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every governance action |
| MSG-P4-002 | The role holds no right for the operation, or the version is outside its scope | You cannot {action} here. Your role does not include it. | This story, through the guard of the P4 story |

For MSG-P3-027 the `{check}` value is compile, schema, overlap, unreachable row, default row or scenario; the match order and the catalog completeness are part of the schema check. The `{detail}` names row IDs, cells, rule IDs, package codes, version labels and test-case IDs only, never a case fact or a person. The exact wording of the detail for the two Epic 2 checks is Not specified in the source documents (GAP-1300; ASM-2310): this story fixes the naming rule above and confirms the text with the business analyst before SIT. MSG-P3-015 is named by FSD P7 v3 A2.7 AC-EXC-P7-007-05 and its text is not written out in a source this story may read (GAP-1302; ASM-2312). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The registry is read through the operations of section 12.1; SCR-39 Rules and parameters (Epic 8) shows the same packages and versions through the gateway-bff composite route of DP-19, and this story feeds the states and the counts that screen consumes. The workbench screens of the load and the approval are the Epic 8 administration story's, and the rights behind them are RWB-P4-E2042-APP's.

| Where | State | What the caller sees |
|---|---|---|
| The package list | Seeded | RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH with owner role RW-COE and hit policy FIRST |
| The version list | LOADED | The version, its author, the checksum, the test result and the dry-run counts; not in force |
| The version list | APPROVED | The version and its approver; waiting for its valid-from date |
| The version list | IN_FORCE | The version, its valid-from date and its checksum, and the version it superseded |
| The version list | SUPERSEDED, ROLLED_BACK | The version, the date it stopped being in force and, for a rollback, the reason on the record |
| The version list | REFUSED, or no row | The refusal with MSG-P3-027 and the check that failed; the version in force is unchanged |
| The dry-run read | Counts | The dry-run counts and the per-test-case result of the version |
| The decision-log read | Record | The governance record with its inputs reference, rule ID, rule version, actor, final call, decided time and hashes |
| SCR-39 Rules and parameters (Epic 8) | List and detail | The same packages, versions and states; the screen is built by the Epic 8 story, not here |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01 | AC1, AC2, BR2, BR3, BR5, BR6 | Component | RESTRUCTURE "RES-2026.12", 38 rows, 62 scenarios, valid from 2026-12-15; route-set rows with R-RES-04 |
| TC-E2-042-02 | AC3, AC5, BR3, BR4, BR7 | Component | PAYMENT_MATCH "PMT-2026.12", 3 rows, 58 scenarios; EXACT 1, WINDOW 2, PARTIAL 3; a "PMT-2026.13" with PARTIAL at 2 |
| TC-E2-042-03 | AC4, AC6, BR6, BR8 | Component | BOOKING_MATCH "BKG-2026.12", 21 rows, 54 scenarios; a 49-scenario RESTRUCTURE variant |
| TC-E2-042-04 | AC3, AC5, AC7, BR4, BR7, BR9 | Component | The JOB-20 tick at 00:01 on 2026-12-14 and 2026-12-15; one rollback of "RES-2026.12" |
| TC-E2-042-05 | AC8, BR9, BR11, BR12 | Contract | The package list, the version list, the dry-run read and the decision-log read for RW-AUDIT |
| TC-E2-042-06 | AC9, BR14 | Contract | A `rwb_decision` database migrated from empty; no `payment_match_rule`; no column of DF-REF-261 to DF-REF-273 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component and the legacy Schema case to Contract; the registry half of each legacy case is proved here, and the `-ITG` copies of all six cases belong to RWB-ITG-E2042-ITG. The `Covers` column names the criteria and rules of this story that the case proves; the legacy AC1 to AC6 they derive from are owned by RWB-P3-E2042-APP, so no legacy criterion is claimed by a case of this story.

### 17. Guardrails

- No business value in code: the package rows, the labels, the valid-from dates, the row order, the match types, the thresholds, `action_text`, `owner_role`, `timer_spec` and `rules.testcases.min` are rows and parameters; only the check names and the version-state vocabulary are fixed by design.
- No personal data in logs, events, workflow history, tests or prompts: the rows, the test cases and the records hold package codes, version labels, rule IDs, thresholds, dates and synthetic payment codes only.
- No read of another service's tables, and no other service reads `rwb_decision` (DP-01): the parameters and the reference lists arrive on their operations, a case fact never enters the registry, and the dry-run counts carry no case identifier.
- The decision record is written before the action commits; no version exists, no version is approved, promoted or rolled back without its record (BR11).
- One registry, one evaluator: this story governs and stores; the consuming service evaluates through its own embedded Drools kit (DP-04). This story never evaluates a package for a business decision and never caches a KieBase.
- A version is never edited in place: a change is a new version, the workbook and the DRL are stored by reference and checksum, and a rollback moves the pointer.
- The version states are the six of BR10 and the check names are the seven of BR3; no other value is written and none is a constant of the code beyond the state machine.
- `payment_match_rule` is never created and DF-REF-261 to DF-REF-273 are never referenced by a migration, a test, a query or a document of this service; the schema check fails the build on any attempt.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD, and the schema check reads only `rwb_decision`.
- No secret in a workbook, a record or the run material: the rwb-decision login (DP-02) and the certificate come from the platform secret store, and the test data is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call | Epic 1, section 4 and Program, section 5.3; the legacy pointer to Epic 1 3.3 and Epic 2 3.2/3.8 is out of date in BRD v2 (GAP-1303; ASM-2313) | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38; R-RES-26 | TC-E2-042-01, TC-E2-042-02, TC-E2-042-04, TC-E2-042-05, TC-E2-042-06 |
| REQ-CWC-014 | Rule loads are validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect | Epic 1, section 4 and Program, section 5.3; the same legacy pointer is out of date (GAP-1303; ASM-2313) | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26; R-RES-04 | TC-E2-042-01 to TC-E2-042-05 |

- ADR-017: embedded Drools per service and the rule registry in rwb-decision — Arch v5 slide 27; this story is the registry and governance half of RWB-E2-042.
- ADR-022: a local decision record plus the central ledger — each governance action writes a record on `rwb.decision-record.v1` and the central entry is collected in this service (DP-03).
- D-RCV-36 T3 to T7: authoring, test, four-eyes approval, effective dating and version audit — inherited through the registry and exercised by the load, the approval and the promotion.
- D-RCV-36 T10: `payment_match_rule` is retired and DF-REF-261 to DF-REF-273 stay retired — asserted by AC9.
- D-RCV-60: the realignment that splits RWB-E2-042 into the P3, P4, P6, P7 and ITG stories; the P7 registry slice is this story.
- RWB-P3-E2042-CON: the contract this story provides the registry side of; RWB-P3-E2042-APP and RWB-P3-E1073-APP own the authoring artefacts this story consumes.

The requirement text is that of Business Requirements Epic 1 v4 (REQ-CWC-013 and REQ-CWC-014) and Program v4; the section pointers in the legacy story no longer match BRD v2, where the P7 requirements are section 3.7 and the requirement set sits in Epic 1 section 4 and Program section 5.3. The mismatch is recorded in GAP-1303 and read as ASM-2313 rather than corrected silently; no requirement ID and no requirement text changes.

### 19. Out of scope

- The workbook authoring, the Rows and Tests tabs, the write-once Blob object and its SHA-256 metadata, the three xlsx files and their Tests tabs — RWB-P3-E2042-APP and RWB-P3-E1073-APP.
- The model cache, the checksum-verified swap, the atomic pointer and `RuleScenarioBuildGate` — RWB-P3-E2042-APP and RWB-P3-E1073-APP. This story runs its own load pipeline and no build gate.
- The model read and the catalog read that a consuming service calls — the P7 rule-package contract story RWB-P7-E1073-CON; this story supplies the rows and publishes the event.
- The evaluation of the three packages in the engines that own those decisions: PAYMENT_MATCH in JOB-07 (RWB-E2-027 and the rwb-payment stories), BOOKING_MATCH in the booking confirmation (RWB-E2-007), RESTRUCTURE in the treatment stage (RWB-E2-002, RWB-E2-004, RWB-E2-035). This story never evaluates a package.
- The screens, the load and approval screens, the roles, the permission matrix and the delegation of authority — RWB-P4-E2042-APP, RWB-P4-E1037-CON and the Epic 8 administration stories. This story declares the right and holds no role row.
- The notices and the assertion that a rule change raises none — RWB-P6-E2042-APP.
- The change checklist and the rule change report — RWB-E2-041.
- The remaining 448 routing rules, the UNIVERSAL package and the Phase 2 packages of S1 and S3 to S9 — Epic 3 and DL24.
- The decision-log query screen, the ledger seal and the JOB-14 chain check — the decision-log stories of this service and the Epic 8 screen.
- The real cross-service proof of the load, the approval, the promotion, the rollback and the decision record across the services — RWB-ITG-E2042-ITG.
- The retired `payment_match_rule` table, its drop in the monolith schema and its thirteen field IDs: this story never creates, drops or reads them, and only asserts their absence in `rwb_decision`.
- The field-level completeness of the model and catalog resources (GAP-1296; ASM-2306), the package titles, the dry-run breakdown and the MSG-P3-015 text (GAP-1302; ASM-2312), which are confirmed with their owners before SIT.
