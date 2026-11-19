# Increment Card — INC-034-epic-1-RWB-E1-070

**RWB-E1-070 — Temporal platform on the ACE AKS clusters**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-034` |
| Title | Temporal platform on the ACE AKS clusters |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-070` |
| RUN_ID | `INC-034-epic-1-RWB-E1-070` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 34 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-044, RWB-E1-056, RWB-E1-022 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **a Temporal cluster per environment on the ACE AKS clusters, with its own persistence databases, the rwb-recovery namespace, mTLS and the Web UI behind Entra SSO**, so that **case workflows from Epic 3 have a durable engine that SCB IT runs like the rest of ACE**.

**Business outcome:** Case workflow begins in Epic 3, and a durable engine must exist before the first case workflow is written. ADR-011 replaces ADR-003 (DT09, DT10): Temporal runs the case lifecycle, while case data remains the system of record in the ACE DB recovery schema. If the engine is installed without its own database, identity, certificates and run book, Epic 3 builds on a shared service that nobody owns and a restart becomes a developer task.

**Main flow:**
1. Platform administrator: deploys Helm release rwb-temporal into the ACE namespace of DEV, then SIT, from the values file; the chart runs frontend, history, matching, internal-worker and web.
2. TemporalSchemaJob: creates the databases temporal and temporal_visibility owned by temporal_svc, then runs the Temporal schema tool at the pinned server version; a second run changes nothing.
3. NamespaceBootstrapJob: registers the namespace rwb-recovery with retention 30 days and the Keyword search attributes CaseId, Stage, ProductGroup and QueueCode; a second run changes nothing.
4. Platform administrator: binds the mTLS certificate and key from Key Vault to the frontend and the workers through the CSI driver; the certificate is issued by the ACE internal CA and names the namespace.
5. Platform administrator: configures the Web UI with Entra ID OIDC; the app roles map RW-PLATADM to operate and RW-AUDIT to read; any other role is refused.
6. Platform administrator: turns on the metrics scrape to the ACE monitoring stack and imports the platform dashboard.

**Acceptance criteria:**
- AC1: Cluster healthy
- AC2: Separate database grants
- AC3: mTLS enforced
- AC4: Web UI roles
- AC5: Namespace settings
- AC6: Frontend restart loses no workflow
- AC7: Run book with the eight headings

**Out of scope:**
- Case workflows (Epic 3) and the worker (RWB-E1-071).
- Workflow-level alerts, the stuck workflow scanner and the workflow dashboard (RWB-E2-037).
- The codec server, decode and the Temporal admin audit (RWB-E2-038).
- Backup, point-in-time restore, zone failover, upgrade procedure and archive (RWB-E2-039).
- The ace-collection namespace and the ACE team's own Temporal use.
- Workbench screens and the admin console (Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-070-temporal-platform-on-the-ace-aks-clusters-v1.md` |
| Requirement IDs | REQ-DRI-007, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, sections 5.1 and 5.2 |
| Decision | D-RCV-36 (T1); ADR-011 |
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
| RW-PLATADM | Installs and upgrades the release, runs the namespace bootstrap, reads the database grants, operates the Web UI and restarts a service (Platform administration, U) |
| RW-AUDIT | Reads the namespace and workflow history in the Web UI (Platform administration, R) |
| RW-SECADM | Reads the certificate and OIDC configuration; decode through the codec server is RWB-E2-038, not this story |
| RW-CASEOWN and every other Workbench role | No Web UI access; a sign-in is refused with MSG-P4-002 |
| SY-CASEWF | Connects to the frontend as the worker with its own client certificate; no Web UI account |
| SY-RULES | Runs the Drools evaluator inside the recovery module and does not connect to Temporal directly |
| RW-TRIBE | Maintains the Helm values and the run book through the change process; may not deploy to PROD |
| No delegation of authority level applies | A platform deployment is not a credit decision |

## Contract extract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The platform interfaces are internal to the ACE network. | Interface | Method | Request | Response | Errors | Authorization | Idempotency | |---|---|---|---|---|---|---| | Temporal frontend | gRPC over mTLS, port 7233: StartWorkflowExecution, SignalWorkflowExecution, DescribeWorkflowExecution | namespace rwb-recovery, workflow type, workflow ID, task queue, encrypted input | workflow ID and run ID | TLS handshake failure; NOT_FOUND namespace; PERMISSION_DENIED; FAILED_PRECONDITION | Client certificate from the ACE internal CA with the namespace claim | Workflow ID is the idempotency key; a repeated start with the same ID returns the running execution | | Temporal Web UI | HTTPS 443: HTTP GET and POST through the internal ingress (OIDC sign-in and UI pages) | Entra ID OIDC authorization code flow | namespace and workf…

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

- No business value in code: replica counts, retention, node sizes and versions are Helm values or parameters. - No personal data in logs, tests, workflow history or prompts: search attributes hold case codes and queue codes only; the smoke payload is synthetic. - No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no recovery or ACE table. - Temporal persistence is never placed in the ACE database, and the recovery schema is never granted to temporal_svc. - No Web UI account for a role other than RW-PLATADM and RW-AUDIT; no shared operator account. - No clear personal data in the Temporal payload; the codec is RWB-E1-071. - No mTLS bypass in DEV or SIT; a test that needs a certificate uses a certificate from the test CA.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-070-temporal-platform-on-the-ace-aks-clusters-v1.md` |
| Specification | `output/INC-034-epic-1-RWB-E1-070/specify/spec.md` |
| Compliance validation | `output/INC-034-epic-1-RWB-E1-070/specify/compliance-validation.md` |
| Agent run log | `output/INC-034-epic-1-RWB-E1-070/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-034-epic-1-RWB-E1-070/plan/` |
| Implementation evidence | `output/INC-034-epic-1-RWB-E1-070/implement/` |
| API / functional test reports | `output/INC-034-epic-1-RWB-E1-070/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-034-epic-1-RWB-E1-070/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-070-temporal-platform-on-the-ace-aks-clusters-v1.md` |
| Output run | `output/INC-034-epic-1-RWB-E1-070/` |

