# RWB-ITG-NFR Non-functional integration - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 2 |
| Resolved in the stories | 28 |
| Cross-document (pending in another document) | 23 |
| Not applied (value not in the sources) | 1 |
| Open business decisions | 4 |
| Register gaps linked | 15 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-TE009-ITG | 15 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-NFR Non-functional integration/RWB ITG TE009 ITG Performance test harness - integration v2.md |
| RWB-ITG-TE010-ITG | 13 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-NFR Non-functional integration/RWB ITG TE010 ITG Browser and accessibility tests - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-TE009-ITG | R-22918 | GAP-0015 | Register gap | Compliance and Product Owner | RPO and RTO are not set | Leave RPO/RTO unset in the baseline and confirm the tiers with Compliance before the release gate |
| RWB-ITG-TE009-ITG | R-22922 | GAP-2058 | Register gap | RWB-PLT-DB with SCB IT infrastructure, confirmed by Compliance and Operations | No recovery point objective and no recovery time objective is set for any store or any service | Every per-store row carries the placeholder 'Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2)' and no tier or number of minutes is invented. The gap is closed by RWB-PLT-DB with SCB IT infrastructure before the first production release, and the restore test records the measured time until the target exists. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1047-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P3-E1042-APP | R-35662 | ASM-3199 | Register assumption |  | The six open-point rows that named an individual (DL03, DL04, DL05, DL06, DL07, DL37) carry the Template and Rules R9 placeholder in the Owner column, with the organisation the same row already stated kept after it, and the five roles of section 9 are left as the only owner labels in the document. | Confirm the role that owns each of the six open points. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-TE009-ITG | R-04167 | DOR-RWB-ITG-TE009-ITG-21 | header | Definition of Ready item 21 Contract published: Fail | No contract story for this story is named in the story set, so no contract dependency is recorded. The header keeps None. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02255 | RWB-ITG-TE009-ITG | CG-ALL-101 | 18 | Align the test lists for REQ-OCC-007 and REQ-WKM-002 between RTM v7 and section 18 in the next RTM version. |
| CDC-02268 | RWB-ITG-TE010-ITG | DOR-RWB-ITG-TE010-ITG-12 | 18 | Add to REQ-OCC-007: TC-ITG-TE010-ITG-01, TC-ITG-TE010-ITG-02. Add to REQ-WKM-001: TC-ITG-TE010-ITG-01. |
| CDC-02270 | RWB-ITG-TE010-ITG | CG-ALL-106 | 18 | Align the REQ-OCC-007 and REQ-WKM-001 test lists in the next RTM version with story section 18 (TC-ITG-TE010-ITG-01 and -02, and -01). |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02250 | RWB-ITG-TE009-ITG | DOR-RWB-ITG-TE009-ITG-14 | find it | Record the signed epic design sign-off for EP01-TE against RWB-ITG-TE009-ITG |
| CDC-02264 | RWB-ITG-TE010-ITG | DOR-RWB-ITG-TE010-ITG-14 | find it | Record the signed epic design sign-off in the epic design record; no signed design is in the story or source documents. |

### OTHER:Recovery Workbench capacity forecast v3 (workbook) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02254 | RWB-ITG-TE009-ITG | GAP-0277 | find it | Add sheet Service volumes with one row per each of the 19 services: driver, 2027 volume by formula, unit, basis cell, topic, task queue and consumers. Totals on other sheets unchanged. |
| CDC-02256 | RWB-ITG-TE009-ITG | GAP-0282 | find it | Keep the formula and figures; add per-service rows and a cross-check block citing the Architecture v5 slide 48 figure of about 3,110 new cases a month, stated as rounded up. |

### OTHER:Legacy dependency trace sheet and story dependencies v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02260 | RWB-ITG-TE009-ITG | GAP-3233 |  | Keep the five Not carried rows visible, including RWB-TE-009 to RWB-TE-004; add an X row only if a run book or harness really waits for the named story. |
| CDC-02271 | RWB-ITG-TE010-ITG | GAP-3233 | find it | Keep the RWB-TE-010 to RWB-TE-003 row visible in the trace as Not carried; add an X row only if the run books or harness waits for RWB-PLT-TE003-APP-2. |

### OTHER:Template and Rules §R5.6 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02261 | RWB-ITG-TE009-ITG | GAP-3199 |  | State epic wave as the earliest wave among its stories, with the service wave shown beside it; use NF only for NF-01 to NF-08 stories. |
| CDC-02272 | RWB-ITG-TE010-ITG | GAP-3199 | find it | State the epic wave rule: epic wave equals earliest wave among its stories, with service wave shown beside it; use NF only for NF-01 to NF-08. |

### OTHER:Version 3 workbook; OTHER:Read path and Key sheets (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02251 | RWB-ITG-TE009-ITG | GAP-0278 | find it | Name rwb-source-data as the one reader of recovery.v_ace_* views, reading on behalf of screens and workflows; headline figures unchanged (Read path A2, C16, Inputs G7, Key C10) |

### OTHER:Version 3 workbook; OTHER:Inputs rows and Route activity rows 5 to 9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02252 | RWB-ITG-TE009-ITG | GAP-0281 | find it | Carry the section R9 placeholder for payments, guarantee claims, partner instructions, report reads, lots and deviation share; basis states the run cadence, lot cadence or named stock |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02253 | RWB-ITG-TE009-ITG | GAP-2061 | find it | Add a per-service availability table of 19 rows applying the two targets, write the shape of one service once, and state the composed screen as the product of the services it calls within the one-hop budget. |

### OTHER:Recovery Workbench source v2 (load table, section 2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02257 | RWB-ITG-TE009-ITG | GAP-2060 | find it | Keep the seven rows; state the differences; add a 2031 figure of about 47,389 open cases in new section 2.1 with its Architecture v5 source. Note 410 vs 414 is about 1 percent, not under 0.2 percent. |

### OTHER:Recovery Workbench source document version 3 (sections 1; OTHER:5 and 6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02258 | RWB-ITG-TE009-ITG | GAP-2064 |  | Name RWB-PLT-OBS as owner of per-service detection and alerting; record that no monitoring threshold exists; threshold belongs to ADR-023 and the observability platform story. |

### OTHER:Recovery Workbench source document version 3 (section 1; OTHER:COLLINS load complete row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02259 | RWB-ITG-TE009-ITG | GAP-2065 |  | Keep the 07:00 level; name P1 rwb-source-data as owner with P3 rwb-case and P8 rwb-payment in the chain; leave per-step deadlines to batch and scheduling design. |

### OTHER:split_plan.json and source document version 2 section 6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02262 | RWB-ITG-TE009-ITG | GAP-2066 |  | Record failover test owner as RWB-PLT-NF06-DB with ACE DBA and restore test owner as P5 rwb-document with RWB-PLT-DB; record the missing story and invent none. |

### OTHER:Recovery Workbench source document version 3; OTHER:Read path sheet (note on cells B15 and C15) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02263 | RWB-ITG-TE009-ITG | GAP-0279 |  | Name the existing jobs: case creation and allocation (JOB-02, JOB-03), reconciliation (JOB-04) and WIN notice file (JOB-10); keep the count of three and all figures. |

### OTHER:rwb-case reference-data contract story and story dependency graph (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02265 | RWB-ITG-TE010-ITG | DOR-RWB-ITG-TE010-ITG-21 | header | Contract dependencies row names the rwb-case reference-data contract; story key marked Not specified. |

### OTHER:rwb-case contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02266 | RWB-ITG-TE010-ITG | DOR-RWB-ITG-TE010-ITG-22 | 12.8 | Publish an rwb-case contract fake and record its library version as published. |

### OTHER:07 Screens and experience/Recovery Workbench Screen Specifications v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02267 | RWB-ITG-TE010-ITG | DOR-RWB-ITG-TE010-ITG-10 | 15 | Define the missing states: SCR-02 error, no access; SCR-03, SCR-04, SCR-07, SCR-09 empty, error, no access; SCR-05 empty, loading, error, no access. Then copy them into story section 15. |

### OTHER:Browser-stage configuration review (owner QA lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02269 | RWB-ITG-TE010-ITG | GAP-0331 | find it | Before the first SIT run, fix the gateway-bff composite route list, the scan engine and the stage name; keep browsers.json and a11y-exceptions.json in configuration. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0277 | The forecast is written for one monolith and has no per-service volumes | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0278 | The read path gives every Workbench screen the recovery.v_ace_* views | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0279 | The three scheduled Workbench jobs include a lake refresh that the target removes | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0281 | No demand figure exists for payments, guarantee claims, partner instructions, the report read volume, the lots or the deviation share | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0282 | Arch v5 states 3,110 new cases a month; the forecast divides the account inflow by 1.2 | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0330 | Performance harness target routes, SIT identity set and pipeline stage are not named for the microservice target | QA lead | Resolved (directive) |
| GAP-0331 | Browser stage screen routes, Thai and English label source and scan engine are not named for the microservice edge | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2060 | The load figures of the source and Architecture v5 differ, and the source has no 2031 row | Architecture with the performance test owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2061 | The source is written for one recovery module and has no per-service target, size or deployment shape | Architecture with RWB-PLT-OBS and RWB-PLT-DB | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2064 | The source sets no monitoring or alerting target, and a per-service failure needs one | RWB-PLT-OBS with the owning services | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2065 | The 07:00 deadline of the COLLINS load is one number for a chain of services, with no per-service deadline | P1 rwb-source-data with P3 rwb-case and P8 rwb-payment | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2066 | The failover test and the restore test of the source have no story in the split plan | QA team suggested, with RWB-PLT-DB and P5 rwb-document | Resolved (directive) |
| GAP-3191 | The performance mix does not name the owning service of its 7 operations | QA team | Resolved (directive) |
| GAP-3199 | The epic wave is not defined for an epic whose stories span several business-epic waves | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
