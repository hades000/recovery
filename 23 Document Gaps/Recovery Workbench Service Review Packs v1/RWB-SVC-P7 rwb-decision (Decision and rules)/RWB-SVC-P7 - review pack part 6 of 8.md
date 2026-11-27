# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 6 of 8 (RWB-P7-E2021-APP to RWB-P7-E2027-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 140 |
| Cross-document (pending in another document) | 162 |
| Not applied (value not in the sources) | 32 |
| Open business decisions | 36 |
| Register gaps linked | 138 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E2021-APP | 17 | 40 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2021 APP Letter dispatch loop with proof of delivery from WIN v2.md |
| RWB-P7-E2022-APP | 15 | 24 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2022 APP SMS and LINE dispatch through NSS and LINE OA v2.md |
| RWB-P7-E2024-APP | 26 | 21 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2024 APP Field app photos and bills into the document hub v2.md |
| RWB-P7-E2025-APP | 24 | 25 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2025 APP Extraction for the stage 2 and 3 document types v2.md |
| RWB-P7-E2026-APP | 19 | 19 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2026 APP Document generation engine for contract, CA and mortgage templates v2.md |
| RWB-P7-E2027-APP | 39 | 31 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2027 APP Payment matching rules with the data team v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-E2021-APP | R-11303 | CG-ALL-7252 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2022-APP | R-11306 | CG-ALL-7264 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2024-APP | R-11315 | CG-ALL-7283 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2025-APP | R-11321 | CG-ALL-7298 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2026-APP | R-11325 | CG-ALL-7314 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2027-APP | R-11332 | CG-ALL-7334 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E1034-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22081 | GAP-1598 | Register gap | Product owner with the solution architect | Two of the module's business requirements describe the case record view and the case timeline, which the case service owns | Read both requirements as this service's contribution to the case record view: the notice and message block with its states, and the ordered notice and message history. The view, the timeline and the timer projection stay with rwb-case; the ledger entries stay with rwb-source-data. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4040-APP, RWB-P6-E4040-CON, RWB-P6-E4041-APP, RWB-P6-E4041-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22551 | GAP-1607 | Register gap | Product owner | Seven features in the Communications functional specification belong to other services in Architecture v5 | Keep the seven features in the source with their identifiers, mark them as not carried in section 5.1 of this PRD with their owning service, and raise the story-level split in the service work packages. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22552 | GAP-1603 | Register gap | Business lead with the data lead | No source states the notice, message or proof-of-delivery volumes | Size the volume test on the document volume of about 860,000 in 2027 as the upper bound for letters and on the interaction volume for messages, and replace both with the measured figures when the business lead provides them. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22554 | GAP-2092 | Register gap | Service owners of P6 rwb-comms and S8 rwb-deviation; business lead | The sources name different sets of deviation codes that raise a contact stop | Read the stop as X1 to X3, which is the wider and the safer reading, keep the hold reason on the notice, and ask the business lead to correct R-LIT-05. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22562 | GAP-1091 | Register gap | Business lead | The arithmetic of the 7-day proof window on the sent date is not stated | Confirm with the business lead and Legal counsel that the window is 7 calendar days counted from the sent date and that a notice is unserved on the first run on or after sent_date plus 7 days, then record the value and the rule in the reference data with its version. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22564 | GAP-1276 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P6 business analyst and the business owner | The dispatch decision record's payload, its field placement, the rule version label, the message id set, the parameter names, a panel id and the edge right of the two reads have no source | At the design review of wave 2 the solution architect, the data steward, the P6 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the dispatch columns of decision_log_entry (new columns or jsonb members of actions and outcome), the notice-reference filter and the answer field set of the read, the rule version label of the letter rules and their registry rows, the message ids and their texts, the panel id of the decision-log view, the parameter names and version labels of the page-size bound and the ingest target, and how the right and the scope reach the two reads at the edge; until then the story holds the assumed shape of ASM-B-P7-02-E2021-1, ASM-B-P7-02-E2021-2, ASM-B-P7-02-E2021-4, ASM-B-P7-02-E2021-5 and ASM-B-P7-02-E2021-6 and its nine criteria stand on that shape |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4039-APP, RWB-P6-E4039-CON, RWB-P7-E2022-APP | R-22574 | GAP-2091 | Register gap | Service owners of P6 rwb-comms and P1 rwb-source-data; product owner | The contact point and its consent state are a P6 feature but a P1 table, and no endpoint carries them | Keep the contact point and its consent in P1 rwb_source_data.contact_point_ext as the owner of record, and have rwb-comms read and maintain it through a P1 contract that the P1 API specification publishes. |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2022-APP | R-22577 | GAP-0954 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force and the unmask rows for DF-ACE-078 and DF-ACE-077 are not recorded | Record the masking version in force per environment in the policy pack load record with its approver and valid-from date, and add both contact point fields to the pack with unmasked false for every role before the first SIT run of SCR-03 |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2022-APP | R-22584 | GAP-1274 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P6 business analyst and the business owner | The contact entry payload, the read shape, the final call of a passed check, the reason-code list, the message id set, the parameter names, the rule version label of R-LIT-03 and the login name have no source | At the design review of wave 2 the solution architect, the data steward, the P6 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the channel, the reason code and the requesting role inside actions, the request and answer field set of the two reads, the final call of a passed check, the reason-code list and its labels, the message ids and texts of this slice, the parameter names and version labels of the page-size bound and the completeness target, the rule version labels, and the per-service login name; until then the story holds the assumed shape of ASM-B-P7-02-E2022-1 to ASM-B-P7-02-E2022-4 |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2022-APP | R-22585 | GAP-1275 | Register gap | Business owner, with the solution architect, P7 rwb-decision, and the P6 business analyst | The legacy story names one decision entry only for the contact stop, while the contact check has five refusal causes and a send that passed the check | Confirm at the wave 2 design review that one decision code X6 and one final call contact refused cover every refusal of the contact check with the reason code naming the cause, add the final call of a passed check to the service vocabulary as a reference row, and state in RWB-P6-E2022-APP and in this story that the local record of DP-03 is the write that blocks the send and the central append is the ledger copy under the completeness target |
| RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2024-APP, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P7-E2024-APP | R-22594 | GAP-0950 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masking rows and the mask version for the capture position are not specified | Record the DF-DOC-028 and DF-DOC-029 rows per role in the MASK-SIT-01 pack, with unmasked true for RW-CASEOWN and RW-RESTRUCT, false for RW-FIELDCOL and RW-PHONECOL and no row for SY-OCR, and let the platform masking library own one rendering per field type |
| RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2024-APP, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P7-E2024-APP | R-22596 | GAP-1281 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P5 business analyst and the business owner | The field-capture decision record's payload, read shape, message id set, panel id, parameter names and login name have no source | At design time of wave 2 the solution architect, the data steward, the P5 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the capture columns of decision_log_entry (new columns or jsonb members), the object-reference filter of the read and the answer field set, the message ids and their texts, the panel id of the decision-log view, the parameter names and version labels of the ingest target and the chain check, and the per-service login name; until then the story holds the assumed shape of ASM-B-P7-03-E2024-1, ASM-B-P7-03-E2024-2 and ASM-B-P7-03-E2024-3 and its seven criteria stand on that shape |
| RWB-ITG-E2025-ITG, RWB-P5-E2025-APP, RWB-P5-E2025-CON, RWB-P5-E2025-OPS, RWB-P7-E2025-APP, RWB-S2-E2025-APP, RWB-S4-E2025-APP | R-22604 | GAP-1285 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The extraction decision record's payload, value sets, read shape and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the extraction column set of decision_log_entry (new columns or jsonb members), the decision code of an extraction decision, the final-call value set, the threshold parameter names and version labels, the message ids and their texts, the document filter of the read and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2025-1 and its eight criteria stand on that shape |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-22619 | GAP-1287 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The generation record's payload, value sets, read shape, message set and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the template code, the template version, the treatment reference and the requesting role on decision_log_entry, the shape of the merge snapshot reference, the decision code D6.4 as a value of LOV-DECISION, the final-call list that holds GENERATED, the message ids and texts of a refused record and a duplicate append, the page-size parameter name, the search index and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2026-1 to ASM-B-P7-03-E2026-5 and its nine criteria stand on that shape |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1043-CON, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-28792 | GAP-2097 | Register gap | Service owners of P3 rwb-case and P4 rwb-access; business lead | Reference data is read from P4 in TSD P6 and from P3 in the plan default ruling | Follow R3 and DP-07: contact times and frequency are reference data of P3 rwb-case, read through C RWB-P3-E1043-CON. Access data, roles and DoA stay with P4. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-28804 | GAP-2222 | Register gap | Business lead | The legal hold reason list is not stated | Hold the reason list as a reference table of rwb-case loaded by RW-COE; the reason is stored as given until the list is approved. |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-28820 | GAP-0940 | Register gap | Compliance and PDPA officer | The masking version label and the DF-PTY-007 rows on the generation path are not specified | Load the DF-PTY-007 masking rows with unmasked false for RW-RESTRUCT, RW-CASEOWN, RW-TEAMMGR and SY-CASEWF under the SIT masking version, name the version in the policy pack load record, and leave the format to the one masking library every screen uses. |
| RWB-P7-E2027-APP | R-33455 | ASM-ALL-7334 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P7-E2022-APP | R-37528 | ASM-2252 | Register assumption |  | The shape of the contact entry and of its two reads is read as follows and is written in the story as a placeholder, never as a guess: the entry carries entryId, chainSeq, caseId, decisionCode, finalCall, ruleId, ruleVersion, inputsRef, an actions object holding the channel, the reason code and the requesting role, decidedAt, prevHash, entryHash, correctsEntryId and actorUserId, with no reason column of its own; the DecisionLogEntry answer carries the same fields and the DecisionLogPage answer carries items, page, size and total and is filterable by caseId with the from and to dates of TSD P7 v2 T-A.2; the inputs reference keeps the shape inputs/<businessDate>/<hash> of FSD P7 v3 AC-ALT-P7-001-02; and the search index of the case-and-date read is not named. | Solution architect, with the data steward and the P6 business analyst, at the design review of wave 2 and in the OpenAPI of the service |
| RWB-P7-E2022-APP | R-37529 | ASM-2253 | Register assumption |  | The refusal vocabulary of the contact check is read as follows: decision code X6 with final call contact refused covers all five causes of a refusal, and the cause is carried in the reason code as X6 Lost contact, X1 Dispute or complaint, No consent on the channel, Legal hold or Template withdrawn, the first two copied from the legacy message placeholder and the last three from the legacy scenario titles; the rule id of the entry is R-UNI-04 for a contact stop (with R-UNI-05 and R-DEV-16 as its supporting rules of BR2 and BR3, named in the rules rather than in rule_id), R-UNI-10 for no consent, R-UNI-20 for a legal hold and R-LIT-03 for a withdrawn template; a send that passed the check is appended with no reason code and with a final call that no source names, so the story carries it as a placeholder. | Business owner, with the solution architect and the Conduct and QA officer, at the design review of wave 2 |
| RWB-P7-E2024-APP | R-37532 | ASM-2271 | Register assumption |  | The shape of the field-capture decision entry and of its two reads is read as follows and is written in the story as a placeholder, never as a guess: the entry carries entryId, chainSeq, caseId, decisionCode, ruleId, ruleVersion, inputsRef, a recommendation holding the document type, the capture kind and the item result, finalCall, an object reference holding the document ID of a stored capture or the client file ID of a refused item, the client file ID, the document type code, the capture kind, the capture time, the message id of a refusal, decidedAt, prevHash, entryHash, correctsEntryId and actorUserId, as new columns of decision_log_entry; the DecisionLogPage answer carries items, page, size and total and is filterable by the object reference as well as by the eight query values of TSD P7 v2 T-A.2; the final call values are ACCEPTED, REFUSED and QUARANTINED, taken from the item result of the legacy field-capture response; MSG-P7-009 names ruleVersion or decisionCode and MSG-GEN-006 names the system that is unavailable; and the decision-log view of a case is described without a panel id. | Solution architect, with the data steward and the P5 business analyst, at the design review of wave 2 and in the OpenAPI of the service |
| RWB-P7-E2025-APP | R-37538 | ASM-2277 | Register assumption |  | The extraction decision entry carries, beside the TSD P7 v2 T3.1 columns of decision_log_entry, the document reference and version, the document type code, the field name, the field pattern or rule identifier and version, the parameter version in force, the confidence, the threshold value and the threshold reading; the final call is 'accepted' or 'sent to the review queue' as the work package fixes it; the decision code is a value of the list in force for the document decision and no new code is invented; the read answers the seven field groups of FSD P7 v3 AC-ALT-P7-001-02 plus the extraction facts, filtered by case and by the document reference the entry carries; and the panel id, the message ids of the extraction refusals and a feature switch of this capability are left unspecified until the design-time agreement of CG-B-P7-03-E2025-1. | Solution architect, P7 rwb-decision; data steward; business owner for the value sets |
| RWB-P7-E2026-APP | R-37543 | ASM-2282 | Register assumption |  | The generation entry carries, beside the TSD P7 v2 T3.1 columns of decision_log_entry, the template codes with their versions, the treatment reference and the requesting role as members of actions, and the merge snapshot reference in inputs_ref; the version evidence the FSD asks of every record (a rule, a model or an agent version) is the template code and version pair of this record; the decision code is D6.4 and the final call is GENERATED as the work package fixes them; a record that names no template code with its version is refused; and the container names, the member names and the snapshot shape are left as written here until the design-time agreement of CG-B-P7-03-E2026-1. | Solution architect, P7 rwb-decision; data steward; business owner for the value sets |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E2021-APP | R-06846 | DOR-RWB-P7-E2021-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or the 03 and 04 sources (prior search). Sign-off cannot be confirmed, so no value is written. |
| RWB-P7-E2021-APP | R-06848 | DOR-RWB-P7-E2021-APP-21 | header | Definition of Ready item 21 Contract published: Fail | RWB-P7-E2021-CON is not a story key of the set, so it is not added to Contract dependencies. |
| RWB-P7-E2021-APP | R-06849 | DOR-RWB-P7-E2021-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | No published contract fake library version is recorded in the sources. No version is invented; section 3 already marks the label Not specified (DOR-RWB-P7-E2021-APP-23). |
| RWB-P7-E2021-APP | R-26360 | CG-ALL-7253 | 3, 3.1 | Flyway file V2021_1__decision_log_dispatch_index.sql is not in the V0001..Vnnnn form | The next Vnnnn of the rwb_decision Flyway sequence is not in the sources, and the migration file name is not in this chunk. Left unchanged; the solution architect supplies the number. |
| RWB-P7-E2022-APP | R-06853 | DOR-RWB-P7-E2022-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off record in the story or sources (searched whole folder). A reference would be invented. Needs the epic design record. |
| RWB-P7-E2022-APP | R-06856 | DOR-RWB-P7-E2022-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded as published in the sources. A version would be invented. |
| RWB-P7-E2022-APP | R-06857 | DOR-RWB-P7-E2022-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Only the /v1 path is sourced. API Specification v3 info.version 3.0.0 is the spec version, not a contract version for this path. Not used. |
| RWB-P7-E2022-APP | R-18130 | DOR-RWB-P7-E2022-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The P2 fields classed as personal data are not named in any source. The data steward must list them. Story cannot be corrected until then. |
| RWB-P7-E2022-APP | R-18133 | DOR-RWB-P7-E2022-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Adding criteria and test rows for BR10, BR11 and BR13 needs section 7 and section 16 text, which is not in this chunk. |
| RWB-P7-E2022-APP | R-22553 | GAP-1610 | 8 | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | No rule package name in the sources, so none can be named. Evaluating conduct rules here conflicts with BR13 and DP-04. Needs the conduct and QA officer. |
| RWB-P7-E2022-APP | R-22575 | GAP-0405 | 3; 12.8; 13 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | NSS and LINE OA test doubles, seeding, evidence format and gate are not in the sources. Placeholders sit in sections 3, 12.8 and 13, outside this chunk. Needs ACE and QA agreement. |
| RWB-P7-E2022-APP | R-26366 | CG-ALL-7265 | 3 | Flyway file V2022_1__decision_log_contact_index.sql is not in the V0001..Vnnnn form | Next V number of rwb-decision's Flyway sequence is not in the sources (Not specified in the source documents (CG-ALL-7265)). Grep of the P7 story found only line 369, the DP-19 row. No edit. |
| RWB-P7-E2024-APP | R-11311 | CG-ALL-7276 | 4, 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 (cached copy, _work/msr/probe/cache) lists MSG-GEN-001 to 007 only; no 401 or no-session message ID. Placeholder stays until the business analyst maps it. |
| RWB-P7-E2024-APP | R-26371 | CG-ALL-7280 | 16 | Test cases cover other criteria in Test Cases v8 | The TC number had been copied into the AC column. Test Cases v8 is not in the source set, so alignment is not made here. |
| RWB-P7-E2024-APP | R-26373 | CG-ALL-7284 | 3, 3.1 | Flyway file V2_5_024__field_capture.sql is not in the V0001..Vnnnn form | The next rwb-decision Flyway number is not in the sources searched (03 folder grep). The migration name sits at line 400, which is outside this chunk. Cannot invent a number. |
| RWB-P7-E2024-APP | R-26374 | CG-ALL-7285 | 3, 3.1 | Flyway file V2024_1__decision_field_capture_entry.sql is not in the V0001..Vnnnn form | The next rwb-decision Flyway number is not in the sources searched (03 folder grep). The migration name sits at line 421, which is outside this chunk. Cannot invent a number. |
| RWB-P7-E2025-APP | R-06869 | DOR-RWB-P7-E2025-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source documents (searched 'epic design'). Sign-off not invented. Needs the epic design record. |
| RWB-P7-E2025-APP | R-06874 | DOR-RWB-P7-E2025-APP-8 |  | Definition of Ready item 8 Contract: Fail | Event type part belongs to CG-ALL-7293, not in this chunk. The 401 message ID is pending under CG-ALL-7292. Not resolved here. |
| RWB-P7-E2025-APP | R-11318 | CG-ALL-7292 | 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 has no 401 or session entry; system-unavailable does not fit no-session. Placeholder added at 12.1. Business analyst to confirm the message ID. |
| RWB-P7-E2025-APP | R-18142 | DOR-RWB-P7-E2025-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Only a quarantined scratch copy of Data Classification v5 exists, not a source of record. No personal-data field list for the story in sources; not invented. |
| RWB-P7-E2025-APP | R-26381 | CG-ALL-7299 | 13 | Flyway file V2025_1__decision_extraction_entry.sql is not in the V0001..Vnnnn form | Section 13 names V2025_1__decision_extraction_entry.sql in unchanged text. Next version number is assigned by the rwb-decision sequence owner at build time (E1008 DB, Sequencing). Not invented. |
| RWB-P7-E2026-APP | R-06875 | DOR-RWB-P7-E2026-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design sign-off is in the sources; the record ID is Not specified in the source documents (DOR-RWB-P7-E2026-APP-14). Nothing to confirm in the story. |
| RWB-P7-E2026-APP | R-18154 | DOR-RWB-P7-E2026-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in the chunk text, so no AC or TC row can be anchored or written for BR11, BR12, BR14, BR15. Needs those sections in a chunk. |
| RWB-P7-E2026-APP | R-22620 | GAP-1289 | 8 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Open at architecture review; BR13 keeps the source wording and no strict-mode acknowledgement is added here. |
| RWB-P7-E2026-APP | R-26388 | CG-ALL-7315 | 3, 3.1 | Flyway file V2026_1__decision_log_generation_index.sql is not in the V0001..Vnnnn form | The rule is in RWB P1 E1001 story (V<seq>__ four-digit, next free at merge), but no next number is in sources and the name is on line 454, outside the chunk. |
| RWB-P7-E2026-APP | R-28822 | GAP-1288 | 13 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | The metadata rows still omit the DP-added dependencies; their correction is deferred to the next story-set version, so the gap is not resolved in this story. |
| RWB-P7-E2027-APP | R-06881 | DOR-RWB-P7-E2027-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in 03 Requirements (grep rechecked). Sign-off cannot be recorded without the record. Needs the epic design record. |
| RWB-P7-E2027-APP | R-06885 | DOR-RWB-P7-E2027-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in 03 Requirements. Version not invented. Needs the fake publish record. |
| RWB-P7-E2027-APP | R-06887 | DOR-RWB-P7-E2027-APP-8 | 12.1 | Definition of Ready item 8 Contract: Fail | 401/404 message IDs and Catalog v1 RulePackageInForce payload not in sources. Section 12.1 text is outside this chunk, so no edit. Resubmit with 12.1. |
| RWB-P7-E2027-APP | R-18155 | DOR-RWB-P7-E2027-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-28, SCR-39 and SCR-40 state rows are outside this chunk and their text was not provided. No states invented. Resubmit with those screen sections. |
| RWB-P7-E2027-APP | R-22451 | GAP-2502 | 12.3 | Decision-record event naming and the boundary with RWB-P7-E1008-APP and RWB-P7-E2027-APP | Event name correction and boundary text sit in 12.3, whose current text was not provided. Resubmit with section 12.3 to make the exact edit. |
| RWB-P7-E2027-APP | R-26394 | CG-ALL-7329 | 3 | Flyway file V2027_1__decision_payment_match_governance.sql is not in the V0001..Vnnnn form | Next free number of the rwb-decision Flyway sequence is not in the sources. Searched folder 22 for db/migration and V0001; no rwb-decision sequence found. Line 424 is outside this chunk. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12461 | RWB-P7-E2021-APP | CG-ALL-7244 | 13 | Index column changed to decided_at and DESC removed from the index definition |
| CDC-12464 | RWB-P7-E2021-APP | DOR-RWB-P7-E2021-APP-7 | 11 | Trigger paragraph added in section 11 (P2) |
| CDC-12530 | RWB-P7-E2024-APP | CG-ALL-7271 | 3 | Record bill_amount as a field of the UTILITY_BILL document type in the owning reference data, or give it its dictionary name. |
| CDC-12531 | RWB-P7-E2024-APP | CG-ALL-7272 | 3 | Record due_date as a field of the UTILITY_BILL document type in the owning reference data, or give it its dictionary name. |
| CDC-12532 | RWB-P7-E2024-APP | CG-ALL-7273 | 3 | Record account_ref as a field of the UTILITY_BILL document type in the owning reference data, or give it its dictionary name. |
| CDC-12533 | RWB-P7-E2024-APP | CG-ALL-7274 | 8, 13 | Record tr_declog_append_only as the append-only trigger object on decision_log_entry, or give it its dictionary name. |
| CDC-12549 | RWB-P7-E2025-APP | CG-ALL-7290 | find it | Record review_only as a flag on the field definition in the owning document, or name the dictionary field; it is not an LDM v9 or Data Classification v5 field |
| CDC-12550 | RWB-P7-E2025-APP | CG-ALL-7291 | find it | Record trigger tr_declog_append_only on decision_log_entry as an object of the owning document (FSD P7 v3 AC-P7-001-01), or name the dictionary entry |
| CDC-12553 | RWB-P7-E2025-APP | DOR-RWB-P7-E2025-APP-7 | 11, 13 | Add review_only as a field of the document type field definition, or confirm it is rwb-document's type-table attribute. The trigger tr_declog_append_only is marked as a physical object in section 13. |
| CDC-12595 | RWB-P7-E2027-APP | DOR-RWB-P7-E2027-APP-7 | 11 | Confirm that DF-DEC-001 to DF-DEC-031 are all fields of decision_log_entry, or drop the IDs that are not. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12474 | RWB-P7-E2021-APP | GAP-2096 | find it | Read proof through the P1 contract on the ACE batch business date, match it to the notice by barcode, publish EV-15 NoticeDelivered from rwb-comms; no new job. |
| CDC-12492 | RWB-P7-E2021-APP | GAP-2095 | 1 | Record the partner instruction as S9 InstructionWorkflow and the internal alert as a P3 task. rwb-comms keeps the partner-instruction template only and no record of the internal alert. |
| CDC-12508 | RWB-P7-E2022-APP | GAP-1075 | 12.8 | Declare Case record right C on the gateway-bff composite route to SCR-03; add a Case record area to T6.1 and record its reconciliation. |
| CDC-12511 | RWB-P7-E2022-APP | GAP-1069 | 12.8 | Publish the request and result contract and the NSS and LINE OA result-code maps before wave 2 SIT entry. |
| CDC-12512 | RWB-P7-E2022-APP | GAP-1071 | 12 | Platform relay owner confirms that one attempt is one relay window and that path-internal retries are excluded from the R-UNI-34 count. |
| CDC-12524 | RWB-P7-E2022-APP | GAP-1601 | 12 | JOB-11 text sits in section 12, outside this chunk, so it is not resolved here; retry job reference needs that section. |
| CDC-12558 | RWB-P7-E2025-APP | GAP-0068 | header | Set rwb-litigation to wave 2 to match W-MAP and this story's wave 2. |
| CDC-12565 | RWB-P7-E2025-APP | GAP-2703 | 13 | Record the S2 Treatment to P5 Document cell as an open amendment; the read stays one-hop REST per RWB-P5-E2025-CON with 2 s timeout, breaker and no retry chain. |
| CDC-12570 | RWB-P7-E2025-APP | GAP-1704 |  | Request generation, review and signature through the P5 and P6 contracts, hold the document reference on the treatment, and keep no document content in schema rwb_treatment. |
| CDC-12598 | RWB-P7-E2027-APP | GAP-1626 | find it | Use the API Specification v4 pair GET /proceeds and POST /proceeds/{proceedsId}/match as the rwb-payment contract; confirm before the contract story closes. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12470 | RWB-P7-E2021-APP | DOR-RWB-P7-E2021-APP-12 | 16, 18 | Align the section 18 test lists with RTM v7 for TC-E2-021-01 to TC-E2-021-15 once RTM v7 is confirmed against the story. |
| CDC-12489 | RWB-P7-E2021-APP | CG-ALL-7251 | 18 | Align the test lists of REQ-OCC-003 and REQ-OCC-005 in RTM v7 with section 18 of RWB-P7-E2021-APP in its next version. |
| CDC-12520 | RWB-P7-E2022-APP | CG-ALL-7263 | 18 | Align the test lists for the five differing requirements with RWB-P7-E2022-APP section 18 in the next RTM version. |
| CDC-12544 | RWB-P7-E2024-APP | CG-ALL-7282 | 18 | Align REQ-DCM-013 in RTM v7 with section 18 of the story, which lists TC-E2-024-01 to TC-E2-024-20, in the next RTM version. |
| CDC-12546 | RWB-P7-E2025-APP | DOR-RWB-P7-E2025-APP-12 | 16 | TC-14 and TC-15 have no RTM v7 mapping in section 18; RTM v7 is not in the source set, so its differences stay open. |
| CDC-12569 | RWB-P7-E2025-APP | CG-ALL-7297 | 18 | Align the test case lists of the eight requirements in RTM v7 with section 18 of RWB-P7-E2025-APP, or the reverse, as QA decides; the RTM v7 lists are truncated in the evidence. |
| CDC-12586 | RWB-P7-E2026-APP | CG-ALL-7313 | 18 | Align the test lists of the seven requirements in the RTM with section 18 of this story in the next version. |
| CDC-12594 | RWB-P7-E2027-APP | DOR-RWB-P7-E2027-APP-12 | 12.7, 16, 18 | Align REQ-CHO-009 test case list with this story's TC-E2-027-01 to TC-E2-027-22 as given in section 18. |
| CDC-12613 | RWB-P7-E2027-APP | CG-ALL-7328 | 18 | Align the REQ-CHO-009 test list with section 18 of RWB-P7-E2027-APP (TC-E2-027-01 to TC-E2-027-22) in the next RTM version. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12468 | RWB-P7-E2021-APP | CG-ALL-7250 | 4, 14 | Add a new message ID for a dispatch record refused on its schema check (missing or invalid field), so the story cites it in place of MSG-P7-009 in sections 4, 14 and 18. |
| CDC-12471 | RWB-P7-E2021-APP | DOR-RWB-P7-E2021-APP-9 | 14 | Standard holds MSG-P7-009 for another meaning (CG-ALL-7250). Text Not specified; placeholder restored (GAP-1276; ASM-2250). |
| CDC-12534 | RWB-P7-E2024-APP | CG-ALL-7278 | 14 | Add a new message ID for 'An entry has a rule id with no version, or a decision code outside the list in force'; the story then cites it. |
| CDC-12535 | RWB-P7-E2024-APP | CG-ALL-7279 | 14 | Add a new message ID for 'The log, the reference list or the parameters are unavailable'; the story then cites it. |
| CDC-12536 | RWB-P7-E2024-APP | DOR-RWB-P7-E2024-APP-9 | 14 | State the standard meaning of MSG-P7-009 and MSG-GEN-006, or align the story's use of both IDs to it. |
| CDC-12551 | RWB-P7-E2025-APP | CG-ALL-7294 | 14 | Add a message ID for an entry with no rule or pattern version or a decision code outside the list in force; MSG-P7-009 keeps its decision-log meaning. The story cites it once it exists. |
| CDC-12554 | RWB-P7-E2025-APP | DOR-RWB-P7-E2025-APP-9 | 14 | Add a message ID for an entry with no rule or pattern version or a decision code outside the list in force, as in CG-ALL-7294; MSG-P7-009 keeps its standard meaning. |
| CDC-12560 | RWB-P7-E2025-APP | GAP-1022 | find it | Ship each unconfirmed value as an environment placeholder. Bind the model route endpoint and client credential as secret references. Verify the intake OCR endpoint. Name the two alert identifiers. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12462 | RWB-P7-E2021-APP | CG-ALL-7246 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log (API-P7-006) in rwb-decision.yaml through RWB-P7-E2021-CON. |
| CDC-12463 | RWB-P7-E2021-APP | CG-ALL-7247 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} (API-P7-007) in rwb-decision.yaml through RWB-P7-E2021-CON. |
| CDC-12465 | RWB-P7-E2021-APP | DOR-RWB-P7-E2021-APP-8 | 12.1 | Add GET /api/recovery/decision/v1/decision-log (API-P7-006) and GET /api/recovery/decision/v1/decision-log/{entryId} (API-P7-007) with their 200 and error responses, as section 12.1 states. |
| CDC-12571 | RWB-P7-E2026-APP | CG-ALL-7307 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log in rwb-decision.yaml through the RWB-P7 CON story. |
| CDC-12572 | RWB-P7-E2026-APP | CG-ALL-7308 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} in rwb-decision.yaml through the RWB-P7 CON story. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12473 | RWB-P7-E2021-APP | GAP-2090 | find it | Hold barcode, callback date and delivery status on the notice row as INT-14 and INT-15 mapping does; add a separate proof table only if a DB story needs it. |
| CDC-12490 | RWB-P7-E2021-APP | GAP-2094 | none | Add the P6 case-level notice list GET /cases/{caseId}/notices (Architecture v5 slide 17), or settle its path in the P6 API specification. Until then read notices per notice via GET /notices/{noticeId}. |
| CDC-12601 | RWB-P7-E2027-APP | GAP-0260 | 5 | Add an Ownership Map row for payment_match_rule: retired as a table by D-RCV-36, Owner P3 rwb-case (retired table), PAYMENT_MATCH rule package P7 rwb-decision; keep the 13 field rows marked retired. |
| CDC-12615 | RWB-P7-E2027-APP | GAP-1639 | 3 | Name the two event-started workflows after matchPayments and confirmBookings, register them on task queue rwb-payment, or confirm the activity is the unit. |

### RWB-P6-E2021-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12478 | RWB-P7-E2021-APP | GAP-1089 | find it | Fix WIN dispatch file name, record layout, acknowledgement fields and INT-15 proof result record with the WIN and rwb-integration owners; read proof results via rwb-integration contract or add C RWB-P1-E1066-CON. |
| CDC-12483 | RWB-P7-E2021-APP | GAP-1095 | 12 | Publish the Airflow-to-Schedule handoff row: the window signals the rwb-comms Schedule with the business date; a rerun of the same date writes no second file. |
| CDC-12488 | RWB-P7-E2021-APP | GAP-1092 | 7 | Declare the capability area and right per operation; gateway-bff asks rwb-access (DP-08) before the call; serve scope from the rwb-case case read, or add C RWB-P4-E1037-CON. |
| CDC-12493 | RWB-P7-E2021-APP | GAP-1094 | none | Fix the Notice component with id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus, sentType, holdReason, dispatchFileId and dispatchAttempts. Only id and caseId are required. Types: Not specified in the source documents (GAP-1094). Validate the additive rule against RWB-P6-E1052-CON Notice. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12481 | RWB-P7-E2021-APP | GAP-0946 | 12 | Add POST /authorise with request and answer schemas, stub it in the contract fake, and add access entry decision codes to the ledger code list. |
| CDC-12506 | RWB-P7-E2022-APP | GAP-2321 | 12.1 | Publish the authorise element, masking version label, covered field IDs and AC-READ granularity; story text needs no change. |
| CDC-12540 | RWB-P7-E2024-APP | GAP-0952 |  | Publish the authorise, me-permissions and masking-policies shapes; state whether a sync is authorised once for the manifest or once per item, and how the field list is carried. |
| CDC-12580 | RWB-P7-E2026-APP | GAP-0938 | find it | Add the authorise request and answer schema and publish it with RWB-P4-E1037-CON |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12501 | RWB-P7-E2022-APP | CG-ALL-7260 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. No story edit made. |
| CDC-12502 | RWB-P7-E2022-APP | DOR-RWB-P7-E2022-APP-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise (see CG-ALL-7260). Story side: messageId marked Not specified for 401, 422 and 503. |
| CDC-12525 | RWB-P7-E2024-APP | CG-ALL-7275 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-12573 | RWB-P7-E2026-APP | CG-ALL-7309 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12504 | RWB-P7-E2022-APP | DOR-RWB-P7-E2022-APP-1 | 1 | Register the roles named in section 1 (case owner who sends SMS or LINE, conduct officer, auditor) as role codes or names. |
| CDC-12521 | RWB-P7-E2022-APP | GAP-0956 |  | Record the JOB-11 service identity with its role class, scope and Case letters, and add decision codes for a send and a refused send to the ledger list. |
| CDC-12576 | RWB-P7-E2026-APP | DOR-RWB-P7-E2026-APP-1 |  | Register the role names of section 1 or confirm their role codes; the story uses RW-RESTRUCT as the requesting role code |
| CDC-12582 | RWB-P7-E2026-APP | GAP-0937 | find it | Load Documents letters: C for RW-RESTRUCT, C for RW-CASEOWN, C for SY-CASEWF, R for RW-TEAMMGR, no row for RW-PHONECOL |

### RWB-P5-E2025-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12547 | RWB-P7-E2025-APP | DOR-RWB-P7-E2025-APP-21 | find it | Record publication of the contract the story depends on; RWB-P5-E2025-CON is the listed contract dependency and no RWB-P7-E2025-CON exists |
| CDC-12548 | RWB-P7-E2025-APP | DOR-RWB-P7-E2025-APP-22 | find it | Record the published contract fake library version for the contract and its fakes |
| CDC-12557 | RWB-P7-E2025-APP | GAP-1020 | find it | Publish the checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes as a superset of the legacy list. Confirm names with S4 and S2 before wave 2. |
| CDC-12562 | RWB-P7-E2025-APP | GAP-1900 | find it | Declare the checked-fields read once as a GET on the rwb-document base with case and document type parameters, a CheckedField list answer, state filter and role masking. |

### RWB-S4-E2025-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12563 | RWB-P7-E2025-APP | GAP-1901 | 3 | Map only same-name codes onto legal_action and hearing columns; record filing_date to filed_date as one name difference; leave contract, approval, mortgage codes, party_names, notice_date, hearing_type, lawsuit_no unmapped. |
| CDC-12566 | RWB-P7-E2025-APP | GAP-2835 | 3 | Build against RWB-P5-E2025-CON; add source stamps and apply key to legal_action on its own Flyway sequence; map same-name codes only; count the twelve unmapped codes in the apply result. |
| CDC-12567 | RWB-P7-E2025-APP | GAP-2836 | 3 | One hearing per action and hearing_date; hearing_type empty with source stamp; update next_date when date held; closed or withdrawn action answers 409; confirm hearing_type with litigation BA. |
| CDC-12568 | RWB-P7-E2025-APP | GAP-1903 | 3 | Fix fill trigger, write key, request and answer element names, and the one-hearing-per-date uniqueness rule in rwb_litigation; take parameter and list calls from RWB-P3-E1042-CON and RWB-P3-E1043-CON. |

### RWB-P8-E2027-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12606 | RWB-P7-E2027-APP | GAP-1359 | 12 | Publish RuleResult as packageCode, versionInForce, ruleId, rowOrder and outputs; mark versionInForce and rowOrder as placeholders; rwb-decision confirms in RWB-P7-E1073-CON. |
| CDC-12607 | RWB-P7-E2027-APP | GAP-1360 | find it | Publish the payload field lists of TreatmentBooked, PaymentMissed and ProceedsMatched in the AsyncAPI fragment as a working read, identifiers and facts only, and confirm them with the catalogue consumers. |
| CDC-12609 | RWB-P7-E2027-APP | GAP-2507 | find it | Publish RuleResult as packageCode, versionInForce, ruleId, rowOrder and outputs with the NoPackageInForce outcome; declare the version-in-force read and the treatment installment-paid operation with placeholder names; publish the three payload field lists; declare DecisionRecorded read-only on the shared topic. |
| CDC-12611 | RWB-P7-E2027-APP | GAP-2705 | find it | Publish one read returning payment code, installment due date, match type, rule ID, package code and version, and shortfall for a case and plan; carry PLAN_RUNNING, PLAN_CURE_PERIOD, PLAN_BROKEN and BACK_TO_ROUTE_DECISION as treatment states; name payload members at major version 1. |

### RWB-P1-E1066-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12491 | RWB-P7-E2021-APP | GAP-2182 | none | Settle one case-scoped path family for the interaction ledger and realign the fake of RWB-P6-E2021-CON and the consumed row of RWB-P3-E2021-APP to it. |
| CDC-12507 | RWB-P7-E2022-APP | GAP-1070 | header | Name the contact-point read, consent and verified fields, failed-count update, and ledger record and delivery-update operations. |
| CDC-12509 | RWB-P7-E2022-APP | GAP-1605 | header | Expose contact point read, consent and verification write, and failed-count update through the rwb-source-data contract. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12590 | RWB-P7-E2027-APP | CG-ALL-7321 | 13 | Create story file RWB-P7-E1073-CON (rule-package contract of rwb-decision), or name the existing story key in section 13 and the metadata. |
| CDC-12591 | RWB-P7-E2027-APP | DOR-RWB-P7-E2027-APP-17 | find it | Create story file RWB-P7-E1073-CON, or correct the named dependency key to an existing story (see CG-ALL-7321). |
| CDC-12592 | RWB-P7-E2027-APP | DOR-RWB-P7-E2027-APP-21 | find it | Publish contract story RWB-P7-E2027-CON, or record the contract key this service builds against (section 13 names RWB-P7-E1073-CON). |

### RWB-P6-E2021-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12466 | RWB-P7-E2021-APP | GAP-1608 | 4 | Keep proof capture behind its feature flag until RWB-ACE-001 lands; agree the hand-entry fallback with the litigation business owner before wave 2. |
| CDC-12497 | RWB-P7-E2021-APP | GAP-1093 |  | Set deployment slot and replica counts once DL35 is decided; confirm the six alert thresholds at UAT and record them in each linked runbook entry |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12469 | RWB-P7-E2021-APP | DOR-RWB-P7-E2021-APP-11 | 11 | Personal-data fields are Not specified in the sources; the no-customer-value statement stays open until Data confirms. |
| CDC-12577 | RWB-P7-E2026-APP | DOR-RWB-P7-E2026-APP-11 |  | Classify the fields of decision_log_entry carried by the record (candidates: actorUserId, requesting role) or confirm none is personal data |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12472 | RWB-P7-E2021-APP | GAP-1597 | 8 | Keep notice proof fields in rwb-comms, read proof rows through the rwb-source-data contract, apply proof to the notice by barcode; ACE team settles the v_ace_pod writer. |
| CDC-12475 | RWB-P7-E2021-APP | GAP-2093 | find it | Hold approval in P7 ApprovalWorkflow as child of NoticeDispatchWorkflow with the notice as source; keep POST /notices/{noticeId}/approve in S4 as decision point; notice waits in Approved. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12480 | RWB-P7-E2021-APP | GAP-0948 | 7 | Name the JOB-10 runner service identity with role class NON_HUMAN_ACTOR, scope ALL and its Litigation R row. Code: Not specified in the source documents (GAP-0948). |
| CDC-12539 | RWB-P7-E2024-APP | GAP-0949 |  | Add the five DOCUMENTS rows (RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU, RW-PHONECOL R) to the PM-2026.12 permission file, and add a Documents column to the TSD P4 RBAC matrix. |

### RWB-P6-E2022-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12522 | RWB-P7-E2022-APP | GAP-1073 | n/a | Settle field-level definitions of MessageRequest and Interaction (types, lengths, formats, optionality) at the baseline review with the app and gateway-bff consumers. |
| CDC-12523 | RWB-P7-E2022-APP | GAP-1076 | n/a | Hold the message delivery status list SENT, DELIVERED, FAILED, READ as its own list; data steward confirms or names it. LOV-DELIVERY stays with the notice capability. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12528 | RWB-P7-E2024-APP | DOR-RWB-P7-E2024-APP-7 | 11 | Register bill_amount, due_date and account_ref as fields, or name their document type field definitions. |
| CDC-12575 | RWB-P7-E2026-APP | CG-ALL-7306 | 3 | Add transfer_price as the dictionary name of the case fact used in the merge fields, or name the dictionary field it maps to; nearest names are not confirmed as the same fact |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12537 | RWB-P7-E2024-APP | GAP-3194 |  | Raise an ACE DB story for the column drop in S2, S4, S5, S6, S7, P6 and P8, or attach the drop to the creating APP story, and cite the chosen story on row 121 before wave 2. |
| CDC-12556 | RWB-P7-E2025-APP | GAP-3194 | find it | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the 42-column source drop, or attach the drop to the creating APP story, and cite the chosen story on row 121 before wave 2. |

### OTHER:FSD P8 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12597 | RWB-P7-E2027-APP | GAP-1625 | find it | Replace the placeholder rows of A2.3.4.1 to A2.11.4.1 with testable main-flow criteria written from the feature statement, rules and fields, marked new; FSD owner confirms before wave 3 system test. |
| CDC-12599 | RWB-P7-E2027-APP | GAP-1631 | find it | Read ALS position via rwb-source-data after the next completed ACE batch; post ledger entries via rwb-integration; treat ATS, AMIS and LED routes as outside the 19 services until an interface is named. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12603 | RWB-P7-E2027-APP | GAP-1290 | 12 | Add the rollback body, dry-run body, governance decision code, rule_id and rule_version values, and success and MSG-P3-015 text before the wave 2 contract freeze. |
| CDC-12604 | RWB-P7-E2027-APP | GAP-1293 | 12 | Attribute the rule-package operations to P7 rwb-decision on /admin/rule-packages and /admin/rule-package-versions under /api/recovery/decision/v1; mark /admin/rule-versions as legacy with no target story. |

### OTHER:rwb-integration interface definition for INT-14 WIN (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12467 | RWB-P7-E2021-APP | GAP-1602 | 4 | Take the WIN registered-mail dispatch file layout as a versioned interface definition and hold it as a contract item before wave 2. |

### RWB-P6-E2021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12476 | RWB-P7-E2021-APP | GAP-1610 | find it | Name one versioned conduct-and-consent rule package governed in rwb-decision; package name Not specified in the source documents (GAP-1610); conduct and QA officer approves first version. |

### RWB-P1-E1016-CON; RWB-P1-E1066-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12477 | RWB-P7-E2021-APP | GAP-2181 | find it | Publish DP02 contact-and-consent row and vocabulary; add LETTER append required members; add UNSERVED to LOV-SEND-STATUS with version, or confirm the FAILED mapping with the ACE result code. |

### OTHER:Recovery Workbench TSD P4; OTHER:T6.1 RBAC matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12479 | RWB-P7-E2021-APP | GAP-0945 | 7 | Add a Litigation column with C and R letters for every role the legacy authority table names; publish the 14-area matrix as data with RWB-P4-AD002-APP; confirm letters with the matrix owner. |

### OTHER:Wave 2 harness pack (INT-14 and INT-15 fixtures, file-window control, seeding, evidence format) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12482 | RWB-P7-E2021-APP | GAP-0404 | 16 | Agree WIN and INT-15 fixtures and the file-window control with the ACE integration team; agree seeding, evidence format and pass gate with QA. |

### OTHER:SERVICE_LEVEL reference data (timer table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12484 | RWB-P7-E2021-APP | GAP-2218 | 7 | Load the task code NOTICE_UNSERVED, case owner role and due date from the SERVICE_LEVEL reference row before the wave starts. Due date: Not specified in the source documents (GAP-2218). |

### OTHER:rwb-source-data and rwb-decision published contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12485 | RWB-P7-E2021-APP | GAP-2220 | 12 | Take ledger and decision-record operation names and paths from the published contracts and fakes; REST bases /api/recovery/source-data/v1 and /api/recovery/decision/v1. |

### OTHER:Recovery Workbench TSD P3; OTHER:T3.1 data model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12486 | RWB-P7-E2021-APP | GAP-2221 | 9 | Remove the interaction row from the P3 module objects; the interaction ledger stays with rwb-source-data, and rwb-case reads and writes it only through that contract. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12487 | RWB-P7-E2021-APP | GAP-3183 | 9 | Name the INT-15 delivery result event and its topic, published by rwb-source-data and consumed by rwb-comms. Remove the JOB-09 loader step from the build notes. |

### OTHER:Administration Stories v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12494 | RWB-P7-E2021-APP | GAP-1096 | 14 | MSG-P6-005 row added from Administration Stories v4; MSG-P3-005 text is Not specified in the sources. |

### OTHER:Recovery Workbench data dictionary and policy pack load; OTHER:gateway-bff composite route field list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12495 | RWB-P7-E2021-APP | GAP-0947 |  | Fix the masking version in force in SIT; publish the addressee postal address and party field IDs with mask format; publish the SCR-18 and SCR-04 composite route field list (DP-19) |

### OTHER:rwb-source-data reconciliation story (JOB-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12496 | RWB-P7-E2021-APP | GAP-1090 |  | Assign REC-05 with its owner, frequency, break definition and output; add the notice break count and its series |

### OTHER:rwb-integration story of the JOB-10 WIN file transport (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12498 | RWB-P7-E2021-APP | GAP-2106 | 8 | Own the file window retry after a failed acknowledgement; publish FileDelivered or FileFailed to rwb-comms |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12499 | RWB-P7-E2021-APP | GAP-2219 |  | Allocate a key for the rwb-case-side flag that turns off the hold switch, ledger facts and task per environment at first build |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12500 | RWB-P7-E2021-APP | GAP-1277 | header | Platform and published dependency rows added to Contract dependencies; the second service baseline is not named in the supplied text. |

### OTHER:Decision-log store baseline (TSD P7 v2 T3.1; OTHER:GAP-1274) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12503 | RWB-P7-E2022-APP | CG-ALL-7259 | 3, 5, 13 | Record tr_declog_append_only as a database trigger object of the store, not a Logical Data Model or Data Classification field. Story already names it as an object only. |

### OTHER:P3 screen specifications for SCR-03; OTHER:SCR-04 and SCR-38 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12505 | RWB-P7-E2022-APP | DOR-RWB-P7-E2022-APP-10 | 12.1 | Add empty, loading, error and no-access states to SCR-03, SCR-04 and SCR-38. |

### OTHER:TSD P4 v3 T6.1 role to permission matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12510 | RWB-P7-E2022-APP | GAP-0953 | 10 | Add the Case record column and other decided capability areas; load the letters as PM-2026.12 rows before first SIT entry. |

### OTHER:ACE notification path result transport (NSS and LINE OA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12513 | RWB-P7-E2022-APP | GAP-1072 | 12.8 | State the result transport for both channels, callback or poll, for a known external reference. |

### OTHER:Platform security team and ACE notification path owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12514 | RWB-P7-E2022-APP | GAP-1074 | 3 | Publish the egress endpoint, client certificate issuer and secret names; chart carries references only; the egress check fails a release on a missing reference. |

### OTHER:RWB-P1 interaction record (DF-INT-002 to DF-INT-029) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12515 | RWB-P7-E2022-APP | GAP-1077 | 15 | P1 adds a template reference to the interaction record, or the SCR-04 timeline drops the template column. |

### OTHER:TSD P6 appendix T-A (rwb-comms API) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12516 | RWB-P7-E2022-APP | GAP-1078 | 18 | Add a P6 admin read over outbox rows in the exception state, or a P3 queue fed by a P6 event, and declare its owner before SCR-09 is built. |

### RWB-P6-E2022-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12517 | RWB-P7-E2022-APP | GAP-1599 | 18 | Keep the message outcome as an interaction ledger entry of rwb-source-data; add no fourth rwb_comms table; agree the interaction read path with P1 before wave 2. |

### RWB-P1-E1066-CON; RWB-P6-E2022-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12518 | RWB-P7-E2022-APP | GAP-2183 |  | Publish PartyApi.contactPoints, PartyApi.recordFailedContact and InteractionLedgerApi.updateDelivery with paths, requests, answers and errors; confirm delivery column types at contract review. |

### RWB-P4-E1037-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12519 | RWB-P7-E2022-APP | GAP-0955 | 3 | Publish the authorise, me-permissions and masking-policies shapes in RWB-P4-E1037-CON and the SCR-03 composite field list in RWB-PLT-N001-CON before the send story is built. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12526 | RWB-P7-E2024-APP | DOR-RWB-P7-E2024-APP-14 | Metadata | Record the signed epic design sign-off and cite it in the story. |

### RWB-P5-E2024-CON; RWB-P4-E1037-CON; RWB-P3-E1043-CON; RWB-P3-E1042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12527 | RWB-P7-E2024-APP | DOR-RWB-P7-E2024-APP-22 | Metadata | Publish the contract fakes and record the fake library version as published. |

### OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12529 | RWB-P7-E2024-APP | DOR-RWB-P7-E2024-APP-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise in the rwb-access API yaml; Kafka Catalog v1 names the DecisionRecorded event type rwb.decision.DecisionRecorded.v1. |

### RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12538 | RWB-P7-E2024-APP | GAP-2223 |  | Add stageCode and routeCode to the Case resource; record the authorise request and response shape in the rwb-access API specification; name the checklist contract story in the Ownership Map and C dependency set; load task code, owner role, discretion, due-date parameter and decision code as data rows. |

### RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12541 | RWB-P7-E2024-APP | GAP-1018 | 3 | Add an optional capture block (capturedAt, captureLatitude, captureLongitude, clientFileId, captureKind) to the store request as an additive v1 change; RWB-P5-E1057-CON to publish the intake submit path and shape; RWB-P3-E1042-CON and RWB-P3-E1043-CON to publish the parameter and list names under the legacy and TSD codes. |

### RWB-P5-E2024-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12542 | RWB-P7-E2024-APP | GAP-1019 | 12 | Declare the manifest as one JSON part named manifest and each file part named by its clientFileId; item properties clientFileId, kind, capturedAt, latitude, longitude and fileName with required set clientFileId, kind and capturedAt; 415 only for a request whose content type is not multipart/form-data; a refused type stays an item with status REFUSED and MSG-P5-001 at 201; Idempotency-Key window and not-found message ID carry the placeholder until the platform catalogue fixes them. |

### RWB-ITG-E2024-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12543 | RWB-P7-E2024-APP | GAP-1284 | 16 | Correct sections 12.2 and 12.8 to assert the DOCATT entry of each refused item rather than its absence, per the approved rule of one entry per stored document and per refused item, with DUPLICATE resolving to the first entry. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12545 | RWB-P7-E2024-APP | GAP-0951 | 15 | State the field app route: the capture sync as a composed call beside the rwb-document call and the SCR-30 panel as a parallel read, reached through the gateway-bff composite route, with rwb-access not called directly. |

### RWB-P5-E2025-APP; OTHER:SCR-31); OTHER:decision-log query story (SCR-38) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12552 | RWB-P7-E2025-APP | DOR-RWB-P7-E2025-APP-10 | 15 | Define the empty, loading, error and no-access states for SCR-30, SCR-31 and SCR-38. |

### OTHER:Service contract of RWB-SVC-P7 (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12555 | RWB-P7-E2025-APP | GAP-1713 | find it | Record once the owning service of each dependency code by capability: approval P7, case P3, documents P5, communications P6, valuation S1. Carry the duplicate FEAT-CHO-08 as written. |

### OTHER:Extraction test and harness pack (QA; OTHER:P5 and P10 owners) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12559 | RWB-P7-E2025-APP | GAP-0407 | find it | Agree the classifier version, the masked sample pack beyond 60 documents, the extraction report format, SIT seeding of DOCTYPE-2026.12 and the accuracy pass mark, the evidence format and the gate. |

### OTHER:rwb-treatment story and TSD S2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12561 | RWB-P7-E2025-APP | GAP-1876 | find it | Take the checked-fields operation and payload from RWB-P5-E2025-CON. Add contract_amount, contract_date, mortgage_amount, registration_date, land_office, title_doc_no and source_document_id, source_doc_version, source_table_version. Keep party_names masked and unstored. Stamp tableVersion. |

### RWB-S2-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12564 | RWB-P7-E2025-APP | GAP-2702 | 3 | Take operation, payload and element names from RWB-P5-E2025-CON; add fact and source columns to treatment on its own Flyway sequence; map same-name codes only; stamp tableVersion; mask party_names as returned. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; OTHER:rwb-access published contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12574 | RWB-P7-E2026-APP | DOR-RWB-P7-E2026-APP-8 | 12.1 | Add GET decision-log and GET decision-log/{entryId} to rwb-decision.yaml; publish POST /api/recovery/access/v1/authorise in rwb-access |

### OTHER:FSD S2 and service contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12578 | RWB-P7-E2026-APP | GAP-1713 | find it | Replace each FEAT prerequisite with the owning service contract: approval P7, case P3, documents P5, communications P6, valuation S1 |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12579 | RWB-P7-E2026-APP | GAP-1580 | find it | Add a generation section for REQ-DCM-012 carrying FR-P5-026 and AC-P5-019 |

### OTHER:Recovery Workbench Gap Register v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12581 | RWB-P7-E2026-APP | GAP-0408 |  | Record the recommended resolution: agree the DIL-CONTRACT, DIL-CA, DIL-MORTGAGE and RES-AGREEMENT template fixtures, the PDF/A-2b check and Thai font pack with the P5 and P6 owners, and the wave 2 harness pack, seeding and evidence format with QA (owner: Integration lead). |

### OTHER:PM-2026.12 policy pack and reference data load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12583 | RWB-P7-E2026-APP | GAP-0939 | find it | Add SY-CASEWF with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL, under its own approver |

### OTHER:TSD S2 T3.1 (rwb-treatment); RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12584 | RWB-P7-E2026-APP | GAP-1878 | 12 | Add two nullable treatment columns (document reference, pinned template version) with index; take the generation operation and its shapes from RWB-P5-E2026-CON. |

### OTHER:rwb-comms service baseline (V-baseline migration); API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12585 | RWB-P7-E2026-APP | GAP-2393 | 12 | Add an rwb_comms table for the generation request key and request lock; record the rwb-document create operation from RWB-P5-E2026-CON in the P6 API specification. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-S2-E2026-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12587 | RWB-P7-E2026-APP | GAP-1704 | 12 | Hold the document reference on the treatment and keep no document content in rwb_treatment; request generation, review and signature through the P5 and P6 contracts. |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12588 | RWB-P7-E2026-APP | GAP-1024 | 12 | Declare the path POST /cases/{caseId}/generated-documents; type the four provider interfaces; fix the three resources and their required sets; declare one event with five payload fields. |

### API:(service not named); OTHER:gateway-bff route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12589 | RWB-P7-E2026-APP | GAP-2394 | 12 | Add the generated-documents operation with the next API-P6-nnn ID allocated at D1 and its gateway-bff route. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12593 | RWB-P7-E2027-APP | CG-ALL-7326 | 16 | Add Story test cases rows for TC-E2-027-12 (Given, When, Then from AC13) and TC-E2-027-13 (from AC10), and TC-E2-027-14 to TC-E2-027-22 added by this story. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12596 | RWB-P7-E2027-APP | GAP-2395 | find it | Name the rwb-comms rule package code and read the three Epic 2 codes through the contract fixture set; settle assignment with the rule registry owner before integration. |

### OTHER:TSD P8 v2 T-A.1 (P4 Technical Solution Design) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12600 | RWB-P7-E2027-APP | GAP-2313 | 12 | Correct TSD P4 T-A.1 at the next version so the six rule-package and rule-version endpoints are owned by P7 rwb-decision; P4 keeps only the loader and approver rights. |

### OTHER:Wave 2 harness pack and ALS fixture specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12602 | RWB-P7-E2027-APP | GAP-0409 | 16 | Agree the ALS payment fixture, JOB-07 window control, rule-version load route, SIT seeding and evidence format with P8, P7 and QA. No values invented here. |

### RWB-P8-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12605 | RWB-P7-E2027-APP | GAP-1355 | 7 | Add C RWB-P7-E1073-CON to the C row of RWB-P8-E2027-APP in D1. Story-side AC6 rewrite not applied because section 7 text was not in this chunk. |

### OTHER:rwb-decision deployment values files (three files) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12608 | RWB-P7-E2027-APP | GAP-1361 | find it | Add a placeholder chart value for each numeric operations value (alert thresholds, staleness window, outbox lag and dead-letter limits, pool size, canary percentage, probe timings) and close them with the DL11 decisions before UAT. |

### OTHER:deployment values files and platform secret-store catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12610 | RWB-P7-E2027-APP | GAP-2508 | find it | Add a chart value for each numeric operations value and close with DL11 before UAT; reference each secret and the workload identity by role and record their names in the platform secret-store catalogue, keeping the rwb-payment login (DP-02). |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12612 | RWB-P7-E2027-APP | GAP-1291 | find it | Record RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON as non-blocking H or C dependencies, built against their fakes. |

### OTHER:FSD P8 v3 and TSD P8 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12614 | RWB-P7-E2027-APP | GAP-1624 | 18 | Fill the Requirements served table of FSD P8 v3 and the T8 Requirement traceability table of TSD P8 v2 with REQ IDs, or state that P8 has no requirement ID of its own. |

### RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12616 | RWB-P7-E2027-APP | GAP-1357 | 3 | Reconcile the PAYMENT_MATCH label PMT-2026.12 to PM-2026.12 as the one version row in rwb-decision before SIT. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12617 | RWB-P7-E2027-APP | GAP-1358 |  | Confirm consumers rwb-decision and rwb-reporting. DecisionRecorded is read only by rwb-payment for ledger acknowledgement. No second writer. |

### OTHER:Platform secret-store catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12618 | RWB-P7-E2027-APP | GAP-1362 |  | Record names for the rwb-payment per-service login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity. Chart references them by role. |

### OTHER:Build notes RWB-E2-027, step 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12619 | RWB-P7-E2027-APP | GAP-3188 |  | Replace the P4 endpoint line with one rule-package load path in rwb-decision. P4 reference load endpoint only for non-package reference data. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12620 | RWB-P7-E2027-APP | GAP-1296 |  | Keep metadata rows. Carry the DP-added H and C dependencies in section 13 as build-against fakes, with Ready to start Day 1. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20799 | RWB-P7-E2021-APP | R-22567 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20814 | RWB-P7-E2027-APP | R-22628 |  | Change is to TSD P4 T-A.1 rwb-decision rule-package endpoints. This P8 document holds only API-P8-001 and API-P8-002. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0068 | Wave conflict S4 / EP02 | Tech lead | Resolved (directive) |
| GAP-0218 | LOV-MATCH-TYPE is used by payment_match_rule, a table the target drops and the Ownership Map does not carry | Center of excellence | Resolved (directive) |
| GAP-0260 | payment_match_rule is in the inventory but not in the Ownership Map, and D-RCV-36 retires it as a table | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0404 | The WIN dispatch harness pack and the proof-file test window are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0405 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0406 | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | Integration lead | Resolved (directive) |
| GAP-0407 | The extraction harness pack, the classifier version and the cross-service reader pack are not specified | Integration lead | Resolved (directive) |
| GAP-0408 | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0409 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0937 | The Documents letters per role are not in the P4 RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0938 | The authorise request and answer for a document generation request are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0939 | The role row, class and scope of the SY-CASEWF service identity are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0945 | rwb-access letter dispatch loop: the TSD RBAC matrix has no Litigation column, so the LITIGATION C and R letters the legacy authority table names are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0946 | rwb-access letter dispatch loop: the authorise request and answer shape for a notice request, a notice read and a dispatch read is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0947 | rwb-access letter dispatch loop: the masking version in force in SIT, the field IDs of the addressee postal address and party field on the notice panel, and the composite route field list are not specified | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0948 | rwb-access letter dispatch loop: the role code and scope of the service identity that runs JOB-10 are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0949 | The Documents letters per role are not carried by the P4 access documents | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0951 | Whether the field app reaches the authorise path through gateway-bff or directly is not specified | Solution architect, P4 with the gateway-bff route owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0952 | The request and answer shape of the authorise call for a multi-item sync is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0953 | The Case record letters per role are not in the TSD P4 role-to-permission matrix | Security administrator with the P4 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0955 | The authorise shape for a send and the field list of the composite route are not specified | Solution architect, P4 and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0956 | The rights of the JOB-11 service identity and the decision code of a send are not recorded | Security administrator with the P4 build squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1018 | Field capture: the store capture block, the intake submit path, the parameter and list names, the service login name and the approval status are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1019 | Field capture contract: the manifest part and item field names, the stored-answer window, the not-found message and the 415 reading are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1021 | The published Java reader becomes a REST contract no source names, the extraction operations belong to another baseline of the same service, and the plan lists no C row for the case read | Tech lead | Resolved (directive) |
| GAP-1022 | The deployment values of the extension are not specified: the model name and the provider product behind the agent route, the alert thresholds and identifiers, the evaluation cadence, the business-hours window and the reader thresholds | DevOps team | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1024 | The generation contract baseline has no settled operation name, no published provider shapes and two consumed contracts outside the plan | Solution architect | Resolved (directive) |
| GAP-1069 | The NSS and LINE OA request and result contract is not in the source set | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1070 | The interaction ledger write and the contact-point failed count are not named in this key's contracts | Solution architect | Resolved (directive) |
| GAP-1071 | The retry mechanism and the five-attempt limit sit on two different readings of JOB-11 | Solution architect | Resolved (directive) |
| GAP-1072 | How the LINE OA read status reaches rwb-comms is not specified | Solution architect | Resolved (directive) |
| GAP-1073 | The MessageRequest and Interaction field-level definitions are not specified | Tech lead of rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1074 | The NSS and LINE OA egress credentials, certificate and endpoint are not specified | Platform security team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1075 | DP-08 is not in the pattern set and the case facts of the conduct check are not in the contract dependencies | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1076 | The message delivery status vocabulary conflicts with LOV-DELIVERY | Data steward | Resolved (directive) |
| GAP-1077 | The timeline shows the template of a message and the interaction ledger carries no template field | Business analyst, P6 | Resolved (directive) |
| GAP-1078 | SCR-09 Exception queue has no owner in the sources | Solution architect | Resolved (directive) |
| GAP-1089 | The WIN dispatch file, its acknowledgement and the INT-15 proof result record have no layout and no owning operation in the sources | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1090 | The daily reconciliation REC-05 that the legacy story names has no owner and no mechanism in the sources | Solution architect | Resolved (directive) |
| GAP-1092 | The scope test of the notice read has no scope source in the dependencies of this story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1093 | The deployment slots, the worker placement and the alert thresholds of the dispatch loop are not stated | DevOps lead | Resolved (directive) |
| GAP-1094 | The Notice response fields and types are named by the legacy story but not specified by the contract sources | Tech lead | Resolved (directive) |
| GAP-1095 | The handoff from the Airflow WIN file window to the 16:00 Temporal Schedule has no mechanism in the sources | Solution architect | Resolved (directive) |
| GAP-1096 | The message text of MSG-P6-005 and MSG-P3-005 is not given by the legacy story or the P6 extracts | Tech lead | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1283 | The decision code of a field-capture entry is D6.5 in the legacy metadata but DOCATT on the store path | Business analyst, P7, with the business analyst of P5 rwb-document and the data steward | Resolved (directive) |
| GAP-1284 | No source settles whether an item the store refuses leaves a DOCATT entry | Business analyst, P7, with the P5 business analyst and the integration lead of RWB-ITG-E2024-ITG | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1289 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Solution architect, with the platform team and the P7 rwb-decision owner | Resolved (directive) |
| GAP-1290 | PAYMENT_MATCH registry governance: shapes, decision-record payload, message set and promotion and rollback semantics are not specified | Solution architect, with the P7 business analyst and the rule owner RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1293 | The rule-package operations: the legacy P4 attribution and the /admin/rule-versions paths against P7 and /admin/rule-package-versions | P7 solution architect, with the API specification owner | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1355 | The AC6 package load and the rule-evaluation contract have no C row in this key | Solution architect | Resolved (directive) |
| GAP-1356 | The ordering column is called row order in the story and priority in the TSD | Data steward | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1358 | DecisionRecorded is listed as consumed here but the catalogue names only two consumers | Integration architect | Resolved (directive) |
| GAP-1359 | The rule-evaluation result has no published schema and two of its field names are not given | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1360 | The three payment event payloads have no schema in any source | Integration architect | Resolved (directive) |
| GAP-1361 | No numeric operations value is specified for the matching service | DevOps engineer | Resolved (directive) |
| GAP-1362 | The secret names, the workload identity and the certificate of rwb-payment are not specified | Identity and access team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1599 | The message record and its delivery status have no table in the service under Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1600 | The retry limit for a send is five in the functional specification and three in the non-functional requirements | Solution architect | Resolved (directive) |
| GAP-1601 | The functional specification names JOB-11 as the retry job for sends, and Architecture v5 makes JOB-11 the outbox relay in every service | Solution architect | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1605 | The contact repository and the consent state are held in an extension table the source-data service owns | Solution architect | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1609 | The notice period timer and the transfer on a non-delivered notice are the case service's, and the trigger is not fixed | Solution architect with P3 | Resolved (directive) |
| GAP-1610 | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | Conduct and QA officer with rwb-decision | Resolved (directive) |
| GAP-1624 | FSD P8 issues no requirement ID, so the product requirement cannot be traced to an FSD requirement | Business analyst, P8 | Resolved (directive) |
| GAP-1625 | Eight of the eleven P8 features carry a placeholder acceptance criterion instead of a testable one | Business analyst, P8 | Resolved (directive) |
| GAP-1626 | The two operations named in Architecture v5 slide 17 are not the two operations in the API Specification and the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1628 | The matching values have no table and no owner after payment_match_rule was retired | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1876 | The checked-fields operation and payload on the treatment side, the treatment columns that carry the contract and mortgage facts, the masking of the treatment read and who stamps the type-table version are not specified | Solution architect with the rwb-treatment and rwb-document squads | Resolved (directive) |
| GAP-1877 | Architecture v5 puts the S2 call to P5 in the Temporal column while the legacy published interface and DP-11 make the checked-fields read one REST hop | Solution architect with the platform workflow team, rwb-document and rwb-treatment | Resolved (directive) |
| GAP-1878 | The treatment-side generation call, its two columns, the merge-field set and the generation event are not specified | Solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-1880 | The treatment-side matching read, the shortfall columns, the breach decision code and the plan-check cadence are not specified | Solution architect with the rwb-treatment and rwb-payment squads | Resolved (directive) |
| GAP-1881 | PAYMENT_MATCH is the rwb-payment matching package while this slice evaluates it for the plan breach on the treatment side | Solution architect with rwb-decision, rwb-payment and rwb-treatment | Resolved (directive) |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1899 | DP-09 and DP-10 are in the pattern list but this slice produces no event, consumes no event and registers no Schedule, and DocumentFieldsExtracted is consumed by rwb-case only | Solution architect | Resolved (directive) |
| GAP-1900 | The sources give only the Java interface of the field reader: no REST operation, path, transport or field-level name is named for the checked-fields read | Solution architect, with the rwb-document owner (P5) | Resolved (directive) |
| GAP-1901 | The mapping of an extracted field code onto an S4 column is not stated, and eleven codes, hearing_type and lawsuit_no have no counterpart of the same name | Business analyst and solution architect, with the rwb-document owner | Resolved (directive) |
| GAP-1902 | REQ-DCM-017 and REQ-DCM-018 are in the plan's requirement list for this story but in no row of the legacy traceability table, and legacy section 19 puts them out of scope | Business analyst | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1904 | SCR-19 Litigation workspace is listed with its first release in E5, while this story is a wave 2 story released on 31 December 2026 | Solution architect and the edge owner | Resolved (directive) |
| GAP-1905 | No approval of the realigned story or of the sources it consumes is recorded, so the story runs in Draft | Solution architect | Resolved (directive) |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2093 | The notice approval sits in P6, P7 and S4 at once | Service owners of P6 rwb-comms, P7 rwb-decision and S4 rwb-litigation | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2095 | The partner instruction and the internal alert are rows of the design but are not rwb-comms notices in the target | Service owners of P6 rwb-comms, S9 rwb-partner and P3 rwb-case | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2105 | SMS and LINE dispatch stays open under DL30 while Architecture v5 gives the call to rwb-comms | Solution architect | Resolved (directive) |
| GAP-2106 | The WIN notices file window JOB-10 has two owners and no single accountable service | Solution architect | Resolved (directive) |
| GAP-2181 | The DP02 contact-and-consent row, the consent vocabulary, the members of the letter append and the unserved status are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2182 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2183 | The rwb-source-data slice of RWB-E2-022 has no API shapes, no lists and no delivery columns in the source | TechX API owner, with the data steward (RW-DATASTEW) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2217 | The rwb-case slice of RWB-E2-021 owns no legacy acceptance criterion | Business analyst, P3 | Resolved (directive) |
| GAP-2218 | The task due date and the task code of an unserved letter are not stated | Business analyst, P3 | Resolved (directive) |
| GAP-2219 | No feature flag is named for the rwb-case slice | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2220 | The operation names and paths of the ledger and decision-record contracts are not in the source set | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2221 | The interaction ledger is listed in the P3 data model but owned by rwb-source-data | Solution architect | Resolved (directive) |
| GAP-2223 | The case-side slice of the field-capture path rests on answers no source specifies: the stage and route fields of the case resource, the authorise call shape, the contract story of the checklist read, and the task data | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2311 | Values of the payment-matching access profile that the legacy story does not state | Business analyst, P4 | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2313 | The rule-package endpoints are P4 in the legacy contract and P7 in Arch v5 | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2314 | No legacy acceptance criterion of RWB-E2-027 belongs to the P4 slice | Business analyst, P4 | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2393 | rwb-comms generation request key and P5 document-create operation are not specified | Service owner, rwb-comms; service owner, rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2394 | Generated-documents endpoint is not in the P6 operation inventory | Architecture owner; service owner, rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2502 | Decision-record event naming and the boundary with RWB-P7-E1008-APP and RWB-P7-E2027-APP | P7 solution architect, with the event platform owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2507 | The consumed rule-evaluation result, the treatment installment-paid call, the three event payloads and the shared record's consumer list have no published schema or operation name | Solution architect, with the owners of rwb-decision, rwb-treatment and the event catalogue | Resolved (directive) |
| GAP-2508 | No numeric operations value and no name of a secret, identity or certificate is specified for the matching deployment | DevOps engineer, with the platform administrator and the identity and access team | Resolved (directive) |
| GAP-2702 | The treatment-side checked-field read, the fact columns it fills, the type-table version stamp and the unmapped field codes are not specified | Tech lead of rwb-treatment with the P5 owner of the checked-field contract and the rwb-treatment data owner | Resolved (directive) |
| GAP-2703 | Architecture v5 puts the S2 read of rwb-document on Temporal while the legacy interface and DP-11 make it one REST hop | Solution architect with the P5 contract owner and the platform Temporal owner | Resolved (directive) |
| GAP-2705 | The match consequence that rwb-treatment consumes is not published, and no source names the plan states the treatment row holds after a match | Contract owner of rwb-treatment with the owner of rwb-payment and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2706 | No source names the rule set, the parameter codes or the signal that announce a plan state change, and none states who consumes the plan consequence once rwb-treatment owns it | Solution architect with the rule owner of rwb-decision and the parameters owner of rwb-case | Resolved (directive) |
| GAP-2835 | The litigation-side checked-field read, the fact columns it fills on legal_action and hearing, the source stamps and the unmapped field codes are not specified | Tech lead of rwb-litigation with the P5 owner of the checked-field contract and the rwb-litigation data owner | Resolved (directive) |
| GAP-2836 | No source says how an extracted hearing_date becomes a hearing row, which hearing_type that row carries, or what the apply does to an action in a closed status | Litigation business analyst with the rwb-litigation data owner and the S4 hearing story owner | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3183 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 result file with it | Integration lead with the communications lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3188 | The payment match rule load is a P4 reference load in the story and a P7 rule package in the target | Decision and rules lead with the access lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P7-E2024-APP | Not specified without item ID | 508 | No screen is built in this story. The empty, loading, error and no access states of SCR-11 are not written here and are Not specified in the source documents (D |
