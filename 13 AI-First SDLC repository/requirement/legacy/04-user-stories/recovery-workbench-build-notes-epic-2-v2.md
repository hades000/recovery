<!-- source: 04 User stories/Recovery Workbench Build Notes Epic 2 v2.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench Build Notes Epic 2 v2.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench build notes, Epic 2

SCB Collections and Recovery. Henka Group.

(C) Siam Commercial Bank and Henka Pte Ltd

Every flow step of every story in Epic 2, written out in full so it can be followed without knowing the Workbench already. Each entry gives the step as the story states it, then what it means: who acts, what runs on its own, and what has to be built. The story remains the specification. Where the two differ, the story governs.

## RWB-E2-001 EFS hand-over with full history from the COLLINS load

Module: P2 Integration

### Step 1

**In the story.** Scheduler: JOB-02 starts after JOB-01 publishes LoadCompleted (EV-26) for sources ALS and EFS with business date D.

Nothing is started by hand. JOB-01 publishes LoadCompleted (EV-26) once its load checks pass, and your LoadCompletedListener consumes that event for sources ALS and EFS with the same business date before HandoverJob begins. Put the listener behind IdempotencyGuard from RWB-E1-007, so a redelivered event does not start a second run; events are often delivered more than once, and the guard keeps the work to one time per key. Build HandoverJob as the JOB-02 step in the Java package recovery.integration.handover, and chain JOB-03 allocation after it. The feature flag for the story is rwb.integration.efs-handover.

### Step 2

**In the story.** SY-DATALOAD: the HandoverService checks that both data products carry business date D; if not, it holds the run (step X3).

HandoverService makes this check itself. Confirm that both the ALS and EFS data products carry business date D before any account is read. When one is older, hold the run: create no case from the earlier day's data, show MSG-P1-001 against the stale product with the date it holds, and alert the data steward with MSG-P2-007, which names the date and the number of accounts waiting. No case is built from a load that did not pass its checks, per BR4. When a day is missed, the next good load covers it and the run summary names the gap date, which AC6 shows as 2026-12-15 with cases created on 2026-12-17.

### Step 3

**In the story.** SY-DATALOAD: reads through the P1 AccountQuery every account with days_past_due at or above the threshold and no open case link on business date D.

This runs under the SY-DATALOAD managed identity with no person involved. Call AccountQuery.findAtOrAboveDpd(threshold, businessDate) from the P1 published interface recovery.data.api, and take the threshold from the parameter case.entry.dpd_threshold, in force at 90 per DL16. Do not write 90 into the code and do not read the account tables directly. The call returns the EntryCandidate rows for accounts at or above the threshold on business date D with no open case link. Your module reads loan_account values through that interface only: the product code, the total balance, the days past due and the data as of date.

### Step 4

**In the story.** SY-DATALOAD: for each account, calls IdempotencyGuard.firstTime("handover", accountId + ":" + D); a repeat is skipped and counted.

Your code makes this call for each account before any write. IdempotencyGuard from RWB-E1-007 remembers the keys it has already seen, so a second run for the same account and business date does the work only once. Idempotent means running the same request twice leaves the same result as running it once. The key is the fixed text handover with the account id and the business date, exactly as the step writes it, and section 12 gives the job's idempotency key as account ID plus business date. An account whose key is already present is skipped and counted as a repeat in the run summary, which is exception path X1 and AC2.

### Step 5

**In the story.** SY-DATALOAD: groups the accounts by primary customer and product group (DL17).

HandoverGroupBuilder does this grouping. Two accounts of the same customer in the same product group belong to one case, per BR2 and decision DL17, so group the candidates by primary customer and product group before any case is created. The product group comes from the account's product code through the loaded product code map, LOV-PRODUCT-CODE to LOV-PRODUCT, which is reference data and not a value in code. Build this with tests for one account and for two accounts per customer and product group, as build step 1 says. An account whose customer is not in the party data is dropped and listed in the data quality exceptions, which is exception path X3 and AC5.

### Step 6

**In the story.** SY-CASEWF: for each group, CaseCreation.createOrLink writes the decision log entry first, then creates the case with status New, case number RW-YYYY-NNNNNN and entry date D+1, or links the account to the customer's open case for the product group.

Your service calls CaseCreation.createOrLink from the P3 published interface for each group, and P3 does the writing. It writes the decision log entry first, then creates the case with status New, a case number in the form RW-YYYY-NNNNNN and entry date D+1, or links the account to the customer's open case for that product group. For a link it writes the case_account row with linked_from and is_primary false and creates no new case, which is exception path X5 and AC4. The call throws DecisionLogUnavailableException: stop that account, count it as held, raise the incident and leave it for the next run.

### Step 7

**In the story.** SY-CASEWF: publishes CaseCreated (EV-01) with the business date, in the same transaction.

P3 publishes the event and you build nothing for it. CaseCreated (EV-01) goes out through the P3 outbox in the same transaction as the case row, so the event exists only when the case does. An outbox is a table the event is written to beside the data, with a separate sender delivering it afterward. The event carries the business date, which AC1 checks as 2026-12-14 even though the case was created on 2026-12-15. What your code must get right is passing that business date into the request, and the same date into the inputs snapshot of the decision log entry, which AC1 also checks.

### Step 8

**In the story.** SY-DATALOAD: reads the EFS contact and promise records for the account and appends them through InteractionLedger.appendEfsHistory with source system EFS.

SY-DATALOAD does this once the case exists. Read the account's EFS records with EfsHistoryQuery.forAccount(accountId, businessDate) from P1, limited to the action codes of the collection period that DL29 lists, and pass them to InteractionLedger.appendEfsHistory(caseId, records), which returns the number of entries written. Each interaction entry carries the time it occurred, the channel, direction, action code, contact result, promise amount, promise date and source_system EFS, per BR5. AC1 sets the count: 14 contact records and 2 promises give 16 entries with source system EFS. Do not log the content of these entries; the guardrails allow counts and synthetic keys only.

### Step 9

**In the story.** SY-DATALOAD: writes the run summary: accounts read, cases created, accounts linked, repeats, held; JOB-03 allocation follows.

HandoverService returns HandoverSummary with the accounts read, the cases created, the accounts linked, the repeats, the held accounts and the gap dates, and HandoverSummaryRepository writes it to interface_run.checks. The data steward reads it on SCR-45 Data quality, together with the accounts held because their customer was missing. Carry MSG-P7-003 on the summary for an account stopped by a failed decision log write, which is AC7. JOB-03 allocation runs after this job, so the new cases get a queue and an owner the same morning. A rerun requested while JOB-02 is still running is refused with 409 and MSG-P2-006.

## RWB-E2-002 ACE plan status on the case

Module: P2 Integration

### Step 1

**In the story.** Scheduler: the plan status step runs in JOB-02 after the case creation step, once a day.

No person starts this. JOB-02 already runs once a day and creates cases from the COLLINS load, built in RWB-E2-001. You add PlanStatusStep as a second step of the same job, ordered after the case creation step, so every case created that morning is covered in the same run. Put the step behind the feature flag rwb.integration.ace-plan-status, so it can be switched off without a release. This step is the daily path; the endpoint of step 8 is the live path for a single case. Both read the same stored columns, and the daily step is what keeps them current when nobody opens the case.

### Step 2

**In the story.** SY-DATALOAD: the PlanStatusService lists every open case with its account numbers through the P3 CaseQuery.

The step does this, running under the service identity SY-DATALOAD. PlanStatusService asks the P3 CaseQuery interface for every open case with its account numbers. The numbers come from case_account and loan_account.account_no, and the account number is the join key between a Workbench case and an ACE plan under DL21, because the two systems share no case identifier. Read them through the P3 interface rather than querying recovery_case or loan_account yourself, since other modules own those tables. Build PlanStatusService in package recovery.integration.aceplan. The result is the work list for the rest of the step: one entry per open case with the account numbers to ask ACE about.

### Step 3

**In the story.** SY-DATALOAD: calls RestructurePlanQuery.statusFor with the account numbers in batches of 500 (assumed; DL11).

The service does this through AcePlanClient, which you build as a thin wrapper around the ACE published interface RestructurePlanQuery. Call statusFor with a list of account numbers and read back one PlanStatusView per plan, holding planRef, accountNo, status and statusDate. Send the account numbers in batches of 500, set by the property rwb.ace.plan.batch-size, and apply a 2-second timeout from rwb.ace.plan.timeout-ms. ACE is reached this way only, never by reading ACE tables. When ACE does not answer inside the timeout, the whole step changes nothing, writes MSG-GEN-006 naming the ACE common module on the run summary, and leaves every case to the next run.

### Step 4

**In the story.** SY-DATALOAD: for each plan returned, compares status and status date with the stored values; an unchanged plan is skipped.

The service compares, with no person involved. For each plan returned, read the stored plan_status and plan_status_as_of on the case and compare them with the status and status date from ACE. An unchanged plan is skipped, which costs nothing and raises no event. The idempotency key for this step is the case ID with the plan reference, the status and the status date, so a rerun on the same day writes no second row and raises no second event. Check the status against the list LOV-PLAN-STATUS, which holds CREATED, APPROVED, BOOKED and BROKEN. A code such as SUSPENDED is not stored and gets a data quality exception with the check Lists of values.

### Step 5

**In the story.** SY-CASEWF: writes plan_ref, plan_status and plan_status_as_of on the case through CasePlanStatus.update.

The write goes through P3, called by the service and not by a person. CasePlanStatus.update takes the case ID, the plan reference, the status and the status date, and writes plan_ref, plan_status and plan_status_as_of on recovery_case. P3 adds those three columns, varchar(30), varchar(10) and a date, in its own migration for this story; P2 gets no table of its own here. Call the interface rather than updating recovery_case directly, because the case table belongs to P3. After this write the rules component and the case record view both read the stored status, which is what keeps litigation away from a customer who is paying a plan.

### Step 6

**In the story.** SY-DATALOAD: on a change to BROKEN, looks up the event in the plan event map and calls CaseEvents.raise with plan_status = broken and the break count.

The service does this when the status has just changed to BROKEN. Read the plan event map, a versioned reference table whose rows hold an ACE status, a route state and a rule event, loaded by the center of excellence analyst. A case in route state PLAN_CURE_PERIOD maps to the event CURE_PERIOD_EXPIRED; any other route state maps to TREATMENT_BROKEN. Then call CaseEvents.raise on P3 with the case ID, that event code and the facts, which include plan_status broken and the break count. Build PlanEventMap as a rule table, so a row can be added without a release. The event, and not this step, is what moves the case.

### Step 7

**In the story.** SY-RULES and SY-CASEWF: evaluate the rule for the case's route state, write the decision log entry, move the route state and place the case in the case owner's queue with a task.

This runs in P3 and P4 after the event, with no person involved, and your work is to handle what comes back. SY-RULES evaluates the rule for the current route state: R-RES-29 moves PLAN_CURE_PERIOD to PLAN_BROKEN, R-RES-30 moves PLAN_BROKEN to BACK_TO_ROUTE_DECISION while the break count is below restructure.max_breaks, which is 2, R-RES-31 bars a further restructure at that limit, and R-LIT-02 returns a litigation case to the legal route. Each move writes a decision log entry with the rule ID and version, and SY-CASEWF places the case in the case owner queue with a task due in 5 working days. CaseEvents.raise throws DecisionLogUnavailableException when the entry cannot be written: catch it, leave the route state alone, raise an incident with MSG-P7-003, and let the next run raise the event again.

### Step 8

**In the story.** Case owner: opens the case record view; the front end calls GET /cases/{caseId}/plan-status, which reads ACE live with a 2-second timeout and falls back to the stored status.

A person triggers this one by opening the case record view, SCR-03. Build GET /cases/{caseId}/plan-status on PlanStatusController with an access check for Case record right R and the scope check, which answers 404 with MSG-P4-003 for a case outside the scope of the caller. The endpoint tries ACE live with the same 2-second timeout and falls back to the stored status when ACE is slow or silent. The response holds planRef, status, statusDate, a live flag that is true only when the value came from ACE just now, and a message code. Build PlanStatusPanel to show the plan, the status and the date, with MSG-P2-008 and the stored date when live is false. The read writes nothing.

### Step 9

**In the story.** SY-DATALOAD: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a data quality exception for the ACE team.

The daily step does this with no person involved. A case can hold a plan reference that ACE no longer returns any status for. Keep the stored plan_status and plan_status_as_of as they are, because the last known status is of more use than none, and write a data quality exception naming the plan with product DP04 so the ACE team can follow it up. The data steward and the platform administrator read those exceptions with Platform administration right R. The case record view then shows MSG-P2-008 with the stored date, which tells the case owner the status on screen is from an earlier day.

## RWB-E2-003 Customer's other products on the case

Module: P2 Integration

### Step 1

**In the story.** Case owner: opens SCR-03 Case record for a case in scope.

A person does this, on a screen that already exists. SCR-03 Case record went live with Epic 1, and this story adds one panel to it, the React component OtherProductsPanel in src/modules/recovery/case. Build the panel with four states: loading, the product list, the stale banner and the empty state. The case has to be in the caller's scope, which for a case owner means a case they own, and the server tests that in step 3 rather than the screen. Put the panel behind feature flag rwb.integration.customer-products, so SCR-03 can ship without it if the work is unfinished.

### Step 2

**In the story.** Front end: calls GET /cases/{caseId}/customer-products.

This happens on its own when the panel loads. Build the new endpoint GET /cases/{caseId}/customer-products with path parameter caseId, authorized by Case record R with scope applied. The response is CustomerProducts, holding dataAsOf, stale, messageCode and items, where each item carries partyId, partyRole, productType, accountNo already masked for the caller, productStatus and dataAsOf. The controller is CustomerProductsController in package recovery.integration.customer. The endpoint is read only, so it needs no idempotency key. Its errors are 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003 and 503 with MSG-GEN-006, each returned in the Problem shape.

### Step 3

**In the story.** System: checks the Case record right and the scope of the case.

This happens on its own before any data is read. The access check tests that the caller's session holds right R in capability area Case record, and refuses with 403 and MSG-P4-002 otherwise, as for RW-REFADM. Then test the scope: a case owner with scope Own passes only for a case they own. A case outside the scope answers 404 with MSG-P4-003 rather than 403, so the caller learns nothing about a case they may not see. Both checks sit in the controller and the service, and no party or product row is read until they pass.

### Step 4

**In the story.** System: reads the borrower and co-borrower parties of the case through the P3 CaseQuery.

This happens on its own in CustomerProductsService. Call CaseQuery.partiesOf(caseId, partyRoles) on the P3 published interface, passing the party roles from property rwb.customer.products.party-roles, which holds BORROWER and CO_BORROWER. Reading the case_party rows directly is not allowed; every cross-module read goes through the published interface. The result is the party IDs whose products the panel will show. Keep the role list in the property so the business can add a party role without a code change, and carry the party role on each item in the response so the screen can show whose product each line is.

### Step 5

**In the story.** System: reads each party's products through the P1 CustomerProfileQuery, excluding accounts already linked to the case.

This happens on its own. Call CustomerProfileQuery.otherProducts(partyIds, excludeAccountIds) on the P1 published interface. The exclude set is the account IDs already on the case, read from case_account, so the case's own account never appears in the panel. The products come from party_product, a P1 table in data product DP02 that the COLLINS customer profile load fills through JOB-01 from UDP, SCBPDM and the core bank batch. Agree PartyProductView with the P1 squad first and build a stub to test against. A party with no other product gives an empty list, which the panel shows with MSG-P2-017.

### Step 6

**In the story.** System: compares data_as_of with the expected business date of DP02; if older, sets the stale marker.

This happens on its own. Call DataProductStatus.freshness for DP02, which returns dataAsOf, expectedBusinessDate and a stale boolean. When the loaded date is older than the expected business date, set stale true on the response with messageCode MSG-P1-001, and log a stale read event holding the case ID and DP02. The products still go back to the caller, carrying the date they were loaded, so the case owner sees facts from yesterday and knows they are from yesterday. The panel then shows the banner naming the product Customer profile and that date.

### Step 7

**In the story.** System: applies the masking rule for the caller's role to each account number.

This happens on its own. For each item call Masking.apply on the ACE common module with the field party_product.account_no, the value and the caller's role codes. The masking rule rows are reference data owned by RW-COMPLY and loaded per DL26: clear for RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, and masked to the last four digits for every other role with Case record R, so RW-PHONECOL sees XXXXXX5678 where a case owner sees 9900015678. Mask on the server, so the clear value never reaches the browser of a role that may not see it, and hold no masking logic of your own.

### Step 8

**In the story.** System: writes one PII access event (user, case, party IDs, fields shown) through the ACE PII logging service.

This happens on its own, and it has to succeed. Call PiiAccessLog.write with the user, the case, the party IDs and the fields shown. When it throws PiiLogUnavailableException, return no products at all and answer 503 with MSG-GEN-006, because customer data is never returned without its access event. Write that path as a resilience test with a logging stub that refuses the event. The event holds case and party IDs only, never names or account numbers, and it is what lets the bank show under PDPA who read which customer record and when.

### Step 9

**In the story.** Front end: shows each product with product type, masked or clear account number, status and business date; a stale list shows MSG-P1-001.

This happens on its own in the browser. OtherProductsPanel renders one line per item with the product type, the account number exactly as the server returned it, the product status and the business date of the load. Status values come from the new list LOV-PRODUCT-STATUS, with values ACTIVE, DELINQUENT, CLOSED and WRITTEN_OFF; the P1 load check holds any unknown code, so the panel can show whatever code it is given. Show the stale banner with MSG-P1-001 when the response says stale, and the empty state with MSG-P2-017 when there are no items. The panel is read only and changes nothing on the case.

## RWB-E2-004 Treatment entity and plan timers data model

Module: P3 Case and workflow, with P1 Recovery data engine for the data product

### Step 1

**In the story.** ACE plan status reader (SY-CASEWF): calls `TreatmentRecords.recordApproved(...)` with the case ID, treatment type, terms, approval level, the approval's decision log entry ID and the first due date.

A service makes this call, with no user involved. The ACE plan status reader from RWB-E2-002 runs under the service identity SY-CASEWF, and in SIT a test harness calls the same method. Build the published interface TreatmentRecords in the S2 package recovery.treatment.record.api together with the command it takes: case ID, treatment type, who proposed the plan and when, offer and haircut amounts, installments, valid until, approval level, the decision log entry ID of the approval, the first due date and an idempotency key. That key is a value the caller sends so a repeated call is recognized and not handled twice. The approval happened before this call, so what you record is a plan that is already approved.

### Step 2

**In the story.** Treatment service: checks the case exists and is open through the P3 case interface, and that the decision log entry exists and names an approver through the P7 interface.

The service runs both checks automatically before it writes anything. Ask the P3 case interface whether the case exists and what its status is, and refuse a closed case with MSG-P3-005. Ask the P7 interface for the decision log entry named in the command and read approver_user_id on it; refuse with MSG-GEN-001 when the entry is unknown or carries no approver. The decision log holds who decided what, and these two checks keep a plan from being recorded without a traceable approval behind it. S2 reaches the case only through the P3 interface, never through P3 tables.

### Step 3

**In the story.** Treatment service: checks the required fields and the list values; writes one `treatment` row and the TreatmentApproved event (EV-10) in the outbox, in one transaction.

TreatmentRecordService does this in code. Check the required fields, that installments are above zero for a restructure, that the first due date is on or after the proposed date, and that the treatment type is a value in LOV-TREATMENT. Then write the treatment row and the outbox row for TreatmentApproved inside one transaction. A transaction is a single database unit of work that either saves everything in it or saves nothing. The outbox is a table the event is written to so it is sent only after the commit. Together they keep any event from naming a treatment that was not saved, and any treatment from being saved without its event. The migration creates treatment with first_due_date and its two indexes.

### Step 4

**In the story.** Plan timer listener (P3): consumes TreatmentApproved; finds the case in route state BOOKED_IN_ALS_NLEADS and the terms carrying a first due date (event SCHEDULE_SET).

The listener reacts to the event on its own, after the write of step 3 has committed. Build PlanTimerListener in recovery.casewf.plan. It reads the case route state, which is the position of the case inside its route and is held apart from the case status, and it looks for the first due date in the event terms. Only a case in BOOKED_IN_ALS_NLEADS carrying a first due date counts as SCHEDULE_SET and goes on to the rule. Keep the event ID, so a repeated delivery is ignored and counted; test TC-E2-004-08 sends the same event twice and expects one timer and one decision log entry.

### Step 5

**In the story.** Rules component: evaluates R-RES-25 and returns the action "start the plan timers" and the to state PLAN_RUNNING with the rule version.

The rules component SY-RULES answers this call, and logic of this kind does not belong in your listener. Pass the case and the event to it and take back the action, the to state PLAN_RUNNING and the version of the rule row that matched. The rule rows R-RES-25 and R-RES-27 sit in the Restructure route set and are loaded by the center of excellence through RWB-E1-029, so a condition can change without a code change. Hold the returned rule version, because the next step writes it to the decision log entry and to rule_version on the case. When no rule matches, the case goes to the exception queue with MSG-P3-005.

### Step 6

**In the story.** Plan timer listener: writes the decision log entry with rule R-RES-25 and its version; only after that succeeds writes the INSTALLMENT_DUE timer and sets the route state to PLAN_RUNNING, and publishes CaseStateChanged (EV-05).

The listener does this in a fixed order you have to keep. Write the decision log entry through the P7 interface first, with rule R-RES-25 and its version. Only when that write has succeeded may you create the INSTALLMENT_DUE timer, set route_state to PLAN_RUNNING and publish CaseStateChanged with the from state, the to state, the rule ID and the decision log entry ID. When the decision log store is unavailable, no timer and no state change happen, the event is retried three times and then goes to the exception queue with MSG-P7-003. PlanTimerService sets the timer to expire at the first due date, 23:59 Asia/Bangkok, and sets warn at plan.warn-days earlier. The unique index on treatment_id, timer_type and expires_at stops a second timer for the same due date.

### Step 7

**In the story.** JOB-05 Timer check: at the timer's expiry publishes TimerDue (EV-18) with the timer type and the treatment ID, and sets the timer status to EXPIRED.

JOB-05 is the timer job from RWB-E1-028. It runs every five minutes and needs no change of its own. When it finds a timer past its expiry it publishes TimerDue and moves the timer status from RUNNING to EXPIRED. Your part is to make the INSTALLMENT_DUE timers it reads carry what the event needs, including the treatment_id column this story adds to timer with the index ix_timer_treatment_id. Test TC-E2-004-02 moves a controlled clock past 2026-12-31 23:59 and expects the event and the EXPIRED status, so the timer has to be readable by the job without further work.

### Step 8

**In the story.** Payment matching (P8, JOB-07): publishes PaymentMissed (EV-12) when no payment matched the installment.

Another module does this. P8 payment matching in JOB-07 decides that an installment went unpaid and publishes PaymentMissed with the treatment ID, the due date and the amount due. Building that matching is out of scope here, so you work against the event contract and a test that publishes the event by hand. Nothing in this story reads payments or judges whether money arrived. What you need from the payload is the treatment ID and the due date, because the next step uses them to find the plan and start its cure period.

### Step 9

**In the story.** Plan timer listener: consumes PaymentMissed; applies R-RES-27; writes the decision log entry, then the CURE_PERIOD timer from CURE_PERIOD_DAYS for the product, and sets the route state to PLAN_CURE_PERIOD.

The same listener handles the second event automatically. Call the rules component for R-RES-27, write the decision log entry with that rule and its version first, and only then create the CURE_PERIOD timer and set route_state to PLAN_CURE_PERIOD. The cure period is the time the customer has to pay a missed installment before the plan counts as broken, and its length is CURE_PERIOD_DAYS, a product parameter read through ProductParameterService; for MORTGAGE it is 30 calendar days. Handling a plan that is still unpaid after the cure period belongs to a later epic. This path is build step 6, with test TC-E2-004-12.

### Step 10

**In the story.** JOB-15 Reporting extract: each night reads changed treatments through `TreatmentRecords.changedSince(...)` and writes the treatment data product (DP04) with each treatment's status.

This runs each night at 01:30 with no person involved. Add TreatmentExtractStep as a Spring Batch step in JOB-15. It calls TreatmentRecords.changedSince for the business date, so P1 reads treatments only through that method and never from the S2 table, and writes one row per treatment to the DP04 treatment data product. Derive each row's status: APPROVED while booked at is empty, BOOKED once it is set, and RUNNING, BROKEN, COMPLETED or CANCELED from the outcome. The business date is the idempotency key, so a second run replaces that date's extract instead of adding a copy. A failed run leaves the previous date in place, shown with MSG-P1-001.

## RWB-E2-005 Decision log query API for audit

Module: P7 Decision center and log

### Step 1

**In the story.** Internal auditor: opens SCR-38 Decision log query and enters the filters: case or list of cases, decision, rule ID, rule version, approver, from and to.

A person does this on the screen you build. DecisionLogQueryScreen is SCR-38 Decision log query, a React component with fields for one case or a list of cases, the decision, the rule ID, the rule version, the approver, and a from and to date. Build its Loading, Results, Export and Empty states. The filters caseIds, holding up to 500 case IDs separated by commas, and ruleVersion are new in this story and are recorded in the additions file. The internal auditor holds the right R in Decision log with scope ALL, so the screen is open to them for every case; a role whose Decision log letter is - never reaches it.

### Step 2

**In the story.** ACE front end: calls GET /decision-log with the filters, page and size.

The screen does this, with no further action from the auditor. It calls GET /decision-log with the filters the auditor set, plus page and size. The endpoint exists as API-P7-006; this story adds the caseIds and ruleVersion parameters, the chainVerified field on each item, and text/csv as an Accept value for the export. Add the parameters to the API specification as well as to DecisionCenterAndLogController. The response is a DecisionLogPage carrying items, page, size and total, with the warning MSG-P7-012 at the top when any entry on the page fails its check. Size runs from 1 to 500 under the parameter rwb.decision.query.max-size.

### Step 3

**In the story.** Workbench (DecisionLogQueryService): validates the filters; applies the caller's scope through the case of each entry; runs the query in chain_seq order.

The Workbench does this in DecisionLogQueryService. Validate the filters first and refuse a bad one with 422: a from date later than the to date gives MSG-GEN-003 naming the field, and a size or case count outside its limit gives MSG-GEN-002 with its minimum and maximum. Then apply the caller's scope, which you get from ScopeService.scopeFor in P4 and pass to the P3 interface casesInScope(ScopeFilter, Collection<UUID>); only entries whose case comes back are read, and the number of entries left out is never shown. Run the query in chain_seq order, the sequence number each entry carries in the log. Add index ix_declog_approver_time on (approver_user_id, decided_at) in migration V_E2_005__declog_approver_index.sql.

### Step 4

**In the story.** Workbench (ResultChainCheck): for each entry on the page, recomputes entry_hash from the canonical form and compares prev_hash with the entry before it; sets chainVerified on the entry.

The Workbench does this for every entry it is about to return, in ResultChainCheck. Recompute entry_hash from the entry's canonical form, the fixed layout that RWB-E1-008 defines for hashing an entry, and compare the stored prev_hash with the hash of the entry before it in chain_seq order. The pair of checks is what shows a change: a changed field gives a different entry_hash, and a removed entry breaks the link. Set chainVerified true or false on each item from the result. The entry before the first one on the page sits outside the page, so read one extra row per page to check it. The query path writes nothing to any entry.

### Step 5

**In the story.** Workbench: where an entry does not verify, returns it with chainVerified false and the warning, and raises an incident to Compliance once per entry.

The Workbench does this on its own. An entry whose recomputed hash, or whose link to the entry before it, does not match is still returned, with chainVerified false and the warning MSG-P7-012 naming the entry, and ChainMismatchNotifier raises one incident to the Compliance queue for it. Raise it once per entry so that a repeated query over the same page does not fill the queue. An entry that fails is never hidden and never dropped from the result, because the auditor has to see that the log has a gap. Test it with one entry changed in the SIT database with the trigger disabled, the database rule that otherwise refuses a change to a stored entry.

### Step 6

**In the story.** Workbench: writes one AC-READ access event with the filter and the row count.

The Workbench writes this itself, through the access event interface of RWB-E1-039, for every query that runs. One entry per query, carrying the decision code AC-READ, the filter the auditor used and the number of rows returned. The entry goes into the decision log, which is why a query that cannot write its access event returns 503 with MSG-P7-003 and gives the auditor nothing back; test TC-E2-005-12 forces that failure. A refused query writes its own entry as well, with decision code AC-DENY, area DECISION_LOG and right R.

### Step 7

**In the story.** Internal auditor: selects export; the Workbench returns the full result as CSV and writes one AC-EXPT access event with the filter and the row count.

The auditor chooses the export, and DecisionLogCsvWriter produces it. Build it to stream the full result instead of one page, with a header row, one row per entry, and chainVerified on every row. The export runs the same filters and the same scope as the query, so an auditor cannot reach an out-of-scope entry through it. Write one more access event for the export, with decision code AC-EXPT, the filter and the row count. Personal fields inside a recommendation or an action are masked under the masking rules before the file is written, and the file otherwise carries references and codes.

## RWB-E2-006 Credit approval pack for NLEADS

Module: P2 Integration

### Step 1

**In the story.** Restructuring officer: opens SCR-14 Treatment record and selects the credit approval pack.

A person starts this, the restructuring officer, on the treatment the plan belongs to. SCR-14 Treatment record already exists, and this story adds a read only pack to it. Build CreditPackPanel as a React component on that screen, shown while the treatment is submitted and the case is in route state AWAITING_CREDIT_APPROVAL. The panel gives a copy action per field, because the officer has to put these values into NLEADS, a separate bank system the Workbench cannot call. The case owner may also open the pack on cases in their scope. Opening the pack writes nothing and takes no decision.

### Step 2

**In the story.** Front end: calls GET /treatments/{treatmentId}/credit-pack.

The screen makes this call automatically when the officer opens the pack. The endpoint GET /treatments/{treatmentId}/credit-pack is new in this story and recorded in the additions file, with the treatment ID in the path and nothing in the body. It is read only, so it needs no idempotency key and a repeated call changes nothing. The response is a CreditPack holding the case number, the product group, the accounts, the collateral, the plan terms, the required level, the documents and the messages. Build CreditPackController for this endpoint and for the result endpoint. A source interface that does not answer gives 503 with MSG-GEN-006.

### Step 3

**In the story.** System: checks the Treatment and offer right and the case scope; reads the case, accounts, collateral, latest valuation, plan terms and documents through the owning modules' interfaces.

Your code does this, with nobody involved. Check two things before reading: the caller holds the Treatment and offer right at level R, and the case is inside the caller's scope. A missing right answers 403 with MSG-P4-002; a case outside scope answers 404 with MSG-P4-003, the same answer as a case that does not exist, so the response tells the caller nothing about cases they may not see. Then build CreditPackService to gather the pack through published interfaces only: TreatmentQuery.get for the treatment and its terms, the P1 interfaces for accounts, balances, collateral and the latest valuation, and CaseDocuments.byTypes for the documents. Query no other module's tables.

### Step 4

**In the story.** System: reads the required approval level for the plan from the P7 DelegationQuery and the pack checklist rows.

Two reference reads happen automatically here. Call DelegationQuery.requiredLevel in module P7 with the decision code, the product group and the amount, and it returns the level the delegation of authority sets for that plan, for example L6 under item 2.1.1. Read the document types that belong in the pack from NleadsChecklist, the versioned rule rows holding the NLEADS pack checklist, and pass those types to CaseDocuments.byTypes. Both values are data rows: the checklist is agreed by the business lead with Legal, and the limits are loaded by Risk. Write neither the level nor the list of document types into your code, since both change with no release.

### Step 5

**In the story.** System: returns the pack with each field ready to copy, the documents present with links, each missing checklist item, and the age of each input.

The service builds the response automatically. Every field is returned ready to copy, so the officer types nothing: the case number, the product group, each account with its principal, interest, total balance, days past due and data as of date, the collateral with its appraised value and appraisal date, and the plan terms. For each checklist type, return the document ID and a link when the case holds one, and mark it missing with MSG-P2-009 when it does not. Compute the age in days of each input from its data as of date, and where an input is past its age limit of one business day, attach MSG-P7-006 with the day count.

### Step 6

**In the story.** Restructuring officer: submits the plan in NLEADS and receives the NLEADS reference and later the result.

This happens outside the Workbench and no code of yours runs. NLEADS has no interface, so the officer opens NLEADS, copies the pack values into it, opens the documents from the links, and submits. NLEADS gives back a reference at once and the credit decision later, with the level that approved it. Build no call to NLEADS, not even a stub meant for later use, because the guardrail for this story is that the Workbench never calls NLEADS. The wait between submission and result is open ended, so the treatment sits in state submitted and the case stays in route state AWAITING_CREDIT_APPROVAL until the officer comes back with the result.

### Step 7

**In the story.** Restructuring officer: records the NLEADS reference, result, approval level, result date and, for a refusal, the reason.

The same person returns to SCR-14 and types the outcome. Build CreditResultForm as a React component with fields for the NLEADS reference, the result, the approval level, the result date and the reason, each showing its own field error. It posts to the new endpoint POST /treatments/{treatmentId}/credit-result with an If-Match header holding the treatment version the officer read. The reference is 1 to 30 letters, digits and dashes, the result is APPROVED or REFUSED, the level is L1 to L6, and the reason is 1 to 1,000 characters and required when the result is REFUSED. The case owner may record a result on cases in their scope.

### Step 8

**In the story.** System: validates the input and the treatment version; writes the decision log entry with decision D5, final call and the NLEADS reference in the actions.

Your code runs the checks and the first write automatically. Refuse an empty reference or an empty reason on a refusal with 422 and MSG-GEN-001, a result date after today with 422 and MSG-GEN-002, an approval level below the level the plan needs with 409 and MSG-P2-018, a result already recorded with 409 and MSG-P2-010, a case not awaiting credit approval with 409 and MSG-P3-005, and an If-Match version that no longer matches with 409 and MSG-GEN-004. Then call DecisionLogWriter.write with decision D5, the final call and the NLEADS reference in the actions. Write that entry before the treatment changes, and change nothing when DecisionLogUnavailableException is thrown.

### Step 9

**In the story.** System: writes the reference, result, reason, approval level and state on the treatment and raises CREDIT_APPROVED or CREDIT_DECLINED to P3.

Your code writes the outcome once the decision log entry is in. Call TreatmentCommands.recordCreditResult with the treatment ID, the command and the version the officer read, so two officers saving at the same time end with one saved result and one 409 with MSG-GEN-004. The treatment then holds nleads_ref, credit_result, credit_result_reason, credit_result_at, approval_level, the decision log ID and its state, APPROVED or REFUSED. The four new treatment columns are added by the treatment owner in its own migration, with a check that the reason is not empty when the result is REFUSED. Then call CaseEvents.raise with CREDIT_APPROVED or CREDIT_DECLINED, which hands the case move to P3.

### Step 10

**In the story.** SY-RULES and SY-CASEWF: an approval releases the offer to the customer (R-RES-11); a refusal records the reason (R-RES-12) and returns the case to the route decision in the case owner's queue (R-RES-14).

The rules component and the case workflow module do this on the event you raised, and you build none of it here. On CREDIT_APPROVED, rule R-RES-11 moves the route state from AWAITING_CREDIT_APPROVAL to OFFER_WITH_CUSTOMER and the offer goes to the customer with a 14 day validity. On CREDIT_DECLINED, rule R-RES-12 moves it to DECLINED_BY_CREDIT and records the reason, then R-RES-14 moves it to BACK_TO_ROUTE_DECISION on DECLINE_RECORDED and the case appears in the case owner's queue. Your tests check the route state and the queue after each event, since this is how the officer and the case owner see a credit result.

## RWB-E2-007 Booking confirmation from the ALS load

Module: P2 Integration, with P8 Payments and posting

### Step 1

**In the story.** Scheduler: JOB-08 starts after JOB-01 publishes LoadCompleted (EV-26) for ALS with business date D.

Quartz starts this job; no person starts it. The trigger is daily and chained on an event: JOB-01 publishes LoadCompleted, event EV-26, when the ALS load for a business date has passed its checks, and JOB-08 runs after that. An event here is a message one module publishes that another consumes, rather than a direct call. Build BookingMatchJob so it runs for a business date only when that date load passed. A refused or late load means JOB-08 does not run for that date at all, and no missing booking task is raised for it, which AC5 checks with the load refused at DQ-003 Control total. MSG-P1-001 tells the user the product is from the earlier date.

### Step 2

**In the story.** SY-DATALOAD: the BookingMatchService lists approved treatments of type RESTRUCTURE or SETTLEMENT not yet booked, through the treatment interface.

The job does this itself, under the service identity SY-DATALOAD. Build BookingMatchService and get the work list by calling TreatmentQuery.approvedNotBooked from RWB-E2-004 with the two treatment types RESTRUCTURE and SETTLEMENT. Read the treatments through that interface and not from the treatment table, because this story may reach treatments, accounts and tasks only through their published interfaces. A treatment stays in this list every night until it is marked booked, which is why a booking that is still missing on the next load needs no new list and raises no second task. The approval date the match uses is recorded by TreatmentApprovedListener, which consumes the TreatmentApproved event.

### Step 3

**In the story.** SY-DATALOAD: for each treatment, checks IdempotencyGuard on treatment ID + D; a repeat is skipped.

The job makes this check in its own code. IdempotencyGuard comes from RWB-E1-007. Idempotent means that doing the same work a second time leaves the same result as doing it once. The key here is the treatment ID together with the business date, so for each treatment the guard answers whether this pair has already been handled. A treatment already handled for that date is skipped, which gives the behavior AC6 asks for when the platform administrator reruns JOB-08 for 2026-12-16: no second booking, no second TreatmentBooked event and no new task. Build this check before any match work, so a rerun costs nothing and changes nothing.

### Step 4

**In the story.** SY-DATALOAD: reads every account of the case through the P1 AccountQuery for business date D.

The job reads this itself. Call AccountQuery.forCase in package recovery.data.api with the case ID and the business date, rather than reading loan_account. Read every account of the case, because a restructure counts as booked only when every account matches, and a case with one account booked out of two stays approved. The values the match needs from each account are tdr_flag, last_tdr_date, interest_rate, principal_outstanding, data_as_of, settlement_booked_date and settlement_booked_amount. The last two columns are new on loan_account and are added by P1 with the INT-01 mapping; their ALS source fields are still to confirm with the system owner. The match never calls ALS and works only on the loaded data.

### Step 5

**In the story.** SY-DATALOAD: applies the booking match rows for the treatment type to each account.

The job does this with no person involved. Build BookingMatchRules as a versioned rule table with one row per comparison: treatment type, ALS field, treatment field, comparison and tolerance, loaded by the center of excellence analyst and in force as a version such as BKG-2026.12. Build the comparison evaluator with a test for each row. For a restructure the rows compare tdr_flag, last_tdr_date and principal_outstanding against the offer amount, and the account interest rate against the approved rate; a restructure counts as booked when every account shows tdr_flag true with a last TDR date on or after the approval date. For a settlement the rows compare the settlement booked date and amount against the offer amount. The tolerance on amounts and rates is zero. The result per treatment is booked, missing, partly booked or differing.

### Step 6

**In the story.** SY-DATALOAD: when every account matches, calls TreatmentCommands.markBooked with the business date; P8 publishes TreatmentBooked (EV-11); P3 writes the decision log entry and moves the case by R-RES-22 or R-SET-13.

The job makes the call; the modules do the rest in their own code. Call TreatmentCommands.markBooked with the treatment ID, the business date and the booking reference, which is the account ID together with the business date and holds the account ID rather than the account number. That command writes the decision log entry first and throws DecisionLogUnavailableException when the log is not available; handle it by changing nothing, so the treatment stays APPROVED, no TreatmentBooked event goes out, an incident is raised with MSG-P7-003 and the next load tries the match again. On success the treatment state moves from APPROVED to BOOKED with its booked at date, the payments module publishes TreatmentBooked, and the case workflow module moves the case by rule R-RES-22 or R-SET-13, as AC1 shows from WITH_OPS_SETTLEMENT to AWAITING_PAYMENT.

### Step 7

**In the story.** SY-DATALOAD: when no booking is found after the grace loads, raises one task WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT for role RW-RESTRUCT with MSG-P2-011; the treatment stays approved.

The job raises the task itself. Read the grace from the parameter booking.missing.grace_loads, one ALS load after approval, so a treatment is reported missing only after that many loads have been checked. Raise the task through TaskApi.raiseTask with the case ID, the task code, the owner role RW-RESTRUCT, the message ID and its parameters. That call returns the open task when one already exists for the same case, code and treatment, so the next night raises no second task and the open one stays, as AC7 requires. MSG-P2-011 names the treatment, the load date and the accounts with no booking, which is how the part-booked case in AC4 names account A-0705. The treatment state and the route state are left unchanged.

### Step 8

**In the story.** SY-DATALOAD: when a booking is found with a different term, writes the difference on the treatment and raises one task UNMATCHED_EXCEPTION for role RW-CREDITAD with MSG-P2-012; the treatment stays approved.

The job does this with no person involved. Call TreatmentCommands.recordBookingDifference with the treatment ID and the list of differing terms; it writes them to the treatment column booking_difference, a jsonb column the treatment owner adds. Then raise one task with code UNMATCHED_EXCEPTION through TaskApi for the role RW-CREDITAD, the Credit Administration officer, with MSG-P2-012, which names the term with its booked value and its approved value. AC3 gives the example: an interest rate approved at 4.2500 and booked at 4.5000. The treatment stays APPROVED, so the next load checks it again. The restructuring officer and the Credit Administration officer see the difference on SCR-14 Treatment record, term by term, and their tasks on SCR-01 My work.

### Step 9

**In the story.** SY-DATALOAD: writes the run summary: treatments read, booked, missing, differing; the P1 reconciliation REC-03 reads the same results.

The job writes the summary itself. Build BookingRunSummaryWriter to put the four counts, treatments read, booked, missing and differing, into the checks field of the interface_run row for the run. The reconciliation REC-03 compares approved treatments with bookings and reads those counts rather than counting again, so the figures the data steward sees come from this one place. REC-03 is where a treatment missing for more than one load shows up: AC7 has TRT-SYN-0702 on the break list as missing for two days. The target is zero after two days. The story is done when REC-03 over a week in SIT shows every synthetic approved treatment either booked or raised as a task.

## RWB-E2-008 Payment matching with the missed payment event

Module: P8 Payments and posting

### Step 1

**In the story.** JOB-07 Payment matching: starts when LoadCompleted arrives for the ALS source and business date, after JOB-01.

No clock starts this job. Build PaymentMatchingJob as a Spring Batch job started by the LoadCompleted event, EV-26, that JOB-01 publishes for the ALS source once every check has passed. A refused or late ALS load therefore means JOB-07 does not run for that business date, and no missed payment is raised from stale data, which AC5 tests. A rerun for a business date is possible from SCR-44 and skips rows already written. The job runs under the service identity SY-DATALOAD, which holds Write-off and posting U.

### Step 2

**In the story.** System: reads the payments loaded for the business date through the P1 interface.

The job reads the data through another module's interface. Call RecoveryDataApi.paymentsLoaded with the business date, the P1 published interface, to read the payments JOB-01 wrote into account_payment for that date. This module reads neither account_payment nor loan_account nor case_account directly. Each payment carries its payment code, account, payment date, amount and data_as_of. Amounts are BigDecimal with scale 2 and are compared exactly with no rounding, because the EXACT rule carries an amount tolerance of 0 percent.

### Step 3

**In the story.** System: for each payment, finds the open case of the account through the P3 interface; a payment on an account with no open case goes to the data quality exception list.

The job does this for every payment on its own. Call CaseWorkflowApi.openCaseForAccount with the account, the P3 published interface, which returns the open case or nothing. With no open case, write no proceeds row and hold the payment on the data quality exception list with check References, the reference exception of DQ-012. AC4 tests this with payment PAY-90003 on account A-0999. Payments are identified in logs by payment code and account ID, and account numbers are never logged. A payment that does have an open case goes on to the plan matching of the next step.

### Step 4

**In the story.** System: reads the running plans on the case and the parameter row in force; a payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment.

The matcher does this with no person deciding. Call TreatmentApi.runningPlans for the plans on the case and RecoveryDataApi.nextInstallmentDate for the account's due date, and read the payment_match_rule row valid on the business date through PaymentMatchRuleRepository. The EXACT row of version PM-2026.12 holds amount tolerance 0 percent, a window of 10 days before the due date and 0 days after, and grace 0 days. A payment on the plan account for the installment amount and dated inside that window matches that installment. AC7 tests both sides of the window: 10 days before matches, 11 days before does not.

### Step 5

**In the story.** System: writes a proceeds row with source CUSTOMER and matched_to INSTALLMENT, calls TreatmentApi.recordInstallmentPaid, and writes ProceedsMatched to the outbox in the same transaction.

The job writes all three things together. Insert the proceeds row with the case, the treatment, source CUSTOMER, the amount and matched_to INSTALLMENT. Call TreatmentApi.recordInstallmentPaid with the treatment, the proceeds ID, the due date and the amount, so that P3 raises installments_paid on the plan. Write ProceedsMatched, EV-25 with proceedsId, caseId and amount, to the outbox. All of it sits in one transaction, so none of the three can exist without the others. Add unique index ux_proceeds_account_payment on account_payment_id where it is not null, which gives one proceeds row for each ALS payment.

### Step 6

**In the story.** System: a payment that matches no plan installment is written with matched_to UNMATCHED and appears on the exception list for the reconciliation agent (R-UNI-03).

The job writes this itself. Insert the proceeds row with matched_to UNMATCHED and no treatment, and count it in the run summary with MSG-P8-001, which names the count and the date. Build ProceedsController for GET /api/recovery/v1/proceeds with a matched query value, so matched=false returns these rows for the Credit Administration officer on SCR-28. Authorization is Write-off and posting R with scope applied, and a role without the right is refused with MSG-P4-002. AC3 has payment PAY-90002 of 3,000.00 THB against an installment amount of 12,500.00 THB.

### Step 7

**In the story.** System: after all payments, for each running plan whose next due date plus the grace days is before the business date and that has no matched payment for that due date, writes PaymentMissed with treatment ID, due date and amount due.

The detector runs after every payment of the load has been matched, with no person involved. Build MissedPaymentDetector. For each running plan, add the grace days from the parameter row to the next due date, compare that against the business date, then look for a matched payment for that due date. With no payment, write PaymentMissed, EV-12 with treatmentId, dueDate and amountDue, to the outbox. New table payment_missed_event_key, unique on treatment_id and due_date, holds one event per plan and due date, so a rerun writes no second event. Unit test the grace boundary, as section 13 build step 4 asks.

### Step 8

**In the story.** P3: applies R-RES-27 (plan to the cure period) and the transfer rule; the case owner sees the missed payment on the treatment record the same morning.

Another module acts here, and nothing in this story changes a plan state. P3 consumes PaymentMissed, moves plan T-0701 from PLAN_RUNNING to PLAN_CURE_PERIOD under rule R-RES-27, and records the case movement with reason payment missed through the transfer rules of RWB-E1-021. The case owner, holding Treatment and offer R, reads the plan position on SCR-14 Treatment record and the missed payment on SCR-04 Case timeline, both on the morning after the due date passed.

### Step 9

**In the story.** System: writes the run summary (payments read, matched, unmatched, missed events) to the job monitor and runs REC-04 (payments in the ALS load against proceeds).

The job closes itself out. Write the run counts, payments read, matched, unmatched and missed events, so SCR-44 shows them, with MSG-P8-001 when unmatched payments exist and MSG-P8-002 when the job stopped because no matching rule was in force on the business date. That second case also marks JOB-07 failed with an alert to Credit Administration, which AC8 tests. Then run reconciliation REC-04, which compares the payments in the ALS load against the proceeds rows by count and by amount for the date. The done condition is a synthetic month in which every ALS payment shows as a proceeds row or a held reference exception.

## RWB-E2-009 Steering dashboard v1 data set

Module: P9 Reporting

### Step 1

**In the story.** JOB-15 Reporting extract, nightly 01:30: reads the definitions in force, including the steering measures of MD-2026.12.

Automatic. JOB-15 already exists from RWB-E1-013 and runs each night at 01:30 with no person involved. At the start of a run it reads the measure definitions in force from measure_definition through MeasureCatalog, which now include the seven steering measures of version MD-2026.12: CASES_BY_STAGE, CASES_BY_QUEUE_AGE, DECISIONS_LOGGED, TREATMENTS, LETTERS_SENT, AGENT_ACCEPTANCE and AGENT_OVERRIDE. The reference data administrator loads that version and the Tribe lead approves it, so your code holds no measure list. Your change is to add the steering calculators and the reconciliation to the existing job.

### Step 2

**In the story.** System: computes each steering measure for the previous business date from the owning modules' reporting interfaces.

Automatic. Write SteeringCalculators with one calculator per measure code, each working on the previous business date. Take every figure through the published interface of the module that owns it: CaseReportingApi.caseFacts in P3 for cases by stage, queue and age, DecisionLogApi.decisionFacts in P7 for decisions logged, TreatmentApi.treatmentFacts in P3 for treatments, NoticeApi.noticeFacts in P6 for letters sent, and AgentMonitorApi.runFacts in P10 for the agent measures. Read no other module's tables. AC2 expects DECISIONS_LOGGED for 2026-12-15 to be 1,412, the count of decision log entries decided that day.

### Step 3

**In the story.** System: compares the total of CASES_BY_STAGE with the open case count of the case list at the same cut-off (P3 interface).

Automatic. Build CountReconciliation to add up the CASES_BY_STAGE values it has just computed and compare that total with CaseReportingApi.openCaseCount for the same cut-off, which is the number the case list shows the teams. The tolerance is zero, so the two numbers either match or they do not. Write the comparison to the new measure_publish table with the business date, the dashboard count, the case list count and the status. AC2 has both counts at 240 and AC4 has 239 against 240. Run this before anything is published, which is the order build step 3 sets.

### Step 4

**In the story.** System: if the counts are equal, writes the snapshot rows and the INT-19 extract with the freshness stamp; if not, holds the publish, keeps the previous day as the latest published and alerts the Reporting and BI analyst and the data steward.

Automatic, and the comparison decides the outcome. On a match, write the measure_snapshot rows for the business date with published_at set, and write the INT-19 extract for the data lake with its freshness stamp. On a mismatch, publish nothing for that date: measure_publish carries the held status and the reason, the previous day stays the latest published day, and an alert with MSG-P9-002 naming both counts and the date goes to the Reporting and BI analyst and the data steward. A held day is published by the first later run whose counts match, and a rerun of a published day writes the same values and leaves the frozen baseline rows of 2026-11-27 alone.

### Step 5

**In the story.** Reporting and BI analyst: the Power BI data set refreshes at 07:30 from the extract.

The refresh is scheduled in Power BI and the Reporting and BI analyst owns the report, so nothing in the Workbench triggers it. Your part is that the INT-19 extract for the business date is in place with its freshness stamp before 07:30, which AC1 states. Because Power BI and the screen read the same measure_snapshot rows, the committee and the teams work from one set of numbers. On a held day there is no new extract, so the report keeps showing the previous published day with that day's date.

### Step 6

**In the story.** Product head or team manager: opens SCR-37 Steering dashboard; the screen calls GET /reports/measures with product, route and date filters.

A person does this. Build SCR-37 as the React component SteeringDashboard, with filters for product, route and dates, a loading state of skeleton rows and a filtered state. It calls GET /reports/measures with those filters, which MeasureController serves from published measure_snapshot rows through MeasureQueryRepository. Dates in the wrong order are refused with 422 and MSG-GEN-003 naming from and to, as AC6 shows for from 2026-12-15 and to 2026-12-01. The Tribe lead, the product head, the team manager, the Reporting and BI analyst, the data steward and the Finance delegate are the roles that read this screen.

### Step 7

**In the story.** System: checks Reporting R and the scope, returns the published values with the business date and the freshness stamp, and shows the baseline beside each value.

Automatic. MeasureController checks right R in the capability area Reporting and applies the caller's scope, so a team manager sees only the teams in their scope and a role without the right gets 403 with MSG-P4-002. It returns published rows only, each with its period, and sets the response header X-Data-As-Of to the business date of the latest published day. Add the two new fields to the Measure schema in api.yaml and record them in the additions file: dimension, which carries the dimension code and value, and baselineValue, which carries the frozen 2026-11-27 figure the screen shows beside each value.

### Step 8

**In the story.** System: computes agent acceptance and override rates per agent and version from the decision log and the agent runs; an agent with no runs shows "No runs" and no rate.

Automatic, inside the same JOB-15 run. For each agent code and version, take the recommendations from AgentMonitorApi.runFacts and the verdicts from the decision log, then compute acceptance as accepted recommendations over all recommendations and override as overridden over all. AC3 gives agent case-intake version 1.2.0 with 200 recommendations, 170 accepted and 30 overridden, so acceptance is 85.0 percent and override is 15.0 percent. An agent with no recommendations that day has nothing in the denominator, so write no value for it and let SCR-37 show “No runs”, as AC7 expects for deviation-screen version 0.9.0. Carry the agent and version in the dimension, for example “agent:case-intake:1.2.0”.

## RWB-E2-010 Stage 2 data products: contracts, plans and treatments

Module: P1 Recovery data engine

### Step 1

**In the story.** JOB-01: after the COLLINS load for business date D passes its checks, starts the stage 2 product step.

No person starts this. The stage 2 step is a new part of JOB-01, wired in after the COLLINS load for business date D has passed its own checks, so it runs daily before 07:00. You build Stage2ProductStep for that position in the job. When the step fails, the platform administrator restarts it from the job monitor with POST /api/recovery/v1/admin/jobs/{jobId}/rerun, and a rerun for the same business date replaces the rows rather than adding to them. The business date carried into the step is what every later part of the flow keys on.

### Step 2

**In the story.** Stage2ProductService: calls TreatmentQuery.changedBetween(start of D, end of D) and receives the treatments created or changed on D, with plan terms from the ACE restructure calculation.

Stage2ProductService makes this call itself. TreatmentQuery is a published interface of the treatment module from RWB-E2-004, so treatments never come from its tables. changedBetween takes a window, and the window for business date D runs from the start of D up to the start of D plus one day, which puts a treatment changed at 2026-12-14T23:59:59+07:00 in that day and one changed a second later in the next. Each TreatmentView carries the treatment fields including installments, which the ACE restructure calculation produced. An error from the interface fails the step with MSG-GEN-006 and leaves the previous day's rows in place.

### Step 3

**In the story.** Stage2ProductService: calls GuaranteeClaimQuery.changedBetween() for guarantee claims changed on D.

The same service makes a second interface call, for guarantee claims changed on D. GuaranteeClaimQuery belongs to the guarantee module, which is built in Epic 4; until then the interface answers with an empty list, so write the step to treat no claims as a normal day rather than an error. Each GuaranteeClaimView carries the claim type, the claim deadline, the claimed and paid amounts, the filing time and the status. The 5 TCG claims in the test data each name an existing case and each produce one row later in the flow.

### Step 4

**In the story.** Stage2ProductService: resolves each case's primary account through CaseScopeQuery and reads its contract number and contract date from loan_account.

This is code filling in the contract reference. For each case behind a treatment or a claim, call CaseScopeQuery.linksInScope with a system context rather than a user, because the job has no user whose scope could narrow the answer. From the links take the case's primary account, then read contract_no and contract_date from loan_account, a P1 table your own module owns. Those two values go onto every dp_treatment row beside the treatment fields. A case that does not resolve is held back in the next step rather than written with an empty contract.

### Step 5

**In the story.** Stage2ProductService: holds in the data quality exception list any row whose case does not resolve (check References), and writes the other rows to dp_treatment and dp_guarantee_claim keyed by record ID.

Two outcomes, both automatic. A row whose case does not resolve is not written; record it instead through DataQualityExceptions with product DP04 and check References, and leave it for the next day's load to pick up. Everything else goes to dp_treatment and dp_guarantee_claim, both new tables in this story's Flyway migration along with their sys_objects and sys_fields entries. Write by record ID and business date: the unique key over those two columns means a second run for 2026-12-14 updates the same rows, so the count holds at 40 instead of doubling. dp_treatment also carries business_date, contract_no and contract_date.

### Step 6

**In the story.** Stage2ProductService: compares the count of active treatments in dp_treatment with TreatmentQuery.countActive(); a difference holds the publish (DL25).

The service checks its own work before anything is published. Count the active treatment rows it just wrote and compare that with TreatmentQuery.countActive from the owning module. The tolerance is zero: 40 rows against a count of 41 holds the publish, so DP04 gets no freshness stamp for that business date and a break naming the two numbers goes to the data steward with MSG-P1-002. The data store therefore never shows a day as complete while it disagrees with the module that owns the records. On a match the step moves to the stamp.

### Step 7

**In the story.** FreshnessStampService: on a match, writes the DP04 stamp for business date D.

FreshnessStampService writes the stamp, and only a matching count reaches it. The stamp is a data_product_load row for DP04 and business date D with status LOADED, built in RWB-E1-015, and it is what tells every reader how current the product is. DP04 carries an expected-by time of 08:00; when no stamp for the day has arrived by then, the stale check flags DP04 with MSG-P1-001 naming the date of the last load it does have. Call the existing service rather than writing the row yourself.

### Step 8

**In the story.** Case owner or restructuring officer: reads DP04 for a case through GET /data-products/DP04/records?caseId=.

A person reads the product, through an endpoint that already exists from RWB-E1-016. GET /api/recovery/v1/data-products/DP04/records with a caseId answers with that case's treatments, plan terms, contract reference and guarantee claims. Two things have to be true for the read to pass: the caller holds the Case record R right with the case in scope, and the caller's role has a DP04 row in data_product_access, version DPA-2026.12, which covers RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT. A role with no DP04 row, such as RW-PHONECOL, gets 403 with MSG-P4-002, and the refusal is logged with the user and the product.

### Step 9

**In the story.** Data steward: reads the DP04 catalog entry and any breaks.

The owner of the product checks it after the run, by hand. The data steward reads the DP04 catalog entry through GET /admin/data-products, where it shows the system of record Workbench, the owner RW-DATASTEW and the fields of treatment and guarantee_claim, and reads the breaks and References exceptions through GET /api/recovery/v1/admin/data-quality/exceptions with the Platform administration R right. From Epic 2 the same lists appear on SCR-45 Data quality in its loading and breaks states. Rows held with check References keep their place in the list until a later load resolves their case.

## RWB-E2-011 Queue view screens: my queue, team queues, filters and ageing

Module: P3 Case and workflow

### Step 1

**In the story.** Case owner: opens My queue from the menu.

A person starts this. The case owner picks My queue from the menu, which opens the My queue view of SCR-02. The menu item appears only when the feature flag rwb.p3.queue-views is on; with the flag off both My queue and Team queues are hidden. You build the screen as the React component MyQueuePage, and its first state is Loading with skeleton rows while the call of step 2 runs. The signed in person needs Case record R with scope Own, which RWB-E1-037 sets, and the list then holds the open cases whose owner is that person (BR1).

### Step 2

**In the story.** Front end: calls `GET /cases` with `owner=me`, `sort=serviceLevelDueAt` and the filters kept for the session.

The front end asks the existing case endpoint for the data. It calls GET /cases with owner set to me, sort set to serviceLevelDueAt, and any filters kept for the session. Both the sort value and the route filter are new, and you add them to the endpoint in build step 2. Filters live in browser session storage through the useSessionFilters hook: wrap every read and write in try and catch, because storage can be blocked, and the page has to work without it. Session storage also means the filter survives opening a case and coming back, and is gone after sign out and sign in (AC3). The server stores nothing about filters (BR8).

### Step 3

**In the story.** Case service: applies the scope, the filters and the sort; returns one page of cases with age, status and service level state.

The case service answers with one page of cases and no person is involved. CaseListQueryService applies the caller scope, the filters, the age range and the sort, and CaseListRepository runs one SQL query joining recovery_case with the SERVICE_LEVEL timer of each case. Three fields are computed instead of stored: ageDays, the calendar days from entry_date to the business date; serviceLevelDueAt from the timer; and serviceLevelState as BREACHED, RUNNING, PAUSED or NONE. The sort has four groups in that order, breached first, then running by due date earliest first (BR2). A page size outside 1 to 200 is refused with MSG-GEN-002, and an age range with age from above age to with MSG-GEN-003. The header X-Data-As-Of carries the business date of the case data.

### Step 4

**In the story.** Front end: shows the list in state List, or Empty with MSG-P3-017.

The front end draws what came back. With rows it shows the List state, each row holding the case number, product group, stage, status, age in days from the entry date and the service level due date. With no row for this person and these filters it shows the Empty state with MSG-P3-017, which reads that there are no cases in this queue (AC4). MSG-P3-017 is a new message recorded in the additions file, and its Thai text follows DL10. Build step 5 asks for all four states of the page, Loading, Empty, List and Filtered, so write the empty state together with the list.

### Step 5

**In the story.** Case owner: sets the stage filter to Litigation; the front end keeps the filter in session storage and reloads the list in state Filtered.

The case owner sets the stage filter, for example to Litigation, and the front end reloads the list in the Filtered state showing only those cases (AC3). The stage values come from the list LOV-STAGE through the P4 list interface, with LOV-ROUTE and LOV-CASE-STATUS for the route and status filters, so no label or code sits in the front end. The chosen filter is written to session storage by useSessionFilters and sent on the next GET /cases call. Age from and age to belong to the same filter set, and an age range the wrong way round is refused before the list reloads (AC5).

### Step 6

**In the story.** Team manager: opens Team queues from the menu.

The team manager opens Team queues from the menu, which is the second screen of this story, SCR-07, built as the React component TeamQueuesPage. The person needs Queue and allocation R with team scope and sees only the queues of their own teams. RW-CAPACITY holds the same right with scope All and opens the same screen. A role without the right is refused with MSG-P4-002, which is access test TC-E2-011-13 with RW-WRITEOFF. The screen starts in Loading with skeleton rows, then moves to the List state once the call of step 7 returns.

### Step 7

**In the story.** Front end: calls `GET /queues`.

The front end calls GET /queues, which takes no request parameters. The scope on the endpoint decides what comes back, so the caller receives the queues of their own teams and nothing else. The endpoint already exists and you extend its response with the computed fields of step 8 in build step 3. One call serves the whole screen, so the queue rows and the owner counts arrive in the same response. With the feature flag rwb.p3.queue-views off the endpoint answers with the Epic 1 fields only, which keeps the screen hidden and the API working.

### Step 8

**In the story.** Queue service: returns each queue in the manager's teams with the open case count, the oldest entry date, the breach count and the open cases per owner against the cap.

The queue service computes the numbers for each queue in scope. QueueSummaryService with QueueSummaryRepository groups counts by queue_id and owner_user_id and returns openCaseCount, the cases whose status is not Closed; oldestEntryDate and oldestAgeDays; breachCount, the open cases whose SERVICE_LEVEL timer has status EXPIRED; and owners, each with their open case count and atCap against queue.capacity_cap, 150 in the examples. The counts have to equal the case list count for the same queue, so MTG-BKK-CO shows 412 on both screens (AC11). A queue is listed even when it has no cap loaded.

### Step 9

**In the story.** Team manager: selects a queue; the front end calls `GET /queues/{queueId}/cases` and shows the cases sorted by service level.

The team manager selects a queue row, and the front end calls GET /api/recovery/v1/queues/{queueId}/cases with page, size and the service level sort, showing the same case rows as My queue. Build step 4 adds the scope check to this endpoint: a queue of another team is answered with 404 and MSG-P4-003, so SME-NTH-CO is not found for a MTG-BKK manager (AC7). From the list the manager can go on to SCR-05 Transfer case, which story RWB-E2-012 builds. This story reads cases, queues and timers and changes no case.

## RWB-E2-012 Manual transfer and reassignment screen with reason

Module: P3 Case and workflow

### Step 1

**In the story.** Team manager: opens SCR-05 Transfer case from SCR-03 Case record or from a selection on SCR-07 Team queues.

A person opens it, and from two places. Build TransferCasePage as SCR-05 in src/modules/recovery/casewf/transfer, reachable from SCR-03 Case record for one case and from a selection on SCR-07 Team queues for up to 50 cases, the limit in transfer.bulk.max. The person needs RW-TEAMMGR or RW-CAPACITY with Queue and allocation right U, and the cases must be in their scope. A case owner may read the result and may not transfer. The feature flag rwb.p3.manual-transfer hides the screen and makes the endpoint answer 403 for every role except SY-CASEWF when it is off.

### Step 2

**In the story.** Team manager: chooses a target queue or a target owner, a reason code and an optional note, and confirms.

The manager fills the form. One of the two targets is required and only one is allowed: a queue, which leaves the owner to the engine, or a named owner. The reason code is required and comes from LOV-TRANSFER-REASON, with the assumed values R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue. The note is optional and holds at most 500 characters. Build the reason picker from that list rather than from a fixed set in code, because the center of excellence owns those values. The note is never logged. This is the Form state of SCR-05.

### Step 3

**In the story.** Front end: calls `POST /cases/{caseId}/transfer` with a new Idempotency-Key per case.

The page sends the call when the manager confirms. One request per case, each with its own Idempotency-Key header holding a fresh UUID. An idempotency key is a value that names one attempt, so a request sent twice takes effect once. Build IdempotencyStore to keep the key, a hash of the request and the response for 24 hours, and have the controller return the stored response when the same key arrives again. For a bulk move, BulkTransferRunner sends the requests one after another and collects a result per row, so each case is its own request and its own transaction.

### Step 4

**In the story.** Transfer service: checks the reason code, that the case is open and not under a legal hold, and the scope.

Automatic, in ManualTransferService, and the order of the checks is set in the build steps. Check the reason code first: a missing one answers 422 with MSG-P3-001 and changes nothing. Then the case state. A case that is closed, or whose legal_hold flag is true, answers 409 with MSG-P3-005 naming the target and the held state. Then scope: a case the caller may not reach answers 404 with MSG-P4-003. A legal hold is a flag on recovery_case that keeps the case where it is while legal work runs on it. Make every check before any write, so a refusal leaves the case, its assignment and the decision log untouched.

### Step 5

**In the story.** Rules component: evaluates the transfer rule table for the case, the target and the reason; returns the allowing rule row or the refusing rule ID.

No person is involved, and the logic is not yours. Call TransferRules.evaluate from RWB-E1-021 with the case ID, the target queue, the target owner and the reason code. It answers a TransferDecision holding either the rule row that allows the move or the ID of the rule that refuses it. On a refusal, answer 409 with MSG-P3-033 naming that rule, as AC2 expects for rule R-DEV-02 on a case with an open deviation. Keep the allowing rule's ID and version, because both have to appear on the assignment row and in the decision log entry. Write no transfer condition into this service; the rows decide.

### Step 6

**In the story.** Transfer service: for a queue transfer, asks `AssignmentEngine` for the owner by the target queue's method; for a reassignment, checks the target owner is below the cap and, for reason R04, in the case's team.

Two paths, both automatic. For a queue transfer, call AssignmentEngine.pickOwner from RWB-E1-020, which picks by the queue's assignment_method, so ROUND_ROBIN on queue LIT-BKK-01 gives the owner whose turn it is. For a named owner, build OwnerLoadRepository to count that owner's open cases and compare them with the queue's capacity_cap: at or above it, answer 422 with MSG-P3-002 naming the owner, and name every owner when the whole target queue is at the cap. For reason R04, owner absent, also check that the target owner's team matches the case's team, and refuse with MSG-P3-033 naming R-UNI-18 when it does not.

### Step 7

**In the story.** Transfer service: writes the decision log entry through the P7 interface; on success, in one transaction ends the current assignment, writes the new assignment with reason, rule ID, queue and reason code, updates the case queue, owner and team, and writes CaseTransferred (EV-04) to the outbox.

Automatic, and the sequence is the rule. Call DecisionLogWriter.record through the P7 interface first; a failed write answers 503 with MSG-P7-003 and nothing else happens. Only after it succeeds, open one transaction holding five writes: set ended_at on the current assignment, insert the new assignment with reason TRANSFER or MANUAL, the rule ID, the queue ID and transfer_reason_code, update recovery_case with the new queue, owner and team_code, and insert the CaseTransferred event into the outbox. The case update uses the version column as an optimistic lock, which means the update names the version it read and fails when another transfer changed the row first, answering 409 with MSG-GEN-004. The status, route state and clocks stay as they were.

### Step 8

**In the story.** Front end: shows state Saved with MSG-GEN-005; for a bulk move, one result per case and the summary.

The page shows the outcome. For a single case, the Saved state with MSG-GEN-005. For a bulk move, BulkTransferRunner keeps the result of each request and the page lists one line per case, so a refused case shows its own message, MSG-P3-005 for a case under a legal hold, beside the cases that moved. Above the list, show MSG-P3-035 with the counts, which for AC11 reads 8 of 10. A refused case is queued nowhere and no retry happens; the manager corrects the reason and sends it again. SCR-09 Exception queue has no part in this story.

## RWB-E2-013 Approval routing with the delegation of authority table

Module: P7 Decision center and log

### Step 1

**In the story.** Calling module (for example the litigation route after R-LIT-03 generates a notice): calls ApprovalRouter.request with the case, decision, regulation item, product, amounts, preparer, source reference and the rule ID and version that asked for approval.

Another module starts this, not a person and not your code. For the first use, the litigation route calls you after rule R-LIT-03 generates a notice. You publish the interface ApprovalRouter in the Java package recovery.decision.approval with the method request(ApprovalRequest), which throws DecisionLogUnavailableException. The request carries the case, the decision code, the regulation item, the product group, the amounts, the recommendation, the preparer, the source type and reference, the rule id and version, and an idempotency key. Keep the preparer, because BR4 forbids that person from approving the item. Keep the rule id and version too, because AC1 expects the routing entry to record R-LIT-03 and LIT-2026.12.

### Step 2

**In the story.** Workbench (ApprovalRoutingService): for a decision with delegation rows, calls DelegationOfAuthority.lowestLevel and assigns the item to the holder of that level; for a decision with no amount limit, assigns it to the route role from the parameters.

ApprovalRoutingService chooses the approver with no person involved, and there are two paths. For a decision with delegation rows, call DelegationOfAuthority.lowestLevel through the P4 interface of RWB-E1-038, which returns the lowest level whose row covers the decision, product and amount on the routing date, and assign the item to the holder of that level. AC4 routes a 2,400,000.00 mortgage settlement to L6 holder U-9201. For a decision with no amount limit, read the route role from its parameters, which for D7.1 notices is rwb.approval.route.D7.1.role holding RW-LITOFF, and assign the item to that role rather than to one named person.

### Step 3

**In the story.** Workbench: where the level has no holder and no substitute, moves the item one level up at once and records why; where the lookup returns NOT_COVERED, holds the item and raises the incident.

Both branches are automatic. When the required level has no holder and no substitute, move the item one level up straight away and record the reason on the routing entry, which AC11 expects as NO_HOLDER for L6 with the item assigned to the L5 holder. An item must never wait on an empty level, per BR8. When the lookup returns NOT_COVERED, meaning no delegation row covers that decision and product, store the approval with status HELD_NO_LIMIT, leave the case at Waiting approval and raise an incident to RW-RISK with MSG-P7-010, which names the decision and the product. AC14 uses a hire purchase decision with no rows in DOA-2026.11.

### Step 4

**In the story.** Workbench: stores the approval with status WAITING, the level, the delegation row and version, and the due time; asks P3 to open the decision task and start the service level timer; writes the routing entry to the decision log; publishes EV-09 ApprovalRequested.

Your service does all of this in one transaction. Create the row in the new approval table from the migration V_E2_013__approval.sql with status WAITING, the level, the delegation row id and limit version, and due_at from the service level parameter, one working day for D7.1 notices and three working days by default. Call the P3 task and timer interfaces to open the decision task and start the service level timer. Write the routing entry through the decision log writer, and publish EV-09 ApprovalRequested with the approval id, case id, level and amount. P3 moves the case to Waiting approval, which AC1 checks.

### Step 5

**In the story.** Approver: opens SCR-10 Approval queue (GET /approvals) and sees the items waiting on them with decision, amount, level, limit and age.

A person does this. The approver opens SCR-10 Approval queue, which calls GET /api/recovery/v1/approvals and lists each item waiting on them with the decision, the case, the amount, the level, the limit version, the age and the due time. Build the screen as the React component ApprovalQueueScreen with its loading, list and empty states. The query returns the items assigned to that user and the items routed to a role they hold, and never an item they prepared, which AC1 checks for U-9211. The indexes ix_approval_assignee on (assigned_user_id, status) and ix_approval_role on (route_role_code, status) serve these reads.

### Step 6

**In the story.** Approver: approves, changes and approves, refuses or returns the item through the approval endpoints.

The approver acts through four endpoints, three of which already exist: POST /approvals/{approvalId}/approve, /refuse and /return, plus GET /approvals/{approvalId} for the detail. This story adds reasonCode from LOV-OVERRIDE-REASON, the changed terms and membersPresent to the approve request. Each call takes an Idempotency-Key header, so a repeated send does not produce a second outcome. Refuse and return both need a reason in text, and a refusal with no reason is rejected with 422 and MSG-GEN-001 for the field reason, which is AC8. A return sets status RETURNED and opens a task for the preparer, which is AC9.

### Step 7

**In the story.** Workbench (ApprovalDecisionService): checks the A letter in the decision's capability area, the caller's level against the required level, that the caller did not prepare the item, the reason or coded reason where needed, and the record version.

ApprovalDecisionService runs the checks before anything is written. Confirm the caller holds the A letter in the decision's capability area, taken from the parameter rwb.approval.area for that decision code, and that they are the holder or substitute of the required level or hold the route role; otherwise refuse with 403 and MSG-P4-002. Refuse the preparer with 409 and MSG-P7-002 even when that person is a substitute at the right level, which is AC6. Require a coded reason where the approver departs from the recommendation, refusing with 422 and MSG-P7-005. Check the record version with the optimistic lock, so the second of two approvers acting at once gets 409 and MSG-GEN-004.

### Step 8

**In the story.** Workbench: writes the decision entry with approver, approval level, limit version, rule ID and version and final call; sets the approval status; publishes EV-08 DecisionRecorded; P3 moves the case from Waiting approval to In progress and the source module acts (for a notice, release to dispatch, RWB-E2-014).

The writes happen together in one transaction, the decision log entry among them, so an outcome that cannot be recorded does not take effect. Write the entry with the approver, the approval level, the limit version, the rule id and version and the final call, APPROVED, REFUSED, RETURNED or ESCALATED. Set the approval status and publish EV-08 DecisionRecorded. P3 then moves the case from Waiting approval to In progress, and the source module acts on the outcome, which for a D7.1 notice is release to dispatch in RWB-E2-014. AC5 expects MSG-P7-004 in the response naming the new state. For a committee level, L1 to L3, the entry also holds the resolution reference and the members present.

### Step 9

**In the story.** Workbench (ApprovalEscalationListener): on EV-19 TimerBreached for an approval, moves the item one level up, or to the escalation role for a role-routed item, restarts the timer, writes the escalation entry and tells the new approver.

This happens on its own when an approval passes its service level. JOB-05 of RWB-E1-028 publishes EV-19 TimerBreached, and your ApprovalEscalationListener consumes it for approval timers. Move a limit-routed item one level up, and a role-routed item to the escalation role, which for D7.1 is rwb.approval.route.D7.1.escalation-role holding RW-HEADLIT. Raise escalation_level, set a new due time, restart the service level timer, write an entry with final call ESCALATED and tell the new approver with MSG-P7-011. The case stays at Waiting approval. AC2 moves the AC1 item to RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026. Test it with a fixed clock.

## RWB-E2-014 Approval screen for D7.1 demand and recall notices

Module: P7 Decision center and log, with P6 Communications

### Step 1

**In the story.** Notice module (P6): on EV-13 NoticeGenerated for a DEMAND or RECALL notice, calls ApprovalRouter.request with decision D7.1, source type NOTICE, the notice ID, the preparer and rule R-LIT-03 with its version.

No person does this. Build NoticeGeneratedListener to consume the event EV-13 NoticeGenerated, which the notice module publishes in RWB-E1-052 when it generates a notice from an Approved template. Filter to the notice types DEMAND and RECALL and ignore the rest. For each one, call ApprovalRouter.request with decision D7.1, source type NOTICE, the notice ID, the preparer, and rule R-LIT-03 with its version, for example LIT-2026.12. The routing itself is already built in RWB-E2-013: it creates the approval in status WAITING for role RW-LITOFF with a 1 working day service level and escalates to RW-HEADLIT. Your part is the listener and the call it makes.

### Step 2

**In the story.** Litigation officer: opens SCR-10 Approval queue and selects the D7.1 item.

A person does this. The litigation officer opens SCR-10 Approval queue, which exists from RWB-E2-013, and selects the waiting D7.1 item. Nothing happens to the notice at this point: it keeps the state Generated until the officer decides. Who can see and take the item is set by the routing of RWB-E2-013 and by the right Litigation A for decision D7.1, so a case owner holding Litigation R reads the case and cannot act on the approval. The person who prepared the notice may also hold a role that routes the item to them, and step 8 is where such a call is refused.

### Step 3

**In the story.** ACE front end: opens SCR-11 Decision screen with the SCR-18 Notice approval panel; loads the approval (GET /approvals/{approvalId}), the notice (GET /notices/{noticeId}), the document content and the case facts with their business dates.

The front end does this when the item is selected. Build DecisionScreen as the SCR-11 shell and NoticeApprovalPanel as the SCR-18 panel inside it. On open, make three reads: GET /api/recovery/v1/approvals/{approvalId} for the approval with its source reference, rule, version and due time, GET /api/recovery/v1/notices/{noticeId} for the notice, and the document content for the PDF. Read the case facts with their business dates as well: the case number and product group through the P3 interface, and the total balance through the P1 data product interface, which returns the value together with the business date of the load it came from. This story adds no new endpoint.

### Step 4

**In the story.** Workbench: shows the notice PDF, the case facts used in it (case number, product, total balance, the addressee's role, postal address masked per the masking rules), the business date of each input, the rule ID and version, the template code and version, and the preparer.

The screen shows this, assembled from the reads of the previous step. Put on one screen the notice PDF, the case number, the product group, the total balance with its business date, the role of the addressee, the postal address, the rule ID and version, the template code and version, and the user who prepared the notice. The address comes from contact_point as a masked value token through the DTO of the owning module, so the officer sees it in the form the masking rules allow and the raw value never reaches the browser. Showing each input with its business date is the point of the screen: the approver sees how old the facts are before deciding.

### Step 5

**In the story.** Workbench: checks each input's age against its limit and the template's current status; sets the screen state to Ready, Stale input or held.

The screen and the service do this together, with no person involved. Build InputFreshnessCheck to compare the business date of each input with its age limit parameter: rwb.decision.input-age-days.TOTAL_BALANCE is 1 day and rwb.decision.input-age-days.POSTAL_ADDRESS is 30 days. Read the current state of the template version the notice was built from as well. The result sets the screen state. Ready means every input is inside its limit and the template is still Approved. Stale input means an input is past its limit: show MSG-P7-006 with the input name and the age in days, and disable approve. A template withdrawn after generation holds the notice under R-LIT-04 and shows MSG-P6-003.

### Step 6

**In the story.** Litigation officer: approves; or picks another Approved template variant, enters a coded reason and approves; or rejects with a reason.

A person does this, and it is the decision the story exists for. The litigation officer has three actions on the panel: approve as proposed; pick another Approved template variant, enter a coded reason and approve; or reject with a reason. The variant list offers only Approved variants of the same notice type and product, such as DEMAND-MTG-B beside DEMAND-MTG. The coded reason comes from LOV-OVERRIDE-REASON, which holds TEMPLATE_VARIANT and WRONG_PARTY. A rejection needs free text and is refused with 422 and MSG-GEN-001 when the reason is empty. A variant change with no reason code is refused with 422 and MSG-P7-005, and no new notice version is generated.

### Step 7

**In the story.** Workbench: for a change, calls NoticeApi.regenerate with the chosen template; the new notice version replaces the proposed one on the approval.

This runs only when the officer changed the variant, and the service does it. Call NoticeApi.regenerate with the notice ID and the chosen template code. The notice module builds a new notice version from that Approved variant and returns a NoticeRef. Put the new version on the approval in place of the proposed one, so the version the officer looked at is the version approved and the only one that can reach dispatch. The decision entry of the next step records both: the proposed template DEMAND-MTG, the chosen DEMAND-MTG-B and the reason code, under the final call APPROVED_CHANGED. The notice version first proposed is kept and is never sent.

### Step 8

**In the story.** Workbench: calls the approval endpoint (RWB-E2-013 checks: Litigation A, not the preparer, reason rules); writes the decision entry with inputs reference, rule version, template version, approver and time.

NoticeApprovalService calls the approval endpoint, POST /approvals/{approvalId}/approve or POST /approvals/{approvalId}/refuse, with an ApprovalAction holding the reason, the reason code and, for a change, changes.templateCode. The checks come from RWB-E2-013 and you rely on them: Litigation A for D7.1, and the preparer rule, which refuses with 409 and MSG-P7-002 when the approver prepared the notice. The call writes the decision entry with the inputs reference and the business date of each input, the rule version, the template version, the approver and the time. Send an Idempotency-Key header. An item another approver already decided is refused with 409 and MSG-GEN-004, and a failed entry write gives 503 with MSG-P7-003.

### Step 9

**In the story.** Workbench: on approval, calls NoticeApi.approve so the notice state becomes Approved for the 16:00 dispatch run (JOB-10, RWB-E2-021); on rejection, calls NoticeApi.hold with reason REFUSED_BY_APPROVER and opens a task in the case owner's queue with the reason.

The service does this straight after the entry is written, with no person involved. On approval, call NoticeApi.approve with the notice ID and the decision entry ID, which moves the notice from Generated to Approved and makes it part of the 16:00 dispatch run, JOB-10 in RWB-E2-021. On rejection, call NoticeApi.hold with the reason code REFUSED_BY_APPROVER and the entry ID, which moves the notice from Generated to Held, and open a task in the case owner queue carrying the reason text of the officer. The approval entry and the notice state change commit in one transaction, so no notice is Approved without its entry.

### Step 10

**In the story.** Workbench: shows MSG-P7-004 and sets the screen state to Decided.

The screen does the last part, with no person involved. Show MSG-P7-004, Approved. The case moves to {state}, and set the screen state to Decided, which shows the outcome, the approver and the decision time and offers no action. A screen loaded before another approver decided reloads into that same state and names the approver who was first. The approval also publishes EV-08 DecisionRecorded for anything downstream that listens to it. The case status returns to In progress on approval, and a rejection leaves the case In progress with the new task in the case owner queue.

## RWB-E2-015 Timers, escalation and the deviation flag on the case record view

Module: P3 Case and workflow

### Step 1

**In the story.** Case owner: opens SCR-03 Case record for a case.

A person does this, on the screen RWB-E1-035 already built. This story adds two panels to it, the React components CaseClocksPanel and DeviationPanel in src/modules/recovery/casewf/caserecord. The case owner has to hold Case record R and have the case in scope. Put both panels behind feature flag rwb.p3.case-clocks; with the flag off SCR-03 shows the Epic 1 read only fields and nothing else changes. Both panels are read only, so nothing the user does on this screen changes a timer, a deviation or the case.

### Step 2

**In the story.** Front end: calls `GET /cases/{caseId}` and `GET /cases/{caseId}/timers`.

This happens on its own when the screen loads. Both endpoints exist in P3 already and this story extends them. GET /cases/{caseId} gains the array deviations, holding deviationCode, raisedAt, handlerUserId, approverUserId, pausedState, contactStop, clearedAt and outcome, plus the boolean deviationsAvailable. GET /cases/{caseId}/timers gains nextStepOwnerRole, escalatedToRole, escalatedAt, nextEscalationRole and inWarning on each Timer. Add the fields to the API file and regenerate the types the front end uses. Both need Case record R with scope applied, and both answer 404 with MSG-P4-003 for a case outside the scope. While the calls are in flight the panels show skeleton rows.

### Step 3

**In the story.** Case service: reads the case, its timers and, for each timer with a task, the owner role of the task.

This happens on its own on the server. Build TimerViewService with TimerRepository reading the timers of the case and, where timer.task_id is set, the owner_role of that task, which becomes nextStepOwnerRole so the screen can name who acts next. Show every timer with status Running, Paused or Expired, with its type, started_at, expires_at, warn_at, paused flag and escalation_level. Read through the existing indexes ix_timer_case_id and ix_task_case_id. Resolve the timer type labels through the P4 list interface from LOV-TIMER rather than writing them in code, and order the timers by due date for the panel.

### Step 4

**In the story.** Case service: reads the open deviations from `DeviationQuery` and the approver of each from the P7 decision log query.

This happens on its own in CaseViewService, through two published interfaces. Call DeviationQuery.forCase(caseId) on the deviation module S8 with the 2 second timeout from caseview.deviation-timeout-ms, and for each deviation call DecisionLogQuery.approverOf(caseId, decisionCode, raisedAt) on P7, which returns the approver's user ID. Reading the deviation or decision log tables directly is not allowed. When S8 does not answer in time, set deviationsAvailable false and still return the case, so the timers and the on hold banner taken from recovery_case.deviation_open still show. The caller needs no Decision log right, because only the approver's user ID comes back.

### Step 5

**In the story.** Case service: reads the escalation role for the case's product and status from `ProductParameterService.serviceLevel(...)`.

This happens on its own. Call ProductParameterService.serviceLevel(productGroup, caseStatus, businessDate) on the P3 interface from RWB-E1-045 and take the escalation role the SERVICE_LEVEL row names for that product group and status, for example RW-PRODHEAD for HIRE_PURCHASE at IN_PROGRESS. Return it as nextEscalationRole on the timer, beside escalatedToRole and escalatedAt. Those two columns are new: migration V<next>__rwb_e2_015_timer_escalation.sql adds timer.escalated_to_role and timer.escalated_at, and EscalationRecorder changes the escalation step of JOB-05 from RWB-E1-028 to write them. The escalation roles themselves are data rows set by the business.

### Step 6

**In the story.** Front end: shows the timers ordered by due date, each with status, due date, warning state, escalation level, escalated to and the next escalation point.

This happens on its own in the browser. CaseClocksPanel renders the timers from the response in due date order, nearest first. Per timer show the type label, the due date, the status, the escalation level, the role it was escalated to with the time, and the next escalation point. A paused timer shows the date it paused, for example Paused since 2026-12-10. Resolve role codes to display names through the ACE common module, so RW-TEAMMGR reads as Team manager. When the case has no timer with status Running, Paused or Expired, show MSG-P3-018 in place of the list. A breached service level changes neither the queue nor the case status.

### Step 7

**In the story.** Front end: shows the prescription date with the warning when the business date is on or after the prescription timer's warn at.

This happens on its own in the browser. Show recovery_case.prescription_date in the panel at all times, and add the warning MSG-P3-003 once the business date has reached the warn_at of the PRESCRIPTION timer. That warn_at comes from prescription.warning-days, which is 90, so a prescription date 60 days ahead warns and one 91 days ahead does not. Take the number of days from the configuration service rather than counting them in front end code. The prescription clock keeps running while a deviation is open, so this warning shows on a case on hold as well, which is the gap control CTL-18 was raised against.

### Step 8

**In the story.** Front end: when a deviation is open, shows state On hold with MSG-P3-004, each deviation's code, handler, approver, raised date, contact stop and return point.

This happens on its own in the browser. While any deviation on the case is open, DeviationPanel puts SCR-03 in its On hold state with banner MSG-P3-004, which names the deviation and repeats the prescription date. List every deviation with its code label from LOV-DEVIATION, the handler, the approver from P7, the raised date, the return point, which is the routing state the case was in when it paused, and Contact stopped for codes X1, X2 and X3. A cleared deviation shows its cleared date and outcome. The case leaves On hold only once every open deviation is cleared, so with two open deviations the banner holds until both clear. When S8 did not answer, show MSG-GEN-006 naming Deviation handling in this section and keep the banner from the case flag.

## RWB-E2-016 Full case record view with the history timeline

Module: P3 Case and workflow, with P7 Decision center and log

### Step 1

**In the story.** Case owner: opens SCR-04 Case timeline from SCR-03 Case record.

A person navigates here. SCR-04 is a new screen in this story, opened from the case record, and it holds the full timeline with its filters and the queue history. The timeline panel inside SCR-03 from RWB-E1-035 stays as it is. Build CaseTimelinePage in src/modules/recovery/casewf/timeline with a Loading state of skeleton rows and a Filtered state for the list after a filter is applied. The feature flag rwb.p3.full-timeline controls the new screen; with the flag off, the user sees the older panel on SCR-03.

### Step 2

**In the story.** Front end: calls `GET /cases/{caseId}/timeline` with the filters kept for the session.

The page makes the call on its own when it opens, and again each time a filter changes. The endpoint already exists from RWB-E1-035, and this story adds page with a default of 0, size with a default of 50 and limits of 1 to 200, the type and date filters, and unavailableSources in the answer. Keep the chosen filters in session storage, so a user who leaves the screen and comes back sees the same view. Answer 422 with MSG-GEN-002 when size falls outside 1 to 200. The new parameters are build step 3.

### Step 3

**In the story.** Timeline service: checks the scope and the caller's rights in Decision log, Documents and Litigation.

TimelineService runs this check on every call. First the case: a caller without Case record R receives 403 with MSG-P4-002, and a case outside the caller's scope receives 404 with MSG-P4-003. Then the item types: Decision log R allows decision items, Documents R allows document items, Litigation R allows notice items. A caller without one of those rights simply sees no items of that type, with no error, which is what a phone collector sees on the AC5 case. Run the rights check before the source calls, so you never fetch what the caller may not read.

### Step 4

**In the story.** Timeline service: reads assignments, interactions and timer events from the P3 tables, and in parallel calls the P7, P5 and P6 interfaces for the sources the caller may read, each with a 2 second timeout.

The service does all of this inside one request. Read assignment, interaction and timer from the P3 tables through AssignmentHistoryRepository and InteractionRepository, using ix_assignment_case_id, ix_interaction_case_time and ix_timer_case_id. At the same time call DecisionLogQuery.forCase, DocumentQuery.forCase and NoticeQuery.forCase, each on its own thread so the three waits overlap instead of adding up. The limit is the parameter timeline.source-timeout-ms, 2000 milliseconds. A source that does not answer in time is left out, its name goes into unavailableSources, and the screen shows MSG-GEN-006 naming it while the items from the other sources still show.

### Step 5

**In the story.** Timeline service: maps each record to a timeline item with time, type, summary, actor and reference, merges them newest first and returns one page.

TimelineItemMapper and the service do this in code. The seven kinds of record have different shapes, so each becomes the same timeline item: the time, the type, a one line summary built from code values and their labels, the actor and a reference to the record behind it. Mask personal data in a contact summary by role through the ACE common module, and never log it. Merge the lists into one, order them newest first, keep the order of each source's own sequence for items that share a time, and return the page the caller asked for with the total count.

### Step 6

**In the story.** Front end: shows the timeline in state Loading, then the list; the filter by type and date reloads it in state Filtered.

The page handles its own states. Show skeleton rows while the call is running, then the list of items with type, actor and time. When the user changes the type filter or the date range, call the endpoint again and show the answer in the Filtered state. Type labels and reason code labels come from LOV-ASSIGN-REASON and LOV-TRANSFER-REASON through the P4 list interface, so no wording sits in the code. A filter that matches nothing shows MSG-P3-019, and a date range with to before from is refused with MSG-GEN-003 naming the two fields.

### Step 7

**In the story.** Case owner: opens Queue history; the front end calls the timeline with type ASSIGNMENT and TRANSFER and shows from queue, to queue, from owner, to owner, reason code and rule ID for each move.

A person opens this view, and it reuses the same endpoint. QueueHistoryTab asks for types ASSIGNMENT and TRANSFER only, and renders one row per move with the queue and the owner the case came from and went to, the reason code with its label, and the rule ID. The queue on the assignment comes from RWB-E2-012, so an assignment written before that story has no queue_id and its row shows Queue not recorded. The first allocation of the case is one of these rows and shows with reason ALLOCATION, which test TC-E2-016-03 checks together with the three transfers.

### Step 8

**In the story.** Case owner: opens a decision item; the front end opens the entry through `GET /decision-log/{entryId}` (P7).

A person opens the item, and the front end then calls the P7 endpoint with the entry ID that the timeline item already carries as its reference. That call needs Decision log R, which the caller holds, because an item of this type reaches only a caller with that right. A decision log entry is never changed after it is written, and a correction appears as a further entry, so the page shows what was decided at the time. Keep no copy of the entry in P3 tables; the timeline holds the reference and reads the entry through P7.

## RWB-E2-017 Contract, CA and mortgage document generation screens

Module: P5 Document hub

### Step 1

**In the story.** Restructuring officer: opens SCR-14 Treatment record for an approved deed in lieu treatment and chooses Generate documents.

A person starts this. The restructuring officer, holding RW-RESTRUCT with scope over the case, opens SCR-14 Treatment record for a deed in lieu treatment that was approved at D6.4, and chooses Generate documents. You build GenerateDocumentsPanel, the React component that adds this to SCR-14. The control is available only while the treatment is approved and still open, which the panel reads from treatment.decision_log_id and treatment.outcome: a treatment with no decision_log_id has not been approved, so the panel disables the control and shows MSG-P5-011, and a direct call returns 409 with the same message. The whole panel is hidden while the feature flag rwb.dochub.generation-screens is off.

### Step 2

**In the story.** System: shows the document set for the treatment type and product, with the current approved version of each template.

The Workbench does this with no person involved. Read the document set for the treatment type and product group from the template catalog in reference data (RWB-E1-046), and for each template read the current version that Legal approved. DEED_IN_LIEU gives DIL-CONTRACT, DIL-CA and DIL-MORTGAGE; RESTRUCTURE gives RES-AGREEMENT. Show each template with the version the drafts will be made from, which for the deed in lieu set of AC1 is versions 2, 1 and 1. The set and the versions are data owned by Legal, so hold none of them in code. Templates are reached through the published interface of the owning module, never by reading its tables.

### Step 3

**In the story.** Restructuring officer: confirms; the system calls the generation engine (RWB-E2-026) and shows the three drafts with their merge values.

The officer confirms, and the Workbench then calls the generation engine. Post to POST /api/recovery/v1/cases/{caseId}/generated-documents, the endpoint RWB-E2-026 defines, which fills each template with the case facts and returns the drafts. Show the three drafts with the merge values that were filled, a merge value being one named field in the template, for example the contract date or the transfer price. Each draft is a document of its own type, CONTRACT, CREDIT_APPROVAL or MORTGAGE_DOCUMENT, all three legal types in the document type table, held at doc_version 1 in state DRAFT. The merge rules and the template selection belong to RWB-E2-026.

### Step 4

**In the story.** Restructuring officer: opens a draft; the system shows the PDF next to the list of merge values, with locked values read only.

A person reads here, and the work is in the component. Build GeneratedDocumentReview on SCR-30 Case documents: the PDF of the draft on one side and the list of merge values on the other. Each merge field is marked overridable or locked in the merge field catalog, and a locked one is shown read only. Amounts, parties, title numbers and the treatment terms are locked, and the dates of signing and the witness details are overridable. Show the fields read only for a team manager as well, who holds Documents R. Reading the catalog flag in the component keeps the officer from attempting a change that the endpoint would refuse.

### Step 5

**In the story.** Restructuring officer: corrects an overridable value and enters the reason.

The officer does this in the review component, which calls POST /documents/{documentId}/regenerate. You build that endpoint, which is new and recorded in the additions file. The request is RegenerateRequest: between one and ten overrides, each holding the merge field, the new value and a reason, plus the version of the document the officer read. An empty reason is refused with 422 and MSG-GEN-001 naming Reason, and a change to a field that the catalog locks is refused with 422 and MSG-P5-014 naming the field. A document already in state SENT is refused with 409 and MSG-P5-002. The second of two officers saving against the same version gets 409 with MSG-GEN-004.

### Step 6

**In the story.** System: writes a decision log entry with the override and its reason, regenerates the draft as the next doc_version, and keeps the earlier version readable.

The Workbench does all of this in DocumentSetService, in an order you have to keep. Write the decision log entry first, through DecisionLogWriter, carrying the decision code, the old value, the new value and the reason as override_reason. Then call DocumentGenerator.generate with the overrides and store the result as the next doc_version, leaving the earlier version readable. A failed decision log write stops the whole action with 503 and MSG-P7-003, with the document left at its doc_version and no file added. A correction on a REVIEWED document moves it back to DRAFT at the new doc_version, so the officer has to review it again.

### Step 7

**In the story.** Restructuring officer: marks each draft reviewed; the system sets state REVIEWED.

The officer does this for each draft, and the Workbench records it. The call is POST /api/recovery/v1/documents/{documentId}/review with action COMPLETE, the endpoint that RWB-E1-054 adds. Extend it for generated drafts so that it sets the document state to REVIEWED and review_status to CONFIRMED where nothing was corrected or CORRECTED where something was. Every document of the set has to reach REVIEWED before the send in step 9 is allowed, which is why the Mark reviewed control is per draft and not per set.

### Step 8

**In the story.** Restructuring officer: chooses Send for signature.

The officer does this once, on SCR-14 from GenerateDocumentsPanel, and the control is available only while every draft of the set is reviewed. The request goes to POST /treatments/{treatmentId}/signature-requests with the treatment ID, the list of document IDs and a required Idempotency-Key header, which the Workbench keeps for 24 hours under the parameter GEN_IDEMPOTENCY_HOURS. That key is what makes a repeated send safe: the same key arriving again returns the first result, with one signature request for the treatment and no second copy to the container. The send step sits behind its own flag, rwb.dochub.generation-screens.send, until RWB-E2-018 is merged.

### Step 9

**In the story.** System: checks every document of the set is REVIEWED, copies each final file to the write-once container, writes the decision log entry for the send, starts the signature request in P6 and sets each document to state SENT with write_once true.

The Workbench does the whole sequence, and the order is fixed. Check that every document of the set is REVIEWED and was made from the template version that is current now; a document that fails either check gives 422 with MSG-P5-013, naming the document and the reason, and nothing is sent. Then copy each final file to the write-once container through BlobStorageAdapter, which is idempotent by file hash through ContentHashGuard. Then write the decision log entry with final_call SENT_FOR_SIGNATURE. Then call SignatureRequests.start in P6; an answer of UNAVAILABLE gives 503 with MSG-GEN-006 and leaves every document REVIEWED. On an accepted request, set each document to state SENT with write_once true.

### Step 10

**In the story.** System: shows MSG-P5-012; the documents show as sent on SCR-30 Case documents.

The Workbench does this once the send succeeds. The screen shows MSG-P5-012 with the count of documents sent, three for the deed in lieu set, and each document appears on SCR-30 Case documents in state SENT. A sent document is read only: SCR-30 shows it without edit controls, and a later attempt to correct it is refused with 409 and MSG-P5-002. The file in the write-once container is never changed after this point, so a correction has to be made before the send. The signature flow itself, the wet ink path and the return of the signed copy belong to RWB-E2-018.

## RWB-E2-018 E-signature flow for customers and the bank

Module: P6 Communications

### Step 1

**In the story.** Restructuring officer: on SCR-14 Treatment record chooses Send for signature on a generated agreement.

A person starts this, the restructuring officer, or the case owner on a case in their scope. The agreement document already exists on the case, generated and stored in the document hub by RWB-E2-017. Build SendForSignatureDialog as a React component on SCR-14 Treatment record, shown while the treatment is approved and the offer is with the customer. The dialog lets the officer pick the document and the party who signs, and the request list beside it shows each request with its status. The customer never signs in the Workbench and has no login there; they sign in EasyApp or on paper at a branch.

### Step 2

**In the story.** System: reads the signature basis of the agreement's template; offers E-signature only when the basis is E_SIGNATURE_ALLOWED, otherwise Branch or Paper.

Your code decides which methods the officer may choose. Read signature_basis from the template the document was generated from, which Legal counsel sets in RWB-E1-034 to either E_SIGNATURE_ALLOWED or WET_INK_REQUIRED. When the basis allows it, offer E_SIGNATURE, BRANCH and PAPER; when Legal requires wet ink, offer only BRANCH and PAPER. Apply the same rule again on the server in SignatureService.create, because the dialog alone cannot hold the rule. A request with method E_SIGNATURE for a wet ink template is refused with 409 and MSG-P6-009 naming the template, and nothing reaches EasyApp.

### Step 3

**In the story.** System: runs the conduct check for the customer (RWB-E2-022); a contact stop or legal hold refuses the request.

Your code calls the check built in RWB-E2-022 before it creates anything. A signature request sent to a customer is an outbound contact, so it passes the same conduct check as any other contact. An open deviation with a contact stop refuses the request with 409 and MSG-P6-001 naming the deviation, for example X2 Vulnerable customer or hardship. A legal hold on the case refuses it with 409 and MSG-P3-004. In both cases no signature_request row is written and nothing goes to the outbox. Test this with an open X2 carrying a contact stop, and check that the EasyApp stub received no call.

### Step 4

**In the story.** System: creates the signature request (method, document, party, expiry equal to the treatment's offer validity) and, for E-signature, writes the send to the outbox for the ACE path to EasyApp.

Your code writes the row and queues the send automatically. Insert a signature_request row with the case ID, the treatment ID, the document ID, the party ID, the method, the status, and expires_at taken from the treatment's valid_until, so the request ends with the offer and not on a date of its own. Create the table in the migration V2_018__signature_request.sql with a unique index on external_ref and an index on treatment ID and status. For E_SIGNATURE, write the send to the outbox in place of calling EasyApp inline; JOB-11 Outbox sender delivers it through EsignPort with a retry limit of 5, and an unavailable path answers 201 with status QUEUED and MSG-GEN-006.

### Step 5

**In the story.** Customer: signs in EasyApp; EasyApp adds the bank signature with the bank certificate and returns the signed PDF through the ACE path.

This happens outside the Workbench. The customer opens EasyApp and signs there, and EasyApp applies the bank signature using the bank signing certificate held in the key store. The Workbench never holds the private key and never calls EasyApp directly; the ACE common module owns that path under INT-34. EasyApp returns the signed PDF, the result and the time of signing through the same path. Your side of it is the method the ACE module calls, SignatureResultListener.onEasyAppResult, taking the external reference, the result, the signed PDF bytes and the signing time. Test everything behind a stub of that path, using synthetic PDFs.

### Step 6

**In the story.** System: stores the signed PDF as a new write-once version of the agreement on the case, sets the request Signed and calls TreatmentApi.recordSignature, which raises CUSTOMER_SIGNED in P3.

Three writes happen automatically in your listener, within 60 seconds of the result arriving. Call DocumentHubApi.addVersion to store the signed PDF as a new version of the same document with write_once true, which means a stored version can never be changed or replaced, only followed by a further version. Set the signature request to status SIGNED with signed_at and signed_document_id. Then call TreatmentApi.recordSignature with signed true and the method used, which is how the case moves; P3 owns the treatment fields and this story writes none of them directly. Make the listener idempotent on the external reference and the result, so a repeated result stores no second document.

### Step 7

**In the story.** Customer at a branch: signs the paper agreement; the branch scan arrives through JOB-12 Document intake; the restructuring officer links the scan and records Signed.

Three actors appear here and only the last one calls your endpoint. The customer signs the printed agreement at a branch. The branch scan reaches the case through JOB-12 Document intake, which already exists, so this story does not load the image. The restructuring officer then calls POST /signature-requests/{requestId}/result with result SIGNED, the scanned document ID and the signed date, and your code sets the request to SIGNED, links the scan to the generated agreement with DocumentHubApi.linkSigned, and calls TreatmentApi.recordSignature with method BRANCH. A result recorded with no scanned document is refused with 422 and MSG-GEN-001 naming the signed document.

### Step 8

**In the story.** For a deed in lieu with WET_INK_REQUIRED: the officer records the paper signature with the scan; P3 receives CUSTOMER_ACCEPTED with signature basis wet ink and routes to the field inspection and then the Land Office transfer (R-DIL-18, R-DIL-27).

The officer records the result as in the branch path, with method PAPER and the scan of the signed contract, and the rest is P3's work. Pass the signature basis with the recorded signature, because wet ink is what sends a mortgage deed in lieu to the collateral inspection before the transfer. On that event P3 moves the case to WITH_FIELD_INSPECTION under rule R-DIL-18, and later to the Land Office transfer under R-DIL-27. Build neither the inspection nor the transfer, since both are Epic 3 screens. Your test checks the route state after the result, using a deed in lieu treatment whose contract template carries WET_INK_REQUIRED.

### Step 9

**In the story.** System: a decline in EasyApp sets the request Declined and records not signed; an expiry from P3 cancels the request.

Two closing paths run automatically. When EasyApp returns DECLINED, set the request to status DECLINED and call TreatmentApi.recordSignature with signed false, which lets the route set's decline rule return the case. When the offer validity passes with no signature, P3 raises OFFER_EXPIRED and calls SignatureApi.cancel, which you implement in SignatureApiService to set the request to EXPIRED. A signing result that arrives after that keeps the request EXPIRED, makes no call to recordSignature, and goes to the exception queue on SCR-09. A result naming an external reference that matches no request goes to the same queue with the reason unknown signature request.

## RWB-E2-019 Partner identities through the external gateway

Module: P4 Access and administration

### Step 1

**In the story.** Partner and agency manager (RW-AGENCYMG): requests a partner user in the bank IAM, naming the firm, the partner role and the person's business e-mail at the firm.

A person does this, the partner and agency manager, and it happens in the bank IAM rather than in the Workbench. The request names the firm, the partner role and the person business e-mail at that firm. There is no code to write for this step: partner users are requested by the partner and agency manager, approved by the role owner and created by the access administrator, all three in the bank IAM. Your code never creates a partner identity and never holds a partner e-mail, because a partner is referenced by the directory ID of the identity. The same manager also sets the firm panel status in the partner management module, which decides later whether a sign-in is allowed.

### Step 2

**In the story.** Role owner: approves the request; access administrator creates the partner identity in the partner directory and adds it to the group of the partner role.

Two people do this in the bank IAM, so that nobody both asks for access and grants it. The role owner approves the request at level 2 and the access administrator creates the identity at level 3. The identity is created in the partner identity directory, which is separate from bank identities and reachable from the external gateway in SIT and UAT; in production it waits for DL03. The administrator then adds the identity to the group of its partner role, one group per role and environment, for example RWB-SIT-PT-LAWFIRM. Your code builds none of this. What it reads later is the role table: the role code, the role class PARTNER_USER and the Entra group of each partner role.

### Step 3

**In the story.** Reference data administrator (RW-REFADM): loads the partner user binding (partner identity, partner ID, role, valid from, valid to) with POST /admin/reference-loads table "partner_user"; RW-SECADM approves it.

Two people do this. The reference data administrator loads the binding file through the shared reference load endpoint for the table partner_user, and the security administrator approves it, as the parameter rwb.refload.approver.partner_user says. The binding ties one directory identity to one firm and one partner role for a period; an identity with no active binding is refused. Create the table partner_user with the migration V_E2_019__partner_user.sql, holding id, identity_ref, partner_id, role_code, valid_from and valid_to with the standard columns, and a unique index on identity_ref and valid_from. Add no foreign key to partner, which is a column forced to match a row in another table, because partner belongs to the partner management module. Build PartnerUserLoader to check the partner IDs through the S9 interface, to allow partner role codes only, and to refuse an identity bound twice in one period.

### Step 4

**In the story.** Partner user: opens the partner portal through the external gateway and signs in with password and second factor.

A person at the partner firm does this. Partners reach the Workbench only through the external gateway, and that route is theirs alone: a bank identity on it is refused, and a partner identity on the bank route is refused as well. The second factor is multi-factor authentication, a second proof of identity beyond the password, and the Workbench reads it from the token rather than asking for it again. Build PartnerSignInPage as the entry screen in the partner portal, with the refusal states for MSG-P4-008 and MSG-P4-001 and no data shown on either. Keep the whole partner route behind the feature flag rwb.access.partner-signin, which stays off in production until DL03 is approved.

### Step 5

**In the story.** Workbench (SessionResolver): checks the token comes from the partner directory, holds "mfa" in the amr claim and maps to exactly one partner role; finds the active binding for the identity.

Code does this on every sign-in, with no person involved. Extend SessionResolver from RWB-E1-022 to tell the partner route from the bank route and to make four checks. The token has to come from the partner directory, so a bank identity on this route is refused with MSG-P4-001 and an AC-DENY entry with reason BANK_IDENTITY_ON_PARTNER_ROUTE. The amr claim, which is the list in the token of how the person proved who they are, has to hold "mfa", or the session is refused with 401 and MSG-P4-005. The identity has to map to exactly one partner role: two partner role groups, or a partner and a bank group together, are refused with MSG-P4-006 and an incident to the security administrator queue. Last, read the active binding from partner_user; with none, refuse with 401, MSG-P4-001 and reason NO_PARTNER_BINDING.

### Step 6

**In the story.** Workbench (PartnerAccessService): asks the S9 interface for the firm's panel status and contract end; refuses the session unless the status is ACTIVE or ON_NOTICE and the contract end is today or later.

Code does this check at sign-in. Build PartnerAccessService to call the S9 published interface for the firm, which returns the panel status and the contract end, and read neither from the partner table, because that table belongs to the partner management module. Allow the session only when the status is ACTIVE or ON_NOTICE and the contract end is today or later. A firm that is SUSPENDED or EXITED, or whose contract end has passed, means the sign-in is refused with MSG-P4-008 and an AC-DENY entry with reason PARTNER_NOT_ACTIVE, as AC3 shows for firm LF-0012 at 11:20. This check is what makes a firm lose access on the day it leaves the panel.

### Step 7

**In the story.** Workbench: resolves the session with scope PLACED, the partner ID and the instruction types of the role; writes an AC-SIGN entry.

Code builds the session, with no person involved. Add the scope type PLACED to ScopeFilter and return it from scopeFor for a partner session, carrying the partner ID and the instruction types of the role. PLACED means the session may see only the cases and instructions placed with that one firm. Take the instruction types from the parameters that name them per role, FILE_SUIT and ENFORCE for a law firm, APPRAISE for a valuer and COLLECT for an agency, owned by the partner and agency manager, so they stay data. Write one AC-SIGN entry in the decision log for the sign-in, in the same way as for a bank user, since the access log applies to partner users as well. GET /me/session returns the partner ID and the scope for the front end.

### Step 8

**In the story.** Partner portal PRT-01 Partner home: lists the open instructions through GET /partner/instructions; the S9 handler applies the PLACED scope filter, so only instructions of the partner's firm and of the role's instruction types return.

The partner sees this screen; the endpoint behind it belongs to the partner management module, and this story supplies the scope filter it applies. PRT-01 Partner home has two states, Loading while the instructions are fetched and List showing the firm open instructions with their due dates. The S9 repository applies the PLACED filter inside its query, so an instruction of another firm never reaches the response: AC1 returns the 5 instructions of LF-0012 and none of LF-0019, and AC2 returns the 2 APPRAISE instructions of a valuer and not the LIST one. A direct request for an instruction of another firm answers 404 with MSG-P4-003 and no data. Write the repository test for those three cases in S9.

### Step 9

**In the story.** Workbench: on each request, checks the binding and the firm status again (refreshed at most every 5 minutes, assumed; DL38) and ends the session when either has ended.

Code does this on each request, and no job and no person ends the session. Build PartnerSessionRevalidation to read the binding from partner_user and the firm status from the S9 interface again once the refresh interval has passed, with the interval taken from the property rwb.access.membership-refresh-minutes, five minutes. A firm that changes during an open session therefore loses access at the first request after that interval: AC3 moves LF-0012 to EXITED at 11:00 and ends the session opened at 10:00 at its first request after 11:05. The permission matrix applies on every request as well, so a partner calling an endpoint outside the letters of the partner role, such as the queue list, is refused with 403 and MSG-P4-002.

## RWB-E2-021 Letter dispatch loop with proof of delivery from WIN

Module: P6 Communications

### Step 1

**In the story.** Litigation officer: requests a notice through POST /cases/{caseId}/notices; the system calls NoticeApi.generate (RWB-E1-052) and returns the notice in state Generated.

A person starts this. Build NoticeController with POST /api/recovery/v1/cases/{caseId}/notices taking NoticeRequest with noticeType required, partyId defaulting to the borrower and language defaulting to TH, and returning 201 Notice. Authorization is Litigation C with scope applied, so the litigation officer or the enforcement owner may call it. The controller calls NoticeApi.generate from RWB-E1-052 and adds no generation logic of its own. The Idempotency-Key header is kept for 24 hours and a repeat returns the first notice, which AC10 tests. A request with no notice type answers 422 with MSG-GEN-001 naming the field.

### Step 2

**In the story.** Approver: approves the notice on SCR-18 (RWB-E2-014); state Approved.

A person approves the notice on SCR-18, the screen built in RWB-E2-014, and this story builds nothing here. The notice reaches state Approved, which is the only state this story dispatches: the configuration key rwb.comms.dispatch.eligible-states is set to APPROVED, so the job of the next step picks up Approved notices alone. Holding that list in configuration rather than in code lets another state become eligible later without a release. Read the key in the job rather than writing the state name into the query.

### Step 3

**In the story.** JOB-10, daily 16:00: for each Approved notice runs the conduct check: legal hold on the case, open deviation with contact stop, current template still Approved, statutory status of the notice type.

The job runs on a daily schedule at 16:00. Build ConductCheckService and call it from WinNoticeFileJob, which comes from RWB-E1-055, before each file record is written. The four checks run in order: a legal hold on the case, an open deviation carrying a contact stop, the template of the notice still being Approved, and the statutory status of the notice type. Read the hold through CaseWorkflowApi.getCaseSummary, the stops through DeviationApi.activeContactStops on S8, and the statutory notice type list from reference data. The service returns Passed or Blocked with the reason and the rule ID, and runs inside the same transaction that selects the notice for the file.

### Step 4

**In the story.** System: a notice that fails the check is held, the reason is written to the decision log and to the ledger with conduct check Blocked, and the case goes to the deviation owner (R-LIT-05) or the hold owner; it is not written to the file.

The job does this with no person involved. Set the notice state to Held with hold_reason naming the cause, such as CONTACT_STOP_X1, LEGAL_HOLD or TEMPLATE_WITHDRAWN, and leave it out of the WIN file. Write the decision log entry through DecisionLogApi.write with decision code D7.1 and the rule that blocked it, R-LIT-05 for a contact stop, and the ledger entry through InteractionLedgerApi.record with conduct_check set to BLOCKED. Then call CaseWorkflowApi.applyEvent so P3 routes the case. AC4 routes it to the complaint officer with MSG-P6-001 naming X1 Dispute or complaint, and AC7 shows MSG-P3-004 on the case record for a legal hold.

### Step 5

**In the story.** System: a notice that passes is written to the INT-14 file with conduct check Passed; the WIN acknowledgment sets Sent with the barcode (RWB-E1-055) and the ledger entry carries the barcode.

The job and the acknowledgment handling do this; both come from RWB-E1-055, and what this story adds is the conduct result on each record and on the ledger entry. The notice is written to the INT-14 file with conduct check Passed. The WIN acknowledgment then sets the notice to Sent with its sent date and barcode, the number printed on the mail item that the later proof is matched by, and the ledger entry carries that barcode. Publish NoticeDispatched, EV-14. AC1 runs JOB-10 at 16:00 on 2026-12-14 and expects sent date 2026-12-15 with barcode RR223344556TH and conduct check PASSED.

### Step 6

**In the story.** JOB-09: loads the INT-15 file; a Delivered record sets Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).

JOB-09 loads the file on its own. Add the INT-15 result column to the file reader and map its result codes to LOV-DELIVERY through the code map, which the data steward owns. Build DeliveryResultHandler: a DELIVERED record sets the notice state Delivered with callback_date and delivery_status, writes the ledger entry and publishes NoticeDelivered, EV-15. P3 then starts the NOTICE_PERIOD timer from the delivery date under R-LIT-07, so the period runs from the proof date. AC2 returns barcode RR223344556TH with call-back date 18122026 and expects the timer running from 2026-12-18.

### Step 7

**In the story.** System: a Refused or Undeliverable record sets Unserved, writes the decision log entry under R-LIT-09, writes the ledger entry and raises DELIVERY_FAILED to P3, which transfers the case to the owner's queue with reason NOTICE_UNSERVED.

The same handler takes this branch on its own. Set the notice state Unserved with delivery_status REFUSED or UNDELIVERABLE, write one decision log entry with decision code D7.1 and rule R-LIT-09, write the ledger entry, and call CaseWorkflowApi.applyEvent with DELIVERY_FAILED so P3 transfers the case to its owner's queue with reason NOTICE_UNSERVED. No notice period timer starts. The owner sees MSG-P6-008 naming the notice type and the reason, which asks them to choose another service method. A failed decision log write leaves the notice as it was and is tried again on the next run, which AC9 tests.

### Step 8

**In the story.** JOB-10, at the start of each run: a Sent notice with no proof 7 days after its sent date becomes Unserved under R-LIT-08; the notice period does not start.

This step runs at the start of each JOB-10 run, before anything is written to a file. Build ProofWindowStep as the first step of the job. For each notice in state Sent, compare its sent date against the business date using the proof window of 7 days, held as a timer row rather than in code. At 7 days with no proof returned, set the notice Unserved with delivery_status PENDING and write the decision log entry with rule R-LIT-08; no notice period starts. Index ix_notice_state_sent supports that read. AC6 marks one notice Unserved at 7 days and leaves a second Sent at 6 days, so test both.

### Step 9

**In the story.** Litigation officer: reads the notice, its dispatch and its proof through GET /notices/{noticeId} and on SCR-18.

A person reads the result. Build GET /api/recovery/v1/notices/{noticeId} returning the Notice with id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus and sentType, with Litigation R and scope applied. A notice on a case outside the caller's scope answers 404 with MSG-P4-003 rather than telling the caller the notice exists, which AC11 tests with N-0200. SCR-18, built in RWB-E2-014, shows the Sent, Delivered and Unserved states this story sets, and SCR-04 Case timeline shows each ledger entry with its conduct check result.

## RWB-E2-022 SMS and LINE dispatch through NSS and LINE OA

Module: P6 Communications

### Step 1

**In the story.** Case owner: on SCR-03 Case record chooses Send message, the channel (SMS or LINE), the template and the party.

A person starts this. Build SendMessageDialog on SCR-03 for roles holding right C in the capability area Case record, with inputs for the channel SMS or LINE, the template, the language TH or EN defaulting to TH, and the party, which defaults to the borrower. The dialog posts to POST /cases/{caseId}/messages with an Idempotency-Key header. The channel and the template are both required: leaving either out is refused with 422 and MSG-GEN-001 naming the field, as AC12 shows for a missing channel. The dialog also shows the refusal message when a check stops the send.

### Step 2

**In the story.** System: checks the role (Case record C) and the scope; reads the current template for the channel and language through TemplateCatalog.

Automatic. MessageController checks right C in the capability area Case record and applies the caller's scope, so a role without it gets 403 with MSG-P4-002 and a case outside the scope gets 404 with MSG-P4-003. MessageService then asks TemplateCatalog for the current Approved template for that code, channel and language. Only a current Approved template may be used, so a withdrawn template with no later approved version is refused with 409 and MSG-P6-003 naming the template, which AC6 checks with SMS-REMIND TH version 1. Templates are data from RWB-E1-046 and belong in no list inside the code.

### Step 3

**In the story.** System: runs the conduct check: legal hold on the case, open deviation with contact stop, open deviation in the blocking list for the channel, and consent GIVEN on a verified contact point of that channel.

Automatic. Extend ConductCheckService from RWB-E2-021 with four tests that run before any message leaves the bank. It reads the legal hold flag of the case, asks DeviationApi.activeContactStops in S8 for open deviations with contact stop on, compares the open deviation codes against the reference list of codes that block the chosen channel, and calls PartyApi.contactPoints in P1 to confirm the party has a contact point of that channel that is verified and carries consent GIVEN. The blocking codes are reference data owned by the Conduct and QA officer, so the codes stay out of the code.

### Step 4

**In the story.** System: if the check fails, refuses, writes the decision log entry and a ledger entry with conduct check Blocked; stops.

Automatic. On a failed check nothing is sent. MessageService answers 409 with the message that fits the reason: MSG-P6-001 naming the deviation for a contact stop, MSG-P6-002 naming the channel when consent is missing, and MSG-P3-004 for a legal hold. It writes a decision log entry for the refusal and an interaction ledger entry with conduct check BLOCKED through InteractionLedgerApi.record, so the refusal is visible on the case. When the decision log store is down the refusal does not complete: the caller gets 503 with MSG-P7-003, nothing reaches NSS or LINE OA, and an incident is raised under R-UNI-39.

### Step 5

**In the story.** System: merges the template, writes the ledger entry with conduct check Passed and delivery status Sent, and writes the send request to the outbox in the same transaction.

Automatic. MessageService merges the case and party values into the template text, calls InteractionLedgerApi.record for an interaction with the channel, direction OUTBOUND, conduct check PASSED and delivery status Sent, and writes the send request to the outbox table of the ACE pattern. All three happen in one transaction, which means the database keeps them together or discards them all, so no message is queued without its ledger entry. The caller gets 202 with the interaction. Keep the phone number and LINE identifier as tokens in the request; the ACE notification path turns a token back into a real value.

### Step 6

**In the story.** JOB-11 Outbox sender: sends the request to the ACE notification path; NSS or LINE OA returns an accepted reference, which the system stores on the ledger entry.

Automatic. JOB-11 runs every minute and picks up queued sends, with no person involved. Write MessageOutboxSender as its handler for message sends, calling NotificationPort.send with the channel, the contact point token, the template reference, the language and the case reference. The acknowledgment carries the reference NSS or LINE OA gave the message, which you write to the ledger entry as external_ref, for example NSS-7781 in AC1. The interaction ID is the idempotency key, so the same send is never dispatched twice. When the notification path is unavailable the send stays queued and is retried up to the limit of 5, after which it goes to the exception queue under R-UNI-34 and the entry becomes FAILED.

### Step 7

**In the story.** ACE notification path: returns the delivery result (NSS result code; LINE delivered and read); the system updates the ledger entry to Delivered, Read or Failed.

The ACE notification path calls you here, so build MessageResultListener.onResult to take the external reference, the channel, the result and the time. Map the result to a delivery status through reference data: NSS result codes map to SENT, DELIVERED and FAILED, and LINE OA statuses map to DELIVERED and READ, both maps owned by the data steward. Then call InteractionLedgerApi.updateDelivery for that interaction. A LINE message reported delivered and then read ends at READ, which is what AC2 expects, and an NSS failure code ends at FAILED.

### Step 8

**In the story.** System: on Failed, adds one to the failed count of the contact point through the P1 interface.

Automatic. When a result maps to FAILED, call PartyApi.recordFailedContact in P1 with the contact point and the time, which raises that contact point's failed_count by one. AC8 has a contact point at failed count 0 before an NSS result of FAILED and at 1 after it. Make the call through the interface: contact_point belongs to P1, and this module writes none of its tables directly. The count is what later work uses to decide that a contact point is no longer reaching the customer.

### Step 9

**In the story.** Case owner: sees the message and its status on SCR-04 Case timeline.

A person does this. The case owner, and a team manager, Conduct and QA officer or complaint officer holding right R in the capability area Case record, opens SCR-04 Case timeline and sees each message with its channel, the template used, the conduct check result and the current delivery status. The screen reads GET /cases/{caseId}/interactions, which P3 already serves, so no new read endpoint is needed. A blocked contact appears in the same list with conduct check BLOCKED, which is how the Conduct and QA officer sees what was stopped and why.

## RWB-E2-023 Automated EFS file load

Module: P2 Integration

### Step 1

**In the story.** Scheduler: JOB-04 starts after JOB-02 for business date D.

Nothing here is manual. JOB-04 Daily reconciliation is already scheduled on Control-M from RWB-E1-051 and runs after JOB-02 for business date D; your work is EfsReconStep, a new step inside it. The step keys on the business date, and its idempotency key is the text INT-07 followed by that date, which is what makes a second run for the same day harmless. When JOB-02 did not run for D because the load was late, there is no reconciliation for that date at all; the day counts as not clean and MSG-P1-001 explains that today's load has not arrived.

### Step 2

**In the story.** SY-DATALOAD: the EfsReconService reads the count and the list of accounts EFS handed over at 90 days past due on D through the P1 EfsHandoverQuery.

EfsReconService reads one side of the comparison through a published interface. EfsHandoverQuery.handedOver in P1 recovery.data.api takes the business date and answers with the account IDs that EFS handed over at 90 days past due on that date; the count is the size of that list. Call the interface rather than reading loan_account or any other module's table yourself. For the first test day, 2026-12-14, that call answers with 104 accounts. The service identity running the step is SY-DATALOAD, so no user scope narrows the answer.

### Step 3

**In the story.** SY-DATALOAD: reads the cases created and the accounts linked by JOB-02 for D from the hand-over run summary.

The other side of the comparison comes from the hand-over run that JOB-02 already recorded. Call HandoverRun.summary in P2 recovery.integration.handover.api, built in RWB-E2-001, with the same business date; it answers with the cases created and the accounts linked for that date. For 2026-12-14 that is 98 cases created and 4 accounts linked, which is 102 accounts on cases. Read the summary rather than counting the cases again, so both sides describe the same run. An absent summary is the late-load case covered in step 1.

### Step 4

**In the story.** SY-DATALOAD: compares the two lists by account ID; each account on one side only is a difference with a reason (no case, held in the exception list, case without a hand-over).

The comparison is code. Match the two lists on account ID and keep every account that appears on one side only. Give each difference a reason: the account was handed over and has no case, the account was held in the data quality exception list, or a case carries the account with no hand-over on that date. The difference count divided by the number of accounts handed over gives the percent used in step 6, so 3 differences in 2,000 accounts is 0.15 percent and 1 in 2,000 is 0.05 percent. A day with no difference at all is a clean day.

### Step 5

**In the story.** SY-DATALOAD: writes each difference as a data quality exception with product DP05 and check "EFS hand-over reconciliation", and writes the day result (counts, difference percent, clean or not) to the run record.

Two writes, both automatic. Each difference goes in through DataQualityExceptions.add with product DP05, check EFS hand-over reconciliation, the account ID as the record key, the business date and the reason from step 4; a rerun adds only differences not already listed for that date, so the three listed for 2026-12-15 remain three. The day result goes onto the run record in interface_run.checks: the two counts, the difference percent, and whether the day was clean. CleanDayCounter reads those day results later, counting back from the last business date and breaking the run at a missing day.

### Step 6

**In the story.** SY-DATALOAD: when the difference is above the alert threshold, alerts the data steward and the platform administrator with MSG-P2-013.

The step sends the alert, not a person. Read the threshold from the parameter recon.efs.alert_pct, which is 0.1 percent, and compare the percent from step 4 with it. Above the threshold, alert both the data steward and the platform administrator with MSG-P2-013, which names the number of hand-overs with no case, the date and the percent, and points at the data quality exceptions; those alerts arrive by email. At or below the threshold, list the differences and send nothing, and still record the day as not clean when the difference is above zero. Send one alert per business date, even after a rerun.

### Step 7

**In the story.** Data steward: after ten clean days in a row, signs off the retirement of the manual EFS file handling.

A person decides this, once the days support it. The data steward calls POST /admin/interfaces/{interfaceCode}/manual-retirement, a new endpoint, with a note of up to 500 characters and the Reference data U right. The required run of clean days is the parameter recon.efs.clean_days_required, which is 10, and CleanDayCounter counts them back from the last business date. With 7 clean days the call answers 409 with MSG-P2-014, naming the count reached and the count needed, and the manual path keeps running. The platform administrator, who holds no Reference data U, is refused with MSG-P4-002.

### Step 8

**In the story.** System: checks the clean days, writes the sign-off record and switches flag `rwb.integration.efs-manual-upload` off for the environment.

The rest is code inside ManualRetirementService. Check the clean days again rather than trusting the caller, then write the sign-off row to interface_signoff with interface ID INT-07, the first and last dates of the clean run, the number of clean days, the user and the time. The migration V2026_12_23__p2_interface_signoff.sql creates that table with a unique constraint on interface_id, which is what makes a second sign-off impossible and answers 409 with MSG-P2-019. Then switch rwb.integration.efs-manual-upload off for the environment through FeatureFlagService, write the ACE audit entry, and answer with MSG-P2-015.

## RWB-E2-024 Field app photos and bills into the document hub

Module: P5 Document hub

### Step 1

**In the story.** Field collector: captures photos, bills and the checklist in the field app; the app records for each file the device time and GPS position, and a client file ID.

The field collector does this in the field app, and the app itself is out of scope for you. For each file it records the device time of the capture, the GPS position and a client file ID, which is the identifier the app gives that one file. Your side takes those values as sent: the device time is stored with its offset and the server never replaces it (BR2 and the guardrail in section 17). The collector can capture with no signal, so the capture time and the time the file reaches you can be a day apart (AC2). The kinds captured are photos, bills and the checklist.

### Step 2

**In the story.** Field app: when a signal is available, sends the captures for the case to POST /cases/{caseId}/field-captures with a manifest of the items.

The app sends the captures for one case to POST /cases/{caseId}/field-captures, the new endpoint you build as FieldCaptureController. The request is multipart form data: a JSON manifest holding inspectionRef and one item per file with clientFileId, kind of PHOTO, BILL or CHECKLIST, capturedAt with its offset, latitude, longitude and fileName, plus one file part per item named by its clientFileId. The app sends when a signal is available, which can be hours after the visit. The feature flag rwb.dochub.field-capture is off at first, and the endpoint then answers 404. The endpoint itself is recorded in the additions file.

### Step 3

**In the story.** System: checks the role, the right and the case scope, and that every manifest item has one file and every file has one manifest item.

Three checks run before any file is touched. The caller must hold Documents right C, so a phone collector with read only is refused with 403 and MSG-P4-002 (TC-E2-024-16). The case must be in the caller scope, which you read through CaseDirectory.findById in P3; a case where the collector has no task gives 404 with MSG-P4-003 and nothing is stored (AC12). The manifest and the file parts must match one to one, and a mismatch gives 422 with MSG-GEN-001 naming the client file ID with no file, again storing nothing (AC14). More files than CAPTURE_MAX_FILES, set to 50, gives 413 with MSG-GEN-002 and stores nothing (AC15).

### Step 4

**In the story.** System: for each item, checks the client file ID against items already received for the case; a repeat returns the earlier result.

The duplicate check comes next, per item. FieldCaptureService looks up the client file ID among the items already received for that case, and a repeat returns the result of the first attempt with status DUPLICATE and the documentId written then, storing nothing new. The partial unique index ux_document_client_file on case_id and client_file_id, which applies only to rows where client_file_id is filled, backs this up in the database. This makes the endpoint idempotent per item, meaning the app can resend a whole sync after the connection dropped: six items return DUPLICATE and the four that never arrived are accepted (AC5).

### Step 5

**In the story.** System: checks file type, size, capture time and position, writes the file to the intake container, and calls MalwareScanService.scanNow.

For an item that is new the service checks the file and the times, then stores and scans it. The file type must be in INTAKE_ALLOWED_TYPES, so a HEIC photo is refused with MSG-P5-001 while the other items of the same sync go on (AC10), and the size limit is INTAKE_MAX_FILE_MB of 25 with MSG-P5-017. A capture time later than the receipt time plus CAPTURE_CLOCK_SKEW_MINUTES of 5 is refused with MSG-GEN-002, and one before the case entry date or older than CAPTURE_MAX_AGE_DAYS of 30 with MSG-GEN-003. The file is written to the intake container and MalwareScanService.scanNow is called; a threat gives status QUARANTINED, MSG-P5-016, an incident and no document (AC11).

### Step 6

**In the story.** System: calls DocumentStore.store with the case, the type from the item kind (photo, bill, checklist), source UPLOAD, the file and its hash; the store writes the document, the DOCATT decision log entry and DocumentStored (EV-16).

Storage goes through the existing document hub. Call DocumentStore.store from RWB-E1-024 with a StoreRequest holding the case, the document type, source UPLOAD, the file and its hash. The type comes from the item kind with no classification step: PHOTO to INSPECTION_PHOTO, BILL to UTILITY_BILL and CHECKLIST to INSPECTION_CHECKLIST (BR5), and the case is the one in the path, so no case matching runs (BR6). The store writes the document row, the DOCATT decision log entry and the DocumentStored event. When the decision log write fails, that item is refused with MSG-P7-003 and nothing is stored for it (TC-E2-024-17).

### Step 7

**In the story.** System: in the same transaction sets on the document captured_at, capture_latitude, capture_longitude, client_file_id and capture_kind.

Five columns on document are new in this story and you set them in the same transaction as the store call, so a document never exists without its capture detail. They are captured_at, capture_latitude and capture_longitude as numeric with six decimals, client_file_id and capture_kind, added by migration V2_5_024__field_capture.sql and written through DocumentHubRepository. A transaction means these writes and the store writes are kept together or dropped together. An item with no GPS position is still stored, with latitude and longitude left empty, and the response carries the warning MSG-P5-015 with the count of such files (AC6).

### Step 8

**In the story.** System: DocumentStoredListener (RWB-E1-049) creates the intake item for OCR; for a UTILITY_BILL, extractStep (RWB-E1-053) writes bill_amount and due_date on the document.

Two components you already have carry the item on, with no further call from your service. DocumentStoredListener from RWB-E1-049 reacts to the DocumentStored event and creates the OCR intake item; your check in build step 4 is that the item carries the type you gave, so classifyStep skips it. For a UTILITY_BILL, extractStep from RWB-E1-053 reads the UTILITY_BILL field list and writes bill_amount and due_date on the document, turning the Thai date 28/12/2569 into 2026-12-28 (AC3). A field read below the confidence threshold of 0.80 goes to state REVIEW, the document joins the review queue on SCR-31, and MSG-P5-003 shows on it (AC13).

### Step 9

**In the story.** System: returns a result per item (accepted, duplicate, refused with the message).

The endpoint answers 201 with FieldCaptureResult, which holds one entry per item: the clientFileId, a status of ACCEPTED, DUPLICATE, REFUSED or QUARANTINED, the documentId when one was written, and a messageCode. Item level refusals leave the rest of the request working, so a sync of ten items can return nine accepted and one refused. Only the request level failures of step 3 refuse everything. The warning MSG-P5-015 is returned when any accepted item arrived with no position. The field app shows these per item results to the collector, who can then capture a refused photo again.

### Step 10

**In the story.** Case owner: sees the inspection photos, bills and the bill fields on SCR-30 Case documents with capture time and position.

The case owner reads the result on SCR-30 Case documents. You build the React component CaptureDetails for that screen, showing the capture time, the position and a map link for each capture, the bill fields with their confidence, and MSG-P5-015 on captures that have no position. A GPS position and a photo of a home are personal data, so the position is masked for roles without the right to see it (BR9), and positions, file names and bill values are kept out of the logs. The phone collector holds Documents R and reads only. The restructuring officer reads the captures on deed in lieu cases.

## RWB-E2-025 Extraction for the stage 2 and 3 document types

Module: P5 Document hub

### Step 1

**In the story.** Reference data administrator: loads DOCTYPE-2026.12 with valid from 2026-12-31 after approval.

A person does this, and two more approve it. The reference data administrator loads the document type table version DOCTYPE-2026.12 through the RWB-E1-025 loader with valid from 2026-12-31, after legal counsel and the Head of NPA have signed the type and field list. You write no loader code. Your work is the load file: the five new types with their classify_threshold and their field definitions, each field carrying its data type, its extraction method, its review_only flag and an optional pattern. Prepare it with a test case per new row and validate it in SIT first. The document_hub_parameter row EXTRACT_ACCURACY_PASS, 0.90, is loaded the same way.

### Step 2

**In the story.** JOB-12 Document intake: an inbound contract, credit approval, mortgage document, court filing, hearing notice or judgment passes scanStep and ocrStep (RWB-E1-041, RWB-E1-049).

Automatic, and already built. JOB-12 Document intake runs its steps in order, and the first two, scanStep and ocrStep from RWB-E1-041 and RWB-E1-049, need no change for these documents. OCR turns the scanned page into text that later steps can read, which matters here because these documents arrive on paper and much of their text is Thai. Nothing in this story touches the file itself. A write-once document, one whose stored file may never be altered, keeps its hash, its storage_ref and its write_once flag through everything that follows.

### Step 3

**In the story.** ClassifyStep (RWB-E1-050): the classifier version for the eleven types returns a type and a confidence; below the classify_threshold of the type the item goes to the review queue with reason LOW_CONFIDENCE.

Automatic, in the classifyStep of RWB-E1-050, whose code does not change. What changes is the classifier version it uses: one trained on the 60-document labeled sample to tell eleven types apart, the six from Epic 1 plus the five new ones, selected through the agent runtime in P10. For each document it writes predicted_type and classification_confidence on document_intake. Confidence is a number between 0 and 1 saying how sure the classifier is. Below the classify_threshold held on the type's own row, the item goes to the review queue with review_reason LOW_CONFIDENCE. The evaluation run has to show at least 45 of the 50 new-type samples classified correctly.

### Step 4

**In the story.** ExtractStep (RWB-E1-053): reads the field definitions of the type from DocumentTypeCatalog for the version in force and calls the extractor named by extraction_method.

Automatic, and the point of the story is that no Java changes here either. ExtractStep reads the field definitions for the predicted type from DocumentTypeCatalog, taking the table version in force on the extraction date, then calls the extractor named in each field's extraction_method, either TemplateFieldExtractor or ModelFieldExtractor. Both are configured from the type table alone, so a new type is rows and not a class. For JUDGMENT the definitions name court_name, red_case_no, judgment_date and judgment_amount. A document received before 2026-12-31 is read against DOCTYPE-2026.11 and its six types, which is why the judgment in AC6 ends in the review queue with review_reason UNKNOWN_TYPE.

### Step 5

**In the story.** System: normalizes each value, checks it against the field pattern held in the type table, and writes document_field rows with confidence and state.

Automatic. ValueNormalizer from RWB-E1-053 turns each extracted value into its stored form: "2,400,000.00 บาท" becomes "2400000.00", and a Buddhist Era date becomes an ISO date, so "5 มีนาคม 2570" is stored as 2027-03-05. The normalized value is then matched against the pattern on the field's own row in field_definitions, a text rule the value has to fit, for example two to four letters, a space, digits, a slash and four digits for red_case_no. One document_field row is written per field, with the extracted value, the extractor version, the confidence and the state. The patterns are data, so write none of them into code.

### Step 6

**In the story.** System: a field below the threshold, failing its pattern or marked review-only gets state REVIEW and the document goes to the review queue.

Automatic, and three separate conditions lead to the same place. A confidence below the field threshold of 0.80, a value that does not fit its pattern, and a field whose review_only flag is true each set the field state to REVIEW and send the document to the review queue of RWB-E1-054 with that field marked. So "Por345-2570" at confidence 0.9200 goes to review on its pattern, while "Por 345/2570" at the same confidence is OK. SCR-30 shows MSG-P5-003 on the document. The review_only flag is how a field whose accuracy on the sample fell below the 0.90 pass mark is held back, and it takes effect only when the new table version is loaded.

### Step 7

**In the story.** MatchStep (RWB-E1-032): stores the document with its fields through DocumentStore; DocumentFieldsExtracted (EV-17) is written for documents already attached.

Automatic, in the matchStep of RWB-E1-032. The document and its fields are written through DocumentStore, never by this story's code reaching into another module's tables. For a document already attached to a case, the event DocumentFieldsExtracted, EV-17, is written so that the modules waiting on those values learn they exist. The idempotency key is the document ID, the doc_version and the table version, so the same document extracted again under the same version produces no second set of rows. A write-once document gains its document_field rows and keeps its file, its hash and its storage_ref, which AC10 checks with four rows on a judgment.

### Step 8

**In the story.** Litigation officer: sees the fields on SCR-30, and checks the marked ones on SCR-31.

A person reads and corrects here. SCR-30 Case documents lists the new types with their fields and confidences, and shows MSG-P5-003 on any document holding a field in REVIEW. SCR-31 Document review queue, built in RWB-E1-054, is where the officer checks a marked field and either confirms the extracted value or corrects it, which moves the field state to CONFIRMED or CORRECTED. Both screens are existing work, and this story only brings the new types and fields into them. Party names and other personal values are masked unless the officer's role may see them, and a document of another team answers 404 with MSG-P4-003.

### Step 9

**In the story.** S4 and S2 modules: read confirmed field values through DocumentFieldReader to fill the pack and the treatment record (from Epic 3 and Epic 5).

Automatic, and this is the one new interface you build. DocumentFieldReader.checkedFields(caseId, documentType) in recovery.dochub.extract answers a list of CheckedField holding the document ID, the doc version, the field name, the value, the state and the confidence. Return only fields in state OK, CONFIRMED or CORRECTED; a field still in REVIEW is held back until a person has dealt with it. The caller passes its own service identity, and values come back unmasked only to a module whose purpose needs them, SY-CASEWF or SY-AGENT, and are never logged. Add the index ix_document_type_case on document (case_id, document_type) for this query, and write a contract test from the S4 side.

## RWB-E2-026 Document generation engine for contract, CA and mortgage templates

Module: P5 Document hub

### Step 1

**In the story.** Restructuring officer or SY-CASEWF: requests generation for a case, a treatment and a list of template codes.

Either a person or another module starts this. The person is a restructuring officer or case owner holding Documents C, who reaches the engine through the screens of RWB-E2-017; the module is SY-CASEWF for rule-driven generation from Epic 3. Build both doors: the endpoint POST /cases/{caseId}/generated-documents and the published interface DocumentGenerator.generate. The request carries the treatment id, one to ten template codes and the language, TH or EN with TH as the default, and an Idempotency-Key header is required. An empty templateCodes list is refused with 422 and MSG-GEN-001. The whole engine sits behind the feature flag rwb.dochub.generation-engine, which when off makes the endpoint return 404.

### Step 2

**In the story.** System: reads the treatment through TreatmentReader and checks it is approved and open.

DocumentGenerationService does this first. Call TreatmentReader.find from S2 and never read the treatment table yourself. The treatment passes only when its type is DEED_IN_LIEU or RESTRUCTURE, its decision_log_id is set, which is what shows it was approved at D6.4, and its outcome is still empty. Anything else is refused with 409 and MSG-P5-011 and nothing is stored, which is exception path X4 and AC6. Check the case scope at the same time: a case outside the caller's scope returns 404 with MSG-P4-003, as AC12 shows for a case of team HP-NE requested by an officer of team FCR-BKK.

### Step 3

**In the story.** System: for each template code, reads the current version from the template catalog for the language and product group: approved by Legal, active, highest version valid on the request date.

TemplateSelector does this through the P6 interface TemplateCatalog.current(templateCode, language, productGroup, asOf). For each code it takes the version that is approved by Legal, active and the highest one valid on the request date, and a template for that exact product group wins over a template for all products, per BR1. A current version with approved_by_legal false is refused with 422 and MSG-P5-010 naming the template and version, which is AC4. A withdrawn template with no approved successor is refused with 422 and MSG-P6-003, and a task goes to the officer who asked, which is AC5. No template for the product group or language is MSG-P5-010 as well.

### Step 4

**In the story.** System: reads the merge field list of that version and asks each owning module's MergeFieldProvider for the values.

MergeFieldResolver does this automatically. A merge field is a named placeholder in the template body, written as {{merge_field_code}}, that is replaced by a value from the case. Read the list for the chosen version with TemplateCatalog.mergeFields(templateId), group the codes by the module that owns them, and call MergeFieldProvider.resolve(caseId, treatmentId, mergeFieldCodes) on each provider listed in your configuration: P3 for the case, S2 for the treatment and P1 for party and collateral. The background of section 7 gives the fields of DIL-CONTRACT version 2 as case_no, borrower_name, title_doc_no, transfer_price and contract_date. A national ID number is filled from the token service at render time only.

### Step 5

**In the story.** System: checks that every required merge field has a value; formats each value by its catalog format (Thai long date in Buddhist Era, amount with two decimals, amount in Thai words).

The same resolver checks completeness and ValueFormatter does the formatting. A required field with no value stops the whole request with 422 and MSG-P5-009 naming the template and the field, and nothing is stored, which is AC2 for a case with no title_doc_no. Formatting follows the format the merge field catalog holds for each field: a Thai long date in the Buddhist Era, an amount with two decimals, and an amount written out in Thai words. AC1 sets the expected output exactly, with "1,250,000.00 บาท (หนึ่งล้านสองแสนห้าหมื่นบาทถ้วน)" and the date 2026-12-10 shown as "10 ธันวาคม 2569". Unit test both conversions.

### Step 6

**In the story.** System: renders each template body to PDF/A-2b with the Thai fonts embedded, and stores each file and the merge snapshot in the draft area of the standard container.

TemplateRenderer does the rendering with no person involved. PDF/A-2b is a PDF profile made for long-term keeping, which requires every font used to be carried inside the file, so embed the Thai font named by the parameter GEN_FONT. Replace each {{merge_field_code}} tag in the body with its formatted value. Write each rendered file and the merge snapshot, the record of the values used, into the draft area of the standard container through BlobStorageAdapter from RWB-E1-024. Do not use DocumentStore.store here, which would place a legal type in the write-once container at once. A body that cannot be rendered returns 503 with MSG-GEN-006, stores nothing and raises an incident.

### Step 7

**In the story.** System: writes one decision log entry with decision code D6.4, the inputs reference (merge snapshot), and per document the template code and version.

Your service writes one entry for the whole request through DecisionLogWriter.write, and that entry holds the decision code, an inputs reference pointing at the merge snapshot, and the template code and version of each document produced. AC13 checks that one entry names the three template codes and versions for a three-template request. A failed write stops everything: return 503 with MSG-P7-003, remove the draft files from the container, write no document row and raise an incident as R-UNI-39 requires. That is exception path X5, AC7 and the resilience test TC-E2-026-16, which forces the failure during a three-document set.

### Step 8

**In the story.** System: in the same transaction writes one document row per file with source GENERATED, state DRAFT, template code, template version and treatment ID, and one DocumentStored event (EV-16) per document.

These writes sit in the same transaction as the decision log entry, so the documents and the entry are kept together or not at all. Write one document row per file with source GENERATED, state DRAFT, write_once false, the document type the mapping gives for that template code, and the template and treatment values. The Flyway migration in this story adds the three columns those values need, with the partial unique index ux_document_draft_per_template on document (treatment_id, template_code) where the state is DRAFT, which is what makes the second of two requests at the same moment fail with 409 and MSG-GEN-004. Write one DocumentStored (EV-16) per document to the outbox.

### Step 9

**In the story.** System: returns the generated documents; the screens of RWB-E2-017 show them for review.

The response is 201 with a DocumentPage of the generated documents, and the interface returns GenerationResult with the decision log entry id and, for each document, the document id, template code, template version and document type. A repeated request with the same Idempotency-Key returns that first result and writes nothing further, which is AC8, so hold the key and its result in IdempotencyRepository for the 24 hours the parameter GEN_IDEMPOTENCY_HOURS sets. The documents stay DRAFT until they are sent. No screen belongs to this story: review and send are RWB-E2-017, and the documents also show on SCR-30 Case documents in its list state.

## RWB-E2-027 Payment matching rules with the data team

Module: P8 Payments and posting

### Step 1

**In the story.** Reference data administrator: loads a parameter version through POST /admin/reference-loads with table "payment_match_rule" and a valid from date.

A person does this: the reference data administrator, holding Reference data right C. They post the file to /api/recovery/v1/admin/reference-loads as multipart form data with the file, the table name payment_match_rule and a valid from date. P4 owns the endpoint. Your work is PaymentMatchRuleLoadHandler, a ReferenceLoadHandler for that table, with its validate and apply methods. A version is a set of rows sharing a rule_version such as PM-2026.12, each row holding a rule code, a priority, a match type, an amount tolerance, window days before and after, and a partial floor. The endpoint takes the SHA-256 hash of the file per table, so a file already loaded is refused with 409 and MSG-P1-002.

### Step 2

**In the story.** System: checks each row: match type in the list, tolerance between 0 and 100, window days 0 or more, unique priority within the version, approver present; any failure refuses the whole load.

The handler checks the file with no person involved. For each row: match_type is one of EXACT, WINDOW and PARTIAL; amount_tolerance_pct is between 0 and 100; window_days_before and window_days_after are 0 or more; priority is unique within the rule_version; approved_by is filled, since Credit Administration owns the list and approves the version the administrator loaded. Any failed row refuses the whole load with 422, using MSG-GEN-002 for a value outside its range or a repeated priority and MSG-GEN-001 for an empty value, and the version in force stays in force. Migration V2_027__match_rule_partial.sql adds partial_floor_pct as numeric(5,2), the check constraint on the tolerance, and a unique key on rule_version and priority.

### Step 3

**In the story.** JOB-07: for the business date, reads the parameter version in force on that date.

JOB-07 does this at the start of its run, with no person involved. The job already exists from RWB-E2-008. For the business date it is matching, read the rule rows whose valid_from is on or before that date and whose valid_to is empty or later, and use that one version for the whole run. This is what lets Credit Administration change a window or a floor without a release: a run on 2027-01-05 under version PM-2027.01 allows 5 window days after the due date, while a match already decided under PM-2026.12 keeps that version on its decision entry and is never recomputed.

### Step 4

**In the story.** System: for each payment, tries the rows in priority order (EXACT, then WINDOW, then PARTIAL) against each running plan on the case; the first row that matches decides.

The job does this per payment, with no person involved. Build MatchRuleEvaluator to take the rows of the version in force, sort them by priority and try each one against every running plan on the case, stopping at the first row that matches. Build one evaluator per match type behind it: ExactMatch for an amount inside the tolerance with a payment date inside the window before the due date, WindowMatch for the same with the window extended after the due date, and PartialMatch for an amount at or above the partial floor and below the installment. When two rows would both match, the lower priority number decides, so a payment of the exact installment amount is matched by EXACT even though WINDOW also fits.

### Step 5

**In the story.** System: writes the D5 decision log entry with rule R-RES-26, rule version equal to the parameter version, the row code and the inputs; then writes the proceeds row and calls TreatmentApi.

The job does this, and the order of the two writes matters. Build MatchDecisionWriter to assemble a D5 DecisionLogRequest holding rule R-RES-26, the rule version equal to the parameter version in force, the row code that matched and the inputs, which are the payment code, the amount, the dates and the row code only, never personal data. Call DecisionLogApi.write on P7 first, then write the proceeds row and call TreatmentApi. A DecisionLogWriteException means no proceeds row is written for that payment: the run summary shows MSG-P7-003 for it, an incident is raised under R-UNI-39, and the next run of JOB-07 for that business date matches the payment again.

### Step 6

**In the story.** System: for a PARTIAL match, passes the shortfall to TreatmentApi, which holds it on the plan.

The job does this when the matching row is PARTIAL, with no person involved. Call TreatmentApi.recordInstallmentPaid on P3 with the treatment ID, the proceeds ID, the due date, the amount paid and the shortfall, which is the installment amount less the amount paid. P3 writes it to treatment.installment_shortfall and holds it on the plan, so the plan shows what is still owed for that due date. A payment of 11,875.00 against an installment of 12,500.00 is 95 percent, above the partial floor of 90 percent, and leaves a shortfall of 625.00 THB on due date 2026-12-15. You build the call and the amounts; holding the shortfall belongs to the treatment interface.

### Step 7

**In the story.** System: a payment no row matches is written UNMATCHED with a D5 entry under R-UNI-03 and appears on the exception list.

The job does this when no row matched, with no person involved. Write the proceeds row with matched_to set to UNMATCHED and write a D5 decision entry under rule R-UNI-03, so even a payment that matched nothing carries a record of why. These are the receipts a person works through: a payment 4 days after the due date where the window allows 3, a payment at 80 percent of the installment against a floor of 90, and a payment above the installment by more than the tolerance. The run summary carries MSG-P8-001 with the count of unmatched payments for the business date, and they come back from GET /proceeds with matched false.

### Step 8

**In the story.** Credit Administration officer: reads matched and unmatched receipts on SCR-28, with the row that matched each one.

A person does this: the Credit Administration officer, or another role holding Write-off and posting right R. They open SCR-28 Proceeds matching, which has the states Loading, matched and unmatched. For each matched receipt the screen shows the row code and the rule version that decided it, and for each unmatched receipt the reason. The data comes from two reads: GET /api/recovery/v1/proceeds for the receipts, and GET /api/recovery/v1/decision-log for the entry behind each one, which is where the row code and the version are held. Until SCR-40 Reference data is built, the administrator reads the result of a parameter load on the reference load record.

## RWB-E2-031 Agent monitoring dashboard v2 [E3d]

Module: P10 Agent runtime

### Step 1

**In the story.** RW-COE: opens SCR-46 Agent monitor from the Administration menu.

A person does this. The center of excellence analyst opens SCR-46 Agent monitor, which you build as the React component AgentMonitorPage in src/modules/recovery/agent/monitor, with filters for agent, segment and date range and a badge per agent and segment reading Shadow, live or paused. Build the common states as well: skeleton rows while loading, a sentence for a period with no runs, and an error message at the top. The menu entry shows only for a session holding Platform administration R. Put the page behind feature flag rwb.agent.monitor-v2; with the flag off SCR-46 shows runs and fallbacks only and the drift step is skipped.

### Step 2

**In the story.** System: checks Platform administration R, then calls GET /admin/agent-metrics for the last 30 days.

This happens on its own when the page loads. The access check refuses a session without right R in Platform administration with 403 and MSG-P4-002, as for RW-CASEOWN. Build the new endpoint GET /admin/agent-metrics with query parameters agent, segment such as MORTGAGE/BKK, from, to and version, and put its filter checks in AgentMetricsController: a from date later than the to date is 422 with MSG-GEN-003, and a range longer than 92 days is 422 with MSG-GEN-002 naming 1 and 92 days. The page asks for the last 30 days on first load. The endpoint is read only and applies the caller's scope.

### Step 3

**In the story.** System: returns one row per agent, policy version, prompt version, model version, segment and day: runs, fallback rate, acceptance rate, correction rate, override rate, median and 95th percentile latency, tokens and cost.

This happens on its own in AgentMetricsService. Build one AgentMetric row per agent, policy version, prompt version, model version, segment and date from three sources: the daily rows in agent_run_daily written by JOB-15, the agent_feedback verdicts, and the override counts from DecisionLogQuery.byAgentVersion on P7. Acceptance rate is accepted divided by accepted plus corrected plus rejected, so 119 accepted of 140 feedback entries gives 0.8500, and correction rate uses the same total. Override rate is the decisions on that agent version whose final_call differs from the recommendation, over all decisions on that version. Report latency as latencyP50Ms and latencyP95Ms. A segment is the case product group and region at run time, held on agent_run in the new columns segment_product_group and segment_region_code from migration V10_007__agent_run_segment.sql.

### Step 4

**In the story.** RW-COE: filters by agent, segment and date range; the screen shows the state of each agent: Shadow, live (L1) or paused (mode OFF).

The analyst drives this, and the screen calls the same endpoint again with the new filter values. The state badge comes from the autonomy mode of the agent policy for that segment, so one agent can be live on one segment and in shadow everywhere else, as SCREENING is for MORTGAGE and BKK. Shadow shows runs, fallbacks and evaluation scores and no acceptance, because nobody has given a verdict yet; live shows every measure; paused shows history only. A segment with fewer than 20 feedback entries in a week shows not enough feedback. From any row the analyst opens the runs behind it through GET /admin/agent-runs.

### Step 5

**In the story.** JOB-15 Reporting extract: after the daily rows, runs the drift check for each L1 agent and segment: acceptance of the last 7 days against the 7 days before.

This runs on its own on a timetable, with nobody watching. Add the step agentDrift to the nightly JOB-15 Reporting extract at 01:30, after the step agentRunDaily, and build it as DriftCheckStep. For each L1 agent and segment it reads the agent_feedback rows of the last 14 days and works out the acceptance rate of the last 7 days and of the 7 days before. The window of 7 days, the fall of 10 points and the minimum of 20 feedback entries per week all come from watch_measures on the agent policy, loaded by RW-COE and approved by RW-RISK, so none of the three sits in code. A segment under the minimum in either week is skipped.

### Step 6

**In the story.** System: on a fall of 10 points or more, writes one DRIFT alert and sends MSG-P10-006 to the policy alert role and RW-RISK.

This happens on its own inside the same job step. When the later week's acceptance is at least 10 points below the earlier week's, insert one agent_alert row of type DRIFT holding the agent, the segment, the business date, measured_value, threshold_value, sent_to_role and sent_at; for 0.8600 falling to 0.7500 the measured value is 0.7500 and the threshold 0.7600. Send MSG-P10-006 through the P6 notification interface to the role named in agent_policy.alert_role and to RW-RISK. The unique key of agent_code, alert_type, segment and business_date means a rerun of JOB-15 for the same date writes no second row and sends nothing again.

### Step 7

**In the story.** RW-COE: opens the override reasons for an agent and month and sees the count per coded reason.

A person does this on the screen. Build OverrideReasonPanel to show, for one agent and one month, the count of decisions per coded override reason, taken from decision_log_entry.override_reason through the P7 query interface. An override is a decision where the person's final_call differs from the agent's recommendation, and REQ-APD-005 requires a coded reason on each one and a monthly report of them. Show counts only: no prompt text and no agent output content belongs on this screen. The same monthly view carries the token and cost reconciliation, showing not reconciled with the token difference when the daily rows and the run sums disagree.

## RWB-E2-032 TDR offer-suggestion model through the model gateway [E3e]

Module: P10 Agent runtime

### Step 1

**In the story.** Restructuring officer: opens a restructure treatment on case "RW-2026-001001" on SCR-14 Treatment record.

A person starts this. The restructuring officer opens the treatment record screen SCR-14 for a restructure treatment created by RWB-E2-004, in its draft state. Your work on the screen is TreatmentSuggestionPanel, a new area in the draft state that shows either the suggestion with its model code and version, or MSG-P10-007 when no suggestion is available. The officer goes on editing the offer fields as before; the suggestion is never copied into them and never changes the treatment status. The feature flag rwb.agent.tdr-suggestion controls the whole path and, when off, makes suggestOffer answer empty with no call.

### Step 2

**In the story.** P3 treatment service: calls ModelSuggestionClient.suggestOffer with the case ID and treatment ID.

The treatment service makes this call when the screen opens, with no separate action by the officer. Build the published interface ModelSuggestionClient in recovery.agent.api with one method, suggestOffer, which returns an optional suggestion and can throw DecisionNotRecordedException. An empty answer is a normal outcome and means the screen shows MSG-P10-007. The call runs as SY-CASEWF. The treatment type is checked before any model work: a treatment of type SETTLEMENT gets no model call and no suggestion, because the model is called only for type RESTRUCTURE.

### Step 3

**In the story.** System: reads the TDR_OFFER policy in force; if the mode is OFF, returns no suggestion and makes no call.

TdrSuggestionService does this first, automatically. Read the policy row TDR_OFFER that is in force and look at autonomy_mode. Mode OFF means the model is not in service: answer empty at once, make no gateway call and write no decision log entry. That is the state the story ships in, because policy version P1 has mode OFF with review date 2027-02-28 until the TDR team deploys the model. When they do, RW-COE loads a new version with mode L1, the model code and version, the output schema and the 60 second timeout, and RW-RISK approves it. GET /admin/agent-configs shows which version, mode and review date are in force.

### Step 4

**In the story.** System: reads the account balance, arrears and the last 12 months of payments through the P3 interface and masks personal fields.

TdrInputAssembler gathers the inputs in code. Read principal outstanding, total balance, days past due and the interest rate for the account, and the payment dates and amounts of the last twelve months, all through the P3 interface; those tables belong to another module and are not queried here. Mask the personal fields, the account number among them, before anything leaves the service, so the model request carries no identifying customer data. Hold the masked set as a snapshot, because the decision log entry written later points to it as the inputs reference.

### Step 5

**In the story.** System: calls the model through ModelGatewayClient with the policy timeout, and checks the answer against "tdr-offer-v1".

The service makes the call through ModelGatewayClient from RWB-E1-058, which is the only route to the model and uses the private endpoint of integration INT-23. Use the timeout from the policy row, 60 seconds. Then check the answer against the output schema tdr-offer-v1, which allows installments from 1 to 360, a monthly amount above zero, an interest rate from 0 to 30 and a confidence. A timeout writes the agent run with status TIMED_OUT and fallback true; an answer that fails the schema writes GUARDRAIL_FAILED with check SCHEMA. In both cases no suggestion is returned, the screen shows MSG-P10-007, and the officer carries on with the treatment.

### Step 6

**In the story.** System: writes one decision log entry (decision D5, model version, suggestion, final call SUGGESTION_RECORDED) and one agent run row.

The service writes both records before it answers. The decision log entry goes through the P7 DecisionLogWriter with decision code D5, the model version, the inputs reference, the suggested terms as the recommendation, final call SUGGESTION_RECORDED, and the treatment ID and agent run ID in its actions. The agent run row holds the status, the model version, the latency, the guardrail result, the output and the decision log entry ID. When the decision log write fails, return no suggestion, throw DecisionNotRecordedException so the treatment service can show MSG-P7-003, keep the run row without a decision link and raise an incident.

### Step 7

**In the story.** System: returns the suggestion and the decision log entry ID to the treatment service.

The service answers the call it received in step 2, returning an OfferSuggestion with the agent run ID, the decision log entry ID, the model code and version, the installments, the monthly amount, the interest rate and the confidence. A suggestion is returned only after its decision log entry has been written. The answer is idempotent under the key TDR_OFFER plus the treatment ID, which means a second request for the same treatment returns the first suggestion and the same decision log entry ID and makes no second model call. Publish EV-28 AgentRunCompleted for the run.

### Step 8

**In the story.** Restructuring officer: sees the suggestion on SCR-14 with the model code and version, and builds the offer.

A person reads the panel and decides. TreatmentSuggestionPanel shows the suggested terms together with a line naming the agent and the model version, as AC3 shows with Suggested by TDR_OFFER, version TDR-OFFER-1.0. The officer types the offer fields and submits the offer, because the suggestion is advice and nothing applies it. Roles with Treatment and offer R, among them RW-RESTRUCT and RW-CASEOWN, may read it. Reading the agent runs through GET /admin/agent-runs needs Platform administration R, so RW-RESTRUCT is refused there with MSG-P4-002.

## RWB-E2-033 Case and queue list with status, owner and ageing

Module: P2 Integration

### Step 1

**In the story.** Team manager: opens the case list (SCR-02).

A person does this. The team manager, holding RW-TEAMMGR with Team scope, opens SCR-02 Case list. You change CaseListPage, the React component behind that screen, instead of building a new one: add the columns age in state, service level state, service level due, prescription date, prescription clock and deviation, add the breach filter, and mark a breached row with the text Breached so that the mark does not rest on color alone. A paused stage clock shows Paused. Build the Loading, Empty, List and Filtered states. While the flag rwb.casewf.case-list-ageing is off, the screen keeps the columns of RWB-E2-011 and RWB-E1-031.

### Step 2

**In the story.** Front end: calls GET /api/recovery/v1/cases with the filters chosen, including breached when set.

The screen does this with no further action from the manager. It calls GET /api/recovery/v1/cases with the filters the manager chose: product, stage, status, owner, queue, page, size, sort, and the new parameter breached, set to true or false. No new endpoint is added in this story. Add breached and the response field prescriptionClockStatus to the API specification, record the change in the additions file, and regenerate the types through RWB-TE-003 so that the front end and the service agree on the shape. Each item of the CasePage already carries ageDays, serviceLevelDueAt and serviceLevelState from RWB-E2-011.

### Step 3

**In the story.** CaseAndWorkflowController: checks Case record R through the common module access check and applies the caller's scope (CTL-09).

The Workbench does this in CaseAndWorkflowController, before any case is read. The common module access check tests the right R in the capability area Case record and refuses a caller without it with 403 and MSG-P4-002, which test TC-E2-033-12 shows for the reference data administrator. The caller's scope then limits every row to Own, Team or All, taken from the default scope of their roles, so the manager of MTG-BKK sees the cases of that team's queues and no others. A case outside the scope appears on no page and under no filter, and the number of rows left out is never shown.

### Step 4

**In the story.** CaseAndWorkflowController: validates each filter value against its list of values and the page size against 1 to 200.

The controller does this next, again before any case is read. Check each filter value against its list of values: the product against LOV-PRODUCT, the status against LOV-CASE-STATUS, the stage against LOV-STAGE, and the queue against the queue codes in force, all read through the P4 reference data interface. A value outside its list is refused with 422 and MSG-GEN-007, which names the value and the field, so a request with product CAR reads nothing. Check the page size against 1 to 200 and refuse a size outside that range with 422 and MSG-GEN-002, which carries the minimum and the maximum.

### Step 5

**In the story.** CaseListQueryService (RWB-E2-011): reads the cases in scope with their queue, owner and SERVICE_LEVEL timer, and computes ageDays and serviceLevelState.

The Workbench does this in CaseListQueryService, which RWB-E2-011 built and which you extend. It reads the cases in scope with their queue and owner and the SERVICE_LEVEL timer row of each, and computes ageDays and serviceLevelState. Age in state is the whole number of calendar days from stage_clock_start to today in Asia/Bangkok, or from entry_date where stage_clock_start is empty. A case is breached when its SERVICE_LEVEL timer has status EXPIRED, or has status RUNNING with expires_at earlier than now; a paused timer is never breached, and a case with no timer gets serviceLevelState NONE. Hold these as pure functions in AgeingCalculator and unit test them without a database.

### Step 6

**In the story.** PrescriptionClockReader (this story): adds prescriptionClockStatus from the PRESCRIPTION timer and applies the breached filter (BR3, BR4).

This is the new code of the story, and the Workbench runs it with no person involved. PrescriptionClockReader reads the PRESCRIPTION timer of each case and sets prescriptionClockStatus to RUNNING or EXPIRED from timer.status, or NONE where the case has no such timer. It then applies the breached filter, keeping only breached cases when breached is true and only the rest when it is false. Both clocks appear side by side because a deviation pauses the stage clock while the prescription clock keeps running. Add index ix_timer_case_type on timer (case_id, timer_type) where the status is RUNNING, PAUSED or EXPIRED, through a Flyway migration in the P3 migration folder.

### Step 7

**In the story.** CaseListQueryService: orders the rows by breach, then age in state descending, then case number, and returns one page.

The service does this before it returns the page. Order the rows by breach first, then by age in state descending, then by case number. The three cases of AC1 therefore come back as RW-2026-000101, which is breached, then RW-2026-000102 at two days, then RW-2026-000103 at zero days. Case number is what makes the order stable: 120 cases with no breach and the same age in state still split cleanly into pages of 50, with no case on two pages and none missing. Put the order in the query rather than the front end, because only one page of rows is returned.

### Step 8

**In the story.** Front end: shows the columns in section 15 and marks each breached case.

The screen does this from the response. Show the columns case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock and deviation, and write Unassigned where a case has no owner. Mark each breached row with text, so that the mark is readable without color. Where no case matches the filters, show the Empty state with MSG-P3-020. The layout itself belongs to the designer under DL31, so keep the component to the columns and states listed in section 15.

### Step 9

**In the story.** Team manager: chooses Extract; the front end calls GET /api/recovery/v1/cases/export with the same filters.

The manager does this, and the screen calls GET /api/recovery/v1/cases/export with the same filters, including breached, and without page and size. The endpoint comes from RWB-E1-031; this story adds the new columns and the breached parameter, and records the change in the additions file. Keeping one set of filters for the list and the export is what makes the file match what the manager is looking at, as AC3 expects: three filters and one row. The right needed is R in Case record, and the caller's scope applies to the export exactly as it does to the list.

### Step 10

**In the story.** CaseExportService (RWB-E1-031): writes the matching rows with the ageing and clock columns to an Excel file, after the export is written to the access log.

The Workbench does this in CaseExportService, which RWB-E1-031 built. Extend it with the columns age in state, service level state, service level due, prescription date, prescription clock and deviation open, on top of the columns it already writes. Two rules control the file. The access log entry goes in first, through the RWB-E1-039 interface that the service already calls, with the user, the time, the filters and the row count; an entry that cannot be written returns 503 with MSG-P7-003 and no file. The row count is checked against caselist.export.maxrows, 10,000 at release, and a larger result is refused with 422 and MSG-P3-021 naming the limit. The file carries no customer personal field.

## RWB-E2-034 Interaction ledger on the case and from every channel

Module: P2 Integration

### Step 1

**In the story.** Outbox (RWB-TE-006): delivers to consumer "ledger-channels" the events InstructionIssued, PartnerResultSubmitted, NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched, and LoadCompleted for the COLLINS load.

The outbox built in RWB-TE-006 does this automatically. An outbox holds each published event in the database and delivers it to its consumers, retrying until the consumer succeeds, so no event is lost while your code is down. Your work is to add a consumer named ledger-channels to rwb.integration.outbox.consumers and have it take seven events: EV-20 InstructionIssued, EV-21 PartnerResultSubmitted, EV-14 NoticeDispatched, EV-15 NoticeDelivered, EV-10 TreatmentApproved, EV-25 ProceedsMatched and EV-26 LoadCompleted for the COLLINS load. Delivery is at least once, so the same event can arrive twice. EV-02 CaseAllocated and EV-04 CaseTransferred stay with the consumer of RWB-E1-067.

### Step 2

**In the story.** LedgerChannelListener: checks the event's idempotency key through IdempotencyGuard (RWB-E1-007) and passes the event to LedgerChannelMapper.

Your listener runs with no person involved. Write LedgerChannelListener and call IdempotencyGuard.firstTime with the consumer name ledger-channels and the event's idempotency key before you do any work. Idempotent means a repeated delivery has the same effect as the first one: the guard answers false on a key it has seen, the listener acknowledges the delivery, writes nothing, and the hit count for that key goes up by one under rule R-UNI-40. On a first delivery, pass the event to LedgerChannelMapper. With the flag rwb.integration.ledger-channels off, acknowledge all seven events and write nothing.

### Step 3

**In the story.** LedgerChannelMapper: maps the event to one LedgerEntryCommand with event code, channel, direction, occurred time, source, holder references and links (BR1 to BR5), reading the facts it needs through the owning module's published interface.

Your mapper turns one event into one ledger command, automatically. Write LedgerChannelMapper with a method per event type: InstructionIssued becomes a HANDOVER entry with channel PORTAL and direction OUTBOUND, PartnerResultSubmitted becomes PARTNER_RESULT with channel PORTAL and direction INBOUND, NoticeDispatched and NoticeDelivered each become a LETTER entry carrying the delivery status and the barcode, TreatmentApproved becomes OFFER linked to the treatment, and ProceedsMatched becomes PAYMENT linked to the proceeds. All of these carry source WORKBENCH. Read the facts you need through NoticeQuery.byId, InstructionQuery.byId and CaseQuery.byId, never from those modules' tables. Hold the contact point as a reference and never copy the number itself.

### Step 4

**In the story.** EfsContactOutcomeImporter (for LoadCompleted): reads the day's EFS contact outcomes for accounts linked to open cases through the P1 EFS interface, keeps the action codes on the EFS ledger outcome list and maps each to a CONTACT entry with source EFS.

This path runs as a job step and not through the mapper. Write EfsContactOutcomeImporter as a step of JOB-01 COLLINS load check and intake, running under SY-DATALOAD after the load passes its checks. Call EfsContactHistory.outcomesFor for the business date, then for each row call CaseQuery.openCaseIdsForAccount and keep only rows whose account sits on an open case. Keep only the action codes on the EFS ledger outcome list, a reference table loaded by the reference data administrator. Each kept row becomes a CONTACT entry with source EFS and the channel from its list row. Write an import summary counting rows read, written, excluded by the list and not on a case.

### Step 5

**In the story.** HolderEnricher: for CaseAllocated and CaseTransferred, which RWB-E1-067 maps to CASE_ALLOCATED and CASE_TRANSFERRED, adds the holder before and after the move to the same entry.

This is a change to code another story owns, so have its code owners review it. RWB-E1-067 already maps EV-02 CaseAllocated and EV-04 CaseTransferred to CASE_ALLOCATED and CASE_TRANSFERRED entries, and those two events keep their own consumer. Write HolderEnricher inside that mapper in recovery.dataengine.ledger to fill from_holder_ref and to_holder_ref on the same entry, in the form USER followed by the user ID. A hand-over between bank owners carries no channel. A hand-over to a partner is a separate entry, the HANDOVER of step 3, which holds the partner as PARTNER followed by the partner code.

### Step 6

**In the story.** RetentionClassResolver: sets the retention class from the Retention classes reference table by event code, for every entry the writer appends.

Your code sets this field on every entry, with no person involved. Write RetentionClassResolver to read the Retention classes reference table by ledger event code and return the class, and call it from InteractionLedgerWriter, so no entry is ever appended without one. Until Compliance sets the periods, every event code takes the class ILG-STD. The class is held per entry and set apart from the decision log, because a call note and a decision are kept for different lengths of time. The Compliance and PDPA officer changes a class through a reference data change, so read the table and write no value into code. The retention job itself is out of scope.

### Step 7

**In the story.** LedgerChannelListener: calls InteractionLedgerWriter.append for each entry inside the delivery's transaction; the writer refuses a repeated idempotency key and counts the repeat (R-UNI-40).

Your listener writes through the published interface of RWB-E1-066. Call InteractionLedgerWriter.append with each command inside the transaction of the outbox delivery, so the entry and the delivery succeed or fail together; a transaction is a group of writes the database applies all at once or not at all. The writer holds a unique key on idempotency_key, refuses a repeat and counts it under rule R-UNI-40. When the ledger store cannot be written, let the delivery fail so the outbox keeps it with status RETRYING, and raise an incident; the entry is written when the store comes back. After the retry limit, the delivery goes to the exception queue with a task for RW-PLATADM.

### Step 8

**In the story.** Case owner: opens the case record (SCR-03) and the timeline (SCR-04).

A person does this, the case owner or any role holding Case record R for a case in their scope. SCR-03 Case record gains a ledger section showing the latest 20 entries, and SCR-04 Case timeline gains filters for channel, source, actor and date range. Build LedgerTimelineSection as the React component behind both. The case owner is the reason the story exists: whoever picks up a case needs to see which number answered and who held the case last, without asking EFS or the partner. A case with no entry yet shows the empty state with MSG-P3-024 in place of a bare empty list.

### Step 9

**In the story.** Front end: calls GET /api/recovery/v1/cases/{caseId}/interactions with the channel, actor and date filters.

The screen makes this call automatically. The endpoint GET /api/recovery/v1/cases/{caseId}/interactions already exists and takes the case ID in the path and channel, actor, from, to, page and size as parameters. This story adds fields to the Interaction schema it returns: contactPointId, fromHolderRef, toHolderRef, treatmentId, proceedsId and retentionClass, all recorded in the additions file. Extend the schema in the API specification and regenerate the types. A caller without Case record R is refused with 403 and MSG-P4-002; a case that does not exist or sits outside the caller's scope is refused with 404 and MSG-P4-003, so scope and absence look the same.

### Step 10

**In the story.** Front end: shows the entries in case sequence order with time, channel, contact point reached (masked by role), outcome, promise, offer or payment link, holder change and source.

The screen renders what the endpoint returned, and no further read happens. Show each entry with its time, channel, the contact point reached, the outcome, any promise amount and date, a link to the linked offer or payment, the holder change on a hand-over, the delivery status on a letter, and the source, EFS or WORKBENCH. Mask the contact point by role, so a role that may not see a phone number gets the reference and not the digits. The first page of a case holding 500 entries has to appear in under 2 seconds, which the index on case and time serves. Keep the ordering rule in one place in the front end.

## RWB-E2-035 Next action on the case

Module: P2 Integration

### Step 1

**In the story.** SY-RULES: evaluates the route set and returns the firing rule row for the case's state and event.

The rules component does this with no person involved. A route set is the set of rule rows for a recovery route, and each row holds the from-state, the event, the to_state, the action text, the owner role, the timer and the rule ID and version. The firing rule is the one row whose from-state and event match what just happened on the case. The center of excellence analyst owns the action, owner and timer columns of those rows, and they are loaded as data in RWB-E1-029, so no action text ever sits in your code. There is nothing to build in this step itself. What follows depends on it: your code is handed the firing rule row and copies from it.

### Step 2

**In the story.** SY-CASEWF: moves the case to the rule's to_state and, in the same transaction, calls NextActionAssigner with the firing rule.

The case workflow module does this; no person is involved. Your change is one call: from the transition service built in RWB-E1-018, call NextActionAssigner.assign with the case ID, the firing rule and the business date, inside the transaction that already holds the move. A transaction is a group of database changes that either all take effect or none do, so a case never carries its new state with the next action of the old one. Two transitions committing on one case at once are handled by the optimistic lock on the case row, which refuses the second commit against a changed version: it answers MSG-GEN-004, is retried against the new version, and leaves the next action of the rule that committed last.

### Step 3

**In the story.** NextActionAssigner: copies the rule's action_text, owner_role and rule_id to the case.

The assigner does this in code, and no person ever types a next action. Add the columns to recovery_case with a migration in the P3 migration folder: next_action_text varchar(1000), next_action_owner_role varchar(20), next_action_due_date date, next_action_rule_id varchar(20) and next_action_waiting boolean not null default false, with the partial index named in section 13 for cases with no due date. Build NextActionAssigner to write the action text, the owner role and the rule ID from the firing rule row onto those columns. For the owner shown to a reader, compare the rule owner role with the role code of the case queue: when they are the same, show the case owner named on the case, and otherwise show the role name read through the P4 reference data interface.

### Step 4

**In the story.** TimerSpecResolver: turns the rule's timer_spec into a due date (BR3); when the spec has no fixed duration it reads the service levels and timers reference table for the to_state (BR4).

Code does this with no person involved. Build TimerSpecResolver as pure functions that take the timer text, the to_state, the date of the move and the holiday list. The patterns are fixed in BR3: "n working days" adds that many working days, "n days" with any label before it adds that many calendar days, "same day" and "immediate" give the date of the move, and "next working day" adds one working day. Any other text, "None" among it, means reading the service levels and timers table for the to_state through the P4 reference data interface. Working days are Monday to Friday, less the dates in the bank holiday list under the configuration key rwb.calendar.bank-holidays. Keep durations for named states out of the parser, which recognizes patterns only. Build the pattern table from the rule rows in force and unit test AC5, AC7 and AC12.

### Step 5

**In the story.** NextActionAssigner: sets next_action_waiting when the owner role belongs to a customer party or a partner user (BR5).

The assigner does this in code. Read the owner role through the P4 reference data interface, which returns the role name and the role class, and set next_action_waiting to true when that class is Customer party or Partner user. The screen then shows the text starting "Waiting for" and the owner name before the action text, as AC3 reads: "Waiting for Customer (borrower): Set the payment due date and wait for the money", with the wait ending on 13 January 2027. A wait is a valid next action, so a case in this state raises no exception task and is not on the list of cases with no next action. The flag is a column on the case, so the list and the record both read it from the same place.

### Step 6

**In the story.** NextActionAssigner: when no due date can be found, leaves the due date empty and raises task NEXT_ACTION_MISSING on the exception queue for the team manager (BR7).

The assigner does this with no person involved. It happens when the rule timer has no fixed duration and the service levels and timers table holds no row for the to_state, which is AC6 with rule R-DEV-05 moving a case to DEV_WITH_OWNER. Write the action text and the owner role as usual, leave the due date empty, and write one task row with task code NEXT_ACTION_MISSING, element type HUMAN_TASK, discretion REQUIRED and owner role RW-TEAMMGR, for the team manager of the case team. The case record then shows the warning MSG-P2-023 naming that team, and the team manager works the task on SCR-09 Exception queue. At most one open task exists per case, and the task is canceled when the case closes.

### Step 7

**In the story.** JOB-05 timer check: every 5 minutes finds active cases with no next action, resolves them from the latest state change in the decision log, or raises the same task once.

This runs as a step in an existing job, with no person involved. Build NextActionCheckStep inside JOB-05 Timer check, which runs every five minutes, and have it select active cases whose next action rule ID or due date is empty, using the partial index on the case table. For each such case, call the P7 decision log query for the latest state change, which returns the rule that last moved the case, and fill the next action fields from that rule. AC11 is the case to test: three active cases moved by R-RES-04 on 11 December 2026 come out with the due date of 15 December 2026 after a run on 14 December. Where no rule can be found, raise the NEXT_ACTION_MISSING task, once only. A case the run misses is picked up by the next run.

### Step 8

**In the story.** Case owner: opens the case record (SCR-03); the front end calls GET /api/recovery/v1/cases/{caseId}/next-action and shows the action, the owner and the due date, or the waiting text.

A person opens the case record and the browser makes the call. Build NextActionController for the new endpoint and NextActionPanel for the SCR-03 header. The response holds the action text, the owner role, the owner name, the owner user ID where the case owner is the one shown, the due date, and the flags for waiting, overdue and missing, with the rule ID and version. The panel shows the action, its owner and its due date, or the waiting text with the wait end date, marks an overdue action with the word Overdue, and shows MSG-P2-023 when the action is missing. A reader without Case record R is refused with 403 and MSG-P4-002, which is the access test, and a case outside their scope answers 404 with MSG-P4-003.

### Step 9

**In the story.** Team manager: opens the case list (SCR-02); the next action, its owner and due date are columns and an overdue action is marked (BR6).

A person reads this, and the work is in the list and export responses. Add nextAction, nextActionOwner, nextActionDueDate and nextActionOverdue to each Case item returned by the case list endpoint and to each row of the export, read from the same columns on the case, with the authorization and errors left as RWB-E2-033 set them. An action is overdue when its due date is earlier than today and the case is not closed, so in AC4, read on 16 December 2026, the case due 15 December is marked Overdue and the case due 13 January 2027 is not. With the feature flag rwb.casewf.next-action off, these columns and the panel are hidden. The story is done when the report of active cases with no next action reads zero on the SIT data set after JOB-05 has run.

## RWB-E2-036 Queue write interface for models and agents

Module: P2 Integration

### Step 1

**In the story.** Caller (model job or agent under its service identity): sends POST /api/recovery/v1/queues/{queueId}/placements with caseId, reason, modelOrAgent and version.

The caller is a model job or an agent running under its own service identity, so no person makes this call. Build the endpoint from the generated server interface for operationId postQueuesQueueidPlacements, taking PlacementRequest with caseId required as a uuid, reason required at 1 to 1,000 characters, modelOrAgent required as a caller code from the approved list, and version required at 1 to 40 characters. The acceptance criteria use identity SY-AGENT with caller MDL-SYN-PRIORITY. The code sits in folder recovery/casewf/placement even though the story is in the P2 backlog, because the queue and case tables belong to P3.

### Step 2

**In the story.** PlacementController: returns 404 with MSG-P2-025 when the feature flag is off.

The controller does this first, before any other check. Read the feature flag rwb.casewf.queue-placement, which is off by default and on only in DEV and SIT test runs. When it is off, answer 404 with MSG-P2-025, which reads that queue placement by models and agents is switched off, and change nothing: no case, no assignment and no decision log entry, which AC4 tests. The platform administrator switches the flag on once a caller has been approved. The flag has to be off in UAT and production at the release, and the tests of this story run with it on in SIT.

### Step 3

**In the story.** PlacementController: checks Queue and allocation C through the common module access check.

The controller does this with no person involved. Call the common module access check so the caller's service identity passes the same test as a person: it needs Queue and allocation C in the permission matrix version in force, with scope All for service identities. Without the right, answer 403 with MSG-P4-002. The production matrix gives SY-AGENT R only, so the security administrator has to load a matrix version granting C before the first caller can work, which is what access test TC-E2-036-13 checks. No model or agent reaches a queue without passing this check.

### Step 4

**In the story.** PlacementController: validates the four fields and checks that modelOrAgent is in the approved callers list for this service identity.

The controller does this. Reject an empty field with 422 and MSG-GEN-001 naming it, and a reason or version outside its length with MSG-GEN-002. Build ApprovedCallerList to read the configuration key rwb.casewf.placement.approved-callers, which holds each caller code, its type MODEL or AGENT, and the service identity listed for it. A caller code that is not in the list for the calling identity answers 422 with MSG-P2-020 and changes nothing, which AC5 tests with MDL-SYN-UNLISTED. The list is empty at go-live: the center of excellence analyst asks for an entry and the risk and model risk officer approves it.

### Step 5

**In the story.** PlacementService: reads the queue and the case; refuses a closed case, a case with an open deviation and a case already in this queue.

The service does this with no person involved. Read the queue for its assignment method, caseload cap and overflow queue, and the case for its status, its current queue and its deviation_open flag. Three refusals follow, each answering 409 and changing nothing: a case already in the target queue answers MSG-P2-024, which also covers a repeated call; a closed case answers MSG-P3-005; and a case with an open deviation answers MSG-P2-021 and stays with the deviation handler under R-DEV-01. A queue or case that does not exist answers 404 with MSG-P4-003.

### Step 6

**In the story.** PlacementService: builds the decision log record with the caller, reason, model or agent version and target queue (BR5).

The service builds the record itself. Fill a DecisionLogRecord with decision code D6 from LOV-DECISION, the caller identity, the reason text sent in the request, the model or agent with its version, the target queue, and a final call in the form PLACED MTG-BKK-PRI. The record is built here and written at the end of step 8, which puts it in the same transaction as the case change. AC3 checks each of those values on the entry. The reason text is the caller's own code or phrase and holds no customer data, which keeps personal data out of the log.

### Step 7

**In the story.** PlacementService: sets the case queue and calls AllocationService.assignInQueue, which applies the queue's method and caseload cap and uses the overflow queue when every owner is at the cap.

The service calls the allocation engine; no person picks the owner. Add assignInQueue, taking the case, the queue and the source identity, to AllocationService from RWB-E1-020, reusing the owner choice, cap and overflow logic that allocate already has. The method skips owners at the caseload cap, 150 in the queue data under DL23, and picks the next owner by the queue's method, ROUND_ROBIN in the acceptance criteria. AC2 gives the case to U-5002 at 149 open cases while skipping U-5001 at 150, then places the next case in queue MTG-BKK-OVF with no owner and status NEW when both owners are at the cap.

### Step 8

**In the story.** PlacementService: ends any previous assignment, writes the new assignment with reason ALLOCATION, publishes CaseAllocated (and CaseTransferred when the case had an owner) to the outbox and calls DecisionLogWriter.write as the last step, all in one transaction. If the write fails, nothing commits.

The service writes all of this in one transaction. End the open assignment, insert the new assignment with reason ALLOCATION and the caller's service identity in created_by, and write EV-02 CaseAllocated to the outbox, plus EV-04 CaseTransferred when the case already had an owner. Add the unique index uk_assignment_open_case on assignment by case_id where ended_at is null and task_id is null, so a case holds one open case assignment. DecisionLogWriter.write runs last under Propagation.MANDATORY, so a failure throws, the whole transaction rolls back, the endpoint answers 503 with MSG-P7-003 and an incident is raised under R-UNI-39.

### Step 9

**In the story.** PlacementController: returns 201 with the placement result.

The controller answers the caller. Return 201 with the Assignment of the new owner. When every owner was at the cap, no owner is set, and the response carries the placement result with the overflow queue ID and no assignment, a response variant recorded in the additions file, so build both shapes of the reply. Two placements of one case committing at the same time leave one at 201 and refuse the other with 409 and MSG-GEN-004 through the optimistic lock on the case version, which AC11 tests. A placed case then shows on SCR-07 and SCR-02 like any other, and its entry on the decision log query SCR-38.

## RWB-E2-028 Case intake agent live at L1 [E3a]

Module: P10 Agent runtime

### Step 1

**In the story.** SY-CASEWF: creates case "RW-2027-000501" and writes EV-01 CaseCreated.

Automatic. The case and workflow service identity SY-CASEWF creates the case and publishes CaseCreated, event EV-01, which already happens and needs no change from you. This story consumes that event: IntakeShadowListener from the earlier agent stories picks it up and decides whether to run the intake agent for the case. Nothing in this story creates or changes a case, and agent output never sets a case status, a task or a field. The case number used in the acceptance criteria, RW-2027-000501, is synthetic test data.

### Step 2

**In the story.** System: runs agent "INTAKE" in mode L1 through the orchestrator and stores the summary and gap flags on the agent run.

Automatic, with no user waiting on it. Extend IntakeShadowListener to read the autonomy mode of the agent policy in force for the case's segment, which is L1 under policy INTAKE version P2, approved by RW-RISK from 2027-01-25. On L1 it runs the agent through the orchestrator, and the run is kept in agent_run with its agent code, version, mode, status, output, confidence, data_as_of and run time. The summary holds masking tokens only, so no personal value goes to the model or into the stored output. A segment whose mode is still SHADOW produces a run that is never shown to a user.

### Step 3

**In the story.** Case owner: opens SCR-03 Case record for the case.

A person does this. The case owner, holding RW-CASEOWN with Case record CRU, opens the case record for a case in their scope. SCR-03 already exists from RWB-E1-035 with its history timeline, and your change adds one panel to it. The screen has to load in under two seconds whether or not the panel has anything to show, so the panel loads beside the case record and never blocks it. In the read only state of SCR-03 the feedback controls are hidden.

### Step 4

**In the story.** System: loads the case record and, without waiting on the model, calls GET /cases/{caseId}/agent-outputs for the stored L1 output.

Automatic. Build GET /cases/{caseId}/agent-outputs to return an AgentOutput array read from stored agent runs, never by calling the model, so the case record waits for nothing. AgentOutputQueryService checks the caller's scope through the P3 interface and keeps only runs whose mode is L1 for the case segment, so shadow output never reaches a user and a case outside the scope gets 404 with MSG-P4-003. The response is an empty array when no L1 output exists, which is also what the endpoint returns with the feature flag rwb.agent.intake-l1 off. Right R in the capability area Case record is required.

### Step 5

**In the story.** System: shows the panel "Agent summary" with the agent name, the version "INTAKE@P2/PR3", the gap flags with reasons and the controls Accept, Correct and Reject.

Automatic. Build AgentSummaryPanel as a React component on SCR-03 showing the summary text, each gap flag with its reason, the agent name INTAKE, the version INTAKE@P2/PR3 and the marker “Agent output”, so the reader always knows the text came from an agent and which version produced it. Add the three controls Accept, Correct and Reject. Build the panel states the story lists: loading with a skeleton, empty with no panel at all, unavailable with MSG-P10-005 when the run timed out or failed a guardrail, stale with MSG-P1-001 and the data date above the summary, ready, and recorded with the verdict and date and no controls.

### Step 6

**In the story.** Case owner: chooses Accept, or Correct or Reject with a reason.

A person does this, and only a role holding right U in the capability area Case record, so a case owner may give feedback while a team manager reading a team case may not. The panel posts to POST /agent-runs/{runId}/feedback with the item key, which defaults to SUMMARY, the verdict ACCEPTED, CORRECTED or REJECTED, and an If-Match header carrying the run row version. A reason of up to 1,000 characters is required for CORRECTED and REJECTED: an empty reason is refused with 422 and MSG-P7-005 and nothing is stored. A correction records the reason and leaves the summary text alone.

### Step 7

**In the story.** System: writes one decision log entry (decision D6, agent version, recommendation reference, final call ACCEPTED, CORRECTED or REJECTED, reason), then stores the feedback on the agent run.

Automatic, and the order is the point of the step. AgentFeedbackService writes the decision log entry first through the P7 DecisionLogWriter, with the case id, decision code D6, the agent version INTAKE@P2/PR3, the model version, the agent run reference as the inputs reference, the recommendation holding the run id and the gaps, the final call as the verdict, the reason as the override reason and the owner as the approver. It then writes the agent_feedback row with the decision log id, both in one transaction, so the database keeps the entry and the row together or discards both. When the decision log write fails, the caller gets 503 with MSG-P7-003, no feedback row exists and the controls stay on the panel.

### Step 8

**In the story.** System: the panel shows the recorded verdict; the next JOB-15 run counts it in the acceptance and correction rates by segment.

Automatic. After a successful write the panel moves to its recorded state, showing the verdict and its date with the controls gone, and a second feedback request for the same run is refused with 409 and MSG-GEN-004, which the unique key on agent_run_id and item_key in migration V10_008__agent_feedback.sql enforces. JOB-15 then counts the stored verdicts into the rates SCR-46 shows by agent and segment. AC2 gives 300 feedback records for MORTGAGE and BKK in January 2027, with 240 accepted, 45 corrected and 15 rejected, so the acceptance rate is 0.8000 and the correction rate 0.1500.

## RWB-E2-029 Deviation screening agent evaluation and L1 on one segment [E3b]

Module: P10 Agent runtime

### Step 1

**In the story.** RW-COE: starts the evaluation of "SCREENING" on "SCREEN-S2" version 1.

A person starts the run. RW-COE calls POST /api/recovery/v1/admin/agent-evaluations with the Rules and parameters C right, naming the agent SCREENING and the sample SCREEN-S2 version 1. That sample holds the business analysts' review of 500 shadow cases: for each case, which of the deviation codes X1 to X7 the analysts judged to be present. Shadow means the agent has been running on real cases without its output reaching anyone, which RWB-E1-062 put in place. The evaluation compares the agent's output on those cases with the analysts' judgement, and nothing happens to the cases themselves.

### Step 2

**In the story.** System: stores precision and recall per code X1 to X7 with sample size 500.

The scoring is code. For each code X1 to X7, count the true positives, false positives and false negatives against the sample, then store precision and recall on agent_evaluation with label_key set to the code and sample_size 500. Precision is true positives divided by every case the agent flagged with that code; recall is true positives divided by every case the sample says carries it. For X1 with 41 true positives, 4 false positives and 5 false negatives, that gives 0.9111 and 0.8913. Keep four decimal places, because the promotion conditions in step 3 compare against values at that precision.

### Step 3

**In the story.** RW-COE: loads policy "SCREENING" version "P2" with mode L1 for segment MORTGAGE and BKK, the evaluation run, the conditions, the fallback and the measures; RW-RISK approves it.

A person loads the proposal and a second person approves it. RW-COE calls POST /api/recovery/v1/admin/agent-configs with policy SCREENING version P2: autonomy mode L1 for segment product group MORTGAGE and segment region BKK, the ID of the evaluation run from step 1, the promotion conditions, the fallback and the measures. RW-RISK then approves through POST /admin/agent-configs/{versionId}/approve with the Rules and parameters A right. The policy loader checks the stated conditions against that evaluation run, so a condition of recall at least 0.75 for every code refuses the load with 422 and MSG-P10-001 naming X4 at 0.6000. On a clean load the version reaches status LOADED.

### Step 4

**In the story.** System: on EV-01 or EV-16 for a Mortgage case in region BKK, runs SCREENING in mode L1; for any other segment, runs it in shadow.

The agent runs on an event, with no one asking. ScreeningShadowListener already consumes EV-01 CaseCreated and EV-16 DocumentStored; extend it to read the autonomy mode from the policy in force for the case rather than running every case in shadow. Compare the case product_group and region_code with segment_product_group and segment_region_code on agent_policy: a Mortgage case in BKK runs in mode L1, and every other case keeps running in shadow with its output reaching no user. Record the mode and the segment on the agent_run row. With the flag rwb.agent.screening-l1 off, every segment runs in shadow.

### Step 5

**In the story.** Case owner: opens SCR-03 Case record; the panel "Proposed deviations" lists each proposed code with reasons, sources, confidence and the marker "Agent output".

The officer opens the case and the proposals are already there. Build ProposedDeviationsPanel on SCR-03 Case record, fed by GET /api/recovery/v1/cases/{caseId}/agent-outputs, which answers with the SCREENING proposals: the code, the reasons, the source references, the preceding contact, the confidence, a low confidence flag and any feedback already given. ScreeningOutputFilter prepares that list: drop any code already open as a deviation on the case, and set the low confidence flag when the confidence falls under the floor 0.80, which the panel shows as the marker Low confidence. Every proposal carries the marker Agent output, and reasons shown on the panel hold masking tokens in place of personal data.

### Step 6

**In the story.** Case owner: confirms a proposal; the system calls the S8 deviation service, which raises the deviation with raised_by SCREENING_AGENT and applies R-DEV-01.

The officer confirms, and the agent itself raises nothing. On a confirmation, call DeviationService.raise from RWB-E2-015 with the case, the code, the reason, any document IDs, raisedBy set to SCREENING_AGENT and the agent run ID; it answers with the deviation ID and the ID of the decision log entry it wrote. S8 applies R-DEV-01, which pauses the stage clock and routes the case, so the case status becomes On hold and the flag shows on SCR-03 and in SCR-08 Deviation queue. S8 publishes EV-06. Two confirmations of the same proposal leave one deviation; the second answers 409 with MSG-GEN-004.

### Step 7

**In the story.** System: stores feedback ACCEPTED for that code, linked to the decision log entry S8 wrote.

Your code writes the feedback row after S8 answers. Insert one agent_feedback row with the agent run ID, item_key set to the code such as X1, verdict ACCEPTED, the user and the time, and decision_log_id set to the entry ID that DeviationService.raise returned. One row per run and item: a repeat is refused rather than counted twice. This row is what ties the officer's judgement back to the agent output, so the error rate per flag can be measured later. The endpoint carrying the verdict is POST /api/recovery/v1/agent-runs/{runId}/feedback, which needs the Case record U right.

### Step 8

**In the story.** Case owner: rejects a proposal with a reason; the system writes a decision log entry with final call REJECTED and stores feedback REJECTED.

A rejection is also a decision, and the order of writes matters. The same feedback endpoint takes verdict REJECTED with a reason, and an empty reason answers 422 with MSG-P7-005. Write the decision log entry first, through the P7 DecisionLogWriter, holding the code as the decision, the agent version SCREENING@P2/PR2, the final call REJECTED and the officer's reason; only then insert the agent_feedback row with verdict REJECTED. When the decision log write fails, store nothing at all: answer 503 with MSG-P7-003 and raise the incident, leaving no feedback row behind. No deviation is raised and the case status does not change.

## RWB-E2-030 Legal document agent in shadow on Epic 1 data [E3c]

Module: P10 Agent runtime

### Step 1

**In the story.** RW-COE: loads sample "LEGAL-S1" and starts the evaluation of "LEGAL_DOC" through POST /admin/agent-evaluations.

A person does both actions. The center of excellence analyst, RW-COE, loads the sample LEGAL-S1 through POST /api/recovery/v1/admin/agent-samples and then starts the evaluation through POST /api/recovery/v1/admin/agent-evaluations for agent LEGAL_DOC. Both endpoints come from RWB-E1-058 and need Rules and parameters right C, so RW-LITOFF calling them is refused with MSG-P4-002 (TC-E2-030-10). The sample is the answer key: for 50 Epic 1 litigation cases it holds one row per case and checklist item with the status the legal officers gave, PRESENT, MISSING or DEFECT. The officers supply those packs. A sample with no labeled rows is refused with MSG-P10-002.

### Step 2

**In the story.** System: for each sample case, runs the agent in shadow: reads the case, the legal action, the documents with their fields and the checklist for the case type.

The run is automatic, once per sample case. Shadow mode means the agent reads and answers while nothing it produces reaches a user or changes a record. LegalPackInputAssembler builds the input: the case, its legal action through S4 LegalActionQueryService.listByCase, the documents and their fields through P5 DocumentQueryService.listByCase and getFields, and the checklist for the case type through getChecklist. Every call runs as the service identity SY-AGENT with read rights only, and field values are masked before the model call. Policy LEGAL_DOC version P1 sets the 60 second timeout and the allowed tools. A call that fails gives the run status TOOL_UNAVAILABLE with fallback true, and that case is scored as not run (AC6).

### Step 3

**In the story.** System: checks the answer: every checklist item has a status, every document ID belongs to the case, and every DEFECT has a reason.

The answer is checked before it is kept, by LegalPackRuleChecks, with no person reviewing it. The checks are that the output matches the schema legal-pack-v1, that every item of the checklist for that case type has a status, that every document ID named belongs to the same case, and that every DEFECT carries a reason. A missing status fails the SCHEMA check (AC5) and a document from another case fails the SCHEMA_RULE check (AC4). Either way the run holds status GUARDRAIL_FAILED and the case counts as wrong for every item in the scoring of step 5. The checklist for case type MORTGAGE_CIVIL has 9 items in the examples.

### Step 4

**In the story.** System: stores the pack (document IDs per item) and the completeness list on the agent run; nothing is shown to a user and no document, pack or legal action changes.

The system writes the result on the agent_run row and nowhere else: the pack as document IDs per checklist item, the completeness list, the autonomy mode, the guardrail result, the latency, the tokens in and out and the cost. No document, legal action, task or case field changes, and no user facing endpoint returns the pack (AC1). SCR-46 Agent monitor shows LEGAL_DOC in state Shadow with its runs, fallbacks and score, which is where the analyst watches the batch. The event EV-28 AgentRunCompleted is published per run. The agent never changes a write once legal document.

### Step 5

**In the story.** System: scores agreement with the officers' pack per checklist item and stores it with sample size.

LegalPackScorer compares each run with the officer answer for the same case and item, and the harness stores the result in agent_evaluation. The agreement rate for an item is the number of cases where the agent status equals the officer status divided by the scored cases, written to four decimals, so 46 agreeing cases out of 50 give 0.9200 for DEMAND_NOTICE_PROOF (AC2). The sample size is stored next to the rate, and a case that did not run is left out of both, which leaves 49 scored after one TOOL_UNAVAILABLE run. Build step 4 asks you to test the scorer first on a 10 case fixture with known agreement.

### Step 6

**In the story.** RW-COE: reads the scores and loads policy version "P2": mode L1 with conditions to promote, or mode SHADOW with a review date to keep shadow.

The analyst reads the scores through GET /api/recovery/v1/admin/agent-evaluations and then loads the next policy version, P2, through POST /api/recovery/v1/admin/agent-configs. There are two choices: mode L1 with the conditions under which the agent may act, or mode SHADOW with a review date to keep it in shadow. Your work here is PromotionProposalValidator, extended for this story. It refuses a proposal of mode L1 when fewer than 50 cases were scored, and a proposal of mode SHADOW with no review date, both with 422 and MSG-P10-001 naming the check (AC7, AC8). An L1 proposal is accepted only when the evaluation meets every condition stated in it.

### Step 7

**In the story.** RW-RISK: approves the version; the decision and its date are recorded on the policy row.

A second person closes the decision. RW-RISK, the risk and model risk officer, approves version P2, and the system records the status, the approver and the approval date on the agent_policy row. The person who loaded the version cannot approve it: coe.user01 approving their own load is refused with 409 and MSG-P7-002 (AC9). This is the separation of duty between the center of excellence analyst and the risk officer, the same pattern as a rule load. Until the approval the version in force is unchanged, so the agent keeps running under P1.
