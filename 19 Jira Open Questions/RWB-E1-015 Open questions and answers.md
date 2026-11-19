# RWB-E1-015 Freshness stamp per data product

| Field | Value |
|---|---|
| Jira | TB0001-1177, component E2E Workbench, status To Do, parent TB0001-1162 |
| Jira comments read | 4 (R. Kasemphin 16 Nov; N. Anuroje 17 Nov; C. Gingpuwaluck 17 Nov): about 40 points covering dependencies, business questions, AC details, two schema questions and two follow-ups |
| Story text used | Story Files v7, `RWB E1 015 Freshness stamp per data product v1.md` (15 Nov; same text in Epic 1 v9) |
| Build order | Build Sequence v6 order 56, Window 2 (16 to 27 Nov); depends on E1-001, E1-069, E1-027 |
| Prepared | 18 November 2026 |

Status key: **ANSWERED** = a document in the set decides it. **PROPOSED** = the documents imply the answer; the owner should ratify it. **OPEN** = no document decides it; options and a recommendation are given. Gap IDs (G-...) are in `Document Gaps.md`.

## Summary

| Status | Items |
|---|---|
| ANSWERED | Q03, Q05, Q14, Q28 (confirmed), Q31 |
| PROPOSED | Q02, Q04, Q06, Q08, Q10, Q11, Q12, Q15, Q16, Q17, Q18, Q21, Q22, Q25, Q26, Q27 |
| OPEN | Q01, Q07 (and Q19), Q09, Q13, Q20, Q23, Q24, Q29, Q30 |

The biggest finding is not in the comments: **the product-to-source map names sources that ACE does not ingest in Epic 1** (AMIS and RPS first release E3, GL first release E6). Under BR8 the gate would hold on them every day. See Q13 and G-015-03.

## A. Concerns (dependencies)

### Q01 RWB-ACE-001 and DL43 are open and on the critical path (OPEN)

DL43 (ACE team lead, needed by 2026-11-21) is open; its recommendation is "yes, scope and dates as in RWB-ACE-001". RAID v4 DEP-34 and DEP-35 carry the same date and owners (ACE team lead; Sponsor with the ACE team lead). No document holds an ACE commitment. The decision log gives the fallback: "Tier 1 views plus the case list, costed but not recommended". Stories that depend on this one (Build Sequence v6): E1-034, E2-010; the reviewer also lists E1-002, 007, 011, 052, 056. **Action:** the Sponsor asks the ACE team lead for a committed date before 21 Nov; if there is none, the Epic 1 release plan has to choose between moving 30 Nov and the Tier 1 fallback.

### Q02 No fallback when the flag is off (PROPOSED)

Section 13 says only "the panel shows no stamp". Nothing says what `DailyCompletenessGate` does. Two options:

- **A (recommended).** The gate returns COMPLETE with reason `NOT_CHECKED`, writes a warning to the job run, and the data steward confirms the day by hand until RWB-ACE-001 lands. The load checks it replaced are already retired, so HOLD would stop the case list from existing at all in Epic 1.
- **B.** The gate returns HOLD every day; no case list until ACE-001.

Decision: Business lead and Data steward. Add an AC for the flag-off case (see Q23).

### Q03 Depends on (ANSWERED)

E1-001, E1-069 and E1-027 are already in the header. **E1-043 and E1-064 are used but not listed**: the product-to-source map is loaded through E1-043 (section 12) and `refresh_cycle` and `expected_by` through E1-064 (section 13). Both are earlier in Build Sequence v6 (orders 8 and 13), so adding them changes no schedule. Add them to Depends on.

### Q04 E1-015 changes E1-027's code (build step 7) (PROPOSED)

E1-027 is order 20 and this story is order 56, so E1-027 will already be built. **Proposed:** this story only publishes `FreshnessQuery.stampsFor()`; the call from the inputs snapshot builder is a change request raised against E1-027's owner (module P7) with its own test. AC3 stays here as the acceptance test of the pair.

### Q05 Thai text and message wording (ANSWERED; the 08:00 times are Q07)

- **a. DL10.** Error and Message Standard v4 holds the Thai text for MSG-P1-001 as "proposed". DL10 (business lead with Legal and Compliance) is open and past its date (5 Nov). Nothing to build around; the English text ships and the Thai text follows.
- **b. Message wording.** Standard v4 reads "{product} is from {date}. Today's **load** has not arrived." The story says "Today's **ACE batch** has not arrived." Update the standard (G-015-04).

## B. Business clarifications

### Q06 Business calendar (PROPOSED)

Epic 1 reads the holiday calendar from the ACE view `v_ace_holiday` (E1-043 BR1: "The holiday calendar is not among [the reference tables]; it is read from v_ace_holiday"; Batch Design v4 section 7: "Working days come from the bank holiday calendar"). That is the bank holiday calendar, so Thai bank holidays count. Owner: ACE team (the view reads an ACE table). No document names a business owner of the calendar content; ask the ACE team who maintains it.

### Q07 Cut-off times: 08:00, 07:15 or 07:00 (OPEN, gap G-015-02)

The documents disagree on when "late" starts:

| Source | Time |
|---|---|
| E1-015 (expected-by, AC2, AC9) | 08:00 daily, Monday 08:00 weekly. DL11 is cited as the source but DL11 is the non-functional targets decision, open |
| Observability Design v3, alert "Load late" | not arrived by 07:00, to the data steward |
| Batch Design v4, JOB-03 | morning allocation by 07:00 |
| E1-002 (per reviewer) | JOB-04 runs at 07:15 if JOB-03 has not finished |

A gate at 08:00 cannot protect an allocation due at 07:00. **Recommendation:** keep `expected_by` as data (E1-064) and set it to 07:00 (daily) and Monday 07:00 (weekly), which matches the alert and the allocation deadline; update AC2, AC7, AC9, AC11 and the E1-002 text to read the value from data. Nobody approved 08:00 in any document. Decision: Business lead with Data steward.

### Q08 Expected business date (PROPOSED)

Daily products: the previous working day, from the calendar in Q06 (the 12-01 cut-off expects 11-30, and the Friday 11-27 before Monday 11-30 per AC2). Weekly products: not defined, and AC3, AC8 and AC11 use three different patterns (Story Defects v4 lists AC3 as open). **Proposed:** the weekly expected business date is the last working day before the Monday cut-off (Friday), the same T-1 rule. Then AC3 reads business date 11-27 loaded Monday 11-30, AC8 reads 11-27 completed Monday 11-30 04:40, AC11 is already correct. Confirm with the Data steward.

### Q09 Batch never arrives that day (OPEN)

Batch Design v4: the data jobs "start when its record arrives" and "no job retries a load". E1-015 says the story "polls the batch view" and gives no interval. There is no final deadline and no override anywhere in the documents. **Proposed:** a poll interval property (assumed 5 minutes, DL11); no automatic skip; the case list holds and the previous list stays published (BR8). An override on business sign-off is a new decision before Epic 2 (SCR-45). Owner: Data steward and Business lead.

### Q10 Alert recipients (PROPOSED)

Section 10 names the data steward and the platform administrator; AC9 and E1-002 X1 add the team manager group. Batch Design v4 says AceDataLate goes to the data steward and Observability v3 sends "Load late" to the data steward only. **Proposed:** e-mail alert to the data steward and the platform administrator; the team managers see MSG-P1-001 as a banner on the case list (E1-002), not by e-mail. Fix AC9.

### Q11 One message for "missing" and "FAILED" (PROPOSED)

Error and Message Standard v4 has one message, MSG-P1-001. The user does different things in each case. **Proposed:** keep MSG-P1-001 for "not arrived" and add `MSG-P1-023` (next free; P1 ends at 022) for "failed: the previous data stays in use", with Thai text under DL10.

### Q12 Who may read the stamps, and which fields (PROPOSED)

API v4 gives `GET /data-products/freshness` the capability Case record R. `GET /data/freshness` **does not exist in API v4** (G-X-05). Section 10 gives the data steward Platform administration R only, so the data steward cannot call a Case record R endpoint unless the matrix gives them that right. **Proposed:** keep `/data-products/freshness` (Case record R; its response already has no `record_count` or `feed_version`) and move the ACE batch view endpoint to **Platform administration R**, which answers both questions: case users do not see operational data and the data steward can call it.

### Q13 The 99 percent measure and which sources the gate waits for (OPEN, gap G-015-03)

**Measure.** BM-26 "Loads on time and complete" (Business Measures and Targets v2): loads passed on time divided by loads due, target 99.0 percent from Epic 1, owner data steward. Its source is "Load check log", which no longer exists. **Proposed:** per source and business day, on time = a COMPLETED row in `v_ace_batch_status` by `expected_by`; reported by the data steward from `data_product_load`. Update BM-26 to the ACE read path (G-015-03).

**Sources in the map.** The Integration Inventory v3 first-release column shows: CCMS, SVAF, LIT, WIN, EFS, SCBPDM, COLLINS = E1; **AMIS = E3, RPS = E3, GL = E6**. The product-to-source map (section 12) puts AMIS and RPS under DP06 and GL under DP13, and AC9's Background lists GL as COMPLETED. In Epic 1 those batches will never exist, so DP06 and DP13 would be stale every day and the gate would hold. **Proposed:** the map carries a `first_release` or `active_from` column and the gate ignores sources not yet live. Owner: Data steward with the ACE team.

### Q14 Snapshot status in the decision log (ANSWERED)

The status **at decision time**. BR5 records the product, business date, load time and status in the inputs snapshot, and the decision log is append-only and hash chained (E1-008). Setting a later row to STALE does not change a snapshot that was already written.

## C. AC details

### Q15 AC3 against AC8 and AC11 (weekly products) (PROPOSED)

Resolved by Q08.

### Q16 Trigger model: AC1 and AC6 against AC9 and BR8 (PROPOSED)

Batch Design v4: JOB-02 starts on the ALS record; JOB-04, JOB-07 and JOB-08 follow JOB-02 on the same record; JOB-03 follows by 07:00. BR8: no job starts until every source it reads is COMPLETED. **Proposed reading:** each job starts when the sources **it reads** are COMPLETED. JOB-02, JOB-07 and JOB-08 read ALS only, so they start on the ALS record. JOB-04 reads the other sources, so it calls the gate. If ALS completes and EFS has not: JOB-02, 07, 08 start; the case list step of JOB-04 holds (AC9). Rewrite AC1 so that it starts JOB-02, 07 and 08, and calls the gate for JOB-04. The job-to-source map (Q18) makes this explicit.

### Q17 Which job holds the case list? (PROPOSED, gap G-015-06)

AC9 says "the case list step of JOB-04". Batch Design v4 calls JOB-04 "Daily reconciliation" and JOB-02 "Case creation". The documents never name the job that writes `case_list_row`. Settle it once (for E1-002, E1-015 and E1-056) and use the same job ID everywhere.

### Q18 No job-to-product map (PROPOSED)

Confirmed: section 12 has only the product-to-source map. `check(businessDate, productCodes)` gets its product codes from the calling job. **Proposed:** a second reference row set `job_source_map` (job ID, source system, critical Y or N) owned by the data steward. **E1-043 has no table code for it**: its BR1 lists 12 codes (PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, PRODUCT_PARAMETER), so both maps need codes added to LOV-REF-TABLE (G-015-01). Answers C. Gingpuwaluck item 2 too.

### Q19 Gate time inconsistent (see Q07).

### Q20 Multi-source products against the unique key (OPEN, gap G-015-05)

Physical Schema v6: `data_product_load` has one `source_system varchar(40) NOT NULL` and `UNIQUE (product_code, business_date)`. For DP13 (ALS and GL) or DP06 (four sources) the second source's COMPLETED row hits the unique key and would be counted as a duplicate (AC5, BR4 conflict). Options: **(1, recommended)** change the key to `(product_code, business_date, source_system)`; the stamp in use is the oldest business date among the source rows; or **(2)** keep one row, store only the limiting (oldest or late) source, and track duplicates by batch row ID in `processed_event`. Option 1 needs a Physical Schema v7 change **before V0001 merges** (RWB-E1-001 is Dev In Progress). Owner: Data architect.

### Q21 Which row is STALE, and when is it cleared (PROPOSED)

AC2 sets STALE on the 11-27 row; AC6 then writes 11-30 as LOADED. **Proposed:** the 11-27 row stays STALE as history; the stamp in use is the newest LOADED row; `staleSince` comes from the row in use only while it is STALE. The guardrail "the stale check never changes a loaded row" contradicts AC2 and should read "never deletes a loaded row or alters its business date and times".

### Q22 AC4: time of "STALE from 05:20" and a FAILED batch that completes later (PROPOSED)

Use the batch row's time, not the time the system reads it: ACE Field Gap List v1 shows `ace_batch_run.started_at` NOT NULL and `completed_at` nullable, so use `completed_at` when present, otherwise `started_at`. A FAILED batch that later COMPLETES for the same business date follows AC6 (new COMPLETED row, status LOADED, jobs start); add one explicit AC.

### Q23 `ageDays` (OPEN)

No document defines it. **Recommendation:** business days between the business date and today (Asia/Bangkok), using `v_ace_holiday`; on Monday reading Friday's data it is 1. Measured from today, not from `completed_at`. Owner: Data steward.

### Q24 `source_extracted_at` = `started_at` (OPEN, gap G-015-07)

Confirmed: ACE Field Gap List v1 shows `ace_batch_run` has `started_at` and `completed_at` and no source extraction time. The ACE batch start is not when the source system extracted the data, and the story shows it on the case record and stores it in decision snapshots (audit). Either label it "ACE batch started" or ask RWB-ACE-001 for a real `source_extracted_at` column. Decision: ACE team and Compliance.

### Q25 Where the gate result is stored (PROPOSED)

Section 9 says in the job run, with no table. **Proposed:** the gate result is written to the JOB-04 run record and shows as the job's `checks` in `GET /admin/jobs` (RWB-E1-056) and in the "Recovery jobs" workbook. SCR-45 is Epic 2. State this in section 9.

### Q26 Section 11 lists `case_list_row` as read by the gate (PROPOSED)

The flow never reads it; AC9 only asserts that no `case_list_row` is written. **Proposed:** remove DF-RPT-002 and DF-RPT-019 from section 11. The test can assert through JOB-04's own repository, which keeps the guardrail "no read of another module's tables".

### Q27 Missing ACs (PROPOSED)

Add:

```gherkin
  Scenario: AC12 Role without the right
    When a user with role RW-REFADM calls GET /data-products/freshness
    Then the response is 403 with message MSG-P4-002

  Scenario: AC13 Batch view unavailable
    Given v_ace_batch_status cannot be read
    When GET /data-products/freshness is called
    Then the response is 503 with message MSG-GEN-006
    Then the stored stamps are not changed

  Scenario: AC14 Feature flag off
    Given flag "rwb.dataengine.freshness-stamp" is off
    When SCR-03 Case record is opened
    Then the data panel shows no stamp
    Then DailyCompletenessGate returns COMPLETE with reason NOT_CHECKED
```

## D. Schema questions (N. Anuroje)

### Q28 `physical_type` = integer for every `v_ace_batch_status` field (CONFIRMED, gap G-015-08)

Confirmed in `06 Data/Recovery Workbench Physical Schema v6.sql` (the sys_fields seed rows DF-ACE-178 to DF-ACE-186) **and** in Logical Data Model and Data Dictionary v8 (same rows: `data_type TEXT`, `physical_type integer`). It is wider than nine rows: **173 of the 304 DF-ACE rows have `physical_type integer`** (the others: varchar(255) 109, date 18, boolean 4; there is no timestamptz or numeric at all, so even `appraised_value` is "integer"). For the nine rows, the view in the same file and ACE Field Gap List v1 give the correct values:

| Field | Correct physical type | Source |
|---|---|---|
| source_system | varchar(20) | view cast |
| business_date | date | ace_batch_run |
| started_at | timestamptz | ace_batch_run |
| completed_at | timestamptz (nullable) | ace_batch_run |
| status | varchar(12) | view cast |
| record_count | bigint | ace_batch_run |
| checksum | varchar(64) | view cast |
| feed_version | varchar(20) | view cast |
| is_complete | boolean | derived: status = 'COMPLETED' |

The `data_type` column (TEXT for all) needs the matching business type (text, date, datetime, number, boolean). Yes, the rows should be corrected before V0001 merges. The generator that produced the block must be fixed, not only these nine rows. Owner: Data architect (Physical Schema and Data Dictionary owner), then tell RWB-E1-001 (TB0001-1163).

### Q29 Derived fields have no flag in `sys_fields` (OPEN, gap G-015-09)

Confirmed: the `sys_fields` table in Physical Schema v6 has no derived flag, and DF-ACE-186 `is_complete` points at the same source column as DF-ACE-182 `status`. **Recommendation:** add `is_derived boolean NOT NULL DEFAULT false` and put the expression in `source_field` (for example `derived: status = 'COMPLETED'`). The pattern recurs (E1-064's seven derived view fields), and CHK-01 could then check it. Needs Physical Schema v7 before V0001 merges.

## E. Follow-up (C. Gingpuwaluck)

### Q30 One late source stops the whole case list (OPEN)

BR8 is deliberate: it replaces the daily gate of the retired load checks (FSD P1 A2.14). The business acceptance is not recorded. Options: **A** accept; **B (recommended)** each job names the sources it needs, in the job-source map (Q18), and only sources flagged critical hold the job. Keep the map as data (BR7). Decision: Business lead and Data steward.

### Q31 Sources with no disposition (ANSWERED)

The comment is out of date against System Disposition and Integration Inventory v3: **SCBPDM** is Keep, ACE ingests the customer profile (INT-04, E1); **COLLINS** is Keep and feed, feeds the daily batch and receives decisions back (INT-08, INT-20, E1); **RPS** is Keep, ACE ingests the weekly file (INT-13, first release **E3**). The table code that holds the map is the open point in Q18.

## Changes to make to the story

1. Header: Depends on adds RWB-E1-043 and RWB-E1-064 (Q03).
2. Section 12: remove or re-home `GET /data/freshness` and give it Platform administration R (Q12).
3. Section 12: map gets an `active_from` column; add `job_source_map` and table codes (Q13, Q18).
4. Rewrite AC1, AC3, AC8, AC9 for the trigger model and the weekly pattern (Q08, Q16).
5. Section 10: alert recipients (Q10); section 9: gate result location (Q25); section 11: drop `case_list_row` (Q26).
6. Add AC12 to AC14 and the FAILED-then-COMPLETED case (Q22, Q27).
7. Guardrail wording for the stale check (Q21).
8. Define `ageDays` (Q23) and label `source_extracted_at` correctly (Q24).
9. Section 13: build step 7 becomes a change request to E1-027 (Q04); flag-off gate behaviour (Q02).
