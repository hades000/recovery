# RWB-SVC-S6 rwb-debtsale (Debt sale) - review pack, part 3 of 3 (RWB-S6-E6012-APP to RWB-S6-E6012-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 1 |
| Resolved in the stories | 20 |
| Cross-document (pending in another document) | 15 |
| Not applied (value not in the sources) | 0 |
| Open business decisions | 3 |
| Register gaps linked | 2 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S6-E6012-APP | 20 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6012 APP Apply the debt sale cap v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S6-E5023-APP, RWB-S6-E5023-CON, RWB-S6-E6012-APP | R-09247 | GAP-1473 | Register gap | Head of Asset Liquidity | The debt sale cap is stated as a percentage with no basis, period or measurement | Hold the cap as a versioned policy parameter with its basis and period in the version label, compute headroom against the population the policy names, and report the version used with each lot. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-S6-E6005-APP, RWB-S6-E6012-APP | R-23244 | GAP-3015 | Register gap | Solution architect with the owners of rwb-case (P3), rwb-decision (P7), rwb-access (P4) and rwb-source-data (P1), and the business owner of the debt sale cap | RWB-S6-E6012-APP: the cap slice has no plan row for the five consumed contracts, no cap parameter row, no cap route rule, no published trigger, no headroom column and no service contract baseline | Publish the five consumed operations with their fake; add C rows for rwb-case, rwb-decision, rwb-access and rwb-source-data; add the DP-04, DP-06, DP-07, DP-08 and DP-09 rows the tables need; name the cap row, its version, its basis and its owner; publish one route rule for the cap or confirm that R-DS-19 and R-DS-23 are its only test and which story owns them; publish the trigger or confirm the call from the lot build and award steps; add the cap-position and headroom fields or confirm the decision record as their only home; create the service contract baseline for this legacy key; and carry REQ-S6-001 and BR-050 in the plan |
| RWB-S6-E5023-APP, RWB-S6-E5023-CON, RWB-S6-E6012-APP | R-23578 | GAP-1777 | Register gap | Head of Asset Liquidity | The debt sale cap has no basis and no period, only a figure | Hold the cap, its denominator and its period as one versioned reference-data row with the role that owns it, and record the version applied at the selection, the award and the headroom report. |

## 4. Not applied (the value is not in the source documents)

None.

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18881 | RWB-S6-E6012-APP | CG-ALL-10822 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case, as given in the Document Index service table. |
| CDC-18882 | RWB-S6-E6012-APP | CG-ALL-10823 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case, as given in the Document Index service table. |
| CDC-18883 | RWB-S6-E6012-APP | CG-ALL-10824 | 12.2 | Declare REST base /api/recovery/source-data/v1 for provider P1 rwb-source-data, as given in the Document Index service table. |
| CDC-18884 | RWB-S6-E6012-APP | CG-ALL-10825 | 12.2 | Declare REST base /api/recovery/decision/v1 for provider P7 rwb-decision, as given in the Document Index service table. |
| CDC-18885 | RWB-S6-E6012-APP | CG-ALL-10826 | 12.2 | Declare REST base /api/recovery/access/v1 for provider P4 rwb-access, as given in the Document Index service table. |
| CDC-18889 | RWB-S6-E6012-APP | DOR-RWB-S6-E6012-APP-8 | 12 | Add the base paths /api/recovery/case/v1, /source-data/v1, /decision/v1, /access/v1 and the three further bases in the detcheck. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18890 | RWB-S6-E6012-APP | CG-ALL-10820 | 8 | Record account_id as a field of debt_sale_account, or name the dictionary field the story should use. |
| CDC-18891 | RWB-S6-E6012-APP | CG-ALL-10821 | 12.7 | Record case_list as the P3 object the story reads, or name the dictionary field the story should use. |
| CDC-18894 | RWB-S6-E6012-APP | DOR-RWB-S6-E6012-APP-7 | 11 | Register account_id as a field of debt_sale_account and case_list as a field or entity of the case set, or name the held field. P3 wording fixed under item 7. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18886 | RWB-S6-E6012-APP | DOR-RWB-S6-E6012-APP-14 | header | Confirm and record the signed epic design sign-off for this story's epic, since none is in the story or source documents. |

### RWB-PLT-E1027-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18887 | RWB-S6-E6012-APP | DOR-RWB-S6-E6012-APP-21 | header | Reach Done so that the contract this story depends on is published; this story has no contract story of its own. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18888 | RWB-S6-E6012-APP | DOR-RWB-S6-E6012-APP-22 | header | Publish a fake library version for the contracts faked in section 12.2 (rwb-case, rwb-source-data, rwb-decision, rwb-access reads). |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18892 | RWB-S6-E6012-APP | CG-ALL-10829 | 12.5 | Add activity applyDebtSaleCap to the Activities sheet. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18893 | RWB-S6-E6012-APP | CG-ALL-10831 | 16 | Add rows TC-E6-012-01 to TC-E6-012-04 with Given, When and Then copied from the criteria they cover. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18895 | RWB-S6-E6012-APP | GAP-1781 | find it | Add a job row for the monthly sale cycle opener: a Temporal Schedule or event-started workflow on rwb-debtsale through the workflow kit, with its owner, run book and the cycle date it ran for. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1781 | The monthly sale cycle has no schedule and no job row | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1785 | Two state vocabularies describe the same lot: the routing ladder and the status list | Data architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
