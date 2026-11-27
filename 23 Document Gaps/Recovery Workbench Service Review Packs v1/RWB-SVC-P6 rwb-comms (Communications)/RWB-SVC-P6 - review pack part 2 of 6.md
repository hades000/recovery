# RWB-SVC-P6 rwb-comms (Communications) - review pack, part 2 of 6 (RWB-P6-E1046-CON to RWB-P6-E1055-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 194 |
| Cross-document (pending in another document) | 208 |
| Not applied (value not in the sources) | 21 |
| Open business decisions | 15 |
| Register gaps linked | 97 |
| Unconfirmed assumptions | 0 |
| Lint findings | 5 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P6-E1046-CON | 18 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1046 CON Template and merge field catalog as data - contract v2.md |
| RWB-P6-E1049-APP | 20 | 20 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1049 APP OCR pipeline on the Workbench document hub v2.md |
| RWB-P6-E1052-APP | 29 | 35 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1052 APP Notice generation v1 v2.md |
| RWB-P6-E1052-CON | 20 | 29 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1052 CON Notice generation v1 - contract v2.md |
| RWB-P6-E1055-APP | 43 | 22 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1055 APP Proof of delivery capture design with WIN v2.md |
| RWB-P6-E1055-CON | 26 | 22 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1055 CON Proof of delivery capture design with WIN - contract v2.md |
| RWB-P6-E1055-INF | 17 | 26 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1055 INF Proof of delivery capture design with WIN - infrastructure v2.md |
| RWB-P6-E1055-OPS | 21 | 25 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1055 OPS Proof of delivery capture design with WIN - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1049-ITG, RWB-ITG-E1050-ITG, RWB-P3-E1050-APP, RWB-P5-E1049-APP, RWB-P5-E1049-CON, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1053-CON, RWB-P6-E1049-APP | R-09185 | GAP-1586 | Register gap | Solution architect with the AI product owner | The OCR, classification and extraction services are named as external pieces but no source names them or their owner | The PRD keeps the pipeline behaviour in P5 and states the OCR, classification and extraction engines as an external contract reached as an AgentRunCompleted event or a Temporal child run, with the provider, the contract and the version scheme carried as OQ-P5-06. |
| RWB-P6-E1052-APP | R-11005 | CG-ALL-6388 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E1055-APP | R-11012 | CG-ALL-6416 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22078 | GAP-1595 | Register gap | Product owner | The document module is said to own the letter templates and their fields, while Architecture v5 gives templates and merge fields to rwb-comms | Hold the template record, its versions and the Legal approval in rwb-comms, hold the merge-field catalog in rwb-comms, and keep the template body file in rwb-document as a document with a reference on the template row; record DL28 as superseded by D-RCV-60 and close it with the product owner. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22125 | GAP-2089 | Register gap | Product owner; service owners of P6 rwb-comms and P5 rwb-document | The Decision Log gives the letter templates to the document module, while Architecture v5 and the Ownership Map give them to rwb-comms | Follow Architecture v5 and the Ownership Map: templates and merge fields are P6 rwb_comms. Record the DL28 answer as a gap and ask the product owner to reaffirm or amend DL28 before the template story is Done. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1025-APP, RWB-P5-E1052-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-22159 | GAP-2347 | Register gap | Data steward and document type owner, with the Legal counsel and the P5 TechX squad | The notice-type to document-type mapping, the retention class and the write-once flag of each notice document type are not specified in any source read here | The document type load of RWB-P5-E1025-APP carries the DEMAND_LETTER and GUARANTOR_NOTICE rows with their class and flag, and the notice-type mapping row is added to the type or mapping table before the wave-1 test data is loaded |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-22191 | GAP-2245 | Register gap | Legal and the business lead | Whether a deviation pauses a statutory notice period is not settled by the sources | Keep the notice period unpaused as ASM-B2-P3-016-3 records; if Legal rules that it pauses, the deviation contract gains one signal to the notice clock and one criterion changes. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-28596 | GAP-2098 | Register gap | Service owner of P6 rwb-comms; Compliance and Legal roles | The Compliance approval of customer wording has no artefact in the target template | Record the Compliance approval as a second approval of P7 with the template as its source, and keep approved_by_legal on the template row for the Legal approval that the endpoint records. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1052-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-28611 | GAP-2088 | Register gap | Business lead with Legal and Compliance; document owner | DL10 is listed open with one answer and is recorded as answered with another | Keep the source row word for word, record in section 6.1 that DL10 is answered on 5 November 2026 with answer A, and add no Thai wording in this document. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-28627 | GAP-2248 | Register gap | Business lead | The role that receives the expiry of a notice period is not named | Take the escalation role from the SERVICE_LEVEL row in force as ASM-B2-P3-016-6 records, and add a named default role for a missing row if the business lead asks for one. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P6-E1049-APP | R-25984 | CG-ALL-6379 | 3 | Flyway file V1049_1__rescan_notice.sql is not in the V0001..Vnnnn form | Next Vnnnn of the rwb-comms Flyway sequence is Not specified in the source documents (CG-ALL-6379). Grep of the project found no value in Service Template Specification v1 section 3.1. Story text for the migration name is not in this chunk. |
| RWB-P6-E1049-APP | R-28599 | GAP-1208 | 5 | The document token of the rescan message has no named reference form | The reference form of the document token is in no source (GAP-1208); no rule is invented. |
| RWB-P6-E1052-APP | R-25991 | CG-ALL-6389 | 3 | Flyway file V1052_1__notice_generation.sql is not in the V0001..Vnnnn form | Next Flyway number not in sources. Grep found no Service Template Specification v1 .md with db/migration. Needs solution architect. |
| RWB-P6-E1052-CON | R-17581 | DOR-RWB-P6-E1052-CON-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 text is not in this chunk, so exact old text cannot be copied. Re-send section 15 to add the empty, loading, error and no access states for SCR-01, SCR-18 and SCR-30. |
| RWB-P6-E1052-CON | R-28612 | GAP-0750 | 12.3 | The decision code and the final call of the case-side notice record are only partly specified | Ruling is to reuse D7.1 with template code and version, notice reference and business date. Section 12.3 text is not in this chunk. Re-send 12.3 to apply. |
| RWB-P6-E1052-CON | R-28796 | GAP-1096 | 14 | The message text of MSG-P6-005 and MSG-P3-005 is not given by the legacy story or the P6 extracts | No published source gives the MSG-P6-005 or MSG-P3-005 text. The placeholder needs section 14 text, which is not in this chunk. Re-send section 14 once the owning stories publish the texts. |
| RWB-P6-E1052-CON | R-31276 | NEWAC-RWB-P6-E1052-CON-AC10 | 7, 16 | AC10: §8 BR10, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC10 needs section 7 and 16 text, which is not in this chunk. The proposed test is not specified in the sources. Re-send sections 7 and 16 with a test from the owner. |
| RWB-P6-E1055-APP | R-06422 | DOR-RWB-P6-E1055-APP-14 | none | Definition of Ready item 14 Epic design: Fail | No signed epic design or epic design record found (grep of project folder for 'signed epic design', 'epic design record', 'Epic design' returned no files). Sign-off cannot be confirmed without an invented value. |
| RWB-P6-E1055-APP | R-11013 | CG-ALL-6418 | 12.8 | Criteria and test data read ACE views directly | The AC2, AC3 and test-data Given lines that read ACE views are in sections 7 and 16, which are not in this chunk, so their old text cannot be copied. Re-issue with those sections. |
| RWB-P6-E1055-APP | R-17586 | DOR-RWB-P6-E1055-APP-10 | none | Definition of Ready item 10 Screens and states: Partial | Screen-state lines for SCR-03, SCR-30, SCR-44 and SCR-45 are in the screen sections, which are not in this chunk. Re-issue with those sections. |
| RWB-P6-E1055-APP | R-21908 | GAP-1169 | none | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | No source names a code for the notice barcode break, so REC-05 cannot be renumbered without an invented code. Needs the data steward; the story text in this chunk has no REC-05 line. |
| RWB-P6-E1055-APP | R-26005 | CG-ALL-6417 | 3 | Flyway file V1055_1__notice_dispatch.sql is not in the V0001..Vnnnn form | Next free rwb-comms Flyway number is not in the sources (Service Template v1 3.1 and 6.2 name only V0001). The migration filename is not in the story parts supplied. Name left as is. |
| RWB-P6-E1055-CON | R-06428 | DOR-RWB-P6-E1055-CON-14 | n/a | Definition of Ready item 14 Epic design: Fail | Signed epic design record is not in this chunk or the story text; the sign-off value cannot be written without it (DOR-RWB-P6-E1055-CON-14). |
| RWB-P6-E1055-CON | R-17595 | DOR-RWB-P6-E1055-CON-10 | 9 | Definition of Ready item 10 Screens and states: Partial | SCR-03, SCR-30, SCR-44 and SCR-45 state text sits in section 9, which is not in this chunk, so it cannot be anchored. |
| RWB-P6-E1055-CON | R-17596 | DOR-RWB-P6-E1055-CON-12 | 12, 12.7, 16, 18 | Definition of Ready item 12 Test cases: Partial | TC-13 contract and TC-14 boundary rows already exist; RTM v7 lists and AC ownership text are not in the chunk, so they cannot be checked. |
| RWB-P6-E1055-CON | R-22178 | GAP-0578 | 12.2, 7 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Section 12.2 row 3 and AC3/AC4 text are not in this chunk. Section 18 DP-18 already names rwb-source-data as the writer, but the contract row cannot be anchored. |
| RWB-P6-E1055-CON | R-22179 | GAP-0580 | 7, 16 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | AC4 text and the DP07 repeat-counter wording are not in this chunk, so the edit cannot be anchored. |
| RWB-P6-E1055-INF | R-17602 | DOR-RWB-P6-E1055-INF-12 | 16, 18 | Definition of Ready item 12 Test cases: Partial | Needs section 7 criteria ownership and RTM v7 test lists for this story. Neither is in the chunk or in _work/msr/docs/C2-RTM notes. No TC row removed without them. |
| RWB-P6-E1055-INF | R-22182 | GAP-0366 | 3, 4, 5, 7, 12 | WIN file path, proof-of-delivery read and interaction ledger home move in the target | Proposed fix edits sections 3, 4, 5, 7, 12, which are not in the chunk, so no old text to copy. Section 18 REQ-ILG-004 already names the P1 ledger writer. |
| RWB-P6-E1055-OPS | R-11020 | CG-ALL-6446 | 12.8 | Criteria and test data read ACE views directly | The defective Given lines of TC-E1-055-02 and TC-E1-055-07 are in section 16, which is not in this chunk. Resend section 16. |
| RWB-P6-E1055-OPS | R-31286 | NEWAC-RWB-P6-E1055-OPS-AC12 | 8 | AC12: §8 BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC12 needs section 7 to anchor and its test row in section 16, neither in this chunk. The test proposal is Not specified in the source documents. Resend sections 7 and 16. |

## 5. Cross-document changes (pending in the target document)


### RWB-P6-E1055-CON (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10818 | RWB-P6-E1055-APP | DOR-RWB-P6-E1055-APP-21 | header | Move build status from Not started to Done for the contract story. |
| CDC-10819 | RWB-P6-E1055-APP | DOR-RWB-P6-E1055-APP-22 | header | Publish the contract fake library and record its version in the contract story. |
| CDC-10824 | RWB-P6-E1055-APP | GAP-0577 | 12.2 | Align the consumed row 1 path to GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= and the DP07 fake to the same path at the wave 1 contract freeze. |
| CDC-10825 | RWB-P6-E1055-APP | GAP-1043 |  | Publish the notice read by notice ID and the dispatch reference as one named operation with its field list, including the document reference field used by the INT-14 file. |
| CDC-10827 | RWB-P6-E1055-APP | GAP-1100 | 3 | Attach the WIN owner INT-14 and INT-15 specifications to the contract baseline as annexes with a version label; declare the file element as a shape until then, and treat a layout change as a new file version. |
| CDC-10848 | RWB-P6-E1055-CON | GAP-1043 | 12.2 | Publish the notice read by notice ID and the dispatch reference as one operation with named fields, including the field that carries the document reference. |
| CDC-10860 | RWB-P6-E1055-INF | DOR-RWB-P6-E1055-INF-21 |  | Set the contract story build status to Done so the contract is published. |
| CDC-10861 | RWB-P6-E1055-INF | DOR-RWB-P6-E1055-INF-22 |  | Publish a contract fake library version for this story and record its version. |
| CDC-10862 | RWB-P6-E1055-INF | DOR-RWB-P6-E1055-INF-23 | header | Fix and record the contract version this story builds against. |
| CDC-10871 | RWB-P6-E1055-INF | GAP-0577 |  | Publish GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= with the ten-field record, ascending pod_key order, page parameters and error set; align the consumed row at wave 1 freeze. |
| CDC-10872 | RWB-P6-E1055-INF | GAP-1043 |  | Publish the notice read by notice ID and the dispatch reference as one operation with named request and response fields, including the document reference field. |
| CDC-10877 | RWB-P6-E1055-INF | GAP-2243 | none | Confirm the element names of the NoticeDelivered.v1 delivery fields and the notice read at contract review; rename in this story if they differ. |
| CDC-10886 | RWB-P6-E1055-OPS | DOR-RWB-P6-E1055-OPS-21 | header | Set build status to Done (currently Not started) once the contract is published. |
| CDC-10887 | RWB-P6-E1055-OPS | DOR-RWB-P6-E1055-OPS-22 | 12.8 | Publish the contract fake library version and record it as published. |
| CDC-10888 | RWB-P6-E1055-OPS | DOR-RWB-P6-E1055-OPS-23 | header | Publish a fixed contract version and state it in the story's Contract dependencies row. |
| CDC-10898 | RWB-P6-E1055-OPS | GAP-1043 | Not in chunk | Publish the notice read by notice ID and the dispatch reference as one operation with named request and response fields, including the document reference used by the INT-14 file. |
| CDC-10900 | RWB-P6-E1055-OPS | GAP-1100 | Not in chunk | Attach the WIN owner INT-14 and INT-15 specifications as versioned annexes to the contract baseline and declare the file element as a shape until then. |
| CDC-10902 | RWB-P6-E1055-OPS | GAP-2243 | n/a | Confirm the JSON element names of rwb.comms.NoticeDelivered.v1 and of the notice read at contract review; no value, rule or criterion changes. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10731 | RWB-P6-E1049-APP | CG-ALL-6375 | Intro | Remove the closed sentType enum so LOV-SENT-TYPE values load as data without a schema change. |
| CDC-10816 | RWB-P6-E1055-APP | CG-ALL-6406 | 4 | Remove the fixed enum on deliveryStatus so LOV-DELIVERY values are read as data, as the story specifies. |
| CDC-10817 | RWB-P6-E1055-APP | CG-ALL-6407 | 4 | Remove the fixed enum on sentType so LOV-SENT-TYPE values are read as data, as the story specifies. |
| CDC-10837 | RWB-P6-E1055-CON | CG-ALL-6425 | 12.1 | Publish POST /api/recovery/comms/v1/internal/pod-digests (Idempotency-Key required, service identity only) in rwb-comms.yaml through the CON story, or remove it from 12.1. |
| CDC-20740 | RWB-P6-E1055-APP | R-01657 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20741 | RWB-P6-E1052-CON | R-21954 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20742 | RWB-P6-E1055-APP | R-01660 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20743 | RWB-P6-E1052-APP | R-22166 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20744 | RWB-P6-E1055-APP | R-06427 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20746 | RWB-P6-E1049-APP | R-01653 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20747 | RWB-P6-E1049-APP | R-06411 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20748 | RWB-P6-E1055-APP | R-01659 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20751 | RWB-P6-E1055-CON | R-01663 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10714 | RWB-P6-E1046-CON | DOR-RWB-P6-E1046-CON-12 | 16, 18 | Test cases added in section 16 (TC-E1-046-10 to 18); section 18 test lists not changed |
| CDC-10728 | RWB-P6-E1046-CON | CG-ALL-6370 | 18 | Align the TC-E1-046 entries for REQ-OCC-001 and REQ-OCC-002 with RWB-P6-E1046-CON section 18 in the next RTM version |
| CDC-10800 | RWB-P6-E1052-CON | CG-ALL-6398 | 18 | Align the REQ-OCC-001 test list in the RTM with section 18 of RWB-P6-E1052-CON in the next RTM version. |
| CDC-10830 | RWB-P6-E1055-APP | CG-ALL-6415 | 18 | Align the test lists of REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006 with section 18 of RWB-P6-E1055-APP in the next RTM version. |
| CDC-10852 | RWB-P6-E1055-CON | CG-ALL-6430 | n/a | Align its test lists for REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006 with section 18 of RWB-P6-E1055-CON in the next version. |
| CDC-10879 | RWB-P6-E1055-INF | CG-ALL-6438 | 18 | Align the test lists for REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006 with section 18 of this story in the next RTM version. |
| CDC-10903 | RWB-P6-E1055-OPS | CG-ALL-6445 | 18 | Align the test lists of REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006 with section 18 of RWB-P6-E1055-OPS in the next RTM version. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10715 | RWB-P6-E1046-CON | DOR-RWB-P6-E1046-CON-14 | none located | Record the signed epic design sign-off for RWB-P6-E1046-CON; none is in the story or the source documents. |
| CDC-10733 | RWB-P6-E1049-APP | DOR-RWB-P6-E1049-APP-14 | Header | Record the signed sign-off of the epic design for RWB-P6-E1049-APP. |
| CDC-10751 | RWB-P6-E1052-APP | DOR-RWB-P6-E1052-APP-14 | find it | Record the signed epic design sign-off for EP01 and link it to RWB-P6-E1052-APP. |
| CDC-10786 | RWB-P6-E1052-CON | DOR-RWB-P6-E1052-CON-14 | Header | Record the signed epic design sign-off for this story in the epic design record; the story cannot carry it from the sources. |
| CDC-10859 | RWB-P6-E1055-INF | DOR-RWB-P6-E1055-INF-14 |  | Record the signed epic design sign-off for RWB-P6-E1055-INF against the epic design record. |
| CDC-10885 | RWB-P6-E1055-OPS | DOR-RWB-P6-E1055-OPS-14 | header | Record the signed epic design sign-off for RWB-SVC-P6 in the epic design record. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10747 | RWB-P6-E1049-APP | GAP-1207 | 13, 14 | Add one LOV-NOTICE value for an operational notice to the case owner, named by the business owner, and set DF-LEG-018 from it. |
| CDC-10762 | RWB-P6-E1052-APP | GAP-0749 | 3 | Supply field IDs for the seven notice columns (notice reference, notice state, hold reason, template code, template version, document reference, delivery date) and the notice timeline event codes in LOV-LEDGER-EVENT. |
| CDC-10793 | RWB-P6-E1052-CON | GAP-0749 | find it | Assign field IDs to the seven notice columns on recovery_case and enumerate notice timeline event codes in LOV-LEDGER-EVENT. |
| CDC-10834 | RWB-P6-E1055-APP | GAP-1105 | 10 | Publish a versioned hold reason list with TEMPLATE_WITHDRAWN as its first row and add the other values with the business owner before Epic 2 dispatch refinements. |
| CDC-10883 | RWB-P6-E1055-INF | GAP-1105 |  | Publish hold_reason as a versioned list with TEMPLATE_WITHDRAWN as the first row; add the other hold reasons with the business owner before Epic 2 dispatch refinements. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10750 | RWB-P6-E1049-APP | GAP-1051 | 3 | Publish the per-case document count and the version depth with RWB-P1-E1065-CON. |
| CDC-10783 | RWB-P6-E1052-APP | GAP-1083 | - | Record that the Litigation right and scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON; add DP-08 and RWB-P4-E1037-CON to this story only if the check moves into the service. |
| CDC-10784 | RWB-P6-E1052-APP | GAP-2455 | - | Confirm that rwb-decision appends every DecisionRecorded fact to decision_log_entry, that the local record is the working record and the ledger entry is the record of record, and that RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0/wave-1 baseline outside the H row. |
| CDC-10811 | RWB-P6-E1052-CON | GAP-1083 | 9 | Record that the Litigation right and the scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON; DP-08 is not added to this story |
| CDC-10812 | RWB-P6-E1052-CON | GAP-2455 | 12.7 | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry; the producer's local record is the working record and the ledger entry is the record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0 and wave-1 baseline outside the H row |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10716 | RWB-P6-E1046-CON | DOR-RWB-P6-E1046-CON-1 | 1 | Add 'tech lead' as a role, or name the existing role code this story maps to; the story gives no role code to use. |
| CDC-10841 | RWB-P6-E1055-CON | DOR-RWB-P6-E1055-CON-1 | 1 | Add 'tech lead' of rwb-comms as a role code or role name, or name an existing role for section 1. |
| CDC-10864 | RWB-P6-E1055-INF | DOR-RWB-P6-E1055-INF-1 | 1 | Add a role code and name for infrastructure engineer, or confirm the existing role the story should use. |
| CDC-10891 | RWB-P6-E1055-OPS | DOR-RWB-P6-E1055-OPS-1 | 1 | Add 'platform engineer' as a role code or name, or confirm the role code that section 1 of RWB-P6-E1055-OPS should use. |

### RWB-P6-E1046-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10717 | RWB-P6-E1046-CON | DOR-RWB-P6-E1046-CON-10 | 12 | Add empty, loading, error and no access states for SCR-33 and SCR-40. |
| CDC-10719 | RWB-P6-E1046-CON | GAP-1064 | find it | Add the rwb-source-data data-dictionary contract (GET /api/recovery/source-data/v1/admin/data-dictionary/fields) to C, or confirm the published admin surface covers it; until then a fake with one hop and 2 s timeout (DP-11). |
| CDC-10725 | RWB-P6-E1046-CON | GAP-2345 | 16 | Add GET /admin/templates/current with code, language and onDate as an additive change within major version 1 |
| CDC-10758 | RWB-P6-E1052-APP | GAP-0357 | 8, 14 | Read the five template operations from the P6 contract in the registry under /api/recovery/comms/v1/admin/templates, keeping request, response, state and message unchanged. |

### RWB-P6-E1052-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10752 | RWB-P6-E1052-APP | DOR-RWB-P6-E1052-APP-21 | find it | Complete RWB-P6-E1052-CON and set its build status to Done (currently Not started). |
| CDC-10753 | RWB-P6-E1052-APP | DOR-RWB-P6-E1052-APP-22 | find it | Publish the contract fake library and record its version as published. |
| CDC-10767 | RWB-P6-E1052-APP | GAP-2454 | 11 | Fix the generation record payload: template code and version and merge snapshot reference in inputs_ref with ACE data date; notice reference and type in actions; hold or refusal and freshness message in outcome; final-call set GENERATED, HELD, REFUSED as a reference list. Mirror in Service Contract Catalog v1. |
| CDC-10798 | RWB-P6-E1052-CON | GAP-1265 | 12 | Add RWB-P1-E1015-CON and RWB-P3-E1018-CON as C rows of this key, or record both reads as route-level composites of RWB-PLT-N001-CON. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10765 | RWB-P6-E1052-APP | GAP-1082 | 12 | Publish the NoticeRequest and Notice schemas with required flags, and the NoticeGenerated payload, and confirm them with the app stories of this key. |
| CDC-10796 | RWB-P6-E1052-CON | GAP-1082 | 12 | Publish the NoticeRequest and Notice schemas with their required flags and the NoticeGenerated payload in rwb-comms API specification v5, and confirm them with the app stories of this key. |
| CDC-10842 | RWB-P6-E1055-CON | DOR-RWB-P6-E1055-CON-6 | 10 | Publish the authorise check that rwb-comms operations call so section 10 can name it; the check name is not in the source documents. |
| CDC-10847 | RWB-P6-E1055-CON | GAP-0577 | 12.2 | Publish the proof-of-delivery read as GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= with the ten-field record, ascending pod_key order, page parameters and error set; align the consumed row at the wave 1 freeze. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10797 | RWB-P6-E1052-CON | GAP-1264 | 12 | Name an owner path for the notice operations approve, regenerate and hold, or state one decision operation with an outcome code; correct the api rows and publish them on the rwb-comms contract. |
| CDC-10801 | RWB-P6-E1052-CON | GAP-2094 | header | Settle the path of the case-level notice list (Architecture v5 slide 17 GET /cases/{id}/notices) as a P6 rwb-comms operation and add it to the Endpoints sheet for P6. |
| CDC-10867 | RWB-P6-E1055-INF | GAP-2090 | find it | Hold barcode, callback date and delivery status as fields of the notice row; add a separate proof table only if a DB story needs it. |
| CDC-10875 | RWB-P6-E1055-INF | GAP-1101 |  | Record rwb-comms as owner of the REC-05 barcode break and rwb-source-data as owner of the References exception list and the data-quality read. |

### RWB-P1-E1066-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10822 | RWB-P6-E1055-APP | GAP-1097 |  | Add the pod records, freshness and batch-status elements of the pod data product with business date, feed version, batch status and stale marker. Until then use DP07 records and freshness GET paths, one hop, 2 s budget. |
| CDC-10845 | RWB-P6-E1055-CON | GAP-1097 | 12.2 | Add the pod records, freshness and batch-status elements of the pod data product with business date, feed version, batch status and stale marker; until then consume DP07 records and freshness endpoints with a 2 s budget. |
| CDC-10869 | RWB-P6-E1055-INF | GAP-1097 |  | Add the DP07 pod records, freshness and batch-status elements, with business date, feed version, batch status and stale marker, each with its operation name and fields. |
| CDC-10895 | RWB-P6-E1055-OPS | GAP-1097 | Not in chunk | Add the pod records, freshness and batch-status elements of the pod data product, with business date, feed version, batch status and stale marker, as named operations and fields. |

### RWB-P5-E1054-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10823 | RWB-P6-E1055-APP | GAP-1099 |  | Name the stored letter read operation of the document hub and its claim-check handle. Until then use GET /api/recovery/document/v1/documents/{documentId}, one hop, 2 s budget; a missing letter is a held notice. |
| CDC-10846 | RWB-P6-E1055-CON | GAP-1099 | 12.3 | Name the stored letter read and its claim-check handle, returning metadata for notice.document_id; until then consume GET /api/recovery/document/v1/documents/{documentId} with a 2 s budget and treat a missing letter as held. |
| CDC-10870 | RWB-P6-E1055-INF | GAP-1099 |  | Name the operation and element that return the stored letter of a notice, and state whether it returns metadata or a claim-check handle. |
| CDC-10896 | RWB-P6-E1055-OPS | GAP-1099 | Not in chunk | Name the document read that returns the stored letter of a notice and its claim-check handle, consumed through the document hub. |

### OTHER:Message catalogue (FSD P5 upload exception flow) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10832 | RWB-P6-E1055-APP | GAP-1046 | 14 | Add the text of MSG-P5-016 to the message catalogue so the upload refusal shows a written message. |
| CDC-10854 | RWB-P6-E1055-CON | GAP-1046 | 14 | Add the text of MSG-P5-016 (malware found) to the message catalogue so the 422 upload refusal shows a written message. |
| CDC-10882 | RWB-P6-E1055-INF | GAP-1046 | none | Add the text of MSG-P5-016 (malware found, 422) to the message catalogue; Not specified in the source documents (GAP-1046). |
| CDC-10906 | RWB-P6-E1055-OPS | GAP-1046 |  | Add the text of MSG-P5-016 (malware found, 422 response) to the message catalogue. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10835 | RWB-P6-E1055-APP | GAP-2246 |  | Allocate the Data Dictionary field ID for the nullable notice reference column and its index on the timer table, and add it to the ownership map at the next revision. |
| CDC-10857 | RWB-P6-E1055-CON | GAP-2246 | 9 | Allocate a Data Dictionary field ID for the nullable notice reference column on timer and add it to the ownership map at the next revision. Column, type and index stand as written. |
| CDC-10884 | RWB-P6-E1055-INF | GAP-2246 |  | Allocate the Data Dictionary field ID for the nullable notice reference column on timer and add it to the ownership map at the next revision. |
| CDC-10909 | RWB-P6-E1055-OPS | GAP-2246 |  | Allocate the Data Dictionary field ID for the nullable notice reference column on the timer table and add it to the ownership map. |

### RWB-P5-E2026-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10729 | RWB-P6-E1046-CON | GAP-2344 | header | Name request fields of GenerateRequest and RegenerateRequest, the regenerate reason field, the refused-document error body, index ix_document_template and the Flyway step name |
| CDC-10741 | RWB-P6-E1049-APP | GAP-0998 | 12 | Add rwb.document.OcrCompleted.v1 (eight fields, no personal data) to the rwb-document event catalogue and its two-event count. |
| CDC-10773 | RWB-P6-E1052-APP | GAP-2348 | n/a | Name the request and reason fields of GenerateRequest and RegenerateRequest and the answer shape; RWB-PLT-DB fixes the login names; document type load publishes container name and MSG-P5-006 text. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10754 | RWB-P6-E1052-APP | CG-ALL-6386 | 16 | Add a row for TC-E1-052-11 with Given, When and Then copied from AC9 and BR11 in the next Test Cases version. |
| CDC-10756 | RWB-P6-E1052-APP | DOR-RWB-P6-E1052-APP-12 | 12, 12.7, 16 | Add tab Story test cases rows for TC-E1-052-11 and TC-E1-052-12 to TC-E1-052-16 under the same IDs; TC-E1-052-07 keeps BR9 only. |
| CDC-10799 | RWB-P6-E1052-CON | CG-ALL-6396 | 16 | Add rows for TC-E1-052-11 to the Story test cases tab in the next version, with Given, When and Then copied from AC9 of RWB-E1-052. |

### RWB-P3-E1018-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10759 | RWB-P6-E1052-APP | GAP-1149 | 12 | Publish the rwb-case operation, task code, target queue and fields for the litigation officer task, carrying template code, version, language, case, notice type and MSG-P6-003. Record code and queue in the service values file. |
| CDC-10760 | RWB-P6-E1052-APP | GAP-1085 | 12 | Publish the rwb-case task-raise operation (or the event that creates a task) and record it in the ownership map. |
| CDC-10790 | RWB-P6-E1052-CON | GAP-1085 | find it | Publish the task-raise operation or the task-creating event of rwb-case and record it in the Ownership Map. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10821 | RWB-P6-E1055-APP | CG-ALL-6413 | 12.5 | Add Activities row generateLetter (rwb-comms; calls rwb-document P5), or name a catalogued activity in the story. |
| CDC-10840 | RWB-P6-E1055-CON | CG-ALL-6428 | 12.5 | Add activity generateLetter (P6, task queue rwb-comms) to the Activities sheet, or switch 12.5 to a catalogued activity. |
| CDC-10892 | RWB-P6-E1055-OPS | DOR-RWB-P6-E1055-OPS-8 | 12 | Add activity generateLetter, or confirm the catalogue version that holds it. Workflow ID form and start rule stated as not specified in section 12. |

### RWB-P6-E1055-INF (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10828 | RWB-P6-E1055-APP | GAP-1102 | 3 | Record host, port, zone, certificate subject and owner, container names, retention and sizes as reviewed values per environment; confirm with the WIN owner and Security before SIT cutover. |
| CDC-10850 | RWB-P6-E1055-CON | GAP-1102 | n/a | Record host, port, zone, certificate subject and owner, container names, retention and file sizes as reviewed values per environment; confirm with WIN owner and Security before SIT cutover. |
| CDC-10901 | RWB-P6-E1055-OPS | GAP-1102 | n/a | Record host, port, network zone, certificate subject and owner, container names, retention and file sizes as reviewed values per environment, confirmed with the WIN owner and Security before SIT cutover. |

### RWB-P6-E1055-OPS (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10829 | RWB-P6-E1055-APP | GAP-1103 | 12.5 | Fix the deployment slot and namespace under DL35 with the platform team; name the dispatch Schedule; record the Airflow window call in the runbook; assert both in the registration step. |
| CDC-10851 | RWB-P6-E1055-CON | GAP-1103 | n/a | Fix the deployment slot and namespace under DL35 with the platform team, name the Schedule, record the Airflow window call in the runbook and assert both in the registration step. |
| CDC-10876 | RWB-P6-E1055-INF | GAP-1103 |  | Fix the deployment slot and namespace under DL35, name the Schedule, record the Airflow window call (task, signal or business date parameter) in the runbook, and assert both in the registration step. |

### OTHER:TSD P6 T3.1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10722 | RWB-P6-E1046-CON | GAP-1066 | 11 | Staff identifier to uuid conversion is not in any source; the story now states it as Not specified. |
| CDC-10723 | RWB-P6-E1046-CON | GAP-1067 | 12.1 | Current-version filter added to API-P6-003 with a Not specified marker |

### OTHER:TSD P6 v2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10727 | RWB-P6-E1046-CON | GAP-2392 | 12.7 | Add treatment-type and product-group filters to API-P6-003 and an application/json representation of API-P6-005 as additive changes within major version 1 |
| CDC-10761 | RWB-P6-E1052-APP | GAP-1084 | 11 | Give the party reference its own field ID, keep person_key as the notice business key, and correct DF-LEG-030 in the module specification or the legacy field list. |

### RWB-P5-E1049-INF (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10743 | RWB-P6-E1049-APP | GAP-0997 |  | Name the OCR engine product, endpoint, engine version and page limit with the provider owner; set the business-hours window and the four parameter rows as data at the wave 1 entry check; keep row RWB-P5-E1049-INF until then. |
| CDC-10745 | RWB-P6-E1049-APP | GAP-1000 |  | Set the OCR engine capacity ceiling, admission queue depth, bytes per page and container quota at the capacity review with the OCR provider owner. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10757 | RWB-P6-E1052-APP | DOR-RWB-P6-E1052-APP-9 | 14 | Confirm the MSG-P1-001 wording against v4 or the rwb-source-data catalog text, and state which text this story carries. |
| CDC-10770 | RWB-P6-E1052-APP | CG-ALL-6385 | 14 | MSG-P1-001 wording reverted to the legacy text; the v4 wording is not in this chunk |

### 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10764 | RWB-P6-E1052-APP | GAP-1081 | 4 | Name the merge snapshot store (a snapshot table or a column on the local decision record) and publish it in the next physical-schema version. |
| CDC-10795 | RWB-P6-E1052-CON | GAP-1081 | find it | Name the merge snapshot store (table or column on the local decision record) and publish it in the next physical-schema version. |

### RWB-P1-E1015-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10771 | RWB-P6-E1052-APP | GAP-1080 | n/a | Publish the data-product record shape of DP01 Account and arrears and DP07 Legal, naming each returned field and its source column. |
| CDC-10802 | RWB-P6-E1052-CON | GAP-1080 | 15 | Publish the data-product record shape of DP01 Account and arrears and DP07 Legal, naming each returned field and its source column. |

### OTHER:Recovery Workbench Notification and Correspondence Design (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10775 | RWB-P6-E1052-APP | GAP-2087 | n/a | Name the document version 3 from the file name; add Source version row 1, 28 October 2026; change log carries both readings. |
| CDC-10804 | RWB-P6-E1052-CON | GAP-2087 | header | Take the file name as the family version so the design becomes version 3, add a Source version row (1, 28 October 2026), and record both readings in the change log. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10778 | RWB-P6-E1052-APP | GAP-0752 | n/a | Show P3 as a consumer of P6 in slide 13 (E in the P6 column); the request stays a REST call inside a CaseWorkflow activity. |
| CDC-10806 | RWB-P6-E1052-CON | GAP-0752 | 12.1 | Mark P3 Case as a consumer of the P6 answer in the E cell of slide 13; keep POST /notices as a REST request from the CaseWorkflow activity |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10779 | RWB-P6-E1052-APP | GAP-0753 | n/a | Add the case-side notice request switch key with default on, owner RW-COE; RWB-PLT-DB names the rwb-case service login. |
| CDC-10807 | RWB-P6-E1052-CON | GAP-0753 | header | Add the case-side notice-request switch key (name: Not specified in the source documents (GAP-0753)), default on, owner RW-COE; name the rwb-case service login in the platform DB story |

### OTHER:FSD P5 document type table (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10826 | RWB-P6-E1055-APP | GAP-1044 |  | Add a WIN proof-of-delivery receipt type with retention class and write-once flag, or confirm which existing type it uses, and confirm the DEMAND to DEMAND_LETTER mapping at the next table version. |
| CDC-10899 | RWB-P6-E1055-OPS | GAP-1044 | Not in chunk | Add a proof-of-delivery receipt type with its retention class and write-once flag, and confirm the DEMAND to DEMAND_LETTER mapping, at the next type table version. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10844 | RWB-P6-E1055-CON | GAP-2096 | 12.2 | Add a consumer row for a proof arrival that reads through the P1 contract on the ACE batch business date, matches by barcode and publishes EV-15 NoticeDelivered from rwb-comms; add no new event or job. |
| CDC-10868 | RWB-P6-E1055-INF | GAP-2096 | find it | Add the proof read through the P1 contract on the ACE batch business date, the barcode match to the notice, and the EV-15 NoticeDelivered publish from rwb-comms, with producer and consumer rows. |

### 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20889 | RWB-P6-E1055-INF | R-09188 |  | WIN INT-14 file layout belongs in the rwb-integration INT-14 interface definition (contract item). No layout in any source, so none written here (GAP-1602). |
| CDC-20894 | RWB-P6-E1055-INF | R-22186 |  | WIN INT-14 and INT-15 layout annexes belong to the contract baseline. No layouts or version label are in any source (GAP-1100). |

### OTHER:rwb-document API file and TSD P5 T3.1 (document table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10718 | RWB-P6-E1046-CON | GAP-1023 | find it | Use POST /cases/{caseId}/generated-documents on /api/recovery/document/v1 (ASM-101); add template_code varchar(30) and template_version integer to document; partial unique index on (treatment_id, template_id) where DRAFT and is_active (ASM-103). |

### OTHER:rwb-comms API file and wave 1 harness (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10720 | RWB-P6-E1046-CON | GAP-1063 | find it | Record POST /admin/templates plus the approve and withdraw operations of /api/recovery/comms/v1 as the mapping of legacy POST /admin/reference-loads; keep the SHA-256 file-hash rule as upload idempotency; TC-E1-046-09 asserts refusal on the mapped operation. |

### OTHER:rwb-comms API file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10721 | RWB-P6-E1046-CON | GAP-1065 | 11 | State one resolution rule for bodyRef: a P5 rwb-document object when the body is a document-hub object, otherwise the service's own container; fix it before RWB-P6-E1052 generation is built. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10724 | RWB-P6-E1046-CON | GAP-2343 | 12.7 | Fix the per-service login name for rwb-document before the wave-1 contract tests. Identifier property of the version answer still open in RWB-P6-E1046-CON. |

### OTHER:FSD P7 v3 and TSD P7 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10726 | RWB-P6-E1046-CON | GAP-2453 | 12.7 | Make P7 hold one template_use record per accepted answer, not a catalog copy; fix its table, columns and migration file as the proposed fix states |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10730 | RWB-P6-E1046-CON | GAP-2346 | 7 | Record one owning story per legacy criterion and mark RWB-P5-E1046-APP as test-case-bearing but criterion-free, so traceability does not expect matching lists. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10732 | RWB-P6-E1049-APP | CG-ALL-6376 | 12.4 | Add rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1, produced by P5 rwb-document, with the 12.4 element list. |

### OTHER:Story backlog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10734 | RWB-P6-E1049-APP | DOR-RWB-P6-E1049-APP-21 | 12 | Create contract story RWB-P6-E1049-CON for the section 12 operations and events and add it as a CON dependency here. |

### RWB-P5-E1049-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10735 | RWB-P6-E1049-APP | DOR-RWB-P6-E1049-APP-22 | 12 | Publish the fake for the rwb.document.OcrRescanRequested.v1 envelope and record its library version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10736 | RWB-P6-E1049-APP | DOR-RWB-P6-E1049-APP-8 | not in chunk | rwb-comms.yaml: replace closed enum for sentType with a reference to LOV-SENT-TYPE. Kafka Catalog v1: add rwb.document.OcrRescanRequested.v1. HTTP 401, 403, 404 without message IDs: Not applied, no source gives the IDs. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-P5-E1049-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10737 | RWB-P6-E1049-APP | GAP-1205 | 12.4 | Publish rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1 from P5 rwb-document in the intake state change transaction, with the GAP-1205 element list. |

### OTHER:P3 screen specification for SCR-01; OTHER:SCR-31 and SCR-44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10738 | RWB-P6-E1049-APP | DOR-RWB-P6-E1049-APP-10 | find it | Removed the P5 owner label from the SCR-31 and SCR-44 rows |

### OTHER:rwb-access API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10739 | RWB-P6-E1049-APP | DOR-RWB-P6-E1049-APP-6 | 10 | Publish the authorise check for the notice read (GET /api/recovery/comms/v1/notices/{noticeId}; right R, notice area) under DP-08. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10740 | RWB-P6-E1049-APP | GAP-1590 | 12 | Restate AC-BG-P5-001-01 to AC-BG-P5-022-01 intake as an event-started DocumentIntakeWorkflow on queue rwb-document, with the 15-minute schedule raising the intake, and JOB-17 as a Temporal Schedule on the 1st Sunday monthly. |

### RWB-P5-E1049-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10742 | RWB-P6-E1049-APP | GAP-0362 | 13 | Keep OCR_MIN_QUALITY, OCR_WORKERS, OCR_TIMEOUT_SECONDS and OCR_MAX_ATTEMPTS in document_hub_parameter and read them as data; OCR_WORKERS is the worker concurrency cap while the platform scales on queue depth; keep the 60-minute target. |

### OTHER:TSD P5 T-A.1 and T3.1; OTHER:message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10744 | RWB-P6-E1049-APP | GAP-0999 | 14 | Publish derived property names for IntakeItem, OcrTextPage and IntakeStatus, the GET .../ocr-status path, the workflow input and output, and the not-found message ID. |

### RWB-P6-E1046-APP; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:platform integration owner (Notice answer and ACE path baselines) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10746 | RWB-P6-E1049-APP | GAP-1204 | 3, 12, 13 | Publish the rescan notice template row (code, version, language, body, channel); extend LOV-NOTICE with the business owner's value; baseline the Notice answer and the ACE request and result; set retry values and state list as data rows. |

### OTHER:Operations story that registers the JOB-12 Schedule (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10748 | RWB-P6-E1049-APP | GAP-1001 | none in this story | Set the business-hours window, the four alert thresholds and the deployment slot at the wave 1 entry check with the platform administrator; owner DevOps team. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10749 | RWB-P6-E1049-APP | GAP-1206 | 3, 13 | Add build rows RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, and contract rows RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-case contract row (ID not specified in the source documents). |

### OTHER:Screen Specifications v1 (SCR-01; OTHER:SCR-18; OTHER:SCR-30 state text) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10755 | RWB-P6-E1052-APP | DOR-RWB-P6-E1052-APP-10 | 15 | Empty, loading, error and no access marked per Screen Specifications v1 or as Not specified |

### RWB-P5-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10763 | RWB-P6-E1052-APP | GAP-1079 | 12 | Publish the rwb-document generated-document operation (POST /cases/{caseId}/generated-documents) with request, answer, failure shape and 2 s behaviour, and record it in the service contract catalog. |

### OTHER:rwb-comms contract (API-P6-001) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10766 | RWB-P6-E1052-APP | GAP-1086 | 12 | Publish one error row per condition for API-P6-001: withdrawn template as Held notice, repeat key with different body as 409, missing field as 422. |

### RWB-P5-E2017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10768 | RWB-P6-E1052-APP | GAP-1182 |  | Publish create, read-by-external-reference and update operations for signature_request before the wave 2 exit; section 12.2 placeholder and 12.8 fake stay until then. |

### RWB-P6-E4037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10769 | RWB-P6-E1052-APP | GAP-1125 |  | Declare POST and GET /notices/{noticeId}/payment-intents under /api/recovery/comms/v1 with Idempotency-Key on POST and statuses 401, 403, 404, 409, 422, 503; record HOME.SCB customer screen. |

### RWB-P5-E1055-APP; RWB-P5-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10772 | RWB-P6-E1052-APP | GAP-2351 | header | Schedule row names no owner; the JOB-17 owner is Not specified in the source documents |

### OTHER:RWB-P6-E1052 Work Package (H and C rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10774 | RWB-P6-E1052-APP | GAP-2350 | header | Add the platform contract stories for DP-03, DP-07, DP-09, DP-15, DP-19 and RWB-P5-E2026-CON to the H or C rows of this slice. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10776 | RWB-P6-E1052-APP | GAP-0750 | 3 | Reuse of D7.1 applied in section 3 |

### OTHER:Recovery Workbench P3 TSD v3; OTHER:T3.1 and T3.2 case task model (owner RW-COE) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10777 | RWB-P6-E1052-APP | GAP-0751 | 3 | Load task rows for the request task code and the hold task code (values Not specified in the source documents) with element type HUMAN_TASK and discretion REQUIRED. |

### OTHER:Recovery Workbench TSD P6 v2 (T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10780 | RWB-P6-E1052-APP | GAP-1087 | n/a | Add LOV-HOLD-REASON carrying POSTAL_ADDRESS and TEMPLATE_WITHDRAWN and any later value, read through the reference-data contract. |

### OTHER:AsyncAPI document of rwb-comms (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10781 | RWB-P6-E1052-APP | GAP-1088 | - | Publish the NoticeGenerated schema naming noticeId, caseId, templateId, templateVersion, noticeType and generatedAt; confirm it with rwb-decision and rwb-reporting. |

### OTHER:Split plan (traceability plan for the P5 and P6 key split) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10782 | RWB-P6-E1052-APP | GAP-2349 | - | Record one owning story per legacy criterion and mark secondary slices as test-case-bearing but criterion-free. |

### OTHER:TSD P6 (next version after v2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10785 | RWB-P6-E1052-APP | GAP-1115 | - | Correct the T8 mapping of REQ-OCC-011 from FEAT-COM-01 to FEAT-COM-04; no Litigation right claimed for dispute operations. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10787 | RWB-P6-E1052-CON | DOR-RWB-P6-E1052-CON-12 | 12, 12.7, 16, 18 | Add TC-E1-052-11 to tab Story test cases; align the section 18 test lists with RTM v7; drop test cases for criteria this story does not own. |

### OTHER:P6 API contract in the registry (rwb-comms) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10788 | RWB-P6-E1052-CON | GAP-0357 | find it | Name base and route of the five template operations under /api/recovery/comms/v1/admin/templates, keep requests, responses, states and messages unchanged, read the freshness stamp from the P1 freshness contract. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10789 | RWB-P6-E1052-CON | GAP-1238 | AC6, 12.3 | AC6 and 12.3 now read rwb.decision.DecisionRecorded.v1 per R-01656 |

### OTHER:TSD P6 v2 module specification (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10791 | RWB-P6-E1052-CON | GAP-1084 | 11 | Give the party reference its own field ID and correct DF-LEG-030 to person_key as the notice business key. |

### OTHER:P1 rwb-source-data data-product contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10792 | RWB-P6-E1052-CON | GAP-0364 | find it | Publish the ACE fact reads and the stale-batch signal as the P1 data-product contract; P6 reads through it and keeps merge snapshot as references only. |

### RWB-P5-E1052-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10794 | RWB-P6-E1052-CON | GAP-1079 | find it | Publish the request, answer, failure shape and 2 s behaviour of POST /cases/{caseId}/generated-documents. |

### RWB-P5-E2026-CON; OTHER:RWB-PLT-DB; OTHER:P5 document type load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10803 | RWB-P6-E1052-CON | GAP-2348 | header | Name the request and reason fields of GenerateRequest and RegenerateRequest and the answer shape; fix the rwb-document login names; publish the container name and the MSG-P5-006 text. |

### OTHER:TSD P3 v3 (T3.1; OTHER:T3.2) and case model reference data via rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10805 | RWB-P6-E1052-CON | GAP-0751 | header | Load the request task code and the notice task code, HUMAN_TASK element type, REQUIRED discretion and status values as case-model task rows through the reference-data contract. |

### OTHER:TSD P6 v2 T3.2 list of values (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10808 | RWB-P6-E1052-CON | GAP-1087 | 7 | Add LOV-HOLD-REASON carrying POSTAL_ADDRESS and TEMPLATE_WITHDRAWN and any later value; read it through the reference-data contract |

### OTHER:rwb-comms AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10809 | RWB-P6-E1052-CON | GAP-1088 | 12.2 | Publish NoticeGenerated with noticeId, caseId, templateId, templateVersion, noticeType and generatedAt; confirm with rwb-decision and rwb-reporting |

### OTHER:Split plan and traceability reports (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10810 | RWB-P6-E1052-CON | GAP-2349 | 16 | Mark RWB-P5-E1052-APP as test-case-bearing but criterion-free and record one owning story per legacy criterion AC1 to AC9 |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10813 | RWB-P6-E1052-CON | GAP-2389 | 12.8 | Add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON, and RWB-P3-E1042-CON and RWB-P3-E1043-CON, to the C list; keep H empty |

### RWB-P6-E2021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10814 | RWB-P6-E1052-CON | GAP-1094 | 8 | Fix the Notice component as id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus, sentType, holdReason, dispatchFileId and dispatchAttempts. Make all optional except id and caseId. Validate the additive rule against the Notice of RWB-P6-E1052-CON. |

### RWB-P6-E1055-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10815 | RWB-P6-E1055-APP | CG-ALL-6404 | 12.1 | Publish POST /api/recovery/comms/v1/internal/pod-digests in rwb-comms.yaml through the CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; OTHER:rwb-source-data API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10820 | RWB-P6-E1055-APP | DOR-RWB-P6-E1055-APP-8 |  | Add POST /internal/pod-digests to rwb-comms.yaml; publish GET /api/recovery/source-data/v1/data-products/DP07/records in rwb-source-data; make deliveryStatus and sentType LOV-driven or align the story; resolve the 6 further failures. |

### OTHER:FSD (A2, proof of delivery) and TSD P5 field_definitions for the receipt type (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10831 | RWB-P6-E1055-APP | GAP-1045 | 11 | Name the field names of the receipt facts (barcode, callback date, delivery status, sent type) and state whether a receipt is one document per file or one per notice. |

### OTHER:rwb-comms values files and runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10833 | RWB-P6-E1055-APP | GAP-1104 | 13 | Set the alert thresholds, the late-batch reviewed time and the Schedule state per environment, confirmed at UAT and recorded in the runbook. |

### OTHER:FSD P6 Communications v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10836 | RWB-P6-E1055-APP | GAP-1194 |  | Record in the next version that the officer-recorded path of this story is the manual correction path of the same notice. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10838 | RWB-P6-E1055-CON | CG-ALL-6426 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP07/records through the P1 provider story RWB-P1-E1066-CON. |

### OTHER:rwb-integration WIN dispatch file interface definition (INT-14) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10839 | RWB-P6-E1055-CON | GAP-1602 | header | Hold a versioned file layout as a contract item before wave 2: record set, field list, field order, envelope, naming, encoding, barcode and sent date return. |

### OTHER:Reconciliation check register (REC codes) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10843 | RWB-P6-E1055-CON | GAP-1169 | find it | Give the notice barcode break its own check code, keep REC-05 for the business-key orphan check, and align RWB-E1-055 and RWB-E1-011. |

### OTHER:Document type table (FSD P5 AC-ALT-P5-003-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10849 | RWB-P6-E1055-CON | GAP-1044 | 10 | Add a WIN proof-of-delivery receipt type with its retention class and write-once flag, and confirm the DEMAND to DEMAND_LETTER mapping at the next type table version. |

### OTHER:FSD P6 v3 (A2 proof of delivery) and TSD P5 (field_definitions of the receipt type) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10853 | RWB-P6-E1055-CON | GAP-1045 | 11 | Name the four receipt fields (barcode, callback date, delivery status, sent type) in the receipt type field_definitions and state the receipt granularity in FSD A2 for proof of delivery. |

### OTHER:rwb-comms values files and the runbook entry for each alert (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10855 | RWB-P6-E1055-CON | GAP-1104 | 9 | Set the alert thresholds, windows, evaluation interval and the reviewed late-batch time in the values files; confirm at UAT with the service owner and platform observability owner; record each agreed value in its runbook entry. |

### OTHER:TSD P6 v2 (hold_reason reference list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10856 | RWB-P6-E1055-CON | GAP-1105 | 10 | Publish the hold reason list as a versioned reference list with TEMPLATE_WITHDRAWN as its first row, and add the other hold reasons with the business owner before the Epic 2 dispatch refinements. |

### OTHER:split_plan.json (RWB-E2-018 slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10858 | RWB-P6-E1055-CON | GAP-1184 | 9 | Record that the three signature-request operations use the baseline in section 12.1 of their own story until a RWB-P6-E2018-CON exists. A later CON takes it over without code change. |

### OTHER:rwb-integration interface definition for INT-14 WIN file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10863 | RWB-P6-E1055-INF | GAP-1602 | header | Publish the versioned WIN dispatch file layout: record set, fields, order, envelope, naming, encoding, barcode and sent-date return. |

### OTHER:RWB-E1-011 and RWB-E1-055 (legacy stories) and the check register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10865 | RWB-P6-E1055-INF | GAP-1169 | find it | Give the notice barcode break its own code in both stories; keep REC-05 for the business-key orphan check and its result rows of RWB-E1-011. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:ACE team (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10866 | RWB-P6-E1055-INF | GAP-1597 | find it | State that proof rows are read through rwb-source-data's contract and applied by barcode to the notice held in rwb-comms; ACE team settles the writer of v_ace_pod. |

### OTHER:FSD P5 document type table (AC-ALT-P5-003-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10873 | RWB-P6-E1055-INF | GAP-1044 |  | Add the proof-of-delivery receipt type with its retention class and write-once flag, and confirm the DEMAND to DEMAND_LETTER mapping. Retention class value not specified in the source documents (GAP-1044). |

### OTHER:WIN owner INT-14 and INT-15 specifications, attached to the contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10874 | RWB-P6-E1055-INF | GAP-1100 |  | Attach the WIN owner INT-14 and INT-15 layouts as annexes with a version label; treat any layout change as a new file version. |

### RWB-P6-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10878 | RWB-P6-E1055-INF | GAP-1098 | 16 | Record gateway-bff enforcement of the declared Litigation R right; add the P4 authorise contract as C dependency or state that a service identity call carries no user right. |

### RWB-P3-E5002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10880 | RWB-P6-E1055-INF | GAP-2247 | none | Revisit notice-period clock ownership at the wave 3 refinement, keeping one clock with the unique running index and the idempotency key of notice and delivered date. |

### OTHER:field_definitions of the WIN receipt type (P5) and FSD P1 A2 proof-of-delivery section (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10881 | RWB-P6-E1055-INF | GAP-1045 | none | Name the four receipt fields and state the receipt granularity (one document per file or per notice); Not specified in the source documents (GAP-1045). |

### OTHER:rwb-integration interface definition for INT-14 WIN (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10889 | RWB-P6-E1055-OPS | GAP-1602 | header | Publish the versioned WIN dispatch file layout (record set, fields, order, envelope, naming, encoding, barcode and sent date return) before wave 2. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10890 | RWB-P6-E1055-OPS | CG-ALL-6443 | 12.5 | Add the generateLetter activity (P6, rwb-comms) to the Activities sheet or name a catalogued activity instead. |

### OTHER:TSD P1 v3 (T3.2; OTHER:T3.7; OTHER:Appendix T-A) and FSD P1 v3 A2.1.4 (rwb-source-data proof-of-delivery read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10893 | RWB-P6-E1055-OPS | GAP-0579 |  | Answer 200 with no row; the ten fields marked not available with reason SECTION_B_NOT_DEPLOYED; DP07 STALE and MSG-P1-001; behind platform flag rwb.dataengine.pod-read. Never an empty list alone, never a guessed date, never a fallback to data_as_of. |

### RWB-P6-E1055-CON; RWB-P6-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10894 | RWB-P6-E1055-OPS | GAP-0578 |  | rwb-source-data's ledger writer writes the delivery entry for the caseId named on the read, in the same transaction as the read; rwb-comms writes only the dispatch entry; a read without caseId writes nothing. |

### RWB-P6-E1055-CON; OTHER:TSD P1 v3 Appendix T-A.1 row API-P1-010 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10897 | RWB-P6-E1055-OPS | GAP-0577 |  | Publish GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= with the ten-field record in ascending pod_key order, its page parameters and its error set; align the consumed row and the fake at the wave 1 contract freeze. |

### OTHER:Message catalogue under OQ-P1-07 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10904 | RWB-P6-E1055-OPS | GAP-0581 | 14 | MSG-P1-001 text restored to the original message standard |

### OTHER:TSD P5 (T3.1 field_definitions) and FSD P6 v3 A2 (proof of delivery) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10905 | RWB-P6-E1055-OPS | GAP-1045 |  | Name the field_name of the barcode, callback date, delivery status and sent type facts for the receipt type, and state whether a receipt is one document per file or per notice. |

### OTHER:rwb-comms values files and runbook entries (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10907 | RWB-P6-E1055-OPS | GAP-1104 | 8 | Set the alert thresholds, the reviewed late-batch time and the Schedule state per environment; confirm at UAT with the service owner and platform observability owner. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10908 | RWB-P6-E1055-OPS | GAP-1105 |  | Publish a versioned hold reason list with TEMPLATE_WITHDRAWN as its first row and add the other values with the business owner. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20755 | RWB-P6-E1052-CON | R-28613 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0360 | Reference-load owner, field-ID check and template body storage move in the target | Solution architect | Resolved (directive) |
| GAP-0362 | OCR trigger, worker count and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0364 | Cross-service notice path, merge snapshot home and stale-batch signal are not named for the target | Tech lead | Resolved (directive) |
| GAP-0366 | WIN file path, proof-of-delivery read and interaction ledger home move in the target | Tech lead | Resolved (directive) |
| GAP-0577 | The address, the answer envelope and the paging of the proof-of-delivery read of rwb-source-data are not fixed by any source: the sources name a data-product records path, the contract of this key names another, and no source names the page parameters, the element types or the error set | Solution architect | Resolved (directive) |
| GAP-0578 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Solution architect | Resolved (directive) |
| GAP-0579 | No source names what the proof-of-delivery read answers before RWB-ACE-001 deploys the Section B views, nor the flag that holds it: the sources require the feature to stay behind a flag and the product to show stale, and give neither the answer shape, the reason code nor the flag name | Solution architect | Resolved (directive) |
| GAP-0580 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | Data architect | Resolved (directive) |
| GAP-0581 | No source fixes the render of MSG-P1-001 for the WIN proof of delivery: the legacy story names the product 'DP07 Legal', the FSD names the ACE batch and the product code, and the date is either the last complete business date or the due date | Business analyst | Resolved (directive) |
| GAP-0749 | No field IDs for the notice facts on recovery_case, and no event code list for the notice timeline entries | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0750 | The decision code and the final call of the case-side notice record are only partly specified | RW-COE | Resolved (directive) |
| GAP-0751 | The task model values of the request task and of the task Complete notice data are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0752 | Architecture v5 gives P3 as a listener of P6, while the P6 contract accepts a REST notice request | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0753 | The per-service login name and the case-side feature switch key are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0997 | OCR engine product, endpoint, engine version, capacity, intake request property names and the business-hours window are not named in the sources | Tech lead | Resolved (directive) |
| GAP-0998 | The pipeline publishes a third event name on rwb.document.events.v1 while the architecture catalogue lists two events for rwb-document | Solution architect | Resolved (directive) |
| GAP-0999 | Field-level names of IntakeItem, OcrTextPage and IntakeStatus, the OCR status path and the not-found message ID are not specified | Tech lead | Resolved (directive) |
| GAP-1000 | OCR engine capacity, admission queue depth, per-page text size and container quota are not named in the sources | SCB IT infrastructure | Resolved (directive) |
| GAP-1001 | The business-hours window, the deployment slot and the alert thresholds of the document intake pipeline are not specified | DevOps team | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1043 | The rwb-comms operations and field names behind RWB-P6-E1055-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1044 | The document type of the WIN proof-of-delivery receipt and the notice-type to document-type mapping | Center of excellence analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1045 | The field names of the WIN receipt in document_field and the receipt granularity | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1046 | The text of MSG-P5-016 | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1063 | The legacy template and catalog load path is replaced by the TSD admin template operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1064 | The data-dictionary read has no contract dependency in the plan | Solution architect | Resolved (directive) |
| GAP-1065 | No source says where the template body object lives | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1066 | The approver identity type of a template version is not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1067 | The request and answer field names of the five admin operations are not in T-A.2 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1068 | The service-side guard on the admin operations is not specified and DP-08 is not declared | Solution architect | Resolved (directive) |
| GAP-1079 | The rwb-document contract used for the write-once generated PDF has no contract dependency row | Solution architect | Resolved (directive) |
| GAP-1080 | The field names behind the rwb-source-data data-product contract are not specified | Solution architect | Resolved (directive) |
| GAP-1081 | Where the merge snapshot is persisted is not specified | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1082 | The request and answer field list of the notice operations is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1083 | The scope and right check of the notice operations has no rwb-access dependency row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1084 | Field DF-LEG-030 is party_id in the module specification and person_key in the legacy story | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1085 | No operation in the ownership map raises a task on rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1086 | The error code of each refusal condition on the notice POST is not fixed | Solution architect | Resolved (directive) |
| GAP-1087 | The hold reason value set is not enumerated in a list of values | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1088 | The NoticeGenerated payload element list is not enumerated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1094 | The Notice response fields and types are named by the legacy story but not specified by the contract sources | Tech lead | Resolved (directive) |
| GAP-1096 | The message text of MSG-P6-005 and MSG-P3-005 is not given by the legacy story or the P6 extracts | Tech lead | Resolved (directive) |
| GAP-1097 | The pod and batch-status contract elements are not named in RWB-P1-E1066-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1098 | No access guard story covers the notice read of rwb-comms | Solution architect | Resolved (directive) |
| GAP-1099 | The stored letter retrieval is not named in RWB-P5-E1054-CON | Solution architect | Resolved (directive) |
| GAP-1100 | The INT-14 and INT-15 fixed layouts, their record keys and their transport are not in the source material | Solution architect | Resolved (directive) |
| GAP-1101 | The owner of REC-05 and of the References exception list is not named | Solution architect | Resolved (directive) |
| GAP-1102 | The WIN host, port, zone, certificate owner, container names and file sizes are not in the source material | SCB IT infrastructure | Resolved (directive) |
| GAP-1103 | The deployment slot and namespace of rwb-comms, and the exact form of the JOB-10 Airflow handoff, are not specified | DevOps lead | Resolved (directive) |
| GAP-1104 | No source gives the alert thresholds, the reviewed time of the late WIN batch or the Schedule state per environment | DevOps lead | Resolved (directive) |
| GAP-1105 | Only one hold reason is named for a notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1115 | RWB-E4-038: the legacy screen, permission and endpoint rows describe notice administration, not a customer dispute, and TSD P6 T8 maps its requirement to another feature | Business analyst, P6, at the story review | Resolved (directive) |
| GAP-1125 | No source names an operation or a screen for FEAT-COM-03: the endpoint inventory stops at API-P6-011 and the legacy story copies the two notice operations | Tech lead | Resolved (directive) |
| GAP-1132 | No source states which event a digital view raises, and the proof-of-delivery element has two possible paths | P6 service owner and event owner | Resolved (directive) |
| GAP-1149 | The task target of a withdrawn template and the resumption of held generation are not specified | Business analyst, P6 | Resolved (directive) |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1182 | The published P5 document names no operation to create, read by external reference or update a signature request | Solution architect | Resolved (directive) |
| GAP-1184 | The plan holds no RWB-P6-E2018-CON, so the three signature-request operations have no published contract story | Solution architect | Resolved (directive) |
| GAP-1194 | The source reads the proof of delivery from v_ace_pod in process, and this story may read no ACE view | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1204 | The values the rescan notice needs are not named in any source | Business analyst, P6 | Resolved (directive) |
| GAP-1205 | The document rescan event that triggers the notice is in no event catalogue and has no name or payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1207 | The notice list of values has no value for an operational rescan notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1208 | The document token of the rescan message has no named reference form | Business analyst, P6 | Resolved (directive) |
| GAP-1238 | Two ce_type values are published for DecisionRecorded | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1264 | The three notice operations of the legacy NoticeApi have no owner path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1268 | The notice summary excludes the PDF body and the addressee that the legacy screen shows | Data steward | Resolved (directive) |
| GAP-1590 | The FSD makes document intake a 15-minute scheduled job while Architecture v5 makes it an event-started workflow with KEDA workers | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-2087 | The source reads version 1 in its metadata table and v2 in its file name | Document owner of the notification and correspondence design | Resolved (directive) |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2243 | Element names of the delivery fact and of the notice answer are not in the sources read for this work package | TechX and rwb-comms contract owner | Resolved (directive) |
| GAP-2246 | The timer has no field for the notice it belongs to, and its field ID is unallocated | rwb-case data owner and the Data Dictionary owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2247 | The notice period is owned by two rwb-case stories of the same legacy loop | TechX | Resolved (directive) |
| GAP-2343 | The catalog version answer read by rwb-document, its field names and the rwb-document login name are not specified, and the legacy document-to-template key becomes a soft cross-service reference | Solution architect, with the P5 TechX squad and the P6 rwb-comms squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2344 | The dependency rows of this slice name one contract only, and the request field names, the reason field, the index name and the migration step name are not specified | Solution architect, with the P5 TechX squad | Resolved (directive) |
| GAP-2345 | The rwb-comms catalog baseline declares no operation that answers the current Approved version for a template code, language and date | Tech lead of rwb-comms, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2346 | This slice owns no legacy acceptance criterion while the Work Package lists all nine legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2348 | The rwb-document login, the request and answer field names of the generation path, the message text of MSG-P5-006, the container name, the index name, the Flyway step name and the P5 feature flag are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2349 | This slice owns no legacy acceptance criterion while the Work Package lists all eleven legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2350 | The dependency rows of this slice name one contract only, while the pattern set names five platform contracts, the rwb-case reference-data contract and the generation contract of the service | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2363 | The legacy screen, endpoints and rights of RWB-E4-035 serve an officer's notice screen, not a customer's offer view | Solution architect | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2454 | The D7.1 generation record has no field layout, no final-call set and no message text in the sources | TechX | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P6-E1049-APP | Not specified without item ID | 322 | Errors: 401 (Not specified in the source documents (CG-ALL-6374)), 403 (MSG-P4-002), 404 (Not specified in the source documents (CG-ALL-6374)), 503. The read is |
| RWB-P6-E1052-APP | unknown story key | 25 | RWB-P5-E1052-CON is not a story of the set: \| Contract dependencies \| RWB-P3-E1043-CON, RWB-P1-E1015-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON, RWB-P5-E1052-CON, RWB-P5-E2026-CON \| |
| RWB-P6-E1052-APP | unknown story key | 66 | RWB-P5-E1052-CON is not a story of the set: - Notice generation is driven through POST /cases/{caseId}/notices on rwb-comms (GAP-0364). The ACE facts and the stale-batch signal are rea |
| RWB-P6-E1055-CON | skipped AC ID | 91 | missing: AC9, AC10, AC11 |
| RWB-P6-E1055-INF | skipped AC ID | 90 | missing: AC7, AC8, AC9, AC10, AC11 |
