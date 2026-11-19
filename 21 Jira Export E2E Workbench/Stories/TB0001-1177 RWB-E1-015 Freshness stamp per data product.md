# TB0001-1177 [RWB-E1-015] Freshness stamp per data product

| Field | Value |
|---|---|
| Jira | [TB0001-1177](https://scbjira.atlassian.net/browse/TB0001-1177) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:17.063+0700 |
| Updated | 2026-11-18T17:00:45.298+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 4 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want every data product to carry the source extract time and the load time, exposed to every consumer and shown on the case record view, so that every decision input states how old it is and stale facts are visible.

## Acceptance criteria

```gherkin
Feature: Freshness stamp per data product

  Background:
    Given data product "DP01" Account and arrears has refresh cycle "DAILY" and expected-by time 08:00
    Given data product "DP06" Collateral and asset has refresh cycle "WEEKLY" and expected-by time Monday 08:00

  Scenario: AC1 Freshness on the row
    Given the account and arrears product for business date 2026-11-30 loaded at 06:50 on 2026-12-01 from an extract taken at 23:30 on 2026-11-30
    Given loan account "ACC-SYN-000101" has data_as_of 2026-11-30
    When the row is read through FreshnessQuery.stampForRow("DP01", 2026-11-30) and GET /data-products/freshness?product=DP01
    Then the row carries source time 2026-11-30T23:30+07:00 and load time 2026-12-01T06:50+07:00
    Then the status is "LOADED"

  Scenario: AC2 Stale product flagged
    Given no DP01 load for business date 2026-11-30 exists at 08:00 on 2026-12-01
    When the freshness step runs at 08:00
    Then the system flags the product "STALE"
    Then a data quality exception with product "DP01" and check "FRESHNESS" is raised on 2026-12-01
    Then the alert goes to the operations channel
    Then the case record view shows the stamp in the data panel with "Account and arrears is from 2026-11-30. Today's load has not arrived."

  Scenario: AC3 Freshness in the decision log
    Given a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23
    When the entry and its inputs snapshot are read
    Then the snapshot lists DP01 with load time 2026-12-01T06:50+07:00 and status "LOADED"
    Then the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED"

  Scenario: AC4 A refused load marks the product stale at once
    Given the DP01 load for 2026-11-30 is refused at check "Control totals" at 05:20
    When LoadRefused is processed
    Then DP01 is "STALE" from 05:20
    Then the stamp for business date 2026-11-30 stays the one in use

  Scenario: AC5 The same load stamped twice
    Given DP01 for business date 2026-11-30 is stamped at 06:50
    When the same stamp is written again for DP01 and 2026-11-30
    Then one data_product_load row exists for DP01 and 2026-11-30
    Then the duplicate count for that stamp is 1

  Scenario: AC6 A late load clears the stale flag
    Given DP01 was flagged "STALE" at 08:00 on 2026-12-01
    When the DP01 load for 2026-11-30 commits at 08:40
    Then DP01 status is "LOADED" with load time 2026-12-01T08:40+07:00
    Then the FRESHNESS exception for DP01 on 2026-12-01 is closed

  Scenario: AC7 A load one minute before the expected-by time
    Given the DP01 load for 2026-11-30 commits at 07:59 on 2026-12-01
    When the freshness step runs at 08:00
    Then the system does not flag DP01 stale

  Scenario: AC8 A weekly product between its loads
    Given the DP06 load for business date 2026-11-30 committed at 04:40 on Monday 2026-11-30
    When the freshness step runs at 08:00 on Thursday 2026-12-03
    Then the system does not flag DP06 stale
```

## Comments (4)

### Comment 1: Ratchadaphorn Kasemphin, 2026-11-16T23:41:12.739+0700, edited 2026-11-17T11:36:15.908+0700

Comment ID 1793581

@CHANISSARA MAHAKITTIKUN 
cc. @Chitchaya Muanchonchana 

After reviewing the card, I have the following concerns and questions that need clarification:

h3. Concerns (Dependencies)

# *RWB-ACE-001 / DL43 (ACE team) is still open and on the critical path.*
#* The {{rwb.dataengine.freshness-stamp}} flag can only be turned on once {{public.ace_batch_run}} and {{v_ace_batch_status}} exist.
#* The plan assumes delivery on 21 Nov, but ACE has not committed a date (DEP-34, DEP-35). The release is 30 Nov.
#* A slip affects every story that depends on RWB-E1-015: RWB-E1-002 (case list), 007, 011, 034, 052 and 056.
# *No fallback is defined for when the flag is off.*
#* The story only says "the panel shows no stamp".
#* It does not say how DailyCompletenessGate behaves. Does JOB-04 run without a gate, or does it HOLD everything?
#* The gate replaces the retired load checks, so with no gate there is no data-completeness check at all.
# *RWB-E1-001:* {{data_product}} (DP01 to DP14) and {{data_product_load}} must exist first.
# *RWB-E1-069:* {{v_ace_batch_status}} is in Section B, which itself depends on DL43.
# *RWB-E1-027:* the P7 decision log writer must call {{stampsFor()}} when it builds the inputs snapshot. Build step 7 changes another story's code.
# *Dependencies that are used but not listed in "Depends on":*
#* RWB-E1-043 loads the product-to-source map.
#* RWB-E1-064 loads {{refresh_cycle}} and {{expected_by}}.
#* The flow cannot run end to end without them.
# *Other open decisions:*
#* DL10: the Thai text for MSG-P1-001 is not approved yet.
#* DL11: the story cites it as the source of the 08:00 and MON 08:00 expected-by times, but DL11 actually covers NFR targets and is still open. Who approved 08:00?

h3. Clarification needed

h4. A. Business

# *Business calendar:* AC2 treats 2026-11-27 (Fri) as the day before 11-30 (Mon), so daily data excludes weekends.
#* Which calendar applies? Does it include Thai bank holidays?
#* Who owns the calendar?
# *Definition of "expected business date":*
#* For daily products it is T-1 (the 12-01 08:00 cut-off expects business date 11-30).
#* There is no clear definition for weekly products (DP06).
# *Batch never arrives that day:*
#* After the gate HOLDs, how often does it retry?
#* Is there a final deadline?
#* Can anyone override it to run on older data, for example with business sign-off?
# *Alert recipients are inconsistent:*
#* Section 10 names the data steward and the platform admin.
#* AC9 and RWB-E1-002 X1 also include the team manager group.
#* Which list is correct?
# *MSG-P1-001:* "Today's ACE batch has not arrived" is used both when the batch is missing and when it FAILED.
#* Should these be separate messages? The user has to do different things in each case.
# *Access:*
#* GET /data/freshness lets every role with Case record R see {{record_count}} and {{feed_version}}, which are operational data. Should case users see them?
#* The data steward holds Platform administration R, but the endpoint requires Case record R. Can the data steward call it?
# *The 99% measure:* how is it measured, who reports it, and is it per source or per day?
# *Snapshot status in the decision log:*
#* When the 11-27 row is later set to STALE, earlier decisions that read 11-27 still show LOADED.
#* Does audit need the status at decision time or the current status?

h4. B. AC details

# *AC3 conflicts with AC8 and AC11 (DP06 weekly):*
#* AC3: business date 11-23, loaded 11-24 (Tue).
#* AC8: business date 11-30, loaded the same day (Mon).
#* AC11: CCMS business date 11-27 (Fri).
#* Please confirm a single business-date pattern for weekly products.
# *AC1 and AC6 conflict with AC9 and BR8 (trigger model):*
#* AC1 and AC6 say one completed ALS batch starts JOB-02/04/07/08 straight away through EV-26.
#* AC9 and BR8 say the gate must first check every source the jobs read.
#* If ALS completes but EFS has not arrived, what happens? Which sources does each job wait for?
# *Gate cut-off time is inconsistent:*
#* AC9 uses 08:00.
#* RWB-E1-002 says JOB-04 runs at 07:15 if JOB-03 has not finished, which is earlier than expected-by.
#* When does the gate run? If it runs at 07:15, will it HOLD on most days?
# *No job-to-product map:*
#* AC9 and AC10 refer to "the sources the day's jobs read", but the story only has a product-to-source map.
#* Where do the productCodes in {{check(businessDate, productCodes)}} come from? Should they be data rows per BR7?
# *Multi-source products vs. the unique key:*
#* The unique key is (product_code, business_date), with a single {{source_system}} column.
#* Which source is stored for DP13 (ALS+GL) and DP06 (4 sources)?
#* Will the second source be wrongly counted in {{duplicate_count}}? That would conflict with AC5 and BR4.
# *AC2 and flow step 5:* STALE is set on the previous row (11-27). When the 11-30 batch arrives (AC6):
#* Is the 11-27 row cleared back to LOADED, or does it stay STALE?
#* Which row does the API's {{staleSince}} come from?
# *AC4:* for "STALE from 05:20" on FAILED, is the time taken from the batch row or from when the system reads it?
#* There is no AC for a FAILED batch that later COMPLETES for the same business date (a rerun).
# *AC1* {{ageDays 1}}:
#* Is it calendar days or business days?
#* Is it measured from today or from {{completed_at}}?
#* On Monday, reading Friday's data, is it 3 or 1?
# *AC1* {{source_extracted_at = started_at}}: the ACE batch start time is not the source-system extraction time. Please confirm what it means before it is shown for audit.
# *AC10:* the gate "records the business date, sources read and completion time", but Section 9 says the result is held in the job run with no table of its own.
#* Where is it stored, and where does the data steward see it in Epic 1?
# *Section 11:* lists the gate as reading {{case_list_row}} (DF-RPT-002/019), but the flow does not use it, and this conflicts with the guardrail "no read of another module's tables". Is that read actually needed?
# *AC gaps:*
#* No AC for X9 (403); there is only TC-09.
#* No AC for a 503 when the view is down.
#* No AC for the flag-off case.

### Comment 2: NATAPATCHARA ANUROJE, 2026-11-17T11:09:51.181+0700

Comment ID 1794121

Dug into the actual SQL in {{recovery-workbench-physical-schema-v6.sql}} to check point 4 above against real evidence, and found one more issue of the same kind.

*9. {{physical_type}} = integer for every {{v_ace_batch_status}} field — confirmed with the actual seed rows*

The seed {{INSERT}} statements for {{v_ace_batch_status}} (DF-ACE-178 to -186) are literally:
{noformat}
DF-ACE-178 source_system  data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.source_system)
DF-ACE-179 business_date  data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.business_date)
DF-ACE-180 started_at     data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.started_at)
DF-ACE-181 completed_at   data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.completed_at)
DF-ACE-182 status         data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.status)
DF-ACE-183 record_count   data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.record_count)
DF-ACE-184 checksum       data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.checksum)
DF-ACE-185 feed_version   data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.feed_version)
DF-ACE-186 is_complete    data_type=TEXT  physical_type=integer  (source: public.ace_batch_run.status)
{noformat}

All 9 rows have {{physical_type='integer'}} regardless of the real column type (several are {{varchar}}, one is {{timestamptz}}, one is {{boolean}}) — the whole block was generated the same wrong way, not a one-off typo.

{color:#ff5630}*Question:*{color} Can these 9 {{sys_fields}} seed rows get their correct {{physical_type}} per column before V0001 merges?

*10. {{is_complete}} is a derived field with no way to say so*

The view itself defines it as computed, not copied:
{noformat}
CREATE OR REPLACE VIEW recovery.v_ace_batch_status AS
SELECT ..., r.status::varchar(12) AS status, ..., (r.status = 'COMPLETED') AS is_complete
FROM public.ace_batch_run r;
{noformat}

But the seed row for {{is_complete}} (DF-ACE-186, above) maps {{source_field}} to {{public.ace_batch_run.status}} — the exact same source column as the literal {{status}} field (DF-ACE-182). {{sys_fields}} has no {{is_derived}}-style flag to say "this is computed from that column, not copied from it." Same gap as RWB-E1-064's "7 derived view fields" exception (contact_type, city, post_code, country, installments, recommended_installment, recommended_package) — a recurring pattern in the dictionary design, not isolated to this view.

{color:#ff5630}*Question:*{color} Should {{sys_fields}} gain a flag column for derived fields, or is noting it only in the field description the intended approach?

----

Neither this story nor RWB-E1-064 can fix either item themselves — both explicitly say "No DDL: V0001 owns these tables," and the bad seed rows are written by V0001's seed script. This is RWB-E1-001's (TB0001-1163) territory, and worth flagging there directly since it's currently Dev In Progress.

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T11:59:02.553+0700

Comment ID 1794309

These points add to the questions already on this card.

# *One late source stops the whole case list.* Under AC9, one late or failed EFS batch holds the case list for every case.
#* Question: does the business accept this? Or should each job name the products it actually needs, and should only critical sources hold it? Please keep that job-to-product map as data, not code.
# *Sources with no disposition.* The product-to-source map names SCBPDM (DP02), COLLINS (DP11) and RPS (DP06), which still have no disposition in Integration Inventory v3 (feedback #61). The story also does not say which RWB-E1-043 table code holds the map.

Who answers: Business lead, Data steward, Solution architect.

### Comment 4: Chanapai Gingpuwaluck, 2026-11-18T16:12:13.115+0700

Comment ID 1797151

Follow-up after grooming. These points are not yet in this thread (calendar, weekly business date, gate retry, alert list, message split, endpoint access, trigger model, multi-source key, ageDays, gate result storage and the sys_fields seed are already asked above).

# *How a changed batch row is detected.* The story polls v_ace_batch_status (no event consumed) for a "new or changed" row, but the view has no updated_at or row version, and the poll interval is not stated. A rerun that turns FAILED into COMPLETED for the same business date keeps the same key.
#* Question: what is the poll interval, and how does the listener tell a changed row from one already handled (compare status and completed_at, or ask ACE for an updated_at column under RWB-ACE-001)?
# *Daily jobs started more than once.* Flow step 11 and AC1/AC6 start JOB-02, 04, 07 and 08 through EV-26 when a batch completes. With seven sources, each COMPLETED row can publish EV-26.
#* Question: is EV-26 published once per business date when all sources the jobs read are complete, or once per source? Which key stops a second run of the same job for the same business date?
# *Format of expected_by.* Physical Schema v6 holds data_product.expected_by as varchar(20), and the story uses "08:00" and "MON 08:00". The Quartz trigger per product needs a defined format.
#* Proposal: one format rule (for example a cron expression, or HH:MM plus an optional day code) validated when RWB-E1-064 loads the row.
# *Products with no source.* DP03, 04, 08, 09, 10, 12 and 14 are "current on change" and have no ACE source.
#* Question: what do stampFor() and the inputs snapshot (BR5) hold for these products: no entry, or a stamp with status LOADED and the time of the read?
# *Two endpoints and two access rules.* GET /data-products/freshness (stamp per product) and GET /data/freshness (raw batch rows) overlap. The story gives Case record R to /data-products/freshness, while Administration Stories v3 lists it under Platform administration R.
#* Question: are both endpoints needed in Epic 1, and which right applies? A case user needs only the product stamp on SCR-03.
# *MSG-GEN-006 on a read.* The text "Your request is queued and will be retried" fits a write, not a GET of freshness. Please use a read-only wording for the 503.
# *Dependencies and sprint (Jira, 18 Nov 2026).*
#* Ready or in delivery: RWB-E1-001 (TB0001-1163, Dev In Progress, Q4S2 Squad1) and RWB-E1-064 (TB0001-1225, Dev To Do, Q4S2 Squad1).
#* Blocked: RWB-E1-043 (TB0001-1204) is on Hold, and it loads the product-to-source map.
#* No ticket: RWB-E1-069 and RWB-ACE-001 (feedback #83). The flag text names V0003 as the migration that creates v_ace_batch_status, while the preconditions name RWB-E1-069 Section B. Please confirm one owner.
#* No sprint: RWB-E1-027 (TB0001-1189), whose code build step 7 changes.
#* Stories that need this one: RWB-E1-007, 011 and 056 are in Design - Grooming; RWB-E1-002, 034 and 052 are in no sprint.
#* Decision needed: deliver this story in Q4S2 behind the flag with a stubbed v_ace_batch_status and a seeded product-to-source map, or move it until RWB-E1-069, RWB-ACE-001 and RWB-E1-043 have owners and dates.

Who answers: Solution architect, ACE team, Data steward, Henka (BA), PO.


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
