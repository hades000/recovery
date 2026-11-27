# RWB-SVC-P6 rwb-comms (Communications) - review pack, part 4 of 6 (RWB-P6-E2021-APP to RWB-P6-E2022-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 136 |
| Cross-document (pending in another document) | 169 |
| Not applied (value not in the sources) | 29 |
| Open business decisions | 17 |
| Register gaps linked | 59 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P6-E2021-APP | 30 | 40 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2021 APP Letter dispatch loop with proof of delivery from WIN v2.md |
| RWB-P6-E2021-CON | 24 | 32 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2021 CON Letter dispatch loop with proof of delivery from WIN - contract v2.md |
| RWB-P6-E2021-OPS | 22 | 33 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2021 OPS Letter dispatch loop with proof of delivery from WIN - deployment v2.md |
| RWB-P6-E2022-APP | 22 | 18 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2022 APP SMS and LINE dispatch through NSS and LINE OA v2.md |
| RWB-P6-E2022-CON | 20 | 18 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2022 CON SMS and LINE dispatch through NSS and LINE OA - contract v2.md |
| RWB-P6-E2022-OPS | 18 | 19 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2022 OPS SMS and LINE dispatch through NSS and LINE OA - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P6-E2022-APP | R-01694 | CG-ALL-6587 | Script gap | Product owner | The story adds GET to the closed list LOV-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E2021-APP | R-11056 | CG-ALL-6551 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
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
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1043-CON, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-28792 | GAP-2097 | Register gap | Service owners of P3 rwb-case and P4 rwb-access; business lead | Reference data is read from P4 in TSD P6 and from P3 in the plan default ruling | Follow R3 and DP-07: contact times and frequency are reference data of P3 rwb-case, read through C RWB-P3-E1043-CON. Access data, roles and DoA stay with P4. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-28804 | GAP-2222 | Register gap | Business lead | The legal hold reason list is not stated | Hold the reason list as a reference table of rwb-case loaded by RW-COE; the reason is stored as given until the list is approved. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P6-E2021-APP | R-37271 | ASM-2039 | Register assumption |  | The proof window is 7 calendar days counted from the sent date, and a notice with no proof is Unserved on the first run whose business date is on or after sent_date plus 7 days, which makes a notice sent on 2026-12-15 unserved on the run of 2026-12-22 and a notice sent on 2026-12-16 still Sent on that run. | Business lead and Legal counsel, in the reference-data review that loads the window. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P6-E2021-APP | R-22553 | GAP-1610 | 8 | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | Package name is not in the sources, so it stays a placeholder (GAP-1610). The name cannot be filled without inventing a value. |
| RWB-P6-E2021-APP | R-22561 | GAP-0404 | 16 | The WIN dispatch harness pack and the proof-file test window are not specified | Harness pack, fixture values, window control, result codes, seeding and gate are in no source. Section 16 is not in this chunk, so no placeholder row could be placed. Needs ACE integration and QA agreement. |
| RWB-P6-E2021-APP | R-26067 | CG-ALL-6552 | 3, 3.1 | Flyway file V2021_1__notice_dispatch.sql is not in the V0001..Vnnnn form | Migration name V2021_1 is not in this chunk. Grep found no source giving the next free rwb-comms Flyway number, so none was invented. Needs the service's sequence owner. |
| RWB-P6-E2021-APP | R-28794 | GAP-2095 | 1 | The partner instruction and the internal alert are rows of the design but are not rwb-comms notices in the target | Section 1 is not in this chunk, so the rewrite cannot be placed. Re-issue with section 1: partner instruction as S9 InstructionWorkflow, internal alert as a P3 task. |
| RWB-P6-E2021-APP | R-28796 | GAP-1096 | 14 | The message text of MSG-P6-005 and MSG-P3-005 is not given by the legacy story or the P6 extracts | Texts of MSG-P6-005 and MSG-P3-005 are in no source. Grep found only FSD P3 MSG-P3-005 text, a state-move message with a different meaning. Section 14 is not in this chunk. |
| RWB-P6-E2021-CON | R-06493 | DOR-RWB-P6-E2021-CON-14 | - | Definition of Ready item 14 Epic design: Fail | No signed epic design sign-off found in the story or the .md sources searched; the sign-off cannot be recorded. Needs the epic design record. |
| RWB-P6-E2021-CON | R-22557 | GAP-1089 | - | The WIN dispatch file, its acknowledgement and the INT-15 proof result record have no layout and no owning operation in the sources | WIN file name, layout, acknowledgement fields and proof record are not in the sources (TSD P6 v2 T5.1; Architecture v5 slide 17). Routing via rwb-integration is already in BR8. |
| RWB-P6-E2021-CON | R-22561 | GAP-0404 | - | The WIN dispatch harness pack and the proof-file test window are not specified | Harness fixtures, file-window control, seeding, evidence format and gate are not in the sources; ownership.json gives owners only. Needs ACE integration and QA agreement. |
| RWB-P6-E2021-CON | R-22569 | GAP-1092 | - | The scope test of the notice read has no scope source in the dependencies of this story | No source names a read that returns the notice scope, and the capability area and right codes are not in the sources. Needs the section 12 dependency decision, outside this chunk. |
| RWB-P6-E2021-CON | R-31314 | NEWAC-RWB-P6-E2021-CON-AC13 | 7 | AC13: §8 BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are outside this chunk, so AC13 and its test row cannot be added. The proposed test is not in the sources. |
| RWB-P6-E2021-OPS | R-06497 | DOR-RWB-P6-E2021-OPS-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | Epic design sign-off section is not in the supplied text. Source grep for epic design finds no signed record; no sign-off value written. |
| RWB-P6-E2021-OPS | R-22561 | GAP-0404 | not in chunk | The WIN dispatch harness pack and the proof-file test window are not specified | WIN and INT-15 fixtures, window control, seeding, evidence format and gate values are in no source; they need agreement with ACE integration and QA. |
| RWB-P6-E2021-OPS | R-26084 | CG-ALL-6582 | 7, 12.5, 16 | Criteria and tests keep legacy job and decision-log wording | Remaining legacy wording in AC2, AC3 and AC7 sits in section 7, outside this chunk. Section 12.5 already uses workflow wording; TC-E2-021-06 keeps its source wording. |
| RWB-P6-E2022-APP | R-06502 | DOR-RWB-P6-E2022-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources; sign-off cannot be confirmed without inventing it. |
| RWB-P6-E2022-APP | R-06505 | DOR-RWB-P6-E2022-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded as published in the sources; adding one would invent it. |
| RWB-P6-E2022-APP | R-11068 | CG-ALL-6588 | 4, 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 section 4 has no no-session message; MSG-P4-001 (no-role sign-in) and MSG-P4-005 (MFA) do not fit. Placeholder stays for the Business analyst. |
| RWB-P6-E2022-APP | R-17681 | DOR-RWB-P6-E2022-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | No empty, loading, error or no-access text for SCR-03, SCR-04, SCR-09 in the PRD set; adding it would invent text. Section 9 text is not in this chunk. |
| RWB-P6-E2022-APP | R-17684 | DOR-RWB-P6-E2022-APP-18 |  | Definition of Ready item 18 Open decisions: Partial | Open-decisions section is not in this chunk, so DL30 has no anchor; ASM-2022 and ASM-3378 wording is not in the story text. |
| RWB-P6-E2022-APP | R-22570 | GAP-2321 |  | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Masking label, covered field IDs, AC-READ granularity, parameter defaults and login name are Compliance and steward values not in sources. Owners: Solution architect, rwb-access contract owner. |
| RWB-P6-E2022-APP | R-22575 | GAP-0405 | 3, 12.8, 13 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Test doubles, harness, seeding and evidence gate are not in the sources; they need ACE team and QA agreement (owner Integration lead). Placeholders stay. |
| RWB-P6-E2022-APP | R-26091 | CG-ALL-6593 | 3 | Flyway file V2022_1__message_dispatch.sql is not in the V0001..Vnnnn form | Next free rwb-comms Flyway number is not in the sources. Service Template Spec v1 (sec 3.1, 6.2) gives only V0001 baseline and V0001 to Vnnnn. Line 346 is outside this chunk. |
| RWB-P6-E2022-CON | R-17689 | DOR-RWB-P6-E2022-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Coverage needs new AC rows in section 7 and TC rows in section 16, which are outside this chunk. New IDs cannot be numbered without their text. |
| RWB-P6-E2022-CON | R-22575 | GAP-0405 | 3; 12.8; 13 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Test doubles, result codes, harness, seeding, evidence and gate are in no source. Placeholders stay until the ACE notification team and QA agree them. |
| RWB-P6-E2022-CON | R-26096 | CG-ALL-6600 | 16 | Test cases cover other criteria in Test Cases v8 | No criteria AC10 to AC12 exist in section 7; the v8 mapping for those rows cannot be applied. |
| RWB-P6-E2022-CON | R-28807 | GAP-1073 | 11; 12 | The MessageRequest and Interaction field-level definitions are not specified | Interaction field text is in section 12, outside this chunk. Types, lengths and optionality are in no source, so no value can be written. Settle at baseline review. |
| RWB-P6-E2022-CON | R-31322 | NEWAC-RWB-P6-E2022-CON-AC10 | 8 | AC10: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14, BR15, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Adding the AC needs the current text of section 7 (anchor and numbering) and section 16 (test row), which this chunk does not include. Not edited; send those parts. |
| RWB-P6-E2022-OPS | R-22575 | GAP-0405 | 3, 12.8, 13 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Test doubles, harness, seeding, evidence format and gate need agreement with ACE team and QA; sources give owners only (ownership.json). Placeholders stay; owner Integration lead. |
| RWB-P6-E2022-OPS | R-26102 | CG-ALL-6607 | 16 | Test cases cover other criteria in Test Cases v8 | AC9 to AC12 do not exist in section 7 and the new values conflicted with the BR Covered-by column; Test Cases v8 alignment is not confirmed. |
| RWB-P6-E2022-OPS | R-31323 | NEWAC-RWB-P6-E2022-OPS-AC9 | 8 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | A new AC9 needs a proposed test the sources do not give (Not specified in the source documents); section 7 and 16 text was not supplied, so no edit is made. |

## 5. Cross-document changes (pending in the target document)


### RWB-P6-E2021-CON (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11103 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-21 | - | Build RWB-P6-E2021-CON to Done and publish the contract; its build status is currently Not started. |
| CDC-11104 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-22 | - | Publish a contract fake library version and record it as published. |
| CDC-11120 | RWB-P6-E2021-APP | GAP-1089 | 12.2 | Fix the WIN dispatch file name, record layout, acknowledgement fields and the INT-15 proof result record with the WIN owner and the rwb-integration owner, and publish them in RWB-P6-E2021-CON; the proof read now goes through P1 per GAP-2096. |
| CDC-11124 | RWB-P6-E2021-APP | GAP-1095 | find it | Publish the handoff row: the Airflow WIN window signals the rwb-comms Schedule with the business date; the run records the date; a rerun of the same date writes no second file. |
| CDC-11128 | RWB-P6-E2021-APP | GAP-1092 | find it | Declare the capability area and right per operation; gateway-bff asks rwb-access (DP-08) before the call; scope is served from the rwb-case case read. |
| CDC-11133 | RWB-P6-E2021-APP | GAP-1094 | find it | Define the Notice component with id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus, sentType, holdReason, dispatchFileId and dispatchAttempts; id and caseId required, the rest optional; validate the additive rule against the RWB-P6-E1052-CON Notice. |
| CDC-11168 | RWB-P6-E2021-CON | GAP-2095 | 1 | Section 1 (outside chunk c05): record the partner instruction as S9 InstructionWorkflow and the internal alert as a P3 task; rwb-comms keeps only the partner instruction template |
| CDC-11172 | RWB-P6-E2021-OPS | DOR-RWB-P6-E2021-OPS-21 | header | Move build status from Not started to Done once the contract is published; the dependency is now recorded in the header. |
| CDC-11173 | RWB-P6-E2021-OPS | DOR-RWB-P6-E2021-OPS-22 |  | Publish a contract fake library version and record it as published. |
| CDC-11183 | RWB-P6-E2021-OPS | GAP-1089 | header | Fix the INT-14 file name, record layout, acknowledgement fields and INT-15 proof result record with the WIN and rwb-integration owners, and publish them in this contract. Header dependency row now cites GAP-1089. |
| CDC-11187 | RWB-P6-E2021-OPS | GAP-1095 | not in chunk | Agree the Airflow-to-Schedule handoff with the Airflow owner: the window signals the rwb-comms Schedule with the business date, the run records the date, and a rerun of the same date writes no second file. Publish the row. |
| CDC-11192 | RWB-P6-E2021-OPS | GAP-1092 | find it | Declare the capability area and the right per operation; gateway-bff asks rwb-access (DP-08) before the call; serve scope from the rwb-case case read or add C RWB-P4-E1037-CON |
| CDC-11198 | RWB-P6-E2021-OPS | GAP-1094 |  | Fix the Notice component fields (nine legacy fields plus holdReason, dispatchFileId, dispatchAttempts), all optional except id and caseId, and validate against RWB-P6-E1052-CON Notice. |

### RWB-P1-E1066-CON (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11117 | RWB-P6-E2021-APP | GAP-2096 | 12 | Proof rows are read through the P1 contract; read timing removed from the story. |
| CDC-11132 | RWB-P6-E2021-APP | GAP-2182 | find it | Settle one path family for the interaction ledger, covering append and the case read in case_seq order, keep the case-scoped form, and realign the fake in RWB-P6-E2021-CON and the consumed row in RWB-P3-E2021-APP to it. |
| CDC-11167 | RWB-P6-E2021-CON | GAP-2182 | 12.1, 12.2 | Settle one path family for the interaction ledger (append and case-ordered read); then realign the faked ledger write in 12.2 of RWB-P6-E2021-CON and the consumed row of RWB-P3-E2021-APP |
| CDC-11196 | RWB-P6-E2021-OPS | GAP-2182 |  | Settle one path family for the interaction ledger, keep the case-scoped form, and realign the fake in RWB-P6-E2021-CON and the consumed row in RWB-P3-E2021-APP to it. |
| CDC-11209 | RWB-P6-E2022-APP | GAP-1070 | 8 | Name the contact-point read, consent and verified fields, failed-count update, and ledger record and delivery-update operations, or add a P1 ledger contract to Contract dependencies. |
| CDC-11211 | RWB-P6-E2022-APP | GAP-1605 |  | Expose contact point read, consent state, verification write and failed-count read through the rwb-source-data contract; rwb-comms keeps enforcement. |
| CDC-11216 | RWB-P6-E2022-APP | GAP-1599 |  | Carry channel, direction, conduct check, delivery status and channel reference on the interaction ledger entry; add no fourth rwb_comms table. |
| CDC-11225 | RWB-P6-E2022-CON | GAP-1070 | find it | Name the contact-point read, the consent and verified fields, the failed-count update, and the ledger record and delivery-update operations, or add a P1 ledger contract to this key's Contract dependencies. |
| CDC-11227 | RWB-P6-E2022-CON | GAP-1605 | find it | Expose the contact point read, its consent state and failed count, and the verification and consent change writes through the rwb-source-data contract; enforcement stays in rwb-comms. |
| CDC-11247 | RWB-P6-E2022-OPS | GAP-1070 | header | Name the contact-point read, consent and verified fields, failed-count update, and ledger record and delivery-update operations, or add a P1 ledger contract to this key's Contract dependencies. |
| CDC-11249 | RWB-P6-E2022-OPS | GAP-1605 | header | Expose read of contact point, consent state and failed count, and write of verification and consent change, to rwb-comms through the rwb-source-data contract. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11114 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-12 | 16 | Align per-requirement test lists with section 16 of this story (TC-01 to TC-25) |
| CDC-11130 | RWB-P6-E2021-APP | CG-ALL-6550 | 18 | Align the test lists for the four requirements with section 18 of this story in the next version of the RTM. |
| CDC-11165 | RWB-P6-E2021-CON | CG-ALL-6569 | 18 | Align the test lists of REQ-OCC-003, REQ-OCC-005 and the other listed requirements in the RTM's next version with RWB-P6-E2021-CON section 18 |
| CDC-11194 | RWB-P6-E2021-OPS | CG-ALL-6581 | 18 | Trace REQ-OCC-003 and REQ-OCC-005 to the TC-P6-E2021-OPS IDs listed in section 18 of this story; remove the legacy TC-E1 and TC-E2 entries against this story |
| CDC-11208 | RWB-P6-E2022-APP | DOR-RWB-P6-E2022-APP-12 | 12, 12.7, 16, 18 | Align the test lists for RWB-E2-022 rows with section 16 and remove TC lists for criteria this story does not own (AC1, AC3, AC5, AC6, AC7, AC10, AC12). |
| CDC-11219 | RWB-P6-E2022-APP | CG-ALL-6592 | 18 | In the next RTM version, align the test lists of REQ-OCC-004, REQ-OCC-005 and the other requirements listed in CG-ALL-6592 with section 18 of RWB-P6-E2022-APP |
| CDC-11223 | RWB-P6-E2022-CON | DOR-RWB-P6-E2022-CON-12 | 12.7, 16, 18 | Align the RWB-E2-022 test lists with section 18 of RWB-P6-E2022-CON, which now lists TC-E2-022-15 and TC-E2-022-16. |
| CDC-11238 | RWB-P6-E2022-CON | CG-ALL-6602 | 18 | REQ-OCC-004 row restored to its prior test list |
| CDC-11256 | RWB-P6-E2022-OPS | CG-ALL-6609 | 18 | Align the test lists for REQ-OCC-004 and REQ-OCC-005 with RWB-P6-E2022-OPS section 18 in the next RTM version; the TC-E2-021 IDs cited there are outside this story. |

### RWB-P6-E2022-CON (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11206 | RWB-P6-E2022-APP | DOR-RWB-P6-E2022-APP-21 | header | Build status moved from Not started to Done once the contract is published. |
| CDC-11217 | RWB-P6-E2022-APP | GAP-2183 | find it | Publish the contact-point read and the failed-count operation and the InteractionLedgerApi.updateDelivery extension in the P1 API appendix within the RWB-P6-E2022-CON baseline, and confirm the open details at contract review |
| CDC-11221 | RWB-P6-E2022-APP | GAP-1073 | find it | Fix the MessageRequest and Interaction names and their two closed value lists in the baseline, and settle lengths, formats and optionality at the baseline review |
| CDC-11222 | RWB-P6-E2022-APP | GAP-1076 | 9 | Hold the message status list as its own list with SENT, DELIVERED, FAILED and READ; leave LOV-DELIVERY to the notice and proof-of-delivery capability. Data steward confirms or names the list. |
| CDC-11242 | RWB-P6-E2022-OPS | DOR-RWB-P6-E2022-OPS-21 | header | Set build status to Done and publish the contract. Story Contract dependencies row now names it. |
| CDC-11243 | RWB-P6-E2022-OPS | DOR-RWB-P6-E2022-OPS-22 | header | Publish a contract fake library version and record it. |
| CDC-11244 | RWB-P6-E2022-OPS | DOR-RWB-P6-E2022-OPS-23 | header | Fix and record the contract version this story builds against. |
| CDC-11258 | RWB-P6-E2022-OPS | GAP-1073 | find it | Fix the MessageRequest and Interaction field names, the channel and language value lists, and the required and defaulted properties; lengths, formats and optionality stay Not specified until the baseline review. |
| CDC-11259 | RWB-P6-E2022-OPS | GAP-1076 | find it | Hold the message status list SENT, DELIVERED, FAILED and READ as its own list; leave LOV-DELIVERY to the notice and proof-of-delivery capability; data steward confirms. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11100 | RWB-P6-E2021-APP | CG-ALL-6539 | - | Remove the closed enum on deliveryStatus so LOV-DELIVERY values are accepted as data, as the story (line 52) states. |
| CDC-11101 | RWB-P6-E2021-APP | CG-ALL-6540 | - | Remove the closed enum on sentType so LOV-SENT-TYPE values are accepted as data, as the story (line 52) states. |
| CDC-11205 | RWB-P6-E2022-APP | CG-ALL-6589 | header | Remove the fixed enum on deliveryStatus so LOV-DELIVERY values are accepted as data without a code change. |
| CDC-11207 | RWB-P6-E2022-APP | DOR-RWB-P6-E2022-APP-8 | 12.1, 12.3 | Remove the fixed enum on deliveryStatus (see CG-ALL-6589). The 401 mapping and event type are fixed in the story. |
| CDC-20786 | RWB-P6-E2022-APP | R-01695 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20788 | RWB-P6-E2021-APP | R-01690 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20789 | RWB-P6-E2022-APP | R-06508 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20790 | RWB-P6-E2021-APP | R-01689 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11107 | RWB-P6-E2021-APP | CG-ALL-6538 | 12.1 | Add or confirm a message ID for 401 no session so story section 12.1 Errors can cite it. |
| CDC-11111 | RWB-P6-E2021-APP | CG-ALL-6547 | 14 | Add a new message ID for the template-not-approved case, not MSG-P6-005; story then cites it in 12.1 and 14. |
| CDC-11112 | RWB-P6-E2021-APP | CG-ALL-6548 | 14 | Add a new message ID for the notice-already-in-progress case, not MSG-P3-005; story then cites it in 12.1 and 14. |
| CDC-11147 | RWB-P6-E2021-CON | CG-ALL-6564 | 4, 14 | Add a new message ID for 'The request could not be read: {detail}.' (schema validation); the story then cites it |
| CDC-11148 | RWB-P6-E2021-CON | CG-ALL-6565 | 4, 14 | Add a new message ID for 'The template of the notice is not approved'; its text is Not specified in the source documents (GAP-1096; ASM-2044) |
| CDC-11149 | RWB-P6-E2021-CON | CG-ALL-6566 | 4, 14 | Add a new message ID for 'A notice of this type is already in progress for the case'; its text is Not specified in the source documents (GAP-1096; ASM-2044) |
| CDC-11153 | RWB-P6-E2021-CON | DOR-RWB-P6-E2021-CON-9 Messages: Partial | 14 | Schema-validation row of MSG-P3-030 restored with its original text |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11108 | RWB-P6-E2021-APP | CG-ALL-6544 | 12.5 | Add an Activities row for generateLetter: type Activity, in rwb-document, task queue rwb-document. |
| CDC-11109 | RWB-P6-E2021-APP | CG-ALL-6545 | 12.5 | Add an Activities row for conductCheck: type Activity, in rwb-comms, task queue rwb-comms. |
| CDC-11110 | RWB-P6-E2021-APP | CG-ALL-6546 | 12.5 | Add an Activities row for recordDecision: type Activity, in rwb-comms through the library, task queue rwb-comms. |
| CDC-11144 | RWB-P6-E2021-CON | CG-ALL-6561 | 12.5 | Add an Activity row for conductCheck with task queue rwb-comms, as named in section 12.5. |
| CDC-11176 | RWB-P6-E2021-OPS | CG-ALL-6578 | 12.5 | Add activity generateLetter (owner rwb-document, task queue rwb-document) so the catalogue matches story section 12.5. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11135 | RWB-P6-E2021-APP | GAP-1090 |  | Assign REC-05 to the rwb-source-data reconciliation story (JOB-04) with the notice break count and its series. |
| CDC-11154 | RWB-P6-E2021-CON | GAP-2096 | 11 | Add EV-15 NoticeDelivered produced by rwb-comms on proof match by barcode to the event catalogue (slide 42), and map the read to the P1 contract batch on the ACE business date to the job map (slide 44). |
| CDC-11155 | RWB-P6-E2021-CON | GAP-2093 |  | Replace 'Decision: child: approval' in the slide 17 P6 OUT list with approval held in P7 ApprovalWorkflow as a child of NoticeDispatchWorkflow, with POST /notices/{noticeId}/approve of S4 as the decision point. The approved notice is not written to the file. |
| CDC-11197 | RWB-P6-E2021-OPS | GAP-2095 |  | Record the partner instruction as S9 InstructionWorkflow and the internal alert as a P3 task; rwb-comms keeps only the partner instruction template. |
| CDC-11230 | RWB-P6-E2022-CON | GAP-1071 |  | Count JOB-11 as one send attempt of the message capability per relay window; exclude the path's internal retries from the count; platform relay owner confirms window semantics. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11150 | RWB-P6-E2021-CON | DOR-RWB-P6-E2021-CON-1 | 1 | Add or confirm a role code or name for the tech lead of rwb-comms, the role §1 names |
| CDC-11177 | RWB-P6-E2021-OPS | DOR-RWB-P6-E2021-OPS-1 | 1 | Register 'platform engineer' as a role code or role name, or name the role already in use for the section 1 persona. |
| CDC-11220 | RWB-P6-E2022-APP | GAP-0956 | find it | Record the JOB-11 service identity and the platform service identities with class and scope in the role table, and add decision codes for a send and a refused send to the ledger decision-code list |
| CDC-11245 | RWB-P6-E2022-OPS | DOR-RWB-P6-E2022-OPS-1 | 1 | Confirm or add 'platform engineer' as a role code or name, or confirm the role §1 should use. |

### RWB-P1-E1016-CON; RWB-P1-E1066-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11119 | RWB-P6-E2021-APP | GAP-2181 | 11, 12.2 | Publish the DP02 contact-and-consent row and its vocabulary in RWB-P1-E1016-CON; add the required-members table of the LETTER append to RWB-P1-E1066-CON; add UNSERVED to LOV-SEND-STATUS with its version, or confirm the FAILED mapping with the ACE result code in source_ref. |
| CDC-11156 | RWB-P6-E2021-CON | GAP-2181 | 12.1, 13 | Publish the DP02 contact-and-consent row and its vocabulary in RWB-P1-E1016-CON; add the required-members table of the LETTER append to RWB-P1-E1066-CON; add UNSERVED to LOV-SEND-STATUS with its version, or confirm the FAILED mapping with the ACE result code in source_ref. |
| CDC-11182 | RWB-P6-E2021-OPS | GAP-2181 | not in chunk | Publish the DP02 contact-and-consent row and its vocabulary (GIVEN, WITHDRAWN, UNKNOWN) in E1016; add the LETTER append required-members table in E1066; add UNSERVED to LOV-SEND-STATUS with version or confirm FAILED mapping. |

### RWB-P4-AD002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11122 | RWB-P6-E2021-APP | GAP-0948 | not in chunk | Add the JOB-10 runner as NON_HUMAN_ACTOR, scope ALL, with a Litigation R row. Role code: Not specified in the source documents (GAP-0948). |
| CDC-11184 | RWB-P6-E2021-OPS | GAP-0945 | not in chunk | Add the Litigation column for each role the legacy authority table names; publish the full 14-area matrix as data; confirm C and R letters with the matrix owner. |
| CDC-11185 | RWB-P6-E2021-OPS | GAP-0948 | not in chunk | Name the JOB-10 runner service identity in the role table with role class NON_HUMAN_ACTOR, scope ALL and its Litigation R row, and load it in the policy pack. |

### RWB-P6-E2021-OPS (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11136 | RWB-P6-E2021-APP | GAP-1093 |  | Set slot and replica counts in the values files once DL35 is decided; confirm the six alert thresholds at UAT and record them in the runbook entries. |
| CDC-11170 | RWB-P6-E2021-CON | GAP-1093 | header | Record deployment slot and replica counts in the values files once DL35 is decided; confirm the six alert thresholds at UAT and record them in each runbook entry. |
| CDC-11204 | RWB-P6-E2021-OPS | GAP-1277 | header | Carry the platform H dependencies, the published C dependency and the two service baselines in the header dependency rows. Dependency map rows DP-07, DP-09, DP-10 and DP-19 already carry them. Keep Ready to start = Day 1. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11138 | RWB-P6-E2021-APP | GAP-2219 |  | Allocate a key for the rwb-case slice flag at first build, alongside rwb.comms.win-dispatch-loop. |
| CDC-11171 | RWB-P6-E2021-CON | GAP-2219 | 13 | Allocate a key for the rwb-case dispatch-loop switch (hold, ledger facts, task) at the first build, alongside rwb.comms.win-dispatch-loop. |
| CDC-11203 | RWB-P6-E2021-OPS | GAP-2219 | 7 | Allocate the key for the rwb-case case-side flag at the first build; value Not specified in the source documents (GAP-2219). |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11102 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-14 | - | Record the signed epic design sign-off for the epic that this story sits in. |
| CDC-11241 | RWB-P6-E2022-OPS | DOR-RWB-P6-E2022-OPS-14 | none | Record the signed epic design sign-off for RWB-P6-E2022-OPS. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11123 | RWB-P6-E2021-APP | GAP-0946 | not in chunk | Add POST /authorise with the request fields and answer fields listed in the item, publish with RWB-P4-E1037-CON, stub it in that contract fake, and add the access decision codes to the ledger code list. |
| CDC-11159 | RWB-P6-E2021-CON | GAP-0946 |  | Add POST /authorise with its request and answer schema, publish with RWB-P4-E1037-CON, stub it in the contract fake, and add the access entry decision codes to the ledger code list. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11127 | RWB-P6-E2021-APP | GAP-3183 | find it | Name the delivery result event and its topic; delete the JOB-09 loader from the Epic 2 story set. |
| CDC-11191 | RWB-P6-E2021-OPS | GAP-3183 | find it | Name the delivery result event and its topic in the next Event and Messaging version; delete the JOB-09 loader from the Epic 2 story set. Owner: Integration lead with the communications lead |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11145 | RWB-P6-E2021-CON | CG-ALL-6562 | 12.5 | Add activity generateLetter, owner rwb-document, task queue rwb-document, or use a catalogued activity |
| CDC-11146 | RWB-P6-E2021-CON | CG-ALL-6563 | 12.5 | Add activity recordDecision, task queue rwb-comms, or use a catalogued activity |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11152 | RWB-P6-E2021-CON | DOR-RWB-P6-E2021-CON-12 | 12.7, 16, 18 | Add TC-P6-E2021-CON-01 to -13 to Test Cases v8; align the §18 test lists with RTM v7; re-assign legacy cases TC-E2-021-01 to -14 to the stories owning their criteria |
| CDC-11179 | RWB-P6-E2021-OPS | DOR-RWB-P6-E2021-OPS-12 | 12, 16, 18 | Add TC-P6-E2021-OPS-01 to -09 and -10 rows to Test Cases v8; reconcile the section 18 test lists with RTM v7. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11164 | RWB-P6-E2021-CON | CG-ALL-6567 | 16 | Add rows TC-P6-E2021-CON-01 to TC-P6-E2021-CON-08 with Given, When and Then copied from the criterion each covers. |
| CDC-11193 | RWB-P6-E2021-OPS | CG-ALL-6579 | 16 | Add rows TC-P6-E2021-OPS-01 to TC-P6-E2021-OPS-09 with Given, When and Then copied from the criterion each covers |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11166 | RWB-P6-E2021-CON | GAP-2094 | 12.1 | Add GET /cases/{id}/notices as a P6 operation, settled in the P6 API specification; until then read a case's notices through GET /notices/{noticeId} per notice |
| CDC-11195 | RWB-P6-E2021-OPS | GAP-2094 |  | Publish the case-level list GET /cases/{id}/notices as a P6 operation with its path settled. Until then, read a case's notices through GET /notices/{noticeId} per notice. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11174 | RWB-P6-E2021-OPS | CG-ALL-6576 | 12.5 | Add activity conductCheck for rwb-comms on task queue rwb-comms, or name a catalogued activity in the story. |
| CDC-11175 | RWB-P6-E2021-OPS | CG-ALL-6577 | 12.5 | Add activity recordDecision for rwb-comms on task queue rwb-comms, or name a catalogued activity in the story. |

### RWB-P4-E1037-CON; RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11218 | RWB-P6-E2022-APP | GAP-0955 | find it | Publish the authorise, me-permissions and masking-policies shapes in RWB-P4-E1037-CON, and the SCR-03 composite field list in RWB-PLT-N001-CON, before the send story is built |
| CDC-11255 | RWB-P6-E2022-OPS | GAP-0955 | header | Publish the authorise, me-permissions and masking-policies shapes, and the composite route field list for SCR-03 and SCR-04, before the send story is built. |

### OTHER:ACE notification path contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11229 | RWB-P6-E2022-CON | GAP-1069 | find it | Publish the NSS and LINE OA request and result contract with the result-code maps before the wave 2 SIT entry. |
| CDC-11231 | RWB-P6-E2022-CON | GAP-1072 |  | State the result transport for NSS and LINE OA (callback or poll); rwb-comms applies a result only for a known external reference; an unknown reference is not applied. |

### OTHER:TSD P6 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11234 | RWB-P6-E2022-CON | GAP-1078 |  | Declare SCR-09 Exception queue as a P6 administrative read over outbox rows in the exception state, or a P3 queue fed by a P6 event; declare the owner before the screen is built. |
| CDC-11248 | RWB-P6-E2022-OPS | GAP-1075 | header | Declare Case record right C on the gateway-bff composite route to SCR-03 with refusals MSG-P4-002 and MSG-P4-003; record reconciliation of the Case record area in T6.1. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20825 | RWB-P6-E2021-CON | R-22565 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09171', 'R-16120', 'R-22565'] |
| CDC-20855 | RWB-P6-E2021-OPS | R-22565 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09171', 'R-22565', 'R-28487'] |

### OTHER:rwb-integration interface definition for INT-14 (WIN dispatch file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11105 | RWB-P6-E2021-APP | GAP-1602 | 4 | Define the WIN dispatch file layout (record set, fields, order, envelope, naming, encoding, barcode and sent date return) as a versioned interface contract item before wave 2. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11106 | RWB-P6-E2021-APP | CG-ALL-6537 | 11 | Confirm the dictionary name for the party field of notice (DF-LEG-030) or record party_id as an object in LDM v9; story then uses that name. |

### OTHER:P3 screen specification for SCR-04; OTHER:SCR-18 and SCR-44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11113 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-10 | none | Add empty, loading, error and no-access states to SCR-04, SCR-18 and SCR-44 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11115 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-7 | 7, 16 | Add party_id (notice, DF-LEG-030) as a field, or confirm it as a key to rwb-source-data's party |

### OTHER:Message catalogue (standard for MSG-P6-005 and MSG-P3-005) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11116 | RWB-P6-E2021-APP | DOR-RWB-P6-E2021-APP-9 | 14 | Publish or confirm the text and meaning of MSG-P6-005 and MSG-P3-005, or retire their use here |

### RWB-S4-E5002-CON; RWB-P6-E2021-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:P6 and S4 appendices; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11118 | RWB-P6-E2021-APP | GAP-0437 | 12 | Publish the proof-record operation on RWB-S4-E5002-CON and the notice proof write on the rwb-comms baseline; add the notice state and the three case notice facts to the LDM with field IDs; fix the LOV-DELIVERY mapping and the period and window reference rows; record in the P6 and S4 appendices that the v_ace_pod loop is the Epic 2 dispatch story; attach the requirement ID to FEAT-LIT-02 in the EP05 PRD. |

### OTHER:TSD P4 RBAC matrix, table T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11121 | RWB-P6-E2021-APP | GAP-0945 | not in chunk | Add a Litigation column for every role that legacy RWB-E2-021 section 10 names, publish the 14-area matrix as data with RWB-P4-AD002-APP, and confirm the C and R letters with the matrix owner. |

### OTHER:Published rwb-source-data and rwb-decision REST contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11125 | RWB-P6-E2021-APP | GAP-2220 | find it | Publish operation names and paths for InteractionLedgerApi.record and DecisionLogApi.write under /api/recovery/source-data/v1 and /api/recovery/decision/v1. |

### OTHER:Technical Solution Design P3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11126 | RWB-P6-E2021-APP | GAP-2221 | find it | Remove interaction from the P3 module object list; the ledger is owned by rwb-source-data and rwb-case holds no interaction table, view or foreign key. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11129 | RWB-P6-E2021-APP | GAP-1132 | find it | Publish NoticeDelivered on first delivery of a notice, WIN or digital, reusing the RWB-P6-E1055-CON element with channel added; state the once-per-notice rule. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:P6 rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11131 | RWB-P6-E2021-APP | GAP-2094 | find it | Add the case-level notice list GET /cases/{caseId}/notices for P6 rwb-comms and settle its path in the P6 API specification; until then read a case's notices through GET /notices/{noticeId} per notice. |

### OTHER:FSD P4 v3 (A2.7) and gateway-bff composite route field list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11134 | RWB-P6-E2021-APP | GAP-0947 |  | Publish the masking version in force per environment, the addressee postal address and party field IDs with mask format, and the SCR-18 and SCR-04 composite route field list. |

### OTHER:WP B2-P3-007 story line (rwb-case slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11137 | RWB-P6-E2021-APP | GAP-2217 |  | Keep legacy AC1 to AC12 with RWB-P6-E2021-APP and write the nine case-side criteria in the rwb-case story. |

### OTHER:FSD P6 Communications, next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11139 | RWB-P6-E2021-APP | GAP-1194 |  | Record that the officer-recorded path of this story is the manual correction path of the same notice, and keep the automatic v_ace_pod read in RWB-P6-E2021-APP and RWB-P6-E1055-APP. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11140 | RWB-P6-E2021-CON | CG-ALL-6558 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations with query parameter caseId, or the story consumes a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11141 | RWB-P6-E2021-CON | DOR-RWB-P6-E2021-CON-8 | 12.3, 12.5 | Publish the deviations GET path in rwb-deviation.yaml; add activity conductCheck to Temporal Catalog v1 Activities. |

### OTHER:Gap register (GAP-1608 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11142 | RWB-P6-E2021-CON | GAP-1608 | find it | Record the feature-flag hold on proof-of-delivery capture until RWB-ACE-001 lands and v_ace_pod is available, with the hand-entry fallback against the barcode. |

### OTHER:rwb-integration interface definition (INT-14 dispatch file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11143 | RWB-P6-E2021-CON | GAP-1602 | 12.2 | Hold the WIN dispatch file layout as a versioned contract item before wave 2. |

### OTHER:Recovery Workbench P3 screen specification (SCR-04; OTHER:SCR-18; OTHER:SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11151 | RWB-P6-E2021-CON | DOR-RWB-P6-E2021-CON-10 | find it | Add the empty, loading, error and no access states for SCR-04, SCR-18 and SCR-44 |

### OTHER:TSD P4 RBAC matrix (T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11157 | RWB-P6-E2021-CON | GAP-0945 |  | Add a Litigation column for each role the legacy authority table names; publish the full 14-area matrix version as data with RWB-P4-AD002-APP; confirm the C and R letters with the matrix owner before the pack goes in force. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11158 | RWB-P6-E2021-CON | GAP-0948 |  | Name the JOB-10 runner service identity with role class NON_HUMAN_ACTOR, scope ALL and its Litigation R row. Role code: Not specified in the source documents (GAP-0948). |

### OTHER:SERVICE_LEVEL reference table (timer table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11160 | RWB-P6-E2021-CON | GAP-2218 |  | Load the row for task NOTICE_UNSERVED with its case owner role and due date before wave 2 starts. |

### OTHER:rwb-source-data and rwb-decision contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11161 | RWB-P6-E2021-CON | GAP-2220 |  | Take the ledger and decision-record operation names and paths from the published contracts. REST bases: /api/recovery/source-data/v1 and /api/recovery/decision/v1. |

### OTHER:TSD P3 section T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11162 | RWB-P6-E2021-CON | GAP-2221 |  | Show the interaction ledger as owned by rwb-source-data, not the P3 module; rwb-case reads and writes it only through that contract. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:Epic 2 story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11163 | RWB-P6-E2021-CON | GAP-3183 |  | Name the INT-15 delivery result event and its topic. Delete the JOB-09 loader from the Epic 2 story set, as JOB-09 is retired under D-RCV-35. |

### OTHER:gateway-bff composite route field list (DP-19); OTHER:Recovery Workbench data dictionary; OTHER:policy pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11169 | RWB-P6-E2021-CON | GAP-0947 | 8 | Publish the masking version in force for SIT (MASK-SIT-01 assumed), the field IDs of the addressee postal address and second party field with mask format, and the SCR-18/SCR-04 composite field list. |

### OTHER:Recovery Workbench Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11178 | RWB-P6-E2021-OPS | DOR-RWB-P6-E2021-OPS-10 | 9 | Define empty, loading, error and no access states for SCR-04, SCR-18 and SCR-44 (none present in the source). |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities and Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11180 | RWB-P6-E2021-OPS | DOR-RWB-P6-E2021-OPS-8 | 12.5 | Add activities conductCheck, recordDecision and generateLetter; state the NoticeDispatchWorkflow workflow ID form and start rule. |

### OTHER:rwb-decision rule package (conduct and consent rule set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11181 | RWB-P6-E2021-OPS | GAP-1610 | not in chunk | Publish the versioned conduct and consent rule package with requirement IDs, governed in rwb-decision, approved as first version by the conduct and QA officer. Then name it in the story. |

### RWB-P4-E1037-CON; OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11186 | RWB-P6-E2021-OPS | GAP-0946 | not in chunk | Add the POST /authorise path with request and answer schema, stub it in the contract fake, and add the access entry decision codes to the ledger code list. |

### OTHER:Recovery Workbench FSD P3 timer table (SERVICE_LEVEL reference row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11188 | RWB-P6-E2021-OPS | GAP-2218 | find it | Hold task code NOTICE_UNSERVED, case owner role and due date from the SERVICE_LEVEL reference row; load the row before the wave starts. Owner: Business analyst, P3 |

### OTHER:Published rwb-source-data and rwb-decision contracts and their fakes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11189 | RWB-P6-E2021-OPS | GAP-2220 | find it | Publish operation names and paths for InteractionLedgerApi.record and DecisionLogApi.write under REST bases /api/recovery/source-data/v1 and /api/recovery/decision/v1 |

### OTHER:Recovery Workbench TSD P3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11190 | RWB-P6-E2021-OPS | GAP-2221 | find it | Remove interaction from the P3 object list (T3.1); the ledger stays with rwb-source-data, and rwb-case reads and writes it only through that contract, with no table, view or foreign key |

### RWB-P6-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11199 | RWB-P6-E2021-OPS | GAP-1096 | 14 | Publish the texts of MSG-P6-005 and MSG-P3-005, then copy them unchanged into section 14. Until then use Not specified in the source documents (GAP-1096). |

### OTHER:Policy pack load (SIT masking version), data dictionary (DF-PTY addressee and party field IDs) and gateway-bff composite (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11200 | RWB-P6-E2021-OPS | GAP-0947 |  | Fix the masking version in force in SIT, publish the postal address and party field IDs with mask format, and publish the SCR-18 and SCR-04 composite route field list. |

### OTHER:rwb-source-data reconciliation story (JOB-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11201 | RWB-P6-E2021-OPS | GAP-1090 |  | Assign REC-05 to the rwb-source-data reconciliation story with the notice break count and its series. Until then the proof-window series and unacknowledged-file alert stand in. |

### OTHER:FSD P6 (AC-ALT-P6-001-01 and AC-ALT-P6-001-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11202 | RWB-P6-E2021-OPS | GAP-1609 | 7 | Restate the NOTICE_PERIOD timer as started by rwb-case on NoticeDelivered from the callback date, and the NOTICE_UNSERVED transfer as a call to rwb-case's transfer operation; no timer in rwb-comms. |

### OTHER:Recovery Workbench TSD P6 and story pattern set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11210 | RWB-P6-E2022-APP | GAP-1075 | 10 | Add a Case record area row to TSD P6 T6.1 and record its reconciliation; add DP08 to the key pattern set and declare the rwb-access dependency. |

### OTHER:TSD P4 v3 T6.1 role-to-permission matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11212 | RWB-P6-E2022-APP | GAP-0953 |  | Add the Case record column and the other decided capability areas; load the letters as PM-2026.12 rows. |

### OTHER:ACE notification path contract (INT-17; OTHER:INT-18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11213 | RWB-P6-E2022-APP | GAP-1069 | 12.8 | Publish the request, accepted-reference, result and callback contract with NSS and LINE OA result-code maps before wave 2 SIT. |

### OTHER:ACE notification path contract (INT-18 LINE OA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11214 | RWB-P6-E2022-APP | GAP-1072 |  | State the result transport for NSS and LINE OA; rwb-comms accepts a callback or poll for a known external reference and does not apply an unknown reference. |

### OTHER:TSD P6 T5.1 INT-17 and INT-18; OTHER:platform secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11215 | RWB-P6-E2022-APP | GAP-1074 |  | Publish endpoint, certificate issuer, secret names and egress timeout; the chart carries references only and the egress check fails a release with a missing reference. |

### RWB-P6-E2022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11224 | RWB-P6-E2022-CON | DOR-RWB-P6-E2022-CON-10 | 9 | Add empty, loading, error and no access states for SCR-03, SCR-04 and SCR-09 in the app story that builds these screens. |

### OTHER:gateway-bff composite route to SCR-03; OTHER:TSD P6 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11226 | RWB-P6-E2022-CON | GAP-1075 | find it | Declare Case record right C on the gateway-bff composite route to SCR-03 answering MSG-P4-002 and MSG-P4-003, and record the reconciliation of the TSD P6 T6.1 Case record area. |

### OTHER:TSD P4 v3 role to permission matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11228 | RWB-P6-E2022-CON | GAP-0953 | find it | Add the Case record column and the other capability areas the stories decide on to the role to permission matrix, loading the letters as PM-2026.12 rows. |

### OTHER:Platform deployment configuration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11232 | RWB-P6-E2022-CON | GAP-1074 |  | Publish the NSS and LINE OA endpoint, certificate issuer, secret names and egress timeout; chart carries references only; egress check fails a release with a missing reference. |

### OTHER:P1 interaction record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11233 | RWB-P6-E2022-CON | GAP-1077 |  | Add a template reference to the interaction record (DF-INT-002 to DF-INT-029), or drop the template column from SCR-04; until then show channel, conduct check and delivery status. |

### OTHER:rwb-source-data interaction ledger contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11235 | RWB-P6-E2022-CON | GAP-1599 |  | Hold message outcome, delivery status and channel reference as an interaction ledger entry owned by rwb-source-data; add no fourth table to rwb_comms; agree the read path with P1 before wave 2. |

### OTHER:RWB P1 API appendix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11236 | RWB-P6-E2022-CON | GAP-2183 |  | Publish the contact-point read, the failed-contact count operation and the ledger delivery extension in the P1 API appendix; confirm delivery column types, count rule and list sources at contract review. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11237 | RWB-P6-E2022-CON | GAP-0955 |  | Publish the authorise, me-permissions and masking-policies shapes here; the composite route field list for SCR-03 goes in RWB-PLT-N001-CON before the send story is built. |

### OTHER:split_plan.json (RWB-E2-018 slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11239 | RWB-P6-E2022-CON | GAP-1184 | find it | Add RWB-P6-E2018-CON for the three signature-request operations, baselined from the legacy request and answer shapes and TSD P6 v2 T-A.1 API-P6-009 to API-P6-011. |

### OTHER:rwb-access role table and access log decision-code list (P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11240 | RWB-P6-E2022-CON | GAP-0956 | find it | Record the JOB-11 service identities with role class and scope; add decision codes for a message send and a refused send to the decision-code list. |

### OTHER:P3 screen specification (SCR-03; OTHER:SCR-04; OTHER:SCR-09) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11246 | RWB-P6-E2022-OPS | DOR-RWB-P6-E2022-OPS-10 | none | Add empty, loading, error and no access states for SCR-03, SCR-04 and SCR-09. |

### OTHER:TSD P4 role-to-permission matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11250 | RWB-P6-E2022-OPS | GAP-0953 | header | Add the Case record column and other capability areas the stories decide on, and load the letters as PM-2026.12 rows before first SIT entry. |

### OTHER:ACE notification path request and result contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11251 | RWB-P6-E2022-OPS | GAP-1069 | header | Publish request shape, accepted-reference format, NSS and LINE OA result codes and callback path before the wave 2 SIT entry. |

### OTHER:Technical Solution Design P6, table T5.1; OTHER:ACE notification path request and result contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11252 | RWB-P6-E2022-OPS | GAP-1072 | header | State the result transport (callback or poll) for both channels; a known external reference is accepted, an unknown reference is not applied. |

### OTHER:Technical Solution Design P6, rows INT-17 and INT-18, and the platform secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11253 | RWB-P6-E2022-OPS | GAP-1074 | header | Publish the endpoint, certificate issuer, secret names and egress timeout; the chart carries references only and the egress check fails a release with a missing reference. |

### OTHER:P1 API appendix; RWB-P6-E2022-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11254 | RWB-P6-E2022-OPS | GAP-2183 | header | Publish the contact-point read, the failed-count operation and the ledger extension with paths, shapes and error sets; confirm the delivery column types, consent renderings, channel mapping, count rule and list sources. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx; OTHER:access log decision-code list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11257 | RWB-P6-E2022-OPS | GAP-0956 | find it | Record the JOB-11 service identities with role code, role class and scope in the role table, and add decision codes for a send and for a refused send to the ledger decision-code list. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20757 | RWB-P6-E2021-APP | R-22567 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20805 | RWB-P6-E2021-APP | R-28797 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: 'the document store and the data lake copy is written to the access |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20901 | RWB-P6-E2022-OPS | R-22581 |  | Item text not re-read in this run, so no fix was written. Not verified against this document. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0404 | The WIN dispatch harness pack and the proof-file test window are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0405 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0437 | The legacy delivery step is split across rwb-comms, rwb-litigation and rwb-case with no named hand-off operation and no named reference rows, so the end-to-end chain of RWB-E5-002 has no single source of record | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0945 | rwb-access letter dispatch loop: the TSD RBAC matrix has no Litigation column, so the LITIGATION C and R letters the legacy authority table names are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0946 | rwb-access letter dispatch loop: the authorise request and answer shape for a notice request, a notice read and a dispatch read is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0947 | rwb-access letter dispatch loop: the masking version in force in SIT, the field IDs of the addressee postal address and party field on the notice panel, and the composite route field list are not specified | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0948 | rwb-access letter dispatch loop: the role code and scope of the service identity that runs JOB-10 are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0953 | The Case record letters per role are not in the TSD P4 role-to-permission matrix | Security administrator with the P4 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0955 | The authorise shape for a send and the field list of the composite route are not specified | Solution architect, P4 and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0956 | The rights of the JOB-11 service identity and the decision code of a send are not recorded | Security administrator with the P4 build squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1132 | No source states which event a digital view raises, and the proof-of-delivery element has two possible paths | P6 service owner and event owner | Resolved (directive) |
| GAP-1184 | The plan holds no RWB-P6-E2018-CON, so the three signature-request operations have no published contract story | Solution architect | Resolved (directive) |
| GAP-1194 | The source reads the proof of delivery from v_ace_pod in process, and this story may read no ACE view | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1599 | The message record and its delivery status have no table in the service under Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1600 | The retry limit for a send is five in the functional specification and three in the non-functional requirements | Solution architect | Resolved (directive) |
| GAP-1601 | The functional specification names JOB-11 as the retry job for sends, and Architecture v5 makes JOB-11 the outbox relay in every service | Solution architect | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1605 | The contact repository and the consent state are held in an extension table the source-data service owns | Solution architect | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1609 | The notice period timer and the transfer on a non-delivered notice are the case service's, and the trigger is not fixed | Solution architect with P3 | Resolved (directive) |
| GAP-1610 | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | Conduct and QA officer with rwb-decision | Resolved (directive) |
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
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2363 | The legacy screen, endpoints and rights of RWB-E4-035 serve an officer's notice screen, not a customer's offer view | Solution architect | Resolved (directive) |
| GAP-2368 | The two contracts and the contact-stop events the view depends on carry no C row and no source shape in this key's plan | Solution architect | Resolved (directive) |
| GAP-3183 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 result file with it | Integration lead with the communications lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P6-E2021-CON | skipped AC ID | 92 | missing: AC9, AC10, AC11, AC12, AC13 |
| RWB-P6-E2022-APP | skipped AC ID | 109 | missing: AC1, AC3, AC5, AC6, AC7, AC10, AC12 |
