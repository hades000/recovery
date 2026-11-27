# RWB-SVC-P10 rwb-agent (Agent) - review pack, part 3 of 3 (RWB-P10-E2031-OPS to RWB-P10-TE013-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 15 |
| Resolved in the stories | 239 |
| Cross-document (pending in another document) | 251 |
| Not applied (value not in the sources) | 14 |
| Open business decisions | 17 |
| Register gaps linked | 62 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P10-E2031-OPS | 14 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2031 OPS Agent monitoring dashboard v2 [E3d] - deployment v2.md |
| RWB-P10-E2032-APP | 16 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2032 APP TDR offer-suggestion model through the model gateway [E3e] v2.md |
| RWB-P10-E2032-CON | 17 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2032 CON TDR offer-suggestion model through the model gateway [E3e] - contract v2.md |
| RWB-P10-E2032-INF | 8 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E2032 INF TDR offer-suggestion model through the model gateway [E3e] - infrastructure v2.md |
| RWB-P10-E3030-APP | 14 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E3030 APP Change an autonomy level v2.md |
| RWB-P10-E3030-CON | 16 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E3030 CON Change an autonomy level - contract v2.md |
| RWB-P10-E3031-APP | 8 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E3031 APP Detect model drift and raise a decision v2.md |
| RWB-P10-E8003-APP | 13 | 9 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E8003 APP Run a champion and challenger test v2.md |
| RWB-P10-E8004-APP | 11 | 10 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E8004 APP Raise or lower an autonomy level with approval v2.md |
| RWB-P10-E8004-CON | 13 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E8004 CON Raise or lower an autonomy level with approval - contract v2.md |
| RWB-P10-E8005-APP | 12 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E8005 APP Review agent risk at the committee v2.md |
| RWB-P10-E8005-CON | 15 | 5 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E8005 CON Review agent risk at the committee - contract v2.md |
| RWB-P10-TE013-APP | 29 | 27 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 TE013 APP Agent runtime client with fallback v2.md |
| RWB-P10-TE013-CON | 28 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 TE013 CON Agent runtime client with fallback - contract v2.md |
| RWB-P10-TE013-OPS | 25 | 20 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 TE013 OPS Agent runtime client with fallback - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P10-E8003-APP | R-00528 | CG-ALL-2866 | Script gap | Product owner | The story adds EVALUATION to the closed list LOV-AGENT-RUN | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P10-E2032-APP | R-09957 | CG-ALL-2827 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E2032-CON | R-09963 | CG-ALL-2840 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E3030-APP | R-09965 | CG-ALL-2850 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E3030-CON | R-09966 | CG-ALL-2858 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E8004-APP | R-09979 | CG-ALL-2883 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E8004-CON | R-09981 | CG-ALL-2892 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E8005-APP | R-09983 | CG-ALL-2898 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-P10-E3030-APP, RWB-P10-E3030-CON | R-22969 | GAP-1523 | Register gap | Risk and model risk officer | No target exists for agent acceptance, override, latency and cost, and no evidence or threshold exists for an autonomy change | The PRD writes no value. The measures and the threshold are policy rows, the dashboard shows the measure, and the four targets stay open as Q-P10-01 and Q-P10-02 until Risk sets them. The fallback rate below 10 percent is carried as the one stated target. |
| RWB-P10-E3030-APP, RWB-P10-E3030-CON, RWB-P10-E8004-APP, RWB-P10-E8004-CON | R-22970 | GAP-1477 | Register gap | Risk and model risk officer | The evidence and threshold for raising or lowering an agent autonomy level are not specified | Hold the measure, the threshold and the approval level per agent and per decision as a versioned row, keep the first autonomy level at its current setting, and let the committee set the threshold before any step-up is taken. |
| RWB-P10-E8005-APP, RWB-P10-E8005-CON | R-22973 | GAP-0642 | Register gap | Solution architect with the model risk function | Committee review of agent risk in rwb-agent: pack composition, window, export rule, score-fact read path, recorded version, right of the pack read and the Power BI integration point are not specified | Build the pack from the service's own rows: agent_run for performance and fallbacks, agent_feedback for acceptance and overrides over LOV-FEEDBACK, agent_alert for the incidents over LOV-AGENT-ALERT and agent_evaluation_run for the failure counts, with the window stated as one assumption; read the score facts through the rwb-source-data contract and never from the view; record the policy version in force with the agent, prompt and model versions of the reviewed runs and resolve no Drools package version; serve the pack on the two admin reads of `/api/recovery/agent/v1` through the gateway-bff route and state the CSV and JSON export rule; replace the Power BI integration point with the read operation and the export, because Arch v5 removes the lake; reconcile the pack right with rwb-access. |
| RWB-P10-TE013-CON, RWB-S4-E5012-APP, RWB-S4-E5012-CON | R-22978 | GAP-2793 | Register gap | Solution architect of S4 with the P10 architect and the business owner of S4 | The recommendation, its reasons and its cost and effect have no table, no operation and no vocabulary in any source | The proposal is not a business row: it is a view of the decision record answered on API-S4-003, with the step vocabulary as a versioned reference value, and the cost and effect are read on rwb-agent's contract under DP-20 with the rule as fallback. No sixth operation is added to the five of TSD S4 T-A.1 and the C row stays None until D1 or the plan owner rules otherwise. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E2032-ITG, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P7-E2032-APP, RWB-S2-E2032-APP | R-28842 | GAP-1531 | Register gap | Product owner | The boundary of the TDR suggestion message is not defined between rwb-agent and the treatment screen | The PRD requires that a caller learns that no suggestion is available and why, in the terms of the outcome the service recorded, and leaves the screen, the wording and the message ownership to the treatment PRD and the message standard. |
| RWB-ITG-TE013-ITG, RWB-P10-TE013-APP, RWB-P10-TE013-CON, RWB-P10-TE013-OPS, RWB-P7-TE013-APP | R-28926 | GAP-1320 | Register gap | P10 agent runtime business analyst with the model risk officer | No source fixes the model version of agent INTAKE, which the entry must carry | The model version of agent INTAKE is fixed with the approved policy of the agent in RWB-P10-TE013-CON and RWB-P10-TE013-APP and arrives inside the record; the fixtures of this story carry a synthetic model version and the criteria assert presence, not a value |
| RWB-P10-E8005-APP, RWB-P10-E8005-CON | R-28952 | GAP-1489 | Register gap | Risk and model risk officer | Agent acceptance, override, latency and cost are measured with no target and no baseline | Report the four measures per agent and per decision from the agent run record, and let the model risk owner set the targets before the first autonomy step-up. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P10-E2032-CON | R-15461 | DOR-RWB-P10-E2032-CON-4 | 7 | Definition of Ready item 4 Business rules: Partial | TC-08 checks BR1 to BR9, but AC7 is only a coverage check. Rule-specific criteria are still to be written. |
| RWB-P10-E2032-CON | R-30399 | NEWAC-RWB-P10-E2032-CON-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 and TC-08, TC-09 only check that coverage exists. Criteria stating the behaviour of each of BR1 to BR9 are still to be written. |
| RWB-P10-E2032-INF | R-04691 | DOR-RWB-P10-E2032-INF-16 Size: Fail | section header | Definition of Ready item 16 Size: Fail | Size is not in the sources. The item stays open until a size is given in a source. |
| RWB-P10-E3030-APP | R-04695 | DOR-RWB-P10-E3030-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found. Searched source folders for 'epic design'; hits were only scratch files under _work/msr, none a sign-off. A sign-off cannot be invented; no story edit. |
| RWB-P10-E3030-CON | R-04702 | DOR-RWB-P10-E3030-CON-16 | header | Definition of Ready item 16 Size: Fail | No size value exists in the sources, so the Size item stays open until the story is sized. |
| RWB-P10-E8003-APP | R-04711 | DOR-RWB-P10-E8003-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the source documents or the story. Sign-off cannot be invented; Not specified in the source documents (DOR-RWB-P10-E8003-APP-14). |
| RWB-P10-E8003-APP | R-04712 | DOR-RWB-P10-E8003-APP-16 | header | Definition of Ready item 16 Size: Fail | Size stays unspecified; the item stays open, so the Not applied status holds. |
| RWB-P10-E8003-APP | R-04713 | DOR-RWB-P10-E8003-APP-21 | find it | Definition of Ready item 21 Contract published: Fail | Depends on RWB-PLT-E1027-CON and RWB-PLT-N001-CON being Done, which a story text edit cannot change. Not specified in the source documents (DOR-RWB-P10-E8003-APP-21). |
| RWB-P10-E8003-APP | R-04714 | DOR-RWB-P10-E8003-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the source documents. Not specified in the source documents (DOR-RWB-P10-E8003-APP-22). |
| RWB-P10-E8004-APP | R-04717 | DOR-RWB-P10-E8004-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP08 epic design record in the sources; the sign-off cannot be stated. Grep of the .md sources found only the sign-off process, not a record. Scratch hits ignored. |
| RWB-P10-E8004-APP | R-04718 | DOR-RWB-P10-E8004-APP-16 | 1 | Definition of Ready item 16 Size: Fail | No size value exists in the sources; the squad sizes the story at refinement. |
| RWB-P10-E8004-APP | R-04720 | DOR-RWB-P10-E8004-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version is recorded in the P10 or service story files or the architecture md. A version cannot be invented; Not specified in the source documents (DOR-RWB-P10-E8004-APP-22). |
| RWB-P10-E8004-APP | R-22965 | GAP-0640 | 11 | RWB-E8-004 in rwb-agent: the autonomy level set, the approval reference column, which approval element carries the approved level, the evidence and the breach behind a change, the right the change needs against the legacy permission list, the route, the decision code, the message for a level outside the list and the migration number are not fixed by any source | Only the approval reference column is settled (ASM-5). Refusal wording and screen fields remain Not specified under GAP-0640, so the item is not fully resolved. |
| RWB-P10-TE013-OPS | R-04748 | DOR-RWB-P10-TE013-OPS-16 | header | Definition of Ready item 16 Size: Fail | Size row added as Not specified; no size value exists in the source documents, so the item stays open until the squad sizes the story. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (59)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04131 | RWB-P10-E2031-OPS | CG-ALL-2806 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-metrics in rwb-agent.yaml through RWB-P10-E2031-CON. |
| CDC-04132 | RWB-P10-E2031-OPS | CG-ALL-2807 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-runs in rwb-agent.yaml through RWB-P10-E2031-CON. |
| CDC-04133 | RWB-P10-E2031-OPS | CG-ALL-2808 | 12.1 | Publish GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs in rwb-agent.yaml through RWB-P10-E2031-CON. |
| CDC-04155 | RWB-P10-E2032-APP | CG-ALL-2818 | 12.1 | Publish the POST operation for the suggestion path through RWB-P10-E2032-CON, or remove it from 12.1. Path is not specified in the source documents (GAP-0633; ASM-0977). |
| CDC-04159 | RWB-P10-E2032-APP | DOR-RWB-P10-E2032-APP-8 | 12 | Add the suggestion POST operation under /api/recovery/agent/v1, with case ID, treatment ID and idempotency key TDR_OFFER:<treatmentId>. |
| CDC-04177 | RWB-P10-E2032-CON | CG-ALL-2831 | 12.1 | Publish the POST operation for the suggestion path (path Not specified in the source documents, GAP-0634; ASM-0977), or remove it from the owner's yaml. |
| CDC-04184 | RWB-P10-E2032-CON | GAP-1713 | none | Record the mapping of each prerequisite feature code to the owning service contract once; carry the duplicate FEAT-CHO-08 as written. |
| CDC-04207 | RWB-P10-E3030-APP | CG-ALL-2845 | 12.1 | Publish GET /api/recovery/agent/v1/admin/agent-configs in rwb-agent.yaml through RWB-P10-E3030-CON. |
| CDC-04208 | RWB-P10-E3030-APP | CG-ALL-2846 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs in rwb-agent.yaml through RWB-P10-E3030-CON. |
| CDC-04209 | RWB-P10-E3030-APP | CG-ALL-2847 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve in rwb-agent.yaml through RWB-P10-E3030-CON. |
| CDC-04212 | RWB-P10-E3030-APP | DOR-RWB-P10-E3030-APP-8 | 12.1 | Declare Idempotency-Key on POST agent-configs and POST agent-configs/{versionId}/approve and publish the three operations. |
| CDC-04215 | RWB-P10-E3030-CON | CG-ALL-2853 | 12.1 | Add path GET /api/recovery/agent/v1/admin/agent-configs |
| CDC-04216 | RWB-P10-E3030-CON | CG-ALL-2854 | 12.1 | Add path POST /api/recovery/agent/v1/admin/agent-configs |
| CDC-04217 | RWB-P10-E3030-CON | CG-ALL-2855 | 12.1 | Add path POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve |
| CDC-04219 | RWB-P10-E3030-CON | DOR-RWB-P10-E3030-CON-8 | 12.1, 12.3 | Add the three missing paths: GET and POST /api/recovery/agent/v1/admin/agent-configs and POST .../{versionId}/approve |
| CDC-04242 | RWB-P10-E8004-APP | CG-ALL-2878 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs through RWB-P10-E8004-CON, or remove it from 12.1. |
| CDC-04243 | RWB-P10-E8004-APP | CG-ALL-2879 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve through RWB-P10-E8004-CON, or remove it from 12.1. |
| CDC-04245 | RWB-P10-E8004-APP | DOR-RWB-P10-E8004-APP-8 | 12.1, 12.3 | Publish the two 12.1 operations (POST admin/agent-configs and POST admin/agent-configs/{versionId}/approve) through RWB-P10-E8004-CON, or remove them. |
| CDC-04252 | RWB-P10-E8004-CON | CG-ALL-2886 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs in rwb-agent.yaml; the story already carries this path. |
| CDC-04253 | RWB-P10-E8004-CON | CG-ALL-2887 | 12.1 | Publish POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve in rwb-agent.yaml. |
| CDC-04271 | RWB-P10-E8005-CON | CG-ALL-2902 | 12.1 | Add path GET /api/recovery/agent/v1/admin/agent-runs with the access and response declared in 12.1 |
| CDC-04272 | RWB-P10-E8005-CON | CG-ALL-2903 | 12.1 | Add path GET /api/recovery/agent/v1/admin/agent-metrics with the access and response declared in 12.1 |
| CDC-04274 | RWB-P10-E8005-CON | DOR-RWB-P10-E8005-CON-8 | 12.1 | Event type decision-record fixed in story at 12.3 and the relay line; the two missing yaml paths remain cross-document. |
| CDC-04303 | RWB-P10-TE013-CON | CG-ALL-2919 | 12.1 | Publish POST /api/recovery/agent/v1/agent-steps in rwb-agent.yaml through this CON story. |
| CDC-04304 | RWB-P10-TE013-CON | CG-ALL-2920 | 12.1 | Publish PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record in rwb-agent.yaml through this CON story. |
| CDC-04323 | RWB-P10-TE013-CON | GAP-2421 | 11, 12 | Publish the model_version of each live agent with the agent policy in the rwb-agent contract. Story side (assert equality with the run fixture) is in sections 11-12, not in chunk c05. |
| CDC-04330 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-23 | 3 | Add POST /agent-steps and PUT /agent-runs/{runId}/decision-record as fixed by RWB-P10-TE013-CON; the file (version 5.0.0) does not list them. |
| CDC-20699 | RWB-P10-E2031-OPS | R-00511 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20708 | RWB-P10-E2031-OPS | R-00512 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00498', 'R-00499', 'R-00500', 'R-00501', 'R-00502', 'R-00503', 'R-00504', 'R-00508', 'R-00511', 'R-00512', 'R-0 |
| CDC-20716 | RWB-P10-E2031-OPS | R-00513 |  | GET /cases/{caseId}/agent-outputs already in rwb-agent.yaml at L425 under base /api/recovery/agent/v1; no yaml change. |
| CDC-20717 | RWB-P10-E2031-OPS | R-04679 |  | Three REST paths already in rwb-agent.yaml; workflow and activity catalog belong in Temporal Catalog v1. |
| CDC-20718 | RWB-P10-E2032-APP | R-04685 |  | Suggestion POST path Not specified in the source documents (GAP-0633; ASM-0977); operation not added. |
| CDC-20719 | RWB-P10-E3030-APP | R-00519 |  | GET /admin/agent-configs already in rwb-agent.yaml at L86 under the single /api/recovery/agent/v1 base. |
| CDC-20720 | RWB-P10-E3030-APP | R-00520 |  | POST /admin/agent-configs already in rwb-agent.yaml at L128 under the single /api/recovery/agent/v1 base. |
| CDC-20721 | RWB-P10-E3030-APP | R-00521 |  | POST /admin/agent-configs/{versionId}/approve already in rwb-agent.yaml at L173. |
| CDC-20722 | RWB-P10-E3030-CON | R-00523 |  | GET /admin/agent-configs already in rwb-agent.yaml at L86 with the single prefix. |
| CDC-20723 | RWB-P10-E3030-CON | R-00524 |  | POST /admin/agent-configs already in rwb-agent.yaml at L128 with the single prefix. |
| CDC-20728 | RWB-P10-E3030-CON | R-00525 |  | POST /admin/agent-configs/{versionId}/approve is already in rwb-agent.yaml (line 172-173) under base /api/recovery/agent/v1. |
| CDC-20729 | RWB-P10-E3030-CON | R-04704 |  | GET and POST /admin/agent-configs (lines 86, 128) and POST .../{versionId}/approve (line 173) are already in rwb-agent.yaml. |
| CDC-20730 | RWB-P10-E8004-APP | R-00531 |  | POST /admin/agent-configs is already in rwb-agent.yaml (line 128) under the single REST base prefix. |
| CDC-20731 | RWB-P10-E8004-APP | R-00532 |  | POST /admin/agent-configs/{versionId}/approve is already in rwb-agent.yaml (lines 172-173). |
| CDC-20732 | RWB-P10-E8004-APP | R-04722 |  | Both 12.1 operations (POST admin/agent-configs line 128; POST approve line 173) are already in rwb-agent.yaml. |
| CDC-20733 | RWB-P10-E8004-CON | R-00534 |  | POST /admin/agent-configs is already in rwb-agent.yaml (line 128); the story path is unchanged. |
| CDC-20734 | RWB-P10-E8004-CON | R-00535 |  | POST /admin/agent-configs/{versionId}/approve is already in rwb-agent.yaml (line 173). |
| CDC-20735 | RWB-P10-E8004-CON | R-04726 |  | Both rwb-agent operations are already in rwb-agent.yaml (lines 128, 173). The authorise operation belongs in rwb-access.yaml, not this document. |
| CDC-20736 | RWB-P10-E8005-APP | R-00538 |  | GET /admin/agent-runs is already in rwb-agent.yaml (lines 42-43). |
| CDC-20737 | RWB-P10-E8005-APP | R-00539 |  | GET /admin/agent-metrics is already in rwb-agent.yaml (lines 370-371). |
| CDC-20738 | RWB-P10-E8005-APP | R-04731 |  | info.version 5.0.0 and the base path /api/recovery/agent/v1 are already in rwb-agent.yaml (lines 9, 14, 22). Both admin operations are present. |
| CDC-20739 | RWB-P10-E8005-APP | R-04732 |  | The two admin paths, POST /admin/agent-configs (line 128) and POST approve (line 173), are already in rwb-agent.yaml. |
| CDC-20760 | RWB-P10-TE013-APP | R-00544 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20761 | RWB-P10-TE013-APP | R-04742 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20762 | RWB-P10-E8005-CON | R-00541 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20763 | RWB-P10-E8005-CON | R-00542 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20764 | RWB-P10-TE013-APP | R-00545 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20765 | RWB-P10-TE013-CON | R-00546 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20766 | RWB-P10-TE013-OPS | R-04751 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20768 | RWB-P10-E8005-CON | R-04736 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20769 | RWB-P10-TE013-CON | R-28930 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |
| CDC-20770 | RWB-P10-TE013-CON | R-00547 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04140 | RWB-P10-E2031-OPS | CG-ALL-2811 | 12.5 | Add activity raiseCostAlerts to the Activities sheet, or name a catalogued activity in §12.5 |
| CDC-04141 | RWB-P10-E2031-OPS | CG-ALL-2812 | 12.5 | Add activity agentDrift to the Activities sheet, or name a catalogued activity in §12.5 |
| CDC-04142 | RWB-P10-E2031-OPS | CG-ALL-2813 | 12.5 | Add activity dispatchAgentAlerts to the Activities sheet, or name a catalogued activity in §12.5 |
| CDC-04161 | RWB-P10-E2032-APP | CG-ALL-2821 | 12.5 | Catalogue trigger and child-start origin stated in 12.5. Workflow ID form and start rule are marked Not specified in the source documents; the catalogue owner must state them. |
| CDC-04162 | RWB-P10-E2032-APP | CG-ALL-2822 | 12.5 | Add an Activities row for BuildTdrInputs on task queue rwb-agent, or name the catalogued activity used instead. |
| CDC-04163 | RWB-P10-E2032-APP | CG-ALL-2823 | 12.5 | Add an Activities row for CallModelGateway on task queue rwb-agent, or name the catalogued activity used instead. |
| CDC-04164 | RWB-P10-E2032-APP | CG-ALL-2824 | 12.5 | Add an Activities row for CheckGuardrail on task queue rwb-agent, or name the catalogued activity used instead. |
| CDC-04181 | RWB-P10-E2032-CON | CG-ALL-2837 | 12.5 | Add activity CheckGuardrail to the Activities sheet with its task queue rwb-agent, or name a catalogued activity in section 12.5. |
| CDC-04227 | RWB-P10-E3031-APP | DOR-RWB-P10-E3031-APP-8 | find it | Add activities DriftFacts and DriftEvaluate with task queue rwb-agent. Event type is fixed in this story (12.3, line 144). |
| CDC-04228 | RWB-P10-E3031-APP | CG-ALL-2861 | 12.5 | Add activity DriftFacts with task queue rwb-agent. |
| CDC-04229 | RWB-P10-E3031-APP | CG-ALL-2862 | 12.5 | Add activity DriftEvaluate with task queue rwb-agent. |
| CDC-04285 | RWB-P10-TE013-APP | CG-ALL-2911 | 12.5 | Add an Activities row ApplyAutonomyMode on task queue rwb-agent, or name a catalogued activity |
| CDC-04286 | RWB-P10-TE013-APP | CG-ALL-2912 | 12.5 | Add an Activities row LinkDecisionRecord on task queue rwb-agent, or name a catalogued activity |
| CDC-04306 | RWB-P10-TE013-CON | CG-ALL-2922 | 12.5 | Add activity ResolveAutonomyMode to the Activities sheet for queue rwb-agent. |
| CDC-04307 | RWB-P10-TE013-CON | CG-ALL-2923 | 12.5 | Add activity ApplyAutonomyMode to the Activities sheet for queue rwb-agent. |
| CDC-04308 | RWB-P10-TE013-CON | CG-ALL-2924 | 12.5 | Add activity LinkDecisionRecord to the Activities sheet for queue rwb-agent. |
| CDC-04331 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-8 | 12.5 | Add Activities rows for ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord on task queue rwb-agent. |
| CDC-04332 | RWB-P10-TE013-OPS | CG-ALL-2929 | 12.5 | Add an Activities row for ResolveAutonomyMode on task queue rwb-agent. |
| CDC-04333 | RWB-P10-TE013-OPS | CG-ALL-2930 | 12.5 | Add an Activities row for ApplyAutonomyMode on task queue rwb-agent. |
| CDC-04334 | RWB-P10-TE013-OPS | CG-ALL-2931 | 12.5 | Add an Activities row for LinkDecisionRecord on task queue rwb-agent. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04149 | RWB-P10-E2031-OPS | CG-ALL-2814 | 16 | Add rows to the Story test cases of the next version for TC-P10-E2031-OPS-01 to TC-P10-E2031-OPS-08, with Given, When and Then copied from the criterion each covers. |
| CDC-04165 | RWB-P10-E2032-APP | CG-ALL-2825 | 16 | Add rows TC-E2-032-11 to TC-E2-032-17 with Given, When and Then copied from the criteria they cover (AC9 to AC15). |
| CDC-04188 | RWB-P10-E2032-CON | CG-ALL-2838 | 16 | Add rows TC-P10-E2032-CON-01 to TC-P10-E2032-CON-06 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-04204 | RWB-P10-E2032-INF | CG-ALL-2842 | 16 | Add rows for TC-P10-E2032-INF-01 to TC-P10-E2032-INF-07 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-04213 | RWB-P10-E3030-APP | CG-ALL-2849 | 16 | Story §16 lists the IDs; v8 has no Given, When or Then rows for them. TC-E3-030-12 to -15 are new in §16 and also need v8 rows. |
| CDC-04214 | RWB-P10-E3030-APP | DOR-RWB-P10-E3030-APP-12 | 12.7, 16 | Add rows TC-E3-030-01 to TC-E3-030-13 with Given, When and Then copied from the criterion or §12.7 row each covers. |
| CDC-04221 | RWB-P10-E3030-CON | DOR-RWB-P10-E3030-CON-12 | 12.7, 16 | Register TC-P10-E3030-CON-01 to TC-P10-E3030-CON-08 in Test Cases v8 |
| CDC-04223 | RWB-P10-E3030-CON | CG-ALL-2857 | 16 | Add a row to Story test cases for each of TC-P10-E3030-CON-01 to TC-P10-E3030-CON-06, with Given, When and Then copied from the criterion it covers. |
| CDC-04230 | RWB-P10-E3031-APP | CG-ALL-2863 | 16 | Add rows TC-E3-031-01 to TC-E3-031-12 with Given, When and Then copied from the criteria they cover. |
| CDC-04231 | RWB-P10-E3031-APP | DOR-RWB-P10-E3031-APP-12 | 12.7, 16 | Add TC-E3-031-01 to TC-E3-031-14 under tab Story test cases with their Given, When and Then. |
| CDC-04240 | RWB-P10-E8003-APP | CG-ALL-2873 | 16 | Add rows TC-E8-003-01 to TC-E8-003-12 with Given, When and Then copied from the criteria they cover; include TC-E8-003-13 to TC-E8-003-16 in the next version |
| CDC-04248 | RWB-P10-E8004-APP | CG-ALL-2882 | 16 | Rows TC-E8-004-13 to -25 were added to section 16 in this story, so the Test Cases v8 rows must cover 25 IDs. |
| CDC-04260 | RWB-P10-E8004-CON | CG-ALL-2891 | 16 | Add rows for TC-P10-E8004-CON-01 to TC-P10-E8004-CON-08, with Given, When and Then copied from the criterion each covers. |
| CDC-04268 | RWB-P10-E8005-APP | CG-ALL-2897 | 16 | Add rows TC-E8-005-01 to TC-E8-005-13 with Given, When and Then copied from the criterion each covers |
| CDC-04269 | RWB-P10-E8005-APP | DOR-RWB-P10-E8005-APP-12 | 16 | Add the test case rows TC-E8-005-01 to TC-E8-005-15 under tab Story test cases with their Given, When and Then. |
| CDC-04275 | RWB-P10-E8005-CON | CG-ALL-2905 | 16 | Add rows for TC-P10-E8005-CON-01 to TC-P10-E8005-CON-09 with Given, When and Then copied from the criteria they cover; add -11 to -13 once they are in this story. |
| CDC-04319 | RWB-P10-TE013-CON | CG-ALL-2925 | 16 | Add rows for TC-P10-TE013-CON-01 to TC-P10-TE013-CON-06 with Given, When and Then copied from the criteria they cover. |
| CDC-04344 | RWB-P10-TE013-OPS | CG-ALL-2932 | 16 | Rows belong in the next Test Cases version; section 16 now lists nine test cases, TC-P10-TE013-OPS-01 to -09. |

### RWB-P10-E2032-CON (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04157 | RWB-P10-E2032-APP | DOR-RWB-P10-E2032-APP-21 | header | Complete the build and publish the contract; build status is currently Not started. |
| CDC-04158 | RWB-P10-E2032-APP | DOR-RWB-P10-E2032-APP-22 | header | Publish the contract fake library and record its version. |
| CDC-04168 | RWB-P10-E2032-APP | GAP-1713 | find it | Record once the owning service contract for each FEAT prerequisite (P7 approval, P3 case, P5 documents, P6 communications, S1 valuation); carry the duplicate FEAT-CHO-08 as written. |
| CDC-04169 | RWB-P10-E2032-APP | GAP-0634 | find it | Fix the operation under /api/recovery/agent/v1 with request and answer members, record member types, EV-28 payload, boundary error mapping and admin read pass-through. |
| CDC-04170 | RWB-P10-E2032-APP | GAP-0633 | find it | Fix the operation path below /api/recovery/agent/v1 with its media type and refusal codes; the other points are already stated in this story. |
| CDC-04171 | RWB-P10-E2032-APP | GAP-0414 | find it | Agree a one-hop REST start operation on the rwb-agent contract for a TDR suggestion run; QA lead fixes harness, stub controls, evidence format and gate at the wave 2 entry check. |
| CDC-04173 | RWB-P10-E2032-APP | GAP-1882 | find it | Fix the caller-side operation, request members and proposal columns in the wave 2 contract review; record override and fallback decision codes with rwb-decision before Done. |
| CDC-04192 | RWB-P10-E2032-INF | DOR-RWB-P10-E2032-INF-21 | section header | The story names and gates the dependency. The contract is published only when RWB-P10-E2032-CON, now Not started, is Done. |
| CDC-04193 | RWB-P10-E2032-INF | DOR-RWB-P10-E2032-INF-22 | header | Publish a contract fake library version for RWB-P10-E2032-CON and record it as published |
| CDC-04197 | RWB-P10-E2032-INF | GAP-1713 | find it | Map each FEAT prerequisite of the module once to the owning service contract (approval to P7, case to P3, documents to P5, communications to P6, valuation to S1); carry the duplicate FEAT-CHO-08 as written. |
| CDC-04198 | RWB-P10-E2032-INF | GAP-0634 | find it | Fix the suggestion operation under /api/recovery/agent/v1 with its request and answer members, the EV-28 payload from TSD P10 v2 T3.1, the boundary request and error mapping, and the admin reads restated from RWB-P10-E1058-CON. |
| CDC-04199 | RWB-P10-E2032-INF | GAP-0633 | find it | Place the suggestion operation under the base path, read account, payments and treatment through the named contracts, keep the 60-second exception on the suggestion call only, and record agent_version null. |
| CDC-04200 | RWB-P10-E2032-INF | GAP-0414 | find it | Agree a one-hop REST operation on the rwb-agent contract that starts a TDR suggestion run; QA lead fixes harness environment, stub controls, evidence format and gate at the wave 2 entry check. |
| CDC-04201 | RWB-P10-E2032-INF | GAP-1882 | find it | Fix the caller-side operation, request members and proposal columns at the wave 2 contract review; record override and fallback decision codes with rwb-decision before Done. |
| CDC-04203 | RWB-P10-E2032-INF | GAP-2403 | find it | Agree at wave 2 contract review: append on POST /api/recovery/decision/v1/decision-log, two reads with DecisionLogPage fields, LOV-DECISION D5, final-call list with SUGGESTION_RECORDED, reference-data path, MSG-P7-009 text and rwb-decision login name. |

### RWB-P10-TE013-CON (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04280 | RWB-P10-TE013-APP | DOR-RWB-P10-TE013-APP-21 | n/a | Complete RWB-P10-TE013-CON build to Done so the contract is published |
| CDC-04288 | RWB-P10-TE013-APP | GAP-1005 | find it | Name the extractor provider, model, model version and field-extraction route in the rwb-agent contract baseline; keep the route as a property of rwb-document with no model name in code. |
| CDC-04289 | RWB-P10-TE013-APP | GAP-2187 | find it | Publish the step and link operations with their members; record the 60 s budget as the single DP-11 exception in ADR-020; name the rwb-agent login with wave 1 schemas; settle the guardrail check-code list with RWB-P10-E1058-APP. |
| CDC-04290 | RWB-P10-TE013-APP | GAP-0381 | find it | Fix the client-to-agent call type, post-budget read through GET /api/recovery/agent/v1/admin/agent-runs, and the guardrail check-code list with the policy schema at the wave 1 contract review. |
| CDC-04291 | RWB-P10-TE013-APP | GAP-0620 | find it | Declare both operations under /api/recovery/agent/v1 with fixed member types, refusal set 401, 403, 409, 422, 503 and the UUID record reference, and the route pass-through name. |
| CDC-04295 | RWB-P10-TE013-APP | GAP-2188 | 3 | Fix the JSON spelling of the members ruleResult, inputs, confidence and record reference in the contract; settle types, refusal set and record reference with rwb-decision and rwb-case owners; name the route once RWB-PLT-N001-CON is baselined. |
| CDC-04328 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-21 | n/a | Set build status to Done with the contract published. |
| CDC-04329 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-22 | n/a | Publish the contract fake library version and record it as published. |
| CDC-04337 | RWB-P10-TE013-OPS | GAP-1005 | n/a | Gap sits in the rwb-agent contract baseline; no story text change needed. |
| CDC-04338 | RWB-P10-TE013-OPS | GAP-2187 | n/a | Seam, call type and login belong to the contract baseline and ADR-020. |
| CDC-04339 | RWB-P10-TE013-OPS | GAP-0381 | n/a | Call type and post-budget read are settled at the wave-1 contract review, outside this story. |
| CDC-04340 | RWB-P10-TE013-OPS | GAP-0620 | n/a | Contract shapes belong to the rwb-agent contract baseline; the story builds against them once published. |
| CDC-04341 | RWB-P10-TE013-OPS | GAP-1315 | n/a | Decision codes and key sets are approved in the contract and schema, not in this OPS story. |
| CDC-04343 | RWB-P10-TE013-OPS | GAP-2188 | 12 | Fix member names and JSON spelling of ruleResult, inputs, confidence and the record reference; leave types, confidence scale, refusal detail and record reference to review with the rwb-decision and rwb-case owners; name the route when RWB-PLT-N001-CON is baselined. |

### Epic design record (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04135 | RWB-P10-E2031-OPS | DOR-RWB-P10-E2031-OPS-14 | 3 | Record the signed epic design sign-off for RWB-P10-E2031-OPS so Definition of Ready item 14 passes. |
| CDC-04156 | RWB-P10-E2032-APP | DOR-RWB-P10-E2032-APP-14 | header | Record the signed epic design sign-off; none is in the source documents. |
| CDC-04191 | RWB-P10-E2032-INF | DOR-RWB-P10-E2032-INF-14 | header | Record the signed epic design sign-off for RWB-SVC-P10 and confirm it against this story |
| CDC-04218 | RWB-P10-E3030-CON | DOR-RWB-P10-E3030-CON-14 | find it | Record the signed epic design sign-off for EP03 |
| CDC-04255 | RWB-P10-E8004-CON | DOR-RWB-P10-E8004-CON-14 | none | Record the signed epic design sign-off for RWB-SVC-P10 in the epic design record. |
| CDC-04263 | RWB-P10-E8005-APP | DOR-RWB-P10-E8005-APP-14 |  | Record the signed epic design sign-off for EP08 |
| CDC-04278 | RWB-P10-TE013-APP | DOR-RWB-P10-TE013-APP-14 | n/a | Record or confirm the signed epic design sign-off for RWB-P10-TE013-APP |
| CDC-04305 | RWB-P10-TE013-CON | DOR-RWB-P10-TE013-CON-14 | Header | Record the signed epic design sign-off for RWB-P10-TE013-CON and cite it in the story. |
| CDC-04327 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-14 | n/a | Record the signed epic design sign-off for EP01-TE so the story can cite it. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04150 | RWB-P10-E2031-OPS | CG-ALL-2815 | 18 | Align the test lists of REQ-DRI-009 and REQ-APD-005 in RTM v7 with section 18 of this story, in the next RTM version. |
| CDC-04166 | RWB-P10-E2032-APP | DOR-RWB-P10-E2032-APP-12 | 12.7, 16, 18 | Align the §18 test lists of RWB-P10-E2032-APP with the RTM v7 rows for this story. |
| CDC-04176 | RWB-P10-E2032-APP | CG-ALL-2826 | 18 | Align the REQ-CHO-006 and REQ-DRI-001 test lists with section 18 of RWB-P10-E2032-APP in the next RTM version. |
| CDC-04189 | RWB-P10-E2032-CON | CG-ALL-2839 | 18 | Align the traces of REQ-CHO-006 and REQ-DRI-001 with section 18 (TC-P10-E2032-CON-01 to -03) in the next RTM version. |
| CDC-04205 | RWB-P10-E2032-INF | CG-ALL-2843 | 18 | Align the REQ-CHO-006 and REQ-DRI-001 test lists in RTM v7 with RWB-P10-E2032-INF §18 in its next version. |
| CDC-04287 | RWB-P10-TE013-APP | DOR-RWB-P10-TE013-APP-12 | 16 | Align the P3 section 18 test lists with RTM v7 |
| CDC-04296 | RWB-P10-TE013-APP | CG-ALL-2913 | 18 | Align the test cases traced to REQ-DRI-001 and the other two differing requirements with section 18 of this story in the next RTM version. |
| CDC-04320 | RWB-P10-TE013-CON | CG-ALL-2926 | 18 | Add to the test lists: REQ-DRI-001 TC-P10-TE013-CON-02, -05; REQ-DRI-005 TC-P10-TE013-CON-01, -05; REQ-ACA-010 TC-P10-TE013-CON-01. |
| CDC-04345 | RWB-P10-TE013-OPS | CG-ALL-2933 | 18 | Align the test lists of the three requirements that differ between the RTM and section 18 of RWB-P10-TE013-OPS in their next versions |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04236 | RWB-P10-E8003-APP | CG-ALL-2868 | 12.1 | Add message IDs for: 404 unknown evaluation run; 422 version label resolving to no policy row of the agent; 503 evaluation store down on a read or run start. |
| CDC-04247 | RWB-P10-E8004-APP | CG-ALL-2881 | 14 | Add a new message ID for 'The caller loaded the version and also approves it'; MSG-P7-002 keeps its standard meaning 'Approver prepared the decision'. |
| CDC-04250 | RWB-P10-E8004-APP | DOR-RWB-P10-E8004-APP-9 | 14 | The MSG-P7-002 row is replaced by a Not specified placeholder. |
| CDC-04258 | RWB-P10-E8004-CON | CG-ALL-2890 | 14 | Business analyst adds a new message ID for the loader who also approves, using the four-eyes wording; story then cites it. |
| CDC-04283 | RWB-P10-TE013-APP | CG-ALL-2909 | 12.1 | Add or name message IDs for 401 (no session or service identity), 409 (step key still RUNNING, or run holds another record) and 503 (store, workflow or contract unavailable). |
| CDC-04298 | RWB-P10-TE013-APP | GAP-2418 | 14 | Allocate message IDs and texts for the P7 not-found (404) answer and the chain-break report. MSG-P7-009 text is already there; no change to it. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04139 | RWB-P10-E2031-OPS | CG-ALL-2810 | 12.5 | Add an Activities row for aggregateAgentRuns on task queue rwb-agent, or name the catalogued replacement. |
| CDC-04179 | RWB-P10-E2032-CON | CG-ALL-2835 | 12.5 | Add activity BuildTdrInputs (rwb-agent) to the Activities sheet, or name a catalogued activity. |
| CDC-04180 | RWB-P10-E2032-CON | CG-ALL-2836 | 12.5 | Add activity CallModelGateway (rwb-agent) to the Activities sheet, or name a catalogued activity. |
| CDC-04237 | RWB-P10-E8003-APP | CG-ALL-2870 | 12.5 | Add activity VersionPairRunner on task queue rwb-agent |
| CDC-04284 | RWB-P10-TE013-APP | CG-ALL-2910 | 12.5 | Add activity ResolveAutonomyMode on task queue rwb-agent |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04182 | RWB-P10-E2032-CON | DOR-RWB-P10-E2032-CON-1 | 1 | Add the role 'tech lead' with its role code, or confirm the role code the story should use from the catalogue. |
| CDC-04194 | RWB-P10-E2032-INF | DOR-RWB-P10-E2032-INF-1 | 1 | Add a role for 'infrastructure engineer' with a role code, or confirm the existing role name that section 1 should use |
| CDC-04220 | RWB-P10-E3030-CON | DOR-RWB-P10-E3030-CON-1 | 1 | Add a role row for 'tech lead of rwb-agent' with its role code, or name the existing role of that scope |
| CDC-04309 | RWB-P10-TE013-CON | DOR-RWB-P10-TE013-CON-1 | 1 | Add 'tech lead' as a role code or role name, or map the section 1 persona to an existing role in that document. |
| CDC-04335 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-1 | 1 | Add 'platform engineer' as a role code or role name, or confirm the role name this story uses against the v5 role list |

### RWB-P10-E2031-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04136 | RWB-P10-E2031-OPS | DOR-RWB-P10-E2031-OPS-21 |  | Complete the contract publication so the build status is Done. |
| CDC-04137 | RWB-P10-E2031-OPS | DOR-RWB-P10-E2031-OPS-22 |  | Publish and record a contract fake library version for RWB-P10-E2031-CON. |
| CDC-04147 | RWB-P10-E2031-OPS | GAP-0630 | find it | Fix the seven added member names and four-decimal rule as additive within major version 1; keep paging and held-date status of RWB-P10-E1063-CON unchanged; name drift inputs after watch_measures members; declare agent-version filter and three decision-record elements as additive in rwb-decision; name notice path by owner; register route under RWB-PLT-N001-CON. |
| CDC-04154 | RWB-P10-E2031-OPS | GAP-2199 |  | Decision-log, comms and read-right items belong to the contract story; this deployment story reads no decision-log query, so nothing changes here. |

### RWB-P10-E8005-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04261 | RWB-P10-E8005-APP | CG-ALL-2894 | 12.1 | Add the path GET /api/recovery/agent/v1/admin/agent-runs with its operation to paths |
| CDC-04262 | RWB-P10-E8005-APP | CG-ALL-2895 | 12.1 | Add the path GET /api/recovery/agent/v1/admin/agent-metrics with its operation to paths |
| CDC-04266 | RWB-P10-E8005-APP | DOR-RWB-P10-E8005-APP-23 | header | Contract version row names the file and base path; version number shown as Not specified. |
| CDC-04267 | RWB-P10-E8005-APP | DOR-RWB-P10-E8005-APP-8 | 12.1, 12.3 | Publish the two admin paths in rwb-agent.yaml; event type fixed in the story (12.3) |

### RWB-P10-E2031-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04143 | RWB-P10-E2031-OPS | DOR-RWB-P10-E2031-OPS-10 | find it | Define empty, loading, error and no-access states for SCR-46 in the app story |
| CDC-04144 | RWB-P10-E2031-OPS | GAP-0629 | find it | Apply the proposed fix: drift step in the workflow of the v1 Schedule, segment read from the run row, override figures via the rwb-decision read with additive filter and elements, notice by owner, policy values in watch_measures, migration V10_007, login DP-02, route under RWB-PLT-N001-CON, right of API-P10-009 decided. |
| CDC-04151 | RWB-P10-E2031-OPS | GAP-2198 | find it | Apply the accepted defaults: drift as agentDrift in the Schedule, segment from run row, decision-log read of rwb-decision, notice via rwb-comms, policy values as approved rows, migration indexes only, additive element change, screen states from policy mode, range limits as configuration, windows as stated in the item. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04160 | RWB-P10-E2032-APP | CG-ALL-2817 | 11 | Record loan_account.principal_outstanding (DF-ACC-009, numeric(18,2), principal outstanding in baht, not personal). |
| CDC-04246 | RWB-P10-E8004-APP | CG-ALL-2877 | 11, 13 | `approval_ref` is kept as the agreed backward-compatible column (ASM-5); `approval` is the name of another entity. The model and classification need the field. |
| CDC-04249 | RWB-P10-E8004-APP | DOR-RWB-P10-E8004-APP-7 | 11 | Add approval_ref as the backward-compatible approval reference column of agent_policy in rwb_agent (ASM-5), and classify it in Data Classification v5. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04174 | RWB-P10-E2032-APP | GAP-1883 | 7 | Add the suggestion operation of RWB-P10-E2032-CON to the rwb-agent inbound list of slide 16 at the architecture review before wave 2 closes. |
| CDC-04186 | RWB-P10-E2032-CON | GAP-1883 | none | Slide 16 lists no inbound suggestion operation; the amendment goes to the architecture review before wave 2 closes. |
| CDC-04202 | RWB-P10-E2032-INF | GAP-1883 | find it | Add the suggestion operation of RWB-P10-E2032-CON to the rwb-agent inbound list on slide 16 through the architecture review before wave 2 closes. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04233 | RWB-P10-E8003-APP | CG-ALL-2867 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-04235 | RWB-P10-E8003-APP | DOR-RWB-P10-E8003-APP-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise (CG-ALL-2867). Other findings are fixed here by CG-ALL-2868, CG-ALL-2869, CG-ALL-2870 |
| CDC-04254 | RWB-P10-E8004-CON | CG-ALL-2888 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04148 | RWB-P10-E2031-OPS | GAP-2317 | find it | Add H RWB-PLT-E1027-CON for DP-03; H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON for DP-07; H RWB-PLT-E1044-CON for DP-15; H RWB-PLT-N001-CON for DP-19. Keep this Work Package metadata unchanged. |
| CDC-04325 | RWB-P10-TE013-CON | GAP-1319 | 13 | Add as DP-added: H PLT-E1027, E1072, E1043, TE006, E1071, E1044, N001 CON (RWB- keys); C RWB-P7-E1073-CON, RWB-P3-E1043-CON, RWB-P10-TE013-CON; the P4 authorise answer. Ready to start stays Day 1. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04183 | RWB-P10-E2032-CON | DOR-RWB-P10-E2032-CON-12 | 16 | Register TC-P10-E2032-CON-01 to TC-P10-E2032-CON-07 in Test Cases v8 and align the section 18 test lists of this story with RTM v7. |
| CDC-04196 | RWB-P10-E2032-INF | DOR-RWB-P10-E2032-INF-12 | 16, 18 | Add TC-P10-E2032-INF-01 to -07 rows to Test Cases v8; align the section 18 test lists with RTM v7 |

### RWB-P10-E3030-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04210 | RWB-P10-E3030-APP | DOR-RWB-P10-E3030-APP-21 | header | Build status to Done with the contract published, before this story starts. |
| CDC-04211 | RWB-P10-E3030-APP | DOR-RWB-P10-E3030-APP-22 | header | Publish a contract fake library version and record the version as published. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04234 | RWB-P10-E8003-APP | DOR-RWB-P10-E8003-APP-5 | 9 | Add value EVALUATION to the closed list LOV-AGENT-RUN |
| CDC-04294 | RWB-P10-TE013-APP | GAP-2417 | find it | Enumerate the agent-step decision code in LOV-DECISION before the first joint environment; keep agent run id, mode, fallback and reason in actions. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04238 | RWB-P10-E8003-APP | CG-ALL-2871 | 12.5 | Add a row for activity OutcomeComparator (type Activity, task queue rwb-agent) as named in section 12.5 |
| CDC-04239 | RWB-P10-E8003-APP | CG-ALL-2872 | 12.5 | Add a row for activity ComparisonWriter (type Activity, task queue rwb-agent) as named in section 12.5 |

### RWB-P10-E8004-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04244 | RWB-P10-E8004-APP | DOR-RWB-P10-E8004-APP-21 | find it | Set Build status to Done once the contract is published. |
| CDC-04251 | RWB-P10-E8004-APP | GAP-0641 | 3 | Fix the contract on the agreed readings: approval_ref holds the rwb-decision approval id; ApprovalDetail carries approval id, LOV-APPROVAL-STATUS status, decision code and approved autonomy level; 409 = version not LOADED or loaded by caller; 404 = unknown version id; repeat under same Idempotency-Key returns first answer; authorise route as the proposed fix states. |

### RWB-P10-E8005-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04264 | RWB-P10-E8005-APP | DOR-RWB-P10-E8005-APP-21 |  | Build the contract to Done so the contract is published |
| CDC-04265 | RWB-P10-E8005-APP | DOR-RWB-P10-E8005-APP-22 |  | Publish a contract fake library version and record it against this story |

### RWB-P10-TE013-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04276 | RWB-P10-TE013-APP | CG-ALL-2907 | 12.1 | Publish POST /api/recovery/agent/v1/agent-steps in rwb-agent.yaml through RWB-P10-TE013-CON |
| CDC-04277 | RWB-P10-TE013-APP | CG-ALL-2908 | 12.1 | Publish PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record in rwb-agent.yaml through RWB-P10-TE013-CON |

### RWB-P10-TE013-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04279 | RWB-P10-TE013-APP | DOR-RWB-P10-TE013-APP-16 | header | Size row added as a placeholder |
| CDC-04342 | RWB-P10-TE013-OPS | GAP-0619 | 12 | Fix the step operation as POST /api/recovery/agent/v1/agent-steps and the link operation as PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record, legacy members unchanged; the step has the 60 second policy budget as the single exception to the 2 s budget. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04301 | RWB-P10-TE013-APP | GAP-2425 |  | Index the event as rwb.decision-record.DecisionRecorded.v1 and tie it to the P7 event row, without changing the topic or payload. |
| CDC-04324 | RWB-P10-TE013-CON | GAP-2425 | 5 | Tie rwb.decision-record.DecisionRecorded.v1 to the P7 event row (EV-08, EV-09 or EV-30) once the catalog is indexed, without changing the topic or payload. |

### RWB-PLT-NF06-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04302 | RWB-P10-TE013-APP | GAP-1318 | find it | Allocate the rwb-decision database login name with its schema and write it into the platform secret store |
| CDC-04326 | RWB-P10-TE013-CON | GAP-1318 | find it | Allocate the rwb-decision database login name with its schema and write it into the platform secret store. No change to this story; it keeps the phrase. |

### RWB-S6-E5024-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04316 | RWB-P10-TE013-CON | GAP-1953 |  | Declare the pricing-agent run as consumed from RWB-P10-TE013-CON with the 60 s budget, schema-check verdict and rule fallback; add DP-20 and the RWB-PLT-TE013-CON and RWB-P10-TE013-CON rows. |
| CDC-04318 | RWB-P10-TE013-CON | GAP-2975 |  | Record the four consumed rows as class C with placeholders, add C RWB-P10-TE013-CON and RWB-PLT-TE006-CON, read the rule values into rule rows with placeholders, and adopt REQ-S6-002. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04134 | RWB-P10-E2031-OPS | CG-ALL-2809 | 12.5 | Add a Workflows row for AgentRunDailyRollupWorkflow on task queue rwb-agent, or name the catalogued replacement. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04138 | RWB-P10-E2031-OPS | DOR-RWB-P10-E2031-OPS-8 | 12.1, 12.5 | Publish the three REST paths in rwb-agent.yaml and catalog the workflow and activity, per CG-ALL-2806 to 2810. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04145 | RWB-P10-E2031-OPS | GAP-2316 | find it | Add the object-type code of the agent monitor, the DP-03 record code, the entry field list, the page bounds, the read index name and the Flyway step to the next access-log contract version. |

### RWB-ITG-E2031-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04146 | RWB-P10-E2031-OPS | GAP-0413 | find it | Agree with the QA lead the SIT harness profile, seed pack for INTAKE and SCREENING (weeks 2026-12-01..07 and 2026-12-08..14, November 2026), fixed clock at 2026-12-14, evidence format and gate; confirm the drift Schedule runs in rwb-agent. |

### OTHER:RWB-E2-031 Work Package plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04152 | RWB-P10-E2031-OPS | GAP-2201 |  | This story cites no ASM-B-P10-02 id and shares no output path; the fanout and check fix sits in the Work Package plan, not in this story. |

### RWB-P4-E2031-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04153 | RWB-P10-E2031-OPS | GAP-2319 |  | Boundary belongs to the secondary slice RWB-P4-E2031-APP; this story already keeps TC-E2-031 ids out of section 16 and no legacy master change is made here. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04167 | RWB-P10-E2032-APP | DOR-RWB-P10-E2032-APP-7 | 11 | Section 11 now marks DF-ACC-009 as not in LDM v9. The decision-log wording in the criteria is handled under CG-ALL-2828. |

### RWB-P10-E2032-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04172 | RWB-P10-E2032-APP | GAP-0635 | find it | Provision the INT-23 host, port, certificate, Key Vault names, login, topic partitions, retention and retry, budgets and alarms as reviewed values per environment. |

### RWB-P10-E2032-CON; OTHER:T-A.1; OTHER:T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04175 | RWB-P10-E2032-APP | GAP-2403 | 7 | Agree the append and read shapes, LOV-DECISION value D5, final-call value SUGGESTION_RECORDED, reference-data path, MSG-P7-009 text and rwb-decision login at wave 2 contract review. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04178 | RWB-P10-E2032-CON | DOR-RWB-P10-E2032-CON-16 | section header | Size row set to Not specified in the source documents |

### OTHER:Infrastructure environment values record (SCB IT infrastructure) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04185 | RWB-P10-E2032-CON | GAP-0635 | none | Environment values are absent from every source; provisioning and reviewed per-environment values are needed. |

### RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04187 | RWB-P10-E2032-CON | GAP-2403 | 12 | At wave 2 contract review fix: POST /api/recovery/decision/v1/decision-log with request and DecisionRecord answer; DecisionLogPage and DecisionLogEntry reads; reference-data path; LOV-DECISION value D5; final-call list with SUGGESTION_RECORDED; MSG-P7-009 text; rwb-decision login name. |

### OTHER:decision row naming who confirms the model exists (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04190 | RWB-P10-E2032-CON | GAP-1463 | section 3 | Confirming party set to Not specified in the source documents |

### OTHER:Screen specification for SCR-14 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04195 | RWB-P10-E2032-INF | DOR-RWB-P10-E2032-INF-10 | 3 | Add empty, loading, error and no-access states for SCR-14, or confirm this story owns no screen |

### OTHER:03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04206 | RWB-P10-E2032-INF | GAP-1463 |  | Add a decision row for BR-E2-032 (RWB-E2-032): Restructure operations officer with the TDR team confirms the model exists; date needed: Not specified in the source documents (GAP-1463). |

### RWB-P10-AD020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04222 | RWB-P10-E3030-CON | GAP-0636 | 8, 11 | Approval instant recorded in section 11 as updated_at; autonomy value set and unit of change marked Not specified; per-decision key referenced to the other story. |

### RWB-PLT-E1027-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04224 | RWB-P10-E3031-APP | DOR-RWB-P10-E3031-APP-21 | find it | Publish the contract these stories provide and bring both stories to Done. |

### OTHER:Contract fake library (not named in source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04225 | RWB-P10-E3031-APP | DOR-RWB-P10-E3031-APP-22 | find it | Publish a contract fake library version and record its version in the contract sources. |

### OTHER:Owner of the rwb-source-data score-facts operation version (not named in source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04226 | RWB-P10-E3031-APP | DOR-RWB-P10-E3031-APP-23 | 12 | Story records the topic and the /api/recovery/agent/v1 path versions and marks the score-facts operation version Not specified (GAP-0646). |

### OTHER:rwb-agent and rwb-source-data contracts (with rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04232 | RWB-P10-E3031-APP | GAP-0646 | 15 | Publish the segment composition and the score-fact read operation before wave 2 exit; settle the review-date rule and the RW-RISK right with rwb-access. |

### RWB-P10-E1058-CON; OTHER:rwb-source-data contract; OTHER:Epic 8 BRD; OTHER:policy version rows (RW-COE; OTHER:RW-RISK) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04241 | RWB-P10-E8003-APP | GAP-0645 |  | Open in the named sources; the story cannot resolve these. Owner: tech lead. Story unchanged for this gap. |

### OTHER:Size at refinement (not in source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04256 | RWB-P10-E8004-CON | DOR-RWB-P10-E8004-CON-16 | header | Size row shows Not specified; no process claim added |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04257 | RWB-P10-E8004-CON | DOR-RWB-P10-E8004-CON-8 | 12.1 | Publish the two rwb-agent operations in rwb-agent.yaml and the authorise operation in rwb-access.yaml; event type already fixed in story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04259 | RWB-P10-E8004-CON | GAP-0641 | 11 | Approval reference name and type left Not specified; repeat-call assertion limited to returning the first answer |

### OTHER:TSD P10 v2 and the rwb-agent API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04270 | RWB-P10-E8005-APP | GAP-0643 |  | Publish AgentRunsPack and AgentMetricsPack shapes with members named after TSD columns, mark open elements as additive, fix the CSV and JSON export rule, declare the committee-outcome members as an additive set, and write the fake fixtures. |

### RWB-P10-E8005-CON; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04273 | RWB-P10-E8005-CON | DOR-RWB-P10-E8005-CON-14 | 3 | Record the signed epic design sign-off for RWB-P10-E8005-CON as the baseline this contract serves; no epic design record is named in the story or the source excerpts. |

### OTHER:Owner of the wave 0 contract fakes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04281 | RWB-P10-TE013-APP | DOR-RWB-P10-TE013-APP-22 | 12.8 | Fake is named in 12.8 with library version Not specified; publishing the fake is outside this story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04282 | RWB-P10-TE013-APP | DOR-RWB-P10-TE013-APP-8 | 4, 12.1, 12.5 | Publish the two operations, add activity ResolveAutonomyMode, and map the error statuses to message IDs (CG-ALL-2907, 2908, 2909, 2910) |

### OTHER:TSD P7 v2 (T3.1; OTHER:T3.2) and the rwb-decision OpenAPI of wave 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04292 | RWB-P10-TE013-APP | GAP-1315 | find it | Approve at wave 1 design review the actions key set of an agent-step entry, the LOV-DECISION code for an agent step, and the request and answer field set of the two ledger reads. |

### OTHER:Wave 1 message catalogue of rwb-decision with the P7 topic contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04293 | RWB-P10-TE013-APP | GAP-1317 | find it | Approve the text of MSG-P7-009 and the retry, dead-letter and alert treatment of a refused record. |

### OTHER:Deployment slice (DevOps lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04297 | RWB-P10-TE013-APP | GAP-2189 | 5 | Carry chart values per environment, reference the agent login through a platform secret, draft five alert rules and six runbook entries for on-call sign-off, and publish the route from the edge contract when baselined. |

### OTHER:Service template and platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04299 | RWB-P10-TE013-APP | GAP-2420 | 13 | Take the service login, consumer group, Flyway user and property names from the template; take the chain-check time from the decision-log store slice (JOB-14). |

### OTHER:rwb-agent API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04300 | RWB-P10-TE013-APP | GAP-2421 | 11 | Publish the model version of each live agent with the agent policy; until then assert equality with the run fixture, not a literal. |

### OTHER:P3 screen specification of SCR-46 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04310 | RWB-P10-TE013-CON | DOR-RWB-P10-TE013-CON-10 | find it | Declare the empty, loading, error and no-access states of SCR-46 in P3; this rwb-agent contract story has no screen to carry them. |

### RWB-S8-E7006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04311 | RWB-P10-TE013-CON | GAP-3061 | find it | Keep the H, C, I and X rows; declare the four consumed rows class C with placeholders and fakes; record the absent DP-05, DP-09, DP-14 and DP-20 rows in the registers. |

### OTHER:SCB IT infrastructure and DevOps deployment values (per environment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04312 | RWB-P10-TE013-CON | GAP-0621 |  | Reviewed per-environment values for login secret, topic rights, worker concurrency, alert thresholds, route path and capacity figures. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04313 | RWB-P10-TE013-CON | GAP-2419 |  | Treat seven platform contracts and RWB-P3-E1043-CON as wave 0 contract fakes, add authorise row; header dependency rows stay as the Work Package fixes them. |

### OTHER:S1 rwb-valuation story set (FEAT-VAL-03) and its split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04314 | RWB-P10-TE013-CON | GAP-2597 |  | Declare the market benchmark as an input element of the outlier step with its source name, source date and version on the first publishing contract; keep the placeholder and no path until one owner publishes it. |

### OTHER:split plan for the S1 rwb-valuation key (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04315 | RWB-P10-TE013-CON | GAP-2625 |  | If the agent call is a client of the valuation service, add DP-20 and C RWB-P10-TE013-CON to the plan row and declare the row against this contract. |

### RWB-S7-E6015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04317 | RWB-P10-TE013-CON | GAP-3021 |  | Record the seven consumed rows as class C with placeholders, add C RWB-P10-TE013-CON, RWB-PLT-TE006-CON, RWB-PLT-E1072-CON and RWB-P7-E1073-CON, and adopt REQ-S7-002. |

### RWB-P10-TE013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04321 | RWB-P10-TE013-CON | GAP-2189 | 13 | Environment values as chart values reviewed per environment; login by platform secret; draft five alert rules and six runbook entries for on-call sign-off; publish the route from the baselined edge contract. |

### OTHER:decision-log store slice (owner of JOB-14) and service template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04322 | RWB-P10-TE013-CON | GAP-2420 | 13 | State the nightly chain-check time, timezone and overlap policy of JOB-14. Take the login, consumer group, Flyway user and property names from the service template and platform DB story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04336 | RWB-P10-TE013-OPS | DOR-RWB-P10-TE013-OPS-12 | 12, 12.7, 16, 18 | Add TC-P10-TE013-OPS-01 to -09 with their Covers; align the section 18 test lists with RTM v7 |

### OTHER:Next story-set version (metadata rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04346 | RWB-P10-TE013-OPS | GAP-1319 | n/a | DP-added dependencies are carried in the dependency map; Ready to start Day 1 is kept; metadata rows are corrected at the next story-set version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-decision.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20597 | RWB-P10-TE013-APP | R-22930 |  | Retry (1 min, 10 min, 1 h), .dlt dead-letter and alert treatment already in x-topic. MSG-P7-009 wording is not in this document; no criterion depends on it. |

### 12 Project communication/Recovery Workbench Document Control Sheet v13.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20607 | RWB-P10-TE013-OPS | R-28934 |  | Metadata rows are corrected at the next story-set version, not this sheet; DP dependencies stay in the dependency map and Ready to start Day 1 is kept. No sheet edit made. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20861 | RWB-P10-E2032-CON | R-22678 |  | INT-23 and per-environment values Not specified in the source documents (GAP-0635). Values belong in the SCB IT infrastructure environment register. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0080 | The agent platform of DL33 is never named as a service | TechX | Resolved (directive) |
| GAP-0083 | The tool gateway's target systems are not named | TechX | Resolved (directive) |
| GAP-0381 | The call type between the client and rwb-agent, the run result after the 60 second budget and the guardrail check codes are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0413 | SIT harness environment, two-week and November seed, fixed clock, cost reconciliation fixture, evidence and gate for the agent-monitor journey | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0414 | The TDR suggestion has no agreed start operation: the legacy treatment side calls rwb-agent in process, Architecture v5 gives no S2-to-P10 call, and no source gives the harness environment, the TDR model stub controls, the evidence format or the gate | Integration lead | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0619 | The app slice of the agent runtime client: the two operations the legacy Java interface spans, the call type and the budget of a step, the login, the record write and its link, the guardrail check-code list and the route in front of the run read are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-decision, rwb-case and rwb-access | Resolved (directive) |
| GAP-0620 | The client contract: the operation paths and the member types beyond the legacy Java records, the refusal set, the 409 of an in-flight repeat, the record reference and the route in front of the run read are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0621 | The deployment slice of the agent runtime client: the chart values, the login secret, the topic rights of the shared decision-record topic, the worker concurrency, the alert thresholds, the route path and the capacity figures are not specified by any source | SCB IT infrastructure and the DevOps team with the ACE platform team and security | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0631 | The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified | Platform administrator | Resolved (directive) |
| GAP-0633 | The TDR offer-suggestion slice in rwb-agent: the operation path below the base, the treatment and account read operations, the parameter keys, the screen route, the run version fields, the inputs reference and the two waits of the call are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-treatment, rwb-case and rwb-decision | Resolved (directive) |
| GAP-0634 | The TDR offer-suggestion contract slice: the operation path and request members, the record member types, the boundary answer and error mapping, the admin read route and the two-wait exception are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision, rwb-treatment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-0635 | The infrastructure slice of the TDR offer-suggestion key: the INT-23 host, port, certificate and Key Vault names, the partition and retention values, the sizing, the budget measurement points and the alarm thresholds are not specified by any source | SCB IT infrastructure with the ACE platform team and security | Resolved (directive) |
| GAP-0636 | The decision scope of a version, the autonomy value set, the right of the change, the record rule version, the load file and the approval instant are not fixed by any source | Solution architect with the service owner of rwb-agent and the owners of rwb-decision, rwb-access and rwb-case | Resolved (directive) |
| GAP-0637 | The operation path of a configuration change, the record payload members, the approval instant, the kind value set and the state mapping are not fixed by one source | Solution architect with the service owner of rwb-agent and the owners of rwb-decision and rwb-access | Resolved (directive) |
| GAP-0640 | RWB-E8-004 in rwb-agent: the autonomy level set, the approval reference column, which approval element carries the approved level, the evidence and the breach behind a change, the right the change needs against the legacy permission list, the route, the decision code, the message for a level outside the list and the migration number are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0641 | The approval-gated version-change contract of rwb-agent: the field detail of the consumed approval answer, the name and type of the approval reference, the meaning of each 409 and 404, who calls the authorise operation, the record element map of a change with no rule, and the test of a repeated call are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0643 | Committee-review read contract of rwb-agent: response element names, export contract, record payload members, errors and the pack right are not published by any source | Solution architect with the tech lead of rwb-agent | Resolved (directive) |
| GAP-0645 | RWB-E8-003 in rwb-agent: the champion/challenger request fields, the comparison measure and its policy row, the P1 score-fact read, the version of a score row, the proposal shape, the migration number, the evaluation-run name and the requirement row are not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0646 | Drift thresholds, the drift window, the segment composition, the score-fact read path and the requirement ID are not fixed by any source | Service owner of rwb-agent with the Center of Excellence analyst and the service owner of rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1009 | The field-extraction route of the rwb-agent contract, its answer field names and its model version are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1315 | The key set of the decision entry of an agent step, the sub-decision code beside the route code, and the field set of the two ledger reads have no source | Solution architect, P7 rwb-decision, with the P10 agent runtime business analyst and the data steward | Resolved (directive) |
| GAP-1316 | The operation and parameter names of the agent fallback-rate measure have no source | Data steward with the P9 reporting analyst and the P10 agent runtime business analyst | Resolved (directive) |
| GAP-1317 | The text of MSG-P7-009 and the shape of an append that is refused are not written out in any source | Solution architect, P7 rwb-decision, with the platform event team | Resolved (directive) |
| GAP-1318 | The name of the per-service database login is not fixed by any source | ACE DB team with the platform team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1463 | RWB-E2-032 is conditional on a model existing and no decision row names who confirms it | Restructure operations officer with the TDR team | Resolved (directive) |
| GAP-1480 | An Epic 3 feature depends on an Epic 8 administration feature | Solution architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1882 | The treatment-side use of the suggestion is unspecified: the agent-run operation and its payload on the caller side, the treatment columns that hold the proposal and the model, prompt and policy versions, the 60 s wait and its fallback contract, and the decision code of a suggestion record | Solution architect | Resolved (directive) |
| GAP-1883 | Architecture v5 slide 16 publishes no inbound suggestion operation on rwb-agent, while the legacy treatment flow calls one synchronously | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1953 | RWB-S6-E5024: the price estimate is an rwb-agent pricing-agent call with no DP-20 row in the plan and no published operation | Solution architect | Resolved (directive) |
| GAP-2187 | The agent runtime client has no published operation, no call type and no target-side home for the record write | Solution architect | Resolved (directive) |
| GAP-2188 | The client contract has no source member types, refusal detail or record reference shape | Solution architect | Resolved (directive) |
| GAP-2189 | The release has no source topology, sizing, login name, alert threshold, runbook text or route path | DevOps lead | Resolved (directive) |
| GAP-2198 | RWB-E2-031 version 2 app slice: the drift step and its Schedule, the segment source, the decision-log read, the notice, the policy values, the migration scope, the element change, the screen states, the login, the route path, the range limits and the two windows are not named by the sources | Tech lead of rwb-agent with the solution architect | Resolved (directive) |
| GAP-2199 | RWB-E2-031 version 2 contract slice: the decision-log filter and override element, the notice operation, the name of the read right, the paging and member types, the route path, the login and the Schedule step names are not fixed by the sources | Tech lead of rwb-agent with the owners of rwb-decision, rwb-comms and rwb-access | Resolved (directive) |
| GAP-2200 | RWB-E2-031 version 2 deployment slice: the route path, the login secret, the topology and budget, the notice operation, the Schedule registration detail and the model gateway egress are not fixed by the sources | DevOps engineer with the platform administrator and the security administrator | Resolved (directive) |
| GAP-2201 | Two Work Packages write the same three story files, the same three fragments and two overlapping assumption sets for legacy RWB-E2-031 on rwb-agent | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2316 | The agent-monitor object of the access log, the record code of a read, the field list of an entry and the migration step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2318 | The legacy story and the rwb-agent contract name different rights for the same read of the agent monitor | Security administrator | Resolved (directive) |
| GAP-2319 | The secondary slice carries no legacy acceptance criterion of its own, and the legacy data, endpoint, job and screen blocks belong to other services and other slices | Business analyst with the solution architect | Resolved (directive) |
| GAP-2403 | No source gives the wire shape or the value sets this story needs: the append request and answer, the ledger read and its page, the reference-data operation, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2417 | The decision code of an agent step and the placement and key set of the agent run, the mode, the fallback and its reason are in no source | Solution architect | Resolved (directive) |
| GAP-2418 | The text of MSG-P7-009 and the identifiers and texts of the not-found answer and the chain-break report are not written in any source | Business analyst, P7 | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2420 | The per-service login name, the environment and property names and the time of the chain check are in no source | Solution architect | Resolved (directive) |
| GAP-2421 | The model version of agent INTAKE is named in no source | Solution architect | Resolved (directive) |
| GAP-2422 | The legacy story says the client publishes no event while DP-03 requires the record on the shared decision-record topic | Solution architect | Resolved (directive) |
| GAP-2423 | The fixed story path already held an artefact of the superseded Work Package B-P7-05 whose citations resolve to no register row | Documentation lead | Resolved (directive) |
| GAP-2424 | The fallback-rate measure, its operation name and its threshold ownership are in no source | Business analyst, P7 | Resolved (directive) |
| GAP-2425 | The EV number of the DecisionRecorded event is left open by the Ownership Map among three P7 events | Solution architect | Resolved (directive) |
| GAP-2597 | The market value has no published owner, operation or element, and the model gateway the FSD names is not a contract of this service | Solution architect of S1 with the owner of rwb-agent (P10) and the owner of rwb-source-data (P1) | Resolved (directive) |
| GAP-2625 | The route agent is a service of its own and DP-20 with its C row RWB-P10-TE013-CON is not in this key's pattern set | S1 rwb-valuation service owner with the P10 rwb-agent owner | Resolved (directive) |
| GAP-2975 | RWB-S6-E5024-APP: the lot build and price slice has no plan row for its four consumed contracts, its agent contract, the R-DS-04 criterion split, the rules that carry no value or the outbox library | Solution architect | Resolved (directive) |
| GAP-3021 | RWB-S7-E6015-APP: the pack slice has no plan row for its seven consumed contracts, its agent, outbox and rule-kit dependencies, its pack columns, its requirement id or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3061 | RWB-S8-E7006-APP: the X6 slice has no plan row for its consumed contracts, its skip-trace sources, its events, its agent dispatch, its 30-day clock or the deviation service level | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P10-E3030-CON | Not specified without item ID | 168 | \| BR2 \| The autonomy mode is one of the values of LOV-AUTONOMY (value set Not specified in the source documents, GAP-0636) and the status one of the values of L |
