# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 9 of 12 (RWB-P3-E2014-APP to RWB-P3-E2021-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 122 |
| Cross-document (pending in another document) | 170 |
| Not applied (value not in the sources) | 27 |
| Open business decisions | 32 |
| Register gaps linked | 84 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E2014-APP | 18 | 43 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2014 APP Approval screen for D7.1 demand and recall notices v2.md |
| RWB-P3-E2015-APP | 19 | 18 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2015 APP Timers, escalation and the deviation flag on the case record view v2.md |
| RWB-P3-E2015-CON | 15 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2015 CON Timers, escalation and the deviation flag on the case record view - contract v2.md |
| RWB-P3-E2015-OPS | 11 | 21 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2015 OPS Timers, escalation and the deviation flag on the case record view - deployment v2.md |
| RWB-P3-E2016-APP | 19 | 17 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2016 APP Full case record view with the history timeline v2.md |
| RWB-P3-E2016-CON | 13 | 20 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2016 CON Full case record view with the history timeline - contract v2.md |
| RWB-P3-E2021-APP | 27 | 26 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2021 APP Letter dispatch loop with proof of delivery from WIN v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E2014-APP | R-10430 | CG-ALL-4195 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2015-APP | R-10432 | CG-ALL-4210 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2016-APP | R-10438 | CG-ALL-4242 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2021-APP | R-10446 | CG-ALL-4267 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E1034-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22081 | GAP-1598 | Register gap | Product owner with the solution architect | Two of the module's business requirements describe the case record view and the case timeline, which the case service owns | Read both requirements as this service's contribution to the case record view: the notice and message block with its states, and the ordered notice and message history. The view, the timeline and the timer projection stay with rwb-case; the ledger entries stay with rwb-source-data. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22482 | GAP-0931 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masked rendering of the addressee postal address is not specified | Let the platform masking library own one rendering per field type, record it as data beside the masking row, and add the postal address rendering to the MASK-SIT-01 pack before the first SIT run of the approval screen |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22483 | GAP-1260 | Register gap | Business lead | The limit that applies on the approval screen conflicts with D7.1 carrying no amount limit | Show the approval level and the route role as the limit that applies for D7.1 (no amount, level none) and read the DoA table only where an amount-bearing decision uses the screen; confirm with Risk and Credit. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-ITG-E2015-ITG, RWB-ITG-E7006-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON | R-22499 | GAP-1827 | Register gap | Business lead | The deviation service level is 'set with DL22' and has no number, and the ten working day escalation comes only from the design | Carry the service level, the escalation period and the skip trace window as versioned reference data read at run time, assert no number, and take the values from DL22 when the business lead sets them. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22503 | GAP-0935 | Register gap | Business lead | Precedence between a role's default scope and an escalation grant is not specified | Rule that the wider of the two scopes is named, that the reason ESCALATED_TO_ROLE is carried while the escalation is open, and that the grant never exceeds Case record R on that one case. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22504 | GAP-0936 | Register gap | Compliance and PDPA officer | The masking version in force for SIT and the answer when two versions overlap are not specified | Record MASK-SIT-01 as the SIT version in the policy pack, and rule that the version with the latest valid_from on or before the business date is used, the answer naming the version it used. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22506 | GAP-3099 | Register gap | Solution architect, with the rwb-deviation owner, the rwb-case contract and reference-data owners, the product owner of the deviation service level, the rule-set owner of the Deviations package and the QA lead | RWB-S8-E2015-APP: the deviation section of the case record view has no read operation, no published view field names, no label for a code other than X3, no published value for the deviation service level and no escalation target | Publish the case deviation read as a service operation with a catalogue row, or amend the Ownership Map to carry GET /cases/{caseId}/deviations; freeze the deviation view field names in RWB-P3-E2015-CON; publish LOV-DEVIATION with a label per code and LOV-DEV-OUTCOME with a label per value; publish the deviation service level, its calendar and the row that holds it; publish the escalation target and the codes R-DEV-20 covers; record the six platform contracts as template dependencies of S8 beside the H row of the secondary slice; publish a level for each legacy test case. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4040-APP, RWB-P6-E4040-CON, RWB-P6-E4041-APP, RWB-P6-E4041-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22551 | GAP-1607 | Register gap | Product owner | Seven features in the Communications functional specification belong to other services in Architecture v5 | Keep the seven features in the source with their identifiers, mark them as not carried in section 5.1 of this PRD with their owning service, and raise the story-level split in the service work packages. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22552 | GAP-1603 | Register gap | Business lead with the data lead | No source states the notice, message or proof-of-delivery volumes | Size the volume test on the document volume of about 860,000 in 2027 as the upper bound for letters and on the interaction volume for messages, and replace both with the measured figures when the business lead provides them. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22554 | GAP-2092 | Register gap | Service owners of P6 rwb-comms and S8 rwb-deviation; business lead | The sources name different sets of deviation codes that raise a contact stop | Read the stop as X1 to X3, which is the wider and the safer reading, keep the hold reason on the notice, and ask the business lead to correct R-LIT-05. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22562 | GAP-1091 | Register gap | Business lead | The arithmetic of the 7-day proof window on the sent date is not stated | Confirm with the business lead and Legal counsel that the window is 7 calendar days counted from the sent date and that a notice is unserved on the first run on or after sent_date plus 7 days, then record the value and the rule in the reference data with its version. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22564 | GAP-1276 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P6 business analyst and the business owner | The dispatch decision record's payload, its field placement, the rule version label, the message id set, the parameter names, a panel id and the edge right of the two reads have no source | At the design review of wave 2 the solution architect, the data steward, the P6 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the dispatch columns of decision_log_entry (new columns or jsonb members of actions and outcome), the notice-reference filter and the answer field set of the read, the rule version label of the letter rules and their registry rows, the message ids and their texts, the panel id of the decision-log view, the parameter names and version labels of the page-size bound and the ingest target, and how the right and the scope reach the two reads at the edge; until then the story holds the assumed shape of ASM-B-P7-02-E2021-1, ASM-B-P7-02-E2021-2, ASM-B-P7-02-E2021-4, ASM-B-P7-02-E2021-5 and ASM-B-P7-02-E2021-6 and its nine criteria stand on that shape |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28769 | GAP-0933 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force in SIT is not recorded anywhere | Record the masking version in force per environment in the policy pack load record, with its approver and valid-from date, and assert it in the SIT entry check |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28770 | GAP-1261 | Register gap | Data steward and data product owner | The module specification keeps two daily data-lake interfaces that DP-17 removes | Retire INT-19, INT-20 and the daily copy from the P7 documents in the next module-specification version; no lake element appears in this key's stories, chart or run book. |
| RWB-ITG-E2016-ITG, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P5-E2016-APP | R-28783 | GAP-1062 | Register gap | Data steward and data product owner | Which table supplies the document type label a timeline item shows | Display the label from document_type at the version in force, label_en by default and label_th by locale, and compare the list with LOV-DOC-TYPE through the reference-data contract of rwb-case rather than copying it; fall back to the type code when the row of that version is absent. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1043-CON, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-28792 | GAP-2097 | Register gap | Service owners of P3 rwb-case and P4 rwb-access; business lead | Reference data is read from P4 in TSD P6 and from P3 in the plan default ruling | Follow R3 and DP-07: contact times and frequency are reference data of P3 rwb-case, read through C RWB-P3-E1043-CON. Access data, roles and DoA stay with P4. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-28804 | GAP-2222 | Register gap | Business lead | The legal hold reason list is not stated | Hold the reason list as a reference table of rwb-case loaded by RW-COE; the reason is stored as given until the list is approved. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-P3-E2021-APP | R-36405 | ASM-3654 | Register assumption |  | A legal hold is placed and lifted with a reason from a hold reason list held as reference data of rwb-case, loaded and versioned by RW-COE without a code release; until the list is approved the reason is stored as it is given. | Business lead |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E2014-APP | R-05256 | DOR-RWB-P3-E2014-APP-16 | Header | Definition of Ready item 16 Size: Fail | No size is in the sources, so the item cannot be resolved by this story; the squad sizing claim was removed as invented. |
| RWB-P3-E2014-APP | R-16168 | DOR-RWB-P3-E2014-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Naming the P2 field needs a value not in the story or sources; BR10 already states no personal data is carried. Left unchanged. |
| RWB-P3-E2014-APP | R-25099 | CG-ALL-4198 | 3.1 | Flyway file V2014_1__case_notice_redress_task.sql is not in the V0001..Vnnnn form | Story line 423 names no migration now. The rwb-case next Flyway number is not in the sources (checked Service Template Specification v1 §3.1, ADRs). Not specified in the source documents (CG-ALL-4198). |
| RWB-P3-E2015-APP | R-00936 | CG-ALL-4211 | not in chunk | Java package th.co.scb.ace.workbench.recovery.case.caseview uses the reserved word 'case' | Segment ruling and Service Template naming rule not in sources (searched workbench). Package text is outside this chunk. No segment invented. |
| RWB-P3-E2015-APP | R-05262 | DOR-RWB-P3-E2015-APP-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story, chunk or sources. Sign-off cannot be confirmed, so it cannot be recorded. |
| RWB-P3-E2015-APP | R-16173 | DOR-RWB-P3-E2015-APP-10 | not in chunk | Definition of Ready item 10 Screens and states: Partial | SCR-03 empty, loading, error and no-access wording sits in the screens text outside this chunk. Exact text needed for an edit. |
| RWB-P3-E2015-APP | R-16174 | DOR-RWB-P3-E2015-APP-11 | not in chunk | Definition of Ready item 11 Guardrails: Partial | Personal-data statement and P2 field classes are outside this chunk. Field classes need the LDM, which was not supplied. |
| RWB-P3-E2015-APP | R-16177 | DOR-RWB-P3-E2015-APP-18 | not in chunk | Definition of Ready item 18 Open decisions: Partial | DL10 and DL22 open-decision rows and assumption text are outside this chunk. Cannot edit without that text. |
| RWB-P3-E2015-APP | R-25106 | CG-ALL-4212 | 7 | Criteria and tests keep legacy job and decision-log wording | Section 12.5 has no JOB or decision-log wording. The AC2 and AC10 lines that carry it are outside this chunk; exact old text needed. |
| RWB-P3-E2015-APP | R-28777 | GAP-0715 | not in chunk | No source gives the alert values for the timer projection, the degradation rate or the breach volume | No source gives timer lag, degradation-rate or breach-volume values, so none can be set. Gap stays open until DevOps lead agrees values. |
| RWB-P3-E2015-OPS | R-05272 | DOR-RWB-P3-E2015-OPS-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or 03 sources; searched 03 Requirements and specifications. Sign-off not invented. |
| RWB-P3-E2015-OPS | R-05275 | DOR-RWB-P3-E2015-OPS-22 | header | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded as published in the story or 03 sources; searched 03 folder. Not invented. |
| RWB-P3-E2015-OPS | R-05276 | DOR-RWB-P3-E2015-OPS-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Sources give only the /v1 path; no fixed contract version in 03 sources. Not invented; story has no value to fix. |
| RWB-P3-E2015-OPS | R-25115 | CG-ALL-4232 | 7 | Criteria and tests keep legacy job and decision-log wording | Section 16 legacy wording is not changed in this diff, and the section 7 AC6 line sits outside this chunk, so the item is not fully resolved. |
| RWB-P3-E2016-APP | R-00950 | CG-ALL-4243 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Segment name needs the solution architect's ruling; not in sources (checked 03 Requirements PRD P3 rwb-case v1 and FSD P3 v5). Line 354 left blank. |
| RWB-P3-E2016-APP | R-00951 | CG-ALL-4244 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.timeline uses the reserved word 'case' | Segment name needs the solution architect's ruling; not in sources (checked 03 Requirements PRD P3 rwb-case v1 and FSD P3 v5). Line 354 left blank. |
| RWB-P3-E2016-APP | R-16195 | DOR-RWB-P3-E2016-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Personal-data class of the named P2 field and guardrail text are not in this chunk or the sources; needs P2 section and Data Classification inventory. |
| RWB-P3-E2016-APP | R-22508 | GAP-0400 |  | Gateway-bff composite timeline route, harness environment and evidence gate are not specified | Route path, merge order, fixture seeding, SIT environment, evidence format, retention and gate are not in sources; Not specified in the source documents (GAP-0400). |
| RWB-P3-E2016-APP | R-25118 | CG-ALL-4245 | 3 | Flyway file V2016_1__timeline_indexes.sql is not in the V0001..Vnnnn form | Line 395 is blank in the supplied text. D-RCV-28 (P1 E1001 APP, line 359) sets seq at merge; no next number in sources. Not invented. |
| RWB-P3-E2016-CON | R-25124 | CG-ALL-4257 | 12.5 | Criteria and tests keep legacy job and decision-log wording | 'Decision log R' is the roles.txt permission name (BR7); renaming it invents a permission. JOB-05 is in 12.6, outside sections 7 and 16. Story not edited. |
| RWB-P3-E2021-APP | R-00958 | CG-ALL-4268 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Service Template Spec v2 (line 133) gives only the pattern recovery.<short>; no replacement for 'case' in sources. Solution architect ruling needed. |
| RWB-P3-E2021-APP | R-00959 | CG-ALL-4269 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.letterloop uses the reserved word 'case' | Same as CG-ALL-4268: Service Template Spec v2 (line 133) has no replacement segment for 'case.letterloop'. Solution architect ruling needed. |
| RWB-P3-E2021-APP | R-05289 | DOR-RWB-P3-E2021-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off is in the story or the chunk. The record was not found in the sources searched, so the sign-off cannot be confirmed. |
| RWB-P3-E2021-APP | R-05294 | DOR-RWB-P3-E2021-APP-8 | 12.1 | Definition of Ready item 8 Contract: Fail | Story gives no PATCH /tasks/{taskId} idempotency key, and no key value is in sources. Kafka Catalog v1 payload and event-name fixes are outside this chunk. |
| RWB-P3-E2021-APP | R-10440 | CG-ALL-4260 | 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 has no 401 or session-expired message ID (MSG-GEN-006 is system-unavailable). Business analyst must supply the ID; none invented. |
| RWB-P3-E2021-APP | R-16210 | DOR-RWB-P3-E2021-APP-11 | header | Definition of Ready item 11 Guardrails: Partial | The P2 personal-data field list is not in the chunk or the sources, so the no-personal-data claim cannot be checked. |
| RWB-P3-E2021-APP | R-16213 | DOR-RWB-P3-E2021-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Section 8 maps BR1-BR8 to AC1-AC10. Adding AC rows in section 7 and TC rows in section 16 needs those sections, which are outside this chunk. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06776 | RWB-P3-E2014-APP | CG-ALL-4184 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId} through the CON story (RWB-P7-E2014-CON), as recommended; the story keeps API-P3-002. |
| CDC-06777 | RWB-P3-E2014-APP | CG-ALL-4185 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId}/timeline through the CON story (RWB-P7-E2014-CON), as recommended; the story keeps API-P3-003. |
| CDC-06778 | RWB-P3-E2014-APP | CG-ALL-4186 | 8 | Remove the fixed enum on reason so LOV-ASSIGN-REASON values are accepted as data. |
| CDC-06779 | RWB-P3-E2014-APP | CG-ALL-4187 | 8 | Remove the fixed enum on status that gates LOV-CASE-STATUS values so they are accepted as data. |
| CDC-06780 | RWB-P3-E2014-APP | CG-ALL-4188 | 8 | Remove the fixed enum on elementType so LOV-ELEMENT values are accepted as data. |
| CDC-06781 | RWB-P3-E2014-APP | CG-ALL-4189 | 8 | Remove the fixed enum on status that gates LOV-TASK-STATUS values so they are accepted as data. |
| CDC-06790 | RWB-P3-E2014-APP | DOR-RWB-P3-E2014-APP-8 | 9 | Add GET /api/recovery/case/v1/cases/{caseId} and /api/recovery/case/v1/cases/{caseId}/timeline; hold reason and status as LOV-ASSIGN-REASON and LOV-CASE-STATUS data, not closed enums; clear the five further detcheck findings. |
| CDC-06820 | RWB-P3-E2015-APP | CG-ALL-4206 | 3 | Remove the closed enum on timerType so LOV-TIMER values are accepted as data without a code change. |
| CDC-06821 | RWB-P3-E2015-APP | CG-ALL-4207 | 3 | Remove the closed enum on status so LOV-TIMER-STATUS values are accepted as data without a code change. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06819 | RWB-P3-E2015-APP | CG-ALL-4205 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story. |
| CDC-06837 | RWB-P3-E2015-CON | CG-ALL-4216 | 12.2 | Publish POST /api/recovery/access/v1/authorise, or the provider consumes a published operation as its CON story rules |
| CDC-06859 | RWB-P3-E2015-OPS | CG-ALL-4226 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story, or the consumer re-points to a published operation. |
| CDC-06880 | RWB-P3-E2016-APP | CG-ALL-4238 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-06881 | RWB-P3-E2016-APP | CG-ALL-4239 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through the provider's CON story. |
| CDC-06897 | RWB-P3-E2016-CON | CG-ALL-4250 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-06898 | RWB-P3-E2016-CON | CG-ALL-4251 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through the provider's CON story. |

### RWB-P7-E2014-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06787 | RWB-P3-E2014-APP | DOR-RWB-P3-E2014-APP-21 | Header | Publish the contract under RWB-P7-E2014-CON, the contract named in this story's dependencies. |
| CDC-06788 | RWB-P3-E2014-APP | DOR-RWB-P3-E2014-APP-22 | Header | Publish the contract fake library and record its version as published. |
| CDC-06805 | RWB-P3-E2014-APP | GAP-1258 | 3 | Publish the field list and mask flags of the SCR-11 and SCR-18 panels as the working read, confirm with the route owner and the three consumer sign-offs, and version the contract. |
| CDC-06806 | RWB-P3-E2014-APP | GAP-1259 | 3 | Carry GET /api/recovery/approvals/{approvalId} as the working read and register it with the route owner at the first version freeze. |
| CDC-06807 | RWB-P3-E2014-APP | GAP-1270 | 3 | Register the approval composite with a 2 s budget per downstream, the 1.2 s composition budget of the case screen, and record the measured p95 on the dashboard. |
| CDC-06814 | RWB-P3-E2014-APP | GAP-1266 | n/a | Set the queue page size default at 20 and the maximum at 100; publish the field types and order of the screen model in RWB-P7-E2014-CON; confirm with front end and route owner. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06810 | RWB-P3-E2014-APP | CG-ALL-4194 | 18 | Align the trace to RWB-P3-E2014-APP section 18: REQ-APD-002 to TC-E2-014-01, -02, -05, -06, -10, -13, -14; REQ-APD-006 to TC-E2-014-01, -03, -04, -07, -08, -09, -11, -12, -14. |
| CDC-06832 | RWB-P3-E2015-APP | CG-ALL-4209 | 18 | Align the test case lists for REQ-WKM-004, REQ-WKM-005 and REQ-DVH-002 with section 18 of RWB-P3-E2015-APP in the next RTM version. |
| CDC-06854 | RWB-P3-E2015-CON | CG-ALL-4221 | 18 | Align the test lists for REQ-WKM-004, REQ-WKM-005 and REQ-DVH-002 with section 18 of this story. |
| CDC-06876 | RWB-P3-E2015-OPS | CG-ALL-4231 | 18 | Align the test lists for REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 and the fourth requirement in both documents, in their next versions. |
| CDC-06892 | RWB-P3-E2016-APP | CG-ALL-4241 | 18 | Align the test lists of REQ-WKM-008, REQ-OCC-008, REQ-CWC-016 and the fourth listed requirement to RWB-P3-E2016-APP section 18 in its next version. |
| CDC-06911 | RWB-P3-E2016-CON | CG-ALL-4255 | 18 | Align the four differing requirement trace rows so RTM v7 and story §18 list the same test cases. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06830 | RWB-P3-E2015-APP | GAP-0714 | 7 | Add GET /cases/{caseId}/deviations to the S8 rows and the S8 API file; until then consume the read behind the S8 contract with the 2 s timeout. |
| CDC-06851 | RWB-P3-E2015-CON | GAP-0714 | n/a | Add GET /cases/{caseId}/deviations to the S8 rows; until then consume the read behind the S8 contract with the 2 s timeout. |
| CDC-06873 | RWB-P3-E2015-OPS | GAP-0714 | 12 | Add GET /cases/{caseId}/deviations to the S8 rows. Until then, consume the read behind the S8 contract with the 2 s timeout, as RWB-ITG-E2015-ITG assumes. |
| CDC-06890 | RWB-P3-E2016-APP | GAP-0716 | Find it | Publish one case-scoped interaction-ledger read on the rwb-source-data base with the query and masked summary shape of API-P3-014; record in the Ownership Map which interaction operation rwb-case keeps. |
| CDC-06908 | RWB-P3-E2016-CON | GAP-0716 | 12.2 | Publish one case-scoped interaction-ledger read on the rwb-source-data base with the query and masked summary shape of API-P3-014, and record which interaction operation rwb-case keeps. |
| CDC-06913 | RWB-P3-E2016-CON | GAP-0717 | 12.2 | Add the case-scoped notice list (GET /cases/{id}/notices) to the Ownership Map API section under P6 with its query and response shape, and align the P6 baseline. |

### RWB-P4-E1037-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06794 | RWB-P3-E2014-APP | GAP-0932 |  | Publish the authorise, me-permissions and masking-policies shapes and state whether the routed role or the holder is a request field. |
| CDC-06828 | RWB-P3-E2015-APP | GAP-0934 | 7 | Specify POST /authorise request v1 with caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt, versioned BACKWARD compatible. |
| CDC-06849 | RWB-P3-E2015-CON | GAP-0934 | n/a | Fix the authorise request with caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt; version v1 with BACKWARD compatibility. |
| CDC-06871 | RWB-P3-E2015-OPS | GAP-0934 | 12 | Define the authorise request as v1 with caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt. Mark it BACKWARD compatible so a case service can add attributes. |
| CDC-06926 | RWB-P3-E2021-APP | GAP-0946 | 9 | Add POST /authorise with request and answer schema to the API specification and TSD P4 appendix T-A; stub in contract fake; add access entry decision codes to ledger code list. |

### RWB-P6-E1052-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06795 | RWB-P3-E2014-APP | GAP-1264 | Not located in chunk | Publish notice approve, regenerate and hold operations with states and error codes, and correct the Ownership Map api rows. |
| CDC-06796 | RWB-P3-E2014-APP | GAP-1268 | Not located in chunk | Serve notice PDF as document reference through rwb-document; addressee role and masked address come from rwb-source-data. |
| CDC-06798 | RWB-P3-E2014-APP | GAP-2384 | Not located in chunk | Add POST notices/{noticeId}/approve, /regenerate and /hold to the rwb-comms API file and Ownership Map, with request fields and 401/403/404/409/422/503 responses. |
| CDC-06800 | RWB-P3-E2014-APP | GAP-2386 | Not located in chunk | State that a template change regenerates on the same notice row, moving document_id and template_id to the Approved variant and incrementing the version column. |
| CDC-06801 | RWB-P3-E2014-APP | GAP-2387 | Not located in chunk | Baseline notice answer fields: id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt, decisionLogEntryId. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06879 | RWB-P3-E2016-APP | CG-ALL-4237 | 12.2 | Publish GET /api/recovery/comms/v1/cases/{caseId}/notices in rwb-comms.yaml through the provider's CON story. |
| CDC-06896 | RWB-P3-E2016-CON | CG-ALL-4249 | 12.2 | Publish GET /api/recovery/comms/v1/cases/{caseId}/notices in rwb-comms.yaml through the provider's CON story. |
| CDC-20676 | RWB-P3-E2016-APP | R-00947 |  | GET /cases/{caseId}/notices is absent; only POST exists. Its response shape is not specified in the source documents (CG-ALL-4237). |
| CDC-20677 | RWB-P3-E2016-CON | R-00952 |  | GET /cases/{caseId}/notices is absent; response shape not specified in the source documents (CG-ALL-4249). |
| CDC-20678 | RWB-P3-E2016-CON | R-05288 |  | Three operations missing (CG-ALL-4249 to 4251). Response shapes not specified in sources; rwb-access.yaml is outside this document (DOR-RWB-P3-E2016-CON-8). |

### RWB-P6-E2021-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06916 | RWB-P3-E2021-APP | DOR-RWB-P3-E2021-APP-21 | Header | Confirm the contract story for rwb-case and record it as published; the story already names it under Contract dependencies. |
| CDC-06917 | RWB-P3-E2021-APP | DOR-RWB-P3-E2021-APP-22 | Header | Record the published contract fake library version. Not specified in the source documents. |
| CDC-06923 | RWB-P3-E2021-APP | GAP-1089 | 12 | Publish WIN file name, record layout, acknowledgement fields and INT-15 proof result record, agreed with WIN and rwb-integration owners at baseline review. |
| CDC-06928 | RWB-P3-E2021-APP | GAP-1095 | 12 | Publish the Airflow window to Temporal Schedule handoff: window signals the Schedule with business date, run records the date, rerun of same date writes no second file. |
| CDC-06932 | RWB-P3-E2021-APP | GAP-1092 |  | Declare capability area and right per operation; gateway-bff asks rwb-access (DP-08) before the call; serve the scope fact from the rwb-case case read already consumed, or add C RWB-P4-E1037-CON. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06792 | RWB-P3-E2014-APP | GAP-2093 |  | Hold the approval in P7 ApprovalWorkflow as a child of NoticeDispatchWorkflow; keep POST /notices/{noticeId}/approve in S4 as the decision point; remove 'Decision: child: approval' from P6 OUT. |
| CDC-06835 | RWB-P3-E2015-APP | GAP-1830 | find it | Record SCR-06 and SCR-08 as gateway-bff composite routes over this service's read and command contract, and confirm the read operation before the wave 2 screen test. |
| CDC-06856 | RWB-P3-E2015-CON | GAP-1830 | n/a | Record the raise screen and the deviation queue as gateway-bff composite routes owned at the edge; record the deviation queue read operation after confirming it with the platform edge owner. |
| CDC-06864 | RWB-P3-E2015-OPS | GAP-1820 | find it | Record the approval as a step inside DeviationWorkflow taken by the code-assigned role; keep the P7 ApprovalWorkflow edge open. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06809 | RWB-P3-E2014-APP | CG-ALL-4193 | 16 | Story now defines AC9 and AC10, but Test Cases v8 maps its tests to AC9 and AC10 with different content |
| CDC-06853 | RWB-P3-E2015-CON | CG-ALL-4220 | 16 | Add rows TC-P3-E2015-CON-01 to TC-P3-E2015-CON-06 with Given, When and Then copied from AC1 to AC6. |
| CDC-06875 | RWB-P3-E2015-OPS | CG-ALL-4230 | 16 | Add rows TC-P3-E2015-OPS-01 to TC-P3-E2015-OPS-06, with Given, When and Then copied from the criterion each covers. |
| CDC-06910 | RWB-P3-E2016-CON | CG-ALL-4254 | 16 | Add rows for TC-P3-E2016-CON-01 to TC-P3-E2016-CON-06 with Given, When and Then copied from the criterion each covers. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06826 | RWB-P3-E2015-APP | GAP-3177 | 7 | Register the five-minute next-action Temporal Schedule in rwb-case; delete EV-18 TimerDue from the Epic 2 contract tables. |
| CDC-06847 | RWB-P3-E2015-CON | GAP-3177 | 16 | Register the five-minute next-action Schedule in rwb-case and remove EV-18 from the Epic 2 contract tables. |
| CDC-06869 | RWB-P3-E2015-OPS | GAP-3177 | 12 | Register the five-minute next-action Temporal Schedule in rwb-case. Delete TimerDue (EV-18) from the Epic 2 contract tables. |
| CDC-06920 | RWB-P3-E2021-APP | CG-ALL-4266 | 12.5 | Add activity ApplyNoticeFact on task queue rwb-case with the purpose stated in section 12.5. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06775 | RWB-P3-E2014-APP | CG-ALL-4183 | 13 | Add one field on entity task for the notice reference of the redress task; its name, type and length are Not specified in the source documents (CG-ALL-4183). |
| CDC-06789 | RWB-P3-E2014-APP | DOR-RWB-P3-E2014-APP-7 | 11, 13 | Add one field on entity task for the notice reference of the redress task; its name, type and length are Not specified in the source documents (CG-ALL-4183). |
| CDC-06799 | RWB-P3-E2014-APP | GAP-2385 | Not located in chunk | Add nullable decision_log_entry_id uuid to notice with unique index, via Flyway step V2014_1__notice_decision_reference.sql. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06782 | RWB-P3-E2014-APP | CG-ALL-4191 | 12.4 | Add event type rwb.decision.ApprovalRefused.v1 to the Events sheet on topic rwb.decision.events.v1, owner P7, with its ce_type. |
| CDC-06783 | RWB-P3-E2014-APP | CG-ALL-4192 | 12.4 | Add event type rwb.decision.ApprovalReturned.v1 to the Events sheet on topic rwb.decision.events.v1, owner P7, with its ce_type. |
| CDC-06919 | RWB-P3-E2021-APP | CG-ALL-4264 | 12.4 | Add rwb-case as a consumer of rwb.comms.NoticeDispatched.v1, with its ACL entry. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06818 | RWB-P3-E2015-APP | CG-ALL-4204 | 12.2 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/deviations through the rwb-deviation provider CON story. |
| CDC-06836 | RWB-P3-E2015-CON | CG-ALL-4215 | 12.2 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/deviations, or the provider consumes a published operation as its CON story rules |
| CDC-06858 | RWB-P3-E2015-OPS | CG-ALL-4225 | 12.2 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/deviations through the provider CON story, or the consumer re-points to a published operation. |

### RWB-P3-E2015-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06822 | RWB-P3-E2015-APP | DOR-RWB-P3-E2015-APP-21 | header | Move the build status of the contract story from Not started to Done before this story is ready. |
| CDC-06823 | RWB-P3-E2015-APP | DOR-RWB-P3-E2015-APP-22 | header | Publish a contract fake library version and record it in the dependency details of this story. |
| CDC-06860 | RWB-P3-E2015-OPS | DOR-RWB-P3-E2015-OPS-21 | header | Build status Done before RWB-P3-E2015-OPS starts. Story header now names this dependency. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06838 | RWB-P3-E2015-CON | DOR-RWB-P3-E2015-CON-14 | header | Record the signed epic design sign-off for RWB-P3-E2015-CON |
| CDC-06882 | RWB-P3-E2016-APP | DOR-RWB-P3-E2016-APP-14 | header | Sign off the epic design and record the signed sign-off so the story can cite it. |
| CDC-06900 | RWB-P3-E2016-CON | DOR-RWB-P3-E2016-CON-14 | n/a | Confirm and record the signed epic design sign-off for RWB-P3-E2016-CON. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06841 | RWB-P3-E2015-CON | CG-ALL-4219 | 14 | Add a new message ID for schema failure of a response body or query, text 'The request could not be read: {detail}.'; keep MSG-P3-030 for the scheduled job row |
| CDC-06845 | RWB-P3-E2015-CON | DOR-RWB-P3-E2015-CON-9 | 14 | Add the same new schema-failure message ID as CG-ALL-4219; keep MSG-P3-030 for the scheduled job |
| CDC-06886 | RWB-P3-E2016-APP | CG-ALL-4240 | 12.1 | Errors line maps 503 to MSG-GEN-006; text fit for a read is not confirmed. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06844 | RWB-P3-E2015-CON | DOR-RWB-P3-E2015-CON-12 | 16 | Add TC-P3-E2015-CON-01 to -08 to Test Cases v8; align section 18 lists to RTM v7 |
| CDC-06867 | RWB-P3-E2015-OPS | DOR-RWB-P3-E2015-OPS-12 | 12, 12.7, 16, 18 | Add TC-P3-E2015-OPS-01 to -06 to Test Cases v8 and align the section 18 test lists to RTM v7. |
| CDC-06904 | RWB-P3-E2016-CON | DOR-RWB-P3-E2016-CON-12 | 12.7, 16, 18 | Story adds CON-07 and CON-08 to the §16 list and updates it to eight cases. CON-07 is not linked to REQ-CWC-016 because it tests table boundaries. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06862 | RWB-P3-E2015-OPS | GAP-1816 | find it | Return the FSD S8 source fields, including party-flag, deceased-marker and freshness fields; S8 builds only on that contract; P1 confirms the fields before wave 2 system test. |
| CDC-06878 | RWB-P3-E2015-OPS | GAP-1830 | 15 | Story records SCR-06 and SCR-08 as gateway-bff composite routes. The owner cell is missing from the Architecture screen matrix and the edge owner is not named, so the item is not fully resolved in the story. |
| CDC-06940 | RWB-P3-E2021-APP | GAP-2106 |  | Record rwb-comms as owner of the JOB-10 notice and Schedule, and rwb-integration as owner of transport and retry, publishing FileDelivered or FileFailed to P6. |

### RWB-P3-E2016-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06883 | RWB-P3-E2016-APP | DOR-RWB-P3-E2016-APP-21 | find it | Set build status to Done so the contract is published. |
| CDC-06884 | RWB-P3-E2016-APP | DOR-RWB-P3-E2016-APP-22 | find it | Publish a contract fake library version and record it. |
| CDC-06895 | RWB-P3-E2016-APP | GAP-1060 | 3 | Return doc_version on the TimelineItem for document items; the full version history stays on API-P5-003 when the item is opened (TSD P5 T-A.2). |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06784 | RWB-P3-E2014-APP | CG-ALL-4196 | 1 | Rule a Java package segment for rwb-case that is not the reserved word case; the segment is Not specified in the source documents (CG-ALL-4196). |
| CDC-06785 | RWB-P3-E2014-APP | CG-ALL-4197 | 12.7 | Rule a Java package segment for the noticefacts sub-package of rwb-case that is not the reserved word case; the segment is Not specified in the source documents (CG-ALL-4197). |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06842 | RWB-P3-E2015-CON | DOR-RWB-P3-E2015-CON-1 | 1 | Add or name the role for tech lead with its role code; section 1 then cites that code |
| CDC-06902 | RWB-P3-E2016-CON | DOR-RWB-P3-E2016-CON-1 | 1 | Name the tech lead of rwb-case as a role code or role name, or confirm the existing role code this story uses. |

### RWB-P7-E1027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06889 | RWB-P3-E2016-APP | GAP-2210 | Find it | Target corrected: removed stray 'C' prefix. |
| CDC-06906 | RWB-P3-E2016-CON | GAP-2210 | 11 | Story §11 states the case status history is Not specified in the source documents (GAP-2210); the unsourced read paths are removed |

### RWB-P3-E1023-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06893 | RWB-P3-E2016-APP | GAP-2211 | 3 | Publish the timeline addition as v1.1, an additive minor version in major version 1, with the item detail fields, the TimelineSection state on a 200 response and the page total; keep type order, section timeout and page size as rwb-case parameters. |
| CDC-06912 | RWB-P3-E2016-CON | GAP-2211 | 12.2 | Publish the timeline addition as v1.1, an additive minor version inside major version 1, with item detail fields, TimelineSection state on a 200 response and page total; keep type order, section timeout and page size as rwb-case parameters. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06924 | RWB-P3-E2021-APP | GAP-0945 | 12 | Add Litigation column to TSD P4 T6.1 for each role in the legacy authority table; publish 14-area matrix as data; confirm C and R letters with matrix owner before go-live. |
| CDC-06925 | RWB-P3-E2021-APP | GAP-0948 | 12 | Name the JOB-10 runner service identity in the role table with role class NON_HUMAN_ACTOR, scope ALL and its Litigation R row; record in policy pack load. |

### RWB-P3-E2014-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06786 | RWB-P3-E2014-APP | DOR-RWB-P3-E2014-APP-14 | 14 | Record the signed epic design sign-off for RWB-P3-E2014-APP, then cite that record in the Definition of Ready item 14 |

### OTHER:rwb-case case contract; OTHER:FSD P7 acceptance criteria A2.15 and A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06791 | RWB-P3-E2014-APP | GAP-1623 |  | Record that the Waiting approval state move and the approval task are a P3 reaction to ApprovalRequested; this story writes no case state. |

### RWB-P7-E2014-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06793 | RWB-P3-E2014-APP | GAP-2216 |  | Fix the case-facts projection with inputAsOf on API-P3-002, the refusal and return events on rwb.decision.events.v1, the task code and reference row, and the dated contact read. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06797 | RWB-P3-E2014-APP | GAP-0398 |  | GAP-0398: integration lead to agree with the platform edge owner the composite decision-screen route and merge order; with business dates, SIT environment, evidence format, retention and the 16:00 pass/fail gate with QA at the wave 2 entry check. No values in sources. |

### OTHER:TSD P6 v2 (T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06802 | RWB-P3-E2014-APP | GAP-2388 | Not located in chunk | Add three rows for the notice decision operations declared as Litigation right A with scope applied, called by rwb-decision with service identity and approver user identifier. |

### OTHER:TSD P6 v2 (T4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06803 | RWB-P3-E2014-APP | GAP-2390 | Not located in chunk | State that a notice move writes one local decision record via the library with code D7.1 and a reference to the approval entry. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06804 | RWB-P3-E2014-APP | GAP-2743 | Not located in chunk | Record the two consumed rows as C dependencies with placeholders, declare notice and template ownership for P6, add REQ-S4-001 to the trace, and decide the D7.1 gate in the EP05 PRD. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06808 | RWB-P3-E2014-APP | GAP-2742 | Header, 3, 18 | Requirement trace row set to Not specified |

### OTHER:TSD P7 v2 T8 traceability table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06811 | RWB-P3-E2014-APP | GAP-1263 | header | Correct T8 rows for REQ-APD-002 and REQ-APD-006 to FEAT-APD-08 with RWB-E2-014 for the screen and FEAT-APD-01 with RWB-E2-013 for routing, as in FSD P7 v3. |

### OTHER:Edge and gateway design (SCR-10; OTHER:SCR-11; OTHER:SCR-12; OTHER:SCR-38 screen contracts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06812 | RWB-P3-E2014-APP | GAP-1621 | n/a | Record which of the four screens gateway-bff composes from this service's operations and which states this service owns, with the four screen contracts. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:slides 41 to 43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06813 | RWB-P3-E2014-APP | GAP-1262 | n/a | Publish the decided outcome on rwb-decision-record.v1 through the local library (DP-03); retire ApprovalDecided from the slide 14 line or add it to the catalogue with its consumers. |

### OTHER:TSD P7 v2 observability text (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06815 | RWB-P3-E2014-APP | GAP-1271 | n/a | Add alerts on any 5xx in five minutes, on route p95 above the registered budget, on a failed record write and on an empty D7.1 queue for 24 hours; review with the platform observability owner. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06816 | RWB-P3-E2014-APP | GAP-2391 | n/a | Add LOV-HOLD-REASON with REFUSED_BY_APPROVER and TEMPLATE_WITHDRAWN; keep the switch rwb.decision.notice-approval read by both services until the feature-flag owner renames it. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06817 | RWB-P3-E2014-APP | GAP-2389 | n/a | At the next plan revision add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to the C list; keep H empty. |

### OTHER:rwb-deviation API yaml; OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06824 | RWB-P3-E2015-APP | DOR-RWB-P3-E2015-APP-8 | 12 | rwb-deviation publishes GET /api/recovery/deviation/v1/cases/{caseId}/deviations; rwb-access publishes POST /api/recovery/access/v1/authorise; rwb-case.yaml timerType and status reference LOV-TIMER and LOV-TIMER-STATUS, not closed enums. |

### OTHER:FSD S8 (A2.2.4.1 to A2.9.4.1; OTHER:A2.2.4.2 to A2.9.4.2; OTHER:A2.2.4.3 to A2.9.4.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06825 | RWB-P3-E2015-APP | GAP-1823 | 7 | Rewrite each repeated 'Timers shown', deviation and exception row as one owned criterion with its owner; keep row text as evidence and add step criteria for pause, stop, routing and clear. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:EV-07 DeviationCleared) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06827 | RWB-P3-E2015-APP | GAP-1832 | 7 | Add to the envelope: case key, deviation code, state, contact stop flag, return point and decision record reference; no personal or financial value; schema written with the contract story. |

### RWB-ITG-E2015-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06829 | RWB-P3-E2015-APP | GAP-0399 | 16 | Record the gateway-bff case-record route path, merge order, timer and deviation fixtures with fixed clocks, seeding, evidence format and retention, and pass/fail gate, agreed at wave 2 entry. |

### OTHER:FSD S8 (Functional Specification S8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06831 | RWB-P3-E2015-APP | GAP-1817 | find it | Replace the 'Workbench, Quartz scheduler' integration point at A2.2.2, A2.3.2 and A2.6.2 with durable timers inside DeviationWorkflow through the workflow kit; remove the Quartz dependency. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06833 | RWB-P3-E2015-APP | GAP-2203 | find it | Add timer.escalated_to_role (DF-WRK-043) and timer.escalated_at (DF-WRK-044) with type, length and optionality, and fix the TimerBreached event 19 payload field list. Values not in sources: Not specified in the source documents (GAP-2203). |

### OTHER:FSD S8 document control and inherited history table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06834 | RWB-P3-E2015-APP | GAP-1834 | find it | Add the v1 and v2 change-note rows as Not specified in the source documents (GAP-1834) until the FSD folder is completed. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06839 | RWB-P3-E2015-CON | DOR-RWB-P3-E2015-CON-8 | 12.2 | Publish GET deviation and POST authorise paths; Kafka event name fixed in story at 12.3 |

### OTHER:FSD S8 A1.1 Constraints (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06840 | RWB-P3-E2015-CON | GAP-1816 | none | S8 reads ACE data only through the rwb-source-data contract, with no direct view read |

### RWB-P3-E2015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06843 | RWB-P3-E2015-CON | DOR-RWB-P3-E2015-CON-10 | none | Add empty, loading, error and no-access states for SCR-03 to the app story |

### OTHER:FSD S8 main success criterion and alternate rows (owner: groomer) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06846 | RWB-P3-E2015-CON | GAP-1823 | 7 | AC7 and TC-08 assert behaviour the FSD rows do not hold. The FSD criterion is rewritten with its owner; no story-side resolution. |

### RWB-P3-E2015-CON; OTHER:EV-07), another chunk of this story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06848 | RWB-P3-E2015-CON | GAP-1832 | 12 | Carry DeviationRaised (EV-06) and DeviationCleared (EV-07) keyed by case, with code, state, contact stop flag, return point and decision record reference; no personal or financial value. |

### OTHER:Wave 2 harness pack (no file name in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06850 | RWB-P3-E2015-CON | GAP-0399 |  | Record the agreed gateway-bff composite case-record route path and merge order, timer and deviation fixtures with fixed clocks, harness environment and seeding, evidence format and retention, and pass/fail gate, agreed with the platform edge story and QA at the wave 2 entry check. |

### OTHER:FSD S8 A2.2.2; OTHER:A2.3.2; OTHER:A2.6.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06852 | RWB-P3-E2015-CON | GAP-1817 | n/a | State pause, prescription clock and resume as durable timers inside DeviationWorkflow via the workflow kit; drop the Quartz integration row. |

### OTHER:FSD S8 Document control (FSD v6 extract folder) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06855 | RWB-P3-E2015-CON | GAP-1834 | n/a | Add the change notes of v1 and v2 with their dates and contents when the folder is completed; until then the history stays Not specified in the source documents (GAP-1834). |

### OTHER:rwb-case values files and the runbook entry each alert links (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06857 | RWB-P3-E2015-CON | GAP-0715 | n/a | Set the timer projection lag, the MSG-GEN-006 degradation rate and the TimerBreached volume alert values, confirm them at UAT and record the agreed values in the runbook. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06861 | RWB-P3-E2015-OPS | DOR-RWB-P3-E2015-OPS-8 | 12.2, 12.3 | Publish the two REST operations in their provider yaml files; align the two CaseWorkflow workflow ID forms in the sources. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06863 | RWB-P3-E2015-OPS | GAP-1818 | find it | Settle the deviation raise, clear and case-record read paths and the read owner in the S8 contract story before the screen is built. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06865 | RWB-P3-E2015-OPS | CG-ALL-4229 | 12.5 | Add an Activities row for Timer projection write on task queue rwb-case. |

### OTHER:P3 screen specification (SCR-03) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06866 | RWB-P3-E2015-OPS | DOR-RWB-P3-E2015-OPS-10 | find it | Add empty, loading, error and no-access states for SCR-03. |

### OTHER:Functional Specification Document S8 (A2.2.4.1 to A2.9.4.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06868 | RWB-P3-E2015-OPS | GAP-1823 | 7 | Rewrite each feature's AC-S8-00n-01 and its alternate and exception rows as single criteria, and carry them as evidence. Add step criteria for pause, stop, routing, clear and resume. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; RWB-P3-E2015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06870 | RWB-P3-E2015-OPS | GAP-1832 | 12 | Carry DeviationRaised and DeviationCleared keyed by case, with code, state, contact stop flag, return point and decision record reference in the envelope. No personal or financial value. |

### OTHER:Wave 2 case-record harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06872 | RWB-P3-E2015-OPS | GAP-0399 | 14 | At the wave 2 entry check, agree with the platform edge story and QA the route path, merge order, timer and deviation fixtures with fixed clocks, seeding, evidence format and retention, and pass/fail gate. |

### OTHER:FSD S8 (A2.2.2; OTHER:A2.3.2; OTHER:A2.6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06874 | RWB-P3-E2015-OPS | GAP-1817 | 12 | Replace the Quartz scheduler integration point with durable timers inside DeviationWorkflow through the workflow kit. Remove the Quartz row from this service's integration list. |

### OTHER:Functional Specification S8 (FSD v6 extract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06877 | RWB-P3-E2015-OPS | GAP-1834 | find it | Add the v1 and v2 change notes of S8 with their dates and contents to the version history; until then carry them as Not specified in the source documents. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06885 | RWB-P3-E2016-APP | DOR-RWB-P3-E2016-APP-8 | find it | Publish GET /cases/{caseId}/timeline with type=ASSIGNMENT,TRANSFER; GET /api/recovery/comms/v1/cases/{caseId}/notices; POST /api/recovery/access/v1/authorise; GET /api/recovery/access/v1/masking-policies; and the one further path in the detcheck. |

### OTHER:RWB-SVC-P3 database story and service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06887 | RWB-P3-E2016-APP | GAP-0675 | Find it | Allocate the rwb-case login name, grants limited to schema rwb_case with no privilege on another schema, and its secret reference; record them in the service catalogue. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06888 | RWB-P3-E2016-APP | GAP-0674 | Find it | Publish the gateway-bff composite route for SCR-02 and SCR-03: path, parallel calls to rwb-case and rwb-source-data, merge order, customer-field masking rules and the 2 s budget. |

### OTHER:TSD P5 T-A.2 (API-P5-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06891 | RWB-P3-E2016-APP | GAP-1059 | Find it | Serve the case-scoped read on API-P5-002 under /api/recovery/document/v1 with from and to inclusive and items carrying at, type DOCUMENT, summary, by, reference and doc_version; fix names at the RWB-P3-E2016-CON baseline review. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:API section; OTHER:P6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06894 | RWB-P3-E2016-APP | GAP-0717 | 3 | Add the case-scoped notice list GET /cases/{caseId}/notices under P6 with its query and response shape, and align the P6 contract baseline to it. |

### OTHER:05 Technical architecture/Recovery Workbench Service Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06899 | RWB-P3-E2016-CON | CG-ALL-4256 | 2 | Solution architect to rule a non-reserved Java package segment for rwb-case, replacing the reserved word 'case' in th.co.scb.ace.workbench.recovery.case (lines 65, 125, 250). Story copies it once ruled. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06901 | RWB-P3-E2016-CON | DOR-RWB-P3-E2016-CON-8 | 12.2, 12.4 | Publish the three missing operations (CG-ALL-4249 to 4251); event type already fixed in story (CG-ALL-4252). |

### RWB-P3-E2016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06903 | RWB-P3-E2016-CON | DOR-RWB-P3-E2016-CON-10 | find it | Add empty, loading, error and no-access states for SCR-03 and SCR-04. |

### OTHER:RWB-SVC-P3 (database story and service catalogue) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06905 | RWB-P3-E2016-CON | GAP-0675 | find it | Allocate the rwb-case login name and its grants (schema rwb_case only, no privilege on another schema) and record them in the service catalogue. |

### RWB-ITG-E2016-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06907 | RWB-P3-E2016-CON | GAP-0400 | find it | Agree the composite route and merge order with the platform edge story, seed the 4,000-item case from the fixture pack, and agree SIT environment, evidence format, retention and pass/fail gate with QA before wave 2 exit. |

### OTHER:Recovery Workbench TSD P5 (API-P5-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06909 | RWB-P3-E2016-CON | GAP-1059 | 12.2 | Serve the case-scoped read on API-P5-002 under /api/recovery/document/v1 with from and to inclusive, items carrying at, type DOCUMENT, summary, by, reference and doc_version; fix names at baseline review. |

### OTHER:Recovery Workbench TSD P5 (API-P5-002 and API-P5-003) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06914 | RWB-P3-E2016-CON | GAP-1060 | 12.2 | Return doc_version on the document item of API-P5-002 so the timeline shows the count, and return the full version history on API-P5-003 when an item is opened. |

### OTHER:Recovery Workbench TSD P5 (summary wording, screen review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06915 | RWB-P3-E2016-CON | GAP-1061 | 11 | Summary wording of a document timeline item recorded as Not specified in the source documents (GAP-1061). |

### OTHER:Technical specification P6; OTHER:INT-14 (rwb-integration interface definition) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06918 | RWB-P3-E2021-APP | GAP-1602 | find it | Define a versioned WIN dispatch file layout (record set, fields and order, envelope, naming, encoding, barcode and sent-date return) as a contract item before wave 2; build against a fake until agreed. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:P6 rows) and TSD P6 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06921 | RWB-P3-E2021-APP | GAP-2090 | find it | Add barcode, callback date and delivery status as fields of the notice row with no separate proof table unless the DB story of rwb-comms needs one; name the owner row for these fields. |

### RWB-P1-E1016-CON; RWB-P1-E1066-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06922 | RWB-P3-E2021-APP | GAP-2181 | 13 | Publish the DP02 contact-and-consent row and its vocabulary in RWB-P1-E1016-CON; add the LETTER append required-members table to RWB-P1-E1066-CON; add UNSERVED to LOV-SEND-STATUS with version or confirm FAILED mapping. |

### OTHER:Wave 2 harness pack (ACE integration team and QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06927 | RWB-P3-E2021-APP | GAP-0404 | 16 | Agree WIN and INT-15 fixtures, JOB-10 window control, data seeding, evidence report format and pass or fail gate for the wave entry check. |

### OTHER:SERVICE_LEVEL reference data (timer table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06929 | RWB-P3-E2021-APP | GAP-2218 | 7 | Load NOTICE_UNSERVED task code, case owner role and due date as a timer table row before the wave starts. |

### OTHER:rwb-source-data and rwb-decision published contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06930 | RWB-P3-E2021-APP | GAP-2220 | 9 | Take operation names and paths for ledger and decision-record writes from the published contracts; REST bases per R4 are /api/recovery/source-data/v1 and /api/recovery/decision/v1. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:Epic 2 story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06931 | RWB-P3-E2021-APP | GAP-3183 | 12 | Name the delivery result event and its topic in the Event and Messaging next version; delete the JOB-09 loader from the Epic 2 story set. |

### RWB-P6-E2021-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06933 | RWB-P3-E2021-APP | GAP-2094 |  | Keep GET /cases/{id}/notices as a P6 operation and settle its path; until then read case notices through GET /notices/{noticeId} per notice. |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06934 | RWB-P3-E2021-APP | GAP-2182 |  | Settle one path family for the interaction ledger with the case-scoped form; then realign the consumed row of this story and the fake in RWB-P6-E2021-CON. |

### RWB-P6-E2021-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06935 | RWB-P3-E2021-APP | GAP-2095 |  | Record the partner instruction as S9 InstructionWorkflow and the internal alert as a P3 task; rwb-comms keeps only the partner instruction template. |

### RWB-P6-E2021-CON; RWB-P6-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06936 | RWB-P3-E2021-APP | GAP-1094 |  | Fix the nine legacy fields plus holdReason, dispatchFileId and dispatchAttempts as the Notice component, all optional except id and caseId; validate the additive rule against RWB-P6-E1052-CON. |

### OTHER:Policy pack load (masking version), data dictionary (field IDs), gateway-bff (DP-19 route field list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06937 | RWB-P3-E2021-APP | GAP-0947 |  | Fix the SIT masking version in the policy pack load, publish the addressee postal address and party field IDs with mask format, and publish the SCR-18 and SCR-04 composite route field list. |

### OTHER:rwb-source-data reconciliation story (JOB-04; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06938 | RWB-P3-E2021-APP | GAP-1090 |  | Assign REC-05 to the JOB-04 reconciliation story and add the notice break count and its series there. |

### RWB-P6-E2021-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06939 | RWB-P3-E2021-APP | GAP-1093 |  | Set deployment slot and replica counts once DL35 is decided; confirm the six alert thresholds at UAT. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06941 | RWB-P3-E2021-APP | GAP-2219 |  | Allocate one key for the rwb-case slice flag (hold switch, ledger facts, NOTICE_UNSERVED task) at first build. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0398 | Integration harness values for the D7.1 decision-screen journey are not specified | Integration lead | Resolved (directive) |
| GAP-0399 | Wave 2 case-record harness: composite route, timer and deviation fixtures, environment and evidence format undefined | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0400 | Gateway-bff composite timeline route, harness environment and evidence gate are not specified | Integration lead | Resolved (directive) |
| GAP-0404 | The WIN dispatch harness pack and the proof-file test window are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0714 | Deviation read path is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0715 | No source gives the alert values for the timer projection, the degradation rate or the breach volume | DevOps lead | Resolved (directive) |
| GAP-0716 | Case interaction-ledger read has no agreed owner-side contract path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0717 | Case-scoped notice list has no Ownership Map row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0932 | The request and response shape of the authorise operation is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0934 | The object attributes an authorise request carries are not specified | Solution architect | Resolved (directive) |
| GAP-0945 | rwb-access letter dispatch loop: the TSD RBAC matrix has no Litigation column, so the LITIGATION C and R letters the legacy authority table names are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0946 | rwb-access letter dispatch loop: the authorise request and answer shape for a notice request, a notice read and a dispatch read is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0947 | rwb-access letter dispatch loop: the masking version in force in SIT, the field IDs of the addressee postal address and party field on the notice panel, and the composite route field list are not specified | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0948 | rwb-access letter dispatch loop: the role code and scope of the service identity that runs JOB-10 are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1059 | The contract shape rwb-case and rwb-document share for the case timeline is not specified | Solution architect | Resolved (directive) |
| GAP-1060 | Whether the version count of a document travels on the timeline item or only on the document detail | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1061 | The summary wording of a document timeline item is not specified | Business analyst, P5 | Resolved (directive) |
| GAP-1089 | The WIN dispatch file, its acknowledgement and the INT-15 proof result record have no layout and no owning operation in the sources | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1090 | The daily reconciliation REC-05 that the legacy story names has no owner and no mechanism in the sources | Solution architect | Resolved (directive) |
| GAP-1092 | The scope test of the notice read has no scope source in the dependencies of this story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1093 | The deployment slots, the worker placement and the alert thresholds of the dispatch loop are not stated | DevOps lead | Resolved (directive) |
| GAP-1094 | The Notice response fields and types are named by the legacy story but not specified by the contract sources | Tech lead | Resolved (directive) |
| GAP-1095 | The handoff from the Airflow WIN file window to the 16:00 Temporal Schedule has no mechanism in the sources | Solution architect | Resolved (directive) |
| GAP-1096 | The message text of MSG-P6-005 and MSG-P3-005 is not given by the legacy story or the P6 extracts | Tech lead | Resolved (directive) |
| GAP-1258 | The field-level list and the mask flags of the D7.1 approval screen are published by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1259 | The composite-route name and path segment of the approval screen are not specified | Solution architect | Resolved (directive) |
| GAP-1262 | ApprovalDecided is named on the slide 14 contract line but has no event-catalogue row | Solution architect | Resolved (directive) |
| GAP-1263 | REQ-APD-002 and REQ-APD-006 are mapped to two different features and stories | Business analyst | Resolved (directive) |
| GAP-1264 | The three notice operations of the legacy NoticeApi have no owner path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1266 | The field types and order of the screen model and the queue paging defaults are not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1267 | The legacy screen states and the platform route states are two unreconciled vocabularies | Business analyst | Resolved (directive) |
| GAP-1268 | The notice summary excludes the PDF body and the addressee that the legacy screen shows | Data steward | Resolved (directive) |
| GAP-1270 | The timeout budget of a screen that composes three reads is not specified | Solution architect | Resolved (directive) |
| GAP-1271 | The dashboard names, the alert thresholds and the empty-queue window are not specified | DevOps engineer | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1609 | The notice period timer and the transfer on a non-delivered notice are the case service's, and the trigger is not fixed | Solution architect with P3 | Resolved (directive) |
| GAP-1610 | The conduct rule set and the consent rule set have no requirement identifiers in the module's sources | Conduct and QA officer with rwb-decision | Resolved (directive) |
| GAP-1621 | Four screens are attributed to P7 while the edge ruling composes every screen in gateway-bff | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1817 | Three FSD integration points name the Quartz scheduler, which Architecture v5 and the Temporal design replace with durable timers in DeviationWorkflow | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1820 | The FSD records an approver on a deviation while the S8 row has no rwb-decision cell and no approval workflow is named for this service | Solution architect with the S8 business analyst | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1830 | The two deviation screens have no owner cell in the Architecture screen matrix and no recorded route at the edge | Solution architect | Resolved (directive) |
| GAP-1831 | The wording, the Thai version and the approver of the eight messages the service shows are not in the FSD | Business analyst, S8 | Resolved (directive) |
| GAP-1832 | The two deviation events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision log entry to travel with them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2093 | The notice approval sits in P6, P7 and S4 at once | Service owners of P6 rwb-comms, P7 rwb-decision and S4 rwb-litigation | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2095 | The partner instruction and the internal alert are rows of the design but are not rwb-comms notices in the target | Service owners of P6 rwb-comms, S9 rwb-partner and P3 rwb-case | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2106 | The WIN notices file window JOB-10 has two owners and no single accountable service | Solution architect | Resolved (directive) |
| GAP-2181 | The DP02 contact-and-consent row, the consent vocabulary, the members of the letter append and the unserved status are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2182 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2203 | No source gives the field-level detail of the two escalation columns or of the TimerBreached payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2210 | No source gives the case status history, the transfer from-queue or the decision-record read behind the timeline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2211 | No source fixes the v1.1 timeline item shape, the section state or its version against the RWB-P3-E1023-CON baseline | Solution architect | Resolved (directive) |
| GAP-2216 | No source fixes the case-facts field list behind the D7.1 approval screen, the names of the two approval outcome events, the naming of the redress task, or the business date of the postal address input | Solution architect | Resolved (directive) |
| GAP-2217 | The rwb-case slice of RWB-E2-021 owns no legacy acceptance criterion | Business analyst, P3 | Resolved (directive) |
| GAP-2218 | The task due date and the task code of an unserved letter are not stated | Business analyst, P3 | Resolved (directive) |
| GAP-2219 | No feature flag is named for the rwb-case slice | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2220 | The operation names and paths of the ledger and decision-record contracts are not in the source set | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2221 | The interaction ledger is listed in the P3 data model but owned by rwb-source-data | Solution architect | Resolved (directive) |
| GAP-2226 | Legacy occurred-time order and the case timeline page order differ | TechX | Resolved (directive) |
| GAP-2384 | The three notice decision operations of the D7.1 approval have no REST row in the Ownership Map or in appendix T-A | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2385 | The notice table has no column for the decision entry reference that the approve and hold calls carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2386 | No source says whether a change of template variant replaces the notice row or creates a new version of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2387 | The notice answer has no field list, and the template state the approval panel must show is not part of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2388 | The declared right of the three notice decision operations is not in the endpoint inventory or the RBAC matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2390 | No source says whether a notice move writes its own decision record or only references the approval entry of rwb-decision | Solution architect | Resolved (directive) |
| GAP-2391 | The hold reason vocabulary has no list of values, and the owner namespace of the feature switch is not settled for the comms half | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3183 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 result file with it | Integration lead with the communications lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E2015-CON | skipped AC ID | 87 | missing: AC7 |
