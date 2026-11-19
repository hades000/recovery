# TB0001-1173 [RWB-E1-011] Reconciliation and data quality report

| Field | Value |
|---|---|
| Jira | [TB0001-1173](https://scbjira.atlassian.net/browse/TB0001-1173) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Decision, R-Dependency, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:13.569+0700 |
| Updated | 2026-11-18T17:10:40.754+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 3 |

## Description

As a team manager (RW-TEAMMGR), I want a daily reconciliation of the case list to ALS, with the variance by product and the data quality results in one Power BI report, so that everyone sees whether today's case list can be trusted.

## Acceptance criteria

```gherkin
Feature: Reconciliation and data quality report

  Background:
    Given the business date is 2026-11-30 and DP01 is loaded for 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for REC-01 and REC-02

  Scenario: AC1 Variance under limit
    Given the ALS accounts at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903
    Given the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums
    When the reconciliation step of JOB-04 runs
    Then the system writes six reconciliation_result rows , REC-01 and REC-02 for each product, each with variance 0 and result PASS
    Then the system releases the case list extract for 2026-11-30 for publish
    Then the report after the 07:30 refresh shows all three products green

  Scenario: AC2 Variance over limit
    Given the ALS count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent
    When the reconciliation step runs
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    Then the system writes 12 dq_exception rows with check code "REC-01" and the 12 account numbers
    Then the system holds the case list publish for 2026-11-30 and the lake keeps the case list of 2026-11-27
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ALS for SSME: a difference of 12 accounts, 0.41 percent."
    Then the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green

  Scenario: AC3 Variance equal to the tolerance
    Given the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30
    Given the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent
    When the reconciliation step runs
    Then the MORTGAGE result is PASS and the SSME result is BREAK

  Scenario: AC4 Account data not loaded
    Given the INT-01 load for 2026-11-30 is LATE and not COMPLETED
    When JOB-04 reaches the reconciliation step
    Then the system writes no reconciliation_result for 2026-11-30
    Then the system holds the case list publish for 2026-11-30
    Then the report shows every product as not run with the reason "DP01 is from 2026-11-27"

  Scenario: AC5 Rerun after a fix
    Given the SSME result for 2026-11-30 is BREAK and the publish is held
    Given P3 has created the 12 missing cases and the case list step has been rerun
    When the platform administrator reruns the reconciliation step for 2026-11-30
    Then the system replaces the six results for 2026-11-30 and all are PASS
    Then the system sets the 12 REC-01 exceptions CLEARED with cleared_on 2026-11-30
    Then the system releases the case list extract for 2026-11-30 for publish

  Scenario: AC6 Two runs for the same date
    Given two JOB-04 runs for 2026-11-30 start on two nodes
    When both reach the reconciliation step
    Then reconciliation_result holds one row per reconciliation, product and date, six rows in all
```

## Attachments

- [image-20261118-051925.png](../../Attachments/TB0001-1173/image-20261118-051925.png) (69349 bytes, NAMTIP WONGSOMBOON, 2026-11-18T12:20:49.489+0700)

## Comments (3)

### Comment 1: thanapat khumprom, 2026-11-17T15:53:31.645+0700

Comment ID 1794985

*RWB-E1-011 Reconciliation and data quality report: open questions (hub v17)*

*High (blocks build or makes an AC untestable)*

# *REC-02 and excluded accounts.* REC-01 subtracts the accounts excluded at entry (Flow step 3, BR8). REC-02 (Flow step 4, BR2) sums {{v_ace_account.total_balance}} without excluding them, and {{excludedAccountsByProduct()}} returns counts only. If excluded balances stay in the ACE sum, REC-02 breaks on every day that has an exclusion, and the case list is HELD every day. Should REC-02 exclude the balances of the accounts in {{case_entry_exclusion}}? If yes, through which interface?
# *Restart after a break (AC5).* RWB-TE-007 returns 409 (MSG-GEN-004) on {{POST /admin/jobs/{jobId}/rerun}} for a run that SUCCEEDED, and RWB-E1-056 AC7 confirms this for JOB-04. Does a run that ends with a BREAK finish as SUCCEEDED or FAILED? If it finishes as SUCCEEDED, how does the platform administrator restart the reconciliation step in AC5?
# *REC-04 in Epic 1.* {{proceeds}} is written by RWB-E2-008 and RWB-E2-027 (Epic 2). In E1, every {{v_ace_payment}} row would be unmatched, so REC-04 would be BREAK (red) every day. Should REC-04, and REC-03 ({{treatment}} from RWB-E2-004), report NOT_RUN until Epic 2, or should they run as written?
# *Ownership of REC rows.* RWB-E2-001 (REC-01), RWB-E2-007 (REC-03), and RWB-E2-008 and RWB-E4-050 (REC-04) also write {{reconciliation_result}} with the same unique key ({{rec_code}}, {{business_date}}, {{product_group}}). This story replaces all results of the date (BR11). Which story owns each REC row? The two REC-03 definitions also differ:
#* This story uses {{v_ace_plan.booked_at}} and 2 business days.
#* RWB-E2-007 uses {{v_ace_account}} ({{tdr_flag}} and the booked terms) and 1 ALS batch, and also covers SETTLEMENT.
# Which definition is correct?

*Medium (affects logic)*

# *REC-01 offsetting differences.* REC-01 compares counts only. If 5 accounts are missing from the case list and 5 extra rows exist, the variance is 0 and the result is PASS. A5 lists breaks in both directions, and CTL-01 requires "zero unexplained". Should any break row in either direction make the result BREAK?
# *variance_pct formula.* The story does not define it. AC2 (12 / 2,903 = 0.41) matches {{variance / source_count × 100}}. Please confirm the formula, the rounding (2 decimals?) and whether the absolute value is used.
# *Feature flag off.* Section 13 says that with {{rwb.p1.reconciliation}} off, "the case list publishes as in RWB-E1-002". RWB-E1-002 writes PENDING and publishes only when the status is RELEASED. Who sets RELEASED when the flag is off?
# *REC-04 scope.* Flow step 6 checks "v_ace_payment rows of the business date". BR4 counts a payment as a break one business day after its payment date. On business date D, which payments should REC-04 check (for example {{payment_date <= D - 1 business day}}, all history)? Does a {{proceeds}} row with {{matched_to = UNMATCHED}} count as matched?
# *Business day.* Which calendar defines a business day for {{recon.treatment.days}} and {{recon.payment.days}}? RWB-E1-028 and RWB-E1-045 use {{v_ace_holiday}}. Is "after two business days" a break on the second business day (≥) or only after it (>)?
# *Product group for REC-03 to REC-05.* Which {{product_group}} does a REC-03, REC-04 or REC-05 row get? This matters most for keys that are not linked to a case, for example {{listing.asset_key}}, or a payment on an account with no open case. AC1 expects 15 rows (5 × 3).
# *AC4 publish status.* When the gate holds JOB-04, no {{case_list_row}} exists for the date (RWB-E1-015 AC). What does "the case list publish for 2026-11-30 stays HELD" mean in that case? Where is NOT_RUN with its reason stored for the report, given that {{result}} holds only PASS or BREAK?

*Low*

# *MSG-P1-001 text.* Section 14 says "Today's ACE batch has not arrived." The message catalog says "Today's load has not arrived." Which text is final?
# *"Case exceptions".* Build Notes Epic 1 v6 says the story writes "the case exceptions". Section 12 says there is no exception table. What are "the case exceptions"?
# *Timing.* Must the reconciliation step finish before the 07:30 Power BI refresh? The case list step can start as late as 07:15 (RWB-E1-002).

### Comment 2: Piyawan Sanpanya, 2026-11-17T15:59:26.383+0700, edited 2026-11-17T16:00:26.077+0700

Comment ID 1795035

@CHANISSARA MAHAKITTIKUN 

QA Question 

*Preconditions* 

# The reporting and BI analyst has built the Power BI report "Reconciliation and data quality" on the lake extracts and scheduled its refresh at 07:30. ==> How to done this story without power BI

*Flow*

# step2 :  for v_ace_batch_status ,wich the story to implement this view function? there is no on precondition
# step3 : for v_ace_collateral_detail ,wich the story to implement this view function? there is no on precondition , and what is value of  "entry threshold"
# step 5 : How does REC-03 know that a treatment has been approved for more than two business days?
# step 6 : REC-04 waits until the next business day—but how does a same-date payment query retain aged items?
# step8 : How to computes the variance and the variance percent for each check and product group?, Dose Henka provide the formula? , rounding?
# step 9 : How to do writes the break list, what is condition?
# step 11 : writes the reconciliation extract and the data quality extract to the data lake. on this the  story scope can we do the feature?
# Release requires complete PASS results—not merely the absence of a BREAK : Must all six required product/check results belong to the same generation before release? What hold applies if one is missing/stale/FAILED/NOT_RUN? When case_list_row has zero rows, where is publish status recorded so empty-set any/all logic cannot pass incorrectly? How are REC-03/04/05 breaks that do not hold publication alerted and explained to users?

### Comment 3: NAMTIP WONGSOMBOON, 2026-11-18T12:20:49.695+0700

Comment ID 1796390

Ref: Grooming Session – Room 2 with Henka , {{2026-11-18}}
Topic 1  Story → This Story does not require integration with Power BI, and Power BI testing is out of scope.

!image-20261118-051925.png|width=682,alt="image-20261118-051925.png"!


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
