# RWB-P3-E2041-APP Rule change governance and audit report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2041-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-041 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1073-APP |
| Depends on (build) | RWB-P3-E2041-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1073-APP |
| Contract dependencies | RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-026, FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-041 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E2041-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE) and an internal audit reader**, I want **every case decision that rwb-case makes to carry the rule ID and the package version label, the open-case count behind an impact summary to be read from the case queues, and one case-side audit read that lists per package version the decisions rwb-case made, the cases they touched, the first and last decision time, the open cases still at that version and the version each open case keeps, while the rule package registry, the change checklist, the four-eyes approval and the change report themselves are consumed from rwb-decision**, so that **a rule change is as controlled as a code change and every case outcome can be explained by the version that decided it**.

This story owns the case-side half of RWB-E2-041 only. The registry half — `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the change checklist DF-REF-295, the approval checks, the effect counts and the change report — is owned by P7 rwb-decision under ASM-0069 and is consumed here through its contract and its fake. rwb-case writes no rule table and reads none (DP-01). The integration harness RWB-ITG-E2041-ITG proves the whole journey across the three services; this story builds only what rwb-case must do for that journey.

### 2. Business rationale

Audit found the collection procedure was not followed because rules lived in documents (control CTL-08). Rules are data now: one wrong row in a rule package changes every case that reaches it, so each package version needs the same evidence as a code change — who asked, what it affects, the test result, who approved, when it took effect and how to undo it — and each case outcome must name the version that decided it. The legacy story answered both halves in one monolith: the checklist on `rule_package_version`, the approval checks and one change report, all in the recovery schema.

In the target the governance of a package is central in rwb-decision (P7) and evaluation is local to the service that owns the decision (DP-04; Architecture v5 slide 27). That split leaves rwb-case with three things it must do and nothing else: it must pin the rule ID and the package version label on every decision record it writes (DP-03), so the decisions per version reconcile; it must answer the open-case count an impact summary speaks about, filtered by product group and status, from its own case list (DP-01, DP-06, DP-07); and it must offer one audit read of what its own cases did under each package version, including the version each still-open case keeps under R-UNI-38. It meets REQ-CWC-013 and REQ-DRI-011 at the case-side level. The measure is that every package version in force reconciles between the decisions the ledger holds and the decisions rwb-case reports, and that no open case is silently re-pointed to a newer version.

### 3. Preconditions

- RWB-P3-E2041-CON is published: the case resource and queue-case-list shapes, the new case-side audit read with its fields, errors and the two consumed event contracts, and the contract fakes.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger contract behind it.
- RWB-PLT-E1072-CON is published: the embedded Drools kit, with one KieBase per package version, first-match semantics and the `NoPackageInForce` outcome (DP-04). RWB-P3-E1073-APP is done: the packages in use by rwb-case are approved by RW-RISK, who is not the author, and are in force from their valid-from date with at least 50 passing scenarios.
- RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the parameters contract and the reference-data contract, both owned by rwb-case, with the client library (DP-06, DP-07).
- RWB-PLT-E1037-CON is published: the guard library. RWB-P4-E1037-CON is the rwb-access authorise contract, consumed and faked (DP-08).
- RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15). RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19).
- Package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows, loaded by "U-41" and approved by "U-51", through the rwb-decision contract or its fake.
- The users "U-41" (RW-COE), "U-51" (RW-RISK) and "U-AUD-01" (RW-AUDIT) exist in rwb-access with the Rules and parameters rights of the legacy story.
- The retention period of the case-side audit read and of its CSV export: Not specified in the source documents (GAP-0720; ASM-1267).

### 4. Flow

1. rwb-decision: RW-COE loads a package version with its change checklist, the load checks and the scenarios run, and RW-RISK approves it; the version reaches IN_FORCE on its valid-from date at 00:01 and `rwb.decision.RulePackageInForce.v1` is published. Steps 1 and 2 are P7's and are exercised here through the contract or its fake.
2. rwb-case: the case router consumes `rwb.decision.RulePackageInForce.v1` through its inbox and drops the cached KieBase for that package, so the next evaluation fetches the version in force and verifies the checksum (DP-04).
3. rwb-case: an event, a timer or a task reaches a case, the CaseWorkflow calls the EvaluateRules activity, the embedded Drools kit returns `RuleResult(packageCode, packageVersion, ruleId, outputs)` for the version in force on the business date.
4. The RecordAndApply activity writes, in one `rwb_case` transaction, the local decision record with `rule_id` and the package version label, the state change and the outbox row; a record that cannot be written rolls the whole transaction back, so no case moves without its record (DP-03).
5. rwb-case: an open case keeps the package version it was decided under (R-UNI-38). A later version in force changes what the next decision uses; it never rewrites the version on the decisions already taken, and the case's own pinned version stays readable on the case.
6. rwb-case: a caller asks for the open cases of a queue through `GET /api/recovery/case/v1/queues/{queueId}/cases` with the product group and status filters; the response total is the count an impact summary speaks about, for example 412 open Mortgage cases in the queue.
7. rwb-case: RW-COE or RW-AUDIT reads the consumed change report from rwb-decision for a period and a package, as JSON or CSV, and sees the request, the impact, the test result, the author, the approver, the approved time, the valid-from date, the checksum, the effect counts and the decisions per package version.
8. rwb-case: the same reader calls `GET /api/recovery/case/v1/admin/rule-change-audit` with `from`, `to`, an optional package code and a format; rwb-case answers per package version with the decisions it made, the cases affected, the first and last decision time, the open cases still at that version and the version each open case keeps.
9. rwb-case: the audit read reconciles with the ledger. For the same period and package version the decision count of the case-side answer equals the count read from `GET /api/recovery/decision/v1/decision-log`, because both count the same records by `rule_id` and `rule_version`.
10. rwb-case: the reader asks for the same audit read as CSV; the answer holds one header row and one row per package version, with counts and times only, no case number and no party key.
11. rwb-case: a package version that is not in force is never used. An evaluation with no version in force fails with `NoPackageInForce`, the caller reports MSG-P3-027, nothing is written and the case waits; the stuck-case scan raises it.
12. rwb-case: the reader asks for a period with no case decision; the answer is an empty list with total 0, never an error.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No package version of the package is in force on the business date | The EvaluateRules activity fails at once with `NoPackageInForce`, non-retryable; no decision record, no state change; the case waits and the stuck-case scan raises it | MSG-P3-027 | AC2, AC10 |
| X2 | A package version reaches its valid-from date with no approver | rwb-case never receives it and never serves it; the case-side audit read names the version in force for the period | None | AC2 |
| X3 | A package version fails its load or approval checks in rwb-decision | Nothing reaches rwb-case; the refusal is answered by rwb-decision with MSG-P3-022 and asserted against the fake | MSG-P3-022 | AC3, AC4 |
| X4 | The decision record cannot be written | The state change, the record and the outbox row are one transaction, so nothing moves and the case is retried | MSG-P7-003 | AC10 |
| X5 | The audit read period ends before it starts | The call is refused before any read; nothing is computed | MSG-GEN-003 | AC8 |
| X6 | The audit read period holds no case decision | An empty list with total 0 and no error | None | AC6 |
| X7 | A reader holds no Rules and parameters right | The authorise check behind the operation refuses the call; nothing is returned | MSG-P4-002 | TC-E2-041-11 |
| X8 | rwb-decision does not answer the change report or the decision log inside the REST budget | One hop and the 2 s timeout apply; the call answers 503 and the case-side audit read still answers from rwb_case alone | None | AC1, AC10 |
| X9 | A newer package version is in force for an open case | The case keeps the version it was decided under and the audit read shows both the pinned version and the version now in force | None | AC10 |
| X10 | A case has decisions under two package versions in the period | The audit read counts the decisions under each version and the affected case once per version | None | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts and the platform contract stories; the whole registry half and the access answer come from the contract fakes, so no P7 story blocks the build |
| Negotiable | The audit read columns, the CSV header and the retention period are agreed with the consumers; the version pin, the refusal and the reconciliation are fixed by R-UNI-38 and DP-03 |
| Valuable | Audit can explain every case outcome by the version that decided it, and the impact summary of a pending change is a real count rather than a claim |
| Estimable | One audit read, two case-side answers, one version pin on the decision record, one refusal guard and the contract tests |
| Small | Fits one sprint with its tests |
| Testable | Every criterion is an API or component test; every P7 answer is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Rule change governance and audit report

  Background:
    Given the business date is 2026-12-01
    Given the rwb-decision contract mock returns package ALLOCATION version "ALLOC-2026.11" in force with 24 rows
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given user "U-41" holds RW-COE, "U-51" holds RW-RISK and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 Change by checklist (legacy RWB-E2-041 AC1)
    Given the rwb-decision contract mock returns a request "CR-2026-0042" to change ALLOCATION row "ALLOC-031" from queue "MTG-BKK-CO" to "MTG-CEN-CO" from 2026-12-10
    Given a request "CR-2026-0042" to change ALLOCATION row "ALLOC-031" from queue "MTG-BKK-CO" to "MTG-CEN-CO" from 2026-12-10
    Given the rwb-decision contract mock returns ALLOCATION version "ALLOC-2026.12" loaded by "U-41" with impact summary "412 open Mortgage cases in the BKK queue" and rollback plan "Roll back to ALLOC-2026.11"
    Given "U-41" loads ALLOCATION version "ALLOC-2026.12" with impact summary "412 open Mortgage cases in the BKK queue" and rollback plan "Roll back to ALLOC-2026.11"
    Given the rwb-decision contract mock returns the load checks passed and 50 of 50 scenarios passed
    Given the load checks and the 50 scenarios pass
    Given the rwb-decision contract mock returns version "ALLOC-2026.12" approved by "U-51" on 2026-12-02
    Given "U-51" approves version "ALLOC-2026.12" on 2026-12-02
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then one entry shows package "ALLOCATION", version "ALLOC-2026.12", request "CR-2026-0042", test result "PASSED", author "U-41", approver "U-51", approved on 2026-12-02 and valid from 2026-12-10
    Then the entry shows 1 row changed, 0 added and 0 removed against "ALLOC-2026.11"
    Then the approval time is before the valid from date

  Scenario: AC2 Checklist skipped (legacy RWB-E2-041 AC2)
    Given the rwb-decision contract mock returns ALLOCATION version "ALLOC-2026.13" loaded by "U-41" with a complete checklist, valid from 2026-12-15 and never approved
    Given ALLOCATION version "ALLOC-2026.13" loaded by "U-41" with a complete checklist, valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the rule package service still serves version "ALLOC-2026.12"
    Then the change report shows version "ALLOC-2026.13" with status "LOADED" and approver empty

  Scenario: AC3 Checklist item missing at approval (legacy RWB-E2-041 AC3)
    Given the rwb-decision contract mock returns RESTRUCTURE version "RES-2026.12" loaded with no rollback plan
    Given RESTRUCTURE version "RES-2026.12" loaded with no rollback plan
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    Then version "RES-2026.12" stays "LOADED"

  Scenario: AC4 Failed test result (legacy RWB-E2-041 AC4)
    Given the rwb-decision contract mock returns PAYMENT_MATCH version "PMT-2026.12" whose scenario result is "FAILED" with 2 of 58 scenarios failing
    Given PAYMENT_MATCH version "PMT-2026.12" whose scenario result is "FAILED" with 2 of 58 scenarios failing
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"

  Scenario: AC5 Verify item recorded before approval (legacy RWB-E2-041 AC5)
    Given the rwb-decision contract mock returns ALLOCATION version "ALLOC-2026.12" loaded on 2026-12-08 with verify note "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases" and verify date 2026-12-08
    Given ALLOCATION version "ALLOC-2026.12" loaded on 2026-12-08 with verify note "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases" and verify date 2026-12-08
    When "U-51" approves it on 2026-12-09
    Then the change report shows verify date 2026-12-08, the verify note, the load time 2026-12-08 and checksum "9f2c...e1b4"
    Then the checklist holds all seven items: request, impact, test result, approver, load, verify and rollback plan

  Scenario: AC6 Period with no changes (legacy RWB-E2-041 AC6)
    When "U-AUD-01" reads the change report for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC7 Verify date before the load (legacy RWB-E2-041 AC7)
    Given the rwb-decision contract mock returns ALLOCATION version "ALLOC-2026.14" with verify date 2026-12-07 and load time 2026-12-08
    Given ALLOCATION version "ALLOC-2026.14" with verify date 2026-12-07 and load time 2026-12-08
    When "U-41" loads it
    Then the system refuses the load with MSG-GEN-003 naming "verifiedAt" and "loadedAt"

  Scenario: AC8 Period in the wrong order (legacy RWB-E2-041 AC8)
    When "U-AUD-01" reads the change report from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"

  Scenario: AC9 Report as CSV (legacy RWB-E2-041 AC9)
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per package version
    Then it carries no party identifier and no case data

  Scenario: AC10 Decisions per package version (legacy RWB-E2-041 AC10)
    Given the rwb-decision contract mock returns ALLOCATION version "ALLOC-2026.11" in force until 2026-12-09 and "ALLOC-2026.12" from 2026-12-10
    Given ALLOCATION version "ALLOC-2026.11" was in force until 2026-12-09 and "ALLOC-2026.12" from 2026-12-10
    Given the rwb-decision contract mock returns 96 decision log entries with package version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" in December 2026
    Given the decision log holds 96 entries with package version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" in December 2026
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then version "ALLOC-2026.11" shows 96 decisions and version "ALLOC-2026.12" shows 1,204
    Then the entry shows the decisions per rule ID across both versions: "ALLOC-031" 700 and "ALLOC-032" 600
    Then the total matches GET /api/recovery/decision/v1/decision-log for the same period and package version
    Then RWB-E2-005 reconciles the count per package version from this report
```

These ten criteria are the legacy acceptance of the whole governance journey and are copied unchanged apart from the origin tag, the decision-log path of AC10 and the parallel mock Given; the split they hide is this. Steps 1 to 6 of the flow — the checklist on the package version, the load checks and scenarios, the four-eyes approval, the effect counts, the valid-from promotion and the change report in JSON and CSV — are P7 rwb-decision and are faked for every criterion here; this story consumes them through the five operations of section 12.2 and asserts only what it receives. The case-side half is P3's and is what this story builds: the pin of `rule_id` and the package version label on every case decision record (DP-03, DP-04), the open-case impact count through the queue case list, the case-side audit read of 12.1, the refusal of a package version that is not in force (MSG-P3-027) and the rule that an open case keeps the version it was decided under (R-UNI-38). Where a criterion speaks of the decision log, this story counts only the decisions rwb-case made and reconciles them with the ledger read.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version can be approved only when it carries a change request reference, an impact summary, a verify record, a rollback plan and a test result of PASSED | CTL-08; rule package change process steps 1 to 4 |
| BR2 | The approver is not the author | roles.txt Separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013 |
| BR4 | The verify item is dated on or after the load and before the approval | rule package change process step 6 |
| BR5 | The report lists every package version whose load, approval, valid from, verification or rollback falls in the period | REQ-DRI-011 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, by Drools rule name and row order, and the rule IDs changed | D-RCV-36 T4, T5; ADR-012 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38 |
| BR8 | The decisions per package version are counted from `rule_id` and `rule_version`; the report never recomputes a decision | REQ-DRI-011; D-RCV-36 T5 |
| BR9 | The checklist is one JSON object on the package version row; this story adds no table and no column for it | D-RCV-36 T4; RWB-E1-072 |
| BR10 | Every case decision record pins the rule ID and the package version label, written in the same transaction as the state change | DP-03; D-RCV-36 T5; Architecture v5 slide 28 |
| BR11 | An open case keeps the package version it was decided under; a version in force changes the next decision only | R-UNI-38; TSD P3 T2.2 |
| BR12 | A package version that is not in force is never used: the evaluation fails with `NoPackageInForce` and nothing is written | R-UNI-38; DP-04; MSG-P3-027 |
| BR13 | The case-side audit read lists, per package version, the decisions rwb-case made, the cases affected, the first and last decision time, the open cases still at that version and the version each open case keeps | REQ-DRI-011; R-UNI-38 |
| BR14 | The impact count is the total of the open cases of the queue, filtered by product group and status, read from the case list of rwb-case | REQ-CWC-013; FSD P3 A2.16 example "412 open Mortgage cases" |

BR1 to BR4, BR6, BR7 and BR9 are implemented in P7 rwb-decision under ASM-0069 and are asserted here only through the consumed operations and the fake. BR5 and BR8 are P7's counts; this story reconciles BR8 for its own cases and never recomputes a decision. BR10 to BR14 are built here.

### 9. State transitions

None. No case status changes in this story. The package version states are P7's and are shown only to fix what rwb-case observes.

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | Approve | Checklist complete, test result PASSED, approver is not the author | APPROVED |
| LOADED | Approve | Any item missing or test result FAILED | LOADED (refused) |
| APPROVED | Valid-from date reached at 00:01 | The version is approved and rwb-case receives `RulePackageInForce` | IN_FORCE |
| IN_FORCE | A newer version is promoted | The newer version reaches its valid-from date | SUPERSEDED |
| IN_FORCE | Rollback | One call in rwb-decision names the version it returns to | ROLLED_BACK |

The case side is a pin, not a move. A decision already taken keeps its `rule_version`; a case that is still open keeps the version it was decided under (R-UNI-38) until its next decision, and the audit read reports both the pinned version and the version now in force. No case row is rewritten by a promotion, a rollback or a refusal.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a package version with its checklist in rwb-decision (Rules and parameters CRUD); reads the change report with its fake of the impact summary and reads the case-side audit read |
| RW-RISK, risk and model risk officer | Approves a package version in rwb-decision (Rules and parameters A); reads the change report and the case-side audit read |
| RW-AUDIT, internal audit | Reads and exports the change report and the case-side audit read (Rules and parameters R). Changes nothing |
| RW-PLATADM, platform administrator | Reads both reads (Rules and parameters R) |
| RW-CASEOWN, case owner | Reads the queue case list for the impact count (Case record R); holds no Rules and parameters right and is refused by both audit reads |
| SY-RULES, Drools evaluator | Evaluates the version in force and writes its rule ID and version to the decision record; it takes no decision and approves nothing |
| No delegation of authority level applies | A package version is not a credit decision |

The right behind the new case-side audit read follows the legacy right of the report, Rules and parameters R, answered by rwb-access through `POST /api/recovery/access/v1/authorise` (DP-08). The right is not stated for the case-side read in any source, so it is carried as an assumption (GAP-0718; ASM-1265) and confirmed with rwb-access in the capability matrix review.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-024 to DF-CAS-029 | case_account | the account link fields of the case | Read |
| DF-REF-275 | rule_package | package_code | Read through the rwb-decision contract |
| DF-REF-279 | rule_package_version | id | Read through the rwb-decision contract |
| DF-REF-281 | rule_package_version | version_label | Read through the rwb-decision contract, and written into the decision record |
| DF-REF-282 | rule_package_version | status | Read through the rwb-decision contract |
| DF-REF-286 | rule_package_version | valid_from | Read through the rwb-decision contract |
| DF-REF-287 | rule_package_version | valid_to | Read through the rwb-decision contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read, written by the local record library |
| DF-DEC-005 | decision_log_entry | rule_version | Read, written by the local record library |
| DF-DEC-016 | decision_log_entry | decided_at | Read, written by the local record library |

Field IDs are those of the Logical Data Model and Data Dictionary. rwb-case stores no rule package, no rule row and no test case: the package label on the decision record is a value, not a foreign key (DP-01, ASM-0069). The decision record fields the local library writes are `chain_seq`, `inputsRef`, `ruleId`, `ruleVersion`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prev_hash` and `entry_hash` (Temporal and Drools design slide 16). The response shape of the case-side audit read and its CSV column list are Not specified in the source documents (GAP-0718; ASM-1265); its retention period is Not specified in the source documents (GAP-0720; ASM-1267).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/queues/{queueId}/cases` | The open cases of a queue, filterable by `productGroup` and `status`, with the page total used as the impact count (BR14) | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}` | One case with the package version label its decisions are pinned to | Case record R, scope applied | Not applicable |
| GET | `/admin/rule-change-audit` | Per package version for a period: decisions made, cases affected, first and last decision time, open cases still at that version and the version each open case keeps (BR13) | Rules and parameters R | Not applicable |

The audit read takes the query `from` (date, required), `to` (date, required), `packageCode` (optional), `format` (`json` default or `csv`), `page` and `size` (default 50, max 200). It answers 200 with `items[]` of `CaseRuleChangeAuditEntry` (`packageCode`, `versionLabel`, `versionStatus`, `decisions`, `casesAffected`, `firstDecisionAt`, `lastDecisionAt`, `openCasesAtVersion`, `openCasesKeepingVersion`), `page`, `size`, `total`, or `text/csv` with the same columns. Errors: 401 no session (MSG-P4-001), 403 no Rules and parameters R (MSG-P4-002), 422 `to` before `from` (MSG-GEN-003), 503 store down.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Service | Used for |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/change-report` | rwb-decision (P7) | The change report for a period and a package, as JSON or CSV (AC1, AC5, AC6, AC8, AC9) |
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | rwb-decision (P7) | The package version load with its change checklist (AC1, AC7) |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | rwb-decision (P7) | The four-eyes approval and its refusal (AC1, AC3, AC4) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | rwb-decision (P7) | The version in force, its status, its dates and its checksum |
| GET | `/api/recovery/decision/v1/decision-log` | rwb-decision (P7) | The decisions the case-side audit read is reconciled with (AC10) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Rules and parameters right check behind every read (DP-08) |

#### 12.3 Events published

None. This story publishes no event type of its own; the local decision-record library writes the record row and its `DecisionRecorded` message in the same transaction as the state change (DP-03), and the type is owned by P7.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Case router, inbox dedupe; drops the cached KieBase for the package so the next evaluation fetches the version in force and verifies the checksum |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); every service publishes its own record | The audit read reconciles its own counts against the ledger entries of this type for the same period and package version |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Carries the case from entry to closure and pins the package version on each decision |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Calls the embedded Drools kit with a package code, facts and the business date; fails with `NoPackageInForce` |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record with `rule_id` and the package version label, the state change and the outbox row in one transaction |

#### 12.6 Schedules

None. The audit read is a request-driven call; the rule promotion at 00:01 and the chain check at 02:00 are P7's Schedules, and rwb-case starts none for this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case header, its status and its queue, read for the impact count and the audit read |
| queue | P3 (rwb_case) | The queue of the case list the impact count is read from |
| case_account | P3 (rwb_case) | The account link of a case, counted for the cases affected |

No rule table is named, written or read: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` are P7 rwb-decision tables (DP-01, ASM-0069). The local decision-record row and the outbox row are objects the platform library creates in rwb_case and are not owned by this story.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock | The P7 contract | ALLOCATION "ALLOC-2026.11" in force with 24 rows loaded by "U-41" and approved by "U-51"; "ALLOC-2026.12" loaded with the checklist and approved on 2026-12-09, valid from 2026-12-10; "ALLOC-2026.13" loaded and never approved; RESTRUCTURE "RES-2026.12" with no rollback plan; PAYMENT_MATCH "PMT-2026.12" with test result FAILED, 2 of 58 scenarios failing; "ALLOC-2026.14" with verify date before the load; checksum "9f2c...e1b4"; 1 row changed, 0 added, 0 removed; 96 and 1,204 decisions, "ALLOC-031" 700 and "ALLOC-032" 600; a CSV answer; an empty answer with total 0; 409 for MSG-P3-022, 422 for MSG-GEN-003 naming "to" and "from" or "verifiedAt" and "loadedAt" |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Rules and parameters R to RW-COE, RW-RISK, RW-AUDIT and RW-PLATADM, and refusing RW-CASEOWN with MSG-P4-002 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 6 consumed | The two existing case reads and the audit read provided; five rwb-decision operations and the authorise call consumed; one hop, 2 s timeout |
| Kafka | 0 published, 2 consumed | `rwb.decision.RulePackageInForce.v1` refreshes the package; `rwb.decision-record.DecisionRecorded.v1` is the ledger entry the audit read reconciles with |
| Temporal | 1 workflow, 2 activities | CaseWorkflow; EvaluateRules and RecordAndApply |
| File | None | The CSV answer is a REST response; this story writes no file |

### 13. Solution plan

**This story builds the case-side half only.** Step by step: the version pin on the decision record is P3's; the open-case impact count is P3's; the case-side audit read is P3's; the refusal of a version not in force is P3's; the rule that an open case keeps its version is P3's. The package registry, the change checklist DF-REF-295, the load checks and scenarios, the four-eyes approval, the effect counts, the valid-from promotion, the change report in JSON and CSV, the approval records and the ledger are P7 rwb-decision's and are consumed and faked — never rebuilt here. The test cases of section 16 run against the P7 fake for that half. The case-side audit read is not in the ownership map, so its owner, path and right are carried as a gap and an assumption (GAP-0718; ASM-1265).

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `rulechangeaudit`, Java package `th.co.scb.ace.workbench.recovery.case.rulechangeaudit`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleVersionPin | Service | Reads `version_label` and `rule_id` from the `RuleResult` and hands them to the record writer, so no caller builds the label itself (BR10) |
| CaseDecisionRecorder | Service | Calls the local decision-record library and writes the record row with the state change and the outbox row in one transaction (DP-03) |
| PackageInForceCache | Service | Holds the KieBase per package version, drops it on `RulePackageInForce` and refuses the evaluation when no version is in force (DP-04, BR12) |
| CaseQueueImpactReader | Service | Counts the open cases of a queue by product group and status from the case list; returns the page total used as the impact count (BR14) |
| RuleChangeAuditReader | Service | Groups the case decisions of the period by package version, computes the counts and the first and last decision time, and joins the open cases of each version (BR13) |
| RuleChangeAuditController | Controller | `GET /admin/rule-change-audit` in JSON and CSV; problem responses |
| CaseQueueController | Controller | `GET /queues/{queueId}/cases` with the product-group and status filters |
| CaseRepository | Repository | `recovery_case`, `queue`, `case_account`; writes only schema rwb_case |
| DecisionLogClient | Client | The rwb-decision decision log read used for the reconciliation of AC10 |
| AccessCheckClient | Client | The rwb-access authorise contract (cached) behind every read |

**Database and migrations**

- No new table and no new column. `recovery_case`, `queue` and `case_account` are read; the decision record rows are written by the library (DP-03).
- Migration `V2041_1__rule_change_audit_index.sql` adds `ix_case_queue_status` on `recovery_case (queue_id, status, product_group)` and `ix_case_decided_at` on the decision record `(rule_version, decided_at)` in rwb_case, so the audit read and the impact count answer inside the 2 s budget.
- The audit read is a read model over rows already written; it stores no copy of a package version and no copy of a ledger entry.

**Configuration and reference data**

- The list of package codes rwb-case evaluates is a parameter read through the parameters contract (DP-06), never a Java constant. The audit read accepts a `packageCode` filter from that list only.
- The status values used by the impact count come from LOV-CASE-STATUS and the product groups from LOV-PRODUCT through the reference-data contract (DP-07); no status or product group is written in code.
- The report right and the retention period of the audit read: right from the legacy story (Rules and parameters R), retention Not specified in the source documents (GAP-0720; ASM-1267).

**Build steps**

1. RuleVersionPin and CaseDecisionRecorder over the local record library; unit tests for BR10 and the one-transaction rule (AC10, X4).
2. PackageInForceCache over the embedded Drools kit with the `NoPackageInForce` path and the checksum check; tests for BR12 and X1.
3. The pinned-version guarantee: a promotion or rollback changes the next decision only; test for BR11 and X9.
4. CaseQueueImpactReader over `GET /queues/{queueId}/cases` with the product-group and status filters and the page total; tests for BR14 and AC1's impact summary count.
5. RuleChangeAuditReader and its grouping, counts and times; tests for BR13, AC10, X10.
6. RuleChangeAuditController in JSON and CSV with the date-order refusal and the authorise check; tests for AC6, AC8, AC9 and TC-E2-041-11.
7. DecisionLogClient against the rwb-decision decision log read and the reconciliation assertion of AC10.
8. Contract-fake run: every P7 and P4 answer of section 12.8 stubbed, so the story builds and its tests run before P7 and P4 land.

**Feature switch.** The legacy switch name `rwb.p3.rule-change-report` is kept as the legacy reference and read as a parameter through the parameters contract. Off: the case-side audit read answers 404 and the consumed change report is not called; the version pin, the impact count and the refusal are unaffected, because they are not a report.

**Done when.** The tests in section 16 pass, every case decision record of the SIT run names its rule ID and package version, the case-side audit read reconciles with the decision log for the same period and package version, no open case has been re-pointed by a promotion or a rollback, and the contract tests of RWB-P3-E2041-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-003 | Verify date before the load, or a report period in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-001 | A required checklist value is empty | Enter {field}. |
| MSG-P7-002 | The author approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right reads the report | You cannot {action} here. Your role does not include it. |
| MSG-P3-027 | No package version is in force on the business date | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

MSG-P3-022, MSG-GEN-003, MSG-GEN-001, MSG-P7-002 and MSG-P4-002 keep the text of the legacy story and are answered by the owning service; this story asserts them through the fake. MSG-P3-027 and MSG-P7-003 are carried unchanged from the rwb-case contract. For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code only.

### 15. Screens and states

No screen in this story. Internal audit and the center of excellence read the change report through the endpoint and open the CSV in a spreadsheet, and read the case-side audit read the same way. The rules and parameters screen SCR-39 of Epic 8 consumes the same entries; this story serves the two reads, not the screen.

| Screen | State | What this story answers |
|---|---|---|
| SCR-39 Rules and parameters | Report list | The change report entries of the period, with the request, the impact, the test result, the author, the approver, the approved time, the valid-from date, the checksum, the effect counts and the decisions per version |
| SCR-39 Rules and parameters | Export | One CSV header row and one row per package version, with counts and times only, no case number and no party key |
| SCR-39 Rules and parameters | No changes in the period | An empty list with total 0 and no error |
| No screen | Case-side audit read | Counts per package version: decisions, cases affected, first and last decision time, open cases at that version and the version each open case keeps |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-041-11 | Access; BR13 | Component | RW-CASEOWN (no Rules and parameters right) reads the audit read; refused with MSG-P4-002 |
| TC-E2-041-01 | AC1, BR1, BR5, BR6 | End to end | ALLOCATION v11 to v12, request CR-2026-0042, one changed row |
| TC-E2-041-02 | AC2, BR3, BR11 | End to end | ALLOCATION v13 loaded and never approved |
| TC-E2-041-03 | AC3, BR1 | End to end | RESTRUCTURE v12 with no rollback plan |
| TC-E2-041-04 | AC4, BR1 | End to end | PAYMENT_MATCH v12 with a FAILED scenario result |
| TC-E2-041-05 | AC5, BR1, BR4 | End to end | Verify date 2026-12-08, approval 2026-12-09 |
| TC-E2-041-06 | AC6, BR13 | End to end | Period 2026-11-01 to 2026-11-15 with no versions |
| TC-E2-041-07 | AC7, BR4 | End to end | Verify date one day before the load |
| TC-E2-041-08 | AC8, BR13 | End to end | Period end before start |
| TC-E2-041-09 | AC9, BR13 | End to end | CSV export of December versions |
| TC-E2-041-10 | AC10, BR8, BR10, BR13 | End to end | 96 and 1,204 decisions in December 2026; 412 open Mortgage cases in queue "MTG-BKK-CO" |

The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The Level column maps the legacy System level to End to end and the legacy Access level to Component. Ten of the eleven tests run against the rwb-decision fake for the registry half and against rwb_case for the case-side half; TC-E2-041-11 runs against the rwb-access fake.

### 17. Guardrails

- No business value in code: the checklist items, the impact summary, the rollback plan and the package rows are data held by rwb-decision; the package codes rwb-case evaluates are a parameter and the statuses are reference data. The audit read computes from rows.
- No personal data in logs, tests, workflow history or prompts. The two reads carry staff user IDs, counts and times only: no customer name, no address, no identity number and no case number in the CSV.
- No read of another service's tables and no ACE view: the package version, its status and the decision ledger come only through the rwb-decision contract; account and customer data come only through rwb-source-data (DP-01, DP-05).
- One evaluator: every package version is evaluated only through the embedded Drools kit on the model fetched from rwb-decision, with the checksum verified; no code reads a workbook, a generated DRL or a rule row (DP-04).
- No rule table in rwb_case and no second registry: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` stay P7's (ASM-0069).
- The decision record, the state change and the outbox row are one transaction; a refused or failed write moves nothing (R-UNI-39).
- The approver is never the author; the check is P7's and is asserted here, not re-implemented.
- Forbidden: any change to a decision already taken, and any rewrite of the version an open case keeps. A rollback is a new entry that names the version it returns to.
- One hop only, 2 s timeout and a breaker per downstream; a caller never chains two services (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated package version with a checklist and rollback | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E2-041-11, TC-E2-041-01 to TC-E2-041-04 |
| REQ-DRI-011 | Versioned tables with author and approver, and a count of decisions per version | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16, FEAT-CHO-11 | 14 Set strategy, policy and decision rules | CTL-08; R-UNI-38 | TC-E2-041-01, TC-E2-041-05 to TC-E2-041-10 |

### 19. Out of scope

- The registry half of the legacy story: the change checklist on the package version, the load checks and scenarios, the four-eyes approval, the effect counts, the valid-from promotion, the rollback and the change report itself (RWB-P7-E2041-APP).
- The rule package registry tables `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the approval records and the decision log entry table (P7 rwb-decision; ASM-0069).
- The five consumed rwb-decision operations and the authorise operation as provided operations; this story consumes and fakes them.
- The reference table checklist fields and their report (RWB-E1-043); this story covers rule package versions only. The FSD A2.16 examples use a reference-data version and status while this story keeps the rule package scope of the legacy key, the WP title and the test cases (GAP-0719; ASM-1266).
- The load, approval and rollback mechanics of a package version as built (RWB-E1-073) and the rule package rows themselves.
- The rules and parameters screen SCR-39 (Epic 8) and the QA sample against the package version applied (FEAT-ADM-08, Epic 8).
- The decision log store, its read operation and its chain check (RWB-E1-008, RWB-E1-027, JOB-14).
- The cross-service journey harness and its evidence (RWB-ITG-E2041-ITG).
- Deployment of this capability: the Helm values, the event subscription, the topics, the dashboards and the runbook. No deployment story is split from this legacy key, so the platform and DevOps stories of wave 2 carry them.
