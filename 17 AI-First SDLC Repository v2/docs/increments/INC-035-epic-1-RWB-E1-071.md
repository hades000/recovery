# Increment Card — INC-035-epic-1-RWB-E1-071

**RWB-E1-071 — Temporal worker and SDK in the recovery module**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-035` |
| Title | Temporal worker and SDK in the recovery module |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-071` |
| RUN_ID | `INC-035-epic-1-RWB-E1-071` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 35 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-070, RWB-E1-042, RWB-E1-047, RWB-TE-001 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **the recovery module to run a Temporal worker through the Spring Boot starter, with fixed task-queue and workflow-ID conventions, a PDPA payload codec and a smoke workflow**, so that **Epic 3 workflows plug into a worker that is already secure and observable**.

**Business outcome:** The Temporal cluster of RWB-E1-070 is only useful when a worker connects to it from the recovery module. Without one worker pattern, each Epic 3 squad would choose its own task queue, workflow ID, payload handling and start-up checks, and the first clear personal data in a workflow history would be found in production. This story gives the module one worker, one codec, one gateway and one smoke workflow, and it proves the path end to end before the first case workflow exists.

**Main flow:**
1. Application start: TemporalConfig reads temporal.target, temporal.namespace and temporal.taskqueue.platform through ParameterService; a missing value stops start-up with MSG-P3-032.
2. Application start: TemporalWorkerLifecycle reads rwb.p3.temporal; when it is on, it creates one worker on rwb-platform with the workflow and activity classes and the build ID from the pipeline.
3. Worker: connects to the frontend with its mTLS certificate and polls rwb-platform; when the flag is off, no worker and no poller are created.
4. PdpaPayloadCodec: registers as the data converter on the client and the worker; it encrypts every payload with AES-GCM and the Key Vault key, and it decrypts only inside the worker.
5. WorkflowGateway: starts and signals workflows by workflow ID; a start with an existing workflow ID returns the running execution and does not start a second run.
6. SmokeScheduleJob: Quartz runs daily at 06:00 and calls WorkflowGateway.start("PlatformSmokeWorkflow", "platform-smoke-{yyyymmdd}", input).

**Acceptance criteria:**
- AC1: Smoke workflow completes
- AC2: History holds encrypted payloads only
- AC3: Temporal unreachable
- AC4: Duplicate workflow ID
- AC5: Flag off
- AC6: Missing parameter at start-up
- AC7: Workflow class outside the package

**Out of scope:**
- Case workflows, case signals and the case task queue (Epic 3).
- The replay test gate, history export and build ID rollout (RWB-E2-040).
- Workflow alerts, the stuck workflow scanner and the workflow dashboard (RWB-E2-037).
- The codec server, decode and the Temporal admin audit (RWB-E2-038).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The reference case workflow skeleton (RWB-E2-043).
- The Temporal cluster, namespace, mTLS and Web UI (RWB-E1-070).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-071-temporal-worker-and-sdk-in-the-recovery-module-v1.md` |
| Requirement IDs | REQ-DRI-005, REQ-DRI-007, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, sections 5.1 and 5.2 |
| Decision | D-RCV-36 (T1, T2, T7); ADR-011 |
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
| RW-PLATADM | Runs the smoke workflow on demand, reads the worker health and the history (Platform administration, U) |
| RW-AUDIT | Reads the history and the decision log entry (Platform administration and Decision log, R) |
| RW-SECADM | Reads the codec configuration; decode through the codec server is RWB-E2-038, not this story |
| SY-CASEWF | The worker identity; connects with mTLS and writes the PLATFORM_SMOKE entry (Decision log C) |
| RW-COE | Reads the smoke result as a platform check (Platform administration, R) |
| RW-TRIBE | Builds and deploys the worker through the pipeline; has no PROD endpoint right |
| No delegation of authority level applies | A smoke run is not a credit decision |

## Contract extract

**POST /api/recovery/v1/admin/workflows/smoke** (P3 endpoint) | Item | Value | |---|---| | Request | Body optional: { workflowId: string }. Default platform-smoke-{yyyymmdd} in the server time zone | | Response | 200 WorkflowRun: workflowId, runId, workflowType, status, taskQueue, startedAt | | Errors | 401 (MSG-P4-001); 403 no Platform administration U (MSG-P4-002); 404 flag off; 409 the workflow ID already completed for the day (MSG-GEN-004); 503 Temporal unreachable (MSG-P3-036) | | Authorization | Platform administration, right U | | Idempotency | Workflow ID; a repeat while RUNNING returns the running execution, and a repeat after COMPLETED returns 409 with no second run | **Published interface WorkflowGateway** (package recovery.casewf.workflow, Epic 1): ```java public interface WorkflowGateway { String start(String workflowType, String workflowId, Object input); // returns the ru…

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

- No business value in code: the target, namespace, task queue, retention and flag are parameters. - No personal data in logs, tests, workflow history or prompts: every payload is encrypted; the test national ID is synthetic. - No read of another module's tables; ACE data only through recovery.v_ace_* views: the smoke workflow reads no case and no ACE row. - Workflow code is deterministic: no clock, random, I/O or Drools call in workflow code; all I/O is an activity. - The codec is the only payload path; no clear personal data is written to history, even in DEV. - No worker without a build ID and no start with a missing parameter. - No Temporal Schedule and no case wait on Quartz; the smoke job is the only Epic 1 workflow and it has no business wait.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-071-temporal-worker-and-sdk-in-the-recovery-module-v1.md` |
| Specification | `output/INC-035-epic-1-RWB-E1-071/specify/spec.md` |
| Compliance validation | `output/INC-035-epic-1-RWB-E1-071/specify/compliance-validation.md` |
| Agent run log | `output/INC-035-epic-1-RWB-E1-071/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-035-epic-1-RWB-E1-071/plan/` |
| Implementation evidence | `output/INC-035-epic-1-RWB-E1-071/implement/` |
| API / functional test reports | `output/INC-035-epic-1-RWB-E1-071/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-035-epic-1-RWB-E1-071/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-071-temporal-worker-and-sdk-in-the-recovery-module-v1.md` |
| Output run | `output/INC-035-epic-1-RWB-E1-071/` |

