SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P10 rwb-agent
description: Product requirements for the Agent runtime service rwb-agent (P10) of the Recovery Workbench under D-RCV-60 - the agent runtime and model gateway, the guardrail checker and the rule fallback, the policy and prompt store, shadow running, evaluation and scoring, the monitoring dashboard with cost and drift alerts, autonomy governance, champion and challenger with committee review, feedback and override capture, and the TDR offer suggestion through the gateway.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx
version: 1
date: 22 November 2026
decision: D-RCV-60
service: P10 rwb-agent
service_epic: RWB-SVC-P10
wave: 1
---

# Recovery Workbench PRD P10 rwb-agent

**Change log.** D-RCV-60, 26 November 2026: cross-document changes under the programme directive. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## 1. Document control and change log

### 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P10 rwb-agent |
| Document ID | P10-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | rwb-agent (P10, Agent runtime, wave 1; business epics EP01 to EP08) |
| Service epic | RWB-SVC-P10 |
| Realignment decision | D-RCV-60 |
| Business baseline | Recovery Workbench Business Requirements Program v5 (22 November 2026), sections 5.3, 5.5, 5.7, 6.2, 6.3, 6.4, 6.6, 6.7, 6.8, 6.9, 6.12, 8 and 10 |
| Business baseline, epic detail | Recovery Workbench Business Requirements Epic 1 v5 (22 November 2026), section 3.9; Epic 2 v3, section 3.10; Epics 3 to 8 v1, sections 8.1 and 8.6 |
| Functional baseline | Recovery Workbench FSD P10 Agent runtime v3 (15 November 2026) |
| Architecture baseline | Recovery Workbench Architecture v5 Text Extract v1; Temporal and Drools Design Text Extract v1; Ownership Map v1; Story Template and Rules v1 |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Tool and model | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | PRD Builder, AI-SDLC playbook |

### 1.2 Trace metadata

| Item | Value |
|---|---|
| Run | D-RCV-60 microservice realignment, folder 22 |
| Work package | B-REQ-PRD-P10 |
| Upstream artifacts | BRD Program v5; BRD Epic 1 v5; BRD Epic 2 v3; BRD Epics 3 to 8 v1; FSD P10 Agent runtime v3; Arch v5 Text Extract v1; Temporal and Drools Design Text Extract v1; Ownership Map v1 (ASM-2639) |
| Upstream ID sets | REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-DCM-005, REQ-DCM-006, REQ-DCM-011, REQ-DRI-001, REQ-DRI-005, REQ-APD-005, REQ-ACA-005, REQ-ACA-010, REQ-CHO-006, REQ-DVH-001; BR-015, BR-081, BR-084; NFR-008, NFR-010, NFR-020, NFR-021, NFR-024, NFR-027, NFR-030, NFR-033, NFR-034, NFR-036, NFR-039, NFR-040, NFR-042, NFR-045, NFR-046, NFR-047, NFR-048, NFR-051, NFR-052, NFR-053, NFR-055, NFR-064, NFR-066, NFR-067, NFR-068; FEAT-AGT-01 to FEAT-AGT-16; RWB-E1-058, RWB-E1-059, RWB-E1-060, RWB-E1-061, RWB-E1-062, RWB-E1-063, RWB-E2-028, RWB-E2-029, RWB-E2-030, RWB-E2-031, RWB-E2-032, RWB-E3-030, RWB-E3-031, RWB-E8-003, RWB-E8-004, RWB-E8-005 |
| Generated ID sets | CAP-P10-001 to CAP-P10-011; FR-P10-001 to FR-P10-026; NFR-P10-001 to NFR-P10-017; AC-P10-001 to AC-P10-017; Q-P10-01 to Q-P10-08 |
| Source artifact | 03 Requirements and specifications/Recovery Workbench FSD P10 Agent runtime v3 (extract: _work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P10 Agent runtime v3.md) |
| Status | Draft; approval gate open |

### 1.3 Change log

| Version | Date | Change | Decision | Tool |
|---|---|---|---|---|
| 1 | 22 November 2026 | First version. The service PRD is derived from BRD Program v5 sections 5.3, 5.5, 5.7, 6 and 8, BRD Epic 1 v5 section 3.9, BRD Epic 2 v3 section 3.10, BRD Epics 3 to 8 v1 sections 8.1 and 8.6, and FSD P10 Agent runtime v3 under D-RCV-60. The module becomes the service rwb-agent with its own schema, login, REST base, topic and task queue, one published event and one workflow. AI stays isolated in this one service with a policy row that can switch it off, every answer passes the guardrail or falls back to the rule result within 60 seconds, the data lake dashboard feed is replaced by the service's own daily measures and the rwb-reporting read model, and autonomy changes are versioned rows with the approval each change needs. | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1.4 Requirement ID conventions

| Prefix | Meaning | Example |
|---|---|---|
| CAP-P10-nnn | Product capability of the service | CAP-P10-001 |
| FR-P10-nnn | Functional requirement; mapped to the FSD section and acceptance criteria it serves | FR-P10-001 |
| NFR-P10-nnn | Non-functional requirement; mapped to the BRD NFR IDs | NFR-P10-001 |
| AC-P10-nnn | Acceptance criterion in Gherkin, mapped to FR and NFR | AC-P10-001 |
| Q-P10-nn | Open question | Q-P10-01 |
| BR IDs | Business requirement IDs of the BRD, copied unchanged | REQ-CWC-018 |
| CG and ASM | Candidate gap and assumption rows of this work package, numbered later as GAP-nnnn and ASM-nnnn | GAP-1516 |

No BRD requirement is renumbered (ASM-2655). There is no predecessor PRD in this family, so this file is version 1 (ASM-2638). The FSD for P10 carries no requirement row of its own: its "Requirements served" table is empty, so the FSD column of the functional requirements names the FSD section and acceptance criteria instead of a requirement ID (GAP-1522; ASM-2643).

## 2. Product overview and relationship to ACE

### 2.1 What the service is

rwb-agent is the agent runtime of the Recovery Workbench. It runs an agent on a request, calls the approved model endpoint through the model gateway, tests the answer against the output schema, the allowed tools and the confidence floor, returns the answer or the rule result, and records what happened. It owns the policy and prompt versions, the runs, the guardrails, the evaluation samples, the scores, the feedback and the alerts, and it serves the agent monitor.

The product value is one property the business asked for and nothing else: an officer is never blocked by AI and never handed an AI answer nobody can explain. The FSD measure is unchanged: the agent fallback rate stays below 10 percent, read from the decision log and the Workbench records (FSD P10 v3 A2.1.1). The BOT AI risk guidelines of 12 September 2025 are the reason the capability sits in one service: an agent suggests, a person decides, the model and prompt versions are recorded, personal data is masked before it leaves, and after 60 seconds the rules decide (Arch v5 slide 35).

### 2.2 What is new under D-RCV-60

| New | Detail |
|---|---|
| One service, one boundary | The module becomes rwb-agent with schema `rwb_agent`, its own ACE database login, REST base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, task queue `rwb-agent` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.agent` (Arch v5 slide 41; Story Template and Rules R4) |
| One published event | `rwb.agent.AgentRunCompleted.v1`, key case ID, no numbered EV ID in the sources beyond EV-28 (Arch v5 slides 16, 43) |
| The run as a durable step | `AgentRunWorkflow` on queue `rwb-agent`: 60 seconds, then the rule result; bursts of uploads scale the worker to zero (Arch v5 slides 16, 33 and 34; ADR-016) |
| AI isolated and switchable | `agent_policy.autonomy_mode` is a versioned row with the values OFF, SHADOW and L1; OFF is the switch that removes the agent from the path without a code release (Arch v5 slides 35 and 36; FSD P10 v3 A2.6.3.2) |
| Ownership of eight tables | `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback` and `agent_alert`; the outbox, inbox, idempotency and local decision-record objects are platform library objects created in the service schema (Ownership Map, Tables sheet) |
| A read-only tool gateway | The agent reads case facts through the rwb-source-data tool and extracted document fields through the rwb-document tool; it writes nothing outside its own schema (Arch v5 slide 16; ASM-2645) |
| No data lake and no Power BI connection | The dashboard the FSD describes as a lake and Power BI feed becomes the service's own daily measures for screen SCR-46, and the read model in rwb-reporting (ADR-018; GAP-1516; ASM-2641) |

### 2.3 What is reused from ACE and from the platform

| Reused capability | Owner | Effect on this PRD |
|---|---|---|
| Sign-in, access check, audit and PII logging to SOC | ACE common module | No product requirement; every agent call under a service identity is written to the ACE PII log path (Arch v5 slide 35) |
| Notification path NSS and LINE OA | ACE common module | The cost and drift alerts to the risk and centre-of-excellence roles use the shared path; no P10 build (ASM-2650) |
| Role, scope and masking policy | P4 rwb-access | The agent passes the same role checks as a person, and the masking rule of the case is applied before personal data enters a prompt (REQ-ACA-010; NFR-039) |
| Case and subject facts, ACE read-only through thirty views | P1 rwb-source-data | Every ACE fact a run needs is one hop away through that contract; this service holds no grant on `recovery` (ASM-2644) |
| Extracted document fields and document identity | P5 rwb-document | The tool gateway reads the fields the hub extracted; the service stores no document and no OCR text |
| Decision record and central ledger | P7 rwb-decision | Each answer, suggestion and fallback is recorded locally and sealed through the shared decision-record topic (DP-03; ADR-022) |
| Deviation codes X1 to X7 and their owners | S8 rwb-deviation | The screening agent proposes codes with reasons; the deviation service decides (FR-P10-013) |
| Approval routing, delegation of authority | P7 rwb-decision, table owned by P4 | The approval of a policy or prompt version and of an autonomy step is a decision of the risk role, not a P10 approval engine (FR-P10-006, FR-P10-021) |
| Case, queue, task and route state | P3 rwb-case | A suggestion reaches a queue only through the rwb-case contract and only when the mode allows it (FR-P10-007) |
| Model endpoint, private network, observability, Kafka, Temporal, gateway route | Platform epics RWB-PLT, ACE platform | The service narrows the platform rules and redefines none of them |
| Report layout and measures delivery | P9 rwb-reporting | The daily per-agent measures are handed to the read model; the dashboard is served from both (FR-P10-016, FR-P10-017) |

### 2.4 Confirmed constraints from Architecture v5

| Constraint | Source |
|---|---|
| Schema `rwb_agent`; own login; no grant on `recovery` and no grant on another `rwb_*` schema | Arch v5 slides 29 and 41; ADR-014; DP-01, DP-02, DP-05 |
| REST base `/api/recovery/agent/v1` behind gateway-bff; one hop, 2 s timeout | Arch v5 slides 8, 11 and 41; ADR-020; DP-11, DP-13 |
| Topic `rwb.agent.events.v1` with retry topics and `.dlt`; CloudEvents 1.0; outbox and inbox | Arch v5 slides 9, 11, 41 and 43; ADR-015; DP-09, DP-14 |
| Task queue `rwb-agent`; `AgentRunWorkflow`; 60 s then the rule result; no Temporal Schedule of this service in wave 1 | Arch v5 slides 16 and 44; ADR-016; DP-10 |
| Model endpoint: approved Enterprise AI endpoint on a private endpoint inside the SCB tenant | Arch v5 slides 16 and 35; NFR-048 |
| Kafka consumers: `CaseCreated` (EV-01) and `DocumentStored` (EV-16); producer of `AgentRunCompleted` (EV-28) | Arch v5 slides 42 and 43 |
| No data lake and no Power BI connection | Arch v5 slides 7, 8, 13 and 37; ADR-018; DP-17 |
| AI runs only in rwb-agent, suggests and never decides, and can be switched off | Arch v5 slides 35 and 36; BOT AI risk guidelines of 12 September 2025 |
| Embedded Drools in the owning service; the rule result the agent falls back to is the owning service's rule answer | ADR-017; DP-04; R-UNI-32 |

### 2.5 Exclusions of this PRD

| Excluded | Reason and later home |
|---|---|
| The business decisions an agent supports: the route decision, the treatment, the deviation determination, the write-off | Owned by S1, S2, S8 and S7; this service proposes and records, the owner decides (FR-P10-007, FR-P10-013) |
| The queue write interface for models and agents (REQ-CWC-017 to REQ-CWC-020) | The queue, its ordering and the write API are P3's; this service supplies the agent side of the call and its record (ASM-2654) |
| The rules engine, rule packages and the rule registry | P7 rwb-decision and the embedded Drools kit (ADR-017; DP-04) |
| Document classification, OCR, extraction and the document store | P5 rwb-document; this service evaluates the extraction quality and runs agents over the extracted fields |
| The dashboard product, report definitions and the steering measures | P9 rwb-reporting; this service supplies the per-agent measures and the alerts |
| A general-purpose model host, model training, fine-tuning or a model registry beyond the policy row | Not in the source set; the model is an approved external endpoint reached through the gateway (ASM-2646) |
| Solution design: class names, table columns, endpoint signatures, deployment topology | Out of scope of a PRD; the story set and the technical specification carry it |

## 3. Personas and roles

Roles only; no person is named anywhere.

| Role | Who | What they need from this service |
|---|---|---|
| AI product owner (RW-COE) | Centre of excellence | Load a policy and a prompt version, start an evaluation, read the score and the report, propose an autonomy step on evidence |
| Risk and model risk officer (RW-RISK) | Model risk | Approve a policy or prompt version, approve a step-up or a drop, see drift and cost, take the agent risk pack to the committee |
| Centre of excellence analyst | Centre of excellence | Run champion and challenger, load a labeled sample, read the per-check failure counts |
| Case owner and case officer roles (case owner, litigation officer, restructuring officer FCR, conduct and QA officer) | Recovery operations | See what the agent proposed, accept, correct or reject it with a coded reason, and never be blocked when the agent is slow or down |
| Platform administrator (RW-PLATADM) | Operations and platform team | Switch a switch-shaped row, read a run, see a fallback or a cost alert, and know that every change is audited |
| Reporting and BI analyst | Data office | Read the per-agent and per-version measures of a business date on one screen and in the read model |
| Data steward and data product owner | Data office | Know that a run used a stale business date or a masked field set, and see which agent and which version |
| Security administrator | Second line | Confirm that agents run under service identities, that the tool gateway is read-only, and that no personal data leaves in a prompt or an event |
| Compliance and internal audit | Second and third line | Reproduce any answer from the recorded policy, prompt, model version and inputs, and hold the fallback evidence |
| Tech lead of rwb-agent | TechX | A stable contract for the service, its one event and its one workflow |

## 4. User journeys

### 4.1 One agent run, today and in the target

| Step | Today (monolith) | Target (rwb-agent) |
|---|---|---|
| 1 | The module calls a model from inside its own code, with the prompt in the code or in a file | The service takes the policy and prompt version in force for the business date from its own tables |
| 2 | The answer is used by the calling code with no schema check | The guardrail tests the answer against the output schema, the allowed tools and the confidence floor |
| 3 | A model that is slow blocks the officer | The call ends at the timeout, the rule result is used, the case still routes and the fallback is recorded |
| 4 | Nothing records the model version or the cost | One run row holds the versions, the latency, the tokens, the cost and the fallback flag, and `AgentRunCompleted` is published |

### 4.2 From shadow to L1 for the intake agent, today and in the target

| Step | What happens |
|---|---|
| 1 | The intake policy is in mode SHADOW: the agent summarises the case and flags gaps, and no case field, task, queue or decision changes (FSD P10 v3 AC-P10-003-01) |
| 2 | Business analysts review the same cases; the evaluation scores the agreement per gap type against sample `INTAKE-S1` (AC-ALT-P10-003-01) |
| 3 | The evaluation report holds the sample size, the agreement, the failure counts, the cost per case and the latency, with the policy, prompt and model version (AC-P10-007-01) |
| 4 | The centre of excellence loads a new policy version with mode L1, the evaluation run, the conditions and the measures to watch; the risk role approves it and it takes effect from its valid-from date (AC-ALT-P10-007-01) |

### 4.3 The extraction evaluation that sets the confidence threshold

| Step | What happens |
|---|---|
| 1 | A labeled sample is loaded for a document type; a row for a document the hub does not return refuses the whole file and stores nothing |
| 2 | Three approaches run per field: OCR template, model, and both; one score row exists per field and approach with precision and recall |
| 3 | The proposal names the approach with the highest mean F1 and the lowest confidence at which every chosen field reaches precision 0.95 |
| 4 | A type with too few labels is scored and marked insufficient sample, and no approach and no threshold are proposed for it |

### 4.4 An agent slow, an agent wrong, an agent off

| Step | What happens |
|---|---|
| 1 | The model does not answer inside the timeout: the run is `TIMED_OUT` with fallback true and the rule result is returned |
| 2 | The answer arrives but fails the output schema: the run is `GUARDRAIL_FAILED` with the check code and the field name, and the rule result is used |
| 3 | The answer is below the confidence floor, or the document tool is unavailable: the run is `BELOW_FLOOR` or `TOOL_UNAVAILABLE`, fallback true |
| 4 | The mode is OFF: no model call is made and the caller is told that no suggestion is available |

### 4.5 A morning of watching, and a drift breach

| Step | What happens |
|---|---|
| 1 | The daily aggregation writes one measure row per agent and version for the business date; a rerun of the same date writes no second row |
| 2 | A cost above the daily parameter raises one alert row for that agent and date and one notification to the holders of the two roles; a rerun sends nothing |
| 3 | Calibration and drift are watched against the threshold and the minimum feedback on the policy row; below the minimum feedback no drift alert is raised and the screen says so |
| 4 | A breach raises a decision with an owner and a date, and can drop the agent's mode with the approval that change needs |

### 4.6 The TDR offer suggestion (wave 2)

| Step | What happens |
|---|---|
| 1 | The treatment service asks for a suggestion for one treatment; the gateway returns the installments and the model version, or nothing |
| 2 | The suggestion is recorded with decision D5, the model version and the inputs reference, and the treatment screen shows that it was suggested and by which version |
| 3 | The same treatment asking twice receives the first suggestion and its record, and no second model call is made |
| 4 | A treatment that is not a restructure, a model that is not built and a failed decision record all return no suggestion with the message the source names |

## 5. Capabilities and features

A capability carries the highest priority among the BRD requirements it traces to, and no capability is prioritised above or below what it serves. Ten capabilities are Must because each serves a BRD requirement of priority Must; CAP-P10-005 is Should because its only business requirement, BR-015, is Should in the epic BRD. The governance capabilities CAP-P10-008 and CAP-P10-009 are Must because they serve BR-084, which the epic BRD sets to Must, while the autonomy row itself serves the Should requirement BR-015.

| CAP | Capability | BR IDs | MoSCoW | Wave | FRs | FSD feature |
|---|---|---|---|---|---|---|
| CAP-P10-001 | The agent runtime and the model gateway: one run per request, the versions in force, the run record, the idempotency key, the read-only tool gateway and the service identity | REQ-CWC-018, REQ-ACA-005, REQ-ACA-010, REQ-DRI-001 | Must | 1 | FR-P10-001, FR-P10-002, FR-P10-024, FR-P10-025 | FEAT-AGT-01 |
| CAP-P10-002 | The guardrail checker on every answer and the refusal to return an answer whose decision record cannot be written | REQ-CWC-018, REQ-DRI-005 | Must | 1 | FR-P10-003, FR-P10-026 | FEAT-AGT-02 |
| CAP-P10-003 | Fallback to the rule result inside 60 seconds, recorded | REQ-DRI-001 | Must | 1 | FR-P10-004 | FEAT-AGT-11 |
| CAP-P10-004 | Shadow running: the intake, screening and legal document agents record an answer and change nothing | REQ-CWC-017, REQ-CWC-019, REQ-DCM-011, REQ-DVH-001 | Must | 1 builds, 2 first use | FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014 | FEAT-AGT-03, FEAT-AGT-08, FEAT-AGT-09 |
| CAP-P10-005 | The policy, prompt and version store with a validated load, a separate approval and validity dates | BR-015 | Should | 1 | FR-P10-005, FR-P10-006 | FEAT-AGT-01 |
| CAP-P10-006 | Evaluation and scoring: the labeled sample, the score per label key, the extraction threshold proposal and the evaluation report | REQ-DRI-001, REQ-DCM-005, REQ-DCM-006, BR-084 | Must | 1 | FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011 | FEAT-AGT-04, FEAT-AGT-05 |
| CAP-P10-007 | Monitoring and alerting: the daily per-agent and per-version measures, the screen, and the cost and drift alerts to the named roles | BR-084 | Must | 1 builds, 2 full | FR-P10-016, FR-P10-017 | FEAT-AGT-06 |
| CAP-P10-008 | Autonomy governance: the level as a versioned row, drift watched against a stated threshold, a step up or down on measured evidence with approval | BR-015, BR-084, REQ-CWC-019 | Must | 2 | FR-P10-019, FR-P10-020, FR-P10-021 | FEAT-AGT-12, FEAT-AGT-13, FEAT-AGT-15 |
| CAP-P10-009 | Champion and challenger, and the committee view of performance, overrides and incidents | BR-084, BR-081 | Must | 4 | FR-P10-022, FR-P10-023 | FEAT-AGT-14, FEAT-AGT-16 |
| CAP-P10-010 | Feedback and override capture: a person's verdict with a coded reason, recorded only when the decision record is written | REQ-APD-005, REQ-DRI-005 | Must | 2 | FR-P10-018 | FSD P10 v3 A2.7, A2.8; RWB-E2-028, RWB-E2-029 |
| CAP-P10-011 | The TDR offer-suggestion model served through the model gateway, recorded as decision D5 | REQ-CHO-006, REQ-DRI-001, REQ-CWC-017 | Must | 2 | FR-P10-015, FR-P10-026 | FEAT-AGT-10; RWB-E2-032 |

### 5.1 Capabilities carried out of scope, with their source

| Removed or non-capability | Source and disposition |
|---|---|
| The Power BI data set and the lake write behind the agent dashboard | Removed by Architecture v5 (ADR-018, DP-17); the measures are the service's own and the read model's (GAP-1516; ASM-2641) |
| `agent_run_daily` as a table of the service | Not in the Logical Data Model v8 entity list; read as a projection over the run record (GAP-1517; ASM-2642) |
| The queue write interface, the queue ordering and the case write | P3 rwb-case, P2 rwb-integration for the interface; this service supplies the agent side (ASM-2654) |
| Any write by an agent to a case, a task, a queue, a deviation, a treatment or a decision other than its own record | Forbidden by the shadow rule and by the role checks (FR-P10-007, FR-P10-025) |
| Model training, tuning and a model registry | Not in the source set (ASM-2646) |
| The legal decision the agent supports (route, treatment, deviation, write-off) | The owning service decides (GAP-1531) |

## 6. Functional requirements

Every requirement is specific and testable. The FSD column names the FSD section and acceptance criteria the requirement serves; the BR column names the business requirement it traces to.

| ID | Requirement | CAP | BR (BRD) | FSD source | Priority |
|---|---|---|---|---|---|
| FR-P10-001 | The service SHALL run an agent only on a request that carries the agent code, the case or subject key, the trigger and an idempotency key; it SHALL take the policy, prompt and model version in force for the business date, SHALL record one run row with those versions, the mode, the status, the confidence, the guardrail result, the latency, the tokens in and out and the cost, and SHALL publish `rwb.agent.AgentRunCompleted.v1` with the run ID, the agent, the case ID, the outcome and the fallback flag, carrying no personal data. | CAP-P10-001 | REQ-DRI-001 | FSD P10 v3 A2.1, AC-P10-001-01; Arch v5 slides 16 and 43 | Must |
| FR-P10-002 | The service SHALL recognise a run request whose idempotency key it has already processed, SHALL make no second model call and write no second run row, SHALL return the first result and SHALL count the repeat against that key. | CAP-P10-001 | REQ-DRI-001 | FSD P10 v3 AC-EXC-P10-001-04, AC-EXC-P10-003-02, R-UNI-40 | Must |
| FR-P10-003 | The service SHALL test every answer against the output schema referenced by the policy, the allowed tool list and the confidence floor; it SHALL return the rule result and record the run as `GUARDRAIL_FAILED` or `BELOW_FLOOR` with the failed check code and its detail, and SHALL count the failures per check code, per agent and per business date. | CAP-P10-002 | REQ-CWC-018, REQ-ACA-010 | FSD P10 v3 A2.2, AC-ALT-P10-001-02, AC-EXC-P10-010-03 | Must |
| FR-P10-004 | The service SHALL end a model call at the timeout held on the policy row, SHALL record the run as `TIMED_OUT` with fallback true and the measured latency, SHALL return the rule result with the fallback reason, and SHALL leave the case able to route; the timeout SHALL be a data row and not a value in code. | CAP-P10-003 | REQ-DRI-001 | FSD P10 v3 A2.11, AC-EXC-P10-001-01, R-UNI-32; Arch v5 slides 16 and 34 | Must |
| FR-P10-005 | The service SHALL hold every policy and every prompt as a versioned row with its validity dates, its status, the loader and the approver, and SHALL use for a run the version in force on the run's business date; a retired or superseded prompt SHALL stay readable with its text hash unchanged. | CAP-P10-005 | BR-015 | FSD P10 v3 A2.1, A2.6.3.2, AC-ALT-P10-001-01 | Should |
| FR-P10-006 | The service SHALL refuse a policy or prompt load that fails a stated check, with the failed check named and no version row written, and SHALL refuse an approval by the user who loaded the version. | CAP-P10-005 | BR-015 | FSD P10 v3 AC-EXC-P10-001-02, AC-EXC-P10-001-03 | Should |
| FR-P10-007 | In mode SHADOW the service SHALL store the answer on the run only, SHALL change no case field, task, queue, route state, deviation record or contact stop, SHALL return the answer from no user-facing endpoint, and SHALL NOT pass the answer to another service for action. | CAP-P10-004 | REQ-CWC-017, REQ-CWC-019 | FSD P10 v3 A2.3, A2.8, A2.9, AC-P10-003-01, AC-P10-008-01, AC-P10-009-01 | Must |
| FR-P10-008 | The service SHALL score an agent against a versioned labeled sample before any autonomy change, SHALL write one score row per label key and approach holding the agreement rate, the precision, the recall, the sample size and the policy, prompt and model version, and SHALL NOT accept an autonomy proposal that names no evaluation run. | CAP-P10-006 | REQ-DRI-001, BR-084 | FSD P10 v3 A2.5, AC-ALT-P10-003-01, AC-ALT-P10-008-01 | Must |
| FR-P10-009 | The service SHALL evaluate field extraction for a document type across the three approaches the source names (OCR template, model, and both), SHALL write one score row per field and approach with the true and false positives and negatives, the precision and the recall, and SHALL propose the approach with the highest mean F1 and the lowest confidence at which every chosen field reaches precision 0.95; a type below the minimum labeled sample SHALL be scored, marked insufficient sample, and given no approach and no threshold. | CAP-P10-006 | REQ-DCM-005, REQ-DCM-006 | FSD P10 v3 A2.4, AC-P10-004-01, AC-ALT-P10-004-01, AC-ALT-P10-004-02 | Must |
| FR-P10-010 | The service SHALL produce an evaluation report holding the sample size, the agreement rate per gap type or code, the failure counts by type, the total cost, the cost per case, the median and 95th percentile latency and the policy, prompt and model versions, with no personal field; it SHALL refuse the report of an evaluation that is still running. | CAP-P10-006 | BR-084, REQ-DRI-001 | FSD P10 v3 A2.7, AC-P10-007-01, AC-ALT-P10-007-02 | Must |
| FR-P10-011 | The service SHALL refuse an evaluation on a sample with no labeled row for the agent, SHALL refuse a second evaluation of the same agent, sample and sample version while one is running, and in both cases SHALL write no evaluation run and no run row. | CAP-P10-006 | REQ-DRI-001 | FSD P10 v3 AC-EXC-P10-001-05, AC-EXC-P10-001-06 | Must |
| FR-P10-012 | The service SHALL start one intake run per `CaseCreated` event and business date, keyed by the case and the date, SHALL store the case summary and the gap flags on the run only, and SHALL score the agreement per gap type against the reviewers' sample. | CAP-P10-004 | REQ-CWC-017, REQ-DCM-011 | FSD P10 v3 A2.3, AC-P10-003-01, AC-ALT-P10-003-01, AC-ALT-P10-003-02 | Must |
| FR-P10-013 | The service SHALL propose deviation codes X1 to X7 for a case from its data, its call notes and its documents, with the reason and the source reference of each proposal, SHALL record the proposal on the run only, and SHALL leave the deviation record and the contact stop to rwb-deviation. | CAP-P10-004 | REQ-DVH-001, REQ-DCM-005 | FSD P10 v3 A2.8, AC-P10-008-01, AC-ALT-P10-008-01, AC-ALT-P10-008-02 | Must |
| FR-P10-014 | The service SHALL build a legal document pack that lists, for each of the nine items the source names, the document IDs held and a completeness status of PRESENT, MISSING or DEFECT, SHALL store the pack on the run only, and SHALL return it from no user-facing endpoint while the mode is SHADOW. | CAP-P10-004 | REQ-DCM-011 | FSD P10 v3 A2.9, AC-P10-009-01 | Must |
| FR-P10-015 | The service SHALL serve the TDR offer suggestion through the model gateway for a restructure treatment, SHALL return the suggested terms with the model version and record one decision log entry with decision D5 and the inputs reference, SHALL return the first suggestion for a repeated request for the same treatment with no second model call, and SHALL return no suggestion when the mode is OFF, when the treatment is not a restructure, when the model is unavailable or when the decision record cannot be written. | CAP-P10-011 | REQ-CHO-006, REQ-DRI-001, REQ-CWC-017 | FSD P10 v3 A2.10, AC-P10-010-01, AC-ALT-P10-010-01 to AC-EXC-P10-010-05 | Must |
| FR-P10-016 | The service SHALL expose, per agent and per policy and prompt version for a business date, the number of runs, the fallback rate, the median and 95th percentile latency, the cost, and the latest evaluation score, and SHALL show acceptance and override as not applicable while no run of that agent is at L1. | CAP-P10-007 | BR-084 | FSD P10 v3 A2.6, AC-P10-006-01, AC-EXC-P10-006-02 | Must |
| FR-P10-017 | The service SHALL write one daily measure row per agent and version for the business date, SHALL raise one alert row and one notification to the holders of the centre-of-excellence and model-risk roles when the cost of an agent exceeds the daily parameter on its policy row, and SHALL create no second measure row, alert row or notification when the same date is processed again. | CAP-P10-007 | BR-084 | FSD P10 v3 AC-ALT-P10-006-01, AC-ALT-P10-006-02, AC-EXC-P10-006-03 | Must |
| FR-P10-018 | The service SHALL record a person's verdict on an agent answer (accept, correct or reject) against the run with a coded reason, SHALL require the coded reason for an override of a recommendation, SHALL write no feedback row when the decision log entry cannot be written, and SHALL make the override rate reportable per agent and per role. | CAP-P10-010 | REQ-APD-005, REQ-DRI-005 | FSD P10 v3 AC-EXC-P10-007-02, AC-EXC-P10-008-02; BRD Epics 3 to 8 v1 BR-084 | Must |
| FR-P10-019 | The service SHALL change the autonomy level of one agent for one segment or for all through a versioned policy row, SHALL keep the version in force until a new version is approved, SHALL require the approver to differ from the loader, and SHALL switch the agent off when the row says OFF with no other change. | CAP-P10-008 | BR-015, REQ-CWC-019 | FSD P10 v3 A2.12, A2.6.3.2, AC-EXC-P10-001-03; BRD Epics 3 to 8 v1 ASM-024 | Must |
| FR-P10-020 | The service SHALL watch calibration and drift for each agent and segment against the threshold and the minimum feedback held on the policy row, SHALL raise no drift alert below the minimum feedback and show that state, and SHALL raise on a breach a decision with an owner and a date and may propose the lower mode. | CAP-P10-008 | BR-015, BR-084 | FSD P10 v3 A2.13, AC-EXC-P10-006-04; BRD Epics 3 to 8 v1 BR-015 | Must |
| FR-P10-021 | The service SHALL accept a step up or a step down of an autonomy level only when the policy row names the evaluation run, the conditions and the measures to watch, only when every stated condition is met by that evaluation, and only with the approval the risk role gives for that change; the previous version SHALL stay in force until then. | CAP-P10-008 | BR-084 | FSD P10 v3 A2.15, AC-ALT-P10-007-01, AC-ALT-P10-009-02; BRD Epics 3 to 8 v1 BR-084 | Must |
| FR-P10-022 | The service SHALL run two rule or model versions side by side on the same population as a champion and a challenger, SHALL score both on the same sample, and SHALL present the comparison with the outcome, the cost and the latency of each, without changing which version is in force. | CAP-P10-009 | BR-084 | FSD P10 v3 A2.14; BRD Epics 3 to 8 v1 BR-084 | Must |
| FR-P10-023 | The service SHALL produce the agent risk pack for the strategy and model committee holding, per agent and version, the performance, the override rate, the fallbacks and the incidents of the period, and SHALL record the committee decision against it. | CAP-P10-009 | BR-084, BR-081 | FSD P10 v3 A2.16; BRD Epics 3 to 8 v1 BR-084 | Must |
| FR-P10-024 | The service SHALL call the model endpoint and every tool under its own service identity, SHALL pass the same role and scope checks as a person through the rwb-access contract, SHALL apply the masking rule before personal data enters a prompt, and SHALL place no personal data in a prompt body, a run payload, a workflow input, an event or a log. | CAP-P10-001 | REQ-ACA-010, REQ-ACA-005 | FSD P10 v3 A2.1, A2.2; Arch v5 slide 35; NFR-039, NFR-040 | Must |
| FR-P10-025 | The service SHALL reach case facts and extracted document fields only through the tool gateway, which is read-only and one hop, SHALL write nothing outside `rwb_agent`, SHALL hold no grant on the recovery schema and no grant on another `rwb_*` schema, and SHALL expose no tool that writes to another service; the allowed tool list of a policy version SHALL only narrow the read tools of the gateway, and `read_case` is a tool identifier on that list, not a data entity or field. | CAP-P10-001 | REQ-CWC-018 | FSD P10 v3 A2.1 integration points; Arch v5 slides 16 and 29; DP-05, DP-11 | Must |
| FR-P10-026 | The service SHALL return no answer when the decision log entry of the run cannot be written, SHALL raise the failure to the caller with the message the source names, and SHALL leave the run without a decision log entry ID. | CAP-P10-002, CAP-P10-011 | REQ-DRI-005 | FSD P10 v3 AC-EXC-P10-010-04, AC-EXC-P10-001-08, AC-EXC-P10-007-02 | Must |

### 6.1 Business rules that qualify the requirements

| BR ID | Rule | Source |
|---|---|---|
| BR-P10-001 | No value a business person may change is written in code: the timeout, the confidence floor, the daily cost cap, the price per token, the autonomy mode, the watch measures and the fallback rule are policy rows | FSD P10 v3 BR-P10-001 to BR-P10-016; principle 1; Arch v5 slide 35 |
| BR-P10-001-SHADOW | An agent suggests and never decides: a person keeps the decision on every material action, and the shadow mode is the proof that a new agent suggests well before it is allowed to act | Arch v5 slide 35; BOT AI risk guidelines of 12 September 2025 |
| BR-P10-002 | The rule is deterministic: the rule result the fallback uses is the owning service's answer for the same inputs, not a second rule evaluation inside this service | ADR-017; RULE-031 of BRD Epics 3 to 8 v1; R-UNI-32 |
| BR-P10-003 | No personal data and no document content in a prompt, a run payload, an event, a workflow input or a log; identifiers and masked values only | Arch v5 slide 35; CTL-11; DP-09; NFR-039, NFR-040 |
| BR-P10-004 | The service owns the policies, the prompts, the runs, the guardrails, the evaluations, the feedback and the alerts; it owns no case, no document, no deviation, no treatment, no queue and no ACE object | DP-01; Arch v5 slide 41; Ownership Map |
| BR-P10-005 | An autonomy change is a decision of the model risk role on measured evidence, and the evidence is an evaluation run that exists when the change is made | BRD Epics 3 to 8 v1 BR-015, BR-084, RULE-029 |

## 7. Non-functional requirements

Each requirement traces to a BRD non-functional requirement; a target the source does not state is held open and never invented (ASM-2647).

| ID | Requirement | Traces to | Target | Status |
|---|---|---|---|---|
| NFR-P10-001 | An agent answers inside its target, and after that the rule result is used and the case still routes | NFR-010 | 60 seconds, then the rule result | Proposed |
| NFR-P10-002 | An agent or model outage falls back to the rule result and the case still routes | NFR-024 | Fallback always on | Proposed |
| NFR-P10-003 | The approved model endpoint is reached over a private endpoint inside the bank's tenancy, and no service calls a model endpoint except through this gateway | NFR-048, NFR-046 | Private endpoint; one gateway | Proposed |
| NFR-P10-004 | Agents run under service identities and pass the same role, scope and delegation checks as a person on every run and every tool call | NFR-051 | Service identities | Proposed |
| NFR-P10-005 | Secrets are held in the key store and never in code, configuration files or prompt text | NFR-052 | No secret in code or prompts | Proposed |
| NFR-P10-006 | Data is encrypted at rest and in transit, workflow payloads are encrypted, and personal data is minimised per agent and masked before it leaves the service | NFR-053, NFR-039, NFR-040 | Encrypted; masked in use; minimised per agent | Proposed |
| NFR-P10-007 | Every answer is schema checked against the allowed tool list and the confidence floor, and a failed check falls back to the rules | NFR-055 | Schema check on every output | Proposed |
| NFR-P10-008 | Logs, traces and metrics are produced for every run, guardrail check, fallback and evaluation, and acceptance, override rate, latency and cost are measured per agent and version | NFR-064, NFR-066 | Measured per agent and per version | Proposed |
| NFR-P10-009 | A failing agent, a fallback rate above its limit, a cost cap and a drift breach raise an alert to the named owner role inside its target, and every agent has a run book entry | NFR-067, NFR-068 | Alert within 15 minutes to the named owner | Proposed, DL11 |
| NFR-P10-010 | The service is available when cases are worked and when agents run, including outside business hours | NFR-020, NFR-021 | 99.9 percent in business hours; 99.5 percent outside, excluding the change window | Proposed, DL11 |
| NFR-P10-011 | Every answer is reproducible from the record: the policy, prompt and model version, the rule version, the guardrail result and the inputs reference | NFR-033, NFR-034 | Every decision reproducible | Proposed |
| NFR-P10-012 | Runs, feedback, samples, evaluations and alerts are retained for the period set for them and are answerable to audit before a purge | NFR-030, NFR-036 | Not specified in the source documents (GAP-1524; ASM-2648) | Open, DL26 |
| NFR-P10-013 | No production data is used in development, and every evaluation sample and fixture is synthetic or masked | NFR-045 | Synthetic in development, masked in user acceptance | Proposed |
| NFR-P10-014 | Agent data stays in the bank's own tenancy in the agreed region, and every policy and prompt row carries a classification | NFR-046, NFR-047 | SCB Azure, Southeast Asia; classification per row | Proposed, DL26 |
| NFR-P10-015 | The agent monitor answers inside the screen target under normal load, including a business date with every agent and version | NFR-008 | Under 2 seconds | Proposed |
| NFR-P10-016 | A restart, a replay or a repeated request runs no agent twice and charges no model call twice, a release rolls back by redeploying the previous tag, and a policy change rolls back to its previous version by one call | NFR-027 | Idempotent on the run key; rollback by previous tag and by one call | Proposed |
| NFR-P10-017 | An audit or regulatory request is answered inside its deadline with the run history, the guardrail result and the decision record of a named case population | NFR-036 | Inside the deadline set by the requester | Proposed |

## 8. Data requirements

The service holds the policy, the evidence of a run and the evidence of an evaluation. It holds no case, no document, no deviation, no treatment and no ACE copy.

| Entity | Key fields | Classification | Source | Retention |
|---|---|---|---|---|
| Agent policy version (`agent_policy`) | agent code, policy version, model code and version, output schema reference, allowed tools, autonomy mode, segment product group and region, confidence floor, timeout, daily cost cap, price per token, alert role, review date, evaluation run, promotion conditions, watch measures, fallback rule, status, valid from and to, loader, approver | [CONFIDENTIAL] | Loaded by the centre of excellence, approved by the model risk role | Versioned; superseded rows kept with their validity dates; period open (NFR-P10-012) |
| Agent prompt version (`agent_prompt`) | agent code, prompt version, prompt text with placeholders, SHA-256 of the text, status, valid from and to, loader, approver | [CONFIDENTIAL] | Loaded by the centre of excellence, approved by the model risk role | Versioned; text hash kept unchanged after retirement |
| Agent run (`agent_run`) | run ID, agent code, agent version, prompt version, model version, case key, subject key, autonomy mode, trigger event, idempotency key, status, fallback flag, guardrail result, masked output, confidence, latency, tokens in and out, cost, decision log entry ID | [CONFIDENTIAL], with [PII] inside the masked output where the answer holds party facts | Written by the service on every run | Open (NFR-P10-012; GAP-1524) |
| Agent sample (`agent_sample`) | sample code, sample version, agent code, label key, subject reference, expected label, labeled by role | [PII] where the subject is a case or a document | Loaded by the centre of excellence and reviewed by the business reviewers | Open (NFR-P10-012) |
| Agent evaluation run (`agent_evaluation_run`) | evaluation run ID, agent code, sample code and version, policy and prompt version, status, started at, finished at, failure counts | [CONFIDENTIAL] | Written by the service | Open (NFR-P10-012) |
| Agent evaluation (`agent_evaluation`) | evaluation run, label key or field, approach, true and false positives and negatives, precision, recall, agreement rate, sample size, model and prompt version | [CONFIDENTIAL] | Written by the service | Open (NFR-P10-012) |
| Agent feedback (`agent_feedback`) | run ID, verdict (accept, correct, reject), coded reason, the user role, the time, the decision log entry ID | [CONFIDENTIAL] | Written by the service on a person's verdict | Open (NFR-P10-012) |
| Agent alert (`agent_alert`) | alert ID, agent code, type (cost cap, drift), business date, measured value, threshold, role notified, sent at | [CONFIDENTIAL] | Written by the service on a breach | Open (NFR-P10-012) |
| Daily agent measure (projection) | business date, agent code, policy and prompt version, runs, fallback rate, median and 95th percentile latency, cost, latest evaluation score | [CONFIDENTIAL] | Computed by the service from the run record; the entity the FSD names is not in the Logical Data Model v8 (GAP-1517) | Recomputed per business date; one row per agent and version |
| Published event record (library) | event type and version, case ID, sequence, idempotency key, payload, occurred at | [CONFIDENTIAL] | Platform outbox library, written in the same transaction as the run | Per the platform event retention |
| Processed event record (library) | consumer, key, event ID, hit count, last seen at | [CONFIDENTIAL] | Platform inbox library, on every consumed event | Per the platform event retention |
| Idempotency record (library) | key, operation, request hash, stored response | [CONFIDENTIAL] | Platform library | 24 hours for the stored response |
| Local decision record (library) | decision code, action (answer, suggestion, fallback, refusal), run reference, freshness, versions | [CONFIDENTIAL] | Library on the shared decision-record topic | Per the decision log retention, DL26 |
| Case and document facts read at run time | case key, product, stage, route, arrears band, document type, extracted fields | [PII] and [SENSITIVE_FINANCIAL] | Read through the rwb-source-data and rwb-document tool contracts | Not stored by this service |
| Status and list values | agent list, autonomy list, configuration status list, run status list, alert type list | [PUBLIC] | Reference data | Versioned |

Rules that apply to the data:

- The service holds no copy of an ACE row, no staging table and no load table (ADR-014; DP-01; DP-05).
- A prompt body carries placeholders and no personal data; the values are bound at run time from the masked tool result and are not stored in the prompt row (BR-P10-003).
- A shadow run stores its answer on the run row and nowhere else; no case, task, deviation or treatment row exists because of it (FR-P10-007).
- The physical names, lengths and required flags of the eight owned entities are the technical specification's; this PRD fixes the product content only.

## 9. Integration points

| System or service | Direction | Protocol | Owner | Notes and unknowns |
|---|---|---|---|---|
| Enterprise AI endpoint (INT-23) | Out | HTTPS over a private endpoint inside the SCB tenant | ACE platform with the rwb-agent owner | The approved model endpoint; no public egress; no other service calls a model directly |
| gateway-bff | In | REST under `/api/recovery/agent/v1` behind the gateway | RWB-PLT-EDGE | One hop, 2 s timeout; the agent monitor and the admin reads |
| rwb-case | In | Kafka: `CaseCreated` | rwb-case | Starts the intake run once per case (EV-01) |
| rwb-document | In | Kafka: `DocumentStored`; out: REST tool call for extracted fields | rwb-document | Starts a screening run once per document event; the pack reads document identity only (EV-16) |
| rwb-source-data | Out | REST tool call, one hop, 2 s budget | rwb-source-data | Case facts come through this contract and not from a view (GAP-1518) |
| rwb-access | Out | REST | rwb-access | Role, scope and masking policy of the acting role and of the service identity |
| rwb-decision | Out | REST and the shared decision-record topic | rwb-decision | The decision record of every answer, suggestion and fallback; the approval of a policy or an autonomy change |
| rwb-deviation | In | REST request and a Temporal child run request | rwb-deviation | The screening run is started by the deviation service as a child run; the proposal returns on the run, and the deviation record, the pause and the contact stop stay with S8 |
| rwb-treatment | In | REST request for a TDR suggestion | rwb-treatment | Wave 2; the suggestion is recorded against the treatment (FR-P10-015) |
| rwb-reporting | Out | Events and the daily measure hand-over | rwb-reporting | The read model and the steering measures; no data lake and no Power BI connection (GAP-1516) |
| ACE common module (notification path, PII logging, sign-in) | Out | ACE paths | ACE team | Cost and drift alerts to the two roles; PII logging to SOC; no P10 build |
| Bank scheduler (Airflow) | In | Trigger for the daily aggregation | Platform | The daily aggregation of the agent measures; JOB-15 stays the reporting extract of rwb-reporting (GAP-1519) |
| Key store | Out | Managed identity | Platform | Model credentials and certificates; never in code, configuration or prompts |

Unknowns carried as questions: the acceptance, override and cost targets per agent (Q-P10-01), the evidence and threshold for an autonomy change (Q-P10-02), the E3 and E8 screen dependency (Q-P10-03), the mask list per agent (Q-P10-04), the retention of runs, feedback and samples (Q-P10-05), whether an agent may ever call a write tool (Q-P10-06), the regulator position on recording prompts and model outputs (Q-P10-07) and the boundary of the TDR suggestion message (Q-P10-08).

## 10. Release slicing proposal

Waves follow Architecture v5 slide 38 and the wave map of the Story Template and Rules section R5.6. Dates are copied unchanged from BRD Program v5 section 8 and are tentative.

| Slice | Wave | Release (tentative) | Capabilities | Rationale |
|---|---|---|---|---|
| Platform enablers | 0 | November 2026 (tentative) as the wave month; day: Not specified in the source documents (GAP-1525; ASM-2656) | None of this PRD; the platform epics supply the service template, the outbox and inbox library, the workflow kit, the schema and login, the Kafka topic and ACLs, the gateway route and observability | Nothing of this service is buildable before its platform enablers exist |
| MVP | 1 (Epic 1, EP01) | 30 November 2026 (tentative) | CAP-P10-001, CAP-P10-002, CAP-P10-003, CAP-P10-005, CAP-P10-006, CAP-P10-007 (built), CAP-P10-004 (built, shadow only) | The Epic 1 promise for this service is the runtime, the guardrail, the fallback and the evidence: a prompt and a policy version that is approved before use, an answer that is checked or replaced, and a score before anyone sees it. The FSD places the platform set-up, the guardrail, the intake shadow, the extraction evaluation, the harness, the dashboard and the fallback in E1 (FEAT-AGT-01 to FEAT-AGT-06, FEAT-AGT-11) |
| Wave 2 increment | 2 (Epic 2 and Epic 3, EP02 and EP03) | 31 December 2026 (tentative) and 31 January 2027 (tentative) | CAP-P10-004 activated (screening and legal document, and the intake at L1), CAP-P10-010, CAP-P10-011, CAP-P10-007 full, CAP-P10-008 | Shadow work already scored becomes live work on measured evidence, the feedback loop that measures acceptance starts, the TDR suggestion is exposed on the gateway, and the autonomy row and drift watch arrive with EP03 as the FSD and the epic BRD place them (FEAT-AGT-07 to FEAT-AGT-10, FEAT-AGT-12, FEAT-AGT-13) |
| Wave 3 reuse | 3 (Epic 4 and Epic 5, EP04 and EP05) | 28 February 2027 (tentative) and 31 March 2027 (tentative) | No new capability | The route agent of S1 and the litigation pack reuse the runtime as policy rows and runs; the capability set of this PRD is unchanged |
| Wave 4 governance | 4 (Epic 6 to Epic 8, EP06 to EP08) | 30 April 2027 (tentative), 31 May 2027 (tentative) and 30 June 2027 (tentative) | CAP-P10-009 | Champion and challenger, the approval of an autonomy step and the committee pack are the E8 governance promise (FEAT-AGT-14 to FEAT-AGT-16) |

Slicing rules:

- A capability ships whole: an autonomy row never ships without the drift watch that can lower it, and an answer never ships without the guardrail and the fallback.
- CAP-P10-004 ships built in wave 1 and activated in wave 2; an agent that runs in shadow longer than its slice states is a defect of the slice, not a stretch.
- No slice of this PRD starts before the platform enablers of wave 0 exist.
- A capability that cannot meet its slice is cut from the slice and reported, never shipped partly.

## 11. Acceptance criteria and validation evidence

```gherkin
Feature: P10 rwb-agent product behaviour

  Background:
    Given the policy version in force for the agent names its model, output schema, allowed tools, confidence floor and timeout
    Given the business date is 2026-11-30
    Given every consumed contract is the published contract of its owner and every downstream answer is the fake of that contract

  Scenario: AC-P10-001 An approved endpoint answers and the run is recorded once
    Given the approved model endpoint on the private endpoint of the SCB tenant
    When the orchestrator runs the agent for case "RW-2026-000101"
    Then the call succeeds with run status ANSWERED
    And one agent run row holds the agent, the policy version, the prompt version, the model version, the latency, the tokens in and out and the cost
    And one AgentRunCompleted event is written to the outbox with the run ID, the agent, the case ID, the outcome and fallback false
    And the event carries no name, no address and no document content

  Scenario: AC-P10-002 A repeated run request has no further effect
    Given the agent ran for case "RW-2026-000101" with the idempotency key "AGENT:RW-2026-000101:2026-11-30"
    When the same request arrives again with the same key
    Then no second agent run row and no second model call exist
    And the first result is returned and the idempotency hit is counted

  Scenario: AC-P10-003 An answer that fails the guardrail is replaced by the rule result
    Given the model stub returns an answer with the summary field missing from the output schema
    When the guardrail runs
    Then the output is rejected with run status GUARDRAIL_FAILED and fallback true
    And the guardrail result holds check code SCHEMA with the missing field name
    And the count of SCHEMA failures for that agent on the business date rises by one

  Scenario: AC-P10-004 A model that does not answer inside 60 seconds does not block the case
    Given the model stub does not answer for 61 seconds
    When the orchestrator runs the agent for case "RW-2026-000102"
    Then the call is ended at the timeout on the policy row
    And the agent run holds status TIMED_OUT, fallback true and the measured latency
    And the orchestrator returns the rule result with reason TIMED_OUT
    And the case is still able to route

  Scenario: AC-P10-005 Prompt versions take effect on their own date
    Given prompt version "PR1" is in force for the agent
    When version "PR2" is loaded and approved with valid from 2026-11-20
    Then version "PR2" exists with status APPROVED
    And version "PR1" stays readable with its text hash unchanged
    And a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2"

  Scenario: AC-P10-006 A configuration that fails a check is refused, and a loader cannot approve their own version
    Given a policy row with timeout_seconds 0
    When it is loaded
    Then the load is refused and the failed check is named
    And the version in force stays in force and no new version row exists
    Given a policy version loaded by one user
    When the same user approves it
    Then the approval is refused and the version keeps status LOADED

  Scenario: AC-P10-007 A shadow run changes nothing
    Given 200 cases created between 2026-11-30 and 2026-12-04 and the policy in mode SHADOW
    When the agent runs on each CaseCreated event
    Then 200 agent runs with mode SHADOW store a summary and gap flags
    And no case field, task, queue, route state or decision changes
    And no user-facing endpoint returns the answer

  Scenario: AC-P10-008 The evaluation scores an agent and proposes a threshold
    Given a labeled sample version and the reviewers' answers for the same cases
    When the comparison runs
    Then one score row per label key or field holds the agreement rate, the precision, the recall and the sample size
    And each score row holds the policy, the prompt and the model version
    And the extraction proposal names the approach with the highest mean F1 and the lowest confidence at which every chosen field reaches precision 0.95
    And a type below the minimum labeled sample is marked insufficient sample with no proposal

  Scenario: AC-P10-009 An evaluation that cannot be run or reported is refused
    Given a sample with 0 labeled rows for the agent
    When the evaluation is started
    Then the request is refused and no evaluation run and no agent run row exist
    Given an evaluation of the same agent, sample and version is RUNNING
    When it is started again, or its report is requested
    Then the request is refused and the running evaluation is unchanged

  Scenario: AC-P10-010 The monitor shows every agent by version
    Given two agents in shadow and one agent with no run on 2026-12-01
    When the screen opens for 2026-12-01
    Then each agent shows runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score by policy and prompt version
    And acceptance and override show that no run of that agent is at L1

  Scenario: AC-P10-011 A cost cap alerts once per day
    Given the cost of one agent above its daily parameter
    When the daily aggregation completes for 2026-12-01
    Then one alert row exists for that agent, type COST_CAP, with the measured value and the threshold
    And one notification reaches the holders of the centre-of-excellence and model-risk roles
    And a rerun of the same date creates no second measure row, alert row or notification

  Scenario: AC-P10-012 A verdict is recorded, an override needs a reason, and a failed record stops both
    Given an agent answer and a person reviewing it
    When the person rejects it with a coded reason
    Then one feedback row holds the run, the verdict, the reason, the role and the time
    When the person rejects it with no coded reason
    Then the request is refused and no feedback row exists
    Given the decision log writer fails
    When the person accepts the answer
    Then the request fails, no feedback row exists, and the controls stay on the panel

  Scenario: AC-P10-013 An autonomy step needs evidence and a second pair of eyes
    Given a policy version in mode L1 naming an evaluation run, its conditions and the measures to watch
    When the version is loaded and approved by a different user
    Then the version is stored with status LOADED and takes effect on its valid-from date
    And the previous version stays in force until then
    When a condition of the evaluation is not met
    Then the step is refused and the previous version stays in force

  Scenario: AC-P10-014 Drift raises a decision with an owner and a date
    Given a drift threshold and a minimum feedback on the policy row
    When a segment has fewer feedback entries than the minimum
    Then no drift alert is raised and the screen says that there is not enough feedback
    When a breach is measured with enough feedback
    Then a decision is raised with an owner and a date
    And the lower mode may be proposed with the approval that change needs

  Scenario: AC-P10-015 The TDR suggestion is served, recorded and refused when it cannot be
    Given the model deployed with a policy in mode L1 for a restructure treatment
    When the treatment service asks for a suggestion
    Then the suggestion returns with the installments and the model version
    And one decision log entry holds decision D5, the model version and the inputs reference
    When the same treatment asks again
    Then the first suggestion and its entry return and no second model call is made
    When the mode is OFF, the treatment is not a restructure, the model is unavailable or the record cannot be written
    Then no suggestion returns and the caller receives the message the source names

  Scenario: AC-P10-016 The service crosses no boundary and holds no personal data
    Given the code, the migrations and the tool list of the service
    When the boundary and privacy checks run
    Then no statement reads an ACE view, a public table or another service's table
    And no tool writes to another service and no grant exists on the recovery schema or on another service schema
    And every call runs under the service identity with the role checks of the acting role
    And no prompt body, run payload, event, workflow input or log carries a name, an address, an identity number or document content

  Scenario: AC-P10-017 Champion and challenger compares without changing what is in force
    Given two rule or model versions and one sample
    When the comparison runs
    Then both versions are scored on the same sample
    And the comparison presents the outcome, the cost and the latency of each
    And the version in force is unchanged
    And the committee pack holds the performance, the override rate, the fallbacks and the incidents of the period
```

### 11.1 Criterion to requirement mapping

| AC | FR and NFR | Origin in the source |
|---|---|---|
| AC-P10-001 | FR-P10-001, FR-P10-024; NFR-P10-006, NFR-P10-008 | FSD P10 v3 AC-P10-001-01; Arch v5 slides 16 and 43 |
| AC-P10-002 | FR-P10-002; NFR-P10-016 | FSD P10 v3 AC-EXC-P10-001-04 |
| AC-P10-003 | FR-P10-003; NFR-P10-007 | FSD P10 v3 AC-ALT-P10-001-02 |
| AC-P10-004 | FR-P10-004; NFR-P10-001, NFR-P10-002 | FSD P10 v3 AC-EXC-P10-001-01; R-UNI-32 |
| AC-P10-005 | FR-P10-005; NFR-P10-011 | FSD P10 v3 AC-ALT-P10-001-01 |
| AC-P10-006 | FR-P10-006, FR-P10-019 | FSD P10 v3 AC-EXC-P10-001-02, AC-EXC-P10-001-03 |
| AC-P10-007 | FR-P10-007, FR-P10-012, FR-P10-014; NFR-P10-006 | FSD P10 v3 AC-P10-003-01, AC-P10-008-01, AC-P10-009-01 |
| AC-P10-008 | FR-P10-008, FR-P10-009, FR-P10-010 | FSD P10 v3 AC-P10-004-01, AC-ALT-P10-003-01, AC-ALT-P10-004-01 |
| AC-P10-009 | FR-P10-010, FR-P10-011 | FSD P10 v3 AC-EXC-P10-001-05, AC-EXC-P10-001-06, AC-ALT-P10-007-02 |
| AC-P10-010 | FR-P10-016; NFR-P10-008, NFR-P10-015 | FSD P10 v3 AC-P10-006-01, AC-EXC-P10-006-02 |
| AC-P10-011 | FR-P10-017; NFR-P10-009 | FSD P10 v3 AC-ALT-P10-006-01, AC-ALT-P10-006-02, AC-EXC-P10-006-03 |
| AC-P10-012 | FR-P10-018, FR-P10-026; NFR-P10-011 | FSD P10 v3 AC-EXC-P10-007-02, AC-EXC-P10-008-02; REQ-APD-005 |
| AC-P10-013 | FR-P10-019, FR-P10-021; NFR-P10-016 | FSD P10 v3 AC-ALT-P10-007-01, AC-ALT-P10-009-02; BR-084 |
| AC-P10-014 | FR-P10-020; NFR-P10-009 | FSD P10 v3 AC-EXC-P10-006-04; BRD Epics 3 to 8 v1 BR-015 |
| AC-P10-015 | FR-P10-015, FR-P10-026; NFR-P10-003 | FSD P10 v3 AC-P10-010-01 to AC-EXC-P10-010-05 |
| AC-P10-016 | FR-P10-024, FR-P10-025; NFR-P10-004, NFR-P10-006 | Arch v5 slides 16, 29 and 35; DP-05, DP-11; NFR-039, NFR-040, NFR-051, NFR-055 |
| AC-P10-017 | FR-P10-022, FR-P10-023; NFR-P10-008 | FSD P10 v3 A2.14, A2.16; BRD Epics 3 to 8 v1 BR-081, BR-084 |

### 11.2 Validation evidence required before a capability is called done

| Evidence | What it shows |
|---|---|
| Contract test of the run request, the tool gateway and AgentRunCompleted | The manifest, the outcome, the fallback flag and the no-personal-data rule hold |
| Contract test of the consumed contracts against their fakes | The service builds and is tested without rwb-case, rwb-document, rwb-source-data or the model endpoint being finished |
| Boundary test | No ACE view, no cross-schema statement, no foreign key out of the schema, no write tool, no transfer call outside the one gateway |
| Guardrail test | The schema check, the allowed tool list and the confidence floor reject and fall back with the check code recorded |
| Fallback test | The timeout ends the call, the rule result is returned and the case still routes |
| Shadow test | A shadow run writes the run row and changes nothing else, and no endpoint returns the answer |
| Evaluation test | A score per label key, the precision and recall, the threshold proposal and the refusal of an empty or concurrent evaluation |
| Governance test | A policy load, a four-eyes approval, an autonomy step on evidence, a drift breach with an owner and a date |
| Privacy test | No personal data in a prompt body, a run payload, an event, a workflow input or a log, and masking applied before the call |
| Operations evidence | A run book entry, a dashboard and a cost and drift alert per agent |
| Audit evidence | Any answer reproduced from the run record for a named case population |

## 12. Open questions

Questions carried forward from the BRD, plus product-level questions this PRD raises. No answer is invented.

| ID | Question | Owner | Needed by | Impact if unanswered |
|---|---|---|---|---|
| Q-P10-01 | What targets apply to agent acceptance, override rate, latency and cost? The BRD carries no target per agent (BRD Epics 3 to 8 v1 KPI-012 and Q-026; GAP-1523) | Risk and model risk officer | Before the wave-2 release | The dashboard reports a number with nothing to judge it against and the fallback target stays the only measure |
| Q-P10-02 | What measured evidence and threshold justify raising or lowering an agent autonomy level? The BRD leaves Q-014 open (GAP-1523) | Risk and model risk officer | Before the wave-2 release | An autonomy change cannot be approved on evidence and the agent stays in shadow |
| Q-P10-03 | How does the E3 autonomy change depend on the E8 administration screen, and which screen serves the change in wave 2? The BRD leaves Q-017 open and assumes the E1 configuration path serves it | Solution architect with the centre of excellence | Before the wave-2 release | An autonomy change has no screen and the path is a manual load |
| Q-P10-04 | Which fields are masked before they enter a prompt, per agent and per role? DL26 is open | Compliance with the data office | Before the wave-2 release | An unmasked field in a prompt is a reportable breach |
| Q-P10-05 | How long are a run, a guardrail result, a feedback row, a sample and an evaluation kept? DL26 is open (GAP-1524) | Compliance | Before the wave-1 release | A purge before the case closes destroys the evidence of an answer |
| Q-P10-06 | May an agent ever call a write tool, or is the tool gateway permanently read-only? The source set states read-only calls and also an allowed action list (GAP-1528) | Solution architect with the model risk officer | Before the wave-2 release | An agent either cannot act at all or acts without a stated limit |
| Q-P10-07 | What does the regulator expect to see of a prompt text and a model output, and for how long? No source states it beyond the decision log rules | Compliance with Legal | Before the first production release | A retention or a disclosure gap against the BOT AI risk guidelines |
| Q-P10-08 | Which screen and which message shows that no TDR suggestion is available, given that the treatment screen is S2's and the fallback wording is not in the source set (GAP-1521; GAP-1531) | Product owner with the S2 owner | Before the wave-2 release | A user sees an empty field and cannot tell an unavailable model from a treatment that does not qualify |

## 13. Approval

| Role | Name | Decision | Date | Signature |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

Approval is open. The BRD carries no approval record and no status field (GAP-1526; ASM-2637), so this PRD is issued as Draft and the requirements approval gate is not evidenced.

## Appendix A. Traceability summary

The master matrix `requirement/Traceability_Matrix.md` in the AI-SDLC workspace is assembler-owned; the rows this PRD contributes are below.

| BR ID | CAP | FR and NFR | AC |
|---|---|---|---|
| REQ-CWC-017 | CAP-P10-004, CAP-P10-011 | FR-P10-007, FR-P10-012, FR-P10-015 | AC-P10-007, AC-P10-015 |
| REQ-CWC-018 | CAP-P10-001, CAP-P10-002 | FR-P10-003, FR-P10-024, FR-P10-025 | AC-P10-003, AC-P10-016 |
| REQ-CWC-019 | CAP-P10-004, CAP-P10-008 | FR-P10-007, FR-P10-019 | AC-P10-007, AC-P10-013 |
| REQ-DCM-005 | CAP-P10-004, CAP-P10-006 | FR-P10-009, FR-P10-013 | AC-P10-008 |
| REQ-DCM-006 | CAP-P10-006 | FR-P10-009 | AC-P10-008 |
| REQ-DCM-011 | CAP-P10-004 | FR-P10-012, FR-P10-014 | AC-P10-007 |
| REQ-DRI-001 | CAP-P10-001, CAP-P10-003, CAP-P10-006, CAP-P10-011 | FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-010, FR-P10-015 | AC-P10-001, AC-P10-002, AC-P10-004, AC-P10-008, AC-P10-009, AC-P10-015 |
| REQ-DRI-005 | CAP-P10-002, CAP-P10-010, CAP-P10-011 | FR-P10-018, FR-P10-026 | AC-P10-012, AC-P10-015 |
| REQ-APD-005 | CAP-P10-010 | FR-P10-018 | AC-P10-012 |
| REQ-ACA-005 | CAP-P10-001 | FR-P10-024; NFR-P10-006 | AC-P10-016 |
| REQ-ACA-010 | CAP-P10-001, CAP-P10-002 | FR-P10-003, FR-P10-024; NFR-P10-004 | AC-P10-003, AC-P10-016 |
| REQ-CHO-006 | CAP-P10-011 | FR-P10-015 | AC-P10-015 |
| REQ-DVH-001 | CAP-P10-004 | FR-P10-013 | AC-P10-007 |
| BR-015 | CAP-P10-005, CAP-P10-008 | FR-P10-005, FR-P10-006, FR-P10-019, FR-P10-020 | AC-P10-005, AC-P10-006, AC-P10-013, AC-P10-014 |
| BR-081 | CAP-P10-001, CAP-P10-009 | FR-P10-023, FR-P10-025 | AC-P10-016, AC-P10-017 |
| BR-084 | CAP-P10-006, CAP-P10-007, CAP-P10-008, CAP-P10-009 | FR-P10-008, FR-P10-010, FR-P10-016, FR-P10-017, FR-P10-021, FR-P10-022, FR-P10-023 | AC-P10-008, AC-P10-010, AC-P10-011, AC-P10-013, AC-P10-017 |
| NFR-008 | CAP-P10-007 | NFR-P10-015 | AC-P10-010 |
| NFR-010, NFR-024 | CAP-P10-003 | NFR-P10-001, NFR-P10-002 | AC-P10-004 |
| NFR-020, NFR-021 | All | NFR-P10-010 | AC-P10-001 |
| NFR-027 | All | NFR-P10-016 | AC-P10-002, AC-P10-013 |
| NFR-030, NFR-036 | CAP-P10-001, CAP-P10-006, CAP-P10-010 | NFR-P10-012, NFR-P10-017 | AC-P10-012 |
| NFR-033, NFR-034 | CAP-P10-001, CAP-P10-005 | NFR-P10-011 | AC-P10-005, AC-P10-012 |
| NFR-039, NFR-040 | CAP-P10-001 | NFR-P10-006 | AC-P10-016 |
| NFR-045, NFR-046, NFR-047 | All | NFR-P10-013, NFR-P10-014 | AC-P10-016 |
| NFR-048 | CAP-P10-001, CAP-P10-011 | NFR-P10-003 | AC-P10-001, AC-P10-015 |
| NFR-051, NFR-052, NFR-053 | CAP-P10-001 | NFR-P10-004, NFR-P10-005, NFR-P10-006 | AC-P10-016 |
| NFR-055 | CAP-P10-002 | NFR-P10-007 | AC-P10-003 |
| NFR-064, NFR-066 | CAP-P10-007 | NFR-P10-008 | AC-P10-001, AC-P10-010, AC-P10-017 |
| NFR-067, NFR-068 | CAP-P10-007, CAP-P10-008 | NFR-P10-009 | AC-P10-011, AC-P10-014 |

### A.1 Business requirement coverage

| BR ID | FR count | Status |
|---|---|---|
| REQ-CWC-017 | 3 | Covered |
| REQ-CWC-018 | 3 | Covered |
| REQ-CWC-019 | 2 | Covered |
| REQ-DCM-005 | 2 | Covered |
| REQ-DCM-006 | 1 | Covered |
| REQ-DCM-011 | 2 | Covered |
| REQ-DRI-001 | 6 | Covered |
| REQ-DRI-005 | 2 | Covered |
| REQ-APD-005 | 1 | Covered |
| REQ-ACA-005 | 1 | Covered |
| REQ-ACA-010 | 2 | Covered |
| REQ-CHO-006 | 1 | Covered |
| REQ-DVH-001 | 1 | Covered |
| BR-015 | 4 | Covered |
| BR-081 | 2 | Covered |
| BR-084 | 7 | Covered |

No P10 business requirement of the BRD is without a functional requirement. Two obligations are carried without a requirement of their own and are named here so the gap is not read as an omission:

- REQ-CWC-020 (a model or agent write and a rule-allocated case share one queue and one ordering) is P3 rwb-case's: this PRD requires only that the agent's proposal reaches the queue through that owner's contract and in that owner's order (FR-P10-007).
- KPI-012 of the epic BRD (agent acceptance, override, latency and cost measured and reported) is delivered as NFR-P10-008 and FR-P10-016 with no BR ID, because the BRD carries it as a measure and not as a business requirement; its target is open under Q-P10-01.
