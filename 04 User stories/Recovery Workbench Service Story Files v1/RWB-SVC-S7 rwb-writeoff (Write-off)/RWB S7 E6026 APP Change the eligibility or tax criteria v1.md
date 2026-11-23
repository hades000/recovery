# RWB-S7-E6026-APP Change the eligibility or tax criteria

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6026-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the criteria-change slice of RWB-E6-026 in rwb-writeoff (FEAT-WOF-14). The three legacy criteria are kept word for word with their origin tag; the change becomes the acceptance and pinning of a published criteria version of the WO package read from rwb-decision (P7), recorded on the decision record through the local library before any scan outcome (DP-03), applied uniformly to a cut-off under R-WO-01 and its absence held under R-WO-03 and R-WO-04, reached from SCR-27 through the gateway-bff composite route (DP-19) on the target base `/api/recovery/writeoff/v1` (DP-13). No screen, no operation and no write right for the change is published for this service, and `tax_criteria_version` has no table, owner or key in any source. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst**, I want **the Workbench to let the center of excellence change the criteria as a versioned rule load**, so that **write-offs follow the criteria and the committee's decision**.

This is the criteria-change slice of legacy RWB-E6-026. It owns:

- the three legacy criteria of the key (AC1 to AC3), copied verbatim with their origin tag, and the messages and the screen state they depend on;
- the acceptance of a published criteria version of the WO package — the eligibility rule on both tracks, the hold condition of R-WO-03 and the tax criteria with `tax_criteria_version` — read on the package read of rwb-decision (P7) at its version, and the refusal of an incomplete version;
- one pinned version per cut-off, so every open case of a monthly scan is tested against one version of the criteria under R-WO-01, and a version published mid-run does not split a run (FSD S7 A2.14; TSD S7 T4);
- the hold and the restart of the scan when no version is in force, R-WO-03 to `SCAN_HELD` with MSG-S7-001 and R-WO-04 back to `SCAN_DUE`, with nothing written (FSD S7 A2.14.3.1; TSD S7 T4);
- the local decision record of the acceptance and of every outcome, written through RWB-PLT-E1027-CON before the outcome exists (DP-03), carrying the rule ID, the package version and `tax_criteria_version`;
- the criteria-version state of the scan on SCR-27 Write-off proposal, read only, behind the gateway-bff composite route (DP-19);
- the behaviour behind the criteria-version parameter of API-S7-001 `POST /write-off-scans` on base `/api/recovery/writeoff/v1` (DP-13).

It does not own: the published shape of the scan operation and of the criteria-version element, the consumed rows, the error set and the fakes, which are RWB-S7-E6026-CON; the authoring, validation, approval and rollback of the package itself, which is the rule authoring story RWB-P7-E1073 in rwb-decision (ASM-5105); the eligibility test of the population and the `JOB-16` Schedule, which are the scan story of RWB-E6-013; the tax-criteria test of the population and the remittance path, which are RWB-S7-E6014-APP; the pack, the committee, the posting, the Finance feed, the reconciliation, the exception loop and the closure by retention (FEAT-WOF-03 to 13); the case of record and its route states, which are rwb-case (P3); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: the Workbench lets the center of excellence change the criteria as a versioned rule load (FSD S7 A2.14.1), because write-off populations are assembled by hand each month (FSD S7 A1.3), and the result is measured on the decision log and the Workbench records against "write-off packs accepted first time", rising each month, reviewed monthly (FSD S7 A2.14.1). The requirement is REQ-S7-001, "Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks" (FSD S7 Requirements served). What D-RCV-60 changes is where a criteria value lives and who may move it.

- **A criterion is a versioned package fact, not a row of this service.** BR-S7-014 forbids a changeable value in code, VR-S7-014-1 and R-WO-03 test `tax_criteria_version`, and the package is governed in rwb-decision (P7); the "versioned rule load" of the legacy story is therefore a published version this service accepts and pins, never a value it stores (ASM-5104).
- **The change is authored elsewhere and approved there.** Rule authoring, test scenarios, approval and rollback are the rwb-decision capability (RWB-P7-E1073); S7 declares no second authoring path, because two authors of one rule set is the coupling DP-04 removes (ASM-5105).
- **Access is the open point.** TSD S7 T6.1 gives RW-COE right R on "Write-off and posting" while FSD S7 A2.14.3.3 makes the center of excellence analyst the primary role of the change; the change right is therefore read as held on the rwb-decision capability area and this service performs no authoring and no approval (ASM-5107; GAP-3043).
- **One version per run is the point of the change.** A scan that mixed two versions of the eligibility rule could not be defended to the committee, so the version is pinned at the start of a cut-off and recorded with every outcome (ASM-5104).
- **The case stays with rwb-case**, and the population and the move are answered on the workflow boundary; this service reads no `recovery_case` row (ASM-5110).
- **No new path is invented.** TSD S7 T-A.1 publishes two operations for this service and none of them changes the criteria, so the acceptance is a workflow step and the only published surface it touches is the criteria-version parameter of the scan (ASM-5108; GAP-3043).

No business value moves: the criteria set, `tax_criteria_version`, the states and the rule rows stay values of the rule package and of reference data, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6026-CON is published: the scan operation with its criteria-version element, the consumed rows, the criteria-version state, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-decision package read is available on the `rwb-decision` queue as a Temporal activity, or on its published REST contract if the owner publishes one, and its fake answers the WO package at a version with R-WO-01, R-WO-03, R-WO-04 and `tax_criteria_version`; the operation name, the call type and the home of the version are Not specified in the source documents (GAP-3043; ASM-5104, ASM-5108).
- The rwb-case population and the case-move answer are available on the workflow boundary: the case reference, the case number, the product group, the balance, the account link and the state in, and the moves `POPULATION_PROPOSED` and `SCAN_HELD` out. No REST line from S7 to P3 exists in the connection matrix (GAP-3043; ASM-5110).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service with the columns of TSD S7 T3.1 and the standard record columns of T3.0; this story adds no table, no column and no migration. There is no column and no table for the criteria version, and none is created (GAP-3043; ASM-5104).
- A criteria version to accept exists in rwb-decision at Draft or later; the FSD is "In review" and no sign-off row is filled, so the version in force is a working read of the package (ASM-5104, ASM-5105).
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; this story stays at Draft (realignment v1) until the wave 4 contract freeze (ASM-5111).

### 4. Flow

1. The center of excellence publishes a new version of the WO criteria in rwb-decision: the eligibility rule on both tracks, the hold condition, the tax criteria and their version (FSD S7 A2.14.2 step 1; ASM-5105).
2. The case router of rwb-case, or the monthly scan of the sibling story, starts the criteria step of `WriteOffWorkflow` on queue `rwb-writeoff` in namespace `rwb-recovery` for the cut-off date (Temporal and Drools Design slides 5 and 13; context pack workflow row).
3. `CriteriaVersionReader` reads the version in force on the package read, one hop, with its rule set, its reference data and `tax_criteria_version` (ASM-5104, ASM-5108).
4. `CriteriaVersionValidator` checks the version is complete for this service: it carries R-WO-01 and R-WO-03 and R-WO-04, the eligibility rule on both tracks and the tax criteria with a version; a version missing any of them is refused and nothing is pinned (FSD S7 VR-S7-014-1; ASM-5104).
5. Where no version is in force or the version is refused, R-WO-03 holds the scan: the case stays at `SCAN_HELD`, nothing is written, and SCR-27 shows MSG-S7-001 (legacy AC1; FSD S7 A2.14.3.1).
6. On acceptance, `CriteriaDecisionRecordWriter` writes one decision record for the acceptance — the package, the version, the rule set it carries and the cut-off it is pinned to — **before any outcome exists**, through the local library (DP-03; legacy AC1 and AC3).
7. The accepted version is pinned to the cut-off: `CriteriaPin` keeps the version, its hash and the package reference for the length of the run, so every case of the cut-off is tested against one version whatever is published while the run lasts (ASM-5104).
8. `CriteriaEvaluator` runs R-WO-01 for each open case with the pinned version: the eligibility test is the scan story's and the tax-criteria test is RWB-S7-E6014-APP's; this step supplies the version both run under and records it with each outcome (legacy AC2).
9. `CriteriaOutcomeWriter` records the version on each outcome in one transaction with the `write_off` row the tax-criteria step writes, and sets nothing on the row that is another story's: `tax_criteria_met` (DF-FIN-014) stays the tax-criteria step's write and this story adds no column (TSD S7 T3.1).
10. `CaseMoveAnswer` answers rwb-case for the move the rule names, `POPULATION_PROPOSED` on R-WO-01 and `SCAN_HELD` on R-WO-03; rwb-case writes the `recovery_case` row and this service writes neither the row nor the state (ASM-5110).
11. R-WO-04 restarts the scan for the cut-off once a version is published and the ALS extract is complete, and the restart re-reads the version and records the change of version on the record (TSD S7 T4; Business Rules and Routing Logic v4 row R-WO-04).
12. A repeated trigger for the same cut-off and version writes no second record and no second pin, and the same `Idempotency-Key` on the scan answers the scan it ran; the repeat is counted (TSD S7 T-A.2).
13. SCR-27 Write-off proposal shows the version in force, the cut-off it is pinned to and the state of the run, read only, next to the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no pin, no version on an outcome and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E6-026-03 |
| X2 | The role does not hold the right the operation declares | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-026-04 |
| X3 | No criteria version is in force, or the published version is incomplete | R-WO-03 holds the scan at `SCAN_HELD`; nothing is pinned and nothing is written; the run resumes on R-WO-04 | MSG-S7-001 | AC1, AC2, X5 |
| X4 | A version is published while a cut-off is running | The running cut-off keeps its pinned version; the new version is accepted for the next cut-off and the change is recorded | None | AC1, AC2 |
| X5 | The package read does not answer inside its budget, or its breaker is open | The step retries on the workflow's own schedule; nothing is pinned and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, X3 |
| X6 | The case is outside the population of the cut-off, or it has left it since it was read | 409 and nothing is written for that case; a case that has moved is not re-tested | None | AC2 |
| X7 | A repeated trigger for the same cut-off and version, or the same `Idempotency-Key` twice | One record, one pin and one answer per case; the repeat is counted and the key answers the scan that exists | None | AC1 |
| X8 | A component, a statement or a test reads a `v_ace_*` view, a `recovery_case` row or another service's schema, or writes a criteria value in code | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR4, BR5 |

X1, X2 and X3 are the legacy paths of this key carried onto the slice, X4 to X7 are the paths a versioned package and the once-per-cut-off trigger add, and X8 is the decoupling guard. The deviation codes X1 to X7 of the DEV route set are codes of the rule package and are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6026-CON, the rwb-decision package fake, the decision-record stub and the workflow-boundary fake, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity names, the decision code of the acceptance and the shape of the pin are this story's choice; the rules, the messages, the screen state, the operation and the table columns are fixed |
| Valuable | A criteria change reaches every open case of a cut-off as one version with the version recorded, so the population is provable to the committee and to audit |
| Estimable | One workflow step, one reader, one validator, one pin, one record write, one outcome writer, one case-move answer, one client and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic package at two versions and a synthetic population, plus the hold, the incomplete version and the failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Change the eligibility or tax criteria

  Background:
    Given case "RC-2026-000914" is one of 120 cases in state "SCAN_DUE" on the population of the monthly write-off scan
    Given the WO rule package is in force at its version and carries R-WO-01, R-WO-03, R-WO-04 and the tax criteria
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Change the eligibility or tax criteria (legacy RWB-E6-026 AC1)
    Given the rwb-decision contract mock returns the WO criteria version "2026-11" with R-WO-01, R-WO-03, R-WO-04 and tax_criteria_version "2026-11"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the center of excellence change the criteria as a versioned rule load
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-01 (legacy RWB-E6-026 AC2)
    Given the rwb-case contract mock returns case "RC-2026-000914" in state "SCAN_DUE" and accepts the move "POPULATION_PROPOSED"
    Given the rwb-decision contract mock returns the WO criteria version "2026-11" pinned to the cut-off
    Given a case in state SCAN_DUE
    When monthly scan started
    Then test every open case against the eligibility rule on both tracks and the tax criteria
    Then the case moves to POPULATION_PROPOSED

  Scenario: AC3 Not recorded (legacy RWB-E6-026 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E6-026 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `the user acts on the screen`, `monthly scan started` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry one or two `Given the <service> contract mock returns <x>` lines and those are the only additions; AC3 needs none, because its failure is the local record stub. AC2 names the whole R-WO-01 action: this story supplies the pinned version the rule runs under, the eligibility half is the scan story's and the tax-criteria half is RWB-S7-E6014-APP's, so one rule produces one outcome and neither story duplicates the other (ASM-5104). The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-01 | Write-off | D9 | SCAN_DUE | MONTHLY_SCAN_STARTED | cut_off_date reached and the ALS load is complete | Test every open case against the eligibility rule on both tracks and the tax criteria | POPULATION_PROPOSED | Write-off team | Rules component, COLLINS, ALS core and GL | monthly cut-off |
| R-WO-03 | Write-off | D9 | SCAN_DUE | TAX_CRITERIA_UNPUBLISHED | tax_criteria_version absent | Hold the scan until Finance publishes the version | SCAN_HELD | Write-off team | Reference data, Finance provision feed | None |
| R-WO-04 | Write-off | D9 | SCAN_HELD | LOAD_RESTORED | the ALS extract is complete and the tax criteria published | Restart the scan for the cut-off date | SCAN_DUE | Workbench | Reference data | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target the "Rules component" is the WO package read from rwb-decision (P7) and evaluated here, "Reference data" and the "Finance provision feed" are the versioned rows that carry the criteria and `tax_criteria_version`, "Workbench" is SCR-27, and "ALS core and GL" is reached by the scan and posting stories, not by this step. The criteria set is 51 rules over 27 states of the WO route set (TSD S7 T4), and this story owns the version under which R-WO-01 runs, not the rule contents.

| ID | Rule | Source |
|---|---|---|
| BR1 | A criterion is a versioned rule row or a reference-data row read with its version; no threshold, no list value and no condition of the criteria is a constant, a default or a branch of the code | FSD S7 BR-S7-014 and A2.14.3.1; legacy Guardrails; ASM-5104 |
| BR2 | The change is authored, tested, approved and rolled back in rwb-decision (P7); this service accepts, pins and records a version and authors nothing | Epics 3 to 8 Specification feature row FEAT-WOF-14; RWB-P7-E1073; ASM-5105 |
| BR3 | The decision record of the acceptance and of each outcome is written before the outcome exists, with the rule ID, the package version and `tax_criteria_version`; a failed write changes nothing and shows MSG-P7-003 | DP-03; TSD S7 T2; legacy AC1 and AC3 |
| BR4 | The case and its route states stay with rwb-case: this story answers `POPULATION_PROPOSED` and `SCAN_HELD` and writes no `recovery_case` row | ASM-5110; TSD S7 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` is an identifier of another service's fact | DP-01; TSD S7 T3.3 |
| BR6 | `tax_criteria_version` absent or a version incomplete for R-WO-01 and R-WO-03 holds the scan at `SCAN_HELD` under R-WO-03 with MSG-S7-001 and pins nothing; a published version restarts it under R-WO-04 | FSD S7 VR-S7-014-1; TSD S7 T4; ASM-5104 |
| BR7 | One version is pinned per cut-off: a version published mid-run is accepted for the next cut-off and never splits a running one | ASM-5104; legacy AC1 |
| BR8 | The same trigger twice, or the same `Idempotency-Key` twice, writes one record, one pin and one answer per case | TSD S7 T-A.2 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input; the step carries a version, a rule set, identifiers, amounts and dates only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR10 | The change itself is not performed here: this service holds no right to author or approve a criterion, and the change right stays on the rwb-decision capability area | TSD S7 T6.1; FSD S7 A2.14.3.3; ASM-5107 |
| BR11 | The version is recorded on the outcome and not on a column of `write_off`: no version column, no version table and no migration is created | TSD S7 T3.1; GAP-3043; ASM-5104 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the pin, the acceptance record and the state of the step.

| From (case route state) | Event | Condition | To |
|---|---|---|---|
| SCAN_DUE | A scan under R-WO-01 with a pinned version | cut_off_date reached and the ALS load is complete | POPULATION_PROPOSED, answered per case with the pinned version recorded |
| SCAN_DUE | The hold of R-WO-03 | tax_criteria_version absent or the version incomplete | SCAN_HELD, answered with MSG-S7-001 and nothing pinned |
| SCAN_HELD | The restart of R-WO-04 | the ALS extract is complete and the tax criteria published | SCAN_DUE, answered for the cut-off with the new version |
| Any other state | A trigger for a case outside the population | X6 | Unchanged: 409 and nothing written |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The scan opens, or a version is published | The cut-off is open | Reading |
| Reading | The package read answers | The version carries R-WO-01, R-WO-03, R-WO-04 and the tax criteria | Accepting |
| Reading | The version is absent or incomplete | X3 | Held, until R-WO-04 restarts the cut-off |
| Accepting | The decision record is written and the version pinned | The transaction commits | Running the cut-off |
| Running the cut-off | A second version is published | X4 | Running, on the pinned version; the new one is taken at the next cut-off |
| Accepting | The record write fails | X1 | Waiting, nothing changed |

The route states are those of the WRITEOFF machine of TSD S7 T4 and live on the case of record. This story writes no column of `write_off`; `tax_criteria_met` stays the tax-criteria step's write and the version lives on the decision record (BR11).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Write-off and posting R in TSD S7 T6.1: the primary role of the feature (FSD S7 A2.14.3.3), reading the version in force and the run state on SCR-27; the change itself is made under the rwb-decision authoring right and not here (ASM-5107) |
| RW-FINANCE, Finance and CFO delegate; RW-RISK, Risk and model risk officer | Write-off and posting RA: the also-users of FSD S7 A2.14.3.3, reading the version and its effect on the population |
| RW-WRITEOFF, RW-CREDITAD | Write-off and posting CRU and CRUA: run and re-run the scan of a cut-off under the pinned version |
| RW-PRODHEAD, RW-WOCOMM | Write-off and posting RA: read the run and decide at committee, not here |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Write-off and posting R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the step, reads the package, writes the record and the pin and answers the moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider. The one conflict is stated rather than smoothed: T6.1 gives RW-COE R only, while FSD S7 A2.14.3.3 makes the analyst the primary role of a change, so the change right is read as held on the rwb-decision capability area and this service performs no authoring (GAP-3043; ASM-5107). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| Item | Content |
|---|---|
| `write_off` (S7, `rwb_writeoff`) | The write-off row of TSD S7 T3.1, DF-FIN-010 to DF-FIN-020; this story sets no column on it, and `tax_criteria_met` (DF-FIN-014) stays the tax-criteria step's write |
| Standard record columns | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` of TSD S7 T3.0, written by the row's owner stories |
| Decision record DF-DEC-001 to DF-DEC-018 | Written through the local library before the outcome exists (DP-03): the package reference, the version accepted, the rule set it carries, the cut-off it is pinned to, the decision code and the decided-at time |
| The criteria version and the criteria set | Read from the package in force; its table, its owner and its key are Not specified in the source documents (GAP-3043; ASM-5104) |
| rule_row, decision_log_entry (P7) | Not read and not written here: the rule rows arrive on the package read and the local record is this service's, sealed into the central ledger by rwb-decision |
| recovery_case, timer (P3) | Not read as a table and not written: the population and the state arrive on the workflow boundary (ASM-5110) |
| v_ace_* views (P1) | Not read here: this service holds no grant and the population is a published contract answer |
| Not declared | No criteria table, no version column, no history table of this service; the history is the package's versions in rwb-decision |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, the record and the idempotency key are library objects created in `rwb_writeoff` by the library's own migration (DP-03), and the criteria version is a package fact with no column (GAP-3043; ASM-5104).

**No personal data.** The step carries a version, a rule set, a package reference, identifiers, amounts and dates. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the behaviour behind the criteria-version parameter of the scan, whose shape RWB-S7-E6026-CON declares; it declares no operation of its own, because TSD S7 T-A.1 publishes two and none changes the criteria (GAP-3043).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-off-scans` | ScanRequest in with the criteria version of the cut-off, WriteOffScan out with the pinned version and its run state, the population tested under it (API-S7-001) | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The errors are 401, 403 with MSG-P4-002, 409 for a conflicting or closed cut-off, 422 with MSG-GEN-001 and MSG-S7-001 for an absent version, and 503 when the library or the package read does not answer (TSD S7 T-A.2). `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) records the committee decision and belongs to the approve, reject and defer stories; it is not built or declared here. The population half of the scan is RWB-S7-E6013-CON's and the tax-criteria half is RWB-S7-E6014-CON's; this baseline adds the version element and reconciles with them at the wave 4 freeze (ASM-5108).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The WO criteria package read at its version (operation name and call type Not specified in the source documents (GAP-3043; ASM-5108)) | rwb-decision (P7), reached as a Temporal activity on the `rwb-decision` queue per the connection matrix row S7 to P7 | P7 rwb-decision | R-WO-01, R-WO-03 and R-WO-04, the eligibility rule on both tracks, the tax criteria with `tax_criteria_version` and the reference data the rules read; faked |
| The population of the cut-off (operation name Not specified in the source documents (GAP-3043; ASM-5110)) | rwb-case (P3), on the child-workflow boundary | P3 rwb-case | The cases in `SCAN_DUE` for the cut-off with the case reference, product group, balance, account link and state; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3043; ASM-5110)) | rwb-case (P3), on the child-workflow boundary | P3 rwb-case | The moves `POPULATION_PROPOSED` and `SCAN_HELD` with the rule ID and the pinned version; the stage outcome the parent `CaseWorkflow` applies; faked |

The connection matrix gives this service a Temporal line to rwb-decision and no line to rwb-case, so the package is called as an activity on the owner's queue and the case is answered on the workflow boundary; where an owner publishes a REST contract instead, one hop with a 2 s budget and a breaker applies (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3043).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1`, whose event set carries `WriteOffApproved` (event `EV-24`) with the retry and `.dlt` topics of the platform (TSD S7 T5.3; DP-14), and it belongs to the committee story: a criteria version accepted is not an approval and changes no balance. This story therefore declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test of the contract baseline. The outbox and inbox library that relays the topic is the DP-09 dependency the pattern set of this key does not carry (ASM-5109).

#### 12.4 Events consumed

None. The version arrives on the package read and the case on the forwarded signal; this service holds no consumer group, no subscription and no inbox row for either (ASM-5108, ASM-5110). The connection matrix gives S7 a listen line to rwb-source-data and rwb-payment, and neither carries a criteria version, so a build that adds a subscription for one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case, the cut-off date, the population reference and the version in force; signals: the package accepted, the version refused and the move answered. It hosts the criteria step and needs no compensation |
| `acceptCriteriaVersion` | Activity, the acceptance and the pin | `rwb-writeoff` | The cut-off and the package version in; the accepted version, its hash, the rule set it carries, the record reference and the pin out |
| `evaluateCriteria` | Activity, the R-WO-01 run of the cut-off under the pinned version | `rwb-writeoff` | The population, the pinned version and the package in; the rule ID with its version, the outcome, the write-off reference and the moves out, with the record and the row written in one transaction |

No child workflow for the case and none for the money exists in this service. The activity names are a target design choice fixed by no source document. The step waits on the scan and on the package publication, because R-WO-03 and R-WO-04 carry no clock beyond the monthly cut-off of R-WO-01.

#### 12.6 Schedules

None. The monthly scan is job `JOB-16` in the legacy and becomes a Temporal Schedule of the scan story (`RWB-S7-E6013-APP`), which opens the cut-off this step accepts a version for; this story declares no Schedule and no Quartz row, and the DP-10 dependency `RWB-PLT-E1071-CON` is absent from the pattern set and recorded (ASM-5109).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a balance on a case; this story sets no column on it and reads none of it as a criterion |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the acceptance and of each outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `proceeds` (P8) and the later stories' tables of this service. No foreign key leaves the schema (DP-01). No table, column or object holds the criteria version (BR11).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision criteria package fake | The WO package at version `2026-11` with R-WO-01, R-WO-03, R-WO-04, the eligibility rule on both tracks and `tax_criteria_version "2026-11"`; a version `2026-12` published mid-run; an incomplete version and an absent version | AC1, AC2, X3, X4 |
| rwb-case population fake | The population of the cut-off with 120 cases in `SCAN_DUE`, `RC-2026-000914` among them, with the product group, the balance, the account link and the state; a case that has left the population | AC2, X6 |
| rwb-case case-move fake | The moves `POPULATION_PROPOSED` and `SCAN_HELD` accepted for `RC-2026-000914`; a move refused because the case is not in the expected state | AC2, X3, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC1, AC3, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000914`, with the version in force and the run state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the package read, the population read and the case-move answer carry the placeholder until their owners confirm them (GAP-3043; ASM-5108, ASM-5110).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 0 consumed | `POST /write-off-scans` on `/api/recovery/writeoff/v1` with the criteria version of the cut-off; no REST row is consumed by this step |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the committee story's and no event carries a criteria version (§12.3, §12.4) |
| Temporal | 1 workflow, 2 activities and 1 remote activity | `WriteOffWorkflow`, `acceptCriteriaVersion` and `evaluateCriteria` on `rwb-writeoff`; the package read as an activity on the `rwb-decision` queue; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `criteria`; front end `src/modules/recovery/writeoff/CriteriaVersion.tsx`, a read-only fragment SCR-27 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the acceptance record, the pin and every outcome's version commit together or not at all. DP-13 moves the base of the scan operation and nothing else. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit and the rule packages of rwb-decision), DP-06 and DP-07 (the parameters and reference-data contracts of rwb-case), DP-09 (the outbox and inbox library) and DP-10 (the Temporal Schedule of `JOB-16`) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3043; ASM-5109).

**Dependencies the tables add and the plan does not hold.** The package read and the case-boundary rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the parameters and reference-data rows of DP-06 and DP-07 would add `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`; the schedule row of DP-10 would add `RWB-PLT-E1071-CON`; the outbox library of DP-09 would add `RWB-PLT-TE006-CON`. None is declared, because the criteria arrive as a package read, the step starts on the scan its sibling owns and it publishes nothing. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` criteria branch | Workflow | Waits for the cut-off or the publication, reads the version, pins it and reports the outcome to the parent |
| `acceptCriteriaVersion` | Activity | Reads the package, validates the version, writes the record, pins the version for the cut-off |
| `evaluateCriteria` | Activity | Runs R-WO-01 for each open case under the pinned version and records the version on the outcome |
| `CriteriaVersionReader` | Client | The package read at its version, with `tax_criteria_version` and the rule set |
| `CriteriaVersionValidator` | Service | The completeness check: R-WO-01, R-WO-03, R-WO-04, the eligibility rule on both tracks and the tax criteria with a version |
| `CriteriaPin` | Service | Holds the accepted version, its hash and the package reference for the length of a cut-off |
| `CriteriaDecisionRecordWriter` | Library adapter | Writes the acceptance and the outcome records before any change, hash-linked; refuses the step when the write fails |
| `CriteriaOutcomeWriter` | Repository | Records the pinned version on each outcome in one transaction with the row its owner story writes; adds no column |
| `CaseMoveAnswer` | Client | The move answer to rwb-case on the workflow boundary, one answer per case |
| `WriteOffScanController` | Controller | The scan operation with the criteria version, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `CriteriaVersion` | React component | Shows the version in force, the cut-off and the run state on SCR-27, read only |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service and the record and the idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column and no table is added for the criteria version, the pin or the version history (BR11).

**Configuration and reference data.**

- The criteria set and `tax_criteria_version`: package facts read with their version, never a constant, a default or a branch (ASM-5104).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access read through the guard.
- The Temporal timeout and the retry of the package activity, and the 2 s budget where a REST contract is used, are the platform rule (ADR-020); the monthly cut-off is R-WO-01's timer and not a parameter of this build.

**Build steps**

1. The criteria branch of `WriteOffWorkflow` and its input record on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the cut-off and the publication as its triggers.
2. `CriteriaVersionReader` against its fake, with the no-answer and breaker paths (AC1, X5).
3. `CriteriaVersionValidator` with the four completeness conditions and the absent version (AC1, X3).
4. `CriteriaDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
5. `CriteriaPin` with the mid-run publication path (AC1, X4).
6. `evaluateCriteria` and `CriteriaOutcomeWriter` with the version on each outcome and the one transaction (AC1, AC2, X7).
7. `CaseMoveAnswer` with the two moves, one per case of the population (AC2, X3, X6).
8. `WriteOffScanController` with the right, the `Idempotency-Key` and the problem mapping, and `CriteriaVersion` on SCR-27 through the composite route fake (AC1, AC2).
9. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case` or `rwb_decision`, and no criteria value in code (X8, BR1, BR4, BR5).

**Feature flag.** `rwb.writeoff.criteria-version-v1`, a flag of the platform library; off means the step accepts no version, the scan holds at `SCAN_HELD` with MSG-S7-001 and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, a version `2026-11` is accepted and pinned on the fakes, a version published mid-run does not split the cut-off, an absent or incomplete version holds the scan and restarts on R-WO-04, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, no criteria value is a constant, and SCR-27 answers the version state through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | No criteria version is in force or the published version is incomplete, so R-WO-03 holds the scan (X3) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the request, of the population or of the package is absent or invalid (X6) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right calls the scan or opens the version state (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the version is pinned or an outcome recorded (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set and of FSD S7 A2.14.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 is the VR-S7-014-1 hold of R-WO-03 and is shown on SCR-27 in its held state.

### 15. Screens and states

No screen is named for the criteria change: FSD S7 A2.14.2 says the analyst "opens the screen", SCR-27 Write-off proposal is the only screen the module lists, and the authoring screen of the rule set belongs to rwb-decision (GAP-3043; ASM-5106). This story therefore serves the version state of SCR-27 through the gateway-bff composite route (DP-19): the version in force, the cut-off it is pinned to, the run state and the held state, read only. The route calls rwb-writeoff for the version state and rwb-case for the case and its route state; the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved": the version state sits inside the scan state, the proposed, in-committee and approved states belong to the population and committee stories, and the held state is the reading of MSG-S7-001. The refusal and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-026-01 | AC1 | Component | The package at `2026-11` on the fake; the acceptance record written with the version, the pin set and the decision code asserted |
| TC-E6-026-02 | AC2 | Component | Case `RC-2026-000914` at `SCAN_DUE` with the version pinned; the outcome recording the version and the `POPULATION_PROPOSED` move asserted on the fake |
| TC-E6-026-03 | AC3 | Component | The decision-record stub stopped; nothing pinned, nothing written and MSG-P7-003 shown |
| TC-E6-026-04 | Access | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-026-05 | Principle 5 | Component | A forced decision log write failure inside the transaction; no pin, no outcome and no answer |

The five legacy cases are those of RWB-E6-026 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the criteria set, `tax_criteria_version`, the hold and restart conditions, the states and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, a version and a rule set only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- The case stays with rwb-case: no `recovery_case` row, no case route-state column and no case write here (BR4).
- The change is not authored here: no rule edit, no threshold, no list value and no approval of a criterion exists in this build (BR2, BR10).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no version column added for convenience (BR11).
- The decision is recorded before the change; a build that pins a version outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks (FSD S7 Requirements served); the split plan carries no requirement id for this slice (GAP-3043) | The accepted and pinned criteria version, the hold and restart of R-WO-03 and R-WO-04, the version on each outcome | TC-E6-026-01, TC-E6-026-02, TC-E6-026-05 |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (FSD S7 Requirements served); a population tested under one version is the precondition of that completeness | The single pinned version per cut-off | TC-E6-026-02 |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the acceptance and the pin | TC-E6-026-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-026-01 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The criteria package read at its version and evaluated here | TC-E6-026-01, TC-E6-026-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed rows with their budget and breaker | TC-E6-026-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the pin and the outcome | TC-E6-026-03, TC-E6-026-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-026, disposition Split (rework); feature FEAT-WOF-14 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story; AC2's eligibility half is the scan story's and its tax-criteria half is RWB-S7-E6014-APP's |
| Source text | Legacy RWB-E6-026; FSD S7 Write-off and recovery v3 A1, A2.14 and Requirements served; TSD S7 Write-off and recovery v2 T2, T3.1, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-01, R-WO-03 and R-WO-04; Epics 3 to 8 Specification v3 feature row FEAT-WOF-14 |
| Test cases | TC-E6-026-01 to TC-E6-026-05 |
| Feature and screens | FEAT-WOF-14, SCR-27 Write-off proposal in its version state |
| Rules | R-WO-01, R-WO-03 and R-WO-04, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the scan operation and of the criteria-version element, the consumed rows, the criteria-version state, the error set and the fakes: RWB-S7-E6026-CON.
- The authoring, validation, test scenarios, approval and rollback of the WO package and the home of `tax_criteria_version`: rwb-decision (P7) and the rule authoring story RWB-P7-E1073 (ASM-5104, ASM-5105).
- The monthly scan Schedule from `JOB-16`, the eligibility test of the population and its proposal: the scan story of RWB-E6-013 (ASM-5109).
- The tax-criteria test of the population and the post charge-off remittance path: RWB-S7-E6014-APP.
- The pack, the committee routing, the approve, the reject and the defer: FEAT-WOF-03 and FEAT-WOF-05 to 08, API-S7-002.
- The posting to ALS and the general ledger, the provision release, the Finance feed and the reconciliation of the approved and posted populations: FEAT-WOF-09 to 11.
- The exception loop, the retention closure and the post charge-off sale: FEAT-WOF-12, FEAT-WOF-13 and FEAT-WOF-16.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the money and the posting reference: rwb-payment (P8).
- The gateway-bff composite route and the screen field list of SCR-27, and the authoring screen of the rule set: RWB-PLT-N001-CON and rwb-decision.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
