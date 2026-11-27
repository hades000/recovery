# RWB-P10-E8004-APP Raise or lower an autonomy level with approval

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E8004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P10-K |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P10-E8004-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-004 for rwb-agent. The step up and the drop stay with the service that owns the agent policy rows: the raised or lowered level is a new `agent_policy` version in `rwb_agent` (DP-01), the approval is a P7 approval read through rwb-decision's contract and its reference is held on the version, the change is written to the local decision record and to `rwb.decision-record.v1` in the same transaction (DP-03), and the two admin operations move to the rwb-agent base and reach the browser through the gateway-bff composite route (DP-13, DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P10-E8004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **to step an agent up to a higher autonomy level on measured evidence and to drop it on a breach, each change taking effect only as a new approved version of its policy row that carries the approval it was granted under, recorded on the decision record in the same transaction**, so that **no agent ever runs at a level the committee did not approve, every level change can be read back with the version that carried it and the approval behind it, and a refused or half-written approval leaves the agent exactly where it was**.

### 2. Business rationale

The legacy story RWB-E8-004 gave the risk and model risk officer one action: step an agent up on measured evidence, and drop it on a breach, with the approval each needs, and write the result to the decision log with the rule version (FEAT-AGT-15; FSD P10 v3 A2.15). It builds on FEAT-AGT-12, the change of an autonomy level as a versioned configuration row (FSD P10 v3 A2.12), and it sits under the BOT AI Risk Management Guidelines of 12 Sep 2025, which ask for autonomy levels and a human decision on material actions (Arch v5 slide 36). Arch v5 keeps the AI inside rwb-agent, where it can be switched off (slide 35).

In the target the change has two homes and they are different services. rwb-agent owns the policy versions, the prompts, the runs, the guardrails and the evaluations (Arch v5 slide 41), so the level lives in `agent_policy.autonomy_mode` of a version that is loaded and then approved, exactly as a prompt version is (FSD P10 v3 A2.1 AC-ALT-P10-001-01). The approval itself belongs to rwb-decision, which owns the approvals, their routing by delegation of authority and the central decision ledger (Arch v5 slide 41; Ownership Map). The two are joined by one field on the version — the approval it was granted under, which the administration source requires the version to show (legacy RWB-AD-020 AC2). That is why this story is small and load-bearing: it holds the join.

Three things in the legacy story no longer hold. Its data table names `decision_log_entry`, which is rwb-decision's table and is now written through the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03; ADR-022). Its data table names `rule_row`, and no Drools package decides an autonomy change: the "rule version" the legacy criterion speaks of is the policy version of `agent_policy`, so no rule row is read and no package version is named. Its endpoint table names one read on the monolith base, and the change itself was reached on a path of the monolith; in the target the reads and the two writes are on the rwb-agent base `/api/recovery/agent/v1` (DP-13) and reach the browser through the gateway-bff composite route, never as a direct call to an owner service (DP-19).

The realignment also has to say which approval is meant. rwb-decision routes an approval by delegation of authority and records an `approval_level` of LOV-APPROVAL-LEVEL, L1 to L6 (TSD P7 v2 T3.2), while an autonomy level is a value of LOV-AUTONOMY, OFF, SHADOW and L1 (TSD P10 v2 T3.2). The two lists share three strings and mean different things. This story never reads one as the other: the approved autonomy level is a fact of the approval's subject and the DoA level stays the DoA level (ASM-1025).

This story owns both legacy criteria of RWB-E8-004, AC1 and AC2, and copies them verbatim in section 7 with one inserted Given each, explained there. AC3 to AC10 are new and test the microservice deliverable of the title only. The legacy story carries no requirement ID; section 18 records that and traces the feature instead.

### 3. Preconditions

- RWB-P10-E8004-CON is published: the load-then-approve two-step, the rights, the error codes, the Idempotency-Key rules, the approval reference on the version, the consumed approval read, the decision-record payload and the two fakes. This story implements what that contract fixes and starts on Day 1 against its fakes.
- RWB-PLT-E1027-CON is published: the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1` with its CloudEvents envelope. This story writes its record through the library and never writes the shared topic directly (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route contract for SCR-46 and its stub (DP-19).
- The `rwb_agent` schema exists with the agent runtime baseline migration — `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback` and `agent_alert` (TSD P10 v2 T3.1). This story adds one column to `agent_policy`, the approval reference, and no table (ASM-1026).
- A policy version is in force for the agent and the business date: `agent_code`, `policy_version`, `model_code`, `model_version`, `output_schema_ref`, `autonomy_mode`, the segment product group, `confidence_floor`, `timeout_seconds`, `daily_cost_cap_thb`, `status`, `valid_from`, `valid_to`, `loaded_by` and `approved_by` (DF-AGT-001 to DF-AGT-025).
- The level values used by the change are those of LOV-AUTONOMY: OFF, SHADOW and L1 (TSD P10 v2 T3.2). The lists are reference data owned by rwb-case under the §R3 default ruling and the service holds no copy of a list in code. A level above L1 is named by the administration source (legacy RWB-AD-020 AC2 speaks of a committee approval for L2) but is not a value of LOV-AUTONOMY in any technical source, so this story stores no such level (GAP-0640; ASM-1022).
- The measured evidence behind a step up is the approved evaluation run the loaded version points at in `agent_policy.evaluation_run_id` (DF-AGT-017), and the breach behind a drop is an `agent_alert` row with `alert_type` DRIFT (DF-AGT-105). This story reads the reference and the alert and chooses no threshold of its own (GAP-0640; ASM-1023, ASM-1024).
- The login is the rwb-agent login (DP-02): its name is Not specified in the source documents (GAP-0640; ASM-1029).

### 4. Flow

1. The officer reads SCR-46 Agent monitor in state live and sees the agent, its policy version in force, its `autonomy_mode` and the approval behind it. The screen is served by the gateway-bff composite route, which calls the agent reads on `/api/recovery/agent/v1` and merges the answers; the browser calls no owner service directly (DP-19).
2. The officer decides a step up on the evidence of the approved evaluation run of the agent version, or a drop on a drift breach. The evidence reference is taken from `agent_policy.evaluation_run_id` of the version being replaced, or from the `agent_alert` row with `alert_type` DRIFT; the officer does not type a level that the list does not carry (ASM-1023, ASM-1024).
3. The load call is `POST /api/recovery/agent/v1/admin/agent-configs` with the checked file, the kind, the agent and the valid-from date, under the Rules and parameters right C and an Idempotency-Key (API-P10-003; TSD P10 v2 T-A.1 and T-A.2). The service writes one `agent_policy` row for the agent with a new `policy_version`, the new `autonomy_mode`, `status` LOADED, `valid_from` as given, `loaded_by` the caller and no approval reference. The version in force is untouched by this call.
4. The officer presents the committee approval. The approve call is `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` under the Rules and parameters right A and an Idempotency-Key (API-P10-004).
5. The service reads the approval through rwb-decision's contract, `GET /api/recovery/decision/v1/approvals/{approvalId}`, one hop with a 2 s budget (DP-11; API-P7-008 of rwb-decision). It takes the approval id, the approval status of LOV-APPROVAL-STATUS and the approved autonomy level of the approval's subject (ASM-1025).
6. A version is approved only when the approval is APPROVED and its approved level equals the `autonomy_mode` of the loaded version. The DoA `approval_level` of LOV-APPROVAL-LEVEL is never read as an autonomy level, and a mismatch is refused with 409 and the version stays LOADED (ASM-1025).
7. RecordAndApply runs in one `rwb_agent` transaction: it sets the version to APPROVED, writes the approval reference on the row, writes the local decision record with the old and the new level, the approval reference, the approver identity and the valid-from date, and inserts the DecisionRecorded row in the outbox. A failed record write rolls the whole transaction back, so the version stays LOADED and nothing partial is visible (DP-03; R-UNI-39).
8. The superseded version closes: its `valid_to` is set to the day before the new `valid_from` and its `status` moves from APPROVED to RETIRED. No other field of it is rewritten, so the level that was in force on any past date stays readable (ASM-1027).
9. The DecisionRecorded row is relayed from the outbox to `rwb.decision-record.v1` and rwb-decision seals it into the central ledger. The change waits for no confirmation: an autonomy change is not a point of no return.
10. The next agent run reads the version in force on its business date: a run on the day before the new `valid_from` still uses the old level and a run on or after it uses the new one (`agent_run.autonomy_mode`, DF-AGT-043).
11. A repeat of either call under the same Idempotency-Key returns the first answer and writes nothing: no second row, no second record and no second outbox row (R-UNI-40).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The approval read answers 404 for the approval id | The approve call is refused with 404, the version stays LOADED and no record is written | None | AC5 |
| X2 | The approval is REFUSED or RETURNED in rwb-decision | The version stays LOADED with no approval reference, the version in force is unchanged and the next run still uses it | None | AC8 |
| X3 | The approval is APPROVED for a level other than the `autonomy_mode` of the loaded version | The approve call is refused with 409, the version stays LOADED and nothing is written | None | AC5 |
| X4 | The version is already APPROVED, or is RETIRED | The approve call is refused with 409 and the existing row, its approval reference and its record are unchanged | None | AC2 |
| X5 | The caller loaded the version and also approves it | The approve call is refused with 409 and the version stays LOADED (FSD P10 v3 A2.1 AC-EXC-P10-001-03, same four-eyes rule) | MSG-P7-002 | AC2 |
| X6 | The local decision record cannot be written | The transaction rolls back: the version stays LOADED, the version in force is unchanged, no outbox row exists, and the call answers 503 | MSG-P7-003 | AC2, AC7 |
| X7 | The loaded level is not a value of LOV-AUTONOMY | The load is refused with 422 and no `agent_policy` row is written | MSG-GEN-001 | AC10 |
| X8 | A role without the Rules and parameters right C or A calls either operation | Refused with 403 before any row is written; the version in force is unchanged | MSG-P4-002 | AC9 |
| X9 | Either call is repeated under the same Idempotency-Key | The first answer is returned and nothing is written a second time | None | AC6 |

The change writes no case field and raises no case task on any path, so none of these exceptions moves a case. X6 is the behaviour FSD A2.15 AC-EXC-P10-015-02 describes, X8 the behaviour of AC-EXC-P10-015-01, and both are the legacy criteria AC1 and AC2 in the words of RWB-E8-004.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P10-E8004-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, the agent runtime baseline and the rwb-decision fake; it waits for no in-lane story |
| Negotiable | The approval reference field, the evidence and breach references, the route and the superseded-version rule are agreed defaults, recorded as assumptions |
| Valuable | No agent runs at a level nobody approved, and every level on record carries the version and the approval behind it |
| Estimable | One controller pair, one service, one approval client, one repository, one decision-record writer, one column |
| Small | Fits one sprint with its tests |
| Testable | Each of the ten criteria of section 7 is one automated test against the rwb-decision, rwb-access and gateway-bff fakes; no criterion needs a production approval |

### 7. Acceptance criteria

```gherkin
Feature: Raise or lower an autonomy level with approval

  Background:
    Given agent "SCREENING" is in force on 2026-12-15 with policy version "P1" and autonomy_mode "SHADOW"
    Given policy version "P1" is APPROVED with valid_from 2026-11-01 and holds model_code "MODEL-A", model_version "MODEL-A-2026-10" and segment product group "MORTGAGE"
    Given the approval "APR-2026-1201" of rwb-decision is APPROVED for the change of "SCREENING" to level "L1" from 2026-12-15

  Scenario: AC1 Raise or lower an autonomy level with approval (legacy RWB-E8-004 AC1)
    Given the rwb-decision contract mock returns the approval record "APR-2026-1201" with status APPROVED and the approved level "L1"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then steps an agent up on measured evidence, and drops it on a breach, with the approval each needs
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-004 AC2)
    Given the rwb-decision decision-record mock refuses the write with 503
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A raised level is a new approved version of the policy row (new, D-RCV-60)
    Given the approval "APR-2026-1201" of the background
    When the risk and model risk officer loads policy version "P2" of "SCREENING" with autonomy_mode "L1" and valid_from 2026-12-15 and approves it
    Then one agent_policy row holds agent_code "SCREENING", policy_version "P2", autonomy_mode "L1", status "APPROVED", valid_from 2026-12-15, loaded_by the loader identity and approved_by the approver identity
    Then version "P1" keeps its own row with autonomy_mode "SHADOW" and every field but status and valid_to unchanged
    Then version "P1" holds status "RETIRED" and valid_to 2026-12-14
    Then both rows are read and written in rwb_agent and no table of another schema is read or written

  Scenario: AC4 A lowered level is a new version too (new, D-RCV-60)
    Given policy version "P1" of "SCREENING" is APPROVED with autonomy_mode "L1" and valid_from 2026-11-01
    Given an agent_alert row with alert_type "DRIFT" was raised for "SCREENING" on 2026-12-14
    When the officer loads and approves policy version "P2" with autonomy_mode "SHADOW" and valid_from 2026-12-15
    Then one agent_policy row holds policy_version "P2", autonomy_mode "SHADOW", status "APPROVED" and valid_from 2026-12-15
    Then a run on 2026-12-14 holds autonomy_mode "L1" and a run on 2026-12-15 holds autonomy_mode "SHADOW"
    Then the drop needs the same approval as the raise and no level changes without one

  Scenario: AC5 The approval is read from rwb-decision and its reference is held on the version (new, D-RCV-60)
    Given version "P2" of "SCREENING" is LOADED with autonomy_mode "L1" and valid_from 2026-12-15
    When the officer approves version "P2" under approval "APR-2026-1201"
    Then the approve call makes one read of GET /api/recovery/decision/v1/approvals/APR-2026-1201, one hop, inside the 2 s budget
    Then version "P2" is APPROVED and holds the approval reference "APR-2026-1201" on its row
    Then no approval_level of LOV-APPROVAL-LEVEL is read as an autonomy level and no autonomy level is taken from a list other than LOV-AUTONOMY
    Then an approval that is not APPROVED, and an approval whose approved level is not the autonomy_mode of the version, are each refused with 409 and the version stays LOADED

  Scenario: AC6 The change is written to the decision record and the shared topic (new, D-RCV-60)
    Given the approval read of AC5 and the loaded version "P2"
    When the approval takes effect for 2026-12-15
    Then one decision record is written before the version is in force, naming agent "SCREENING", policy version "P1" with autonomy_mode "SHADOW", policy version "P2" with autonomy_mode "L1", the approval reference "APR-2026-1201", the approver identity and valid_from 2026-12-15
    Then the record is hash-linked to the previous record and carries the decision code read from LOV-DECISION for the change
    Then rwb.decision-record.DecisionRecorded.v1 is written to the outbox on rwb.decision-record.v1 with the record reference and the change facts
    Then the record is written through the local decision-record library and rwb_agent holds no copy of decision_log_entry
    Then either call repeated under the same Idempotency-Key returns the first answer, writes no second record and no second outbox row

  Scenario: AC7 The approval and the change commit together or not at all (new, D-RCV-60)
    Given version "P2" of "SCREENING" is LOADED with autonomy_mode "L1" and the approval "APR-2026-1201" is APPROVED
    When the record write is forced to fail on the approve call
    Then version "P2" keeps status "LOADED" with no approval reference
    Then version "P1" keeps status "APPROVED", keeps autonomy_mode "SHADOW" and stays in force
    Then no outbox row exists for the change and no record exists for it
    Then the approve call answers 503 and a later read of GET /api/recovery/agent/v1/admin/agent-configs shows no partial change

  Scenario: AC8 A refused approval leaves the version in force untouched (new, D-RCV-60)
    Given version "P2" of "SCREENING" is LOADED with autonomy_mode "L1" and valid_from 2026-12-15
    Given the approval "APR-2026-1201" is REFUSED, then RETURNED, in rwb-decision
    When the officer approves version "P2" on each
    Then version "P2" keeps status "LOADED", holds no approval reference and has no record
    Then version "P1" keeps status "APPROVED" and autonomy_mode "SHADOW" and stays in force
    Then the next agent run of "SCREENING" holds autonomy_mode "SHADOW" and no run holds "L1"
    Then a load whose approval is refused may be replaced by a new load, and no refused version is edited in place

  Scenario: AC9 The two operations run on the rwb-agent base through the gateway-bff route only (new, D-RCV-60)
    Given the officer steps "SCREENING" up from SCR-46 Agent monitor
    When the load and the approval are submitted
    Then the browser calls the gateway-bff composite route only, and the two calls that reach rwb-agent are POST /api/recovery/agent/v1/admin/agent-configs and POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve
    Then no call is made to a path outside the rwb-agent base and no owner service is called directly by the browser
    Given user "U-5001" holds a role whose Rules and parameters right is R only
    When "U-5001" calls either operation
    Then the call is refused with 403 and MSG-P4-002, version "P2" stays "LOADED" and version "P1" stays in force
    Given user "U-5002" holds Platform administration R only
    When "U-5002" calls the approve operation
    Then the call is refused with 403 and MSG-P4-002, because the change needs the Rules and parameters right A and not the Platform administration right

  Scenario: AC10 Only the listed autonomy levels are stored (new, D-RCV-60)
    Given the level values of LOV-AUTONOMY are OFF, SHADOW and L1
    When a version of "SCREENING" is loaded with autonomy_mode "L1" and another with autonomy_mode "L2"
    Then the "L1" version is stored with status "LOADED" and valid_from as given
    Then the "L2" load is refused with 422 and no agent_policy row is written for it
    Then no stored autonomy_mode holds a value outside LOV-AUTONOMY, and no level above L1 is defaulted to a listed one
```

AC1 and AC2 are the legacy criteria of RWB-E8-004, copied verbatim: every Given, When and Then line of the legacy fence appears unchanged and in the legacy order. **Target reading.** AC1 gets one inserted first Given, `Given the rwb-decision contract mock returns the approval record "APR-2026-1201" with status APPROVED and the approved level "L1"`, because the criterion asserts a cross-service read that can be mocked: the approval the change needs is a record of rwb-decision and the test must be able to state it. AC2 gets one inserted first Given, `Given the rwb-decision decision-record mock refuses the write with 503`, because the criterion asserts a cross-service write failure that can be mocked: the decision log of the legacy sentence is the local decision record written through the P7 library, and the test drives its failure through the fake rather than through a stopped store. No other legacy line is added, moved or reworded. The words "the rule version" in AC1 are kept as the legacy story wrote them; in the target they read as the policy version of `agent_policy`, because no Drools package decides an autonomy change (BR4). AC3 to AC10 are new for this service change and test only the version, the approval reference, the record, the transaction, the refusal and the route.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An autonomy level changes only as a new version of the agent's policy row that is loaded and then approved: no version is created APPROVED and no approved version is edited in place | FEAT-AGT-15; FSD P10 v3 A2.15 and A2.12; legacy RWB-E8-004 AC1 |
| BR2 | A step up needs measured evidence and a drop needs a breach, and both need the approval each needs: the evidence reference is `agent_policy.evaluation_run_id` and the breach is an `agent_alert` row with `alert_type` DRIFT | FEAT-AGT-15; FSD P10 v3 A2.15; DF-AGT-017; DF-AGT-105; ASM-1023, ASM-1024 |
| BR3 | The approval is a fact of rwb-decision, read through its contract by approval id; the version stores the approval reference it was granted under | FEAT-AGT-15; Arch v5 slide 41; legacy RWB-AD-020 AC2; ASM-1025 |
| BR4 | The version on the decision record is the policy version of `agent_policy`; no rule row is read and no Drools package version is named, because no package decides an autonomy change | Legacy RWB-E8-004 data table (`rule_row`); DP-01; TSD P10 v2 T3.1 |
| BR5 | The decision record is written before the version takes effect and no change proceeds unrecorded: the version row, the record and the outbox row are one transaction | Principle 5; R-UNI-39; DP-03 |
| BR6 | No value a business person may change is written in code: the level, the valid-from date, the evidence, the approval and the review date are rows of the policy version or of the approval | BR-P10-015; VR-P10-015-1 |
| BR7 | An autonomy level is a value of LOV-AUTONOMY, OFF, SHADOW or L1, and the DoA `approval_level` of LOV-APPROVAL-LEVEL is a different value that is never read as an autonomy level | TSD P10 v2 T3.2; TSD P7 v2 T3.2; ASM-1022, ASM-1025 |
| BR8 | The approval must be APPROVED and its approved level must be the `autonomy_mode` of the loaded version; a mismatch, a refusal, a return or an unknown approval changes nothing | FSD P10 v3 A2.15; TSD P10 v2 T-A.2 API-P10-004; ASM-1025 |
| BR9 | A superseded version closes with `valid_to` the day before the new `valid_from` and status RETIRED; every other field of it, including its level, stays as approved | TSD P10 v2 T3.1 DF-AGT-021 to DF-AGT-023; ASM-1027 |
| BR10 | One REST base and one topic per service: the two write operations are on `/api/recovery/agent/v1` and the open events are the shared decision-record topic and `rwb.agent.events.v1`, which publishes AgentRunCompleted only | DP-13; DP-14; Arch v5 slide 41 and slide 43 row 28 |
| BR11 | The screen composes the level, the version and the approval through the gateway-bff route and calls no owner service directly | DP-19; Arch v5 slides 8, 10 and 41 |
| BR12 | A repeat of either call under the same Idempotency-Key returns the first answer, writes no second row and no second record, and the repeat is counted | R-UNI-40; TSD P10 v2 T-A.2 API-P10-003 and API-P10-004 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | LOAD | a checked file is loaded for an agent with a new policy version and a level of LOV-AUTONOMY | LOADED |
| LOADED | APPROVE | the approval is APPROVED for the same level and the record, the row and the outbox row commit | APPROVED |
| LOADED | APPROVE_REFUSED | the approval is REFUSED or RETURNED, or the approved level differs | LOADED, with no approval reference |
| LOADED | RECORD_WRITE_FAILED | the local decision record cannot be written | LOADED, because the transaction rolls back |
| APPROVED | SUPERSEDE | a later version is approved with a later `valid_from` | RETIRED, with `valid_to` set |
| APPROVED | APPROVE | a second approval of the same version | APPROVED, refused with 409 |

These are the states of `agent_policy.status` under LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED) and nothing else (TSD P10 v2 T3.1, DF-AGT-021). **This story moves no case status**: `recovery_case.status` is neither read nor written, no task and no assignment row is written, and the case side of an autonomy change belongs to rwb-case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Risk and model risk officer (RW-RISK) | The primary actor: reads SCR-46, decides the step up or the drop, and approves the version under the committee approval |
| Center of excellence analyst (RW-COE) | Loads the version, owns the policy rows, their level, their valid-from date and their evidence, and reads the change back |
| Platform administrator (RW-PLATADM) | Reads the runs and the versions, and may reload a version; holds Platform administration CRUD and CRUDA but not the Rules and parameters right the change needs unless rwb-access grants it |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the two operations; reads the policy rows and writes the version row, the record and the outbox row |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| rwb-decision owner | Owns the approvals, their DoA routing and the approval read this story consumes |
| SY-RULES rules identity | Not used by this story: no Drools package is evaluated for an autonomy change, so no rule row and no package version is read |
| RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-SECADM | Read the version, its level and its approval through the monitor read, as the legacy permission list allows |
| RW-REFADM | Holds no Rules and parameters right and no Platform administration right; refused with MSG-P4-002 |

The legacy permission list of RWB-E8-004 gives Platform administration R to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM and does not list RW-RISK, while FSD P10 v3 A2.15 names the risk and model risk officer as the primary user and the TSD gives the two write operations the Rules and parameters right C and A. The two readings are reconciled here as they are for the rest of the service: Platform administration R stays the read on SCR-46, and the change itself needs Rules and parameters C to load and A to approve. The right under which RW-RISK holds A is Not specified in the source documents (GAP-0640; ASM-1028) and is settled by rwb-access with the approval story of P7. The per-service login name is Not specified in the source documents (GAP-0640; ASM-1029).

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-001 to DF-AGT-025 | agent_policy | id, agent_code, policy_version, model_code, model_version, autonomy_mode, segment_product_group, confidence_floor, timeout_seconds, daily_cost_cap_thb, evaluation_run_id, status, valid_from, valid_to, loaded_by, approved_by | Write on the new version; read on the version in force and on the version being superseded |
| Not in TSD P10 v2 T3.1 | agent_policy | the approval reference of the version: the approval id the level was granted under, agreed as the backward-compatible column `approval_ref` | Write at approval, read back on the version |
| DF-AGT-036 to DF-AGT-060 | agent_run | agent_code, agent_version, autonomy_mode, run_at, decision_log_id | Read, to prove which level a run used |
| DF-AGT-103 to DF-AGT-111 | agent_alert | agent_code, alert_type, business_date, measured_value, threshold_value | Read, to name the breach behind a drop |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | every field of the record, written through P7's library and sealed by rwb-decision | Write locally |
| DF-DEC-034 to DF-DEC-053 | approval (rwb_decision, owner P7) | id, decision_code, status, approver and the approved scope; read through rwb-decision's contract only | Read, through P7's contract (DP-01) |
| DF-REF-001 to DF-REF-015 | rule_row (rwb_decision, owner P7) | No longer read by this slice: the version on the decision is `agent_policy.policy_version` and no Drools package is evaluated | Not used |

Field IDs are those of the Logical Data Model and Data Dictionary v9. The version row is written inside `rwb_agent` and no foreign key crosses a schema (DP-01). The approval is read through rwb-decision's contract and never from `approval` directly. The approval reference column is Not specified in the source documents (GAP-0640; ASM-1026): TSD P10 v2 T3.1 ends `agent_policy` at DF-AGT-025 `approved_by` and no source names a column for the approval, while legacy RWB-AD-020 AC2 requires the version to show the approval reference. No account, no customer and no personal data is written by this story: the row holds an agent code, a level, a version label and an approval id.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Method | Path | Right | Errors | Idempotency |
|---|---|---|---|---|---|
| API-P10-003 load a version | POST | `/api/recovery/agent/v1/admin/agent-configs` | Rules and parameters C | 401, 403, 409, 422, 503 | Idempotency-Key header |
| API-P10-004 approve a version | POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | Rules and parameters A | 401, 403, 404, 409, 503 | Idempotency-Key header |

The shapes, the request bodies, the rights, the error codes and the Idempotency-Key rules are baselined by RWB-P10-E8004-CON and are not restated here. What this story adds to them is the behaviour behind them: the level of LOV-AUTONOMY on the loaded version, the approval read, the approval reference on the row, the decision record and the atomic effect. The read that shows the result, `GET /api/recovery/agent/v1/admin/agent-configs` (API-P10-002) and `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001, the legacy read of this key on the rwb-agent base), belongs to the agent monitor and configuration stories and is consumed here, never re-declared.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | rwb-decision (P7), API-P7-008 | The approval of the change: its id, its status of LOV-APPROVAL-STATUS, its decision code and the approved autonomy level of its subject (DP-11) | One hop, 2 s |

The operation is rwb-decision's and is consumed as published; its field-level answer is Not specified in the source documents beyond "Read one approval with its routing details for the decision screen" (GAP-0640; ASM-1025). No `POST /api/recovery/access/v1/authorise` call is made by this service: the two operations declare their right and the gateway-bff route asserts it, and DP-08 is not a pattern of this key.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, agent code, previous policy version and level, new policy version and level, approval reference, approver identity role, valid-from date |

The row is written to the outbox in the same transaction as the version row and relayed with the CloudEvents envelope (DP-03). No `rwb.agent.events.v1` event is published for the change: the P10 OUT line of Arch v5 slide 16 and the event catalogue row 28 name AgentRunCompleted only, so the level is read from the table through the monitor read and not from a topic. No personal data is carried.

#### 12.4 Events consumed

None. The change is made on a request path and reads no topic; it has no inbox handler of its own.

#### 12.5 Workflows and activities

None in this story. The change is synchronous on the two request paths and starts no workflow and no activity on task queue `rwb-agent`. The approval itself is routed by the kit's ApprovalWorkflow on rwb-decision, which is rwb-decision's and is read here through the approval contract, not through Temporal (Temporal and Drools design slide 12 and slide 13).

#### 12.6 Schedules

None. No job in the Arch v5 job map belongs to an autonomy change (slide 44), and no Schedule is created, changed or owned by this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_policy | P10 (rwb_agent) | The version row: written on the new version and on the `valid_to` and status of the superseded one; DF-AGT-001 to DF-AGT-025 plus the approval reference column |
| agent_run | P10 (rwb_agent) | Read only here: the level each run used |
| agent_alert | P10 (rwb_agent) | Read only here: the breach behind a drop |
| outbox_event, idempotency_key | PLT library, created in rwb_agent | The transaction outbox and the idempotency envelope, used through the decision-record library and the platform library (DP-03) |

`approval` and `decision_log_entry` are rwb-decision tables and are reached only through the P7 contract and the P7 library (DP-01, DP-03). No copy of an approval row is written into `rwb_agent`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock — approvals | The P7 approval read of DP-11 | An APPROVED approval for level "L1"; one for level "SHADOW"; a REFUSED and a RETURNED approval; an approval whose level differs from the loaded version; a 404 for an unknown id; a slow answer beyond the 2 s budget |
| Decision-record library stub | The P7 record contract and `rwb.decision-record.v1` (DP-03) | A committed record with its reference; a forced write failure with 503; the outbox row and its relay |
| gateway-bff composite route stub | The DP-19 route of SCR-46 and the two admin paths | The merged screen answer with the version, the level and the approval; the refusal of a role without Rules and parameters C or A with MSG-P4-002 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The load and the approve on `/api/recovery/agent/v1`; the P7 approval read; one hop, 2 s; the two reads the screen needs belong to other stories |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox; nothing consumed |
| Temporal | None | No workflow and no activity on `rwb-agent`; the ApprovalWorkflow is rwb-decision's |
| File | None | This story reads and writes no file; the load's checked file is the contract's and is carried by the load operation |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `autonomy`, Java package `th.co.scb.ace.workbench.recovery.agent.autonomy`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is applied throughout as the schema rule of the service: the level, the evidence, the breach and the version are read and written in `rwb_agent`, and the approval is read from rwb-decision's contract and never from its table. DP-01 adds no dependency, which is why the metadata rows carry the same set as the WP.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ConfigVersionController | REST controller | The two operations of API-P10-003 and API-P10-004, their validation, their Idempotency-Key and the mapping of errors to problem responses (the shapes are the contract's) |
| AutonomyChangeService | Service | Applies the level rules of BR1, BR7 and BR8, drives the approval read, and calls RecordAndApply |
| ApprovalClient | Client | Calls `GET /api/recovery/decision/v1/approvals/{approvalId}` with one hop, the 2 s timeout and a breaker per downstream (DP-11) |
| PolicyVersionRepository | Repository | Writes the loaded version and the approved version, and closes the superseded one, in `rwb_agent` only |
| DecisionRecordWriter | Library adapter | Writes the local decision record with both versions, both levels, the approval reference and the valid-from date, hash-linked, in the same transaction (DP-03) |
| IdempotencyFilter | Platform library | Holds the Idempotency-Key of each POST and returns the first answer on a repeat |

**Database and migrations**

- One column on `agent_policy`: the approval reference, agreed as `approval_ref`, nullable until the version is approved and immutable afterwards, holding the approval id of rwb-decision (GAP-0640; ASM-1026). No table and no other column is added: every other field this story uses is DF-AGT-001 to DF-AGT-025.
- The script takes its number from the rwb-agent Flyway sequence; that number is Not specified in the source documents (GAP-0640; ASM-1026) and no number is claimed here.
- Two indexes for the change, on the keys it reads: `agent_policy (agent_code, status, valid_from)` so the version in force is a key lookup, and a unique index on the approval reference so one approval cannot carry two versions. The index names are naming-library values and not business values.

**Configuration and reference data**

- Policy versions (RW-COE): `agent_code` over LOV-AGENT, `policy_version`, `model_code`, `model_version`, `autonomy_mode` over LOV-AUTONOMY, the segment product group, `confidence_floor`, `timeout_seconds`, `daily_cost_cap_thb`, `evaluation_run_id`, `status`, `valid_from` and `valid_to`.
- The approval record of rwb-decision: its status over LOV-APPROVAL-STATUS and its DoA level over LOV-APPROVAL-LEVEL, which is never read as an autonomy level (ASM-1025).
- List values of TSD P10 v2 T3.2: LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT, held as reference data by rwb-case under the §R3 default ruling; the service reads no list row and holds no copy of a list in code.
- The decision code of an autonomy change and the wording of a value outside LOV-AUTONOMY are Not specified in the source documents (GAP-0640; ASM-1026).

**Build steps**

1. PolicyVersionRepository and the version-in-force query, with the close of the superseded version; tests for AC3 and AC4.
2. ApprovalClient against the rwb-decision fake, with the 2 s timeout, the breaker, the status check and the level check; tests for AC5, AC8 and X1 to X3.
3. AutonomyChangeService with the level rules and the four-eyes and second-approval refusals; tests for AC2 and AC10.
4. DecisionRecordWriter in one transaction with the row and the outbox row, and the rollback path; tests for AC6 and AC7.
5. The idempotency filter on both POSTs; test for AC6.
6. The gateway-bff route contract test with the two refusal paths; test for AC9.
7. The migration for the approval reference and its unique index; tests for AC5 and AC7.
8. Register the two operations in the service's OpenAPI document from the baseline of RWB-P10-E8004-CON and drop the old monolith base from the service's route table; test for AC9.

**Done when.** The tests in section 16 pass, no version is APPROVED without an approval reference and a record, every level in force is a value of LOV-AUTONOMY, a refused approval left the version in force untouched in the SIT run, and the contract tests of RWB-P10-E8004-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | A required value of the load or of the version is empty | Enter {field}. |
| MSG-P4-002 | A role without the Rules and parameters right C or A calls either operation | You cannot {action} here. Your role does not include it. |
| MSG-P7-002 | The caller loaded the version and also approves it | Not restated here: the message is rwb-decision's four-eyes message, named by FSD P10 v3 A2.1 AC-EXC-P10-001-03 with the 409, and its wording is not in the extracts |

The first three messages are the legacy messages of RWB-E8-004 and keep their wording character for character. MSG-P7-002 is named by ID and not restated. No other message is added by this story, and the wording of a refusal of a value outside LOV-AUTONOMY is Not specified in the source documents (GAP-0640; ASM-1026).

### 15. Screens and states

SCR-46 Agent monitor, states Shadow, live and paused, is the screen of the legacy story and it is where the officer acts. The screen and its read belong to the agent monitor story (RWB-P10-E1063-APP) and this story does not change them; what this story adds is the action on the screen and the data behind it: the agent, its policy version in force, its level, the approval reference and the version history, all of them read from `agent_policy` through the monitor read and the gateway-bff composite route (DP-19). The three states are the states of the monitor, not of a version: a version is LOADED, APPROVED or RETIRED (BR9), and the monitor shows a paused agent as paused whatever version is in force. The screen fields, their order, the label of each level and the masking are Not specified in the source documents (GAP-0640; ASM-1028) and stay with the monitor story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-004-01 | AC1 | Component | Agent "SCREENING" in force at "SHADOW"; the approval "APR-2026-1201" APPROVED for "L1"; the load and the approve of "P2" |
| TC-E8-004-02 | AC2 | Component | Decision-record write stopped through the library stub; nothing changes and MSG-P7-003 is shown |
| TC-E8-004-03 | Access | Component | User "U-5001" holding Rules and parameters R only, and user "U-5002" holding Platform administration R only; each refused with MSG-P4-002 |
| TC-E8-004-04 | Principle 5 | NFR | Decision-record write forced to fail on the approve call; no APPROVED version, no outbox row and no record |
| TC-E8-004-05 | AC3 | Component | Version "P1" APPROVED at "SHADOW" from 2026-11-01; "P2" loaded at "L1" from 2026-12-15 and approved; snapshot of both rows |
| TC-E8-004-06 | AC4 | Component | Version "P1" APPROVED at "L1"; one DRIFT alert on 2026-12-14; "P2" loaded at "SHADOW" from 2026-12-15; runs on 2026-12-14 and 2026-12-15 |
| TC-E8-004-07 | AC5 | Contract | rwb-decision approval fake: APPROVED "L1", APPROVED "SHADOW", REFUSED, RETURNED, unknown id, slow answer; one DoA level "L6" that must not be read as an autonomy level |
| TC-E8-004-08 | AC6 | Component | The approve call of AC3; the record, the outbox row and the same call repeated under one Idempotency-Key |
| TC-E8-004-09 | AC7 | Component | The record write forced to fail after the row update; the version rows, the outbox and a later admin read |
| TC-E8-004-10 | AC8 | Component | A REFUSED then a RETURNED approval for the loaded "P2"; the next run of "SCREENING" |
| TC-E8-004-11 | AC9 | Contract | gateway-bff route stub and the two admin paths; the two refusal cases; an assertion that no request leaves the rwb-agent base |
| TC-E8-004-12 | AC10 | Component | A load at "L1" and a load at "L2"; the second refused with 422 and no row |

The legacy levels map System to Component, Access to Component and Principle 5 to NFR, because the cross-service behaviour of this key is proved by the integration story of the wave. No `-ITG` copy is held here: the integration copies of this key belong to the integration story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the level, the valid-from date, the evidence, the approval and the review date are rows of the policy version or of the approval (BR-P10-015).
- No personal data in logs, tests, workflow history or prompts: the rows hold an agent code, a level, a version label and an approval id; no account, no customer and no name is read, written or logged.
- No read of another service's tables: the approval comes through rwb-decision's contract and the record through the P7 library; `rwb_agent` holds no foreign key into another schema (DP-01, DP-03).
- The decision record is written before the version takes effect, in one transaction with the row and the outbox row; a failed write rolls the whole transaction back (R-UNI-39).
- A version is never edited in place once approved: a change is a new version, and the superseded one closes with a date and a status (BR1, BR9).
- No level outside LOV-AUTONOMY is stored and no level is defaulted to a listed one; the DoA level of an approval is never taken as an autonomy level (BR7).
- The screen calls no owner service directly; every read and every write reaches rwb-agent through the gateway-bff route (DP-19).
- Only a version row, a record and an outbox row are new data; no copy of an approval row or of a run row is written outside its owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | A level is raised on measured evidence and dropped on a breach, with the approval each needs, and the result is recorded with the rule version | No BRD section carries the feature (GAP-0640) | FEAT-AGT-15 | All recovery processes (legacy RWB-E8-004) | R-UNI-39 | TC-E8-004-01, TC-E8-004-05, TC-E8-004-06 |
| None (the legacy story carries no requirement ID) | Nothing changes when the decision cannot be recorded, and the user sees MSG-P7-003 | No BRD section carries the feature (GAP-0640) | FEAT-AGT-15 | All recovery processes | R-UNI-39 | TC-E8-004-02, TC-E8-004-04, TC-E8-004-09 |
| D-RCV-60 DP-01 | The level, the version and the evidence are rows of `rwb_agent`; the approval is read from its owner | Template and Rules §R5.5 DP-01; Arch v5 slide 41 | FEAT-AGT-15 | All recovery processes | None | TC-E8-004-05, TC-E8-004-06 |
| D-RCV-60 DP-03 | The decision record is written locally before the change and carried to the central ledger on the shared topic | Template and Rules §R5.5 DP-03; ADR-022 | FEAT-AGT-15 | All recovery processes | R-UNI-39 | TC-E8-004-02, TC-E8-004-04, TC-E8-004-08 |
| D-RCV-60 DP-13 | The two write operations sit on `/api/recovery/agent/v1` and the old monolith base is gone | Template and Rules §R5.5 DP-13; Arch v5 slide 41 | FEAT-AGT-15 | All recovery processes | None | TC-E8-004-11 |
| D-RCV-60 DP-19 | The screen composes the version, the level and the approval through the gateway-bff route and calls no owner service directly | Template and Rules §R5.5 DP-19; Arch v5 slides 8 and 41 | FEAT-AGT-15 | All recovery processes | None | TC-E8-004-11, TC-E8-004-03 |

The legacy story RWB-E8-004 carries no requirement ID: it names its feature (FEAT-AGT-15) and no BRD in the extracts carries that feature, so no BRD section and no requirement is cited for it and the absence is recorded as GAP-0640. The feature source is the Epics 3 to 8 Specification v3 row E8 · P10 · FEAT-AGT-15 and FSD P10 v3 A2.15; the rule is R-UNI-39; the decision is D-RCV-60.

### 19. Out of scope

- The configuration operations baseline of the two admin paths, their shapes, request bodies and error catalogue (RWB-P10-E3030-CON) and the plain level change of Epic 3 (RWB-P10-E3030-APP).
- The autonomy level per decision step and its per-step resolution (RWB-P10-AD020-APP and RWB-P10-AD020-CON).
- The agent runtime, the run itself, the guardrail checker and the 60-second rule fallback (RWB-P10-E1058-APP and RWB-P10-E1058-CON).
- The agent monitor, its read, the screen SCR-46 and its three states (RWB-P10-E1063-APP).
- The measured evidence itself: the evaluation harness of RWB-P10-E1058-APP, the extraction evaluation of RWB-P10-E1060-APP and the champion and challenger comparison of RWB-P10-E8003-APP.
- The drift alert that triggers a drop and its own decision (RWB-P10-E3031-APP); this story reads the alert row and does not raise it.
- The review of agent risk at the committee and the committee's decision (RWB-P10-E8005-APP and RWB-P10-E8005-CON).
- The approvals, their DoA routing, their statuses and the central ledger (P7 rwb-decision).
- The roles, the rights, the scope, the masking rules and the reconciliation of the RW-RISK right (P4 rwb-access).
- The parameters and the lists (P3 rwb-case under the §R3 default ruling).
- The gateway-bff route contract itself (RWB-PLT-N001-CON) and the decision-record library itself (RWB-PLT-E1027-CON).
- The real cross-service proof of the load, the approval and the effect (the integration story of wave 4).
- The deployment of this capability: chart values, dashboards and the runbook.
