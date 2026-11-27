# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 8 of 11 (RWB-P4-E2017-APP to RWB-P4-E2026-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 144 |
| Cross-document (pending in another document) | 192 |
| Not applied (value not in the sources) | 21 |
| Open business decisions | 35 |
| Register gaps linked | 103 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E2017-APP | 19 | 24 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2017 APP Contract, CA and mortgage document generation screens v2.md |
| RWB-P4-E2019-APP | 24 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2019 APP Partner identities through the external gateway v2.md |
| RWB-P4-E2019-CON | 20 | 16 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2019 CON Partner identities through the external gateway - contract v2.md |
| RWB-P4-E2019-INF | 9 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2019 INF Partner identities through the external gateway - infrastructure v2.md |
| RWB-P4-E2021-APP | 19 | 40 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2021 APP Letter dispatch loop with proof of delivery from WIN v2.md |
| RWB-P4-E2022-APP | 17 | 30 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2022 APP SMS and LINE dispatch through NSS and LINE OA v2.md |
| RWB-P4-E2024-APP | 16 | 19 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2024 APP Field app photos and bills into the document hub v2.md |
| RWB-P4-E2026-APP | 20 | 21 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2026 APP Document generation engine for contract, CA and mortgage templates v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E2019-APP | R-01294 | CG-ALL-5253 | Script gap | Product owner | The story adds BANK_IDENTITY_ON_PARTNER_ROUTE to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2019-APP | R-01295 | CG-ALL-5254 | Script gap | Product owner | The story adds PLACED to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2019-CON | R-01299 | CG-ALL-5262 | Script gap | Product owner | The story adds PLACED to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2017-APP | R-10731 | CG-ALL-5249 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2022-APP | R-10740 | CG-ALL-5294 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2024-APP | R-10743 | CG-ALL-5311 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
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
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-22619 | GAP-1287 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The generation record's payload, value sets, read shape, message set and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the template code, the template version, the treatment reference and the requesting role on decision_log_entry, the shape of the merge snapshot reference, the decision code D6.4 as a value of LOV-DECISION, the final-call list that holds GENERATED, the message ids and texts of a refused record and a duplicate append, the page-size parameter name, the search index and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2026-1 to ASM-B-P7-03-E2026-5 and its nine criteria stand on that shape |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1043-CON, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-28792 | GAP-2097 | Register gap | Service owners of P3 rwb-case and P4 rwb-access; business lead | Reference data is read from P4 in TSD P6 and from P3 in the plan default ruling | Follow R3 and DP-07: contact times and frequency are reference data of P3 rwb-case, read through C RWB-P3-E1043-CON. Access data, roles and DoA stay with P4. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-28804 | GAP-2222 | Register gap | Business lead | The legal hold reason list is not stated | Hold the reason list as a reference table of rwb-case loaded by RW-COE; the reason is stored as given until the list is approved. |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-28820 | GAP-0940 | Register gap | Compliance and PDPA officer | The masking version label and the DF-PTY-007 rows on the generation path are not specified | Load the DF-PTY-007 masking rows with unmasked false for RW-RESTRUCT, RW-CASEOWN, RW-TEAMMGR and SY-CASEWF under the SIT masking version, name the version in the policy pack load record, and leave the format to the one masking library every screen uses. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P4-E2017-APP | R-36733 | ASM-1677 | Register assumption |  | Masking version MASK-SIT-01 is the version in force for SIT, the personal fields of the review view are DF-PTY-007 and DF-PTY-016 as the FSD P4 A2.7 entry names them, both are masked for every role of the set because the pack holds no unmask row for them, and any further field ID is marked from the request; no rendering of either field is fixed by this story. | Compliance and PDPA officer and the rwb-access tech lead before SIT |
| RWB-P4-E2022-APP | R-36754 | ASM-1685 | Register assumption |  | Masking version MASK-SIT-01 is in force in SIT, and no row of the pack names DF-ACE-078 or DF-ACE-077 unmasked for any role on the message path, so both fields are masked for every role, including the case owner and the platform administrator. The story reads the version from the rows at run time and asserts only that no value is returned; the rendering is the masking library's. | Compliance and PDPA officer, at the masking pack review |
| RWB-P4-E2024-APP | R-36759 | ASM-1680 | Register assumption |  | Masking version MASK-SIT-01 is in force for SIT; the two position fields DF-DOC-028 and DF-DOC-029 have unmasked rows for RW-CASEOWN and RW-RESTRUCT and no unmask for RW-FIELDCOL, RW-PHONECOL or SY-OCR; and the masked rendering is left to the one platform masking library, so the story asserts the masked flag and the mask version and never a format. | Compliance and PDPA officer, at the masking pack review |
| RWB-P4-E2026-APP | R-36765 | ASM-1668 | Register assumption |  | The masking version in force for SIT is MASK-SIT-01, the DF-PTY-007 national ID field carries unmasked false rows for RW-RESTRUCT, RW-CASEOWN, RW-TEAMMGR and SY-CASEWF in that version, a field with no covering row stays masked by default, and the mask format is the one masking library's and not this story's. | Compliance and PDPA officer with the security administrator at the policy pack load |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E2017-APP | R-25486 | CG-ALL-5246 | 16 | Test cases cover other criteria in Test Cases v8 | AC12 and AC13 are not in section 7. TC rows restored to prior criteria mapping. Confirm the mapping against Test Cases v8. |
| RWB-P4-E2019-APP | R-25492 | CG-ALL-5261 |  | Story cites document versions that are not the highest | The story line citing API Specification v4 is not in the supplied text. Grep of the chunks and story folder found v4 only in gap-register text, not in the story. Cannot match old text. |
| RWB-P4-E2019-CON | R-16810 | DOR-RWB-P4-E2019-CON-1 | 1 | Definition of Ready item 1 Story: Partial | No role name in the sources supports the replacement. Confirm the role against Users Roles and Permissions v5, then edit section 1. |
| RWB-P4-E2019-CON | R-16813 | DOR-RWB-P4-E2019-CON-18 | 19 | Definition of Ready item 18 Open decisions: Partial | Section 19 current text is not in this chunk, so no exact old text exists to add DL10 and ASM-2250, ASM-2357, ASM-2377, ASM-2863. Needs section 19 in the next chunk. |
| RWB-P4-E2019-CON | R-25495 | CG-ALL-5267 | 9 | Story cites document versions that are not the highest | Section 9 current text is not in this chunk, so the API Specification v4 citation has no exact old text. Document Index v14 confirms v5 is highest. Needs section 9. |
| RWB-P4-E2021-APP | R-16825 | DOR-RWB-P4-E2021-APP-3 | 5, 7 | Definition of Ready item 3 Acceptance criteria: Partial | Section 16 row for AC11 is not added; the section 16 text is not in this chunk, so it is deferred. |
| RWB-P4-E2021-APP | R-16826 | DOR-RWB-P4-E2021-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Section 16 rows for the business rules are not added; the section 16 text is not in this chunk, so they are deferred. |
| RWB-P4-E2021-APP | R-22561 | GAP-0404 | 16 | The WIN dispatch harness pack and the proof-file test window are not specified | No WIN or INT-15 fixture, window control, seeding, evidence or gate value found in the project. Needs agreement with ACE integration team and QA. |
| RWB-P4-E2021-APP | R-25498 | CG-ALL-5277 | 16 | Test cases cover other criteria in Test Cases v8 | Covers changed on nine rows, but several rows still conflict with criterion content (TC-02, TC-04, TC-05, TC-08, TC-10). Not resolved until the v8 check is done. |
| RWB-P4-E2021-APP | R-25500 | CG-ALL-5280 | 3, 3.1 | Flyway file V2021_1__access_dispatch_read_indexes.sql is not in the V0001..Vnnnn form | The next Flyway number of the rwb-access sequence is not in the sources searched. Line 405 text is not in this chunk. |
| RWB-P4-E2021-APP | R-28796 | GAP-1096 | 14 | The message text of MSG-P6-005 and MSG-P3-005 is not given by the legacy story or the P6 extracts | MSG-P6-005 and MSG-P3-005 wordings are not published in the sources searched. Section 14 text is not in this chunk, so no placeholder row was added. |
| RWB-P4-E2022-APP | R-16830 | DOR-RWB-P4-E2022-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | Field not named in item. No DOR-RWB-P4-E2022-APP-11 text in 22 Microservice Realignment; no classed-as-personal-data field identified. Needs the detcheck report. |
| RWB-P4-E2022-APP | R-16832 | DOR-RWB-P4-E2022-APP-15 | find it | Definition of Ready item 15 INVEST: Partial | Size is Not specified in the source documents (DOR-RWB-P4-E2022-APP-16); a two-week fit would be an invented value. Story header Size row unchanged. |
| RWB-P4-E2022-APP | R-25506 | CG-ALL-5295 | 3, 3.1 | Flyway file V2022_1__access_send_indexes.sql is not in the V0001..Vnnnn form | Service Template Spec v1 §3.1 has V0001 only as baseline; no rwb-access V00nn file found in sources. Next number not stated. Line 429 is outside this chunk. |
| RWB-P4-E2024-APP | R-16837 | DOR-RWB-P4-E2024-APP-15 | Header | Definition of Ready item 15 INVEST: Partial | No size is invented; the squad sizes it at refinement (DOR-16). |
| RWB-P4-E2024-APP | R-22593 | GAP-0406 |  | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | No source gives the field-app test client, capture fixtures, intake profile, SIT seeding or evidence format. Needs P5 owner and QA agreement; no value invented. |
| RWB-P4-E2024-APP | R-25512 | CG-ALL-5308 | 16 | Test cases cover other criteria in Test Cases v8 | Story AC11 to AC15 collide with the story's own criteria, so no v8 renumbering was applied. |
| RWB-P4-E2024-APP | R-25514 | CG-ALL-5312 | 3, 3.1 | Flyway file V2_5_024__field_capture.sql is not in the V0001..Vnnnn form | The next V-number for rwb-access is in no source (searched V2_5_024 and V0001 across the set). Story line 383 text was not supplied. Not invented. |
| RWB-P4-E2024-APP | R-28813 | GAP-1282 | 13 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | The fix defers the metadata rows to a later story set version. |
| RWB-P4-E2026-APP | R-05857 | DOR-RWB-P4-E2026-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in 04 User stories or the story text; sign-off cannot be confirmed. Needs the epic design record (not in sources). |
| RWB-P4-E2026-APP | R-16844 | DOR-RWB-P4-E2026-APP-18 |  | Definition of Ready item 18 Open decisions: Partial | DL10 and DL26 are open business decisions; directive removed them from scope. Story text given has no open-decisions section to edit. Decisions stay open. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (31)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08757 | RWB-P4-E2017-APP | CG-ALL-5242 | 2 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data. |
| CDC-08758 | RWB-P4-E2017-APP | CG-ALL-5243 | 2 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data. |
| CDC-08761 | RWB-P4-E2017-APP | DOR-RWB-P4-E2017-APP-8 | find it | Add Idempotency-Key to POST /api/recovery/access/v1/authorise; add paths POST authorise, GET /api/recovery/access/v1/me/permissions and GET /api/recovery/access/v1/masking-policies; hold roleClass as LOV-ROLE-CLASS data, not a closed enum. |
| CDC-08778 | RWB-P4-E2019-APP | CG-ALL-5255 | 12.1 | Publish POST /api/recovery/access/v1/partner-identities/resolve in rwb-access.yaml through RWB-P4-E2019-CON |
| CDC-08779 | RWB-P4-E2019-APP | CG-ALL-5257 | 12.8 | Remove the fixed enum on roleClass and validate it against LOV-ROLE-CLASS as data |
| CDC-08780 | RWB-P4-E2019-APP | CG-ALL-5258 | 12.8 | Remove the fixed enum on defaultScope and validate it against LOV-SCOPE as data |
| CDC-08784 | RWB-P4-E2019-APP | DOR-RWB-P4-E2019-APP-8 | 12.1 | Publish the resolve path and drop the roleClass and defaultScope enums. The 400 message id is flagged in 12.1 as Not specified. |
| CDC-08801 | RWB-P4-E2019-CON | CG-ALL-5263 | 12.1 | Publish POST /api/recovery/access/v1/partner-identities/resolve with the contract of RWB-P4-E2019-CON section 12.1 |
| CDC-08836 | RWB-P4-E2021-APP | CG-ALL-5271 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08837 | RWB-P4-E2021-APP | CG-ALL-5272 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08838 | RWB-P4-E2021-APP | CG-ALL-5273 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08839 | RWB-P4-E2021-APP | CG-ALL-5274 | 2 | Remove the fixed enum from defaultScope so LOV-SCOPE values are accepted as data without a code change. |
| CDC-08843 | RWB-P4-E2021-APP | DOR-RWB-P4-E2021-APP-8 | 12.1 | Add POST /api/recovery/access/v1/authorise, GET /api/recovery/access/v1/me/permissions and GET /api/recovery/access/v1/masking-policies; hold defaultScope as LOV-SCOPE data, not a closed enum; resolve the two further detcheck findings. |
| CDC-08876 | RWB-P4-E2022-APP | CG-ALL-5285 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON, as section 12.1 states. |
| CDC-08877 | RWB-P4-E2022-APP | CG-ALL-5286 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in rwb-access.yaml through RWB-P4-E1037-CON, as section 12.1 states. |
| CDC-08878 | RWB-P4-E2022-APP | CG-ALL-5287 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through RWB-P4-E1037-CON, as section 12.1 states. |
| CDC-08879 | RWB-P4-E2022-APP | CG-ALL-5288 | 1 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data, as section 1 states. |
| CDC-08880 | RWB-P4-E2022-APP | CG-ALL-5289 | 1 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data, as section 1 states. |
| CDC-08883 | RWB-P4-E2022-APP | DOR-RWB-P4-E2022-APP-8 | 12.1 | Add paths POST /api/recovery/access/v1/authorise, GET /api/recovery/access/v1/me/permissions and GET /api/recovery/access/v1/masking-policies; hold roleClass as LOV-ROLE-CLASS data, not a closed enum; clear the three further detcheck items. |
| CDC-08906 | RWB-P4-E2024-APP | CG-ALL-5301 | 12.1 | Publish the POST operation for /api/recovery/access/v1/authorise in the paths, through the CON story RWB-P4-E1037-CON. |
| CDC-08907 | RWB-P4-E2024-APP | CG-ALL-5302 | 12.1 | Publish the GET operation for /api/recovery/access/v1/me/permissions in the paths, through the CON story RWB-P4-E1037-CON. |
| CDC-08908 | RWB-P4-E2024-APP | CG-ALL-5303 | 12.1 | Publish the GET operation for /api/recovery/access/v1/masking-policies in the paths, through the CON story RWB-P4-E1037-CON. |
| CDC-08909 | RWB-P4-E2024-APP | CG-ALL-5304 | 13 | Remove the fixed enum on roleClass; LOV-ROLE-CLASS values are data read at runtime, as section 13 states. |
| CDC-08910 | RWB-P4-E2024-APP | CG-ALL-5305 | 13 | Remove the fixed enum on defaultScope; LOV-SCOPE values are data read at runtime, as section 13 states. |
| CDC-08914 | RWB-P4-E2024-APP | DOR-RWB-P4-E2024-APP-8 | 4 | Add paths POST /api/recovery/access/v1/authorise, GET /api/recovery/access/v1/me/permissions and GET /api/recovery/access/v1/masking-policies; add Idempotency-Key header to POST authorise; hold roleClass as data aligned to LOV-ROLE-CLASS. |
| CDC-08925 | RWB-P4-E2026-APP | CG-ALL-5317 | 12.1 | Publish operation POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON. Story path is correct; item detail doubles the prefix. |
| CDC-08926 | RWB-P4-E2026-APP | CG-ALL-5318 | 12.1 | Publish operation GET /api/recovery/access/v1/me/permissions in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08927 | RWB-P4-E2026-APP | CG-ALL-5319 | 12.1 | Publish operation GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08928 | RWB-P4-E2026-APP | CG-ALL-5320 | 2 | Remove the fixed enum on roleClass; LOV-ROLE-CLASS values are data accepted without a code change. |
| CDC-08929 | RWB-P4-E2026-APP | CG-ALL-5321 | 2 | Remove the fixed enum on defaultScope; LOV-SCOPE values are data accepted without a code change. |
| CDC-08931 | RWB-P4-E2026-APP | DOR-RWB-P4-E2026-APP-8 | 7 | Add POST /api/recovery/access/v1/authorise, GET /api/recovery/access/v1/me/permissions and GET /api/recovery/access/v1/masking-policies; hold roleClass as LOV-ROLE-CLASS, not a closed enum. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08774 | RWB-P4-E2017-APP | CG-ALL-5248 | 18 | Trace REQ-DCM-012 and REQ-OCC-002 to this story's test list as in section 18 (TC-E2-017-01 to 04, 09, 10, 14, 15 and 05, 06, 08, 13); RTM v7 currently lists TC-E2-026 and TC-E1 IDs. |
| CDC-08787 | RWB-P4-E2019-APP | DOR-RWB-P4-E2019-APP-12 | 12, 12.7, 16, 18 | Added TC-E2-019-12 and TC-E2-019-13; section 16 now runs to TC-E2-019-25. |
| CDC-08797 | RWB-P4-E2019-APP | CG-ALL-5260 | 18 | Align the REQ-ACA-012 test list in RTM v7 with the story (TC-E2-019-06, TC-E2-019-09, TC-E2-019-10, TC-E2-019-11) in its next version. |
| CDC-08814 | RWB-P4-E2019-CON | CG-ALL-5266 | 18 | Align the REQ-ACA-012 test list with section 18 of RWB-P4-E2019-CON (TC-E2-019-CON-01 to TC-E2-019-CON-08). |
| CDC-08834 | RWB-P4-E2019-INF | CG-ALL-5269 | 18 | Align REQ-ACA-012 test cases to TC-E2-019-INF-01 to TC-E2-019-INF-07 in place of TC-E2-019-01, TC-E2-019-05 and TC-E2-019-09. |
| CDC-08840 | RWB-P4-E2021-APP | DOR-RWB-P4-E2021-APP-12 | 16, 18 | Align the test case lists of the REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010 rows to section 18 of RWB-P4-E2021-APP. RTM v7 is not in the folder. |
| CDC-08864 | RWB-P4-E2021-APP | CG-ALL-5279 | 18 | Align the REQ-OCC-003 and REQ-OCC-005 test lists with RWB-P4-E2021-APP section 18 in the next RTM version. |
| CDC-08901 | RWB-P4-E2022-APP | CG-ALL-5293 | 18 | Align the REQ-OCC-004 and REQ-OCC-005 test lists with section 18 of RWB-P4-E2022-APP in the next RTM version. |
| CDC-08942 | RWB-P4-E2026-APP | CG-ALL-5326 | 18 | Align the REQ-DCM-012 and REQ-OCC-002 test lists in the RTM with the test cases of this story's section 18 in the next version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08764 | RWB-P4-E2017-APP | DOR-RWB-P4-E2017-APP-7 | 11 | Add DF-PTY-007, DF-PTY-016 and DF-REF-039 as field IDs, and add transfer_price as a field or entity in LDM v9 or in Data Classification v5. |
| CDC-08788 | RWB-P4-E2019-APP | DOR-RWB-P4-E2019-APP-7 | 11 | Confirm DF-REF-039 exists in the role table of LDM v9, or remove it from the DF-REF-034 to DF-REF-039 range |
| CDC-08845 | RWB-P4-E2021-APP | CG-ALL-5270 | 11, 12.7, 17 | Record contact_point as a named P1 object or map the story to its dictionary name; nearest dictionary names are contact_point_ext, contact_at and contract_no. |
| CDC-08884 | RWB-P4-E2022-APP | CG-ALL-5284 | 11 | Record contact_point as the owning entity of DF-ACE-078 and DF-ACE-077, or confirm its dictionary name. |
| CDC-08887 | RWB-P4-E2022-APP | DOR-RWB-P4-E2022-APP-7 | 11 | Confirm DF-REF-039 exists; it is not in LDM v9. Confirm the field names in section 11, including contact_point, against the dictionary. |
| CDC-08932 | RWB-P4-E2026-APP | CG-ALL-5316 | n/a | Confirm transfer_price as a dictionary field or record the merge-value object with its owner; the story names it in sections 7, 16 and 18. |
| CDC-08934 | RWB-P4-E2026-APP | DOR-RWB-P4-E2026-APP-7 | 11 | Confirm or add DF-PTY-007 and DF-REF-039 as LDM v9 fields, and confirm contact_point and transfer_price as fields or entities in LDM v9 or Data Classification v5. |
| CDC-08940 | RWB-P4-E2026-APP | GAP-1878 | 12 | Add two nullable treatment columns for the document reference and the pinned template version, with their index; the event name and code stay story design. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08805 | RWB-P4-E2019-CON | GAP-0067 | header | Set the rwb-partner wave to 2 to match W-MAP; this story stays Wave 2. |
| CDC-08826 | RWB-P4-E2019-INF | GAP-1273 | find it | Confirm the dual path: the record path on the resolution for the fail-closed answer, and topic rwb.decision-record.v1 for durability, replay and the five-minute completeness target, deduplicated by idempotency key. |
| CDC-08848 | RWB-P4-E2021-APP | GAP-1597 | header | Record the proof path: notice and proof fields held in rwb-comms, proof rows read through the rwb-source-data contract, barcode match applies the proof to the notice; ACE team states the writer of v_ace_pod |
| CDC-08850 | RWB-P4-E2021-APP | GAP-2096 | none | Record that rwb-comms reads the proof through the P1 contract on the ACE batch business date, matches by barcode and publishes EV-15 NoticeDelivered; no new job |
| CDC-08867 | RWB-P4-E2021-APP | GAP-2095 |  | Record the partner instruction as S9 InstructionWorkflow and the internal alert as a P3 task; rwb-comms keeps only the partner instruction template. |
| CDC-08872 | RWB-P4-E2021-APP | GAP-1609 | 7 | Publish NoticeDelivered so rwb-case starts NOTICE_PERIOD from the callback date; record the undelivered transfer decision and call rwb-case transfer with NOTICE_UNSERVED; publish NoticeDispatched with delivery status. |
| CDC-08873 | RWB-P4-E2021-APP | GAP-2106 | 12.5 | Record rwb-comms as owner of the JOB-10 Schedule and rwb-integration as owner of transport and retry, publishing FileDelivered or FileFailed to P6. |
| CDC-08896 | RWB-P4-E2022-APP | GAP-1071 | 12 | Confirm that the attempt counter and rule R-UNI-34 count one send attempt per relay window, with the path's internal retries excluded. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08759 | RWB-P4-E2017-APP | DOR-RWB-P4-E2017-APP-14 | Metadata | Record the signed epic design sign-off; none is recorded in the story or source documents. |
| CDC-08802 | RWB-P4-E2019-CON | DOR-RWB-P4-E2019-CON-14 | n/a | Record a signed epic design for EP02 and confirm the sign-off |
| CDC-08817 | RWB-P4-E2019-INF | DOR-RWB-P4-E2019-INF-14 | header | Record the signed epic design sign-off for EP02 in the epic design record |
| CDC-08841 | RWB-P4-E2021-APP | DOR-RWB-P4-E2021-APP-14 | Metadata | Record the signed epic design sign-off for RWB-SVC-P4 and cite it in the story; no sign-off asserted in the story. |
| CDC-08881 | RWB-P4-E2022-APP | DOR-RWB-P4-E2022-APP-14 | header | Record the signed epic design sign-off for EP02 in the epic design record. |
| CDC-08911 | RWB-P4-E2024-APP | DOR-RWB-P4-E2024-APP-14 | header | Record the signed epic design sign-off for EP02; no signed epic design exists in the source documents or this story. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08763 | RWB-P4-E2017-APP | CG-ALL-5244 | 12.3 | Record the payload of rwb.access.AccessPolicyChanged.v1 (policy kind, old and new version, validFrom, affected areas or fields, load reference) in the Events row new; owner Solution architect. |
| CDC-08846 | RWB-P4-E2021-APP | CG-ALL-5275 | 12.3 | Add the payload of rwb.access.AccessPolicyChanged.v1 to the Events row, matching RWB-P4-E2021-APP section 12.3 (gap-0127; asm-0204). |
| CDC-08885 | RWB-P4-E2022-APP | CG-ALL-5290 | 12.3 | Define the payload of rwb.access.AccessPolicyChanged.v1 (Events row new) with the five story payload fields, or confirm them; its field list is Not specified in the source documents (gap-0127; asm-0204). |
| CDC-08915 | RWB-P4-E2024-APP | CG-ALL-5306 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 (gap-0127; asm-0204) so the story's section 12.3 payload can be aligned to it. |
| CDC-08933 | RWB-P4-E2026-APP | CG-ALL-5322 | n/a | Record the payload of rwb.access.AccessPolicyChanged.v1 as in section 12.3 (policy kind, old and new version, validFrom, affected areas or fields, load reference) or resolve gap-0127. |

### RWB-P4-E1037-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08766 | RWB-P4-E2017-APP | GAP-1713 | find it | Record once the mapping of each FEAT prerequisite to its owning service contract: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1. Carry duplicate FEAT-CHO-08 as written. |
| CDC-08882 | RWB-P4-E2022-APP | DOR-RWB-P4-E2022-APP-22 | header | Publish a contract fake library version for the section 12.1 operations and record the version as published. |
| CDC-08912 | RWB-P4-E2024-APP | DOR-RWB-P4-E2024-APP-21 | header | Publish the contract covering the operations of section 12.1; no contract story RWB-P4-E2024-CON exists and this story does not create one. |
| CDC-08919 | RWB-P4-E2024-APP | GAP-0952 | none | Publish the authorise, me-permissions and masking-policies shapes and state whether a sync is authorised once per manifest or once per item, and how the field list is carried. |
| CDC-08936 | RWB-P4-E2026-APP | GAP-0938 | 12.1 | Add the request and answer schema of POST /api/recovery/access/v1/authorise, publish it with RWB-P4-E1037-CON, and stub the generation facts in RWB-P5-E2026-CON. |

### RWB-P6-E2021-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08842 | RWB-P4-E2021-APP | DOR-RWB-P4-E2021-APP-22 | 3 | Publish the contract fake library and record its version as published. |
| CDC-08854 | RWB-P4-E2021-APP | GAP-1089 | header | Fix the WIN file name, record layout, acknowledgement fields and proof result record; read proof results via the rwb-integration contract or add RWB-P1-E1066-CON |
| CDC-08858 | RWB-P4-E2021-APP | GAP-1095 | find it | Publish the Airflow window to Temporal Schedule handoff row: window signals the Schedule with the business date, the run records the date, and a rerun of the same date writes no second file. |
| CDC-08863 | RWB-P4-E2021-APP | GAP-1092 | find it | Declare the capability area and right per operation so gateway-bff asks rwb-access (DP-08) first; serve the scope fact from the rwb-case read, or add C RWB-P4-E1037-CON if rwb-comms decides scope. |
| CDC-08868 | RWB-P4-E2021-APP | GAP-1094 |  | Add the Notice component with the nine legacy fields plus holdReason, dispatchFileId and dispatchAttempts, all optional except id and caseId; validate the additive rule against RWB-P6-E1052-CON. |

### RWB-P4-E2019-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08782 | RWB-P4-E2019-APP | DOR-RWB-P4-E2019-APP-21 | header | Set build status to Done once the contract is published |
| CDC-08798 | RWB-P4-E2019-APP | GAP-1567 | none | Drop lov_value and partner_user with the partner relationship from TSD P4 T3.1 and T3.3; state in the rwb-access contract which list-of-values versions and partner identity attributes are read and how often they refresh. |
| CDC-08818 | RWB-P4-E2019-INF | DOR-RWB-P4-E2019-INF-21 | header | Set build status to Done and publish the contract; header now names it as a contract dependency |
| CDC-08819 | RWB-P4-E2019-INF | DOR-RWB-P4-E2019-INF-22 | header | Publish the contract fake library and record its published version |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08786 | RWB-P4-E2019-APP | CG-ALL-5259 | 16 | Add rows TC-E2-019-01 to TC-E2-019-11 with Given, When and Then copied from the criterion each covers |
| CDC-08813 | RWB-P4-E2019-CON | CG-ALL-5265 | 16 | Add rows for TC-E2-019-CON-01 to TC-E2-019-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-08833 | RWB-P4-E2019-INF | CG-ALL-5268 | 16 | Add rows TC-E2-019-INF-01 to TC-E2-019-INF-07 with Given, When and Then copied from the criteria they cover. |
| CDC-08886 | RWB-P4-E2022-APP | DOR-RWB-P4-E2022-APP-12 | 16 | Add TC-E2-022-15 boundary test for the section 12.7 tables to the Story test cases tab; align the section 18 test lists with RTM v7. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08790 | RWB-P4-E2019-APP | GAP-0785 | 11 | Resolution path added to section 11; no event statement is made, since AC-SIGN is published to rwb.decision-record.v1 per DP-03. |
| CDC-08806 | RWB-P4-E2019-CON | GAP-0785 | 11, 7, 8 | Register POST /partner-identities/resolve with the PartnerIdentityClaim and PartnerIdentityAnswer schemas and the refusal-to-status table; state that no event is published or consumed. |
| CDC-08811 | RWB-P4-E2019-CON | GAP-0784 | header | Register the partner identity resolution operation with its schema; state whether PLACED is a session scope descriptor or role default scope; state answer lifetime against the partner edge token lifetime. |
| CDC-08945 | RWB-P4-E2026-APP | GAP-2394 | 12 | Allocate the next API-P6-nnn ID to POST /api/recovery/comms/v1/cases/{caseId}/generated-documents and add it to the P6 API specification with the gateway-bff route. |

### RWB-P4-E1037-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08754 | RWB-P4-E2017-APP | CG-ALL-5239 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml; the path is already named in 12.1, so no story edit. |
| CDC-08755 | RWB-P4-E2017-APP | CG-ALL-5240 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in rwb-access.yaml; no story edit. |
| CDC-08756 | RWB-P4-E2017-APP | CG-ALL-5241 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml; no story edit. |

### RWB-P5-E2017-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08760 | RWB-P4-E2017-APP | DOR-RWB-P4-E2017-APP-22 | find it | Record the contract fake library version as published. |
| CDC-08770 | RWB-P4-E2017-APP | GAP-1278 | find it | Publish the rwb.decision-record.v1 payload field set, the correction final call, the document set and value pair reference shapes, the two parameter names and the MSG-P4-003 message id. |
| CDC-08771 | RWB-P4-E2017-APP | GAP-2697 | find it | Publish the treatment panel as an optional additive property of the declared treatment read, with its action vocabulary. Take the set read from RWB-P5-E2017-CON with a 2 s budget and a fake. Take document types and the set row from the reference-data contract at its version. |

### RWB-P4-AD002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08765 | RWB-P4-E2017-APP | GAP-0942 | find it | Add a Documents column to the RBAC matrix: CRU for RW-RESTRUCT and RW-CASEOWN, R for RW-TEAMMGR, CRUA for RW-LEGAL (A is template approval). Confirm with the matrix owner and publish in the PM-2026.12 pack. |
| CDC-08855 | RWB-P4-E2021-APP | GAP-0945 | find it | Add a Litigation column to T6.1 for every role the legacy authority table names; publish the 14-area matrix version as data; confirm the C and R letters with the matrix owner. |
| CDC-08856 | RWB-P4-E2021-APP | GAP-0948 | find it | Name the JOB-10 runner service identity in the role table with class NON_HUMAN_ACTOR, scope ALL and its Litigation R row; the role code is a source value still to be supplied. |

### RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08773 | RWB-P4-E2017-APP | GAP-0401 | 15 | Publish the gateway-bff composite route path for SCR-14 and SCR-30, its merge order, the harness repository and environment, test-data seeding, evidence format and retention, and the wave 2 pass/fail gate, agreed with QA. |
| CDC-08777 | RWB-P4-E2017-APP | GAP-0944 | 15 | Publish the composite route field list for SCR-14 and SCR-30, and add the allowed-action decision code for updates and sends to the ledger decision-code list before the audit query is built. |
| CDC-08924 | RWB-P4-E2024-APP | GAP-0951 | find it | State the field app route: capture sync as a composed call beside the rwb-document call, and the SCR-30 panel as a parallel read, both through the gateway-bff composite route. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08783 | RWB-P4-E2019-APP | DOR-RWB-P4-E2019-APP-5 | 9 | Carry PLACED and BANK_IDENTITY_ON_PARTNER_ROUTE as LOV-SCOPE data values |
| CDC-08803 | RWB-P4-E2019-CON | DOR-RWB-P4-E2019-CON-5 | 9 | Add PLACED to the closed list LOV-SCOPE |
| CDC-08922 | RWB-P4-E2024-APP | GAP-1283 | none | Approve DOCATT as the LOV-DECISION value on every document-attach entry, keep D6.5 as a routing tag only, and record the decision in the register. |

### RWB-S9-E2019-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08794 | RWB-P4-E2019-APP | GAP-3181 | none | Own the DDL V_E2_019__partner_user.sql and the partner_user reference load handler in the rwb_partner sequence; keep the session, role and scope checks in rwb-access. |
| CDC-08800 | RWB-P4-E2019-APP | NEWAC-RWB-P4-E2019-APP-AC19 | 7 | Add a criterion that refuses a partner status change the partner state model does not allow. |
| CDC-08810 | RWB-P4-E2019-CON | GAP-3181 | 18 | Move the partner_user DDL V_E2_019__partner_user.sql and the reference load handler to the S9 story set; keep session, role and scope checks in rwb-access. |

### RWB-P1-E1066-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08866 | RWB-P4-E2021-APP | GAP-2182 |  | Settle one case-scoped ledger path family, then realign the fake in RWB-P6-E2021-CON and the consumed row in RWB-P3-E2021-APP to it. |
| CDC-08890 | RWB-P4-E2022-APP | GAP-1070 | header | Name the contact-point read, consent and verified fields, failed-count update, and ledger record and delivery-update operations. Dependency row now lists RWB-P1-E1066-CON. |
| CDC-08899 | RWB-P4-E2022-APP | GAP-2183 | 3 | Publish the two contact-point operations and the ledger extension in the P1 API appendix at the RWB-P6-E2022-CON baseline, and confirm the delivery column types, consent renderings, channel mapping, count rule and list sources at contract review. |

### RWB-P5-E2026-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08930 | RWB-P4-E2026-APP | DOR-RWB-P4-E2026-APP-22 | n/a | Record a published contract fake library version for the rwb-document contract mock this story uses. |
| CDC-08941 | RWB-P4-E2026-APP | GAP-2393 | 12 | Record the rwb-document create operation in the P6 API specification from RWB-P5-E2026-CON; keep the request key and lock in an rwb_comms table from the V-baseline migration. |
| CDC-08944 | RWB-P4-E2026-APP | GAP-1024 | 12 | Declare the path POST /cases/{caseId}/generated-documents, fix the three resources and their required sets, publish the four provider interfaces and the decision record as typed contracts, and declare one event with five payload fields. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08762 | RWB-P4-E2017-APP | CG-ALL-5238 | 16 | Confirm the dictionary name for the transfer price field named as transfer_price at TC-E2-017-06, or add that field; owner Data. |
| CDC-08847 | RWB-P4-E2021-APP | DOR-RWB-P4-E2021-APP-7 | 11 | Add or confirm DF-PTY-007, DF-PTY-016 and DF-REF-039 as BR field IDs, and name contact_point as an entity or field |

### OTHER:FSD P5 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08767 | RWB-P4-E2017-APP | GAP-1580 | find it | Add a generation section with FR-P5-026 and AC-P5-019 covering contracts, credit applications and mortgage documents generated from approved templates with case data and no re-keying, per API-P5-016, API-P5-017 and POST /documents/generate. |
| CDC-08935 | RWB-P4-E2026-APP | GAP-1580 | header | Add a generation section for REQ-DCM-012 in the next version, with FR-P5-026 and AC-P5-019 carrying the behaviour of the BRD Epic 2 requirement and API-P5-016. |

### OTHER:split_plan.json (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08785 | RWB-P4-E2019-APP | GAP-1844 | Header | Keep RWB-S9-E2019-APP in wave 2 as the partner identity and portal contract slice; publish the partner_user binding and the FAPI 2.0 route before panel work starts |
| CDC-08820 | RWB-P4-E2019-INF | GAP-1844 | header | Align the wave of the rwb-access service creation with wave 2, as the RWB-S9-E2019-APP slice requires; this story stays at wave 2 |

### OTHER:rwb-decision contract baseline (TSD P7 v2) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08791 | RWB-P4-E2019-APP | GAP-1272 | 12 | Fix the record path, the two query parameters, entry composition, result vocabulary, page-size bound parameter and index names |
| CDC-08825 | RWB-P4-E2019-INF | GAP-1272 | find it | Fix the record path, partnerId and date-range query parameters, entry composition, allowed/refused result vocabulary, page-size bound parameter and index names before the app build starts. |

### RWB-PLT-N007-INF (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08799 | RWB-P4-E2019-APP | GAP-0786 | none | Extend the certificate profile and rotation window to the gateway-to-rwb-access hop; record the per-client rate limit and burst for the resolution route; publish the rwb-access namespace, service and port. |
| CDC-08816 | RWB-P4-E2019-CON | GAP-0786 |  | Extend the certificate profile and rotation window to the rwb-access hop; record the per-client limit and burst for the resolution route; publish the rwb-access namespace, service and port. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08821 | RWB-P4-E2019-INF | DOR-RWB-P4-E2019-INF-1 | 1 | Add the role 'infrastructure and security engineer' or name the existing role code this story uses |
| CDC-08902 | RWB-P4-E2022-APP | GAP-0956 | 7 | Record JOB-11 and other platform service identities with role code, class and scope; add decision codes for a send and a refused send to the access-log decision-code list. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08849 | RWB-P4-E2021-APP | GAP-2090 | none | Add barcode, callback date and delivery status as columns of notice; add a separate proof table only if a DB story needs one |
| CDC-08865 | RWB-P4-E2021-APP | GAP-2094 |  | Settle the case-level notices list path as a P6 rwb-comms operation; the Endpoints sheet has no case-level GET. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08889 | RWB-P4-E2022-APP | GAP-2321 | 3 | GAP-2321 per R-22570: settle masking label and covered field IDs with Compliance and data steward at wave-2 policy load; confirm AC-READ granularity with Internal audit; name access-log parameter rows, defaults and batch limit at build; confirm authorise element against RWB-P4-E1037-CON at contract review. Owner: Solution architect and rwb-access contract owner. |
| CDC-08893 | RWB-P4-E2022-APP | GAP-0405 | 3, 12.8, 13 | GAP-0405 per R-22575: agree NSS and LINE OA test doubles and result-code maps with the ACE notification team and wave 2 harness pack; agree seeding and evidence format with QA. Owner: Integration lead. |

### RWB-P6-E2022-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08903 | RWB-P4-E2022-APP | GAP-1073 | Header | Fix MessageRequest and Interaction field names, closed value lists, channel and templateCode required, language default TH, partyId default borrower; settle lengths, formats and optionality at baseline review. |
| CDC-08904 | RWB-P4-E2022-APP | GAP-1076 | 7 | Hold the message delivery status as its own list SENT, DELIVERED, FAILED, READ; leave LOV-DELIVERY to the notice and proof-of-delivery capability; data steward confirms or names the list. |

### RWB-P5-E2024-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08913 | RWB-P4-E2024-APP | DOR-RWB-P4-E2024-APP-22 | Header | Publish the contract fake library and record its published version in the fake version row of the story header. |
| CDC-08921 | RWB-P4-E2024-APP | GAP-1019 | none | Declare the manifest part and clientFileId file parts, required clientFileId, kind and capturedAt, 415 only for non-multipart type, and REFUSED with MSG-P5-001 at 201; baseline Day 1, Draft. |

### OTHER:TSD P6 v2; RWB-P6-E1046-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08768 | RWB-P4-E2017-APP | GAP-2392 | find it | Add treatment-type and product-group filters to API-P6-003 and an application/json form of API-P6-005 as additive changes in major version 1. Add the locked attribute to merge_field. Publish set rows as rwb-case reference data. Copy the five message texts when the catalog is issued. |

### OTHER:TSD P4 v3 appendix T-A and T6.2; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08769 | RWB-P4-E2017-APP | GAP-0941 | find it | Publish the POST /authorise path with request and answer schema in the API specification and TSD P4 appendix T-A. Carry it on RWB-P4-E1037-CON and stub it in the contract fake. Fix the rwb-access login in the platform DB story. State the service identity scope rule in TSD P4 T6.2. |

### OTHER:Recovery Workbench work package plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08772 | RWB-P4-E2017-APP | GAP-2698 | find it | Keep the action and record placement with P5 (rwb-document). Keep the treatment gate and treatment leg with S2. Serve the screen through the gateway-bff composite route. Record that S2 writes no decision record of this key. |

### OTHER:Recovery Workbench FSD S2 (A2.18.2; OTHER:A2.15.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08775 | RWB-P4-E2017-APP | GAP-1704 | 15 | Replace 'the Workbench document hub' with requests through the P5 generation and review contracts and the P6 signature contract, with the document reference held on the treatment and no document content in schema rwb_treatment. |

### OTHER:Recovery Workbench TSD P5 T-A.1 and rwb-document generation-screens baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08776 | RWB-P4-E2017-APP | GAP-1017 | 15 | Declare the seven operations on /api/recovery/document/v1, map regenerate to API-P5-017, declare the section 13 send path and consume API-P6-009, fix request and answer field names, and map failures to one envelope and status set. |

### OTHER:source review file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08781 | RWB-P4-E2019-APP | DOR-RWB-P4-E2019-APP-14 | header | Epic design sign-off row kept as a placeholder |

### OTHER:Platform edge team test route and wave 2 harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08789 | RWB-P4-E2019-APP | GAP-0403 | 16 | Agree the partner gateway test route, FAPI 2.0 profile, directory test tenant, amr token source, harness seeding, evidence format and pass gate |

### OTHER:Backlog split plan (Epic 2; OTHER:P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08792 | RWB-P4-E2019-APP | GAP-1573 |  | Create the Epic 2 story for REQ-ACA-011 with group-change, session re-resolution, rwb-case reallocation and leaver response time; answer DL38 and DL40 |

### OTHER:TSD S9; OTHER:T-A.1 and T-A.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08793 | RWB-P4-E2019-APP | GAP-3148 | none | Add the load operation POST /api/recovery/partner/v1/admin/reference-loads with table code partner_user and an Idempotency-Key; map each refusal to its legacy message id at its legacy status; take the partner_user fields from DF-REF-212 to DF-REF-217; keep the five-minute refresh as an assumed parameter. |

### API:(service not named); OTHER:TSD P4 v3 (appendix T-A and T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08795 | RWB-P4-E2019-APP | GAP-0784 | none | Register the partner identity resolution operation with its path, method, access rule, claim set and answer schema; state whether PLACED is a session scope descriptor or a role default scope; state the answer lifetime against the partner token lifetime. |

### OTHER:Security design decision record; OTHER:Service Catalog and gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08796 | RWB-P4-E2019-APP | GAP-1395 | none | Record the DMZ zone design and firewall policy, gateway product and version, client authentication method, token lifetimes, external identity provider, certificate validity, overlap window, revocation propagation, rate limits, request size limit, WAF rule set and DR objectives. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08804 | RWB-P4-E2019-CON | DOR-RWB-P4-E2019-CON-12 | 12.7, 16, 18 | Register TC-E2-019-CON-01 to TC-E2-019-CON-08 in Test Cases v8 and align the RTM v7 test list to section 18 of this story. |

### OTHER:rwb-decision contract baseline (TSD P7 v2 appendix T-A.1 and T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08807 | RWB-P4-E2019-CON | GAP-1272 | 11 | Fix the record path, the two query parameters, the entry composition, the result vocabulary, the page-size bound parameter and the index names. |

### OTHER:Recovery Workbench backlog (new Epic 2 story for REQ-ACA-011) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08808 | RWB-P4-E2019-CON | GAP-1573 | header | Create the Epic 2 story for REQ-ACA-011 in the P4 epic with group-change, session re-resolution, rwb-case reallocation hand-off and leaver response time; answer DL38 and DL40. |

### OTHER:TSD S9 (T-A.1; OTHER:T-A.2; RWB-S9-E2019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08809 | RWB-P4-E2019-CON | GAP-3148 | 18 | Add POST /api/recovery/partner/v1/admin/reference-loads with table code partner_user and Idempotency-Key; map refusals to legacy message ids; take partner_user fields from DF-REF-212 to DF-REF-217; keep five-minute refresh as an assumed parameter. |

### OTHER:Security design decision; OTHER:Service Catalog and gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08812 | RWB-P4-E2019-CON | GAP-1395 | 18 | Fix the DMZ zone design, gateway product and version, client authentication, token lifetimes, identity provider, certificate and rate-limit values, WAF rule set and DR objectives before the penetration test. |

### OTHER:TSD P4 v3 T3.1 (and TSD P3; OTHER:TSD S9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08815 | RWB-P4-E2019-CON | GAP-1567 |  | Drop lov_value and partner_user from T3.1; keep lists of values in TSD P3 and partner identity in TSD S9; the rwb-access read path and refresh are stated in this contract. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08822 | RWB-P4-E2019-INF | DOR-RWB-P4-E2019-INF-12 | 16, 18 | Add TC-E2-019-INF-01 to TC-E2-019-INF-06 to Test Cases v8 and align the section 18 test list in RTM v7 with section 16 |

### OTHER:External partner gateway test route and partner harness pack agreement (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08823 | RWB-P4-E2019-INF | GAP-0403 | find it | Agree the partner gateway test route, directory test tenant, harness seeding of firms and identities, evidence format and pass/fail gate with platform edge and QA. Values are not in source documents. |

### OTHER:Resolution path source (not named in any source) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08824 | RWB-P4-E2019-INF | GAP-0785 | 11 | Route path left as a Not specified marker; the event statement is now a Not specified marker in section 11. |

### OTHER:Epic 2 P4 backlog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08827 | RWB-P4-E2019-INF | GAP-1573 | find it | Create the Epic 2 story for REQ-ACA-011 with the group-change scenario, session re-resolution, rwb-case reallocation hand-off and leaver response time; answer DL38 and DL40. |

### OTHER:Program v5 section 11 and FSD S9 existing capability check (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08828 | RWB-P4-E2019-INF | GAP-1852 | find it | Keep the internal role model in P4; S9 holds the partner_user binding scoping a partner user to one firm and one partner role; the gateway enforces the external identity. |

### OTHER:TSD S9 (partner_user load, message catalogue and field list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08829 | RWB-P4-E2019-INF | GAP-3148 | find it | Add the load on POST /api/recovery/partner/v1/admin/reference-loads with table code partner_user and Idempotency-Key; map refusals to legacy message ids; take fields from DF-REF-212 to DF-REF-217; keep the five-minute refresh as an assumed parameter. |

### OTHER:RWB-S9 story set (rwb_partner sequence) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08830 | RWB-P4-E2019-INF | GAP-3181 | find it | Move the partner_user DDL and its migration, and the reference load handler, to the S9 story set; keep session, role and scope checks in rwb-access. |

### API:(service not named); OTHER:TSD P4 v3 (appendix T-A; OTHER:T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08831 | RWB-P4-E2019-INF | GAP-0784 | find it | Register the partner identity resolution operation with its claim set and answer schema; state whether PLACED is a session scope descriptor or role default; state answer lifetime vs token lifetime. |

### OTHER:Security design decision; OTHER:Service Catalog; OTHER:gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08832 | RWB-P4-E2019-INF | GAP-1395 | find it | Fix DMZ zone design, gateway product and version, client authentication method, token lifetimes, external IdP, certificate validity, rate limits, WAF rule set and DR objectives before the penetration test. |

### OTHER:TSD P4 v3 (T3.1; OTHER:T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08835 | RWB-P4-E2019-INF | GAP-1567 | find it | Drop lov_value and partner_user from T3.1 and the partner_user to partner relationship from T3.3; keep the lists of values in TSD P3 and the partner identity in TSD S9. |

### OTHER:rwb-integration interface definition of INT-14 WIN dispatch file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08844 | RWB-P4-E2021-APP | GAP-1602 | header | Publish the WIN dispatch file layout as a versioned interface definition: record set, fields and order, envelope, naming, encoding, barcode and sent-date return. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08851 | RWB-P4-E2021-APP | GAP-2093 | none | Hold approval in P7 ApprovalWorkflow under NoticeDispatchWorkflow; keep S4 POST /notices/{noticeId}/approve as the decision point; remove approval from P6 OUT |

### OTHER:FSD P6 and Program BRD v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08852 | RWB-P4-E2021-APP | GAP-1610 | none | Name one versioned conduct and consent rule package governed in rwb-decision (identifier Not specified in the source documents (GAP-1610)); conduct and QA officer approves its first version |

### RWB-P1-E1016-CON; RWB-P1-E1066-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08853 | RWB-P4-E2021-APP | GAP-2181 | 12.1, 13 | Publish the DP02 contact-and-consent row and vocabulary; add required members of the LETTER append; add UNSERVED to LOV-SEND-STATUS or confirm the FAILED mapping |

### API:(service not named); RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08857 | RWB-P4-E2021-APP | GAP-0946 | find it | Add the POST /authorise path with request and answer schemas, stub it in the contract fake, and add the access entry decision codes to the ledger code list. |

### OTHER:Reference data: SERVICE_LEVEL timer row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08859 | RWB-P4-E2021-APP | GAP-2218 | find it | Load the SERVICE_LEVEL row that gives the task code NOTICE_UNSERVED, the case owner role and the due date before the wave starts. |

### OTHER:Published rwb-source-data and rwb-decision contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08860 | RWB-P4-E2021-APP | GAP-2220 | find it | Take the InteractionLedgerApi.record and DecisionLogApi.write paths from the published contracts and fakes, using the REST bases /api/recovery/source-data/v1 and /api/recovery/decision/v1. |

### OTHER:TSD P3 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08861 | RWB-P4-E2021-APP | GAP-2221 | find it | Keep the interaction ledger with rwb-source-data; remove interaction from the rwb-case object list so rwb-case holds no table, view or foreign key to it. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:Epic 2 story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08862 | RWB-P4-E2021-APP | GAP-3183 | find it | Name the delivery result event and its topic, and delete the JOB-09 loader that reads the INT-15 file from the Epic 2 story set. |

### OTHER:Data dictionary (DF-PTY-007; OTHER:DF-PTY-016) and gateway-bff composite route field list for SCR-18 and SCR-04 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08869 | RWB-P4-E2021-APP | GAP-0947 | 7 | Publish the SIT masking version in force, the addressee postal address and party field IDs with mask format, and the composite route field list. Story keeps MASK-SIT-01 assumption. |

### OTHER:rwb-source-data story for JOB-04 reconciliation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08870 | RWB-P4-E2021-APP | GAP-1090 | 13 | Assign REC-05 with notice break count, its series and output to the rwb-source-data reconciliation story (JOB-04). |

### RWB-P6-E2021-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08871 | RWB-P4-E2021-APP | GAP-1093 | 13 | Set deployment slot and replica counts once DL35 is decided; confirm the six alert thresholds at UAT and record them in each linked runbook entry. |

### OTHER:WP B2-P3-007 story (rwb-case slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08874 | RWB-P4-E2021-APP | GAP-2217 | 7 | Keep legacy AC1 to AC12 with RWB-P6-E2021-APP and write the nine new case-side acceptance criteria in the rwb-case story. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08875 | RWB-P4-E2021-APP | GAP-2219 | 13 | Allocate a key for the rwb-case slice flag at first build, enabled through the platform flag mechanism alongside rwb.comms.win-dispatch-loop. |

### OTHER:rwb-decision: conduct and consent rule package (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08888 | RWB-P4-E2022-APP | GAP-1610 | 7 | Publish the first version of one versioned conduct and consent rule package, approved by the conduct and QA officer, so the story can name its identifier. |

### OTHER:TSD P6 T6.1 and gateway-bff composite route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08891 | RWB-P4-E2022-APP | GAP-1075 | 7 | Add a Case record row for the T6.1 area and declare Case record right C on the gateway-bff composite route answering MSG-P4-002 and MSG-P4-003. |

### OTHER:rwb-source-data contract for contact_point_ext (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08892 | RWB-P4-E2022-APP | GAP-1605 | 12 | Expose the contact point, its consent state and failed count for read, and a verification and consent change for write, through the rwb-source-data contract. Enforcement stays in rwb-comms. |

### OTHER:TSD P4 v3 role-to-permission matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08894 | RWB-P4-E2022-APP | GAP-0953 | 1 | Add the Case record column and the other decided capability areas to the matrix before the first SIT entry, and load the letters as PM-2026.12 rows. |

### RWB-P6-E2022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08895 | RWB-P4-E2022-APP | GAP-1069 | 12 | Publish the request shape, accepted-reference format, NSS and LINE OA result-code maps and callback path before the wave 2 SIT entry. |

### OTHER:ACE notification path contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08897 | RWB-P4-E2022-APP | GAP-1072 | 12 | State the result transport for NSS and LINE OA. rwb-comms accepts a callback or a poll for a known external reference; a result for an unknown reference is not applied. |

### OTHER:Platform deployment chart and ACE notification path owner (Platform security team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08898 | RWB-P4-E2022-APP | GAP-1074 | 3 | Publish the egress endpoint, certificate issuer and secret names; the chart carries references only and the egress check fails a release with a missing reference. |

### RWB-P4-E1037-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08900 | RWB-P4-E2022-APP | GAP-0955 | 3 | Publish the authorise, me-permissions and masking-policies shapes in RWB-P4-E1037-CON and the SCR-03 composite field list in RWB-PLT-N001-CON before the send story is built. |

### OTHER:FSD P6 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08905 | RWB-P4-E2022-APP | GAP-1600 | 16 | Set the send retry limit to three per NFR-026 on the platform schedule; keep the fifth-attempt wording as source text until the solution architect confirms the number before wave 2. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08916 | RWB-P4-E2024-APP | GAP-3194 | none | Raise an ACE DB story for S2, S4, S5, S6, S7, P6 and P8, or attach the column drop to the creating APP story, and cite it on row 121 before wave 2. |

### RWB-P3-E1018-CON; API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:rwb-case administration stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08917 | RWB-P4-E2024-APP | GAP-2223 | none | Add stageCode and routeCode to the Case resource; record the authorise request and response shape; name the checklist contract story; load the task, owner role, discretion, due-date and decision data rows before wave 2. |

### RWB-P4-AD002-APP; OTHER:TSD P4 v3 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08918 | RWB-P4-E2024-APP | GAP-0949 | none | Add the five DOCUMENTS rows (RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU, RW-PHONECOL R) to the permission file and a Documents column to the TSD P4 RBAC matrix. |

### RWB-P5-E1024-APP; RWB-P5-E1057-CON; RWB-P5-E1049-CON; OTHER:P3 parameters and reference-data contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08920 | RWB-P4-E2024-APP | GAP-1018 | none | Store takes an optional capture block as an additive change within major version 1; intake submit creates the item; publish the five parameters and four lists under the agreed codes. |

### RWB-ITG-E2024-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08923 | RWB-P4-E2024-APP | GAP-1284 | find it | Sections 12.2 and 12.8 assert the DOCATT entry of a refused item, not its absence; one entry per stored document and per refused item, final call carries result and refusal messageId. |

### OTHER:Wave 2 SIT harness pack and template fixtures (QA; OTHER:P5 and P6 owners) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08937 | RWB-P4-E2026-APP | GAP-0408 | 16 | Record the agreed template fixtures, PDF/A-2b check, Thai font pack, harness seeding and evidence format and retention with the P5, P6 and QA owners. |

### OTHER:Policy pack PM-2026.12 (TSD P4 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08938 | RWB-P4-E2026-APP | GAP-0937 | 8 | Load Documents C for RW-RESTRUCT, RW-CASEOWN and SY-CASEWF, R for RW-TEAMMGR, and no row for RW-PHONECOL, then confirm at the policy pack review. |

### OTHER:Policy pack PM-2026.12 and reference data load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08939 | RWB-P4-E2026-APP | GAP-0939 | 8 | Add the SY-CASEWF role row with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL, and record it in the reference data load with its own approver. |

### OTHER:FSD S2 (A2.18.2 and A2.15.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08943 | RWB-P4-E2026-APP | GAP-1704 | 11 | Name rwb-document and the P5 and P6 contracts for generation, review and signature in place of the Workbench document hub. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0067 | Wave conflict S9 / EP02 | Tech lead | Resolved (directive) |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0403 | The external partner gateway test route and the partner harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0404 | The WIN dispatch harness pack and the proof-file test window are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0405 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0406 | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | Integration lead | Resolved (directive) |
| GAP-0408 | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1272 | The partner access decision record has no operation, no field composition and no result vocabulary in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1273 | The append path of a partner access record is read synchronously while Arch v5 names it as a consumed event | Solution architect and integration lead | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1278 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1283 | The decision code of a field-capture entry is D6.5 in the legacy metadata but DOCATT on the store path | Business analyst, P7, with the business analyst of P5 rwb-document and the data steward | Resolved (directive) |
| GAP-1284 | No source settles whether an item the store refuses leaves a DOCATT entry | Business analyst, P7, with the P5 business analyst and the integration lead of RWB-ITG-E2024-ITG | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1289 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Solution architect, with the platform team and the P7 rwb-decision owner | Resolved (directive) |
| GAP-1395 | DMZ network design, gateway product, FAPI 2.0 settings, external identity provider, certificate lifecycle, rate limits, WAF rule set and DR target of the partner gateway are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1573 | The joiner, mover and leaver capability has a Must requirement in Epic 2, a feature code in Epic 1 and no legacy story, and its response times are open under DL38 | Business analyst with the security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1852 | Partner identity is a table in rwb_partner while the requirement that governs it is delivered by rwb-access | Security administrator with the P4 and S9 owners | Resolved (directive) |
| GAP-1878 | The treatment-side generation call, its two columns, the merge-field set and the generation event are not specified | Solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
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
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2393 | rwb-comms generation request key and P5 document-create operation are not specified | Service owner, rwb-comms; service owner, rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2394 | Generated-documents endpoint is not in the P6 operation inventory | Architecture owner; service owner, rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2697 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Solution architect | Resolved (directive) |
| GAP-2698 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Solution architect | Resolved (directive) |
| GAP-3147 | EP02 wave 2 for rwb-partner while the service's Architecture v5 wave is 4 | Solution architect | Resolved (directive) |
| GAP-3148 | The rwb-partner slice of the key has no published load path, no message per condition and no partner_user catalogue | Solution architect with the reference data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3181 | The partner_user table is created by P4 in the story and owned by S9 in the ownership map | Access lead with the partner lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3183 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 result file with it | Integration lead with the communications lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
