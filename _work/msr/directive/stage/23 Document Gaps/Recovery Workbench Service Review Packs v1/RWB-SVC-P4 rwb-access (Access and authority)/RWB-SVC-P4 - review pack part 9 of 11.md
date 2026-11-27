# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 9 of 11 (RWB-P4-E2027-APP to RWB-P4-E8007-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 214 |
| Cross-document (pending in another document) | 230 |
| Not applied (value not in the sources) | 21 |
| Open business decisions | 29 |
| Register gaps linked | 145 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E2027-APP | 21 | 38 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2027 APP Payment matching rules with the data team v2.md |
| RWB-P4-E2031-APP | 16 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2031 APP Agent monitoring dashboard v2 [E3d] v2.md |
| RWB-P4-E2033-APP | 18 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2033 APP Case and queue list with status, owner and ageing v2.md |
| RWB-P4-E2034-APP | 25 | 21 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2034 APP Interaction ledger on the case and from every channel v2.md |
| RWB-P4-E2035-APP | 28 | 29 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2035 APP Next action on the case v2.md |
| RWB-P4-E2036-APP | 20 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2036 APP Queue write interface for models and agents v2.md |
| RWB-P4-E2041-APP | 22 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2041 APP Rule change governance and audit report v2.md |
| RWB-P4-E2042-APP | 19 | 37 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2042 APP Epic 2 rule packages in Drools v2.md |
| RWB-P4-E8006-APP | 14 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E8006 APP Run the full administration screens v2.md |
| RWB-P4-E8006-CON | 17 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E8006 CON Run the full administration screens - contract v2.md |
| RWB-P4-E8007-APP | 14 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E8007 APP Change a decision rule through the administration screens v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E2031-APP | R-01327 | CG-ALL-5341 | Script gap | Product owner | The story adds BKK to the closed list LOV-CAPABILITY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2031-APP | R-01328 | CG-ALL-5342 | Script gap | Product owner | The story adds BKK to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2033-APP | R-01330 | CG-ALL-5351 | Script gap | Product owner | The story adds CAR to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2033-APP | R-01331 | CG-ALL-5352 | Script gap | Product owner | The story adds CAR to the closed list LOV-CAPABILITY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2033-APP | R-01332 | CG-ALL-5353 | Script gap | Product owner | The story adds CAR to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2035-APP | R-01337 | CG-ALL-5374 | Script gap | Product owner | The story adds CUSTOMER_PARTY to the closed list LOV-CAPABILITY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2035-APP | R-01338 | CG-ALL-5375 | Script gap | Product owner | The story adds CUSTOMER_PARTY to the closed list LOV-ROLE-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2035-APP | R-01339 | CG-ALL-5376 | Script gap | Product owner | The story adds CUSTOMER_PARTY to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2041-APP | R-01347 | CG-ALL-5406 | Script gap | Product owner | The story adds APPROVE to the closed list LOV-CAPABILITY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E2031-APP | R-10752 | CG-ALL-5347 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2033-APP | R-10755 | CG-ALL-5362 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-P4-E2035-APP | R-10762 | CG-ALL-5387 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2035-APP | R-10763 | CG-ALL-5393 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-P4-E2042-APP | R-10772 | CG-ALL-5422 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E8007-APP | R-10775 | CG-ALL-5452 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-ITG-E2041-ITG, RWB-P3-E2041-APP, RWB-P3-E2041-CON, RWB-P4-E2041-APP, RWB-P7-E2041-APP | R-22719 | GAP-0963 | Register gap | Solution architect with internal audit | The record code and the field shape of a rule-change authority and of an audit export inside a decision-record entry are not specified | Carry the capability area, the right, the action, the version label, the author reference, the period, the package, the format, the row count and the matrix version in the actions list of the decision-record entry, reuse AC-READ, AC-DENY and AC-EXPT rather than minting a fourth code, and add the fields in the next LDM version with audit. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28853 | GAP-1560 | Register gap | AI product owner | The queue write interface for models and agents has no approved consumer and no flag removal date | Name the first approved consumer and the flag removal date before the wave 2 release. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-P4-AD011-APP, RWB-P4-E8007-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON | R-28970 | GAP-0878 | Register gap | Business analyst, with the compliance and PDPA officer | The legacy story carries a rule-change capability it does not have | Keep the capability, the two criteria, the five messages and the four test ids, leave the rule-version endpoints and the rule_row row with RWB-P4-E8007-APP and RWB-P4-AD011-APP, and read the rule version of AC1 as the version of the parameter row in force. |
| RWB-P4-E2033-APP | R-33448 | ASM-ALL-5362 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-P4-E2035-APP | R-33449 | ASM-ALL-5393 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-P4-E2036-APP | R-36803 | ASM-1693 | Register assumption |  | The access entry of a placement admission carries decision code AC-READ and the entry of a refusal carries AC-DENY, with the calling service identity, the caller code, the caller type, the model or agent version, the reason code, the target queue, the team code, the case, the product group, the matrix version, the masking version, the field IDs marked and the time; the column set of the decision_record library table is left to RWB-PLT-E1027-CON. | internal audit at the access-log story (RWB-P4-AD007-APP) and the platform library owner at RWB-PLT-E1027-CON |
| RWB-P4-E2041-APP | R-36805 | ASM-1695 | Register assumption |  | A rule-change authority is written under AC-READ when it is granted and under AC-DENY when it is refused, and an export under AC-EXPT, reusing the three codes of FSD P4 v3 A2.7 and A2.16 and minting no fourth code. The entry carries the caller reference, the capability area, the right, the action, the version label and the author reference where an approval was asked, the period, the package, the format, the row count and the matrix version in the actions list, with the case id empty. | Solution architect with internal audit in the next LDM version |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E2027-APP | R-05862 | DOR-RWB-P4-E2027-APP-14 | not in supplied text | Definition of Ready item 14 Epic design: Fail | No signed epic design record for EP02 or this story in the sources; ways-of-working and DT05 state only the rule. Sign-off cannot be stated. |
| RWB-P4-E2027-APP | R-05866 | DOR-RWB-P4-E2027-APP-22 | not in supplied text | Definition of Ready item 22 Fake published: Fail | Story section 8 text not supplied, so no anchor. No contract fake library version for this story in sources; 04 User stories names only other stories' fakes. |
| RWB-P4-E2027-APP | R-05867 | DOR-RWB-P4-E2027-APP-23 | not in supplied text | Definition of Ready item 23 Contract version fixed: Fail | Story section 9 text not supplied, so no anchor. Sources give only base /api/recovery/access/v1 (DP-13) with no contract version number. |
| RWB-P4-E2027-APP | R-16849 | DOR-RWB-P4-E2027-APP-18 | 19 | Definition of Ready item 18 Open decisions: Partial | Open decision DL10 and its assumptions sit in section 19, which is not in the supplied story text. Re-run with section 19 to edit. |
| RWB-P4-E2027-APP | R-22630 | GAP-0409 | 16 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | ALS fixture, JOB-07 window, load route, harness seeding and evidence format are in no source read. Needs P8, P7, integration lead and QA agreement. |
| RWB-P4-E2033-APP | R-05877 | DOR-RWB-P4-E2033-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story copy (Grep for sign-off text found none) or the sources. Adding a sign-off would invent a value. Left unedited. |
| RWB-P4-E2033-APP | R-16862 | DOR-RWB-P4-E2033-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Section 18 text is not in this chunk, so no exact 'old' text exists. DL31 has no assumption; adding one would invent a value. Story line 476 ties DL31 to the designer. |
| RWB-P4-E2034-APP | R-25539 | CG-ALL-5370 | 3, 3.1 | Flyway file V2034_1__ledger_access_read_path.sql is not in the V0001..Vnnnn form | Next free rwb_access Flyway number is not in the sources. Migration name line (story file ~L381) is not in the supplied story text, so no edit. Solution architect to supply the number. |
| RWB-P4-E2034-APP | R-30975 | NEWAC-RWB-P4-E2034-APP-AC16 | 7, 16 | AC16: replay of a write with the same idempotency key (no criterion covers a replay) | Story has no write operation (section 3: adds no operation) and no idempotency key in sources. No replay AC written without inventing a write; proposed test stays Not specified. |
| RWB-P4-E2035-APP | R-16875 | DOR-RWB-P4-E2035-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The personal-data field is not named in the item, the story, or the RWB-P4 review (CG-ALL-5387 row). Naming one would invent a value. |
| RWB-P4-E2035-APP | R-25545 | CG-ALL-5388 | 3, 3.1 | Flyway file V2035_1__nextaction_access_read_path.sql is not in the V0001..Vnnnn form | Story text has no V2035_1 name (line 381 reads None). Service Template Spec v1 §3.1 gives only V0001 to Vnnnn. The next rwb_access number is not in the sources. |
| RWB-P4-E2041-APP | R-05907 | DOR-RWB-P4-E2041-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-P4-E2041-APP in the story or sources; searched all .md sources, no match. Sign-off cannot be cited. |
| RWB-P4-E2041-APP | R-05911 | DOR-RWB-P4-E2041-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version recorded for RWB-P3-E2041-CON; searched all .md sources, no match. Version cannot be cited. |
| RWB-P4-E2042-APP | R-16893 | DOR-RWB-P4-E2042-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The P2 fields classed as personal data are not named in this chunk or the sources; the detcheck message alone cannot supply a field name. |
| RWB-P4-E2042-APP | R-28856 | GAP-1302 | find it | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Package title, dry-run breakdown, MSG-P3-015 text, rollback body and switch-off answer sit in sections not in this chunk. No placeholder edit possible here. |
| RWB-P4-E2042-APP | R-28866 | GAP-1299 | find it | The name of the rwb-decision database login is not specified | The rwb-decision login name is not in the sources (PRD P7 rwb-decision v1 says only 'a login'). The text naming it is not in this chunk, so no edit. |
| RWB-P4-E2042-APP | R-28867 | GAP-1300 | 14 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | MSG-P3-027 detail wording is in section 14, which is not in this chunk. Cannot edit without its exact text. |
| RWB-P4-E2042-APP | R-28873 | GAP-1296 | 13, 18 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | The DP-added H and C dependency text is in sections 13 and 18, not in this chunk. Metadata rows stay as written; the carry-over needs a separate edit. |
| RWB-P4-E2042-APP | R-28874 | GAP-2398 | 13, 18 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | The eleven DP-added rows belong in sections 13 and 18, not in this chunk. Metadata rows unchanged; needs a separate edit of those sections. |
| RWB-P4-E8006-APP | R-05922 | DOR-RWB-P4-E8006-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in sources. Grep of all .md sources for 'epic design' found only scratch, decision-log and other-story hits. Sign-off cannot be confirmed. |
| RWB-P4-E8006-CON | R-05928 | DOR-RWB-P4-E8006-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed EP08 epic design record ID in the sources. Grep of the folder found none for this story; the stakeholder map names only a sign-off pack per epic. Needs the record ID. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (23)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08946 | RWB-P4-E2027-APP | CG-ALL-5332 | 4 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as reference data without a schema change. |
| CDC-08947 | RWB-P4-E2027-APP | DOR-RWB-P4-E2027-APP-8 | 12.3 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as reference data without a schema change. |
| CDC-09004 | RWB-P4-E2033-APP | CG-ALL-5354 | find it | Remove the closed enum on defaultScope so LOV-SCOPE values are read as data, as this story and Reference Data v5 Lists state. |
| CDC-09006 | RWB-P4-E2033-APP | DOR-RWB-P4-E2033-APP-8 | find it | Remove the closed enum on defaultScope; LOV-SCOPE is data per ruling R-01333. |
| CDC-09018 | RWB-P4-E2034-APP | CG-ALL-5363 | 12.1 | Publish POST /api/recovery/access/v1/authorise through RWB-P4-E1037-CON, or remove it from the story. |
| CDC-09019 | RWB-P4-E2034-APP | CG-ALL-5364 | 12.1 | Publish GET /api/recovery/access/v1/admin/access-log through RWB-P4-E1037-CON, or remove it from the story. |
| CDC-09022 | RWB-P4-E2034-APP | DOR-RWB-P4-E2034-APP-8 | 12.1 | Declare an idempotency key on POST /api/recovery/access/v1/authorise; key name not specified in the source documents. |
| CDC-09043 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-8 | find it | Hold roleClass and defaultScope as references to LOV-ROLE-CLASS and LOV-SCOPE, not closed enums; use event type rwb.decision.DecisionRecorded.v1 and the Kafka Catalog v1 payload for AccessPolicyChanged.v1. |
| CDC-09068 | RWB-P4-E2036-APP | CG-ALL-5395 | n/a | Remove the closed enum on roleClass so the values come from LOV-ROLE-CLASS as data, as the story reads them. |
| CDC-09069 | RWB-P4-E2036-APP | CG-ALL-5396 | n/a | Remove the closed enum on defaultScope so the values come from LOV-SCOPE as data, as the story reads them. |
| CDC-09072 | RWB-P4-E2036-APP | DOR-RWB-P4-E2036-APP-8 | 12.3 | Remove the closed enums on roleClass and defaultScope so LOV-ROLE-CLASS and LOV-SCOPE are data. |
| CDC-09087 | RWB-P4-E2041-APP | CG-ALL-5407 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON (the DP-08 authorise contract). |
| CDC-09139 | RWB-P4-E8006-APP | CG-ALL-5425 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths through the rwb-access provider CON story |
| CDC-09140 | RWB-P4-E8006-APP | CG-ALL-5426 | 12.1 | Remove the fixed enum on roleClass so it reads LOV-ROLE-CLASS as data |
| CDC-09141 | RWB-P4-E8006-APP | CG-ALL-5427 | 12.1 | Remove the fixed enum on defaultScope so it reads LOV-SCOPE as data |
| CDC-09143 | RWB-P4-E8006-APP | DOR-RWB-P4-E8006-APP-8 | 12.2 | Publish the authorise path and remove the fixed enums on roleClass and defaultScope |
| CDC-09149 | RWB-P4-E8006-CON | CG-ALL-5436 | 12.1 | AC1 and section 11 give the full path /api/recovery/access/v1/admin/home; the path is still to be published in rwb-access.yaml. |
| CDC-09150 | RWB-P4-E8006-CON | CG-ALL-5437 | 12.2 | Publish POST /api/recovery/access/v1/authorise |
| CDC-09151 | RWB-P4-E8006-CON | CG-ALL-5438 | 12.1 | Remove the fixed enum on roleClass; LOV-ROLE-CLASS values are data |
| CDC-09152 | RWB-P4-E8006-CON | CG-ALL-5439 | 11 | Remove the fixed enum on defaultScope; LOV-SCOPE values are data |
| CDC-09153 | RWB-P4-E8006-CON | DOR-RWB-P4-E8006-CON-8 | 12.1 | Publish GET admin/home and POST authorise; remove roleClass and defaultScope enums; close the remaining detcheck item |
| CDC-09161 | RWB-P4-E8007-APP | CG-ALL-5448 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation. |
| CDC-09165 | RWB-P4-E8007-APP | DOR-RWB-P4-E8007-APP-8 |  | Publish POST /api/recovery/access/v1/authorise (CG-ALL-5448). The event-name fix (CG-ALL-5449) is applied in this story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08950 | RWB-P4-E2027-APP | DOR-RWB-P4-E2027-APP-12 | 16, 18 | Align the test lists of section 18 to TC-E2-027-11 to TC-E2-027-18 of RWB-P4-E2027-APP. |
| CDC-08976 | RWB-P4-E2027-APP | CG-ALL-5336 | 18 | Section 18 requirements row now reads TC-E2-027-11 to TC-E2-027-21 |
| CDC-08998 | RWB-P4-E2031-APP | §18 test lists differ from RTM v7 | 18 | REQ-DRI-009 and REQ-APD-005 test lists reverted to the prior values; new REQ-ACA rows kept |
| CDC-09016 | RWB-P4-E2033-APP | CG-ALL-5359 | 18 | In the next version align REQ-WKM-002 and REQ-DVH-006 test lists with section 18 of this story, or record the difference. |
| CDC-09037 | RWB-P4-E2034-APP | CG-ALL-5369 | 18 | Align the test lists of the nine requirements in RTM v7 with section 18 of this story in its next version; the full RTM list is cut off in the evidence. |
| CDC-09060 | RWB-P4-E2035-APP | CG-ALL-5386 | 18 | Align the RTM v7 test lists for REQ-WKM-012 to REQ-WKM-016 with section 18 of this story in its next version. |
| CDC-09085 | RWB-P4-E2036-APP | CG-ALL-5401 | 18 | Align the test lists of REQ-CWC-017, REQ-CWC-018 and REQ-CWC-019 with RWB-P4-E2036-APP section 18 in the next RTM version |
| CDC-09098 | RWB-P4-E2041-APP | CG-ALL-5411 | 18 | Align REQ-CWC-013 and REQ-DRI-011 test lists in RTM v7 with section 18 of RWB-P4-E2041-APP for every TC-E2-041 row. |
| CDC-09115 | RWB-P4-E2042-APP | GAP-2503 |  | Declare the nine consumed operations on the per-service bases; name workflow matchPayments with its four activities; record in RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story. |
| CDC-09128 | RWB-P4-E2042-APP | CG-ALL-5421 | 18 | Align the test lists for REQ-CWC-013 and REQ-CWC-014 with section 18 of RWB-P4-E2042-APP in the next RTM version. |
| CDC-09147 | RWB-P4-E8006-APP | CG-ALL-5430 | 18 | Align the test lists of REQ-ACA-002, REQ-ACA-003 and REQ-CWC-006 with section 18 of RWB-P4-E8006-APP in the next RTM version. |
| CDC-09157 | RWB-P4-E8006-CON | CG-ALL-5442 | 18 | Align the test trace of REQ-ACA-002, REQ-ACA-003 and REQ-CWC-006 with §18 of RWB-P4-E8006-CON in the next RTM version. |
| CDC-09170 | RWB-P4-E8007-APP | CG-ALL-5451 | 18 | Align the test lists of REQ-CWC-013, REQ-CWC-014 and the third requirement with section 18 of RWB-P4-E8007-APP |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08989 | RWB-P4-E2031-APP | CG-ALL-5344 | 14 | Add a new message ID for 'A drill-down names an agent the metric answer does not hold' with text '{record} was not found.'; section 14 then cites it. |
| CDC-09007 | RWB-P4-E2033-APP | CG-ALL-5356 | 4, 14 | Add a new message ID for 'A contract does not answer inside its budget' so MSG-GEN-006 keeps its R-UNI-33 meaning; then the story cites that ID in section 14. |
| CDC-09023 | RWB-P4-E2034-APP | CG-ALL-5366 | 4, 14 | Add a new message ID for 'Two roles of the caller conflict' with text '{role} may not be held together with {role}.'; keep MSG-P4-006 for its standard meaning. |
| CDC-09025 | RWB-P4-E2034-APP | DOR-RWB-P4-E2034-APP-9 | 14 | Add a new message ID for the role conflict text, as in CG-ALL-5366; the section 14 MSG-P4-006 row cites it once issued. |
| CDC-09045 | RWB-P4-E2035-APP | CG-ALL-5382 | 4, 14 | Add a new message ID for the text '{role} may not be held together with {role}.'; the story cites it in §14 once it exists. MSG-P4-006 stays as the standard holds it. |
| CDC-09074 | RWB-P4-E2036-APP | CG-ALL-5398 | 4, 14 | Add a new message ID for the no-role, no-session or no-token caller; the story then cites it in place of MSG-P4-001. |
| CDC-09076 | RWB-P4-E2036-APP | DOR-RWB-P4-E2036-APP-9 | 14 | Add the new message ID for the no-role, no-session or no-token caller, as under CG-ALL-5398. |
| CDC-09109 | RWB-P4-E2042-APP | CG-ALL-5418 | 14 | Add a new message ID for 'The change checklist is incomplete, so the version cannot be approved'; section 14 cites it in place of MSG-P3-022 once the ID exists. |
| CDC-09111 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-9 | 14 | Add a message ID for the incomplete change checklist and let section 14 cite it in place of MSG-P3-022. MSG-P3-027 text is already copied. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09024 | RWB-P4-E2034-APP | DOR-RWB-P4-E2034-APP-7 | 11 | Confirm DF-REF-039 is listed for the role table, or drop it from the range; the story keeps DF-REF-034 to DF-REF-039 until then. |
| CDC-09047 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-7 | 11 | Confirm or add DF-REF-039 as a field ID of table role in rwb_access |
| CDC-09073 | RWB-P4-E2036-APP | CG-ALL-5394 | 12.7 | Record `decision_record` as the PLT decision-record library table of rwb_access, or give it its dictionary name. |
| CDC-09075 | RWB-P4-E2036-APP | DOR-RWB-P4-E2036-APP-7 | 11 | Confirm DF-REF-039 (role entra_group) as a field ID of LDM v9, or assign the field its LDM ID. |
| CDC-09110 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-7 | 11 | Confirm the field ID for role.entra_group; DF-REF-039 is cited in section 11 but is not in LDM v9. |
| CDC-09145 | RWB-P4-E8006-APP | DOR-RWB-P4-E8006-APP-7 | 11 | Carry DF-REF-039 for role.entra_group, the last field of the DF-REF-034 to DF-REF-039 range in section 11, or confirm the ID is withdrawn. |
| CDC-09167 | RWB-P4-E8007-APP | DOR-RWB-P4-E8007-APP-11 | 8, 11 | Remove the personal-data class from each field the P2 check names, or name the field that carries personal data, so it agrees with BR12 (no personal field carried) |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08948 | RWB-P4-E2027-APP | CG-ALL-5334 | 16 | Add rows TC-E2-027-12 and TC-E2-027-13 to Story test cases, with Given, When and Then copied from AC3 and AC7 of RWB-P4-E2027-APP section 7. |
| CDC-09036 | RWB-P4-E2034-APP | CG-ALL-5367 | 16 | Rows 03 to 10 cover cells restored to the section 7 criterion mapping |
| CDC-09046 | RWB-P4-E2035-APP | CG-ALL-5383 | 16 | Add rows for TC-E2-035-14 in the next version, with Given, When and Then copied from AC2 (BR1). |
| CDC-09144 | RWB-P4-E8006-APP | CG-ALL-5429 | 16 | Add rows TC-E8-006-01 to TC-E8-006-06, and TC-E8-006-07 to TC-E8-006-12 added in section 16, with Given, When and Then copied from the criteria they cover. |
| CDC-09156 | RWB-P4-E8006-CON | CG-ALL-5441 | 16 | Story §16 lists all ten test cases; the rows are missing from Test Cases v8. |
| CDC-09166 | RWB-P4-E8007-APP | CG-ALL-5450 | 16 | Add rows TC-E8-007-01 to TC-E8-007-06 with Given, When and Then copied from the criteria they cover. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08961 | RWB-P4-E2027-APP | GAP-0260 | none in chunk | Add a row for payment_match_rule: 13 field rows kept and marked retired as a table; Owner P3 rwb-case (retired table); PAYMENT_MATCH rule package owned by P7 rwb-decision. |
| CDC-08968 | RWB-P4-E2027-APP | GAP-1628 |  | Hold tolerance, window days, grace days, partial floor and priority as versioned parameter rows read through the rwb-case contract; PAYMENT_MATCH logic comes from rwb-decision. Values: Not specified in the source documents (GAP-1628). |
| CDC-09077 | RWB-P4-E2036-APP | GAP-0670 | 13 | Keep POST /api/recovery/case/v1/queues/{queueId}/placements with rwb-case. rwb-integration serves the caller-facing admission on its own base and forwards to it. |
| CDC-09093 | RWB-P4-E2041-APP | GAP-0718 |  | Publish GET /api/recovery/case/v1/admin/rule-change-audit with the section 11 entry fields and Rules and parameters R; add the ownership map row to rwb-case before the wave 2 contract baseline. |
| CDC-09099 | RWB-P4-E2041-APP | GAP-0203 | none | Add row payment_match_rule with owning service P7 and target schema rwb_decision, keep all 13 fields, and record that the table is retired by D-RCV-36 T10 and the rule lives in the PAYMENT_MATCH rule package. |
| CDC-09135 | RWB-P4-E2042-APP | GAP-1994 | find it | Remove payment_match_rule as a NEW table; build the match rules as the PAYMENT_MATCH package in rwb-decision; keep the proceeds rows in rwb-payment. |

### RWB-P4-E1037-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09005 | RWB-P4-E2033-APP | DOR-RWB-P4-E2033-APP-22 | 1 | Publish the contract fake library and record its version; the story row carries a placeholder until then. |
| CDC-09021 | RWB-P4-E2034-APP | DOR-RWB-P4-E2034-APP-22 | Metadata | Publish the contract fake library version and record it in RWB-P4-E2034-APP. |
| CDC-09071 | RWB-P4-E2036-APP | DOR-RWB-P4-E2036-APP-22 | n/a | Publish the fake library and record the version this story builds against. |
| CDC-09079 | RWB-P4-E2036-APP | GAP-0957 | find it | Carry the request and answer element names of the POST /authorise admission as the realignment baseline and reconfirm them with the RWB-P2-E2036-CON owner at contract review. |
| CDC-09082 | RWB-P4-E2036-APP | GAP-0958 | find it | Fix the five reason codes with one status each: RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL as 403 with MSG-P4-002; the remaining two keep MSG-GEN-001, MSG-GEN-002 and MSG-P7-003 at 422 and 503. |
| CDC-09112 | RWB-P4-E2042-APP | GAP-0966 | 1, 4, 11 | Add the rule-package action set, request and answer fields and a change decision code to the authorise contract; agree AC-CHG with the access-log owner; stub both in the contract fake. |

### RWB-P8-E2027-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08965 | RWB-P4-E2027-APP | GAP-1359 | 12 | Publish result as packageCode, versionInForce, ruleId, rowOrder, outputs; mark the two unnamed operations as placeholders; rwb-decision confirms in RWB-P7-E1073-CON. |
| CDC-08966 | RWB-P4-E2027-APP | GAP-1360 | 12 | Publish the three event payload field lists in the AsyncAPI fragment as a marked working read, identifiers and facts only; confirm with the catalogue consumers. |
| CDC-08969 | RWB-P4-E2027-APP | GAP-1880 | 12 | Take the matching read operation and payload from RWB-P8-E2027-CON; use the standard state column with outcome BROKEN and outcome_at; keep the plan check as one durable timer with the 30-day cure period. |
| CDC-08970 | RWB-P4-E2027-APP | GAP-2507 | 12 | Publish evaluation result with NoPackageInForce outcome, placeholder names for the two unnamed operations, three payload field lists, and DecisionRecorded as read only on the shared topic. |
| CDC-08972 | RWB-P4-E2027-APP | GAP-2705 | none | Publish one read by case, plan and business date returning payment code, due date, match type, rule ID, package code and version, shortfall; carry plan states on the treatment state column; name payload members at major version 1. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09020 | RWB-P4-E2034-APP | DOR-RWB-P4-E2034-APP-14 | Metadata | Record the signed epic design sign-off for RWB-P4-E2034-APP. |
| CDC-09039 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-14 | header (metadata) | Record the signed epic design sign-off for RWB-SVC-P4 / EP02 so the story can cite it. |
| CDC-09070 | RWB-P4-E2036-APP | DOR-RWB-P4-E2036-APP-14 | n/a | Record the signed sign-off of the epic design for this story's epic. |
| CDC-09103 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-14 | find it | Record the signed epic design sign-off for EP02 in the epic design record, then cite it in the story. |
| CDC-09162 | RWB-P4-E8007-APP | DOR-RWB-P4-E8007-APP-14 |  | Record the signed epic design sign-off in the epic design record. |

### RWB-P2-E2035-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09040 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-21 | header (metadata) | Confirm RWB-P2-E2035-CON is published, as this APP story only consumes it; no RWB-P4-E2035-CON is needed. |
| CDC-09041 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-22 | 13 | Record the published fake library version of RWB-P2-E2035-CON; the version is not in the source set and was not invented. |
| CDC-09052 | RWB-P4-E2035-APP | GAP-0668 | 12 | Baseline operation names, consumed shapes, Schedule values and error mapping; record the read path ruling in the Ownership Map |
| CDC-09055 | RWB-P4-E2035-APP | GAP-2405 | 3 | Specify the rule-catalog answer (packageCode, packageVersion, versionState, inForce, ruleId, ruleVersion, actionText, ownerRole, timerSpec, toState, droolsRuleName, outputs) and the latest-state-change answer (entryId, ruleId, ruleVersion, decidedAt, missing); add 404 and 422 for MSG-P3-027 and MSG-GEN-001. |
| CDC-09063 | RWB-P4-E2035-APP | GAP-2409 |  | Mark packageVersion as required on GET /api/recovery/decision/v1/rule-catalog/{ruleId} and keep the MSG-GEN-001 refusal for an absent value. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08953 | RWB-P4-E2027-APP | GAP-1626 | none in chunk | Restate slide 17 P8 pair as GET /proceeds and POST /proceeds/{proceedsId}/match per API Specification v4 and Ownership Map. |
| CDC-09123 | RWB-P4-E2042-APP | GAP-2396 | 1 | Correct the P6 Comms to P7 Decision cell to an event for rwb.decision.events.v1 RulePackageInForce, or confirm the matrix; keep consumption in RWB-P6-E1073-APP. |
| CDC-09136 | RWB-P4-E2042-APP | GAP-2026 | find it | State that S2 rwb-treatment owns and evaluates PAYMENT_MATCH, and that matchPayments in rwb-payment asks S2 through its contract. Record as an assumption until the package is authored. |

### RWB-P10-E2031-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08986 | RWB-P4-E2031-APP | DOR-RWB-P4-E2031-APP-21 | Header | Publish the contract this story depends on and record it as published; RWB-P4-E2031-CON is not in the source documents. |
| CDC-08987 | RWB-P4-E2031-APP | DOR-RWB-P4-E2031-APP-22 | 12.8 | Publish the rwb-case contract fake and record the contract fake library version; the rwb-agent fake is now attributed in 12.8. |
| CDC-08996 | RWB-P4-E2031-APP | GAP-0630 | find it | Fix the seven added member names and four-decimal rule under major version 1; keep paging and RWB-P10-E1063-CON held-date status; name drift inputs after watch_measures; additive rwb-decision change; register route under RWB-PLT-N001-CON. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08988 | RWB-P4-E2031-APP | DOR-RWB-P4-E2031-APP-5 | 9 | Confirm the BKK value in the closed lists LOV-CAPABILITY and LOV-PRODUCT, which the detcheck says the story adds. Section 9 already states no transition. |
| CDC-09042 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-5 | 9 | Remove CUSTOMER_PARTY from the closed lists LOV-CAPABILITY and LOV-SCOPE; keep it as a data value of LOV-ROLE-CLASS only. |
| CDC-09065 | RWB-P4-E2035-APP | GAP-2407 |  | Publish LOV-DECISION in the reference-data load with state-change codes marked; the filter reads the mark. Until then, take the newest entry carrying a rule ID and rule version. |

### RWB-P2-E2034-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09032 | RWB-P4-E2034-APP | GAP-0664 | 12 | Approve the five assumptions at the contract review before the app story starts: login, append and fact element names, admin bodies, mapping, retry intervals and ledger ownership reading. |
| CDC-09033 | RWB-P4-E2034-APP | GAP-0665 | 12 | Approve wire shapes of append, two P1 reads, five fact answers and two admin operations; dedupe key, state moves, append-before-inbox order and repeated-key success. |
| CDC-09035 | RWB-P4-E2034-APP | GAP-3149 |  | Publish the EV-20 and EV-21 payload element names, the seam with RWB-P2-E2034-CON, the list members, the retry bound and the holder-reference form, and the rwb-partner ledger estate. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09044 | RWB-P4-E2035-APP | CG-ALL-5380 | 12.3 | Add the payload of rwb.access.AccessPolicyChanged.v1 as RWB-P4-E2035-APP section 12.3 gives it: policy kind, version label, valid-from date and change reference. Catalog payload is Not specified in the source documents (CG-ALL-5380) |
| CDC-09107 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-8 | find it | Add rwb-access as a consumer of rwb.access.AccessPolicyChanged.v1 with its ACL (CG-ALL-5417); the event type P1 is fixed in the story by CG-ALL-5416. |
| CDC-09108 | RWB-P4-E2042-APP | CG-ALL-5417 | 12.4 | Add rwb-access as a consumer of rwb.access.AccessPolicyChanged.v1 in the Events row and in its ACL, for the cache refresh. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09102 | RWB-P4-E2042-APP | CG-ALL-5415 | 13 | Create story RWB-P7-E1073-CON for the rule-package contract, or name an existing story key that covers it, then update the DP-04 dependency in section 13. |
| CDC-09104 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-17 | find it | Create story RWB-P7-E1073-CON or name an existing story key for the rule-package dependency (same as CG-ALL-5415). |
| CDC-09105 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-21 | find it | Create contract story RWB-P4-E2042-CON, or name the existing contract dependency RWB-P3-E2042-CON as a CON dependency in the story metadata. |

### RWB-P6-E1073-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08951 | RWB-P4-E2027-APP | GAP-2395 | none | Name the rule package and version labels of rwb-comms through the contract; prove AC1 and AC5 on the three Epic 2 fixture codes; no fourth code invented. |
| CDC-09114 | RWB-P4-E2042-APP | GAP-2395 |  | Settle the rwb-comms package assignment with the rule registry owner before the integration stage; invent no fourth package code. |

### OTHER:FSD P8 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08952 | RWB-P4-E2027-APP | GAP-1625 | none in chunk | Write testable main-flow criteria for A2.3.4.1 to A2.11.4.1 from the feature statement, rules and fields, marked new; FSD owner confirms before wave 3 SIT. |
| CDC-08954 | RWB-P4-E2027-APP | GAP-1631 | none in chunk | Replace ALS, GL, ATS, AMIS and LED interface points with rwb-source-data reads and rwb-integration ledger deliveries; treat auto-debit and LED routes as outside the 19 services. |

### RWB-P7-E2027-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08958 | RWB-P4-E2027-APP | GAP-3180 |  | Record the match priority order EXACT, then PARTIAL, then WINDOW in the PAYMENT_MATCH scenario set and drop the other order from the legacy build notes. |
| CDC-09117 | RWB-P4-E2042-APP | GAP-1292 |  | Reconcile PM-2026.12 from 2026-12-01 with PMT-2026.12 from 2026-12-15 into one label and one valid-from date before PAYMENT_MATCH is promoted in SIT. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08962 | RWB-P4-E2027-APP | GAP-1290 | 12 | Carry load and version-list shapes from legacy section 12; add approve, rollback and dry-run bodies and the governance decision code before wave 2 freeze. |
| CDC-08963 | RWB-P4-E2027-APP | GAP-1293 | 12 | Use P7 rwb-decision with /admin/rule-packages and /admin/rule-package-versions on /api/recovery/decision/v1; keep /admin/rule-versions as legacy with no target story; correct legacy P4 attribution and monolith base. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08975 | RWB-P4-E2027-APP | GAP-1291 | none | Record the DP-added H and C contracts (DP-03, 04, 06, 07, 10, 14, 15, 19) as non-blocking platform and published contracts built against fakes; keep the metadata rows as given. |
| CDC-08997 | RWB-P4-E2031-APP | GAP-2317 | find it | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON to the dependency map; keep this Work Package metadata unchanged. |

### RWB-P10-E2031-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08999 | RWB-P4-E2031-APP | GAP-2198 | find it | Accept the proposed defaults: agentDrift in baseline Schedule, segment from run row, decision-log read, rwb-comms notice, approved policy rows, index-only migration, additive v1 element change, policy-mode screen states, configured range limits and windows. |
| CDC-09000 | RWB-P4-E2031-APP | GAP-2200 | find it | Accept the proposed defaults: route path fixed with edge story; login via secret reference; topology and budget in values files; notice via contract; idempotent Schedule; single model gateway private endpoint. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09003 | RWB-P4-E2031-APP | GAP-0631 | 12 | Register the gateway-bff route for the v2 read and override panel, path set by the edge story. Login via secret reference (rwb-agent login, DP-02); thresholds and topology as named chart values; Schedule updated in place. |
| CDC-09058 | RWB-P4-E2035-APP | GAP-0418 | 3 | Agree with QA at the wave 2 entry check: composite route path, merge order, call list, slow-source answer, harness repository, SIT environment, seeded data, evidence format and retention, and pass/fail gate. |

### RWB-P2-E2035-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09053 | RWB-P4-E2035-APP | GAP-0669 | 13 | Fix the identity and secret reference; create the next-action-check job row with its run book path; record ownership |
| CDC-09121 | RWB-P4-E2042-APP | GAP-0669 | 13 | Fix the rwb-integration login, secret reference and probe checks; add the next-action-check job row with its run book path; record the read path ruling in the Ownership Map and review the three runbook entries. |

### RWB-P7-E2042-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09054 | RWB-P4-E2035-APP | GAP-2406 | 3, 16 | Set the valid-from of RES-2026.12 to one date reconciled with RWB-E2-035 (2026-12-01 or 11 December 2026) before the wave-2 fixture freeze. |
| CDC-09122 | RWB-P4-E2042-APP | GAP-2406 | 3 | Reconcile one valid-from date for RES-2026.12: move the registry to 2026-12-01 or re-date the legacy criteria; keep the legacy reading in fixtures until decided. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09064 | RWB-P4-E2035-APP | GAP-2325 |  | Version role rows by the matrix version they are loaded with, or add a role_version label; add the cache lifetime as a DP-06 parameter agreed at the wave 2 design review; test the version-keyed drop. |
| CDC-09155 | RWB-P4-E8006-CON | GAP-0867 | 7, 11 | Story side fixed in AC1, AC8 and §11 for endpoint path and answer fields; cache parameter name marked Not specified (GAP-0867) |

### OTHER:TSD P4 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09092 | RWB-P4-E2041-APP | GAP-1565 |  | Re-issue without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 with its ACs to rwb-decision documents; keep RULES_AND_PARAMETERS rule-evaluation rights; set x-module of the six paths to P7 in API Specification v4. |
| CDC-09133 | RWB-P4-E2042-APP | GAP-0968 | find it | Correct T3.1 and T6.1 in the next version so the four rule tables and registry operations belong to P7; keep P4 rows for rights and access log only. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09095 | RWB-P4-E2041-APP | GAP-0964 |  | Add GET /api/recovery/access/v1/rule-authority and POST /api/recovery/access/v1/rule-report-exports as P4 operations with their query, body and answer fields; freeze action set and refusal reasons at RWB-P3-E2041-CON review. |
| CDC-09168 | RWB-P4-E8007-APP | GAP-1565 | 11 | Re-issue TSD P4 without the four rule tables, RulePackageStore and the six rule-package operations; move FEAT-ADM-02 to rwb-decision; set x-module of the six paths to P7 |

### RWB-P3-E2042-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09106 | RWB-P4-E2042-APP | DOR-RWB-P4-E2042-APP-22 | find it | Publish the rwb-decision and rwb-access fake library version of RWB-P3-E2042-CON and record its version as published. |
| CDC-09125 | RWB-P4-E2042-APP | GAP-0722 | 1 | Publish GET /rule-models/{packageCode}/{version} and GET /rule-catalog/{ruleId} with the listed elements: packageCode, versionLabel, checksum, model content, compiler version, valid-from, and the catalog fields. |

### RWB-P2-E2035-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09119 | RWB-P4-E2042-APP | GAP-0667 | 4, 7, 12 | Serve GET /cases/{caseId}/next-action from the integration base under DP-13; fix consumed field names, operation names, Schedule values and message texts; correct the Ownership Map row. |
| CDC-09120 | RWB-P4-E2042-APP | GAP-0668 | 12 | Baseline the next-action contract with three operation names, nine consumed shapes, Schedule values, timer vocabulary and error mapping; confirm the five message texts. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20777 | RWB-P4-E2031-APP | R-16860 |  | The standard meaning of MSG-P4-003 is not in the sources, so it cannot be confirmed here. MSG-P4-004 is already the break-glass message. |
| CDC-20778 | RWB-P4-E2035-APP | R-16880 |  | MSG-P4-006 meaning and any new role-conflict ID belong to the P4 message catalogue. The story keeps its own use. |

### RWB-P4-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08949 | RWB-P4-E2027-APP | DOR-RWB-P4-E2027-APP-10 | none | Add empty, loading, error and no-access states for SCR-28, SCR-43 and SCR-44 in the screen specification. |

### OTHER:Rule registry (PAYMENT_MATCH package version row) and RWB-E2-027 / RWB-E2-042 stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08955 | RWB-P4-E2027-APP | GAP-1292 | none in chunk | Hold one label and one valid-from date for PAYMENT_MATCH before SIT; keep PM-2026.12 from 2026-12-01 as the record in force under R7.3 and reconcile PMT-2026.12 from 2026-12-15 into it. |

### OTHER:Recovery Workbench story RWB-E2-042 (section 3 version labels) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08956 | RWB-P4-E2027-APP | GAP-1297 | 3 | Reconcile PMT-2026.12 (valid from 2026-12-15) to one PAYMENT_MATCH version row with PM-2026.12 (valid from 2026-12-01) before SIT; owner: Business analyst of RWB-E2-027. |

### OTHER:RWB-E2-027 build notes (step 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08957 | RWB-P4-E2027-APP | GAP-3179 | none in chunk | Remove payment_match_rule table load and reads; keep PAYMENT_MATCH package as sole home of rows, loaded through rule package endpoints; drop the table from every service schema. |

### OTHER:Work Package B2-P8-002 story (rwb-payment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08959 | RWB-P4-E2027-APP | GAP-2506 | 13, 12.3 | Add C RWB-P7-E1073-CON to the metadata C row; name the ordering column row order with priority as its legacy and TSD name; read PM-2026.12 as the single version; declare DecisionRecorded read only with no second writer. |

### OTHER:TSD P4 T-A.1 (rule-package and rule-version endpoints) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08960 | RWB-P4-E2027-APP | GAP-2313 | 10, 12.1 | Move the six rule-package and rule-version endpoints to P7 rwb-decision; P4 keeps the loader and approver rights and the refusals; correct at the next version. |

### OTHER:Consumer contract index D1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08964 | RWB-P4-E2027-APP | GAP-1355 | 7 | Add C RWB-P7-E1073-CON to the C row of RWB-P8-E2027-CON; read AC6 through the rwb-decision contract mock with legacy steps kept verbatim. |

### OTHER:Service values files (three) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08967 | RWB-P4-E2027-APP | GAP-1361 |  | Expose every operations value as a chart value with a placeholder in the three values files; close with DL11 decisions before UAT. |

### OTHER:platform secret-store catalogue and the three values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08971 | RWB-P4-E2027-APP | GAP-2508 | none | Chart every numeric operations value in the three values files; close DL11 before UAT; record secret and workload identity names in the platform secret-store catalogue. |

### OTHER:parameters contract of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08973 | RWB-P4-E2027-APP | GAP-2706 | none | Evaluate the RES rule set in rwb-treatment with the package from rwb-decision; read CURE_PERIOD_DAYS and restructure.max_breaks from the parameters contract; open package code and keys at contract freeze. |

### OTHER:Not specified in the source documents (GAP-1881) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08974 | RWB-P4-E2027-APP | GAP-1881 | none | Keep the PAYMENT_MATCH package and version with rwb-decision and the match rows with rwb-payment; rwb-treatment evaluates the version for the plan breach and publishes TreatmentClosed.v1 once. |

### OTHER:FSD P8 v3 and TSD P8 v2 (Requirements served and T8 traceability tables) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08977 | RWB-P4-E2027-APP | GAP-1624 |  | Fill the REQ ID rows of both tables, or state that P8 has no requirement ID; the story then traces to FEAT-PAY-01 to FEAT-PAY-11 and the AC IDs. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08978 | RWB-P4-E2027-APP | GAP-1639 |  | Name the event-started workflows after matchPayments and confirmBookings on task queue rwb-payment, and add them to the workflows sheet. |

### RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08979 | RWB-P4-E2027-APP | GAP-1357 |  | Change the precondition label PAYMENT_MATCH PMT-2026.12 to PM-2026.12 so one version row in rwb-decision is in force. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08980 | RWB-P4-E2027-APP | GAP-0218 |  | Record rwb-decision as holder of LOV-MATCH-TYPE and rwb-payment as reader, with the codes as the match type column of package PAYMENT_MATCH; copy the Values sheet rows unchanged. |

### OTHER:rwb-decision rule_row catalogue and evaluation result (TSD P8 T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08981 | RWB-P4-E2027-APP | GAP-1356 |  | Publish the column name row order in the rule_row catalogue and evaluation result, with priority recorded as its legacy and TSD name. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08982 | RWB-P4-E2027-APP | GAP-1358 |  | Confirm the consumer list for DecisionRecorded with the event catalogue owner and declare rwb-payment read-only for the ledger acknowledgement. |

### OTHER:Platform secret-store catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08983 | RWB-P4-E2027-APP | GAP-1362 |  | Record the rwb-payment login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity; keep the phrase the rwb-payment login (DP-02). |

### RWB-P4-E2031-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08984 | RWB-P4-E2031-APP | DOR-RWB-P4-E2031-APP-14 | Header | Record the signed epic design sign-off; no signed epic design is in the story or source documents. |

### OTHER:Squad sizing at refinement (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08985 | RWB-P4-E2031-APP | Definition of Ready item 16 Size: Fail | Header | Size row kept as a Not specified placeholder |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08990 | RWB-P4-E2031-APP | DOR-RWB-P4-E2031-APP-12 | 16 | Align the §18 test lists with RTM v7; drop the drift criteria of RWB-P10-E2031-APP from the Covers of TC-E2-031-02, TC-E2-031-06 and TC-E2-031-07. |

### OTHER:Recovery Workbench FSD P4 message set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08991 | RWB-P4-E2031-APP | DOR-RWB-P4-E2031-APP-9 | 14 | Confirm the meaning of MSG-P4-003 against the standard; the story uses it for a drill-down that names an agent the metric answer does not hold. |

### RWB-PLT-N001-CON; RWB-P10-E2031-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08992 | RWB-P4-E2031-APP | GAP-0629 | find it | Register the SCR-46 screen route under RWB-PLT-N001-CON; the drift step, segment, policy values, migration and range limits stay with RWB-P10-E2031-APP; take the right of API-P10-009 as the decision. |

### RWB-P4-E1039-CON; 06 Data/Recovery Workbench Physical Schema v7; OTHER:the service's Flyway sequence (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08993 | RWB-P4-E2031-APP | GAP-2316 | 12.7 | Add the agent-monitor object-type value, the access-entry field list and the log page bounds to the next version of RWB-P4-E1039-CON; take the record code from the DP-03 library at build time; name the read index in the physical schema of rwb_access; record the Flyway step in the service's own sequence. |

### RWB-ITG-E2031-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08994 | RWB-P4-E2031-APP | GAP-0413 | find it | Agree the SIT harness profile, seed pack, fixed clock at 2026-12-14, evidence format and gate with the QA lead; confirm the drift Schedule runs in rwb-agent at the wave 2 entry check. |

### OTHER:Legacy RWB-E2-031 story and rwb-agent contract (right names) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08995 | RWB-P4-E2031-APP | GAP-2318 | 7 | Second read right marked Not specified in the source documents (GAP-2318) in the AC1 scenario; both gates recorded for the wave 2 access review. |

### OTHER:Work Package plan generator (B-P10-02 fanout) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09001 | RWB-P4-E2031-APP | GAP-2201 | find it | Remove RWB-E2-031 from B-P10-02 or retire it; number defaults once as ASM-B2-P10-005-1 to -24 and supersede the duplicate part rows; add duplicate-output and ASM-resolution checks. |

### RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09002 | RWB-P4-E2031-APP | GAP-2199 | 12 | Add the agent-version query filter and the override-reason element as additive fields to GET /decision-log and GET /decision-log/{entryId}; AC3 query unchanged. Other defaults stay with their owners. |

### RWB-P3-E2033-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09008 | RWB-P4-E2033-APP | DOR-RWB-P4-E2033-APP-10 | none | Add empty, loading, error and no-access states for SCR-02 to the P3 story. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; RWB-P3-E2033-APP; RWB-P2-E2033-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09009 | RWB-P4-E2033-APP | DOR-RWB-P4-E2033-APP-9 | 14 | Align the P3 MSG-GEN-007 text and the P2 MSG-GEN-006 use with Error and Message Standard v4. |

### RWB-P2-E2033-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09010 | RWB-P4-E2033-APP | GAP-0661 | none | Baseline GET /api/recovery/integration/v1 read-only operations with twelve columns, filter set, breach filter, order, paging envelope and problem body; declare eight consumed operations, no table, event, workflow or Schedule. |

### RWB-P3-E2033-APP; RWB-P4-E2033-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09011 | RWB-P4-E2033-APP | GAP-0660 | none | Keep GET /cases and GET /cases/export with rwb-case; add composed read and export on the integration base as additional, read-only; fix ageing, reference-data and access-log operations. |

### RWB-P2-E2033-CON; RWB-P3-E2011-APP; OTHER:rwb-case baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09012 | RWB-P4-E2033-APP | GAP-2224 | none | Fix row and envelope names in v1, confirm page bounds and export limit as parameter rows, keep ageDays with ageInStateDays added, drop duplicate timer index, name login and flag owner. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P2-E2033-CON; OTHER:rwb-case baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09013 | RWB-P4-E2033-APP | GAP-3101 | none | Declare a batched read GET /api/recovery/deviation/v1/deviation-flags with one hop and a page-bound parameter row; add it to the RWB-P2-E2033-CON consumed set. |

### RWB-P2-E2033-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09014 | RWB-P4-E2033-APP | GAP-2320 | Metadata | Fix the session element list, authorise branch and batch bound, and extract record fields in baseline review with the rwb-access contract owner. Story now records the P2 build-against attribution. |

### OTHER:Wave 2 release record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09015 | RWB-P4-E2033-APP | GAP-0415 | Not applicable | Ratify as one appendix the harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence and gate format before RWB-ITG-E2033-ITG claims Done. |

### OTHER:Recovery Workbench plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09017 | RWB-P4-E2033-APP | GAP-3187 | Metadata | Keep rwb-integration as primary for RWB-E2-033 to RWB-E2-036 in this version and record the P3 code-location tension for the assembly step. |

### OTHER:Recovery Workbench FSD P7 (wave 1 contract review with rwb-source-data and rwb-case owners) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09026 | RWB-P4-E2034-APP | GAP-1612 | header | Integration dependencies row lists the ledger on rwb-source-data with its IDs Not specified. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09027 | RWB-P4-E2034-APP | GAP-3175 |  | List AceDataReady (EV-26) as the target event on rwb.source-data.events.v1 and LoadCompleted as its legacy alias. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09028 | RWB-P4-E2034-APP | GAP-3176 |  | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### RWB-P2-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09029 | RWB-P4-E2034-APP | GAP-0590 | 12 | Fix the key format EFS:<efs_record_key>; count view rows folded per entry; report the ledger writer hit count and the run summary count as the run's key set. |

### RWB-P1-E2001-APP; RWB-P2-E2034-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09030 | RWB-P4-E2034-APP | GAP-2186 | 12 | Publish the contact-fact read on the P1 base with path, contact-key parameter and masked members; confirm GET /efs-history answers the outcome list; realign the two consumed rows. |

### OTHER:Ledger harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09031 | RWB-P4-E2034-APP | GAP-0416 | 16 | Agree composite route path and merge order, SIT environment, seeding, evidence format, retention and pass/fail gate with QA at the wave 2 entry check; hold as data. |

### RWB-P2-E2034-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09034 | RWB-P4-E2034-APP | GAP-0666 | none | Carry the nine deployment values (consumer groups and offset policy, scan and retry intervals, lag and alert thresholds, build ID format, fixture owner) as environment values, approved at release readiness review |

### RWB-P1-E1066-CON; RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09038 | RWB-P4-E2034-APP | GAP-2185 | 12.1 | Settle one ledger path family on POST and GET /cases/{caseId}/interactions and realign the append row POST /interactions in RWB-P1-E1066-APP section 12.1 to it. |

### OTHER:Message catalogue of P4 (standard entry MSG-P4-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09048 | RWB-P4-E2035-APP | DOR-RWB-P4-E2035-APP-9 | 14 | Settle the meaning of MSG-P4-006 or assign a new ID for the role-conflict message used in section 14 |

### OTHER:Legacy RWB-E2-042 and FSD P6 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09049 | RWB-P4-E2035-APP | GAP-2395 | none | Name the rule package codes and the rwb-comms package assignment as the proposed fix sets out |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09050 | RWB-P4-E2035-APP | GAP-3177 | 13 | Register the five-minute next-action Schedule in rwb-case; delete EV-18 from the Epic 2 contract tables |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P2-E2035-CON; OTHER:rwb-case, rwb-access and rwb-decision contract baselines (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09051 | RWB-P4-E2035-APP | GAP-0667 | 4, 7, 12 | Correct the next-action row to P2 read and P3 write; fix login, field names, operation names, Schedule values and message texts |

### OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09056 | RWB-P4-E2035-APP | GAP-2324 | 3 | Add a Case record column for every role, publish the 14-area matrix as data through RWB-P4-AD002-APP, and fix the default scope of the specialist roles with the security administrator before PM-2026.12 is in force. |

### OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09057 | RWB-P4-E2035-APP | GAP-2322 | 3 | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema, publish it with RWB-P4-E1037-CON and stub it in the contract fake; fix the authorise request and answer; fix the rwb-access login in the platform DB story; add the unknown or inactive role code message. |

### OTHER:TSD P4 T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09059 | RWB-P4-E2035-APP | GAP-2323 | 3 | Add CUSTOMER_PARTY to LOV-ROLE-CLASS in the same load that carries the roles, let customer-party roles carry it, and confirm the value with the role catalogue owner before the wave-2 policy pack goes in force. |

### OTHER:Delivery plan (rwb-integration primary for RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09061 | RWB-P4-E2035-APP | GAP-3187 |  | Keep the four keys primary in rwb-integration as the directive records; record the tension for the assembly step. No change in this story. |

### OTHER:RWB-P6 rwb-comms story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09062 | RWB-P4-E2035-APP | GAP-2400 |  | Read the three route-set fields in rwb-comms only where a notice is decided by a route-set rule; test the copy with legacy R-RES-04 values; keep the case next action with RWB-E2-035 in rwb-case. |

### OTHER:rwb-case reference data (timer spec list of values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09066 | RWB-P4-E2035-APP | GAP-2408 |  | Publish the timer spec shapes as a list of values with their parsing rule, extended with the two legacy values 'payment due 30 days' and 'deadline driven'. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09067 | RWB-P4-E2035-APP | GAP-2411 |  | Fix the rwb-decision per-service database login name in RWB-PLT-DB and the secret store, with migration and application roles kept apart; reference it from every P7 story. |

### RWB-P2-E2036-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09078 | RWB-P4-E2036-APP | GAP-0671 | 12 | Declare the integration-base placement as the provided operation (four body fields, required Idempotency-Key, 201 shape) and the case-base placement as consumed and owned by P3; carry consumed element names as placeholders. |

### RWB-ITG-E2036-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09080 | RWB-P4-E2036-APP | GAP-0419 | find it | Hold the composite route path and merge order, harness repository, SIT environment, seeded data, evidence format, retention and pass/fail gate as data in the harness pack, agreed at wave 2 entry. |

### parameter-catalog.csv; RWB-P2-E2036-CON; RWB-ITG-E2036-ITG; OTHER:platform DB story (login name); OTHER:RW-SECADM matrix version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09081 | RWB-P4-E2036-APP | GAP-0735 | find it | Hold the six values in their named owners: callers list as a parameter, matrix version by RW-SECADM, overflow shape and caller mapping in the contract, login name in the platform DB story, legacy criteria in the ITG story. |

### OTHER:rwb.deviation.events.v1 (S8 service contract); OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09083 | RWB-P4-E2036-APP | GAP-3102 | find it | Publish the hold element on DeviationRaised and DeviationCleared additively in rwb.deviation.events.v1, and have the rwb-case owner declare the event-driven set and clear of recovery_case.deviation_open. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; RWB-P4-E1037-CON; RWB-P3-E1019-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09084 | RWB-P4-E2036-APP | GAP-2412 | find it | Publish the placement fact element names, the P3 case-read and P4 authorise shapes, the reference-data operation, the MSG-P7-009 text, and the platform DB login name and secret entry. |

### OTHER:Plan (assembly step) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09086 | RWB-P4-E2036-APP | GAP-3187 | find it | Keep rwb-integration as primary for RWB-E2-033 to RWB-E2-036 and record the P2/P3 tension for the assembly step |

### OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09088 | RWB-P4-E2041-APP | DOR-RWB-P4-E2041-APP-8 | header | Publish POST /api/recovery/access/v1/authorise in the rwb-access API yaml or confirm it under RWB-P4-E1037-CON; reconcile the decision-record event type name to Catalog v1 |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09089 | RWB-P4-E2041-APP | DOR-RWB-P4-E2041-APP-12 | 12.7, 16, 18 | Story side done: boundary row TC-12 added and rows 13 to 17 added in section 16. Section 18 is unchanged here (see CG-ALL-5411). |

### OTHER:TSD P7; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09090 | RWB-P4-E2041-APP | GAP-1615 | 1 | Re-issue TSD P7 with T3.1 entries for the four rule tables and T-A rule operations; remove them from TSD P3 and TSD P4; set x-module P7 on the nine rule paths |

### OTHER:TSD P3 v3; OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09091 | RWB-P4-E2041-APP | GAP-1993 | 1 | Remove rule_package, rule_package_version, rule_row and rule_test_case ownership; read the package through the P7 contract (DP-04) |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09094 | RWB-P4-E2041-APP | GAP-0962 | 16 | Publish one RULES_AND_PARAMETERS row set giving the letter of every role a rule change touches; restate that RW-REFADM prepares the checklist and load file with no C letter, no upload, approval or rollback. |

### OTHER:TSD P4 v3 T6.1 permission data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09096 | RWB-P4-E2041-APP | GAP-0965 |  | Add rwb-decision service identity and the gateway-bff route with R in RULES_AND_PARAMETERS only; confirm with security administrator before the authorise contract is frozen. |

### RWB-P3-E2041-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09097 | RWB-P4-E2041-APP | GAP-2413 |  | Agree at wave 2 contract review the ChangeReportPage and RulePackageChangeEntry shapes, rulesChanged element, CSV column order, decision-code and item-list LOV values, package-version count, load and approve answers, and rwb-decision login name. |

### OTHER:rwb-decision contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09100 | RWB-P4-E2041-APP | GAP-0720 | 16 | State a deprecation window for a published field; the window length is Not specified in the source documents (GAP-0720). |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09101 | RWB-P4-E2041-APP | GAP-2415 | none | Record the split: checklist, two amended operations and change report to rwb-decision; audit read and impact count to rwb-case; screens and rights to rwb-access; legacy flag rwb.p3.rule-change-report read as a rwb-decision parameter. |

### OTHER:TSD P7; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09113 | RWB-P4-E2042-APP | GAP-1615 |  | Re-issue TSD P7 with the four rule tables and rule-version and rule-package operations; remove them from TSD P3 and TSD P4; set x-module P7 on the nine rule paths. |

### RWB-P2-E2007-APP; RWB-ITG-E2007-ITG; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09116 | RWB-P4-E2042-APP | GAP-0657 |  | Keep JOB-08 with rwb-integration; record Architecture v5 slide 44 owner row as superseded; read ACE facts through rwb-source-data; fix six consumed paths in RWB-P2-E2007-CON. |

### OTHER:PAYMENT_MATCH scenario set (RWB-E2-027 and RWB-E2-042) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09118 | RWB-P4-E2042-APP | GAP-3180 |  | Confirm the order with Credit Administration and carry one order, EXACT then PARTIAL then WINDOW, in the PAYMENT_MATCH scenario set. |

### OTHER:Rule package harness pack (SIT) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09124 | RWB-P4-E2042-APP | GAP-0421 | 1 | Agree the harness repository, SIT environment, seeding set, evidence format and retention, gate and five fake response bodies at the wave 2 entry check; hold values as data in the pack. |

### OTHER:TSD P4 v3 (permission matrix; OTHER:T6.1 and T6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09126 | RWB-P4-E2042-APP | GAP-0967 | 3 | Publish service-identity rows across the fourteen capability areas; confirm one non-human actor per service; record the area each package serves as an rwb-decision package attribute. |

### OTHER:FSD P6 v3 (A2.1.4.2; OTHER:A2.1.4.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09127 | RWB-P4-E2042-APP | GAP-2399 | none | Refuse the notice request with MSG-GEN-006; create no notice row; dispatch nothing; add no hold reason of this service. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09129 | RWB-P4-E2042-APP | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime; a version names its format; conversion is a version change with its own test evidence; both formats stay in the load checks and model fetch. |

### OTHER:rwb-decision version register (PAYMENT_MATCH) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09130 | RWB-P4-E2042-APP | GAP-1357 | find it | Hold one version row for PAYMENT_MATCH: PM-2026.12 in force from 2026-12-01; reconcile the PMT-2026.12 label to that row before SIT. |

### OTHER:RWB-E2-035 rwb-case story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09131 | RWB-P4-E2042-APP | GAP-2400 | find it | Keep the route-set behaviour on the case next action; read action_text, owner_role and timer_spec in rwb-comms only where a notice is decided by a route-set rule, tested with the legacy R-RES-04 values. |

### RWB-P3-E2042-INF; RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09132 | RWB-P4-E2042-APP | GAP-0723 | find it | Set the container to write-once with no deletion and reviewed audit retention per environment; size the pod by a load test caching 20 versions; expose alert windows, replica counts and probe timings as reviewed values files, confirmed with platform and audit owners before wave 2 release. |

### OTHER:TSD P7 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09134 | RWB-P4-E2042-APP | GAP-1298 | find it | List the LOV-DECISION values used for decision_code DF-DEC-003 and confirm them with the LOV-DECISION owner before SIT. |

### OTHER:Rules Engine Design v3 (section 2) and Temporal and Drools Design Text Extract v1 (slide 13) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09137 | RWB-P4-E2042-APP | GAP-2034 | find it | State that UNIVERSAL is evaluated in every service from its own copy of the same approved version, with authoring, scenarios and approval in rwb-decision (P7). |

### OTHER:Decision record of DP-03 (DF-DEC-001 to DF-DEC-031) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09138 | RWB-P4-E2042-APP | GAP-2397 | find it | Confirm the field IDs that carry the package code and the checksum when the record is published. Add no column to notice, template or merge_field. |

### RWB-P4-E8006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09142 | RWB-P4-E8006-APP | DOR-RWB-P4-E8006-APP-21 | header | Build status to Done once the contract is published |

### OTHER:Recovery Workbench Features sheet (FEAT-AGT-12) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09146 | RWB-P4-E8006-APP | GAP-1480 |  | Change the Epic 3 dependency of FEAT-AGT-12 from FEAT-CWC-22 to the Epic 1 configuration path and the Epic 2 approvals path; the Epic 8 screen presents the same rows. |

### OTHER:TSD P4 v3 and TSD P3 (technical specifications) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09148 | RWB-P4-E8006-APP | GAP-1566 | none | Remove API-P4-021 and WorkflowAdminService from TSD P4, and remove the same smoke path from TSD P3; keep the smoke workflow once in the platform workflow story and specification. |

### OTHER:Features sheet (FEAT-AGT-12) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09154 | RWB-P4-E8006-CON | GAP-1480 | none | Change the Epic E3 dependency of FEAT-AGT-12 from FEAT-CWC-22 to the Epic 1 configuration path and the Epic 2 approvals path; the E8 screen presents the same rows. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09158 | RWB-P4-E8006-CON | CG-ALL-5443 | 15 | Add the empty, loading, error and no access states of SCR-39, SCR-42, SCR-43 and SCR-47 to Screen Specifications v1. |

### OTHER:Technical Specification P4 v3 (T-A.1; OTHER:T2) and Technical Specification P3 (API-P3-027) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09159 | RWB-P4-E8006-CON | GAP-1566 | find it | Remove API-P4-021 and WorkflowAdminService from TSD P4 and API-P3-027 from TSD P3; keep the smoke workflow once in the platform workflow story and specification. |

### OTHER:02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09160 | RWB-P4-E8006-CON | NEWAC-RWB-P4-E8006-CON-AC9 | 7, 16 | Add the refusal criterion for a status change the case model does not allow, owned by rwb-case. This contract declares no status model, so no criterion is added to RWB-P4-E8006-CON. |

### RWB-P4-E8007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09163 | RWB-P4-E8007-APP | DOR-RWB-P4-E8007-APP-21 |  | Set build status to Done once the contract is published. |

### RWB-P3-E1042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09164 | RWB-P4-E8007-APP | DOR-RWB-P4-E8007-APP-22 | 12.8 | Record the published fake library version for the rwb-case parameters fake. |

### OTHER:FSD P4 v3 and rwb-access personal-data register build (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09169 | RWB-P4-E8007-APP | GAP-2298 |  | Name the register table, operations, statutory period, states, record codes and case-hold link per GAP-2298; this story holds no PDPA register |

### 02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20614 | RWB-P4-E8006-CON | R-30992 |  | Refusal test and its event/state values are not specified in the sources (R-30992). Workbook not read; docview unavailable, so no row was appended. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20752 | RWB-P4-E2041-APP | R-22286 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20815 | RWB-P4-E2027-APP | R-28825 |  | rule_row catalogue and evaluation result belong to rwb-decision (TSD P3 T2.2). This document has no rule_row catalogue; payment_match_rule priority already present. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0203 | The entity Payment match rule has no row in the Ownership Map and no target table | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0218 | LOV-MATCH-TYPE is used by payment_match_rule, a table the target drops and the Ownership Map does not carry | Center of excellence | Resolved (directive) |
| GAP-0260 | payment_match_rule is in the inventory but not in the Ownership Map, and D-RCV-36 retires it as a table | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0409 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0413 | SIT harness environment, two-week and November seed, fixed clock, cost reconciliation fixture, evidence and gate for the agent-monitor journey | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0415 | The SIT harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence format for the case-list journey are not specified in any source read | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0416 | Ledger harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0418 | Gateway-bff composite next-action route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0419 | Wave 2 queue-placement harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0420 | Rule-change report harness environment, seeding, evidence format, retention and composite route detail are not specified | Integration lead | Resolved (directive) |
| GAP-0421 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0631 | The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified | Platform administrator | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0664 | The rwb-integration login, the entry and fact JSON field names, the admin bodies, the mapping detail, the retry intervals and the ownership split of the ledger intake are not fixed in the source documents | Solution architect | Resolved (directive) |
| GAP-0665 | The append, EFS and contact wire shapes, the admin operation bodies, the dedupe key of each type and the ordering of the append and the inbox are not stated for the intake contract | Solution architect | Resolved (directive) |
| GAP-0666 | The consumer group names, the offset policy, the retry scan interval, the lag and alert thresholds, the build ID format and the fixture owner of the intake deployment are not fixed in the source documents | DevOps lead | Resolved (directive) |
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
| GAP-0734 | The next-action slice leaves the legacy AC allocation, the daily check Schedule, the DL22 durations and the role-class field unspecified | Tech lead | Resolved (directive) |
| GAP-0735 | The placement slice leaves the legacy AC allocation, the approved callers list, the production matrix grant, the overflow shape, the caller mapping and the login name unspecified | Tech lead | Resolved (directive) |
| GAP-0867 | The administration home operation, its fields, its parameter name, its entitlement rule and its record code are not in the sources | Tech lead | Resolved (directive) |
| GAP-0868 | The rule-change request record while the registry, the load gate and the approval belong to other stories | Tech lead of rwb-access | Resolved (directive) |
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
| GAP-1290 | PAYMENT_MATCH registry governance: shapes, decision-record payload, message set and promotion and rollback semantics are not specified | Solution architect, with the P7 business analyst and the rule owner RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1293 | The rule-package operations: the legacy P4 attribution and the /admin/rule-versions paths against P7 and /admin/rule-package-versions | P7 solution architect, with the API specification owner | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1298 | The decision code of a rule-governance entry is not named in any source this key may read | Decision log owner | Resolved (directive) |
| GAP-1299 | The name of the rwb-decision database login is not specified | ACE database administrator | Resolved (directive) |
| GAP-1300 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Business analyst | Resolved (directive) |
| GAP-1301 | The four rule registry tables are declared for P4 and P3 in their TSDs and are absent from the P7 TSD | Solution architect | Resolved (directive) |
| GAP-1302 | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Business analyst | Resolved (directive) |
| GAP-1303 | The BRD section pointers copied from the legacy story no longer match BRD v2 and v4 | Business analyst | Resolved (directive) |
| GAP-1355 | The AC6 package load and the rule-evaluation contract have no C row in this key | Solution architect | Resolved (directive) |
| GAP-1356 | The ordering column is called row order in the story and priority in the TSD | Data steward | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1358 | DecisionRecorded is listed as consumed here but the catalogue names only two consumers | Integration architect | Resolved (directive) |
| GAP-1359 | The rule-evaluation result has no published schema and two of its field names are not given | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1360 | The three payment event payloads have no schema in any source | Integration architect | Resolved (directive) |
| GAP-1361 | No numeric operations value is specified for the matching service | DevOps engineer | Resolved (directive) |
| GAP-1362 | The secret names, the workload identity and the certificate of rwb-payment are not specified | Identity and access team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1480 | An Epic 3 feature depends on an Epic 8 administration feature | Solution architect | Resolved (directive) |
| GAP-1565 | The rule package registry, the rule-package operations and the change report are claimed by the P4 technical specification while the Ownership Map gives them to rwb-decision | Solution architect with the rwb-decision contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1566 | POST /admin/workflows/smoke is claimed by the P3 and P4 technical specifications while the Ownership Map and Architecture v5 give the smoke workflow to the platform | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1624 | FSD P8 issues no requirement ID, so the product requirement cannot be traced to an FSD requirement | Business analyst, P8 | Resolved (directive) |
| GAP-1625 | Eight of the eleven P8 features carry a placeholder acceptance criterion instead of a testable one | Business analyst, P8 | Resolved (directive) |
| GAP-1626 | The two operations named in Architecture v5 slide 17 are not the two operations in the API Specification and the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1628 | The matching values have no table and no owner after payment_match_rule was retired | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1880 | The treatment-side matching read, the shortfall columns, the breach decision code and the plan-check cadence are not specified | Solution architect with the rwb-treatment and rwb-payment squads | Resolved (directive) |
| GAP-1881 | PAYMENT_MATCH is the rwb-payment matching package while this slice evaluates it for the plan breach on the treatment side | Solution architect with rwb-decision, rwb-payment and rwb-treatment | Resolved (directive) |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-1994 | payment_match_rule has no owner in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-2026 | Owning service of the PAYMENT_MATCH package is not stated in one place | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2034 | The UNIVERSAL package has no single owning service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2184 | The retention class list, the added event codes, the link column types and the feature IDs of four requirements are in no source | Data architect | Resolved (directive) |
| GAP-2185 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2186 | The EFS outcome read and the contact-fact read that the channel consumer calls are named by interface only, with no path, parameter or owning story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2198 | RWB-E2-031 version 2 app slice: the drift step and its Schedule, the segment source, the decision-log read, the notice, the policy values, the migration scope, the element change, the screen states, the login, the route path, the range limits and the two windows are not named by the sources | Tech lead of rwb-agent with the solution architect | Resolved (directive) |
| GAP-2199 | RWB-E2-031 version 2 contract slice: the decision-log filter and override element, the notice operation, the name of the read right, the paging and member types, the route path, the login and the Schedule step names are not fixed by the sources | Tech lead of rwb-agent with the owners of rwb-decision, rwb-comms and rwb-access | Resolved (directive) |
| GAP-2200 | RWB-E2-031 version 2 deployment slice: the route path, the login secret, the topology and budget, the notice operation, the Schedule registration detail and the model gateway egress are not fixed by the sources | DevOps engineer with the platform administrator and the security administrator | Resolved (directive) |
| GAP-2201 | Two Work Packages write the same three story files, the same three fragments and two overlapping assumption sets for legacy RWB-E2-031 on rwb-agent | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2224 | The case list is served twice in the target, and the row names, the bounds, the login and the flag mechanism of the owner's list have no source | Solution architect | Resolved (directive) |
| GAP-2225 | Element names of the interaction item, the append command and the intake result are not in the sources | TechX and rwb-source-data contract owner | Resolved (directive) |
| GAP-2226 | Legacy occurred-time order and the case timeline page order differ | TechX | Resolved (directive) |
| GAP-2298 | The personal-data request register of rwb-access has no table, no operation set, no statutory period, no state set and no link to the case hold in the sources | Tech lead of rwb-access | Resolved (directive) |
| GAP-2311 | Values of the payment-matching access profile that the legacy story does not state | Business analyst, P4 | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2313 | The rule-package endpoints are P4 in the legacy contract and P7 in Arch v5 | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2314 | No legacy acceptance criterion of RWB-E2-027 belongs to the P4 slice | Business analyst, P4 | Resolved (directive) |
| GAP-2316 | The agent-monitor object of the access log, the record code of a read, the field list of an entry and the migration step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2318 | The legacy story and the rwb-agent contract name different rights for the same read of the agent monitor | Security administrator | Resolved (directive) |
| GAP-2319 | The secondary slice carries no legacy acceptance criterion of its own, and the legacy data, endpoint, job and screen blocks belong to other services and other slices | Business analyst with the solution architect | Resolved (directive) |
| GAP-2320 | rwb-access answer behind the case and queue list: element names, the P2 attribution of the contract dependency, the authorise branch, the extract record, the login and the parameter and reference paths are not settled by any source read | Solution architect | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
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
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2507 | The consumed rule-evaluation result, the treatment installment-paid call, the three event payloads and the shared record's consumer list have no published schema or operation name | Solution architect, with the owners of rwb-decision, rwb-treatment and the event catalogue | Resolved (directive) |
| GAP-2508 | No numeric operations value and no name of a secret, identity or certificate is specified for the matching deployment | DevOps engineer, with the platform administrator and the identity and access team | Resolved (directive) |
| GAP-2705 | The match consequence that rwb-treatment consumes is not published, and no source names the plan states the treatment row holds after a match | Contract owner of rwb-treatment with the owner of rwb-payment and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2706 | No source names the rule set, the parameter codes or the signal that announce a plan state change, and none states who consumes the plan consequence once rwb-treatment owns it | Solution architect with the rule owner of rwb-decision and the parameters owner of rwb-case | Resolved (directive) |
| GAP-3101 | rwb-deviation case and queue list slice: no read in the Ownership Map, no seam with the composed page, no path, field names or page bound, the flag derived twice and the pause projection without the rule package | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3102 | RWB-S8-E2036-APP: the deviation hold that the queue-write interface obeys has no published element names, no case-event names, no case-side setter for deviation_open and no placement-half criteria, and the pattern set adds dependencies the metadata rows do not carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3149 | rwb-partner interaction-ledger slice: no ledger column or operation in S9, no published payload for EV-20 or EV-21, the seam with RWB-P2-E2034-CON undefined, the list members, the retry bound and the holder-reference form unpublished, and an empty H row against ten platform contracts | Solution architect; rwb-integration contract owner (RWB-P2-E2034-CON); rwb-source-data ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3188 | The payment match rule load is a P4 reference load in the story and a P7 rule package in the target | Decision and rules lead with the access lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P4-E2027-APP | date removed | 1 | 2027-02-01 |
| RWB-P4-E2033-APP | duplicate TC ID | 468 | TC-E2-033-12 |
| RWB-P4-E2041-APP | date added | 1 | 9 December 2026 |
