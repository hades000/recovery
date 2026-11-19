# TB0001-1225 [RWB-E1-064] Data dictionary for the 14 data products

| Field | Value |
|---|---|
| Jira | [TB0001-1225](https://scbjira.atlassian.net/browse/TB0001-1225) |
| Type | Story |
| Status | Dev To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Jesniphat Pukkham |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed, R-Requirement, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S2 Squad1 |
| Team | - |
| Created | 2026-11-05T12:37:58.136+0700 |
| Updated | 2026-11-17T13:37:08.479+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 3 |
| Comments | 3 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want every field in the 14 data products typed, sourced and owned, with a data contract per source system that its owner confirms, so that a data contract can be agreed with the system that owns it.

## Acceptance criteria

```gherkin
Feature: Data dictionary for the 14 data products

  Background:
    Given the dictionary holds 1,256 fields in 108 entities
    Given data product "DP01" Account and arrears has owner role RW-DATASTEW and system of record "Core bank (ALS) via COLLINS"
    Given contract "DC-ALS" for source system "Core bank (ALS)" and interfaces "INT-01" and "INT-02" is "DRAFT" with 32 mapped fields

  Scenario: AC1 Every field is defined
    Given the 14 data products
    When a developer calls GET /admin/data-dictionary/fields?entity=loan_account&field=days_past_due
    Then the field "DF-ACC-014" shows type "NUMBER", physical type "integer", source system "Core bank (ALS) via COLLINS", source field "DELAY_DAYS", refresh "Daily, end of day", owner RW-DATASTEW and behavior when late "Keep the previous value and mark DP01 stale"
    Then a call for all 1,256 fields returns no field with an empty type, source system, source field, refresh, owner or behavior when late

  Scenario: AC2 The owning system has agreed it
    Given the data steward recorded the confirmation of "DC-ALS" by role "ALS system owner" on 2026-11-12 with document "DOC-SYN-0640"
    When the data steward publishes "DC-ALS"
    Then the contract status is "PUBLISHED" with version 1 and the confirmation on 2026-11-12
    Then the 32 mapped fields of Core bank (ALS) show mapping status "Confirmed"

  Scenario: AC3 A change is visible
    Given field "DF-ACC-014" is at version 1
    When the data steward changes its source field to "DPD_DAYS" with reason "ALS renamed the field in release 26.4" on 2026-11-18
    Then field "DF-ACC-014" is at version 2 dated 2026-11-18 with that reason
    Then version 1 stays readable with its own date

  Scenario: AC4 Publish without the owner's confirmation
    Given contract "DC-EFS" for EFS has no recorded confirmation
    When the data steward publishes "DC-EFS"
    Then the system refuses the call with status 409 and MSG-P1-021 for system "EFS"
    Then the contract stays "DRAFT"

  Scenario: AC5 A change without a reason
    When the data steward changes field "DF-ACC-015" with an empty reason
    Then the system refuses the call with status 422 and MSG-GEN-001 for field "reason"
    Then field "DF-ACC-015" stays at version 1

  Scenario: AC6 A dictionary load with a missing attribute
    Given a dictionary load in which field "DF-COL-005" collateral.plot_no has no refresh cycle
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "refresh_cycle missing for DF-COL-005"
    Then the dictionary in force is unchanged

  Scenario: AC7 Two changes to the same field at once
    Given two data stewards read field "DF-ACC-016" at version 1
    When both send a change with version 1
    Then the system saves the first change as version 2
    Then the system refuses the second with status 409 and MSG-GEN-004

  Scenario: AC8 A change to a field in a published contract
    Given contract "DC-ALS" is "PUBLISHED" at version 1
    When field "DF-ACC-014" changes to version 2
    Then the system creates contract "DC-ALS" version 2 as "DRAFT"
    Then version 1 stays "PUBLISHED" and in force
```

## Comments (3)

### Comment 1: NATAPATCHARA ANUROJE, 2026-11-17T10:54:07.840+0700

Comment ID 1794047

Reviewed this card against the story, the physical schema, and the sibling stories it depends on (RWB-E1-001, RWB-E1-069).

*Concerns (Dependencies):* Header lists RWB-E1-001, RWB-E1-043, RWB-E1-069. One more belongs on it: *RWB-TE-003* (Types and contract tests) — the solution plan (§13 step 5) names it directly for the endpoint contract tests, but it's not in the "Depends on" line. Build order check: RWB-E1-001 (#9), RWB-TE-003 (#5), RWB-E1-043 (#8), RWB-E1-069 (#10) are all earlier than this story (#13) — no circular dependency.

----

*Clarification needed:*

*1. AC2 claims all 304 ACE view fields are ready, but 127 of them (Section B) may not be*

RWB-E1-069's own story confirms the split this story also states (177 Section A / 127 Section B fields), and is explicit that *Section B views can't even be created* until *RWB-ACE-001* (external ACE team) delivers its 14 Tier 2 tables (DL43) — "the features that read a Section B view stay behind their flags" until then. But AC2 here reads as if all 304 fields across all 30 views are testable together right now.

{color:#ff5630}*Question:*{color} Can AC2 only be tested in full (30/30 views, 304/304 fields) once RWB-ACE-001 lands, with a partial version (16 Section A views, 177 fields) testable before that? If so, should AC2 say so explicitly?

*2. The governance data for 1,366 fields doesn't exist yet anywhere*

The story's Background assumes "the governance load... was published," and flow step 1 has the data steward "prepare the governance load for all 1,366 fields with owner role, refresh cycle, late behavior and interface." The only named source, BRD Epic 1 §5, is a single action-item row: "Confirm the data dictionary sources and owners for each data product — during the build" — not a prepared dataset.

{color:#ff5630}*Questions:*{color}
# Is there an actual prepared source (spreadsheet, prior workshop output) for 1,366 fields × 4 governance attributes each, or does the data steward gather this from scratch during this story?
# If from scratch, does "Small — finished inside two weeks" (§6 INVEST) still hold? And given the load is all-or-nothing (X3: refused in full on any single bad row), is a single 1,366-field load realistic, or should it be loadable product-by-product?

*3. The 7 "derived" view fields have no flag anywhere in the schema*

AC1/X3 exempt 7 named fields (e.g. {{v_ace_contact.contact_type}}) from the "must name one ACE column" rule. {{sys_fields}} has no {{is_derived}} (or similar) column — the exemption list can only live as a hardcoded constant in code or config, which sits awkwardly against this story's own guardrail "No business value in code."

{color:#ff5630}*Question:*{color} Should {{sys_fields}} gain a flag column for this, or is a hardcoded/config list the intended, accepted approach?

*4. Date order in the test scenarios*

Background: "the governance load... was published on *2026-11-30*." AC5: the data steward changes a field's late behavior "on *2026-11-18*" — 12 days *before* the Background's publish date. If these scenarios are meant to compose (not run as fully independent fixtures), the ordering doesn't line up.

{color:#ff5630}*Question:*{color} Are the Gherkin scenarios independent fixtures with their own dates (fine as-is), or should they share one timeline?

----

Net: items 1 and 2 look like real sizing/sequencing risks worth flagging up; 3 and 4 are smaller, implementation-level items.

### Comment 2: NATAPATCHARA ANUROJE, 2026-11-17T11:05:58.081+0700

Comment ID 1794106

Follow-up to point 3 above (the 7 derived fields with no schema flag) — found concrete proof it's a recurring pattern, not isolated to this story.

Checked RWB-E1-015's view, {{v_ace_batch_status}}: its {{is_complete}} field is {{(r.status = 'COMPLETED')}} — computed, not copied — but the dictionary seed row for it (DF-ACE-186) maps {{source_field}} to {{public.ace_batch_run.status}}, the *same* column as the literal {{status}} field (DF-ACE-182). Same missing {{is_derived}}-style flag as the 7 fields here.

Also found, while checking that view's seed rows: *every* {{v_ace_batch_status}} field (DF-ACE-178 to -186, 9 rows) has {{physical_type='integer'}} in the seed, regardless of actual type (several are {{varchar}}, one is {{boolean}}). Posted the detail on {{TB0001-1177}}.

Both are really RWB-E1-001's to fix (V0001 owns the seed and the DDL), but flagging here since they directly affect what "every field has a correct physical type" (AC1) and the derived-field exception mechanism (point 3) actually mean for this story.

### Comment 3: Nitchayaphan Kanpirompachira, 2026-11-17T13:34:58.129+0700

Comment ID 1794468

After reviewing the story and reading through the comments, my questions align with what the dev team has already raised and I also have an additional question

*Clarification needed:*

# Dictionary load validation — check order when multiple failures occur

Section 4 (Flow, step 3) and exception X3 state that {{DataDictionaryLoader}} refuses the whole load if any of several conditions is violated (unknown field, source system not "ACE"/"Workbench", view field's source field not a valid column or derived field, or any required attribute empty). The response message MSG-P1-002 includes a placeholder {{{check}}} — implying only the first failing check is reported, not all of them.

*Question:* When a single load has more than one of these violations at once, which check fires first and gets reported? Is there a defined validation order (e.g., unknown field → source system → source field/column → required attributes), or is it undefined/implementation-dependent?


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
