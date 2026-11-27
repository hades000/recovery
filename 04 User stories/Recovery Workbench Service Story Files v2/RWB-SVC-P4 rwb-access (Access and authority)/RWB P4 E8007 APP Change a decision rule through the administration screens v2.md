# RWB-P4-E8007-APP Change a decision rule through the administration screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BA |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P4-E8007-APP-16) |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E8007-APP-23) |
| Depends on (build) | RWB-P4-E8007-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-007 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **RW-COE (center of excellence analyst), and the access service that keeps the change record**, I want **one rule change taken on the administration screen as a dated request that binds a registry version, its test evidence and the role that must approve it into a single record that the screen and the audit can read**, so that **a rule changes as data with no code release, the version, its test result and its dry-run counts are stated the moment the change is raised, and the governance of the version itself stays in the one service that owns the registry instead of being copied into the administration service**.

Inside `rwb-access` this is the change-request slice of the legacy story RWB-E8-007:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Service facts of this slice: no event of its own is published, no workflow is started, no rule table is held, and no screen of its own is served — SCR-39 Rules and parameters arrives through the gateway-bff composite route of DP-19.
- Two deliverables, and nothing else: the write `POST /api/recovery/access/v1/admin/rule-changes`, which takes `packageCode`, `versionId`, `validFrom`, `reason` and the seven-item change checklist, reads the version and its evidence from the rule registry, records the change and answers it in state `REQUESTED`; and the read `GET /api/recovery/access/v1/admin/rule-changes/{changeId}`, which answers the change with the state the registry reports for its version.
- The rule registry is `rwb-decision`'s (P7): `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's under ASM-0069, and the rule-package paths are P7's under ASM-0040. This story reads no rule table and holds no copy of a version; the version, its label, its state, its checksum, its test result and its dry-run counts arrive through the registry's contract.
- The load gate of a version is `RWB-P4-AD011-APP` and the approval of a version is `RWB-P4-AD012-APP`. This story duplicates neither, is not a build dependency of either, and adds no path and no field to them.
- The change request is a record of this service and not a table of this service: it is one entry of the local decision-record chain of the library of DP-03, written in the same transaction as the idempotency row, hash-linked to the entry before it and published as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`. The central ledger `decision_log_entry` stays in `rwb-decision` and is never read or written here (ASM-1571).
- A load is not a decision and records nothing — that is the rule of RWB-P4-AD011-APP. A change request is a decision: the analyst decides that this version, on this evidence, is the one Risk is asked to approve from this date, and the audit must be able to read that decision in the service that made it. That difference is why this story records and the load story does not.
- Only a version the registry reports in state `LOADED` can be raised as a change. The version states are the registry's, and the set of TSD P4 v3 T4 is LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED with VALIDATED; this story observes them and writes none of them.
- The approval `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` and the promotion at 00:01 (JOB-20 with `RulePackageInForce` EV-30 on `rwb.decision.events.v1`) are P7's and are out of scope. The four-eyes rule is P7's too: RW-COE authors and RW-RISK approves, and the registry refuses an approval by the author with MSG-P7-002 (TSD P4 v3 T6.1 and T6.3).
- The metadata contract-dependency list of this story carries no P7 rule-package contract, so the two registry reads are built against that contract and its fake and the missing C dependency is raised at D1 — Not specified in the source documents (GAP-0868; ASM-1571).
- The record code an administrative change is written under, and the field-level shape of the change request inside an entry of the chain, are Not specified in the source documents (GAP-0868; ASM-1573).

### 2. Business rationale

The business owns the rule and IT owns the engine, and the FSD states the target in one measure: rule and limit changes made without a code release, 100 percent, read from the decision record and the Workbench records every month (FSD P4 v3 A2.18.1). Today the problem the FSD names is that "access, limits and rules live in documents and people's heads; changes need code or manual checks" (FSD P4 v3 A2.18.1), and the legacy key carries the whole journey — change, test, put in force — as one administration screen against the monolith's own rule rows (RWB-E8-007; FEAT-ADM-02).

In the target the governance of a rule moves out of the administration module: authoring, the compile to a decision model, the checks, the scenario run, the four-eyes approval, the effective dating and the version audit are central in `rwb-decision` (Architecture v5 slide 27; Temporal and Drools design slide 15: "governance is central in rwb-decision; evaluation is local in the one service that owns each model"). What is left for the administration service is the act the analyst takes in front of the screen, and the record that the act happened. That is this story: the change request that binds a version, the evidence the registry already holds for it, the date it should take effect and the role that must approve it, into one record with one identifier that the screen, the audit and the change report can all point at.

The record matters more than it looks. The registry can say a version exists and who approved it, but it cannot say which version an analyst asked Risk to approve, on what date, for what reason, with which checklist, and under which policy versions — that is an administrative decision, and it is the decision the metric counts. R-UNI-38 says no change takes effect without a version stamp, and R-UNI-39 says no action proceeds unlogged; this story carries the second half for the change request in the service that owns the administration surface. Where the record cannot be written the request is not taken, and the analyst sees MSG-P7-003 (legacy RWB-E8-007 AC2).

The story meets REQ-CWC-013 (a rule change goes from a validated load to production with a version stamp and no code release, and rolls back by one call), REQ-CWC-014 (a load is validated for schema, overlapping rows, unreachable rows, a missing default row and a set of test cases before it takes effect), REQ-DRI-010 (every threshold, limit and name lives in a versioned catalog and changes without a code release) and REQ-ACA-013 (the full administration screens for roles, permissions and delegation are available to the security administrator). It contributes the change-checklist and evidence half of REQ-CWC-014 at the point where the change is raised, and it leaves the compile, the overlap check, the scenario run and the approval to the registry, which enforces them again on its side.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8007-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two operations, the `RuleChange` and `RuleChangeChecklist` schemas, the version state set of TSD P4 v3 T4, the error envelope, the consumed declarations and the contract fakes. This story implements that document and adds no path and no field |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a change, hash-linked, in the transaction that writes the idempotency row |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the parameters version in force, read and carried on the change. A C dependency, so it never blocks the build |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): SCR-39 Rules and parameters reaches the two operations through it, one hop each |
| The `rwb-decision` rule-package contract | The two reads this story consumes and their fake: the versions of a package with their state, label, checksum, test result and dry-run counts, and the dry-run result of a version. It is not in this story's metadata contract-dependency list (GAP-0868; ASM-1571) |
| RWB-P4-AD011-APP, RWB-P4-AD012-APP | The load gate of a version and the approval of a version, both already owned. Neither is a build dependency of this story, and this story neither repeats nor extends them |

Business preconditions carried from RWB-E8-007 and from the rule design:

- The rights in force are those of TSD P4 v3 T6.1: RW-COE holds `CRUD` in Rules and parameters and `R` in Platform administration, RW-RISK holds `RA` in Rules and parameters, RW-AUDIT holds `R` in both, and RW-CASEOWN holds `R` in Rules and parameters. Raising a change needs C; the approval needs A and is the registry's (BR4).
- The author of a version is RW-COE and the approver is RW-RISK, and the author cannot approve (Temporal and Drools design slide 15; TSD P4 v3 T6.3, MSG-P7-002).
- The change checklist has seven items — request, impact, test result, approver, load, verify and rollback plan — and a version cannot be approved while an item is missing (TSD P4 v3 T6.3; DF-REF-295; MSG-P3-022).
- The version states are the values of LOV-VERSION-STATUS: LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (TSD P4 v3 T3.2 and T4). This story accepts only `LOADED`.
- A version in force keeps deciding until the registry promotes its successor at 00:01, and a promoted version records its label on every decision it makes (Temporal and Drools design slide 15; TSD P4 v3 T6.3 decision-log linkage).
- The change checklist item codes and the version states are fixed by the technical specification and by the contract; the pattern list of this story holds no DP07 and its contract-dependency list holds no `RWB-P3-E1043-CON`, so this story adds no reference-data read and treats both lists as contract constants (ASM-1572).
- The staff reference of the author resolves through the session, and no name and no e-mail address is read, held or returned by this story (NFR-040).

### 4. Flow

1. The center of excellence analyst opens SCR-39 Rules and parameters, panel rule versions, through the gateway-bff composite route (DP-19). The route reads the versions of the package from the registry and shows them with their state, their label, their test result and their dry-run counts.
2. The analyst selects a version in state `LOADED` and raises a change: the route calls `POST /api/recovery/access/v1/admin/rule-changes` on `rwb-access` with the body `packageCode`, `versionId`, `validFrom`, `reason` and `checklist`, the seven items of the change checklist, and the `Idempotency-Key` of the submission.
3. `RuleChangeController` validates the body: `packageCode`, `versionId`, `validFrom` and `reason` are required and an empty one is 422 with MSG-GEN-001 naming the field; `validFrom` that is not a date is 422 with MSG-GEN-001; a body larger than the request limit of the contract is refused before it is read.
4. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters C. A caller without the letter is refused with 403 and MSG-P4-002, and nothing is written: no ticket, no entry (BR4, AC3).
5. `ChecklistGate` checks the seven items of the checklist in the order of TSD P4 v3 T6.3 — request, impact, test result, approver, load, verify, rollback plan. A missing or empty item refuses the request with 422 and MSG-P3-022 whose `detail` and `missingItem` name the item code, and the gate runs before any registry call, so an incomplete checklist costs no hop and leaves no entry (BR3, AC3).
6. `ParameterReader` reads the parameters version in force through the parameters contract of DP-06 on the date of the request. The version label is carried on the change so a change states the parameter set it was raised under; no bound and no threshold is read, because this story holds none (BR11).
7. `RulePackageClient` reads the version through `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` of `rwb-decision`, filtered to the `versionId` of the body: its state, its version label, its checksum, its valid-from date, its test result and its dry-run counts, one hop with a 2 s timeout.
8. A version the registry reports in any state other than `LOADED` is refused with 409 and MSG-GEN-004, the state is named in the answer, and nothing is recorded: an approved, in-force, superseded, rolled-back or refused version is not a version a change can be raised against (BR2, AC4).
9. `RulePackageClient` then reads the evidence through `GET /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run` of `rwb-decision`: the dry-run result of the version against the open cases it would decide, with its counts and its overall test result.
10. `RuleChangeService` mints the `changeId`, fixes the approver role as `RW-RISK`, and computes `canApprove`: true only where the caller holds Rules and parameters A and is not the author reference recorded on the version. For the author of the version the answer is `canApprove` false, so the screen offers no approve action to the author (BR5, AC5).
11. `ChangeRecordAppender` appends exactly one entry to the local decision-record chain of DP-03 in the same transaction as the idempotency row: the change id, the package code, the version id and label, the test result, the dry-run counts, the valid-from date, the reason, the checklist, the author reference, the approver role and the parameters version. The entry is written under the administrative-change record code of the library and is hash-linked to the entry before it (BR1, BR9; ASM-1573).
12. The answer is 201 with `changeId`, `packageCode`, `versionId`, `versionLabel`, `versionState` as the registry reported it, `testResult`, `dryRunCounts`, `validFrom`, `reason`, `checklist`, `state` `REQUESTED`, `approverRole` `RW-RISK`, `canApprove`, `authorReference`, `parameterVersion` and `recordedAt`, and the `Location` of the read (BR6).
13. Where the entry or its idempotency row cannot be written, the change is not taken: the call fails with 503 and MSG-P7-003, and no change id is returned, because an administrative decision that is not in the record cannot be defended later (legacy RWB-E8-007 AC2; R-UNI-39).
14. The same `Idempotency-Key` replayed answers the first answer and writes no second entry and no second change id (BR10, AC5).
15. `GET /api/recovery/access/v1/admin/rule-changes/{changeId}` reads the entry of the change from the local chain and reads the state of its version through the registry. It answers the same document with `versionState` as the registry reports it now — `LOADED`, `APPROVED` or `IN_FORCE`, and later `SUPERSEDED` or `ROLLED_BACK` — so a change raised as `REQUESTED` shows the progress of its version with no build (BR8).
16. An unknown `changeId` is 404 and names the identifier only. Where the registry cannot be reached for the read, the answer is 503 with MSG-P7-003 and the change is not shown in a state this service cannot confirm (X8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `packageCode`, `versionId`, `validFrom` or `reason` is empty, or `validFrom` is not a date | 422 naming the field, no registry call and no entry | MSG-GEN-001 | AC1 |
| X2 | The caller holds no Rules and parameters C | 403, no registry call and no entry; nothing about the version is disclosed | MSG-P4-002 | AC3 |
| X3 | The caller's session has ended | 401, no registry call and no entry | MSG-P4-001 | AC3 |
| X4 | A checklist item is missing or empty | 422 with `missingItem` naming the item code, before any registry call, and no entry | MSG-P3-022 | AC3 |
| X5 | The registry reports the version in a state other than `LOADED` | 409 naming the state, no change id and no entry | MSG-GEN-004 | AC4 |
| X6 | The registry does not answer inside 2 s, or the connection fails | 503; no change is recorded and no state is reported as confirmed; a retry with the same `Idempotency-Key` cannot create a second change | MSG-P7-003 | AC1 |
| X7 | The entry of the change, or its idempotency row, cannot be written | 503 and no change id; nothing is written at all | MSG-P7-003 | AC2 |
| X8 | The registry cannot be reached for the read | 503 and no answer; the change is never shown in a state this service cannot confirm | MSG-P7-003 | AC5 |
| X9 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; no second change id and no second entry | None | AC5 |
| X10 | The `changeId` of the read is unknown to this service | 404 naming the identifier only, and no version is read | None | AC5 |

No exception path of this story changes a version, a rule row, a case or a task: this service writes one entry of its own chain and reads the registry's answer, and the lifecycle of a version is P7's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8007-CON and its fakes; the registry is consumed through its contract and reads its own tables, and this story holds no rule table and no version state |
| Negotiable | The checklist item codes and the version states are fixed by the technical specification and the contract; the field shape of the change inside the record is settled with audit and with the registry owner |
| Valuable | One change raised, evidenced and recorded in one call, and one read that shows the progress of the version without a second integration |
| Estimable | One controller, one change service, one checklist gate, one registry client, one parameters reader, one record appender, one record reader, five fakes and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule, no event of its own and no screen of its own |
| Testable | Each owned criterion has a test case in section 16; the refusal of a state, the refusal of a checklist item and the four-eyes answer are provable against the registry fake |

### 7. Acceptance criteria

```gherkin
Feature: Change a decision rule through the administration screens

  Background:
    Given the environment is SIT
    Given the run date is 15 December 2026
    Given test user "U-7101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS"
    Given test user "U-7103" holds RW-RISK with "RA" in "RULES_AND_PARAMETERS"
    Given test user "U-7110" holds RW-CASEOWN with "R" only in "RULES_AND_PARAMETERS"
    Given the change checklist is the seven items request, impact, test result, approver, load, verify and rollback plan

  Scenario: AC1 Change a decision rule through the administration screens (legacy RWB-E8-007 AC1)
    Given the rwb-decision contract mock returns package version "ENTRY-2027.01" in state "LOADED" with test result "PASS" and the dry-run counts
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the center of excellence change a rule, test it and put it in force as a new version
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-007 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 An incomplete checklist and a role without the right are refused (new, D-RCV-60)
    Given the rwb-decision contract mock returns package version "ENTRY-2027.01" in state "LOADED"
    Given "U-7101" posts a change for packageCode "ENTRY", that versionId, validFrom 2027-01-01 and a checklist in which the item "verify" is missing
    When POST /api/recovery/access/v1/admin/rule-changes is called with Idempotency-Key "k-e8007-1"
    Then the response is 422 with message MSG-P3-022 and its missingItem names "verify"
    Then the rwb-decision contract fake records no call
    Then no changeId is returned and no decision-record entry is appended
    Then the same change with all seven items posts afterwards and is accepted, so the refusal changed nothing
    When "U-7110" holding RW-CASEOWN with "R" only posts the same change
    Then the response is 403 with message MSG-P4-002 and no change is recorded

  Scenario: AC4 A version that is not LOADED is refused and the version in force still decides (new, D-RCV-60)
    Given the rwb-decision contract mock returns package version "ENTRY-2026.11" in state "IN_FORCE"
    When "U-7101" posts a change for packageCode "ENTRY" and that versionId with all seven checklist items
    Then the response is 409 with message MSG-GEN-004 and the answer names state "IN_FORCE"
    Then no changeId is returned, no decision-record entry is appended and no change exists for that version
    Then nothing is in force differently and version "ENTRY-2026.11" still decides the cases it decided before the call

  Scenario: AC5 The change carries its evidence, and the author cannot approve (new, D-RCV-60)
    Given the rwb-decision contract mock returns package version "ENTRY-2027.01" in state "LOADED" with test result "PASS" and the dry-run counts of that version
    When "U-7101" posts the change with the complete checklist and validFrom 2027-01-01
    Then the response is 201 with changeId, packageCode "ENTRY", versionLabel "ENTRY-2027.01", versionState "LOADED", testResult "PASS", the same dryRunCounts the registry returned, validFrom 2027-01-01, state "REQUESTED" and approverRole "RW-RISK"
    Then exactly one decision-record entry is appended carrying the changeId, the version label, the test result, the dry-run counts and the author reference
    Then GET /api/recovery/access/v1/admin/rule-changes/{changeId} answers the same fields with versionState "LOADED"
    Then the answer carries canApprove false for "U-7101", who authored the version, so no approve action is offered to the author
    Then the rwb-decision contract mock records no call from rwb-access to the approve operation and none to the rollback operation
    When the registry is asked to approve the same version for its author "U-7101"
    Then the registry refuses it with MSG-P7-002 and version "ENTRY-2027.01" stays "LOADED"

  Scenario: AC6 The boundary rules hold: no registry table is read, the parameters version is carried and the record holds no person (new, D-RCV-60)
    Given the rwb-decision contract mock returns package version "ENTRY-2027.01" in state "LOADED"
    When "U-7101" posts a change for packageCode "ENTRY" and that versionId with all seven checklist items
    Then the reads and writes of this service reach only the permitted tables and no foreign key crosses a schema
    Then the parameters version is the one read through DP-06 and carried on the change, and no threshold is held
    Then the entry holds references, codes, versions, dates and times only
    Then no route for a load or an approve is found in this service

  Scenario: AC7 A call without an authenticated caller is answered 401 and an unknown change is answered 404 (new, D-RCV-60)
    When POST /api/recovery/access/v1/admin/rule-changes is called without an authenticated caller
    Then the response is 401 and no changeId is returned and no decision-record entry is appended
    When the read of a change beside that POST is called for a changeId that does not exist
    Then the response is 404 with message "Not specified in the source documents (NEWAC-RWB-P4-E8007-APP-AC7)"

  Scenario: AC8 A consumed call that fails or does not answer writes nothing (new, D-RCV-60)
    Given the rwb-decision contract mock fails or does not answer
    When "U-7101" posts a change for packageCode "ENTRY" and that versionId with all seven checklist items
    Then the response is "Not specified in the source documents (NEWAC-RWB-P4-E8007-APP-AC8)" and no changeId is returned
    Then no decision-record entry is appended and no change exists for that version
```

AC1 and AC2 are the two criteria of RWB-E8-007, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the registry mock, so the change is provable while the rule-package contract is still a fake. AC3 to AC8 are new under D-RCV-60 and test only what this story adds: the checklist gate and the right, the state gate, the evidence and four-eyes answer of the change, the boundary rules, the 401 and 404 answers, and the failed consumed call.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A rule change is one record of this service: an entry of the local decision-record chain of DP-03 that binds a registry version, its test evidence and the approving role, written in the same transaction as its idempotency row | RWB-E8-007 AC1; DP-03; ASM-1571 |
| BR2 | Only a version the registry reports in state `LOADED` can be raised as a change; every other state of TSD P4 v3 T4 is refused with 409 and MSG-GEN-004 | TSD P4 v3 T4 and T3.2; Temporal and Drools design slide 15 |
| BR3 | The change checklist of seven items — request, impact, test result, approver, load, verify and rollback plan — must be complete; a missing item is refused with 422 and MSG-P3-022 naming the item, before any registry call and before any entry | TSD P4 v3 T6.3; DF-REF-295; ASM-1572 |
| BR4 | Raising a change needs Rules and parameters C and the approval needs A; RW-COE holds CRUD, RW-RISK holds RA and RW-CASEOWN holds R only, and a caller without C is refused with 403 and MSG-P4-002 with nothing written | TSD P4 v3 T6.1; legacy RWB-E8-007 permission checks |
| BR5 | The author cannot approve: the change carries `approverRole` `RW-RISK` and `canApprove` false for the author of the version, and the approval itself is the registry's, where an approval by the author is refused with MSG-P7-002 | Temporal and Drools design slide 15; TSD P4 v3 T6.3 |
| BR6 | The change carries the version label, the test result and the dry-run counts exactly as the registry answered them; this story computes no result, runs no scenario and re-checks no checksum | TSD P4 v3 T6.3; DF-REF-285, DF-REF-292, DF-REF-293 |
| BR7 | The registry is P7's: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are never read, and no foreign key crosses a schema; the version arrives through the contract | ASM-0069; ASM-0040; DP-01 |
| BR8 | This story writes no version state: the approval and the promotion at 00:01 with `RulePackageInForce` are the registry's, and the read answers the state the registry reports at the time of the read; the change request accepts only `LOADED` (BR2) and the read observes the states that TSD P4 v3 T4 defines | TSD P4 v3 T4; Temporal and Drools design slide 15; R-UNI-38 |
| BR9 | Every change appends exactly one entry in the same transaction as the answer; where the entry cannot be written the change is not taken and the caller sees 503 with MSG-P7-003 | R-UNI-39; legacy RWB-E8-007 AC2; DP-03 |
| BR10 | One `Idempotency-Key` answers one change: a replay answers the first answer and writes no second entry and no second change id | Architecture v5 slide 11; DP-09 |
| BR11 | No business value in code: the checklist item codes and the version states are the contract constants of TSD P4 v3 T6.3 and T4, and the parameters version in force is read through DP-06 and carried on the change; this story holds no threshold and no bound | BR-P4-018; FSD P4 v3 A2.18.3.1; REQ-DRI-010 |
| BR12 | The record of a change carries references, codes, versions, dates and times only: no name, no e-mail address and no personal field | NFR-040; FSD P4 v3 A2.18.3.2 |
| BR13 | The load gate of a version and its approval are other stories': RWB-P4-AD011-APP and RWB-P4-AD012-APP, with the registry as their owner; this story adds neither a load path nor an approve path | RWB-P4-AD011-APP; TSD P4 v3 API-P4-015 to API-P4-017 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR9 are one appender: the entry and the idempotency row commit in one transaction, and a failure rolls both back, so a change id can never exist without its record.
- BR2 is one comparison against the state the registry returned in the same request, and the state is echoed in the 409 so the screen can say which state the version is in.
- BR3 is one pass over the seven item codes before the registry client is called; the gate returns the first missing item and the controller maps it to a 422 whose `missingItem` is that code.
- BR4 is the authorise call before the registry is read, so a caller without the letter cannot spend a hop and learns nothing about the version.
- BR5 is a comparison of the caller reference with the author reference the registry returned for the version, plus a read of the A letter; the story exposes no approve path at all, so the rule cannot be broken here.
- BR6 is the field set of the answer: the label, the test result and the counts are the registry's fields and are copied, never recomputed.
- BR7 is the absence of a rule repository: the service has no entity, no migration and no query for a rule table, and the fields arrive as a JSON document of the contract.
- BR8 is the pass-through of the read: `versionState` is asked of the registry on every read, so a promotion at 00:01 changes the answer with no release here.
- BR11 is checked by test: a new checklist item or a new version state is a contract change and not a data change, and the parameters version moves with the parameters contract.
- BR12 is the shape of the entry: references, codes and times only, and no field of a person.

### 9. State transitions

This story defines one state of its own and observes the registry's. The change is `REQUESTED` from the moment it is recorded, the entry is append-only and is never updated, and the live state of the version is read from the registry on every read.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A change is posted | Rules and parameters C, a complete checklist and a version in state `LOADED` | One entry appended, `state` `REQUESTED` |
| (none) | A change is posted | A checklist item is missing | No change, no entry, 422 with MSG-P3-022 |
| (none) | A change is posted | The registry reports the version in another state | No change, no entry, 409 with MSG-GEN-004 |
| `REQUESTED` | The registry approves the version | The approval is P7's and the author is not the approver | `versionState` `APPROVED` on the next read |
| `APPROVED` | The registry promotes the version at 00:01 | The valid-from date is reached | `versionState` `IN_FORCE` on the next read |
| `IN_FORCE` | A later version is promoted | None | `versionState` `SUPERSEDED` on the next read |
| `IN_FORCE` | One-call rollback in the registry | None | `versionState` `ROLLED_BACK` on the next read |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A change is recorded, refused or replayed | One entry appended with its `prev_hash` and `entry_hash`, or none at all; no entry is ever updated or deleted |
| Append-only local chain | The parameters version changes | A new change carries the new version; an old entry keeps the version it was raised under |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Center of excellence analyst (RW-COE) | Holds Rules and parameters C: raises a change on a loaded version, reads it back, and is the author whose approval the registry refuses. Primary actor (FSD P4 v3 A2.18.3.3) |
| Risk and model risk officer (RW-RISK) | Holds Rules and parameters A: reads the change, answers `canApprove` true where not the author, and approves the version in the registry, not here |
| Internal audit (RW-AUDIT) | Holds Rules and parameters R: reads the change and its `versionState`, with the test result and the dry-run counts as evidence |
| RW-CASEOWN, RW-PHONECOL, RW-TEAMMGR and the other case roles | Hold R or `-` in Rules and parameters: may read a change where R is held, and are refused a change with 403 and MSG-P4-002 |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and caches nothing across users |
| `rwb-access` itself | Reads `role` and `permission` in its own schema, its own session, and writes only entries of its own chain and its own idempotency rows |
| `rwb-decision` (P7) | Owns the version, its states, its checksum, its test result, its dry-run counts, the four-eyes approval and the promotion; this story only reads them |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002, and the unauthenticated shape is 401 with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8007-CON together with the rest of the service's contract.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-038 | `role` | id, role_code, role_class, default_scope | Read: the role and its class; DF-REF-039 is not in LDM v9 and is Not specified in the source documents (DOR-RWB-P4-E8007-APP-7) |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read: the C and A letters in `RULES_AND_PARAMETERS` |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the change entry: `decision_code` DF-DEC-003 (the administrative-change record code, ASM-1573), `case_id` DF-DEC-002 empty for an administrative change, `inputs_ref` DF-DEC-008 with the change id, the package code, the version id and label, the test result, the dry-run counts, the valid-from date, the reason, the checklist, the author reference, the approver role and the parameters version, `actions` DF-DEC-014, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the change read by identifier |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a change | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` (platform library table in `rwb_access`) | the record row of a change | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-274 to DF-REF-278 | `rule_package` of `rwb_decision` | the package code and its title | Returned through the registry's contract; not read |
| DF-REF-279 to DF-REF-295 | `rule_package_version` of `rwb_decision` | version id, label, status, checksum, valid-from, test result, dry-run counts and change checklist | Returned through the registry's contract; not read |
| DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054, DF-REF-296 to DF-REF-298 | `rule_row` of `rwb_decision` | none | Not read |
| DF-REF-185 to DF-REF-197, DF-REF-299 | `rule_test_case` of `rwb_decision` | none | Not read |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` of `rwb_decision` | none: the central ledger is P7's | Not read and not written |

No rule table exists in `rwb_access` and none is created: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s under ASM-0069, and their fields arrive in the contract, not by a schema read (DP-01). No row of `case`, `task` or `assignment` is read, and the case id of an administrative change is empty. The field-level shape of the change inside `inputs_ref`, the record code it is written under and the field-level shape of `dryRunCounts` beyond the fields `DryRunResult` already declares are Not specified in the source documents (GAP-0868; ASM-1573); the contract of RWB-P4-E8007-CON fixes the answer, and the entry carries the same fields. Field IDs are those of the Logical Data Model and Data Dictionary v9. The two registry reads are consumed against the P7 rule-package contract and its fake; the contract dependency they need is not in the metadata and is raised at D1. The operation POST /api/recovery/access/v1/admin/rule-changes and the read beside it are Not specified in the source documents (GAP-0868).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/rule-changes` | P4 `rwb-access` | Body: `packageCode`, `versionId`, `validFrom`, `reason`, `checklist` (the seven items of TSD P4 v3 T6.3) | `RuleChange`: `changeId`, `packageCode`, `versionId`, `versionLabel`, `versionState`, `testResult`, `dryRunCounts`, `validFrom`, `reason`, `checklist`, `state` `REQUESTED`, `approverRole` `RW-RISK`, `canApprove`, `authorReference`, `parameterVersion`, `recordedAt`, with `Location` of the read | 401 (MSG-P4-001); 403 Rules and parameters C (MSG-P4-002); 409 the version is not `LOADED` (MSG-GEN-004); 422 a required field empty or not a date (MSG-GEN-001) and a checklist item missing (MSG-P3-022); 503 the change cannot be recorded or the registry is unavailable (MSG-P7-003) | Rules and parameters C | `Idempotency-Key` header required; the stored answer is replayed |
| GET | `/api/recovery/access/v1/admin/rule-changes/{changeId}` | P4 `rwb-access` | None | The same `RuleChange` with `versionState` as the registry reports it at the time of the read | 401; 403 Rules and parameters R (MSG-P4-002); 404 unknown change id; 503 the registry or the record cannot be read (MSG-P7-003) | Rules and parameters R | Not applicable, read only; no Idempotency-Key |

Both operations sit under the base `/api/recovery/access/v1` of DP-13. They are this service's administration record of a rule change; the rule-package operations themselves — the version load, the version list, the dry run, the approval, the rollback and the change report — are `rwb-decision`'s (ownership map, ASM-0040), and the contract-dependencies row of this story names no P7 contract, which is the missing dependency of GAP-0868 and ASM-1571. The two operations of RWB-P4-AD011-APP and RWB-P4-AD012-APP are not repeated, extended or shadowed here.

The boundary of the record is deliberate: a version load records nothing (RWB-P4-AD011-APP), because a load is not a decision, and the approval records in the registry's own version row (TSD P4 v3 T6.3). A change request records here, because it is the administration's decision that this version is the one Risk is asked to approve from this date, on this evidence.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 `rwb-decision` | The version of the body: its state, label, checksum, valid-from date, test result and dry-run counts. Not in this story's metadata contract-dependency list (GAP-0868; ASM-1571) |
| GET | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run` | P7 `rwb-decision` | The dry-run result of the version, with its counts and its overall test result. Not in the metadata list either (same gap) |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters C check of the write and the R check of the read, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The parameters version in force on the change date, which the change carries; the C dependency `RWB-P3-E1042-CON` |

The two `rwb-decision` operations are declared as consumed, never as provided. The approve and the rollback operations of the registry are not consumed by this story at all: the approval is the decision center's and this service offers no approve action.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a recorded change: change id, package code, version id and label, test result, dry-run counts, valid-from date, author reference, approver role and parameters version |

CloudEvents 1.0 envelope; the payload carries references, codes, versions, dates and times and no name, no e-mail address and no personal field. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` and `DoaLimitChanged`, owned by other stories of this service, and the rule-version event `rwb.decision.RulePackageInForce.v1` (EV-30) is published by the registry's promotion at 00:01, not here.

#### 12.4 Events consumed

None. The state of a version is read on request, and the promotion at 00:01 is `rwb-decision`'s Schedule on `rwb-decision`'s queue.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals none and registers no activity on the `rwb-access` queue. The promotion at 00:01 (JOB-20) is a Temporal Schedule of `rwb-decision`, and the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.6 Schedules

None. A change is request-driven.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role and class of the caller and of the author |
| `permission` | P4 (`rwb_access`) | Read only: the C and A letters in Rules and parameters |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of a change. Read: the entry by change id |
| `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in `rwb_access` | The idempotency row and the outbox row of each entry; no inbox row is written because no event is consumed (DP-09) |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the version arrives through the registry's contract (ASM-0069) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's |

No rule table is named as this service's and no table of another service is read, and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision rule-package fake | the P7 rule-package contract (GAP-0868; ASM-1571) | `GET /admin/rule-packages/{packageCode}/versions` answering version "ENTRY-2027.01" in state `LOADED` with its label, its checksum, test result `PASS` and dry-run counts, and version "ENTRY-2026.11" in state `IN_FORCE`; the same version later `APPROVED` then `IN_FORCE` for the read; `GET /admin/rule-package-versions/{versionId}/dry-run` answering the counts and the result of AC5; a 503 for X6 and X8; a record of every call, so the refusal of AC3 can assert that no call was made |
| rwb-case parameters fake | RWB-P3-E1042-CON | `GET /api/recovery/case/v1/admin/parameters` answering the parameters version "PAR-2026.11" in force on 15 December 2026 |
| authorise and guard fake | RWB-P4-E8007-CON, RWB-P4-E1037-CON | A granted answer for RW-COE with Rules and parameters C, for RW-AUDIT with R and for RW-RISK with A and R, and a refused answer with MSG-P4-002 for RW-CASEOWN holding R only on the write |
| decision-record fake | RWB-PLT-E1027-CON | The append of a change entry, the hash-link check, the change read by id, the replay by `Idempotency-Key` and the forced write failure of AC2 |
| gateway-bff fake | RWB-PLT-N001-CON | The SCR-39 route with the rule-versions panel, the change form, the checklist state and the change read |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2; consumed 4 | Base `/api/recovery/access/v1`; two `rwb-decision` reads, the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The promotion at 00:01 is a Schedule of `rwb-decision` |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/rulechange`, Java package `th.co.scb.ace.workbench.recovery.access.rulechange`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module rule-version screen that raised, tested and approved a change in one process (DP-13 and DP-19: the service's own base and the operation moved to the registry, and the screen arrives through the composite route) and the monolith's own decision log write (DP-03: the local chain of the library). There is no DP-04 and no DP-07 in this story's pattern set on purpose: the Drools kit, the evaluation and the version states are P7's and of the model-owning services, and the lists this story uses are contract constants of the technical specification, so no reference-data read is claimed.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleChangeController | Controller | The two operations: body validation, the authorise call before the registry read, the RFC 9457 mapping, `Location` on a created change |
| RuleChangeService | Service | The change id, the approver role, the `canApprove` computation, and the assembly of the answer from the registry's fields |
| ChecklistGate | Service | The seven item codes of TSD P4 v3 T6.3 and the first missing item, named in the 422 |
| RulePackageClient | Client | The two registry reads, one hop and 2 s, with a breaker; maps a refused or unavailable registry to 409 or 503 |
| PermissionReader | Service | The `role` and `permission` rows of the caller behind the authorise operation |
| ParameterReader | Service | The parameters version in force through the contract of DP-06 |
| ChangeRecordAppender | Service | The change entry and its outbox and idempotency rows, in one transaction (DP-03, DP-09) |
| ChangeReader | Service | The entry of a change by change id, and its replay by `Idempotency-Key` |

**Database and migrations**

- This story creates no table of its own. The local decision-record table of DP-03 and the platform library objects `outbox_event`, `processed_event` and `idempotency_key` are created in `rwb_access` by the service's own DB work in the per-service Flyway sequence of DP-15, and this story only writes and reads them.
- No rule table is created and no rule column is added to `rwb_access`: the registry holds `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` (ASM-0069), and a version arrives as a document of the contract.
- The read of a change by its identifier needs a lookup on the reference column of the record entry; where the SIT plan needs an index that the creating story does not have, the index is added to that story's migration and not to a new one here.
- No statement updates or deletes an entry: the chain is append-only, and the only writes of this story are one entry, one outbox row and one idempotency row per change.
- The entry, the outbox row and the idempotency row commit in one transaction; a failure rolls all three back, which is why legacy AC2 changes nothing.

**Configuration and reference data**

- The parameters version in force is read through DP-06 on the change date and carried on the change; this story holds no threshold, no bound and no default, so no parameter value is a constant in code (BR11).
- The seven checklist item codes and the version states are contract constants, fixed by TSD P4 v3 T6.3 and T4 and published by RWB-P4-E8007-CON; a new item or a new state is a contract change reviewed with the registry owner and with audit (ASM-1572).
- The approver role `RW-RISK` is the role the technical specification names for the approval, and it is stated in the contract; this service resolves no role name of its own.

**Build steps**

1. `ChecklistGate` with the seven item codes, and the 422 of AC3 that names the missing item and makes no registry call.
2. `PermissionReader` and the authorise call before the registry read; the AC3 refusal of RW-CASEOWN with R only, and the 401 of X3.
3. `RulePackageClient` against the registry fake: the `LOADED` read of AC1 and AC5, the `IN_FORCE` refusal of AC4, and the 503 of X6.
4. `RuleChangeService` with the approver role and `canApprove`; the AC5 answer, including `canApprove` false for the author and true for RW-RISK.
5. `ChangeRecordAppender` and `ChangeReader` with the hash link, the replay by `Idempotency-Key` and the forced failure of AC2 (X7).
6. `ParameterReader` over the parameters contract; the test that a changed parameters version is data and needs no build.
7. The composite-route run of the SCR-39 states through the gateway-bff fake, so the screen can be demonstrated while the registry is being built.

**Feature switch.** No switch of this slice's own: a change request that is switched off would leave the analyst without a record of the change they took, which is the failure the record exists to prevent. The service-level flag of the service baseline governs the administration surface, and this story adds none.

**Done when.** The tests in section 16 pass; a change on a loaded version is answered 201 with the version label, the test result, the dry-run counts and `approverRole` `RW-RISK`, and leaves exactly one entry; a checklist with `verify` missing is answered 422 with MSG-P3-022 naming `verify`, with no registry call and no entry; a version in `IN_FORCE` is answered 409 with MSG-GEN-004 and nothing changes; the author of the version is answered `canApprove` false and the registry refuses the author with MSG-P7-002; and a forced record failure leaves nothing written and answers 503 with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters C on the write, or no R on the read | You cannot {action} here. Your role does not include it. | This story, from the authorise answer |
| MSG-P3-022 | A checklist item is missing or empty; `missingItem` names the item code | The change cannot be approved: {item} is missing or failed. | This story, from the checklist gate, with `{item}` filled with the item code |
| MSG-GEN-001 | A required body field is empty, or `validFrom` is not a date | Enter {field}. | This story, on the write |
| MSG-GEN-004 | The registry reports the version in a state other than `LOADED` | Someone else changed this record. Reload it to see their change. | This story, on the write; the answer names the state |
| MSG-P7-002 | The author of the version asks the registry to approve it | You prepared this decision, so you cannot approve it. | `rwb-decision`; this story asserts it through the fake and offers no approve path |
| MSG-P7-003 | The change cannot be recorded, or the registry cannot be reached | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 422 of an incomplete checklist also carries `missingItem` with the item code, and the 409 of a state refusal also carries `versionState`, so the screen can show the refusal without a second call. The text of MSG-P3-022 and of MSG-P7-002 is the text of the message tables of the rule-change stories and of TSD P4 v3 T6.3 and is copied unchanged.

### 15. Screens and states

SCR-39 Rules and parameters is the administration screen, served through the gateway-bff composite route of DP-19, which calls the registry's version reads and the two operations of this story, one hop each, and merges the answers. This story serves the two operations behind it and builds no screen surface of its own.

| Screen | State | What it shows |
|---|---|---|
| SCR-39 Rules and parameters | Versions | The versions of the package with their state, their label, their test result and their dry-run counts, read from the registry |
| SCR-39 Rules and parameters | Change form | The seven checklist items, the valid-from date and the reason, with the invalid ones marked before the call |
| SCR-39 Rules and parameters | Checklist incomplete | The 422 with MSG-P3-022 and the missing item named, with nothing sent to the registry |
| SCR-39 Rules and parameters | Not loadable | The 409 with MSG-GEN-004 and the state of the version named, so the analyst sees that only a `LOADED` version can be raised |
| SCR-39 Rules and parameters | Recorded | The change with its id, the version label, the test result, the dry-run counts, `state` `REQUESTED` and `approverRole` `RW-RISK`, and the note that the approval is Risk's in the decision center |
| SCR-39 Rules and parameters | Change read | The change with `versionState` `LOADED`, `APPROVED` or `IN_FORCE` as the registry reports it, so the analyst sees the progress without a second screen |
| SCR-39 Rules and parameters | Refused | The MSG-P4-002 refusal for a role without Rules and parameters C, with no form and no version detail |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (DOR-RWB-P4-E8007-APP-10) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (DOR-RWB-P4-E8007-APP-10) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (DOR-RWB-P4-E8007-APP-10) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (DOR-RWB-P4-E8007-APP-10) |

The legacy story also lists SCR-41 Delegation of authority with the states Versions, load and approval. That screen belongs to the delegation of authority capability and to RWB-P4-E8008-APP, which moves a limit; a decision rule is not a limit, and this story serves no field of SCR-41.

SCR-41 Delegation of authority states Empty, Loading, Error and No access: Not specified in the source documents (DOR-RWB-P4-E8007-APP-10).

Approval is not a state of this story: the approve action on a loaded version is the registry's, so the change shows `approverRole` `RW-RISK` and `canApprove`, and the screen links to the decision center rather than offering the approval here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-007-01 | AC1, BR1, BR6 | Contract | The registry fake: version "ENTRY-2027.01" `LOADED`, test result `PASS`, the dry-run counts and the checksum; the change recorded with the version label, the evidence and one entry |
| TC-E8-007-02 | AC2, BR9 | Component | The record store forced to fail during a change: 503, MSG-P7-003, no change id and no entry |
| TC-E8-007-03 | AC3, BR3, BR4 | Component | A checklist with the item `verify` missing: 422, MSG-P3-022 naming `verify`, no registry call and no entry; then RW-CASEOWN with R only: 403 and MSG-P4-002 with nothing written |
| TC-E8-007-04 | AC2, BR9, BR10 | NFR | The record store forced to fail on a run of repeated attempts with one `Idempotency-Key`: every attempt answers 503 with MSG-P7-003, nothing is written, no partial change exists and a later retry with the same key answers one change |
| TC-E8-007-05 | AC4, BR2 | Component | The registry fake answers version "ENTRY-2026.11" in state `IN_FORCE`: 409, MSG-GEN-004 with the state named, no entry, and the version in force still decides the cases it decided |
| TC-E8-007-06 | AC5, BR5, BR6, BR8 | Component | The change read back with `versionState` `LOADED` then `APPROVED` then `IN_FORCE`, `approverRole` `RW-RISK`, `canApprove` false for the author and true for RW-RISK, and the registry's refusal of the author with MSG-P7-002 |
| TC-E8-007-07 | BR7, section 12.7 | Component | Each table of section 12.7 checked at its boundary: the reads and writes of this service reach only `role`, `permission`, the local decision-record table and the three PLT library tables; no row of the P7 tables is read or written and no foreign key crosses a schema |
| TC-E8-007-08 | BR11, BR12 | Component | The entry of a change read back: references, codes, versions, dates and times only, with no name, e-mail address or personal field; the parameters version is the one read through DP-06 and carried on the change |
| TC-E8-007-09 | BR13 | Component | A request to a load or approve path of RWB-P4-AD011-APP or RWB-P4-AD012-APP finds no route in this service, and no registry load or approve call is made |
| TC-E8-007-10 | AC6, BR7, BR11, BR12, BR13 | Component | The registry fake answers version "ENTRY-2027.01" `LOADED`: the table reads, the parameters version, the entry fields and the route list of this service are checked against the boundary rules |
| TC-E8-007-11 | AC7 | Component | A call without an authenticated caller: 401 and no change; a read of an unknown changeId: 404; neither writes an entry |
| TC-E8-007-12 | AC8 | Component | The rwb-decision contract mock fails or does not answer on a change for "ENTRY": the answer is as AC8 states, with no changeId, no entry and no change for that version |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows of RWB-E8-007 are kept: TC-E8-007-01 for AC1, TC-E8-007-02 for AC2, TC-E8-007-03 for the access refusal and TC-E8-007-04 for the forced record failure, and two rows are added for the new criteria of this story. The legacy table carries a Covers column and no Level column: `System` is not a legacy value, and the Level of each row is the assignment of this template under §R7.2 s16, with `Access` read as Component and `Principle 5` as NFR. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the checklist item codes and the version states are the contract constants of the technical specification, and the parameters version in force is read through DP-06; a test proves that a changed parameters version and a promoted version need no build (BR11).
- No personal data anywhere: a change carries references, codes, versions, dates and times, and no name, no e-mail address and no personal field appears in the answer, the entry or the tests (BR12, NFR-040).
- No read of another service's tables (DP-01): `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` are `rwb-decision`'s, `case` and `task` are `rwb-case`'s, and no join crosses a schema. No rule table is named as this service's.
- One writer for a version: only `rwb-decision` writes a version, its state and its approval. This story holds no rule table, exposes no approve path and starts no workflow, so a change cannot approve itself.
- One record per change: the entry, the outbox row and the idempotency row commit together, and the chain is append-only, so a retry cannot produce a second change and a change can never lose its record (BR9, BR10).
- No record, no change: where the entry cannot be written the request is refused with MSG-P7-003 and nothing is written, so an administrative decision that cannot be defended is never taken (legacy AC2, R-UNI-39).
- A refused caller learns nothing: the 403 names the missing right and not the version, and the state refusal names the state the caller could already see on the screen.
- The evidence is copied and never recomputed: the label, the test result and the dry-run counts are the registry's fields, so a change can never claim a result the registry did not return.
- The legacy load gate and approval are untouched: this story adds no operation to RWB-P4-AD011-APP or RWB-P4-AD012-APP and is not a build dependency of either (BR13).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a version stamp and no code release, and rolls back by one call | Epic 8 | FEAT-ADM-02 | All recovery processes | BR1, BR6, BR7, BR8 | TC-E8-007-01, TC-E8-007-05, TC-E8-007-07 |
| REQ-CWC-014 | A load is validated for schema, overlapping rows, unreachable rows, a missing default row and a set of test cases before it takes effect | Epic 8 | FEAT-ADM-02 | All recovery processes | BR2, BR3, BR6 | TC-E8-007-03, TC-E8-007-06 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold and limit, versioned | Epic 8 | FEAT-ADM-02 | All recovery processes | BR11 | TC-E8-007-01, TC-E8-007-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 | FEAT-ADM-02 | All recovery processes | BR4, BR5 | TC-E8-007-03, TC-E8-007-06 |

The requirement IDs are the rows this story serves, taken from the Program and Epic 1 BRDs and the FSD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this story.

| Legacy reference | Where it is kept |
|---|---|
| AC1 change a decision rule through the administration screens: change a rule, test it and put it in force as a new version, and write the result to the decision log with the rule version | Sections 1, 4, 7, 8, 12.1, 12.3, 14 |
| AC2 not recorded: the decision log cannot be written, nothing changes and MSG-P7-003 | Sections 1, 4, 5, 7, 8, 17 |
| The legacy endpoints `POST /admin/rule-versions` and `POST /admin/rule-versions/{versionId}/approve` | Sections 1, 4, 12.1, 12.2, 19 — both are the registry's under ASM-0040 |
| Permission checks: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 10, 12.1, 16 |
| Screens SCR-39 and SCR-41 and their states Versions, load and approval | Sections 15, 19 |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P7-002, MSG-P7-003 | Section 14, exception paths |
| The `decision_log_entry` and `rule_row` entities of the legacy data table | Section 11, carried to P7's registry and to the local chain |
| TC-E8-007-01 to TC-E8-007-04 | Section 16 |
| Legacy key RWB-E8-007, story RWB-P4-E8007-APP, contract RWB-P4-E8007-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The registry half under `rwb-decision` (P7, ASM-0069 and ASM-0040): the compile to DRL and the KieBase, the checksum, the overlap, unreachable-row and default-row checks, the scenario run, the dry run itself, the version states, the four-eyes approval by RW-RISK with its MSG-P7-002 refusal, the promotion at 00:01 with `RulePackageInForce`, the one-call rollback and the change report.
- The load of a rule version and its row gate: RWB-P4-AD011-APP (legacy RWB-AD-011). This story raises a change on a version that story loaded and neither repeats nor extends it.
- The approval of a rule version: RWB-P4-AD012-APP (legacy RWB-AD-012) and the registry. This story records who must approve and offers no approve action.
- The Drools kit and any evaluation of a rule: the model-owning services fetch the version, verify the checksum and swap it in (DP-04), and this story embeds no Drools kit.
- The `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables and their migrations; they are `rwb-decision`'s.
- The change report and the decision counts per package version: the registry's change report and RWB-P3-E2041 (legacy RWB-E2-041).
- The move of a delegation limit on SCR-41 Delegation of authority: RWB-P4-E8008-APP.
- The screen SCR-39 itself, its panels beyond the change form and its composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
