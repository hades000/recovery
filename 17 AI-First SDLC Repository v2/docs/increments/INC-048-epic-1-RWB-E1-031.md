# Increment Card — INC-048-epic-1-RWB-E1-031

**RWB-E1-031 — Queue and owner on the case list with filters**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-048` |
| Title | Queue and owner on the case list with filters |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-031` |
| RUN_ID | `INC-048-epic-1-RWB-E1-031` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 48 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-020, RWB-E1-039 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **the queue and owner columns on the case list, with filters by queue, team and status and an export to Excel**, so that **I see my queues and who owns each case without a new screen**.

**Business outcome:** Today a team manager asks each collector for their list to know who holds which case. With allocation by rule (RWB-E1-020), every case has a queue and an owner; this story shows both on the case list, filters by queue, team and status inside the manager's scope, and exports the filtered list with the export written to the access log for PDPA. It meets REQ-CWC-007 (the result of allocation is visible) and REQ-ACA-009 (a user sees only the cases their scope allows).

**Main flow:**
1. Team manager: opens SCR-02 Case list; the screen shows the Loading state.
2. CaseListPage: calls GET /cases with page 0 and size 50; the service applies the caller's scope.
3. CaseListPage: shows each row with case number, product, status, stage, queue, owner and entry date (list state).
4. Team manager: picks queue "DIL-BKK-CO", team "DIL-BKK" and status "ASSIGNED"; the page calls GET /cases with the filters (filtered state).
5. CaseQueryService: returns only cases inside the caller's scope that meet every filter, with the total.
6. Team manager: chooses Export.

**Acceptance criteria:**
- AC1: Filter by queue
- AC2: Export
- AC3: No case meets the filters
- AC4: Export above the limit
- AC5: Access log unavailable
- AC6: Queue outside the scope
- AC7: A case with no owner
- AC8: Export at the limit

**Out of scope:**
- My queue and team queue screens (RWB-E2-011, SCR-07 in Epic 2).
- The base case list with filters by product, stage, age and deviation (RWB-E1-002, FEAT-RDF-18).
- The masking rules themselves (RWB-E1-037, DL26).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-031-queue-and-owner-on-the-case-list-with-filters-v1.md` |
| Requirement IDs | REQ-CWC-007, REQ-ACA-009 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.4; Business Requirements Program, sections 5.3 and 5.4 |
| Decision | None |
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
| RW-TEAMMGR | Lists, filters and exports cases in team scope (Case record R) |
| RW-CASEOWN | Lists and exports their own cases (Case record R, scope Own) |
| Every role with Case record R | Lists cases in its scope |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| RW-COMPLY | Reads the access log entries for exports |

## Contract extract

**GET /api/recovery/v1/cases** | Item | Value | |---|---| | Request | Query queue (uuid), status, owner, product, stage, page, size, sort; new query parameter team (see additions) | | Response | CasePage: items (Case with caseNo, productGroup, status, stageCode, queueId, ownerUserId, teamCode, entryDate), page, size, total | | Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 503 | | Authorization | Case record, right R, scope applied | | Idempotency | Not applicable | **GET /cases/export** (new endpoint, see additions) | Item | Value | |---|---| | Request | The same query parameters as GET /cases, without page and size | | Response | 200 application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | | Errors | 401; 403 no Case record R (MSG-P4-002); 422 above the row limit (MSG-P3-021); 503 access log unavailable (MSG-P7-003) | | Authorization | Case record, right R, s…

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

- No business value in code: the export limit and the lists come from data. - No personal data in logs, tests or prompts; the export applies masking by role and holds no customer name or ID number. - No read of another module's tables: the access log is written through AccessEventPublisher (P4); owner names come from the ACE user directory interface. - The export is never made when its access log entry cannot be written.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-031-queue-and-owner-on-the-case-list-with-filters-v1.md` |
| Specification | `output/INC-048-epic-1-RWB-E1-031/specify/spec.md` |
| Compliance validation | `output/INC-048-epic-1-RWB-E1-031/specify/compliance-validation.md` |
| Agent run log | `output/INC-048-epic-1-RWB-E1-031/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-048-epic-1-RWB-E1-031/plan/` |
| Implementation evidence | `output/INC-048-epic-1-RWB-E1-031/implement/` |
| API / functional test reports | `output/INC-048-epic-1-RWB-E1-031/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-048-epic-1-RWB-E1-031/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-031-queue-and-owner-on-the-case-list-with-filters-v1.md` |
| Output run | `output/INC-048-epic-1-RWB-E1-031/` |

