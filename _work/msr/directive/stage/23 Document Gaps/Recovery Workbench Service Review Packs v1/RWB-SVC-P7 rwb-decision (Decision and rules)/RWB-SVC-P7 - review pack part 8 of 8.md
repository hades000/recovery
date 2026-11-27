# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 8 of 8 (RWB-P7-TE013-APP to RWB-P7-TE013-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 1 |
| Resolved in the stories | 28 |
| Cross-document (pending in another document) | 22 |
| Not applied (value not in the sources) | 5 |
| Open business decisions | 2 |
| Register gaps linked | 25 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-TE013-APP | 28 | 22 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 TE013 APP Agent runtime client with fallback v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-TE013-APP | R-11383 | CG-ALL-7479 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-TE013-ITG, RWB-P10-TE013-APP, RWB-P10-TE013-CON, RWB-P10-TE013-OPS, RWB-P7-TE013-APP | R-28926 | GAP-1320 | Register gap | P10 agent runtime business analyst with the model risk officer | No source fixes the model version of agent INTAKE, which the entry must carry | The model version of agent INTAKE is fixed with the approved policy of the agent in RWB-P10-TE013-CON and RWB-P10-TE013-APP and arrives inside the record; the fixtures of this story carry a synthetic model version and the criteria assert presence, not a value |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-TE013-APP | R-06962 | DOR-RWB-P7-TE013-APP-8 | 12.1 | Definition of Ready item 8 Contract: Fail | Error and Message Standard v4 has no 401 or 404 IDs, so they stay marked. The P1 event name in section 12 was not in this chunk, so it is not applied. |
| RWB-P7-TE013-APP | R-18219 | DOR-RWB-P7-TE013-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Seven uncovered rules need AC text in section 7 and TC rows in section 16, neither in this chunk. No edit made. |
| RWB-P7-TE013-APP | R-26452 | CG-ALL-7480 | 3, 3.1 | Flyway file V2026_11_02__declog_agent_step_profile.sql is not in the V0001..Vnnnn form | Next V-number of the rwb-decision Flyway sequence is not in the sources (searched folder). Migration name not in this chunk. No edit made. |
| RWB-P7-TE013-APP | R-28928 | GAP-2418 | 14 | The text of MSG-P7-009 and the identifiers and texts of the not-found answer and the chain-break report are not written in any source | No source writes MSG-P7-009 text or ids for the 404 and chain-break outcomes (FSD P7 v3, PRD P7 v1, TSD P7 v2). Needs text authored by the P7 business analyst. |
| RWB-P7-TE013-APP | R-28934 | GAP-1319 | 9 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Section 9 is not in this chunk, so no edit was made. Metadata row correction is deferred to the next story version per the directive. |

## 5. Cross-document changes (pending in the target document)


### RWB-P10-TE013-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12819 | RWB-P7-TE013-APP | DOR-RWB-P7-TE013-APP-21 |  | Publish the contract story RWB-P10-TE013-CON with the DP-20 contract row |
| CDC-12820 | RWB-P7-TE013-APP | DOR-RWB-P7-TE013-APP-22 |  | Record the published fake library version |
| CDC-12825 | RWB-P7-TE013-APP | GAP-1005 | find it | Name the extractor provider, model name, model version and field-extraction route in the rwb-agent contract baseline; keep the route a property of rwb-document with no model name in code. |
| CDC-12826 | RWB-P7-TE013-APP | GAP-2187 | find it | Publish the run-submit and run-to-record link operations with their members; record the 60 s budget as the single DP-11 exception in ADR-020; name the rwb-agent login; settle the guardrail code list with RWB-P10-E1058-APP. |
| CDC-12827 | RWB-P7-TE013-APP | GAP-0381 | find it | Fix the client-to-agent call type and the post-budget read at the wave-1 review: AgentRunWorkflow start with the policy timeout, TIMED_OUT handling, run read on GET /api/recovery/agent/v1/admin/agent-runs; publish the guardrail check code list with the policy schema. |
| CDC-12828 | RWB-P7-TE013-APP | GAP-0620 | find it | Declare the step submit and link operations under /api/recovery/agent/v1 with fixed member types; set refusals 401, 403, 409, 422, 503 with 409 for a RUNNING step key or a run already holding a record; state the record reference as UUID with rwb-decision read-back. |
| CDC-12830 | RWB-P7-TE013-APP | GAP-0619 | 12 | Fix POST /api/recovery/agent/v1/agent-steps and PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record with legacy members unchanged; the step operation is the one recorded exception to the 2 s budget with a 60 s budget. |
| CDC-12832 | RWB-P7-TE013-APP | GAP-2188 | 12 | Fix member names and JSON spelling of ruleResult, inputs, confidence and record reference; settle refusal set and reference shape with rwb-decision and rwb-case owners; name the route once RWB-PLT-N001-CON is baselined. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12816 | RWB-P7-TE013-APP | CG-ALL-7473 | 13 | Solution architect to name the existing story file for RWB-P7-E1073-CON or create it |
| CDC-12818 | RWB-P7-TE013-APP | DOR-RWB-P7-TE013-APP-17 | 13 | Solution architect to name or create the story file for RWB-P7-E1073-CON, the same-service contract of DP-04 |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12822 | RWB-P7-TE013-APP | CG-ALL-7472 | 12.1 | Add message IDs for 401 no session and 404 unknown entry id |
| CDC-12823 | RWB-P7-TE013-APP | CG-ALL-7475 | 4, 14 | Add a new message ID for the decision-record refusal of a missing or invalid field, then cite it in section 14 for MSG-P7-009. |

### RWB-P10-TE013-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12834 | RWB-P7-TE013-APP | GAP-0080 | 1 | Name rwb-agent (P10) as the agent platform of DL33 with task queue rwb-agent as the only place a model call is made; no other service or workflow code calls the endpoint. |
| CDC-12835 | RWB-P7-TE013-APP | GAP-0083 | 4 | Name the two read-only rwb-agent tools: case facts and score via the rwb-source-data (P1) data-product contract, and extracted document fields via the rwb-document (P5) REST contract. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12817 | RWB-P7-TE013-APP | DOR-RWB-P7-TE013-APP-14 |  | Record the signed epic design sign-off for the epic |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12821 | RWB-P7-TE013-APP | DOR-RWB-P7-TE013-APP-7 | 11 | Confirm the index columns decision_log_entry.decided_at DESC and decision_log_entry.(actions->>'fallback') against LDM v9, or remove them from the index definition. |

### OTHER:Screen specifications for SCR-38 and SCR-46 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12824 | RWB-P7-TE013-APP | DOR-RWB-P7-TE013-APP-10 | find it | Add the empty, loading, error and no-access states for SCR-38 and SCR-46, or state that this story owns neither screen. |

### OTHER:RWB-TE-013 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12829 | RWB-P7-TE013-APP | GAP-2422 | find it | Supersede the section 12 sentence that the client publishes no event: the calling service publishes DecisionRecorded on rwb.decision-record.v1 from its outbox and this service collects it into the ledger. |

### RWB-P10-TE013-OPS; RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12831 | RWB-P7-TE013-APP | GAP-0621 | 12, 13 | Name the rwb-agent login, its secret reference and grants on rwb_agent only; fix topic rights, partitions, retention, retry and .dlt names of rwb.decision-record.v1; record worker, alert and capacity values per environment. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12833 | RWB-P7-TE013-APP | CG-ALL-7478 | 18 | Align the REQ-DRI-001, REQ-DRI-005 and REQ-ACA-010 test lists with story section 18 in the next RTM version. |

### OTHER:Template and Rules v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12836 | RWB-P7-TE013-APP | GAP-2420 | 13 | Supply the rwb-decision login name, consumer group, Flyway user and property names (DP-02, DP-10), and the nightly chain-check time from the decision-log store slice (JOB-14). |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12837 | RWB-P7-TE013-APP | GAP-2425 | 5 | Tie rwb.decision-record.DecisionRecorded.v1 to one of EV-08, EV-09 or EV-30 without changing the topic or the payload. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0080 | The agent platform of DL33 is never named as a service | TechX | Resolved (directive) |
| GAP-0083 | The tool gateway's target systems are not named | TechX | Resolved (directive) |
| GAP-0381 | The call type between the client and rwb-agent, the run result after the 60 second budget and the guardrail check codes are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0619 | The app slice of the agent runtime client: the two operations the legacy Java interface spans, the call type and the budget of a step, the login, the record write and its link, the guardrail check-code list and the route in front of the run read are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-decision, rwb-case and rwb-access | Resolved (directive) |
| GAP-0620 | The client contract: the operation paths and the member types beyond the legacy Java records, the refusal set, the 409 of an in-flight repeat, the record reference and the route in front of the run read are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0621 | The deployment slice of the agent runtime client: the chart values, the login secret, the topic rights of the shared decision-record topic, the worker concurrency, the alert thresholds, the route path and the capacity figures are not specified by any source | SCB IT infrastructure and the DevOps team with the ACE platform team and security | Resolved (directive) |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1315 | The key set of the decision entry of an agent step, the sub-decision code beside the route code, and the field set of the two ledger reads have no source | Solution architect, P7 rwb-decision, with the P10 agent runtime business analyst and the data steward | Resolved (directive) |
| GAP-1316 | The operation and parameter names of the agent fallback-rate measure have no source | Data steward with the P9 reporting analyst and the P10 agent runtime business analyst | Resolved (directive) |
| GAP-1317 | The text of MSG-P7-009 and the shape of an append that is refused are not written out in any source | Solution architect, P7 rwb-decision, with the platform event team | Resolved (directive) |
| GAP-1318 | The name of the per-service database login is not fixed by any source | ACE DB team with the platform team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-2187 | The agent runtime client has no published operation, no call type and no target-side home for the record write | Solution architect | Resolved (directive) |
| GAP-2188 | The client contract has no source member types, refusal detail or record reference shape | Solution architect | Resolved (directive) |
| GAP-2189 | The release has no source topology, sizing, login name, alert threshold, runbook text or route path | DevOps lead | Resolved (directive) |
| GAP-2417 | The decision code of an agent step and the placement and key set of the agent run, the mode, the fallback and its reason are in no source | Solution architect | Resolved (directive) |
| GAP-2418 | The text of MSG-P7-009 and the identifiers and texts of the not-found answer and the chain-break report are not written in any source | Business analyst, P7 | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2420 | The per-service login name, the environment and property names and the time of the chain check are in no source | Solution architect | Resolved (directive) |
| GAP-2421 | The model version of agent INTAKE is named in no source | Solution architect | Resolved (directive) |
| GAP-2422 | The legacy story says the client publishes no event while DP-03 requires the record on the shared decision-record topic | Solution architect | Resolved (directive) |
| GAP-2423 | The fixed story path already held an artefact of the superseded Work Package B-P7-05 whose citations resolve to no register row | Documentation lead | Resolved (directive) |
| GAP-2424 | The fallback-rate measure, its operation name and its threshold ownership are in no source | Business analyst, P7 | Resolved (directive) |
| GAP-2425 | The EV number of the DecisionRecorded event is left open by the Ownership Map among three P7 events | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
