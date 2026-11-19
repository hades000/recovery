# Increment Card — INC-052-epic-1-RWB-E1-021

**RWB-E1-021 — Transfer rules and engine v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-052` |
| Title | Transfer rules and engine v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-021` |
| RUN_ID | `INC-052-epic-1-RWB-E1-021` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 52 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-028, RWB-E1-020, RWB-E1-027, RWB-E1-072, RWB-E1-073 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **cases moved between queues and roles by the TRANSFER rule package on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason**, so that **hand-offs between teams run without email**.

**Business outcome:** A case changes hands between the TDR, litigation, NPA and debt sale teams by email today, and the case can wait between teams with nobody holding it. This story moves the case by rule when one of eight triggers fires, picks the owner in the receiving queue, ends the old assignment and records the rule ID and package version, and gives the team manager a programmatic transfer with a coded reason before the Epic 2 screens. It meets REQ-CWC-010 and REQ-CWC-016.

**Main flow:**
1. Event source: writes a trigger event to the outbox: CaseStateChanged for a stage change or a route decided (rule event ROUTE_APPROVED), TimerDue, DeviationRaised, DeviationCleared, ApprovalRequested, DocumentStored or PaymentMissed.
2. TransferListener: receives the event once per event ID; a repeated event ID is ignored (R-UNI-40), and builds one `TransferTrigger` fact for the event and the case snapshot.
3. RuleEvaluator (SY-RULES): calls `RuleEvaluator.evaluate("TRANSFER", trigger, businessDate)` for the `TransferTrigger` and returns the first matching rule in row order (T5), its rule ID and package version; no match means no transfer and no decision log entry.
4. TransferService: skips an automated transfer when legal_hold is true (R-UNI-20) and logs the skip.
5. TransferService: locks the case by its version, picks the owner in the target queue with AssignmentEngine, and checks the move is allowed from the case status.
6. TransferService: in one transaction ends the open assignment, writes the new assignment (reason TRANSFER and the rule ID), updates queue, team and owner, and writes CaseTransferred (EV-04).

**Acceptance criteria:**
- AC1: Rule-driven transfer
- AC2: Manual transfer
- AC3: One queue only
- AC5: Admin API
- AC6: Manual transfer without a reason
- AC7: Target owner at the cap
- AC8: Closed case
- AC9: Decision log unavailable
- AC10: Legal hold stops automated transfers
- AC11: A repeated event
- AC12: No owner below the cap in the target queue
- AC13: Hold on a case already on hold
- AC14: No rule matches

**Out of scope:**
- The transfer screen and queue history on the case (RWB-E2-012, RWB-E2-016).
- Reallocation when an owner leaves or passes the cap (Epic 2, R-UNI-18, R-UNI-19).
- Escalation of a breached timer without moving the case (RWB-E1-028).
- The route decision itself (Epic 4).
- From Epic 3 the trigger arrives as a Temporal signal (ADR-011), not from the outbox listener.
- Loading, validating, approving and rolling back the TRANSFER package (RWB-E1-073).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-021-transfer-rules-and-engine-v1-v2.md` |
| Requirement IDs | REQ-CWC-010, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| Decision | D-RCV-36; ADR-011; ADR-012 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR | Transfers and reassigns cases in team scope (Queue and allocation U) |
| RW-CAPACITY | Transfers cases (Queue and allocation U) |
| RW-LITOFF and other roles with Case record U | Place and lift a legal hold on a Legal or court instruction (Case record U) |
| RW-CASEOWN | Reads the case; may not transfer (Queue and allocation R) |
| SY-RULES | Evaluates package TRANSFER through `RuleEvaluator` |
| SY-CASEWF | Carries out rule transfers (Queue and allocation CRU) |
| SY-DECLOG | Writes the entries |

## Contract extract

**POST /api/recovery/v1/cases/{caseId}/transfer** | Item | Value | |---|---| | Request | TransferRequest: toOwnerId (uuid) or toQueueId (uuid), reasonCode = "MANUAL", note, and transferReasonCode (new field, LOV-TRANSFER-REASON) | | Response | 200 Assignment: id, caseId, assigneeUserId, assignedAt, reason, ruleId | | Errors | 401 (MSG-P4-001); 403 no Queue and allocation U (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 409 status does not allow the move (MSG-P3-005) or version changed (MSG-GEN-004); 422 no reason (MSG-P3-001), owner at cap (MSG-P3-002); 503 decision not recorded (MSG-P7-003) | | Authorization | Queue and allocation, right U, scope Team | | Idempotency | Idempotency-Key header; a repeat with the same key returns the first response | The manual transfer request, response, errors and authorization are unchanged by this rewrite. **POST /api/recovery/v1/cases/{cas…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: triggers, target queues and the reason list are data in the TRANSFER package and the list. - No personal data in logs, tests, workflow history or prompts. - No read of another module's tables; ACE data only through `recovery.v_ace_*` views: trigger events arrive through the outbox; the rule package comes through `RuleEvaluator` (RWB-E1-072). - One evaluator: TRANSFER is evaluated only through `RuleEvaluator`; no trigger list, row order or target queue is written in code (D-RCV-36 T3, T5). - The manual transfer API keeps its request, response, errors and authorization. - A transfer never resets the stage clock or the prescription date. - JOB-05 and the timer events stay on Quartz in Epic 1 and Epic 2 (D-RCV-36 T2); no case wait moves to Temporal in this story.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-021-transfer-rules-and-engine-v1-v2.md` |
| Specification | `output/INC-052-epic-1-RWB-E1-021/specify/spec.md` |
| Compliance validation | `output/INC-052-epic-1-RWB-E1-021/specify/compliance-validation.md` |
| Agent run log | `output/INC-052-epic-1-RWB-E1-021/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-052-epic-1-RWB-E1-021/plan/` |
| Implementation evidence | `output/INC-052-epic-1-RWB-E1-021/implement/` |
| API / functional test reports | `output/INC-052-epic-1-RWB-E1-021/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-052-epic-1-RWB-E1-021/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 13 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-021-transfer-rules-and-engine-v1-v2.md` |
| Output run | `output/INC-052-epic-1-RWB-E1-021/` |

