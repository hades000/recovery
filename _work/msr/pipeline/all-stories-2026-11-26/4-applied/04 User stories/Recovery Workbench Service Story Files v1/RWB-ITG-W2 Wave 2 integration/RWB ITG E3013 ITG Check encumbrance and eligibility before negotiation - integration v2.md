# RWB-ITG-E3013-ITG Check encumbrance and eligibility before negotiation

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E3013-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S2-E3013-APP, RWB-P3-E3013-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-013 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E3013-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **integration and QA harness**, I want **one repeatable cross-service harness that proves the encumbrance and title checks run early, that a missing title document raises the task that re-creates the title set before release, and that the case reaches EARLY_READINESS_CHECK with one decision record naming the rule and its version — across rwb-treatment, rwb-case, the ACE collateral views read through rwb-source-data, and rwb-decision**, so that **a deed in lieu is never negotiated on an asset that cannot transfer, and every early readiness check is proven with the rule and the rule version that decided it**.

The harness builds no production operation, no table, no workflow, no schedule and no screen. RWB-S2-E3013-APP owns the encumbrance and title check inside rwb-treatment, the R-DIL-01 and R-SET-22 rules and the deed-in-lieu treatment; RWB-P3-E3013-APP owns the case move, the task that re-creates the title set and its assignment. This story drives those two services' published contracts, reads the ACE collateral, title and non-performing asset facts through the rwb-source-data products contract, reads the record back from rwb-decision and asserts what the owners did. Nothing here is a deliverable of the Workbench.

### 2. Business rationale

A deed in lieu negotiated on an asset that cannot transfer wastes the negotiation, and an agreement the bank cannot register exposes it to a void settlement after the customer has already relied on it. The defence is timing: the encumbrance, title and lien facts are checked before the offer is made and not at the transfer, so a case that cannot transfer is stopped while the officer has spent nothing. Those facts are not re-keyed; they are read from ACE's collateral, collateral detail and non-performing asset rows, a task is raised in rwb-case when the title set is incomplete, and every step is recorded with the rule and its version so the decision can be defended years later.

In the monolith this all sat inside one S2 module, so a defect showed up either as a negotiation on an untransferable asset or as a case that moved without a record. In v5 the same behaviour crosses four services: rwb-treatment evaluates R-DIL-01 and R-SET-22 and raises the task, rwb-case holds the case state, the task and its assignment, rwb-source-data owns the ACE view contract the collateral and asset facts are read through, and rwb-decision holds the record with its rule version. A defect at any of those four now looks like a negotiation that should never have started, and only a run that crosses all four can tell the difference between a check that ran and a check that was skipped.

This story owns the harness for FEAT-TRT-13 and its FEAT-TRT-12 parent, and it carries REQ-S2-005, REQ-RDF-004, REQ-DRI-001 and REQ-DRI-005 into evidence. It never reads another service's table (DP-01): the treatment comes from rwb-treatment, the case and the task from rwb-case, the collateral, title and asset facts from rwb-source-data's products contract (DP-05), the record from rwb-decision (DP-03) and the authorisation answer from rwb-access. Every call sits on the owner's base `/api/recovery/<short>/v1` with one hop and a 2 s budget (DP-13), and the composed read a screen would make is exercised through the gateway-bff composite route (DP-19).

### 3. Preconditions

- The published contracts of rwb-treatment, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the contract registry, a WireMock stub set is generated from each, and each contract version is pinned in the run report.
- A case is at ROUTE_APPROVED_DIL carrying its deed-in-lieu treatment, and a second case is at COLLATERAL_RELEASE_REQUESTED whose title documents are missing. Both cases and both treatments are seeded through the owning services' published operations only; the seeding set is not specified in the source documents (GAP-0425; ASM-0601).
- The ACE collateral, collateral detail and non-performing asset rows for the accounts of both cases are available through the P1 products contract, with the lien rank, the title document number and the asset facts the check reads present as ACE holds them.
- The rule package in force carries R-DIL-01 and R-SET-22, and the version of each is readable on the decision record that cites it.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for a role that holds Treatment and offer R, and for a caller whose role does not.
- The CCMS and Land Office check interface, its result codes and its fixtures are not specified in the source documents (GAP-0425; ASM-0601); where the check leaves the Workbench it is modelled by a fixture on that interface. So are the harness repository and its SIT environment, and the evidence format and its retention (GAP-0425; ASM-0601).
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run, and each fake replaced by the real service when RWB-S2-E3013-APP and RWB-P3-E3013-APP land.

### 4. Flow

1. Harness: seeds both cases, their states and their deed-in-lieu treatments through the owning services' published operations only; the seeding set, its identifiers and its environment are not specified in the source documents (GAP-0425; ASM-0601).
2. Harness: reads the collateral row, its title detail and the non-performing asset row through `GET /api/recovery/source-data/v1/data-products/DP06/records` and asserts the lien rank, the title document number and the asset facts the check needs, without re-keying any of them (DP-05, REQ-RDF-004).
3. Harness: observes the R-DIL-01 move the owner applies to the route approval, from ROUTE_APPROVED_DIL to EARLY_READINESS_CHECK, and reads the state back with `GET /api/recovery/case/v1/cases/{caseId}`.
4. Harness: asserts, on the second case where the title set is incomplete, that a task exists and is assigned, through `GET /api/recovery/case/v1/me/tasks` and the task read on the rwb-case contract, and that the task names the re-creation of the title set.
5. Harness: asserts that the second case still reads COLLATERAL_RELEASE_REQUESTED on the R-SET-22 path, that the case did not move to another state, and that the treatment on the case is unchanged.
6. Harness: reads `GET /api/recovery/decision/v1/decision-log` for both cases and asserts exactly one record per move, each naming R-DIL-01 or R-SET-22 with its rule version, and asserts `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` for the same two moves.
7. Harness: asserts that the case move is published as `rwb.case.CaseStateChanged.v1` once per move and that no personal data is present on any event it reads.
8. Harness: authorises each call through `POST /api/recovery/access/v1/authorise`, records the refusal for a role that does not hold Treatment and offer R, and asserts the refusal message the owner returns.
9. Harness: asserts one hop per call, a 2 s budget and a circuit breaker per downstream on every call in the trace, and fails the run on a call chain deeper than the gateway and one owner.
10. Harness: writes one evidence report per business date, keyed by story, naming the two moves, the two records with their rule versions, the task and the contract versions; the evidence format and its retention are not specified in the source documents (GAP-0425; ASM-0601).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow, or a reachable service answers on a contract version that differs from the registry | The run fails at that hop, before any later assertion; the report names the service, the operation and both contract versions | None | AC3 |
| X2 | No collateral row answers for the account of the case | The run fails and the report names the account, the data product and the operation; the run is not marked passed | None | AC1 |
| X3 | A lien rank or a title document number is present but the check cannot classify it | The run fails and the report names the field and the row; the harness never substitutes a value | None | AC1 |
| X4 | The case does not reach EARLY_READINESS_CHECK on the R-DIL-01 path | The run fails and the report names the two states and the case | None | AC1 |
| X5 | No task is raised when the title set is incomplete | The run fails and the report names the case, the treatment and the state | None | AC2 |
| X6 | The case moves when the title set is incomplete | The run fails on the R-SET-22 path and the report names the state it moved to | None | AC2 |
| X7 | Zero or two decision records exist for a move, or a record carries no rule version | The run fails and the report names the records it found and the version field it read | None | AC1, AC2 |
| X8 | A decision record cannot be written | The move does not happen, every state is left as it was, the owner answers MSG-P7-003, and the run asserts that nothing changed | MSG-P7-003 | AC3 |
| X9 | A caller whose role does not hold the right calls an operation | The call is refused with MSG-P4-002 and the run asserts the refusal, not a silent pass | MSG-P4-002 | AC3 |

The report text is for the wave entry check and is not part of the message standard. R-DIL-01 and R-SET-22 carry no message ID in the rule set, so the harness asserts state, data and the decision record and names a message ID only where the owning service returns MSG-P7-003, MSG-P4-002 or MSG-GEN-001; the business messages this journey can produce are in section 14 and belong to the owning services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only waits are two I stories, RWB-S2-E3013-APP and RWB-P3-E3013-APP |
| Negotiable | The CCMS and Land Office fixture, the seeding set and the report shape are configuration agreed at the wave entry check, not business values in code |
| Valuable | The early encumbrance and title check, the title re-creation task and the record that carries the rule version are proven before the wave opens |
| Estimable | One harness runner, one stub set, one check fixture, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion runs against its fakes on Day 1 and again against the real owners as the two app stories land |

### 7. Acceptance criteria

```gherkin
Feature: Check encumbrance and eligibility before negotiation

  Background:
    Given the rule package in force carries R-DIL-01 and R-SET-22 with a readable version for each
    Given the published contracts of rwb-treatment, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the registry with a stub set generated from each
    Given the seeded case identifiers and the harness environment are Not specified in the source documents (GAP-0425; ASM-0601)

  Scenario: AC1 The R-DIL-01 path reaches EARLY_READINESS_CHECK with one record naming the rule and its version (new, D-RCV-60)
    Given a case in state ROUTE_APPROVED_DIL carrying its deed-in-lieu treatment
    And the collateral row, its title detail and the non-performing asset row are readable through the P1 products contract
    When the harness reads the collateral, the title document number, the lien rank and the asset facts through the P1 products contract
    And the owning service applies R-DIL-01 to the route approval
    Then the case reads at EARLY_READINESS_CHECK through the rwb-case contract
    And the move is published as rwb.case.CaseStateChanged.v1 for the case
    And exactly one decision record names R-DIL-01 with its rule version on rwb.decision-record.v1
    And the run is green with one trace and one hop per call

  Scenario: AC2 The R-SET-22 path holds the case and raises the task that re-creates the title set (new, D-RCV-60)
    Given a second case in state COLLATERAL_RELEASE_REQUESTED whose title documents are missing
    When the owning service applies R-SET-22 to the title check
    Then a task exists on the case and its assignment is readable through the rwb-case task read
    And the task names the re-creation of the title set before release
    And the case still reads at COLLATERAL_RELEASE_REQUESTED
    And the treatment on the case is unchanged
    And exactly one decision record names R-SET-22 with its rule version

  Scenario: AC3 Refusals and a failure that changes nothing (new, D-RCV-60)
    Given the decision-record write is forced to fail for one move
    When that move is attempted
    Then nothing changes on the case, the treatment or the task
    And the owning service answers MSG-P7-003
    And a caller whose role does not hold Treatment and offer R is refused with MSG-P4-002
    And a contract version that differs from the registry fails the run before any assertion
```

The legacy key owns AC1 to AC4 of RWB-E3-013; those criteria test the rwb-treatment behaviour and are held by RWB-S2-E3013-APP and RWB-P3-E3013-APP. This story owns no legacy AC. Its three criteria test only the harness deliverable named in the title: the early check read through the ACE views, the two rules observed as the owners apply them, the task raised when the title set is incomplete, the one record per move with its rule version, and the refusal and failure paths that must not change state.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The encumbrance and title checks run before negotiation starts, and a deed in lieu is not negotiated on an asset that cannot transfer | Legacy RWB-E3-013; REQ-S2-005; FEAT-TRT-13 |
| BR2 | At ROUTE_APPROVED_DIL with the route approved and the route set to R3, the lead is prioritised and the early readiness checks start, and the case moves to EARLY_READINESS_CHECK | R-DIL-01 |
| BR3 | At COLLATERAL_RELEASE_REQUESTED with the title documents missing, a task re-creates the title set before release and the case stays at COLLATERAL_RELEASE_REQUESTED | R-SET-22 |
| BR4 | The collateral, title and non-performing asset facts are read through the ACE views and never re-keyed | REQ-RDF-004; legacy RWB-E3-013 |
| BR5 | The decision record carries the rule and its version, and it is written with the state change in one transaction | REQ-DRI-001; R-UNI-39 |
| BR6 | No action proceeds if its decision record cannot be written | REQ-DRI-005; R-UNI-39 |
| BR7 | The treatment is the owner's and the harness writes no treatment row; a seeded treatment is placed through the rwb-treatment contract only | Legacy RWB-E3-013; DP-05 |
| BR8 | The checks run early and not at transfer, so a blocked asset is found before the offer rather than at registration | FEAT-TRT-13; FEAT-TRT-12 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ROUTE_APPROVED_DIL | ROUTE_APPROVED | decision.approved and route = R3 | EARLY_READINESS_CHECK (R-DIL-01) |
| COLLATERAL_RELEASE_REQUESTED | TITLE_DOCUMENTS_MISSING | title documents not found | COLLATERAL_RELEASE_REQUESTED, with a task to re-create the title set (R-SET-22) |

The case state is the owner's: rwb-treatment evaluates the rule and raises the task, the case move is published as `rwb.case.CaseStateChanged.v1`, and both states are read back through the rwb-case contract. The rule table also carries R-DIL-02 and R-DIL-04 out of EARLY_READINESS_CHECK, the clear and the unresolved encumbrance; those belong to the check itself and are asserted by RWB-S2-E3013-APP, not by this harness.

The harness sets nothing by hand. It seeds through the owning services' published operations, lets the owner apply the rule, and then asserts the state the owner reached. A state the harness set by hand would prove nothing, so the report names the owner and the operation behind each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT and the roles that hold Treatment and offer R | Read the treatment and the check evidence through the rwb-treatment contract, and the collateral and title facts through the P1 products contract |
| RW-CASEOWN and the roles that hold the title re-creation task | Hold and read the task and its assignment through the rwb-case task read |
| QA lead | Owns the harness configuration, the CCMS and Land Office check fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-treatment, rwb-case, rwb-source-data, rwb-decision and rwb-access make every state change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the deed-in-lieu approval and the early readiness decision belong to the treatment story |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, status (ROUTE_APPROVED_DIL, EARLY_READINESS_CHECK, COLLATERAL_RELEASE_REQUESTED), stage_code | Read, through the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at | Read, through the rwb-case contract |
| DF-WRK-017 to DF-WRK-026 | task | id, case_id, task_code, element_type, discretion, status | Read, through the rwb-case contract |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date, active flag | Read, through the P1 products contract (DP-05) |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail | asset_key, title_doc_no, plot_no, area_text, province, lien_rank | Read, through the P1 products contract (DP-05) |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value | Read, through the P1 products contract (DP-05) |
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at, state | Read, through the rwb-treatment contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The harness owns no table and writes no row directly: it seeds and reads through the API of the owning service only (DP-01, DP-05). The collateral, title and asset rows are ACE's, read through rwb-source-data's DP06 product, and the Workbench writes no collateral, title or asset row (REQ-RDF-004).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/treatment/v1/cases/{caseId}/treatments` | S2 rwb-treatment | Seed the deed-in-lieu treatment on each case and read its state (AC1, AC2) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, its state and its decision_log_id after each rule applies (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The collateral row, its title detail and the non-performing asset row from DP06 (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state at EARLY_READINESS_CHECK and at COLLATERAL_RELEASE_REQUESTED (AC1, AC2) |
| GET | `/api/recovery/case/v1/me/tasks` | P3 rwb-case | The title re-creation task and its assignment after R-SET-22 (AC2) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The single record per move, with R-DIL-01 or R-SET-22 and its version (AC1, AC2) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and right check for each call, including the refusal path (AC3) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-13); where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story, and no operation reaches another service's schema.

#### 12.3 Events published

None. The harness publishes no Kafka event; it seeds through the owners' operations and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through the local decision-record library | One record per move, written with the state change (AC1, AC2) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | The case move on the R-DIL-01 path, and the absence of a move on the R-SET-22 path (AC1, AC2) |
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The treatment was approved before the run (AC1) |

All three carry IDs and business facts only, keyed by caseId and treatmentId, and the harness asserts that no personal data is present (DP-03, DP-09).

#### 12.5 Workflows and activities

None added. The harness exercises the existing TreatmentWorkflow in rwb-treatment, which evaluates R-DIL-01 and R-SET-22, writes the record and raises the task, and the CaseWorkflow in rwb-case, which moves the case status and holds the task and its assignment. It asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. R-DIL-01 and R-SET-22 are triggered by facts and not by a Schedule, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the treatment is rwb-treatment's, the case, the task and the assignment are rwb-case's, the record is rwb-decision's, and the collateral, title and asset rows are ACE's, read through rwb-source-data's contract (DP-05).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-treatment | `POST /cases/{caseId}/treatments`, `GET /treatments/{treatmentId}`, `rwb.treatment.events.v1` | Day-1 seeding and reads on both paths before RWB-S2-E3013-APP is live |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /me/tasks`, `rwb.case.events.v1` | Day-1 assertions on both case states, the task and its assignment |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the collateral row, the title detail and the asset row |
| WireMock stub for rwb-decision | `GET /decision-log`, `rwb.decision-record.v1` | Day-1 assertion of one record per move with its rule version |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| CCMS or Land Office check fixture | The check interface the rule leaves the Workbench through | The check result the owner reads, where the configured check is an outside interface |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The CCMS and Land Office interface codes, their result codes, their transports and layouts, their test endpoints and the fixture contents, the seeding set, the harness environment and the evidence format and retention are not specified in the source documents (GAP-0425; ASM-0601).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.decision-record.DecisionRecorded.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.treatment.TreatmentApproved.v1` consumed (DP-03, DP-09) |
| Temporal | None added; the TreatmentWorkflow and the CaseWorkflow exercised |
| File | None. The CCMS or Land Office check is asserted through a fixture where the check leaves the Workbench, and no file is produced or read by the harness |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays None. The blocking dependencies are the two I stories, RWB-S2-E3013-APP and RWB-P3-E3013-APP: until they are live the run uses their stubs, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour. The monolith S2 module's check becomes rwb-treatment's behaviour, with the task raised in rwb-case; the ACE collateral, title and asset facts are read through the P1 products contract and never from a local view or a copy (DP-05); every call sits on the owner's per-service base with a single hop (DP-13); the record is read through the local decision-record library and its shared topic (DP-03); and the composed read a screen would make is exercised through the gateway-bff composite route (DP-19). Per-service schemas mean no service reads another's tables (DP-01), so the harness fails a run whose trace shows a cross-schema reference.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ReadinessRunner | Job | Runs the two paths in order for a business date and holds the run lock |
| StubSet | Fake | The five WireMock stubs and the check fixture, each generated from the published contract with its version pinned |
| CheckFixture | Fixture | The CCMS or Land Office check result the owner reads, keyed by case and by asset, where the check leaves the Workbench |
| SourceDataProbe | Assertion | Reads the collateral row, its title detail and the asset row through DP06 and asserts the lien rank, the title document number and the asset facts |
| TaskProbe | Assertion | Reads the title re-creation task and its assignment through the rwb-case task read and asserts that the task names the re-creation of the title set |
| RecordProbe | Assertion | Reads one record per move with its rule and rule version from rwb-decision, and cross-checks the same move on `rwb.decision-record.v1` |
| EventProbe | Service | Consumes `rwb.case.events.v1`, `rwb.treatment.events.v1` and `rwb.decision-record.v1` and asserts the facts for both cases |
| TraceAssertion | Assertion | Fails the run on a call chain deeper than the gateway and one owner, on a call outside the 2 s budget, and on a missing breaker |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** The harness repository and its SIT environment are not specified in the source documents (GAP-0425; ASM-0601). The run is against the stub set from Day 1 and against each real owner as RWB-S2-E3013-APP and RWB-P3-E3013-APP land. The seed is two cases: one at ROUTE_APPROVED_DIL with its deed-in-lieu treatment, and one at COLLATERAL_RELEASE_REQUESTED whose title documents are missing; the identifiers, the business date under test and the exact response values of the fakes are not specified in the source documents (GAP-0425; ASM-0601). The collateral, title and asset rows come from the ACE DP06 product as ACE holds them, and the harness copies no values into its fixture. Seeding uses only the owning services' published operations, never a schema write. The evidence format and its retention are not specified in the source documents (GAP-0425; ASM-0601).

**Build steps**

1. Generate the five stubs and the check fixture from the published contracts, pin each contract version in the report and fail the run on a version mismatch (X1).
2. Build the ReadinessRunner and the seed path: two cases, their states and their deed-in-lieu treatments through the owners' operations only, never a schema write.
3. Add SourceDataProbe for AC1: the collateral row, the title detail and the asset row through DP06, with the lien rank, the title document number and the asset facts asserted and none substituted (X2, X3).
4. Add the R-DIL-01 assertion: the move to EARLY_READINESS_CHECK read back through the rwb-case contract, and one record naming R-DIL-01 with its rule version (X4, X7).
5. Add TaskProbe and the R-SET-22 assertion: the task raised, its assignment, the task naming the re-creation of the title set, and the case still at COLLATERAL_RELEASE_REQUESTED (X5, X6).
6. Add RecordProbe and EventProbe for `rwb.case.CaseStateChanged.v1`, `rwb.treatment.TreatmentApproved.v1` and `rwb.decision-record.DecisionRecorded.v1`, and assert the key and the absence of personal data.
7. Add the forced record failure of AC3 and prove that nothing changes on the case, the treatment or the task and that the owner answers MSG-P7-003 (X8).
8. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a role that does not hold Treatment and offer R (X9).
9. Add TraceAssertion and the EvidenceReport, then swap each stub for its real owner when RWB-S2-E3013-APP and RWB-P3-E3013-APP land and rerun both paths.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it; the flag key for this harness is not specified in the source documents (GAP-0425; ASM-0601).

**Done when.** The tests of section 16 pass for AC1, AC2 and AC3; both paths pass against the fakes on Day 1 and again against rwb-treatment and rwb-case when RWB-S2-E3013-APP and RWB-P3-E3013-APP land; and the wave entry check holds a run report keyed by story and business date with the two moves, the two records with their rule versions and the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the move cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-DIL-01 and R-SET-22 carry no message ID in the rule set, so the harness asserts the state, the data and the decision record and names the message ID only where the owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-16 Deed in lieu and SCR-14 Treatment record show the states this harness asserts. The harness renders no screen; it reads the states through the rwb-treatment, rwb-case and rwb-source-data contracts, so a passed run means the screens have the right data behind them.

| State | What the user sees and does |
|---|---|
| Checks | The early readiness check has started; the collateral, title and lien facts are read and the record names the rule and its version |
| Appraisal | The check cleared and the valuation was ordered; the harness asserts only the earlier readiness state |
| Approved | The deed in lieu is approved before negotiation; no offer exists yet |
| Transferred | The asset has been transferred to the bank; the states that lead here are the ones the harness asserts, and the transfer itself belongs to RWB-E3-012 |
| Broken | A title document is missing and a task re-creates the title set before release (R-SET-22) |

The case states EARLY_READINESS_CHECK and COLLATERAL_RELEASE_REQUESTED are read through the rwb-case contract and shown on the case record view, whose screen ID is not named for this feature in the source documents (GAP-0425; ASM-0601). What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0425; ASM-0601).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-013-01-ITG | Legacy RWB-E3-013 AC1; asserts AC1 | Integration | A case at ROUTE_APPROVED_DIL with its deed-in-lieu treatment; the collateral row, the title detail and the asset row through DP06 |
| TC-E3-013-02-ITG | Legacy RWB-E3-013 AC2; asserts AC2 | Integration | A case at COLLATERAL_RELEASE_REQUESTED with the title documents missing; the task and its assignment |
| TC-E3-013-03-ITG | Legacy RWB-E3-013 AC3; asserts AC1 | Integration | ROUTE_APPROVED_DIL; route approved; the move to EARLY_READINESS_CHECK and one record naming R-DIL-01 |
| TC-E3-013-04-ITG | Legacy RWB-E3-013 AC4; asserts AC3 | Integration | Decision-record write forced to fail; nothing changes; MSG-P7-003 |
| TC-E3-013-05-ITG | Legacy RWB-E3-013 Access; asserts AC3 | Component | A role without Treatment and offer R; refused with MSG-P4-002 |
| TC-E3-013-06-ITG | Legacy RWB-E3-013 Principle 5; asserts AC3 | NFR | Decision-record write forced to fail; no case, treatment or task state changes |

The integration cases above are the ITG copies of the legacy cases TC-E3-013-01 to TC-E3-013-06 and carry the legacy intent unchanged; the component and NFR copies keep the legacy levels. TC-E3-013-01-ITG and TC-E3-013-03-ITG are the copies that cover the two rules this harness owns. The full test, with its Given, When and Then, is in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under the legacy test case IDs TC-E3-013-01 to TC-E3-013-06.

### 17. Guardrails

- No business value in code: the rule versions, the check fixture, the seeding set and the state names are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the collateral, title and asset rows are ACE's, read through rwb-source-data's DP06 product (DP-05).
- The harness never re-keys an ACE fact: a lien rank, a title document number, an area, a province or a value is asserted as ACE returns it and never copied into a fixture.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a case, treatment, task or record state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-005 | Deed in lieu readiness, including the encumbrance check and an early valuation, is established before negotiation starts | Business Requirements Program v5, section 5.9 | FEAT-TRT-13 | D6.4 Deed in lieu | R-DIL-01, R-SET-22 | TC-E3-013-01-ITG, TC-E3-013-02-ITG, TC-E3-013-03-ITG |
| REQ-RDF-004 | Collateral records and appraisal values are available on the case without a person looking them up, read through the ACE views | Business Requirements Program v5, section 5.1 | FEAT-TRT-13 | D6.4 Deed in lieu | R-DIL-01, R-SET-22 | TC-E3-013-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-TRT-13 | D6.4 Deed in lieu | R-DIL-01, R-SET-22 | TC-E3-013-03-ITG, TC-E3-013-04-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program v5, section 5.7 | FEAT-TRT-13 | D6.4 Deed in lieu | R-DIL-01, R-SET-22 | TC-E3-013-04-ITG, TC-E3-013-06-ITG |

### 19. Out of scope

- AC1, AC2, AC3 and AC4 of the legacy key, which are owned by RWB-S2-E3013-APP and RWB-P3-E3013-APP.
- The whole rwb-treatment behaviour: the encumbrance and title check, R-DIL-02 and R-DIL-04 out of EARLY_READINESS_CHECK, the deed-in-lieu treatment and its approval are RWB-S2-E3013-APP.
- The whole rwb-case behaviour: the case move, the task, its definition, its assignment and its service level are RWB-P3-E3013-APP.
- The contract baselines of the two services, which are RWB-S2-E3013-CON.
- The CCMS and Land Office interface codes, transports, layouts, result codes and test endpoints, none of which a source read gives.
- The deed-in-lieu offer, appraisal and transfer, which are RWB-E3-012, and the release after settlement, which is RWB-E3-017.
- The non-performing asset unlock rule, which is RWB-E3-014.
- Any production screen, endpoint, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the seeding set, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.
