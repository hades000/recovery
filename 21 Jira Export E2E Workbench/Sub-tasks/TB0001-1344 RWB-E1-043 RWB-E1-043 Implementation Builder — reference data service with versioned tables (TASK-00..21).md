# TB0001-1344 RWB-E1-043: Implementation Builder — reference data service with versioned tables (TASK-00..21)

| Field | Value |
|---|---|
| Jira | [TB0001-1344](https://scbjira.atlassian.net/browse/TB0001-1344) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1204 |
| Epic link | - |
| Assignee | RACHATAPON PONGANANTAYOTIN |
| Reporter | pongpat.jantanon |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-10T16:56:56.893+0700 |
| Updated | 2026-11-16T15:39:30.871+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 2 |
| Comments | 1 |

## Description

h2. Scope
Implementation Builder work for RWB-E1-043 (Reference data service with versioned tables), parent [TB0001-1204|https://scbjira.atlassian.net/browse/TB0001-1204]. This existing sub-task tracks all 22 planned tasks TASK-RWB-E1-043-00 through -21; no duplicate Jira tasks are required by this update.

h2. Planning status — reconciled 2026-11-11
* *PLANNER_STATUS: SUCCESS* — planning complete; 22 unique tasks with an acyclic dependency graph; all 20 source logic-coverage rows mapped (9 BR, 10 AC, one grouped X1..X7 exception row).
* Spec clarification status: READY, 0 open spec clarification items. UI/design evidence: NOT_REQUIRED (UI In Scope: NO). API In Scope: YES.
* Mandatory Compliance Reviewer continuation REVIEW-RWB-E1-043-PLAN-002 initially returned FAIL with 1 Low correlation-propagation finding. Remediation in TASK-12/-13 and TC-03/-15 received targeted re-review *PASS*, REVIEW-RWB-E1-043-PLAN-002-001-RR-01, zero unresolved findings. Initial FAIL and historical review 001 remain preserved; no historical result is relabelled.
* Dependency-scope correction received mandatory bounded Compliance Reviewer *PASS*, REVIEW-RWB-E1-043-PLAN-003, Critical 0 / High 0 / Medium 0 / Low 0. This review covers the narrowed PRE-6 sequencing only; security acceptance and other gates remain unchanged.
* Planning completion is not implementation completion, executed test evidence, SIT approval or release approval. No implementation task is marked Done by this planning update.

h2. Canonical planning references
Workspace base: {{output/INC-009-epic-1-RWB-E1-043/plan/}}
* {{plan.md}}, {{tasks.md}}, {{data-model.md}}
* {{contracts/backend-apis.json}}, {{contracts/frontend-integrations.json}}, {{tests/scenarios.md}}
* Correlation review and targeted PASS: {{review/plan-gate-review-20261111.md}}
* Dependency-scope review PASS: {{review/plan-gate-review-20261111-dependency-scope.md}}
* Historical review: {{review/plan-gate-review.md}}
* Increment approvals/readiness: {{docs/increments/INC-009-epic-1-RWB-E1-043.md}}
* Traceability: {{requirement/Traceability_Matrix.md}}, section 10.
These are workspace paths, not a claim that the latest continuation has been committed or published.
Existing ticket provenance retained: planning branch {{plan/INC-009-e1-043-gates-7-8}}, MR !23 into {{main}} in ace-aisdlc. Its current merge/publish state was not verified in this update; it is not the ACE implementation branch policy below.

h2. Recorded human approvals — no duplicate approval request
* *PRE-1: bounded PO/BA story/task-update approval recorded.* Chitchaya Muanchonchana, 2026-11-11 09:27:13 +0700, [parent comment 1784557|https://scbjira.atlassian.net/browse/TB0001-1204?focusedCommentId=1784557]: "As an internal PO/BA TechX, Approved to update task follow the comments from Henka." Preserve that scope; do not infer blanket requirements/deployment/release approval. This supersedes this ticket's former claim that PO approval is still pending and the sole blocker.
* *PRE-2 / PRE-7 / PRE-8: approved.* Jesniphat Pukkham, 2026-11-10 16:33:53 +0700, [parent comment 1783867|https://scbjira.atlassian.net/browse/TB0001-1204?focusedCommentId=1783867], "Approve all.", following [gate request 1783397|https://scbjira.atlassian.net/browse/TB0001-1204?focusedCommentId=1783397]. This ticket already recorded PRE-2 design, PRE-7 plan and PRE-8 task approval; the approval comment is on the parent, not this sub-task.
* [Parent comment 1783253|https://scbjira.atlassian.net/browse/TB0001-1204?focusedCommentId=1783253] separately approves Option A: rollback 404 only for no matching version row; 422 for an existing non-APPROVED row; apply D-RCV-47/-48 now. It does not settle inferred rollback restoration mechanics/authority.

h2. Dependency-scope correction — 2026-11-11
* Source story {{Depends on}} lists *E1-042 and E1-044 only*. Its Independent criterion says "Needs only the migration tool (RWB-E1-044) and the configuration service (RWB-E1-042)."
* D-RCV-36 assigns {{RecoveryAccessGuard}}/common access check and sign-on/role ownership to E1-022; it does not require that entire story to finish before any E1-043 coding.
* The former blanket PRE-6 stop before all coding was a Planner inference and is withdrawn. Missing E1-022 does *not* fail TASK-01 or block independent migration/domain/service/cache/logger work or their isolated unit tests.
* PRE-6 remains a *protected API authorization integration/acceptance gate*. TASK-13, protected-HTTP portions of TASK-15/-16/-17 and final TASK-20/-21 cannot complete without actual shared authorization integration and method-security/session-derived identity/C/A/R/401/403 verification.
* No unsecured endpoint, fake production guard, permissive fallback or bypass. Isolated test mocks do not prove integrated authorization. Required tests must not be disabled or skipped to claim completion. Any unfinished code follows the existing feature-flag previous-path rule and is not completed authorization.
* Evidence: source story {{requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 043 Reference data service with versioned tables v1.md}}, Depends on / Independent; {{docs/decisions/INC-001-decisions.md}}, D-RCV-36; {{specify/spec.md}}, Authorization; REVIEW-RWB-E1-043-PLAN-003 PASS. No latest-remote absence or dependency completion is asserted.

h2. Implementation readiness and bounded stops
* *TASK-00:* verify the recorded approvals and review evidence; do not stop solely to request the same approvals again.
* *TASK-01 before coding:* verify actual start dependencies on refreshed {{develop-recovery}}: PRE-4 RWB-E1-044 Recovery Flyway configuration/history/settings; PRE-5 RWB-E1-042 published configuration/schema catalog/table codes/cache TTL and source-backed isolated synthetic prerequisites. Stop if these start prerequisites are missing; do not stub them or use a shared database.
* *TASK-01 PRE-6 inspection only:* record available shared guard/session/role contracts or the scoped API integration gap/owner. Closure of PRE-6 is not required to complete TASK-01 or start independent work; actual authorization is still required before affected API/test and story completion as above.
* *IMPL-NOTE-01 before rollback coding:* FDA/Technical Specifier must specifically confirm field-restoration mechanics, eligible predecessor and authority; record evidence and finalize TC-13 before TASK-09 and rollback portions of TASK-13/-17. General plan/task approval and the approved 404/422 rule are not that confirmation.
* *PRE-3 before SIT approval tests only:* verify RW-RISK Reference-data-A grant. This is not a blanket prerequisite for all coding or planning completion.

h2. Task register — planned scope, not executed completion
The full descriptions, trace IDs, BLOCKED_BY dependencies and verification commands remain authoritative in {{tasks.md}}. All build work transitively depends on TASK-00/-01. TASK-01 completion does not require E1-022 completion. Write applicable synthetic failing tests before production code; TASK-15..18 complete/verify those suites, not permission to write tests only afterwards. Dependencies on TASK-13 are completion dependencies, not a ban on earlier independent domain/unit work.

||Task ID (TASK-RWB-E1-043-)||Planned work||
|00|Verify recorded human gates, bounded approval scope and current review outcome; preserve review history.|
|01|Refresh integration baseline; verify Flyway/config/catalog start prerequisites and isolated synthetic fixtures; record authorization availability/gap without blocking independent work.|
|02|Add refdata package/API/internal skeleton inside existing recovery.casewf module.|
|03|Write migration tests first, then the next-sequence recovery migration with unqualified rwb_ tables, rwb_uq_ constraints, maker-checker and append-only guards.|
|04|JPA reference-version/reference-row entities and status mapping.|
|05|Internal repositories for version lookup, effective-date resolution, idempotency and rows.|
|06|Source-owned LOV-REF-TABLE/schema catalog resolution and unknown-table validation; no hardcoded business values.|
|07|Transactional load validation, content hash, idempotency and VALIDATED version/row persistence.|
|08|Maker-checker approval, concurrent approval handling and effective-version update.|
|09|Conditional rollback after IMPL-NOTE-01 confirmation; preserve approved distinct 404/422 error paths.|
|10|ReferenceDataService date-based APPROVED-version serving and no-version behavior; list support.|
|11|Reference row cache with source-owned TTL; never cache non-APPROVED versions.|
|12|Per-table/cycle version logging; restricted non-PII business payload plus separate shared correlation metadata.|
|13|Load/approve/list/conditional rollback controllers, method security, JSON/MSG contracts and shared X-Correlation-ID handling; actual shared authorization integration required before completion.|
|14|Run existing module-boundary/Modulith verification without weakening rules.|
|15|Load/schema/date/idempotency/empty-file unit and HTTP integration tests; protected-HTTP completion requires PRE-6.|
|16|Approval/concurrency and effective-version-resolution unit/integration tests; protected-HTTP completion requires PRE-6.|
|17|Conditional rollback, 404/422, logging and correlation propagation/isolation tests; protected-HTTP completion requires PRE-6.|
|18|Cache TTL and APPROVED-only behavior tests.|
|19|Verify feature-flag catalog entry and off-path compatibility; no engine-side wiring.|
|20|Tests, supported JaCoCo coverage gates, diff/module/privacy guardrails and evidence; cannot pass final acceptance with outstanding API authorization integration.|
|21|Implementation traceability, ACE branch/commit/MR evidence, readiness escalation and later-stage gate tracking; cannot declare story complete with outstanding PRE-6.|

h2. Applied planning feedback
[Comment 1784626|https://scbjira.atlassian.net/browse/TB0001-1344?focusedCommentId=1784626] is reflected in the planned migration/data model:
* {{rwb_uq_reference_version_table_version}}
* {{rwb_uq_reference_version_table_validfrom_hash}}
* {{rwb_uq_reference_row_version_key}}
The last pasted target ending {{_ke}} is treated as truncation of the original {{_key}}, preserving its meaning. This is a plan change, not evidence that a migration has run. Never edit an applied migration; use the next corrective migration with human disposition if needed.

h2. ACE implementation branch and verification policy
* D-RCV-50: {{feature/TB0001-1204-reference-data-versions}} from refreshed {{develop-recovery}}; story MR targets {{develop-recovery}}, batches target {{develop}}. No branch or MR was created by this planning update.
* Work remains inside recovery.casewf.refdata and the approved recovery migration/test paths; no other module internals, shared DB or new dependency.
* Backend tests required; planned coverage at least 80% for supported native JaCoCo LINE/INSTRUCTION/BRANCH/METHOD metrics. Unsupported statement/function metrics are explicitly N/A, not fabricated equivalents. Frontend NOT_APPLICABLE.
* No application tests/coverage have been executed or claimed passed by the planning continuation. API Tester is a later human-started stage.

h2. Next step
Human-initiated Implementation Builder, starting with TASK-00/-01. After PRE-4/-5 checks pass, independent work may proceed without waiting for E1-022 to finish. Retain the protected API authorization integration/acceptance gate, specific rollback coding stop and pre-SIT grant check. This ticket remains an implementation-tracking sub-task, not a completed implementation. Workflow status, assignee, priority and parent are unchanged by this update.

## Linked issues

- blocks TB0001-1358: [RWB-E1-001] BE - Data product catalog handler, feature flag and tests (TASK-09..11, 13, 14, 16) (To Do)
- blocks TB0001-1359: [RWB-E1-001] BE - Authorisation and release readiness (TASK-15, 17) (To Do)

## Comments (1)

### Comment 1: PREMMAST SUWANNIKOM, 2026-11-11T09:39:43.689+0700

Comment ID 1784626

From [https://scbjira.atlassian.net/browse/TB0001-1163?focusedCommentId=1784386|https://scbjira.atlassian.net/browse/TB0001-1163?focusedCommentId=1784386|smart-link] 

Please update the following uq_ name to rwb_uq

{{uq_reference_version_table_version        →  rwb_uq_reference_version_table_version uq_reference_version_table_validfrom_hash →  rwb_uq_reference_version_table_validfrom_hash uq_reference_row_version_key              →  rwb_uq_reference_row_version_ke}}


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| Actual Start Date | customfield_14457 | 2026-11-11 |
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-10 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
