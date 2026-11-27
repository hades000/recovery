# RWB-PLT-EVT Kafka event platform - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 3 |
| Resolved in the stories | 21 |
| Cross-document (pending in another document) | 19 |
| Not applied (value not in the sources) | 7 |
| Open business decisions | 0 |
| Register gaps linked | 13 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-N002-INF | 5 | 4 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EVT Kafka event platform/RWB PLT N002 INF Kafka topics, retry and dead-letter topics and ACLs - infrastructure v2.md |
| RWB-PLT-N008-INF | 7 | 6 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EVT Kafka event platform/RWB PLT N008 INF Schema registry with BACKWARD compatibility - infrastructure v2.md |
| RWB-PLT-N012-INF | 9 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EVT Kafka event platform/RWB PLT N012 INF Blob, Key Vault and MFT SFTP standard resources - infrastructure v2.md |

## 3. Open business decisions (not resolved; owner decides)

None.

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-N002-INF | R-07296 | DOR-RWB-PLT-N002-INF-14 | find it | Definition of Ready item 14 Epic design: Fail | No epic design sign-off for RWB-PLT-N002 in the sources. Grep of 03 folder finds N002 only in PRD PLT Platform v1 (no sign-off). Gap Not specified in the source documents (DOR-RWB-PLT-N002-INF-14). |
| RWB-PLT-N002-INF | R-07298 | DOR-RWB-PLT-N002-INF-21 | find it | Definition of Ready item 21 Contract published: Fail | No RWB-PLT-N002-CON story exists in the sources; adding a CON dependency would need an invented story. Contract dependencies row left as None. Not specified in the source documents (DOR-RWB-PLT-N002-INF-21). |
| RWB-PLT-N002-INF | R-07299 | DOR-RWB-PLT-N002-INF-22 | find it | Definition of Ready item 22 Fake published: Fail | No published contract fake library version for RWB-PLT-N002 in the sources (Grep of 03 and project .md files). Not specified in the source documents (DOR-RWB-PLT-N002-INF-22). |
| RWB-PLT-N002-INF | R-07300 | DOR-RWB-PLT-N002-INF-23 | find it | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-PLT-N002 in the sources; /v1 is topic naming only. Not specified in the source documents (DOR-RWB-PLT-N002-INF-23). |
| RWB-PLT-N002-INF | R-18746 | DOR-RWB-PLT-N002-INF-4 | 8 | Definition of Ready item 4 Business rules: Partial | Rule rows BR1 to BR8 are in section 8 (this chunk), but the criteria and test rows sit in sections 7 and 16, which are not in this chunk. Needs the chunk holding those sections. |
| RWB-PLT-N002-INF | R-31801 | NEWAC-RWB-PLT-N002-INF-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 must be added to section 7 and its test row to section 16; neither is in this chunk, so it cannot be anchored. Proposed test stays Not specified in the source documents (NEWAC-RWB-PLT-N002-INF-AC7). |
| RWB-PLT-N012-INF | R-31816 | NEWAC-RWB-PLT-N012-INF-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 added to section 7 for BR1 to BR8 coverage. Its section 16 TC row is needed and lies outside this chunk, so it is not added here. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15065 | RWB-PLT-N002-INF | GAP-0123 | 12.9 | Write the retry topic naming rule: three retry topics per event topic, one per window (1 min, 10 min, 1 h), derived from the event topic name. |
| CDC-15066 | RWB-PLT-N002-INF | GAP-0124 | 12.9 | Record the dead-letter topic name, replication factor, retention and replay window agreed with the ACE platform team; provision the 20 dead-letter topics from the same configuration file as the event topics. |
| CDC-15067 | RWB-PLT-N002-INF | GAP-1398 | 12.9 | Record the retry and dead-letter topic names, ACL principal model and names, per-service quotas and the environment list, agreed with the ACE platform team, before provisioning. |
| CDC-15101 | RWB-PLT-N008-INF | GAP-1397 | 8 | Select the schema registry product with the Kafka hosting decision (bank platform registry; Event Hubs Premium registry as fallback) and fix the subject naming convention. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15064 | RWB-PLT-N002-INF | DOR-RWB-PLT-N002-INF-1 | 1 | Add a role code or role name for 'infrastructure engineer', the role used in section 1 of RWB-PLT-N002-INF. |
| CDC-15099 | RWB-PLT-N008-INF | DOR-RWB-PLT-N008-INF-1 | 1 | Map or add the role 'infrastructure engineer' used in section 1 of RWB-PLT-N008-INF to a role code, or the story must use an existing role code. |
| CDC-15126 | RWB-PLT-N012-INF | DOR-RWB-PLT-N012-INF-1 | 1 | Register 'infrastructure engineer' as a role name or role code |

### RWB-PLT-N008-INF (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15097 | RWB-PLT-N008-INF | DOR-RWB-PLT-N008-INF-14 |  | Record the signed sign-off of the epic design for RWB-PLT-EVT in the epic design record. |
| CDC-15098 | RWB-PLT-N008-INF | DOR-RWB-PLT-N008-INF-16 | header | Size row added to the header table as Not specified in the source documents. |
| CDC-15100 | RWB-PLT-N008-INF | DOR-RWB-PLT-N008-INF-7 | 11 | Added a line after each of the two section 11 tables stating the BR Field ID for each row is Not specified in the source documents. |

### OTHER:RWB-E6-037 Endpoints and TSD P9 (T-A.2; OTHER:T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15102 | RWB-PLT-N008-INF | GAP-2580 |  | Fix the three comparison properties, variance arithmetic, row ceiling, baseline date parameter and default, and whether rwb-reporting publishes its own event type. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15123 | RWB-PLT-N012-INF | DOR-RWB-PLT-N012-INF-14 | header | Record the signed epic design sign-off for RWB-PLT-EVT |

### OTHER:Contract publication (contract story, not in the story set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15124 | RWB-PLT-N012-INF | DOR-RWB-PLT-N012-INF-21 | section header | Publication is not confirmed by any source; no contract story exists to confirm it. |

### OTHER:Contract fake library (contract story, not in the story set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15125 | RWB-PLT-N012-INF | DOR-RWB-PLT-N012-INF-22 | section header | Publish the fake library version and record it on RWB-PLT-N012-INF |

### OTHER:Technical Specifications by Module v6 (or a PLT module file in the FSD v6 set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15127 | RWB-PLT-N012-INF | GAP-1664 | header | Write the platform functional specification as the T0 Service section or a PLT module file, and map FR-PLT-001 to FR-PLT-034 to its requirement IDs. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15128 | RWB-PLT-N012-INF | GAP-3227 | header | Set Release for RWB-PLT-N001 to N012 (with CON variants) and RWB-PLT-NF01 to NF08 to Window 1 (E1, 30 November 2026, tentative), or to a named wave-0 date. |

### OTHER:Wave 0 standard resource list and network and security design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15129 | RWB-PLT-N012-INF | GAP-1399 | 7 | Fix Blob container names, immutable retention periods per container, Key Vault name, codec key names and rotation period, MFT/SFTP endpoint names, PGP key ownership and network ranges. |

### OTHER:Version 3 window order (Epic 1 to Epic 3 plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15130 | RWB-PLT-N012-INF | GAP-3244 | header | Place the wave 0 platform stories N001 to N012 and the harness stories W1J01 to W4J01 as Day-1 work before window 1. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20873 | RWB-PLT-N012-INF | R-23296 |  | Blob container names, retention, Key Vault, codec keys, endpoints and network ranges belong in the Wave 0 standard resource list and network and security design. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0123 | No retry topic name is given for any event topic | Platform architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0124 | No dead-letter topic name, partition count or retention is given | Platform architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0125 | The shared topic rwb.decision-record.v1 has no settings of its own in any source | Platform architect | Resolved (directive) |
| GAP-0129 | No registry subject and no JSON Schema is named per event type | Platform architect | Resolved (directive) |
| GAP-0649 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | SCB IT infrastructure | Resolved (directive) |
| GAP-1397 | Schema registry product, hosting and subject naming are not specified | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1398 | Retry and dead-letter topic names, ACL principals and quotas are not specified | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1399 | Blob container names, Key Vault key names, rotation and MFT/SFTP endpoints are not specified | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1664 | No FSD module exists for the platform, so no FSD requirement ID states a platform capability | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1666 | The retry limit of an event and of a call is stated differently in the BRD and in Architecture v5 | Solution architect | Resolved (directive) |
| GAP-2580 | Benefit realisation: the variance fields, the variance rule, the row ceiling, the event absence and the baseline date default are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-3227 | The 23 new wave-0 platform stories have no release date | Delivery lead | Resolved (directive) |
| GAP-3244 | The new platform stories N001 to N012 and the harness stories W1J01 to W4J01 sit in no window of version 3 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-PLT-N012-INF | new AC without TC row | 296 | AC7 is new and no section 16 row covers it |
