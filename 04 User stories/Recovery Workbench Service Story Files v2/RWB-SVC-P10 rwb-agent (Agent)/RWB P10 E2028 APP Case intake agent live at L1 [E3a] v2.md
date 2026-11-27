# RWB-P10-E2028-APP Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Contract version | Not specified in the source documents (DOR-RWB-P10-E2028-APP-23) |
| Patterns applied | DP03, DP07, DP08, DP09, DP10, DP13, DP15, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E2031-APP and RWB-P10-E2028-OPS |
| Depends on (build) | RWB-P10-E2028-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E2031-APP, RWB-P10-E1061-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1035-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P10-E2028-OPS |
| Deployment values | Not specified in the source documents (GAP-0624; GAP-2192): the rwb-agent login, the topic partitions, retention and retry names, the migration order, the alert window and thresholds, the worker and probe values, the consumer groups, the route path (GAP-0623) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E2-028 for rwb-agent. The behaviour of the legacy story is kept whole and its nine criteria are carried word for word: the intake summary and its gap flags shown on the case record as agent output, the accept, correct and reject controls, the acceptance and correction rates by segment, the fallback, the reason rule, the unrecordable decision, the double feedback, the out-of-scope case, the segment still in shadow and the stale input. Only the seams move, and each one is written down in this document: the L1 gate lives in rwb-agent and its mode, segment, segment threshold and confidence floor are policy data of the approved `agent_policy` row of schema `rwb_agent` (DP-01 as the service's own schema, DP-15 for the migration of `agent_feedback`); the decision record of each accepted, corrected or rejected recommendation goes through the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03); the segment reference values and the lists are read through the rwb-case reference-data contract (DP-07); the case record read and the case-decision proposal are the rwb-case contract of RWB-P3-E1035-CON (C only, never a build dependency); the run is an event-started Temporal workflow on the queue `rwb-agent` (DP-10); the run facts and the L1 acceptance record leave on `rwb.agent.events.v1` through the outbox (DP-09); the two operations sit on the base `/api/recovery/agent/v1` (DP-13); the `agent_feedback` table arrives with the service's own Flyway sequence (DP-15); and the panel is reached through the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E2028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 15 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the intake summary and its gap flags shown on the case record for every new case of a segment where the agent runs at L1, marked as agent output, with a control to accept, correct or reject it, the verdict written as a decision record of the local library and the acceptance measured by segment**, so that **I start from a summary instead of reading every file, and the bank measures how often the summary is right before the next segment is opened**.

### 2. Business rationale

A case owner reads accounts, documents, appraisals and contact points before the first action on a new case. The shadow run of the intake agent gave a measured agreement per gap type; this story opens one segment at autonomy level 1, shows the summary of that segment only, and records every verdict so the acceptance and correction rates of the segment are known before a second segment is considered (REQ-DRI-001). Personal data stays masked in the agent call and in the stored summary, and the panel shows masking tokens (REQ-ACA-005).

In the legacy delivery the run, the policy, the prompt, the feedback row, the decision log and the case record sat in one module and one schema: the intake listener called an in-process orchestrator, the mode came from a loader table beside the code, the decision log was written by a `DecisionLogWriter` of the same deployment, the case facts and the owner check came from `CaseQueryService`, the acceptance figures were read from a daily copy, and the panel called the service directly. The behaviour does not change, so the nine criteria, the policy version "P2", the prompt "PR3" and every legacy value are carried onto the service. What changes is where each fact lives and how it is reached:

- **The L1 gate is rwb-agent's own.** The autonomy mode, the segment (product group and region), the segment threshold that decides whether a case of the segment is eligible at L1, and the confidence floor below which a summary is marked are columns of the approved `agent_policy` row (`autonomy_mode` DF-AGT-008, `segment_product_group` DF-AGT-009, `segment_region_code` DF-AGT-010, `confidence_floor` DF-AGT-011) in schema `rwb_agent`, read at run time and at read time. No value of them is written in the source, and no other service decides the mode of a case (DP-01, DP-15).
- **The decision record of a verdict is local and sealed centrally.** Each accept, correct and reject writes one record through the decision-record library of RWB-PLT-E1027-CON in the same transaction as the feedback row and publishes it on the shared topic `rwb.decision-record.v1`; rwb-decision collects it into the central ledger and owns `decision_log_entry` (DP-03; H RWB-PLT-E1027-CON, C RWB-P7-E1027-CON).
- **The segment reference values and the lists are rwb-case's.** LOV-PRODUCT, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION, LOV-AGENT and LOV-AGENT-RUN are versioned reference data read through the reference-data contract of RWB-P3-E1043-CON, so a list change is a data change of its owner and never a release of this service (DP-07).
- **The case record is rwb-case's.** The case facts, the owner and the team scope are read through the case record contract of RWB-P3-E1035-CON, and the owner's verdict is proposed to that contract so the case record shows it; rwb-agent writes no case row and holds no foreign key across a schema (C RWB-P3-E1035-CON).
- **The run is an event-started workflow.** The intake run is one `AgentRunWorkflow` execution per case and triggering event on the task queue `rwb-agent` in namespace `rwb-recovery`, started by the event, with the 60-second model budget of the policy and the rule result on timeout; no cadence and no Quartz entry belongs to it (DP-10).
- **The facts leave through the outbox.** The run completion (`rwb.agent.AgentRunCompleted.v1`, EV-28) and the L1 acceptance record (`rwb.agent.AgentFeedbackRecorded.v1`) are CloudEvents on `rwb.agent.events.v1`, keyed by the case, inserted in the outbox in the same transaction as the row and routed to the `.dlt` topic on a registry refusal (DP-09).
- **The two operations sit on the service base.** The agent-outputs read and the feedback operation answer on `/api/recovery/agent/v1`; the legacy monolith base is retired for them (DP-13).
- **The feedback table arrives with the service's own migration.** `V10_008__agent_feedback.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` with its unique key and its verdict check and touches no other schema (DP-15; H RWB-PLT-E1044-CON).
- **A screen reaches the panel through the edge.** The read and the verdict are reached through the gateway-bff route of RWB-PLT-N001-CON, one hop, so no screen calls rwb-agent directly (DP-19).

The cross-service behaviour of this key — that the summary really is built from facts rwb-case and rwb-source-data serve, that the verdict really appears on the case record, and that the record really is sealed in rwb-decision — is proved by the integration work of the wave 2 integration epic, RWB-ITG-W2, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes, owns the nine legacy criteria AC1 to AC9 and adds none, and states its service change in sections 8, 9, 12, 13 and 17 where the contract test cases of RWB-P10-E2028-CON prove the seam.

### 3. Preconditions

- RWB-P10-E2031-APP is done: the agent monitor of this service shows the acceptance and override rates of an agent per segment and business date on `GET /api/recovery/agent/v1/admin/agent-metrics`, so the figures of AC2 are served by that read and not by this story.
- RWB-P10-E2028-CON is baselined: the agent-outputs read and the feedback operation, the L1 output members, the L1 request and its outcome members, the segment eligibility answer, the decision-record mapping with its idempotency key, the event contract of `rwb.agent.AgentRunCompleted.v1` and of the L1 acceptance record `rwb.agent.AgentFeedbackRecorded.v1`, the gateway-bff route and the four fakes of section 12.8 exist as a document with the contract test cases `TC-P10-E2028-CON-01` to `TC-P10-E2028-CON-08`.
- RWB-P10-E1061-CON is in force: the L1 proposal payload and the configuration operations that load and approve policy version "P2" of agent "INTAKE" with its mode, its segment and its promotion condition, through the same-service contract of that key. The platform baseline of the service is RWB-P10-E1058-CON; it is named here as context and is not claimed as a build dependency.
- RWB-PLT-E1027-CON is published: the local decision-record library, the record type on the `rwb.decision-record.v1` topic, and its retry and `.dlt` rules (DP-03). RWB-PLT-E1043-CON is published: the reference-data client library (DP-07). RWB-PLT-TE006-CON is published: the outbox and inbox library, the CloudEvents envelope, the registry subject check and the `.dlt` route (DP-09). RWB-PLT-E1071-CON is published: the workflow kit with namespace `rwb-recovery`, the event-started workflow registration, the activity contract and the worker versioning (DP-10). RWB-PLT-E1044-CON is published: the per-service Flyway sequence with parameterized schema names (DP-15). RWB-PLT-N001-CON is published: the gateway-bff route contract and its stub (DP-19).
- The `rwb_agent` schema baseline exists with the standard record columns, the Flyway history table of the service, the six tables of RWB-P10-E1058-APP and `agent_feedback` from this story's own migration `V<next>__agent_feedback.sql` (next number of the service's own Flyway sequence: Not specified in the source documents (CG-ALL-2687)).
- The rwb-case contracts of RWB-P3-E1043-CON and RWB-P3-E1035-CON are published: the reference-data contract for the seven lists of section 12.2, and the case record contract for the case facts, the owner check and the case-decision proposal. A case outside the caller's scope is answered by that contract and surfaces as the legacy refusal of MSG-P4-003.
- The rwb-decision contract of RWB-P7-E1027-CON is published: the decision-log entry read, so the entry a verdict writes can be read back by its ID and the acceptance figures of the monitor can be counted per entry.
- The rwb-source-data freshness read of Arch v5 slide 15 (`GET /freshness` on the service base) is published: it answers the business date of the ACE load, which is the second value of AC9.
- Agent "INTAKE" has policy version "P2" approved with mode L1 for the segment MORTGAGE and BKK, prompt version "PR3", a 60-second timeout, the allowed tools of the approved row, its confidence floor and its segment threshold, and output schema "intake-v1"; the mode is SHADOW for every other segment, and the policy row is read as a version and never written by this story.
- Policy version "P2" is in force from 2027-01-25 and is approved by RW-RISK; the per-segment mode of BR1 is a value of that row and not a rule in code.
- The per-service login of rwb-agent under DP-02 (grants on schema `rwb_agent` only) is required by every read and write of this story and is Not specified in the source documents (GAP-0622; ASM-0916); the story names it "the rwb-agent login (DP-02)" until it is agreed.
- The service identity SY-AGENT holds the case, reference-data and freshness reads of section 12.2, so each read is answered under the same role check as a person.
- The release date 31 January 2027 is tentative and is copied unchanged.

### 4. Flow

1. SY-CASEWF writes EV-01 `rwb.case.CaseCreated.v1` for a new case; the intake listener of rwb-agent consumes it through its inbox, dedupes on the event ID, and starts one `AgentRunWorkflow` execution on the queue `rwb-agent` with the case ID and the event ID (DP-10; AC1, AC3).
2. `ResolveIntakeMode` reads the approved `agent_policy` row of agent "INTAKE" from `rwb_agent` and the segment of the case (product group, region) through the case record contract of RWB-P3-E1035-CON, and compares them with `segment_product_group`, `segment_region_code` and the segment threshold of the row: a case of the L1 segment runs in mode L1, every other case runs in SHADOW (AC8; BR1).
3. In mode SHADOW the run is stored as the shadow story of this service leaves it and no output is returned to a user; in mode L1 the run assembles its masked inputs, calls the model inside the policy budget, applies the guardrail and stores the summary and the gap flags on the run row with the agent version "INTAKE@P2/PR3" (AC1, AC3; BR7).
4. `RecordIntakeRun` writes the run status, the fallback flag, the guardrail result, the summary, the gap flags, the confidence and `data_as_of` in one transaction with the outbox rows, and never touches a case row, a task or a queue (BR8).
5. `PublishIntakeEvents` inserts `rwb.agent.AgentRunCompleted.v1` (EV-28) in the outbox, keyed by the case, and the relay publishes it on `rwb.agent.events.v1`, where rwb-decision, rwb-document, rwb-deviation and rwb-reporting consume it (DP-09).
6. The case owner opens SCR-03 Case record; the screen is composed by the gateway-bff route and calls `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` in one hop with the 2 s client budget (DP-13, DP-19; AC1).
7. `AgentOutputQueryService` answers the stored L1 outputs of the case only: a run of mode SHADOW is never returned, and a case whose segment is in SHADOW answers an empty list and no panel (AC8; BR1, BR6).
8. The panel "Agent summary" shows the summary, each gap flag with its reason, the agent "INTAKE", the version "INTAKE@P2/PR3", the marker "Agent output" and the controls Accept, Correct and Reject; a summary built on a business date later than its `data_as_of` shows MSG-P1-001 with that date above the summary (AC1, AC9).
9. The owner chooses Accept, or Correct, or Reject with a reason. `IntakeFeedbackService` validates the request: item key default "SUMMARY", verdict ACCEPTED, CORRECTED or REJECTED, and a reason required for CORRECTED and REJECTED at most 1 000 characters (AC4; BR4).
10. `RecordIntakeFeedback` writes, in one transaction, the decision record through the library of RWB-PLT-E1027-CON (decision "D6", agent version "INTAKE@P2/PR3", the model version, the run reference as the inputs snapshot, the recommendation, the final call, the reason and the owner), the `agent_feedback` row with the entry ID, and the outbox row of the acceptance record; nothing is stored if the record cannot be written (AC5; BR3, BR9).
11. The acceptance record `rwb.agent.AgentFeedbackRecorded.v1` is relayed on `rwb.agent.events.v1` with the run ID, the case ID, the item key, the verdict, the agent version and the entry ID, and carries no personal data (BR10).
12. The owner's verdict is proposed to the case record through the rwb-case contract of RWB-P3-E1035-CON, so SCR-03 shows the recorded verdict and its date while rwb-case owns the case row (AC1, AC2).
13. A second feedback request for the same run and item is refused with 409 and MSG-GEN-004 and leaves one record and one feedback row; a case outside the caller's scope is refused with 404 and MSG-P4-003 by the case record contract before any read of `rwb_agent` (AC6, AC7).
14. The monitor read of RWB-P10-E2031-APP aggregates the feedback of a business date per segment and answers the acceptance rate 0.8000 and the correction rate 0.1500 of "INTAKE" for MORTGAGE and BKK after the refresh of the reporting job (AC2).
15. Every read of another service is one hop on that service's base inside the 2 s client budget: the case facts and the case-decision proposal through rwb-case, the seven lists through the rwb-case reference-data contract, the entry read through rwb-decision, and the business date through the rwb-source-data freshness read (DP-07; the one-hop rule behind every consumed read).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent timed out or failed a guardrail for the case | The case record loads with no summary; the panel shows the message; the miss is on the agent run as TIMED_OUT or GUARDRAIL_FAILED with fallback true | MSG-P10-005 | AC3 |
| X2 | The owner corrects or rejects without a reason, or with a reason longer than 1 000 characters | Refused with 422 before anything is written | MSG-P7-005 | AC4 |
| X3 | The decision record cannot be written | The feedback is not stored, the controls stay on the panel, and an incident is raised under R-UNI-39 | MSG-P7-003 | AC5 |
| X4 | Feedback was already given, or two owners send at once, or the run row version does not match the `If-Match` header | The second request is refused with 409 and one record and one feedback row remain | MSG-GEN-004 | AC6 |
| X5 | The case is outside the user's scope | The case record contract answers not found and the read is refused with 404 | MSG-P4-003 | AC7 |
| X6 | The approved policy row of the case segment is mode SHADOW | The read returns an empty list and no panel is shown; no L1 output is ever returned | None to a user | AC8 |
| X7 | The run used data older than the business date | The panel shows the stale warning with the data date above the summary | MSG-P1-001 | AC9 |
| X8 | A role without Case record U sends feedback | Refused with 403 by the platform guard at the edge of the service | MSG-P4-002 | AC10, TC-E2-028-10 |
| X9 | The rwb-case case record read, the reference-data read or the case-decision proposal does not answer inside the 2 s budget | The read or the verdict is refused with 503 and nothing is stored; no default owner, scope or list is assumed and no case row is written by this service | MSG-P4-003 (the scope case) or none | AC11, TC-E2-028-13, TC-P10-E2028-CON-08 |
| X10 | The approved policy row of the segment carries no confidence floor, no segment threshold or no mode | The run and the read stop and the missing value is named; no code default is used | None to a user | AC12, TC-E2-028-14, TC-P10-E2028-CON-03 |
| X11 | The rwb-source-data freshness read fails while the run holds a `data_as_of` | The panel shows the summary with the stale warning of X7 and never claims a current business date | MSG-P1-001 | AC9 |
| X12 | The feature flag `rwb.agent.intake-l1` is off | The read answers an empty list and the panel is hidden, whatever the policy row says | None to a user | AC8 |

X1 to X8 are the legacy exception paths of RWB-E2-028 carried onto the service, with their legacy value, message and criterion unchanged; the legacy X8 (a role without Case record U) is reached by criterion AC10 and proved by the access test case TC-E2-028-10, and the message is kept so a reader finds the legacy set complete. X9 to X12 are the failures that appear when the case record, the reference data and the business date become contracts of their owners, when the mode becomes a row of the approved policy, and when the flag is read from the platform library instead of a local property.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the platform libraries, the published rwb-case, rwb-decision and rwb-source-data contracts with their fakes, its own CON and the two in-lane stories it waits for; it owns its own schema objects and its own migration |
| Negotiable | The package layout, the component names and the internal order of the read are design; the nine criteria, the policy version "P2", the prompt "PR3", the agent version "INTAKE@P2/PR3", the case IDs, the counts 300, 240, 45 and 15, the rates 0.8000 and 0.1500, the dates 2027-01-25, 2027-01-26 and 2027-01-28 and the message IDs are fixed by the legacy story |
| Valuable | Opens one segment at L1 with a measured acceptance and correction rate before a second segment is considered, and saves the owner the first read of every file |
| Estimable | One mode resolver, one read operation, one feedback operation with the decision record, one event pair and one migration, against five consumed reads |
| Small | One back end and one front end developer for two weeks, as in the legacy estimate |
| Testable | Each of the nine criteria is one automated test on an observable: a panel element, a stored run, a feedback row, a decision record, a refusal code, a rate or a date that did not move |

### 7. Acceptance criteria

```gherkin
Feature: Case intake agent live at L1 [E3a]

  Background:
    Given policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is in force from 2027-01-25
    Given case owner "owner.user07" holds RW-CASEOWN and owns case "RW-2027-000501"

  Scenario: AC1 Summary shown (legacy RWB-E2-028 AC1)
    Given the rwb-case contract mock returns case "RW-2027-000501" in the scope of "owner.user07"
    Given a new case "RW-2027-000501" with an ANSWERED intake run and gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL
    When the case record view loads
    Then the panel "Agent summary" shows the summary, the two gap flags with reasons, agent "INTAKE", version "INTAKE@P2/PR3" and the marker "Agent output"
    Then the controls Accept, Correct and Reject are shown
    Then the case record loads in under 2 seconds whether or not the panel has data

  Scenario: AC2 Acceptance measured (legacy RWB-E2-028 AC2)
    Given the rwb-decision decision-record contract mock returns one entry per feedback with decision "D6" and agent version "INTAKE@P2/PR3" and the monitor read of RWB-P10-E2031-APP returns acceptance 0.8000 and correction 0.1500 for "INTAKE" and MORTGAGE/BKK
    Given a month of summaries in January 2027 for segment MORTGAGE and BKK: 300 with feedback, 240 accepted, 45 corrected and 15 rejected
    When the dashboard refreshes after the reporting job of Arch v5 slide 44
    Then SCR-46 shows for "INTAKE" and MORTGAGE/BKK acceptance rate 0.8000 and correction rate 0.1500
    Then each feedback has one decision record with decision "D6" and agent version "INTAKE@P2/PR3"

  Scenario: AC3 Fallback (legacy RWB-E2-028 AC3)
    Given the rwb-case contract mock returns case "RW-2027-000502" in the scope of "owner.user07"
    Given the agent timed out for case "RW-2027-000502"
    When the view loads
    Then the case shows without a summary and the panel shows MSG-P10-005
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC4 Correction without a reason (legacy RWB-E2-028 AC4)
    When "owner.user07" chooses Correct on case "RW-2027-000501" with an empty reason
    Then the system refuses the request with 422 and MSG-P7-005
    Then no decision record and no feedback are stored

  Scenario: AC5 The decision cannot be recorded (legacy RWB-E2-028 AC5)
    Given the rwb-decision decision-record contract mock returns a failed record write
    Given the decision record writer fails
    When "owner.user07" chooses Accept
    Then the system refuses the request with 503 and MSG-P7-003
    Then no agent_feedback row exists for the run and the controls stay on the panel

  Scenario: AC6 Feedback given twice (legacy RWB-E2-028 AC6)
    Given the rwb-decision decision-record contract mock returns one entry for the accepted summary of case "RW-2027-000501"
    Given "owner.user07" accepted the summary of case "RW-2027-000501"
    When a second feedback request for the same run arrives
    Then the system refuses it with 409 and MSG-GEN-004
    Then one decision record exists for the run

  Scenario: AC7 A case outside the user's scope (legacy RWB-E2-028 AC7)
    Given the rwb-case contract mock returns case "RW-2027-000601" in team "HP-NE" outside the scope of "owner.user07"
    Given case "RW-2027-000601" belongs to team "HP-NE" outside the scope of "owner.user07"
    When "owner.user07" requests GET /cases/{caseId}/agent-outputs for it
    Then the system refuses the request with 404 and MSG-P4-003

  Scenario: AC8 A segment still in shadow (legacy RWB-E2-028 AC8)
    Given the rwb-case reference-data contract mock returns segment UNSECURED in LOV-PRODUCT
    Given the INTAKE policy for segment UNSECURED is mode "SHADOW"
    When the owner opens unsecured case "RW-2027-000701"
    Then GET /cases/{caseId}/agent-outputs returns an empty list and no panel is shown

  Scenario: AC9 Stale input (legacy RWB-E2-028 AC9)
    Given the rwb-source-data freshness contract mock returns business date 2027-01-28 over the ACE load of 2027-01-26
    Given the run for case "RW-2027-000503" used data as of 2027-01-26 and the business date is 2027-01-28
    When the view loads
    Then the panel shows MSG-P1-001 with the date 2027-01-26 above the summary

  Scenario: AC10 Refused for a role without Case record U (new, D-RCV-60)
    Given a user holding Case record R only sends feedback on the run of case "RW-2027-000501"
    When the feedback request reaches the service
    Then the platform guard refuses the request with 403 and MSG-P4-002

  Scenario: AC11 The rwb-case read does not answer inside the 2 s budget (new, D-RCV-60)
    Given the rwb-case case record contract mock does not answer within 2 seconds for case "RW-2027-000501"
    When "owner.user07" opens case "RW-2027-000501"
    Then the read is refused with 503 and nothing is stored
    Then no case row is written by this service

  Scenario: AC12 A policy row with no mode, threshold or floor stops the run (new, D-RCV-60)
    Given the approved INTAKE policy row for segment MORTGAGE and BKK carries no confidence floor
    When the agent run starts for case "RW-2027-000501"
    Then the run and the read stop and the missing value is named
    Then no code default is used

  Scenario: AC13 Business rules BR7 to BR13 hold (new, D-RCV-60)
    Given the approved INTAKE policy row for segment MORTGAGE and BKK is mode "L1"
    When the agent run completes for case "RW-2027-000501" and "owner.user07" sends a verdict
    Then the summary and the gap flags hold masking tokens only and no personal field leaves the service
    Then the L1 gate is resolved from the approved agent_policy row of rwb_agent only
    Then the decision record is written in the same transaction as the agent_feedback row and published on rwb.decision-record.v1
    Then the run facts and the L1 acceptance record leave on rwb.agent.events.v1 through the outbox
    Then the segment reference values and the lists are read through the rwb-case reference-data contract and a value outside the list is refused
    Then the case record is proposed to rwb-case and no case row is written by this service

  Scenario: AC14 The two operations answer 401 and 403 (new, D-RCV-60)
    Given a request without a valid session reaches GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs or POST /api/recovery/agent/v1/agent-runs/{runId}/feedback
    When the request reaches the service
    Then the platform guard refuses the request with 401
    Given a user the platform guard does not admit sends the same request
    Then the platform guard refuses the request with 403
```

**Target reading.** The agent "INTAKE", the policy version "P2", the prompt "PR3" and the agent version "INTAKE@P2/PR3", the mode L1 from 2027-01-25, the segment MORTGAGE and BKK, the cases "RW-2027-000501" to "RW-2027-000503", "RW-2027-000601" and "RW-2027-000701", the team "HP-NE", the segment UNSECURED, the gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL, the decision "D6", the item "SUMMARY", the month January 2027, the counts 300, 240, 45 and 15, the rates 0.8000 and 0.1500, the run status "TIMED_OUT", the dates 2027-01-26 and 2027-01-28, the message IDs MSG-P10-005, MSG-P7-005, MSG-P7-003, MSG-GEN-004, MSG-P4-003, MSG-P1-001 and MSG-P4-002, and the status codes 404, 409, 422 and 503 are the legacy values of RWB-E2-028, copied character for character; every scenario keeps its legacy title and every legacy Given, When and Then, and each carries the origin tag of its legacy criterion.

Eight scenarios gained one inserted first Given of the form `Given the <service> contract mock returns <x>`, because each reads a value that now belongs to another service, and nothing the service owns is mocked. AC1, AC3 and AC7 read the case facts, the owner and the team scope through the rwb-case case record contract of RWB-P3-E1035-CON. AC2 reads the recorded entries from rwb-decision and the rates from the monitor read of RWB-P10-E2031-APP, which is the story that serves SCR-46. AC5 reads the failure of the record write through the rwb-decision decision-record contract, which is the sealed side of the local library. AC6 reads the recorded entry back from rwb-decision. AC8 reads the segment value from the rwb-case reference-data contract of RWB-P3-E1043-CON. AC9 reads the business date from the rwb-source-data freshness read. AC4 crosses no service boundary — the reason check and the refusal happen before any write — and keeps its legacy lines unchanged.

The legacy values that the target holds as data are kept as data: the confidence floor, the segment threshold and the mode of the segment are columns of the approved `agent_policy` row, the lists are reference data of rwb-case, and the acceptance and correction rates are aggregates of the feedback rows per segment. The reporting job of Arch v5 slide 44, which AC2 reads after, is owned by rwb-reporting; this story neither schedules it nor changes it. DP-11 sits behind every consumed read (one hop, 2 s) and adds no dependency of its own.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only runs in mode L1 for the case segment are returned to a user; shadow output is never returned, and a segment whose policy row is SHADOW answers an empty list | agent_policy.autonomy_mode, segment_product_group, segment_region_code (DF-AGT-008 to DF-AGT-010); legacy BR1 |
| BR2 | Agent output is marked "Agent output" with the agent name and version | REQ-DRI-001; labels "Agent version"; legacy BR2 |
| BR3 | A verdict writes one decision record before the feedback is stored: decision "D6", agent version, the run as the inputs snapshot, the recommendation, the final call, the reason and the owner | Principle 5; R-UNI-39; CTL-06; DP-03; legacy BR3 |
| BR4 | A correction or a rejection needs a reason, at most 1 000 characters | CTL-07; MSG-P7-005; legacy BR4 |
| BR5 | One feedback per run and item; the intake summary is item "SUMMARY" | agent_feedback unique key (DF-AGT-098, DF-AGT-099); legacy BR5 |
| BR6 | The case record never waits for the model; the panel reads stored output | NFR-009; R-UNI-32; legacy BR6 |
| BR7 | The summary and the gap flags hold masking tokens only, and no personal field leaves the service in the model call, the event or the log | CTL-11; REQ-ACA-005; legacy BR7 |
| BR8 | The L1 gate of a case is resolved from the approved `agent_policy` row of `rwb_agent` only, against the product group and region the rwb-case contract serves; no other service decides the mode and no mode literal appears in the source | DP-01; DP-07; DF-AGT-008 to DF-AGT-011 |
| BR9 | Each verdict writes the record through the local decision-record library in the same transaction as the `agent_feedback` row and publishes it on `rwb.decision-record.v1`; rwb-decision seals it into `decision_log_entry`, which it owns | DP-03; ADR-022; R-UNI-39 |
| BR10 | The run facts and the L1 acceptance record are CloudEvents 1.0 messages on `rwb.agent.events.v1`, keyed by the case ID, inserted in the outbox in the same transaction as the state change, validated against their registry subject before the relay and routed to the `.dlt` topic on a refusal | DP-09; §R7.2 s17 |
| BR11 | The segment reference values and the seven lists are read at run time through the rwb-case reference-data contract with their version; a value outside the list in force is refused and never defaulted | DP-07 |
| BR12 | `agent_feedback` is the one table this story creates, by `V10_008__agent_feedback.sql` in the rwb-agent Flyway sequence of `rwb_agent`, with unique (agent_run_id, item_key) and the verdict check; no migration of this service touches another schema | DP-15; Ownership Map (agent_feedback owner P10) |
| BR13 | The case facts, the owner and the team scope come from the rwb-case case record contract, and the verdict is proposed to it; rwb-agent writes no case row and holds no foreign key across a schema | DP-01; C RWB-P3-E1035-CON |

### 9. State transitions

No case state transition is made by this story. The case owner's verdict is an observation on an agent output: it is stored in `agent_feedback` and proposed to the case record, and it changes no case status, no task, no queue and no clock (BR13). A corrected or a rejected summary changes the record of the decision, never the case.

The state of one intake run of the L1 segment:

| From | Event | Condition | To |
|---|---|---|---|
| None | EV-01 `rwb.case.CaseCreated.v1` is consumed, or the run is started for the case and event | No run exists for the same idempotency key | The run row is written and passes to ANSWERED when the answer passes its guardrail (agent_run.status, DF-AGT-046; LOV-AGENT-RUN) |
| None | EV-01 is consumed | A run exists for the same case and event ID | No second run; the stored run is returned and the repeat is counted (R-UNI-40) |
| None | The run is started | The approved policy row of the segment is mode SHADOW | The run is stored in SHADOW and no output is served |
| None | The run is started | The answer fails a guardrail check | GUARDRAIL_FAILED with fallback true and the check code in guardrail_result (DF-AGT-048) |
| None | The run is started | The model does not answer inside the 60-second policy budget | TIMED_OUT with fallback true, counted, not retried for that event (AC3) |

The state of one item of an L1 output and of its feedback row:

| From | Event | Condition | To |
|---|---|---|---|
| Open | The panel loads | The run is mode L1 and the segment is eligible | Shown with the marker "Agent output" |
| Open | The panel loads | The stored `data_as_of` is older than the business date | Shown with MSG-P1-001 and the data date |
| Open | The owner accepts, corrects or rejects with a reason | The record is written | `agent_feedback` ACCEPTED, CORRECTED or REJECTED with the entry ID, and the verdict on the panel |
| Open | The owner corrects or rejects without a reason | The reason is empty or longer than 1 000 characters | No write; 422 MSG-P7-005 |
| Open | The owner sends a verdict | The record cannot be written | No write; 503 MSG-P7-003; incident under R-UNI-39 |
| Recorded | A second verdict for the same run and item arrives | The unique key or the `If-Match` version refuses | 409 MSG-GEN-004; one record and one feedback row remain |
| Recorded | Nothing | None | Recorded; the panel shows the verdict and its date and hides the controls |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads the panel for cases in scope (Case record R); gives feedback (Case record U) |
| RW-TEAMMGR | Reads the panel for team cases (Case record R); no feedback |
| SY-AGENT | Runs the agent (read only) |
| SY-DECLOG, the local decision-record library | Writes the record and publishes it on `rwb.decision-record.v1` |
| RW-COE | Reads the acceptance of SCR-46 (Platform administration R) and loads the policy version (Rules and parameters C) |
| RW-RISK | Approves the policy version (Rules and parameters A) |
| rwb-agent service identity (the rwb-agent login, DP-02) | Resolves the mode, serves the two operations, writes `agent_feedback`, the record and the outbox rows, and reads the case record, the reference data, the entry and the business date through their owners' contracts |
| rwb-case (P3) | Owns the case of record, the owner and team scope, the case-decision proposal and the reference data |
| rwb-decision (P7) | Owns `decision_log_entry`, the central ledger and the sealing of a record |
| rwb-source-data (P1) | Owns the ACE view contract and the freshness read that answers the business date |
| No role | Reads `rwb_case`, `rwb_decision`, `rwb_source_data` or any other service's schema as a table, changes a case status, a task, a queue or a clock from a summary, or reads production data |

The login of the service is Not specified in the source documents (GAP-0622; ASM-0916); the story names it "the rwb-agent login (DP-02)" until it is agreed. Every role in the table above acts with the permission letter shown against it, and the service enforces each right and the case scope on the server through the rwb-access authorise contract (DP-08) and the guard library, so the refusals MSG-P4-002 and MSG-P4-003 are proved by TC-E2-028-10 and by the case record contract.

### 11. Data

| BR Field ID | Entity (owner schema) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3 `rwb_case`) | id | Read through the rwb-case case record contract |
| DF-CAS-003 | recovery_case (P3 `rwb_case`) | product_group | Read through the rwb-case case record contract (segment) |
| DF-CAS-009 | recovery_case (P3 `rwb_case`) | owner_user_id | Read through the rwb-case case record contract |
| DF-CAS-011 | recovery_case (P3 `rwb_case`) | team_code | Read through the rwb-case case record contract (scope) |
| DF-CAS-012 | recovery_case (P3 `rwb_case`) | region_code | Read through the rwb-case case record contract (segment) |
| DF-WRK-012 | assignment (P3 `rwb_case`) | assignee_user_id | Read through the rwb-case case record contract (owner check) |
| DF-DOC-004 | document (P5 `rwb_document`) | document_type | Read through the P5 read inside the run path (gap reasons) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7 `rwb_decision`) | all fields | Write through the local decision-record library, sealed by rwb-decision; read back through its entry read |
| DF-REF-001 to DF-REF-012 | reference_row, reference_version (P3 `rwb_case`) | the seven lists | Read through the rwb-case reference-data contract |
| DF-AGT-001 to DF-AGT-025 | agent_policy (P10 `rwb_agent`) | the approved row "INTAKE" version "P2": autonomy_mode, segment_product_group, segment_region_code, confidence_floor, timeout_seconds, output_schema_ref, allowed_tools | Read as the approved version; no column added here |
| DF-AGT-026 to DF-AGT-035 | agent_prompt (P10 `rwb_agent`) | the approved prompt version "PR3" and its body hash | Read |
| DF-AGT-036 | agent_run (P10 `rwb_agent`) | id | Read |
| DF-AGT-037 | agent_run (P10 `rwb_agent`) | agent_code | Read |
| DF-AGT-038 | agent_run (P10 `rwb_agent`) | agent_version | Read |
| DF-AGT-043 | agent_run (P10 `rwb_agent`) | autonomy_mode | Read |
| DF-AGT-046 | agent_run (P10 `rwb_agent`) | status | Read |
| DF-AGT-047 | agent_run (P10 `rwb_agent`) | fallback | Read |
| DF-AGT-049 | agent_run (P10 `rwb_agent`) | output | Read (the summary and the gap flags) |
| DF-AGT-050 | agent_run (P10 `rwb_agent`) | confidence | Read |
| DF-AGT-055 | agent_run (P10 `rwb_agent`) | data_as_of | Read |
| DF-AGT-056 | agent_run (P10 `rwb_agent`) | run_at | Read |
| DF-AGT-059 | agent_run (P10 `rwb_agent`) | segment_product_group | Read (the segment of the run) |
| DF-AGT-060 | agent_run (P10 `rwb_agent`) | segment_region_code | Read (the segment of the run) |
| DF-AGT-097 | agent_feedback (P10 `rwb_agent`) | id | Write |
| DF-AGT-098 | agent_feedback (P10 `rwb_agent`) | agent_run_id | Write |
| DF-AGT-099 | agent_feedback (P10 `rwb_agent`) | item_key | Write |
| DF-AGT-100 | agent_feedback (P10 `rwb_agent`) | verdict | Write |
| DF-AGT-101 | agent_feedback (P10 `rwb_agent`) | reason | Write |
| DF-AGT-102 | agent_feedback (P10 `rwb_agent`) | decision_log_id | Write |
| Standard column | agent_feedback (P10 `rwb_agent`) | created_by, created_at, version | Write |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E2-028. `recovery_case` and `assignment` belong to P3, `document` to P5, `decision_log_entry` to P7, `reference_row` and `reference_version` to P3, and each is read or written through its owner's contract and never as a table (DP-01, DP-07, DP-03). `agent_policy`, `agent_prompt` and `agent_run` are the P10 tables of schema `rwb_agent` in the Ownership Map and are read here; `agent_feedback` is the one table this story creates. The policy write is the configuration operation of RWB-P10-E1061-CON and is not a write of this story.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). Both operations are the E3 operations of TSD P10 Agent runtime v2 T-A.1 (API-P10-010 and API-P10-011) and their full shape, members and error taxonomy are fixed by RWB-P10-E2028-CON; this story supplies their behaviour.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/agent-outputs` | Read the L1 agent outputs of a case for the panel "Agent summary": `AgentOutput[]` with runId, agent, agentVersion, mode "L1", status, summary, gaps[{gapType, reason}], confidence, dataAsOf and feedback; an empty array when no L1 output exists for the case or the segment is in shadow; errors 401, 403 (MSG-P4-002), 404 (MSG-P4-003), 503 | Case record R, scope applied | Not applicable: the call writes nothing |
| POST | `/agent-runs/{runId}/feedback` | Record the owner's verdict on the summary item: AgentFeedbackRequest with itemKey (default "SUMMARY"), verdict ACCEPTED, CORRECTED or REJECTED, reason required for CORRECTED and REJECTED at most 1 000 characters, and the `If-Match` header with the run row version; 200 AgentOutput with the feedback set; errors 401, 403, 404, 409 (MSG-GEN-004), 422 (MSG-P7-005), 503 (MSG-P7-003) | Case record U, scope applied | Idempotency-Key header; one feedback per run and item key; a repeat returns 409 |

Errors: 401 no session (message ID Not specified in the source documents (CG-ALL-2679)), 403 no Case record right (MSG-P4-002), 404 an unknown case, run or out-of-scope case (MSG-P4-003), 409 a second verdict or a stale row version (MSG-GEN-004), 422 an empty or over-long reason (MSG-P7-005), 422 a verdict outside LOV-FEEDBACK (message ID Not specified in the source documents (GAP-0622); fixed by RWB-P10-E2028-CON), 503 the store, the decision-record library or a consumed contract unavailable (MSG-P7-003). The configuration operations and the L1 proposal payload belong to RWB-P10-E1061-CON and the metric read belongs to RWB-P10-E2031-APP; neither is re-declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E1035-CON) | AC1, AC3, AC7: the case facts, the owner and the team scope - product group MORTGAGE, region BKK, owner "owner.user07", team "HP-NE" outside the scope, and the case status | One hop, 2 s |
| POST | the case-decision proposal operation of rwb-case (RWB-P3-E1035-CON): the path is Not specified in the source documents (GAP-0623) | P3 rwb-case (RWB-P3-E1035-CON) | AC1, AC2: the owner's verdict proposed to the case record, so SCR-03 shows the recorded verdict and its date while rwb-case owns the case row | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | AC2, AC8: LOV-PRODUCT (with segment UNSECURED), LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION (with "D6"), LOV-AGENT and LOV-AGENT-RUN, read before an answer is checked or a verdict stored | One hop, 2 s |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision (RWB-P7-E1027-CON) | AC2, AC6: the sealed entry of a verdict, so `agent_feedback.decision_log_id` names the central entry and the monitor counts one entry per feedback | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/freshness` | P1 rwb-source-data | AC9: the business date of the ACE load, compared with `agent_run.data_as_of`; the read is the `GET /freshness` of Arch v5 slide 15 on the service base (GAP-0622; ASM-0918) | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (the one-hop rule behind every consumed read); rwb-agent calls no service through another service and holds no schema client of another service. The seven lists are P3's and are read through its reference-data contract (DP-07); the case is P3's and is read and proposed to through its case record contract; the entry is P7's; the business date is P1's. The decision record itself is not a REST call of this story: it is written by the local library of DP-03 and sealed by rwb-decision. The append request and answer of a record, the page and entry field sets of the two decision-log reads, the LOV-DECISION values beyond "D6", the reason-code list, the text of MSG-P7-009 and the rwb-decision login name are fixed by RWB-P10-E2028-CON and RWB-P7-E1027-CON at their wave 2 contract review, and this story builds and tests against the assumed values recorded for this key until then (GAP-1294).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | agent, caseid, fallback, outcome, runid |
| `rwb.agent.AgentFeedbackRecorded.v1` | `rwb.agent.events.v1` | P10 | the case ID | run ID, case_id, item_key "SUMMARY", verdict, agent_version, decision entry ID, recorded_at |
| DecisionRecorded, the decision-record type of the library | `rwb.decision-record.v1`, the shared decision-record topic, with its retry and `.dlt` rule (DP-03; the type name on the topic is fixed by ASM-0922) | P7 rwb-decision owns the central ledger; the library of RWB-PLT-E1027-CON owns the envelope | the case ID | the record of a verdict: the case ID, decision "D6", agent version "INTAKE@P2/PR3", the model version, the run reference as the inputs snapshot, the recommendation, the final call, the reason, the owner and the entry ID |

All three are inserted in the outbox in the same transaction as the row they describe and relayed by the outbox library: the agent events on `rwb.agent.events.v1`, , and the decision record on `rwb.decision-record.v1` with its retry and `.dlt` rule; a payload is validated against its registry subject before the relay and a refusal is routed to the `.dlt` topic of its topic with an alert (DP-09; BR10). No personal data is carried: no name, no national ID number, no account number and no document text (section 17). `AgentRunCompleted` is EV-28 of Arch v5 slide 43; `AgentFeedbackRecorded` is added on the same topic by the contract of this key under the naming rule of §R4, because the catalogue names only the completion event (GAP-0623).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use | Rule |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | AC1, AC3, AC8: a new case starts one intake run in the mode of its segment | Dedupe on the event ID in the inbox; one run per case and event (R-UNI-40) |

No other topic is consumed. The case facts, the lists, the entry and the business date are read through their owners' REST contracts, and the policy, the prompt and the run are rows of `rwb_agent` (Arch v5 slides 13 and 16).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, one execution per case and triggering event, workflow ID = the case ID and the event ID (of the run path of this service, restated here) | `rwb-agent` | Input: agent code "INTAKE", case ID, trigger event "CaseCreated", event ID, idempotency key and the resolved autonomy mode. One execution per idempotency key, the 60-second policy budget, then the rule result (R-UNI-32) |
| ResolveIntakeMode | Activity, added by this story | `rwb-agent` | Input: the case ID and the approved policy row of agent "INTAKE". Output: mode L1 or SHADOW, the policy version, the segment it matched and the confidence floor, or the refusal of X10 (DP-01, DP-07) |
| RecordIntakeFeedback | Activity (workflow kit, one transaction) | `rwb-agent` | Input: the verdict, the reason, the run row version and the proposal of the case record. Output: the decision record, the `agent_feedback` row and the outbox row, or no write at all (DP-03, DP-09) |

The workflow name, the queue and the 60-second budget are those of Arch v5 slide 16 ("AgentRunWorkflow: 60 s, then rule result"); the two activity names are this story's and are accepted by RWB-P10-E2028-CON. The read and the verdict are synchronous inside the request and add no workflow.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the intake run is event-started from EV-01 `rwb.case.CaseCreated.v1` and never on a cadence, and a verdict comes from a person (DP-10; BR8). The legacy Quartz entry of the intake job is retired with the stage, and no job table is read or written here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_feedback | P10 (`rwb_agent`) | One verdict per run and item key, with its reason and the entry ID; created by `V10_008__agent_feedback.sql` with unique (agent_run_id, item_key) and the verdict check |
| agent_policy | P10 (`rwb_agent`) | The approved row "INTAKE" version "P2" with its mode, its segment, its segment threshold and its confidence floor; read here, written through the configuration operation of RWB-P10-E1061-CON; no column added |
| agent_run | P10 (`rwb_agent`) | The intake run, its status, its fallback, its summary, its gap flags, its `data_as_of` and its segment; read here; no column added |
| agent_prompt | P10 (`rwb_agent`) | The approved prompt version "PR3"; read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope (DP-09) |

rwb-agent reads no table of another service and holds no foreign key across services (DP-01). `recovery_case` and `assignment` are P3's, `document` is P5's, `decision_log_entry` is P7's and `reference_row` and `reference_version` are P3's, and each is reached through its owner's contract. `V10_008__agent_feedback.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The case record contract of RWB-P3-E1035-CON and the reference-data contract of RWB-P3-E1043-CON | Cases "RW-2027-000501" to "RW-2027-000503" in the scope of "owner.user07" with product group MORTGAGE and region BKK; case "RW-2027-000601" in team "HP-NE" outside the scope; case "RW-2027-000701" with segment UNSECURED; the case-decision proposal with its accepted answer; LOV-PRODUCT, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION, LOV-AGENT and LOV-AGENT-RUN; a case that does not exist and an answer beyond 2 s |
| rwb-decision WireMock and decision-record stub | The entry read of RWB-P7-E1027-CON and the record side of the library of RWB-PLT-E1027-CON | One sealed entry per feedback with decision "D6" and agent version "INTAKE@P2/PR3"; a failed record write for AC5; a duplicate entry answer for AC6; a `.dlt` route on a permanent relay failure |
| rwb-source-data WireMock | The freshness read of Arch v5 slide 15 | Business date 2027-01-28 over the ACE load of 2027-01-26 for AC9; a fresh business date equal to `data_as_of`; a failed freshness answer for X11; an answer beyond 2 s |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the two operations, one hop, with the query, the `If-Match` header and the media type preserved, and the 403, 404 and 409 passed through unchanged |

The inbox and outbox stubs, the access guard stub, the model gateway stub and the workflow kit stub are the platform's and are used but not declared here. Every fixture is synthetic; no production case, summary, party record or document is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The agent-outputs read and the feedback operation provided on `/api/recovery/agent/v1`; the case read, the case-decision proposal, the lists, the entry read and the freshness read consumed, one hop and 2 s each |
| Kafka | 3 published, 1 consumed | `AgentRunCompleted`, `AgentFeedbackRecorded` and the decision record published; `CaseCreated` consumed |
| Temporal | 1 workflow, 2 activities | AgentRunWorkflow with ResolveIntakeMode and RecordIntakeFeedback on the queue `rwb-agent`, started by the event |
| File | None | No file is read or written; the policy and the prompt are rows of `rwb_agent` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.intake`, module `intake`, inside the rwb-agent service; the panel component lives with the SCR-03 Case record composition and is reached through the gateway-bff route.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are the ones in the metadata rows: the six platform contract stories and RWB-P10-E2028-CON are build dependencies, RWB-P10-E2031-APP and RWB-P10-E1061-CON are the same-lane and same-service contracts this story waits for, and RWB-P3-E1043-CON, RWB-P3-E1035-CON and RWB-P7-E1027-CON are contract dependencies built against their fakes. DP-01 (the service's own schema) and DP-02 (one login per service) hold behind all of them and add no dependency; DP-11 sits behind every consumed read (one hop, 2 s) and adds none of its own. DP-10 adds the workflow kit and registers no Schedule, because the run is event-started.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntakeEventStartedRun | Listener | Consumes EV-01 through the inbox, dedupes on the event ID and starts one AgentRunWorkflow execution per case and event (AC1, AC3) |
| IntakeModeResolver | Service and activity | Applies BR8: the mode, the segment match, the segment threshold and the confidence floor come from the approved `agent_policy` row and the case facts of the rwb-case contract (AC8; X10) |
| IntakeOutputQueryService | Service | Serves the read from `agent_run` and `agent_feedback` in `rwb_agent`: L1 only, an empty list for a shadow segment, the stale marker from `data_as_of` against the freshness read (AC1, AC7, AC8, AC9) |
| IntakeOutputController | Controller | The two operations on `/api/recovery/agent/v1`, with the 200 answers and the refusal codes of section 12.1 (DP-13) |
| IntakeFeedbackService | Service | Validates the verdict and the reason, checks the one-feedback-per-item rule and the row version, and calls the record writer before any store (AC4, AC6) |
| DecisionRecordWriter | Client of the platform library | Applies BR3 and BR9: inserts the record and the outbox row in the same transaction as the feedback and reads the sealed entry ID back (AC5) |
| IntakeCaseProposalClient | Client | Proposes the verdict to rwb-case through the case record contract, one hop and 2 s (BR13) |
| CaseFactReader, ReferenceDataReader, FreshnessReader, EntryReader | Clients | The case facts, the seven lists, the business date and the entry read, one hop and 2 s each (DP-07) |
| AgentSummaryPanel | React component | The panel on SCR-03: the marker, the version, the gap flags with reasons, the controls, the stale warning and the recorded state |
| AgentFeedbackRepository | Repository | Writes and reads `agent_feedback` and reads `agent_run`, `agent_policy` and `agent_prompt` in `rwb_agent` only (BR12) |
| IntakeEventPublisher | Library adapter | Inserts the completion and acceptance events in the outbox in the run's and the verdict's transaction and maps a registry refusal to the `.dlt` route (DP-09) |

**Database and migrations**

- `V10_008__agent_feedback.sql` creates `agent_feedback` (id, agent_run_id, item_key varchar(20), verdict varchar(10), reason varchar(1000), created_by uuid, created_at timestamptz, decision_log_id uuid and the standard record columns) with unique (agent_run_id, item_key) and the check verdict in ('ACCEPTED','CORRECTED','REJECTED'), runs in the rwb-agent Flyway sequence after `V10_001` and the P10 migrations of the earlier stories, and touches no other schema (DP-15; BR12; GAP-0622; ASM-0921).
- One index serves the read and the repeat check: `ix_agent_feedback_run_item ON agent_feedback (agent_run_id, item_key)`.
- No table is created outside `rwb_agent`, and no foreign key crosses a service (DP-01).

**Configuration and reference data**

- Policy "INTAKE" version "P2": mode L1 for segment MORTGAGE and BKK, mode SHADOW elsewhere, the segment threshold, the confidence floor, the 60-second timeout, the allowed tools, output schema "intake-v1" and prompt version "PR3"; loaded by RW-COE and approved by RW-RISK through the operations of RWB-P10-E1061-CON, in force from 2027-01-25, and every one of those values is a column of the approved row and never a value of this story (GAP-0622; ASM-0929).
- The seven lists in force in rwb-case, read through its reference-data contract (DP-07). The list codes are service configuration; the list values are its owner's data.
- The `decision_code` of the record is the LOV-DECISION value "D6" of the legacy story, read as data and never written in the source (GAP-0622; ASM-0917).
- The legacy feature flag `rwb.agent.intake-l1` is kept as a legacy reference and held as a data row of the platform feature-flag library: off, the read answers an empty list and the panel is hidden (§R3 default ruling: feature flags to the platform library; BR12).
- The 2 s client budget, the run-key format and the item key default "SUMMARY" as service configuration.

**Build steps**

1. Flyway migration `V10_008__agent_feedback.sql` and its unique key and index in `rwb_agent` (BR12).
2. The five contract clients against their fakes, with the one-hop budget and the refusal mapping (X9).
3. IntakeModeResolver over the approved policy row and the case facts, with the shadow path, the missing-value path and the segment threshold (AC8; X10).
4. IntakeOutputQueryService: L1 only, the empty answer, the stale marker and the missing feedback (AC1, AC3, AC7, AC8, AC9).
5. IntakeOutputController and the two operations on `/api/recovery/agent/v1` against the contract of RWB-P10-E2028-CON (DP-13).
6. IntakeFeedbackService with the reason rule, the row version and the second-verdict refusal (AC4, AC6).
7. DecisionRecordWriter and the one-transaction path of the record, the feedback and the outbox, with the failure of AC5 (BR3, BR9).
8. IntakeCaseProposalClient and the recorded verdict on the case record (BR13).
9. AgentSummaryPanel with its five states and the gateway-bff route in front of the two operations (DP-19).
10. Pipeline scans for a mode, segment, threshold, floor or list literal in the source, for a case table name, for a cross-schema foreign key and for a personal field in a payload (section 17).

**Done when.** The eleven test cases of section 16 pass, the two operations answer on `/api/recovery/agent/v1`, a DEV run over the synthetic cases shows the summary and the gap flags for the L1 segment and an empty answer for a shadow segment, each verdict writes one record, one feedback row and one acceptance event, the refusals answer 404, 409, 422 and 503 with their messages, the migration applies cleanly on an empty `rwb_agent` schema, and no business value appears in the source.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-005 | No L1 summary for the case because the run failed | The agent summary is not available for this case. Work from the case record. |
| MSG-P7-005 | Correct or Reject with no reason, or a reason longer than 1 000 characters | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Feedback already given or the row changed | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | The case is outside scope or unknown | This case is not in your scope. |
| MSG-P1-001 | The summary was built on stale data | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

The seven texts are copied unchanged from RWB-E2-028 and this story adds no message ID. In AC9 the {date} is 2027-01-26 and the {product} is the ACE data product the freshness read names. In the access test the {action} value is "give feedback on an agent summary". In AC3 no message reaches a user beyond the panel text of MSG-P10-005, and in AC8 no message is shown at all.

### 15. Screens and states

SCR-03 Case record keeps its states loading, read only, editable and on hold and gains the panel "Agent summary". Panel states: loading (skeleton), empty (no panel when no L1 output exists for the case or the segment is in shadow), unavailable (MSG-P10-005 when the run failed), stale (MSG-P1-001 with the data date above the summary), ready (summary, gap flags with reasons, marker "Agent output", the version "INTAKE@P2/PR3", Accept, Correct, Reject) and recorded (the verdict and its date, no controls). In the read only state of SCR-03 the controls are hidden. The page states of SCR-03 empty, error and no access are Not specified in the source documents (CG-ALL-2689).

In the target the panel is composed by the gateway-bff route and reads `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs`; the verdict is sent to `POST /api/recovery/agent/v1/agent-runs/{runId}/feedback`. No screen calls rwb-agent directly (DP-19). The path of the gateway-bff route in front of the two operations is Not specified in the source documents (GAP-0623; ASM-0923), and the route passes the read, the `If-Match` header and the refusals through unchanged. SCR-46 Agent monitor is the screen of RWB-P10-E2031-APP and shows the acceptance and correction rates of "INTAKE" for MORTGAGE and BKK; it is not changed here. The states of SCR-46 empty, loading, error and no access are Not specified in the source documents (CG-ALL-2690).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-028-10 | AC10, Access | Contract | RW-PHONECOL (Case record R only) sends feedback; refused with MSG-P4-002 |
| TC-E2-028-01 | AC1, BR1, BR2, BR6 | Component | Case RW-2027-000501 with an ANSWERED run and two gaps |
| TC-E2-028-02 | AC2, BR3 | Component | January 2027, MORTGAGE/BKK: 300 feedback, 240, 45, 15 |
| TC-E2-028-03 | AC3, BR6 | Component | Case RW-2027-000502 with a TIMED_OUT run |
| TC-E2-028-04 | AC4, BR4 | Component | Correct with an empty reason |
| TC-E2-028-05 | AC5, BR3 | Component | Decision record writer fails on Accept |
| TC-E2-028-06 | AC6, BR5 | Component | Second feedback on the same run |
| TC-E2-028-07 | AC7 | Component | Case RW-2027-000601 in team HP-NE |
| TC-E2-028-08 | AC8, BR1 | Component | Unsecured case RW-2027-000701, segment in SHADOW |
| TC-E2-028-09 | AC9 | Component | Data as of 2027-01-26, business date 2027-01-28 |
| TC-E2-028-11 | Principle 5 | NFR | Decision record write forced to fail on feedback; no feedback stored; MSG-P7-003 |
| TC-E2-028-12 | Tables owned (section 12.7, ASM-3438) | Contract | Writes to agent_feedback, outbox_event, processed_event and idempotency_key only; a write to agent_policy, agent_run or agent_prompt is refused |
| TC-E2-028-13 | AC11, X9 | Component | Case RW-2027-000501; rwb-case read does not answer within 2 s; 503 and nothing stored |
| TC-E2-028-14 | AC12, X10 | Component | MORTGAGE/BKK INTAKE policy row with no confidence floor |
| TC-E2-028-15 | BR7 | Component | Summary and gap flags of case RW-2027-000501; masking tokens only |
| TC-E2-028-16 | BR8 | Component | Approved agent_policy row of INTAKE for MORTGAGE/BKK at mode L1 |
| TC-E2-028-17 | BR9 | Component | Verdict on the run of case RW-2027-000501; record and agent_feedback written in one transaction |
| TC-E2-028-18 | BR10 | Contract | AgentRunCompleted and the L1 acceptance record on rwb.agent.events.v1; refused payload routed to .dlt |
| TC-E2-028-19 | BR11 | Contract | Segment reference value outside the list in force; refused, not defaulted |
| TC-E2-028-20 | BR12 | Component | Second feedback on the same run and item SUMMARY; unique key holds |
| TC-E2-028-21 | BR13 | Component | Verdict proposed to rwb-case; no row written in the case schema |
| TC-E2-028-22 | AC13, BR7, BR8, BR9, BR10, BR11, BR12, BR13 | Component | Data as TC-E2-028-15 to TC-E2-028-21 |
| TC-E2-028-23 | AC14 | Contract | A request without a valid session refused with 401; a user the guard does not admit refused with 403 |

TC-E2-028-10 is placed first and TC-E2-028-11 follows the other nine legacy cases in their legacy order, as the split record of this key lists them; TC-E2-028-12 to TC-E2-028-23 are not legacy. All eleven are the legacy test cases of RWB-E2-028, kept with their legacy IDs and their legacy data: the legacy System level maps to Component, because the in-process call it tested is now a contract read with a fake; the legacy Access level maps to Contract, because the refusal is answered by the platform guard at the edge of the service and asserted on the contract answer; and the legacy Resilience level of TC-E2-028-11 maps to NFR, because the failure of the decision-record write is held to the R-UNI-39 rule and the platform envelope. No `-ITG` copy is added: the integration dependency row is None, so the cross-service behaviour of this key — the case facts served by rwb-case, the proposal on the case record, the freshness date and the sealed entry — is proved by the wave 2 integration story of the key, RWB-ITG-W2, and not here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. TC-E2-028-12 to TC-E2-028-23 are not yet in that workbook.

### 17. Guardrails

- No business value in code: the mode, the segment, the segment threshold, the confidence floor, the seven lists, the decision code "D6" and the item key are policy, reference and configuration values read at run time, and a missing value stops the read or the run instead of falling back to a default (BR1, BR8, BR11).
- No personal data in logs, tests, prompts, events or workflow inputs: the summary and the gap flags hold masking tokens, the model call carries masked values only, the events carry identifiers and facts only, and no prompt or log carries a national ID number, a name or an account number (BR7, BR10; REQ-ACA-005).
- No read of another service's tables and no schema client: the case, the owner and the team scope through rwb-case, the lists through rwb-case, the entry through rwb-decision and the business date through rwb-source-data (DP-01, DP-07).
- `agent_feedback` is the only table this story creates, by `V10_008__agent_feedback.sql` in the rwb-agent Flyway sequence; `agent_policy`, `agent_run` and `agent_prompt` are read and never written here (BR12, DP-15).
- A summary changes nothing in force: no case status, no task, no queue and no clock is set from it, and the verdict is proposed to rwb-case and stored as a record and a feedback row only (BR13).
- ACE data is reached only through its owner's contract or the service's own `v_ace_*` view; this story reads no ACE table and names none.
- One hop and a 2 s client budget on every consumed REST call; the 60-second model budget belongs to the agent platform and is never a REST budget of this story.
- Every event is a CloudEvents 1.0 message on the owner's topic, keyed by the case, validated against its registry subject before the relay and routed to `.dlt` on a refusal (DP-09).
- One feedback per run and item, with the row version on the request, so a second owner never overwrites a verdict (BR5).
- Every fixture is synthetic; no production case, summary, account or party record is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32, R-UNI-39 | TC-E2-028-01, TC-E2-028-02, TC-E2-028-03, TC-E2-028-04, TC-E2-028-05, TC-E2-028-06, TC-E2-028-09, TC-E2-028-11 |
| REQ-ACA-005 | Personal data masked by role on every screen and every agent call | Business Requirements Program, section 5.4 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-01, TC-E2-028-07, TC-E2-028-08, TC-E2-028-10 |
| D-RCV-60 DP-03 | Decision record written locally and sealed centrally | Template and Rules §R5.5; ADR-022 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-39 | TC-E2-028-02, TC-E2-028-05, TC-E2-028-11, TC-P10-E2028-CON-04 |
| D-RCV-60 DP-07 | The segment values and the lists are read from the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-08, TC-P10-E2028-CON-03 |
| D-RCV-60 DP-09 | The run facts and the acceptance record leave through the outbox as CloudEvents | Template and Rules §R5.5; ADR-015 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-02, TC-P10-E2028-CON-05 |
| D-RCV-60 DP-10 | The run is an event-started workflow with no cadence | Template and Rules §R5.5; ADR-016 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-01, TC-E2-028-03 |
| D-RCV-60 DP-13 | The two operations are served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-01, TC-E2-028-07, TC-P10-E2028-CON-01 |
| D-RCV-60 DP-15 | `agent_feedback` arrives with the service's own Flyway sequence | Template and Rules §R5.5; ADR-021 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-06, TC-P10-E2028-CON-01 |
| D-RCV-60 DP-19 | The panel is reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-10, TC-P10-E2028-CON-06 |
| R-UNI-32 | The agent is not waited on: after its budget the rule result is used | Business Requirements Program, section 5.5 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32 | TC-E2-028-03 |
| R-UNI-39 | The record, the state change and the event are one transaction | Business Requirements Program, section 5.5 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-39 | TC-E2-028-05, TC-E2-028-11 |
| RWB-E2-028 (legacy story) | Case intake agent live at L1 [E3a]: the nine criteria AC1 to AC9 and the two access and resilience tests | Business Requirements Epic 2 | FEAT-AGT-07 | 06 Take over and own the case | None | The eleven legacy test cases of section 16 |
| RWB-ITG-W2 (integration copy) | The same behaviour proved across rwb-case, rwb-decision, rwb-source-data and rwb-agent on the real services | Business Requirements Epic 2 | FEAT-AGT-07 | 06 Take over and own the case | None | The test cases of that story |

The gap GAP-0622 records the areas the sources leave open for this story — the service login, the decision code and the record field list, the business date of the stale check, the item key, the invalid-verdict refusal, the migration after `V10_008` and the policy row the gate reads — and each default it raises is settled by ASM-0916, ASM-0917, ASM-0918, ASM-0919, ASM-0920, ASM-0921 and ASM-0929. The seam the read and the verdict cross is fixed by the contract of this key, RWB-P10-E2028-CON, whose gap GAP-0623 carries the member types, the record event name, the name of the acceptance event, the path of the case-decision proposal and the route path; the cross-service proof is RWB-ITG-W2.

### 19. Out of scope

- The cross-service behaviour of this key and the harness: RWB-ITG-W2 and RWB-ITG-W1J01-ITG.
- The contract slice of this key as a published artefact with its fakes: RWB-P10-E2028-CON.
- The deployment of the capability — chart values, the migration job, the queue and namespace, the topic and its consumer groups, the dashboards, the alerts and the runbook: RWB-P10-E2028-OPS.
- The shadow run of the intake agent and the agent platform behind it: the earlier P10 stories of this service, and the platform baseline RWB-P10-E1058-CON.
- The L1 proposal payload and the configuration operations that load and approve policy version "P2": RWB-P10-E1061-CON.
- The monitor read and SCR-46: RWB-P10-E2031-APP, with SCR-46 itself belonging to RWB-E2-031.
- Agent actions taken without the owner (autonomy L2 and above, Epic 8).
- Editing the summary text in the Workbench; a correction records the reason only.
- Intake document classification and the document hub: P5 rwb-document.
- The right check and the refusals of MSG-P4-002 and MSG-P4-003 as a service deliverable: P4 rwb-access and P3 rwb-case; the platform guard applies them here.
- The case record composition, the case of record and the reference data themselves: P3 rwb-case.
- The central decision ledger, its hash chain and its sealing: P7 rwb-decision.
- The ACE view contract, the extension tables and the freshness read: P1 rwb-source-data.
