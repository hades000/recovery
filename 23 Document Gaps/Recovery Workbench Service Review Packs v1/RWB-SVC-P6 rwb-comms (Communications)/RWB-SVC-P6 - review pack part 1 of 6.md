# RWB-SVC-P6 rwb-comms (Communications) - review pack, part 1 of 6 (RWB-P6-AD017-APP to RWB-P6-E1046-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 160 |
| Cross-document (pending in another document) | 215 |
| Not applied (value not in the sources) | 20 |
| Open business decisions | 24 |
| Register gaps linked | 159 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P6-AD017-APP | 16 | 7 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 AD017 APP Manage letter and notice templates v2.md |
| RWB-P6-AD017-CON | 14 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 AD017 CON Manage letter and notice templates - contract v2.md |
| RWB-P6-E1007-APP | 34 | 44 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1007 APP Integration adapters for outbound files v2.md |
| RWB-P6-E1011-APP | 29 | 50 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1011 APP Reconciliation and data quality report v2.md |
| RWB-P6-E1019-APP | 16 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1019 APP Roles, teams and queues as data v2.md |
| RWB-P6-E1032-APP | 17 | 39 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1032 APP Automatic attach from the OCR intake v2.md |
| RWB-P6-E1034-APP | 17 | 12 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1034 APP Letter template management v2.md |
| RWB-P6-E1046-APP | 17 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1046 APP Template and merge field catalog as data v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P6-E1032-APP | R-01652 | CG-ALL-6344 | Script gap | Product owner | The story adds PAYSLIP to the closed list LOV-NOTICE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E1007-APP | R-10982 | CG-ALL-6312 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E1032-APP | R-10995 | CG-ALL-6350 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E1034-APP | R-10998 | CG-ALL-6358 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E1034-APP | R-10999 | CG-ALL-6361 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-P6-E1046-APP | R-11000 | CG-ALL-6363 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-21888 | GAP-1545 | Register gap | Compliance | The debt buyer tape is required to be masked before the data room, and to carry the personal data the sale terms allow | The tape carries only the fields the sale terms and the approved mask list allow, and the mask list is a reference-data row owned by Compliance under DL26; the PRD states the rule and leaves the field list open. |
| RWB-ITG-E1011-ITG, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21922 | GAP-1651 | Register gap | Data steward and data product owner | The reconciliation and the data quality break are P1's, but FSD P9 specifies them as its own features | Read the reconciliation result and the break rows from P1's contract and hold the break view and the closure in P9 |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22078 | GAP-1595 | Register gap | Product owner | The document module is said to own the letter templates and their fields, while Architecture v5 gives templates and merge fields to rwb-comms | Hold the template record, its versions and the Legal approval in rwb-comms, hold the merge-field catalog in rwb-comms, and keep the template body file in rwb-document as a document with a reference on the template row; record DL28 as superseded by D-RCV-60 and close it with the product owner. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E1034-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22081 | GAP-1598 | Register gap | Product owner with the solution architect | Two of the module's business requirements describe the case record view and the case timeline, which the case service owns | Read both requirements as this service's contribution to the case record view: the notice and message block with its states, and the ordered notice and message history. The view, the timeline and the timer projection stay with rwb-case; the ledger entries stay with rwb-source-data. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22125 | GAP-2089 | Register gap | Product owner; service owners of P6 rwb-comms and P5 rwb-document | The Decision Log gives the letter templates to the document module, while Architecture v5 and the Ownership Map give them to rwb-comms | Follow Architecture v5 and the Ownership Map: templates and merge fields are P6 rwb_comms. Record the DL28 answer as a gap and ask the product owner to reaffirm or amend DL28 before the template story is Done. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-28455 | GAP-1548 | Register gap | Compliance | No retention period is set for an outbound item, a delivery record or the transmission evidence of a file | The PRD states the retention of P2 transmission records as open under DL26 with the section R9 placeholder, and requires only that a resend and its audit record outlive the retention period of the case they belong to. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-28596 | GAP-2098 | Register gap | Service owner of P6 rwb-comms; Compliance and Legal roles | The Compliance approval of customer wording has no artefact in the target template | Record the Compliance approval as a second approval of P7 with the template as its source, and keep approved_by_legal on the template row for the Legal approval that the endpoint records. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1052-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-28611 | GAP-2088 | Register gap | Business lead with Legal and Compliance; document owner | DL10 is listed open with one answer and is recorded as answered with another | Keep the source row word for word, record in section 6.1 that DL10 is answered on 5 November 2026 with answer A, and add no Thai wording in this document. |
| RWB-P6-E1034-APP | R-33452 | ASM-ALL-6361 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P6-AD017-APP | R-06356 | DOR-RWB-P6-AD017-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No epic design sign-off record in the sources. Section text for item 14 is not in this chunk, so no anchored edit. Needs the signed epic design record. |
| RWB-P6-AD017-APP | R-17497 | DOR-RWB-P6-AD017-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | FSD P6 Communications v3 (v5-v7) lists SCR-33 Template approval only as a screen row with no states. Empty/loading/error/no-access text cannot be sourced; section 10 not in chunk. |
| RWB-P6-AD017-APP | R-31234 | NEWAC-RWB-P6-AD017-APP-AC3 | 7, 16 | AC3: §8 BR2, BR5, BR6, BR9, BR11, BR12, BR15, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | The scenario body tests only self-approval. The other listed rules need a criterion or a boundary check. |
| RWB-P6-AD017-CON | R-06362 | DOR-RWB-P6-AD017-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in 04 User stories or the story text (searched 'epic design' and sign-off terms, 26 Nov 2026). No sign-off to cite; needs the epic design record. |
| RWB-P6-E1007-APP | R-06367 | DOR-RWB-P6-E1007-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources; the prior search found none. Recording a sign-off would invent it. Needs the epic design record. |
| RWB-P6-E1007-APP | R-21891 | GAP-1161 | 3 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Section 3 names four DP contracts (DP-03, DP-09, DP-10, DP-19); DP-07 is not named, so the count is not six. |
| RWB-P6-E1007-APP | R-29606 | ACR-RWB-P6-E1007-APP-AC5 | 7 | AC5 | Section 7 AC5 still cites TC-E1-007-11, which now tests AC9. Fix needed in section 7 outside this chunk. |
| RWB-P6-E1011-APP | R-06373 | DOR-RWB-P6-E1011-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | Searched the folder for epic design and sign-off records; none found in the story or sources. A sign-off reference would be invented, so the owner must supply the record. |
| RWB-P6-E1011-APP | R-06376 | DOR-RWB-P6-E1011-APP-22 | 14 | Definition of Ready item 22 Fake published: Fail | Searched the folder for a published contract fake library version; none found in the sources. A version number would be invented, so the owner must supply it. |
| RWB-P6-E1011-APP | R-21908 | GAP-1169 | 19 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | The new notice-barcode check code is not in the sources, so it would be invented. REC-09 stays with ASM-2116 in this story. RWB-E1-055 and the register are unchanged. |
| RWB-P6-E1011-APP | R-25956 | CG-ALL-6334 | 3 | Flyway file V1011_1__comms_quality.sql is not in the V0001..Vnnnn form | Next number is V0002: the only documented sequence value is V0001 (Service Template v1 §3.1 line 78; §6 line 164). The name is at story line 243, outside the supplied parts, so no exact old text was available to edit. |
| RWB-P6-E1019-APP | R-17527 | DOR-RWB-P6-E1019-APP-12 | 16 | Definition of Ready item 12 Test cases: Partial | Section 16 has 16 rows; TC-E1-019-13 is cited but its row is absent and its data is in Test Cases v8 only. |
| RWB-P6-E1032-APP | R-10994 | CG-ALL-6347 | 4 | Payload of rwb.comms.NoticeGenerated.v1 differs from Kafka Catalog v1 | Section 4 step 7 still carries the old payload, so the item is not resolved. |
| RWB-P6-E1032-APP | R-25966 | CG-ALL-6351 | 3.1 | Flyway file V1032_1__comms_letter_copy.sql is not in the V0001..Vnnnn form | Migration name is absent from the story (line 382 blank). Source search found no V1032_1 name and no next number for the service Flyway sequence. |
| RWB-P6-E1032-APP | R-28571 | GAP-2450 | 12 | The trigger of the ledger completeness check is not stated | Completeness-check trigger belongs in section 12 job notes of the ledger story, outside this chunk and not in this story. No edit made. |
| RWB-P6-E1032-APP | R-28572 | GAP-3145 | 15 | The partner portal screen that submits a file is not fixed | No source names the screen that carries the PRT-02 submission (FSD S9 gives no mapping). Section 15 is outside this chunk. Business analyst to confirm. |
| RWB-P6-E1032-APP | R-31255 | NEWAC-RWB-P6-E1032-APP-AC16 | 7, 16 | AC16: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are outside this chunk, so AC16 and its test row cannot be anchored. Proposed test is not specified in the source documents. |
| RWB-P6-E1034-APP | R-10996 | CG-ALL-6355 | 12.7; 13 | Name `uk_template_version` is not a field or entity in LDM v9 or Data Classification v5 | uk_template_version still appears in story text outside this chunk (see R-17544); the remaining occurrence must be removed from the story text. |
| RWB-P6-E1034-APP | R-17544 | DOR-RWB-P6-E1034-APP-7 | 11 | Definition of Ready item 7 Data: Partial | uk_template_version appears in story text outside this chunk (not in section 11 rows). Grep found it in the story file only outside sections 8 and 11. Needs that text to correct it. |
| RWB-P6-E1046-APP | R-25974 | CG-ALL-6364 | 3, 3.1 | Flyway file V1_046__template_catalog.sql is not in the V0001..Vnnnn form | The rwb_comms next Vnnnn is not in the sources (GAP-1067; ASM-2015). Section 3 has no migration name; the name is in section 11, outside this chunk. No edit. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10531 | RWB-P6-E1007-APP | CG-ALL-6292 | 12.1 | Publish GET /api/recovery/comms/v1/file-runs/{businessDate} in paths through the owner's contract story. |
| CDC-10532 | RWB-P6-E1007-APP | CG-ALL-6293 | 12.1 | Publish POST /api/recovery/comms/v1/file-runs/{businessDate}/retry in paths through the owner's contract story. |
| CDC-10575 | RWB-P6-E1011-APP | CG-ALL-6320 | 12.1 | Publish GET /quality-runs/{businessDate} in rwb-comms.yaml through RWB-P6-E1011-CON. |
| CDC-10576 | RWB-P6-E1011-APP | CG-ALL-6321 | 12.1 | Publish GET /quality-results in rwb-comms.yaml through RWB-P6-E1011-CON. |
| CDC-10577 | RWB-P6-E1011-APP | CG-ALL-6322 | 12.1 | Add a GET operation on /cases/{caseId}/notices in rwb-comms.yaml through RWB-P6-E1011-CON; the path currently has POST only. |
| CDC-10579 | RWB-P6-E1011-APP | CG-ALL-6324 | 12.2 | Remove the fixed deliveryStatus enum; the value set is data taken from LOV-DELIVERY in Reference Data v5 Lists. |
| CDC-10625 | RWB-P6-E1019-APP | CG-ALL-6338 | 12.1 | Publish GET /api/recovery/comms/v1/admin/notice-routing in rwb-comms.yaml through the owner's CON story, or remove the operation. |
| CDC-10628 | RWB-P6-E1019-APP | DOR-RWB-P6-E1019-APP-8 | 12.1 | Publish the notice-routing operation in rwb-comms.yaml (P1). The 404 message ID (P2) stays open under CG-ALL-6339. |
| CDC-20683 | RWB-P6-E1007-APP | R-01640 |  | GET /file-runs/{businessDate} is absent; publication belongs to the owner's contract story (CG-ALL-6292). |
| CDC-20689 | RWB-P6-E1007-APP | R-01641 |  | Retry operation publication belongs to the owner's contract story (RWB-P6-E1007-CON); operation not added here. |
| CDC-20690 | RWB-P6-E1007-APP | R-06372 |  | Operation bodies for file-runs GET and retry are not in the sources; rwb-source-data is a separate contract. Publish via owner contract story. |
| CDC-20691 | RWB-P6-E1011-APP | R-01645 |  | Quality run read is published via RWB-P6-E1011-CON; no source gives its schema, so not added in this yaml. |
| CDC-20692 | RWB-P6-E1011-APP | R-01646 |  | Quality result read is published via RWB-P6-E1011-CON; no source gives its schema, so not added in this yaml. |
| CDC-20693 | RWB-P6-E1011-APP | R-01647 |  | GET on /cases/{caseId}/notices is published via RWB-P6-E1011-CON; the yaml lacks the GET but no response schema is in this document. |
| CDC-20694 | RWB-P6-E1011-APP | R-06378 |  | Adding GET quality-runs, quality-results, notices and six detcheck paths needs operation contents not in sources; rwb-source-data is a separate contract. |
| CDC-20695 | RWB-P6-E1019-APP | R-01651 |  | notice-routing operation is published via owner CON story; story already states API ID None, so no edit here. |
| CDC-20696 | RWB-P6-E1019-APP | R-06384 |  | P1 notice-routing publication belongs to owner CON story (CG-ALL-6338); P2 404 message ID stays open under CG-ALL-6339. |
| CDC-20697 | RWB-P6-E1034-APP | R-21954 |  | Template operation routes and SCR-33 composite route are recorded in the P6 rwb-comms contract in the API registry, not in this yaml. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10614 | RWB-P6-E1011-APP | CG-ALL-6333 | 18 | Align the REQ-RDF-007 and REQ-RDF-008 test case lists with section 18 of this story in the next RTM version. |
| CDC-10638 | RWB-P6-E1019-APP | CG-ALL-6341 | 18 | In the next RTM version, align the test lists of REQ-CWC-006 and REQ-ACA-002 with section 18 of this story. |
| CDC-10670 | RWB-P6-E1032-APP | GAP-3144 | find it | Record the primary/secondary AC split so the fifteen legacy criteria are counted once, against RWB-P5-E1032-APP. |
| CDC-10672 | RWB-P6-E1032-APP | CG-ALL-6349 | 18 | Align the test lists traced to REQ-DCM-007 and REQ-DRI-004 with the section 18 rows of RWB-P6-E1032-APP in the next RTM version. |
| CDC-10687 | RWB-P6-E1034-APP | DOR-RWB-P6-E1034-APP-12 | 16 | Align the test list for RWB-P6-E1034-APP to section 18: TC-E1-034-01 to -11, TC-P6-E1034-APP-01 and TC-P6-E1034-APP-02. |
| CDC-10694 | RWB-P6-E1034-APP | CG-ALL-6357 | 18 | Align the REQ-OCC-002 test list between section 18 and the RTM at their next versions. |
| CDC-10699 | RWB-P6-E1046-APP | DOR-RWB-P6-E1046-APP-12 | 12, 16, 18 | Align the RTM v7 test case lists with section 18 of RWB-P6-E1046-APP. |
| CDC-10711 | RWB-P6-E1046-APP | CG-ALL-6362 | 18 | Align the REQ-OCC-001 and REQ-OCC-002 test lists with section 18 of RWB-P6-E1046-APP in the next RTM version. |

### RWB-P6-E1046-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10703 | RWB-P6-E1046-APP | GAP-0360 | 8 | Body placement rule moved to the CON document. |
| CDC-10704 | RWB-P6-E1046-APP | GAP-1063 | 12.1 | Record which legacy request maps to which operation: POST /admin/reference-loads to POST /admin/templates plus approve and withdraw; the legacy file-hash refusal is the upload idempotency rule; TC-E1-046-09 asserts on the mapped operation. |
| CDC-10705 | RWB-P6-E1046-APP | GAP-1065 | 3 | Fix one resolution rule for body_ref: a P5 rwb-document object or an object in the service's own container. |
| CDC-10706 | RWB-P6-E1046-APP | GAP-1066 | 3 | State the approved_by rule: keep LEG-0001 in fixtures and resolve it to the USER_REF uuid at approval time through the platform staff directory. |
| CDC-10707 | RWB-P6-E1046-APP | GAP-1067 | 3 | Baseline the Template, TemplatePage, TemplateApproval and TemplateWithdrawal fields in camelCase and add the code, language and on-date filter to API-P6-003. |
| CDC-10708 | RWB-P6-E1046-APP | GAP-2343 | 3 | Name the identifier property of the version answer; RWB-PLT-DB to fix per-service logins; document template_id stamp as a soft reference with a reconciliation check. |
| CDC-10709 | RWB-P6-E1046-APP | GAP-2345 | 3 | Record GET /admin/templates/current with code, language and onDate as an additive change within major version 1 before the wave-1 contract tests. |

### RWB-P2-E1007-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10535 | RWB-P6-E1007-APP | DOR-RWB-P6-E1007-APP-22 | 12.2 | Publish the fake library and record its version as published. |
| CDC-10551 | RWB-P6-E1007-APP | GAP-0334 | 11 | Define the deliverFile manifest schema, the claim-check handoff and the two Airflow window calls, and publish them in the activity contract jar and AsyncAPI before the first SIT run. |
| CDC-10554 | RWB-P6-E1007-APP | GAP-0648 | n/a | Fix deliverFile manifest and return, the three typed failures, the notice-fact read (notice ID, sent date, person key, document ID), the RFC 9457 problem body, JSON names and event subject. |
| CDC-10556 | RWB-P6-E1007-APP | GAP-0739 | n/a | Keep the seam: two outcomes and admin item from RWB-P2-E1007-CON; resume state from latest decision-record entry; task code and due date as rwb-case reference rows; lake extracts dropped under DP-17. |
| CDC-10562 | RWB-P6-E1007-APP | GAP-2229 |  | Confirm rwb.integration.FileFailed.v1 and FileDelivered.v1 payload elements, the resume-state carrier and the owner task code and due-date values at contract review; rename here if they differ, changing no value or rule. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10540 | RWB-P6-E1007-APP | CG-ALL-6290 | 16, 18 | Record interface_run as a retired legacy object (or add it to Fields) so the retirement assertion in the test case and section 18 resolves. |
| CDC-10541 | RWB-P6-E1007-APP | CG-ALL-6291 | 18 | Record interface_signoff as a retired legacy object (or add it to Fields) so the retirement reference in section 18 resolves. |
| CDC-10593 | RWB-P6-E1011-APP | DOR-RWB-P6-E1011-APP-7 | 11 | Add entities comms_quality_run, comms_quality_result and comms_quality_break (rwb_comms) or record them as this story's design; check against Data Classification v5. |
| CDC-10649 | RWB-P6-E1032-APP | CG-ALL-6345 | 4 | Record party_id as the notice link to the case party, or name the dictionary field for it. Nearest dictionary names are partner_id, party_ext and party_role; none matches exactly. |
| CDC-10655 | RWB-P6-E1032-APP | GAP-0742 |  | Add field IDs for rwb_case.case_document_link: case_id, document_id, checklist_state, extracted_field_count, linked_at, source_event_id; unique key (case_id, document_id). |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10544 | RWB-P6-E1007-APP | CG-ALL-6301 | 12.5 | Add activity selectFileRecords on task queue rwb-comms in namespace rwb-recovery. |
| CDC-10545 | RWB-P6-E1007-APP | CG-ALL-6302 | 12.5 | Add activity renderNoticeFile on task queue rwb-comms in namespace rwb-recovery. |
| CDC-10546 | RWB-P6-E1007-APP | CG-ALL-6303 | 12.5 | Add activity storeNoticeFile on task queue rwb-comms in namespace rwb-recovery, calling the claim-check object store. |
| CDC-10547 | RWB-P6-E1007-APP | CG-ALL-6304 | 12.5 | Add activity handoffFile on task queue rwb-integration in namespace rwb-recovery, calling deliverFile. |
| CDC-10548 | RWB-P6-E1007-APP | CG-ALL-6305 | 12.5 | Add activity recordFileRun on task queue rwb-comms in namespace rwb-recovery. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10561 | RWB-P6-E1007-APP | GAP-1544 |  | Inherit the programme NFR targets for every service and state the interface-level targets (file size, notices per file, daily volume, window length, extract size) as open under DL11, placeholder R9. |
| CDC-10570 | RWB-P6-E1007-APP | GAP-1540 | 16 | Hold the 5, 15 and 45 minute values as configuration in force; state FSD AC-EXC-P2-001-01 as the acceptance criterion; fix neither as a product rule |
| CDC-10571 | RWB-P6-E1007-APP | GAP-1542 | 16 | State that no inbound adapter, inbound folder, inbound run or sign-off exists in P6, and list FEAT-DRI-09, the inbound half of FEAT-RDF-21, FEAT-DRI-10, FileLoadAdapter, DQ-057, DQ-059, JOB-09, interface_run and interface_signoff as removed with later home ACE ingestion. |
| CDC-10572 | RWB-P6-E1007-APP | GAP-1546 |  | Record that the INT-17, INT-18 and INT-22 notification and logging paths are reused ACE capabilities with no P2 build and no FR, and that their behaviour is ACE's. |
| CDC-10573 | RWB-P6-E1007-APP | GAP-1547 |  | State that the partner and document channels keep their own contracts and transport, that P2 carries no requirement for them, and record the FSD transport sentence as superseded. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10580 | RWB-P6-E1011-APP | CG-ALL-6325 | 12.5 | Add a Workflows row for NoticeQualityWorkflow: rwb-comms, task queue rwb-comms, namespace rwb-recovery, one run per business date, from the kit template |
| CDC-10586 | RWB-P6-E1011-APP | CG-ALL-6326 | 12.5 | Add a loadTolerance activity row to the Activities sheet, calling rwb-case (P3), task queue rwb-comms. |
| CDC-10587 | RWB-P6-E1011-APP | CG-ALL-6327 | 12.5 | Add a readDeliveryFacts activity row to the Activities sheet, calling rwb-source-data (P1), task queue rwb-comms. |
| CDC-10588 | RWB-P6-E1011-APP | CG-ALL-6328 | 12.5 | Add a reconcileNotices activity row to the Activities sheet, reading rwb_comms only, task queue rwb-comms. |
| CDC-10589 | RWB-P6-E1011-APP | CG-ALL-6329 | 12.5 | Add a writeQualityFacts activity row to the Activities sheet, writing rwb_comms only, task queue rwb-comms. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10519 | RWB-P6-AD017-APP | GAP-1146 | 18 | Record that template and merge_field are P6 rwb-comms, that DL28 is superseded by Architecture v5 slide 41 under the precedence rule, the split of RWB-P6-E1034-APP and RWB-AD-017, and retire the Litigation rows of the legacy permission table. |
| CDC-10526 | RWB-P6-AD017-CON | GAP-1146 | find it | Record template and merge_field as P6 rwb-comms and DL28 superseded by Architecture v5 slide 41; split RWB-P6-E1034-APP (Epic 1 upload and approve core) and RWB-P6-AD017-APP (Epic 8 administration); confirm Documents right of T-A.1 for the five operations; retire Litigation rows of the legacy permission table. |
| CDC-10603 | RWB-P6-E1011-APP | GAP-1170 | 2 | Record that the reconciliation and data quality extracts and the INT-19 path are dropped; quality facts are served from GET /api/recovery/comms/v1/quality-results; rwb-reporting report read decision is recorded. |
| CDC-10610 | RWB-P6-E1011-APP | GAP-2237 | 12 | Record the uuid cross-reference form of TSD P3 v3 as the pre-re-base artefact; keep account_key and person_key as varchar business keys per FSD re-base under D-RCV-35. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10523 | RWB-P6-AD017-CON | CG-ALL-6285 | 4, 14 | Add a new message ID for 'A response body or a query fails schema validation' with text 'The request could not be read: {detail}.'; story then cites that ID |
| CDC-10525 | RWB-P6-AD017-CON | DOR-RWB-P6-AD017-CON-9 | 14 | MSG-P3-030 is defined there as an Information message for a missed scheduled-job run; the standard needs a schema-failure message ID, or must define MSG-P3-030 for schema failure. |
| CDC-10566 | RWB-P6-E1007-APP | CG-ALL-6308 | 14 | Add a message ID for a read or rerun naming a business date with no run, with its English text. The sources give no new ID, so none is invented here. |
| CDC-10629 | RWB-P6-E1019-APP | CG-ALL-6339 | 12.1 | Add a message ID for HTTP 404 (notice unknown or case outside scope) to section 4; business analyst to confirm. Story 503 now uses MSG-GEN-006. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10528 | RWB-P6-AD017-CON | CG-ALL-6286 | 16 | Add rows for TC-P6-AD017-CON-01 to TC-P6-AD017-CON-07 with Given, When and Then copied from the criterion each covers. |
| CDC-10590 | RWB-P6-E1011-APP | CG-ALL-6332 | 16 | Add rows for TC-E1-011-08 and TC-E1-011-09 with Given, When and Then copied from AC7, AC4 and BR8, BR9, BR12. |
| CDC-10592 | RWB-P6-E1011-APP | DOR-RWB-P6-E1011-APP-12 | 16 | Tab Story test cases: include TC-E1-011-08 and TC-E1-011-09; align section 18 test lists with RTM v7. |
| CDC-10686 | RWB-P6-E1034-APP | CG-ALL-6356 | 16 | Add a row for TC-P6-E1034-APP-01 with Given, When and Then copied from the criterion it covers. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10549 | RWB-P6-E1007-APP | GAP-0673 | 7 | Supersede the INT-03 line of FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 for legacy key RWB-E4-046, with date and decision; interface owner loads the ALS interface as one versioned interface_config row per environment. |
| CDC-10635 | RWB-P6-E1019-APP | GAP-1176 | 12 | State that queue, team code, role code and version are read from P3, and role, rights and scope from P4; publish or withdraw a membership operation on the P3 contract |
| CDC-10659 | RWB-P6-E1032-APP | GAP-1199 |  | State whether the hub creates an intake item from a generated document and which request fields it needs, including the source of the case ID. |
| CDC-10666 | RWB-P6-E1032-APP | GAP-3138 | find it | Publish the partner file channel: submission row, PartnerDocumentSubmitted fact, attach event consumed, item read used to copy match state. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10583 | RWB-P6-E1011-APP | CG-ALL-6317 | find it | Record comms_quality_run as a service-owned table of rwb_comms (P6), or add it under the dictionary name. |
| CDC-10584 | RWB-P6-E1011-APP | CG-ALL-6318 | find it | Record comms_quality_result as a service-owned table of rwb_comms (P6), or add it under the dictionary name. |
| CDC-10585 | RWB-P6-E1011-APP | CG-ALL-6319 | find it | Record comms_quality_break as a service-owned table of rwb_comms (P6), or add it under the dictionary name. |
| CDC-10651 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-7 | 11 | Confirm party_id as a field of the notice entity (DF-LEG-030) and classify it in Data Classification v5, or give the LDM v9 field name for DF-LEG-030. |

### RWB-P5-E1032-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10645 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-21 | Header | Publish the contract story the header names and confirm it covers the rwb-comms notice operations and the NoticeGenerated event. No RWB-P6-E1032-CON exists in the sources. |
| CDC-10646 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-22 | Header | Publish a fake library version for RWB-P5-E1032-CON and record its version against this story. |
| CDC-10653 | RWB-P6-E1032-APP | GAP-0992 | find it | Add RWB-P3-E1042-CON and RWB-P3-E1043-CON as C dependencies for the two rwb-case reads; declare their fakes; keep unnamed shape elements as placeholders until owner documents confirm them. |
| CDC-10664 | RWB-P6-E1032-APP | GAP-2447 |  | Define the DecisionRecorded attach fact keyed by caseId with decisionCode, caseId, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId and inputsRef; refuse a fact without documentId. |

### RWB-P6-E1046-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10695 | RWB-P6-E1046-APP | DOR-RWB-P6-E1046-APP-14 | n/a | Record the signed epic design sign-off for EP01 in the epic design record. |
| CDC-10696 | RWB-P6-E1046-APP | DOR-RWB-P6-E1046-APP-21 | n/a | Set the build status of contract story RWB-P6-E1046-CON to Done. |
| CDC-10697 | RWB-P6-E1046-APP | DOR-RWB-P6-E1046-APP-22 | n/a | Record the published version of the contract fake library for this story. |
| CDC-10698 | RWB-P6-E1046-APP | DOR-RWB-P6-E1046-APP-11 | n/a | Reconcile the personal-data classification of the P2 fields with the statement that this story carries no personal data. |

### RWB-P6-AD017-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10516 | RWB-P6-AD017-APP | DOR-RWB-P6-AD017-APP-21 | header | Build status Done with the contract published; currently Not started |
| CDC-10517 | RWB-P6-AD017-APP | DOR-RWB-P6-AD017-APP-22 | none | Record the published contract fake library version for RWB-P6-AD017-CON |
| CDC-10527 | RWB-P6-AD017-CON | GAP-1147 | find it | Add DP07 to the pattern set and rows H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON at the next plan revision. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10542 | RWB-P6-E1007-APP | CG-ALL-6298 | 12.4 | Add rwb-comms as a consumer of rwb.integration.FileDelivered.v1 on rwb.integration.events.v1, with its ACL, as the requesting service named in Architecture v5 slide 43. |
| CDC-10543 | RWB-P6-E1007-APP | CG-ALL-6299 | 12.4 | Add rwb-comms as a consumer of rwb.integration.FileFailed.v1 on rwb.integration.events.v1, with its ACL, as the requesting service named in Architecture v5 slide 43. |
| CDC-10652 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-8 | 12 | Record the payload of rwb.comms.NoticeGenerated.v1 as used by this story (IDs and facts only, keyed by case ID), or name the field difference so the story can conform. HTTP 404 and 409 cases added in section 12 of the story. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10578 | RWB-P6-E1011-APP | GET /api/recovery/source-data/v1/data-products/DP07/records is not published by rwb-source-data | 12.2 | Path is not published; the story cannot resolve it. |
| CDC-10620 | RWB-P6-E1011-APP | GAP-1172 | section 15 | Quality model names kept; run cadence marked Not specified in the source documents (GAP-1172) |
| CDC-10674 | RWB-P6-E1032-APP | GAP-0743 | 3 | Add a row for GET /api/recovery/source-data/v1/accounts/{id} owned by rwb-source-data; the story now uses this path. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10626 | RWB-P6-E1019-APP | DOR-RWB-P6-E1019-APP-14 | none | Confirm and record the signed epic design sign-off. |
| CDC-10644 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-14 | Header | Record the signed epic design sign-off for EP01 in the epic design record so the story can cite it. No sign-off exists in the source documents. |
| CDC-10683 | RWB-P6-E1034-APP | DOR-RWB-P6-E1034-APP-14 | header | Record the signed epic design sign-off for RWB-P6-E1034-APP. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20575 | RWB-P6-E1007-APP | R-09174 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '`debt_sale_account` by `account_key`; account data from `v_ace_acc |
| CDC-20576 | RWB-P6-E1007-APP | R-09173 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '`debt_sale_account` by `account_key`; account data from `v_ace_acc |
| CDC-20577 | RWB-P6-E1007-APP | R-21885 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '`debt_sale_account` by `account_key`; account data from `v_ace_acc |

### RWB-P6-E1034-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10518 | RWB-P6-AD017-APP | DOR-RWB-P6-AD017-APP-17 | header | Build to Done before this story starts |
| CDC-10693 | RWB-P6-E1034-APP | GAP-1147 | 13; 18 | Add DP07 to the pattern set of RWB-P6-E1034-APP and rows H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON. |

### OTHER:Recovery Workbench Notification and Correspondence Design (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10521 | RWB-P6-AD017-APP | GAP-2087 | none | Take the file name v2 as the family version so this document becomes version 3; add a Source version row with 1 and 28 October 2026; the change log carries both readings. |
| CDC-10529 | RWB-P6-AD017-CON | GAP-2087 | find it | Take v2 from the file name as the family version so the document becomes version 3; add a Source version row with 1 and 28 October 2026; the change log carries both readings. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10522 | RWB-P6-AD017-APP | GAP-1150 | 8 | Record that template approval and withdrawal publish no event; consumers read template state through the rwb-comms read operation; add a template event only when a consumer outside rwb-comms needs it; declare the absence in the contract with an absence test. |
| CDC-10530 | RWB-P6-AD017-CON | GAP-1150 | 8 | Record that template approval and withdrawal publish no event; consumers read template state via the rwb-comms read operation; allocate a template event only if a consumer outside rwb-comms needs it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; OTHER:rwb-source-data contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10536 | RWB-P6-E1007-APP | DOR-RWB-P6-E1007-APP-8 | 12.1 | Add paths GET /file-runs/{businessDate} and POST /file-runs/{businessDate}/retry to rwb-comms.yaml; publish GET /api/recovery/source-data/v1/customers/{customerId} in rwb-source-data. |
| CDC-10582 | RWB-P6-E1011-APP | DOR-RWB-P6-E1011-APP-8 | find it | Add GET /quality-runs/{businessDate}, GET /quality-results and GET /cases/{caseId}/notices to rwb-comms.yaml. Publish GET /api/recovery/source-data/v1/data-products/DP07/records in rwb-source-data. Add the six further paths named by detcheck. |

### OTHER:Functional Specification Document P2 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10538 | RWB-P6-E1007-APP | GAP-1535 | 4 | Restate A1.5 and AC-ALT-P2-001-03 so outbound facts are read through the rwb-source-data contract, one hop with 2 s budget; no rwb_integration grant on the recovery schema. |
| CDC-10539 | RWB-P6-E1007-APP | GAP-1539 | 4 | Build the INT-25 tape from the manifest raised by rwb-debtsale and read account facts via the rwb-source-data contract; P2 reads neither debt_sale_account nor v_ace_account. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10563 | RWB-P6-E1007-APP | GAP-3160 |  | Keep the file and outbox tables in P2; S6 rwb_debtsale owns debt_sale_account via a contract call or event from P2; recovery_case stays with P3 rwb_case. |
| CDC-10637 | RWB-P6-E1019-APP | GAP-3159 | find it | Load the role table in P4 rwb_access and read roles in P3 by contract; keep teams, queues, queue_member and reference rows in P3. |

### RWB-P1-E1011-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10600 | RWB-P6-E1011-APP | GAP-0496 | 2 | Keep REC-01, REC-02 and REC-05 over P1 tables only; remove REC-03 and REC-04 from P1; REC-03 to RWB-P3/RWB-S5, REC-04 to the payment slice, REC-05 case/asset/comms keys to their slices; prove in RWB-ITG-E1011-ITG. |
| CDC-10604 | RWB-P6-E1011-APP | GAP-1508 | 12.7 | Publish the REC-05 break list as part of the reconciliation result and its read operation, not in an unowned table; fix the store at the data-model review before system test. |

### RWB-P1-E1011-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10601 | RWB-P6-E1011-APP | GAP-0497 | 12.1 | Publish GET /admin/reconciliation/results and GET /admin/reconciliation/results/{resultId} with element lists, ReconciliationWorkflow ID recon-{businessDate}, activity reconciliation on rwb-source-data, and ReconciliationQuery interface. |
| CDC-10608 | RWB-P6-E1011-APP | GAP-2235 | 3 | Publish the freshness read and one product-coded records read per data product on /api/recovery/source-data/v1 with paging and element names; build against the fake until then. |

### RWB-P3-E1011-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10602 | RWB-P6-E1011-APP | GAP-0740 | 2 | Confirm REC-01 EXCL, REC-05 KEY and REC-05 REF codes and TRUSTED/HELD/NOT_RUN/FAILED states; publish four rwb-case operation paths; set Schedule cron; align account_id with account_key; add Platform administration right. |
| CDC-10606 | RWB-P6-E1011-APP | GAP-2233 | 12.7 | Create case_quality_run, case_quality_result and case_quality_break in schema rwb_case with legacy column names, unique key on rec_code, quality_check, business_date and product_group, and name the EXCL, PLAN and KEY checks. |

### OTHER:Recovery Workbench register workbook v3; OTHER:Reconciliations sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10615 | RWB-P6-E1011-APP | GAP-0271 | find it | Add a Per-service reconciliation sheet with one row per service (19 services) giving tables, check part, key, tolerance, cadence, break and result route, pattern and basis; unstated cells carry the Template and Rules R9 placeholder. |
| CDC-10616 | RWB-P6-E1011-APP | GAP-0272 | find it | Tolerance cell of the ten service rows (P2, P4, P5, P10, S1, S3, S4, S6, S8, S9) carries the Template and Rules R9 placeholder; the value is a Step D1 business decision. |

### OTHER:Build Notes v6 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10623 | RWB-P6-E1011-APP | GAP-3172 |  | State the wave 1 delivery of rwb-asset in the service epic and the wave plan; the rwb-asset service wave governs its later stories. |
| CDC-10682 | RWB-P6-E1032-APP | GAP-3174 | n/a | State the wave 1 delivery of rwb-partner in the service epic and the wave plan; the rwb-partner service wave governs its later stories. |

### RWB-P3-E1019-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10627 | RWB-P6-E1019-APP | DOR-RWB-P6-E1019-APP-22 | 3 | Record the published version of the contract fake library. |
| CDC-10634 | RWB-P6-E1019-APP | GAP-0682 | 5, 12 | Publish POST /admin/reference-loads/{loadId}/rollback and .../verify in a later rwb-case contract story; RWB-P3-E1019-APP keeps them out of its section 12 until then |

### OTHER:TSD P4 T3.1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10639 | RWB-P6-E1019-APP | GAP-1574 | find it | Add valid-from and valid-to to the matrix version or state that dating lives on the load; publish the role conflict list with its version label and row counts. |
| CDC-10640 | RWB-P6-E1019-APP | GAP-1567 | find it | Drop lov_value and partner_user from T3.1; name in the rwb-access contract the LOV versions and partner identity attributes it reads and its refresh rate. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10647 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-5 | 9 | Confirm the closed list LOV-NOTICE holds the value PAYSLIP the story adds, or the story stops using it. PAYSLIP is not in the story parts given. |
| CDC-10663 | RWB-P6-E1032-APP | GAP-2445 |  | Add DOCATT as a value of LOV-DECISION at the version in force; an unknown code is refused with MSG-P7-009. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10675 | RWB-P6-E1032-APP | GAP-0745 | - | Add the rwb-case parameter for the case-side switch, key Not specified in the source documents (GAP-0745), default on, owner RW-COE; off means the case side writes nothing from an event. |
| CDC-10678 | RWB-P6-E1032-APP | GAP-1200 | n/a | Add the business-owned notice values of the communications module as parameter rows with defaults, or record that the module has none and DP-06 applies as a path without a value. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20670 | RWB-P6-E1032-APP | R-28573 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21890', 'R-28478', 'R-28528', 'R-28558', 'R-28573', 'R-28662'] |
| CDC-20671 | RWB-P6-E1011-APP | R-28478 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21890', 'R-28478', 'R-28528', 'R-28558', 'R-28573', 'R-28662'] |

### OTHER:Recovery Workbench plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10520 | RWB-P6-AD017-APP | GAP-1147 | 18 | DP07 added to both pattern rows; reference-list validation recorded as Not specified |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10524 | RWB-P6-AD017-CON | DOR-RWB-P6-AD017-CON-10 |  | Define empty, loading, error and no-access states for SCR-33 (P3) |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10533 | RWB-P6-E1007-APP | CG-ALL-6294 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{customerId} in paths through the P1 provider's contract story. |

### RWB-P6-E1007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10534 | RWB-P6-E1007-APP | DOR-RWB-P6-E1007-APP-21 | header | CON dependency added to header with key not specified. |

### OTHER:Business Requirements Document Program v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10537 | RWB-P6-E1007-APP | GAP-1534 | 4 | Correct section 5.2 to Architecture v5: INT-19 served as an rwb-reporting delivery request via the rwb-integration delivery contract; INT-20 is continuous ingest in rwb-decision; no lake target. |

### RWB-PLT-TE006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10550 | RWB-P6-E1007-APP | GAP-1416 | 11 | Specify the library artifact and major version, the three interfaces, the DDL of outbox, processed_event and idempotency_key, CloudEvents attributes, the retry ladder and dead-letter topic. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10552 | RWB-P6-E1007-APP | GAP-0338 | n/a | Add the P2 Integration row cells for the read path to rwb-source-data and the FileFailed edge into rwb-case, or pass figures in the manifest. |

### OTHER:TSD P2 Integration v3 (T1.1; OTHER:T5.2; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10553 | RWB-P6-E1007-APP | GAP-0647 | n/a | Record that the direct-view wording is superseded by Architecture v5 and ADR-010; ACE facts read via rwb-source-data (one hop, 2 s); INT-25 rows from the deliverFile manifest; retire INT-19/20 and JOB-13/15 lake statements. |

### OTHER:Operations story (Not specified in the source documents (GAP-0650)) and bank Airflow owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10555 | RWB-P6-E1007-APP | GAP-0650 | n/a | Set chart values, replica counts, KEDA threshold, lag and alert thresholds and build ID format as environment values; confirm both windows as calls; keep the §R9 placeholder until named. |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10557 | RWB-P6-E1007-APP | GAP-1162 | header | Add a read returning the postal addressee only, by party_id, with a 2 s budget and a fake; keep the value out of rwb_comms, events and logs. Story contract list updated. |

### OTHER:rwb-document contract and WIN interface owner (rwb-integration interface row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10558 | RWB-P6-E1007-APP | GAP-1164 | header | Fix the WIN record layout and file pattern as the rwb-integration interface row; store built file behind a claim-check reference in the document hub; pass only the reference in the manifest. |

### OTHER:TSD P6 Communications v2 appendix T-A and T6.1; OTHER:platform edge SCR-44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10559 | RWB-P6-E1007-APP | GAP-1166 | n/a | Add a read and a rerun operation on the service base; enforce the right at gateway-bff; confirm with edge owner whether a local guard is needed. |

### OTHER:FSD P2 Integration v3 A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10560 | RWB-P6-E1007-APP | GAP-1536 | n/a | Remove JOB-10, JOB-13 and JOB-15 as P2 schedules; the Ownership Map is applied: JOB-10 P6, JOB-13 P7, JOB-15 P9, with rwb-integration registering no Temporal Schedule. |

### OTHER:Egress infrastructure values (SCB IT infrastructure, key-rotation runbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10564 | RWB-P6-E1007-APP | GAP-0649 |  | Provision both endpoints per environment with one receiver and one key each; fix hosts, ports, accounts, folders, receiver ranges, PGP key IDs, staging names, size, timeout and rotation period with the MFT, network and security teams. |

### OTHER:Owner CON stories of rwb-source-data, rwb-integration and rwb-reporting (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10565 | RWB-P6-E1007-APP | GAP-1396 |  | Fix the Airflow product, tenancy, service principal, timeout and retry values, DailyCaseRun wait mechanism and the three file-window operations at scheduling design review; publish before the first SIT chain run. |

### RWB-P2-E1007-CON; RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10567 | RWB-P6-E1007-APP | GAP-0981 | 16 | Register one OUTBOUND interface row for the access-review file with interface ID, file pattern, data product, owner role and alert role; publish extract layout and recipient in RWB-P4-AD008-APP |

### OTHER:Interface mapping workbook (ACE-new rows; OTHER:Mapping column M) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10568 | RWB-P6-E1007-APP | GAP-0213 | 16 | Keep the cell text word for word in v5; confirm v4 interface numbers at the next interface review |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Events sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10569 | RWB-P6-E1007-APP | GAP-1538 | 16 | Add rows for FileDelivered and FileFailed (producer rwb-integration, topic rwb.integration.events.v1, keyed by case ID, no EV ID) in the next version |

### OTHER:Legacy dependency trace sheet (realignment trace) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10574 | RWB-P6-E1007-APP | GAP-3233 |  | Keep the five Not carried rows, including RWB-E1-056 to RWB-E1-007, visible as Not carried; add an X row only if the run books or the harness really wait for the named story. |

### RWB-P6-E1011-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10581 | RWB-P6-E1011-APP | DOR-RWB-P6-E1011-APP-21 Contract published: Fail | header | CON dependency names a story not in the set. |

### OTHER:Screen Specifications v1 (SCR-44; OTHER:SCR-45) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10591 | RWB-P6-E1011-APP | DOR-RWB-P6-E1011-APP-10 Screens and states: Partial | 10 | States in section 10 replaced with Not specified marking, matching section 15. |

### OTHER:Recovery Workbench reconciliation workbook v3 (sheet Reconciliations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10594 | RWB-P6-E1011-APP | GAP-0268 | 8 | Add an owner from the Ownership Map to every reconciliation row; rwb-source-data keeps the ACE side and the JOB-04 run. |

### OTHER:Recovery Workbench reconciliation workbook v3 (sheets Reconciliations and Quality measures) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10595 | RWB-P6-E1011-APP | GAP-0269 | 8 | Append Owner and Per-service reconciliation to Reconciliations and Owner service to Quality measures, from the Ownership Map. |

### OTHER:Recovery Workbench BRD section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10596 | RWB-P6-E1011-APP | GAP-1456 | header | State the wave rule: business-epic wave kept; stories of rwb-payment, rwb-asset and rwb-deviation built in wave 1 where the service starts in wave 2; delivery lead confirms wave per story at build sequencing. |

### OTHER:v3 Reconciliations sheet; OTHER:REC-08 row (B12/C12) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10597 | RWB-P6-E1011-APP | GAP-0270 | 9 | REC-08 compares the local decision record of each of the 19 services on rwb.decision-record.v1 with the central decision_log_entry of P7, on count and last hash, nightly, with the 02:00 hash-chain check (JOB-14). |

### OTHER:reconciliation workbook v3 (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10598 | RWB-P6-E1011-APP | GAP-0273 |  | Add a REC numbering block mapping each check to its v4 number and to the RWB-E1-011 story-set number; keep source IDs and do not renumber any ID. |

### OTHER:_work/msr/plan/split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10599 | RWB-P6-E1011-APP | GAP-0275 |  | At Step D1 add service slices for rwb-treatment (S2) owning REC-03 and rwb-payment (P8) owning REC-04; record the per-service split. No story is created here. |

### RWB-P3-E1011-APP; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10605 | RWB-P6-E1011-APP | GAP-2232 | 2 | Rule that the rwb-case slice owns the case-side facts (REC-01 exclusions, REC-03 plan link, REC-05 referential check over rwb-case tables), writes no reconciliation_result row and owns no legacy AC. |

### RWB-P3-E1011-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10607 | RWB-P6-E1011-APP | GAP-2234 | 12.1 | Publish the four case-side quality run operations with Platform administration R, Reporting R and Platform administration U, the 400/401/403/404/409/503 problem set and Idempotency-Key on rerun. |

### OTHER:rwb-case contract and rwb-source-data publish gate (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10609 | RWB-P6-E1011-APP | GAP-2236 | 4 | Expose GET /reconciliation/status on rwb-case (RELEASED, HELD or NOT_RUN with unexplained exclusion count per product group) and have the rwb-source-data case-list gate read it before release. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10611 | RWB-P6-E1011-APP | GAP-1946 | 3 | Keep H and C at None; record the nine platform and rwb-case CONs as wave-0 prerequisites and fakes; read the ACE side through the DP06 Collateral and assets product; serve quality facts from the GET /api/recovery/asset/v1 endpoints. |

### OTHER:TSD P6 v2 module specification and RWB-E1-052 legacy field list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10612 | RWB-P6-E1011-APP | GAP-1084 | 12 | Settle DF-LEG-030 with the data steward: keep person_key as the notice business key, give the party reference its own field ID, and correct the DF-LEG-030 row. |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10613 | RWB-P6-E1011-APP | GAP-1097 | 3 | Add the pod records, freshness and batch-status elements with business date, feed version, batch status and stale marker; until then the two data-product paths are the consumed operations. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Services row S1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10617 | RWB-P6-E1011-APP | GAP-0274 | find it | S1 row keeps rwb-valuation as owner, states the capability from Architecture v5 and carries the Template and Rules R9 placeholder until a table is listed. |

### OTHER:Recovery Workbench register workbook v3; OTHER:Quality measures sheet (B7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10618 | RWB-P6-E1011-APP | GAP-0276 | find it | Restate Timeliness: complete when rwb-source-data reads it and publishes AceDataReady; other services measure the freshness contract; owner is P1 rwb-source-data. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10619 | RWB-P6-E1011-APP | GAP-0337 | find it | Add the three JOB-04 outbound reads to the rwb-source-data row of the connection matrix and publish the exclusion resource on the rwb-case contract with its path, fields and 2 s budget. |

### OTHER:TSD P6 Communications v2 (T6.1 RBAC matrix); OTHER:gateway-bff route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10621 | RWB-P6-E1011-APP | GAP-1173 | 15 | Add a Platform administration area to the rwb-comms RBAC matrix and the gateway-bff route, with the two quality reads at right R. |

### RWB-P3-E1011-APP; RWB-P3-E1011-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10622 | RWB-P6-E1011-APP | GAP-2238 The report, the Schedule cadence, the alert groups and the feature flag of the case-side run have no source | 8 | BR15 reduced to Not specified; invented schedule, flag and DP-17 removed. |

### OTHER:BRD v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10624 | RWB-P6-E1011-APP | GAP-1457 |  | Renumber section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### OTHER:Screen specification of SCR-42 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10630 | RWB-P6-E1019-APP | DOR-RWB-P6-E1019-APP-10 | none | Add the empty, loading, error and no-access states of SCR-42. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10631 | RWB-P6-E1019-APP | GAP-0679 | 11 | Confirm the column list of the legacy ROLE and TEAM split with P4: roles, permissions, scope, masking and delegation in rwb-access; TEAM kept as reference data and role_code kept as a code in rwb-case |

### OTHER:rwb-access OpenAPI document (GET /me/session) and rwb-comms OpenAPI document (notice response) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10632 | RWB-P6-E1019-APP | GAP-0344 | 12 | Publish the team scope field of GET /me/session and the queue and team code fields of the notice response, or record them in the Service Contract Catalog before wave 1 exit |

### OTHER:Queues reference-load template (xlsx) under the Reference data owner (Shared operations); RWB-P3-E1019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10633 | RWB-P6-E1019-APP | GAP-0681 | 4, 12 | Publish the Queues template as an xlsx workbook with one header row per sheet (QUEUE and QUEUE_MEMBER), one column per queue and queue_member field, and one check per required column |

### OTHER:TSD P6 Communications v2 Appendix T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10636 | RWB-P6-E1019-APP | GAP-1179 | 12.1 | Add the routing read to the P6 API file with an allocated API identifier at its next revision. |

### OTHER:rwb-access (access data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10641 | RWB-P6-E1019-APP | GAP-0683 | 3, 10 | Record that RW-TEAMMGR holds Reference data A for TEAM, QUEUE and QUEUE_MEMBER as rwb-access grant data; keep 403 MSG-P4-002 as the refusal. |

### OTHER:Service template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10642 | RWB-P6-E1019-APP | GAP-1177 | 3 | State the reader caching rule: a reader may cache for the life of one call only; a longer-lived cache is an owner contract with a version and an invalidation event. |

### OTHER:Control register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10643 | RWB-P6-E1019-APP | GAP-1180 | 8 | Register CTL-08 with its text, owner and evidence, and cite the register row from the stories that apply it (this story cites it in BR3 and BR4). |

### RWB-S9-E1032-APP; RWB-S9-E1057-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10648 | RWB-P6-E1032-APP | GAP-1843 | Header | Cut the wave 1 slices to contract-only: publish partner identity and partner document path; move panel, allocation and fees to wave 4. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10650 | RWB-P6-E1032-APP | DOR-RWB-P6-E1032-APP-12 | 12, 12.7, 16, 18 | Write the Given, When and Then of TC-E1-032-18 to TC-E1-032-29 in Test Cases v8, tab Story test cases; align the RWB-E1-032 test list in RTM v7 to section 18 of the story. Story side added contract, table boundary and BR test rows. |

### RWB-P5-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10654 | RWB-P6-E1032-APP | GAP-0356 | find it | Start the intake from DocumentStored with KEDA workers; keep /review-items and /resolve with the item version; keep the three parameters as document_hub_parameter rows read as data. This story keeps no JOB-12 or attach step (BR4). |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10656 | RWB-P6-E1032-APP | GAP-0991 |  | Confirm or add rwb.document.DocumentAttached.v1 on rwb.document.events.v1; publish /intake-items/{intakeItemId}/resolve as the attach operation with Documents C and the 201 Document answer. |

### OTHER:Environment files (SCB IT infrastructure) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10657 | RWB-P6-E1032-APP | GAP-0993 |  | Record replica count, request and limit set, KEDA ceiling, document_text growth and index budget, rwb-quarantine clearing age, hold capacity and scan rate per environment from SIT measurement. |

### OTHER:TSD P5 and TSD P6 Communications v2 contracts; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:notice parameter register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10658 | RWB-P6-E1032-APP | GAP-1197 |  | Publish the generated-document request and answer with the intake item created, the document type and source for a notice letter copy, notice parameter names, event payload fields and the notice screen ID. |

### OTHER:Test case register (test lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10660 | RWB-P6-E1032-APP | GAP-1201 |  | Record that attach proof for TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP, that the P6 copy proves the service side, and that the legacy access case is the notice-read refusal. |

### RWB-ITG-E1032-ITG; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10661 | RWB-P6-E1032-APP | GAP-1202 | 1 | Set the consumer of rwb.comms.NoticeGenerated.v1 to rwb-decision only, state the hub handoff as a call from rwb-comms, and align the integration suite. |

### OTHER:TSD P7 v2 T3.1 decision_log_entry field list and migration V1032_1 in rwb_decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10662 | RWB-P6-E1032-APP | GAP-2444 |  | Map document reference and intake item and match method into actions, classifier version into model_version, confidence and candidates into recommendation, refusal message id into outcome, and final_call ATTACHED. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10665 | RWB-P6-E1032-APP | GAP-3137 | find it | Confirm the secondary partner slice in the Change Register and publish the S9 frame for RWB-S9-E1032-APP; story stands on Template R4 naming and cites this row. |

### RWB-S9-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10667 | RWB-P6-E1032-APP | GAP-3141 | find it | Publish the two partner submission operations, intake creation, PartnerDocumentSubmitted payload, and 404/409 bodies in RFC 9457 shape before Done. |

### OTHER:S9 reference data set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10668 | RWB-P6-E1032-APP | GAP-3142 | find it | Publish the intake bound parameter row, acceptance decision code with version, and LOV-DOC-TYPE; keep values out of code. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10669 | RWB-P6-E1032-APP | GAP-3143 | find it | Add partner_intake to the LDM and rwb_partner schema with its field IDs before the wave 1 entry check. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10671 | RWB-P6-E1032-APP | GAP-1198 | find it | Add the seven platform contracts and two P3 contracts to the RWB-P6-E1032-APP dependency rows, or record them in the platform release train. |

### OTHER:TSD P3 v3 (rwb-case reference tables) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10673 | RWB-P6-E1032-APP | GAP-0746 | - | Hold the review task code, element type and task status values as reference data in the rwb-case reference tables, loaded with RWB-P3-E1043-CON before the review queue story starts. |

### OTHER:Platform DB story (one login per service) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10676 | RWB-P6-E1032-APP | GAP-0748 | - | Name the login for rwb-case and for rwb-document, one per service; this story keeps the role names until the logins are agreed. |

### OTHER:RWB-E1-032 legacy story section 12 (rwb-document intake job JOB-12) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10677 | RWB-P6-E1032-APP | GAP-0994 | 12 | Register Schedule for business-hours window, overlap skip, catch-up of one run; thresholds as environment values; lag alert placeholder until the Error and Message Standard names it. |

### OTHER:FSD P6 Communications v3 and TSD P6 Communications v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10679 | RWB-P6-E1032-APP | GAP-1203 | n/a | Approve both documents, or record that wave 1 builds on the reviewed versions and that any change in approved text is a change request. |

### OTHER:FSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10680 | RWB-P6-E1032-APP | GAP-2446 | n/a | State that a held item or refused attach writes no DOCATT entry because no document was stored; the hold remains a status on the intake item. |

### OTHER:TSD P7 v2 (T3, appendix T-A) and FSD P7 v3 (exception flow) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10681 | RWB-P6-E1032-APP | GAP-2449 | 12 | Name the login as 'the rwb-decision login (DP-02)'; keep placeholders for parameter names and MSG-P7-009 and MSG-GEN-006 texts; read parameters via the rwb-case parameters contract. |

### RWB-P3-E1043-CON; RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10684 | RWB-P6-E1034-APP | DOR-RWB-P6-E1034-APP-21 | header | Bring RWB-P3-E1043-CON and RWB-P1-E1015-CON to Done with their contracts published. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10685 | RWB-P6-E1034-APP | DOR-RWB-P6-E1034-APP-22 | header | Record a published fake library version for the contracts consumed by RWB-P6-E1034-APP. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10688 | RWB-P6-E1034-APP | DOR-RWB-P6-E1034-APP-18 | header | Record DL08, DL10, DL11, DL27, DL28 and DL31 as settled by the directive of 26 November 2026, and give DL31 an assumption entry. |

### OTHER:P6 rwb-comms contract in the API registry (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10689 | RWB-P6-E1034-APP | GAP-0357 | header | Name the base path and route of the five template operations under /api/recovery/comms/v1/admin/templates and the composite route of SCR-33 reached through gateway-bff, with the stamp source and hold point. Story header rows now state the sources. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10690 | RWB-P6-E1034-APP | GAP-0942 | 10 | Add a Documents column to T6.1 with RW-CASEOWN CRU, RW-RESTRUCT CRU, RW-TEAMMGR R and RW-LEGAL CRUA, confirm with the matrix owner, and publish in the PM-2026.12 pack before it is in force. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10691 | RWB-P6-E1034-APP | GAP-1146 | header | Scope split stated in header |

### OTHER:rwb-case contract, task operation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10692 | RWB-P6-E1034-APP | GAP-1149 | 8 | Name the litigation officer task operation, task code, target queue and fields in the rwb-case contract, with MSG-P6-003 as content; record code and queue in the service values file. |

### OTHER:Recovery Workbench open decisions register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10700 | RWB-P6-E1046-APP | DOR-RWB-P6-E1046-APP-18 | n/a | Record DL10 assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863 and DL28 assumptions ASM-1861, ASM-1925, ASM-2093, ASM-2727 as confirmed. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P5 (API-P5-016; OTHER:T3.1); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:rwb-document story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10701 | RWB-P6-E1046-APP | GAP-1023 | 12.1 | Use /cases/{caseId}/generated-documents on /api/recovery/document/v1 (ASM-101); add template_code varchar(30) and template_version integer beside template_id and treatment_id; partial unique index on (treatment_id, template_id) where state is DRAFT and is_active (ASM-103); read templates only through RWB-P6-E1046-CON (ASM-102). |

### OTHER:Split plan and rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10702 | RWB-P6-E1046-APP | GAP-1064 | header | Data-dictionary contract dependency row now placeholder. |

### OTHER:FSD P7 v3 and TSD P7 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10710 | RWB-P6-E1046-APP | GAP-2453 | 3 | Record the P7 copy as one template_use row per accepted answer with no catalog copy; treat the three platform H rows as wave-0 prerequisites. |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10712 | RWB-P6-E1046-APP | GAP-2344 | Header | Add the rwb-case reference-data contract and the platform contract stories to this slice's dependency rows; RWB-P5-E2026-CON to name GenerateRequest and RegenerateRequest fields, the regenerate reason field, the refused-document error body, index ix_document_template and the Flyway step name. |

### OTHER:Split plan (Work Package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10713 | RWB-P6-E1046-APP | GAP-2346 | 7 | Record one owning story per legacy criterion and mark RWB-P5-E1046-APP as test-case-bearing and criterion-free. |

### 10 Policy, controls and compliance/Recovery Workbench Controls Catalog v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20571 | RWB-P6-E1019-APP | R-28520 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-28520'] |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20759 | RWB-P6-E1032-APP | R-28560 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0063 | Wave conflict S5 / EP01 | Tech lead | Resolved (directive) |
| GAP-0065 | Wave conflict S9 / EP01 | Tech lead | Resolved (directive) |
| GAP-0213 | Five rows still cite 'number in Interface Specifications v3' after v4 of that document was issued | Integration architecture team | Resolved (directive) |
| GAP-0268 | The nine reconciliations name one Workbench side, but that side sits in seven service schemas | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0269 | No reconciliation and no quality measure carries an owner | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0270 | REC-08 compares a decision-log copy that the target retires | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0271 | No per-service reconciliation rule, cadence or result route | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0272 | Ten services have no tolerance and no legacy reconciliation row | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0273 | REC-05 and REC-09 are numbered the other way round from RWB-E1-011 | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0274 | S1 rwb-valuation owns no table in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0275 | REC-03 and REC-04 have no per-service owner in the RWB-E1-011 slice set | TechX | Resolved (directive) |
| GAP-0276 | The Timeliness measure reads a Workbench read of the ACE batch that no service but P1 makes | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0334 | deliverFile manifest payload, claim-check handoff and the file-window trigger contract are not defined | Solution architect | Resolved (directive) |
| GAP-0336 | Owner of REC-03 and REC-04 and the reporting delivery path of the two extracts are not named for the microservice target | Solution architect | Resolved (directive) |
| GAP-0337 | The connection matrix does not show the rwb-source-data outbound reads and the exclusion operation of the case contract is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0338 | Connection matrix gives rwb-integration only the document REST call and the outside file edge, while the file build reads source data and the failure reaches rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0344 | Field names of the P4 session team scope and the P6 notice queue code are not fixed by any source | Service owner of rwb-access and service owner of rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0356 | Intake trigger, attach operation and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0360 | Reference-load owner, field-ID check and template body storage move in the target | Solution architect | Resolved (directive) |
| GAP-0495 | The two lake extracts and the Power BI data set have no successor in the target, while the legacy story still writes them and reads the report | Solution architect | Resolved (directive) |
| GAP-0496 | TSD P1 keeps REC-03, REC-04 and a cross-estate REC-05 inside P1 while the Change Register gives rwb-case, rwb-asset and rwb-comms their own slices of the same legacy key | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0497 | The reconciliation result path, the result and break-row shape, the ReconciliationQuery interface and the workflow and activity names are not specified in any source | Tech lead | Resolved (directive) |
| GAP-0647 | rwb-integration outbound-file capability: ACE read path, INT-25 source table, data-lake retirement, JOB-10 and JOB-11 split, operation naming, alert event names, deliverFile manifest and job catalog rows not settled | Solution architect | Resolved (directive) |
| GAP-0648 | Outbound-file contract: deliverFile manifest and return, notice-fact read of rwb-comms, JSON field names and problem body, event schema subject and compatibility level not fixed by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0649 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | SCB IT infrastructure | Resolved (directive) |
| GAP-0650 | Outbound-file deployment: chart values, replica counts, KEDA threshold, lag and alert thresholds, dashboard names, build ID format, Airflow trigger contract of the two file windows and the message identifiers of the lag and window alerts not specified in any source | DevOps team | Resolved (directive) |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0678 | The per-service database login name of rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0679 | The column-level split of the legacy role and permission tables between rwb-case and rwb-access is not defined | Solution architect | Resolved (directive) |
| GAP-0680 | The column-level definition of queue measures and of the remaining list-of-values columns is not specified | Technical lead, rwb-case | Resolved (directive) |
| GAP-0681 | The queues reference-load template format is not specified | Reference data owner (Shared operations) | Resolved (directive) |
| GAP-0682 | The rollback and verify operations of reference loads sit outside the rwb-case operation set given for this legacy key | Solution architect | Resolved (directive) |
| GAP-0683 | The approver authority for a queues load is assumed, not confirmed | Access owner, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0739 | The case side of an outbound file outcome leaves the delivery-event element names, the route state to resume, the task code and due date, the fate of the legacy in-process interfaces and the two lake extracts unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0740 | The rwb-case slice of RWB-E1-011 leaves the check codes, the four operation paths, the call type to rwb-source-data, the case key columns, the Schedule cron, the access right, the login and every report value that only the data lake held unspecified | Solution architect, with the P1 rwb-source-data owner, the P3 rwb-case owner and the data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0742 | No case-side document link table or field IDs in the sources | RW-DATASTEW | Resolved (directive) |
| GAP-0743 | No named rwb-source-data operation for the ACE account number | RW-COE | Resolved (directive) |
| GAP-0744 | Cadence and time of the daily reconcile Schedule not specified | RW-COE | Resolved (directive) |
| GAP-0745 | The rwb-case feature switch key is not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0747 | Decision code and final call for the case document link are not specified | RW-COE | Resolved (directive) |
| GAP-0748 | Per-service login names for rwb-case and rwb-document are not specified | RW-SECADM | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0857 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Business analyst, P4 | Resolved (directive) |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0985 | Role version: roster, row counts, role-file layout, matrix effective date, conflict list and MSG-P4-006 text not specified | Security administrator (RW-SECADM), with the reference data administrator (RW-REFADM) | Resolved (directive) |
| GAP-0991 | The attach operation, its right and the attach event name differ between the legacy story, the TSD and the Arch v5 event catalogue | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0993 | The compute, storage, hold-container and scanning capacity values of the intake-match path are not specified | SCB IT infrastructure | Resolved (directive) |
| GAP-0994 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | DevOps team | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1063 | The legacy template and catalog load path is replaced by the TSD admin template operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1064 | The data-dictionary read has no contract dependency in the plan | Solution architect | Resolved (directive) |
| GAP-1065 | No source says where the template body object lives | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1066 | The approver identity type of a template version is not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1067 | The request and answer field names of the five admin operations are not in T-A.2 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1068 | The service-side guard on the admin operations is not specified and DP-08 is not declared | Solution architect | Resolved (directive) |
| GAP-1084 | Field DF-LEG-030 is party_id in the module specification and person_key in the legacy story | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1097 | The pod and batch-status contract elements are not named in RWB-P1-E1066-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1137 | Legacy /templates paths disagree with the TSD /admin/templates paths | Tech lead | Resolved (directive) |
| GAP-1138 | Legacy 'set current' has no operation in the target contract | Tech lead | Resolved (directive) |
| GAP-1139 | Allowed body file types and the size limit are marked assumed and fixed by no source | Tech lead | Resolved (directive) |
| GAP-1140 | Template body container: own Blob store or a P5 rwb-document object | Solution architect | Resolved (directive) |
| GAP-1146 | Template ownership is a conflict between DL28 and the catalogue, and the split of the surface between RWB-E1-034 and RWB-AD-017 is not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1147 | The reference lists the template screen needs have no contract row and no DP-07 in this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1148 | The withdrawal reason, the field that holds it and the decision code of an approval or a withdrawal are not stated | Business analyst, P6 | Resolved (directive) |
| GAP-1149 | The task target of a withdrawn template and the resumption of held generation are not specified | Business analyst, P6 | Resolved (directive) |
| GAP-1150 | No template event exists in the service event catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1162 | The addressee and contact value reach the INT-14 file through a contract that is not in the story's contract list, and no source names the operation or its elements | Solution architect, with the P1 and P6 owners | Resolved (directive) |
| GAP-1163 | DP-17 removes the INT-19 reporting extract and the INT-20 decision-log copy, so part of legacy RWB-E1-007 has no target and no replacement in this service | Business analyst and solution architect | Resolved (directive) |
| GAP-1164 | The INT-14 record layout, the file pattern and the claim-check store of the built file are named by no source, and the document contract is not in the story's contract list | Solution architect, with the P2 and P5 owners | Resolved (directive) |
| GAP-1165 | The retired inbound load leaves TC-E1-007-05, TC-E1-007-06 and the file checks DQ-057 and DQ-059 without a target in this service | Business analyst and QA lead | Resolved (directive) |
| GAP-1166 | No source defines a run record, a run operation or the right on the interface monitor for rwb-comms | Solution architect and the gateway-bff owner | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1170 | RWB-P6-E1011-APP: the data lake is removed, so the reconciliation and data quality extracts and the report built on them have no target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1171 | RWB-P6-E1011-APP: no event is published because DP-09 is not in the pattern set, and no operation of rwb-reporting or rwb-source-data accepts the quality facts | Solution architect | Resolved (directive) |
| GAP-1172 | RWB-P6-E1011-APP: the quality tables, the check codes, the run cadence and the two quality read operations are not named in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1173 | RWB-P6-E1011-APP: the right of the quality reads is Platform administration R in the legacy story, and the rwb-comms RBAC matrix has no Platform administration column | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1175 | DP-08 is claimed while the authorise contract and the guard library are in no dependency list | Solution architect | Resolved (directive) |
| GAP-1176 | The split of the legacy role, queue and membership data between rwb-case and rwb-access is not stated, and the membership read has no published operation | Solution architect | Resolved (directive) |
| GAP-1177 | No source decides whether a reader keeps a local cache of the role and queue data | Solution architect | Resolved (directive) |
| GAP-1178 | The legacy reference-load path has no rwb-comms target, so the legacy access case has no endpoint in this service | Test lead | Resolved (directive) |
| GAP-1179 | The P6 API specification has no operation that exposes the approver role and the approver queue of a notice | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1180 | Control CTL-08 is cited by the legacy story and the case story but is absent from the rules register | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1197 | The request and answer shape of the letter-copy handoff, the document type and source the hub assigns, the notice parameters, the P1 recipient field IDs, the payload field names of the event and the notice screen identifier are all unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1199 | No source describes the letter copy becoming an intake item at the document hub, and FSD P6 keeps a generated document as a stored document on the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1200 | The P6 module declares no notice parameter, so DP-06 has no named value to read | Business analyst | Resolved (directive) |
| GAP-1201 | The legacy access case and the legacy attach cases have no subject in rwb-comms, so the carried test cases prove the notice read instead | Test lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1202 | The event catalogue names rwb-decision as the only consumer of NoticeGenerated, while the document hub is expected to turn the copy into an intake item | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1203 | The base documents of the story are in review, not approved | Business analyst | Resolved (directive) |
| GAP-1396 | Airflow product, tenancy, DAG names, identity method, timeout and retry values, the DailyCaseRun wait contract and the file-window operation are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1508 | The per-account reconciliation break rows have no store after the quality-exception table leaves the schema | Data architect | Resolved (directive) |
| GAP-1514 | The job monitor and data-quality screens are first-in here and owned by reporting in the architecture | Solution architect | Resolved (directive) |
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
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2087 | The source reads version 1 in its metadata table and v2 in its file name | Document owner of the notification and correspondence design | Resolved (directive) |
| GAP-2095 | The partner instruction and the internal alert are rows of the design but are not rwb-comms notices in the target | Service owners of P6 rwb-comms, S9 rwb-partner and P3 rwb-case | Resolved (directive) |
| GAP-2229 | Element names of the two delivery outcomes, the carrier of the route state to resume and the values of the owner task are not in the sources | TechX and the rwb-integration contract owner | Resolved (directive) |
| GAP-2230 | The legacy P3 interfaces and the case-action path have no operation in the target case contract | TechX | Resolved (directive) |
| GAP-2232 | The split of RWB-E1-011 across the services and the case-side scope are not ruled by any source | Solution architect | Resolved (directive) |
| GAP-2233 | The case-side result row has no table and no check codes in the target | Solution architect | Resolved (directive) |
| GAP-2234 | No source names the operations, rights or response shapes of the case-side quality run | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2235 | The data-product reads that replace the ACE views have no published path, element shape or product code in this story's sources | Solution architect | Resolved (directive) |
| GAP-2236 | The hand-off of the case-side hold to the case-list publish gate is not specified | Solution architect | Resolved (directive) |
| GAP-2237 | TSD P3 v3 declares the case links as uuid cross-references while the FSD re-base and the legacy data table use the ACE business keys | Solution architect | Resolved (directive) |
| GAP-2238 | The report, the Schedule cadence, the alert groups and the feature flag of the case-side run have no source | Solution architect | Resolved (directive) |
| GAP-2343 | The catalog version answer read by rwb-document, its field names and the rwb-document login name are not specified, and the legacy document-to-template key becomes a soft cross-service reference | Solution architect, with the P5 TechX squad and the P6 rwb-comms squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2344 | The dependency rows of this slice name one contract only, and the request field names, the reason field, the index name and the migration step name are not specified | Solution architect, with the P5 TechX squad | Resolved (directive) |
| GAP-2345 | The rwb-comms catalog baseline declares no operation that answers the current Approved version for a template code, language and date | Tech lead of rwb-comms, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2346 | This slice owns no legacy acceptance criterion while the Work Package lists all nine legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2444 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Solution architect, P7 | Resolved (directive) |
| GAP-2445 | The decision code list in force does not enumerate DOCATT in any source readable here | Reference data administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2446 | Whether an item held for a person leaves a decision record is not stated | Business analyst, P7 | Resolved (directive) |
| GAP-2447 | The DecisionRecorded payload of an attach has no defined field set | Solution architect, integration | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2449 | Login name, parameter names and message texts are not written in any source readable here | Tech lead, P7 | Resolved (directive) |
| GAP-2450 | The trigger of the ledger completeness check is not stated | Solution architect, P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3137 | The partner slice of RWB-E1-032 and its target service frame are not stated in any source | Solution architect | Resolved (directive) |
| GAP-3138 | The partner-origin channel of an intake item and its attach state are a boundary no source states | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3139 | Wave conflict: EP01 puts this story in wave 1 while rwb-partner is wave 4 in Arch v5 | Tech lead | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3141 | The two partner submission operations, the intake creation path and the PartnerDocumentSubmitted event are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3142 | The intake bound, the decision code and version, and the two lists in force are not named | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3143 | No data model carries a partner-side submission row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3144 | No source states how the legacy criteria split between the document-hub and partner slices | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3145 | The partner portal screen that submits a file is not fixed | Business analyst | Resolved (directive) |
| GAP-3159 | The role table is loaded by P3 in the story and owned by P4 in the Ownership Map | P4 access owner | Resolved (directive) |
| GAP-3160 | The P2 outbound adapter writes a table owned by rwb-debtsale | Integration lead | Resolved (directive) |
| GAP-3169 | The reconciliation story writes 'the case exceptions' without naming a table | P1 data owner | Resolved (directive) |
| GAP-3172 | Service S5 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3174 | Service S9 takes Epic 1 stories in wave 1 although its Arch v5 wave is 4 | Delivery lead | Resolved (directive) |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3240 | One module per item in version 3 becomes several services per item in the split | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P6-E1011-APP | unknown story key | 24 | RWB-P6-E1011-CON is not a story of the set: \| Contract dependencies \| RWB-P6-E1011-CON (rwb-comms contract story; carries the operations of 12.1; builds against contract version v1, th |
| RWB-P6-E1032-APP | skipped AC ID | 121 | missing: AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16 |
