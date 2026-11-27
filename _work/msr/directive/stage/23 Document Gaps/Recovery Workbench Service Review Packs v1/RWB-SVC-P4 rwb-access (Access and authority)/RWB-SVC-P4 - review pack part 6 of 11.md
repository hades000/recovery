# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 6 of 11 (RWB-P4-E1054-APP to RWB-P4-E2003-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 150 |
| Cross-document (pending in another document) | 192 |
| Not applied (value not in the sources) | 31 |
| Open business decisions | 30 |
| Register gaps linked | 135 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E1054-APP | 21 | 18 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1054 APP Review queue for low-confidence documents v2.md |
| RWB-P4-E1062-APP | 17 | 30 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1062 APP Deviation screening agent in shadow [E2b] v2.md |
| RWB-P4-E1063-APP | 15 | 19 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1063 APP Agent monitoring dashboard v1 [E2c] v2.md |
| RWB-P4-E1064-APP | 21 | 18 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1064 APP Data dictionary for the 14 data products v2.md |
| RWB-P4-E1065-APP | 17 | 30 | 9 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1065 APP Sandbox database with synthetic recovery data v2.md |
| RWB-P4-E1069-APP | 21 | 28 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1069 APP Read-only ACE source views, grants and boundary rule v2.md |
| RWB-P4-E2002-APP | 20 | 30 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2002 APP ACE plan status on the case v2.md |
| RWB-P4-E2003-APP | 18 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2003 APP Customer's other products on the case v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E1054-APP | R-01237 | CG-ALL-5062 | Script gap | Product owner | The story adds REVIEW_TEAM_UNATTACHED to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E1062-APP | R-01240 | CG-ALL-5073 | Script gap | Product owner | The story adds PR1 to the closed list LOV-DEVIATION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E1062-APP | R-01241 | CG-ALL-5074 | Script gap | Product owner | The story adds CALLER_KIND to the closed list LOV-ROLE-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E1063-APP | R-10686 | CG-ALL-5087 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E1069-APP | R-10699 | CG-ALL-5128 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2002-APP | R-10703 | CG-ALL-5143 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2003-APP | R-10705 | CG-ALL-5150 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1039-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22216 | GAP-2330 | Register gap | Internal audit role and the solution architect, P4 | The access entry of an agent read has no source row, element list or decision-code vocabulary of its own | Fix the entry members of a non-human read in the access-entry writer of RWB-P4-E1039-APP and publish them once for every service identity, so an audit query by agent code and policy version answers from the same chain as the screen entries. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22221 | GAP-2328 | Register gap | Compliance and PDPA officer and the security administrator role | Which of the run's fields are personal for a non-human actor, and the mask format served to an agent, are not specified | Fix the personal field list of the four agent reads and the mask format served to a non-human caller with the masking owner, load it as a masking version rather than as code, and prove it with a synthetic value that must appear in no answer, no log and no span. |
| RWB-ITG-E1069-ITG, RWB-P1-E1069-APP, RWB-P1-E1069-DB, RWB-P4-E1069-APP | R-22278 | GAP-0901 | Register gap | Compliance and PDPA officer | rwb-access ACE masking pack: no source names which ACE view fields the masking rows must cover or at which field IDs | Publish the masking field map as part of the pack design: one row per personal field ID of the 30 views with the role that may see it, agreed by the Compliance and PDPA officer, and load it with the pack instead of leaving the set to the story. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-AD004-APP, RWB-P4-E2003-APP | R-22343 | GAP-0910 | Register gap | Compliance and PDPA officer (RW-COMPLY) | The roster of roles that see the other-products account number unmasked is an assumption of the legacy story | Confirm the five clear roles and that every other role holding Case record R is masked, then load the roster through the masking load path of RWB-P4-AD004-APP. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E1063-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P4-E1063-APP, RWB-P6-E1063-APP | R-28650 | GAP-1213 | Register gap | data steward, data product owner and architecture owner | REQ-DRI-009 still requires a daily copy to the data lake, which DP-17 and Arch v5 slide 37 remove | Reword REQ-DRI-009 in the next BRD version as the daily agent measures being available for reporting from rwb-reporting with the row counts matched against the P10 source, keep the requirement identifier, and record that the P6 slice carries only the cost-alert notification, as ASM-B-P6-05-E1063-6 sets out. |
| RWB-ITG-E1064-ITG, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P4-E1064-APP | R-28656 | GAP-2308 | Register gap | Compliance and PDPA officer | No source states how many of the 1,366 dictionary fields are personal, so the masking coverage the gate checks has no expected count | Publish the personal-field list of the 14 data products from the dictionary (is_personal true) and the masking pack coverage it must reach, so that the gate can fail a load that leaves a personal field uncovered and the SIT run can assert a count. Until then the gate asserts the rule per field ID and reports the count it finds. At D1 number this row GAP-nnnn and cite it from ASM-B2-P4-020-3. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-E2003-APP | R-28706 | GAP-0911 | Register gap | Compliance and PDPA officer (RW-COMPLY) | No source fixes the masking version label in force for the wave-2 release, or the rule for two valid versions on one day | Name the masking version of the wave-2 release in the masking load file and confirm the latest-valid-from rule for a day with two valid versions. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-E2003-APP | R-28707 | GAP-0912 | Register gap | Data steward and data product owner (RW-DATASTEW) | No source states whether the other-products account number is the only personal field of the panel | Record the personal-data classification of the seven v_ace_party_product fields in the data dictionary, and add a masking row or an explicit unmasked false for any further personal field. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P4-E1062-APP | R-36670 | ASM-3869 | Register assumption |  | For the screening run the personal fields are the two the legacy marks masked - DF-INT-011 (the ledger summary) and DF-DOC-015 (the stored document field value) - together with the party identifiers a case read presents, and they are answered masked for a non-human actor at the masking version in force, with the shapes the FSD fixes for a screen: XXXXXXXXX1234, XXXXXX5678 and XXXX-XX-XX. A field ID with no masking_rule row is masked, and no clear value, rendering or last four digits is answered. | Compliance and PDPA officer with the security administrator role |
| RWB-P4-E1062-APP | R-36672 | ASM-3871 | Register assumption |  | The access entry of an agent answer carries the actor, the caller type, the agent code, the policy version, the autonomy mode, the case, the trigger event, the field IDs with their markers, the matrix version, the masking version and the time, with decision code AC-READ for an admission and AC-DENY for a refusal, in the append-only chain written by RWB-P4-E1039-APP. | Internal audit role with the writer of RWB-P4-E1039-APP |
| RWB-P4-E1069-APP | R-36689 | ASM-1622 | Register assumption |  | The masking pack of this story covers the 20 field IDs of v_ace_customer, DF-ACE-055 to DF-ACE-074, and no field of the other 29 views; the clear identity number is out of reach in every case because the view returns id_no_masked (DF-ACE-073) and id_no_last4 (DF-ACE-074). | Compliance and PDPA officer and the rwb-access tech lead when the pack design is published |
| RWB-P4-E2003-APP | R-36699 | ASM-1632 | Register assumption |  | The masking_rule rows for DF-ACE-281 at the masking version in force carry unmasked true for RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, and unmasked false for RW-PHONECOL and every other role that holds Case record R. | Compliance and PDPA officer (RW-COMPLY), through the masking load path of RWB-P4-AD004-APP |
| RWB-P4-E2003-APP | R-36700 | ASM-1633 | Register assumption |  | The masking version of the wave-2 release is MASK-2026.12, and the version in force for a business date is the one whose valid_from is the latest on or before that date. | Compliance and PDPA officer (RW-COMPLY) and the solution architect |
| RWB-P4-E2003-APP | R-36701 | ASM-1634 | Register assumption |  | DF-ACE-281 (v_ace_party_product.account_no) is the only personal field of the other-products panel that this service masks; the other six fields of the view carry no masking row and are named as identifiers only. | Data steward and data product owner (RW-DATASTEW), in the data dictionary |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E1054-APP | R-10681 | CG-ALL-5064 | 12.3 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | Kafka Topic and Event Catalog v1 row for AccessPolicyChanged has its payload as Not specified in the source documents (GAP-0127; ASM-0204). Nothing to align to; story unchanged. |
| RWB-P4-E1054-APP | R-25410 | CG-ALL-5070 | 3, 3.1 | Flyway file V1054_1__review_authority_read_path.sql is not in the V0001..Vnnnn form | Migration name line (L401) is blank in this chunk; next Flyway number for rwb_access is not specified in the source documents (CG-ALL-5070). Story unchanged. |
| RWB-P4-E1054-APP | R-30887 | NEWAC-RWB-P4-E1054-APP-AC18 | 7, 16 | AC18: §5 X4: The token carries no Recovery role, or no second factor (covered by 'BR4' only) | Sections 7 and 16 text not in this chunk, so no exact old text to add AC18. Test Not specified in the source documents (NEWAC-RWB-P4-E1054-APP-AC18). |
| RWB-P4-E1054-APP | R-30888 | NEWAC-RWB-P4-E1054-APP-AC19 | 7, 16 | AC19: §5 X6: Two roles of the caller conflict (for example RW-SECADM with a business role) (covered by 'BR4' only) | Sections 7 and 16 text not in this chunk, so no exact old text to add AC19. Test Not specified in the source documents (NEWAC-RWB-P4-E1054-APP-AC19). |
| RWB-P4-E1054-APP | R-30889 | NEWAC-RWB-P4-E1054-APP-AC20 | 7, 16 | AC20: §5 X7: The caller is an agent or a service identity, not a person (covered by 'BR4, section 10' only) | Sections 7 and 16 text not in this chunk, so no exact old text to add AC20. Test Not specified in the source documents (NEWAC-RWB-P4-E1054-APP-AC20). |
| RWB-P4-E1063-APP | R-16722 | DOR-RWB-P4-E1063-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Sections 9-10 are not in this chunk, so no exact old text exists. Re-send sections 9-10 to add the SCR-43 empty, loading, error and no-access states. |
| RWB-P4-E1063-APP | R-16723 | DOR-RWB-P4-E1063-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 is not in this chunk, so no exact old text exists. Re-send section 11 to correct the personal-data wording for the P2 fields. |
| RWB-P4-E1064-APP | R-05738 | DOR-RWB-P4-E1064-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design in the project .md sources; the grep for 'epic design' hits only _work scratch files. Sign-off cannot be recorded without inventing it. |
| RWB-P4-E1064-APP | R-10689 | CG-ALL-5096 | 4, 12.1 | HTTP errors with no message ID: 404 unknown load or unknown table code | Error and Message Standard v4 is not a .md in the project. No 404 message ID can be taken from it, so none is added. Needs the standard's 404 mapping and the business analyst. |
| RWB-P4-E1064-APP | R-16734 | DOR-RWB-P4-E1064-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | The Error and Message Standard v4 text is not in the project, so the difference cannot be resolved. The story MSG-P7-002 text also differs from FSD P7 v5 line 141; no edit made. |
| RWB-P4-E1064-APP | R-25421 | CG-ALL-5097 MSG-P7-002 text differs from Error and Message Standard v4 | 4, 14 | MSG-P7-002 text differs from the Error and Message Standard v4 | Error and Message Standard v4 is not in the project, so the new wording had no source. Difference cannot be resolved here. |
| RWB-P4-E1065-APP | R-05745 | DOR-RWB-P4-E1065-APP-14 | not located | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off found in the project (Glob and Grep). Sign-off cannot be confirmed, so no text can be added. |
| RWB-P4-E1065-APP | R-16735 | DOR-RWB-P4-E1065-APP-10 | 9, 10 | Definition of Ready item 10 Screens and states: Partial | SCR-43 empty, loading, error and no-access states belong in sections 9 and 10, which are outside this chunk. The screen spec is not in the source set. |
| RWB-P4-E1065-APP | R-16740 | DOR-RWB-P4-E1065-APP-4 | 7, 8, 16 | Definition of Ready item 4 Business rules: Partial | BR2, BR7 and BR8 need criteria in section 7 and test cases in section 16, both outside this chunk. TC-E1-065-14 AC10 text is Not specified. |
| RWB-P4-E1065-APP | R-22250 | GAP-0374 | 3, 4 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | The proposed fix edits the per-schema wording in sections 3 and 4, which are outside this chunk. It cannot be placed here. |
| RWB-P4-E1065-APP | R-22251 | GAP-0501 | 3, 4 | The sandbox scope per service and the placement of the generator module are not specified | Sandbox scope and generator placement text sits in sections outside this chunk. The proposed fix cannot be placed here. |
| RWB-P4-E1065-APP | R-22253 | GAP-2137 | Not in chunk | Which service seeds which rows of the shared case set is not specified | Seeding-rules section text is not in this chunk, so no exact old text exists to edit. Accepted fix needs that section; re-run with it. |
| RWB-P4-E1065-APP | R-22254 | GAP-2249 | 4, 11 | Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | Task and timer count text in sections 4 and 11 is not in this chunk, so no exact old text exists to edit. Re-run with those sections. |
| RWB-P4-E1065-APP | R-22255 | GAP-2250 | Not in chunk | The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | Queue distribution and cap-of-40 text is in seed sections not in this chunk, so no exact old text exists to edit. Re-run with those sections. |
| RWB-P4-E1065-APP | R-22256 | GAP-2252 | 11 | The decision code and the payload of the decision records the seed writes are not in the sources | Decision code wording in section 11 is not in this chunk, so no exact old text exists to edit. Re-run with section 11. |
| RWB-P4-E1069-APP | R-10700 | CG-ALL-5130 | 12.8 | Criteria and test data read ACE views directly | Added an rwb-source-data fake row to 12.8. The Given lines that read recovery.v_ace_customer (AC7, AC8) are in section 7, not in this chunk, so they are not rewritten. |
| RWB-P4-E1069-APP | R-16742 | DOR-RWB-P4-E1069-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 text for SCR-43 and SCR-47 is not in this chunk, so the empty, loading, error and no-access states cannot be added. |
| RWB-P4-E1069-APP | R-16743 | DOR-RWB-P4-E1069-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 text is not in this chunk, so the personal-data classing of P2 fields cannot be reconciled with the story. |
| RWB-P4-E1069-APP | R-16744 | DOR-RWB-P4-E1069-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Section 18 text is not in this chunk, so the DL43 assumption rows ASM-0193, ASM-0737, ASM-0748 and ASM-0816 cannot be recorded. |
| RWB-P4-E1069-APP | R-16745 | DOR-RWB-P4-E1069-APP-4 | 7, 8, 16 | Definition of Ready item 4 Business rules: Partial | Criteria and test rows for BR2, BR5, BR6, BR9, BR10, BR13 and BR14 belong in sections 7 and 16, not in this chunk. Section 8 is unchanged. |
| RWB-P4-E1069-APP | R-22279 | GAP-0903 | 3 | rwb-access ACE masking pack: no source holds the roster of roles that see a personal field unmasked | No source holds the roster, so the approval claim was not supported and was removed. |
| RWB-P4-E1069-APP | R-28413 | GAP-2035 | 7 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | The story follows Architecture v5 (per-service logins, views granted only to rwb_source_data). Section 7 rows are not in this chunk, so no edit was made. |
| RWB-P4-E2002-APP | R-05762 | DOR-RWB-P4-E2002-APP-17 | header | Definition of Ready item 17 Dependencies: Fail | Dependency row naming RWB-P7-E1073-CON is outside the supplied story text, so no exact old text exists. No replacement key invented. |
| RWB-P4-E2002-APP | R-16747 | DOR-RWB-P4-E2002-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-03 screen-state text is outside the supplied story text. Sources give no empty, loading, error or no-access states, so none invented. |
| RWB-P4-E2002-APP | R-16749 | DOR-RWB-P4-E2002-APP-18 |  | Definition of Ready item 18 Open decisions: Partial | Section 19 and the DL10 entry are not in the supplied story text, so they cannot be located and edited. |
| RWB-P4-E2002-APP | R-25440 | CG-ALL-5144 | 3, 3.1 | Flyway file V2002_1__plan_status_access.sql is not in the V0001..Vnnnn form | Migration line cited at L373 is outside supplied text; L373 shown is the Temporal row. Next Vnnnn number not in sources. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (21)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08373 | RWB-P4-E1054-APP | CG-ALL-5063 | 7 | Remove the closed enum on defaultScope so LOV-SCOPE values are read as data, as the story states (ruling R-01238). |
| CDC-08392 | RWB-P4-E1062-APP | CG-ALL-5076 | 13 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are read as data, matching Reference Data v5 Lists and section 13 DP-07. |
| CDC-08393 | RWB-P4-E1062-APP | CG-ALL-5077 | 13 | Remove the fixed enum on defaultScope so LOV-SCOPE values are read as data, matching Reference Data v5 Lists and section 13 DP-07. |
| CDC-08397 | RWB-P4-E1062-APP | DOR-RWB-P4-E1062-APP-8 | 12.2 | Declare roleClass and defaultScope as values read from LOV-ROLE-CLASS and LOV-SCOPE at the version in force, not as closed enums |
| CDC-08440 | RWB-P4-E1064-APP | CG-ALL-5092 | 12.1 | Publish operation GET /api/recovery/access/v1/admin/dictionary-authority through the owner's CON story, or remove it |
| CDC-08441 | RWB-P4-E1064-APP | CG-ALL-5093 | 12.1 | Publish operation POST /api/recovery/access/v1/admin/dictionary-authority-loads/{loadId}/approve through the owner's CON story, or remove it |
| CDC-08442 | RWB-P4-E1064-APP | CG-ALL-5094 | 12.1 | Publish operation POST /api/recovery/access/v1/admin/dictionary-authority-loads/{loadId}/return through the owner's CON story, or remove it |
| CDC-08443 | RWB-P4-E1064-APP | CG-ALL-5095 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |
| CDC-08444 | RWB-P4-E1064-APP | DOR-RWB-P4-E1064-APP-8 | 12.1 | Publish GET /admin/dictionary-authority, POST /admin/dictionary-authority-loads/{loadId}/approve, POST /admin/dictionary-authority-loads/{loadId}/return and POST /api/recovery/access/v1/authorise in rwb-access.yaml. |
| CDC-08458 | RWB-P4-E1065-APP | CG-ALL-5108 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON |
| CDC-08459 | RWB-P4-E1065-APP | CG-ALL-5109 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in rwb-access.yaml through RWB-P4-E1037-CON |
| CDC-08461 | RWB-P4-E1065-APP | CG-ALL-5111 | 13 | Remove the fixed enum on roleClass; LOV-ROLE-CLASS is data, per the ruling |
| CDC-08462 | RWB-P4-E1065-APP | CG-ALL-5112 | 13 | Remove the fixed enum on defaultScope; LOV-SCOPE is data, per the ruling |
| CDC-08464 | RWB-P4-E1065-APP | DOR-RWB-P4-E1065-APP-8 | 12.1 | Add paths POST /authorise and GET /me/permissions; replace closed enums of roleClass and defaultScope with references to LOV-ROLE-CLASS and LOV-SCOPE. |
| CDC-08488 | RWB-P4-E1069-APP | CG-ALL-5120 | 12.1 | Publish POST /api/recovery/access/v1/authorise through the RWB-P4-E1037-CON contract, or remove it from this story's section 12.1. |
| CDC-08489 | RWB-P4-E1069-APP | CG-ALL-5121 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions through the RWB-P4-E1037-CON contract, or remove it from this story's section 12.1. |
| CDC-08490 | RWB-P4-E1069-APP | CG-ALL-5122 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies through the RWB-P4-E1037-CON contract, or remove it from this story's section 12.1. |
| CDC-08491 | RWB-P4-E1069-APP | CG-ALL-5124 | find it | Remove the fixed enum on defaultScope so that LOV-SCOPE values are accepted as data without a code change. |
| CDC-08494 | RWB-P4-E1069-APP | DOR-RWB-P4-E1069-APP-8 | 12.1 | Add POST /authorise, GET /me/permissions and GET /masking-policies under /api/recovery/access/v1 as described in section 12.1 |
| CDC-08516 | RWB-P4-E2002-APP | CG-ALL-5134 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the CON story, or remove the operation from the story. |
| CDC-08517 | RWB-P4-E2002-APP | CG-ALL-5135 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in rwb-access.yaml through the CON story, or remove the operation from the story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08384 | RWB-P4-E1054-APP | CG-ALL-5069 | 18 | Align the REQ-DCM-005 test list in the RTM to the section 18 list of RWB-P4-E1054-APP; remove test IDs of other keys that this story does not own. |
| CDC-08413 | RWB-P4-E1062-APP | CG-ALL-5080 | 18 | Align the test lists of REQ-DVH-001, REQ-DVH-003, REQ-DVH-007 and REQ-ACA-010 in the RTM next version with §18 of this story. |
| CDC-08438 | RWB-P4-E1063-APP | CG-ALL-5086 | 18 | Align the REQ-DRI-009 test list with RWB-P4-E1063-APP section 18 (TC-E1-063-01 to -03), or move the TC-E1-014 and TC-E2-031 rows out of RTM v7. |
| CDC-08454 | RWB-P4-E1064-APP | CG-ALL-5100 | 18 | Align the REQ-RDF-001 and REQ-RDF-011 test lists with section 18 of RWB-P4-E1064-APP in the next RTM version. |
| CDC-08478 | RWB-P4-E1065-APP | CG-ALL-5115 | 18 | Align the REQ-RDF-001 and REQ-RDF-010 test lists with RWB-P4-E1065-APP section 18 in the next RTM version; RTM v7 lists TC-E1-065-02, -03 and -06 for REQ-RDF-001. |
| CDC-08508 | RWB-P4-E1069-APP | CG-ALL-5127 | 18 | Align the REQ-RDF-002 and REQ-DRI-006 test lists with section 18 of RWB-P4-E1069-APP at the next RTM version. |
| CDC-08509 | RWB-P4-E1069-APP | GAP-3213 | 18 | REQ-RDF-004 row: list RWB-E1-069, RWB-E1-018 and RWB-E2-006 as legacy slices, and cite RWB-ITG-E3013-ITG, RWB-ITG-E3017-ITG and RWB-ITG-E3026-ITG as the citing stories. |
| CDC-08542 | RWB-P4-E2002-APP | CG-ALL-5142 | 18 | Align the REQ-DRI-013 and REQ-CHO-002 test lists to RWB-P4-E2002-APP §18 and remove the TC-E2-001-xx rows and other tests not in that list. |
| CDC-08553 | RWB-P4-E2003-APP | CG-ALL-5149 | 18 | Align the REQ-CHO-003 and REQ-RDF-010 test lists with section 18 of RWB-P4-E2003-APP in the next RTM version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08378 | RWB-P4-E1054-APP | DOR-RWB-P4-E1054-APP-7 | 11 | Add DF-REF-039 for role.entra_group (table role in rwb_access) to the model |
| CDC-08401 | RWB-P4-E1062-APP | DOR-RWB-P4-E1062-APP-7 | 11 | Add DF-REF-039 (role.entra_group) to LDM v9, or remove it from the range DF-REF-034 to DF-REF-039 in section 11 |
| CDC-08446 | RWB-P4-E1064-APP | CG-ALL-5090 Name v_data_dictionary is not in LDM v9 or Data Classification v5 | 1, 12.7, 18 | Name replaced by a placeholder citing DOR-RWB-P4-E1064-APP-7. |
| CDC-08447 | RWB-P4-E1064-APP | CG-ALL-5091 Name ace_view_owner is not in LDM v9 or Data Classification v5 | 12.7 | Owner label replaced by a placeholder citing DOR-RWB-P4-E1064-APP-7. |
| CDC-08465 | RWB-P4-E1065-APP | CG-ALL-5106 | 11 | No LDM v9 row exists for DF-REF-039. Section 11 range narrowed to DF-REF-034 to DF-REF-038 by CG-ALL-5105; the fix sits in LDM v9. |
| CDC-08468 | RWB-P4-E1065-APP | DOR-RWB-P4-E1065-APP-7 | 11 | DF-REF-039 and the role field range are not in LDM v9; register them there. Section 11 range narrowed to DF-REF-034 to DF-REF-038 by CG-ALL-5105. |
| CDC-08477 | RWB-P4-E1065-APP | GAP-2251 |  | Story marks the DEV read-only role name Not specified; rwb-case login is set in RWB-PLT-NF06-DB. |
| CDC-08498 | RWB-P4-E1069-APP | DOR-RWB-P4-E1069-APP-7 | 11 | Add DF-REF-039 to entity role in v9, or withdraw it; section 11 row DF-REF-034 to DF-REF-039 cites it. |

### RWB-P10-E1063-APP (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08430 | RWB-P4-E1063-APP | GAP-0372 | 15 | Name the P9 rwb-reporting read model fed from agent events, GET /reports/measures, the Airflow JOB-15 trigger in rwb-reporting and the P1 admin job owner; drop the agent_run_daily lake copy. |
| CDC-08431 | RWB-P4-E1063-APP | GAP-0616 | 15 | Name the Temporal Schedule AgentRunDailyRollup on rwb-agent at 01:30 with overlap SKIP, the agent-metrics route, the EV-28 feed, the service login and the home of the daily aggregate in rwb_agent. |
| CDC-08433 | RWB-P4-E1063-APP | GAP-1210 | 15 | Removed the added P9/P10 target sentence and the GET route path and ASM citation |
| CDC-08434 | RWB-P4-E1063-APP | GAP-1211 | 15 | Publish the agent alert event on rwb.agent.events.v1 with the alert reference; send the cost alert on the published P6 message operation with the alert reference in the case position, no case lookup, read back via GET /notices/{noticeId}. |
| CDC-08436 | RWB-P4-E1063-APP | GAP-1519 | 15 | Give rwb-agent its own daily aggregation step triggered once per business date after the run record closes; JOB-15 stays the rwb-reporting Airflow extract; the PRD names no job ID; correct FSD P10 v3 AC-ALT-P10-006-01. |
| CDC-08439 | RWB-P4-E1063-APP | GAP-0618 |  | Specify the topology, host, SKU, budget, gateway-bff route path, rwb-agent login, feed retention, relay interval and alert thresholds in the rwb-agent story; this slice reads only through the composite route. |

### RWB-P10-E1062-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08407 | RWB-P4-E1062-APP | GAP-0371 | find it | Name the P7 rule-row owner lookup, the P1 interaction ledger read and the P3 case read as owner contracts for the screening run |
| CDC-08408 | RWB-P4-E1062-APP | GAP-0615 | find it | Declare one run-start and one run-read operation on /api/recovery/agent/v1, with request members, three event payloads and consumed paths |
| CDC-08412 | RWB-P4-E1062-APP | GAP-0614 |  | Fix the run-start operation on /api/recovery/agent/v1 with its members and refusal codes; read case, parameters and lists via rwb-case, deviations via rwb-deviation, ledger via rwb-source-data, documents via rwb-document, 2 s budget each; publish run events on rwb.agent.events.v1 via outbox. |
| CDC-08416 | RWB-P4-E1062-APP | GAP-1047 |  | State that the agent case read maps to API-P5-002 and its document read to API-P5-003, with API-P5-009 for an extracted-field filter; publish the tool call field names in the AsyncAPI and OpenAPI of rwb-document. |
| CDC-08417 | RWB-P4-E1062-APP | GAP-1048 |  | Fix the DocumentStored payload as documentId, caseId, documentType, source and storedAt; state that the idempotency key is the outbox event ID. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08374 | RWB-P4-E1054-APP | DOR-RWB-P4-E1054-APP-14 | Metadata | Record the signed epic design sign-off reference; no sign-off exists in the source documents to carry into the story. |
| CDC-08421 | RWB-P4-E1063-APP | DOR-RWB-P4-E1063-APP-14 | find it | Record the signed epic design sign-off for RWB-P4-E1063-APP; no signed epic design is in the story or source documents. |
| CDC-08520 | RWB-P4-E2002-APP | DOR-RWB-P4-E2002-APP-14 | section header | No signed epic design is in the story or the source documents; the story cannot evidence sign-off. |
| CDC-08546 | RWB-P4-E2003-APP | DOR-RWB-P4-E2003-APP-14 | Metadata | Record the signed epic design sign-off for RWB-P4-E2003-APP |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08386 | RWB-P4-E1054-APP | GAP-0988 | 5 | Publish the review-item authorise request and answer schema, naming the review team attribute and every other attribute, and record the matrix and masking version labels with valid-from dates and environment per release date. Story already carries the acting-default note. |
| CDC-08410 | RWB-P4-E1062-APP | GAP-2327 | find it | Publish CALLER_KIND, RIGHT_NOT_HELD and SCOPE_NOT_ALL as refusal reasons of POST /authorise, with their status codes |
| CDC-08475 | RWB-P4-E1065-APP | GAP-0898 |  | Add POST /authorise and GET /me/permissions with request and answer schemas, publish with RWB-P4-E1037-CON, stub them in the contract fake, and publish the SCR-43 composite route with gateway-bff (DP-19). |
| CDC-08526 | RWB-P4-E2002-APP | GAP-0908 | 11 | Add the POST /authorise path and the resolved permission view with request and answer schemas, publish with RWB-P4-E1037-CON, and record whether the plan reference is in the authorise request. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08405 | RWB-P4-E1062-APP | GAP-1819 | find it | Add S8 rows in rwb_deviation for the screening run, score, contact stop, agent feedback and breach entity groups |
| CDC-08411 | RWB-P4-E1062-APP | GAP-3085 |  | Publish a service read of open deviations by case; publish the agent-policy read operation and its fields; publish codes and owner roles of R-DEV-05 and R-DEV-06 with package version; set the answer limit and test level. |
| CDC-08500 | RWB-P4-E1069-APP | GAP-0014 | find it | Add the v5 tables for S1 (rwb_valuation object groups) and P8 (payment, proceeds matching, fees, bookings, posting files); populate FK cuts as ID references. |
| CDC-08501 | RWB-P4-E1069-APP | GAP-0110 | find it | Keep the 30 v_ace_* views in schema recovery, read only; move v_data_dictionary to rwb_source_data. |

### RWB-P2-E2002-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08522 | RWB-P4-E2002-APP | DOR-RWB-P4-E2002-APP-22 | header | Publish a contract fake library version and record it as published for this story's contract dependency. |
| CDC-08528 | RWB-P4-E2002-APP | GAP-0655 |  | Approve the four assumptions (accountNo answer shape, live and messageCode rule, interface batch and budget rules, consumed read shapes) before tagging, and reconcile the interface-versus-view wording in the Service Contract Catalog. |
| CDC-08530 | RWB-P4-E2002-APP | GAP-0769 |  | Confirm whether a batch plan-status operation is published; if not, the rwb-case step calls the per-case read with the parameter-driven batch size and timeout. |
| CDC-08536 | RWB-P4-E2002-APP | GAP-2472 |  | Keep the plan read and stored status with rwb-integration and rwb-case; limit the rwb-decision slice to the registry version and decision record; restate the endpoint on the owner's per-service base. |

### RWB-PLT-N001-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08539 | RWB-P4-E2002-APP | GAP-0386 |  | Agree the harness repository, SIT and UAT environments, seeded case, plan and package values, evidence format and retention, pass or fail gate, and publish the gateway-bff composite route path and merge order. |
| CDC-08540 | RWB-P4-E2002-APP | GAP-0773 |  | Publish the SCR-03 composite route with its path, the two parallel calls, the merge rule (live answer wins, stored answer with MSG-P2-008 when live is missing or not live), the masking rule and the 2 s budget split. |
| CDC-08544 | RWB-P4-E2002-APP | GAP-0909 | find it | Fix the rwb-access per-service login name and publish the SCR-03 composite route field list, hop list, merge order and masking rule (DP-19). |
| CDC-08557 | RWB-P4-E2003-APP | GAP-0913 | 15 | Publish the gateway-bff composite route for SCR-03 and its other products panel with its field list and masking step |

### RWB-P5-E1054-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08380 | RWB-P4-E1054-APP | GAP-1010 | 3 | Read the four review parameters from document_hub_parameter in rwb_document as data; publish the by-number case read on RWB-P3-E1035-CON; fix field-level names and platform message texts before wave 1 entry. |
| CDC-08381 | RWB-P4-E1054-APP | GAP-1011 |  | Freeze the seven operations, nine resources, five value sets, IntakeResolution envelope, If-Match lock with idempotent repeat, document read reference and event schema; keep message texts as recorded placeholders. |
| CDC-08382 | RWB-P4-E1054-APP | GAP-0365 |  | Publish queue, resolve, field-review and document-review operations on P5 under /api/recovery/document/v1; read case status through P3 and scope through P4; prove attach and DOCATT end to end. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (service story folder) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08391 | RWB-P4-E1062-APP | CG-ALL-5075 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that holds the rwb-decision rule package contract used by the DP-04 row of section 13. |
| CDC-08394 | RWB-P4-E1062-APP | DOR-RWB-P4-E1062-APP-17 | 13 | Create story RWB-P7-E1073-CON, or name the existing story for the rwb-decision rule package contract, so the named dependency exists. |
| CDC-08395 | RWB-P4-E1062-APP | DOR-RWB-P4-E1062-APP-21 | 13 | Create contract story RWB-P4-E1062-CON covering POST /authorise and GET /me/session, and add it as the CON dependency of this story. |

### RWB-P10-E1063-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08423 | RWB-P4-E1063-APP | DOR-RWB-P4-E1063-APP-21 | header | Contract dependency RWB-P10-E1063-CON is in the header table and is published by the P10 slice; no RWB-P4-E1063-CON story exists. No edit made in this story. |
| CDC-08424 | RWB-P4-E1063-APP | DOR-RWB-P4-E1063-APP-22 | 12.8 | Publish the fake library version and add a fake for rwb-case; name the published version against the fakes in 12.8. |
| CDC-08428 | RWB-P4-E1063-APP | GAP-0617 | find it | Fix the query on /api/recovery/agent/v1 with the five parameters, a declared page size and cursor, the aggregate element, held-date status members, Schedule AgentRunDailyRollup in rwb-recovery on the rwb-agent queue with SKIP overlap, and the notification operation per its proposed fix. |

### RWB-P1-E1064-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08450 | RWB-P4-E1064-APP | GAP-0499 | find it | Fix the five schema property names from API Specification v4, set required flags and string lengths at baseline review, and name the login as rwb_source_data (DP-02). |
| CDC-08452 | RWB-P4-E1064-APP | GAP-2306 | 2 | Publish the register path, query parameters and answer schema, and fix the marker vocabulary masked and clear and the MSG-P1-002 coded check names in the Error and Message Standard. |
| CDC-08453 | RWB-P4-E1064-APP | GAP-2309 | 2 | Confirm the apply order with the owners of rwb-case, rwb-source-data and rwb-access and publish it in both contracts and the reference-load handler note. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08466 | RWB-P4-E1065-APP | CG-ALL-5107 | 16 | Add list LOV-RISK-TIER to Lists, or name the Reference Data v5 list used for recovery_case.risk_tier in TC-E1-065-03. |
| CDC-08467 | RWB-P4-E1065-APP | DOR-RWB-P4-E1065-APP-20 | find it | Publish list LOV-RISK-TIER (for recovery_case.risk_tier, used by TC-E1-065-03) in Reference Data v5. |
| CDC-08532 | RWB-P4-E2002-APP | GAP-0771 |  | Add a table code for the plan event map to LOV-REF-TABLE and load its rows as reference_row under a reference_version, one row per ACE status and route state pair, with no map row in code. |

### OTHER:TSD P4 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08473 | RWB-P4-E1065-APP | GAP-0900 | find it | Extend the T6.1 matrix to the 14 capability areas of LOV-CAPABILITY and publish the matrix version with pack load story RWB-P4-AD002-APP. |
| CDC-08511 | RWB-P4-E1069-APP | GAP-0902 | 16 | Record in T3.1 the masking version naming rule fixed with the pack owner (year and month, as PM-2026.12), so the label comes from the pack owner at load time. |
| CDC-08513 | RWB-P4-E1069-APP | GAP-0905 | 16 | Record that masking_rule.field_id is a dictionary field ID held as a value with no cross-schema key, and confirm the dictionary stays with P1 and is not duplicated. |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08547 | RWB-P4-E2003-APP | DOR-RWB-P4-E2003-APP-21 | Metadata | Contract dependency names RWB-P4-E1037-CON; its published state is not shown in this story and sits with that contract. |
| CDC-08548 | RWB-P4-E2003-APP | DOR-RWB-P4-E2003-APP-22 | 3 | No fake library version is in the sources; the placeholder is recorded as Not specified, and the publication state sits with the contract fake. |
| CDC-08550 | RWB-P4-E2003-APP | GAP-0915 | 7 | Fix the masking answer schema: per-role row, marker values clear and masked, last-four shape, and masking version. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08376 | RWB-P4-E1054-APP | CG-ALL-5066 | 4, 14 | Add a new message ID for 'Two roles of the caller conflict' with text '{role} may not be held together with {role}.'; the story cites it once it exists |
| CDC-08379 | RWB-P4-E1054-APP | DOR-RWB-P4-E1054-APP-9 | 14 | Add a new message ID for 'Two roles of the caller conflict' with text '{role} may not be held together with {role}.'; the story cites it once it exists |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08389 | RWB-P4-E1054-APP | GAP-1593 |  | PRD reads the two sections as one behaviour delivered by CAP-P5-010, FR-P5-017 and FR-P5-018 and adds the correction feed to the decision record; FSD P5 needs one distinct criterion for the correction feed to the labelled set. |
| CDC-20589 | RWB-P4-E1054-APP | R-28625 |  | Correction feed and CAP-P5-010, FR-P5-017/018 belong to PRD P5 rwb-document v2 and FSD P5 v3; this P4 PRD has no P5 references to change. |

### OTHER:FSD P10 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08425 | RWB-P4-E1063-APP | GAP-1516 | find it | Remove the Power BI and model gateway integration points (A2.6.2) and reword AC-EXC-P10-006-01 to check the measure hand-over row count, not a data lake write, per Architecture v5. |
| CDC-08435 | RWB-P4-E1063-APP | GAP-1517 | 15 | Replace the agent_run_daily assertion in AC-ALT-P10-006-02 with a per-date projection over agent_run, idempotent per agent and version; physical name and retention in the technical specification. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08448 | RWB-P4-E1064-APP | DOR-RWB-P4-E1064-APP-6 | 10 | Add role SY-DATALOAD (data load service identity, R in Reference data per the matrix fixture in §12.8). |
| CDC-08451 | RWB-P4-E1064-APP | GAP-0891 | 2 | Give one role the Reference data A letter in the SIT and production matrices and record which role approves a governance load of the authority tables. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08460 | RWB-P4-E1065-APP | CG-ALL-5110 | 13 | Name the existing story for the DP-04 contract or create RWB-P7-E1073-CON |
| CDC-08463 | RWB-P4-E1065-APP | DOR-RWB-P4-E1065-APP-17 | 13 | Name the existing story for the DP-04 contract or create RWB-P7-E1073-CON |

### RWB-ITG-W1J01-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08469 | RWB-P4-E1065-APP | GAP-0384 | find it | Record the harness repository, environment, namespace, pipeline stage, tooling, fixture set, reset, report format and all-green gate as agreed by QA lead at the wave 1 entry check. |
| CDC-08470 | RWB-P4-E1065-APP | GAP-2154 | find it | Keep seed, business date, volumes and identifiers as configuration; write the Template and Rules R9 placeholder until QA lead sets them. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08479 | RWB-P4-E1065-APP | GAP-1051 | find it | Publish the per-case document count and the version depth as seed parameters, shared with RWB-P5-E1025-APP so a change is a parameter. |
| CDC-08484 | RWB-P4-E1065-APP | GAP-0899 | find it | Publish the 54-role list with administration and non-human roles marked; reconcile it with the 42 rows of TSD P4 T6.1; fix the role count the DEV seed carries. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08485 | RWB-P4-E1065-APP | GAP-1052 |  | Fix the synthetic file naming pattern next to the sandbox file properties and state that file content is derived from the seed value, case ID and type so the hash is stable. |
| CDC-08507 | RWB-P4-E1069-APP | GAP-0568 |  | Publish the login creation and credential policy and the exact grant and revoke list with migration order; record RWB-PLT-E1044-CON as platform dependency of per-service database stories. |

### RWB-P4-E1069-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08492 | RWB-P4-E1069-APP | DOR-RWB-P4-E1069-APP-14 | find it | Confirm the signed epic design sign-off and record it in the epic design record. |
| CDC-08493 | RWB-P4-E1069-APP | DOR-RWB-P4-E1069-APP-22 | find it | Publish the contract fake library and record its version against this story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08519 | RWB-P4-E2002-APP | DOR-RWB-P4-E2002-APP-12 | 16 | Add TC-E2-002-11 to tab Story test cases; add TC-E2-002-12 to -14 for AC8, the contract and the §12.7 boundary; align section 18 test lists with RTM v7. |
| CDC-08524 | RWB-P4-E2002-APP | CG-ALL-5139 | 16 | Add a row for TC-E2-002-11 on tab Story test cases with Given, When and Then copied from AC2 and BR6. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20865 | RWB-P4-E1069-APP | R-09196 |  | Per-service ACE DB logins are named in the RWB-PLT-DB stories; no login name is in any source. Section 3 already states the 18 logins are not specified. |
| CDC-20866 | RWB-P4-E1069-APP | R-28673 |  | The 19 login names would be invented; none is in any source. Placeholder stays in TC-E1-069-02. Section 3 keeps the CG-B-TECH-05-4 statement. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; OTHER:path not located in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08375 | RWB-P4-E1054-APP | DOR-RWB-P4-E1054-APP-8 | header | Replace the closed enum for defaultScope with a reference to LOV-SCOPE data. Rename event type rwb.decision-record.DecisionRecorded.v1 to rwb.decision.DecisionRecorded.v1 as in Kafka Catalog v1. Story already reads LOV-SCOPE and uses the catalog event name. |

### RWB-P5-E1054-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08377 | RWB-P4-E1054-APP | DOR-RWB-P4-E1054-APP-10 | find it | Add empty, loading, error and no-access states for SCR-31 Document review queue |

### RWB-P7-E1054-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08383 | RWB-P4-E1054-APP | GAP-2456 |  | Take review codes and final-call values from LOV-DECISION and the final-call list via rwb-case reference data; keep DOCATT; actions and outcome keys documentRef, reviewStatus, reviewOutcome, fieldCount; allocate rwb_decision login in the secret store. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08385 | RWB-P4-E1054-APP | GAP-0746 |  | Hold case review task code, element type and task status values as reference data in rwb-case reference tables; load with RWB-P3-E1043-CON before the review queue story starts. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08387 | RWB-P4-E1054-APP | GAP-0756 | 13 | Add the rwb-case review switch as a parameter under key Not specified in the source documents (GAP-0756), stored in the platform flag library; off means no review task is raised and the queue answers no row. |

### OTHER:Reference-data contract and data dictionary (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08388 | RWB-P4-E1054-APP | GAP-0757 |  | Load the review task code, the review state values and the case-side decision code as reference rows; allocate field IDs for document_ref, review_reason, item_version and review_state on task at the next data dictionary version. Values Not specified in the source documents (GAP-0757). |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08390 | RWB-P4-E1054-APP | GAP-0758 |  | Agree the rwb-case per-service login name with RWB-PLT-NF06-DB and use it for grants, Flyway history and the connection pool. Name Not specified in the source documents (GAP-0758). |

### RWB-P3-E1043-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08396 | RWB-P4-E1062-APP | DOR-RWB-P4-E1062-APP-5 | 9 | Add PR1 to closed list LOV-DEVIATION and CALLER_KIND to closed list LOV-ROLE-CLASS |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:13; OTHER:45) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08398 | RWB-P4-E1062-APP | GAP-1816 | 12.2 | Carry FSD field names as source field names of the rwb-source-data contract; confirm party-flag, deceased-marker and freshness fields with P1 before the wave 2 system test |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:rwb-document and rwb-source-data contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08399 | RWB-P4-E1062-APP | GAP-1822 | 12.2 | Add a document read on rwb-document as an S8 dependency and a call-note field on the rwb-source-data contract; confirm with both owners before the shadow screening test |

### RWB-P4-E1062-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08400 | RWB-P4-E1062-APP | DOR-RWB-P4-E1062-APP-10 | 7 | Add empty, loading, error and no-access states to SCR-43 and SCR-47 in their screen definitions |

### OTHER:BRD (section 8.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08402 | RWB-P4-E1062-APP | GAP-1456 | find it | State in section 8.2 that the business-epic wave is kept and each story builds in its own wave, with the delivery lead confirming wave per story at build sequencing |

### OTHER:FSD S8 (features A2.2 to A2.9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08403 | RWB-P4-E1062-APP | GAP-1823 | find it | Rewrite each E2 main criterion to assert its own behaviour, carrying the FSD row unchanged as evidence, with the S8 owner and QA lead |

### OTHER:FSD S8 (deviation feature tables) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08404 | RWB-P4-E1062-APP | GAP-1826 | find it | Name R-DEV-19 to R-DEV-21 and the other unnamed rules of the 22-rule set as requirements; package authoring stays with rwb-decision |

### OTHER:TSD P4 v3 (appendix T-A; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08406 | RWB-P4-E1062-APP | GAP-2326 | find it | Add a row for POST /authorise (role, scope, DoA) with its agent-authority part, kept inside RWB-P4-E1037-CON |

### OTHER:FSD P10 v3 (A2.8.1 and AC-P10-008-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08409 | RWB-P4-E1062-APP | GAP-1532 | find it | Read the mode from the policy row, with one code path for shadow (Epic 1) and L1 (Epic 2), and retitle A2.8.1 to match |

### OTHER:FSD S8 (FSD v6 extract folder) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08414 | RWB-P4-E1062-APP | GAP-1834 |  | Add the v1 and v2 change notes, dates and contents to the FSD S8 version history; carry them as Not specified in the source documents (GAP-1834) until then. |

### OTHER:FSD S8 A2.1.4.1 and A2.7.4.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08415 | RWB-P4-E1062-APP | GAP-1833 |  | State the platform population figures NFR-001, NFR-002 and NFR-011 and the two evaluation samples of 200 and 500 cases; assert no module volume; size wave 2 after measuring the shadow run. |

### OTHER:TSD P5 (rwb-access masking contract; OTHER:T6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08418 | RWB-P4-E1062-APP | GAP-1049 | 8 | Publish the mask format, the per-role personal field list and the SY-AGENT policy version label; state that SY-AGENT holds Documents R with every personal field masked and no clear value in answer, log or trace. |

### OTHER:FSD P5 and TSD P5 (document_type read rule) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08419 | RWB-P4-E1062-APP | GAP-1050 | 8 | State that a stored document is served with the type on its row and is never re-typed on read; the unknown-type refusal (422, MSG-P5-006) applies at store time only. |

### OTHER:Access matrix PM-2026.11 (role.default_scope for the agent service identity) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08420 | RWB-P4-E1062-APP | GAP-2329 | 8 | Set the agent service identity default_scope to ALL in the matrix version in force, and state the default-scope rule for every NON_HUMAN_ACTOR role in the access and administration documentation. |

### RWB-P4-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08422 | RWB-P4-E1063-APP | DOR-RWB-P4-E1063-APP-16 | header | Size row marked as not specified |

### RWB-P10-E1058-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08426 | RWB-P4-E1063-APP | GAP-0644 | find it | Keep the three legacy admin operations on /api/recovery/agent/v1; leave report and configuration operations there; route reads via gateway-bff on that path; read LOV-DOC-TYPE from the rwb-case reference-data contract; read scores only through the evaluation read. |

### OTHER:Agent monitoring dashboard v2 app story (not named in this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08427 | RWB-P4-E1063-APP | GAP-0629 | find it | Place the drift step in the v1 Schedule workflow; read segment from the run row; read overrides via rwb-decision with the agent-version filter and three added elements; hold policy values in watch_measures; migration V10_007 with legacy index and one agent_feedback index; range limits as configuration; login rwb-agent (DP-02); route under RWB-PLT-N001-CON; right of API-P10-009 per its proposed fix. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08429 | RWB-P4-E1063-APP | GAP-2332 | find it | Publish the two dashboard-read access-event codes, the entry field list and the page bounds in the next access-log contract version; name the read index in the rwb_access physical schema; register the Flyway step and the two parameter codes in the service's own sequence and parameter set. |

### RWB-P6-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08432 | RWB-P4-E1063-APP | GAP-1209 | 15 | Seed the MSG-P10-004 template code, channel, notice type and outbox retry window as P6 parameter and reference rows; publish request and answer fields; declare the cost-alert read guard at gateway-bff. |

### OTHER:FSD P4 v3 and TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08437 | RWB-P4-E1063-APP | GAP-2333 | 18 | Correct REQ-ACA-006 and NFR-042 in the next FSD P4 and TSD P4 versions; replace the lake copy of the access rule with the served-read access entry; record Reporting letters for the other roles in the matrix load. |

### OTHER:TSD P4 v3 T6.1 (RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08445 | RWB-P4-E1064-APP | GAP-2307 | 10 | Grant an A letter in Reference data to one role in the next matrix version and name it approver of reference and dictionary loads; the submitting role may not also approve. |

### OTHER:rwb-case reference-data contract (DP-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08449 | RWB-P4-E1064-APP | GAP-0498 | find it | Publish GET /api/recovery/case/v1/reference-data/{tableCode} with its fake, one hop and a 2 s timeout; read every list through it. |

### OTHER:Work package plan generator (B-P1-02; OTHER:B2-P1-001) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08455 | RWB-P4-E1064-APP | GAP-2161 |  | Keep one WP per story slice for RWB-E1-064 on rwb-source-data; add a plan-uniqueness check that fails on duplicate 'Write only' output paths. |

### RWB-P1-E1064-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08456 | RWB-P4-E1064-APP | GAP-0500 |  | Carry each deployment value as a named chart value set per environment by the platform team; hard-code none, since no source gives the values. |

### RWB-P1-E1064-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08457 | RWB-P4-E1064-APP | GAP-1506 |  | Correct the seed (one product per object family, view physical types, two personal view fields, 'ACE (ingested from X)', counts 16 and 14) before the dictionary load. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; RWB-P4-E1022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08471 | RWB-P4-E1065-APP | GAP-0896 | 13 | Owner marked Not specified in the source documents (GAP-0896); key format and retirement rule stay in the template spec, DL39 and RWB-P4-E1022-APP. |

### RWB-S8-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08472 | RWB-P4-E1065-APP | GAP-3086 | find it | Publish the deviation seed profile, deviation count per case, shape-to-code mapping, stage contract operation and field names, R-DEV-05 and R-DEV-06 codes and owner roles, and test level of the ten legacy cases; keep the H row empty. |

### RWB-P4-E1037-CON; OTHER:catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08474 | RWB-P4-E1065-APP | GAP-0895 | 3 | Line 55 assigns location, format, version label and row count to RWB-P4-E1037-CON; the DEV-versus-SIT label question is marked Not specified. |

### OTHER:TSD P1 v3 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08476 | RWB-P4-E1065-APP | GAP-0502 |  | Publish the sandbox stage interface with its input and output profile, the four fixtures (full seed, empty seed, refused seed, timeout) and drift detection as a build failure. |

### OTHER:Work Package plan generator (B-P1-02; OTHER:B2-P1-001) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08480 | RWB-P4-E1065-APP | GAP-2161 | find it | Keep one Work Package per RWB-E1-064 story slice: remove the key from B-P1-02 fanout or retire B2-P1-001; number CG-B-P1-02-E1064 rows once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-P1-E1065-CON; RWB-P5-E1049-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08481 | RWB-P4-E1065-APP | GAP-1054 | find it | Fix held item count per exception shape and page count per item as seed parameters in RWB-P1-E1065-CON; name the DEV review reasons in RWB-P5-E1049-APP test data. |

### RWB-P1-E1065-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08482 | RWB-P4-E1065-APP | GAP-0503 | find it | Fix one DEV database rwb_sandbox per service release, build database rwb_sandbox_next, and read-only role rwb_sandbox_read granted SELECT only. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08483 | RWB-P4-E1065-APP | GAP-0897 | find it | Fix the rwb-access login in the platform DB story; publish the DEV-only read-only role and its grant list (SELECT on role and permission only) in the Service Template Specification; record the single-schema grant retirement with DP-15. |

### OTHER:Recovery Workbench Build Notes v6 (RWB-E1-065) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08486 | RWB-P4-E1065-APP | GAP-3168 |  | Build the sandbox from the 19 Flyway sequences plus the two view migrations and state the seeding order per schema. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08487 | RWB-P4-E1065-APP | GAP-1053 |  | Record the DEV storage account and container names, the rwb-document login and the DEV read-only role; publish the SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### OTHER:RWB-ACE-001 (ACE team dependency; OTHER:DL43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08495 | RWB-P4-E1069-APP | GAP-1505 | n/a | Accept RWB-ACE-001 scope and dates; keep the 14 Section B views, batch-status freshness and Tier 2 features behind flags until it lands; confirm fallback freshness source CG-9 before system test |

### OTHER:RWB-PLT-DB; OTHER:Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08496 | RWB-P4-E1069-APP | GAP-3155 | n/a | Name the per-service logins in the ACE DB stories of RWB-PLT-DB and state them in the next version of Environment and Deployment Design |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08497 | RWB-P4-E1069-APP | GAP-3156 | n/a | Split the V0002 and V0003 grant block into one grant per service login, keeping ace_view_owner and the 30 views with P1 |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08499 | RWB-P4-E1069-APP | GAP-0566 | find it | Publish the three read operations with response fields and problem body; record the rwb-source-data application, database and wave 1 integration slices and the 19-login proof. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Fields tab) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08502 | RWB-P4-E1069-APP | GAP-0259 | find it | Set Owner to P1 rwb-source-data (recovery view) on all 304 view fields; no other login holds a view grant. |

### OTHER:Handling tab (v4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08503 | RWB-P4-E1069-APP | GAP-0263 | find it | Replace the recovery identity SELECT on recovery.v_ace_* with rwb_source_data only; other services read via the P1 REST contract or Temporal, audited through ACE Common PII logging. |

### OTHER:TSD P1 v3 (T2; OTHER:T5.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08504 | RWB-P4-E1069-APP | GAP-0567 | find it | Carry the REST contract of Architecture v5 slides 15 and 41 (base /api/recovery/source-data/v1, 2 s client budget) into the next TSD version as a change note. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; OTHER:DP-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08505 | RWB-P4-E1069-APP | GAP-0569 | find it | Rename the service role to rwb_source_data; state the per-service schema and USAGE grant on schema recovery in the Service Template Specification; record the rename against DP-02. |

### OTHER:FSD P1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08506 | RWB-P4-E1069-APP | GAP-1509 |  | Record that this service holds the 365-day appraisal age rule as data and writes valuation_ext.stale_flag and valuation_ext.age_days until the owning function is assigned (OQ-P1-05). |

### OTHER:FSD P1 and TSD P1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08510 | RWB-P4-E1069-APP | GAP-0570 | 12 | ACE team lead to confirm the Tier 1 table list and publish the 21 names or the 22nd table name; keep the legacy grant block as the enumeration until then. |

### OTHER:Environment and Deployment Design; RWB-P1-E1069-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08512 | RWB-P4-E1069-APP | GAP-0904 | 16 | Fix the 19 per-service login names, then replace the placeholder 'the rwb-access login (DP-02)' in TC-E1-069-02 with the fixed name. |

### OTHER:Per-service module map for rwb-access (Not specified in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08514 | RWB-P4-E1069-APP | GAP-0906 | 16 | Publish the module map with an explicitly empty source-object list, and fix the BND-6 failure wording once in the service template. |

### OTHER:Story dependencies v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08515 | RWB-P4-E1069-APP | GAP-3233 |  | Keep the five Not carried rows visible in the trace; add an X row later only if the run books or the harness really wait for the named story. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08518 | RWB-P4-E2002-APP | CG-ALL-5136 | 13 | Create RWB-P7-E1073-CON, or name the existing story key that carries the rule-kit dependency of DP-04 in section 13. |

### OTHER:Story files folder: 04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08521 | RWB-P4-E2002-APP | DOR-RWB-P4-E2002-APP-21 | 12.1 | Publish the §12.1 operations and §12.3 event through a CON story (RWB-P4-E1037-CON or new RWB-P4-E2002-CON) and list it as a dependency. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08523 | RWB-P4-E2002-APP | DOR-RWB-P4-E2002-APP-8 | 12 | Event rename in §12.3 already applied (R-01263) |

### OTHER:TSD P4 (T6.1 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08525 | RWB-P4-E2002-APP | GAP-0907 |  | Add a Case record column for all roles, publish the 14-area matrix as data with RWB-P4-AD002-APP, and confirm the CASE_RECORD letters and default scopes with the matrix owner before PM-2026.12. |

### RWB-P2-E2002-CON; RWB-P2-E2002-OPS; RWB-P3-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08527 | RWB-P4-E2002-APP | GAP-0654 |  | Settle at the wave 2 contract review: rwb-integration login, case read, field sets, live and messageCode owner, settings owner, connection-matrix rows and the daily step. |

### RWB-P2-E2002-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08529 | RWB-P4-E2002-APP | GAP-0656 |  | Approve the identity, environment, trigger, alert and runbook assumptions at release readiness, with every threshold and endpoint held as an environment value. |

### OTHER:P7 decision contract (/api/recovery/decision/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08531 | RWB-P4-E2002-APP | GAP-0770 |  | Publish the rule-catalog row read by rule ID and package version in the P7 contract, returning action_text, owner_role, timer_spec, target queue code and outputs. |

### OTHER:Platform database story (19-schema list) and the Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08533 | RWB-P4-E2002-APP | GAP-0774 |  | Allocate the rwb-case database login with its schema, derive the name from the schema, hold the secret in Key Vault and record the login in the Service Catalog before first deployment. |

### OTHER:rwb-decision contract in the wave-2 contract baseline, with the RWB-P7 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08534 | RWB-P4-E2002-APP | GAP-2469 |  | Publish the registry version answer and decision-log item field names, the artifact column and what the checksum covers, the read page size, the service login and one refusal message ID before the baseline tag. |

### OTHER:rwb-decision decision-record contract (RWB-P7 story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08535 | RWB-P4-E2002-APP | GAP-2471 |  | State one entry per case, business date and rule identity, with one entry per rule for a transaction running two rules; publish the content model of the inputs snapshot and actions payload. |

### RWB-P7-E1073-CON; RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08537 | RWB-P4-E2002-APP | GAP-1336 |  | Fix the model answer, the inputs snapshot and the announcement payload with their element names, name the plan-status section with the gateway-bff route owner, and publish the per-service login before wave 2 build. |

### RWB-PLT-E1027-CON; RWB-ITG-E2002-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08538 | RWB-P4-E2002-APP | GAP-1338 |  | Settle whether a route move running two rules is one entry with the second rule in its actions or two entries for the date, then align the harness and case story to that answer. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08541 | RWB-P4-E2002-APP | GAP-2470 |  | Complete the RWB-P7 metadata rows from the DP table, and state in R5.5 that platform H rows and self-referential C rows are held by platform and contract stories and not repeated on the APP line. |

### OTHER:P1 contract story for rwb-source-data (reconciliation_result) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08543 | RWB-P4-E2002-APP | GAP-0772 | find it | Publish a break operation on the rwb-source-data contract (product, check, key, detail, owner role) and have the plan-status step call it once per rejected or missing plan. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08545 | RWB-P4-E2002-APP | GAP-1337 | find it | Carry the platform contracts and rwb-case rule-package, parameters and reference-data contracts in the dependency map; keep metadata rows as fixed. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; RWB-P2-E2003-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08549 | RWB-P4-E2003-APP | DOR-RWB-P4-E2003-APP-7 | 11 | Add or confirm BR field ID DF-REF-039 in LDM v9; P2 Criteria and test data must read through the rwb-source-data contract, not ACE views directly. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3; RWB-P1-E1069-CON; RWB-P3-E1043-CON; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08551 | RWB-P4-E2003-APP | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | 3 | Flag name removed from section 3; the switch is described without a name. |

### RWB-PLT-N001-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:integration harness record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08552 | RWB-P4-E2003-APP | GAP-0390 | 16 | Publish the gateway-bff composite route and merge order; agree the harness repository, environments, seed data, evidence format and gate; publish the rwb_access field IDs in the next LDM. |

### RWB-P4-E1037-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08554 | RWB-P4-E2003-APP | CG-ALL-5151 | 3, 3.1 | Record the next free number in the rwb-access V0001 to Vnnnn sequence, so RWB-P4-E2003-APP can name its migration in place of V2003_1__other_products_masking.sql. |

### OTHER:Not specified in the source documents (GAP-0914) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08555 | RWB-P4-E2003-APP | It is not settled who writes the PII access event for the composed other-products read | 8 | BR10 restored to its prior wording; no writer named. |

### RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08556 | RWB-P4-E2003-APP | GAP-0916 | 8 | Name the rwb_access database login and grant it SELECT on schema rwb_access only |

### 02 Business architecture and process/Recovery Workbench Role to System Access Matrix v3.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20603 | RWB-P4-E1062-APP | R-28647 |  | Matrix has no default_scope column. The rule belongs in TSD P4 Access and administration v4.md, with the schema value in rwb_source_data.sql. Workbook not opened. |

### 04 User stories/Recovery Workbench ACE Team Stories v2.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20611 | RWB-P4-E1069-APP | R-09195 |  | Flags, Tier 2 and CG-9 belong to consumer stories RWB-P1-E1069-APP and RWB-P1-E1015-APP. This story already states its legacy RWB-ACE-001 scope (line 47). No fix. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20776 | RWB-P4-E1063-APP | R-22234 |  | The served-read access entry wording is not in the sources, so REQ-ACA-006 is unchanged. NFR-042 is not in this FSD. Reporting letters belong to the story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20852 | RWB-P4-E2002-APP | R-22336 |  | Ledger and inputs snapshot/actions content model belong to the rwb-decision decision-record contract, not this file. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0014 | Table inventory does not cover the v5 schema-per-service model and the FK cuts are empty | Solution architect and ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0110 | The map does not say which schema holds the 30 ACE views | ACE team | Resolved (directive) |
| GAP-0111 | The source grants use placeholder roles and do not create the 19 logins | ACE team | Resolved (directive) |
| GAP-0259 | The 30 ACE source views have no owner in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0263 | One recovery identity reads the ACE views; the target has one login and one schema per service | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0365 | Review queue operation names, scope source and attach evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0371 | Rule-row owner lookup, interaction ledger read and deviation-absence evidence are not named for the target | P10 agent owner, P7 decision owner, P1 source data owner, S8 deviation owner and P4 access owner | Resolved (directive) |
| GAP-0372 | Data lake removed: agent daily read model, reporting read and job rerun owner are not named for the target | P10 agent owner, P9 reporting owner, P1 source data owner, P6 comms owner and P2 integration owner | Resolved (directive) |
| GAP-0373 | Reference-load operation owner, ACE view value read and contract confirmation form are not named for the target | P1 source data owner, P3 case owner and P4 access owner | Resolved (directive) |
| GAP-0374 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | Solution architect | Resolved (directive) |
| GAP-0377 | The 19 login names, the grant matrix on the 30 ACE views and the two-part boundary rule after the schema split are not stated | ACE database administrator | Resolved (directive) |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0390 | Customer other-products harness pack: repository, environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0498 | The read of the rwb-case reference-data contract that returns a table of values is not specified | Solution architect | Resolved (directive) |
| GAP-0499 | The field-level detail of the five dictionary schemas and the login wording of the contract baseline are not specified | Tech lead | Resolved (directive) |
| GAP-0500 | No deployment value, probe timing, alert threshold or incident route exists for the dictionary slice | DevOps lead | Resolved (directive) |
| GAP-0501 | The sandbox scope per service and the placement of the generator module are not specified | Solution architect | Resolved (directive) |
| GAP-0502 | The contract of a build tool is not described by any source document | Tech lead | Resolved (directive) |
| GAP-0503 | The sandbox database scope and its read-only role name are not specified | ACE data architect | Resolved (directive) |
| GAP-0554 | Where the masking of the ACE-sourced personal fields is answered is fixed in another service's story, while this story may declare no contract dependency and no masking pattern | Solution architect | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0567 | The ACE read is a REST contract of rwb-source-data in Architecture v5 and an in-process Java interface in TSD P1 and legacy RWB-E1-069 | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0568 | rwb-source-data database slice: who creates the login and holds its credential, the exact grant names, the position of the three grant migrations on the sequence, and the platform sequence dependency of a Day-1 database story are not specified | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0569 | The service role is recovery_svc on one recovery schema in TSD P1 and legacy RWB-E1-069, and a per-service login rwb_source_data with its own schema under Architecture v5 | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0570 | The number of Tier 1 ACE tables is 21 in legacy RWB-E1-069 and 22 in FSD P1 and TSD P1, and the grant list is enumerated only in the legacy story | ACE team lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0614 | The screening slice in rwb-agent: the run-start path, the parameter and ledger operation paths, the two added events, the screening feature flag, the boundary status of a failed tool call and the route in front of the reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-deviation, rwb-case, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0615 | The screening contract slice: the run-start path and request members, the member types of the proposal payload, the two added event names and payloads, the consumed paths no source names and the route name are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0616 | Agent monitoring dashboard in rwb-agent: the data lake of the legacy story is removed, and the schedule name, the service login, the route path, the notification operation and the home of the daily aggregate are not specified | Solution architect | Resolved (directive) |
| GAP-0617 | Agent monitoring contract in rwb-agent: the page size and cursor, the member types of the aggregate element, the held-date status members, the Schedule name, the route path and the notification operation are not specified | Solution architect | Resolved (directive) |
| GAP-0618 | Agent monitoring deployment in rwb-agent: the topology, host, SKU, budget, route path, login, feed retention and alert thresholds are not specified | Platform administrator | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0644 | Extraction evaluation in rwb-agent: service login, document-type owner, admin operation set, route path and score read path | Solution architect | Resolved (directive) |
| GAP-0654 | rwb-integration ACE plan status: the login, the account resolution, the interface field types, the meaning of live and messageCode, the two settings, the connection-matrix rows and the ownership split are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0655 | The plan-status contract baseline: the accountNo field, the meaning and owner of live and messageCode, the interface null rules, the consumed read shapes, the composite route and the two specification conflicts are not fixed by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0656 | The plan-status deployment values, the ACE endpoint and certificate references, the two setting values at run time, the trigger wiring, the alert thresholds, the mapping of the no-package condition and the fixture owner are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0662 | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0755 | Review team for a review item with no case: the legacy value is assumed and the parameter has no agreed owner | RW-COE | Resolved (directive) |
| GAP-0756 | The rwb-case feature switch of the review queue has no name in any source | RW-COE | Resolved (directive) |
| GAP-0757 | The review task code, the review state values, the case-side decision code and the field IDs of the review link columns are not specified | RW-COE | Resolved (directive) |
| GAP-0758 | The rwb-case per-service login name is not specified | RW-SECADM | Resolved (directive) |
| GAP-0769 | The hand-over of the plan status between rwb-integration and rwb-case, and its batching, are not specified | Solution architect | Resolved (directive) |
| GAP-0770 | No published operation reads a rule catalog row by rule ID and package version | P7 decision owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0771 | The plan event map has no table code in LOV-REF-TABLE and no target table or column | Reference data owner (RW-COE) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0772 | The delivery path of a plan-status break to the data-quality console is not specified | P1 source data owner | Resolved (directive) |
| GAP-0773 | The gateway-bff composite route of the case record plan section is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0774 | The per-service database login name of rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0902 | rwb-access ACE masking pack: no source names the masking version label | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0903 | rwb-access ACE masking pack: no source holds the roster of roles that see a personal field unmasked | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0904 | rwb-access: the per-service database login name is named by no source | ACE team lead and ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0905 | rwb-access: unclear whether this service may hold masking rows that key on the P1 field catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0906 | rwb-access: the boundary rule has no allowed-object list and no build-log wording for this service | Tech lead, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0907 | rwb-access plan status: the TSD RBAC matrix has no Case record column, so the CASE_RECORD letters this slice decides are not tabulated for any role | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0908 | rwb-access plan status: the authorise request and answer shapes and the resolved permission view are absent from the TSD P4 appendix, including whether the plan reference travels in the authorise request | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0909 | rwb-access plan status: the per-service login name and the gateway-bff composite route field list behind SCR-03 and the plan status panel are not specified | Solution architect | Resolved (directive) |
| GAP-0913 | The field list and the masking step of the gateway-bff composite route for the other-products panel are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0914 | It is not settled who writes the PII access event for the composed other-products read | Solution architect | Resolved (directive) |
| GAP-0915 | The field names of the masking answer inside the authorise reply and the masking-policies read are not specified | Solution architect | Resolved (directive) |
| GAP-0916 | The per-service database login name of rwb-access is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0988 | The review-item authorise request shape, the label of the matrix and masking versions in force at the release date, and the review-field roster of the masking pack are fixed by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1011 | No source fixes the field-level names of the nine review resources, the one resolve answer, the field-patch idempotency, the document read position or the three platform message texts | Tech lead of rwb-document with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1047 | The agent's document-read tool contract is not defined in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1048 | The idempotency-key format of DocumentStored and the event field names the agent reads are not defined | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1049 | The mask format and the per-role list of personal fields for SY-AGENT are not defined | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1050 | The read behaviour for a stored document whose type has left the version in force is not defined | Business analyst, P5 | Resolved (directive) |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1052 | The file-name pattern of the synthetic documents is not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1209 | Template code, channel, notice type, field names, recipient role holders, guard right and retry window are not named for the target | P6 comms owner, P10 agent owner and platform notification path owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1210 | The legacy data lake copy and the agent monitoring dashboard have no target, and P6 has no replacement for the dashboard | P6 comms owner, P9 reporting owner and architecture owner | Resolved (directive) |
| GAP-1211 | The agent alert event name, the alert notification operation name and the non-case binding of the cost alert are not named for the target | P10 agent owner and P6 comms owner | Resolved (directive) |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1336 | Shape of the model answer, of the inputs snapshot and of the announcement, with the carrier names of the plan-status move | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1338 | One ledger entry per route move or per case and business date, for a move that runs two rules | Solution architect | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1505 | The Section B views and every Tier 2 feature depend on ACE additions that the ACE team has not accepted | ACE team lead | Resolved (directive) |
| GAP-1506 | The physical dictionary mapping and the system-of-record wording disagree with the frozen view list | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1509 | Which function writes the appraisal stale flag and age is not set | Business analyst, P1 and S1 | Resolved (directive) |
| GAP-1516 | FSD P10 v3 publishes the agent dashboard through a data lake write and Power BI, both removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1517 | The daily aggregate table the FSD acceptance criteria name is not in the Logical Data Model v8 entity list | Solution architect | Resolved (directive) |
| GAP-1519 | JOB-15 is the reporting extract of rwb-reporting in the Ownership Map, but the FSD uses its completion as the trigger of the P10 dashboard | Platform administrator | Resolved (directive) |
| GAP-1532 | The screening feature is titled at L1 and its main criterion stores a shadow run that creates no deviation | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1593 | Two FSD features assert the same review-queue criteria and the correction feed has no distinct criterion | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2040 | The view conformance test of RWB-E1-069 is split across two services | P1 rwb-source-data with the ACE DBA | Resolved (directive) |
| GAP-2137 | Which service seeds which rows of the shared case set is not specified | QA | Resolved (directive) |
| GAP-2154 | The seed, business date, volumes and identifiers of the synthetic fixture set are not stated | QA lead | Resolved (directive) |
| GAP-2161 | Two Work Packages write the same three story files and three fragments for legacy RWB-E1-064 on rwb-source-data | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2456 | The review decision codes and outcome values, the placement of the review facts in the record, and the rwb-decision login name are in no source | Solution architect with the reference-data owner and the ACE team | Resolved (directive) |
| GAP-2469 | RWB-P7-E2002-APP: the values of the version answer, the entry payload, the artifact reference, the service login, the page size and the model-refusal message are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2471 | RWB-P7-E2002-APP: the width of one ledger entry is ambiguous where a move runs two rules in one transaction, and no source fixes the payload that carries the plan facts | Service owner of rwb-decision with the rwb-case service owner and the data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2472 | RWB-P7-E2002-APP: the legacy story sits in Module P2 Integration and names the plan-status endpoint on the monolith base, while the plan gives this APP slice to rwb-decision and the read to rwb-integration | Solution architect with the rwb-decision and rwb-integration service owners | Resolved (directive) |
| GAP-3085 | RWB-S8-E1062-APP: the deviation estate the shadow screening run reads has no read operation, no published agent-policy read, no owner role for R-DEV-05 and R-DEV-06, no value for the answer limit and no test level | Solution architect, with the rwb-deviation owner, the rule-set owner of the Deviations package, the rwb-agent contract owner, the rwb-case parameter and reference-data owners, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3155 | The per-service login names are not fixed in any source | ACE DB lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3156 | The V0002 and V0003 grant block gives one monolith login, not one login per service | ACE DB lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3168 | The sandbox story applies three migrations where 19 schemas now need their own sequence | ACE DB lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P4-E1065-APP | skipped AC ID | 101 | missing: AC9 |
| RWB-P4-E1065-APP | Not specified without item ID | 366 | - The login is the rwb-access login (DP-02); the DEV-only read-only role name is Not specified in the source documents for the target schema (GAP-0897; ASM-1618 |
