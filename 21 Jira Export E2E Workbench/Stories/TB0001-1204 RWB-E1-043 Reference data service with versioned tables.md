# TB0001-1204 [RWB-E1-043] Reference data service with versioned tables

| Field | Value |
|---|---|
| Jira | [TB0001-1204](https://scbjira.atlassian.net/browse/TB0001-1204) |
| Type | Story |
| Status | Hold |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | RACHATAPON PONGANANTAYOTIN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:41.425+0700 |
| Updated | 2026-11-17T09:59:39.549+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 7 |
| Comments | 13 |

## Description

As a reference data administrator (RW-REFADM), I want products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority, legal periods and holidays held as versioned reference data with valid from, valid to, author and approver, so that business values change by a data release and not by code, and every engine can say which version it used.

## Acceptance criteria

```gherkin
Feature: Reference data service with versioned tables

  Background:
    Given the business date is 2026-11-25
    Given the table "EXPOSURE_BAND" has version 3 approved with valid from 2026-11-30 and bands "E1" to "E4"
    Given user "U-REF-01" holds RW-REFADM and user "U-RSK-01" holds the approve right in Reference data

  Scenario: AC1 Versioned row
    Given "U-REF-01" loads table "EXPOSURE_BAND" with bands "E1" to "E5" and valid from 2026-12-01
    Given "U-RSK-01" approves the load
    When the allocation engine reads "EXPOSURE_BAND" for business date 2026-11-30
    Then version 4 exists with status "APPROVED" and 5 rows
    Then version 3 stays readable with its 4 rows and has valid to 2026-11-30
    Then the service returns version 3 for business date 2026-11-30
    Then the service returns version 4 for business date 2026-12-01

  Scenario: AC2 Approver recorded
    Given "U-REF-01" loads table "DELEGATION_LIMIT" with 24 rows and valid from 2026-12-01
    When "U-REF-01" tries to approve the same load
    Then the system refuses the approval with MSG-P7-002
    Then the version stays "VALIDATED" with no approver
    Then the service still returns the previous "DELEGATION_LIMIT" version for business date 2026-12-01

  Scenario: AC3 Read by services
    Given approved versions are in force for "QUEUE" version 7, "SERVICE_LEVEL" version 2 and "HOLIDAY" version 1
    When the case service and the allocation engine start for business date 2026-11-30
    Then each reads every table it uses from the reference data service
    Then each writes one log line per table with the table code, the version number and the business date
    Then no log line contains a party identifier

  Scenario: AC4 Row fails the schema check
    Given a "SERVICE_LEVEL" load file whose row 12 has the text "five" in the column "limit_days"
    When "U-REF-01" loads it
    Then the system refuses the load with MSG-P3-027 naming row 12 and column "limit_days"
    Then no version and no rows are written

  Scenario: AC5 Approval with no approver
    Given a "HOLIDAY" version 2 with status "VALIDATED" and valid from 2026-12-01
    When the business date reaches 2026-12-01 with no approval recorded
    Then the service returns "HOLIDAY" version 1
    Then version 2 stays "VALIDATED"

  Scenario: AC6 Valid from in the past
    Given the business date is 2026-11-25
    When "U-REF-01" loads table "LEGAL_PERIOD" with valid from 2026-11-24
    Then the system refuses the load with MSG-P3-027 naming the valid from date
    Then the system writes no version

  Scenario: AC7 Same file loaded twice
    Given "U-REF-01" has loaded a "REGION" file with content hash "a1b2" and valid from 2026-12-01 as version 5
    When "U-REF-01" loads the same file with the same valid from date again
    Then the response returns the version 5 load
    Then there is still exactly one version 5 and no version 6

  Scenario: AC8 Two approvals at once
    Given a "QUEUE" version 8 with status "VALIDATED"
    When "U-RSK-01" and "U-RSK-02" approve it at the same moment
    Then the system records exactly one approval
    Then the system refuses the other with MSG-GEN-004

  Scenario: AC9 No version in force
    Given the table "TEAM" has no approved version with valid from on or before 2026-11-30
    When the allocation engine starts for business date 2026-11-30
    Then the engine does not start its run
    Then an alert names table "TEAM" and business date 2026-11-30 with MSG-P3-027

  Scenario: AC10 Empty load file
    Given a "DOCUMENT_TYPE" load file with a header row and no data rows
    When "U-REF-01" loads it
    Then the system refuses the load with MSG-GEN-001 naming "rows"
    Then the system writes no version
```

## Linked issues

- is blocked by TB0001-1449: [Issue] Request to create Jenkins pipeline for Workbench Recovery (Open)

## Sub-tasks

- TB0001-1344 [To Do] RWB-E1-043: Implementation Builder — reference data service with versioned tables (TASK-00..21)

## Comments (13)

### Comment 1: pongpat.jantanon, 2026-11-10T11:37:18.114+0700

Comment ID 1782710

Plan Gate review result: FAIL (Low-only — does not auto-block handoff, per REVIEW_GATE_WARNING)

Compliance Reviewer has completed the plan-gate review for RUN_ID
INC-009-epic-1-RWB-E1-043.
Result: [CRITICAL:0] [HIGH:0] [MEDIUM:0] [LOW:1]

Finding REVIEW-RWB-E1-043-PLAN-001 (Low):
The rollback endpoint (POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback)
declares both error code 404 (MSG-P4-003) and 422 (MSG-P3-027) for the same underlying
condition ("loadId does not resolve to an APPROVED version"), with no stated rule for
which status code applies when.
This has been recorded in plan.md §Risks and tied to TASK-09/TASK-13, to be resolved
before Builder codes this part.

Per severity policy (.github/rules/pdlc.md), a Low-only finding does not auto-block
the handoff, but the FAIL status is preserved (not relabelled PASS), and this finding
must remain visible until a human records remediation or explicit acceptance.

Required before Implementation Builder starts:
1. Review and approve plan.md + tasks.md
2. Resolve REVIEW-RWB-E1-043-PLAN-001 (choose one rule — 404-only or 422-only — for the
   rollback endpoint, update contracts/backend-apis.json and TASK-09's description, and
   add a negative-path test scenario)
3. Clear PRE-1 through PRE-8 (all currently pending — see plan.md §Plan approval
   preconditions)

Full review document: output/INC-009-epic-1-RWB-E1-043/plan/review/plan-gate-review.md

### Comment 2: pongpat.jantanon, 2026-11-10T14:14:29.020+0700

Comment ID 1783146

Question — PRE-4 blocking status needs confirmation (ref: blocking story RWB-E1-044 / TB0001-1205)

Plan-gate review flagged a status conflict for the dependency this story's migration rides on:

- docs/increments/INDEX.md marks RWB-E1-044 as SUCCESS
- RWB-E1-044's own spec (output/INC-001-epic-1-RWB-E1-044/specify/spec.md) frontmatter still reads status: BLOCKED, with 2 open clarifications (CLAR-001 BR7 drift gate, CLAR-002 job-monitor deferral)

What RWB-E1-043 actually depends on (PRE-4) is narrow: only the Flyway bean mechanics (own bean, ${recoverySchema}, flyway_schema_history_recovery, outOfOrder(false), H2 skip) — not the two open clarifications above, which concern unrelated features (drift gate, job-monitor).

Question for RWB-E1-044 owner / ACE tech lead: Is the Flyway bean itself merged to develop, independent of CLAR-001/CLAR-002 still being open? If yes, please confirm so PRE-4 can clear. If the bean is not yet merged, RWB-E1-043 Builder will stop at TASK-01 (NEXT_STEP) rather than stub it.

Ref: TB0001-1205 (RWB-E1-044), plan.md §Plan approval preconditions PRE-4.

### Comment 3: pongpat.jantanon, 2026-11-10T14:20:59.068+0700

Comment ID 1783164

Update — recheck of PRE-4 after pulling latest RWB-E1-044 changes

1) RWB-E1-044 status improved, but PRE-4 still not cleared:
- Spec is no longer BLOCKED -> now SPECIFIED (CLAR-001/CLAR-002 answered 2026-11-09; spec gates 1-4 remediated).
- Plan approval and Task approval both done: 2026-11-10 13:41 by Jesniphat Pukkham (plan commit 56e310b, MR !20).
- However, no implement/ output exists yet for E1-044 -- it is approved-to-build, not yet coded/merged to develop. PRE-4 ("Flyway bean merged to develop") is therefore still PENDING, just further along. The earlier INDEX.md-vs-spec.md status conflict I raised is now resolved (both consistent as SPECIFIED/in-progress), so that part of the prior question is answered/stale.

2) New, more significant issue found -- schema design underneath RWB-E1-043 changed:
D-RCV-47 (2026-11-10) replaces the schema this story's plan was built on:
- Old (D-RCV-18, what this story's plan/data-model.md uses): placeholder schema ${recoverySchema}, literal schema "recovery".
- New (D-RCV-47 + D-RCV-48): no separate schema -- tables live in the ACE schema "ace" (currentSchema), every recovery table/sequence/index prefixed rwb_ (e.g. rwb_case). createSchemas(false), baseline at 0, flyway_schema_history_recovery as the history table name.

RWB-E1-043's plan/data-model.md is written entirely against the old pattern: every DDL statement for reference_version / reference_row (tables, indexes, trigger functions) is qualified as ${recoverySchema}.xxx. Under D-RCV-47 these must become unqualified rwb_reference_version / rwb_reference_row in schema ace. plan.md's own PRE-4 description still cites ${recoverySchema} as the expected pattern too.

This is not just "pending verification" anymore -- it is a known-stale design that must be corrected (table names + schema qualifier removed) before Builder codes TASK-03 (the migration task), in addition to the still-open rollback 404/422 finding (REVIEW-RWB-E1-043-PLAN-001).

Recommendation: re-run/update the RWB-E1-043 plan gate applying D-RCV-47/D-RCV-48 (schema/prefix) before Builder starts, rather than waiting on E1-044's merge alone.

Ref: D-RCV-47, D-RCV-48 (docs/decisions/INC-001-decisions.md); plan/data-model.md §1; plan.md PRE-4.

### Comment 4: pongpat.jantanon, 2026-11-10T14:36:45.709+0700

Comment ID 1783232

Approval needed before Builder starts -- pick A/B/C for each item

1) Rollback endpoint error-code rule (REVIEW-RWB-E1-043-PLAN-001, Low, plan-gate review)
Approver role: Forward Deployed Architect / Technical Specifier

POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback lists both 404 (MSG-P4-003) and 422 (MSG-P3-027) for the same condition (loadId resolves to a version whose status isn't APPROVED). Pick one:

A. 404-only vs 422 (recommended -- matches the approve endpoint's existing pattern): 404 when no reference_version row resolves to loadId at all; 422 when a row resolves but its status isn't APPROVED.
B. 422-only: always return 422 for any non-APPROVED-status case; drop the 404 condition from this endpoint entirely.
C. Keep both, add precedence rule: 404 is checked first (row existence), 422 only once a row is confirmed to exist -- functionally same as A but keeps both codes "active" in the spec wording.

2) Schema/table naming -- apply D-RCV-47/D-RCV-48 now or later?
Approver role: Forward Deployed Architect (Plan approval, PRE-7); originating decision: recovery tech lead (Jesniphat Pukkham)

RWB-E1-043's plan (data-model.md, plan.md) still uses the superseded ${recoverySchema} pattern (D-RCV-18). D-RCV-47/D-RCV-48 (2026-11-10) moved to schema "ace" + "rwb_" table prefix, createSchemas(false), baseline at 0. Pick one:

A. Apply now (recommended): update data-model.md/plan.md to rwb_reference_version / rwb_reference_row in schema ace before plan approval, independent of E1-044's merge timing.
B. Defer to implementation: leave plan docs as ${recoverySchema} for now; Builder renames at TASK-03 once E1-044's actual Flyway bean is confirmed in develop.
C. Hold plan approval: don't approve PRE-7/PRE-8 until E1-044 is actually merged to develop with D-RCV-47/48 applied, then re-verify exact naming before touching RWB-E1-043's migration.

Reply with your pick for each (e.g. "1A, 2A") and the plan artifacts will be updated accordingly.

Ref: plan-gate-review.md REVIEW-RWB-E1-043-PLAN-001; docs/decisions/INC-001-decisions.md D-RCV-47, D-RCV-48.

### Comment 5: Jesniphat Pukkham, 2026-11-10T14:40:33.008+0700

Comment ID 1783253

@pongpat.jantanon Approved
1) A
2) A

### Comment 6: pongpat.jantanon, 2026-11-10T15:12:41.636+0700

Comment ID 1783397

h3. Confirming Plan approval (PRE-7) and Task approval (PRE-8) — explicit decision needed

Thank you for the Option-A dispositions (comment 1783253) — both applied to the plan artifacts (plan.md, data-model.md, contracts/backend-apis.json, tasks.md, tests/scenarios.md).

That comment resolved two specific open items (rollback 404/422 rule; schema-naming timing). It reads as a disposition on those two items, not yet as an explicit Plan/Task approval decision under plan.md §Plan approval preconditions:

* *PRE-7 — Plan approval*: sign-off that plan.md itself (data model, API contracts, task breakdown, risk list) is sound and ready to build from. Owner: Forward Deployed Architect (D-RCV-15).
* *PRE-8 — Task approval*: sign-off that tasks.md (the TASK-00..21 list Implementation Builder will execute) is correct and ready to assign. Owner: Forward Deployed Engineer (D-RCV-15).

Per D-RCV-15 you hold both gates for Recovery stories. Compare RWB-E1-044's own increment record, which states explicitly: "Plan approval and Task approval both done: 2026-11-10 13:41 by Jesniphat Pukkham."

Could you confirm, in that same explicit form:
# Plan approval (PRE-7) is given for the updated plan.md (post Option-A edits), and
# Task approval (PRE-8) is given for the updated tasks.md.

Implementation Builder is blocked at TASK-RWB-E1-043-00 until both have a recorded decision and date. PRE-1 (Product Owner spec/backlog approval) and PRE-2 (FDA design/architecture approval) also remain TBC in the increment card — flagging in case those need separate action from Product Owner / FDA rather than this gate.

Ref: plan.md §Plan approval preconditions; docs/increments/INC-009-epic-1-RWB-E1-043.md §Owners and approvals.

### Comment 7: Jesniphat Pukkham, 2026-11-10T16:33:53.879+0700

Comment ID 1783867

@pongpat.jantanon Approve all.

### Comment 8: PREMMAST SUWANNIKOM, 2026-11-11T09:24:49.141+0700

Comment ID 1784553

@Chitchaya Muanchonchana Please approve as as PO ka.

cc @pongpat.jantanon  @Jesniphat Pukkham 

### Comment 9: Chitchaya Muanchonchana, 2026-11-11T09:27:13.144+0700

Comment ID 1784557

@PREMMAST SUWANNIKOM As an internal PO/BA TechX, Approved to update task follow the comments from Henka.

### Comment 10: Nitchayaphan Kanpirompachira, 2026-11-11T18:22:36.098+0700, edited 2026-11-12T10:44:02.168+0700

Comment ID 1786523

Could you please provide the following details to assist with testing / implementation?

# Sequence Diagram / Flow Chart of API :

* {{POST /admin/reference-loads}}
* {{POST /admin/reference-loads/{loadId}/approve}}
* {{POST /admin/reference-loads/{loadId}/rollback}}
* {{GET /reference-data/{tableCode}}}

# *Example cURL Request:* Including sample header and request body fields.
# *Example API Response:* Expected response payloads (for both success and error scenarios, if available).
# *Database Tables:* Relevant DB tables involved in this flow.

### Comment 11: RACHATAPON PONGANANTAYOTIN, 2026-11-12T12:56:58.895+0700, edited 2026-11-12T13:41:10.227+0700

Comment ID 1787329

Prerequisite, need these code base to be added before re

* [https://scbjira.atlassian.net/browse/TB0001-1205|https://scbjira.atlassian.net/browse/TB0001-1205|smart-link] 
* [https://scbjira.atlassian.net/browse/TB0001-1203|https://scbjira.atlassian.net/browse/TB0001-1203|smart-link] 

### Comment 12: RACHATAPON PONGANANTAYOTIN, 2026-11-16T15:40:35.585+0700

Comment ID 1792830

Hold until new microservice design.

### Comment 13: Jesniphat Pukkham, 2026-11-16T16:57:22.424+0700, edited 2026-11-16T16:58:48.354+0700

Comment ID 1793098

Waiting for create jenkins pipeline build and deploy new microservice and dbmigration.


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
| Created Date | customfield_10249 | 2026-11-05 |
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
