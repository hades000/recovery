# RWB-P4-AD011-APP Load a rule version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP06, DP13, DP19 |
| Parallel lane | L-P4-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-AD011-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-011 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst, and the access service that accepts the route-set workbook**, I want **a route set accepted as a new rule version only when every one of its rows names the test case that covers it, with the accepted workbook handed to the rule registry and the version, its checksum and its SIT test result shown back on the administration screen**, so that **rules change as data with no code release, a row that nobody has tested can never become a version, and the governance of the version stays in the one service that owns the registry instead of being copied into the administration service**.

Inside `rwb-access` this is the administration-ingest slice of the legacy story RWB-AD-011:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Service facts of this slice: no topic of its own is published, no workflow is started, no rule table is held and no screen of its own is served — SCR-39 arrives through the gateway-bff composite route of DP-19.
- Two deliverables, and nothing else: the ingest `POST /api/recovery/access/v1/admin/rule-version-loads`, which reads the multipart workbook, checks every row for a test case ID and the required columns, hands the accepted workbook to `rwb-decision` through its rule-package contract and answers the version with `versionId`, `packageCode`, `versionLabel`, `validFrom`, `rowCount`, `checksum`, `testResult`, `dryRunCounts` and `state`; and the read `GET /api/recovery/access/v1/admin/rule-version-loads/{versionId}`, which answers the same version, its status, its checksum and its test result.
- The registry half stays in `rwb-decision` (P7) under ASM-0069: the compile of the workbook to DRL and the KieBase, the SHA-256 checksum, the checks for overlap, an unreachable row and a missing default row, the scenario run against at least 50 scenarios, the four-eyes approval by RW-RISK, the promotion at 00:01 by JOB-20 with `RulePackageInForce` (EV-30) on `rwb.decision.events.v1`, and the one-call rollback. This story does none of it and embeds no Drools kit.
- The FSD A2.18 presents the change as one journey in the P4 administration screens (FEAT-ADM-02). The target splits it, because the registry is `rwb-decision`'s: this story is the workbook ingest and the row-level gate on SCR-39, and the compile, the checks, the scenario run, the approval, the promotion and the rollback are the P7 slice. The metadata contract-dependency list of this story carries no P7 rule-package contract, so the call into the registry is built against that contract and its fake and the missing C dependency is raised at D1 — Not specified in the source documents (GAP-0821; ASM-1522).
- The compile, the checks and the SIT scenario run execute in `rwb-decision`, where the Drools kit (RWB-PLT-E1072-CON) lives; the kit is not in this story's build list, and this story embeds no Drools kit and evaluates no rule (GAP-0822; ASM-1523).
- The workbook format is the Drools XLS decision-table workbook with the `rule_row` columns of TSD P4 T3.1 plus `test_case_id` on every row; the exact column order and the header row are Not specified in the source documents (GAP-0823; ASM-1524).
- "The result is attached to the version" is read as the registry's `test_result` and `dry_run_counts` of the package version (DF-REF-292 and DF-REF-293) returned by the load and shown with the SIT report reference — Not specified in the source documents (GAP-0824; ASM-1525).
- A row without a test case ID is refused at upload, with the row number, before the registry is called and before any version is stored — Not specified in the source documents (GAP-0825; ASM-1526).

### 2. Business rationale

A rule change must not need a software release, and a row that nobody has tested must not decide a case. The FSD states the target plainly: rule and limit changes made without a code release, 100 percent, measured from the decision log and the Workbench records every month (FSD P4 A2.18.1). The legacy story served that target inside the monolith, where the rule rows and the rule version were rows of the recovery schema and the approval was a screen in the same module. In the target the registry is central in `rwb-decision` (Architecture v5 slide 27) and evaluation is local to each owning service, so the administration service no longer holds a rule row: it holds the gate that decides whether a workbook is worth sending to the registry at all, and it shows what the registry answered.

That gate is the cheapest control in the whole rule lifecycle. Every rule row of a decision table carries a `test_case_id` (TSD P4 T3.1, DF-REF-015), and the legacy acceptance criterion of RWB-AD-011 says a row with no test case ID refuses the version. Checked here, at upload, the analyst learns the row number before a compile is spent; checked only at approval, a refused version sits in the registry waiting for a person to notice. It is the same reason REQ-CWC-014 asks that rule loads be validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect: this story contributes the schema and the test-case part of that sentence at the point of upload, and the registry contributes the rest.

This story meets REQ-CWC-013, REQ-CWC-014, REQ-DRI-010 and REQ-ACA-013 on the administration side: a rule change goes from a validated load to production with a version stamp and no code release; the load is validated before it takes effect; the scenario minimum and the load limits are parameter rows and not code; and the administration screens carry the rights that decide who may load and who may read. It supports the measure rule and limit changes made without a code release (target 100 percent) and it carries R-UNI-38 at its edge: this story never decides which version is applied, it hands a dated workbook to the service that does. R-UNI-39 is not engaged, because a load is not a decision: no decision record is written here, and the audit of the load is the registry's own version record.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD011-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two console operations, the `RuleVersionLoad` and `RuleVersionCheck` schemas, the state set, the error envelope, the consumed-operation list and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1042-CON | The parameters client library (DP-06): the scenario minimum `rules.testcases.min` and the row and file limits of a load |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): SCR-39 reaches the two operations through it, one hop each |
| RWB-P3-E1042-CON | The parameters contract of `rwb-case` (DP-06): the value of `rules.testcases.min` and of the load limits, read with the version in force. A C dependency, so it never blocks the build |
| The `rwb-decision` rule-package contract | The two operations this story consumes and their fake: the load of a version and the read of a version with status, checksum, test result and dry-run counts. It is not in this story's metadata contract-dependency list (GAP-0821; ASM-1522) |
| The Drools kit RWB-PLT-E1072-CON | It is not a dependency of this story: the compile, the checks and the scenario run are `rwb-decision`'s, where the kit is installed (GAP-0822; ASM-1523) |

Business preconditions carried from RWB-AD-011:

- The route sets are the values of LOV-ROUTE-SET (RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS, UNIVERSAL_RULES); they are rows and never a list in code.
- Every row of the workbook names its test case, and the test cases are the registry's `rule_test_case` rows for the package version.
- The author of a version is RW-COE and the approver is RW-RISK, and the author cannot approve (Temporal and Drools Design slide 15).
- The scenario minimum is the parameter row `rules.testcases.min`, valued 50 in force (slide 15 notes). No threshold is written in code.
- The version states are the values of LOV-VERSION-STATUS; the two this story produces or receives are LOADED and REFUSED.
- The administration screens are reached through the gateway-bff composite route; the load screen is SCR-39 Rules and parameters.
- The analyst's staff reference and its Entra group resolve through the service's own ACE view `v_ace_iam_group` (DP-05), and no personal data is read, held or returned by this story.

### 4. Flow

1. The analyst, holding Rules and parameters C, posts the workbook to `POST /api/recovery/access/v1/admin/rule-version-loads` through the gateway-bff composite route with the multipart part `file` (xlsx) and the query `packageCode`, `routeSet` and `validFrom`, and an `Idempotency-Key` header.
2. `RuleVersionLoadController` calls the service's own authorise contract (`POST /api/recovery/access/v1/authorise`, Rules and parameters C) with the caller's role and scope. A caller without the C letter is refused with 403 and MSG-P4-002 and no workbook is read (BR10).
3. Where a break-glass grant is active for the caller, the answer carries the warning MSG-P4-004 with the grant reference, and the grant id is recorded with the load (BR12).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer and stores nothing (BR11, AC5).
5. `ParameterReader` reads the scenario minimum `rules.testcases.min` and the row and file limits through the parameters contract of DP-06 with the version in force on the load date. No value is a constant.
6. `WorkbookParser` opens the xlsx and reads the decision-table sheet: the header row, then one row per rule. A workbook that cannot be opened, or that carries no decision-table sheet, is 422 with MSG-GEN-001 naming the part that could not be read.
7. `ColumnGate` checks the twelve required columns of the workbook — `rule_id`, `route_set`, `from_state`, `event_code`, `condition_expr`, `action_text`, `to_state`, `owner_role`, `timer_spec`, `valid_from`, `valid_to`, `test_case_id` — against the `rule_row` fields of TSD P4 T3.1 (DF-REF-002 to DF-REF-015). A missing column is 422 with MSG-GEN-001 naming the column.
8. `RowGate` checks the query against the reference lists: `routeSet` must be a value of LOV-ROUTE-SET, `validFrom` must be a date, and `packageCode` must be a package the registry lists. An unknown route set or an unreadable date is 422 with MSG-GEN-001 naming the field.
9. `RowGate` then walks every row of the sheet: a row whose `test_case_id` is empty refuses the whole workbook with 422 and MSG-GEN-001 naming the row (`row 57`) and the field (`test_case_id`). No call is made to `rwb-decision`, no version is stored and nothing is in force (BR1, BR2, AC2, AC3).
10. `RowGate` checks the row count and the file size against the limits read in step 5, so a workbook over the limit is refused with 422 and MSG-GEN-001 naming the limit and its parameter row; the number of rows of the sheet becomes the `rowCount` of the answer.
11. `RulePackageClient` posts the accepted workbook, unchanged, to `POST /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` of `rwb-decision` as multipart with `file` and `validFrom`, forwarding the `Idempotency-Key`, in one hop with a 2 s timeout. The registry compiles the workbook, checks overlap, unreachable rows and the default row, runs the scenarios against the minimum, and stores the version.
12. The registry answers the stored version in state `LOADED` with its `versionId`, `versionLabel`, `checksum`, `validFrom`, `testResult`, `dryRunCounts` and `rowCount`. This story answers 201 with the same nine fields plus `packageCode` and `state`, and the `Location` of the read (BR3, BR8).
13. Where the registry refuses the workbook, it answers 409 with its check list. This story answers 409 with MSG-GEN-004, the registry's `checks[]` and `state` `REFUSED`, and stores nothing: the version exists as a refused record in the registry and nothing is in force (BR4, AC4).
14. `GET /api/recovery/access/v1/admin/rule-version-loads/{versionId}` reads the version through `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions/{versionId}` and answers its status, checksum, test result and dry-run counts with the same field set. The read is a pass-through: this service adds no state and holds no copy (BR5).
15. Where the registry cannot be reached, or answers beyond the 2 s budget, the load answers 503 and no version is reported as loaded; the analyst is asked to post again with the same `Idempotency-Key` so a retry cannot create a second version (BR11, X8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `packageCode`, `routeSet`, `validFrom` or the file part is empty | 422, no workbook is read and no call is made | MSG-GEN-001 | AC3 |
| X2 | The workbook carries no decision-table sheet, or a required column is missing | 422 naming the column or the part that could not be read | MSG-GEN-001 | AC3, AC4 |
| X3 | `routeSet` is not a value of LOV-ROUTE-SET, or `validFrom` is not a date | 422 naming the field; nothing is forwarded | MSG-GEN-001 | AC3 |
| X4 | A row of the sheet carries no `test_case_id` | 422 naming the row number and `test_case_id`; the registry is not called, no version is stored, nothing is in force | MSG-GEN-001 | AC2, AC3 |
| X5 | The sheet carries more rows or the file is larger than the limit in force | 422 naming the limit and its parameter row | MSG-GEN-001 | AC3 |
| X6 | The caller holds no Rules and parameters C | 403, no workbook is read, no answer about the workbook is given | MSG-P4-002 | AC3 |
| X7 | The registry refuses the workbook: compile, overlap, unreachable row, missing default row, fewer than 50 scenarios | 409 with the registry's `checks[]` and `state` `REFUSED`; the version is refused in the registry and nothing is in force | MSG-GEN-004 | AC4 |
| X8 | The registry does not answer inside 2 s, or the connection fails | 503 and no version is reported; a retry with the same `Idempotency-Key` cannot create a second version | MSG-P7-003 | AC5 |
| X9 | The same workbook is posted twice with the same `Idempotency-Key` | The first answer is replayed; the registry is called once and one version exists | None | AC5 |
| X10 | A break-glass grant is active for the caller | The load proceeds and the answer carries the warning and the grant reference | MSG-P4-004 | AC3 |

No exception path of this story changes a case, a task or an approval: the registry holds the version and its states, and the approval is `rwb-decision`'s with RW-RISK.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-AD011-CON, the parameters contract and the platform composite route; the registry contract is consumed through its fake, and no rule table is read or written |
| Negotiable | The column order of the workbook, the exact check list wording and the screen field list are settled with the registry owner and the analysts; the operations, the states and the gate are fixed |
| Valuable | One ingest that refuses an untested row before a compile is spent, and one read that shows the version, its checksum and its SIT result |
| Estimable | One controller, one parser, one column gate, one row gate, one registry client, one parameters reader, one idempotency lookup and their tests |
| Small | Fits two weeks with its tests; it creates no table, starts no workflow and publishes no event |
| Testable | Each owned criterion has a test case in section 16, and the registry side is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Load a rule version

  Background:
    Given the environment is SIT
    Given the run date is 15 December 2026
    Given the parameter rules.testcases.min is 50 in force on the run date
    Given the route sets are the values of LOV-ROUTE-SET
    Given test user "U-7101" holds RW-COE with the C letter in Rules and parameters
    Given test user "U-7103" holds RW-RISK with the A letter in Rules and parameters
    Given test user "U-7110" holds RW-CASEOWN with the R letter only in Rules and parameters

  Scenario: AC1 Rule rows tested (legacy RWB-AD-011 AC1)
    Given the rwb-decision contract mock returns version "ENTRY-2027.01" in state "LOADED" with checksum "3f9c…" and test result "PASS" with 448 rule rows and the SIT report attached
    Given a route set file where every row has a test case ID
    When I load it
    Then the rule table tests run in SIT and the result is attached to the version

  Scenario: AC2 Row without a test (legacy RWB-AD-011 AC2)
    Given a row with no test case ID
    When I load it
    Then the system refuses the version

  Scenario: AC3 A row without a test case ID is refused at upload with its row number (new, D-RCV-60)
    Given "U-7101" posts the RESTRUCTURE workbook of 448 rows with packageCode "ENTRY", routeSet "RESTRUCTURE" and validFrom 2027-01-01, and row 57 of the sheet carries an empty test_case_id
    When POST /api/recovery/access/v1/admin/rule-version-loads is called with Idempotency-Key "k-011-1"
    Then the response is 422 with message MSG-GEN-001, and its detail names "row 57" and "test_case_id"
    Then the rwb-decision contract fake records no call
    Then no version is stored and no version id is returned
    Then a correct workbook posts afterwards and is accepted, so the refusal changed nothing

  Scenario: AC4 A refused workbook shows the registry check list and nothing is in force (new, D-RCV-60)
    Given "U-7101" posts a RESTRUCTURE workbook in which rows 12 and 13 overlap, row 88 is unreachable, the default row is missing and 41 scenarios exist against the minimum 50
    When the load is made
    Then rwb-decision answers 409 with its check list
    Then rwb-access answers 409 with message MSG-GEN-004, state "REFUSED" and a checks list naming the overlap at rows 12 and 13, the unreachable row 88, the missing default row and the scenario count 41 against 50
    Then GET /api/recovery/access/v1/admin/rule-version-loads/{versionId} answers state "REFUSED" with the same check list
    Then no version is in force and the version that was in force still decides cases

  Scenario: AC5 The same workbook twice with one Idempotency-Key answers one version (new, D-RCV-60)
    Given "U-7101" posts the accepted RESTRUCTURE workbook with Idempotency-Key "k-011-1"
    When the same workbook is posted again with Idempotency-Key "k-011-1"
    Then the first response is 201 with versionId, packageCode "ENTRY", versionLabel "ENTRY-2027.01", validFrom 2027-01-01, rowCount 448, checksum "3f9c…", testResult "PASS", the dry-run counts and state "LOADED"
    Then the second response repeats that first answer and the rwb-decision contract fake records one call
    Then no second version is stored
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every row of a route-set workbook names the test case that covers it; a row without one refuses the version | Legacy RWB-AD-011 AC2; REQ-CWC-014; TSD P4 T3.1 DF-REF-015 |
| BR2 | The refusal happens at upload, before the registry is called and before any version is stored, and it names the row and the field | Legacy RWB-AD-011 AC2; GAP-0825; ASM-1526 |
| BR3 | The workbook carries the `rule_row` columns of the technical specification plus `test_case_id`, and no other column is required | TSD P4 T3.1 DF-REF-001 to DF-REF-015; GAP-0823; ASM-1524 |
| BR4 | The compile, the checks and the scenario run are the registry's and are not repeated here; `rwb-access` passes the workbook and shows the answer | Temporal and Drools Design slide 15; ASM-0069; GAP-0822; ASM-1523 |
| BR5 | The version is in force from its valid-from date by the registry's promotion; this story writes no state of a version and answers what the registry answers | Temporal and Drools Design slide 15; R-UNI-38; TSD P4 T4 |
| BR6 | The scenario minimum is the parameter row `rules.testcases.min`, 50 in force, and the row and file limits are parameters too; no threshold is written in code | Temporal and Drools Design slide 15 notes; DP-06; BR-P4-018 |
| BR7 | The author cannot approve: RW-COE loads and RW-RISK approves, and the approval is the registry's | Temporal and Drools Design slide 15; TSD P4 T6.1 |
| BR8 | The result attached to the version is the registry's `test_result` and `dry_run_counts` of the package version, returned by the load and shown on the screen | Legacy RWB-AD-011 AC1; TSD P4 T3.1 DF-REF-292, DF-REF-293; GAP-0824; ASM-1525 |
| BR9 | Route sets and version states are data: LOV-ROUTE-SET and LOV-VERSION-STATUS, read as values and never as code | TSD P4 T3.2; FSD P4 A2.18.3.1 BR-P4-018 |
| BR10 | Only a caller holding Rules and parameters C may load a workbook, and a refused caller learns nothing about the workbook or the route set | Legacy RWB-AD-011 permission checks; TSD P4 T6.1 |
| BR11 | One `Idempotency-Key` answers one version: a repeated post replays the first answer and the registry is called once | Architecture v5 slide 11; DP-09 |
| BR12 | Every load records the caller reference and, where a break-glass grant is active, the grant id; the record carries no personal data | Legacy RWB-AD-011 MSG-P4-004; Principle 5 |
| BR13 | This story writes no decision-record entry of its own: the audit of a load is the registry's version record, and the version it names is the version that decided | ASM-0069; R-UNI-39 not engaged |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are one pass over the parsed sheet before the registry client is called: the gate returns the first row whose `test_case_id` is empty, and the controller maps it to a 422 whose `detail` names the row number and the field. Nothing is sent, so nothing can be stored.
- BR3 is the column gate over the header row; the twelve columns are the `rule_row` fields that a decision table must carry, and an extra column that the registry ignores is not a refusal here.
- BR4 is the absence of a Drools dependency: the service has no KieBase, no DRL compilation and no scenario runner, so a check can only come from the registry's answer.
- BR5 is the pass-through of the read: the version, its status, its checksum and its test result are the registry's fields, and this service holds no copy that could drift from them.
- BR6 is the parameters reader: the scenario minimum and the limits arrive as rows with the version in force, and the registry enforces the minimum on its side against the same row.
- BR7 is a right, not a state: RW-COE holds C and RW-RISK holds A in Rules and parameters, and this story exposes no approval path at all.
- BR8 is the field set of the answer: `test_result` and `dry_run_counts` come from DF-REF-292 and DF-REF-293 and travel through the contract with the SIT report reference the registry returns.
- BR9 is checked by test: a new route set is a reference value and a new state is a list value, and the build changes nothing.
- BR10 is the authorise call before the multipart body is read, so a caller without the right cannot even spend the parse.
- BR11 is the idempotency table of the platform library in `rwb_access`, written with the answer in the same transaction as the registry call's reply.
- BR12 is the caller reference in the answer and in the record, and the grant id where the warning MSG-P4-004 is returned; no name and no e-mail address is held.
- BR13 is a deliberate absence: the load's audit is the registry's version row with its author, approver and times (TSD P4 T6.3), and no local decision record is written, so R-UNI-39 has nothing to block and no event is published.

### 9. State transitions

This service holds no version state. The states it produces or observes are the registry's, and it answers them unchanged.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A workbook is posted and passes the column gate and the row gate | The registry stores the version | `LOADED`, with a version id and a checksum |
| (none) | A workbook is posted and a row carries no `test_case_id` | The gate refuses before the call | No version, no state; the caller is answered 422 |
| (none) | A workbook is posted and the registry refuses it | Compile, overlap, unreachable row, default row or scenario count fails | `REFUSED`, held by the registry; nothing is in force |
| `LOADED` | Approval by RW-RISK in `rwb-decision` | The author is not the approver | `APPROVED`, then `IN_FORCE` from its valid-from date by the promotion at 00:01 |
| `IN_FORCE` | The next version is promoted | The newer version reaches its valid-from date | `SUPERSEDED`, readable for its own dates |
| `IN_FORCE` | One-call rollback in `rwb-decision` | None | `ROLLED_BACK`, and the version before it is in force again |

| Command | Condition | Outcome |
|---|---|---|
| Load a workbook | Rules and parameters C, a valid workbook, every row tested, the registry accepts it | 201 with the version in state `LOADED` |
| Load a workbook | A row without a `test_case_id`, a missing column, an unknown route set or a limit exceeded | 422 with MSG-GEN-001; nothing is forwarded |
| Load a workbook | The registry refuses the workbook | 409 with MSG-GEN-004, `checks[]` and state `REFUSED` |
| Load a workbook | No C letter in Rules and parameters | 403 with MSG-P4-002 |
| Read a version | Rules and parameters R | 200 with the version, its status, its checksum, its test result and its dry-run counts |

The registry owns the lifecycle of a version (TSD P4 T4); this story holds no copy of it and changes none of its states.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE Center of excellence analyst | Holds Rules and parameters C: loads a version and reads it. The upload, the list, the dry run and the rollback are the rights the technical specification gives this role on rule packages |
| RW-RISK Risk and model risk officer | Holds Rules and parameters A and approves a loaded version; the approval is an operation of `rwb-decision`, and this story exposes no approval path |
| RW-AUDIT Internal audit | Holds Rules and parameters R and reads the versions, the test result and the dry-run counts; the change report is `rwb-decision`'s |
| RW-REFADM Reference data administrator | Prepares the change checklist and the load file and holds no upload and no approval right; a post from this role is refused with 403 and MSG-P4-002 |
| RW-PLATADM, RW-SECADM | Hold Rules and parameters R and may read a version; they load nothing |
| The `rwb-decision` service identity | Answers the two consumed operations; it calls nothing of this story |
| `rwb-access` itself | Reads `role`, `permission` and its own `v_ace_iam_group` ACE view, and writes only the idempotency row of a load |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right and MSG-P4-001 for an absent session. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-AD011-CON together with the rest of the service's contract.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| (ACE view) | `v_ace_iam_group` (ACE `iam_group`, RWB-ACE-001) | entra_group of the calling staff reference | Read through the service's own ACE view (DP-05) |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a load | Write (DP-09; ASM-0074) |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-001 to DF-REF-015 | `rule_row` of `rwb_decision` | the twelve workbook columns, `test_case_id` among them | Checked in the workbook and stored by the registry; not read |
| DF-REF-279 to DF-REF-295 | `rule_package_version` of `rwb_decision` | version id, version label, status, checksum, valid-from, test result, dry-run counts | Returned through the contract; not read |
| DF-REF-274 to DF-REF-278 | `rule_package` of `rwb_decision` | package code, title, owner role, hit policy | Returned through the contract; not read |
| DF-DEC-001 to DF-DEC-018 | decision record | none | None |

No rule table exists in `rwb_access`, and none is created: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s under ASM-0069, and their fields arrive in the contract, not by a schema read (DP-01). No row of `decision_log_entry` is read or written either: this story writes no decision-record entry of its own, and the audit of a load is the registry's own version record with its author, approver and times (TSD P4 T6.3), so R-UNI-39 has no local write to block. No row of `case` or `task` is read. The workbook itself is not stored here: it travels in the request to the registry, which keeps it as `source_blob_ref` (DF-REF-283) with the generated DRL and the checksum. Field IDs are those of the Logical Data Model and Data Dictionary v9; `lov_value` is reference data of P3 under the ownership ruling and is read through DP-07 by the registry, not from `rwb_access`.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/rule-version-loads` | P4 `rwb-access` | Multipart: `file` (xlsx decision table); query `packageCode`, `routeSet`, `validFrom` | `versionId`, `packageCode`, `versionLabel`, `validFrom`, `rowCount`, `checksum`, `testResult`, `dryRunCounts`, `state`, with `Location` of the read | 401 (MSG-P4-001); 403 Rules and parameters C (MSG-P4-002); 409 refused by the registry, with `checks[]` (MSG-GEN-004); 422 missing column, missing test case ID, unknown route set or limit exceeded (MSG-GEN-001); 503 registry unavailable (MSG-P7-003) | Rules and parameters C | `Idempotency-Key` header; the stored answer is replayed |
| GET | `/api/recovery/access/v1/admin/rule-version-loads/{versionId}` | P4 `rwb-access` | None | The same nine fields, with the status of the version | 401; 403 Rules and parameters R (MSG-P4-002); 404 unknown version; 503 registry unavailable | Rules and parameters R | Not applicable, read only |

Both operations sit under the base `/api/recovery/access/v1` of DP-13. They are this service's administration ingest and read of a rule version; the rule-package operations themselves are `rwb-decision`'s (ownership map, ASM-0040), and the contract dependencies row of this story names no P7 contract, which is the missing dependency of GAP-0821 and ASM-1522.

The workbook format is the Drools XLS decision-table workbook whose sheet carries one row per rule with the `rule_row` columns of TSD P4 T3.1 plus `test_case_id`; the exact header order and the sheet name are Not specified in the source documents (GAP-0823; ASM-1524).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 `rwb-decision` | The workbook load: multipart `file` and `validFrom`; the registry compiles, checks, runs the scenarios and stores the version `LOADED`, or refuses it with its check list |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions/{versionId}` | P7 `rwb-decision` | The version, its status, its checksum, its test result and its dry-run counts |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (this service) | The Rules and parameters C or R check behind both operations, under the guard library of DP-08 |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | `rules.testcases.min` and the row and file limits of a load, with the version in force (DP-06) |

The two `rwb-decision` operations are the registry half and are declared as consumed, never as provided. The parameters read is the C dependency `RWB-P3-E1042-CON` and never blocks the build.

#### 12.3 Events published

None. `rwb-access`'s own topic `rwb.access.events.v1` carries only `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 14), and this story adds neither and no other event type. The rule-version event is `rwb.decision.RulePackageInForce.v1` (EV-30) on `rwb.decision.events.v1`, published by JOB-20 in `rwb-decision` when it promotes a version at 00:01; it is not this story's. No event payload can carry personal data, because no payload is produced here.

#### 12.4 Events consumed

None. This story subscribes to no event and its read answers from the registry on request. The promotion of a version at 00:01 is `rwb-decision`'s Schedule, and the services that swap a model in on `RulePackageInForce` are the model-owning services, not this one.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals none and registers no activity on the `rwb-access` queue. The promotion at 00:01 is a Temporal Schedule of `rwb-decision` (JOB-20), and the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.6 Schedules

None. A load is request-driven, and the only Schedule in the version lifecycle — the 00:01 promotion — runs on `rwb-decision`'s queue.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the caller's role and its class |
| `permission` | P4 (`rwb_access`) | Read only: the C or R letter of the caller's role in Rules and parameters |
| `idempotency_key` | PLT library, created in `rwb_access` | The stored request and answer of a load, so one key answers one version (DP-09) |
| `outbox_event`, `processed_event` | PLT library, created in `rwb_access` | Not written and not read: this story publishes no event and consumes none |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the version is the registry's (ASM-0069) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: this story takes no decision and writes no record |
| `case`, `task` | P3 (`rwb_case`) | Not read |

No table of another service is read and no foreign key crosses a schema (DP-01). The workbook is not stored here; the ACE data this story touches is its own `v_ace_iam_group` view (DP-05), which carries group names and no personal field.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision rule-package WireMock | the P7 rule-package contract (GAP-0821; ASM-1522) | `POST /admin/rule-packages/{packageCode}/versions` answering version "ENTRY-2027.01" in state `LOADED`, checksum "3f9c…", test result `PASS`, 448 rule rows and the SIT report reference of AC1 and AC5; the refusal of AC4 with `checks[]` naming the overlap at rows 12 and 13, the unreachable row 88, the missing default row and 41 scenarios against 50; a 503 for X8; `GET /admin/rule-packages/{packageCode}/versions/{versionId}` answering the same version, then the refused one |
| parameters fake | RWB-P3-E1042-CON | `GET /api/recovery/case/v1/admin/parameters` answering `rules.testcases.min` = 50 and the row and file limits, with the version in force on 15 December 2026 |
| authorise and guard fake | RWB-P4-AD011-CON, RWB-P4-E1037-CON | A granted answer for RW-COE with Rules and parameters C and for RW-RISK and RW-AUDIT with R, and a refused answer with MSG-P4-002 for RW-CASEOWN and RW-REFADM |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The SCR-39 route that calls the load and the read, one hop each, and merges the version fields with the check list of a refused load |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 new; consumed 4 | Base `/api/recovery/access/v1`; two `rwb-decision` operations, the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 0; consumed 0 | None; `RulePackageInForce` is `rwb-decision`'s |
| Temporal | 0 workflows, 0 activities | The 00:01 promotion is a Schedule of `rwb-decision` |
| File | One xlsx in, none out | The multipart workbook is parsed here and forwarded unchanged to the registry, which stores it as the version's source blob |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/ruleversion`, Java package `th.co.scb.ace.workbench.recovery.access.ruleversion`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module rule-row read and the in-module version approval of the monolith (DP-13: the service's own base and the operation moved to the registry), the `AceSourceQuery` call that resolved the analyst's group (DP-05: the service's own `v_ace_iam_group` view), and the `casewf.config` read of the scenario minimum (DP-06: the parameters contract of `rwb-case` with the version in force). There is no DP-04 in this story's pattern set on purpose: the Drools kit and the evaluation are P7's and of the model-owning services, and this story must not claim them (GAP-0822; ASM-1523).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleVersionLoadController | Controller | The two operations: multipart and query validation, the authorise call before the body is read, RFC 9457 error mapping, `Location` on a created version |
| WorkbookParser | Service | Opens the xlsx decision-table workbook and returns the header row and one row per rule; refuses a file that is not a decision table |
| ColumnGate | Service | The twelve required columns of BR3; a missing column is named in the 422 |
| RowGate | Service | The `test_case_id` pass of BR1 and BR2, the route-set and date check, and the row and file limits read through DP-06 |
| RulePackageClient | Client | The two `rwb-decision` operations, one hop and 2 s, forwarding the `Idempotency-Key`, mapping a 409 to the check list and a timeout to 503 |
| PermissionReader | Service | The `role` and `permission` rows of the caller in `rwb_access`, behind the authorise operation |
| StaffGroupReader | Service | The analyst's staff reference and Entra group through `v_ace_iam_group`, with no personal field read |
| ParameterReader | Service | `rules.testcases.min` and the load limits through the parameters contract of DP-06, with the version in force |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table of its own. The `idempotency_key` table is the platform library's object created in `rwb_access` by the service's own DB story in the per-service Flyway sequence of DP-15, and this story only uses it.
- No rule table is created and no rule column is added to `rwb_access`: the registry holds `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` (ASM-0069), and the workbook is forwarded, not stored.
- No write statement touches `role` or `permission`: the reader is read-only, so a load can never grant itself a right.

**Configuration and reference data**

- `rules.testcases.min` = 50 and the row and file limits are parameter rows of `rwb-case`, read through the parameters contract of DP-06 with the version in force (RWB-P3-E1042-CON). No threshold is a constant.
- LOV-ROUTE-SET and LOV-VERSION-STATUS are values read with the version in force; a new route set or a new state is a row and a list value, and the build changes nothing.
- The package codes are the registry's LOV and are validated against its package list, so a new package needs no build here either.

**Build steps**

1. `WorkbookParser` and `ColumnGate` over a synthetic 448-row workbook; tests for the missing-column 422 of X2 and for a file that is not a decision table.
2. `RowGate` with the `test_case_id` pass; the AC2 and AC3 tests, including the row number and the field name in the answer, and the proof that the registry client is not called.
3. `ParameterReader` over the parameters contract; the test that a changed `rules.testcases.min` or limit changes the outcome with no code change (BR6).
4. `RulePackageClient` against the `rwb-decision` fake: the `LOADED` answer of AC1 and AC5, the `REFUSED` answer with `checks[]` of AC4, and the 503 of X8.
5. `IdempotencyStore`: the replay of AC5 and the proof that the registry fake records one call for two posts.
6. The authorise path before the body read; the AC3 access refusal of a caller with R only, and the break-glass warning of X10.
7. The composite-route run of the SCR-39 states through the gateway-bff fake, in isolation from the registry build.

**Feature switch.** No switch of this slice's own: a load that is switched off would quietly leave the old version in force while the screen said nothing, which is the failure the gate exists to prevent. The service-level feature flag of the service baseline governs the administration surface, and this story adds no flag.

**Done when.** The tests in section 16 pass; a workbook whose every row has a test case ID loads to `LOADED` with the checksum and the SIT result shown; a row without one is refused with 422 naming row 57 and `test_case_id` and the registry is not called; a refused workbook shows the registry's check list with state `REFUSED` and nothing is in force; and two posts with one `Idempotency-Key` answer one version.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-001 | A required query field or multipart part is empty, a required column is missing, the route set is unknown, a limit is exceeded, or a row carries no test case ID | Enter {field}. | This story, on the load; the detail names the row number and the field for a missing test case ID |
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters C for a load, or no R for a read | You cannot {action} here. Your role does not include it. | This story, from the authorise answer |
| MSG-GEN-004 | The registry refuses the workbook, or the same key arrives with a different body | Someone else changed this record. Reload it to see their change. | This story maps the registry's refusal onto this 409; `detail` and `checks[]` carry the registry's check list, so the analyst reads which check failed |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the answer, with the grant id recorded |
| MSG-P7-003 | The registry cannot be reached, or cannot record the version | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `rwb-decision`, passed through unchanged on a 503 |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 409 of a refused load also carries `state` `REFUSED` and the `checks[]` list, so the screen can show each failing check without a second call.

### 15. Screens and states

SCR-39 Rules and parameters is the administration screen, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), which calls the load and the read of this service and the registry's version operations in parallel, one hop each, and merges the answers. This story serves the two operations behind it and builds no screen surface of its own.

| Screen | State | What the screen shows |
|---|---|---|
| SCR-39 Rules and parameters | Empty | No version is listed for the package yet: an empty list with a total of 0 and no error |
| SCR-39 Rules and parameters | Checked | The workbook has passed the column gate and the row gate and the registry is running the compile, the checks and the scenarios; the row count is shown |
| SCR-39 Rules and parameters | Refused | The 409 with the registry's `checks[]` and state `REFUSED`: each failing check with its rows, and the statement that the version in force still decides |
| SCR-39 Rules and parameters | Loaded, waiting for approval | State `LOADED` with the version label, the valid-from date, the row count, the checksum and the test result with its dry-run counts, and the fact that approval is RW-RISK's in the decision center |

The legacy story also lists SCR-47 Personal data with the states Loading and list. That screen is not this slice: it belongs to the masking capability of `rwb-access`, and this story serves no field of it and reads no personal data.

Approval is not a state of this story: the approve action on a loaded version is `rwb-decision`'s, so the screen shows the version as waiting and links to the decision center rather than offering the approval here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-011-01 | AC1, BR4, BR8 | Contract | The `rwb-decision` fake: version "ENTRY-2027.01" `LOADED`, checksum "3f9c…", test result `PASS`, 448 rule rows, the SIT report reference attached |
| TC-AD-011-02 | AC2, AC3, BR1, BR2 | Component | A 448-row RESTRUCTURE workbook whose row 57 has an empty `test_case_id`; 422 naming row 57 and `test_case_id`; the registry fake records no call |
| TC-AD-011-03 | AC3, BR10 | Component | A caller holding RW-CASEOWN with Rules and parameters R only, posting the load; 403 with MSG-P4-002 and no parse |
| TC-AD-011-04 | AC4, BR4, BR5 | Contract | The registry's refusal with `checks[]`: overlap at rows 12 and 13, unreachable row 88, missing default row, 41 scenarios against 50 |
| TC-AD-011-05 | AC5, BR11 | Component | The same workbook twice with `Idempotency-Key` "k-011-1"; one registry call, one version, the first answer replayed |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Contract and Access to Component as the rows show. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the scenario minimum, the row and file limits, the route sets and the version states are parameter rows and list values with versions (BR6, BR9). A test proves that a new route set or a changed minimum needs no build.
- No personal data anywhere: the load carries rule text, codes, dates and a caller reference; the answer and the check list carry no name, no e-mail address and no personal field, and no test data or prompt holds one.
- No read of another service's tables (DP-01): `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s, and no foreign key crosses a schema. The version fields arrive in the contract.
- ACE data only through the owner's contract or its own `v_ace_*` views: the analyst's group is read through `v_ace_iam_group` (DP-05), which carries no personal field.
- One writer for a rule version: only `rwb-decision` writes a version, its rows and its states. This story holds no rule table and no write path to one, so a load cannot create a version that the registry did not accept.
- No version without its test: the row gate runs before the registry is called, so an untested row cannot reach a compile, and the registry's own scenario minimum is enforced again on its side (BR1, BR6).
- One key, one version: the `Idempotency-Key` of a load is stored with the answer, so a retry after a timeout cannot create a second version (BR11).
- No record, no claim: this story writes no decision-record entry and publishes no event of its own, so the audit of a load is exactly the registry's version record and cannot disagree with it (BR13).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a version stamp and no code release, and rolls back by one call | Epic 8 | FEAT-ADM-02 | All recovery processes | BR3, BR5, BR7 | TC-AD-011-01, TC-AD-011-04 |
| REQ-CWC-014 | Rule loads are validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect | Epic 8 | FEAT-ADM-02 | All recovery processes | BR1, BR2, BR3, BR4, BR6 | TC-AD-011-02, TC-AD-011-04 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold and limit, versioned | Epic 8 | FEAT-ADM-02 | All recovery processes | BR6 | TC-AD-011-02, TC-AD-011-04 |
| REQ-ACA-013 | Full administration screens are available to the administrator, with their rights | Epic 8 | FEAT-ADM-02 | All recovery processes | BR9, BR10 | TC-AD-011-03 |

| Legacy reference | Where it is kept |
|---|---|
| AC1: a route set file where every row has a test case ID, the tests run in SIT and the result is attached to the version | Sections 1, 4, 7, 8, 12.2, 14 |
| AC2: a row with no test case ID refuses the version | Sections 1, 4, 5, 7, 8, 17 |
| The `rule_row` fields DF-REF-001 to DF-REF-015, `test_case_id` among them | Sections 8, 11, 12.1 |
| MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 | Section 14, exception paths |
| Screens SCR-39 and SCR-47 and their states | Sections 15, 19 |
| Permission checks: Rules and parameters A for RW-RISK and R for the case roles | Sections 10, 12.1, 16 |
| Decision DL24 and rule IDs R-UNI-38 and R-UNI-39 | Sections 2, 8, 11 |
| Legacy key RWB-AD-011, story RWB-P4-AD011-APP, contract RWB-P4-AD011-CON | Metadata, sections 3, 12 |
| Field IDs DF-REF-001 to DF-REF-015, DF-REF-034 to DF-REF-044, DF-REF-274 to DF-REF-295 | Section 11 |

### 19. Out of scope

- The registry half under `rwb-decision` (P7, ASM-0069): the compile to DRL and the KieBase, the checksum, the overlap, unreachable-row and default-row checks, the scenario run, the version states beyond `LOADED` and `REFUSED`, the four-eyes approval by RW-RISK, the promotion at 00:01 with `RulePackageInForce`, the one-call rollback and the change report.
- The Drools kit and any evaluation of a rule: the model-owning services fetch the version, verify the checksum and swap it in (DP-04), and this story embeds no Drools kit.
- The `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables and their migrations; they are `rwb-decision`'s.
- The approval action, the approval screen surface and the `rule_package_version` approve and rollback operations; the legacy key RWB-AD-012 (approve a rule version) is the approval half and is the registry's.
- SCR-47 Personal data and the masking capability of `rwb-access`; this story reads and serves no personal field.
- The integration harness of the rule-version journey: no ITG story is split from this legacy key, so the `-ITG` copies of the test cases are not written here.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
