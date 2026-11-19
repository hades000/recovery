# TB0001-1206 [RWB-E1-045] Multi-product parameters for Mortgage, HP and SSME

| Field | Value |
|---|---|
| Jira | [TB0001-1206](https://scbjira.atlassian.net/browse/TB0001-1206) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, R-Decision, R-Dependency, R-Spec, SLA-Breach |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:43.017+0700 |
| Updated | 2026-11-18T17:01:01.556+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 8 |
| Comments | 9 |

## Description

As a center of excellence analyst (RW-COE), I want every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product in the reference data, so that a new product or a product change needs no code change.

## Acceptance criteria

```gherkin
Feature: Multi-product parameters for Mortgage, HP and SSME

  Background:
    Given the business date is 2026-12-01
    Given PRODUCT_PARAMETER version 2 is in force with NOTICE_PERIOD_DAYS 30 calendar days for "MORTGAGE" and 60 calendar days for "HIRE_PURCHASE"
    Given PRODUCT version 1 is in force with "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"

  Scenario: AC1 Product value differs
    Given case "RW-2026-000101" with product group "MORTGAGE" and case "RW-2026-000102" with product group "HIRE_PURCHASE"
    When the timer engine sets the notice timer on both cases on 2026-12-01
    Then the notice timer of "RW-2026-000101" expires on 2026-12-31
    Then the notice timer of "RW-2026-000102" expires on 2027-01-30
    Then each timer start records PRODUCT_PARAMETER version 2

  Scenario: AC2 New product added
    Given PRODUCT version 2 adds product group "AUTO_LEASE" with valid from 2026-12-05
    Given PRODUCT_PARAMETER version 3 and SERVICE_LEVEL version 3 add every required row for "AUTO_LEASE" with valid from 2026-12-05
    Given all three versions are approved
    When the COLLINS load of 2026-12-05 carries an "AUTO_LEASE" account at 90 days past due
    Then the system creates a case with product group "AUTO_LEASE"
    Then the system sets its timers from the "AUTO_LEASE" rows
    Then no deployment took place between 2026-12-01 and 2026-12-05

  Scenario: AC3 Missing parameter blocked
    Given a SERVICE_LEVEL load with valid from 2026-12-10 that has no row for "SSME" and status "WAITING_PARTNER"
    When the load validates
    Then the system refuses the load with MSG-P3-034 naming "SSME" and "WAITING_PARTNER"
    Then SERVICE_LEVEL version 3 stays in force

  Scenario: AC4 Value outside its range
    Given the catalog range for NOTICE_PERIOD_DAYS is 1 to 365
    When a PRODUCT_PARAMETER load sets NOTICE_PERIOD_DAYS to 0 for "SSME"
    Then the system refuses the load with MSG-GEN-002 naming "NOTICE_PERIOD_DAYS", 1 and 365

  Scenario: AC5 Duplicate product row
    Given a PRODUCT_PARAMETER load with two NOTICE_PERIOD_DAYS rows for "MORTGAGE", 30 and 45
    When the load validates
    Then the system refuses the load with MSG-P3-027 naming "MORTGAGE" and "NOTICE_PERIOD_DAYS"

  Scenario: AC6 Product removed while cases are open
    Given 3 open cases with product group "UNSECURED"
    When a PRODUCT load with valid from 2026-12-15 leaves out "UNSECURED"
    Then the system refuses the load with MSG-P3-027 naming "UNSECURED" and 3 open cases

  Scenario: AC7 No parameter in force at run time
    Given case "RW-2026-000140" with product group "SSME" and no NOTICE_PERIOD_DAYS row for "SSME" in force
    When the timer engine sets the notice timer on 2026-12-01
    Then the system writes no notice timer
    Then the system places the case in the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS"

  Scenario: AC8 Value changes while a timer runs
    Given the notice timer of "RW-2026-000101" started on 2026-12-01 and expires on 2026-12-31
    Given PRODUCT_PARAMETER version 4 with NOTICE_PERIOD_DAYS 45 for "MORTGAGE" takes effect on 2026-12-03
    When the timer engine sets a notice timer on Mortgage case "RW-2026-000150" on 2026-12-03
    Then the timer of "RW-2026-000101" still expires on 2026-12-31
    Then the timer of "RW-2026-000150" expires on 2027-01-17
```

## Comments (9)

### Comment 1: NAMTIP WONGSOMBOON, 2026-11-16T15:14:02.161+0700

Comment ID 1792753

Ref: Grooming Session – Room 2 with Henka (K. Sahilmore), {{2026-11-16}}

This story covers the validation configuration used to check business rules when data is received from ACE into Recovery.


### Comment 2: Nate Trakarntanasuk, 2026-11-16T16:15:43.628+0700, edited 2026-11-16T16:17:31.765+0700

Comment ID 1792942

@CHANISSARA MAHAKITTIKUN 

QA Question 

* For the AC Does it all call *GET /api/recovery/v1/cases/{caseId}/timers* to validate? 
* Action _การกระทํา :_ the load validates → This action meaning to call *POST /api/recovery/v1/admin/reference-loads?* Can you pls give more information of this action
* This testcase {{TC-E1-045-09}} about Access Can it be test in this story?

|{{TC-E1-045-09}}|Access|Access|{{RW-PHONECOL}} (Reference data R only) loads PRODUCT_PARAMETER; refused with {{MSG-P4-002}}|

### Comment 3: thanapat khumprom, 2026-11-16T17:47:37.463+0700

Comment ID 1793321

h2. RWB-E1-045 Multi-product parameters: specification blocked, questions for BA, Product Owner and tech lead

The technical specification for RWB-E1-045 is drafted, but it is *BLOCKED*. The spec gate review failed: 1 High, 1 Medium and 6 Low findings. Planning cannot start until the questions below are answered.

*Why it is blocked, in short:*

# The story file (v1, 28 Oct 2026) was written before *D-RCV-36* (16 Nov 2026, Temporal and Drools). D-RCV-36 rewrote case creation (RWB-E1-018) and allocation (RWB-E1-020). Several product values this story requires are no longer read by any story.
# The story depends on *RWB-E1-043* (reference data service), which is not built. Its spec must be re-done under D-RCV-35 (OPEN-036).
# Four acceptance criteria (AC1, AC2, AC7, AC8) test engines that are built after this story.

*How to answer:* reply in this thread with the question number (for example "Q4: option A"), or write your own answer. If an option needs a change to a story file, please say which version will carry it.

||No.||Owner||Topic||Blocks the spec?||
|Q1–Q10|BA (Kuldeep)|Story text, data layout, messages, business rules|Yes, except Q3|
|Q11–Q13|Product Owner (Chitchaya Muanchonchana)|Required values, scope of "done", run-time failure rule|Yes|
|Q14–Q16|Recovery tech lead / FDA (Jesniphat Pukkham)|Dependencies, component ownership, feature flag|Yes|
|Q17|FDA (Jesniphat Pukkham)|Package name|No (plan gate)|

----

h3. Questions for BA (Kuldeep)

*Q1. Remove the steps that D-RCV-36 replaced?*

* *What the documents say:* RWB-E1-045 §4 step 7 and §13 build step 5 say case creation and allocation read ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET from {{ProductParameterService}}. §10 says SY-RULES (the Drools evaluator) reads product values for allocation.
* *What changed:* Under D-RCV-36, RWB-E1-018 v2 takes the entry threshold from the GLOBAL parameter {{case.entry.dpd}} = 90 (DL16), decides entry and exclusion with the Drools packages ENTRY and EXCLUSION, and reads exposure bands from LOV-EXPOSURE. RWB-E1-020 v2 allocates with the Drools package ALLOCATION. Neither story lists RWB-E1-045 in "Depends on". In D-RCV-36 §4, SY-RULES reads reference values as Drools facts.
* *Why it matters:* The story asks us to change two engines that no longer read these values.
* *Options:* (A) Issue RWB-E1-045 v2 without §4 step 7, §13 step 5 and the SY-RULES row, and update BR1 and BR2 to match. (B) Keep them, and say how case creation and allocation should read product values alongside Drools.
* *Recommendation:* A.
* *Answer needed:* A or B. If A, the version of the new story file.

*Q2. Which story builds the notice timer in AC1, AC7 and AC8?*

* *What the documents say:* AC1, AC7 and AC8 are about a notice timer set from NOTICE_PERIOD_DAYS. For example, AC1 expects the MORTGAGE timer to expire on 2026-12-31 (30 days) and the HP timer on 2027-01-30 (60 days).
* *What we found:* No story in the Epic 1 v7 or Epic 2 v5 story files reads NOTICE_PERIOD_DAYS. RWB-E1-028 v2 (timers) reads only the SERVICE_LEVEL row. RWB-E2-004 reads only CURE_PERIOD_DAYS.
* *Why it matters:* These three ACs cannot be tested in any increment.
* *Options:* (A) Name the story that will build the notice timer and read NOTICE_PERIOD_DAYS, and add that to its story file. (B) Rewrite AC1, AC7 and AC8 around the SERVICE_LEVEL row, which RWB-E1-028 reads in Epic 1. (C) Rewrite them around CURE_PERIOD_DAYS (RWB-E2-004, Epic 2).
* *Answer needed:* A (with the story key), B or C.

*Q3. Is* {{plan.warn-days}} a product parameter? (does not block this story)

* *What the documents say:* The RWB-E2-004 v2 precondition says "RWB-E1-045 is done: CURE_PERIOD_DAYS and {{plan.warn-days}} are product parameters in force (assumed 3)". {{plan.warn-days}} is not in RWB-E1-045 BR2 and is not in the parameter catalog.
* *Answer needed:* Should {{plan.warn-days}} be added to the catalog with scope PRODUCT, and should it be required? Owner and value source?

*Q4. Move the engine steps of AC1, AC2, AC7 and AC8 to the stories that build the engines?*

* *What the documents say:* §13 build steps 4–6 change the timer engine (RWB-E1-028, build #47), case creation (RWB-E1-018, #38) and allocation (RWB-E1-020, #41). This story is #31, so none of these engines exists when it is built. RWB-E1-028 lists RWB-E1-045 as a dependency.
* *Why it matters:* Unchanged, these ACs cannot pass in this increment.
* *Options:*
** (A) This story proves AC1, AC2, AC7 and AC8 at service level: the right value, unit and PRODUCT_PARAMETER version for each product and date, and the "missing value" error. The engine steps (timer written, AUTO_LEASE case created, case placed on the exception queue, version written to the decision log) become ACs of RWB-E1-018 and RWB-E1-028. BA rewrites the four ACs and adds the engine steps to those stories.
** (B) Keep the ACs as written, and accept that RWB-E1-045 is not "done" until RWB-E1-028 is built.
* *Recommendation:* A. The Product Owner must accept the change (Q12).
* *Answer needed:* A or B. If A, the versions of the updated story files.

*Q5. Who places a case on the exception queue when a product value is missing (X5)?*

* *What the documents say:* X5 and BR8 say that when a case's product has no value in force, "no timer is set; the case goes to the exception queue" with MSG-P3-034. RWB-E1-028 v2 X1 already does this for a missing SERVICE_LEVEL version, with MSG-P3-026.
* *Why it matters:* The service in this story only reads values. It reports "missing" and changes no case.
* *Answer needed:* Which story moves the case to the exception queue: RWB-E1-028 for timers, RWB-E1-018 for case creation, or another?

*Q6. Adding a new product: one list or two, and in what order?* (AC2 and AC6)

* *(a) PRODUCT table vs LOV-PRODUCT.* The completeness check uses the PRODUCT reference table. The guardrail says product group is "checked against LOV-PRODUCT". In Reference Data and LOVs v4, LOV-PRODUCT is a closed list of 4 values (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED) owned by the product heads. _Are PRODUCT and LOV-PRODUCT the same list? If not, must both be changed to add AUTO_LEASE, and in which order?_
* *(b) Order of loads.* The check counts "every product in the PRODUCT version in force on the valid from date". In AC2, PRODUCT v2 (AUTO_LEASE) may still be waiting for approval when PRODUCT_PARAMETER v3 is loaded, so it is not "in force". _Must PRODUCT v2 be approved before PRODUCT_PARAMETER v3 and SERVICE_LEVEL v3 are loaded? Or should the check also count a PRODUCT version that is loaded but not yet approved, with the same valid from?_
* *(c) Rows for an unknown product.* _If a PRODUCT_PARAMETER or SERVICE_LEVEL file has rows for a product that is not in the PRODUCT version in force, is the load refused, are the rows ignored, or are they accepted?_
* *(d) Check on approval.* The check runs when a file is loaded. _When an approver approves a PRODUCT version that adds a product, must the system check again that the parameter and service level rows exist? Or is a gap left to the run-time path (X5)?_
* *(e) AC3 Background.* AC3 expects "SERVICE_LEVEL version 3 stays in force". The Background sets business date 2026-12-01 and no SERVICE_LEVEL version. Version 3 comes from AC2 with valid from 2026-12-05. _Please add the SERVICE_LEVEL version in force on 2026-12-01 to the Background._

*Q7. SERVICE_LEVEL columns, and is the queue part of the key?*

* *What the documents say:* RWB-E1-045 §12 gives the service level as {{limit}} + {{unit}} + {{warnPercent}} + {{escalateToRole}}, keyed by product group and case status. RWB-E1-043 AC4 tests a SERVICE_LEVEL column called {{limit_days}}. REQ-CWC-011 says "Service levels per queue and status held as data".
* *Why it matters:* The column names are data in RWB-E1-043, but the code maps them to fixed fields, and the key drives the duplicate check.
* *Please confirm:*
** PRODUCT_PARAMETER columns: {{product_group}}, {{parameter_code}}, {{value}}, {{unit}}; key = product group + parameter code.
** SERVICE_LEVEL columns: {{product_group}}, {{case_status}}, {{limit}}, {{unit}}, {{warn_percent}}, {{escalate_to_role}}; key = product group + case status.
** PRODUCT key: {{product_group}}.
** Which is right, {{limit}} + {{unit}} or {{limit_days}}? (Whichever is chosen, RWB-E1-043 AC4 or RWB-E1-045 §12 must change.)
** Is the queue part of the service level key, as REQ-CWC-011 says?

*Q8. Which message for a value of the wrong type?* (X2)

* *What the documents say:* X2 sends both "outside the range" and "wrong type" to MSG-GEN-002, "{field} must be between {min} and {max}." In the catalog, only NOTICE_PERIOD_DAYS has a range (1–365). ENTRY_DPD, CURE_PERIOD_DAYS, EXCLUSION_LIST and EXPOSURE_BAND_SET have none, so the message would show empty limits. RWB-E1-043 AC4 uses MSG-P3-027 (schema check) for text in a number column.
* *Options:* (A) Wrong type: MSG-P3-027, naming the row and the column. Outside the range: MSG-GEN-002. (B) MSG-GEN-002 for both, with a defined text when there is no range. (C) A new message ID.
* *Recommendation:* A.
* *Answer needed:* A, B or C.
* *Note:* MSG-P3-034 is already in Error and Message Standard v4, in English and Thai. The standard's MSG-P3-027 text ("…The version in force is unchanged.") differs from the story's §14 ("…Version {version} stays in force."). We will use the standard. Please align the story.

*Q9. Working days: are weekends skipped, and which units are allowed?* (BR7)

* *What the documents say:* BR7 says WORKING_DAYS "skips the dates in v_ace_holiday". RWB-E1-028 v2 AC11 counts 5 working days from Monday 2026-12-14 to Monday 2026-12-21, which skips the weekend. Reference Data and LOVs v4 has no list with CALENDAR_DAYS and WORKING_DAYS. The catalog uses {{CALENDAR_DAYS}} for {{case.entry.dpd}} but {{DAYS}} for the five product parameters.
* *Answer needed:*
** Does WORKING_DAYS skip Saturdays and Sundays as well as the {{v_ace_holiday}} dates?
** Can a day-unit list (CALENDAR_DAYS, WORKING_DAYS) be added to Reference Data and LOVs?
** Is the unit a column on each PRODUCT_PARAMETER and SERVICE_LEVEL row (so MORTGAGE could be 30 calendar days while SSME is 20 working days)?

*Q10. Add the missing dependencies to the story?*

* *What the documents say:* The story depends only on RWB-E1-042 and RWB-E1-043. It also needs the {{recovery_case}} and {{timer}} tables (RWB-E1-001, build #9) for the open-case check in AC6, and {{v_ace_holiday}} (RWB-E1-069, build #10) for working days. Neither is built yet.
* *Answer needed:* Please add RWB-E1-001 and RWB-E1-069 to "Depends on" in the next story version, or tell us why they are not needed. The tech lead confirms the order in Q14.

----

h3. Questions for the Product Owner (Chitchaya Muanchonchana)

*Q11. Which product values must every product have?* (please consult the product heads, RW-PRODHEAD, who own these catalog entries)

* *What the documents say:* BR2 makes five values mandatory for every product: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. A load that leaves one out is refused.
* *What changed:* After D-RCV-36 (see Q1 and Q2), only CURE_PERIOD_DAYS (RWB-E2-004) and the SERVICE_LEVEL rows (RWB-E1-028, RWB-E2-015) have a reader. ENTRY_DPD, EXCLUSION_LIST, EXPOSURE_BAND_SET and NOTICE_PERIOD_DAYS have none.
* *Why it matters:* Unchanged, the business must load and approve four values per product that the system never uses, and a load is refused when they are missing.
* *Options:* (A) Keep all five mandatory. (B) Mandatory only for values that a story reads: CURE_PERIOD_DAYS and the SERVICE_LEVEL rows, plus NOTICE_PERIOD_DAYS if Q2 names a reader. The rest stay in the catalog but are not mandatory. (C) Remove the unused values from the catalog.
* *Recommendation:* B. It is a reviewed change to the RWB-E1-042 catalog data; no code changes.
* *Answer needed:* A, B or C, and the list of values that stay mandatory.

*Q12. What counts as "done" for this story?* (linked to Q4)

* *Context:* The story's measure is "a product is added or changed by a reference load with no deployment". The pieces that show this end to end (case creation, timers) are built later, in RWB-E1-018 and RWB-E1-028.
* *Proposal:* RWB-E1-045 is done when (1) the read service returns the right value, unit and version per product and date, (2) loads that break a rule are refused with the right message, and (3) the access test passes. The end-to-end measure is accepted when RWB-E1-018 and RWB-E1-028 are done.
* *Answer needed:* Accept the proposal, or say what must be shown in this increment.

*Q13. When a value is missing at run time: stop the engine, or set the case aside?*

* *What the documents say:* Three stories say three different things:
** RWB-E1-043 BR9: if a reference table has *no version in force*, the engine does not run at all.
** RWB-E1-028 v2 X1: if *no SERVICE_LEVEL version* is in force, the case gets no timer and is listed on the exception queue (MSG-P3-026).
** RWB-E1-045 X5: if a product has *no row* in force, the case gets no timer and goes to the exception queue (MSG-P3-034).
* *Answer needed:*
** When a whole table has no version in force, does the engine stop for every case, or are only the affected cases put on the exception queue?
** Which message applies: MSG-P3-026 or MSG-P3-034?
** Does the same rule apply to PRODUCT_PARAMETER and SERVICE_LEVEL?

----

h3. Questions for the recovery tech lead / FDA (Jesniphat Pukkham)

*Q14. Order of work and what the RWB-E1-043 re-spec must include*

* *Context:* Under the pull rule ("take the next item whose dependencies are done"), RWB-E1-045 cannot be planned until RWB-E1-043 is re-specified (OPEN-036) and built.
* *Please confirm:*
** (a) RWB-E1-045 waits for RWB-E1-043 to be re-specified and built.
** (b) RWB-E1-001 and RWB-E1-069 are also prerequisites (see Q10).
** (c) The RWB-E1-043 re-spec provides a per-table check hook that this story can use for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL loads. The RWB-E1-043 v2 interfaces have none today; in ACE the per-table hook is P4's {{ReferenceTableHandler.check(...)}}.
** (d) The RWB-E1-043 re-spec uses {{UNIQUE (version_id, row_key)}} on {{reference_row}}. Physical Schema v6 has {{UNIQUE (row_key)}}, which stops version 2 of a table from reusing the row keys of version 1.

*Q15. One working-day calculator, in RWB-E1-028*

* *What the documents say:* RWB-E1-045 §13 builds a {{DueDateCalculator}}. RWB-E1-028 v2 builds a {{WorkingDayCalculator}} and the P1 {{holidays()}} query on {{v_ace_holiday}}. RWB-E1-043 v2 §12 says the calculator reads {{v_ace_holiday}} "through the P1 query of RWB-E1-028".
* *Proposal:* Keep one calculator, in RWB-E1-028. RWB-E1-045 returns only the value and its unit.
* *Answer needed:* Agree, or name the owner.

*Q16. What does the feature flag* {{rwb.p3.product-parameters}} switch off?

* *What the story says:* "Off: the engines use the values they read before this story." No engine reads product values yet, so this has no meaning today.
* *Why it matters:* If "off" also switches off the load checks, a load with a missing or wrong value could be approved. That weakens the "refuse in full" control (BR4, CTL-08).
* *Options:* (A) The flag controls only whether the read service is offered to engines; the load checks always run. (B) The flag also switches the load checks off.
* *Recommendation:* A.
* *Answer needed:* A or B.

*Q17. Package name (for the plan gate; does not block the spec)*

* The story puts the published interface in {{recovery.casewf.refdata.api}}. The module map publishes only {{casewf.api}}, where RWB-E1-042 put {{ParameterService}} (D-RCV-20). RWB-E1-043 v2 and RWB-E1-028 v2 also name sub-packages, so one rule is needed for all three stories.
* *Answer needed:* Accept {{casewf.api}}, or allow {{refdata.api}} as a published sub-package.

----

*After the answers:* we update the spec in the same run ({{INC-031-epic-1-RWB-E1-045}}), re-run the spec gate review, and start planning only when RWB-E1-043 is ready.
Draft spec and review: {{output/INC-031-epic-1-RWB-E1-045/specify/spec.md}}, {{output/INC-031-epic-1-RWB-E1-045/review/spec-gate-review.md}} (ace-aisdlc repository).

### Comment 4: NAMTIP WONGSOMBOON, 2026-11-17T09:45:32.896+0700

Comment ID 1793808

@CHANISSARA MAHAKITTIKUN 

Please clarify the issue and provide more details ka. 

### Comment 5: Chanapai Gingpuwaluck, 2026-11-17T11:13:43.765+0700

Comment ID 1794138

These points add to Q1–Q17 of the spec gate review already on this card.

# *No mapping from ACE product codes.* The story does not map ACE product codes ({{v_ace_account.product_code}} / {{product_category}}) to Workbench product groups. AC2 (AUTO_LEASE) assumes the case arrives with the right group.
#* Question: who owns the mapping, where is it held, and what happens to an account whose code does not map?
# *Values still pending.* Service level and cap values wait on DL22 and DL23, both past due 13 Nov.
# *Purpose of the story.* The grooming note describes this story as "validation configuration used to check business rules when data is received from ACE". The story itself is about product parameters held as reference data.
#* Please confirm the room's reading so the spec is not built on two meanings.

Who answers: Data architect, ACE team, Product heads (RW-PRODHEAD).

### Comment 6: SAHIL MORE, 2026-11-17T13:24:13.185+0700

Comment ID 1794445

@thanapat khumprom 

i am pasting a gate-pass.md file here which addresses all the questions that agent is asking



h1. RWB-E1-045 – Spec Gate Response (Latest Baseline v17)

*Story:* RWB-E1-045 Multi-product Parameters for Mortgage, HP and SSME *Latest baseline:* Recovery Workbench Project Hub v17 (16 November 2026) *Spec run:* INC-037-epic-1-RWB-E1-045 *Source reviewed:* RWB-E1-045 v1 text carried in Project Hub v17 *Response date:* 17 November 2026 *Response owner:* BA / Recovery Workbench *Status:* CONDITIONAL PASS *Applies to:* specify/spec.md, specify/compliance-validation.md, specify/agent-run-log.md

h2. 0. How the Technical Specifier Must Use This Response

# Treat Project Hub v17 as the latest consolidated baseline for story text, build order and decisions. If another file disagrees, v17 takes precedence. The old v5 story file dated 4 November 2026 is historical only and must not be used.
# Treat Section 3 as the BA/user response to the gate. Do not ask these questions again.
# Apply Section 2 as the delta for RWB-E1-045 v2. If v2 is not yet available in the requirement folder, this response is the authoritative interim source for the changed sections.
# Update spec.md in place. Do not create a competing replacement specification.
# Record every reply in the Clarification Log using the rows in Section 4. Retain the existing CLAR-001 through CLAR-008 history.
# Re-run the complete specification validation and Compliance Reviewer. The gate can close only after the reviewer has received the updated specification and this response.
# In the specification header:
#* Change Source requirement to the RWB-E1-045 v2 file.
#* Change Prepared to 17 November 2026.
#* Set Status to DRAFT while applying this response.
#* Set Status to SUCCESS only after the reviewer passes.
# Do not start the Implementation Planner until Section 5 indicates READY_FOR_PLANNER.

h2. 1. What the Gate Is Asking

The current specification faithfully reflects the E1-045 v1 text. The latest consolidated baseline is Project Hub v17, dated 16 November 2026, which still carries the v1 story text. The old v5 story file dated 4 November 2026 is superseded.

The source has changed since v1:

* D-RCV-36 (16 November 2026) rewrote RWB-E1-018 and RWB-E1-020 so that entry, exclusion, allocation and assignment are Drools packages evaluated through RuleEvaluator. They no longer read ProductParameterService.
* RWB-E1-028 is the only Epic 1 timer story. It builds SERVICE_LEVEL timers, not notice or cure timers. Notice and cure timers are out of scope in Section 19.
* RWB-E1-043 v2 does not provide a per-table check hook for the product completeness check.
* Physical Schema v6 defines UNIQUE(row_key) on reference_row, not UNIQUE(version_id, row_key).

The gate is therefore not asking the specifier to invent a new design. It requires the BA to reissue the source story and the technical lead/data architect to resolve two dependencies.

The correct approach is to issue RWB-E1-045 v2 and then re-specify. Do not patch the existing specification around v1.

h2. 2. Source Story Delta: RWB-E1-045 v2 Relative to Project Hub v17

*Section 1 – Story*

Remove entry rule, exclusion list and exposure bands. Retain service levels and cure periods. Retain notice periods only when their timer story is scheduled.

*Section 2 – Rationale*

Focus on service levels and cure periods. Include notice periods only if a reader is scheduled.

*Section 3 – Preconditions*

Only E1-028 reads SERVICE_LEVEL through ProductParameterService. E1-018 and E1-020 evaluate Drools packages. Add E1-001. Add E1-069 only if Q15 is rejected.

*Section 4 – Flow Step 6*

Replace the notice timer call to get(..., "NOTICE_PERIOD_DAYS", ...) with the SERVICE_LEVEL read used by E1-028.

*Section 4 – Flow Step 7*

Delete case creation and allocation reads involving entry thresholds, exclusion lists and exposure bands. D-RCV-36 replaced this path.

*Section 5 – Exception Path X5*

E1-045 throws MissingProductParameterException. E1-028 handles SERVICE_LEVEL failures, and E2-004 handles CURE_PERIOD_DAYS failures. These stories move affected cases to the exception queue.

*Section 7 – Acceptance Criteria*

Rewrite AC1, AC2, AC7 and AC8 as service-level outcomes. They must prove the correct value, unit, version per product/date and missing-value error. Engine outcomes move to E1-028 v3 and E2-004 v3.

*Section 8 – Business Rules*

BR1: Every product-specific business parameter, including service level, cure period and notice when scheduled, must be stored as a PRODUCT_PARAMETER or SERVICE_LEVEL row. Product-specific rules such as entry, exclusion, allocation and assignment are Drools package rows, not reference rows.

BR2: Mandatory values are SERVICE_LEVEL rows for every required status and CURE_PERIOD_DAYS. NOTICE_PERIOD_DAYS is mandatory only if a reader exists. ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET are removed from the PRODUCT-scope mandatory list.

*Section 10 – Authority*

Remove the SY-RULES authority row. If a future package needs a product value as a fact, add a new authority row with that wording.

*Section 11 – Data*

Remove timer and recovery_case.queue_id writes under X5. E1-045 reads reference tables and recovery_case only for the AC6 open-case count.

*Section 12 – Contract*

Add queueCode to the serviceLevel(productGroup, caseStatus, businessDate) contract.

ServiceLevel fields are:

* queueCode
* caseStatus
* limit
* unit
* warnPercent
* escalateToRole
* versionNo

*Section 13 – Components*

Remove:

* DueDateCalculator
* TimerEngine
* CaseEntryService
* AllocationService

Add the E1-043 per-table check hook integration.

Retain:

* ProductParameterServiceImpl
* ProductCompletenessCheck
* OpenCaseCounter

*Section 14 – Messages*

Wrong type: MSG-P3-027, naming the row and column.

Out of range: MSG-GEN-002.

*Section 15 – Screens*

No screen is included in this story. E1-028 displays SCR-09.

*Section 16 – Test Cases*

Rewrite TC-01, TC-02, TC-07 and TC-08 as service-level tests. Retain TC-09 access testing.

*Section 18 – Traceability*

Update the test mapping to service-level tests and E1-028/E2-004 end-to-end tests.

*Dependencies*

Add RWB-E1-001. Add RWB-E1-069 only if Q15 is rejected.

h2. 3. Comment-by-Comment Replies

Disposition codes:

* ACCEPTED_SOURCE_CHANGE
* ACCEPTED_SPEC_CLARIFICATION
* DEFERRED_TO_OWNER
* OUT_OF_SCOPE
* NO_CHANGE

h3. 3.1 QA Questions from Nate Trakarntanasuk

*N1 – API endpoint for acceptance criteria*

Reply:

No. Only AC1, AC2 and AC8 use GET /cases//timers. AC1 and AC8 read timer expiry, while AC2 reads the timers of the new AUTO_LEASE case.

AC3 through AC6 assert the POST /admin/reference-loads response and the version in force. AC7 asserts that no timer exists and that the exception-queue row is present.

The specification will make this distinction explicit in the test table.

Disposition: ACCEPTED_SPEC_CLARIFICATION.

Spec action: Update spec.md Test Scenarios and API Change Assessment.

*N2 – Meaning of "the load validates"*

Reply:

Yes. "The load validates" means the loader calls POST /api/recovery/v1/admin/reference-loads with file, table (PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL) and validFrom.

The registry runs E1-043 checks and product completeness, range and duplicate checks synchronously.

* HTTP 201 means VALIDATED.
* HTTP 422 means refused, with nothing written.
* Approval is a separate POST //approve operation.

There is no separate validate endpoint and no dry run in this story.

Disposition: ACCEPTED_SPEC_CLARIFICATION.

Spec action: Update spec.md Entry Trigger and API Change Assessment.

*N3 – TC-E1-045-09 access testing*

Reply:

Yes, provided the access path is in place.

E1-022 and E1-037 are build order 26 and 27. E1-045 is build order 31. Add both dependencies to the preconditions.

If PM-2026.11 is not loaded, record the test as Blocked, not Pass or Fail. Do not mock the role.

The test is valid because it proves that the new table codes use the same Reference data C right.

Disposition: ACCEPTED_SPEC_CLARIFICATION.

Spec action: Update spec.md Test Scenarios and Preconditions, and add the dependencies to story v2.

h3. 3.2 Spec Gate Questions from Thanapat Khumprom

*Q1 – Remove steps replaced by D-RCV-36*

Decision: A.

Issue RWB-E1-045 v2 without Section 4 Step 7, Section 13 Step 5 and the SY-RULES authority row. Update BR1 and BR2.

D-RCV-36 moved ENTRY, EXCLUSION, ALLOCATION and ASSIGNMENT to RuleEvaluator. E1-018 and E1-020 no longer read ProductParameterService.

The v2 file must also remove E1-018 and E1-020 from Sections 3 and 13.

Disposition: ACCEPTED_SOURCE_CHANGE.

*Q2 – Ownership of notice timer*

Decision: B.

Rewrite AC1, AC7 and AC8 around the SERVICE_LEVEL row read by E1-028.

No Epic 1 story builds the notice timer. E1-028 Section 19 places notice and cure timers out of scope.

Option A would name a nonexistent story. Option C would use CURE_PERIOD_DAYS in Epic 2.

Option B keeps the story testable in this release.

Disposition: ACCEPTED_SOURCE_CHANGE.

*Q3 – Is plan.warn-days a product parameter?*

Decision:

No. It is not PRODUCT scope.

Add plan.warn-days to the E1-042 catalog with these attributes:

* Scope: GLOBAL
* Required: Yes
* Default: 3
* Owner: RW-COE
* Value source: DL22

E2-004 is the only reader.

If product heads want a different warning per product, it can become PRODUCT scope, required no, default 3. This is an E2-004 decision and does not block E1-045.

Disposition: DEFERRED_TO_OWNER (PO/catalog).

*Q4 – Move engine steps to the stories that build the engines*

Decision: A, with one correction.

E1-045 proves AC1, AC2, AC7 and AC8 at service level. It verifies the correct value, unit, version per product/date and missing-value error.

Engine steps move to:

* E1-028 v3 for SERVICE_LEVEL timers.
* E2-004 v3 for CURE_PERIOD_DAYS.

They do not move to E1-018 because E1-018 no longer reads product values.

Disposition: ACCEPTED_SOURCE_CHANGE.

*Q5 – Who moves a case to the exception queue?*

Reply:

RWB-E1-028 handles SERVICE_LEVEL timer failures.

RWB-E2-004 handles the CURE_PERIOD_DAYS variant.

E1-028 already has the exception-queue path in X1/AC4 and owns timer start.

E1-045 only throws MissingProductParameterException. It does not move cases.

Disposition: ACCEPTED_SOURCE_CHANGE.

*Q6 – PRODUCT versus LOV-PRODUCT, approval order and unknown-product rows*

Reply:

PRODUCT and LOV-PRODUCT are different lists.

PRODUCT is the versioned reference table of product groups in force. LOV-PRODUCT is the value list used to validate product_group fields. Neither is data_product (DP01-DP14).

The required order is:

# LOV-PRODUCT first.
# PRODUCT v2 second.
# PRODUCT_PARAMETER v3 and SERVICE_LEVEL v3 afterward.

The approval process is a two-phase gate. Parameter and service-level loads may validate against a PRODUCT version that is VALIDATED with the same validFrom. Only approved versions are in force.

Approve PRODUCT first, followed by the other two. Each approval must re-check the data.

Unknown-product rows must cause the entire load to be refused with MSG-P3-034, naming the product and row. They must not be ignored or accepted.

The PRODUCT version must be re-checked at approval.

For AC3 Background, add SERVICE_LEVEL version 2, effective 2026-12-01, with a row for SSME/WAITING_PARTNER.

Disposition: ACCEPTED_SOURCE_CHANGE + E1-043 hook.

*Q7 – SERVICE_LEVEL columns and key*

Reply:

Use limit and unit, not limit_days.

The SERVICE_LEVEL key is queue_code + case_status, or product_group + queue_code + case_status, with product_group retained as a column.

REQ-CWC-011 requires per-queue and per-status configuration. E1-028 flow also refers to the new queue and status.

The keys are:

* PRODUCT: product_group.
* PRODUCT_PARAMETER: product_group + parameter_code.
* SERVICE_LEVEL: queue_code + case_status.

If the room rejects queue in the key, REQ-CWC-011 and E1-028 must be changed instead.

Disposition: ACCEPTED_SOURCE_CHANGE + tech lead confirmation.

*Q8 – Message for wrong value type*

Decision: A.

Wrong type: MSG-P3-027, naming the row and column.

Outside the permitted range: MSG-GEN-002.

Do not use one message for both conditions.

Disposition: ACCEPTED_SOURCE_CHANGE.

*Q9 – Working days and units*

Reply:

WORKING_DAYS skips Saturdays, Sundays and dates in v_ace_holiday.

Add LOV-DAY-UNIT with:

* CALENDAR_DAYS
* WORKING_DAYS

Retire the ambiguous DAYS value.

The unit is a column on each PRODUCT_PARAMETER and SERVICE_LEVEL row. Therefore, MORTGAGE can use 30 calendar days while SSME uses 20 working days.

Disposition: ACCEPTED_SOURCE_CHANGE + catalog.

*Q10 – Missing dependencies*

Reply:

Add RWB-E1-001.

Add RWB-E1-069 only if Q15 is rejected. With Q15 accepted, the working-day calculator moves to E1-028, so E1-069 (v_ace_holiday) belongs to E1-028.

E1-001 is required for the AC6 open-case count against recovery_case.

Disposition: ACCEPTED_SOURCE_CHANGE.

*Q11 – Mandatory product values*

Decision: B.

Mandatory values are limited to values read by a story:

* SERVICE_LEVEL rows for every required status.
* CURE_PERIOD_DAYS.

NOTICE_PERIOD_DAYS is mandatory only if Q2 identifies a reader. Under decision B, it does not.

ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET are Drools package rows, not mandatory catalog values.

The remaining values stay in the catalog but are not mandatory.

The PO must confirm this with RW-PRODHEAD.

Disposition: DEFERRED_TO_OWNER (PO).

*Q12 – Definition of done*

Reply:

Accept the proposal with the Q4 amendment.

The story is done when:

* The read service returns the correct value, unit and version per product and date.
* Loads that break a rule are refused with the correct message.
* The access test passes.

The end-to-end measure is accepted when E1-028 and E2-004 are complete, not E1-018.

Disposition: DEFERRED_TO_OWNER (PO).

*Q13 – Missing value at runtime*

Reply:

The handling depends on the scope of the missing data.

If the entire table has no approved version, the engine must not start its run. The platform administrator is alerted with MSG-P3-027 under E1-043 AC9. Do not put every case on the exception queue.

If the table is in force but a product or row is missing, no timer is created. Only the affected case moves to the exception queue with MSG-P3-034.

Apply the same rule to PRODUCT_PARAMETER and SERVICE_LEVEL.

Use one message for product gaps. Retain MSG-P3-026 only for the legal-period case or retire it from this path.

Disposition: ACCEPTED_SOURCE_CHANGE + PO confirmation.

*Q14 – Order of work, E1-043 hook and UNIQUE constraint*

Reply:

The following decisions are confirmed:

# E1-045 waits for E1-043 v3 re-specification and build.
# E1-001 is required. E1-069 belongs to E1-028 after Q15.
# E1-043 v3 must expose a per-table check hook equivalent to P4's ReferenceTableHandler.check(...). The registry must call this hook during both load and approval.
# Use UNIQUE(version_id, row_key).

Physical Schema v6 currently has UNIQUE(row_key), which prevents version 2 from reusing version 1's row keys.

The schema must be corrected, and a test must prove that two versions can share a row key.

Disposition: DEFERRED_TO_OWNER (tech lead).

*Q15 – One working-day calculator in E1-028*

Reply:

Agree.

There must be one working-day calculator in E1-028.

E1-045 returns only value, unit and version. Remove DueDateCalculator and the v_ace_holiday read from E1-045.

E2-004 uses the timer port rather than implementing its own calculator.

Disposition: ACCEPTED_SOURCE_CHANGE + tech lead confirmation.

*Q16 – Feature flag behaviour*

Decision: A.

The feature flag controls only whether the read service is offered to engines.

Load checks must always run.

Disabling data-integrity checks would allow invalid data to be approved and could cause failures when the flag is enabled again.

E1-028 is new and has no previous execution path, so the feature flag cannot be the only release control for SERVICE_LEVEL timers.

Disposition: ACCEPTED_SPEC_CLARIFICATION.

*Q17 – Package name*

Reply:

Accept recovery.casewf.api.

Published types must be placed in the module's api package under BS-1.2.

Do not introduce refdata.api as a nested published package unless the module map lists it.

Update E1-043 and E1-045 at their next versions. If E1-043 has already shipped refdata.api, list that package in the module map instead of duplicating it.

Disposition: DEFERRED_TO_OWNER (tech lead).

h3. 3.3 Questions from NAMTIP WONGSOMBOON

*NM1 – Clarification of the issue*

Reply:

The issue is scope, not a defect.

Version 1 mixes product reference data with engine behaviour. After D-RCV-36, case creation and allocation read Drools packages, while E1-028 builds only SERVICE_LEVEL timers.

Notice and cure timers are later.

Version 2 narrows E1-045 to reference tables, ProductParameterService and load checks. Engine acceptance criteria move to E1-028 and E2-004.

The blocking questions were Q1, Q2, Q4, Q5, Q7 and Q14.

Disposition: ACCEPTED_SPEC_CLARIFICATION.

h3. 3.4 Additional Questions from Chanapai Gingpuwaluck

*C1 – ACE product-code mapping*

Reply:

The mapping is not part of E1-045.

LOV-PRODUCT-CODE holds the core bank product codes read from ACE through v_ace_product.

The mapping to LOV-PRODUCT is reference data owned by the data steward and data product owner (RW-DATASTEW), and loaded by RW-REFADM.

An account whose code does not map is held on the data quality exception list and receives no case. E2-001 X3/AC5 owns this path.

Moving this responsibility into E1-045 would duplicate E2-001.

Disposition: OUT_OF_SCOPE.

*C3 – Purpose of the story*

Reply:

E1-045 is the data and read-service story.

It owns:

* PRODUCT
* PRODUCT_PARAMETER
* SERVICE_LEVEL
* ProductParameterService contract
* Value, unit, table code, version and missing-value error
* Load completeness, range and duplicate checks

It does not own the engines.

The consumers are E1-028 for SERVICE_LEVEL timers and E2-004 for CURE_PERIOD_DAYS.

Disposition: ACCEPTED_SPEC_CLARIFICATION.

h3. 3.5 Reviewer-Level Replies

*Nate Trakarntanasuk*

Only AC1, AC2 and AC8 use GET /cases//timers. AC3 through AC6 assert the load response and version in force. AC7 asserts no timer and the exception queue.

"The load validates" means POST /admin/reference-loads with synchronous checks. HTTP 201 means VALIDATED; HTTP 422 means refused. Approval is separate.

TC-E1-045-09 is testable with E1-022 and E1-037. If PM-2026.11 is not loaded, it is Blocked, not Pass or Fail.

*Thanapat Khumprom*

Accepted decisions:

* Q1: A, issue E1-045 v2 and remove D-RCV-36-replaced steps.
* Q2: B, SERVICE_LEVEL/E1-028.
* Q3: GLOBAL, not PRODUCT.
* Q4: A amended, E1-028 v3 and E2-004 v3, not E1-018.
* Q5: E1-028 and E2-004.
* Q6: Separate LOV-PRODUCT and PRODUCT lists, two-phase approval, unknown-product refusal, approval re-check and SERVICE_LEVEL v2 Background.
* Q7: limit + unit and queue in the key.
* Q8: A.
* Q9: Skip weekends and holidays, add LOV-DAY-UNIT and use a unit per row.
* Q10: Add E1-001; move E1-069 to E1-028.
* Q11: B.
* Q12: Accept with Q4 amendment.
* Q13: Separate whole-table missing from product-gap handling.
* Q14: Confirm per-table hook and UNIQUE(version_id, row_key).
* Q15: Agree.
* Q16: A.
* Q17: recovery.casewf.api.

E1-045 v2 will be issued and the specification re-run.

*NAMTIP WONGSOMBOON*

The issue is scope, not a defect. Version 1 mixes product reference data/read service with engine behaviour.

After D-RCV-36, case creation and allocation read Drools packages, and E1-028 builds only SERVICE_LEVEL timers.

Version 2 narrows E1-045 to reference tables, ProductParameterService and load checks. Engine acceptance criteria move to E1-028 and E2-004.

*Chanapai Gingpuwaluck*

The product-code map is not part of E1-045.

LOV-PRODUCT-CODE and the mapping to LOV-PRODUCT are reference data owned by RW-DATASTEW and loaded by RW-REFADM. Unmapped accounts are held on the data quality exception list, and E2-001 owns that path.

E1-045 is the data and read-service story, not the engines. It owns the three reference tables, ProductParameterService contract and load checks. E1-028 and E2-004 consume it.

h2. 4. Clarification Log Entries

Add the following entries after CLAR-001 through CLAR-008. Keep all existing entries unchanged.

*CLAR-009*

References: BR1, BR2, Section 4 Step 7, Section 13.

Gap: D-RCV-36 removed case-creation and allocation product reads.

Impact: Two sources of truth if retained.

Response: See Q1. Issue v2 without the replaced steps and rows.

Status: RESOLVED.

Resulting specifications: SPEC-001, SPEC-003.

*CLAR-010*

References: AC1, AC7, AC8.

Gap: No Epic 1 story builds the notice timer.

Impact: Acceptance criteria cannot run in this release.

Response: See Q2. Rewrite around SERVICE_LEVEL and E1-028.

Status: RESOLVED.

Resulting specifications: SPEC-004, SPEC-008, SPEC-009.

*CLAR-011*

References: BR2, E2-004.

Gap: Is plan.warn-days a PRODUCT parameter?

Impact: Catalog and mandatory list.

Response: See Q3. GLOBAL, required, default 3, owner RW-COE, source DL22.

Status: RESOLVED.

Resulting specification: E1-042 catalog and E2-004.

*CLAR-012*

References: AC1, AC2, AC7, AC8.

Gap: Which story owns the engine steps?

Impact: Scope and dependencies.

Response: See Q4. E1-045 at service level; E1-028 v3 and E2-004 v3 own the engines.

Status: RESOLVED.

Resulting specifications: SPEC-001 through SPEC-003, SPEC-008 through SPEC-010.

*CLAR-013*

References: X5.

Gap: Who moves the case to the exception queue?

Impact: Case action ownership.

Response: See Q5. E1-028 handles SERVICE_LEVEL; E2-004 handles CURE. E1-045 throws the exception.

Status: RESOLVED.

Resulting specification: SPEC-010.

*CLAR-014*

References: AC2, AC3, PRODUCT/LOV-PRODUCT.

Gap: Are PRODUCT and LOV-PRODUCT the same? What is the load and approval order?

Impact: New-product path.

Response: See Q6. Different lists; LOV first; two-phase gate; refuse unknown products; re-check at approval; add SERVICE_LEVEL v2 to Background.

Status: RESOLVED.

Resulting specifications: SPEC-002 through SPEC-004 and E1-043 v3.

*CLAR-015*

References: BR3, Section 12.

Gap: SERVICE_LEVEL columns and key.

Impact: Read contract and completeness.

Response: See Q7. limit + unit; queue in the key; PRODUCT key product_group.

Status: RESOLVED.

Resulting specifications: SPEC-004, SPEC-008, E1-043 AC4 and E1-028 v3.

*CLAR-016*

References: X2.

Gap: Which message is used for wrong type?

Impact: Error contract.

Response: See Q8. MSG-P3-027 for wrong type; MSG-GEN-002 for range.

Status: RESOLVED.

Resulting specification: SPEC-005.

*CLAR-017*

References: BR7.

Gap: Working days and unit list.

Impact: Date arithmetic and load schema.

Response: See Q9. Skip weekends and holidays; add LOV-DAY-UNIT; unit per row.

Status: RESOLVED.

Resulting specification: SPEC-009, E1-042 catalog and E1-043 schema.

*CLAR-018*

References: Depends on.

Gap: Missing dependencies.

Impact: Build order.

Response: See Q10. Add E1-001; move E1-069 to E1-028 unless Q15 is rejected.

Status: RESOLVED.

Resulting specification: Story v2.

*CLAR-019*

References: BR2.

Gap: Which values are mandatory?

Impact: Load refusal and product onboarding.

Response: See Q11. B: SERVICE_LEVEL + CURE; NOTICE only with a reader. PO confirmation required.

Status: RESOLVED (PO confirmation pending).

Resulting specification: SPEC-003 and story v2 BR2.

*CLAR-020*

References: Done when.

Gap: What counts as done?

Impact: Gate and acceptance.

Response: See Q12. Accept with Q4 amendment; end-to-end after E1-028/E2-004.

Status: RESOLVED (PO confirmation pending).

Resulting specification: Story v2 Done when.

*CLAR-021*

References: X5, BR8.

Gap: Stop the engine or set the case aside?

Impact: Operations and message.

Response: See Q13. Whole table: stop and alert using MSG-P3-027. Product gap: exception queue using MSG-P3-034. Same for both tables.

Status: RESOLVED.

Resulting specification: SPEC-010 and E1-028 v3.

*CLAR-022*

References: E1-043 dependency.

Gap: Per-table check hook and unique constraint.

Impact: Build blocker.

Response: See Q14. Add the hook and UNIQUE(version_id, row_key); fix schema v6.

Status: RESOLVED (tech lead confirmation pending).

Resulting specification: E1-043 v3 and schema v7.

*CLAR-023*

References: Section 13, BR7.

Gap: Where does the working-day calculator live?

Impact: Duplicate date logic.

Response: See Q15. One calculator in E1-028; E1-045 returns value and unit only.

Status: RESOLVED (tech lead confirmation pending).

Resulting specification: SPEC-009 and E1-028 v3.

*CLAR-024*

References: Feature flag.

Gap: What does the flag switch off?

Impact: Release control.

Response: See Q16. A: the read service only; load checks always run.

Status: RESOLVED.

Resulting specification: SPEC-013.

*CLAR-025*

References: Section 13 package.

Gap: casewf.api or refdata.api?

Impact: Plan gate and boundary test.

Response: See Q17. recovery.casewf.api.

Status: RESOLVED (tech lead confirmation pending).

Resulting specification: SPEC-013.

*CLAR-026*

References: Test scenarios, API.

Gap: Which acceptance criteria use the timers endpoint?

Impact: Test design.

Response: See N1. Only AC1, AC2 and AC8.

Status: RESOLVED.

Resulting specification: Test scenarios.

*CLAR-027*

References: Flow, API.

Gap: What does "the load validates" mean?

Impact: Test design.

Response: See N2. POST /admin/reference-loads; synchronous checks; HTTP 201/422; approval separate.

Status: RESOLVED.

Resulting specification: API Change Assessment.

*CLAR-028*

References: TC-09 access.

Gap: Can the access test run here?

Impact: Test dependency.

Response: See N3. Yes, with E1-022/E1-037; Blocked if PM-2026.11 is not loaded.

Status: RESOLVED.

Resulting specification: Test scenarios and story v2 Depends on.

*CLAR-029*

References: Product-code mapping.

Gap: Who owns the ACE product-code map?

Impact: Scope boundary.

Response: See C1. E2-001; not E1-045.

Status: RESOLVED.

Resulting specification: Out of scope.

*CLAR-030*

References: Purpose.

Gap: One meaning of the story.

Impact: Scope ambiguity.

Response: See C3. Data and read service, not engines.

Status: RESOLVED.

Resulting specification: User story intent.

h2. 5. Readiness and Blockers

*RWB-E1-045 v2 issued*

* Owner: BA Kuldeep
* Status: OPEN
* Closure condition: v2 is available in the requirement folder with the Section 2 delta.
* Blocks: Specification re-run and gate closure.

*Specification updated from this response*

* Owner: Technical Specifier
* Status: READY
* Closure condition: spec.md and Clarification Log updated.
* Blocks: Gate closure.

*Compliance Reviewer re-run*

* Owner: Compliance Reviewer
* Status: NOT RUN
* Closure condition: Reviewer receives updated specification and this response.
* Blocks: Gate closure.

*E1-043 v3 per-table check hook*

* Owner: Tech lead / BA
* Status: OPEN
* Closure condition: E1-043 v3 adds the hook and the registry calls it on load and approval.
* Blocks: Implementation.

*reference_row unique constraint*

* Owner: Data architect
* Status: OPEN
* Closure condition: Schema v7 or corrective migration uses UNIQUE(version_id, row_key), with a test proving that two versions can share a row key.
* Blocks: AC2 and implementation.

*E1-028 v3 exception queue and message*

* Owner: BA / Tech lead
* Status: OPEN
* Closure condition: E1-028 X1/AC4 uses MSG-P3-034 for product gaps and E1-069 is added.
* Blocks: End-to-end AC1/AC7.

*E2-004 v3 cure timer*

* Owner: BA
* Status: OPEN
* Closure condition: E2-004 uses CURE_PERIOD_DAYS through ProductParameterService and TimerScheduler.
* Blocks: End-to-end cure path.

*Q11 mandatory list*

* Owner: PO Chitchaya
* Status: OPEN
* Closure condition: PO confirms decision B with RW-PRODHEAD.
* Blocks: BR2 and load checks.

*Q12 definition of done*

* Owner: PO Chitchaya
* Status: OPEN
* Closure condition: PO accepts the Q4-amended definition.
* Blocks: Gate closure.

*Q14 order, hook and unique constraint*

* Owner: Tech lead Jesniphat
* Status: OPEN
* Closure condition: Tech lead confirms points (a) through (d).
* Blocks: Implementation.

*Q17 package name*

* Owner: Tech lead Jesniphat
* Status: OPEN
* Closure condition: Tech lead accepts recovery.casewf.api.
* Blocks: Plan gate.

*Planner readiness*

READY_FOR_PLANNER: NO.

The Implementation Planner must not start until all of the following are complete:

* RWB-E1-045 v2 is issued.
* The specification is updated.
* The Compliance Reviewer has re-run and passed.
* PO confirmations Q11 and Q12 are received.
* Tech lead confirmations Q14 and Q17 are received.

Additionally, E1-043 v3 and the schema fix must be merged before the builder starts, even if the specification gate closes earlier.

h2. 6. Machine-Readable Decision Summary (Text Format)

Story: RWB-E1-045

Latest baseline: Recovery Workbench Project Hub v17 (14 Story Updates, 16 November 2026).

Spec run: INC-037-epic-1-RWB-E1-045.

Response date: 17 November 2026.

Status: CONDITIONAL_PASS.

Required source story version: v2.

Ready for Planner: FALSE.

Gate closure requires:

# Updated specification based on this response.
# Compliance Reviewer re-run.
# PO confirmation of Q11 and Q12.
# Tech lead confirmation of Q14 and Q17.

*Decisions*

* N1: Only AC1, AC2 and AC8 use the timers endpoint. Type: Spec clarification.
* N2: Load validation means POST /admin/reference-loads with synchronous checks. Type: Spec clarification.
* N3: Access test is valid with E1-022 and E1-037. Type: Spec clarification.
* Q1: Decision A. Issue v2 and remove D-RCV-36-replaced steps. Type: Source change.
* Q2: Decision B. SERVICE_LEVEL timer belongs to RWB-E1-028. Type: Source change.
* Q3: GLOBAL, required, default 3, owner RW-COE, source DL22. Type: Deferred to owner.
* Q4: Decision A amended. Engine targets are RWB-E1-028 v3 and RWB-E2-004 v3. Type: Source change.
* Q5: RWB-E1-028 and RWB-E2-004 own exception-queue actions. Type: Source change.
* Q6: PRODUCT and LOV-PRODUCT are different lists. Load order is LOV-PRODUCT, PRODUCT v2, PRODUCT_PARAMETER v3 and SERVICE_LEVEL v3. Approval is two-phase, with PRODUCT approved first. Unknown-product rows are refused with MSG-P3-034. Approval re-check is required. Add SERVICE_LEVEL v2 to AC3 Background. Type: Source change.
* Q7: Use limit and unit, not limit_days. Queue is part of the key. Key is queue_code and case_status. Type: Source change.
* Q8: Wrong type uses MSG-P3-027. Out-of-range uses MSG-GEN-002. Type: Source change.
* Q9: Skip weekends and holidays. Add LOV-DAY-UNIT. Unit is stored per row. Type: Source change.
* Q10: Add RWB-E1-001. Move RWB-E1-069 to RWB-E1-028. Type: Source change.
* Q11: Decision B. Mandatory values are SERVICE_LEVEL and CURE_PERIOD_DAYS. NOTICE_PERIOD_DAYS is mandatory only if a reader exists. Type: Deferred to owner.
* Q12: Accept the Q4-amended definition of done. End-to-end acceptance targets E1-028 and E2-004. Type: Deferred to owner.
* Q13: Whole-table missing version means stop the run and alert with MSG-P3-027. Product-specific gap means exception queue with MSG-P3-034. Apply to both tables. Type: Source change.
* Q14: Wait for RWB-E1-043 v3. Require per-table check hook and UNIQUE(version_id, row_key). Fix Schema v6. Type: Deferred to owner.
* Q15: One calculator in RWB-E1-028. E1-045 returns value, unit and version only. Type: Source change.
* Q16: Feature flag controls the read service only. Load checks always run. Type: Spec clarification.
* Q17: Use recovery.casewf.api. Type: Deferred to owner.
* NM1: Narrow scope to data and read service, not engines. Type: Spec clarification.
* C1: Product-code mapping is out of scope for E1-045 and belongs to E2-001. Type: Out of scope.
* C3: E1-045 owns reference data and read service, not engines. Type: Spec clarification.

*Blocking dependencies*

# E1-043-HOOK

* Owner: Tech lead / BA.
* Status: OPEN.

# REFERENCE_ROW-UNIQUE

* Owner: Data architect.
* Status: OPEN.

# E1-028-V3

* Owner: BA / Tech lead.
* Status: OPEN.

# E2-004-V3

* Owner: BA.
* Status: OPEN.

# PO-Q11

* Owner: Product Owner.
* Status: OPEN.

# PO-Q12

* Owner: Product Owner.
* Status: OPEN.

# TECH-LEAD-Q14

* Owner: Tech lead.
* Status: OPEN.

# TECH-LEAD-Q17

* Owner: Tech lead.
* Status: OPEN.

### Comment 7: VAISHNAVI KAULGE, 2026-11-17T16:19:24.355+0700

Comment ID 1795118

@Nate Trakarntanasuk 


h3. 1. Does every AC call {{GET /cases/{caseId}/timers}}?

No. Section 12 says this endpoint is "Used to check AC1, AC2 and AC8", the three ACs that end in a timer date. The other ACs check something else:

||AC||What to call or check||
|AC1|{{GET /cases/{caseId}/timers}} for both cases. Check {{expiresAt}} is 2026-12-31 for Mortgage and 2027-01-30 for HP. The {{Timer}} response has no version field, so "records PRODUCT_PARAMETER version 2" is checked in the decision log entry for the timer start. That entry is written by RWB-E1-028.|
|AC2|The new AUTO_LEASE case, then {{GET .../timers}} on it. "No deployment" is checked from the release record, not an API.|
|AC3|{{POST /admin/reference-loads}} (SERVICE_LEVEL). Expect 422 with MSG-P3-034 naming SSME and WAITING_PARTNER. Then check version 3 is still in force.|
|AC4|{{POST /admin/reference-loads}} (PRODUCT_PARAMETER). Expect 422 with MSG-GEN-002 naming NOTICE_PERIOD_DAYS, 1 and 365.|
|AC5|{{POST /admin/reference-loads}}. Expect 422 with MSG-P3-027 naming MORTGAGE and NOTICE_PERIOD_DAYS.|
|AC6|{{POST /admin/reference-loads}} (PRODUCT). Expect 409 with MSG-P3-027 naming UNSECURED and 3 open cases.|
|AC7|{{GET .../timers}} should show no notice timer. The case should also be in the exception queue with MSG-P3-034.|
|AC8|{{GET .../timers}} for both cases. RW-2026-000101 stays 2026-12-31 and RW-2026-000150 is 2027-01-17.|

Two gaps to raise with the BA:

* *"Stays in force" checks (AC3–AC6):* the story names no read endpoint for these. The only read endpoint nearby is {{GET /admin/lists/{listCode}}} from E1-043, which reads lists of values. The story says the criteria run "against a PostgreSQL test container", so this is probably checked with {{ReferenceDataService.versionInForce(...)}}.
* *Exception queue check (AC7):* the story shows it on screen SCR-09 and names no endpoint for it.

h3. 2. What does "the load validates" mean?

It is not a separate step or call. It is the {{POST /api/recovery/v1/admin/reference-loads}} call.

* *What the call does:* the administrator uploads the file ({{file}}, {{table}}, {{validFrom}}) as multipart/form-data. The reference data service then runs its checks inside that request (E1-043 flow steps 2–4, E1-045 flow steps 3–4). These are:
** the E1-043 checks on table code, row schema, keys, valid from date and author;
** the product completeness check, which tests required rows, range and type, duplicates, and open cases on a removed product.
* *If every check passes:* the call returns 201 {{ReferenceLoad}} with status VALIDATED. This is not live yet.
* *If any check fails:* the whole load is refused (422, or 409 for AC6). Nothing is written, and the version in force is unchanged.
* *After validation:* the approver calls {{POST /admin/reference-loads/{loadId}/approve}}, and the version takes effect on its valid from date. AC2's "all three versions are approved" means that approve call, made once per version.

So in AC3 and AC5, "When the load validates" means "when the file is posted and checked". The assertion is the 422 response plus the version in force.

h3. 3. Can TC-E1-045-09 (Access) be tested in this story?

Yes. It is a live test in section 16 and in the regression suite. It covers "Access" rather than an AC, like every story's access case (compare TC-E1-043-11).

* *Call:* {{POST /admin/reference-loads}} with {{table=PRODUCT_PARAMETER}}. The endpoint requires Reference data C, and section 12 lists 403 with MSG-P4-002.
* *User:* RW-PHONECOL, which holds Reference data R only.
* *Expected:*
** 403 with MSG-P4-002 ("You cannot {action} here. Your role does not include it.").
** Nothing changes: no new {{reference_version}}, and the version in force is unchanged.
** The refusal is logged.

Tips for testing it:

* Send an otherwise valid file. That shows the refusal is caused by the role and not by file content.
* Check that the 403 comes before validation. No MSG-P3-034, MSG-P3-027 or MSG-GEN-002 should appear.
* Use the test users that exist in SIT and UAT only.
* E1-045 adds no new permission code. The role check belongs to the P4 endpoint and the E1-043 permission matrix, so this test confirms that PRODUCT_PARAMETER loads go through that same check.

### Comment 8: VAISHNAVI KAULGE, 2026-11-17T16:59:03.108+0700

Comment ID 1795356

@Chanapai Gingpuwaluck 

# *Mapping from ACE product codes to Workbench product groups*

This is outside RWB-E1-045. The story owns PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL, the ProductParameterService contract and the load checks.

* ACE holds public.product with product_key, product_type, product_category and product_category_efs. account.product_key is a nullable foreign key to it. ACE has no Workbench product group column. The old Workbench source_code_map was removed under D-RCV-35.
* RWB-E1-018 v2 reads the group from v_ace_account.product_category. RWB-E2-001 reads it from product_key through a map (LOV-PRODUCT-CODE to LOV-PRODUCT) that is listed as a precondition. The two stories use different sources.
* LOV-PRODUCT is a closed list of 4 (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED), owned by the product heads. LOV-PRODUCT-CODE is a source list read from ACE through v_ace_product, owned by the data steward and data product owner. The map between them is not defined as a list, and its owner and location are not named.
* No story defines what happens to an account whose code does not map. RWB-E2-001 X3/AC5 covers a missing customer (person_key), not a missing product code.
* AC2 (AUTO_LEASE) assumes the case arrives with the right group. Adding AUTO_LEASE needs a new LOV-PRODUCT value, a PRODUCT row, and the link from ACE to it.

Decisions needed from the data architect and the ACE team:

# Confirm whether product_category reliably holds the four group values.
# Pick one source of the group for RWB-E1-018 and RWB-E2-001. If a map is needed, name its owner and who loads it.
# Add an unmapped-account path to the chosen story. Proposal: the account gets no case and is listed for the data steward.

RWB-E1-045 only needs the resulting group strings to match LOV-PRODUCT. This does not block the spec.

# *Values still pending (DL22 and DL23)*

DL22 (service levels per case state, owner business lead) and DL23 (caseload cap and queue rules, owner product owner) were due 13 Nov 2026 and are still open in Decision Log v10.

* The build and the tests do not need the real values. The story fixes the lookup and the load checks. Tests use synthetic values.
* A SERVICE_LEVEL or PRODUCT_PARAMETER version cannot be approved with invented numbers.
* While DL22 is open, RWB-E1-028 has no real service levels in production.

Decisions needed:

# The business lead closes DL22 and the product owner closes DL23.
# The product heads (RW-PRODHEAD) supply the values per product.
# Proposal: if the values slip past the 30 Nov 2026 release, record them as assumed in the story, as the other stories do. The first approved loads then carry those values.

# *Purpose of the story*

RWB-E1-045 is the data and read-service story for product parameters.

* It owns the reference tables PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL, the ProductParameterService contract (value, unit, table code, version, missing-value error), and the completeness, range, type and duplicate checks on loads.
* It does not validate data received from ACE, does not hold business rules, and does not own the engines.
* RWB-E1-028 reads the SERVICE_LEVEL rows. RWB-E2-004 reads CURE_PERIOD_DAYS. Entry, exclusion, allocation and assignment are Drools packages under D-RCV-36 and do not read this story.

{quote}{quote}

### Comment 9: Chanapai Gingpuwaluck, 2026-11-18T16:59:32.912+0700, edited 2026-11-18T17:01:01.533+0700

Comment ID 1797371

@VAISHNAVI KAULGE  @SAHIL MORE Thank you for the replies. C3 (purpose of the story) is closed. Five points remain open.

# *Two different answers on C1.* The gate response (17 Nov 13:24) says the map from LOV-PRODUCT-CODE to LOV-PRODUCT is reference data owned by RW-DATASTEW and loaded by RW-REFADM, and that an unmapped account goes to the data quality exception list under RWB-E2-001 X3/AC5. The reply of 17 Nov 16:59 says the owner and location of the map are not named, and that RWB-E2-001 X3/AC5 covers a missing person_key, not a missing product code.
#* Question: which answer stands? If the gate response stands, RWB-E2-001 needs its own exception path and AC for an unmapped product code.
# *One source for the product group.* RWB-E1-018 v2 reads the group from v_ace_account.product_category, and RWB-E2-001 reads it through the map. RWB-E1-018 is Epic 1 and RWB-E2-001 is Epic 2, so in Epic 1 no story handles an account whose code does not map.
#* Question: which source does Epic 1 use, and which Epic 1 story holds the unmapped-account path until RWB-E2-001?
# *AC2 "no deployment" with a closed LOV-PRODUCT.* Adding AUTO_LEASE needs a new LOV-PRODUCT value, a PRODUCT row and the link from ACE. LOV-PRODUCT is a closed list of four values.
#* Question: please confirm that no code, Drools package or CHECK constraint lists the four groups, so that AC2 really passes with no deployment.
# *DL22 and DL23.* Both are past due (13 Nov) and the reply gives no new date. It also says a version cannot be approved with invented numbers, but proposes approving the first loads with assumed values.
#* Question: what is the new date for DL22 and DL23, and who signs off the assumed values (RW-PRODHEAD, business lead) if they are used for the first approved loads?
# *RWB-E1-045 v2.* The gate response says v2 will be issued and the specification re-run. No v2 is attached yet, and the engine ACs are to move to RWB-E1-028 v3 and RWB-E2-004 v3.
#* Question: when will v2 and the two receiving stories be issued?

Who answers: Henka (BA), Data architect, ACE team, Business lead, PO.

@CHANISSARA MAHAKITTIKUN 


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
