# RWB-SVC-P6 rwb-comms (Communications) - review pack, part 3 of 6 (RWB-P6-E1063-APP to RWB-P6-E2018-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 140 |
| Cross-document (pending in another document) | 199 |
| Not applied (value not in the sources) | 20 |
| Open business decisions | 29 |
| Register gaps linked | 127 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P6-E1063-APP | 19 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1063 APP Agent monitoring dashboard v1 [E2c] v2.md |
| RWB-P6-E1073-APP | 27 | 29 | 10 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v2.md |
| RWB-P6-E2013-APP | 23 | 33 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2013 APP Approval routing with the delegation of authority table v2.md |
| RWB-P6-E2014-APP | 14 | 38 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2014 APP Approval screen for D7.1 demand and recall notices v2.md |
| RWB-P6-E2017-APP | 13 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2017 APP Contract, CA and mortgage document generation screens v2.md |
| RWB-P6-E2018-APP | 25 | 28 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2018 APP E-signature flow for customers and the bank v2.md |
| RWB-P6-E2018-OPS | 19 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2018 OPS E-signature flow for customers and the bank - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P6-E2018-APP | R-01685 | CG-ALL-6519 | Script gap | Product owner | The story adds GET to the closed list LOV-SIGN-METHOD | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E2018-APP | R-01686 | CG-ALL-6520 | Script gap | Product owner | The story adds GET to the closed list LOV-SIGN-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E2018-APP | R-01687 | CG-ALL-6521 | Script gap | Product owner | The story adds GET to the closed list LOV-SIGNATURE-BASIS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E2013-APP | R-11034 | CG-ALL-6481 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E2014-APP | R-11039 | CG-ALL-6496 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E2017-APP | R-11044 | CG-ALL-6507 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22470 | GAP-1253 | Register gap | Business lead with the Center of excellence | The escalation ceiling and the service level values of an approval are not specified | Fix three values as data owned by RW-COE: the service level per decision and per default, the escalation step in working days, and a maximum escalation count with its ceiling behaviour (hold, incident to RW-RISK, or committee). Carry them as rwb.approval.service-level.*, rwb.approval.escalation.step and rwb.approval.escalation.max-levels and close DL22. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22482 | GAP-0931 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masked rendering of the addressee postal address is not specified | Let the platform masking library own one rendering per field type, record it as data beside the masking row, and add the postal address rendering to the MASK-SIT-01 pack before the first SIT run of the approval screen |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22483 | GAP-1260 | Register gap | Business lead | The limit that applies on the approval screen conflicts with D7.1 carrying no amount limit | Show the approval level and the route role as the limit that applies for D7.1 (no amount, level none) and read the DoA table only where an amount-bearing decision uses the screen; confirm with Risk and Credit. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22514 | GAP-0943 | Register gap | Compliance and PDPA officer | rwb-access document set: the masking version in force for SIT and the field IDs of the personal fields on the review view are not specified | Fix the mask version label per environment in the policy pack load, publish the field IDs of a generated contract and its parties with the LDM, and have the pack owner confirm the DF-PTY-007 and DF-PTY-016 rows before SIT. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22516 | GAP-1582 | Register gap | Legal counsel | E-discovery and court-ready evidence have no FSD feature, no operation and no response target | FR-P5-028, FR-P5-029 and AC-P5-021 carry the behaviour with the response target left open as OQ-P5-09. A discovery operation and its response target are needed before wave 2 acceptance. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E1063-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P4-E1063-APP, RWB-P6-E1063-APP | R-28650 | GAP-1213 | Register gap | data steward, data product owner and architecture owner | REQ-DRI-009 still requires a daily copy to the data lake, which DP-17 and Arch v5 slide 37 remove | Reword REQ-DRI-009 in the next BRD version as the daily agent measures being available for reporting from rwb-reporting with the row counts matched against the P10 source, keep the requirement identifier, and record that the P6 slice carries only the cost-alert notification, as ASM-B-P6-05-E1063-6 sets out. |
| RWB-ITG-E1073-ITG, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28681 | GAP-0006 | Register gap | RW-COE and RW-RISK | Rule format XLS decision tables or DMN 1.6 | Keep XLS tables for the Phase 1 packages and convert one table at a time, with both formats on the same runtime |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28693 | GAP-2047 | Register gap | Solution architect with Risk and Internal Audit | The decision log is now written locally by each service and sealed centrally | Version 4 measures the local decision record of each service and the central ledger of P7 rwb-decision as two instances of the same two alerts, with the chain check read per service and once for the ledger. |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28694 | GAP-2051 | Register gap | P7 rwb-decision with Compliance and Internal Audit | The hash chain check now spans 19 local chains and one central ledger | Version 4 raises the alert on the local chain of each service and once on the central ledger, and attributes a break to the service whose chain fails; the run book of RWB-E1-073 and RWB-E2-037 names the check. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28769 | GAP-0933 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force in SIT is not recorded anywhere | Record the masking version in force per environment in the policy pack load record, with its approver and valid-from date, and assert it in the SIT entry check |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28770 | GAP-1261 | Register gap | Data steward and data product owner | The module specification keeps two daily data-lake interfaces that DP-17 removes | Retire INT-19, INT-20 and the daily copy from the P7 documents in the next module-specification version; no lake element appears in this key's stories, chart or run book. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P6-E1063-APP | R-06442 | DOR-RWB-P6-E1063-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources; searched the folder and 23 Document Gaps. Sign-off cannot be confirmed without inventing it. |
| RWB-P6-E1063-APP | R-06445 | DOR-RWB-P6-E1063-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded as published in the source documents. Stating one would invent a value, so the item stays open. |
| RWB-P6-E1063-APP | R-26029 | CG-ALL-6453 | 13 | Flyway file V1063_1__agent_cost_alert_notice.sql is not in the V0001..Vnnnn form | Next rwb_comms Flyway number is not stated in Service Template Specification v1 section 3.1 or elsewhere in the sources; V1063_1 cannot be corrected without inventing a number. |
| RWB-P6-E1073-APP | R-06450 | DOR-RWB-P6-E1073-APP-16 | Header | Definition of Ready item 16 Size: Fail | The squad sizing at refinement is not in the sources; no value or process invented. |
| RWB-P6-E1073-APP | R-06453 | DOR-RWB-P6-E1073-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version in the sources; recording one would invent a value. Not specified in the source documents (DOR-RWB-P6-E1073-APP-22). |
| RWB-P6-E1073-APP | R-11026 | CG-ALL-6463 | 14 | MSG-P3-027 text differs from the Error and Message Standard v4 | Error and Message Standard v4 wording is not in the sources (see R-17627); the rewrite invented text. |
| RWB-P6-E1073-APP | R-17625 | DOR-RWB-P6-E1073-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Section 8 and the BR11 and BR12 test rows are outside this chunk; only the ALLOC synthetic marking is done. |
| RWB-P6-E1073-APP | R-17627 | DOR-RWB-P6-E1073-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | Error and Message Standard v4 is not in the sources (folder searched). MSG-P3-027 wording stays unchanged. Not specified in the source documents (DOR-RWB-P6-E1073-APP-9). |
| RWB-P6-E1073-APP | R-26032 | CG-ALL-6464 | 16 | Test cases cover other criteria in Test Cases v8 | Test Cases v8 cache mapping covers only 11 of 13 rows and lacks AC8-AC10 in section 7; aligning would invent covers. Not specified in the source documents (CG-ALL-6464). |
| RWB-P6-E1073-APP | R-26033 | CG-ALL-6466 | 3, 3.1 | Flyway file V1073_1__local_rule_copy.sql is not in the V0001..Vnnnn form | Migration name is at line 378, outside this chunk; next rwb-comms Flyway number is not in the sources. Not specified in the source documents (CG-ALL-6466). |
| RWB-P6-E1073-APP | R-28687 | GAP-2031 |  | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | Story sections naming RulePackageEffectiveDateJob are outside this chunk, so no exact old text can be matched. Edit needed in a later chunk. |
| RWB-P6-E1073-APP | R-28691 | GAP-2030 | 19 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | Section 19 delivery-ownership text is not in this chunk, so no exact old text can be matched. Needs the section 19 edit in a later chunk. |
| RWB-P6-E1073-APP | R-31294 | NEWAC-RWB-P6-E1073-APP-AC18 | 7 | AC18: §8 BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | BR11 and BR12 need a section 7 criterion and a section 16 row. Neither section's text is fully in this chunk, so no exact anchor can be matched. Needs a later chunk. |
| RWB-P6-E2014-APP | R-11038 | CG-ALL-6492 | 4, 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 §4 has no 401 or no-session message; MSG-GEN-006 is system-unavailable only and does not fit. Placeholder in 12.1 kept for the business analyst. |
| RWB-P6-E2014-APP | R-17634 | DOR-RWB-P6-E2014-APP-11 | 3 | Definition of Ready item 11 Guardrails: Partial | Data Classification v5 was not found in the readable sources (06 Data searched), so the personal-data field list cannot be named. Data owner to check. |
| RWB-P6-E2014-APP | R-26044 | CG-ALL-6497 | 3, 3.1 | Flyway file V2014_1__notice_decision_reference.sql is not in the V0001..Vnnnn form | The migration name is not in the supplied story text (line 244 is DF-LEG-016), and the next rwb-comms Flyway number is not in the sources read. |
| RWB-P6-E2018-APP | R-06480 | DOR-RWB-P6-E2018-APP-8 | 12.1 | Definition of Ready item 8 Contract: Fail | No 401 message ID in Error and Message Standard v4 (MSG-GEN-006 is for unavailability only); placeholder kept. Event name is in section 13, not supplied; no edit. |
| RWB-P6-E2018-APP | R-11045 | CG-ALL-6522 | 12.1 | HTTP errors with no message ID: 401 no session | No 401 message ID in Error and Message Standard v4 (probe cache); MSG-GEN-006 covers unavailability only. Placeholder kept in 12.1 for the business analyst. |
| RWB-P6-E2018-APP | R-17650 | DOR-RWB-P6-E2018-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Criteria and test rows for BR10 to BR15 sit in sections 7 and 16, not in the supplied text; no AC or test row can be added here. |
| RWB-P6-E2018-APP | R-26054 | CG-ALL-6525 | 3 | Flyway file V2018_1__esign_indexes.sql is not in the V0001..Vnnnn form | Next number in the rwb_comms V0001 to Vnnnn sequence is not in the sources; Service Template Spec v1 section 3.1 gives the rule only. Placeholder kept. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10990 | RWB-P6-E2014-APP | CG-ALL-6489 | 12.1 | Publish POST /notices/{noticeId}/approve in rwb-comms.yaml through the RWB-P6-E2014-CON story |
| CDC-10991 | RWB-P6-E2014-APP | CG-ALL-6490 | 12.1 | Publish POST /notices/{noticeId}/regenerate in rwb-comms.yaml through the RWB-P6-E2014-CON story |
| CDC-10992 | RWB-P6-E2014-APP | CG-ALL-6491 | 12.1 | Publish POST /notices/{noticeId}/hold in rwb-comms.yaml through the RWB-P6-E2014-CON story |
| CDC-10996 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-23 | header | State the exact contract version the story builds against; only the /v1 path is in the sources |
| CDC-10997 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-8 | 12.1 | Publish the three POST paths (approve, regenerate, hold) in rwb-comms.yaml as in CG-ALL-6489 to 6491 |
| CDC-20745 | RWB-P6-E1063-APP | R-22229 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20749 | RWB-P6-E2014-APP | R-01674 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20750 | RWB-P6-E2014-APP | R-01673 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01653', 'R-01657', 'R-01659', 'R-01660', 'R-01663', 'R-01673', 'R-01674', 'R-06411', 'R-06427', 'R-21954', 'R-2 |
| CDC-20784 | RWB-P6-E2014-APP | R-22484 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20785 | RWB-P6-E2014-APP | R-06469 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20787 | RWB-P6-E2014-APP | R-06468 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20791 | RWB-P6-E2014-APP | R-01675 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20792 | RWB-P6-E2014-APP | R-22486 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20794 | RWB-P6-E2018-OPS | R-22347 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10923 | RWB-P6-E1063-APP | GAP-1517 |  | Read the daily measure as a projection over the run record per agent, version and business date, idempotent on the date; leave physical name and retention to the technical specification. |
| CDC-10944 | RWB-P6-E1073-APP | GAP-2457 | 11 | Add the physical columns, types and nullability of rule_package, rule_package_version, rule_row and rule_test_case, using the field names of legacy section 11 and the artifact columns confirmed with RWB-PLT-E1072-CON. |
| CDC-10957 | RWB-P6-E2013-APP | CG-ALL-6469 | 13 | Add field approval_ref to entity notice, the field the migration of RWB-P6-E2013-APP adds |
| CDC-10958 | RWB-P6-E2013-APP | CG-ALL-6470 | 13 | Add field escalation_level to entity notice, the field the migration of RWB-P6-E2013-APP adds |
| CDC-10963 | RWB-P6-E2013-APP | DOR-RWB-P6-E2013-APP-7 | 11 | Add notice.approval_ref and notice.escalation_level as fields of notice, and the other assumed notice columns of section 11 |
| CDC-10998 | RWB-P6-E2014-APP | CG-ALL-6486 | 11 | Confirm party_id as a dictionary field or record the object in the owning document; nearest dictionary names are partner_id, party_ext, party_role |
| CDC-10999 | RWB-P6-E2014-APP | CG-ALL-6487 | 11 | Add decision_log_entry_id as a notice field, or record the object in the owning document; nearest names are decision_log_entry, decision_log_id, decision_code |
| CDC-11010 | RWB-P6-E2014-APP | GAP-2385 | 11 | Add nullable decision_log_entry_id uuid to notice with a unique index, written by approve and hold, before the wave 2 build |
| CDC-11053 | RWB-P6-E2018-APP | DOR-RWB-P6-E2018-APP-7 | 11 | Register DF-DOC-103 (signature_request field within DF-DOC-096 to DF-DOC-107) in LDM v9 or correct its ID to the LDM value. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10965 | RWB-P6-E2013-APP | CG-ALL-6472 | 12.1 | Add a message ID for 401 no session; the business analyst supplies it |
| CDC-10967 | RWB-P6-E2013-APP | CG-ALL-6477 | 4, 14 | Add a new message ID for notification path unavailable or merge value absent, then the story cites it |
| CDC-10968 | RWB-P6-E2013-APP | DOR-RWB-P6-E2013-APP-9 | 14 | MSG-GEN-006 reverted to the placeholder; no standard text used |
| CDC-11031 | RWB-P6-E2017-APP | CG-ALL-6501 | 4, 14 | Add a new message ID for 'The template id is unknown, or the template is outside the scope'; the story then cites it in §14 in place of MSG-P4-003. |
| CDC-11032 | RWB-P6-E2017-APP | CG-ALL-6502 | 4, 14 | Add a new message ID for 'A version of a code of the set has no Legal approval'; the story then cites it in §14 in place of MSG-P5-010. |
| CDC-11033 | RWB-P6-E2017-APP | CG-ALL-6503 | 4, 14 | Add a new message ID for 'A code of the set is withdrawn and no later version is approved'; the story then cites it in §14 in place of MSG-P6-003. |
| CDC-11099 | RWB-P6-E2018-OPS | GAP-2357 | 14 | Add an rwb-document message for refusing a result on a SIGNED, DECLINED or EXPIRED signature request at the next message standard version. Confirm Documents C, R and U as the operation-level rights of the signature-request operations in the RBAC matrix. |

### RWB-P5-E2017-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11043 | RWB-P6-E2017-APP | GAP-1278 |  | Publish the rwb.decision-record.v1 payload field set, the correction final call, the reference shapes, the two parameter names and the MSG-P4-003 text. |
| CDC-11046 | RWB-P6-E2017-APP | GAP-1017 |  | Declare the seven generation-screen operations, their paths, request and answer fields, failure envelope and status map, and the decision record name per GAP-1017 (ASM-113 to ASM-116). |
| CDC-11051 | RWB-P6-E2018-APP | DOR-RWB-P6-E2018-APP-5 | 9 | Define QUEUED, SENT, SIGNED, DECLINED and EXPIRED as a signature request value list separate from LOV-CASE-STATUS. |
| CDC-11055 | RWB-P6-E2018-APP | GAP-1182 |  | Publish create, read-by-external-reference and update operations for signature_request before wave 2 exit. |
| CDC-11058 | RWB-P6-E2018-APP | GAP-1186 |  | Publish whether the version add takes the signed PDF bytes in the body or returns an upload link before rwb-comms streams the signed PDF. |
| CDC-11083 | RWB-P6-E2018-OPS | GAP-1182 | 12 | Publish create, read-by-external-reference and update operations for signature_request. |
| CDC-11086 | RWB-P6-E2018-OPS | GAP-1186 | none | Publish whether the version add takes the signed PDF bytes in the body or returns an upload link. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10910 | RWB-P6-E1063-APP | CG-ALL-6451 | 12.4 | Event name flagged as to be added to the catalogue; owner Not specified in the source documents. |
| CDC-10912 | RWB-P6-E1063-APP | DOR-RWB-P6-E1063-APP-8 | 12.4 | Add rwb.agent.AgentAlertRaised.v1 to the Events sheet on topic rwb.agent.events.v1, or name a catalogued event type. Same change as CG-ALL-6451. |
| CDC-10933 | RWB-P6-E1073-APP | DOR-RWB-P6-E1073-APP-8 | 4, 12.4 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} in the rwb-decision API; reconcile the DecisionRecorded event type name to one value; add rwb-comms as consumer of rwb.decision.RulePackageInForce.v1. |
| CDC-10935 | RWB-P6-E1073-APP | CG-ALL-6459 | 12.4 | Add rwb-comms as consumer of rwb.decision.RulePackageInForce.v1 (EV-30) in the Events row and its ACL. |
| CDC-10966 | RWB-P6-E2013-APP | CG-ALL-6476 | 12.4 | Add rwb-comms as a consumer of rwb.decision.ApprovalRequested.v1 (EV-09) and add its ACL |
| CDC-10979 | RWB-P6-E2013-APP | GAP-1221 |  | Add rwb-comms as consumer of rwb.decision.ApprovalRequested.v1 (re-published with raised escalation level and new due time); do not add ApprovalEscalated; keep TimerBreached as legacy reference. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10924 | RWB-P6-E1063-APP | GAP-1519 |  | Keep JOB-15 as the P9 reporting extract and give rwb-agent its own daily aggregation step triggered once per business date after the run record closes. |
| CDC-10934 | RWB-P6-E1073-APP | GAP-1329 | 4 | Fix one registry family (/admin/rule-versions per API Specification v4 and RWB-ITG-E1073-ITG) in API Specification v4 and the Ownership Map; publish GET /rule-catalog as an owned operation or remove it from the consumed set. |
| CDC-10939 | RWB-P6-E1073-APP | GAP-0383 | 13 | Assign one package code and version label to rwb-comms and one to rwb-integration; add GET /rule-models/{packageCode}/{versionLabel} with the checksum under P7 rwb-decision; publish the refused load keeping MSG-P3-027 and its {check} values. |
| CDC-10940 | RWB-P6-E1073-APP | GAP-0700 | 12 | Add the seven operations (load, version list, approve, rollback, dry run, model read, catalog read) with rights, answers and error codes; publish packageCode, versionLabel, checksum and catalogue element names. |
| CDC-10969 | RWB-P6-E2013-APP | GAP-1623 | 8 | Record that P3 moves the case state and raises the approval task on ApprovalRequested; state the choice in FSD A2.15 and A2.16 acceptance criteria. |
| CDC-11020 | RWB-P6-E2014-APP | GAP-2742 | n/a | Declare owner of DF-LEG-015 to DF-LEG-023 and DF-REF-045 to DF-REF-051; name P6 notice generate/send and rwb-case answer operations; add REQ-S4-001; decide D7.1 approval conflict. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10947 | RWB-P6-E1073-APP | GAP-2396 | 3 | Correct the P6 Comms to P7 Decision cell of the connection matrix to show the RulePackageInForce event subscription. |
| CDC-11061 | RWB-P6-E2018-APP | GAP-1188 | 12.4 | Add a cancel operation for P3 on /api/recovery/comms/v1 or an event from P3 that P6 consumes, and name it in P3's expiry story. |
| CDC-11067 | RWB-P6-E2018-APP | GAP-2700 | 12.9 | Publish the signature record on the update operation of /api/recovery/treatment/v1 with a fake, and record the later move to a Temporal activity. |
| CDC-11068 | RWB-P6-E2018-APP | GAP-2701 | 12.9 | Give rwb-treatment the signature record and window closure, rwb-document the request and signed version, rwb-comms the basis and circuit, reconciled on the published operation and events. |
| CDC-11090 | RWB-P6-E2018-OPS | GAP-1596 |  | Remove signature_request from the rwb-comms data model; state that rwb-comms owns the request operation and flow via the rwb-document contract. Confirm the status read path with P5 before wave 2. |
| CDC-11094 | RWB-P6-E2018-OPS | GAP-2700 |  | Publish the signature record on the update operation of /api/recovery/treatment/v1 with a fake for same-day build; record that a later Temporal move changes only the client, not section 7 criteria. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10986 | RWB-P6-E2013-APP | CG-ALL-6480 | 18 | Restate the test case lists of REQ-APD-001 to REQ-APD-011 to the section 18 lists of RWB-P6-E2013-APP |
| CDC-11045 | RWB-P6-E2017-APP | CG-ALL-6506 | 18 | Align the test lists of REQ-DCM-012, REQ-OCC-002 and the third requirement with section 18 of RWB-P6-E2017-APP in the next RTM version. |
| CDC-11052 | RWB-P6-E2018-APP | DOR-RWB-P6-E2018-APP-12 | 16 | Align the RWB-P6-E2018-APP test lists with TC-E2-018-01 to TC-E2-018-14 in section 18. |
| CDC-11072 | RWB-P6-E2018-APP | CG-ALL-6524 | 18 | Align the REQ-OCC-009 test list between section 18 and RTM v7 in their next versions |
| CDC-11076 | RWB-P6-E2018-OPS | DOR-RWB-P6-E2018-OPS-12 | 16 | Add TC-E2-018-13 (AC8) to the RWB-P6-E2018-OPS test list in RTM v7 |
| CDC-11097 | RWB-P6-E2018-OPS | CG-ALL-6532 | 18 | Align the REQ-OCC-009 test list in the RTM to TC-E2-018-01, TC-E2-018-02, TC-E2-018-03, TC-E2-018-04 and TC-E2-018-06, as in story section 18. |

### RWB-P7-E2014-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11003 | RWB-P6-E2014-APP | GAP-1623 | find it | Record that a P3 reaction to ApprovalRequested moves the case to Waiting approval and raises the task, so P3 is the one writer of case state |
| CDC-11012 | RWB-P6-E2014-APP | GAP-2387 | not in chunk | Baseline the notice answer fields id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt and decisionLogEntryId, with template states DRAFT, APPROVED and WITHDRAWN. |
| CDC-11016 | RWB-P6-E2014-APP | GAP-1258 | not in chunk | Publish the field list and mask flags of the approval and case panels as the working read, confirm with the route owner and the three consumer sign-offs, and correct by a new contract version. |
| CDC-11017 | RWB-P6-E2014-APP | GAP-1259 | not in chunk | Carry GET /api/recovery/approvals/{approvalId} as the working read and register it with the route owner at the first version freeze. |
| CDC-11018 | RWB-P6-E2014-APP | GAP-1267 | not in chunk | Keep READY, STALE_INPUT, DECIDED, GENERATED, APPROVED and HELD as panel states; treat loading, temporarily unavailable and session expired as route overlay states, per its AC4. |
| CDC-11024 | RWB-P6-E2014-APP | GAP-1266 | n/a | Fix queue page size default at 20 and maximum at 100; publish field types and screen model field order. |

### RWB-P10-E1063-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10911 | RWB-P6-E1063-APP | DOR-RWB-P6-E1063-APP-21 | Header | Contract dependency already in header; no change. |
| CDC-10916 | RWB-P6-E1063-APP | GAP-0617 |  | Fix the read on /api/recovery/agent/v1 with the five API-P10-009 parameters, a declared page size and cursor, the aggregate figures, the held-date status members and the AgentRunDailyRollup Schedule as proposed. |
| CDC-10919 | RWB-P6-E1063-APP | GAP-0616 |  | Serve the daily aggregate from rwb-agent on GET /api/recovery/agent/v1/admin/agent-metrics, feed rwb.agent.AgentRunCompleted.v1 to rwb-reporting, and run AgentRunDailyRollup at 01:30 with overlap SKIP. |
| CDC-10922 | RWB-P6-E1063-APP | GAP-1211 |  | Publish an agent alert event on rwb.agent.events.v1 and send the cost alert on the case-bound P6 message operation with the alert reference in the case position, per ASM-B-P6-05-E1063-1 and -2. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10930 | RWB-P6-E1073-APP | DOR-RWB-P6-E1073-APP-14 |  | Record the signed epic design sign-off for RWB-P6-E1073-APP; the sign-off is not in the story or the source documents. |
| CDC-10960 | RWB-P6-E2013-APP | DOR-RWB-P6-E2013-APP-14 | Metadata | Record the signed epic design sign-off. |
| CDC-10993 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-14 | header | Record the signed epic design sign-off for RWB-P6-E2014-APP |
| CDC-11028 | RWB-P6-E2017-APP | DOR-RWB-P6-E2017-APP-14 | find it | Record the signed epic design sign-off for EP02 in the epic design record; the story then cites it. |

### RWB-P7-E2013-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10962 | RWB-P6-E2013-APP | DOR-RWB-P6-E2013-APP-22 | Metadata | Publish the contract fake and record its library version. |
| CDC-10972 | RWB-P6-E2013-APP | GAP-1251 | 10 | State that the level lookup is a read with a 2 s budget and that the approval stores delegation_limit_id, approval_level and limit_version only, with no join, view or foreign key into rwb_access. |
| CDC-10977 | RWB-P6-E2013-APP | GAP-0929 |  | Freeze the DoA lookup and authority-decision request and response field sets; outcome values COVERED, NO_HOLDER, NOT_COVERED, NO_AMOUNT_LIMIT, RELATED_PARTY; requiredLevel on refused decisions. |
| CDC-10981 | RWB-P6-E2013-APP | GAP-1255 |  | Baseline the five approval resources and the case-status operation from TSD P7 T3.1 field names in camelCase with platform page and error conventions; fix the required property of ApprovalAction. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10976 | RWB-P6-E2013-APP | GAP-0928 |  | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses; correct the v4 omission under R-PREC. |
| CDC-11064 | RWB-P6-E2018-APP | GAP-2352 | 12.2 | Add the five signature-request operations with API IDs, paths and query names, settled with rwb-comms in the same review. |
| CDC-11088 | RWB-P6-E2018-OPS | GAP-1188 |  | Add a cancel operation for P3 on expiry (or a P3 event that P6 consumes) and name it in the P3 expiry story. Story sections not in chunk; AC6 unchanged. |
| CDC-11091 | RWB-P6-E2018-OPS | GAP-2352 |  | Add the five signature-request operations with API IDs, paths, and settled query names for the list and external-reference read agreed with rwb-comms. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10929 | RWB-P6-E1073-APP | CG-ALL-6457 | 13 | Create story file RWB-P7-E1073-CON for the rwb-decision rule-model contract, or name the existing story that holds that capability. |
| CDC-10931 | RWB-P6-E1073-APP | DOR-RWB-P6-E1073-APP-17 | 13 | Create story RWB-P7-E1073-CON or name the existing story for the rwb-decision contract that the dependency names. |
| CDC-10932 | RWB-P6-E1073-APP | DOR-RWB-P6-E1073-APP-21 | 13 | Create the contract story for RWB-P7-E1073-CON (rwb-decision rule-model operation) so the contract dependency it names exists. |

### RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11019 | RWB-P6-E2014-APP | GAP-1270 | not in chunk | Register the approval screen route with a 2 s budget per downstream and the 1.2 s composition budget of the case screen; record the measured p95 on the dashboard. |
| CDC-11044 | RWB-P6-E2017-APP | GAP-0401 |  | Publish the gateway-bff composite route path, merge order, wave 2 harness repository, environment, seeding, evidence format and pass/fail gate with QA. |
| CDC-11047 | RWB-P6-E2017-APP | GAP-0944 | find it | Publish the composite route field list for SCR-14 and SCR-30 with the gateway-bff contract, and add the allowed-action decision code to the decision-code list before the audit query is built. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10952 | RWB-P6-E1073-APP | GAP-1219 |  | Name every service that evaluates a rule package in the consumers of RulePackageInForce, rwb-comms included, or publish the package-to-service map. |
| CDC-10982 | RWB-P6-E2013-APP | GAP-1257 |  | Either add ApprovalDecided to the event catalogue with a number and consumers, or remove it from slide 14 and rely on DecisionRecorded; no story publishes it until decided. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10954 | RWB-P6-E1073-APP | GAP-2460 |  | Register rules.testcases.min with value 50 as assumed, to be confirmed by RW-COE at the first package load; the guard reads the parameter and no value is written in code. |
| CDC-11026 | RWB-P6-E2014-APP | GAP-2391 | 8 | BR11 names the hold reasons and marks their list of values as Not specified; no LOV ID is given |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10978 | RWB-P6-E2013-APP | GAP-0930 |  | Add the rwb-decision service identity with Approval check R and no other Recovery right; security administrator confirms before the authorise contract is frozen. |
| CDC-11080 | RWB-P6-E2018-OPS | DOR-RWB-P6-E2018-OPS-1 | 1 | Add the role 'platform engineer' or confirm the role code this story uses |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10985 | RWB-P6-E2013-APP | CG-ALL-6478 | 16 | Restate the AC column of TC-E2-013-01 to -16 to the AC numbers of RWB-P6-E2013-APP section 16; add TC-E2-013-17 to -30, which v8 lacks |
| CDC-11034 | RWB-P6-E2017-APP | CG-ALL-6504 | 16 | Add rows TC-P6-E2017-APP-01 (covers AC1, AC5) and TC-P6-E2017-APP-02 (covers AC7) with Given, When and Then copied from those criteria. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11000 | RWB-P6-E2014-APP | CG-ALL-6488 | 8 | Add list LOV-OVERRIDE-REASON to Reference Data v5 Lists, or name the existing list used |
| CDC-11001 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-20 | 8 | Add list LOV-OVERRIDE-REASON to Reference Data v5 Lists, or name the existing list used |

### RWB-P6-E2018-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11048 | RWB-P6-E2018-APP | DOR-RWB-P6-E2018-APP-14 | find it | Record the signed epic design sign-off in the epic design record; no signed epic design is in the source documents. |
| CDC-11096 | RWB-P6-E2018-OPS | GAP-1196 |  | Add DP-03 and H RWB-PLT-E1027-CON to the slice pattern set, or confirm the platform release train delivers the decision-record library. Story keeps one record per request and result. |

### OTHER:Contract fake library (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11050 | RWB-P6-E2018-APP | DOR-RWB-P6-E2018-APP-22 | 12.8 | Publish a version of the section 12.8 fakes and record that version as published. |
| CDC-11078 | RWB-P6-E2018-OPS | DOR-RWB-P6-E2018-OPS-22 | header | Record the published fake library version for the rwb-document and rwb-treatment fakes |

### RWB-P5-E1024-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11057 | RWB-P6-E2018-APP | GAP-2356 |  | Settle container, WORM tier, maximum object size, transfer path of the signed PDF and write-once refusal reporting; carry as configuration rows of rwb.document.esign. |
| CDC-11085 | RWB-P6-E2018-OPS | GAP-2356 | none | Settle the container, WORM tier, maximum object size and transfer path of the signed PDF, and record them as rwb.document.esign configuration rows. |

### OTHER:FSD P10 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10913 | RWB-P6-E1063-APP | GAP-1516 | 3, 8 | Retire the Power BI and model gateway integration points at A2.6.2 and the data lake row-count check in AC-EXC-P10-006-01. Replace the check with one on the measure hand-over. |

### OTHER:RWB-E1-060 extraction evaluation story (rwb-agent) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10914 | RWB-P6-E1063-APP | GAP-0644 | find it | Apply the proposed fix there: login the rwb-agent login (DP-02); LOV-DOC-TYPE read through the rwb-case reference-data contract; three legacy admin operations on /api/recovery/agent/v1; report and configuration operations left with RWB-P10-E1058-APP; gateway-bff route; scores read only through the evaluation read. |

### OTHER:RWB-E2-031 agent monitoring dashboard v2 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10915 | RWB-P6-E1063-APP | GAP-0629 | find it | Apply the proposed fix there: drift step in the v1 Schedule workflow; segment read from the run row; override figures via rwb-decision with agent-version filter; notice path by owner; policy values in watch_measures; migration V10_007; range limits as configuration; login the rwb-agent login (DP-02); route under RWB-PLT-N001-CON; right of API-P10-009 decided. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10917 | RWB-P6-E1063-APP | GAP-2332 |  | Publish the two dashboard-read access-event codes, the entry field list, the page bounds and the read index name, and register the Flyway step and parameter codes, as proposed. |

### OTHER:ASM-B-ITG-W1-08-E1063-1 to -6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10918 | RWB-P6-E1063-APP | GAP-0372 |  | Name the P9 reporting read model fed from agent events and the P10 daily step, read via GET /reports/measures, and JOB-15 via P1 admin operations, as the assumption set records. |

### OTHER:P6 rwb-comms contract and ASM-B-P6-05-E1063-4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10920 | RWB-P6-E1063-APP | GAP-1209 |  | Publish the template code, channel, notice type, notice field names, role holders, guard right and retry window in the P6 contract and parameter rows, as proposed. |

### OTHER:P9 rwb-reporting read model and ASM-B-P6-05-E1063-5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10921 | RWB-P6-E1063-APP | GAP-1210 |  | Confirm the lake copy, count check and Power BI page are dropped from this slice, and record the dashboard as P9 and P10 work as ASM-B-P6-05-E1063-5 sets out. |

### OTHER:FSD P4 v3; RWB-P10-E1063-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10925 | RWB-P6-E1063-APP | GAP-2333 |  | Keep both Reporting rights, replace the lake copy access rule with the served-read access entry, correct REQ-ACA-006 and NFR-042, and add the listed contracts to H and C. |

### OTHER:rwb-agent deployment story (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10926 | RWB-P6-E1063-APP | GAP-0618 | n/a | Expose topology values as chart values; register the schedule, topic, grants, gateway route and four alerts as GAP-0618 proposes; invent no value. |

### RWB-P6-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10927 | RWB-P6-E1063-APP | GAP-1212 | header | Add to H list RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON; add to C list RWB-P3-E1042-CON, RWB-P3-E1043-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10928 | RWB-P6-E1073-APP | CG-ALL-6456 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} through the RWB-P7-E1073-CON contract story; the story keeps its current row. |

### OTHER:Document holding screen SCR-39 (named by detcheck as P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10936 | RWB-P6-E1073-APP | DOR-RWB-P6-E1073-APP-10 | not in chunk | Add empty, loading, error and no-access states for SCR-39. |

### OTHER:TSD P7; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10937 | RWB-P6-E1073-APP | GAP-1615 | find it | Re-issue TSD P7 with entries for rule_package, rule_package_version, rule_row and rule_test_case and the rule operations; remove those tables and operations from TSD P3 and TSD P4; set x-module P7 on the nine rule paths |

### RWB-P3-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10938 | RWB-P6-E1073-APP | GAP-1330 | find it | State in section 12.1 whether it publishes the case reads this consumer needs, or move the dependency to RWB-P3-E1023-CON |

### OTHER:rwb-decision API document and wave-1 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10941 | RWB-P6-E1073-APP | GAP-1217 | 12 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} with the DRL, SHA-256, version state and valid-from date; 404 for an unknown label; 409 for a version not loadable; 2 s budget, one hop. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10942 | RWB-P6-E1073-APP | GAP-1327 | 12 | Publish registry physical columns, model answer shape, dry-run counts, workbook container and object name, version-list panel identifier, service login and the two parameter codes. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:EV-09; OTHER:EV-30) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10943 | RWB-P6-E1073-APP | GAP-2459 | 12 | Name rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1, keyed by package code, carrying package code, version label, in-force time and SHA-256; map it to EV-08, EV-09 and EV-30. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-P7-E1073-CON; OTHER:rwb_integration DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10945 | RWB-P6-E1073-APP | GAP-0672 | 3 | Record the eight DP H rows as wave-0 platform prerequisites; publish the model fetch with path, request and response fields in RWB-P7-E1073-CON; fix the local copy table in the rwb_integration DB story; name the rwb-comms login before the baseline. |

### OTHER:Template and Rules v1 section R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10946 | RWB-P6-E1073-APP | GAP-1328 | 3 | State that a platform H row and a self-referential C row added by a pattern are held by the platform and contract stories and are not repeated on the APP line. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10948 | RWB-P6-E1073-APP | GAP-1620 | 3 | Record that the registry accepts an XLS decision table and a DMN 1.6 model as two package formats on one runtime, that a version names its format, and that conversion is a version change with its own test evidence. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10949 | RWB-P6-E1073-APP | GAP-0118 | find it | Confirm the amended text of T1 and T2: the workflow runs on the task queue of the owning service, and each scheduled job becomes a Temporal Schedule or an event-started workflow in the owning service, with JOB-05 kept behind the TimerScheduler port until Epic 3. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10950 | RWB-P6-E1073-APP | GAP-0205 |  | Add rule_package and rule_package_version as entities of P7 in the next LDM version; rename nothing, and record 'Rule' as rule_row in the ownership basis. |

### RWB-P3-E1073-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10951 | RWB-P6-E1073-APP | GAP-0702 |  | Record the readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed values per environment in the deployment files; confirm them at SIT with the platform and security owners; keep them out of code and chart constants. |

### OTHER:Temporal and Drools design (slide 15) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10953 | RWB-P6-E1073-APP | GAP-1331 |  | State that REFUSED is a state of a stored version that failed promotion checks, and that a load refused at a check leaves no version row and is proved by its decision log entry. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10955 | RWB-P6-E1073-APP | GAP-2461 | Not in chunk | Record the move of the five rule-package and rule-version operations, their authority checks and the package list from recovery.accessadmin.rulepackages (P4 endpoint label) to rwb-decision (P7). The rights stay rows of the rwb-access role model. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10956 | RWB-P6-E1073-APP | GAP-1215 | 13 | Correct the DP-04 row or the plan line so both agree. Treat RWB-PLT-E1072-CON as a wave-0 platform prerequisite and RWB-P7-E1073-CON as the contract the model fetch fake stands in for. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10959 | RWB-P6-E2013-APP | CG-ALL-6471 | 12.2 | Publish POST /api/recovery/access/v1/authorise through RWB-P4-E1037-CON, or the story consumes a published operation. |

### OTHER:Story register (contract story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10961 | RWB-P6-E2013-APP | DOR-RWB-P6-E2013-APP-21 | Metadata | Create RWB-P6-E2013-CON or confirm RWB-P7-E2013-CON as the published contract story the build depends on. |

### OTHER:rwb-access API yaml (RWB-P4 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10964 | RWB-P6-E2013-APP | DOR-RWB-P6-E2013-APP-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10970 | RWB-P6-E2013-APP | GAP-3177 |  | Register the five-minute next-action Schedule in rwb-case and delete EV-18 (TimerDue) from the Epic 2 contract tables. |

### RWB-P4-E1038-APP; RWB-P4-E2013-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10971 | RWB-P6-E2013-APP | GAP-0842 |  | Serve GET /doa-limits once from rwb-access; RWB-P4-AD016-APP owns the answer and RWB-P4-E2013-APP the routing, with no second copy of the path. |

### RWB-P4-E1037-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10973 | RWB-P6-E2013-APP | GAP-1252 |  | Add GET /api/recovery/access/v1/doa-limits with P4 as owner, its query and its answer fields. |

### RWB-P4-E1037-CON; RWB-P7-E2013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10974 | RWB-P6-E2013-APP | GAP-1256 |  | Fix one refresh rule: a local read-through cache warmed at start, refreshed on DoaLimitChanged, with an alert when older than the version in force. |

### OTHER:Approval-routing harness pack (owner: Integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10975 | RWB-P6-E2013-APP | GAP-0397 |  | Hold the composite route, merge order, environment, seeding, evidence format, retention and gate as data; agree them at the wave 2 entry check. |

### RWB-P6-E2013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10980 | RWB-P6-E2013-APP | GAP-1222 |  | Confirm or rename GET /notices/{noticeId} and POST /cases/{caseId}/messages on /api/recovery/comms/v1 with Notice and MessageRequest fields carrying approval reference, escalation level, recipient and send time. |

### RWB-P7-E2013-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10983 | RWB-P6-E2013-APP | GAP-0732 |  | Record at contract review the approval event fields the case consumes, the task fields written (approval and preparer references), escalation representation, status mapping, composite route fields and the rwb-case login name. |

### OTHER:rwb-comms template catalogue (TSD P6 v2 template) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10984 | RWB-P6-E2013-APP | GAP-1220 |  | Load MSG-P7-011 with placeholders {decision} and {caseNo}, a channel from LOV-CHANNEL and an Approved version; retry from RWB-PLT-TE006-CON outbox policy; code and channel agreed at wave 2 design review. |

### OTHER:TSD P7 v2 (next version); OTHER:T8 traceability table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10987 | RWB-P6-E2013-APP | GAP-1263 | 18 | Map REQ-APD-002 and REQ-APD-006 to FEAT-APD-01 with RWB-E2-013 for routing, and to FEAT-APD-08 with RWB-E2-014 for the screen. |

### OTHER:Edge and gateway design (gateway-bff composite route; OTHER:DP-19; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10988 | RWB-P6-E2013-APP | GAP-1621 | 15 | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations, and record those four screen contracts there. |

### OTHER:TSD P7 (next version); 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10989 | RWB-P6-E2013-APP | GAP-1254 | 13 | State INT-19, INT-20, lake partition, manifest and watermark as retired; rwb-reporting reads from rwb.decision-record.v1; keep EV-08 unchanged; drop lake elements from contract and deployment. |

### RWB-P6-E2014-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10994 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-21 | header | Create contract story RWB-P6-E2014-CON publishing the four notice operations; RWB-P6-E1052-CON added as contract dependency |

### OTHER:rwb-case contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10995 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-22 | 12.8 | Name the rwb-case contract fake in 12.8 and record its published library version |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11002 | RWB-P6-E2014-APP | DOR-RWB-P6-E2014-APP-7 | 11 | Confirm party_id as a notice field or its field ID, and add decision_log_entry_id uuid to notice in rwb_comms; the story already carries both |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:17 and 42; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11004 | RWB-P6-E2014-APP | GAP-2093 | find it | Record approval as P7 ApprovalWorkflow child of NoticeDispatchWorkflow with the notice as source; S4 POST /notices/{noticeId}/approve is the litigation decision point; notice waits in Approved |

### RWB-P7-E2014-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11005 | RWB-P6-E2014-APP | GAP-2216 | find it | Fix the case-facts projection with inputAsOf on API-P3-002, a refusal and a return event on rwb.decision.events.v1, the task code and reference row, and the dated contact read |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11006 | RWB-P6-E2014-APP | GAP-0932 | find it | Publish the authorise, me-permissions and masking-policies shapes and state whether the routed role or the holder is a request field |

### RWB-P6-E1052-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11007 | RWB-P6-E2014-APP | GAP-1264 | find it | Publish approve, regenerate and hold on the rwb-comms contract with their states and error codes, and correct the Ownership Map rows |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11008 | RWB-P6-E2014-APP | GAP-0398 | find it | GAP-0398: record owner as Integration lead; resolution route is agreement with the platform edge owner and QA at the wave 2 entry check. Harness values stay open. |

### OTHER:rwb-comms API file; RWB-P7-E2014-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11009 | RWB-P6-E2014-APP | GAP-2384 | find it | Add POST notices/{noticeId}/approve, regenerate and hold with decisionLogEntryId, reasonCode and templateCode in the requests, and the 401, 403, 404, 409, 422 and 503 set |

### OTHER:rwb-comms API file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11011 | RWB-P6-E2014-APP | GAP-2386 | not in chunk | State that regeneration keeps the same notice row: document_id and template_id move to the chosen Approved variant, the version increments, and the superseded document stays in rwb-document with its template version. |

### OTHER:TSD P6 v2 T-A.1 and T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11013 | RWB-P6-E2014-APP | GAP-2388 | not in chunk | Add the three notice decision operations with Litigation right A, scope applied, enforced at gateway-bff via rwb-access; rwb-decision calls them with service identity, approver user ID and decision entry reference. |

### OTHER:FSD P6 v3 A2.1.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11014 | RWB-P6-E2014-APP | GAP-2390 | not in chunk | State that the notice move writes one local decision record through the library (D7.1, rule, IDs, states, approver) that references the rwb-decision approval entry; the central ledger holds both. |

### RWB-S4-E5001-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11015 | RWB-P6-E2014-APP | GAP-2743 | not in chunk | Record the two consumed rows as C dependencies, declare P6 notice and template ownership, name P6 operations, add REQ-S4-001 to the trace, and decide the D7.1 gate in the EP05 PRD. |

### OTHER:TSD P7 v2 traceability table T8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11021 | RWB-P6-E2014-APP | GAP-1263 | n/a | Correct REQ-APD-002 and REQ-APD-006 to FEAT-APD-08 with RWB-E2-014 for the screen and FEAT-APD-01 with RWB-E2-013 for routing. |

### OTHER:Edge and gateway design (gateway-bff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11022 | RWB-P6-E2014-APP | GAP-1621 | n/a | Record which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service and the state each owns. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:41; OTHER:42; OTHER:43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11023 | RWB-P6-E2014-APP | GAP-1262 | n/a | Publish decided outcome on rwb.decision-record.v1 via DP-03 and retire ApprovalDecided from the slide 14 line or add it to the catalogue. |

### OTHER:Recovery Workbench FSD P7 and TSD P7 observability text (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11025 | RWB-P6-E2014-APP | GAP-1271 |  | Add the alert set: 5xx in five minutes, route p95 above registered budget, failed record write, empty D7.1 queue for 24 hours; review thresholds with platform observability owner. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11027 | RWB-P6-E2014-APP | GAP-2389 |  | Add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to the C list; keep H empty. |

### RWB-P6-E2017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11029 | RWB-P6-E2017-APP | DOR-RWB-P6-E2017-APP-21 | header | Create and publish contract story RWB-P6-E2017-CON for the rwb-comms API; the story already lists it under Contract dependencies. |

### OTHER:fake library publication (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11030 | RWB-P6-E2017-APP | DOR-RWB-P6-E2017-APP-22 | 12.8 | Fake named for rwb-document; library version placeholder stays until the fake library publishes it. |

### OTHER:Screen Specifications v1, section SCR-30; RWB-P6-E2017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11035 | RWB-P6-E2017-APP | DOR-RWB-P6-E2017-APP-10 Screens and states: Partial | 4, 15 | Row 11 rewritten: empty, loading (SCR-14), error and no-access states marked Not specified; SCR-30 loading follows Screen Specifications v1. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11036 | RWB-P6-E2017-APP | DOR-RWB-P6-E2017-APP-12 Test cases: Partial | 12.7, 16, 18 | Five new cases TC-P6-E2017-APP-03 to -05 added; section 16 now has 20 cases (15 legacy plus 5 new). |

### OTHER:Message catalog (standard MSG IDs) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11037 | RWB-P6-E2017-APP | DOR-RWB-P6-E2017-APP-9 | 14 | Confirm the meaning of MSG-P4-003, MSG-P5-010 and MSG-P6-003 against the standard and align the story rows to it. |

### OTHER:Technical Solution Design P4 T6.1 RBAC matrix; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11038 | RWB-P6-E2017-APP | GAP-0942 | 16 | Add a Documents column to T6.1: CRU for RW-RESTRUCT and RW-CASEOWN, R for RW-TEAMMGR, CRUA for RW-LEGAL. Confirm with matrix owner and publish before the pack is in force. |

### OTHER:Service contract of rwb-comms; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11039 | RWB-P6-E2017-APP | GAP-1713 | header | Record once in the service contract the mapping of each FEAT prerequisite to its owning contract: approval P7, case P3, documents P5, communications P6, valuation S1. |

### OTHER:Functional Specification Document P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11040 | RWB-P6-E2017-APP | GAP-1580 | 18 | Add a generation section for REQ-DCM-012 in the next version, carrying FR-P5-026 and AC-P5-019 with the confirmed operations. |

### OTHER:TSD P6 v2; RWB-P6-E1046-CON; RWB-P3-E1043-CON; OTHER:message catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11041 | RWB-P6-E2017-APP | GAP-2392 | 12.7, 14, 16 | Add treatment-type and product-group filters to API-P6-003; add an application/json form of API-P6-005; add the locked attribute to merge_field; publish set rows as rwb-case reference data; copy five message texts when issued. |

### OTHER:TSD P4 appendix T-A and T6.2; RWB-P4-E1037-CON; OTHER:platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11042 | RWB-P6-E2017-APP | GAP-0941 | 16 | Publish the authorise path with request and answer schema in TSD P4 T-A, stub it in the contract fake, fix the rwb-access login, and state the service identity scope rule in T6.2. |

### RWB-P3-E1043-CON; RWB-P5-E2017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11049 | RWB-P6-E2018-APP | DOR-RWB-P6-E2018-APP-21 | 12.1 | Reach Done. Section 12.1 already states that no RWB-P6-E2018-CON story exists for this legacy key. |

### OTHER:RWB-SVC-P6 service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11054 | RWB-P6-E2018-APP | GAP-1713 |  | Record once the mapping of each FEAT prerequisite to its owning service contract (approval to P7, case to P3, documents to P5, communications to P6, valuation to S1); carry duplicate FEAT-CHO-08 as written. |

### OTHER:rwb-treatment contract story (not yet in plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11056 | RWB-P6-E2018-APP | GAP-1183 |  | Add an rwb-treatment contract story to the plan; S2 publishes the signature-record operation and its field names in the wave 2 contract on the PATCH of a treatment at /api/recovery/treatment/v1. |

### OTHER:Integration and test environment plan for wave 2 (EasyApp test tenant, harness pack, seeding, evidence format) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11059 | RWB-P6-E2018-APP | GAP-0402 | 16 | Agree the EasyApp test tenant and route via INT-34, the signed-PDF fixture, SIT harness hosts, seeding, evidence format and pass/fail gate with QA and the ACE team. |

### OTHER:Integration inventory (TSD P6 v2 T5.1) and ACE common module interface specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11060 | RWB-P6-E2018-APP | GAP-1187 | Header; 12.8 | Add INT-34 with request and result shape, endpoint and certificate issuer; carry endpoint and certificate as secret references (NFR-052). |

### OTHER:FSD P5 Document hub v3 (A1.1 and A2 feature set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11062 | RWB-P6-E2018-APP | GAP-1589 | 12.1 | Add the signature requirement text as OQ-P5-13 and record the signature request as a document event and metadata row. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11063 | RWB-P6-E2018-APP | GAP-1596 | 12.1 | Confirm with P5 the read path for request status before wave 2; this service creates the request through P5's contract and calls the treatment service. |

### OTHER:TSD P6 Communications v2 T3.1; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11065 | RWB-P6-E2018-APP | GAP-2353 | 11 | Keep signature_request in rwb_document, remove it from the rwb-comms model, and add its columns, constraints and indexes to TSD P5 T3.1 and rwb_document.sql. |

### OTHER:TSD S2 Treatment v2 (T3.1; OTHER:T-A.1) and FSD S2 A2.7 to A2.9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11066 | RWB-P6-E2018-APP | GAP-2699 | 12.2 | Add five nullable signature columns with two indexes on the service's Flyway sequence, add the record to the update operation, name the two events, and let the offer-validity timer close the window. |

### RWB-P5-E2018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11069 | RWB-P6-E2018-APP | GAP-3182 | 3, 12 | Own the signature_request DDL in the P5 story set and publish the request and result operations on the rwb-document contract |

### OTHER:RWB-PLT plan (DP-03 in pattern set and build list of the e-signature key) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11070 | RWB-P6-E2018-APP | GAP-1196 | 3 | Precondition cites RWB-PLT-E1027-CON for decision records until the plan adds DP-03 and the H row to the slice. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11071 | RWB-P6-E2018-APP | GAP-2354 | 3 | Record the six platform CONs as wave-0 prerequisites and add RWB-P3-E1043-CON to the contract rows of DP-07 stories; Work Package rows stay as fixed |

### RWB-S2-E2018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11073 | RWB-P6-E2018-APP | GAP-1704 | 3 | Hold the document reference on the treatment only, keep no document content in schema rwb_treatment, and request generation, review and signature through the P5 and P6 contracts |

### OTHER:rwb-document generation-screens API baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11074 | RWB-P6-E2018-APP | GAP-1017 | 12 | Declare the seven operations on /api/recovery/document/v1, map regenerate to API-P5-017, consume API-P6-009 for the signature send, and fix field names and the error envelope as the Detail states |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11075 | RWB-P6-E2018-APP | GAP-2357 | 14 | Confirm Documents C, R and U as the operation-level rights of the five signature-request operations; add a rwb-document message for a closed signature request at the next message standard version. Story keeps MSG-P3-005 unchanged meanwhile. |

### OTHER:Recovery Workbench story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11077 | RWB-P6-E2018-OPS | DOR-RWB-P6-E2018-OPS-21 | header | Contract dependencies row now states that no contract story is recorded for the signature-request operations. |

### OTHER:Contract owner API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11079 | RWB-P6-E2018-OPS | DOR-RWB-P6-E2018-OPS-23 | header | Fix the contract version this story builds against, not only the /v1 path |

### OTHER:Recovery Workbench screen specification (SCR-09; OTHER:SCR-14; OTHER:SCR-30) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11081 | RWB-P6-E2018-OPS | DOR-RWB-P6-E2018-OPS-10 | none | Add empty, loading, error and no-access states for SCR-09, SCR-14 and SCR-30 |

### OTHER:rwb-comms service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11082 | RWB-P6-E2018-OPS | GAP-1713 | none | Map each prerequisite FEAT code to its owning service contract (approval P7, case P3, documents P5, communications P6, valuation S1); carry duplicate FEAT-CHO-08 as written. |

### OTHER:delivery plan (rwb-treatment contract story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11084 | RWB-P6-E2018-OPS | GAP-1183 | 1 | Add a rwb-treatment contract story on /api/recovery/treatment/v1 with PATCH for the signature record; S2 publishes its operation and field names. |

### OTHER:Integration inventory (add INT-34) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11087 | RWB-P6-E2018-OPS | GAP-1187 | 11 | Add INT-34 with its request and result shape, endpoint and certificate issuer, as published by the ACE common module owner. |

### OTHER:PRD and FSD P5 Document hub v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11089 | RWB-P6-E2018-OPS | GAP-1589 |  | Record the signature request as a document event and a metadata row on the document, keep the signing journey with P6 and S2, and add OQ-P5-13 carrying the missing requirement text. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11092 | RWB-P6-E2018-OPS | GAP-2353 |  | Keep signature_request in rwb_document; add the table with its columns, constraints and indexes to TSD P5 T3.1 and rwb_document.sql; remove it from TSD P6 T3.1. |

### OTHER:TSD S2 v2 T3.1; OTHER:T3.2 and T-A.1; OTHER:FSD S2 A2.7 to A2.9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11093 | RWB-P6-E2018-OPS | GAP-2699 |  | Add five nullable signature columns and two indexes on the rwb-treatment Flyway sequence; carry the record on the update operation; name the two outcome events; read method and status lists via reference-data contract; closure by the offer-validity timer. |

### OTHER:P5 story set for rwb-document (signature_request DDL migration) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11095 | RWB-P6-E2018-OPS | GAP-3182 |  | Move the signature_request DDL out of this story's build notes (V2_018__signature_request.sql) into the P5 story set; publish request and result operations on the rwb-document contract. |

### OTHER:FSD S2 (A2.18.2; OTHER:A2.15.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11098 | RWB-P6-E2018-OPS | GAP-1704 | find it | Name rwb-document as the document hub; request generation, review and signature through the P5 and P6 contracts; hold the document reference on the treatment; keep no document content in schema rwb_treatment. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0118 | The amendment of D-RCV-36 T1 and T2 has no wording in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0205 | The entity called Rule is rule_row, and the model holds neither rule_package nor rule_package_version | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0372 | Data lake removed: agent daily read model, reporting read and job rerun owner are not named for the target | P10 agent owner, P9 reporting owner, P1 source data owner, P6 comms owner and P2 integration owner | Resolved (directive) |
| GAP-0383 | The rule package of rwb-comms and of rwb-integration, the rule-model fetch path and its owner, and the message family of the refusal are not stated in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0397 | Approval-routing harness environment, composite queue route and evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-0398 | Integration harness values for the D7.1 decision-screen journey are not specified | Integration lead | Resolved (directive) |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0402 | The e-signature harness pack and the EasyApp test route are not specified | Integration lead | Resolved (directive) |
| GAP-0616 | Agent monitoring dashboard in rwb-agent: the data lake of the legacy story is removed, and the schedule name, the service login, the route path, the notification operation and the home of the daily aggregate are not specified | Solution architect | Resolved (directive) |
| GAP-0617 | Agent monitoring contract in rwb-agent: the page size and cursor, the member types of the aggregate element, the held-date status members, the Schedule name, the route path and the notification operation are not specified | Solution architect | Resolved (directive) |
| GAP-0618 | Agent monitoring deployment in rwb-agent: the topology, host, SKU, budget, route path, login, feed retention and alert thresholds are not specified | Platform administrator | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0644 | Extraction evaluation in rwb-agent: service login, document-type owner, admin operation set, route path and score read path | Solution architect | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0699 | The rule package registry and the workbook object are declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0700 | The five authoring operations and the two rule reads have no Ownership Map row and no field-level shape | P7 rwb-decision owner with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0701 | The KieBase cache sizing, the JVM heap and the storage of a local model artefact are not specified | SCB IT infrastructure with the rwb-case owner team | Resolved (directive) |
| GAP-0702 | No source gives the readiness gate, the probe timings, the ports, the certificate subject or the image-scan window | SCB IT infrastructure with the platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0928 | GET /doa-limits is named in Architecture v5 and API v3 but absent from API Specification v4 | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0929 | The DoA lookup and authority-decision request and response shape is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0930 | The scope of the rwb-decision service identity inside rwb-access is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0932 | The request and response shape of the authorise operation is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0941 | rwb-access document set: the authorise request and answer shape for the document screens, and the scope a service identity is asked for, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1017 | The generation-screens baseline fixes six operations and four shapes that no source names, two conflicting legacy paths, the field names of the request and answer objects, and a status mapping the legacy section 12 states only in prose | Tech lead of rwb-document, with the solution architect and the rwb-comms owner | Resolved (directive) |
| GAP-1181 | signature_request is defined in TSD P6 but is owned by P5 rwb-document | Solution architect | Resolved (directive) |
| GAP-1182 | The published P5 document names no operation to create, read by external reference or update a signature request | Solution architect | Resolved (directive) |
| GAP-1183 | No rwb-treatment contract story is in the plan, although the story reads the treatment and writes its signature record | Solution architect | Resolved (directive) |
| GAP-1184 | The plan holds no RWB-P6-E2018-CON, so the three signature-request operations have no published contract story | Solution architect | Resolved (directive) |
| GAP-1185 | The Architecture v5 event catalogue carries no comms signature event | Solution architect | Resolved (directive) |
| GAP-1186 | The signed PDF object and the byte transfer into the P5 write-once store are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1187 | The ACE common module e-signature path (INT-34) is not in the integration inventory and its shape, endpoint and certificate are unknown | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1188 | P3's cancel on offer expiry has no operation in the target catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1196 | DP-03 and its decision-record library are missing from the pattern set and the build list of the e-signature key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1209 | Template code, channel, notice type, field names, recipient role holders, guard right and retry window are not named for the target | P6 comms owner, P10 agent owner and platform notification path owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1210 | The legacy data lake copy and the agent monitoring dashboard have no target, and P6 has no replacement for the dashboard | P6 comms owner, P9 reporting owner and architecture owner | Resolved (directive) |
| GAP-1211 | The agent alert event name, the alert notification operation name and the non-case binding of the cost alert are not named for the target | P10 agent owner and P6 comms owner | Resolved (directive) |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1215 | RWB-P6-E1073-APP: the DP-04 row of the pattern table names H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON while the plan gives no H and C RWB-P3-E1073-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1216 | RWB-P6-E1073-APP: no source names the rule package rwb-comms is assigned, its version labels or its target queues | Solution architect | Resolved (directive) |
| GAP-1217 | RWB-P6-E1073-APP: the model fetch operation, its path segments, its request fields and its response fields are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1219 | RWB-P6-E1073-APP: Arch v5 slide 43 lists four consumers of RulePackageInForce while slide 20 says every service refreshes its cache on it, and the ITG story makes rwb-comms an evaluator | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1220 | The template code, channel, notice kind, state vocabulary, retry limit, template owner and MSG-GEN-006 text of the escalation notice are not specified in any source | Solution architect | Resolved (directive) |
| GAP-1221 | The event catalogue lists gateway-bff as the only consumer of ApprovalRequested and carries no ApprovalEscalated event, yet this story also consumes the event for the escalation notice | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1222 | No source names the notice and message operations or the notice fields that carry an approval reference, an escalation level, a recipient and a sent time | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1251 | The delegation of authority table is P4 rwb-access's while the routing rules and the approval resource are P7 rwb-decision | Solution architect | Resolved (directive) |
| GAP-1252 | The delegation limits operation has no row in the Ownership Map API catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1254 | The data lake copy of the decision record is removed under DP-17 while the legacy log path streams to it | Solution architect | Resolved (directive) |
| GAP-1255 | The request and answer field lists of the five approval operations and the case-status operation are not enumerated in any source | Tech lead of rwb-decision with the Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1256 | The delegation snapshot and its cache refresh have no named operation, store or interval | Solution architect | Resolved (directive) |
| GAP-1257 | ApprovalDecided is named on the service contract slide but has no event catalogue row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1278 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Solution architect | Resolved (directive) |
| GAP-1327 | RWB-P7-E1073-APP: the model answer, the dry-run report, the refusal of the model read, the workbook object, the version-list panel, the service login, the parameter codes and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1329 | RWB-P7-E1073-APP: the same rule registry is named as /admin/rule-versions by API Specification v4 and the integration story and as /admin/rule-package* by the legacy story and the Ownership Map, and a third read /rule-catalog is consumed but unowned | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1330 | RWB-P7-E1073-APP: the case read that feeds the dry run is attributed to RWB-P3-E1073-CON by the plan and to RWB-P3-E1023-CON by the P3 contract story, which serves no operation | Solution architect with the rwb-case contract owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1331 | RWB-P7-E1073-APP: REFUSED is one of the six version states while a load refused at a check writes no rule_package_version row, so no stored version ever reaches it | Solution architect with the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1516 | FSD P10 v3 publishes the agent dashboard through a data lake write and Power BI, both removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1517 | The daily aggregate table the FSD acceptance criteria name is not in the Logical Data Model v8 entity list | Solution architect | Resolved (directive) |
| GAP-1519 | JOB-15 is the reporting extract of rwb-reporting in the Ownership Map, but the FSD uses its completion as the trigger of the P10 dashboard | Platform administrator | Resolved (directive) |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1589 | Signatures are owned by P5 in Architecture v5 and the Ownership Map but have no requirement, feature or story | Solution architect with P6 and S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1596 | The signature request is defined as a Communications table while Architecture v5 gives signatures to the document hub | Solution architect | Resolved (directive) |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1621 | Four screens are attributed to P7 while the edge ruling composes every screen in gateway-bff | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-2030 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2031 | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2049 | The rule package compile alert names P3 while the registry is P7 and the load happens in every owning service | P7 rwb-decision with the centre of excellence | Resolved (directive) |
| GAP-2093 | The notice approval sits in P6, P7 and S4 at once | Service owners of P6 rwb-comms, P7 rwb-decision and S4 rwb-litigation | Resolved (directive) |
| GAP-2216 | No source fixes the case-facts field list behind the D7.1 approval screen, the names of the two approval outcome events, the naming of the redress task, or the business date of the postal address input | Solution architect | Resolved (directive) |
| GAP-2332 | The access-event codes of a dashboard read, the entry field list, the page bounds, the read index and the Flyway step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2352 | The signature-request operations exist in no P5 source and carry no API ID, because the legacy key is a communications module story while the table is P5's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2353 | signature_request is defined in TSD P6 T3.1 inside the communications module and owned by P5 in the ownership ruling, so the table has no P5 data model | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2355 | No source names a signature event on the rwb-document topic, and the request state is readable only through the operations of the story | Solution architect | Resolved (directive) |
| GAP-2356 | The write-once container, the WORM tier, the size limit and the byte transfer behind the signed-version add are named by no source | SCB IT infrastructure | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2357 | No rwb-document message exists for a closed signature request and no source names the operation-level right of the five request operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2384 | The three notice decision operations of the D7.1 approval have no REST row in the Ownership Map or in appendix T-A | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2385 | The notice table has no column for the decision entry reference that the approve and hold calls carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2386 | No source says whether a change of template variant replaces the notice row or creates a new version of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2387 | The notice answer has no field list, and the template state the approval panel must show is not part of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2388 | The declared right of the three notice decision operations is not in the endpoint inventory or the RBAC matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2390 | No source says whether a notice move writes its own decision record or only references the approval entry of rwb-decision | Solution architect | Resolved (directive) |
| GAP-2391 | The hold reason vocabulary has no list of values, and the owner namespace of the feature switch is not settled for the comms half | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2396 | Architecture v5 slide 13 gives P6 to P7 a Temporal cell and no event cell, while RWB-P6-E1073-APP consumes RulePackageInForce from rwb.decision.events.v1 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2457 | The physical columns of rule_package, rule_package_version, rule_row and rule_test_case are not in any source | TechX and the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2458 | No provided operation of the case service returns the open case facts a dry run needs | P3 and P7 contract owners | Resolved (directive) |
| GAP-2459 | Which owned event announces a rule package version in force is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2460 | The value of rules.testcases.min is assumed and no parameter catalogue holds it | P3 parameter owner and the P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2461 | The legacy endpoints and their controller sit in the access module, while the Ownership Map gives them to P7 | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2697 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Solution architect | Resolved (directive) |
| GAP-2698 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Solution architect | Resolved (directive) |
| GAP-2699 | The treatment-side signature columns, the operation a signature record arrives on, the event names, the two list codes and the closure are not specified for rwb-treatment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2700 | Architecture v5 gives S2 to P5 the Temporal cell and no cell from P6 or P5 into S2, while the legacy seam is one synchronous in-process call and the work package lists DP-11 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2701 | The legacy one module and one transaction for the signature request, the signed version and the treatment field become three owners, and the offer expiry that closed the request is now the treatment's own date | Solution architect | Resolved (directive) |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3157 | The rule tables are described as recovery-schema tables but are owned by rwb-decision | P7 rule owner | Resolved (directive) |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3182 | The signature_request table is created by P6 in the story and owned by P5 in the ownership map | Document hub lead with the communications lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P6-E2017-APP | unknown story key | 24 | RWB-P6-E2017-CON is not a story of the set: \| Contract dependencies \| RWB-P5-E2017-CON, RWB-P6-E2017-CON (contract story not yet issued) \| |
| RWB-P6-E2017-APP | unknown story key | 426 | RWB-P6-E2017-CON is not a story of the set: Generation, review and signature go through the RWB-P5-E2017-CON and RWB-P6-E2017-CON contracts (the latter not yet issued); the treatment h |
