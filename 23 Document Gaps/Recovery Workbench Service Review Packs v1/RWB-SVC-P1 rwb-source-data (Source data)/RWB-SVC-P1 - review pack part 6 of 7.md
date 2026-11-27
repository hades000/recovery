# RWB-SVC-P1 rwb-source-data (Source data) - review pack, part 6 of 7 (RWB-P1-E2007-APP to RWB-P1-E2022-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 153 |
| Cross-document (pending in another document) | 240 |
| Not applied (value not in the sources) | 1 |
| Open business decisions | 37 |
| Register gaps linked | 138 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P1-E2007-APP | 20 | 44 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2007 APP Booking confirmation from the ALS load v2.md |
| RWB-P1-E2008-APP | 26 | 55 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2008 APP Payment matching with the missed payment event v2.md |
| RWB-P1-E2010-APP | 20 | 22 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2010 APP Stage 2 data products contracts, plans and treatments v2.md |
| RWB-P1-E2010-CON | 19 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2010 CON Stage 2 data products contracts, plans and treatments - contract v2.md |
| RWB-P1-E2010-OPS | 24 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2010 OPS Stage 2 data products contracts, plans and treatments - deployment v2.md |
| RWB-P1-E2021-APP | 22 | 44 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2021 APP Letter dispatch loop with proof of delivery from WIN v2.md |
| RWB-P1-E2022-APP | 22 | 32 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2022 APP SMS and LINE dispatch through NSS and LINE OA v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P1-E2021-APP | R-00415 | CG-ALL-2434 | Script gap | Product owner | The story adds POSTAL to the closed list LOV-SEND-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00416 | CG-ALL-2435 | Script gap | Product owner | The story adds RR223344556TH to the closed list LOV-SEND-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00417 | CG-ALL-2436 | Script gap | Product owner | The story adds CONTACT_STOP_X1 to the closed list LOV-SEND-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00418 | CG-ALL-2437 | Script gap | Product owner | The story adds POSTAL to the closed list LOV-CONDUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00419 | CG-ALL-2438 | Script gap | Product owner | The story adds OUT to the closed list LOV-CONDUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00420 | CG-ALL-2439 | Script gap | Product owner | The story adds POSTAL to the closed list LOV-LEDGER-EVENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00421 | CG-ALL-2440 | Script gap | Product owner | The story adds OUT to the closed list LOV-LEDGER-EVENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2021-APP | R-00422 | CG-ALL-2441 | Script gap | Product owner | The story adds OUT to the closed list LOV-SEND-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E2007-APP | R-09782 | CG-ALL-2379 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E2008-APP | R-09785 | CG-ALL-2392 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E2021-APP | R-09799 | CG-ALL-2450 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E2022-APP | R-09802 | CG-ALL-2464 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E1034-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22081 | GAP-1598 | Register gap | Product owner with the solution architect | Two of the module's business requirements describe the case record view and the case timeline, which the case service owns | Read both requirements as this service's contribution to the case record view: the notice and message block with its states, and the ordered notice and message history. The view, the timeline and the timer projection stay with rwb-case; the ledger entries stay with rwb-source-data. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22414 | GAP-1630 | Register gap | Finance and CFO delegate | The posting file has no layout, no schedule and no receiving ledger in any source | Fix one line per posting with case, account key, entry type, amount, value date, business date and posting reference, a manifest with count and checksum, and delivery through rwb-integration. Agree the layout with Finance and the ledger owner before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22415 | GAP-1632 | Register gap | Business lead | A reversed payment has no product behaviour in the FSD although the routing rules require the case to reopen | Decide whether a reversal is in scope for this service. If it is, add a reversal source value, a reversal state on the proceeds record and an event that reopens the case through rwb-case. Until then the capability is out of scope and listed as an open question. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22416 | GAP-1633 | Register gap | Finance and CFO delegate | The fee tables that the fee feature reads are not defined anywhere | Name the fee table, its owner and its schedule, and hold the fee rate, the cap and the basis as versioned rows. Until then the fee calculation has no input and the feature cannot be tested. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22419 | GAP-1636 | Register gap | Finance and CFO delegate | The order in which a receipt is applied to the balance is named but not specified | Hold the application order as versioned rows with an owner and a valid-from date, record the version on each proceeds row, and let Finance set the sequence before wave 3. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4040-APP, RWB-P6-E4040-CON, RWB-P6-E4041-APP, RWB-P6-E4041-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22551 | GAP-1607 | Register gap | Product owner | Seven features in the Communications functional specification belong to other services in Architecture v5 | Keep the seven features in the source with their identifiers, mark them as not carried in section 5.1 of this PRD with their owning service, and raise the story-level split in the service work packages. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22552 | GAP-1603 | Register gap | Business lead with the data lead | No source states the notice, message or proof-of-delivery volumes | Size the volume test on the document volume of about 860,000 in 2027 as the upper bound for letters and on the interaction volume for messages, and replace both with the measured figures when the business lead provides them. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22554 | GAP-2092 | Register gap | Service owners of P6 rwb-comms and S8 rwb-deviation; business lead | The sources name different sets of deviation codes that raise a contact stop | Read the stop as X1 to X3, which is the wider and the safer reading, keep the hold reason on the notice, and ask the business lead to correct R-LIT-05. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22562 | GAP-1091 | Register gap | Business lead | The arithmetic of the 7-day proof window on the sent date is not stated | Confirm with the business lead and Legal counsel that the window is 7 calendar days counted from the sent date and that a notice is unserved on the first run on or after sent_date plus 7 days, then record the value and the rule in the reference data with its version. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22564 | GAP-1276 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P6 business analyst and the business owner | The dispatch decision record's payload, its field placement, the rule version label, the message id set, the parameter names, a panel id and the edge right of the two reads have no source | At the design review of wave 2 the solution architect, the data steward, the P6 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the dispatch columns of decision_log_entry (new columns or jsonb members of actions and outcome), the notice-reference filter and the answer field set of the read, the rule version label of the letter rules and their registry rows, the message ids and their texts, the panel id of the decision-log view, the parameter names and version labels of the page-size bound and the ingest target, and how the right and the scope reach the two reads at the edge; until then the story holds the assumed shape of ASM-B-P7-02-E2021-1, ASM-B-P7-02-E2021-2, ASM-B-P7-02-E2021-4, ASM-B-P7-02-E2021-5 and ASM-B-P7-02-E2021-6 and its nine criteria stand on that shape |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4039-APP, RWB-P6-E4039-CON, RWB-P7-E2022-APP | R-22574 | GAP-2091 | Register gap | Service owners of P6 rwb-comms and P1 rwb-source-data; product owner | The contact point and its consent state are a P6 feature but a P1 table, and no endpoint carries them | Keep the contact point and its consent in P1 rwb_source_data.contact_point_ext as the owner of record, and have rwb-comms read and maintain it through a P1 contract that the P1 API specification publishes. |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2022-APP | R-22577 | GAP-0954 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force and the unmask rows for DF-ACE-078 and DF-ACE-077 are not recorded | Record the masking version in force per environment in the policy pack load record with its approver and valid-from date, and add both contact point fields to the pack with unmasked false for every role before the first SIT run of SCR-03 |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2022-APP | R-22584 | GAP-1274 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P6 business analyst and the business owner | The contact entry payload, the read shape, the final call of a passed check, the reason-code list, the message id set, the parameter names, the rule version label of R-LIT-03 and the login name have no source | At the design review of wave 2 the solution architect, the data steward, the P6 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the channel, the reason code and the requesting role inside actions, the request and answer field set of the two reads, the final call of a passed check, the reason-code list and its labels, the message ids and texts of this slice, the parameter names and version labels of the page-size bound and the completeness target, the rule version labels, and the per-service login name; until then the story holds the assumed shape of ASM-B-P7-02-E2022-1 to ASM-B-P7-02-E2022-4 |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2022-APP | R-22585 | GAP-1275 | Register gap | Business owner, with the solution architect, P7 rwb-decision, and the P6 business analyst | The legacy story names one decision entry only for the contact stop, while the contact check has five refusal causes and a send that passed the check | Confirm at the wave 2 design review that one decision code X6 and one final call contact refused cover every refusal of the contact check with the reason code naming the cause, add the final call of a passed check to the service vocabulary as a reference row, and state in RWB-P6-E2022-APP and in this story that the local record of DP-03 is the write that blocks the send and the central append is the ledger copy under the completeness target |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-28740 | GAP-1638 | Register gap | Product owner | The only success measure of the module has no baseline and no measurement definition | Take the measure from the decision log as the FSD says, and have the product owner set the baseline, the target and the definition of 'the same day' before the wave-2 release note. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1043-CON, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-28792 | GAP-2097 | Register gap | Service owners of P3 rwb-case and P4 rwb-access; business lead | Reference data is read from P4 in TSD P6 and from P3 in the plan default ruling | Follow R3 and DP-07: contact times and frequency are reference data of P3 rwb-case, read through C RWB-P3-E1043-CON. Access data, roles and DoA stay with P4. |
| RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-28804 | GAP-2222 | Register gap | Business lead | The legal hold reason list is not stated | Hold the reason list as a reference table of rwb-case loaded by RW-COE; the reason is stored as given until the list is approved. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P1-E2008-APP | R-35833 | ASM-0842 | Register assumption |  | Both reads are gated on DP01 Account and arrears and on the ALS row of `v_ace_batch_status` for the business date, read from this service's own `data_product_load` and view, and the answer carries the product stamp and the batch stamp it was read under. A product that is not LOADED for the date, or a batch that is not COMPLETE, absent or FAILED, answers 409 with MSG-P1-001 naming the product and the date of the load in use and MSG-P2-007 for the held run, and no row of any kind; an empty business date with a COMPLETE batch and a LOADED product answers 200 with `rowCount` 0. The run's own refusal for the business date stays RWB-P8-E2008-APP's, and DP05 is recorded as not the stamp of a payment read. | Data product owner of P1 with the P8 tech lead and the business analyst before the wave 2 exit |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P1-E2010-APP | R-04509 | DOR-RWB-P1-E2010-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources. Decision Log v11 DT05 (row 80) sets sign-off timing only. Sign-off cannot be invented; the record is needed. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03426 | RWB-P1-E2007-APP | CG-ALL-2371 | 12.1 | Add path GET /api/recovery/source-data/v1/booking-facts with the operation shape declared by RWB-P2-E2007-CON |
| CDC-03427 | RWB-P1-E2007-APP | CG-ALL-2372 | 12.1 | Add path GET /api/recovery/source-data/v1/batch-status with the operation shape declared by RWB-P2-E2007-CON |
| CDC-03432 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-8 | 12.1 | Add paths GET /api/recovery/source-data/v1/booking-facts and GET /api/recovery/source-data/v1/batch-status |
| CDC-03470 | RWB-P1-E2008-APP | CG-ALL-2383 | 12.1 | Publish GET /api/recovery/source-data/v1/payments in paths through contract story RWB-P1-E2008-CON. |
| CDC-03471 | RWB-P1-E2008-APP | CG-ALL-2384 | 12.1 | Publish GET /api/recovery/source-data/v1/accounts/{accountKey}/installment-facts in paths through contract story RWB-P1-E2008-CON. |
| CDC-03476 | RWB-P1-E2008-APP | DOR-RWB-P1-E2008-APP-8 | 12.1 | Publish GET /payments and GET /accounts/{accountKey}/installment-facts in paths of rwb-source-data.yaml. |
| CDC-03525 | RWB-P1-E2010-APP | CG-ALL-2399 | 12.1 | Publish GET /api/recovery/source-data/v1/data-products/{productCode}/records (DP04 branch) in rwb-source-data.yaml through RWB-P1-E2010-CON. |
| CDC-03547 | RWB-P1-E2010-CON | CG-ALL-2412 | 12.1 | Add path /data-products/{productCode}/records (DP04 branch, API-P1-010 shape) under base /api/recovery/source-data/v1. |
| CDC-03584 | RWB-P1-E2021-APP | CG-ALL-2443 | 1 | Remove the fixed enum on conductCheck so LOV-CONDUCT values are data; the list stays in Reference Data v5 Lists. |
| CDC-03585 | RWB-P1-E2021-APP | CG-ALL-2444 | 1 | Remove the fixed enum on eventCode so LOV-LEDGER-EVENT values are data. |
| CDC-03586 | RWB-P1-E2021-APP | CG-ALL-2445 | 1 | Remove the fixed enum on deliveryStatus so LOV-SEND-STATUS values are data. |
| CDC-03589 | RWB-P1-E2021-APP | DOR-RWB-P1-E2021-APP-8 | 12.1 | Hold conductCheck, eventCode and deliveryStatus as references to LOV-CONDUCT, LOV-LEDGER-EVENT and LOV-SEND-STATUS instead of closed enums. |
| CDC-03628 | RWB-P1-E2022-APP | CG-ALL-2455 | 12.1 | Publish GET /api/recovery/source-data/v1/contact-points through RWB-P6-E2022-CON, or remove it from section 12.1. |
| CDC-03629 | RWB-P1-E2022-APP | CG-ALL-2456 | 12.1 | Publish POST /api/recovery/source-data/v1/contact-points/{contactPointKey}/failed-contacts through RWB-P6-E2022-CON, or remove it from section 12.1. |
| CDC-03630 | RWB-P1-E2022-APP | CG-ALL-2457 | 12.1 | Publish POST /api/recovery/source-data/v1/interactions through RWB-P6-E2022-CON, or remove it from section 12.1. |
| CDC-03631 | RWB-P1-E2022-APP | CG-ALL-2458 | 12.1 | Publish GET /api/recovery/source-data/v1/interactions through RWB-P6-E2022-CON, or remove it from section 12.1. |
| CDC-03632 | RWB-P1-E2022-APP | CG-ALL-2459 | 16 | Remove the closed enum on channel so LOV-CHANNEL values are accepted as data, per Reference Data v5 Lists. |
| CDC-03636 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-8 | 12 | Add paths GET and POST /api/recovery/source-data/v1/contact-points, POST .../contact-points/{contactPointKey}/failed-contacts, GET and POST /api/recovery/source-data/v1/interactions, and the one further path. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03512 | RWB-P1-E2008-APP | GAP-0603 | 13 | Correct the P8 to P1 activity description to one REST hop wrapped by the run's Temporal activity; record the run's workload identity as operator in the RWB-P8-E2008-APP authority table. |
| CDC-03527 | RWB-P1-E2010-APP | CG-ALL-2402 | 12.5 | Register Stage2ProductWorkflow on task queue rwb-source-data in namespace rwb-recovery, or name the catalogued workflow that replaces it. |
| CDC-03532 | RWB-P1-E2010-APP | CG-ALL-2403 | 12.5 | Add an Activities row for snapshot(page) on task queue rwb-source-data, or name a catalogued activity in RWB-P1-E2010-APP section 12.5. |
| CDC-03533 | RWB-P1-E2010-APP | CG-ALL-2404 | 12.5 | Add an Activities row for writeDp04Page on task queue rwb-source-data, or name a catalogued activity in RWB-P1-E2010-APP section 12.5. |
| CDC-03534 | RWB-P1-E2010-APP | CG-ALL-2405 | 12.5 | Add an Activities row for checkActiveCount on task queue rwb-source-data, or name a catalogued activity in RWB-P1-E2010-APP section 12.5. |
| CDC-03535 | RWB-P1-E2010-APP | CG-ALL-2406 | 12.5 | Add an Activities row for stampDp04 on task queue rwb-source-data, or name a catalogued activity in RWB-P1-E2010-APP section 12.5. |
| CDC-03564 | RWB-P1-E2010-OPS | CG-ALL-2421 | 12.5 | Add a Workflows row for Stage2ProductWorkflow on rwb-source-data, or name the catalogued workflow that replaces it. |
| CDC-03567 | RWB-P1-E2010-OPS | DOR-RWB-P1-E2010-OPS-8 | 12.5 | Add the workflow and activities in section 12.5 (CG-ALL-2421 to CG-ALL-2424) to the catalog sheets, or name catalogued replacements. |
| CDC-03568 | RWB-P1-E2010-OPS | CG-ALL-2422 | 12.5 | Add an Activities row for snapshot(page) on rwb-source-data, or name a catalogued activity that replaces it. |
| CDC-03569 | RWB-P1-E2010-OPS | CG-ALL-2423 | 12.5 | Add an Activities row for writeDp04Page on rwb-source-data, or name a catalogued activity that replaces it. |
| CDC-03570 | RWB-P1-E2010-OPS | CG-ALL-2424 | 12.5 | Add an Activities row for checkActiveCount on rwb-source-data, or name a catalogued activity that replaces it. |
| CDC-03571 | RWB-P1-E2010-OPS | CG-ALL-2425 | 12.5 | Add activity stampDp04 to the Activities sheet, or name a catalogued activity in section 12.5. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03441 | RWB-P1-E2007-APP | CG-ALL-2375 | 14 | Add a new message ID for 'No session on the read' with text 'Sign in to continue.'; the story then cites it. |
| CDC-03447 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-9 | 14 | Reconcile MSG-P1-001 text with FSD P1 OQ-P1-07 wording, and confirm the meaning of MSG-P4-001 used here for no session. |
| CDC-03463 | RWB-P1-E2007-APP | CG-ALL-2374 | 4, 14 | Story use (ALS batch absent, failed or not complete) differs from the standard's Raised when; BA adds a new message ID for this refusal instead of reusing MSG-P1-001. |
| CDC-03477 | RWB-P1-E2008-APP | CG-ALL-2388 | 4, 14 | Add a new message ID for the story's 'No token' text; RWB-P1-E2008-APP then cites it. The ID does not exist yet, so the story is not edited |
| CDC-03479 | RWB-P1-E2008-APP | DOR-RWB-P1-E2008-APP-9 | 14 | Add a message ID for the 'No token' text (CG-ALL-2388) and a payment-matching wording for the run hold now cited as MSG-P2-007 |
| CDC-03516 | RWB-P1-E2008-APP | GAP-1637 | 13 | Publish wording, Thai text, channel and blocking flag for MSG-P8-001 and MSG-P8-002. |
| CDC-03523 | RWB-P1-E2008-APP | NEWAC-RWB-P1-E2008-APP-AC15 | 7 | AC11 and TC-E2-008-18 no longer name MSG-P4-001 for 401 |
| CDC-03551 | RWB-P1-E2010-CON | CG-ALL-2414 | 4, 14 | MSG-P4-001 now carries the standard's meaning and text. A message for no valid session is marked Not specified; any new ID must come from the standard. |
| CDC-03592 | RWB-P1-E2021-APP | CG-ALL-2446 | 14 | Add a new message ID for the body-validation and Idempotency-Key replay text; the story then cites it in section 14 in place of MSG-GEN-004. |
| CDC-03637 | RWB-P1-E2022-APP | CG-ALL-2460 | 14 | Add a new message ID for 'No token' with text 'Your session has ended. Sign in again.'; section 14 then cites it in place of MSG-P4-001. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03464 | RWB-P1-E2007-APP | CG-ALL-2378 | 18 | Align the REQ-CHO-008 test list in RTM v7 with section 18 of RWB-P1-E2007-APP. |
| CDC-03509 | RWB-P1-E2008-APP | CG-ALL-2391 | 18 | Align the test lists of REQ-CHO-007 and REQ-CHO-009 with RWB-P1-E2008-APP section 18 in the next RTM version. |
| CDC-03537 | RWB-P1-E2010-APP | DOR-RWB-P1-E2010-APP-12 | 12, 12.7, 16, 18 | Reconcile the section 18 test lists with RTM v7; section 16 now holds TC-E2-010-10 to TC-E2-010-13 for the contract, boundary, AC9 and AC10 tests. |
| CDC-03546 | RWB-P1-E2010-APP | CG-ALL-2408 | 18 | Align its test lists for REQ-RDF-014 and REQ-RDF-010 to section 18 of RWB-P1-E2010-APP in its next version. |
| CDC-03563 | RWB-P1-E2010-CON | CG-ALL-2417 | 18 | Align the REQ-RDF-014 and REQ-RDF-010 test lists in the RTM with section 18 of RWB-P1-E2010-CON in the next version. |
| CDC-03582 | RWB-P1-E2010-OPS | CG-ALL-2429 | 18 | Align the test lists of the three differing requirements in the next RTM version with section 18 of this story; REQ-RDF-010 list is truncated in evidence. |
| CDC-03612 | RWB-P1-E2021-APP | CG-ALL-2449 | 18 | Align the test lists of REQ-OCC-003 and REQ-OCC-005 with story section 18; full RTM v7 lists are truncated in the evidence. |
| CDC-03655 | RWB-P1-E2022-APP | CG-ALL-2463 | 18 | Align the test lists of the five listed requirements with section 18 in the next RTM version. |

### RWB-P1-E2010-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03528 | RWB-P1-E2010-APP | DOR-RWB-P1-E2010-APP-21 | n/a | Complete the build of RWB-P1-E2010-CON and publish the contract so its build status is Done. |
| CDC-03529 | RWB-P1-E2010-APP | DOR-RWB-P1-E2010-APP-22 | n/a | Publish the contract fake library and record its published version against RWB-P1-E2010-CON. |
| CDC-03543 | RWB-P1-E2010-APP | GAP-0512 | find it | Publish DP04 record property names from legacy RWB-E2-010 Data rows and API Specification v4; leave required flags and lengths to baseline review; fake the guarantee claim read. |
| CDC-03545 | RWB-P1-E2010-APP | GAP-2738 | find it | Publish GET /api/recovery/guarantee/v1/guarantee-claims?changedFrom=&changedTo=&page=&size= ordered by updated_at and id, with max size declared and 400 on empty or inverted window; declare it in RWB-P1-E2010-CON with a fake returning empty list and an error. |
| CDC-03566 | RWB-P1-E2010-OPS | DOR-RWB-P1-E2010-OPS-22 | header | Publish a contract fake library version and record its version. |
| CDC-03578 | RWB-P1-E2010-OPS | GAP-0512 | 12 | Fix DP04 property names from the legacy RWB-E2-010 data rows and API Specification v4; leave required flags and lengths to baseline review; fake the guarantee claim read. |
| CDC-03580 | RWB-P1-E2010-OPS | GAP-2738 | 12 | Publish GET /api/recovery/guarantee/v1/guarantee-claims?changedFrom=&changedTo=&page=&size= (items, window, page, size, scoped total; order updated_at, id; declared max size; 400 on empty or inverted window); fake: empty list and error. |

### RWB-P2-E2007-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03431 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-22 | 12.1 | Record the published fake library version |
| CDC-03450 | RWB-P1-E2007-APP | GAP-1713 | 12.1 | Record once in the service contract the owner service of each FEAT prerequisite: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1; carry the duplicate FEAT-CHO-08 as written. |
| CDC-03452 | RWB-P1-E2007-APP | GAP-0657 | 3 | Fix the six unsettled consumed paths and shapes with owners; allocate the rwb-integration login in RWB-PLT-DB; record TSD P2 Integration v3 T5.2 and the Architecture v5 slide 44 owner row as superseded. |
| CDC-03457 | RWB-P1-E2007-APP | GAP-0658 | find it | Baseline result shape, task table, envelope, rerun operation, twelve consumed operations and seven fakes; contract owners confirm element names; record JOB-08 owner and TSD P2 v3 T5.2 supersession in the gap register; confirm seven message texts. |
| CDC-03459 | RWB-P1-E2007-APP | GAP-0730 | find it | Fix the rwb-case login in the platform DB story; publish the composite route and treatment booking fields with RWB-P2-E2007-CON and the S2 contract; publish the raiseTask result schema; confirm route-rule and treatment-state split in build. |
| CDC-03460 | RWB-P1-E2007-APP | GAP-2486 | find it | Take the operation set from the six legacy interfaces on the DP-13 base with one hop and 2 s timeout; take the decision code from LOV-DECISION; account facts in inputs_ref, difference terms and unbooked accounts in actions; fix read filters, page size, ordering and MSG-GEN-006 text before SIT. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03433 | RWB-P1-E2007-APP | GAP-1696 | 4 | Route the payoff, collateral, NLEADS, ALS and CCMS facts through the rwb-source-data contract; add the S2 to P1 REST cell to the connection matrix. |
| CDC-03486 | RWB-P1-E2008-APP | GAP-1626 |  | Replace the slide 17 pair with the API Specification v4 pair GET /proceeds and POST /proceeds/{proceedsId}/match as the single rwb-payment contract. |
| CDC-03557 | RWB-P1-E2010-CON | GAP-0066 | - | Align the wave of rwb-guarantee (S3) with W-MAP, which is kept; EP02 stays wave 2. |
| CDC-03598 | RWB-P1-E2021-APP | GAP-2096 | none | Add the proof-arrival path: read proof through the P1 contract on the ACE batch business date, match by barcode, and publish EV-15 NoticeDelivered from rwb-comms; no new job invented. |
| CDC-03617 | RWB-P1-E2021-APP | GAP-2095 | 1 | Record the partner instruction as S9 InstructionWorkflow and the internal alert as a P3 task. rwb-comms keeps the partner instruction template only. |
| CDC-03623 | RWB-P1-E2021-APP | GAP-1609 |  | Publish NoticeDelivered for rwb-case to start the NOTICE_PERIOD timer; record the undelivered-path decision and the call to rwb-case transfer with reason NOTICE_UNSERVED; publish NoticeDispatched. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03442 | RWB-P1-E2007-APP | CG-ALL-2376 | 16 | Add row TC-E2-007-11 with Given, When and Then copied from the Principle 5 criterion it covers. |
| CDC-03478 | RWB-P1-E2008-APP | CG-ALL-2389 | 16 | Add the TC-E2-008-10 row to the next version, with Given, When and Then copied from the criterion it covers (AC10 for X8) |
| CDC-03562 | RWB-P1-E2010-CON | CG-ALL-2415 | 16 | TC-P1-E2010-CON-01 to 08, including the new 07 and 08, are not in Test Cases v8; they are added in the next Test Cases version. |
| CDC-03581 | RWB-P1-E2010-OPS | CG-ALL-2427 | 16 | Add rows TC-P1-E2010-OPS-01 to TC-P1-E2010-OPS-06 to tab Story test cases, with Given, When and Then copied from AC1 to AC6 of section 7. |
| CDC-03611 | RWB-P1-E2021-APP | CG-ALL-2447 | 16 | Map TC-E2-021-01 to -14 for RWB-P1-E2021-APP to the AC numbers in its section 16 Covers column, and add TC-E2-021-15 to -23 from that section. |
| CDC-03654 | RWB-P1-E2022-APP | CG-ALL-2461 | 16 | Section 16 keeps the story's own criterion numbering. v8 cites other criteria, including an AC12 for TC-12; QA to correct v8. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03429 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-14 | n/a | Record the signed epic design sign-off |
| CDC-03472 | RWB-P1-E2008-APP | DOR-RWB-P1-E2008-APP-14 | Header | Record the signed epic design sign-off for RWB-P1-E2008-APP. |
| CDC-03549 | RWB-P1-E2010-CON | DOR-RWB-P1-E2010-CON-14 | find it | Record the signed epic design sign-off for EP02 and confirm it against this story. |
| CDC-03565 | RWB-P1-E2010-OPS | DOR-RWB-P1-E2010-OPS-14 | header | Confirm and record the signed epic design sign-off. |
| CDC-03633 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-14 | header | Record the signed epic design sign-off for RWB-P1-E2022-APP in the epic design record. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03434 | RWB-P1-E2007-APP | CG-ALL-2364 | 1, 3, 4, 8 | Record principal_outstanding as a Section B column of v_ace_account with its object, or add the dictionary name for it. |
| CDC-03435 | RWB-P1-E2007-APP | CG-ALL-2365 | 1, 3, 4, 8 | Record settlement_booked_date as a Section B column of v_ace_account with its object, or add the dictionary name for it. |
| CDC-03436 | RWB-P1-E2007-APP | CG-ALL-2366 | 1, 3, 4, 8 | Record settlement_booked_amount as a Section B column of v_ace_account with its object, or add the dictionary name for it. |
| CDC-03437 | RWB-P1-E2007-APP | CG-ALL-2367 | 12.7, 13 | Record ace_view_owner as the object owner of the recovery views, or add the dictionary name for it. |
| CDC-03446 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-7 | 11 | Assign field IDs to principal_outstanding, settlement_booked_date and settlement_booked_amount (DF-ACC-009, DF-ACC-030, DF-ACC-031 are not in v9); register the other flagged names and ace_view_owner. |

### RWB-P8-E2008-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03475 | RWB-P1-E2008-APP | DOR-RWB-P1-E2008-APP-22 | Header | Record the published fake library version this story builds against. |
| CDC-03493 | RWB-P1-E2008-APP | GAP-1350 |  | Publish one OpenAPI 3.1 and one AsyncAPI document per service; problem+json body on every non-2xx status; MatchRequest of proceeds identifier, case, treatment, account payment and reason code; major version 1 with BACKWARD acceptance. |
| CDC-03503 | RWB-P1-E2008-APP | GAP-2494 | 4 | Fix one DecisionRecorded shape and one consumer group; take decision codes from LOV-DECISION; carry inputs_ref as opaque; keep the input age limit key as a DP-06 placeholder; publish the decision-log read page default. |
| CDC-03504 | RWB-P1-E2008-APP | GAP-2504 | header | Publish v1 with the two operations, three event schemas, nine declarations, schema baseline and message map; mark unsettled elements with the placeholder and one review row; gate the tag on contract tests and schema lint. |
| CDC-03507 | RWB-P1-E2008-APP | GAP-1347 | 4 | Publish the three event schemas (TreatmentBooked, PaymentMissed, ProceedsMatched) with their data fields and the CloudEvents envelope; keep the decision-record element with its library owner; new version for any added business field. |

### RWB-P8-E2008-APP (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03483 | RWB-P1-E2008-APP | GAP-1346 |  | Name the seven consumed rows in section 12.2 with the placeholder until each owner publishes; keep plan rows H, C, I and X; confirm scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |
| CDC-03495 | RWB-P1-E2008-APP | GAP-1354 |  | Reallocate AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP in the next split plan revision, or add a coverage note to the epic overview. |
| CDC-03500 | RWB-P1-E2008-APP | GAP-1640 | 4 | Keep one run per business date in wave 2; record the payment-received same-day trigger as an open question; add an intraday run only when an interface carrying a payment is named. |
| CDC-03505 | RWB-P1-E2008-APP | GAP-2505 | header | Ship one chart with api and worker deployments, migration job, topic and two consumer groups, five alerts with runbook links, four dashboard series, flag, backfill and rollback; take thresholds as environment values. |
| CDC-03521 | RWB-P1-E2008-APP | GAP-1349 | 12.5 | Serve case payments via GET /proceeds with case scope, no extra operation; name workflow matchPayments and its four activities; SCR-28 and run view from the edge contract (RWB-PLT-N001-CON) |

### RWB-P6-E2021-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03588 | RWB-P1-E2021-APP | DOR-RWB-P1-E2021-APP-22 | Header | Publish the fake library version for RWB-P1-E2021-APP and record it as published. |
| CDC-03601 | RWB-P1-E2021-APP | GAP-1089 | 12 | Publish WIN file name, record layout, acknowledgement fields and INT-15 proof result record, agreed at baseline review with WIN owner and rwb-integration owner. |
| CDC-03606 | RWB-P1-E2021-APP | GAP-1095 | 12 | Publish Airflow-to-Schedule handoff: window signals rwb-comms Schedule with business date, run records date, rerun of same date writes no second file. |
| CDC-03610 | RWB-P1-E2021-APP | GAP-1092 | 12.1 | Declare the capability area and the right per operation; gateway-bff asks rwb-access (DP-08) before the call; serve the scope from the rwb-case read or add C RWB-P4-E1037-CON. |
| CDC-03618 | RWB-P1-E2021-APP | GAP-1094 | 12 | Fix the Notice component with the nine legacy fields plus holdReason, dispatchFileId and dispatchAttempts; all optional except id and caseId; validate the additive rule against RWB-P6-E1052-CON. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03438 | RWB-P1-E2007-APP | CG-ALL-2368 | 11 | Assign DF-ACE field IDs to the Section B columns of v_ace_account, or confirm the frozen IDs DF-ACC-009 in the dictionary. |
| CDC-03439 | RWB-P1-E2007-APP | CG-ALL-2369 | 11 | Assign DF-ACE field IDs to the Section B columns of v_ace_account, or confirm the frozen IDs DF-ACC-030 in the dictionary. |
| CDC-03440 | RWB-P1-E2007-APP | CG-ALL-2370 | 11 | Assign DF-ACE field IDs to the Section B columns of v_ace_account, or confirm the frozen IDs DF-ACC-031 in the dictionary. |
| CDC-03513 | RWB-P1-E2008-APP | GAP-0927 | 13 | Carry filter and row count in the actions list of the decision-record entry; add capability area and right to the same list in the next LDM version. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03454 | RWB-P1-E2007-APP | GAP-0922 | 12.1 | Add POST /authorise with request and answer schema to the API specification and TSD P4 appendix T-A, stub it in the contract fake, fix the rwb-access login, publish the composite route via gateway-bff. |
| CDC-03490 | RWB-P1-E2008-APP | GAP-0925 |  | Extend the envelope with area, right, scope, resource, filter, rowCount and matrixVersion, and fix the three answer codes (allow, refuse by right, refuse by scope) at the wave 2 contract review. |
| CDC-03604 | RWB-P1-E2021-APP | GAP-0946 | 12 | Add POST /authorise with request and answer schema to API spec and TSD P4 appendix T-A; stub in contract fake; add access decision codes to ledger code list. |
| CDC-03642 | RWB-P1-E2022-APP | GAP-2321 | find it | Settle the masking version label, the covered ledger field IDs and the AC-READ granularity; name the access-log and batch-limit parameters; confirm the authorise element at contract review. |

### parameter-catalog.csv (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03465 | RWB-P1-E2007-APP | GAP-0924 | n/a | Add the cached-authorise lifetime as a parameter; value agreed at the wave 2 design review, not specified in the source documents (GAP-0924). |
| CDC-03544 | RWB-P1-E2010-APP | GAP-2696 | find it | Fix GET /treatments?changedFrom=&changedTo=&page=&size= and GET /treatments/active-count on the S2 base (page, size, total, window; max page size 1000; 400 on empty window); add a parameter row for active states (states not specified in source documents); read the three lists via GET /api/recovery/case/v1/reference-data/{tableCode} with version. |
| CDC-03579 | RWB-P1-E2010-OPS | GAP-2696 | 12 | Add GET /treatments?changedFrom=&changedTo=&page=&size= and GET /treatments/active-count (page, size, total, window; max page 1000; 400 on empty window); active-states parameter row; reference-data read with version. |
| CDC-03626 | RWB-P1-E2021-APP | GAP-2219 |  | Allocate a feature-flag key for the rwb-case slice of RWB-P1-E2021-APP at the first build, using the platform flag mechanism. |

### RWB-P6-E2022-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03634 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-21 | header | Publish the contract the message path consumes (ContactPointAnswer, FailedContactRequest, InteractionRequest, MessageLedgerEntry) and confirm the dependency. |
| CDC-03652 | RWB-P1-E2022-APP | GAP-2183 |  | Publish the contact-point read, the failed-count operation and the ledger extension; confirm delivery column types, consent renderings, channel mapping, count rule and list source at contract review. |
| CDC-03657 | RWB-P1-E2022-APP | GAP-1073 | - | Fix the MessageRequest and Interaction names and the two closed value lists; settle lengths, formats and optionality at baseline review with app and gateway-bff. |
| CDC-03658 | RWB-P1-E2022-APP | GAP-1076 | - | Hold the message status list as its own list (SENT, DELIVERED, FAILED, READ) and leave LOV-DELIVERY to the notice and proof-of-delivery capability; data steward confirms. |

### RWB-P4-AD002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03453 | RWB-P1-E2007-APP | GAP-0923 | 12.1 | Extend the RBAC matrix with Case record and Treatment and offer columns, publish the 14-area matrix as data, and confirm the RW-RESTRUCT and RW-CREDITAD letters with the matrix owner. |
| CDC-03602 | RWB-P1-E2021-APP | GAP-0945 | 12 | Add Litigation column for each role the legacy authority table names; publish 14-area matrix as data; confirm C and R letters with matrix owner. |
| CDC-03603 | RWB-P1-E2021-APP | GAP-0948 | 12 | Name JOB-10 runner service identity with role class NON_HUMAN_ACTOR, scope ALL and Litigation R row; role code Not specified in the source documents (GAP-0948). |

### OTHER:Batch and Scheduling (next version) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03539 | RWB-P1-E2010-APP | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |
| CDC-03554 | RWB-P1-E2010-CON | GAP-3176 | - | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |
| CDC-03574 | RWB-P1-E2010-OPS | GAP-3176 | none | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03540 | RWB-P1-E2010-APP | GAP-3194 | find it | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the column drop, or attach it to the creating APP story; cite the chosen story on row 121 before wave 2. |
| CDC-03555 | RWB-P1-E2010-CON | GAP-3194 | - | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 (or attach the drop to the APP story creating the table) and cite the chosen story on row 121 before wave 2 starts. |
| CDC-03575 | RWB-P1-E2010-OPS | GAP-3194 |  | Raise one ACE DB story for the 42-column drop in each of S2, S4, S5, S6, S7, P6 and P8, or attach the drop to the APP story that creates each table, and cite the chosen story on row 121 before wave 2. |

### RWB-P6-E2022-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03641 | RWB-P1-E2022-APP | GAP-1610 | find it | Govern the conduct and consent checks as one versioned rule package in rwb-decision, evaluated by rwb-comms. Package name: Not specified in the source documents (GAP-1610). First version approved by the conduct and QA officer. |
| CDC-03643 | RWB-P1-E2022-APP | GAP-1075 | find it | Declare Case record right C on the gateway-bff composite route to SCR-03 with refusals MSG-P4-002 and MSG-P4-003. Add a Case record row to T6.1 and record its reconciliation. |
| CDC-03644 | RWB-P1-E2022-APP | GAP-0405 | find it | Agree NSS and LINE OA test doubles and result-code maps with the ACE notification team; agree harness seeding, evidence format and pass gate with QA. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20806 | RWB-P1-E2008-APP | R-22408 |  | T3.1 proceeds field set and account_payment_id identity already present; no payment_missed_event_key in this doc. Data owner confirmation is open, not a document change. |
| CDC-20807 | RWB-P1-E2008-APP | R-22417 |  | Conflicts with R-22408 and R-21862, which keep account_payment_id as uuid. Dropping it for a varchar(255) payment_code column needs a data owner decision. |
| CDC-20810 | RWB-P1-E2008-APP | R-28737 |  | T5.3 already names DecisionRecorded (EV-08) on rwb.decision-record.v1, published through the DP-03 outbox. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03428 | RWB-P1-E2007-APP | CG-ALL-2373 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story holding the rwb-decision BOOKING_MATCH evaluation and correct the DP-04 row |
| CDC-03430 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-17 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story holding the rwb-decision BOOKING_MATCH evaluation |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03444 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-11 | 11 | Reconcile the personal-data class of the fields listed in section 11 with the story statement that no personal data is carried. |
| CDC-03594 | RWB-P1-E2021-APP | DOR-RWB-P1-E2021-APP-11 | 7 | Reconcile the personal-data class of the P2 fields flagged by the detcheck with the story's statement that no personal data is carried. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03445 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-12 | 16 | Story adds contract test TC-12, boundary test TC-13 and criteria tests TC-14 to TC-20; the other registers still need the rows. |
| CDC-03553 | RWB-P1-E2010-CON | DOR-RWB-P1-E2010-CON-12 | 12.7, 16, 18 | Add story test cases TC-P1-E2010-CON-01 to -07 under tab Story test cases; align RTM v7 test lists with section 18. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03448 | RWB-P1-E2007-APP | GAP-3175 | find it | Keep AceDataReady (EV-26) as the target event name on rwb.source-data.events.v1, with LoadCompleted listed as its legacy alias. |
| CDC-03480 | RWB-P1-E2008-APP | GAP-3175 | find it | List AceDataReady (EV-26) as the target name on rwb.source-data.events.v1, with LoadCompleted as its legacy alias |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03469 | RWB-P1-E2007-APP | GAP-2692 | n/a | Add booking.missing.grace_loads and the treatment-type and outcome list codes; record TreatmentBooked ownership against rwb-payment; record the stage outcome contract in the rwb-case baseline. |
| CDC-03531 | RWB-P1-E2010-APP | CG-ALL-2401 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 in the catalog and add its ACL entry. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03511 | RWB-P1-E2008-APP | GAP-1639 | 4 | Register the event-started workflows matchPayments and confirmBookings on task queue rwb-payment for JOB-07 and JOB-08. |
| CDC-03615 | RWB-P1-E2021-APP | GAP-2094 |  | Add and settle the case-level notice list path for P6. Until then, read a case's notices through GET /notices/{noticeId} per notice. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03522 | RWB-P1-E2008-APP | GAP-2496 | 13 | Decide whether the added H rows and consumed contracts named in the pattern table of RWB-P1-E2008-APP enter the dependency map |
| CDC-03627 | RWB-P1-E2021-APP | GAP-1277 | 13 | Add the six platform H dependencies, the C dependency RWB-P3-E1043-CON and the two service baselines as DP-added and baseline rows; correct the metadata rows; Ready to start stays Day 1. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03526 | RWB-P1-E2010-APP | CG-ALL-2400 | 12.2 | Publish GET /api/recovery/case/v1/cases/{caseId}/treatments and the changed-window and active-count reads in rwb-case.yaml through RWB-P3-E2004-CON. |
| CDC-03548 | RWB-P1-E2010-CON | CG-ALL-2413 | 12.2 | The case treatments read stays to be published by the provider. Section 12.2 now places the changed-window and active-count reads with S2 rwb-treatment (GAP-2695). |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03542 | RWB-P1-E2010-APP | GAP-2695 | find it | Publish GET /treatments and GET /treatments/active-count on /api/recovery/treatment/v1, with a fake for the DP04 build of rwb-source-data; the case base serves no treatment fact. |
| CDC-03651 | RWB-P1-E2022-APP | GAP-1078 |  | Declare the exception queue as a P6 administrative read over outbox rows in the exception state, or a P3 queue fed by a P6 event; name the owner before the screen is built. |

### RWB-P1-E2010-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03556 | RWB-P1-E2010-CON | GAP-0509 | - | Add the guarantee claim read of rwb-guarantee as a C dependency with its fake, and take the case-existence answer from the rwb-case contract, faked the same way. |
| CDC-03576 | RWB-P1-E2010-OPS | GAP-0509 |  | Add the guarantee claim read of rwb-guarantee as a C dependency with its fake, returning no claim until S3 is built, and take the case-existence answer from the rwb-case case contract with the same fake. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03572 | RWB-P1-E2010-OPS | DOR-RWB-P1-E2010-OPS-1 | 1 | Register role name platform engineer in v5, or the story uses a role that v5 already lists. |
| CDC-03593 | RWB-P1-E2021-APP | DOR-RWB-P1-E2021-APP-1 | 1 | Add a role code for the dispatch loop of rwb-comms (service actor), or name the existing role that holds it. |

### RWB-P1-E1066-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03595 | RWB-P1-E2021-APP | DOR-RWB-P1-E2021-APP-9 | 14 | Confirm the standard meaning of MSG-GEN-004 covers the idempotency replay and schema uses in X1, X7 and §14, or align those uses. MSG-P3-004 and MSG-P6-003 rows added to §14. |
| CDC-03616 | RWB-P1-E2021-APP | GAP-2182 | 12.1 | Settle one case-scoped path family for the ledger; realign the RWB-P6-E2021-CON fake and the RWB-P3-E2021-APP consumed row to it. This story keeps POST and GET /cases/{caseId}/interactions. |

### RWB-P3-E2021-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03613 | RWB-P1-E2021-APP | CG-ALL-2451 | 15 | SCR-04 empty, loading, error and no access states left as Not specified in the source documents (CG-ALL-2451) |
| CDC-03625 | RWB-P1-E2021-APP | GAP-2217 |  | The item concerns the rwb-case slice, not this rwb-source-data story. No story edit. |

### RWB-P6-E2021-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03622 | RWB-P1-E2021-APP | GAP-1093 |  | Set deployment slots and replica counts in the values files once DL35 is decided; confirm the six alert thresholds at UAT and record them in the runbook entries. |
| CDC-03624 | RWB-P1-E2021-APP | GAP-2106 |  | P6 rwb-comms owns the notice and the JOB-10 Schedule; P2 rwb-integration owns transport and retry and publishes FileDelivered or FileFailed to P6. |

### OTHER:rwb-case (P3) screen specification for SCR-03 and SCR-14 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03443 | RWB-P1-E2007-APP | DOR-RWB-P1-E2007-APP-10 | 9 | Add empty, loading, error and no-access states to SCR-03 and SCR-14. This story owns no screen; its error and no-access messages are in section 14. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03449 | RWB-P1-E2007-APP | GAP-2395 | find it | Name the rule package code and version labels that rwb-comms reads through the contract as fixture set; settle package assignment with the rule registry owner before integration. |

### RWB-P2-E2007-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03451 | RWB-P1-E2007-APP | GAP-1703 | Change log | Booking slice records the booking reference from TreatmentBooked and the break from PaymentMissed; rwb-payment owns booking, matching and posting; release request leaves via the integration contract. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03455 | RWB-P1-E2007-APP | GAP-2485 | Change log | Record that the booking slice evaluates BOOKING_MATCH on the version it holds through the embedded kit and restate the registry boundary once in RWB-P7-E2042-APP section 19. |

### OTHER:booking confirmation harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03456 | RWB-P1-E2007-APP | GAP-0395 | find it | Record the composite booking and treatment route path and merge order, harness environment, ALS booking fixture format, seed pack, evidence format, retention and pass or fail gate at the wave 2 entry check. |

### RWB-P2-E2007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03458 | RWB-P1-E2007-APP | GAP-0659 | find it | Fix identity, secret reference and probe checks; register workflow on rwb-integration and record the JOB-08 owner conflict; take four thresholds, series windows and backfill limit as environment values; write JOB-08 catalogue row with run book path; review four runbook entries. |

### OTHER:P7 context pack (rwb-decision ownership rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03461 | RWB-P1-E2007-APP | GAP-2487 | find it | Publish rwb.decision.BookingDecisionMade.v1 per treatment and business date on rwb.decision.events.v1, keyed by treatmentId, with outcome, row, package code and version, business date and difference terms. |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03462 | RWB-P1-E2007-APP | GAP-2691 | find it | Add the three booking operations and element names at the wave 2 contract freeze; check constraint on state with APPROVED and BOOKED; booking_difference as jsonb keyed by term name with approved and booked value; unique key per treatment and business date. |

### OTHER:Platform secret store (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03466 | RWB-P1-E2007-APP | GAP-2489 | n/a | Allocate the rwb-decision login with schema rwb_decision and record it in the platform secret store. |

### OTHER:RWB-E2-007 legacy story (sections 4; OTHER:5; OTHER:12; OTHER:13) and rwb-integration slice (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03467 | RWB-P1-E2007-APP | GAP-2491 | n/a | Record the run on queue rwb-decision at Asia/Bangkok, one run per date with MSG-P2-006 on a second start, retry on next AceDataReady, no fallback Schedule, flag off stops start. |

### OTHER:TSD P7 v2 and rwb-reporting read model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03468 | RWB-P1-E2007-APP | GAP-2492 | n/a | Create no reconciliation_result table in rwb_decision; serve counts from decision_log_entry; rwb-reporting builds the REC-03 break list from events. |

### RWB-P1-E2008-APP; 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03473 | RWB-P1-E2008-APP | DOR-RWB-P1-E2008-APP-16 | Header | Size row shows Not specified; no sizing is stated in the sources |

### RWB-P1-E2008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03474 | RWB-P1-E2008-APP | DOR-RWB-P1-E2008-APP-21 | 12.1 | Create contract story RWB-P1-E2008-CON publishing the two GET operations of 12.1 and list it as a CON dependency. |

### OTHER:Recovery Workbench FSD P6 v3 and TSD P6 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03481 | RWB-P1-E2008-APP | GAP-2395 |  | Name the Epic 2 rule package and version label that rwb-comms reads for each of the three packages; attach no notice by assumption. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; OTHER:AC3; OTHER:AC4; OTHER:AC5 of RWB-E2-008) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03482 | RWB-P1-E2008-APP | GAP-2503 |  | Record in the RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story of this split; declare the nine consumed operations on the per-service bases. |

### OTHER:Recovery Workbench FSD S2 (A2.10; OTHER:A2.11; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03484 | RWB-P1-E2008-APP | GAP-1703 |  | Remove booking, payment schedule, missed-payment count and security release writes from this service; record the TreatmentBooked and PaymentMissed references; route the release request through rwb-integration. |

### OTHER:Recovery Workbench FSD P8 v3 (A2.3.4.1 to A2.11.4.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03485 | RWB-P1-E2008-APP | GAP-1625 |  | Replace the eight placeholder acceptance criteria with testable main-flow criteria written from the statement, rules and fields, marked as new; FSD owner confirms before wave 3 system test. |

### OTHER:Recovery Workbench FSD P8 v3 (integration points of A2.1; OTHER:A2.3 to A2.11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03487 | RWB-P1-E2008-APP | GAP-1631 |  | Read ALS and ACE positions only through rwb-source-data; deliver ledger postings through rwb-integration; treat the auto-debit and LED routes as outside the 19 services until named. |

### OTHER:Recovery Workbench source contract (GAP-0599) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03488 | RWB-P1-E2008-APP | GAP-0599 | 1 | Introduced type names removed; wording restored to descriptive element names |

### OTHER:Recovery Workbench TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03489 | RWB-P1-E2008-APP | GAP-0926 |  | Publish the permission letters of all 14 LOV-CAPABILITY areas per role with the default scope of each role as a new T6.1 version, loaded through RWB-P4-AD002-APP. |

### OTHER:RWB-E2-008 v2 payment matching integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03491 | RWB-P1-E2008-APP | GAP-0393 |  | Agree the composite proceeds and exception route path and merge order, harness environment, ALS payment fixture format, seed pack, evidence format, retention and pass/fail gate at the wave 2 entry check. |

### OTHER:TSD P8 v2 T3.1; OTHER:legacy RWB-E2-008 sections 11 and 13 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03492 | RWB-P1-E2008-APP | GAP-1348 |  | Keep the TSD P8 T3.1 proceeds field set; hold payment identity on account_payment_id; replace payment_missed_event_key with the DP-09 idempotency_key table; use the next number in the service Flyway sequence; data owner confirms the payment code location. |

### OTHER:rwb-payment deployment specification (TSD P8 v2 T6.2; OTHER:T7; OTHER:Appendix T-B DL06; OTHER:DL11; OTHER:DL35) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03494 | RWB-P1-E2008-APP | GAP-1352 |  | Render the unit from the pinned chart with two api replicas; set worker floor, ceiling and sizes; create the three topics with platform partition and retention defaults; gate every environment; canary or blue/green for PROD; down script per migration. |

### OTHER:FSD P8 v3 AC-EXC-P8-001-02 and AC-EXC-P8-002-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03496 | RWB-P1-E2008-APP | GAP-1627 |  | Report the orphan as a break row on the rwb-source-data reconciliation break list with check name References; write no exception table in rwb_payment; data steward confirms the check name. |

### OTHER:FSD P8 v3 A1.2 (FEAT-PAY-06); OTHER:Epics 3 to 8 BRD 7.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03497 | RWB-P1-E2008-APP | GAP-1629 |  | Build the booking confirmation in wave 2 with EP03, the earlier date; the proceeds features stay in wave 3. |

### OTHER:TSD P8 v2 T3.1 and T3.3 (DF-FIN-004) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03498 | RWB-P1-E2008-APP | GAP-1634 |  | Keep one varchar(255) business-key column holding the ACE payment_code with no foreign key; drop the uuid cross-reference from the field list. |

### OTHER:FSD P8 v3 A2.11.2; OTHER:TSD P8 v2 T5.1 (INT-16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03499 | RWB-P1-E2008-APP | GAP-1635 |  | Reconcile to the ACE payment and account position and to the posting file delivered and confirmed by rwb-integration; record a ledger return as an open question unless the ledger owner publishes one. |

### OTHER:NFR Spec v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03501 | RWB-P1-E2008-APP | GAP-1643 |  | State the receipt count per business date as the receipt-to-installment ratio observed on busy-month ACE data in the next NFR version. |

### OTHER:Work Package B2-P7-022 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03502 | RWB-P1-E2008-APP | GAP-2493 | header | Keep the rwb-decision placement and split the record: rwb-payment writes and publishes the local record; rwb-decision holds package, rows and tests, collects records, appends to ledger and runs JOB-14, evaluates no payment. |

### RWB-S2-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03506 | RWB-P1-E2008-APP | GAP-2693 | 4 | Apply the match on ProceedsMatched and the miss on PaymentMissed through the inbox of rwb-treatment; name activities applyProceedsMatched and holdMissedInstallment; serve the position in the API-S2-002 treatment read. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03508 | RWB-P1-E2008-APP | GAP-0604 | header | Contract dependency row reverted; DP-07 stands |

### OTHER:Functional Specification P8 v3 and Technical Specification P8 v2 (T8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03510 | RWB-P1-E2008-APP | GAP-1624 | 18 | Fill the Requirements served table and TSD T8 Requirement traceability with REQ IDs for REQ-CHO-007 and REQ-CHO-009, or state that P8 has no requirement ID of its own. |

### OTHER:TSD P8 v2 (T5.3) and rwb-payment AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03514 | RWB-P1-E2008-APP | GAP-1351 | 13 | Name DecisionRecorded as a produced event whose schema is rwb-decision's, on topic rwb.decision-record.v1; publish it only through the DP-03 library. |

### OTHER:TSD P8 v2 T7 and Appendix T-B DL11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03515 | RWB-P1-E2008-APP | GAP-1353 | 13 | Hold outbox-lag, dead-letter and workflow-failure thresholds as service values with no default; close DL11 with the solution architect and platform administrator before PROD. |

### OTHER:Work Package plan (B-P1-08; OTHER:B2-P1-014) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03517 | RWB-P1-E2008-APP | GAP-2180 | 19 | Keep one Work Package per story slice; drop B2-P1-014 or RWB-E2-008 from B-P1-08 fanout; number CG rows once; add a plan-uniqueness check. |

### OTHER:FSD P7 v3 and rule registry (dry-run operation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03518 | RWB-P1-E2008-APP | GAP-2495 | 7 | Publish the dry run as a read-only operation returning testResult with total, passed, failed, failing case IDs, per-case expected and actual results, and recorded counts. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03519 | RWB-P1-E2008-APP | GAP-2497 | 13 | ACE team allocates the rwb-decision login name and role name and records them in the platform secret store. |

### OTHER:Program BRD v5, section 11 note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03520 | RWB-P1-E2008-APP | GAP-1641 | find it | Add section 5.11 (REQ-S4-010) to the note on P8 requirements in the next version. |

### RWB-P1-E1015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03524 | RWB-P1-E2008-APP | NEWAC-RWB-P1-E2008-APP-AC16 | 7, 16 | This story has two reads only and changes no status, so no criterion is added here. The disallowed-transition test belongs with the story that changes load status; confirm that owner. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03530 | RWB-P1-E2010-APP | DOR-RWB-P1-E2010-APP-8 | n/a | Apply the owner-side changes of CG-ALL-2399, CG-ALL-2400, CG-ALL-2401, CG-ALL-2402 and the four further detcheck findings. |

### OTHER:Screen specification of the P3 screens SCR-03 and SCR-45 (document not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03536 | RWB-P1-E2010-APP | DOR-RWB-P1-E2010-APP-10 | find it | Add empty, loading, error and no-access states to SCR-03 and SCR-45. |

### RWB-P1-E1015-APP; RWB-P1-E1069-APP; RWB-P1-E2010-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03538 | RWB-P1-E2010-APP | DOR-RWB-P1-E2010-APP-17 | find it | Complete the build of each named dependency before this story starts. |

### OTHER:Work Package B-P1-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03541 | RWB-P1-E2010-APP | GAP-0509 | find it | Add the guarantee claim read of rwb-guarantee as a C dependency with its fake; case existence via rwb-case RWB-P3-E2004-CON, faked the same way. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03550 | RWB-P1-E2010-CON | DOR-RWB-P1-E2010-CON-8 | find it | Add the paths named in CG-ALL-2412 and CG-ALL-2413 to the two yaml files. |

### OTHER:Screen specification of SCR-03 and SCR-45 (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03552 | RWB-P1-E2010-CON | DOR-RWB-P1-E2010-CON-10 | find it | Add empty, error and no-access states to SCR-03; add error and no-access states to SCR-45. |

### OTHER:DP04 integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03558 | RWB-P1-E2010-CON | GAP-0392 | find it | Record the composite DP04 route path and merge order, harness environment, seed pack (40 treatments, 12 plans, 5 claims), evidence format, retention and pass/fail gate at the wave 2 entry check. |

### RWB-P3-E2004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03559 | RWB-P1-E2010-CON | GAP-2696 | 18 | Publish GET /treatments (changedFrom, changedTo, page, size) and GET /treatments/active-count on the S2 base, with max page size 1000, 400 on an empty window, active states as a parameter row; read the three lists via GET /api/recovery/case/v1/reference-data/{tableCode}. |

### OTHER:rwb-guarantee service OpenAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03560 | RWB-P1-E2010-CON | GAP-2738 | 18 | Publish GET /api/recovery/guarantee/v1/guarantee-claims with changedFrom, changedTo, page and size, a declared maximum page size, 400 on empty or inverted window, and a fake with an empty list and an error. |

### OTHER:DP04 release note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03561 | RWB-P1-E2010-CON | GAP-2739 | header | Record the wave 3 rwb-guarantee claim read dependency; the DP04 guarantee part stays empty in wave 2 rather than stale. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03573 | RWB-P1-E2010-OPS | DOR-RWB-P1-E2010-OPS-12 | 12, 12.7, 16, 18 | Add rows TC-P1-E2010-OPS-01 to -08 on Story test cases tab; align section 18 test lists with RTM v7. |

### RWB-P1-E2010-APP; RWB-P1-E2010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03577 | RWB-P1-E2010-OPS | GAP-2695 |  | Publish GET /treatments and GET /treatments/active-count on /api/recovery/treatment/v1 owned by S2; remove the treatment reads from the case contract and the case base; DP04 build calls them with a fake. |

### OTHER:TSD P1 v3; OTHER:T3.1 data_product row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03583 | RWB-P1-E2010-OPS | GAP-0511 |  | Record the DP04 expected-by time as 08:00, as DL11 assumed, until the data steward confirms the value. |

### Epic design record; OTHER:EP02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03587 | RWB-P1-E2021-APP | DOR-RWB-P1-E2021-APP-14 | Header | Record the signed epic design sign-off for RWB-P1-E2021-APP. |

### RWB-P1-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03590 | RWB-P1-E2021-APP | GAP-1608 | 1 | Keep proof-of-delivery capture behind its feature flag until RWB-ACE-001 lands and v_ace_pod is available; agree the hand-entered proof fallback against the barcode with the litigation business owner before wave 2. |

### OTHER:WIN dispatch file interface definition (rwb-integration; OTHER:INT-14) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03591 | RWB-P1-E2021-APP | GAP-1602 | 1 | Hold the WIN dispatch file layout as a versioned interface definition owned by rwb-integration, a contract item before wave 2; build against a fake until agreed with the WIN owner. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:41) and FSD P6 document control change note v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03596 | RWB-P1-E2021-APP | GAP-1597 | none | Keep the notice and its proof fields in rwb-comms; read proof rows through the rwb-source-data contract and apply by barcode; assign the v_ace_pod writer question to the ACE team. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:P6 rows) and TSD P6 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03597 | RWB-P1-E2021-APP | GAP-2090 | none | Hold barcode, callback date and delivery status on the notice row, listed in the P6 object list; add a proof table only if a DB story needs it. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03599 | RWB-P1-E2021-APP | GAP-2093 | none | Remove 'Decision: child: approval' from the rwb-comms OUT list; hold ApprovalWorkflow in P7 with the notice as source; keep POST /notices/{noticeId}/approve of S4 as decision point; notice waits in Approved. |

### RWB-P1-E1016-CON; RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03600 | RWB-P1-E2021-APP | GAP-2181 | 12.1 | Publish the DP02 contact row and its vocabulary in RWB-P1-E1016-CON; add the LETTER required-members table to RWB-P1-E1066-CON; add UNSERVED to LOV-SEND-STATUS with its version or confirm the FAILED mapping with the ACE result code in source_ref. |

### RWB-ITG-E2021-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03605 | RWB-P1-E2021-APP | GAP-0404 | 16 | Agree and specify the INT-14 WIN and INT-15 fixtures and result codes, 16:00 JOB-10 window control, harness environment, seeding set, evidence report format and retention, and wave gate. |

### OTHER:Timer table reference data (SERVICE_LEVEL row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03607 | RWB-P1-E2021-APP | GAP-2218 | 7 | Load NOTICE_UNSERVED task code, case owner role and due date from the SERVICE_LEVEL row before the wave starts. |

### OTHER:Published rwb-source-data and rwb-decision contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03608 | RWB-P1-E2021-APP | GAP-2220 | 12 | Take operation names and paths from the published contracts; REST bases /api/recovery/source-data/v1 and /api/recovery/decision/v1. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03609 | RWB-P1-E2021-APP | GAP-3183 | 12 | Name delivery result event and topic that rwb-source-data publishes and rwb-comms consumes; delete JOB-09 loader from Epic 2 story set. |

### OTHER:rwb-comms story (owner of SCR-18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03614 | RWB-P1-E2021-APP | CG-ALL-2452 | 15 | SCR-18 empty, loading, error and no access states left as Not specified in the source documents (CG-ALL-2452) |

### OTHER:Message catalogue owner of MSG-P6-005 and MSG-P3-005 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03619 | RWB-P1-E2021-APP | GAP-1096 | 14 | Both rows read Not specified in the source documents (GAP-1096). |

### OTHER:RWB-P1 story set source: TSD P4 T3.1 masking_rule values; OTHER:FSD P4 A2.7 DF-PTY-007 and DF-PTY-016, gateway-bff composite route (DP-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03620 | RWB-P1-E2021-APP | GAP-0947 |  | Publish the masking version in force in SIT, the field IDs and mask format of the addressee postal address and second party field, and the composite route field list for SCR-18 and SCR-04. |

### OTHER:Reconciliation story of rwb-source-data (JOB-04; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03621 | RWB-P1-E2021-APP | GAP-1090 |  | Assign REC-05 to the rwb-source-data reconciliation story and add the notice break count and its series there. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03635 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-22 | header | Publish a contract fake library version for RWB-P6-E2022-CON and record its version. |

### OTHER:Recovery Workbench P3 screen stories for SCR-03; OTHER:SCR-04 and SCR-09 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03638 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-10 |  | Add empty, loading, error and no-access states for SCR-03, SCR-04 and SCR-09. |

### OTHER:rwb-access (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03639 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-6 | 10 | Name the authorise check of DP-08 that the REST operations of section 12 call. |

### OTHER:P2 document that uses MSG-P4-001 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03640 | RWB-P1-E2022-APP | DOR-RWB-P1-E2022-APP-9 | 14 | Use MSG-P4-001 only for 'No token' with the text 'Your session has ended. Sign in again.', as in the standard. |

### OTHER:TSD P4 v3 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03645 | RWB-P1-E2022-APP | GAP-0953 | find it | Add the Case record column and the other capability areas the stories decide on to the role-to-permission matrix; load the letters as PM-2026.12 rows. |

### OTHER:ACE notification path owner contract (INT-17; OTHER:INT-18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03646 | RWB-P1-E2022-APP | GAP-1069 | find it | Publish the request and result contract with NSS and LINE OA result-code maps before the wave 2 SIT entry. Until then, use the stub of section 12.8 of the CON story. |

### RWB-P6-E2022-APP; OTHER:JOB-11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03647 | RWB-P1-E2022-APP | GAP-1071 | 14 | Name the attempt counter and rule R-UNI-34 as the message capability's own send attempt, counted once per relay window; exclude path-internal retries. Platform relay owner confirms window semantics. |

### OTHER:ACE notification path (TSD P6 T5.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03648 | RWB-P1-E2022-APP | GAP-1072 |  | State the result transport for LINE and NSS; rwb-comms accepts a callback or a poll for a known external reference; an unknown reference is not applied. |

### OTHER:TSD P6 T5.1 and the platform chart (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03649 | RWB-P1-E2022-APP | GAP-1074 |  | Publish endpoint, certificate issuer, secret names and egress timeout; chart carries references only; egress check fails on a missing reference. |

### RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03650 | RWB-P1-E2022-APP | GAP-1077 |  | Add a template reference to the interaction record, or drop the template column from the SCR-04 timeline; until then show channel, conduct check and delivery status. |

### RWB-P4-E1037-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03653 | RWB-P1-E2022-APP | GAP-0955 |  | Publish authorise, me-permissions and masking-policies shapes in RWB-P4-E1037-CON, and the SCR-03 composite field list in RWB-PLT-N001-CON, before the send story is built. |

### OTHER:Recovery Workbench role table and access-log decision-code list (P4 rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03656 | RWB-P1-E2022-APP | GAP-0956 | - | Record the platform service identities with class and scope in the role table, and add decision codes for a message send and a refused send to the decision-code list. |

### OTHER:Recovery Workbench gaps register (DL30; OTHER:O03) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03659 | RWB-P1-E2022-APP | GAP-2105 | - | Record that rwb-comms owns the call to the ACE Common notification path for O03 and builds its own dispatch only if ACE confirms no bank-wide service; DL30 stays open until then. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20520 | RWB-P1-E2022-APP | R-15249 |  | This FSD does not use MSG-P4-001; it uses only MSG-P4-002, which is unchanged. The P2 use the item names is in another document. |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20551 | RWB-P1-E2008-APP | R-04503 |  | Size-row change belongs to the DoR owner record for RWB-P1-E2008-APP. Item 16 here is the generic gate criterion and is left as written. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_access.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20601 | RWB-P1-E2022-APP | R-28806 |  | Service identity rights and send/refused-send decision codes are absent from all sources, so adding them needs invented values. No writer exists for .sql. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0066 | Wave conflict S3 / EP02 | Tech lead | Resolved (directive) |
| GAP-0392 | DP04 integration harness: composite record route, environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0393 | Payment matching integration harness: composite proceeds and exception route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0404 | The WIN dispatch harness pack and the proof-file test window are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0405 | The NSS and LINE OA notification test doubles and the messaging harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0509 | The guarantee claim read of rwb-guarantee and the case-existence answer are not in the Work Package's contract list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0510 | The workflow and activity names of the stage 2 build are a target design choice | Solution architect | Resolved (directive) |
| GAP-0511 | The expected-by time of DP04 is assumed from the decision log and stated by no source | Data steward | Resolved (directive) |
| GAP-0512 | The field-level DP04 record schema and the shape of the guarantee claim read are not specified | Tech lead | Resolved (directive) |
| GAP-0513 | No deployment value, threshold, probe timing or fixture owner exists for the stage 2 build | DevOps lead | Resolved (directive) |
| GAP-0594 | The shapes and property names of the two booking-fact reads are in no source document | Tech lead | Resolved (directive) |
| GAP-0595 | The case's account set and its product group have no P1 read in the target | Solution architect | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0597 | The batch-status answer has two values in the legacy interface and nine fields in the view, and no source fixes which of them it returns | Tech lead | Resolved (directive) |
| GAP-0598 | No source says where the account read ends and the built match facts begin | Solution architect | Resolved (directive) |
| GAP-0599 | The two read operations, their resource and element names and their error status set are stated by no source, because the legacy read was an in-process Java interface with no path, no query parameter and no status code | Solution architect with the P8 contract owner | Resolved (directive) |
| GAP-0601 | The order of the payment answer, the fold of a repeated payment_code, the row cap of one call and the number of ALS payments per business date are stated by no source | Tech lead with the P8 contract owner | Resolved (directive) |
| GAP-0602 | Architecture v5 slide 15 names a GET /accounts/{id} of rwb-source-data that TSD P1 T-A.1 does not carry and no Work Package owns, while this story answers nextInstallmentDate | Solution architect with the P1 tech lead | Resolved (directive) |
| GAP-0603 | The caller of both reads has no actor of record after the data-load actor was retired, and the architecture names the P8 to P1 call as a Temporal activity while the Work Package fixes one REST hop | Solution architect with the P8 tech lead and the P4 owner | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0658 | rwb-integration booking confirmation (contract slice): the JOB-08 ownership and consumer lists, the ACE read boundary, the rerun placement and the twelve consumed shapes are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0659 | rwb-integration booking confirmation (deployment slice): the login and secret reference, the JOB-08 ownership, the alert thresholds, the runbook ownership and the backfill limit are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner; business on-call owner for the package alerts | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0924 | rwb-access booking confirmation: the lifetime of a cached authorise decision is not specified | Solution architect | Resolved (directive) |
| GAP-0925 | POST /authorise request and response shape is not specified for the payment-matching reads | Solution architect | Resolved (directive) |
| GAP-0926 | Permission letters for WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER and the scope of the Credit Administration role are absent from the RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0927 | The field that carries the filter and the row count in an AC-READ or AC-DENY entry is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1347 | RWB-E2-008: the three event payloads and the decision-record element are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1348 | RWB-E2-008: the proceeds field set and its idempotency tables disagree between the legacy story and TSD P8 T3.1 | Solution architect | Resolved (directive) |
| GAP-1349 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1350 | RWB-E2-008: the contract artefact names, the problem+json body, the MatchRequest shape and the registry mode of rwb-payment are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1351 | RWB-E2-008: the producer and the owner of DecisionRecorded disagree between the event catalogue and the messaging design | Solution architect | Resolved (directive) |
| GAP-1352 | RWB-E2-008: the deployment targets, the tier sizes, the rollout strategy and the rollback procedure of rwb-payment have no source | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1353 | RWB-E2-008: no source fixes a numeric target for the outbox-lag, dead-letter or workflow-failure alerts of rwb-payment | Platform administrator | Resolved (directive) |
| GAP-1354 | Legacy AC1, AC3, AC4 and AC5 of RWB-E2-008 are owned by no story in this split | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1627 | The data quality exception list that holds an unmatched payment has no home in v5 | Data architect | Resolved (directive) |
| GAP-1629 | Settlement booking confirmation is Epic 3 work in the BRD and Epic 4 work in the FSD | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1634 | The proceeds record names the ACE payment twice, once as a uuid cross-reference and once as a business key | Data architect | Resolved (directive) |
| GAP-1635 | The daily money reconciliation compares to a ledger position the Workbench does not receive | Reconciliation officer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1637 | The two run messages of this module have no wording in the message standard | Business analyst, P8 | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1640 | Payment received is a named same-day trigger under DL06 and the matching run is once per business date | Solution architect | Resolved (directive) |
| GAP-1641 | The program BRD note on P8 requirements leaves out the enforcement proceeds requirement it also cites | Business analyst, P8 | Resolved (directive) |
| GAP-1643 | No receipt volume is stated for the volume test of this service | Solution architect | Resolved (directive) |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1716 | The treatment record exists twice: as this service's live record and as P1's dated copy | Data architect | Resolved (directive) |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2093 | The notice approval sits in P6, P7 and S4 at once | Service owners of P6 rwb-comms, P7 rwb-decision and S4 rwb-litigation | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2095 | The partner instruction and the internal alert are rows of the design but are not rwb-comms notices in the target | Service owners of P6 rwb-comms, S9 rwb-partner and P3 rwb-case | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2105 | SMS and LINE dispatch stays open under DL30 while Architecture v5 gives the call to rwb-comms | Solution architect | Resolved (directive) |
| GAP-2106 | The WIN notices file window JOB-10 has two owners and no single accountable service | Solution architect | Resolved (directive) |
| GAP-2180 | Two Work Packages of the same stage write the same story file for RWB-P1-E2008-APP | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2181 | The DP02 contact-and-consent row, the consent vocabulary, the members of the letter append and the unserved status are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2182 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2183 | The rwb-source-data slice of RWB-E2-022 has no API shapes, no lists and no delivery columns in the source | TechX API owner, with the data steward (RW-DATASTEW) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2217 | The rwb-case slice of RWB-E2-021 owns no legacy acceptance criterion | Business analyst, P3 | Resolved (directive) |
| GAP-2218 | The task due date and the task code of an unserved letter are not stated | Business analyst, P3 | Resolved (directive) |
| GAP-2219 | No feature flag is named for the rwb-case slice | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2220 | The operation names and paths of the ledger and decision-record contracts are not in the source set | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2221 | The interaction ledger is listed in the P3 data model but owned by rwb-source-data | Solution architect | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2485 | The booking-confirmation decision is placed in rwb-decision while DP-04 and the registry story keep the evaluation in the owning service and state that rwb-decision never evaluates | Solution architect, with the decision service owner | Resolved (directive) |
| GAP-2486 | The operation set, paths and payloads of the batch, account, treatment, task, parameter and list contracts, the decision code, the record's snapshot and actions shape and several read and message details are in no source | Solution architect, with the owners of rwb-integration, rwb-treatment and rwb-case | Resolved (directive) |
| GAP-2487 | No source names the event that carries a booking decision out of rwb-decision, because the legacy TreatmentBooked is rwb-payment's and is raised after the treatment is booked | Solution architect, with the event platform owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2489 | The name of the rwb-decision database login is in no source | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2490 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its eleven legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2491 | The timezone, overlap, retry and fallback of the JOB-08 run and the behaviour of the legacy feature flag when off are in no source | Solution architect, with the workflow platform owner | Resolved (directive) |
| GAP-2492 | The legacy run writes the REC-03 result to reconciliation_result, and no table or owner of that name exists in the target and no source assigns the break list | Solution architect, with the reporting owner | Resolved (directive) |
| GAP-2493 | The Work Package places the payment-matching decision and its record in rwb-decision, while DP-03 keeps the record write in the owning service's transaction and DP-04 keeps the evaluation there, so no source fixes where a match record becomes central | Solution architect, with the decision service owner and the payment service owner | Resolved (directive) |
| GAP-2494 | No source names the target operations, the DecisionRecorded payload, the decision code of a missed payment, the inputs reference, the parameter key of the input age limit or the read page | Solution architect, with the owners of rwb-payment, rwb-access and rwb-case | Resolved (directive) |
| GAP-2495 | The dry-run answer of a rule-package version beyond testResult and dryRunCounts, and whether a caller may supply boundary cases, is in no source | Solution architect, with the rule registry owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2497 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2498 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2504 | rwb-payment payment matching (contract slice): the element names of the nine consumed operations, the extra event payload fields, the operation the architecture lists and the ownership map does not, and the schema baseline of proceeds are fixed by no single source | Contract owner of rwb-payment, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the event platform | Resolved (directive) |
| GAP-2505 | rwb-payment payment matching (deployment slice): the login and secret reference, the replica and threshold values, the partition and retention values, the build ID policy, the backfill limit and the runbook ownership are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2693 | The delivery route of a match to rwb-treatment, the plan-position elements and the payment frequency of a plan are not specified for the S2 slice of RWB-E2-008 | Tech lead of rwb-treatment with the P8 rwb-payment owner, the P3 rwb-case owner and the P7 rwb-decision package owner at the wave 2 contract freeze | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2695 | The owner of the treatment changed-window and active-count reads conflicts between the DP04 story and the service ownership | Solution architect | Resolved (directive) |
| GAP-2696 | The two operation shapes, the active-state rule and the reference-data read path are fixed by no source document | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2738 | No source publishes a claim-side changed-window read for the DP04 build: the operation, its path, its page parameters, its maximum size, its error mapping and a count read all have no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2739 | The owner and the timing of the dated DP04 copy of a guarantee claim conflict: the legacy story writes dp_guarantee_claim itself and puts the claim interface in Epic 4, the target gives the copy to rwb-source-data in wave 2 and the claim record to rwb-guarantee in wave 3 | Solution architect | Resolved (directive) |
| GAP-2740 | No source says which side resolves a claim whose case does not exist, or whether the claim read answers such a claim at all | Data steward | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3183 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 result file with it | Integration lead with the communications lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
