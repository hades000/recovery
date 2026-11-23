# RWB-P7-E2035-APP Next action on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2035-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-AL |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2035-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for rwb-decision, the registry side of the next action. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As **the case workflow's rule evaluation and the case owner, team manager and internal auditor who read a next action**, I want **the decision service to answer three questions from its own registry — what the row of the rule that moved a case says (action text, owner role, timer spec, to-state), which version of the package is in force, and which rule and rule version set the latest state change of a case in the ledger — without reading a workbook, a generated DRL, a case table or another service's schema**, so that **every next action in the target names the rule and the package version that produced it, and a re-read of an old case gets the row that moved it and never the row of a later version**.

Inside `rwb-decision` this is the registry slice of legacy RWB-E2-035:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- Behind `GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=`, the operation `RWB-P3-E2042-CON` publishes and `RWB-P2-E2035-CON` consumes as `RuleCatalog.row(ruleId, packageVersion)`: the row of one rule in one package version — DF-REF-008 `action_text`, DF-REF-010 `owner_role`, DF-REF-011 `timer_spec`, DF-REF-009 `to_state`, DF-REF-003 `rule_version`, DF-REF-297 `drools_rule_name` and DF-REF-298 `outputs`.
- Behind `GET /api/recovery/decision/v1/decision-log?caseId=&latestStateChange=true`, the read the fill uses when a case has no next action: the latest state change of the case, with DF-DEC-004 `rule_id`, DF-DEC-005 `rule_version`, the entry ID and DF-DEC-016 `decided_at`, in `chain_seq` order.
- The version facts both answers carry, read from `rule_package` and `rule_package_version`: the package code, the version label, the version state and whether that version is in force. The version in force per environment is what the callers' embedded kit checks before it evaluates, and no lock file exists.
- Rows are immutable once stored: a row of a SUPERSEDED or ROLLED_BACK version is still answered, which is what makes a re-read of an old case return the action that was set (legacy BR10, legacy AC11).

Not this story, and stated again in section 6 and section 19:

- The five case fields, the `NEXT_ACTION_MISSING` task and its cancel, the JOB-05 check, the read endpoint and the case list and export columns are **RWB-P3-E2035-APP**; the resolve, the read and the fill are **RWB-P2-E2035-APP** and **RWB-P2-E2035-CON**.
- The role name and class, the authorise answer, the service levels and timers rows and the calendar are **RWB-P4-E2035-APP**, **RWB-P4-E1037-CON** and **RWB-P3-E1043-CON**. This story returns the owner role as a code and computes no due date.
- The registry load, the six checks, the four-eyes approval, the promotion and the rollback are **RWB-P7-E1073-APP** and **RWB-P7-E2042-APP**. This story reads their rows and writes none of them.
- The cross-service proof is **RWB-ITG-E2035-ITG**; every criterion of this story is proved against the registry alone or through a contract fake.

The database login is the per-service login of DP-02, written only as "the rwb-decision login (DP-02)". Its name is Not specified in the source documents (GAP-2411; ASM-4010), and the shared monolith login appears nowhere in this story.

### 2. Business rationale

A case owner today reads the case history to work out what is owed next, and a case can wait with nobody owing anything on it. The rule package that moves the case already holds the action, the owner and the timer, and the next action copies them onto the case — but only because a caller can ask what a rule row says. In the monolith that question was answered in process by `RuleCatalog.row`, over a table shared by every module; in the target the table is `rwb_decision`'s and every other service reaches it over one contract (DP-01, DP-04, DP-11). Two facts travel with it: the version the row belongs to, and the version that set the last state change of the case, which is where the fill starts when a case has no next action at all.

This story is the rwb-decision half of the RWB-E2-035 split. It supplies the row, the version state and the ledger lookup, and it supplies them read-only: a catalogue row and a ledger entry are evidence, and evidence that can be edited at a read is worthless in audit (NFR-033, NFR-034). It meets REQ-WKM-013 on the rule that set the action, REQ-WKM-012 on every case carrying one, REQ-WKM-016 on the case with none, REQ-WKM-014 on what is shown and REQ-WKM-015 on the version an overdue action is escalated under.

The realignment changes the mechanism, not the business rule:

1. The `rule_row`, `rule_package_version` and `decision_log_entry` rows move into `rwb_decision`, and no other service reads them (DP-01); the DF-REF and DF-DEC field IDs are unchanged.
2. `RuleCatalog.row(ruleId, packageVersion)` becomes one REST read under `/api/recovery/decision/v1` (DP-13) with a 2 s budget and a cache, instead of an in-process call (DP-11).
3. The decision-log query of the latest state change becomes a filter on the decision-log read of the service, not a second store (DP-03).
4. The rule row, the package version and the ledger entry are read through the service's own schema and its own Flyway sequence (DP-15); the topic and event names of the service are the per-service ones (DP-14).
5. Nothing a business person may change is written in code: the action text, the owner role, the timer spec, the version labels and the version states are rows (DP-06, DP-07).

The measure is the legacy one, the count of active cases with no next action, at zero, plus the registry measure this slice adds: every next action on a case names a rule ID and a package version that the registry can answer for that version, and no answer is served from a superseded row in place of the row that moved the case.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E2035-CON | The two consumed shapes this story provides: `GET /rule-catalog/{ruleId}?packageVersion=` returning action_text, owner_role, timer_spec and outputs, and `GET /decision-log?caseId=&latestStateChange=true` returning rule ID and rule version, with their 2 s client budget and their fakes |
| RWB-P3-E2042-CON | The published `RuleCatalog.row` operation name, the package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH, the version-state vocabulary and the `RulePackageInForce` consumption contract (DP-04) |
| RWB-P7-E1073-APP, RWB-P7-E2042-APP | The rows this story reads: the registry load, the four-eyes approval, the 00:01 promotion to IN_FORCE and the rollback, and the version and dry-run reads. Reused where they have landed; built against their published set and fake |
| RWB-P7-E1008-APP, RWB-P7-E1027-APP, RWB-P7-E1027-CON | The ledger store, its append-only rule and its read indexes, and the decision-record contract: the entries this story reads are written by these stories, never here |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): the `RuleResult` and `NoPackageInForce` types and the version-in-force check. This story supplies the facts; the kit raises the outcome in the owning service |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON; RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The parameters and reference-data client libraries and contracts (DP-06, DP-07): the business date, the version-state list and DF-SYS field names |
| RWB-PLT-E1044-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON | The per-service Flyway sequence (DP-15), the naming library (DP-14) and the gateway-bff route (DP-19) |

The DP-added H and C dependencies above — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON, and C RWB-P2-E2035-CON, RWB-P3-E2042-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON — are platform contracts of wave 0 and published contracts an APP story builds against as fakes, so none blocks this story and Ready to start stays Day 1 (GAP-2410; ASM-4009). The registry rows this story reads are the same service's and are in place from the wave-1 stories named above.

Business preconditions carried from RWB-E2-035:

- Package RESTRUCTURE version "RES-2026.12" holds R-RES-04, R-RES-03, R-SET-13, R-DEV-05 and R-RES-07 with the action text, owner role and timer spec of the background below. The valid-from date of that version is GAP-2406: the registry stories carry 2026-12-15 and the legacy tests of this key read it as in force on 11 December 2026; ASM-4005 pins the fixture until it is reconciled.
- The version states are LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (Temporal and Drools design, adopted by RWB-P7-E1073-APP).
- No RESTRUCTURE version is in state IN_FORCE on 2027-01-04, which is the fixture of legacy AC14.
- Roles and rights: RW-COE holds Rules and parameters R, RW-AUDIT holds Rules and parameters R and Decision log R, and the service identities SY-RULES and SY-CASEWF hold the read letters of their own service. No role holds a write letter on this path.
- Synthetic data only: package codes, version labels, rule IDs, dates, role codes and entry IDs of the legacy story. No real account, customer, party or case appears in a read, a test or a fixture.

### 4. Flow

1. Caller: the case workflow's `EvaluateRules` activity, holding the `RuleResult` of a fired rule, calls `GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion={label}` with the rule ID and the version label the evaluation returned.
2. `RuleCatalogController`: authenticates the session or the service identity, checks Rules and parameters R through the authorise contract of rwb-access, and validates the two parameters. A blank or malformed parameter is 422 with MSG-GEN-001 naming the field (BR7).
3. `VersionStateResolver`: reads the `rule_package` row and the `rule_package_version` row of the label, and the version state and valid-from and valid-to it holds. A label the package does not hold is 404 with MSG-P3-027 for the version check.
4. `RuleCatalogService`: reads one `rule_row` by `rule_id` and `rule_version` through the catalogue index, and builds the answer: action text, owner role, timer spec, to-state, rule version, Drools rule name, the outputs map, the package code, the package version and its state (BR1, BR2).
5. The answer is returned as stored, character for character: the timer spec is a string and the outputs a map, and the service computes no due date, no working-day count and no calendar (BR3). The vocabulary of a timer spec has no list in any source (GAP-2408; ASM-4007).
6. Caller: the fill of a case with no next action calls `GET /api/recovery/decision/v1/decision-log?caseId={caseId}&latestStateChange=true`. `DecisionLogQueryService` reads the `decision_log_entry` rows of the case in `chain_seq` order, takes the newest entry that carries a rule ID and a rule version, and answers the rule ID, the rule version, the entry ID and the decided-at time (BR5).
7. A case with no such entry is answered 200 with an empty result and `missing` true, not an error; a case with one entry answers that entry even when it is old (BR5, BR6).
8. No step of either read writes anything: no rule row, no version row, no ledger entry, no decision record and no outbox row. The read is idempotent for its inputs, and the cache is keyed by package version and dropped when this service promotes or rolls back a version (BR8, BR9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A call carries no `packageVersion`, a blank `ruleId` or a malformed `caseId` | 422 before any row is read; the field is named and nothing is answered | MSG-GEN-001 | AC4 |
| X2 | The package version label exists but holds no row for the rule ID | 404; no default row, no last row and no row of another version is substituted | MSG-P3-027 | AC4 |
| X3 | The package code or the version label is unknown to the registry | 404 with the version check named; the registry is never asked to guess a version | MSG-P3-027 | AC4 |
| X4 | No version of the package is in force on the business date | The version list names no IN_FORCE row, the answer carries `inForce` false, and the caller's kit raises `NoPackageInForce`; this service invents no default | MSG-P3-027 | AC5 |
| X5 | The case has no state change in the ledger | 200 with an empty result and `missing` true; the fill raises its own task; the read is not an error | None | AC7 |
| X6 | The same decision record is delivered twice with one idempotency key | One entry, the first; both reads answer the same entry and the repeat is counted by the wave-1 ingest | None | AC7 |
| X7 | The caller's role holds no read letter | 403 before a row is read; no rule text, owner role, version label or entry ID is returned | MSG-P4-002 | AC9 |
| X8 | The registry or the ledger cannot be read | 503, nothing is answered, the caller retries inside its budget and an incident is raised | MSG-GEN-006 | AC8 |
| X9 | The row is read with a case fact in the answer or through a workbook, a DRL or another schema | Refused at review and failed by the build check: this service answers rows, never case values | None | AC10 |

X1 to X3 are the lookup refusals of the legacy `RuleCatalog.row` carried onto this service; X4 is legacy AC14 on the registry side; X5 to X6 are legacy AC9, AC10 and AC11 on the ledger side; X7 to X9 are the target's own boundaries. Whether an absent `packageVersion` may be answered with the row of the version in force is GAP-2409; ASM-4008 fixes the refusal of X1.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads `rwb_decision` only and builds against the RWB-P2-E2035-CON, RWB-P3-E2042-CON and RWB-P4-E1037-CON fakes; calls no other service at run time |
| Negotiable | Nothing business is fixed here: the action text, the owner role, the timer spec, the version labels and the states are rows and list values |
| Valuable | The next action can always name the rule and the version that set it, and an old case is never re-read against a newer version |
| Estimable | Two read operations, one version-state resolver, two repositories, one cache and one index |
| Small | Fits one sprint with its tests; no screen, no workflow, no Schedule and no write path |
| Testable | Every criterion below has a test case in section 16, on registry and ledger fixtures |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given package "RESTRUCTURE" version "RES-2026.12" holds rule R-RES-04 under rule version "RES-2026.12", which moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role "RW-RESTRUCT" and timer "2 working days"
    Given the same version holds R-SET-13 with owner role "CU-BORROW" and timer "payment due 30 days", R-RES-03 with owner role "RW-CASEOWN" and timer "None", R-DEV-05 with owner role "RW-LEGAL" and timer "deadline driven", and R-RES-07 with timer "same day"
    Given the rwb-integration contract mock returns the next action of case "RW-2026-000401" for rule "R-RES-04" of package version "RES-2026.12"
    Given version "RES-2026.12" is in state IN_FORCE from 2026-12-01 and holds no valid-to date

  Scenario: AC1 The row of the firing rule is answered (new, D-RCV-60)
    Given the case workflow holds RuleResult package "RESTRUCTURE", package version "RES-2026.12" and rule "R-RES-04" for case "RW-2026-000401"
    When it calls GET /api/recovery/decision/v1/rule-catalog/R-RES-04?packageVersion=RES-2026.12
    Then the answer is 200 with ruleId "R-RES-04", ruleVersion "RES-2026.12", packageCode "RESTRUCTURE", packageVersion "RES-2026.12", actionText "Assign the case to a restructuring officer and start the offer clock", ownerRole "RW-RESTRUCT", timerSpec "2 working days" and toState "WITH_FCR_OFFICER"
    Then the answer carries the outputs map of the row and no due date, because 15 December 2026 is the caller's arithmetic

  Scenario: AC2 The row follows the version named by the caller (new, D-RCV-60)
    Given version "RES-2026.12" of package "RESTRUCTURE" is SUPERSEDED and version "RES-2027.01" is IN_FORCE on 2027-01-04
    Given both versions hold a row for rule R-RES-04 and the row of "RES-2026.12" carries timer "2 working days"
    When the fill of case "RW-2026-000402", whose last state change was made under "RES-2026.12", reads the row
    Then the answer is the row of "RES-2026.12" with timer "2 working days", packageVersion "RES-2026.12", versionState "SUPERSEDED" and inForce false
    Then the row of "RES-2027.01" is not substituted, so an action already set is never rewritten

  Scenario: AC3 A timer spec is answered as stored (new, D-RCV-60)
    Given the five rows of the background each carry the timer spec named there
    When each row is read under "RES-2026.12"
    Then each timerSpec is returned character for character: "2 working days", "payment due 30 days", "None", "deadline driven" and "same day"
    Then no due date, no working-day count, no holiday and no default is applied, and a spec the service does not recognise is returned as stored

  Scenario: AC4 An unknown row or a missing parameter is refused (new, D-RCV-60)
    Given version "RES-2026.12" holds no row for rule "R-RES-99"
    When the row of "R-RES-99" is read under "RES-2026.12", and a second call names no packageVersion
    Then the first answer is 404 with MSG-P3-027 for the rule row check naming "R-RES-99" and "RES-2026.12"
    Then the second answer is 422 with MSG-GEN-001 naming "packageVersion"
    Then no default row, no last row and no row of another version is answered in either case

  Scenario: AC5 The version in force is the only one named in force (new, D-RCV-60)
    Given no RESTRUCTURE version is in state IN_FORCE on 2027-01-04
    When the version list of package "RESTRUCTURE" is read for that business date
    Then no version is named IN_FORCE and the catalogue answer of any label carries inForce false
    Then the caller's embedded kit raises NoPackageInForce and the move is refused with MSG-P3-027 for the package in force check, naming "RESTRUCTURE" and 2027-01-04 only
    Then this service answers no row in place of a version in force and writes no next action

  Scenario: AC6 The latest state change of a case is answered from the ledger (new, D-RCV-60)
    Given case "RW-2026-000402" has three ledger entries and the newest carries rule "R-RES-04" of rule version "RES-2026.12" with idempotency key "DLE-SYN-0402" and decided-at 2026-12-11
    When GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000402&latestStateChange=true is called
    Then the answer is 200 with entryId, ruleId "R-RES-04", ruleVersion "RES-2026.12" and the decided-at time of that entry
    Then the answer is the newest entry in chain_seq order that carries a rule ID and a rule version, and it carries no case value, no customer value and no actor name

  Scenario: AC7 An empty ledger and a repeated record (new, D-RCV-60)
    Given case "RW-2026-000404" has no state change in the ledger
    When its latest state change is read
    Then the answer is 200 with an empty result and missing true, and no message is raised
    Given a record with idempotency key "DLE-SYN-0402" was already written for case "RW-2026-000402"
    When the same record is delivered again and the latest state change is read
    Then one entry exists for the key and both reads answer the entry written first

  Scenario: AC8 The reads write nothing and answer the same bytes twice (new, D-RCV-60)
    Given the same two calls are made twice under one version state
    When both answers are compared
    Then no rule row, version row, ledger entry, outbox row and no decision record is written by either read, and the ledger sequence is unchanged
    Then the second answer equals the first, and a promotion or a rollback of the package drops the cached row so the next read sees the new state
    Then a read that cannot be served answers 503 with MSG-GEN-006 and writes nothing

  Scenario: AC9 A caller without the read letter is refused (new, D-RCV-60)
    Given test user "U-REF-01" holds RW-REFADM and no Rules and parameters R
    When they call the catalogue read for R-RES-04 and the latest state change of case "RW-2026-000402"
    Then each answer is 403 with MSG-P4-002 and no action text, no owner role, no version label and no entry ID
    Then no row of rwb_decision is read for either call

  Scenario: AC10 The row is the only source, and no case value crosses (new, D-RCV-60)
    Given a row of "RES-2026.12" is read
    When the answer is inspected
    Then it holds the row, the outputs, the package version and its state, and no case ID, no customer value, no approver and no role name
    Then no workbook, no generated DRL, no `recovery.*` table and no other service's schema is read on the path
```

AC1 to AC10 are the criteria this story owns. The legacy criteria stay with the primary slices: the case fields, the task and the check step with RWB-P3-E2035-APP at AC2, AC6, AC8, AC10 and AC11; the resolve, the read and the fill with RWB-P2-E2035-APP at AC1, AC3 to AC7 and AC9 to AC14; the refusal of a role without Case record R with RWB-P4-E2035-APP at AC13. What this story proves is that the two answers exist, name their versions and cannot be edited from outside.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The row of a firing rule is read only through `RuleCatalog.row(ruleId, packageVersion)`, and it returns action_text, owner_role, timer_spec, to_state, rule_version, drools_rule_name and outputs | Legacy BR1 and section 12; D-RCV-36 T6 |
| BR2 | The answer is keyed by the rule ID and the package version label the caller names; a version label is never resolved to another version and a row is never rewritten | Legacy AC2 and section 12; D-RCV-36 T5, T7 |
| BR3 | The timer spec is answered as stored. The service computes no due date, no working-day count and no calendar, and holds no duration for a named state | Legacy BR3 and BR4 on the caller's side; legacy section 17 |
| BR4 | The next action is never entered by a person: no operation of this story writes a row of the registry or of the ledger | Legacy BR2; RWB-P3-E2035-APP |
| BR5 | The latest state change of a case is the newest ledger entry of that case, in `chain_seq` order, that carries a rule ID and a rule version; it answers the rule ID, the rule version, the entry ID and the decided-at time | Legacy AC11 flow step 7 and legacy section 12 `DecisionLogQuery.latestStateChange` |
| BR6 | A case with no such entry is answered 200 with an empty result and missing true; it is not an error and it creates no task, because the task is the fill's | Legacy AC8; RWB-P2-E2035-APP |
| BR7 | A missing or malformed parameter is refused before a row is read: 422 with MSG-GEN-001 for a field, 404 with MSG-P3-027 for an unknown row or version, 403 with MSG-P4-002 for a missing right | RWB-P2-E2035-CON X3 and X4; RWB-P7-E1073-APP |
| BR8 | A version is in force only while its state is IN_FORCE, which the 00:01 promotion sets and the rollback withdraws; no version in force is a fact of the registry, and `NoPackageInForce` is raised by the caller's kit | Legacy AC14; D-RCV-36 T3, T9; RWB-P7-E1073-APP |
| BR9 | Both reads are side-effect free and idempotent for their inputs: no row, no entry and no decision record is written, and the answer for a version state is the same whatever the business date | NFR-033, NFR-034; RWB-P7-E1008-APP |
| BR10 | A row is read only from `rwb_decision`; the workbook, the generated DRL, the `recovery.*` tables, `recovery_case` and the other services' schemas are never read and never joined | DP-01; ownership map |
| BR11 | No business value is written in code: action text, owner role, timer spec, to-state, version labels, version states and package codes are rows and list values | BR-P7-001, BR-P7-003 and BR-P7-007; DP-06, DP-07 |

How the rules hold in `rwb-decision`:

- BR1 to BR3 are one indexed read of `rule_row` by `rule_id` and `rule_version` plus one read of `rule_package_version` by `version_label`; the answer is a projection of those rows and holds no arithmetic.
- BR4 and BR9 are visible in the code review and in the fake run: the module has no write method on either repository and no outbox writer.
- BR5 is one ordered read of `decision_log_entry` by `case_id` with `chain_seq` descending; the filter is over the entries that carry DF-DEC-004 and DF-DEC-005, and the index of section 13 serves it. Which entries count as a state change is not enumerated in any source (GAP-2407; ASM-4006).
- BR6 is the empty answer: `missing` is a field of the answer, not an error code.
- BR7 is the envelope of the service's reads: 401 without a session, 403 without the right, 404 for an unknown row, 422 for a parameter and 503 when the store cannot be read.
- BR8 is a state read, not a date computation: the promotion story sets IN_FORCE at 00:01 on the valid-from date and the rollback withdraws it, so this story never compares a date to decide what is in force.
- BR10 is the reason there is no case repository and no ACE view grant of this service.

### 9. State transitions

None. This story changes no case status, no next-action field, no rule row and no ledger entry, and it starts no task. The registry states it reads are set by RWB-P7-E1073-APP; the only state this story has is the state of an answer:

| Answer state | When | What the caller gets |
|---|---|---|
| Row answered | The version label exists and holds the rule ID | The row, the outputs, the package version, the version state and the in-force flag |
| Row not found | The version holds no row for the rule ID, or the version is unknown | 404 with MSG-P3-027; no substitute row |
| Not in force | No version of the package is IN_FORCE | `inForce` false on every answer; the kit raises `NoPackageInForce` |
| Latest change answered | The case has a ledger entry with a rule ID and a rule version | Rule ID, rule version, entry ID and decided-at |
| No change | The case has no such entry | 200, empty result, `missing` true |
| Refused | No session, no read letter or a malformed parameter | 401, 403 or 422, and nothing is read |
| Not served | The registry or the ledger cannot be read | 503 with MSG-GEN-006 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-RULES, the embedded rules kit in the owning service | Reads the row of a fired rule and the version state under its service identity (Rules and parameters R) |
| SY-CASEWF, the case workflow's `EvaluateRules` activity | Reads the row of a fired rule for the facts of a case; it holds the case, not this service |
| rwb-integration, the resolve and the fill | Reads the row and the latest state change of a case under its service identity (Rules and parameters R, Decision log R) |
| RW-COE, center of excellence analyst | Owns the action text, the owner role and the timer spec of the rows and reads them here; the writes are RWB-P7-E1073-APP's |
| RW-AUDIT, internal audit | Reads a row, its version state and the latest state change of any case in scope (Rules and parameters R, Decision log R) |
| RW-PLATADM, platform administrator | Operates the promotion and rollback of RWB-P7-E1073-APP; this story reads only the state those set |
| Any other role | Refused 403 with MSG-P4-002 where it holds no letter; no row is read |

Reading is the whole of this story. It holds no write operation, no approval and no break-glass path, and it delegates every write of a rule row, a version or an entry to the stories named above.

### 11. Data

| BR Field ID | Table in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-REF-002, DF-REF-003 | `rule_row` | rule_id, rule_version | Read (the lookup key) |
| DF-REF-008, DF-REF-009, DF-REF-010, DF-REF-011 | `rule_row` | action_text, to_state, owner_role, timer_spec | Read |
| DF-REF-296, DF-REF-297, DF-REF-298 | `rule_row` | package_version_id, drools_rule_name, outputs | Read |
| DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054 | `rule_row` | the row order, condition and output columns of a rule | Not read: the answer holds the named fields only |
| DF-REF-274 to DF-REF-278 | `rule_package` | package_code, title, owner_role, hit_policy | Read |
| DF-REF-279 to DF-REF-294 | `rule_package_version` | version_label, state, valid_from, valid_to, checksum, author, approver | Read |
| DF-DEC-001 to DF-DEC-031 | `decision_log_entry` | case_id, decision_code, rule_id, rule_version, decided_at, chain_seq, idempotency_key | Read |
| DF-REF-185 to DF-REF-197, DF-REF-299 | `rule_test_case` | the scenario rows of a version | Not read |
| DF-DEC-032 to DF-DEC-053 | `approval` | the approval items | Not read |
| DF-CAS-049 to DF-CAS-053 | `recovery_case` (P3) | next_action_text, owner_role, due_date, rule_id, waiting | Never read: the values arrive in the caller's request |
| DF-REF-036, DF-REF-037 | `role` (P4) | role_name, role_class | Never read: read through RWB-P4-E1037-CON |
| (library) | outbox, inbox and idempotency tables | — | Not used: no write path in this story |

Field IDs are those in the Logical Data Model and Data Dictionary. The row is answered from `rwb_decision` only; the workbook, the generated DRL, `recovery.*` and the case tables are not read (BR10). Which of the row's remaining columns an answer may carry is Not specified in the source documents (GAP-2405; ASM-4004).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Status | What this story decides behind it |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | New in this story; the shape is published in `RWB-P3-E2042-CON` and consumed in `RWB-P2-E2035-CON` | The row of one rule in one package version: actionText, ownerRole, timerSpec, toState, ruleId, ruleVersion, droolsRuleName, outputs, packageCode, packageVersion, versionState, inForce. 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P3-027, 422 MSG-GEN-001, 503 MSG-GEN-006 |
| GET | `/api/recovery/decision/v1/decision-log?caseId=&latestStateChange=true` | Existing operation `API-P7-006`; the `latestStateChange` filter is new in this story | The latest state change of one case: entryId, ruleId, ruleVersion, decidedAt, missing. Same errors; 200 with `missing` true when the case has none |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | Existing, from RWB-P7-E1073-APP | Read unchanged; this story asserts in AC5 that the version list names no IN_FORCE row when none is in force |

`GET /decision-log/{entryId}`, `GET /admin/rule-packages`, `GET /admin/rule-versions` and the approval operations are the same service's and are unchanged by this story.

#### 12.2 REST operations consumed

None at run time. The two shapes this story provides are the ones `RWB-P2-E2035-CON` and `RWB-P3-E2042-CON` declare, and both are used as fakes in the tests (12.8) and as the alignment reference in the build. The case facts a read needs are parameters of the call, never a call back to the case service.

#### 12.3 Events published

None. A read is a read: no event, no `RulePackageInForce` and no decision record leaves this story. The service topic `rwb.decision.events.v1`, its retry topic and its `.dlt` carry the registry and approval events of RWB-P7-E1073-APP, and the shared topic `rwb.decision-record.v1` carries the records the callers write.

#### 12.4 Events consumed

None. The cache of section 13 is keyed by package version, and the promotion and the rollback that change a version's state are written and published by this same service, so the cache is dropped on the commit that publishes `rwb.decision.RulePackageInForce.v1` rather than on a subscription.

#### 12.5 Workflows and activities

None. This story registers no workflow and no activity on the `rwb-decision` queue. The `EvaluateRules` activity that asks for a row runs on the case service's queue, and the fill runs on `rwb-integration`; both call the REST operations of 12.1.

#### 12.6 Schedules

None. The JOB-20 rule-promote Schedule at 00:01 is RWB-P7-E1073-APP's, and the JOB-05 next-action check is RWB-P2-E2035-APP's. This story starts no Schedule and holds no timer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `rule_row` | P7 (`rwb_decision`) | The row of the fired rule, by rule ID and rule version |
| `rule_package` | P7 (`rwb_decision`) | The package code, title, owner role and hit policy |
| `rule_package_version` | P7 (`rwb_decision`) | The version label, state, valid-from and valid-to of the answer |
| `decision_log_entry` | P7 (`rwb_decision`) | The latest state change of a case, in `chain_seq` order |
| `rule_test_case`, `approval` | P7 (`rwb_decision`) | Not read in this story |
| `recovery_case`, `queue`, `task` | P3 (`rwb_case`) | Never read; the case ID is a parameter (BR10) |
| `role`, `permission`, `masking_rule` | P4 (`rwb_access`) | Never read; the right is answered by RWB-P4-E1037-CON |
| `lov_value`, `reference_row`, `parameter_catalog` | P3 (`rwb_case`) | Never read; the lists and the business date arrive through DP-06 and DP-07 |

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rule-catalog WireMock | `RWB-P3-E2042-CON` / `RWB-P2-E2035-CON` | R-RES-04, R-SET-13, R-RES-03 with timer "None", R-DEV-05 with timer "deadline driven" and R-RES-07 with timer "same day", all of "RES-2026.12"; one 404 for R-RES-99; one SUPERSEDED answer for "RES-2026.12" after "RES-2027.01" is in force |
| decision-log WireMock | `RWB-P2-E2035-CON` | The latest state change R-RES-04 of "RES-2026.12" with entry DLE-SYN-0402; an empty answer with `missing` true; a 503 beyond the 2 s budget |
| registry fixtures | `RWB-P7-E1073-APP` | Package RESTRUCTURE with "RES-2026.12" IN_FORCE from 2026-12-01, "RES-2026.12" SUPERSEDED and "RES-2027.01" IN_FORCE on 2027-01-04, and the 2027-01-04 fixture with no version in force |
| access fake | `RWB-P4-E1037-CON` | Rules and parameters R for RW-COE, RW-AUDIT and the service identities; 403 with MSG-P4-002 for RW-REFADM |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1 new operation and 1 new filter on an existing operation; consumed 0 | Base `/api/recovery/decision/v1`, one hop, 2 s budget, cached by package version |
| Kafka | None | No event published or consumed; the state change arrives through the writes of RWB-P7-E1008-APP |
| Temporal | None | No workflow, no activity and no Schedule on this service |
| File | None | No file reached; the workbook is RWB-P7-E1073-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `decision/catalogue`, Java package `th.co.scb.ace.workbench.recovery.decision.catalogue`.

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

DP-01 is the reason the answer is built from `rwb_decision` rows and holds no case value. DP-03 is recorded because the entry the fill reads is a decision record written by the owning service on `rwb.decision-record.v1` and stored here; this slice reads the store and writes no record. DP-04 is the split of the legacy rule component: the registry and the catalogue are this service's, the KieBase and the 300 ms evaluation stay in the owning service, and the row is fetched over the contract instead of the classpath. DP-05 is recorded and used for nothing on this path: no ACE view is granted to `rwb_decision`. DP-06 and DP-07 supply the business date, the version-state list and the DF-SYS field names as data, because the legacy key reads a configuration key and a holiday list and this story must not turn either into a constant. DP-10 is recorded because the legacy key carries JOB-05: in the target that check is the `rwb-integration` Schedule and the promotion is the JOB-20 Schedule, so this story adds no job. DP-11 is the boundary: two reads, one hop, 2 s, cached. DP-13, DP-14 and DP-15 are the naming and migration conventions. DP-19 is the route the case screens read through; this story serves no screen.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleCatalogController | Controller | The catalogue operation; validation and the problem envelope of BR7 |
| RuleCatalogService | Service | Builds the answer of BR1 to BR3 from the row and the version row; no arithmetic |
| VersionStateResolver | Service | The package code, the version label, the version state and the in-force flag; 404 for an unknown label |
| DecisionLogQueryController | Controller | The decision-log read with the `latestStateChange` filter |
| LatestStateChangeService | Service | BR5: the newest entry of a case that carries a rule ID and a rule version, or the empty answer of BR6 |
| RuleRowRepository | Repository | `rule_row`, `rule_package` and `rule_package_version` in `rwb_decision`; read methods only |
| DecisionEntryRepository | Repository | `decision_log_entry` by case in `chain_seq` order; read methods only |
| CatalogCache | Service | The answer per package version, dropped on the commit that promotes or rolls back a version (BR9) |

**Database and migrations.** No new table: the four tables exist from RWB-P7-E1001-APP and RWB-P7-E1008-APP, and the catalogue index of `rule_row (rule_id, rule_version)` is created with them. One migration in the per-service Flyway sequence of DP-15, `V2_035_1__latest_state_change_index.sql`, adds `ix_declog_case_latest` on `decision_log_entry (case_id, chain_seq DESC) WHERE case_id IS NOT NULL`, so the latest state change is an index read inside the 2 s budget of DP-11. The story writes no row of either table.

**Configuration and reference data.** The version-state list and the business date are read through DP-07 and DP-06. The timer specs, the action texts, the owner roles and the version labels are rows of the package versions. No parameter, no timeout constant, no rule ID and no role code appears in code (BR11). The database login is the rwb-decision login (DP-02): Not specified in the source documents (GAP-2411; ASM-4010).

**Build steps**

1. `RuleRowRepository` and `VersionStateResolver` over the three registry tables, with the 404 of X2 and X3; tests for AC1, AC2 and AC4.
2. `RuleCatalogService` with the projection of BR1 to BR3, and a test that a timer spec is returned byte for byte for the five shapes of AC3.
3. `DecisionEntryRepository` and `LatestStateChangeService` with the ordered read and the empty answer; tests for AC6 and AC7.
4. `CatalogCache` keyed by package version and dropped on the promotion and the rollback commits; test AC8, including the 503 path.
5. The access check on both operations and the refusal of AC9 through the RWB-P4-E1037-CON fake.
6. The migration of the index, and a timing test that both reads stay inside the 2 s budget on a package of 38 rows and a case of 400 entries.
7. The fake run of both operations against the RWB-P2-E2035-CON and RWB-P3-E2042-CON fakes, so the story builds before the registry is loaded in the environment.

**Feature switch.** None. A switch here would let a next action be resolved from a row the registry cannot name for that version, which is the failure this story exists to prevent; the states of a version are data and the promotion is the only way a version becomes servable.

**Done when.** The tests of section 16 pass; the row of a fired rule is answered for the version the caller names whatever its state; a timer spec is returned as stored; an unknown row is refused without a substitute; a package with no version in force is named in force nowhere; the latest state change of a case is answered from the ledger or answered empty; and neither read writes a row, an entry or a decision record.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | No valid session or service identity | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answers |
| MSG-P4-002 | The caller holds no Rules and parameters R, or no Decision log R, on the operation asked | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR7 |
| MSG-P3-027 | The rule row, the package code or the version label is not found, or no version is in force | The rule version was refused at the {check} check: {detail}. | This story, for the rule row, the version and the package in force checks |
| MSG-GEN-001 | A parameter is missing or malformed | Enter {field}. | This story, before a row is read (X1) |
| MSG-GEN-006 | The registry or the ledger cannot be read | {system} is not available. Try again in a few minutes. | This story, on X8 and on a read beyond the budget |

For MSG-P3-027 the {check} values of this story are "rule row", "version" and "package in force"; {detail} names the rule ID, the package code, the version label and the business date only, never a case fact, a customer value or an actor. Every error is a problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10.

### 15. Screens and states

This story builds no screen. SCR-03 Case record, SCR-02 Case list, SCR-09 Exception queue and SCR-38 Decision log query are P3's and P4's through the gateway-bff composite route of DP-19, and the next-action panel and columns are RWB-P3-E2035-APP's.

What this story decides for those screens is what the two answers may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record | Read only | The next action names the rule ID and its version, and both come from the row and the entry answered here |
| SCR-03 Case record | Waiting | The owner role of the row is the code the caller turns into the waiting text with the role name of RWB-P4-E1037-CON |
| SCR-03 Case record | Overdue | The overdue marker is the case side's; the version shown is the one the answer names, so an escalation can cite it |
| SCR-02 Case list | Columns shown | The rule ID and version behind each row are the ones this story answers for that case |
| SCR-38 Decision log query | Entry opened | The latest state change read here is the same entry the query returns; no second ordering exists |

A screen that shows a next action with no rule ID and no version, or with a version the registry does not hold, is a defect of the screen: both answers always name what they answered for.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, AC2, BR1, BR2 | Component | R-RES-04 of "RES-2026.12": action text, owner role RW-RESTRUCT, timer "2 working days", to-state WITH_FCR_OFFICER |
| TC-E2-035-02 | AC1, AC3, BR1, BR7 | Contract | The catalogue request of a fired rule with rule ID and package version, and a 422 for a missing packageVersion |
| TC-E2-035-03 | AC1, AC10, BR1 | Component | R-SET-13 with owner role CU-BORROW and timer "payment due 30 days"; the answer carries the code, not the role name |
| TC-E2-035-04 | AC1, AC3, BR1 | Component | The two rows of the SCR-02 columns, R-RES-04 and R-SET-13, read under one version |
| TC-E2-035-05 | AC3, BR3 | Component | R-RES-03 with timer "None" and owner role RW-CASEOWN; no substitution by the caller's table |
| TC-E2-035-06 | AC3, AC4, BR3 | Component | R-DEV-05 with timer "deadline driven"; R-RES-99 with no row; no default row answered |
| TC-E2-035-07 | AC3, BR3 | Component | R-RES-04 read on 30 December 2026 with two bank holidays; the spec is answered as stored and no holiday is applied |
| TC-E2-035-08 | AC2, AC8, BR2, BR9 | Component | Closed case "RW-2026-000404"; the row of its version is unchanged and the read writes nothing |
| TC-E2-035-09 | AC7, BR5, BR6 | Component | Idempotency key DLE-SYN-0402 delivered twice; one entry and the same answer |
| TC-E2-035-10 | AC6, AC7, BR5 | Component | Three entries on case "RW-2026-000402"; the newest in `chain_seq` order is answered |
| TC-E2-035-11 | AC6, BR5 | Component | Three cases with no next action before the JOB-05 fill, each answered from its latest state change |
| TC-E2-035-12 | AC3, BR3 | Component | R-RES-07 with timer "same day"; the spec is answered as stored and no date is computed |
| TC-E2-035-13 | AC9, BR7 | Component | RW-REFADM "U-REF-01" reads both operations; 403 with MSG-P4-002 and no row read |
| TC-E2-035-14 | AC5, BR8 | Contract | No RESTRUCTURE version in force on 2027-01-04; no IN_FORCE row, inForce false, and NoPackageInForce with MSG-P3-027 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component where the case side is stubbed and to Contract where the shape of a read is proved; the legacy Access level of TC-E2-035-13 maps to Component. Every legacy test case of the key is listed above with its Covers column rewritten to the criteria this story owns; each one is proved at its own legacy assertions in RWB-P2-E2035-APP or RWB-P3-E2035-APP and at the registry assertions here. No `-ITG` copy sits in this story: the integration copy of the key is RWB-ITG-E2035-ITG.

### 17. Guardrails

- No business value in code: action text, owner role, timer spec, to-state, package codes, version labels, version states and role codes are rows and list values (BR11).
- No personal data in a log, an answer, an event or a test: the two answers carry rule identifiers, version labels, dates and entry IDs, and test data is synthetic with parties as role codes.
- ACE data only through the owner's contract or `v_ace_*` views (DP-05): this service holds no customer value, is granted no ACE view and answers no case value.
- No cross-schema read (DP-01, BR10): `recovery_case`, `queue`, `task`, `role`, `lov_value` and `recovery.*` are never queried; the case ID is a parameter.
- One writer per row: this story holds no write method on either repository, so a rule row, a version and a ledger entry change only through RWB-P7-E1073-APP and RWB-P7-E1008-APP.
- The row is read only through `RuleCatalog.row`; the workbook, the generated DRL and the `rule_row` table of a retired schema appear in no code path (legacy section 17).
- One evaluation: the kit evaluates in the owning service and this service answers facts, so no second rule engine decides a to-state.
- A read is idempotent and side-effect free: the same question under the same version state answers the same bytes and writes nothing (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-02, TC-E2-035-05, TC-E2-035-06, TC-E2-035-12 |
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-03, TC-E2-035-08, TC-E2-035-14 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-09, TC-E2-035-10, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-02, TC-E2-035-04 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-04 | TC-E2-035-10, TC-E2-035-11 |

| Legacy reference | Where it is kept |
|---|---|
| `RuleCatalog.row(ruleId, packageVersion)` returning action_text, owner_role and timer_spec (legacy BR1, section 12) | Sections 1, 4, 8, 12.1 |
| BR2 no entry by a person, BR3 timer arithmetic, BR4 the state's service level | Sections 7, 8, 11, 17 |
| BR10 a later version does not rewrite an action, BR11 no version in force is a refusal | Sections 7, 8, 9, 12.1 |
| `DecisionLogQuery.latestStateChange` returning ruleId and ruleVersion (legacy section 12 and AC11) | Sections 1, 4, 8, 12.1 |
| Legacy AC9, AC10 and AC11 on the repeated record and the old case | Sections 5, 7, 16 |
| MSG-P4-001, MSG-P4-002, MSG-P3-027, MSG-GEN-001, MSG-GEN-006 | Section 14, exception paths |
| Legacy key RWB-E2-035, story RWB-P7-E2035-APP, contracts RWB-P2-E2035-CON and RWB-P3-E2042-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The primary slices: RWB-P2-E2035-CON and RWB-P2-E2035-APP for the resolve, the read and the fill; RWB-P3-E2035-APP for the five case fields, the `NEXT_ACTION_MISSING` task and its cancel, the JOB-05 check and the case list and export columns; RWB-P4-E2035-APP for the role name, the role class and the access answer.
- The registry itself: the load, the six checks, the two Epic 2 checks, the 50-scenario gate, the dry run, the four-eyes approval, the JOB-20 promotion and the rollback (RWB-P7-E1073-APP, RWB-P7-E2042-APP).
- The ledger store, its append-only trigger, its hash chain, its verification and the decision-record ingest (RWB-P7-E1008-APP, RWB-P7-E1027-APP, RWB-P7-E1027-CON).
- The audit query of the decision log across a population of cases, the export and the approval items (RWB-P7-E2005-APP, RWB-P7-E2013-APP).
- The timer arithmetic, the service levels and timers rows, the holiday calendar and the waiting text (RWB-P3-E2035-APP, RWB-P4-E2035-APP, DL22).
- The escalation of an overdue next action (RWB-E2-015) and the next action column in the queue view screens (RWB-E2-011).
- The gateway route, the screens and their states (RWB-PLT-N001-CON, RWB-P3-E1023-APP).
- The Helm chart, the Kafka subscriptions, the metrics, the alerts and the runbook of this capability (the OPS story of this key), and RWB-ITG-E2035-ITG, the wave-2 harness that proves the real cross-service behaviour.
