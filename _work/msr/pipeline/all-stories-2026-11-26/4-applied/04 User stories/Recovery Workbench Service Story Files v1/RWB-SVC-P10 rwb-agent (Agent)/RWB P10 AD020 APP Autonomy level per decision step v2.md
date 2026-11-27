# RWB-P10-AD020-APP Autonomy level per decision step

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-AD020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1063-APP |
| Depends on (build) | RWB-P10-AD020-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON, RWB-P10-E1063-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-020 for rwb-agent. The level of a decision step becomes a column of the policy version in `rwb_agent` that the run reads at run time and never a value in code (DP-01); the step is a decision code held as data, the run records the level it ran under, and the record of the answer carries the step, the level and the version through the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03); the admin read moves to the service base `/api/recovery/agent/v1` (DP-13) and reaches SCR-46 through the gateway-bff composite route (DP-19); the case facts a step reads come through rwb-source-data's contract (DP-05) and never from a view of this service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P10-AD020-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **the autonomy level of each agent step held as data and changed only with committee approval**, so that **an agent never acts beyond what the committee approved**.

The story keeps the words of the legacy story RWB-AD-020. What is new is where the level lives and how it reaches the run: the level is a column of the policy version in force in `rwb_agent`, the step is a decision code of the decision set, and the answer of a step at L1 is shown to a person as a recommendation while a step at L2 acts under the approval reference of its version.

### 2. Business rationale

The legacy story gave one sentence and two criteria to this behaviour: the level of a step is data, and a step up is recorded with the approval reference of the version that takes effect. The functional source is FEAT-AGT-12, which changes the autonomy level of one agent and one decision as a versioned configuration row, and FEAT-AGT-15, which raises or lowers a level with the approval each change needs (FSD P10 v3 A2.12 and A2.15). The regulatory source is the BOT AI Risk Management Guidelines of 12 Sep 2025: accountability, lifecycle risk management and explainability, with the AI isolated in rwb-agent and easy to switch off, and a person approving what a suggestion would change (Arch v5 slide 35 and slide 50). A level held in code, or a level that a run does not record, cannot be reconciled with the approval that allowed it.

In the target the level and the run are in the same service, so the resolution is a read of one row and not a call. rwb-agent owns the agent policies, the prompts, the runs, the guardrails and the evaluations (Arch v5 slide 41), and `agent_policy` carries `autonomy_mode` per policy version (DF-AGT-008, LOV-AUTONOMY) with `valid_from`, `valid_to` and `status` (DF-AGT-022, DF-AGT-023, DF-AGT-021). The run is `agent_run`, whose `autonomy_mode` (DF-AGT-043) is the level the run ran under and whose `decision_log_id` (DF-AGT-058) is the record of its answer. No level, no step code and no threshold is written in code, which is the rule the two legacy business rules state in the same words (BR-P10-012 and BR-P10-015: no value a business person may change is written in code; it is read from reference data with its version).

The legacy data table named `decision_log_entry` and read it directly. In the target that table belongs to rwb-decision (P7), so the row is written through the local decision-record library in the same transaction as the answer and relayed to the shared topic `rwb.decision-record.v1` (DP-03; ADR-022). That is what carries the step, the level and the version to the central ledger: `decision_code` (DF-DEC-003) already holds the step, and the level and the version travel as two named members of the record's `recommendation` (DF-DEC-009) because `approval_level` (DF-DEC-011) is the delegation ladder L1 to L6 of LOV-APPROVAL-LEVEL and its L1 is not the autonomy L1 — a collision this story states rather than hides.

Three further moves are the realignment. The legacy base becomes the service base (DP-13): the admin read is answered on `/api/recovery/agent/v1/admin/agent-runs` and no monolith path answers it. The screen is served by the gateway-bff composite route, which composes the level per step with the run and evaluation reads so that the browser calls no owner service (DP-19). The case facts a step answers on are read through rwb-source-data's contract by the tool gateway and never from a `v_ace_*` view granted to this service (DP-05; ADR-010; Arch v5 slide 16).

This story owns both legacy criteria of RWB-AD-020 — AC1 and AC2 — and copies them verbatim in section 7. AC3 to AC11 are new and test the microservice deliverable of the title only. The legacy story carries no requirement ID; section 18 records that and traces the feature instead. The legacy dependency RWB-E1-063 (the agent monitor) is the story RWB-P10-E1063-APP in the target, and it is the one in-lane story this one waits for.

### 3. Preconditions

- RWB-P10-AD020-CON is published: the per-step autonomy slice of the rwb-agent contract — the step, the level, the version label and the approval reference as a backward-compatible extension of the agent configuration resource, the resolution rule of the level in force, the response shape of the agent configuration and agent output reads, the decision-record members, and the three fakes. This story builds against that contract and its fakes and waits for nothing else in the contract set.
- RWB-PLT-E1027-CON is published: the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1` with its CloudEvents envelope. This story writes its record through the library and never writes the shared topic directly.
- RWB-PLT-N001-CON is published: the gateway-bff composite route contract for SCR-46 and its stub, so the exposure of the level per step is built and tested before the screen story lands.
- RWB-P10-E1063-APP is done: SCR-46 Agent monitor, its states Shadow, live and paused, and the run and evaluation reads behind it exist, and this story adds the step and the level to what that screen shows.
- The `rwb_agent` schema exists with the agent runtime baseline migration — `agent_policy` and `agent_run` among its tables (TSD P10 v2 T3.1; RWB-P10-E1058-APP owns the schema and the baseline). The step scope of a policy version is held in a jsonb member of the version until a dedicated column is agreed (GAP-0638; ASM-1010), so this story issues no migration of its own.
- Policy versions are in force with `agent_code`, `policy_version`, `model_code`, `model_version`, `autonomy_mode`, `valid_from`, `valid_to` and `status`, and each version names the decision step it governs. The step is a value of LOV-DECISION, which is D1 to D9 with sub-decisions and X1 to X7 (LDM v8, DF-DEC-003 and the list table). The legacy example is step D6.3, the route decision is D6, and the route agent output of D6 is owned by S1 rwb-valuation (Arch v5 slide 41).
- The list values used by the step are those of TSD P10 v2 T3.2: LOV-AUTONOMY (OFF, SHADOW, L1), LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED) and LOV-AGENT (INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER). The lists are reference data owned by rwb-case under the §R3 default ruling and the step holds no copy of a list in code.
- The case facts a step answers on are reachable through rwb-source-data's contract: the exact operation and its product path are Not specified in the source documents (GAP-0638; ASM-1014).
- The login is the rwb-agent login (DP-02): its name is Not specified in the source documents (GAP-0638; ASM-1018).

### 4. Flow

1. The run of a decision step is started by its own trigger — an event such as CaseCreated for screening or DocumentStored for intake, or the stage workflow of the case — and the request names the step by its decision code. The step code, the case and the business date are input data; no step code is a constant of the service (AC4).
2. ResolveStepLevel reads the policy version in force for the agent and the step on the run date: status APPROVED, `valid_from` on or before the date, and `valid_to` empty or on or after it (AC7). At most one version is in force per agent, step and date; where two are, the step resolves nothing and reports a configuration exception that names both version labels (AC7).
3. The level is the `autonomy_mode` column of that version — L1, L2, SHADOW or OFF — read at run time and never from a class, an enumeration, a constant or a property file (AC3). The same row carries the model code and version, the output schema and the prompt version the run uses.
4. A step with no version in force resolves OFF: no agent call is made, no run row and no record are written, and the monitor shows the step as having no policy in force. No level is defaulted to L1 or to SHADOW (AC11).
5. At L1 the run answers and the answer is a recommendation: it is stored on the run and returned by the case agent-output read with its mode, its step, its policy version and the reference of the record, and no case field, task, assignment, queue or route is changed by the run. A person decides, and that decision is a decision of rwb-case recorded under its own decision code (AC1, AC9).
6. At L2 the run answers and acts under the version that a committee approved: the answer carries the approval reference of its version, and the record names the reference beside the step, the level and the version (AC2, AC6, AC9).
7. The run row records the level it ran under in `agent_run.autonomy_mode` and links its record through `agent_run.decision_log_id`; the row is written once for the key of the case, the step and the business date, and a rerun writes no second row (AC5).
8. RecordAndApply writes the decision record through the library in one `rwb_agent` transaction: `decision_code` carries the step, the record names the agent and prompt version, the model version and the policy version, and the level travels as the named member `autonomyMode` of `recommendation`; the outbox row for DecisionRecorded commits with it. A failed write rolls the whole transaction back, so no record, no outbox row and no answer exist (AC10; DP-03; R-UNI-39).
9. The DecisionRecorded row is relayed from the outbox to `rwb.decision-record.v1`, and rwb-decision seals it into the central ledger. The run waits for no confirmation: the level of a step is not a point of no return.
10. A new version takes effect at its `valid_from` and only when its status is APPROVED. A version in LOADED or RETIRED status changes no level, and the level a finished run recorded is never rewritten by a later version (AC5, AC7).
11. The version shows the approval reference of the committee approval that allowed it, as the legacy criterion requires, and the admin reads that carry it are answered on `/api/recovery/agent/v1/admin/agent-runs` and `/api/recovery/agent/v1/admin/agent-configs` (AC2, AC8; DP-13).
12. The risk and model risk officer reads the level per step on SCR-46 Agent monitor, in state Shadow, live or paused. The screen is served by the gateway-bff composite route, which calls the agent reads and merges them; the browser calls no owner service directly (AC8; DP-19).
13. Where a step answers on case facts, the tool gateway reads them through rwb-source-data's contract within one hop and a 2 s budget, and no `v_ace_*` view is granted to the rwb-agent login (DP-05; ASM-1014).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two policy versions are in force for the same agent, step and date | The step resolves no level, writes no run and no record, and the configuration exception names both version labels | None | AC7 |
| X2 | The policy version in force carries an `autonomy_mode` outside LOV-AUTONOMY | The configuration load refuses such a version, so it cannot be in force; where one is found on the row anyway the step resolves nothing, writes nothing and reports the row | MSG-GEN-001 | AC3 |
| X3 | No policy version is in force for the step on the run date | The step resolves OFF, calls no agent, writes no run row and no record, and the monitor shows the step with no policy in force | None | AC11 |
| X4 | The step code of the run is not a value of LOV-DECISION | The run is refused as a configuration exception and no row is written; no step code is invented or defaulted | None | AC4 |
| X5 | The decision record cannot be written | The transaction rolls back: no record, no outbox row and no answer reach a caller; the run is marked failed and is retried | MSG-P7-003 | AC10 |
| X6 | A caller without the Platform administration right opens the monitor route | Refused; nothing is returned and nothing is written | MSG-P4-002 | AC8 |
| X7 | The rwb-source-data contract returns an error or stale facts | The step answers on the case facts it holds or does not answer at all; it never substitutes a value of its own, and the run records that the fact set was incomplete | None | AC9 |
| X8 | A run is repeated for the same case, step and business date | No second run row, no second record and no second answer; the repeat is counted once in the run summary | None | AC5 |

The step writes no case field, raises no task and moves no case state on any path, so none of these exceptions moves a case. The rollback of X5 is the behaviour FSD P10 v3 AC-EXC-P10-012-02 describes, and the refusal of X6 is AC-EXC-P10-012-01.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P10-AD020-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON; the one in-lane dependency is RWB-P10-E1063-APP, because the level per step is read on SCR-46 and the run and evaluation reads behind that screen are its |
| Negotiable | The step scope of a version, the approval reference member, the response field names and the behaviour of a step with no version in force are agreed defaults, recorded as assumptions |
| Valuable | No agent acts beyond the level the committee approved, and every answer can be traced to the step, the level and the version that governed it |
| Estimable | One resolver, one level reader, one run writer, one record adapter, one client, no controller of its own |
| Small | Fits one sprint with its tests |
| Testable | Ten of the eleven criteria of section 7 are automated tests against the policy and run rows and the decision-record fake; one is a contract test of the gateway-bff route |

### 7. Acceptance criteria

```gherkin
Feature: Autonomy level per decision step

  Background:
    Given policy version "P1" governs step "D6.3" with autonomy_mode "L1" and is in force on 2026-12-15
    Given its model version is "MODEL-A-2026-10"

  Scenario: AC1 Level applied (legacy RWB-AD-020 AC1)
    Given step D6.3 at level L1
    When the route agent answers
    Then the system shows the answer as a recommendation and a person decides

  Scenario: AC2 Step up recorded (legacy RWB-AD-020 AC2)
    Given the rwb-decision contract mock returns the committee approval reference for L2
    Given a committee approval for L2
    When the new version takes effect
    Then the change shows the approval reference in the version

  Scenario: AC3 The level is a column of the policy version and never a value in code (new, D-RCV-60)
    Given policy version "P1" of step "D6.3" holds autonomy_mode "L1" and is in force on 2026-12-14
    Given policy version "P2" of the same step holds autonomy_mode "L2" and is in force from 2027-01-15
    When the run of step "D6.3" resolves its level on 2026-12-14 and again on 2027-01-15
    Then the first run resolves "L1" and the second resolves "L2", with no release, no redeploy and no code change between them
    Then no autonomy level is held in a class, an enumeration, a constant or a property file of rwb-agent, and the level is read from agent_policy.autonomy_mode of the version in force
    Then the level resolves to a value of LOV-AUTONOMY, and a value outside that list cannot be in force because the configuration load refuses it

  Scenario: AC4 The step is identified as data (new, D-RCV-60)
    Given step "D6.3" is a value of LOV-DECISION and the run request carries it as a decision code
    When the run of step "D6.3" resolves its level for case "RW-2026-000401"
    Then the step travels as a decision code in the run request, on the record through decision_code "D6.3", and on the run through decision_log_id
    Then no step code is written in a class, an enumeration, a constant or a property file
    When a run request carries a step code that is not a value of LOV-DECISION
    Then the run is refused as a configuration exception and no agent_run row and no record are written

  Scenario: AC5 The run records the level it ran under (new, D-RCV-60)
    Given policy version "P1" of step "D6.3" at autonomy_mode "L1" is in force on 2026-12-15
    When the run of step "D6.3" answers for case "RW-2026-000401" on 2026-12-15
    Then one agent_run row carries autonomy_mode "L1" and the decision_log_id of the record of the answer
    Then the step and the policy version of the run are read from that record, and the level is read from the row
    Then the row is written once for the key of case "RW-2026-000401", step "D6.3" and business date 2026-12-15, and a rerun writes no second row
    When version "P2" at autonomy_mode "L2" takes effect on 2027-01-15
    Then the autonomy_mode of the row of 2026-12-15 stays "L1"

  Scenario: AC6 The record carries the step, the level and the version (new, D-RCV-60)
    Given the run of AC5 answered at L1 under policy version "P1"
    When RecordAndApply writes the record through the decision-record library
    Then one record names decision_code "D6.3", the agent and prompt version, the model version "MODEL-A-2026-10" and the policy version "P1"
    Then the autonomy mode "L1" and the policy version "P1" travel as the named members autonomyMode and policyVersion of the record's recommendation
    Then the record's approval_level is not set from the autonomy mode, because LOV-APPROVAL-LEVEL is the delegation ladder L1 to L6 and its L1 is a different value
    Then the record, the agent_run row and the outbox row commit in one rwb_agent transaction, and rwb.decision-record.DecisionRecorded.v1 is written to the outbox on rwb.decision-record.v1
    Then no rule row and no Drools package version is named, because no Drools package decides this step

  Scenario: AC7 The change takes effect only when the approved version is in force (new, D-RCV-60)
    Given policy version "P2" of step "D6.3" holds autonomy_mode "L2", status "LOADED" and valid_from 2027-01-15
    When the run of step "D6.3" resolves its level for 2026-12-15 and for 2027-01-16
    Then neither run resolves "L2", because a version in LOADED status is not in force
    Given version "P2" is approved with the committee approval reference the rwb-decision contract answers, and its status is "APPROVED"
    When the run resolves its level for 2027-01-14 and for 2027-01-15
    Then neither run resolves "L2" before its valid_from and the run of 2027-01-15 resolves "L2"
    Given version "P1" is retired with valid_to 2027-01-14
    When a run of step "D6.3" asks for its level on 2026-12-15
    Then it resolves "L1", and a run with no version in force on its date resolves no level at all
    Given two versions of step "D6.3" are in force on 2027-01-15
    When a run asks for its level on that date
    Then it resolves no level, writes nothing and reports a configuration exception that names both version labels

  Scenario: AC8 The reads are reached through the gateway-bff route on the service base (new, D-RCV-60)
    Given the runs and the policy versions of step "D6.3" for 2026-12-15
    When the risk and model risk officer opens SCR-46 Agent monitor in state Shadow
    Then the levels per step are served by the gateway-bff composite route, which calls the agent reads on /api/recovery/agent/v1 and merges them
    And the browser calls no owner service directly
    Then the admin read is answered on GET /api/recovery/agent/v1/admin/agent-runs and on GET /api/recovery/agent/v1/admin/agent-configs, and no monolith base answers either
    Then each run answer carries the step, the autonomy mode, the policy version and the approval reference of its version
    Given user "U-5001" holds RW-REFADM, which has no Platform administration right
    When "U-5001" calls the same route
    Then the call is refused with 403 and MSG-P4-002 and nothing is written

  Scenario: AC9 An answer at L1 is a recommendation and moves nothing (new, D-RCV-60)
    Given policy version "P1" of step "D6.3" at autonomy_mode "L1" answered for case "RW-2026-000401" on 2026-12-15
    When a person reads GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs for that case
    Then the answer is returned with its mode "L1", step "D6.3", policy version "P1" and run reference, marked as a recommendation
    Then no case field, task, assignment, queue or route is written by the run, and the case holds the state it held before the answer
    Then the person's decision is a decision of rwb-case with its own decision code and its own record, and this step records none of it
    When the facts the step answers on are unavailable from rwb-source-data
    Then the answer says so and carries no substituted value, and the case still moves nothing

  Scenario: AC10 The record is written before the answer leaves and a failed write changes nothing (new, D-RCV-60)
    Given the decision-record library is forced to fail for the run of step "D6.3"
    When the run finishes its answer at L1 for case "RW-2026-000401"
    Then no record, no outbox row and no agent_outputs answer reach a caller
    Then the run is marked failed, the case moves nothing and the caller sees MSG-P7-003
    When the same run is retried with the library working
    Then one record, one outbox row and one answer exist for the key, and no second record exists for the same case, step and business date

  Scenario: AC11 A step with no version in force runs at OFF (new, D-RCV-60)
    Given no policy version of step "D6.3" is in force on 2026-12-15
    When the run of step "D6.3" is started for case "RW-2026-000401"
    Then the step resolves autonomy_mode "OFF" and no agent call is made
    Then no agent_run row, no record and no agent_outputs answer exist for the key
    Then the monitor shows the step as having no policy in force, and no level is defaulted to L1 or to SHADOW
```

**Target reading.** AC2 carries one inserted line, as its first Given: `Given the rwb-decision contract mock returns the committee approval reference for L2`. The legacy criterion asserts that the change shows the approval reference in the version, and the reference is created and held by rwb-decision (P7) — the `approval` row and its `GET /api/recovery/decision/v1/approvals/{approvalId}` read — so the criterion can only be tested with that read faked. Every legacy line and value is kept: a committee approval for L2, the new version taking effect, and the approval reference in the version.

AC1 carries no inserted line, and no mock is needed for it: every fact it asserts is a row of `rwb_agent` — the step and the level come from the policy version, the answer from the service's own run, and the presentation as a recommendation from the service's own agent-output read. The person's decision is an act of rwb-case and is not asserted as a read of another service, so nothing is stubbed. The one thing the criterion leaves open — the agent that answers at step D6.3, since no value of LOV-AGENT names a route agent — is Not specified in the source documents (GAP-0638; ASM-1013) and the criteria identify the run by its step instead.

AC3 to AC11 are new and test only this service change: the level as a column read at run time, the step as data, the level recorded on the run, the record members, the take-effect rule, the gateway-bff exposure on the service base, the recommendation behaviour at L1, the record-before-answer rule, and the OFF path.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The autonomy level of a step is held as data and changed only with committee approval; an agent never acts beyond what the committee approved | Legacy RWB-AD-020 story and AC1, AC2; FEAT-AGT-12; FEAT-AGT-15 |
| BR2 | No value a business person may change is written in code: the level, the step scope, the model version and the approval reference are rows of the policy version in force, read at run time | BR-P10-012; BR-P10-015; legacy RWB-AD-020 guardrails |
| BR3 | A version is in force only when its status is APPROVED and its `valid_from`..`valid_to` window contains the run date; at most one version is in force per agent, step and date | TSD P10 v2 T3.1 DF-AGT-021, DF-AGT-022 and DF-AGT-023; ASM-1012 |
| BR4 | The step is a decision code of LOV-DECISION and is carried as data on the request, on the run and on the record; no step code is a constant of the service | LDM v8 DF-DEC-003 and the LOV-DECISION row; legacy RWB-AD-020 AC1 (step D6.3) |
| BR5 | The level a run ran under is the `autonomy_mode` of its `agent_run` row and is never rewritten when a later version takes effect; the step and the version of the run are read from its record through `decision_log_id` | TSD P10 v2 T3.1 DF-AGT-043 and DF-AGT-058; legacy RWB-AD-020 AC1 |
| BR6 | The record is written before the answer leaves and no answer proceeds unrecorded: the record, the run row and the outbox row are one transaction, and a failed write changes nothing | Principle 5; R-UNI-39; FSD P10 v3 AC-EXC-P10-012-02; DP-03 |
| BR7 | The autonomy mode is not carried on `approval_level`: that field is the delegation ladder L1 to L6 of LOV-APPROVAL-LEVEL, and its L1 is a different value from the autonomy L1 | LDM v8 DF-DEC-011 and DF-DEC-038; TSD P10 v2 T3.2 LOV-AUTONOMY; ASM-1015 |
| BR8 | At L1 the answer is a recommendation and a person decides; the run writes no case field, no task, no assignment, no queue and no route | Legacy RWB-AD-020 AC1; FSD P10 v3 A2.12; TSD P10 v2 T-A.2 API-P10-010 |
| BR9 | A step with no version in force resolves OFF and runs nothing; no level is defaulted and no agent is called | TSD P10 v2 T3.2 LOV-AUTONOMY (OFF); ASM-1016 |
| BR10 | The case facts a step answers on are read through rwb-source-data's contract and never from a `v_ace_*` view of this service; no table of another schema is read | DP-05; DP-01; ADR-010; ASM-1014 |
| BR11 | The admin reads are answered on the service base and reach the screen through the gateway-bff composite route; the browser calls no owner service | DP-13; DP-19; legacy RWB-AD-020 endpoint and screen tables |
| BR12 | An agent or a model that does not answer inside its timeout falls back to the rule result and the fallback is recorded on the decision; the level resolution never blocks the fallback | R-UNI-32; TSD P10 v2 NFR-010 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | APPROVED | the committee approval is recorded and the reference is written on the version | APPROVED, not yet in force |
| APPROVED | IN_FORCE | the run date reaches `valid_from` and is on or before `valid_to` | IN_FORCE, one version per agent and step |
| APPROVED | RETIRED | the version is retired before or at its `valid_to` | RETIRED, which resolves no level |
| IN_FORCE | SUPERSEDED | a later approved version reaches its `valid_from` | SUPERSEDED, and the level it set is not rewritten on any finished run |
| NO_VERSION | RESOLVE | no version is in force for the step and the date | OFF, with no run and no record |

These are the states of a policy version and of the resolution, not a case state machine. No column holds the words IN_FORCE or SUPERSEDED: they are read from `status`, `valid_from` and `valid_to` (TSD P10 v2 T3.1), so the table states the reading and not a new column. **This story moves no case status**: `recovery_case.status` is neither read nor written, no task and no assignment row is written, and the case side of an agent answer belongs to rwb-case (BR8).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Risk and model risk officer (RW-RISK) | The primary reader of the level per step on SCR-46 and the role that approves a level change; decisions on agents are prepared for this role |
| Center of excellence analyst (RW-COE) | Loads and maintains the policy versions, their step scope and their level; reads the level per step |
| Platform administrator (RW-PLATADM) | Reads the runs and their levels, and may rerun a step for a business date |
| Data steward and data product owner (RW-DATASTEW) | Reads the level per step and the runs it governed |
| RW-AUDIT, RW-COMPLY, RW-SECADM | Read the level per step and the records through the monitor read, as the legacy permission list allows |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the step; reads the policy version and the case facts through their contracts; writes the run row, the record and the outbox row |
| Decision-record library identity | Writes the local record and its outbox row |
| SY-RULES rules identity | Not used by this story: no Drools package decides a step of the agent runtime, so no rule row and no package version is read |
| RW-REFADM | Holds no Platform administration right; refused on the monitor route with MSG-P4-002 |

The legacy permission list of RWB-AD-020 gives Platform administration R to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM, and TSD P10 v2 T6.1 gives the same six roles R or more, so the two agree and no right is reconciled here. The per-service login name is Not specified in the source documents (GAP-0638; ASM-1018); the story names it "the rwb-agent login (DP-02)" until it is agreed. The agent code that runs the D6 route step is likewise Not specified (GAP-0638; ASM-1013), so every criterion identifies the run by its step.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-001 to DF-AGT-025 | agent_policy | agent_code, policy_version, model_code, model_version, output_schema_ref, autonomy_mode, valid_from, valid_to, status, promotion_conditions, loaded_by, approved_by | Read |
| DF-AGT-036 to DF-AGT-060 | agent_run | id, agent_code, autonomy_mode, status, decision_log_id, case_id, run_at, data_as_of, model_version, prompt_version | Read, and write `autonomy_mode` on the run row |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | decision_code, agent_version, model_version, recommendation, approval_level, final_call, decided_at, prev_hash, entry_hash | Write locally through P7's library |
| DF-AGT-018 | agent_policy | promotion_conditions | Read: the member that names the step the version governs (ASM-1010) |
| DF-AGT-025 | agent_policy | approved_by | Read: the committee approval recorded on the version, beside the approval reference (ASM-1011) |
| LOV-DECISION, LOV-AUTONOMY, LOV-CONFIG-STATUS | reference data (rwb_case, owner P3, §R3 default ruling) | D1 to D9 with sub-decisions and X1 to X7; OFF, SHADOW, L1; LOADED, APPROVED, RETIRED | Read as values, never as a table of this service |
| DF-ACE-270 to DF-ACE-279 | v_ace_score (rwb_source_data, owner P1) | the case and account facts a step answers on | Read through rwb-source-data's contract (DP-05), never from a view |
| DF-WRK-009 to DF-WRK-016 | assignment (rwb_case, owner P3) | No longer read or written by this slice: an answer at L1 changes no case, no task and no assignment | Not used |

Field IDs are those of the Logical Data Model and Data Dictionary v9. The step, the level and the version are three reads of `rwb_agent` and one write through P7's library; no foreign key crosses a schema (DP-01). The policy version names its step through a jsonb member because no column of `agent_policy` names a decision; the member, its key and the fallback of a dedicated column are Not specified in the source documents (GAP-0638; ASM-1010). The approval reference is likewise Not specified as a column (GAP-0638; ASM-1011): `approved_by` names a person and no source adds a reference column, so the reference travels in the same jsonb. The record carries the level and the version as members of `recommendation` for the reason stated in BR7. No personal data is added by this story: the run row holds identifiers, the step, the level and the version, and the record holds identifiers and business facts.

### 12. Contract

#### 12.1 REST operations provided

None new. This story adds the step and the level to the answers of three reads that rwb-agent already provides and that other stories implement: `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001, the run list of the agent monitor, owned by RWB-P10-E1063-APP), `GET /api/recovery/agent/v1/admin/agent-configs` (API-P10-002, the policy and prompt version list, owned by the agent platform set-up and the autonomy change stories) and `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` (API-P10-010, the L1 agent outputs of a case, TSD P10 v2 T-A.2). The three answers gain `step`, `autonomyMode`, `policyVersion` and `approvalRef` as backward-compatible additions, and the field names are fixed by RWB-P10-AD020-CON and recorded as an assumption until the wave 4 contract freeze (GAP-0638; ASM-1017).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-0638; ASM-1014) | rwb-source-data (P1) | The case facts a step answers on, read by the tool gateway and never from a view (DP-05) | One hop, 2 s |

No `POST /api/recovery/access/v1/authorise` call is made by the resolution: the level read runs under the service identity on the service's own table, and the rights on the admin reads belong to the stories that own those reads. No read of rwb-decision is made at run time either: the approval reference is written on the version when the version is approved, and the read of it is the admin read of 12.1.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, decision code (the step), agent code, agent and prompt version, model version, policy version, autonomy mode, final call |

The row is written to the outbox in the same transaction as the run row and relayed with the CloudEvents envelope (DP-03). No agent event is published by this story: the P10 OUT line of Arch v5 slide 16 names AgentRunCompleted only, that event is `rwb.agent.AgentRunCompleted.v1` (EV-28) on the service topic `rwb.agent.events.v1`, it belongs to the run story, and a level resolution is read from the table through the admin reads and not from a topic. No personal data is carried.

#### 12.4 Events consumed

None. The step is started by its trigger in the run stories and reads no topic; it has no inbox handler of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| AgentRunWorkflow | Existing workflow of the agent runtime (owned by the run story) | `rwb-agent` | Carries the step in its input, drives the three activities below, and gives up the answer after 60 s to the rule result (R-UNI-32; Arch v5 slide 16) |
| ResolveStepLevel | Activity | `rwb-agent` | Reads the policy version in force for the agent, the step and the run date, returns its level, its version label, its approval reference and its model version, and returns OFF where no version is in force |
| RunAgentStep | Activity | `rwb-agent` | Calls the agent or model through the model gateway within the timeout and returns the answer with its mode |
| RecordAndApply | Activity (workflow kit) | `rwb-agent` | Writes the run row with the level it ran under, the record through the library and the outbox row in one transaction |

No new workflow template is defined: the resolution joins the existing AgentRunWorkflow on the queue `rwb-agent`, and the four steps of the workflow model apply to it (Temporal and Drools design slide 13).

#### 12.6 Schedules

None. The run has no Schedule of its own: it is started by an event or by a stage workflow, and the level resolution inherits that start. No Schedule is created, changed or owned by this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_policy | P10 (rwb_agent) | Read only here: the version in force, its `autonomy_mode`, its `valid_from`, `valid_to`, `status`, its step member and its approval |
| agent_run | P10 (rwb_agent) | Written here for `autonomy_mode` and `decision_log_id`; created by the agent runtime baseline migration, not by this story |

`decision_log_entry` is a rwb-decision table and is written only through the P7 library (DP-01, DP-03). The case facts are read from rwb-source-data and no copy of a case or score row is written into `rwb_agent`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock | The P7 approval read (DP-03 side) | `GET /api/recovery/decision/v1/approvals/{approvalId}` returning the committee approval reference of an L2 version; a 404 for an unknown reference |
| Decision-record library stub | The P7 record contract and `rwb.decision-record.v1` (DP-03) | A committed record with its reference; a forced write failure; the outbox row and its relay |
| gateway-bff composite route stub | The DP-19 route of SCR-46 | The merged screen answer with the runs, their steps and their levels; the refusal of a role without Platform administration R with MSG-P4-002 |
| rwb-source-data WireMock | The P1 case-fact contract (DP-05) | Case facts of case "RW-2026-000401"; an error answer; facts older than the business date |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The rwb-source-data case-fact read and the rwb-decision approval read used by the contract tests; one hop, 2 s; no operation is provided by this story |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox; nothing consumed |
| Temporal | 0 workflows, 3 activities | ResolveStepLevel, RunAgentStep and RecordAndApply on the queue `rwb-agent`, inside the existing AgentRunWorkflow |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `autonomy`, Java package `th.co.scb.ace.workbench.recovery.agent.autonomy`. No front-end module: the screen is the monitor story's, and this story feeds it through the gateway-bff route.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/agent/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 resolves to the rwb-source-data contract and to no view of this service: the case facts are not copied into `rwb_agent`, so no `v_ace_*` view is granted to the rwb-agent login (ADR-010). DP-13 and DP-19 add no build dependency of their own; the two H dependencies of the table are platform contract stories and the other two H rows are the service's own contract story and the monitor story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| StepLevelResolver | Service | Reads the policy version in force for the agent, the step and the date, applies the take-effect rule and returns the level, the version label, the approval reference and the model version, or OFF |
| StepCodeGuard | Service | Refuses a step code that is not a value of LOV-DECISION and a configuration with two versions in force, and names the row it refused |
| AgentRunWriter | Repository | Writes the `agent_run` row with `autonomy_mode` and `decision_log_id`, holds the key of case, step and business date, and counts a repeat |
| RecommendationPresenter | Service | Shapes the answer of a step at L1 as a recommendation with its mode, step, version and run reference, and asserts no applied outcome |
| DecisionRecordWriter | Library adapter | Writes the local record with `decision_code`, the member `autonomyMode`, the policy version and the model version, hash-linked, in the same transaction (DP-03) |
| SourceFactClient | Client | Calls the rwb-source-data operation with one hop, the 2 s timeout and a breaker per downstream (DP-05) |
| Controller | None | The step exposes no operation of its own; the level reaches the screen through the admin reads and the gateway-bff route |

**Database and migrations**

- No new table and no new column in this story. `agent_policy` and `agent_run` and their fields come from the agent runtime baseline migration of `rwb_agent`, which RWB-P10-E1058-APP owns (TSD P10 v2 T3.1).
- The step scope of a version is a named member of `agent_policy.promotion_conditions` until a `decision_code` column is agreed; the member is read through one accessor so that a column can replace it without touching a caller (ASM-1010).
- If the wave 4 review adds the column, the script that adds it takes its number from the rwb-agent Flyway sequence; that number is Not specified in the source documents (GAP-0638; ASM-1010) and no number is claimed here.
- Two indexes serve the read and the key: `agent_policy (agent_code, status, valid_from, valid_to)` and `agent_run (case_id, decision_log_id)`. The index names are naming-library values and not business values.

**Configuration and reference data**

- Policy versions in force (RW-COE): `agent_code` over LOV-AGENT, `policy_version`, the step, `autonomy_mode`, `model_code`, `model_version`, `output_schema_ref`, `valid_from`, `valid_to`, `status`, and the approval reference of the version. The step member key and the approval reference member are Not specified in the source documents (GAP-0638; ASM-1010 and ASM-1011).
- List values of TSD P10 v2 T3.2 and of the LDM: LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-AGENT and LOV-DECISION, held as reference data by rwb-case under the §R3 default ruling; the step reads the value of the row and holds no copy of a list in code.
- The level names used by this story are the legacy L1 and L2 of the two criteria and the list values OFF, SHADOW and L1; L2 is not yet a value of LOV-AUTONOMY (GAP-0638; ASM-1012), and the story defines no further level.
- The agent code of the D6 route step is not fixed by any source (GAP-0638; ASM-1013); the configuration names the step and the policy version, and the run is identified by the step.

**Build steps**

1. StepLevelResolver against the two-version and the retired-version fixtures, with the take-effect rule and the two-in-force refusal; tests for AC3 and AC7.
2. StepCodeGuard over LOV-DECISION, with the refusal of an unknown step and of a duplicate version in force; test for AC4.
3. AgentRunWriter with the key of case, step and business date, the level it ran under, the record link and the rerun guard; tests for AC5.
4. DecisionRecordWriter with `decision_code`, the two members of `recommendation` and the rollback path, and the assertion that `approval_level` is left alone; tests for AC6 and AC10.
5. RecommendationPresenter and the agent-output answer at L1, with the absence of any applied outcome; test for AC9.
6. SourceFactClient against the rwb-source-data fake, with the 2 s timeout and the breaker; test for AC9.
7. The OFF path and the "no policy in force" reading of the monitor; test for AC11.
8. The gateway-bff route contract test on the two admin reads and the refusal path; test for AC8.
9. Register the resolution in the AgentRunWorkflow input and run it for a business date over synthetic rows; tests for AC1 and AC2 against the legacy values.

**Done when.** The tests in section 16 pass, no level is a constant of the service, every finished run names the level it ran under and the record that carries its step and version, a version in LOADED status changes no level, and no run of the SIT week ran at a level that was not in force on its business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of a policy version is empty, or an autonomy mode is outside its list at the load | Enter {field}. |
| MSG-P4-002 | A role without the Platform administration right opens the monitor route | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written for the run | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three messages are the legacy messages of RWB-AD-020 and keep their wording character for character. MSG-GEN-001 is the message of VR-P10-012-1 and VR-P10-015-1 of FSD P10 v3, and MSG-P4-002 and MSG-P7-003 are the messages of AC-EXC-P10-012-01 and AC-EXC-P10-012-02. This story adds no message: the refusal of an unknown step and the report of two versions in force are configuration exceptions with no message in any source, and they are raised as run failures and logged, not shown to a person.

### 15. Screens and states

SCR-46 Agent monitor, in its legacy states Shadow, live and paused, shows the runs of a step with the step, the autonomy mode, the policy version and the approval reference beside the run outcome (legacy RWB-AD-020 screen and states; FSD P10 v3 screens). The screen and its read belong to RWB-P10-E1063-APP; what this story adds is the data, and it is served by the gateway-bff composite route, which calls the two admin reads on `/api/recovery/agent/v1` and merges them (DP-19). The three states are the legacy states of the screen and this story changes none of them: Shadow and live describe what the monitor shows, and paused describes the run switch. No level is mapped to a screen state by this story, and the screen fields, their order and their masking are Not specified in the source documents (GAP-0638; ASM-1017).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-020-01 | AC1 | Component | Policy version "P1" of step "D6.3" at L1 in force on 2026-12-15; one run of the route step; the agent-output read of case "RW-2026-000401" |
| TC-AD-020-02 | AC2 | Component | Version "P2" of step "D6.3" at L2 with the approval reference the rwb-decision stub answers; `valid_from` 2027-01-15; status APPROVED |
| TC-AD-020-03 | Access | Component | User "U-5001" holding RW-REFADM calls the SCR-46 route; refused with MSG-P4-002 |
| TC-AD-020-04 | Principle 5 | NFR | Decision-record write forced to fail on the run of step "D6.3"; no record, no outbox row and no answer |
| TC-AD-020-05 | AC3 | Component | "P1" at L1 in force to 2030-01-14 and "P2" at L2 from 2027-01-15; the same run started on both dates, no redeploy |
| TC-AD-020-06 | AC4 | Component | Step code "D6.3" of LOV-DECISION and the step code "D6.9", which is outside the list |
| TC-AD-020-07 | AC5 | Component | Run for case "RW-2026-000401" on 2026-12-15 at L1, run twice, then a version at L2 taking effect on 2027-01-15 |
| TC-AD-020-08 | AC6 | Component | The record library stub; an L1 run under "P1"; a step with no Drools package |
| TC-AD-020-09 | AC7 | Component | "P2" LOADED then APPROVED from 2027-01-15; runs on 2027-01-14, 2027-01-15 and 2027-01-16; "P1" retired at 2027-01-14; a second version in force on the same date |
| TC-AD-020-10 | AC8 | Contract | gateway-bff route stub with the runs and the versions; the refusal of RW-REFADM; the two admin reads on the service base |
| TC-AD-020-11 | AC9 | Component | L1 run for "RW-2026-000401"; the case snapshot before and after the answer; the agent-output read; the rwb-source-data error path |
| TC-AD-020-12 | AC10 | NFR | The record library failing, then working, on the same case, step and business date |
| TC-AD-020-13 | AC11 | Component | No policy version in force for step "D6.3" on 2026-12-15 |

The legacy levels map System to Component, Access to Component and Principle 5 to NFR, because the cross-service behaviour of this key is proved by the integration story of the wave. No `-ITG` copy is held here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the level, the step scope, the model version, the approval reference and the take-effect dates are rows of the policy version in force (BR-P10-012, BR-P10-015).
- No personal data in logs, tests, workflow history or prompts: the run and the record hold identifiers, the step, the level and the version; the case facts the step answers on are consumed and never written to a log, and the workflow payloads pass the payload codec.
- No read of another service's tables: the case facts come through rwb-source-data's contract, the record is written through the P7 library, and `rwb_agent` holds no foreign key into another schema (DP-01, DP-05).
- The record is written before the answer leaves, in one transaction with the run row; a failed write rolls the whole transaction back (R-UNI-39).
- The step writes no case field, task, assignment, queue or route, and no case state is read or written for a level (BR8).
- The level a finished run recorded is never rewritten; a later version changes what a later run does and nothing else.
- A step with no version in force runs nothing and no level is defaulted (BR9).
- The autonomy mode never travels on `approval_level`, and no DoA delegation value is read or written by this story.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | The autonomy level of each agent step is held as data and changed only with committee approval, so that an agent never acts beyond what the committee approved | No BRD section carries the feature (GAP-0638) | FEAT-AGT-12 | All recovery processes (legacy RWB-AD-020) | BR-P10-012 | TC-AD-020-01, TC-AD-020-05 |
| None (the legacy story carries no requirement ID) | A step up records the approval reference of the version that takes effect | No BRD section carries the feature (GAP-0638) | FEAT-AGT-15 | All recovery processes (legacy RWB-AD-020) | BR-P10-015 | TC-AD-020-02, TC-AD-020-09 |
| BR-P10-012 | No value a business person may change is written in code; it is read from reference data with its version | FSD P10 v3 A2.12.3.1 | FEAT-AGT-12 | All recovery processes | BR-P10-012 | TC-AD-020-05, TC-AD-020-06 |
| BR-P10-015 | No value a business person may change is written in code; it is read from reference data with its version | FSD P10 v3 A2.15.3.1 | FEAT-AGT-15 | All recovery processes | BR-P10-015 | TC-AD-020-09 |
| D-RCV-60 DP-03 | The decision record is written locally before the action and the shared topic carries it to the central ledger | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-AGT-12 | All recovery processes | R-UNI-39 | TC-AD-020-08, TC-AD-020-04 |
| D-RCV-60 DP-05 | The case facts are read through the owner's contract and never from a table | Template and Rules §R5.5; Architecture v5 slide 16 | FEAT-AGT-12 | All recovery processes | None | TC-AD-020-11 |
| D-RCV-60 DP-13 | The service answers on its own REST base | Template and Rules §R5.5 | FEAT-AGT-12 | All recovery processes | None | TC-AD-020-10 |
| D-RCV-60 DP-19 | The screen composes its answer through the gateway-bff route and calls no owner service directly | Template and Rules §R5.5; Architecture v5 slides 13 and 41 | FEAT-AGT-12 | All recovery processes | None | TC-AD-020-10, TC-AD-020-03 |
| R-UNI-32 | The agent or the model that does not answer inside the timeout falls back to the rule result and the fallback is recorded | Business Rules and Routing Logic v4, Universal rules | FEAT-AGT-11 for the fallback | All recovery processes | R-UNI-32 | TC-AD-020-01 |

The legacy story RWB-AD-020 carries no requirement ID: it names its feature as None and no BRD in the extracts carries FEAT-AGT-12 or FEAT-AGT-15, so no BRD section and no requirement is cited and the absence is recorded as GAP-0638. The feature source is FSD P10 v3 A2.12 and A2.15; the rules are BR-P10-012 and BR-P10-015; the decision is D-RCV-60; the regulator context is the BOT AI Risk Management Guidelines of 12 Sep 2025 (Arch v5 slides 35 and 50).

### 19. Out of scope

- The load, the approval and the rollback of a policy version (FEAT-AGT-12; RWB-P10-E3030-APP and RWB-P10-E3030-CON).
- The raise or lower of a level with approval, its evidence and its committee step (FEAT-AGT-15; RWB-P10-E8004-APP and RWB-P10-E8004-CON).
- The review of agent risk at the committee, which reads the levels and the records (FEAT-AGT-16; RWB-P10-E8005-APP).
- The agent monitor, SCR-46, its states and its read (RWB-P10-E1063-APP), which this story waits for.
- The agent run itself, the guardrail checker, the tool gateway and the 60-second rule fallback of the run (FEAT-AGT-01, FEAT-AGT-02, FEAT-AGT-11; RWB-P10-E1058-APP).
- The evaluation harness and the extraction evaluation (FEAT-AGT-05; RWB-P10-E1060-APP).
- The drift check and the cost-cap alert (FEAT-AGT-06, FEAT-AGT-13; RWB-P10-E1063-APP and RWB-P10-E3031-APP).
- The ladder of autonomy levels beyond the values the sources name, and the ownership of LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-DECISION, which is rwb-case's under the §R3 default ruling.
- The roles, the rights, the scope and the masking rules (P4 rwb-access), the delegation table and its L1 to L6 ladder (P7 rwb-decision), and the central ledger and its sealing (P7).
- The case facts themselves and the data products that carry them (P1 rwb-source-data).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
