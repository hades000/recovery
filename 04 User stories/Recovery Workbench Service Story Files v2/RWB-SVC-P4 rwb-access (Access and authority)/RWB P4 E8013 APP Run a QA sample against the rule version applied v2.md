# RWB-P4-E8013-APP Run a QA sample against the rule version applied

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BG |
| Ready to start | Day 1 |
| Contract version | 5.0.0 (Recovery Workbench API Specification v5, rwb-access.yaml info.version; REST base /api/recovery/access/v1) |
| Size | Not specified in the source documents (DOR-RWB-P4-E8013-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P4-E8013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON; rwb-decision decision-log and rule-catalog contract (GAP-2284; P7 contract dependency not specified in the source documents (GAP-0873)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-013 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **conduct and QA officer**, I want **a sample of the closed decisions of a period tested against the rule version that was recorded on each of them, with a verdict and one reason code per decision and the run recorded once**, so that **a rule or a limit change can be shown afterwards to have been applied as it was approved, without a code release and without asking the rule owner to re-run anything**.

Inside `rwb-access` this is the assurance sample of the legacy story RWB-E8-013:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the write `POST /api/recovery/access/v1/admin/qa-samples`, which authorises, draws the sample, tests each drawn decision, records the run and answers it; and the read `GET /api/recovery/access/v1/admin/qa-samples/{qaSampleId}`, which answers one run with its items.
- The decision log and the rule registry are `rwb-decision`'s (P7). The ownership map puts `decision_log_entry` in P7 and the ruling ASM-0069 puts `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` there too, with `GET /decision-log` and `GET /decision-log/{entryId}` P7's own operations. This story reads **no** decision row and **no** rule row, holds no copy of a ledger entry and no copy of a rule row, and renames or redefines no P7 operation.
- The two P7 reads are the decision-log query of a period and the read of one rule-model version by package code and version label, and they are declared as consumed in section 12.2 and built against the P7 contract and its fake (DP-01). The metadata of this story carries no P7 contract dependency — its only C is `RWB-P3-E1042-CON` — so the missing dependency is raised at D1 and not added to the metadata: Not specified in the source documents (GAP-0873; ASM-1586).
- The test is a **time-travel consistency test and not a Drools re-run**. This story's pattern list carries no DP-04 and no DP-08: it evaluates no rule package, uses no rule evaluator and builds no KieBase. For each sampled decision it checks three things: that the `rule_id` and `rule_version` recorded on the decision resolve to a rule version whose `valid_from` and `valid_to` cover the decision's `decided_at`; that the recorded rule id exists in that version's `rule_row` set; and that the recorded answer agrees with that row's `action_text` and `outputs`. Each item gets a verdict of PASS or FAIL with exactly one reason code, drawn from a set held as parameter rows and never as a constant in code.
- The sample is drawn from what P7 answers, sized and bounded by parameter rows read through DP-06: the default sample size, the period bounds, the page bounds and the reason codes are rows of `rwb-case`, and a changed cap is data and needs no build.
- The run is reached from SCR-39 Rules and parameters through the gateway-bff composite route of DP-19, which shows the rule version in force and its evidence and calls the two operations of this story; this story renders no screen of its own and holds no rule-version panel.
- This story starts no workflow, owns no Schedule and publishes no `rwb.access.<Event>.v1` message: a QA verdict changes no policy, and the two events of `rwb-access` are `AccessPolicyChanged` and `DoaLimitChanged`, neither of which fits. The only message it produces is `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`.

The state a rule package version carries — `LOADED`, `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED` — is P7's, read through the P7 contract and never written here (TSD P4 v3 T3.2 LOV-VERSION-STATUS, T4). This story records one state of its own, the state of a QA-sample run, whose value set is fixed by RWB-P4-E8013-CON; the legacy story and the FSD name no run state, so its label is Not specified in the source documents (GAP-0873; ASM-1586).

### 2. Business rationale

REQ-DRI-001 asks that every decision write one record holding the case and the decision, the rule, model, agent and prompt versions, the inputs snapshot, the recommendation, the approval, the actions and the outcome, Must. REQ-DRI-012 asks that audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call, Must. REQ-CWC-016 asks that every allocation, assignment, transfer and timer event be logged with the rule id and the rule version that caused it, Must. Together those three requirements make the record good enough to be **tested after the fact** — and this story is that test. The legacy story carried it as one administration journey inside the monolith (FEAT-ADM-08, RWB-E8-013, FSD P4 v3 A2.24), where the decision log, the rule rows and the screen were rows and panels of one schema. In the target the ledger and the registry are `rwb-decision`'s (Architecture v5 slides 14 and 41; ADR-022; ADR-017), and the only way to see a decision is the P7 contract.

This story is the assurance side of that split. It meets REQ-DRI-012 on the read side — a population of closed decisions is queried, and each one is answered with the versions it recorded — and it meets REQ-CWC-016 by proving that the rule version stamped on a decision is the version that was in force when the decision was taken. It carries the FSD target measure for the feature: rule and limit changes made without a code release, 100 percent, measured monthly from the decision record (FSD P4 v3 A2.24.1). A rule version is data, its evidence is data, and neither needs a release.

The control that makes the sample worth anything is that it is a **consistency** test and not a second opinion. A re-evaluation would need the package, the facts and the engine, it would cost a Drools run per sampled decision, and it would answer a different question — what the rules would say now, or what they say when replayed with a snapshot that may itself have drifted. The question the conduct and QA officer actually asks is narrower and answerable from the record alone: was the version stamped on this decision the version in force at its decided time, does the rule it names exist in that version, and does the answer it recorded agree with the row it names. Those three checks read two things P7 already holds and never touch a package source, which is why the story needs no DP-04, no rule evaluator and no local KieBase.

Keeping the registry in P7 is the point of the split. This service authorises, draws, compares and records; `rwb-decision` owns the ledger, the versions, the rows and the test cases, and the owning service of each model evaluates its own package locally. A single writer for the registry is what makes the second check provable: one `rule_row` set per package version, published once, and the row a decision names identifiable years later.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8013-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `QaSampleRequest`, `QaSampleRun` and `QaSampleItem` schemas, the run state set, the verdict and reason-code sets, the error envelope, the consumed-operation list and the six contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a run, hash-linked, written in the transaction that stores the answer |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the default sample size, the period bounds, the page bounds and the reason-code set, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-39 Rules and parameters and calls the two operations, one hop each |
| The `rwb-decision` contract | The two operations this story consumes and their fake: the decision-log query of a period with the rule id, the rule version and the decided time of each entry, and the read of one rule-model version with its `valid_from`, `valid_to` and its `rule_row` set. It is not in this story's metadata contract-dependency list (GAP-0873; ASM-1586) |

Business preconditions carried from RWB-E8-013, from the feature specification and from the technical specification:

- The rights in force are those of TSD P4 v3 T6.1: the conduct and QA officer holds `R` in Rules and parameters, the center of excellence analyst holds `CRUD`, the internal audit role holds `R`, and the phone collector holds a dash. The run authorises Rules and parameters R, and a caller without it is refused with 403 and MSG-P4-002 (BR3).
- The FSD P4 v3 A2.24.3.3 role table names the conduct and QA officer as primary and the center of excellence analyst and internal audit as also using the feature, which matches the letters of the T6.1 matrix; the run is an assurance read whose verdicts the service records under its own code (ASM-1586).
- The legacy story depends on FEAT-DRI-03, the decision record and its log, and that dependency is met by the P7 contract rather than by a table of this service (GAP-0873; ASM-1586).
- A decision is **closed** when its case is closed; the population the sample draws from is the decision-log query of the period as P7 answers it, and this story applies no case state of its own and reads no `case` row (BR5).
- The verdict and the reason codes are a parameter row set: PASS and FAIL, and the codes RULE_VERSION_NOT_IN_FORCE, RULE_ROW_ABSENT and ANSWER_MISMATCH. The legacy story names none of them and the FSD names none, so the set is Not specified in the source documents (GAP-0873; ASM-1586) and it is held as parameter rows (ASM-1587).
- The sample size, the period bounds and the page bounds are Not specified in the source documents either (GAP-0873; ASM-1586): their names are fixed by RWB-P4-E8013-CON and their values are rows read through DP-06.

### 4. Flow

1. The conduct and QA officer opens SCR-39 Rules and parameters through the gateway-bff composite route (DP-19). The route shows the rule version in force and its evidence as `rwb-decision` answers them and calls this service only for the sample and its read.
2. The officer enters a period and a sample size and submits the run. The route calls `POST /api/recovery/access/v1/admin/qa-samples` on `rwb-access` with the body `from`, `to`, `sampleSize` and `reason`, and an `Idempotency-Key` header.
3. `QaSampleController` validates the request: every field is required, `from` and `to` are dates, `to` is not earlier than `from`, `sampleSize` is a whole number, and the period lies inside the bounds in force read through DP-06. An empty field, a wrong shape or a period outside its bounds is refused with 422 and MSG-GEN-001 naming the field, and no decision is read and no entry is written (BR11).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer and stores nothing and reads nothing (BR12, AC5).
5. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters R. A caller without the R letter is refused with 403 and MSG-P4-002, and nothing is read, no verdict is computed and no entry is written (BR3, AC3).
6. `ParameterReader` reads the default sample size, the period bounds, the page bounds and the reason-code set through `GET /api/recovery/case/v1/admin/parameters` of `rwb-case` with the version in force (DP-06). No cap, no bound and no code is a constant in code (BR11).
7. `QaSampleDrawer` reads the period through `GET /api/recovery/decision/v1/decision-log?from=&to=&page=` of `rwb-decision`, one hop with a 2 s timeout and a breaker, and takes from each entry only its entry id, its case id, its `decidedAt`, its `ruleId`, its `ruleVersion` and its recorded answer. It draws the sample by the rule and the size of the parameter rows, in a stable order, so the same request and the same data draw the same decisions in the same order (BR6, AC5).
8. For each drawn decision, `RuleModelClient` reads `GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` of `rwb-decision`, one hop with a 2 s timeout and a breaker, and takes from the answer the version's `valid_from`, its `valid_to` and the `rule_row` set of that version. No package source, no DRL and no KieBase is read or built (BR5).
9. `RuleVersionConsistencyChecker` runs the three checks of BR7 in order and stops at the first that fails: the version's `valid_from` and `valid_to` must cover the decision's `decided_at`; the recorded `rule_id` must be present in the version's `rule_row` set; and the recorded answer must agree with that row's `action_text` and `outputs`. A decision that passes all three is PASS with no reason code; a decision that fails one is FAIL with that one reason code.
10. `VerdictReasonResolver` maps the failed check to its code from the parameter rows, so the code is data and the checker holds no literal (BR10).
11. In one local transaction the service appends one entry to the decision-record chain of DP-03 with the record code of a QA sample, the `qaSampleId`, the period, the requested and drawn sizes, the passed and failed counts, the window and the reason code of each failure, and no person and no case narrative; sets the idempotency row to the answer; and stages the outbox row of the entry (BR8, BR12, AC5).
12. The answer is 201 with `qaSampleId`, `from`, `to`, `sampleSize`, `draws`, `passed`, `failed`, `state` and `recordedAt`, and the `Location` of the read (BR9).
13. Where `rwb-decision` cannot be reached, or answers beyond the 2 s budget, the call answers 503 with MSG-P7-003, nothing is recorded and no run is answered; the officer retries with the same `Idempotency-Key` and the reads are made again (BR12, X8).
14. Where the local record cannot be written, the answer is withheld with 503 and MSG-P7-003 (BR8, AC2); the retry with the same `Idempotency-Key` completes exactly one entry against the run, and the on-call engineer raises the incident on the record failure. The order of the reads and the record is Not specified in the source documents (GAP-0873; ASM-1586).
15. `GET /api/recovery/access/v1/admin/qa-samples/{qaSampleId}` answers the run with its counts and its `items[]`, each item carrying `decisionEntryId`, `caseId`, `decidedAt`, `ruleId`, `ruleVersion`, `verdict` and `reasonCode`, ordered by the draw order so the paging is stable, with the page default and maximum read through DP-06 (BR9, BR13).
16. The read answers the same items in the same order for the same `qaSampleId` on every call, because the item set is stored with the run and not drawn again (BR13, AC5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, `from` or `to` is not a date, `to` is earlier than `from`, or `sampleSize` is not a whole number | 422 naming the field; no decision read, no verdict, no entry | MSG-GEN-001 | AC1 |
| X2 | The period lies outside the bounds in force | 422 naming `from` or `to`; no decision read, no verdict, no entry | MSG-GEN-001 | AC5 |
| X3 | `sampleSize` exceeds the maximum in force | 422 naming `sampleSize`; the run is not silently shrunk, so the officer sees the cap | MSG-GEN-001 | AC5 |
| X4 | The caller holds no Rules and parameters R | 403, no decision read, no verdict, no entry | MSG-P4-002 | AC3 |
| X5 | The caller's session has ended | 401, no decision read, no verdict and no entry | MSG-P4-001 | AC3 |
| X6 | The period holds no closed decision | 201 with `draws` 0, `passed` 0 and `failed` 0, and an empty `items`; the run is recorded, so an empty population is visible | None | AC1 |
| X7 | A drawn decision names a rule version P7 does not hold | The item is FAIL with RULE_VERSION_NOT_IN_FORCE; the other items are tested and the run completes | None | AC4 |
| X8 | `rwb-decision` does not answer inside 2 s, or the connection fails | 503 and no entry; a retry with the same `Idempotency-Key` makes no second run | MSG-P7-003 | AC5 |
| X9 | The local decision-record entry, the idempotency row or the outbox row cannot be written | 503 and no run answered; nothing is recorded and the retry completes one entry | MSG-P7-003 | AC2 |
| X10 | The same run arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, one read | None | AC5 |
| X11 | A break-glass grant is active for the caller | The run proceeds and the answer carries the warning with the end time of the grant, and the entry carries the grant id | MSG-P4-004 | AC3 |

No exception path of this story changes a case, a task, a role, a permission, a rule version or a decision: the ledger and the registry belong to `rwb-decision`, and the only row this story writes of its own is the entry of its own chain plus the platform library rows of the request. A FAIL verdict is an observation about a decision already taken and never reopens the case it belongs to (BR14).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8013-CON and its fakes; the decisions and the rule versions are read through the P7 contract, so no ledger row and no rule row is held here |
| Negotiable | The sample size, the period bounds, the page bounds and the reason-code set are parameter rows; the run state set and the item order are reviewed with the P7 owner and with Internal audit |
| Valuable | One run proves, from the record alone, that the rule version stamped on each sampled decision was in force when it was taken, and leaves a record of the run |
| Estimable | One controller, one drawer, one consistency checker, one reason resolver, one run service, one run repository, two P7 clients, one record appender, one idempotency store, six fakes and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule, no screen and no event of its own |
| Testable | Each owned criterion has a test case in section 16; the three failures are provable with three seeded decisions, and the stable order and the replay are provable against a stored run |

### 7. Acceptance criteria

```gherkin
Feature: Run a QA sample against the rule version applied

  Background:
    Given the environment is SIT
    Given the decision log and the rule registry are held by rwb-decision and rwb-access holds no decision row and no rule row
    Given test user "U-6201" holds RW-CONDUCT, the role the FSD A2.24.3.3 role table names as the primary user, with Rules and parameters R in the SIT matrix
    Given test user "U-6202" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"
    Given test user "U-6203" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS"
    Given test user "U-6205" holds RW-PHONECOL with no letter in "RULES_AND_PARAMETERS"
    Given the rule ids "ALLOC-014", "ALLOC-015" and "ALLOC-030" in AC4 are test data and occur in no current source document

  Scenario: AC1 Run a QA sample against the rule version applied (legacy RWB-E8-013 AC1)
    Given the rwb-decision contract mock returns the closed decisions of the period with their rule id, rule version and decided time, and the rule versions they name
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then samples closed decisions and tests each against the rule version that was in force
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-013 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller with no letter in Rules and parameters is refused (new, D-RCV-60)
    Given "U-6205" holds RW-PHONECOL with no letter in "RULES_AND_PARAMETERS"
    When "U-6205" calls POST /api/recovery/access/v1/admin/qa-samples for from 2026-10-01, to 2026-10-31, sampleSize 20 and reason "monthly conduct check" with Idempotency-Key "k-013-3"
    Then the response is 403 with message MSG-P4-002 and no run is answered
    Then the rwb-decision contract fake records no decision-log read and no rule-model read
    Then no QA entry is appended and GET /api/recovery/access/v1/admin/qa-samples/{qaSampleId} answers no run for any id

  Scenario: AC4 The three consistency failures are named (new, D-RCV-60)
    Given the rwb-decision contract mock returns three closed decisions of the period
    And decision "D-901" records ruleId "ALLOC-014" and ruleVersion "ALLOC-2026.09" with decidedAt 2026-10-04 and a recorded answer of queue "MTG-BKK-CO"
    And rule version "ALLOC-2026.09" of package "ALLOCATION" carries valid_from 2026-10-15 and valid_to 2026-11-14
    And decision "D-902" records ruleId "ALLOC-030" and ruleVersion "ALLOC-2026.10" with decidedAt 2026-10-18
    And rule version "ALLOC-2026.10" of package "ALLOCATION" carries valid_from 2026-10-01 and valid_to 2026-10-31 and no row with ruleId "ALLOC-030"
    And decision "D-903" records ruleId "ALLOC-015" and ruleVersion "ALLOC-2026.10" with decidedAt 2026-10-20 and a recorded answer of queue "MTG-UPC-CO"
    And row "ALLOC-015" of that version carries action_text "queue MTG-BKK-CO" and outputs queue "MTG-BKK-CO"
    When "U-6201" runs the sample over that period with Idempotency-Key "k-013-4"
    Then the item for "D-901" is FAIL with reasonCode RULE_VERSION_NOT_IN_FORCE
    Then the item for "D-902" is FAIL with reasonCode RULE_ROW_ABSENT
    Then the item for "D-903" is FAIL with reasonCode ANSWER_MISMATCH
    Then the run answers draws 3, passed 0 and failed 3, and no case state, rule version or decision changes

  Scenario: AC5 The sample is bounded by parameter rows and a run is recorded once (new, D-RCV-60)
    Given the parameter rows in force set the maximum sample size to 50, the period bound to 400 days and the page maximum to 100
    When "U-6201" sends a run for a period of 60 days with sampleSize 500 and Idempotency-Key "k-013-5"
    Then the response is 422 with message MSG-GEN-001 naming sampleSize and no decision is read
    When "U-6201" sends a run for the period 2026-10-01 to 2026-10-31 with sampleSize 20 and Idempotency-Key "k-013-1"
    Then the response is 201 with a qaSampleId, draws 20, passed and failed summing to 20, a state and a recordedAt
    When "U-6202" calls GET /api/recovery/access/v1/admin/qa-samples/{qaSampleId} for that run
    Then the answer carries the same 20 items in the same order with their decisionEntryId, caseId, decidedAt, ruleId, ruleVersion, verdict and reasonCode
    When "U-6201" sends the same run again with Idempotency-Key "k-013-1"
    Then the first answer is replayed with the same qaSampleId and the same counts
    Then exactly one QA entry exists for the run and the rwb-decision contract fake records one decision-log read for it

  Scenario: AC6 The run entry carries its fields and a FAIL changes nothing (new, D-RCV-60)
    Given the rwb-decision contract mock returns the three closed decisions of AC4
    When "U-6201" runs the sample over that period with Idempotency-Key "k-013-6"
    Then the run entry carries the run id, the period, the requested and drawn sizes, the passed and failed counts, the window, the state, the time and the reason code of each failure
    Then no case, task, rule version or decision is changed or written

  Scenario: AC7 The check reads through the contract and evaluates no rule (new, D-RCV-60)
    Given the rwb-decision contract mock returns the closed decisions of the period with their rule versions
    When "U-6201" runs the sample over that period with Idempotency-Key "k-013-7"
    Then the three checks compare the values the contract returned and no rule package is evaluated and no KieBase is built
    Then no row of decision_log_entry, rule_package, rule_package_version, rule_row or rule_test_case is read or written in rwb_access

  Scenario: AC8 A call without a credential is answered 401 and an unknown run id is answered 404 (new, D-RCV-60)
    When a caller with no credential calls POST /api/recovery/access/v1/admin/qa-samples for from 2026-10-01, to 2026-10-31, sampleSize 20 and reason "monthly conduct check" with Idempotency-Key "k-013-8"
    Then the response is 401 and no run is answered
    When "U-6202" calls GET /api/recovery/access/v1/admin/qa-samples/{qaSampleId} for an id that names no run
    Then the response is 404 and no items are returned

  Scenario: AC9 A consumed call that fails or does not answer ends the run with no entry (new, D-RCV-60)
    Given the rwb-decision contract fake does not answer the decision-log read for the period
    When "U-6201" runs the sample over that period with Idempotency-Key "k-013-9"
    Then the run is not answered as 201 and no QA entry is appended
    Then no case, task, rule version or decision is changed or written
```

AC1 and AC2 are the two criteria of RWB-E8-013, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the decision mock, so the sample is provable while the `rwb-decision` contract is still a fake. AC3 to AC9 are new under D-RCV-60 and test only what this story adds: the right, the three consistency failures and the bounded, recorded and replayable run.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A sample of closed decisions is tested against the rule version that was recorded on each of them, and the result of the run is recorded with the rule version | RWB-E8-013 AC1; FSD P4 v3 A2.24; REQ-DRI-001 |
| BR2 | A decision record carries the rule id and the rule version that decided it, so the record alone is enough to test the decision afterwards | REQ-DRI-001, REQ-CWC-016; TSD P4 v3 T6.3 |
| BR3 | The run needs Rules and parameters R; a caller without it is refused with 403 and MSG-P4-002 and nothing is read, computed or recorded | TSD P4 v3 T6.1; FSD P4 v3 A2.24.4.3 |
| BR4 | The decision log and the rule registry are P7's: this story reads them through the P7 contract and holds no decision row, no rule row, no package source and no copy of a version state | Ownership Map v1 (`decision_log_entry`, `rule_row` = P7; ASM-0069); Architecture v5 slides 14 and 41; DP-01 |
| BR5 | The test is a consistency test and never a re-evaluation: no rule package is evaluated, no KieBase is built and no rule evaluator is called, because evaluation is the owning service's and the registry is P7's | Temporal and Drools Design slide 15 T6; ASM-1586 |
| BR6 | The sample is drawn by the rule and the size held as parameter rows, in a stable order, so the same request over the same data draws the same decisions in the same order | ASM-1587; FSD P4 v3 A2.24.3.1 BR-P4-024 |
| BR7 | Each drawn decision is checked in order: the recorded rule version's `valid_from` and `valid_to` cover the decision's `decided_at`; the recorded rule id is present in that version's `rule_row` set; the recorded answer agrees with that row's `action_text` and `outputs`. The first failure decides the item | REQ-CWC-016; TSD P4 v3 T3.1 DF-REF-001 to DF-REF-015, DF-REF-296 to DF-REF-298; ASM-1586 |
| BR8 | Every run appends exactly one entry to the local decision-record chain of DP-03 in the transaction that stores the answer; an answer that cannot be recorded is withheld with 503 and MSG-P7-003 | R-UNI-39; RWB-E8-013 AC2; DP-03 |
| BR9 | The entry and the answer carry the run id, the period, the requested and drawn sizes, the passed and failed counts, the window, the state, the time and the reason code of each failure | REQ-DRI-012; ASM-1588 |
| BR10 | The verdict is PASS or FAIL and each FAIL carries exactly one reason code, taken from a parameter row set and never from a constant in code | FSD P4 v3 A2.24.3.1 BR-P4-024; ASM-1587 |
| BR11 | The default sample size, the maximum sample size, the period bounds and the page bounds are parameter rows read through DP-06 with the version in force; a changed cap is data and needs no build | DP-06; BR-P4-024; ASM-1587 |
| BR12 | One `Idempotency-Key` answers one run: a replay answers the first answer, appends no second entry and makes no second read | Architecture v5 slide 42; DP-09 |
| BR13 | A run is answered from what this service stored: the same `qaSampleId` answers the same items in the same order, and the item set is never re-drawn on a read | REQ-DRI-012; ASM-1588 |
| BR14 | A FAIL verdict is an observation and changes nothing: no case is reopened, no task is raised, no rule version is moved and no decision is rewritten | REQ-DRI-002; DP-03; ASM-1588 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1, BR3 and BR7 are one ordered run in `QaSampleService`: authorise, read the parameters, read the period, draw, read each version, check, record. Each step that refuses returns before the next one is reached, so a refused run can never have read a decision.
- BR2 is not a rule of this service but the reason for it: the record of a decision carries `ruleId` and `ruleVersion` (Temporal and Drools Design slide 16), and a QA run that had to guess the version would be testing a re-evaluation and not the record.
- BR4 is the absence of a ledger and registry repository: the module has no table, no view and no join for `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case`, and every decision field and rule field arrives in a P7 answer.
- BR5 is the absence of a rule evaluator: the module has no KieBase, no DRL parser, no agenda listener and no DP-04 dependency, and the checker compares three values it was handed.
- BR6 and BR11 are the parameter reader at request time with the version in force: the size, the bounds and the order rule are rows, so a changed cap is data.
- BR7 and BR10 are the checker and the reason resolver: the checker returns which of the three checks failed, and the resolver maps that to the code the parameter rows hold.
- BR8, BR9 and BR13 are the record appender of DP-03 and its read: the entry and the stored items commit with the idempotency row, and the read is a read over that stored run with no write method.
- BR12 is the `idempotency_key` row of the platform library in `rwb_access`, written with the answer.
- BR14 is the absence of a side effect: the run writes no case, no task and no rule version, and a FAIL is answered and recorded only.

### 9. State transitions

This story holds no rule version state and no case state. The states it reads are `rwb-decision`'s, and the one state it records is the state of its own run.

| From | Event | Condition | To |
|---|---|---|---|
| No run | A sample is requested | R held, the fields valid, the period inside its bounds, P7 answers the period and the versions | One run recorded, answer 201 with its counts and its items |
| No run | A sample is requested | No R letter | Refused 403 with MSG-P4-002; no read, no entry |
| No run | A sample is requested | A field invalid, the period outside its bounds, or the size above the maximum | Refused 422 with MSG-GEN-001; no read, no entry |
| No run | A sample is requested | The period holds no closed decision | One run recorded with draws 0 and an empty item set |
| No run | A sample is requested | `rwb-decision` cannot be reached | Refused 503 with MSG-P7-003; no entry |
| No run | A sample is requested | The entry cannot be written | Refused 503 with MSG-P7-003; nothing recorded |
| Recorded | The same `Idempotency-Key` is sent again | None | The first answer is replayed; no second entry, no second read |
| Recorded | The run is read by its id | None | The same items in the same order, paged |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A run, or a refusal that is recorded at the service edge | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `rwb-decision` | A rule version is promoted or superseded | Its `valid_from`, its `valid_to` and its `rule_row` set change as P7 writes them; a run already recorded keeps the verdicts it reached |

A run recorded before a rule version is superseded keeps its verdicts: the entry is append-only, the comparison it made is stated in its items, and a later promotion at `rwb-decision` is P7's and not a correction of this run (BR4, BR13).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Conduct and QA officer (RW-CONDUCT) | Runs a sample and reads it: the primary user of the FSD P4 v3 A2.24.3.3 role table, holding `R` in Rules and parameters in the T6.1 matrix |
| Center of excellence analyst (RW-COE) | Also uses the feature per the FSD role table and holds `CRUD` in Rules and parameters; runs a sample and reads it, and authors no rule version here (that is P7's) |
| Internal audit (RW-AUDIT) | Also uses the feature and holds `R`; reads a run and its verdicts and runs a sample of a period |
| A role without Rules and parameters R (RW-PHONECOL, RW-FIELDCOL) | Refused with 403 and MSG-P4-002; nothing is read, computed or recorded |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` unchanged |
| `rwb-access` itself | Reads `role` and `permission` in its own schema and writes only its own chain and the platform library rows of the request |
| `rwb-decision` (P7) | Owns the decision log, the rule packages, their versions, their rows and their test cases; answers the period read and the rule-model read, and promotes a version at 00:01 |
| The owning service of a model | Evaluates its own package locally and writes the decision with the rule id and the rule version; this story never evaluates it |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right, 401 with MSG-P4-001 for no session, 422 with MSG-GEN-001 for a field, a period or a size, and 503 with MSG-P7-003 for a read or a record that cannot be completed. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8013-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the role code of the caller who ran the sample |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the Rules and parameters R letter and the role it is held through |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the run entry: `decision_code` DF-DEC-003, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the qaSampleId, the period, the sizes, the counts, the window and the reason code of each failure, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the run read |
| (run items) | the stored item set of a run in `rwb_access` | per item: `decisionEntryId`, `caseId`, `decidedAt`, `ruleId`, `ruleVersion`, `verdict`, `reasonCode`, and the draw order | Write and read |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a run | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the record row of the run entry | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` of `rwb_decision` | id, case_id, decision_code, rule_id, rule_version, model_version and the rest of the record | Returned through the P7 contract; not read |
| DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054, DF-REF-296 to DF-REF-298 | `rule_row` of `rwb_decision` | rule_id, rule_version, route_set, from_state, event_code, action_text, owner_role, timer_spec, valid_from, valid_to, rule_table, row_order, target_queue_code, package_version_id, drools_rule_name, outputs | Returned through the P7 contract; not read |
| DF-REF-274 to DF-REF-278, DF-REF-279 to DF-REF-295 | `rule_package`, `rule_package_version` of `rwb_decision` | package_code, version_label, status, valid_from, valid_to and the rest of the version | Returned through the P7 contract; not read |
| DF-REF-185 to DF-REF-197, DF-REF-299 | `rule_test_case` of `rwb_decision` | none | Not read |

No row of `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case` is read or written: they are `rwb-decision`'s (P7) under the ownership map and the ruling ASM-0069, and their fields arrive in the contract, not by a schema read (DP-01). No row of `case` or `task` is read either: a QA sample addresses a period and not a case, and the `caseId` it answers is the one P7 returned on the entry. No row of `delegation_limit` is read, because the sample tests rule versions and not approval limits. Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P4 v3 T3.1.

The name and the shape of a run id, the ordered field set of the run answer and of an item, the run state set, the reason-code set, the draw rule, and the record code of a QA sample are Not specified in the source documents (GAP-0873; ASM-1586): FSD P4 v3 A2.24 names the journey and one validation rule (VR-P4-024-1) and one business rule (BR-P4-024) and no operation and no field. The schema of RWB-P4-E8013-CON fixes them and this story reads and writes them as that contract publishes them.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/qa-samples` | P4 `rwb-access` | Body: `from`, `to`, `sampleSize`, `reason` | `qaSampleId`, `from`, `to`, `sampleSize`, `draws`, `passed`, `failed`, `state`, `recordedAt`, with `Location` of the read | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters R | `Idempotency-Key` required; a replay answers the first answer and makes no second read |
| GET | `/api/recovery/access/v1/admin/qa-samples/{qaSampleId}` | P4 `rwb-access` | Path: `qaSampleId`. Query: `page`, `size` | `QaSampleRun`: `qaSampleId`, `from`, `to`, `sampleSize`, `draws`, `passed`, `failed`, `state`, `recordedAt`, `items[]` of `decisionEntryId`, `caseId`, `decidedAt`, `ruleId`, `ruleVersion`, `verdict`, `reasonCode`, and `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters R | Not applicable, read only |

Both operations sit on the base `/api/recovery/access/v1` of DP-13. The read answers only what this service recorded, so its items and their order are the ones the run stored, and a later promotion of a rule version at `rwb-decision` is P7's answer and not this read's. `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR11). A `qaSampleId` this service issued but has no run for cannot arise, because ids are issued by this service and a run is never deleted, so the read has no 404 branch; a malformed id is a 422 with MSG-GEN-001.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters R check behind both operations, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The default sample size, the maximum sample size, the period bounds, the page bounds and the reason-code set, with the version in force (DP-06) |
| GET | `/api/recovery/decision/v1/decision-log?from=&to=&page=` | P7 `rwb-decision` | The closed decisions of the period: each entry's id, case id, `decidedAt`, `ruleId`, `ruleVersion` and recorded answer, from which the sample is drawn. Declared as consumed, never as provided, and named as the missing C dependency of the key (GAP-0873; ASM-1586) |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` | P7 `rwb-decision` | One rule-model version with its `valid_from`, its `valid_to` and its `rule_row` set, read once per drawn version and cached for the run. Declared as consumed, never as provided, and part of the same missing C dependency |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the authorise answer and the parameters read are cached for the session or the request, and a rule-model version is read once per run and reused across the decisions that name it. The two P7 operations are the decision-log query and the rule-model read of the P7 contract (Architecture v5 slide 14: `GET /decisions?caseId=` and `GET /rule-models/{n}/{v}`); this story declares them as consumed and never defines them, and its metadata carries no P7 contract dependency, which is the missing dependency raised in the key's gap row and not added to the metadata. No other operation of `rwb-decision`, `rwb-case`, `rwb-document` or `rwb-comms` is called, and no rule-version operation of the legacy endpoint table is called either: under the ruling ASM-0040 the rule-version paths belong to P7 and this story only reads a version.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a QA sample: the run id, the period, the requested and drawn sizes, the passed and failed counts, the window and the reason code of each failure |

CloudEvents 1.0 envelope, from the outbox of the transaction that stores the answer. The payload carries ids, counts, codes and times and no name, no e-mail address, no case narrative and no personal field. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` (RWB-P4-E1037-APP) and `DoaLimitChanged` (RWB-P4-E8008-APP), and a QA verdict changes no policy and no limit, so neither fits (Architecture v5 slide 14).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and the run answers from the P7 contract and its own chain. No `processed_event` row is written, and `RulePackageInForce` (EV-30) is not subscribed to: a run reads the version it needs at the time it runs.

#### 12.5 Workflows and activities

None. The run is synchronous: this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The daily chain check at 02:00 (JOB-14) is P7's Schedule and not a workflow of this story.

#### 12.6 Schedules

None. The run is request-driven; the six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP. A monthly conduct check is a person's act on the screen and not a Schedule of this story.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code of the caller who ran the sample |
| `permission` | P4 (`rwb_access`) | Read only: the Rules and parameters R letter and the role it is held through |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of a run. Read: the run read |
| the stored item set of a run | P4, in `rwb_access` | Write: the items of a run with their draw order. Read: the run read |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the entry and the idempotency row of the request; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's and is read through its contract |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the registry is P7's under ASM-0069 and is read through its contract |

No rule or ledger table is named as this service's and none is created here. `lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so a verdict or a reason code is taken from the parameter rows and validated against no list of this service (GAP-0873; ASM-1587). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| decision fake | the `rwb-decision` contract (GAP-0873; ASM-1586) | `GET /decision-log?from=&to=&page=` answering the closed decisions of a period with their entry id, case id, `decidedAt`, `ruleId`, `ruleVersion` and recorded answer; an empty period; a 503 for X8 |
| rule-model fake | the `rwb-decision` contract (GAP-0873; ASM-1586) | `GET /rule-models/{packageCode}/{versionLabel}` answering "ALLOCATION" version "ALLOC-2026.09" with `valid_from` 2026-10-15 and `valid_to` 2026-11-14, version "ALLOC-2026.10" with `valid_from` 2026-10-01 and `valid_to` 2026-10-31 and its `rule_row` set, and a 404 for a version P7 does not hold |
| authorise fake | RWB-P4-E8013-CON, RWB-P4-E1037-CON | A granted answer for RW-CONDUCT, RW-COE and RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-PHONECOL with no letter |
| parameters fake | the `rwb-case` contract (RWB-P3-E1042-CON) | The default sample size, the maximum sample size, the period bounds, the page bounds and the reason-code set, with the version in force |
| decision-record fake | RWB-PLT-E1027-CON | The append of a run, the hash-link check, a seeded run with its items, and the forced failure AC2 needs |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-39 with the rule version in force and its evidence, the run form and the run panel |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the run and the read); consumed 4 | Base `/api/recovery/access/v1`; two `rwb-decision` operations, the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | No file input and no file output: the run is a request, and a report export is not part of this capability |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/qasample`, Java package `th.co.scb.ace.workbench.recovery.access.qasample`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | the monolith REST base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module decision-log read and the in-module rule-row read of the monolith (DP-01 and DP-13: the ledger and the registry owned by P7 and addressed on this service's own base through the P7 contract), and the ace-web screen that read a rule version in process (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. **DP-04 is not applied**: this story evaluates no rule package, so it needs no embedded Drools kit, no `RWB-PLT-E1072-CON` and no `RWB-P7-E1073-CON`; the consistency test reads the recorded version and its row and never runs the engine (BR5). DP-08 is not applied either: the right is checked through the own authorise operation, which is the service baseline, and this story calls no guard library. The two `rwb-decision` operations are consumed through the P7 contract and its fake, and the missing C dependency is raised in the key's gap row and not added to the metadata.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| QaSampleController | Controller | The two operations: validation, the `Idempotency-Key` lookup, the RFC 9457 problem responses, `Location` on a created run |
| QaSampleService | Service | The ordered run of BR1, BR3 and BR7: right, parameters, period, draw, version reads, checks, record; a refusal returns before the next step |
| QaSampleDrawer | Service | The sample of BR6: the population from the P7 answer, the size from the parameter rows, the stable draw order |
| RuleVersionConsistencyChecker | Service | The three checks of BR7 in order, stopping at the first failure, and the verdict |
| VerdictReasonResolver | Service | The reason code of a failed check, read from the parameter rows and never held as a literal (BR10) |
| QaSampleRunService | Service | The answer of BR9: the counts, the state, the `recordedAt` and the entry payload |
| QaSampleRunRepository | Repository | The stored run and its item set in `rwb_access`: write on the run, read on the read, with no re-draw |
| DecisionLogClient | Client | The `rwb-decision` decision-log query, one hop, 2 s timeout and a breaker; maps a timeout to 503 |
| RuleModelClient | Client | The `rwb-decision` rule-model read by package code and version label, one hop, 2 s timeout, a breaker and a per-run cache; maps a 404 to the absent-version check |
| PermissionReader | Service | The `role` and `permission` rows of the caller and the Rules and parameters R letter |
| ParameterReader | Service | The default size, the maximum size, the period bounds, the page bounds and the reason-code set through DP-06, with the version in force |
| DecisionRecordAppender | Service | The run entry with its outbox row, in the transaction that stores the answer (DP-03, DP-09) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` are created by RWB-P4-E1037-APP, the local decision-record table by RWB-P4-E1039-APP and the platform library tables by the service's own DB story, in the per-service Flyway sequence of DP-15; this story reads and uses them.
- The stored item set of a run is a table of this service in `rwb_access`, created by the same DB story; it holds the run id, the draw order and the seven item fields, and it is written once per run and never updated (BR13).
- No decision-log or rule table is created in `rwb_access` and no column of one is copied: a copy would be a second writer of a ledger entry and would drift from `rwb-decision` on the first correction (BR4).
- No write statement touches `role`, `permission` or `delegation_limit`: the readers are read-only, so a run can never grant itself a right or move a limit.
- The entry, the stored items, the idempotency row and the outbox row commit in one transaction; a failure rolls all four back and the answer is withheld with MSG-P7-003 (BR8).

**Configuration and reference data**

- The default sample size, the maximum sample size, the period bounds and the page bounds are parameter rows of `rwb-case` read through DP-06 with the version in force; no bound is a constant in code (BR11). Their names are fixed by RWB-P4-E8013-CON.
- The reason-code set is a parameter row set of the same contract: PASS, FAIL, RULE_VERSION_NOT_IN_FORCE, RULE_ROW_ABSENT and ANSWER_MISMATCH at the version in force, and a code that is not in the set is a configuration error and not a silent pass (BR10).
- The draw rule — the ordering key of the population and the rounding of the drawn size — is a parameter row too, so a change of sampling policy is data (BR6, ASM-1587).
- The role codes are read from `role` through the `permission` row that carries the R letter; no role code and no capability area is a constant in code (BR3).

**Build steps**

1. `QaSampleController` and its validation; tests for X1, X2 and X3 with no decision read.
2. `PermissionReader` and the authorise call of step 5; test the AC3 refusal of a caller with no letter, with no P7 read and no entry afterwards.
3. `DecisionLogClient` and `QaSampleDrawer` over the decision fake: the period read of AC1, the empty period of X6, the stable order and the draw size.
4. `RuleModelClient` over the rule-model fake: the two versions of AC4, the absent version of X7 and the 503 of X8.
5. `RuleVersionConsistencyChecker` with the three checks in order; tests for AC4, one per failure, and the proof that a decision that passes all three is PASS with no code.
6. `VerdictReasonResolver` over the parameters fake; test that a changed code set is data and that a code outside the set fails the run rather than passing it.
7. `QaSampleRunService`, `QaSampleRunRepository`, `DecisionRecordAppender` and `IdempotencyStore` in one transaction; test the replay of AC5 with one entry and one read, and the forced failure of AC2 with no record.
8. The run read over a seeded run of twenty items; test the order, the paging, the same answer on every call and the absence of a re-draw.
9. The contract-fake run of both operations through the gateway-bff fake, so SCR-39 can be demonstrated while the route and the P7 platform are being built.

**Feature switch.** The two operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. A run that is switched off would leave a period untested and invisible as such, which is the state the sample is meant to resolve, so this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; a sample of twenty closed decisions is run by RW-CONDUCT and answered with its counts and its items; a caller with no letter is refused with MSG-P4-002 and no decision is read; the three seeded decisions of AC4 are FAIL with RULE_VERSION_NOT_IN_FORCE, RULE_ROW_ABSENT and ANSWER_MISMATCH and nothing changes for any of them; a size above the maximum is refused with MSG-GEN-001; the same run id answers the same items in the same order; the same `Idempotency-Key` replays one answer with one entry and one read; and a forced record failure withholds the answer with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters R | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the run answer, with the grant id recorded in the entry |
| MSG-GEN-001 | A required field is empty, `from` or `to` is not a date, `to` is earlier than `from`, `sampleSize` is not a whole number, the period is outside its bounds, or the size is above the maximum | Enter {field}. | This story, on both operations |
| MSG-P7-003 | `rwb-decision` cannot be reached, or the entry, the stored items, the idempotency row or the outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001 and MSG-P7-003 are the legacy texts, and VR-P4-024-1 of the FSD is the rule behind MSG-GEN-001. The four-eyes message of a rule package approval is not produced here: this story approves no rule version and its failure codes are the three of BR7, not a message. MSG-P3-022, the missing checklist item, is not produced here either, because this story approves no package version.

### 15. Screens and states

SCR-39 Rules and parameters is the screen, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), which shows the rule version in force and its evidence as `rwb-decision` answers them and calls the two operations of this story, one hop each. This story renders no screen surface of its own.

| Screen | State | What it shows |
|---|---|---|
| SCR-39 Rules and parameters | Rule version in force | The version in force and its evidence as `rwb-decision` answers them, with the run panel of this service beside it |
| SCR-39 Rules and parameters | Sample, form | The period, the sample size and the reason, with the size and the bounds shown from the parameter rows in force |
| SCR-39 Rules and parameters | Sample, recorded | The 201 answer with `qaSampleId`, `from`, `to`, `sampleSize`, `draws`, `passed`, `failed`, `state` and `recordedAt` |
| SCR-39 Rules and parameters | Sample, items | One row per drawn decision with its decision entry, case, decided time, rule id, rule version, verdict and reason code, paged |
| SCR-39 Rules and parameters | Sample, all passed | A run with `failed` 0 and every item PASS, so a clean period is visible as a clean period |
| SCR-39 Rules and parameters | Sample, failures | A run with its FAIL items and their reason codes, with no action offered on the case they belong to |
| SCR-39 Rules and parameters | Sample, refused | The 403 of X4 with MSG-P4-002 for a role without the R letter |
| SCR-39 Rules and parameters | Sample, out of bounds | The 422 of X2 or X3 with MSG-GEN-001 naming the field and the bound in force |
| SCR-39 Rules and parameters | Not recorded | The 503 of X9 or X8 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-39 Rules and parameters | Sample, error | The 422 of X2 or X3 and the 503 of X9 or X8 listed above, each with its message |
| SCR-39 Rules and parameters | Sample, no access | The 403 of X4 with MSG-P4-002 for a role without the R letter, shown as no access |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (CG-ALL-5566) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-5566) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-5566) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-5566) |
| SCR-40 | Empty | Not specified in the source documents (CG-ALL-5567) |
| SCR-40 | Loading | Not specified in the source documents (CG-ALL-5567) |
| SCR-40 | Error | Not specified in the source documents (CG-ALL-5567) |
| SCR-40 | No access | Not specified in the source documents (CG-ALL-5567) |
| SCR-41 | Empty | As defined in Screen Specifications v1, section SCR-41 |
| SCR-41 | Loading | Not specified in the source documents (CG-ALL-5568) |
| SCR-41 | Error | Not specified in the source documents (CG-ALL-5568) |
| SCR-41 | No access | Not specified in the source documents (CG-ALL-5568) |
| SCR-42 | Empty | Not specified in the source documents (CG-ALL-5569) |
| SCR-42 | Loading | Not specified in the source documents (CG-ALL-5569) |
| SCR-42 | Error | Not specified in the source documents (CG-ALL-5569) |
| SCR-42 | No access | Not specified in the source documents (CG-ALL-5569) |
| SCR-43 | Empty | Not specified in the source documents (CG-ALL-5570) |
| SCR-43 | Loading | Not specified in the source documents (CG-ALL-5570) |
| SCR-43 | Error | Not specified in the source documents (CG-ALL-5570) |
| SCR-43 | No access | Not specified in the source documents (CG-ALL-5570) |
| SCR-47 | Empty | Not specified in the source documents (CG-ALL-5571) |
| SCR-47 | Loading | As defined in Screen Specifications v1, section SCR-47 |
| SCR-47 | Error | Not specified in the source documents (CG-ALL-5571) |
| SCR-47 | No access | Not specified in the source documents (CG-ALL-5571) |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority in its screen table although a QA sample sits on neither of them as a panel of its own; the target screen is SCR-39 Rules and parameters, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The FSD P4 screen list names no QA-sample screen — it lists SCR-39, SCR-40, SCR-41, SCR-42, SCR-43 and SCR-47 and no sample screen — so this story claims no screen id of its own and the absence is carried in the key's gap row rather than filled with an invented id (GAP-0873; ASM-1586).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-013-01 | AC1, BR1, BR2, BR6, BR7 | Component | The decision fake answers twenty closed decisions of 2026-10-01 to 2026-10-31 and the rule-model fake their versions; the run by RW-CONDUCT answers 201 with `draws` 20, `passed` and `failed` summing to 20, a state and a `recordedAt`, and every item carries its decision entry, rule id, rule version and verdict |
| TC-E8-013-02 | AC2, BR8 | Component | The record store forced to fail during the run: 503 with MSG-P7-003, no run answered and no entry; a retry with the same `Idempotency-Key` completes exactly one entry |
| TC-E8-013-03 | AC3, BR3 | Component | A caller holding RW-PHONECOL with no letter in Rules and parameters: 403 with MSG-P4-002, no decision-log read, no rule-model read, no entry and no run answered |
| TC-E8-013-04 | AC2, BR8 | NFR | The append, the stored items and the outbox row forced to fail under load: every failure is a 503 with MSG-P7-003, no partial run is ever readable, and the retry path yields one entry |
| TC-E8-013-05 | AC4, BR7, BR10 | Component | Three seeded decisions: "D-901" whose version was not in force at its decided time is FAIL with RULE_VERSION_NOT_IN_FORCE, "D-902" whose rule id is absent from the version is FAIL with RULE_ROW_ABSENT, "D-903" whose answer disagrees with the row is FAIL with ANSWER_MISMATCH, and no case, task or rule version changes |
| TC-E8-013-06 | AC5, BR6, BR11, BR12, BR13 | Component | The parameter rows at a maximum of 50 and a period bound of 400 days: sampleSize 500 refused 422 with MSG-GEN-001; a 20-item run answered once, read twice with the same items in the same order, and replayed on `Idempotency-Key` "k-013-1" with one entry and one read |
| TC-E8-013-07 | AC7, BR4, BR5 | Contract | Every operation, event and activity of section 12 checked against the schema of RWB-P4-E8013-CON with the rwb-decision contract fake; the run reads no decision-log row and no rule row from any table, and no rule package is evaluated |
| TC-E8-013-08 | AC6, BR8, BR9, BR14 | Component | Boundary test of each table of section 12.7 (the DP-03 record, the stored item set and the outbox row): the run entry carries the fields of BR9, a FAIL run writes no case, task, rule version or decision, and no table outside section 12.7 is written |
| TC-E8-013-09 | AC8 | Component | A call with no credential: 401 and no run answered; a GET of a run id that names no run: 404 and no items returned |
| TC-E8-013-10 | AC9 | Component | The rwb-decision contract fake does not answer the decision-log read: the run is not answered as 201, no QA entry is appended, and no case, task, rule version or decision changes |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-013-01 for AC1, TC-E8-013-02 for AC2, TC-E8-013-03 for the access refusal and TC-E8-013-04 for the forced record failure; four rows are added for the new criteria of this story. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the default and maximum sample size, the period bounds, the page bounds, the draw rule and the reason codes are parameter rows (BR6, BR10, BR11), and a test proves that a changed cap needs no build.
- No personal data anywhere: the request, the answer, the items and the entry carry ids, dates, rule ids, rule versions, verdicts, reason codes and counts; no name, no e-mail address and no case narrative appears in the answer, the entry or a test (BR9, NFR-040).
- No read of another service's tables (DP-01): `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's, and no join crosses a schema. The decision fields and the rule fields arrive in the P7 answer.
- No second opinion on a decision: the run never evaluates a package, never builds a KieBase and never rewrites a decision, so a FAIL is an observation and not a re-decision (BR5, BR14).
- No record without its answer: the entry, the stored items and the outbox row commit with the answer, and the answer is withheld with MSG-P7-003 when they cannot be written (BR8, R-UNI-39).
- One key, one run: the `Idempotency-Key` is stored with the answer, so a retry after a timeout cannot create a second run or a second entry (BR12).
- A run cannot be re-drawn: the items are stored with the run, so the same id answers the same items in the same order and a later rule promotion cannot change a past verdict (BR13).
- A run reads what it needs and no more: the decision query answers six fields per entry and the rule-model read one version at a time, so the sample never pulls a case narrative or a package source into this service.
- Every example, fixture and test payload is synthetic; no ledger entry, rule package or production payload is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Program, Decision record | FEAT-ADM-08 | All recovery processes | BR1, BR2, BR7 | TC-E8-013-01, TC-E8-013-05 |
| REQ-DRI-012 | Audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call | Program, Decision record | FEAT-ADM-08 | All recovery processes | BR1, BR9, BR13 | TC-E8-013-01, TC-E8-013-06, TC-E8-013-08 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Program, Case and workflow | FEAT-ADM-08 | All recovery processes | BR2, BR5, BR7 | TC-E8-013-05, TC-E8-013-07 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 run a QA sample against the rule version applied, and the record of the result with the rule version | Sections 1, 4, 7, 8, 12.1, 12.2 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 14 |
| The permission checks of the legacy table, Rules and parameters C for RW-COE and A for RW-RISK, read here as the R letter of the T6.1 matrix (GAP-2285, ASM-B2-P4-013-4) | Sections 3, 7 (AC3), 8 (BR3), 10, 12.1 |
| The legacy endpoint table's two rule-version paths, which are P7's under ASM-0040 and are not provided here | Sections 3, 8 (BR4), 12.2, 19 |
| MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The legacy data rows `decision_log_entry` DF-DEC-001 to DF-DEC-018, `rule_row` DF-REF-001 to DF-REF-015 and `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7 |
| TC-E8-013-01 to TC-E8-013-04 | Section 16 |
| Legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried to SCR-39 Rules and parameters |
| FEAT-ADM-08 and its dependency FEAT-DRI-03 | Sections 2, 3, 18 |
| Legacy key RWB-E8-013, story RWB-P4-E8013-APP, contract RWB-P4-E8013-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The decision log, its entries, its query API and its corrections: `rwb-decision` (P7) under the ownership map, read here through its contract and never by a schema read.
- The rule registry, its packages, their versions, their rows and their test cases: `rwb-decision` (P7) under the ruling ASM-0069.
- The Drools evaluation of a package, the rule packages in force and the promotion at 00:01: P7 governance and the local evaluation of the owning service, DP-04, and neither is part of this story.
- The chain-integrity check at 02:00 (JOB-14) and the daily ledger seal: RWB-P4-E8015-APP and P7's own Schedule.
- The publication and the rollback of an access configuration version: RWB-P4-E8012-APP and RWB-P4-E8011-APP.
- The permission matrix, the role administration and the masking policy: RWB-P4-E1037-APP and the Epic 8 administration stories.
- The screen SCR-39 Rules and parameters itself, its other panels and its composite route specification: RWB-PLT-N001-CON.
- The integration harness and the `-ITG` copies of the test cases: no ITG story is split from this legacy key.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
