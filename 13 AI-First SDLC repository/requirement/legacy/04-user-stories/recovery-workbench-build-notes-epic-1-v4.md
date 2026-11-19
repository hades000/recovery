<!-- source: 04 User stories/Recovery Workbench Build Notes Epic 1 v4.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench Build Notes Epic 1 v4.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench build notes, Epic 1

SCB Collections and Recovery. Henka Group.

(C) Siam Commercial Bank and Henka Pte Ltd

Every flow step of every story in Epic 1, written out in full so it can be followed without knowing the Workbench already. Each entry gives the step as the story states it, then what it means: who acts, what runs on its own, and what has to be built. The story remains the specification. Where the two differ, the story governs.

## RWB-E1-001 Recovery tables for the 14 data products

Module: P1 Recovery data engine

### Step 1

**In the story.** Pipeline: runs migration `V0001__rwb_e1_001_recovery_schema.sql` in DEV with `recoverySchema = recovery`.

Create one Flyway migration file at src/main/resources/db/migration/recovery/V0001__rwb_e1_001_recovery_schema.sql. Its contents come from Recovery Workbench Physical Schema v4.sql, which holds the DDL for all 108 tables of the recovery module. This story needs 44 of them. Wherever that file fixes the schema name, put the placeholder ${recoverySchema} instead, which Flyway fills in when it runs. Add recoverySchema to the configuration service with the value recovery for both DEV and SIT. You never run the file by hand. Merging your branch is what makes the pipeline apply it, so the file has to be correct before it is merged.

### Step 2

**In the story.** Migration: creates the 43 tables, the 68 foreign keys, the 76 indexes and the append-only triggers on decision_log_entry and interaction, and the new table data_product, in one transaction.

Create all 44 tables inside one transaction, so a failure part way through leaves the schema untouched. Copy the columns, primary keys and unique constraints from Recovery Workbench Physical Schema v4.sql without changing a name or a type, because the test in step 4 compares them against the dictionary and fails on any difference. Declare the foreign keys as ALTER TABLE ... ADD CONSTRAINT statements after the tables exist, which is the form the schema file uses. Add the two triggers that call refuse_change() on decision_log_entry and interaction, so neither table accepts an UPDATE or a DELETE. Reconcile the counts first: this step says 68 foreign keys and 76 indexes, and the schema file now holds 66 and 76 for these tables.

### Step 3

**In the story.** Migration: inserts the 108 sys_objects rows, the 1,256 sys_fields rows and the 14 data_product seed rows (section 13), and creates the view `v_data_dictionary`.

Insert the dictionary rows in the same migration. One row in sys_objects for each of the 41 entities, and one row in sys_fields for each of the 413 fields, with the values taken from Recovery Workbench Source to Target Mapping v3.xlsx, which lists every field with its entity, data product, physical type, source system and source field. Insert the 14 data_product rows before the sys_objects rows, because sys_objects.data_product has a foreign key to data_product.product_code. Leave owner_user_id empty; a person supplies it in step 6. Then create the view v_data_dictionary, joining sys_objects and sys_fields so one query returns everything about a field. The schema file has no definition for that view, so you write it.

### Step 4

**In the story.** Pipeline: runs the dictionary conformance test, which compares every column in the recovery schema with sys_fields.

Write the conformance test as a pipeline test, not a unit test, because it has to run against a real database after the migration. Read the live columns from information_schema.columns for the recovery schema, read the rows of sys_fields, and compare in both directions. Fail the build if a real column has no dictionary row, if a dictionary row has no column, or if the physical types differ. Leave the 7 standard columns out of the comparison. The failure message must name the column that caused it, because AC5 asserts the exact wording.

### Step 5

**In the story.** Pipeline: repeats steps 1 to 4 in SIT.

No new code. The pipeline promotes the same artifact to SIT and runs the migration and the test again there. Flyway keeps its own table of which versions it has applied, so a second run finds 1.001 already applied and does nothing, which is what AC6 checks by comparing the row counts of sys_objects and sys_fields before and after.

### Step 6

**In the story.** Reference data administrator: loads the data product catalog file with table code `data_product` through `POST /admin/reference-loads`, naming the owner user ID of each product for the environment.

Build the load path for this table code. The reference data administrator sends the catalog file to POST /api/recovery/v1/admin/reference-loads with the table code data_product. Implement that endpoint if RWB-E1-043 has not already delivered it, and implement DataProductCatalogHandler as the ReferenceTableHandler registered for that code, which is how a load finds the class that handles it. The file holds the 14 products with the owner user ID for that environment, so DEV and SIT are given different files.

### Step 7

**In the story.** System: `DataProductCatalogHandler.validate` checks the file: 14 products DP01 to DP14, each with one system of record, one owner role from LOV-ROLE, one owner user ID and one refresh cycle.

Implement validate on DataProductCatalogHandler. Refuse the file unless it holds exactly DP01 to DP14 with none missing and none repeated, and unless every row names exactly one system of record, one owner role that exists in LOV-ROLE, one owner user ID, and one refresh cycle from DAILY, WEEKLY, MONTHLY and ON_CHANGE. Return MSG-P1-003, MSG-P1-004 and MSG-P1-007 for the cases AC7, AC8 and AC9 set out. Validation writes nothing at all: one bad row refuses the whole file.

### Step 8

**In the story.** Data steward: confirms the load as owner of the catalog through the reference data change process (RWB-E1-043).

Do not apply the load when it is uploaded. A second person has to approve it first, so the load stays pending until the data steward who owns the catalog approves it through the approve endpoint of the reference data change process built in RWB-E1-043. Record both the load and the approval in the decision log. This is what stops one person changing reference data alone.

### Step 9

**In the story.** System: `DataProductCatalogHandler.apply` writes the 14 rows in one transaction with the valid from date.

Implement apply. Write the 14 rows in a single transaction, each carrying the valid from date given on the load. Do not delete the version that was in force; reference data is versioned, and AC7 requires the rows already in force to survive when a later load is refused.

### Step 10

**In the story.** Developer or data steward: queries `v_data_dictionary` for entity loan_account and field days_past_due.

No application code in this step. It checks that the dictionary can be read by the people who will rely on it. Run a query against the view v_data_dictionary, filtering on the entity loan_account and the field days_past_due, which holds the number of days an account is overdue. Run it as a plain SQL query against the DEV database, not through the application, because the point is to prove the view itself returns the joined row. The same query is what a developer will use later whenever they need to know where a field comes from.

### Step 11

**In the story.** System: returns field ID DF-ACC-014, the types, the source system and source field, the data product, its refresh cycle and its owner.

The query must return one row holding field_id DF-ACC-014, data_type NUMBER, physical_type integer, source system Core bank (ALS) via COLLINS, source field DELAY_DAYS, data product DP01, refresh cycle DAILY and owner role RW-DATASTEW, with the owner user ID of DP01. If any of those come back empty, the sys_fields insert in step 3 is incomplete and the story is not done.

## RWB-E1-002 Case list v1 with case ID, owner and queue

Module: P1 Recovery data engine

### Step 1

**In the story.** Quartz: JOB-04 Daily reconciliation reaches its case list step after JOB-03 completes for the business date.

Quartz is the scheduler inside the Workbench that starts jobs by clock time or by a chain. No person starts this. You build CaseListChainListener, a Quartz job listener, which watches JOB-03 for the business date and starts the case list step of JOB-04 as soon as JOB-03 completes. If JOB-03 has not completed, the listener starts the step at the time held in the parameter caselist.allocation.wait.until, 07:15. The step itself is CaseListStepConfig, a Spring Batch step inside JOB-04, and it runs under the service identity SY-DATALOAD. The feature flag rwb.p1.case-list controls it: with the flag off, JOB-04 runs its other steps and skips this one.

### Step 2

**In the story.** System: checks through `LoadRunQuery.completedLoad("INT-01", businessDate)` that the account load for the business date is COMPLETED.

The step makes this check on its own, with no person involved. LoadRunQuery is the published read interface over the load_run table, built in RWB-E1-003. You call it instead of reading that table directly, because this story may read case and load data only through published interfaces. Pass interface INT-01, which is the account and arrears feed, and the business date. When the answer is COMPLETED, the step carries on. When it is anything else, the step stops before it writes any case list rows, writes a load_run with status REFUSED and the failed check "INT-01 not complete", and sends MSG-P1-001 to the team manager group. The previous extract file in the lake is left as it is.

### Step 3

**In the story.** System: opens a load_run row with job code JOB-04 and product DP03.

The step writes this row itself. load_run is the run record table from RWB-E1-003; it holds one row per job run with the job code, the product code, the business date, the status and the check results. Open means insert the row with status RUNNING at the start, then set it to COMPLETED, REFUSED or FAILED when the step ends, as section 9 says. Write job code JOB-04 and product code DP03 on the row. Later in the same run you add the four check results named in section 12: COUNT, BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED. The platform administrator reads this row through GET /admin/jobs with type=JOB-04.

### Step 4

**In the story.** System: reads the open case accounts from `CaseQueryApi.openCaseAccounts(businessDate)`.

The step calls this itself. CaseQueryApi is the Java interface published by the case workflow module and built in RWB-E1-018; the case workflow identity SY-CASEWF serves it. Your code may not query recovery_case, case_account or queue, so this call is the only way to reach case data. openCaseAccounts returns a Stream of OpenCaseAccountView, which carries the case ID, case number, account ID, product group, stage code, status, owner user ID, queue code, team code and route code. A Stream is read in pieces as the step works through it, so the whole day of cases is never held in memory at once. Write a contract test against this interface with a stub of synthetic cases. If the call raises an error part way, the step rolls back and the run status is FAILED.

### Step 5

**In the story.** System: joins each account to loan_account for account number, total balance and days past due.

The step does this with no person involved. loan_account is the data engine own table, so you read it directly, by the account ID that CaseQueryApi returned. A join here means matching that account ID to loan_account.id and taking three values from the matched row: account_no, total_balance and days_past_due. Some case accounts have no matching row, as exception X7 describes. For those, write the case list row with an empty total balance and empty days past due, and write one dq_exception row with check code CL-01 and the account as the record key. dq_exception is the data quality exception table, so the data steward can see which accounts were short of account data.

### Step 6

**In the story.** System: replaces the case_list_row rows for the business date in one transaction, each with the refresh time.

The step does this on its own. Create case_list_row with migration V1_002__case_list_row.sql and the columns listed in section 13, with the unique key uk_case_list_row on business date, case ID and account ID. Replace means delete every row already held for that business date and insert the new set. A transaction is a group of database changes that either all take effect or none do, so a reader never sees a part-built list, and a rerun for the same date leaves the same row count with no case account twice. Put the time of this run in refreshed_at on every row. CaseListRowRepository owns the delete and the insert, and your first test is the replace of one date of rows.

### Step 7

**In the story.** System: counts the case list rows at or above 90 days past due and compares the count with the ALS count of accounts at or above 90 days past due, less the accounts P3 excluded at entry.

The service CaseListCountCheck does this work with no person involved. Read the threshold from the parameter case.entry.dpd rather than writing 90 into the code. Count the case list rows you just wrote whose days past due reach the threshold. Then build the figure to match: count the loan_account rows at or above the threshold for the business date and subtract the number that the case workflow module excluded when the cases were created, which you get from CaseQueryApi.excludedAccountCount. In AC1, 28,140 accounts less 21 exclusions gives 28,119 to match. Compare the two counts against the parameter recon.caselist.tolerance.pct. Count the rows below the threshold as well, because they are reported as the BELOW_ENTRY check. Unit test the boundary exactly at the tolerance.

### Step 8

**In the story.** System: writes the count check result to the load_run and alerts the data steward and the team managers if the difference is above the tolerance.

The step writes the result and sends the alert with no person involved. Put the COUNT check on the load_run row of this run: PASS when the difference is inside the tolerance, FAIL with the difference when it is not. On a FAIL, call LoadAlertNotifier, the alert service built in RWB-E1-003, with MSG-P1-012, so the data steward group and the team manager groups receive the date, the product, the number of accounts and the percentage, as AC4 shows with 25 accounts and 0.09 percent. A failed count check does not hold the list back: the rows stay written and the extract file is still published, as exception X1 says. The recipient groups are configuration values that the platform administrator sets per environment.

### Step 9

**In the story.** System: writes the extract file for the business date to the data lake through the outbound file adapter.

The step writes the file itself. Build CaseListExtractWriter to produce the CSV with the ten columns in the order AC2 names, plus team, business date and refresh time, under the name case-list/<businessDate>.csv. Hand the file to the outbound file adapter from RWB-E1-007, interface INT-19, and never write to the lake from this code, because the adapter owns every outbound transfer. The lake path is a configuration value set per environment by the platform administrator. When the adapter fails every retry, the run still completes, the PUBLISHED check on the load_run is NO, and the transfer goes to the exception queue with a task for the platform administrator. Test that PUBLISHED check with the adapter forced to fail.

### Step 10

**In the story.** Power BI: refreshes the data set at 07:30; the report shows the ten columns, the filters and the refresh time.

No Workbench code runs here. The reporting and BI analyst builds the Power BI data set "Case list v1" on the extract file in the lake and schedules its refresh at 07:30, and the team managers read the report with Reporting R. Your part is the file behind it: the ten columns in the order AC2 names, plus team, business date and refresh time, so the analyst can offer filters on team, queue and product and show the line "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026" from the refresh time and the business date. This story builds no Workbench screen, and row-level security by team belongs to RWB-E1-016. The story is done when this data set refreshes in SIT from your extract file.

## RWB-E1-003 ALS daily extract load

Module: P1 Recovery data engine

### Step 1

**In the story.** Quartz: starts JOB-01 COLLINS load check and intake at 05:00 for the expected business date, the previous working day.

Quartz is the scheduler inside the application, so no person starts this run. Build CollinsLoadJob as a Quartz job with a cron trigger at 05:00 Asia/Bangkok on working days, then a retry every 60 minutes, the value of load.retry.interval, until the window end at 09:00 or until both interfaces reach COMPLETED or REFUSED. The job computes the expected business date from the working day calendar in the reference data service of RWB-E1-043, which gives the previous working day. It runs under the service identity SY-DATALOAD. Use @DisallowConcurrentExecution and the clustered job store so two ACE nodes do not both carry out the same run.

### Step 2

**In the story.** System: opens a load_run row for INT-01 with status RUNNING; the unique key (interface, business date) stops a second run.

This happens on its own as the first step of the Spring Batch job. Insert one load_run row for interface INT-01 and the business date with status RUNNING, started_at, job_code, product_code and the mapping version in force. Migration V1_003__load_run.sql creates load_run and the unique index uk_load_run_active on interface_id and business_date where status is RUNNING or COMPLETED. A unique index is a database rule that refuses a second row with the same values, so when a second node tries the same insert the database rejects it and that attempt ends with nothing written. A rerun for a date already COMPLETED hits the same key, and the endpoint answers 409 with MSG-P1-011.

### Step 3

**In the story.** System: runs DQ-001 business date, DQ-002 structure, DQ-003 control total and DQ-004 keys on the staging records; any failure refuses the load.

The check runner carries this out with no person involved. Write the four checks in LoadCheckRunner as SQL over the COLLINS staging tables, whose names come from the configuration keys rwb.p1.collins.int01.table, rwb.p1.collins.int02.table and rwb.p1.collins.trailer.table. DQ-001 compares the business date on the records and the trailer against the expected date. DQ-002 checks structure. DQ-003 compares the trailer record count and balance total against the staging rows. DQ-004 looks for a repeated account key. One failure refuses the whole load: no loan_account row changes, load_run takes status REFUSED with failed_check set, LoadRefused goes to the outbox and MSG-P1-002 goes to the data steward and platform administrator groups.

### Step 4

**In the story.** System: runs DQ-005 references and DQ-006 lists of values; records that fail are counted, and the load is refused if the count is above 0.50 percent.

The same check runner does this once the blocking checks pass. These two checks count records whose values do not match anything: the reference check looks for a key with no matching row to point at, and the list of values check looks for a source code the code map cannot translate. Count the failures and divide by the rows read. Compare the result against the parameter load.hold.tolerance.pct, which is 0.50 percent. At or below the tolerance those records are held and the rest load. Above it the load is refused in full and no row for that date is written. Write tests for both sides of the 0.50 percent boundary, as section 13 build step 2 asks.

### Step 5

**In the story.** System: maps each record through the mapping version in force and the code map, and writes loan_account in one transaction, with data_as_of set to the business date.

The job does this; nobody keys anything. SourceMappingService reads the approved mapping version in force from source_field_map and the code map from source_code_map, then builds each target value with the transformations COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP and BUSINESS_DATE. A mapping version with no approval refuses the load. LoanAccountWriter upserts by account_no, so add uk_loan_account_no when it is not present. A transaction is one unit of work that the database either keeps in full or throws away in full, and the whole interface writes inside one, so a failure part way leaves no row carrying the new business date. Every written row takes data_as_of from the business date.

### Step 6

**In the story.** System: writes the held records to dq_exception with the check code and the account number.

This runs inside the same write step. For every record the tolerance checks held, insert a dq_exception row through DqExceptionRepository with load_run_id, product_code, the check code, record_key, reason_code, detail, raised_on and status. Migration V1_003 creates the table and an index on product_code and raised_on. The record_key column holds the account key alone, because no personal data may sit in this table, in logs or in tests. The number of held rows also goes on load_run.rows_held, which is what a run shows through GET /admin/jobs. AC6 is the test: 11 held payments give 11 rows with check code DQ-012, the account key and raised_on set to the business date.

### Step 7

**In the story.** System: runs DQ-007 movement against the previous load and alerts the data steward if it is outside 10 percent.

The job does this after the rows are written. Read the previous completed load_run for the same interface and compare its count and balance total against this load. Work out the change as a percentage and compare it against load.movement.tolerance.pct, which is 10.00 percent. The load still completes and nothing is held back. When the change is above the limit, LoadAlertNotifier sends MSG-P1-006 to the data steward group through the ACE notification path, with the recipient groups taken from reference data. A change of exactly 10.00 percent sends no alert, so write the comparison as strictly greater than the limit and test that boundary with the 165,000 to 184,500 fixture.

### Step 8

**In the story.** System: repeats steps 2 to 7 for INT-02 into account_payment, after INT-01 completes.

The Spring Batch job runs the same seven steps a second time, this time for interface INT-02 into account_payment. Order matters, because the reference check on payments reads loan_account.account_no, which the INT-01 steps have just written, so CollinsLoadJob launches the interfaces one after the other. AccountPaymentWriter inserts by account_id and payment_code with ON CONFLICT DO NOTHING, so add uk_account_payment on those two columns. INT-02 opens its own load_run row with its own counts, status and unique key, which means one business date has two runs, one per interface. Nothing here is a person's action.

### Step 9

**In the story.** System: runs the sample check on 50 random accounts and writes the result to the load_run check results.

The job does this once both interfaces are written. Pick accounts at random, the number coming from the parameter load.sample.size, which is 50, and compare total_balance, days_past_due and classification on each loaded row against the staging values after mapping. Write the outcome into load_run.check_results, the object that GET /admin/jobs returns, in the form SAMPLE = 50 of 50. That column holds one entry per check code with PASS, FAIL, HELD n or NOT_APPLICABLE, so the sample entry sits beside the DQ entries. This check never refuses a load; it records what was compared, which is what AC3 reads.

### Step 10

**In the story.** System: sets the load_run status to COMPLETED and publishes LoadCompleted through the outbox in the same transaction; RWB-E1-015 adds the freshness stamp to this transaction.

The job closes the run with no person involved. Set load_run status COMPLETED with ended_at, rows_read, rows_loaded and rows_held, and have LoadEventPublisher write LoadCompleted, EV-26 with source, businessDate, rows and checks, into the ACE outbox inside the same transaction as that status change. The outbox is a table the event is written into with the rest of the data, so the event and the status can never disagree: either both commit or neither does. The freshness stamp belongs to RWB-E1-015, which calls its own recordLoad inside this commit, so give that story a hook at the commit point rather than writing the stamp here.

## RWB-E1-004 EFS extract load

Module: P1 Recovery data engine

### Step 1

**In the story.** Quartz: JOB-01 attempt reaches the INT-07 step after the INT-01 step has completed for the business date.

Quartz is the scheduler inside the service, and it starts JOB-01 on every hourly attempt with no person involved. You add the INT-07 step to JOB-01 as a Spring Batch step, configured in EfsLoadStepConfig, and order it so that it only runs after the INT-01 step has finished for the same business date. When INT-01 has not completed, the INT-07 step does nothing on that attempt and the next hourly attempt tries again. The step runs under the service identity SY-DATALOAD, not under a user account. With the feature flag rwb.p1.efs-load off, JOB-01 skips this step and the window check.

### Step 2

**In the story.** System: opens a load_run for INT-07 and checks that the mapping version in force is approved.

No person triggers this. Your step code creates one load_run row for interface INT-07 and the business date before it reads any data. That row carries the status, the row counts and the check results, and the pair of interface_id and business_date is the key that keeps one run per interface per day. The step then reads the mapping version in force from source_field_map and checks approved_by, approved_on and approval_ref. A version with no approval means the load is refused in full with MSG-P1-002 and no collections_history row is written. The approval reference is the EFS system owner's sign-off that the data steward recorded earlier on the mapping version.

### Step 3

**In the story.** System: runs DQ-036 business date, DQ-037 structure, DQ-038 control total and DQ-039 keys; any failure refuses the load.

These four checks run automatically inside the step, through LoadCheckRunner from RWB-E1-003. Your work is to configure the four check codes for INT-07, not to write a new check engine. DQ-036 compares the business date on the COLLINS staging records, DQ-037 compares the columns present, DQ-038 compares the counts and totals against the trailer COLLINS writes, and DQ-039 checks the keys. Any one of them failing stops the whole load: nothing reaches collections_history, the load_run status becomes REFUSED, MSG-P1-002 names the failed check, and a LoadRefused event goes to the outbox, the table the service writes events to for publishing, with that check code. AC9 shows this for DQ-037.

### Step 4

**In the story.** System: runs DQ-040 references (the account key matches loan_account) and DQ-041 lists of values; above 0.50 percent the load is refused.

Two more automatic checks, with a tolerance instead of a hard stop. DQ-040 looks up each record's account key in loan_account.account_no, and DQ-041 looks up each action code and call result in the code maps for LOV-ACTION-CODE and LOV-CONTACT-RESULT. A record that fails either check is held rather than loaded. The step counts the held records as a share of the records read: at or below 0.50 percent the rest of the load continues, above that the whole load is refused. AC5 shows 40 of 9,450 records at 0.42 percent passing this rule, with 9,410 rows written and 40 records held.

### Step 5

**In the story.** System: skips records whose action code is not in the named list and counts them.

Automatic, inside the same step. The named list is the parameter efs.history.action.codes, which the business lead owns and the center of excellence analyst loads. Read it from the parameter catalog and keep only records whose action code appears in it. A skipped record is not the same as a held record: no dq_exception row is written for it, and only the count matters. Write that count to the load_run check results under SKIPPED_ACTION_CODE, as AC7 shows with 120 records carrying action code SYS01. Keep the list out of Java code, because it has to change without a release when the business lead names the codes.

### Step 6

**In the story.** System: maps the remaining records and inserts collections_history rows by their EFS record key in one transaction; a key already held is not inserted again.

Your step calls SourceMappingService to turn each COLLINS staging record into a CollectionsHistory entity, using mapping version EFS-MAP-1 and the two code maps. CollectionsHistoryRepository then inserts the rows with ON CONFLICT (efs_record_key) DO NOTHING, so a record key already in the table is left alone and counted as REPEATED. The column efs_record_key is unique in migration V1_004__collections_history.sql, which is what makes that work. One transaction means the database applies every insert of the run together or none of them, so a failure part way through leaves no half-loaded day of history. Free-text notes are not mapped; only codes, dates and amounts.

### Step 7

**In the story.** System: writes held records to dq_exception, runs DQ-042 movement, calls `FreshnessStampService.recordLoad` for DP05 in the same transaction, sets the status COMPLETED and publishes LoadCompleted.

All of this runs in the same step and the same transaction as the inserts. Write one dq_exception row for each held record with its check code, record key and the time raised, carrying the account key and nothing more, because personal data is kept out. Run DQ-042, the movement check, over the loaded rows. Call FreshnessStampService.recordLoad from RWB-E1-015 for data product DP05, so data_product_load holds the product code, the business date, the extraction time and the load time. Then set the load_run status to COMPLETED with rows read, loaded and held, and put the LoadCompleted event in the outbox with source INT-07.

### Step 8

**In the story.** System: the case list step of JOB-04 reads the latest contact per case from collections_history and writes it to case_list_row.

This runs in JOB-04, not JOB-01, and again with no person involved. Write CaseListLastContactEnricher and add it to the existing case list step. For each case it takes the latest contact_at across every account linked to that case, which is why the migration adds the index on (account_no, contact_at desc), and writes last_contact_at and last_action_code to case_list_row. The same migration adds those two columns to case_list_row. The team manager then sees the latest contact on the Power BI case list, as AC1 shows for case RW-2026-000123 with last contact 2026-11-30 15:42 and action code PTP.

### Step 9

**In the story.** System: at 08:00, if INT-07 is not COMPLETED, marks the load LATE and publishes LoadRefused with failed check LATE; the freshness check of RWB-E1-015 marks DP05 stale and alerts the data steward.

Write EfsWindowCheck as a separate Quartz trigger that fires at the window end held in the parameter load.window.end.INT-07, which is 08:00. No person runs it. It reads the INT-07 load_run for the business date, and when the status is not COMPLETED it sets LATE and puts a LoadRefused event in the outbox with failed check LATE. It writes nothing to collections_history, so the previous day of history stays in place with its own freshness stamp. The freshness check built in RWB-E1-015 then turns DP05 stale and sends MSG-P1-001 to the data steward group.

## RWB-E1-005 Excel and SharePoint inventory

Module: P1 Recovery data engine

### Step 1

**In the story.** Data steward: fills the inventory template, one row per tracker, with the decision and reason for each.

A person does this outside the Workbench. The data steward collects one row per tracker from the six team managers and fills the inventory template. Your part is the column set the loader will read: tracker_code, team_code, tracker_name, location_type, location_ref, owner_user_id, field_list, update_cycle, target_product, decision and decision_reason. Every row carries both a decision and the reason for it, because the handler refuses a row that has one without the other. The field_list column holds field names with a personal data tag, never field values. No code runs at this point, so build nothing for it beyond accepting that column set in the parser.

### Step 2

**In the story.** Reference data administrator: loads the file through `POST /admin/reference-loads` with table code `tracker_inventory`, version "TRK-2026.11" and valid from 2026-11-16.

The reference data administrator uploads the file. The endpoint POST /admin/reference-loads already exists from RWB-E1-043, so you write no controller here; you supply the handler it calls for table code tracker_inventory. The request carries the file, the table code and the valid-from date of 2026-11-16. The load service recognizes a repeated file by its hash, which makes the call idempotent: sending the same file twice changes nothing and answers 409 with MSG-P1-011 instead of writing a second set of rows. The administrator who loads the file may not confirm it, so this call only submits the version for checking.

### Step 3

**In the story.** System: `TrackerInventoryHandler.validate` checks every row: required fields, list values, a unique tracker code, a target data product for each LOAD decision, and at least one row for each of the six teams.

The checks run on their own inside code you write. TrackerInventoryHandler implements the ReferenceTableHandler interface whose signature comes from RWB-E1-001, and its validate method reads every row of the file before anything is written. Check the required fields, the list values for location_type, update_cycle and decision, a tracker code that appears once per inventory version, a target_product naming a row in data_product for each LOAD decision, and team_code membership of LOV-TEAM through the P4 published interface. Last, count the rows per team against the parameter tracker.inventory.teams, which holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. Unit test each check with a failing row.

### Step 4

**In the story.** System: refuses the whole file and returns the row errors if any check fails.

This is the whole-file rule, and it happens automatically when any check in validate fails. Write no row at all, including the rows that passed, and answer 422 with one entry per failing row in the detail field: MSG-GEN-001 for an empty required field, MSG-P1-007 for a value outside its list, MSG-P1-016 for a team with no row, MSG-P1-017 for a repeated tracker code. Each entry names the row number and the field, so the data steward can correct the file in one pass. The inventory version already in force keeps its rows and keeps serving reads while the file is corrected.

### Step 5

**In the story.** Data steward: confirms the version as its owner through the reference data change process.

A version does not take effect because the administrator uploaded it. The data steward, who owns the tracker inventory, has to confirm it first. That two-person flow is the reference data change process built in RWB-E1-043: one person loads the file, a different person confirms it, and both actions are recorded. The separation of duty rule in section 10 means your code must refuse a confirmation from the same user who loaded the version. Until the confirmation arrives, the rows are not applied and GET /admin/trackers keeps returning the previous version.

### Step 6

**In the story.** System: `TrackerInventoryHandler.apply` writes the rows in one transaction; a tracker already in the previous version keeps its status; a new tracker gets status LISTED, or KEPT for a KEEP decision.

Once the confirmation arrives, the apply method of your handler writes the rows. Run the whole write inside one transaction, which is a single unit of database work that either completes for every row or leaves the table as it was, so a failure halfway through cannot leave part of version TRK-2026.11 in tracker_inventory. For each row, look up the tracker code in the previous version. A tracker already there keeps the status it had. A tracker new to the inventory gets status LISTED, or KEPT when its decision is KEEP. The column check limits status to LISTED, LOADED, SIGNED_OFF, RETIRED and KEPT.

### Step 7

**In the story.** Data steward or team manager: calls `GET /admin/trackers?team=LIT` and reads the trackers of the team with owner, fields, update cycle, decision and status.

A person calls this, and you build both the service and the endpoint. GET /admin/trackers takes optional team, decision and status filters and returns Tracker objects with id, trackerCode, team, name, locationType, locationRef, ownerUserId, fields with their personal tag, updateCycle, targetProduct, decision, decisionReason, status and inventoryVersion. TrackerService applies the filters and reads through the index on team_code and status. The caller needs the Reference data R right; without it answer 403 with MSG-P4-002, which is what the access test does with a partner user. For team LIT the response holds that team's trackers, among them LIT-07 with its owner and 18 fields.

## RWB-E1-006 Data quality rules v1

Module: P1 Recovery data engine

### Step 1

**In the story.** System: a load completes for a data product (for example INT-01 for DP01), or the case list step of JOB-04 completes for DP03.

Nobody starts this run by hand. It begins when a load step finishes. Your work is to call the runner from two places: the end of each load step in JOB-01 and JOB-09, and the end of the case list step of JOB-04 for data product DP03. The call is the internal method DataQualityRuleRunner.runFor with the product code and the load run ID of the step that has just finished, so each run knows which rules to read and which load to attach its results to. A data product is one named set of recovery data, for example DP01 for accounts and DP03 for the case list. The feature flag rwb.p1.dq-rules controls it; with the flag off, loads finish as before and no rule runs.

### Step 2

**In the story.** System: reads the dq_rule rows in force for that data product on the business date.

The runner takes its work from database rows and not from Java code. DqRuleRepository selects the dq_rule rows whose product_code matches the data product of this run and whose dates cover the business date: valid_from on or before it, and valid_to empty or on or after it. In force means approved and inside those dates. A rule whose valid to date has passed or whose valid from date is still in the future is left out, which is exception path X5, and it then appears nowhere in the load run results. Build step 1 in section 13 asks you to test this date query on its own, because every later step depends on reading the right set of rules for the right day.

### Step 3

**In the story.** System: builds the SQL for each rule from its rule type template and its parameters, using only table and column names that sys_fields holds for P1-owned tables.

Each rule row holds a rule type and parameters, so the runner has to turn the row into a SQL statement. RuleTypeTemplates holds one template per rule type, seven in all: NOT_NULL, UNIQUE_ACROSS, RANGE, SUM_EQUALS, EXISTS_LINK, MAX_AGE_DAYS and FIELD_BEFORE. The template supplies the shape of the statement. Table and column names come only from sys_fields, the data dictionary of the P1 owned tables, and the values in rule_params go in as bound parameters, which means the database receives them as values and never as text it executes. No rule text is run as SQL. A rule naming a field that sys_fields does not hold is refused at load time with MSG-P1-005, so the runner never meets one.

### Step 4

**In the story.** System: runs each rule and collects the failing records.

This happens inside the runner with no person present. DataQualityRuleRunner executes each built statement and keeps the records it returns, which are the rows that fail that rule. Each rule has a limit of 60 seconds. When one rule passes that limit or fails for another reason, the runner marks that rule as ERROR on the load run, carries on with the remaining rules, and alerts the data steward group with MSG-P1-015. One slow or broken rule therefore does not stop the others. Build step 4 in section 13 covers the per rule limit, the ERROR result and the clear step together, so write them as one service.

### Step 5

**In the story.** System: writes one dq_exception row per failing record with the rule code as check and reason code, the rule version, the record key and the business date.

The runner writes the failing records to dq_exception, one row per failing record, filling check_code and reason_code with the rule code, plus the rule version, the record key and the business date. The insert has to be idempotent, which means running it again gives the same result instead of a second row. The unique constraint uk_dq_exception on load_run_id, check_code and record_key gives you that, and DqExceptionRepository inserts with ON CONFLICT DO NOTHING, so a repeat of the same run adds nothing, which is exception path X4. record_key holds an account key or a record ID. Never put a name or a contact value in it.

### Step 6

**In the story.** System: sets CLEARED on any OPEN exception of the same rule and record that no longer fails.

An exception row carries a status. A row raised earlier is OPEN until the record passes its rule again, and the runner then sets that row to CLEARED with cleared_on set to the business date. It does this by matching the same rule code and the same record key. Nothing is deleted, so the history of the break stays readable. AC9 is the test: an OPEN DQ01 exception for case account ACC0000777 raised on 2026-11-27 becomes CLEARED with cleared_on 2026-11-30 once the case has an owner. The cleared_on column is new and comes with the rule_version column in migration V1_006__dq_rule.sql.

### Step 7

**In the story.** System: writes the count per rule to the load_run check results.

The runner also writes a count for each rule it ran into check_results on the load_run row, which is the record of that load. This is what the data steward reads to see how many records failed each rule, for example DQ02 equal to 3 in AC1. A rule that failed at run time appears there as ERROR, and a rule outside its valid dates appears not at all, as AC8 states for DQ07. load_run already exists from RWB-E1-003, so you add content to check_results and create no table for this.

### Step 8

**In the story.** System: the JOB-04 publish step writes the open and new exceptions for the business date to the data lake extract for Power BI.

The daily reconciliation job JOB-04 has a publish step, and this story adds DataQualityExtractWriter to it. The writer selects the exceptions that are open and the ones raised on the business date, and writes them to the data lake extract, which is the file the reporting layer reads. Each row carries the rule code, the rule name, the data product, the business date and the record key, as AC2 requires with its 19 rows. No person triggers this. The reporting and BI analyst builds the Power BI data quality report on top of the extract and owns the report layout.

### Step 9

**In the story.** Data steward: reads the exceptions through GET /admin/data-quality/exceptions or the Power BI data quality report.

The data steward reads the result in one of two ways. The first is the endpoint GET /admin/data-quality/exceptions, which you build as a method on RecoveryDataEngineController with the query parameters product, from and to, returning id, product, check, record and raisedOn per row. The method needs the capability check for Platform administration R with scope All, so a role without it receives 403 with MSG-P4-002, as test TC-E1-006-10 asks. The second way is the Power BI data quality report built from the extract of step 8. The endpoint is read only and changes nothing in the data.

## RWB-E1-007 Integration adapters for file loads and outbound files

Module: P2 Integration

### Step 1

**In the story.** Scheduler: JOB-09 starts the file load for an inbound interface, for example INT-10 CCMS, at its time.

Nobody presses a button here. Quartz, the scheduler that runs inside the ACE service, fires JOB-09 on its own clock. You build FileLoadJob as the entry point and give it one run per interface, so INT-10 CCMS is one run and INT-11 SVAF is another. Section 12 gives the times: weekly on Monday at 04:00 for CCMS, SVAF, RPS and WIN, and monthly on the second working day for AMIS and GL. The job itself holds no file logic. It reads which interface it is running for and calls FileLoadAdapter.run with that interface ID and the business date.

### Step 2

**In the story.** SY-DATALOAD: the FileLoadAdapter reads the interface configuration row in force and lists the inbound folder for the file pattern and business date.

This runs automatically, under the service identity SY-DATALOAD, which is the Entra ID managed identity the load code runs as. Build FileLoadAdapterImpl. It first reads the interface_config row for that interface whose valid_from and valid_to cover the business date. In force means exactly that date test, because several versions of a row can exist at once. From the row it takes inbound_path and file_pattern, then lists that folder for a file whose name matches the pattern for the business date. The folder is reached over SFTP, and only SftpTransport may open the connection, with credentials read from the key store. No folder path and no file name belongs in your code.

### Step 3

**In the story.** SY-DATALOAD: the adapter writes an interface_run row with status RECEIVED, the file name, the file hash and the business date.

The adapter does this with no person involved. Build the InterfaceRun entity and InterfaceRunRepository, and have the adapter insert one row for each file it finds, with status RECEIVED, the file name, the file hash and the business date. The hash is a short fingerprint computed from the file content, so the same bytes always give the same value. The migration V2026_11_07__p2_adapter_tables.sql puts a unique constraint on (interface_id, business_date, file_hash). A unique constraint is a database rule that refuses a second row carrying the same three values, which is how the repeat delivery in exception path X5 is caught instead of being loaded twice.

### Step 4

**In the story.** SY-DATALOAD: the adapter runs the file checks held as data (business date, structure, control total, keys) against the header and trailer.

Automatic, and the work goes into FileCheckRunner. It reads the load check rows for the interface, DQ-057 to DQ-063 for INT-10 CCMS and DQ-085 to DQ-091 for INT-15 WIN, and runs four kinds of check: business date, structure, control total and keys. The values the checks compare against come from the file's own header and trailer lines, which are the first and last lines of the file and carry the business date and the record count or total. Write one test per check type against synthetic header and trailer files. No tolerance and no expected total goes into code; every one of them is a table row.

### Step 5

**In the story.** SY-DATALOAD: when every file check passes, the adapter hands the records to the owning module's loader through its published interface and sets the run to LOADED with the record count.

Still automatic. Only when every check has passed does the adapter pass any record on, which is what acceptance criterion AC4 tests. The adapter never writes into another module's tables. It calls RecordLoader.load, the interface in recovery.integration.adapter.api that the owning module implements, for example the P1 collateral loader for collateral records. A published interface is a Java type the other module depends on, so your package does not need to know its tables. The adapter then updates the interface_run row to status LOADED and stores the number of records it handed over. The loader, not P2, publishes LoadCompleted (EV-26) or LoadRefused (EV-27).

### Step 6

**In the story.** Owning module: writes an outbound file request through OutboundFiles.enqueue, for example JOB-10 for the daily WIN notice file (INT-14).

Here the direction turns around. The calling code is not yours: the module that owns the content calls OutboundFiles.enqueue and passes an OutboundFileRequest holding the interface ID, an idempotency key, a reference to the payload and the case IDs. For INT-14 that caller is JOB-10, which Quartz runs daily at 16:00 and which takes the approved notices from P6. What you build is the method they call, OutboundFilesImpl. Keep the request type as section 12 defines it, and let no customer name and no address into it. Outbound items carry case IDs only.

### Step 7

**In the story.** SY-DATALOAD: the adapter writes one outbound_item with an idempotency key, in the same transaction as the request.

OutboundFilesImpl writes the row itself, with no separate job in between. Write it inside the caller's transaction. A transaction is one unit of database work that either completes in full or is undone in full, so the caller's own changes and this outbound_item row live or die together, and no file is ever queued for work that was rolled back. The row carries an idempotency key, a value that identifies the request so a repeat cannot create a second item. For INT-14 the key is "INT-14:" plus the business date. The migration puts a unique constraint on idempotency_key, which is what makes a second run for the same date add nothing.

### Step 8

**In the story.** Scheduler: JOB-11 runs every minute; the OutboundSender sends each due item over SFTP and marks it SENT, then ACKNOWLEDGED when the acknowledgment file arrives.

Quartz starts JOB-11 every minute without anyone asking. Build OutboundSender. It reads outbound_item rows whose status is PENDING or RETRY and whose next_attempt_at is at or before now, using FOR UPDATE SKIP LOCKED. That clause locks the rows this run takes and lets a second run step over them instead of waiting, which is how two sender instances avoid sending one file twice. Sending goes through SftpTransport. On a good transfer the item becomes SENT. ACKNOWLEDGED comes later, when the acknowledgment file for that transfer arrives. An item left in SENT without an acknowledgment after 30 minutes is sent again.

### Step 9

**In the story.** SY-DATALOAD: on a transfer failure, the sender raises SYSTEM_UNAVAILABLE for each case in the file and schedules the next attempt from the retry intervals.

The sender does both parts on its own. For every case ID on the item it calls CaseEvents.raise with SYSTEM_UNAVAILABLE through the P3 interface. P3, not your code, moves each case's route state to RETRY_QUEUE, and the case status in recovery_case does not change at all. The sender then sets next_attempt_at from retry_intervals_min on the interface_config row, so for INT-14 the second attempt falls 5 minutes after the first and the third 15 minutes after the second. The user sees MSG-GEN-006. Read the intervals and max_attempts from the row on every run. Neither number is allowed in code.

### Step 10

**In the story.** SY-DATALOAD: after the last allowed attempt fails, the sender sets the item to EXCEPTION, raises OUTBOUND_FAILED for each case and a task for the owner role, and logs MSG-P2-001.

Automatic, and it is the end of the retry path. When the attempt count reaches max_attempts from the configuration row, OutboundSender sets the item status to EXCEPTION. It then calls the P3 interface twice for the cases on that item: CaseEvents.raise with OUTBOUND_FAILED, which moves each case to route state EXCEPTION_QUEUE, and TaskApi.raiseTask to create the task for the role in owner_role, which is RW-PLATADM for INT-14. It logs MSG-P2-001, naming the interface, the file and the attempt count. The item then appears on SCR-09 Exception queue, where a platform administrator can resend it through POST /admin/outbound-items/{itemId}/resend.

### Step 11

**In the story.** SY-DATALOAD: every consumer of an application event checks the idempotency key through IdempotencyGuard before it acts.

This one changes code you do not own. Idempotent means the same event delivered twice has the same effect as delivering it once. Build IdempotencyGuardImpl, then put the check into every event listener in the recovery module through one shared base listener, so no squad has to remember it. The guard inserts a row into processed_event, whose primary key is (consumer, idempotency_key). A primary key is the set of columns that must be unique in a table, so a second insert for the same consumer and key cannot succeed. On that conflict the guard increases hit_count and returns false, and the listener returns without acting.

## RWB-E1-008 Decision log store v1, append only and hash chained

Module: P7 Decision center and log

### Step 1

**In the story.** Writer (SY-DECLOG, built in RWB-E1-027): calls DecisionLogStore.append with a validated record inside the caller's transaction, as its last statement.

No person does this. The decision log writer, service identity SY-DECLOG from RWB-E1-027, calls your append method. You build DecisionLogStore in the Java package recovery.decision.log with the method append(DecisionLogRecord record) from section 12, declared to throw DecisionLogUnavailableException. Only the writer calls it; other modules reach the log through the writer. The call runs inside the caller's own transaction. A transaction is one group of database statements that either all take effect or none do. BR5 puts the append as the last statement of that group, so the business action and its entry commit together. Do not open your own transaction inside append and do not commit there.

### Step 2

**In the story.** Store (DecisionLogStore): takes the chain lock (a PostgreSQL transaction advisory lock on the key "decision_log_chain").

Your store code takes the lock; the database does not do it for you. Use a PostgreSQL transaction advisory lock on the key "decision_log_chain". An advisory lock is a lock the application asks for by a name of its own choosing, and the database does not attach it to any row or table; a transaction-level one is released when the transaction ends. It makes the appends line up one after another, so two writers cannot read the same last entry and give two entries the same chain_seq. AC5 is the test: entries after chain_seq 50 take 51 and 52, and the prev_hash of 52 equals the entry_hash of 51.

### Step 3

**In the story.** Store: reads the chain_seq and entry_hash of the last entry; sets chain_seq to last plus 1 and prev_hash to the last entry_hash, or 64 zeros for the first entry.

Still inside append, the store reads the last stored entry and works out the two chain columns. chain_seq is the last value plus one, and prev_hash is the entry_hash of that last entry. For the very first entry there is nothing before it, so prev_hash takes 64 zeros. Read that value from the property rwb.decision.chain.genesis-hash rather than writing it into the code, as section 13 requires. The migration V_E1_008__declog_chain.sql adds chain_seq as bigint not null unique, so a repeated value is refused by the database itself. AC2 checks that the first prev_hash is 64 zeros and that each later prev_hash matches the entry before it.

### Step 4

**In the story.** Store: builds the canonical form of the entry and sets entry_hash to its SHA-256 in lower-case hexadecimal.

The store builds the canonical form and hashes it. A canonical form is one fixed way of writing the entry as text, so the same entry always produces the same hash. BR4 sets it: every field of the entry except entry_hash and the standard columns, as JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers written as strings and empty fields as null. SHA-256 turns that text into a fixed value, which you write as lower-case hexadecimal. Build this once as CanonicalEntryForm and use the same class in the verifier. Check golden test vectors into the test resources, a fixed entry with its expected hash.

### Step 5

**In the story.** Store: inserts the row; the caller's transaction commits the action and the entry together and releases the lock.

The insert is the only write the store makes. Use DecisionCenterAndLogRepository, which has no update and no delete method. Your code does not commit; the caller's transaction does, and it covers both the business action and this entry, so the two are kept together or not at all. The transaction advisory lock from step 2 ends with that commit, which lets the next writer read the new last entry. AC7 tests the other direction: when the append fails inside a transaction that also changes the case owner, no entry is stored, the case owner is unchanged and no chain_seq is used up.

### Step 6

**In the story.** Store: on any failure, raises DecisionLogUnavailableException; the caller's transaction rolls back and the action does not happen.

The store catches any failure of the lock, the read, the hash or the insert and throws DecisionLogUnavailableException, which section 12 declares on the append method. Do not swallow the error and do not let the caller carry on. Because the append sits inside the caller's transaction, that throw rolls the whole transaction back, so the business action is undone with it. The caller then shows MSG-P7-003, which tells the user the action was not taken because the decision could not be recorded and to try again in a few minutes. This is exception path X5 and acceptance criterion AC7.

### Step 7

**In the story.** Database: refuses any UPDATE or DELETE on decision_log_entry through tr_declog_append_only; the ACE service writes the refused attempt to the ACE audit and SOC log.

The database stops this, not your Java code. The trigger tr_declog_append_only already exists from RWB-E1-001. A trigger is code the database runs by itself when a statement touches a table, and this one refuses the statement with the text "decision_log_entry is append only". Your migration also revokes UPDATE and DELETE on decision_log_entry from the service role, so the service role is refused by the missing grant and the schema owner is refused by the trigger. Confirm both paths in the migration test, which is build step 1. The ACE service writes each refused attempt to the ACE audit and SOC log with the table, the operation and the entry ID, as AC1 requires.

### Step 8

**In the story.** Verifier (HashChainVerifier): reads entries in chain_seq order over a range, recomputes each entry_hash and checks each prev_hash against the entry before it.

You build HashChainVerifier with the method verify(fromSeq, toSeq) from section 12. It reads the entries in chain_seq order across the range, in batches of 1,000 as section 13 requires, rebuilds each entry's canonical form with the same CanonicalEntryForm class the store uses, recomputes the SHA-256 and compares it with the stored entry_hash. It also checks that each prev_hash equals the entry_hash of the entry before it. Nothing calls it on a schedule in this story; the nightly run and its daily report are RWB-TE-008. AC2 runs it over 100 entries and AC4 over 10,000 entries with one of them changed in the DEV database.

### Step 9

**In the story.** Verifier: returns the result with the count checked, the last chain_seq and its entry_hash; on a break, it names the first entry that fails, raises an incident and sends MSG-P7-008 to Compliance within 15 minutes.

verify returns ChainCheckResult holding the count checked, lastSeq, lastHash, breakSeq and breakEntryId. When every hash matches, the break fields stay empty. When one does not, the first entry in chain_seq order that fails is named, and your code calls ChainBreakNotifier, which raises the incident on the ACE incident path and sends MSG-P7-008 to the Compliance group through the ACE notification path. The notification group is configuration, not a value in code. BR6 and AC4 set the time limit: Compliance is told within 15 minutes of the run start. AC4 expects chain_seq 7,412 and its entry ID reported as the first break.

## RWB-E1-009 CCMS and SVAF loads

Module: P1 Recovery data engine

### Step 1

**In the story.** File adapter (P2): JOB-09 receives the CCMS file for the week, passes its file checks, and calls `CcmsCollateralLoader.load("INT-10", businessDate, records)`.

No person starts this load. JOB-09 File loads in the P2 adapter runs weekly on Monday at 04:00, or when the file arrives after its due time. The adapter has already run the business date, structure, control total and key checks built in RWB-E1-007, and it refuses a file it has loaded before. Your work here is the receiving side. Write CcmsCollateralLoader in package recovery.dataengine.load.ccms as an implementation of the P2 interface RecordLoader, typed to CcmsCollateralRecord. The adapter hands it the interface ID INT-10, the business date and a stream of checked records. A stream delivers the records one at a time, so you never hold the whole weekly file in memory. The loader runs under the service identity SY-DATALOAD.

### Step 2

**In the story.** System: opens a load_run for INT-10 with the interface_run reference.

The loader does this itself, at the start of the call. Insert a load_run row, the table built in RWB-E1-003, with interface_id INT-10, the job code, the business date, status RUNNING and interface_run_id set to the adapter interface run that passed you the records. Migration V1_009 adds interface_run_id to load_run with a unique index on it. That index is what makes the loader idempotent. Idempotent means a second call for the same interface run has no further effect, because the insert cannot succeed twice, and you return the outcome of the completed run instead. Fill rows_read, rows_loaded, rows_held and check_results on the same row as the load proceeds.

### Step 3

**In the story.** System: runs DQ-061 references (each account link matches loan_account) and DQ-062 lists of values; above 0.50 percent the file is refused.

The loader runs these checks itself, through the LoadCheckRunner of RWB-E1-003, once the load_run is open. DQ-061 is a reference check: every account link in the file must name an account key that already exists in loan_account. DQ-062 checks each coded value against the approved code maps for LOV-COLL-TYPE, LOV-PROVINCE and LOV-APPRAISAL. A record that fails is held, which means it is not written and a dq_exception row carries the check code and the record key. Compare the held count with the parameter load.hold.tolerance.pct, which is 0.50 percent. At 0.36 percent the rest of the file loads. At 0.54 percent refuse the whole file, publish LoadRefused and send MSG-P1-002 to the data steward group.

### Step 4

**In the story.** System: upserts collateral by collateral_no and replaces the account_collateral links of each loaded collateral, in one transaction.

The loader writes the collateral data with no person involved. Upsert means insert a row when collateral_no is new and update the existing row when it is already there; the unique key uk_collateral_no added by migration V1_009 is what lets the database decide which of the two applies. Two fields are left alone on update, occupancy and encumbrance_status, because the Workbench owns them. For each collateral in the file, remove its existing account_collateral links and insert the links from the file, under uk_account_collateral on account_id and collateral_id. Do all of this in one transaction, so either every write of the batch is kept or none is, and a half loaded week cannot be left behind.

### Step 5

**In the story.** System: runs DQ-063 movement, calls `FreshnessStampService.recordLoad` for DP06, sets COMPLETED, publishes LoadCompleted and returns the LoadOutcome to the adapter.

Still the loader, with no person involved. DQ-063 compares the counts and values of this week with the previous load and fails when the movement is larger than load.movement.tolerance.pct, which is 10.00. Then call FreshnessStampService.recordLoad from RWB-E1-015, which writes a data_product_load row for product DP06 with the business date and the load time; the freshness check of that story marks DP06 stale when no file has arrived. Set the load_run status to COMPLETED, write the LoadCompleted event EV-26 to the outbox, and return a LoadOutcome to the adapter carrying the status, rows read, rows loaded, rows held and any failed check.

### Step 6

**In the story.** File adapter (P2): after INT-10, calls `SvafAppraisalLoader.load("INT-11", businessDate, records)` for the SVAF file.

The adapter drives this, not a person, and the order is fixed: INT-10 first, then INT-11. Write SvafAppraisalLoader in package recovery.dataengine.load.svaf as a second implementation of RecordLoader, typed to SvafAppraisalRecord, and connect it to JOB-09 the same way as the CCMS loader. The order matters because DQ-068 checks that each appraisal names a collateral already in DP06, so the collateral from the CCMS file has to be written first. When the adapter refused the CCMS file at one of its own checks, the CCMS loader is never called, the collateral keeps the previous week, and the SVAF file still loads with the affected appraisals held under DQ-068.

### Step 7

**In the story.** System: opens a load_run for INT-11 and runs DQ-068 references (each appraisal names a collateral in DP06) and DQ-069 lists of values.

The SVAF loader does this itself. Open a second load_run row with interface_id INT-11, its own interface run reference and status RUNNING, exactly as the CCMS loader does for INT-10. The two loads are separate runs with separate statuses, so one can complete while the other is refused. Then run DQ-068, a reference check that every appraisal names a collateral number present in the collateral data of DP06, and DQ-069, which checks the coded values on each appraisal against the approved code maps. Rows that fail are held in dq_exception with the check code, and the held count is compared with load.hold.tolerance.pct in the same way as INT-10. Four appraisals naming unknown collateral are held and the other 2,136 load.

### Step 8

**In the story.** System: for each appraisal, computes the age in days at the file's business date and sets the stale flag when the age is above `appraisal.max.age`.

Build AppraisalAgeCalculator for this, and it runs inside the loader with no person involved. For each appraisal, take the number of whole days from the appraisal date to the business date of the file, write it to the new valuation column age_days, and set stale_flag true when that number is above the parameter appraisal.max.age, which is 365. The boundary is exact: 366 days gives stale_flag true and 365 days gives false. Appraisal dates arrive in Buddhist Era years, so convert them first; 15/03/2569 in the file is stored as 2026-03-15. Migration V1_009 adds stale_flag, a boolean not null with default false, and age_days as an integer.

### Step 9

**In the story.** System: writes the appraisals through `ValuationRecordApi.upsertAppraisals` in the same transaction as the load_run status; runs DQ-070 movement and the sample check; stamps DP06; publishes LoadCompleted.

The loader does this, in one unit of work. Call ValuationRecordApi.upsertAppraisals with the appraisal records and the load run ID. That interface is published by S1 and you build it in this story, with its JPA writer in package recovery.valuation; it inserts or updates by appraisal_no under the new unique key and runs inside the transaction of the caller, so the appraisal writes and the load_run status commit together. When the write fails after 1,000 of 2,140 rows, the transaction rolls back, no appraisal is stored, the status is FAILED and the platform administrator reruns the load. Then run DQ-070 movement and the sample check over 50 cases with collateral, stamp DP06 and publish LoadCompleted.

## RWB-E1-010 Excel and SharePoint loads

Module: P1 Recovery data engine

### Step 1

**In the story.** Data steward: calls `POST /admin/trackers/{trackerId}/loads` with the tracker file.

A person starts this. The data steward sends the exported tracker file to the new endpoint POST /admin/trackers/{trackerId}/loads. Build it as multipart/form-data with one part named file, accepting .xlsx or .csv of at most 20 MB, plus an Idempotency-Key header. Idempotency-Key means the same request sent twice has the effect of one request, so a retry after a dropped connection does not load the file a second time. The controller is TrackerLoadController in package recovery.dataengine.tracker, and the caller needs Reference data U. A role without that right gets 403 with MSG-P4-002. Epic 1 has no screen for this, so the steward calls the endpoint through an API client.

### Step 2

**In the story.** System: checks the tracker has decision LOAD and status LISTED or LOADED, the file type, and that the file hash has not been loaded before.

This happens on its own in TrackerLoadService, before anything is stored. There are three pre-checks. Read the tracker_inventory row and refuse unless its decision is LOAD and its status is LISTED or LOADED, with 409 and MSG-P1-010. Refuse a file that is not .xlsx or .csv with 415 and MSG-P1-018, and one above 20 MB with 413. Compute the SHA-256 hash of the file content and refuse when a load_run for this tracker already carries that hash, with 409 and MSG-P1-011. A hash is a short fingerprint of the content, so the same file uploaded twice gives the same value. The unique index on tracker_id and source_file_hash in migration V1_010 backs that check. A failed check stores nothing.

### Step 3

**In the story.** System: stores the file in the write-once tracker file store, opens a load_run for the tracker and returns 202 with the Job.

This runs on its own. TrackerFileStore writes the uploaded file to the write-once container through the ACE storage pattern and returns its reference and hash. Write-once means the content can never be changed or deleted, which keeps the file as the read-only archive copy. Hold the reference in tracker_inventory.source_file_ref. TrackerLoadService then inserts a load_run row with the tracker ID, the source file name, the hash, loaded_by and its status, and launches the Spring Batch job trackerLoadJob. The response is 202 with a Job of type TRACKER and status RUNNING, so the caller does not wait for the rows to be written. The upload launches the job, and it has no place in the daily timeline.

### Step 4

**In the story.** System: checks that the header columns match the field list; a mismatch refuses the file.

This runs on its own inside TrackerFileReader. Read the header row of the file and compare the column names with the field_list held on the tracker_inventory row, loaded by RWB-E1-005. Read .xlsx with Apache POI streaming so a large file does not fill memory, and .csv with a plain reader. When a column named in the field list is missing, for example Court name, refuse the load at structure with MSG-P1-002 and write no tracker_row at all. The rows of the previous load of that tracker keep their place and stay in use. The field list is data per tracker, so never put the column names in code.

### Step 5

**In the story.** System: for each row, rejects it if the account number is empty (TRK-01) or not in loan_account (TRK-02), and writes the rejection to dq_exception with the row number.

This runs on its own inside trackerLoadJob, which you build as TrackerLoadJobConfig. For every data row, take the account number. An empty value gives check code TRK-01. A value with no matching account_no in loan_account, the table loaded by RWB-E1-003, gives TRK-02. Write one dq_exception row for each rejected row holding the check code, the reason code, the time raised and a record key built from the tracker code and the row number, for example LIT-07 row 14. Nothing else identifies the row, which keeps personal data out of the exception table. A rejected row is never written to tracker_row, and every other row in the file still loads.

### Step 6

**In the story.** System: drops every field tagged as personal data and writes the other fields of each accepted row to tracker_row with the target data product, the file name and the row number, in one transaction; rows of an earlier load of the same tracker are replaced.

This runs on its own. For each accepted row, remove the fields that the inventory field list tags as personal, then write the remaining values into tracker_row.field_values as jsonb together with tracker_id, load_run_id, row_no, account_no, target_product, source_file_name and loaded_on. TrackerRowRepository deletes the tracker's earlier rows and inserts the new ones in one transaction, so either both happen or neither does and the table never holds rows from two files at once. Count the dropped personal fields on the load_run check results as DROPPED_PERSONAL_FIELDS. Create tracker_row with its indexes on tracker_id and account_no in migration V1_010__tracker_row.sql.

### Step 7

**In the story.** System: sets the file rows, loaded rows and rejected rows on the tracker, sets status LOADED and sends MSG-P1-008 to the data steward and the team manager.

This runs on its own at the end of the job. Write file_rows, loaded_rows, rejected_rows and last_load_run_id on the tracker_inventory row, and move its status to LOADED. When this file replaces an earlier load that was never signed off, set that earlier load_run to SUPERSEDED, a status value that migration V1_010 adds. Then send MSG-P1-008 through the ACE notification path to the data steward who uploaded the file and to the team manager of the tracker's team, naming the loaded count, the file name and the rejected count. The counts have to be written before the message goes out, because the team manager confirms them in the next step.

### Step 8

**In the story.** Team manager: calls `POST /admin/trackers/{trackerId}/sign-off` with the row count of the file the team knows.

A second person acts here. The team manager of the tracker's team sends POST /admin/trackers/{trackerId}/sign-off with confirmedFileRows and an optional comment of up to 400 characters. Build the endpoint to require Queue and allocation A with Team scope. A missing count is 400 with MSG-GEN-001. A repeated sign-off of a tracker already SIGNED_OFF by the same user returns 200 with the same Tracker, so the caller can retry safely. The number must be the team's own count of the rows in their file, taken from what the team knows rather than from the figures the load produced.

### Step 9

**In the story.** System: checks the signer is not the person who loaded the file, belongs to the tracker's team, and that the confirmed count equals the file rows, which equal loaded plus rejected rows.

This runs on its own inside TrackerSignOffService, as three checks. Compare the signer with load_run.loaded_by and refuse with 409 and MSG-P7-002 when they are the same person. That is the separation of duty rule: nobody approves work they prepared themselves. Compare the signer's team with tracker_inventory.team_code and refuse a manager of another team with 403 and MSG-P4-002. Compare confirmedFileRows with file_rows and refuse with 409 and MSG-P1-009 when they differ, naming the confirmed, file, loaded and rejected counts. The tracker status stays LOADED after any refusal. Loaded plus rejected rows always equal the file rows, so one comparison covers the whole reconciliation.

### Step 10

**In the story.** System: sets status SIGNED_OFF with the signer and the time.

This runs on its own once the three checks pass. Write signed_off_by with the signer's user ID and signed_off_at with the time, and move tracker_inventory.status to SIGNED_OFF. Do the write under an optimistic lock on the record version, so when somebody else changed the tracker row between the read and the write the call fails with 409 and MSG-GEN-004 instead of overwriting their change. The response is 200 with the Tracker holding the new status, signedOffBy and signedOffAt. SIGNED_OFF is the state that RWB-E1-012 needs before a team retires its local copy, and no further file is accepted for the tracker.

## RWB-E1-011 Reconciliation and data quality report

Module: P1 Recovery data engine

### Step 1

**In the story.** System: JOB-04 Daily reconciliation runs its reconciliation step after the case list step for the business date.

No person starts this. JOB-04 is a scheduled batch job, and you add a new step to it. A step is one unit of work inside a job, and Spring Batch runs the steps in the order the job defines. Build ReconciliationStepConfig in the package recovery.dataengine.recon and place it after the case list step and before the publish step. The step takes the business date from the job parameters, so every row it writes carries that one date. The job runs as the service identity SY-DATALOAD, so your step needs no user session. Add the checks REC-01 and REC-02 to the JOB-04 job mapping as well, so GET /admin/jobs reports them per product.

### Step 2

**In the story.** System: checks through `LoadRunQuery` that the INT-01 load for the business date is COMPLETED.

The step makes this check itself; nobody confirms it by hand. Call LoadRunQuery, the published read interface from RWB-E1-003, with interface INT-01 and the business date, and read the status on the load_run row. Only the value COMPLETED lets the work go on. When the status is anything else, write no reconciliation_result row for that date, report every product as not run with MSG-P1-001 as the reason, and leave the case list publish held. This path is build step 5 in the solution plan. Reading another module's load table directly is not allowed, so the interface call is the only way to the status.

### Step 3

**In the story.** System: for each product group, counts the ALS accounts at or above 90 days past due less the accounts excluded at entry, and the case list rows at or above 90 days past due (REC-01).

ReconciliationService does this arithmetic once per product group, with no user involved. On the ALS side, count loan_account rows whose days_past_due is 90 or more, taking the 90 from the parameter case.entry.dpd rather than from code, then subtract the accounts that were excluded when cases were created. Those exclusion counts come from CaseQueryApi.excludedAccountsByProduct(businessDate), the P3 interface this story extends; do not query P3 tables for them. On the Workbench side, count case_list_row rows at the same days past due. Hold both numbers per product group, because each product gets its own result row and its own grade on the report.

### Step 4

**In the story.** System: for each product group, sums total_balance on both sides (REC-02).

The same service method runs the second comparison automatically, inside the same step. Sum total_balance over the ALS accounts you selected for REC-01, and sum total_balance over the matching case_list_row rows, again per product group. Store the two sums as source_amount and workbench_amount, both numeric(18,2), so the money values keep two decimal places and nothing is rounded away. REC-02 uses the same product grouping and the same days past due filter as REC-01, so the two results for one product always describe the same set of accounts and a reader can compare them.

### Step 5

**In the story.** System: computes the variance and the variance percent and compares it with the tolerance; writes one reconciliation_result per reconciliation and product.

The service computes variance_count and variance_pct, reads recon.tolerance.pct for that reconciliation from the parameter catalog, and sets result to PASS or BREAK. A variance above the tolerance is a break; a variance equal to the tolerance passes. Write the tolerance you used into tolerance_pct on the row, so a later reader sees which limit applied that day. Migration V1_011__reconciliation_result.sql creates the table with a unique constraint on rec_code, business_date and product_group. A unique constraint is a database rule that refuses a second row carrying the same three values, which is how two job runs on two nodes still leave six rows. ReconciliationResultRepository replaces all results for one date when the step runs again.

### Step 6

**In the story.** System: writes one dq_exception per account that breaks, with check code REC-01 and the account number: in ALS and not on the case list, or on the case list and not in ALS.

The step writes these rows itself. Compare the two sets of account numbers in both directions and write one dq_exception row for every account that appears on one side only. Set check_code to REC-01, put the account number in record_key, set raised_on to the business date and status to OPEN. Nothing else about the customer belongs in the row. When a later run for the same date passes, set those rows to CLEARED with cleared_on, which is build step 3. Only a role with Platform administration R may list the rows through GET /admin/data-quality/exceptions; others receive 403 with MSG-P4-002.

### Step 7

**In the story.** System: if every result is PASS, releases the case list extract for publish; if any is BREAK, holds the case list publish for the business date and alerts the data steward, the platform administrator and the team managers.

CaseListPublishGate makes this decision in code, with no approval by a person. Add publish_status to case_list_row with the values PENDING, HELD and RELEASED, and have the gate set HELD or RELEASED for the business date once all six results exist. Then change the publish step built in RWB-E1-002 so it writes the case list extract only when the status is RELEASED, which takes the place of the total count check that story used. On a break, LoadAlertNotifier from RWB-E1-003 sends MSG-P1-012 to the data steward, platform administrator and team manager groups, which are held as configuration. A held case list is never published by hand from here.

### Step 8

**In the story.** System: writes the reconciliation extract and the data quality extract to the data lake.

ReconciliationExtractWriter produces both files inside the job run. Write reconciliation/<businessDate>.csv and data-quality/<businessDate>.csv and send them to the data lake through the outbound adapter INT-19. Add both writes to the publish step so the files travel the same path as the case list extract. A run for the same date writes the files for that date again, matching the results you replaced. These two files are the only input the Power BI report reads, so every column the report shows has to be in them. This is build step 6 in the solution plan.

### Step 9

**In the story.** Power BI: the 07:30 refresh shows each product as green, red or not run, the variance, the break rows and the data quality failures by rule.

No code in the Workbench runs this. The reporting and BI analyst owns the report Reconciliation and data quality and its scheduled refresh at 07:30, which reads the two lake files from the previous step. Your work is to make those files carry what the report needs: one row per reconciliation and product with the counts, the balances, the variance and the result, the break rows with their account numbers, and the data quality failures by rule. The grades follow BR7: green when every reconciliation for the product passed, red when at least one broke, not run when the reconciliation did not run, with the reason. The story is done when the report shows the three grades from the SIT files.

## RWB-E1-012 Retire local copies

Module: P1 Recovery data engine

### Step 1

**In the story.** Team manager: works from the case list for at least two working days after the tracker's load is signed off.

This is work a person does away from the keyboard. After the tracker's load is signed off in RWB-E1-010, the team manager and the team use the Workbench case list as their only list for at least two working days. The number of days comes from the parameter tracker.retire.parallel.days, set to 2, so a later change is a parameter change and no code change. Working days means weekends and holidays are skipped, using the working day calendar held in the reference data service. You build no endpoint for this step. You do need the WorkingDayCalendar call that step 5 uses, which adds working days to signed_off_at to find the first date on which a retirement is allowed.

### Step 2

**In the story.** Team manager: sets the tracker read-only in SharePoint or moves it to the archive location.

A person does this in SharePoint, and the Workbench takes no part in it. The team manager either changes the permissions on the Excel or SharePoint tracker so that nobody can write to it, or moves the file to a read-only archive folder. Section 19 puts this work outside the story, and the guardrails say the Workbench never changes, moves or deletes the team's tracker. Your code records where the file now lives and nothing more. Treat the archive location in the next step as a string the caller supplies, with no check that the location exists and no check that the file is read-only.

### Step 3

**In the story.** Team manager: calls `POST /admin/trackers/{trackerId}/retire` with the archive location.

The team manager triggers the retirement. No screen exists in this story, so the call arrives through the endpoint itself. You add POST /admin/trackers/{trackerId}/retire to TrackerLoadController, which already carries the load endpoints from RWB-E1-010. The request body is TrackerRetirement: archiveRef, a string of up to 400 characters, required, and version, the integer version the caller read. A request with no archiveRef returns 400 with MSG-GEN-001. The endpoint is new and is recorded in the additions file, so add it to the API specification as well as the controller. The response is the Tracker with status RETIRED, archiveRef, retiredAt, retireConfirmedBy and unfedFields.

### Step 4

**In the story.** System: checks the caller belongs to the tracker's team and holds Queue and allocation A.

The Workbench does this, with no person involved, in TrackerRetirementService before any field is written. Two checks run. The caller's role needs the letter A in the capability area Queue and allocation, and the caller's team has to match tracker_inventory.team_code. A team manager of another team is refused, and so is a role without the letter, both with 403 and MSG-P4-002. Test TC-E1-012-11 covers the second case, where the data steward calls the retirement. Scope Team means a right applies only to records of the caller's own team, so read the team code from the tracker row and compare it with the team on the session.

### Step 5

**In the story.** System: checks the tracker can be retired: decision LOAD with status SIGNED_OFF and at least two working days since sign-off, or decision RETIRE with status LISTED.

The service decides this on its own from the tracker row. Two combinations pass. A tracker with decision LOAD passes when its status is SIGNED_OFF and at least two working days have gone by since signed_off_at, counted with WorkingDayCalendar. A tracker with decision RETIRE passes from status LISTED, with no load and no waiting period. Everything else is refused with 409 and MSG-P1-013, which names the decision and the status, and a KEEP tracker is never retired. Where the decision and status pass but the days have not, the refusal is MSG-P1-014 and carries the first allowed date. Unit test each decision and status pair, and test the boundary on the second working day and across a weekend.

### Step 6

**In the story.** System: lists the fields of the tracker's field list that are not personal and have no data product field mapped to them.

The service builds this list by itself from tracker_inventory.field_list, the JSON field list that RWB-E1-005 stores for each tracker. That list gains an optional mappedTo entry, written as entity.field, which says which data product field carries the tracker field. Keep an entry when it is not marked personal and has no mappedTo value. The result is the set of fields that no feed carries, which tells the Tribe which fields a later epic has to pick up. AC2 shows three such fields on LIT-07. Personal fields are left out so that no personal data reaches the stored list or the retirement report.

### Step 7

**In the story.** System: sets status RETIRED with the archive location, the time, the confirming user and the list of fields no feed carries, using the optimistic lock version.

One update, written by the service with no further human step. Write status RETIRED, archive_ref, retired_at, retire_confirmed_by and unfed_fields on the tracker_inventory row. Migration V1_012__tracker_retirement.sql adds those four columns as varchar(400), timestamptz, uuid and jsonb. An optimistic lock means the update carries the version the caller read and changes the row only while that version is still current. Two sessions that both read version 4 therefore give one success and one 409 with MSG-GEN-004. A call on a tracker that is already RETIRED changes nothing and returns 200 with the retirement already stored, so check the status before the update runs.

### Step 8

**In the story.** Data steward or team manager: calls `GET /admin/trackers?status=RETIRED` and reads the archive location, the date and the stored file reference.

A person reads the result, and the work for you is on the response body. GET /admin/trackers already exists from RWB-E1-005. Add archiveRef, retiredAt, retireConfirmedBy, sourceFileRef and unfedFields to the Tracker schema it returns, and support the status filter. The reader needs the right R in Reference data, which the data steward, the team manager, the center of excellence analyst and internal audit all hold. sourceFileRef points at the copy of the tracker file in the write-once tracker file store from RWB-E1-010, which the retirement leaves unchanged, so a reader sees both the team's archive location and the Workbench copy.

### Step 9

**In the story.** Tribe lead (RW-TRIBE): on 26 November 2026, calls `GET /admin/trackers/retirement-report` and files the report with the release checklist.

The Tribe lead makes this call and files the result by hand with the release checklist for 30 November 2026. You build the endpoint and TrackerRetirementReportService behind it. The service reads tracker_inventory and the team list in the parameter tracker.inventory.teams, and returns one row per team: the count of LOAD and RETIRE trackers, how many are retired, the outstanding count with each outstanding tracker code and status, and the confirmations with tracker code, user ID and date. The request takes asOf, a date that defaults to today. Team names come through the P4 published interface, never by reading the reference tables directly. The right needed is Reference data R.

## RWB-E1-013 Baseline measures

Module: P9 Reporting

### Step 1

**In the story.** Reference data administrator: loads the measure definition file through POST /admin/reference-loads with table "measure_definition".

A person starts this, the reference data administrator, who holds the Reference data C right. They upload the file of six measure definitions to the existing endpoint POST /admin/reference-loads with table set to measure_definition. The Tribe lead agrees the definitions and is named as approver on each row; the administrator only loads them. Your work is MeasureDefinitionLoadHandler, which the P4 reference load service calls for this table code. It receives the parsed rows and the valid from date. Each row carries the measure code, name, formula, data product, unit, definition version, approver and approval date, so the formula of a measure is data and never code.

### Step 2

**In the story.** System: checks each row has a measure code, name, formula, data product, unit, approver and approval date; any failure refuses the whole load.

This runs automatically in MeasureDefinitionLoadHandler, before anything is written. Check every row for a measure code, a name, a formula, a data product, a unit, an approver and an approval date. One missing value refuses the entire file, including the rows that are correct, and no definition version is put in force. Answer with MSG-GEN-001 naming the field that is empty. Refusing in full is the rule for every reference load, because a half loaded definition set would let a measure publish under a formula nobody approved. Write unit tests for a good file of six rows and for a file whose TIME_IN_STAGE row has no formula.

### Step 3

**In the story.** JOB-15 Reporting extract, nightly 01:30: reads the case facts of the previous business date through the P3 reporting interface and the payments since entry through the P1 interface.

A scheduled job does this with nobody present. Build ReportingExtractJob and schedule it in Quartz for 01:30 Asia/Bangkok every night. It reads case facts for the previous business date by calling CaseReportingApi.caseFacts, which belongs to module P3 and returns the case ID, product group, route code, stage code, queue code, entry date, stage clock start, closed date and status. It reads payments by calling RecoveryDataApi.paymentsSinceEntry in module P1. Use these two interfaces only, since reporting never queries another module's tables. Call RecoveryDataApi.loadStatus as well, so the job knows whether the loads of that business date passed their checks before it computes anything.

### Step 4

**In the story.** System: computes each measure in force by its definition: counts by route, age band and queue; realized recovery; median time in stage; median turnaround per route.

The job computes the values itself. Build MeasureCalculators, one calculator per measure code, and let each one read only the facts the interfaces returned. Ask MeasureCatalog.inForce for the definitions valid on the business date, then run the calculator for each measure code it names: counts of cases by route code, by age band and by queue; realized recovery as the sum of payments since entry; the median time in stage; and the median turnaround per route. Age bands are reference rows, so read the band edges from that list rather than writing day numbers into the code. Test each calculator against the synthetic case set, where the answers are known in advance.

### Step 5

**In the story.** System: writes one measure_snapshot row per measure, product and dimension value, with the definition version and business date.

The job writes the results, with no person involved. One computed number becomes one row in measure_snapshot, so a count of cases by route for one product gives one row per route value. Each row carries the measure code, the definition version used, the business date, the product group, the dimension code, the dimension value, the value, the case count and the time it was published. The unique key across measure code, definition version, business date, product group, dimension code and dimension value is what makes a rerun safe: the same computation replaces its own row rather than adding a second copy. Build MeasureSnapshotEntity and the migration V1_013__measures.sql for both new tables.

### Step 6

**In the story.** System: on the baseline business date, marks the rows as baseline and frozen; frozen rows are never changed.

The job decides this from configuration, not from a person. Read the property rwb.reporting.baseline-date, set to 2026-11-27, and when the business date being computed matches it, set is_baseline and frozen to true on the rows written. Protect frozen rows in two places. In the service, skip any row already frozen when a date is rerun. In the database, add a trigger to measure_snapshot that refuses an UPDATE or DELETE where frozen is true; a trigger is code the database runs by itself on a write, so even a direct SQL statement cannot change a frozen value. Test that an update of a frozen row fails and that a rerun answers MSG-P9-001.

### Step 7

**In the story.** System: writes the extract files of INT-19 to the data lake with the business date and the freshness stamp, and records the run in the job monitor.

The job does this at the end of its run. Build DataLakeWriter, which writes the INT-19 extract files through the integration adapters into the data lake load area. Each file carries the business date, the freshness stamp and a trailer holding the record count, so a reader can tell whether the data is complete and how old it is. When the load area does not answer, hold the extract, send an alert to the operations channel with MSG-GEN-006, and send the files on the next JOB-15 run; the snapshot rows are already written in the Workbench, so nothing is lost. Record the run on the job monitor with its row count, start time and end time.

### Step 8

**In the story.** Reporting and BI analyst: the Power BI data set refreshes at 07:30 from the extract; the report shows the previous day and the baseline side by side.

A person owns this part and no Workbench code runs in it. The Reporting and BI analyst builds the Power BI data set over the extract files in the data lake and sets it to refresh at 07:30, after JOB-15 has written the night's files. The report reads the previous day's rows and the frozen baseline rows of 2026-11-27 together, which is why every extract has to carry the baseline rows unchanged. Your side of the handover is the extract: a stable file layout, the business date, the freshness stamp and the trailer count. The story is done when the analyst has refreshed the data set once in SIT from your extract.

## RWB-E1-014 Decision log copy to the data lake

Module: P1 Recovery data engine

### Step 1

**In the story.** Quartz: starts JOB-13 Decision log copy at 01:00 for business date D (the previous calendar day).

Quartz is the scheduler inside the Workbench, and it starts this job on its own with no person involved. Put the trigger in Quartz as the cron expression 0 0 1 * * ? in the Asia/Bangkok time zone, so the job starts at 01:00 every night. The business date it works on is the previous calendar day, so the run at 01:00 on 1 December copies the entries of 30 November. Build DecisionLogLakeCopyJob as the Quartz job and mark it @DisallowConcurrentExecution, which makes Quartz refuse a second start while a run is in progress. The run, its status and its checks appear in the job monitoring built in RWB-E1-056. The whole job sits behind the feature flag rwb.dataengine.lake-copy.

### Step 2

**In the story.** DecisionLogLakeCopyService: reads the watermark (last copied entry hash and cumulative count) from lake_copy_watermark.

The service reads the row itself; no person is involved. Create the table lake_copy_watermark with a Flyway migration in this story: copy_name varchar(40) as the primary key, last_entry_hash char(64) not null, last_decided_at timestamptz, rows_copied_total bigint not null, business_date date not null, and the standard columns. The same migration inserts a seed row, which is a starting row the migration writes so the first run has something to read: copy_name DECISION_LOG, last_entry_hash of 64 zeros, which the interface calls the genesis hash, and rows_copied_total 0. The watermark is the point the last matched copy reached, held as the hash of the last copied entry and the running total of rows copied. LakeCopyWatermarkRepository reads and writes it.

### Step 3

**In the story.** DecisionLogLakeCopyService: calls DecisionLogExport.head() and fixes the cut-off: the live count and last entry hash at start.

The service makes this call on its own. DecisionLogExport is the interface published by the decision log module in package recovery.decisionlog.api; your code reads the log only through it and never queries decision_log_entry. If the interface is not there yet, it is built in P7 with head() and entriesAfter(), with unit tests on chain order. head() returns a ChainHead holding the live row count, the hash of the last entry and the time of the last decision at the moment of the call. Hold those values for the rest of the run as the cut-off, which is the target this run copies up to. Entries written after the call are left for the next night, and the later match compares the copy against this fixed cut-off.

### Step 4

**In the story.** DecisionLogLakeCopyService: calls DecisionLogExport.entriesAfter(watermarkHash, 5000) in chain order until it reaches the cut-off hash.

The service runs this loop itself. entriesAfter takes the hash to start after and a page limit, and returns at most that many entries in chain order. Chain order follows the hash chain: each entry holds its own hash and the hash of the entry before it, so the entries come back in the order they were written. Read the page size from the property rwb.dataengine.lake.page-size, which is 5000 per environment, rather than writing the number in the code. Pass the watermark hash on the first call and the last hash of each page on the next, and keep going until you reach the cut-off hash held at step 3. Test the paging with 12,480 synthetic entries. When every call fails, the job ends Failed, MSG-GEN-006 names the decision log, and the watermark is left where it was.

### Step 5

**In the story.** LakeFileWriter: writes the entries to `decision-log/business_date=D/` as Parquet files and writes `_manifest.json` with the row count, first hash, last hash and cumulative count.

LakeFileWriter does this with no person involved. Parquet is a column-based file format that the lake and the reporting tools read. Write the entries into the intake container named by the property rwb.dataengine.lake.container, under the prefix from rwb.dataengine.lake.path-prefix, which is decision-log, in a folder named business_date= and the date. That folder is the partition for the day. Split the entries across files using rwb.dataengine.lake.rows-per-file, which is 50000. Each row carries the 18 DecisionLogEntry fields with the same names they have in api.yaml. Then write _manifest.json in the same folder with the row count, the first hash, the last hash and the cumulative count. On a night with no new entries, write the partition with a manifest of zero rows and the unchanged last hash. Test the writer against an Azurite or local file system container.

### Step 6

**In the story.** LakeCopyReconciler: reads the manifest back from the lake and compares the cumulative count and last hash with the cut-off (REC-08, tolerance zero).

LakeCopyReconciler does this check itself. Read _manifest.json back from the lake rather than trusting the values your own code held in memory, because a write that stopped part way is only found by reading the result. Compare the cumulative count and the last hash in the manifest with the cut-off taken at the start of the run. The tolerance is zero, so any difference at all fails the check, which is recorded on the job run under the reconciliation code REC-08. On a failure, as AC3 shows when 379 of 380 rows reach the lake, record the break with MSG-P1-019, leave the partition not marked complete, leave the watermark where it is, and alert the data steward. The job tries the same range again the next night.

### Step 7

**In the story.** LakeCopyReconciler: on a match, marks the partition complete, moves the watermark forward and records the checks on the job run.

The reconciler does this itself, and only when the check at step 6 matched. Mark the day partition complete, which moves its state from Written to Complete. Then update the single lake_copy_watermark row for copy name DECISION_LOG with the cut-off values: the last entry hash, the time of the last decision, the new total of rows copied and the business date. Write the checks on the job run record as well, so GET /admin/jobs shows the row count and the REC-08 result to the platform administrator and the data steward. Move the watermark nowhere else in the code: a run that did not match leaves it untouched, which is what makes the next night copy the same range again.

### Step 8

**In the story.** LakeRetentionService: reads the retention rule for DP12 LAKE_COPY and moves each partition older than the rule to the archive tier, recording the partition list, the count and the rule version on the job run.

This runs inside the same job, with no person involved. Read the retention rule row for product DP12 and record class LAKE_COPY from the retention_rule table built in RWB-E1-017, and take retention_months and rule_version from it. The reference data administrator loads that row and Compliance approves it, so the period is never a value in your code. Compare each partition business date with the rule and move only the partitions older than the period to the archive tier, the cheaper storage the lake keeps old data in. The comparison is strict: a partition exactly at its retention age is kept. Write the list of partitions moved, how many there were and the rule version on the job run, as AC2 shows with one partition under rule version RET-2026.11.

### Step 9

**In the story.** Data steward: reads the run result in GET /admin/jobs and the break, if any, in the morning.

A person does this, the data steward, who holds Platform administration R. There is no screen in this story, so the data steward reads the result through GET /api/recovery/v1/admin/jobs with type=JOB-13; the interface and job monitor screen SCR-44 arrives in Epic 2. Your work is to make that response carry what the data steward needs: the job ID, type, business date, status, start and end time, and the checks with the row count, the REC-08 result, the number of partitions archived and the rule version. A role without Platform administration R is refused with 403 and MSG-P4-002, which is the access test TC-E1-014-09. On a failed run the data steward also receives the operations alert, and the platform administrator reruns the job from the job monitor.

## RWB-E1-015 Freshness stamp per data product

Module: P1 Recovery data engine

### Step 1

**In the story.** Load job (JOB-01 or JOB-09): commits a load for product DP01 and business date D.

Nothing new is built at this step. It is the moment a load job finishes its write and commits, and it happens on its own. JOB-01 is the COLLINS load check and intake built in RWB-E1-003, and JOB-09 loads the weekly and monthly file products. Commit means the database has accepted every row of that load as one unit of work. The stamp of step 2 has to be written inside that same unit, so each load job needs a hook at its commit point rather than a call that runs afterward. Every Epic 1 load job has to call recordLoad, which is part of the done condition of this story.

### Step 2

**In the story.** FreshnessStampService: in the same transaction, writes one data_product_load row with business date D, the source extract time from the COLLINS control record and the load time.

The load job calls this; no person types the times. Build FreshnessStampService.recordLoad with product code, business date, source extract time and load time, and a Flyway migration for data_product_load holding id, product_code, source_system, business_date, source_extracted_at, loaded_at, status, stale_flagged_at, duplicate_count and the standard columns, unique on product_code and business_date, with an index on product_code and loaded_at descending. Flyway applies versioned SQL files in order, so every environment reaches the same schema. The source extract time is when the source system took the data, read from the COLLINS control record; the load time is when the Workbench wrote it. A repeat for the same product and date adds 1 to duplicate_count and writes no second row.

### Step 3

**In the story.** JOB-01 freshness step: at each product's expected-by time, checks that a load for the expected business date exists.

This runs on a schedule, not on request. Build FreshnessCheckStep and create one Quartz trigger per product from the data_product rows, each firing at that product's expected_by time in Asia/Bangkok. DP01 is daily at 08:00 and DP06 is weekly at Monday 08:00. The step reads data_product, then looks for a data_product_load row for the expected business date. Cycles and times are data rows, so a new product or a changed time needs no code change. A weekly product inside its cycle has to be left alone on the days between loads, which is AC8. Tests run against a fixed test clock rather than the real clock.

### Step 4

**In the story.** FreshnessStampService: for a product with no load, sets the latest row to status STALE, writes a data quality exception with check FRESHNESS and sends the operations alert.

The same scheduled step does this. When no load for the expected business date is present, set status STALE and stale_flagged_at on the product's latest data_product_load row, raise one data quality exception row with the product code and check FRESHNESS in the list built in RWB-E1-006, and send the alert to the channel named by the property rwb.dataengine.freshness.alert-channel. Loaded rows are never changed or removed, so the previous load stays in use for every reader. A rerun after a failure must not raise a second exception for the same product and day, so look for an open exception for that product and date before writing one.

### Step 5

**In the story.** StaleMarkerListener: on LoadRefused, marks the product STALE at once.

This is event driven and needs no person and no clock. Build a listener on LoadRefused, EV-27, which the load job of RWB-E1-003 publishes when a check refuses a load, and set the product STALE as soon as the event is handled rather than waiting for the expected-by time. AC4 sets DP01 stale from 05:20, the time of the refusal. The listener is idempotent on the event ID, which means handling the same event twice leaves the same result and writes nothing a second time, so keep the event ID and check it before acting. The stamp for the business date already in use stays in use.

### Step 6

**In the story.** Consumer (case record view, P3 or P7): calls FreshnessQuery or GET /data-products/freshness and receives business date, source extract time, load time and status per product.

Other modules and the front end read the stamp here; no person acts. Build the published interface FreshnessQuery in package recovery.dataengine.freshness.api with stampFor, stampForRow and stampsFor, and FreshnessController for GET /data-products/freshness with optional product and asOf query values. The response is DataProductFreshness with productCode, productName, businessDate, sourceExtractedAt, loadedAt, status and staleSince. Authorization is Case record R and no case scope applies, because the stamp holds no case data. A malformed product code or date answers 400 with MSG-GEN-001. P3 and P7 read stamps only through this interface and never read data_product_load.

### Step 7

**In the story.** Case record view: shows the stamp in the data panel, with MSG-P1-001 when the product is stale.

A person reads this on the screen. Build DataFreshnessPanel, a React component in the data panel of SCR-03 Case record, showing each product with its business date and its load time. When a product is STALE the panel shows MSG-P1-001 beside it, in the form Account and arrears is from 2026-11-30. Today's load has not arrived. The Loading state shows skeleton rows while the call runs. The reader needs Case record R, so case roles such as the case owner and the team manager see it, and the Thai text of the message follows decision DL10.

### Step 8

**In the story.** P7 inputs snapshot builder: calls FreshnessQuery.stampsFor() for the products a decision reads and writes each stamp into the snapshot that inputs_ref points to.

The decision log writer does this while it records a decision. The inputs_ref column on decision_log_entry points at a snapshot of the values a decision read, and this step adds the freshness of each of those products to that snapshot. Pass the set of product codes to stampsFor, which returns one stamp per code in a single call, then write each stamp into the snapshot. The snapshot itself belongs to RWB-E1-027; the work here is the interface and the call. AC3 expects the snapshot to list DP01 and DP06 with their load times and status LOADED. This story writes no P7 table.

### Step 9

**In the story.** Load job: a later load for date D sets status LOADED and clears the stale flag.

The arriving load does this through the same recordLoad call. A load that commits after the product was flagged sets status LOADED on the row for that business date with the new load time, clears the stale flag and closes the open FRESHNESS exception for that product and day. AC6 has DP01 flagged at 08:00 on 2026-12-01 and the load committing at 08:40, after which the status reads LOADED with load time 08:40. The row is found by the unique key on product_code and business_date, so this changes the existing row rather than adding another one.

## RWB-E1-016 Access control per data product and catalog entries

Module: P1 Recovery data engine

### Step 1

**In the story.** User: opens a data product view, which calls GET /data-products/{productCode}/records?caseId=.

A person starts this. A user whose role may read the product opens the view for one case, and the front end calls GET /data-products/{productCode}/records with the product code and the case id. The product code is one of DP01 to DP14, and caseId is required: a call without it returns 400 with MSG-GEN-001. You build this path in DataProductController, with page and size for paging. The response is a DataProductRecordPage holding the record items, the product's freshness stamp, the page, the size and the total. Write a contract test for the endpoint from the additions schema recorded in RWB-TE-003.

### Step 2

**In the story.** DataProductAccessService: checks the capability right Case record R through the ACE access check.

Automatic, and first in order. DataProductAccessService asks the ACE access check whether the caller's role holds right R in the capability area Case record. A capability right is the letter granted to a role for one area of the system, R meaning read here. The role codes come from the session, so your code queries neither the role table nor the permission table. A caller without that right gets 403 with MSG-P4-002 and no row is read. Keep this check ahead of the access row check and the scope call, in the order the build steps set out, so a caller who may read nothing never reaches the data.

### Step 3

**In the story.** DataProductAccessService: checks data_product_access for a row in force for one of the user's roles and the product.

The same service then reads data_product_access through DataProductAccessRepository. A row in force is one whose role_code matches a role in the session and whose product_code matches the request, with can_read true, valid_from on or before today and valid_to not yet passed. No matching row gives 403 with MSG-P4-002, and the refusal goes to the access log with the user and the product. A row dated ahead of today does not count, as AC8 shows for RW-PHONECOL and DP06 valid from 2026-12-15 read on 2026-12-14. Create the table in this story's Flyway migration, a versioned SQL file the pipeline applies to each environment, unique on product_code, role_code and access_version.

### Step 4

**In the story.** DataProductAccessService: calls the P3 case scope interface for the case's accounts and parties in the user's scope.

Automatic. DataProductAccessService calls CaseScopeQuery.linksInScope in P3 with the case id and the user context, and gets back a CaseLinks record holding the account ids and party ids of that case. When the case sits outside the caller's scope, P3 throws CaseNotInScopeException, the controller answers 404 with MSG-P4-003, the refusal is logged and no row is read. AC5 shows a case owner with scope Own asking for a case they do not own. Call the interface rather than reading P3 tables: scope belongs to P3, and this module never queries another module's tables.

### Step 5

**In the story.** DataProductRecordService: reads the product rows for those accounts or parties from P1 tables.

Automatic. Using only the account ids and party ids that P3 returned, DataProductRecordService reads the rows of the product's own entities from the P1 tables, among them party, contact_point, loan_account and collateral. Which entities belong to which product comes from sys_objects, so the service holds no product list in code. Build the read to return a record id, the entity and a map of field name to value, which is the shape the response items take. Apply the page and size from the request to the query, and leave every masking decision to the next step.

### Step 6

**In the story.** DataProductRecordService: for each field tagged is_personal in sys_fields, applies the P4 masking interface for the user's roles.

Automatic. For every field read, DataProductRecordService finds the sys_fields row and checks is_personal. A personal field value goes through MaskingPolicy.apply from P4 with the object name, the field name, the value and the caller's role codes, and the returned text is what the response carries. When Compliance has loaded no masking rule, every personal field stays masked for every role, which is the behavior AC6 asks for with first_name, last_name, cif_no, date_of_birth and the contact value. Masking rule values are data owned by Compliance under RWB-E1-037, so write no rule into code.

### Step 7

**In the story.** DataProductAccessService: writes the read to the PII access log with user, product, case, field list and time.

Automatic, and it happens before the response is returned. DataProductAccessService writes one entry through the ACE common module logging interface to PII Kafka, holding the user, the product code, the case, the names of the fields read and the time. No field value is ever logged. A refused call is logged the same way, with the user and the product. When the log write fails, the call is refused with 503 and MSG-GEN-006 naming the PII access log, and no personal field reaches the caller. Order the code to log first and answer second, which is build step 5.

### Step 8

**In the story.** Controller: returns the rows with the product's freshness stamp.

Automatic. DataProductController builds the DataProductRecordPage from the masked rows and adds the FreshnessStamp for that product, the same type RWB-E1-015 returns, so the reader sees which business date the values belong to. Fill page, size and total from the query. Map the failure paths to the responses in section 12: 400 for a missing caseId, 401 without a session, 403 with no capability right or no access row, 404 for a case out of scope, and 503 when the PII log or the store is down. Cover both new endpoints with contract tests from the additions schema.

### Step 9

**In the story.** User with Platform administration R: calls GET /admin/data-products and reads the 14 catalog entries with owner, system of record, refresh cycle, retention and fields with PDPA tags.

A person does this, and only a role holding right R in the capability area Platform administration, among them the data steward, Compliance, the center of excellence analyst, audit and the platform administrator. Build DataProductCatalogService to assemble one DataProductCatalogEntry per product from data_product, sys_objects, sys_fields and retention_rule, and return all 14 when no product filter is given. Each entry carries the product code and name, the definition, the owner role, the system of record, the refresh cycle, the expected-by time, the retention class and the field list with data type and the personal flag. AC2 expects the DP02 entry to list 20 fields with 9 marked personal.

## RWB-E1-017 Retention and archive rule for the data store

Module: P1 Recovery data engine

### Step 1

**In the story.** Reference data administrator: loads a retention rule version through POST /admin/reference-loads with table retention_rule; the owner approves it.

A person starts this. Compliance owns the retention periods and prepares the rows; the reference data administrator submits them with POST /admin/reference-loads for table retention_rule, which needs the Reference data C right. A second person, the holder of Reference data A, then calls POST /admin/reference-loads/{loadId}/approve. The reference data service from RWB-E1-043 already provides both endpoints, so your work is the handler behind the table name. Version RET-2026.11 is the first load, with one row for product DP05, table interaction, age basis occurred_at and 24 months. A version label that clashes with the one in force answers 409 with MSG-GEN-004.

### Step 2

**In the story.** RetentionRuleLoader: validates the rows (known product, known table in sys_objects, months between 1 and 600, table not decision_log_entry) and stores the version.

Your code does this with no person involved. RetentionRuleLoader.apply is the published interface the reference data service calls after approval, and it validates the whole load before storing anything. Check that product_code names a row in data_product, that table_name names an object in sys_objects, that the table is not decision_log_entry, that retention_months falls between 1 and 600, and that age_basis_field is a field of that table in sys_fields. A single bad row refuses the load in full with MSG-GEN-002 or MSG-P1-002, and RET-2026.11 keeps serving. The retention_rule table is new here, created by a Flyway migration, a numbered SQL file the pipeline applies to each environment.

### Step 3

**In the story.** Quartz: starts JOB-17 Retention job on the first Sunday of the month.

Nobody presses anything. Quartz is the scheduler inside the service, and it fires JOB-17 on the cron expression 0 30 2 ? * SUN#1 in the Asia/Bangkok zone, which is 02:30 on the first Sunday of each month. You write RetentionJob as the Quartz job class and annotate it with @DisallowConcurrentExecution so a second firing cannot overlap a run already going. A platform administrator can also start it from the job monitor with POST /admin/jobs/{jobId}/rerun; while a run is active that call answers 409 with MSG-P2-006. The trigger itself is already loaded before this story begins.

### Step 4

**In the story.** RetentionService: reads the rules in force on the run date.

RetentionService reads the rule rows itself at the start of the run. A rule is in force on the run date when its valid_from falls on or before that date and its valid_to is empty or later, so the version a run uses depends on when the run happens: a run on 2026-12-06 uses RET-2026.11, and a run on 2027-01-03 uses RET-2027.01 once that version starts on 2027-01-01. Keep the version label with the run, because an earlier run keeps the version it recorded even after a newer one takes over. Read the rows through RetentionRuleRepository.

### Step 5

**In the story.** RetentionService: calls CaseHoldQuery.casesOnLegalHold() and excludes every row of those cases.

The job calls out to the case and workflow module for this, and the exclusion is absolute. CaseHoldQuery is a published interface of P3, so you never read recovery_case or its legal_hold column yourself. casesOnLegalHold() answers with the case IDs under hold, and every row of those cases is left in the live table whatever its age. In the test data, 40 interaction rows of case RW-2024-000311 are older than 24 months and all 40 are kept. Pair this call with caseNumbers() on the same interface, because the hold report in step 9 names cases by case number.

### Step 6

**In the story.** RetentionService: selects, per rule, the rows whose age-basis field is older than the run date minus the retention months.

The selection is pure code. For each rule, read rows of the named table and keep those whose age-basis field is older than the run date minus the retention months. The comparison is strictly older: with 24 months and a run date of 2026-12-06, a row with occurred_at of 2024-12-06T00:00+07:00 is kept, and only rows before that moment are selected. Drop the case IDs from step 5 before selecting. Work in batches of rwb.dataengine.retention.batch-size, which is 5000, and use the index ix_interaction_case_time over case_id and occurred_at. Nothing is deleted at this point.

### Step 7

**In the story.** ArchiveWriter: writes the selected rows per table to the archive container with a manifest (row count and SHA-256 per file) and reads the manifest back.

ArchiveWriter does this on its own, and it is the step that makes the deletion safe. Write the selected rows of each table as JSON lines files into the write-once archive container from RWB-TE-012, under the path retention/YYYY-MM-DD/<table>/ with the run date. Beside them write a manifest, a small file holding the row count and the SHA-256 hash of each data file. SHA-256 is a fixed-length fingerprint of the file content, so a file that was truncated or altered no longer matches. Read the manifest back from the container and compare both numbers before anything else happens. The container location comes from the property rwb.dataengine.retention.archive-container.

### Step 8

**In the story.** RetentionService: after the manifest matches, deletes the archived rows from the live table in one transaction per table and rule, under the purge setting the append-only trigger allows.

Only after the manifest matches does the service remove the live rows, and the database refuses the delete unless you ask for it correctly. The interaction table carries an append-only trigger: a trigger is a function the database runs on every insert, update or delete, and this one refuses changes through refuse_change(). Your Flyway migration replaces that function so a DELETE on interaction passes when the transaction setting recovery.retention_purge is set to on. RetentionService sets it inside its own delete transaction and nowhere else. UPDATE is still refused, and decision_log_entry keeps the refusal with no exception. One transaction covers one table and one rule.

### Step 9

**In the story.** RetentionService: records on the job run the counts per product and table, the rule version, the archive location and the hold report (case numbers and row counts kept).

The run writes its own record, with no person involved. On the JOB-17 job run, record the row count per data product and table, the rule version the run used, the archive location under retention/YYYY-MM-DD/, and the hold report. The hold report holds the case numbers from CaseHoldQuery.caseNumbers() with the number of rows kept for each, as with the single case holding 40 rows. Counts and case numbers only: no field value from an archived row goes into the run record, the log or a test. This is the content that GET /admin/jobs returns in the next step.

### Step 10

**In the story.** Compliance officer: reads the run result through GET /admin/jobs and the summary alert (MSG-P1-020).

A person reads the result; nothing in the flow pushes it to them. The Compliance officer calls GET /admin/jobs with the Platform administration R right and sees the JOB-17 run with its counts, rule version, archive location and hold report. The summary alert MSG-P1-020 carries the same figures in one line: the row count, the product, the rule and its version, and the number of cases kept on legal hold. Build that alert as part of this story. Reading the run is all the Compliance role may do here; a rerun needs the platform administrator, and RW-COMPLY posting one is refused with MSG-P4-002.

## RWB-E1-018 Case ID issuance and case record v1

Module: P3 Case and workflow

### Step 1

**In the story.** JOB-01: publishes LoadCompleted for source COLLINS and business date 2026-12-01.

Your story does not build this step. JOB-01 loads the COLLINS data, runs its load checks, and publishes the event LoadCompleted, which carries the source and the business date. Publishing means writing the event once so that other parts of the system can react to it. The event arrives only when every load check has passed, which is why no case can be created from a refused or late load (BR7). When the load is refused, JOB-01 publishes nothing, your job never starts for that date, and the job monitor shows MSG-P1-001 (AC9). Treat the event as the one trigger of your job and read the business date from it.

### Step 2

**In the story.** CaseCreationJob (JOB-02): starts on LoadCompleted and reads the entry threshold parameter `case.entry.dpd`.

You build CaseCreationJob as a listener on LoadCompleted for source COLLINS, scheduled as JOB-02 after JOB-01. No person starts it. Its first action is to read the entry threshold from the parameter service built in RWB-E1-042, under the key case.entry.dpd, whose value is 90. Read the value on every run and keep no copy of 90 in Java code, because the threshold is data and the center of excellence owns it. The feature flag rwb.p3.casecreation turns the job off, and with it off JOB-02 creates no case. Build step 5 in section 13 pairs the listener with the skip rule that makes a second run harmless.

### Step 3

**In the story.** CaseCreationJob: asks the P1 interface for every account with days_past_due at or above 90 on the business date that has no open case link.

The job asks P1 for the accounts that qualify instead of querying the account tables itself. Call RecoveryDataQuery.accountsAtOrAbove with the threshold and the business date. The call returns AccountEntrySnapshot records holding the account ID, the primary party ID, the product group, the region code, days past due, the total balance, the data as of date and the flags for restructuring, dispute, deceased, bankruptcy and fraud. Accounts already sitting on an open case are left out, which means no open case_account link for that account. An account at 89 days past due is not returned and comes back into view the next day once the load moves it to 90 (AC7).

### Step 4

**In the story.** EntryRuleEvaluator (SY-RULES): evaluates the exclusion rows in force for each account; an excluded account gets an exclusion record with the reason code, rule ID and version, and no case.

EntryRuleEvaluator runs inside the job as the service identity SY-RULES, with no person involved. It reads the exclusion rows, which are rule rows with rule table EXCLUSION, through RuleTableReader in P4, and applies them to each account snapshot. The five reason codes are DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN and OPEN_DISPUTE. When a row matches, the account gets no case, and you write one case_entry_exclusion row holding the account ID, the business date, the reason code, the rule ID and the rule version, for example ACTIVE_PLAN with version EXCL-2026.11 in AC2. The unique key on account_id and business_date keeps a repeated run from writing a second exclusion row.

### Step 5

**In the story.** CaseGrouping: groups the remaining accounts by primary customer and product group; an existing open case for the same pair receives the new account link instead of a new case.

CaseGrouping takes the accounts that passed the entry rule and groups them by primary customer and product group. One group becomes one case, so a customer with two hire purchase accounts at 95 days past due receives a single case with both accounts linked (AC3), and a customer with a mortgage and a hire purchase account receives two cases (AC12). Before creating anything the service looks for an open case for the same customer and product group through CaseRecordService.findOpenCase and links the new account to it. The partial unique index ux_case_open_customer_product enforces this in the database. A partial index applies only to the rows matching its WHERE clause, here the cases with no closed date.

### Step 6

**In the story.** CaseNumberIssuer: takes the next number from the sequence for the entry year and formats RW-2026-000123.

CaseNumberIssuer produces the case number. It draws the next value from the yearly database sequence case_no_seq_YYYY and formats it as RW, the entry year and six digits, for example RW-2026-000123. A sequence is a database object that hands out each number once, which is what keeps a number from being used again after a case closes (AC4). The issuer refuses a value above 999999: creation stops for the rest of that year, the job record carries MSG-P3-025 and an incident goes to the platform administrator (AC11). The job creates the next year sequence each December, so case_no_seq_2026 and case_no_seq_2027 both come with migration V018_1__case_creation.sql.

### Step 7

**In the story.** CaseCreationService: in one transaction writes recovery_case with status NEW, case_account rows, the BORROWER case_party row and CaseCreated (EV-01) in the outbox.

CaseCreationService writes the case in one transaction, which means the database keeps every write of that case or none of them. Inside it you write the recovery_case row with status NEW, the case_account rows for the linked accounts with the primary account marked, the case_party row with role BORROWER for the primary customer, and the CaseCreated event row in the outbox. The outbox is a table in the same database: writing the event there inside the same transaction means the event exists only when the case exists, and delivery happens after the commit. Status NEW is read from the list LOV-CASE-STATUS through CaseStatusCatalog, so write no Java enum of statuses.

### Step 8

**In the story.** CaseCreationService: as the last step before commit, calls DecisionLogWriter.write with decision code "D6", final call "CASE_CREATED", the entry rule version and the inputs; a failed write rolls the transaction back.

The last call before the commit is DecisionLogWriter.write from RWB-E1-027, with decision code D6, final call CASE_CREATED, the entry rule version and the inputs that led to the case. The writer runs inside the same transaction as the case. When it throws DecisionLogUnavailableException the whole transaction rolls back, which means every write of step 7 is undone: no case, no account links, no party link and no outbox row. The job record then lists that account as failed with MSG-P7-003 and the next run takes the account again (AC10). Test TC-E1-018-14 forces the decision log write to fail for a whole run.

### Step 9

**In the story.** CaseCreationJob: records counts (accounts read, excluded, linked, created, failed) on the job record; JOB-03 starts after it.

At the end of the run the job writes its counts on the job record: accounts read, excluded, linked, created and failed. The platform administrator reads these in the job monitor and reruns the job from there when needed. A rerun has to be harmless, so the job skips any account already linked or excluded for that business date and takes only the failed ones again; the second run issues no case number (AC8). The entry decision is keyed on account ID and business date for exactly this reason. JOB-03 is scheduled after JOB-02 and starts once it completes, so set the job completion correctly.

### Step 10

**In the story.** Case owner: opens the case through GET /cases/{caseId} and its accounts through GET /cases/{caseId}/accounts.

A person reads the result. The case owner, or any role holding Case record R, opens the case with GET /api/recovery/v1/cases/{caseId} and its accounts with GET /api/recovery/v1/cases/{caseId}/accounts. You build both methods on CaseAndWorkflowController, plus the caseNo query parameter on GET /cases for the case number search in AC4. Each method applies the right and the scope: 403 with MSG-P4-002 when the role has no Case record R, and 404 with MSG-P4-003 when the case is outside the caller scope. RW-REFADM holds no Case record right and is refused, which is access test TC-E1-018-13. The full read only case view comes later in RWB-E1-023.

## RWB-E1-019 Roles, teams and queues as data

Module: P3 Case and workflow

### Step 1

**In the story.** RW-REFADM: fills the Queues template (sheets QUEUE and QUEUE_MEMBER) and calls POST /admin/reference-loads once per sheet with valid from 2026-11-30.

A person starts this. The reference data administrator fills the Queues template, which Shared operations owns, and uploads it. The endpoint already exists from RWB-E1-043, so you build nothing here: it takes multipart form data with the file, a table code of either QUEUE or QUEUE_MEMBER, and a valid from date. Two sheets means two calls, one per table code, both with valid from 2026-11-30. Each call answers 201 with a ReferenceLoad holding the load ID, the table, the date, the status and the row count. The caller needs Reference data right C; without it the call is refused with 403 and MSG-P4-002.

### Step 2

**In the story.** QueueTableChecks: runs the queue checks on top of the RWB-E1-043 row checks: team code in TEAM, role code in ROLE, method in LOV-ASSIGN, cap range, overflow queue exists and forms no loop, member holds the queue role.

This happens inside the load call, with no second person involved. What you build is QueueTableChecks, a class implementing ReferenceTableCheck for the table codes QUEUE and QUEUE_MEMBER and plugged into the RWB-E1-043 checks. It adds six checks on top of the row checks that already run: the team code must exist in TEAM, the role code must exist in ROLE, the method must be a value of LOV-ASSIGN, the capacity cap must fall between 1 and 500, the overflow queue must exist and the overflow chain must form no loop, and each member must hold the role of the queue they are listed on. Each check returns a RowCheckFailure naming its row.

### Step 3

**In the story.** ReferenceVersionRegistry (RWB-E1-043): on any failed row refuses the load whole and names every failed row; on a clean file stores the version with status VALIDATED.

Code from RWB-E1-043 decides this, so you reuse it rather than write it. One failed row refuses the whole file: no queue row and no member row changes, which is what AC4 checks. The response is 422 and every failed row is listed in Problem.detail, as MSG-P1-002 for the queue checks and MSG-GEN-001 or MSG-GEN-002 for an empty column or a cap out of range. A file with no failed row is stored as a new version with status VALIDATED. VALIDATED means checked and not yet in use: the rows sit in reference_version and reference_row and reach the queue tables only later.

### Step 4

**In the story.** RW-TEAMMGR: approves through POST /admin/reference-loads/{loadId}/approve; refused if the approver is the author.

A load does not take effect because it passed its checks. A second person has to approve it, and that person is the queues table owner in Shared operations, acting as RW-TEAMMGR with Reference data right A. The approve endpoint belongs to RWB-E1-043; your part is to prove the rule holds for queue loads. When the approver is the same user who uploaded the file, the call answers 409 with MSG-P7-002, and the version stays VALIDATED and out of use. Two people are needed so that no one person can change the team structure alone. A successful call returns the load with status APPROVED.

### Step 5

**In the story.** QueueVersionApplier: on the valid from date, applies the QUEUE and QUEUE_MEMBER versions in force to the queue and queue_member tables: upsert by queue code keeping the queue ID, replace active member rows, set table_version.

Build QueueVersionApplier as a job. It runs daily at 00:05 and again right after an approval or a rollback, with no one triggering it. It takes the QUEUE and QUEUE_MEMBER versions whose valid from date has arrived and writes them into the queue and queue_member tables. Match each queue by its queue code and update that existing row instead of inserting a new one: this is an upsert, insert when the row is absent and update when it is present. Keeping the queue's record ID is the point, because recovery_case.queue_id points at it and open cases must keep the queue they are in. Member rows are replaced, every row written carries table_version, and the whole version applies in one transaction.

### Step 6

**In the story.** CapacityService: answers capacity questions for the allocation engine from the applied version.

No person calls this. Build CapacityService in recovery.casewf.queues.api as a published interface, which means the allocation engine of RWB-E1-020 depends on the Java type and never reads the queue tables itself. check(queueId, userId, onDate) counts the user's open cases in recovery_case against their capacity, where the capacity is the lower of the member's own capacity and the queue's cap. It answers a CapacityAnswer of BELOW_CAP or AT_CAP with the open case count, the capacity and the overflow queue ID. The answer must come from the version applied for the date asked, so a question about 2026-12-14 uses the version in force then, not a version approved for 2026-12-15.

### Step 7

**In the story.** QueueMembershipQuery: answers the teams and regions of a user for scope by team (RWB-E1-037).

Also automatic, and also a published interface. QueueMembershipQuery.membershipOf(userId, onDate) returns a Membership holding the team codes, the region codes and the queue IDs for that user on that date. RWB-E1-037 calls it to work out what a user is allowed to see, so scope checks across the service all come from one place. The team codes come from the queue rows the user is a member of, and the region code from the TEAM row for each of those teams. Build it to answer from the version applied for the date given, the same way the capacity answer does. Return codes only, with no name and no other personal field.

### Step 8

**In the story.** RW-REFADM: if the version is wrong, calls POST /admin/reference-loads/{loadId}/rollback; the previous version is in force again and QueueVersionApplier re-applies it in one transaction.

A person decides this one. The reference data administrator calls POST /admin/reference-loads/{loadId}/rollback, which is a new endpoint you build, with a reason in the body. Build ReferenceRollbackHandler behind it: it marks the version ROLLED_BACK through the RWB-E1-043 store and then triggers QueueVersionApplier, which writes the earlier approved version back over the queue and queue_member rows in one transaction. One call is enough, and there is no second step for the user. With no earlier version to return to, the call answers 409 with MSG-P3-015 and nothing changes. An empty reason answers 422 with MSG-GEN-001. The Idempotency-Key header makes a repeated call return the first result.

## RWB-E1-020 Allocation and assignment engine v1

Module: P3 Case and workflow

### Step 1

**In the story.** Quartz: starts JOB-03 Morning allocation after JOB-02 completes for business date 2026-12-01.

Nobody starts this by hand on a normal day. Quartz is the scheduler inside the service, and you configure it to fire JOB-03 Morning allocation once JOB-02 case creation has completed for the business date. Build AllocationJob as a Quartz job with @DisallowConcurrentExecution, which stops a second copy of the same job running at the same time. The job checks the JOB-02 completion before it does any work: when JOB-02 has not completed, JOB-03 does not start, the job monitor shows it waiting with MSG-P1-001, and the cases keep status NEW. That is exception path X7 and AC10. The run has to be finished by 07:00 Asia/Bangkok.

### Step 2

**In the story.** AllocationJob: selects every case with status NEW whose last allocation date is before the business date.

AllocationJob runs the selection with no person involved. Read recovery_case for rows with status NEW whose last_allocation_date is before the business date. last_allocation_date is a new date column added by the migration V020_1__allocation_columns.sql in this story, together with queue.rr_cursor_user_id. That date is what makes the run safe to repeat: a case already allocated for the business date is skipped and the outcome type is SKIPPED, which is build step 5 and AC8. The job then calls AllocationService.allocate with the case ID and the business date for each case, and commits per case, so one failing case leaves the others in place.

### Step 3

**In the story.** AllocationService: locks the case row and reads deviation_open; a case with an open deviation goes to the deviation handler queue (R-DEV-01).

AllocationServiceImpl does this. Start by locking the case row with SELECT ... FROM recovery_case WHERE id = ? AND status = 'NEW' FOR UPDATE SKIP LOCKED. A row lock held for the length of the transaction keeps a second worker off the same case, and SKIP LOCKED makes that worker pass over it instead of waiting, which is AC11 and exception path X8. Then read deviation_open. When it is true, place the case in the queue named by the parameter allocation.deviation.queue.code, set no owner and leave the status NEW. Rule R-DEV-01 and AC7 cover this branch, and no allocation row is read for such a case.

### Step 4

**In the story.** AllocationRuleEvaluator (SY-RULES): reads the allocation rows in force on the business date and returns the first row, in row order, whose product group, region and exposure band match the case.

This happens automatically, and the rows are evaluated under the service identity SY-RULES. Your AllocationRuleEvaluator does not read the rule tables itself. It calls RuleTableReader.rowsInForce("ALLOCATION", businessDate), the P4 published interface in section 12, then walks the returned rows in row_order. The first row whose product group, region and exposure band match the case wins, and "any" in a column matches every value, per BR1. When no row matches, the case goes to the queue named by allocation.exception.queue.code, keeps status NEW, gets a decision log entry with final call RULE_GAP and publishes CaseAllocationFailed (EV-03), which is exception path X2 and AC5.

### Step 5

**In the story.** AssignmentEngine: reads the target queue's method (DF-WRK-006) and cap (DF-WRK-007), counts the open cases of each queue member and picks the owner below the cap by the method.

AssignmentEngine picks the owner, with no person choosing. Read assignment_method and capacity_cap from the target queue row and the members from queue_member. Build OwnerLoadRepository to count each member's open cases, which BR3 defines as cases in that queue owned by the person with a status other than CLOSED. Implement all four methods named in BR2: ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER and SKILL. Skip any member at or above the cap, and for round robin carry the turn in queue.rr_cursor_user_id. When every member is at the cap the case goes to the queue's overflow_queue_id, and when the queue has none, to the exception queue with the reason NO_OVERFLOW_QUEUE.

### Step 6

**In the story.** AllocationService: in one transaction sets queue, team, owner, status ASSIGNED, stage clock start and rule version, writes the assignment with reason ALLOCATION, sets the last allocation date and writes CaseAllocated (EV-02) to the outbox.

All of these writes happen in the one transaction that already holds the case row lock, so they take effect together or not at all. On recovery_case set queue_id, team_code, owner_user_id, status ASSIGNED, stage_clock_start, rule_version and last_allocation_date, and update the optimistic version column. Insert the assignment row with reason ALLOCATION. Write CaseAllocated (EV-02) into the outbox table instead of publishing it directly: the outbox pattern stores the event beside the data in the same transaction and a separate sender delivers it afterward, so no event goes out for a change that rolled back. EV-02 carries caseId, queueId, ownerId, ruleId and ruleVersion.

### Step 7

**In the story.** AllocationService: as the last step before commit, calls DecisionLogWriter.write with the row ID, table version, queue, owner and inputs; a failed write rolls the allocation back.

Your service calls DecisionLogWriter.write from the P7 interface of RWB-E1-027, inside the same transaction and after the case and assignment writes, as the last step before commit. Pass the row ID, the table version, the queue, the owner and the inputs used, which AC6 checks as rule ID ALLOC-014 and rule version ALLOC-2026.11. The call can throw DecisionLogRecordInvalidException or DecisionLogUnavailableException. Let either one roll the transaction back, so the case keeps status NEW with no queue and no owner, and record MSG-P3-013 for that case on the job record. The case is tried again in the next run. This is BR7, exception path X3 and test TC-E1-020-15.

### Step 8

**In the story.** AllocationJob: after the last case, builds the allocation summary per team (MSG-P3-011, MSG-P3-012) and sends it to the team manager through the ACE notification path.

After the last case, AllocationJob calls AllocationSummaryBuilder, which counts the overflow and exception cases for each team and fills MSG-P3-011 with the overflow count and MSG-P3-012 with the count that matched no allocation row. The job sends each summary to the team manager of that team through the ACE notification path. No case number or customer detail belongs in it; the guardrails allow counts and the team only. A run with no new cases still sends the summary with count 0, which is exception path X6 and AC9. Thai text for both messages follows decision DL10.

### Step 9

**In the story.** AllocationJob: records the run result (cases read, assigned, overflow, exception, failed) on the job record for the monitor.

The job writes its own counts: cases read, assigned, overflow, exception and failed. Write them to the job record that the job monitoring of RWB-E1-056 reads, so the platform administrator sees the result of each run and can rerun JOB-03 through POST /api/recovery/v1/admin/jobs/{jobId}/rerun. Count the cases skipped as already allocated as well, because AC8 expects the job record to show 1 case skipped after a repeated run for 2026-12-01. A rerun by a user without Platform administration U is refused with 403 and MSG-P4-002, which is exception path X10 and the access test TC-E1-020-14.

## RWB-E1-021 Transfer rules and engine v1

Module: P3 Case and workflow

### Step 1

**In the story.** Event source: writes a trigger event to the outbox: CaseStateChanged for a stage change or a route decided (rule event ROUTE_APPROVED), TimerDue, DeviationRaised, DeviationCleared, ApprovalRequested, DocumentStored or PaymentMissed.

You build nothing here; the publishing modules already write these events. The outbox is a table a module writes in the same transaction as its own change, so an event cannot exist without the change that caused it, and a listener reads it afterwards. The eight triggers reach you as seven event types: CaseStateChanged (EV-05) for a stage change and also for a route decision, where the rule event code is ROUTE_APPROVED, plus TimerDue (EV-18), DeviationRaised (EV-06), DeviationCleared (EV-07), ApprovalRequested (EV-09), DocumentStored (EV-16) and PaymentMissed (EV-12). Your job is to consume them. A TimerBreached event for a service level is not in that list and never moves a case.

### Step 2

**In the story.** TransferListener: receives the event once per event ID; a repeated event ID is ignored (R-UNI-40).

Build TransferListener for this; it runs on its own with no person involved. It reads the seven event types from the outbox and calls TransferService.transferByRule with the case ID, the trigger event and the event ID. Deduplicate by event ID, because a message can be delivered more than once. Migration V021_1__transfer.sql creates table processed_event with event_id as its primary key, a consumer column of 60 characters and processed_at. A primary key cannot hold the same value twice, so the second insert fails, you drop the event and count an idempotency hit. One transfer results from one event, however often it arrives.

### Step 3

**In the story.** TransferRuleEvaluator (SY-RULES): reads the transfer rows in force and returns the first row, in row order, whose trigger and condition match the case.

This is automatic and runs under the service identity SY-RULES. Build TransferRuleEvaluator so that it reads the rows of rule table TRANSFER through RuleTableReader in P4, never from the tables of another module. Each row holds a trigger event code, a condition expression, a target queue code and a row order. Take the rows of the version in force, which is TRF-2026.11, keep those whose event code equals the trigger, evaluate the condition against a snapshot of the case, and return the first match in row order. Later matching rows are not applied. When no row matches there is no transfer, and no decision log entry is written at all.

### Step 4

**In the story.** TransferService: skips an automated transfer when legal_hold is true (R-UNI-20) and logs the skip.

TransferService does this check itself before anything moves. Read legal_hold on the case. When it is true, an event-driven transfer stops here under R-UNI-20: the queue, the team and the owner are unchanged, and you write the skip to the job log naming that rule so the reason can be seen later. No decision log entry and no message to a user come out of it. The legal hold placed through the endpoint of step 9 is what sets the flag. This check covers rule transfers; a manual transfer is a person acting with a coded reason and goes through the path of step 8.

### Step 5

**In the story.** TransferService: locks the case by its version, picks the owner in the target queue with AssignmentEngine, and checks the move is allowed from the case status.

Three things happen inside TransferService, with no person involved for a rule transfer. First, read the case with its version column and plan the update as UPDATE ... WHERE id = ? AND version = ?. That is optimistic locking: when another transaction has already changed the row, zero rows are updated and you refuse the call with MSG-GEN-004. Second, ask the AssignmentEngine of RWB-E1-020 for an owner in the target queue, using the queue method and the queue capacity_cap. When every member is at the cap, place the case in the queue named by overflow_queue_id with no owner and tell the team manager with MSG-P3-011. Third, refuse the move when the case status does not allow it, as a closed case does not.

### Step 6

**In the story.** TransferService: in one transaction ends the open assignment, writes the new assignment (reason TRANSFER), updates queue, team and owner, and writes CaseTransferred (EV-04).

The service writes all of this in one transaction, so the case and its assignments can never be read half changed. Set ended_at on the open assignment row, insert a new assignment row with reason TRANSFER, the rule ID and, for a manual call, transfer_reason_code. Update recovery_case queue_id, team_code and owner_user_id, and the row version. Write CaseTransferred (EV-04) to the outbox with the case ID, the previous owner, the new owner and the reason code. The partial unique index ux_assignment_open_case keeps one open assignment per case. A partial index applies only to the rows that meet its condition, here the rows where ended_at and task_id are both null.

### Step 7

**In the story.** TransferService: as the last step before commit, writes the decision log entry with the row ID, version, from and to queue and owner, and the trigger.

The service writes the decision log entry, through the writer built in RWB-E1-027, as the last write before the transaction commits. The entry holds the rule row ID, the rule version, the queue and owner the case came from, the queue and owner it goes to, and the trigger that fired. A refused transfer is logged too, with the final call TRANSFER_REJECTED. When the entry cannot be written, nothing takes effect: a manual call returns 503 with MSG-P7-003 and the case keeps its queue and owner, and a rule transfer rolls back so the event is retried later. A transfer leaves the case status and the clocks untouched.

### Step 8

**In the story.** Team manager: calls POST /cases/{caseId}/transfer with reason code MANUAL, transfer reason R03 and a target owner or queue; steps 5 to 7 run with reason MANUAL.

A person does this one. The team manager calls POST /api/recovery/v1/cases/{caseId}/transfer with a TransferRequest carrying either toOwnerId or toQueueId, reasonCode MANUAL, an optional note and transferReasonCode, a new field holding a value of LOV-TRANSFER-REASON such as R03 Skill. Build the endpoint on CaseAndWorkflowController with an access check for Queue and allocation right U in team scope, and support the Idempotency-Key header so a repeat with the same key returns the first response. Refuse with 422 and MSG-P3-001 when the transfer reason is missing, and with 422 and MSG-P3-002 when the named owner is at the caseload cap. The work of steps 5 to 7 is reused with reason MANUAL.

### Step 9

**In the story.** Litigation officer: calls POST /cases/{caseId}/legal-hold with action place or lift; the case goes to On hold or back to the status it paused in.

A person does this as well, usually a litigation officer acting on a legal or court instruction, and the caller needs Case record right U. Build POST /api/recovery/v1/cases/{caseId}/legal-hold taking a LegalHoldRequest with action place or lift, a required reason and a reference, and build LegalHoldService behind it. On place, store the current case status in the new column status_before_hold, set legal_hold true and move the status to On hold. On lift, read status_before_hold and return the case to that status under R-UNI-21. A place on a case already on hold, or a lift on a case not on hold, is refused with 409 and MSG-P3-005. Each call writes its own decision log entry.

## RWB-E1-022 Sign-on with SSO, MFA and the first roles

Module: P4 Access and administration

### Step 1

**In the story.** Person: opens the Workbench in the ACE front end.

A person does this and no Workbench code runs yet. The user opens the Workbench in a browser. The Workbench is a module folder loaded by the ACE front end, so there is no Workbench login page, no Workbench password and no local account. What you build here is the front end entry: the recovery/access folder in the ACE front end holding the SessionBanner and AccessRequestPage components that later steps use. A user who already holds an ACE session from another module comes straight back from the redirect in step 2. Epic 1 has no business screens, so the first page after sign-in is an administration screen or the access request page.

### Step 2

**In the story.** ACE common module: redirects to Entra ID; the person signs in with password and second factor; Entra ID returns an OpenID Connect token with the groups claim and the amr claim.

The ACE common module and Entra ID do this, with the person typing their credentials. You configure it rather than code it: the Workbench application is already set up in Entra ID as INT-21, under the bank conditional access policy that requires a second factor. Entra ID is the bank identity provider. What comes back is an OpenID Connect token, a signed set of claims about the person, where a claim is one named value inside the token. Two claims matter here. The groups claim holds the Entra ID group names the person belongs to. The amr claim, authentication methods reference, holds how they proved who they are.

### Step 3

**In the story.** Workbench (SessionResolver): checks that the amr claim contains "mfa".

This happens on its own and is the first Workbench code in the flow. Build SessionResolver in package recovery.access.signin. Read the amr claim from the verified token and refuse the session unless it holds the value named in property rwb.access.required-amr, which is mfa. A token carrying only pwd fails here. Throw SessionRefusedException with reason code NO_MFA, which the controller maps to 401 with MSG-P4-005 asking the person to sign in again with their second factor, and publish the refusal through AccessEventPublisher. Keep the expected value in the property so the check holds no fixed text in code.

### Step 4

**In the story.** Workbench: maps each group in the groups claim to an active role row by role.entra_group; groups with no active role row are ignored.

This happens on its own inside SessionResolver. For each group name in the groups claim, read the role table for an active row whose entra_group column equals that name, and collect the role codes found. Use index ix_role_entra_group on role (entra_group) where is_active. A group with no active role row is skipped without an error, and the skipped name is written on the sign-in event so an administrator can see it. When no group maps to a role, refuse the session with 401, MSG-P4-001 and reason NO_ROLE, and the person sees the access request page with no data. Group names differ per environment and are data rows, never values in code.

### Step 5

**In the story.** Workbench: checks the resulting role set against the role conflict table version in force.

This happens on its own. Read the role_conflict rows whose conflict_version is in force by valid_from and valid_to, and test every pair of roles the person now holds. The conflicts_with column holds either a role code or one of the class values ANY_BUSINESS_ROLE and ANY_OTHER_ROLE, so one row can bar a role from every business role at once. On a match, refuse the session with reason ROLE_CONFLICT and MSG-P4-006 naming both roles, and raise an incident to the security administrator queue. You create the table in migration V_E1_022__role_conflict.sql with the RoleConflict entity; RW-REFADM loads version SOD-2026.11 into it.

### Step 6

**In the story.** Workbench: resolves the session: user reference, roles, the permission matrix version in force at that time, and the default scope of each role.

This happens on its own. Build the SessionContext object that every later check reads: the Entra ID object reference for the person, never their name or e-mail, the role codes from step 4, the default_scope of each of those roles from the role table, and the permission matrix version in force at that moment, PM-2026.11 at release. Hold the conflict version on it as well. The session keeps both versions until it ends, so a matrix version that takes effect later in the day does not change an open session and the next sign-in picks the new one up. Build the one-line scope text here too, for example Case owner. Scope: own cases.

### Step 7

**In the story.** Workbench: writes the sign-in event through the AccessEventPublisher (ACE audit log and SOC log through INT-22).

This happens on its own. Build AccessEventPublisher as a published interface in recovery.access.signin with one method, publish(AccessEvent). In Epic 1 it writes to the ACE audit log and to the SOC log through INT-22. RWB-E1-039 later adds the decision log write behind the same interface, so no caller has to change. Publish a successful sign-in with the roles resolved and any unmapped group name, and publish every refusal with its reason code: NO_ROLE, NO_MFA, ROLE_CONFLICT or NO_RIGHT. The event carries the Entra ID object reference and no personal data. These events are how the bank answers who could see a case on a given date.

### Step 8

**In the story.** ACE front end: calls GET /me/session and shows the first screen with one line naming the roles and the scope, for example "Case owner. Scope: own cases.", and a menu holding only screens whose capability area has R for at least one role.

The front end does this on its own once the session resolves. Build the new endpoint GET /me/session returning userRef, the roles with code, name and default scope, the matrix and conflict versions, the scope line and resolvedAt. It needs only a resolved session and no capability area, because it returns the caller's own session and nothing else. The React component SessionBanner shows the scope line at the top of every page. Menu filtering reads the same response and shows an entry only when at least one session role holds R in that screen's capability area, so RW-CASEOWN sees no Administration menu. Leave the breakGlass field empty until RWB-E1-039 fills it.

### Step 9

**In the story.** Person: calls any endpoint; AccessCheck evaluates the capability area and right the endpoint declares against the session's matrix version and allows or refuses the call.

The person makes the call and the check runs on its own on the server. Every endpoint declares its capability area and right with the x-capability marking in the API file. AccessCheckInterceptor, a Spring method interceptor, reads that marking before the handler runs and calls AccessCheck.check with the session, the area and the right. AccessCheckService unions the permission letters of all the session's roles for that area and tests the right needed; a dash for every role refuses every action in the area. A refusal is 403 with MSG-P4-002 naming the action, plus one refusal event with the area, the right and result REFUSED. Service identities such as SY-RULES go through the same check. Add a contract test that fails any operation with no declared area.

## RWB-E1-023 Case record view v1, read only

Module: P3 Case and workflow

### Step 1

**In the story.** Case owner: opens a case from SCR-02 Case list; SCR-03 shows the Loading state.

A person starts this. The case owner picks a case on SCR-02 Case list, and the front end opens SCR-03 Case record. Build the Loading state of SCR-03 as skeleton rows in each section, so the screen shows its shape while the five calls are still running. CaseRecordPage is the React component that owns this, in src/modules/recovery/casewf/caserecord. The whole screen is read only in Epic 1, so render no edit control anywhere on it. The feature flag rwb.p3.caserecordview controls the new page; with the flag off, SCR-03 shows the case header only.

### Step 2

**In the story.** CaseRecordPage: calls GET /cases/{caseId}, GET /cases/{caseId}/accounts, GET /cases/{caseId}/parties, GET /cases/{caseId}/interactions and GET /cases/{caseId}/documents in parallel.

The page makes these calls on its own, and all five go out together instead of one after another, which is how the screen meets its two second target. Each section renders as soon as its own call answers. Give every call the limit held in the parameter caserecord.section.timeout.ms, which is 3000 milliseconds, and when one call fails or passes that limit, show MSG-P3-023 in that section and leave the other sections alone. Four of the five endpoints belong to P3 and the documents endpoint belongs to P5. Parallel loading with per-section messages is build step 4.

### Step 3

**In the story.** CaseAndWorkflowController: checks Case record R and the scope; out of scope returns 404.

The controller runs this check on every request, before any data is read. Two separate questions are asked. First, does the caller's role include the right Case record R; if not, answer 403 with MSG-P4-002. Second, is this case inside the caller's scope. Scope is the set of cases a role may open, and ScopeService from RWB-E1-037 gives it to you as a ScopeFilter: Own means the user's own cases, Team the team's cases, All every case. A case outside the scope answers 404 with MSG-P4-003 and shows no case data, so a user cannot learn that a case exists by asking for it.

### Step 4

**In the story.** CaseRecordQueryService: reads the case from P3 tables, and the account balances, arrears and party facts through the P1 interface with their data_as_of dates.

The service does this inside the request. Read recovery_case, case_account, case_party, interaction and queue from the P3 tables through CaseAndWorkflowRepository. For the account and party values, call RecoveryDataQuery.accountsFor and RecoveryDataQuery.partiesFor on the P1 interface with the IDs from the case links; querying P1 tables directly is not allowed. Each answer carries data_as_of, the date of the COLLINS load that produced it, and you keep that date beside each section rather than one date for the whole screen. Build step 1 covers this service and the per-section dates, with tests AC2 and AC3.

### Step 5

**In the story.** CaseRecordQueryService: applies the masking rules for the caller's role through FieldMasker and publishes one AC-READ access event with the field IDs read and their masked flags.

MaskingApplier does both of these automatically on every read. Call mask(dto, session) from the P4 package built in RWB-E1-037, which hides the personal fields the caller's role may not see, so a customer number comes back with only its last digits visible. Then call AccessEventPublisher.publish with event code AC-READ, the field IDs that were read and a masked flag for each, which records who saw what. When that publish throws DecisionLogUnavailableException, mask every personal field and show MSG-P3-023 for Personal details; the rest of the case still shows. Personal fields are never shown unmasked when the access log write fails.

### Step 6

**In the story.** DocumentHub (P5): returns the document list for the case through its endpoint.

This is another module's work, reached through GET /cases/{caseId}/documents, which P5 serves and which needs Documents R. You call it and render what comes back; you do not read document tables. Apply the same 3000 millisecond limit here as on the other sections. When the document hub does not answer in time, the Documents section shows MSG-P3-023 and the header, accounts, parties and contact history still show, which is what test TC-E1-023-06 checks. A case with no documents shows MSG-P3-024 instead, the sentence for a section that has nothing in it.

### Step 7

**In the story.** CaseRecordPage: shows the header (case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation and hold flags), then Accounts, Parties, Contact history and Documents, each with its business date (read only state).

The page renders this once the calls answer. CaseHeader shows the case number, product, status, stage, route, owner, queue, entry date, prescription date and the deviation and hold flags. Below it, AccountsPanel, PartiesPanel, ContactHistoryPanel and DocumentsPanel each show one section, and each carries a DataDateBadge with the business date of the data product behind it. Use the data_as_of value you kept per section in step 4, not the date the screen was opened. Fields appear as text with no edit control, because SCR-03 is read only until the editable view in Epic 2.

### Step 8

**In the story.** CaseRecordPage: shows the stale banner with MSG-P1-001 on any section whose business date is before the latest business date.

The page decides this on its own, section by section. Compare each section's business date with the latest business date, and when the section is older, render StaleBanner above it with MSG-P1-001, which names the data product and its date. A refused COLLINS load is the usual cause, so the accounts section can be stale while the other sections are current, and each section is judged alone. The banner tells the case owner that the numbers below it come from an earlier day before they act on them. StaleBanner is build step 5, with test TC-E1-023-04.

### Step 9

**In the story.** CaseRecordPage: shows the on hold banner with MSG-P3-004 when the case is on hold.

The page shows this automatically from the case it has already read. When the case status is ON_HOLD, render OnHoldBanner with MSG-P3-004, filling in the deviation or legal hold from deviation_open and legal_hold and the date from prescription_date. The prescription date is the date after which the debt can no longer be pursued, so the banner keeps it in front of the owner while the case is held. On hold is one of the SCR-03 states listed in section 15, beside Loading, read only, stale input and error, and each state has its own layout.

## RWB-E1-024 Document store and index

Module: P5 Document hub

### Step 1

**In the story.** Caller: calls DocumentStore.store with the case ID, the document type, the source, the file in the intake container, its SHA-256 hash and any extracted fields.

The caller is another part of the Workbench, either the upload service from RWB-E1-026 acting for a person who holds Documents C, or the OCR intake from RWB-E1-032 running under the service identity SY-OCR. You build the entry point they call: the published interface DocumentStore in package recovery.dochub.store, with a store method taking caseId, documentType, source, intakeBlobRef, sha256, fields and partyId. A published interface is the only way another module may reach this code, so no caller writes the document tables for itself. The file sits in the intake container at this point, and the hash is the SHA-256 the caller computed over the file content, which step 5 uses to find a repeat.

### Step 2

**In the story.** DocumentStoreService: gets the case through CaseDirectory.findById and refuses the call if the case does not exist.

DocumentStoreService runs this check with no person involved. Call CaseDirectory.findById, the P3 published interface from RWB-E1-018, and refuse the store when it returns nothing. The guardrails forbid reading another module's tables, so never query recovery_case from this package even though the case ID is in hand. BR1 makes document.case_id mandatory, which is why the case has to exist before anything is written. The fields you keep from the case are its id and case_no. Build this check first in DocumentStoreService.store, together with the type, content and size checks of the next two steps, so that a refusal happens before the transaction opens.

### Step 3

**In the story.** DocumentStoreService: reads the type row from the document type table version in force: write_once and retention_class.

The service reads this by itself through DocumentTypeReader, which you build over the document type table that RWB-E1-025 created. The version in force is the one whose valid_from and valid_to dates cover today, DOCTYPE-2026.11 at release. Take write_once and retention_class from that row and copy them onto the document. BR3 says the caller never supplies either value, so ignore anything a caller sends for them. A type that is not in the version in force is refused with 422 and MSG-P5-006, and nothing is stored. Unit test the version in force on a boundary date, where one version ends and the next begins.

### Step 4

**In the story.** DocumentStoreService: checks the file type by its content signature and the file size against INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB.

The service does this, again before the transaction opens. Read the file's own leading bytes, its content signature, and accept the file only when those bytes say PDF, JPG or PNG. A Word file renamed to .pdf therefore fails, which is test TC-E1-024-06. A file outside the allowed list is refused with 415 and MSG-P5-001, and a file above the limit with 413 and MSG-P5-017, which shows 25 MB. Both values come from document_hub_parameter, read through DocumentHubParameters and cached for five minutes. This story creates that table in migration V1_5_024__document_store.sql with a unique key on param_code and table_version. AC7 fixes the boundary at 26,214,400 bytes.

### Step 5

**In the story.** DocumentStoreService: looks for an active document on the case with the same type and hash; if one exists, returns it and stops.

The service decides this alone. Query for an active document row with the same case_id, document_type and content_sha256, and when one is found return it and write nothing more: no second row, no decision log entry, no event. This behavior is called idempotent, meaning the same call made twice leaves the same single result. Back the check with the unique partial index uk_document_case_type_hash on document (case_id, document_type, content_sha256) where is_active, which the migration creates, so that two calls arriving together still produce one row. Test that the index refuses a second active row with the same three values.

### Step 6

**In the story.** DocumentStoreService: in one transaction, writes the decision log entry (decision code DOCATT, final call STORED) through DecisionLogWriter, inserts the document row with doc_version 1 and state COPY_PENDING, inserts the document_field rows and writes DocumentStored (EV-16) to the outbox.

The service performs all four writes, and a transaction means they commit together or none of them commits. Call DecisionLogWriter from RWB-E1-027 first, with decision code DOCATT and final call STORED; it writes inside your transaction. Then insert the document row with doc_version 1 and state COPY_PENDING, insert one document_field row per extracted field, and put the DocumentStored event (EV-16) into the outbox, a table the publisher reads after commit so that an event cannot be sent for a store that rolled back. A failed decision log write leaves no row and no event, which gives MSG-P7-003 and is test TC-E1-024-14. Write an integration test that forces the writer to fail.

### Step 7

**In the story.** DocumentStoreService: after commit, calls DocumentStorage.store (RWB-TE-012), which writes the file to rwb-docs-legal when write_once is true and to rwb-docs otherwise, at {container}/{caseId}/{documentId}/v1; the service sets storage_ref and state STORED.

The service continues on its own after the commit. Call DocumentStorage.store from RWB-TE-012, which writes the blob and refuses an overwrite; never write to blob storage any other way. Pass container rwb-docs-legal when the type row has write_once true and rwb-docs when it is false, with the path {container}/{caseId}/{documentId}/v1. On success set storage_ref and move the state from COPY_PENDING to STORED. When the container refuses the write the row stays COPY_PENDING, content reads return 503 with MSG-GEN-006, and CopyPendingStep, the step you add to JOB-12 Document intake, retries the copy on the next run. Container names are properties per environment.

### Step 8

**In the story.** User with Documents R: opens the document from the case documents screen (SCR-30); GET /documents/{documentId} returns the metadata, the extracted fields and the version list; GET /documents/{documentId}/content returns the file. The ACE common module writes each read to the PII access log.

A person who holds Documents R does this from SCR-30 Case documents, which RWB-E1-026 builds. You add DocumentDetailPanel, the React component that opens from a row of that screen, and the two read endpoints behind it. GET /documents/{documentId} returns the metadata, the extracted fields and the version list; GET /api/recovery/v1/documents/{documentId}/content returns the file of that version as application/octet-stream. Both apply the right R in Documents and the caller's scope, so a case outside the scope returns 403 with MSG-P4-003 and no metadata or content. A write-once document shows no edit control and the label Write once. The ACE common module writes the PII access log entry for each read, so your package writes none.

### Step 9

**In the story.** User with Documents U: adds a version with POST /documents/{documentId}/versions; the service inserts a new document row with doc_version n+1 and previous_version_id set to the current row, and marks the earlier row is_active = false. The earlier version stays readable.

A person who holds Documents U does this, through POST /documents/{documentId}/versions with multipart form data: the file and a reason, which is required. Build addVersion in DocumentStoreService. Insert a new document row with doc_version n+1 and previous_version_id pointing at the current row, then set is_active false on that earlier row, which stays readable through the content endpoint. Only the latest version takes a new version, so a call on an inactive row is refused with 409 and MSG-P5-025. The optimistic lock column version on DocumentEntity gives the second of two parallel calls 409 with MSG-GEN-004, leaving exactly one new row. The migration adds previous_version_id with a foreign key to document(id), a column whose value has to match an existing row's id.

## RWB-E1-025 Document types and fields agreed

Module: P5 Document hub

### Step 1

**In the story.** Center of excellence analyst: prepares the list of six types and 26 fields; legal counsel and the Head of NPA review it and sign with a date.

Three people do this away from the Workbench, and no code runs. The center of excellence analyst draws up the six document types, demand letter, court notice, appraisal report, title deed, settlement agreement and guarantor notice, with their 26 fields in total. A legal counsel user signs for Legal and a Head of NPA user signs for NPA, each with a user ID and a date, and both sign-offs sit on every row of the load file. Classification and extraction cannot be built against a list that may still change, so the sign-off is the gate. Your code never creates this list; it holds what the file carries and refuses any row without both sign-offs.

### Step 2

**In the story.** Reference data administrator: uploads the file with POST /admin/reference-loads, table DOCUMENT_TYPE, validFrom 2026-11-30.

A person uploads the file, the reference data administrator, who holds the Reference data C right. The request is multipart form data on the existing P4 endpoint POST /admin/reference-loads: the file itself in the Excel template, table set to DOCUMENT_TYPE and validFrom set to 30 November 2026. The response is a ReferenceLoad holding the load ID, the table, the valid from date, the status and the row count. Your work here is to add DOCUMENT_TYPE to the table codes the endpoint accepts and to parse the template columns into rows. A caller without Reference data C is refused with 403 and MSG-P4-002, and with the feature flag rwb.dochub.doctypes off the table code is refused.

### Step 3

**In the story.** P4 reference load service: passes the rows to DocumentTypeLoader through the ReferenceTableLoader interface.

This handover happens automatically inside the service. P4 owns the endpoint and P5 owns the document types, so P5 supplies a class that P4 calls. Write DocumentTypeLoader as your implementation of the published interface ReferenceTableLoader: tableCode returns DOCUMENT_TYPE, validateAndStage takes the load ID, the table version, the valid from date and the parsed rows, and approve takes the load ID and the approver's user ID. P4 picks the implementation by matching the table code in the request, so no change inside P4 is needed beyond listing the code. Keep every rule about document types in your class, since P4 knows nothing about retention classes or sign-offs.

### Step 4

**In the story.** DocumentTypeLoader: validates every row: type code unique, label present, write-once flag present, retention class in LOV-RETENTION, at least one field, both sign-offs with a user ID and a date.

Your code runs these checks with no person involved. In validateAndStage, read every row and test it: the type code appears once in the file, label_en is present, write_once is set, retention_class is a value in LOV-RETENTION, the field list holds at least one field, and both the Legal and the NPA sign-off carry a user ID and a date. Read LOV-RETENTION through the P4 list service, which holds LEGAL10Y and GENERAL05Y, rather than querying the lov_value table yourself. Collect the errors of every row before you answer, because the response names each failing row with its error. Unit test a valid file of six rows first.

### Step 5

**In the story.** DocumentTypeLoader: on any failure refuses the load whole and returns the row errors; the version in force is unchanged.

Your code decides this, and nobody is asked. One failing row refuses the whole file, so a file of six types with a missing NPA sign-off on the sixth writes none of the six. Answer with 422 and MSG-P3-027 naming the table, the error and the row number. The version already in force keeps every row it had and the readers keep returning it, so work in flight is untouched by a bad file. Set the load status to REFUSED and write nothing to document_type. Test this with the guarantor notice row missing its NPA sign-off, and with a file holding retention class KEEP99 and a repeated court notice type code.

### Step 6

**In the story.** DocumentTypeLoader: on success writes the rows as table version DOCTYPE-2026.11 with status LOADED, not yet in force.

Your code writes the rows automatically once every row has passed. Insert the six rows into document_type with table_version set to the version name in the file, DOCTYPE-2026.11, and valid_from set to the date on the load. The load status becomes LOADED, which means written and waiting for approval. DocumentTypeCatalog must not return these rows yet, so the readers in RWB-E1-024, RWB-E1-050 and RWB-E1-053 keep seeing the earlier version until approval comes. The unique constraint on doc_type_code and table_version is what refuses a second load of the same version with 409. Keep the load ID on each row, so the approval can find them.

### Step 7

**In the story.** Approver: approves with POST /api/recovery/v1/admin/reference-loads/{loadId}/approve; a different person from the loader.

A second person acts here. The approver holds the Reference data A right, which the permission matrix gives to no role today and which is assumed granted to the legal counsel who owns the table. They call POST /api/recovery/v1/admin/reference-loads/{loadId}/approve with the load ID in the path and get back the ReferenceLoad with status APPROVED. Build the separation of duty check inside approve: compare the approver's user ID with the user who loaded the version and refuse with 409 and MSG-P7-002 when they match, even if that user holds both rights. Refuse with 409 as well when the load is not in status LOADED. Approving an approved load returns it unchanged.

### Step 8

**In the story.** DocumentTypeLoader: sets the version APPROVED; from validFrom the readers return it as the version in force; the previous version gets valid_to of the day before.

Your code does all of this inside approve. Set the load status to APPROVED, and set valid_to on the rows of the version that was in force to the day before the new valid from date, so two versions never overlap. A version takes effect on its own date and not on its approval date: a version approved in December with valid from 1 January 2027 is returned only from that day, and a read on 31 December still gets the earlier one. Build that date rule into DocumentTypeCatalogService, which holds a five minute cache, and clear the cache on approval so the new version is not hidden behind stale entries.

## RWB-E1-026 Attach and search screen

Module: P5 Document hub

### Step 1

**In the story.** Case owner: opens case RW-2026-000123 on the case record view (SCR-03) and the Documents tab (SCR-30, state Loading then list).

A person starts this. The case owner opens the case record screen SCR-03 and selects the Documents tab, which is screen SCR-30. You build that tab as the React component CaseDocumentsTab, with the states listed in section 15: Loading shows skeleton rows while the list and the checklist are fetched, then the list shows the documents, the search bar and the checklist. The other states you build are upload, Empty and Error. The reader needs a role with Documents R and the case inside their scope, or the tab shows no document name. The feature flag rwb.dochub.casedocs controls the whole tab: with the flag off, the tab is hidden and the endpoints answer 404.

### Step 2

**In the story.** Front end: calls GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist and shows the list and the checklist placeholder.

The browser code makes both calls as soon as the tab opens, with no further action by the user. GET /cases/{caseId}/documents returns a DocumentPage with the items, the page, the size and the total, and only the active version of each document; the default size is 20 and the maximum is 100. GET /cases/{caseId}/document-checklist is new in this story and returns the case ID, the checklist version, which here is the document type table version, and one item per type with its code, label, required flag and present count. Placeholder means the service answers required false for every item, missing count 0 and complete null until RWB-E1-040 sets the required items per case type. Build it as ChecklistPlaceholderService from the document type catalog and the counts per type on the case.

### Step 3

**In the story.** Case owner: chooses Upload, picks a file and a document type from the list, and submits; the front end checks the size against INTAKE_MAX_FILE_MB before sending and sends an Idempotency-Key.

A person does this. Build UploadDocumentDialog with a file picker and a document type list taken from LOV-DOC-TYPE, which comes from the document type table in force. Before sending, the dialog compares the file size with the parameter INTAKE_MAX_FILE_MB and shows MSG-P5-017 when the file is larger. The server checks the size as well and answers 413, because the front end check does not replace it. The dialog also sends an Idempotency-Key header, which is a value the client sets so that the same submit arriving twice creates one document only; the key is kept for 24 hours per user and a repeat returns the first response. The Upload choice is shown only to roles that hold Documents C.

### Step 4

**In the story.** CaseDocumentUploadService: puts the file in the intake container, calls the malware scan (RWB-E1-041) and, if clean, calls DocumentStore.store with source UPLOAD.

Server code does this as soon as the submit arrives. Build CaseDocumentUploadService to write the file into the intake container first, then call the malware scan built in RWB-E1-041, because every upload is scanned before it is stored. When the scan finds a threat, answer 422 with MSG-P5-016, leave the file in the quarantine container and write no document row. When the file is clean, call DocumentStore.store with source UPLOAD, which is the only source value a user call may send; any other value is refused with 422. The same service refuses a submit with no document type with 422 and MSG-GEN-001, a type outside the table in force with 422 and MSG-P5-006, and a file type outside PDF, JPG and PNG with 415 and MSG-P5-001.

### Step 5

**In the story.** DocumentStore (RWB-E1-024): writes the decision log entry, the document row and DocumentStored, then copies the file.

This code already exists from RWB-E1-024, so you call DocumentStore.store and do not write this part again. The order matters. The decision log entry is written first, because a store that cannot be recorded does not proceed; when the decision log write fails, no document row and no file are kept and your dialog shows MSG-P7-003 from the 503 response. The document row is then created and the event DocumentStored is published, and the file is copied last, so the row is in state COPY_PENDING until the copy finishes and STORED after it. Your work here is the call and the error handling, plus the resilience test TC-E1-026-13, which forces the decision log write to fail during an upload and checks that nothing is stored.

### Step 6

**In the story.** Front end: on 201 refreshes the list; the new document shows within 5 seconds of submit.

The browser code does this with no further action by the user. A 201 response means a new document was created, and the tab then calls the list endpoint again so the new document appears at the top of the case document list. A 200 response with the message code MSG-P5-024 means the same file and type is already on the case; for that answer, show the document that already exists and highlight it, and add nothing to the list. The time from submit to the document appearing has to be 5 seconds or less. That is measured by a browser test in SIT, and the story is done when a 2 MB upload shows in the list inside 5 seconds there.

### Step 7

**In the story.** Case owner: enters a type and a date range in the search bar; GET /cases/{caseId}/documents with type, dateFrom and dateTo returns only the matching documents, newest first, 20 per page.

The case owner types the filter and the browser sends it. Add dateFrom and dateTo as query parameters on the existing list endpoint. In Epic 1 the date filter works on the stored date of the document, which is the created_at standard column, and not on any date inside the file. Sort newest first and take the page size from the property rwb.dochub.casedocs.page-size, which is 20. CaseDocumentQueryService and CaseDocumentQueryRepository read the document table filtered by case, type, active flag and created_at, using the index ix_document_case_type_created already created in RWB-E1-024. When dateFrom is later than dateTo, answer 422 with MSG-GEN-003 and run no search. When nothing matches, the tab shows the empty state with the sentence "No documents match this search." and the action "Clear the search".

### Step 8

**In the story.** Case owner: opens a document; DocumentDetailPanel (RWB-E1-024) shows it.

A person does this by selecting a row in the list. The panel that shows the document, DocumentDetailPanel, was built in RWB-E1-024, so your work is to open it with the document ID from the row and nothing more. The access check still applies on the way: the reader needs Documents R and the case has to be in their scope, and a case outside the scope is refused with 403 and MSG-P4-003 with no document name shown, which is the test in AC11. Searching across cases, free text search and search on extracted fields are not part of this story; they come in RWB-E1-033. When you log anything about a document, write the document ID in place of the file name.

## RWB-E1-027 Decision log writer v1

Module: P7 Decision center and log

### Step 1

**In the story.** Calling module (for example SY-CASEWF in the morning allocation): builds a DecisionLogRecord with the case, the event, the rule ID and version, the inputs reference, the actor and an idempotency key, inside its own transaction.

The calling module does this, not the code of this story. A module such as the case workflow module under identity SY-CASEWF fills a DecisionLogRecord with the case, the decision code, the rule ID and rule version, the inputs reference, the actor, the final call, decidedAt and an idempotency key, while its own transaction is open. Build Epic1DecisionRecords with one builder per Epic 1 event: case created, owner assigned, case transferred and document attached. Each builder takes its decision code from the parameter catalog keys rwb.decision.code.CASE_CREATED, OWNER_ASSIGNED, CASE_TRANSFERRED and DOCUMENT_ATTACHED, so no decision code is written in Java. The idempotency key is the event ID the calling module already holds.

### Step 2

**In the story.** Calling module: calls DecisionLogWriter.write as the last step before commit.

The caller makes this call. Wire JOB-02, JOB-03, the transfer engine of RWB-E1-021 and document attach of RWB-E1-032 to call the published interface DecisionLogWriter.write in package recovery.decision.writer. The call is placed last so that everything the action changes is already in the transaction when the record is written, which lets a failed write take the whole action back with it. An architecture test has to fail the build when any class outside recovery.decision writes to decision_log_entry, which keeps this interface the only write path. The method hands back a DecisionLogEntryRef with entryId, chainSeq, entryHash and a repeated flag.

### Step 3

**In the story.** Writer (DecisionLogWriterService): checks that a transaction is open; refuses the call if not.

The writer does this first, with no person involved. Mark the write method @Transactional with Propagation.MANDATORY. MANDATORY means the method joins the caller's open transaction and never starts one of its own, so Spring raises IllegalTransactionStateException when a caller has no transaction and nothing at all is written. That setting is what makes a refused record stop the action: the entry and the action share one unit of work, which either commits together or rolls back together. Build DecisionLogWriterService in folder recovery/decision/writer and test the refusal with a caller that has no transaction open, which is AC6.

### Step 4

**In the story.** Writer: checks the idempotency key; for a key already written, returns the first entry reference and counts the repeat.

The writer does this before any write. Add Flyway migration V_E1_027__declog_idempotency.sql with the column idempotency_key varchar(80) on decision_log_entry and the unique index uk_declog_idempotency. Idempotent means the same call made twice leaves the same single result. Look the key up through DecisionCenterAndLogRepository; on a hit, hand back the first entry's reference with repeated set to true and add 1 to the repeat count, which is exposed as the metric decision_log_repeats_total in the monitoring of RWB-E1-056. AC5 sends the document attached event twice with key EV-7f3a-0001 and expects one entry and the first entry's ID in the reply.

### Step 5

**In the story.** Writer (DecisionLogRecordValidator): checks the required fields and the version group; refuses an incomplete record with the missing field named.

The validator runs inside the writer. Build DecisionLogRecordValidator for the three rules of section 8. BR2 needs a decision code that is in LOV-DECISION, the inputs reference, the final call, decided at and the actor, plus the case unless the decision code is an access event. BR3 needs at least one of rule version, model version and agent version, and a rule ID always needs its rule version. BR4 needs an approval level from LOV-APPROVAL-LEVEL on any record that names an approver. A failure throws DecisionLogRecordInvalidException carrying MSG-P7-009 and the field name, and the writer logs the case ID with that field name alone.

### Step 6

**In the story.** Writer: calls DecisionLogStore.append (RWB-E1-008).

The writer calls the store that RWB-E1-008 built. That store appends hash-chained entries: each row carries chain_seq and a hash computed over the previous entry, so a later change to an entry can be found. Nothing of the chain is built here; this story only appends through it and reads back the entry reference. When the store cannot be written, the append raises DecisionLogUnavailableException, which carries MSG-P7-003. The columns chain_seq, corrects_entry_id and actor_user_id already exist in that store, so pass the values from the record through instead of adding columns.

### Step 7

**In the story.** Writer: writes the DecisionRecorded event to the outbox in the same transaction.

The writer does this in the same breath as the append. Build DecisionRecordedPublisher to write EV-08 DecisionRecorded, with entryId, caseId, decisionCode and approver, into the ACE outbox of RWB-TE-006. The outbox is a table in the same database, so the event row joins the caller's transaction: a rollback leaves no event and a commit leaves exactly one. Test the rollback case and check the outbox is empty, as section 13 build step 4 asks. The ledger and reporting consume the event later, and nothing is sent to a broker from inside the write.

### Step 8

**In the story.** Calling module: commits; the action, the entry and the event are stored together.

The calling module commits, and the database writes the action's own changes, the decision log entry and the outbox event as one unit. No code of this story runs at this point. AC1 shows the result: two entries for the case with final calls CASE_CREATED and OWNER_ASSIGNED, the second carrying rule ID ALLOC-MTG-BKK-01, rule version ALLOC-2026.11, actor SY-CASEWF and an inputs reference, with two DecisionRecorded events in the outbox. Both entries also have to pass the schema check, so the validator of step 5 and the commit here are tested together in TC-E1-027-01.

### Step 9

**In the story.** Writer: on a refused record or a failed append, raises the exception; the caller's transaction rolls back, an incident is raised and the caller shows MSG-P7-003 or its own message.

The writer throws and does nothing else. It never retries; the caller's job or request is what tries again. The exception travels out through the caller's transaction, which rolls back, so the action does not happen: in AC4 the case owner stays empty and the case status stays New. An incident goes to the platform administrator queue through the monitoring of RWB-E1-056. The caller chooses what a user sees, either MSG-P7-003 for a store failure or its own message, such as MSG-P3-013 on the allocation summary when a case was not allocated.

## RWB-E1-028 Service levels, timers, escalation and prescription dates

Module: P3 Case and workflow

### Step 1

**In the story.** TimerStarter: on CaseAllocated, CaseTransferred or CaseStateChanged, stops the running SERVICE_LEVEL timer of the case.

Automatic. Build TimerStarter as a listener on the three case events, which other stories publish when a case gets a queue and owner, moves to another owner, or changes status. Its first action is to stop the SERVICE_LEVEL timer the case is already running, setting that row to STOPPED so the old clock cannot warn or breach later. A SERVICE_LEVEL timer is the clock for one queue and status, so each new queue or status needs a fresh one. The partial unique index ux_timer_sl_running allows one RUNNING or PAUSED service level timer per case, which is why the stop comes before the start.

### Step 2

**In the story.** TimerStarter: reads the service level for the new queue and status and starts a SERVICE_LEVEL timer with started_at, expires_at in working days and warn_at at the warning percentage.

Automatic, in the same listener. Call ProductParameterService.serviceLevel with the case's product group, its new status and the business date, which returns the limit, the unit, the warning percent and the escalation role. Then write a timer row with started_at at the event time, expires_at at the limit counted in working days by WorkingDayCalculator from the HOLIDAY table, and warn_at at the warning percent of that limit. AC1 places a hire purchase case in LIT-BKK-OFF at 2026-12-01 09:00 with a limit of 5 working days and 80 percent warning, giving expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00, with 2026-12-05 to 2026-12-07 not working days.

### Step 3

**In the story.** PrescriptionService: on CaseCreated, reads the last payment date of each linked account through the P1 interface and the legal period for the product, and sets the earliest result as the prescription date.

Automatic. Build PrescriptionService as a listener on CaseCreated. It reads case_account for the linked accounts, calls RecoveryDataQuery.accountDates in P1 for their contract and last payment dates, and reads the LEGAL_PERIOD row for the product through ReferenceDataService. For each account it adds the legal period to the last payment date, and where no payment exists it uses the contract date. The earliest of those dates goes to recovery_case.prescription_date. AC3 gives an account with last payment 2026-03-15 and a two year period, so the date is 2028-03-15. With no LEGAL_PERIOD row for the product, the date stays empty and the case is listed on the exception queue with MSG-P3-026.

### Step 4

**In the story.** PrescriptionService: starts a PRESCRIPTION timer with expires_at on the prescription date and warn_at 180 days before; a PRESCRIPTION timer never pauses.

Automatic, in the same listener. Write a second timer row of type PRESCRIPTION with expires_at on the prescription date and warn_at that many days earlier, the number coming from the parameter legal.prescription.warn.days, which is 180. For the 2028-03-15 date of AC3 that gives warn_at 2027-09-17. Code the pause handler so it never touches this type: a deviation on the case leaves the prescription clock running with the same expires_at, because the legal period keeps passing whatever the bank does. GET /cases/{caseId} returns the prescription date on the Case schema for the screen to show.

### Step 5

**In the story.** TimerCheckJob (JOB-05): every 5 minutes finds RUNNING timers whose warn_at or expires_at has passed.

Quartz runs JOB-05 every five minutes under the service identity SY-CASEWF, with no person involved. Build TimerCheckJob to select timers with status RUNNING whose warn_at or expires_at is before now. Two partial indexes serve the two reads: ix_timer_due on expires_at and the new ix_timer_warn on warn_at, both limited to RUNNING rows, added in migration V028_1__timer_warn_index.sql. A partial index covers only the rows that match its condition, which keeps the query small as the table grows. PAUSED timers fall outside the status condition. The job has to handle the timers of 26,500 open cases inside one five minute cycle.

### Step 6

**In the story.** TimerCheckJob: for a passed warn_at, writes the decision log entry and sends MSG-P3-003 to the case owner once.

Automatic. For each timer past its warn_at, the job writes a decision log entry and sends MSG-P3-003 to the case owner, naming the timer and its end date. The word once matters: add the column timer.warned_at, set it in the same write, and exclude rows that already carry it, so a later run does not warn again. AC11 has the warning sent in the run at 08:05 on Friday 2026-12-18 with end date Monday 2026-12-21, and no warning in the run at 07:55 the same morning, because the fourth working day had not yet passed.

### Step 7

**In the story.** TimerCheckJob: for a passed expires_at of a SERVICE_LEVEL timer, writes the decision log entry with rule R-UNI-30, sets the timer EXPIRED with escalation level 1, and publishes TimerBreached with the escalation role; the case keeps its queue and owner.

Automatic. Do the three writes in one transaction, which means the database keeps them together or discards them all: the decision log entry naming rule R-UNI-30, the timer row set to EXPIRED with escalation level 1, and the TimerBreached event in the outbox, the table events wait in until they are published, carrying the timer id, the case id and the escalation role from the service level row. When the decision log store is down the transaction does not complete, the timer stays RUNNING at escalation level 0, MSG-P7-003 goes on the job record, and the first run after the store returns raises the breach. Write no change to recovery_case: the queue and the owner stay as they are.

### Step 8

**In the story.** TimerCheckJob: for a passed expires_at of any other timer type, sets it EXPIRED and publishes TimerDue.

Automatic. A timer of any type other than SERVICE_LEVEL, the PRESCRIPTION timer among them, takes the simpler path: set its status to EXPIRED and put a TimerDue event in the outbox with the timer id, the case id and the timer type. No escalation level is set and no escalation role is named, because only a service level breach goes to an escalation point. Keep the same guard as the breach branch, so a timer already EXPIRED is passed over and no second event is published for it when the job runs again.

### Step 9

**In the story.** TimerPauseHandler: on DeviationRaised pauses the SERVICE_LEVEL timer; on DeviationCleared resumes it and moves expires_at and warn_at by the paused time (R-UNI-43).

Automatic. Build TimerPauseHandler as a listener on the two deviation events. On DeviationRaised it sets the case's SERVICE_LEVEL timer to PAUSED, which takes it out of the job's selection. On DeviationCleared it sets the timer back to RUNNING and pushes expires_at and warn_at forward by the time the timer spent paused, counted in working days through WorkingDayCalculator. AC10 pauses from 2026-12-02 to 2026-12-04 and moves expires_at by two working days, while the PRESCRIPTION timer on the same case keeps running with its original expires_at.

### Step 10

**In the story.** Case owner or team manager: reads the timers through GET /cases/{caseId}/timers and the prescription date through GET /cases/{caseId}.

A person does this from SCR-03 Case record, which shows the prescription date and the due date of the running service level. Build GET /cases/{caseId}/timers in CaseAndWorkflowController to return a Timer array with id, caseId, timerType, startedAt, expiresAt, warnAt, paused, status and escalationLevel. Apply right R in the capability area Case record with the caller's scope, so a role without it gets 403 with MSG-P4-002 and a case out of scope gets 404 with MSG-P4-003. The prescription date comes back on the Case schema from GET /cases/{caseId}. Publish TimerService as well, for other modules that need the timers or the date.

## RWB-E1-029 Rule load, validation and rollback

Module: P3 Case and workflow

### Step 1

**In the story.** RW-COE: fills the Rules template (tabs Rows and Tests) for table ALLOCATION, version "ALLOC-2026.12", valid from 2026-12-15.

A person does this in Excel. RW-COE fills the Rules template, which has a Rows tab for the rule rows and a Tests tab for the expected results. The rule table name and the version label are columns in the file, so ALLOCATION and ALLOC-2026.12 arrive inside the workbook rather than as separate parameters. Your work is RuleTemplateParser, which reads both tabs and keeps the spreadsheet row number of every row, because the refusal messages name rows by that number. Parse the 26 rows and 50 test cases of the example without changing their order; row order drives the overlap and unreachable checks later.

### Step 2

**In the story.** RW-COE: calls POST /admin/rule-versions with the file, route set UNIVERSAL_RULES and valid from.

The analyst uploads the file to POST /api/recovery/v1/admin/rule-versions as multipart form data with three parts: the xlsx file, routeSet set to UNIVERSAL_RULES, and validFrom. The caller needs the Rules and parameters C right, so a role without it gets 403 with MSG-P4-002. The version label is the idempotency key, which means a second file carrying ALLOC-2026.12 answers 409 with MSG-GEN-004 rather than loading again. Two further refusals happen before any check runs: a valid-from date earlier than today answers 422 with MSG-GEN-003, and a template with no rows answers 422 with MSG-GEN-001.

### Step 3

**In the story.** RuleLoadValidator: runs the schema check (columns, types, lists), then overlap, unreachable rows and missing default.

This runs automatically once the file parses. RuleLoadValidator is a published P3 interface and you write all four checks behind it. The schema check comes first: every required column present, each value of the right type, and list values matched against the P4 lists LOV-ASSIGN, LOV-ASSIGN-REASON, LOV-PRODUCT, LOV-REGION and LOV-EXPOSURE. Then the overlap check, which refuses two rows that can both match one case at the same row order, because hit policy Unique allows only one condition to hold there. Then the unreachable row check, which refuses a row an earlier row already covers. Then the default row check for ALLOCATION. Each failure refuses the load with MSG-P3-027 naming the check and the rows.

### Step 4

**In the story.** RuleTestRunner: runs the 50 test cases against the new rows and compares each result with the expected queue or outcome.

RuleTestRunner runs with no person watching. Take the 50 test cases from the Tests tab, evaluate each one against the draft rows, and compare the result with the expected queue or outcome in the file. Use the same evaluator the live engines use, so a passing test means the same answer in production. Any mismatch refuses the load with MSG-P3-027 naming the failing test case IDs, as with TA-07 and TA-19 expecting queue MTG-BKK-CO while the new rows answer MTG-CEN-CO. The minimum number of test cases is the parameter rules.testcases.min, which is 50, so read it rather than coding the number.

### Step 5

**In the story.** RuleDryRun: evaluates the new rows against every open case and counts the cases whose result would change, by product and queue.

RuleDryRun also runs by itself, and it changes nothing. Evaluate the draft rows against every open case and count the cases whose result would differ from the result the version in force gives, grouped by product and queue. Read the case fields through the P3 repository. The output is counts only, with no case numbers and no personal data, and it goes into the change log entry written in the next step so the approver can see the size of the change. This check refuses nothing on its own. Live cases have to be present for the counts to mean anything, which is why the story needs RWB-E1-018 in place.

### Step 6

**In the story.** RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.

RuleVersionService decides the outcome with no person involved. If any check from steps 3 to 5 failed, refuse the load whole and name every failing row and test case in the Problem detail with MSG-P3-027; the version takes status REFUSED and the version in force keeps working. If everything passed, write the rows to rule_row with rule_table, row_order and target_queue_code, and write the rule_version header with status LOADED, in one transaction, which is a single unit of database work that either completes in full or leaves both tables untouched. That header is the change log: version label, author, load time, check result and dry run counts. Only P4 code writes rule_row.

### Step 7

**In the story.** RW-RISK: approves through POST /admin/rule-versions/{versionId}/approve; refused if the approver is the author.

A second person has to approve, and it cannot be the person who loaded. RW-RISK calls POST /api/recovery/v1/admin/rule-versions/{versionId}/approve with the Rules and parameters A right, and the version moves from LOADED to APPROVED. Compare the approver user ID with the author on the rule_version header: when they match, answer 409 with MSG-P7-002 and leave the status at LOADED. The same answer applies when the version is not in LOADED status. Approval alone changes no decision; it clears the version for its valid-from date. RW-REFADM may prepare load files and may never approve.

### Step 8

**In the story.** RuleVersionService: on the valid from date the version is in force; new decisions use it and open cases keep the version they were decided under (R-UNI-38).

No one triggers this. RuleEffectiveDateJob runs daily at 00:01 and sets every APPROVED version whose valid-from date is today to IN_FORCE, marking the version it replaces SUPERSEDED, which flips is_active on the rule_row rows. From that moment RuleTableReader.rowsInForce answers with the new rows for that table and date, cached per version, and every new decision uses them. A case already decided keeps the rule version recorded on its decision log entry, so a case allocated under ALLOC-2026.13 still shows that label after a later version arrives. The partial index ix_rule_table_version over rule_table and rule_version where is_active serves this read.

### Step 9

**In the story.** RW-COE: if the version is wrong, calls POST /admin/rule-versions/{versionId}/rollback; the previous version is in force again in one transaction and the change log records the rollback.

A person calls this once and the code does the rest. POST /admin/rule-versions/{versionId}/rollback is a new endpoint you build; it takes a required reason in the body, an Idempotency-Key header, and the Rules and parameters U right. In one transaction, set is_active false on the rolled-back version and true on the previous one, so readers never see a moment with no version in force. Record the rollback in the change log with the caller, the time and the reason. When the table has no earlier version, answer 409 with MSG-P3-015, as with TRANSFER holding only TRF-2026.11. A missing reason answers 422 with MSG-GEN-001.

## RWB-E1-030 Daily rebalancing and queue measures

Module: P3 Case and workflow

### Step 1

**In the story.** Quartz: starts JOB-06 at 06:30, or when JOB-03 completes for the business date if that is later.

Quartz is the scheduler inside the service, so no person starts this. You configure a daily trigger for JOB-06 at 06:30 and a condition on JOB-03: when JOB-03 has not completed for the business date at 06:30, the job waits and starts once JOB-03 completes. The platform administrator can rerun it through POST /api/recovery/v1/admin/jobs/{jobId}/rerun, which needs Platform administration U and answers 409 while the job is running. A role without that right is refused with MSG-P4-002, which is access test TC-E1-030-11. The feature flag rwb.p3.rebalance turns the moves off while the snapshot of steps 7 and 8 still runs.

### Step 2

**In the story.** RebalanceJob: lists cases in each queue with no owner and status NEW or ASSIGNED, and owners whose open cases exceed their capacity.

RebalanceJob collects two work lists from the database. The first is the cases in each queue with no owner and status NEW or ASSIGNED, read from recovery_case by queue_id, owner_user_id and status. The second is the owners whose open case count is above their capacity, which comes from counting open cases per owner_user_id against queue_member.capacity and queue.capacity_cap. A queue with no cap loaded is still listed for the snapshot and no case in it is moved (AC5), so treat a missing cap as no move. The caps and member capacity come from RWB-E1-019 and are data values (DL23), so read them on every run.

### Step 3

**In the story.** RebalanceService: for each owner above the cap, selects the newest cases by assignment time until the owner is inside the cap (R-UNI-19).

RebalanceService decides which cases leave an owner above the cap. It orders that owner open cases by assignment time, newest first, and takes them from the top until the owner count is back inside the cap. Rule R-UNI-19 sets this order, so the oldest work stays with the person who has held it. An owner holding exactly the cap loses no case, for example 150 against a cap of 150 in AC10. An owner at 153 loses 3. The selection runs in the service with no person involved, and build step 1 asks for unit tests on it with AC8 and AC10.

### Step 4

**In the story.** RebalanceService: skips cases with deviation_open or legal_hold true.

Two fields on the case block a move: deviation_open and legal_hold. When either is true the case stays with its owner, whatever its assignment time. RebalanceService checks both as it walks the ordered list, skips the held cases and goes on to the next newest, so an owner at 152 whose two newest cases have deviation_open true loses the two after them instead (AC8). The check reads recovery_case and needs no call to another module. Rules R-UNI-20 and R-DEV-01 are the source, and a move never resets the stage clock or the prescription date.

### Step 5

**In the story.** AssignmentEngine: picks an owner below the cap in the same queue for each selected or unassigned case.

AssignmentEngine from RWB-E1-020 chooses the receiving owner, so this story calls it and repeats none of that logic. It is given the queue and picks a member below the cap by the method on the queue row, queue.assignment_method, which is LOWEST_LOAD for TDR-BKK-CO in AC1. Ties go to the member first in the queue list, which is how the 12 cases with no owner split 8 to U-61 at 140 cases and 4 to U-62 at 144. When no member of the queue has capacity, those cases keep no owner and the team manager receives MSG-P3-011 with the count (AC4). The engine is called for selected cases and for cases with no owner alike.

### Step 6

**In the story.** RebalanceService: writes the decision log entry, ends the old assignment, writes the new one with reason REBALANCE and publishes CaseTransferred, case by case.

Each move is one transaction, case by case, so a failure on one case leaves the other moves in place. The transaction holds the decision log write through the writer from RWB-E1-027, the end of the current assignment row, the new assignment row with reason REBALANCE, the new value of recovery_case.owner_user_id, and the CaseTransferred event in the outbox, which is a table in the same database whose rows are delivered after the commit. When the decision log write fails, that case is not moved, the job record lists it with MSG-P7-003, and the run carries on with the next case (AC6). BR7 requires a log entry for every move.

### Step 7

**In the story.** QueueMeasureService: at the end of the run, takes one snapshot per queue at one time: depth, unassigned, age in days from the entry date, owner spread and SERVICE_LEVEL timers EXPIRED.

QueueMeasureService runs once at the end of the job and writes one queue_measure row per queue, all read at a single time so the numbers agree with each other. The snapshot holds depth, the number of cases with no owner, age in days counted from the case entry date as an average and a maximum, the lowest and highest open case count per owner, and the count of SERVICE_LEVEL timers with status EXPIRED. The read runs in one REPEATABLE READ transaction, which means every query inside it sees the same picture of the database. The row starts with status TAKEN, and the unique key on queue_id and as_of keeps a rerun from writing a second row for the same time.

### Step 8

**In the story.** QueueMeasureService: checks each queue depth against the case count for the same queue and time, and publishes the snapshot only when every queue matches.

Before anything is published the service checks itself. For each queue it compares the depth it just counted with the case count for the same queue at the same time, and only when every queue matches does it set the rows to PUBLISHED. One difference holds the whole set: the rows stay HELD, nothing reaches the reporting layer, and the data steward receives MSG-P3-029 naming the check, as AC9 shows with depth 88 against a count of 87 for DIL-BKK-CO. GET /api/recovery/v1/cases filtered by queue gives the second count in the test. DL25 and REC-01 are the source of the zero difference rule.

### Step 9

**In the story.** JOB-15: copies the snapshot to the data lake; Power BI shows it from the next morning.

JOB-15 is the reporting extract job owned by the reporting and BI analyst and it already runs nightly, so you do not build it. It copies the published snapshot to the data lake, and the Power BI queue page shows the numbers the next morning: the snapshot of 2026-12-02 appears on 2026-12-03. Your part is the hand over in build step 7. P9 reads the snapshot through the published interface QueueMeasureService.latestPublished for a business date and never queries queue_measure directly. A snapshot held at step 8 is not copied, so the report keeps the last published numbers.

### Step 10

**In the story.** TimerBreachNotifier: on TimerBreached from JOB-05, sends the team manager MSG-P3-028 with the queue's breach count.

TimerBreachNotifier is a listener, so it reacts to an event instead of running on a schedule. JOB-05 raises TimerBreached when a case passes its service level, and the listener counts the breaches for that queue and sends MSG-P3-028 to the team manager of the team, for example count 1 for queue TDR-BKK-CO in AC3. The case itself does not move and its owner does not change (BR8). The same breach appears in the next snapshot inside the breached count, which is how the Power BI queue page shows it. Build step 6 covers the listener and test AC3.

## RWB-E1-031 Queue and owner on the case list with filters

Module: P3 Case and workflow

### Step 1

**In the story.** Team manager: opens SCR-02 Case list; the screen shows the Loading state.

A person starts this by opening the screen. SCR-02 Case list already exists, and this story adds to it. Build the Loading state into CaseListPage as skeleton rows, which are gray placeholder rows the same shape as the real ones, so the table does not jump when the data arrives. Loading is one of four states the page must handle, with empty, list and filtered. The page is a React component in src/modules/recovery/casewf/caselist. Put the new queue and owner columns and the export behind the feature flag rwb.p3.caselistqueue, so the screen falls back to its old columns when the flag is off.

### Step 2

**In the story.** CaseListPage: calls GET /cases with page 0 and size 50; the service applies the caller's scope.

The page does this itself as soon as it loads. It calls GET /api/recovery/v1/cases with page 0 and size 50, and sends no scope of its own. Scope is applied on the server from the caller's role, as Own, Team, Region or All, with Team the team manager's default. CaseQueryService builds the query with that limit already in it, so a case outside the caller's scope cannot come back even if the request asks for it. The endpoint needs Case record right R and answers 403 with MSG-P4-002 without it. Never filter by scope in the browser, because the response would still carry the rows.

### Step 3

**In the story.** CaseListPage: shows each row with case number, product, status, stage, queue, owner and entry date (list state).

The page renders what the response gave it. Seven columns are needed: case number, product, status, stage, queue, owner and entry date. Queue and owner are the new ones in this story. The response carries queueId and ownerUserId, so CaseQueryService joins the queue table to supply the queue code and name, and the owner display name comes from the ACE user directory interface in the common module. A case with no owner still shows, with the owner cell left blank, which AC7 tests. Build the table with the Radix table component. The labels "Export" and "Owner user ID" are set by DL10 and not chosen in the component.

### Step 4

**In the story.** Team manager: picks queue "DIL-BKK-CO", team "DIL-BKK" and status "ASSIGNED"; the page calls GET /cases with the filters (filtered state).

The manager chooses the values and the page reacts. Build CaseListFilters with three pickers, queue, team and status, filled from the queues of RWB-E1-019 and the lists LOV-CASE-STATUS and LOV-TEAM through the P4 list interface. On a change, call the same GET /cases with the chosen values. Queue and status already exist as query parameters; team is new and has to be added to the endpoint. The filters combine with AND, so a case has to match every one of them to show. The filtered state keeps the chosen values visible above the list with a control to clear them, and Export uses exactly the filters shown.

### Step 5

**In the story.** CaseQueryService: returns only cases inside the caller's scope that meet every filter, with the total.

Server-side work, with no user action. CaseQueryService applies the caller's scope first and the filters after, so a queue of another team returns no row rather than an error, which is what AC6 expects. The response is a CasePage holding the items, the page number, the page size and the total. The total is the count of all matching rows, not of the page, and the table needs it to show how many pages there are. Add the index ix_case_team_status on recovery_case (team_code, status) in migration V031_1__case_team_index.sql; the query uses it along with ix_case_status_queue. The list has to answer in under two seconds on 26,500 cases.

### Step 6

**In the story.** Team manager: chooses Export.

A person presses this. Build ExportButton, which calls GET /cases/export with the same query parameters as the list but without page and size, since an export covers the whole filtered set. The endpoint is new in this story. The button also shows what comes back from a refusal: MSG-P3-021 when the filtered set is above the row limit, and MSG-P7-003 when the access log cannot be written. A good call answers with an xlsx file, content type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet. Hide the button when the feature flag rwb.p3.caselistqueue is off.

### Step 7

**In the story.** CaseExportService: checks the row count against the limit, publishes the access event AC-EXPT with user, time, filters and row count, then builds the xlsx with masking by role (FieldMasker, RWB-E1-037).

Automatic, and the order of the three actions is the requirement. First count the rows and compare them with the parameter caselist.export.maxrows, which is 10,000; above it, stop with 422 and MSG-P3-021. Second, publish the access event AC-EXPT through AccessEventPublisher, the P4 interface from RWB-E1-039, with the user, the time, the filters and the row count. If that write throws DecisionLogUnavailableException, make no file and answer 503 with MSG-P7-003. Only then build the workbook, running each column through FieldMasker so the caller's role decides which values appear. Exactly 10,000 rows is allowed, so the check refuses only a count above the limit.

### Step 8

**In the story.** Browser: downloads "Case list 20261202 1.xlsx".

The browser handles the download once the response arrives, so there is no code for saving the file. What you do control is the file name, which follows the pattern "Case list YYYYMMDD 1.xlsx" with the date of the export, and the content type on the response, which is what makes the browser offer a download instead of showing the bytes. The file holds one row per case in the filtered set, with the masked columns. Nothing in the export is written back to the database. The only trace of it is the AC-EXPT access log entry from the previous step, which RW-COMPLY reads.

## RWB-E1-032 Automatic attach from the OCR intake

Module: P5 Document hub

### Step 1

**In the story.** JOB-12 Document intake: runs matchStep after the extraction step.

No person starts this. JOB-12 Document intake runs every 15 minutes in business hours, and matchStep is one more step inside that job, placed after the extraction step. Your work is the step itself, built as MatchStep in the Java package recovery.dochub.attach. It reads rows the earlier steps left behind, so it needs nothing from the scanners or the mailboxes. The feature flag rwb.dochub.autoattach controls it: with the flag off, matchStep gives every classified item match_status NO_MATCH and reviewers attach them by hand. Items the step leaves untouched are taken by the next run, as the restart behavior in section 12 states.

### Step 2

**In the story.** MatchStep: selects intake items with ocr_status DONE, match_status PENDING, no document_id and a predicted type (review_reason empty or LOW_CONFIDENCE), locking each row; items with review_reason UNKNOWN_TYPE or MODEL_UNAVAILABLE get match_status NO_TYPE and are held for a person.

MatchStep runs the selection. Read document_intake for rows with ocr_status DONE, match_status PENDING, no document_id and a predicted type, where review_reason is empty or LOW_CONFIDENCE. Lock each row as you take it, so two runs cannot work on the same item. An item whose review_reason is UNKNOWN_TYPE or MODEL_UNAVAILABLE is not matched at all: give it match_status NO_TYPE and leave it for a person, which is exception path X9 and AC11. match_status is a new varchar(12) column with default PENDING, added together with candidate_case_ids by the migration V1_5_032__intake_match.sql. Items already MATCHED are never read again, so a repeat run writes nothing further, as AC9 requires.

### Step 3

**In the story.** CaseMatcher: collects case numbers from the extracted field case_no and from the OCR text with CASE_NO_PATTERN, and account numbers from the extracted field account_no and the text with ACCOUNT_NO_PATTERN.

CaseMatcher gathers the identifiers automatically, from two places for each kind. Case numbers come from the extracted field case_no of RWB-E1-053 and from the OCR text in document_text.text_content, found with the parameter CASE_NO_PATTERN. Account numbers come from the extracted field account_no and the same text, found with ACCOUNT_NO_PATTERN. Read both patterns through MatchPatterns from document_hub_parameter; no pattern belongs in the code. The scanned text holds Thai and English around the numbers, so build the unit tests on text of that kind, as build step 2 says. Collect every value found, because more than one value is what produces the MULTIPLE and CONFLICT outcomes in the next step.

### Step 4

**In the story.** CaseMatcher: resolves each case number with CaseDirectory.findByCaseNo and each account number with CaseDirectory.findOpenCasesByAccountNo, and returns one of MATCHED, NO_MATCH, MULTIPLE, CONFLICT or CASE_CLOSED with the candidates.

CaseMatcher resolves what it collected through the P3 published interface CaseDirectory, calling findByCaseNo for each case number and findOpenCasesByAccountNo for each account number. Your module never reads the case tables itself. It then returns one of five results together with the candidates it found: MATCHED for exactly one open case, NO_MATCH when nothing resolves, MULTIPLE when an account number gives two or more open cases, CONFLICT when the case number and the account number point to different cases, and CASE_CLOSED when the only candidate is closed. The matcher never picks one of several candidates. Unit test all five against a CaseDirectory stub, which is build step 3.

### Step 5

**In the story.** MatchStep: for MATCHED, calls DocumentStore.store with the case ID, predicted_type, the intake source, the file, its hash and the extracted fields; the store writes the DOCATT entry with the classifier version, the confidence and the match method, the document row and DocumentStored.

MatchStep calls DocumentStore.store from RWB-E1-024 with the case ID, the predicted type, the intake source, the file, its hash and the extracted fields. The store already exists: it writes the DOCATT decision log entry holding the classifier version, the confidence and the match method, then the document row and the DocumentStored event. Your part is building the StoreRequest in AutoAttachService, including the match method, which AC1 expects as CASE_ID and AC4 as ACCOUNT_NO. When the same file with the same hash is already on the matched case, the item is linked to that existing document and no second document row is written, which is exception path X6 and AC8.

### Step 6

**In the story.** MatchStep: on the stored document sets classification_confidence, document_type and type_candidates; for review_reason LOW_CONFIDENCE sets review_status PENDING and write_once false, so it is held in rwb-docs and listed on SCR-31 (RWB-E1-054).

AutoAttachService sets these values on the stored document. Write classification_confidence, document_type and type_candidates from the classification of RWB-E1-050. When review_reason is LOW_CONFIDENCE, meaning the confidence is under the parameter CLASSIFY_THRESHOLD of 0.80, also set review_status PENDING and write_once false, so the file is held in rwb-docs. Write-once storage cannot be altered or deleted for its retention period, and a type that is not yet confirmed must not be fixed that way. The document is then listed on SCR-31 for a person to confirm its type in RWB-E1-054. AC10 covers this, with a scan classified APPRAISAL_REPORT at 0.62.

### Step 7

**In the story.** MatchStep: sets the intake item match_status MATCHED, case_id and document_id; for any other result sets match_status to the result and candidate_case_ids, and the item is held for a person.

MatchStep closes out each intake item itself. For a MATCHED item write match_status MATCHED, case_id and document_id, which is what keeps the next run from processing it again under BR6. For any other result write that result as match_status, one of NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED or NO_TYPE, and write the candidates found into candidate_case_ids as JSON. Write no document row for those items, as AC2, AC3 and AC7 require. The partial index ix_intake_held on document_intake (match_status, received_at) covers the held values, so the review list can read them oldest first.

### Step 8

**In the story.** Reviewer: opens the Unmatched list on SCR-31 (GET /intake-items), opens an item to see the scan, the OCR text and the candidates, picks the case and the type, and attaches it (POST /intake-items/{intakeItemId}/attach).

A person does this part. A reviewer holding Documents C opens the Unmatched tab of SCR-31, which lists the held items oldest first with source, received time, match status, proposed type and candidate cases. Only items whose candidates are in that reviewer's scope are listed, and items with no candidate are listed only for roles with scope ALL. The reviewer opens one item, sees the scan, the OCR text page by page and the candidate cases, picks the case and the document type and sends the attach request. Build UnmatchedIntakeTab as the React component for the list, the viewer and the two pickers, and IntakeItemController for the endpoints in section 12. Each read of the item text is written to the PII access log.

### Step 9

**In the story.** ManualAttachService: checks the case is in the reviewer's scope and the type is in force, calls DocumentStore.store with the reviewer as approver on the DOCATT entry, and sets the item match_status MATCHED.

ManualAttachService runs the checks before anything is stored. Confirm the chosen case is in the reviewer's scope, and refuse with 403 and MSG-P4-003 when it is not, leaving the item held, which is exception path X10 and AC13. Confirm the chosen document type is in force, and refuse with 422 and MSG-P5-006 naming the value when it is not. Use the version the client sent as an optimistic lock, a check that the record has not changed since it was read, so the second of two reviewers acting at once gets 409 and MSG-GEN-004. Then call DocumentStore.store with the reviewer as approverUserId, which puts PERSON as the match method on the DOCATT entry, and set the item match_status MATCHED.

## RWB-E1-033 Search across cases

Module: P5 Document hub

### Step 1

**In the story.** Litigation officer: opens Document search from the Documents menu and enters a type, a stored date range, a field condition (field, operator, value) and or a free text term.

A litigation officer starts this by hand. There is no screen ID for a cross-case search in screens.txt, so you build the page yourself under the Documents menu and the missing ID is recorded in the additions file. Build DocumentSearchPage as a React component in the front end folder recovery/documents, with a criteria form holding the document type, a stored date range, a field condition made of a field name, an operator (eq, gt, lt or between) and one or two values, and a free text term. The field list offered to the user comes from the field_definitions of the chosen document type. The user may fill one criterion or several.

### Step 2

**In the story.** Front end: calls GET /documents with the criteria.

The browser does this when the user submits the form. Send the criteria as query parameters: type, dateFrom, dateTo, field, op, value, value2, q for the free text, page and size, where size defaults to 50 and 50 is also the maximum. The response is a DocumentSearchPage object holding items, page, size, total and capped. Each item carries documentId, caseId, caseNo, documentType, storedAt, source, matchedField, matchedValue and snippet. Keep the path you build on the controller and the path the front end calls the same, and hide the menu item when the feature flag rwb.dochub.search is off, because the endpoint then answers 404.

### Step 3

**In the story.** DocumentSearchService: validates the criteria: at least one criterion, date order, free text length, field in the type's field list.

DocumentSearchService does this on the server, before any query reaches the database. Four checks. At least one criterion is filled, otherwise 422 with MSG-GEN-001 naming a search criterion. dateFrom is not after dateTo, otherwise 422 with MSG-GEN-003. The free text term is between FREE_TEXT_MIN_CHARS and FREE_TEXT_MAX_CHARS, which are 3 and 100, otherwise 422 with MSG-GEN-002 showing those two numbers. The named field is in the field list of the chosen document type, read from document_type.field_definitions. Read the two length limits from document_hub_parameter rather than writing 3 and 100 in code, because the reference data administrator can change them.

### Step 4

**In the story.** DocumentSearchService: checks with the masking policy that the role may search a personal field or free text; refuses otherwise.

The service does this next, still before any query. Call the P4 interface mayReadUnmasked with the role code of the user and the field class, which is PARTY_NAME, ACCOUNT_NO or ID_NO. Masking means a value is replaced by a token for roles that may not see it, so a role that cannot read party names unmasked also cannot search on them: free text runs over document text that holds names, and a condition on a personal field would reveal the value by matching it. Refuse such a request with 422 and MSG-P5-020 naming the field, and run no query at all. Under the assumed rules of DL26, RW-LITOFF, RW-LEGAL and RW-AUDIT may search these; other roles may not.

### Step 5

**In the story.** DocumentSearchService: gets the case IDs in the user's scope through CaseDirectory.caseIdsInScope (all cases for scope ALL).

The service does this with no person involved. Call caseIdsInScope on the P3 CaseDirectory interface with the scope filter of the signed-in user, and use the returned set of case IDs as the boundary of the search. For a user whose scope is ALL, pass an empty filter and every case is in range. This is how a litigation officer with scope TEAM on a mortgage team never sees a document on a hire purchase case, even when that document matches every criterion. Take the case IDs from this interface rather than reading recovery_case, because another module owns that table. The result is the only list of cases the query may touch.

### Step 6

**In the story.** DocumentSearchRepository: queries active documents in those cases by type and stored date, joined to document_field for the field condition and to document_text for the free text, newest first, up to SEARCH_MAX_RESULTS.

DocumentSearchRepository runs one SQL query and no person is involved. Select active documents whose case_id is in the scope set, filtered by document_type and by created_at, which is the stored date in Epic 1. Join document_field for a field condition and document_text for a free text term, order newest first, and stop at SEARCH_MAX_RESULTS, which is 1000, with the page size applied on top. Flyway migration V1_5_033__document_search_indexes.sql gives the query its support: the pg_trgm extension and a GIN trigram index on document_text.text_content, which makes an ILIKE search over Thai text fast, a function dochub_to_numeric for numeric comparisons on field values, and two indexes on document_field.

### Step 7

**In the story.** DocumentSearchService: builds each row: case number, document type, stored date, source, the matched field or a text snippet of 60 characters with the term highlighted and other personal identifiers masked.

The service builds the result rows with no person involved. Each row carries the case number, read through CaseDirectory.caseNumbers, the document type, the stored date, the source, and either the matched field with its value or a text snippet. Build SnippetBuilder for the snippet: 60 characters of the OCR text around the matched term, with the term highlighted and any other personal identifier in that window replaced by a token through the ACE PII service. A result that matched on a field shows the field value instead of a snippet. The masking applies even for a role allowed to search the text, because other people can be named in the same line.

### Step 8

**In the story.** DocumentSearchService: writes the access event DOCUMENT_SEARCH (user, role, criteria with the free text term as a SHA-256 hash, result count, case IDs returned) through the PII access log and waits for the confirmation.

The service writes the access event and waits, with no person involved. Build the DOCUMENT_SEARCH event with the user, the role, the criteria, the result count and the case IDs returned, and send it to the PII access log of the ACE common module. The free text term goes in as a SHA-256 hash, which is a one-way fingerprint of the text: the same term always gives the same value and the term cannot be read back out, so the log holds no personal data. Wait for the write to be confirmed. Without a confirmation, return 503 with MSG-P5-019 and no result rows, because a read of personal data is allowed only once it is recorded.

### Step 9

**In the story.** Front end: shows the first page of 50 rows; the user opens a row in DocumentDetailPanel (RWB-E1-024).

The user sees the results and works with them. Render the first 50 rows with paging controls, driven by the page and size values of the response, and show the capped flag with MSG-P5-021 and the count 1000 when more documents matched than the limit allows. Build the other screen states as well: skeleton rows while loading, the empty state with the text No documents match this search and the action Clear the search, and an error state showing the message from section 14 at the top. Clicking a row opens DocumentDetailPanel, built in RWB-E1-024, so you reuse that component rather than building a second detail view.

## RWB-E1-034 Letter template management

Module: P6 Communications

### Step 1

**In the story.** Litigation officer: opens SCR-33 Template approval and chooses the template code and language, or a new code.

A person starts this. The litigation officer opens SCR-33 Template approval, which you build as the React component TemplateApprovalScreen in folder recovery/comms/templates. The screen lists templates by code and language from GET /templates, which needs Documents R and applies the caller's scope. The officer picks an existing pair, for example DEMAND-MTG with language TH, to add the next version, or types a new code for a template that does not exist yet. Show the versions of the chosen pair with their state, approver and valid from date, so the officer can see what is current before uploading anything. The common loading and error states apply to the screen.

### Step 2

**In the story.** Litigation officer: uploads the DOCX body and enters product group, channel, notice type, signature basis and the merge codes used.

The same person continues. The screen sends POST /templates as multipart with the DOCX file and the fields templateCode, language, productGroup, channel, noticeType, signatureBasis and mergeCodes. A merge code is a placeholder in the letter body that the generation step later replaces with a value from the case, for example CASE_NO or TOTAL_OUTSTANDING. The caller needs Documents C, which RW-LITOFF and RW-LEGAL hold. Build the upload form with each field required where the contract says so. Keep the allowed file types in property rwb.comms.template.allowed-types rather than in code; DOCX is the only value in Epic 1.

### Step 3

**In the story.** System: checks the role (Documents C), the required fields, the file type and size, and every merge code against the catalog (MergeCodeScanner from RWB-E1-046).

This happens on its own in TemplateAdminService, before anything is stored. Refuse a caller without Documents C with 403 and MSG-P4-002. A missing template code or language is 422 with MSG-GEN-001 naming the field. A file that is not DOCX is 415 with MSG-P6-010, and a file above rwb.comms.template.max-size-mb, which is 10, is 413. Then run MergeCodeScanner from RWB-E1-046 over the body and test every merge code it finds against the merge field catalog in force. An unknown code such as LINE_ID is 422 with MSG-P6-006 naming it, no version row is created and no file is kept.

### Step 4

**In the story.** System: stores the body write-once, creates the next version number in state Draft and shows it in the list.

This happens on its own. TemplateBodyStore writes the DOCX through the ACE storage pattern into a write-once container and returns body_ref. Write-once means a stored body can never be overwritten, so a correction is always a new version. Then insert the template row with the next template_version for that code and language, state Draft, created_by and the fields from the upload. Assign the number inside a transaction with SELECT ... FOR UPDATE on the highest existing version of that code and language, so two uploads at the same moment cannot take the same number; the unique constraint uk_template_version from RWB-E1-046 is the backstop. The response is 201 with the Template.

### Step 5

**In the story.** Legal counsel: opens the Draft version, reads the body and the merge codes, enters the valid from date and approves.

A second person acts. Legal counsel opens the Draft version on SCR-33, downloads the body through GET /templates/{templateId}/content and reads the merge codes shown beside it. Offer Approve with a valid from date only in the Draft state and only to a role holding Documents A. The action sends POST /templates/{templateId}/approve with validFrom and an Idempotency-Key header. Idempotency means the same key sent twice returns the first result and changes nothing, so a repeated click leaves one approval in the audit log. Hide the action from roles without Documents A, and check the right on the server as well, because hiding a button is not a control.

### Step 6

**In the story.** System: checks the role (Documents A), that the approver is not the uploader (CTL-05), that the version is Draft and that valid from is not before today; sets state Approved with approver and approval time.

This happens on its own in TemplateAdminService, as four checks. A caller without Documents A gets 403 with MSG-P4-002. An approver whose user ID equals created_by gets 409 with MSG-P7-002, the separation of duty rule that nobody approves their own work. A version in any state other than Draft gets 409 with MSG-P3-005. A valid from date before today gets 422 with MSG-GEN-003. When all four pass, write state Approved, approved_by, approved_at and valid_from. Use the optimistic lock on the version column, so a second approver acting at the same moment gets 409 with MSG-GEN-004 instead of overwriting the first approval.

### Step 7

**In the story.** System: from valid from, TemplateCatalog returns this version as current; earlier Approved versions stay readable on SCR-33.

This happens on its own, with no further action by anyone. The current version is derived, so there is nothing to switch over: TemplateCatalog from RWB-E1-046 picks, for a code and language, the Approved version with the latest valid_from that is on or before the date asked for. A version approved with valid from today becomes current today, and one approved with a later date becomes current on that date. Earlier Approved versions keep their rows, their approver and their approval time, and stay visible on SCR-33 to any role with Documents R. That is how the bank shows which wording was approved when a notice was sent.

### Step 8

**In the story.** Legal counsel: may withdraw an Approved version with a reason; the system sets state Withdrawn and generation for that code and language holds (R-LIT-04).

A person starts this and the system then holds generation. Legal counsel sends POST /templates/{templateId}/withdraw with a reason. An empty reason is 422 with MSG-GEN-001, and a version that is not Approved is 409 with MSG-P3-005. Write state Withdrawn and keep the reason on the row for the screen to show. From then on TemplateCatalog throws TemplateWithdrawnException with MSG-P6-003 for that code and language, so notices wait until Legal approves a new version. Do not fall back to the earlier Approved version. Resuming the held notices once a new version is approved is built in RWB-E2-021.

### Step 9

**In the story.** System: writes every upload, approval and withdrawal to the ACE audit log with the user, the version and the time.

This happens on its own in TemplateAdminService on all three actions. Write one ACE audit entry per action, holding the user ID, the template code, the version number and the time. Hold nothing else: no body text and no personal data, so test bodies carry synthetic wording only. The Idempotency-Key store makes the count exact, because an approve repeated with the same key returns the first response and adds no second entry. These entries are what control CTL-14 rests on, showing for any notice which version was in force and who approved the wording.

## RWB-E1-035 Case record view v1.1 with documents and history timeline

Module: P3 Case and workflow

### Step 1

**In the story.** Case owner: opens SCR-03 for case RW-2026-000801 and selects the Timeline panel.

A person does this. The case owner is already on SCR-03 Case record from RWB-E1-023 and chooses the Timeline panel, which this story adds. Build TimelinePanel in src/modules/recovery/casewf/caserecord/timeline and show skeleton rows while the call is running. The panel appears only when the feature flag rwb.p3.timeline is on; with the flag off, SCR-03 hides the panel and the endpoint answers 404. Nothing is fetched until the panel is selected, so opening the case record itself is not made slower by this story.

### Step 2

**In the story.** TimelinePanel: calls GET /cases/{caseId}/timeline with page 0 and size 50.

The panel makes this call by itself when it opens. The endpoint is new work for you: api.yaml first lists it for Epic 2, and this story delivers it in Epic 1 behind the flag. Add page and size as query parameters. Paging means the server returns a slice of the events together with the total count, so a long history arrives in parts; page 0 with size 50 asks for the first fifty. The panel shows the total beside the items and asks for the next page when the user moves on. Paging with the total is build step 3.

### Step 3

**In the story.** CaseAndWorkflowController: checks Case record R and the scope.

The controller runs this check on every call, with no person involved. A caller whose role does not include Case record R receives 403 with MSG-P4-002, which is what the access test does with RW-REFADM. A case outside the caller's scope receives 404 with MSG-P4-003, so RW-CASEOWN reads own cases, RW-TEAMMGR reads team cases, and RW-CONDUCT and RW-AUDIT read every case. Reuse the controller and the scope check that already serve the other case endpoints; this story adds one more method to them rather than a second check of its own.

### Step 4

**In the story.** TimelineService: reads interactions and assignments from P3 tables, documents through the P5 interface and decision log entries through the P7 interface, for the case.

The service gathers from four places on each request. Read interaction and assignment through CaseAndWorkflowRepository, using the indexes ix_interaction_case_time and ix_assignment_case_id. Call DocumentQuery.documentsForCase for the documents and DecisionLogQuery.entriesForCase for the decision log entries; those tables belong to P5 and P7 and may not be queried directly. Give each outside call the limit in caserecord.section.timeout.ms, 3000 milliseconds. When the decision log does not answer, return the other three sources and MSG-P3-023 for Decisions, so a slow module costs one section only. This partial result is build step 4.

### Step 5

**In the story.** TimelineService: maps each record to a TimelineItem with time, type, summary, by and reference.

TimelineItemMapper does this in code, with one mapper per source. The four sources hold different shapes of record, so each one becomes the same TimelineItem: at for the time, type for the kind of event, summary for one line of text built from code values and their labels, by for who or what caused it, and reference for the record it points back to. Keep personal data out of the summary and follow the masking rules by role for anything taken from a contact. Build step 1 covers the four mappers with their unit tests.

### Step 6

**In the story.** TimelineService: sorts by time, then by a fixed type order for equal times, then by record ID, and returns the page with the total.

The service sorts the merged list itself. Two events can carry the same timestamp, and a sort on time alone would then put them in any order, so two tie breaks follow. First the type order held in the parameter timeline.type.order: decision, status change, assignment, transfer, contact, document. Then the record ID, which settles two events of the same type at the same time. The result is the same on every opening, which AC5 checks with an assignment and a decision log entry both at 07:00:00. Return the slice the caller asked for together with the total count of events.

### Step 7

**In the story.** TimelinePanel: shows each item with an icon for its type; "by" shows a person's name, or a rule ID with its version.

The panel renders what the service returned. Give each type its own icon so a reader sees the kind of event without reading the text. For the by value, show the person when a person acted, and show the rule ID together with its version when a rule acted, taking rule_id and rule_version from the record. The version matters because rule rows change over time and the panel has to show which version was in force when the event happened. A new case whose only record is its creation entry shows one item with the entry rule and its version.

### Step 8

**In the story.** Case owner: opens a transfer item; the panel shows the transfer reason, the from and to queue and owner, and the rule version.

A person opens the item, and the panel shows detail it already holds from the call. Build the detail view for a transfer: the transfer reason from transfer_reason_code with its label from LOV-TRANSFER-REASON, the owner and queue the case moved between, and the rule version. AC2 shows the shape with reason R04 Owner absent, the from owner, the to owner and rule version TRF-2026.11. The response fields reasonCode, fromQueueCode, toQueueCode and ruleId carry this detail. The panel and the item detail are build step 6, with test TC-E1-035-02 on a manual transfer.

## RWB-E1-037 Role to permission matrix as data and PDPA field masking by role

Module: P4 Access and administration

### Step 1

**In the story.** Reference data administrator (RW-REFADM): prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls POST /admin/reference-loads with table "permission" and validFrom.

A person starts this. The reference data administrator, holding RW-REFADM and the right C in Reference data, builds the matrix file from the approved workbook, puts the application owner's approval reference in the file header, and posts it to POST /api/recovery/v1/admin/reference-loads as multipart form data with the file, table set to permission and a validFrom date. The endpoint already exists from RWB-E1-043; your work is the handling behind it for the permission and masking_rule tables, through AccessAndAdministrationController. The approval that the file header names happens outside the Workbench, so your code carries the reference and never checks it. A repeat with the same Idempotency-Key header returns the first response.

### Step 2

**In the story.** Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.

The Workbench does this with no person involved. Build PermissionMatrixLoader to check the whole file before it keeps any part of it: every active role appears exactly once for each of the 14 capability areas, the letters come from C, R, U, D, A in that order or the single character -, and every role code is known. A file with any error is refused in full with MSG-P1-002, which names the failed check, and the version in force stays untouched. A file that passes is stored as rows in the permission table with status Loaded and the new matrix_version. Add the unique index uk_permission_version on permission (matrix_version, role_id, capability_area) so that one role and area cannot be stored twice for a version.

### Step 3

**In the story.** Security administrator (RW-SECADM): reviews the difference report against the version in force and calls POST /admin/reference-loads/{loadId}/approve.

A second person acts here. The security administrator, holding RW-SECADM, reads the difference report against the version in force and calls POST /admin/reference-loads/{loadId}/approve. Build that difference report in the loader so that the approver can see which letters changed before deciding. The request has no body. Nothing of the loaded version takes effect until this call succeeds, which is why the work is split across two roles: RW-REFADM may load and may never approve, and RW-SECADM approves for the permission table. A repeat approve of a version already approved returns 409 and writes nothing.

### Step 4

**In the story.** Workbench: checks that the approver holds the role the parameter names for the table and is not the person who loaded it; writes one decision log entry for the approval with decision code AC-VERS and no case; marks the version Approved with its valid from date.

ReferenceLoadApprovalService does all of this in one transaction, meaning the checks, the decision log entry and the status change commit together or none of them commits. Read the approver role for the table from the parameter catalog: rwb.refload.approver.permission names RW-SECADM and rwb.refload.approver.masking_rule names RW-COMPLY. A caller without that role is refused with 403 and MSG-P4-002. The person who loaded the version may never approve it, which returns MSG-P7-002 and leaves the version Loaded. Then write one decision log entry through the P7 writer with decision code AC-VERS and no case, and set the version to Approved with its valid from date. A failed decision log write leaves the version Loaded and returns 503 with MSG-P7-003.

### Step 5

**In the story.** Workbench: from the valid from date, every new session resolves the new version (RWB-E1-022 keeps open sessions on their version), and the screens and endpoints of the new letters open with no deployment.

This happens on its own, with no deployment and nobody pressing anything. From the valid from date, each new session reads the approved version when it resolves the caller's rights, so the screens and endpoints that the new letters open start working. Sessions already open keep the version they resolved at sign-in, which RWB-E1-022 handles. Your work is to make the lookup of the version in force a query by date instead of a value in code, so that AC1 passes: a user holding RW-LEGAL gets 403 from GET /queues under PM-2026.11 and 200 under PM-2026.12, with the same build deployed.

### Step 6

**In the story.** Person: requests a list or a record; ScopeService builds the filter from the role's default scope (own, team, region, all) and the person's teams and regions; the owning module applies it in its query.

A person makes the request, and two parts of the Workbench share the work. Build ScopeService as a published interface with scopeFor(SessionContext), returning a ScopeFilter that carries the type OWN, TEAM, REGION or ALL, the user reference, the team codes and the region codes. The type comes from role.default_scope, and the teams and regions come from the P3 queue membership interface of RWB-E1-019. The owning module then puts that filter into its own query, because this package may not read another module's tables. OWN covers cases the person owns or has a task on, TEAM the cases in their team queues, REGION the cases in the regions of their teams, and ALL every case. Scope filters first, and the permission check follows.

### Step 7

**In the story.** Workbench: AccessCheck tests the right in the capability area on the records inside the scope.

The Workbench does this, through the AccessCheck of RWB-E1-022 that runs on every endpoint. The check reads the letters that the matrix version in force gives the session's roles for the capability area the endpoint belongs to, and refuses the call with 403 and MSG-P4-002 before the handler runs. A capability area holding - refuses every action in it. The refusal is written as an event with the area and the right that was missing, for example area QUEUE_AND_ALLOCATION and right U when a case owner calls the transfer endpoint. The check itself needs no new code; confirm it through the AccessCheckInterceptor on that endpoint, and make sure the records reaching it are already limited to the scope from step 6.

### Step 8

**In the story.** Workbench (FieldMasker): masks every field tagged as personal data unless the masking rule in force lets one of the session's roles see it; unmasked values are fetched through the ACE PII service, which logs the read to PII Kafka (INT-22).

The Workbench does this, in code you build as the published interface FieldMasker. Mark every personal field on a DTO with the annotation @PersonalData carrying its field ID, which covers the party identity number, the date of birth and the contact point value. FieldMasker then replaces each value unless a row in the masking version in force gives one of the session's roles unmasked true for that field. A field with no row is masked, so a session makes no request for a clear value it may not see. Where a rule does allow it, fetch the clear value through the ACE PII service, which logs the read to PII Kafka as INT-22. Masking runs before data reaches a screen or an agent. The number of characters kept comes from rwb.access.mask.keep-last, set to 4.

### Step 9

**In the story.** Workbench: on each request, compares the session's groups with the groups the ACE common module holds for the person (refreshed at most every 5 minutes, assumed; DL38); if a group has been removed the session ends and the request is refused.

The Workbench does this on every request, in SessionRevalidationFilter. Compare the group memberships held on the session with the memberships the ACE common module currently holds for that person, refreshed at most every five minutes under rwb.access.membership-refresh-minutes. When a group that gave the person a role has gone, end the session and refuse the request with 401 and MSG-P4-001, and refuse a new sign-in as well. Removal from the Entra ID group is the work of the bank access administrator and is started by the line manager, both outside the Workbench, so your code only reacts to the change. Test it with a group removed in the ACE test double during an open session.

## RWB-E1-038 Delegation of authority table as reference data

Module: P4 Access and administration

### Step 1

**In the story.** Reference data administrator (RW-REFADM): converts the Delegation of authority matrix to the load file: one row per limit and decision code, for MORTGAGE and SSME, amounts converted from THB million to baht.

A person prepares this by hand, the reference data administrator. The source is the Delegation of authority matrix, where one limit can cover several decision codes and regulation items, so the file holds one row per limit and decision code, and the same limits are repeated for product MORTGAGE and for product SSME. Build the converter template that guides this work: amounts in THB million become baht, No limit becomes an empty cell, Up to X percent becomes loss_pct_limit, At least X percent against fair market value becomes min_price_pct_fmv, and Once and Twice become max_delay_count. Amounts are never converted or rounded later, so the file carries baht with two decimals.

### Step 2

**In the story.** RW-REFADM: calls POST /admin/reference-loads with table "delegation_limit", validFrom and the version name, for example DOA-2026.11.

The same person uploads the file to the endpoint built in RWB-E1-043. The request is multipart: the file, table set to delegation_limit, and the valid from date, with the version name carried in the file, for example DOA-2026.11. The response is 201 with a ReferenceLoad holding the load ID, the table, the valid from date, status Loaded and the row count. The caller sends an Idempotency-Key header, so a repeated request creates no second load. The endpoint refuses a caller without the Reference data C right with 403 and MSG-P4-002, a version name that already exists with 409 and MSG-GEN-004, and a file that fails validation with 422 and MSG-P1-002.

### Step 3

**In the story.** Workbench (DelegationLimitLoader): validates the file whole and stores 218 rows with status Loaded.

Your code runs this with nobody watching. Write DelegationLimitLoader and check the whole file before you write anything: every decision code, approval level and product is a known value in LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT, no required field is empty, no two rows repeat the same decision, regulation item, product, level and limits, and the highest principal limit of a level does not fall below the limit of the level under it. One failure refuses the whole file with MSG-P1-002 and leaves the version in force untouched. When every row passes, insert the rows with the version name and status Loaded, which means written and not yet usable by the lookup.

### Step 4

**In the story.** Risk and model risk officer (RW-RISK): reviews the difference report and calls POST /admin/reference-loads/{loadId}/approve.

A second person acts here, the Risk and model risk officer. The load response carries a difference report showing what the new version changes against the version in force, and that officer reads it before approving. They then call POST /admin/reference-loads/{loadId}/approve with the load ID in the path. Build no screen for this; the officer sees the difference report and the approval result in the endpoint responses until SCR-41 arrives in Epic 8. The approver role for this table is held in the parameter rwb.refload.approver.delegation_limit, set to RW-RISK, so read the role from the parameter rather than writing RW-RISK into your code.

### Step 5

**In the story.** Workbench: checks that the approver holds RW-RISK and did not load the file; writes one decision log entry with decision code AC-VERS and no case; sets valid_to on the rows of the previous version to the day before the new valid from; marks the new version Approved.

Four things happen automatically in one call, and their order matters. Reuse ReferenceLoadApprovalService, shared with RWB-E1-037. Check the approver's role against the parameter and refuse with 403 and MSG-P4-002 otherwise, then check that the approver is not the user who loaded the file and refuse with 409 and MSG-P7-002. Next write one decision log entry with decision code AC-VERS and no case ID, naming the version and its valid from date. Only then close the previous version by setting valid_to to the day before the new valid from, and mark the version Approved. A failed decision log write answers 503 with MSG-P7-003 and leaves the load Loaded.

### Step 6

**In the story.** Approval router (RWB-E2-013): calls DelegationOfAuthority.lowestLevel with the decision, the regulation item (one decision code can cover several items, for example D7.5 covers items 2.1.4, 2.1.6 and 2.1.9), the product, the amounts, the conditions and the decision date.

Another module calls your code, and no person is involved. The approval router of RWB-E2-013 calls the published interface DelegationOfAuthority.lowestLevel, which you offer from package recovery.access.delegation. The DelegationRequest carries the decision code, the regulation item, the product group, applies_when, the principal in baht, the loss percentage and loss amount, the price percentages, the received percentage, the delay count, the term in years, the related party flag and the decision date. The regulation item is in the request because one decision code can cover several items, for example D7.5 covering items 2.1.4, 2.1.6 and 2.1.9, and each item has its own limits. Your lookup never guesses the item.

### Step 7

**In the story.** Workbench (DelegationLookupService): walks levels L6 to L1 over the rows valid on that date and returns the first level with a row that covers the request, the row IDs and the version.

Your code computes the answer. Write DelegationLookupService to read the delegation_limit rows whose valid from and valid to span the decision date for that decision code, regulation item, product and applies_when, then test them from L6, the lowest level, upward to L1, the Board. The first level with a row that covers every figure in the request is the answer. Where a level has two rows, the level qualifies when either row is met. An empty limit column means no limit on that figure. Return the status COVERED, the approval level, the row IDs used, the version name, and the holder and substitute user IDs. The lookup index serves this read.

### Step 8

**In the story.** Workbench: where no row covers the request at any level, returns NOT_COVERED and raises an incident to RW-RISK naming the decision and product.

Your code handles this case automatically. When no row at any level covers the request, for example a hire purchase decision before the chapter 8 limits are supplied, answer with status NOT_COVERED in place of a level, so the caller holds the item rather than letting it through. Raise an incident through the ACE incident path to the RW-RISK queue naming the decision code and the product group, with MSG-P7-010 as the message the user sees. Do not fall back to L1 and approve nothing. Test this with a request for decision D6.4, item 2.1.1 and product HIRE_PURCHASE against a version that holds no hire purchase rows.

## RWB-E1-039 Access log into the decision log and break-glass admin

Module: P4 Access and administration, with P7 Decision center and log

### Step 1

**In the story.** Person: signs in, or reads a case record, a document or a list, or exports a list.

A person starts this. Every bank role generates access events by working normally: signing in, opening a case record, opening a document, listing cases and exporting a list. Those actions are what the rest of this story has to record, each with its own event code from LOV-DECISION: AC-SIGN for a sign-in, AC-READ for a read, AC-EXPT for an export and AC-DENY for a refusal. The data steward loads those codes with this story. There is no code to write for this step alone; it names the points your code has to cover. The measure in section 2 is that 100 percent of reads of the case store and the document store reach the access log.

### Step 2

**In the story.** Owning module: calls AccessEventPublisher.publish with the event, the case ID where there is one, and the field IDs returned with their masking position, or the filter and row count for a list or export.

The module serving the read makes this call in its own code, with no person involved. AccessEventPublisher is the interface published in RWB-E1-022, and this story extends it. Your work is to add the publish call to the case read and the list export in the case store module and to the document content read in the document hub, each through the published interface rather than by writing to the log directly. The AccessEvent you pass carries the event code, the actor, the case ID where the action has one, the capability area and right, the result, the field IDs returned with a flag saying which were masked, and, for a list or an export, the filter used and the number of rows. Pass field IDs and the masking position only, never field values. Sign-in, refusal, export and break-glass events carry no case ID.

### Step 3

**In the story.** Workbench (AccessLogWriter): writes one decision log entry with an access event code, the actor, the area, the result and the details in actions, in the same transaction as the read response is built; if the write fails, the read returns nothing.

Your code does this; no person is involved. Build AccessLogWriter to turn an AccessEvent into a decision log record and write it through the P7 DecisionLogWriter, inside the transaction the caller already opened for the read. A transaction is a group of database changes that either all take effect or none do, so the entry and the answer to the user succeed or fail together. The entry holds the access event code, the actor, the capability area and right and the result, with the rest of the detail in the actions field: fields returned, filter, row count, and the grant and incident where one applies. The store itself is append only and hash chained from RWB-E1-008, and this story adds no table. When the write fails, return 503 with MSG-P7-003 and no data, and raise an incident to the platform administrator queue.

### Step 4

**In the story.** Platform administrator (RW-PLATADM): raises a break-glass request in the bank IAM naming the open incident, the capability area, the scope and the reason; the security administrator approves it there, and the IAM adds the administrator to the break-glass group until the window ends.

Two people do this, and it happens outside the Workbench. Break-glass means emergency access beyond the rights a role normally holds. The platform administrator raises the request in the bank IAM, naming the open incident, the capability area, the scope and the reason, and the security administrator approves it there. The IAM then adds the platform administrator to the break-glass group for that environment, with an end time; the group name follows DL40 and is RWB-SIT-BREAKGLASS in SIT. You build none of this flow, and the request, approval and review records stay in the IAM. What your code later needs from it is one thing: whether the caller is in the break-glass group, and when that membership ends.

### Step 5

**In the story.** RW-PLATADM: calls POST /admin/break-glass with the incident reference, the IAM request ID, the area, the right, the scope and the reason.

A person makes this call. Approval in the bank IAM does not open the grant by itself; the platform administrator has to activate it in the Workbench. Build the activation endpoint to take a BreakGlassActivation holding the incident reference, the IAM request ID, the capability area from LOV-CAPABILITY, the right as C, R or U, the scope from LOV-SCOPE and a reason of 20 to 1000 characters. It answers 201 with a BreakGlassGrant carrying the grant ID, which is the ID of the AC-BGON entry, the incident reference, the area, the right, the scope and the start and end times. The caller needs Platform administration C and membership of the break-glass group. The call takes an Idempotency-Key header.

### Step 6

**In the story.** Workbench (BreakGlassService): checks the break-glass group, the incident reference pattern and the reason length; writes an AC-BGON entry; sets the session grant to end at the earlier of the window end and the group end.

Your service does this with no person involved. Build BreakGlassService with three checks before anything is granted. First, membership of the break-glass group: a caller outside it is refused with 403 and MSG-P4-007, and an AC-DENY entry with reason NO_BREAKGLASS_GRANT is written. Second, the incident reference against the parameter rwb.access.breakglass.incident-pattern; a missing reference gives 422 with MSG-GEN-001 naming the field. Third, the reason length against rwb.access.breakglass.reason-min, with 422 and MSG-GEN-002 below it. Then write the AC-BGON entry, whose entry ID becomes the grant ID. Set the end time to the earlier of the window from rwb.access.breakglass.window-hours and the group end: in AC2, 10:30 plus four hours gives 14:30, which is earlier than the group end of 18:00. A second activation with a new key while a grant is active answers 409.

### Step 7

**In the story.** Workbench: marks every entry written while the grant is active with the grant ID and the incident reference; the ACE front end shows the MSG-P4-004 banner with the end time.

This happens in code while the person works. Build BreakGlassGrantCheck to add the grant right, in its area and scope, to AccessCheck until the grant end time, and to put the grant ID and the incident reference on every decision log entry written for that user while the grant is active. AC8 shows the result: the read at 11:02 carries incident INC0004521 and the two ordinary reads do not. For the screen part, add the break-glass fields to GET /me/session and build the React component BreakGlassBanner, which shows MSG-P4-004 with the end time in the front end shell. This story has no screen of its own, so the banner is the only visible part.

### Step 8

**In the story.** Workbench: after the end time, AccessCheck ignores the grant with no action by anyone.

No person ends the grant and no job ends it. Check the end time on every request instead, so that from the first request after the end time AccessCheck uses only the letters RW-PLATADM holds in the permission matrix version in force. A call the grant allowed is then refused with 403 and MSG-P4-002, and the refusal is written as an AC-DENY entry. AC2 gives the case to test: the same PATCH on a task is allowed at 14:20 under the grant and refused at 14:31, because RW-PLATADM holds only R in Case record. Test it with a clock fixed at 10:30 and then moved to 14:31, so the end is checked without waiting four hours.

### Step 9

**In the story.** Security administrator: reviews each use inside the review window from GET /admin/access-log with event AC-BGON and the entries marked with its incident, and records the review in the bank IAM.

A person does this: the security administrator, who holds Platform administration R, and who may not review their own use. The review window comes from the parameter rwb.access.breakglass.review-days, one working day. Your work is the query behind it. Build AccessLogQueryService and the endpoint GET /admin/access-log, mapping the query onto the P7 DecisionLogReader interface rather than reading the log table. The query takes user, from, to, event, page and a size of 1 to 500, and returns AccessLogPage of entries with the time, the actor, the event code, the capability area and the result. Refuse a caller without Platform administration R with 403 and MSG-P4-002, and answer 422 when from is later than to or the size is outside the range. The review itself is recorded in the bank IAM.

### Step 10

**In the story.** Internal audit (RW-AUDIT): asks who read a case over a period through GET /decision-log with caseId, decision AC-READ, from and to.

A person does this. Internal audit reads and changes nothing. The endpoint already exists as the decision log query, and it takes the case ID, the decision code AC-READ, a from date, a to date, the page and the size, returning a page of decision log entries under Decision log right R with scope applied. This answer is complete only because step 3 wrote one entry for every read, so your work here is in the entries rather than the endpoint: actor, time and the field IDs in actions have to be there. AC8 gives the test: three reads of one case on 3 December 2026 come back in time order, and the 11:02 read carries incident INC0004521. The screen for this query, SCR-38, comes in RWB-E2-005.

## RWB-E1-040 Document checklist per case type as reference data

Module: P5 Document hub

### Step 1

**In the story.** Reference data administrator: loads the checklist file with POST /api/recovery/v1/admin/reference-loads, table DOCUMENT_CHECKLIST; the owner approves it.

Two people are involved and nothing starts on its own. The reference data administrator, RW-REFADM with Reference data C, sends a multipart request to POST /api/recovery/v1/admin/reference-loads with the file, table set to DOCUMENT_CHECKLIST and a validFrom date. A second person holding Reference data A approves it, and the response of the load itself is 201 ReferenceLoad. No role holds Reference data A in the permission matrix today, so the right is assumed granted to the legal counsel as co-owner of the checklist under DL01. The version for this release is CHK-2026.11. Stages, routes and required types stay rows, never code.

### Step 2

**In the story.** ChecklistLoader: validates every row: stage in LOV-STAGE, route in LOV-ROUTE or empty, document type in the type table in force, no duplicate row; refuses the load whole on any error.

The loader runs on its own when a file arrives. Build ChecklistLoader against the ReferenceTableLoader interface for table DOCUMENT_CHECKLIST. Check each row: the stage is in LOV-STAGE, the route is in LOV-ROUTE or empty, the document type is in the document type table in force from RWB-E1-025, and no row repeats. One bad row refuses the whole file, nothing is written, and the version already in force keeps serving. Row errors answer 422 with MSG-P3-027 naming the row and the error, and a version already loaded answers 409 with the same message. AC7 is the test, with type POWER_OF_ATTORNEY absent from the type table.

### Step 3

**In the story.** ChecklistEvaluator: on DocumentStored (EV-16), on CaseStateChanged (EV-05) and when a checklist version takes effect, takes the case's stage and route through CaseDirectory.

The evaluator runs on events, with no person pressing anything. Build ChecklistEvaluator plus two listeners, DocumentStoredChecklistListener for DocumentStored, EV-16, and CaseStateChangedChecklistListener for CaseStateChanged, EV-05. Each listener keeps the event ID so a second delivery of the same event is ignored and counted, and after the retry limit the event goes to the exception queue with the platform administrator as owner. The evaluator asks the P3 published interface CaseDirectory for stage_code, route_code and owner, and never reads the P3 tables. The third trigger is the job step of step 8. The evaluator only reports and never blocks a case from moving stage.

### Step 4

**In the story.** ChecklistEvaluator: picks the rows of the version in force for that stage, using the rows for the route where they exist and the rows with no route otherwise.

The evaluator does this as part of each recompute. Read from document_checklist_item the rows whose table_version is in force on the business date and whose stage_code matches the case stage. Where rows exist for the case route, use those; where none exist for the route, use the rows with an empty route. Index ix_checklist_stage on stage_code and valid_from supports the read. A version takes effect on its valid_from date with no deployment, so the date decides which rows apply rather than a release. When the stage has no rows at all, the result is the empty checklist of exception path X1, which AC6 tests at stage DEBT_SALE.

### Step 5

**In the story.** ChecklistEvaluator: counts the active documents of each required type on the case and writes case_document_check: checklist version, required count, present count, missing types and complete.

The evaluator writes the result; no person edits it. Count documents on the case by document_type where is_active is true, counting each type once even when the case holds several versions of one document, so an appraisal report at version 2 with version 1 inactive counts as one present. Write one case_document_check row per case, unique on case_id, holding checklist_version, required_count, present_count, missing_types as jsonb, complete, checked_at and last_event_id. The complete flag is false while a required type is missing, true when every required type is present, and empty when the stage has no checklist. AC3 expects complete false, missing count 1 and missing type SETTLEMENT_AGREEMENT.

### Step 6

**In the story.** Litigation officer: opens the Documents tab (SCR-30); GET /cases/{caseId}/document-checklist returns each required item marked present or missing.

A person reads the result here. Extend the endpoint that RWB-E1-026 built as a placeholder so GET /api/recovery/v1/cases/{caseId}/document-checklist returns DocumentChecklist with caseId, checklistVersion, stageCode, items holding documentType, label, required and presentCount, plus missingCount and complete. Build DocumentChecklistPanel, the React component that replaces the placeholder on SCR-30, with skeleton rows in its Loading state and MSG-P5-023 above the list when a type is missing. Authorization is Documents R with scope applied, so a role without the right is refused with 403 and MSG-P4-002, and a case outside the reader's scope with MSG-P4-003.

### Step 7

**In the story.** Case owner: sees the number of missing documents for each case on the case list (SCR-02) through DocumentChecklistService.missingCounts.

The case owner reads this, and the count comes from the stored flag rather than a fresh count per row. Build the published interface DocumentChecklistService with forCase and missingCounts, where missingCounts takes up to 500 case IDs in one call and returns the missing count per case. The P3 case list calls it, because P3 never reads case_document_check itself. Build MissingDocumentsBadge for the SCR-02 rows, showing nothing when the count is 0, and let the list be filtered to cases with one or more missing documents. AC3 expects the owner to see 1 missing for the deed in lieu case.

### Step 8

**In the story.** JOB-12 Document intake: the step checklistRefreshStep finds checklist versions whose valid from date has been reached since the last run and recomputes the cases of the stages they change.

The job step runs on a schedule. Add ChecklistRefreshStep to JOB-12 Document intake. Each run looks for checklist versions whose valid from date has been reached since the previous run, then recomputes case_document_check for the cases sitting at the stages those versions change. Without this step a case already at its stage would keep its old counts until its next document or stage event. AC2 is the test: version CHK-2026.12 adds GUARANTOR_NOTICE for DEED_IN_LIEU from 1 December 2026, and the case opened that day shows four items, with no code deployed between 30 November and 1 December 2026.

## RWB-E1-041 Retention classes and virus scan on intake

Module: P5 Document hub

### Step 1

**In the story.** JOB-12 Document intake: runs scanStep first, before ocrStep.

Automatic. JOB-12 already exists from RWB-E1-049 and runs every 15 minutes in business hours. Your change is to the job definition: put scanStep ahead of ocrStep, so no file is read for text until it has been checked for malware. The step runs under the service identity SY-OCR with Documents CRU rights, and no person starts it. With the feature flag rwb.dochub.malware-scan off, intake items are left unscanned, the OCR step does not read them, and an upload is refused with 503 and MSG-P5-022.

### Step 2

**In the story.** ScanStep: selects intake items with no scan_result and sends each file to MalwareScanClient.

Automatic. Write ScanStep to read document_intake rows whose scan_result is empty and pass each file to MalwareScanClient, the adapter to the bank malware scanning service. Each scan gets the timeout from the property rwb.dochub.scan.timeout-seconds, which is 30. The intake item ID is the key that makes the step safe to repeat: an item that already carries a scan result is not scanned again, so a rerun costs nothing and changes nothing. Build the client against a stub that flags the EICAR signature, the harmless test pattern scanners treat as infected, which AC1 uses in the file eicar-0002.pdf.

### Step 3

**In the story.** ScanStep: on CLEAN, sets scan_result CLEAN and scanned_at, so ocrStep may read the item; on INFECTED, moves the file to the quarantine container, sets scan_result INFECTED, writes the audit event MALWARE_BLOCKED and alerts the platform administrator; the file is never stored.

Automatic, and the two outcomes part ways here. On CLEAN, set document_intake.scan_result to CLEAN and scanned_at to the time of the scan, which is what lets ocrStep pick the item up; scanned_at is a new column in your migration. On INFECTED, call QuarantineMover to move the file from the intake container to the quarantine container named by rwb.dochub.container.quarantine, set scan_result to INFECTED, write the audit event MALWARE_BLOCKED with the intake ID and the source, and alert the platform administrator. No document row is created for that file and the OCR step never reads it. Keep the file name and content out of the audit event.

### Step 4

**In the story.** Upload (RWB-E1-026): calls MalwareScanService.scanNow before DocumentStore.store; INFECTED returns 422 MSG-P5-016; if the scanning service does not answer, the call returns 503 MSG-P5-022 and nothing is kept.

A person starts this one, by uploading a file in the dialog of SCR-30. The upload path built in RWB-E1-026 calls your published interface MalwareScanService.scanNow and waits for the answer before it calls DocumentStore.store. On INFECTED the caller gets 422 with MSG-P5-016 and the file is held in quarantine. When the scanning service does not answer, scanNow throws ScanUnavailableException, the caller gets 503 with MSG-P5-022, and neither a document row nor a blob is written. Your work here is the interface and the behavior behind it; the upload story makes the call.

### Step 5

**In the story.** DocumentStore (RWB-E1-024): stores clean files with the retention class of the type; legal types go to the write-once container.

This behavior comes from RWB-E1-024 and already exists, so check it rather than build it again. When a clean file is stored, the document row takes the retention class and the write_once flag from the document type table, and a file whose type is marked write_once goes to the write-once container, where stored content cannot be changed afterward. AC2 expects a demand letter of type DEMAND_LETTER to carry class LEGAL10Y with write_once true and to sit in that container. The retention job later reads those two values and never alters a write-once blob.

### Step 6

**In the story.** JOB-17 Retention job: runs on the first Sunday of each month; for each active document computes expiry date = stored date plus period_months of its class.

Automatic, on a Quartz schedule in Asia/Bangkok time, with no person starting it. Write RetentionJob to read every active document with its retention class, look the class up in the retention table version in force, and add period_months to the document's created_at date, which serves as the stored date. A document is due when that expiry date falls on or before the run date. AC3 has a GENERAL05Y document stored 1 November 2021, so 60 months gives 1 November 2026 and the run on 6 December 2026 finds it due. AC10 shows that an expiry date equal to the run date is also due. Work in committed chunks of 500 documents, so a stopped run resumes.

### Step 7

**In the story.** RetentionJob: skips a document whose case has legal_hold true and counts it as held.

Automatic. For each due document the job asks the P3 published interface CaseDirectory for the legal hold flag of that document's case, and when it is true the job does nothing to the document: no archive, no row on the review list. Add one to the held count that goes on the job record. A legal hold outranks the retention class for as long as it is in place, which is what AC5 checks on case RW-2026-000789. Read the flag through CaseDirectory rather than from the case table, because the case data belongs to another module.

### Step 8

**In the story.** RetentionJob: for a due document with end action ARCHIVE, writes the decision log entry DOCRET, moves the blob to the archive tier and sets the document state ARCHIVED; for end action REVIEW, adds it to the review list for Compliance and changes nothing.

Automatic, and the end action of the class decides which path a document takes. For ARCHIVE, write the decision log entry with code DOCRET naming the document, its class, the table version and the expiry date, then move the blob to the archive tier and set the document state to ARCHIVED. Write the entry first: when that write fails the document is left as it is, MSG-P7-003 goes on the job log and the next run tries again. For REVIEW, add the document to the review list for Compliance and change neither the row nor the blob. The unique pair of document_id and run_month in retention_action keeps a document from being acted on twice in one month.

### Step 9

**In the story.** RetentionJob: writes the review list to retention/review/{runDate}.csv in the standard container and the counts (due, archived, listed, held, exceptions) to the job record.

Automatic. Build RetentionReviewWriter to write one CSV file per run at retention/review/{runDate}.csv, holding each listed document with its class and expiry date, together with any document whose class is missing from the version in force, marked as the exception RETENTION_CLASS_MISSING. AC4 names the file retention/review/2026-12-06.csv for the 6 December 2026 run. Write the five counts of due, archived, listed, held and exceptions to the job record, so the compliance and PDPA officer and the platform administrator read them on SCR-44. A rerun in the same month archives nothing again and leaves the listed rows as they were, which AC8 checks with 4 archived and 9 listed.

## RWB-E1-042 Central configuration service and parameter catalog

Module: P3 Case and workflow

### Step 1

**In the story.** Squad member: adds a parameter to `config/parameter-catalog.csv` with key, kind, type, unit, range, default, scope, required, owner role, environments and used by; the pull request is reviewed by the owner.

A squad member does this as a code change. The parameter is a line added to config/parameter-catalog.csv with key, kind, type, unit, range, default, scope, required flag, owner role, environments and the packages that use it. The pull request goes to the owner named on the line for review, following the code owner rule. Your work is the column set, because two build tools and a generated migration read this file. An environment setting and a secret each get a catalog line as well; the value of a secret lives only in the ACE secret store and never in the file. The Epic 1 lines include case.entry.dpd with default 90.

### Step 2

**In the story.** Build: generates the `ParameterKeys` class from the catalog file; code reads a value only through ParameterService with a generated key.

The build does this, not a developer by hand. ParameterKeysGenerator reads config/parameter-catalog.csv and writes the ParameterKeys class, giving each catalog line a typed constant such as ParameterKeys.CASE_ENTRY_DPD of type ParameterKey<Integer>. Application code then reads a value only through ParameterService.get with one of those constants and a business date. Because the constants are generated, a key the catalog does not list will not compile, and the type on the key stops an integer parameter being read as text. Wire the generator into the build so the class is written again whenever the catalog file changes.

### Step 3

**In the story.** Build: runs the magic number check over the recovery packages and the catalog completeness check.

Both checks run in the pipeline on every pull request. RwbMagicNumberCheck scans the recovery packages for numeric and text business literals; 0, 1, -1 and test code are allowed. When it finds one it fails the build and names the file, the line, and any catalog key whose default equals that literal, so a hard-coded 90 points at case.entry.dpd. CatalogCompletenessCheck compares the keys that services read through ParameterService with the lines in the catalog file and fails on a key that is missing, or on a catalog line with no owner or no default. Both live in build-tools/rwb-checks.

### Step 4

**In the story.** Flyway: loads the catalog rows and the default values into parameter_catalog and parameter_value at deployment.

This happens at deployment with nobody present. Flyway is the migration runner: it applies numbered SQL files to each environment in order and records which ones have run. V042_1__parameter_catalog.sql creates parameter_catalog, keyed on param_key, and parameter_value, which holds one row per key, environment, product group and version number. V042_2__parameter_seed.sql is generated from the catalog file and inserts the seed rows, meaning the first rows a table needs in order to work: the catalog lines themselves and their default values. The schema name in both files comes from the Flyway placeholder, so the same files run in every environment.

### Step 5

**In the story.** RW-COE: loads a new value version through POST /admin/reference-loads with table "PARAMETER", for example `case.entry.dpd` = 91 in PROD valid from 2026-12-10.

A person loads the new value. RW-COE calls POST /api/recovery/v1/admin/reference-loads with table set to PARAMETER and a file whose rows hold key, environment and value, plus the valid-from date. The example sets case.entry.dpd to 91 for PROD from 2026-12-10. The caller needs the Reference data C right. The idempotency key is the table, the valid-from date and the content hash of the file together, so sending the same file again returns the load that already exists instead of making a second one. This story builds the PARAMETER handler behind that existing endpoint.

### Step 6

**In the story.** ParameterLoadChecks: checks key in catalog, type, range, environment and required values; refuses the load whole on any failure.

Your checks run automatically when the file arrives. ParameterLoadChecks reads the catalog line for each key in the file and verifies that the key is listed, that the value parses as the declared type, that it falls inside min_value and max_value, that the environment is one the line allows, and that a required parameter ends up with a value. One bad row refuses the whole load; nothing partial is written. A value of 400 for case.entry.dpd answers 422 with MSG-GEN-002 naming 1 and 365, and a value of ninety answers MSG-P1-002 with the check that the value is not INTEGER. The version already in force keeps serving.

### Step 7

**In the story.** Owner: approves through POST /admin/reference-loads/{loadId}/approve; refused if the approver is the author.

A second person approves, and the author cannot. The owner named on the catalog line calls POST /api/recovery/v1/admin/reference-loads/{loadId}/approve with the Reference data A right; where the change moves a threshold or a limit, RW-RISK approves instead. Compare the approver with the author of the load and answer 409 with MSG-P7-002 when they are the same user, leaving the version at VALIDATED. Approval moves the version to APPROVED. Approval changes no value yet: the version waits for its valid-from date, which is why a version approved on 2026-12-05 still answers with the old value on 2026-12-09.

### Step 8

**In the story.** ParameterService: from the valid from date returns the new value; every instance refreshes its cache on ParameterVersionApproved and at the latest after the cache time to live.

This is all code. ParameterService resolves a read by key, environment and the business date passed in, so an approved version starts answering on its valid-from date with no deployment and no restart. Each instance keeps a cache of values; publish ParameterVersionApproved to the outbox when a version is approved, carrying the keys, the version number and the valid-from date, and have every instance reload those keys when it receives the event. The cache also expires on its own after config.cache.ttl-seconds, which is 60, so an instance that missed the event still picks the value up. The result carries the version number.

### Step 9

**In the story.** Engines: read values at run time with the version number, and record the version in their decision log inputs.

The engines do this as part of their own work. A read answers with a ParameterValue holding the key, the typed value, the version number, the valid-from date and the environment, and the caller writes that version number into the inputs it records on its decision log entry. The entry decision in the acceptance criteria records parameter version 1 alongside the value 90. This is what lets a decision be explained later: the inputs name the version in force when the decision was taken, and a decision already taken keeps that version after a newer one starts. Pass the business date on every call.

### Step 10

**In the story.** Any role with Rules and parameters R: reads the catalog and the values in force through GET /admin/parameters.

Any role holding the Rules and parameters R right calls this, and you build the endpoint. GET /admin/parameters takes optional key prefix, kind, owner and environment filters and answers with one entry per parameter: key, kind, type, unit, min, max, default, scope, required flag, owner, environments, usedBy, secret flag, the value in force, its version number and its valid-from date. ParameterCatalogController leaves the value out when the line is marked secret, so ace.db.password shows its owner, environments and usedBy with no value anywhere in the response. A role without the right gets 403 with MSG-P4-002.

## RWB-E1-043 Reference data service with versioned tables

Module: P3 Case and workflow

### Step 1

**In the story.** Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.

A person starts this. The reference data administrator uploads one file for one table through POST /api/recovery/v1/admin/reference-loads, sending multipart form data with the file as CSV or XLSX with one sheet, the table code, and the valid from date on which the new values take effect. The endpoint belongs to P4 and is already deployed, so your work begins at step 2. The caller must hold Reference data right C; a role with read only is refused with 403 and MSG-P4-002, which is test TC-E1-043-11. One load covers one table, and that table code has to be a value of the list LOV-REF-TABLE.

### Step 2

**In the story.** P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.

The P4 handler writes nothing itself. It calls the method recordVersion on the published interface of this story, in package recovery.casewf.refdata.api, passing the file rows as a list of maps, the table code, the valid from date, the user ID of the caller as the author, and the load ID. Your work in build step 7 is to wire the handler to that interface and to map the exceptions it throws onto the error responses of section 12, for example 422 with MSG-P3-027 for a failed check. P4 reaches this module only through the interface and never reads reference_version or reference_row, which the boundary test RWB-TE-001 checks.

### Step 3

**In the story.** Reference data service: checks the table code, the row schema for that table, the row keys, the valid from date and the author; computes the content hash and the next version number.

The service runs every check before it writes anything. The table code must be in LOV-REF-TABLE, read through the P4 list interface. The rows are checked against ReferenceTableSchemas, which holds the column names, types and key columns per table and comes from the parameter catalog of RWB-E1-042, so the text five in the numeric column limit_days fails with MSG-P3-027 naming row 12 and that column (AC4). Row keys must be unique. The valid from date must not be before the business date (AC6). A file with no data rows fails with MSG-GEN-001. The service also computes the content hash, a SHA-256 over the rows sorted by key, and the next version number, one above the highest version of that table.

### Step 4

**In the story.** Reference data service: writes one `reference_version` row with status VALIDATED and one `reference_row` row per file row, in one transaction.

Writing happens on its own once the checks pass. The service writes one reference_version row with status VALIDATED and one reference_row row per file row, holding row_key and row_data as jsonb, in one transaction, which means the version and all its rows appear together or not at all. A load with any failed check writes no version and no rows (BR5). When the same file arrives again for the same table and valid from date, the unique key on table_code, valid_from and content_hash matches, the service returns the existing load and writes nothing, so there is still one version 5 and no version 6 (AC7).

### Step 5

**In the story.** Approver: approves the load through `POST /admin/reference-loads/{loadId}/approve`.

A second person has to act before the values are served. The approver calls POST /api/recovery/v1/admin/reference-loads/{loadId}/approve with no body. This is the separation of duty that control CTL-08 requires: one person prepares the load and a different person releases it. The approver holds Reference data right A, which section 10 assumes is RW-RISK, the risk and model risk officer, because no role holds that right in the permission matrix today. The same person may not hold RW-REFADM and RW-RISK. Until the approval arrives the version stays VALIDATED and the engines keep reading the earlier version, as AC5 shows with HOLIDAY version 1.

### Step 6

**In the story.** Reference data service: checks that the approver is present, is not the author and holds the approve right; sets status APPROVED, `approver_user_id` and `approved_at`.

The service checks the approver and then records the approval. The approver must be present, must not be the author of the load, and must hold the approve right, which is checked through the ACE access check. It then sets status to APPROVED and fills approver_user_id and approved_at. The database backs this with a CHECK constraint that refuses an approver equal to the author. Build step 4 adds an optimistic lock on the version column, which means the update carries the row version it read and fails when another thread changed the row first, so two approvals arriving together give one success and one refusal with MSG-GEN-004 (AC8). An author approving their own load receives 409 with MSG-P7-002.

### Step 7

**In the story.** Reference data service: sets `valid_to` of the version it replaces to the day before the new valid from date.

The same approve call closes the version it replaces. The service sets valid_to on the previous approved version of that table to the day before the new valid from date, so approving a version valid from 2026-12-01 sets the earlier valid_to to 2026-11-30 (AC1). The old version and its rows stay readable, which is what lets an open case show the values it was decided under. valid_to is one of the few columns an update may change on reference_version; the update trigger refuses changes to anything else and refuses every change to reference_row. A trigger is database code that runs on each write and can reject it.

### Step 8

**In the story.** Case service, allocation engine and timer engine: on start and on each cache expiry, call `ReferenceDataService.rows(tableCode, businessDate)` and receive the approved version whose valid from is the latest on or before the business date.

The engines read the values with no person involved. The case service, the allocation engine and the timer engine call ReferenceDataService.rows with a table code and a business date, at start up and again each time their cache entry expires. The service answers with the approved version whose valid from is the latest on or before that date (BR3), so EXPOSURE_BAND returns version 3 for business date 2026-11-30 and version 4 for 2026-12-01. ReferenceRowCache keys entries by table code and business date and takes its lifetime from refdata.cache.ttl-seconds, 300 seconds. The cache never holds a version that is not APPROVED. When no approved version applies, rows throws NoVersionInForceException and the engine does not run (AC9).

### Step 9

**In the story.** Each engine: writes one log line per table read, with the table code, the version number and the business date.

Each engine writes one line per table it read, carrying the table code, the version number and the business date. You build ReferenceVersionLogger for this and call it from the start up hook of the case service, the allocation engine and the timer engine, which is build step 6. The line holds no row content and no party identifier, which AC3 tests on captured log lines. This is what lets anyone say later which version of QUEUE, SERVICE_LEVEL or HOLIDAY a run used, and it is the measure named in section 2.

## RWB-E1-044 Database migrations versioned with parameterized schema names

Module: P3 Case and workflow

### Step 1

**In the story.** Developer: adds one migration file for the story under `recovery/src/main/resources/db/migration/recovery/`, named `V<number>__<description>.sql`, with the header line `-- Story: <story key>`.

A developer does this by hand, once per story that changes the database. Put the file in recovery/src/main/resources/db/migration/recovery, name it V<number>__<description>.sql, and make the first line a comment reading "-- Story: <story key>". A migration is a SQL file Flyway applies once and then remembers, so the database of any environment is the sum of the migrations applied to it. One story gets one file, and no two files may carry the same story key. Write no schema name in the SQL: use the ${schema} placeholder, which Flyway replaces with the value of RWB_SCHEMA for the environment it is running in.

### Step 2

**In the story.** Pipeline: runs the migration lint: no literal schema name, exactly one story key per file, no story key in two files, no undo file.

The build does this, not a reviewer. Build MigrationLint as a build step with four refusals: a literal schema name written before a table name, a file with no story key in its header, the same story key in two files, and any file whose name begins with U, which would be an undo migration. For the literal name check, compare against every object name in sys_objects. Each failure stops the build with MSG-P3-016 and names the file, and the line as well for a literal schema name. Test each refusal with its own fixture file. The lint is the reason a wrong file never reaches an environment.

### Step 3

**In the story.** Pipeline: starts a clean PostgreSQL container and applies all migrations with `RWB_SCHEMA` set.

This runs in the pipeline with no person watching. Start an empty PostgreSQL container, set RWB_SCHEMA, and let Flyway apply every migration from the first to the newest. The result is the schema the repository describes and nothing else, which is why it can be compared against a real environment in the next step. It also proves the placeholder works: the same files build a schema named rwb_case here and in SIT, from files that are byte for byte identical in both runs. Use a clean container every time, because a container that keeps state from an earlier run would hide a migration that only works against an older database.

### Step 4

**In the story.** Pipeline: runs the drift check: dumps the schema object list of the clean database and of the target environment, and compares them.

Build SchemaDriftCheck and put it in the pipeline before each deployment to SIT, UAT and PROD. It lists the tables, columns, types, constraints and indexes of RWB_SCHEMA in the clean container, then the same list from the target environment, read through the read-only database account from the key store, and reports every difference. Drift is any object in an environment that the migrations did not produce, such as a column someone added by hand. A difference fails the pipeline with MSG-P3-016 naming the object, and no deployment starts. The feature flag rwb.p3.migration-drift-gate controls this: on in SIT, UAT and PROD, off in DEV, where drift is reported and the deployment continues.

### Step 5

**In the story.** Deployment: on service start, Flyway applies each pending migration once, in version order, and writes its checksum to the history table.

Flyway does this inside the service as it starts, with no pipeline step and no person. Configure it with RecoveryFlywayConfig and the properties in section 12, including spring.flyway.table set to flyway_schema_history_recovery, so the recovery module keeps its own history and its version numbers cannot collide with the ACE and collection modules. Pending means present in the repository and not yet in this database. Flyway applies those migrations lowest version first and writes one history row per migration with its version and its checksum, a number computed from the file content. Out of order is off, so a version below the newest applied one is refused.

### Step 6

**In the story.** Deployment: Flyway validates the checksums of applied migrations; a changed file stops the start.

Also automatic, and it happens before anything is applied, because validate-on-migrate is true. Flyway recomputes the checksum of each file that has a history row and compares it with the stored one. A file edited after it ran gives a different number, so validation fails with MSG-P3-016 naming the version and the service does not start, as AC4 describes with checksum 104553219 changed to 88120477. An applied migration is never edited. A mistake in one is corrected by adding a new migration that puts it right. PROD runs forward only: clean is disabled in every profile and an undo file is refused by the lint.

### Step 7

**In the story.** Platform administrator: reads the migration run on SCR-44 Interface and job monitor.

A person reads the result here. Build MigrationRunRecorder to write one job record per migration run through the P1 job monitor interface, which is what gives SCR-44 something to show. The administrator then sees each run with its version, its checksum and its drift result, in state running, failed or complete, and the same data comes back from GET /api/recovery/v1/admin/jobs with type MIGRATION. Reading it needs Platform administration right R, and a role without that right is refused with MSG-P4-002. MSG-P3-016 belongs in the pipeline log and on this screen only, and is never shown to a business user.

## RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME

Module: P3 Case and workflow

### Step 1

**In the story.** Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status.

A person does this, the center of excellence analyst holding Reference data C. Nothing is built here and no screen exists in this story. The analyst prepares two files: a PRODUCT_PARAMETER load with one row for each product group and parameter code, and a SERVICE_LEVEL load with one row for each product group and case status. BR2 names the parameters each product must carry, those the catalog of RWB-E1-042 marks with scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. The values themselves belong to the product heads, with entry at 90 days from DL16, service levels from DL22 and caps from DL23.

### Step 2

**In the story.** Reference data administrator: loads each file through `POST /admin/reference-loads`.

A person again, the reference data administrator, who also holds Reference data C. The call is POST /api/recovery/v1/admin/reference-loads, a P4 endpoint that already exists; this story adds checks behind it. The request is multipart form data carrying the file, the table code PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL, and the valid from date, and the response is a ReferenceLoad with its id, table, validFrom, status and row count. A load by a role without Reference data C is refused with 403 and MSG-P4-002, which is the access test TC-E1-045-09. Two loads of the same table code, valid from date and content are treated as one, as in RWB-E1-043.

### Step 3

**In the story.** Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.

This runs on its own once the file is loaded. The checks of RWB-E1-043 run first, then the new one you build as ProductCompletenessCheck, added as a table check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL. It confirms that every product in the PRODUCT version in force on the valid from date has a row for each catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for each status in the parameter servicelevel.required-statuses. A missing row refuses the whole load, with MSG-P3-034 naming the product and the item, and the version already in force stays in force. AC3 names SSME and WAITING_PARTNER.

### Step 4

**In the story.** Reference data service: checks each value against the catalog type and range.

The same check does this, with no person involved. Read the type, unit and allowed range the parameter catalog of RWB-E1-042 holds for each parameter code and compare every value in the file against them. A value of the wrong type or outside the range refuses the load in full, with MSG-GEN-002 naming the field and the two ends of the range, which AC4 shows as NOTICE_PERIOD_DAYS, 1 and 365 for a loaded value of 0. Two rows for the same product and parameter also refuse the load, with MSG-P3-027, as does a PRODUCT load that drops a product with open cases. Build OpenCaseCounter for that last count.

### Step 5

**In the story.** Approver: approves the version; it takes effect on its valid from date.

A second person has to act before any value is used. The approver holds the approve right in Reference data, and for a version where a limit or threshold moves it is the risk and model risk officer, per section 10. A validated version sits unused until that approval, and it then takes effect on its own valid from date rather than on the approval date. AC2 turns on this timing: PRODUCT version 2, PRODUCT_PARAMETER version 3 and SERVICE_LEVEL version 3 all carry valid from 2026-12-05, all three are approved, and the new product group AUTO_LEASE works on that date with no deployment between 2026-12-01 and 2026-12-05.

### Step 6

**In the story.** Timer engine: when it starts a notice timer for a case, calls `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", businessDate)` and sets `expires_at` from the value and its unit.

The timer engine of RWB-E1-028 does this when it starts a notice timer, and you change it to take the period from the published interface instead of its own table. The call is ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", businessDate), and the returned ProductParameter carries the value, the unit and the version number. Pass the value and the unit to DueDateCalculator, which you build: a value in CALENDAR_DAYS is added straight, and a value in WORKING_DAYS skips the dates in the HOLIDAY rows in force, per BR7. Write the result to timer.expires_at. When no row is in force the call throws MissingProductParameterException, handled in build step 6.

### Step 7

**In the story.** Case creation and allocation: read the entry threshold, the exclusion list and the exposure bands for the case's product group the same way.

You change two services that already exist, CaseEntryService from RWB-E1-018 and AllocationService from RWB-E1-020, so they call ProductParameterService.get for ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET with the case's product group and the business date. Remove any product group code, period or band written in their code; the done condition is that a search of the recovery module finds no product group code literal outside test fixtures and the generated API types. Where the call throws MissingProductParameterException, place the case in the exception queue and name the gap with MSG-P3-034, which is exception path X5 and AC7.

### Step 8

**In the story.** Each engine: records the PRODUCT_PARAMETER version used in its decision log entry inputs (written by the owning story).

The owning story of each engine writes its own decision log entry, so you add no entry here. What this story requires is that the version number the lookup returned travels into the inputs of that entry, which is why ProductParameter and ServiceLevel both carry versionNo. AC1 checks it on the timer side: each timer start records PRODUCT_PARAMETER version 2. Keep the number the lookup gave at the moment of the call and do not read the version again later, because a running timer keeps the value it started with while new timers take the new value from its valid from date, per BR6 and AC8.

## RWB-E1-046 Template and merge field catalog as data

Module: P6 Communications

### Step 1

**In the story.** Reference data administrator: loads the merge field catalog file through POST /admin/reference-loads with table "merge_field" and a valid from date.

A person does this: the reference data administrator, who holds Reference data right C. They post the merge field catalog file to /api/recovery/v1/admin/reference-loads as multipart form data with the file, the table name merge_field and a valid from date. P4 owns that endpoint and you do not build it. What you build is a table handler: MergeFieldLoadHandler, implementing the P4 interface ReferenceLoadHandler, whose table method returns merge_field and whose validate and apply methods do the checks and the writes. The file holds one row per merge field, each naming the BR Field ID of the case data it draws from in the Logical Data Model.

### Step 2

**In the story.** System: checks every row: merge code unique, BR Field ID present in sys_fields, source entity and field present, required flag set. A row that fails refuses the whole load (refdata change process, step 3).

The handler does the checking with no person involved. For every row: merge_code is unique within the catalog version, field_id names a BR Field ID that exists in sys_fields, source_entity and source_field are filled, and is_required is set. Read sys_fields through the P4 reference data interface, not by querying the tables of another module. A single failed row refuses the whole load, so no row of the file is written and the catalog version already in force stays in force; the answer is 422 with MSG-P1-002 naming the failed check. Write the accepted rows to table merge_field, which migration V1_046__template_catalog.sql creates with a unique key on merge_code and catalog_version.

### Step 3

**In the story.** Reference data administrator: loads a template version file through POST /admin/reference-loads with table "template", carrying template code, language, product group, channel, notice type, signature basis, the body file reference, the merge codes used and, where Legal has signed, the approver and approval date.

The same person does this second load, again through the P4 endpoint, this time with the table name template. The file carries one row per template version: template code, language from LOV-LANG, product group from LOV-PRODUCT, channel, notice type from LOV-NOTICE, signature basis, the body_ref that points at the DOCX body, the list of merge codes the template uses and, where Legal counsel has signed, approved_by and approved_at. Build TemplateLoadHandler as the second ReferenceLoadHandler. Those approval columns are how a version is approved in Epic 1, before the template screen of RWB-E1-034 is live. A row with no template code, language or body reference refuses the load with MSG-GEN-001 naming the field.

### Step 4

**In the story.** System: reads every merge code in the body and in the merge code list and checks each one against the catalog in force. An unknown code refuses the load and names the code (MSG-P6-006).

The handler does this with no person involved. Build MergeCodeScanner to read the merge codes out of the DOCX body, where they are written in the form {{CODE}}, and compare that set with the merge code list declared on the row. Check every code from both places against the merge field catalog version in force. One unknown code refuses the whole load with MSG-P6-006 naming the template and the code, and no version of that template is created. This check is what keeps the letter engine safe: it can only fill a field the catalog knows, so a template cannot ask for data the Workbench has no source for.

### Step 5

**In the story.** System: assigns the next version number for the template code and language, keeps every earlier version readable and sets state Approved only where the approver and approval date are present, otherwise Draft.

The handler assigns the version, with no person involved. Count the existing versions for the template code and language and use the next number. Earlier versions are never updated or deleted, because an open case has to keep the version its notice was generated under. Migration V1_046__template_catalog.sql replaces the unique key on template_code alone with uk_template_version on template_code, language and template_version, so one code can hold many versions. Set the state column from the approval columns: APPROVED when both approved_by and approved_at are present, DRAFT when they are not. A check constraint allows only DRAFT, APPROVED and WITHDRAWN, and requires both approval columns when the state is APPROVED.

### Step 6

**In the story.** System: the published interface TemplateCatalog returns, for a template code, language and date, the current version: the Approved version with the highest version number whose valid from date is on or before that date.

This is the read side, used by other code and not by a person. Build TemplateCatalogService to implement the published interface TemplateCatalog in package recovery.comms.templates. Its current method takes a template code, a language and a date, and returns the Approved version with the highest version number whose valid_from is on or before that date. A version with a valid_from in the future is therefore ignored until that day arrives: version 3 valid from 2026-12-01 leaves version 2 current on 2026-11-30 and becomes current on 2026-12-01. The TemplateVersion returned carries the version numbers, the body reference, the approver, the approval date and the merge codes, and no personal data.

### Step 7

**In the story.** Letter engine (RWB-E1-052): asks TemplateCatalog for the current version. If none is Approved, the catalog refuses and names the missing approval (MSG-P6-005).

The caller is the letter engine built in RWB-E1-052, so this happens in code with no person involved. When every version of the template is still Draft, the catalog throws TemplateNotApprovedException and the refusal carries MSG-P6-005 naming the template and the version, and nothing is generated. When the version that was current has been withdrawn, it throws TemplateWithdrawnException with MSG-P6-003, and generation waits until Legal counsel approves a new version. Build both exceptions as part of the interface, because the engine has to tell the two cases apart: one is a template waiting for its first approval, the other is a template taken out of use.

### Step 8

**In the story.** System: writes the load result (rows loaded, rows refused, version numbers) to the reference load record and the ACE audit log.

The handler does this at the end of each load, with no person involved. Write the result of the load to the reference load record that P4 keeps: rows loaded, rows refused and the version numbers assigned, with the load status moving to refused or in force. Send the same result to the ACE audit log. The administrator reads it there, because Epic 1 has no screen for it; SCR-40 Reference data shows the template and merge_field versions once it is built. A repeat of a file already loaded for the same table is caught on the SHA-256 hash of the file and answered with 409 and MSG-P1-002, with no new version created.

## RWB-E1-047 Feature flags for module release with a removal date

Module: P2 Integration

### Step 1

**In the story.** Platform administrator: creates a flag with key, description, owner, default value and removal date.

A person does this through an endpoint you build, POST /admin/feature-flags, which needs Platform administration C. The request body FeatureFlagRequest holds key, description, ownerUserId, ownerTeam, defaultOn and removalDate. There is no screen in this story, so the platform administrator calls the endpoint through the ACE admin console API client; the flag list screen arrives later as SCR-44. A feature flag is a data row that switches one piece of behavior on or off per environment with no new deployment, so unfinished work can ship switched off. The removal date is the date by which the flag and the old code path should both be gone.

### Step 2

**In the story.** System: validates the key pattern `rwb.<module>.<short-name>`, the removal date and the owner, and writes the flag row with every environment set to the default.

This happens on its own in FeatureFlagService. Test the key against the pattern rwb.<module>.<short-name>. The same rule is a check constraint in migration V2026_11_47__p2_feature_flags.sql written as ^rwb\.[a-z0-9]+\.[a-z0-9-]+$, so a bad key is refused in the service and in the database. A missing removal date is 422 with MSG-GEN-001, and a removal date before today is 422 with MSG-GEN-003. A key that already exists is 409. Then insert the feature_flag row with dev_on, sit_on, uat_on and prod_on all set to default_on, so a new flag behaves the same in every environment until somebody changes one. The response is 201.

### Step 3

**In the story.** Service code: calls FeatureFlags.isOn(key) at each request; the value comes from a cache refreshed every 30 seconds (assumed; DL11).

This runs on its own inside every module that has work behind a flag. Build the published interface FeatureFlags with the single method isOn(String flagKey) in package recovery.integration.flags.api, and FeatureFlagsImpl behind it. Hold the value per key in a cache refreshed every rwb.flags.cache-seconds, which is 30, so a change takes effect within half a minute with no restart. Read the current environment from property rwb.environment and pick the matching column. Return false for a key with no row and write a warning with the key and no user data to the application log. Other modules call this interface and never read the flag tables themselves.

### Step 4

**In the story.** Front end: reads GET /feature-flags at page load and hides or shows the component.

This runs on its own in the browser when the page loads. Build GET /feature-flags returning a map of flag key to boolean for the caller's environment. It needs a resolved session and no capability area, and answers 401 with MSG-P4-001 without one. In front end folder src/modules/recovery/flags build the hook useFeatureFlag, which reads that endpoint once per page load and returns the value for a key, and the component FlagGate, which renders its children only while the flag is on. The queue column on SCR-02 Case list behind rwb.casewf.case-list-queue-column is the reference use. A value read at page load changes only on the next reload.

### Step 5

**In the story.** Platform administrator: switches the flag on for one environment with a reason.

A person does this. The platform administrator sends PATCH /admin/feature-flags/{flagKey} with FeatureFlagChange holding environment, value and reason, plus an If-Match header carrying the version they read. If-Match is how the server learns which copy of the row the caller saw. The endpoint needs Platform administration U. An empty reason is 422 with MSG-GEN-001 and an unknown key is 404 with MSG-P2-016. Setting the value the environment already holds writes no change row. RW-SECADM may also change flags, while RW-COE, RW-DATASTEW, RW-AUDIT and RW-COMPLY may only read flags and their change history.

### Step 6

**In the story.** System: checks the version, writes the new value and a feature_flag_change row with user, time, old and new value, and writes the ACE audit log entry.

This happens on its own in FeatureFlagService, all in one transaction. Compare the If-Match version with the version on the feature_flag row and refuse with 409 and MSG-GEN-004 when they differ, so of two administrators who both read version 4 one write succeeds at version 5 and the other is refused. Then write the new value into the environment column, insert a feature_flag_change row with flag_key, environment, old_value, new_value, reason, created_by and created_at, and call the ACE audit log with the same change. The change row and the audit entry hold the user ID, never the person's name.

### Step 7

**In the story.** Front end: after reload, shows the component; no deployment takes place.

This happens on its own, and the step needs no code beyond steps 3 and 4. The browser reloads the page, useFeatureFlag reads GET /feature-flags again, and FlagGate renders the component the flag now allows, for example the queue column on SCR-02. On the server side the cache picks the new value up within 30 seconds. No code is released and no service is restarted, which is the reason for holding the value as a row. Every flag that is off has to run the previous code path, so write a test for both paths of each flag you add.

### Step 8

**In the story.** Scheduler: the weekly flag report job runs every Monday 08:00 and lists every flag past its removal date with its owner.

This runs on its own on a timetable, with nobody starting it. Build FlagRemovalReportJob as a Quartz job that fires every Monday at 08:00 Asia/Bangkok. It reads the feature_flag rows where is_active is true and removal_date is before today, and works out how many days each one is overdue. Its idempotency key is the report date, so a rerun on the same date sends nothing new; a restart runs the job from the beginning. The same rows are available on demand through GET /admin/feature-flags with overdue=true, which returns daysOverdue per flag to a caller with Platform administration R.

### Step 9

**In the story.** System: sends the report to each owner and to the RW-PLATADM group by email and logs MSG-P2-003 per flag.

This happens on its own at the end of the job. Send one email per owner, holding that owner's flags, and one email to the RW-PLATADM group, both through the ACE notification path for staff. Write one log line per flag with MSG-P2-003, which names the flag, the date it passed and its owner, and asks for the flag and its old code path to be removed. The owners are the tribe lead and squad members, who receive the report and hold no right to change a flag. The report repeats every week until the flag is retired.

## RWB-E1-048 Rule change audit report

Module: P3 Case and workflow

### Step 1

**In the story.** Center of excellence analyst: raises the change request in the bank's request tool and receives its reference, for example CR-2026-0042.

A person does this outside the Workbench. The center of excellence analyst opens a change request in the bank's own request tool and receives a reference such as CR-2026-0042. No code of yours creates that reference and no endpoint of yours calls that tool. What you build is the place to hold it: the column change_request_ref on reference_version, up to 30 characters, added by the migration in the solution plan. The reference ties a configuration change to the request that asked for it, and the approval check later refuses a version that carries no reference.

### Step 2

**In the story.** Reference data administrator: loads the new version through `POST /admin/reference-loads` (or `POST /admin/rule-versions`) with the request reference, the impact summary and the rollback plan as form fields.

A second person, the reference data administrator, uploads the version. Your work is to accept three more form fields on both existing load endpoints: changeRequestRef up to 30 characters, impactSummary up to 1000 and rollbackPlan up to 1000. A load with any of them missing still succeeds, because the fields are checked at approval and not at load. Pass the three values through to recordVersion on the published interface so they reach the version row. The two P4 load handlers are build step 2. Rule versions arrive by the same path, with a table code that starts RULE_ and names the route set.

### Step 3

**In the story.** Reference data service: stores the checklist fields on the version and records the test result from the load checks or the harness (PASSED or FAILED).

The service writes these values with no further action by a person. Store the three uploaded fields on the reference_version row, then set test_result to PASSED or FAILED. Where that result comes from depends on the table: for a reference table it is the outcome of the load checks built in RWB-E1-043, and for a rule table it is the outcome of the rule table test harness RWB-TE-005. The new columns all come from one migration: change_request_ref, impact_summary, test_result, rollback_plan, verified_by, verified_at and verify_note, with indexes for the period query of the report.

### Step 4

**In the story.** Approver: approves through `POST /admin/reference-loads/{loadId}/approve`.

A third person approves. The approver holds the approve right, which RW-RISK carries, and calls the approve endpoint that already exists from RWB-E1-043; this story adds checks to that endpoint rather than a new one. Until the approval happens, the version stays VALIDATED and is never served, even after its valid from date has passed, which is what AC2 shows with SERVICE_LEVEL version 5. The three people so far are different on purpose: one asks for the change, one loads it, one approves it, so no single person can put a new rule into force.

### Step 5

**In the story.** Reference data service: refuses the approval unless the request reference, impact summary, rollback plan and a PASSED test result are present and the approver is not the author.

The service enforces this inside the approve call, automatically. Build ChangeChecklistValidator and call it from approve. It refuses when the request reference, the impact summary or the rollback plan is empty, and when test_result is not PASSED, answering 409 with MSG-P3-022 naming the first item that is missing or failed. It also compares the caller with author_user_id on the version and refuses when they are the same person, with MSG-P7-002. A refused approval changes nothing: the version stays VALIDATED and the version already in force keeps being served.

### Step 6

**In the story.** Reference data administrator: after the valid from date, records the verification through `POST /admin/reference-loads/{loadId}/verify`.

A person makes this call, and you build the endpoint. POST /admin/reference-loads/{loadId}/verify takes a note of up to 1000 characters, which is required, and answers 200 with the load showing verifiedBy and verifiedAt. The caller needs Reference data U. Check the date against valid_from and answer 422 with MSG-GEN-003 when the verification comes too early, and 422 with MSG-GEN-001 when the note is empty. The call is idempotent, which means a second verification of the same version changes nothing and answers 200 with the first record, so a repeated click cannot overwrite who verified and when.

### Step 7

**In the story.** Internal audit or the center of excellence analyst: reads the report through `GET /admin/change-log` for a period and a table, as JSON or CSV.

A person reads the report, through a new endpoint you build. GET /admin/change-log takes from and to, both required, an optional table, format json or csv, and page and size with a default of 50 and a maximum of 200. It needs Rules and parameters R, so RW-AUDIT, RW-COE, RW-RISK and RW-PLATADM may read it and other roles receive 403. Answer 422 with MSG-GEN-003 when to is before from, and an empty list with total 0 for a period with no changes. ChangeEffectCalculator fills rowsAdded, rowsChanged and rowsRemoved by comparing a version's rows with the version it replaced by row_key and row_data, and lists the changed rule IDs for RULE_ tables. The report carries staff user IDs and no customer or case data.

## RWB-E1-049 OCR pipeline on the Workbench document hub

Module: P5 Document hub

### Step 1

**In the story.** JOB-12 Document intake: starts every 15 minutes in business hours and runs the OCR step after the intake and scan steps.

This runs on a schedule with nobody starting it. JOB-12 Document intake fires from its Quartz schedule every 15 minutes during business hours in Asia/Bangkok. You build DocumentIntakeJob as a Spring Batch job with ordered steps, and add ocrStep as the step that runs after the intake and scan steps. The order matters because BR3 lets a file be read only once its malware scan says CLEAN, and that scan step arrives in RWB-E1-041; until then test data is seeded with scan_result CLEAN. A stopped run leaves its unfinished items PENDING for the next run, and the platform administrator can also rerun the job from the job monitor through POST /api/recovery/v1/admin/jobs/{jobId}/rerun.

### Step 2

**In the story.** DocumentStoredListener: for each DocumentStored event with source UPLOAD, creates an intake item with the case ID, the document ID and scan_result CLEAN (the upload was scanned before storage).

The Workbench does this by itself, as soon as a document is stored. Build DocumentStoredListener to consume the DocumentStored event (EV-16) that RWB-E1-024 publishes, keep only the events whose source is UPLOAD, and insert one document_intake row for each: the case ID, the document ID and scan_result CLEAN, because an upload is scanned before it is stored. ocr_status starts at PENDING from the column default and ocr_attempts at 0. This row is the unit of work for the rest of the flow, and its ID is the idempotency key of the OCR step: an item whose status is no longer PENDING is never read again.

### Step 3

**In the story.** OcrStep: selects intake items with scan_result CLEAN and ocr_status PENDING, oldest first, locking each row so that no two workers take the same item; runs up to OCR_WORKERS items in parallel.

The step does this with no person involved. Select document_intake rows with scan_result CLEAN and ocr_status PENDING, oldest first by received_at, using SELECT ... FOR UPDATE SKIP LOCKED. That clause takes a lock on each row it returns and passes over rows another worker already holds, so two workers never take the same item and the second simply moves on. Index ix_intake_ocr_pending on (ocr_status, received_at) where scan_result = 'CLEAN' serves the query. Run up to OCR_WORKERS items at a time, four at release, through a worker pool. Test this with one pending item and four workers starting together: the OCR service has to receive exactly one call.

### Step 4

**In the story.** OcrClient: sends the file to the OCR service with the languages Thai and English and receives, per page, the lines, words, positions, language and word confidence.

Your adapter does this, under the service identity SY-OCR. Build OcrClient with a read method taking the blob reference, the list of languages and a timeout, and OcrServiceAdapter behind it calling the OCR service that Autonomous Ops runs, at the endpoint in the property rwb.dochub.ocr.endpoint. Send Thai and English together, because a Thai recovery document often carries English words as well. The answer gives, for each page, the lines, the words, their positions, the language and a confidence value per word. Map a call that does not answer within OCR_TIMEOUT_SECONDS, 120 at release, or that returns an error, to OcrUnavailableException, and a file that cannot be opened to UnreadableFileException. Build this against a stub returning fixed pages first.

### Step 5

**In the story.** OcrStep: computes the page quality as the mean word confidence of the page; stores the full output as JSON at ocr/{intakeId}.json in the standard container and sets ocr_ref.

The step does this on its own for each item. Take the mean of the word confidence values on a page as that page's quality. Write the whole OCR answer as JSON to the standard container at ocr/{intakeId}.json and put that location in document_intake.ocr_ref. Keeping the full output lets classification in RWB-E1-050 and extraction in RWB-E1-053 read the lines and positions without a second call to the OCR service, which they do through the published interface OcrOutputReader that you build in this story. The guardrails keep OCR text out of application logs, so log the intake ID and the counts only.

### Step 6

**In the story.** OcrStep: writes one document_text row per page with the page text and quality, with the document ID where the item is already attached.

The step writes these rows itself. Insert one document_text row for each page: intake_id, page_no, text_content and quality, and document_id as well when the intake item is already attached to a document, which it is for an uploaded file. Migration V1_5_049__document_intake.sql creates the table, with a foreign key from intake_id to document_intake(id) and from document_id to document(id); a foreign key means the value has to match an existing row in the other table. The unique key uk_document_text_page on (intake_id, page_no) stops a second set of rows for the same item, so a repeat run cannot double the text. Test that index first.

### Step 7

**In the story.** OcrStep: if every page has quality at or above OCR_MIN_QUALITY, sets ocr_status DONE; otherwise sets ocr_status RESCAN and rescan_pages to the page numbers below the threshold.

The step decides the status with no human step. Compare every page's quality with OCR_MIN_QUALITY, 0.70 at release. When every page is at or above it, set ocr_status DONE; the threshold counts as a pass, so a page at exactly 0.70 is accepted. When any page falls below it, set ocr_status RESCAN and put the page numbers of the failing pages in rescan_pages. A four page document with page 3 at 0.41 therefore gives status RESCAN and rescan_pages 3. The threshold is a parameter row in document_hub_parameter, loaded by the reference data administrator, so a change to it needs no release.

### Step 8

**In the story.** OcrStep: for an item in RESCAN with a known case, sends MSG-P5-018 to the case owner through the ACE notification path; for an item with no case, sets review_reason RESCAN so the item shows in the document review queue (SCR-31, RWB-E1-054).

The step does this for each item it set to RESCAN, and the branch depends on whether the item has a case. With a case ID, RescanNotifier sends MSG-P5-018 to the case owner through the ACE notification path, naming the page, the document and the case; the owner comes through CaseDirectory, never by reading the case tables. Build RescanNotifier and add the message template to the ACE notification path under the recovery templates. With no case, send nothing and set review_reason RESCAN, which puts the item on SCR-31 Document review queue once RWB-E1-054 is built. A mailroom scan with no case therefore gets no notification.

### Step 9

**In the story.** OcrStep: records the run counts (read, done, rescan, failed) on the job record shown in the job monitor.

The step does this at the end of its run. Count the items read, the items set DONE, the items set RESCAN and the items that failed, and write those four counts onto the JOB-12 job record. The platform administrator reads them on SCR-44 Interface and job monitor, which shows a run as running, failed or complete, and reruns the job from there when needed. The same record carries the step failure that AC6 expects: two runs in which the OCR service answered 503 show the OCR step failed in both, and the job raises an alert to the platform administrator after the second. The counts hold no document content.

## RWB-E1-050 Document classification

Module: P5 Document hub

### Step 1

**In the story.** JOB-12 Document intake: runs classifyStep after ocrStep.

A scheduled job calls your code, with no person involved. JOB-12 Document intake already exists and runs every 15 minutes in business hours; this story adds one step to it, classifyStep, placed after the OCR step that RWB-E1-049 built. Write ClassifyStep as that step and wire it into the job after ocrStep, so it only ever sees items whose text has already been read. That order is what makes the selection in the next step possible, because classification needs the OCR text. With the feature flag rwb.dochub.classify off, the step is skipped and every scanned item goes to review with reason LOW_CONFIDENCE, so the job has to run with the step absent.

### Step 2

**In the story.** ClassifyStep: selects intake items with ocr_status DONE, no predicted_type and no document type given (uploads carry their type and are skipped), locking each row.

Your step picks its own work, with no person choosing. Query document_intake for items whose ocr_status is DONE, whose predicted_type is empty and which carry no document type already, and lock each row as you take it, so two runs of the job cannot classify the same item twice. An upload arrives with its type named by the person who uploaded it, so it is skipped and no model call is made for it. Items in RESCAN or FAILED are not selected either, because their ocr_status is not DONE. Add the index ix_intake_classify on ocr_status for rows where predicted_type and review_reason are both empty, so the query stays cheap as the table grows.

### Step 3

**In the story.** ClassifyStep: takes the text of the first CLASSIFY_MAX_PAGES pages and replaces national ID numbers, account numbers and phone numbers with tokens through the ACE PII masking service.

Your step does this itself, before any text leaves the document hub. Read the page count from the parameter CLASSIFY_MAX_PAGES in document_hub_parameter, set to 3, and take the text of that many pages from document_text. Then build TextMasker, which calls the ACE PII masking service and replaces every national ID number, account number and phone number with a token, a short placeholder that keeps the text readable while carrying no personal value. Only the masked text goes to the model. Test this with a synthetic page holding a national ID number and an account number, and check that the stub received tokens in place of both. Never log the text.

### Step 4

**In the story.** ClassifierClient: sends the masked text and the six type codes with their labels from the type table in force; receives a score per type and the model version.

This is an automatic call to a model outside your code. Write ClassifierClient with one method, classify, taking the masked text, the type labels and a timeout, and implement it as ModelGatewayClassifier over the P10 model gateway on the route named in rwb.dochub.classify.model-route. Read the six type codes and their labels from the document type table in force, DOCTYPE-2026.11, so the model is told which types exist as data and not from a list inside the code. The answer holds one score per type and the model version. Set the timeout from CLASSIFY_TIMEOUT_SECONDS, 60 seconds, and throw ClassifierTimeoutException when the model does not answer in time.

### Step 5

**In the story.** ClassifyStep: ranks the scores; writes predicted_type, classification_confidence, the top two candidates in type_candidates and classifier_version.

Your step writes the result automatically. Sort the scores, highest first, and write to the intake item: predicted_type as the top type code, classification_confidence as its score in a numeric column with four decimals, type_candidates as the two highest scoring types with their scores, and classifier_version as the model version the gateway returned. Write the two candidates on every item, including the ones that pass the threshold, because the review queue of RWB-E1-054 offers them to a person as the two choices. Add these columns to document_intake in the migration V1_5_050__intake_classification.sql, along with classify_fallback, and add document_type and type_candidates to document.

### Step 6

**In the story.** ClassifyStep: if the top score is at or above CLASSIFY_THRESHOLD and the type is in the table in force, marks the item classified with no review_reason; attach (RWB-E1-032) stores it with review_status NOT_NEEDED.

Your code decides this with no person involved. Compare the top score with the parameter CLASSIFY_THRESHOLD, which holds 0.80, and treat the threshold as inclusive, so a score of exactly 0.80 passes. Check as well that the predicted type code appears in the document type table in force. When both hold, leave review_reason empty, which is the signal that attach reads. Attach is built in RWB-E1-032 and stores the document with review_status NOT_NEEDED, so no person sees it. Because the threshold is a parameter row, raising it to 0.90 changes the outcome with no code change and no deployment, and that behavior is itself a test case.

### Step 7

**In the story.** ClassifyStep: below the threshold, sets review_reason LOW_CONFIDENCE; attach (RWB-E1-032) stores the document with review_status PENDING and write_once false, so it shows on SCR-31 with MSG-P5-003 and its two candidates (RWB-E1-054). A type outside the table sets review_reason UNKNOWN_TYPE with no predicted type, and attach holds the item for a person.

Your code sets one field and the rest follows from it. A top score under the threshold sets review_reason to LOW_CONFIDENCE and keeps the predicted type and the two candidates on the item. A type code the model returns that is not in the table in force sets review_reason to UNKNOWN_TYPE with no predicted type, and still keeps the two highest agreed types as candidates. Attach, in RWB-E1-032, reads review_reason and stores the document with review_status PENDING and write_once false, so a person can correct the type later. The document then shows on SCR-31, built in RWB-E1-054, with MSG-P5-003 and its two candidates. A model timeout sets MODEL_UNAVAILABLE the same way.

### Step 8

**In the story.** ClassificationEvaluationRunner: on demand, runs the labeled sample, writes the accuracy and the 6 by 6 confusion matrix to evaluation/classification/{runDate}.json in the standard container and to the job record.

A person starts this one, the center of excellence analyst, and it is no part of the nightly job. Build ClassificationEvaluationRunner to classify the labeled sample of 180 synthetic documents, 30 of each type, where the true type of each document is known. It counts how many predictions match the label and writes the accuracy, the 6 by 6 confusion matrix showing which type was predicted for each true type, and the model version, into evaluation/classification/{runDate}.json in the standard container and onto the job record. The risk and model risk officer reads that report before the step runs in production, and at least 162 of the 180 have to be correct.

## RWB-E1-051 Legacy feed jobs on ADF and Control-M

Module: P2 Integration

### Step 1

**In the story.** Platform administrator: commits the Control-M job definitions for the ALS and EFS extracts into COLLINS and the ADF pipelines for the CCMS and SVAF file moves to the `ops/` folder.

A person does this: the platform administrator, who owns these definitions. Control-M is the bank batch scheduler and ADF is the bank pipeline service. The four definitions are held as JSON in the repository, in ops/control-m/ for the Control-M jobs RWB_ALS_EXTRACT and RWB_EFS_EXTRACT, which extract from ALS and EFS into COLLINS, and in ops/adf/ for the pipelines rwb-ccms-file-move and rwb-svaf-file-move, which move the weekly CCMS and SVAF files. Those four names are proposed until SCB IT issues the bank names. SCB IT gives the platform administrator access to the Control-M folder and the ADF factory for DEV and SIT. Keeping the definitions in the repository is what lets the pipeline check them.

### Step 2

**In the story.** Pipeline: validates the definitions and deploys them to the environment through the bank's deployment path.

The pipeline does this; nobody copies a definition into Control-M or ADF by hand. Your work is the pipeline step that reads the files in ops/control-m/ and ops/adf/ and refuses a definition that is not valid, which is build step 5. The deployment itself follows the bank deployment path into each environment. Keep the times, the folders and the retry window where they belong in configuration: the interface configuration rows hold the inbound path and the file pattern, and the properties rwb.jobs.collins.start, rwb.jobs.collins.last-retry and rwb.jobs.files.weekly-cron hold the times. The story is done when a full week of the four feeds runs in SIT with no manual start.

### Step 3

**In the story.** Control-M: runs the ALS and EFS extracts after COLLINS end of day; COLLINS completes its load before 05:00.

Control-M runs these two extracts on its own, outside the Workbench. The Workbench never calls ALS or EFS directly: both feeds reach it only through the COLLINS daily batch, as interfaces INT-01 and INT-07. Control-M starts the extracts after the COLLINS end of day, and COLLINS finishes its own load before 05:00, which is why the Workbench job in step 5 starts at that time. Nothing in your code starts or waits on Control-M; your code looks for the result of the load at 05:00 and treats a feed with no data as missing. A Control-M job that fails alerts the platform administrator through the bank scheduler, and the Workbench run for that interface is written as MISSING.

### Step 4

**In the story.** ADF: moves the weekly CCMS and SVAF files from the source drop folder to the Workbench SFTP inbound folder by Sunday 23:00 (assumed; DL12).

The two ADF pipelines do this with no person involved. CCMS and SVAF reach the Workbench only as weekly file loads, interfaces INT-10 and INT-11, so there is no direct call from the Workbench to either system. ADF takes the files from the source drop folder and puts them in the Workbench SFTP inbound folder by Sunday 23:00, a time that is still an assumption under DL12. Read the inbound path and the file pattern from the interface configuration rows rather than holding folder names in code. When the ADF pipeline fails, as AC4 describes for CCMS, no file is waiting on Monday, the run row for that interface is written as MISSING and the alert goes out.

### Step 5

**In the story.** Scheduler: JOB-01 starts at 05:00 and reads the COLLINS load; JOB-09 starts Monday 04:00 and reads the CCMS and SVAF files through FileLoadAdapter.

Quartz inside the Workbench starts both jobs; no person starts them. Build CollinsIntakeJob as the JOB-01 entry point, running daily at 05:00 and retrying each hour until the last retry, with both times read from the properties rwb.jobs.collins.start and rwb.jobs.collins.last-retry. After the 09:00 attempt with no load, write the run rows for INT-01 and INT-07 as MISSING, mark the products stale and show MSG-P1-001 with the date of the load in use. JOB-09 runs weekly on Monday at 04:00 for INT-10 and INT-11 and reads the files through the FileLoadAdapter built in RWB-E1-007; that job entry point also comes from that story. The idempotency key is the interface and the business date, with the file hash added for JOB-09.

### Step 6

**In the story.** SY-DATALOAD: each run writes an interface_run row with interface, business date, status, record count, start and end time.

The job writes this row itself, under the service identity SY-DATALOAD, with no person involved. The interface_run table already exists from RWB-E1-007, so this story needs no migration; you read interface_config and read and write interface_run. Build FeedRunRecorder to write the row at the start of a run and to complete it at the end, and call it from CollinsIntakeJob and from FileLoadJob. The row holds the interface, the business date, the status, the record count and the start and end time, with the status one of LOADED, MISSING, FAILED, REFUSED and DUPLICATE. Keep the row to counts and times, with no customer data. The platform administrator and the data steward read these rows through GET /admin/jobs.

### Step 7

**In the story.** SY-DATALOAD: on failure, the run row is FAILED or REFUSED, a structured event `rwb.integration.job.failed` is written to Log Analytics and the alert rule emails the data steward and the platform administrator with MSG-P2-004.

The job does this with no person involved. On a failure, write the run row as FAILED or REFUSED and write the event rwb.integration.job.failed to Log Analytics. A structured event is a log record with named fields rather than a line of free text, so an alert rule can match on it. The alert rule itself, JobFailureAlert, is held as code in ops/monitoring/ and emails the data steward and the platform administrator with MSG-P2-004, which names the job, the time, the business date and the run book to follow. The target is 15 minutes from the failure, which is an assumption under DL11. Alerts arrive by email, since this story has no screen. Test the rule with a forced failure in SIT.

### Step 8

**In the story.** Pipeline: on every merge, the contract tests parse each sample file against its layout file and fail on any field that differs.

The merge pipeline runs these tests, with no person involved. Write the four layout files in contracts/ from the interface specifications and the source to target mapping, each naming the field, type, length and whether it is mandatory, and put the synthetic sample files in src/test/resources/contracts/. Build LayoutContractImpl behind the LayoutContract interface to read a layout file and check a sample file against it, returning every field that differs. FeedContractTest is one parameterized test per interface, so one test body covers INT-01, INT-07, INT-10 and INT-11. A field whose name, type or length differs fails the test with MSG-P2-002 naming the field, and the merge is blocked, as AC3 shows for the SVAF field Appraised Value declared as a number of 18 digits with 2 decimals and supplied as text.

## RWB-E1-052 Notice generation v1

Module: P6 Communications

### Step 1

**In the story.** Caller: calls NoticeApi.generate with case ID, notice type, party ID and language.

The caller is the case workflow module under SY-CASEWF, or a person later through the endpoint of RWB-E2-021. Epic 1 has no endpoint at all, so build the published interface NoticeApi in package recovery.comms.notices with generate taking a NoticeGenerationRequest of caseId, noticeType, partyId, language, requestedBy and businessDate, and returning NoticeResult with noticeId, state, documentId, holdReason, templateVersion and messageCodes. The method throws TemplateNotApprovedException, PartyNotOnCaseException and DecisionNotRecordedException. NoticeGenerationService sits behind the interface and carries out steps 2 to 9 without any further input from the caller.

### Step 2

**In the story.** System: reads the case summary (case number, product group, status) through the P3 interface and the party role through the case parties.

The service does this on its own. Call CaseWorkflowApi.getCaseSummary for the case number, product group and status, and CaseWorkflowApi.getCaseParties for the parties on the case. Both are P3 published interfaces, and this module reads neither recovery_case nor case_party directly. The product group decides which template applies in step 3, and the party list is what makes the check of exception path X7 possible: a party that is not on the case is refused with MSG-P4-003, which AC8 tests with party P-0999 on case RC-2026-000123.

### Step 3

**In the story.** System: asks TemplateCatalog for the current LETTER template for the notice type, product group and language on the business date.

The service reads the catalog built in RWB-E1-046; no person picks a template. TemplateCatalog returns the version that is Approved and current for that notice type, product group and language on the business date. Two outcomes end generation here. With no Approved version the call is refused with MSG-P6-005 naming the template and version, and no notice row and no document are created, which AC2 tests with RECALL-HP version 1 in Draft. With the current version Withdrawn and no later approved version, write the notice in state Held with hold reason TEMPLATE_WITHDRAWN and raise a task to the litigation officer team with MSG-P6-003.

### Step 4

**In the story.** System: resolves each merge code of the template through the interface of the module that owns its source field, and detokenizes personal values through the ACE PII service, which writes the access to PII Kafka.

The service resolves the values; nobody keys them. Build MergeValueResolver. For each merge code on the template, read merge_field.source_entity and merge_field.source_field, then call the published interface of the module that owns that source, such as PartyApi.contactPoints for a contact point or RecoveryDataApi.caseBalance for the balance. Personal values are held as tokens, which are placeholders carrying no name or address. The ACE PII service exchanges a token for the real value and writes one access event per field to PII Kafka. Clear values go into the PDF alone: the merge snapshot keeps tokens, and logs, tests and prompts hold no personal data.

### Step 5

**In the story.** System: if a required merge value is empty, holds the notice, names the field and raises a task to the case owner; stops.

The service decides this with no person in the loop. The column merge_field.is_required says which values must be present. When one of them is empty, write the notice row in state Held with hold_reason set to that field, store no document, and call CaseWorkflowApi.raiseTask with task code Complete notice data and the case owner as owner role, carrying MSG-P6-007, which names the notice, the case and the field. Generation ends there: no render, no decision log entry, no document. AC3 is the test, with party P-0001 holding no postal address contact point and hold reason POSTAL_ADDRESS.

### Step 6

**In the story.** System: renders the DOCX template to PDF and adds the footer: case number, template code, template version and generation date.

The renderer does this. Build LetterRenderer to fill the DOCX body named by template.body_ref with the resolved values and render a PDF. The footer carries four items in order: case number, template code, template version and generation date, which AC1 shows as RC-2026-000123 DEMAND-MTG v2 2026-11-25. Use the ACE document rendering library, or docx4j with PDF export where ACE has none, which needs dependency approval under NFR-054. Thai text has to come out correctly, and the done condition is a generated PDF from the synthetic set opening in a standard PDF reader with its Thai shown.

### Step 7

**In the story.** System: writes the D7.1 decision log entry with rule R-LIT-03, the template code and version and the reference to the merge snapshot.

The service writes this through DecisionLogApi.write from P7, built in RWB-E1-027. The entry carries decision code D7.1, rule R-LIT-03, the template code and version, and an inputs reference pointing at the merge snapshot. It is written before the document is stored, which is the order section 12 fixes. A failed write means no notice at all: the call fails with MSG-P7-003, no notice row and no document are created, and an incident is raised under R-UNI-39. When the account data product is stale, the entry records the data date used, 2026-11-24 in AC7, and the result carries MSG-P1-001 naming the product and that date.

### Step 8

**In the story.** System: stores the PDF in the document hub as a generated, write-once document on the case.

The service calls the document hub; no person uploads anything. Call DocumentHubApi.storeGenerated with the case, the party, the document type and the PDF bytes. P5 owns the document table, so write nothing to it from this module. Write-once means the stored file is never replaced, and a correction is a new notice with a new document. AC1 expects source GENERATED and write_once true on the stored PDF. A failed document store rolls the notice back, and the decision log entry already written is followed by a correcting entry under R-UNI-24 rather than being changed in place.

### Step 9

**In the story.** System: creates the notice row in state Generated with the document ID, notice type and sent type, and writes NoticeGenerated to the outbox in the same transaction.

The service finishes the work in one transaction. Migration V1_052__notice_generation.sql alters the existing notice table to add party_id, template_id and hold_reason, adds the check constraint on state, and adds the unique index ux_notice_generation on case_id, notice_type, party_id and the date part of created_at. That index is the idempotency key: a repeat on the same business date hands back the first notice and creates no second one, which AC6 tests. Sent type is NPL for a case at 90 days past due or more, taken from LOV-SENT-TYPE. NoticeGeneratedPublisher writes NoticeGenerated, EV-13 with noticeId, caseId, type and templateVersion, to the outbox in that same transaction.

## RWB-E1-053 Field extraction for the six types into the index

Module: P5 Document hub

### Step 1

**In the story.** JOB-12 Document intake: runs extractStep after classifyStep and before matchStep.

Automatic. JOB-12 runs every 15 minutes in business hours and already holds the OCR and classification steps. Your change is to the job definition: add extractStep after classifyStep, so the document type is known, and before matchStep, so the extracted values are ready when the item is matched to its case. The step runs under the service identity SY-OCR with Documents CRU rights. With the feature flag rwb.dochub.extract off, extractStep sets extract_status to DONE with no fields, and items go on to matchStep with the OCR text only.

### Step 2

**In the story.** ExtractStep: selects intake items with ocr_status DONE and extract_status PENDING that are classified with no review_reason, or that carry a document ID with a given type (uploads), locking each row.

Automatic. Write the selection query over document_intake for rows whose ocr_status is DONE and extract_status is PENDING, taking two groups: items classified with no review_reason, and items that already carry a document_id with a known type, which is the upload path. Select with FOR UPDATE SKIP LOCKED, so a row another worker holds is passed over instead of waited for, which is how AC10 ends with one set of fields when two workers start together. The new index ix_intake_extract on extract_status for rows with ocr_status DONE serves this query. Add the three new intake columns in migration V1_5_053__extraction.sql.

### Step 3

**In the story.** ExtractStep: reads the field definitions of the type from the version of DocumentTypeCatalog in force, the threshold and the attempts.

Automatic. For each item, read the field definitions of its document type from the DocumentTypeCatalog version in force on the business date, which is DOCTYPE-2026.11 with six types and 26 fields. Each definition carries the field name, the data type, the personal flag, the extraction method TEMPLATE or MODEL, the review_only flag and an optional pattern. Read EXTRACT_FIELD_THRESHOLD, EXTRACT_MAX_ATTEMPTS and EXTRACT_TIMEOUT_SECONDS from document_hub_parameter in the same way. None of these values belongs in code, because the field list and the thresholds change through a load and an approval, not through a release.

### Step 4

**In the story.** ExtractStep: reads the page text and layout through OcrOutputReader.

Automatic. Call OcrOutputReader from RWB-E1-049 for the text and layout of each page of the item, and pass what it returns to the extractor. Read it through that interface rather than querying the text table yourself. The layout matters for the template path, which finds a value by its position on the page and by the anchor text near it. Build your tests against fixed OCR pages, so the extractor behavior can be checked without running OCR, which is what the build steps ask for in TemplateFieldExtractor and ModelFieldExtractor.

### Step 5

**In the story.** FieldExtractor: the extractor named by extraction_method returns a raw value and a confidence per field, with the extractor version.

Automatic. Define FieldExtractor with one method that takes the pages, the field definitions and the timeout and returns a raw value and a confidence for each field. Write two implementations and choose between them by the extraction_method of each field definition: TemplateFieldExtractor for TEMPLATE, which works from layout and anchor text, and ModelFieldExtractor for MODEL, which calls the model through the P10 gateway with the text masked the way RWB-E1-050 masks it. Each result carries the extractor version, for example EXT-TPL-1.0 in AC1, so a later report can say which extractor produced a value.

### Step 6

**In the story.** ValueNormalizer: converts each value to its data type: Thai and English dates to ISO dates, Buddhist Era years less BE_YEAR_OFFSET, Thai digits to Arabic digits, amounts to numeric(18,2) baht.

Automatic. Write ValueNormalizer to turn each raw value into the data type its definition names. Dates in Thai or English become ISO dates, a Buddhist Era year has BE_YEAR_OFFSET of 543 subtracted from it, Thai digits become Arabic digits, and amounts become numeric with two decimal places in baht. AC1 turns “1 ธันวาคม 2569” into 2026-12-01, and AC12 turns “3 October 2026” into 2026-10-03 and “THB 4,250,000” into 4250000.00. Unit test each conversion on its own, with the invalid date of AC6 among the cases, because this class carries most of the risk in the story.

### Step 7

**In the story.** ExtractStep: sets each field to state OK, or REVIEW when the confidence is below the threshold, the value cannot be converted, the value fails its pattern, or the field is review_only.

Automatic. For each field, FieldExtractionService sets the state from four conditions. A confidence at or above EXTRACT_FIELD_THRESHOLD gives OK, so the 0.8000 of AC5 passes at a threshold of 0.80 and the 0.6200 of AC3 does not. A value the normalizer cannot convert keeps its raw text with confidence 0.0000 and state REVIEW. A value that fails the pattern in its definition, such as the black case number format, also goes to REVIEW. A field marked review_only goes to REVIEW whatever its confidence, which AC4 shows with area_sq_wa at 0.9900.

### Step 8

**In the story.** ExtractStep: for an item with no document, writes the fields to document_intake.extracted_fields and sets extract_status DONE; matchStep (RWB-E1-032) passes them to DocumentStore.store, which writes the document_field rows and sets review_status PENDING when a field is in REVIEW.

Automatic, and this is the path for an item not yet attached to a case. Write the fields as JSON into the new extracted_fields column and set extract_status to DONE. matchStep from RWB-E1-032 then passes those fields in the StoreRequest to DocumentStore.store, which writes one document_field row per field and sets document.review_status to PENDING when any field is in REVIEW. Your work with RWB-E1-024 is to check that StoreRequest carries the state, the extracted value and the extractor version, and that the store sets review_status. The case number and account number extracted here are what matchStep uses to find the case.

### Step 9

**In the story.** ExtractStep: for an item with a document, writes the document_field rows directly, sets document.review_status PENDING when a field is in REVIEW, and writes DocumentFieldsExtracted (EV-17) to the outbox in the same transaction.

Automatic, and this is the upload path, where the document already exists. Write the document_field rows yourself through DocumentFieldRepository, set document.review_status to PENDING when any field is in REVIEW, and put the DocumentFieldsExtracted event in the outbox, the table events wait in until they are published. All three happen in one transaction, so the rows and the event are applied together or not at all. The event payload carries the document id, the field names and the confidence, never a value. For a new version of a document, write new active rows and set is_active false on the earlier version's rows, which the unique index ux_document_field_active requires.

### Step 10

**In the story.** Case owner: opens SCR-30 Case documents and sees the fields with their confidence; a document with review_status PENDING shows MSG-P5-003.

A person does this. The case owner, or the litigation officer, opens SCR-30 for a case in their scope and sees each document with its fields, the confidence of each field and a mark on the fields in REVIEW. A document whose review_status is PENDING shows MSG-P5-003 with a link to SCR-31. Build the screen with a loading state of skeleton rows and a list state. The read applies right R in the capability area Documents with the caller's scope: a role without it gets 403 with MSG-P4-002, and a document outside the scope gets 404 with MSG-P4-003 and no field value, as AC13 shows for a case owner of team MTG-BKK reading a document of team HP-NE.

## RWB-E1-054 Review queue for low-confidence documents

Module: P5 Document hub

### Step 1

**In the story.** Litigation officer: opens SCR-31 Document review queue.

A person opens the screen. SCR-31 Document review queue is new in this story, built as the React component ReviewQueuePage with four states: skeleton rows while the queue loads, the list itself, the state after an item is resolved, and the empty state showing the text No documents are waiting for review. The officer holds RW-LITOFF with the Documents CRU rights and team scope. The screen appears only when the feature flag rwb.dochub.review is on; with the flag off, the queue is hidden and the items waiting in it are left untouched.

### Step 2

**In the story.** System: lists, oldest first, the intake items with a review_reason and no case that belong to the officer's review team, the intake items whose candidate cases are in the officer's scope, and the stored documents with review_status PENDING on cases in scope; each row shows the reason, the proposed type, the two candidates, confidence and age.

The list is assembled by code as soon as the screen opens. ReviewQueueService answers GET /review-items and brings three groups into one list: intake items that carry a review_reason and no case, shown to the review team named in the document_hub_parameter row REVIEW_TEAM_UNATTACHED; intake items whose candidate cases fall in the officer's scope; and stored documents with review_status PENDING on cases in scope. Order by the time received, oldest first, and page at REVIEW_PAGE_SIZE, which is 50. Each row carries the reason, the proposed type, the type candidates with their confidence, and the age. Two partial indexes in your migration serve these reads.

### Step 3

**In the story.** Litigation officer: opens an item; the system shows the file, the OCR text, the type with its candidates, the candidate cases and the fields, with fields in REVIEW marked.

The officer picks a row, and the detail arrives from two endpoints you build. GET /intake-items/{intakeItemId} answers with the item: source, time received, review reason, predicted type and candidates, the candidate cases with their status, the page text, and the extracted fields with their state. GET /intake-items/{intakeItemId}/content answers with the file itself for the viewer. Mark every field whose state is REVIEW so the officer sees what needs a decision. Field values are masked for roles that may not see them. An item on a case outside the officer's scope answers 404 with MSG-P4-003 rather than revealing that it exists.

### Step 4

**In the story.** Litigation officer: keeps the type or chooses another type from the list in force; a new type re-runs extraction for that type and shows the new fields.

The officer chooses, and your code reacts. Keeping the type needs no call. Choosing another type is POST /intake-items/{intakeItemId}/resolve with action SET_TYPE, and you check the chosen type against the type version in force through DocumentTypeCatalog; a type outside that list answers 422 with MSG-P5-006 naming the value, as with PAYSLIP. For a type that is in force, call FieldExtraction.extractIntake so extraction runs again for the new type, then show the new field set with every field in state REVIEW. The fields of the old type are no longer offered: a demand letter changed to a guarantor notice shows the four guarantor notice fields.

### Step 5

**In the story.** Litigation officer: chooses the case from the candidates, or enters a case number that the system looks up through CaseDirectory.

The officer supplies the case. The candidate cases already on the item come from the matching step; when none of them is right, the officer types a case number and your code resolves it with CaseDirectory.findByCaseNo, a published P3 interface. Use that same call to read the case status, because a closed case is refused later with MSG-P5-005. Never query the case tables directly; the case module owns them and CaseDirectory is the only way in. The case chosen here also decides whose scope the item falls in.

### Step 6

**In the story.** Litigation officer: confirms each marked field with Confirm, or enters the value with Correct; the system checks it against the field data type and range.

Field by field, the officer decides and your endpoint saves. Confirm keeps the extracted value; Correct replaces it. Both go through PATCH /api/recovery/v1/documents/{documentId}/fields/{fieldId} with an If-Match header holding the document version the officer loaded, which lets the server refuse a save made against an older version. Validate the entered value against the field data type, and a date against the document_hub_parameter rows REVIEW_DATE_MIN and REVIEW_DATE_MAX, which hold 2000-01-01 and 2100-12-31, so a Buddhist year such as 2569-12-16 falls outside and answers 422 with MSG-GEN-002. An empty value on a Correct answers 422 with MSG-GEN-001. Keep the original in extracted_value and write the officer into confirmed_by.

### Step 7

**In the story.** Litigation officer: chooses Attach; the system calls DocumentStore.store with the case, the type and the fields, which writes the document, its fields and the DOCATT decision log entry, and stores a legal type in the write-once container.

The officer presses Attach and a chain of checks runs before anything is stored. Refuse with 422 when a field is still in state REVIEW (MSG-GEN-001), when the type is not in force (MSG-P5-006), or when the chosen case is closed (MSG-P5-005). When the file hash already belongs to a document on that case, link the item to the existing document instead of storing a second one and show MSG-P5-024. Otherwise call DocumentStore.store from RWB-E1-024 with the case, the type and the fields; it writes the document, its fields and the DOCATT decision log entry, and places a legal type in the write-once container. A failed decision log write stores nothing and answers MSG-P7-003.

### Step 8

**In the story.** System: sets the intake item review_outcome ATTACHED and the document review_status CONFIRMED (nothing changed) or CORRECTED (type, case or a value changed), and writes DocumentFieldsExtracted (EV-17).

This is bookkeeping your code does inside the same unit of work as the attach. Set review_outcome to ATTACHED on the intake item, with resolved_by and resolved_at, and set the document review_status: CONFIRMED when the type, the case and every value were kept as extracted, CORRECTED when any of them changed. Then publish DocumentFieldsExtracted, event EV-17. The four columns review_outcome, resolved_by, resolved_at and discard_reason are added to document_intake by the migration V1_5_054__review_outcome.sql in this story. An item with an outcome drops out of the queue, which is why the queue index looks for a review_reason with no review_outcome.

### Step 9

**In the story.** Litigation officer: for a stored document with a field in REVIEW, confirms or corrects the field and completes the review with POST review.

This is the second kind of item in the queue, and the officer works it the same way. For a document already stored whose field is in state REVIEW, the officer confirms or corrects with the PATCH call from step 6, then finishes with POST /documents/{documentId}/review carrying action COMPLETE and the document version. Refuse with 422 and MSG-GEN-001 while any field is still in REVIEW, and with 409 and MSG-GEN-004 when the version sent is older than the stored one. On success set review_status to CONFIRMED or CORRECTED by the same rule as step 8. RWB-E2-017 reuses this action for generated drafts.

### Step 10

**In the story.** Center of excellence analyst: the model evaluations (RWB-E1-060) read the resolved items through LabeledSetReader.

Nobody clicks this; another module pulls the data. Build LabeledSetReader as a published P5 interface with resolvedSince(since, limit), answering with each resolved item as a labeled example: the intake or document ID, the predicted type, the confirmed type, and per field the name, the extracted value, the confirmed value, the confidence and the extractor version. The model evaluations in RWB-E1-060 call it; those evaluations are out of scope here, so your part ends at the interface and its tests. The examples hold real field values, so they stay inside the bank and go into no log and no prompt.

## RWB-E1-055 Proof of delivery capture design with WIN

Module: P6 Communications

### Step 1

**In the story.** JOB-10 WIN outbound notices, daily 16:00: selects notices in a dispatch-eligible state with no sent date.

Quartz starts JOB-10 every day at 16:00 Bangkok time with no person involved. WinNoticeFileJob selects the notices to send: those in a dispatch eligible state with no sent date. The eligible states are configuration, rwb.comms.dispatch.eligible-states set to GENERATED in Epic 1, so read the value and keep no state name in code. The index ix_notice_state_sent on state and sent_date supports the query. A notice already written into an unacknowledged file of the same date is skipped, which is how a rerun from SCR-44 writes no notice twice (AC8). The platform administrator can rerun the job from that screen.

### Step 2

**In the story.** System: builds one INT-14 file: ContractNO of the case's primary account, addressee, address detokenized through the ACE PII service, notice type, template version and document reference; writes the trailer with the record count.

WinNoticeFileWriter builds one file per run to the INT-14 layout. Each record carries the contract number of the case primary account, the addressee, the address, the notice type, the template version and the document reference. The contract number comes through the P1 and P3 interfaces, from the case_account row marked is_primary and loan_account.contract_no, with no direct read of another module tables. The address is held as a token, so call PiiService.detokenize to put the real value into the outbound file stream only and keep it out of every log line. The file ends with a trailer, a final record holding the count of records, which lets WIN check that nothing was lost in transit.

### Step 3

**In the story.** System: hands the file to the integration adapters and marks each notice "file sent" with the file ID.

The system hands the finished file to the P2 integration adapters by calling WinFileGateway.send, and the adapters place it on the SFTP path agreed with the WIN owner. No code in this story talks to WIN directly (REQ-DRI-006). For each notice in the file you then write dispatch_file_id with the file ID and add one to dispatch_attempts, both new columns from migration V1_055__notice_dispatch.sql. The notice state does not change yet and stays Generated until WIN acknowledges. The attempt count is what the limit rwb.comms.dispatch.max-attempts, set to 3, is measured against.

### Step 4

**In the story.** Integration adapters: deliver the WIN acknowledgment, which carries per ContractNO the sent date (DDMMYYYY), Barcode and Sent Type (s2t mapping of INT-14).

WIN answers with an acknowledgment file, and the P2 adapters deliver it by calling WinAcknowledgmentHandler.onAcknowledgment, a published interface you implement in P6. The acknowledgment holds one entry per contract number with the sent date, the barcode and the sent type, following the s2t mapping of INT-14. The sent date arrives as DDMMYYYY, so 26112026 has to be parsed into 2026-11-26 before it is stored. When no acknowledgment arrives, the notices stay Generated with their file sent and the next JOB-10 run writes them again; after the third attempt a task goes to the litigation officer team with MSG-GEN-006 naming WIN (AC4).

### Step 5

**In the story.** System: sets notice state Sent with sent_date, barcode and sent_type; writes a LETTER entry to the interaction ledger; publishes NoticeDispatched.

The handler applies the acknowledgment. For each entry it sets the notice state to Sent and fills sent_date, barcode and sent_type. The unique index ux_notice_barcode keeps one barcode on one notice. It then writes an outbound LETTER entry to the interaction ledger through InteractionLedgerApi.record from RWB-E1-066, and writes NoticeDispatched to the outbox through NoticeEventPublisher, so the event is delivered after the change is committed. The case record then shows MSG-P6-004 with the notice type and the date. AC1 covers the whole step with barcode RR123456789TH and sent date 2026-11-26.

### Step 6

**In the story.** JOB-09 File loads, weekly Monday 04:00: loads the INT-15 proof of delivery file and runs checks DQ-085 to DQ-091.

JOB-09 runs weekly on Monday at 04:00, or on file arrival, and loads the INT-15 proof of delivery file. You build WinProofOfDeliveryStep as a Spring Batch step inside that job, running checks DQ-085 to DQ-091 on the file. A file failing any one of them is refused in full: nothing is written, the delivery data already on the notices stays as it is, and the message is MSG-P1-002 naming the check, for example a trailer saying 40 records against a body of 39 (AC5). A file for a business date that has already loaded is refused the same way (AC7). A corrected file is loaded whole.

### Step 7

**In the story.** System: matches each record to a notice by barcode, then by ContractNO and sent date; sets callback_date, delivery_status DELIVERED and state Delivered.

DeliveryMatcher ties each record in the file to a notice. It matches on the barcode first, and when that finds nothing it matches on the contract number together with the sent date. On a match the system sets callback_date from the call back date in the record, delivery_status to DELIVERED and the notice state to Delivered. A record matching no notice on either key is held on the exception list with check References, and the other records in the same file still load, so 29 of 30 records update their notices (AC6). The data steward sees the held records on SCR-45.

### Step 8

**In the story.** System: writes the delivery to the interaction ledger and publishes NoticeDelivered with the delivery date; P3 starts the notice period timer from that date.

Two writes follow each matched delivery. The system records the delivery in the interaction ledger through the ledger writer, and publishes NoticeDelivered to the outbox with the delivery date. P3 consumes that event and starts the NOTICE_PERIOD timer from the delivery date, so the notice period counts from the day the letter arrived (CTL-15). P3 already holds that consumer from RWB-E1-028, so your part is the event and the delivered date on it. A later file repeating a delivery already recorded leaves the notice unchanged, publishes no second event, and counts the repeat under R-UNI-40 (AC10).

### Step 9

**In the story.** System: each day, compares notices sent to WIN with barcodes returned (REC-05) and lists any notice with no barcode three days after sending for the platform administrator.

BarcodeReconciliation is a daily job you build, running after JOB-01. It compares the notices written to WIN files with the barcodes that have come back, which is reconciliation REC-05, and lists any notice still without a barcode three days after it was sent. The three days come from rwb.comms.dispatch.barcode-break-days, so the number is configuration. The breaks go to the platform administrator on SCR-45 Data quality, as AC9 shows with notice N-0002 sent on 2026-11-25 and listed on 2026-11-28. The same job marks the notice data product stale one business day after an INT-15 file was due, which produces MSG-P1-001 on the case (AC11).

## RWB-E1-056 Run books and monitoring for every Epic 1 job

Module: P2 Integration

### Step 1

**In the story.** Platform administrator: adds a job_catalog row per job with job ID, name, owner role, schedule, run book path, expected duration and alert threshold.

A person owns these rows, and the platform administrator keeps them. Your part is the table and the first rows. Build job_catalog in migration V2026_11_56__p2_job_catalog.sql with job_id as the primary key and a check that it matches ^JOB-[0-9]{2}$, which refuses a job ID in any other shape. Build the JobCatalogEntry entity and JobCatalogRepository over it. The migration inserts the 13 Epic 1 rows from the batch schedule, each with the job name, the owner role, the schedule text, the run book path, the expected minutes, the alert threshold in minutes and first_release. Thresholds are assumed at 1.5 times the expected duration.

### Step 2

**In the story.** Squad member (RW-TRIBE): writes the run book at `docs/operations/runbooks/<job ID>.md` with the six sections.

A person writes these too, one file per job, and the squad that built the job writes its own. The path is docs/operations/runbooks/<job ID>.md and it must match the runbook_path on the catalog row. Six headings are required: purpose, schedule, owner, failure signs, restart steps and escalation. Write the restart steps so that the operations team can follow them without the developer, since that is the whole point of the story. Name roles and service identities in the text, never a person, because the file outlives whoever holds the job today. Thirteen run books are needed for Epic 1.

### Step 3

**In the story.** Pipeline: RunbookCompletenessTest checks that every Quartz job and Spring Batch job in the service has a catalog row and a run book with the six headings; it fails the build if one is missing.

The build does the checking, so a missing run book cannot be merged. Build RunbookCompletenessTest to find every Quartz JobDetail bean and every Spring Batch Job bean in the service and, for each one, assert that a job_catalog row exists and that the file at its runbook_path holds all six headings. A failure stops the build with MSG-P2-005 naming the job and the missing section, as AC4 describes for a job whose run book has no Escalation section. Finding the jobs from the Spring context instead of from a written list means a job added later is caught on its first build.

### Step 4

**In the story.** Each job: writes a structured event `rwb.job.run` at start and end with job ID, business date, status and duration.

The jobs emit this themselves once you attach the listener. Build JobRunEventListener as a Spring Batch JobExecutionListener and attach it to every Spring Batch job, so no squad writes logging code of its own. It emits an event named rwb.job.run at the start and at the end of a run, carrying the job ID, the business date, the status and the duration. Structured means the fields are separate named values rather than one sentence, which is what lets Log Analytics filter and total them. Put no personal data in the event: job IDs, dates, counts and durations only.

### Step 5

**In the story.** Platform administrator: opens the Log Analytics workbook "Recovery jobs" or calls GET /admin/jobs and sees last run, status and duration per job.

A person looks, and both paths have to show the same numbers. Build the Log Analytics workbook named "Recovery jobs" in ops/monitoring, with one line per job holding its last run time, status and duration. For the endpoint, build JobOperationsImpl.lastRun, which reads the last run from the Spring Batch job repository through the framework rather than by querying its tables. GET /admin/jobs then answers with the job ID, type, business date, status, startedAt and endedAt. Reading needs Platform administration right R, which RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-COE and RW-SECADM hold as well as RW-PLATADM.

### Step 6

**In the story.** Alert rule: a job with status FAILED, or running longer than its alert threshold, emails the owner role and RW-PLATADM with MSG-P2-004.

No one is watching the workbook at 05:00, so two alert rules do it. Build them in ops/monitoring over the rwb.job.run events: one for a run whose status is FAILED, one for a run still going past alert_after_minutes on its catalog row. Each one emails the role in owner_role and RW-PLATADM with MSG-P2-004, which names the job, the time, the business date and the run book to follow. The owner is the role from the batch schedule, so JOB-01 and JOB-02 alert the data steward and JOB-03 the team managers. A job over its threshold is alerted and left running; the rule never stops it. Test each rule with a forced failure in SIT.

### Step 7

**In the story.** Platform administrator: follows the restart steps in the run book and calls POST /admin/jobs/{jobId}/rerun.

A person drives the restart, with the run book open. The endpoint takes the ID of the failed execution, not the job ID on the catalog row, and calls JobOperations.rerun. Build it on the Spring Batch JobOperator.restart call. Check first whether the job is running: if it is, throw JobAlreadyRunningException and map it to 409 with MSG-P2-006, and let the running job carry on. An unknown execution answers 404 with MSG-P4-003. The call needs Platform administration right U, so RW-TEAMMGR, who receives the alerts for JOB-03 and JOB-06, cannot make it, and RW-CASEOWN is refused with MSG-P4-002.

### Step 8

**In the story.** System: restarts the job from its failed step; the dependent jobs run in the order of the daily timeline.

The service does the rest. Spring Batch restarts the execution at the step that failed instead of at the beginning, so the steps that already completed are not run twice. The jobs that depend on it then run in the order of the daily timeline, which is why AC2 expects JOB-02 after JOB-01. A rerun has to be idempotent for the job and the business date, meaning a second run has no further effect: running JOB-01 again for a date it already completed writes each interface run as DUPLICATE and loads no account record a second time, which the unique key on interface_run from RWB-E1-007 enforces.

## RWB-E1-057 Intake from branches, mailroom, partner SFTP and email

Module: P5 Document hub

### Step 1

**In the story.** Scheduler: JOB-12 Document intake fires every 15 minutes in business hours on one service instance; intakeStep runs first, before scanStep.

Nothing here is done by hand. The job is JOB-12 Document intake, which already exists as the Spring Batch job DocumentIntakeJob from RWB-E1-049, and this story adds intakeStep as its first step, ahead of the malware scan step of RWB-E1-041. The Quartz cron in section 12 is 0 0/15 8-17 in Asia/Bangkok on Monday to Friday, and bank holidays from the reference data holiday table are skipped. Two service instances may be running, so the schedule has to produce one run only: AC12 expects a single run recorded for 09:15 and one document_intake row per file. Outside business hours no run starts, which is exception path X11 and AC15.

### Step 2

**In the story.** IntakeStep: lists new files in each branch scanner folder and the mailroom folder, in each partner subfolder of the SFTP inbound folder, and new messages in each recovery mailbox.

IntakeStep lists the work automatically through three readers you build behind one interface, IntakeChannelReader, with listNew, open, markProcessed and markRejected. FolderChannelReader covers the branch scanner folders, one per branch code, and the mailroom folder. SftpChannelReader covers each partner subfolder under the SFTP inbound folder. MailboxChannelReader covers each recovery mailbox, read as Exchange Online through Microsoft Graph by the SY-OCR managed identity, which is an identity the platform holds for the service so no password or key is kept anywhere. Every folder path and mailbox address is a property set per environment by the platform administrator, and each channel has its own sub-flag under rwb.dochub.intake.

### Step 3

**In the story.** IntakeStep: for each file or email attachment computes the SHA-256 hash and checks document_intake for the same channel and hash inside the duplicate window.

IntakeService does this for each file and each email attachment. A SHA-256 hash is a fixed value computed from the file's bytes, so two copies of one file give the same value and any change gives a different one. Look in document_intake for the same channel_code and file_sha256 with received_at inside the window the parameter INTAKE_DUPLICATE_WINDOW_DAYS sets, loaded as 30 days. A match means no new row: move the file to the processed folder and count it as a duplicate, which is exception path X4 and AC8. The index ix_intake_hash on document_intake (channel_code, file_sha256, received_at) serves this lookup.

### Step 4

**In the story.** IntakeStep: checks the file type by content and extension, and the size, against the parameters.

The same service applies the two limits, with no person involved. Check the type by the file's content as well as its extension and accept only the values in INTAKE_ALLOWED_TYPES, loaded as PDF, JPG and PNG. Check the size against INTAKE_MAX_FILE_MB, loaded as 25. A refused file gets no document_intake row, is moved to the rejected folder of its channel and is counted as refused, with MSG-P5-007 on the job record and MSG-P5-001 or MSG-P5-017 as the reason. Test the boundary exactly as AC6 sets it: a file of 25.1 MB is refused and one of 25.0 MB is taken in.

### Step 5

**In the story.** IntakeStep: for a partner file, reads the partner by the subfolder's partner_code and checks that its panel_status is ACTIVE.

SftpChannelReader applies this check by itself. The subfolder name is the partner_code, and you resolve it through the S9 published interface PartnerDirectory.findByCode, which returns the partner's id, code, type and panel status. Your module never reads the partner table. Take the file in only when a partner is found and its panel_status is ACTIVE, and write that partner's id to document_intake.partner_id. An unknown code and a partner that is not ACTIVE are both refused, with no row written and the file moved to the rejected folder, counted with the reasons PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE. This is exception path X3 and AC7.

### Step 6

**In the story.** IntakeStep: copies an accepted file to the intake container and writes one document_intake row with source, channel code, source reference, file name, size, hash, received time, scanner time (scanner files), partner ID (partner files) or sender address (email), and the run ID; scan_result is left empty for scanStep.

IntakeService copies the accepted file into the intake container of RWB-TE-012, reached by managed identity only, then writes one document_intake row. The row holds source SCAN, PARTNER or EMAIL per BR1, the channel code, the source reference, the file name, size and hash, the received time, the scanner time in captured_at for scanner files, the partner id for partner files or the sender address for email, and the run id. Leave scan_result empty, because scanStep sets it and ocrStep reads nothing until it says CLEAN, which is AC16. The seven new columns come from the migration V1_5_057__intake_channels.sql, which also widens source_ref to varchar(400).

### Step 7

**In the story.** IntakeStep: after the commit, moves the scanner or SFTP file to the processed folder, or moves the email to the archive folder; a refused file goes to the rejected folder.

The order matters and your code keeps it: commit the document_intake row first, then move the source file. A file moved before the commit could be lost when the transaction rolls back, so BR6 allows the move only after the commit. Scanner and SFTP files go to the processed folder, emails to the archive folder of their mailbox, and refused files to the rejected folder. When the move fails after a successful commit, leave it: the next run sees the file again, finds the same channel and hash, writes no second row and moves it then, which is exception path X10 and AC14. Build the unit test for this order, as build step 2 says.

### Step 8

**In the story.** IntakeStep: writes the counts per channel and result (taken in, refused by reason, duplicate) to the job record shown on SCR-44 Interface and job monitor.

IntakeStep writes its own counts with no person involved: for each channel, the number taken in, the number refused with the reason, and the number treated as duplicates. Write them to the job record that SCR-44 Interface and job monitor reads, so the platform administrator sees each run. A run where no channel has a new file still writes zero counts for every channel, which is exception path X5 and AC9. No sender address and no email file name may appear in these counts or in any log, because BR9 treats the sender address as personal data, masked by role and never logged.

### Step 9

**In the story.** ScanStep, ocrStep, classifyStep, extractStep and matchStep (RWB-E1-041, RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-032) then run on the new rows in the same job.

These five steps already exist in other stories and they run after yours inside the same JOB-12 run: scanStep from RWB-E1-041, ocrStep from RWB-E1-049, classifyStep from RWB-E1-050, extractStep from RWB-E1-053 and matchStep from RWB-E1-032. You build none of them. Your work is to place intakeStep ahead of them in DocumentIntakeJob and to leave each new row in the state they expect, with scan_result empty and ocr_status PENDING. scanStep then sets scan_result and quarantines an infected file, and ocrStep reads only a file whose scan_result is CLEAN, which TC-E1-057-16 tests with a delayed scanStep stub.

### Step 10

**In the story.** Platform administrator: sees the run on SCR-44 and reruns a failed run when needed.

A person does this, the platform administrator holding Platform administration U. SCR-44 shows each JOB-12 run in the states running, failed and complete with the intakeStep counts per channel, and the rerun is POST /api/recovery/v1/admin/jobs/{jobId}/rerun with the job id of a failed run. A rerun while a run is still in progress is refused with 409 and MSG-GEN-004, and a caller without the right is refused with 403 and MSG-P4-002, which is the access test TC-E1-057-17. A failed run leaves its files at the channel, so the next scheduled run takes them even without a rerun. Add the intakeStep section to the JOB-12 run book of RWB-E1-056.

## RWB-E1-058 Agent platform set-up [E1a]

Module: P10 Agent runtime

### Step 1

**In the story.** RW-COE: loads a prompt file and a policy file for agent "INTAKE" through POST /admin/agent-configs.

A person does this: a center of excellence analyst holding Rules and parameters right C. They post each file to /api/recovery/v1/admin/agent-configs as multipart form data with the file in JSON, the kind PROMPT or POLICY, the agent code and a valid from date. The policy file carries the values the runtime reads later: model code and version, output schema reference, allowed tools, autonomy mode, confidence floor, timeout seconds, daily cost cap, price per 1,000 tokens, alert role and review date. Build AgentConfigController for the endpoint and AgentConfigService behind it. The agent in this flow is INTAKE; the test agent ECHO is seeded from files in src/test/resources/agent/.

### Step 2

**In the story.** System: validates each file, stores it as a new version with status "LOADED" and keeps every earlier version readable.

The service does this with no person involved. Validate the file against the policy JSON schema file that is versioned with the loader, which holds the limits: timeout seconds between 1 and 120, confidence floor between 0 and 1. A file that fails any check is refused in full with 422 and MSG-P10-001 naming the check, and no version row is created, so the version already in force is untouched. A file that passes becomes a new row in agent_policy or agent_prompt with status LOADED, its valid from date and the loader, and for a prompt the body text and its hash. Earlier versions stay readable through GET /admin/agent-configs with their hashes unchanged.

### Step 3

**In the story.** RW-RISK: approves the version through POST /admin/agent-configs/{versionId}/approve; the version takes effect on its valid from date.

A different person does this: a risk and model risk officer holding Rules and parameters right A. They call POST /admin/agent-configs/{versionId}/approve with an If-Match header carrying the row version they read, and the status moves from LOADED to APPROVED. Build two rules. The loader may not approve their own version, so compare the approver with loaded_by and refuse with 409 and MSG-P7-002. The If-Match value is checked against the current row version, so when two officers approve at the same moment the first succeeds and the second gets 409 with MSG-GEN-004. An approved version takes effect on its valid from date, and the version it replaces is retired with valid_to set to the day before.

### Step 4

**In the story.** Calling step (any module, through RWB-TE-013): asks the orchestrator to run agent "INTAKE" for one case with an idempotency key.

Another module calls this in code, through the orchestration built in RWB-TE-013, and no person is involved. The entry point is AgentOrchestrator.run with an AgentRunRequest holding the agent code, the case ID, a subject ID, the trigger event, the inputs and an idempotency key. Idempotent means a repeat has no further effect: agent_run carries a unique key on idempotency_key, so a second request with the key ECHO:RW-2026-000101:2026-11-30 writes no second row, makes no second model call, returns the result of the first run and counts the repeat. Build the request and result types in package recovery.agent.orchestrator, so every caller reaches a model by one path.

### Step 5

**In the story.** System: reads the approved policy and prompt in force, reads the inputs through the tool gateway, masks personal fields through the P4 masking service and calls the model endpoint with the policy timeout.

AgentRuntimeService does all of this with no person involved. Resolve the policy and prompt versions with status APPROVED whose valid from date is on or before the run date; a run already open keeps the versions it started with. Gather the inputs through ToolGateway, which executes only the tools on the policy allowed list, acts as the service identity SY-AGENT and reads through the published interfaces of P3 and P5. Pass every input value through PromptInputMasker, which calls the P4 masking service built in RWB-E1-037, so the prompt holds masking tokens in place of names, national ID numbers, phone numbers and account numbers. Then call the INT-23 endpoint through ModelGatewayClient with the policy timeout and no retry inside the step.

### Step 6

**In the story.** System: runs the guardrail checker on the answer: output schema, allowed tool list and confidence floor.

GuardrailChecker does this on the answer, with no person involved, and the order is fixed. First the output schema: validate the answer against the schema named by the policy, using JSON Schema draft 2020-12, and fail with check code SCHEMA naming the field that is missing. Second the allowed tool list: a tool the agent asked for that is not on the policy list is refused, is not executed and is logged with check code TOOL_NOT_ALLOWED. Third the confidence floor: an answer with confidence 0.79 against a floor of 0.80 gives status BELOW_FLOOR. The first check that fails sets the run status and sets fallback true, and the checks after it are not run.

### Step 7

**In the story.** System: writes one agent run row with the agent, policy, prompt and model versions, status, latency, tokens and cost, and publishes AgentRunCompleted.

The service writes the record with no person involved. Insert one agent_run row holding the agent code, the agent version, the prompt and model versions, the case and subject, the autonomy mode, the trigger event, the idempotency key, the status, the fallback flag, the guardrail result, the output, the confidence, latency_ms, tokens_in, tokens_out, cost_thb, the data as of date and the run time. Compute the cost as tokens in plus tokens out, divided by 1,000, multiplied by the policy price per 1,000 tokens, rounded to four decimals: 1,050 tokens at 0.0500 baht gives 0.0525. Write the AgentRunCompleted event EV-28 to the outbox in the same transaction as the row, so the event and the record cannot disagree.

### Step 8

**In the story.** System: returns the checked answer, or a fallback result with its reason, to the calling step.

The orchestrator answers its caller in code, with no person involved. The AgentRunResult carries the run ID, the status, the fallback flag, a fallback reason, the output, the confidence, the agent version and the model version. The fallback reason is the one value the caller acts on: TIMED_OUT when the endpoint did not answer inside the policy timeout, TOOL_NOT_ALLOWED or the schema code from the guardrail, BELOW_FLOOR under the confidence floor, and DISABLED when the feature flag rwb.agent.platform is off and no model call was made. On any fallback the calling step uses its rule result under R-UNI-32. None of these paths shows a message to a user.

### Step 9

**In the story.** RW-COE: loads a labeled sample through POST /admin/agent-samples and starts the evaluation harness through POST /admin/agent-evaluations.

A person does both of these: the center of excellence analyst. First they post a labeled sample to /admin/agent-samples as a CSV with the columns subject_type, subject_id, label_key and expected_value, and each load creates the next sample version. Then they start the harness with POST /admin/agent-evaluations carrying the agent, the sample code, the sample version and the approaches, which default to AGENT alone. Build two refusals: 422 with MSG-P10-002 when the sample holds no labeled row for that agent, and 409 with MSG-P10-003 when an evaluation of the same agent, sample and sample version is already RUNNING. A partial unique index on agent_evaluation_run enforces the second, applying only to rows whose status is RUNNING.

### Step 10

**In the story.** System: runs the agent on every sample row in shadow, scores it against the labels and stores the scores with the policy, prompt and model versions.

EvaluationHarness does the work with no person involved, after the endpoint has answered 202 with status RUNNING. Run the agent once for every row of the sample in shadow mode, which means the answer is scored and stored and no case is changed by it; each run writes a normal agent_run row with trigger EVALUATION and mode SHADOW. Compare each answer with the expected value of its label key and write one agent_evaluation score row per label key, holding the approach, sample size, true positives, false positives, false negatives, agreement rate, precision and recall. Each score row carries the policy, prompt and model versions, so a score can later be read against the versions that produced it. The run then moves to DONE.

## RWB-E1-059 Case intake agent in shadow [E1b]

Module: P10 Agent runtime

### Step 1

**In the story.** SY-CASEWF: creates case "RW-2026-000301" and writes EV-01 CaseCreated to the outbox.

No person is involved and nothing in this story does this. The case workflow module, under service identity SY-CASEWF, creates and allocates cases daily and writes event EV-01 CaseCreated to the outbox, all of it built in RWB-E1-030. An outbox is a table the publishing module writes the event into inside the same transaction as the case, so the event cannot be lost when messaging is down. The event carries caseId, caseNo, productGroup, accounts and businessDate. Your work starts on the consumer side in step 2; for this step you only need cases being created in DEV to test against.

### Step 2

**In the story.** System (IntakeShadowListener): receives the event and calls the orchestrator for agent "INTAKE" with key "INTAKE:<caseId>:<businessDate>".

This runs on its own. Build IntakeShadowListener in package recovery.agent.intake to consume EV-01 from the outbox and call AgentOrchestrator from RWB-E1-058 for agent INTAKE. Build the run key INTAKE:<caseId>:<businessDate> and hold it in agent_run.idempotency_key. Idempotent here means the same event delivered twice leaves one run: the listener checks the event ID and that run key, and counts the repeat. The listener sits behind feature flag rwb.agent.intake-shadow, and with the flag off it ignores CaseCreated, so this work can ship without touching case creation.

### Step 3

**In the story.** System: reads the case, accounts, documents, valuations and contact points through the tool gateway as SY-AGENT, masks personal fields and calls the model.

This runs on its own. Build IntakeInputAssembler to call the five allowed tools through the gateway: read_case, read_accounts and read_contact_points on the P3 CaseQueryService, read_documents on the P5 DocumentQueryService and read_valuations on the P1 CollateralQueryService. Each call runs under service identity SY-AGENT, which holds Case record R and Documents R, so the agent reads no more than its role allows and touches no other module's tables. Mask every personal field before the request leaves, so the model receives masking tokens only. Then call the model with prompt version PR1 and the 60 second timeout from policy P1. Write a test that no personal field reaches the request.

### Step 4

**In the story.** System: checks the answer (schema, tools, floor) and stores the summary and gap flags on the agent run with mode SHADOW.

This runs on its own in the guardrail from RWB-E1-058. There are three checks on the model's answer. It has to match output schema intake-summary-v1, with summary up to 1,500 characters, gaps holding a gapType from the enum with reason and sourceRef, and confidence between 0 and 1. It may have used only tools on the allowed list. Its confidence has to reach the floor of 0.80. Add the stale input rule here as check SCHEMA_RULE for INTAKE. Write the agent_run row either way, with status ANSWERED, TIMED_OUT, GUARDRAIL_FAILED or BELOW_FLOOR, autonomy_mode SHADOW, the policy, prompt and model versions, output, confidence, latency, tokens, cost and data_as_of.

### Step 5

**In the story.** System: publishes EV-28 AgentRunCompleted; no screen and no case field changes.

This runs on its own. Publish EV-28 AgentRunCompleted with runId, agent INTAKE, caseId, outcome and fallback. SHADOW mode means the output is stored and shown to nobody, so this step has to leave no other trace: no case field, no task, no queue entry and no decision log entry changes, and the case owner sees nothing. GET /cases/{caseId} and the case timeline return no agent output, and GET /admin/agent-runs returns run metadata without the summary or the gap flags. Write tests that look for exactly those absences, because the agreement rate is only worth measuring while nobody has acted on the output.

### Step 6

**In the story.** RW-COE: starts the evaluation of "INTAKE" on sample "INTAKE-S1" through POST /admin/agent-evaluations.

A person starts this. The center of excellence analyst sends POST /admin/agent-evaluations with agent INTAKE, sampleCode INTAKE-S1 and sampleVersion 1, holding Rules and parameters C. The endpoint comes from RWB-E1-058 and answers 202 with an AgentEvaluationRun, so the comparison runs in the background. One RUNNING run is allowed per agent and sample version, and a second attempt is 409 with MSG-P10-003. A sample with no labeled rows for the agent is 422 with MSG-P10-002, which tells the analyst to load the labels first. The same analyst loaded sample INTAKE-S1, the business analysts' review of 200 Epic 1 cases with one row per case and gap type.

### Step 7

**In the story.** System: runs the agent in shadow on each of the 200 sample cases and compares each gap flag with the label.

This runs on its own inside the evaluation harness from RWB-E1-058. For each of the 200 cases in the sample the agent runs again in SHADOW mode, through the same assembler, guardrail and policy as a live shadow run, and its agent_run row carries the evaluation_run_id. Build IntakeOutputScorer to compare, per case and gap type, the flag the agent returned against expected_value Y or N in agent_sample. Cases with no label are left out of the comparison and listed as unlabeled on the evaluation run, so a sample labeled for 180 of 200 cases is scored on 180. Test the scorer on a small fixture whose counts you already know.

### Step 8

**In the story.** System: stores one score row per gap type with the agreement rate, precision, recall and sample size.

This runs on its own at the end of the evaluation. Write one agent_evaluation row per gap type: MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT. Each row holds evaluation_run_id, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value and recall_value, together with the policy, prompt and model versions. The agreement rate is the count of cases where the agent's flag equals the label divided by the labeled cases, to four decimals, so 182 agreeing cases out of 200 gives 0.9100. Precision and recall come from the same three counts. Move the evaluation run from RUNNING to DONE.

### Step 9

**In the story.** RW-COE: reads the scores through GET /admin/agent-evaluations.

A person does this. The analyst calls GET /admin/agent-evaluations with agent, from and to, holding Rules and parameters R; RW-RISK may read the same scores. The response is the evaluation runs with their score rows. No screen is built in this story, so the read happens through an API client, and a role without the right is refused with 403 and MSG-P4-002. These numbers are the purpose of the shadow run: the move of the intake agent to autonomy level 1 in RWB-E2-028 rests on the measured agreement rate per gap type, and the report with the level 1 proposal is built in RWB-E1-061.

## RWB-E1-060 Extraction evaluation [E1c]

Module: P10 Agent runtime

### Step 1

**In the story.** RW-COE: loads sample "EXTRACT-S1" through POST /admin/agent-samples with one row per document and field.

A person starts this. The center of excellence analyst uploads a CSV through the endpoint built in RWB-E1-058, one row per document and field: subject_type DOCUMENT, subject_id, label_key as the field name and expected_value as the value a person confirmed or corrected. The analyst needs Rules and parameters C. Each upload creates a new sample version rather than changing the one before it. Your work is SampleRowValidator, which checks every row against the P5 interface before anything is stored, and the hashing of personal label values with SHA-256 so the stored sample holds no readable customer data. A row naming a document P5 does not return refuses the whole file with 422 and MSG-P10-001.

### Step 2

**In the story.** RW-COE: starts the evaluation with approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL through POST /admin/agent-evaluations.

The analyst makes this call, with agent EXTRACT, sampleCode EXTRACT-S1, sampleVersion 1 and the three approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL. The endpoint answers 202 and the work goes on in the background, so the caller does not wait for the scoring. Write one agent_evaluation_run row with status RUNNING, the agent code and the sample code and version, and set it to DONE when the scoring finishes. Only one RUNNING run is allowed per agent and sample version, so a second request while the first is running receives 409 with MSG-P10-003.

### Step 3

**In the story.** System: for OCR_TEMPLATE, reads the stored document_field values through the P5 interface; makes no model call.

The run does this without a person and without the model. ExtractionApproachRunner calls DocumentQueryService.getFields(documentId) as SY-AGENT for each document in the sample and takes field_value and confidence as the P5 pipeline of RWB-E1-053 already wrote them. No prompt is sent and no token is spent, which is why a tie is later settled in this approach's favor. Do not read P5 tables; the interface is the only route to the fields. Keep the confidence of every field, because the threshold the story proposes later needs to know at which confidence the values were right.

### Step 4

**In the story.** System: for MODEL, calls agent "EXTRACT" in shadow on the document content and reads the fields from its answer.

The run makes these calls itself, through AgentOrchestrator. Shadow mode means the model's answer is recorded and scored and never reaches a case or a document record, so a wrong answer here changes nothing in the Workbench. Use the approved policy EXTRACT version P1 with prompt PR1 and the allowed tools read_document_content and read_document_fields, and write one agent_run row per call with its status, latency, tokens and cost. When the model times out or fails a guardrail on a document, every labeled field of that document counts as a false negative for MODEL and the failure is counted on the evaluation run.

### Step 5

**In the story.** System: for OCR_AND_MODEL, passes the OCR fields with the content to agent "EXTRACT" and takes its checked values.

The run does this as a third pass over the same documents. Send the stored OCR field values together with the document content to the same agent, and keep the values the model returns after it has seen both. This approach costs one model call per document, as MODEL does, so it sits between the two others when a tie has to be settled. All three approaches have to run over the same documents and the same labels, because the scores are compared with each other. Build step 3 adds this path and the MODEL path together, covering AC1 and AC4.

### Step 6

**In the story.** System: compares each value with the label and stores true positives, false positives, false negatives, precision and recall per field and approach.

FieldMatchScorer does the comparison in code. A value counts as a true positive when it equals the label after trimming spaces and folding case; dates are compared as dates, and personal fields are compared by their SHA-256 hashes. A wrong value is a false positive and a missing value is a false negative. Precision is true positives divided by true positives plus false positives. Recall is true positives divided by true positives plus false negatives. Write both to four decimal places on one agent_evaluation row per label_key and approach, with the sample size, and keep the model version and prompt version on the rows where the model was called.

### Step 7

**In the story.** System: for each document type, picks the approach with the highest F1 and proposes the confidence threshold for the review queue.

ExtractionProposalBuilder computes this and writes it to the proposal column on the evaluation run; no person chooses at this point. F1 combines precision and recall as two times precision times recall divided by their sum. Take the approach with the highest mean F1 across the type's fields, and settle a tie in favor of fewer model calls, OCR_TEMPLATE before OCR_AND_MODEL before MODEL. The proposed threshold is the lowest confidence at which every chosen field reaches the target precision of 0.95, and a field that never reaches it is proposed as review-only. A type with fewer labeled documents than the minimum of 30 is scored and marked insufficient sample, with no approach and no threshold proposed. The target, the minimum and the tie order sit on the policy row.

### Step 8

**In the story.** RW-COE: reads the result through GET /admin/agent-evaluations and exports it; the solution architect records the choice as a proposed architecture decision after ADR-009.

Two people act here and neither part is automated. The analyst reads the scores and the proposal through GET /admin/agent-evaluations, which needs Rules and parameters R, and exports the proposal rows by asking for text/csv. The solution architect then writes the architecture decision after ADR-009, which happens outside the code and is out of scope for this story. Nothing the evaluation produced changes how documents are handled today: a proposed threshold takes effect only when P5 loads it as a new reference data version. Your work ends at the CSV export, which is part of build step 5.

## RWB-E1-061 Intake agent evaluation and L1 proposal [E2a]

Module: P10 Agent runtime

### Step 1

**In the story.** RW-COE: requests the report for the evaluation run through GET /admin/agent-evaluations/{evaluationId}/report.

A person starts this. The center of excellence analyst calls GET /api/recovery/v1/admin/agent-evaluations/{evaluationId}/report for the evaluation run that RWB-E1-059 finished, and sets Accept to application/json, text/csv or application/pdf for the format wanted. You add the endpoint to AgentEvaluationController. The right needed is R in Rules and parameters, which RW-COE, RW-RISK and RW-AUDIT hold; a case owner is refused with 403 and MSG-P4-002, which is test TC-E1-061-08. The call is read only, and the same run always gives the same report. A run that has not finished is refused with 409 and MSG-P10-008.

### Step 2

**In the story.** System: builds the report from the stored runs and scores: sample size, agreement rate per gap type, failure counts by type, total and per-case cost, median and 95th percentile latency, policy, prompt and model versions.

The Workbench builds this with no person involved, in EvaluationReportService. Read the stored rows of agent_evaluation_run, agent_evaluation and agent_run, and put together the sample size, the agreement rate for each gap type, the count of each failure type, the total cost and the cost per case, the median and 95th percentile latency, and the policy, prompt and model versions. Cost per case is the total cost divided by the number of runs to four decimal places, so 412.6000 baht over 200 runs gives 2.0630. Latency percentiles count every run, with a timed out run counted at 60,000 ms. The report holds counts and rates only, and no personal field. Build it over a fixture of 200 runs.

### Step 3

**In the story.** RW-COE: exports the report as CSV and PDF for the steering committee pack.

The analyst does this, and you build what makes it possible. EvaluationReportExporter writes both the CSV and the PDF from the same report object that step 2 built, so the three formats cannot disagree with one another. The format is chosen by the Accept header on the report endpoint, with no second endpoint. The analyst then puts the export into the pack for the steering committee, which is work outside the Workbench; the committee meeting and its minutes are out of scope. Keep the export clear of personal fields, as the report itself is.

### Step 4

**In the story.** RW-COE: loads policy "INTAKE" version "P2" with autonomy mode L1, the evaluation run ID, the conditions, the fallback and the measures to watch through POST /admin/agent-configs.

The analyst does this. RW-COE posts the new policy version to POST /api/recovery/v1/admin/agent-configs with kind POLICY and agent INTAKE, carrying autonomy mode L1, the ID of the evaluation run it rests on, the conditions, the fallback and the measures to watch. The endpoint comes from RWB-E1-058; this story adds the L1 checks behind it. The right needed is C in Rules and parameters. The four new values are stored on agent_policy by migration V10_004__policy_promotion.sql, which adds evaluation_run_id as uuid, promotion_conditions and watch_measures as jsonb, and fallback_rule as varchar(20). The fallback of an L1 agent is the rule result.

### Step 5

**In the story.** System: checks that the evaluation run is DONE, that its scores meet every stated condition and that the fallback and measures are present; stores the version as LOADED.

The Workbench checks the proposal with no person involved, in PromotionProposalValidator, which you add inside AgentConfigService and run only for mode L1. Three checks apply. The named evaluation run has to have status DONE. Its sample size has to be at least 200, the minimum held in the policy JSON schema version the loader uses. Every condition stated in the proposal is compared with the scores of that run, and a score below a stated condition refuses the load while naming the gap type and the value. The conditions, the fallback and the measures to watch all have to be present. A failed check refuses the whole file with 422 and MSG-P10-001 and leaves the version in force unchanged. A file that passes is stored with status LOADED.

### Step 6

**In the story.** RW-RISK: approves version "P2" with a valid from date through POST /admin/agent-configs/{versionId}/approve after the committee agrees.

A second person does this. The risk and model risk officer, holding the right A in Rules and parameters, calls POST /api/recovery/v1/admin/agent-configs/{versionId}/approve with a valid from date once the steering committee has agreed. Reuse the approval check from RWB-E1-058 and test it for an L1 version. The person who loaded the version may never approve it, which returns 409 with MSG-P7-002. Until this approval succeeds and the valid from date arrives, version P1 in SHADOW mode stays in force, so no agent output reaches case owners on the strength of the proposal alone.

## RWB-E1-062 Deviation screening agent in shadow [E2b]

Module: P10 Agent runtime

### Step 1

**In the story.** SY-CASEWF or P5: writes EV-01 CaseCreated for a new case, or EV-16 DocumentStored for a document on an open case.

Two other modules produce these events, and your code creates neither. The case workflow module writes EV-01 CaseCreated when a case is opened, and the document hub writes EV-16 DocumentStored when a document is stored on an open case, carrying the document ID, the case ID, the type and the source. This story only consumes them, so nothing changes in the modules that publish them. Both events are delivered at least once and each carries an event ID, which is what makes the idempotency check in the next step possible. Your work starts at the consumer; treat these two events as the only two ways a screening run begins.

### Step 2

**In the story.** System (ScreeningShadowListener): calls the orchestrator for agent "SCREENING" with key "SCREENING:<caseId>:<eventId>".

Your listener does this automatically. Write ScreeningShadowListener to consume both events and call the agent orchestrator for agent SCREENING, passing a run key built from SCREENING, the case ID and the event ID joined by colons. The key makes the call idempotent, which means the same event arriving twice has the same effect as arriving once: the second delivery finds the existing run, no second model call is made, and the repeat is counted under rule R-UNI-40. The case ID on its own would not do, because one case has one run per triggering event. With the flag rwb.agent.screening-shadow off, both listeners ignore their events.

### Step 3

**In the story.** System: reads the case, the interaction ledger entries, the documents and their fields as SY-AGENT, masks personal fields and calls the model.

Your code assembles the input, with no person involved. Write ScreeningInputAssembler to call P3 CaseQueryService.getCase, P7 InteractionLedgerReader.list for the ledger window of 180 days held in the policy, and P5 DocumentQueryService.listByCase and getFields. Every call runs as the system identity SY-AGENT, which holds Case record R and Documents R, so the agent reads no more than those rights allow. Mask the personal fields before the text leaves, which here means the interaction summaries and the document field values. The model call then goes out under the approved policy SCREENING P1 with the approved prompt PR1 and a 60 second timeout. Prompts and responses are never written to logs.

### Step 4

**In the story.** System: checks the answer: each proposal has a code in X1 to X7, reasons, source references and a confidence.

A guardrail in your code tests the model's answer before anything is stored. The output schema screening-v1 says each proposal holds a code in the range X1 to X7, an array of reasons, source references pointing at interaction or document IDs, a confidence, and, for an X1 proposal, the ID of the preceding contact. Build ScreeningRuleChecks to apply the schema and the added rule checks. A code outside the list fails the check named SCHEMA, and the run is stored with status GUARDRAIL_FAILED and fallback true. An X1 proposal that names no preceding contact, while the ledger holds one in the 30 days before, fails the check named SCHEMA_RULE.

### Step 5

**In the story.** System: asks the rules component which owner role each proposed code routes to (R-DEV-02 to R-DEV-06) and stores it with the proposal.

Your code asks another component, and nobody decides by hand. Write ScreeningOwnerResolver to call P3 RuleEvaluator.ownerFor with the route set Deviations, the event OWNER_ASSIGNED and the proposed deviation code, running as SY-RULES. The answer is the owner role held in rule rows R-DEV-02 to R-DEV-06, which the center of excellence maintains as data, so an owner change is a rule row change and not a code change. Store the role with the proposal, so the evaluation can show who each proposal would have gone to. A proposed code with no rule row takes owner role RW-TEAMMGR and is marked unmapped, since five rows cover seven codes.

### Step 6

**In the story.** System: marks proposals below the confidence floor as "review"; stores everything on the agent run in mode SHADOW. No deviation record, contact stop or clock change is made.

Your code writes the run and stops there. Compare each proposal's confidence with the floor of 0.80 held in the agent policy and mark the ones below it with the marker review. Write one agent_run row holding the agent code and version, the prompt and model versions, the case ID, the autonomy mode SHADOW, the trigger event, the idempotency key, the status, the fallback flag, the guardrail result, the output, the confidence, the latency, the token counts and the cost. Shadow mode means stored and acted on by nobody: write no deviation row, leave deviation_open false, set no contact stop, pause no clock, and never call the S8 deviation service.

### Step 7

**In the story.** RW-COE: starts the evaluation of "SCREENING" on sample "SCREEN-S1".

A person starts this, the center of excellence analyst, who holds Rules and parameters C. They call POST /api/recovery/v1/admin/agent-evaluations naming agent SCREENING and sample SCREEN-S1, which is the business analysts' review of 200 Epic 1 cases, one row per case and code with an expected value of Y or N. Your code creates an agent_evaluation_run row with status RUNNING. Refuse a sample with no labeled rows with 422 and MSG-P10-002, and a second evaluation of the same agent and sample while one is running with 409 and MSG-P10-003. A role without the right is refused with 403 and MSG-P4-002.

### Step 8

**In the story.** System: compares proposals at or above the floor with the labels and stores precision and recall per deviation code, with the count of review proposals.

Your scorer runs on its own once the evaluation starts. Write ScreeningScorer to compare the proposals at or above the confidence floor with the Y and N labels in the sample, code by code. Proposals marked review are left out of that comparison and counted on their own in review_count, a column this story adds to agent_evaluation_run in the migration V10_005__evaluation_review_count.sql. For each code X1 to X7, write one agent_evaluation row holding the sample size, the true positive, false positive and false negative counts, and precision and recall computed from them. Precision is the share of proposals that were right; recall is the share of labeled deviations the agent found.

## RWB-E1-063 Agent monitoring dashboard v1 [E2c]

Module: P10 Agent runtime

### Step 1

**In the story.** JOB-15 Reporting extract: at 01:30 calls the P10 step AgentRunExtractStep for the previous business date.

JOB-15 starts on its own from its Quartz schedule at 01:30 Asia/Bangkok, with no person involved. The job already exists, so your work is one new step added after the ones already there: build AgentRunExtractStep as a Spring Batch step that the job calls for the previous business date. Keep it behind the feature flag rwb.agent.monitor, so that with the flag off JOB-15 runs its other steps and skips this one. The platform administrator can also start a run by hand with POST /admin/jobs/{jobId}/rerun under Platform administration U. The step reads its input through the P10 published interface AgentRunExtractSource rather than from another module tables.

### Step 2

**In the story.** System: groups the agent runs of that date by agent, policy version, prompt version and model version: runs, answered, fallback, median and 95th percentile latency, tokens and cost.

The step does this with no person involved. Build AgentMonitorService to read the agent_run rows whose run_at falls on the business date and group them by agent code, policy version, prompt version and model version. For each group work out the number of runs, how many were answered, how many used a fallback, the median and 95th percentile of latency_ms, the tokens from tokens_in and tokens_out, and the cost from cost_thb. The fallback rate is the runs with a fallback divided by the runs, to four decimals, so AC1 reads 0.0750 for 120 runs with 9 fallbacks. Add an index on agent_run (run_at) so the grouping reads one date. Test the aggregates on the fixture of 270 runs that AC1 and AC5 describe.

### Step 3

**In the story.** System: adds the latest DONE evaluation score per agent and version.

The step does this on its own, in the same pass as the grouping. Read agent_evaluation for each agent and version and take the latest row whose status is DONE, so an evaluation still in progress is left out. Put its score on the group row in the eval_score column of the output table listed in section 12. The evaluation fields the story names are label_key, agreement_rate, precision_value and recall_value. An agent and version with no DONE evaluation leaves the column with no value, which the report then shows as having no score. The dashboard needs this joined here, because the report reads only the data lake table and never the live agent tables.

### Step 4

**In the story.** System: writes the rows to the data lake table agent_run_daily and checks that the row count and the sum of runs match the source.

The step writes and checks with no person involved. Write one row per group into the data lake table agent_run_daily, with the columns named in section 12. The write replaces the date: delete the rows already held for that business date in the same transaction as the new insert, so a rerun leaves the same rows and no duplicates. A transaction is a group of changes that either all take effect or none do. Then compare the number of rows written and the sum of runs with the source figures, with zero tolerance. When they differ, as AC3 shows with one row written for two groups, hold the publish, leave the previous day visible with the MSG-P1-001 banner, report the step failed in GET /admin/jobs and alert the data steward and the platform administrator.

### Step 5

**In the story.** System: compares each agent's cost for the date with daily_cost_cap_thb of its policy; for each breach writes one agent alert and sends MSG-P10-004 through the P6 notification interface to the alert role and to RW-RISK.

The step does this itself. Build CostAlertService and read both the cap and the alert role from agent_policy, where RW-COE loads them and RW-RISK approves them, so no cap sits in code. The test is strictly greater than: a cost equal to the cap raises nothing, which AC6 checks at 2,000.0000 baht. Create agent_alert with the migration V10_006__agent_alert.sql, the standard record columns and a unique key on agent code, alert type, segment and business date, so one alert exists per agent, type and date and a rerun writes no second one. The row holds alert type COST_CAP, the business date, the measured value, the threshold, the role sent to and the sent time. Send MSG-P10-004 through the P6 notification interface to the policy alert role and to RW-RISK; when that path is down, leave the sent time empty and let the outbox sender retry.

### Step 6

**In the story.** RW-RISK: opens the Power BI report "Agent monitor v1" and reads each agent by version and date.

A person does this: the risk and model risk officer, who holds Reporting R, and RW-COE reads the same report. The report is built and maintained by the reporting and BI analyst on the data lake table agent_run_daily, one page per agent with version filters, so no Workbench screen comes from this story; the agent monitor screen SCR-46 arrives in RWB-E2-031. The report has two states: loaded with the figures of the latest published date, and stale with the MSG-P1-001 banner naming the date shown, which is what a held publish looks like to the reader. A role without Reporting R is refused by the workspace with MSG-P4-002. Your part is finished when the page shows the fixture figures for 2026-12-01.

## RWB-E1-064 Data dictionary for the 14 data products

Module: P1 Recovery data engine

### Step 1

**In the story.** Reference data administrator: loads the dictionary attributes (owner role, refresh cycle, behavior when late, interface) for all 1,256 fields through POST /admin/reference-loads with table sys_fields.

A person starts this. The reference data administrator, RW-REFADM with Reference data C, submits one file covering every field through POST /api/recovery/v1/admin/reference-loads with table sys_fields, and it is approved through POST /api/recovery/v1/admin/reference-loads/{loadId}/approve with Reference data A. The data steward prepares the file from s2t.txt and the Logical Data Model. The attributes in it land in the new sys_fields columns owner_role, refresh_cycle, late_behavior and interface_id, which the Flyway migration of this story adds. The rows themselves already exist: RWB-E1-001 seeded 108 entities in sys_objects and 1,256 fields in sys_fields, so this load fills attributes rather than creating fields.

### Step 2

**In the story.** DataDictionaryLoader: refuses the whole load if any field lacks an attribute; otherwise writes the attributes and version 1 of each field to sys_field_version.

The loader does this on its own. Build the published interface DataDictionaryLoader with apply taking the load version, a valid from date and the rows. Validate the whole file before writing anything: one field missing one attribute refuses the load in full with MSG-P1-002 and the first failing check, and the dictionary in force is left as it was. AC6 shows the form of that check, refresh_cycle missing for DF-COL-005. On success, write the attributes and one sys_field_version row per field holding the definition as jsonb with its version number, change reason, changed_at and changed_by. The migration seeds version 1 for all 1,256 fields.

### Step 3

**In the story.** DataDictionaryLoader: creates or updates one data_contract per source system in status DRAFT, naming its interfaces, listing its mapped fields.

DataContractService does this as part of the same load, with no person involved. Group the fields by sys_fields.interface_id to build one data_contract row per source system, holding contract_code, source_system, interface_id, contract_version, status DRAFT and the count of mapped fields. The Flyway migration creates data_contract with a status check of DRAFT, PUBLISHED or SUPERSEDED and unique contract_code with contract_version. A data contract is the written agreement with the system that sends the data. The background of section 7 shows the shape: DC-ALS for Core bank (ALS) covering INT-01 and INT-02, DRAFT with 32 mapped fields.

### Step 4

**In the story.** Developer or analyst: calls GET /admin/data-dictionary/fields and reads a field's type, source system, source field, refresh, owner and behavior when late.

A developer or an analyst reads this. Build DataDictionaryController with GET /admin/data-dictionary/fields taking product, entity, field, sourceSystem, page and size, returning DataDictionaryFieldPage of DataDictionaryField with fieldId, entity, fieldName, dataType, physicalType, mandatory, listCode, sourceSystem, sourceField, refreshCycle, ownerRole, lateBehavior, interfaceId, isPersonal, version and versionDate. Authorization is Reference data R. AC1 reads loan_account.days_past_due and expects DF-ACC-014 to show type NUMBER, physical type integer, source field DELAY_DAYS and late behavior of keeping the previous value and marking DP01 stale. Other modules read the same values through DataDictionaryQuery rather than this endpoint.

### Step 5

**In the story.** Data steward: sends the contract to the system owner outside the Workbench and records the owner's confirmation with PATCH /admin/data-contracts/{contractId}: confirming role, date and the stored confirmation document.

A person does both halves of this, and the first half happens outside the system: the data steward sends the contract to the system owner by their own means. The steward, RW-DATASTEW with Reference data U, then records confirmedByRole, confirmedOn and confirmationDocumentId with PATCH /admin/data-contracts/{contractId}. Build the PATCH with an If-Match header carrying the version the caller read. That is optimistic locking: the write is accepted only while the row has not changed since that read, and a later version answers 409 with MSG-GEN-004. An empty field answers 422 with MSG-GEN-001. AC2 records the ALS confirmation on 2026-11-12 with document DOC-SYN-0640.

### Step 6

**In the story.** Data steward: publishes the contract with POST /admin/data-contracts/{contractId}/publish; the service refuses a contract without a confirmation.

The data steward makes the call and the check sits in code. Build POST /admin/data-contracts/{contractId}/publish with an Idempotency-Key header, so a repeated call returns the first result. DataContractService refuses a contract that has no recorded confirmation with 409 and MSG-P1-021, which reads that the data contract for the system cannot be published until its system owner confirms it, and the contract stays DRAFT. AC4 tests this with DC-EFS for EFS. Authorization is Reference data U. This refusal is what keeps a load from depending on a source field nobody has agreed to send.

### Step 7

**In the story.** DataContractService: sets the contract PUBLISHED and the mapping status of its fields to Confirmed.

The service does this inside the publish call. Set status PUBLISHED with published_at and published_by on the contract version, and set the mapping status of every field of that source system to Confirmed, which replaces the s2t.txt text reading To confirm with the system owner. AC2 expects DC-ALS at version 1 PUBLISHED with its confirmation date, and the 32 mapped fields of Core bank (ALS) reading Confirmed. A published contract is never edited in place afterward, so this write happens once for each contract version.

### Step 8

**In the story.** Data steward: changes a field definition with PATCH /admin/data-dictionary/fields/{fieldId} and a reason; the service writes a new version with its date and reason.

The data steward makes the change and the versioning happens on its own. Build PATCH /admin/data-dictionary/fields/{fieldCode} in DataDictionaryService with the If-Match header and a reason that cannot be empty: an empty reason answers 422 with MSG-GEN-001 and leaves the field at its current version, which AC5 tests on DF-ACC-015. Each accepted change writes a new sys_field_version row, unique on field_id and field_version, with change_reason, changed_at and changed_by, and raises the version on sys_fields. Earlier versions stay readable with their own dates. AC3 changes DF-ACC-014 to source field DPD_DAYS and expects version 2 dated 2026-11-18.

### Step 9

**In the story.** DataContractService: when a changed field belongs to a published contract, opens a new DRAFT contract version; the published version stays in force until the new one is confirmed and published.

The service does this on the back of the field change, with no second call from anyone. Look up the contract holding the changed field; when its status is PUBLISHED, write a new row for the same contract_code with contract_version raised by one and status DRAFT. The published version keeps serving until the new one is confirmed and published in its turn. AC8 changes DF-ACC-014 while DC-ALS version 1 is PUBLISHED and expects version 2 as DRAFT with version 1 still in force. Section 12 gives no endpoint for this, so build it inside the field change path.

## RWB-E1-065 Sandbox database with synthetic recovery data

Module: P1 Recovery data engine

### Step 1

**In the story.** Pipeline: on a merge to main that changes a recovery Flyway migration, or on a manual start, runs the sandbox build stage in DEV.

The pipeline runs this, and a person only starts it by hand when they choose to. Add a DEV stage that fires on a merge to main touching any file under the recovery Flyway migration folder, and that a Tribe member or the platform administrator can also start manually. Flyway migrations are the versioned SQL files that build the schema, so a change to one is what makes the sandbox out of date. The stage is not a scheduled job and does not belong in the production job list. The pipeline holds a PostgreSQL advisory lock for the whole build, so a second build waits for the first to end, as AC9 asks.

### Step 2

**In the story.** Pipeline: drops and recreates schema `recovery` in `rwb_sandbox` and applies every Flyway migration.

Automatic. The stage builds the schema from the same migration files every other environment uses, so the sandbox cannot drift from the real schema. Point Flyway at the database rwb_sandbox and let it apply every recovery migration in order. That also creates sys_objects, sys_fields and the seed lists of values the generator reads in the next step, and it means no table is ever hand-built for the sandbox. A build that fails here leaves the previous sandbox in use, so the squads keep working while you fix the migration.

### Step 3

**In the story.** SandboxGenerator: reads sys_objects, sys_fields and lov_value from the sandbox to learn every table, column, type and list.

Automatic. Build SandboxGenerator in tools/sandbox-generator, as its own build module that is never packaged into the ACE service. Before it writes anything it reads sys_objects for the tables, sys_fields for each column with its data type and personal flag, and lov_value for the allowed values of each list column, and works out the order to fill the tables from the relationships between them. Reading the dictionary this way is what lets a new column appear in the sandbox with no generator change, which AC3 checks by adding recovery_case.risk_tier. A column with no sys_fields row fails the build and names the table and column.

### Step 4

**In the story.** SandboxGenerator: creates synthetic cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), with their accounts, parties, contact points, collateral, valuations, payments and interactions.

Automatic. The generator writes 2,812 cases across the three product groups and the rows that hang off them in loan_account, party, contact_point, collateral, account_collateral, valuation, account_payment and interaction. A foreign key is the column that points at another table's row, and the generator fills tables in an order that lets every foreign key point at a row that exists, so a case has real accounts and parties to read. Every count comes from properties, among them rwb.sandbox.seed of 20261128 and the three case counts, so the same seed and commit give the same rows and the same totals, as AC5 checks.

### Step 5

**In the story.** SandboxGenerator: adds 10 cases for each exception shape in section 8, BR4.

Automatic. Build ExceptionShapeBuilder to add ten cases for each shape BR4 lists: a duplicate case for one customer and product, a deceased customer, a bankruptcy, an open deviation, a legal hold, an unmapped product code, collateral with no account, a case with three accounts, accounts at 89 and at 90 days past due, and withdrawn consent. These are the shapes the rules have to handle, so a squad can test them from the first day without asking another team for data. The count is the property rwb.sandbox.shape-count. AC8 expects ten accounts at 89 days past due with no case and ten at 90 days past due with one open case each.

### Step 6

**In the story.** SandboxGenerator: loads the 54 roles, the permission matrix and one named test user per role.

Automatic. Build AccessSeedLoader to read the roles and permissions seed file and write the 54 roles, the role to permission rows and one named test user for each role. Every role gets a test user before it has real users, so a developer can call the DEV service as any role and see what that role may do. Those users are what the access tests use, among them the test user with RW-REFADM calling GET /cases and being refused with MSG-P4-002. Keep the rows in the seed file, so a permission change reaches the sandbox with no code change.

### Step 7

**In the story.** SandboxVerifier: checks every table has rows, every LOV column holds list values, every foreign key resolves and no value matches a personal data pattern.

Automatic, and it decides whether the build is published. Write SandboxVerifier with four checks: each table holds at least one row, each list column holds only values from its list in lov_value, each foreign key points at a row that exists, and no value matches a personal data pattern. The pattern check covers a 13 digit national ID with a valid check digit, a mobile number and an email address. Any failure fails the build with the table and column named, and the previous sandbox stays in use, which AC4, AC6 and AC7 expect. Nothing is published from a failed build.

### Step 8

**In the story.** Pipeline: grants SELECT on schema `recovery` to role `rwb_sandbox_read` and publishes the build result with the row count per table.

Automatic. Once the verifier has passed, the stage grants SELECT on the schema to the database role rwb_sandbox_read, which maps to the Entra ID group RWB-DEV-RW-TRIBE. SELECT on its own means a Tribe member can read and export rows and cannot change them, which is why AC2 expects an UPDATE by that role to be refused. The stage then publishes the build result with the row count of each table and the verifier outcome, so anyone can see what the current sandbox holds without querying it first.

### Step 9

**In the story.** Developer or analyst: queries the sandbox with SQL or the export script, or calls the DEV service, without a request to another team.

A person does this, and the point of the story is that they need no one else's help. A Tribe lead or squad member in the group runs SQL against the schema, writes a table to CSV with SandboxExport, or signs in to the DEV service as a test user and calls the normal endpoints, GET /cases among them. Build SandboxExport for the read-only role. The DEV profile points the service at rwb_sandbox under the feature flag rwb.dataengine.sandbox. The access rules still apply to those calls: a test user outside the case scope gets MSG-P4-003, and one without the right gets MSG-P4-002.

## RWB-E1-066 Interaction ledger store and writer

Module: P1 Recovery data engine

### Step 1

**In the story.** Case owner: records a call with POST /cases/{caseId}/interactions (channel CALL, direction OUTBOUND, result RIGHT_PARTY, summary, promise amount and date).

A person records the call. POST /api/recovery/v1/cases/{caseId}/interactions is the existing P3 endpoint API-P3-015, so you change its handler rather than add a route. The case owner sends the channel CALL, the direction OUTBOUND, the contact result RIGHT_PARTY and a summary, and the example also carries a promise of 25,000.00 baht for 2026-12-15. The caller needs the Case record C right and the case in scope. Epic 1 has no screen for this; the case record view SCR-03 shows the entries later through RWB-E1-068. A successful call answers 201 with the stored Interaction.

### Step 2

**In the story.** P3 interactions handler: checks Case record C and the case scope, opens a transaction and calls InteractionLedgerWriter.append().

The handler runs the access checks first and then opens the unit of work the whole step depends on. Check the Case record C right and the case scope: a missing right answers 403 with MSG-P4-002, and a case that does not exist or sits outside the scope answers 404 with MSG-P4-003. Then open a database transaction, which is one unit of work that either commits in full or leaves the database unchanged, and call InteractionLedgerWriter.append inside it. The writer is marked Propagation.MANDATORY, meaning it refuses to run unless a caller has already opened such a transaction. The entry and the action it records therefore commit together.

### Step 3

**In the story.** InteractionLedgerWriter: validates the command (case, event code in LOV-LEDGER-EVENT, occurred time, actor, source, idempotency key).

Validation is the first thing inside the writer, before any lock or insert. Check that the case ID is present, that the event code is a value of the list LOV-LEDGER-EVENT, which holds CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN and CORRECTION, and that the occurred time, the actor type, the actor reference, the source system and the source reference are all there. A missing value answers 422 with MSG-GEN-001 naming the field and writes nothing, as in the test where append is called with no event code. The reference data administrator loads that list.

### Step 4

**In the story.** InteractionLedgerWriter: takes a transaction-level advisory lock on the case ID and assigns case_seq as the case's highest case_seq plus 1.

The writer assigns the position in the case history itself. Take a transaction-level advisory lock on the case ID with pg_advisory_xact_lock: an advisory lock is a lock on a number of your choosing rather than on a row, and a transaction-level one is released when the transaction ends. While it is held, no other transaction can be assigning a sequence number for the same case. Read the highest case_seq for that case and add 1. The unique key over case_id and case_seq catches any clash, so retry once on a unique key violation. Two appends at the same moment therefore take 7 and 8, with no gap.

### Step 5

**In the story.** InteractionLedgerWriter: inserts the entry with event code, actor type and reference, source system and source reference, channel and direction where they apply, and the decision log entry ID for a decision.

The insert happens in code with no person involved. Write one interaction row carrying the event code, the actor type and actor reference, the source system and source reference, and the case_seq from step 4. Channel and direction go in where the event has them; a Workbench event such as CASE_CREATED has neither, which is why the migration drops NOT NULL on those two columns. For a decision, put the decision log entry ID in decision_log_id and leave the rule, the version and the inputs to the decision log itself. A correction carries corrects_entry_id naming the entry it corrects, since no entry is ever edited.

### Step 6

**In the story.** P3 handler: commits the action and the entry in one transaction and returns 201 with the Interaction.

The handler finishes the work it opened in step 2. Commit once: the action the user asked for and the ledger entry both sit in the transaction opened before the writer was called, so either both are saved or neither is. Then answer 201 with the Interaction object holding id, caseId, partyId, occurredAt, channel, direction, actionCode, contactResult, promiseAmount, promiseDate, summary, conductCheck and sourceSystem. The idempotency key is built from the request ID header, so a repeated request answers with the entry already written rather than a second one. After the commit the case has one more entry and the next case_seq is free.

### Step 7

**In the story.** Other recording paths (EFS history load, ALS payment load, notice dispatch): call append() in their own transactions with source system EFS or WORKBENCH.

These paths are code, not people, and they use the same writer. The EFS history load, the ALS payment load and notice dispatch each call append within their own transactions, setting source system to EFS or WORKBENCH and filling source_ref with the key the sending system used. They pass their own event codes from the same list, so an EFS history row and an officer's call land in one ordered sequence per case. The architecture test in the build steps holds this in place: no class outside recovery.dataengine.ledger may use InteractionRepository, so there is no second way to write an entry. The EFS history load of RWB-E1-004 has to go through append before this story is done.

### Step 8

**In the story.** On a write failure: the transaction rolls back, the caller receives MSG-P1-022, and the writer raises an incident with incident code LEDGER_WRITE_FAILED, the case ID and the cause.

This path runs on its own when the insert fails. Translate the database error into LedgerWriteException so the transaction rolls back; the user action is undone with it, which is the point, since no contact may be saved without its ledger entry. The API answers 503 with MSG-P1-022, telling the caller the entry was not saved and to try again in a few minutes. Then call IncidentRecorder.raise from RWB-E1-027 with incident code LEDGER_WRITE_FAILED, the case ID and a detail holding the error class. The platform administrator receives that incident. Keep the summary and every other personal value out of the detail and out of the log.

## RWB-E1-067 Every Workbench action into the interaction ledger

Module: P1 Recovery data engine

### Step 1

**In the story.** Publishing module: commits its change and writes the event to the outbox in the same transaction.

This is not your code. Each publishing module, for example the case creation story RWB-E1-018, commits its own change and writes the event row to the outbox inside the same transaction. The outbox is a table in the same database as the change, and writing both together means an event exists only for a change that was kept, and a change is never kept without its event. Your story depends on six of these events: EV-01 CaseCreated, EV-02 CaseAllocated, EV-04 CaseTransferred, EV-08 DecisionRecorded, EV-16 DocumentStored and EV-19 TimerBreached. The event header carries the event ID, the idempotency key, the schema version, the time it happened and the actor.

### Step 2

**In the story.** Outbox: delivers the event to LedgerEventListener, in order per case.

The outbox delivers each event to your listener after the publishing transaction commits. LedgerEventListener is the consumer you build, subscribed to the six events; it runs inside the service and not as a scheduled job. Delivery is at least once, so the same event can arrive more than once, and step 7 handles that. Delivery for one case keeps the order in which the events were written, which RWB-TE-006 provides, so the ledger entries of a case follow that order in case_seq: CASE_CREATED at 1 and CASE_ALLOCATED at 2 (AC6). An event not yet processed is delivered again after a restart.

### Step 3

**In the story.** LedgerEventListener: checks the schema version is the current or the previous version for the event.

The listener checks the schema version in the event header before it does anything else. A schema version is the number of the event payload layout, and a consumer accepts the current one and the one before it (BR6). When CaseTransferred is at schema version 2 and accepts version 1, an event at version 3 is not written: it goes to the exception queue with owner RW-PLATADM and a reason naming the version, and nothing reaches the ledger (AC4). Build step 3 covers the listener with this check, and test TC-E1-067-04 sends a CaseTransferred event at schema version 3.

### Step 4

**In the story.** LedgerEventMapper: maps the event to a LedgerEntryCommand: EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED, EV-19 to CASE_ESCALATED, EV-16 to DOCUMENT_ATTACHED, EV-08 to DECISION_TAKEN with the decision log entry ID.

LedgerEventMapper turns one event into one LedgerEntryCommand, which is the input the ledger writer takes. The pairing is EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED, EV-19 to CASE_ESCALATED, EV-16 to DOCUMENT_ATTACHED and EV-08 to DECISION_TAKEN. Read it from configuration, the property rwb.dataengine.ledger.event-map, so the map is data and not a switch in Java. For EV-08 the command also carries the decision log entry ID into decision_log_id. Everything the entry needs comes from the event payload, so the mapper queries no assignment, document or decision table.

### Step 5

**In the story.** LedgerEventMapper: sets actor from the event header (user ID or service identity), source system WORKBENCH, source reference as the owning module and event ID, and the event's idempotency key.

The mapper fills the fields that say where the entry came from. actor_type and actor_ref come from the event header and hold either a user ID, for example u-teammgr-03, or a service identity, for example SY-RULES. The source system is always WORKBENCH. source_ref is built as the owning module followed by the event ID and name, which gives P3 case and workflow, EV-02 CaseAllocated for an allocation (AC2). The event idempotency key is copied onto the entry as idempotency_key, which is what step 7 uses. No personal data goes into any of these fields; the events carry codes and references only.

### Step 6

**In the story.** InteractionLedgerWriter: appends the entry with the next case_seq.

InteractionLedgerWriter.append writes the entry, and it comes from RWB-E1-066 rather than from this story. It appends the row and sets case_seq, the per case sequence number that gives the case history its order. The writer checks that the calling identity holds Case record C and throws AccessDeniedException otherwise, mapped to MSG-P4-002, so the listener has to run as SY-CASEWF. Build step 5 adds that identity check. SY-AGENT holds read only and is refused, which is access test TC-E1-067-09. An event naming a case that does not exist writes no entry and goes to the exception queue (AC8).

### Step 7

**In the story.** LedgerDuplicateService: when the idempotency key already exists, writes no entry and adds 1 to the hit count for that key (R-UNI-40).

Appending the same event twice has to leave one entry, which is what idempotent means: doing it again changes nothing. The unique constraint on interaction.idempotency_key makes the second insert fail, and LedgerDuplicateService catches that clash and upserts a processed_event row instead, adding one to hit_count and setting last_hit_at. Run that upsert in a new transaction, because the failed insert is rolling its own transaction back and the hit has to survive it. processed_event is a new table in this story, keyed on idempotency_key with first_interaction_id, hit_count and last_hit_at. The same event on two consumer threads at once gives one entry and one hit (AC7).

### Step 8

**In the story.** Outbox: marks the event processed for the ledger consumer.

The outbox marks the event processed for the ledger consumer, which stops it being delivered again. Mark it only once the entry has been written, the repeat counted, or the event moved to the exception queue. A guardrail in section 17 states this: the listener never acknowledges an event it has not written or moved. An event left unmarked is delivered again after a restart, and the duplicate rule of step 7 keeps that harmless. Each consumer has its own processed marker, so marking an event for the ledger leaves other consumers of the same event untouched.

### Step 9

**In the story.** On failure: the outbox retries; after three retries the event goes to the exception queue with owner RW-PLATADM and incident LEDGER_WRITE_FAILED is raised.

When the ledger write fails the event is kept. The outbox retries it with the retry limit of 3 from the outbox settings, so an event is delivered four times in all before it stops (AC5). After that it goes to the exception queue with owner RW-PLATADM, and the system raises the incident LEDGER_WRITE_FAILED for the case, carrying MSG-P1-022. The platform administrator sees these events on SCR-09 Exception queue. Build step 6 covers the path, and test TC-E1-067-05 forces every ledger insert to fail.

## RWB-E1-068 Interaction ledger read interface

Module: P1 Recovery data engine

### Step 1

**In the story.** Case owner: opens SCR-03 Case record; the history panel calls GET /cases/{caseId}/interactions?page=0&size=50.

A person opens the screen, and the panel calls on its own. Build CaseHistoryPanel as a React component on SCR-03 Case record. On load it calls GET /cases/{caseId}/interactions with page 0 and size 50, which is the default page size from the property rwb.dataengine.ledger.page-size-default. The panel needs three states beyond the list: Loading with skeleton rows, Empty with a sentence saying no interaction is recorded on the case, and Error showing the message from section 14 above the panel. SCR-03 is read only in Epic 1, so the panel reads and offers nothing to change. The full timeline screen SCR-04 is Epic 2 work.

### Step 2

**In the story.** P3 interactions handler (API-P3-014): checks Case record R and calls InteractionLedgerReader.read() with the caller's context.

This is automatic, and it is a change to an endpoint that already exists. InteractionsHandler in P3 keeps the access check it has: without Case record right R the call is refused with 403 and MSG-P4-002. What you add is the actor query parameter and the delegation. The handler builds a LedgerFilter from channel, actor, from and to, then calls InteractionLedgerReader.read with it, the page, the size and the caller's UserContext. The handler queries nothing itself. Passing the caller's context down is what lets the reader apply scope and masking for the right user, rather than the handler deciding either of them.

### Step 3

**In the story.** InteractionLedgerReader: checks the case is in the caller's scope through CaseScopeQuery.

The reader does this first, before it touches the ledger. Build LedgerReadService behind the published interface and have it call CaseScopeQuery, the P3 interface from RWB-E1-016, to ask whether this caller may see this case. Scope is the set of cases a role may reach: Own for a case owner, Team for a team manager. A case outside it answers 404 with MSG-P4-003, not 403, so the response does not tell the caller that a case they may not see exists. The interface throws CaseNotInScopeException, which the handler maps to that 404. Make the scope check before the query, never by filtering rows afterwards.

### Step 4

**In the story.** InteractionLedgerReader: validates the filter (channel in LOV-CHANNEL, from not after to, size 1 to 200).

Still inside the reader, with no call back to the browser. Three checks on the LedgerFilter: the channel must be a value of LOV-CHANNEL, the from date must not fall after the to date, and the page size must lie between 1 and 200, the maximum held in the property rwb.dataengine.ledger.page-size-max. Each failure answers 422 and changes nothing: MSG-GEN-003 for the dates, naming "to" and "from"; MSG-GEN-002 for the size, naming the minimum and the maximum; MSG-GEN-001 for a malformed channel or date. Size 200 passes and size 201 is refused, so the size check refuses only a value above 200.

### Step 5

**In the story.** InteractionLedgerReader: reads the case's entries matching the filter, ordered by occurred_at, then case_seq.

Automatic. Build the query in InteractionRepository: the interaction rows for the case, narrowed by channel, actor_ref and an occurred_at range when the filter holds them, ordered by occurred_at and then case_seq, earliest first. The second column is the tie-break, so two entries recorded at the same moment always come back in the same order and paging cannot repeat or skip a row. The existing index ix_interaction_case_time serves the case and time part; add an index on (case_id, actor_ref) in a Flyway migration for the actor filter. One read of a case with 5,000 entries has to finish inside two seconds.

### Step 6

**In the story.** InteractionLedgerReader: masks the summary field (is_personal) through the P4 masking interface for the caller's roles.

The reader does this to every row before it answers. Call the P4 masking interface from RWB-E1-037 with the caller's roles for the summary field, which is the one field marked is_personal. When no masking rule allows the caller to see it, the value comes back as "MASKED". Compliance owns those rules and they may be empty, in which case every personal field is masked, so write the code to mask by default rather than to allow by default. The channel, the result, the promise amount and the promise date are returned in full. Masking belongs here so that every consumer of the ledger gets the same treatment.

### Step 7

**In the story.** InteractionLedgerReader: writes the read to the PII access log when a personal field is returned unmasked.

Automatic, and only on the condition named. When a personal field leaves the reader unmasked, write the read to the PII access log; when every personal field was masked, write nothing. Put the write in LedgerReadService after the masking step, so the decision rests on what actually went out. The entry is what lets Compliance show later who read which personal content. Never put the summary text into that entry or into any log: the guardrails say summaries are never logged, and test data uses synthetic text instead.

### Step 8

**In the story.** P3 handler: returns InteractionPage with each entry's event, time, actor, channel, outcome, promise and source.

The handler maps the reader's LedgerPage to the API response with no further logic. InteractionPage holds the items, the page, the size and the total, where total is the count of all matching entries. The Interaction type gains six fields in this story: eventCode, caseSeq, actorType, actorRef, sourceRef and decisionLogEntryId. Source matters to the person reading the screen, because each entry has to name the system it came from and its reference, for example "EFS, INT-07" or "WORKBENCH, P3 case and workflow", so a case owner can tell a call loaded from EFS from an entry made in the Workbench. An empty page answers 200 with 0 items and total 0.

### Step 9

**In the story.** Case owner: filters by channel, actor or date range; the panel calls the same endpoint with the filter.

A person chooses the filter, and the panel repeats the call it made on load with the chosen values added. There is no second endpoint and no filtering in the browser: the three filters go to the server every time, so scope and masking are applied again on each read. Build the controls on CaseHistoryPanel as a channel picker fed by LOV-CHANNEL, an actor field, a from and to date pair, and paging. Reset to page 0 when a filter changes, because the page numbers of the old result mean nothing against the new one. An architecture test proves that no class outside recovery.dataengine.ledger queries the interaction table.
