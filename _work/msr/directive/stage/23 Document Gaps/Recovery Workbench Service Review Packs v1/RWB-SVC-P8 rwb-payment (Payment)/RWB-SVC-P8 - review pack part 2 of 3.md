# RWB-SVC-P8 rwb-payment (Payment) - review pack, part 2 of 3 (RWB-P8-E2027-APP to RWB-P8-E4048-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 304 |
| Cross-document (pending in another document) | 274 |
| Not applied (value not in the sources) | 32 |
| Open business decisions | 9 |
| Register gaps linked | 102 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P8-E2027-APP | 39 | 32 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E2027 APP Payment matching rules with the data team v2.md |
| RWB-P8-E2027-CON | 32 | 28 | 9 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E2027 CON Payment matching rules with the data team - contract v2.md |
| RWB-P8-E2027-OPS | 27 | 37 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E2027 OPS Payment matching rules with the data team - deployment v2.md |
| RWB-P8-E4043-APP | 29 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4043 APP Match a settlement payment v2.md |
| RWB-P8-E4043-CON | 17 | 27 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4043 CON Match a settlement payment - contract v2.md |
| RWB-P8-E4044-APP | 29 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4044 APP Match auction and enforcement proceeds v2.md |
| RWB-P8-E4044-CON | 24 | 20 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4044 CON Match auction and enforcement proceeds - contract v2.md |
| RWB-P8-E4045-APP | 19 | 25 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4045 APP Calculate fees and charges v2.md |
| RWB-P8-E4046-APP | 29 | 24 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4046 APP Post a settlement booking to ALS v2.md |
| RWB-P8-E4047-APP | 35 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4047 APP Post to the general ledger v2.md |
| RWB-P8-E4048-APP | 24 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4048 APP Run the deed in lieu rental auto-debit v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P8-E2027-APP | R-11429 | CG-ALL-7574 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E2027-CON | R-11440 | CG-ALL-7595 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E4043-APP | R-11446 | CG-ALL-7618 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E4044-APP | R-11458 | CG-ALL-7648 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E4045-APP | R-11471 | CG-ALL-7681 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E4046-APP | R-11478 | CG-ALL-7699 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E4047-ITG, RWB-P8-E4047-APP | R-22790 | GAP-2553 | Register gap | Business analyst, P8, with Finance | The posting entry set, the posting type mapping and the rule of the posting of a settlement or a sale route are in no read source | Hold the entry set and the posting type mapping as data of the ledger interface configuration, and publish the posting rule of the settlement and sale routes from the rule registry of rwb-decision |
| RWB-P8-E4047-APP | R-37686 | ASM-4213 | Register assumption |  | The accounting entry set, the chart-of-accounts reference and the posting type a match value maps to stay with the ledger and with Finance, and this service posts the facts of the matched receipt — case, proceeds, receipt, amount, value date, match value and route — as one item on the ledger interface; the mapping is held as data of the interface configuration and no account, cost centre or amount rule is written in code. | Business analyst, P8, with Finance and the ledger owner |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P8-E2027-APP | R-06993 | DOR-RWB-P8-E2027-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the project (searched for epic design). Sign-off value not in sources; needs the epic design record. |
| RWB-P8-E2027-APP | R-18262 | DOR-RWB-P8-E2027-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | Section 9 and SCR-28, SCR-39, SCR-40 text not in the supplied chunk; cannot match old text to add the states. |
| RWB-P8-E2027-APP | R-18263 | DOR-RWB-P8-E2027-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | Detcheck report names no P2 personal-data field for this story; section 12 text not supplied. No edit. |
| RWB-P8-E2027-APP | R-22630 | GAP-0409 | 9 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | No source read gives the ALS fixture, JOB-07 window, harness, seeding, evidence format or gate values. ownership.json gives owners only. No value invented; nothing to edit in this chunk. |
| RWB-P8-E2027-APP | R-26484 | CG-ALL-7575 | 13 | Flyway file V2027_2__payment_matching_rules.sql is not in the V0001..Vnnnn form | The migration line is not in this chunk, and the next free Flyway number of rwb-payment is not in the sources read. Number not invented. |
| RWB-P8-E2027-APP | R-28733 | GAP-1639 | 13 | The two event-started workflows have no name or identifier in any v5 source | No v5 source names the event-started workflow; naming it is not supported. |
| RWB-P8-E2027-APP | R-31581 | NEWAC-RWB-P8-E2027-APP-AC11 | 7 | AC11: §5 X1: A partial payment below the partial floor (covered by AC5, which exist nowhere in this story) | Adding AC11 needs the section 7 and section 16 text, which is not in this chunk, so there is no anchor. Test value not in sources. X1 left unchanged. |
| RWB-P8-E2027-APP | R-31582 | NEWAC-RWB-P8-E2027-APP-AC12 | 7 | AC12: §5 X2: A late payment one day past the window (covered by AC4, which exist nowhere in this story) | Adding AC12 needs the section 7 and section 16 text, which is not in this chunk, so there is no anchor. Test value not in sources. X2 left unchanged. |
| RWB-P8-E2027-CON | R-07000 | DOR-RWB-P8-E2027-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found. Searched 03 Requirements folder and whole project for 'epic design' (no sign-off record). Sign-off needs a value not in sources. |
| RWB-P8-E2027-CON | R-11439 | CG-ALL-7594 MSG-P3-027 text differs from the Error and Message Standard v4 | 14 | MSG-P3-027 text differs from the Error and Message Standard v4 | Standard v4 wording is not in the chunk (DOR-RWB-P8-E2027-CON-9). Not specified in the source documents (CG-ALL-7594). |
| RWB-P8-E2027-CON | R-22627 | GAP-2506 | 7, 12, 16 and metadata C row | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Sections 7, 12, 16 and the metadata C row are not in this chunk, so no exact-match edit. Re-send them to add C RWB-P7-E1073-CON and fix AC6. |
| RWB-P8-E2027-CON | R-22630 | GAP-0409 | 16 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | No source gives the ALS fixture, JOB-07 window control, harness seeding or pass gate. Needs P8, P7 and QA agreement. Not specified in the source documents (GAP-0409). |
| RWB-P8-E2027-CON | R-22634 | GAP-1359 | 12 | The rule-evaluation result has no published schema and two of its field names are not given | Section 12 RuleResult text is not in this chunk, so no exact-match edit. Re-send section 12 to place the schema and the two placeholder names. |
| RWB-P8-E2027-CON | R-22635 | GAP-1360 | 12 | The three payment event payloads have no schema in any source | Section 12 AsyncAPI payload text is not in this chunk, so no exact-match edit. Re-send section 12 to place the three payload fragments. |
| RWB-P8-E2027-CON | R-22638 | GAP-1880 | 12 | The treatment-side matching read, the shortfall columns, the breach decision code and the plan-check cadence are not specified | Section 12 treatment-side read and breach code text is not in this chunk, so no exact-match edit. Re-send section 12. |
| RWB-P8-E2027-CON | R-22639 | GAP-2507 | 12 | The consumed rule-evaluation result, the treatment installment-paid call, the three event payloads and the shared record's consumer list have no published schema or operation name | Section 12 surfaces (RuleResult, treatment call, payloads, DecisionRecorded) are not in this chunk, so no exact-match edit. Re-send section 12. |
| RWB-P8-E2027-CON | R-22641 | GAP-2705 | 12 | The match consequence that rwb-treatment consumes is not published, and no source names the plan states the treatment row holds after a match | The contract read belongs in section 12, which is not in this chunk, so no exact-match edit. Re-send section 12. |
| RWB-P8-E2027-OPS | R-07006 | DOR-RWB-P8-E2027-OPS-16 | header | Definition of Ready item 16 Size: Fail | No size value is in the sources. The item stays open until the squad sizes the story. |
| RWB-P8-E4044-APP | R-07022 | DOR-RWB-P8-E4044-APP-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources (Grep found none). Definition of Ready text is not in this chunk, so no exact old text to edit. No sign-off value written. |
| RWB-P8-E4044-APP | R-18310 | DOR-RWB-P8-E4044-APP-11 | 8 | Definition of Ready item 11 Guardrails: Partial | Section 8 text is not in this chunk, so no exact old text to edit. Data Classification v5 gives Not personal = Internal, personal flag No; apply in section 8 on the next run. |
| RWB-P8-E4044-APP | R-29017 | GAP-1374 | 12.5 | The name of the JOB-07 event-started workflow is not published | Section 12.5 text is not in this chunk. JOB-07 workflow name is not published; use placeholder Not specified in the source documents (GAP-1374) in 12.5 on the next run. |
| RWB-P8-E4044-CON | R-18327 | DOR-RWB-P8-E4044-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sources give no separate BR IDs beyond column 1, so no column was added. |
| RWB-P8-E4044-CON | R-23133 | GAP-1369 | 7, 16 | Legacy acceptance criteria and test cases of RWB-E4-044 are generic placeholders | Sections 7 and 16 are not in the chunk, so no exact old text exists. The mp/out copy has different numbering and was not used. |
| RWB-P8-E4044-CON | R-23143 | GAP-1892 | 12.3, 12.4 | ProceedsMatched does not list rwb-litigation as a consumer, so the payment fact cannot arrive as an event | Text of 12.3 and 12.4 is not in the chunk, so the old text cannot be copied to declare None. The mp/out copy was not used. |
| RWB-P8-E4044-CON | R-29017 | GAP-1374 | 12.5 | The name of the JOB-07 event-started workflow is not published | Text of 12.5 is not in the chunk. The mp/out copy cites GAP-2520 and ASM-4170, not GAP-1374, so it was not used. |
| RWB-P8-E4045-APP | R-18337 | DOR-RWB-P8-E4045-APP-3 | 5 | Definition of Ready item 3 Acceptance criteria: Partial | No section 5 change is in the diff. The Covered by column sits on the error table; section 5 needs its own Covered by column. |
| RWB-P8-E4046-APP | R-18342 | DOR-RWB-P8-E4046-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-28 and SCR-29 screen sections are outside this chunk. FSD P8 v4 lines 916-917 name no empty, loading, error or no-access states, so none can be written without inventing them. |
| RWB-P8-E4046-APP | R-22766 | GAP-0436 |  | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Harness values belong to W3J01, not this story. No source gives them; the wave 3 entry check with the Integration lead must agree them first. Placeholders kept. |
| RWB-P8-E4046-APP | R-22785 | GAP-0432 |  | ALS interface, booking operation and wave 3 harness pack are not specified | ALS interface ID, transport, layout and rwb-payment operation are in no source (Architecture v5 slides 16, 18, 43). Owned by the ALS interface story; agree at wave 3 entry check. |
| RWB-P8-E4047-APP | R-18353 | DOR-RWB-P8-E4047-APP-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 is not in the supplied story text, so its Empty, Error and No access rows cannot be copied as exact old text. Needs section 15 in the chunk. |
| RWB-P8-E4048-APP | R-07056 | DOR-RWB-P8-E4048-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No contract fake version in story set, Change Register v1 or realignment folder (grep 'fake'). Not invented; needs the published fake version. |
| RWB-P8-E4048-APP | R-23149 | GAP-2522 | 14 | The wording of MSG-P8-001 and MSG-P8-002 is not in the read sources | IDs have a different meaning in the standard; text stays Not specified (GAP-2522). |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (30)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13086 | RWB-P8-E2027-CON | DOR-RWB-P8-E2027-CON-8 |  | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} under the /api/recovery/decision/v1 base (CG-ALL-7585, CG-ALL-7586). |
| CDC-13099 | RWB-P8-E2027-CON | GAP-1293 | 12 | Attribute rule-package load to P7 rwb-decision on /api/recovery/decision/v1 using /admin/rule-packages and /admin/rule-package-versions. Mark /admin/rule-versions as legacy with no target story. Correct the P4 attribution and monolith base in legacy section 12. |
| CDC-13147 | RWB-P8-E4043-APP | CG-ALL-7610 | 12.2 | Declare REST base /api/recovery/treatment/v1 for the treatment provider so the GET /treatments/{treatmentId} path in 12.2 resolves. |
| CDC-13148 | RWB-P8-E4043-APP | CG-ALL-7611 | 12.2 | Declare REST base /api/recovery/case/v1 for the case provider used in 12.2. |
| CDC-13149 | RWB-P8-E4043-APP | CG-ALL-7612 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the source-data provider used in 12.2. |
| CDC-13150 | RWB-P8-E4043-APP | CG-ALL-7613 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package provider used in 12.2. |
| CDC-13155 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-8 | 12 | Add base paths /api/recovery/treatment/v1, /api/recovery/case/v1, /api/recovery/source-data/v1 and /api/recovery/decision/v1, and the two further paths the detcheck lists. |
| CDC-13165 | RWB-P8-E4043-APP | GAP-2514 | 4 | Publish the MatchRequest element (case reference, treatment reference, account payment reference, amount, received date, match value) and the ProceedsPage element (page, size, total). |
| CDC-13169 | RWB-P8-E4043-CON | CG-ALL-7628 | 12.2 | Declare the REST base /api/recovery/treatment/v1 for the provider rwb-treatment, taken from the Document Index service table. |
| CDC-13170 | RWB-P8-E4043-CON | CG-ALL-7629 | 12.2 | Declare the REST base /api/recovery/case/v1 for the provider rwb-case, taken from the Document Index service table. |
| CDC-13171 | RWB-P8-E4043-CON | CG-ALL-7630 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the provider rwb-source-data, taken from the Document Index service table. |
| CDC-13172 | RWB-P8-E4043-CON | CG-ALL-7631 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the provider rwb-decision, taken from the Document Index service table. |
| CDC-13175 | RWB-P8-E4043-CON | DOR-RWB-P8-E4043-CON-8 | 12.2 | Declare REST bases for /api/recovery/treatment/v1, /api/recovery/case/v1, /api/recovery/source-data/v1 and /api/recovery/decision/v1 (items CG-ALL-7628 to CG-ALL-7631). |
| CDC-13196 | RWB-P8-E4044-APP | CG-ALL-7641 | 12.2 | Declare the REST base for /api/recovery/case/v1 (provider P3 rwb-case) from the Document Index service table. |
| CDC-13197 | RWB-P8-E4044-APP | CG-ALL-7642 | 12.2 | Declare the REST base for /api/recovery/decision/v1 (provider P7 rwb-decision) from the Document Index service table. |
| CDC-13214 | RWB-P8-E4044-CON | CG-ALL-7656 | 12.2 | Declare REST base /api/recovery/case/v1 for the P3 rwb-case provider, taken from the Document Index service table. |
| CDC-13215 | RWB-P8-E4044-CON | CG-ALL-7657 | 12.2 | Declare REST base /api/recovery/decision/v1 for the P7 rwb-decision provider, taken from the Document Index service table. |
| CDC-13234 | RWB-P8-E4045-APP | CG-ALL-7671 | 12.2 | Declare the REST base of /api/recovery/case/v1 from the Document Index service table for provider P3 rwb-case. |
| CDC-13235 | RWB-P8-E4045-APP | CG-ALL-7672 | 12.2 | Declare the REST base of /api/recovery/case/v1 from the Document Index service table for provider P3 rwb-case. |
| CDC-13236 | RWB-P8-E4045-APP | CG-ALL-7673 | 12.2 | Declare the REST base of /api/recovery/partner/v1 from the Document Index service table for provider S9 rwb-partner. |
| CDC-13259 | RWB-P8-E4046-APP | CG-ALL-7686 | 12.2 | Declare REST base /api/recovery/treatment/v1 for GET /treatments/{treatmentId}, taken from the Document Index service table. |
| CDC-13260 | RWB-P8-E4046-APP | CG-ALL-7687 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the data product read, taken from the Document Index service table. |
| CDC-13261 | RWB-P8-E4046-APP | CG-ALL-7688 | 12.2 | Declare REST base /api/recovery/integration/v1 for GET /admin/outbound-items, taken from the Document Index service table. |
| CDC-13262 | RWB-P8-E4046-APP | CG-ALL-7689 | 12.2 | Declare REST base /api/recovery/case/v1 for the case reference and route state read, taken from the Document Index service table. |
| CDC-13266 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-8 | Header | Add base paths /api/recovery/treatment/v1, /api/recovery/source-data/v1, /api/recovery/integration/v1, /api/recovery/case/v1 and the five further bases detcheck reports. |
| CDC-13301 | RWB-P8-E4048-APP | CG-ALL-7720 | 12.2 | Declare the REST base /api/recovery/treatment/v1 (from the Document Index service table) in the yaml for rwb-treatment. |
| CDC-13302 | RWB-P8-E4048-APP | CG-ALL-7721 | 12.2 | Declare the REST base /api/recovery/source-data/v1 (from the Document Index service table) in the yaml for rwb-source-data. |
| CDC-13303 | RWB-P8-E4048-APP | CG-ALL-7722 | 12.2 | Declare the REST base /api/recovery/case/v1 (from the Document Index service table) in the yaml for rwb-case. |
| CDC-13304 | RWB-P8-E4048-APP | CG-ALL-7723 | 12.2 | Declare the REST base /api/recovery/decision/v1 (from the Document Index service table) in the yaml for rwb-decision. |
| CDC-13307 | RWB-P8-E4048-APP | DOR-RWB-P8-E4048-APP-8 | 12.1 | Add the bases /api/recovery/treatment/v1, /api/recovery/source-data/v1, /api/recovery/case/v1 and /api/recovery/decision/v1, and the Idempotency-Key header on POST /proceeds/{proceedsId}/match. Story already declares the key in section 12.1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13156 | RWB-P8-E4043-APP | CG-ALL-7608 | 4 | Add account_payment_id for proceeds (DF-FIN-004, TSD P8 T3.1) to both Fields lists, or name the dictionary field it stands for. |
| CDC-13161 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-7 | 11 | Record field account_payment_id on proceeds and entity decision_record, or confirm they are platform library objects. Section 11 row without BR Field ID now carries the placeholder. |
| CDC-13202 | RWB-P8-E4044-APP | CG-ALL-7638 | 11 | Add account_payment_id as the ACE payment reference (DF-FIN-004; GAP-2521), or name the dictionary field that holds it. |
| CDC-13203 | RWB-P8-E4044-APP | CG-ALL-7639 | 12.4; 12.7 | Record inbox_event as a platform library table created in rwb_payment (DP-09), or name the dictionary object for it. |
| CDC-13204 | RWB-P8-E4044-APP | CG-ALL-7640 | 12.7 | Record decision_record as a platform library table created in rwb_payment (DP-03), or name the dictionary object for it. |
| CDC-13219 | RWB-P8-E4044-CON | CG-ALL-7652 | 11 | Record account_payment_id as a field or entity in the owning document, or confirm the dictionary name for its uses |
| CDC-13220 | RWB-P8-E4044-CON | CG-ALL-7653 | 11 | Record account_payment as a field or entity in the owning document, or confirm the dictionary name for its use |
| CDC-13221 | RWB-P8-E4044-CON | CG-ALL-7654 | 12.4, 12.7 | Record inbox_event as a platform library table object in the owning document, or confirm the dictionary name; nearest is outbox_event |
| CDC-13222 | RWB-P8-E4044-CON | CG-ALL-7655 | 12.7 | Record decision_record as a platform library table object in the owning document, or confirm the dictionary name |
| CDC-13225 | RWB-P8-E4044-CON | DOR-RWB-P8-E4044-CON-7 | 11 | Declare account_payment_id, account_payment, inbox_event and decision_record, plus the one further name the detcheck flags, as fields or entities. |
| CDC-13243 | RWB-P8-E4045-APP | CG-ALL-7668 | 1, 4, 12.1, 17 | Record fees_outstanding (DF-ACC-011) under the dictionary name, or record the object in the owning document. |
| CDC-13244 | RWB-P8-E4045-APP | CG-ALL-7669 | 12.4, 12.7 | Record inbox_event as a platform library table created in rwb_payment, or use the dictionary name. |
| CDC-13245 | RWB-P8-E4045-APP | CG-ALL-7670 | 12.7 | Record decision_record as a platform library table created in rwb_payment, or use the dictionary name. |
| CDC-13249 | RWB-P8-E4045-APP | DOR-RWB-P8-E4045-APP-7 | 11 | Register fees_outstanding, inbox_event and decision_record as fields or entities, or confirm their DF IDs (DF-ACC-011 and the platform library tables). |
| CDC-13274 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-7 | 11 | Add decision_record as an entity with its §11 fields, or confirm it as a PLT library object, and classify it in Data Classification v5. |
| CDC-13289 | RWB-P8-E4047-APP | CG-ALL-7704 | 3, 11, 12.7 | Record decision_record as the platform library created in rwb_payment (DP-03), or give it a dictionary name in the Fields of the owning document. |
| CDC-13294 | RWB-P8-E4047-APP | DOR-RWB-P8-E4047-APP-7 | 11 | Add decision_record as the local platform-library entity of rwb_payment (DP-03) to the entity list of both documents. |
| CDC-13317 | RWB-P8-E4048-APP | DOR-RWB-P8-E4048-APP-7 | 11 | Add entity decision_record (PLT library, rwb_payment), field account_payment_id of proceeds, and event attribute ce_source |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13056 | RWB-P8-E2027-APP | CG-ALL-7564 | Header | Record decision_record as a platform library table (RWB-PLT-E1027-CON) with its DF-DEC-001 to DF-DEC-031 columns, not as an LDM field. Story name unchanged. |
| CDC-13057 | RWB-P8-E2027-APP | DOR-RWB-P8-E2027-APP-7 | 11 | Add entity decision_record (P2, PLT library table created in rwb_payment, fields DF-DEC-001 to DF-DEC-031) and classify it in Data Classification v5. |
| CDC-13087 | RWB-P8-E2027-CON | CG-ALL-7583 | 11 | Confirm the dictionary name of the payment account identifier on proceeds (story line 222 uses account_payment_id) or add it to Fields. |
| CDC-13090 | RWB-P8-E2027-CON | DOR-RWB-P8-E2027-CON-7 | 11 | Register decision_record, ce_type, account_payment_id and ce_subject as fields or entities, or state the story's CloudEvents and table names where they are not LDM objects. |
| CDC-13118 | RWB-P8-E2027-OPS | CG-ALL-7598 | 12.7 | Record decision_record as a PLT library table in LDM v9 (owner role Data), or use its dictionary name; section 12.7 already names it as a library table |
| CDC-13157 | RWB-P8-E4043-APP | CG-ALL-7609 | 12.7 | Record decision_record as a platform library table created in rwb_payment (DP-03), as section 12.7 states, or name the dictionary object. |
| CDC-13176 | RWB-P8-E4043-CON | CG-ALL-7622 | find it | Record ce_type, ce_source, ce_subject, ce_id and ce_specversion as CloudEvents 1.0 binary-mode envelope attributes of the event messages, not as entity fields. |
| CDC-13177 | RWB-P8-E4043-CON | CG-ALL-7623 | 4, 7, 12.3 | Record ce_source as a CloudEvents 1.0 envelope attribute of the three event schemas, or use the dictionary name for it |
| CDC-13178 | RWB-P8-E4043-CON | CG-ALL-7624 | 4, 12.3 | Record ce_subject as a CloudEvents 1.0 envelope attribute of the three event schemas, or use the dictionary name for it |
| CDC-13179 | RWB-P8-E4043-CON | CG-ALL-7625 | 11, 1, 7 | Add account_payment_id as a Proceeds element column of DF-FIN-001 to DF-FIN-009, or use the dictionary name for it |
| CDC-13180 | RWB-P8-E4043-CON | CG-ALL-7626 | 12.3 | Record ce_specversion as a CloudEvents 1.0 envelope attribute of the three event schemas |
| CDC-13181 | RWB-P8-E4043-CON | CG-ALL-7627 | 7, 12.3 | Record ce_id as a CloudEvents 1.0 envelope attribute of the three event schemas |
| CDC-13208 | RWB-P8-E4044-APP | DOR-RWB-P8-E4044-APP-7 | 11 | Add account_payment_id, inbox_event and decision_record to LDM v9 or Data Classification v5 (or re-point them); confirm the ACE view reads in the criteria. |
| CDC-13267 | RWB-P8-E4046-APP | CG-ALL-7685 | 208 | Record decision_record as a platform library object created in rwb_payment, or give it a dictionary entity or field name. |
| CDC-13281 | RWB-P8-E4046-APP | GAP-2551 | 8 | Record that the booking item is outbound_item in rwb_integration and rwb_payment holds no booking row; keep the item reference on TreatmentBooked as the booking reference. |
| CDC-13308 | RWB-P8-E4048-APP | CG-ALL-7717 | 3, 12.7 | Record decision_record as the local decision record library object of RWB-PLT-E1027-CON (DP-03), created in rwb_payment, or add it as a field or entity. |
| CDC-13309 | RWB-P8-E4048-APP | CG-ALL-7718 | 4, 8 | Add account_payment_id as the identifier of the receipt held in the proceeds table of rwb_payment (DF-FIN-004), or use the dictionary name for it. |

### RWB-P8-E2027-CON (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13053 | RWB-P8-E2027-APP | DOR-RWB-P8-E2027-APP-21 | none | Complete RWB-P8-E2027-CON and set its build status to Done |
| CDC-13054 | RWB-P8-E2027-APP | DOR-RWB-P8-E2027-APP-22 | none | Publish the contract fake library and record its version as published |
| CDC-13069 | RWB-P8-E2027-APP | GAP-1359 | 12 | Publish RuleResult as packageCode, versionInForce, ruleId, rowOrder and outputs; mark the two unnamed operation names as placeholders. rwb-decision to confirm in RWB-P7-E1073-CON. |
| CDC-13070 | RWB-P8-E2027-APP | GAP-1360 | 12 | Publish the payload field lists of TreatmentBooked, PaymentMissed and ProceedsMatched in the AsyncAPI fragment as the working read, identifiers and facts only, and confirm with the consumers. |
| CDC-13072 | RWB-P8-E2027-APP | GAP-2507 | 12 | Publish RuleResult with NoPackageInForce outcome; declare version-in-force read and installment-paid operation as placeholders; publish three payload field lists; declare DecisionRecorded read-only on shared topic. |
| CDC-13074 | RWB-P8-E2027-APP | GAP-2705 | 9 | Publish one read returning payment code, due date, match type, rule ID, package code and version, and shortfall per case and plan; name payload members at major version 1 and carry the four plan states. |
| CDC-13115 | RWB-P8-E2027-OPS | DOR-RWB-P8-E2027-OPS-21 | header | Complete build of RWB-P8-E2027-CON and publish the contract so its build status reads Done. |
| CDC-13116 | RWB-P8-E2027-OPS | DOR-RWB-P8-E2027-OPS-22 | header | Publish a contract fake library version and record it as published. |
| CDC-13132 | RWB-P8-E2027-OPS | GAP-1360 | 12.3 | Keep the marked payload field lists of TreatmentBooked, PaymentMissed and ProceedsMatched in the AsyncAPI fragment and confirm them with the catalogue consumers. |
| CDC-13133 | RWB-P8-E2027-OPS | GAP-1880 | find it | Publish the treatment-side matching read and payload, the treatment plan-state column and BROKEN outcome, the plan-breach decision code, and the 30-day plan-check cadence with its durable timer. |
| CDC-13134 | RWB-P8-E2027-OPS | GAP-2507 | find it | Publish RuleResult as packageCode, versionInForce, ruleId, rowOrder and outputs with NoPackageInForce; declare placeholder operation names; give three event payload field lists; declare DecisionRecorded read-only. |
| CDC-13135 | RWB-P8-E2027-OPS | GAP-2705 | find it | Publish one read returning payment code, installment due date, match type, rule ID, package code and version, and shortfall per case and plan; name payload members at major version 1; carry the four plan states. |
| CDC-13136 | RWB-P8-E2027-OPS | GAP-2706 | find it | Name the package code of the RES rule set, evaluate it in rwb-treatment, read CURE_PERIOD_DAYS and restructure.max_breaks from the rwb-case parameters contract, and publish no plan event in wave 2. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13158 | RWB-P8-E4043-APP | CG-ALL-7617 | 16 | Add rows TC-E4-043-01 to TC-E4-043-04 with Given, When and Then copied from the criteria they cover (AC1, AC2, AC7 access, Principle 5). |
| CDC-13163 | RWB-P8-E4043-APP | GAP-2510 | 7 | Carry the confirmed settlement data set (case, settlement treatment, receipt, amount, business date) into TC-E4-043-01 and TC-E4-043-02, and add the FEAT-PAY-03 requirement row to FSD P8. |
| CDC-13184 | RWB-P8-E4043-CON | DOR-RWB-P8-E4043-CON-12 | 12.7, 16 | Story gains boundary case TC-P8-E4043-CON-07 for the 12.7 tables; the workbook rows are missing and belong to v8. |
| CDC-13192 | RWB-P8-E4043-CON | CG-ALL-7634 | 16 | Add rows TC-P8-E4043-CON-01 to TC-P8-E4043-CON-05 with Given, When and Then copied from the criteria they cover. |
| CDC-13206 | RWB-P8-E4044-APP | CG-ALL-7647 | 16 | Add rows TC-E4-044-01 to TC-E4-044-04 with Given, When and Then copied from AC1, AC2, Access and Principle 5 in section 7. |
| CDC-13224 | RWB-P8-E4044-CON | DOR-RWB-P8-E4044-CON-12 | 12.7, 16 | Add rows for TC-P8-E4044-CON-01 to TC-P8-E4044-CON-06 and the new TC-P8-E4044-CON-07 |
| CDC-13232 | RWB-P8-E4044-CON | CG-ALL-7664 | 16 | Add rows for TC-P8-E4044-CON-01 to TC-P8-E4044-CON-06 with Given, When and Then copied from the criteria they cover. |
| CDC-13247 | RWB-P8-E4045-APP | CG-ALL-7679 | 16 | Add rows for TC-E4-045-01 to TC-E4-045-04 with Given, When and Then copied from the criteria they cover in section 7. |
| CDC-13271 | RWB-P8-E4046-APP | CG-ALL-7697 | 16 | Add rows TC-E4-046-01 to TC-E4-046-04 to tab Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-13272 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-12 | 16 | Add rows TC-E4-046-01 to TC-E4-046-11 under tab Story test cases; the story now has boundary row TC-E4-046-05 and criteria AC3 to AC9. |
| CDC-13293 | RWB-P8-E4047-APP | CG-ALL-7712 | 16 | Add rows TC-E4-047-01, TC-E4-047-02, TC-E4-047-03 and TC-E4-047-04 to Story test cases in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-13314 | RWB-P8-E4048-APP | CG-ALL-7730 | 16 | Add rows TC-E4-048-01, TC-E4-048-02, TC-E4-048-03 and TC-E4-048-04 to the next Story test cases version, with Given, When and Then copied from the criteria they cover. |
| CDC-13315 | RWB-P8-E4048-APP | DOR-RWB-P8-E4048-APP-12 | 16 | Register TC-E4-048-01 to TC-E4-048-07 (legacy 01 to 04 and new contract and boundary cases 05 to 07) |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13058 | RWB-P8-E2027-APP | DOR-RWB-P8-E2027-APP-9 | 14 | Confirm the MSG-P3-027 text against v4 and align §14 and the test data to the v4 wording. |
| CDC-13091 | RWB-P8-E2027-CON | DOR-RWB-P8-E2027-CON-9 | 14 | Confirm the MSG-P3-027 text against the standard v4 wording and align either the standard or the section 14 text, recording any variance. |
| CDC-13162 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-9 | 14 | Align MSG-P1-001 text with the standard, or confirm the FSD wording as the standard text. Story keeps the FSD wording until then. |
| CDC-13250 | RWB-P8-E4045-APP | DOR-RWB-P8-E4045-APP-9 | 14 | Confirm the MSG-P1-001 text, or supply the v4 text so sections 5, 8 and 14 of the story can be aligned to it. |
| CDC-13258 | RWB-P8-E4045-APP | CG-ALL-7678 | 14 | MSG-P1-001 text reverted to the story wording |
| CDC-13275 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-9 | 14 | Provide MSG-P1-001 wording as the standard holds it so §14 and VR-P8-006-1 can copy it; MSG-P2-001 text is Not specified in the source documents. |
| CDC-13292 | RWB-P8-E4047-APP | CG-ALL-7711 | 14 | Add a new message ID for a ledger rejection that puts the item on rwb-integration's exception queue; MSG-P2-001 keeps its standard meaning. The story cites the new ID after it exists. |
| CDC-13295 | RWB-P8-E4047-APP | DOR-RWB-P8-E4047-APP-9 | 14 | MSG-P1-001 story text kept as before |
| CDC-13299 | RWB-P8-E4047-APP | CG-ALL-7710 | 14 | MSG-P1-001 text kept as story text; not changed to standard wording |
| CDC-13311 | RWB-P8-E4048-APP | CG-ALL-7727 | 4, 14 | MSG-P8-001 row restored to placeholder text |
| CDC-13312 | RWB-P8-E4048-APP | CG-ALL-7728 | 4, 14 | MSG-P8-002 row restored to placeholder text |
| CDC-13313 | RWB-P8-E4048-APP | CG-ALL-7729 | 4, 14 | Business analyst adds a new message ID for the consumed answer timeout; section 14 then cites it. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13151 | RWB-P8-E4043-APP | CG-ALL-7615 | 12.5 | Add a Workflows row for PaymentMatchingWorkflow: task queue rwb-payment, namespace rwb-recovery, event-started by AceDataReady, with the signals named in 12.5. |
| CDC-13173 | RWB-P8-E4043-CON | CG-ALL-7632 | 12.5 | Add a Workflows row for the JOB-07 event-started workflow (PaymentMatchingWorkflow, started by AceDataReady, task queue rwb-payment, namespace rwb-recovery). |
| CDC-13198 | RWB-P8-E4044-APP | CG-ALL-7644 | 12.5 | Add the JOB-07 payment-matching workflow row to the Workflows sheet, under the name used in §12.5 once it is specified. |
| CDC-13212 | RWB-P8-E4044-APP | GAP-2520 | 12.5 | Name the JOB-07 workflow and its matching activity, state whether the trigger is EV-26 batch completion or a Schedule, and publish the activity input and output. |
| CDC-13223 | RWB-P8-E4044-CON | CG-ALL-7662 | 12.5 | Add the activity 'The matching activity' (name Not specified in the source documents (GAP-2520; ASM-4170)) to the Activities sheet, or use a catalogued activity |
| CDC-13230 | RWB-P8-E4044-CON | GAP-2520 | 4 | Name the JOB-07 workflow and its matching activity; state whether the trigger is the batch-completion event EV-26 or a Schedule; publish the activity input and output. |
| CDC-13257 | RWB-P8-E4045-APP | GAP-2546 | 12.5 | Name the fee run and its activity, and state in FSD P8 A2.5.2 whether the trigger is the fee-due event or the daily batch completion. |
| CDC-13268 | RWB-P8-E4046-APP | CG-ALL-7693 | 12.5 | Add an Activities row for postBooking on queue rwb-payment, with its input and output as stated in section 12.5. |
| CDC-13269 | RWB-P8-E4046-APP | CG-ALL-7694 | 12.5 | Add an Activities row for readBackBooking on queue rwb-payment, with its input and output as stated in section 12.5. |
| CDC-13270 | RWB-P8-E4046-APP | CG-ALL-7695 | 12.5 | Add an Activities row for deliverFile(manifest) on queue rwb-integration, with its input and output as stated in section 12.5. |
| CDC-13290 | RWB-P8-E4047-APP | CG-ALL-7708 | 12.5 | Add activity confirmBookings (JOB-08 booking confirmation) to the Activities sheet, or name a catalogued activity in its place. |
| CDC-13291 | RWB-P8-E4047-APP | CG-ALL-7709 | 12.5 | Add the outbound-call activity of rwb-integration, name Not specified in the source documents (GAP-2557; ASM-4217), to the Activities sheet, or name a catalogued activity. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13088 | RWB-P8-E2027-CON | DOR-RWB-P8-E2027-CON-1 | 1 | Add role 'tech lead' as a role code or name, or the story actor is changed to an existing role in that document. |
| CDC-13119 | RWB-P8-E2027-OPS | DOR-RWB-P8-E2027-OPS-1 | 1 | Add platform engineer as a role code or name, or the story must name the existing role code from the register |
| CDC-13160 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-6 | 10 | Add role SY-DATALOAD (data load from COLLINS) with Write-off and posting U. Story side adds the rwb-access authorise check per operation. |
| CDC-13182 | RWB-P8-E4043-CON | DOR-RWB-P8-E4043-CON-1 | 1 | Add the role 'tech lead of rwb-payment' as a role code or role name, or name the existing role code used in section 1 |
| CDC-13207 | RWB-P8-E4044-APP | DOR-RWB-P8-E4044-APP-6 | 10 | Add role SY-DATALOAD with the match right (U) in Users Roles and Permissions v5, or remove it from section 10 of this story. |
| CDC-13248 | RWB-P8-E4045-APP | DOR-RWB-P8-E4045-APP-6 | 10 | Add role code SY-DATALOAD, which section 10 of RWB-P8-E4045-APP and TSD P8 T6.1 (right R) name. |
| CDC-13273 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-6 | 10 | Add role SY-DATALOAD (data load from COLLINS) with the Write-off and posting U right as §10 states. |
| CDC-13316 | RWB-P8-E4048-APP | DOR-RWB-P8-E4048-APP-6 | 10 | Add role SY-DATALOAD (data load identity, right U on the match operation) |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13113 | RWB-P8-E2027-OPS | DOR-RWB-P8-E2027-OPS-14 | header | Record the signed epic design sign-off for RWB-SVC-P8 in the epic design record. |
| CDC-13152 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-14 | header | Record the signed epic design sign-off for this story's epic and confirm it against the epic design record. |
| CDC-13174 | RWB-P8-E4043-CON | DOR-RWB-P8-E4043-CON-14 | Header | Record the signed sign-off for the epic design of RWB-P8-E4043-CON. |
| CDC-13217 | RWB-P8-E4044-CON | DOR-RWB-P8-E4044-CON-14 | Header | Record the signed epic design sign-off for RWB-P8-E4044-CON, then confirm it against the epic design record. |
| CDC-13240 | RWB-P8-E4045-APP | DOR-RWB-P8-E4045-APP-14 | find it | Record the signed epic design sign-off for RWB-P8-E4045-APP. |
| CDC-13264 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-14 | header | Record the signed epic design sign-off; the story is then re-checked against DoR item 14. |
| CDC-13285 | RWB-P8-E4047-APP | DOR-RWB-P8-E4047-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-P8 in the epic design record. |
| CDC-13305 | RWB-P8-E4048-APP | DOR-RWB-P8-E4048-APP-14 | 14 | Record the signed epic design sign-off, then the story can cite it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13050 | RWB-P8-E2027-APP | CG-ALL-7565 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions through the provider's CON story |
| CDC-13051 | RWB-P8-E2027-APP | CG-ALL-7566 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} through the provider's CON story |
| CDC-13082 | RWB-P8-E2027-CON | CG-ALL-7585 | 12.2 | Publish the operation GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in rwb-decision.yaml. |
| CDC-13083 | RWB-P8-E2027-CON | CG-ALL-7586 | 12.2 | Declare the REST base /api/recovery/decision/v1 in rwb-decision.yaml. |
| CDC-13110 | RWB-P8-E2027-OPS | CG-ALL-7599 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions through the provider's CON story, or consume a published operation. |
| CDC-13111 | RWB-P8-E2027-OPS | CG-ALL-7600 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} through the provider's CON story, or consume a published operation. |

### OTHER:FSD P8 v3 (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13121 | RWB-P8-E2027-OPS | GAP-1625 |  | Replace the placeholder criteria AC-P8-003-01 to AC-P8-011-01 (A2.3.4.1 to A2.11.4.1) with the testable criteria written in PRD P8 from feature statement, business rules and field list. |
| CDC-13123 | RWB-P8-E2027-OPS | GAP-1631 |  | Integration points: read ALS via rwb-source-data after the next completed ACE batch; send ledger postings via rwb-integration; auto-debit and LED routes stay outside the 19 services until named. |
| CDC-13253 | RWB-P8-E4045-APP | GAP-2542 | 7 | Publish the FEAT-PAY-05 fee facts as a documented example set in the next version of FSD P8. |
| CDC-13255 | RWB-P8-E4045-APP | GAP-2544 | 4 | Publish the fee type list and fee rows with rate, cap, validity and version, and add the message for a fee type with no row in force. |
| CDC-13277 | RWB-P8-E4046-APP | GAP-2547 | 7 | Publish the FEAT-PAY-06 booking data set in A2.6 (case, treatment, account, accepted amount, business date, ALS interface) and add the slice requirement row in the next split-plan version. |
| CDC-13278 | RWB-P8-E4046-APP | GAP-2549 | 11 | Correct the Data table of A2.6 and the DP-05 row so only rwb-source-data is shown reading recovery.v_ace_* views; retire the v_ace_account and v_ace_payment reads of rwb-payment. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13052 | RWB-P8-E2027-APP | CG-ALL-7567 | 13 | Create story file RWB-P7-E1073-CON (the rwb-decision C row of DP-04) |
| CDC-13084 | RWB-P8-E2027-CON | CG-ALL-7588 | 13 | Create story RWB-P7-E1073-CON or name the existing story that carries the rule-model registry capability. |
| CDC-13085 | RWB-P8-E2027-CON | DOR-RWB-P8-E2027-CON-17 | find it | Create story RWB-P7-E1073-CON or name the existing story for the DP-04 class-C dependency. |
| CDC-13112 | RWB-P8-E2027-OPS | CG-ALL-7601 | 13 | Name the existing story for the DP-04 capability or create RWB-P7-E1073-CON; no such file exists today. |
| CDC-13114 | RWB-P8-E2027-OPS | DOR-RWB-P8-E2027-OPS-17 | 13 | Create or name the existing story behind the RWB-P7-E1073-CON dependency, as in CG-ALL-7601. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13066 | RWB-P8-E2027-APP | GAP-0260 |  | Add a row for payment_match_rule as retired: owner P3 rwb-case (retired table) with values as versioned reference rows; PAYMENT_MATCH rule package owned by P7 rwb-decision. |
| CDC-13097 | RWB-P8-E2027-CON | GAP-0260 |  | Add a row for payment_match_rule as a retired table: owner P3 rwb-case (retired table), with the PAYMENT_MATCH rule package owned by P7 rwb-decision, and mark its 13 field rows retired. |
| CDC-13126 | RWB-P8-E2027-OPS | GAP-0260 |  | Keep the 13 payment_match_rule rows and field IDs, mark retired as a table, Owner P3 rwb-case (retired table); PAYMENT_MATCH rule package is P7 rwb-decision (D-RCV-36). |
| CDC-13211 | RWB-P8-E4044-APP | GAP-2519 | 4 | Publish the proceeds payment match package with package code, rule IDs and values; record in the Ownership Map whether payment_match_rule is a rwb-decision rule row or a rwb-case reference-data row. |
| CDC-13229 | RWB-P8-E4044-CON | GAP-2519 | Header | Publish the package code, rule IDs and values for auction, broker and LED proceeds; record whether payment_match_rule is a rwb-decision rule row or a rwb-case reference-data row. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13067 | RWB-P8-E2027-APP | GAP-1290 |  | Add the rollback body, dry-run detail, governance decision code and approve and promote shapes before the wave 2 contract freeze. |
| CDC-13068 | RWB-P8-E2027-APP | GAP-1293 | 12 | Correct legacy section 12 P4 attribution and monolith base to P7 rwb-decision on /api/recovery/decision/v1, using /admin/rule-packages and /admin/rule-package-versions. Keep /admin/rule-versions as a legacy path with no target story. |
| CDC-13098 | RWB-P8-E2027-CON | GAP-1290 | 14 | Add the governance decision code, rollback request and answer, dry-run body, and promotion and rollback messages per the P7 A2.7 readings, before the wave 2 contract freeze. |
| CDC-13228 | RWB-P8-E4044-CON | GAP-2518 | 4 | Publish the case read (GET /cases/{caseId} or account-scoped) on rwb-case and the rule-package read with its package code on rwb-decision; enumerate the MatchRequest elements on API-P8-002. |
| CDC-13276 | RWB-P8-E4046-APP | GAP-0673 | 1 | Mark FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 INT-03 superseded for legacy key RWB-E4-046, with date and decision; load the ALS booking interface_config row per environment as one versioned row. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13237 | RWB-P8-E4045-APP | CG-ALL-7674 | find it | Remove the fixed enum on matchedTo so LOV-MATCH values are accepted as data without a code change. |
| CDC-13238 | RWB-P8-E4045-APP | CG-ALL-7675 | find it | Remove the fixed enum on source so LOV-PROCEEDS-SRC values are accepted as data without a code change. |
| CDC-13242 | RWB-P8-E4045-APP | DOR-RWB-P8-E4045-APP-8 | Header | Add base paths /api/recovery/case/v1 and /api/recovery/partner/v1; make matchedTo and source LOV-driven rather than closed enums; apply the 2 further detcheck items. |
| CDC-13283 | RWB-P8-E4047-APP | CG-ALL-7706 | 1 | Remove the fixed enum on matchedTo and validate it against the LOV-MATCH values in Reference Data v5 Lists, as data. |
| CDC-13284 | RWB-P8-E4047-APP | CG-ALL-7707 | 1 | Remove the fixed enum on source and validate it against the LOV-PROCEEDS-SRC values in Reference Data v5 Lists, as data. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13060 | RWB-P8-E2027-APP | GAP-1626 | find it | Slide 17 and slide 41 to name GET /proceeds and POST /proceeds/{proceedsId}/match per API Specification v4 in place of the older paths. |
| CDC-13122 | RWB-P8-E2027-OPS | GAP-1626 |  | On slides 17 and 41 use the API Specification v4 pair GET /proceeds and POST /proceeds/{proceedsId}/match for the rwb-payment receipt list and manual match. |
| CDC-13252 | RWB-P8-E4045-APP | GAP-0431 | 4 | Name the owner and store of the fee and schedule tables, the fee operation and field names in rwb-payment, the v_ace_payment product code and the wave 3 harness pack. |

### OTHER:Platform secret-store catalogue (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13080 | RWB-P8-E2027-APP | GAP-1362 | find it | Record names of per-service login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity; chart refers to them by role. |
| CDC-13108 | RWB-P8-E2027-CON | GAP-1362 | 12 | Record the names of the rwb-payment login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity; the story references them by role. |
| CDC-13143 | RWB-P8-E2027-OPS | GAP-1362 |  | Record names of the rwb-payment Kafka client credential, Temporal mTLS material, registry certificate, database login and workload identity; reference by role in the chart |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13089 | RWB-P8-E2027-CON | DOR-RWB-P8-E2027-CON-11 | 11 | Identify each field it classes as personal data that section 11 and BR12 say is not carried, and correct the classification or record the field as out of scope of this contract. |
| CDC-13159 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-11 | 16 | Reconcile the personal-data class of the fields this story carries with its statement that no person data reaches the outputs (BR11, TC-E4-043-07). |
| CDC-13310 | RWB-P8-E4048-APP | CG-ALL-7719 | 12.3 | Record ce_source as the CloudEvents 1.0 source header attribute of topic rwb.payment.events.v1, held by this service's event contract. |

### RWB-P8-E4043-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13153 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-21 | header | Complete the contract story build so its status moves from Not started to Done, and publish the contract. |
| CDC-13154 | RWB-P8-E4043-APP | DOR-RWB-P8-E4043-APP-22 | header | Publish a contract fake library version for RWB-P8-E4043-CON and record its version. |
| CDC-13287 | RWB-P8-E4047-APP | DOR-RWB-P8-E4047-APP-22 | 1 | Publish the contract fake library and record its version, so item 22 can be confirmed. |

### RWB-PLT-E1027-CON; RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13241 | RWB-P8-E4045-APP | DOR-RWB-P8-E4045-APP-21 | find it | Reach Done with their contracts published, as this story depends on them for build. |
| CDC-13265 | RWB-P8-E4046-APP | DOR-RWB-P8-E4046-APP-21 | Header | Publish the contract these stories depend on and set both stories to Done before RWB-P8-E4046-APP starts. |
| CDC-13286 | RWB-P8-E4047-APP | DOR-RWB-P8-E4047-APP-21 | Metadata | Set RWB-PLT-E1027-CON and RWB-PLT-N001-CON to Done so the Depends on (build) row is satisfied |

### OTHER:03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P8 P (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13061 | RWB-P8-E2027-APP | GAP-1631 | find it | Replace the ALS, GL, ATS and AMIS integration points with ALS read through the rwb-source-data contract, ledger postings out through rwb-integration; auto-debit and LED routes outside the 19 services until an interface is named. |
| CDC-13094 | RWB-P8-E2027-CON | GAP-1631 |  | Route the ALS read through rwb-source-data and ledger postings out through rwb-integration; keep the auto-debit and LED routes outside the 19 services until an interface is named. |

### RWB-P7-E2027-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13062 | RWB-P8-E2027-APP | GAP-1292 |  | Reconcile PM-2026.12 (valid from 2026-12-01) and PMT-2026.12 (valid from 2026-12-15) into one PAYMENT_MATCH version row under the R7.3 fill order before SIT. |
| CDC-13063 | RWB-P8-E2027-APP | GAP-1297 |  | Raise one reconciliation so the PAYMENT_MATCH package code holds one version row: PMT-2026.12 from 2026-12-15 against PM-2026.12 from 2026-12-01. |

### OTHER:TSD P4 T-A.1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13065 | RWB-P8-E2027-APP | GAP-2313 |  | Correct the six rule-package and rule-version endpoints to P7 ownership, with P4 keeping the loader and approver rights, at the next version. |
| CDC-13096 | RWB-P8-E2027-CON | GAP-2313 | 12 | Change the six rule-package and rule-version endpoints in T-A.1 from P4 to P7 (RWB-P7-E2027-APP, RWB-P7-E2042-APP); P4 keeps the loader and approver rights. |

### OTHER:Temporal and Drools Design (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13075 | RWB-P8-E2027-APP | GAP-2706 |  | Name the package code holding the RES rule set, state whether rwb-treatment evaluates R-RES-25 to R-RES-31, and name the parameter keys CURE_PERIOD_DAYS and restructure.max_breaks. |
| CDC-13323 | RWB-P8-E4048-APP | GAP-1382 | 8 | Name the rental collection workflow as a local baseline choice and read the arrears threshold from the package version in force announced on RulePackageInForce until rwb-decision names the package code |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13079 | RWB-P8-E2027-APP | GAP-1358 | find it | Declare DecisionRecorded read-only for ledger acknowledgement; register no second writer; confirm consumer list with event catalogue owner. |
| CDC-13142 | RWB-P8-E2027-OPS | GAP-1358 |  | Confirm consumer list with event catalogue owner; declare DecisionRecorded read-only for ledger acknowledgement in rwb-payment, no second writer |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13106 | RWB-P8-E2027-CON | GAP-1291 | 13 | Record the DP-added H contracts (RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) and C contracts (RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON) as non-blocking, built against fakes. |
| CDC-13137 | RWB-P8-E2027-OPS | GAP-1291 | find it | Record the DP-added H and C contracts (DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15, DP-19) as non-blocking platform and published contracts built against fakes; keep the metadata rows as given. |

### RWB-P4-E2027-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13145 | RWB-P8-E2027-OPS | GAP-2314 | section 7 | The gap concerns the P4 slice. No legacy criterion is added to this deployment story. |
| CDC-13146 | RWB-P8-E2027-OPS | GAP-2312 | 13 | Section 13 keeps the DP-added platform and rwb-case contracts as build-against dependencies outside the metadata rows; wave 2 planning gate confirms no H chain is missing. |

### RWB-P8-E4043-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13183 | RWB-P8-E4043-CON | DOR-RWB-P8-E4043-CON-10 | 9, 10 | Add empty, loading, error and no-access states for SCR-28 Proceeds matching |
| CDC-13186 | RWB-P8-E4043-CON | GAP-1363 | find it | Keep legacy AC1 and AC2 word for word with the origin tag, fill settlement detail from FSD P8 A2.3 and TSD P8, and cite FEAT-PAY-03 with AC-P8-003-01. |

### RWB-P8-E4044-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13199 | RWB-P8-E4044-APP | DOR-RWB-P8-E4044-APP-21 | Header | Complete the contract build so its status is Done and the contract is published. |
| CDC-13200 | RWB-P8-E4044-APP | DOR-RWB-P8-E4044-APP-22 | Header | Publish a contract fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13205 | RWB-P8-E4044-APP | CG-ALL-7645 | 12.5 | Add the matching activity (name Not specified in the source documents (GAP-2520; ASM-4170)), task queue rwb-payment, with its In and Out, to the Activities sheet. |
| CDC-13246 | RWB-P8-E4045-APP | CG-ALL-7677 | 12.5 | Add an activity row for the calculation activity, name Not specified in the source documents (GAP-2546; ASM-4205), on task queue rwb-payment. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13216 | RWB-P8-E4044-CON | CG-ALL-7661 | 12.5 | Add a row for the JOB-07 payment-matching workflow (name Not specified in the source documents (GAP-2520; ASM-4170)) so the story can cite a catalogued workflow. |
| CDC-13239 | RWB-P8-E4045-APP | CG-ALL-7676 | 12.5 | Add a row for the fee-calculation run workflow on task queue rwb-payment in namespace rwb-recovery, with the name given by GAP-2546. |

### OTHER:TSD P8 v2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13256 | RWB-P8-E4045-APP | GAP-2545 | 4 | Publish a fee operation or a FeeCalculated event on rwb.payment.events.v1 with its envelope and key, and add the ownership row. |
| CDC-13279 | RWB-P8-E4046-APP | GAP-2548 | 12.2 | Allocate a service contract baseline for this key publishing rwb.payment.TreatmentBooked.v1 (BACKWARD), the deliverFile manifest element set with booking branch, error envelope and fakes; publish ALS row values and the data product code in appendix T-A. |

### OTHER:Work package plan (WP JSON) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13320 | RWB-P8-E4048-APP | GAP-2524 | 4 | Add class C rows for the rental read of rwb-treatment, the receipt read of rwb-source-data, the case answer of rwb-case and the package read of rwb-decision; name the rental match rule code. |
| CDC-13322 | RWB-P8-E4048-APP | GAP-1379 | 4 | Add a class C dependency row for the rwb-treatment rental read and build it against its fake; settle the rental-terms field names with the rwb-treatment owner. |

### OTHER:rwb-decision API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13055 | RWB-P8-E2027-APP | DOR-RWB-P8-E2027-APP-8 | 4 | Publish GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions and GET /api/recovery/decision/v1/rule-models/{packageCode}/{version}. Payload gaps are resolved under CG-ALL-7568 to 7570. |

### OTHER:owning story of rwb-comms package assignment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13059 | RWB-P8-E2027-APP | GAP-2395 | find it | Package assignment belongs to its owning story; no change in this story. |

### OTHER:RWB-E2-027 build notes step 1 and RWB-E2-042 schema check (legacy, folder 21, read-only) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13064 | RWB-P8-E2027-APP | GAP-3179 | find it | Drop the payment_match_rule table from every service schema; keep the PAYMENT_MATCH rule package as the only home of the rows; load them through the rule package endpoints. |

### OTHER:Chart values files of the rwb-payment deployment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13071 | RWB-P8-E2027-APP | GAP-1361 | 13 | Expose each numeric operations value (alert thresholds, cache staleness, outbox lag, dead-letter limits, pool sizes, canary percentage, probe timings) as a placeholder chart value; close with DL11 before UAT. |

### OTHER:Platform secret-store catalogue and rwb-payment values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13073 | RWB-P8-E2027-APP | GAP-2508 | 13 | Reference each secret, identity and certificate by role and record names in the secret-store catalogue, keeping the rwb-payment login (DP-02); expose numeric values as chart placeholders. |

### OTHER:FSD P8 v3 and TSD P8 v2 (T8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13076 | RWB-P8-E2027-APP | GAP-1624 |  | Fill the FSD P8 Requirements served table with REQ IDs and the TSD P8 T8 traceability table with trace rows, or state that P8 has no requirement ID of its own. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13077 | RWB-P8-E2027-APP | GAP-0218 | find it | Holder rwb-decision, reader rwb-payment; codes carried as match type column of PAYMENT_MATCH; package version recorded in decision log; payment_match_rule use removed. |

### OTHER:rwb-decision rule_row catalogue and evaluation result (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13078 | RWB-P8-E2027-APP | GAP-1356 | find it | rwb-decision to publish one name in the rule_row catalogue and evaluation result (outside this story). |

### OTHER:Build notes RWB-E2-027 step 1 and Template and Rules R3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13081 | RWB-P8-E2027-APP | GAP-3188 | find it | One load path for rule packages in rwb-decision; P4 reference load endpoint used only for reference data that is not a rule package. |

### OTHER:FSD P6 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13092 | RWB-P8-E2027-CON | GAP-2395 | 8 | Name which of RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 the rwb-comms notice reads, and the package code; the TSD P6 v2 T2 row and Ownership Map v1 P6 rows follow. |

### OTHER:Functional Specification P8 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13093 | RWB-P8-E2027-CON | GAP-1625 |  | Replace placeholder rows AC-P8-003-01 to AC-P8-011-01 (A2.3.4.1 to A2.11.4.1) with testable main-flow criteria, using the feature statement, business rules and field list. |

### OTHER:RWB-E2-042 story and legacy key (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13095 | RWB-P8-E2027-CON | GAP-1292 |  | Reconcile PM-2026.12 (valid from 2026-12-01) and PMT-2026.12 (valid from 2026-12-15) into one PAYMENT_MATCH version row before SIT promotion. |

### OTHER:D1 workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13100 | RWB-P8-E2027-CON | GAP-1355 | 12 | Add C RWB-P7-E1073-CON to the C row of RWB-P8-E2027-APP. |

### OTHER:Matching service values files (three) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13101 | RWB-P8-E2027-CON | GAP-1361 | 12 | Expose each numeric operations value as a placeholder chart value and close them with the DL11 decisions before UAT. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13102 | RWB-P8-E2027-CON | GAP-1628 | 8 | Add versioned keys for the payment_match tolerance, window before and after, grace days, partial floor and priority, read through the rwb-case contract. |

### OTHER:Platform values files and secret-store catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13103 | RWB-P8-E2027-CON | GAP-2508 | 13 | Expose each numeric operations value as a chart value in the three values files; close DL11 before UAT; record names of per-service login, Kafka client credential, Temporal mTLS, registry certificate and workload identity in the secret-store catalogue. |

### OTHER:rwb-decision package register and rwb-case parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13104 | RWB-P8-E2027-CON | GAP-2706 | 9 | Name the package holding the RES rule set and the parameter keys CURE_PERIOD_DAYS and restructure.max_breaks; rwb-treatment evaluates the RES set with the package in force from rwb-decision. |

### OTHER:rwb-treatment contract (RESTRUCTURE rows) and rwb-decision package register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13105 | RWB-P8-E2027-CON | GAP-1881 | 9 | Keep PAYMENT_MATCH with rwb-decision and rwb-payment; rwb-treatment evaluates the RESTRUCTURE version in force for the plan breach and publishes rwb.treatment.TreatmentClosed.v1 once per breached plan. |

### RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13107 | RWB-P8-E2027-CON | GAP-1357 | not in chunk | Reconcile the PMT-2026.12 label to the single version PM-2026.12 in rwb-decision before SIT. |

### OTHER:Build notes RWB-E2-027 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13109 | RWB-P8-E2027-CON | GAP-3188 | 13 | Step 1: the load of rule packages goes through the rwb-decision endpoints; the P4 reference load endpoint is used only for reference data that is not a rule package. |

### OTHER:rwb-decision API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13117 | RWB-P8-E2027-OPS | DOR-RWB-P8-E2027-OPS-8 | 12 | Publish GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions and GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in rwb-decision API yaml; confirm event name rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; add the rule-cache refresh handler to Temporal Catalog v1 |

### RWB-P3-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13120 | RWB-P8-E2027-OPS | GAP-2395 |  | Use the three package codes and version labels as the fixture set, prove AC1 and AC5 on them; settle the rwb-comms package assignment with the rule registry owner before integration. No fourth code. |

### RWB-P8-E2027-CON; RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13124 | RWB-P8-E2027-OPS | GAP-2506 | 17 | Fix the evaluation-result field names, version-in-force read and installment-paid operation with owners; reconcile PMT-2026.12 to one version row before SIT. |

### OTHER:Recovery Workbench TSD P4; OTHER:T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13125 | RWB-P8-E2027-OPS | GAP-2313 |  | The story side already uses the P7 owner (see GAP-1293). The legacy P4 attribution belongs to the TSD. |

### OTHER:RWB ITG E2027 ITG integration story v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13127 | RWB-P8-E2027-OPS | GAP-0409 | 19 | Add the fixture business-date window, further version fixtures and evidence retention; confirm the ALS fixture contract, which is not in the workspace. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13128 | RWB-P8-E2027-OPS | GAP-1290 |  | Adopt ASM-B-P7-03-E2027-1; carry legacy s12 load and version-list shapes to the API spec; add approve, rollback, dry-run detail and governance decision code before wave 2 freeze. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13129 | RWB-P8-E2027-OPS | GAP-1293 | 12.2 | Set rule-package paths to P7 rwb-decision, /admin/rule-packages and /admin/rule-package-versions on /api/recovery/decision/v1; drop P4 and monolith base; /admin/rule-versions legacy, no target story. |

### RWB-P8-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13130 | RWB-P8-E2027-OPS | GAP-1355 | header | Add RWB-P7-E1073-CON to Contract dependencies (the C row); read AC6 through the rwb-decision contract mock, keeping every legacy step verbatim. |

### RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13131 | RWB-P8-E2027-OPS | GAP-1359 | 12 | Confirm the result packageCode, versionInForce, ruleId, rowOrder, outputs, and name the version-in-force lookup and treatment installment-paid operations, now placeholders. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13138 | RWB-P8-E2027-OPS | GAP-1639 |  | Register matchPayments and confirmBookings as named event-started workflows on task queue rwb-payment, or confirm the activity as the unit |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13139 | RWB-P8-E2027-OPS | GAP-1357 |  | Reconcile PMT-2026.12 to PM-2026.12 as the single version row in force for PAYMENT_MATCH before SIT |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:Lists sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13140 | RWB-P8-E2027-OPS | GAP-0218 |  | Record rwb-decision (P7) as holder and rwb-payment (P8) as reader of LOV-MATCH-TYPE, codes as match type column of PAYMENT_MATCH; copy Values rows unchanged |

### OTHER:rwb-decision rule_row catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13141 | RWB-P8-E2027-OPS | GAP-1356 |  | Publish row order as the single column name in the rule_row catalogue and evaluation result; record priority as legacy and TSD name |

### RWB-P4-E2027-APP; OTHER:security administrator confirmation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13144 | RWB-P8-E2027-OPS | GAP-2311 |  | SY-AGENT letters and login name stay open pending security administrator confirmation before wave 2 sign-off. |

### OTHER:Rule registry (PAYMENT_MATCH package); 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13164 | RWB-P8-E4043-APP | GAP-2511 | 4 | Publish the settlement arm package code, rule IDs, tolerance, window and grace; name the three consumed operations; rwb-case to publish the money-side answer and outcome code. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13166 | RWB-P8-E4043-APP | GAP-2515 | 4 | Publish field lists for rwb.payment.TreatmentBooked.v1 and rwb.payment.ProceedsMatched.v1, keyed by case id, with BACKWARD registry mode. |

### OTHER:Split plan (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13167 | RWB-P8-E4043-APP | GAP-2513 | header | Add the RWB-P1 source-data, RWB-P3 case, RWB-S2 treatment and RWB-P7 decision contract stories to the C list of lane L-P8-F; keep R5.7 unchanged. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13168 | RWB-P8-E4043-APP | GAP-2516 | 8 | Register R-SET-14 as the settlement money-side transition; publish the PAYMENT_MATCH package code and tolerance, window and partial rule IDs with values; retire payment_match_rule from the TSD data model. |

### OTHER:Recovery Workbench TSD P8 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13185 | RWB-P8-E4043-CON | GAP-2548 | find it | Publish in appendix T-A the ALS interface id, transport, layout and result codes and the data product code; publish the deliverFile(manifest) element set and the TreatmentBooked field list (GAP-2548). |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; OTHER:FSD P8 v3 Requirements served table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13187 | RWB-P8-E4043-CON | GAP-2510 | 16 | Carry the settlement data set (case, settlement treatment, receipt on business date, amount to SETTLEMENT) into the four legacy test case rows; add the FEAT-PAY-03 requirement row to FSD P8. |

### OTHER:Rule registry (PAYMENT_MATCH settlement arm); API:(service not named); 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13188 | RWB-P8-E4043-CON | GAP-2511 | 4 | Publish the settlement arm package code, rule IDs, tolerance, window and grace; name the three consumed operations; rwb-case publishes the money-side answer and outcome code. |

### OTHER:FSD P8 v3 A2.3.3.1 Data table and the DP-05 row of the pattern table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13189 | RWB-P8-E4043-CON | GAP-2512 | 4 | Retire the v_ace_payment and v_ace_batch_status reads of rwb-payment; only rwb-source-data reads the ACE views, with its freshness stamp. |

### OTHER:TSD P8 v2 appendix T-A; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13190 | RWB-P8-E4043-CON | GAP-2514 | 4 | Publish MatchRequest (case reference, treatment reference, account payment reference, amount, received date, match value) and ProceedsPage (page, size, total). |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:AsyncAPI document of rwb-payment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13191 | RWB-P8-E4043-CON | GAP-2515 | 4 | Publish field lists of rwb.payment.TreatmentBooked.v1 and rwb.payment.ProceedsMatched.v1 keyed by caseId, with identifiers, amounts, dates, list values and rule version only; registry in BACKWARD mode. |

### OTHER:Split plan for lane L-P8-F (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13193 | RWB-P8-E4043-CON | GAP-2513 | header | Add the four consumed rows (RWB-P1, RWB-P3, RWB-S2, RWB-P7 contract stories) to the C list of this slice; keep R5.7 unchanged. |

### OTHER:TSD P8 v2 and the rule registry (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13194 | RWB-P8-E4043-CON | GAP-2516 | 8 | Record R-SET-14 as the settlement money-side transition; publish the PAYMENT_MATCH package code and its rule IDs with values; retire payment_match_rule from the TSD data model. |

### OTHER:Rental-profile contract story of the same service (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13195 | RWB-P8-E4043-CON | GAP-2527 | 12 | Declare only the rental members, rental constraints and fakes as additive; do not redeclare the GET /proceeds and POST match operations, or the three event schemas held in this story. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13201 | RWB-P8-E4044-APP | DOR-RWB-P8-E4044-APP-8 | 12.2, 12.3, 12.5 | Close CG-ALL-7641 and CG-ALL-7642 (yaml REST bases) and CG-ALL-7644 (workflow row). CG-ALL-7643 topic is fixed in 12.3. |

### OTHER:FSD P8 v3, 'Requirements served' table (A2.4.4.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13209 | RWB-P8-E4044-APP | GAP-2517 | 7 | Add the requirement row of FEAT-PAY-04 to the 'Requirements served' table in the next version. AC1 Given now carries the proceeds data set; section 16 test rows still need the data column. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:API-P8-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13210 | RWB-P8-E4044-APP | GAP-2518 | 4 | Publish the rwb-case case read and the rwb-decision rule-package read with package code; enumerate MatchRequest elements on API-P8-002. Story step 3 and 4 placeholders stay until then. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13213 | RWB-P8-E4044-APP | GAP-2521 | 9 | State whether account_payment_id carries the ACE payment code of v_ace_payment only; remove the account_payment relationship from TSD P8 T3.3 in its next version if no object is intended. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13218 | RWB-P8-E4044-CON | DOR-RWB-P8-E4044-CON-8 | 1, 12.3 | Add the /api/recovery/case/v1 and /api/recovery/decision/v1 bases to the API yaml; place rwb.payment.TreatmentBooked.v1 and rwb.payment.PaymentMissed.v1 on the .retry and .dlt topics in the catalog |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13226 | RWB-P8-E4044-CON | GAP-1370 | header | Contract dependencies row lists four services; the fifth class C dependency is not identified in the sources. |

### OTHER:FSD P8 v3 (Requirements served table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13227 | RWB-P8-E4044-CON | GAP-2517 | 16 | Add the requirement row of FEAT-PAY-04 to the Requirements served table in the next FSD P8 version. Story test rows TC-E4-044-01 and -02 need the proceeds data set in section 16, which is outside this chunk. |

### RWB-S4-E5022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13231 | RWB-P8-E4044-CON | GAP-1891 | Header | Add RWB-P8-E4044-CON, RWB-P8-E4049-CON and the rwb-case case-move answer to the C list once the solution architect confirms the owner contracts; record the wave 3 legacy-to-P8 operation mapping. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:TSD P8 T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13233 | RWB-P8-E4044-CON | GAP-2521 | find it | State that account_payment_id carries the ACE payment code of v_ace_payment only; remove the account_payment relationship from TSD P8 T3.3 in its next version if no object is intended. |

### OTHER:Wave 3 entry check agreement (integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13251 | RWB-P8-E4045-APP | GAP-0436 | none | Agree the harness environment, seeded set, business date, product codes, evidence format and gate thresholds; settle the three unnamed operations. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13254 | RWB-P8-E4045-APP | GAP-2543 | 4 | Name the fee table owner, publish the read returning a fee row with its version, and state in TSD P8 T3.1 whether fee rows are stored in rwb_payment. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13263 | RWB-P8-E4046-APP | CG-ALL-7692 | 12.5 | Add a row for SettlementBookingWorkflow: task queue rwb-payment, namespace rwb-recovery, event-started by TreatmentApproved; or the story adopts the catalogued workflow name. |

### OTHER:Split plan (work package, lane L-P8-I C list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13280 | RWB-P8-E4046-APP | GAP-2550 | 12.2 | Add the five consumed rows to the C list of this slice in the next split-plan version: RWB-S2 treatment, RWB-P1 source-data, RWB-P2 integration (incl. deliverFile), RWB-P3 case; keep R5.7 Day-1 rule. |

### OTHER:Settlement route set (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13282 | RWB-P8-E4046-APP | GAP-2552 | 8; 5 | Fix booking actor as rwb-payment booking step after TreatmentApproved; add settlement counterpart of R-RES-23 with its state, message and owner role. |

### RWB-P8-E4043-CON; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13288 | RWB-P8-E4047-APP | DOR-RWB-P8-E4047-APP-8 | header | Add message IDs for 400, 401, 404 and 503 to the error set; add activity confirmBookings (JOB-08) to Temporal Catalog v1; fix the two enums via CG-ALL-7706 and CG-ALL-7707. |

### OTHER:P1 contract epic (rwb-source-data posting-reference read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13296 | RWB-P8-E4047-APP | GAP-2555 | 11 | Publish the posting-reference read with payment code, business date, reference and batch status; confirm the DF-FIN-009 mapping with the solution architect. |

### OTHER:rwb-integration interface configuration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13297 | RWB-P8-E4047-APP | GAP-2557 | 4 | Load the GL (INT-16) and ALS (INT-03) interface rows with interface identifier, transport, layout, result codes, retry intervals and message text; keep MSG-P2-001 wording in the message standard. |

### RWB-P8-E4047-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13298 | RWB-P8-E4047-APP | GAP-2560 | 4 | Add C rows for the rwb-source-data posting-reference read and the rwb-decision rule-in-force read in place of C []. |

### RWB-ITG-E4047-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13300 | RWB-P8-E4047-APP | GAP-2558 |  | Read receipts through GET /proceeds with its case filter in place of cases/{caseId}/payments, the operation rwb-payment declares. |

### RWB-P8-E4048-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13306 | RWB-P8-E4048-APP | DOR-RWB-P8-E4048-APP-21 | 14 | Move build status from Not started to Done once the contract is published. |

### OTHER:NPA and asset manager (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13318 | RWB-P8-E4048-APP | GAP-1378 | 11 | Amount, debit day and arrears threshold read from rwb-treatment and reference data; value set confirmation by NPA and asset manager is pending before wave 3. |

### OTHER:S2 contract epic (rwb-treatment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13319 | RWB-P8-E4048-APP | GAP-2523 | 4 | Publish the rental read with the rental reference, the treatment reference, the case reference, the rental amount, the debit day and the due date. |

### OTHER:AsyncAPI fragment of the payment profile (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13321 | RWB-P8-E4048-APP | GAP-2526 | 4 | Publish the PaymentMissed and ProceedsMatched payloads with the rental reference, business date, debit day and rule identity fields, and register them in BACKWARD mode. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0218 | LOV-MATCH-TYPE is used by payment_match_rule, a table the target drops and the Ownership Map does not carry | Center of excellence | Resolved (directive) |
| GAP-0260 | payment_match_rule is in the inventory but not in the Ownership Map, and D-RCV-36 retires it as a table | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0409 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0431 | The fee tables, the fee operation and the wave 3 harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0432 | ALS interface, booking operation and wave 3 harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0433 | The general ledger interface, the posting reference, the entry set per route and the wave 3 harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1290 | PAYMENT_MATCH registry governance: shapes, decision-record payload, message set and promotion and rollback semantics are not specified | Solution architect, with the P7 business analyst and the rule owner RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1293 | The rule-package operations: the legacy P4 attribution and the /admin/rule-versions paths against P7 and /admin/rule-package-versions | P7 solution architect, with the API specification owner | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1355 | The AC6 package load and the rule-evaluation contract have no C row in this key | Solution architect | Resolved (directive) |
| GAP-1356 | The ordering column is called row order in the story and priority in the TSD | Data steward | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1358 | DecisionRecorded is listed as consumed here but the catalogue names only two consumers | Integration architect | Resolved (directive) |
| GAP-1359 | The rule-evaluation result has no published schema and two of its field names are not given | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1360 | The three payment event payloads have no schema in any source | Integration architect | Resolved (directive) |
| GAP-1361 | No numeric operations value is specified for the matching service | DevOps engineer | Resolved (directive) |
| GAP-1362 | The secret names, the workload identity and the certificate of rwb-payment are not specified | Identity and access team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1363 | Legacy RWB-E4-043 acceptance criteria and test cases are generic placeholders | Business analyst | Resolved (directive) |
| GAP-1364 | Settlement match outcomes, rule package code, thresholds and money-side close state have no source value | Solution architect | Resolved (directive) |
| GAP-1365 | The legacy step reads v_ace_payment and four other modules tables in process | Solution architect | Resolved (directive) |
| GAP-1366 | The field lists of MatchRequest, ProceedsPage and the remaining Proceeds answer are not specified | Solution architect | Resolved (directive) |
| GAP-1367 | The payloads of TreatmentBooked and ProceedsMatched are not published | Solution architect | Resolved (directive) |
| GAP-1368 | No rule row, package code or rule ID exists for the settlement arm of the match | Solution architect | Resolved (directive) |
| GAP-1369 | Legacy acceptance criteria and test cases of RWB-E4-044 are generic placeholders | Business analyst | Resolved (directive) |
| GAP-1370 | Contract dependencies row is None while the match reads five other services | Tech lead | Resolved (directive) |
| GAP-1371 | The elements of MatchRequest are not published | Tech lead | Resolved (directive) |
| GAP-1372 | The legacy word a broker has no value in LOV-PROCEEDS-SRC | Business analyst | Resolved (directive) |
| GAP-1373 | payment_match_rule is defined in the TSD P8 data model but has no owner in the Ownership Map | Data architect | Resolved (directive) |
| GAP-1374 | The name of the JOB-07 event-started workflow is not published | Tech lead | Accepted (directive); not applied: value not in the source documents |
| GAP-1375 | The split plan carries no requirement id for this slice | Business analyst | Resolved (directive) |
| GAP-1376 | The payload elements of the three payment events are not published | Tech lead | Resolved (directive) |
| GAP-1377 | The acceptance criteria and test cases of RWB-E4-048 are generic placeholders that name no rental value | Business analyst | Resolved (directive) |
| GAP-1378 | No source gives the rental amount, the debit day or the arrears threshold of the deed in lieu rental | NPA and asset manager | Resolved (directive) |
| GAP-1379 | The rental terms arrive through the rwb-treatment contract, which the plan does not carry as a contract dependency, and the field list of that answer is not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1380 | The test cases of RWB-E4-048 are generic placeholders and name no contract element | QA lead | Resolved (directive) |
| GAP-1381 | No source gives a rental-specific property or a separate receipt and arrears operation, and the consumed rental-terms element has no field list | Solution architect | Resolved (directive) |
| GAP-1382 | The name of the rental collection workflow and the package code that decides the arrears threshold are not specified | Solution architect | Resolved (directive) |
| GAP-1624 | FSD P8 issues no requirement ID, so the product requirement cannot be traced to an FSD requirement | Business analyst, P8 | Resolved (directive) |
| GAP-1625 | Eight of the eleven P8 features carry a placeholder acceptance criterion instead of a testable one | Business analyst, P8 | Resolved (directive) |
| GAP-1626 | The two operations named in Architecture v5 slide 17 are not the two operations in the API Specification and the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1628 | The matching values have no table and no owner after payment_match_rule was retired | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1880 | The treatment-side matching read, the shortfall columns, the breach decision code and the plan-check cadence are not specified | Solution architect with the rwb-treatment and rwb-payment squads | Resolved (directive) |
| GAP-1881 | PAYMENT_MATCH is the rwb-payment matching package while this slice evaluates it for the plan breach on the treatment side | Solution architect with rwb-decision, rwb-payment and rwb-treatment | Resolved (directive) |
| GAP-1891 | The target gives the matching, the proceeds and the balance application to rwb-payment while the legacy story gives them to S4, and the plan adds no contract dependency for them | Solution architect | Resolved (directive) |
| GAP-1892 | ProceedsMatched does not list rwb-litigation as a consumer, so the payment fact cannot arrive as an event | Solution architect | Resolved (directive) |
| GAP-1896 | The LED round result, the percentage of official value, the proceeds source code and three operation names have no field or name in any source | Solution architect | Resolved (directive) |
| GAP-2311 | Values of the payment-matching access profile that the legacy story does not state | Business analyst, P4 | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2313 | The rule-package endpoints are P4 in the legacy contract and P7 in Arch v5 | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2314 | No legacy acceptance criterion of RWB-E2-027 belongs to the P4 slice | Business analyst, P4 | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2507 | The consumed rule-evaluation result, the treatment installment-paid call, the three event payloads and the shared record's consumer list have no published schema or operation name | Solution architect, with the owners of rwb-decision, rwb-treatment and the event catalogue | Resolved (directive) |
| GAP-2508 | No numeric operations value and no name of a secret, identity or certificate is specified for the matching deployment | DevOps engineer, with the platform administrator and the identity and access team | Resolved (directive) |
| GAP-2510 | The legacy criterion of RWB-E4-043 names no settlement, its test cases carry no settlement data, and the story master gives no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2511 | The settlement match has no published package code, rule IDs, tolerance, window or outcome fields, and the consumed reads have no published operation names | P7 rule owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2512 | The legacy story reads v_ace_payment and v_ace_batch_status in process while the target gives the ACE views to rwb-source-data alone | P1 source-data owner and the P8 solution architect | Resolved (directive) |
| GAP-2513 | The work package gives the contract-dependency row as None while the story consumes four contracts, and it still starts on Day 1 | P8 solution architect and the split-plan owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2514 | TSD P8 names MatchRequest and ProceedsPage without a field list, so the request and the page have to be derived | P8 solution architect and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2515 | The payloads of TreatmentBooked and ProceedsMatched are not published, while PaymentMissed is | P8 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2516 | The settlement money side is rule R-SET-14, but the matching mechanism has no package code and no rule IDs, and payment_match_rule is replaced | P7 rule owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2517 | The legacy criteria of RWB-E4-044 are generic, carry no proceeds data and the split plan gives the slice no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2518 | The consumed case and rule-package reads have no published operation names and the MatchRequest elements are not enumerated | P3 case owner, P7 rule owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2519 | No match package code, rule ID, tolerance, window, grace or priority is published for the auction, broker and LED proceeds, and payment_match_rule has no owner | P7 rule owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2520 | The JOB-07 workflow and the matching activity have no published names, and no source fixes the trigger or the schedule form of the run | P8 solution architect and the workflow platform owner (RWB-PLT-WF) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2521 | proceeds.account_payment_id points at an account_payment object that no owner of the ownership map declares | ACE DB owner (RWB-PLT-DB) and the P8 data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2522 | The wording of MSG-P8-001 and MSG-P8-002 is not in the read sources | Business analyst, P8 | Resolved (directive) |
| GAP-2523 | The rental read of rwb-treatment has no published operation name, path or field list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2524 | Four reads are consumed as class C while the plan's contract row is None, and the rental rule code is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2525 | FSD P8 A2.9 names ATS and AMIS while TSD P8 T5.1 names ALS and GL only | Solution architect | Resolved (directive) |
| GAP-2526 | The rental fields of the PaymentMissed and ProceedsMatched payloads are not published | Solution architect | Resolved (directive) |
| GAP-2527 | Two contract stories of one service declare the same base surface | Solution architect | Resolved (directive) |
| GAP-2528 | LOV-MATCH holds no value that names a rental | Business analyst, P8 | Resolved (directive) |
| GAP-2542 | The legacy criteria of RWB-E4-045 are generic, the split gives this slice only AC2, and the slice carries no requirement id | P8 business analyst and the Payment module owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2543 | The fee tables held as data have no owning service and no place in this schema, and the consumed reads that carry them are unpublished | P8 data owner, the P3 reference-data owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2544 | No fee type list, fee row value, rate, cap or fee-specific message is published, and rule_row is named by the legacy key but is not the source of the value | the reference-data owner (P3), the P7 rule owner and the P8 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2545 | The service owns no fee operation and no fee event, so the answer of the calculation has no published carrier | P8 solution architect and the service contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2546 | The fee run and its activity have no published names, and the trigger of the calculation is stated two different ways | P8 solution architect and the workflow platform owner (RWB-PLT-WF) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2547 | The legacy key leaves this slice one generic criterion, its four test cases carry no booking data, the FSD success criterion is a single line and the plan gives the slice no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2549 | The legacy story reads v_ace_account and v_ace_payment in process while the target gives the ACE views to rwb-source-data alone | P1 source-data owner and the P8 solution architect | Resolved (directive) |
| GAP-2550 | The work package gives the contract-dependency row as None while the story consumes four REST contracts and one activity contract, and it still starts on Day 1 | P8 solution architect and the split-plan owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2551 | The legacy key tracks the booking in outbound_item, a table this service owns in the monolith and rwb-integration owns in the target | P8 solution architect and the P2 integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2552 | No source says which service raises the booking call after the accepted treatment, and the settlement path has no rejection rule row of its own | P8 business analyst and the Settlement route set owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2554 | The trigger and the posting window of the feature are not stated for this service | Solution architect | Resolved (directive) |
| GAP-2555 | The field that carries the posting reference, and the read that serves it, are named in no contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2556 | The event catalogue holds no posting-result event, so a confirmed posting is announced nowhere | Solution architect | Resolved (directive) |
| GAP-2557 | The ledger interface values, its layout, its result codes and its retry schedule are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2558 | The integration story assigns a payments read to rwb-payment that its ownership rows do not hold | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2559 | The rejection of a posting is a route state for the debt sale and the write-off and has no stated owner for a settlement or a sale receipt | Business analyst, P8 | Resolved (directive) |
| GAP-2560 | Two consumed reads are class C in fact while the plan's contract row for the key is None | Solution architect | Resolved (directive) |
| GAP-2705 | The match consequence that rwb-treatment consumes is not published, and no source names the plan states the treatment row holds after a match | Contract owner of rwb-treatment with the owner of rwb-payment and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2706 | No source names the rule set, the parameter codes or the signal that announce a plan state change, and none states who consumes the plan consequence once rwb-treatment owns it | Solution architect with the rule owner of rwb-decision and the parameters owner of rwb-case | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3188 | The payment match rule load is a P4 reference load in the story and a P7 rule package in the target | Decision and rules lead with the access lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P8-E2027-APP | skipped AC ID | 135 | missing: AC1, AC2, AC3, AC4, AC5, AC8, AC9, AC15, AC16 |
| RWB-P8-E2027-OPS | date added | 1 | 2026-12-15 |
