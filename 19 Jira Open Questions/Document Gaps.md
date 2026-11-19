# Document gaps found while answering the Jira questions

Prepared 18 November 2026 for RWB-E1-047, RWB-E1-015, RWB-E1-007 and RWB-E1-056. A gap is something the **latest document set** does not say, says two ways, or gets wrong. Each row says what to change and who has to decide. Priority: **P1** blocks a build or a merge, **P2** blocks a test or a decision, **P3** is a clean-up.

Documents checked (latest versions): Story Files v7 and Epic 1 v9, Decision Log v10, Physical Schema v6, Logical Data Model and Data Dictionary v8, API Specification v4, Interface Specifications v3, Integration Inventory v3, Non Functional Specification v3, Batch and Scheduling Design v4, Observability and Monitoring Design v3, Error and Message Standard v4, Test Cases v7, Story Defects v4, Build Sequence v6, RAID v4, Data Load Story Removals v2, Run Operating Model v2, Users Roles and Permissions v4, ACE Field Gap List v1, and `recovery-modules.yaml` in the workbench repo. **Not opened:** Project Hub v17 (27 MB HTML; Epic 1 v9 and the story files carry the same story text) and the Henka attachment on TB0001-1169 (the Jira tool cannot read it).

## Cross-story gaps

| ID | Gap | Evidence | Fix | Decides | P |
|---|---|---|---|---|---|
| G-X-01 | Four jobs have no catalog row and no run book: the weekly flag report job (E1-047), JOB-20, JOB-22 (and JOB-21 in Epic 2) | Batch Design v4 lists 22 jobs; E1-056 seeds 16 rows; `RunbookCompletenessTest` checks every Quartz job. AC4 of E1-056 uses JOB-20 as an invented ID | Add the flag report job as JOB-23 in Batch Design v5; E1-056 catalog becomes 19 rows (JOB-21 follows with E2-037); use "JOB-99" in test examples | Tech lead | P1 |
| G-X-02 | Observability Design v3 still lists the alerts "Load failed" and "Load late" from before the ACE re-base, and has no alert for "job over threshold" or "flag overdue" | Observability v3 section 2 | Rewrite to "ACE batch late or failed" (AceDataLate, EV-27) and add the two alerts | Solution architect | P2 |
| G-X-03 | Dependency lists disagree with Build Sequence v6 | E1-007 header says it depends on E1-015 (order 56), Build Sequence builds it at order 11. E1-056 needs E1-015 and TE-007 (orders 56 and 21) but is built at order 18, and TE-007 depends on E1-056 | Re-sequence TE-007 before E1-056; correct the headers | Delivery lead, Tech lead | P1 |
| G-X-04 | Physical Schema v7 needs four changes **before V0001 merges** (RWB-E1-001, TB0001-1163, Dev In Progress) | (1) `data_product_load` key for multi-source products; (2) `processed_event.hit_count` to `duplicate_count` default 0; (3) `sys_fields.is_derived`; (4) correct `physical_type` and `data_type` for the DF-ACE rows (G-015-08) | One schema v7 with the four changes, then E1-001 reads it | Data architect | P1 |
| G-X-05 | API Specification v5 needs the following | `GET /feature-flags` is right but the E1-047 story says "Map"; `If-Match` is declared nowhere (E1-047 PATCH, E1-007 resend, E1-056 rerun); `GET /data/freshness` (E1-015) does not exist in v4; resend returns `OutboundItem` with no message field; `/admin/jobs/{jobId}/rerun` should be `executionId`; `overdue` on `GET /admin/feature-flags` is a string; `daysOverdue` undefined | Raise v5; descriptions for the overdue filter and `daysOverdue` | API owner | P2 |
| G-X-06 | New message IDs must be assigned once. Error and Message Standard v4 ends at MSG-P1-022 and MSG-P2-025 | Proposed here: **MSG-P1-023** failed-batch text (E1-015 Q11); **MSG-P2-026** invalid flag key, **MSG-P2-027** duplicate flag key (E1-047 Q05); **MSG-P2-028** run book forbidden line (E1-056 Q17), **MSG-P2-029** job over threshold (Q24), **MSG-P2-030** job already completed (Q28). Also fix MSG-P1-001 wording ("load" to "ACE batch"), MSG-P2-001 wording and MSG-P2-005 ("six" to "eight" sections) | Standard v5 with English and Thai (Thai under DL10) | Content owner | P2 |

## RWB-E1-047

| ID | Gap | Evidence | Fix | Decides | P |
|---|---|---|---|---|---|
| G-047-01 | Story says GET /feature-flags returns a map; the contract returns an array | API v4 `getFeatureFlags` | Correct the story | BA | P2 |
| G-047-02 | The story says its own migration creates `feature_flag` with primary key `flag_key` and a check constraint; Physical Schema v6 already defines both tables with `id uuid` as primary key and a unique `flag_key`, and RWB-E1-001 does not mention them | Story section 13; Physical Schema v6 lines 1248 to 1285 | Decide who creates the tables and where the key check lives | Tech lead | P1 |
| G-047-03 | No AC, test or message for an invalid key, a duplicate key or a change to the same value; the duplicate key reuses a message that does not fit | Story Defects v4 (E1-047 item 2, open) | Add AC10 to AC12 and messages (G-X-06) | BA | P2 |
| G-047-04 | No document describes the ACE audit log service or the ACE notification path the story depends on | Story sections 3 and 13 | Get the contract and SIT/UAT availability from the ACE team; fall back to the Log Analytics alert rule | ACE team | P2 |
| G-047-05 | Flag keys use the module code in places (`rwb.p3.temporal`, 29 mentions; `rwb.p3.drools`, `rwb.p3.ruleload`, `rwb.p3.rule-harness`, `rwb.p3.quartz-jobs`, `rwb.p3.rule-change-report`) and the module name elsewhere (`rwb.casewf.*`) | `recovery-modules.yaml`: "the only source of module names" | Rename the `rwb.p3.*` flags to `rwb.casewf.*` in the stories and TSDs | Tech lead | P3 |
| G-047-06 | The allowed `<module>` values exist only in a test resource, but the runtime key check needs them | `recovery-modules.yaml` is under `src/test/resources` | Add a reference list of module names (E1-043 LOV) | Tech lead | P2 |
| G-047-07 | No approval or change-control rule for a PROD flag change; RW-SECADM holds "A" with no function | Users Roles v4 Key; Admin and Access Model v5 section 6.2 | Decide: none in Epic 1, or a new story | Product owner, Security, Operational Risk | P2 |

## RWB-E1-015

| ID | Gap | Evidence | Fix | Decides | P |
|---|---|---|---|---|---|
| G-015-01 | The product-to-source map is "loaded through RWB-E1-043" but E1-043 has no table code for it, and there is no job-to-source map at all | E1-043 BR1 lists 12 codes | Add `PRODUCT_SOURCE` and `JOB_SOURCE` to LOV-REF-TABLE; see also `JOB_CATALOG` (E1-056 Q36) | BA, Data steward | P1 |
| G-015-02 | Four different cut-off times: 08:00 (story), 07:15 (E1-002), 07:00 (Observability v3 "Load late"), allocation "by 07:00" (Batch v4). Nobody approved 08:00; the story cites DL11, which is the NFR decision | Q07 | One value held in `data_product.expected_by`; the stories read it | Business lead, Data steward | P1 |
| G-015-03 | The map names sources that are not live in Epic 1 (AMIS and RPS first release E3, GL E6), so DP06 and DP13 would be stale every day. BM-26 still measures from a "Load check log" that no longer exists | Integration Inventory v3; Business Measures v2 | `active_from` on the map; BM-26 reads `data_product_load` | Data steward, ACE team | P1 |
| G-015-04 | MSG-P1-001 reads "load" in Standard v4 and "ACE batch" in the story; MSG-P1-002 (load refused) is obsolete | Error and Message Standard v4 | Standard v5 (G-X-06) | Content owner | P3 |
| G-015-05 | `data_product_load` has one source and `UNIQUE (product_code, business_date)`, which breaks multi-source products and the duplicate count | Physical Schema v6 | Key `(product_code, business_date, source_system)` (G-X-04) | Data architect | P1 |
| G-015-06 | No document names the job that writes `case_list_row`. E1-015 and E1-056 say "the case list step of JOB-04"; Batch v4 calls JOB-04 "Daily reconciliation" and JOB-02 "Case creation" | Batch Design v4 | Name it once and use it everywhere | Tech lead | P2 |
| G-015-07 | `source_extracted_at` is filled from the ACE batch `started_at`; ACE has no source extraction time | ACE Field Gap List v1 | Relabel, or add a column to RWB-ACE-001 | ACE team, Compliance | P2 |
| G-015-08 | 173 of the 304 DF-ACE `sys_fields` rows have `physical_type integer`, including all nine `v_ace_batch_status` rows; `data_type` is TEXT for 252 rows. Same in Data Dictionary v8 | Physical Schema v6; Data Dictionary v8 | Fix the generator and re-issue both | Data architect | P1 |
| G-015-09 | `sys_fields` cannot mark a derived field (`is_complete`, and the seven derived view fields of E1-064) | Physical Schema v6 | Add `is_derived` (G-X-04) | Data architect | P2 |
| G-015-10 | No fallback or business rule for the daily gate when the flag is off, when a batch never arrives, or for `ageDays` and the weekly business date | Q02, Q08, Q09, Q23 | Decide and write into the story | Business lead, Data steward | P2 |

## RWB-E1-007

| ID | Gap | Evidence | Fix | Decides | P |
|---|---|---|---|---|---|
| G-007-01 | The Jira title and description still describe "file loads and outbound files"; the story is outbound only | Data Load Story Removals v2 | Replace with the v7 text; review the Block and R-* labels | BA | P1 |
| G-007-02 | AC3 still has 3 attempts with waits of 5, 15 and 45 minutes. Story Defects v4 closed this item in error. INT-14 says "after the third failure"; NFR-026 says "three retries" | Story AC3; Interface Specifications v3; NFR v3 | Choose 4 attempts or `[5, 15]` and align story, INT-14 row, test case | Integration architect | P1 |
| G-007-03 | "Acknowledged" is undefined: the flow waits for an acknowledgment file, BR9 says no file is picked up, and WIN proof of delivery reaches ACE weekly | Story flow step 6, BR9; Integration Inventory v3 | Define it (Q15) and name the file | Integration architect, Henka | P1 |
| G-007-04 | Test case IDs differ between the story and Test Cases v7 (v7 adds TC-08 and TC-09; renumbers 05 to 07) | Test Cases v7 | Align | QA | P2 |
| G-007-05 | MSG-P2-001 wording differs; MSG-P2-001 and MSG-GEN-005 are missing from the SCR-09 list | Standard v4; SCR-09 | Fix (G-X-06) | Content owner | P3 |
| G-007-06 | INT-14 SFTP folder, write access and acknowledgment file name are unknown; encryption, retention class and transport for INT-14, 19, 20, 25 are unstated; DL26 is open | Interface Specifications v3; Records Retention v2 | Answers from Henka, Security, Compliance | Henka, Security, Compliance | P1 |
| G-007-07 | One transport failure creates one task per case (85); `task.case_id` is NOT NULL | Physical Schema v6 | One alert per file (Q16) | Integration architect, Product owner | P1 |

## RWB-E1-056

| ID | Gap | Evidence | Fix | Decides | P |
|---|---|---|---|---|---|
| G-056-01 | Build order contradicts the preconditions (see G-X-03) | Build Sequence v6 | Re-sequence | Delivery lead | P1 |
| G-056-02 | Test Cases v7 and FSD P7 still use 13 rows, JOB-03, a different date and JOB-12 | Test Cases v7 TC-E1-056-01 to -06 | Regenerate from the story | QA | P2 |
| G-056-04 | Nobody is named to provision the Log Analytics workbook, alert rules and workbook access in DEV, SIT and UAT | Observability v3 | Name an owner | ACE team | P2 |
| G-056-05 | Language of run books and alert text, and the PROD holder of RW-PLATADM, are not decided | Run Operating Model v2; DL39 | Decide | Business lead | P3 |
| G-056-06 | MSG-P2-005 says "six sections"; the story has eight | Standard v4 | Fix (G-X-06) | Content owner | P3 |
| G-056-07 | CELK is not in any document; the story and Observability v3 use Log Analytics | Search of the converted set | Decide the tool before building the workbook | Solution architect | P2 |
| G-056-08 | The module map file has no list of forbidden run book words | `recovery-modules.yaml` | Add `forbiddenRunbookTerms` via a TE-001 change | Tech lead | P2 |
| G-056-09 | Alert channels, out-of-hours cover and a force-rerun path after an ACE restatement are in no document | Q12, Q15 | Decide | SCB IT operations, Product owner | P3 |

## Recommended order of work

1. **Before V0001 merges (today):** G-X-04 (schema v7: four changes) and G-015-08. These change a migration that is already in progress.
2. **This week, to unblock builds:** G-X-03 re-sequence, G-047-02 who creates the flag tables, G-007-02 retry count, G-007-03 acknowledged, G-007-07 one task per file, G-015-01 table codes, G-015-02 one cut-off, G-015-03 sources live in Epic 1, G-X-01 catalog rows.
3. **Before 21 Nov:** ACE team lead answer on DL43 / RWB-ACE-001 (E1-015 Q01).
4. **Then:** API v5, message standard v5, Batch Design v5, Observability v4, and the story re-issues listed at the end of each question file.
