# RWB-PLT-OBS Observability - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 2 |
| Resolved in the stories | 28 |
| Cross-document (pending in another document) | 33 |
| Not applied (value not in the sources) | 7 |
| Open business decisions | 0 |
| Register gaps linked | 13 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-E1056-OPS | 20 | 30 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-OBS Observability/RWB PLT E1056 OPS Run books and monitoring for every Epic 1 Workbench job - deployment v2.md |
| RWB-PLT-N005-OPS | 8 | 3 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-OBS Observability/RWB PLT N005 OPS Platform dashboards and alerts baseline - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

None.

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-E1056-OPS | R-11663 | CG-ALL-1468 | 7 | Criteria and test data read ACE views directly | AC3 and AC7 are not in this chunk and still read ACE views; the item is not fully resolved. |
| RWB-PLT-E1056-OPS | R-18631 | DOR-RWB-PLT-E1056-OPS-10 | 7 | Definition of Ready item 10 Screens and states: Partial | Needs a new state AC for SCR-44 in section 7 plus a section 16 test row. Neither section's text is in this chunk, so no exact old text is available to edit. |
| RWB-PLT-N005-OPS | R-07314 | DOR-RWB-PLT-N005-OPS-22 | find it | Definition of Ready item 22 Fake published: Fail | Searched 03 Requirements and specifications for fake/stub versions: only generic 'a fake per contract' wording, no published fake library version. None invented. |
| RWB-PLT-N005-OPS | R-07315 | DOR-RWB-PLT-N005-OPS-23 | find it | Definition of Ready item 23 Contract version fixed: Fail | No contract version is stated in the story or the 03 folder; only the /v1 path and generic OpenAPI 3.1 and AsyncAPI 3.0 spec formats appear. No version invented. |
| RWB-PLT-N005-OPS | R-18757 | DOR-RWB-PLT-N005-OPS-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 text is not in this chunk, so no AC or test case row for BR1 to BR8 can be placed against existing numbering. Needs that text. |
| RWB-PLT-N005-OPS | R-18758 | DOR-RWB-PLT-N005-OPS-7 | 11 | Definition of Ready item 7 Data: Partial | No source defines BR Field IDs. Keying the 19 section 11 rows would invent values. Left unchanged. |
| RWB-PLT-N005-OPS | R-31804 | NEWAC-RWB-PLT-N005-OPS-AC8 | 8 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Adding AC8 to section 7 and its row to section 16 needs that text, which is not in this chunk. The proposed test is Not specified in the source documents (NEWAC-RWB-PLT-N005-OPS-AC8). |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14251 | RWB-PLT-E1056-OPS | CG-ALL-1469 | find it | Renumber the duplicate FR-PLT-001 row in the next PRD version. |
| CDC-14252 | RWB-PLT-E1056-OPS | CG-ALL-1470 | find it | Renumber the duplicate FR-PLT-009 row in the next PRD version. |
| CDC-14253 | RWB-PLT-E1056-OPS | CG-ALL-1471 | Header | Renumber the duplicate FR-PLT-010 row so each FR-PLT-010 has one meaning in the next PRD version. |
| CDC-14254 | RWB-PLT-E1056-OPS | CG-ALL-1472 | Header | Renumber the duplicate FR-PLT-011 row so each FR-PLT-011 has one meaning in the next PRD version. |
| CDC-14255 | RWB-PLT-E1056-OPS | CG-ALL-1473 | Header | Renumber the duplicate FR-PLT-012 row so each FR-PLT-012 has one meaning in the next PRD version. |
| CDC-14256 | RWB-PLT-E1056-OPS | CG-ALL-1474 | Header | Renumber the duplicate FR-PLT-013 row so each FR-PLT-013 has one meaning in the next PRD version. |
| CDC-14257 | RWB-PLT-E1056-OPS | CG-ALL-1475 | Header | Renumber the duplicate FR-PLT-021 row so each FR-PLT-021 has one meaning in the next PRD version. |
| CDC-14258 | RWB-PLT-E1056-OPS | CG-ALL-1476 | Header | Renumber the duplicate FR-PLT-022 row so each FR-PLT-022 has one meaning in the next PRD version. |
| CDC-14259 | RWB-PLT-E1056-OPS | CG-ALL-1477 | Header | Renumber the duplicate FR-PLT-023 row so each FR-PLT-023 has one meaning in the next PRD version. |
| CDC-14260 | RWB-PLT-E1056-OPS | CG-ALL-1478 | Header | Renumber the duplicate FR-PLT-024 row so each FR-PLT-024 has one meaning in the next PRD version. |
| CDC-14261 | RWB-PLT-E1056-OPS | CG-ALL-1479 | Header | Renumber the duplicate FR-PLT-025 row so each FR-PLT-025 has one meaning in the next PRD version. |
| CDC-14262 | RWB-PLT-E1056-OPS | CG-ALL-1480 | Header | Renumber the duplicate FR-PLT-026 row so each FR-PLT-026 has one meaning in the next PRD version. |
| CDC-14263 | RWB-PLT-E1056-OPS | CG-ALL-1481 | header | Renumber the duplicate FR-PLT-028 in the PRD's next version so it has one meaning |
| CDC-14264 | RWB-PLT-E1056-OPS | CG-ALL-1482 | header | Renumber the duplicate FR-PLT-029 in the PRD's next version so it has one meaning |
| CDC-14266 | RWB-PLT-E1056-OPS | DOR-RWB-PLT-E1056-OPS-2 | 18 | Renumber the duplicate FR-PLT IDs (001, 009, 010, 011 and the other flagged IDs) in the PRD's next version |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14249 | RWB-PLT-E1056-OPS | CG-ALL-1461 | 12.4 | Add platform as a consumer of rwb.source-data.AceDataReady.v1 and add its ACL. |
| CDC-14250 | RWB-PLT-E1056-OPS | CG-ALL-1462 | 12.4 | Add platform as a consumer of rwb.source-data.AceDataLate.v1 and add its ACL. |
| CDC-14267 | RWB-PLT-E1056-OPS | DOR-RWB-PLT-E1056-OPS-8 | find it | Add P2 platform as a consumer of rwb.source-data.AceDataReady.v1 and of rwb.source-data.AceDataLate.v1. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14246 | RWB-PLT-E1056-OPS | DOR-RWB-PLT-E1056-OPS-14 | header | Confirm and record the signed epic design sign-off for RWB-PLT-OBS. |
| CDC-15081 | RWB-PLT-N005-OPS | DOR-RWB-PLT-N005-OPS-14 | Header | Record the signed epic design sign-off against this story |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14265 | RWB-PLT-E1056-OPS | DOR-RWB-PLT-E1056-OPS-12 | 16 | Add TC-E1-056-09 and TC-E1-056-10 to tab Story test cases; align RTM v7 test lists with story section 18 |
| CDC-14270 | RWB-PLT-E1056-OPS | CG-ALL-1466 | 16 | Add rows for TC-E1-056-09 and TC-E1-056-10 to tab Story test cases, with Given, When and Then copied from AC6 and from AC1/AC7 (legacy AC8 and AC9). |

### OTHER:Recovery Workbench story set (contract stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14247 | RWB-PLT-E1056-OPS | DOR-RWB-PLT-E1056-OPS-21 | header | Create contract story RWB-PLT-E1056-CON for the rwb-source-data contract the story fakes, or confirm no CON dependency. |

### OTHER:rwb-source-data contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14248 | RWB-PLT-E1056-OPS | DOR-RWB-PLT-E1056-OPS-22 | 12.8 | Publish the contract fake library and record its version as published. |

### OTHER:Recovery Workbench document holding Version 3 section 1 Jobs row (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14268 | RWB-PLT-E1056-OPS | GAP-2046 | find it | Version 4 reads the Jobs row as Temporal Schedules and event-started workflows of the owning service, using the Architecture v5 slide 44 job map and the P2 job catalogue. |

### OTHER:Business analyst to confirm the section count (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14269 | RWB-PLT-E1056-OPS | CG-ALL-1463 | 14 | MSG-P2-005 now says six sections |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14271 | RWB-PLT-E1056-OPS | CG-ALL-1467 | 18 | Align the REQ-DRI-007 row to the tests this story carries (TC-E1-056-01 to TC-E1-056-10) in the next RTM version. |

### OTHER:Sequence v6 register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14272 | RWB-PLT-E1056-OPS | GAP-3230 | find it | Drop or strike through items 19 and 21 (RWB-E1-014, RWB-TE-007) and clear their Depends on references in RWB-E1-056 and RWB-E1-017. |

### OTHER:Story dependencies v5 and legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14273 | RWB-PLT-E1056-OPS | GAP-3233 | find it | Keep the five Not carried rows visible; a follow-up adds an X row only if the named story is really awaited. |

### OTHER:Recovery Workbench dashboards version 3 (sections 1 and 3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14274 | RWB-PLT-E1056-OPS | GAP-2050 | find it | In version 4 name the service behind the Data health and Work health panels (P1, P3, P9 sources); keep the console names as dashboard names only. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14275 | RWB-PLT-E1056-OPS | GAP-3164 | find it | Change the module of RWB-E1-056 from P2 Integration to the platform OPS story RWB-PLT-E1056-OPS, and let each service keep its run book rows in its own ops lane. |

### OTHER:Recovery Workbench measures, alerts and dashboards document; OTHER:Version 3 (to become Version 4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15082 | RWB-PLT-N005-OPS | GAP-2043 |  | Read each measure and each alert with the service as the unit: 19 measured units (1.1), per-service reading of the 13 alerts (2.1), one Service health dashboard per service (3.1); leave dashboard name, panel order, refresh interval and saved query to the RWB-PLT-N005-OPS baseline. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15083 | RWB-PLT-N005-OPS | GAP-1390 |  | State that the platform runs PgBouncer itself with one database or user entry per login so the cap and statement timeout are per login; ACE DBA confirms the deployment shape before wave 1. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1001 | The business-hours window, the deployment slot and the alert thresholds of the document intake pipeline are not specified | DevOps team | Resolved (directive) |
| GAP-1015 | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | DevOps engineer | Resolved (directive) |
| GAP-1390 | Whether the per-login cap is delivered by the managed PgBouncer of the Azure Database for PostgreSQL service or by a PgBouncer deployment the platform runs is not specified | Platform template owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1418 | The observability baseline artefacts, thresholds and ownership are not specified | Solution architect | Resolved (directive) |
| GAP-1419 | The job-run record, the run book home and the catalogue-to-run join are not specified after the split | Solution architect | Resolved (directive) |
| GAP-2043 | Version 3 measures, alerts and dashboards the Workbench as one; the target architecture is 19 services | Solution architect with the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2044 | No source names the owner of a per-service dashboard or alert rule as a team | Platform team with the DevOps team | Resolved (directive) |
| GAP-2045 | Metric and span names, labels, retention, sampling and the alert delivery channel are not specified | Platform team | Resolved (directive) |
| GAP-2046 | The Jobs row still reads the Quartz job table, which the target architecture retires | Platform team with the DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2050 | The Data health and Work health panels read objects of two services and the consoles are not named after the split | P1 rwb-source-data with P3 rwb-case and P9 rwb-reporting | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3164 | The run books are a P2 story in the notes and a platform OPS story in the split plan | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3230 | Two retired items still carry v6 windows and dependencies | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
