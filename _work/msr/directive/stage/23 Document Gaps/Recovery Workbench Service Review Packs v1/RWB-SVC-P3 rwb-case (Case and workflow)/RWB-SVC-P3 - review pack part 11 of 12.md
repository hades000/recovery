# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 11 of 12 (RWB-P3-E2042-CON to RWB-P3-E3013-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 78 |
| Cross-document (pending in another document) | 244 |
| Not applied (value not in the sources) | 30 |
| Open business decisions | 6 |
| Register gaps linked | 66 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E2042-CON | 21 | 37 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2042 CON Epic 2 rule packages in Drools - contract v2.md |
| RWB-P3-E2042-INF | 8 | 38 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2042 INF Epic 2 rule packages in Drools - infrastructure v2.md |
| RWB-P3-E2042-OPS | 14 | 41 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2042 OPS Epic 2 rule packages in Drools - deployment v2.md |
| RWB-P3-E2043-APP | 6 | 31 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2043 APP Temporal and Drools integration pattern and reference case workflow v2.md |
| RWB-P3-E2043-CON | 5 | 28 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2043 CON Temporal and Drools integration pattern and reference case workflow - contract v2.md |
| RWB-P3-E2043-OPS | 10 | 27 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2043 OPS Temporal and Drools integration pattern and reference case workflow - deployment v2.md |
| RWB-P3-E3013-APP | 14 | 18 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E3013 APP Check encumbrance and eligibility before negotiation v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E3013-APP | R-10500 | CG-ALL-4456 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-22736 | GAP-1306 | Register gap | Center of excellence analyst with the P3 reference-data owner and the business owner | The decision code of a reference-case step and the value set of LOV-DECISION are not fixed by any source | Enumerate LOV-DECISION in the P3 reference-data load with the route and approval codes of the FSD P7 and fix the code of a route move; until then the ledger stores the code the fact carries, validates it against the list in force, and the reference-data fake supplies the value the reference package uses |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-28878 | GAP-1309 | Register gap | Compliance and PDPA officer with the solution architect and the platform observability team | The shape and route of the chain-check break report, and whether JOB-14 writes a ledger entry of its own, are not fixed | Agree the report fields, the alert route and the result retention with Compliance and the platform observability team, and state in the ledger run book whether the check is recorded as an operational event or as a decision record; until then ASM-B-P7-05-E2043-6 holds and the check writes no ledger row |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-28879 | GAP-1310 | Register gap | Solution architect with the Compliance and PDPA officer and the owners of the points of no return (S6, S7, S5, S4) | The strict-mode acknowledgement and the daily seal of the ledger hash are named by the architecture and no story of this key owns them | Raise the seal and the strict-mode acknowledgement as their own stories of the P7 epic with the Risk and Internal Audit sign-off that the ADR-009 change needs, and fix the seal manifest, its storage path and its schedule and the confirmation read together; until then ASM-B-P7-05-E2043-7 holds and this story builds only the ledger they consume |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E2042-CON | R-05349 | DOR-RWB-P3-E2042-CON-16 | Header | Definition of Ready item 16 Size: Fail | Size value is not in the sources; the header carries the Not specified placeholder. |
| RWB-P3-E2042-CON | R-28862 | GAP-0723 |  | Blob immutability period, pod memory for 20 KieBases, alert windows and probe timings are not specified | Container, pod, alert and probe text is in a section not in this chunk, so no exact old text. No source gives the memory or timing values. Needs that section. |
| RWB-P3-E2042-CON | R-28865 | GAP-1298 |  | The decision code of a rule-governance entry is not named in any source this key may read | Story text holding any decision code is in a section not in this chunk, so no exact old text. Needs that section. |
| RWB-P3-E2042-CON | R-28866 | GAP-1299 |  | The name of the rwb-decision database login is not specified | Login text is in a section not in this chunk, so no exact old text. The login name is not in the sources. Needs that section. |
| RWB-P3-E2042-CON | R-28867 | GAP-1300 | 14 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Section 14 is not in this chunk, so no exact old text. Exact wording also needs business analyst confirmation before SIT. |
| RWB-P3-E2042-CON | R-28868 | GAP-1303 |  | The BRD section pointers copied from the legacy story no longer match BRD v2 and v4 | Traceability pointers are in a section not in this chunk, so no exact old text. Needs that section. |
| RWB-P3-E2042-CON | R-28874 | GAP-2398 | 13; 18 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Sections 13 and 18 and the DP table rows are not in this chunk (line 304 is the header only), so no exact old text. Needs those sections. |
| RWB-P3-E2042-INF | R-22325 | GAP-2395 | notice path (not supplied) | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Fix edits a notice-path section not in this chunk, so no exact old text exists. Package codes are not in the chunk; none invented. Resend the section to apply. |
| RWB-P3-E2042-INF | R-22729 | GAP-2399 | notice path (not supplied) | No source states the state a notice rests in, or the message, when no package version is in force | Fix edits a notice-path section not in this chunk, so no exact old text exists. Resend that section to add the MSG-GEN-006 refusal rule. |
| RWB-P3-E2042-INF | R-28846 | GAP-2400 | route-set section (not supplied) | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | The route-set criterion sits in a section not in this chunk, so it cannot be edited. Resend that section to keep route-set on RWB-E2-035. |
| RWB-P3-E2042-INF | R-28856 | GAP-1302 | sections not supplied | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Package title, dry-run breakdown, MSG-P3-015 text and rollback answer sit in sections not in this chunk. Resend them to write the placeholders. |
| RWB-P3-E2042-INF | R-30732 | NEWAC-RWB-P3-E2042-INF-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 must be added to section 7 and its TC row to section 16; neither is in this chunk. Covered-by line in section 8 left unchanged until AC7 exists. Resend sections 7 and 16. |
| RWB-P3-E2042-OPS | R-01014 | CG-ALL-4412 | 13 | Story RWB-P7-E1073-CON named as a dependency does not exist | Naming the existing RWB-P7-E1073 APP story needs its key, which is not in the story or item. Creating CON is not allowed. Solution architect to supply the key. |
| RWB-P3-E2042-OPS | R-05359 | DOR-RWB-P3-E2042-OPS-14 | header | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off in 03 Requirements and specifications or the story. Sign-off value not specified in the source documents. |
| RWB-P3-E2042-OPS | R-05361 | DOR-RWB-P3-E2042-OPS-17 | header | Definition of Ready item 17 Dependencies: Fail | Depends on the RWB-P7-E1073-CON key, which cannot be named until CG-ALL-4412 is resolved. No other dependency is in the sources. |
| RWB-P3-E2042-OPS | R-05363 | DOR-RWB-P3-E2042-OPS-22 | header | Definition of Ready item 22 Fake published: Fail | No published contract fake version found in 04 User stories or 03 Requirements and specifications. Version not invented. |
| RWB-P3-E2042-OPS | R-05364 | DOR-RWB-P3-E2042-OPS-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version found in 03 Requirements and specifications. The story states only the /v1 path, so no version is named. |
| RWB-P3-E2042-OPS | R-16279 | DOR-RWB-P3-E2042-OPS-10 | 15 | Definition of Ready item 10 Screens and states: Partial | States are already named in section 15 with CG-ALL-4418. FSD P4 v3 SCR-39 row gives no state definitions and no screen spec is in the sources; definitions needed. |
| RWB-P3-E2043-APP | R-01017 | CG-ALL-4424 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment ruling not found. Service Template Spec v1 L116 gives the rule and L354 gives 'case', which is reserved. No name invented. |
| RWB-P3-E2043-APP | R-01018 | CG-ALL-4425 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.workflow.reference uses the reserved word 'case' | Same as CG-ALL-4424: no architect package segment ruling in Service Template Spec v1 (L116, L354). No name invented. |
| RWB-P3-E2043-APP | R-01019 | CG-ALL-4426 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.outbox.reference uses the reserved word 'case' | Same as CG-ALL-4424: no architect package segment ruling in Service Template Spec v1 (L116, L354). No name invented. |
| RWB-P3-E2043-APP | R-16291 | DOR-RWB-P3-E2043-APP-7 | 11 | Definition of Ready item 7 Data: Partial | Legacy job and decision-log wording is in sections 7 and 16, not in this chunk. Section 11 needs no edit. |
| RWB-P3-E2043-CON | R-01021 | CG-ALL-4437 | 3 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Replacement package segment is a solution architect ruling, not in any source. BR-PLT-006 yields 'case'. Line 47 left unchanged; no value invented. |
| RWB-P3-E2043-CON | R-05372 | DOR-RWB-P3-E2043-CON-14 |  | Definition of Ready item 14 Epic design: Fail | Epic design sign-off is an approval. No signed EP02 epic design record exists in the sources, so sign-off cannot be confirmed. |
| RWB-P3-E2043-CON | R-28876 | GAP-0727 | 12 | Field-level detail of RecordAndApplyRequest and of the rule outputs map | Fix edits section 12 text, which is not in this chunk; exact old text cannot be copied. Needs the section 12 lines (around L215-L220) in a follow-up chunk. |
| RWB-P3-E2043-OPS | R-28882 | GAP-1308 | 13 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | The metadata rows do not yet carry the eight platform and published dependencies. The correction is deferred to the next version, so the item is not resolved here. |
| RWB-P3-E3013-APP | R-16306 | DOR-RWB-P3-E3013-APP-10 | 13 | Definition of Ready item 10 Screens and states: Partial | Section 13 text is not in this chunk, so the SCR-14 and SCR-16 state lines cannot be anchored or edited. Needs a chunk with section 13. |
| RWB-P3-E3013-APP | R-16309 | DOR-RWB-P3-E3013-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Criteria for BR1-BR12 go in section 7 and test rows in section 16; neither section is in this chunk, so no anchor text exists. Needs those parts. |
| RWB-P3-E3013-APP | R-25194 | CG-ALL-4459 | 3.1 | Flyway file V3013_1__encumbrance_check.sql is not in the V0001..Vnnnn form | Next V-number of the rwb-case Flyway sequence is not in the cited Service Template Specification v1 (not in folder). V3013_1 name is not in the supplied story text, so no anchor. |
| RWB-P3-E3013-APP | R-30741 | NEWAC-RWB-P3-E3013-APP-AC9 | 7 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in the supplied story text, so no anchored edit is possible. The proposed test is Not specified in the source documents (NEWAC-RWB-P3-E3013-APP-AC9). |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07188 | RWB-P3-E2042-OPS | CG-ALL-4413 | 12.5 | Add a Workflows row for RuleModelSwap (task queue rwb-case, started by RulePackageInForce), or name the catalogued swap workflow. JOB-20 names only RulePackageInForce. |
| CDC-07190 | RWB-P3-E2042-OPS | DOR-RWB-P3-E2042-OPS-8 | find it | Add activity swapRuleModel and workflow RuleModelSwap to the catalog. Also publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in the rwb-decision API yaml. |
| CDC-07191 | RWB-P3-E2042-OPS | CG-ALL-4414 | 12.5 | Add an Activities row for swapRuleModel: type Activity, task queue rwb-case, registered by the rwb-case worker. |
| CDC-07228 | RWB-P3-E2043-APP | CG-ALL-4419 | 12.5 | Add a row for ReferenceCaseWorkflow (test-only, task queue rwb-case), or name the catalogued workflow in RWB-P3-E2043-APP 12.5. The catalogued name is Not specified in the source documents (CG-ALL-4419). |
| CDC-07234 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-8 | 12.5 | Add rows for ReferenceCaseWorkflow (workflow), and EvaluateRulesActivity and RecordAndApplyActivity (activities), with task queue rwb-case. |
| CDC-07235 | RWB-P3-E2043-APP | CG-ALL-4420 | 12.5 | Add an Activities row for EvaluateRulesActivity on task queue rwb-case, or name a catalogued activity in 12.5 |
| CDC-07236 | RWB-P3-E2043-APP | CG-ALL-4421 | 12.5 | Add an Activities row for RecordAndApplyActivity on task queue rwb-case, or name a catalogued activity in 12.5 |
| CDC-07259 | RWB-P3-E2043-CON | CG-ALL-4430 | 12.5 | Add ReferenceCaseWorkflow to the Workflows sheet, or name the catalogued workflow to use. |
| CDC-07261 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-8 | 12.5 | Add ReferenceCaseWorkflow, EvaluateRulesActivity and RecordAndApplyActivity to the catalog, or name catalogued equivalents. |
| CDC-07262 | RWB-P3-E2043-CON | CG-ALL-4431 | 12.5 | Add EvaluateRulesActivity to the Activities sheet, or use a catalogued activity. |
| CDC-07263 | RWB-P3-E2043-CON | CG-ALL-4432 | 12.5 | Add RecordAndApplyActivity to the Activities sheet, or use a catalogued activity. |
| CDC-07287 | RWB-P3-E2043-OPS | CG-ALL-4439 | 12.5 | Add workflow ReferenceCaseWorkflow to the Workflows sheet, or name the catalogued workflow to use in section 12.5. |
| CDC-07291 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-8 | 12.5 | Add ReferenceCaseWorkflow to Workflows, and EvaluateRulesActivity and RecordAndApplyActivity to Activities. |
| CDC-07292 | RWB-P3-E2043-OPS | CG-ALL-4440 | 12.5 | Add activity EvaluateRulesActivity to the Activities sheet. |
| CDC-07293 | RWB-P3-E2043-OPS | CG-ALL-4441 | 12.5 | Add activity RecordAndApplyActivity to the Activities sheet. |

### 05 Technical architecture/Recovery Workbench Workflow Engine Design v4.docx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20874 | RWB-P3-E2043-CON | R-22047 |  | Timer design is owned by P3 rwb-case with the platform team; this story builds no timer. v4 docx not read, so nothing verified. |
| CDC-20875 | RWB-P3-E2043-CON | R-22737 |  | v4 docx is binary and no docview/shell access; exact section 7 anchor not read. Child timeout not in sources (GAP-2019). |
| CDC-20876 | RWB-P3-E2043-APP | R-22738 |  | v4 docx not readable here, so section 3 anchor not verified. Timeout value not in sources (GAP-2018); design owner must set it. |
| CDC-20877 | RWB-P3-E2043-APP | R-28880 |  | v4 docx not readable here, so section 5 anchor not verified. ID literal format not in any source (GAP-2021). |
| CDC-20878 | RWB-P3-E2043-CON | R-22047 |  | v4 docx not readable here; section 4 timer text not verified, so the timer ruling was not written. |
| CDC-20879 | RWB-P3-E2043-APP | R-22732 |  | v4 docx not readable here; versioning text anchor not verified (GAP-0725). No fix written. |
| CDC-20880 | RWB-P3-E2043-APP | R-22733 |  | v4 docx not readable here; replay corpus text not written. MSG-P3-038 text not checked in the message catalogue (GAP-0726). |
| CDC-20881 | RWB-P3-E2043-CON | R-22737 |  | v4 docx not readable here; section 7 anchor not verified. MSG-P3-037 text and child timeout not in sources (GAP-2019). |
| CDC-20882 | RWB-P3-E2043-APP | R-22738 |  | v4 docx not readable here; section 7 anchor not verified. Timeout not specified in source documents (GAP-2018). |
| CDC-20883 | RWB-P3-E2043-APP | R-28880 |  | v4 docx not readable here; section 5 anchor not verified. Child and kit ID format not specified in source documents (GAP-2021). |
| CDC-20884 | RWB-P3-E2043-CON | R-22047 |  | Adopted design fix for section 4 not verified in v4 docx; the file could not be read to confirm or write the anchor. |
| CDC-20885 | RWB-P3-E2043-CON | R-22737 |  | v4 docx not readable here; section 7 anchor not verified. Child timeout not specified in source documents (GAP-2019). |
| CDC-20904 | RWB-P3-E2043-OPS | R-22738 |  | write failed: WRITE FAILED (nothing was written): X002-F2: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20907 | RWB-P3-E2043-OPS | R-22737 |  | write failed: WRITE FAILED (nothing was written): X002-F2: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20908 | RWB-P3-E2043-OPS | R-22047 |  | write failed: WRITE FAILED (nothing was written): X002-F2: old text found 0 time(s) in paragraphs, expected 1 |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07135 | RWB-P3-E2042-CON | GAP-0967 | find it | Publish service-identity rows for the fourteen capability areas; record the area each package serves as a rwb-decision package attribute. |
| CDC-07154 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-1 | 1 | Add the role 'infrastructure engineer' with a role code, or name the existing role code used in section 1. |
| CDC-07173 | RWB-P3-E2042-INF | GAP-0967 | 4 | Publish the service-identity rows of the permission matrix across the fourteen areas, and record the capability area of each package as a rwb-decision attribute. |
| CDC-07209 | RWB-P3-E2042-OPS | GAP-0967 | find it | Publish the service-identity rows of the permission matrix for the fourteen capability areas; confirm each service runs as one non-human actor; record the area each package serves as a rwb-decision attribute. |
| CDC-07238 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-1 | 1 | Confirm developer as a role code or name, or the story names an existing role in section 1 |
| CDC-07266 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-1 | 1 | Add a role code and name for 'tech lead' or confirm the listed role §1 should use. |
| CDC-07295 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-1 | 1 | Add a role for 'platform engineer', or confirm the existing role it maps to; §1 then names that role. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07137 | RWB-P3-E2042-CON | CG-ALL-4405 | 16 | Add rows TC-P3-E2042-CON-01 to TC-P3-E2042-CON-06 with Given, When and Then copied from AC1 to AC6 of RWB-P3-E2042-CON. |
| CDC-07175 | RWB-P3-E2042-INF | CG-ALL-4409 | 16 | Add rows TC-P3-E2042-INF-01 to -06 to Story test cases, with Given, When and Then copied from criteria AC1 to AC6. |
| CDC-07192 | RWB-P3-E2042-OPS | DOR-RWB-P3-E2042-OPS-12 | 16 | Register TC-P3-E2042-OPS-01 to TC-P3-E2042-OPS-17 in Test Cases v8; align the §18 test lists with RTM v7. |
| CDC-07212 | RWB-P3-E2042-OPS | CG-ALL-4416 | 16 | Add rows for TC-P3-E2042-OPS-01 to TC-P3-E2042-OPS-06 in the next Test Cases version, with Given, When and Then copied from the criteria they cover. |
| CDC-07280 | RWB-P3-E2043-CON | CG-ALL-4435 | 16 | Add rows TC-P3-E2043-CON-01 to TC-P3-E2043-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-07307 | RWB-P3-E2043-OPS | CG-ALL-4444 | 16 | Add rows TC-P3-E2043-OPS-01 to TC-P3-E2043-OPS-06 with Given, When and Then copied from the criterion each covers. |
| CDC-07325 | RWB-P3-E3013-APP | CG-ALL-4455 | 16 | Add rows TC-E3-013-01 to TC-E3-013-06 to Story test cases, with Given, When and Then copied from the criteria they cover. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07138 | RWB-P3-E2042-CON | CG-ALL-4406 | 18 | Align the REQ-CWC-013 trace and the other RTM rows with section 18 of RWB-P3-E2042-CON so both list the same tests for the two requirements. |
| CDC-07176 | RWB-P3-E2042-INF | CG-ALL-4410 | 18 | Align the tests traced to REQ-CWC-013 and REQ-CWC-014 with RWB-P3-E2042-INF section 18 in the next RTM version. |
| CDC-07213 | RWB-P3-E2042-OPS | CG-ALL-4417 | 18 | Align the REQ-CWC-013 trace to the story §18 test cases TC-P3-E2042-OPS-02 and TC-P3-E2042-OPS-05 and remove the other stories' test IDs from this requirement. |
| CDC-07240 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-12 | 12, 16, 18 | Align the test case lists for this story with section 18; section 16 now has TC-E2-043-08 to TC-E2-043-10 for the contract, payload and reference checks |
| CDC-07252 | RWB-P3-E2043-APP | CG-ALL-4423 | 18 | Align the test lists of the four differing requirements with section 18 of RWB-P3-E2043-APP in the next RTM version |
| CDC-07281 | RWB-P3-E2043-CON | CG-ALL-4436 | 18 | Align the test lists of the four traced requirements, including REQ-DRI-001, with section 18 of this story in the next RTM version. |
| CDC-07308 | RWB-P3-E2043-OPS | CG-ALL-4445 | 18 | Align the test lists of the four differing requirements with section 18 of RWB-P3-E2043-OPS; REQ-DRI-001 differs (story 02, 05; RTM lists other IDs). |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07237 | RWB-P3-E2043-APP | CG-ALL-4422 | 14 | Add a message ID for the NoPackageInForce refusal at evaluation time, with its English text. The ID is not specified in the source documents (CG-ALL-4422). MSG-P3-027 in section 14 stays as is. |
| CDC-07242 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-9 | 14 | Add a message ID for the NoPackageInForce refusal, as in CG-ALL-4422. The ID is not specified in the source documents (DOR-RWB-P3-E2043-APP-9). |
| CDC-07264 | RWB-P3-E2043-CON | CG-ALL-4433 MSG-P3-027 text differs from the Error and Message Standard v4 | 14 | Row now points to the standard; text not copied into the story. |
| CDC-07265 | RWB-P3-E2043-CON | CG-ALL-4434 | 14 | Add a new message ID for 'A recorded history does not replay against this build' with its text; the story then cites it. |
| CDC-07270 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-9 | 14 | State the meaning of MSG-P3-038 so §14 matches; MSG-P3-027 now points to the standard text. |
| CDC-07294 | RWB-P3-E2043-OPS | CG-ALL-4443 | 4, 14 | Add a new message ID for 'A recorded history does not replay against the build' with the workflow-change text; the story then cites it. |
| CDC-07297 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-9 | 14 | Align MSG-P3-027 text to the standard's text, and give MSG-P3-038 the standard's new ID once it exists. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20844 | RWB-P3-E2043-OPS | R-22734 |  | Event schema of rwb.decision-record.v1 is already in this file. Decision-log OpenAPI and ingest/message approvals belong to rwb-decision. |
| CDC-20845 | RWB-P3-E2043-OPS | R-22734 |  | Event schema of rwb.decision-record.v1 is already in this file. Decision-log OpenAPI and ingest/message approvals belong to rwb-decision. |
| CDC-20846 | RWB-P3-E2043-OPS | R-22734 |  | Event schema of rwb.decision-record.v1 is already in this file. Decision-log OpenAPI and ingest/message approvals belong to rwb-decision. |
| CDC-20847 | RWB-P3-E2043-OPS | R-22734 |  | Event schema of rwb.decision-record.v1 is already in this file. Decision-log OpenAPI and ingest/message approvals belong to rwb-decision. |
| CDC-20848 | RWB-P3-E2042-OPS | R-28872 |  | Field IDs for package code and SHA-256 appear in no source. The DP-03 decision-record owner (Data steward role) confirms them. This file is unchanged. |
| CDC-20849 | RWB-P3-E2042-OPS | R-28872 |  | Field IDs for package code and SHA-256 appear in no source. The DP-03 decision-record owner (Data steward role) confirms them. This file is unchanged. |
| CDC-20850 | RWB-P3-E2042-OPS | R-28872 |  | Field IDs for package code and SHA-256 appear in no source. The DP-03 decision-record owner (Data steward role) confirms them. This file is unchanged. |

### RWB-P7-E2042-APP (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07133 | RWB-P3-E2042-CON | GAP-2406 | find it | Section 3: set valid-from of RES-2026.12 to 2026-12-01, matching the ITG harness and RWB-P3-E2035-APP, in place of 2026-12-15. |
| CDC-07168 | RWB-P3-E2042-INF | GAP-2406 | 11 | Reconcile one valid-from date for RES-2026.12 (2026-12-01 or the legacy 11 December 2026) before the wave-2 fixture is frozen. |
| CDC-07185 | RWB-P3-E2042-INF | GAP-1296 | none | Keep the metadata as written. Carry the eight H and three C dependencies added by the DP table in sections 13 and 18. Ready to start stays Day 1. |
| CDC-07186 | RWB-P3-E2042-INF | GAP-2398 | none | Carry the eleven DP-added rows in the DP application of sections 13 and 18. Leave the metadata rows as the Work Package fixes them, so the Day-1 rule holds. |
| CDC-07204 | RWB-P3-E2042-OPS | GAP-2406 | find it | Reconcile the valid-from of RES-2026.12 to 2026-12-01 as used by the ITG harness and RWB-P3-E2035-APP, or re-date the legacy criteria, before the wave-2 fixture is frozen. |
| CDC-07207 | RWB-P3-E2042-OPS | GAP-0721 | find it | Keep the registry, seeding, admin operations, approval, rollback and JOB-20 in RWB-P7-E2042-APP; keep the workbooks, model cache, checksum, atomic swap, catalog read and schema assertion in RWB-P3-E2042-APP. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07134 | RWB-P3-E2042-CON | GAP-2396 | find it | Correct the P6 Comms to P7 Decision cell from T to an event cell, matching the RulePackageInForce subscription from rwb.decision.events.v1. |
| CDC-07146 | RWB-P3-E2042-CON | GAP-2026 | n/a | State in one place that S2 rwb-treatment owns and evaluates PAYMENT_MATCH and that matchPayments asks S2 through its contract; record as an assumption until the package is authored. |
| CDC-07169 | RWB-P3-E2042-INF | GAP-2396 | 7 | Correct the P6 Comms to P7 Decision cell from T to E in the next diagram issue so the matrix matches the RulePackageInForce subscription. |
| CDC-07205 | RWB-P3-E2042-OPS | GAP-2396 | find it | Correct the P6 Comms to P7 Decision cell from T to an event cell in the next diagram issue. Consumption stays with RWB-P6-E1073-APP. |
| CDC-07322 | RWB-P3-E3013-APP | GAP-1696 | 11 | Obtain every source fact through the rwb-source-data contract; add S2 to the P1 REST cell of the connection matrix; S2 reads no ACE view or table. |
| CDC-07328 | RWB-P3-E3013-APP | GAP-1705 | 12 | Add the connection-matrix cells from rwb-case to S5 for asset take-on and to rwb-integration for the CCMS release and Land Office title check, and record the returned references. |

### RWB-P3-E2043-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07231 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-21 | header | Move the contract story build status from Not started to Done (contract published). |
| CDC-07232 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-22 | header | Publish the contract fake library and record its published version. The version is Not specified in the source documents (DOR-RWB-P3-E2043-APP-22). |
| CDC-07254 | RWB-P3-E2043-APP | GAP-0727 | 12.5 | Settle RecordAndApplyRequest members (event key, rule result, state change, business date) and types at baseline review; RuleResult outputs package-specific |
| CDC-07289 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-21 | header | Contract dependencies row now names RWB-P3-E2043-CON with build status Not started |
| CDC-07290 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-22 |  | Record a published contract fake library version; none is recorded in the sources |
| CDC-07310 | RWB-P3-E2043-OPS | GAP-0727 |  | Settle the request record and the outputs map at baseline review: event key, rule result, state change and business date as the only request members, with a package-specific output schema. |

### RWB-P3-E2042-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07151 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-21 | find it | Move build status from Not started to Done once the contract is published. |
| CDC-07152 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-22 | find it | Publish the contract fake library and record its version in RWB-P3-E2042-CON. |
| CDC-07153 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-23 | find it | Fix the contract version this story builds against and publish it. |
| CDC-07189 | RWB-P3-E2042-OPS | DOR-RWB-P3-E2042-OPS-21 | Header | Set build status to Done once the contract is published. |
| CDC-07208 | RWB-P3-E2042-OPS | GAP-0722 | find it | Publish the model and catalog read resources with packageCode, versionLabel, checksum, model content, compiler version, valid-from, ruleId, packageVersion and the listed catalog elements. |

### OTHER:Workflow Engine Design v3 (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07243 | RWB-P3-E2043-APP | GAP-2016 |  | Durable timer is authoritative; timer row is the audit copy written by ApplyStateActivity in the same transaction as the state and read back on reopen; JOB-05 five-minute check retired. |
| CDC-07246 | RWB-P3-E2043-APP | GAP-0725 | find it | State the build ID as the release commit ID supplied by the workflow kit, pin builds with drain-on-complete, and have the platform workflow kit owner set the versioning policy once for all 19 services. |
| CDC-07247 | RWB-P3-E2043-APP | GAP-0726 | find it | Define the replay corpus as one recorded history per acceptance path of the reference fixture, kept with the contract jar. Take the MSG-P3-038 text from the message catalogue before the gate is mandatory. |
| CDC-07250 | RWB-P3-E2043-APP | GAP-2019 |  | Parent starts the stage child with the case ID, retries the start with the same workflow ID, and raises an incident with MSG-P3-037 when retries are exhausted; case stays in its last applied state. Child start-to-close timeout is not specified in the source documents (GAP-2019). |
| CDC-07251 | RWB-P3-E2043-APP | GAP-2018 |  | Pivot activity waits for the ledger acknowledgement using the section 7 retry policy and a documented timeout; workflow fails with an incident at timeout without repeating a completed step. Timeout value is not specified in the source documents (GAP-2018). |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07116 | RWB-P3-E2042-CON | DOR-RWB-P3-E2042-CON-14 | n/a | Record the signed epic design sign-off and cite it in this story. |
| CDC-07150 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-14 | find it | Record the signed epic design sign-off so this story can cite it. |
| CDC-07229 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-14 | header | Record the signed epic design sign-off for RWB-P3-E2043-APP. The sign-off reference is Not specified in the source documents (DOR-RWB-P3-E2043-APP-14). |
| CDC-07288 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-14 |  | Record the signed epic design sign-off for RWB-SVC-P3 / EP02 |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07120 | RWB-P3-E2042-CON | DOR-RWB-P3-E2042-CON-12 | 12.7, 16, 18 | Register TC-P3-E2042-CON-01 to -08 in Test Cases v8; align the section 18 test lists with RTM v7. Boundary test TC-07 added in story. |
| CDC-07155 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-12 | 16, 18 | Add TC-P3-E2042-INF-01 to -06 to Test Cases v8; reconcile the RWB-P3-E2042-INF test lists in RTM v7 with section 18. |
| CDC-07268 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-12 | 16, 18 | Add TC-P3-E2043-CON-01 to -06 to Test Cases v8 and align RTM v7 test lists with §18 of this story. |
| CDC-07296 | RWB-P3-E2043-OPS | DOR-RWB-P3-E2043-OPS-12 | 12, 16, 18 | Register TC-P3-E2043-OPS-01 to -17 in Test Cases v8 and align the §18 test lists to RTM v7. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07131 | RWB-P3-E2042-CON | GAP-0668 | 12 | Record GET /cases/{caseId}/next-action as served by rwb-integration from the integration base (DP-13), with the case row and write kept with rwb-case. |
| CDC-07145 | RWB-P3-E2042-CON | GAP-1994 | n/a | Add a payment_match_rule row owned by P7 rwb-decision as the PAYMENT_MATCH package; keep the proceeds rows with P8 rwb-payment. |
| CDC-07182 | RWB-P3-E2042-INF | GAP-1994 | none | Add a payment_match_rule row owned by rwb-decision as the PAYMENT_MATCH package. Keep the proceeds rows with rwb-payment. |
| CDC-07224 | RWB-P3-E2042-OPS | GAP-1994 |  | Assign the match rules to rwb-decision as the PAYMENT_MATCH package; keep the proceeds rows in rwb-payment; define no payment_match_rule table. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07112 | RWB-P3-E2042-CON | CG-ALL-4399 | n/a | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in paths, or the consumer must use a published operation. |
| CDC-07113 | RWB-P3-E2042-CON | CG-ALL-4400 | n/a | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId} with the packageVersion query parameter in paths. |
| CDC-07187 | RWB-P3-E2042-OPS | CG-ALL-4411 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in rwb-decision.yaml through the provider CON story. |

### RWB-P3-E2042-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07119 | RWB-P3-E2042-CON | DOR-RWB-P3-E2042-CON-10 | find it | Add empty, loading, error and no-access states to SCR-39 screen design; this contract story has no screen states to add. |
| CDC-07171 | RWB-P3-E2042-INF | GAP-0721 | 7 | Keep the registry, seeding, admin operations, approval, rollback and JOB-20 in RWB-P7-E2042-APP; prove AC1 to AC3 of the registry here against the rwb-decision contract mock. |
| CDC-07181 | RWB-P3-E2042-INF | GAP-1300 | none | Fix the MSG-P3-027 detail for the schema check match order and catalog completeness to rule IDs, row orders and column names only. Confirm the text with the business analyst before SIT. |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07121 | RWB-P3-E2042-CON | GAP-0966 | find it | Add the rule-package action set, request and answer fields and a change decision code to POST /authorise, and stub them in the fake. |
| CDC-07157 | RWB-P3-E2042-INF | GAP-0966 | find it | Add the rule-package action names, request fields, answer fields and a change decision code to the POST /authorise contract; stub them in the contract fake. |
| CDC-07193 | RWB-P3-E2042-OPS | GAP-0966 | find it | Add rule-package actions LOAD, APPROVE, ROLLBACK, DRY_RUN, EVALUATE; request fields action, packageCode, versionLabel, authorRef, capabilityArea, right, caseRef; answer fields authorised, reason, matrixVersion, area, right, packageArea, entryRef; a change decision code agreed with the RWB-E1-039 access-log owner; stubs in the contract fake. |

### RWB-P8-E2008-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07123 | RWB-P3-E2042-CON | GAP-2503 |  | Declare the nine consumed operations on per-service bases with one hop and 2 s timeout; name workflow matchPayments and its four activities; record AC1, AC3, AC4, AC5 gap in the RTM. |
| CDC-07124 | RWB-P3-E2042-CON | GAP-1346 |  | Name the seven consumed rwb-payment operations in its section 12.2 with placeholders until each owner publishes; confirm scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |
| CDC-07129 | RWB-P3-E2042-CON | GAP-2506 |  | Add C RWB-P7-E1073-CON to the C row of D1; name the ordering column priority with row order as target name; declare DecisionRecorded read only; register no second writer. |

### RWB-P2-E2035-OPS (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07132 | RWB-P3-E2042-CON | GAP-0669 | 13 | Fix login, secret reference and probe checks; set catch-up window, overlap window, backfill limit and thresholds as environment values; add next-action-check job row with run book path; review three runbook entries with on-call rota. |
| CDC-07167 | RWB-P3-E2042-INF | GAP-0669 | 13 | Fix the rwb-integration login, secret reference and probe checks; create the next-action-check job row with its run book; set catch-up, overlap, backfill and thresholds as environment values. |
| CDC-07203 | RWB-P3-E2042-OPS | GAP-0669 | 13 | Fix the login, secret reference and probe checks; add a next-action-check job catalogue row with its runbook path; record the read path ruling in the Ownership Map; review the three runbook entries with the on-call rota. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07144 | RWB-P3-E2042-CON | GAP-0969 | n/a | Add a parameter key for the cached authorise answer lifetime with value Not specified in the source documents (GAP-0969) until the wave 2 design review fixes it. |
| CDC-07220 | RWB-P3-E2042-OPS | GAP-0969 | find it | Add a parameter row under DP-06 for the authorise cache lifetime, value Not specified in the source documents (GAP-0969), fixed at the wave 2 design review. |
| CDC-07249 | RWB-P3-E2043-APP | GAP-1305 | find it | Add the five-minute collection target and the 02:00 chain-check time as rwb-case parameter rows with a name, a version and an owner, using the names of ASM-B-P7-05-E2043-2. The story holds no default. |

### RWB-P2-E2035-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07165 | RWB-P3-E2042-INF | GAP-0667 | 4, 7, 12 | Serve GET /cases/{caseId}/next-action from /api/recovery/integration/v1 under DP-13; correct the Ownership Map row to P2 read and P3 write; fix contract names, operations, Schedule values and messages. |
| CDC-07201 | RWB-P3-E2042-OPS | GAP-0667 | 4, 7, 12 | Serve the read from the integration base under DP-13; fix consumed field names, operation names, Schedule values and message texts; correct the Ownership Map row so P2 owns the read and P3 the write. |
| CDC-07202 | RWB-P3-E2042-OPS | GAP-0668 | 12 | Baseline three operation names, nine consumed shapes, split note, workflow and Schedule contract, error mapping; record the read path ruling in the Ownership Map. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07257 | RWB-P3-E2043-APP | GAP-2053 | 8 | Record Arch v5 outbox and inbox scope for all 19 services as target and Epic 1 and 2 wording as as-built, with R-PREC precedence |
| CDC-07285 | RWB-P3-E2043-CON | GAP-2053 |  | Precedence is recorded in the Change Register; no story text changes. |
| CDC-07313 | RWB-P3-E2043-OPS | GAP-2053 |  | Record the R-PREC precedence rule: outbox and inbox apply to all 19 services as target scope (Arch v5); Epic 1 and 2 outbox wording is the as-built position. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07269 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-7 | 11 | Assign a BR Field ID to each of the seven §11 data rows, or record that none is defined. |
| CDC-07314 | RWB-P3-E3013-APP | CG-ALL-4447 | 13 | Add a recovery_case field that holds the S2 check reference (the index name in the story uses check_ref), or Data rules which existing field holds it. |
| CDC-07320 | RWB-P3-E3013-APP | DOR-RWB-P3-E3013-APP-7 | 11 | Record recovery_case columns check_ref varchar(40), check_outcome_code varchar(20) and decision_record_id uuid in LDM v9 Fields, as in migration V3013_1. |

### RWB-P7-E2027-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07126 | RWB-P3-E2042-CON | GAP-1292 |  | Reconcile PM-2026.12 valid from 2026-12-01 and PMT-2026.12 valid from 2026-12-15 into one PAYMENT_MATCH version row before SIT. |
| CDC-07127 | RWB-P3-E2042-CON | GAP-1297 |  | Reconcile the PAYMENT_MATCH label PMT-2026.12 (from 2026-12-15) with PM-2026.12 (from 2026-12-01) into one version row with the owner before SIT. |

### RWB-P2-E2035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07130 | RWB-P3-E2042-CON | GAP-0667 |  | Serve GET /cases/{caseId}/next-action from the integration base under DP-13; fix consumed field names, operation names, Schedule values and message texts; correct the Ownership Map row. |
| CDC-07166 | RWB-P3-E2042-INF | GAP-0668 | 12 | Baseline the next-action contract with the three operation names, nine consumed shapes, Schedule values and error mapping; confirm element names with rwb-case, rwb-access and rwb-decision owners. |

### OTHER:TSD P4 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07143 | RWB-P3-E2042-CON | GAP-0968 | n/a | Correct T3.1 and T6.1 so the four rule tables (rule_package, rule_package_version, rule_row, rule_test_case) and the registry operations belong to P7; keep only the P4 rights and access-log rows. |
| CDC-07219 | RWB-P3-E2042-OPS | GAP-0968 | find it | Correct T3.1 and T6.1 so the four rule tables and the registry operations belong to P7; keep only the P4 rows for rights and the access log. |

### RWB-P3-E2042-INF (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07156 | RWB-P3-E2042-INF | DOR-RWB-P3-E2042-INF-4 | 8 | BR8 Covered-by entry replaced with a placeholder; BR1 to BR7 mapping stays. |
| CDC-07218 | RWB-P3-E2042-OPS | GAP-0723 | find it | Set the Blob container to write-once with no deletion and reviewed audit retention per environment; size the pod by a load test caching 20 versions; expose alert windows, replica counts and probe timings as reviewed values. |

### RWB-P3-E2042-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07161 | RWB-P3-E2042-INF | GAP-1292 | 11 | Status changed from Resolved to Cross-document. |
| CDC-07178 | RWB-P3-E2042-INF | GAP-1357 | find it | Reconcile PAYMENT_MATCH to one version label: PM-2026.12 in force from 2026-12-01; remove PMT-2026.12 so one version row is in force before SIT. |

### OTHER:RWB-E2-027 build notes (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07163 | RWB-P3-E2042-INF | GAP-3179 | find it | Remove the payment_match_rule load step and table; load PAYMENT_MATCH rows only through the rule package endpoints. |
| CDC-07164 | RWB-P3-E2042-INF | GAP-3180 | find it | Change step 4 priority order to EXACT, then PARTIAL, then WINDOW once Credit Administration confirms; carry it in the PAYMENT_MATCH scenario set. |

### OTHER:ADR-017 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07177 | RWB-P3-E2042-INF | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime; a package version names its format; conversion is a version change with its own test evidence. |
| CDC-07214 | RWB-P3-E2042-OPS | GAP-1620 | find it | Record that the registry accepts an XLS decision table and a DMN 1.6 model as two package formats on one Drools runtime, that a package version names its format, and that conversion is a version change with its own test evidence. |

### OTHER:rwb-case parameters contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07277 | RWB-P3-E2043-CON | GAP-1305 |  | Publish the five-minute collection target and the 02:00 chain-check time as named parameters with a version and an owner. |
| CDC-07304 | RWB-P3-E2043-OPS | GAP-1305 | find it | Publish the five-minute collection target and the 02:00 chain-check time as parameters with a name, version and owner; the ledger reads them at the version in force. |

### OTHER:Workflow Engine Design v3, section 7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07278 | RWB-P3-E2043-CON | GAP-2019 |  | Add child start retry with the same workflow ID, incident MSG-P3-037 when retries are exhausted, case kept in last applied state; child timeout is Not specified in the source documents (GAP-2019). |
| CDC-07305 | RWB-P3-E2043-OPS | GAP-2019 | find it | Parent starts the child with the case ID and retries the start with the same workflow ID; on exhausted retries it raises an incident with MSG-P3-037 and the case stays in its last applied state. |

### OTHER:Workflow Engine Design v3, section 3 (WriteDecisionLogActivity) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07279 | RWB-P3-E2043-CON | GAP-2018 |  | Pivot activity waits for the ledger acknowledgement with the section 7 retry policy and a documented timeout; incident on timeout without repeating completed steps. |
| CDC-07306 | RWB-P3-E2043-OPS | GAP-2018 | find it | Pivot activity waits on ledger acknowledgement with the section 7 retry policy; timeout value: Not specified in the source documents (GAP-2018); on timeout the workflow raises an incident without repeating a completed step. |

### OTHER:Workflow Engine Design v3 section 5 (Workflow IDs) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07284 | RWB-P3-E2043-CON | GAP-2021 |  | Skeleton has no child workflows, so no story edit is needed here. |
| CDC-07312 | RWB-P3-E2043-OPS | GAP-2021 |  | Add the child and kit workflow ID format: the parent generates one ID per child from the case ID and stage code, so a restart cannot create a second child for the same stage. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07316 | RWB-P3-E3013-APP | CG-ALL-4457 | 12.9 | Rule a rwb-case package segment that is not a Java reserved word; the P3 row and the rule at line 116 currently give 'case'. |
| CDC-07317 | RWB-P3-E3013-APP | CG-ALL-4458 | 12.9 | Rule a rwb-case package segment that is not a Java reserved word, covering the encumbrance subpackage as well. |

### RWB-S2-E3013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07318 | RWB-P3-E3013-APP | DOR-RWB-P3-E3013-APP-21 | header | Publish the contract story and confirm it as the CON dependency for this story. |
| CDC-07319 | RWB-P3-E3013-APP | DOR-RWB-P3-E3013-APP-22 | header | Publish the fake library and record its published version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07323 | RWB-P3-E3013-APP | CG-ALL-4448 | 11, 12.7, 13 | Record check_outcome_code (varchar(20), per V3013_1) as a recovery_case column in LDM v9 Fields and Data Classification v5 Fields. |
| CDC-07324 | RWB-P3-E3013-APP | CG-ALL-4449 | 11, 12.7, 13 | Record decision_record_id (uuid, per V3013_1) as a recovery_case column in LDM v9 Fields and Data Classification v5 Fields. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07114 | RWB-P3-E2042-CON | CG-ALL-4401 | n/a | Create RWB-P7-E1073-CON or name the existing story for the rule-model contract, then re-point the DP-04 dependency. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07115 | RWB-P3-E2042-CON | CG-ALL-4402 | n/a | Add a Workflows row for RuleModelSwap (started by RulePackageInForce, task queue rwb-case) or confirm its catalogued name. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07117 | RWB-P3-E2042-CON | DOR-RWB-P3-E2042-CON-8 | n/a | Resolve the four detcheck contract items: CG-ALL-4399, CG-ALL-4400, CG-ALL-4402, CG-ALL-4403. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07118 | RWB-P3-E2042-CON | CG-ALL-4403 | n/a | Add an Activities row for swapRuleModel (task queue rwb-case; input package code, version label, checksum; output cached version, KieBase reference, outcome). |

### OTHER:TSD P7; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07122 | RWB-P3-E2042-CON | GAP-1615 | find it | Re-issue TSD P7 with the four rule tables and rule operations; remove them from TSD P3 and P4; set x-module of nine rule paths to P7. Story BR5 already matches. |

### RWB-P2-E2007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07125 | RWB-P3-E2042-CON | GAP-0657 |  | Keep JOB-08 with rwb-integration; read ACE facts through the rwb-source-data contract; fix consumed paths and shapes in RWB-P2-E2007-CON; allocate the rwb-integration login in RWB-PLT-DB. |

### OTHER:RWB-E2-027 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07128 | RWB-P3-E2042-CON | GAP-3180 |  | Adopt priority order EXACT, then PARTIAL, then WINDOW in its step 4 and PAYMENT_MATCH scenario set. |

### OTHER:Functional Specification P6 v3; OTHER:A2.1.4.3 AC-EXC-P6-001-02 (notice story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07136 | RWB-P3-E2042-CON | GAP-2399 | 7 | Refuse a notice request when no package version is in force with MSG-GEN-006, create no notice row, dispatch nothing and add no hold reason of this service. |

### OTHER:ADR-017 ruling (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07139 | RWB-P3-E2042-CON | GAP-1620 | 13 | Story names both formats but does not choose; the ADR-017 ruling sets which format the registry accepts. |

### OTHER:rwb-decision rule registry (version rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07140 | RWB-P3-E2042-CON | GAP-1357 |  | Read PM-2026.12 as the single version in force for PAYMENT_MATCH and reconcile the PMT-2026.12 label to that one version row before SIT. |

### API:(service not named); OTHER:GET /api/recovery/decision/v1/rule-catalog/{ruleId} (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07141 | RWB-P3-E2042-CON | GAP-2409 |  | Mark packageVersion as required and keep the refusal of MSG-GEN-001 when it, the rule ID or the business date is absent. |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07142 | RWB-P3-E2042-CON | GAP-2410 |  | Record that a secondary slice builds against the platform contracts and published fakes and reads the same service's wave-1 rows through its own schema, within the lane-depth limit of R5.7 rule 5. |

### OTHER:Rules Engine Design v3 (section 2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07147 | RWB-P3-E2042-CON | GAP-2034 | n/a | Add that UNIVERSAL is evaluated in every service from its own copy of the same approved version, with authoring, scenarios and approval in rwb-decision (P7). |

### OTHER:Decision record of the DP-03 library (published decision record) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07148 | RWB-P3-E2042-CON | GAP-2397 | 12 | Confirm the field IDs that carry the package code and the checksum when the record is published; add no column to notice, template or merge_field. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07149 | RWB-P3-E2042-INF | CG-ALL-4408 | 13 | Create story RWB-P7-E1073-CON, or name an existing story that supplies the DP-04 rule-package contract, then align the Contract dependencies row of RWB-P3-E2042-INF. |

### OTHER:TSD P7 rwb-decision; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07158 | RWB-P3-E2042-INF | GAP-1615 | find it | Re-issue TSD P7 with the four rule tables and rule-version operations; remove them from TSD P3 and TSD P4; set x-module of the nine rule paths to P7. |

### OTHER:RWB-E2-008 consumers: rwb-source-data, rwb-case, rwb-treatment contracts; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07159 | RWB-P3-E2042-INF | GAP-2503 | find it | Declare the nine consumed operations on per-service bases with one hop and 2 s timeout; name workflow matchPayments with its four activities; record in the RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story. |

### RWB-P2-E2007-CON; OTHER:RWB-PLT-DB; OTHER:TSD P2 Integration v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07160 | RWB-P3-E2042-INF | GAP-0657 | find it | Fix the six unsettled consumed paths and shapes in RWB-P2-E2007-CON; allocate the rwb-integration login in RWB-PLT-DB; record TSD P2 v3 T5.2 and the slide 44 rwb-payment owner row as superseded for JOB-08. |

### OTHER:RWB-E2-027 owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07162 | RWB-P3-E2042-INF | GAP-1297 | 11 | Status changed from Resolved to Cross-document. |

### RWB-ITG-E2042-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07170 | RWB-P3-E2042-INF | GAP-0421 | 16 | Agree the harness repository, SIT environment, seeding set, evidence format, pass or fail gate and fake response bodies at wave 2 entry, held as data in the harness pack. |

### OTHER:rwb-decision contract (RWB-P7 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07172 | RWB-P3-E2042-INF | GAP-0722 | 12 | Publish the model and catalog resources with packageCode, versionLabel, checksum, model content, compiler version, valid-from, and the catalog element names. |

### OTHER:TSD P7 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07174 | RWB-P3-E2042-INF | GAP-1301 | 11 | Add the four registry tables rule_package, rule_package_version, rule_row and rule_test_case to the P7 TSD at its next version under rwb_decision. |

### OTHER:TSD P4 v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07179 | RWB-P3-E2042-INF | GAP-0968 | find it | Correct T3.1 and T6.1 so the four rule tables and registry operations are P7's; P4 keeps only the rights and access-log rows. |

### OTHER:Parameters contract (DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07180 | RWB-P3-E2042-INF | GAP-0969 | find it | Add a parameter row for the cached authorise answer lifetime, fixed at the wave 2 design review; confirm with the access-log owner that one entry covers one dry run. |

### OTHER:Temporal and Drools Design Text Extract v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07183 | RWB-P3-E2042-INF | GAP-2026 | none | Name S2 rwb-treatment as owner and evaluator of PAYMENT_MATCH, recorded as an assumption until the package is authored. matchPayments in rwb-payment asks S2 through its contract. |

### OTHER:Rules Engine Design v3 section 2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07184 | RWB-P3-E2042-INF | GAP-2034 | none | State that UNIVERSAL is evaluated in every service from its own copy of the same approved version, with authoring, scenarios and approval in rwb-decision (P7). |

### OTHER:Technical Specification P7 (rwb-decision), with TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07194 | RWB-P3-E2042-OPS | GAP-1615 | 12 | Add T3.1 entries for rule_package, rule_package_version, rule_row and rule_test_case and appendix T-A operations to TSD P7; remove them from TSD P3 and P4; set x-module to P7 on the nine rule paths. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07195 | RWB-P3-E2042-OPS | GAP-2395 | 12 | Read the three Epic 2 package codes and version labels through the contract as the fixture set; settle the rwb-comms package assignment with the rule registry owner before integration. |

### OTHER:RWB-E2-008 application slice and the owning service contract baselines (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07196 | RWB-P3-E2042-OPS | GAP-2503 | 12 | Declare the nine consumed operations on per-service bases with one hop and 2 s timeout; name workflow matchPayments and its four activities; record in RTM that legacy AC1, AC3, AC4, AC5 have no story. |

### RWB-P2-E2007-CON; RWB-P2-E2007-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07197 | RWB-P3-E2042-OPS | GAP-0657 | 12 | Keep JOB-08 with rwb-integration; mark slide 44 rwb-payment row superseded; read ACE facts via rwb-source-data; supersede TSD P2 Integration v3 T5.2; allocate the rwb-integration login in RWB-PLT-DB. |

### OTHER:Registry rows of RWB-E2-027 and RWB-E2-042 (PAYMENT_MATCH package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07198 | RWB-P3-E2042-OPS | GAP-1292 | 7 | Hold one row per package version; reconcile PM-2026.12 (2026-12-01) and PMT-2026.12 (2026-12-15) into one label and valid-from date before SIT promotion. |

### OTHER:RWB-E2-027 story owner (business analyst) and the PAYMENT_MATCH registry row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07199 | RWB-P3-E2042-OPS | GAP-1297 | 7 | Raise one reconciliation so one package code holds one version row before SIT. This key keeps its legacy value PMT-2026.12 from 2026-12-15 until then. |

### OTHER:PAYMENT_MATCH rule package scenario set (decision and rules lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07200 | RWB-P3-E2042-OPS | GAP-3180 | 7 | Confirm the order with Credit Administration; carry EXACT, then PARTIAL, then WINDOW into the PAYMENT_MATCH scenario set so one order is tested. |

### OTHER:Rule package harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07206 | RWB-P3-E2042-OPS | GAP-0421 | find it | Agree the harness repository, SIT environment, seeding set, evidence format and retention, pass or fail gate and fake response bodies at the wave 2 entry check; hold values as data in the pack. |

### OTHER:TSD P7 v2 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07210 | RWB-P3-E2042-OPS | GAP-1301 | find it | Record the R-PREC default reading that P7 owns the four registry tables in rwb_decision, and add those tables to the P7 TSD at its next version. |

### OTHER:FSD P6 v3 (A2.1.4.2 and A2.1.4.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07211 | RWB-P3-E2042-OPS | GAP-2399 | find it | Refuse the notice request with MSG-GEN-006, create no notice row, dispatch nothing and add no hold reason of this service. |

### OTHER:rwb-decision version register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07215 | RWB-P3-E2042-OPS | GAP-1357 | find it | Reconcile the PMT-2026.12 label to the single version row PM-2026.12 in force from 2026-12-01 before SIT; the precondition naming PMT-2026.12 is outside this chunk. |

### OTHER:rwb-comms story for legacy RWB-E2-042 (route-set criterion) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07216 | RWB-P3-E2042-OPS | GAP-2400 |  | Keep the next action, owner and due date on RWB-E2-035 (rwb-case). In rwb-comms read action_text, owner_role and timer_spec only where a notice is decided by a route-set rule; test with legacy R-RES-04 values. |

### OTHER:rwb-decision Epic 2 rule packages story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07217 | RWB-P3-E2042-OPS | GAP-1302 |  | Write placeholders for the package title (DF-REF-276), dry-run breakdown (DF-REF-293), MSG-P3-015 text, rollback answer body and switch-off answers, using ASM-B-P7-05-E2042-7 defaults. |

### OTHER:TSD P7 v2 section T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07221 | RWB-P3-E2042-OPS | GAP-1298 | find it | Add the LOV-DECISION values written by load, approval, promotion and rollback, confirmed by the decision log owner before SIT; the story resolves the code at run time through DP-07 with no literal. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07222 | RWB-P3-E2042-OPS | GAP-1299 |  | Write the login only as 'the rwb-decision login (DP-02)'. Never use the shared monolith login. |

### OTHER:rwb-decision Epic 2 rule packages story and FSD P7 v3 MSG-P3-027 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07223 | RWB-P3-E2042-OPS | GAP-1300 |  | Fix the {detail} for the match order and catalog completeness checks to rule IDs, row orders and column names only, with no case fact or person. Confirm wording with the business analyst before SIT. |

### OTHER:Temporal and Drools Design Text Extract v1; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07225 | RWB-P3-E2042-OPS | GAP-2026 | find it | Name one owning service for PAYMENT_MATCH (proposed S2 rwb-treatment, with matchPayments asking S2 through its contract) on slide 18 and slide 14, and record it as an assumption until the package is authored. |

### OTHER:Rules Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07226 | RWB-P3-E2042-OPS | GAP-2034 | find it | Name the service that evaluates UNIVERSAL (R-UNI-01 to 50) for the other services, or state that each service evaluates its own copy of the approved version, with authoring and approval in rwb-decision (P7). |

### OTHER:Decision-record entry field list for the DP-03 library (rwb.decision-record.v1), owner role Data steward (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07227 | RWB-P3-E2042-OPS | GAP-2397 | 13 | Confirm which field ID carries the rule package code and which carries the SHA-256 checksum on the decision record. The source documents do not name them: Not specified in the source documents (GAP-2397). |

### OTHER:Refinement size record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07230 | RWB-P3-E2043-APP | Definition of Ready item 16 Size: Fail | section header | Size placeholder row added to the header table |

### OTHER:rwb-case contract (contract version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07233 | RWB-P3-E2043-APP | Definition of Ready item 23 Contract version fixed: Fail | section 1 | Contract version placeholder row added to the header table |

### OTHER:Recovery Workbench Functional Specifications by Module v7; OTHER:FSD P1 Recovery data engine v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07239 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-10 |  | Define empty, loading, error and no-access states for SCR-44 Interface and job monitor. Not specified in the source documents (DOR-RWB-P3-E2043-APP-10). |

### RWB-P3-E2043-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07241 | RWB-P3-E2043-APP | DOR-RWB-P3-E2043-APP-17 | find it | Complete RWB-P3-E2043-OPS, the external dependency not yet done |

### OTHER:Temporal and Drools Design v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07244 | RWB-P3-E2043-APP | GAP-2024 |  | Parent forwards DeviationRaised to the running stage child; the child pauses its own stage timer on DeviationRaised and resumes it on DeviationCleared (slide 24 wording replaced). |

### OTHER:ownership.json and the rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07245 | RWB-P3-E2043-APP | GAP-0422 | find it | Add a rwb-case outbox delivery read to the rwb-case contract, or record that the retry is asserted only through the effect and the event key on rwb.case.events.v1. Harness, SIT, seeding and gate are agreed by the integration lead at the wave 2 entry check. |

### OTHER:rwb.decision-record.v1 AsyncAPI schema and the OpenAPI of the two decision-log operations (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07248 | RWB-P3-E2043-APP | GAP-1304 | find it | Publish the schema and operations at the wave 2 design review, and approve the three ingest columns of decision_log_entry and the three message texts. Until then the story holds the assumed shape of ASM-B-P7-05-E2043-1. |

### OTHER:SCR-44 state definitions in the functional specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07253 | RWB-P3-E2043-APP | SCR-44 has no empty, loading, error, no access state in the story | section 15 | Placeholder for the four states added |

### OTHER:ACE DB story (wave 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07255 | RWB-P3-E2043-APP | GAP-1307 | 13 | Allocate the rwb-decision schema login in wave 1 and keep it in the platform secret store; the story takes it as a secret reference |

### OTHER:Workflow Engine Design v3 section 5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07256 | RWB-P3-E2043-APP | GAP-2021 | 12.5 | Define child and kit workflow IDs generated by the parent from case ID and stage code, unique per stage so a restart creates no second child |

### OTHER:Story metadata rows (next story-set version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07258 | RWB-P3-E2043-APP | GAP-1308 | 13 | DP-07 row marks C RWB-P3-E1043-CON as DP-added; DP-04 row keeps the original text |

### OTHER:Squad sizing process (not in any source) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07260 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-16 Size: Fail | header | Size row marked Not specified in the source documents (DOR-RWB-P3-E2043-CON-16) |

### OTHER:P3 screen specification for SCR-44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07267 | RWB-P3-E2043-CON | DOR-RWB-P3-E2043-CON-10 Screens and states: Partial |  | The four states belong to the SCR-44 screen spec, which is outside this story; no state text invented here. |

### OTHER:Workflow Engine Design v3 section 4; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07271 | RWB-P3-E2043-CON | GAP-2016 |  | Adopted fix recorded for the design documents. This contract uses RecordAndApplyActivity as the single writer. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:Temporal and Drools Design v1 slide 24 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07272 | RWB-P3-E2043-CON | GAP-2024 |  | Adopted fix recorded for the architecture and design documents; no change needed in this contract story. |

### OTHER:Integration harness plan and ownership.json (P2 rwb-integration outbox reads) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07273 | RWB-P3-E2043-CON | GAP-0422 |  | Harness decisions and the retry choice are recorded outside this story, before the harness is declared Done. |

### OTHER:Platform workflow kit policy (DevOps team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07274 | RWB-P3-E2043-CON | GAP-0725 |  | Adopted fix recorded for the platform workflow kit owner; no build values in this story. |

### OTHER:Message catalogue (MSG-P3-038 text) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07275 | RWB-P3-E2043-CON | GAP-0726 Replay corpus, history retention and the text of MSG-P3-038 | 16 | MSG-P3-038 reference removed from TC-P3-E2043-CON-06; replay corpus wording kept. |

### OTHER:AsyncAPI schema of rwb.decision-record.v1 and OpenAPI of the two decision-log operations (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07276 | RWB-P3-E2043-CON | GAP-1304 |  | Publish the schema of rwb.decision-record.v1, the OpenAPI of the two decision-log operations, the three decision_log_entry ingest columns and the three message texts at the wave 2 design review. |

### OTHER:Test resources of the app story RWB-E2-043 (DEV and SIT) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07282 | RWB-P3-E2043-CON | GAP-0724 |  | Keep RW-2026-000777 as a JSON seed owned by the app story, loaded and removed per run in DEV and SIT only, carried by no release. |

### OTHER:ACE DB story of wave 1 (schema and login allocation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07283 | RWB-P3-E2043-CON | GAP-1307 |  | Story already refers to the rwb-decision login without a literal name; allocation sits in the ACE DB story. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07286 | RWB-P3-E2043-CON | GAP-1308 |  | Item says three C dependencies but names two; only the two named are carried. Metadata rows unchanged this version. |

### OTHER:Workflow Engine Design v3 (section 4); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07298 | RWB-P3-E2043-OPS | GAP-2016 | find it | Make the durable timer authoritative; keep the timer row as audit copy, written by ApplyStateActivity in the same transaction and read back on reopen. |

### OTHER:Temporal and Drools Design v1 (slide 24); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07299 | RWB-P3-E2043-OPS | GAP-2024 | find it | The parent forwards DeviationRaised to the running stage child; the child pauses and resumes its own stage timer on DeviationRaised and DeviationCleared. |

### OTHER:Harness and SIT environment values (not in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07300 | RWB-P3-E2043-OPS | GAP-0422 | header | Outbox retry check row recorded; harness row carries not-specified placeholders |

### OTHER:Platform workflow kit worker versioning policy (DevOps team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07301 | RWB-P3-E2043-OPS | GAP-0725 | find it | Build ID is the release commit ID supplied by the workflow kit; pin builds with drain-on-complete; set the policy once for all 19 services. |

### OTHER:Message catalogue (MSG-P3-038) and replay-gate corpus record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07302 | RWB-P3-E2043-OPS | GAP-0726 | find it | Take the MSG-P3-038 text from the message catalogue. Replay one recorded history per acceptance path of the reference fixture, kept with the contract jar. |

### OTHER:rwb.decision-record.v1 AsyncAPI schema and decision-log OpenAPI (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07303 | RWB-P3-E2043-OPS | GAP-1304 | find it | Publish the AsyncAPI schema and the two decision-log OpenAPI operations; approve the three decision_log_entry ingest columns and three message texts at wave 2 design review. |

### OTHER:Reference fixture owner (GAP-0724) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07309 | RWB-P3-E2043-OPS | GAP-0724 | 7 | Background seed lifecycle and store added in section 7; owner still not specified. |

### OTHER:ACE DB story of wave 1 (rwb-decision schema and login allocation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07311 | RWB-P3-E2043-OPS | GAP-1307 |  | Allocate the rwb-decision schema login with its schema and keep it in the platform secret store; the story and migration take it as a secret reference. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07315 | RWB-P3-E3013-APP | CG-ALL-4450 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or name a published operation instead. |

### OTHER:rwb-access API yaml (P4 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07321 | RWB-P3-E3013-APP | DOR-RWB-P3-E3013-APP-8 | 12.3, 12.8 | Publish POST /api/recovery/access/v1/authorise in the rwb-access API yaml. |

### OTHER:Recovery Workbench P2 field catalogue (personal-data classes) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07326 | RWB-P3-E3013-APP | DOR-RWB-P3-E3013-APP-11 | 8 | Reconcile the personal-data class of the P2 fields with this story's statement that it carries none of them (BR9). |

### OTHER:RWB-P2 story that carries MSG-P3-027 (outside this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07327 | RWB-P3-E3013-APP | DOR-RWB-P3-E3013-APP-9 | 14 | Align its MSG-P3-027 text to the Error and Message Standard v4 row MSG-P3-027 (Error and Message Standard v4, line 148). |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07329 | RWB-P3-E3013-APP | GAP-2675 | 12 | Publish the readiness section (checkType, encumbranceStatus, registrationStatus, titleSetStatus, checkedAt, ruleId, ruleVersion, holdUntil, collateralNo, assetKey), TitleSetTaskRequest, the three view ranges as read only, and errors 401, 403 MSG-P4-002, 404, 422 MSG-GEN-001, 503. |

### OTHER:Recovery Workbench CCMS and Land Office check interface and SIT harness specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07330 | RWB-P3-E3013-APP | GAP-0425 | 16 | Name one check interface with codes and fixture result set; one SIT harness environment and repository; one seeding set of two cases with treatments, accounts, asset keys; exact values of six fakes; evidence report shape, retention and gate. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07331 | RWB-P3-E3013-APP | GAP-1559 | 10.3 | Relabel RWB-P3-E3013-APP from wave 3 to wave 2 to match BRD Program v5 section 10.3 for EP03. Release date 31 January 2027 is unchanged. |

### 05 Technical architecture/Recovery Workbench Interface Specifications v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20612 | RWB-P3-E3013-APP | R-22756 |  | Check codes, SIT harness, seeding set, fakes and evidence report belong to the CCMS and Land Office check interface and SIT harness specification. No values here. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20899 | RWB-P3-E2042-INF | R-22383 |  | Item text not re-read in this run, so no fix was written. Not verified against this document. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0421 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0422 | Reference workflow harness repository and SIT environment, seeding, evidence format and gate are not specified, and the ownership map holds no rwb-case outbox delivery read | Integration lead | Resolved (directive) |
| GAP-0425 | The CCMS and Land Office check interface, the harness environment and seeding set, the fake response values and the evidence and gate of the early readiness harness are not in the sources | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0721 | The rule package registry is declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0722 | The rule-model and rule-catalog read operations have no published field-level shape | P7 rwb-decision owner | Resolved (directive) |
| GAP-0723 | Blob immutability period, pod memory for 20 KieBases, alert windows and probe timings are not specified | SCB IT infrastructure with the DevOps team | Resolved (directive) |
| GAP-0724 | Reference fixture lifecycle, store and owner for the synthetic case | TechX | Resolved (directive) |
| GAP-0725 | Worker build ID format and worker versioning policy are not stated | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0726 | Replay corpus, history retention and the text of MSG-P3-038 | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0727 | Field-level detail of RecordAndApplyRequest and of the rule outputs map | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0736 | The encumbrance-check slice leaves the requirement ID, the check-versus-state boundary, the S2 answer shape, the rule timer specs and three new field IDs unspecified | Tech lead | Resolved (directive) |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0967 | rwb-access rule-package authority: the scope of a running service identity inside rwb-access and the capability area each rule package serves are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0968 | rwb-access rule-package authority: TSD P4 v3 gives P4 the four rule tables, while Architecture v5 and the ownership ruling put the rule registry in P7 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0969 | rwb-access rule-package authority: the lifetime of a cached authorise answer, the refresh trigger of the cached permission data and the granularity of the access-log entry of a dry run are not specified | Solution architect | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1298 | The decision code of a rule-governance entry is not named in any source this key may read | Decision log owner | Resolved (directive) |
| GAP-1299 | The name of the rwb-decision database login is not specified | ACE database administrator | Resolved (directive) |
| GAP-1300 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Business analyst | Resolved (directive) |
| GAP-1301 | The four rule registry tables are declared for P4 and P3 in their TSDs and are absent from the P7 TSD | Solution architect | Resolved (directive) |
| GAP-1302 | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Business analyst | Resolved (directive) |
| GAP-1303 | The BRD section pointers copied from the legacy story no longer match BRD v2 and v4 | Business analyst | Resolved (directive) |
| GAP-1304 | The payload of DecisionRecorded, the field set of the ledger ingest and the answer bodies of the two reads have no source | Solution architect, P7 rwb-decision, with the platform outbox and event team, the P3 business analyst and the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1305 | The collection target of five minutes and the chain-check time of 02:00 are named as values but no source names them as parameter rows | Center of excellence analyst with the P3 rwb-case team and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1307 | The name of the per-service database login of rwb-decision is not fixed by any source | ACE DB team with the P7 rwb-decision team | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1559 | The encumbrance slice is labelled wave 3 although its business epic is released in the wave 2 window | Program manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1702 | The FSD triggers on a completed ACE batch, and AceDataReady does not reach this service while no S2 job exists in the job map | Solution architect with the P1 owner | Resolved (directive) |
| GAP-1705 | The CCMS release, the Land Office title check and the asset take-on have no path from this service in Architecture v5 | Solution architect with the integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1994 | payment_match_rule has no owner in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2018 | Strict-mode wait at a point of no return is not defined in this design | Service owner P7 rwb-decision with the saga owners S2, S5, S6 and S7 | Resolved (directive) |
| GAP-2019 | Child workflow start policy and failure path are not specified | Service owner P3 rwb-case with the stage owners S1 to S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2021 | Child and kit workflow ID format | Service owner P3 rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2024 | Who pauses the stage clock when the stage runs as a child | Service owner P3 rwb-case with S8 rwb-deviation | Resolved (directive) |
| GAP-2026 | Owning service of the PAYMENT_MATCH package is not stated in one place | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2034 | The UNIVERSAL package has no single owning service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2053 | Outbox scope: Epics 1 and 2 in version 3, every service in Arch v5 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2396 | Architecture v5 slide 13 gives P6 to P7 a Temporal cell and no event cell, while RWB-P6-E1073-APP consumes RulePackageInForce from rwb.decision.events.v1 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2397 | No source states where the package version and checksum of a notice decision are stored, and the legacy story adds no column for them | Data steward | Resolved (directive) |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2399 | No source states the state a notice rests in, or the message, when no package version is in force | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2405 | rwb-decision next action: the answer shape of the rule-catalog and latest-state-change reads, and their not-found and malformed-parameter messages, are not specified | Solution architect | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2409 | The published catalogue path shows packageVersion as an optional query parameter and no source says what an absent value answers | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2674 | The readiness check result, the title-set task, the trigger and the ACE status field are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P1 owner of the ACE read and the owner of the local decision-record library | Resolved (directive) |
| GAP-2675 | The published shape of the readiness section, of the title-set task request and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract and the P1 owner of the ACE read | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E2042-INF | date added | 1 | 2026-12-01 |
