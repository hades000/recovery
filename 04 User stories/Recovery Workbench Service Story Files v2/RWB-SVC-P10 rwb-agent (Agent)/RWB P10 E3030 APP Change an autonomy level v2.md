# RWB-P10-E3030-APP Change an autonomy level

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E3030-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P10-H |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P10-E3030-APP-16) |
| Depends on (build) | RWB-P10-E3030-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-030 for rwb-agent. The autonomy level stops being a row of the shared configuration service and becomes `autonomy_mode` of a versioned `agent_policy` row in `rwb_agent` (DP-01; TSD P10 v2 T3.1, DF-AGT-008); the version is loaded and approved on the rwb-agent configuration operations published under `/api/recovery/agent/v1` (DP-13; TSD P10 v2 API-P10-002 to API-P10-004) and reached through the gateway-bff composite route for SCR-46 (DP-19); the change is recorded through the local decision-record library and the shared topic `rwb.decision-record.v1` in the transaction that writes the version (DP-03). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E3030-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 8 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **to change the autonomy level of one agent as a versioned configuration row of the service that runs the agent — loaded by the center of excellence as a checked file, approved by me, recorded with the version that is now in force, and read by the run step at run time**, so that **an agent prepares the work and people decide where they must, and no change to what an agent may do unattended takes effect without a dated version, an approver and a decision record behind it**.

### 2. Business rationale

The legacy story RWB-E3-030 gave the risk and model risk officer one administrative step: change the autonomy level for one agent and one decision as a versioned configuration row, and write the result to the decision log with the rule version, with nothing changed when the log cannot be written (FEAT-AGT-12; FSD P10 v3 A2.12; Epics 3 to 8 Specification v3 row E3 · P10 · FEAT-AGT-12). It is an Admin feature of Epic 3, priority Should, read on SCR-46 Agent monitor in the states Shadow, live and paused, and its only operation in the legacy story is the monitor read `GET /admin/agent-runs` under Platform administration R. Its configuration path is served by Epic 1 and its approvals path by Epic 2, and the Epic 8 administration screen presents the same rows, so no second store is created for autonomy (GAP-1480). The BOT AI Risk Management Guidelines of 12 Sep 2025 put lifecycle risk management and a human decision on material actions behind every agent, which is what an autonomy level written and approved as data makes provable (Arch v5 slide 35 and the guideline row of the extract).

In the target the configuration row lives where the agent lives. rwb-agent owns the agent policies, the prompts, the runs, the guardrails and the evaluations in schema `rwb_agent` (Arch v5 slide 41), and the level is the `autonomy_mode` column of `agent_policy`, whose list is LOV-AUTONOMY — OFF, SHADOW and L1 — with the version status in LOV-CONFIG-STATUS, LOADED, APPROVED and RETIRED (TSD P10 v2 T3.1 DF-AGT-008 and DF-AGT-021, T3.2). A prompt version is the same shape in `agent_prompt` (DF-AGT-026 to DF-AGT-035), and the load carries a `kind` that selects one of the two (TSD P10 v2 API-P10-002). The legacy prerequisite FEAT-CWC-22 — the parameter catalog and configuration service of P3 — is therefore not read for this row: the parameter catalog keeps the parameters that are not agent configuration, and `parameter_catalog` and `parameter_value` stay with rwb-case under the §R3 default ruling (DP-01). That is the first realignment: the autonomy level is no longer a shared parameter row but a version of the owning service's own table. The unit of change is one agent's version, and the finer key that makes a level apply to one decision step belongs to the per-decision story, because `agent_policy` carries no decision column (GAP-0636; ASM-0993).

The second is the record. The legacy step wrote the decision log in process; the target writes the version row, the local decision record and the outbox row in one transaction, and the relay publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for rwb-decision to seal (Temporal and Drools design slide 11 and slide 16; R-UNI-39; DP-03). That is what turns legacy AC2 from a promise into a property: if the record cannot be written, the version row is not written either, so nothing changes. The record names the configuration version in its rule-version element, because no Drools package is evaluated on a configuration change and `rule_row` stays with rwb-decision (DP-04 is not a pattern of this story; ASM-0998).

The third is the seam. The load and the approval are the two admin operations the service already publishes — `POST /admin/agent-configs` and `POST /admin/agent-configs/{versionId}/approve`, with the read `GET /admin/agent-configs` — under the per-service base `/api/recovery/agent/v1` (DP-13; TSD P10 v2 API-P10-002 to API-P10-004; Ownership Map v1). The screen that shows the change is SCR-46 Agent monitor, served by the gateway-bff composite route, so the browser calls no owner service directly (DP-19; Arch v5 slides 8, 10 and 20). The gate on the loader approving their own version is the four-eyes rule the platform already states with MSG-P7-002 (FSD P10 v3 A2.1 AC-EXC-P10-001-03).

The step-up and step-down of a level on measured evidence is FEAT-AGT-15 and the Epic 8 key RWB-E8-004; the autonomy level per decision step is FEAT-ADM-01 and the Administration key RWB-AD-020. This story owns the plain change of one agent's version and nothing else. It owns both legacy criteria of RWB-E3-030 — AC1 and AC2 — and copies them verbatim in section 7; AC3 to AC9 are new and test the microservice deliverable of the title only. The legacy story carries no requirement ID and no BRD in the extracts carries FEAT-AGT-12, which section 18 records (GAP-0636).

### 3. Preconditions

- RWB-P10-E3030-CON is published: the shape of a configuration version, the three operations with their rights, errors and Idempotency-Key rule, the decision-record payload written on a change, the ordering rule that a version takes effect only after approval, the message set and the contract fakes (GAP-0637).
- RWB-PLT-E1027-CON is published: the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1` with its CloudEvents envelope. This story writes its record through the library and never writes the shared topic directly (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route contract for SCR-46 and its stub, so the exposure of the change is built and tested before the screen story lands (DP-19).
- The `rwb_agent` schema exists with the agent runtime baseline migration that carries `agent_policy` (DF-AGT-001 to DF-AGT-025) and `agent_prompt` (DF-AGT-026 to DF-AGT-035). RWB-P10-E1058-APP owns the schema and the baseline; this story issues no migration of its own and adds no table and no column (ASM-1001).
- A policy version is in force for the agent before the change: its `status` is APPROVED and the business date falls within `valid_from` and `valid_to`; the change is a new version and never an edit of the one in force (FSD P10 v3 A2.1 AC-ALT-P10-001-01).
- The lists used by the load are those of TSD P10 v2 T3.2: LOV-AGENT (INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER), LOV-AUTONOMY (OFF, SHADOW, L1), LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED), LOV-PRODUCT (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED) and LOV-REGION. The list rows are reference data of rwb-case under the §R3 default ruling; the wiring of the reference-data contract is the platform set-up story's (DP-07 with H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON there), and this story adds no list of its own and holds no copy of a list in code (ASM-0997).
- The version label is free text inside `policy_version` and `prompt_version`, both varchar(20). The labels P1 and PR1 of the FSD examples are illustrative and no format rule is stated (GAP-0636; ASM-0996).
- The approver is a person other than the loader, as the four-eyes rule requires; the approval instant is read from `updated_at` of the row at the APPROVED transition, because `agent_policy` carries `approved_by` and no `approved_at` column (GAP-0636; ASM-0996).
- The login is the rwb-agent login (DP-02): its name is Not specified in the source documents (GAP-0636; ASM-1003).

### 4. Flow

1. The center of excellence analyst (RW-COE) prepares one checked file for one agent and one kind, POLICY or PROMPT. The file carries the fields of the FSD field catalog and of the policy table: the agent code, the version label, the autonomy mode, the model code and version, the output schema reference, the allowed tools and the segment product group and region (FSD P10 v3 A2.12.3.2; TSD P10 v2 T3.1), together with the remaining policy fields of the version — the confidence floor, the timeout, the daily cost cap, the price per 1k tokens, the alert role, the review date, the promotion conditions, the watched measures, the fallback rule and the valid-from date.
2. The analyst calls `POST /api/recovery/agent/v1/admin/agent-configs` with the file, the kind, the agent and the valid-from date, and an `Idempotency-Key` header (TSD P10 v2 API-P10-003 and T-A.2).
3. AgentConfigValidator checks the file against the field catalog and against the lists. A required value that is empty is refused with 422 and MSG-GEN-001 naming the field; a value outside its list is refused with 422 naming the field; a file that fails a further check is refused with 422 and no version row is written, and the version in force stays in force (FSD P10 v3 A2.1 AC-EXC-P10-001-02; VR-P10-012-1).
4. The version is written as one `agent_policy` row, or one `agent_prompt` row when the kind is PROMPT, with status LOADED, `loaded_by` the caller and `valid_from` the date of the file. No other schema is written: no `parameter_catalog` and no `parameter_value` row of rwb-case, and no `rule_row` of rwb-decision (DP-01).
5. The risk and model risk officer (RW-RISK) approves the version with `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` and an `Idempotency-Key` header (TSD P10 v2 API-P10-004 and T-A.2). The operation is refused with 409 and MSG-P7-002 when the caller loaded the version (FSD P10 v3 A2.1 AC-EXC-P10-001-03); it is refused with 404 when the version does not exist.
6. RecordAndApply runs in one `rwb_agent` transaction: it moves the version to APPROVED with `approved_by`, it writes the local decision record that names the agent, the kind, the configuration version, the autonomy level, the version that was in force before, the approver role and the valid-from date, and it inserts the DecisionRecorded row in the outbox. A failed record write rolls the whole transaction back, so the version keeps status LOADED and no outbox row exists (DP-03; R-UNI-39; legacy AC2).
7. The DecisionRecorded row is relayed from the outbox to `rwb.decision-record.v1`, and rwb-decision seals it into the central ledger. The request waits for no confirmation: an autonomy change is not a point of no return.
8. A version is in force for a business date when its status is APPROVED and the date falls within `valid_from` and `valid_to`. The run step reads `autonomy_mode` from the row in force at run time and writes the value it used into `agent_run.autonomy_mode`; it reads no cache and no copy of the level is held anywhere (DP-01; TSD P10 v2 DF-AGT-043).
9. A repeat of the load or of the approval with the same `Idempotency-Key` returns the first answer and writes nothing: no second version row, no second record and no second outbox row (TSD P10 v2 T-A.2; R-UNI-40).
10. The analyst and the risk officer read the version and its state on SCR-46 Agent monitor. The screen is served by the gateway-bff composite route, which calls the config read on `/api/recovery/agent/v1` and merges the answers; the browser calls no owner service directly (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field of the file is empty | The load is refused with 422 before any row is written, and the field is named | MSG-GEN-001 | AC3 |
| X2 | The autonomy mode of the file is not a value of LOV-AUTONOMY | The load is refused with 422 and the field is named; no version row exists and no value is mapped to a nearby level | MSG-GEN-001 | AC4 |
| X3 | The same agent and version label are loaded a second time | The load is refused with 409 and no second row exists; the version in force is unchanged | None | AC9 |
| X4 | The local decision record cannot be written on the approval | The transaction rolls back: the version keeps status LOADED, no outbox row exists and no notification is sent | MSG-P7-003 | AC2, AC5 |
| X5 | The approver is the loader of the version | The approval is refused with 409 and the version keeps status LOADED | MSG-P7-002 | AC6 |
| X6 | A caller without the right of the operation calls the load or the approve | The call is refused with 403, nothing is written and nothing is returned | MSG-P4-002 | AC7 |
| X7 | The version is LOADED and its valid-from date has arrived | It is not in force: the run step keeps the previous APPROVED version, because a version takes effect only after approval | None | AC6 |
| X8 | The same request arrives again with the same Idempotency-Key | No second version row, no second record and no second outbox row; the first answer is returned and the repeat is counted | None | AC9 |
| X9 | The gateway-bff route cannot reach the agent read | The screen shows the route's own degraded answer and no business value is defaulted; no version row is written by the screen | None | AC7 |

The step writes no case field and raises no case task on any path, so none of these exceptions moves a case. X4 is the behaviour legacy AC2 and FSD A2.12 AC-EXC-P10-012-02 describe, and X6 is FSD A2.12 AC-EXC-P10-012-01.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P10-E3030-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, the agent runtime baseline and the three contract fakes; it waits for no other in-lane story and its metadata "Depends on (build)" holds no non-CON story of this service |
| Negotiable | The version label, the file format of the load and the granularity of "one decision" are agreed at the contract freeze and recorded as assumptions; the values themselves are always rows of the version |
| Valuable | The level an agent may act at is a dated, approved and recorded version of the owning service, and a failed record leaves nothing changed |
| Estimable | One controller, one validator, one repository, one record writer, one route and its contract test |
| Small | Fits one sprint with its tests |
| Testable | Each of the nine criteria of section 7 is one automated test against the decision-record, access and route fakes; no criterion needs a production file |

### 7. Acceptance criteria

```gherkin
Feature: Change an autonomy level

  Scenario: AC1 Change an autonomy level (legacy RWB-E3-030 AC1)
    Given the rwb-decision contract mock records the decision log entry with the rule version
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then changes the autonomy level for one agent and one decision, as a versioned configuration row
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E3-030 AC2)
    Given the rwb-decision contract mock refuses the decision log write
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The level is a version of the policy row in rwb_agent (new, D-RCV-60)
    Given agent "SCREENING" has policy version "P1" in force with autonomy_mode "SHADOW" on 2026-12-15
    Given the center of excellence analyst loads a checked file for "SCREENING" with policy version "P2", autonomy_mode "L1" and valid from 2026-12-16
    When the analyst calls POST /api/recovery/agent/v1/admin/agent-configs with kind POLICY and an Idempotency-Key
    Then one agent_policy row holds agent_code "SCREENING", policy_version "P2", autonomy_mode "L1", status "LOADED", loaded_by the caller and valid_from 2026-12-16
    Then the row is written in rwb_agent and in no other schema: no parameter_catalog or parameter_value row of rwb-case and no rule_row of rwb-decision is inserted or updated
    Then policy version "P1" keeps its fields and its autonomy_mode "SHADOW" and stays readable through GET /api/recovery/agent/v1/admin/agent-configs

  Scenario: AC4 A value outside LOV-AUTONOMY is refused (new, D-RCV-60)
    Given the autonomy levels of the service are those of LOV-AUTONOMY: OFF, SHADOW and L1
    When a file carries autonomy_mode "L2" or "PAUSED"
    Then the load is refused with 422 and the field autonomy_mode is named
    Then no version row exists for the agent and the version in force is unchanged
    Then no value is mapped to a nearby level, no level outside the list is stored and no list is extended by this story

  Scenario: AC5 The change is recorded in the transaction that writes the version (new, D-RCV-60)
    Given policy version "P2" of "SCREENING" in status "LOADED" and the decision-record library stub answering a committed record
    When the risk and model risk officer approves "P2"
    Then one decision record is written before "P2" can take effect, naming agent "SCREENING", kind POLICY, configuration version "P2", autonomy level "L1", the version in force before the change, the approver role and the valid-from date 2026-12-16
    Then the version row, the local record and the outbox row commit in one rwb_agent transaction
    Then rwb.decision.DecisionRecorded.v1 is written to the outbox on rwb.decision-record.v1 with the record reference
    Then no rule row is read and no package version is named, because no Drools package decides an autonomy change

  Scenario: AC6 Only an approved version takes effect, and it takes effect on its date (new, D-RCV-60)
    Given policy version "P2" of "SCREENING" with valid from 2026-12-16 and status "LOADED"
    When the run step asks for the version in force on 2026-12-16
    Then it gets policy version "P1", because a version in status "LOADED" is not in force
    When the risk and model risk officer approves "P2"
    Then a run on 2026-12-15 uses policy version "P1" and a run on 2026-12-16 uses policy version "P2"
    Then policy version "P1" is not overwritten and stays readable with its own dates and its own autonomy_mode

  Scenario: AC7 The change is reached through the gateway-bff route and refused without the right (new, D-RCV-60)
    Given the three configuration operations are published on /api/recovery/agent/v1
    When the center of excellence analyst loads a version and the risk and model risk officer approves it from the Workbench
    Then each call is served by the gateway-bff composite route in one hop with a 2 s budget, and the browser calls no owner service directly
    Then SCR-46 Agent monitor shows the state live for autonomy level "L1", shadow for "SHADOW" and paused for "OFF" once the version is in force
    Given user "U-5001" holds RW-REFADM, which holds neither Rules and parameters C nor A
    When "U-5001" calls the load or the approve
    Then the call is refused with 403 and MSG-P4-002, nothing is written and nothing is returned

  Scenario: AC8 The level is read from the row at run time and cached nowhere (new, D-RCV-60)
    Given policy version "P2" of "SCREENING" is in force from 2026-12-16 with autonomy_mode "L1"
    When the run step starts a run for 2026-12-16
    Then it reads autonomy_mode from the agent_policy row in force and writes the value it used into agent_run.autonomy_mode
    Then no cache table, no parameter row and no second copy of the level exists in rwb_agent or in another schema
    When "P2" is retired and "P3" with autonomy_mode "SHADOW" is in force from 2026-12-20
    Then the run on 2026-12-20 uses "SHADOW" without a release and without a restart of the service

  Scenario: AC9 A repeat of the load or the approve writes nothing new (new, D-RCV-60)
    Given policy version "P2" of "SCREENING" was loaded and approved with an Idempotency-Key
    When the same load request arrives again with the same key
    Then no second agent_policy row exists for "SCREENING" and "P2" and the first answer is returned
    When the same approve request arrives again with the same key
    Then no second decision record and no second outbox row exist and the repeat is counted
    Given the same agent and the same version label are loaded again with a different key
    Then the load is refused with 409 and no second row exists

  Scenario: AC10 The rules of section 8 are each proved by a criterion or a test (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8 are in force
    When the service is built and its tests are run
    Then each rule has a criterion in section 7 or a test case in section 16 that names it in the rule coverage line
    Then a rule that is an architecture constraint is proved by a guardrail or boundary test in section 16 instead

  Scenario: AC11 An unauthenticated call is answered 401 and an unknown policy version 404 (new, D-RCV-60)
    Given the configuration operations of /api/recovery/agent/v1 are published
    When a caller without a session calls one of them
    Then the answer is 401 and nothing is written or returned
    When a caller with the right calls the approve with a versionId that does not exist
    Then the answer is 404 and nothing is written
```

AC1 and AC2 are the legacy criteria of RWB-E3-030, copied verbatim, and AC3 to AC11 are new for this service change.

**Target reading.** AC1 and AC2 each gained one Given line and lost nothing. AC1 gained `Given the rwb-decision contract mock records the decision log entry with the rule version` as its first Given, because the write that the legacy criterion asserts is now a cross-service act — the local record through the RWB-PLT-E1027-CON library and the shared topic `rwb.decision-record.v1` that rwb-decision seals — and the criterion cannot be proved without the contract fake that stands in for that write (DP-03). AC2 gained `Given the rwb-decision contract mock refuses the decision log write` as its first Given for the same reason: the legacy line "the decision log cannot be written" now has one concrete, testable cause, the refusal of the record library, and the fake is the only way to force it. Every other legacy line and value is unchanged, including "the data and the rule version this feature needs are in place", "the user acts on the screen", both Then lines and MSG-P7-003.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The autonomy level of an agent is `autonomy_mode` of a versioned configuration row and not a value in code; a change of the level is a new version | BR-P10-012; FEAT-AGT-12; TSD P10 v2 DF-AGT-008 |
| BR2 | A version is never edited in place: a change writes a new version with a new label, and the version in force stays readable with its own fields and dates | FSD P10 v3 A2.1 AC-ALT-P10-001-01; TSD P10 v2 DF-AGT-022 and DF-AGT-023 |
| BR3 | A version takes effect only after approval and only from its valid-from date; a version in status LOADED is not in force | FSD P10 v3 A2.1 AC-ALT-P10-001-01; TSD P10 v2 DF-AGT-021 |
| BR4 | The version row, the local decision record and the outbox row are one `rwb_agent` transaction; a failed record write leaves the version LOADED and writes nothing else | Principle 5; R-UNI-39; DP-03; legacy RWB-E3-030 AC2 |
| BR5 | The version on the decision record is the configuration version label, and the record names the agent and the kind in its rule-identity element, the kind being POLICY or PROMPT; the approval instant is Not specified in the source documents (GAP-0637); the record member names are left to RWB-PLT-E1027-CON; no Drools package is evaluated and no rule row is read on a configuration change | Legacy RWB-E3-030 AC1; ASM-0998; DP-04 not applied |
| BR6 | The load needs Rules and parameters C, the approve A and the read R; a caller without the right is refused with MSG-P4-002 and nothing changes | TSD P10 v2 API-P10-002 to API-P10-004 and T6.1; FSD P10 v3 A2.12.3.3; ASM-0994 |
| BR7 | The loader may not approve their own version; the approval is refused with 409 and MSG-P7-002 | FSD P10 v3 A2.1 AC-EXC-P10-001-03 |
| BR8 | Only the values of LOV-AUTONOMY are accepted, and a value outside the list is refused rather than mapped or created | TSD P10 v2 T3.2; ASM-0992 |
| BR9 | The run step reads the level from the row in force at run time and records the value it used on the run; no cache and no second copy of the level is held | DP-01; FSD P10 v3 A2.12; TSD P10 v2 DF-AGT-043 |
| BR10 | The configuration row is `rwb_agent`'s and no foreign key crosses a schema: `parameter_catalog` and `parameter_value` stay with rwb-case and `rule_row` stays with rwb-decision | DP-01; Template and Rules §R3 default ruling; Ownership Map v1 |
| BR11 | One load and one approval per Idempotency-Key: a repeat returns the first answer and writes no second row, no second record and no second outbox row | TSD P10 v2 T-A.2; R-UNI-40 |
| BR12 | No personal data is written by the change: the version holds agent codes, list values, numbers, dates and a user reference for the loader and the approver, classed as Not specified in the source documents (DOR-RWB-P10-E3030-APP-11), and the record carries no personal data | TSD P10 v2 T3.1 and T6.2; Template and Rules §R7.2 s17 |

**Rule coverage (DOR-RWB-P10-E3030-APP-4).** BR1 by AC3 (TC-E3-030-05); BR2 and BR3 by AC6 (TC-E3-030-08); BR4 by AC2 (TC-E3-030-02) and TC-E3-030-04; BR5 by AC1 (TC-E3-030-01); BR6 by TC-E3-030-03 and TC-E3-030-09; BR7 by TC-E3-030-13; BR8 by AC4 (TC-E3-030-06); BR9 by AC8 (TC-E3-030-10); BR10 by AC3 (TC-E3-030-05) and TC-E3-030-12; BR11 by AC9 (TC-E3-030-11); BR12 by AC5 (TC-E3-030-07).

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | LOAD | the checked file passes the field catalog and the lists | LOADED |
| None | LOAD_REFUSED | a required value is empty, a value is outside its list, or the label already exists for the agent | None, and nothing is written |
| LOADED | APPROVE | the approver is not the loader and the record is written in the same transaction | APPROVED |
| LOADED | SELF_APPROVAL_REFUSED | the approver is the loader | LOADED, unchanged |
| LOADED | RECORD_WRITE_FAILED | the local decision record cannot be written | LOADED, because the transaction rolls back |
| APPROVED | IN_FORCE | the business date is at or after `valid_from` and before `valid_to` | APPROVED, in force for the date |
| APPROVED | RETIRE | `valid_to` is passed or a later version is approved for the same agent | RETIRED, and the row stays readable |

These are the states of a configuration version and not a case state machine. The status column carries the three values of LOV-CONFIG-STATUS (TSD P10 v2 DF-AGT-021); "in force for a date" is read from the status together with the two date columns and is not a fourth value. **This story moves no case status**: `recovery_case` is neither read nor written, no task and no assignment row is written, and no run is started, retried or ended.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Risk and model risk officer (RW-RISK) | Primary actor of the change: approves a loaded version under Rules and parameters A, reads the version and its record, and reads the state on SCR-46 |
| Center of excellence analyst (RW-COE) | Loads a version under Rules and parameters C, reads the version list, and may not approve what they loaded |
| Platform administrator (RW-PLATADM) | Holds CRUD on Platform administration in TSD P10 v2 T6.1 and R in the legacy permission list; reads the versions and the run evidence, and may re-drive a refused approval |
| Internal audit (RW-AUDIT), Compliance and PDPA officer (RW-COMPLY), Security administrator (RW-SECADM) | Read the version list and its records, as the legacy permission list allows under Platform administration R |
| Data steward and data product owner (RW-DATASTEW) | Reads the versions and the lists the change uses |
| rwb-agent service identity (the rwb-agent login, DP-02) | Writes the version row, the local record and the outbox row, and serves the three operations |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| SY-RULES rules identity | Not used by this story: no Drools package is evaluated on a configuration change |
| RW-REFADM | Holds neither Rules and parameters C nor A; refused on the load and on the approve with MSG-P4-002 |

The legacy permission list of RWB-E3-030 gives Platform administration R to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM, while the configuration operations of TSD P10 v2 T-A.1 are governed by Rules and parameters with rights R, C and A and FSD P10 v3 A2.12.3.3 names the risk and model risk officer as the primary user. The right under which a change is made is therefore Not specified in the source documents (GAP-0636; ASM-0994), and this story reads the legacy row as the read on the monitor while the change is made under Rules and parameters, reconciled by rwb-access. The per-service login name is Not specified in the source documents (GAP-0636; ASM-1003); the story names it "the rwb-agent login (DP-02)" until it is agreed.

The three operations of the contract are GET /admin/agent-configs, POST /admin/agent-configs and POST /admin/agent-configs/{versionId}/approve (API-P10-002 to API-P10-004 of TSD P10 v2 T-A.1), on the base /api/recovery/agent/v1 named in the change log; the GET/POST /agent-policies label of Arch v5 slide 16 is a summary and not the contract.

Each of these operations and the monitor read is guarded by an rwb-access authorise check (DP-08); the check's name is Not specified in the source documents (DOR-RWB-P10-E3030-APP-6), and a refused load or approve returns MSG-P4-002.

The screen states of SCR-46 Agent monitor are: empty, Not specified in the source documents (DOR-RWB-P10-E3030-APP-10); loading, Not specified in the source documents (DOR-RWB-P10-E3030-APP-10); error, Not specified in the source documents (DOR-RWB-P10-E3030-APP-10); and no access, Not specified in the source documents (DOR-RWB-P10-E3030-APP-10).

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-001 to DF-AGT-025 | agent_policy | id, agent_code, policy_version, model_code, model_version, output_schema_ref, allowed_tools, autonomy_mode, segment_product_group, segment_region_code, confidence_floor, timeout_seconds, daily_cost_cap_thb, price_per_1k_tokens_thb, alert_role, review_date, evaluation_run_id, promotion_conditions, watch_measures, fallback_rule, status, valid_from, valid_to, loaded_by, approved_by | Write on a POLICY load and approve; read on the list |
| DF-AGT-026 to DF-AGT-035 | agent_prompt | id, agent_code, prompt_version, body_text, body_hash, status, valid_from, valid_to, loaded_by, approved_by | Write on a PROMPT load and approve; read on the list |
| DF-AGT-043 | agent_run | autonomy_mode | Read only here: written by the run step with the value in force at run time, not by this story |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | all fields, written through P7's library and sealed by rwb-decision | Write locally |
| TSD P10 v2 T3.0 | standard record columns of `agent_policy` and `agent_prompt` | state, version, created_at, created_by, updated_at, updated_by | Write; `updated_at` is the approval instant (ASM-0996) |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and TSD P10 v2 T3.1. No foreign key crosses a schema (DP-01). Three tables that the legacy step touched are no longer read or written by this slice: `parameter_catalog` and `parameter_value` stay with rwb-case under the §R3 default ruling, because the autonomy level is no longer a shared parameter row, and `rule_row` stays with rwb-decision, because no Drools package decides a configuration change. The `body_text` and `body_hash` of a prompt version are stored as the file supplies them and the hash is computed on the text; the file format of the load and its column order are Not specified in the source documents (GAP-0636; ASM-0995). The version label has no format rule (GAP-0636; ASM-0996). No personal data is written: the loader and the approver appear as user references and the record carries no personal data.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Right |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-configs` | List policy and prompt versions per agent with status and dates; query agent, kind, status (API-P10-002) | Rules and parameters R |
| POST | `/api/recovery/agent/v1/admin/agent-configs` | Load a new policy or prompt version from a checked file; multipart file, kind, agent, validFrom; `Idempotency-Key` (API-P10-003) | Rules and parameters C |
| POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | Approve a loaded version; no request body; `Idempotency-Key` (API-P10-004) | Rules and parameters A |

The three operations are the service's own and are declared once; their shape, their error codes, the Idempotency-Key rule and the checks of the file are the contract of RWB-P10-E3030-CON, which this story implements. Contract version this story builds against: version 5.0.0 of the rwb-agent API document (`05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml`), which publishes the three operations under `/api/recovery/agent/v1`. The legacy monitor read on the shared base under DP-13 becomes `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001, Platform administration R); it belongs to the monitor stories and is not changed here.

#### 12.2 REST operations consumed

None. The decision record is written through a library and not over REST, and the rights of the three operations are resolved by the access guard that the service template and the gateway-bff route install, so this story calls no rwb-access operation of its own and claims no contract dependency (ASM-0999). No reference-data operation is called by this story either: the list rows are wired by the platform set-up story (ASM-0997).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, agent code, kind POLICY or PROMPT, configuration version, autonomy level, the version in force before the change, approver role, valid-from date |

The row is written to the outbox in the same transaction as the version row and relayed with the CloudEvents envelope (DP-03). No agent event is published for the change: the P10 OUT line of Arch v5 slide 16 names AgentRunCompleted only, and the agent event `rwb.agent.AgentRunCompleted.v1` (EV-28) on the service topic `rwb.agent.events.v1` is published by the run path of RWB-P10-E1058-APP and not here, while the version is read from the table through the config read. No personal data is carried.

#### 12.4 Events consumed

None. The change is a request path and reads no topic; this story has no inbox handler of its own.

#### 12.5 Workflows and activities

None. The load and the approval are synchronous admin operations of the request path, and the record is written in the request transaction; no Temporal workflow, no activity and no task queue is added by this story. The run that reads the level belongs to AgentRunWorkflow on the queue `rwb-agent` and to the run story.

#### 12.6 Schedules

None. No Schedule creates, changes, promotes or retires a configuration version; the effective date is `valid_from` of the row and needs no job (ASM-1000).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_policy | P10 (rwb_agent) | The policy version: DF-AGT-001 to DF-AGT-025, including `autonomy_mode`; created by the agent runtime baseline migration, not by this story |
| agent_prompt | P10 (rwb_agent) | The prompt version: DF-AGT-026 to DF-AGT-035; created by the same baseline |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope of the record write and of the two admin operations (DP-09 library elements, not a pattern of this story) |

`decision_log_entry` is a rwb-decision table and is written only through the P7 decision-record library (DP-01, DP-03). `parameter_catalog` and `parameter_value` are rwb-case tables and `rule_row` is a rwb-decision table; this story reads and writes none of them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision decision-record library stub | The P7 record contract and `rwb.decision-record.v1` (DP-03) | A committed record with its reference; a forced write failure on the approve; the outbox row and its relay |
| rwb-access guard stub | The rights of the three operations (P4) | Rules and parameters C and A granted to RW-COE and RW-RISK; a role without the right refused with 403 and MSG-P4-002 |
| gateway-bff composite route stub | The DP-19 route of SCR-46 | The merged screen answer with the version in force and its state; the degraded answer of X9 |

The list values of TSD P10 v2 T3.2 are not faked here: they arrive through the baseline wiring of the platform set-up story and this story adds no list dependency (ASM-0997).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed | The config read, the load and the approve on `/api/recovery/agent/v1`; the rights are resolved by the access guard; no operation of another service is called |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox; nothing consumed |
| Temporal | 0 workflows, 0 activities | The change is synchronous and the run that reads the level is the run story's |
| File | 1 per load | The checked file of a policy or prompt version is the input of the load and is stored as rows; no run-time file exchange |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `config`, Java package `th.co.scb.ace.workbench.recovery.agent.config`. No front-end module: the change is called from the Workbench through the gateway-bff route, and the screen is the monitor story's.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/agent/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The two platform contract stories are build dependencies of the metadata rows, and the third build dependency is RWB-P10-E3030-CON, the contract story of this key. DP-13 adds no dependency because it is a naming rule.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentConfigController | REST controller | The three operations, the multipart load, the Idempotency-Key header, validation errors as problem responses |
| AgentConfigValidator | Service | Checks the file against the field catalog and the lists, and returns the field and the check that failed |
| AgentConfigService | Service | Loads, approves and retires a version; applies the four-eyes rule; resolves the version in force for a business date |
| AgentConfigRepository | Repository | Reads and writes `agent_policy` and `agent_prompt` only, in `rwb_agent` |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the configuration version, the level and the approver role, hash-linked, in the same transaction (DP-03) |
| ConfigView | Read model | The version list and the one version in force, for the read operation and the route |
| Screen adapter | None | SCR-46 is served by the gateway-bff composite route and belongs to the monitor stories |

**Database and migrations**

- No new table and no new column. `agent_policy` and `agent_prompt` come from the agent runtime baseline migration of `rwb_agent` that RWB-P10-E1058-APP owns, and this story adds only what TSD P10 v2 T3.1 already lists (ASM-1001).
- If the baseline does not carry the table when the story is picked up, the script that adds it takes its number from the rwb-agent Flyway sequence; that number is Not specified in the source documents (GAP-0636; ASM-1001) and no number is claimed here.
- One index for the read of the version in force: `agent_policy (agent_code, status, valid_from)` and the same on `agent_prompt`, so the in-force lookup and the duplicate-label check are key lookups and not scans. The index name is a naming-library value and not a business value.

**Configuration and reference data**

- The values the load accepts are the list values of TSD P10 v2 T3.2 and none is written in code: LOV-AGENT, LOV-AUTONOMY (OFF, SHADOW, L1), LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED), LOV-PRODUCT and LOV-REGION.
- The kind of a version is POLICY or PROMPT and is carried by the resource, `agent_policy` or `agent_prompt`; the list name of the kind is not in TSD P10 v2 T3.2, and only the two resource names are used (GAP-0636; ASM-0995).
- The version label is free text and its format is not fixed by any source (GAP-0636; ASM-0996).
- The file format of the load is Not specified in the source documents (GAP-0636; ASM-0995); the contract of RWB-P10-E3030-CON fixes the column set from the field catalog of FSD P10 v3 A2.12.3.2 and TSD P10 v2 T3.1, and the two are one document.

**Build steps**

1. AgentConfigRepository and the in-force resolver over `agent_policy` and `agent_prompt`, with the duplicate-label check; tests for AC3 and AC6.
2. AgentConfigValidator against the field catalog and LOV-AUTONOMY, with the field and the check named in the refusal; tests for AC3, AC4 and X1.
3. The load operation with the multipart file and the Idempotency-Key; tests for AC3, AC9 and X3.
4. The approve operation with the four-eyes rule and the version transition; tests for AC6 and X5.
5. DecisionRecordWriter and the one-transaction write of the version, the record and the outbox row, with the rollback path; tests for AC2 and AC5.
6. The read operation and the route contract with the refusal path and the degraded answer; tests for AC7 and X9.
7. The run-time read of `autonomy_mode` and its hand-over to the run step, including the value on `agent_run`; test for AC8.
8. The list wiring check against the baseline of RWB-P10-E1058-APP and the full scenario run over synthetic rows for a business date; tests for AC6 and AC8.

**Done when.** The tests in section 16 pass, no version row exists without its decision record, every record names the configuration version and the approver role, a version in status LOADED never takes effect, the decision-record and route contract tests stay green, and the SIT week showed no change of a level without an approved version behind it.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the file is empty, or a value is outside its list | Enter {field}. |
| MSG-P4-002 | A caller without the right of the operation calls the load or the approve | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written on the approval | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-002 | An approver who is also the loader of the version calls the approve (FSD P10 v3 A2.1 AC-EXC-P10-001-03) | Not specified in the source documents (DOR-RWB-P10-E3030-APP-9) |
| MSG-P10-001 | A configuration file fails a check (FSD P10 v3 A2.1 AC-EXC-P10-001-02) | Not specified in the source documents (DOR-RWB-P10-E3030-APP-9) |

The three messages are the legacy messages of RWB-E3-030 and keep their wording. Two further messages are named by the specifications and are listed in the table above with their IDs: MSG-P7-002 for an approver who is also the loader (FSD P10 v3 A2.1 AC-EXC-P10-001-03) and MSG-P10-001 for a configuration file that fails a check (FSD P10 v3 A2.1 AC-EXC-P10-001-02). Their wording is not in the legacy message set, so it is Not specified in the source documents (DOR-RWB-P10-E3030-APP-9); this story tests the code and the ID and invents no text for them. No other message is added.

### 15. Screens and states

SCR-46 Agent monitor, states Shadow; live; paused, is the legacy screen of RWB-E3-030 and shows the version in force and its autonomy level. The empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2851), because Screen Specifications v1 lacks them too; they stay with the monitor stories. The screen and its read belong to the agent monitoring stories (RWB-P10-E1063-APP and RWB-P10-E2031-APP), and this story changes no panel, no field order and no masking; what it adds is the data: the agent, the kind, the version label, the autonomy level, the status, the valid-from date, the approver role and the approval instant, read from `agent_policy` or `agent_prompt` and the record through the config read and the gateway-bff composite route (DP-19). The mapping from the level to the screen state — shadow for SHADOW, live for L1 and paused for OFF — is a reading of the three states the legacy story names against the three values of LOV-AUTONOMY, and it is Not specified in the source documents (GAP-0636; ASM-1002); it is shown for the user's orientation and changes no value. The screen fields, their order and their masking are Not specified in the source documents (GAP-0636; ASM-1002) and stay with the monitor stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-030-01 | AC1 | Component | Agent "SCREENING" with policy version "P1" in force; the checked file of "P2" with autonomy_mode "L1"; the decision-record library stub answering a committed record |
| TC-E3-030-02 | AC2 | Component | The same approval with the decision-record library stub refusing the write; snapshot of the `agent_policy` and outbox rows before and after |
| TC-E3-030-03 | Access | Contract | User "U-5001" holding RW-REFADM, which has neither Rules and parameters C nor A, calls the load and the approve; refused with 403 and MSG-P4-002 |
| TC-E3-030-04 | Principle 5 | Component | Decision record write forced to fail on the approval; no status change, no outbox row and no second attempt inside the transaction |
| TC-E3-030-05 | AC3 | Component | "P1" in force with "SHADOW"; a POLICY load of "P2" with "L1" and valid from 2026-12-16; assertions on `agent_policy`, `parameter_catalog`, `parameter_value` and `rule_row` |
| TC-E3-030-06 | AC4 | Component | A file with autonomy_mode "L2" and a file with "PAUSED"; the version in force before and after |
| TC-E3-030-07 | AC5 | Component | "P2" in LOADED; the approval with the record library stub; the record fields, the single transaction and the outbox row |
| TC-E3-030-08 | AC6 | Component | "P2" LOADED with valid from 2026-12-16 and "P1" APPROVED; the in-force answer on 2026-12-15 and 2026-12-16 before and after the approval |
| TC-E3-030-09 | AC7 | Contract | gateway-bff route stub with the version in force and its state; the refusal of RW-REFADM; the degraded answer of the route |
| TC-E3-030-10 | AC8 | Component | "P2" in force with "L1", then "P3" with "SHADOW" from 2026-12-20; the `agent_run.autonomy_mode` value on each run; no cache table |
| TC-E3-030-11 | AC9 | Component | The same load and approve requests with the same Idempotency-Key; a second load of the same label with a different key |
| TC-E3-030-12 | §12.7 table boundary (ASM-3438) | Component | Load and approve requests through the library; snapshot of the `agent_policy` and outbox rows, and of `parameter_catalog`, `parameter_value` and `rule_row`, before and after; nothing written outside the tables owned by rwb_agent |
| TC-E3-030-13 | BR7 | Component | P2 in LOADED; the approve call by the same user who loaded it; refused with 409 and MSG-P7-002; the version stays LOADED |
| TC-E3-030-14 | AC10 | Component | Rule coverage line of section 8 checked against sections 7 and 16; a rule with no criterion or test named in it fails; proposed test Not specified in the source documents (NEWAC-RWB-P10-E3030-APP-AC10) |
| TC-E3-030-15 | AC11 | Contract | Call without a session to a provided operation of /api/recovery/agent/v1, answered 401; approve call with a versionId that does not exist, answered 404; proposed test Not specified in the source documents (NEWAC-RWB-P10-E3030-APP-AC11) |

The legacy levels map System to Component, Access to Contract and Principle 5 to Component, because the cross-service behaviour of this key is proved by the integration story of the wave and the access right is proved against the published contract and its fake. No `-ITG` copy is held here: the integration copies of this key belong to the integration story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the autonomy levels are the values of LOV-AUTONOMY, the statuses those of LOV-CONFIG-STATUS, and every other value of a version is a row of the loaded file (BR-P10-012).
- No personal data in logs, tests, workflow history or prompts: the version holds agent codes, list values, numbers, dates and user references for the loader and the approver, and the record carries no personal data.
- No read or write of another service's tables: the version lives in `rwb_agent`, the record is written through the P7 library, and `parameter_catalog`, `parameter_value` and `rule_row` are never touched (DP-01).
- The record is written in the same transaction as the version, before the version can take effect; a failed write rolls the whole transaction back (R-UNI-39).
- A version in status LOADED never takes effect, and no date, level or status is defaulted to make one take effect.
- The change starts no agent run, retries no run and changes no run status; the value a run used is written by the run step and not by this story.
- The change moves no case status and raises no task or assignment row; the case side of an autonomy decision belongs to rwb-case.
- Only the version row, the record and the outbox row are new data; no copy of a list, of a parameter or of the level is written outside `rwb_agent`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | The autonomy level of one agent and one decision is changed as a versioned configuration row | No BRD section carries the feature (GAP-0636) | FEAT-AGT-12 | All recovery processes (legacy RWB-E3-030) | BR-P10-012 | TC-E3-030-01, TC-E3-030-05, TC-E3-030-08 |
| None (the legacy story carries no requirement ID) | The result is written to the decision log with the rule version, and nothing changes when it cannot be recorded | No BRD section carries the feature (GAP-0636) | FEAT-AGT-12 | All recovery processes (legacy RWB-E3-030) | R-UNI-39 | TC-E3-030-02, TC-E3-030-04, TC-E3-030-07 |
| D-RCV-60 DP-01 | The configuration row is the owning service's and no foreign key crosses a schema | Decision log D-RCV-60; Template and Rules §R5.5 | FEAT-AGT-12 | All recovery processes | BR-P10-012 | TC-E3-030-05 |
| D-RCV-60 DP-03 | The decision record is written locally in the same transaction as the change, and the shared topic carries it to the central ledger | Decision log D-RCV-60; Template and Rules §R5.5 | FEAT-AGT-12 | All recovery processes | R-UNI-39 | TC-E3-030-02, TC-E3-030-04, TC-E3-030-07 |
| D-RCV-60 DP-13 and DP-19 | The three operations sit on the per-service base and the screen composes the result through the gateway-bff route and calls no owner service directly | Template and Rules §R5.5; Architecture v5 slides 13 and 41 | FEAT-AGT-12 | All recovery processes | None | TC-E3-030-09, TC-E3-030-03 |
| Legacy FEAT-CWC-22 | The parameter catalog and configuration service holds the versioned parameters of the Workbench; it no longer holds the agent autonomy level | FSD P3 Case and workflow v4 A2.22; Template and Rules §R3 default ruling | FEAT-AGT-12 and FEAT-CWC-22 | All recovery processes | None | TC-E3-030-05 |

The legacy story RWB-E3-030 carries no requirement ID: it names its feature (FEAT-AGT-12) and no BRD in the extracts carries that feature, so no BRD section and no requirement is cited for it and the absence is recorded as GAP-0636. The feature source is the Epics 3 to 8 Specification v3 row E3 · P10 · FEAT-AGT-12 and FSD P10 v3 A2.12; the prerequisite FEAT-CWC-22 of the legacy story is read as the parameter catalog of P3, which no longer carries this row; the rule is BR-P10-012; the decision is D-RCV-60.

### 19. Out of scope

- The step-up and step-down of an autonomy level on measured evidence with the approval of the committee path (FEAT-AGT-15; RWB-P10-E8004-APP and RWB-P10-E8004-CON).
- The autonomy level per decision step, its per-step key and its committee approval (FEAT-ADM-01; RWB-P10-AD020-APP and RWB-P10-AD020-CON).
- The agent run itself, the guardrail checker, the fallback of R-UNI-32 and the write of `agent_run.autonomy_mode`, which is the run step's (RWB-P10-E1058-APP and the run story).
- The evaluation harness that measures an agent before a level changes (FEAT-AGT-05; RWB-P10-E1060-APP).
- The drift check, the alert and its decision (FEAT-AGT-13; RWB-P10-E3031-APP).
- The agent monitoring screens SCR-46 and their states, fields and masking (RWB-P10-E1063-APP and RWB-P10-E2031-APP), and the gateway-bff route contract itself (RWB-PLT-N001-CON).
- The contract artefacts of this key — the version shape, the three operations, the record payload, the ordering rule, the messages and the fakes (RWB-P10-E3030-CON).
- The central ledger, its sealing and the ledger read (P7 rwb-decision), and the record library and shared topic (RWB-PLT-E1027-CON).
- The roles, the rights, the scope and the masking rules (P4 rwb-access), and the reconciliation of the right of the change.
- The parameter catalog, the reference data and the lists (P3 rwb-case), and the wiring of the reference-data contract (RWB-P10-E1058-APP).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
