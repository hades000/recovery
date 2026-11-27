# RWB-SVC-S7 rwb-writeoff (Write-off) - review pack, part 2 of 2 (RWB-S7-E6021-APP to RWB-S7-E6028-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 16 |
| Resolved in the stories | 321 |
| Cross-document (pending in another document) | 210 |
| Not applied (value not in the sources) | 22 |
| Open business decisions | 29 |
| Register gaps linked | 35 |
| Unconfirmed assumptions | 0 |
| Lint findings | 5 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S7-E6021-APP | 27 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6021 APP Post an approved write-off v2.md |
| RWB-S7-E6021-CON | 20 | 11 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6021 CON Post an approved write-off - contract v2.md |
| RWB-S7-E6022-APP | 30 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6022 APP Send provision inputs to Finance v2.md |
| RWB-S7-E6022-CON | 12 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6022 CON Send provision inputs to Finance - contract v2.md |
| RWB-S7-E6023-APP | 28 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6023 APP Reconcile the approved and posted populations v2.md |
| RWB-S7-E6023-CON | 18 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6023 CON Reconcile the approved and posted populations - contract v2.md |
| RWB-S7-E6024-APP | 22 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6024 APP Work the write-off exception loop v2.md |
| RWB-S7-E6024-CON | 14 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6024 CON Work the write-off exception loop - contract v2.md |
| RWB-S7-E6025-APP | 24 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6025 APP Close the case after the retention period v2.md |
| RWB-S7-E6025-CON | 17 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6025 CON Close the case after the retention period - contract v2.md |
| RWB-S7-E6026-APP | 23 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6026 APP Change the eligibility or tax criteria v2.md |
| RWB-S7-E6026-CON | 10 | 9 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6026 CON Change the eligibility or tax criteria - contract v2.md |
| RWB-S7-E6027-APP | 22 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6027 APP Record a customer payment after charge-off v2.md |
| RWB-S7-E6027-CON | 11 | 12 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6027 CON Record a customer payment after charge-off - contract v2.md |
| RWB-S7-E6028-APP | 28 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 APP Sell a post charge-off population v2.md |
| RWB-S7-E6028-CON | 15 | 15 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 CON Sell a post charge-off population - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E6025-ITG, RWB-P3-E6025-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-09218 | GAP-1475 | Register gap | Compliance and PDPA officer | Retention periods and masking rules by record class and role are not set | Hold a retention class and a masking rule per record class and role as versioned reference data, apply the class at creation, and record every disposal as a decision so a period that is not yet set cannot be breached silently. |
| RWB-S7-E6021-APP | R-13262 | CG-ALL-11064 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6021-CON | R-13265 | CG-ALL-11078 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6022-APP | R-13273 | CG-ALL-11090 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6022-CON | R-13277 | CG-ALL-11102 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6023-APP | R-13282 | CG-ALL-11115 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6023-CON | R-13286 | CG-ALL-11129 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6024-APP | R-13294 | CG-ALL-11143 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6024-CON | R-13298 | CG-ALL-11154 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6025-APP | R-13306 | CG-ALL-11168 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6025-CON | R-13311 | CG-ALL-11181 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6026-APP | R-13317 | CG-ALL-11192 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6027-APP | R-13327 | CG-ALL-11214 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6027-CON | R-13330 | CG-ALL-11225 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6028-APP | R-13338 | CG-ALL-11242 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6028-CON | R-13342 | CG-ALL-11256 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E6021-ITG, RWB-S3-E4013-APP, RWB-S3-E4013-CON, RWB-S7-E6021-APP, RWB-S7-E6021-CON | R-22822 | GAP-1619 | Register gap | Business lead with the center of excellence analyst | A committee decision has no field for the members present or their votes, although the requirement and the screen need both | Agree a member and vote structure for the committee path before Epic 4, either as two child tables of approval or as a versioned structure inside terms, and extend the decision-log entry so the committee's outcome and its members are queryable in the population query. |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6018-APP, RWB-S7-E6018-CON, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22834 | GAP-3049 | Register gap | Solution architect, business lead and the rwb-writeoff tech lead | RWB-S7-E6028-APP: no source publishes a sale-selection operation or a sold-population read, placement_type and the sale reference have no column, field ID or list, the entry state PLACEMENT_DECIDED is produced by an unclaimed rule, AC2's R-WO-12 is already built by RWB-S7-E6018-APP, the hand-off to rwb-debtsale has no edge, the debt sale officer holds right R only, and the plan's C row is empty while the step consumes three contracts | Declare the two operations on /api/recovery/writeoff/v1 with placeholder paths and element names confirmed by the solution architect; read placement_type and the sale reference as request inputs with placeholder value sets and no column; start the step at PLACEMENT_DECIDED and record that R-WO-29 is unclaimed in S7; assert R-WO-12 on the branch RWB-S7-E6018-APP builds instead of building it twice; describe the hand-off as the case move plus the published population read and declare no event; declare the selection at right C with the role conflict recorded; state the post-charge-off and sold states as edge placeholders; build against the three consumed rows as class C dependencies; trace to REQ-S7-006 from the FSD row. |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22838 | GAP-1313 | Register gap | Solution architect, P7 rwb-decision, with the S7 rwb-writeoff solution architect and the internal audit lead | One escalation leaves two decision entries, the routing record of rwb-decision and the write-off record of rwb-writeoff, and no source says so plainly | Keep both records and make the pair explicit: the write-off record names the state change and the rule that fired, the routing record names the level, the delegation row and the limit version the pack was routed at, neither repeats the other's facts, and the ledger read returns them in chain order so an auditor sees the pair as one step. State the reading in the ledger documentation of the service before the wave entry check. |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22840 | GAP-3050 | Register gap | Solution architect, business lead, rwb-writeoff tech lead and the rwb-debtsale owner | RWB-S7-E6028-CON: the two operations, their paths, operation IDs and element names, the placement_type and sale-reference placeholders, the consumed operation names, the decision code set, the role right of the sale and the paging of the population read have no published baseline, and the error set carries no message ID per condition | Publish one OpenAPI 3.1 document with the two operations, their placeholders and the error envelope of one message ID per condition; declare the three elements over DF-FIN-010 to DF-FIN-020 with the placement_type and sale-reference placeholders; declare the three consumed rows with placeholders for their operation names; declare the rights C and R and the role conflict as a carried assumption; declare the decision-record element with the chain to the approval record; publish five fakes and the drift, vocabulary and absence tests; declare no event and no Schedule; trace to REQ-S7-006 from the FSD row. |
| RWB-S7-E6013-APP, RWB-S7-E6013-CON, RWB-S7-E6023-APP, RWB-S7-E6023-CON | R-23622 | GAP-1805 | Register gap | Head of Asset Liquidity with Risk | The write-off cap the epic BRD's risk names has no requirement, no rule and no value | Report the population against the cap once the cap exists, and take the cap, its basis and its period as an open question; no value is asserted here and no cap is enforced in this release. |
| RWB-S7-E6024-APP, RWB-S7-E6024-CON | R-23636 | GAP-1470 | Register gap | Head of recovery | The write-off exception loop has no named owner and no time limit | Assign the loop to the write-off team with an escalation to the team manager after the time limit the business sets, and record the unmapped owner as a gap until the role is confirmed. |
| RWB-S7-E6024-APP, RWB-S7-E6024-CON | R-23637 | GAP-1804 | Register gap | Head of recovery | The write-off exception loop has no named owner, no time limit and no field to hold either | Carry one named owner role and one time limit as required product properties, hold the owner as the write-off team until decided under ASM-014, and take the value as an open question so that the exception can be built and cannot be released without it. |
| RWB-S7-E6026-APP, RWB-S7-E6026-CON | R-23639 | GAP-3043 | Register gap | Product Owner with the owner of rwb-decision's rule registry and the rwb-writeoff tech lead | The criteria change has no screen, no operation, no write right in rwb-writeoff and no home for the criteria version | Keep the change where the rule set is governed: rwb-decision authors, tests and approves a version and rwb-writeoff accepts, pins and records it per cut-off, with the version state shown on SCR-27 and no new path in this service; the criteria version stays a package fact with no column. Confirm the screen, the operation, the write right and the home of tax_criteria_version at the wave 4 contract freeze. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-ITG-E6025-ITG, RWB-P3-E6025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28908 | GAP-1808 | Register gap | Compliance and PDPA officer | The case closes after a retention period that is not set, and the retention class behind a closure is not defined | Hold the closure on a retention class and a recorded period, make the period a versioned data row, and take the periods and the class list as an open question under DL26 and Q-012; no period is asserted here. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S7-E6021-CON | R-13266 | CG-ALL-11079 | 7 | Criteria and test data read ACE views directly | The AC3 and AC7 Given lines are in section 7, which is not in the supplied text. Section 12.8 already holds the rwb-source-data fakes; the lines need rewriting in a follow-up pass. |
| RWB-S7-E6021-CON | R-20943 | DOR-RWB-S7-E6021-CON-11 | 7 | Definition of Ready item 11 Guardrails: Partial | The P2 personal-data field list and the line saying none is carried are not in the supplied text. Naming them would invent fields. |
| RWB-S7-E6021-CON | R-27674 | CG-ALL-11080 | 7 | Criteria and tests keep legacy job and decision-log wording | The JOB-nn, decision log or job record line is in section 7, which is not in the supplied text. JOB-16 in 12.5 is a start trigger, not a criterion, so it stays. |
| RWB-S7-E6022-CON | R-20960 | DOR-RWB-S7-E6022-CON-11 | none | Definition of Ready item 11 Guardrails: Partial | detcheck flags P2 fields by rule, not by name. Item, chunk c02 and story header name none. No field can be reclassified without inventing one. |
| RWB-S7-E6024-APP | R-20985 | DOR-RWB-S7-E6024-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 line 301 states no personal data, but the P2 field list is not in the chunk or the story text found; the P2 fields are needed to correct the classing. |
| RWB-S7-E6026-APP | R-21028 | DOR-RWB-S7-E6026-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Section 8 rule rows already carry BR12, BR13 and BR14 in the Rule column, so no BR ID edit was needed. The AC6/TC-E6-026-11 rows for BR1-BR11 are in sections 7 and 16, which are not in this chunk, so they could not be checked or added. |
| RWB-S7-E6026-CON | R-21033 | DOR-RWB-S7-E6026-CON-12 | 16 | Definition of Ready item 12 Test cases: Partial | No boundary test is present in section 16 of the story. TC-S7-E6026-CON-06 covers tables and personal data. Test Cases v8 gap stays under CG-ALL-11201. |
| RWB-S7-E6026-CON | R-21034 | DOR-RWB-S7-E6026-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Listed test scopes do not cover the mapped rules, and the rules have no test (see AC8). Coverage is stated as Not specified. |
| RWB-S7-E6026-CON | R-27708 | CG-ALL-11202 | 7 and 16 | Criteria and tests keep legacy job and decision-log wording | Offending AC7 and its test line sit in sections 7 and 16, which are not in this chunk, so there is no anchor. Section 12.5 has no JOB or decision-log wording. Needs those parts. |
| RWB-S7-E6026-CON | R-33010 | NEWAC-RWB-S7-E6026-CON-AC8 | 7 and 16 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so there is no anchor for new AC8 or its test row. Proposed test stays Not specified in the source documents. Needs those parts. |
| RWB-S7-E6027-APP | R-21037 | DOR-RWB-S7-E6027-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is not in this chunk, so no edit was made. Empty, loading, error and no-access states are not specified in the source documents (DOR-RWB-S7-E6027-APP-10). |
| RWB-S7-E6027-APP | R-21043 | DOR-RWB-S7-E6027-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Section 8 now states BR7 for R-WO-37 and R-WO-49. No BR column was added. Section 16 test rows and section 7 AC6 text are not in this chunk, so the 11 BR coverage gaps stay open. |
| RWB-S7-E6027-CON | R-13331 | CG-ALL-11226 | 12.8 | Criteria and test data read ACE views directly | Offending Given and test-data line is in section 7, which is not in this chunk. No exact old text, so no edit; needs section 7 text. |
| RWB-S7-E6027-CON | R-21051 | DOR-RWB-S7-E6027-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Mapping BR1 to BR14 to criteria and test cases needs section 7 criteria and section 16 test IDs, not in this chunk. No coverage mapping invented. |
| RWB-S7-E6027-CON | R-27716 | CG-ALL-11227 | 12.5 | Criteria and tests keep legacy job and decision-log wording | Legacy JOB-nn, decision log or job record wording is in the AC7 line of section 7, not in this chunk. No exact old text, so no edit. |
| RWB-S7-E6027-CON | R-33016 | NEWAC-RWB-S7-E6027-CON-AC8 | 7 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC8 must be inserted after a section 7 line, which is not in this chunk, so no anchor. Proposed test is Not specified in the source documents (NEWAC-RWB-S7-E6027-CON-AC8). |
| RWB-S7-E6028-APP | R-21054 | DOR-RWB-S7-E6028-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | The SCR-27 screen-state text is not in this chunk, so there is no exact anchor to copy old text from. Needs a chunk with that section. |
| RWB-S7-E6028-APP | R-21055 | DOR-RWB-S7-E6028-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Detcheck names no P2 field and no source classes fields as personal data. Section 11 is not in this chunk, so there is no anchor. Needs a chunk with section 11 and a source. |
| RWB-S7-E6028-CON | R-21065 | DOR-RWB-S7-E6028-CON-10 | 9 | Definition of Ready item 10 Screens and states: Partial | SCR-27 state text is in section 9, which is not in this chunk, so no exact old text can be anchored. Add empty, loading, error and no-access states with the section 9 pass. |
| RWB-S7-E6028-CON | R-21066 | DOR-RWB-S7-E6028-CON-11 | Not in chunk | Definition of Ready item 11 Guardrails: Partial | Not specified in the source documents (DOR-RWB-S7-E6028-CON-11). The fields to classify are not named in the item or this chunk. |
| RWB-S7-E6028-CON | R-21069 | DOR-RWB-S7-E6028-CON-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Criteria for BR1 to BR14 go in section 7 and their test rows in section 16. Neither section's text is in this chunk, so no anchored edit can be made. |
| RWB-S7-E6028-CON | R-27723 | CG-ALL-11257 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | The flagged AC7 line and its test row are not in this chunk. JOB-16 in 12.5 is a catalog trigger ID and stays as copied. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (32)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19133 | RWB-S7-E6021-APP | CG-ALL-11053 | 12.2 | Declare REST base /api/recovery/case/v1 for P3 rwb-case, taken from the Document Index service table. |
| CDC-19134 | RWB-S7-E6021-APP | CG-ALL-11054 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data, taken from the Document Index service table. |
| CDC-19135 | RWB-S7-E6021-APP | CG-ALL-11055 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data, taken from the Document Index service table. |
| CDC-19136 | RWB-S7-E6021-APP | CG-ALL-11056 | 12.2 | Declare REST base /api/recovery/decision/v1 for P7 rwb-decision, taken from the Document Index service table. |
| CDC-19149 | RWB-S7-E6021-CON | CG-ALL-11068 | 12.2 | Declare REST base /api/recovery/case/v1 for the case provider P3 rwb-case |
| CDC-19150 | RWB-S7-E6021-CON | CG-ALL-11069 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data |
| CDC-19151 | RWB-S7-E6021-CON | CG-ALL-11070 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data |
| CDC-19152 | RWB-S7-E6021-CON | CG-ALL-11071 | 12.2 | Declare REST base /api/recovery/decision/v1 for P7 rwb-decision |
| CDC-19154 | RWB-S7-E6021-CON | DOR-RWB-S7-E6021-CON-8 | 12.2, 12.5 | Declare REST bases /api/recovery/case/v1, /api/recovery/source-data/v1 and /api/recovery/decision/v1; the story queue and branch are fixed |
| CDC-19172 | RWB-S7-E6022-CON | CG-ALL-11094 | 12.2 | Declare REST base /api/recovery/case/v1 for P3 rwb-case, as in the Document Index service table. |
| CDC-19173 | RWB-S7-E6022-CON | CG-ALL-11095 | 12.2 | Declare REST base /api/recovery/case/v1 for P3 rwb-case, as in the Document Index service table. |
| CDC-19174 | RWB-S7-E6022-CON | CG-ALL-11096 | 12.2 | Declare REST base /api/recovery/decision/v1 for P7 rwb-decision, as in the Document Index service table. |
| CDC-19175 | RWB-S7-E6022-CON | DOR-RWB-S7-E6022-CON-8 | header | Declare REST bases /api/recovery/case/v1 and /api/recovery/decision/v1 (see CG-ALL-11094 to CG-ALL-11096). |
| CDC-19185 | RWB-S7-E6023-APP | CG-ALL-11106 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the provider P1 rwb-source-data. |
| CDC-19186 | RWB-S7-E6023-APP | CG-ALL-11107 | 12.2 | Declare the REST base /api/recovery/case/v1 for the provider P3 rwb-case. |
| CDC-19187 | RWB-S7-E6023-APP | CG-ALL-11108 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the provider P7 rwb-decision. |
| CDC-19198 | RWB-S7-E6023-CON | CG-ALL-11120 | 12.2 | Declare the REST base /api/recovery/source-data/v1 of P1 rwb-source-data, per the Document Index service table. |
| CDC-19199 | RWB-S7-E6023-CON | CG-ALL-11121 | 12.2 | Declare the REST base /api/recovery/case/v1 of P3 rwb-case, per the Document Index service table. |
| CDC-19200 | RWB-S7-E6023-CON | CG-ALL-11122 | 12.2 | Declare the REST base /api/recovery/decision/v1 of P7 rwb-decision, per the Document Index service table. |
| CDC-19202 | RWB-S7-E6023-CON | DOR-RWB-S7-E6023-CON-8 | 12.2, 12.5 | Declare the REST bases of /api/recovery/source-data/v1, /api/recovery/case/v1 and /api/recovery/decision/v1 (CG-ALL-11120 to CG-ALL-11122). |
| CDC-19231 | RWB-S7-E6025-APP | CG-ALL-11161 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case read in the yaml. |
| CDC-19232 | RWB-S7-E6025-APP | CG-ALL-11162 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rule-package read in the yaml. |
| CDC-19235 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-8 | 12.5 | Add the base paths /api/recovery/case/v1 and /api/recovery/decision/v1; align WriteOffWorkflow task queue rwb-writeoff in rwb-recovery with Temporal Catalog v1. Workflow ID and start rule resolved in story (CG-ALL-11165). |
| CDC-19251 | RWB-S7-E6025-CON | CG-ALL-11174 | 12.2 | Declare the REST base /api/recovery/case/v1 for GET /cases/{caseId}. |
| CDC-19252 | RWB-S7-E6025-CON | CG-ALL-11175 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the WO rule package version read. |
| CDC-19253 | RWB-S7-E6025-CON | DOR-RWB-S7-E6025-CON-8 | 12.2 | Declare REST bases /api/recovery/case/v1 and /api/recovery/decision/v1; P2 items remain open. |
| CDC-19284 | RWB-S7-E6027-APP | CG-ALL-11206 |  | Declare the REST base /api/recovery/source-data/v1 using the provider's base from the Document Index service table. |
| CDC-19285 | RWB-S7-E6027-APP | CG-ALL-11207 |  | Declare the REST base /api/recovery/case/v1 using the provider's base from the Document Index service table. |
| CDC-19299 | RWB-S7-E6027-CON | CG-ALL-11218 | 12.2 | Declare the REST base /api/recovery/source-data/v1 from the Document Index service table. |
| CDC-19300 | RWB-S7-E6027-CON | CG-ALL-11219 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-19330 | RWB-S7-E6028-CON | CG-ALL-11249 | 12.2 | Declare REST base /api/recovery/case/v1 for the case read provider rwb-case (P3). |
| CDC-19331 | RWB-S7-E6028-CON | CG-ALL-11250 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package read provider rwb-decision (P7). |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (25)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19142 | RWB-S7-E6021-APP | CG-ALL-11062 | 16 | Add rows for TC-E6-021-01 to TC-E6-021-06 with Given, When and Then copied from the criteria they cover. |
| CDC-19143 | RWB-S7-E6021-APP | DOR-RWB-S7-E6021-APP-12 | 16 | On tab Story test cases, add TC-E6-021-02, -04, -05, -06, -07 and -08 with Given, When and Then; remove TC-E6-021-01 and -03, which RWB-ITG-E6021-ITG owns. |
| CDC-19156 | RWB-S7-E6021-CON | DOR-RWB-S7-E6021-CON-12 | 16 | On tab Story test cases, add TC-E6-021-01 to -06, TC-S7-E6021-CON-01 to -08 (08 is the section 12.7 table boundary test, AC7). |
| CDC-19159 | RWB-S7-E6021-CON | CG-ALL-11077 | 16 | Add rows TC-E6-021-01 to -06 and TC-S7-E6021-CON-01 to -09, with Given, When and Then copied from the criterion each covers; CON-09 is new in this story. |
| CDC-19167 | RWB-S7-E6022-APP | CG-ALL-11089 | 16 | Add tab Story test cases rows TC-E6-022-01 to TC-E6-022-05 with Given, When and Then copied from the criteria they cover. |
| CDC-19179 | RWB-S7-E6022-CON | DOR-RWB-S7-E6022-CON-12 Test cases: Partial | 16 | Section 16 now has 11 cases; TC-S7-E6022-CON-05 is the 12.7 tables boundary test (ASM-3438) and CON-06 covers AC8. v8 rows still to be added. |
| CDC-19183 | RWB-S7-E6022-CON | CG-ALL-11101 | 16 | Add rows for TC-E6-022-01 to -05 and TC-S7-E6022-CON-01 to -04 with Given, When and Then copied from the criterion each covers. |
| CDC-19194 | RWB-S7-E6023-APP | CG-ALL-11114 | 16 | Add rows TC-E6-023-01 to -06 with Given, When and Then copied from the criteria they cover; add TC-E6-023-07 and -08 added in section 16. |
| CDC-19207 | RWB-S7-E6023-CON | CG-ALL-11128 | 16 | Add rows for TC-E6-023-01 to TC-E6-023-06 and TC-S7-E6023-CON-01 to TC-S7-E6023-CON-07, with Given, When and Then copied from the criterion each covers. |
| CDC-19215 | RWB-S7-E6024-APP | CG-ALL-11142 | 16 | Add rows TC-E6-024-01 to TC-E6-024-05 with Given, When and Then copied from their criteria in the next version |
| CDC-19228 | RWB-S7-E6024-CON | DOR-RWB-S7-E6024-CON-12 | 12.7, 16 | Add Story test cases rows for TC-E6-024-01 to -05 and TC-S7-E6024-CON-01 to -06 on tab Story test cases |
| CDC-19230 | RWB-S7-E6024-CON | CG-ALL-11153 | 16 | Add rows for TC-E6-024-01 to TC-E6-024-05 and TC-S7-E6024-CON-01 to TC-S7-E6024-CON-05, with Given, When and Then copied from the criterion each covers. |
| CDC-19241 | RWB-S7-E6025-APP | CG-ALL-11167 | 16 | Add rows TC-E6-025-01 to TC-E6-025-06 to the Story test cases tab with Given, When and Then copied from the criteria they cover. |
| CDC-19243 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-12 | 16 | §16 holds 12 test cases (TC-E6-025-01 to 12) with contract (TC-07) and §12.7 boundary (TC-08) rows |
| CDC-19259 | RWB-S7-E6025-CON | DOR-RWB-S7-E6025-CON-12 | 12.7, 16 | Add rows in tab Story test cases for TC-E6-025-01 to -06 and TC-S7-E6025-CON-01 to -09. |
| CDC-19263 | RWB-S7-E6025-CON | CG-ALL-11180 | 16 | Add rows for TC-E6-025-01 to TC-E6-025-06 and TC-S7-E6025-CON-01 to TC-S7-E6025-CON-07, with Given, When and Then copied from the criterion each covers. |
| CDC-19271 | RWB-S7-E6026-APP | CG-ALL-11191 | 16 | Add Story test cases rows for TC-E6-026-01 to TC-E6-026-05 with Given, When and Then copied from the criterion each covers. |
| CDC-19283 | RWB-S7-E6026-CON | CG-ALL-11201 | 16 | Add rows for TC-E6-026-01 to -05, TC-S7-E6026-CON-01 to -06 with Given, When and Then copied from their criteria |
| CDC-19293 | RWB-S7-E6027-APP | CG-ALL-11213 | 16 | Add rows TC-E6-027-01 to TC-E6-027-06 with Given, When and Then copied from the criteria they cover. |
| CDC-19305 | RWB-S7-E6027-CON | DOR-RWB-S7-E6027-CON-12 | 16 | Add rows for TC-E6-027-01 to -06 and TC-S7-E6027-CON-01 to -06 under the same IDs. |
| CDC-19310 | RWB-S7-E6027-CON | CG-ALL-11224 | 16 | Add rows for TC-E6-027-01 to -06 and TC-S7-E6027-CON-01 to -05, with Given, When and Then copied from the criterion each covers. |
| CDC-19320 | RWB-S7-E6028-APP | CG-ALL-11241 | 16 | Add rows TC-E6-028-01 to TC-E6-028-06 with Given, When and Then copied from the criteria each covers. |
| CDC-19321 | RWB-S7-E6028-APP | DOR-RWB-S7-E6028-APP-12 | 12, 12.7, 16 | Add Story test cases rows for TC-E6-028-01 to TC-E6-028-10 under this story ID, with Given, When and Then copied from section 16. |
| CDC-19337 | RWB-S7-E6028-CON | DOR-RWB-S7-E6028-CON-12 | 12.7, 16 | Add rows for TC-E6-028-01 to -06 and TC-S7-E6028-CON-01 to -05 that the detcheck lists, and the new TC-S7-E6028-CON-06, under the same IDs. |
| CDC-19342 | RWB-S7-E6028-CON | CG-ALL-11255 | 16 | Add rows for TC-E6-028-01 to -06 and TC-S7-E6028-CON-01 to -05 with Given, When and Then copied from the criteria they cover. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19140 | RWB-S7-E6021-APP | CG-ALL-11052 | 11 | Add decision_record as a dictionary entity or record it as the platform library object created in rwb_writeoff. |
| CDC-19164 | RWB-S7-E6022-APP | CG-ALL-11083 |  | Add finance_feed_status (values accepted or rejected) as a field, or record the object in the owning document. |
| CDC-19184 | RWB-S7-E6022-CON | GAP-1809 |  | Record DEF-05 as an open question; carry the eleven write_off fields as the field set, marking the three GL-sourced fields as mirrored and never re-keyed. |
| CDC-19192 | RWB-S7-E6023-APP | CG-ALL-11105 | 12.7 | Record decision_record as a platform library table created in rwb_writeoff by RWB-PLT-E1027-CON, not as an LDM field. |
| CDC-19211 | RWB-S7-E6024-APP | CG-ALL-11134 | 12.7 | Add retry_count as the posting step's field from RWB-S7-E6021-APP, or name the dictionary field that carries the count |
| CDC-19227 | RWB-S7-E6024-CON | DOR-RWB-S7-E6024-CON-11 | 8 | Review sys_fields.is_personal (DF-REF-105) for the P2 fields this story carries and set it false where they are not personal data; the field list is not in the source documents. |
| CDC-19236 | RWB-S7-E6025-APP | CG-ALL-11157 | 16 | Add ends_at as the placement end field or confirm ended_at as its dictionary name; the story names ends_at at lines 186, 258, 303 and 395. |
| CDC-19237 | RWB-S7-E6025-APP | CG-ALL-11158 | 11 | Record decision_record as the decision-record library object or name its dictionary field; the story names it at line 240. |
| CDC-19238 | RWB-S7-E6025-APP | CG-ALL-11159 | 16 | Add recovered_amount (cash recovered) as a field or name the existing dictionary field; the story names it at line 258 and in TC-E6-025-02. |
| CDC-19239 | RWB-S7-E6025-APP | CG-ALL-11160 | 14 | Record recovery_log as an object (table or index) in LDM v9 or name the dictionary entity; the story names it at line 412. |
| CDC-19249 | RWB-S7-E6025-APP | GAP-0741 | 12.5, 15 | Add the retention timer type to LOV-TIMER; the retention period stays a parameter row per product group, unset until DL26; the S7 element names and the closure reason go to RWB-S7-E6025-CON and SCR-27 review. |
| CDC-19250 | RWB-S7-E6025-APP | GAP-2227 | 12.5, 15 | Add the retention timer type to LOV-TIMER; keep the retention period as a parameter row per product group, unset until DL26; confirm the S7 element names and closure reason at contract review. |
| CDC-19254 | RWB-S7-E6025-CON | CG-ALL-11172 | find it | Record ends_at as a dictionary field or the owning object, or name the existing field used for the placement end. |
| CDC-19255 | RWB-S7-E6025-CON | CG-ALL-11173 | find it | Record recovered_amount as a dictionary field or the owning object, or name the existing field used for the recovered amount. |
| CDC-19260 | RWB-S7-E6025-CON | GAP-0741 | 8 | Add a retention timer type to LOV-TIMER; the retention period is a parameter row per product group under DL26. Stage code names already match the rules in this story. |
| CDC-19261 | RWB-S7-E6025-CON | GAP-2227 | 8 | Add a retention timer type to LOV-TIMER; the retention period is a parameter row per product group under DL26. |
| CDC-19290 | RWB-S7-E6027-APP | CG-ALL-11204 | 11 | Record decision_record as a PLT library table created in rwb_writeoff (DP-03), or give its dictionary entry name. |
| CDC-19291 | RWB-S7-E6027-APP | CG-ALL-11205 | 11 | Record inbox_event as a PLT library table created in rwb_writeoff (ADR-015 inbox), or give its dictionary entry name. |
| CDC-19318 | RWB-S7-E6028-APP | CG-ALL-11232 | 17 | Record recovery_log as a retired legacy name in the owning document, or clear the dictionary check; the story names it only as a retired element with no write. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19155 | RWB-S7-E6021-CON | CG-ALL-11075 | 12.5 | Add activity prepareWriteOffPackForPosting (Activity, task queue rwb-writeoff) to the Activities sheet, or name a catalogued activity in its place. |
| CDC-19165 | RWB-S7-E6022-APP | CG-ALL-11087 | 12.5 | Add an Activities row for prepareFinanceFeed on task queue rwb-writeoff, or name a catalogued activity for the R-WO-26 step. |
| CDC-19166 | RWB-S7-E6022-APP | CG-ALL-11088 | 12.5 | Add an Activities row for sendFinanceFeed on task queue rwb-writeoff, or name a catalogued activity for the R-WO-27 and R-WO-28 step. |
| CDC-19176 | RWB-S7-E6022-CON | CG-ALL-11099 | 12.5 | Add activity prepareFinanceFeed to the Activities sheet, or name a catalogued activity in 12.5 |
| CDC-19177 | RWB-S7-E6022-CON | CG-ALL-11100 | 12.5 | Add activity sendFinanceFeed to the Activities sheet, or name a catalogued activity in 12.5 |
| CDC-19193 | RWB-S7-E6023-APP | CG-ALL-11112 | 12.5 | Add activity reconcilePopulations to the Activities sheet on task queue rwb-writeoff, or name a catalogued activity. |
| CDC-19203 | RWB-S7-E6023-CON | CG-ALL-11126 | 12.5 | Add activity reconcilePopulations (task queue rwb-writeoff) to the Activities sheet |
| CDC-19224 | RWB-S7-E6024-CON | CG-ALL-11152 | 12.5 | Add an Activities row for recordCorrection, or §12.5 names a catalogued activity instead |
| CDC-19240 | RWB-S7-E6025-APP | CG-ALL-11166 | 12.5 | Add closeAfterRetention to the Activities sheet with its inputs and outputs, or name the catalogued activity to use. |
| CDC-19256 | RWB-S7-E6025-CON | CG-ALL-11179 | 12.5 | Add an Activities row for closeAfterRetention on task queue rwb-writeoff, or name a catalogued activity in section 12.5. |
| CDC-19267 | RWB-S7-E6026-APP | DOR-RWB-S7-E6026-APP-8 | 12.5 | Add activities acceptCriteriaVersion and evaluateCriteria on rwb-writeoff, and state the WriteOffWorkflow ID form and start rule. |
| CDC-19269 | RWB-S7-E6026-APP | CG-ALL-11189 | 12.5 | Add activity acceptCriteriaVersion to the Activities sheet, or name a catalogued activity in its place. |
| CDC-19270 | RWB-S7-E6026-APP | CG-ALL-11190 | 12.5 | Add activity evaluateCriteria to the Activities sheet, or name a catalogued activity in its place. |
| CDC-19277 | RWB-S7-E6026-CON | DOR-RWB-S7-E6026-CON-8 | find it | Add Activities rows for acceptCriteriaVersion and evaluateCriteria and the WriteOffWorkflow ID form and start rule |
| CDC-19279 | RWB-S7-E6026-CON | CG-ALL-11199 | 12.5 | Add an Activities row for acceptCriteriaVersion or name a catalogued activity in its place |
| CDC-19292 | RWB-S7-E6027-APP | CG-ALL-11211 | 12.5 | Add activity applyPostChargeOffRecovery on task queue rwb-writeoff, owner S7, or use a catalogued activity. |
| CDC-19303 | RWB-S7-E6027-CON | CG-ALL-11222 | 12.5 | Add an Activities row for applyPostChargeOffRecovery on task queue rwb-writeoff. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19144 | RWB-S7-E6021-APP | DOR-RWB-S7-E6021-APP-6 | 10 | Add role SY-DATALOAD, named in section 10 of this story, to the roles list. |
| CDC-19168 | RWB-S7-E6022-APP | DOR-RWB-S7-E6022-APP-6 | 10 | Add role SY-DATALOAD to the roles table, or confirm its absence and remove it from the §10 Authority table. |
| CDC-19178 | RWB-S7-E6022-CON | DOR-RWB-S7-E6022-CON-1 | 1 | Add a role row for the tech lead of rwb-writeoff with a role code. Code Not specified in the source documents (DOR-RWB-S7-E6022-CON-1). |
| CDC-19195 | RWB-S7-E6023-APP | DOR-RWB-S7-E6023-APP-6 | 10 | Add the role SY-DATALOAD, which section 10 lists as a service identity. |
| CDC-19204 | RWB-S7-E6023-CON | DOR-RWB-S7-E6023-CON-1 | 1 | Add tech lead as a role name, or the section 1 persona names a role already listed there |
| CDC-19217 | RWB-S7-E6024-APP | DOR-RWB-S7-E6024-APP-6 | 10 | Add role SY-DATALOAD |
| CDC-19225 | RWB-S7-E6024-CON | DOR-RWB-S7-E6024-CON-1 | 1 | Add the role 'tech lead' of rwb-writeoff with its role code, or confirm the role name §1 and §10 use |
| CDC-19242 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-1 | 1 | Confirm Credit Administration officer as a role name or give its role code; section 1 now names the role alone with the unattended note moved to the next sentence. |
| CDC-19244 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-6 | 10 | Add role SY-DATALOAD to the role list, or confirm it is held there as a service identity with the write-off and posting rights in §10. |
| CDC-19257 | RWB-S7-E6025-CON | DOR-RWB-S7-E6025-CON-1 | 1 | Add 'tech lead' as a role code or name, or change the section 1 role to one already listed there. |
| CDC-19272 | RWB-S7-E6026-APP | DOR-RWB-S7-E6026-APP-6 | 10 | Add role SY-DATALOAD as a service identity of the write-off step, or this story removes it from section 10. DP-08 authorise check stated in section 10. |
| CDC-19281 | RWB-S7-E6026-CON | DOR-RWB-S7-E6026-CON-1 | 1 | Add a role named tech lead (the Tech lead of rwb-writeoff of section 10) as a role code or role name |
| CDC-19295 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-6 | 10 | Add role SY-DATALOAD, which section 10 of RWB-S7-E6027-APP names, to the roles of the document. |
| CDC-19322 | RWB-S7-E6028-APP | DOR-RWB-S7-E6028-APP-6 | 10 | Add role SY-DATALOAD, the role section 10 names, to the register. |
| CDC-19326 | RWB-S7-E6028-APP | GAP-1314 | 12.5 | Read TSD P7 v2 T-A.1 Decision log right A as the right on approval operations and the FSD P7 v3 T6.1 column as read only; carry WRITE_OFF_AND_POSTING on the approval row and require both in the authorise answer; add RW-CREDCOMM to the holders of the capability right, or record why the routed role cannot decide, before the wave entry check. |
| CDC-19336 | RWB-S7-E6028-CON | DOR-RWB-S7-E6028-CON-1 | 1 | Add tech lead as a role code or role name, or the story names an existing role code or role name from Users Roles and Permissions v5 in section 1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19145 | RWB-S7-E6021-APP | DOR-RWB-S7-E6021-APP-7 | 11 | Add decision_record as an entity or field of the PLT decision-record library in rwb_writeoff, and classify it in Data Classification v5. |
| CDC-19169 | RWB-S7-E6022-APP | DOR-RWB-S7-E6022-APP-7 | 11 | Register field finance_feed_status and entity decision_record in LDM v9 or Data Classification v5. |
| CDC-19196 | RWB-S7-E6023-APP | DOR-RWB-S7-E6023-APP-7 | 7, 11 | Add decision_record as the PLT decision-record library entity with fields DF-DEC-001 to DF-DEC-018. |
| CDC-19218 | RWB-S7-E6024-APP | DOR-RWB-S7-E6024-APP-7 | 11 | Name retry_count as a field of the posting step record and decision_record as a PLT library object of rwb_writeoff |
| CDC-19245 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-7 | 11 | Add ends_at, decision_record, recovered_amount and recovery_log as fields or entities, or confirm the library and rule names they map to. |
| CDC-19268 | RWB-S7-E6026-APP | CG-ALL-11185 | header | Add tax_criteria_version with its owner, or record it as an object of the rwb-decision (P7) package with its owner. |
| CDC-19273 | RWB-S7-E6026-APP | DOR-RWB-S7-E6026-APP-7 | 11 | Add tax_criteria_version as a field of the write-off package read, or record it as a package fact with no column (GAP-3043; ASM-5104). |
| CDC-19278 | RWB-S7-E6026-CON | CG-ALL-11195 | find it | Add a field or entity for tax_criteria_version, or confirm its dictionary name and owner |
| CDC-19282 | RWB-S7-E6026-CON | DOR-RWB-S7-E6026-CON-7 | 11 | Register tax_criteria_version as a field or entity, or name its home |
| CDC-19316 | RWB-S7-E6028-APP | CG-ALL-11230 | find it | Record placement_type in the owning document as the request input of R-WO-32 with its value set, or add its dictionary name. |
| CDC-19317 | RWB-S7-E6028-APP | CG-ALL-11231 | find it | Record decision_record as the PLT library decision record object created in rwb_writeoff (DP-03), or add its dictionary name. |
| CDC-19323 | RWB-S7-E6028-APP | DOR-RWB-S7-E6028-APP-7 | 11, 17 | Register placement_type (condition of R-WO-32) and decision_record (library object of rwb_writeoff) as fields or entities with field IDs. |
| CDC-19334 | RWB-S7-E6028-CON | CG-ALL-11246 | header | Section 11 BR Field ID column notes placement_type is absent from both documents |

### Epic design record (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19137 | RWB-S7-E6021-APP | DOR-RWB-S7-E6021-APP-14 |  | Confirm and record the signed epic design sign-off, which the story and source documents do not contain. |
| CDC-19160 | RWB-S7-E6022-APP | DOR-RWB-S7-E6022-APP-14 |  | Record the signed epic design sign-off for RWB-SVC-S7 / EP06 in the epic design record. |
| CDC-19188 | RWB-S7-E6023-APP | DOR-RWB-S7-E6023-APP-14 | find it | Record the signed epic design sign-off reference for this epic. |
| CDC-19201 | RWB-S7-E6023-CON | DOR-RWB-S7-E6023-CON-14 | 1 | Record the signed epic design sign-off, or confirm that none exists; the story cannot carry a sign-off it does not hold. |
| CDC-19222 | RWB-S7-E6024-CON | DOR-RWB-S7-E6024-CON-14 | none | Confirm and record the signed epic design sign-off for this story's epic. |
| CDC-19233 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-14 | header | Record the signed epic design sign-off for RWB-S7-E6025-APP in the epic design record. |
| CDC-19264 | RWB-S7-E6026-APP | DOR-RWB-S7-E6026-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S7 in the epic design record. |
| CDC-19276 | RWB-S7-E6026-CON | DOR-RWB-S7-E6026-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S7 |
| CDC-19286 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-14 |  | Record the signed epic design sign-off for EP06 and RWB-SVC-S7, or confirm the existing sign-off. |
| CDC-19332 | RWB-S7-E6028-CON | DOR-RWB-S7-E6028-CON-14 | header | Record the signed epic design sign-off for RWB-S7-E6028-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19208 | RWB-S7-E6024-APP | CG-ALL-11136 | 12.1 | Publish POST /write-offs/{writeOffId}/correction-decision through RWB-S7-E6024-CON, or remove the operation from this story. |
| CDC-19221 | RWB-S7-E6024-CON | CG-ALL-11147 | 12.1 | Publish POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/correction-decision (proposed path, GAP-3040, ASM-5092) with CorrectionRequest in and WriteOffCorrection 200 out. |
| CDC-19311 | RWB-S7-E6028-APP | CG-ALL-11233 | 12.1 | Publish POST /write-offs/{writeOffId}/sale-selection with its operation ID through RWB-S7-E6028-CON; operation ID Not specified in the source documents (GAP-3049). |
| CDC-19312 | RWB-S7-E6028-APP | CG-ALL-11234 | 12.1 | Publish GET /write-offs?sale=SOLD_POST_CHARGEOFF with its operation ID through RWB-S7-E6028-CON; operation ID Not specified in the source documents (GAP-3049). |
| CDC-19328 | RWB-S7-E6028-CON | CG-ALL-11247 | 12.1 | Add the operation POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/sale-selection, operation ID Not specified in the source documents (GAP-3050; ASM-5125), or remove it. |
| CDC-19329 | RWB-S7-E6028-CON | CG-ALL-11248 | 12.1 | Add the operation GET /api/recovery/writeoff/v1/write-offs?sale=SOLD_POST_CHARGEOFF, path and filter Not specified in the source documents (GAP-3050; ASM-5125), or remove it. |
| CDC-19333 | RWB-S7-E6028-CON | DOR-RWB-S7-E6028-CON-8 | 12.1, 12.2 | Add POST /write-offs/{writeOffId}/sale-selection and GET /write-offs?sale=SOLD_POST_CHARGEOFF with their operation IDs, and the /api/recovery/case/v1 and /api/recovery/decision/v1 bases. Path and operation ID Not specified in the source documents (GAP-3050; ASM-5125). |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19139 | RWB-S7-E6021-APP | DOR-RWB-S7-E6021-APP-8 | 12 | Add base paths /api/recovery/case/v1, /api/recovery/source-data/v1 and /api/recovery/decision/v1; align WriteOffWorkflow queue and namespace with the story or the catalog. |
| CDC-19191 | RWB-S7-E6023-APP | DOR-RWB-S7-E6023-APP-8 | 12.5 | Add the base paths /api/recovery/source-data/v1, /api/recovery/case/v1 and /api/recovery/decision/v1 to the yaml; align the WriteOffWorkflow task queue and namespace with the catalog. |
| CDC-19289 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-8 | 12 | Add base paths /api/recovery/source-data/v1 and /api/recovery/case/v1; align WriteOffWorkflow task queue rwb-writeoff and namespace rwb-recovery with the catalog. |
| CDC-19302 | RWB-S7-E6027-CON | DOR-RWB-S7-E6027-CON-8 | find it | Declare the two REST bases in the yaml and catalog WriteOffWorkflow ID form and activity rows as listed in items 1-3, 8 and 9. |

### RWB-S7-E6022-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19161 | RWB-S7-E6022-APP | DOR-RWB-S7-E6022-APP-21 |  | Set the build status to Done before this story starts. |
| CDC-19162 | RWB-S7-E6022-APP | DOR-RWB-S7-E6022-APP-22 |  | Publish the contract fake library and record its published version. |
| CDC-19171 | RWB-S7-E6022-APP | GAP-3036 | 10 | Declare no provided operation and the two absence records; keep placeholders, confirm operation names and feed values before tag, bind errors to section 14 message IDs, record the tag date. |
| CDC-19182 | RWB-S7-E6022-CON | GAP-3036 | 8 | Record the baseline tag date; confirm the three operation names and the feed values with their owners before the tag; bind every error condition to one message id of section 14. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19213 | RWB-S7-E6024-APP | CG-ALL-11140 | 12.5 | Add activity raiseWriteOffException on task queue rwb-writeoff, or name a catalogued activity |
| CDC-19214 | RWB-S7-E6024-APP | CG-ALL-11141 | 12.5 | Add activity recordCorrection on task queue rwb-writeoff, or name a catalogued activity |
| CDC-19280 | RWB-S7-E6026-CON | CG-ALL-11200 | 12.5 | Add activity evaluateCriteria on task queue rwb-writeoff to the Activities sheet |
| CDC-19319 | RWB-S7-E6028-APP | CG-ALL-11240 | 12.5 | Add recordSaleSelection as an rwb-writeoff Activity row, or name a catalogued activity in the story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19141 | RWB-S7-E6021-APP | CG-ALL-11060 | 12.5 | Add activity prepareWriteOffPackForPosting on task queue rwb-writeoff, or name a catalogued activity in the story. |
| CDC-19223 | RWB-S7-E6024-CON | CG-ALL-11151 | 12.5 | Add activity raiseWriteOffException to the Activities sheet, or name a catalogued activity instead. |
| CDC-19335 | RWB-S7-E6028-CON | CG-ALL-11254 | 12.5 | Add activity recordSaleSelection for rwb-writeoff, or name a catalogued activity for the sale step in the story. |

### RWB-S7-E6023-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19189 | RWB-S7-E6023-APP | DOR-RWB-S7-E6023-APP-21 | find it | Set the build status to Done once the contract is published. |
| CDC-19190 | RWB-S7-E6023-APP | DOR-RWB-S7-E6023-APP-22 | find it | Record the published contract fake library version. |
| CDC-19197 | RWB-S7-E6023-APP | GAP-3038 | 13 | Publish the reconciliation baseline with placeholders for unpublished names, class C rows for the four consumed rows, and confirm the posting product, event and cross-reference before tagging. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19205 | RWB-S7-E6023-CON | DOR-RWB-S7-E6023-CON-9 | 14 | Align MSG-P1-001 text with the standard, or record the FSD S7 A2.11.3.1 wording as the approved variant |
| CDC-19296 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-9 | 14 | Align the text of MSG-P1-001 to the section 14 wording (FSD S7 A2.15.3.1) or confirm the standard's text. |
| CDC-19306 | RWB-S7-E6027-CON | DOR-RWB-S7-E6027-CON-9 | 14 | Confirm the MSG-P1-001 text the Standard holds, so section 14 can copy it. Section 14 wording is kept until then. |

### RWB-S7-E6021-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19138 | RWB-S7-E6021-APP | DOR-RWB-S7-E6021-APP-21 |  | Set the build status to Done once the contract is published, so this story's contract dependency is met. |
| CDC-19148 | RWB-S7-E6021-APP | GAP-3034 |  | Publish the baseline: four consumed rows and placeholders, state enumeration with unprinted POSTING values marked, decision_log_id as local record identifier, prepared-pack schema, and no ALS/GL element declared. |

### RWB-ITG-E6021-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19147 | RWB-S7-E6021-APP | GAP-0456 |  | Agree the ALS and general-ledger answer, posting reference format, rejection codes and retry settings with the ACE integration path owners at the wave 4 entry check; hold each as a fixture. |
| CDC-19158 | RWB-S7-E6021-CON | GAP-0456 | find it | Agree the ALS and general-ledger answer, the posting reference format, the rejection codes and the retry settings with the ACE integration path owners at the wave 4 entry check; hold each as a fixture. |

### RWB-S7-E6022-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19170 | RWB-S7-E6022-APP | GAP-3035 | 12.5 | Record the four consumed reads and the Finance feed call as class C with their placeholders; keep the three H rows as they stand. |
| CDC-19180 | RWB-S7-E6022-CON | GAP-3035 | 12.1 | Keep the H, C, I and X rows; record the four reads and the feed call as class C with placeholders; declare no provided operation; carry the feed fields in the record and the case state with no column |

### RWB-S7-E6024-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19210 | RWB-S7-E6024-APP | DOR-RWB-S7-E6024-APP-21 | Header | Reach build status Done with the contract published, so this story's contract dependency is met. |
| CDC-19220 | RWB-S7-E6024-APP | GAP-3040 | 13 | Publish correction operation and its two elements with placeholders, the loop owner and service level as reference values, and section 14 message IDs for errors |

### RWB-S7-E6024-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19226 | RWB-S7-E6024-CON | DOR-RWB-S7-E6024-CON-10 | find it | Add the empty, loading, error and no-access states of SCR-27 in the app story |
| CDC-19229 | RWB-S7-E6024-CON | GAP-3039 | find it | Add the SCR-27 exception state to the app story; this baseline now carries the correction operation, retry and reference rows and R-WO-41 and R-WO-43 |

### RWB-S7-E6025-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19234 | RWB-S7-E6025-APP | DOR-RWB-S7-E6025-APP-21 | header | Bring RWB-S7-E6025-CON to Done so that its contract is published. |
| CDC-19247 | RWB-S7-E6025-APP | GAP-3042 | 5, 12.5 | Publish the baseline: placeholders, a message id per error condition, the case boundary, timer and placement elements, the two closure states, the closing-entry element, versioned retention reference data, and confirmed operation names. |

### RWB-S7-E6026-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19265 | RWB-S7-E6026-APP | DOR-RWB-S7-E6026-APP-21 | header | Build the contract and set its build status to Done. |
| CDC-19266 | RWB-S7-E6026-APP | DOR-RWB-S7-E6026-APP-22 | header | Publish the contract fake library and record its version in that story. |

### RWB-S7-E6027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19287 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-21 |  | Publish the contract and set its build status to Done before this story starts. |
| CDC-19288 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-22 |  | Publish a contract fake library version and record it as published. |

### OTHER:split plan (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19298 | RWB-S7-E6027-APP | GAP-3048 | 8 | Record DP-04, DP-07, DP-09 and DP-16 as dependencies the plan does not hold; keep its C row as None; raise the fee ownership question to the solution architect before the baseline tag |
| CDC-19308 | RWB-S7-E6027-CON | GAP-1798 |  | Carry placement, result and recall as product behaviour; hold every placement decision until the partner contract is published in the same wave; sequence the placement slice last inside wave 4. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19324 | RWB-S7-E6028-APP | GAP-1794 | 12.7 | Add Tables rows for the four rwb_writeoff entity groups (eligibility, committee, posting, recovery after charge-off) with fields and keys per Architecture v5 slides 20 and 41; state the physical name of write_off. |
| CDC-19338 | RWB-S7-E6028-CON | GAP-1794 | find it | Add rows for the four rwb_writeoff entity groups (eligibility, committee, posting, recovery after charge-off) with key fields; fix write_off as the one physical table held; add the remaining tables with the S7 DB story. |

### RWB-S7-E6021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19146 | RWB-S7-E6021-APP | GAP-3033 |  | Record rwb-source-data, rwb-case and rwb-decision reads as class C rows with H unchanged; treat DP-05 as consumed on rwb-source-data; add REQ-S7-002 and REQ-S7-005 to both stories' traceability at D1. |

### RWB-S7-E6021-CON; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19153 | RWB-S7-E6021-CON | DOR-RWB-S7-E6021-CON-14 | not in supplied text | Record the signed epic design sign-off for RWB-S7-E6021-CON, then the story can state it. No sign-off value was invented. |

### RWB-S7-E6021-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19157 | RWB-S7-E6021-CON | GAP-3033 | find it | Record the four consumed rows as class C with the H row unchanged; treat DP-05 as consumed on rwb-source-data's contract; keep the ALS and GL crossing, re-post and provision release with RWB-ITG-E6021-ITG; add REQ-S7-002 and REQ-S7-005 to both stories' traceability at D1. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:R-WO-21 to R-WO-24) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19163 | RWB-S7-E6022-APP | GAP-1793 | 1 | Align the FSD posting to rwb-payment's queue, and confirm the split with the P8 owner before wave 4 system test. |

### OTHER:Feed interface path owner: Not specified in the source documents (GAP-1796) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19181 | RWB-S7-E6022-CON | GAP-1796 | 8 | BR5 carries the feed as a requirement; the path owner is not named, so the item moves out of the story. |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19206 | RWB-S7-E6023-CON | GAP-3037 | 4 | GAP-3037 belongs to RWB-S7-E6023-APP; the placeholders written in this story do not resolve that story's gap. |

### Epic design record; OTHER:RWB-SVC-S7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19209 | RWB-S7-E6024-APP | DOR-RWB-S7-E6024-APP-14 | Header | Record the signed epic design sign-off for EP06 under RWB-SVC-S7. No sign-off exists in the source documents. |

### OTHER:PLT library (decision_record library table in rwb_writeoff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19212 | RWB-S7-E6024-APP | CG-ALL-11135 | 12.7 | Record decision_record as a PLT library table created in rwb_writeoff, or name the dictionary entity |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19216 | RWB-S7-E6024-APP | DOR-RWB-S7-E6024-APP-10 | 15 | Add the empty, loading, error and no access states of SCR-27 Write-off proposal to the screen-state vocabulary of SCR-27. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19219 | RWB-S7-E6024-APP | GAP-3039 | 13 | Owner, time limit and SCR-27 states recorded in sections 8, 11 and 15. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19246 | RWB-S7-E6025-APP | GAP-1797 | 12.5 | Add a P5 cell and a call type to the S7 row of the connection matrix for the committee pack document and its retention class; P5 owner to confirm the call type. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19248 | RWB-S7-E6025-APP | GAP-0457 | find it | Record the proposed fix on GAP-0457: set the retention period under DL26 before the wave 4 entry check; hold it as a reference value in the fixture until then; agree the clock mechanism, evidence shape and pass or fail gate with Compliance and the integration lead (owner role Integration lead). |

### OTHER:Recovery Workbench Screen Specifications v1 (aisdlc/requirement/legacy/07-screens-and-experience/recovery-workbench-scre (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19258 | RWB-S7-E6025-CON | DOR-RWB-S7-E6025-CON-10 | 15 | Add empty, loading, error and no access states for SCR-27 Write-off proposal; the story already flags them as Not specified (CG-ALL-11183), so section 15 is unchanged. |

### RWB-S7-E6025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19262 | RWB-S7-E6025-CON | GAP-3041 | 12.5 | Keep the H, C, I and X rows; add rwb-case and rwb-decision as class C placeholder rows; record the three dependencies as tracked dependencies; carry the retention classes and closing amounts as the APP story fixes them. |

### OTHER:rwb-decision (P7) contract baseline and TSD S7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19274 | RWB-S7-E6026-APP | GAP-3044 | find it | Publish the criteria-version element, run state and pin with their field list, required flags and payload at the wave 4 contract freeze (GAP-3044). |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19275 | RWB-S7-E6026-CON | CG-ALL-11196 | 13 | Create story file RWB-P7-E1073-CON or name the existing story that holds the WO rule authoring dependency |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19294 | RWB-S7-E6027-APP | DOR-RWB-S7-E6027-APP-11 | 13 | Classify the customer and account fields read from rwb-source-data as personal data, or correct the story's none-carried guardrail statement. |

### OTHER:Technical Specification S7 (TSD S7), section T-A.1 and T3.1 to T6.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19297 | RWB-S7-E6027-APP | GAP-3047 |  | Publish the consumed rwb-payment event name, topic element, payload and CloudEvents fields; the property lists of the two module operations; the rwb-source-data payment read name; the rwb-case reference-data read name; the P8 posting activity name; and the fee element as a consumed reference-data row. Owner: solution architect, to confirm before the tag. |

### RWB-S7-E6027-CON; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19301 | RWB-S7-E6027-CON | DOR-RWB-S7-E6027-CON-14 | find it | Record the signed epic design sign-off in the epic design record. |

### RWB-S7-E6027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19304 | RWB-S7-E6027-CON | DOR-RWB-S7-E6027-CON-10 | find it | Add empty, loading, error and no-access states to SCR-27. This contract story declares no screen states. |

### OTHER:split plan (C row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19307 | RWB-S7-E6027-CON | GAP-3046 | 8 | BR7, BR12 and section 11 already declare no operation, no published event and no fee column. The empty plan C row belongs to the plan document. |

### OTHER:split plan (C rows); OTHER:change log (DP-04; OTHER:DP-07; OTHER:DP-09; OTHER:DP-16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19309 | RWB-S7-E6027-CON | GAP-3048 | 8 | Fee reference stays on the record only (BR5). The plan C rows and DP-04/07/09/16 belong to other documents. Architect question remains open before the baseline tag. |

### RWB-S7-E6028-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19313 | RWB-S7-E6028-APP | DOR-RWB-S7-E6028-APP-14 | header | Record the signed epic design sign-off that covers RWB-S7-E6028-APP. |

### RWB-S7-E6028-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19314 | RWB-S7-E6028-APP | DOR-RWB-S7-E6028-APP-21 | header | Set build status to Done once the contract is published; currently Not started. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19315 | RWB-S7-E6028-APP | DOR-RWB-S7-E6028-APP-8 | find it | Add POST /write-offs/{writeOffId}/sale-selection and GET /write-offs?sale=SOLD_POST_CHARGEOFF to rwb-writeoff.yaml once defined; add bases /api/recovery/case/v1 and /api/recovery/decision/v1 to the v5 yamls; add the three further paths in the detcheck. |

### OTHER:TSD P7 v2 (T-A.1; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19325 | RWB-S7-E6028-APP | GAP-1311 | 12.5 | Publish the raise as POST /approvals on the decision base with caseId, decisionCode, regulationItem, capabilityArea, productGroup, amount, sourceType, sourceRef, ruleId, ruleVersion and Idempotency-Key; give field sets for ApprovalPage, ApprovalDetail, ApprovalAction, DecisionLogPage and DecisionLogEntry; read decision code and final calls as LOV-DECISION and final-call reference data; keep the five LOV-APPROVAL-STATUS values with escalation_level inside WAITING; state the message texts and login name as the proposed fix of GAP-1311 sets. |

### RWB-S7-E6028-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19327 | RWB-S7-E6028-APP | GAP-1312 | 13 | Carry H RWB-PLT-E1027-CON (DP-03) and H RWB-PLT-N001-CON (DP-19) as non-blocking platform contracts of wave 0; carry the four consumed contracts (P4 delegation-limit answer, P4 authorise call, P3 case read, reference-data list values) as published contracts of P3 and P4, built against their fakes; leave the metadata rows as the plan gives them. |

### OTHER:Recovery Workbench TSD P7 v2 (T-A.1 and T-A.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19339 | RWB-S7-E6028-CON | GAP-1311 | find it | Publish the approval raise as POST /approvals with the body fields of the proposed fix; define ApprovalAction, ApprovalPage, ApprovalDetail, DecisionLogPage and DecisionLogEntry field sets; read decision code and final calls as LOV-DECISION and the final-call list; keep the five LOV-APPROVAL-STATUS values and carry escalation through escalation_level. |

### OTHER:Recovery Workbench TSD P7 v2 (T-A.1 and T6.1) and P4 role model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19340 | RWB-S7-E6028-CON | GAP-1314 | find it | Read Decision log right A of T-A.1 as the right on the approval operations; carry WRITE_OFF_AND_POSTING on the approval row; add RW-CREDCOMM to the capability right holders in the P4 role model or record why the rule routes to a role that cannot decide, before the wave entry check. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19341 | RWB-S7-E6028-CON | GAP-1312 | find it | Carry H RWB-PLT-E1027-CON (DP-03) and H RWB-PLT-N001-CON (DP-19) and the four consumed contracts as non-blocking wave 0 platform contracts, built against their fakes; leave the metadata rows as the plan gives them. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0456 | The write-off posting harness pack, the ALS and general ledger answer and the posting reference format are not specified | Integration lead | Resolved (directive) |
| GAP-0457 | The retention period, the closure evidence pack and the synthetic clock for the retention close are not specified | Integration lead | Resolved (directive) |
| GAP-0458 | The post charge-off sale harness pack for the debt sale handover is not specified | Integration lead | Resolved (directive) |
| GAP-0741 | The case side of the retention closure leaves the retention period, the retention timer type, the S7 contract element names, the route-set state names, the closure reason and the screen field names unspecified | Tech lead, with the rwb-writeoff contract owner and the rwb-case reference-data owner (RW-COE) | Resolved (directive) |
| GAP-1311 | The approval item and its two records: the raise operation, the action and answer shapes, the routing and final-call value sets, the message texts and the login name have no source | Business analyst, P7 rwb-decision, with the P4 rwb-access business analyst and the S7 rwb-writeoff analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1312 | The DP table adds two platform contracts and the story consumes three operations that its metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-access team | Resolved (directive) |
| GAP-1314 | The right and the role that may approve an escalated write-off pack are read two ways | P4 rwb-access business analyst and the security administrator, with the P7 rwb-decision business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1792 | The FSD reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1793 | The FSD posts to ALS and the general ledger from this module, while Architecture v5 gives the posting to rwb-payment | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1794 | The Ownership Map lists one table for rwb-writeoff, while Architecture v5 gives the schema four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1796 | The Finance provision feed has no interface path: P2 is outbound-only and the matrix gives S7 no cell to it | Solution architect with the integration lead | Resolved (directive) |
| GAP-1797 | The committee pack is a document in the document hub, and the matrix connects S7 to P5 on no path | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1798 | Agency placement, result and recall run through the partner portal, which is S9 and is created in the same wave | Partner and agency manager with S9 | Resolved (directive) |
| GAP-1799 | A charged-off population is handed to the debt sale route, and neither service's matrix row shows the other | Solution architect with the S6 owner | Resolved (directive) |
| GAP-1800 | The FSD routing rules move the case through twenty states, while Architecture v5 gives the case state to rwb-case | Solution architect with the P3 owner | Resolved (directive) |
| GAP-1802 | The fifty-one write-off rules exist but their package has no owner and no version in force | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1807 | The FSD has no wait for the ledger acknowledgement that strict mode requires before a posting | Solution architect | Resolved (directive) |
| GAP-1809 | The FSD defers the mirrored GL fields of write_off to DEF-05, which no source read here defines | Data architect | Resolved (directive) |
| GAP-1812 | Payment matching after charge-off is given to this module, while P8 owns payment and proceeds matching | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1813 | Completeness is published to a channel the sources remove | Solution architect | Resolved (directive) |
| GAP-2227 | Retention period, retention timer type, S7 contract element names, closure reason value and screen field names of the retention closure are not stated in the sources | TechX, rwb-writeoff contract owner and rwb-case reference-data owner (RW-COE) | Resolved (directive) |
| GAP-3033 | RWB-S7-E6021-APP: the plan holds no C or X row for the four consumed contracts of the pack-prepared step, no dependency row for DP-05, no interface for the ALS and general-ledger crossing, and no separate story for the shared pack rule R-WO-05 | Solution architect with the rwb-writeoff tech lead, the rwb-source-data, rwb-case and rwb-decision owners and the wave 4 integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3034 | RWB-S7-E6021-CON: the consumed operation names, the ACE and ledger shapes, the unprinted state values, the prepared-posting-pack element and the ALS and general-ledger interface have no published baseline | Solution architect with the rwb-writeoff tech lead and the owners of rwb-source-data, rwb-case and rwb-decision | Resolved (directive) |
| GAP-3035 | RWB-S7-E6022-APP: the Finance feed slice provides no operation while four consumed surfaces and one external feed have no plan row, no column carries the feed result, and the feed transport, layouts and codes are unpublished | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3036 | RWB-S7-E6022-CON: the contract baseline declares no operation and no answer property because TSD S7 T-A publishes no feed surface and no column carries the result, while the feed values, the operation names and the module's list of values are unpublished | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3037 | RWB-S7-E6023-APP: the reconciliation step has no published operation, no posting-product operation or event name, no matching cross-reference, no plan C row for its three consumed services, no job or Schedule for its monthly trigger and no requirement row | Solution architect | Resolved (directive) |
| GAP-3038 | RWB-S7-E6023-CON: the reconciliation baseline has no published operation, element, posting-product name, matching cross-reference or completeness element, and its consumed rows have no plan row | Solution architect | Resolved (directive) |
| GAP-3039 | RWB-S7-E6024-APP: no source publishes the correction operation or its elements, the loop's owner and time limit that REQ-S7-004 requires are unconfirmed, the retry count has no column, the other two entries to WRITEOFF_EXCEPTION have no feature, and SCR-27 has no exception state | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3040 | RWB-S7-E6024-CON: the correction operation, its two elements and the loop's owner and service level have no published baseline, the retry count has no element, and the plan's C row is empty while four rows are consumed | Solution architect | Resolved (directive) |
| GAP-3041 | RWB-S7-E6025-APP: the closure slice has no plan row for its five consumed contracts, its rule kit, its event library, its scheduler marker, the retention period, the placement record or the closing amounts | Solution architect | Resolved (directive) |
| GAP-3042 | RWB-S7-E6025-CON: the consumed operation names, the placement element, the retention period and class, the closing amounts and the two unprinted rule rows have no published baseline | Solution architect | Resolved (directive) |
| GAP-3044 | No published field list for the criteria-version element, and the package read has no name, no call type and no owner document | Solution architect with the owner of rwb-decision and the rwb-writeoff tech lead | Resolved (directive) |
| GAP-3046 | RWB-S7-E6027-APP: the post charge-off recovery has no REST operation, no published event name, no fee column and no screen state, and the plan's C row is empty while two rows and one event are consumed | Solution architect | Resolved (directive) |
| GAP-3047 | RWB-S7-E6027-CON: the consumed event, the two consumed operation names, the posting activity name, the fee element and the case-move answer have no published baseline, and the step publishes no event | Solution architect | Resolved (directive) |
| GAP-3048 | R-WO-37's agency fee calculation is also FEAT-PRM-07 of rwb-partner, and neither the plan's C rows nor DP-04, DP-07, DP-09 and DP-16 carry what the recovery step consumes | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S7-E6023-CON | Not specified without item ID | 459 | - No personal data in a schema, an example or a fake: identifiers, amounts, a code and a rule version only, and the populations are compared by reference, never |
| RWB-S7-E6024-APP | new AC without TC row | 456 | AC4 is new and no section 16 row covers it |
| RWB-S7-E6024-APP | new AC without TC row | 456 | AC5 is new and no section 16 row covers it |
| RWB-S7-E6024-APP | new AC without TC row | 456 | AC6 is new and no section 16 row covers it |
| RWB-S7-E6024-APP | new AC without TC row | 456 | AC7 is new and no section 16 row covers it |
