# RWB-ITG-W1 Wave 1 integration - review pack, part 4 of 5 (RWB-ITG-E1052-ITG to RWB-ITG-E1065-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 217 |
| Cross-document (pending in another document) | 193 |
| Not applied (value not in the sources) | 18 |
| Open business decisions | 26 |
| Register gaps linked | 160 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E1052-ITG | 18 | 31 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1052 ITG Notice generation v1 - integration v2.md |
| RWB-ITG-E1054-ITG | 9 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1054 ITG Review queue for low-confidence documents - integration v2.md |
| RWB-ITG-E1055-ITG | 21 | 26 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1055 ITG Proof of delivery capture design with WIN - integration v2.md |
| RWB-ITG-E1057-ITG | 17 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1057 ITG Intake from branches, mailroom, partner SFTP and email - integration v2.md |
| RWB-ITG-E1058-ITG | 17 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1058 ITG Agent platform set-up [E1a] - integration v2.md |
| RWB-ITG-E1059-ITG | 15 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1059 ITG Case intake agent in shadow [E1b] - integration v2.md |
| RWB-ITG-E1060-ITG | 13 | 7 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1060 ITG Extraction evaluation [E1c] - integration v2.md |
| RWB-ITG-E1062-ITG | 20 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1062 ITG Deviation screening agent in shadow [E2b] - integration v2.md |
| RWB-ITG-E1063-ITG | 19 | 12 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1063 ITG Agent monitoring dashboard v1 [E2c] - integration v2.md |
| RWB-ITG-E1064-ITG | 24 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1064 ITG Data dictionary for the 14 data products - integration v2.md |
| RWB-ITG-E1065-ITG | 44 | 18 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1065 ITG Sandbox database with synthetic recovery data - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1062-ITG | R-00091 | CG-ALL-383 | Script gap | Product owner | The story adds PR1 to the closed list LOV-DEVIATION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1025-APP, RWB-P5-E1052-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-22159 | GAP-2347 | Register gap | Data steward and document type owner, with the Legal counsel and the P5 TechX squad | The notice-type to document-type mapping, the retention class and the write-once flag of each notice document type are not specified in any source read here | The document type load of RWB-P5-E1025-APP carries the DEMAND_LETTER and GUARANTOR_NOTICE rows with their class and flag, and the notice-type mapping row is added to the type or mapping table before the wave-1 test data is loaded |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-22191 | GAP-2245 | Register gap | Legal and the business lead | Whether a deviation pauses a statutory notice period is not settled by the sources | Keep the notice period unpaused as ASM-B2-P3-016-3 records; if Legal rules that it pauses, the deviation contract gains one signal to the notice clock and one criterion changes. |
| RWB-ITG-E1057-ITG, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P5-E1057-APP, RWB-P5-E1057-CON, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-S9-E1057-APP | R-22197 | GAP-3146 | Register gap | Business lead; solution architect; rwb-partner tech lead; rwb-access owner; programme lead | RWB-S9-E1057-APP: the split plan gives this secondary slice no legacy criterion and no build row while the P5 slice of the same key hands the partner criteria to it, no source publishes a partner-by-code read or the code filter of GET /partners, the two refusal reasons and the not-found behaviour are not published, the constraint on partner_code and the panel transition table are not specified, the DP-07 rows cannot be carried in an empty H row, and EP01 wave 1 is earlier than the service wave 4 | Serve the partner panel read as the code filter of the published GET /partners under base /api/recovery/partner/v1 with right R and the scope applied, answer the six published properties from partner in rwb_partner, answer an empty list for an unknown code and the stored panel status for a partner that is not ACTIVE, leave BR4 and the two reasons with the caller, read LOV-PANEL and LOV-PARTNER-TYPE through DP-07, write nothing and publish nothing, keep wave 1 and record the DP-07 rows, the constraint on the partner code, the panel transition table and the criteria assignment of the two slices as open items. |
| RWB-ITG-E1058-ITG, RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1058-INF, RWB-P10-E1058-OPS | R-22204 | GAP-1521 | Register gap | Business lead | The P10 message codes are referenced in the acceptance criteria but their wording is in no source document | The PRD refers to the codes and to the message that the source names, and states no wording. The wording is taken from the Error and Message Standard at build time; a code with no entry there is a defect of the message standard and not of this PRD. |
| RWB-ITG-E1058-ITG, RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1058-INF, RWB-P10-E1058-OPS | R-22205 | GAP-1522 | Register gap | Product owner | The FSD P10 requirement table is empty, so no FSD requirement ID exists to map a product requirement to | This PRD maps each FR to the FSD section and acceptance criteria it serves, and to the feature code where the FSD carries one. The FSD is asked to fill its Requirements served table in its next version; no requirement ID is invented here. |
| RWB-ITG-E1058-ITG, RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1058-INF, RWB-P10-E1058-OPS | R-22206 | GAP-1524 | Register gap | Compliance | No retention period is stated for an agent run, a guardrail result, a feedback row, an evaluation or a sample | The PRD requires that the record is retained for the period set for it, is answerable to audit before a purge and is never removed silently, and writes the value as the R9 placeholder until Compliance sets it in DL26. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1039-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22216 | GAP-2330 | Register gap | Internal audit role and the solution architect, P4 | The access entry of an agent read has no source row, element list or decision-code vocabulary of its own | Fix the entry members of a non-human read in the access-entry writer of RWB-P4-E1039-APP and publish them once for every service identity, so an audit query by agent code and policy version answers from the same chain as the screen entries. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22221 | GAP-2328 | Register gap | Compliance and PDPA officer and the security administrator role | Which of the run's fields are personal for a non-human actor, and the mask format served to an agent, are not specified | Fix the personal field list of the four agent reads and the mask format served to a non-human caller with the masking owner, load it as a masking version rather than as code, and prove it with a synthetic value that must appear in no answer, no log and no span. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1052-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-28611 | GAP-2088 | Register gap | Business lead with Legal and Compliance; document owner | DL10 is listed open with one answer and is recorded as answered with another | Keep the source row word for word, record in section 6.1 that DL10 is answered on 5 November 2026 with answer A, and add no Thai wording in this document. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-28627 | GAP-2248 | Register gap | Business lead | The role that receives the expiry of a notice period is not named | Take the escalation role from the SERVICE_LEVEL row in force as ASM-B2-P3-016-6 records, and add a named default role for a missing row if the business lead asks for one. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E1063-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P4-E1063-APP, RWB-P6-E1063-APP | R-28650 | GAP-1213 | Register gap | data steward, data product owner and architecture owner | REQ-DRI-009 still requires a daily copy to the data lake, which DP-17 and Arch v5 slide 37 remove | Reword REQ-DRI-009 in the next BRD version as the daily agent measures being available for reporting from rwb-reporting with the row counts matched against the P10 source, keep the requirement identifier, and record that the P6 slice carries only the cost-alert notification, as ASM-B-P6-05-E1063-6 sets out. |
| RWB-ITG-E1064-ITG, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P4-E1064-APP | R-28656 | GAP-2308 | Register gap | Compliance and PDPA officer | No source states how many of the 1,366 dictionary fields are personal, so the masking coverage the gate checks has no expected count | Publish the personal-field list of the 14 data products from the dictionary (is_personal true) and the masking pack coverage it must reach, so that the gate can fail a load that leaves a personal field uncovered and the SIT run can assert a count. Until then the gate asserts the rule per field ID and reports the count it finds. At D1 number this row GAP-nnnn and cite it from ASM-B2-P4-020-3. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E1054-ITG | R-03584 | DOR-RWB-ITG-E1054-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size is given in the sources. The Size row records it as Not specified and the item stays open. |
| RWB-ITG-E1054-ITG | R-14060 | DOR-RWB-ITG-E1054-ITG-15 | Header | Definition of Ready item 15 INVEST: Partial | Sized to fit row reads Not specified in the source documents. The INVEST line is outside this chunk. |
| RWB-ITG-E1054-ITG | R-23837 | CG-ALL-349 | 15 | SCR-30 has no empty, loading, error, no access state in the story | SCR-30 Loading comes from RWB E1 053 v7. Empty, Error and No access are in no source and read Not specified in the source documents (CG-ALL-349). |
| RWB-ITG-E1055-ITG | R-03588 | DOR-RWB-ITG-E1055-ITG-14 | 17 | Definition of Ready item 14 Epic design: Fail | No signed RWB-ITG-W1 epic design record found in the story or sources (grep of 04 User stories and _work/msr); a sign-off would be invented. |
| RWB-ITG-E1055-ITG | R-03589 | DOR-RWB-ITG-E1055-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the sources. The header Size row marks it Not specified; DoR item 16 stays open until the squad sizes the story at refinement. |
| RWB-ITG-E1055-ITG | R-03591 | DOR-RWB-ITG-E1055-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No published contract fake library version is in the sources. Section 12.8 marks the version Not specified, and the run uses the real services. |
| RWB-ITG-E1058-ITG | R-03600 | DOR-RWB-ITG-E1058-ITG-16 | Header | Definition of Ready item 16 Size: Fail | Size row reads Not specified in the source documents; no size is set, so the item stays open. |
| RWB-ITG-E1059-ITG | R-03605 | DOR-RWB-ITG-E1059-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is recorded in the source documents, so the Definition of Ready item stays open. |
| RWB-ITG-E1059-ITG | R-28555 | GAP-0610 | 5, 7, 12 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Login, route and AC5 are handled in the story. The P5 contract row point has no story change and stays open. |
| RWB-ITG-E1060-ITG | R-03611 | DOR-RWB-ITG-E1060-ITG-16 | find it | Definition of Ready item 16 Size: Fail | No size value is in the story or sources; the Size row reads Not specified in the source documents. The squad still has to size the story. |
| RWB-ITG-E1062-ITG | R-03615 | DOR-RWB-ITG-E1062-ITG-14 | header | Definition of Ready item 14 Epic design: Fail | No signed EP01 epic design found in any .md (searched for EP01 sign/approval). Ways of working v3 requires Business lead sign-off; it cannot be assumed. |
| RWB-ITG-E1062-ITG | R-14105 | DOR-RWB-ITG-E1062-ITG-18 | 19 | Definition of Ready item 18 Open decisions: Partial | Directive confirms ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL10 stays open. No story edit was made. |
| RWB-ITG-E1063-ITG | R-03624 | DOR-RWB-ITG-E1063-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size for RWB-ITG-E1063-ITG or RWB-E1-063 found in any source (searched outside 23 Document Gaps). The squad sizes it at refinement; any value would be invented. |
| RWB-ITG-E1063-ITG | R-03626 | DOR-RWB-ITG-E1063-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No published fake library version found in any source, including RWB-P10-E1063-CON 12.8 and Service Contract Catalog v1. A version would be invented. |
| RWB-ITG-E1063-ITG | R-14113 | DOR-RWB-ITG-E1063-ITG-18 | 8 | Definition of Ready item 18 Open decisions: Partial | Partly applied: BR3 and BR4 now cite DL25 and DL33 with their assumptions. DL10 has not been edited, so the item stays open. |
| RWB-ITG-E1064-ITG | R-03629 | DOR-RWB-ITG-E1064-ITG-16 | header | Definition of Ready item 16 Size: Fail | No source gives a size. The header Size row now reads Not specified in the source documents (DOR-RWB-ITG-E1064-ITG-16); the squad sets the size at refinement. |
| RWB-ITG-E1065-ITG | R-03633 | DOR-RWB-ITG-E1065-ITG-14 | 17 | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-ITG-W1 in the story or sources (grep of *.md for epic design/sign-off with RWB-ITG-W1). A sign-off can't be invented. |
| RWB-ITG-E1065-ITG | R-03634 | DOR-RWB-ITG-E1065-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value is in the sources, so the item stays open until the squad sizes the story at refinement. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00741 | RWB-ITG-E1052-ITG | CG-ALL-342 | 16 | Add rows TC-E1-052-11-ITG, TC-ITG-E1052-ITG-12, TC-ITG-E1052-ITG-13 and TC-ITG-E1052-ITG-14 with Given, When and Then from AC9, AC10, AC11 and AC12 |
| CDC-00744 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-12 | 16 | Add rows TC-E1-052-11-ITG, TC-ITG-E1052-ITG-12, TC-ITG-E1052-ITG-13 and TC-ITG-E1052-ITG-14 with Given, When and Then |
| CDC-00772 | RWB-ITG-E1054-ITG | CG-ALL-348 | 16 | Add a row for TC-ITG-E1054-ITG-20 in the next version, with Given, When and Then copied from AC16, BR6 and BR11. |
| CDC-00774 | RWB-ITG-E1054-ITG | DOR-RWB-ITG-E1054-ITG-12 | 16 | The story now lists TC-ITG-E1054-ITG-21 as well. TC-ITG-E1054-ITG-20 is missing from Test Cases v8, and the new TC-21 must also be added. |
| CDC-00788 | RWB-ITG-E1055-ITG | CG-ALL-353 | 16 | Add a row for TC-ITG-E1055-ITG-13 with Given, When and Then copied from AC13 in the next Test Cases version. |
| CDC-00812 | RWB-ITG-E1057-ITG | CG-ALL-361 | 16 | Add row TC-ITG-E1057-ITG-18 under Story test cases with Given, When and Then copied from AC16 of RWB-ITG-E1057-ITG. |
| CDC-00814 | RWB-ITG-E1057-ITG | DOR-RWB-ITG-E1057-ITG-12 | 16 | Add the test case row TC-ITG-E1057-ITG-18 (AC16, End to end) to Test Cases v8. |
| CDC-00826 | RWB-ITG-E1058-ITG | CG-ALL-367 | 16 | Add rows TC-ITG-E1058-ITG-17, -18 and -19 to the next Test Cases version, with Given, When and Then copied from AC17, AC18 and AC7 in section 7. |
| CDC-00846 | RWB-ITG-E1059-ITG | CG-ALL-376 | 16 | Story rows exist in section 16. Rows 15 to 20 added here also need the same Test Cases v8 entries. |
| CDC-00856 | RWB-ITG-E1060-ITG | CG-ALL-380 | 16 | Rows exist in section 16 of the story; Test Cases v8 needs the matching rows, also for TC-ITG-E1060-ITG-15 to 18 added in this edit. Owner role QA. |
| CDC-00864 | RWB-ITG-E1062-ITG | CG-ALL-386 | 16 | Add rows TC-ITG-E1062-ITG-11 to TC-ITG-E1062-ITG-15 under Story test cases, with Given, When and Then copied from AC10, AC11, AC12, AC14 and AC15. |
| CDC-00884 | RWB-ITG-E1063-ITG | CG-ALL-390 | 16 | Add TC-ITG-E1063-ITG-09 to -13 to Story test cases, with Given, When and Then copied from AC8, AC9, AC10, AC12 and AC13 |
| CDC-00896 | RWB-ITG-E1064-ITG | CG-ALL-394 | 16 | Add rows TC-ITG-E1064-ITG-10, -11, -12 and -13 with Given, When and Then copied from AC9, AC10, AC12 and AC13 of this story. |
| CDC-00915 | RWB-ITG-E1065-ITG | CG-ALL-420 | 16 | Section 16 lists eight TC-ITG rows (01 to 08); their Given, When and Then must be added to Test Cases v8 by QA. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00742 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-1 | 1 | Add QA integration engineer as a role code or name, or map section 1 to an existing role |
| CDC-00773 | RWB-ITG-E1054-ITG | DOR-RWB-ITG-E1054-ITG-1 | 1 | Add a role code or name for QA integration engineer with no service rights, matching the role row in section 5. |
| CDC-00789 | RWB-ITG-E1055-ITG | DOR-RWB-ITG-E1055-ITG-1 | 1 | Add a role code and name for the QA integration engineer on the wave 1 release, or name the existing role that runs the harness |
| CDC-00791 | RWB-ITG-E1055-ITG | DOR-RWB-ITG-E1055-ITG-6 | 10 | Add role SY-DATALOAD (data load) with the Litigation U operation rights stated in section 10 |
| CDC-00813 | RWB-ITG-E1057-ITG | DOR-RWB-ITG-E1057-ITG-1 | 1 | Add QA integration engineer as a role code or name, or map section 1 to the existing QA role there. |
| CDC-00827 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-1 | 1 | Add the role QA integration engineer to Users Roles and Permissions v5, or confirm the existing role that §1 should use. |
| CDC-00847 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-1 | 1 | Add the role 'QA integration engineer', or confirm its existing role code for the section 1 story role. |
| CDC-00857 | RWB-ITG-E1060-ITG | DOR-RWB-ITG-E1060-ITG-1 | 1 | Add the role 'QA integration engineer' to Users Roles and Permissions v5, or name an existing role in section 1. |
| CDC-00865 | RWB-ITG-E1062-ITG | DOR-RWB-ITG-E1062-ITG-1 | 1 | Add the role named in section 1 (QA integration engineer) as a role in Users Roles and Permissions v5, or align the story to the role code that document holds. |
| CDC-00882 | RWB-ITG-E1062-ITG | GAP-2329 |  | Scope value and non-human rule belong in the access matrix; the story records the assumption and refuses narrower scope. |
| CDC-00885 | RWB-ITG-E1063-ITG | DOR-RWB-ITG-E1063-ITG-1 | 1 | Add a role row for QA integration engineer with its role code, so section 1 can name that code |
| CDC-00897 | RWB-ITG-E1064-ITG | DOR-RWB-ITG-E1064-ITG-1 | 1 | Add the role QA integration engineer, or give the persona an existing role code in Users Roles and Permissions v5. |
| CDC-00916 | RWB-ITG-E1065-ITG | DOR-RWB-ITG-E1065-ITG-1 | 1 | Add 'tech lead' as a role code and name, or confirm an existing role; the section 1 role in the story must then match that document. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00804 | RWB-ITG-E1055-ITG | CG-ALL-354 | 18 | Align the test lists for the three requirements (REQ-OCC-003, REQ-ILG-004 and the third) to RWB-ITG-E1055-ITG section 18 in the next RTM version. |
| CDC-00832 | RWB-ITG-E1058-ITG | CG-ALL-368 | 18 | Align the test lists of REQ-ACA-010, REQ-ACA-005 and the third listed requirement with section 18 of RWB-ITG-E1058-ITG in the next RTM version. |
| CDC-00849 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-12 | 16, 18 | Align the §18 test lists with the §16 test cases TC-E1-059-01-ITG to TC-ITG-E1059-ITG-14. |
| CDC-00851 | RWB-ITG-E1059-ITG | CG-ALL-377 | 18 | Align the test case lists for REQ-ACA-005 and the second differing requirement with section 18 of RWB-ITG-E1059-ITG in the next RTM version. |
| CDC-00859 | RWB-ITG-E1060-ITG | CG-ALL-381 | 18 | Align REQ-DCM-005 and REQ-DCM-006 test lists in RTM v7 with section 18 of RWB-ITG-E1060-ITG in its next version. |
| CDC-00876 | RWB-ITG-E1062-ITG | CG-ALL-387 | 18 | Align the test lists for REQ-DVH-001, REQ-DVH-003 and REQ-DVH-007 with section 18 of this story in the next RTM version. |
| CDC-00893 | RWB-ITG-E1063-ITG | CG-ALL-391 | 18 | Align the REQ-DRI-009 test list in RTM v7 with the section 18 row of RWB-ITG-E1063-ITG in its next version |
| CDC-00906 | RWB-ITG-E1064-ITG | CG-ALL-395 | 18 | Align REQ-RDF-001 and the other differing requirement with section 18 in the next version of both. |
| CDC-00925 | RWB-ITG-E1065-ITG | CG-ALL-421 | 18 | Align the REQ-RDF-001 test list with section 18 of RWB-ITG-E1065-ITG (TC-E1-065-01-ITG, TC-E1-065-03-ITG, TC-E1-065-08-ITG, TC-ITG-E1065-01, TC-ITG-E1065-02) in the next version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00784 | RWB-ITG-E1055-ITG | CG-ALL-352 | 12.2 | Publish GET /api/recovery/source-data/v1/admin/data-quality/exceptions through the provider CON story, or the consumer switches to a published operation. |
| CDC-00786 | RWB-ITG-E1055-ITG | DOR-RWB-ITG-E1055-ITG-8 | 12.2 | Publish GET /api/recovery/source-data/v1/admin/data-quality/exceptions in the provider yaml, or consume a published operation. |
| CDC-00836 | RWB-ITG-E1059-ITG | CG-ALL-375 | 12.2 | Publish GET /api/recovery/source-data/v1/collateral/{id} in rwb-source-data.yaml through the provider's CON story, or the consumer switches to a published operation per provider ruling. |
| CDC-00840 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-8 | find it | Publish GET /api/recovery/source-data/v1/collateral/{id} in rwb-source-data.yaml, as for CG-ALL-375. |
| CDC-00910 | RWB-ITG-E1065-ITG | CG-ALL-417 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} through the provider's CON story, or the story consumes a published operation per the provider ruling. |
| CDC-00911 | RWB-ITG-E1065-ITG | CG-ALL-418 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the provider's CON story, or the story consumes a published operation per the provider ruling. |
| CDC-00913 | RWB-ITG-E1065-ITG | DOR-RWB-ITG-E1065-ITG-8 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} and GET /api/recovery/source-data/v1/accounts/{id} per the provider ruling. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00738 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-14 | header | Confirm the signed epic design sign-off and record it there |
| CDC-00769 | RWB-ITG-E1054-ITG | DOR-RWB-ITG-E1054-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-E1054-ITG against the epic design record. |
| CDC-00819 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-14 | Header | Record the signed epic design sign-off for RWB-ITG-W1 / EP01 so the story can cite it. |
| CDC-00837 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-E1059-ITG and confirm it against this story. |
| CDC-00853 | RWB-ITG-E1060-ITG | DOR-RWB-ITG-E1060-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-E1060-ITG in the epic design record. |
| CDC-00883 | RWB-ITG-E1063-ITG | DOR-RWB-ITG-E1063-ITG-14 | none | Confirm and record the signed sign-off of the epic design for RWB-ITG-W1, then cite that record in the story |

### API:(service not named) (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00752 | RWB-ITG-E1052-ITG | GAP-1082 | none | Publish NoticeRequest and Notice schemas with required flags, and the NoticeGenerated payload, and confirm them with the app stories of this key. |
| CDC-00795 | RWB-ITG-E1055-ITG | GAP-0577 | 12.2 | Publish GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= with the ten-field record and pod_key order; align the RWB-P6-E1055-CON row and fake at the wave 1 freeze. |
| CDC-00822 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-23 | 12.2 | Section 12.2 names API Specification v5 and /v1; the document version is marked Not specified. Confirm it from the info.version of the YAML files. |
| CDC-00852 | RWB-ITG-E1059-ITG | GAP-0611 | 12 | Publish a POST /agent-runs start operation beside GET /agent-runs/{id}; agree the four consumed read paths with the rwb-case and rwb-source-data owners; fix the member types. |
| CDC-00870 | RWB-ITG-E1062-ITG | GAP-2326 |  | Add a POST /authorise operation row with the agent-authority part and element names, confirmed at wave 1 review, kept inside RWB-P4-E1037-CON. |
| CDC-00873 | RWB-ITG-E1062-ITG | GAP-2327 |  | Define CALLER_KIND, RIGHT_NOT_HELD and SCOPE_NOT_ALL as authorise refusal reasons with their statuses, and confirm them for each caller service. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00808 | RWB-ITG-E1055-ITG | GAP-1105 | find it | Publish hold_reason as a versioned reference list with TEMPLATE_WITHDRAWN as the first row; add other values with the business owner. |
| CDC-00824 | RWB-ITG-E1058-ITG | CG-ALL-365 | Header | Record read_case as an allow-listed tool name of the agent policy, not a dictionary field; no LDM field added. |
| CDC-00825 | RWB-ITG-E1058-ITG | CG-ALL-366 | Header | Record propose_deviation as a refused tool name in the agent policy, not a dictionary field; no LDM field added. |
| CDC-00850 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-7 | 11 | Register the detcheck names read_case, read_accounts, read_contact_points, read_documents and the two further names as P10 contract tool identifiers, or record them as non-data names. |
| CDC-00914 | RWB-ITG-E1065-ITG | CG-ALL-415 | 13 | Record decision_record as a local object that each service's own baseline creates, per DP-03 (story line 362); the dependency stays with the services. |
| CDC-00924 | RWB-ITG-E1065-ITG | GAP-2251 |  | Confirm the field identifiers of queue, queue_member, assignment, task, timer, case_entry_exclusion and reference_version; the rwb-case login is set at RWB-PLT-NF06-DB. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00790 | RWB-ITG-E1055-ITG | DOR-RWB-ITG-E1055-ITG-12 | 12, 16, 18 | Add TC-ITG-E1055-ITG-13 to the Story test cases tab of Test Cases v8; align RTM v7 test lists with section 18 of this story |
| CDC-00829 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-12 | 16 | Add TC-ITG-E1058-ITG-17 to -24 to Test Cases v8; align the section 18 test lists of RWB-ITG-E1058-ITG with RTM v7 |
| CDC-00866 | RWB-ITG-E1062-ITG | DOR-RWB-ITG-E1062-ITG-12 | 16, 18 | Add TC-ITG-E1062-ITG-11 to -15 to Test Cases v8 story test cases; align RTM v7 test lists for RWB-ITG-E1062-ITG with section 18 of the story. |
| CDC-00886 | RWB-ITG-E1063-ITG | DOR-RWB-ITG-E1063-ITG-12 | 16, 18 | Test Cases: add TC-ITG-E1063-ITG-09 to -13 (see CG-ALL-390). RTM v7: align its test lists for RWB-ITG-E1063-ITG with section 18 |
| CDC-00899 | RWB-ITG-E1064-ITG | DOR-RWB-ITG-E1064-ITG-12 | 16, 18 | Add TC-ITG-E1064-ITG-10 to -13 to Test Cases v8; align the RTM v7 test lists to section 16 of this story |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00755 | RWB-ITG-E1052-ITG | GAP-2094 | find it | Keep the case-level list as a P6 operation, add GET /cases/{id}/notices with its settled path, and until then read a case's notices through GET /notices/{noticeId} per notice. |
| CDC-00799 | RWB-ITG-E1055-ITG | GAP-1101 | find it | ASM-0493 reads the barcode break (renumbered REC-09 under GAP-1169) through P1. The owner of REC-05 and of the References exception list belongs to the Ownership Map. |
| CDC-00869 | RWB-ITG-E1062-ITG | GAP-1819 |  | Add S8 table rows for shadow screening run, score per code, contact stop, agent feedback and breach record, keyed as the FSD requires. |

### RWB-P6-E1055-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00796 | RWB-ITG-E1055-ITG | GAP-1043 | 12.2 | Publish the notice read by notice ID and the dispatch reference as one operation with named fields, including the INT-14 document reference. |
| CDC-00798 | RWB-ITG-E1055-ITG | GAP-1100 | find it | Attach the WIN owner INT-14 and INT-15 specifications as versioned annexes; declare the file element a shape until then; treat a layout change as a new file version. |
| CDC-00802 | RWB-ITG-E1055-ITG | GAP-2243 | find it | Confirm the JSON element names of rwb.comms.NoticeDelivered.v1 and of the notice read at contract review; rename in this story only if they differ. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00830 | RWB-ITG-E1058-ITG | GAP-1520 |  | The base path and operation wording belong to the PRD. No story edit is needed for this item. |
| CDC-00831 | RWB-ITG-E1058-ITG | GAP-1528 |  | The read-only requirement is a PRD ruling. The story has no edit for this item. |
| CDC-00833 | RWB-ITG-E1058-ITG | GAP-1525 |  | The platform wave date belongs to the PRD. The header release date is not changed, per the rules. |

### RWB-P10-E1062-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00875 | RWB-ITG-E1062-ITG | GAP-0614 | 12.2 | Fix one run-start operation on /api/recovery/agent/v1 with its path, request members and refusal codes; name the read, event and outbox operations for case, parameters, deviations, ledger, documents and rule package. |
| CDC-00878 | RWB-ITG-E1062-ITG | GAP-1047 | 12.2 | State that the agent case read maps to API-P5-002 and the document read to API-P5-003, with API-P5-009 for an extracted-field filter; publish the tool call field names in the rwb-document AsyncAPI and OpenAPI documents. |
| CDC-00879 | RWB-ITG-E1062-ITG | GAP-1048 | 9 | Fix the DocumentStored payload as documentId, caseId, documentType, source and storedAt and state the idempotency key as the outbox event ID, in the rwb.document.events.v1 AsyncAPI document too. |

### RWB-ITG-E1052-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00739 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-16 | header | Size row added, reading Not specified in the source documents. |
| CDC-00745 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-15 | header | Size row reads Not specified in the source documents. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00750 | RWB-ITG-E1052-ITG | GAP-0749 | none | Field IDs for the seven recovery_case notice columns (notice reference, notice state, hold reason, template code and version, document reference, delivery date) and the notice timeline event codes in LOV-LEDGER-EVENT. Migration V1052_1 column names are not in the sources, so not applied here. |
| CDC-00764 | RWB-ITG-E1052-ITG | GAP-1087 |  | Add LOV-HOLD-REASON carrying POSTAL_ADDRESS, TEMPLATE_WITHDRAWN and any later value, read through the reference-data contract |

### 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00751 | RWB-ITG-E1052-ITG | GAP-1081 | 4 | Name the merge snapshot store (snapshot table or column on the local decision record) and publish it in the next physical-schema version. |
| CDC-00909 | RWB-ITG-E1064-ITG | GAP-1506 |  | Correct the seed before load: one data product per object family, physical types the views return, two personal view fields marked personal, wording 'ACE (ingested from X)', counts 16 and 14. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00767 | RWB-ITG-E1052-ITG | GAP-1083 |  | Record that the Litigation right and the notice scope test are enforced at the edge under RWB-PLT-N001-CON; add DP-08 and RWB-P4-E1037-CON only if the check moves into the service |
| CDC-00768 | RWB-ITG-E1052-ITG | GAP-2455 |  | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry, the producer local record is the working record and the ledger entry is the record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0 and wave-1 baseline outside the H row |

### RWB-P3-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00779 | RWB-ITG-E1054-ITG | GAP-0746 |  | Load the review task code, element type and task status values as reference data in the rwb-case reference tables before the review queue story starts. |
| CDC-00782 | RWB-ITG-E1054-ITG | GAP-0757 |  | Load the review task code, review states and case-side decision code as reference rows; allocate field IDs for document_ref, review_reason, item_version and review_state at the next data dictionary version. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00781 | RWB-ITG-E1054-ITG | GAP-0756 |  | Add the rwb-case review switch as a parameter key, name not specified in the source documents (GAP-0756), stored in the platform flag library; off raises no review task. |
| CDC-00891 | RWB-ITG-E1063-ITG | GAP-1209 | none | Publish request and answer fields of the two P6 operations; seed template code, channel, notice type and retry window as parameter rows; declare guard right of cost-alert notice read at gateway-bff (ASM-B-P6-05-E1063-4) |

### OTHER:FSD P5 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00783 | RWB-ITG-E1054-ITG | GAP-1593 |  | Replace the duplicated AC-P5-011-01 and AC-EXC-P5-011-01 to -08 with one distinct criterion asserting the correction feed to the labelled set. |
| CDC-00811 | RWB-ITG-E1057-ITG | GAP-1587 | 12.8 | Replace file-channel steps in AC-P5-013-01, AC-ALT-P5-013-01 and AC-ALT-P5-013-02 with the rwb-integration handoff; P5 records no file-system path. |

### RWB-P5-E1057-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00815 | RWB-ITG-E1057-ITG | GAP-1012 | find it | Publish the three admin operations and the run record; carry the channel property layout as environment values of RWB-P5-E1057-INF and RWB-P5-E1057-OPS. Story side: hold container named rwb-quarantine in §13 and TC-E1-057-10-ITG. |
| CDC-00817 | RWB-ITG-E1057-ITG | GAP-1013 | find it | Publish the three admin operations and the IntakeRun, IntakeRunChannel and IntakeRunPage resources as the smallest superset of the legacy job record, the six fakes and the drift test; keep unnamed elements behind the placeholder. |

### OTHER:Contract fake library (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00821 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-22 | 12.8 | Publish and record the contract fake library version for rwb-agent (P10), or keep the real SIT service as stated. |
| CDC-00855 | RWB-ITG-E1060-ITG | DOR-RWB-ITG-E1060-ITG-22 | find it | Record the published fake library version for the P5 and P10 contracts. |

### RWB-ITG-E1059-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00838 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-21 | header | Contract dependencies row reads Not specified in the source documents. |
| CDC-00839 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-22 |  | No fake library version or owning contract story is recorded in the source documents. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00844 | RWB-ITG-E1059-ITG | CG-ALL-373 | 1, 7 | Record read_documents as a tool operation in its owning document, or name the dictionary entity it reads. |
| CDC-00845 | RWB-ITG-E1059-ITG | CG-ALL-374 | 1, 7 | Record read_valuations as a tool operation in its owning document, or name the dictionary entity it reads. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00858 | RWB-ITG-E1060-ITG | DOR-RWB-ITG-E1060-ITG-12 | 16, 18 | Gap sits in Test Cases v8 and RTM v7; story section 16 holds the test cases, including those for AC15 to AC18. |
| CDC-00917 | RWB-ITG-E1065-ITG | DOR-RWB-ITG-E1065-ITG-12 | 16, 18 | Eight new test IDs (TC-ITG-E1065-01 to 08) are missing from Test Cases v8 and the section 18 lists differ from RTM v7. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00860 | RWB-ITG-E1062-ITG | CG-ALL-384 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's rwb-access CON story. |
| CDC-00863 | RWB-ITG-E1062-ITG | DOR-RWB-ITG-E1062-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's rwb-access CON story. |

### RWB-P1-E1064-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00901 | RWB-ITG-E1064-ITG | GAP-0499 | 12 | At baseline review, set required and nullable flags and string lengths of the five schemas; keep API specification property names and the rwb_source_data login (DP-02) |
| CDC-00905 | RWB-ITG-E1064-ITG | GAP-2309 |  | Publish the apply order: load owner moves the version after the gate passes, dictionary owner applies rows via its reference-table handler, gate answers decision and writes no row. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20857 | RWB-ITG-E1057-ITG | R-22194 |  | DMZ position and scan rate need owner confirmation; not in sources (GAP-1014). Target docx not readable in this run, so no exact text edit. |
| CDC-20858 | RWB-ITG-E1063-ITG | R-28649 |  | Job schedule and topics belong to Batch and Scheduling Design and Event and Messaging Design. Host, SKU, budget, alerts Not specified in the source documents (GAP-0618). |

### RWB-ITG-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00740 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-21 | header | Create contract story RWB-ITG-E1052-CON or confirm none is needed, then add its CON dependency to this story |

### OTHER:P3 screen specifications for SCR-01; OTHER:SCR-18 and SCR-30 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00743 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-10 | find it | Add empty, loading, error and no-access states to SCR-01, SCR-18 and SCR-30 |

### OTHER:P2 Criteria and test data story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00746 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-7 | 11 | Read ACE data through the P1 data-product contract, not the v_ace_* views |

### OTHER:P3 story holding MSG-P1-001 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00747 | RWB-ITG-E1052-ITG | DOR-RWB-ITG-E1052-ITG-9 | 14 | This story now uses the Error and Message Standard v4 wording (CG-ALL-341); the P3 entry still needs alignment. |

### RWB-P3-E1018-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00748 | RWB-ITG-E1052-ITG | GAP-1085 | 13 | Publish the rwb-case task-raise operation (or task-creating event) and record it in the ownership map |

### OTHER:TSD P6 v2 and legacy RWB-E1-052 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00749 | RWB-ITG-E1052-ITG | GAP-1084 | 11 | Settle DF-LEG-030 with the data steward: keep person_key as notice business key, give the party reference its own field ID, then correct the module specification or legacy list |

### OTHER:rwb-comms contract (API-P6-001) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00753 | RWB-ITG-E1052-ITG | GAP-1086 | none | Publish one error row per condition: withdrawn-template hold answered with notice in state Held, repeat with different key answered 409, missing field answered 422. |

### RWB-P6-E1052-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00754 | RWB-ITG-E1052-ITG | GAP-2454 | none | Fix the D7.1 generation record payload: template code and version and merge snapshot reference in inputs_ref, notice reference and type in actions, hold reason or refusal and freshness message in outcome, final-call set GENERATED, HELD, REFUSED. |

### RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00756 | RWB-ITG-E1052-ITG | GAP-1080 | find it | Publish the data-product record shape of DP01 Account and arrears and DP07 Legal, naming each returned field and its source column. |

### OTHER:Story map (Work Package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00757 | RWB-ITG-E1052-ITG | GAP-2351 | find it | Record RWB-P5-E1017-APP as sole owner of JOB-17; correct RWB-P5-E1055-APP and RWB-P5-E1065-APP section 12.6 at next version; record RWB-P5-E1052-APP as notice generation slice with no Schedule. |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00758 | RWB-ITG-E1052-ITG | GAP-2348 | find it | Name the request and reason fields of GenerateRequest and RegenerateRequest and the answer shape; RWB-PLT-DB fixes the logins; the document type load publishes the container, message text, index, step and flag. |

### OTHER:Recovery Workbench Notification and Correspondence Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00759 | RWB-ITG-E1052-ITG | GAP-2087 | find it | Name this document version 3; add a Source version row with 1 and 28 October 2026; the change log carries both readings. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00760 | RWB-ITG-E1052-ITG | GAP-0750 | find it | Reuse decision code D7.1 for the case-side record with template code and version, notice reference and business date, or agree a case-side code before build. |

### OTHER:TSD P3 v3 (case model task rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00761 | RWB-ITG-E1052-ITG | GAP-0751 | find it | Load request and hold task codes, element type HUMAN_TASK, discretion REQUIRED and status values as task rows through the reference-data contract; dedupe raises on case, task code and business date. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00762 | RWB-ITG-E1052-ITG | GAP-0752 | find it | Record P3 as a consumer of the P6 REST request POST /cases/{caseId}/notices inside a CaseWorkflow activity, or record the event-only variant if the review chooses it. |

### OTHER:Platform DB story (one login per service); parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00763 | RWB-ITG-E1052-ITG | GAP-0753 |  | Name the rwb-case login in the platform DB story; add the case-side notice switch as a parameter with default on, owner RW-COE. Key: Not specified in the source documents (GAP-0753) |

### OTHER:AsyncAPI document of rwb-comms (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00765 | RWB-ITG-E1052-ITG | GAP-1088 |  | Publish NoticeGenerated schema naming noticeId, caseId, templateId, templateVersion, noticeType and generatedAt; confirm with rwb-decision and rwb-reporting |

### OTHER:Split plan (work package entries for the RWB-E1-052 split) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00766 | RWB-ITG-E1052-ITG | GAP-2349 |  | Record one owning story per legacy criterion and mark secondary slices as test-case-bearing but criterion-free |

### OTHER:Wave 1 contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00770 | RWB-ITG-E1054-ITG | DOR-RWB-ITG-E1054-ITG-21 | Header | No published contract story for this suite is named in the sources. Header Contract dependencies stays None. |

### OTHER:Contract fake library (rwb-access, rwb-case, rwb-decision, rwb-document) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00771 | RWB-ITG-E1054-ITG | DOR-RWB-ITG-E1054-ITG-22 | 12.8 | Publish contract fakes for rwb-access, rwb-case, rwb-decision and rwb-document and record the published library version. |

### RWB-P3-E1035-CON; RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00775 | RWB-ITG-E1054-ITG | GAP-1010 | 13 | Publish the by-number case read on RWB-P3-E1035-CON; add the H row for the store of RWB-P5-E1024-APP; read the four review rows from document_hub_parameter in rwb_document; take role, team and scope from the cached permission decision until a P4 CON row exists; RWB-P5-E1054-CON fixes field names and message texts. |

### OTHER:rwb-document OpenAPI and AsyncAPI documents (wave 1 contract baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00776 | RWB-ITG-E1054-ITG | GAP-1011 | 13 | Freeze seven operations, nine resources, five value sets, one IntakeResolution envelope, the If-Match lock with idempotent repeat, the declared document read reference and the event schema; keep message texts and by-number path as placeholders until owners confirm. |

### OTHER:rwb-case parameters contract (DP-06; OTHER:DP-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00777 | RWB-ITG-E1054-ITG | GAP-0755 | 13 | Hold REVIEW_TEAM_UNATTACHED as a per-environment data row, with the team of each environment agreed by RW-COE; P5 keeps its own row for its screen; the queue reads the rwb-case row only. |

### OTHER:TSD P7 v2 and the reference-data contract of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00778 | RWB-ITG-E1054-ITG | GAP-2456 | 13 | Take review decision codes and final-call values from LOV-DECISION via the rwb-case reference-data contract; keep DOCATT; key actions and outcome as documentRef, reviewStatus, reviewOutcome, fieldCount; allocate the rwb_decision login in the platform secret store. |

### OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00780 | RWB-ITG-E1054-ITG | GAP-0988 |  | Publish the review-item authorise request and answer schema, the matrix and masking version labels with valid-from dates, and the review-field IDs for the masking pack. |

### OTHER:04 User stories / RWB-ITG-W1 Wave 1 integration story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00785 | RWB-ITG-E1055-ITG | DOR-RWB-ITG-E1055-ITG-21 | header | Create and publish contract story RWB-ITG-E1055-CON, then list it in this story's Contract dependencies row |

### OTHER:rwb-integration interface definition for the INT-14 WIN dispatch file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00787 | RWB-ITG-E1055-ITG | GAP-1602 | 12.8 | Publish the INT-14 WIN dispatch file layout as a versioned interface definition, held as a contract item before wave 2. Story side: build against the fake added to section 12.8. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00792 | RWB-ITG-E1055-ITG | GAP-2096 |  | Add EV-15 NoticeDelivered produced by rwb-comms; add a consumer row for the proof arrival read through P1 v_ace_pod on the ACE batch business date; add the matching job window row. |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00793 | RWB-ITG-E1055-ITG | GAP-1097 | 12.2 | Add the pod records, freshness and batch-status elements of the pod data product with business date, feed version, batch status and stale marker. |

### RWB-P5-E1054-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00794 | RWB-ITG-E1055-ITG | GAP-1099 | 12.2 | Name the document read that returns the stored letter of a notice and its claim-check handle; the consumed row and the fake follow from it. |

### OTHER:FSD P5 document type table (AC-ALT-P5-003-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00797 | RWB-ITG-E1055-ITG | GAP-1044 |  | Add a proof-of-delivery receipt type, or confirm which of the six types a receipt uses, with retention class and write-once flag; confirm DEMAND maps to DEMAND_LETTER. |

### RWB-P6-E1055-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00800 | RWB-ITG-E1055-ITG | GAP-1102 | find it | Record WIN host, port, zone, certificate subject and owner, container names, retention and sizes as reviewed per-environment values; confirm with WIN owner and Security before SIT cutover. |

### RWB-P6-E1055-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00801 | RWB-ITG-E1055-ITG | GAP-1103 | find it | Fix the deployment slot and namespace under DL35 with the platform team, name the Schedule, record the Airflow window call in the runbook, and assert both in the registration step. |

### OTHER:rwb-comms API document (API-P6-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00803 | RWB-ITG-E1055-ITG | GAP-1098 | find it | Record that the declared Litigation area and right R are enforced at gateway-bff on the screen path, and either add RWB-P4-E1037-CON as a C dependency of RWB-P6-E1055-APP or state that a service identity call carries no user right. |

### OTHER:Functional Specification P5 (A2, proof of delivery) and Technical Specification P5 (field_definitions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00805 | RWB-ITG-E1055-ITG | GAP-1045 | find it | Name barcode, callback date, delivery status and sent type as the four receipt field_definitions; state whether a receipt is one document per file or per notice. |

### OTHER:Message catalogue (P5 entries) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00806 | RWB-ITG-E1055-ITG | GAP-1046 | find it | Add the text of MSG-P5-016 for a file that fails the malware scan, so the 422 refusal shows a written message. |

### OTHER:rwb-comms values files and the runbook entries (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00807 | RWB-ITG-E1055-ITG | GAP-1104 | find it | Set the alert thresholds, the late-batch reviewed time and the Schedule state per environment; confirm at UAT and record each value in its runbook entry. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00809 | RWB-ITG-E1055-ITG | GAP-2246 | find it | Allocate the Data Dictionary field ID for the nullable notice reference column on timer, with its index, at the next revision. |

### RWB-S9-E1057-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00810 | RWB-ITG-E1057-ITG | GAP-1843 | 12.8 | The wave placement of S9 is fixed in the plan and the S9 stories. This suite reads panel_status through S9 on wave 1 contracts, so no story edit is made here. |

### OTHER:SIT environment configuration of the deployment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00816 | RWB-ITG-E1057-ITG | GAP-1014 | find it | Confirm the channel inventory, the DMZ position of the partner gateway and the scan rate with network and security owners before wave 1 release; provision scan capacity around RWB-P5-E1041-APP. |

### RWB-P5-E1057-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00818 | RWB-ITG-E1057-ITG | GAP-1015 | 12.6 | Add the channel pickup deployment: per-environment values and four channel blocks, chart keys, trigger ID and catch-up, alert thresholds, four alerts, runbook entries; unsourced values as placeholders. |

### OTHER:Story backlog workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00820 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-21 | Header | The header names the contract dependencies; their publication, and the P4 authorise contract ID, are not settled by this story. |

### OTHER:FSD P10 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00823 | RWB-ITG-E1058-ITG | GAP-1518 | 12.8 | Remove ACE from the agent integration points in A2.1.2 and A2.10.2; read case facts through rwb-source-data per Architecture v5 slides 9 and 16 and ADR-010. |

### OTHER:RWB-P3 story for SCR-46 (rwb-case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00828 | RWB-ITG-E1058-ITG | DOR-RWB-ITG-E1058-ITG-10 | 18 | Add empty, loading, error and no access states of SCR-46 to the P3 story |

### OTHER:Recovery Workbench PRD (agent features; OTHER:P10) and FSD P10 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00834 | RWB-ITG-E1058-ITG | GAP-1530 |  | Story text does not repeat the four-feature criteria; the fix belongs in the PRD and FSD, so this story is not edited. |

### OTHER:FSD P10 v3 (A1.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00835 | RWB-ITG-E1058-ITG | GAP-1533 |  | This story already states Wave 1 and its tentative release date; the missing wave is in the FSD agent features, not in this story. |

### OTHER:Not specified in the source documents (CG-ALL-370) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00841 | RWB-ITG-E1059-ITG | CG-ALL-370 | find it | Record read_case as an agent tool identifier in the owning document's tool list, since it is not an LDM v9 or Data Classification v5 name. |

### OTHER:Not specified in the source documents (CG-ALL-371) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00842 | RWB-ITG-E1059-ITG | CG-ALL-371 | find it | Record read_accounts as an agent tool identifier in the owning document's tool list, since it is not an LDM v9 or Data Classification v5 name. |

### OTHER:Not specified in the source documents (CG-ALL-372) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00843 | RWB-ITG-E1059-ITG | CG-ALL-372 | find it | Record read_contact_points as an agent tool identifier in the owning document's tool list, since it is not an LDM v9 or Data Classification v5 name. |

### OTHER:rwb-case story (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00848 | RWB-ITG-E1059-ITG | DOR-RWB-ITG-E1059-ITG-10 | 12 | Add the empty, loading, error and no-access states of SCR-46 to the P3 story. |

### RWB-ITG-E1060-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00854 | RWB-ITG-E1060-ITG | DOR-RWB-ITG-E1060-ITG-21 | find it | Publish contract story RWB-ITG-E1060-CON and name it as the contract dependency of this story. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00861 | RWB-ITG-E1062-ITG | CG-ALL-385 | 13 | Create the story file RWB-P7-E1073-CON, or name the existing rwb-decision contract story in place of it. |

### OTHER:22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00862 | RWB-ITG-E1062-ITG | DOR-RWB-ITG-E1062-ITG-17 | header | Row DP-04 (line 129): replace consumer key RWB-P7-E1073-CON, which does not exist, with RWB-P7-E1073-APP. Track the 4 APP dependencies to Done. |

### OTHER:Recovery Workbench BRD (Epic 1, section 8.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00867 | RWB-ITG-E1062-ITG | GAP-1456 |  | State in section 8.2 that the business-epic wave is kept and that the delivery lead confirms the wave per story at build sequencing. |

### RWB-S8-E1062-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00868 | RWB-ITG-E1062-ITG | GAP-1823 |  | Rewrite the FSD E2 criteria with the S8 owner so each row is one criterion, and add a step criterion for pause, stop, routing and clear. |

### OTHER:TSD P10 v2 (T-A.1; RWB-P10-E1062-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00871 | RWB-ITG-E1062-ITG | GAP-0615 | 12 | Fix one run-start and one run-read operation on the agent base; declare three event payloads from T3.1; mark the three unsourced consumed paths with the placeholder. |

### OTHER:FSD P10 v3 A2.8.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00872 | RWB-ITG-E1062-ITG | GAP-1532 |  | Retitle A2.8 and its intent to the shadow mode of Epic 1; read the mode from the policy row so one code path serves both runs. |

### RWB-S8-E1062-APP; RWB-P10-E1062-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00874 | RWB-ITG-E1062-ITG | GAP-3085 |  | Publish the deviation read and agent-policy read operations, the R-DEV-05 and R-DEV-06 owner codes, the answer limit parameter and the test level split across the three stories. |

### OTHER:FSD S8 (FSD v6 extract folder) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00877 | RWB-ITG-E1062-ITG | GAP-1834 |  | Add the v1 and v2 change-note rows to the S8 version history once the folder is completed; until then carry them as not specified. |

### OTHER:rwb-access masking contract (P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00880 | RWB-ITG-E1062-ITG | GAP-1049 | 9 | Publish the mask format, the per-role personal field list and the SY-AGENT policy version label; state SY-AGENT holds Documents R with every personal field masked and no clear value in answer, log or trace. |

### OTHER:TSD P5 (rwb-document contract) T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00881 | RWB-ITG-E1062-ITG | GAP-1050 | 9 | State that a stored document is served with the type on its row and never re-typed on read, and that the 422 and MSG-P5-006 refusal applies at store time only. |

### OTHER:Extraction evaluation story of rwb-agent (legacy RWB-E1-060) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00887 | RWB-ITG-E1063-ITG | GAP-0644 | 12 | Name the login the rwb-agent login (DP-02); read LOV-DOC-TYPE from the rwb-case reference-data contract; keep the three legacy admin operations on /api/recovery/agent/v1 and leave the report and configuration operations with RWB-P10-E1058-APP; route the reads through gateway-bff on the same admin path; read scores only through the evaluation read. |

### OTHER:Agent monitoring dashboard v2 app slice (legacy RWB-E2-031) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00888 | RWB-ITG-E1063-ITG | GAP-0629 | None in story | Apply the nine fixes of the item: drift step in the v1 Schedule workflow, segment read from the run row, override figures through the rwb-decision contract with the agent-version filter and three additive elements, notice path by its owner, policy values in watch_measures, migration V10_007, range limits as configuration, login the rwb-agent login (DP-02), route under RWB-PLT-N001-CON, and the API-P10-009 right as the proposed fix states. |

### OTHER:rwb-agent agent-monitoring contract (API-P10-009; OTHER:P10 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00889 | RWB-ITG-E1063-ITG | GAP-0617 | 12 | Fix the read on /api/recovery/agent/v1 with the five query parameters, a declared page size and cursor, the aggregate element with the legacy figures, and the held-date status with business date, run state and previous published date. Do not adopt the Temporal Schedule: keep JOB-15 as the Airflow trigger of Arch v5 slide 44. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00890 | RWB-ITG-E1063-ITG | GAP-2332 | None in story | Publish the two access-event codes, the entry field list and the page bounds with the next access-log contract version; name the read index in the physical schema of rwb_access; register the one Flyway step of DP-15 and the two parameter codes in the service's own sequence and parameter set. |

### OTHER:FSD P4 v3 and TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00892 | RWB-ITG-E1063-ITG | GAP-2333 | none | Correct REQ-ACA-006 and NFR-042 to the served access entry; record Reporting letters of other roles in the matrix load; keep both rights and access event names as they stand |

### OTHER:Platform deployment configuration for rwb-agent (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00894 | RWB-ITG-E1063-ITG | GAP-0618 | none | Expose topology values as chart values; register AgentRunDailyRollup at 01:30 on queue rwb-agent with overlap SKIP; provision rwb.agent.events.v1 with retry and .dlt topics; publish the metric read behind gateway-bff |

### OTHER:TSD P4 v3 T6.1 (RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00895 | RWB-ITG-E1064-ITG | GAP-2307 | 4 | Add an A letter in Reference data to one role in the next matrix version, name that role as approver of reference and dictionary loads, and forbid the same role submitting and approving. |

### OTHER:P3 screen specification for SCR-40 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00898 | RWB-ITG-E1064-ITG | DOR-RWB-ITG-E1064-ITG-10 | 9 | Add empty, loading, error and no-access states for SCR-40 to the screen specification. |

### OTHER:rwb-case API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00900 | RWB-ITG-E1064-ITG | GAP-0498 | 13 | DP-07 list read marked Not specified (GAP-0498) |

### RWB-P4-E1064-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00902 | RWB-ITG-E1064-ITG | GAP-0890 | 12 | Keep register read GET /admin/dictionary-authority, its answer fields and markers masked/clear; confirm with data steward and P1 dictionary owner before wave 1 baseline |

### OTHER:TSD P4 v3 T6.1 role matrix (SIT and production) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00903 | RWB-ITG-E1064-ITG | GAP-0891 |  | Give one role the Reference data A letter and record which role approves a governance load of the authority tables; the approver is a matrix row, not a code constant. |

### RWB-P1-E1064-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00904 | RWB-ITG-E1064-ITG | GAP-2306 |  | Publish the register path, query parameters, answer schema and marker vocabulary (masked, clear), and the coded check names of MSG-P1-002. |

### OTHER:Work Package plan for RWB-E1-064 (B-P1-02; OTHER:B2-P1-001) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00907 | RWB-ITG-E1064-ITG | GAP-2161 |  | Keep one WP per story slice: remove RWB-E1-064 from B-P1-02 fanout or retire B2-P1-001 for this key; number CG-B-P1-02-E1064-101, -201, -301 once; add a plan-uniqueness check on 'Write only' paths in checks/run_all.py. |

### OTHER:rwb-source-data chart values file for each environment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00908 | RWB-ITG-E1064-ITG | GAP-0500 | 12 | Carry replica count, resource size, probe path and timing, alert threshold, window and incident route as chart values set per environment by the platform team; none hard-coded. |

### RWB-P1-E1065-APP; RWB-P3-E1065-APP; RWB-P4-E1065-APP; RWB-P5-E1065-APP; RWB-S8-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00912 | RWB-ITG-E1065-ITG | DOR-RWB-ITG-E1065-ITG-17 | header | Reach build done before this story starts; their build status is outside this story. |

### RWB-P4-E1022-APP; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00918 | RWB-ITG-E1065-ITG | GAP-0896 | 13 | State in the sign-in story that the identity resolves to role.entra_group rows only; fix the synthetic key format in the Service Template Specification; record the retirement rule with DL39. |

### RWB-P1-E1065-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00919 | RWB-ITG-E1065-ITG | GAP-3086 | 3 | Publish the deviation seed profile, the deviation count per case and shape-to-code mapping, the stage contract read names, the R-DEV-05/06 codes and owner roles, and the test level of the ten legacy cases. |

### OTHER:TSD P4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00920 | RWB-ITG-E1065-ITG | GAP-0900 | 3 | Extend the T6.1 RBAC matrix to the 14 capability areas of LOV-CAPABILITY and publish the full matrix version with RWB-P4-AD002-APP. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00921 | RWB-ITG-E1065-ITG | GAP-0895 | 3 | Fix the access seed file path, format, owner, version label and row count as a migration resource, and state whether the DEV seed carries the SIT matrix version. |

### OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00922 | RWB-ITG-E1065-ITG | GAP-0898 | 3 | Add POST /authorise and GET /me/permissions with request and answer schemas, stub them in the contract fake, and publish the SCR-43 composite route with gateway-bff (DP-19). |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00923 | RWB-ITG-E1065-ITG | GAP-2252 |  | Confirm the decision code for the seeded creation (RWB-P3-E1018-APP) and for the seeded exclusion (RWB-P3-E1019-APP or the exclusion rule) at the decision-record contract review. |

### OTHER:Work Package plan for rwb-source-data (B-P1-02; OTHER:B2-P1-001) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00926 | RWB-ITG-E1065-ITG | GAP-2161 |  | Remove RWB-E1-064 from B-P1-02 fanout or retire B2-P1-001 for this key; number CG-B-P1-02-E1064-101, -201 and -301 once; add a plan-uniqueness check on Write only paths. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00927 | RWB-ITG-E1065-ITG | GAP-1053 | 7 | Record the DEV storage account and container names, the rwb-document login and the DEV read-only role name; publish the SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20636 | RWB-ITG-E1063-ITG | R-22225 |  | Five query parameters already on /admin/agent-metrics. Page size, cursor, aggregate and held-date status not specified in the source documents (GAP-0617). JOB-15 kept. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0364 | Cross-service notice path, merge snapshot home and stale-batch signal are not named for the target | Tech lead | Resolved (directive) |
| GAP-0365 | Review queue operation names, scope source and attach evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0366 | WIN file path, proof-of-delivery read and interaction ledger home move in the target | Tech lead | Resolved (directive) |
| GAP-0367 | Partner eligibility, channel configuration and job monitoring move in the target | Tech lead | Resolved (directive) |
| GAP-0368 | Model endpoint path, masking route and agent run evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0369 | Stale-input signal, tool-path ownership and shadow-output exposure are not named for the target | P10 agent owner, P1 source data owner, P3 case owner, P4 access owner and P5 document owner | Resolved (directive) |
| GAP-0370 | Document-type reference data owner, extraction field reads and the proposal column are not named for the target | P10 agent owner, P5 document owner and P3 case owner | Resolved (directive) |
| GAP-0371 | Rule-row owner lookup, interaction ledger read and deviation-absence evidence are not named for the target | P10 agent owner, P7 decision owner, P1 source data owner, S8 deviation owner and P4 access owner | Resolved (directive) |
| GAP-0372 | Data lake removed: agent daily read model, reporting read and job rerun owner are not named for the target | P10 agent owner, P9 reporting owner, P1 source data owner, P6 comms owner and P2 integration owner | Resolved (directive) |
| GAP-0373 | Reference-load operation owner, ACE view value read and contract confirmation form are not named for the target | P1 source data owner, P3 case owner and P4 access owner | Resolved (directive) |
| GAP-0374 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | Solution architect | Resolved (directive) |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0498 | The read of the rwb-case reference-data contract that returns a table of values is not specified | Solution architect | Resolved (directive) |
| GAP-0499 | The field-level detail of the five dictionary schemas and the login wording of the contract baseline are not specified | Tech lead | Resolved (directive) |
| GAP-0500 | No deployment value, probe timing, alert threshold or incident route exists for the dictionary slice | DevOps lead | Resolved (directive) |
| GAP-0501 | The sandbox scope per service and the placement of the generator module are not specified | Solution architect | Resolved (directive) |
| GAP-0502 | The contract of a build tool is not described by any source document | Tech lead | Resolved (directive) |
| GAP-0503 | The sandbox database scope and its read-only role name are not specified | ACE data architect | Resolved (directive) |
| GAP-0577 | The address, the answer envelope and the paging of the proof-of-delivery read of rwb-source-data are not fixed by any source: the sources name a data-product records path, the contract of this key names another, and no source names the page parameters, the element types or the error set | Solution architect | Resolved (directive) |
| GAP-0578 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Solution architect | Resolved (directive) |
| GAP-0579 | No source names what the proof-of-delivery read answers before RWB-ACE-001 deploys the Section B views, nor the flag that holds it: the sources require the feature to stay behind a flag and the product to show stale, and give neither the answer shape, the reason code nor the flag name | Solution architect | Resolved (directive) |
| GAP-0580 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | Data architect | Resolved (directive) |
| GAP-0581 | No source fixes the render of MSG-P1-001 for the WIN proof of delivery: the legacy story names the product 'DP07 Legal', the FSD names the ACE batch and the product code, and the date is either the last complete business date or the due date | Business analyst | Resolved (directive) |
| GAP-0606 | The app slice of the agent platform set-up: the service login, the tool reads of the two owners, the parameter keys and lists, the sample key, the migration numbering and the route in front of the admin reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-case, rwb-document and rwb-access | Resolved (directive) |
| GAP-0607 | The contract baseline of the agent platform: the event family beyond EV-28, the member types of the report and the metrics, the inputs reference of the record, the sample key and the assignment of agent_run_daily are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0608 | The infrastructure slice of the agent platform: the INT-23 host, port, certificate and Key Vault entry names, the login name, the partition and retention values, the worker concurrency, the budget measurement points and the alarm thresholds are not specified by any source | SCB IT infrastructure with the ACE platform team and security | Resolved (directive) |
| GAP-0609 | The deployment slice of the agent platform: the replica, resource, probe and rollout values, the alert thresholds, the ordering of the later migrations and the blue-green mechanism of the admin path are not specified by any source | DevOps team with the ACE platform team and the owner of rwb-agent | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0611 | Open points of the intake run contract: the start path, four consumed read paths and the field-level members | Tech lead and platform architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0613 | Intake agent evaluation contract: name of an evaluation-completed event, nested types of the promotion members, type detail of the report members and the route path in front of the operations | Tech lead of rwb-agent, with the solution architect and the platform library owner | Resolved (directive) |
| GAP-0614 | The screening slice in rwb-agent: the run-start path, the parameter and ledger operation paths, the two added events, the screening feature flag, the boundary status of a failed tool call and the route in front of the reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-deviation, rwb-case, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0615 | The screening contract slice: the run-start path and request members, the member types of the proposal payload, the two added event names and payloads, the consumed paths no source names and the route name are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0616 | Agent monitoring dashboard in rwb-agent: the data lake of the legacy story is removed, and the schedule name, the service login, the route path, the notification operation and the home of the daily aggregate are not specified | Solution architect | Resolved (directive) |
| GAP-0617 | Agent monitoring contract in rwb-agent: the page size and cursor, the member types of the aggregate element, the held-date status members, the Schedule name, the route path and the notification operation are not specified | Solution architect | Resolved (directive) |
| GAP-0618 | Agent monitoring deployment in rwb-agent: the topology, host, SKU, budget, route path, login, feed retention and alert thresholds are not specified | Platform administrator | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0644 | Extraction evaluation in rwb-agent: service login, document-type owner, admin operation set, route path and score read path | Solution architect | Resolved (directive) |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0749 | No field IDs for the notice facts on recovery_case, and no event code list for the notice timeline entries | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0750 | The decision code and the final call of the case-side notice record are only partly specified | RW-COE | Resolved (directive) |
| GAP-0751 | The task model values of the request task and of the task Complete notice data are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0752 | Architecture v5 gives P3 as a listener of P6, while the P6 contract accepts a REST notice request | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0753 | The per-service login name and the case-side feature switch key are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0755 | Review team for a review item with no case: the legacy value is assumed and the parameter has no agreed owner | RW-COE | Resolved (directive) |
| GAP-0756 | The rwb-case feature switch of the review queue has no name in any source | RW-COE | Resolved (directive) |
| GAP-0757 | The review task code, the review state values, the case-side decision code and the field IDs of the review link columns are not specified | RW-COE | Resolved (directive) |
| GAP-0758 | The rwb-case per-service login name is not specified | RW-SECADM | Resolved (directive) |
| GAP-0890 | The register operations, their field names, the marker vocabulary and the read path are not in the sources | Solution architect, with the data steward | Resolved (directive) |
| GAP-0891 | No role holds the Reference data A letter that API-P4-006 requires of an approver | Security administrator, with the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0892 | The number of personal fields among the 1,366 is not stated | Data steward | Resolved (directive) |
| GAP-0893 | The apply path of an approved governance load is not assigned | Solution architect, with the reference data administrator | Resolved (directive) |
| GAP-0895 | rwb-access sandbox seed: the access seed file's location, format, version label and row count are not specified, and whether the DEV matrix version must equal the SIT version is not stated | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0897 | rwb-access sandbox seed: the per-service login name and the DEV-only read-only role over rwb_access are not fixed for the target schema | Platform DB owner | Resolved (directive) |
| GAP-0898 | rwb-access sandbox seed: the authorise and me/permissions request and answer shapes, and the screen route that shows the seeded rows, are absent from the TSD appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0899 | rwb-access sandbox seed: the legacy seed loads 54 roles, while the TSD P4 RBAC matrix tabulates 42 role rows, and the difference is not enumerated | Business analyst, P4 | Resolved (directive) |
| GAP-0900 | rwb-access sandbox seed: the matrix letters for 11 of the 14 capability areas are not tabulated, so the seed content has no source table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0988 | The review-item authorise request shape, the label of the matrix and masking versions in force at the release date, and the review-field roster of the masking pack are fixed by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1011 | No source fixes the field-level names of the nine review resources, the one resolve answer, the field-patch idempotency, the document read position or the three platform message texts | Tech lead of rwb-document with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1012 | The channel pickup has no target shape of its own: the run record, the rerun operation, the channel property layout, the single-run rule and the cross-service partner read are named by the legacy story only | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1013 | The channel-intake contract baseline fixes operation names, shapes and enumerations the sources do not name, and the plan's C list omits the partner read | Tech lead | Resolved (directive) |
| GAP-1014 | The four pickup channels, their credentials, their folder lifecycle, the partner DMZ position and the scan capacity are environment facts no source states | SCB IT infrastructure | Resolved (directive) |
| GAP-1015 | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | DevOps engineer | Resolved (directive) |
| GAP-1043 | The rwb-comms operations and field names behind RWB-P6-E1055-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1044 | The document type of the WIN proof-of-delivery receipt and the notice-type to document-type mapping | Center of excellence analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1045 | The field names of the WIN receipt in document_field and the receipt granularity | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1046 | The text of MSG-P5-016 | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1047 | The agent's document-read tool contract is not defined in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1048 | The idempotency-key format of DocumentStored and the event field names the agent reads are not defined | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1049 | The mask format and the per-role list of personal fields for SY-AGENT are not defined | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1050 | The read behaviour for a stored document whose type has left the version in force is not defined | Business analyst, P5 | Resolved (directive) |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1052 | The file-name pattern of the synthetic documents is not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1079 | The rwb-document contract used for the write-once generated PDF has no contract dependency row | Solution architect | Resolved (directive) |
| GAP-1080 | The field names behind the rwb-source-data data-product contract are not specified | Solution architect | Resolved (directive) |
| GAP-1081 | Where the merge snapshot is persisted is not specified | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1082 | The request and answer field list of the notice operations is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1083 | The scope and right check of the notice operations has no rwb-access dependency row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1084 | Field DF-LEG-030 is party_id in the module specification and person_key in the legacy story | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1085 | No operation in the ownership map raises a task on rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1086 | The error code of each refusal condition on the notice POST is not fixed | Solution architect | Resolved (directive) |
| GAP-1087 | The hold reason value set is not enumerated in a list of values | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1088 | The NoticeGenerated payload element list is not enumerated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1097 | The pod and batch-status contract elements are not named in RWB-P1-E1066-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1098 | No access guard story covers the notice read of rwb-comms | Solution architect | Resolved (directive) |
| GAP-1099 | The stored letter retrieval is not named in RWB-P5-E1054-CON | Solution architect | Resolved (directive) |
| GAP-1100 | The INT-14 and INT-15 fixed layouts, their record keys and their transport are not in the source material | Solution architect | Resolved (directive) |
| GAP-1101 | The owner of REC-05 and of the References exception list is not named | Solution architect | Resolved (directive) |
| GAP-1102 | The WIN host, port, zone, certificate owner, container names and file sizes are not in the source material | SCB IT infrastructure | Resolved (directive) |
| GAP-1103 | The deployment slot and namespace of rwb-comms, and the exact form of the JOB-10 Airflow handoff, are not specified | DevOps lead | Resolved (directive) |
| GAP-1104 | No source gives the alert thresholds, the reviewed time of the late WIN batch or the Schedule state per environment | DevOps lead | Resolved (directive) |
| GAP-1105 | Only one hold reason is named for a notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1209 | Template code, channel, notice type, field names, recipient role holders, guard right and retry window are not named for the target | P6 comms owner, P10 agent owner and platform notification path owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1210 | The legacy data lake copy and the agent monitoring dashboard have no target, and P6 has no replacement for the dashboard | P6 comms owner, P9 reporting owner and architecture owner | Resolved (directive) |
| GAP-1211 | The agent alert event name, the alert notification operation name and the non-case binding of the cost alert are not named for the target | P10 agent owner and P6 comms owner | Resolved (directive) |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1506 | The physical dictionary mapping and the system-of-record wording disagree with the frozen view list | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1516 | FSD P10 v3 publishes the agent dashboard through a data lake write and Power BI, both removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1517 | The daily aggregate table the FSD acceptance criteria name is not in the Logical Data Model v8 entity list | Solution architect | Resolved (directive) |
| GAP-1518 | FSD P10 v3 has the agent read ACE and case facts directly, while Architecture v5 and ADR-010 reserve every ACE read to rwb-source-data | Solution architect | Resolved (directive) |
| GAP-1519 | JOB-15 is the reporting extract of rwb-reporting in the Ownership Map, but the FSD uses its completion as the trigger of the P10 dashboard | Platform administrator | Resolved (directive) |
| GAP-1520 | The admin configuration paths differ between the FSD and Architecture v5, and no source states the service REST base explicitly | Tech lead | Resolved (directive) |
| GAP-1525 | No date is stated for the platform wave that this service depends on | Program manager | Resolved (directive) |
| GAP-1528 | The tool gateway is stated as read-only and the guardrail is stated against an allowed action list, without saying whether an agent may ever act | Solution architect | Resolved (directive) |
| GAP-1530 | Four P10 features carry the same main success criterion, so the criterion does not distinguish the feature it belongs to | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1532 | The screening feature is titled at L1 and its main criterion stores a shadow run that creates no deviation | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1533 | The FSD states no wave or release for any of the sixteen agent features | Program manager | Resolved (directive) |
| GAP-1587 | FSD P5 takes branch, mailroom, SFTP and mailbox files inside P5 while Architecture v5 gives P5 no file interface | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1593 | Two FSD features assert the same review-queue criteria and the correction feed has no distinct criterion | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-2087 | The source reads version 1 in its metadata table and v2 in its file name | Document owner of the notification and correspondence design | Resolved (directive) |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2137 | Which service seeds which rows of the shared case set is not specified | QA | Resolved (directive) |
| GAP-2154 | The seed, business date, volumes and identifiers of the synthetic fixture set are not stated | QA lead | Resolved (directive) |
| GAP-2161 | Two Work Packages write the same three story files and three fragments for legacy RWB-E1-064 on rwb-source-data | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2243 | Element names of the delivery fact and of the notice answer are not in the sources read for this work package | TechX and rwb-comms contract owner | Resolved (directive) |
| GAP-2246 | The timer has no field for the notice it belongs to, and its field ID is unallocated | rwb-case data owner and the Data Dictionary owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2247 | The notice period is owned by two rwb-case stories of the same legacy loop | TechX | Resolved (directive) |
| GAP-2249 | Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2250 | The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2251 | The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | TechX and the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2306 | No source names the register's request and answer field names, its marker vocabulary or its read path, and the module FSD and TSD give the tables and the endpoint inventory only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2307 | TSD P4 T6.1 gives no role the Reference data A letter that API-P4-006 requires of an approver, so the four-eyes approver of a governance load is unnamed | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2309 | No target source states which service applies an approved dictionary load, and the legacy reference-load endpoint no longer exists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2326 | The agent-authority part of POST /authorise has no operation row, request shape or answer shape in any source | Solution architect, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2327 | The reason-code vocabulary of a refusal and the status of each code are not specified | Solution architect, P4 and the security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2329 | The default scope of the agent service identity is not specified for this legacy key | Security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2332 | The access-event codes of a dashboard read, the entry field list, the page bounds, the read index and the Flyway step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2348 | The rwb-document login, the request and answer field names of the generation path, the message text of MSG-P5-006, the container name, the index name, the Flyway step name and the P5 feature flag are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2349 | This slice owns no legacy acceptance criterion while the Work Package lists all eleven legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2350 | The dependency rows of this slice name one contract only, while the pattern set names five platform contracts, the rwb-case reference-data contract and the generation contract of the service | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2454 | The D7.1 generation record has no field layout, no final-call set and no message text in the sources | TechX | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2456 | The review decision codes and outcome values, the placement of the review facts in the record, and the rwb-decision login name are in no source | Solution architect with the reference-data owner and the ACE team | Resolved (directive) |
| GAP-3085 | RWB-S8-E1062-APP: the deviation estate the shadow screening run reads has no read operation, no published agent-policy read, no owner role for R-DEV-05 and R-DEV-06, no value for the answer limit and no test level | Solution architect, with the rwb-deviation owner, the rule-set owner of the Deviations package, the rwb-agent contract owner, the rwb-case parameter and reference-data owners, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3168 | The sandbox story applies three migrations where 19 schemas now need their own sequence | ACE DB lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
