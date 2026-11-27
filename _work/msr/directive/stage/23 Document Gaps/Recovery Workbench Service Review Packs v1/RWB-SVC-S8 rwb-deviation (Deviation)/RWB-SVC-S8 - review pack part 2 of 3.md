# RWB-SVC-S8 rwb-deviation (Deviation) - review pack, part 2 of 3 (RWB-S8-E2033-APP to RWB-S8-E7007-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 16 |
| Resolved in the stories | 397 |
| Cross-document (pending in another document) | 212 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 21 |
| Register gaps linked | 50 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S8-E2033-APP | 23 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E2033 APP Case and queue list with status, owner and ageing v2.md |
| RWB-S8-E2036-APP | 25 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E2036 APP Queue write interface for models and agents v2.md |
| RWB-S8-E7001-APP | 32 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7001 APP Run X1 dispute and complaint end to end v2.md |
| RWB-S8-E7001-CON | 22 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7001 CON Run X1 dispute and complaint end to end - contract v2.md |
| RWB-S8-E7002-APP | 35 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7002 APP Run X2 vulnerability and hardship end to end v2.md |
| RWB-S8-E7002-CON | 17 | 7 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7002 CON Run X2 vulnerability and hardship end to end - contract v2.md |
| RWB-S8-E7003-APP | 36 | 18 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7003 APP Run X3 deceased customer end to end v2.md |
| RWB-S8-E7003-CON | 17 | 17 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7003 CON Run X3 deceased customer end to end - contract v2.md |
| RWB-S8-E7004-APP | 38 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7004 APP Run X4 fraud end to end v2.md |
| RWB-S8-E7004-CON | 15 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7004 CON Run X4 fraud end to end - contract v2.md |
| RWB-S8-E7005-APP | 26 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7005 APP Run X5 bankruptcy and seizure end to end v2.md |
| RWB-S8-E7005-CON | 18 | 6 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7005 CON Run X5 bankruptcy and seizure end to end - contract v2.md |
| RWB-S8-E7006-APP | 30 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7006 APP Run X6 lost contact and skip trace end to end v2.md |
| RWB-S8-E7006-CON | 20 | 6 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7006 CON Run X6 lost contact and skip trace end to end - contract v2.md |
| RWB-S8-E7007-APP | 30 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7007 APP Run X7 collateral event end to end v2.md |
| RWB-S8-E7007-CON | 13 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7007 CON Run X7 collateral event end to end - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S8-E7004-APP | R-03069 | CG-ALL-11498 | Script gap | Product owner | The story adds DEV_REROUTE to the closed list LOV-DEV-OUTCOME | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E7005-APP | R-03081 | CG-ALL-11532 | Script gap | Product owner | The story adds DEV_FLAGGED to the closed list LOV-DEVIATION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E7006-APP | R-03084 | CG-ALL-11560 | Script gap | Product owner | The story adds DEV_WITH_OWNER to the closed list LOV-DEVIATION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E7006-APP | R-03085 | CG-ALL-11561 | Script gap | Product owner | The story adds DEV_WITH_OWNER to the closed list LOV-RAISED-BY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E7003-ITG, RWB-S8-E7003-APP, RWB-S8-E7003-CON | R-09219 | GAP-1825 | Register gap | Product Owner | The deceased customer requirement is E3 in the program and the FSD and E7 in the BRD, and the BRD's own question on it is still open | Release the X3 contact stop, the heir notification and the insurance claim path as the E3 slice of wave 2, and the full X3 flow with its approver and return point in wave 4. The Product Owner's answer to Q-015 closes the question without moving a date. |
| RWB-S8-E2033-APP | R-13389 | CG-ALL-11392 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7002-APP | R-13407 | CG-ALL-11443 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7003-APP | R-13418 | CG-ALL-11475 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7004-APP | R-13432 | CG-ALL-11514 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7005-APP | R-13449 | CG-ALL-11545 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7005-CON | R-13453 | CG-ALL-11556 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7007-APP | R-13469 | CG-ALL-11605 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2015-ITG, RWB-ITG-E7006-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON | R-22499 | GAP-1827 | Register gap | Business lead | The deviation service level is 'set with DL22' and has no number, and the ten working day escalation comes only from the design | Carry the service level, the escalation period and the skip trace window as versioned reference data read at run time, assert no number, and take the values from DL22 when the business lead sets them. |
| RWB-ITG-E7003-ITG, RWB-S8-E7003-APP, RWB-S8-E7003-CON | R-22870 | GAP-0467 | Register gap | S8 rwb-deviation product owner with the rule owner in rwb-decision | Legacy X3 acceptance criterion AC3 cites R-DEV-06, a rule the published X3 branch does not use | Keep legacy AC3 verbatim in RWB-S8-E7003-APP as its build criterion and correct its rule id there to R-DEV-03 with R-DEV-11 and R-DEV-12 as the two outcomes. In this harness the legacy AC3 text is carried by TC-E7-003-03-ITG but the run asserts R-DEV-11 (AC4) and R-DEV-12 (AC5) and no approval step. R-DEV-06 stays with the X6 and X7 harness stories. |
| RWB-ITG-E7003-ITG, RWB-S8-E7003-APP, RWB-S8-E7003-CON | R-22872 | GAP-1478 | Register gap | Product Owner | The deceased customer flow is placed in Epic 3 by the program requirement and in Epic 7 by the specification and the stories | Read the requirement as an E7 deviation flow served by RWB-E7-003, and record in the E3 scope that the death and estate capability is delivered in E7. No story moves between epics without the Product Owner's decision. |
| RWB-S8-E7001-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON | R-23644 | GAP-3071 | Register gap | Solution architect with the rwb-source-data owner, the rwb-access owner, the platform library owner and Compliance | RWB-S8-E7010-CON: the consumed ledger operation, the breach-entry attributes, the breach read, the conduct-officer right and the clock length have no published baseline | Publish the interaction-ledger read operation with its fields and its 2 s budget; confirm the breach-entry attributes against the local record schema; publish the SCR-08 breach read; record the RW-CONDUCT conflict and resolve it in the access matrix rather than in a contract; settle the service level with DL22; confirm that no breach event is published in wave 4. Until then the baseline declares the consumed row and the entry with the placeholders and the three absences. |
| RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28853 | GAP-1560 | Register gap | AI product owner | The queue write interface for models and agents has no approved consumer and no flag removal date | Name the first approved consumer and the flag removal date before the wave 2 release. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S8-E2033-APP | R-27781 | CG-ALL-11393 | 3 | Flyway file V2033_1__deviation_flag_read.sql is not in the V0001..Vnnnn form | Service Template Spec v1 §3.1 gives only the Vnnnn rule, and the story's migration line is not in the supplied parts. No next rwb-deviation V-number found in sources. Needs the service V-number. |
| RWB-S8-E7001-APP | R-21162 | DOR-RWB-S8-E7001-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Section 18 text is outside this chunk, so the DL22 fix cannot be placed. Recommended option: load values as parameters (Program BRD v5 section 9). |
| RWB-S8-E7001-APP | R-21166 | DOR-RWB-S8-E7001-APP-3 | 5, 7, 16 | Definition of Ready item 3 Acceptance criteria: Partial | X8 row in section 5 already cites AC3 and TC-E7-001-07. The AC3 test row in section 16 is outside this chunk and cannot be added here. |
| RWB-S8-E7001-APP | R-22213 | GAP-1826 | 8 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | R-DEV-21 is not built as a row here; the DEV package stays Phase 2 with rwb-decision. |
| RWB-S8-E7001-CON | R-08859 | DOR-RWB-S8-E7001-CON-8 |  | Definition of Ready item 8 Contract: Fail | PATCH row L257 already Not applicable. Topic rwb.deviation.events.v1 with .retry/.dlt confirmed in PRD S8 l.37 and FSD S8 l.48. Workflow ID form not in sources (PRD S8 l.124). Event lines not supplied. |
| RWB-S8-E7002-APP | R-08860 | DOR-RWB-S8-E7002-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources; a search for 'epic design' finds only _work escalation files. Needs the epic design record and its sign-off. |
| RWB-S8-E7002-APP | R-21186 | DOR-RWB-S8-E7002-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | PRD S8 gives BR-064 and BR-067 only at FR level (FR-S8-034, FR-S8-038), not per rule; BR IDs for R-DEV-01/03/10/17/20 would be invented. BR1-BR10 AC/TC rows are in sections 7 and 16, not in this chunk. |
| RWB-S8-E7002-CON | R-03053 | CG-ALL-11449 | 12.5; 1; 16 | Workflow DeviationWorkflow task queue rwb-deviation` in namespace `rwb-recovery differs from the catalog | Section 12.5 is fixed. Sections 1 and 16 still name rwb-recovery and their text is not in the diff; they need the same edit before this is resolved. |
| RWB-S8-E7002-CON | R-21190 | DOR-RWB-S8-E7002-CON-1 | 1 | Definition of Ready item 1 Story: Partial | Persona 'Solution architect' is not confirmed in the source; tech lead kept until the role code is verified. |
| RWB-S8-E7003-APP | R-08872 | DOR-RWB-S8-E7003-APP-14 |  | Definition of Ready item 14 Epic design: Fail | Current DoR row text is not in the chunk, so no exact old text exists to edit. Grep found no signed epic design record in the story or sources; sign-off not invented. |
| RWB-S8-E7003-APP | R-21198 | DOR-RWB-S8-E7003-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Current DoR row text is not in the chunk, so no exact old text exists to edit. Personal-data classification of P2 fields is not in the sources; needs owner data classification, not invented. |
| RWB-S8-E7003-CON | R-08878 | DOR-RWB-S8-E7003-CON-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or the realignment folder search. The sign-off value is not in the sources, so nothing can be filled in. |
| RWB-S8-E7003-CON | R-21208 | DOR-RWB-S8-E7003-CON-10 | not in chunk | Definition of Ready item 10 Screens and states: Partial | SCR-06 and SCR-08 state text is not in the chunk, and an edit needs exact current text. No state text invented. |
| RWB-S8-E7003-CON | R-21210 | DOR-RWB-S8-E7003-CON-15 | not in chunk | Definition of Ready item 15 INVEST: Partial | INVEST text is not in the chunk. The two-week fit is not in the sources; the Size row gives DOR-RWB-S8-E7003-CON-16 as not specified. |
| RWB-S8-E7003-CON | R-21212 | DOR-RWB-S8-E7003-CON-4 | 8, 16 | Definition of Ready item 4 Business rules: Partial | TC-S8-E7003-CON-03 to -13 were added mapped to BR1 to BR10, but the BR text is not in the chunk, so the mapping and the 2 s value are unverified. Needs the section 8 text to confirm or remove them. |
| RWB-S8-E7004-APP | R-08883 | DOR-RWB-S8-E7004-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or source documents (grep for epic design sign-off or record). Only scratch escalation files mention it. Sign-off cannot be invented; needs the epic design record. |
| RWB-S8-E7004-CON | R-08895 | DOR-RWB-S8-E7004-CON-8 | 12.3, 12.4, 12.5 | Definition of Ready item 8 Contract: Fail | Item stays open until the three unnamed Contract items are confirmed. |
| RWB-S8-E7005-APP | R-21233 | DOR-RWB-S8-E7005-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | SCR-06 and SCR-08 state rows are outside the supplied story text (header and change log only). No matching old text here; needs the chunk holding those rows. |
| RWB-S8-E7005-CON | R-33144 | NEWAC-RWB-S8-E7005-CON-AC9 | section 7 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Placement still needs the full scenario text. TC-S8-E7005-CON-07 still cites AC9, which now has no scenario. |
| RWB-S8-E7006-APP | R-21253 | DOR-RWB-S8-E7006-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is not in this chunk, so no exact old text exists to edit. Needs section 9 provided in the next chunk. |
| RWB-S8-E7006-APP | R-21260 | DOR-RWB-S8-E7006-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR IDs added in section 8 from existing citations; R-DEV-20 and R-UNI-12 have no cited BR. BR1-BR10 coverage needs section 16, not in this chunk. |
| RWB-S8-E7006-CON | R-21269 | DOR-RWB-S8-E7006-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Coverage needs AC text in section 7 and test rows in section 16, which are not in this chunk. No anchor for an edit, so no change made. |
| RWB-S8-E7006-CON | R-33152 | NEWAC-RWB-S8-E7006-CON-AC8 | 8 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 (AC style and numbering) and section 16 (test rows) are not in this chunk, so AC8 cannot be placed. Proposed test stays Not specified in the source documents (NEWAC-RWB-S8-E7006-CON-AC8). |
| RWB-S8-E7007-APP | R-21273 | DOR-RWB-S8-E7007-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Reclassifying P2 fields needs the personal-data field list, which is not in the header or the sources checked (no field names found). Cannot be done without inventing field names. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (30)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19554 | RWB-S8-E2036-APP | DOR-RWB-S8-E2036-APP-8 | find it | Add the activities named in story section 12.5 that the catalog lacks, starting with recordAndApplyDeviation, to Workflows and activities. Topic names already match EV-06 and EV-07. Workflow ID is covered by CG-ALL-11401. |
| CDC-19556 | RWB-S8-E2036-APP | CG-ALL-11402 | 12.5 | Add an Activities row for recordAndApplyDeviation, or name a catalogued activity in §12.5 |
| CDC-19557 | RWB-S8-E2036-APP | CG-ALL-11403 | 12.5 | Add an Activities row for releaseDeviationHold, or name a catalogued activity in §12.5 |
| CDC-19572 | RWB-S8-E7001-APP | DOR-RWB-S8-E7001-APP-8 | header | Add an idempotency key to PATCH /deviations/{deviationId}; state the DeviationWorkflow ID form and start rule; add evaluateDeviationRules to Temporal Catalog v1. |
| CDC-19573 | RWB-S8-E7001-APP | CG-ALL-11416 | 12.5 | Add an Activities row for evaluateDeviationRules (Activity, EvaluateRules step, queue rwb-deviation). |
| CDC-19574 | RWB-S8-E7001-APP | CG-ALL-11417 | 12.5 | Add an Activities row for recordAndApplyDeviation (Activity, RecordAndApply step, queue rwb-deviation). |
| CDC-19575 | RWB-S8-E7001-APP | CG-ALL-11418 | 12.5 | Add an Activities row for resolveDeviation (Activity, outcome step, queue rwb-deviation). |
| CDC-19600 | RWB-S8-E7002-APP | CG-ALL-11439 | 12.5 | Add activity applyDeviationOutcome to the Activities sheet, or name a catalogued activity |
| CDC-19608 | RWB-S8-E7002-CON | CG-ALL-11451 | 12.5 | Add activity applyDeviationOutcome to the Activities sheet on task queue rwb-deviation, with the inputs and outputs of section 12.5. |
| CDC-19624 | RWB-S8-E7003-APP | CG-ALL-11468 | 12.5 | Add an Activities row for raiseDeviation on task queue rwb-deviation, or name a catalogued activity instead. |
| CDC-19625 | RWB-S8-E7003-APP | CG-ALL-11469 | 12.5 | Add an Activities row for routeToOwner on task queue rwb-deviation, or name a catalogued activity instead. |
| CDC-19626 | RWB-S8-E7003-APP | CG-ALL-11470 | 12.5 | Add activity applyContactStop to the Activities sheet, task queue rwb-deviation, contract element as in RWB-S8-E7003-APP §12.5. |
| CDC-19627 | RWB-S8-E7003-APP | CG-ALL-11471 | 12.5 | Add activity openEstatePath to the Activities sheet, task queue rwb-deviation, contract element as in RWB-S8-E7003-APP §12.5. |
| CDC-19628 | RWB-S8-E7003-APP | CG-ALL-11472 | 12.5 | Add activity recordOutcome to the Activities sheet, task queue rwb-deviation, contract element as in RWB-S8-E7003-APP §12.5. |
| CDC-19638 | RWB-S8-E7003-CON | CG-ALL-11488 | 12.5 | Add an activity row raiseDeviation on task queue rwb-deviation, or name a catalogued activity in its place. |
| CDC-19639 | RWB-S8-E7003-CON | CG-ALL-11489 | 12.5 | Add an activity row routeToOwner on task queue rwb-deviation, or name a catalogued activity in its place. |
| CDC-19640 | RWB-S8-E7003-CON | CG-ALL-11490 | 12.5 | Add an activity row applyContactStop on task queue rwb-deviation, or name a catalogued activity in its place. |
| CDC-19641 | RWB-S8-E7003-CON | CG-ALL-11491 | 12.5 | Add an activity row openEstatePath on task queue rwb-deviation, or name a catalogued activity in its place. |
| CDC-19642 | RWB-S8-E7003-CON | CG-ALL-11492 | 12.5 | Add an activity row recordOutcome on task queue rwb-deviation, or name a catalogued activity in its place. |
| CDC-19653 | RWB-S8-E7004-APP | CG-ALL-11509 | 12.5 | Add activity EvaluateDeviationRules, task queue rwb-deviation, or name a catalogued activity. |
| CDC-19654 | RWB-S8-E7004-APP | CG-ALL-11510 | 12.5 | Add activity RecordAndApplyDeviation, task queue rwb-deviation, or name a catalogued activity. |
| CDC-19666 | RWB-S8-E7004-CON | CG-ALL-11525 | 12.5 | Add an Activities row EvaluateDeviationRules, type Activity, task queue rwb-deviation. |
| CDC-19667 | RWB-S8-E7004-CON | CG-ALL-11526 | 12.5 | Add an Activities row RecordAndApplyDeviation, type Activity, task queue rwb-deviation. |
| CDC-19704 | RWB-S8-E7006-APP | CG-ALL-11566 | 12.5 | Add activity evaluateDeviationRules to the Activities sheet on queue rwb-deviation, as in §12.5, or name a catalogued activity. |
| CDC-19705 | RWB-S8-E7006-APP | CG-ALL-11567 | 12.5 | Add activity recordAndApplyDeviation to the Activities sheet on queue rwb-deviation, as in §12.5, or name a catalogued activity. |
| CDC-19706 | RWB-S8-E7006-APP | CG-ALL-11568 | 12.5 | Add activity runSkipTrace to the Activities sheet on queue rwb-agent, as in §12.5, or name a catalogued activity. |
| CDC-19707 | RWB-S8-E7006-APP | CG-ALL-11569 | 12.5 | Add activity readContactData to the Activities sheet on queue rwb-deviation, as in §12.5, or name a catalogued activity. |
| CDC-19708 | RWB-S8-E7006-APP | CG-ALL-11570 | 12.5 | Add activity resolveDeviation to the Activities sheet on queue rwb-deviation, as in §12.5, or name a catalogued activity. |
| CDC-19714 | RWB-S8-E7006-CON | CG-ALL-11584 | 12.5 | Add activity readContactData to the Activities sheet, or name a catalogued activity in its place (Solution architect) |
| CDC-19729 | RWB-S8-E7007-APP | CG-ALL-11602 | 12.5 | Add activity recordCollateralOutcome to the Activities sheet, or the story uses a catalogued activity. |

### API:(service not named) (21)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19614 | RWB-S8-E7003-APP | CG-ALL-11458 | 12.2 | Declare REST base /api/recovery/source-data/v1 for provider P1 rwb-source-data. |
| CDC-19615 | RWB-S8-E7003-APP | CG-ALL-11459 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case. |
| CDC-19616 | RWB-S8-E7003-APP | CG-ALL-11460 | 12.2 | Declare REST base /api/recovery/access/v1 for provider P4 rwb-access. |
| CDC-19617 | RWB-S8-E7003-APP | CG-ALL-11461 | 12.2 | Declare REST base /api/recovery/decision/v1 for provider P7 rwb-decision. |
| CDC-19623 | RWB-S8-E7003-APP | DOR-RWB-S8-E7003-APP-8 | header | Add the yaml bases /api/recovery/source-data/v1, /api/recovery/case/v1, /api/recovery/access/v1, /api/recovery/decision/v1 and the 11 further bases in detcheck. |
| CDC-19632 | RWB-S8-E7003-CON | CG-ALL-11481 | 12.2 | Declare REST base /api/recovery/source-data/v1 from the Document Index service table. |
| CDC-19633 | RWB-S8-E7003-CON | CG-ALL-11482 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-19634 | RWB-S8-E7003-CON | CG-ALL-11483 | 12.2 | Declare REST base /api/recovery/access/v1 from the Document Index service table. |
| CDC-19635 | RWB-S8-E7003-CON | CG-ALL-11484 | 12.2 | Declare REST base /api/recovery/decision/v1 from the Document Index service table. |
| CDC-19636 | RWB-S8-E7003-CON | DOR-RWB-S8-E7003-CON-8 | 1 | Add the base paths /api/recovery/source-data/v1, /api/recovery/case/v1, /api/recovery/access/v1 and /api/recovery/decision/v1, and the eight other bases named in the readiness check, to the yaml files. |
| CDC-19647 | RWB-S8-E7003-CON | GAP-3056 | 14 | Publish operation names, case event name, EV-06 and EV-07 target names and claim approval operation; bind error codes 401, 403, 404, 409, 422 and 503 to s14 IDs |
| CDC-19719 | RWB-S8-E7007-APP | CG-ALL-11592 | 12.2 | Declare the REST base /api/recovery/case/v1 using the provider's base from the Document Index service table. |
| CDC-19720 | RWB-S8-E7007-APP | CG-ALL-11593 | 12.2 | Declare the REST base /api/recovery/decision/v1 using the provider's base from the Document Index service table. |
| CDC-19721 | RWB-S8-E7007-APP | CG-ALL-11594 | 12.2 | Declare the REST base /api/recovery/guarantee/v1 using the provider's base from the Document Index service table. |
| CDC-19722 | RWB-S8-E7007-APP | CG-ALL-11595 | 12.2 | Declare the REST base /api/recovery/valuation/v1 using the provider's base from the Document Index service table. |
| CDC-19723 | RWB-S8-E7007-APP | CG-ALL-11596 | 12.2 | Declare the REST base /api/recovery/source-data/v1 using the provider's base from the Document Index service table. |
| CDC-19736 | RWB-S8-E7007-CON | CG-ALL-11611 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case provider. |
| CDC-19737 | RWB-S8-E7007-CON | CG-ALL-11612 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision provider. |
| CDC-19738 | RWB-S8-E7007-CON | CG-ALL-11613 | 12.2 | Declare the REST base /api/recovery/guarantee/v1 for the rwb-guarantee provider. |
| CDC-19739 | RWB-S8-E7007-CON | CG-ALL-11614 | 12.2 | Declare the REST base /api/recovery/valuation/v1 for the rwb-valuation provider. |
| CDC-19740 | RWB-S8-E7007-CON | CG-ALL-11615 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the rwb-source-data provider. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19576 | RWB-S8-E7001-APP | CG-ALL-11420 | 16 | Add rows for TC-E7-001-01 to TC-E7-001-04 on tab Story test cases, with Given, When and Then copied from the criteria they cover, in the next version. |
| CDC-19588 | RWB-S8-E7001-CON | DOR-RWB-S8-E7001-CON-12 | 16 | Add rows for TC-E7-001-01 to -04 and TC-S8-E7001-CON-01 to -03 under the same ids; TC-S8-E7001-CON-04 to -06 are new in the story. |
| CDC-19596 | RWB-S8-E7001-CON | CG-ALL-11431 |  | Add rows TC-E7-001-01 to -04 and TC-S8-E7001-CON-01 to -03, with Given, When and Then copied from the criteria they cover. |
| CDC-19601 | RWB-S8-E7002-APP | CG-ALL-11441 | 16 | Add rows TC-E7-002-01 to TC-E7-002-05 to Story test cases, with Given, When and Then from the criteria they cover; add TC-E7-002-06 to TC-E7-002-10 |
| CDC-19612 | RWB-S8-E7002-CON | CG-ALL-11452 | 16 | Add a Story test cases row, with Given, When and Then copied from the covered criterion, for TC-E7-002-01 to -05 and TC-S8-E7002-CON-01 to -05. |
| CDC-19629 | RWB-S8-E7003-APP | CG-ALL-11474 | 16 | Add rows to Story test cases for TC-E7-003-01 to TC-E7-003-06, TC-S8-E7003-APP-01, -02 and -03 with Given, When and Then copied from the covered criterion. |
| CDC-19644 | RWB-S8-E7003-CON | DOR-RWB-S8-E7003-CON-12 | 12.7, 16 | Add the IDs TC-E7-003-01 to TC-E7-003-06, TC-S8-E7003-CON-01 and TC-S8-E7003-CON-02 to Test Cases v8 |
| CDC-19648 | RWB-S8-E7003-CON | CG-ALL-11494 | 16 | Add rows for TC-E7-003-01 to TC-E7-003-06, TC-S8-E7003-CON-01 and TC-S8-E7003-CON-02, with Given, When and Then copied from the criterion each covers. |
| CDC-19655 | RWB-S8-E7004-APP | CG-ALL-11511 | 16 | Add rows TC-E7-004-01 to TC-E7-004-04 to tab Story test cases with Given, When and Then copied from the covered criteria; add TC-E7-004-05 to TC-E7-004-10 as well |
| CDC-19670 | RWB-S8-E7004-CON | DOR-RWB-S8-E7004-CON-12 | 12.7, 16 | Add Story test cases rows for TC-E7-004-01 to -04 and TC-S8-E7004-CON-01 to -19. |
| CDC-19674 | RWB-S8-E7004-CON | CG-ALL-11527 | 16 | Add rows TC-E7-004-01 to TC-E7-004-04 and TC-S8-E7004-CON-01 to TC-S8-E7004-CON-05, with Given, When and Then copied from the criteria they cover. |
| CDC-19685 | RWB-S8-E7005-APP | CG-ALL-11544 | 16 | Add rows for TC-E7-005-02 to -06 and TC-S8-E7005-APP-01 to -03 in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-19686 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-12 | 12 | Add rows TC-E7-005-02 to TC-E7-005-06 and TC-S8-E7005-APP-01 to TC-S8-E7005-APP-06 under tab Story test cases |
| CDC-19695 | RWB-S8-E7005-CON | DOR-RWB-S8-E7005-CON-12 | 12.7, 16 | Add rows for TC-E7-005-01 to TC-E7-005-06 and TC-S8-E7005-CON-01 to TC-S8-E7005-CON-06 under the same IDs. |
| CDC-19697 | RWB-S8-E7005-CON | CG-ALL-11555 | 16 | Add rows for TC-E7-005-01 to TC-E7-005-06 and TC-S8-E7005-CON-01 to TC-S8-E7005-CON-04, with Given, When and Then copied from the criterion each covers |
| CDC-19709 | RWB-S8-E7006-APP | CG-ALL-11572 | 16 | Add rows TC-E7-006-01, TC-E7-006-02, TC-E7-006-03 and TC-E7-006-04 with Given, When and Then copied from the criteria they cover. |
| CDC-19717 | RWB-S8-E7006-CON | CG-ALL-11586 | 16 | Add rows for TC-E7-006-01 to -04 and TC-S8-E7006-CON-01 to -07 in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-19730 | RWB-S8-E7007-APP | CG-ALL-11603 | 16 | Story side: section 16 now lists TC-E7-007-07 to -13. The Test Cases v8 rows are needed for all of them, not only -01 to -06. |
| CDC-19746 | RWB-S8-E7007-CON | DOR-RWB-S8-E7007-CON-12 | 12.7, 16 | Add rows for TC-E7-007-01 to -06 and TC-S8-E7007-CON-01 to -07 under the same IDs |
| CDC-19750 | RWB-S8-E7007-CON | CG-ALL-11619 | 16 | Add rows for TC-E7-007-01 to -06 and TC-S8-E7007-CON-01 to -05 under Story test cases, with Given, When and Then copied from the criterion each covers. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19555 | RWB-S8-E2036-APP | CG-ALL-11398 | 9 | Record decision_record as a platform library table in rwb_deviation (the hash-linked record written before the row, DP-03), or add a dictionary name for it; Data role to confirm. |
| CDC-19559 | RWB-S8-E2036-APP | DOR-RWB-S8-E2036-APP-7 | 11 | Add entity decision_record (platform library table in rwb_deviation, DP-03) |
| CDC-19578 | RWB-S8-E7001-APP | DOR-RWB-S8-E7001-APP-7 | 11 | Record decision_record as a Platform library table in rwb_deviation, or confirm it is outside the entity list, so the section 11 name resolves. |
| CDC-19587 | RWB-S8-E7001-CON | CG-ALL-11426 | 12.6 | Add decision_record as a dictionary name, or record the platform decision-record library table as the object in the owning document; the story names it at section 12.7 (owner: Data). |
| CDC-19599 | RWB-S8-E7002-APP | CG-ALL-11435 | 11, 12.7 | Record decision_record as the PLT library table created in rwb_deviation (DP-03), or add it to the dictionary with its classification. |
| CDC-19602 | RWB-S8-E7002-APP | DOR-RWB-S8-E7002-APP-7 | 11 | Confirm decision_record as a library object outside the LDM or add it as an entity; section 11 now states it is a library object. |
| CDC-19645 | RWB-S8-E7003-CON | DOR-RWB-S8-E7003-CON-7 | 11 | Confirm entity or field decision_record in LDM v9 or Data Classification v5, or the story renames the s12.7 table |
| CDC-19658 | RWB-S8-E7004-APP | DOR-RWB-S8-E7004-APP-7 | 11 | Add decision_record and inbox_event as entities or fields, or confirm them as PLT library objects outside the model. |
| CDC-19696 | RWB-S8-E7005-CON | DOR-RWB-S8-E7005-CON-7 | 11 | Add `decision_record` as the platform library object of RWB-PLT-E1027-CON, or confirm it is outside LDM v9 and Data Classification v5. |
| CDC-19710 | RWB-S8-E7006-APP | DOR-RWB-S8-E7006-APP-7 | 11 | decision_record is not an LDM v9 or DC v5 entity. AC2 now reads 'decision record' per the rename in R-27846; P3 is not changed here. |
| CDC-19732 | RWB-S8-E7007-APP | DOR-RWB-S8-E7007-APP-7 | 11 | Add decision_record as a PLT library object created in rwb_deviation to LDM v9 and Data Classification v5 |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19539 | RWB-S8-E2033-APP | CG-ALL-11386 | 12.1 | Publish GET /api/recovery/deviation/v1/deviation-flags in rwb-deviation.yaml through the owner's CON story, or remove it. |
| CDC-19618 | RWB-S8-E7003-APP | CG-ALL-11462 | 13 | Remove the fixed enum on outcome; LOV-DEV-OUTCOME is read as data at its version. |
| CDC-19619 | RWB-S8-E7003-APP | CG-ALL-11463 | 13 | Remove the fixed enum on deviationCode; LOV-DEVIATION is read as data at its version. |
| CDC-19620 | RWB-S8-E7003-APP | CG-ALL-11464 | 13 | Remove the fixed enum on raisedBy; LOV-RAISED-BY is read as data at its version. |
| CDC-19650 | RWB-S8-E7004-APP | DOR-RWB-S8-E7004-APP-8 | find it | Hold outcome, deviationCode and raisedBy as LOV references to LOV-DEV-OUTCOME, LOV-DEVIATION and LOV-RAISED-BY, not closed enums; align the DeviationRaised topic with the catalog. |
| CDC-19718 | RWB-S8-E7007-APP | CG-ALL-11591 | 12.1 | Publish PATCH /deviations/{deviationId} (API-S8-002) under /api/recovery/deviation/v1 through RWB-S8-E7007-CON, or remove the operation from this story. |
| CDC-19727 | RWB-S8-E7007-APP | DOR-RWB-S8-E7007-APP-8 | Header | Add PATCH /deviations/{deviationId} (API-S8-002) to rwb-deviation.yaml; add base paths /api/recovery/case/v1, /api/recovery/decision/v1, /api/recovery/guarantee/v1 and the eight further listed bases. |
| CDC-19735 | RWB-S8-E7007-CON | CG-ALL-11610 | 12.1 | Add path /deviations/{deviationId} with PATCH operation API-S8-002, request DeviationOutcome, response Deviation 200, and the error set 401, 403, 404, 409, 422, 503. |
| CDC-19742 | RWB-S8-E7007-CON | DOR-RWB-S8-E7007-CON-8 | find it | Add PATCH /deviations/{deviationId} (API-S8-002) to rwb-deviation.yaml; add the base paths /api/recovery/case/v1, /decision/v1, /guarantee/v1 and the other consumed bases to their yamls |

### Epic design record (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19541 | RWB-S8-E2033-APP | DOR-RWB-S8-E2033-APP-14 | header | Record the signed epic design sign-off for RWB-S8-E2033-APP in the epic design record. |
| CDC-19586 | RWB-S8-E7001-CON | DOR-RWB-S8-E7001-CON-14 | find it | Record the signed sign-off of the epic design; the story records no sign-off and none is invented. |
| CDC-19607 | RWB-S8-E7002-CON | DOR-RWB-S8-E7002-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S8 in the epic design record. |
| CDC-19663 | RWB-S8-E7004-CON | DOR-RWB-S8-E7004-CON-14 | header | Confirm the signed epic design sign-off and record it in the epic design record. |
| CDC-19675 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-14 | Header | Record the signed epic design sign-off for EP07 / RWB-SVC-S8; no signed epic design exists in the story or sources. |
| CDC-19698 | RWB-S8-E7006-APP | DOR-RWB-S8-E7006-APP-14 |  | Record the signed epic design sign-off for this epic in the epic design record. |
| CDC-19712 | RWB-S8-E7006-CON | DOR-RWB-S8-E7006-CON-14 | n/a | Record the signed epic design sign-off for RWB-SVC-S8. The story cannot supply this sign-off. |
| CDC-19724 | RWB-S8-E7007-APP | DOR-RWB-S8-E7007-APP-14 | Header | Record the signed sign-off of the epic design for RWB-SVC-S8 in the epic design record. |
| CDC-19741 | RWB-S8-E7007-CON | DOR-RWB-S8-E7007-CON-14 | header | Record the signed epic design sign-off for RWB-S8-E7007-CON. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19545 | RWB-S8-E2033-APP | DOR-RWB-S8-E2033-APP-7 | 12.7 | Record v_deviation_flag as a read-only view of rwb_deviation created by this story's migration; recovery_svc is resolved in the story (section 17). |
| CDC-19651 | RWB-S8-E7004-APP | CG-ALL-11499 | 12.7 | Record decision_record as a PLT library object created in rwb_deviation (DP-03), as RWB-S8-E7004-APP section 12.7 states, or add it to Fields. |
| CDC-19652 | RWB-S8-E7004-APP | CG-ALL-11500 | 12.7 | Record inbox_event as a PLT library object created in rwb_deviation (the processed row per consumed case event, section 12.4), as RWB-S8-E7004-APP section 12.7 states, or add it to Fields. |
| CDC-19687 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-7 | 11 | §11 already records it as a library object; AC4 Given line now reads decision record (CG-ALL-11546). |
| CDC-19693 | RWB-S8-E7005-CON | CG-ALL-11550 | 11 | Record the decision_record object (index, library table or flag) in the owning document, or adopt a dictionary name. |
| CDC-19703 | RWB-S8-E7006-APP | CG-ALL-11562 | 11, 12.7 | Record `decision_record` as a platform library table in rwb_deviation (the object the story names at lines 255 and 330), with no LDM field or entity of that name. |
| CDC-19728 | RWB-S8-E7007-APP | CG-ALL-11590 | 12.7 | Add decision_record as a PLT library object created in rwb_deviation: the local hash-linked decision record of each X7 outcome (DP-03), as RWB-S8-E7007-APP records at its section 12.7 line. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19679 | RWB-S8-E7005-APP | CG-ALL-11538 | 12.5 | Add an Activities row for validateDeviation (queue rwb-deviation, Activity), or map the story to a catalogued activity. |
| CDC-19680 | RWB-S8-E7005-APP | CG-ALL-11539 | 12.5 | Add an Activities row for evaluateRules (queue rwb-deviation, Activity through the embedded Drools kit), or map to a catalogued activity. |
| CDC-19681 | RWB-S8-E7005-APP | CG-ALL-11540 | 12.5 | Add an Activities row for recordDecision (queue rwb-deviation, Activity through the library), or map to a catalogued activity. |
| CDC-19682 | RWB-S8-E7005-APP | CG-ALL-11541 | 12.5 | Add an Activities row for applyDeviation (queue rwb-deviation, Activity, RecordAndApply), or map to a catalogued activity. |
| CDC-19683 | RWB-S8-E7005-APP | CG-ALL-11542 | 12.5 | Add an Activities row for raiseClockSignal (queue rwb-deviation, Activity or signal), or map to a catalogued activity. |
| CDC-19684 | RWB-S8-E7005-APP | CG-ALL-11543 | 12.5 | Add an Activities row for publishDeviation (queue rwb-deviation, Activity through the outbox), or map to a catalogued activity. |
| CDC-19713 | RWB-S8-E7006-CON | CG-ALL-11583 | 12.5 | Add activity runSkipTrace on queue rwb-agent, with its request in and source-of-contact and verified-flag out, as in section 12.5. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19643 | RWB-S8-E7003-CON | DOR-RWB-S8-E7003-CON-1 | 1 | Add the role tech lead of rwb-deviation, with its role code, to Users Roles and Permissions v5, or confirm the existing role code it should map to. |
| CDC-19668 | RWB-S8-E7004-CON | DOR-RWB-S8-E7004-CON-1 | 1 | Add 'tech lead' as a role name or code, or confirm the catalogued role that section 1 should name. |
| CDC-19690 | RWB-S8-E7005-APP | GAP-3059 | 4 | Widen RW-LEGAL to the Case record right on API-S8-001 and API-S8-002 (rwb-access). Story now marks the claim deadline as a versioned reference row Not specified. |
| CDC-19694 | RWB-S8-E7005-CON | DOR-RWB-S8-E7005-CON-1 | 1 | Add or map the role 'contract owner of rwb-deviation (S8)' as a role code or role name in Users Roles and Permissions v5. |
| CDC-19731 | RWB-S8-E7007-APP | DOR-RWB-S8-E7007-APP-6 | 10 | Add role SY-DATALOAD to Users Roles and Permissions v5 |
| CDC-19744 | RWB-S8-E7007-CON | DOR-RWB-S8-E7007-CON-1 | 1 | Add a role code or name for the tech lead of rwb-deviation, or the story role must be one already listed |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19552 | RWB-S8-E2033-APP | CG-ALL-11391 | 18 | Align the test lists for REQ-WKM-002, REQ-DVH-006 and the third requirement with section 18 of this story in the RTM's next version. |
| CDC-19570 | RWB-S8-E2036-APP | CG-ALL-11407 | 18 | REQ-CWC-017 to -019 aligned in §18 |
| CDC-19613 | RWB-S8-E7002-CON | CG-ALL-11453 | 18 | Align REQ-DVH-002 to TC-S8-E7002-CON-03 as section 18 gives, or record why TC-E2-015-02, TC-E2-015-06 and TC-E2-015-07 also trace it. |
| CDC-19661 | RWB-S8-E7004-APP | CG-ALL-11513 | 18 | Align REQ-DVH-002 test cases in RTM v7 (TC-E2-015-02, -06, -07) with section 18 (TC-E7-004-01) in the next version. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19562 | RWB-S8-E2036-APP | GAP-0957 | 12 | Carry the request and answer element names of section 12.1 as the realignment baseline; reconfirm with the rwb-integration owner at contract review; make changes additive first; keep caller type as a carried value of the list. |
| CDC-19565 | RWB-S8-E2036-APP | GAP-0958 | 12 | Fix five reason codes with one status each: 403 for RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL; keep MSG-GEN-001, MSG-GEN-002 and MSG-P7-003 for the 422 and 503 codes; keep MSG-P4-002 as the 403 message. |
| CDC-19566 | RWB-S8-E2036-APP | GAP-0959 | 12 | Admit a non-human caller on scope ALL only; record the presented team code without comparison; refuse other scopes with SCOPE_NOT_ALL; any team or region binding is a later versioned matrix change. |
| CDC-19567 | RWB-S8-E2036-APP | GAP-0960 | 12 | Resolve the subject on the service identity role and the NON_HUMAN_ACTOR class check; record caller code and type in the access entry; hold no copy of the list; per-caller rows only via a matrix version change. |

### RWB-S8-E7004-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19657 | RWB-S8-E7004-APP | DOR-RWB-S8-E7004-APP-18 | not located | Record open decision DL22 with assumptions ASM-1162, ASM-1304, ASM-2217 and ASM-2569 in the open decisions register |
| CDC-19659 | RWB-S8-E7004-APP | GAP-3057 | header | Add the plan rows for the consumed contracts, rule kit, access guard and outbox library; add DP-04, DP-05 and DP-09; publish the deviation state list of values. |
| CDC-19669 | RWB-S8-E7004-CON | DOR-RWB-S8-E7004-CON-10 | none (no screen section in the contract story) | Screen states belong to the app story; this contract story has no screen section. |
| CDC-19672 | RWB-S8-E7004-CON | GAP-3057 | 12.2 | Add plan rows for the five consumed contracts and one consumed event, the rule kit, outbox and inbox, access guard and state vocabulary; add DP-04, DP-05, DP-09 and DP-16 as the item states. |

### RWB-P2-E2033-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19546 | RWB-S8-E2033-APP | GAP-0661 | find it | Baseline the two read-only integration operations with columns, filters, order, paging envelope and problem body; declare the eight consumed operations; add the two paths to the Ownership Map. |
| CDC-19547 | RWB-S8-E2033-APP | GAP-0660 | find it | Fix the composed read and export paths on the integration base and the ageing, reference-data and access-log operations in the P3 and P4 contract stories, one hop each with a 2 s budget. |
| CDC-19548 | RWB-S8-E2033-APP | GAP-2224 | find it | Fix row and envelope names in v1, confirm page bounds and export limit as parameter rows with RWB-P3-E2011-APP, keep ageDays with ageInStateDays added, drop the duplicate timer index, name the login and flag owner. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19549 | RWB-S8-E2033-APP | GAP-3101 | find it | Add a read operation for rwb-deviation on the service base, add it to the consumed set of RWB-P2-E2033-CON at its next revision, and fix the path, field names and rwb-case page bound parameter. |
| CDC-19579 | RWB-S8-E7001-APP | GAP-1819 | 11 | Add S8 rows for the screening run, score, contact stop, agent feedback and breach record entity groups in rwb_deviation, as described in section 11 of RWB-S8-E7001-APP. |
| CDC-19590 | RWB-S8-E7001-CON | GAP-1819 |  | Add S8 rows for the shadow screening run, score row per code, contact stop, agent feedback row and breach record as entity groups with key fields. Name no new physical table beyond rwb_deviation. |

### RWB-S8-E7001-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19581 | RWB-S8-E7001-APP | GAP-3051 | 4, 16 | Record the rwb-document and rwb-source-data reads as C in fact with placeholders and fakes; keep the H, C, I and X rows as they stand. |
| CDC-19591 | RWB-S8-E7001-CON | GAP-3051 |  | Add the C rows for the rwb-document and rwb-source-data reads, adopt EV-06 and EV-07 on rwb.deviation.events.v1 with RWB-PLT-TE006-CON as outbox, treat the complaint service level as DL22 with the 10-working-day escalation, declare the stage clock pause as a stage outcome signal, and carry TC-E7-001-01 as the application half. |
| CDC-19592 | RWB-S8-E7001-CON | GAP-0464 |  | Agree the harness base hosts and fixture layout, fix synthetic keys and outcome codes as fixture data, pin the P5 documents answer as metadata only, set one evidence report per story and case_no, and set the gate as every owned criterion green with each hop owner or named stub. |

### RWB-S8-E7006-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19595 | RWB-S8-E7001-CON | GAP-3062 |  | Publish the X6 use of the deviation element, the three state values and the two event payloads. Declare the five consumed rows with placeholders and fakes. Record the absent trace element, agency read and service level as gaps. |
| CDC-19699 | RWB-S8-E7006-APP | DOR-RWB-S8-E7006-APP-21 |  | Move build status from Not started to Done. |
| CDC-19700 | RWB-S8-E7006-APP | DOR-RWB-S8-E7006-APP-23 | Header | State the contract version the app builds against for /api/recovery/deviation/v1. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19543 | RWB-S8-E2033-APP | CG-ALL-11388 | 14 | Add a message ID for the 2 s budget refusal (parameter or reference-data read unanswered inside budget, X5) so MSG-GEN-006 keeps its standard meaning; the story then cites it in section 14. |
| CDC-19558 | RWB-S8-E2036-APP | CG-ALL-11404 | 4, 14 | §14 MSG-GEN-006 row replaced by a placeholder per DOR-9 |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19580 | RWB-S8-E7001-APP | GAP-3102 |  | Publish element sets for DeviationRaised (EV-06) and DeviationCleared (EV-07), the facts JSON names and the placement refusal element; rwb-case owner declares the event-driven set and clear of recovery_case.deviation_open. |
| CDC-19665 | RWB-S8-E7004-CON | CG-ALL-11522 | 12.4 | Add rwb-deviation as a consumer of rwb.case.CaseStateChanged.v1 (EV-05), and add its ACL. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19585 | RWB-S8-E7001-APP | GAP-1830 | 15 | Add owner cell for SCR-06 and SCR-08 as gateway-bff composite routes and add a read operation for the deviation queue. Story section 15 now carries the confirmation step. |
| CDC-19689 | RWB-S8-E7005-APP | GAP-1821 | 13 | Add an rwb-integration or owning-service carrier and outside cell for Aric, NCB, EFS, LIT, SVAF and partner portal; add S8 integration operations; confirm identities with P2 before wave 4 |

### RWB-S8-E7002-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19598 | RWB-S8-E7002-APP | DOR-RWB-S8-E7002-APP-21 | header | Set build status to Done once the contract is published. |
| CDC-19606 | RWB-S8-E7002-APP | GAP-3054 | header | Publish the baseline with placeholders, bind error conditions to section 14 message IDs, declare the deviation element and the two shared operations once, confirm the names and EV-06 and EV-07. |

### RWB-S8-E7002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19604 | RWB-S8-E7002-APP | GAP-3053 | header | Record the four consumed rows as class C with placeholders, RWB-PLT-TE006-CON as wave 0 library, RWB-PLT-E1072-CON with RWB-P7-E1073-CON as kit; confirm owners. |
| CDC-19711 | RWB-S8-E7006-APP | GAP-0465 | 7 | Correct the AC2 rule citation to R-DEV-03, R-DEV-10 and R-DEV-19 on X2 when refreshed; R-DEV-17 stays with RWB-S8-E7006-APP. |

### RWB-S8-E7003-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19621 | RWB-S8-E7003-APP | DOR-RWB-S8-E7003-APP-21 | header | Set build status to Done (currently Not started) so the contract is published. |
| CDC-19622 | RWB-S8-E7003-APP | DOR-RWB-S8-E7003-APP-22 | header | Record the published contract fake library version; none is recorded in the sources. |

### RWB-S8-E7004-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19649 | RWB-S8-E7004-APP | DOR-RWB-S8-E7004-APP-21 | find it | Set build status to Done; it is currently Not started. |
| CDC-19660 | RWB-S8-E7004-APP | GAP-3058 | find it | Publish the baseline: placeholders for consumed operations, message IDs for errors, case boundary, event names, deviation state list, patch idempotency, tag date. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19662 | RWB-S8-E7004-CON | CG-ALL-11519 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story that holds the same capability as the dependency. |
| CDC-19664 | RWB-S8-E7004-CON | DOR-RWB-S8-E7004-CON-17 | header | Create story RWB-P7-E1073-CON or name the existing story for the Drools kit dependency, then name it in the header. |

### RWB-S8-E7005-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19676 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-21 | Header | Set build status to Done (currently Not started) and publish the contract. |
| CDC-19677 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-22 | Header | Publish a contract fake library version and record it as published. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19678 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-5 | 9 | Confirm DEV_FLAGGED is a DEVIATION state (TSD S8 T4), not a deviationCode value, and remove it from the closed list. |
| CDC-19701 | RWB-S8-E7006-APP | DOR-RWB-S8-E7006-APP-5 | 9 | Add DEV_WITH_OWNER to the closed lists LOV-DEVIATION and LOV-RAISED-BY. |

### RWB-S8-E7007-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19725 | RWB-S8-E7007-APP | DOR-RWB-S8-E7007-APP-21 | Header | Set build status to Done with the contract published. |
| CDC-19726 | RWB-S8-E7007-APP | DOR-RWB-S8-E7007-APP-22 | Header | Publish the contract fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19540 | RWB-S8-E2033-APP | CG-ALL-11387 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19542 | RWB-S8-E2033-APP | DOR-RWB-S8-E2033-APP-8 | 12.1, 12.2 | Publish GET deviation-flags in rwb-deviation.yaml and POST access authorise in rwb-access.yaml through the owners' CON stories. |

### RWB-P2-E2033-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19544 | RWB-S8-E2033-APP | DOR-RWB-S8-E2033-APP-11 | 11 | Reconcile the personal-data classification of the fields it carries with this story's statement that no personal data is carried. |

### RWB-PLT-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19550 | RWB-S8-E2033-APP | GAP-2320 | find it | Fix the session element list, the authorise branch and batch bound, and the extract record fields at baseline review; record the P2 attribution as a build-against dependency. |

### OTHER:Wave 2 release record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19551 | RWB-S8-E2033-APP | GAP-0415 | find it | Ratify the harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence format as one appendix before RWB-ITG-E2033-ITG claims Done. |

### OTHER:The plan (primary P2 for RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19553 | RWB-S8-E2033-APP | GAP-3187 | find it | Keep rwb-integration as primary for the four keys, as recommended; record the P3 tension for the assembly step. |

### RWB-P2-E2036-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19560 | RWB-S8-E2036-APP | GAP-0670 | 4 | Keep rwb-case placement path and behaviour; serve the admission and forwarding operation on the rwb-integration base; read approved callers via the rwb-case reference contract under rwb.casewf.placement.approved-callers; name the login in the DB story. |

### RWB-P2-E2036-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19561 | RWB-S8-E2036-APP | GAP-0671 | 12 | Declare the integration-base placement as provided with the four body fields, required Idempotency-Key and the legacy 201 shape; declare the case-base placement as consumed and owned by P3; mark consumed element names as placeholders until published. |

### OTHER:Wave 2 queue-placement harness pack and gateway-bff composite route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19563 | RWB-S8-E2036-APP | GAP-0419 | 16 | Agree composite route path and merge order with the platform edge story; fix harness repo, SIT environment, seeded callers and queues, evidence format, retention and pass/fail gate with QA at wave 2 entry. |

### parameter-catalog.csv; OTHER:RW-SECADM matrix version; RWB-P2-E2036-CON; RWB-ITG-E2036-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19564 | RWB-S8-E2036-APP | GAP-0735 | 7 | Hold the callers list as a parameter, the matrix version with RW-SECADM, the overflow shape and caller mapping in the contract, the login in the DB story and legacy criteria in RWB-ITG-E2036-ITG. |

### RWB-S8-E2036-APP; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case event-driven set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19568 | RWB-S8-E2036-APP | GAP-3102 | 4 | Publish the hold element (case reference, deviation reference, code, open count, handler, return point, contact-stop flag, rule version) additively in major version 1; rwb-case owner declares the set and clear of recovery_case.deviation_open; metadata rows unchanged. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; OTHER:the wave 2 CON stories for the P3 case read, the P4 authorise call and the reference-data contract; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; OTHER:the platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19569 | RWB-S8-E2036-APP | GAP-2412 | Header | Publish the placement fact element names on rwb.decision-record.v1 with key and envelope; publish the P3, P4 and reference-data shapes; add the MSG-P7-009 text; fix the per-service login name and secret store entry. |

### RWB-S8-E7001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19571 | RWB-S8-E7001-APP | DOR-RWB-S8-E7001-APP-21 | header | Set build status to Done before this story is ready to start; currently Not started. |

### OTHER:Recovery Workbench FSD S8 Deviation handling v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19577 | RWB-S8-E7001-APP | DOR-RWB-S8-E7001-APP-10 |  | Add empty, loading, error and no-access states for SCR-06 Raise deviation and SCR-08 Deviation queue; no source document states them. |

### OTHER:rwb-deviation contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19582 | RWB-S8-E7001-APP | GAP-3052 | 4, 14 | Story binds 400, 403, 422 and 503; 409 Not specified; message mapping removed |

### OTHER:FSD S8 A2.10.4.1 to A2.19.4.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19583 | RWB-S8-E7001-APP | GAP-1824 |  | Keep the placeholder rows visible and unchanged; write wave 4 criteria from the requirement when the E7 stories are groomed. |

### OTHER:Rule sets DEV and UNIVERSAL; OTHER:deviation data model; OTHER:rwb-access RW-CONDUCT (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19584 | RWB-S8-E7001-APP | GAP-3070 | 4 | Publish the contact-breach rule row, the breach column or record decision, the ledger and SCR-08 breach reads, the breach event decision, the RW-CONDUCT right and the service level. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19589 | RWB-S8-E7001-CON | GAP-1826 |  | Carry the twelve named R-DEV rules as the requirement set, name R-DEV-19, R-DEV-20 and R-DEV-21 from the design, and leave package authoring, version label and registry promotion to rwb-decision. |

### OTHER:Owners of the three consumed operation names, the SCR-08 read and the legacy test level (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19593 | RWB-S8-E7001-CON | GAP-3052 | 4, 14 | Event names are resolved from the catalog. Operation names, 401/404/409 messages, the SCR-08 read and the legacy test level remain Not specified until their owners confirm. |

### OTHER:Functional Specification S8 (A2.10.4 to A2.19.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19594 | RWB-S8-E7001-CON | GAP-1824 |  | Carry the placeholder criterion unchanged in the evidence column, and write wave 4 criteria from the requirement and rule when the E7 stories are groomed. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19597 | RWB-S8-E7001-CON | GAP-1830 | 15 | Add an owner cell and a gateway-bff composite route at the edge for SCR-06 and SCR-08 in the screen matrix, over rwb-deviation's contract; confirm the queue read with the platform edge owner before the wave 2 screen test. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:S8 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19603 | RWB-S8-E7002-APP | GAP-1821 | header | Add a P2 cell and an outside cell for EFS, carried by rwb-integration or the owning contract; confirm Aric, NCB, LIT and SVAF identities with P2 before wave 4. |

### OTHER:Recovery Workbench Gap Register v1 (folder 23, read-only this run) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19605 | RWB-S8-E7002-APP | GAP-0466 | find it | Close GAP-0466 by fixing the ITG harness environment, fixture, evidence format, retention and gate at the wave entry check, and hold the contact-limit values as P3 parameter data read from the fixture, never in code. Owner: QA lead with the Center of excellence. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19609 | RWB-S8-E7002-CON | DOR-RWB-S8-E7002-CON-12 | 16, 18 | Add rows for TC-E7-002-01 to -05 and TC-S8-E7002-CON-01 to -06 in Test Cases v8; align RTM v7 test lists to section 18. |

### RWB-S8-E7002-APP; OTHER:Recovery Workbench FSD S8 Deviation handling v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19610 | RWB-S8-E7002-CON | GAP-3053 | 8, 18 | Record four consumed rows as class C with placeholders, RWB-PLT-TE006-CON as wave 0, RWB-PLT-E1072-CON with RWB-P7-E1073-CON as kit, and confirm EFS carry and owners. |

### OTHER:TSD S8 Deviation handling v2 (T-A.2 and T5.3); OTHER:contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19611 | RWB-S8-E7002-CON | GAP-3054 | 11 | Bind each error condition to one section 14 message id, confirm the four operation names and the case event name and EV-06/EV-07 names, and record the tag date in the README. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON; OTHER:Template and Rules v1 DP rows; OTHER:connection matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19630 | RWB-S8-E7003-APP | GAP-3055 | find it | Record the four consumed rows as class C with placeholders; add DP-04, DP-09 and DP-10 rows; record the rule read, outbox library and workflow kit as tracked dependencies; settle the S8-to-P7 edge. |

### RWB-S8-E7003-CON; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19631 | RWB-S8-E7003-APP | GAP-3056 | find it | Publish the baseline with placeholders for the four consumed operations, the case event and the EV-06 and EV-07 names; bind errors to section 14 IDs; declare claim approval as an rwb-decision row; record the tag date. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19637 | RWB-S8-E7003-CON | CG-ALL-11480 | 12.7 | Record decision_record as a library object created in rwb_deviation, or give its dictionary name in LDM v9 or Data Classification v5. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19646 | RWB-S8-E7003-CON | GAP-3055 | find it | Add plan rows for rwb-source-data, rwb-case, rwb-access and rwb-decision as class C; add DP-04, DP-09 and DP-10; record RWB-PLT-TE006-CON and RWB-PLT-E1071-CON as tracked dependencies |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19656 | RWB-S8-E7004-APP | DOR-RWB-S8-E7004-APP-11 | 11 | Reconcile the personal-data flag of DF-CAS-038 to DF-CAS-045 (deviation fields in section 11) with the story statement 'No personal data' in section 11. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:15; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19671 | RWB-S8-E7004-CON | GAP-1821 | 12.2 | Name the carrier for the Aric, NCB, EFS, LIT and SVAF calls and the partner portal: add the P2 cell and an integration operation, each confirmed with P2 before the wave 4 test. |

### OTHER:TSD S8 (T3.2; OTHER:T-A.2); API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19673 | RWB-S8-E7004-CON | GAP-3058 | 12.2 | Publish the baseline with placeholders; settle the deviation state vocabulary and patch idempotency with data owners and the harness; bind error conditions to message IDs; record the tag date in the README. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19688 | RWB-S8-E7005-APP | DOR-RWB-S8-E7005-APP-8 | 12.1 | Align DeviationRaised.v1 and DeviationCleared.v1 payloads with this story; add validateDeviation and the other DeviationWorkflow activities to Temporal Catalog v1 |

### RWB-ITG-E7005-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19691 | RWB-S8-E7005-APP | GAP-0470 | 16 | Record SIT base hosts, fixture layout and synthetic keys, stub answer shapes, evidence format and retention, and the pass or fail gate at the wave 4 entry check. |

### Epic design record; OTHER:EP07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19692 | RWB-S8-E7005-CON | DOR-RWB-S8-E7005-CON-14 | 1 | Record the signed epic design sign-off for RWB-SVC-S8 under EP07; the story cannot attest it. |

### OTHER:rwb-deviation API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19702 | RWB-S8-E7006-APP | DOR-RWB-S8-E7006-APP-8 |  | Add an idempotency key to PATCH /deviations/{deviationId}. |

### RWB-S8-E7006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19715 | RWB-S8-E7006-CON | DOR-RWB-S8-E7006-CON-10 | find it | Add empty, loading, error and no-access states for SCR-06 and SCR-08 |

### OTHER:Split plan (H; OTHER:C; OTHER:I and X rows) and pattern register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19716 | RWB-S8-E7006-CON | GAP-3061 | 4 | Add plan rows for the four consumed contracts, declared class C with placeholders and fakes; record DP-05, DP-09, DP-14 and DP-20 as absent in the registers. |

### OTHER:TSD S8 (T-A.1; OTHER:T3.1) and DEV rule book (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19733 | RWB-S8-E7007-APP | GAP-3063 | 11 | Publish six consumed operation names and claim, appraisal and return-point properties; add RWB-PLT-TE006-CON to pattern set; record R-DEV-12 return point with reference to R-DEV-19 |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19734 | RWB-S8-E7007-APP | GAP-3064 | 12 | Publish DeviationOutcome and Deviation answer schema with required flags and return-point property; add six consumed operation names and RWB-PLT-TE006-CON outbox row |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19743 | RWB-S8-E7007-CON | CG-ALL-11618 | 12.5 | Add a row for activity recordCollateralOutcome (rwb-deviation, X7 outcome step) or name a catalogued activity instead |

### RWB-S8-E7007-APP; OTHER:SCR-06 and SCR-08) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19745 | RWB-S8-E7007-CON | DOR-RWB-S8-E7007-CON-10 | find it | Add empty, loading, error and no-access states for SCR-06 and SCR-08 |

### OTHER:Recovery Workbench pattern set and DEV rule book (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19747 | RWB-S8-E7007-CON | GAP-3063 | 11 | Add outbox library row RWB-PLT-TE006-CON to the pattern set; record R-DEV-12 against the X7 return point with reference to R-DEV-19. Fix six consumed operation names and claim, appraisal and return-point properties in wave 4 review. |

### OTHER:Technical Specification Design S8 (TSD S8 T-A.2 and T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19748 | RWB-S8-E7007-CON | GAP-3064 | 11 | Publish DeviationOutcome and Deviation answer schema with required flags and return-point property; add six consumed operation names from their owners; add the RWB-PLT-TE006-CON outbox library row to the pattern set. |

### OTHER:Wave 4 integration harness run fixture (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19749 | RWB-S8-E7007-CON | GAP-0472 | 16 | Agree at wave entry: SIT base host per service, one fixture file per case, synthetic case, asset, collateral and claim keys, S3 claim answer shape with claim id and status values, run-report schema and retention, and pass, stub pass or fail gate. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0415 | The SIT harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence format for the case-list journey are not specified in any source read | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0419 | Wave 2 queue-placement harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0464 | Harness environment and base hosts, fixture layout, synthetic keys, complaint outcome and reason codes, evidence-pack answer shape, evidence format and retention, and the pass or fail gate for the X1 dispute and complaint harness are not specified | Integration lead | Resolved (directive) |
| GAP-0465 | Legacy AC2 cites the X6 lost-contact rule R-DEV-17 on an X2 vulnerability and hardship case | Center of excellence with S8 rwb-deviation | Resolved (directive) |
| GAP-0466 | Harness environment, fixture, vulnerable-customer contact-limit values, evidence format and gate are not specified | QA lead with the Center of excellence | Resolved (directive) |
| GAP-0468 | Harness environment, fixture, insurer and estate answer shapes, heir-notification content, evidence format and gate are not published | QA lead with the integration lead | Resolved (directive) |
| GAP-0469 | X4 integration harness environment, fixture and evidence are unspecified | Integration lead | Resolved (directive) |
| GAP-0470 | Harness environment, fixture keys, stub answer shapes and pass or fail gate are not specified for the X5 integration run | Integration lead | Resolved (directive) |
| GAP-0471 | X6 integration harness environment, fixture layout, skip-trace answer shapes and evidence gate are not specified | Integration lead | Resolved (directive) |
| GAP-0472 | X7 collateral event integration harness: environment, base hosts, fixture layout, synthetic keys, insurance-claim answer shape, evidence format and retention, and pass/fail gate are not specified | Integration lead | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0670 | rwb-integration queue-write adapter: the operation owner, the login, the consumed contract field names and the replay window are not fixed by one source | Solution architect | Resolved (directive) |
| GAP-0671 | rwb-integration queue-write adapter contract: the ownership of the placement path, the consumed contract shapes and the library table columns are not fixed by one source | Tech lead | Resolved (directive) |
| GAP-0735 | The placement slice leaves the legacy AC allocation, the approved callers list, the production matrix grant, the overflow shape, the caller mapping and the login name unspecified | Tech lead | Resolved (directive) |
| GAP-0957 | rwb-access queue-write authority: the request and answer element set of the placement admission part of POST /authorise and of the non-human part of GET /me/permissions is named by no source | Solution architect | Resolved (directive) |
| GAP-0958 | rwb-access queue-write authority: the refusal reason code vocabulary and the status each code answers with are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0959 | rwb-access queue-write authority: no source binds a role to a list of teams or regions, so a scope narrower than ALL cannot be resolved for a non-human caller | Security administrator | Resolved (directive) |
| GAP-0960 | rwb-access queue-write authority: how a caller code is bound to a Workbench role, and whether a caller code is itself a role, is fixed by no source | Security administrator | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1820 | The FSD records an approver on a deviation while the S8 row has no rwb-decision cell and no approval workflow is named for this service | Solution architect with the S8 business analyst | Resolved (directive) |
| GAP-1821 | The FSD calls Aric, NCB, EFS, LIT, SVAF and the partner portal directly while the S8 row has neither an rwb-integration cell nor an outside cell | Solution architect with the integration lead | Resolved (directive) |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1824 | All ten E7 deviation features carry the placeholder criterion 'Written one epic ahead' and no alternate flow | Business analyst, S8 with the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1830 | The two deviation screens have no owner cell in the Architecture screen matrix and no recorded route at the edge | Solution architect | Resolved (directive) |
| GAP-2024 | Who pauses the stage clock when the stage runs as a child | Service owner P3 rwb-case with S8 rwb-deviation | Resolved (directive) |
| GAP-2224 | The case list is served twice in the target, and the row names, the bounds, the login and the flag mechanism of the owner's list have no source | Solution architect | Resolved (directive) |
| GAP-2320 | rwb-access answer behind the case and queue list: element names, the P2 attribution of the contract dependency, the authorise branch, the extract record, the login and the parameter and reference paths are not settled by any source read | Solution architect | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3051 | RWB-S8-E7001-APP: the X1 slice has no plan row for its two cross-service reads, no event names, no complaint service level and no published case-clock boundary, and its happy path has no acceptance criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3052 | RWB-S8-E7001-CON: the event names, the three consumed operation names, the status-to-message mapping, a read for SCR-08 and the test level of the legacy cases have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3053 | RWB-S8-E7002-APP: the X2 slice has no plan row for its four consumed contracts, its outbox library, its EFS touch, its requirement ids, its work-management owners or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3054 | RWB-S8-E7002-CON: the deviation element, the four consumed operation names, the event names, the two shared operations, the deviating read and the field-level types have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3055 | RWB-S8-E7003-APP: the X3 branch has no plan row for its four consumed contracts, its rule read, its outbox and its workflow, and no source names the claim reference, the heir notification or the escalation level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3056 | RWB-S8-E7003-CON: the consumed operation names, the case event name, the target event names, the claim approval and the lists of values of rwb-deviation have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3058 | RWB-S8-E7004-CON: the consumed operation names, the boundary signal, the event names, the state vocabulary and the patch idempotency of rwb-deviation have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3059 | Seven values of the X5 deviation have no source: the claim deadline, the Legal handler route, the case contract and its two event families, the platform outbox, the legal counsel's right, the requirement identifier and the sign-off | Solution architect | Resolved (directive) |
| GAP-3060 | Five shapes of the deviation contract have no source: the index set, the case announcement operation name, the outcome-to-state mapping, the outbox behind the two events and the unnamed 400 and 409 message text | Solution architect | Resolved (directive) |
| GAP-3061 | RWB-S8-E7006-APP: the X6 slice has no plan row for its consumed contracts, its skip-trace sources, its events, its agent dispatch, its 30-day clock or the deviation service level | Solution architect | Resolved (directive) |
| GAP-3062 | RWB-S8-E7006-CON: the skip-trace element, the consumed operation names, the agency read, the state vocabulary print and the deviation service level have no published baseline | Solution architect | Resolved (directive) |
| GAP-3063 | X7 collateral-event slice: consumed operation names, claim and re-appraisal answer shapes, event library row and the legacy AC3 rule condition are not published | Solution architect, TechX rwb-deviation tech lead, owners of rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3064 | X7 outcome contract: element properties beyond TSD S8 T3.1 and T-A.2, six consumed operation names and the outbox library row are not published | Solution architect, TechX rwb-deviation tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3070 | RWB-S8-E7010-APP: the contact-breach path has no rule row, no column, no published ledger read, no operation of its own, no event and no write right for its primary role | Center of excellence with the solution architect, the rwb-decision rule owner, the rwb-source-data owner and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3101 | rwb-deviation case and queue list slice: no read in the Ownership Map, no seam with the composed page, no path, field names or page bound, the flag derived twice and the pause projection without the rule package | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3102 | RWB-S8-E2036-APP: the deviation hold that the queue-write interface obeys has no published element names, no case-event names, no case-side setter for deviation_open and no placement-half criteria, and the pattern set adds dependencies the metadata rows do not carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
