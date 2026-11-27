# Escalations raised by editors (input to decision batch D: RD-P1-060+ and follow-up reviews)

## Need a ruling
1. E2021: RD-P1-007 rule 7 externalRef = pod_key, but the letter entry carries the barcode – proof and letter never pair (NEW-GAP-S10-16). (S10)
2. E2001: DP01-only gate means a stale EFS (DP05) load no longer refuses the read; history can be partial. (S10)
3. E2022: no store for counted failure references – count-once rule blocked (NEW-GAP-S10-17). (S10)
4. /payments path used by E2008 and E1013 with different query parameters – one owner needed. (S10)
5. JOB-08 owner: RD-P1-040 says rwb-payment, GAP-0657 says rwb-integration (S10 followed GAP-0657).
6. DM012: published DecisionRecorded schema has no rule/version/chain fields and lets rwb-decision assign the chain; migrated entries must keep theirs (NEW-GAP-S13-4, blocking). (S13)
7. Allow-list exceptions: DM013 keeps legacy proceeds amount/received_date (GAP-2533 directive); DM012 carries model_version (legacy AC). Confirm. (S13)
8. DM002: register treats it as writing party_ext; Data Migration Approach says DM002 migrates nothing (NEW-GAP-S12-2). (S12)
9. DM007: lawsuit_no read from ACE, never carried – no link from migrated legal action to court record (NEW-GAP-S12-6). (S12)
10. E7003 (ITG): AceDataReady used to carry deceased/bankrupt flags; RD-P1-003 payload has four fields – flags now read via DP02; S8 stories and contracts need the same (REQUEST). (L01)
11. RWB-P3-E2001-APP: case entry required ALS and EFS; RD-P1-040 starts on ALS alone – does EFS history append need its own completeness check? Late event 05:30 vs handover.hold_until 09:00 (NEW-GAP-L03-2). (L03)
12. RWB-P2-E2007-APP: retries a failed gate on the next AceDataReady for the same date, but RD-P1-041 publishes no second event for a stamped date – retry path? (L05)
13. RWB-P2-E1007: ALS/COMPLETED start rule also applied to held-file release – confirm. (L05)
14. RWB-PLT-NF07-INF: DailyCaseRun described as a Temporal Schedule started by an event – confirm wording with rwb-case owner. (L02)
15. RWB-P7-E1020-APP: preconditions say AceDataReady starts JOB-20; body runs JOB-20 on a 00:01 schedule. (L04)
16. RWB-P3-E2006-APP: reads /freshness, /accounts/{id}, /collateral/{id}; rwb-source-data.yaml 5.1.0 publishes only /data-products/freshness. (L04)
17. Never-stamped products (businessDate null): what the data-date header, stale banner, input age and data_as_of show (NEW-GAP-L03-1, L04-01, L04-03, S12-1). (L03, L04)
18. Fixture dates vs RD-P1-041 expected business date: RWB-P3-E2011 (APP, CON), RWB-P3-E2014-APP, RWB-P7-E2014 (APP, CON) (NEW-GAP-L04-02). (L04)

## Need a full review/edit (ACE boundary or redesign beyond alignment)
- RWB-P8-E4044-APP, RWB-P8-E4044-CON, RWB-P8-E4045-APP: read recovery.v_ace_batch_status directly (breaks the D-RCV-60 ACE rule); E4044 starts from that read, not AceDataReady. (L06)
- RWB-P3-E2006-APP (item 16).

## Shallow edits sent back
- S2 (E1011 APP/CON/OPS, E1013 APP) fixed only ownership findings (10 of 106) – re-run on GPT Sol as S2b.
19. RWB-S7-E6023 (APP, CON): expects an unnamed "monthly GL write-off posting product ready" event on rwb.source-data.events.v1; RD-P1-003 / Kafka v3 carry only AceDataReady and AceDataLate – what starts that reconciliation step? (L08)
20. RWB-P8-E4047-APP, RWB-P8-E4050-APP: say AceDataReady is read through the contract, not consumed from the topic; rulings publish it and have rwb-payment start on it – subscription redesign. (L07)
21. rwb-payment uses one consumer group per story on rwb.source-data.events.v1; RD-P1-003 rule 6 allows one group per service per topic. (L07)
22. RWB-P9-E2009-APP: never-stamped product – date shown in MSG-P1-001 and meaning of "last complete day" (joins item 17). (L07)
23. rwb-comms access to clear customer name/address on DP02 for notices (NEW-GAP-F02-1; E1052 AC1). (F02)
24. NEW-GAP-A1 widen: no rwb-case read/rerun for JOB-03 and JOB-06 steps (ITG E1020, E1030). (F02)
25. rwb-source-data.yaml 5.1.0 lacks GET /proof-of-delivery and GET /admin/reconciliation/results that ITG stories use. (F02)
26. EFS history appender: RD-P1-007 rule 8 says the rwb-integration hand-over run; staged RWB-P3-E2001-APP has rwb-case doing it. (F04)
27. JOB-14 rerun of a completed run (TE008) vs RD-P1-012 failed-only rerun (NEW-GAP-F04-1). (F04)
28. ITG harness reset of append-only ledger rows – blocker (NEW-GAP-F04-2, W1J01). (F04)
29. Staged rwb-source-data.yaml lacks /booking-facts, /batch-status, /payments, /accounts/{accountKey}/installment-facts published by staged E2007/E2008 APP stories – W1 contract must add or the stories drop them. (F04)
30. JOB-15 trigger: Airflow (ITG E2009, batch design) vs Temporal Schedule (P9 app story). (F05)
31. No published read of the stage 2 break list; no rerun of a completed run (E2010 ITG, E4050 ITG – NEW-GAP-F05-2). (F05)
32. Delivered-letter ledger entry could be written by two services; CONTACT vs PROMISE type for promise-to-pay rows (ITG E2034). (F05)
33. No job computes REC-04 / REC-06; some ACE batch record fields not exposed (ITG E4050 AC1 not ready). (F05)
34. Staged source-data AsyncAPI still 5.0.0 with key caseId – check W1 applied RD-P1-003. (F05)
35. REC-05 key list (RD-P1-022) excludes plan_ref and asset_key orphans that DM004/DM006 expect (NEW-GAP-F06-4, F06-6). (F06)
36. DP04 refresh: DM004-APP says on change with no ACE source; rulings stamp it daily. (F06)
37. Hand-recorded proof of delivery – does it write a ledger entry (NEW-GAP-F06-1)? (F06)

## Mechanical checks for the finishing pass
- Wrong GAP numbers: AD018-APP v3 cites GAP-3280/GAP-3272, AD019-APP v3 cites GAP-3276/GAP-3275 for subjects Gap Register v3 gives to other items – verify every GAP-327x+ cited in staged v3 stories against the register text (temp-ID mapping fault?). (F06)
- Check P1 E1065 APP/CON/DB v3 after S7: must not rename the sandbox database (RD-P1-046). (F03)
- Check P1 E1066 APP v3 AC15: missing Idempotency-Key must answer MSG-PLT-N009-03 (RD-P1-001), not MSG-GEN-004. (F03)
38. Screening agent read of unmasked call-note text (NEW-GAP-F03-2); old sandbox kept after a failed build, and who seeds the other schemas (NEW-GAP-F03-4, F03-5); no published read for held proof-of-delivery rows and the REC-09 break (NEW-GAP-F03-1). (F03)
39. Proof-of-delivery read callers: rwb-asset reads it (S5 E3022) but RWB-P1-E1055-APP v3 names only rwb-comms. (F10)
40. No permission row lets rwb-comms append the delivery entry (NEW-GAP-F10-01). (F10)
41. Ledger cannot identify a complaint – blocks P10 E1062 X1 (NEW-GAP-F10-02). (F10)
42. No date-wide DP06 read for S5 reconciliation (NEW-GAP-F10-03, blocker). (F10)
43. Break account keys and orphan keys have no published read (P3 AD019; GAP-1508, NEW-GAP-S2B-03). (F10)
44. Open-case key check done twice: P1 REC-05 (RD-P1-022) and RWB-P3-E1011-APP (NEW-GAP-F11-4). (F11)
45. Late-batch timing: rwb-case list alert 07:15 vs P1 STALE at 08:00; how rwb-case derives the expected date (NEW-GAP-F11-2). (F11)
46. Contract additions requested: rwb-case.yaml GET /parameters/{key} (RD-P1-028); rwb-source-data.yaml PUT /extension-facts/parties/{personKey} and /accounts/{accountKey} (RD-P1-006); freshness query name product vs productCode (E1015-CON v3 text). recon.tolerance.pct used_by must list the rwb-case quality run. (F11)
47. Source of region_code / branch_code on case record (NEW-GAP-F11-6); parameter read blocker (NEW-GAP-F11-8). (F11)
48. Readiness repeat: ITG DM stories assume a repeated readiness call writes no second reconciliation run; RD-P1-040 allows a new run after a closed one – confirm E1011 idempotency. (F07)
49. Contract gaps outside P1: rwb-access.yaml lacks POST /authorise (in Service Contract Catalog); rwb-partner.yaml lacks staff read of an instruction; rwb-writeoff.yaml lacks read of a write-off decision (NEW-GAP-F07-02). identity_ref person key? (NEW-GAP-F07-01). (F07)
50. rwb-partner as ledger appender (RD-P1-007 REST caller) contradicts ASM-5391 and current S9 story (NEW-GAP-F08-1). (F08)
51. Nobody publishes GET /customers/{id} used by gateway-bff (NEW-GAP-F08-4, blocker); gateway own-error code table (RD-P1-004 applied to gateway). (F08)
52. P1 decision_record table: RD-P1-020 says none; Architecture v5 gives every service one (NEW-GAP-F08-7). ce_idempotencykey derivation (F08-6). (F08)
53. Consumer write access on retry/DLT topics (Kafka catalog; NEW-GAP-F08-5). Catalog rows for AceIngestCheck in observability (F08-10). (F08)
- Check: staged rwb.decision-record.v1.asyncapi.yaml must carry rwb.decision.DecisionRecorded.v1 (RD-P1-008) – W1 resume. (F08)
54. Authorise contract mismatch: staged RWB-P1-E1016 v3 stories do not send access resolution / case attributes that RWB-P4-E1016-APP needs, expect role/scope values it does not return, and send no Idempotency-Key (platform filter would 400) (NEW-GAP-F09-3, blocker). (F09)
55. Dictionary gate deadlock: RWB-P4-E1064-APP refuses loads naming unknown fields, but RD-P1-025 adds new fields only through such a load (NEW-GAP-F09-5, blocker). (F09)
56. RD-P1-009 row 06 side effect: every decision record with a caseId becomes a ledger entry, so each case-record read adds a "decision taken" contact-history entry (NEW-GAP-F09-4). (F09)
57. RWB-PLT-E1044-CON still publishes migration-run record and job view fake removed by RD-P1-012 – not in any batch; needs edit. Loader identity after SY-DATALOAD retired (NEW-GAP-F09-2). (F09)

## Extra stories to edit (not in the affected list)
- RWB-PLT-E1044-CON (F09: still publishes migration-run record/job view fake removed by RD-P1-012).
- RWB-P3-E2021-APP (F12: still writes the delivery ledger entry; RD-P1-007 makes rwb-comms the only writer).
- RWB-P3-E2016-CON (F12: cites GAP-0716 settled by RD-P1-007).
- RWB-P10-E1062-APP (F10: needs the same ledger-read alignment as its CON).
- rwb-deviation (S8) stories carrying deceased/bankrupt flags off AceDataReady (L01 E7003).
## More mechanical checks
- GAP-3283 cited by staged RWB-P1-E1001-APP and E2010-APP v3 does not exist in Gap Register v3 (E1001 subject = NEW-GAP-F12-1). (F12)
- RWB-P1-E1066-APP: event code outside the list must answer MSG-GEN-007 (RD-P1-004), not MSG-GEN-001. (F12)
58. Build chains up to 6 deep for seven rwb-source-data stories vs limit 4 – cut needed (solution architect). Blocking cycle E1066-OPS <-> E1067-APP recorded as tracked. (W9)
## Finishing pass steps
- Re-run W9 graph after story editing ends: SET\_work\p1-ready\qa\w9-governance\graph.py, then apply.py and fix_bo.py if rows reported.
- Service Contract Catalog section 6.1 to match Service Catalog v2. (W9)
- Extra story to edit: RWB-P6-E2021-CON (still treats proof of delivery as an INT-15 result from rwb-integration; needs the E2021-OPS fix). (F15)
59. Web portal channel and customer facts for the offer view have no published read (NEW-GAP-F15-4, blocks web); failed-append path (NEW-GAP-F15-2). (F15)
- Extra story to edit: RWB-P6-E4036-CON (match E4036-APP changes). (F16)
- Check: staged RWB-P1-E1017-CON v3 cites GAP-3271 for holdReport (GAP-3271 is the job-read gap). (F16)
60. HOME.SCB answer contact channel (NEW-GAP-F16-1, blocker); customer answer ledger entry and ce_actor for a customer (F16-2, F16-3); case number source for hand-recorded proof business key (F16-4). (F16)
61. KEY CROSS-CUTTING: no ruled read gives rwb-comms (and gateway, E1052 ITG) the recipient name and postal address – yaml says DP02 contact rows carry no value/name/address, E1016-APP v3 returns contact_value in clear to unmasked roles, GET /customers/{id} unpublished. Blocks P6 E1007, E1032, E1052 APP/CON, ITG E1052, gateway N001 (NEW-GAP-F13-1 = F02-1 = F08-4 = F15-4). (F13)
62. Never-stamped product: MSG-P1-001 {date} and whether a notice is held (NEW-GAP-F13-2, F13-5; joins item 17). Ledger eventCode for notice timeline entry (F13-6); 409 code on second idempotency key for notices (F13-7). (F13)
63. Dispatch ledger append: contract requires conductCheck when deliveryStatus SENT/absent; no source gives the Epic 1 dispatch value – append refused 422 (NEW-GAP-F14-1). podKey 255 chars vs externalRef 60 (F14-2). (F14)
- Check/fix: messageCode pattern in RD-P1-004 and staged rwb-source-data.yaml ends in -\d{3} and rejects MSG-PLT-N009-03/-05/-06 that the rulings require – widen the pattern (e.g. ^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$) in the yaml and note as register amendment. (W3)
- Stories quoting v5 English of MSG-GEN-006 and MSG-P4-001 must match Error and Message Standard v6. New MSG-P1-023 cutover sign-off text needs standard-owner confirmation. (W3)
- Promotion: remove render folders _qa_final, _qa_final2 (and any other _qa*) from stage before copying into SET. (W3)
- DEFECT to fix after W2: Test Cases v9 overwrote P9 rows TC-E1-013-01..07 and -09 (P9 in v8) with P1 content; only -08 is still P9 – restore P9 rows and give P1 rows new IDs; check for other overwritten IDs v8→v9 across all services. (F19)
64. P9 E1013 not ready: payments by account not served (only by business date), freshness response lacks COMPLETE/HOLD gate field (NEW-GAP-S3-7); measures run data products and snapshot(page) use (NEW-GAP-F19-5, F19-6); rwb-reporting.yaml lacks definitions read and 422. (F19)
65. Litigation: how the delivery fact reaches rwb-litigation (NEW-GAP-F19-4, blocker). (F19)
- Extra story to edit: RWB-ITG-E2034-ITG v3 still expects the listener to write and retry a letter entry (E2034 stories now append nothing for NoticeDispatched/NoticeDelivered). (F18)
66. Notice dispatch ledger entry owner (NEW-GAP-F05-3); PROMISE mapping for promise-to-pay in daily EFS read (F05-4); who appends treatment, partner and payment entries (NEW-GAP-F18-6); account list for daily EFS read (F18-5); shared consumer group owner with hand-over step (F18-7). (F18)
- Register pass 2: do NOT register NEW-GAP-S4-002 (rwb-case.yaml publishes the case-scope read). Replace temp IDs as whole tokens (NEW-GAP-S5-1 vs S5-10). (S4b, S5)
- Extra story to edit: RWB-P4-E1016-APP Pending note about the P1 caller is out of date (P1 E1016 now sends access resolution, case attributes, Idempotency-Key). (S4b)
67. Four ACE reads (customers, accounts, collateral) in no published contract/story (NEW-GAP-S4b-4, blocks those reads); RD-P1-011 asks for fixtures for six reads but only two operations can be faked; guard library 503 has no message ID vs RD-P1-004; rwb-source-data.yaml lacks 422 on records read; rwb-document.yaml lacks retention read. Per-product field lists and case filtering (S4b-7); source of catalog reconciliation list (S4b-8). (S4b)
68. DP04 freshness stamp written twice? source-completion rule (RD-P1-041) and E2010 stampDp04 activity (NEW-GAP-S11-3); E2010 rerun replacement scope, guarantee-error end state, restart before wave 4 (S11-1..6). (S11)
69. Ledger table in Physical Schema v9 has no document_id column though the contract has documentId (NEW-GAP-S8-12, blocker) – W4 follow-up. Service login can still truncate the ledger (S8-8); ledger metric names (S8-9); refusal answers for bad decision-log reference (S8-2); non-rwb-case callers when case not found (S8-7); intake handling of non-transient refusals (S8-11). DM005 as in-process ledger caller – add to RD-P1-007 final ruling. (S8)

## From Decision Register v2 (for re-review)
- XD-11 merged rule (repeated readiness call after a run closes) – confirm with the P1 owner.
- RWB-P7-E1008-OPS (v2) still reruns a failed migration job through rwb-source-data /admin/jobs/{jobId}/rerun – conflicts with RD-P1-012/065.
- JOB-14 chain-check workflow named ChainCheckWorkflow (TE008 stories) vs DecisionChainCheckWorkflow (RWB-P7-E1008-APP).
- CaseListDayOpen workflow ID case-list-{businessDate} does not follow the RD-P1-022 naming rule – rwb-case owner.
- Final check: Batch and Scheduling workbook rows JOB-02 and JOB-07 name v_ace_batch_status as a dependency although rwb-case and rwb-payment read it only through rwb-source-data /batch-status – reword to the contract (ACE boundary). (FD3)
- Test reconciliation after story groups: 168 cited TC IDs in 22 non-P1 stories now hold a different case or are retired in v9 (caused by this run – fix); 484 cited IDs in 64 stories missing in v8 and v9 (pre-existing – NEW-GAP-W2-tests-7). Changed ACs in P1 E2001 (AC19 new), E2007 AC2/AC20, E2021 AC2, E2022 AC4, E2034 AC1 need TC rows. (G3, G5)
- Final check: rwb-comms.yaml declares /notices/{noticeId}/responses twice (duplicate key – a lenient parser drops the POST) – merge into one path item. (G6)
- RD-P1-072 vs E1023 (publishes a decision record per read) and E1039 (access log into decision log) – needs ruling (NEW-GAP-G6-1). (G6)

## After graph re-run (08:50)
- Story Build Order v5 deep-chain paragraph still lists 7 stories; the re-run gives 11 deeper than four (AD018-APP, AD018-OPS, AD019-APP, AD019-OPS, E1011-OPS, E1013-APP, E1017-OPS, E1064-OPS, E1066-OPS, E2008-APP, E2010-OPS; longest 6) – update text (NEW-GAP-D5 stays).
- 12 cross-service APP->APP header dependencies are not allowed (must point at the provider's CON story): P1-E1016-APP->P4-E1016-APP; P1-E1018-APP<->P3-E1018-APP; P6-E1007/E1032/E1052-APP->P1-E1069-APP; P6-E1011/E1055/E2021-APP->P1-E1055-APP; P6-E2021-APP->P1-E2021-APP; P6-E4036-APP->P1-E2022-APP; PLT-E1056-OPS->P1-AD018-APP – fix in re-review (cite the CON story).
