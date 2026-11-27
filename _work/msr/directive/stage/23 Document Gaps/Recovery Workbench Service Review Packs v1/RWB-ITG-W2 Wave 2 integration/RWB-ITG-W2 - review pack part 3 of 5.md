# RWB-ITG-W2 Wave 2 integration - review pack, part 3 of 5 (RWB-ITG-E2017-ITG to RWB-ITG-E2026-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 147 |
| Cross-document (pending in another document) | 160 |
| Not applied (value not in the sources) | 19 |
| Open business decisions | 27 |
| Register gaps linked | 146 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E2017-ITG | 20 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2017 ITG Contract, CA and mortgage document generation screens - integration v2.md |
| RWB-ITG-E2018-ITG | 13 | 24 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2018 ITG E-signature flow for customers and the bank - integration v2.md |
| RWB-ITG-E2019-ITG | 13 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2019 ITG Partner identities through the external gateway - integration v2.md |
| RWB-ITG-E2021-ITG | 18 | 31 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2021 ITG Letter dispatch loop with proof of delivery from WIN - integration v2.md |
| RWB-ITG-E2022-ITG | 20 | 21 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2022 ITG SMS and LINE dispatch through NSS and LINE OA - integration v2.md |
| RWB-ITG-E2024-ITG | 16 | 15 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2024 ITG Field app photos and bills into the document hub - integration v2.md |
| RWB-ITG-E2025-ITG | 26 | 16 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2025 ITG Extraction for the stage 2 and 3 document types - integration v2.md |
| RWB-ITG-E2026-ITG | 21 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2026 ITG Document generation engine for contract, CA and mortgage templates - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E1034-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22081 | GAP-1598 | Register gap | Product owner with the solution architect | Two of the module's business requirements describe the case record view and the case timeline, which the case service owns | Read both requirements as this service's contribution to the case record view: the notice and message block with its states, and the ordered notice and message history. The view, the timeline and the timer projection stay with rwb-case; the ledger entries stay with rwb-source-data. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22514 | GAP-0943 | Register gap | Compliance and PDPA officer | rwb-access document set: the masking version in force for SIT and the field IDs of the personal fields on the review view are not specified | Fix the mask version label per environment in the policy pack load, publish the field IDs of a generated contract and its parties with the LDM, and have the pack owner confirm the DF-PTY-007 and DF-PTY-016 rows before SIT. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22516 | GAP-1582 | Register gap | Legal counsel | E-discovery and court-ready evidence have no FSD feature, no operation and no response target | FR-P5-028, FR-P5-029 and AC-P5-021 carry the behaviour with the response target left open as OQ-P5-09. A discovery operation and its response target are needed before wave 2 acceptance. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
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
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E2018-ITG | R-03774 | DOR-RWB-ITG-E2018-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value is given in the story or item. The header Size row reads Not specified in the source documents. |
| RWB-ITG-E2018-ITG | R-03776 | DOR-RWB-ITG-E2018-ITG-22 | 13 | Definition of Ready item 22 Fake published: Fail | No published fake library version in 22 Microservice Realignment (grep fake library/package/pack + version) or E2018 story files; would need an invented version. |
| RWB-ITG-E2018-ITG | R-03777 | DOR-RWB-ITG-E2018-ITG-23 | 12.2 | Definition of Ready item 23 Contract version fixed: Fail | Only the /v1 major version is given. The exact OpenAPI version is marked Not specified in section 12.2. |
| RWB-ITG-E2018-ITG | R-22526 | GAP-0402 | 13 | The e-signature harness pack and the EasyApp test route are not specified | EasyApp test tenant, route, fixture, harness hosts, seeding, evidence not in sources; Epic 2 v8 story lists them Not specified (GAP-0402; ASM-0577). Needs ACE/QA agreement. |
| RWB-ITG-E2019-ITG | R-03780 | DOR-RWB-ITG-E2019-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the sources. The header row records it as not specified, and the item stays open until the story is sized. |
| RWB-ITG-E2021-ITG | R-03785 | DOR-RWB-ITG-E2021-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed RWB-ITG-W2 epic design in 22 Microservice Realignment (only checks/reports list missing files). dorcheck.py says item 14 is a record not held. Sign-off can't be invented. |
| RWB-ITG-E2021-ITG | R-03788 | DOR-RWB-ITG-E2021-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published fake library version in 22 Microservice Realignment. dorcheck.py line 426 only flags the missing record. A version can't be invented. |
| RWB-ITG-E2021-ITG | R-22561 | GAP-0404 |  | The WIN dispatch harness pack and the proof-file test window are not specified | Harness pack, window control, fixtures, seeding and evidence format are in no source: searched PRDs, test/interface .md, 22 Microservice Realignment. Needs ACE integration and QA agreement. |
| RWB-ITG-E2022-ITG | R-03793 | DOR-RWB-ITG-E2022-ITG-16 | header | Definition of Ready item 16 Size: Fail | Size row added as Not specified in the source documents; no size value exists, so the item stays open. |
| RWB-ITG-E2022-ITG | R-14321 | DOR-RWB-ITG-E2022-ITG-9 | 14 | Definition of Ready item 9 Messages: Partial | Message text and trigger for MSG-P4-002 are not in the sources; row records Not specified and the item stays open. |
| RWB-ITG-E2022-ITG | R-22553 | GAP-1610 | header | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | Package ID is not in the sources and is recorded as Not specified; the gap stays open until an ID exists. |
| RWB-ITG-E2024-ITG | R-03798 | DOR-RWB-ITG-E2024-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed RWB-ITG-W2 epic design found in 22 Microservice Realignment .md files; recording a sign-off would invent it. |
| RWB-ITG-E2024-ITG | R-03799 | DOR-RWB-ITG-E2024-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the sources. The header carries the placeholder; the squad sizes at refinement. |
| RWB-ITG-E2024-ITG | R-03801 | DOR-RWB-ITG-E2024-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published fake library version found in 22 Microservice Realignment .md files or RWB-P5-E2024-CON; a version would be invented. |
| RWB-ITG-E2024-ITG | R-14324 | DOR-RWB-ITG-E2024-ITG-17 | header | Definition of Ready item 17 Dependencies: Partial | Build dependency stays None, as sections 3 and 13 state. The four APP stories remain Integration dependencies; RWB-P5-E2024-CON is the contract dependency. |
| RWB-ITG-E2024-ITG | R-22593 | GAP-0406 |  | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | Harness, fixture, evidence and gate values are not in the Gap Register line 415 or the story; they need agreement with the P5 owner and QA. |
| RWB-ITG-E2024-ITG | R-22598 | GAP-1284 | 12.2, 12.8 | No source settles whether an item the store refuses leaves a DOCATT entry | No source settles whether a refused item leaves a DOCATT entry. Sections 12.2 and 12.8 now mark the refused-item entry as Not specified in the source documents (GAP-1284). |
| RWB-ITG-E2025-ITG | R-03807 | DOR-RWB-ITG-E2025-ITG-22 | 12.9 | Definition of Ready item 22 Fake published: Fail | No published fake version in sources; story v2 L324 already records fake versions as not specified (GAP-0407; ASM-0582). |
| RWB-ITG-E2025-ITG | R-22614 | GAP-1898 | 13 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | H and C rows are recorded in section 13 as DP-added but are not yet in the build and contract lists; due at the next story version. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01391 | RWB-ITG-E2017-ITG | DOR-RWB-ITG-E2017-ITG-12 | 16, 18 | Add to Test cases: REQ-DCM-012 TC-E2-017-01-ITG to -12-ITG, -14-ITG, -15-ITG; REQ-OCC-002 TC-E2-017-01-ITG, -13-ITG; REQ-OCC-009 TC-E2-017-03-ITG, -12-ITG. |
| CDC-01398 | RWB-ITG-E2017-ITG | CG-ALL-676 | 18 | Add to Test cases: REQ-DCM-012 TC-E2-017-01-ITG to -12-ITG, -14-ITG, -15-ITG; REQ-OCC-002 TC-E2-017-01-ITG, -13-ITG; REQ-OCC-009 TC-E2-017-03-ITG, -12-ITG. |
| CDC-01405 | RWB-ITG-E2018-ITG | DOR-RWB-ITG-E2018-ITG-12 | section 18 | Section 16 holds the story's test cases, now including TC-E2-018-13-ITG; the mismatch sits in RTM v7, which is outside this story. |
| CDC-01419 | RWB-ITG-E2018-ITG | CG-ALL-682 | 18 | Align REQ-OCC-009 test list with section 18 of RWB-ITG-E2018-ITG (TC-E2-018-01 and TC-E2-018-12 in the story) at the next RTM version. |
| CDC-01430 | RWB-ITG-E2019-ITG | DOR-RWB-ITG-E2019-ITG-12 | 16, 18 | Align the REQ-ACA-012 test list with story section 18: TC-E2-019-01-ITG to TC-E2-019-14-ITG, with 06 and 09 run by the app stories. |
| CDC-01439 | RWB-ITG-E2019-ITG | CG-ALL-689 | 18 | Align the REQ-ACA-012 test list in the RTM with section 18 (TC-E2-019-01-ITG to TC-E2-019-12-ITG) in the next RTM version; RTM v7 currently lists TC-E2-019-01, TC-E2-019-05 and TC-E2-019-09. |
| CDC-01476 | RWB-ITG-E2022-ITG | DOR-RWB-ITG-E2022-ITG-12 | 16, 18 | List this story's -ITG cases per requirement (REQ-OCC-004, 005, 006, REQ-ILG-010, REQ-DRI-006); RTM lists legacy-wide cases, and none of E2-022 for REQ-DRI-006. |
| CDC-01489 | RWB-ITG-E2022-ITG | CG-ALL-699 | 18 | Section 18 test lists were updated in the story; remaining differences from RTM v7 need the matrix to be reissued. |
| CDC-01507 | RWB-ITG-E2024-ITG | CG-ALL-707 | 18 | In its next version, align the REQ-DCM-013 test list with the test cases in section 18 of RWB-ITG-E2024-ITG (the -ITG test IDs). |
| CDC-01510 | RWB-ITG-E2025-ITG | DOR-RWB-ITG-E2025-ITG-12 | 18 | Trace REQ-DCM-006 to TC-E2-025-01-ITG, -02-ITG, -04-ITG to -12-ITG, and REQ-DCM-005 to TC-E2-025-03-ITG, -05-ITG, -06-ITG, -09-ITG, as story section 18 lists. |
| CDC-01522 | RWB-ITG-E2025-ITG | CG-ALL-711 | 18 | Align the REQ-DCM-006 and REQ-DCM-005 trace rows with section 18 of RWB-ITG-E2025-ITG in the next RTM version. |
| CDC-01539 | RWB-ITG-E2026-ITG | CG-ALL-716 | 18 | RTM v7 is to be aligned at its next version. Section 18 was edited only under R-14337, to list explicit test IDs. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01412 | RWB-ITG-E2018-ITG | GAP-1188 |  | Contract for the expiry cancel is missing in the target catalogue. No story edit made for this item. |
| CDC-01417 | RWB-ITG-E2018-ITG | GAP-2700 |  | Publish the signature record on the update operation of /api/recovery/treatment/v1 with a fake; record that a later Temporal move changes the client only. |
| CDC-01420 | RWB-ITG-E2018-ITG | GAP-1704 | find it | Name rwb-document and rwb-comms as the Workbench document hub owners on slides 13, 16, 17 and 41, or align FSD S2 A2.18.2 and A2.15.2 to the P5 and P6 contracts. |
| CDC-01422 | RWB-ITG-E2018-ITG | GAP-1185 | find it | Publish no comms signature event; if a signature fact must travel, S2 rwb-treatment publishes it on rwb.treatment.events.v1 in a later catalogue revision. |
| CDC-01423 | RWB-ITG-E2018-ITG | GAP-2355 | find it | Confirm with rwb-reporting whether a signature fact is needed on the rwb-document topic; if yes, allocate a new DP-09 story with a CloudEvents payload of IDs and facts only. |
| CDC-01446 | RWB-ITG-E2021-ITG | GAP-1597 |  | Confirm rwb-comms keeps the notice and its proof of delivery fields, rwb-source-data contract supplies proof rows, this service applies proof by barcode; ACE team to confirm which system writes v_ace_pod. |
| CDC-01448 | RWB-ITG-E2021-ITG | GAP-2096 |  | Add EV-15 NoticeDelivered published by rwb-comms, with a proof-arrival consumer row; read proof through the P1 contract on the ACE batch business date and match by barcode. |
| CDC-01449 | RWB-ITG-E2021-ITG | GAP-2093 |  | Remove approval from rwb-comms OUT list; hold approval in P7 ApprovalWorkflow as a child of NoticeDispatchWorkflow; S4 POST /notices/{noticeId}/approve is the litigation decision point; notice waits in Approved. |
| CDC-01464 | RWB-ITG-E2021-ITG | GAP-2095 |  | Record partner instruction as S9 InstructionWorkflow and internal alert as a P3 task; rwb-comms keeps only the partner instruction template. |
| CDC-01516 | RWB-ITG-E2025-ITG | GAP-1877 | 12.2 | Section 12.2 reads checked fields as one REST hop; the Temporal column belongs to Architecture v5. |
| CDC-01518 | RWB-ITG-E2025-ITG | GAP-2703 | 12.2 | Section 12.2 reads checked fields as one REST hop; the Temporal wording belongs to Architecture v5. |
| CDC-01536 | RWB-ITG-E2026-ITG | GAP-1289 | 13 | Adopt producer-side write inside the generation transaction with atomic idempotent ledger append; keep MSG-P7-003 as refusal; decide strict mode at architecture review, adding ledger acknowledgement as its own change if needed. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01386 | RWB-ITG-E2017-ITG | CG-ALL-673 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or move the consumer to a published operation; provider ruling needed. |
| CDC-01389 | RWB-ITG-E2017-ITG | DOR-RWB-ITG-E2017-ITG-8 | find it | Publish POST /api/recovery/access/v1/authorise (CG-ALL-673). The event type part is fixed in the story (CG-ALL-674). |
| CDC-01401 | RWB-ITG-E2018-ITG | CG-ALL-680 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer switches to a published operation. Provider ruling needed. |
| CDC-01403 | RWB-ITG-E2018-ITG | DOR-RWB-ITG-E2018-ITG-21 | header | The rwb-access operation is not published yet. It is tracked under CG-ALL-680 and needs the provider's CON story. No story edit is made. |
| CDC-01404 | RWB-ITG-E2018-ITG | DOR-RWB-ITG-E2018-ITG-8 | find it | Publish POST /api/recovery/access/v1/authorise (see CG-ALL-680). Event type fixed in the story under CG-ALL-681. |
| CDC-01442 | RWB-ITG-E2021-ITG | CG-ALL-691 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. Story row in 12.2 unchanged. |
| CDC-01443 | RWB-ITG-E2021-ITG | DOR-RWB-ITG-E2021-ITG-21 | header | Contract dependencies name the rwb-access authorise operation, and its contract story key is not specified. Publication belongs to the provider yaml (CG-ALL-691). |
| CDC-01444 | RWB-ITG-E2021-ITG | DOR-RWB-ITG-E2021-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01387 | RWB-ITG-E2017-ITG | DOR-RWB-ITG-E2017-ITG-14 |  | Record the epic design sign-off for RWB-ITG-W2: the approving role and the sign-off date, as given by the epic owner |
| CDC-01402 | RWB-ITG-E2018-ITG | DOR-RWB-ITG-E2018-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-W2 in the epic design record. |
| CDC-01425 | RWB-ITG-E2019-ITG | DOR-RWB-ITG-E2019-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-E2019-ITG. Story row added as not specified. |
| CDC-01473 | RWB-ITG-E2022-ITG | DOR-RWB-ITG-E2022-ITG-14 |  | Record the RWB-ITG-W2 epic design sign-off by the Business lead (ways of working v3): approving role and sign-off date |
| CDC-01509 | RWB-ITG-E2025-ITG | DOR-RWB-ITG-E2025-ITG-14 | header | Record the signed epic design sign-off; no sign-off reference exists in the story or source documents. |
| CDC-01525 | RWB-ITG-E2026-ITG | DOR-RWB-ITG-E2026-ITG-14 | find it | Record the signed epic design sign-off for this story. |

### API:(service not named) (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01414 | RWB-ITG-E2018-ITG | GAP-2352 |  | Add the five signature-request operations with API IDs and paths on /api/recovery/document/v1; settle query names for list and external-reference read with rwb-comms. |
| CDC-01428 | RWB-ITG-E2019-ITG | DOR-RWB-ITG-E2019-ITG-23 | header | Header row records the contract version as not specified; paths carry /v1. POST /partner-identities/resolve was not found in rwb-access.yaml and needs adding. |
| CDC-01431 | RWB-ITG-E2019-ITG | GAP-0785 | header | Register POST /partner-identities/resolve on /api/recovery/access/v1 and its two schemas; agree the refusal-to-status table with the gateway owner and message catalogue. Story header now states the path and that no event is published or consumed. |
| CDC-01462 | RWB-ITG-E2021-ITG | GAP-2094 |  | Keep the case-level notice list as a P6 operation and settle its path; until then read notices per GET /notices/{noticeId}. |
| CDC-01538 | RWB-ITG-E2026-ITG | GAP-2393 | none | Add a table in rwb_comms for the idempotency key and request lock via the V-baseline migration; record the rwb-document create operation from RWB-P5-E2026-CON in the P6 API specification. |
| CDC-01542 | RWB-ITG-E2026-ITG | GAP-2394 | none | Allocate the next API-P6-nnn ID at D1 (Not specified in the source documents (GAP-2394)) and add the generated-documents operation to the P6 API specification with the gateway-bff route. |

### RWB-P5-E2017-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01388 | RWB-ITG-E2017-ITG | DOR-RWB-ITG-E2017-ITG-22 |  | Record the published contract fake library version and its publication record for the ten planned fakes and baseline tag |
| CDC-01407 | RWB-ITG-E2018-ITG | GAP-1182 | 12.2, 12.8 | Publish create, read-by-external-reference and update operations for signature_request before the wave 2 exit. |
| CDC-01410 | RWB-ITG-E2018-ITG | GAP-1186 | find it | Publish whether the signature version add takes the signed PDF bytes in the body or returns an upload link, for rwb-comms to stream to. |
| CDC-01501 | RWB-ITG-E2024-ITG | GAP-1182 | find it | Publish create, read-by-external-reference and update operations for signature_request before wave 2 exit. |

### RWB-P6-E2021-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01452 | RWB-ITG-E2021-ITG | GAP-1089 |  | Fix the WIN dispatch file name, record layout, acknowledgement field list, INT-15 proof result record and owning operation in the baseline review, with the WIN owner and rwb-integration owner. |
| CDC-01456 | RWB-ITG-E2021-ITG | GAP-1095 |  | Publish the handoff row: the Airflow window signals the rwb-comms Schedule with the business date, the run records that date, and a rerun of the same date writes no second file. |
| CDC-01461 | RWB-ITG-E2021-ITG | GAP-1092 |  | Declare capability area and right per operation; gateway-bff asks rwb-access (DP-08) before the call; serve scope from the rwb-case case read or add C RWB-P4-E1037-CON. |
| CDC-01465 | RWB-ITG-E2021-ITG | GAP-1094 |  | Fix the Notice component with nine legacy fields plus holdReason, dispatchFileId and dispatchAttempts; all optional except id and caseId. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01455 | RWB-ITG-E2021-ITG | GAP-0946 |  | Add the authorise path with its request and answer schema to the API specification and TSD P4 appendix T-A; stub it in the contract fake; add the access entry decision codes to the ledger code list. |
| CDC-01478 | RWB-ITG-E2022-ITG | GAP-2321 | find it | Confirm the authorise element at contract review; set the masking version label, covered field IDs, AC-READ granularity, parameter rows and defaults at wave-2 policy load and build. |
| CDC-01504 | RWB-ITG-E2024-ITG | GAP-0952 |  | Publish the authorise, me-permissions and masking-policies request and answer shapes, and state whether a sync is authorised once per manifest or once per item and how the field list is carried. |
| CDC-01532 | RWB-ITG-E2026-ITG | GAP-0938 | header | Add the authorise request and answer schema to TSD P4 appendix T-A and publish it with RWB-P4-E1037-CON; stub generation facts in RWB-P5-E2026-CON. |

### RWB-P6-E2022-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01474 | RWB-ITG-E2022-ITG | DOR-RWB-ITG-E2022-ITG-21 | header | Contract dependencies names RWB-P6-E2022-CON |
| CDC-01475 | RWB-ITG-E2022-ITG | DOR-RWB-ITG-E2022-ITG-22 | find it | Published fake library version is not recorded in the source documents; belongs to the contract story. |
| CDC-01491 | RWB-ITG-E2022-ITG | GAP-1073 | find it | Fix the MessageRequest and Interaction property names and closed value lists from the legacy and TSD; lengths, formats and optionality stay Not specified in the source documents until baseline review. |
| CDC-01492 | RWB-ITG-E2022-ITG | GAP-1076 | find it | Hold the message delivery status as its own list (SENT, DELIVERED, FAILED, READ) and leave LOV-DELIVERY to the notice and proof-of-delivery capability. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01494 | RWB-ITG-E2024-ITG | CG-ALL-703 | 2, 3, 7 | Add field bill_amount for document type UTILITY_BILL, or name the dictionary field the story should use in place of bill_amount. |
| CDC-01495 | RWB-ITG-E2024-ITG | CG-ALL-704 | 2, 3, 7 | Add field due_date for document type UTILITY_BILL, or name the dictionary field the story should use in place of due_date. |
| CDC-01496 | RWB-ITG-E2024-ITG | CG-ALL-705 | 3 | Add field account_ref for document type UTILITY_BILL, or name the dictionary field the story should use in place of account_ref. |
| CDC-01499 | RWB-ITG-E2024-ITG | DOR-RWB-ITG-E2024-ITG-7 | 11 | Add bill_amount, due_date and account_ref as fields in LDM v9 and Data Classification v5. |

### RWB-S4-E2025-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01519 | RWB-ITG-E2025-ITG | GAP-2835 | 11 | Carry the litigation checked-field read per RWB-P5-E2025-CON, the legal_action source stamps and apply key, same-name mapping only, and the twelve unmapped codes counted in the apply result. |
| CDC-01520 | RWB-ITG-E2025-ITG | GAP-2836 | 11 | One hearing per action and hearing_date: new row with hearing_type empty and is_active true, else next_date only; CLOSED or WITHDRAWN action takes no fact and answers 409. |
| CDC-01521 | RWB-ITG-E2025-ITG | GAP-1903 | 12 | Fill trigger is the request document type on create and patch; derived write key; one hearing per action and date; P3-E1042/E1043-CON calls; route fields and merge order from RWB-PLT-N001-CON. |
| CDC-01524 | RWB-ITG-E2025-ITG | GAP-1899 | 13 | The no-producer, no-consumer slice does not match this harness, which consumes three events. DP09 and DP10 are kept here. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01390 | RWB-ITG-E2017-ITG | DOR-RWB-ITG-E2017-ITG-1 | 1 | Define a role code and name for the integration and QA team, or confirm an existing role code to use in section 1. |
| CDC-01424 | RWB-ITG-E2018-ITG | GAP-2357 | find it | Confirm Documents C, R and U as operation-level rights of the five signature-request operations; add the rwb-document closed-request message at the next message standard version. |
| CDC-01527 | RWB-ITG-E2026-ITG | DOR-RWB-ITG-E2026-ITG-1 | 1 | Add a role code or name for member of the integration and QA team, or confirm which existing role section 1 should use. |

### OTHER:FSD P5 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01394 | RWB-ITG-E2017-ITG | GAP-1580 | none | Add a generation section for REQ-DCM-012 with its functional statements in the next version. |
| CDC-01531 | RWB-ITG-E2026-ITG | GAP-1580 | header | Add a generation section for REQ-DCM-012 in the next FSD P5 version, stating the behaviour of FR-P5-026 and AC-P5-019. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01397 | RWB-ITG-E2017-ITG | GAP-0401 | 7 | Publish the gateway-bff composite route path for the SCR-14 and SCR-30 document set and its merge order across rwb-treatment, rwb-document, rwb-comms and rwb-access; agree harness pack, seeding and evidence format with QA. |
| CDC-01508 | RWB-ITG-E2024-ITG | GAP-0951 |  | State the field app route: capture sync as a composed call beside the rwb-document call, and the SCR-30 panel as a parallel read, through the gateway-bff composite route. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01409 | RWB-ITG-E2018-ITG | GAP-2356 | find it | Add configuration keys under rwb.document.esign for write-once container, WORM tier, object size limit and transfer path, settled with RWB-P5-E1024-APP and the infrastructure story. |
| CDC-01471 | RWB-ITG-E2021-ITG | GAP-2219 | 13 | Allocate a key for the rwb-case slice flag (hold switch, ledger facts, task) at first build, enabled via the platform flag mechanism with the P6 dispatch-loop flag. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01434 | RWB-ITG-E2019-ITG | GAP-1852 | n/a | Confirm P4 keeps the internal role model and S9 holds the partner_user binding that scopes a partner user to one firm and one partner role. |
| CDC-01447 | RWB-ITG-E2021-ITG | GAP-2090 |  | Record barcode, callback date and delivery status on the notice row; add a separate proof table only if a DB story needs it. |

### OTHER:Interface Specifications v4 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01445 | RWB-ITG-E2021-ITG | GAP-1602 |  | Add a versioned INT-14 WIN dispatch file definition owned by rwb-integration: record set, field list, field order, envelope, naming, encoding, and barcode and sent date return. |
| CDC-01450 | RWB-ITG-E2021-ITG | GAP-0437 |  | Publish the proof-record operation on RWB-S4-E5002-CON and the notice proof write on the rwb-comms baseline; add notice lifecycle state and case notice facts to the LDM; fix LOV-DELIVERY mapping and notice period and proof window as versioned reference rows. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01453 | RWB-ITG-E2021-ITG | GAP-0945 |  | Extend the TSD P4 T6.1 RBAC matrix with a Litigation column for each role the legacy authority table names; publish the full 14-area matrix as data; confirm the C and R letters with the matrix owner. |
| CDC-01454 | RWB-ITG-E2021-ITG | GAP-0948 |  | Name the JOB-10 runner service identity in the role table with role class NON_HUMAN_ACTOR, scope ALL and a Litigation R row. Role code: Not specified in the source documents (GAP-0948). |

### RWB-P1-E1066-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01463 | RWB-ITG-E2021-ITG | GAP-2182 |  | Settle one path family for the interaction ledger, keep the case-scoped form, and realign the fake in RWB-P6-E2021-CON and the consumed row in RWB-P3-E2021-APP. |
| CDC-01479 | RWB-ITG-E2022-ITG | GAP-1070 | find it | Name the contact-point read, consent and verified fields, failed-count update, and ledger record and delivery-update operations, or add a P1 ledger contract to Contract dependencies. |

### RWB-P5-E2026-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01537 | RWB-ITG-E2026-ITG | GAP-1878 | none | Take generation operation and shapes from RWB-P5-E2026-CON; add two nullable treatment columns (document reference, pinned template version) and index; event name and code stay as story design until catalogue owner confirms. |
| CDC-01541 | RWB-ITG-E2026-ITG | GAP-1024 | none | Declare POST /cases/{caseId}/generated-documents; publish four provider interfaces and decision record as typed contracts; declare one event with five payload fields; record S2, P1 and P7 reads as consumed and faked. |

### OTHER:TSD P4 (T6.1 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01392 | RWB-ITG-E2017-ITG | GAP-0942 | none | Add Documents column: RW-RESTRUCT CRU, RW-CASEOWN CRU, RW-TEAMMGR R, RW-LEGAL CRUA; confirm with matrix owner; publish in PM-2026.12 pack via RWB-P4-AD002-APP. |

### OTHER:Service contract (integration service) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01393 | RWB-ITG-E2017-ITG | GAP-1713 | none | Record the mapping of each FEAT prerequisite to its owning service contract: approval P7, case P3, documents P5, communications P6, valuation S1. |

### OTHER:TSD P6 v2; RWB-P6-E1046-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01395 | RWB-ITG-E2017-ITG | GAP-2392 | none | Add treatment-type and product-group filters to API-P6-003; add application/json to API-P6-005 (additive, v1); add locked attribute to merge_field; publish set rows as rwb-case reference data; copy five messages when issued. |

### API:(service not named); OTHER:TSD P4 (appendix T-A; OTHER:T3.1; OTHER:T6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01396 | RWB-ITG-E2017-ITG | GAP-0941 | 7 | Publish POST /authorise with request and answer schema in appendix T-A and the API specification; state the service identity scope rule in T6.2; stub it on RWB-P4-E1037-CON. |

### OTHER:generation-screens baseline (GAP-1017 document) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01399 | RWB-ITG-E2017-ITG | GAP-1017 |  | Declare seven operations on /api/recovery/document/v1; map regenerate to API-P5-017; consume API-P6-009 for signature; fix field names; one error envelope and status map; record decision record. |

### OTHER:rwb-access document set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01400 | RWB-ITG-E2017-ITG | GAP-0944 |  | Publish the composite route field list for SCR-14 and SCR-30 with contract RWB-PLT-N001-CON; add the allowed-action decision code to the ledger decision-code list. |

### OTHER:split_plan.json (owning-service CON stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01406 | RWB-ITG-E2018-ITG | GAP-1713 | find it | Feature-code prerequisites need mapping to owning-service contracts. No CON story for this key exists in the plan. |

### OTHER:rwb-treatment contract (S2 wave 2 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01408 | RWB-ITG-E2018-ITG | GAP-1183 | header | Publish the rwb-treatment contract on /api/recovery/treatment/v1 with the PATCH on a treatment, and the S2 signature record operation with its field names. |

### OTHER:TSD P6 v2 T5.1 (integration inventory) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01411 | RWB-ITG-E2018-ITG | GAP-1187 | find it | Add INT-34 to the integration inventory and publish its request and result shape, endpoint and certificate issuer from the ACE common module owner. |

### OTHER:FSD P5 Document hub v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01413 | RWB-ITG-E2018-ITG | GAP-1589 |  | Add a signature requirement and criteria recording the signature request as a document event and metadata row; carry the missing text as OQ-P5-13. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01415 | RWB-ITG-E2018-ITG | GAP-2353 |  | Add the signature_request table with columns, constraints and indexes to TSD P5 T3.1 and rwb_document.sql; remove it from TSD P6 T3.1 at its next version. |

### OTHER:TSD S2 Treatment v2 T3.1; OTHER:T-A.1 and FSD S2 A2.7 to A2.9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01416 | RWB-ITG-E2018-ITG | GAP-2699 |  | Add five nullable signature columns and two indexes on the service Flyway sequence; declare the update operation with signature properties; name two outcome events; add one closure callback from the offer-validity timer. |

### RWB-P6-E2018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01418 | RWB-ITG-E2018-ITG | GAP-1196 |  | Add DP-03 and H RWB-PLT-E1027-CON to the slice, or confirm the platform release train delivers the local decision-record library. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01421 | RWB-ITG-E2018-ITG | GAP-1184 | find it | Record RWB-P6-E2018-CON for the three P6 signature-request operations, or confirm section 12.1 of the story as the contract baseline until it exists. |

### RWB-ITG-E2019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01426 | RWB-ITG-E2019-ITG | DOR-RWB-ITG-E2019-ITG-21 | header | Create the contract story and publish the contract, then add it as a contract dependency of this story. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01427 | RWB-ITG-E2019-ITG | DOR-RWB-ITG-E2019-ITG-22 | header | Publish the contract fake library version this story builds against. Story row added as not specified. |

### OTHER:split_plan.json (wave plan for RWB-E2-019 and RWB-E2-034) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01429 | RWB-ITG-E2019-ITG | GAP-1844 | header | Keep RWB-S9-E2019-APP partner identity slice in wave 2 with partner_user binding and FAPI 2.0 route published before panel work; move service creation from wave 4 accordingly. |

### OTHER:TSD P7 v2 rwb-decision contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01432 | RWB-ITG-E2019-ITG | GAP-1272 | n/a | Fix the partner access record path, the two read query parameters, the entry composition, the result vocabulary, the page-size bound parameter and the index names. |

### OTHER:Recovery Workbench backlog split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01433 | RWB-ITG-E2019-ITG | GAP-1573 | n/a | Create the Epic 2 story for REQ-ACA-011 in the P4 epic with the group-change scenario, session re-resolution, reallocation hand-off to rwb-case and leaver response time; answer DL38 and DL40. |

### OTHER:TSD S9 (RWB-S9 technical specification; OTHER:T-A.1; OTHER:T-A.2; OTHER:T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01435 | RWB-ITG-E2019-ITG | GAP-3148 | n/a | Load path, message ids, partner_user catalogue and refresh parameter belong in TSD S9. Story text needs no change. |

### RWB-P4-E2019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01436 | RWB-ITG-E2019-ITG | GAP-3181 | n/a | Table ownership moves to S9 per the ownership ruling. The P4 build notes step is outside this story. |

### OTHER:TSD P4 v3 (appendix T-A; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01437 | RWB-ITG-E2019-ITG | GAP-0784 | n/a | Story reads these values at run time, so the build is not blocked. Source documents need the registration and definitions. |

### OTHER:Security design decision record; OTHER:Service Catalog and gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01438 | RWB-ITG-E2019-ITG | GAP-1395 | n/a | Gateway and security design values are outside this story. Record them in the security design decision and runbook. |

### OTHER:TSD P4 v3 (T3.1; OTHER:T3.3); OTHER:TSD P3; OTHER:rwb-access contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01440 | RWB-ITG-E2019-ITG | GAP-1567 | n/a | Ownership sits with rwb-case and rwb-partner. The P4 specification and the rwb-access contract must change, not this story. |

### RWB-PLT-N007-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01441 | RWB-ITG-E2019-ITG | GAP-0786 | n/a | Infrastructure values are configuration and are set at the security design authority review. Build is not blocked. |

### RWB-P1-E1016-CON; RWB-P1-E1066-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01451 | RWB-ITG-E2021-ITG | GAP-2181 |  | Publish the DP02 contact-and-consent row and its GIVEN/WITHDRAWN/UNKNOWN vocabulary with the resolution rule; add the LETTER append required-members table; add UNSERVED to LOV-SEND-STATUS with version, or confirm the FAILED mapping against the ACE result code. |

### OTHER:SERVICE_LEVEL reference data (timer table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01457 | RWB-ITG-E2021-ITG | GAP-2218 |  | Load the NOTICE_UNSERVED task row with case owner role and due date before the wave starts. Task code NOTICE_UNSERVED is taken from the legacy story. |

### OTHER:Published rwb-source-data and rwb-decision contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01458 | RWB-ITG-E2021-ITG | GAP-2220 |  | Publish operation names and paths under the REST bases /api/recovery/source-data/v1 and /api/recovery/decision/v1, with their contract fakes. |

### OTHER:TSD P3 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01459 | RWB-ITG-E2021-ITG | GAP-2221 |  | Remove the interaction row from the P3 data model or mark it owned by rwb-source-data. rwb-case holds no interaction table, view or foreign key. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01460 | RWB-ITG-E2021-ITG | GAP-3183 |  | Name the delivery result event and its topic; delete the JOB-09 loader from the Epic 2 story set. |

### RWB-P6-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01466 | RWB-ITG-E2021-ITG | GAP-1096 | 14 | Publish the MSG-P6-005 template-approval text and the MSG-P3-005 in-progress text, then copy both unchanged into section 14 of this story. |

### OTHER:Recovery Workbench data dictionary and policy pack load (FSD P4 v3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01467 | RWB-ITG-E2021-ITG | GAP-0947 | 7 | Fix masking version in force in SIT (MASK-SIT-01 assumed); publish postal address and party field IDs with mask format; publish gateway-bff route field list for SCR-18 and SCR-04. |

### OTHER:rwb-source-data reconciliation story (JOB-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01468 | RWB-ITG-E2021-ITG | GAP-1090 | 7 | Assign REC-05 to the rwb-source-data reconciliation story with notice break count and series; define its owner, frequency and break definition there. |

### RWB-P6-E2021-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01469 | RWB-ITG-E2021-ITG | GAP-1093 | 9 | Set deployment slot and replica counts once DL35 is decided; confirm the six alert thresholds at UAT and record them in each linked runbook entry. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:JOB-10) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01470 | RWB-ITG-E2021-ITG | GAP-2106 | 7 | Single accountable owner split set by directive. The job map is outside this story and still needs the change. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01472 | RWB-ITG-E2021-ITG | GAP-1277 | 13 | Add six platform H rows (RWB-PLT-E1027, E1043, TE006, E1071, E1044, N001 CON), C RWB-P3-E1043-CON and two service baselines; keep Ready to start Day 1; fix metadata next version. |

### RWB-P1-E1066-APP; RWB-P1-E2022-APP; RWB-P4-E2022-APP; RWB-P6-E2022-APP; RWB-P7-E2022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01477 | RWB-ITG-E2022-ITG | DOR-RWB-ITG-E2022-ITG-17 | find it | Complete the five build dependencies before this story starts build. |

### OTHER:TSD P6 T6.1 and gateway-bff route to SCR-03 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01480 | RWB-ITG-E2022-ITG | GAP-1075 | find it | Add a Case record area row to T6.1 and record its reconciliation; declare Case record right C on the gateway-bff composite route answering MSG-P4-002 and MSG-P4-003. |

### OTHER:FSD P6 A2.18 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01481 | RWB-ITG-E2022-ITG | GAP-1605 | find it | Describe consent, verification and failed count as read and written through the rwb-source-data contract for contact_point_ext; enforcement stays in rwb-comms. |

### OTHER:ACE notification team and wave 2 harness pack (QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01482 | RWB-ITG-E2022-ITG | GAP-0405 | find it | Agree NSS and LINE OA test doubles and result-code maps, harness seeding, evidence format and the pass and fail gate for the owned criteria. |

### OTHER:TSD P4 v3 T6.1 role to permission matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01483 | RWB-ITG-E2022-ITG | GAP-0953 | find it | Add the Case record column and the other decided capability areas; load RW-CASEOWN C and RW-TEAMMGR, RW-CONDUCT and RW-COMPLAIN R as PM-2026.12 rows. |

### OTHER:Technical specification document P6 (T5.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01484 | RWB-ITG-E2022-ITG | GAP-1069 | 7 | Publish the ACE notification request and result contract with the NSS and LINE OA result-code maps before the wave 2 SIT entry; until then use the section 12.8 stub of the CON story. |

### OTHER:Technical specification document P6 (T5.1 and T7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01485 | RWB-ITG-E2022-ITG | GAP-1074 | 7 | Publish the NSS and LINE OA endpoint, certificate issuer and secret names; chart carries references only; the egress check fails a release with a missing reference. |

### OTHER:P1 API appendix (interaction ledger, rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01486 | RWB-ITG-E2022-ITG | GAP-1599 | 15 | Hold the message outcome as an interaction ledger entry with delivery status and channel reference; agree the interaction read path with P1 before wave 2; add no fourth rwb_comms table. |

### OTHER:P1 API appendix (rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01487 | RWB-ITG-E2022-ITG | GAP-2183 | 7 | Operation shapes and column types are not in the sources; they must be confirmed at the contract review before closing. |

### RWB-P4-E1037-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01488 | RWB-ITG-E2022-ITG | GAP-0955 | 7 | Publish the authorise, me-permissions and masking-policies shapes in RWB-P4-E1037-CON, and the composite route field list for SCR-03 in RWB-PLT-N001-CON, before the send story is built. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx; OTHER:access log decision-code list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01490 | RWB-ITG-E2022-ITG | GAP-0956 | find it | Record the JOB-11 and other platform service identities with class and scope in the role table; add decision codes for a send and a refused send to the access-log list. |

### OTHER:Functional specification and non-functional requirements (NFR-026) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01493 | RWB-ITG-E2022-ITG | GAP-1600 | 15 | Story keeps the limit of 5 (DL11) and records that NFR-026 states three retries. The solution architect must confirm one number and align the source documents. |

### RWB-P3-E2024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01497 | RWB-ITG-E2024-ITG | DOR-RWB-ITG-E2024-ITG-10 | 12 | Add empty, loading, error and no access states to SCR-30 and SCR-31. |

### RWB-P3-E2024-APP; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01498 | RWB-ITG-E2024-ITG | DOR-RWB-ITG-E2024-ITG-12 | 16, 18 | This story's sections 16 and 18 now list 22 cases; the P3 lists differ from RTM v7. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01500 | RWB-ITG-E2024-ITG | GAP-3194 | find it | Raise an ACE DB story for the column drop in S2, S4, S5, S6, S7, P6 and P8, or attach the drop to the owning APP story; cite the chosen story on row 121 before wave 2. |

### RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01502 | RWB-ITG-E2024-ITG | GAP-2223 | find it | Add stageCode and routeCode to the Case resource; record the authorise request and response shape; name the checklist contract story; load task data rows via the rwb-case administration stories. |

### OTHER:TSD P4 v3; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01503 | RWB-ITG-E2024-ITG | GAP-0949 | 10 | Add a Documents column to the TSD P4 RBAC matrix (T6.1) and carry the five DOCUMENTS rows (RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU, RW-PHONECOL R) in the PM-2026.12 permission file. |

### RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01505 | RWB-ITG-E2024-ITG | GAP-1018 |  | Add an optional capture block (capturedAt, captureLatitude, captureLongitude, clientFileId, captureKind) to the store request as an additive change within major version 1. |

### OTHER:reference-data register of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01506 | RWB-ITG-E2024-ITG | GAP-1283 |  | Record DOCATT as the LOV-DECISION value on every document-attach entry, and keep D6.5 as the routing-decision tag of the legacy story, not the entry code. |

### OTHER:Service contract of the module (Not specified in the source documents (GAP-1713)) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01511 | RWB-ITG-E2025-ITG | GAP-1713 | 13 | Record once the mapping of each feature-code prerequisite (FEAT-APD-01, FEAT-CHO-02, FEAT-CHO-06, FEAT-CHO-07, FEAT-CHO-08 twice, FEAT-DCM-12, FEAT-OCC-01, FEAT-OCC-07, FEAT-OCC-09, FEAT-OCC-11, FEAT-TRT-04, FEAT-VAL-06) to the owning service contract; carry the duplicate FEAT-CHO-08 as written |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01512 | RWB-ITG-E2025-ITG | GAP-3194 |  | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the column drop, or attach the drop to the APP story that creates the table; cite the chosen story on row 121 before wave 2 |

### RWB-P5-E1025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01513 | RWB-ITG-E2025-ITG | GAP-1020 |  | Publish the checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes; apply the DOCTYPE-2026.12 load through the type table; keep EXTRACT_ACCURACY_PASS in document_hub_parameter; confirm with S4 and S2 before wave 2 |

### RWB-P5-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01514 | RWB-ITG-E2025-ITG | GAP-1021 |  | Add C dependency on RWB-P5-E1053-CON for the three extraction operations without re-declaring them; declare one checked-fields read on the service base with its shape and status set; add a C row for the scope filter and version case read; confirm name with S4, S2 and the review queue before baseline tag |

### OTHER:Wave 2 harness pack (QA with P5 and P10 owners) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01515 | RWB-ITG-E2025-ITG | GAP-0407 | 3 | Agree classifier version id for the eleven types, masked sample pack beyond 60 documents, extraction report format, SIT harness environment, DOCTYPE-2026.12 and pass mark seeding, evidence format and retention, pass/fail gate, reader paths. |

### RWB-P5-E2025-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01517 | RWB-ITG-E2025-ITG | GAP-1900 | 12.2 | Section 12.2 consumes the checked-fields operation; its definition belongs to RWB-P5-E2025-CON. |

### OTHER:FSD S2 (A2.18.2; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01523 | RWB-ITG-E2025-ITG | GAP-1704 | none | Name rwb-document and rwb-comms with the P5 and P6 contracts at the document hub integration points; keep no document content in schema rwb_treatment. |

### OTHER:Contract fake library (fakes of section 12.8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01526 | RWB-ITG-E2026-ITG | DOR-RWB-ITG-E2026-ITG-22 | find it | Record the published fake library version for the contract fakes this story uses. |

### OTHER:P3 screen specification; OTHER:SCR-30 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01528 | RWB-ITG-E2026-ITG | DOR-RWB-ITG-E2026-ITG-10 | find it | Add empty, loading, error and no access states to SCR-30. |

### OTHER:TSD P5 (Technical Specification Document P5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01529 | RWB-ITG-E2026-ITG | GAP-1023 | 7 | Add template_code varchar(30) and template_version integer to document; partial unique index on (treatment_id, template_id) where state is DRAFT and is_active. |

### OTHER:Service contracts and FSD S2 prerequisites (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01530 | RWB-ITG-E2026-ITG | GAP-1713 | 8 | The feature-code to service mapping belongs to the service contracts and FSD S2. BR3 keeps its FEAT-OCC-07 trace. |

### OTHER:Test Strategy (generation harness pack) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01533 | RWB-ITG-E2026-ITG | GAP-0408 | 12.8 | Path and GEN_FONT filled from the P5 APP story and Epic 2 v8. Fixtures, PDF/A check tool, seeding, evidence format and retention belong to the harness pack. |

### OTHER:PM-2026.12 policy pack (RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01534 | RWB-ITG-E2026-ITG | GAP-0937 | 5 | Add Documents letters: C for RW-RESTRUCT, RW-CASEOWN and SY-CASEWF; R for RW-TEAMMGR; no row for RW-PHONECOL. |

### OTHER:TSD P4 T6.1 policy pack and reference data load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01535 | RWB-ITG-E2026-ITG | GAP-0939 | none | Add SY-CASEWF role row with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL, recorded in the reference data load with its own approver. |

### OTHER:FSD S2 A2.18; OTHER:A2.15; OTHER:A2.8 and TSD S2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01540 | RWB-ITG-E2026-ITG | GAP-1704 | none | Request generation, review and signature through P5 and P6 contracts; hold document reference on the treatment; keep no document content in schema rwb_treatment. |

### 02 Business architecture and process/Recovery Workbench Role to System Access Matrix v3.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20602 | RWB-ITG-E2026-ITG | R-22617 |  | Matrix has no Documents column. The C/R letters belong to the PM-2026.12 RBAC policy pack row load. Workbook not opened: no shell to run docview.py. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20725 | RWB-ITG-E2021-ITG | R-28797 |  | MASK-SIT-01 already in AC-EXC-P4-004-05. Postal address and party field IDs and gateway-bff route list: Not specified in the source documents (GAP-0947). |

### 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20890 | RWB-ITG-E2021-ITG | R-22555 |  | Proof-record operation (RWB-S4-E5002-CON), notice LDM fields, LOV-DELIVERY and notice reference rows belong to the contract, LDM, LOV and reference data owned outside this workbook (GAP-0437). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0067 | Wave conflict S9 / EP02 | Tech lead | Resolved (directive) |
| GAP-0068 | Wave conflict S4 / EP02 | Tech lead | Resolved (directive) |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0402 | The e-signature harness pack and the EasyApp test route are not specified | Integration lead | Resolved (directive) |
| GAP-0403 | The external partner gateway test route and the partner harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0404 | The WIN dispatch harness pack and the proof-file test window are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0405 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0406 | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | Integration lead | Resolved (directive) |
| GAP-0407 | The extraction harness pack, the classifier version and the cross-service reader pack are not specified | Integration lead | Resolved (directive) |
| GAP-0408 | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0437 | The legacy delivery step is split across rwb-comms, rwb-litigation and rwb-case with no named hand-off operation and no named reference rows, so the end-to-end chain of RWB-E5-002 has no single source of record | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0784 | The partner identity resolution operation, its claim set, its answer schema, the scope type PLACED and the lifetime of an answer are specified by no source | Solution architect, P4 rwb-access with the external gateway owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0785 | The contract of the partner identity resolution names no path, no claim or answer field, no refusal-to-status mapping and no statement of its absent events in any source | Tech lead of rwb-access with the external gateway owner and the rwb-partner service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0786 | The certificate profile, the rotation and revocation of the rwb-access hop, the numeric rate limit and the namespace and service names of the DMZ hop are specified by no source | SCB IT infrastructure with the security design authority | Resolved (directive) |
| GAP-0937 | The Documents letters per role are not in the P4 RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0938 | The authorise request and answer for a document generation request are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0939 | The role row, class and scope of the SY-CASEWF service identity are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0941 | rwb-access document set: the authorise request and answer shape for the document screens, and the scope a service identity is asked for, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1017 | The generation-screens baseline fixes six operations and four shapes that no source names, two conflicting legacy paths, the field names of the request and answer objects, and a status mapping the legacy section 12 states only in prose | Tech lead of rwb-document, with the solution architect and the rwb-comms owner | Resolved (directive) |
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
| GAP-1181 | signature_request is defined in TSD P6 but is owned by P5 rwb-document | Solution architect | Resolved (directive) |
| GAP-1182 | The published P5 document names no operation to create, read by external reference or update a signature request | Solution architect | Resolved (directive) |
| GAP-1183 | No rwb-treatment contract story is in the plan, although the story reads the treatment and writes its signature record | Solution architect | Resolved (directive) |
| GAP-1184 | The plan holds no RWB-P6-E2018-CON, so the three signature-request operations have no published contract story | Solution architect | Resolved (directive) |
| GAP-1185 | The Architecture v5 event catalogue carries no comms signature event | Solution architect | Resolved (directive) |
| GAP-1186 | The signed PDF object and the byte transfer into the P5 write-once store are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1187 | The ACE common module e-signature path (INT-34) is not in the integration inventory and its shape, endpoint and certificate are unknown | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1188 | P3's cancel on offer expiry has no operation in the target catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1196 | DP-03 and its decision-record library are missing from the pattern set and the build list of the e-signature key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1272 | The partner access decision record has no operation, no field composition and no result vocabulary in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1273 | The append path of a partner access record is read synchronously while Arch v5 names it as a consumed event | Solution architect and integration lead | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1278 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1283 | The decision code of a field-capture entry is D6.5 in the legacy metadata but DOCATT on the store path | Business analyst, P7, with the business analyst of P5 rwb-document and the data steward | Resolved (directive) |
| GAP-1284 | No source settles whether an item the store refuses leaves a DOCATT entry | Business analyst, P7, with the P5 business analyst and the integration lead of RWB-ITG-E2024-ITG | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1289 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Solution architect, with the platform team and the P7 rwb-decision owner | Resolved (directive) |
| GAP-1395 | DMZ network design, gateway product, FAPI 2.0 settings, external identity provider, certificate lifecycle, rate limits, WAF rule set and DR target of the partner gateway are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1573 | The joiner, mover and leaver capability has a Must requirement in Epic 2, a feature code in Epic 1 and no legacy story, and its response times are open under DL38 | Business analyst with the security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1589 | Signatures are owned by P5 in Architecture v5 and the Ownership Map but have no requirement, feature or story | Solution architect with P6 and S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1596 | The signature request is defined as a Communications table while Architecture v5 gives signatures to the document hub | Solution architect | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1599 | The message record and its delivery status have no table in the service under Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1600 | The retry limit for a send is five in the functional specification and three in the non-functional requirements | Solution architect | Resolved (directive) |
| GAP-1601 | The functional specification names JOB-11 as the retry job for sends, and Architecture v5 makes JOB-11 the outbox relay in every service | Solution architect | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1605 | The contact repository and the consent state are held in an extension table the source-data service owns | Solution architect | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1609 | The notice period timer and the transfer on a non-delivered notice are the case service's, and the trigger is not fixed | Solution architect with P3 | Resolved (directive) |
| GAP-1610 | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | Conduct and QA officer with rwb-decision | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1852 | Partner identity is a table in rwb_partner while the requirement that governs it is delivered by rwb-access | Security administrator with the P4 and S9 owners | Resolved (directive) |
| GAP-1876 | The checked-fields operation and payload on the treatment side, the treatment columns that carry the contract and mortgage facts, the masking of the treatment read and who stamps the type-table version are not specified | Solution architect with the rwb-treatment and rwb-document squads | Resolved (directive) |
| GAP-1877 | Architecture v5 puts the S2 call to P5 in the Temporal column while the legacy published interface and DP-11 make the checked-fields read one REST hop | Solution architect with the platform workflow team, rwb-document and rwb-treatment | Resolved (directive) |
| GAP-1878 | The treatment-side generation call, its two columns, the merge-field set and the generation event are not specified | Solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
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
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2352 | The signature-request operations exist in no P5 source and carry no API ID, because the legacy key is a communications module story while the table is P5's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2353 | signature_request is defined in TSD P6 T3.1 inside the communications module and owned by P5 in the ownership ruling, so the table has no P5 data model | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2355 | No source names a signature event on the rwb-document topic, and the request state is readable only through the operations of the story | Solution architect | Resolved (directive) |
| GAP-2356 | The write-once container, the WORM tier, the size limit and the byte transfer behind the signed-version add are named by no source | SCB IT infrastructure | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2357 | No rwb-document message exists for a closed signature request and no source names the operation-level right of the five request operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2393 | rwb-comms generation request key and P5 document-create operation are not specified | Service owner, rwb-comms; service owner, rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2394 | Generated-documents endpoint is not in the P6 operation inventory | Architecture owner; service owner, rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2697 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Solution architect | Resolved (directive) |
| GAP-2698 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Solution architect | Resolved (directive) |
| GAP-2699 | The treatment-side signature columns, the operation a signature record arrives on, the event names, the two list codes and the closure are not specified for rwb-treatment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2700 | Architecture v5 gives S2 to P5 the Temporal cell and no cell from P6 or P5 into S2, while the legacy seam is one synchronous in-process call and the work package lists DP-11 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2701 | The legacy one module and one transaction for the signature request, the signed version and the treatment field become three owners, and the offer expiry that closed the request is now the treatment's own date | Solution architect | Resolved (directive) |
| GAP-2702 | The treatment-side checked-field read, the fact columns it fills, the type-table version stamp and the unmapped field codes are not specified | Tech lead of rwb-treatment with the P5 owner of the checked-field contract and the rwb-treatment data owner | Resolved (directive) |
| GAP-2703 | Architecture v5 puts the S2 read of rwb-document on Temporal while the legacy interface and DP-11 make it one REST hop | Solution architect with the P5 contract owner and the platform Temporal owner | Resolved (directive) |
| GAP-2835 | The litigation-side checked-field read, the fact columns it fills on legal_action and hearing, the source stamps and the unmapped field codes are not specified | Tech lead of rwb-litigation with the P5 owner of the checked-field contract and the rwb-litigation data owner | Resolved (directive) |
| GAP-2836 | No source says how an extracted hearing_date becomes a hearing row, which hearing_type that row carries, or what the apply does to an action in a closed status | Litigation business analyst with the rwb-litigation data owner and the S4 hearing story owner | Resolved (directive) |
| GAP-3147 | EP02 wave 2 for rwb-partner while the service's Architecture v5 wave is 4 | Solution architect | Resolved (directive) |
| GAP-3148 | The rwb-partner slice of the key has no published load path, no message per condition and no partner_user catalogue | Solution architect with the reference data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3181 | The partner_user table is created by P4 in the story and owned by S9 in the ownership map | Access lead with the partner lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3182 | The signature_request table is created by P6 in the story and owned by P5 in the ownership map | Document hub lead with the communications lead | Resolved (directive) |
| GAP-3183 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 result file with it | Integration lead with the communications lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E2019-ITG | skipped AC ID | 104 | missing: AC6, AC9 |
| RWB-ITG-E2021-ITG | skipped AC ID | 102 | missing: AC3, AC6, AC7, AC8, AC9, AC10, AC11, AC12 |
