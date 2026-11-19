# TB0001-1239 [RWB-TE-005] Rule table test harness

| Field | Value |
|---|---|
| Jira | [TB0001-1239](https://scbjira.atlassian.net/browse/TB0001-1239) |
| Type | Story |
| Status | Hold |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, R-Decision |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1 |
| Team | - |
| Created | 2026-11-05T16:11:13.409+0700 |
| Updated | 2026-11-16T09:13:20.692+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 6 |
| Comments | 20 |

## Description

As a center of excellence analyst (RW-COE), I want a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result), so that a rule change is tested the same way as code before it takes effect.

## Acceptance criteria

```gherkin
Feature: Rule table test harness

  Background:
    Given the Restructure route set version "RES-2026.11" with 37 rows, R-RES-01 to R-RES-37
    Given a Tests sheet with one test case per row

  Scenario: AC1 Every row tested
    When the harness runs on "RES-2026.11"
    Then 37 tests run
    Then each test result names its rule ID and its test case ID
    Then all 37 pass and the version state is "VALIDATED"

  Scenario: AC2 Expected action differs
    Given the test case for "R-RES-04" expects to state "WITH_FCR_OFFICER" and owner role "RW-RESTRUCT"
    Given the row "R-RES-04" in version "RES-2026.12" has to state "IN_FCR_QUEUE"
    When the harness runs on "RES-2026.12"
    Then the test for "R-RES-04" fails with MSG-P3-014 naming the expected and the actual to state
    Then the version state is "FAILED"
    Then the version cannot be approved

  Scenario: AC3 Row with no test case
    Given version "RES-2026.13" where row "R-RES-12" names test case "RT-RES-012" that is not in the Tests sheet
    When the harness runs
    Then the system marks the version "FAILED" with MSG-P3-014 naming "R-RES-12" and "RT-RES-012"

  Scenario: AC4 Two rows hit one input
    Given version "RES-2026.14" where the conditions of "R-RES-09" and "R-RES-10" both hold for an offer outside the range with deviation_flag "Y"
    When the harness runs the test of "R-RES-10"
    Then the test fails with MSG-P3-014 naming "R-RES-09" and "R-RES-10"

  Scenario: AC5 No row hits
    Given version "RES-2026.15" where the condition of "R-RES-28" was changed so no row holds for a payment inside the cure period
    When the harness runs the test of "R-RES-28"
    Then the test fails with MSG-P3-014 naming "R-RES-28" as expected and no row hit

  Scenario: AC6 Missing fact
    Given the test case of "R-RES-30" gives no value for "break_count"
    When the harness runs it
    Then the test fails with MSG-P3-014 naming the fact "break_count"

  Scenario: AC7 Repeated run
    Given the harness ran on "RES-2026.11" with 37 passes
    When it runs again on "RES-2026.11"
    Then the results are the same 37 passes
    Then the system stores one result set for the version

  Scenario: AC8 Build pipeline
    Given the rule files in the repository hold the ten route sets with 448 rows
    When the build runs
    Then the build runs 448 rule tests named by rule ID
    Then a failing rule test fails the build
```

## Sub-tasks

- TB0001-1352 [To Do] [RWB-TE-005] BE - Precondition check, API port, migration, reader/builder, persistence, harness, flag guard, build task
- TB0001-1353 [To Do] [RWB-TE-005] BE - Unit and container tests
- TB0001-1354 [To Do] [RWB-TE-005] BE - Guardrails, regression and coverage gates
- TB0001-1355 [To Do] [RWB-TE-005] Evidence, ACE MR and traceability

## Attachments

- [image-20261109-092415.png](../../Attachments/TB0001-1239/image-20261109-092415.png) (45094 bytes, Chitchaya Muanchonchana, 2026-11-09T16:28:06.629+0700)

## Comments (20)

### Comment 1: Chayaporn Kaewin, 2026-11-09T14:32:22.894+0700

Comment ID 1781055

h3. Technical Specifier - clarification needed before planning (RWB-TE-005)

The specification for this story is drafted but *BLOCKED*. Four decisions are needed from BA / Product Owner before the Implementation Planner can start. Please reply on this issue with a decision for each item.

*CLAR-001 - Where is the rule-version state (VALIDATED / FAILED) stored, and who writes it?* (High)
The story is contradictory (open in Story Defects v2, RWB-TE-005 item 6): section 4 says the P4 load handler sets the version state, section 9 names _rule_row.state_, but section 11 lists every _rule_row_ field as Read-only and section 17 allows rule rows to be read only through the P4 published interface.
Decision needed: which entity and column hold the state, and which P4-owned operation writes it?
Options: (a) _rule_row.state_, written through a new P4 published write operation; (b) a P4-owned rule-version status; (c) other (please state).

*CLAR-002 - What if _expected_owner_role_ or _expected_timer_spec_ is empty in a test case?* (Medium)
DF-REF-194 and DF-REF-195 are optional in the data dictionary, but BR2 requires owner role and timer to equal the expected values.
Options: (a) compare against null (the hit row must also have no value); (b) skip that comparison; (c) reject the test case as incomplete.

*CLAR-003 - Response in DEV when the flag _rwb.p3.rule-harness_ is off and the harness fails* (Medium)
Story section 13 says "warn and the load continues"; the contract says 422 MSG-P3-014 when the harness fails.
Decision needed: (a) 201 with the version marked FAILED and a warning, or (b) 422 MSG-P3-014? And may a FAILED version take effect in DEV? (The story only says it must never take effect above DEV; our proposal is that it stays unapprovable in DEV too.)

*CLAR-004 - Module dependency and transaction (P3 harness / P4 load handler)* (Medium)
The P4 load handler calls the P3 published _RuleTableHarness_, and the harness reads rule rows through a P4 published interface (published api packages only). Please confirm with the architect that this two-way dependency is accepted, and decide: is the _rule_test_case_ write in the same transaction as the P4 version load, and when the load returns 422 are the rule rows and results kept (as a FAILED version) or rolled back?

*Prerequisite:* RWB-E1-044 (parameterized migrations) is still BLOCKED. The _rule_test_case_ migration cannot be planned until it is done.

Spec (draft): output/INC-006-epic-1-RWB-TE-005/specify/spec.md in the AISDLC workspace. Compliance review REVIEW-RWB-TE-005-SPEC-003: FAIL (open: 2 High, 2 Medium, 4 Low). After your answers we update the same spec and re-run the review. Implementation must not start until then.


### Comment 2: Chitchaya Muanchonchana, 2026-11-09T16:28:06.780+0700

Comment ID 1781497

@CHANISSARA MAHAKITTIKUN For ypur information

!image-20261109-092415.png|width=672,alt="image-20261109-092415.png"!

Notice:

* *P4 calls P3* (to kick off testing)
* But *P3 also has to call back into P4* (to request the rule row data, since P4 owns that data)

This is what's called a "two-way / cyclic dependency." In good architecture, modules should normally call each other one-way (A calls B, but B never calls back into A). A cycle like this can cause:

* Deployment difficulty (both modules must be deployed together since they depend on each other)
* Debugging difficulty (on error, it's unclear who called whom first)
* Risk of deadlock/infinite loops if not designed carefully

{color:#bf2600}→ This is why an {color}{color:#bf2600}*architect must confirm*{color}{color:#bf2600} whether this pattern is acceptable within Recovery Workbench's architecture, or whether it needs to be redesigned (e.g., have P4 {color}{color:#bf2600}*"push the rule row data to P3 along with the test command"* {color}{color:#bf2600}instead of P3 calling back to request it).{color}

### Comment 3: CHANISSARA MAHAKITTIKUN, 2026-11-10T12:04:13.451+0700

Comment ID 1782807

@Chayaporn Kaewin 

CLAR-001

 

Decision: Option (b) – a P4-owned rule-version status.

 

VALIDATED / FAILED should be stored at the rule-version level, not on individual rule_row records. P4 should own and write the rule-version lifecycle status. The exact P4 entity and column should be confirmed from the canonical data model.

 

CLAR-002

 

Decision: Option (a) – compare against null.

 

If expected_owner_role or expected_timer_spec is empty, the corresponding value on the hit row must also be null. An empty expected value should not mean that the comparison is skipped.

 

CLAR-003

 

Decision: Option (a), provided that flag OFF means warning-only/non-blocking validation in DEV.

 

Return 201, retain the candidate version as FAILED, and return the warning/validation result. A FAILED version must not be approved or become effective, including in DEV.

 

If rwb.p3.rule-harness = off means that the harness is completely bypassed, then the current requirement is contradictory because no harness failure can occur. In that case, the flag behavior must be clarified before implementation. Mandatory harness failures should continue to return 422 MSG-P3-014.

 

CLAR-004

*Business decision:* Rule validation must be completed before the rule version can be approved. If validation completes and the rule tests fail, the candidate rule version and the rule_test_case results must be retained with status FAILED for traceability. A FAILED version must not be approved or become effective.

If a technical failure prevents the load or validation process from completing, the transaction should be rolled back.

 

### Comment 4: Chayaporn Kaewin, 2026-11-10T15:22:45.547+0700, edited 2026-11-10T15:27:18.896+0700

Comment ID 1783452

h3. Technical Specifier - spec updated, two items still need an answer (RWB-TE-005)

Thanks for the answers. CLAR-001, CLAR-002 and CLAR-004 (business/transaction part) are now applied to the spec (output/INC-006-epic-1-RWB-TE-005/specify/spec.md). CLAR-003 is applied conditionally. Two items remain before planning can start:

*CLAR-004 (architecture) - still open*
Chitchaya flagged the P3/P4 calls as a two-way dependency: P4's load handler calls P3's published {{RuleTableHarness}}, and the harness calls back into P4 to read rule rows. Please have the architect confirm this pattern is acceptable within Recovery Workbench's architecture, or that P4 should instead push the rule-row data to P3 together with the test command (avoiding the call-back).

*CLAR-005 (new) - what does the flag* {{rwb.p3.rule-harness}} *actually gate?*
Your CLAR-003 answer was conditional: Option (a), "provided that flag OFF means warning-only/non-blocking validation in DEV," and you noted that if flag off instead means the harness is completely bypassed, the requirement is contradictory (no harness failure can occur). We need to know which reading is correct:

* (a) flag off = the harness still runs and evaluates every test; a failure is just non-blocking (load returns 201, version retained as FAILED, with a warning), or
* (b) flag off = the harness does not run at all (no test execution, no result)

Please confirm (a) or (b).

Spec status: BLOCKED pending CLAR-004 (architecture) and CLAR-005, and the RWB-E1-044 prerequisite.

### Comment 5: CHANISSARA MAHAKITTIKUN, 2026-11-10T18:19:41.174+0700

Comment ID 1784340

@Chayaporn Kaewin 

*CLAR-004 – Architecture Decision*

Use a *one-way dependency from P4 to P3* for the rule-table validation flow.

P4, as the owner of the rule-version and {{rule_row}} data, should pass the rule-row data required for validation to P3 together with the {{RuleTableHarness}} test command. P3 should execute the validation using the supplied data and return the validation result ({{VALIDATED}} / {{FAILED}}) to P4.

P3 should *not call back into P4 to retrieve the rule rows during the same validation flow*.

 

h3.  CLAR-005 – {{rwb.p3.rule-harness}} feature flag

*Decision: Option (a)*

### Comment 6: Chayaporn Kaewin, 2026-11-11T09:56:51.686+0700

Comment ID 1784678

h3. Technical Specifier - correction to previous comment (RWB-TE-005)

Previous comment listed two blockers; withdrawing the RWB-E1-044 prerequisite item from that list here (tracked separately, not this comment's concern). The item that still needs an answer from this comment:

*Sign-off authority on comment 1784340* - this spec attributes the CLAR-004 business/transaction answer (comment 1782807) and the CLAR-004 architecture + CLAR-005 answers (comment 1784340) to "Product Owner" and "architect" respectively, but neither role is attested for that Jira account anywhere in this repository: the named PO on record is Chitchaya Muanchonchana (D-RCV-46) and the named FDA/architect is Jesniphat Pukkham (D-RCV-15). Could the PO or delivery lead confirm that CHANISSARA MAHAKITTIKUN is authorized to give the architect sign-off for the P3/P4 dependency decision (and/or the PO decision), so this review finding can close?


### Comment 7: Jesniphat Pukkham, 2026-11-11T10:13:51.569+0700

Comment ID 1784731

@Chayaporn Kaewin Approved

### Comment 8: Chayaporn Kaewin, 2026-11-11T10:31:13.351+0700, edited 2026-11-11T10:34:55.620+0700

Comment ID 1784791

h3. Technical Specifier - status update (RWB-TE-005)

Thank you @Jesniphat Pukkham for the architect sign-off on comment 1784731. Compliance review REVIEW-RWB-TE-005-SPEC-005 (2026-11-11) confirms this closes finding 007/013's architecture half: the CLAR-004 dependency-direction decision and the CLAR-005 flag semantics are now attested by the architect of record.

One item from that same review stays open and still needs an answer:

*Finding 013 (PO half) - still OPEN.* CLAR-001, CLAR-002 and the business/transaction part of CLAR-004 (comment 1782807) - the P4-owned rule-version state, the null-comparison rule for {{expected_owner_role}}/{{expected_timer_spec}}, and the no-rollback-on-test-failure rule, all of which gate BR3 (a FAILED rule version can never be approved or take effect) - were answered by CHANISSARA MAHAKITTIKUN. No reply on this issue confirms her authority to give these as Product Owner decisions.

Could @KRISSADA RONGRAT (Product Owner, per D-RCV-46) or the delivery lead confirm CHANISSARA's authority for the CLAR-001/002/003 business/transaction answers, so this item can close? (Not asking about the RWB-E1-044 prerequisite here - that is tracked separately.)

### Comment 9: Chitchaya Muanchonchana, 2026-11-11T10:40:44.850+0700

Comment ID 1784824

@Chayaporn Kaewin As an internal PO/BA , I have approved to revise follow the comments from Henka ka.

### Comment 10: Chayaporn Kaewin, 2026-11-11T15:59:14.793+0700

Comment ID 1785929

h3. Technical Specifier - waiver request for RWB-E1-044 prerequisite (RWB-TE-005)

The plan for this story was built on RWB-E1-044's approved-but-unbuilt plan (output/INC-001-epic-1-RWB-E1-044/plan/tasks.md), blocking every task on TASK-RWB-E1-044-17. Compliance review REVIEW-RWB-TE-005-PLAN-001 found this FAIL (High, REVIEW-001): the person who gave that instruction is the story assignee, not a named authority, so spec finding 002 (RWB-E1-044 not yet built) is not waived.

RWB-E1-044 is not expected to reach implement/ this sprint. Could @Jesniphat Pukkham (FDA/architect of record, D-RCV-15) record a waiver here to proceed with planning/implementation of RWB-TE-005 against E1-044's approved plan, on the understanding that if the built E1-044 migration differs from what's approved, TASK-RWB-TE-005-00 stops and the plan is re-run?

### Comment 11: Jesniphat Pukkham, 2026-11-11T16:00:10.743+0700

Comment ID 1785933

@Chayaporn Kaewin Approved

### Comment 12: Chayaporn Kaewin, 2026-11-11T16:47:49.300+0700

Comment ID 1786121

h3. Plan gate review - sign-off needed from architect/spec owner (RWB-TE-005)

RWB-TE-005 passed plan gate review, but 2 blocking findings still need your sign-off (REVIEW-RWB-TE-005-PLAN-001):

*REVIEW-002:* The plan originally claimed certain business rules (BR3, BR4, BR6) and acceptance criteria (AC1, AC2) were "fully tested," but TE-005 actually only covers half of the flow (called "P3" in the plan) - the remainder (refusing the load on failure, writing status, checking permissions - called "P4") is in scope of RWB-E1-029, which has no plan yet. If the label isn't corrected, a later audit could wrongly conclude these rules are already closed. The label in the plan has been fixed (now states "half coverage + remaining gap"). Requesting your acknowledgement, as spec owner / tech lead, that it's acceptable to defer the P4 portion to RWB-E1-029.

*REVIEW-003:* The plan adds 3 new fields to a contract that another module (P4/RWB-E1-029) reads: {{RuleTestResult.detail}}, {{HarnessResult.failureBlocking}}, {{HarnessResult.outcome()}}. These are additive (nothing removed/renamed), but since it's a cross-module contract, new fields need architect sign-off, not a planner's unilateral call. If these fields don't match what you want RWB-E1-029 to consume (e.g. you'd rather P4 read the flag itself), the code built against this contract will need rework. Requesting your sign-off, as architect of record, that these 3 fields are acceptable before build starts.

Once both are confirmed, the compliance gate will be re-run.

### Comment 13: Chayaporn Kaewin, 2026-11-11T16:48:35.743+0700

Comment ID 1786125

h3. Plan gate review - confirmation/ruling needed from PO (RWB-TE-005)

RWB-TE-005 passed plan gate review, but 2 blocking findings still need your confirmation/ruling (REVIEW-RWB-TE-005-PLAN-001):

*REVIEW-004:* The test plan reads from a sheet named "Tests" in an Excel file (columns like test_case_id, route_set, rule_version, rule_id, from_state, event_code, facts, expected_to_state, expected_owner_role, expected_timer_spec), but the actual column layout/order is not defined in any source document - the planning team guessed it from data-dictionary column names. The risk: our own test fixtures were built on the same guess, so passing tests don't prove they match the real file. A separate module (RWB-E1-029) also has its own parser reading the same sheet, risking mismatched interpretation. Requesting you confirm (or locate the E1-029/BA template owner to confirm) whether the "Tests" sheet column layout matches what's assumed, before work starts. If not confirmed in time, work will proceed under an explicit "ASSUMED" flag.

*REVIEW-005:* There's a conflict between two stories on "what happens to the transaction when a rule-table test fails": RWB-E1-029 (original spec) says it will refuse to load the whole file (full rollback, nothing kept), while TE-005 (per your earlier clarification CLAR-004) says to keep the version as FAILED (commit, no rollback) for traceability. These directly conflict - if not aligned beforehand, real integration will produce mismatched data (one side thinks it's kept, the other already rolled it back), affecting the audit trail. Requesting your ruling, as PO, on how to align them (E1-029 changes to match TE-005, TE-005 changes to match E1-029, or a third option). Since RWB-E1-029 has no plan yet, this can be logged as an open item to track in parallel without blocking TE-005 immediately, but someone needs to formally acknowledge the conflict first.

Once both are confirmed, the compliance gate will be re-run.

### Comment 14: Chayaporn Kaewin, 2026-11-11T16:52:17.321+0700

Comment ID 1786142

@Jesniphat Pukkham  Please approve

### Comment 15: Chayaporn Kaewin, 2026-11-11T16:52:41.870+0700

Comment ID 1786144

@Chitchaya Muanchonchana Please approve

### Comment 16: Jesniphat Pukkham, 2026-11-11T16:59:05.080+0700

Comment ID 1786178

@Chayaporn Kaewin Approve

### Comment 17: Chitchaya Muanchonchana, 2026-11-11T17:44:26.790+0700

Comment ID 1786445

@Chayaporn Kaewin As Henka comments we will exclude all related to E1-029, Approved ka.

### Comment 18: Chayaporn Kaewin, 2026-11-13T10:20:37.144+0700

Comment ID 1789160

@CHANISSARA MAHAKITTIKUNSince Temporal is not included in the current sprint, but this story will have a dependency on Temporal following the grooming meeting on 12 Nov, could you please confirm its priority and whether it can still be completed within this sprint?

### Comment 19: CHANISSARA MAHAKITTIKUN, 2026-11-13T17:25:28.382+0700

Comment ID 1790691

@Chayaporn Kaewin We are working on technical Docs and will be adding temporal and drools part as well. so on 16/112026 we will have some new stories for temporal & drools configuration which will be added to current sprint.

### Comment 20: Pe Chichareon, 2026-11-13T17:37:19.324+0700

Comment ID 1790743

Update status to Hold. Pending Henka come up with new user story / content to support Temporal solution


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
| Rework | customfield_17514 | Rework |
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
