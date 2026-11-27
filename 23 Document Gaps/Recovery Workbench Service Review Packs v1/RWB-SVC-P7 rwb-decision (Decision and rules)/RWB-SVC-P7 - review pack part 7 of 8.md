# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 7 of 8 (RWB-P7-E2028-APP to RWB-P7-E6028-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 178 |
| Cross-document (pending in another document) | 201 |
| Not applied (value not in the sources) | 40 |
| Open business decisions | 28 |
| Register gaps linked | 134 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E2028-APP | 13 | 17 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2028 APP Case intake agent live at L1 [E3a] v2.md |
| RWB-P7-E2029-APP | 22 | 25 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v2.md |
| RWB-P7-E2032-APP | 15 | 19 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2032 APP TDR offer-suggestion model through the model gateway [E3e] v2.md |
| RWB-P7-E2035-APP | 19 | 22 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2035 APP Next action on the case v2.md |
| RWB-P7-E2036-APP | 21 | 15 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2036 APP Queue write interface for models and agents v2.md |
| RWB-P7-E2041-APP | 23 | 22 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2041 APP Rule change governance and audit report v2.md |
| RWB-P7-E2042-APP | 27 | 29 | 14 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2042 APP Epic 2 rule packages in Drools v2.md |
| RWB-P7-E2043-APP | 23 | 25 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2043 APP Temporal and Drools integration pattern and reference case workflow v2.md |
| RWB-P7-E6028-APP | 15 | 21 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E6028 APP Sell a post charge-off population v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-E2032-APP | R-11342 | CG-ALL-7373 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2035-APP | R-11346 | CG-ALL-7385 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2041-APP | R-11356 | CG-ALL-7416 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2042-APP | R-11362 | CG-ALL-7429 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2042-APP | R-11363 | CG-ALL-7434 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-P7-E2043-APP | R-11371 | CG-ALL-7448 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E6028-APP | R-11379 | CG-ALL-7466 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-ITG-E2029-ITG, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P7-E2029-APP, RWB-S8-E2029-APP | R-22656 | GAP-1828 | Register gap | Risk and model risk officer | The confidence threshold for the low-confidence review and the evidence required to run the agent at L1 are not stated | Read the threshold and the autonomy policy from versioned reference data held by rwb-agent and rwb-decision, assert no number, and leave the evidence pack and the approval of a level change to Q-014 and BR-084. |
| RWB-ITG-E2041-ITG, RWB-P3-E2041-APP, RWB-P3-E2041-CON, RWB-P4-E2041-APP, RWB-P7-E2041-APP | R-22719 | GAP-0963 | Register gap | Solution architect with internal audit | The record code and the field shape of a rule-change authority and of an audit export inside a decision-record entry are not specified | Carry the capability area, the right, the action, the version label, the author reference, the period, the package, the format, the row count and the matrix version in the actions list of the decision-record entry, reuse AC-READ, AC-DENY and AC-EXPT rather than minting a fourth code, and add the fields in the next LDM version with audit. |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-22736 | GAP-1306 | Register gap | Center of excellence analyst with the P3 reference-data owner and the business owner | The decision code of a reference-case step and the value set of LOV-DECISION are not fixed by any source | Enumerate LOV-DECISION in the P3 reference-data load with the route and approval codes of the FSD P7 and fix the code of a route move; until then the ledger stores the code the fact carries, validates it against the list in force, and the reference-data fake supplies the value the reference package uses |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6018-APP, RWB-S7-E6018-CON, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22834 | GAP-3049 | Register gap | Solution architect, business lead and the rwb-writeoff tech lead | RWB-S7-E6028-APP: no source publishes a sale-selection operation or a sold-population read, placement_type and the sale reference have no column, field ID or list, the entry state PLACEMENT_DECIDED is produced by an unclaimed rule, AC2's R-WO-12 is already built by RWB-S7-E6018-APP, the hand-off to rwb-debtsale has no edge, the debt sale officer holds right R only, and the plan's C row is empty while the step consumes three contracts | Declare the two operations on /api/recovery/writeoff/v1 with placeholder paths and element names confirmed by the solution architect; read placement_type and the sale reference as request inputs with placeholder value sets and no column; start the step at PLACEMENT_DECIDED and record that R-WO-29 is unclaimed in S7; assert R-WO-12 on the branch RWB-S7-E6018-APP builds instead of building it twice; describe the hand-off as the case move plus the published population read and declare no event; declare the selection at right C with the role conflict recorded; state the post-charge-off and sold states as edge placeholders; build against the three consumed rows as class C dependencies; trace to REQ-S7-006 from the FSD row. |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22838 | GAP-1313 | Register gap | Solution architect, P7 rwb-decision, with the S7 rwb-writeoff solution architect and the internal audit lead | One escalation leaves two decision entries, the routing record of rwb-decision and the write-off record of rwb-writeoff, and no source says so plainly | Keep both records and make the pair explicit: the write-off record names the state change and the rule that fired, the routing record names the level, the delegation row and the limit version the pack was routed at, neither repeats the other's facts, and the ledger read returns them in chain order so an auditor sees the pair as one step. State the reading in the ledger documentation of the service before the wave entry check. |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22840 | GAP-3050 | Register gap | Solution architect, business lead, rwb-writeoff tech lead and the rwb-debtsale owner | RWB-S7-E6028-CON: the two operations, their paths, operation IDs and element names, the placement_type and sale-reference placeholders, the consumed operation names, the decision code set, the role right of the sale and the paging of the population read have no published baseline, and the error set carries no message ID per condition | Publish one OpenAPI 3.1 document with the two operations, their placeholders and the error envelope of one message ID per condition; declare the three elements over DF-FIN-010 to DF-FIN-020 with the placement_type and sale-reference placeholders; declare the three consumed rows with placeholders for their operation names; declare the rights C and R and the role conflict as a carried assumption; declare the decision-record element with the chain to the approval record; publish five fakes and the drift, vocabulary and absence tests; declare no event and no Schedule; trace to REQ-S7-006 from the FSD row. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-ITG-E2032-ITG, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P7-E2032-APP, RWB-S2-E2032-APP | R-28842 | GAP-1531 | Register gap | Product owner | The boundary of the TDR suggestion message is not defined between rwb-agent and the treatment screen | The PRD requires that a caller learns that no suggestion is available and why, in the terms of the outcome the service recorded, and leaves the screen, the wording and the message ownership to the treatment PRD and the message standard. |
| RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28853 | GAP-1560 | Register gap | AI product owner | The queue write interface for models and agents has no approved consumer and no flag removal date | Name the first approved consumer and the flag removal date before the wave 2 release. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-28878 | GAP-1309 | Register gap | Compliance and PDPA officer with the solution architect and the platform observability team | The shape and route of the chain-check break report, and whether JOB-14 writes a ledger entry of its own, are not fixed | Agree the report fields, the alert route and the result retention with Compliance and the platform observability team, and state in the ledger run book whether the check is recorded as an operational event or as a decision record; until then ASM-B-P7-05-E2043-6 holds and the check writes no ledger row |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-28879 | GAP-1310 | Register gap | Solution architect with the Compliance and PDPA officer and the owners of the points of no return (S6, S7, S5, S4) | The strict-mode acknowledgement and the daily seal of the ledger hash are named by the architecture and no story of this key owns them | Raise the seal and the strict-mode acknowledgement as their own stories of the P7 epic with the Risk and Internal Audit sign-off that the ADR-009 change needs, and fix the seal manifest, its storage path and its schedule and the confirmation read together; until then ASM-B-P7-05-E2043-7 holds and this story builds only the ledger they consume |
| RWB-P7-E2042-APP | R-33456 | ASM-ALL-7434 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-P7-E2043-APP | R-37611 | ASM-2316 | Register assumption |  | The decision code of a reference-case step is read from the LOV-DECISION list in force and is never fixed by this story: the ledger stores the code the fact carries after validating it against the list, an unknown code is refused, and the reference-data fake supplies the route code the reference package uses, so no literal decision code appears in the story, the code, a test or a migration. | Center of excellence analyst with the business owner and the P3 reference-data administrator at the LOV-DECISION load of wave 1 |
| RWB-P7-E2043-APP | R-37614 | ASM-2319 | Register assumption |  | The chain-check outcome is read as follows: a complete run records the count, the last chain_seq, that entry's entry_hash, the start time and the end time in the service operational report and reports no break; a break is reported the same day to Compliance and RW-AUDIT as one notification naming the case, the chain_seq and the entry_hash of the entry before it, and the check writes no decision_log_entry row of its own, because a check is not a decision of a case. The completeness gap of a late fact is reported the same way, with the case, the key and the age. | Compliance and PDPA officer with the solution architect and the platform observability team at the ledger run book |
| RWB-P7-E2043-APP | R-37615 | ASM-2320 | Register assumption |  | The write-once daily seal of the ledger hash and the strict-mode acknowledgement before a point of no return are outside this story: the seal is read as a separate step of rwb-decision over this ledger with no story of RWB-E2-043, and strict mode is read as the points of no return of S4, S5, S6 and S7 reading a confirmation the ledger exposes, neither of which this story builds. The ADR-009 change Arch v5 slide 28 proposes needs Risk and Internal Audit sign-off, and that sign-off is an approval outside this run. | Solution architect with RW-RISK and Internal Audit at the ADR-009 and ADR-022 sign-off |
| RWB-P7-E6028-APP | R-37619 | ASM-2324 | Register assumption |  | One escalation is read as two ledger entries and not as one. rwb-writeoff writes the local record of R-WO-12 with the state change and publishes it on rwb.decision-record.v1, and rwb-decision writes the routing record of the approval it raises; both are collected into the central ledger, each names the same case and the same rule and neither repeats the other's facts, and the ledger read returns them in chain order so the pair reads as one step. The same reading applies to R-WO-32 and the sale selection. | P7 and S7 solution architects with the internal audit lead, at the ledger documentation review before the wave 4 entry check |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E2028-APP | R-06888 | DOR-RWB-P7-E2028-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or sources; sign-off cannot be confirmed without inventing a value. Placeholder row added. |
| RWB-P7-E2028-APP | R-06889 | DOR-RWB-P7-E2028-APP-16 | section header | Definition of Ready item 16 Size: Fail | The process phrase was removed because no source gives a size or a sizing rule. |
| RWB-P7-E2028-APP | R-06890 | DOR-RWB-P7-E2028-APP-21 |  | Definition of Ready item 21 Contract published: Fail | RWB-P7-E2028-CON is not in the item or story set, so no contract ID is named. |
| RWB-P7-E2028-APP | R-06891 | DOR-RWB-P7-E2028-APP-22 | header | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the story or sources; none invented. Placeholder row added. |
| RWB-P7-E2028-APP | R-26401 | CG-ALL-7344 | 3 | Flyway file V2028_1__decision_agent_verdict.sql is not in the V0001..Vnnnn form | Next free number of the service Flyway sequence is not in the sources. The V2028_1 name sits in story v1 lines 400 and 413, not in the supplied text. Solution architect to supply the number. |
| RWB-P7-E2032-APP | R-18173 | DOR-RWB-P7-E2032-APP-10 | 5-11 | Definition of Ready item 10 Screens and states: Partial | SCR-14 and SCR-38 screen-state text is in sections 5 to 11, outside this chunk; it cannot be edited unseen. Needs a chunk with those sections. |
| RWB-P7-E2032-APP | R-18174 | DOR-RWB-P7-E2032-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The detcheck P2 finding does not name the fields flagged as personal data, so the BR12 adjustment cannot be made from the sources. |
| RWB-P7-E2032-APP | R-26410 | CG-ALL-7374 | 3, 3.1 | Flyway file V2032_1__decision_offer_suggestion.sql is not in the V0001..Vnnnn form | Line 390 (V2032_1 name) is outside this chunk. Service Template v1 3.1 gives V0001 as baseline only; no next free number is stated in the sources. |
| RWB-P7-E2035-APP | R-06910 | DOR-RWB-P7-E2035-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design is in the story or the sources (searched for an epic design record; none found). Recording a sign-off would invent it. |
| RWB-P7-E2035-APP | R-06914 | DOR-RWB-P7-E2035-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version is in the story or the sources. Recording one would invent a version value. |
| RWB-P7-E2035-APP | R-11343 | CG-ALL-7379 |  | Rule R-RES-99 is not in Business Rules v4 | The R-RES-99 citation is not in this chunk, and no Business Rules v4 replacement rule ID is named, so no old text can be edited. |
| RWB-P7-E2035-APP | R-26417 | CG-ALL-7386 | 3, 3.1 | Flyway file V2_035_1__latest_state_change_index.sql is not in the V0001..Vnnnn form | The V2_035_1 filename at line 381 is outside this chunk. The next V-number of the rwb-decision Flyway sequence is not in the sources. |
| RWB-P7-E2035-APP | R-31541 | NEWAC-RWB-P7-E2035-APP-AC15 | 7, 16 | AC15: §8 BR4, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so AC15 cannot be placed. The proposed test is not specified in the source documents (NEWAC-RWB-P7-E2035-APP-AC15). |
| RWB-P7-E2036-APP | R-06921 | DOR-RWB-P7-E2036-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-P2-E2036-CON in 04 User stories (Epic 2 v8, P3/P4/P7 story files). Placeholder kept. Needs a value from the owner. |
| RWB-P7-E2036-APP | R-11348 | CG-ALL-7395 | 4, 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 has no 401 message ID. MSG-GEN-006 is system-unavailable, for store failure only. Placeholder kept. |
| RWB-P7-E2036-APP | R-26423 | CG-ALL-7398 | 16 | Test cases cover other criteria in Test Cases v8 | Rows 02 to 10 aligned to the v8 AC numbers in the evidence. Row 11 v8 mapping not in sources (Test Cases v8 is .xlsx only). Row 11 unchanged. |
| RWB-P7-E2036-APP | R-26425 | CG-ALL-7401 | 3, 3.1 | Flyway file V2036_1__decision_queue_placement.sql is not in the V0001..Vnnnn form | No V2036_1 name in any .md source, and the next free rwb-decision Vnnnn is not in the sources. Name left unchanged. |
| RWB-P7-E2041-APP | R-18191 | DOR-RWB-P7-E2041-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | The DL10 entry is in section 18, outside this chunk, and its current text was not supplied. Business decisions were removed, so it cannot be edited here. |
| RWB-P7-E2041-APP | R-26432 | CG-ALL-7417 | 3, 3.1 | Flyway file V2_041_1__change_report_indexes.sql is not in the V0001..Vnnnn form | The next rwb-decision Flyway number is not in the sources (Decision Log v11, Test Cases v8 checked). The migration name is in section 13, outside this chunk. No number was invented. |
| RWB-P7-E2042-APP | R-06938 | DOR-RWB-P7-E2042-APP-8 | 4 | Definition of Ready item 8 Contract: Fail | Step 10 already uses the Kafka Catalog v1 EV-30 field names. 401/404 IDs are CG-ALL-7421. The DecisionRecorded event type is in text not supplied in this chunk (CG-ALL-7424). |
| RWB-P7-E2042-APP | R-18196 | DOR-RWB-P7-E2042-APP-11 | not located in chunk | Definition of Ready item 11 Guardrails: Partial | The P2 fields classed as personal data are not named in the item or the story text in this chunk, so they cannot be identified without inventing them. |
| RWB-P7-E2042-APP | R-18198 | DOR-RWB-P7-E2042-APP-18 | 14 | Definition of Ready item 18 Open decisions: Partial | DL10 already cites ASM-2250, ASM-2357, ASM-2377 and ASM-2863 in section 14. No assumption ID for DL24 appears in the sources, and ASM numbers are assigned only at step D1. |
| RWB-P7-E2042-APP | R-18199 | DOR-RWB-P7-E2042-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Adding the BR1, BR10, BR13 and BR15 criteria and TC-E2-042-08 rows needs the current text of sections 7 and 16, which is not in this chunk. The repo search found no other copy of the story. |
| RWB-P7-E2042-APP | R-18201 | DOR-RWB-P7-E2042-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | The Error and Message Standard v4 wording was not found in the repo search, so MSG-P3-027 and MSG-P3-015 cannot be aligned. ASM-2310 and ASM-2312 still apply. |
| RWB-P7-E2042-APP | R-22626 | GAP-3180 | 13 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | AC3, step 6 and the section 1 and rows bullets are reordered to PARTIAL 2, WINDOW 3. BR4 row of section 13 is not in the diff and must be re-sent. |
| RWB-P7-E2042-APP | R-22697 | GAP-2406 | 3 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Reconciling 2026-12-15 with 2026-12-01 changes a valid-from date, which this edit may not do. It is a decision for the date owner (business analyst, P7). |
| RWB-P7-E2042-APP | R-26437 | CG-ALL-7430 | 3, 3.1 | Flyway file V2_042_1__epic2_rule_packages.sql is not in the V0001..Vnnnn form | The next V-number needs the rwb_decision baseline sequence, which is not in the sources. Repo search for the Flyway sequence found only other stories. Not specified in the source documents (CG-ALL-7430). |
| RWB-P7-E2042-APP | R-26438 | CG-ALL-7431 | 3, 3.1 | Flyway file V2_042_2__registry_constraints.sql is not in the V0001..Vnnnn form | The next V-number needs the rwb_decision baseline sequence, which is not in the sources. Story line 478 is blank in this chunk. Not specified in the source documents (CG-ALL-7431). |
| RWB-P7-E2042-APP | R-28846 | GAP-2400 | 7 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Route-set criterion text is not in the chunk, so no exact old text exists to edit. Re-send section 7 and its section 16 rows. |
| RWB-P7-E2042-APP | R-28852 | GAP-2410 |  | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Build-sequence section is not in the chunk, so the build-sequence line cannot be placed. Re-send the build-sequence section. |
| RWB-P7-E2042-APP | R-28856 | GAP-1302 |  | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Sections naming DF-REF-276, DF-REF-293 and the flag behaviour are not in the chunk. Re-send them to write the placeholders. |
| RWB-P7-E2042-APP | R-28865 | GAP-1298 |  | The decision code of a rule-governance entry is not named in any source this key may read | decision_log_entry section is not in the chunk, so the run-time LOV-DECISION lookup line cannot be placed. Re-send that section. |
| RWB-P7-E2042-APP | R-28867 | GAP-1300 | 14 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Section 14 MSG-P3-027 text is not in the chunk, so the {detail} wording cannot be copied. Re-send section 14. |
| RWB-P7-E2043-APP | R-06939 | DOR-RWB-P7-E2043-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or the sources; searched 'epic design' (story and sources, per prior notes). Sign-off cannot be stated without an invented value. |
| RWB-P7-E2043-APP | R-06943 | DOR-RWB-P7-E2043-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | No published fake library version for RWB-P3-E2043-CON is in the sources. Value needs the fake publication record; none invented. |
| RWB-P7-E2043-APP | R-18203 | DOR-RWB-P7-E2043-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 is outside this chunk. No P2 personal-data field list for this story is in the sources (Not specified in the source documents (DOR-RWB-P7-E2043-APP-11)). Classifying fields would invent a value. |
| RWB-P7-E2043-APP | R-26441 | CG-ALL-7446 | 16 | Test cases cover other criteria in Test Cases v8 | AC8 keeps its test case; v8 alignment is not verifiable from this chunk, so AC8 needs a ruling. |
| RWB-P7-E2043-APP | R-26443 | CG-ALL-7449 | 3, 3.1 | Flyway file V2043_1__decision_central_ledger.sql is not in the V0001..Vnnnn form | Next free number of the rwb_decision Flyway sequence is not in the sources (Not specified in the source documents (CG-ALL-7449)). The V2043_1 name sits in section 13, outside this chunk. |
| RWB-P7-E6028-APP | R-01898 | CG-ALL-7453 | 13 | Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9 | Index row still holds decision_log_entry.decided_at DESC; the field correction was not made in this pass. |
| RWB-P7-E6028-APP | R-26447 | CG-ALL-7467 | 3 | Flyway file V6028_1__approval_writeoff_sale.sql is not in the V0001..Vnnnn form | Next Flyway number for rwb-decision is not in the sources: E1001 gives only V0001; Template Spec 3.1 gives only V0001 to Vnnnn. Migration line not in this chunk. |

## 5. Cross-document changes (pending in the target document)


### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12625 | RWB-P7-E2028-APP | CG-ALL-7339 | 12.1 | Add a message ID for HTTP 401 no session, with a section 4 mapping; MSG-GEN-006 (system-unavailable) does not fit. |
| CDC-12626 | RWB-P7-E2028-APP | CG-ALL-7341 | 14 | Add a new message ID for the decision code, final call or version not being a value it must have; the story then cites it in sections 12.1 and 14 |
| CDC-12629 | RWB-P7-E2028-APP | DOR-RWB-P7-E2028-APP-9 | 14 | Add a new message ID for the MSG-P7-009 meaning; the story then cites it in section 14 |
| CDC-12650 | RWB-P7-E2029-APP | CG-ALL-7358 | 14 | Add a new message ID, distinct from MSG-P7-009, for 'A code, a final call or a required version is not a value it must have'; the story then cites it |
| CDC-12652 | RWB-P7-E2029-APP | DOR-RWB-P7-E2029-APP-9 | 14 | Add a new message ID, distinct from MSG-P7-009, for the value check, then cite it in section 14 |
| CDC-12669 | RWB-P7-E2032-APP | CG-ALL-7371 | 14 | Add a new message ID for the 422 decision code, final call or required version validation, with its text, to section 4; the story then cites it in 14 and 12.1 in place of MSG-P7-009 |
| CDC-12672 | RWB-P7-E2032-APP | DOR-RWB-P7-E2032-APP-9 | 14 | Same as CG-ALL-7371: the BA adds a new message ID for the 422 validation text to the standard; the story then cites it in 14 |
| CDC-12682 | RWB-P7-E2035-APP | CG-ALL-7380 | 4, 14 | Add a new message ID for the rule-row, package code and version-label refusal used in section 14; the business analyst assigns the ID. MSG-P3-027 keeps its load-failure text. |
| CDC-12684 | RWB-P7-E2035-APP | DOR-RWB-P7-E2035-APP-9 | 14 | MSG-P3-027 needs a new ID per CG-ALL-7380; the story text is left unchanged, and the {table} placeholder edit is reverted. |
| CDC-12710 | RWB-P7-E2036-APP | CG-ALL-7397 | 14 | Add a new message ID for the decision code, final call and model or agent version validation. The story then cites that ID in section 14 in place of MSG-P7-009. |
| CDC-12712 | RWB-P7-E2036-APP | DOR-RWB-P7-E2036-APP-9 | 14 | Add a new message ID for the decision code, final call and model or agent version validation; the story then cites it in section 14. |
| CDC-12745 | RWB-P7-E2042-APP | CG-ALL-7421 | 4, 12.1 | Add a message ID for 401 no session and one for 404 an unknown package code or version; neither exists in §4 today. Story 12.1 keeps the Not specified placeholders. |
| CDC-12746 | RWB-P7-E2042-APP | CG-ALL-7426 | 4, 14 | Add a new message ID for a rollback called on a version with no earlier version, with its text; the story then cites that ID in place of MSG-P3-015. |
| CDC-12780 | RWB-P7-E2043-APP | CG-ALL-7443 | 14 | Add a new message ID for a fact with a rule ID and no version, a decision code outside the list in force, or a field outside the schema. |
| CDC-12781 | RWB-P7-E2043-APP | CG-ALL-7444 | 14 | Add a new message ID for a query value outside its list or a size above 200. |
| CDC-12782 | RWB-P7-E2043-APP | CG-ALL-7445 | 14 | Add a new message ID for ledger, reference list or parameters unavailable, or a completeness gap or chain break reported. |
| CDC-12805 | RWB-P7-E6028-APP | CG-ALL-7463 | 4, 14 | Add a new message ID for a decision code, capability area, status or level not in its list. Keep MSG-P7-009 for the decision-log refusal. Story cites it once it exists. |
| CDC-12806 | RWB-P7-E6028-APP | CG-ALL-7464 | 4, 14 | Add a new message ID for no delegation row covering the decision. Keep MSG-P7-010 for the no-delegation-limit meaning. Story cites it once it exists. |
| CDC-12810 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-9 | 14 | State the standard's meaning of MSG-P7-009 and MSG-P7-010, then align this story's use to it. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12635 | RWB-P7-E2028-APP | CG-ALL-7343 | 18 | Align the test lists of REQ-DRI-001 and the second requirement with section 18 in the next RTM version. |
| CDC-12662 | RWB-P7-E2029-APP | CG-ALL-7361 | 18 | Align the test case lists of REQ-DVH-001 and REQ-DVH-006 to RWB-P7-E2029-APP section 18 in its next version. |
| CDC-12670 | RWB-P7-E2032-APP | DOR-RWB-P7-E2032-APP-12 | 12.7, 16, 18 | Test cases added for BR6, BR9, BR12 and BR13; §18 list left as is. |
| CDC-12681 | RWB-P7-E2032-APP | CG-ALL-7372 | 18 | Align the test lists for REQ-DRI-001 and the second differing requirement in §18 of this story and in the RTM at their next versions. |
| CDC-12695 | RWB-P7-E2035-APP | CG-ALL-7384 | 18 | Align the test lists of REQ-WKM-012, -013, -016 and the other requirements in the item with RWB-P7-E2035-APP section 18 |
| CDC-12705 | RWB-P7-E2036-APP | DOR-RWB-P7-E2036-APP-12 | 16 | Align the test case lists per requirement with section 18 of this story, which now includes TC-E2-036-15, -16 and -17. |
| CDC-12717 | RWB-P7-E2036-APP | CG-ALL-7400 | 18 | Align the test case lists of REQ-CWC-017 to REQ-CWC-020 and REQ-ACA-010 with section 18 of RWB-P7-E2036-APP |
| CDC-12738 | RWB-P7-E2041-APP | CG-ALL-7415 | 18 | Align the REQ-CWC-013 and the second mismatched requirement test lists with section 18 in the RTM's next version. |
| CDC-12765 | RWB-P7-E2042-APP | CG-ALL-7428 | 18 | In its next version, align the trace lists of REQ-CWC-013 and the other differing requirement to the tests of section 18 of this story, keeping the other stories' tests in place. |
| CDC-12791 | RWB-P7-E2043-APP | CG-ALL-7447 | 18 | Align the test lists of the four requirements with section 18 of this story in the next RTM version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12667 | RWB-P7-E2032-APP | DOR-RWB-P7-E2032-APP-7 | 11 | The P1 index note on decision_log_entry.decided_at is not in the story; the LDM v9 owner must check it. |
| CDC-12709 | RWB-P7-E2036-APP | CG-ALL-7393 | 4 | Record the rwb-case object decision_record (its local decision-record table) in LDM v9 Fields. The story keeps the name as it is owned by rwb-case. |
| CDC-12748 | RWB-P7-E2042-APP | DOR-RWB-P7-E2042-APP-7 | 11 | Confirm the fields of decision_log_entry; DF-DEC-001 to DF-DEC-031 are not all of them. |
| CDC-12770 | RWB-P7-E2043-APP | CG-ALL-7435 | 13 | Add field source_service to entity decision_log_entry (type Not specified in the source documents (CG-ALL-7435)); the story index needs it. |
| CDC-12771 | RWB-P7-E2043-APP | CG-ALL-7436 | 13 | Add field source_entry_ref to entity decision_log_entry (type Not specified in the source documents (CG-ALL-7436)); the story index needs it. |
| CDC-12775 | RWB-P7-E2043-APP | DOR-RWB-P7-E2043-APP-7 | 11 | Section 4 rows restored to their original labels (assumed columns), (inbox), (outbox) |
| CDC-12777 | RWB-P7-E2043-APP | CG-ALL-7437 | 2, 8, 13, 17 | Record the trigger tr_declog_append_only on decision_log_entry as a database object of the owning document. |
| CDC-12778 | RWB-P7-E2043-APP | CG-ALL-7438 | 13 | Add decision_log_entry.ingest_at (collection time of the fact) to the Fields sheet, or name the dictionary column that carries it. |
| CDC-12803 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-7 | 11 | Confirm decided_at (DF-DEC-016) is a field of decision_log_entry, or name the LDM field for the DESC index. Section 11 has no index column. P2 fixed in story via CG-ALL-7454. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12622 | RWB-P7-E2028-APP | CG-ALL-7337 | 12.2 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} through the provider's CON story. |
| CDC-12639 | RWB-P7-E2029-APP | CG-ALL-7349 | 12.2 | Publish GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationRunId} through RWB-P10-E2029-CON, or the consumer switches to a published operation. |
| CDC-12640 | RWB-P7-E2029-APP | CG-ALL-7350 | 12.2 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} through RWB-P10-E2029-CON, or the consumer switches to a published operation. |
| CDC-12664 | RWB-P7-E2032-APP | CG-ALL-7367 | 12.2 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} through RWB-P10-E2032-CON. |
| CDC-20780 | RWB-P7-E2028-APP | R-01869 |  | GET /agent-runs/{runId} is already in the staged next version (docpass X002-F1, operations 12). No further change. |
| CDC-20781 | RWB-P7-E2029-APP | R-01874 |  | GET /agent-runs/{runId} is already in the staged next version (docpass X002-F1). Same change as R-01869; no further change. |
| CDC-20782 | RWB-P7-E2032-APP | R-01882 |  | GET /agent-runs/{runId} is already in the staged next version (docpass X002-F1). Same change as R-01869; no further change. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12623 | RWB-P7-E2028-APP | CG-ALL-7338 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-12644 | RWB-P7-E2029-APP | CG-ALL-7354 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation. |
| CDC-12665 | RWB-P7-E2032-APP | CG-ALL-7368 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-12704 | RWB-P7-E2036-APP | CG-ALL-7394 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the rwb-access contract story. |
| CDC-12719 | RWB-P7-E2041-APP | CG-ALL-7408 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the RWB-P4-E1037-CON provider story |
| CDC-12796 | RWB-P7-E6028-APP | CG-ALL-7456 | 12.2 | Publish GET /api/recovery/access/v1/doa-limits in rwb-access.yaml through the P4 provider CON story. |
| CDC-12797 | RWB-P7-E6028-APP | CG-ALL-7457 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the P4 provider CON story. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12655 | RWB-P7-E2029-APP | GAP-1819 | 11 | Add S8 rows for the screening run, score row per code, contact stop, agent feedback row and breach record, with their key fields as product requirements. |
| CDC-12686 | RWB-P7-E2035-APP | GAP-0667 | 4 | Correct the GET /cases/{caseId}/next-action row so P2 owns the read and P3 owns the write; apply the contract, login, message and rule-value fixes listed in the item. |
| CDC-12733 | RWB-P7-E2041-APP | GAP-0718 | find it | Publish GET /api/recovery/case/v1/admin/rule-change-audit with the section 11 entry fields and Rules and parameters R, and add its row to the ownership map before the wave 2 contract baseline. |
| CDC-12739 | RWB-P7-E2041-APP | GAP-0203 | find it | Add a payment_match_rule row: owning service P7, target schema rwb_decision, no target table; keep all 13 fields; the ownership basis records retirement by D-RCV-36 T10 and the PAYMENT_MATCH rule package. |
| CDC-12751 | RWB-P7-E2042-APP | GAP-2395 | find it | Name which Epic 2 rule package and version label the rwb-comms notice reads, settled with the rule registry owner before integration; no fourth package code. |
| CDC-12758 | RWB-P7-E2042-APP | GAP-0667 | 4 | Record that GET /cases/{caseId}/next-action is served by rwb-integration under /api/recovery/integration/v1; P2 owns the read and P3 owns the write. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12645 | RWB-P7-E2029-APP | DOR-RWB-P7-E2029-APP-14 | Not specified in the source documents (DOR-RWB-P7-E2029-APP-14) | Record the signed epic design sign-off for RWB-P7-E2029-APP in the epic design record, since no signed design is in the story or source documents. |
| CDC-12666 | RWB-P7-E2032-APP | DOR-RWB-P7-E2032-APP-14 | none | Record the signed epic design sign-off for RWB-P7-E2032-APP. |
| CDC-12706 | RWB-P7-E2036-APP | DOR-RWB-P7-E2036-APP-14 | Metadata | Record the signed epic design sign-off for RWB-SVC-P7 in the epic design record. |
| CDC-12722 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-14 | n/a | Confirm and record the signed epic design sign-off, then cite it in the story |
| CDC-12798 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-14 | header | Record the signed epic design sign-off for EP06; the header now carries the open sign-off line. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12720 | RWB-P7-E2041-APP | CG-ALL-7410 | 13 | Create story RWB-P7-E1073-CON, or name the existing story of the same capability in its place in section 13 and the DP-04 row |
| CDC-12723 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-17 | 13 | Create RWB-P7-E1073-CON, or rename the dependency to the existing story of the same capability |
| CDC-12724 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-21 | n/a | Create RWB-P7-E2041-CON and name it as a contract dependency if this story publishes a contract; otherwise record that none is published |
| CDC-12772 | RWB-P7-E2043-APP | CG-ALL-7440 | 13 | Create story RWB-P7-E1073-CON, or name the existing story carrying the embedded Drools kit capability so the story's C dependency points to it. |
| CDC-12773 | RWB-P7-E2043-APP | DOR-RWB-P7-E2043-APP-17 | 13 | Create RWB-P7-E1073-CON or name the existing story; the story's dependency in section 13 then follows that key. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12621 | RWB-P7-E2028-APP | CG-ALL-7336 | 12.1 | Publish POST /api/recovery/decision/v1/decision-log (the append of section 12.1) through the rwb-decision CON story. |
| CDC-12638 | RWB-P7-E2029-APP | CG-ALL-7348 | 12.1 | Publish POST /api/recovery/decision/v1/decision-log in rwb-decision.yaml through the owner's CON story, or remove the operation. |
| CDC-12663 | RWB-P7-E2032-APP | CG-ALL-7366 | 12.1 | Publish POST /api/recovery/decision/v1/decision-log in paths through the CON story for rwb-decision. |
| CDC-12795 | RWB-P7-E6028-APP | CG-ALL-7455 | 12.1 | Publish POST /api/recovery/decision/v1/approvals (raise) in rwb-decision.yaml through the CON story. |

### RWB-P10-E2032-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12674 | RWB-P7-E2032-APP | GAP-0634 | 12 | Fix the operation under /api/recovery/agent/v1 with three request members and eight answer members; declare the EV-28 payload, boundary request, error mapping and admin reads as the item's proposed fix states. |
| CDC-12675 | RWB-P7-E2032-APP | GAP-0633 | 12 | Place the suggestion operation under /api/recovery/agent/v1, read account, payments and treatment through the named source contracts, treat the suggestion call as the DP-11 exception with the 60-second timeout, and compose SCR-14 through gateway-bff. |
| CDC-12676 | RWB-P7-E2032-APP | GAP-0414 | 12 | rwb-treatment and rwb-agent owners agree one one-hop REST operation that starts a TDR suggestion run; QA lead fixes harness environment, stub controls, evidence format and gate. |
| CDC-12678 | RWB-P7-E2032-APP | GAP-1882 | 12 | Fix the caller-side operation, request members and proposal columns at the wave 2 contract review; record override and fallback decision codes with rwb-decision before Done. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12683 | RWB-P7-E2035-APP | CG-ALL-7382 | 16 | Add rows for TC-E2-035-14 on tab Story test cases, with Given, When and Then copied from AC5. |
| CDC-12721 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-12 | 12.7, 16, 18 | Story lists TC-12 and TC-13; workbook rows are not yet added |
| CDC-12807 | RWB-P7-E6028-APP | CG-ALL-7465 | 16 | Add rows TC-E6-028-01 to TC-E6-028-06 with Given, When and Then copied from the criteria each row covers in section 16. |
| CDC-12809 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-12 | 12.7, 16 | Story side done: TC-E6-028-07 gives the boundary test on the approval and decision_log_entry tables. |

### RWB-P3-E2043-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12783 | RWB-P7-E2043-APP | GAP-2016 | 12.7 | Make the durable timer authoritative, with the timer row as its audit copy written by ApplyStateActivity in the same transaction as the state and read back on a reopen. |
| CDC-12784 | RWB-P7-E2043-APP | GAP-2024 | 13 | Parent forwards DeviationRaised to the running stage child, which pauses and resumes its own stage timer on DeviationCleared. Rule for a child started while a deviation is open: Not specified in the source documents (GAP-2024). |
| CDC-12789 | RWB-P7-E2043-APP | GAP-2019 | 3 | Parent starts each child with the case ID, retries the start with the same workflow ID, and raises an incident with MSG-P3-037 when retries are exhausted, leaving the case in its last applied state. |
| CDC-12790 | RWB-P7-E2043-APP | GAP-2018 | 3 | A pivot activity waits on the ledger acknowledgement with the retry policy of section 7 and a documented timeout, and fails with an incident at timeout without repeating a completed step. |

### RWB-P10-E2029-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12657 | RWB-P7-E2029-APP | GAP-0625 | 12 | Name the rwb-agent login, publish the S8 raise operation and path with its C row, name the floor, segment and promotion parameter keys, and name the route with the edge owner. |
| CDC-12659 | RWB-P7-E2029-APP | GAP-2194 | 12 | Publish the raise and entry-read shapes, register the AgentRunCompleted.v1 payload, fix the gateway-bff route and confirm the five score-row members. |
| CDC-12660 | RWB-P7-E2029-APP | GAP-2402 | 12 | Publish the decision-log append path and answer, the evaluation and run read field sets, the case-less approval columns, the LOV-DECISION promotion code, the MSG-P7-009 text, EV-30, the DP-02 login and the nine dependency rows. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12685 | RWB-P7-E2035-APP | GAP-3177 | 16 | Register the five-minute next-action Schedule in rwb-case; delete EV-18 from the Epic 2 contract tables of RWB-P2-E2035-CON. Story TC-E2-035-11 JOB-05 reference removed. |
| CDC-12776 | RWB-P7-E2043-APP | DOR-RWB-P7-E2043-APP-8 | 4, 12.1, 12.5 | Add ChainCheckActivity to the Activities sheet with task queue rwb-decision, owned by rwb-decision. |
| CDC-12779 | RWB-P7-E2043-APP | CG-ALL-7442 | 12.5 | Add the activity ChainCheckActivity to the Activities sheet with task queue rwb-decision. |

### RWB-P10-E2028-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12631 | RWB-P7-E2028-APP | GAP-2191 | 12.1 | Fix the two rwb-agent operations on /api/recovery/agent/v1 with legacy members and refusals; declare event rwb.agent.AgentFeedbackRecorded.v1 with retry and .dlt topics; one gateway-bff route of one hop and 2 s. |
| CDC-12633 | RWB-P7-E2028-APP | GAP-0623 | 12.1 | Record event rwb.decision.DecisionRecorded.v1 is set in Done when |

### OTHER:Case intake agent L1 deployment story in rwb-agent (not this story) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12636 | RWB-P7-E2028-APP | GAP-0624 | none | Supply the deployment values named in GAP-0624: secret-referenced login, Flyway order, topic partitions, replication, retention, retry and .dlt names, relay interval, alert window and thresholds, worker and probe values, route path. |
| CDC-12637 | RWB-P7-E2028-APP | GAP-2192 | none | Supply the deployment values named in GAP-2192: secret-referenced login, gateway-bff route path and name, topic partitions, retention, retry and .dlt names, consumer groups, alert window and thresholds, worker and probe values. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12641 | RWB-P7-E2029-APP | CG-ALL-7351 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{parameterCode} in rwb-case.yaml through the provider's CON story, or consume a published operation. |
| CDC-12642 | RWB-P7-E2029-APP | CG-ALL-7352 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{listCode} in rwb-case.yaml through the provider's CON story, or consume a published operation. |

### RWB-P7-E2029-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12646 | RWB-P7-E2029-APP | DOR-RWB-P7-E2029-APP-21 | header | The contract story key is not in the story set, so the header lists only RWB-P10-E2029-CON. The contract publication stays open. |
| CDC-12658 | RWB-P7-E2029-APP | GAP-0626 | 12 | Publish the raise operation and decision-entry read with members, path, answer and refusal codes; name the parameter keys, the login and the route. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12649 | RWB-P7-E2029-APP | CG-ALL-7357 | 12.3 | Payload cell set to Not specified in the source documents (CG-ALL-7357) |
| CDC-12715 | RWB-P7-E2036-APP | GAP-3102 | 12 | Publish the hold element (case reference, deviation reference, code, open count, handler, return point, contact-stop flag, rule version) additively in rwb.deviation.events.v1 and have the rwb-case owner declare the event-driven set and clear of recovery_case.deviation_open. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12679 | RWB-P7-E2032-APP | GAP-1883 | 13 | Add the suggestion operation of RWB-P10-E2032-CON to the rwb-agent inbound list and take the amendment to the architecture review before wave 2 closes. |
| CDC-12761 | RWB-P7-E2042-APP | GAP-2396 | 7 | Correct the P6 Comms to P7 Decision cell so the RulePackageInForce event route matches the consumer in RWB-P6-E1073-APP. |

### RWB-P2-E2035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12698 | RWB-P7-E2035-APP | GAP-2409 |  | Mark packageVersion required on GET /api/recovery/decision/v1/rule-catalog/{ruleId}; keep the MSG-GEN-001 refusal for an absent value |
| CDC-12759 | RWB-P7-E2042-APP | GAP-0668 | 12 | Baseline the three operation names, nine consumed shapes, split note, workflow and Schedule contract and error mapping; confirm the five message texts. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12714 | RWB-P7-E2036-APP | GAP-0957 | 12 | Carry the request and answer element set of POST /authorise and the non-human part of GET /me/permissions in the service contract document, with the caller type as a carried value of the approved callers list; reconfirm with the rwb-integration owner at contract review. |
| CDC-12749 | RWB-P7-E2042-APP | GAP-0966 | find it | Add rule-package action names, request and answer fields and a change decision code to POST /authorise, and stub them in the contract fake. |

### RWB-P3-E2041-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12726 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-23 | n/a | Record the contract version it publishes, so this story can name the version it builds against |
| CDC-12737 | RWB-P7-E2041-APP | GAP-2413 | find it | Agree at wave 2 contract review: ChangeReportPage and RulePackageChangeEntry shapes, rulesChanged element, CSV column order, decision and item-list codes, count read, flag-off answers, rwb-decision login name. |

### RWB-P7-E1073-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12740 | RWB-P7-E2041-APP | GAP-0720 | find it | Audit read and its CSV export follow decision-record retention; deprecation window for a published field and contract fakes retention: Not specified in the source documents (GAP-0720). |
| CDC-12762 | RWB-P7-E2042-APP | GAP-0722 | 12.1 | Publish GET /rule-models/{packageCode}/{version} and GET /rule-catalog/{ruleId}?packageVersion= with packageCode, versionLabel, checksum (SHA-256), model content, compiler version, valid-from date, ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code and outputs. Property types, lengths and required flags stay open for the rwb-decision owner. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P7 rwb-decision (Decision and rules)/ (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12741 | RWB-P7-E2042-APP | CG-ALL-7422 | 13 | Create story RWB-P7-E1073-CON as the P7 rule-package contract (model read GET /rule-models/{packageCode}/{version}; catalog read GET /rule-catalog/{ruleId}?packageVersion=), or name the existing story that holds them. |
| CDC-12743 | RWB-P7-E2042-APP | DOR-RWB-P7-E2042-APP-17 | header | Create story RWB-P7-E1073-CON as the P7 rule-package contract, or name the existing story that holds the model and catalog reads. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12754 | RWB-P7-E2042-APP | GAP-2485 | find it | Record that rwb-decision evaluates BOOKING_MATCH on the version it holds through the embedded kit, and restate the boundary in section 19 once. |
| CDC-12794 | RWB-P7-E2043-APP | GAP-2053 |  | Record the outbox and inbox rule as target scope for all 19 services per Arch v5, with Epic 1 and Epic 2 sentences kept as as-built, under R-PREC (Arch v5 first). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; OTHER:rwb-agent and rwb-access published APIs (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12624 | RWB-P7-E2028-APP | DOR-RWB-P7-E2028-APP-8 | 12.1 | Publish POST /decision-log in rwb-decision.yaml; publish GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent; publish POST /api/recovery/access/v1/authorise in rwb-access |

### OTHER:Screen specification of SCR-03 and SCR-38 (owner not named in the story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12627 | RWB-P7-E2028-APP | DOR-RWB-P7-E2028-APP-10 | find it | Add empty, loading, error and no access states for SCR-03 and SCR-38 |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12628 | RWB-P7-E2028-APP | DOR-RWB-P7-E2028-APP-12 | 16 | Align the P3 test case coverage to Test Cases v8 and the P3 section 18 test lists to RTM v7 |

### OTHER:Solution architect register; RWB-P10-E2028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12630 | RWB-P7-E2028-APP | GAP-2190 | find it | Resolve the rwb-agent values (login, freshness read, acceptance event, lists, route, flag, topic, policy) in the rwb-agent slice |

### RWB-ITG-E2028-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12632 | RWB-P7-E2028-APP | GAP-0410 | 16 | Agree the Enterprise AI test tenant and guardrail profile with the P10 owner and platform team; agree harness pack, seeding and evidence format with QA. |

### RWB-P7-E2028-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12634 | RWB-P7-E2028-APP | GAP-1294 | 12.1 | Agree at wave 2 review: append on POST /api/recovery/decision/v1/decision-log, two read shapes, LOV-DECISION D6 with verdict list, reason-code list, MSG-P7-009 text and rwb-decision login name. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12643 | RWB-P7-E2029-APP | CG-ALL-7353 | 12.2 | Publish the consumed GET /api/recovery/source-data/v1/... operation through the provider's CON story; the exact path is Not specified in the source documents (CG-ALL-7353). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; OTHER:rwb-agent API yaml; OTHER:rwb-case API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12647 | RWB-P7-E2029-APP | DOR-RWB-P7-E2029-APP-8 | 12.1 | Publish POST /decision-log in rwb-decision.yaml; publish GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationRunId} and GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent; publish GET /api/recovery/case/v1/parameters/{parameterCode} in rwb-case; publish the six further paths the detcheck lists |

### OTHER:RWB-S8 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12648 | RWB-P7-E2029-APP | GAP-1818 | 12.1 | Deviation REST paths and the case-record read belong to the S8 contract story, not this story. |

### OTHER:P3 screen specification for SCR-03 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12651 | RWB-P7-E2029-APP | DOR-RWB-P7-E2029-APP-10 | n/a | Add empty, loading, error and no-access states to SCR-03 |

### OTHER:FSD S8 A2.2.4 to A2.9.4 criteria, with the story groomer and owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12653 | RWB-P7-E2029-APP | GAP-1823 | n/a | Rewrite each 'Timers shown' criterion; carry the row as evidence and add the pause, stop, routing and clear step criteria in the owning story |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12654 | RWB-P7-E2029-APP | GAP-1826 | n/a | Name R-DEV-04, 10, 11, 13, 14, 16, 19, 20, 21 and 22 as the requirement set with their design rule IDs; package authoring stays in the rwb-decision rule registry |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:EV-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12656 | RWB-P7-E2029-APP | GAP-1832 | 12 | Carry case key, code, state, contact stop flag, return point and decision record reference in the envelope; no personal or financial value. |

### RWB-P10-E2029-CON; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12661 | RWB-P7-E2029-APP | GAP-3100 | 12 | Publish the raise request with the return point, agent version and policy segment fields; name the agent-policy read; add the partial unique index for one open code per case; publish the decision-record envelope type; assign a level to each legacy case. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; OTHER:rwb-agent API yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12668 | RWB-P7-E2032-APP | DOR-RWB-P7-E2032-APP-8 | 12.1 | Publish POST /decision-log in rwb-decision.yaml; GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent; POST /api/recovery/access/v1/authorise in rwb-access. |

### OTHER:Decision DL10 owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12671 | RWB-P7-E2032-APP | DOR-RWB-P7-E2032-APP-18 | 14 | Assumptions linked to DL10; DL10 stays open |

### RWB-P7-E2032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12673 | RWB-P7-E2032-APP | GAP-1713 | 1 | Map each feature-code prerequisite to the contract of its owning service (approval to P7, case to P3, documents to P5, communications to P6, valuation to S1) and carry the duplicate FEAT-CHO-08 as written. |

### OTHER:Environment records of the ACE platform (SCB IT infrastructure) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12677 | RWB-P7-E2032-APP | GAP-0635 | 13 | Provision the INT-23 private path, login and Key Vault entries, topic rwb.agent.events.v1 with retry and .dlt topics, queue, identities, budgets, alarms and sizing; record each value per environment. |

### RWB-P10-E2032-CON; RWB-P7-E2032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12680 | RWB-P7-E2032-APP | GAP-2403 | 12 | Agree the append and read shapes, LOV-DECISION and final-call value sets, the reference-data path, the text of MSG-P7-009 and the rwb-decision login name at the wave 2 contract review. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P2-E2035-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12687 | RWB-P7-E2035-APP | GAP-0668 | 12 | Baseline the rwb-integration next-action contract (three operation names, nine consumed shapes, Schedule and error mapping) and record the read path ruling in the Ownership Map. |

### RWB-P2-E2035-OPS; OTHER:job catalogue; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12688 | RWB-P7-E2035-APP | GAP-0669 | 13 | Fix the rwb-integration login, secret reference and probes in RWB-P2-E2035-OPS; create the next-action-check job catalogue row with its run book path; record the read path ruling in the Ownership Map. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12689 | RWB-P7-E2035-APP | GAP-2406 | 16 | Set the valid-from date of RES-2026.12 in the registry stories to 2026-12-01, matching the ITG harness and RWB-P3-E2035-APP. |

### RWB-P3-E2042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12690 | RWB-P7-E2035-APP | GAP-2405 | 4 | Add the row and latest-state-change answer schemas to the API specification and RWB-P3-E2042-CON; add 404 and 422 entries for MSG-P3-027 and MSG-GEN-001 to the message catalogue. |

### OTHER:TSD P4 T6.1; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12691 | RWB-P7-E2035-APP | GAP-2324 | 4 | Add a Case record column for every role to T6.1, publish the 14-area matrix as data via RWB-P4-AD002-APP, and fix specialist default scopes with the security administrator. |

### API:(service not named); OTHER:TSD P4 appendix T-A; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12692 | RWB-P7-E2035-APP | GAP-2322 | 4 | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema; fix the authorise request and answer of a next-action read; fix the rwb-access login; add the unknown-role message. |

### OTHER:Platform edge story (gateway-bff); OTHER:wave 2 integration harness plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12693 | RWB-P7-E2035-APP | GAP-0418 | 13 | Agree the gateway-bff next-action route path, merge order and call list, and the harness repository, SIT environment, seeding, evidence format, retention and pass/fail gate with QA at wave 2 entry. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:FSD P4 A2.3 and A2.4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12694 | RWB-P7-E2035-APP | GAP-2323 | 4 | Add CUSTOMER_PARTY as a fourth value of LOV-ROLE-CLASS in the role load and let customer-party roles carry it; confirm with the role catalogue owner before the wave 2 policy pack. |

### OTHER:Plan of record for RWB-E2-033 to RWB-E2-036 (assembly step) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12696 | RWB-P7-E2035-APP | GAP-3187 |  | Keep rwb-integration as primary P2 for the four keys and record the P3 tension at assembly; no story change |

### OTHER:rwb-comms notice story (key not in sources) and RWB-E2-035 rwb-case story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12697 | RWB-P7-E2035-APP | GAP-2400 |  | Keep case route-set behaviour in RWB-E2-035; in rwb-comms read the route-set fields only for notices decided by a route-set rule, tested with R-RES-04 values |

### OTHER:TSD P4 T3.1 role rows and the parameters contract (DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12699 | RWB-P7-E2035-APP | GAP-2325 | 8 | Version role rows by the matrix version they load with, or add a role_version label; make the cache lifetime a DP-06 parameter whose value is agreed at wave 2 design review. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12700 | RWB-P7-E2035-APP | GAP-2407 | 8 | Publish LOV-DECISION with the state-change codes marked; the latestStateChange filter reads that mark. |

### OTHER:TSD P7 rwb-case reference data (timer spec list of values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12701 | RWB-P7-E2035-APP | GAP-2408 | 8 | BR3 states that no list of values for the timer spec is named in any source; the registry returns the string as stored. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12702 | RWB-P7-E2035-APP | GAP-2411 | 8 | Fix the rwb-decision login name in RWB-PLT-DB and the secret store, with the migration role and the application role kept apart. |

### OTHER:Build sequence (Delivery lead workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12703 | RWB-P7-E2035-APP | GAP-2410 | 5 | Record that the secondary slice builds against the platform contracts and published fakes and reads the wave-1 rows of RWB-P7-E1073-APP and RWB-P7-E1008-APP through its own schema, within R5.7 rule 5. |

### RWB-P2-E2036-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12707 | RWB-P7-E2036-APP | DOR-RWB-P7-E2036-APP-22 | 12.2 | Record the published fake library version for the contract the story faked against. |

### API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12708 | RWB-P7-E2036-APP | DOR-RWB-P7-E2036-APP-8 | 4, 12.1 | Publish POST /api/recovery/access/v1/authorise in the rwb-access API yaml |

### OTHER:Screen specification of the story that owns SCR-02; OTHER:SCR-07 and SCR-38 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12711 | RWB-P7-E2036-APP | DOR-RWB-P7-E2036-APP-10 | 13, 15 | State rows for SCR-02, SCR-07 and SCR-38 added in section 15 from the screen specification, with gaps marked Not specified. |

### RWB-P2-E2036-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12713 | RWB-P7-E2036-APP | GAP-0670 | 4, 12, 13 | Reconcile per the proposed fix: rwb-case keeps POST /api/recovery/case/v1/queues/{queueId}/placements; rwb-integration serves POST /api/recovery/integration/v1/queues/{queueId}/placements and forwards to P3; approved callers under key rwb.casewf.placement.approved-callers. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12716 | RWB-P7-E2036-APP | GAP-2412 | 12 | Publish the placement fact element names on rwb.decision-record.v1 and the decision-record library signature; publish the P3 case-read, P4 authorise and reference-data shapes at wave 2 entry; add the MSG-P7-009 text to the message standard; fix the login name in the platform DB story. |

### OTHER:Recovery Workbench delivery plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12718 | RWB-P7-E2036-APP | GAP-3187 |  | Keep rwb-integration as primary for RWB-E2-033 to RWB-E2-036 and record the P2 and P3 tension for the assembly step |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12725 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-22 | n/a | Publish the fake library for each consumed contract and record its version |

### RWB-P3-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12727 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-10 |  | Add empty, loading, error and no-access states to SCR-39 |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12728 | RWB-P7-E2041-APP | DOR-RWB-P7-E2041-APP-11 | 12.1 | Classify the author and approver staff IDs carried by RulePackageChangeEntry as personal data, or confirm they are not personal data. |

### OTHER:Technical Specification P7 rwb-decision; OTHER:Technical Specification P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12729 | RWB-P7-E2041-APP | GAP-1615 | find it | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule operations; remove those tables and operations from TSD P3 and P4; correct x-module of the nine rule paths to P7. |

### OTHER:Technical Specification P3 v3 and Technical Specification P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12730 | RWB-P7-E2041-APP | GAP-1993 | find it | Remove rule_package, rule_package_version, rule_row and rule_test_case ownership; the registry is built in rwb-decision and read through the P7 contract (DP-04). |

### OTHER:Technical Specification P4 v3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12731 | RWB-P7-E2041-APP | GAP-1565 | find it | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 to rwb-decision; set x-module of the six paths to P7. |

### OTHER:Recovery Workbench Gap Register v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12732 | RWB-P7-E2041-APP | GAP-0420 |  | GAP-0420 resolved: integration lead agrees SIT environment, seeding, evidence format, retention, gate with QA and composite route detail at wave 2 entry check; values held in harness pack |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx; OTHER:TSD P4 v3 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12734 | RWB-P7-E2041-APP | GAP-0962 | 16 | Publish one RULES_AND_PARAMETERS row set. Matrix row RW-CASEOWN gives R, so the 'no right to RW-CASEOWN' mock in the Background conflicts; RW-REFADM is R only |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12735 | RWB-P7-E2041-APP | GAP-0964 | find it | Add GET /api/recovery/access/v1/rule-authority and POST /api/recovery/access/v1/rule-report-exports as P4 operations with their query, body and answer fields; freeze action set and refusal reasons at the RWB-P3-E2041-CON review. |

### OTHER:TSD P4 v3 (T6.1 permission data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12736 | RWB-P7-E2041-APP | GAP-0965 | find it | Add rows for the rwb-decision service identity and the gateway-bff route with the R letter in RULES_AND_PARAMETERS only; security administrator confirms before the authorise contract is frozen. |

### RWB-P7-E2042-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12742 | RWB-P7-E2042-APP | DOR-RWB-P7-E2042-APP-14 | header | Record the signed epic design sign-off; the story cannot assert it from the sources. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P3 rwb-case (Case and workflow)/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12744 | RWB-P7-E2042-APP | DOR-RWB-P7-E2042-APP-21 | header | Record the published status of contract RWB-P3-E2042-CON; no file of that key is in the story folder (only RWB P3 E2042 INF exists). |

### RWB-P3-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12747 | RWB-P7-E2042-APP | DOR-RWB-P7-E2042-APP-10 |  | State the empty, loading, error and no-access states of screen SCR-39. |

### OTHER:TSD P7 rwb-decision (with TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12750 | RWB-P7-E2042-APP | GAP-1615 | find it | Re-issue TSD P7 with T3.1 entries for the four rule tables and rule-version and package operations; remove them from TSD P3 and P4; set x-module of nine rule paths to P7. |

### OTHER:RWB-E2-008 application-slice story (rwb-payment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12752 | RWB-P7-E2042-APP | GAP-2503 | find it | Declare the nine consumed operations on per-service bases, name workflow matchPayments with its four activities, and record in the RTM that AC1, AC3, AC4 and AC5 have no story in this split. |

### RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12753 | RWB-P7-E2042-APP | GAP-0657 | find it | Record the rwb-payment JOB-08 owner row as superseded; fix the six unsettled consumed paths and shapes with their owners; allocate the rwb-integration login in RWB-PLT-DB. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12755 | RWB-P7-E2042-APP | GAP-1292 | find it | Hold one row per package version: PM-2026.12 from 2026-12-01 as the RWB-E2-027 value; PMT-2026.12 from 2026-12-15 as the E2-042 value; reconcile into one label and date before SIT promotion. |

### OTHER:RWB-E2-027 owner (business analyst) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12756 | RWB-P7-E2042-APP | GAP-1297 | find it | Raise one reconciliation so that PAYMENT_MATCH holds one version label and one valid-from date before SIT; this story keeps its copied legacy value. |

### OTHER:TSD P4 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12757 | RWB-P7-E2042-APP | GAP-2313 | 4 | Move the six rule-package and rule-version endpoints to P7 ownership; P4 keeps the Rules and parameters guard and the loader and approver rights. |

### RWB-P2-E2035-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12760 | RWB-P7-E2042-APP | GAP-0669 | 13 | Fix the login, secret reference and probe checks; add the next-action-check job catalogue row with its run book path; review the runbook with on-call. |

### RWB-P4-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12763 | RWB-P7-E2042-APP | GAP-0967 | 3 | Publish the service-identity rows of the permission matrix across the fourteen capability areas; confirm with the platform identity owner that each service runs as one non-human actor. Record the capability area of each package as a rwb-decision package attribute. |

### RWB-P6-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12764 | RWB-P7-E2042-APP | GAP-2399 | 1 | The notice path refuses a request made while no package version is in force with MSG-GEN-006, creates no notice row, dispatches nothing and adds no hold reason of this service. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12766 | RWB-P7-E2042-APP | GAP-1620 | 1 | Section 1 records the format question as Not specified; no format ruling is written. |

### RWB-P3-E2042-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12767 | RWB-P7-E2042-APP | GAP-0723 | find it | Provide reviewed values per environment for blob retention and immutability, pod heap for 20 KieBases, alert windows, replica counts and probe timings, confirmed with the platform and audit owners before wave 2 release. |

### OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12768 | RWB-P7-E2042-APP | GAP-0968 | find it | Correct T3.1 and T6.1 in the next version so the four rule tables (rule_package, rule_package_version, rule_row, rule_test_case) and their registry operations are P7's; keep P4 rows for rights and access log only. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12769 | RWB-P7-E2042-APP | GAP-0969 | find it | Add a parameter row fixing the lifetime of a cached authorise answer, to be set at the wave 2 design review by the Solution architect. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2043 CON Tempo (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12774 | RWB-P7-E2043-APP | DOR-RWB-P7-E2043-APP-21 | header | Move RWB-P3-E2043-CON from Status Draft (realignment v1) to published. |

### OTHER:Platform workflow kit owner (DevOps team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12785 | RWB-P7-E2043-APP | GAP-0725 | 13 | Fix the build ID as the release commit ID supplied by the workflow kit, pin builds with drain-on-complete, and set the policy once for all 19 services. |

### OTHER:Build pipeline replay gate configuration (DevOps team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12786 | RWB-P7-E2043-APP | GAP-0726 |  | Replay one recorded history per acceptance path of the reference fixture, keep them with the contract jar, and take the MSG-P3-038 text from the message catalogue before the gate is mandatory. |

### OTHER:AsyncAPI schema of rwb.decision-record.v1 and OpenAPI of the two decision-log operations (wave 2 design review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12787 | RWB-P7-E2043-APP | GAP-1304 | 3 | Publish the payload of DecisionRecorded, the ingest columns of decision_log_entry and the three message texts; the story keeps the assumed shape of ASM-B-P7-05-E2043-1 until then. |

### OTHER:rwb-case parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12788 | RWB-P7-E2043-APP | GAP-1305 | 3 | Publish the five-minute collection target and the 02:00 chain-check time as named parameters with a version and owner; the ledger reads them at the version in force on the business date. |

### RWB-P3-E2043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12792 | RWB-P7-E2043-APP | GAP-0727 |  | Settle RecordAndApplyRequest and the rule outputs map at the baseline review: event key, rule result, state change and business date as the only request members, plus a package-specific output schema. |

### OTHER:Workflow Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12793 | RWB-P7-E2043-APP | GAP-2021 |  | Add the child and kit workflow ID rule: the parent generates one ID per child from the case ID and the stage code, so a restart cannot create a second child for the same stage. |

### OTHER:Squad sizing source (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12799 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-16 | header | Size row holds the placeholder only. No source states that the squad sizes at refinement. |

### RWB-P7-E6028-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12800 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-21 | header | No header row added; the contract row names RWB-S7-E6028-CON only. Publication of RWB-P7-E6028-CON is outside this story. |

### OTHER:Contract fake library for rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12801 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-22 | header | Publish the contract fake and record its version in the header row added for it. |

### OTHER:Published write-off contract (version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12802 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-23 | header | Version is not in the source documents; the row holds the Not specified placeholder. The version must come from the contract publication. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12804 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-8 | 12.1 | Add POST /approvals to rwb-decision.yaml; publish GET /api/recovery/access/v1/doa-limits and POST /api/recovery/access/v1/authorise in rwb-access. P2 401 fixed in 12.1. |

### OTHER:P3 screen specification for SCR-27 (owner P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12808 | RWB-P7-E6028-APP | DOR-RWB-P7-E6028-APP-10 | none | Add empty, loading, error and no-access states to SCR-27. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12811 | RWB-P7-E6028-APP | GAP-1794 | 12.7 | Add the four S7 entity groups with key fields and rows, and hold write_off as the one table the map lists. |

### OTHER:FSD P7 S7 A2.15 (R-WO-37 to R-WO-39) and the rwb-writeoff story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12812 | RWB-P7-E6028-APP | GAP-1812 | none | Consume ProceedsMatched as the match, hold unmatched payments in its exception list, and open the initial match with the P8 owner. |

### OTHER:TSD P7 v2 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12813 | RWB-P7-E6028-APP | GAP-1311 | 3, 15 | Publish POST /approvals on the decision base with the section 3 body fields and an Idempotency-Key; publish the action, page and decision-log shapes; list the decision code and final calls as LOV-DECISION and final-call reference data. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12814 | RWB-P7-E6028-APP | GAP-1314 | 8 | Add RW-CREDCOMM to the holders of the WRITE_OFF_AND_POSTING capability right, or record why R-WO-12 routes to a role that cannot decide, before the wave 4 entry check. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12815 | RWB-P7-E6028-APP | GAP-1312 | 3 | Carry RWB-PLT-E1027-CON and RWB-PLT-N001-CON as non-blocking wave 0 platform contracts, and the four consumed contracts as P3 and P4 published contracts, built against their fakes. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20795 | RWB-P7-E2041-APP | R-22286 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20871 | RWB-P7-E2032-APP | R-22678 |  | Per-environment INT-23 path, identities, budgets and sizing belong in the ACE platform environment records; topic rwb.agent.events.v1 is already in section 3. |

### 05 Technical architecture/Recovery Workbench Workflow Engine Design v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20906 | RWB-P7-E2043-APP | R-28880 |  | write failed: WRITE FAILED (nothing was written): X002-F2: old text found 0 time(s) in paragraphs, expected 1 |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0203 | The entity Payment match rule has no row in the Ownership Map and no target table | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0410 | The agent-intake harness pack, the Enterprise AI test endpoint and the policy fixtures are not specified | Integration lead | Resolved (directive) |
| GAP-0411 | SIT harness environment, SCREEN-S2 fixture pack, Enterprise AI test profile, evidence format and gate for the deviation-screening journey are not specified in any source read | Integration lead | Resolved (directive) |
| GAP-0414 | The TDR suggestion has no agreed start operation: the legacy treatment side calls rwb-agent in process, Architecture v5 gives no S2-to-P10 call, and no source gives the harness environment, the TDR model stub controls, the evidence format or the gate | Integration lead | Resolved (directive) |
| GAP-0418 | Gateway-bff composite next-action route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0419 | Wave 2 queue-placement harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0420 | Rule-change report harness environment, seeding, evidence format, retention and composite route detail are not specified | Integration lead | Resolved (directive) |
| GAP-0421 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0422 | Reference workflow harness repository and SIT environment, seeding, evidence format and gate are not specified, and the ownership map holds no rwb-case outbox delivery read | Integration lead | Resolved (directive) |
| GAP-0458 | The post charge-off sale harness pack for the debt sale handover is not specified | Integration lead | Resolved (directive) |
| GAP-0622 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the item key set, the invalid-verdict refusal, the migration order and the segment rule are not specified | Solution architect with the P10 service owner and the owners of rwb-case and rwb-decision | Resolved (directive) |
| GAP-0623 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the record event type name, the route path, the 409 rule and the invalid-verdict refusal are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0624 | Case intake agent at L1 deployment in rwb-agent: the login, the migration order, the topic partitions and retry names, the alert window and thresholds, the worker and probe values and the route path are not specified | Platform administrator with the DevOps team and the ACE database team | Resolved (directive) |
| GAP-0625 | The app slice of the deviation screening evaluation and L1 on one segment: the service login, the S8 raise contract story, the parameter keys of the floor and the promotion condition, the sealed decision-entry read, the gateway-bff route path and the migration numbering are not fixed by any source | TechX with the rwb-deviation (S8) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0626 | The contract slice of the deviation screening evaluation and L1 on one segment: the S8 raise path and members, the parameter keys, the member types of a consumed answer, the sealed decision-entry read, the service login and the route path are not specified by any source | TechX with the rwb-deviation (S8) owner, the rwb-decision (P7) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0633 | The TDR offer-suggestion slice in rwb-agent: the operation path below the base, the treatment and account read operations, the parameter keys, the screen route, the run version fields, the inputs reference and the two waits of the call are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-treatment, rwb-case and rwb-decision | Resolved (directive) |
| GAP-0634 | The TDR offer-suggestion contract slice: the operation path and request members, the record member types, the boundary answer and error mapping, the admin read route and the two-wait exception are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision, rwb-treatment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-0635 | The infrastructure slice of the TDR offer-suggestion key: the INT-23 host, port, certificate and Key Vault names, the partition and retention values, the sizing, the budget measurement points and the alarm thresholds are not specified by any source | SCB IT infrastructure with the ACE platform team and security | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0670 | rwb-integration queue-write adapter: the operation owner, the login, the consumed contract field names and the replay window are not fixed by one source | Solution architect | Resolved (directive) |
| GAP-0671 | rwb-integration queue-write adapter contract: the ownership of the placement path, the consumed contract shapes and the library table columns are not fixed by one source | Tech lead | Resolved (directive) |
| GAP-0718 | The case-side rule-change audit read has no row in the ownership map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
| GAP-0720 | Retention and lifecycle windows of the new audit read and its contract are not specified | Data steward | Resolved (directive) |
| GAP-0721 | The rule package registry is declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0722 | The rule-model and rule-catalog read operations have no published field-level shape | P7 rwb-decision owner | Resolved (directive) |
| GAP-0723 | Blob immutability period, pod memory for 20 KieBases, alert windows and probe timings are not specified | SCB IT infrastructure with the DevOps team | Resolved (directive) |
| GAP-0724 | Reference fixture lifecycle, store and owner for the synthetic case | TechX | Resolved (directive) |
| GAP-0725 | Worker build ID format and worker versioning policy are not stated | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0726 | Replay corpus, history retention and the text of MSG-P3-038 | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0727 | Field-level detail of RecordAndApplyRequest and of the rule outputs map | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0734 | The next-action slice leaves the legacy AC allocation, the daily check Schedule, the DL22 durations and the role-class field unspecified | Tech lead | Resolved (directive) |
| GAP-0735 | The placement slice leaves the legacy AC allocation, the approved callers list, the production matrix grant, the overflow shape, the caller mapping and the login name unspecified | Tech lead | Resolved (directive) |
| GAP-0957 | rwb-access queue-write authority: the request and answer element set of the placement admission part of POST /authorise and of the non-human part of GET /me/permissions is named by no source | Solution architect | Resolved (directive) |
| GAP-0958 | rwb-access queue-write authority: the refusal reason code vocabulary and the status each code answers with are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0959 | rwb-access queue-write authority: no source binds a role to a list of teams or regions, so a scope narrower than ALL cannot be resolved for a non-human caller | Security administrator | Resolved (directive) |
| GAP-0960 | rwb-access queue-write authority: how a caller code is bound to a Workbench role, and whether a caller code is itself a role, is fixed by no source | Security administrator | Resolved (directive) |
| GAP-0962 | The roles and letters of the rule-administration area differ between the work package line, the legacy authority table and TSD P4 v3 T6.1, and the legacy access test names a role the matrix gives the right | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0964 | The two operations of this slice, and their request and answer shapes, are absent from Architecture v5, the API Specification and the TSD P4 appendix | Solution architect with the API Specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0965 | Which right a service identity holds to ask this service about a person other than the session user is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0967 | rwb-access rule-package authority: the scope of a running service identity inside rwb-access and the capability area each rule package serves are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0968 | rwb-access rule-package authority: TSD P4 v3 gives P4 the four rule tables, while Architecture v5 and the ownership ruling put the rule registry in P7 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0969 | rwb-access rule-package authority: the lifetime of a cached authorise answer, the refresh trigger of the cached permission data and the granularity of the access-log entry of a dry run are not specified | Solution architect | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1294 | No source gives the value set or the wire shape this story needs: the append request and answer, the ledger read and its page, the reason codes, the run read field set, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1298 | The decision code of a rule-governance entry is not named in any source this key may read | Decision log owner | Resolved (directive) |
| GAP-1299 | The name of the rwb-decision database login is not specified | ACE database administrator | Resolved (directive) |
| GAP-1300 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Business analyst | Resolved (directive) |
| GAP-1301 | The four rule registry tables are declared for P4 and P3 in their TSDs and are absent from the P7 TSD | Solution architect | Resolved (directive) |
| GAP-1302 | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Business analyst | Resolved (directive) |
| GAP-1303 | The BRD section pointers copied from the legacy story no longer match BRD v2 and v4 | Business analyst | Resolved (directive) |
| GAP-1304 | The payload of DecisionRecorded, the field set of the ledger ingest and the answer bodies of the two reads have no source | Solution architect, P7 rwb-decision, with the platform outbox and event team, the P3 business analyst and the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1305 | The collection target of five minutes and the chain-check time of 02:00 are named as values but no source names them as parameter rows | Center of excellence analyst with the P3 rwb-case team and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1307 | The name of the per-service database login of rwb-decision is not fixed by any source | ACE DB team with the P7 rwb-decision team | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1311 | The approval item and its two records: the raise operation, the action and answer shapes, the routing and final-call value sets, the message texts and the login name have no source | Business analyst, P7 rwb-decision, with the P4 rwb-access business analyst and the S7 rwb-writeoff analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1312 | The DP table adds two platform contracts and the story consumes three operations that its metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-access team | Resolved (directive) |
| GAP-1314 | The right and the role that may approve an escalated write-off pack are read two ways | P4 rwb-access business analyst and the security administrator, with the P7 rwb-decision business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1463 | RWB-E2-032 is conditional on a model existing and no decision row names who confirms it | Restructure operations officer with the TDR team | Resolved (directive) |
| GAP-1565 | The rule package registry, the rule-package operations and the change report are claimed by the P4 technical specification while the Ownership Map gives them to rwb-decision | Solution architect with the rwb-decision contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1794 | The Ownership Map lists one table for rwb-writeoff, while Architecture v5 gives the schema four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1799 | A charged-off population is handed to the debt sale route, and neither service's matrix row shows the other | Solution architect with the S6 owner | Resolved (directive) |
| GAP-1800 | The FSD routing rules move the case through twenty states, while Architecture v5 gives the case state to rwb-case | Solution architect with the P3 owner | Resolved (directive) |
| GAP-1812 | Payment matching after charge-off is given to this module, while P8 owns payment and proceeds matching | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1832 | The two deviation events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision log entry to travel with them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1882 | The treatment-side use of the suggestion is unspecified: the agent-run operation and its payload on the caller side, the treatment columns that hold the proposal and the model, prompt and policy versions, the 60 s wait and its fallback contract, and the decision code of a suggestion record | Solution architect | Resolved (directive) |
| GAP-1883 | Architecture v5 slide 16 publishes no inbound suggestion operation on rwb-agent, while the legacy treatment flow calls one synchronously | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-1994 | payment_match_rule has no owner in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2018 | Strict-mode wait at a point of no return is not defined in this design | Service owner P7 rwb-decision with the saga owners S2, S5, S6 and S7 | Resolved (directive) |
| GAP-2019 | Child workflow start policy and failure path are not specified | Service owner P3 rwb-case with the stage owners S1 to S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2021 | Child and kit workflow ID format | Service owner P3 rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2024 | Who pauses the stage clock when the stage runs as a child | Service owner P3 rwb-case with S8 rwb-deviation | Resolved (directive) |
| GAP-2026 | Owning service of the PAYMENT_MATCH package is not stated in one place | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2034 | The UNIVERSAL package has no single owning service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2053 | Outbox scope: Epics 1 and 2 in version 3, every service in Arch v5 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2190 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the acceptance event name, the list codes, the case-decision proposal path, the route path, the feature flag home, the topic and migration values and the policy values the gate reads are not specified | Solution architect with the P10 service owner and the owners of rwb-case, rwb-decision and rwb-source-data | Resolved (directive) |
| GAP-2191 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the acceptance event name, the case-decision proposal path, the route path, the 409 rule, the item key set, the invalid-verdict refusal and the policy values are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-case and rwb-decision | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2192 | Case intake agent at L1 deployment in rwb-agent: the login, the route path, the topic partitions, retry and retention, the migration order, the alert window and thresholds, the worker and probe values and the consumer groups are not specified | Platform administrator with the DevOps team and the ACE database team | Resolved (directive) |
| GAP-2193 | RWB-P10-E2029-APP: values the sources leave open for the screening L1 app slice | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2194 | RWB-P10-E2029-CON: contract detail the sources leave open for the screening key | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2313 | The rule-package endpoints are P4 in the legacy contract and P7 in Arch v5 | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2322 | rwb-access next action: the role-catalogue operation, the authorise request and answer of a next-action read, the rwb-access login and the message for an unknown role code are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2323 | rwb-access next action: the role class list has no customer-party value, while the legacy waiting text is produced for a customer party or a partner user | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2324 | rwb-access next action: the RBAC matrix tabulates three capability areas and gives no Case record letter, so the R rights and the scopes the next-action read needs are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2325 | rwb-access next action: a role row carries no version label of its own and the lifetime of a cached access or role answer is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2396 | Architecture v5 slide 13 gives P6 to P7 a Temporal cell and no event cell, while RWB-P6-E1073-APP consumes RulePackageInForce from rwb.decision.events.v1 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2397 | No source states where the package version and checksum of a notice decision are stored, and the legacy story adds no column for them | Data steward | Resolved (directive) |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2399 | No source states the state a notice rests in, or the message, when no package version is in force | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2402 | No source gives the wire shapes, the value sets or the dependency rows this story needs: the append request and answer, the evaluation and run reads, the case-less approval row, the promotion decision code, the text of MSG-P7-009, the name behind EV-30 and the DP-02 login name | Solution architect, P7 rwb-decision, with the P10 rwb-agent owner, the rwb-case owner, the data steward and the delivery lead | Resolved (directive) |
| GAP-2403 | No source gives the wire shape or the value sets this story needs: the append request and answer, the ledger read and its page, the reference-data operation, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2405 | rwb-decision next action: the answer shape of the rule-catalog and latest-state-change reads, and their not-found and malformed-parameter messages, are not specified | Solution architect | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2407 | rwb-decision next action: no source enumerates the decision codes or final calls that count as a state change for the latestStateChange filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2408 | rwb-decision next action: rule_row.timer_spec has no list of values, and two legacy specs are outside the four shapes the legacy rule enumerates | Business analyst, Epic 2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2409 | The published catalogue path shows packageVersion as an optional query parameter and no source says what an absent value answers | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2411 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2413 | No source gives the field-level shapes this story needs: the change-report element beyond its legacy field names, the CSV column order, the rulesChanged element, the decision-code and item-list values, the reconciliation read and the DP-02 login name | Solution architect | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2415 | The legacy story places the change checklist and the report in module P3 and the P4 package recovery.accessadmin.rulepackages with a P3 feature flag, while the target puts the registry, the checklist column and the decision log in rwb-decision | Solution architect | Resolved (directive) |
| GAP-2416 | Legacy AC1 approves ALLOCATION version ALLOC-2026.12 on 2026-12-02 while AC5 loads the same version on 2026-12-08 and approves it on 2026-12-09, so BR4 (verify on or after the load and before the approval) cannot hold in both readings | Business analyst P7 | Resolved (directive) |
| GAP-2485 | The booking-confirmation decision is placed in rwb-decision while DP-04 and the registry story keep the evaluation in the owning service and state that rwb-decision never evaluates | Solution architect, with the decision service owner | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3100 | RWB-S8-E2029-APP: the confirmed-proposal raise has no published request shape beyond the legacy Java signature, no operation name for the agent-policy read, no published constraint for one open code, no envelope type for the decision-record entry and no test level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3102 | RWB-S8-E2036-APP: the deviation hold that the queue-write interface obeys has no published element names, no case-event names, no case-side setter for deviation_open and no placement-half criteria, and the pattern set adds dependencies the metadata rows do not carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
