# RWB-SVC-P5 rwb-document (Document) - review pack, part 3 of 6 (RWB-P5-E1041-APP to RWB-P5-E1050-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 158 |
| Cross-document (pending in another document) | 154 |
| Not applied (value not in the sources) | 29 |
| Open business decisions | 23 |
| Register gaps linked | 51 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P5-E1041-APP | 24 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1041 APP Retention classes and virus scan on intake v2.md |
| RWB-P5-E1041-CON | 18 | 19 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1041 CON Retention classes and virus scan on intake - contract v2.md |
| RWB-P5-E1046-APP | 14 | 15 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1046 APP Template and merge field catalog as data v2.md |
| RWB-P5-E1049-APP | 25 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1049 APP OCR pipeline on the Workbench document hub v2.md |
| RWB-P5-E1049-CON | 15 | 17 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1049 CON OCR pipeline on the Workbench document hub - contract v2.md |
| RWB-P5-E1049-INF | 14 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1049 INF OCR pipeline on the Workbench document hub - infrastructure v2.md |
| RWB-P5-E1049-OPS | 13 | 17 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1049 OPS OCR pipeline on the Workbench document hub - deployment v2.md |
| RWB-P5-E1050-APP | 13 | 17 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1050 APP Document classification v2.md |
| RWB-P5-E1050-CON | 22 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1050 CON Document classification - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1049-ITG, RWB-ITG-E1050-ITG, RWB-P3-E1050-APP, RWB-P5-E1049-APP, RWB-P5-E1049-CON, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1053-CON, RWB-P6-E1049-APP | R-09185 | GAP-1586 | Register gap | Solution architect with the AI product owner | The OCR, classification and extraction services are named as external pieces but no source names them or their owner | The PRD keeps the pipeline behaviour in P5 and states the OCR, classification and extraction engines as an external contract reached as an AgentRunCompleted event or a Temporal child run, with the provider, the contract and the version scheme carried as OQ-P5-06. |
| RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1041-APP, RWB-P5-E1041-CON | R-09222 | GAP-1581 | Register gap | Solution architect with Legal counsel | Legal hold REQ-DCM-016 has no FSD feature, the hold API belongs to P3, and the delivery story sits in Epic 8 | The PRD states the hold as a P5 product behaviour driven by the hold P3 records (FR-P5-025), slices it to wave 4 with RWB-AD-021, and keeps the retention class and the scan in wave 1. The BRD and the story set need one position on the wave. |
| RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1041-APP, RWB-P5-E1041-CON | R-09223 | GAP-1584 | Register gap | Compliance and PDPA officer | Retention periods are not set while the acceptance criteria assert named retention classes | The PRD requires a class on every document and a period from the retention table, treats the class names in the criteria as examples of a reference-table version, and carries the periods as OQ-P5-10. The retention rule field list and the approved periods are needed before wave 1 acceptance. |
| RWB-P5-E1041-APP | R-10865 | CG-ALL-5880 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1041-CON | R-10868 | CG-ALL-5900 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1046-APP | R-10870 | CG-ALL-5906 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1049-APP | R-10873 | CG-ALL-5914 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1049-CON | R-10876 | CG-ALL-5928 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1050-APP | R-10883 | CG-ALL-5943 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1050-CON | R-10886 | CG-ALL-5956 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P7-E1017-APP | R-21967 | GAP-2070 | Register gap | Service owners P7 rwb-decision, P1 rwb-source-data and P4 rwb-access with Compliance | Where the retention period of the ledgers and the access log is held, and which job enforces it | Keep every period as written and mark the owner open: P7 enforces the ledger period, P1 the interaction ledger and P4 the access log, each as a row of its own retention data, until Compliance states where the periods are held. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22078 | GAP-1595 | Register gap | Product owner | The document module is said to own the letter templates and their fields, while Architecture v5 gives templates and merge fields to rwb-comms | Hold the template record, its versions and the Legal approval in rwb-comms, hold the merge-field catalog in rwb-comms, and keep the template body file in rwb-document as a document with a reference on the template row; record DL28 as superseded by D-RCV-60 and close it with the product owner. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22125 | GAP-2089 | Register gap | Product owner; service owners of P6 rwb-comms and P5 rwb-document | The Decision Log gives the letter templates to the document module, while Architecture v5 and the Ownership Map give them to rwb-comms | Follow Architecture v5 and the Ownership Map: templates and merge fields are P6 rwb_comms. Record the DL28 answer as a gap and ask the product owner to reaffirm or amend DL28 before the template story is Done. |
| RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P5-E1041-APP | R-23065 | GAP-1025 | Register gap | Solution architect, with the Compliance and PDPA officer role owner and the P3 and P5 service owners | The retention-class and legal-hold read surface of rwb-document has no operation, no shape and no document-level hold in any source, and the case and reference contracts it consumes are not in the story's contract list | Read recovery_case.legal_hold through the P3 case contract on every read and project it onto the document as legalHold and legalHoldRef, with no hold table and no hold write in rwb_document; keep the plan's C list as None, build against the three P3 fakes and record the missing rows for step D1; fix the four read paths, their queries and their answers in the RWB-P5-AD021-CON baseline and treat them as not specified in the sources; keep every period, age basis and end action as a class-load data row of RWB-P5-E1041-APP and let a missing class fail as 422 rather than default; read the retention_action rows and the DOCRET reference the run wrote and start, stop or re-run nothing, since JOB-17 belongs to RWB-P5-E1017-APP. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-28596 | GAP-2098 | Register gap | Service owner of P6 rwb-comms; Compliance and Legal roles | The Compliance approval of customer wording has no artefact in the target template | Record the Compliance approval as a second approval of P7 with the template as its source, and keep approved_by_legal on the template row for the Legal approval that the endpoint records. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P4-E1022-APP, RWB-P5-E1025-APP, RWB-P5-E1025-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP | R-35406 | ASM-1988 | Register assumption |  | The approver of a document-type load is the legal counsel who owns the type table, holding Reference data A, as the legacy story assumes under DL01; the loader holds Reference data C and may not approve | Business lead with Legal confirms the role that approves the type list |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P5-E1041-APP | R-25774 | CG-ALL-5881 | 3, 3.1 | Flyway file V1041_1__retention_and_scan.sql is not in the V0001..Vnnnn form | Next number of the rwb-document Flyway sequence is taken at merge (D-RCV-28); no number in the sources. Migration name sits in line 425, outside this chunk, so not edited. |
| RWB-P5-E1041-CON | R-17215 | DOR-RWB-P5-E1041-CON-11 | 12.3 | Definition of Ready item 11 Guardrails: Partial | The §12.3 text is not in this chunk, so no P2 field can be named or dropped. Data Classification v5 Fields is xlsx and unreadable. Needs the §12.3 text. |
| RWB-P5-E1041-CON | R-22036 | GAP-1034 | 12 | The scan operation path of the RWB-P5-E1041-CON malware-scan contract is not specified | No source names the scan path, verb or shapes. Placeholder row ScanOperation added in section 12 with GAP-1034. Stays open for the RWB-P5-E1041-CON owner. |
| RWB-P5-E1046-APP | R-06180 | DOR-RWB-P5-E1046-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No version for RWB-P6-E1046-CON found in 04 User stories, Build Notes Epic 1 v7 or the story file. /v1 is a path, not a contract version. Placeholder kept. |
| RWB-P5-E1046-APP | R-17222 | DOR-RWB-P5-E1046-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 is not in the supplied chunk, so SCR-33 empty, loading, error and no-access states cannot be copied as old text. Re-issue with section 9. |
| RWB-P5-E1046-APP | R-17223 | DOR-RWB-P5-E1046-APP-11 | 8 | Definition of Ready item 11 Guardrails: Partial | Section 8 is not in the supplied chunk, so the personal-data classing of P2 fields cannot be edited. Re-issue with section 8. |
| RWB-P5-E1046-APP | R-17225 | DOR-RWB-P5-E1046-APP-15 | header | Definition of Ready item 15 INVEST: Partial | Two weeks is not in the source; sizing left to the squad. |
| RWB-P5-E1046-APP | R-22121 | GAP-1023 | not in chunk | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Fix text is cut off after point 3 (points 4-6 missing) and the sections they touch are not in the chunk. Re-issue with the full fix text. |
| RWB-P5-E1046-APP | R-31142 | NEWAC-RWB-P5-E1046-APP-AC12 | 7, 16 | AC12: error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | No source names 401 or 404 for these operations; only 403 appears (AC10). Adding AC12 would invent status codes. Needs a source ruling. |
| RWB-P5-E1049-APP | R-25789 | CG-ALL-5915 | 3 | Flyway file V1049_1__document_intake_ocr.sql is not in the V0001..Vnnnn form | Next Flyway number of rwb_document is not in the sources (Service Template v1 §3.1, §4; sibling stories use V<story>_1). Migration name is at story line 391, not in supplied text, so no anchored edit. |
| RWB-P5-E1049-CON | R-06188 | DOR-RWB-P5-E1049-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. The sign-off value cannot be entered; it must come from the epic design record. |
| RWB-P5-E1049-CON | R-17243 | DOR-RWB-P5-E1049-CON-11 |  | Definition of Ready item 11 Guardrails: Partial | The item names no P2 fields and the field list is not in the sources or this chunk. Needs the field list from the detcheck finding. |
| RWB-P5-E1049-CON | R-17245 | DOR-RWB-P5-E1049-CON-18 | 9 | Definition of Ready item 18 Open decisions: Partial | DL10 and ASM-2250, ASM-2357, ASM-2377, ASM-2863 sit in section 9, which is not in this chunk. Resubmit with section 9. |
| RWB-P5-E1049-CON | R-22141 | GAP-0362 | 3-13 | OCR trigger, worker count and parameter home change in the target | Ruling: keep the four OCR parameters in document_hub_parameter, read as data; OCR_WORKERS is the concurrency cap. Sections 3-13 are not in this chunk. Resubmit. |
| RWB-P5-E1049-CON | R-22142 | GAP-0997 | 3, 12 | OCR engine product, endpoint, engine version, capacity, intake request property names and the business-hours window are not named in the sources | Engine product, endpoint, engine version and page limit are in no source. Needs the provider owner and the wave 1 entry check. |
| RWB-P5-E1049-CON | R-22144 | GAP-1000 |  | OCR engine capacity, admission queue depth, per-page text size and container quota are not named in the sources | Capacity ceiling, admission depth, bytes per page and container quota are in no source. Set at the capacity review with the OCR provider owner. |
| RWB-P5-E1049-CON | R-22145 | GAP-1204 | 13 | The values the rescan notice needs are not named in any source | Eight rescan notice values (template code, notice type, Notice properties, request and result shape, recipient reference and more) are in no source. Each needs its own publishing row. |
| RWB-P5-E1049-CON | R-28599 | GAP-1208 | 8 | The document token of the rescan message has no named reference form | No named reference form for the document token exists in any source; the story keeps MSG-P5-018 text unchanged. |
| RWB-P5-E1049-OPS | R-17259 | DOR-RWB-P5-E1049-OPS-18 | 14 | Definition of Ready item 18 Open decisions: Partial | The DL10 and ASM link belongs in section 14, whose text is not in this chunk, so there is no anchor to edit. Needs section 14 text. |
| RWB-P5-E1049-OPS | R-17260 | DOR-RWB-P5-E1049-OPS-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | New criteria go in section 7 and test rows in section 16, neither of which is in this chunk, so there is no anchor. Needs sections 7 and 16 text. |
| RWB-P5-E1049-OPS | R-28599 | GAP-1208 | 14 | The document token of the rescan message has no named reference form | The MSG-P5-018 text is in section 14, which is not in this chunk, so there is no old text to match. Re-run with section 14. |
| RWB-P5-E1049-OPS | R-31150 | NEWAC-RWB-P5-E1049-OPS-AC10 | 7, 16 | AC10: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC10 needs section 7 and the section 16 test row, neither in this chunk. The proposed test is not in the sources. Re-run with sections 7 and 16. |
| RWB-P5-E1050-APP | R-06205 | DOR-RWB-P5-E1050-APP-22 | Header | Definition of Ready item 22 Fake published: Fail | No fake library version for RWB-P5-E1050-CON in the sources (searched contract files and E1050 stories). Header placeholder kept, no value entered. |
| RWB-P5-E1050-APP | R-06206 | DOR-RWB-P5-E1050-APP-23 | Header | Definition of Ready item 23 Contract version fixed: Fail | No fixed contract version in the sources (searched E1050 stories and Service Template v1). Only the /v1 path is given; placeholder kept, no value entered. |
| RWB-P5-E1050-APP | R-25802 | CG-ALL-5944 | 3, 3.1 | Flyway file V1_5_050__intake_classification.sql is not in the V0001..Vnnnn form | Service Template v1 section 3.1 confirms the V0001 to Vnnnn sequence, but the next number for rwb-document is not in the sources. Needs the service owner's number. |
| RWB-P5-E1050-APP | R-25803 | CG-ALL-5945 | 3, 3.1 | Flyway file V1050_1__intake_classification.sql is not in the V0001..Vnnnn form | Service Template v1 section 3.1 confirms the V0001 to Vnnnn sequence, but the next number for rwb-document is not in the sources. Needs the service owner's number. |
| RWB-P5-E1050-APP | R-31153 | NEWAC-RWB-P5-E1050-APP-AC13 | 7, 16 | AC13: a status change the model does not allow is refused (no criterion covers a disallowed transition) | No allowed or disallowed status transition is named in the sources (searched). A refusal AC would need an invented transition, so AC13 is not added. |
| RWB-P5-E1050-CON | R-06209 | DOR-RWB-P5-E1050-CON-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design exists in the story or the source documents (per prior search). A sign-off would be invented; the epic design record is needed. |
| RWB-P5-E1050-CON | R-31154 | NEWAC-RWB-P5-E1050-CON-AC11 | 7 and 16 | AC11: §8 BR1, BR2, BR3, BR4, BR10, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so there is no safe anchor for the new AC11 or its test row. Re-issue with those parts; the proposed test is Not specified in the source documents (NEWAC-RWB-P5-E1050-CON-AC11). |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09807 | RWB-P5-E1041-APP | CG-ALL-5876 | 2 | Remove the fixed enum on action so values of LOV-RETENTION-ACTION load as data, as the story and Reference Data v5 Lists state. |
| CDC-09822 | RWB-P5-E1041-CON | CG-ALL-5886 | 12.1 | Add path /api/recovery/document/v1/retention-rules with operation GET and the shape in the section 12.1 row. |
| CDC-09823 | RWB-P5-E1041-CON | CG-ALL-5887 | 12.1 | Add path /api/recovery/document/v1/retention-rules/{classCode} with operation GET and the shape in the section 12.1 row. |
| CDC-09824 | RWB-P5-E1041-CON | CG-ALL-5888 | 12.1 | Add path /api/recovery/document/v1/admin/retention-loads with operation POST and the shape in the section 12.1 row. |
| CDC-09825 | RWB-P5-E1041-CON | CG-ALL-5889 | 12.1 | Add path /api/recovery/document/v1/admin/retention-loads/{loadId}/approve with operation POST and the shape in the section 12.1 row. |
| CDC-09826 | RWB-P5-E1041-CON | CG-ALL-5890 | 12.1 | Add path /api/recovery/document/v1/admin/retention-loads/{loadId} with operation GET and the shape in the section 12.1 row. |
| CDC-09827 | RWB-P5-E1041-CON | CG-ALL-5891 | 12.1 | Add path /api/recovery/document/v1/scans with operation POST and the shape in the section 12.1 row. |
| CDC-09828 | RWB-P5-E1041-CON | CG-ALL-5892 | 12.1 | Add path /api/recovery/document/v1/documents/{documentId}/scan-status with operation GET and the shape in the section 12.1 row. |
| CDC-09829 | RWB-P5-E1041-CON | CG-ALL-5893 | 12.1 | Add path /api/recovery/document/v1/intake-items/{intakeItemId}/scan-status with operation GET and the shape in the section 12.1 row. |
| CDC-09832 | RWB-P5-E1041-CON | DOR-RWB-P5-E1041-CON-8 |  | Declare GET /retention-rules, GET /retention-rules/{classCode}, POST /admin/retention-loads, POST /admin/retention-loads/{loadId}/approve and the further paths in the detcheck, relative to base /api/recovery/document/v1. |
| CDC-09873 | RWB-P5-E1049-CON | CG-ALL-5919 | 12.1 | Publish POST /api/recovery/document/v1/intake-items in the yaml through this CON story. |
| CDC-09874 | RWB-P5-E1049-CON | CG-ALL-5920 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/text in the yaml through this CON story. |
| CDC-09875 | RWB-P5-E1049-CON | CG-ALL-5921 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/ocr-status in the yaml through this CON story. |
| CDC-09941 | RWB-P5-E1050-CON | CG-ALL-5948 | 12.1 | Publish POST /api/recovery/document/v1/intake-items/{intakeItemId}/classify with the shapes and statuses of sections 12.1 and 14. |
| CDC-09942 | RWB-P5-E1050-CON | CG-ALL-5949 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/classification with the 200 ClassificationResult answer of section 12.1. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09814 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-12 | 12, 16, 18 | Align its test-case lists for RWB-P5-E1041-APP with section 16 (TC-E1-041-01 to TC-E1-041-18) and section 18. |
| CDC-09820 | RWB-P5-E1041-APP | CG-ALL-5879 | 18 | Align REQ-DCM-010 and REQ-DCM-016 test lists with §18 of RWB-P5-E1041-APP, or record the difference; QA owns the change. |
| CDC-09839 | RWB-P5-E1041-CON | CG-ALL-5899 | 18 | Set REQ-DCM-010 to TC-E1-041-01, -02, -06, -09, -10, -13, -14, -15 and REQ-DCM-016 to TC-E1-041-05, matching section 18 of this story. |
| CDC-09845 | RWB-P5-E1046-APP | DOR-RWB-P5-E1046-APP-12 | 12.7, 16, 18 | Align section 18 test lists of RWB-P5-E1046-APP to RTM v7, including TC-E1-046-11 under REQ-OCC-002 |
| CDC-09853 | RWB-P5-E1046-APP | CG-ALL-5905 | 18 | REQ-OCC-002 row gains TC-E1-046-11 |
| CDC-09863 | RWB-P5-E1049-APP | DOR-RWB-P5-E1049-APP-12 | 16 | Confirm §18 test lists of REQ-DCM-006, REQ-DCM-009 and REQ-DCM-010 in RWB-P5-E1049-APP against TC-E1-049-01 to TC-E1-049-14; story §18 not changed here. Added TC-E1-049-11 (contract) and TC-E1-049-12 (boundary). |
| CDC-09869 | RWB-P5-E1049-APP | CG-ALL-5913 | 18 | Align the test lists traced to REQ-DCM-006, REQ-DCM-009 and the third requirement with section 18 in the next RTM version; section 18 unchanged. |
| CDC-09888 | RWB-P5-E1049-CON | CG-ALL-5927 | 18 | Reconcile the test lists of the three differing requirements with section 18 in the next RTM version; section 18 stays as written until then. |
| CDC-09930 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-12 | 12, 12.7, 16, 18 | Align the test case list for REQ-DCM-005 to TC-E1-050-01 to TC-E1-050-13 |
| CDC-09939 | RWB-P5-E1050-APP | CG-ALL-5942 | 18 | In RTM v8, align the REQ-DCM-005 test list with section 18 of RWB-P5-E1050-APP (TC-E1-050-01 to TC-E1-050-13); the story list is unchanged. |
| CDC-09956 | RWB-P5-E1050-CON | CG-ALL-5955 | 18 | Align the REQ-DCM-005 row to RWB-P5-E1050-CON section 18: TC-E1-050-02, -03, -04, -05, -09, -10, -12, -13; RTM IDs of other stories stay. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09808 | RWB-P5-E1041-APP | CG-ALL-5877 | 12.3 | Add event type rwb.document.RetentionApplied.v1 (topic rwb.document.events.v1, key caseId) to the Events sheet. |
| CDC-09830 | RWB-P5-E1041-CON | CG-ALL-5895 | 12.3 | Add event rwb.document.RetentionApplied.v1 on topic rwb.document.events.v1, owner P5 rwb-document, with the schema declared in section 12.3. |
| CDC-09838 | RWB-P5-E1041-CON | GAP-0996 | 12.9 | Record rwb.document.RetentionApplied.v1 on rwb.document.events.v1 as the third event of rwb-document, beside DocumentStored.v1 and DocumentFieldsExtracted.v1. |
| CDC-09856 | RWB-P5-E1049-APP | CG-ALL-5911 | 12.3 | Add rwb.document.OcrCompleted.v1 on rwb.document.events.v1, producer P5 rwb-document, to the Events sheet |
| CDC-09860 | RWB-P5-E1049-APP | DOR-RWB-P5-E1049-APP-8 | 12.3 | Add rwb.document.OcrCompleted.v1 to Events and add rwb-document as consumer of rwb.document.DocumentStored.v1 (EV-16), with ACL |
| CDC-09862 | RWB-P5-E1049-APP | CG-ALL-5912 | 12.4 | Add rwb-document as a consumer of rwb.document.DocumentStored.v1 (EV-16) and grant its ACL |
| CDC-09880 | RWB-P5-E1049-CON | CG-ALL-5924 | 12.4 | Add rwb-document as a consumer of rwb.document.DocumentStored.v1 (EV-16) in the Events row and in its ACL |
| CDC-09924 | RWB-P5-E1050-APP | CG-ALL-5941 | 12.3 | Add rwb.document.DocumentClassified.v1 to the Events sheet, or use a catalogued event type |
| CDC-09927 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-8 | 12.3 | Add rwb.document.DocumentClassified.v1 to the Events sheet, or use a catalogued event type |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09809 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-14 | header | Record the signed epic design sign-off for RWB-P5-E1041-APP in the epic design record. |
| CDC-09831 | RWB-P5-E1041-CON | DOR-RWB-P5-E1041-CON-14 |  | Confirm and record the signed epic design sign-off for this story's epic; no sign-off is recorded in the story or the source documents. |
| CDC-09841 | RWB-P5-E1046-APP | DOR-RWB-P5-E1046-APP-14 | header | Record the signed epic design sign-off and confirm it against this story's placeholder row |
| CDC-09857 | RWB-P5-E1049-APP | DOR-RWB-P5-E1049-APP-14 | header | Record the signed epic design sign-off for RWB-P5-E1049-APP |
| CDC-09890 | RWB-P5-E1049-INF | DOR-RWB-P5-E1049-INF-14 | find it | Record the signed epic design sign-off for EP01 and RWB-SVC-P5 in the epic design record; no signed record exists in the sources. |
| CDC-09907 | RWB-P5-E1049-OPS | DOR-RWB-P5-E1049-OPS-14 |  | Record the signed epic design sign-off for RWB-P5-E1049-OPS (DOR-RWB-P5-E1049-OPS-14) |
| CDC-09925 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-14 | header | Record the signed epic design sign-off for the epic |

### RWB-P6-E1046-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09842 | RWB-P5-E1046-APP | DOR-RWB-P5-E1046-APP-21 | header | Publish the contract and record it as published; the story's contract dependency is RWB-P6-E1046-CON, no RWB-P5 key is invented |
| CDC-09843 | RWB-P5-E1046-APP | DOR-RWB-P5-E1046-APP-22 | header | Record the contract fake library version as published |
| CDC-09846 | RWB-P5-E1046-APP | GAP-1063 | 12 | Map legacy POST /admin/reference-loads to upload on POST /admin/templates plus approve and withdraw operations; keep the SHA-256 refusal as the upload idempotency rule; record the mapping. |
| CDC-09847 | RWB-P5-E1046-APP | GAP-1065 | 11 | Treat body_ref as an opaque claim-check reference; fix one resolution rule (P5 rwb-document contract or the service's own container) before RWB-P6-E1052 is built. |
| CDC-09848 | RWB-P5-E1046-APP | GAP-1066 | 11 | Keep LEG-0001 in fixtures; resolve it to the USER_REF uuid at approval time via the staff directory; state the rule in the API file. |
| CDC-09849 | RWB-P5-E1046-APP | GAP-1067 | 12 | Baseline the four resources from TSD P6 T3.1 field names in camelCase; add the current-version filter (code, language, on-date) to API-P6-003. |
| CDC-09851 | RWB-P5-E1046-APP | GAP-2345 | 12 | Add a resolved current-version read, for example GET /admin/templates/current with code, language and onDate, as an additive change within major version 1. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09815 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-6 | 10 | Add role SY-DOCUMENT (the rwb-document service identity) as a role row. |
| CDC-09833 | RWB-P5-E1041-CON | DOR-RWB-P5-E1041-CON-1 |  | Record tech lead as a role name, or replace the section 1 role with a role code from the document. |
| CDC-09881 | RWB-P5-E1049-CON | DOR-RWB-P5-E1049-CON-1 | 1 | Add 'tech lead' as a role code or role name |
| CDC-09894 | RWB-P5-E1049-INF | DOR-RWB-P5-E1049-INF-1 | 1 | Register infrastructure engineer as a role code and role name in Users Roles and Permissions v5. |
| CDC-09931 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-6 | 10 | Add role SY-DOCUMENT (rwb-document service identity) to the role list |
| CDC-09947 | RWB-P5-E1050-CON | DOR-RWB-P5-E1050-CON-1 | 1 | Add a role code or role name for 'tech lead' so that the role in section 1 of RWB-P5-E1050-CON is found in the document. |

### RWB-P5-E1049-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09858 | RWB-P5-E1049-APP | DOR-RWB-P5-E1049-APP-21 | header | Bring the contract story to Done so the contract is published |
| CDC-09859 | RWB-P5-E1049-APP | DOR-RWB-P5-E1049-APP-22 | header | Publish the contract fake library version and record it against this story |
| CDC-09891 | RWB-P5-E1049-INF | DOR-RWB-P5-E1049-INF-21 | find it | Move the contract story from Not started to Done and publish the contract before this story starts. |
| CDC-09892 | RWB-P5-E1049-INF | DOR-RWB-P5-E1049-INF-22 | find it | Publish a contract fake library version and record its version in the contract story. |
| CDC-09908 | RWB-P5-E1049-OPS | DOR-RWB-P5-E1049-OPS-21 | header | Build status Not started to Done, with the contract published before this story starts. |
| CDC-09909 | RWB-P5-E1049-OPS | DOR-RWB-P5-E1049-OPS-22 | header | Publish the contract fake library and record its published version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09844 | RWB-P5-E1046-APP | CG-ALL-5904 | 16 | Add TC-E1-046-10 rows with Given, When and Then copied from AC8 and AC9 of section 7. Owner role QA. |
| CDC-09896 | RWB-P5-E1049-INF | DOR-RWB-P5-E1049-INF-12 | 16 | Register TC-P5-E1049-INF-01 to TC-P5-E1049-INF-06 with the Covers, Level and Data given in section 16. |
| CDC-09903 | RWB-P5-E1049-INF | CG-ALL-5931 | 16 | Add rows TC-P5-E1049-INF-01 to TC-P5-E1049-INF-06 with Given, When and Then copied from AC1 to AC6 |
| CDC-09906 | RWB-P5-E1049-INF | AC10 | 7 | AC10 not added |
| CDC-09922 | RWB-P5-E1049-OPS | CG-ALL-5939 | 16 | Add rows TC-P5-E1049-OPS-01 to TC-P5-E1049-OPS-06, with Given, When and Then copied from AC1 to AC6 in section 7. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09816 | RWB-P5-E1041-APP | GAP-1590 | 3 | State intake as event-started DocumentIntakeWorkflow with KEDA workers, the 15-minute schedule raising intake, and JOB-17 as a Temporal Schedule on the 1st Sunday monthly. |
| CDC-09883 | RWB-P5-E1049-CON | GAP-1590 | find it | State intake as event-started DocumentIntakeWorkflow with KEDA workers on rwb-document, keep the 15-minute schedule as the cadence that raises intake, and state JOB-17 as a Temporal Schedule on the 1st Sunday monthly. |
| CDC-09897 | RWB-P5-E1049-INF | GAP-1590 | find it | State intake as an event-started DocumentIntakeWorkflow with KEDA workers on queue rwb-document; keep the 15-minute cadence as a schedule that raises the intake; state JOB-17 as a Temporal Schedule on the 1st Sunday of the month. |
| CDC-09917 | RWB-P5-E1049-OPS | GAP-1590 | find it | State intake as an event-started DocumentIntakeWorkflow with KEDA workers on queue rwb-document; keep the 15-minute cadence as a schedule that raises the intake; state JOB-17 as a Temporal Schedule on the 1st Sunday of the month |

### RWB-P5-E2026-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09865 | RWB-P5-E1049-APP | GAP-0998 | 12 | Add rwb.document.OcrCompleted.v1 (eight-field payload, no personal data) to the rwb-document event catalogue and change the two-event count to three, or replace it with a status read. |
| CDC-09898 | RWB-P5-E1049-INF | GAP-0998 | find it | Add rwb.document.OcrCompleted.v1 (eight-field payload, no personal data) to the service event catalogue and the two-event count of rwb-document. |
| CDC-09935 | RWB-P5-E1050-APP | GAP-1003 | 12.3 | Declare the two classify operations, settle the resource field names, add rwb.document.DocumentClassified.v1 to the event catalogue, and amend event count and AC8 together |
| CDC-09951 | RWB-P5-E1050-CON | GAP-1003 | 2 | Add DocumentClassified.v1 to the event catalogue and amend the event count and AC8 in the same change. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09900 | RWB-P5-E1049-INF | GAP-1204 | find it | Publish the rescan notice template row (code, version, language, body, channel); extend LOV-NOTICE with the value the business owner chooses; baseline the Notice answer and the notification-path request and result; set retry values and the state list as data rows. |
| CDC-09901 | RWB-P5-E1049-INF | GAP-1207 | find it | Add one value for an operational notice to the case owner, named by the business owner, as a reference row; set DF-LEG-018 notice_type from it. |
| CDC-09938 | RWB-P5-E1050-APP | GAP-1007 | none | Add EXTRACTION_FAILED as a value of LOV-INTAKE-REVIEW in the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; no code change. |
| CDC-09954 | RWB-P5-E1050-CON | GAP-1007 |  | Add EXTRACTION_FAILED to LOV-INTAKE-REVIEW in the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; no code change. |

### RWB-P5-E1041-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09810 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-21 | header | Publish the contract and set the build status of RWB-P5-E1041-CON to Done. |
| CDC-09811 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-22 | header | Publish the contract fake and record its library version. |
| CDC-09818 | RWB-P5-E1041-APP | GAP-0995 | 3 | Publish the eight operations with paths, query parameters, field sets and statuses on /api/recovery/document/v1; add the C row for RWB-P3-E1018-CON or keep the ruling that the hold read is consumed and faked. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09870 | RWB-P5-E1049-APP | GAP-1051 | 3 | Publish the per-case document count and the version depth as seed parameters, shared with RWB-P5-E1025-APP. |
| CDC-09871 | RWB-P5-E1049-APP | GAP-1054 | 3 | Fix the held item count per exception shape and the page count per held item as seed parameters. |
| CDC-09904 | RWB-P5-E1049-INF | GAP-1051 | 5 | Publish per-case document count and version depth as seed parameters, reused by this story and RWB-P5-E1025-APP |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09911 | RWB-P5-E1049-OPS | CG-ALL-5934 | 12.5 | Add activity ingest: type Activity, P5, task queue rwb-document, registered by the same worker, creates the intake item from DocumentStored. |
| CDC-09912 | RWB-P5-E1049-OPS | CG-ALL-5935 | 12.5 | Add activity ocr: type Activity, P5, task queue rwb-document, registered by the same worker, selects and locks pending items, calls the engine and writes status and text. |
| CDC-09913 | RWB-P5-E1049-OPS | CG-ALL-5936 | 12.5 | Add activity classify: type Activity, P5, task queue rwb-document, registered by the same worker, owned by RWB-P5-E1050-APP. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09914 | RWB-P5-E1049-OPS | CG-ALL-5937 | 12.5 | Add activity extract to the Activities sheet, or name a catalogued activity for the extract step in section 12.5 |
| CDC-09915 | RWB-P5-E1049-OPS | CG-ALL-5938 | 12.5 | Add activity matchStep to the Activities sheet, or name a catalogued activity for the match step in section 12.5 |
| CDC-09916 | RWB-P5-E1049-OPS | DOR-RWB-P5-E1049-OPS-8 | find it | Add the DocumentIntakeWorkflow ID form and start rule, and activities ingest, ocr, classify, extract and matchStep to the Activities sheet |

### RWB-P5-E1041-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09834 | RWB-P5-E1041-CON | DOR-RWB-P5-E1041-CON-10 |  | Add empty, loading, error and no-access states for SCR-44 and SCR-47. |
| CDC-09837 | RWB-P5-E1041-CON | GAP-0995 | find it | Add the C row for the rwb-case P3 case contract, or state by ruling that the legal_hold read is consumed and faked. |

### OTHER:FSD P5 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09836 | RWB-P5-E1041-CON | GAP-1590 | find it | Restate AC-BG-P5-001-01 to AC-BG-P5-022-01 per Architecture v5: intake is an event-started DocumentIntakeWorkflow with KEDA workers on rwb-document; the 15-minute schedule only raises the intake; JOB-17 is a Temporal Schedule on the 1st Sunday monthly. |
| CDC-09864 | RWB-P5-E1049-APP | GAP-1590 | 12 | Restate AC-BG-P5-001-01 to AC-BG-P5-022-01: intake is an event-started DocumentIntakeWorkflow with KEDA workers; the 15-minute schedule only raises the intake; JOB-17 is a Temporal Schedule, monthly, 1st Sunday. |

### OTHER:TSD P6 v2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09866 | RWB-P5-E1049-APP | GAP-1204 | 13 | Publish the rescan template row (code, version, language, body, channel); extend LOV-NOTICE with the business-chosen operational value; baseline API-P6-002 Notice answer and the notification-path request and result. |
| CDC-09867 | RWB-P5-E1049-APP | GAP-1207 | 13,14 | Add one LOV-NOTICE value for an operational notice to the case owner, named by the business owner and loaded as a reference row; DF-LEG-018 is then set from it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09876 | RWB-P5-E1049-CON | CG-ALL-5922 | 12.2 | Provider story publishes GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml. |
| CDC-09943 | RWB-P5-E1050-CON | CG-ALL-5950 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} through the provider's CON story (P3 rwb-case). |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:Events sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09877 | RWB-P5-E1049-CON | CG-ALL-5923 | 12.3 | Add rwb.document.OcrCompleted.v1 on topic rwb.document.events.v1 to the Events sheet, per GAP-0998 and ASM-1780. |
| CDC-09944 | RWB-P5-E1050-CON | CG-ALL-5951 | 12.3 | Add rwb.document.DocumentClassified.v1 on topic rwb.document.events.v1, owner P5 rwb-document, as declared in section 12.3. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09879 | RWB-P5-E1049-CON | GAP-1205 | 7, 16 | Add rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1, produced by rwb-document, with the element list in AC9 |
| CDC-09918 | RWB-P5-E1049-OPS | GAP-0998 | 12 | Keep two events (DocumentStored, DocumentFieldsExtracted). OCR completion is a status read by classify and extract, not rwb.document.OcrCompleted.v1. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09886 | RWB-P5-E1049-CON | GAP-1206 | none | Six build rows RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON; three contract rows RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-case read contract (Not specified in the source documents (GAP-1206)) |
| CDC-09921 | RWB-P5-E1049-OPS | GAP-1206 | 3, 13 | Build: six H rows (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON). Contract: RWB-P3-E1042-CON, RWB-P3-E1043-CON, and a third C row for the rwb-case read (key not specified in the source documents, GAP-1206). |

### RWB-P5-E1049-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09893 | RWB-P5-E1049-INF | GAP-1205 | find it | Publish rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1 with the proposed element list, and add it to the catalogue and to RWB-P5-E1049-CON. |
| CDC-09910 | RWB-P5-E1049-OPS | GAP-1205 | n/a | Add rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1, produced by P5 rwb-document in the same transaction as the intake item state change, with elements intakeItemId, documentId, caseId (absent when no case), rescanPages, quality, languages and occurredAt. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09929 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-11 | 12.3 | Resolve the personal-data classing of the payload fields against the no personal data statement in 12.3 |
| CDC-09950 | RWB-P5-E1050-CON | GAP-0765 |  | Register rwb_case.case_document_link with its field IDs, including the classification columns added in V1050_1; rwb-case writes no P5 table. |

### RWB-P10-TE013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09932 | RWB-P5-E1050-APP | GAP-1005 | 3 | Name the provider, model, model version and field-extraction route; route stays a property of rwb-document with no model name in code |
| CDC-09949 | RWB-P5-E1050-CON | GAP-1005 |  | Name the extractor provider, model, model version and field-extraction route; keep the route a property of rwb-document with no model name in code. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09936 | RWB-P5-E1050-APP | GAP-0761 | 12.3 | Extend the Document schema and EV-16 payload with classifierVersion, reviewReason, candidateOneType with confidence, and candidateTwoType with confidence |
| CDC-09952 | RWB-P5-E1050-CON | GAP-0761 |  | Add classifierVersion, reviewReason, candidateOneType with its confidence and candidateTwoType with its confidence to the published contract and EV-16, or add one agreed classified event to the catalogue. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09940 | RWB-P5-E1050-APP | GAP-0766 | 5 | Add one boolean parameter key for the rwb-case classification handler, agreed with RW-COE, and a daily classification re-drive time outside the case-creation and allocation windows. |
| CDC-09957 | RWB-P5-E1050-CON | GAP-0766 | 8 | Add the rwb-case classification switch as one boolean parameter key, name agreed with RW-COE. The daily re-drive time of day is Not specified in the source documents (GAP-0766). Story BR7 updated to match. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09946 | RWB-P5-E1050-CON | CG-ALL-5952 | 4, 14 | Add a new message ID for sign-in with no identity or an expired token, and the story will cite it in section 14. |
| CDC-09948 | RWB-P5-E1050-CON | Definition of Ready item 9 Messages: Partial | 14 | MSG-P4-001 row reverted to its prior text and the placeholder for the message text. |

### 09 Testing and quality/Recovery Workbench Test Data Plan v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20616 | RWB-P5-E1050-CON | R-22156 |  | Document not read: no shell tool available to run docview.py, and Read cannot parse the .docx. Exact anchor text unknown; rerun with docview access. |
| CDC-20617 | RWB-P5-E1050-CON | R-22156 |  | Same as the APP item: the test data plan .docx could not be read here, so no exact anchor text exists for a valuation seeding insert. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09812 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-8 | 12 | Make the action field a reference to LOV-RETENTION-ACTION, not a closed enum; add rwb.document.RetentionApplied.v1 to Kafka Catalog v1. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09813 | RWB-P5-E1041-APP | DOR-RWB-P5-E1041-APP-11 | 4, 12 | Align P2 personal-data classing of its Fields with the no-personal-data statement for the event in section 4, or amend that statement. |

### OTHER:Environment configuration register (outside this set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09817 | RWB-P5-E1041-APP | GAP-1014 | 3 | Record the four channel classes, the partner MFT/SFTP route, the partner gateway in the DMZ, secret references for keys and mailbox credential, and scan capacity; network and security owners confirm before wave 1. |

### OTHER:rwb-document OpenAPI and AsyncAPI documents; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09819 | RWB-P5-E1041-APP | GAP-0996 | 3 | Freeze the eight operations, five resources and RetentionApplied schema; record the event addition in the Kafka Topic and Event Catalog. |

### OTHER:Story map (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09821 | RWB-P5-E1041-APP | GAP-2351 | 12.6 | Name RWB-P5-E1017-APP as the single owner of JOB-17; correct RWB-P5-E1055-APP and RWB-P5-E1065-APP section 12.6 at next version; record RWB-P5-E1052-APP as notice slice with no Schedule. |

### OTHER:rwb-access contract (API yaml) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09835 | RWB-P5-E1041-CON | DOR-RWB-P5-E1041-CON-6 | 10 | Declare the authorise check that enforces the eight section 10 roles on the rwb-document operations (DP-08). |

### RWB-P5-AD021-CON; RWB-P5-AD021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09840 | RWB-P5-E1041-CON | GAP-1026 | 12 | Carry the three P3 rows this story consumes with owner, 2 s budget and fakes, and record the missing C entries for step D1. |

### RWB-P6-E1046-CON; OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09850 | RWB-P5-E1046-APP | GAP-2343 | 3 | Name the identifier property of the version answer in RWB-P6-E1046-CON and fix the per-service login names in RWB-PLT-DB before wave-1 contract tests. |

### OTHER:FSD P7 v3; RWB-P6-E1046-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09852 | RWB-P5-E1046-APP | GAP-2453 | 12 | No column, index or BR3 change in this story |

### RWB-P5-E2026-CON; OTHER:split plan dependency rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09854 | RWB-P5-E1046-APP | GAP-2344 | header | Name the request fields of GenerateRequest and RegenerateRequest, the regenerate reason field, the index ix_document_template and the Flyway step name. |

### RWB-P5-E1046-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09855 | RWB-P5-E1046-APP | GAP-2346 | 7, 16 | Record one owning story per legacy criterion and mark this slice as test-case-bearing but criterion-free for the nine legacy test cases. |

### RWB-P5-E1049-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09861 | RWB-P5-E1049-APP | GAP-1205 | 12.3 | Add rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1, producer rwb-document, with the proposed element list, and declare it in the contract |

### RWB-P5-E1049-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09868 | RWB-P5-E1049-APP | GAP-1206 | 3,13 | Six H rows (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) and three C rows, the third being the rwb-case read (ID not specified in the source documents). |

### OTHER:Story dependencies v5 (Dependency classes sheet, check row X) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09872 | RWB-P5-E1049-APP | GAP-3234 | 3, 18 | Record that platform technical-enabler work is team-type work, tracked and never blocking; keep X on the ten rows. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09878 | RWB-P5-E1049-CON | DOR-RWB-P5-E1049-CON-8 | 12.1, 12.2 | Publish the three rwb-document paths and the rwb-case parameter path, as in CG-ALL-5919 to CG-ALL-5922. |

### OTHER:P3 screen definition SCR-31 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09882 | RWB-P5-E1049-CON | DOR-RWB-P5-E1049-CON-10 | none | Add empty, loading, error and no-access states to SCR-31 |

### RWB-P5-E2026-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09884 | RWB-P5-E1049-CON | GAP-0998 | find it | Add rwb.document.OcrCompleted.v1 with its eight-field payload to the event catalogue and the two-event count, or replace it with a status read used by classify and extract. |

### OTHER:Recovery Workbench Reference Data and Lists of Values v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09885 | RWB-P5-E1049-CON | GAP-1207 |  | Add a fifth LOV-NOTICE value for the operational rescan notice to the case owner. Value code and label: Not specified in the source documents (GAP-1207). Then set DF-LEG-018 notice_type from it. |

### RWB-P5-E1024-APP; RWB-P5-E1057-CON; OTHER:P3 parameters and reference-data contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09887 | RWB-P5-E1049-CON | GAP-1018 | 12 | Store takes an optional capture block (capturedAt, captureLatitude, captureLongitude, clientFileId, captureKind) as an additive v1 change; intake submit creates the item; five parameters under legacy codes; four lists under TSD codes. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-P1-E1065-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09889 | RWB-P5-E1049-CON | GAP-1051 | 16 | Publish the per-case document count and the version depth of a seeded document; keep both as seed parameters of this story and RWB-P5-E1025-APP |

### OTHER:Recovery Workbench P3 screen specification (SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09895 | RWB-P5-E1049-INF | DOR-RWB-P5-E1049-INF-10 | find it | Add empty, loading, error and no-access states to SCR-44. |

### OTHER:TSD P5 T-A.1 and T3.1 (technical specification P5) and the message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09899 | RWB-P5-E1049-INF | GAP-0999 | find it | Add the IntakeItem field list and the GET .../ocr-status path with derived JSON property names, and the workflow input and output, after sign-off by the four consumers; add the not-found message ID to the message catalogue. |

### RWB-P5-E1049-INF; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09902 | RWB-P5-E1049-INF | GAP-1206 | 3 | Contract dependencies row now names RWB-P5-E1049-CON (DOR-21); plan lists still to be corrected |

### OTHER:Message text baseline for MSG-P5-018 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09905 | RWB-P5-E1049-INF | GAP-1208 | 14 | Fill the document token from the rwb-document read with its display reference, or the document identifier where none is returned; record the decision in the baseline |

### OTHER:TSD P5 T-A.1 and message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09919 | RWB-P5-E1049-OPS | GAP-0999 | 14 | Publish derived property names for IntakeItem and OcrTextPage, GET .../ocr-status and the workflow payload for consumer sign-off; add the not-found message. Message ID: Not specified in the source documents (GAP-0999). |

### OTHER:TSD P6 v2 (T3.1 DF-LEG-018; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09920 | RWB-P5-E1049-OPS | GAP-1207 | 14 | Add a fifth value to LOV-NOTICE for an operational notice to the case owner, loaded as a reference row, then set DF-LEG-018 from it. Value name: Not specified in the source documents (GAP-1207). |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09923 | RWB-P5-E1049-OPS | GAP-1051 | find it | Publish the per-case document count and the version depth of a seeded document with RWB-P1-E1065-CON, held as seed parameters of RWB-P5-E1049-OPS and RWB-P5-E1025-APP. |

### RWB-P5-E1050-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09926 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-21 | 12 | Reach build status Done with the contract published |

### OTHER:SCR-31 screen specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09928 | RWB-P5-E1050-APP | DOR-RWB-P5-E1050-APP-10 | find it | Add empty, error and no access states for SCR-31 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09933 | RWB-P5-E1050-APP | GAP-0765 | not in chunk c02 | Register rwb_case.case_document_link with its field IDs; classification columns added in V1050_1; rwb-case writes no P5 table |

### OTHER:RWB-P5 build plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09934 | RWB-P5-E1050-APP | GAP-1002 | 3 | Add a C row for rwb-agent and the agent contract if the satellite stays external |

### OTHER:Test data plan (valuation inputs and RouteDecided record) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09937 | RWB-P5-E1050-APP | GAP-2133 | none | Seed valuation_ext inputs in rwb_source_data and the RouteDecided outcome as a decision record in rwb_decision; the valuation schema holds platform library objects only. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09945 | RWB-P5-E1050-CON | DOR-RWB-P5-E1050-CON-8 | 12 | Complete CG-ALL-5948 to CG-ALL-5951 so the four contract checks pass. |

### OTHER:Test data plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09953 | RWB-P5-E1050-CON | GAP-2133 |  | Seed valuation inputs in rwb_source_data (valuation_ext) and record the RouteDecided outcome as a decision record in rwb_decision; no valuation table is seeded. |

### RWB-P5-E1025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09955 | RWB-P5-E1050-CON | GAP-1020 checked-fields reader | 2 | Checked-fields path and shapes replaced with a placeholder. |

### 11 Delivery and operations/Recovery Workbench Build Calendar Nov 2026 to Jun 2027 v3.pdf (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20628 | RWB-P5-E1050-APP | R-22151 |  | C4 (CHANNELS AND AGENT) already has an rwb-agent row (RWB-SVC-P10). Story builds classifier internal, so no external-satellite row is needed. No edit made. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0360 | Reference-load owner, field-ID check and template body storage move in the target | Solution architect | Resolved (directive) |
| GAP-0362 | OCR trigger, worker count and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0363 | Classifier route, parameter home and agent run evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0761 | The classification answer the case needs is not carried by the published document contract or by EV-16 and EV-17 | Solution architect | Resolved (directive) |
| GAP-0762 | The rwb-case login name is not in the sources | Tech lead | Resolved (directive) |
| GAP-0763 | The texts of MSG-GEN-004 and MSG-GEN-006 are not in the source extracts | Solution architect | Resolved (directive) |
| GAP-0764 | No source names a classifier version label or its format | Solution architect | Resolved (directive) |
| GAP-0765 | The case document link is not an Owner row and has no field IDs | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0766 | The rwb-case switch key and the re-drive time of day are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0767 | The decision record is written here although DP-03 and its library story are not applied | Solution architect | Resolved (directive) |
| GAP-0995 | The target retention and virus-scan surface of rwb-document, the scan attributes of an upload and the C row of the P3 case contract are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0996 | No source names the retention and scan API of rwb-document, the class-load shape, the RetentionApplied event or the retention-class row shape the load writes | Solution architect, with the P5 TechX squad and the platform event team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0997 | OCR engine product, endpoint, engine version, capacity, intake request property names and the business-hours window are not named in the sources | Tech lead | Resolved (directive) |
| GAP-0998 | The pipeline publishes a third event name on rwb.document.events.v1 while the architecture catalogue lists two events for rwb-document | Solution architect | Resolved (directive) |
| GAP-0999 | Field-level names of IntakeItem, OcrTextPage and IntakeStatus, the OCR status path and the not-found message ID are not specified | Tech lead | Resolved (directive) |
| GAP-1000 | OCR engine capacity, admission queue depth, per-page text size and container quota are not named in the sources | SCB IT infrastructure | Resolved (directive) |
| GAP-1001 | The business-hours window, the deployment slot and the alert thresholds of the document intake pipeline are not specified | DevOps team | Resolved (directive) |
| GAP-1002 | The classify run is drawn as an rwb-agent child while the legacy story calls the P10 model gateway in process, and no source names the model provider, endpoint or model version | Solution architect with the TechX tech lead of rwb-document and the rwb-agent owner | Resolved (directive) |
| GAP-1003 | No source names a classification operation, path or field-level name, a 404 message identifier is absent, and a classification event would be a third event for rwb-document | Solution architect with the TechX contract owner of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1004 | The classifier artefact production and versioning, the evaluation report container, the alert thresholds and the deployment topology values are named by no source | DevOps engineer with the platform administrator and the data steward | Resolved (directive) |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1007 | The review reason EXTRACTION_FAILED is not a value of LOV-INTAKE-REVIEW | Data steward with the P5 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1014 | The four pickup channels, their credentials, their folder lifecycle, the partner DMZ position and the scan capacity are environment facts no source states | SCB IT infrastructure | Resolved (directive) |
| GAP-1018 | Field capture: the store capture block, the intake submit path, the parameter and list names, the service login name and the approval status are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1026 | The contract baseline of the retention-class and legal-hold surface fixes paths, shapes, statuses and a hold projection that no source names, and it consumes three P3 rows the plan does not carry | Tech lead of rwb-document, with the solution architect and the P3 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1034 | The scan operation path of the RWB-P5-E1041-CON malware-scan contract is not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1063 | The legacy template and catalog load path is replaced by the TSD admin template operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1064 | The data-dictionary read has no contract dependency in the plan | Solution architect | Resolved (directive) |
| GAP-1065 | No source says where the template body object lives | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1066 | The approver identity type of a template version is not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1067 | The request and answer field names of the five admin operations are not in T-A.2 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1068 | The service-side guard on the admin operations is not specified and DP-08 is not declared | Solution architect | Resolved (directive) |
| GAP-1204 | The values the rescan notice needs are not named in any source | Business analyst, P6 | Resolved (directive) |
| GAP-1205 | The document rescan event that triggers the notice is in no event catalogue and has no name or payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1207 | The notice list of values has no value for an operational rescan notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1208 | The document token of the rescan message has no named reference form | Business analyst, P6 | Resolved (directive) |
| GAP-1590 | The FSD makes document intake a 15-minute scheduled job while Architecture v5 makes it an event-started workflow with KEDA workers | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-2133 | rwb-valuation owns no table, so the plan does not say where a route decision is kept | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2343 | The catalog version answer read by rwb-document, its field names and the rwb-document login name are not specified, and the legacy document-to-template key becomes a soft cross-service reference | Solution architect, with the P5 TechX squad and the P6 rwb-comms squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2344 | The dependency rows of this slice name one contract only, and the request field names, the reason field, the index name and the migration step name are not specified | Solution architect, with the P5 TechX squad | Resolved (directive) |
| GAP-2345 | The rwb-comms catalog baseline declares no operation that answers the current Approved version for a template code, language and date | Tech lead of rwb-comms, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2346 | This slice owns no legacy acceptance criterion while the Work Package lists all nine legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
