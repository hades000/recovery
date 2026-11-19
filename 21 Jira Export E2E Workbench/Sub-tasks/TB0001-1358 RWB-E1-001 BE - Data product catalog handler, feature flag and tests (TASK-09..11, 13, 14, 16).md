# TB0001-1358 [RWB-E1-001] BE - Data product catalog handler, feature flag and tests (TASK-09..11, 13, 14, 16)

| Field | Value |
|---|---|
| Jira | [TB0001-1358](https://scbjira.atlassian.net/browse/TB0001-1358) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1163 |
| Epic link | - |
| Assignee | - |
| Reporter | PREMMAST SUWANNIKOM |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1; Delivery Workbench Q4S2 Squad1 |
| Team | RWB_SQ1 |
| Created | 2026-11-11T16:11:42.160+0700 |
| Updated | 2026-11-18T09:17:03.604+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

h2. Scope

Implementation Builder work for RWB-E1-001, parent [TB0001-1163|https://scbjira.atlassian.net/browse/TB0001-1163]. This sub-task carries TASK-RWB-E1-001-09, -10, -11, -13, -14 and -16 of the approved plan.

Canonical plan: {{output/INC-010-epic-1-RWB-E1-001/plan/plan.md}}, {{tasks.md}}, {{contracts/backend-apis.json}}, {{tests/scenarios.md}}.

h2. Readiness — NOT READY, waiting on one card

||Precondition||State||Card||
|*PRE-7*|*Not met.* RWB-E1-043's reference load service and the {{ReferenceTableHandler}} Java file are not implemented. {{output/INC-009-epic-1-RWB-E1-043/}} holds {{specify/}} and {{plan/}} only.|[TB0001-1344|https://scbjira.atlassian.net/browse/TB0001-1344]|
|*PRE-8*|*Met by D-RCV-58, acknowledged 2026-11-11* — see below.|—|

This sub-task waits on {{TB0001-1344}} alone.

h2. PRE-8 — settled by D-RCV-58

OPEN-035 said {{ReferenceTableHandler}} had no owning specification and asked for the RWB-E1-043 specification to be re-run. That would not have worked: the type appears *nowhere* in the RWB-E1-043 story file or in its output. That story has the P4 load handler call {{ReferenceVersionRegistry.recordVersion(...)}} directly, and its §12 publishes {{ReferenceVersionRegistry}} and {{ReferenceDataService}} only.

The attribution is circular. RWB-E1-001 §12 line 244 calls the type a "published interface of P4 that P1 implements, *from RWB-E1-043*", while {{recovery-workbench-build-notes-epic-1-v4.md}} line 291 says {{TrackerInventoryHandler}} "implements the ReferenceTableHandler interface *whose signature comes from RWB-E1-001*". Only RWB-E1-001 §12 writes the signature out, so the build notes settle it against our own story.

*D-RCV-58:* the INC-010 specification is the contract of record and publishes the three signatures, quoted verbatim from story §12 and not invented; RWB-E1-043 still declares the Java file in {{recovery.casewf.refdata.api}}.

* {{String tableCode()}}
* {{ValidationReport validate(ReferenceLoadFile file)}}
* {{int apply(UUID loadId, ReferenceLoadFile file, LocalDate validFrom)}}

*Acknowledged 2026-11-11 17:20 +0700.* Jesniphat Pukkham merged MR !29 into {{main}} himself (merge commit {{09909a4}}), and that merge request's description stated the decision and named both halves he could overrule. He gave no separate written ruling, and nothing here claims one. He may still revisit either half; because the signature is quoted from a BA source, that would change who writes the file, not what it says. RWB-E1-005 and RWB-E1-006 implement the same interface and follow if it ever moves.

TASK-01 still confirms these names and return types against the real type once RWB-E1-043 lands, and *reports any difference rather than adapting to it*.

h2. Tasks

||Task||Work||
|TASK-09|{{DataProductCatalogHandler implements ReferenceTableHandler}}, {{tableCode()}} returns {{"data_product"}} — unprefixed, it is the load's business key, not an object name. {{validate}} checks the whole file and returns every failure in one {{ValidationReport}}, writing nothing: exactly the 14 codes DP01–DP14 or *MSG-P1-004* naming the missing products; exactly one non-empty {{system_of_record}} with no list separator and a non-empty {{owner_user_id}} or *MSG-P1-003* naming the product; {{owner_role}} in LOV-ROLE and {{refresh_cycle}} in LOV-REFRESH or *MSG-P1-007* with the 1-based row, the field and the allowed values; each of {{product_name}}, {{definition}}, {{system_of_record}} within its column width. Any failure refuses the load in full with HTTP 422.|
|TASK-10|Apply: on a clean report and the data steward's confirmation, write all 14 rows with the load's {{validFrom}} in one transaction and return 14; a failure on any row rolls back every row. Content-hash idempotency and the version window belong to RWB-E1-043 and are *not* reimplemented — a repeat file is reported by that service with 409 MSG-P1-011.|
|TASK-11|Feature flag {{rwb.p1.data-catalog}} over the handler only: with the flag off the reference data service refuses a {{data_product}} load as an unknown table code, and the tables, dictionary and view are unaffected. Add MSG-P1-003, -004, -007 and -011 with English and Thai text per DL10; code and tests carry the message ID and its parameters, never the wording.|
|TASK-13|Backend unit tests TC-E1-001-07, -08, -09, -10, -12, -15. Positive, negative, boundary and error paths; synthetic fixtures only, no personal data.|
|TASK-14|{{recoveryCoverageVerification}} (D-RCV-06) over the changed recovery packages: 80% on lines, instructions, branches and methods, recorded as native JaCoCo figures. Backend only — no frontend file changes, so no frontend coverage task exists.|
|TASK-16|Boundaries, secrets and personal data: {{RecoveryBoundaryTest}} stays green; nothing reads or writes outside the {{rwb_}} object set, ACE core tables in the same schema included; no recovery module other than {{dataengine}} touches {{rwb_data_product}}, {{rwb_sys_objects}} or {{rwb_sys_fields}} directly. Scan migration, seed, fixtures and tests for credentials, connection strings and tokens. Confirm DEV and SIT owner user IDs are synthetic.|

h2. Dependency inside the story

TASK-09 needs the {{DataProduct}} entity and repository from [TB0001-1356|https://scbjira.atlassian.net/browse/TB0001-1356]. TASK-13's integration half and TASK-16's object-set check need the migration from [TB0001-1357|https://scbjira.atlassian.net/browse/TB0001-1357].

h2. Branch policy

D-RCV-50 as on the parent story. Unit-test mocks of the handler contract do not prove integration with the real reference load service.

## Linked issues

- is blocked by TB0001-1344: RWB-E1-043: Implementation Builder — reference data service with versioned tables (TASK-00..21) (To Do)

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-11 |
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
