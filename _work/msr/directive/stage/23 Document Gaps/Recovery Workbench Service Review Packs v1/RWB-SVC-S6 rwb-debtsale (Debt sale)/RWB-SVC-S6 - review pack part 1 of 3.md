# RWB-SVC-S6 rwb-debtsale (Debt sale) - review pack, part 1 of 3 (RWB-S6-E5023-APP to RWB-S6-E6004-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 14 |
| Resolved in the stories | 342 |
| Cross-document (pending in another document) | 253 |
| Not applied (value not in the sources) | 17 |
| Open business decisions | 34 |
| Register gaps linked | 64 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S6-E5023-APP | 42 | 13 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5023 APP Select eligible accounts for sale by rule v2.md |
| RWB-S6-E5023-CON | 24 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5023 CON Select eligible accounts for sale by rule - contract v2.md |
| RWB-S6-E5024-APP | 31 | 20 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5024 APP Build the lots and estimate the price v2.md |
| RWB-S6-E5024-CON | 24 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5024 CON Build the lots and estimate the price - contract v2.md |
| RWB-S6-E5025-APP | 24 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5025 APP Prepare the masked data tape v2.md |
| RWB-S6-E5026-APP | 26 | 24 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5026 APP Open the buyer data room v2.md |
| RWB-S6-E5026-CON | 18 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E5026 CON Open the buyer data room - contract v2.md |
| RWB-S6-E6001-APP | 31 | 19 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6001 APP Approve lots, reserve and tiered terms v2.md |
| RWB-S6-E6001-CON | 16 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6001 CON Approve lots, reserve and tiered terms - contract v2.md |
| RWB-S6-E6002-APP | 31 | 16 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6002 APP Qualify a buyer against KYC and licensing v2.md |
| RWB-S6-E6002-CON | 17 | 21 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6002 CON Qualify a buyer against KYC and licensing - contract v2.md |
| RWB-S6-E6003-APP | 24 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6003 APP Bar a buyer that fails qualification v2.md |
| RWB-S6-E6003-CON | 12 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6003 CON Bar a buyer that fails qualification - contract v2.md |
| RWB-S6-E6004-APP | 22 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6004 APP Take buyer bids v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S6-E5023-CON | R-02633 | CG-ALL-10339 | Script gap | Product owner | The story adds LOT_CANDIDATE_SELECTED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5023-CON | R-02634 | CG-ALL-10340 | Script gap | Product owner | The story adds LOT_BUILT to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5023-CON | R-02635 | CG-ALL-10341 | Script gap | Product owner | The story adds CASE_EXCLUDED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5023-CON | R-02636 | CG-ALL-10342 | Script gap | Product owner | The story adds BACK_TO_CASE_LIST to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5024-CON | R-02647 | CG-ALL-10373 | Script gap | Product owner | The story adds LOT_BUILT to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5024-CON | R-02648 | CG-ALL-10374 | Script gap | Product owner | The story adds LOT_TOO_THIN to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5024-CON | R-02649 | CG-ALL-10375 | Script gap | Product owner | The story adds LOT_PRICED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5025-APP | R-02655 | CG-ALL-10388 | Script gap | Product owner | The story adds LOT_APPROVED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5026-CON | R-02664 | CG-ALL-10417 | Script gap | Product owner | The story adds TAPE_PREPARED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5026-CON | R-02665 | CG-ALL-10418 | Script gap | Product owner | The story adds DATA_ROOM_OPEN to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6003-APP | R-02687 | CG-ALL-10482 | Script gap | Product owner | The story adds DATA_ROOM_OPEN to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6003-APP | R-02688 | CG-ALL-10483 | Script gap | Product owner | The story adds BUYER_PENDING_KYC to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6003-APP | R-02689 | CG-ALL-10484 | Script gap | Product owner | The story adds BUYER_REJECTED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6003-APP | R-02690 | CG-ALL-10485 | Script gap | Product owner | The story adds BACK_TO_CASE_LIST to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6004-APP | R-02703 | CG-ALL-10518 | Script gap | Product owner | The story adds BIDDING_OPEN to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6004-APP | R-02704 | CG-ALL-10519 | Script gap | Product owner | The story adds BIDS_RECEIVED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6004-APP | R-02705 | CG-ALL-10520 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6004-APP | R-02706 | CG-ALL-10521 | Script gap | Product owner | The story adds LOT_CLOSED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E5023-APP, RWB-S6-E5023-CON, RWB-S6-E6012-APP | R-09247 | GAP-1473 | Register gap | Head of Asset Liquidity | The debt sale cap is stated as a percentage with no basis, period or measurement | Hold the cap as a versioned policy parameter with its basis and period in the version label, compute headroom against the population the policy names, and report the version used with each lot. |
| RWB-S6-E5023-APP | R-13024 | CG-ALL-10334 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E5024-APP | R-13035 | CG-ALL-10368 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E5026-APP | R-13051 | CG-ALL-10414 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6001-APP | R-13058 | CG-ALL-10438 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6002-APP | R-13070 | CG-ALL-10465 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6003-APP | R-13084 | CG-ALL-10500 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6004-APP | R-13095 | CG-ALL-10533 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E5023-APP, RWB-S6-E5023-CON, RWB-S6-E6012-APP | R-23578 | GAP-1777 | Register gap | Head of Asset Liquidity | The debt sale cap has no basis and no period, only a figure | Hold the cap, its denominator and its period as one versioned reference-data row with the role that owns it, and record the version applied at the selection, the award and the headroom report. |
| RWB-S6-E5024-APP, RWB-S6-E5024-CON, RWB-S6-E6005-APP, RWB-S6-E6005-CON | R-23585 | GAP-1778 | Register gap | Risk with the product heads | The approval bands in the design and the delegation in the FSD are two different statements of who approves an award | Route the lot approval and the award through the P7 approval child on the delegation table of P4, hold the bands as versioned reference data with their valid-from date, and record the level applied and the approving role on the award; the free-text authority column then holds the level name, not a person. |
| RWB-S6-E5025-APP, RWB-S6-E6007-APP, RWB-S6-E6007-CON | R-23590 | GAP-1786 | Register gap | Compliance and PDPA officer | borrower_code and account_key are flagged not personal in the data model, yet they identify a customer on the tape | Treat borrower_code and account_key as personal data in use, mask both on every screen and on the tape and the transfer file by role, and correct the is_personal flag in the next version of the Logical Data Model and the physical schema. |
| RWB-S6-E6002-APP, RWB-S6-E6002-CON, RWB-S6-E6003-APP, RWB-S6-E6003-CON | R-23604 | GAP-1474 | Register gap | Compliance and PDPA officer | The buyer licensing and eligibility criteria and the authority that bars a buyer are not specified | Reuse the bank's existing KYC and licensing checks, hold the accepted licence types and their validity as reference data, and let the debt sale officer bar a buyer with Compliance confirming the reason. |
| RWB-S6-E6002-APP, RWB-S6-E6002-CON, RWB-S6-E6003-APP, RWB-S6-E6003-CON | R-23605 | GAP-1776 | Register gap | Compliance and PDPA officer | The buyer's KYC result, licence expiry and panel status have no owner and no source system | Hold the KYC result, the licence expiry and the panel status as data on the buyer record, read the panel through the S9 contract, and record the evidence the officer accepted; confirm the source of the KYC and licence facts with Compliance before wave 4. |
| RWB-S6-E6003-APP, RWB-S6-E6003-CON, RWB-S6-E6009-APP, RWB-S6-E6009-CON, RWB-S6-E6011-APP, RWB-S6-E6011-CON | R-23607 | GAP-1791 | Register gap | Head of Asset Liquidity | The put-back window, the remediation window and the settlement term are not stated and are business values | Hold the three windows as versioned reference-data rows with their valid-from dates, apply the value in force at the business date of the lot, and record the version applied on the claim and the settlement. |
| RWB-S6-E5023-APP, RWB-S6-E5023-CON, RWB-S6-E6005-APP, RWB-S6-E6005-CON | R-29212 | GAP-1485 | Register gap | Head of Asset Liquidity | The debt sale turnaround has a target and no baseline | Measure the current cycle on the first lot of the release and publish it as the baseline with the target of 45 days unchanged. |
| RWB-S6-E5025-APP, RWB-S6-E6007-APP, RWB-S6-E6007-CON | R-29220 | GAP-1790 | Register gap | Compliance and PDPA officer | Retention, classification and the masking rules a record is held under are open | Give every record a data classification and a retention class and hold the periods as reference data from DL26; apply the class to the tape and to the transfer file through P5 and P2, which own the document and the file. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S6-E5023-APP | R-08410 | DOR-RWB-S6-E5023-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. Grep of *.md found no sign-off record; matches were unrelated. Needs the epic design record. |
| RWB-S6-E5023-APP | R-20555 | DOR-RWB-S6-E5023-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR1-BR10 criteria and tests need section 7 and 16 text, which is not in the chunk. No edit made to avoid partial or invented mappings. |
| RWB-S6-E5023-APP | R-27499 | CG-ALL-10336 | 12.5 | Criteria and tests keep legacy job and decision-log wording | Section 12.5 has no legacy wording. The 3 remaining legacy lines are in section 7 or 16, which are not in the chunk. Rerun with them. |
| RWB-S6-E5024-APP | R-08423 | DOR-RWB-S6-E5024-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for EP05 or RWB-S6 found in sources; sign-off cannot be confirmed without inventing it. Story text not changed. |
| RWB-S6-E5024-APP | R-20567 | DOR-RWB-S6-E5024-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 text is not in this chunk, so no old text can be copied. Empty, loading, error and no-access values for SCR-25 are not in sources. |
| RWB-S6-E5024-APP | R-20568 | DOR-RWB-S6-E5024-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Fields to classify as personal data are not named in the story or sources. Classification cannot be applied without inventing them. |
| RWB-S6-E5024-APP | R-20577 | DOR-RWB-S6-E5024-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | Error and Message Standard v4 text for MSG-P1-001 not found in sources (grep across project, excluding 17). Section 14 wording cannot be changed without it. |
| RWB-S6-E5024-APP | R-27507 | CG-ALL-10366 | 4, 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | Error and Message Standard v4 text not found (DOR-RWB-S6-E5024-APP-9); the wording was reverted. |
| RWB-S6-E5024-CON | R-27513 | CG-ALL-10385 | 7; 16 | Criteria and tests keep legacy job and decision-log wording | The three flagged lines (AC2, AC3, TC-E5-024-01) are in sections 7 and 16, which are not in this chunk, so their exact text cannot be copied. Section 12.5 has no legacy wording. Resend those parts. |
| RWB-S6-E5026-APP | R-20595 | DOR-RWB-S6-E5026-APP-11 | not in this chunk | Definition of Ready item 11 Guardrails: Partial | Personal-data class of each field is not in the sources, and the no-personal-data sentence is outside this chunk. Not specified in the source documents (DOR-RWB-S6-E5026-APP-11). |
| RWB-S6-E5026-APP | R-20600 | DOR-RWB-S6-E5026-APP-4 | 8, 7 and 16 | Definition of Ready item 4 Business rules: Partial | BR11 to BR14 IDs are already mapped in the section 8 prose. BR1 to BR10 criteria and test rows sit in sections 7 and 16, outside this chunk, so no anchor text is available. |
| RWB-S6-E6001-APP | R-20612 | DOR-RWB-S6-E6001-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | Empty, loading, error and no-access state text for SCR-25 and SCR-26 is outside this chunk and was not found in the sources. Cannot be written without it. |
| RWB-S6-E6001-APP | R-20613 | DOR-RWB-S6-E6001-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The P2 field that detcheck flags as personal data is not named in this chunk. It cannot be classified without the field name. |
| RWB-S6-E6001-CON | R-02680 | CG-ALL-10446 | 12.5 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | No task queue edit is in the diff. The story still needs the catalog task queue value; the namespace text is kept. |
| RWB-S6-E6001-CON | R-23600 | GAP-1966 |  | RWB-S6-E6001: the award operation and the A right are rowed as this story's although the award belongs to RWB-S6-E6005-APP, and the committee approver of the FSD has no role row | The operation and A-right rows are in story sections not in this chunk (headings 8 to 19). No text was copied, so no edit was made. Re-send those sections to apply. |
| RWB-S6-E6002-APP | R-08464 | DOR-RWB-S6-E6002-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for EP06 in the sources. Grep for 'epic design' and EP06 sign-off found only process and cadence rows. Sign-off not invented. |
| RWB-S6-E6002-APP | R-20627 | DOR-RWB-S6-E6002-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-26 empty, loading, error and no-access states sit in a story part not in this chunk, so they cannot be placed here. Needs that part. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (53)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18363 | RWB-S6-E5023-APP | CG-ALL-10322 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /cases family (read) of P3 rwb-case. |
| CDC-18364 | RWB-S6-E5023-APP | CG-ALL-10323 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the COLLINS score read of P1 rwb-source-data. |
| CDC-18365 | RWB-S6-E5023-APP | CG-ALL-10324 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package read of P7 rwb-decision. |
| CDC-18367 | RWB-S6-E5023-APP | DOR-RWB-S6-E5023-APP-8 | Header | Add base paths /api/recovery/case/v1, /api/recovery/source-data/v1 and /api/recovery/decision/v1; align rwb-debtsale.yaml buyerClass enum with LOV-BUYER-CLASS; resolve the five further detcheck rows. |
| CDC-18376 | RWB-S6-E5023-CON | CG-ALL-10344 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case. |
| CDC-18377 | RWB-S6-E5023-CON | CG-ALL-10345 | 12.2 | Declare REST base /api/recovery/source-data/v1 for provider P1 rwb-source-data. |
| CDC-18378 | RWB-S6-E5023-CON | CG-ALL-10346 | 12.2 | Declare REST base /api/recovery/decision/v1 for provider P7 rwb-decision. |
| CDC-18395 | RWB-S6-E5024-APP | CG-ALL-10359 | 12.2 | Declare the REST base /api/recovery/case/v1 in the yaml. |
| CDC-18396 | RWB-S6-E5024-APP | CG-ALL-10360 | 12.2 | Declare the REST base /api/recovery/source-data/v1 in the yaml. |
| CDC-18397 | RWB-S6-E5024-APP | CG-ALL-10361 | 12.2 | Declare the REST base /api/recovery/agent/v1 in the yaml. |
| CDC-18398 | RWB-S6-E5024-APP | CG-ALL-10362 | 12.2 | Declare the REST base /api/recovery/decision/v1 in the yaml. |
| CDC-18401 | RWB-S6-E5024-APP | DOR-RWB-S6-E5024-APP-8 |  | Add base paths /api/recovery/case/v1, /api/recovery/source-data/v1, /api/recovery/agent/v1, /api/recovery/decision/v1 and the 3 more named in detcheck. |
| CDC-18415 | RWB-S6-E5024-CON | CG-ALL-10376 | 12.2 | Declare REST base /api/recovery/case/v1 using the provider's base from the Document Index service table. |
| CDC-18416 | RWB-S6-E5024-CON | CG-ALL-10377 | 12.2 | Declare REST base /api/recovery/source-data/v1 using the provider's base from the Document Index service table. |
| CDC-18417 | RWB-S6-E5024-CON | CG-ALL-10378 | 12.2 | Declare REST base /api/recovery/agent/v1 using the provider's base from the Document Index service table. |
| CDC-18418 | RWB-S6-E5024-CON | CG-ALL-10379 | 12.2 | Declare REST base /api/recovery/decision/v1 using the provider's base from the Document Index service table. |
| CDC-18445 | RWB-S6-E5026-APP | CG-ALL-10406 | 12.2 | Declare REST base /api/recovery/document/v1 for rwb-document, taken from the Document Index service table. |
| CDC-18446 | RWB-S6-E5026-APP | CG-ALL-10407 | 12.2 | Declare REST base /api/recovery/partner/v1 for rwb-partner, taken from the Document Index service table. |
| CDC-18447 | RWB-S6-E5026-APP | CG-ALL-10408 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case, taken from the Document Index service table. |
| CDC-18451 | RWB-S6-E5026-APP | DOR-RWB-S6-E5026-APP-8 |  | Declare REST bases for /api/recovery/document/v1, /api/recovery/partner/v1 and /api/recovery/case/v1 (CG-ALL-10406 to -10408); clear the two further detcheck items. |
| CDC-18469 | RWB-S6-E5026-CON | CG-ALL-10420 | 12.2 | Declare the REST base /api/recovery/document/v1 with the provider's REST base from the Document Index service table. |
| CDC-18470 | RWB-S6-E5026-CON | CG-ALL-10421 | 12.2 | Declare the REST base /api/recovery/partner/v1 from the Document Index service table. |
| CDC-18471 | RWB-S6-E5026-CON | CG-ALL-10422 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-18473 | RWB-S6-E5026-CON | DOR-RWB-S6-E5026-CON-8 | none | Declare REST bases for /api/recovery/document/v1, /api/recovery/partner/v1 and /api/recovery/case/v1. The task queue part is resolved in 12.5. |
| CDC-18488 | RWB-S6-E6001-APP | CG-ALL-10429 | 12.2 | Declare REST base /api/recovery/decision/v1 from the Document Index service table. |
| CDC-18489 | RWB-S6-E6001-APP | CG-ALL-10430 | 12.2 | Declare REST base /api/recovery/decision/v1 from the Document Index service table. |
| CDC-18490 | RWB-S6-E6001-APP | CG-ALL-10431 | 12.2 | Declare REST base /api/recovery/access/v1 from the Document Index service table. |
| CDC-18491 | RWB-S6-E6001-APP | CG-ALL-10432 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-18507 | RWB-S6-E6001-CON | CG-ALL-10442 | 12.2 | Declare REST base /api/recovery/decision/v1 for rwb-decision (P7), matching the Document Index service table. |
| CDC-18508 | RWB-S6-E6001-CON | CG-ALL-10443 | 12.2 | Declare REST base /api/recovery/decision/v1 for rwb-decision (P7), matching the Document Index service table. |
| CDC-18509 | RWB-S6-E6001-CON | CG-ALL-10444 | 12.2 | Declare REST base /api/recovery/access/v1 for rwb-access (P4), matching the Document Index service table. |
| CDC-18510 | RWB-S6-E6001-CON | CG-ALL-10445 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case (P3), matching the Document Index service table. |
| CDC-18512 | RWB-S6-E6001-CON | DOR-RWB-S6-E6001-CON-8 | 12.2, 12.5 | Declare REST bases for /api/recovery/decision/v1, /api/recovery/access/v1 and /api/recovery/case/v1; task queue fixed in story. |
| CDC-18530 | RWB-S6-E6002-APP | CG-ALL-10457 | 12.2 | Declare REST base /api/recovery/partner/v1 in the yaml. Story path already matches; no story edit. |
| CDC-18546 | RWB-S6-E6002-CON | CG-ALL-10472 | 12.2 | Declare REST base /api/recovery/partner/v1 for S9 rwb-partner, the path the story consumes. |
| CDC-18567 | RWB-S6-E6003-APP | CG-ALL-10489 | 12.2 | Declare the REST base /api/recovery/partner/v1 for the rwb-partner read of buyer licence, KYC and panel facts, per the Document Index service table. |
| CDC-18568 | RWB-S6-E6003-APP | CG-ALL-10490 | 12.2 | Declare the REST base /api/recovery/partner/v1 for the rwb-partner panel suspension request, per the Document Index service table. |
| CDC-18569 | RWB-S6-E6003-APP | CG-ALL-10491 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case GET /cases/{caseId} family, per the Document Index service table. |
| CDC-18570 | RWB-S6-E6003-APP | CG-ALL-10492 | 12.2 | Declare the REST base /api/recovery/access/v1 for the rwb-access authorise call and capability area read, per the Document Index service table. |
| CDC-18571 | RWB-S6-E6003-APP | CG-ALL-10493 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision rule package in force read, per the Document Index service table. |
| CDC-18574 | RWB-S6-E6003-APP | DOR-RWB-S6-E6003-APP-8 | 8 | Add base paths /api/recovery/partner/v1, /api/recovery/case/v1, /api/recovery/access/v1, /api/recovery/decision/v1 and the four further bases the check names. |
| CDC-18582 | RWB-S6-E6003-CON | CG-ALL-10505 | 12.2 | Declare REST base /api/recovery/partner/v1 for S9 rwb-partner, as in the Document Index service table. |
| CDC-18583 | RWB-S6-E6003-CON | CG-ALL-10506 | 12.2 | Declare REST base /api/recovery/partner/v1 for S9 rwb-partner, as in the Document Index service table. |
| CDC-18584 | RWB-S6-E6003-CON | CG-ALL-10507 | 12.2 | Declare REST base /api/recovery/case/v1 for P3 rwb-case, as in the Document Index service table. |
| CDC-18585 | RWB-S6-E6003-CON | CG-ALL-10508 | 12.2 | Declare REST base /api/recovery/access/v1 for P4 rwb-access, as in the Document Index service table. |
| CDC-18586 | RWB-S6-E6003-CON | CG-ALL-10509 | 12.2 | Declare REST base /api/recovery/decision/v1 for P7 rwb-decision, as in the Document Index service table. |
| CDC-18588 | RWB-S6-E6003-CON | DOR-RWB-S6-E6003-CON-8 | 12.2 | Declare REST bases /api/recovery/partner/v1, /case/v1, /access/v1 and /decision/v1 for the consumed providers. |
| CDC-18595 | RWB-S6-E6003-CON | GAP-2987 | find it | Publish the additive OpenAPI 3.1 fragment of rwb-debtsale with the bar element, six consumed rows, closed lists, move names, route states, eight fakes and five contract tests, tagged Draft. |
| CDC-18597 | RWB-S6-E6004-APP | CG-ALL-10524 | 12.2 | Declare REST base /api/recovery/partner/v1 using the provider's base from the Document Index service table. |
| CDC-18598 | RWB-S6-E6004-APP | CG-ALL-10525 | 12.2 | Declare REST base /api/recovery/case/v1 using the provider's base from the Document Index service table. |
| CDC-18599 | RWB-S6-E6004-APP | CG-ALL-10526 | 12.2 | Declare REST base /api/recovery/access/v1 using the provider's base from the Document Index service table. |
| CDC-18600 | RWB-S6-E6004-APP | CG-ALL-10527 | 12.2 | Declare REST base /api/recovery/decision/v1 using the provider's base from the Document Index service table. |
| CDC-18603 | RWB-S6-E6004-APP | DOR-RWB-S6-E6004-APP-8 | 12.2 | Add base paths /api/recovery/partner/v1, /api/recovery/case/v1, /api/recovery/access/v1, /api/recovery/decision/v1 and the four further paths in the detail. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (25)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18368 | RWB-S6-E5023-APP | CG-ALL-10320 | 8 | Record account_id as a field in LDM v9 Fields and Data Classification v5 Fields, or confirm the dictionary name; the story names it at lines 166 and 299. |
| CDC-18369 | RWB-S6-E5023-APP | CG-ALL-10321 | 12.7 | Record decision_record as the PLT decision-record library object created in rwb_debtsale by the library migration (DP-03). |
| CDC-18372 | RWB-S6-E5023-APP | DOR-RWB-S6-E5023-APP-7 | 11 | Register account_id (DF-SAL-033) and decision_record as a field or entity, or confirm their names; the story now flags them. |
| CDC-18382 | RWB-S6-E5023-CON | CG-ALL-10343 | find it | Record account_id as a field of the debt_sale_account object, or name the dictionary entry the story should use. |
| CDC-18435 | RWB-S6-E5025-APP | CG-ALL-10389 | 3, 12.7 | Add account_id as the field of debt_sale_account (DF-SAL-033), or record it as a named object in the owning document. |
| CDC-18436 | RWB-S6-E5025-APP | CG-ALL-10390 | 11, 12.7 | Record document_version as the rwb-document (P5) table name, or confirm its dictionary name. |
| CDC-18440 | RWB-S6-E5025-APP | DOR-RWB-S6-E5025-APP-7 | 11 | Confirm or add account_id, document_version and decision_record as fields or entities; the legacy job and decision-log wording in AC1 and AC3 is kept by design. |
| CDC-18452 | RWB-S6-E5026-APP | CG-ALL-10403 | 4, 11 | Record nda_signed_at as the partner_user field read on the rwb-partner contract (S9), or give its dictionary name. |
| CDC-18453 | RWB-S6-E5026-APP | CG-ALL-10404 | 8, 11, 12.7 | Record account_id as the identifier of debt_sale_account, or give its dictionary name. |
| CDC-18454 | RWB-S6-E5026-APP | CG-ALL-10405 | 11, 12.7 | Record decision_record as the platform library table created in rwb_debtsale (DP-03, DP-09). |
| CDC-18457 | RWB-S6-E5026-APP | DOR-RWB-S6-E5026-APP-7 | 11 | Add nda_signed_at, account_id and decision_record as fields or entities. Story P3 wording now says decision record in AC1, AC2 and the note. |
| CDC-18478 | RWB-S6-E5026-CON | DOR-RWB-S6-E5026-CON-7 | 11 | Add account_id as a field of debt_sale_account, or name the field that holds it so the section 11 account element resolves. |
| CDC-18533 | RWB-S6-E6002-APP | CG-ALL-10452 | find it | Add kyc_status as a field, or record its dictionary name; the story reads it as an rwb-partner contract fact (L56, L64). |
| CDC-18534 | RWB-S6-E6002-APP | CG-ALL-10453 | find it | Add licence_expiry as a field, or record its dictionary name; it is an rwb-partner contract fact (L56, L64). |
| CDC-18535 | RWB-S6-E6002-APP | CG-ALL-10454 | find it | Add nda_signed_at as a field, or record its dictionary name; it is an rwb-partner contract fact (L82, L83). |
| CDC-18536 | RWB-S6-E6002-APP | CG-ALL-10455 | find it | Add account_id as a field, or record its dictionary name; it is an identifier of another service's fact (BR5, L178). |
| CDC-18537 | RWB-S6-E6002-APP | CG-ALL-10456 | find it | Record decision_record as a PLT library object created in rwb_debtsale in the owning document (library migration, DP-03). |
| CDC-18542 | RWB-S6-E6002-APP | DOR-RWB-S6-E6002-APP-7 | 11 | Add kyc_status, licence_expiry, nda_signed_at and account_id, and the two further names detcheck flags, as fields or entities, or map them to their LDM names |
| CDC-18551 | RWB-S6-E6002-CON | CG-ALL-10471 | 12.2 | Record licence_expiry as a buyer field in LDM v9 or Data Classification v5, or give its dictionary name without substituting insurance_expiry unless the meaning matches. |
| CDC-18556 | RWB-S6-E6002-CON | DOR-RWB-S6-E6002-CON-7 | 11 | Record nda_signed_at, kyc_status and licence_expiry as buyer partner fields, or give their dictionary names. |
| CDC-18575 | RWB-S6-E6003-APP | CG-ALL-10486 | 8 | Record account_id under its dictionary name (account, account_code or account_no) or record it as an object in its owning document. |
| CDC-18576 | RWB-S6-E6003-APP | CG-ALL-10487 | 11 | Record decision_record as a PLT library object created in rwb_debtsale under its dictionary name, or record it in its owning document. |
| CDC-18577 | RWB-S6-E6003-APP | CG-ALL-10488 | 12.2 | Record kyc_status under its dictionary name (ocr_status, status or match_status) or record it as a field of the partner contract in its owning document. |
| CDC-18589 | RWB-S6-E6003-CON | CG-ALL-10504 | 12.2 | Register kyc_status as a field, or record the dictionary name or the object (index, library table, flag) that carries the S9 KYC status |
| CDC-18609 | RWB-S6-E6004-APP | DOR-RWB-S6-E6004-APP-7 | 11 | Name account_id (debt_sale_account field) and decision_record (platform library object) in LDM v9 or Data Classification v5 |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (21)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18371 | RWB-S6-E5023-APP | CG-ALL-10333 | 16 | Add rows for TC-E5-023-01 to TC-E5-023-05 (and TC-E5-023-06 to TC-E5-023-08 added in this story) with Given, When and Then copied from the criteria they cover. |
| CDC-18385 | RWB-S6-E5023-CON | DOR-RWB-S6-E5023-CON-12 | 16 | Add tab rows for TC-E5-023-01 to -05 and TC-S6-E5023-CON-01 to -08. |
| CDC-18391 | RWB-S6-E5023-CON | CG-ALL-10352 | 16 | Add rows for TC-E5-023-01 to -05 and TC-S6-E5023-CON-01 to -05, with Given, When and Then copied from the criterion each covers. |
| CDC-18406 | RWB-S6-E5024-APP | CG-ALL-10367 | 16 | Add rows for TC-E5-024-01 to 04 and TC-S6-E5024-APP-01 to 03 with Given, When and Then copied from the criteria they cover. |
| CDC-18407 | RWB-S6-E5024-APP | DOR-RWB-S6-E5024-APP-12 | 12, 12.7, 16 | Story rows TC-S6-E5024-APP-04 to -12 added in section 16 |
| CDC-18424 | RWB-S6-E5024-CON | DOR-RWB-S6-E5024-CON-12 | 12.7, 16 | Add tab Story test cases rows for TC-E5-024-01 to TC-E5-024-04 and TC-S6-E5024-CON-01 to TC-S6-E5024-CON-06. |
| CDC-18426 | RWB-S6-E5024-CON | CG-ALL-10384 | 16 | Add rows for TC-E5-024-01, TC-E5-024-02, TC-E5-024-03, TC-E5-024-04, TC-S6-E5024-CON-01 to TC-S6-E5024-CON-05 with Given, When and Then copied from the criteria they cover. |
| CDC-18439 | RWB-S6-E5025-APP | CG-ALL-10399 | 16 | Add rows TC-E5-025-01 to TC-E5-025-05 with Given, When and Then copied from the criterion each covers. |
| CDC-18456 | RWB-S6-E5026-APP | CG-ALL-10413 | 16 | Add rows TC-E5-026-01 to TC-E5-026-04 with Given, When and Then copied from the criterion each covers, in the next Test Cases version. |
| CDC-18477 | RWB-S6-E5026-CON | DOR-RWB-S6-E5026-CON-12 | 16 | Add rows for TC-E5-026-01 to -04 and TC-S6-E5026-CON-01 to -05 under tab Story test cases. |
| CDC-18485 | RWB-S6-E5026-CON | CG-ALL-10427 | 16 | Add rows for TC-E5-026-01 to -04 and TC-S6-E5026-CON-01 to -04 with Given, When and Then copied from the criteria they cover. |
| CDC-18496 | RWB-S6-E6001-APP | CG-ALL-10437 | 16 | Add story test case rows TC-E6-001-01 to TC-E6-001-06 with Given, When and Then copied from AC1 to AC4, Access and Principle 5. |
| CDC-18516 | RWB-S6-E6001-CON | DOR-RWB-S6-E6001-CON-12 | 12.7, 16 | Add test case rows TC-S6-E6001-CON-01 to TC-S6-E6001-CON-06 to Test Cases v8. |
| CDC-18525 | RWB-S6-E6001-CON | CG-ALL-10449 | 16 | Add rows TC-S6-E6001-CON-01 to TC-S6-E6001-CON-06 with Given, When and Then copied from the criteria they cover. |
| CDC-18540 | RWB-S6-E6002-APP | CG-ALL-10464 | 16 | Add rows TC-E6-002-01 to TC-E6-002-06 with Given, When and Then copied from the criteria each covers. |
| CDC-18541 | RWB-S6-E6002-APP | DOR-RWB-S6-E6002-APP-12 | 16 | Story adds TC-07 to TC-13 with their AC links |
| CDC-18564 | RWB-S6-E6002-CON | CG-ALL-10479 | 16 | Add rows for TC-E6-002-01 to -06 and TC-S6-E6002-CON-01 to -07, with Given, When and Then copied from the criterion each covers. |
| CDC-18580 | RWB-S6-E6003-APP | CG-ALL-10499 | 16 | Story side done (TC-E6-003-07 to TC-E6-003-19 added in section 16). Only the Test Cases v8 rows remain. |
| CDC-18593 | RWB-S6-E6003-CON | DOR-RWB-S6-E6003-CON-12 | 12.7, 16 | Add full test rows for TC-E6-003-01 to -06, TC-S6-E6003-CON-01 to -04 and TC-S6-E6003-CON-05 (new boundary row for the §12.7 tables) |
| CDC-18596 | RWB-S6-E6003-CON | CG-ALL-10515 | 16 | In the next version add rows for TC-E6-003-01 to -06 and TC-S6-E6003-CON-01 to -04, with Given, When and Then copied from the criteria they cover. |
| CDC-18608 | RWB-S6-E6004-APP | CG-ALL-10532 | 16 | Add rows TC-E6-004-01 to TC-E6-004-05 with Given, When and Then copied from the criteria they cover (AC1, AC2, AC3, Access, Principle 5). |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18370 | RWB-S6-E5023-APP | CG-ALL-10331 | 12.5 | Add an Activities row for selectEligibleAccounts with task queue rwb-debtsale, or name a catalogued activity. |
| CDC-18405 | RWB-S6-E5024-APP | CG-ALL-10365 | 12.5 | Add activity buildLotsAndEstimatePrice for rwb-debtsale, or replace it with a catalogued activity. |
| CDC-18422 | RWB-S6-E5024-CON | CG-ALL-10382 | 12.5 | Add buildLotsAndEstimatePrice to the Activities sheet, or name a catalogued activity in its place. |
| CDC-18438 | RWB-S6-E5025-APP | CG-ALL-10397 | 12.5 | Add activity prepareMaskedTape on task queue rwb-debtsale with the contract element of §12.5, or name a catalogued activity. |
| CDC-18475 | RWB-S6-E5026-CON | CG-ALL-10425 | 12.5 | Add an Activities row for openBuyerDataRoom on task queue rwb-debtsale, or name a catalogued activity in section 12.5 instead. |
| CDC-18495 | RWB-S6-E6001-APP | CG-ALL-10436 | 12.5 | Add activity recordCommitteeApproval to the Activities sheet on task queue rwb-debtsale with its contract element, or name a catalogued activity in RWB-S6-E6001-APP section 12.5. |
| CDC-18532 | RWB-S6-E6002-APP | DOR-RWB-S6-E6002-APP-8 | 12.5 | Add activity qualifyBuyer on rwb-debtsale. The story records the DebtSaleWorkflow ID form and start rule as not specified. |
| CDC-18548 | RWB-S6-E6002-CON | DOR-RWB-S6-E6002-CON-8 | 12.5 | Register activity qualifyBuyer. Story now states workflow ID and start rule as not specified; task queue fixed. |
| CDC-18578 | RWB-S6-E6003-APP | CG-ALL-10496 | 12.5 | Add an assessRemediation activity row for task queue rwb-debtsale with its contract element. |
| CDC-18579 | RWB-S6-E6003-APP | CG-ALL-10497 | 12.5 | Add a barBuyer activity row for task queue rwb-debtsale with its contract element. |
| CDC-18590 | RWB-S6-E6003-CON | CG-ALL-10512 | 12.5 | Add activity assessRemediation on queue rwb-debtsale, or name a catalogued activity |
| CDC-18591 | RWB-S6-E6003-CON | CG-ALL-10513 | 12.5 | Add activity barBuyer on queue rwb-debtsale, or name a catalogued activity |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18386 | RWB-S6-E5023-CON | DOR-RWB-S6-E5023-CON-7 | 11 | Confirm account_id as a field or entity of the account element (DF-SAL-031 to DF-SAL-037) and classify it in Data Classification v5 |
| CDC-18402 | RWB-S6-E5024-APP | CG-ALL-10356 |  | Record account_count under its dictionary name, or record it as an object in the owning rules document (R-DS-05 size test). |
| CDC-18403 | RWB-S6-E5024-APP | CG-ALL-10357 |  | Add the account identifier used in debt_sale_account to the dictionary under its dictionary name, or confirm the name used by Data Classification v5. |
| CDC-18404 | RWB-S6-E5024-APP | CG-ALL-10358 |  | Record decision_record as a PLT library object created in rwb_debtsale, as the story table already states. |
| CDC-18437 | RWB-S6-E5025-APP | CG-ALL-10391 | 11 | Record decision_record as a PLT library object created in rwb_debtsale (DP-03), or confirm its dictionary name. |
| CDC-18474 | RWB-S6-E5026-CON | CG-ALL-10419 | 7, 11 | Add account_id, or name the dictionary entry for the DF-SAL-031 account property (nearest: account, account_code, account_no). |
| CDC-18549 | RWB-S6-E6002-CON | CG-ALL-10469 | 12.2 | Record nda_signed_at as a dictionary field, or record the owning object (index, library table, flag) in the owning document. |
| CDC-18550 | RWB-S6-E6002-CON | CG-ALL-10470 | 12.2 | Record kyc_status as a dictionary field, or record the owning object (index, library table, flag) in the owning document. |
| CDC-18604 | RWB-S6-E6004-APP | CG-ALL-10522 | 8, 11 | Add account_id as a Field of debt_sale_account, or record the object it names, as the story uses it in BR6 and the DF-SAL-031 to DF-SAL-037 row. |
| CDC-18605 | RWB-S6-E6004-APP | CG-ALL-10523 | 11, 12.7 | Record decision_record as a PLT library object created in rwb_debtsale by the library migration (DP-03). |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18379 | RWB-S6-E5023-CON | DOR-RWB-S6-E5023-CON-14 | find it | Record the signed epic design sign-off in the epic design record, then cite it in the story. The sign-off is not in the story or the source documents. |
| CDC-18419 | RWB-S6-E5024-CON | DOR-RWB-S6-E5024-CON-14 | header | Record the signed sign-off of the epic design that covers this story. |
| CDC-18448 | RWB-S6-E5026-APP | DOR-RWB-S6-E5026-APP-14 |  | Record the signed epic design sign-off covering RWB-S6-E5026-APP. |
| CDC-18472 | RWB-S6-E5026-CON | DOR-RWB-S6-E5026-CON-14 | none | Record the signed epic design sign-off, which this story and the source documents do not cite. |
| CDC-18511 | RWB-S6-E6001-CON | DOR-RWB-S6-E6001-CON-14 | header | Record the signed epic design sign-off for the EP06 epic design, then cite it in the story. |
| CDC-18547 | RWB-S6-E6002-CON | DOR-RWB-S6-E6002-CON-14 | header | Record the signed epic design sign-off so the story can cite it. |
| CDC-18572 | RWB-S6-E6003-APP | DOR-RWB-S6-E6003-APP-14 | all | Record and confirm the signed epic design sign-off for this story's epic in the epic design record. |
| CDC-18587 | RWB-S6-E6003-CON | DOR-RWB-S6-E6003-CON-14 | header | Record the signed epic design sign-off for RWB-S6-E6003-CON. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18383 | RWB-S6-E5023-CON | CG-ALL-10350 | 12.5 | Add an Activities row for selectEligibleAccounts, type Activity, task queue rwb-debtsale. |
| CDC-18455 | RWB-S6-E5026-APP | CG-ALL-10411 | 12.5 | Add activity openDataRoom (task queue rwb-debtsale) as a catalogued activity. |
| CDC-18514 | RWB-S6-E6001-CON | CG-ALL-10448 | 12.5 | Add a row for activity recordCommitteeApproval (task queue rwb-debtsale) or change 12.5 to a catalogued activity. |
| CDC-18552 | RWB-S6-E6002-CON | CG-ALL-10476 | 12.5 | Add activity qualifyBuyer on queue rwb-debtsale to the Activities sheet. |
| CDC-18553 | RWB-S6-E6002-CON | CG-ALL-10477 | 12.5 | Add the rwb-decision package activity on queue rwb-decision once its name is fixed; name Not specified in the source documents (GAP-2985; ASM-4913). |
| CDC-18606 | RWB-S6-E6004-APP | CG-ALL-10530 | 12.5 | Add activity takeBid on task queue rwb-debtsale, or map the story to a catalogued activity. |
| CDC-18607 | RWB-S6-E6004-APP | CG-ALL-10531 | 12.5 | Add activity closeLotAfterClaimWindow on task queue rwb-debtsale, or map the story to a catalogued activity. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18373 | RWB-S6-E5023-APP | DOR-RWB-S6-E5023-APP-9 | 14 | Confirm the MSG-P1-001 wording against the standard and align the text; the legacy text stays until then. |
| CDC-18387 | RWB-S6-E5023-CON | DOR-RWB-S6-E5023-CON-9 | 14 | Publish the MSG-P1-001 text the standard gives for this condition so the section 14 row follows it |
| CDC-18390 | RWB-S6-E5023-CON | CG-ALL-10351 | 14 | MSG-P1-001 text reverted to the story's earlier wording; closing sentence restored |
| CDC-18414 | RWB-S6-E5024-APP | GAP-1788 | find it | Carry MSG-S6-001, MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 with owner Business analyst, S6 and Thai and English versions; confirm wording before wave 4. |
| CDC-18429 | RWB-S6-E5024-CON | GAP-1788 | find it | Carry MSG-S6-001, MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 with owner Business analyst, S6 and a Thai and English version each; confirm the wording before wave 4. |
| CDC-18441 | RWB-S6-E5025-APP | DOR-RWB-S6-E5025-APP-9 | 14 | Confirm the MSG-P1-001 text of the standard or align the standard to the FSD wording; section 14 keeps the FSD text until then. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18409 | RWB-S6-E5024-APP | GAP-1771 | 2 | Hold debt_sale_lot and debt_sale_account as physical tables; hold data room state, buyer terms, bids, award and transfer as entity groups with key fields; add the missing Ownership Map rows in the same change. |
| CDC-18425 | RWB-S6-E5024-CON | GAP-1771 |  | Hold debt_sale_lot and debt_sale_account as physical tables; hold data room state, buyer terms, bids, award and transfer as entity groups with key fields; add those rows to the Ownership Map in the same change. |
| CDC-18463 | RWB-S6-E5026-APP | GAP-1771 | n/a | Add rows for buyer terms, bids, award and transfer and data room state as entity groups with key fields, and fix physical names with the S6 DB story. |
| CDC-18482 | RWB-S6-E5026-CON | GAP-1771 |  | Add ownership and table or entity-group rows for data room, buyer terms, bids, award and transfer with the key fields this PRD states. |
| CDC-18500 | RWB-S6-E6001-APP | GAP-1771 |  | Hold debt_sale_lot and debt_sale_account as physical tables and the other five as entity groups with the PRD key fields; add their Ownership Map rows in the same change. |
| CDC-18520 | RWB-S6-E6001-CON | GAP-1771 |  | Add ownership rows and key-field lists for data room, buyer terms, bids, award and transfer; fix physical names with the S6 DB story. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18381 | RWB-S6-E5023-CON | GAP-1770 | 8 | BR3 score field names set to Not specified in the source documents (GAP-1770) |
| CDC-18462 | RWB-S6-E5026-APP | GAP-1780 | n/a | Run DebtSaleWorkflow as the stage workflow of the case for eligibility and case-side steps and as the lot saga for sale steps, keyed by lot number. |
| CDC-18481 | RWB-S6-E5026-CON | GAP-1780 |  | State DebtSaleWorkflow as the case stage workflow plus lot saga keyed by lot number; case moved by rwb-case on LotAwarded and AccountsTransferred. |
| CDC-18519 | RWB-S6-E6001-CON | GAP-1780 |  | Record DebtSaleWorkflow as the stage workflow of the case and the saga of the lot keyed by lot number; case moved by rwb-case on LotAwarded and AccountsTransferred. |
| CDC-18559 | RWB-S6-E6002-CON | GAP-1774 | find it | Give S6 a cell to S9 and to the partner gateway; route the buyer operations through the partner gateway and not directly under /partner. |

### RWB-S6-E5024-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18389 | RWB-S6-E5023-CON | GAP-2976 | None | Publish the priced part, bind each error to a section 14 message id, declare the estimate element with model version and placeholder operations, fix minimum lot size as a rule row, record tag date and sign-off. |
| CDC-18399 | RWB-S6-E5024-APP | DOR-RWB-S6-E5024-APP-21 | header | Set its build status to Done once the contract is published; this story is ready only after that. |
| CDC-18400 | RWB-S6-E5024-APP | DOR-RWB-S6-E5024-APP-22 | header | Record the published contract fake library version. |
| CDC-18408 | RWB-S6-E5024-APP | GAP-2976 | 1 | Publish the priced part as an additive v1 change; bind each error to one section 14 message id; declare the estimate element with model version and placeholder operation names; make minimum lot size a rule row; record tag date and consumer sign-off. |

### RWB-S6-E6004-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18479 | RWB-S6-E5026-CON | GAP-2988 |  | Add class C rows for the five consumed reads, DP-08 and DP-09 rows with RWB-PLT-TE006-CON as wave 0 library, and API-S6-005 as the slice operation. |
| CDC-18543 | RWB-S6-E6002-APP | GAP-2988 | 12 | Fill C, I and X for the five consumed rows; add DP-08 and DP-09 to the H row; set API-S6-005 as its operation; add the bid and realised-recovery columns; keep one writer per shared rule |
| CDC-18557 | RWB-S6-E6002-CON | GAP-2988 | find it | Add plan rows for the five consumed contracts, the guard and outbox libraries, DP-08 and DP-09, and fix API-S6-005 as its operation. Not in this story. |
| CDC-18610 | RWB-S6-E6004-APP | GAP-2988 | 9 | Record the five consumed contract rows in class C with placeholders and RWB-PLT-TE006-CON as wave 0 library; add DP-08 and DP-09 rows |

### OTHER:split_plan.json (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18505 | RWB-S6-E6001-APP | GAP-2981 | header | Add the five C rows for RWB-S6-E6001-APP: rwb-decision approval chain, rwb-decision rule package, rwb-access DoA limit, rwb-case state read, rwb-case move answer. |
| CDC-18518 | RWB-S6-E6001-CON | GAP-1963 | header | Add the five C rows (P7 approval chain, P7 rule-package read, P4 delegation_limit, P3 case state read, P3 case-move answer) and the rwb-decision queue dependency to the dependency map. |
| CDC-18521 | RWB-S6-E6001-CON | GAP-1976 |  | Add H row for RWB-S6-E5025-APP (lane L-S6-C) in this Work Package; keep plan wave and release values; record the two EP06 release dates inside the service. |
| CDC-18594 | RWB-S6-E6003-CON | GAP-2986 | find it | Fill C, I and X for RWB-S6-E6003-APP, add plan rows for the six consumed contracts, and record the wave conflict once for rwb-debtsale and EP06. |

### RWB-S6-E6004-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18561 | RWB-S6-E6002-CON | GAP-2989 | find it | Publish the bid baseline with placeholders, bind each error to one section 14 message id, confirm the three operation names and the publish-first question before tagging. |
| CDC-18601 | RWB-S6-E6004-APP | DOR-RWB-S6-E6004-APP-21 | n/a | Complete the contract build so its build status is Done and the contract is published. |
| CDC-18602 | RWB-S6-E6004-APP | DOR-RWB-S6-E6004-APP-22 | n/a | Publish the contract fake and record its library version. |
| CDC-18614 | RWB-S6-E6004-APP | GAP-2989 | 12 | Publish the API-S6-005 baseline with placeholders, bind each error to one message id, declare the Bid element and its storage split, confirm the three operation names and the publish-first question, record the tag date. |

### OTHER:_work/msr/extract (extract step) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18412 | RWB-S6-E5024-APP | GAP-1975 | find it | Add the FSD S6 and TSD S6 module extracts at the next extract pass; until then read the module files directly, with fill order R7.3 unchanged. |
| CDC-18413 | RWB-S6-E5024-APP | GAP-1955 | find it | Produce the FSD S6 and TSD S6 extracts into _work/msr/extract at the next extract pass; read the module files directly until then. |
| CDC-18468 | RWB-S6-E5026-APP | GAP-1961 | none | Add the S6 module extract to the extract set before the baseline is tagged so that a later diff is possible. |

### RWB-S6-E5024-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18423 | RWB-S6-E5024-CON | DOR-RWB-S6-E5024-CON-10 | find it | Declare empty, loading, error and no-access states for SCR-25. |
| CDC-18497 | RWB-S6-E6001-APP | GAP-2975 |  | Keep the H, C, I and X rows; add class C rows for rwb-case, rwb-source-data, rwb-agent and rwb-decision with placeholders; record RWB-P10-TE013-CON and RWB-PLT-TE006-CON; record package rule values as rule rows with placeholders; adopt REQ-S6-002. |
| CDC-18517 | RWB-S6-E6001-CON | GAP-2975 | find it | Keep H, C, I, X rows; add rwb-case, rwb-source-data, rwb-agent and rwb-decision as class C placeholders; add RWB-P10-TE013-CON and RWB-PLT-TE006-CON; record lot size, tiered terms and reserve policy as placeholder rule rows; adopt REQ-S6-002. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-debtsale.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18430 | RWB-S6-E5025-APP | CG-ALL-10392 | 2 | Remove the fixed enum on buyerClass so LOV-BUYER-CLASS values are accepted as data without a code change (BR-S6-003). |
| CDC-18431 | RWB-S6-E5025-APP | CG-ALL-10393 | 2 | Remove the fixed enum on status so LOV-LOT-STATUS values are accepted as data without a code change (BR-S6-003). |
| CDC-18432 | RWB-S6-E5025-APP | CG-ALL-10394 | 2 | Remove the fixed enum on segment so LOV-SEGMENT values are accepted as data without a code change (BR-S6-003). |

### RWB-S6-E5026-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18449 | RWB-S6-E5026-APP | DOR-RWB-S6-E5026-APP-21 |  | Complete the contract build so that its build status is Done. |
| CDC-18450 | RWB-S6-E5026-APP | DOR-RWB-S6-E5026-APP-22 |  | Publish the contract fake and record its library version. |
| CDC-18466 | RWB-S6-E5026-APP | GAP-2978 | header | Publish the baseline with the three operation placeholders, DataRoom, lot, account and tape elements, one message id per error, the case boundary, and no opening event or status. |

### RWB-S6-E6002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18459 | RWB-S6-E5026-APP | GAP-2984 | n/a | Keep plan H, C, I and X rows; declare rwb-partner as class C with placeholder name and 2 s budget; package as activity on rwb-decision; case move as child stage outcome; bid as decision record and raise bid table for the DB story; adopt REQ-S6-004. |
| CDC-18555 | RWB-S6-E6002-CON | DOR-RWB-S6-E6002-CON-10 | n/a | Declare empty, loading, error and no-access states for SCR-26 in the app story that owns it. |
| CDC-18558 | RWB-S6-E6002-CON | GAP-2984 | find it | Declare rwb-partner as class C with a placeholder name and 2 s budget; declare the package as an rwb-decision activity; raise the bid table for the DB story; adopt REQ-S6-004. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18476 | RWB-S6-E5026-CON | DOR-RWB-S6-E5026-CON-1 | 1 | Add the role tech lead as a role name, or give section 1 a role code or role name that Users Roles and Permissions v5 lists. |
| CDC-18554 | RWB-S6-E6002-CON | DOR-RWB-S6-E6002-CON-1 | 1 | Add tech lead as a role name, or confirm the role code that section 1 should use. |
| CDC-18592 | RWB-S6-E6003-CON | DOR-RWB-S6-E6003-CON-1 | 1 | Confirm 'tech lead' as a role name in the file, or the story must name a role that is listed there |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18374 | RWB-S6-E5023-APP | GAP-1781 | 4 | Name the monthly cycle opener as a Temporal Schedule or event-started workflow on rwb-debtsale with owner, run book and cycle date. |
| CDC-18388 | RWB-S6-E5023-CON | GAP-1781 | 12.5 | Start rule no longer names a Temporal Schedule; the schedule and cycle-date record are marked Not specified in the source documents. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18380 | RWB-S6-E5023-CON | DOR-RWB-S6-E5023-CON-8 | 12.5 | Add the three base paths to their yamls; reconcile the rwb-debtsale queue and namespace row with the catalog entry. |
| CDC-18494 | RWB-S6-E6001-APP | DOR-RWB-S6-E6001-APP-8 | 12.5 | Add base paths /api/recovery/decision/v1, /api/recovery/access/v1 and /api/recovery/case/v1 to the API Specification v5 yaml; align the DebtSaleWorkflow task queue rwb-debtsale and namespace rwb-recovery with the catalog row. |

### OTHER:Extract folder _work/msr/extract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18427 | RWB-S6-E5024-CON | GAP-1975 | find it | Add the FSD S6 Debt sale and TSD S6 Debt sale extracts at the next extract pass for the later stages; this run reads FSD S6 v3 and TSD S6 v2 directly and keeps the R7.3 fill order. |
| CDC-18428 | RWB-S6-E5024-CON | GAP-1955 | find it | Produce the FSD S6 and TSD S6 extracts into _work/msr/extract at the next extract pass; until then the module files are read directly, as this story does. |

### RWB-S6-E5026-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18442 | RWB-S6-E5025-APP | GAP-2977 | 13 | Record rwb-document, rwb-partner and rwb-case as class C dependencies with placeholders and fakes, the partner channel as an edge dependency, and no lot status of the opening. |
| CDC-18443 | RWB-S6-E5025-APP | GAP-1960 | 13 | Read the tape on the rwb-document contract and keep its reference only; building, masking, rejection and rebuild stay with RWB-S6-E5025-APP; tape object and field list recorded as unpublished. |

### OTHER:split_plan.json (wave map) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18502 | RWB-S6-E6001-APP | GAP-1965 |  | State in the wave map that rwb-debtsale delivers its EP05 keys in wave 3 and its EP06 keys in wave 4; this story keeps wave 4 and release 30 April 2027. |
| CDC-18522 | RWB-S6-E6001-CON | GAP-1965 | header | State that rwb-debtsale delivers its EP05 keys in wave 3 and its EP06 keys in wave 4; keep wave 4 and release 30 April 2027. |

### OTHER:Extract step, _work/msr/extract (S6 module pair) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18503 | RWB-S6-E6001-APP | GAP-1975 | n/a | Add the FSD S6 v3 and TSD S6 v2 pair to the extract for later stages; fill order of R7.3 unchanged. Story text has no extract reference. |
| CDC-18504 | RWB-S6-E6001-APP | GAP-1967 | n/a | Add the FSD S6 v3 and TSD S6 v2 pair to the extract for later stages; read the module documents directly for S6 stories. |

### OTHER:_work/msr/extract (extract folder) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18526 | RWB-S6-E6001-CON | GAP-1975 |  | Add the S6 module pair (FSD S6 Debt sale v3, TSD S6 Debt sale v2) to the extract for the later stages; the R7.3 fill order is unchanged. |
| CDC-18527 | RWB-S6-E6001-CON | GAP-1967 |  | Add the S6 module pair (FSD S6 Debt sale v3, TSD S6 Debt sale v2) to the extract for the later stages; the R7.3 fill order is unchanged. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18538 | RWB-S6-E6002-APP | CG-ALL-10461 | 12.5 | Add activity qualifyBuyer on task queue rwb-debtsale. |
| CDC-18539 | RWB-S6-E6002-APP | CG-ALL-10462 | 12.5 | Add the rule-package activity of rwb-decision on queue rwb-decision; its name is Not specified in the source documents (GAP-2984; ASM-4913). |

### RWB-S6-E6003-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18573 | RWB-S6-E6003-APP | DOR-RWB-S6-E6003-APP-21 | all | Publish the contract and set its build status to Done before this story is marked ready. |
| CDC-18581 | RWB-S6-E6003-APP | GAP-2987 |  | Publish one additive OpenAPI 3.1 fragment with the bar element embedded in the answers of API-S6-002 and API-S6-004, no provided operation, one envelope and one message ID per error condition, six consumed rows with the placeholders, the four closed lists, the two move names, the four route states, the window as a durable timer, eight fakes and five new contract tests; tag the baseline Draft and collect consumer sign-off. |

### RWB-S6-E5023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18366 | RWB-S6-E5023-APP | DOR-RWB-S6-E5023-APP-21 | Header | Build status must be Done before this story starts; it is currently Not started. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18375 | RWB-S6-E5023-APP | CG-ALL-10337 | 15 | Add empty, loading, error and no access states to section SCR-25. |

### RWB-S6-E5023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18384 | RWB-S6-E5023-CON | DOR-RWB-S6-E5023-CON-10 | find it | Add empty, loading, error and no-access states for SCR-25. |

### OTHER:Run extract folder _work/msr/extract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18392 | RWB-S6-E5023-CON | GAP-1949 | 18 | Add the FSD S6 Debt sale v3 and TSD S6 Debt sale v2 extracts; section 18 naming of these files is outside this chunk. |

### OTHER:FSD S6 (Recovery Workbench FSD S6; OTHER:A1.1 and the prerequisite lines of A2.1.2; OTHER:A2.3.2; OTHER:A2.5.2; OTHER:A2.10.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18393 | RWB-S6-E5023-CON | GAP-1789 | header | Map FEAT-DRI-07, FEAT-RDF-15, FEAT-APD-01 and FEAT-OCC-07 to the owning service contracts (P7 rules component and approval routing, P1 access control per data product, P6 template set) and add FEAT-DBS-05 and FEAT-DBS-16 to A1.1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18394 | RWB-S6-E5023-CON | GAP-1785 |  | State that the workflow state machine writes the routing-ladder value to state, and that the five-value LOV-LOT-STATUS is the business status; record both on the lot and never infer one from the other. |

### RWB-S6-E5024-CON; OTHER:S6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18410 | RWB-S6-E5024-APP | GAP-1773 | 1 | Keep API Specification v4 paths under /api/recovery/debtsale/v1; add the staff read of a lot's bids to the contract when the S6 contract story closes; slide 19 /lots is shorthand. |

### RWB-S6-E6005-APP; RWB-S6-E6006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18411 | RWB-S6-E5024-APP | GAP-2994 | 1 | Keep legacy AC1 to AC4 word for word; trace REQ-S6-006 with the TSD mapping difference recorded; name R-DS-23 and the agreement with RWB-S6-E6006-APP. |

### API:(service not named); OTHER:P1; OTHER:P10; OTHER:P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18420 | RWB-S6-E5024-CON | DOR-RWB-S6-E5024-CON-8 | 12.2 | Declare the REST bases of /api/recovery/case/v1, /source-data/v1, /agent/v1 and /decision/v1, as CG-ALL-10376 to CG-ALL-10379 require. |

### OTHER:FSD S6; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18421 | RWB-S6-E5024-CON | GAP-1770 | 8 | Carry the FSD field names as the rwb-source-data contract's returned names and build every read on that contract; confirm the P1 path (REST for the screen, activity in the workflow) before the wave 3 system test. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18433 | RWB-S6-E5025-APP | DOR-RWB-S6-E5025-APP-5 | 9 | Add LOT_APPROVED to the closed list LOV-LOT-STATUS, which the §9 transitions require. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-debtsale.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18434 | RWB-S6-E5025-APP | DOR-RWB-S6-E5025-APP-8 | n/a | Hold buyerClass, status and segment as references to LOV-BUYER-CLASS, LOV-LOT-STATUS and LOV-SEGMENT, not closed enums; align the DebtSaleWorkflow task queue and namespace with the catalog. |

### OTHER:Section 19 and the wave and release dates (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18444 | RWB-S6-E5025-APP | GAP-1976 | 13 | Owners of tape, award and transfer named in section 13; the release dates and wave stay unchanged. |

### RWB-S6-E6007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18458 | RWB-S6-E5026-APP | GAP-3004 | n/a | Keep plan H, C, I and X rows; build on Day 1 against six contract fakes; publish AccountsTransferred via platform outbox; track RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON as dependencies; serve transfer element on API-S6-002 and API-S6-004 answers; split R-DS-25 into one saga. |

### RWB-S6-E6003-APP; RWB-S6-E6003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18460 | RWB-S6-E5026-APP | GAP-2986 | n/a | Add C, I and X rows for the six consumed contracts, placeholders for panel operations, panel_status and lot status, and record the wave conflict once for the service and EP06. |

### RWB-S6-E6009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18461 | RWB-S6-E5026-APP | GAP-3008 | n/a | Keep H, C, I and X rows; declare the claim window as a versioned parameter with placeholders, and allocate the reporting contract in a later story. |

### RWB-S6-E6005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18464 | RWB-S6-E5026-APP | GAP-2994 | n/a | Keep the four legacy criteria word for word, name R-DS-04 and R-DS-23 with their sibling stories, and trace REQ-S6-006 with the TSD mapping difference recorded. |

### RWB-S6-E5025-APP; RWB-S6-E5026-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18465 | RWB-S6-E5026-APP | GAP-1976 | n/a | Add an H row for the tape between the two slices, keep wave and release values as they are, and record the two EP06 dates inside the service. |

### OTHER:_work/msr/extract (extract step; OTHER:Work Package B-S6-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18467 | RWB-S6-E5026-APP | GAP-1975 | none | Add the FSD S6 v3 and TSD S6 v2 module pair to the extract set for the later stages; the fill order of R7.3 is unchanged. |

### OTHER:Realignment plan; RWB-PLT-N001-CON; OTHER:path not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18480 | RWB-S6-E5026-CON | GAP-1959 | header | Add plan rows for the partner gateway (FAPI 2.0, DMZ) as route of the Partner portal operation of rwb-debtsale and for the rwb-partner buyer panel read; keep PT-BUYER RU and Partner portal R. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:edge story owner and S9 confirmation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18483 | RWB-S6-E5026-CON | GAP-1774 | 8 | Architecture admits buyers only through the partner gateway; the /partner path matches the API specification. Session termination needs edge owner and S9 confirmation. No story edit. |

### RWB-S6-E6004-CON; OTHER:T-A.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18484 | RWB-S6-E5026-CON | GAP-2989 | 4 | Publish the API-S6-005 baseline with placeholders, bind every error condition to one section 14 message ID, declare the Bid element with its storage split, confirm the three operation names and publish-first question with owners, and record the tag date in the contract README. |

### OTHER:Work Package B-S6-01 and extract set (_work/msr/extract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18486 | RWB-S6-E5026-CON | GAP-1975 | 1 | Read FSD S6 v3 and TSD S6 v2 from the requirements folders, keep the R7.3 fill order, and add the S6 module pair to the extract set for later stages. |

### OTHER:Extract set (_work/msr/extract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18487 | RWB-S6-E5026-CON | GAP-1961 | 1 | Add the S6 module extract before the baseline is tagged so a later diff is possible; use legacy FSD S6 v3 and TSD S6 v2 as the module source. |

### RWB-S6-E6001-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18492 | RWB-S6-E6001-APP | DOR-RWB-S6-E6001-APP-14 | find it | Record the signed epic design sign-off. Value: Not specified in the source documents (DOR-RWB-S6-E6001-APP-14) |

### RWB-S6-E6001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18493 | RWB-S6-E6001-APP | DOR-RWB-S6-E6001-APP-21 | n/a | Set build status to Done for the contract story RWB-S6-E6001-CON. |

### RWB-S6-E6001-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18498 | RWB-S6-E6001-APP | GAP-1963 |  | Add the five C rows (P7 approval chain, P7 rule-package read, P4 delegation_limit, P3 case state read, P3 case-move answer) and the rwb-decision queue dependency; the two operation names are Not specified in the source documents (GAP-1963). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:25; OTHER:26) and FSD S6 (A2.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18499 | RWB-S6-E6001-APP | GAP-1780 |  | Run DebtSaleWorkflow as the case stage workflow for eligibility and case-side steps and as the lot saga for sale steps, lot identified by lot number; rwb-case moves the case on LotAwarded and AccountsTransferred. |

### OTHER:Work Package B-S6-01 workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18501 | RWB-S6-E6001-APP | GAP-1976 |  | Add an H row for RWB-S6-E5025-APP (masked data tape) between lanes L-S6-C and L-S6-D; keep the plan's wave and release values and record the two EP06 dates in the service. |

### OTHER:rwb-access delegation-limit publication (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18506 | RWB-S6-E6001-APP | GAP-2983 | 8 | Publish the committee approver level and its delegation limits; the approval chain then names the authority this story writes. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:37 and 45 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18513 | RWB-S6-E6001-CON | GAP-1770 | find it | Replace v_ace_batch_status, v_ace_score and ACE reads with the rwb-source-data contract field names (v_ace_score.*, v_ace_account.*, v_ace_batch_status.*); confirm P1 path before wave 3 system test. |

### OTHER:P3 screen specification for SCR-25 and SCR-26 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18515 | RWB-S6-E6001-CON | DOR-RWB-S6-E6001-CON-10 | find it | Add empty, loading, error and no-access states for SCR-25 and SCR-26. |

### OTHER:FSD S6 A2.5.3.2 and TSD S6 T8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18523 | RWB-S6-E6001-CON | GAP-1968 |  | Add payment_terms and status to the FSD field catalog from TSD S6 T3.1; align the FEAT-DBS-05 requirement mapping with the TSD; state the approval as a case route state. |

### OTHER:rwb-decision and rwb-case contract documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18524 | RWB-S6-E6001-CON | GAP-2980 |  | Publish the DS rule-package read operation name, the case-move answer operation name and the committee decide act form; then remove the R9 placeholders. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; RWB-S6-E6001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18528 | RWB-S6-E6001-CON | GAP-2981 |  | Add five C rows: rwb-decision approval chain, rwb-decision rule package, rwb-access DoA limit, rwb-case state read, rwb-case move answer. |

### OTHER:rwb-access (service RBAC matrix and DoA rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18529 | RWB-S6-E6001-CON | GAP-2983 |  | Publish the Credit approval committee member level and its delegation limits; the approval chain then names the authority this story writes. |

### RWB-S6-E6002-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18531 | RWB-S6-E6002-APP | DOR-RWB-S6-E6002-APP-21 | header | Set build status to Done. |

### OTHER:Context pack and TSD S6 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18544 | RWB-S6-E6002-APP | GAP-2984 | 12 | Add the rwb-debtsale to rwb-partner arrow for the buyer read and publish named operations for the buyer read, case move and package; raise the bid table for the DB story |

### OTHER:_work/msr/extract (extract set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18545 | RWB-S6-E6002-APP | GAP-1975 | 7 | Add FSD S6 Debt sale v3 and TSD S6 Debt sale v2 extracts for the later stages; keep the R7.3 fill order unchanged. Story reads the legacy files meanwhile. |

### OTHER:Split plan and TSD S6 v2 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18560 | RWB-S6-E6002-CON | GAP-1970 | find it | Record the award path and data room read rows as RWB-S6-E6005-APP and RWB-S6-E5026-APP; ask the API owner whether a qualification read is added to T-A. |

### OTHER:Platform and S9 owners, edge register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18562 | RWB-S6-E6002-CON | GAP-1971 | find it | Place the partner gateway channel as a missing edge row for the buyer read by a partner identity; keep the X row at None. |

### OTHER:TSD S6 v2 T3.1 and data steward (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18563 | RWB-S6-E6002-CON | GAP-1974 | find it | Add bid amount, bid time, bid reference and bid window columns to debt_sale_lot or debt_sale_account before the award story needs the amount. |

### OTHER:Work Package B-S6-01 and the extract step (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18565 | RWB-S6-E6002-CON | GAP-1975 | none | Read FSD S6 v3 and TSD S6 v2 from the requirements folders, keep the R7.3 fill order and add the S6 module pair to the extract for later stages. |

### OTHER:Gap register entry for S6 and EP06 (wave conflict) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18566 | RWB-S6-E6002-CON | GAP-1972 | none | Record once for S6 and EP06 that the W-MAP wave 4 differs from the Architecture v5 rwb-debtsale wave 3; the story keeps wave 4 and builds on Day 1. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18611 | RWB-S6-E6004-APP | GAP-1771 | 12.7 | Add Ownership Map rows for bid, buyer terms, data room state, award and transfer as entity groups; name physical tables in the S6 DB story |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18612 | RWB-S6-E6004-APP | GAP-1773 | 12 | Publish the five operations under /api/recovery/debtsale/v1, carry /lots as shorthand, add the staff bid read |

### OTHER:Edge owner; OTHER:S9 session termination (source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18613 | RWB-S6-E6004-APP | GAP-1774 | 8 | BR8 keeps the partner-gateway assertion; session termination with S9 remains open |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18615 | RWB-S6-E6004-APP | GAP-1787 | 15 | Name the screen owner of SCR-26 and PRT-05 and route SCR-25 through gateway-bff composite routes and the partner gateway. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1484 | The debt sale service wave is earlier than the business epic wave that awards a lot | Solution architect | Resolved (directive) |
| GAP-1770 | FSD S6 reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them and gives S6 no cell to P1 | Solution architect | Resolved (directive) |
| GAP-1771 | The Ownership Map and the physical schema give this service two tables, while Architecture v5 gives it six things to hold | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1773 | The lot API is named /lots on slide 19 and /debt-sale-lots in the API specification, and no staff read of the bids exists | Solution architect | Resolved (directive) |
| GAP-1774 | The buyer data room is published under /partner, while the architecture admits buyers only through the partner gateway and S6 has no cell to S9 | Solution architect | Resolved (directive) |
| GAP-1780 | DebtSaleWorkflow is a saga per lot across five services, while the v5 case model is one child workflow per case per stage | Solution architect | Resolved (directive) |
| GAP-1781 | The monthly sale cycle has no schedule and no job row | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1783 | The PII service the tape depends on is not one of the 19 services and has no owner | Solution architect | Resolved (directive) |
| GAP-1784 | The model gateway and the lot agent estimate have no owner among the 19 services | Solution architect | Resolved (directive) |
| GAP-1785 | Two state vocabularies describe the same lot: the routing ladder and the status list | Data architect | Resolved (directive) |
| GAP-1787 | The three screens have no owner in the sources read | Solution architect | Resolved (directive) |
| GAP-1788 | No source states who owns the wording of the debt sale messages and their Thai and English versions | Business analyst, S6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1789 | The FSD's prerequisite feature codes belong to four other modules and two of its own features are missing from its dependency list | Solution architect | Resolved (directive) |
| GAP-1947 | RWB-S6-E5023: the eligibility slice has no C row for its four consumed rows, no DP-04 row and no requirement id | Solution architect | Resolved (directive) |
| GAP-1948 | RWB-S6-E5023: the service owns a topic and two events while DP-09 and its outbox library are absent from the plan | Solution architect | Resolved (directive) |
| GAP-1949 | RWB-S6-E5023: the run's extract folder holds no FSD or TSD extract for module S6, so the module files stand in | Business analyst | Resolved (directive) |
| GAP-1950 | RWB-S6-E5023: the 54 percent cap named in legacy AC1 is carried by R-DS-19, whose criterion and test belong to RWB-S6-E6005-APP | Business analyst | Resolved (directive) |
| GAP-1951 | RWB-S6-E5023: the eligibility inputs deviation_open and fraud_flag have no named owner, field or contract row | Solution architect | Resolved (directive) |
| GAP-1952 | RWB-S6-E5024: the lot build and price step needs rwb-source-data, rwb-agent, rwb-case and rwb-decision while the plan's C row is empty | Solution architect | Resolved (directive) |
| GAP-1953 | RWB-S6-E5024: the price estimate is an rwb-agent pricing-agent call with no DP-20 row in the plan and no published operation | Solution architect | Resolved (directive) |
| GAP-1954 | RWB-S6-E5024: the COLLINS lot economics are the legacy v_ace_score view, which no service but rwb-source-data may read | Solution architect | Resolved (directive) |
| GAP-1955 | RWB-S6-E5024: the run's extract folder holds no FSD S6 or TSD S6 module extract, so the legacy module files stand in | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1956 | RWB-S6-E5024: R-DS-04 produces the priced lot and the committee state, but its criterion is owned by RWB-S6-E6001-APP AC3 | Business analyst | Resolved (directive) |
| GAP-1957 | RWB-S6-E5024: no source gives the minimum lot size, the reserve basis, the payment-terms ladder or the buyer-class rule, and LOV-LOT-STATUS has no priced value while SCR-25 declares a priced state | Business analyst | Resolved (directive) |
| GAP-1958 | RWB-S6-E5026: the data-room slice carries an empty C row although it needs rwb-document, rwb-partner and rwb-case, and the plan holds no requirement id | Solution architect | Resolved (directive) |
| GAP-1959 | RWB-S6-E5026: the partner channel of the data-room read has no plan row and the right is stated twice with different holders | Solution architect | Resolved (directive) |
| GAP-1960 | RWB-S6-E5026: the masked tape is another story's deliverable and its masking rules belong to the PII service and rwb-access | Solution architect | Resolved (directive) |
| GAP-1961 | RWB-S6-E5026: the extract folder holds no FSD or TSD extract for module S6, so the legacy module files stand in | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1962 | RWB-S6-E5026: the data room has no table of its own, the lot status the opening writes is unnamed and the properties the partner read withholds are unstated | Solution architect | Resolved (directive) |
| GAP-1963 | RWB-S6-E6001: the plan gives this step an empty C row while it consumes rwb-decision, rwb-access and rwb-case, and two of the consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1964 | RWB-S6-E6001: the approval chain runs on P7's ApprovalWorkflow while the story's own workflow is the DebtSaleWorkflow saga, and the sources name one approval act where the Ownership Map names three | Solution architect | Resolved (directive) |
| GAP-1965 | RWB-S6-E6001: EP06 puts the story in wave 4 and release 30 April 2027 while rwb-debtsale is an Arch v5 wave 3 service | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1966 | RWB-S6-E6001: the award operation and the A right are rowed as this story's although the award belongs to RWB-S6-E6005-APP, and the committee approver of the FSD has no role row | Solution architect | Resolved (directive) |
| GAP-1967 | RWB-S6-E6001: the extract folder holds no FSD or TSD file for S6 Debt sale, so the module documents stand in for the extract | Run lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1968 | RWB-S6-E6001: the FSD field catalog omits two lot fields, the lot status list carries no approved value, and the requirement mapping of the approval differs between the FSD and the TSD | Solution architect | Resolved (directive) |
| GAP-1969 | RWB-S6-E6002: the qualification slice has no C row, no requirement id and no case-move or authorise operation although it needs rwb-partner, rwb-case, rwb-decision and rwb-access | Solution architect | Resolved (directive) |
| GAP-1970 | RWB-S6-E6002: TSD S6 T-A publishes no KYC operation and the two legacy endpoint rows belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP | Solution architect | Resolved (directive) |
| GAP-1971 | RWB-S6-E6002: the partner channel that reads the qualification has no plan row, no story and no X row, and its gateway sits in the DMZ | Solution architect | Resolved (directive) |
| GAP-1972 | RWB-S6-E6002: the story is EP06 wave 4 while rwb-debtsale is created in wave 3 | Delivery lead | Resolved (directive) |
| GAP-1973 | RWB-S6-E6002: the extract folder holds no FSD or TSD S6 text, so the legacy module files stand in as the module sources | Business analyst | Resolved (directive) |
| GAP-1974 | RWB-S6-E6002: the bid has no contracted column set on debt_sale_lot or debt_sale_account although R-DS-18 records a bid against the lot and the buyer | Data steward | Resolved (directive) |
| GAP-1975 | WP B-S6-01: the extract folder holds no FSD or TSD file for the S6 Debt sale module, so the rule-of-fill sources are read from the module documents themselves | Run lead | Resolved (directive) |
| GAP-1976 | WP B-S6-01: the data-room story publishes a masked tape that no story of this Work Package builds, and the EP06 keys carry release 30 April 2027 against a wave 3 service | Solution architect | Resolved (directive) |
| GAP-2018 | Strict-mode wait at a point of no return is not defined in this design | Service owner P7 rwb-decision with the saga owners S2, S5, S6 and S7 | Resolved (directive) |
| GAP-2973 | RWB-S6-E5023-APP: the eligibility slice has no plan row for its four consumed contracts, its outbox library, its rule kit, the 54 percent cap criterion or the two eligibility inputs | Solution architect | Resolved (directive) |
| GAP-2974 | RWB-S6-E5023-CON: the consumed operation names, the case boundary element, the event names and the field-level types of the two lot operations have no published baseline | Solution architect | Resolved (directive) |
| GAP-2975 | RWB-S6-E5024-APP: the lot build and price slice has no plan row for its four consumed contracts, its agent contract, the R-DS-04 criterion split, the rules that carry no value or the outbox library | Solution architect | Resolved (directive) |
| GAP-2976 | RWB-S6-E5024-CON: the priced properties, the agent estimate element, the four consumed operation names and the field list of the COLLINS lot economics have no published baseline | Solution architect | Resolved (directive) |
| GAP-2977 | RWB-S6-E5026-APP: the data-room slice has no plan row for its three consumed contracts, its partner channel or the lot status of the opening | Solution architect | Resolved (directive) |
| GAP-2978 | RWB-S6-E5026-CON: the consumed operation names, the tape element, the panel fields, the lot status and the event set of the data room have no published baseline | Solution architect | Resolved (directive) |
| GAP-2980 | Approval, rule-package and case-move operation names are not published | Solution architect | Resolved (directive) |
| GAP-2981 | Plan contract-dependency row is empty while five cross-service contracts are consumed | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2982 | No event is published in this key although the service owns EV-23 | Solution architect | Resolved (directive) |
| GAP-2983 | Committee approver has no row in the service RBAC matrix and no published DoA row | Access and authority owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2984 | RWB-S6-E6002-APP: the qualification step has no operation, no bid table, no published names for the buyer read, the case move and the package, and no partner arrow in the connection matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2985 | RWB-S6-E6002-CON: the qualification, buyer and bid elements have no published schema, no bid home, no provided operation and no published names for the consumed rows | Solution architect | Resolved (directive) |
| GAP-2986 | RWB-S6-E6003-APP: the bar slice has no plan row for its six consumed contracts, no published bar operation, no panel or lot-status vocabulary, no next-bidder field and no window row | Solution architect with the owners of rwb-partner, rwb-case, rwb-access and rwb-decision | Resolved (directive) |
| GAP-2987 | RWB-S6-E6003-CON: the bar baseline has no published operation, no panel or release value, no move and timer vocabulary and no field-level types in any source | Solution architect with the owners of rwb-partner, rwb-case, rwb-access and rwb-decision | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2988 | RWB-S6-E6004-APP: the take-bids slice has no plan row for its five consumed contracts, its guard and outbox libraries, the publish-first story of API-S6-005, the bid and realised-recovery columns, the two rules it shares with sibling keys, the reporting destination of R-DS-34, its wave or its requirement id | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2989 | RWB-S6-E6004-CON: the bid operation has no field-level baseline, the consumed operation names are unpublished, the publish-first story of API-S6-005 is contested, the bid fact has no column set and the step has no event, Schedule or requirement row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2994 | RWB-S6-E6005: the four legacy criteria span three sibling stories, R-DS-23 confirms the award, and the requirement mapping differs between the FSD and the TSD | Business analyst | Resolved (directive) |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3008 | RWB-S6-E6009-APP: the put-back review has no published operation, its claim window, claim reason and realized-recovery figure have no field, column or event, its consumed contracts have no plan row, and two of its four criteria execute rules owned by sibling stories | Solution architect | Resolved (directive) |
| GAP-3014 | RWB-S6-E5025: the masking rule set, the tape layout, the tape's storage reference, the PII service mapping and the six consumed contracts are given by no source and sit outside the plan's empty C row | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S6-E5023-APP | table cell count | 287 | 3 cells, header has 4: \| `deviation_open`, `fraud_flag` \| the eligibility inputs of R-DS-01 and R-DS-02 \| Consumed rule inputs of the rwb-case |
