# P1 developer readiness package manifest v1

Updated 27 November 2026 after reconciling G4–G9 finish logs and the RF-tests handoff. D-RCV-60 P1 developer readiness (RD-P1 register).

## Package status

**INCOMPLETE — UNREVIEWED.** This describes the staged working tree at stage/. The user will create the ZIP; none was created. The tree retains its SharePoint-relative folder structure. Task-specific handoff checks are not a final review of the combined package.

## Included staged tree

The staged tree contains 783 files across 15 folders. Counts include this manifest in 24 P1 Developer Readiness v1.

| Staged folder | Files |
|---|---:|
| 01 Decisions and governance | 1 |
| 02 Business architecture and process | 2 |
| 03 Requirements and specifications | 47 |
| 04 User stories | 576 |
| 05 Technical architecture | 102 |
| 06 Data | 29 |
| 07 Screens and experience | 1 |
| 09 Testing and quality | 4 |
| 10 Policy, controls and compliance | 2 |
| 11 Delivery and operations | 2 |
| 14 Story Updates | 1 |
| 15 ACE DB Alignment | 3 |
| 22 Microservice Realignment | 1 |
| 23 Document Gaps | 6 |
| 24 P1 Developer Readiness v1 | 6 |
| Total | 783 |

## Key artifacts and reconciled state

| Staged artifact | Reconciled state |
|---|---|
| 24 P1 Developer Readiness v1 / Decision Register v3 draft (.md and .csv) | 59 rows, latest ID RD-P1-088. RD-P1-089–100 are absent. |
| 24 P1 Developer Readiness v1 / decisions / batch-E recovered draft.csv | 14 recovered draft rulings, RD-P1-075–088; application and verification remain pending. |
| 24 P1 Developer Readiness v1 / P1 re-review baseline v1.csv | 62 story rows. Its 0 Ready / 2 Ready with minor gaps / 60 Not ready verdicts and 658 findings are historical, not current. |
| 09 Testing and quality / Test Cases v9.xlsx | Last saved 27 November 2026 at 13:59:57. RF-tests handoff reports 5,272 rows, 87 edited, 29 retired, no new rows, and 5,002 Live (down from 5,031); it reports 33 of 35 document items addressed and two required no change because already Retired. Earlier targeted checks confirmed TC-P7-E1027-APP-01 (AC13) and TC-P8-E4050-APP-01 (AC16) Live; G7 reports all 94 mapped IDs verified. RF-tests’ last sync dry run was not applied and listed 15 Test Cases rows to add, 19 to update and 17 RTM trace rows to add while story changes were arriving. Remaining G4–G9 requests and full cross-writer reconciliation are pending. Workbook contents were not reopened in this reconciliation. |
| 09 Testing and quality / Requirements Traceability Matrix v9.xlsx | The earlier count of 3,515 unique RTM references and 1,964 Criterion trace references predates later changes. RF-tests handoff reports 23 requirement rows and 8 criterion-trace rows edited, with no retired ID still referenced in RTM. G4–G9 sync items remain, so this is not a final traceability check. |
| 04 User stories / Service Story Files v3 | G4–G9 logs record 465 distinct changed story files: G4 14 source-data DM stories; G5 79 (23 P2, 56 P3); G6 168 P4/P5/P6; G7 65 P7–P10; G8 66 S-services/platform; G9 73 ITG. All 465 changed paths exist after normalizing separators. The G6 log has one combined request-only target string for P6 E4038 APP and CON that is not a literal filename; both corresponding staged stories were changed. |
| 05 Technical architecture / API Specification v7 | Staged API YAMLs include rwb-case.yaml, rwb-source-data.yaml and rwb-comms.yaml. The G6 handoff reports a duplicate /notices/{noticeId}/responses path in rwb-comms.yaml; it remains unmerged. |
| 06 Data / Data Classification and Personal Data Inventory v6.xlsx | Present. FD4 reports adding DF-INT-030 and updating field counts. DF-REF-274–DF-REF-299 remain absent from this classification file, per the handoff. |
| 05 Technical architecture / Service Catalog v2.md and .xlsx | Present. FD4 reports adding GET /parameters/{key} and keeping the payments activity question Pending as GAP-3556. |
| 05 Technical architecture / Technical Specifications by Module v7 / TSD P1 Recovery data engine v6.md | Present. FD4 reports updating eight moved test IDs. The TSD P3 and P6 citation checks remain outstanding. |
| 11 Delivery and operations / Story Build Order v5.docx | Present; predates the E1018 APP to E1069 DB dependency update. GAP-3287 remains Open. |
| 14 Story Updates / Project Hub v19.html | Present; last saved at 09:52, before the latest G4–G9 story updates. Refresh and verify it against the current staged stories. |
| 23 Document Gaps / Gap Register v3.md | Lists GAP-3283, GAP-3287, GAP-3356, GAP-3392–GAP-3400, GAP-3547 and GAP-3556 as Open; GAP-3300 and GAP-3331 are Closed. GAP-3400 remains Open despite the two Live Test Cases v9 rows reported for AC13/AC16; G7 logged the closure request. |
| 24 P1 Developer Readiness v1 / checkpoint v1.md | Updated with this later reconciliation and the current incomplete, unreviewed status. |

## Edit evidence outside stage

These eleven latest reconciliation logs sit beside stage under ../editlog/. They are not included if the user archives stage/ alone. Row counts below are raw log rows, not deduplicated requests.

| Log | Rows | Recorded scope |
|---|---:|---|
| RF-tests.csv | 153 | Handoff reports 87 Test Cases rows edited, 29 retired, 0 new; 23 RTM requirement rows and 8 criterion-trace rows changed; no retired IDs remain referenced. The last sync dry run was not applied and listed 15 Test Cases rows to add, 19 to update and 17 RTM trace rows to add. |
| RF-E-Sol.csv | 22 | Story/API edits, five additional Test Cases cell edits and one Test Cases request. |
| RF-continuation.csv | 30 | E1016 ITG/CON, E1018 APP, API YAML edits and four Test Cases requests. |
| G4-finish.csv | 354 | 14 changed DM001–DM014 story paths, all present. Raw actions: 15 REQUEST-DONE, 9 REQUEST, 9 REQUEST-REJECTED, 1 NEW-GAP and 1 CLOSE-GAP. Handoff reports 128 Test Cases IDs across 140 AC mappings; wording updates routed to the test owner. |
| G5-finish.csv | 765 | 79 unique changed staged story paths. Raw log actions: 46 REQUEST-DONE, 19 REQUEST, 4 REQUEST-REJECTED, 2 NEW-GAP and 2 CLOSE-GAP. Handoff reports 39 requests completed, 4 rejected and 167 mapped Test Cases references verified. |
| G6-finish.csv | 1,646 | 168 changed staged story files; 169 unique story-target strings, with one combined request-only target for P6 E4038 APP and CON that is not a literal filename. Handoff reports all 47 incoming requests disposed (46 completed, 1 rejected), 267 unique Test Cases IDs across 274 story citations, 14 CLOSE-GAP and 3 NEW-GAP actions. Raw log has 46 REQUEST-DONE, 46 REQUEST, 1 REQUEST-REJECTED and 3 NEW-GAP rows. |
| G7-finish.csv | 690 | 65 changed staged story paths, all present; retry handoff reports 65 published citations and all 94 mapped IDs verified. Raw log has 27 REQUEST-DONE rows, 7 REQUEST, 1 REQUEST-REJECTED, 3 NEW-GAP and 1 CLOSE-GAP action. Handoff reports 23 requests completed and 1 rejected. |
| G8-finish.csv | 749 | 66 unique changed staged story paths; handoff reports all 126 backfill rows for 27 stories cited. Raw log has 20 REQUEST-DONE, 9 REQUEST, 1 REQUEST-REJECTED and no new gaps. |
| G9-finish.csv | 714 | 73 changed ITG story paths, all present. Handoff reports 6 requests completed, 0 rejected and 0 new gaps; it verified 307 unique Test Cases IDs across 57 stories and 312 AC mappings. Raw log has 6 REQUEST-DONE, 9 REQUEST and 14 CLOSE-GAP rows. |
| FD3-runtime.csv | 414 | Retry handoff reports 11 staged files checked; 8 rulings plus RD-P1-003/040 amendments; 14 request items accounted (9 completed, 5 rejected); 0 new gaps. Raw log has 12 REQUEST-DONE rows, 5 REQUEST-REJECTED rows and 1 routed REQUEST to an unstaged Decision Register v1 target. |
| FD4-governance.csv | 267 | 21 files touched per handoff; 17 REQUEST-DONE, 1 REQUEST-REJECTED, 2 REQUEST and 2 NEW-GAP actions. |

G4 finished all 14 staged source-data DM stories; its handoff verified 128 Test Cases IDs across 140 AC mappings and routed wording updates to the workbook owner. GAP-3392 remains Open for the unpublished DM012 outbox rows.

The G5 handoff reports 79 stories changed, 39 requests completed, 4 rejected and 17 Test Cases requests for the workbook owner. It verified 167 mapped Test Cases references. Its AC-format scan flagged 53 scenarios missing an explicit Given, When or Then; that format check remains open. The report names workbook Data-cell mismatches TC-P3-E2001-APP-03–05, TC-P3-E2014-APP-01 and TC-P3-E2021-APP-01–03 and says 16 earlier missing-row requests were not rechecked. The five prior requests remain: E1001 APP AC1/AC5; E1016 CON AC2; TC-P1-E1016-CON-02; E1018 APP AC2; and E1016 CON AC11.

G6 retry reports 168 stories changed, 8 Batch D rulings applied, and 47 incoming requests disposed (46 completed, 1 rejected). It verified 267 unique Test Cases IDs across 274 story citations. Test-owner follow-ups remain for the Data cells in TC-P5-E1055-APP-01–04, RTM alignment and unmapped legacy citations. The P6 E4038 APP and CON customer reads were updated to getCustomer; the rwb-comms.yaml duplicate path and P4 E1039 conflict with RD-P1-072 remain unresolved. GAP-3395–GAP-3397 are Open.

G7 retry covers 65 P7–P10 stories and reports 94 mapped test IDs verified. TC-P7-E1027-APP-01 is Live for AC13 and TC-P8-E4050-APP-01 is Live for AC16. GAP-3400 has a CLOSE-GAP action and a separate register request, but remains Open in the current Gap Register. Two gaps remain open: GAP-3398 for the fees_outstanding source and GAP-3399 for permanent REC-04/REC-06 storage. One rejected request leaves snapshot(page) and its fixtures unspecified. The reporting API still needs the interim JOB-15 run endpoint under a contract-owner request. The earlier G7 pass reported 273 stories using wording that permits service-owned ACE-view reads; the retry does not report a cross-service fix. Cross-document requests still need reconciliation.

G8 reports an outstanding request, G8-finish-0747: Test Cases v9 rows TC-E5-001-11 and -12 still have old “to be added” Data text. Some stories also retain Test Cases additions in remaining delivery steps. Its rejected flag-registration request needs an owner ID and removal date.

G9 updated 73 ITG stories, including 18 in its continuation, and reports 307 unique Test Cases IDs across 57 stories and 312 AC mappings. The rwb-comms dispatch decision point and rule remain pending under GAP-3356; DM012 publication remains gated under GAP-3547.

FD3’s latest retry supersedes the earlier runtime handoff. It reports applying 8 Batch D rulings and the RD-P1-003/040 amendments across 11 staged files. It verified that the staged files reopen, version entries and final logged edits are present, and retry/dead-letter grants cover 62 listed consumer-topic pairs. It rendered and reviewed 81 pages across seven Word documents in qa-renders/FD3-runtime, outside stage. The handoff accounts for 14 request items (9 completed, 5 rejected), with no new gaps; MSG-P1-023 remains flagged for owner confirmation. Its separate routed request asks the Decision Register owner to record what the RD-P1-044 reconciliation flags gate; the target named by the log is not staged. The earlier FD3 handoff also raised the rwb-reporting consumer addition against Architecture v5 and missing TreatmentApproved/NoticeDelivered consumer rows; the retry does not say these concerns were settled, so they still need explicit disposition.

FD4 reports GAP-3283 (masking rows) and GAP-3287 (deep build chains) still Pending, and PRD OQ-P1-07 remains open. The DM002 story and Story Catalog disagree on its build dependencies. The payments activity remains Pending under GAP-3556. DF-REF-274–DF-REF-299 are not in Data Classification v6.

G4 reports GAP-3392 Open for unpublished migrated outbox rows. G7 reports GAP-3400 can close because both required cases now exist and are Live, but the Gap Register still marks it Open pending the logged closure. G6 reports GAP-3395 (access-log path), GAP-3396 (phone merge unmasking) and GAP-3397 (PORTAL contact/consent) Open. G5 reports GAP-3393 and GAP-3394 Open; G9 keeps GAP-3356 and GAP-3547 pending.

## Incomplete work

- Complete and verify RD-P1-089–100, then reconcile the complete Batch E decision file and register.
- Reconcile the outstanding Test Cases and RTM requests against the latest G4–G9 story edits. RF-tests applied 87 Test Cases edits and 29 retirements, but its last sync dry run was not applied (15 rows to add, 19 to update, 17 trace rows to add). Resolve G4 test wording routed to the workbook owner, G5 test-data/format findings and earlier 16 missing-row checks, G6 TC-P5-E1055 Data and legacy citation follow-ups, G7 GAP-3400 closure, and G8-finish-0747.
- Resolve or disposition the rejected and owner-dependent items recorded above; close GAP-3400 in the register if its evidence remains valid. Keep GAP-3392–GAP-3400, GAP-3356, GAP-3547 and other listed gaps pending until their owners settle them.
- Route the G4–G9 and FD3/FD4 cross-document requests; resolve the open gaps and architecture/contract mismatches, including the 273-story ACE wording issue reported by G7.
- Refresh and verify Story Build Order v5 and Hub v19 after the latest story edits; complete remaining delivery-only checks.
- Run the post-fix re-review and publish verified readiness counts. No final review or current remaining-finding count is available.

## Reconciliation boundary

This update checked current log row counts, the presence of 465 changed story paths after normalizing separators, staged file totals, key artifact presence, the listed Gap Register statuses, file timestamps and the latest task handoffs. It did not reopen workbook contents, re-review story/document content, or verify every task edit. Task-specific finish checks are not a final review of the full package. No further ruling or implementation edit and no ZIP was created.
