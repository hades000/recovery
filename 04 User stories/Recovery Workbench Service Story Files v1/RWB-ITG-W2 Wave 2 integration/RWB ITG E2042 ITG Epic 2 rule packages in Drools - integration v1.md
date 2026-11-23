# RWB-ITG-E2042-ITG Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2042-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2042-APP, RWB-P6-E2042-APP, RWB-P4-E2042-APP, RWB-P7-E2042-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020) |
| Status | Draft (realignment v1) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that loads the three Epic 2 packages, approves each version as a second user, promotes them at 00:01 and then reads what each owning service decided from the version in force**, so that **the wave 2 rule package journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production operation, table, workflow, schedule or screen, it serves no operation and it owns no table. The real behaviour is owned by the four I stories: RWB-P7-E2042-APP (the three package rows, the load, approve, dry-run and registry reads, the rule rows and the 00:01 promotion in rwb-decision), RWB-P3-E2042-APP (`rules.testcases.min` and the match-type and route-set reference rows), RWB-P6-E2042-APP (the notice path, which the harness asserts stays silent) and RWB-P4-E2042-APP (the Rules and parameters right answered on every call), and those four stories block the ITG run.

The packages themselves are evaluated locally by the one service that owns each model, from the version in force, inside an activity (DP-04, ADR-017). The harness asserts the decision records those services wrote; it never evaluates a package, never recomputes a match and holds no copy of a rule row.

### 2. Business rationale

In v5 governance is central in P7 rwb-decision: the workbook is authored in the Drools template, compiled and checked against at least 50 scenarios, approved four-eyes, dated, and every version is audited. Evaluation is local: each model has exactly one owning service, which loads the approved version, verifies its checksum, swaps it in atomically and keeps the last good model, all inside an activity and under 300 ms. There is no shared rule server on the hot path, so a rule change is data rather than code, it is dated, and the version is stamped on every answer.

The legacy RWB-E2-042 left Epic 2 rules in three places: reference rule rows, the `payment_match_rule` table and the BookingMatchRules class. The harness proves the loop that replaced them: a load and a four-eyes approval in rwb-decision, a promotion at 00:01 with `rwb.decision.RulePackageInForce.v1`, a local swap in each owning service, a decision record naming the rule ID and the rule version, the first-match order of PAYMENT_MATCH proven from the records rather than recomputed, and no customer-facing notice raised by any of it. That is the outcome REQ-CWC-013 and REQ-CWC-014 describe, shown at the integration level rather than per service.

A run gives one evidence report per business date that proves the 50-scenario gate holds for all three packages, that the three package codes and their row counts are the ones in force, that R-RES-04 carries the three fields the route service reads, that the row order decides the two payments the same way the ledger says, and that every refusal writes nothing.

### 3. Preconditions

- The four I stories are published and deployed in the SIT environment: RWB-P7-E2042-APP (the package rows, the load and approve paths, the registry and decision log reads and the promotion), RWB-P3-E2042-APP (`rules.testcases.min` and the reference rows), RWB-P6-E2042-APP (notices and their events) and RWB-P4-E2042-APP (the Rules and parameters right on the authorise operation).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before the I stories land.
- The three package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE, and the three versions are "RES-2026.12" with 38 rows and 62 scenarios, "PMT-2026.12" with 3 rows and 58 scenarios and "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-15.
- The business date is 2026-12-10; the loader is "U-41" (RW-COE) and the approver is "U-51" (RW-RISK), and they are separate users; `rules.testcases.min` is 50.
- Rule R-RES-26 carries the match types EXACT, WINDOW and PARTIAL; payment "PAY-91008" of 12,500.00 THB is matched by both EXACT and WINDOW and is decided by EXACT, and payment "PAY-91002" of 11,875.00 THB is decided by PARTIAL with a shortfall of 625.00 THB. Rule R-RES-04 carries action text "Assign the case to a restructuring officer and start the offer clock", owner role "RW-RESTRUCT" and timer "2 working days", and case "RW-2026-000777" is open.
- The production switch `rwb.p3.drools` is on in the harness environment; with it off the three package endpoints and the row reads answer 404 or NoPackageInForce and nothing else changes.
- The harness repository, the SIT environment, the seeding set for the three versions and the two payment cases, the evidence format and retention, the pass or fail gate and the exact response values of the §12.8 fakes: Not specified in the source documents (GAP-0421; ASM-0596).

### 4. Flow

1. Harness: seeds the three package versions with the two users and their roles through the owning contracts or the published fakes, and reads each version back to assert status LOADED, the row count 38, 3 and 21 and the scenario count 62, 58 and 54.
2. Harness: loads each version through POST `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` as "U-41" with valid from 2026-12-15, and asserts 201, status LOADED, the checksum and the test result "62 of 62", "58 of 58" and "54 of 54 scenarios passed".
3. Harness: asserts the compile, schema, overlap, unreachable row, default row, scenario and dry run checks pass on each version, that the dry run covers the open cases and the payments of the business date, and that each version carries at least `rules.testcases.min` scenarios, read through GET `/api/recovery/case/v1/admin/parameters`.
4. Harness: reads GET `/api/recovery/decision/v1/admin/rule-packages` and asserts exactly the three package codes with owner role RW-COE and no fourth Epic 2 package, then GET `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` and asserts 38 rows under "RES-2026.12" including R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, the rows EXACT, WINDOW and PARTIAL under "PMT-2026.12" and 21 rows under "BKG-2026.12".
5. Harness: approves each version as "U-51" on 2026-12-14 through POST `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve`, asserts status APPROVED with author "U-41" and approver "U-51", and asserts that the same call as "U-41" is refused with MSG-P7-002.
6. Harness: promotes each approved version at 00:01 on 2026-12-15 through the `rulePackagePromote` Schedule in rwb-decision, and asserts status IN_FORCE with the earlier version SUPERSEDED and exactly one `rwb.decision.RulePackageInForce.v1` per package on `rwb.decision.events.v1`, naming the package, the version and its checksum.
7. Harness: asserts the version in force in each owning service is the promoted version and the row counts are 38, 3 and 21 through the registry contract, then asserts the priority order EXACT then WINDOW then PARTIAL and the two payment outcomes from the decision records read through GET `/api/recovery/decision/v1/decision-log`, with rule "R-RES-26" and rule version "PMT-2026.12" on each record; it never recomputes a match.
8. Harness: asserts R-RES-04 as the row the route service reads, with action text "Assign the case to a restructuring officer and start the offer clock", owner role "RW-RESTRUCT" and timer "2 working days", and that every route-set row of the version carries the three fields, read through the registry contract and the route-set reference rows of GET `/api/recovery/case/v1/admin/lists/{listCode}`.
9. Harness: asserts that every call is one hop on `/api/recovery/<short>/v1` with the 2 s budget and a breaker per downstream, that the Rules and parameters right is answered by POST `/api/recovery/access/v1/authorise` on every call, that no service reads another service's schema, and that the deploy-time check rwb-decision publishes for its own schema reports no `payment_match_rule` table and no column of DF-REF-261 to DF-REF-273.
10. Harness: asserts that no `rwb.comms.NoticeGenerated.v1` and no `rwb.comms.NoticeDispatched.v1` appears on `rwb.comms.events.v1` during the load, the approval and the promotion, so a rule change raises no customer-facing notice.
11. Harness: forces each refusal and failure of §5 through the fakes, asserts the message and that nothing was written, then returns the fake to its healthy answer.
12. Harness: writes one evidence report per business date, keyed by story and business date, with the trace of every call; the report format and retention are Not specified in the source documents (GAP-0421; ASM-0596).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A compile or schema check fails: a PAYMENT_MATCH row carries match type "FUZZY" | The load is refused with 422, the row and the cell are named, and no version row and no rule row is written | MSG-P3-027 | TC-E2-042-02-ITG |
| X2 | A RESTRUCTURE version carries 49 scenarios, below `rules.testcases.min` = 50 | The load is refused with 422, the scenario check and the shortfall are named, and status stays absent | MSG-P3-027 | TC-E2-042-01-ITG |
| X3 | The PAYMENT_MATCH row order puts PARTIAL before WINDOW | The load is refused at the schema check with 422, the priority cells are named, and nothing is written | MSG-P3-027 | TC-E2-042-04-ITG |
| X4 | A RESTRUCTURE route-set row has an empty action text, owner role or timer | The load is refused with 422 and the row and column are named | MSG-P3-027 | TC-E2-042-05-ITG |
| X5 | "U-41" approves a version they loaded | The approval is refused and the version stays LOADED; no approver and no approved time is written | MSG-P7-002 | TC-E2-042-01-ITG |
| X6 | The same version label is loaded twice, or an empty workbook is loaded | 409 for the duplicate label and 422 for the empty workbook; the version in force is unchanged | MSG-GEN-004; MSG-GEN-001 | TC-E2-042-01-ITG |
| X7 | The valid from date is before the business date (2026-12-09 with the run on 2026-12-10) | 422 and no version row; the version label is not consumed | MSG-GEN-003 | TC-E2-042-02-ITG |
| X8 | A role with no Rules and parameters right calls a package path, or the decision log does not answer | 403 on the direct call with the refusal and not an empty list; 503 on the read with no record written and no record invented | MSG-P4-002; None (503 refusal text) | TC-E2-042-06-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the four I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the seeding, the evidence format and the gate are agreed with QA; no business value is fixed by the harness |
| Valuable | The author, test, four-eyes, promotion, local swap and decision-record loop is evidenced across services rather than per service |
| Estimable | One harness project, one journey specification, one fake pack and one evidence report per business date |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages in Drools - wave 2 integration harness

  Background:
    Given the business date is 2026-12-10
    Given the loader "U-41" holds RW-COE and the approver "U-51" holds RW-RISK
    Given package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE
    Given rules.testcases.min is 50

  Scenario: AC1 Load, approve and promote the three versions, and every decision names the rule and the version (new, D-RCV-60)
    Given a RESTRUCTURE version "RES-2026.12" with 38 rows and 62 scenarios, a PAYMENT_MATCH version "PMT-2026.12" with 3 rows and 58 scenarios and a BOOKING_MATCH version "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-15
    When "U-41" loads each version with valid from 2026-12-15
    Then each version is LOADED with its checksum and its test result "62 of 62", "58 of 58" and "54 of 54 scenarios passed"
    And the compile, schema, overlap, unreachable row, default row, scenario and dry run checks pass on each version
    When "U-51" approves each version on 2026-12-14
    Then each version is APPROVED with author "U-41" and approver "U-51"
    And the same approval as "U-41" is refused with MSG-P7-002
    When the rulePackagePromote Schedule runs as JOB-20 at 00:01 on 2026-12-15 on queue rwb-decision
    Then each version is IN_FORCE and the version each owning service holds is the promoted version
    And exactly one rwb.decision.RulePackageInForce.v1 per package is on rwb.decision.events.v1, naming the package, the version and its checksum
    And every decision record read through GET /api/recovery/decision/v1/decision-log names the rule ID and the rule version that decided it
    And every call in the run is one hop with the 2 s budget and a breaker per downstream
    And no service reads another service's schema and the harness reads the version in force through the rwb-decision contract only
    And the run report holds one trace spanning rwb-decision, rwb-case, rwb-source-data, rwb-access and rwb-comms

  Scenario: AC2 The first-match order and the two payment outcomes, read from the decision records and never recomputed (new, D-RCV-60)
    Given PAYMENT_MATCH version "PMT-2026.12" is in force on 2026-12-15
    Given payment "PAY-91008" of 12,500.00 THB matches both the EXACT and the WINDOW row, and payment "PAY-91002" of 11,875.00 THB is 625.00 THB short
    When the harness reads the decision records of the business date through GET /api/recovery/decision/v1/decision-log
    Then the rows are recorded in the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3
    And "PAY-91008" is decided by EXACT and "PAY-91002" is decided by PARTIAL with a shortfall of 625.00 THB
    And each record names rule "R-RES-26" and rule version "PMT-2026.12"
    And the payment decisions of the date reconcile one for one with the ledger entries for the same business date and version
    And the harness evaluates no package, holds no copy of a rule row and recomputes no match

  Scenario: AC3 The 50-scenario gate, the three package codes, the row counts and the schema assertion (new, D-RCV-60)
    Given the three versions carry 62, 58 and 54 scenarios and every scenario passes
    When the harness reads GET /api/recovery/decision/v1/admin/rule-packages
    Then the answer names RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH and no fourth Epic 2 package
    And GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions returns 38 rows under "RES-2026.12", the rows EXACT, WINDOW and PARTIAL under "PMT-2026.12" and 21 rows under "BKG-2026.12"
    And each version carries at least rules.testcases.min scenarios read through GET /api/recovery/case/v1/admin/parameters
    And the deploy-time schema check rwb-decision publishes for its own schema reports no payment_match_rule table and no column of DF-REF-261 to DF-REF-273
    And the check runs on the owner's own schema and the harness reads no schema catalogue of another service

  Scenario: AC4 Refusals and failure isolation, with nothing written and no notice raised (new, D-RCV-60)
    Given a PAYMENT_MATCH version whose row carries match type "FUZZY", a RESTRUCTURE version with 49 scenarios and a PAYMENT_MATCH version whose row order puts PARTIAL before WINDOW
    When "U-41" loads each of them
    Then each load is refused with MSG-P3-027 naming the check and the row, and no version row and no rule row is written
    Given a RESTRUCTURE version with an empty action text on a route-set row
    When "U-41" loads it
    Then the load is refused with MSG-P3-027 naming the row and the column
    Given version "RES-2026.12" is already loaded
    When "U-41" loads "RES-2026.12" again and then loads an empty workbook
    Then the first call is refused with MSG-GEN-004 and the second with MSG-GEN-001
    When "U-41" loads a version with valid from 2026-12-09
    Then the load is refused with MSG-GEN-003
    When the harness repeats each call of this scenario as "RW-CASEOWN", a role with no Rules and parameters right
    Then every call is refused with 403 and MSG-P4-002
    And no package version row, no rule row, no rule test case and no decision record is written by any refused call
    And no rwb.comms.NoticeGenerated.v1 and no rwb.comms.NoticeDispatched.v1 appears on rwb.comms.events.v1 during the run
    And when the decision log does not answer, the run reports the failure and writes no record of its own
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the four I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each Epic 2 package is authored in the Drools XLS template and loaded only through rwb-decision; no direct SQL and no second load path | D-RCV-36 T3, T4 |
| BR2 | Each package version carries at least `rules.testcases.min` (50) scenarios, and every scenario passes before approval | REQ-CWC-014; D-RCV-36 T4 |
| BR3 | PAYMENT_MATCH has one row per match type, and the row order is EXACT then WINDOW then PARTIAL | R-RES-26; D-RCV-36 T10 |
| BR4 | RESTRUCTURE route-set rows carry action text, owner role and timer, and the route service reads them only from the catalog | D-RCV-36 T6; FEAT-CWC-28 |
| BR5 | `payment_match_rule` is never created and DF-REF-261 to DF-REF-273 are never referenced; no code, rule row or test reads or writes them | D-RCV-36 T10 |
| BR6 | The package code is the RuleSet and the version labels are RES-, PMT- and BKG-yyyy.MM | D-RCV-36 T5 |
| BR7 | First match wins, exactly one row decides, and the default row is last | D-RCV-36 T5 |
| BR8 | Open cases keep the package version they were decided under | R-UNI-38 |
| BR9 | The build gate runs every in-force package's scenarios in every build | REQ-CWC-014; D-RCV-36 T4 |

The harness asserts these nine rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None. The harness sets no package version state and changes no case status; it calls the owning service and reads the result. The table is what it observes on a package version, and it reads the state, it never sets it.

| Observed state | What it means in the run | Where the harness reads it |
|---|---|---|
| LOADED | The workbook compiled, the checks passed and at least 50 scenarios passed, so the version is stored but not approved | The load answer and the version list of rwb-decision |
| APPROVED | A second user approved the version; the author "U-41" never approves | The approve answer and the version list of rwb-decision |
| IN_FORCE | The 00:01 promotion reached the valid from date, the previous version became SUPERSEDED and the owning service swapped the version in | The version list, `rwb.decision.RulePackageInForce.v1` and the decision records of the date |
| SUPERSEDED | An earlier version was replaced by the promoted one and stays readable for the cases decided under it | The version list of rwb-decision |
| REFUSED | A load or an approval was refused, and no version row, rule row or test case was written | The refusal answer and the version list before and after it |

A refused load or approval leaves every row exactly as it was before the call, and a version in force changes only through the promotion the owning service starts and announces.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | The synthetic user the harness drives to load a version (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves each package version (Rules and parameters A); the harness asserts that the approver is not the author |
| RW-AUDIT, internal audit | Reads the versions, the rows, the scenarios and the dry run counts (Rules and parameters R); changes nothing |
| RW-PLATADM, platform administrator | Reads the same answers (Rules and parameters R); used by the access case only |
| RW-CASEOWN, case owner | Holds no Rules and parameters right; the access case proves the refusal with MSG-P4-002 |
| SY-RULES, Drools evaluator | Evaluates the version in force inside the owning service and writes the rule ID and version to the decision record; the harness asserts its result, it does not act for it |

No delegation of authority level applies: a package version is not a credit decision. Authorisation is answered by rwb-access through the authorise operation of §12.2.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package | id | Read through rwb-decision contract |
| DF-REF-275 | rule_package | package_code | Read through rwb-decision contract |
| DF-REF-276 | rule_package | title | Read through rwb-decision contract |
| DF-REF-277 | rule_package | owner_role | Read through rwb-decision contract |
| DF-REF-279 | rule_package_version | id | Read through rwb-decision contract |
| DF-REF-281 | rule_package_version | version_label | Read through rwb-decision contract |
| DF-REF-282 | rule_package_version | status | Read through rwb-decision contract |
| DF-REF-285 | rule_package_version | checksum | Read through rwb-decision contract |
| DF-REF-286 | rule_package_version | valid_from | Read through rwb-decision contract |
| DF-REF-288 | rule_package_version | author | Read through rwb-decision contract |
| DF-REF-289 | rule_package_version | approver | Read through rwb-decision contract |
| DF-REF-290 | rule_package_version | loaded_at | Read through rwb-decision contract |
| DF-REF-291 | rule_package_version | approved_at | Read through rwb-decision contract |
| DF-REF-292 | rule_package_version | test_result | Read through rwb-decision contract |
| DF-REF-293 | rule_package_version | dry_run_counts | Read through rwb-decision contract |
| DF-REF-002 | rule_row | rule_id | Read through rwb-decision contract |
| DF-REF-008 | rule_row | action_text | Read through rwb-decision contract |
| DF-REF-010 | rule_row | owner_role | Read through rwb-decision contract |
| DF-REF-011 | rule_row | timer_spec | Read through rwb-decision contract |
| DF-REF-052 | rule_row | rule_table | Read through rwb-decision contract |
| DF-REF-053 | rule_row | row_order | Read through rwb-decision contract |
| DF-REF-054 | rule_row | target_queue_code | Read through rwb-decision contract |
| DF-REF-296 | rule_row | package_version_id | Read through rwb-decision contract |
| DF-REF-297 | rule_row | drools_rule_name | Read through rwb-decision contract |
| DF-REF-185 to DF-REF-197 | rule_test_case | all fields | Read through rwb-decision contract |
| DF-REF-299 | rule_test_case | package_version_id | Read through rwb-decision contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read through rwb-decision contract |
| DF-DEC-005 | decision_log_entry | rule_version | Read through rwb-decision contract |
| DF-DEC-016 | decision_log_entry | decided_at | Read through rwb-decision contract |
| DF-CAS-001 | recovery_case | id | Read through rwb-case contract |
| DF-CAS-005 | recovery_case | status | Read through rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Read through rwb-case contract |
| DF-ACE-043 | v_ace_payment | payment_code | Read through rwb-source-data contract |
| DF-ACE-044 | v_ace_payment | account_key | Read through rwb-source-data contract |
| DF-ACE-045 | v_ace_payment | payment_date | Read through rwb-source-data contract |
| DF-ACE-046 | v_ace_payment | payment_amount | Read through rwb-source-data contract |

The case facts and the two payments the dry run and the decisions cover are read through rwb-source-data, never from an ACE view by the harness. Test data is synthetic. No production case, party, payment or package version is copied, and no personal data is written to an evidence report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of Architecture v5 slide 11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The load of each of the three versions with its workbook and valid from 2026-12-15 (Architecture v5 slide 27: author and test) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version in force, its status, its row count and the rule rows that R-RES-04, R-RES-26 and the route-set rows are asserted from |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | P7 rwb-decision | The four-eyes approval by "U-51" and the refusal when the author approves (Architecture v5 slide 27: four-eyes sign-off) |
| GET | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run` | P7 rwb-decision | The dry run counts over the cases and payments of the business date, before approval |
| GET | `/api/recovery/decision/v1/admin/rule-packages` | P7 rwb-decision | The three package codes with owner role RW-COE, and the absence of a fourth Epic 2 package |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision records the rule ID, the rule version and the two payment outcomes are asserted from (Architecture v5 slide 14: central decision ledger) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | `rules.testcases.min` = 50, the gate every version is held to (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The match types EXACT, WINDOW and PARTIAL and the route-set reference rows (DP-07) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The case facts and the two payments the dry run and the decisions cover (DP-05) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters right checked on every call (Architecture v5 slide 14: rwb-access IN POST /authorise) |

The composite screen route is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order, and any gateway call this run makes, are Not specified in the source documents (GAP-0421; ASM-0596).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | One event per package at 00:01 on 2026-12-15, naming the package, the version and its checksum, and each owning service holds the new version only after it |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | Every payment and route decision of the business date reaches the ledger with its rule ID and rule version, and the decision log count matches |
| rwb.comms.NoticeGenerated.v1 | rwb.comms.events.v1 | P6 rwb-comms | Asserted absent: no notice is generated by a load, an approval or a promotion |
| rwb.comms.NoticeDispatched.v1 | rwb.comms.events.v1 | P6 rwb-comms | Asserted absent: no notice reaches a delivery channel for a rule change |

The events are consumed for assertion only; the harness reads the ledger through the P7 contract rather than from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only. The `rulePackagePromote` Schedule and the promotion it starts in rwb-decision, and the build gate that runs every in-force package's scenarios, are owned and started by the owning services; the harness observes their result.

#### 12.6 Schedules

None added. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow. The 00:01 promotion Schedule `rulePackagePromote` (JOB-20, queue rwb-decision) is exercised as an observer of the run: the harness waits for its window and asserts `rwb.decision.RulePackageInForce.v1`.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-decision | rule-packages, rule-packages/{packageCode}/versions, rule-package-versions/{versionId}/approve, rule-package-versions/{versionId}/dry-run, decision-log | RESTRUCTURE "RES-2026.12" with 38 rows and 62 scenarios, PAYMENT_MATCH "PMT-2026.12" with 3 rows and 58 scenarios and BOOKING_MATCH "BKG-2026.12" with 21 rows and 54 scenarios, all LOADED then APPROVED by U-51 then IN_FORCE from 2026-12-15; rule R-RES-04 with its three fields; the rows EXACT priority 1, WINDOW priority 2, PARTIAL priority 3; PAY-91008 decided by EXACT and PAY-91002 by PARTIAL with 625.00 THB short; 422 for MSG-P3-027 and MSG-GEN-003, 409 for MSG-GEN-004, 401 and 403 for MSG-P4-002, and a forced 503 for the decision log failure |
| rwb-case | admin/parameters, admin/lists/{listCode} | `rules.testcases.min` = 50; the match types EXACT, WINDOW and PARTIAL; the route-set reference rows with their action text, owner role and timer; case "RW-2026-000777" open |
| rwb-source-data | data-products/{productCode}/records | The case facts of "RW-2026-000777" and the two payments of 12,500.00 THB and 11,875.00 THB on 2026-12-15 |
| rwb-access | authorise | Allow RW-COE, RW-RISK, RW-AUDIT and RW-PLATADM with their Rules and parameters rights; refuse RW-CASEOWN for Rules and parameters with MSG-P4-002 |
| rwb-comms | the two notice events | No `NoticeGenerated` and no `NoticeDispatched` for any business date of the run, so a notice raised by a rule change fails the run |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness repository, its environment and seeding, its evidence format and retention, the pass or fail gate and the exact response values of these fakes: Not specified in the source documents (GAP-0421; ASM-0596).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | The ten consumed operations of §12.2 through the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision.RulePackageInForce.v1, rwb.decision-record.DecisionRecorded.v1 and the two rwb-comms notice events for the promotion, ledger and silence assertions; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the 00:01 promotion Schedule and the build gate |
| File | No | The workbook is uploaded as the body of the load call; the harness writes no file to a service and reads no workbook back |

### 13. Solution plan

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

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the four I stories.

The legacy P3 module that held the rule packages, the loader and the effective-date job splits in two: governance (authoring, tests, four-eyes approval, effective dating and the version audit) moves to P7 rwb-decision, and evaluation moves into the one service that owns each model, as an embedded Drools kit inside an activity (DP-04, ADR-017). The Quartz effective-date job becomes the 00:01 Temporal Schedule `rulePackagePromote` in rwb-decision (DP-10). The single recovery schema becomes the per-service `rwb_<name>` schemas with their own Flyway sequences (DP-01, DP-15), the `rwb.p3.` topic names become `rwb.<short>.events.v1` (DP-14), `rules.testcases.min` and the reference rows are read through rwb-case (DP-06, DP-07), the payment and case facts through rwb-source-data (DP-05), the monolith base becomes `/api/recovery/<short>/v1` (DP-13) and the screen answer is composed by the gateway-bff route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| PackageClient | Harness adapter | Calls the ten consumed operations of §12.2 for the load, the approval, the dry run, the package and version reads, the registry read, the decision log and the authorise call |
| FakePack | WireMock project | Serves rwb-decision, rwb-case, rwb-source-data, rwb-access and rwb-comms from the published OpenAPI documents of §12.8 |
| ScenarioGateCheck | Assertion | Fails the run when a version carries fewer than 50 scenarios, when a scenario fails, or when the three package codes and the row counts 38, 3 and 21 are not the ones in force |
| FourEyesCheck | Assertion | Fails the run when the approver equals the author, or when a refused approval writes an approver or an approved time |
| DecisionRecordReconciler | Assertion | Compares every decision record of the date with the rule ID and the rule version it must name, and the two payment outcomes with the ledger, and fails the run on any difference; it recomputes nothing |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference in the trace, and asserts the deploy-time schema check rwb-decision publishes for its own schema, without reading a catalogue of another service |
| NoticeSilenceCheck | Assertion | Fails the run when a `NoticeGenerated` or `NoticeDispatched` event appears for a load, an approval or a promotion |
| RunReportWriter | Reporter | Writes one evidence report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0421; ASM-0596) |

**Environment and test data**

- Environment: SIT, one namespace, the four I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0421; ASM-0596).
- Data: the three package codes and versions "RES-2026.12" with 38 rows and 62 scenarios, "PMT-2026.12" with 3 rows and 58 scenarios and "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-15; users "U-41" and "U-51"; `rules.testcases.min` = 50; rule R-RES-26 with EXACT, WINDOW and PARTIAL; rules R-RES-04 and R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02; payments "PAY-91008" of 12,500.00 THB and "PAY-91002" of 11,875.00 THB; case "RW-2026-000777"; the business date 2026-12-10 and the promotion date 2026-12-15.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same evidence report is produced. The seeding order and the seeding script: Not specified in the source documents (GAP-0421; ASM-0596).

**Build steps**

1. Build JourneyRunner and PackageClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the five services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the load, the checks, the 50-scenario gate and the four-eyes approval of AC1 and AC3 with ScenarioGateCheck and FourEyesCheck.
4. Add the 00:01 promotion, the `RulePackageInForce` wait and the local swap assertion of AC1.
5. Add the first-match order, the two payment outcomes and the ledger reconciliation of AC2 with DecisionRecordReconciler, and the R-RES-04 route-set assertion of AC3.
6. Add the refusals of AC4 for a wrong match type, 49 scenarios, a wrong row order, a blank catalog field, a duplicate label, an empty workbook, a valid from before the date and a role without the right, and assert that nothing was written.
7. Add the notice silence assertion and the decision log failure of X8, replace each fake with the real service as its I story lands, then publish the evidence report per business date and the pass or fail gate; the gate definition: Not specified in the source documents (GAP-0421; ASM-0596).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.p3.drools` from the legacy solution plan; with the flag off the three package endpoints and the row reads answer 404 or NoPackageInForce and nothing else changes, and the harness asserts the disabled and the enabled state.

**Done when:** the journey runs green against the four deployed I stories in SIT, the evidence report for the business date holds every assertion of §7 and §16 with its trace, the three versions are in force from 2026-12-15 with 174 passing scenarios, the two payment outcomes reconcile with the ledger, and the pass or fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A workbook check fails, including the match order and the catalog completeness | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-001 | An empty workbook | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-P4-002 | A role without the right calls a package endpoint | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values, including "compile", "schema" and "scenario" for {check} and the row and cell for {detail}, and the version label and the two dates in MSG-GEN-003; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-39 Rules and parameters | Version list | The answer the screen consumes: the three package codes, their versions with status IN_FORCE from 2026-12-15, the row counts 38, 3 and 21 and the test result of each version |
| SCR-39 Rules and parameters | Version detail | The rule rows the screen lists, including R-RES-04 with its action text, owner role and timer, and the PAYMENT_MATCH rows in the order EXACT, WINDOW, PARTIAL |
| SCR-39 Rules and parameters | Refusal | The refusal answer of a failed load, with its message ID and the row it names, and the version in force unchanged |

The harness opens no screen and renders no page; it asserts the answer the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0421; ASM-0596).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01-ITG | AC1, BR1, BR2, BR9; ITG AC1, ITG AC3 | Integration | RESTRUCTURE "RES-2026.12", 38 rows, 62 scenarios |
| TC-E2-042-02-ITG | AC2, BR2, BR3; ITG AC1, ITG AC3 | Integration | PAYMENT_MATCH "PMT-2026.12", 3 rows, 58 scenarios |
| TC-E2-042-03-ITG | AC3, BR2, BR7; ITG AC1, ITG AC3 | Integration | BOOKING_MATCH "BKG-2026.12", 21 rows, 54 scenarios |
| TC-E2-042-04-ITG | AC4, BR3, BR7; ITG AC2 | Integration | PAY-91008 matched by EXACT and WINDOW; PAY-91002 decided by PARTIAL with 625.00 THB short |
| TC-E2-042-05-ITG | AC5, BR4; ITG AC3 | Integration | R-RES-04 and the route-set rows of "RES-2026.12" |
| TC-E2-042-06-ITG | AC6, BR5; ITG AC3 | Component | The deploy-time schema check of rwb-decision, no `payment_match_rule` table, no column of DF-REF-261 to DF-REF-273 |

The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID. The Covers column names the legacy AC of RWB-E2-042 that the ITG copy is derived from and the criterion of §7 it asserts at integration level; the Level column maps the legacy System level to Integration and the legacy Schema test to Component.

### 17. Guardrails

- No business value in code: the rows, match types, tolerances, windows, action text, owner roles, timers and package rows are data held by rwb-decision; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or evidence: the report carries staff user IDs and synthetic payment and case codes, and no customer, account or case data.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never a production endpoint.
- The approver is never the author; FourEyesCheck fails the run when they are equal or when a refused approval writes an approver.
- No second rule engine and no recomputation: the version in force, the row counts, the dry run counts and the decisions are read through the rwb-decision contract, and no caller reads the workbook, the generated DRL or a rule row directly.
- `payment_match_rule` is never created and DF-REF-261 to DF-REF-273 are never referenced; the schema assertion is the deploy-time check of the owner's own schema, not a cross-schema read.
- A refused call writes nothing: the harness asserts every row before and after each refusal and fails the run on any change.
- One hop only: the harness fails a run when the trace shows a call chain deeper than one owner.
- A rule change raises no customer-facing notice: NoticeSilenceCheck fails the run when a notice event appears.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | Business Requirements Epic 1, section 3.3; Epic 2, sections 3.2 and 3.8; Program, section 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38; R-RES-26 | TC-E2-042-01-ITG to TC-E2-042-04-ITG, TC-E2-042-06-ITG |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | Business Requirements Epic 1, section 3.3; Epic 2, sections 3.2 and 3.8; Program, section 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26; R-RES-04 | TC-E2-042-01-ITG to TC-E2-042-05-ITG |

The requirement IDs and their BRD sections are those of the legacy story; this story adds no requirement ID of its own.

### 19. Out of scope

- The four owning I stories RWB-P7-E2042-APP, RWB-P3-E2042-APP, RWB-P6-E2042-APP and RWB-P4-E2042-APP, and every endpoint, table, rule, workflow and screen they build.
- Production code in any service: the harness is test and evidence only.
- The authoring, approval and rollback mechanics of a package version and the rule package rows themselves (RWB-E1-073 lineage); the harness asserts their result and builds none of it.
- The rule change report and its audit (RWB-E2-041), which the wave 2 governance journey covers.
- The payment matching engine and the booking confirmation engine themselves (RWB-E2-027, RWB-E2-008); the harness reads the decision records they wrote and recomputes nothing.
- The remaining routing rules and the UNIVERSAL package (Epic 3; DL24).
- The rules and parameters screen (SCR-39, Epic 8); the harness asserts the answer it consumes only.
- Any production code, endpoint, table, workflow or schedule, including the `rulePackagePromote` Schedule and the build gate, which rwb-decision owns and starts.
