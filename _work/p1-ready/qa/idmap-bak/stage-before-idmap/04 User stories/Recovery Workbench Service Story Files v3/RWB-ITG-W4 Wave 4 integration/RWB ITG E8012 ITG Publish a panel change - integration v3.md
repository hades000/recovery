# RWB-ITG-E8012-ITG Publish a panel change

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E8012-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E8012-ITG-16); the squad sizes the story at refinement |
| Depends on (build) | RWB-P4-E8012-APP (build not done yet) |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | RWB-P4-E8012-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-012 as the wave 4 integration proof of the panel change, driven through the versioned reference load of rwb-case, the rule version and its four-eyes approval in rwb-decision and the panel read of rwb-partner, with the decision record read back and the effective date asserted on both sides of the date; the build of the change, its effective dating and the reference data is RWB-P4-E8012-APP with RWB-S9-E8012-APP and its CON story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E8012-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; finishing pass.

### 1. Story

As a **partner and agency manager**, I want **a partner panel change to be published with its effective date, through the versioned reference row of rwb-case and the approved rule version of rwb-decision, with the partner read returning the old panel status before the date and the new one from the date, proved end to end against the owners' real contracts**, so that **access, limits and rules change without a code release, and no change takes effect unapproved or unrecorded**.

This story builds the wave 4 integration harness and its evidence for this feature, and nothing else. The panel change, its effective dating, the approval and the versioned reference data are built by P4 rwb-access and S9 rwb-partner in RWB-S9-E8012-APP and its CON story; the app story of the same legacy key that this harness swaps in is RWB-P4-E8012-APP, and that is the integration dependency in the metadata above. The versioned reference data is carried by P3 rwb-case under the default ruling that puts parameters and reference data with rwb-case, and the rule versions are carried by P7 rwb-decision under the default ruling that puts the rule package registry with rwb-decision. The harness owns no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A panel change is the one administrative act that moves access, limits and rules at once. The legacy story is written against the release: the panel status of a partner, its fee schedule and the rule version that reads them must be changed without a code release (FEAT-ADM-07). If the effective date is not carried by the data, every service reads the change the moment the row is written, cases that were decided under the old panel are re-read under the new one, and nobody can say which version was in force on which date.

The thin sources put four obligations on the change. Every versioned table carries its valid from and valid to dates, its author and its approver (REQ-DRI-011). Roles, teams, queues, queue membership and capacity are held as versioned reference data and change without a code release (REQ-CWC-006). The limit, the rule version and the approver are written to the decision log with every approval (REQ-APD-009). A new rule version applies to decisions taken from its effective date, while open cases keep the version they were decided under (R-UNI-38). A partner panel exit recalls every open case held by that partner (R-UNI-26, REQ-S9-006), which is why the panel status the change publishes is asserted through the partner read and never through the screen that wrote it, and no action proceeds when its decision record cannot be written (R-UNI-39). Every partner type is managed on the same six points, selection and contract and fees among them (REQ-S9-001), so a panel change is a change to a contract record and not to a display.

What is not proved today is the join between the three owners: the reference row is loaded in rwb-case, the rule version is created and approved in rwb-decision, and the effect is visible in rwb-partner. This harness proves that join on one date: the row and the version are loaded and approved through the owners' own operations, one decision record carries the code, the rule id, the rule version and the approver, and the partner read answers the old panel status before the effective date and the new one from it, with the date taken from the fixture and never from code.

Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The reference data is rwb-case's and the rule version is rwb-decision's, so the harness writes nothing itself: it drives the owners' operations and reads the effect back. The decision record is written by the service that takes the decision, through the local decision-record library on `rwb.decision-record.v1` (DP-03), and confirmed by the central ledger in rwb-decision. Where a screen would compose these calls the path is the gateway-bff composite route (DP-19), which is P4's screen path and not this harness.

### 3. Preconditions

- The published contracts of P7 rwb-decision (rule versions, the approval, the decision log, the rule package event), P3 rwb-case (the versioned reference load and the list read), S9 rwb-partner (the panel read) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The rights are in force for the run: Rules and parameters C to create the rule version and load the reference row, Rules and parameters A to approve it. The legacy section names RW-COE as the holder of C and RW-RISK as the holder of A, and the author cannot approve; the harness holds no business right of its own and drives the run as synthetic callers with those right sets.
- The panel and fee schedule reference row, its valid from and valid to dates, its author and approver, the rule version key, the effective date the run uses and the synthetic panel and partner keys are held in the fixture as data. No business date, decision code or panel status value is written in code.
- RWB-P4-E8012-APP owns the panel change, its effective dating and the versioned reference data on the P4 side, and RWB-S9-E8012-APP with its CON story owns the panel and the partner side; until they land, the stub set of §12.8 stands in for their effect and the run is reported as a stub pass.
- The panel and fee schedule as data is FEAT-PRM-02, held as versioned reference data by S9 and loaded through P3's reference contract; this story asserts the load and the read-back and builds none of it.
- The harness environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the effective date the run uses, the shape of the panel reference row, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0478; ASM-0670).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P4-E8012-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: the synthetic panel and partner keys, the panel and fee schedule reference row with its valid from and valid to dates, its author and approver, the rule version key, and the effective date the run uses. The date and every key come from the fixture; on Day 1 the stubs of §12.8 return the same records.
2. Harness: reads `GET /api/recovery/access/v1/me/session` as the caller that will create the change and asserts Rules and parameters C and not A, then as the approver and asserts Rules and parameters A, then as a caller with no Recovery Workbench role.
3. Harness: reads `GET /api/recovery/partner/v1/partners` and asserts the panel status the partner carries before the change, together with partner_code, partner_type and contract_end (DF-PRT-001 to DF-PRT-007).
4. Harness: loads the versioned panel and fee schedule reference row through `POST /api/recovery/case/v1/admin/reference-loads` with the fixture file and the load key, and asserts the answer carries the row, its valid from and valid to dates, its author and its approver.
5. Harness: reads `GET /api/recovery/case/v1/admin/lists/{listCode}` and asserts the loaded row with its effective dates, so the version is proved to exist in rwb-case and not only in the load answer.
6. Harness: creates the rule version through `POST /api/recovery/decision/v1/admin/rule-versions` as the caller holding Rules and parameters C, and asserts the answer carries the version id and its state.
7. Harness: approves the rule version through `POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` as the approver holding Rules and parameters A, and asserts one approved version with its approver.
8. Harness: submits the same approval a second time and asserts the answer is refused and one approved version remains, so a repeated click is never a second approval.
9. Harness: reads `GET /api/recovery/decision/v1/decision-log?ruleId={ruleId}&from={from}` and asserts one record for the change with its decision_code, rule_id, rule_version and approver (DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015).
10. Harness: counts one `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, asserts the central ledger in rwb-decision confirmed it, replays the event and asserts the decision log still holds one record for the change.
11. Harness: observes `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` and records the version it names against the version id approved in step 7.
12. Harness: reads `GET /api/recovery/partner/v1/partners` before the effective date and asserts the old panel status, then at and after the effective date and asserts the panel status the change carries, on both sides of the date the fixture names.
13. Harness: forces the local decision-record library to fail for the change and asserts the publish stops with MSG-P7-003, the reference version stays unapproved and the partner read still returns the old panel status.
14. Harness: calls the approve operation as a caller holding Rules and parameters C and not A and asserts 403 with MSG-P4-002 and no state change, then as a caller with no Recovery Workbench role and asserts MSG-P4-001.
15. Harness: writes one run report keyed by story and by the reference load key, naming the contract version of each hop, whether the hop was a stub or the owner, the reference row and its effective dates, the rule version and its approver, the decision record, the panel status on both sides of the effective date, and the pass or fail gate.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow, or a contract version moves under the run | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E8-012-01-ITG (ITG AC1) | ITG AC1 |
| X2 | The reference load answers without a valid from or valid to date, an author or an approver | The run fails on AC2 and the report names the load key and the missing field; the harness never supplies an effective date or an approver of its own | None | TC-E8-012-01-ITG (ITG AC2) | ITG AC2 |
| X3 | The partner read returns the new panel status before the effective date, or the old one from it | The run fails on AC2 and the report names the date read, the status answered and the status expected; the date is taken from the fixture, never from the clock of the machine | None | TC-E8-012-01-ITG (ITG AC2) | ITG AC2 |
| X4 | The rule version is approved and no decision record carries its version, or the central ledger has not confirmed the record | The run fails on AC3 and the report names the version, the record and the missing confirmation; confirmation is never assumed | MSG-P7-003 | TC-E8-012-01-ITG (ITG AC3) | ITG AC3 |
| X5 | The same approval is submitted twice and a second approved version is created | The run fails on AC3 and the report names the two submissions and the version; a repeated click is never a second approval | None | TC-E8-012-01-ITG (ITG AC3) | ITG AC3 |
| X6 | The decision record fails and the reference version is approved, or the partner read moves to the new status | The run fails on AC4 and the report names the approval state and the panel status before and after; nothing changes is asserted, not assumed | MSG-P7-003 (expected) | TC-E8-012-02-ITG and TC-E8-012-04-ITG (ITG AC4) | ITG AC4 |
| X7 | A caller holding Rules and parameters C and not A is allowed to approve, or a caller with no Recovery Workbench role is allowed to act | The run fails on AC5 and the report names the caller's rights, the operation and the answer; a 200 is a failure even when no business data changed | MSG-P4-002 and MSG-P4-001 (expected, and missing) | TC-E8-012-03-ITG (ITG AC5) | ITG AC5 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

The SIT environment and base hosts, the fixture layout, the synthetic panel and partner keys, the reference load key, the stub answer shapes for the seven consumed operations and the panel-change fixture, the effective date the run uses, the shape of the panel reference row, the evidence format and retention, and the pass or fail gate are agreed at the wave 4 entry check and recorded in the harness configuration and the run report header, so that a stub pass is never read as a real pass; none of them is hard-coded in this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P4-E8012-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the effective date the run uses, the shape of the panel reference row, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The reference row and the rule version are proved to be loaded and approved by their owners, the approval is proved to be recorded once, and the change is proved to take effect on its date and nowhere else |
| Estimable | One runner, one stub set, one reference load, one list read-back, one rule version create, one approve, one partner probe, one decision read-back, one event observer and one report |
| Small | Fits in one sprint with its five criteria and four tests |
| Testable | Each criterion runs against the stubs and again against RWB-P4-E8012-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Publish a panel change - wave 4 integration harness

  Background:
    Given the synthetic panel and partner keys and the panel and fee schedule reference row are held in the fixture as data, with its valid from and valid to dates, its author and its approver
    Given the rule version of the change is held in the fixture with its author and approver
    Given the effective date the run uses is taken from the fixture and never from code

  Scenario: AC1 Publish a panel change (legacy RWB-E8-012 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then puts a partner panel change in force with an effective date
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The change is published with its effective date (new, D-RCV-60)
    Given the versioned reference row for the panel and the fee schedule is loaded and approved through the owner's operations with valid from and valid to dates, author and approver
    And the rule version of the change is in force for the effective date the fixture names
    When the partner read is made before the effective date and again from it
    Then the partner read shows the panel status the change carries, the old value before the effective date and the new value from it
    And the effective date used is the one the fixture names, never a date written in code
    And the list read returns the loaded reference row with its effective dates
    And a run whose partner read answers the new status before the date fails, and is never written up as a pass

  Scenario: AC3 The approval and the record (new, D-RCV-60)
    Given a caller holding Rules and parameters C creates the rule version of the change
    When the version is approved through the decision service's approval operation by a caller holding Rules and parameters A
    Then one approved version exists, and the author is not the approver
    And one decision record carries decision_code, rule_id and rule_version with the approver
    And "rwb.decision.DecisionRecorded.v1" is published once on "rwb.decision-record.v1" and confirmed by the central ledger
    And the same approval submitted twice is refused and leaves one approved version
    And a replay of the event changes nothing

  Scenario: AC4 A forced local decision-record failure stops the publish (new, D-RCV-60)
    Given the local decision-record library is forced to fail for the change
    When the change is published through the rule-version approval
    Then the publish stops with "MSG-P7-003"
    And the reference version stays unapproved
    And the partner read still returns the old panel status
    And the reference row and the rule version are unchanged when they are read again

  Scenario: AC5 A caller without the approval right is refused (new, D-RCV-60)
    Given a synthetic caller holding Rules and parameters C and not A
    When the caller approves the rule version through POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then the answer is 403 with "MSG-P4-002"
    And no approved version and no decision record are written
    And a caller holding no Recovery Workbench role is refused with "MSG-P4-001"

  Scenario: AC6 Every business rule is held by its owner and one hop away (new, D-RCV-60)
    Given the owners' operations that hold the rules of section 8 are reachable on their own base
    When the publish runs through the owners' operations
    Then each call is one hop on the owner's base within a 2 s budget
    And the reference data and the rule registry are read from their owners and not copied into the harness
    And a call that leaves the owner's base fails the run

  Scenario: AC7 A consumed call that fails or does not answer fails the run (new, D-RCV-60)
    Given a consumed owner operation is forced to fail or to not answer within its 2 s budget
    When the publish runs through that operation
    Then the run fails with the operation named and is never written up as a pass
    And no partial publish is reported as complete
```

Legacy AC2 (the decision log cannot be written) is built and tested in RWB-P4-E8012-APP, and this story asserts the same failure at the publish through AC4.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A partner panel change is put in force with an effective date, and access, limits and rules change without a code release | FEAT-ADM-07; legacy RWB-E8-012 | AC1; AC2 |
| BR2 | Every versioned table carries its valid from and valid to dates, its author and its approver | REQ-DRI-011 | AC2 |
| BR3 | Roles, teams, queues, queue membership and capacity are held as versioned reference data and change without a code release | REQ-CWC-006 | AC6 |
| BR4 | The limit, the rule version and the approver are written to the decision log with every approval | REQ-APD-009 | AC3 |
| BR5 | A new rule version applies to decisions taken from its effective date; open cases keep the version they were decided under | R-UNI-38 | AC2 |
| BR6 | A partner panel exit recalls every open case held by that partner and re-selects | R-UNI-26; REQ-S9-006 | AC6 |
| BR7 | When the decision log entry cannot be written, the action is blocked and no action proceeds unlogged | R-UNI-39 | AC4 |
| BR8 | Every partner type is managed on the same six points, selection and contract and fees among them | REQ-S9-001 | AC6 |
| BR9 | Every call is one hop on the owner's base with a 2 s budget, the reference data and the rule registry stay with their owners, and the decision record is written through the local decision-record library on the shared topic and confirmed by the central ledger | DP-03, DP-06, DP-11, DP-13; ADR-020, ADR-022 | AC2; AC3; AC6 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in the owning services, and BR5 to BR7 are the effective-dating, recall and no-unlogged-action context the change is proved against, not states the harness sets. BR3, BR6 and BR8 are the exception: for them AC6 checks only that they are held by their owners and reached on the owner's base, and the harness does not assert their behaviour.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | the approver approves the version | a different person from the author approves (four-eyes) | APPROVED |
| APPROVED | its effective date arrives | the version reaches the valid from date it carries | IN_FORCE |
| IN_FORCE | a later version is approved | the newer version reaches its effective date | SUPERSEDED |
| IN_FORCE | a rollback call is made | the rollback is the owner's decision, read here and never made here | ROLLED_BACK |
| LOADED | the approver refuses the version | the author cannot approve, and a refusal is recorded | REFUSED |

LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are the rule version states of the rule package registry (Temporal and Drools design slide 15), and they are read from the owners' answers and never set by the harness. The panel status the change carries is the classification of DF-PRT-005: the harness reads the old value before the effective date and the new value from it and never writes either. The reference row's own approval state is P3's and is asserted only through the load answer and the list read-back, because no source names that state vocabulary. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Holds Rules and parameters C: creates the rule version of the change and loads the versioned reference row |
| RW-RISK, risk and model risk officer | Holds Rules and parameters A: approves the rule version, and the author cannot approve |
| Partner and agency manager | The role the legacy story is written for, and the role that decides the panel change; the harness reads the effect of that decision on the partner side |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P3 answers the reference load and the list read-back, P7 creates and approves the rule version, holds the ledger and publishes the rule package event, S9 answers the panel read, P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the approval is RW-RISK's under four-eyes, and authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end | Read through the rwb-partner contract, before and after the effective date |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-034 to DF-REF-038 | role | role_code, role_class | Read through the rwb-access session answer, for the caller's rights |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and the legacy section names these four entities with these ranges. The reference row and the reference version of the panel and fee schedule are P3's, in rwb-case; the legacy section names no field ID for them, so none is cited here. The partner and its panel status are S9's, the decision log and the rule rows are P7's, and the role behind a right is P4's; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-versions` | P7 rwb-decision | Creates the rule version the change is published under; the path is the one the legacy section names, re-based on the owner's base (AC1, AC3) |
| POST | `/api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` | P7 rwb-decision | The four-eyes approval of that version, and the refusal on a second submission (AC3, AC4, AC5) |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | Loads the versioned panel and fee schedule reference row with its valid from date, author and approver (AC1, AC2) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | Reads the panel list back with its effective dates (AC2) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The panel status the change carries, before the effective date and from it (AC2, AC4) |
| GET | `/api/recovery/decision/v1/decision-log?ruleId={ruleId}&from={from}` | P7 rwb-decision | The change records of the run, with decision_code, rule_id and rule_version (AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's rights before a create, an approve or a refusal (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The contract version this story builds against is the /v1 base; no numeric contract version is specified in the source documents (DOR-RWB-ITG-E8012-ITG-23). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The Ownership Map publishes no panel-change operation of its own, so the harness publishes the change through the versioned reference row and the rule version, and proves the effect through the partner read; a hop that has no owner in the map is never invented. The two rule-version paths are owned by P7 and the two reference paths by P3 under the default ruling that puts reference data with rwb-case (ASM-0040, ASM-0041); the panel read is S9's and the session is P4's.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | The service that takes the decision, through the local decision-record library (DP-03) | Proves the change was recorded with its rule version and confirmed by the central ledger, and stays one record after a replay (AC3, AC4) |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Records the version the rule registry put in force against the version id approved in the run (AC3) |

Both events are cited from the Arch v5 extract: `DecisionRecorded` is row 08 of slide 42 on `rwb.decision-record.v1`, and `RulePackageInForce` is row 30 of slide 43 on `rwb.decision.events.v1` with P7 as producer, which is why the second is kept and not left out. The harness subscribes to both topics under one consumer group of its own, counts publications and replays each event once; its consumers of record are rwb-decision and rwb-reporting for the first, and rwb-case, rwb-valuation, rwb-treatment and rwb-payment for the second, and their effect is observed by count because no consumer exposes an operation this story consumes.

#### 12.5 Workflows and activities

None added. The harness observes ApprovalWorkflow, the workflow-kit template that runs on the task queue `rwb-decision` in the `rwb-recovery` namespace and carries the four-eyes approval of the rule version; it is stated here as observed and not built. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. JOB-20, rule promotion at 00:01, is a Schedule of rwb-decision (Arch v5 slide 44) and is observed only; the harness sets no overlap policy and no catch-up window, and it starts nothing by cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); partner and partner_user are S9's, reference row and reference version are P3's, and rule_package, rule_package_version and decision_log_entry are P7's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-decision (rule version create) | `POST /admin/rule-versions` | Creates a version with the id and state the contract allows and returns it with the version id the run then approves |
| Stub for rwb-decision (rule version approve) | `POST /admin/rule-versions/{versionId}/approve` | Approves the version once with its approver, refuses a second submission of the same approval, and answers 403 with MSG-P4-002 for a caller without Rules and parameters A |
| Stub for rwb-case (reference load) | `POST /admin/reference-loads` | Accepts the fixture file and returns the row with its valid from and valid to dates, author and approver; a load without one of them answers the empty field for X2 |
| Stub for rwb-case (list read) | `GET /admin/lists/{listCode}` | Returns the loaded panel list with its effective dates, and the rejection state after a forced decision-record failure |
| Stub for rwb-partner | `GET /partners` | Returns the synthetic partner with partner_code, partner_type, contract_end and the old panel status before the effective date and the new one from it, with the date taken from the fixture |
| Stub for rwb-decision (decision log) | `GET /decision-log?ruleId={ruleId}&from={from}` | One record for the change with decision_code, rule_id, rule_version and approver, and the central ledger confirmation; none after a forced failure |
| Stub for rwb-access | `GET /me/session` | Allows Rules and parameters C and not A for the creator, A for the approver, and refuses a caller holding C and not A on the approve with 403 and MSG-P4-002, and a caller with no Recovery Workbench role with MSG-P4-001 |
| Panel-change fixture | The reference row, the rule version key and the effective date | The panel and fee schedule row with its valid from and valid to dates, author and approver, the rule version key, the synthetic panel and partner keys and the effective date, all as data |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the effective date the run uses, the shape of the panel reference row, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0478; ASM-0670).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.decision.DecisionRecorded.v1` and `rwb.decision.RulePackageInForce.v1`, counted and replayed once |
| Temporal | None added; ApprovalWorkflow on `rwb-decision` observed, and JOB-20 observed as its Schedule |
| File | One: the reference load is a multipart upload and the harness holds the fixture file it posts, on the rwb-case contract |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies the table adds, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON and RWB-PLT-N001-CON, are platform contract stories delivered in the platform wave and are recorded here and not repeated in the metadata H field of this story, which stays None; DP-13 adds none. The C dependency RWB-P3-E1042-CON is built against its published contract and its fake and never blocks. The only blocking dependency is the I story RWB-P4-E8012-APP, which replaces its stub, so the story is Day 1; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ChangeRunner | Job | Runs the five owned criteria in order for one change and holds the run lock |
| SessionProbe | Service | Reads the caller's rights, and names the right each operation needs |
| ReferenceLoadDriver | Service | Posts the fixture file to the reference load, reads the panel list back and asserts the effective dates, the author and the approver |
| RuleVersionDriver | Service | Creates the rule version, drives the four-eyes approval, retries the same approval and asserts the refusal |
| PanelProbe | Service | Reads the partner and asserts the panel status before the effective date and from it, on the date the fixture names |
| DecisionReadBack | Service | Reads the decision log and asserts one record with its code, rule id, rule version and approver, with the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.decision-record.v1` and `rwb.decision.events.v1`, counts publications and replays each event once |
| StubSet | Fake | The seven stubs and the panel-change fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report keyed by story and by the reference load key, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-P4-E8012-APP lands, on the synthetic panel and partner keys, the panel and fee schedule reference row with its valid from and valid to dates, author and approver, the rule version key and the effective date, all held in the fixture as data. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the stub answer shapes, the effective date the run uses, the shape of the panel reference row, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0478; ASM-0670).

**Build steps**

1. Generate the seven stubs and the panel-change fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the SessionProbe and prove the three right sets of AC5: C and not A, A, and no Recovery Workbench role.
3. Build the ReferenceLoadDriver for AC2: post the fixture file, read the panel list back, and fail the run where a valid from date, a valid to date, an author or an approver is missing (X2).
4. Build the RuleVersionDriver for AC3 against both operations, and prove one approved version with the author not the approver, and a refusal on the same approval submitted twice (X5).
5. Add the DecisionReadBack for AC3: one record with its code, rule id, rule version and approver, and the ledger confirmation before the publish is reported as recorded (X4).
6. Add the EventObserver for AC3: one publication of the decision record, one of the rule package in force, a replay that changes nothing, and one record after the replay.
7. Add the PanelProbe and the effective-date assertion for AC2, with the date read from the fixture, and fail a run whose partner read answers the new status before the date (X3).
8. Add the forced decision-record failure for AC4 through the load answer, the rule version state and the partner read, so nothing changes is asserted and not assumed (X6), then the refused approve and the no-role refusal for AC5 (X7), then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-P4-E8012-APP lands.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P4-E8012-APP when it lands, and the wave entry check holds a run report keyed by story and by the reference load key.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. The legacy section carries these five messages for the feature, so none is invented here: MSG-GEN-001 with the missing field when a load or a create is made short of a required value, MSG-P4-002 with the refused approve for a caller holding C and not A, MSG-P4-001 for a caller with no Recovery Workbench role, MSG-P7-003 when the decision record cannot be written and nothing changes, and MSG-P4-004 as the warning that every action is recorded while emergency access is on, which the run reads and does not assert as a state.

### 15. Screens and states

The harness renders no screen: it observes the owners' operations and writes a report. The legacy section names SCR-39 Rules and parameters and SCR-41 Delegation of authority, which belong to P4 and its CON story; the harness neither builds nor reads them, and it asserts their data through the reference load, the rule version and the partner read.

| State | Read through | What the run asserts |
|---|---|---|
| The panel status of DF-PRT-005 | rwb-partner partner read | The old value before the effective date and the new value the change carries from it, with the date taken from the fixture |
| LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED (rule version state) | rwb-decision rule version operations and the decision log | One approved version with its approver, a refusal on a repeated approval, and the version the rule package event puts in force |
| Empty (SCR-39) | P4 screen: no version is listed for the package yet, shown as an empty list with a total of 0 and no error | Nothing: the harness renders and reads no screen |
| Loading (SCR-39) | Not specified in the source documents (CG-ALL-1251) | Not specified in the source documents (CG-ALL-1251) |
| Error (SCR-39) | P4 screen: a refusal shows MSG-P7-002, MSG-P4-002, MSG-P3-022 or MSG-GEN-004 with nothing changed; a failed decision record shows MSG-P7-003 and the version stays LOADED | Nothing on the screen: the harness renders and reads no screen |
| No access (SCR-39) | P4 screen: a role without the letter is refused with MSG-P4-002, nothing is changed and the record reference is shown | Nothing on the screen: the harness renders and reads no screen |
| The approval state of the reference version | rwb-case reference load answer and list read-back | The version is loaded and approved before the publish, and stays unapproved after a forced decision-record failure |
| The decision record of the change | rwb-decision decision log | One record with its decision code, rule id, rule version and approver, confirmed by the central ledger |
| The caller's rights | rwb-access session answer | Rules and parameters C for the creator, A for the approver, and the refusal of C without A and of no Recovery Workbench role |
| Empty (SCR-41) | P4 screen: no version is loaded for the table, shown as the empty version list | Nothing: the harness renders and reads no screen |
| Loading (SCR-41) | Not specified in the source documents (CG-ALL-1252) | Not specified in the source documents (CG-ALL-1252) |
| Error (SCR-41) | P4 screen: a refusal shows MSG-P1-002 for a refused file, MSG-P7-002 for the loader or MSG-P4-002 for a role without the letter, each with nothing changed | Nothing on the screen: the harness renders and reads no screen |
| No access (SCR-41) | P4 screen: a role without the letter is refused with MSG-P4-002 and nothing is changed | Nothing on the screen: the harness renders and reads no screen |

The environment, layout and retention of the run report are Not specified in the source documents (GAP-0478; ASM-0670).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-012-01-ITG | AC1 (legacy); ITG AC1 | End to end | One synthetic panel, one versioned panel and fee schedule reference row and one rule version, with the effective date from the fixture |
| TC-E8-012-02-ITG | Legacy AC2 not recorded stays with RWB-P4-E8012-APP; ITG AC4 | Integration | The decision-record library forced to fail on the publish, with the reference version and the partner read before and after |
| TC-E8-012-03-ITG | Access; ITG AC5 | Component | A caller holding Rules and parameters C and not A, and a caller with no Recovery Workbench role |
| TC-E8-012-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the reference load and the partner read before and after |
| TC-E8-012-05-ITG | ITG AC3 | Integration | A rule version created by a caller holding Rules and parameters C and approved by a caller holding Rules and parameters A, with one decision record and the central ledger confirmation |
| TC-E8-012-06-ITG | ITG AC6 (BR3, BR6, BR8, BR9) | Boundary | Not specified in the source documents (NEWAC-RWB-ITG-E8012-ITG-AC6) |
| TC-E8-012-07-ITG | ITG AC7 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E8012-ITG-AC7) |

The Covers column names the legacy test case the copy derives from and the ITG criterion it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2, the forced decision-log failure, stays with RWB-P4-E8012-APP and is asserted here at the publish through AC4.

### 17. Guardrails

- No business value in code: the panel and fee schedule row, its effective dates, the author and approver, the synthetic keys, the rule version key, the effective date, the panel status values and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the owner's contract or `v_ace_*` views: this run reads no ACE data at all, and the partner, reference, decision and session values are read only through their owners' contracts (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The effective date is read from the fixture and never from the clock or from code, and the partner read is asserted on both sides of it.
- The harness never approves on behalf of the author, and it never supplies an approver, an effective date or a panel status of its own.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E8-012 Publish a panel change | Recovery Workbench User Stories Epics 3 to 8 v4, lines 15579 to 15660 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 15598 to 15602 | Section 7, AC1, marked (legacy RWB-E8-012 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E8-012-02 | The same, lines 15604 to 15607 and 15655 | AC4 asserts the same failure here; the legacy AC stays with RWB-P4-E8012-APP (section 19) |
| Legacy test cases TC-E8-012-01 to TC-E8-012-04 | The same, lines 15654 to 15657 | Copied as -ITG in section 16 |
| FEAT-ADM-07 Publish a panel change | Epics 3 to 8 Specification v3, line 180 | Sections 1, 2 and 3 |
| FEAT-PRM-02 Hold the partner panel and fee schedule as data | Epics 3 to 8 Specification v3, line 135 | Sections 2 and 3: the versioned reference data is read and loaded, not built here |
| REQ-DRI-011, REQ-CWC-006, REQ-APD-009 | Business Requirements Program v5, lines 269, 153 and 279 | Section 8, BR2, BR3 and BR4; section 7, AC2 and AC3 |
| REQ-S9-001 and REQ-S9-006 | Business Requirements Program v5, lines 430 and 435 | Section 8, BR6 and BR8 |
| R-UNI-26, R-UNI-38 and R-UNI-39 | Business Rules and Routing Logic v4, lines 430, 442 and 443 | Sections 2, 8 and 9 |
| P7 rwb-decision contract, the approvals and the rule registry | Architecture v5 slides 14, 27 and 41; slide 43 row 30 | Sections 2, 12.2, 12.4 and 12.5 |
| P3 rwb-case reference data, S9 rwb-partner panel, P4 rwb-access session | Architecture v5 slides 14, 17, 20 and 41 | Sections 2, 11 and 12.2 |
| ApprovalWorkflow on `rwb-decision` and JOB-20 at 00:01 | Architecture v5 slides 14, 27 and 44 | Sections 12.5 and 12.6 |
| Rule version states and four-eyes approval | Temporal and Drools design slides 13, 15 and 25 | Sections 8, 9 and 12.5 |
| DF-PRT-001 to DF-PRT-007, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-REF-034 to DF-REF-038 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-06, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-017, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 8 and 12: the rule registry with rwb-decision, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| Default rulings: reference data to P3, rule package registry to P7 | Template and Rules v1 §R3; Ownership Map v1 (ASM-0040, ASM-0041) | Sections 1, 2 and 12.2 |

### 19. Out of scope

- RWB-P4-E8012-APP: the panel change, its effective dating, the approval and the versioned reference data on the P4 side.
- RWB-S9-E8012-APP and RWB-S9-E8012-CON: the panel, the partner side of the panel change and the partner-portal reads.
- FEAT-PRM-02: the panel, the fee schedule and the service levels as versioned reference data, and the reference-data screens.
- Rule authoring, testing and rollback (FEAT-ADM-02, FEAT-ADM-06) and the move of an approval limit (FEAT-ADM-03): the harness approves one version and rolls nothing back.
- SCR-39 Rules and parameters and SCR-41 Delegation of authority, which are P4's screens and its CON story's.
- The partner gateway and the FAPI 2.0 profile: partner users reach the portal through the DMZ gateway, which is the edge stories' own scope.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness runs in the test environment only.
