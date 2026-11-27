# RWB-SVC-P10 rwb-agent (Agent) - review pack, part 2 of 3 (RWB-P10-E1063-CON to RWB-P10-E2031-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 225 |
| Cross-document (pending in another document) | 226 |
| Not applied (value not in the sources) | 15 |
| Open business decisions | 12 |
| Register gaps linked | 61 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P10-E1063-CON | 18 | 20 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1063 CON Agent monitoring dashboard v1 [E2c] - contract v2.md |
| RWB-P10-E1063-OPS | 14 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1063 OPS Agent monitoring dashboard v1 [E2c] - deployment v2.md |
| RWB-P10-E2028-APP | 22 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2028 APP Case intake agent live at L1 [E3a] v2.md |
| RWB-P10-E2028-CON | 19 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2028 CON Case intake agent live at L1 [E3a] - contract v2.md |
| RWB-P10-E2028-OPS | 20 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2028 OPS Case intake agent live at L1 [E3a] - deployment v2.md |
| RWB-P10-E2029-APP | 29 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v2.md |
| RWB-P10-E2029-CON | 22 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2029 CON Deviation screening agent evaluation and L1 on one segment [E3b] - contract v2.md |
| RWB-P10-E2030-APP | 20 | 24 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2030 APP Legal document agent in shadow on Epic 1 data [E3c] v2.md |
| RWB-P10-E2030-CON | 17 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2030 CON Legal document agent in shadow on Epic 1 data [E3c] - contract v2.md |
| RWB-P10-E2031-APP | 28 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2031 APP Agent monitoring dashboard v2 [E3d] v2.md |
| RWB-P10-E2031-CON | 16 | 20 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2031 CON Agent monitoring dashboard v2 [E3d] - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P10-E1063-CON | R-09894 | CG-ALL-2667 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2028-APP | R-09903 | CG-ALL-2686 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2028-CON | R-09907 | CG-ALL-2701 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2029-CON | R-09918 | CG-ALL-2738 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2030-APP | R-09924 | CG-ALL-2756 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2030-CON | R-09930 | CG-ALL-2775 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2031-CON | R-09945 | CG-ALL-2803 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-ITG-E2029-ITG, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P7-E2029-APP, RWB-S8-E2029-APP | R-22656 | GAP-1828 | Register gap | Risk and model risk officer | The confidence threshold for the low-confidence review and the evidence required to run the agent at L1 are not stated | Read the threshold and the autonomy policy from versioned reference data held by rwb-agent and rwb-decision, assert no number, and leave the evidence pack and the approval of a level change to Q-014 and BR-084. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E1063-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P4-E1063-APP, RWB-P6-E1063-APP | R-28650 | GAP-1213 | Register gap | data steward, data product owner and architecture owner | REQ-DRI-009 still requires a daily copy to the data lake, which DP-17 and Arch v5 slide 37 remove | Reword REQ-DRI-009 in the next BRD version as the daily agent measures being available for reporting from rwb-reporting with the row counts matched against the P10 source, keep the requirement identifier, and record that the P6 slice carries only the cost-alert notification, as ASM-B-P6-05-E1063-6 sets out. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P10-E1063-CON | R-04619 | DOR-RWB-P10-E1063-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (searched 'epic design'). A sign-off cannot be created by a text edit; it needs the epic design record. |
| RWB-P10-E1063-CON | R-15360 | DOR-RWB-P10-E1063-CON-11 |  | Definition of Ready item 11 Guardrails: Partial | Rests on CG-ALL-2667, a removed business decision (business_deferred.jsonl, Compliance). The flagged field is not identified in the sources. |
| RWB-P10-E1063-CON | R-22225 | GAP-0617 | 7, 11, 12 | Agent monitoring contract in rwb-agent: the page size and cursor, the member types of the aggregate element, the held-date status members, the Schedule name, the route path and the notification operation are not specified | Schedule name is not in the sources, so it stays Not specified (GAP-0617; ASM-0895). No agent page size, cursor, types or route path found. P6-E1063-APP cites a case-scoped send for a non-case alert. |
| RWB-P10-E2028-APP | R-04629 | DOR-RWB-P10-E2028-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off for RWB-SVC-P10 found in the source documents; searched all .md files. Cannot confirm sign-off without a record. |
| RWB-P10-E2028-APP | R-15373 | DOR-RWB-P10-E2028-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Story §11 text not in this chunk, so no exact old text to edit. Source Data Classification v5 marks DF-CAS-009 owner_user_id and DF-WRK-012 assignee_user_id as personal data (Yes). created_by not found there. |
| RWB-P10-E2028-APP | R-15379 | DOR-RWB-P10-E2028-APP-7 | 11 | Definition of Ready item 7 Data: Partial | Completeness of the data set is not verifiable from the sources; the item stays open. |
| RWB-P10-E2029-APP | R-04645 | DOR-RWB-P10-E2029-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design found in the source documents or EP03 export. Sign-off cannot be invented. Not specified in the source documents (DOR-RWB-P10-E2029-APP-14). |
| RWB-P10-E2030-APP | R-04656 | DOR-RWB-P10-E2030-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources. Searched the requirements .md files, 23 Document Gaps and the story. Sign-off must come from the epic design record. |
| RWB-P10-E2030-APP | R-04657 | DOR-RWB-P10-E2030-APP-16 | header | Definition of Ready item 16 Size: Fail | No size value is in the sources, so the item stays open until refinement. |
| RWB-P10-E2030-APP | R-09919 | CG-ALL-2748 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 404 an unknown version or evaluation; 503 the store or a consumed contract unavailable. No operation of this story returns the pack or the completeness list (BR1) | Standard v4 has no ID for 401 or 404. MSG-GEN-006 says the request is queued and retried, which this story does not do. Business analyst to confirm the 503 mapping. |
| RWB-P10-E2030-APP | R-15411 | DOR-RWB-P10-E2030-APP-15 | header | Definition of Ready item 15 INVEST: Partial | Whether the story is Small cannot be shown until the squad sizes it at refinement. |
| RWB-P10-E2030-CON | R-04662 | DOR-RWB-P10-E2030-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for E3c, P10 or E2030 exists in the sources. Prior search of folders 01 to 09 found none, and a broad 'epic design' grep returned only scratch and disposition files. A sign-off cannot be invented, so the story is unchanged. |
| RWB-P10-E2031-APP | R-15427 | DOR-RWB-P10-E2031-APP-15 | header | Definition of Ready item 15 INVEST: Partial | No source shows the story fits within two weeks; the Size row says it is not sized and the point value is Not specified in the source documents. |
| RWB-P10-E2031-CON | R-04672 | DOR-RWB-P10-E2031-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design sign-off exists in the story or sources (RWB-SVC-P10 Epic Overview v1, DoR review). A sign-off cannot be invented; the epic design owner must supply it. |
| RWB-P10-E2031-CON | R-24611 | CG-ALL-2804 | 12.7 | Flyway file V10_007__agent_monitor_index.sql is not in the V0001..Vnnnn form | No next Vnnnn for rwb-agent found in Service Template Spec v1 s3 or folders 03-06 (grepped). Renaming would invent a number. Solution architect to confirm the sequence number. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (39)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03927 | RWB-P10-E1063-CON | CG-ALL-2658 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-metrics in rwb-agent.yaml, or remove the operation from RWB-P10-E1063-CON section 12.1. |
| CDC-03929 | RWB-P10-E1063-CON | DOR-RWB-P10-E1063-CON-8 | find it | Publish GET /api/recovery/agent/v1/admin/agent-metrics in rwb-agent.yaml (CG-ALL-2658). |
| CDC-04047 | RWB-P10-E2030-APP | CG-ALL-2740 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-samples in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04048 | RWB-P10-E2030-APP | CG-ALL-2741 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-evaluations in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04049 | RWB-P10-E2030-APP | CG-ALL-2742 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-evaluations in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04050 | RWB-P10-E2030-APP | CG-ALL-2743 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04051 | RWB-P10-E2030-APP | CG-ALL-2744 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04052 | RWB-P10-E2030-APP | CG-ALL-2745 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04053 | RWB-P10-E2030-APP | CG-ALL-2746 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-configs in rwb-agent.yaml through RWB-P10-E1058-CON or RWB-P10-E1061-CON, whichever baselines it. |
| CDC-04057 | RWB-P10-E2030-APP | DOR-RWB-P10-E2030-APP-8 |  | Add the section 12.1 paths missing from the file: POST and GET agent-evaluations, GET agent-evaluations/{evaluationId}/report, agent-samples and the other listed paths (+10 more). |
| CDC-04071 | RWB-P10-E2030-CON | CG-ALL-2758 | 12.1 | Publish POST /api/recovery/agent/v1/agent-runs in rwb-agent.yaml as RWB-P10-E2030-CON section 12.1 provides it. |
| CDC-04072 | RWB-P10-E2030-CON | CG-ALL-2759 | 12.1 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent.yaml as RWB-P10-E2030-CON section 12.1 provides it. |
| CDC-04073 | RWB-P10-E2030-CON | CG-ALL-2760 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-samples in rwb-agent.yaml as RWB-P10-E2030-CON section 12.1 provides it. |
| CDC-04074 | RWB-P10-E2030-CON | CG-ALL-2761 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-evaluations in rwb-agent.yaml as RWB-P10-E2030-CON section 12.1 provides it. |
| CDC-04075 | RWB-P10-E2030-CON | CG-ALL-2762 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-evaluations in rwb-agent.yaml as RWB-P10-E2030-CON section 12.1 provides it. |
| CDC-04076 | RWB-P10-E2030-CON | CG-ALL-2763 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report in rwb-agent.yaml as section 12.1 provides it. |
| CDC-04077 | RWB-P10-E2030-CON | CG-ALL-2764 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs and POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve in rwb-agent.yaml as section 12.1 provides them. |
| CDC-04079 | RWB-P10-E2030-CON | DOR-RWB-P10-E2030-CON-8 | 12.1 | Add the paths the detcheck names as missing: POST and GET agent-runs, POST admin/agent-samples, POST admin/agent-evaluations and the further paths the detcheck lists. |
| CDC-04111 | RWB-P10-E2031-CON | CG-ALL-2793 | 12.1 | Add operation GET /api/recovery/agent/v1/admin/agent-metrics to the paths of rwb-agent.yaml. |
| CDC-04113 | RWB-P10-E2031-CON | DOR-RWB-P10-E2031-CON-8 | 12.3 | Add GET /api/recovery/agent/v1/admin/agent-metrics; Temporal workflow and activity rows per Temporal Catalog v1. |
| CDC-20659 | RWB-P10-E1063-CON | R-00472 |  | GET /admin/agent-metrics is already in rwb-agent.yaml (operationId getAdminAgentMetrics). |
| CDC-20660 | RWB-P10-E1063-CON | R-04622 |  | GET /admin/agent-metrics is already in rwb-agent.yaml (operationId getAdminAgentMetrics). |
| CDC-20661 | RWB-P10-E2030-APP | R-00489 |  | POST /admin/agent-samples is already in rwb-agent.yaml (operationId postAdminAgentSamples). |
| CDC-20662 | RWB-P10-E2030-APP | R-00490 |  | POST /admin/agent-evaluations is already in rwb-agent.yaml (operationId postAdminAgentEvaluations). |
| CDC-20663 | RWB-P10-E2030-APP | R-00491 |  | GET /admin/agent-evaluations is already in rwb-agent.yaml (operationId getAdminAgentEvaluations). |
| CDC-20664 | RWB-P10-E2030-APP | R-00492 |  | GET /admin/agent-evaluations/{evaluationId}/report is already in rwb-agent.yaml. |
| CDC-20665 | RWB-P10-E2030-APP | R-00493 |  | POST /admin/agent-configs is already in rwb-agent.yaml (operationId postAdminAgentConfigs). |
| CDC-20666 | RWB-P10-E2030-APP | R-00494 |  | POST /admin/agent-configs/{versionId}/approve is already in rwb-agent.yaml. |
| CDC-20667 | RWB-P10-E2030-APP | R-00495 |  | GET /admin/agent-configs is already in rwb-agent.yaml (operationId getAdminAgentConfigs). |
| CDC-20698 | RWB-P10-E2030-CON | R-04665 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20700 | RWB-P10-E2030-CON | R-00501 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20701 | RWB-P10-E2031-CON | R-00508 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20702 | RWB-P10-E2030-CON | R-00499 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20703 | RWB-P10-E2030-CON | R-00500 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20704 | RWB-P10-E2030-CON | R-00502 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20705 | RWB-P10-E2030-CON | R-00503 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20706 | RWB-P10-E2031-CON | R-04674 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20707 | RWB-P10-E2030-CON | R-00504 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20709 | RWB-P10-E2030-CON | R-00498 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03947 | RWB-P10-E1063-OPS | CG-ALL-2670 | 12.5 | Add workflow AgentRunDailyRollupWorkflow to the Workflows sheet, or name the catalogued workflow to use. Catalogued name Not specified in the source documents (CG-ALL-2670). |
| CDC-03952 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-8 | 12.5 | Add AgentRunDailyRollupWorkflow to Workflows; add aggregateAgentRuns, raiseCostAlerts and dispatchAgentAlerts to Activities, all on task queue rwb-agent. |
| CDC-03954 | RWB-P10-E1063-OPS | CG-ALL-2671 | 12.5 | Add activity aggregateAgentRuns to the Activities sheet on task queue rwb-agent, or name a catalogued activity to use instead. |
| CDC-03955 | RWB-P10-E1063-OPS | CG-ALL-2672 | 12.5 | Add activity raiseCostAlerts to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03956 | RWB-P10-E1063-OPS | CG-ALL-2673 | 12.5 | Add activity dispatchAgentAlerts to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03977 | RWB-P10-E2028-APP | CG-ALL-2683 | 12.5 | Add an Activities row for ResolveIntakeMode on task queue rwb-agent, or name a catalogued activity. |
| CDC-03978 | RWB-P10-E2028-APP | CG-ALL-2684 | 12.5 | Add an Activities row for RecordIntakeFeedback on task queue rwb-agent, or name a catalogued activity. |
| CDC-03988 | RWB-P10-E2028-CON | CG-ALL-2697 | 12.5 | Add activity ResolveIntakeMode on task queue rwb-agent to the Activities sheet. |
| CDC-03989 | RWB-P10-E2028-CON | CG-ALL-2698 | 12.5 | Add activity RecordIntakeFeedback on task queue rwb-agent, as the one-transaction workflow kit activity of section 12.5 |
| CDC-04015 | RWB-P10-E2029-APP | DOR-RWB-P10-E2029-APP-8 | 12.5 | Add activity ResolveScreeningMode (rwb-agent, queue rwb-agent) and state the Workflow ID form of AgentRunWorkflow. |
| CDC-04019 | RWB-P10-E2029-APP | CG-ALL-2719 | 12.5 | Add ResolveScreeningMode on task queue rwb-agent with the contract element stated in section 12.5. |
| CDC-04033 | RWB-P10-E2029-CON | CG-ALL-2731 | 12.5 | Add an Activities row for ResolveScreeningMode on task queue rwb-agent with output mode L1 or SHADOW, the policy version, the matched segment or a refusal, or name a catalogued activity that gives the same output. |
| CDC-04058 | RWB-P10-E2030-APP | CG-ALL-2752 |  | Add Activities row AssembleLegalPackInputs on queue rwb-agent with the input and output in section 12.5. |
| CDC-04059 | RWB-P10-E2030-APP | CG-ALL-2753 |  | Add Activities row ScoreLegalPack on queue rwb-agent with the input and output in section 12.5. |
| CDC-04081 | RWB-P10-E2030-CON | CG-ALL-2770 | 12.5 | Add an Activities row AssembleLegalPackInputs on task queue rwb-agent with input and output as in RWB-P10-E2030-CON section 12.5. |
| CDC-04082 | RWB-P10-E2030-CON | CG-ALL-2771 | 12.5 | Add an Activities row ScoreLegalPack on task queue rwb-agent with input and output as in RWB-P10-E2030-CON section 12.5. |
| CDC-04094 | RWB-P10-E2031-APP | CG-ALL-2782 | 12.5 | Add a Workflows row for AgentRunDailyRollupWorkflow, the v1 workflow this story extends, on task queue rwb-agent. |
| CDC-04096 | RWB-P10-E2031-APP | DOR-RWB-P10-E2031-APP-8 | 12.5 | Add AgentRunDailyRollupWorkflow and activities aggregateAgentRuns and agentDrift. Section 14 needs 401 and 503 message IDs, not in source. |
| CDC-04100 | RWB-P10-E2031-APP | CG-ALL-2783 | 12.5 | Add activity aggregateAgentRuns (the legacy agentRunDaily step) to the Activities sheet, task queue rwb-agent, or use a catalogued activity. |
| CDC-04101 | RWB-P10-E2031-APP | CG-ALL-2784 | 12.5 | Add activity agentDrift (the legacy agentDrift step) to the Activities sheet, task queue rwb-agent, or use a catalogued activity. |
| CDC-04102 | RWB-P10-E2031-APP | CG-ALL-2785 | 12.5 | Add activity dispatchAgentAlerts to the Activities sheet, task queue rwb-agent, or use a catalogued activity. |
| CDC-04112 | RWB-P10-E2031-CON | CG-ALL-2796 | 12.5 | Add workflow AgentRunDailyRollupWorkflow on task queue rwb-agent. |
| CDC-04114 | RWB-P10-E2031-CON | CG-ALL-2797 | 12.5 | Add activity aggregateAgentRuns on task queue rwb-agent. |
| CDC-04115 | RWB-P10-E2031-CON | CG-ALL-2798 | 12.5 | Add activity raiseCostAlerts on task queue rwb-agent. |
| CDC-04116 | RWB-P10-E2031-CON | CG-ALL-2799 | 12.5 | Add activity agentDrift to the Activities sheet so that section 12.5 of RWB-P10-E2031-CON resolves to a catalogued activity. |
| CDC-04117 | RWB-P10-E2031-CON | CG-ALL-2800 | 12.5 | Add activity dispatchAgentAlerts to the Activities sheet so that section 12.5 of RWB-P10-E2031-CON resolves to a catalogued activity. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03946 | RWB-P10-E1063-CON | CG-ALL-2666 | 18 | Align the REQ-DRI-009 trace so RTM v7 and section 18 list the same test cases for the requirement. |
| CDC-03969 | RWB-P10-E1063-OPS | CG-ALL-2675 | 18 | Align REQ-DRI-009 to TC-P10-E1063-OPS-02, -03 and -07, the story's own tests, and drop the legacy TC-E1-014, TC-E1-063 and TC-E2-031 ids. |
| CDC-03984 | RWB-P10-E2028-APP | CG-ALL-2685 | 18 | Align the test lists of the two differing requirements in RTM v7 with section 18 of RWB-P10-E2028-APP. |
| CDC-03999 | RWB-P10-E2028-CON | CG-ALL-2700 | 18 | Align the differing trace rows, including REQ-DRI-001 (story: TC-P10-E2028-CON-02, -04, -05), with section 18 in the next RTM version. |
| CDC-04012 | RWB-P10-E2028-OPS | CG-ALL-2710 | 18 | Align the REQ-DRI-001 test list in RTM v7 with section 18 of this story (TC-P10-E2028-OPS-02, TC-P10-E2028-OPS-07) in the next RTM version. |
| CDC-04020 | RWB-P10-E2029-APP | DOR-RWB-P10-E2029-APP-12 | 12.7, 16, 18 | Align its test lists for this story with section 18, including TC-E2-029-13 under DP-09. |
| CDC-04029 | RWB-P10-E2029-APP | CG-ALL-2721 | 18 | Align the test lists of REQ-DVH-001 and REQ-DVH-006 with section 18 of RWB-P10-E2029-APP in the next version. |
| CDC-04046 | RWB-P10-E2029-CON | CG-ALL-2737 | 18 | Align the test lists of REQ-DVH-001 and REQ-DVH-006 to the test cases of section 18 of RWB-P10-E2029-CON. |
| CDC-04060 | RWB-P10-E2030-APP | DOR-RWB-P10-E2030-APP-12 | 16, 18 | Align the test case lists of REQ-S4-002 and REQ-DCM-011 with section 18 of RWB-P10-E2030-APP, now TC-E2-030-01 to TC-E2-030-15. |
| CDC-04069 | RWB-P10-E2030-APP | CG-ALL-2755 | 18 | Align REQ-DCM-011 test cases in RTM v7 with the TC-E2-030 IDs in section 18 in its next version. |
| CDC-04093 | RWB-P10-E2030-CON | CG-ALL-2774 | 18 | Align the REQ-DCM-011 test list in RTM v7 with section 18 (TC-P10-E2030-CON-02, -05) in its next version. |
| CDC-04107 | RWB-P10-E2031-APP | CG-ALL-2786 | 18 | Align the REQ-DRI-009 and REQ-APD-005 test case lists with section 18 of RWB-P10-E2031-APP in the next version. |
| CDC-04125 | RWB-P10-E2031-CON | CG-ALL-2802 | 18 | Align the REQ-DRI-009 and REQ-APD-005 test lists in the RTM with section 18 of RWB-P10-E2031-CON. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03945 | RWB-P10-E1063-CON | CG-ALL-2665 | 16 | Add rows for TC-P10-E1063-CON-01 to TC-P10-E1063-CON-06, with Given, When and Then copied from the criteria they cover. |
| CDC-03968 | RWB-P10-E1063-OPS | CG-ALL-2674 | 16 | Add rows for TC-P10-E1063-OPS-01 to TC-P10-E1063-OPS-08 to the next Test Cases version, with Given, When and Then copied from the criterion each covers. |
| CDC-03998 | RWB-P10-E2028-CON | CG-ALL-2699 | 16 | Add rows TC-P10-E2028-CON-01 to TC-P10-E2028-CON-08 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-04011 | RWB-P10-E2028-OPS | CG-ALL-2709 | 16 | Add rows TC-P10-E2028-OPS-01 to TC-P10-E2028-OPS-09 with Given, When and Then copied from the criterion each covers. |
| CDC-04045 | RWB-P10-E2029-CON | CG-ALL-2736 | 16 | Add rows for TC-P10-E2029-CON-01 to TC-P10-E2029-CON-07 with Given, When and Then copied from the criteria they cover. |
| CDC-04092 | RWB-P10-E2030-CON | CG-ALL-2773 | 16 | Add rows for TC-P10-E2030-CON-01 to TC-P10-E2030-CON-07 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-04124 | RWB-P10-E2031-CON | CG-ALL-2801 | 16 | Add rows TC-P10-E2031-CON-01 to TC-P10-E2031-CON-08 with Given, When and Then copied from the criteria they cover. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03932 | RWB-P10-E1063-CON | CG-ALL-2662 | 12.5 | Add an Activities row for aggregateAgentRuns (task queue rwb-agent) or the story uses a catalogued activity. |
| CDC-03933 | RWB-P10-E1063-CON | CG-ALL-2663 | 12.5 | Add an Activities row for raiseCostAlerts (task queue rwb-agent) or the story uses a catalogued activity. |
| CDC-03934 | RWB-P10-E1063-CON | CG-ALL-2664 | 12.5 | Add an Activities row for dispatchAgentAlerts (task queue rwb-agent) or the story uses a catalogued activity. |
| CDC-04001 | RWB-P10-E2028-OPS | DOR-RWB-P10-E2028-OPS-8 | 12.5 | Add Activity rows ResolveIntakeMode and RecordIntakeFeedback on task queue rwb-agent, or name catalogued activities in their place. Task queue and workflow ID items are resolved in the story. |
| CDC-04002 | RWB-P10-E2028-OPS | CG-ALL-2707 | 12.5 | Add an Activity row ResolveIntakeMode on task queue rwb-agent, registered by the same worker. |
| CDC-04003 | RWB-P10-E2028-OPS | CG-ALL-2708 | 12.5 | Add an Activity row RecordIntakeFeedback on task queue rwb-agent, registered by the same worker, as one workflow-kit transaction. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03935 | RWB-P10-E1063-CON | DOR-RWB-P10-E1063-CON-1 | 1 | Add role 'tech lead' for rwb-agent as a role code or role name, or rename the story role to the catalogued role. |
| CDC-03957 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-1 | 1 | Add 'platform engineer' as a role name, or confirm the role code the section 1 story uses |
| CDC-03990 | RWB-P10-E2028-CON | DOR-RWB-P10-E2028-CON-1 | 1 | Register 'tech lead' (Tech lead of rwb-agent) as a role code or role name |
| CDC-04004 | RWB-P10-E2028-OPS | DOR-RWB-P10-E2028-OPS-1 | 1 | Add the role 'platform engineer' as a role code or name, or confirm the role that section 1 maps to |
| CDC-04035 | RWB-P10-E2029-CON | DOR-RWB-P10-E2029-CON-1 | 1 | Add a role code or name for Tech lead of rwb-agent, or name an existing role to use in section 1. |
| CDC-04118 | RWB-P10-E2031-CON | DOR-RWB-P10-E2031-CON-1 | 1 | Add the role 'tech lead of rwb-agent' with a role code assigned by the document owner, then align section 1 and section 10 to it. |

### RWB-P10-E2028-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03972 | RWB-P10-E2028-APP | DOR-RWB-P10-E2028-APP-21 |  | Build and publish the contract so its build status is Done. |
| CDC-03973 | RWB-P10-E2028-APP | DOR-RWB-P10-E2028-APP-22 |  | Publish the contract fake library and record its published version. |
| CDC-03974 | RWB-P10-E2028-APP | DOR-RWB-P10-E2028-APP-23 | Metadata | Contract version is fixed by the contract story; the Metadata row records the placeholder and does not invent a version. |
| CDC-04007 | RWB-P10-E2028-OPS | GAP-2191 | find it | Apply the GAP-2191 proposed fix: two operations on /api/recovery/agent/v1 with legacy members and refusals; acceptance event rwb.agent.AgentFeedbackRecorded.v1; DecisionRecorded on rwb.decision-record.v1; one gateway-bff route |
| CDC-04009 | RWB-P10-E2028-OPS | GAP-0623 | 15 | Route path kept Not specified, consistent with AC9; contract member types left to review with owners. |
| CDC-04010 | RWB-P10-E2028-OPS | GAP-1294 |  | Agree the three operation shapes, the LOV-DECISION value D6 with verdicts ACCEPTED, CORRECTED, REJECTED, the reason-code list, the text of MSG-P7-009 and the rwb-decision login name. |

### RWB-P10-E2029-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04013 | RWB-P10-E2029-APP | DOR-RWB-P10-E2029-APP-21 | header | Set build status to Done (currently Not started) so the contract is published for this story. |
| CDC-04014 | RWB-P10-E2029-APP | DOR-RWB-P10-E2029-APP-22 | header | Record a published contract fake library version. |
| CDC-04025 | RWB-P10-E2029-APP | GAP-0626 | 12 | Publish the raise operation, the decision-entry read, the parameter keys, the member types, the login and the route with their owners; the story keeps them as Not specified. |
| CDC-04026 | RWB-P10-E2029-APP | GAP-2194 | 12 | Publish the raise and entry-read shapes, register the rwb.agent.AgentRunCompleted.v1 payload, fix the gateway-bff route and confirm the five score-row members. |
| CDC-04027 | RWB-P10-E2029-APP | GAP-2402 | 12 | Agree the append on POST /api/recovery/decision/v1/decision-log, the evaluation and run reads, the case-less approval variant, LOV-DECISION promotion code, MSG-P7-009 text, EV-30 and the rwb-decision login. |
| CDC-04028 | RWB-P10-E2029-APP | GAP-3100 | 12 | Publish the raise request with the return point, agent version and policy segment pair fields, name the agent-policy read, and publish the decision-record envelope type. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03976 | RWB-P10-E2028-APP | CG-ALL-2679 | 12.1 | Give the message ID of the standard for 401 no session in §4, so §12.1 of the story and AC14 can cite it. |
| CDC-04034 | RWB-P10-E2029-CON | CG-ALL-2735 | 4, 14 | Add a new message ID for 'The report is read on a run that is not DONE' with text 'The report is not ready: the evaluation is {status}.' so the story can cite it. |
| CDC-04080 | RWB-P10-E2030-CON | CG-ALL-2766 | 12.1 | Add message IDs for 401 no session and for 404 unknown run, version or evaluation. |
| CDC-04084 | RWB-P10-E2030-CON | DOR-RWB-P10-E2030-CON-9 | 14 | Confirm the MSG-P10-008 text against the standard v4 entry so section 14 can carry the standard text. |
| CDC-04091 | RWB-P10-E2030-CON | CG-ALL-2772 | 14 | MSG-P10-008 text restored to the original wording |

### RWB-P10-E2030-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04055 | RWB-P10-E2030-APP | DOR-RWB-P10-E2030-APP-21 |  | Set build status to Done (contract published) before this story is ready. |
| CDC-04056 | RWB-P10-E2030-APP | DOR-RWB-P10-E2030-APP-22 |  | Publish a contract fake library version and record it as published. |
| CDC-04062 | RWB-P10-E2030-APP | GAP-0628 | 4 | Declare the two run operations from the agent runtime baseline, the five pack members with their three statuses, the consumed reads each one hop with the 2 s budget, EV-28 as the only event, and the route as a one-hop pass-through. |
| CDC-04065 | RWB-P10-E2030-APP | GAP-2197 | 4 | Story keeps the harness start of AgentRunWorkflow (ASM-0955). Run-start path, idempotency rule and six policy members stay open with their owners. |
| CDC-04066 | RWB-P10-E2030-APP | GAP-2358 | 4 | Publish the pack tool call as one operation per case with named per-item fields and map a 503 of the document service to TOOL_UNAVAILABLE with fallback true. |

### RWB-P10-E1063-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03936 | RWB-P10-E1063-CON | DOR-RWB-P10-E1063-CON-10 | find it | Add empty, loading, error and no-access states for screen SCR-46 to the app story. |
| CDC-03938 | RWB-P10-E1063-CON | GAP-0629 | find it | Place the drift step in the v1 Schedule workflow; read segment from run row; add agent-version filter and three decision-log elements via rwb-decision; name notice path; hold watch_measures; migration V10_007; login and route per directive. |
| CDC-03958 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-10 | find it | Add empty, loading, error and no access states for SCR-46 |
| CDC-03962 | RWB-P10-E1063-OPS | GAP-0629 | find it | Apply the nine app-slice values per the proposed fix, including migration V10_007, the segment, the override read, the notice path, watch_measures, range limits, login and route |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03937 | RWB-P10-E1063-CON | DOR-RWB-P10-E1063-CON-12 | 12.7, 16, 18 | Add rows TC-P10-E1063-CON-01 to TC-P10-E1063-CON-07 to Test Cases v8 and align the section 18 test lists to RTM v7. |
| CDC-03959 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-12 | 12, 12.7, 16, 18 | Add TC-P10-E1063-OPS-01 to -10 to Test Cases v8; align section 18 test lists with RTM v7 |
| CDC-03993 | RWB-P10-E2028-CON | DOR-RWB-P10-E2028-CON-12 | 12.7, 16, 18 | Add TC-P10-E2028-CON-01 to -11 to Test Cases v8; align the section 18 test lists with RTM v7 |
| CDC-04083 | RWB-P10-E2030-CON | DOR-RWB-P10-E2030-CON-12 | 12.7 | Story adds TC-P10-E2030-CON-11 as the boundary test for the section 12.7 tables and lists it in section 18; the external registers need the changes named. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03948 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-14 | header | Record the signed epic design sign-off for EP01 so that Definition of Ready item 14 can pass. Sign-off reference Not specified in the source documents (DOR-RWB-P10-E1063-OPS-14). |
| CDC-03986 | RWB-P10-E2028-CON | DOR-RWB-P10-E2028-CON-14 | find it | Confirm and record the signed epic design sign-off for RWB-SVC-P10. |
| CDC-04000 | RWB-P10-E2028-OPS | DOR-RWB-P10-E2028-OPS-14 | header | Record the signed epic design sign-off for this story's epic, or state that it is not yet signed. |
| CDC-04031 | RWB-P10-E2029-CON | DOR-RWB-P10-E2029-CON-14 |  | Record the signed epic design sign-off for RWB-P10-E2029-CON under EP03, so Definition of Ready item 14 passes with the epic design record as its evidence. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03960 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-7 | 11 | Register agent_run_daily as a field or entity, or confirm the name is not used by this story |
| CDC-04097 | RWB-P10-E2031-APP | CG-ALL-2777 | 7 | Record agent_run_daily as the legacy lake object with no target (ADR-018; Architecture v5 slide 37). |
| CDC-04098 | RWB-P10-E2031-APP | CG-ALL-2778 | 6 | Record drift_points as a key within agent_policy.watch_measures (DF-AGT-019). |
| CDC-04099 | RWB-P10-E2031-APP | CG-ALL-2779 | 6 | Record window_days as a key within agent_policy.watch_measures (DF-AGT-019). |

### RWB-P10-E2028-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03994 | RWB-P10-E2028-CON | GAP-2190 | 10; 11 | Settle the feature flag home, topic and migration values and the policy values with the app slice |
| CDC-04005 | RWB-P10-E2028-OPS | DOR-RWB-P10-E2028-OPS-10 | find it | Add empty, loading, error and no access states for SCR-03 and SCR-46 |
| CDC-04006 | RWB-P10-E2028-OPS | GAP-2190 | find it | Apply the GAP-2190 proposed fix in the app slice: service identity the rwb-agent login (DP-02) on rwb_agent only; D6 as the LOV-DECISION value; freshness date from the rwb-source-data read; acceptance event rwb.agent.AgentFeedbackRecorded.v1; seven lists via rwb-case |
| CDC-04008 | RWB-P10-E2028-OPS | GAP-0622 | find it | Apply the GAP-0622 proposed fix in the app slice: DP-02 service identity on rwb_agent only; D6 via the local decision-record library; DecisionRecorded as rwb.decision-record.DecisionRecorded.v1; SUMMARY as the only item key |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03931 | RWB-P10-E1063-CON | CG-ALL-2657 | find it | Record the daily aggregate object agent_run_daily (index, library table or flag) in the owning document, or confirm the dictionary name. |
| CDC-03965 | RWB-P10-E1063-OPS | GAP-1517 | 12 | Daily measure is a projection over the run record, not a LDM table; the FSD criterion naming agent_run_daily must be restated. |
| CDC-04037 | RWB-P10-E2029-CON | DOR-RWB-P10-E2029-CON-11 | find it | Classify each field of the AgentRunCompleted payload and of the section 12.7 tables as personal data or not. |

### RWB-P10-E1063-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03949 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-21 | header | The Contract dependencies row records RWB-P10-E1063-CON as not yet published (build status Not started); publication belongs to the contract document. |
| CDC-03950 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-22 | 12.8 | Record the published fake library version for the four contract fakes. |
| CDC-03951 | RWB-P10-E1063-OPS | DOR-RWB-P10-E1063-OPS-23 | Contract dependencies | Record the contract version that RWB-P10-E1063-OPS builds against. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04016 | RWB-P10-E2029-APP | GAP-1816 | 4 | Rebase the S8 reads on the rwb-source-data contract field names and add a build boundary test that fails on a view or ACE table read. |
| CDC-04017 | RWB-P10-E2029-APP | GAP-1822 | 4 | Add the rwb-document read to the S8 row and the call-note field to the rwb-source-data contract; confirm with both owners. |
| CDC-04042 | RWB-P10-E2029-CON | GAP-1832 |  | Carry EV-06 and EV-07 keyed by case, with code, state, contact stop flag, return point and decision record reference in the envelope. No personal or financial value. |

### RWB-P4-E1039-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03939 | RWB-P10-E1063-CON | GAP-2332 | find it | Publish the two access-event codes, the entry field list, the page bounds and the record code with the next access-log contract version; name the read index in the rwb_access schema; register the Flyway step and parameter codes. |
| CDC-04104 | RWB-P10-E2031-APP | GAP-2316 | find it | Add the agent-monitor object-type value, the record code, the entry field list, the page bounds, the read index on rwb_access and the Flyway step. |

### RWB-P4-E1039-CON; 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03963 | RWB-P10-E1063-OPS | GAP-2332 | 12 | Publish the two access-event codes, entry field list, page bounds, read index name, Flyway step and two parameter codes; the story section text was not in this chunk. |
| CDC-04121 | RWB-P10-E2031-CON | GAP-2316 | find it | Add the agent-monitor object-type code, the DP-03 record code, the entry field list, the page bounds, the read index on rwb_access and the Flyway step to the access-log contract. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03980 | RWB-P10-E2028-APP | GAP-2191 | 3 | Publish the path of the two operations as one gateway-bff pass-through route of one hop and 2 s on the base /api/recovery/agent/v1. |
| CDC-04110 | RWB-P10-E2031-APP | GAP-0631 | 10 | Register the gateway-bff route for SCR-46 and the v2 read, path left to the edge story; expose alert thresholds and topology as named chart values; update the Schedule in place; verify rwb-reporting consume right without creating its consumer group. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03985 | RWB-P10-E2028-CON | CG-ALL-2695 | 12.3 | Add event type rwb.agent.AgentFeedbackRecorded.v1 on topic rwb.agent.events.v1 to the Events sheet. |
| CDC-03987 | RWB-P10-E2028-CON | DOR-RWB-P10-E2028-CON-8 | find it | Add rwb.agent.AgentFeedbackRecorded.v1 on rwb.agent.events.v1 to the Events sheet; re-check the three further detcheck findings not itemised here. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03992 | RWB-P10-E2028-CON | DOR-RWB-P10-E2028-CON-11 | find it | Remove the personal-data class from the P2 fields that this story says carry none, or name the personal fields in the story |
| CDC-04120 | RWB-P10-E2031-CON | DOR-RWB-P10-E2031-CON-11 | 11 | Reconcile the personal-data classification of the flagged P2 fields with the statement that no personal data field is carried by this contract. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04030 | RWB-P10-E2029-CON | CG-ALL-2727 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations?caseId= in rwb-deviation.yaml through the provider CON story |
| CDC-04032 | RWB-P10-E2029-CON | DOR-RWB-P10-E2029-CON-8 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations?caseId= in rwb-deviation.yaml |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04054 | RWB-P10-E2030-APP | CG-ALL-2747 | 12.2 | Publish GET /api/recovery/document/v1/documents/{documentId}/fields in rwb-document.yaml through RWB-P5-E2025-CON, the provider's CON story. |
| CDC-04078 | RWB-P10-E2030-CON | CG-ALL-2765 | 12.2 | Publish GET /api/recovery/document/v1/documents/{documentId}/fields through the provider's story RWB-P5-E2025-CON. |

### RWB-P5-E2025-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04061 | RWB-P10-E2030-APP | GAP-0627 | 10 | Name the checklist, document-list and OCR-text operations and their members on rwb-document, one hop, 2 s budget; field values masked before the model call. |
| CDC-04063 | RWB-P10-E2030-APP | GAP-2196 | 4 | Publish the rwb-document read paths below /api/recovery/document/v1, the rwb-litigation legal-action read path, the parameter and list codes, the gateway-bff route path, the member types and the service login. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04068 | RWB-P10-E2030-APP | GAP-2360 | 4 | Fix the DocumentChecklist schema with the per-item fields, the document IDs held per item, the completeness reference and the paging of items. |
| CDC-04090 | RWB-P10-E2030-CON | GAP-2360 | 4 | Fix the DocumentChecklist schema with per-item fields, the document list per item and the completeness reference. |

### RWB-ITG-E2031-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04105 | RWB-P10-E2031-APP | GAP-0413 | find it | Define the SIT harness profile, seed pack, fixed clock at 2026-12-14, evidence format and gate with the QA lead; confirm the drift Schedule location at wave 2 entry. |
| CDC-04122 | RWB-P10-E2031-CON | GAP-0413 | find it | Define the SIT harness profile, the seed pack for INTAKE and SCREENING, the fixed clock at 2026-12-14, the evidence format and the gate, and confirm the drift Schedule runs in rwb-agent. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04106 | RWB-P10-E2031-APP | GAP-2317 | find it | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON. |
| CDC-04123 | RWB-P10-E2031-CON | GAP-2317 | find it | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04109 | RWB-P10-E2031-APP | GAP-2319 | none | At D1 confirm the eight legacy test case ids are held by both slices, no measure is built twice and exception X6 is the one access criterion. |
| CDC-04129 | RWB-P10-E2031-CON | GAP-2319 | 1 | Confirm the eight legacy test case ids are held by both slices, no measure is implemented twice, and exception X6 is the one access criterion; no change to the legacy master. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20654 | RWB-P10-E1063-OPS | R-22229 |  | Template code, channel, notice type, retry window not specified in the source documents (GAP-1209). |
| CDC-20655 | RWB-P10-E1063-OPS | R-22229 |  | Template, channel, notice type, notice fields, role holders, guard right, retry window not in source text (GAP-1209). |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03928 | RWB-P10-E1063-CON | CG-ALL-2661 | 12.5 | Add workflow AgentRunDailyRollupWorkflow: rwb-agent, queue rwb-agent, namespace rwb-recovery, Schedule AgentRunDailyRollup, activities aggregateAgentRuns, raiseCostAlerts, dispatchAgentAlerts |

### OTHER:Functional Specification Document P10 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03930 | RWB-P10-E1063-CON | GAP-1516 | find it | Remove the data lake write, the Power BI integration at A2.6.2 and the lake row-count check at AC-EXC-P10-006-01. Serve the dashboard on SCR-46 from daily measures and the rwb-reporting read model. |

### OTHER:P6 rwb-comms contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03940 | RWB-P10-E1063-CON | GAP-1209 | find it | Seed template code, channel, notice type and retry window as parameter and reference rows; publish request and answer fields of the two operations; declare guard right of cost-alert notice read at gateway-bff (ASM-B-P6-05-E1063-4). |

### RWB-P10-E1058-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03941 | RWB-P10-E1063-CON | GAP-1211 | find it | Publish an agent alert event on rwb.agent.events.v1 with alert reference and facts; send the cost-alert notice on the P6 case-position message operation with the alert reference; read back via GET /notices/{noticeId}. |

### OTHER:FSD P4 v3 and TSD P4 v3 (next versions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03942 | RWB-P10-E1063-CON | GAP-2333 | n/a | Correct REQ-ACA-006 and NFR-042 to the access entry of the served read; record Reporting letters for the other roles in the matrix load; keep both rights and both access event names. |

### OTHER:RWB-E2-009 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03943 | RWB-P10-E1063-CON | GAP-2576 | n/a | Declare the three consumed operations and two owner-queue activities on per-service bases, one hop, 2 s timeout; replace the INT-19 extract with a rwb-integration hand-off; take agent rates from EV-28 and RWB-P10-E1063-CON. |

### OTHER:TSD P10 v2 T-A.2 and the rwb-decision contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03944 | RWB-P10-E1063-CON | GAP-0630 | n/a | Fix the seven added member names with the four-decimal rule and additive major version 1; name drift inputs after watch_measures members; name the notice path by its owner. |

### OTHER:FSD P10 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03953 | RWB-P10-E1063-OPS | GAP-1516 | find it | Remove integration points Power BI and model gateway from A2.6.2 and the lake write from the nightly dashboard job. Serve the dashboard on SCR-46 from the service daily measures and the rwb-reporting read model. Move the row-count check in AC-EXC-P10-006-01 to the measure hand-over. |

### RWB-P10-E1058-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03961 | RWB-P10-E1063-OPS | GAP-0644 | find it | Keep three legacy admin operations on /api/recovery/agent/v1; route reads through gateway-bff on that path; report and configuration operations stay with RWB-P10-E1058-APP |

### OTHER:P6 comms contract and parameter/reference set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03964 | RWB-P10-E1063-OPS | GAP-1209 | 12 | Template code, channel, notice type, notice fields, role holders, guard right and retry window must be published; the story text for those values was not in this chunk. |

### OTHER:FSD P10 v3 AC-ALT-P10-006-01 and Batch and Scheduling Design v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03966 | RWB-P10-E1063-OPS | GAP-1519 | 12 | JOB-15 stays the rwb-reporting extract; the FSD must give rwb-agent its own once-per-date aggregation trigger, not JOB-15 completion. |

### OTHER:FSD P4 v3 REQ-ACA-006 and NFR-042; RWB-P10-E1063-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03967 | RWB-P10-E1063-OPS | GAP-2333 | 12 | Correct the data-lake access rule and record Reporting letters for other roles; the story's Reporting rights text was not in this chunk to edit. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03970 | RWB-P10-E2028-APP | CG-ALL-2678 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness through the provider's CON story (the business date of the ACE load). |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:Events (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03971 | RWB-P10-E2028-APP | CG-ALL-2682 | 12.3 | Add event type rwb.agent.AgentFeedbackRecorded.v1 on topic rwb.agent.events.v1 with owner P10 and key the case ID. |

### OTHER:the rwb-source-data API contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03975 | RWB-P10-E2028-APP | DOR-RWB-P10-E2028-APP-8 | 12.3 | §12.3 payload runid, agent, caseid, outcome, fallback from Catalog Events row 32 and the topic from Topics row 14; the freshness path is P1's. The three further findings are not in the item. |

### OTHER:the SCR-03 and SCR-46 screen definitions (screens and states workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03979 | RWB-P10-E2028-APP | DOR-RWB-P10-E2028-APP-10 | 15 | Give SCR-03 and SCR-46 their empty, loading, error and no access states; §15 of the story cites them. |

### RWB-P10-E2028-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03981 | RWB-P10-E2028-APP | GAP-0410 | 19 | Record the Enterprise AI test tenant (INT-23), its model and guardrail profile, the INTAKE P2 and PR3 policy and prompt fixtures, the 60-second timeout and rule-fallback control, the SIT harness environment and its seeding, the evidence report format and retention, and the L1 intake pass and fail gate. |

### RWB-P10-E2028-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03982 | RWB-P10-E2028-APP | GAP-0623 | 12.3 | Record event type name left to RWB-P10-E2028-CON; no invented type name in §12.3. Member types, route path and 409 ordering stay with the contracts. |

### RWB-P10-E2028-CON; RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03983 | RWB-P10-E2028-APP | GAP-1294 | 12.2 | Agree the append request and answer on POST /api/recovery/decision/v1/decision-log, the two reads with the DecisionLogPage and DecisionLogEntry field sets of TSD P7 v2 T3.1, LOV-DECISION values beyond D6, the reason-code list, the text of MSG-P7-009 and the rwb-decision login name. |

### OTHER:Recovery Workbench P3 screen specification (SCR-03; OTHER:SCR-46) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03991 | RWB-P10-E2028-CON | DOR-RWB-P10-E2028-CON-10 | find it | Add empty, loading, error and no-access states to SCR-03 and SCR-46 |

### OTHER:gateway-bff edge contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03995 | RWB-P10-E2028-CON | GAP-2191 | 11 | Publish the path of the one-hop 2 s route over the two operations on /api/recovery/agent/v1 and the case-decision proposal path of RWB-P3-E1035-CON |

### OTHER:Not specified in the source documents (GAP-0622) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03996 | RWB-P10-E2028-CON | GAP-0622 | 11; 12.2 | Stale-check business date left as Not specified (GAP-0622) |

### RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03997 | RWB-P10-E2028-CON | GAP-1294 | 11 | Decision-log append request and answer left Not specified (GAP-1294) |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04018 | RWB-P10-E2029-APP | GAP-1818 | 4 | The S8 read path in 12.2 was changed under CG-ALL-2716; reconciling the S8 operations across the Architecture slide, Ownership Map and FSD belongs to those documents. |

### OTHER:P3 Criteria and tests (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04021 | RWB-P10-E2029-APP | DOR-RWB-P10-E2029-APP-7 | 11 | Replace the legacy job and decision-log wording with this story's wording: the local decision-record library on rwb.decision-record.v1 (DP-03). |

### OTHER:FSD S8 feature criteria A2.2.4.1 to A2.9.4.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04022 | RWB-P10-E2029-APP | GAP-1823 | 7 | Carry each row as one criterion; the BA and QA lead rewrite the case-record Timers shown rows; add this PRD's step criteria for pause, stop, routing and clear. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S8 rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04023 | RWB-P10-E2029-APP | GAP-1819 | 11 | Add S8 rows in schema rwb_deviation for screening runs, score rows, contact stop, agent feedback and breach record, with the key fields in FSD S8. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:S8 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04024 | RWB-P10-E2029-APP | GAP-1832 | 11 | Add envelope fields: case key, code, state, contact stop flag, return point and decision record reference; no personal or financial value. |

### OTHER:P3 screen specification for SCR-03 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04036 | RWB-P10-E2029-CON | DOR-RWB-P10-E2029-CON-10 | 15 | Section 15 names the SCR-03 states; empty, error and no access are marked Not specified (CG-ALL-2739). Remaining screen content belongs to the screen owner. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04038 | RWB-P10-E2029-CON | DOR-RWB-P10-E2029-CON-12 | 12.7, 16, 18 | TC-08 to TC-15 added; section 16 now has 15 rows. Registration and RTM alignment are in other documents. |

### OTHER:FSD S8 (E2 feature criteria) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04039 | RWB-P10-E2029-CON | GAP-1823 |  | Rewrite the seven feature main criteria and the alternate and exception rows as one criterion each, with this PRD's own step criteria for clock pause, stop, routing and clear. |

### OTHER:FSD S8 and rwb-decision (rule package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04040 | RWB-P10-E2029-CON | GAP-1826 |  | FSD S8: name the ten unnamed R-DEV rules and R-DEV-19 to R-DEV-21 as the requirement set. rwb-decision: author the 22-rule package and its version label. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Tables sheet (S8 rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04041 | RWB-P10-E2029-CON | GAP-1819 |  | Add S8 rows in schema rwb_deviation for shadow screening runs, score rows per code, contact stop, agent feedback and breach record. State them as entity groups with key fields only. |

### RWB-P10-E2029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04043 | RWB-P10-E2029-CON | GAP-0625 |  | Name the rwb-agent login at build start, publish the S8 raise path and add its C row, name the parameter keys, read the sealed entry, name the route, and create the two indexes in the P10 DB story. |

### RWB-S8-E2029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04044 | RWB-P10-E2029-CON | GAP-3100 | 12.2 | Publish the raise request with the return point of DF-CAS-041 deviation.paused_state, the agent version SCREENING@P2/PR2 and the policy segment pair; name the agent-policy read; add the partial unique index of one open code per case; publish the envelope type of the decision-record entry; assign a level to every legacy RWB-E2-029 case in the Test Cases workbook. |

### OTHER:wave 2 integration harness README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04064 | RWB-P10-E2030-APP | GAP-0412 | 4 | Record the harness environment and seeding, the LEGAL-S1 v1 fixture of 50 packs, the MORTGAGE_CIVIL 9-item fixture, the model-stub behaviours, the P5-down control for RW-2026-000903, the evidence format and the pass gate. |

### OTHER:FSD P5 section A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04067 | RWB-P10-E2030-APP | GAP-2359 | 4 | State the case type to stage and route mapping, or add case type as a checklist key, and load the 9-item MORTGAGE_CIVIL checklist at a named version. |

### OTHER:Business Requirements Program (next BRD version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04070 | RWB-P10-E2030-APP | GAP-2362 | find it | Name the BRD section and the L3 process of REQ-DCM-011 so the traceability row can be completed. |

### RWB-P5-E2025-CON; OTHER:rwb-litigation S4 contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04085 | RWB-P10-E2030-CON | GAP-0627 | 11 | Publish the OCR-text read and checklist operation paths with member names in RWB-P5-E2025-CON, and the by-case legal-action read path in the rwb-litigation contract. |

### RWB-P5-E2025-CON; OTHER:rwb-litigation S4 contract; OTHER:TSD P10 Agent runtime v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04086 | RWB-P10-E2030-CON | GAP-0628 | 11 | Fix the OCR-text, checklist and legal-action read paths and member names, the run read paging and the route name in the named sources. |

### parameter-catalog.csv; RWB-P5-E2025-CON; OTHER:rwb-litigation contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04087 | RWB-P10-E2030-CON | GAP-2196 | 11 | Add the parameter keys for the minimum sample 50 and the promotion list, and publish the three rwb-document read paths, the legal-action read path and the gateway-bff route path. |

### OTHER:Harness README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04088 | RWB-P10-E2030-CON | GAP-0412 | 16 | Record the harness environment, the two fixtures, the model stub, the evidence format and the pass gate at the wave 2 entry check. |

### OTHER:FSD P5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04089 | RWB-P10-E2030-CON | GAP-2359 | 4 | State the case type to stage and route mapping in section A2.16, or add case type as a checklist key; load the MORTGAGE_CIVIL checklist of 9 items at a named version. |

### RWB-P10-E2031-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04095 | RWB-P10-E2031-APP | DOR-RWB-P10-E2031-APP-21 | header | Build status moves from Not started to Done. |

### OTHER:RWB-P7 rwb-decision decision-log contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04103 | RWB-P10-E2031-APP | GAP-0629 | find it | Add the agent-version filter and the three decision elements as an additive change to the decision-log read. |

### OTHER:Work Package plan generator and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04108 | RWB-P10-E2031-APP | GAP-2201 | none | Remove RWB-E2-031 from the B-P10-02 fanout list, number the defaults once from ASM-B2-P10-005-1 and add the duplicate output-path check. |

### RWB-P10-E2031-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04119 | RWB-P10-E2031-CON | DOR-RWB-P10-E2031-CON-10 | 11 | Add the states empty, loading, error and no access to screen SCR-46 in the app story. |

### OTHER:App-slice story of RWB-E2-031 version 2 (rwb-agent app slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04126 | RWB-P10-E2031-CON | GAP-2198 | 1 | Record the defaults: agentDrift is the drift activity of the baseline Schedule; segment read from the run row; migration adds indexes only; no data lake copy; screen states from policy mode. |

### OTHER:Deployment-slice story of RWB-E2-031 version 2 (rwb-agent deployment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04127 | RWB-P10-E2031-CON | GAP-2200 | 7 | Reference the login through a secret reference; fix the route path with the edge story; topology and budget as release values files; single model gateway egress as a private endpoint declared once. |

### OTHER:Work Package plan for RWB-E2-031 (B-P10-02 fanout and B2-P10-005) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04128 | RWB-P10-E2031-CON | GAP-2201 | 1 | Keep one Work Package per slice; supersede the B-P10-02 gap and assumption rows; number defaults once as ASM-B2-P10-005-1 to -24; add duplicate-output-path and ASM resolution checks in checks/run_all.py. |

### OTHER:Deployment slice of RWB-E2-031 version 2 (rwb-agent deployment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04130 | RWB-P10-E2031-CON | GAP-0631 | 7 | Reference the rwb-agent login (DP-02) by secret reference; register the route under RWB-PLT-N001-CON; chart values for thresholds and topology; update Schedule in place; verify consume right of rwb-reporting. |

### 07 Screens and experience/Recovery Workbench Screen Inventory and Navigation v2.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20580 | RWB-P10-E2028-APP | R-15372 |  | SCR-03 and SCR-46 states are not in the sources (CG-ALL-2689, CG-ALL-2690). Adding them needs a decision. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0372 | Data lake removed: agent daily read model, reporting read and job rerun owner are not named for the target | P10 agent owner, P9 reporting owner, P1 source data owner, P6 comms owner and P2 integration owner | Resolved (directive) |
| GAP-0410 | The agent-intake harness pack, the Enterprise AI test endpoint and the policy fixtures are not specified | Integration lead | Resolved (directive) |
| GAP-0411 | SIT harness environment, SCREEN-S2 fixture pack, Enterprise AI test profile, evidence format and gate for the deviation-screening journey are not specified in any source read | Integration lead | Resolved (directive) |
| GAP-0412 | Harness environment, seed fixtures, model stub, evidence format and pass gate for the legal document agent shadow journey are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0413 | SIT harness environment, two-week and November seed, fixed clock, cost reconciliation fixture, evidence and gate for the agent-monitor journey | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0616 | Agent monitoring dashboard in rwb-agent: the data lake of the legacy story is removed, and the schedule name, the service login, the route path, the notification operation and the home of the daily aggregate are not specified | Solution architect | Resolved (directive) |
| GAP-0617 | Agent monitoring contract in rwb-agent: the page size and cursor, the member types of the aggregate element, the held-date status members, the Schedule name, the route path and the notification operation are not specified | Solution architect | Resolved (directive) |
| GAP-0618 | Agent monitoring deployment in rwb-agent: the topology, host, SKU, budget, route path, login, feed retention and alert thresholds are not specified | Platform administrator | Resolved (directive) |
| GAP-0622 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the item key set, the invalid-verdict refusal, the migration order and the segment rule are not specified | Solution architect with the P10 service owner and the owners of rwb-case and rwb-decision | Resolved (directive) |
| GAP-0623 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the record event type name, the route path, the 409 rule and the invalid-verdict refusal are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0624 | Case intake agent at L1 deployment in rwb-agent: the login, the migration order, the topic partitions and retry names, the alert window and thresholds, the worker and probe values and the route path are not specified | Platform administrator with the DevOps team and the ACE database team | Resolved (directive) |
| GAP-0625 | The app slice of the deviation screening evaluation and L1 on one segment: the service login, the S8 raise contract story, the parameter keys of the floor and the promotion condition, the sealed decision-entry read, the gateway-bff route path and the migration numbering are not fixed by any source | TechX with the rwb-deviation (S8) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0626 | The contract slice of the deviation screening evaluation and L1 on one segment: the S8 raise path and members, the parameter keys, the member types of a consumed answer, the sealed decision-entry read, the service login and the route path are not specified by any source | TechX with the rwb-deviation (S8) owner, the rwb-decision (P7) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0627 | The app slice of the legal document agent in shadow: the document, OCR-text and checklist operations and members, the legal-action read, the run-start path, the parameter keys, the service login, the route, the BRD section of REQ-DCM-011 and the pack member types are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0628 | The contract baseline of the legal document agent: the OCR-text and checklist operations and member names, the legal-action read, the run-start path, the route, the paging and member types, and the event family beyond EV-28 are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0631 | The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified | Platform administrator | Resolved (directive) |
| GAP-0644 | Extraction evaluation in rwb-agent: service login, document-type owner, admin operation set, route path and score read path | Solution architect | Resolved (directive) |
| GAP-1209 | Template code, channel, notice type, field names, recipient role holders, guard right and retry window are not named for the target | P6 comms owner, P10 agent owner and platform notification path owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1210 | The legacy data lake copy and the agent monitoring dashboard have no target, and P6 has no replacement for the dashboard | P6 comms owner, P9 reporting owner and architecture owner | Resolved (directive) |
| GAP-1211 | The agent alert event name, the alert notification operation name and the non-case binding of the cost alert are not named for the target | P10 agent owner and P6 comms owner | Resolved (directive) |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1294 | No source gives the value set or the wire shape this story needs: the append request and answer, the ledger read and its page, the reason codes, the run read field set, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1516 | FSD P10 v3 publishes the agent dashboard through a data lake write and Power BI, both removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1517 | The daily aggregate table the FSD acceptance criteria name is not in the Logical Data Model v8 entity list | Solution architect | Resolved (directive) |
| GAP-1519 | JOB-15 is the reporting extract of rwb-reporting in the Ownership Map, but the FSD uses its completion as the trigger of the P10 dashboard | Platform administrator | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1832 | The two deviation events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision log entry to travel with them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-2190 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the acceptance event name, the list codes, the case-decision proposal path, the route path, the feature flag home, the topic and migration values and the policy values the gate reads are not specified | Solution architect with the P10 service owner and the owners of rwb-case, rwb-decision and rwb-source-data | Resolved (directive) |
| GAP-2191 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the acceptance event name, the case-decision proposal path, the route path, the 409 rule, the item key set, the invalid-verdict refusal and the policy values are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-case and rwb-decision | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2192 | Case intake agent at L1 deployment in rwb-agent: the login, the route path, the topic partitions, retry and retention, the migration order, the alert window and thresholds, the worker and probe values and the consumer groups are not specified | Platform administrator with the DevOps team and the ACE database team | Resolved (directive) |
| GAP-2193 | RWB-P10-E2029-APP: values the sources leave open for the screening L1 app slice | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2194 | RWB-P10-E2029-CON: contract detail the sources leave open for the screening key | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2196 | Legal document agent in shadow in rwb-agent (app slice): the consumed operation paths below the rwb-document base, the legal-action read path, the parameter codes and the list codes, the gateway-bff route path, the member types of the pack and of the run answer, and the service login are not specified | Solution architect with the owners of rwb-document, rwb-litigation and rwb-case, and the platform library owner for the route | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2197 | Legal document agent in shadow in rwb-agent (contract slice): the run-start path below the agent base, the consumed boundary paths and field names, the six policy members beyond the baseline, the member types of the pack and the score row, and the gateway-bff route path are not specified | Solution architect with the owners of rwb-document, rwb-litigation and rwb-case, and the platform library owner for the route | Resolved (directive) |
| GAP-2198 | RWB-E2-031 version 2 app slice: the drift step and its Schedule, the segment source, the decision-log read, the notice, the policy values, the migration scope, the element change, the screen states, the login, the route path, the range limits and the two windows are not named by the sources | Tech lead of rwb-agent with the solution architect | Resolved (directive) |
| GAP-2199 | RWB-E2-031 version 2 contract slice: the decision-log filter and override element, the notice operation, the name of the read right, the paging and member types, the route path, the login and the Schedule step names are not fixed by the sources | Tech lead of rwb-agent with the owners of rwb-decision, rwb-comms and rwb-access | Resolved (directive) |
| GAP-2200 | RWB-E2-031 version 2 deployment slice: the route path, the login secret, the topology and budget, the notice operation, the Schedule registration detail and the model gateway egress are not fixed by the sources | DevOps engineer with the platform administrator and the security administrator | Resolved (directive) |
| GAP-2201 | Two Work Packages write the same three story files, the same three fragments and two overlapping assumption sets for legacy RWB-E2-031 on rwb-agent | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2316 | The agent-monitor object of the access log, the record code of a read, the field list of an entry and the migration step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2318 | The legacy story and the rwb-agent contract name different rights for the same read of the agent monitor | Security administrator | Resolved (directive) |
| GAP-2319 | The secondary slice carries no legacy acceptance criterion of its own, and the legacy data, endpoint, job and screen blocks belong to other services and other slices | Business analyst with the solution architect | Resolved (directive) |
| GAP-2332 | The access-event codes of a dashboard read, the entry field list, the page bounds, the read index and the Flyway step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2358 | The rwb-agent tool call, per-item field names and unavailable-read mapping behind RWB-P10-E2030-CON | Solution architect | Resolved (directive) |
| GAP-2359 | The checklist is keyed by stage and route while the legacy asks for the checklist of a case type | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2360 | The per-item fields of the document checklist answer the pack reader needs | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2361 | The defect status of a checklist item and the evidence it needs on the hub side | Business analyst, P5 | Resolved (directive) |
| GAP-2362 | The BRD section and L3 process of REQ-DCM-011 | Business analyst, programme | Resolved (directive) |
| GAP-2402 | No source gives the wire shapes, the value sets or the dependency rows this story needs: the append request and answer, the evaluation and run reads, the case-less approval row, the promotion decision code, the text of MSG-P7-009, the name behind EV-30 and the DP-02 login name | Solution architect, P7 rwb-decision, with the P10 rwb-agent owner, the rwb-case owner, the data steward and the delivery lead | Resolved (directive) |
| GAP-2576 | rwb-reporting steering dashboard (application slice): the consumed operation names, the workflow and activity names, the read-model design, the INT-19 replacement and the agent fact source are fixed by no single source | Solution architect, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the reporting service | Resolved (directive) |
| GAP-3100 | RWB-S8-E2029-APP: the confirmed-proposal raise has no published request shape beyond the legacy Java signature, no operation name for the agent-policy read, no published constraint for one open code, no envelope type for the decision-record entry and no test level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
