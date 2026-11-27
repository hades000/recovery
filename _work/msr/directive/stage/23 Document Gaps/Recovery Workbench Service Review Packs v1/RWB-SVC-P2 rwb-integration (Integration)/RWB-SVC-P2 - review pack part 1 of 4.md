# RWB-SVC-P2 rwb-integration (Integration) - review pack, part 1 of 4 (RWB-P2-E1007-APP to RWB-P2-E2001-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 169 |
| Cross-document (pending in another document) | 246 |
| Not applied (value not in the sources) | 4 |
| Open business decisions | 18 |
| Register gaps linked | 99 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P2-E1007-APP | 40 | 41 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E1007 APP Integration adapters for outbound files v2.md |
| RWB-P2-E1007-CON | 25 | 47 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E1007 CON Integration adapters for outbound files - contract v2.md |
| RWB-P2-E1007-INF | 20 | 31 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E1007 INF Integration adapters for outbound files - infrastructure v2.md |
| RWB-P2-E1007-OPS | 24 | 35 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E1007 OPS Integration adapters for outbound files - deployment v2.md |
| RWB-P2-E1073-APP | 30 | 35 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v2.md |
| RWB-P2-E2001-APP | 30 | 41 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2001 APP EFS hand-over with full history v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P2-E1007-APP | R-10007 | CG-ALL-2961 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2001-APP | R-10036 | CG-ALL-3025 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2001-APP | R-10038 | CG-ALL-3033 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-P2-E2001-APP | R-10039 | CG-ALL-3034 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-21888 | GAP-1545 | Register gap | Compliance | The debt buyer tape is required to be masked before the data room, and to carry the personal data the sale terms allow | The tape carries only the fields the sale terms and the approved mask list allow, and the mask list is a reference-data row owned by Compliance under DL26; the PRD states the rule and leaves the field list open. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-E2001-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22309 | GAP-0588 | Register gap | Data steward and data product owner, P1 | The collection period of an account's EFS history is named by no source, so the boundary of the history read is undefined | Fix the period as the EFS assignment window of the account: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read for the open assignment; when the account has no assignment row the period opens at its earliest contact_at. Publish the rule in RWB-P2-E2001-CON with the answer so the run and this service read the same boundary, and ask the data steward to confirm it with the ACE team before wave 2 exit. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-28455 | GAP-1548 | Register gap | Compliance | No retention period is set for an outbound item, a delivery record or the transmission evidence of a file | The PRD states the retention of P2 transmission records as open under DL26 with the section R9 placeholder, and requires only that a resend and its audit record outlive the retention period of the case they belong to. |
| RWB-ITG-E1073-ITG, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28681 | GAP-0006 | Register gap | RW-COE and RW-RISK | Rule format XLS decision tables or DMN 1.6 | Keep XLS tables for the Phase 1 packages and convert one table at a time, with both formats on the same runtime |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28693 | GAP-2047 | Register gap | Solution architect with Risk and Internal Audit | The decision log is now written locally by each service and sealed centrally | Version 4 measures the local decision record of each service and the central ledger of P7 rwb-decision as two instances of the same two alerts, with the chain check read per service and once for the ledger. |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28694 | GAP-2051 | Register gap | P7 rwb-decision with Compliance and Internal Audit | The hash chain check now spans 19 local chains and one central ledger | Version 4 raises the alert on the local chain of each service and once on the central ledger, and attributes a break to the service whose chain fails; the run book of RWB-E1-073 and RWB-E2-037 names the check. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-P2-E2001-APP | R-33395 | ASM-ALL-3033 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-P2-E2001-APP | R-33396 | ASM-ALL-3034 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P2-E1007-APP | R-04754 | DOR-RWB-P2-E1007-APP-16 | Header | Definition of Ready item 16 Size: Fail | Header records Size as not specified in the sources. The item stays open until the squad sizes the story at refinement. |
| RWB-P2-E1007-APP | R-15547 | DOR-RWB-P2-E1007-APP-15 | Header | Definition of Ready item 15 INVEST: Partial | No size is in the story or item title. The squad sizes the story at refinement. |
| RWB-P2-E1007-APP | R-15551 | DOR-RWB-P2-E1007-APP-4 | 16 | Definition of Ready item 4 Business rules: Partial | BR11 to BR13 are linked to test cases, but BR14 to BR17 have none, so the item stays open. |
| RWB-P2-E2001-APP | R-04782 | DOR-RWB-P2-E2001-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design for RWB-SVC-P2 or Epic 2 exists in the sources. Grepped all md files; the only sign/approve match is BR-E2-005 in Business Requirements Epic 2 v3, which is not a sign-off. Sign-off cannot be invented. |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04384 | RWB-P2-E1007-APP | GAP-1546 |  | State INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR; record that their behaviour is ACE's. |
| CDC-04385 | RWB-P2-E1007-APP | GAP-1547 |  | State that the partner and document channels keep their own contracts (rwb-partner, rwb-document) and that P2 carries no requirement for them; record the FSD transport sentence as superseded. |
| CDC-04416 | RWB-P2-E1007-CON | GAP-1536 | Header | Name the owning service of JOB-10 (P6 rwb-comms), JOB-13 (P7 rwb-decision) and JOB-15 (P9 rwb-reporting) per the Ownership Map; state that rwb-integration registers no Temporal Schedule and provides the delivery capability. |
| CDC-04417 | RWB-P2-E1007-CON | GAP-1537 | Header | State that the bank scheduler owns the window, its opening time and its re-run; the service owns the attempt ladder inside the window, the exception state and the owner task; the single retry-count owner is left to DL11. |
| CDC-04418 | RWB-P2-E1007-CON | GAP-1544 | Header | Inherit the programme targets for every service; state interface-level file size, throughput, window length and daily volume as Not specified in the source documents (GAP-1544), open under DL11 with the Template and Rules R9 placeholder. |
| CDC-04451 | RWB-P2-E1007-INF | GAP-1536 |  | Name the owning service of JOB-10 (P6 rwb-comms), JOB-13 (P7 rwb-decision) and JOB-15 (P9 rwb-reporting) per the Ownership Map, and state that rwb-integration registers no Temporal Schedule and provides the delivery capability the owning service calls. |
| CDC-04452 | RWB-P2-E1007-INF | GAP-1537 |  | State that the window, its opening time and any re-run belong to the bank scheduler; that the attempt ladder, exception state and owner task belong to the service; and leave the single owner of the retry count to DL11. |
| CDC-04453 | RWB-P2-E1007-INF | GAP-1544 |  | Inherit the programme targets that apply to every service and state the interface-level file size, throughput, window length and volume targets as open under DL11, with the §R9 placeholder. |
| CDC-04462 | RWB-P2-E1007-INF | GAP-1542 |  | FSD: keep removed IDs in an exclusion table with later home ACE ingestion, no FR, NFR or AC. PRD: state that no inbound adapter, folder, run or sign-off exists. |
| CDC-04463 | RWB-P2-E1007-INF | GAP-1546 |  | State INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR, and record that their behaviour is ACE's. |
| CDC-04464 | RWB-P2-E1007-INF | GAP-1547 |  | State that partner and document channels keep their own contracts with rwb-partner and rwb-document and carry no P2 requirement. Record the FSD transport sentence as superseded. |
| CDC-04486 | RWB-P2-E1007-OPS | GAP-1537 | n/a | The retry owner split is a PRD statement; the change belongs to that document. |
| CDC-04487 | RWB-P2-E1007-OPS | GAP-1544 | - | Inherit programme NFR targets for every service and state interface-level file size, throughput, window length and volume as open under DL11 with the Template and Rules R9 placeholder. |
| CDC-04497 | RWB-P2-E1007-OPS | GAP-1542 | 8 | Move the removed rows to an explicit exclusion table with later home ACE ingestion and no FR, NFR or AC. PRD states no inbound adapter, folder, run or sign-off exists. BR12 already aligned. |
| CDC-04498 | RWB-P2-E1007-OPS | GAP-1546 | 7 | Record INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR, and state that their behaviour is ACE's. |
| CDC-20495 | RWB-P2-E1007-INF | R-28453 |  | From story RWB-P2-E1007-APP. Sections 2.3 and 9 already state INT-17, INT-18 and INT-22 as ACE common module, no P2 build, no FR (ASM-2674). |
| CDC-20496 | RWB-P2-E1007-INF | R-28452 |  | From story RWB-P2-E1007-INF. PRD already states no inbound adapter, folder, run or sign-off (2.3, 2.5, FR-P2-016). FSD exclusion table belongs to FSD P2 v3. |
| CDC-20497 | RWB-P2-E1007-INF | R-28453 |  | From story RWB-P2-E1007-INF. Same as APP item: INT-17, INT-18, INT-22 as ACE common module with no P2 build (2.3, 9). |

### RWB-P2-E1007-CON (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04355 | RWB-P2-E1007-APP | DOR-RWB-P2-E1007-APP-21 | Header | Take the build status from Not started to Done so the contract is published before this story starts. |
| CDC-04356 | RWB-P2-E1007-APP | DOR-RWB-P2-E1007-APP-22 | Header | Header records the fake library version as not specified. Publishing the fake is delivery work outside this story. |
| CDC-04369 | RWB-P2-E1007-APP | GAP-0334 | 12.6 | Fix the deliverFile manifest schema, the claim-check handoff and the two window calls at P2 contract review, and publish them in the activity contract jar and AsyncAPI before the first SIT run of this path. |
| CDC-04371 | RWB-P2-E1007-APP | GAP-0648 |  | Fix the manifest fields, return element and three typed failures; re-confirm with rwb-comms, rwb-payment, rwb-debtsale, rwb-reporting; fix notice-fact read in rwb-comms contract; publish one RFC 9457 body with six status codes; fix OpenAPI JSON names; fix registry subject and compatibility level with the platform event owner. |
| CDC-04373 | RWB-P2-E1007-APP | GAP-0739 |  | Keep the seam: outcomes and admin item from RWB-P2-E1007-CON; route state to resume from latest decision-record entry; task code and due date as reference rows of rwb-case; legacy in-process interfaces internal to the listener; lake extracts dropped under DP-17 with reporting reading rwb.case.events.v1. |
| CDC-04436 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-21 | Header | Move build status from Not started to Done so the contract is published |
| CDC-04437 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-22 | Header | Publish a contract fake library version and record it |
| CDC-04444 | RWB-P2-E1007-INF | GAP-0334 | find it | Fix the deliverFile manifest schema, the claim-check handoff and the WIN 16:00 and buyer-per-lot window calls; publish them in the activity contract jar and AsyncAPI before the first SIT run. |
| CDC-04447 | RWB-P2-E1007-INF | GAP-0648 | find it | Fix the deliverFile manifest and return, the rwb-comms notice-fact read, one RFC 9457 problem body for the four admin operations, JSON names, registry subject and compatibility level. |
| CDC-04454 | RWB-P2-E1007-INF | GAP-2229 |  | At contract review, confirm the element names of rwb.integration.FileFailed.v1 and rwb.integration.FileDelivered.v1, the carrier of the route state to resume, and the task code and due date values, plus the rwb-case parameter and reference loads and the LDM. |
| CDC-04468 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-21 | n/a | Move build status from Not started to Done so the contract is published. |
| CDC-04469 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-22 | n/a | Publish a contract fake library version and record it as published. |
| CDC-04479 | RWB-P2-E1007-OPS | GAP-0334 |  | Define the deliverFile manifest schema, the claim-check handoff and the two window calls; publish in the activity contract jar and AsyncAPI before the first SIT run. |
| CDC-04482 | RWB-P2-E1007-OPS | GAP-0648 |  | Fix the deliverFile manifest and return with three typed failures; fix the notice-fact read in the rwb-comms contract; publish one RFC 9457 problem body and fix JSON names and event subject in OpenAPI. |
| CDC-04483 | RWB-P2-E1007-OPS | GAP-0739 |  | Read the two outcomes and the admin item from RWB-P2-E1007-CON; read the route state to resume from the latest decision-record entry; hold task code and due date as rwb-case reference rows. |
| CDC-04488 | RWB-P2-E1007-OPS | GAP-2229 | - | Confirm rwb.integration.FileFailed.v1 and FileDelivered.v1 payload elements, the resume-state carrier, and the task code and due date rule; rename here at contract review if they differ. |
| CDC-04492 | RWB-P2-E1007-OPS | GAP-1027 | n/a | Field names and type row belong to the contract and type table; no edit to this story text. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04361 | RWB-P2-E1007-APP | CG-ALL-2949 | 12.5 | Add an Activities row for deliverFile(manifest) on task queue rwb-integration. |
| CDC-04362 | RWB-P2-E1007-APP | CG-ALL-2951 | 12.5 | Add an Activities row for buildOutboundFile on task queue rwb-integration. |
| CDC-04363 | RWB-P2-E1007-APP | CG-ALL-2952 | 12.5 | Add an Activities row for storeOutboundFile on task queue rwb-integration. |
| CDC-04364 | RWB-P2-E1007-APP | CG-ALL-2953 | 12.5 | Add an Activities row for sendFileOverMft on task queue rwb-integration. |
| CDC-04365 | RWB-P2-E1007-APP | CG-ALL-2954 | 12.5 | Add an Activities row for parkItemInException on task queue rwb-integration. |
| CDC-04401 | RWB-P2-E1007-CON | CG-ALL-2979 | 12.5 | Add activity sendFileOverMft to the Activities sheet, or name a catalogued activity in the 12.5 row for sendFileOverMft. |
| CDC-04402 | RWB-P2-E1007-CON | CG-ALL-2980 | 12.5 | Add activity parkItemInException to the Activities sheet, or name a catalogued activity in the 12.5 row for parkItemInException. |
| CDC-04536 | RWB-P2-E2001-APP | CG-ALL-3011 | 12.5 | Add workflow EfsHandoverWorkflow to the Workflows sheet, or name the catalogued workflow the story should use. |
| CDC-04539 | RWB-P2-E2001-APP | DOR-RWB-P2-E2001-APP-8 | 12.5 | Add EfsHandoverWorkflow, acceptAceDataReady, readFreshness and listCandidates, plus the five further names flagged by detcheck, to the Workflows and Activities sheets. |
| CDC-04542 | RWB-P2-E2001-APP | CG-ALL-3012 | 12.5 | Add activity acceptAceDataReady (task queue rwb-integration) to the Activities sheet, or use a catalogued activity. |
| CDC-04543 | RWB-P2-E2001-APP | CG-ALL-3013 | 12.5 | Add activity readFreshness to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |
| CDC-04544 | RWB-P2-E2001-APP | CG-ALL-3014 | 12.5 | Add activity listCandidates to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |
| CDC-04545 | RWB-P2-E2001-APP | CG-ALL-3015 | 12.5 | Add activity buildGroups to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |
| CDC-04546 | RWB-P2-E2001-APP | CG-ALL-3016 | 12.5 | Add activity createOrLinkCase to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |
| CDC-04547 | RWB-P2-E2001-APP | CG-ALL-3017 | 12.5 | Add activity appendEfsHistory to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |
| CDC-04548 | RWB-P2-E2001-APP | CG-ALL-3018 | 12.5 | Add activity writeRunSummary to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |
| CDC-04549 | RWB-P2-E2001-APP | CG-ALL-3019 | 12.5 | Add activity recordRunDecision to the Activities sheet, or name a catalogued activity in RWB-P2-E2001-APP §12.5. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04370 | RWB-P2-E1007-APP | GAP-0338 | 7 | Update the P2 Integration row of the connection matrix (slide 13) to show its read path to rwb-source-data and the FileFailed edge into rwb-case, or pass figures in the manifest. |
| CDC-04408 | RWB-P2-E1007-CON | GAP-0338 |  | Update the P2 Integration row of the connection matrix (slide 13) to show its read path to rwb-source-data and the FileFailed edge into rwb-case. |
| CDC-04420 | RWB-P2-E1007-CON | GAP-1396 | Header | Fix the Airflow product, tenancy, scheduler principal, timeout and retry values, DailyCaseRun wait mechanism and the file-window operation paths at the scheduling design review; unset values Not specified in the source documents (GAP-1396). |
| CDC-04445 | RWB-P2-E1007-INF | GAP-0338 | find it | Update the P2 Integration row of the slide 13 connection matrix to show the read path to rwb-source-data and the FileFailed edge into rwb-case. |
| CDC-04456 | RWB-P2-E1007-INF | GAP-1396 |  | Publish the Airflow product, tenancy, DAG names, scheduler identity, timeout and retry values, DailyCaseRun wait mechanism and three owner operation paths before the first SIT chain run. |
| CDC-04480 | RWB-P2-E1007-OPS | GAP-0338 |  | Update the P2 Integration row to show its read path to rwb-source-data and the FileFailed edge into rwb-case, or pass figures in the manifest. |
| CDC-04490 | RWB-P2-E1007-OPS | GAP-0649 | - | Provide per environment: the two outbound endpoints, accounts, folders, receiver ranges, PGP key identifiers, staging names, size, timeout and concurrency budgets, and the rotation period in the key-rotation runbook. |
| CDC-04517 | RWB-P2-E1073-APP | GAP-1216 | 2 | Publish one row per package with owning service, version labels and target queues, including the rwb-comms and rwb-integration assignments, before the wave-1 build. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20518 | RWB-P2-E1007-CON | R-28452 |  | A1.6 exclusion table already lists every removed ID with later home ACE ingestion; A2.4 holds them as removed with no live FR, NFR or AC. PRD part is elsewhere. |
| CDC-20519 | RWB-P2-E1007-CON | R-21873 |  | This FSD has no INT-03 ALS booking row. Supersession and ALS interface_config belong in TSD P2 Integration T1 and T5.1 and the Service Contract Catalog. |
| CDC-20521 | RWB-P2-E1007-CON | R-28452 |  | A1.6 exclusion table already lists the removed IDs with later home ACE ingestion; no FR, NFR or AC is live. PRD statement is elsewhere. |
| CDC-20522 | RWB-P2-E1007-CON | R-21873 |  | This FSD has no INT-03 ALS booking row. Supersession and ALS interface_config belong in TSD P2 Integration T1 and T5.1 and the Service Contract Catalog. |
| CDC-20523 | RWB-P2-E1007-CON | R-28452 |  | A1.6 exclusion table already lists the removed IDs with later home ACE ingestion; no FR, NFR or AC is live. PRD statement is elsewhere. |
| CDC-20524 | RWB-P2-E1007-CON | R-28454 |  | This FSD has no partner portal or document hub transport sentence and carries no requirement for either. Nothing to mark superseded. |
| CDC-20562 | RWB-P2-E1007-OPS | R-28454 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04347 | RWB-P2-E1007-APP | CG-ALL-2940 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness through the provider's CON story (RWB-P1 rwb-source-data), or the consumer uses a published operation. |
| CDC-04348 | RWB-P2-E1007-APP | CG-ALL-2941 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} through the provider's CON story, or the consumer uses a published operation. |
| CDC-04349 | RWB-P2-E1007-APP | CG-ALL-2942 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the provider's CON story, or the consumer uses a published operation. |
| CDC-04388 | RWB-P2-E1007-CON | CG-ALL-2969 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness in rwb-source-data.yaml, or the consumer uses a published operation. |
| CDC-04389 | RWB-P2-E1007-CON | CG-ALL-2970 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} in rwb-source-data.yaml, or the consumer uses a published operation. |
| CDC-04390 | RWB-P2-E1007-CON | CG-ALL-2971 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data.yaml, or the consumer uses a published operation. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04358 | RWB-P2-E1007-APP | CG-ALL-2946 | 12.3 | Specify the payload of rwb.integration.FileDelivered.v1 (gap-0127; asm-0204), then align section 12.3 of this story to it. |
| CDC-04359 | RWB-P2-E1007-APP | CG-ALL-2947 | 12.3 | Add the payload fields fileId, interfaceId, businessDate, attemptCount, lastError code, caseIds and ownerRole to the Events row of rwb.integration.FileFailed.v1. |
| CDC-04360 | RWB-P2-E1007-APP | CG-ALL-2948 | 12.4 | Add rwb-integration as a consumer of rwb.source-data.AceDataReady.v1 (EV-26) and grant it the matching ACL. |
| CDC-04506 | RWB-P2-E1073-APP | DOR-RWB-P2-E1073-APP-8 | 12.4 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} in the rwb-decision API yaml; correct the P1 DecisionRecorded event name to the catalog name; add rwb-integration as consumer of RulePackageInForce.v1. |
| CDC-04508 | RWB-P2-E1073-APP | CG-ALL-3000 | 12.4 | Add rwb-integration as a consumer of rwb.decision.RulePackageInForce.v1 (Events row EV-30) and its ACL. |
| CDC-04521 | RWB-P2-E1073-APP | GAP-2459 | 2 | Name the announcement rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1, keyed by package code, carrying package code, version label, in-force time and SHA-256; map it to the free identifier of EV-08, EV-09 and EV-30. |

### RWB-P2-E2001-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04537 | RWB-P2-E2001-APP | DOR-RWB-P2-E2001-APP-21 | header | Publish the contract and set its build status from Not started to Done. |
| CDC-04538 | RWB-P2-E2001-APP | DOR-RWB-P2-E2001-APP-22 | header | Record the published contract fake library version. |
| CDC-04555 | RWB-P2-E2001-APP | GAP-0590 | 5 | X1 names both counts; key format left Not specified in the source documents |
| CDC-04556 | RWB-P2-E2001-APP | GAP-0592 | 12.2 | Publish GET /entry-candidates (RWB-P1-E1018-APP) and GET /entry-candidate-facts; correct the per-candidate customer read wording at the next version. |
| CDC-04562 | RWB-P2-E2001-APP | GAP-2259 | 12.2 | Publish the candidate page and EFS history page; rwb-source-data stories publish the ledger append, REC-05 break and REC-01 result; then this story names those paths. |
| CDC-04572 | RWB-P2-E2001-APP | GAP-0589 | 4 | Record one account and one business date per call with a configured row cap and no page parameter; a held read answers 409 with a problem body naming MSG-P1-001 and the load date; same in the API Specification. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04367 | RWB-P2-E1007-APP | GAP-0673 | none | Mark INT-03 lines of FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 superseded for legacy key RWB-E4-046 with date and decision; load agreed ALS interface as one versioned interface_config row per environment. |
| CDC-04442 | RWB-P2-E1007-INF | GAP-0673 | find it | Mark the FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 INT-03 lines superseded for the legacy key; load the agreed ALS interface_config row per environment. |
| CDC-04477 | RWB-P2-E1007-OPS | GAP-0673 |  | Mark the FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 INT-03 lines superseded for legacy key RWB-E1-007 with date and decision; load one versioned ALS interface_config row per environment. |
| CDC-04524 | RWB-P2-E1073-APP | GAP-0672 | 3 | Record the eight DP H rows as wave-0 prerequisites; publish the model fetch path, request and response in RWB-P7-E1073-CON; name the rwb_integration login; fix the local copy table in the DB story. |
| CDC-04558 | RWB-P2-E2001-APP | GAP-0651 |  | Record DP-05 and ADR-010 as superseding TSD P2 v3 T5.2 and the P2 inbound exclusion; keep the split recorded by RWB-ITG-E2001-ITG and the Ownership Map. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04378 | RWB-P2-E1007-APP | CG-ALL-2958 | 16 | Covers cells realigned; AC5 and AC6 now have no §16 row |
| CDC-04426 | RWB-P2-E1007-CON | CG-ALL-2984 | 16 | Add rows TC-P2-E1007-CON-01 to TC-P2-E1007-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-04440 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-12 | 16 | Add test case rows TC-P2-E1007-INF-01 to TC-P2-E1007-INF-06 from section 16 of this story to Test Cases v8. |
| CDC-04458 | RWB-P2-E1007-INF | CG-ALL-2987 | 16 | Add story test case rows TC-P2-E1007-INF-01 to TC-P2-E1007-INF-06, with Given, When and Then copied from the criteria they cover. |
| CDC-04493 | RWB-P2-E1007-OPS | CG-ALL-2993 | 16 | Add rows for TC-P2-E1007-OPS-01 to TC-P2-E1007-OPS-06 with Given, When and Then copied from the criteria they cover. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04461 | RWB-P2-E1007-INF | GAP-1538 |  | Add two Events sheet rows for FileDelivered and FileFailed: producer rwb-integration, topic rwb.integration.events.v1, consumer requesting service, keyed by case ID, with no numbered EV ID. |
| CDC-04496 | RWB-P2-E1007-OPS | GAP-1538 | n/a | The event register belongs to the Ownership Map. |
| CDC-04507 | RWB-P2-E1073-APP | GAP-1329 | 12.2 | Fix one registry path family (API Spec v4 /admin/rule-versions) in the spec and Ownership Map, and publish GET /rule-catalog as an owned operation or remove it from the consumed set. |
| CDC-04513 | RWB-P2-E1073-APP | GAP-0383 | 12 | At wave-1 contract review, assign one package code and version label to rwb-integration; add GET /rule-models/{packageCode}/{versionLabel} under P7 rwb-decision with the checksum; publish the refused load in the rwb-decision message catalogue as MSG-P3-027 with its {check} values. |
| CDC-04515 | RWB-P2-E1073-APP | GAP-0700 | 12 | Add the seven rwb-decision operations (load, version list, approve, rollback, dry run, model read, catalog read) to the P7 rows with rights, answers, error codes, and the element names and property types of both reads. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04353 | RWB-P2-E1007-APP | CG-ALL-2950 | 12.5 | Add a Workflows row for OutboundFileWorkflow (service rwb-integration, task queue rwb-integration, workflow ID <interfaceId>:<businessDate>), or name the catalogued workflow to use. |
| CDC-04394 | RWB-P2-E1007-CON | CG-ALL-2976 | 12.5 | Add a Workflows row for OutboundFileWorkflow (workflow ID <interfaceId>:<businessDate>, task queue rwb-integration), or name a catalogued workflow. |
| CDC-04466 | RWB-P2-E1007-OPS | CG-ALL-2990 | 12.5 | Add row: OutboundFileWorkflow; owner P2; service and queue rwb-integration; workflow ID <interfaceId>:<businessDate>; started by deliverFile(manifest); builds, stores, sends, retries, reports one file. |
| CDC-04470 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-8 | 12.5 | Add the OutboundFileWorkflow row described under CG-ALL-2990, then rerun the Definition of Ready item 8 check. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04354 | RWB-P2-E1007-APP | DOR-RWB-P2-E1007-APP-14 |  | Record the signed EP01 epic design sign-off, which DoR item 14 requires before build starts. No signed EP01 design is in the sources; DT05 only states the rule. |
| CDC-04435 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-14 | Header | Record the signed epic design sign-off for RWB-P2-E1007-INF |
| CDC-04467 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-14 | n/a | Record the signed epic design sign-off for RWB-P2-E1007-OPS; none is recorded in the story or source documents. |
| CDC-04503 | RWB-P2-E1073-APP | DOR-RWB-P2-E1073-APP-14 | header | Record the signed epic design sign-off that covers this story. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04366 | RWB-P2-E1007-APP | DOR-RWB-P2-E1007-APP-9 | 14 | §14 takes Standard v4 wording for MSG-P1-001 and MSG-P2-001. The MSG-P4-003 difference remains open (CG-ALL-2957). |
| CDC-04377 | RWB-P2-E1007-APP | CG-ALL-2957 | 14 | Add a new message ID for an unknown outbound item or delivery, English 'This record was not found.', then point this story's section 14 row and its uses at that ID. |
| CDC-04550 | RWB-P2-E2001-APP | CG-ALL-3022 | 4, 14 | Add a new message ID for 'A source contract did not answer inside the budget' with the story's text; RWB-P2-E2001-APP §14 then cites it. |
| CDC-04552 | RWB-P2-E2001-APP | DOR-RWB-P2-E2001-APP-9 | 14 | Section 14 now uses the v4 text for MSG-P1-001 and MSG-P2-006. The other use of MSG-GEN-006 (CG-ALL-3022) still needs a new ID from the standard. |

### RWB-PLT-TE006-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04368 | RWB-P2-E1007-APP | GAP-1416 |  | Fix the library contract: one published artifact with a major version, three interfaces with exceptions, DDL of four tables incl. processed_event and idempotency_key columns, CloudEvents 1.0 attributes with caseId and ce_type, inbox dedupe rule, retry ladder 1 min/10 min/1 h, dead-letter topic with one alert and replay tool, case-step events, task and decision record stay with owning service. |
| CDC-04407 | RWB-P2-E1007-CON | GAP-1416 |  | Fix one published artifact with a major version, the three interfaces and their exceptions, the four-table DDL including processed_event and idempotency_key columns, CloudEvents 1.0 attributes with caseId and ce_type, the inbox dedupe rule, retry ladder 1 min/10 min/1 h, dead-letter topic with one alert and replay tool, and ownership of case-step, task and decision events. |
| CDC-04443 | RWB-P2-E1007-INF | GAP-1416 | find it | Fix the library contract: one versioned artifact, three interfaces with exceptions, four-table DDL with processed_event and idempotency_key columns, CloudEvents attributes, retry ladder, dead-letter topic. |
| CDC-04478 | RWB-P2-E1007-OPS | GAP-1416 |  | Fix the library contract: one artifact with major version, three interfaces, DDL of four tables with processed_event and idempotency_key columns, CloudEvents 1.0 attributes, retry ladder and dead-letter topic. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04379 | RWB-P2-E1007-APP | CG-ALL-2960 | 18 | §18 test lists are not aligned to RTM v7 under this item; the full RTM lists are not readable in the evidence. |
| CDC-04427 | RWB-P2-E1007-CON | CG-ALL-2985 | 18 | Align the test traces of REQ-DRI-006, REQ-DRI-007 and the third differing requirement with section 18 of this story. |
| CDC-04494 | RWB-P2-E1007-OPS | CG-ALL-2994 | 18 | Align the REQ-DRI-006 and REQ-DRI-007 test lists in RTM v7 and section 18 of this story in their next versions. |
| CDC-04570 | RWB-P2-E2001-APP | CG-ALL-3024 | 18 | Align the test lists of the four requirements with RWB-P2-E2001-APP section 18 in the next RTM version. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04403 | RWB-P2-E1007-CON | DOR-RWB-P2-E1007-CON-1 | 1 | Confirm a role code or name for the section 1 persona of RWB-P2-E1007-CON; 'tech lead' is not in v5. |
| CDC-04438 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-1 | 1 | Register the role 'infrastructure engineer' with a role code, or map the §1 role to an existing role in the document |
| CDC-04474 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-1 | 1 | Add platform engineer as a role code or role name, or confirm the role code that the section 1 role maps to. |
| CDC-04509 | RWB-P2-E1073-APP | DOR-RWB-P2-E1073-APP-1 | 1 | Add a role code and name for the rwb-integration service identity (the rules step of an interface run), or name the existing role that matches it. |

### OTHER:Interface configuration version in force; RWB-P4-AD008-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04380 | RWB-P2-E1007-APP | GAP-0981 | find it | Register the access-review file as one OUTBOUND interface row; publish its extract layout, recipient and review-cycle date convention with RWB-P4-AD008-APP. |
| CDC-04428 | RWB-P2-E1007-CON | GAP-0981 |  | Register one OUTBOUND interface row for the access-review file with interface ID, file pattern, data product, owner role and alert role. Publish the extract layout, recipient and review-cycle date convention. |
| CDC-04495 | RWB-P2-E1007-OPS | GAP-0981 | n/a | The story reads these values at run time, so the build is not blocked. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04398 | RWB-P2-E1007-CON | CG-ALL-2975 | 12.5 | Add activity deliverFile(manifest), task queue rwb-integration, provided by P2. |
| CDC-04399 | RWB-P2-E1007-CON | CG-ALL-2977 | 12.5 | Add activity buildOutboundFile, task queue rwb-integration, provided by P2. |
| CDC-04400 | RWB-P2-E1007-CON | CG-ALL-2978 | 12.5 | Add activity storeOutboundFile, task queue rwb-integration, provided by P2. |

### OTHER:TSD P2 Integration v3 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04409 | RWB-P2-E1007-CON | GAP-0647 |  | Record that wording in T1.1, T5.2 and T6.2 giving P2 direct reads of recovery.v_ace_* is superseded by Architecture v5 slide 9 and ADR-010; every ACE fact goes through rwb-source-data. |
| CDC-04446 | RWB-P2-E1007-INF | GAP-0647 | find it | Record that the direct-view wording in T1.1, T5.2 and T6.2 is superseded by Architecture v5 slide 9 and ADR-010, and apply the remaining lake and INT-25 source fixes from the proposed fix. |
| CDC-04481 | RWB-P2-E1007-OPS | GAP-0647 |  | Mark T1.1, T5.2 and T6.2 direct-view wording superseded by Architecture v5 and ADR-010; every ACE fact is one REST call to rwb-source-data with 2 s timeout. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04473 | RWB-P2-E1007-OPS | CG-ALL-2989 | 12.7 | Record decision_record as the PLT library table in rwb_integration (a library object, not a field), or use the dictionary name for it. |
| CDC-04523 | RWB-P2-E1073-APP | GAP-2457 |  | Give the physical columns, types and nullability of rule_package, rule_package_version, rule_row and rule_test_case on the legacy DF-REF field names; confirm artifact columns with RWB-PLT-E1072-CON. |
| CDC-04541 | RWB-P2-E2001-APP | CG-ALL-3010 | 11, 12.7, 13 | Record decision_record as a library table in rwb_integration (PLT library) in the owning data model, or use the dictionary name. |

### OTHER:Recovery Workbench Service Story Files v1 (service story folder) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04502 | RWB-P2-E1073-APP | CG-ALL-2998 | 13 | Create story file RWB-P7-E1073-CON as the rwb-decision contract, or name an existing contract story in the dependency rows. |
| CDC-04504 | RWB-P2-E1073-APP | DOR-RWB-P2-E1073-APP-17 | 13 | Create story RWB-P7-E1073-CON or name an existing contract story as the dependency. |
| CDC-04505 | RWB-P2-E1073-APP | DOR-RWB-P2-E1073-APP-21 | 13 | Publish the contract story RWB-P7-E1073-CON (rwb-decision contract) so the CON dependency is published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04350 | RWB-P2-E1007-APP | CG-ALL-2943 | 12.2 | Publish POST /api/recovery/document/v1/documents alongside the existing GET through the provider's CON story, or the consumer uses a published operation. |
| CDC-04391 | RWB-P2-E1007-CON | CG-ALL-2972 | 12.2 | Publish POST /api/recovery/document/v1/documents in rwb-document.yaml, or the consumer uses a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04351 | RWB-P2-E1007-APP | CG-ALL-2944 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions through the provider's CON story, or the consumer uses a published operation. |
| CDC-04392 | RWB-P2-E1007-CON | CG-ALL-2973 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions in rwb-case.yaml, or the consumer uses a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04352 | RWB-P2-E1007-APP | CG-ALL-2945 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer uses a published operation. |
| CDC-04393 | RWB-P2-E1007-CON | CG-ALL-2974 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml, or the consumer uses a published operation. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04386 | RWB-P2-E1007-APP | GAP-2230 | 8 | BR11 cites ASM-B2-P3-013-4. The missing case operation has to be settled in the case contract; the §12.2 row is left as is. |
| CDC-04520 | RWB-P2-E1073-APP | GAP-2458 | 11 | Add a paged open-case fact read filtered by status, with the fields product group, queue, region, exposure band and deviation flag; the dry run uses it under RWB-P3-E1073-CON with the 2 s one-hop timeout. |

### OTHER:Legacy dependency trace sheet and Story dependencies v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04387 | RWB-P2-E1007-APP | GAP-3233 |  | Keep the five version 4 dependencies visible as Not carried; add an X row only if the run books or the harness really wait for the named story. |
| CDC-04465 | RWB-P2-E1007-INF | GAP-3233 |  | Keep the five version 4 rows visible as Not carried. Add an X row only if the run books or the harness wait on the named story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04405 | RWB-P2-E1007-CON | DOR-RWB-P2-E1007-CON-12 | 12.7, 16, 18 | Add TC-P2-E1007-CON-01 to -06 to Test Cases v8; align the section 18 test lists of RWB-P2-E1007-CON with RTM v7. |
| CDC-04476 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-12 | 12, 12.7, 16, 18 | Add TC-P2-E1007-OPS-01 to -09 to Test Cases v8; align the section 18 test lists with RTM v7. |

### OTHER:rwb-source-data contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04413 | RWB-P2-E1007-CON | GAP-1162 |  | Add a read returning the postal addressee by party_id with a 2 s budget and a fake; keep the value out of rwb_comms, events and logs. |
| CDC-04484 | RWB-P2-E1007-OPS | GAP-1162 |  | Add one read returning the postal addressee by party_id, with a 2 s budget and a fake; keep the value out of rwb_comms, events and logs. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04419 | RWB-P2-E1007-CON | GAP-0649 | Header | Add environment keys for outbound endpoints, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period, owned by SCB IT infrastructure; values Not specified in the source documents (GAP-0649). |
| CDC-04533 | RWB-P2-E1073-APP | GAP-2460 | none | Register rules.testcases.min with value 50 in the parameter catalogue of rwb-case. Confirm with RW-COE at the first package load. |

### OTHER:Legacy dependency trace sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04434 | RWB-P2-E1007-CON | GAP-3233 | find it | Keep the five Not carried rows visible: RWB-E1-056 to RWB-E1-007, RWB-E1-056 to RWB-E1-015, RWB-E1-056 to RWB-E1-069, RWB-TE-009 to RWB-TE-004, RWB-TE-010 to RWB-TE-003. Add an X row later only if confirmed. |
| CDC-04500 | RWB-P2-E1007-OPS | GAP-3233 | 1 | Keep the five dependency rows visible as Not carried. Add an X row only if the run books or harness later need the named story. |

### RWB-P2-E1007-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04449 | RWB-P2-E1007-INF | GAP-0739 |  | Hold the case-side seam: outcomes and admin item from RWB-P2-E1007-CON, resume state from the latest decision-record entry, task code and due date as rwb-case reference rows, no new path. |
| CDC-04450 | RWB-P2-E1007-INF | GAP-1166 |  | Run state from dispatch fields, workflow run and P2 contract status, no run table; one read and one rerun; right enforced at gateway-bff; confirm local guard with edge owner. |

### RWB-P3-E1073-INF (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04516 | RWB-P2-E1073-APP | GAP-0701 | 13 | Record heap request, heap limit and KieBase cache bound of 20 per environment as reviewed values after a load test that holds the bound and evaluates under load; confirm with the platform owner before wave 1 release. Keep the evaluated copy in memory only. |
| CDC-04529 | RWB-P2-E1073-APP | GAP-0702 | none | Record readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed values per environment. Confirm them at SIT with the platform and security owners. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04534 | RWB-P2-E1073-APP | GAP-2461 | none | Record the move of the five rule-package operations and the package list from the access module to rwb-decision (P7), per the Ownership Map. |
| CDC-04565 | RWB-P2-E2001-APP | GAP-2466 | 4 | Record the move of the EFS history append from recovery.decision.api to the rwb-source-data interaction ledger under DP-18; history items stay on the P7 entry as evidence. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04575 | RWB-P2-E2001-APP | GAP-2468 | n/a | Carry RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON and RWB-P7-E2005-CON as H rows; keep lane L-P2-A at Day 1. |
| CDC-04576 | RWB-P2-E2001-APP | GAP-1335 | n/a | Show the six platform contracts and RWB-P3-E1042-CON and RWB-P3-E1043-CON in the wave 2 dependency map; keep this story's metadata rows as fixed. |

### 06 Data/Recovery Workbench Source to Target Mapping v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20514 | RWB-P2-E1007-INF | R-28449 |  | Story asks to keep the five Interface cells word for word, so no edit is required. Cells not re-checked in the workbook. |
| CDC-20515 | RWB-P2-E1007-INF | R-28449 |  | Story asks to keep the Interface cell text unchanged, so no edit is required. Cells not re-checked in the workbook. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20648 | RWB-P2-E1007-CON | R-21878 |  | Manifest and return belong in rwb-payment, rwb-debtsale, rwb-reporting; JSON names and event subject with platform owner (GAP-0648). |
| CDC-20656 | RWB-P2-E1007-CON | R-21878 |  | Notice-fact read and JSON names sit in other contracts; problem body status codes not in source (GAP-0648). |

### OTHER:rwb-source-data and rwb-document API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04357 | RWB-P2-E1007-APP | DOR-RWB-P2-E1007-APP-8 | 12 | Publish the paths named in DOR-RWB-P2-E1007-APP-8 (P1 GET source-data/v1/freshness, customers/{id}, accounts/{id}; P1 POST document/v1/documents; 11 more). |

### RWB-P2-E1007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04372 | RWB-P2-E1007-APP | GAP-0650 | 12.6 | Set chart values, replica counts, KEDA threshold, lag and alert thresholds and build ID format as environment values; confirm the two windows with the Airflow owner as calls; fix trigger contract and alert identifiers with Airflow and observability owners; keep the R9 placeholder. |

### RWB-P2-E1007-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04374 | RWB-P2-E1007-APP | GAP-0649 | none | Provision two outbound endpoints per environment with one receiver and one key each; hold credentials, private keys and certificates in the key store; set endpoint hosts, ports, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period from the bank MFT, network and security teams, recording rotation in the key-rotation runbook. |

### RWB-P2-E1007-CON; OTHER:owner CON stories of rwb-source-data and rwb-reporting (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04375 | RWB-P2-E1007-APP | GAP-1396 | none | Fix Airflow product, tenancy, scheduler service principal, timeout and retry values, DailyCaseRun wait mechanism and the three owner operation paths and payloads at scheduling design review, before first SIT chain run. |

### OTHER:WP B-P5-03 (secondary P5 slice of RWB-E1-007) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04376 | RWB-P2-E1007-APP | GAP-1027 | none | Treat the slice as new work with six new criteria and no legacy AC; take manifest and claim-check field names from RWB-P2-E1007-CON; read the type code and retention class from document_type in force; anchor document.case_id on the store request case ID; use CLAIM_CHECK_MINUTES = 15. |

### OTHER:Mapping workbook (v4 Mapping column M) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04381 | RWB-P2-E1007-APP | GAP-0213 | find it | Keep the five Interface cells word for word in v5 and confirm the v4 interface numbers at the next interface review. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Events sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04382 | RWB-P2-E1007-APP | GAP-1538 |  | Add two rows, FileDelivered and FileFailed, producer rwb-integration, topic rwb.integration.events.v1, consumer requesting service, keyed by case ID, with no numbered EV ID. |

### OTHER:FSD P2 v3 (A1.6 exclusion table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04383 | RWB-P2-E1007-APP | GAP-1542 | 8 | Move the removed IDs (FEAT-DRI-09, inbound half of FEAT-RDF-21, FEAT-DRI-10, FileLoadAdapter, DQ-057, DQ-059, JOB-09, interface_run, interface_signoff) into an exclusion table with later home ACE ingestion; no FR, NFR or AC. PRD states no inbound adapter, folder, run or sign-off exists. |

### RWB-P2-E1007-CON; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04395 | RWB-P2-E1007-CON | DOR-RWB-P2-E1007-CON-14 | none | Record the signed epic design sign-off for RWB-P2-E1007-CON. No signed epic design was found in the story or the source documents. |

### OTHER:API yaml of rwb-source-data and rwb-document (and the other services named in the readiness detail) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04396 | RWB-P2-E1007-CON | DOR-RWB-P2-E1007-CON-8 | 8 | Publish the listed paths: source-data freshness, customers/{id}, accounts/{id}; document POST /documents; and the 8 further paths in the detail. |

### OTHER:BRD Program v4 section 5.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04397 | RWB-P2-E1007-CON | GAP-1534 | 12.7 | Remove the data lake and Power BI delivery; INT-19 as a delivery request from rwb-reporting via the rwb-integration contract; INT-20 as continuous ingest in rwb-decision. |

### OTHER:App story of RWB-E1-007 split (owner of SCR-09) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04404 | RWB-P2-E1007-CON | DOR-RWB-P2-E1007-CON-10 | 15 | Section 15 names SCR-09 and the contract states. Its screen fields and states belong to RWB-P2-E1007-APP. |

### OTHER:FSD P2 Integration v3 A1.5; OTHER:TSD P2 Integration v3 T1 and T5.1; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04406 | RWB-P2-E1007-CON | GAP-0673 | find it | Mark the INT-03 bookings superseded for legacy key RWB-E4-046 with date and decision; load one versioned ALS interface_config row per environment. |

### OTHER:rwb-comms API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04410 | RWB-P2-E1007-CON | GAP-0648 |  | Add the notice-fact read with notice ID, sent date, person key and document ID; confirm deliverFile manifest and return with rwb-comms, rwb-payment, rwb-debtsale and rwb-reporting; fix JSON names in OpenAPI. |

### OTHER:Bank Airflow owner trigger contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04411 | RWB-P2-E1007-CON | GAP-0650 |  | Confirm the 16:00 WIN window and per-lot buyer window as calls to requesting services' own APIs, with call, parameters and missed-window behaviour, and name the lag and window alert identifiers. |

### OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04412 | RWB-P2-E1007-CON | GAP-0739 |  | Provide the route state to resume read from the latest decision-record entry of the case and interface, and the task code and due date as reference rows of rwb-case. |

### OTHER:rwb-document API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04414 | RWB-P2-E1007-CON | GAP-1164 | 12.2, 12.5 | Section 12.2 lists the document operation and 12.5 states the claim-check handoff. The INT-14 record layout and file pattern stay open; the operation is for rwb-document to publish. |

### RWB-P6-E1007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04415 | RWB-P2-E1007-CON | GAP-1166 |  | Run state from notice dispatch fields, workflow run and P2 status, no run table; one read and one rerun on the rwb-comms base; right enforced at gateway-bff; confirm local guard with edge owner. |

### OTHER:Split plan (P8 service contract baseline) and TSD P8 v2 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04421 | RWB-P2-E1007-CON | GAP-2548 | n/a | Allocate a service contract baseline for this key publishing rwb.payment.TreatmentBooked.v1 in BACKWARD mode, the deliverFile manifest booking branch, the error envelope and the fakes; publish ALS interface values and the data product code in T-A. |

### RWB-S8-E7004-APP; OTHER:DP-05; OTHER:DP-09 and DP-16 pattern rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04422 | RWB-P2-E1007-CON | GAP-3057 | n/a | Record the five consumed rows and one consumed event, rule kit, outbox and inbox library, access guard, Aric referral and state list as the GAP-3057 fix states. |

### RWB-S5-E3029-APP; RWB-S5-E3029-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04423 | RWB-P2-E1007-CON | GAP-2886 | n/a | Declare the HOME.SCB, EASY and auction publication and the pause as consumed rows of the P2 rwb-integration contract with a placeholder; add C RWB-P2-E1007-CON and DP-16 to both slices. |

### OTHER:TSD S5 T5.1 external interface table and split plan slice RWB-S5-E4028 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04424 | RWB-P2-E1007-CON | GAP-2931 | n/a | Add a SCIS row with gap ID GAP-2931 and placeholder; record the consumed row as an activity on queue rwb-integration; add DP-16 with C RWB-P2-E1007-CON to the pattern set. |

### RWB-S6-E6007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04425 | RWB-P2-E1007-CON | GAP-3004 | n/a | Record six consumed rows and the AccountsTransferred outbox dependency with RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON; add DP-09; split R-DS-25 as the fix states. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Events sheet (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04429 | RWB-P2-E1007-CON | GAP-1538 |  | Add two rows for FileDelivered and FileFailed: producer rwb-integration, topic rwb.integration.events.v1, consumer requesting service, keyed by case ID, no numbered EV ID. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md; OTHER:FSD P2 v3 AC-EXC-P2-001-01 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04430 | RWB-P2-E1007-CON | GAP-1540 |  | State the FSD retry behaviour as the acceptance criterion and the interface configuration values (max attempts 3; 5, 15, 45 minutes) as configuration in force, not as a product rule. |

### OTHER:FSD P2 v3 (A1.6); 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04431 | RWB-P2-E1007-CON | GAP-1542 |  | Keep removed IDs (FEAT-DRI-09, FileLoadAdapter, DQ-057, DQ-059, JOB-09, interface_run, interface_signoff) in an exclusion table with later home ACE ingestion. Add no FR, NFR or AC. PRD states no inbound adapter, folder, run or sign-off exists. |

### OTHER:FSD P2 v3 (A1.5); 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04432 | RWB-P2-E1007-CON | GAP-1546 |  | State INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR. PRD records that their behaviour is ACE's. |

### OTHER:FSD P2 v3; 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04433 | RWB-P2-E1007-CON | GAP-1547 |  | Record the FSD sentence on the partner portal and document hub transport as superseded. PRD states both channels keep their own contracts and P2 carries no requirement for them. |

### OTHER:P3 story carrying SCR-09 (not named in source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04439 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-10 | find it | Add empty, loading, error and no access states for SCR-09 |

### OTHER:BR field register (not named in source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04441 | RWB-P2-E1007-INF | DOR-RWB-P2-E1007-INF-7 | 11 | BR Field ID column reads Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) on all 9 data rows. |

### OTHER:RWB operations story (DevOps environment values) and bank Airflow owner confirmation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04448 | RWB-P2-E1007-INF | GAP-0650 |  | Set chart values, replica counts, KEDA backlog threshold, lag and alert thresholds and build ID format as environment values; confirm both window calls with the bank Airflow owner; name lag and window alert identifiers with Airflow and observability owners; keep the §R9 placeholder. |

### RWB-P2-E1007-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04455 | RWB-P2-E1007-INF | GAP-3160 |  | Remove debt_sale_account and recovery_case writes from the P2 adapter transaction; S6 rwb_debtsale owns debt_sale_account via contract call or event from P2; P3 rwb_case owns recovery_case. |

### OTHER:WP B-P5-03 and the P5 document hub story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04457 | RWB-P2-E1007-INF | GAP-1027 |  | Treat the secondary P5 slice as new work with six new criteria and no legacy AC; take manifest and claim-check names from RWB-P2-E1007-CON; use CLAIM_CHECK_MINUTES = 15. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04459 | RWB-P2-E1007-INF | GAP-0981 |  | Register one OUTBOUND interface row for the access-review file with its interface ID, file pattern, data product, owner and alert role; publish the extract layout, recipient and review-cycle date convention. |

### OTHER:ACE-new mapping workbook (five rows of the Interface column) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04460 | RWB-P2-E1007-INF | GAP-0213 |  | Keep the cell text word for word in v5; confirm the v4 interface numbers at the next interface review. |

### OTHER:BRD Program v4 section 5.2; OTHER:FSD P2 v3 INT-19 and INT-20 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04471 | RWB-P2-E1007-OPS | GAP-1534 | n/a | Drop the data lake and Power BI targets. INT-19 becomes a delivery request from rwb-reporting via rwb-integration; INT-20 becomes continuous ingest in rwb-decision, per Architecture v5. |

### OTHER:FSD P2 v3; OTHER:INT-25 tape build (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04472 | RWB-P2-E1007-OPS | GAP-1539 | n/a | Build tape rows and account keys from the delivery request manifest raised by rwb-debtsale; read account facts via the rwb-source-data contract. P2 reads neither debt_sale_account nor v_ace_account. |

### OTHER:P3 screen specification (SCR-09; OTHER:SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04475 | RWB-P2-E1007-OPS | DOR-RWB-P2-E1007-OPS-10 | 8 | Add empty, loading, error and no-access states to SCR-09 and SCR-44, or confirm where the P3 spec holds them. |

### OTHER:TSD P6 Communications v2 (T-A and T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04485 | RWB-P2-E1007-OPS | GAP-1166 | - | Name the right a reader of run state holds on the interface monitor and confirm the local guard question with the gateway-bff and edge owner. |

### OTHER:Build Notes v6 (RWB-E1-007 View note); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04489 | RWB-P2-E1007-OPS | GAP-3160 | n/a | This story creates only the rwb_integration tables of §12.7; the correction belongs to the target documents. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:9; OTHER:16; OTHER:20) and owner CON stories for rwb-source-data, rwb-integration, rwb-reporting (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04491 | RWB-P2-E1007-OPS | GAP-1396 | - | Fix the Airflow product, tenancy, service principal, timeout and retry values, DailyCaseRun wait mechanism and the three owner operation paths and payloads before the first SIT chain run. |

### OTHER:FSD P2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04499 | RWB-P2-E1007-OPS | GAP-1547 | 7 | Record the FSD sentence on partner portal and document hub transport as superseded. PRD states the partner and document channels keep their own contracts and P2 carries no requirement for them. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04501 | RWB-P2-E1073-APP | CG-ALL-2997 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} through the provider's CON story, or the consumer switches to a published operation. |

### RWB-P3-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04510 | RWB-P2-E1073-APP | DOR-RWB-P2-E1073-APP-10 | 7 | Add empty, loading, error and no access states for SCR-39 in the P3 story. |

### OTHER:TSD P7; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04511 | RWB-P2-E1073-APP | GAP-1615 |  | Re-issue TSD P7 with T3.1 entries for rule_package, rule_package_version, rule_row and rule_test_case and appendix T-A rule operations; remove those tables and operations from TSD P3 and TSD P4; set x-module of the nine rule paths in the API Specification to P7. |

### RWB-P3-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04512 | RWB-P2-E1073-APP | GAP-1330 | 12 | State whether it publishes the case reads its consumers need, or move the case-read dependency to RWB-P3-E1023-CON. This story reads no case fields (synthetic facts, section 11). |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04514 | RWB-P2-E1073-APP | GAP-0699 | 11 | Correct the ownership labels of rule_package, rule_package_version, rule_row and rule_test_case to P7 rwb-decision (ASM-A6-tables-3). This story already states P7 ownership (section 11 and 12.7). |

### OTHER:rwb-decision API document and wave-1 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04518 | RWB-P2-E1073-APP | GAP-1217 | 13 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} with the DRL, SHA-256, version state, valid-from date, 404 for an unknown label and 409 for a non-loadable version, under the 2 s client budget and one hop. |

### OTHER:rwb-decision contract (registry resources, model answer, dry-run counts, workbook container, panel ID, service login, pa (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04519 | RWB-P2-E1073-APP | GAP-1327 | 11 | Publish the physical registry columns, the model answer (package code, version label, state, valid from, SHA-256, DRL, parsed catalogue rows in row order), the dry-run count shape, the workbook container and object name, the version-list panel ID, the service login and the two parameter codes. |

### OTHER:Wave-1 rwb-decision and rwb-comms contract review record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04522 | RWB-P2-E1073-APP | GAP-1214 | 3 | Record the local copy table name and columns, the two parameter rows and their read path, the two added check values with message text, the scenario set and run result shape, and the 300 ms measurement point. |

### OTHER:Template and Rules v1 §R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04525 | RWB-P2-E1073-APP | GAP-1328 | 3 | State that platform H rows and self-referential C rows are held by the platform and contract stories and are not repeated on the APP line. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04526 | RWB-P2-E1073-APP | GAP-1620 |  | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime, that a version names its format, and that conversion is a version change with its own test evidence. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04527 | RWB-P2-E1073-APP | GAP-0118 |  | Confirm amended text of D-RCV-36 T1 and T2: the workflow runs on the owning service task queue, and each scheduled job becomes a Temporal Schedule or event-started workflow there, with JOB-05 behind the TimerScheduler port until Epic 3. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04528 | RWB-P2-E1073-APP | GAP-0205 | none | Add rule_package and rule_package_version as entities owned by P7 in the next LDM and Ownership Map version. Keep the v6 row names unchanged. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04530 | RWB-P2-E1073-APP | GAP-1219 | none | Add rwb-comms to the consumers of RulePackageInForce in row 30, or publish the package-to-service map that completes the row. |

### OTHER:Temporal and Drools design (slide 15) and RWB-E1-073 legacy story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04531 | RWB-P2-E1073-APP | GAP-1331 | none | State that REFUSED is a state of a stored version that failed promotion checks, and that a load refused at a check writes no version row and is proved by its decision log entry. |

### OTHER:Rules Engine Design v3 (to version 4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04532 | RWB-P2-E1073-APP | GAP-2049 | none | Keep MSG-P3-027 unchanged. Raise the compile alert in the service that loads the package, name P7 rwb-decision as registry owner, and keep RWB-E1-073 as run-book owner. |

### OTHER:Template and Rules v1 (DP-04 row) and split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04535 | RWB-P2-E1073-APP | GAP-1215 | none | Correct the DP-04 row or the plan so H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON agree with the plan Metadata rows at the next rules-of-record pass. |

### OTHER:FSD P3 (A1.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04540 | RWB-P2-E2001-APP | GAP-1549 | none | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04551 | RWB-P2-E2001-APP | DOR-RWB-P2-E2001-APP-10 | find it | Define empty, loading, error and no-access states for the SCR-02, SCR-04 and SCR-45 routes, which this story registers but does not own. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04553 | RWB-P2-E2001-APP | GAP-3175 | none | Add LoadCompleted as the legacy alias of AceDataReady (EV-26), producer rwb-source-data, on rwb.source-data.events.v1. |

### OTHER:Batch and Scheduling (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04554 | RWB-P2-E2001-APP | GAP-3176 |  | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### OTHER:Harness pack (integration lead with QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04557 | RWB-P2-E2001-APP | GAP-0388 |  | Hold composite route paths and merge order, harness repository, SIT and UAT environments, seeding, evidence format, retention and pass/fail gate as data in the harness pack. |

### OTHER:contract/handover-run-activities.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04559 | RWB-P2-E2001-APP | GAP-0652 |  | Fix the workflow, nine activities, twelve summary elements and retry policy; fix the P1 and P3 consumed elements; publish six fakes from owners' OpenAPI and fail the build on drift. |

### OTHER:rwb-integration deployment values file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04560 | RWB-P2-E2001-APP | GAP-0653 |  | Hold all environment values and unnamed message IDs as placeholders until the Error and Message Standard names them; review the runbook with the on-call rota before release. |

### OTHER:TSD P7 API-P7-006 decision-log contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04561 | RWB-P2-E2001-APP | GAP-1333 |  | Add the businessDate filter, full answer field set and page-size limit; name one screen or panel for a decision entry beside the case. |

### OTHER:TSD P3 v3 (T3.1 interaction object) and the P3 ledger story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04563 | RWB-P2-E2001-APP | GAP-2260 | 4 | Re-scope the P3 ledger story to the P1 contract and mark the TSD P3 interaction object as owned by rwb-source-data under DP-18. |

### RWB-P7-E2005-CON; RWB-P2-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04564 | RWB-P2-E2001-APP | GAP-2463 | 4 | Step 7 states the repeat-count source is Not specified in the source documents |

### RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04566 | RWB-P2-E2001-APP | GAP-2464 |  | Fix GET /decision-log parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page and size; page size 1 to 500; order by decided_at. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04567 | RWB-P2-E2001-APP | GAP-1332 | 4 | Step 13 names RWB-PLT-E1027-CON as owner; element names Not specified in the source documents |

### RWB-P7-E2005-CON; RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04568 | RWB-P2-E2001-APP | GAP-2462 |  | Add the element list of decision_log_entry actions and outcome to the DecisionLogEntry resource and the record shape at the contract review. |

### RWB-PLT-E1047-CON; RWB-PLT-TE006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04569 | RWB-P2-E2001-APP | GAP-2262 | 4 | Fix the rwb.case.events.v1 envelope and retry settings; limit the CaseCreated payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry. |

### OTHER:RWB-PLT-OBS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04571 | RWB-P2-E2001-APP | GAP-2465 | 4 | Register the ingest lag of rwb.decision-record.v1 into the ledger as a metric with its threshold as a parameter; raise the gap alert to RW-PLATADM under RWB-P7-E1027-APP. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:database platform story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04573 | RWB-P2-E2001-APP | GAP-1334 | n/a | Publish the per-service login of rwb_decision with the database platform story; fix the workflow, activity and JOB-14 Schedule names in the catalog before wave 2 build. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04574 | RWB-P2-E2001-APP | GAP-2467 | 4, 8, 16 | Decision code value left to LOV-DECISION row load |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20631 | RWB-P2-E1007-OPS | R-21890 |  | RWB-E1-007 'What moves' already routes the debt_sale_account write through S6's contract (GAP-3160); the rwb_integration tables are P2. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20808 | RWB-P2-E1007-CON | R-22788 |  | Contract baseline allocation belongs to the split plan. ALS interface values and data product code are not in the sources (GAP-2548). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0118 | The amendment of D-RCV-36 T1 and T2 has no wording in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0205 | The entity called Rule is rule_row, and the model holds neither rule_package nor rule_package_version | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0213 | Five rows still cite 'number in Interface Specifications v3' after v4 of that document was issued | Integration architecture team | Resolved (directive) |
| GAP-0334 | deliverFile manifest payload, claim-check handoff and the file-window trigger contract are not defined | Solution architect | Resolved (directive) |
| GAP-0338 | Connection matrix gives rwb-integration only the document REST call and the outside file edge, while the file build reads source data and the failure reaches rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0383 | The rule package of rwb-comms and of rwb-integration, the rule-model fetch path and its owner, and the message family of the refusal are not stated in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0388 | EFS hand-over harness: repository, environments, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0589 | The history read is one operation or a paged read, and the HTTP answer of a held read, are stated by no source | Solution architect, P1 | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0647 | rwb-integration outbound-file capability: ACE read path, INT-25 source table, data-lake retirement, JOB-10 and JOB-11 split, operation naming, alert event names, deliverFile manifest and job catalog rows not settled | Solution architect | Resolved (directive) |
| GAP-0648 | Outbound-file contract: deliverFile manifest and return, notice-fact read of rwb-comms, JSON field names and problem body, event schema subject and compatibility level not fixed by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0649 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | SCB IT infrastructure | Resolved (directive) |
| GAP-0650 | Outbound-file deployment: chart values, replica counts, KEDA threshold, lag and alert thresholds, dashboard names, build ID format, Airflow trigger contract of the two file windows and the message identifiers of the lag and window alerts not specified in any source | DevOps team | Resolved (directive) |
| GAP-0651 | rwb-integration EFS hand-over: the mount of the step, the split across four owners, the consumed contract paths, the run summary store and the level of the decision record are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0652 | rwb-integration EFS hand-over contract: the activity contract, the consumed element shapes, the provided surface and the fakes have no source text | Tech lead | Resolved (directive) |
| GAP-0653 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | DevOps lead | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0699 | The rule package registry and the workbook object are declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0700 | The five authoring operations and the two rule reads have no Ownership Map row and no field-level shape | P7 rwb-decision owner with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0701 | The KieBase cache sizing, the JVM heap and the storage of a local model artefact are not specified | SCB IT infrastructure with the rwb-case owner team | Resolved (directive) |
| GAP-0702 | No source gives the readiness gate, the probe timings, the ports, the certificate subject or the image-scan window | SCB IT infrastructure with the platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0739 | The case side of an outbound file outcome leaves the delivery-event element names, the route state to resume, the task code and due date, the fate of the legacy in-process interfaces and the two lake extracts unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1162 | The addressee and contact value reach the INT-14 file through a contract that is not in the story's contract list, and no source names the operation or its elements | Solution architect, with the P1 and P6 owners | Resolved (directive) |
| GAP-1163 | DP-17 removes the INT-19 reporting extract and the INT-20 decision-log copy, so part of legacy RWB-E1-007 has no target and no replacement in this service | Business analyst and solution architect | Resolved (directive) |
| GAP-1164 | The INT-14 record layout, the file pattern and the claim-check store of the built file are named by no source, and the document contract is not in the story's contract list | Solution architect, with the P2 and P5 owners | Resolved (directive) |
| GAP-1165 | The retired inbound load leaves TC-E1-007-05, TC-E1-007-06 and the file checks DQ-057 and DQ-059 without a target in this service | Business analyst and QA lead | Resolved (directive) |
| GAP-1166 | No source defines a run record, a run operation or the right on the interface monitor for rwb-comms | Solution architect and the gateway-bff owner | Resolved (directive) |
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1215 | RWB-P6-E1073-APP: the DP-04 row of the pattern table names H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON while the plan gives no H and C RWB-P3-E1073-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1216 | RWB-P6-E1073-APP: no source names the rule package rwb-comms is assigned, its version labels or its target queues | Solution architect | Resolved (directive) |
| GAP-1217 | RWB-P6-E1073-APP: the model fetch operation, its path segments, its request fields and its response fields are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1219 | RWB-P6-E1073-APP: Arch v5 slide 43 lists four consumers of RulePackageInForce while slide 20 says every service refreshes its cache on it, and the ITG story makes rwb-comms an evaluator | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1327 | RWB-P7-E1073-APP: the model answer, the dry-run report, the refusal of the model read, the workbook object, the version-list panel, the service login, the parameter codes and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1329 | RWB-P7-E1073-APP: the same rule registry is named as /admin/rule-versions by API Specification v4 and the integration story and as /admin/rule-package* by the legacy story and the Ownership Map, and a third read /rule-catalog is consumed but unowned | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1330 | RWB-P7-E1073-APP: the case read that feeds the dry run is attributed to RWB-P3-E1073-CON by the plan and to RWB-P3-E1023-CON by the P3 contract story, which serves no operation | Solution architect with the rwb-case contract owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1331 | RWB-P7-E1073-APP: REFUSED is one of the six version states while a load refused at a check writes no rule_package_version row, so no stored version ever reaches it | Solution architect with the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1332 | Envelope and payload element names of DecisionRecorded, and the shape of the inputs snapshot | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1333 | Answer field set and business-date filter of the decision-log read, and the screen that shows an entry beside the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1334 | Per-service login of rwb_decision, the chain-check workflow and activity names, and the Schedule identifier of JOB-14 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1396 | Airflow product, tenancy, DAG names, identity method, timeout and retry values, the DailyCaseRun wait contract and the file-window operation are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1534 | Data lake extracts INT-19 and INT-20 still listed as outbound adapters in FSD P2 v3, removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1535 | FSD P2 v3 has the outbound file read the recovery.v_ace_* views directly; Architecture v5 and ADR-010 reserve the views to rwb-source-data | Solution architect | Resolved (directive) |
| GAP-1536 | Job ownership of JOB-10, JOB-13 and JOB-15 differs between FSD P2 v3 and the Ownership Map | Platform administrator | Resolved (directive) |
| GAP-1537 | Who retries a failed transfer is stated three ways: Airflow, the service retry ladder, or the outbox sender | Solution architect | Resolved (directive) |
| GAP-1538 | FileDelivered and FileFailed have no row in the 31-row Ownership Map event register | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1539 | FSD P2 v3 builds the debt buyer tape from debt_sale_account, a table the Ownership Map gives to S6 rwb-debtsale | Solution architect | Resolved (directive) |
| GAP-1540 | Retry interval values differ between the FSD criterion and the interface configuration used by the service stories | Platform administrator | Resolved (directive) |
| GAP-1542 | FSD P2 v3 keeps removed function and check IDs with no target behaviour | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1544 | No non-functional target is stated for an outbound file itself: size, throughput, window length or volume per day | Solution architect | Resolved (directive) |
| GAP-1546 | The notification and logging rows of the FSD interface register state no Workbench behaviour | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1547 | FSD P2 v3 claims the transport of the partner portal and the document hub; Architecture v5 gives each its own service | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-2030 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2031 | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2049 | The rule package compile alert names P3 while the registry is P7 and the load happens in every owning service | P7 rwb-decision with the centre of excellence | Resolved (directive) |
| GAP-2229 | Element names of the two delivery outcomes, the carrier of the route state to resume and the values of the owner task are not in the sources | TechX and the rwb-integration contract owner | Resolved (directive) |
| GAP-2230 | The legacy P3 interfaces and the case-action path have no operation in the target case contract | TechX | Resolved (directive) |
| GAP-2258 | No rerun operation for the entry run after JOB-02 becomes a workflow | TechX | Resolved (directive) |
| GAP-2259 | Paths and payloads of the P2 hand-over and P1 ledger contracts | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2260 | Interaction ledger ownership conflicts with the legacy write and the P3 data model | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2457 | The physical columns of rule_package, rule_package_version, rule_row and rule_test_case are not in any source | TechX and the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2458 | No provided operation of the case service returns the open case facts a dry run needs | P3 and P7 contract owners | Resolved (directive) |
| GAP-2459 | Which owned event announces a rule package version in force is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2460 | The value of rules.testcases.min is assumed and no parameter catalogue holds it | P3 parameter owner and the P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2461 | The legacy endpoints and their controller sit in the access module, while the Ownership Map gives them to P7 | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2462 | The inner shape of the actions and outcome columns of a hand-over decision entry is not in any source | Solution architect with the data steward | Resolved (directive) |
| GAP-2463 | Where the R-UNI-40 repeat count of a hand-over record is kept and reported is not stated | P7 and P2 solution architects | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2464 | No source fixes the query parameters and paging of GET /decision-log | P7 contract owner | Resolved (directive) |
| GAP-2465 | The five-minute ledger completeness target has no named alert, owner or threshold | Platform observability owner with the P7 solution architect | Resolved (directive) |
| GAP-2466 | The legacy story puts the EFS history append in the decision module while the Ownership Map and DP-18 put the interaction ledger in rwb-source-data | Solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2467 | The exact LOV-DECISION value of the hand-over entry is not stated | P7 business analyst with RW-COE | Resolved (directive) |
| GAP-2468 | The story line carries one C row and no H row while the pattern table adds six platform H rows and the guard | Coordinator of the realignment with the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2886 | The publication to HOME.SCB, the EASY app and the auction portal has no owner contract in the plan, DP-16 is not in the pattern set, and the publish request and answer have no published shape | Integration architect with the P2 rwb-integration service owner and the S5 rwb-asset service owner | Resolved (directive) |
| GAP-2931 | SCIS has no interface row in TSD S5, no call type, and DP-16 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3157 | The rule tables are described as recovery-schema tables but are owned by rwb-decision | P7 rule owner | Resolved (directive) |
| GAP-3160 | The P2 outbound adapter writes a table owned by rwb-debtsale | Integration lead | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3240 | One module per item in version 3 becomes several services per item in the split | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
