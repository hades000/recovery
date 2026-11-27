# RWB-PLT-EDGE Edge and gateway - review pack, part 2 of 2 (RWB-PLT-N001-CON to RWB-PLT-NF07-INF)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 4 |
| Resolved in the stories | 41 |
| Cross-document (pending in another document) | 177 |
| Not applied (value not in the sources) | 20 |
| Open business decisions | 8 |
| Register gaps linked | 193 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-N001-CON | 20 | 157 | 19 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EDGE Edge and gateway/RWB PLT N001 CON gateway-bff route contract - contract v2.md |
| RWB-PLT-N006-INF | 7 | 5 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EDGE Edge and gateway/RWB PLT N006 INF Redis session store for gateway-bff - infrastructure v2.md |
| RWB-PLT-N007-INF | 7 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EDGE Edge and gateway/RWB PLT N007 INF Partner gateway in the DMZ (FAPI 2.0) - infrastructure v2.md |
| RWB-PLT-NF07-INF | 7 | 6 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EDGE Edge and gateway/RWB PLT NF07 INF Airflow edge integration - infrastructure v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23240 | GAP-3029 | Register gap | Solution architect; business lead | RWB-S7-E6019-APP: the reject reason and the decision code have no field, column or list, R-WO-16's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes three contracts, DP-04 and DP-09 are absent, and no published row moves a case out of RETURNED_TO_PURSUE | Keep the plan's H, C, I and X rows as they stand; record the reason and the decision code as request and record inputs with a placeholder until the business lead confirms them; map R-WO-16's owner to the four roles that hold right A in TSD S7 T6.1; declare the three consumed rows in sections 12.2 and 12.8 and record the absent DP-04 and DP-09 rows; leave the onward path of RETURNED_TO_PURSUE to the case owner and raise it in the next planning cut; keep committee_date and every other write_off column out of the reject slice |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23241 | GAP-3117 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S9-E6034-APP: the legacy story names two read endpoints and no operation that places the account, partner_instruction carries no rule-version or decision column, S9 owns no route set so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32, the legacy permission table gives the Partner portal right R while the issue needs C and the FSD also-uses role has no matrix row, both screens are list states with no placement form, the plan C row is empty while the case and the rule package are consumed, DP-04 and DP-09 are absent, the EV-20 consumer set and payload are not published, and no requirement row traces to FEAT-PRM-06 | Keep the plan H, C, I and X rows as they stand; issue the placement through API-S9-002 and never through a new path; record the rule version and the picked agency on the local decision record and add no column to partner_instruction; read the placement rows from rwb-decision as data and record the absent DP-04 rows; read the case on the rwb-case contract and record the absent C rows; authorise the issue on the Partner portal right C the matrix gives and record the legacy right R and the missing also-uses row as conflicts; serve the placement from the list state of SCR-35 through the composite route and carry the form as a placeholder; publish EV-20 with IDs only and record the absent DP-09 row; let the trace rest on the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-S6-E6005-APP, RWB-S6-E6012-APP | R-23244 | GAP-3015 | Register gap | Solution architect with the owners of rwb-case (P3), rwb-decision (P7), rwb-access (P4) and rwb-source-data (P1), and the business owner of the debt sale cap | RWB-S6-E6012-APP: the cap slice has no plan row for the five consumed contracts, no cap parameter row, no cap route rule, no published trigger, no headroom column and no service contract baseline | Publish the five consumed operations with their fake; add C rows for rwb-case, rwb-decision, rwb-access and rwb-source-data; add the DP-04, DP-06, DP-07, DP-08 and DP-09 rows the tables need; name the cap row, its version, its basis and its owner; publish one route rule for the cap or confirm that R-DS-19 and R-DS-23 are its only test and which story owns them; publish the trigger or confirm the call from the lot build and award steps; add the cap-position and headroom fields or confirm the decision record as their only home; create the service contract baseline for this legacy key; and carry REQ-S6-001 and BR-050 in the plan |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-S8-E7009-APP, RWB-S8-E7009-CON | R-23272 | GAP-3068 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S8-E7009-APP: neither deviation nor any other owned table carries a complaint or contact reference, no published rule row expresses the match, no requirement row traces to FEAT-DVF-09, the Conduct and QA officer holds R only while the feature needs U, the plan's C row is empty while two contracts are consumed, DP-04, DP-05, DP-09 and DP-18 are absent, and no event carries the match to rwb-reporting | Keep the plan's H, C, I and X rows as they stand; carry the complaint and contact references and the match outcome as request inputs recorded on the local decision record until the business lead confirms their names, formats and value set; declare the two consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-05, DP-09 and DP-18 rows; read the contact through rwb-source-data as the connection matrix gives it and never through EFS; authorise the match on the case-record right U the permission table gives and record the matrix row as the conflict; let the trace rest on the legacy key and the feature row until the E7 BRD and the PRD publish a requirement; leave the conduct measure on the decision-record ledger until an event exists |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-N001-CON | R-18742 | DOR-RWB-PLT-N001-CON-4 | 7, 8 | Definition of Ready item 4 Business rules: Partial | BR11 to BR13 have no criterion or test; AC7 traces BR1 to BR9 only. Left open until the rules are traced. |
| RWB-PLT-N001-CON | R-21987 | GAP-0674 | 11 | gateway-bff composite route for the case screens is not specified | Path, parallel calls, merge and 2 s budget already in header and section 12. Masking rule is not in any source; the section 11 placeholder stays (GAP-0674). |
| RWB-PLT-N001-CON | R-22340 | GAP-0386 | 11 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Harness, environments, seed values, evidence format and gate are in no source read. Composite route is the GAP-0773 row in section 11. Nothing added. |
| RWB-PLT-N001-CON | R-22341 | GAP-0773 | 11 | The gateway-bff composite route of the case record plan section is not specified | Merge rule already in section 11. Route path, masking rule and 2 s budget split are not in any source, so the placeholder stays (GAP-0773). |
| RWB-PLT-N001-CON | R-22346 | GAP-0390 | 11 | Customer other-products harness pack: repository, environments, seeding, evidence format, gate and composite route are not specified | Harness, environments, seeds and gate are in no source. Other-products composite path and merge order are not in sources; the section 11 placeholder stays. |
| RWB-PLT-N001-CON | R-22473 | GAP-0732 | 12 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Approval event fields, task fields, status mapping, escalation and rwb-case login are in no source read. Composite field list sits in RWB-PLT-N001-APP section 11. |
| RWB-PLT-N001-CON | R-22519 | GAP-0401 |  | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Harness pack, environment, seeding, evidence format and wave 2 gate are QA decisions with no source value. Section 12 composite route is the case screen only. Nothing written. |
| RWB-PLT-N001-CON | R-22939 | GAP-0385 |  | The wave 1 journey harness environment, seeded data, evidence format and release gate are not specified | Wave 1 harness pack, environment, seeded identifiers, business date, evidence format, gate and P10 agent-run start operation are not in the sources. QA decision. Nothing written. |
| RWB-PLT-N001-CON | R-22940 | GAP-0428 |  | The wave 2 journey harness environment, seeded data, evidence format and release gate are not specified | Wave 2 harness pack, seeded data, business date, evidence format, gate and rwb-deviation read operation are not in the sources. QA decision. Nothing written. |
| RWB-PLT-N001-CON | R-23271 | GAP-3070 |  | RWB-S8-E7010-APP: the contact-breach path has no rule row, no column, no published ledger read, no operation of its own, no event and no write right for its primary role | Fix concerns the RWB-S8-E7010-APP story and its rules, columns and rights, not this story. Its text is not in this chunk, so no edit here. |
| RWB-PLT-N001-CON | R-28444 | GAP-1279 |  | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Fix concerns rwb-decision story text not in this chunk. The login, migration and index names are in no source checked. No edit here. |
| RWB-PLT-N001-CON | R-28445 | GAP-2540 |  | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Concerns the B2-P8-008 story. Header already shows Release None and Ready Day 1. Preconditions and fakes text is not in this chunk. |
| RWB-PLT-N001-CON | R-28496 | GAP-1028 |  | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Concerns the RWB-P5-E1016-APP secondary slice and its catalog contracts. That text is not in this chunk, so no edit here. |
| RWB-PLT-N001-CON | R-28505 | GAP-2429 |  | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Concerns the metadata and pattern rows of another secondary slice; sections 3, 12.2, 12.8 and 13 are not in this chunk. No edit here. |
| RWB-PLT-N001-CON | R-28541 | GAP-3082 |  | RWB-S8-E1023-APP: a P3 Case and workflow module story is placed in rwb-deviation with an empty build row, and the plan gives the slice no platform dependency although seven pattern rows add one | Concerns the RWB-S8-E1023-APP slice in rwb-deviation, not this story. Its text is not in this chunk, so no edit here. |
| RWB-PLT-N001-CON | R-28547 | GAP-1035 | Header | The SCR-30 route specification in the gateway-bff composite route is not specified | SCR-30 path, merged fields and budget are in no source (Grep: only a screen index entry in PRD P5 document hub). Added a Not specified row to the header as a placeholder. |
| RWB-PLT-N001-CON | R-28574 | GAP-3140 |  | The DP table names platform H rows that the plan's H list does not carry | Concerns the H list of slice RWB-S9-E1032-APP in another story. That text is not in this chunk, so no edit here. |
| RWB-PLT-N001-CON | R-28619 | GAP-1083 | header | The scope and right check of the notice operations has no rwb-access dependency row | Edge enforcement of the Litigation right is not in any source; the scope and right check stays open for the rwb-access dependency row. |
| RWB-PLT-N001-CON | R-28812 | GAP-0951 | header | Whether the field app reaches the authorise path through gateway-bff or directly is not specified | The source leaves open whether the field app uses gateway-bff or direct access; the earlier routing text was invented and is removed. |
| RWB-PLT-N007-INF | R-23290 | GAP-1676 | 7 | The partner gateway provision and its penetration-test scope are open | Provision under DL03 and pen-test scope are business decisions with no value in NFS v3 s1 or Arch v5 slide 35 (per item notes). Story AC7 left unchanged; no value invented. |

## 5. Cross-document changes (pending in the target document)


### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14923 | RWB-PLT-N001-CON | GAP-1206 | n/a | Set six build H rows and three contract C rows per the DP table; keep the written story metadata until the plan is corrected. |
| CDC-14932 | RWB-PLT-N001-CON | GAP-1343 |  | List the six DP-added dependencies (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) with RWB-P7-E2006-APP as consumer; optionally add C row RWB-P4-E1037-CON to its story object. |
| CDC-14934 | RWB-PLT-N001-CON | GAP-2501 | not in chunk | Record the DP-added H and C dependencies as non-blocking platform and published contracts, built against their fakes. |
| CDC-14941 | RWB-PLT-N001-CON | GAP-2354 |  | Record the six platform CONs as wave-0 prerequisites of wave-1 services and add RWB-P3-E1043-CON to the contract rows of DP-07 stories. |
| CDC-14945 | RWB-PLT-N001-CON | GAP-1291 |  | Keep the metadata rows as given. Record H RWB-PLT-E1027-CON, H RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON as non-blocking, built against fakes. |
| CDC-14948 | RWB-PLT-N001-CON | GAP-2317 |  | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON to the H list, and C RWB-P3-E1043-CON to the C list for the affected rows. Keep the Work Package metadata unchanged. |
| CDC-14976 | RWB-PLT-N001-CON | GAP-2760 | find it | Carry the three pack-recovery consumed contracts as non-blocking rows, naming the P5 document reads and the P3 case-move answer; leave metadata rows unchanged. |
| CDC-14978 | RWB-PLT-N001-CON | GAP-1885 | find it | Carry the five non-blocking consumed rows (P7 approval, P3 case and reference data, P4 partner instruction, platform reads) and their declared rights as edge guard rules. |
| CDC-14979 | RWB-PLT-N001-CON | GAP-2751 | header | Add non-blocking consumed rows for API-P5-002, API-P5-008 and API-P3-002 built on fakes; C dependency of RWB-P3-E1043-CON for the reference-data read; DP-08 edge and guard rule for the declared right. |
| CDC-14980 | RWB-PLT-N001-CON | GAP-2801 | header | Add the D7.4 approval contract as C dependency of its wave; add the rwb-case and rwb-partner contracts as published contracts built on fakes; add RWB-P3-E1043-CON as C dependency; DP-08 edge and guard for each right. |
| CDC-14990 | RWB-PLT-N001-CON | GAP-2797 |  | Consume the LITIGATION package from rwb-decision as a non-blocking contract with its fake at the version in force; declare no rule row, package or rule version in the stories. |
| CDC-15033 | RWB-PLT-N001-CON | GAP-1335 |  | Show the six platform contracts and the two rwb-case contracts in the wave 2 dependency map. Keep the story metadata rows as the story object fixes them. |
| CDC-15035 | RWB-PLT-N001-CON | GAP-1337 |  | Show the platform contracts and the rwb-case rule-package, parameters and reference-data contracts in the wave 2 dependency map. Keep the metadata rows as the story object fixes them. |
| CDC-15037 | RWB-PLT-N001-CON | GAP-1340 |  | When the build order and dependency map are assembled, read the twelve DP-added dependencies from section 13 and leave the metadata rows as the WP fixes them. |
| CDC-15051 | RWB-PLT-N001-CON | GAP-1308 |  | Carry the platform H and published C dependencies as DP-added in the dependency map; correct metadata rows at the next story set version. |
| CDC-15053 | RWB-PLT-N001-CON | GAP-1319 |  | Carry the seven platform H, three published C and the P4 authorise answer as DP-added in the dependency map; correct metadata rows at next version. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14907 | RWB-PLT-N001-CON | DOR-RWB-PLT-N001-CON-14 | header | Record the signed epic design sign-off for RWB-PLT-EDGE; no signed design exists in the source documents |
| CDC-15084 | RWB-PLT-N006-INF | DOR-RWB-PLT-N006-INF-14 | find it | Record the signed epic design sign-off for RWB-PLT-EDGE in the epic design record; the story cannot carry a sign-off not in the sources. |
| CDC-15089 | RWB-PLT-N007-INF | DOR-RWB-PLT-N007-INF-14 | header | Record the signed epic design sign-off for RWB-PLT-EDGE, which is not in the story or the source documents. |
| CDC-15173 | RWB-PLT-NF07-INF | DOR-RWB-PLT-NF07-INF-14 | find it | Confirm and record the signed epic design sign-off for RWB-PLT-EDGE |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14909 | RWB-PLT-N001-CON | DOR-RWB-PLT-N001-CON-12 | 16 | Align the test lists for REQ-OCC-007, NFR-008 and NFR-009 with section 18 of RWB-PLT-N001-CON, which cites TC-PLT-N001-CON-01 to -06 from section 16 |
| CDC-15026 | RWB-PLT-N001-CON | CG-ALL-1278 | 18 | In the next RTM version, align the REQ-OCC-007 test list with section 18 of RWB-PLT-N001-CON (TC-PLT-N001-CON-01, TC-PLT-N001-CON-02, TC-PLT-N001-CON-06). |
| CDC-15092 | RWB-PLT-N007-INF | DOR-RWB-PLT-N007-INF-12 | 16, 18 | Section 16 now has eight test cases after TC-PLT-N007-INF-08 was added. Section 18 must list TC-08 and still differs from RTM v7; TC-PLT-N007-INF-06 appears in no section 18 row. |
| CDC-15095 | RWB-PLT-N007-INF | CG-ALL-1280 §18 test lists differ from RTM v7 | section 18 | Story keeps its §18 IDs. Section 16 now also holds TC-PLT-N007-INF-08, which section 18 does not list yet. RTM v7 needs the matching update in its next version. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14908 | RWB-PLT-N001-CON | DOR-RWB-PLT-N001-CON-1 | 1 | Add the role consumer of the gateway-bff route contract with a role code, or name the existing role code that consumes the route contract |
| CDC-15085 | RWB-PLT-N006-INF | DOR-RWB-PLT-N006-INF-1 | 1 | Add 'infrastructure engineer' as a role code or role name, or confirm the role that the story should name. |
| CDC-15091 | RWB-PLT-N007-INF | DOR-RWB-PLT-N007-INF-1 | 1 | Add 'infrastructure and security engineer' as a role code or role name, or map this story's role to an existing role code. |

### RWB-P7-E2014-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14937 | RWB-PLT-N001-CON | GAP-1258 |  | Publish the field list and mask flags of the two approval-screen panels as the working read, then confirm with the route owner and consumer sign-offs. |
| CDC-14938 | RWB-PLT-N001-CON | GAP-1259 |  | Carry GET /api/recovery/approvals/{approvalId} as the working read and register it with the route owner at the first version freeze. |
| CDC-14939 | RWB-PLT-N001-CON | GAP-1267 |  | Confirm AC4 there: keep READY, STALE_INPUT, DECIDED, GENERATED, APPROVED and HELD as panel states, with loading, unavailable and session-expired as route overlay states. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14940 | RWB-PLT-N001-CON | GAP-2742 |  | Carry the P6 notice generate and send call and the rwb-case stage answer as non-blocking C rows; record notice and template rows as P6's or correct the S4 row; add REQ-S4-001 to the key trace. |
| CDC-14963 | RWB-PLT-N001-CON | GAP-2281 | Header | Provide POST and GET /api/recovery/access/v1/admin/panel-changes with their fields, the partner_panel handoff to the P3 reference-load contract, and the P7 rule-version read. |
| CDC-14967 | RWB-PLT-N001-CON | GAP-2099 | Header | Add one row for gateway-bff, the Redis session and the App Gateway route, owned by RWB-PLT-EDGE and RWB-PLT-N001-CON, before wave 0 closes. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14910 | RWB-PLT-N001-CON | GAP-0728 | 11 | Publish the three rwb-case console read operations; add reconciliation, business-key resolution and freshness GET operations with a business-date query parameter and a paged answer to rwb-source-data; name the rwb-case login with the ACE DB owners |
| CDC-15040 | RWB-PLT-N001-CON | GAP-1349 | 13 | Map GET /cases/{id}/payments to GET /proceeds with case scope; publish no extra operation; name workflow matchPayments and its four step activities. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14912 | RWB-PLT-N001-CON | GAP-0673 | n/a | Mark FSD P2 Integration A1.5 and TSD T1/T5.1 INT-03 lines superseded for this legacy key with date and decision; load one versioned ALS interface_config row per environment with owner-agreed values. |
| CDC-15029 | RWB-PLT-N001-CON | GAP-2455 | header | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry; producer local record is working record and ledger entry is record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0/1 baseline outside the H row. |

### RWB-P4-E8017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14972 | RWB-PLT-N001-CON | GAP-0879 |  | Fix four operations on /api/recovery/access/v1/admin/incidents, the OPEN and CLOSED states, five step names, step record code, step shape and report fields. Feed nothing from the observability platform. |
| CDC-14973 | RWB-PLT-N001-CON | GAP-2301 |  | Build the incident as rwb-access chain entries, not a table: one entry for DETECTED and HELD on open, one for FIXED, RECORDED and REPORTED on closure. Fix three paths on the access base and OPEN and CLOSED states. |

### RWB-P6-E4035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14974 | RWB-PLT-N001-CON | GAP-2363 | find it | Declare the two customer offer-view operations, their capability area and right, and channel screens per the proposed fix; notice endpoints and SCR-33 stay with their stories. |
| CDC-14975 | RWB-PLT-N001-CON | GAP-2367 | find it | Confirm capability area and right of the two offer-view operations with the rwb-access owner in baseline review; keep scope on the case. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15022 | RWB-PLT-N001-CON | GAP-3227 | - | Set Release for RWB-PLT-N001 to N012 (CON variants) and RWB-PLT-NF01 to NF08 to Window 1 (E1, 30 November 2026, tentative), or to a named wave-0 release date. |
| CDC-15038 | RWB-PLT-N001-CON | GAP-2484 |  | Keep the metadata rows as the WP gives them. Treat the four platform contracts as published before Day 1. Assign the recommendation read to the P7 story serving the decision screen. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15036 | RWB-PLT-N001-CON | GAP-0913 |  | Publish the SCR-03 other products composite route with its field list, merge order and masking step (last-four shape) under RWB-PLT-N001-CON. |
| CDC-15042 | RWB-PLT-N001-CON | GAP-0944 |  | Publish the composite field lists for SCR-14 and SCR-30 and add the allowed-action decision code to the ledger decision-code list before the audit query is built. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:DP-06; OTHER:DP-07; OTHER:DP-09; OTHER:DP-15 and DP-19 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15044 | RWB-PLT-N001-CON | GAP-1282 | 13 | Carry the six platform H rows and the three C rows RWB-P3-E1042-CON, RWB-P3-E1043-CON and the DP-11 legacy C as DP-added. Keep Ready to start Day 1. |
| CDC-15046 | RWB-PLT-N001-CON | GAP-1288 | 13 | Carry the six platform H rows, the two rwb-case C rows, the store baseline and the rwb-access authorise contract as DP-added. Keep Ready to start Day 1. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15055 | RWB-PLT-N001-CON | GAP-0141 | none | Rewrite every operation under /api/recovery/<short>/v1 in API Specification v5, keeping the Ownership Map v1 operation-to-service assignment. |
| CDC-15093 | RWB-PLT-N007-INF | GAP-0784 | 8 | Register the partner identity resolution operation on the P4 base with its claim set, answer schema, PLACED scope type and answer lifetime, confirmed at the RWB-P4-E2019-CON contract review. |

### OTHER:Contract story for the Airflow calls to the Recovery APIs (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15174 | RWB-PLT-NF07-INF | DOR-RWB-PLT-NF07-INF-21 | find it | Contract dependency named without a story key; publication not shown in this story. |
| CDC-15176 | RWB-PLT-NF07-INF | DOR-RWB-PLT-NF07-INF-23 | find it | Contract version row set to the Not specified marker in place of v1. |

### RWB-PLT-NF07-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15175 | RWB-PLT-NF07-INF | DOR-RWB-PLT-NF07-INF-22 | find it | Publish the contract fake library version and record it as published |
| CDC-15177 | RWB-PLT-NF07-INF | GAP-1396 | find it | Publish the Airflow product, tenancy, service principal, timeout and retry values, DailyCaseRun wait mechanism, and the three owner operation paths and payloads, agreed at the scheduling design review. |

### OTHER:Legacy RWB-DM-013 story and the Data Migration Approach (rwb-payment cutover load) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14911 | RWB-PLT-N001-CON | GAP-2533 | n/a | Publish the handover file spec (format, location, count, checksum, resolution stamp, retention), a named load command with run record and rights, a provenance and migration-date column, and the payment_code and H-row decisions. |

### OTHER:split_plan.json and the metadata rows of the dependent stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14913 | RWB-PLT-N001-CON | GAP-1161 | n/a | Keep plan lists as they stand; build against fakes of the six contracts; when published, add the six rows, re-run dependency check and replace fakes in the same iteration. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14914 | RWB-PLT-N001-CON | GAP-1946 | n/a | Keep H and C at None; record nine platform and rwb-case CONs as wave-0 prerequisites and fakes; read ACE side via DP06 data product; serve quality facts from the recovery asset routes; declare the quality design. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14915 | RWB-PLT-N001-CON | GAP-1167 | n/a | Keep H at None for the APP story; record the seven platform CONs as wave-0 build prerequisites with the platform release train; add them to the dependency map as platform prerequisites. |

### RWB-S8-E1021-APP; OTHER:LIB; OTHER:WF; OTHER:DB; OTHER:EVT; OTHER:EDGE platform owners (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14916 | RWB-PLT-N001-CON | GAP-3075 | n/a | Platform owner confirms which of the eight platform contract stories are published before release; story builds against baselines and fakes; assembler corrects metadata rows if the plan is reissued. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14917 | RWB-PLT-N001-CON | GAP-2404 | n/a | Read H as None plus the five platform contracts; read C as RWB-P10-E2032-CON plus the two P3 contracts and the published P4 authorise contract; platform contracts are service-template prerequisites. |

### RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14918 | RWB-PLT-N001-CON | GAP-2448 | n/a | Keep metadata rows as fixed by the work package; record the DP-table dependencies in section 13 of that story, built against fakes on Day 1. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14919 | RWB-PLT-N001-CON | GAP-1198 | n/a | Add the seven platform contracts and two P3 contracts to the dependency rows of RWB-P6-E1032-APP, or record in the platform release train that wave 1 services compile against them. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14920 | RWB-PLT-N001-CON | GAP-2414 | n/a | Set H to None plus the eight platform contracts from the DP table, and C to RWB-P3-E2041-CON plus the four published contracts; keep Ready to start Day 1. |

### OTHER:Integration composed case-list APP story and P3/P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14921 | RWB-PLT-N001-CON | GAP-0660 | n/a | Add the composed read and export on the integration base as a read-only composition; fix ageing, reference-data and access-log operations in the P3 and P4 contract stories. |

### OTHER:RWB-P7 slice of RWB-E1-046 (P7 APP story); RWB-P6-E1046-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14922 | RWB-PLT-N001-CON | GAP-2453 | n/a | Record one template_use row per accepted answer with no catalog copy; publish reads in RWB-P6-E1046-CON; treat three platform H rows as wave-0 prerequisites; fix table and migration. |

### OTHER:Agent monitoring dashboard v2 app story (RWB-E2-031 slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14924 | RWB-PLT-N001-CON | GAP-0629 |  | Settle the nine app-slice values as the item proposes: drift step in the v1 Schedule, segment from the run row, additive rwb-decision change, V10_007, policy values, range limits, login and route. |

### OTHER:rwb-access and rwb-agent contract stories; OTHER:FSD P4 and TSD P4 next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14925 | RWB-PLT-N001-CON | GAP-2333 | n/a | Add five platform contracts to H and two rwb-case contracts to C in the dependent stories; correct REQ-ACA-006 and NFR-042. |

### RWB-P2-E1073-APP; RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14926 | RWB-PLT-N001-CON | GAP-0672 | n/a | Record eight DP H rows as wave-0 prerequisites; publish the model fetch in RWB-P7-E1073-CON; fix the local copy table and name the login. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14927 | RWB-PLT-N001-CON | GAP-1328 | n/a | Complete the metadata rows from the DP table (eight H rows, DP-06 and DP-07 C rows, DP-09 in pattern list) or state the R5.5 exception. |

### OTHER:Assembler lane and Day-1 allocation (WP B2-P3-020) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14928 | RWB-PLT-N001-CON | GAP-2261 | n/a | Add platform CON dependencies RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON to lane and allocation. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14929 | RWB-PLT-N001-CON | GAP-2470 | not in chunk | Complete the metadata rows from the DP table, or state in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories. |

### OTHER:rwb-integration P1; OTHER:P3 and P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14930 | RWB-PLT-N001-CON | GAP-0662 | not in chunk | Fix contract field names, the per-service login, the ACE view owner and endpoint and route names as the proposed fix states. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14931 | RWB-PLT-N001-CON | GAP-2475 | not in chunk | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories, or complete the metadata rows. |

### RWB-S8-E2009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14933 | RWB-PLT-N001-CON | GAP-3087 | not in chunk | Record the slice as secondary serving of the steering data set and publish the seven consumed operation names with owners. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14935 | RWB-PLT-N001-CON | GAP-1223 | n/a | H list: None plus the platform contracts the DP table names (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON). C list: RWB-P7-E2013-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON. Story stays Day 1. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14936 | RWB-PLT-N001-CON | GAP-1265 |  | Add C rows RWB-P1-E1015-CON and RWB-P3-E1018-CON, or record the two reads as route-level composites of RWB-PLT-N001-CON. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14942 | RWB-PLT-N001-CON | GAP-0955 |  | Publish the authorise, me-permissions and masking-policies shapes before the send story is built. The composite field list for SCR-03 and SCR-04 is in this story's route section, not in this chunk. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14943 | RWB-PLT-N001-CON | GAP-1903 |  | Fix the fill trigger, write key, request and answer element names, hearing natural key and the parameter and list operation names as the GAP-1903 proposed fix states; the route field list stays with RWB-PLT-N001-CON. |

### RWB-S4-E2025-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14944 | RWB-PLT-N001-CON | GAP-1898 |  | Keep the plan lists unchanged. Build against the five fakes at Day 1. When the platform stories and the two rwb-case contracts publish, add the five H rows and two C rows, re-run the dependency check and replace each fake. |

### RWB-P7-E2028-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14946 | RWB-PLT-N001-CON | GAP-1295 |  | Read H as None plus the six platform contracts the DP table names. Read C as RWB-P10-E2028-CON plus C RWB-P3-E1043-CON and the published P3 case-read and P4 authorise contracts. Platform contracts are delivery prerequisites, not per-story blockers; story stays Day 1. |

### OTHER:RWB-P10 agent monitoring v2 contract story and the rwb-decision contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14947 | RWB-PLT-N001-CON | GAP-0630 |  | Fix seven added v2 member names with four-decimal rule under additive major version 1. Keep paging and held-date status of RWB-P10-E1063-CON. Name drift inputs after watch_measures members. Add agent-version filter and three decision record elements as additive rwb-decision change. Name notice path by its owner. Register the route under RWB-PLT-N001-CON. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14949 | RWB-PLT-N001-CON | GAP-2412 |  | Publish the placement fact element names, key and CloudEvents envelope on rwb.decision-record.v1. Publish P3 case-read and P4 authorise shapes and the reference-data operation in their own CON stories at wave 2 entry. Add MSG-P7-009 text to the message standard. Fix the login name and secret store entry in the platform DB story. Carry the seven H rows and two C rows in the Dependency Map. |

### OTHER:Work Package plan slice RWB-S5-E3026 (split_plan) and the S5 module model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14950 | RWB-PLT-N001-CON | GAP-2869 |  | Build on Day 1 against owner documents and fakes. Name RWB-PLT-E1071-CON as the wave 0 library for the Schedule without rewriting the H row. Declare the valuation order as consumed from rwb-valuation with placeholder. Keep the three rule inputs as decision record inputs. Trace both slices to REQ-S5-003. Leave AC3 end-to-end evidence to the wave 2 harness. |

### RWB-P8-E4043-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14951 | RWB-PLT-N001-CON | GAP-2548 |  | Allocate a service contract baseline publishing rwb.payment.TreatmentBooked.v1 in BACKWARD mode, the deliverFile manifest element set with the booking branch, the error envelope and fakes. Publish ALS interface row values as reference data and the data product code in TSD P8 appendix T-A. |

### RWB-S6-E6008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14952 | RWB-PLT-N001-CON | GAP-3006 |  | Keep H, C, I and X rows as they stand. Record the four reads and interface call as class C in fact with placeholders. Carry posting result, item reference and rejection code in decision record and case state with no new column. Run posting under service identity. Hold month-end close as a durable timer of DebtSaleWorkflow. Adopt REQ-S6-008. |

### RWB-S7-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14953 | RWB-PLT-N001-CON | GAP-3025 |  | Keep H, C, I and X rows as they stand. Record rwb-case, rwb-deviation and rwb-decision rows as class C in fact with placeholders. Track RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and a meeting-calendar element as tracked dependencies. Declare no REST operation provided. Add a requirement row for the routing step at next programme revision. |

### RWB-S7-E6021-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14954 | RWB-PLT-N001-CON | GAP-3033 |  | Record the four consumed rows as class C, treat DP-05 as consumed on rwb-source-data's contract, keep ALS/GL crossing with RWB-ITG-E6021-ITG, and add REQ-S7-002 and REQ-S7-005 to traceability at D1. |

### RWB-S7-E6025-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14955 | RWB-PLT-N001-CON | GAP-3041 |  | Add class C rows for rwb-case and rwb-decision, record RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON as tracked dependencies, and publish the retention reference data with a placeholder. |

### RWB-S8-E7001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14956 | RWB-PLT-N001-CON | GAP-3051 |  | Record rwb-document and rwb-source-data reads as class C with placeholders; adopt DeviationRaised and DeviationCleared as EV-06 and EV-07 on rwb.deviation.events.v1. |

### RWB-S8-E7002-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14957 | RWB-PLT-N001-CON | GAP-3053 |  | Record the four consumed rows as class C, add RWB-PLT-TE006-CON and RWB-PLT-E1072-CON with RWB-P7-E1073-CON, and adopt REQ-S8-002, REQ-DVH-005 and REQ-S8-004. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14958 | RWB-PLT-N001-CON | GAP-3055 |  | Record rwb-source-data, rwb-case, rwb-access and rwb-decision rows as class C; track RWB-PLT-TE006-CON and RWB-PLT-E1071-CON as dependencies; settle the S8-to-P7 edge. |

### RWB-S8-E7004-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14959 | RWB-PLT-N001-CON | GAP-3057 |  | Record the consumed rows as class C; add RWB-PLT-E1072-CON with RWB-P7-E1073-CON, RWB-PLT-TE006-CON and RWB-PLT-E1037-CON with RWB-P4-E1037-CON; publish the deviation state list. |

### OTHER:Metadata rows of the X5 deviation slice in the S8 story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14960 | RWB-PLT-N001-CON | GAP-3059 |  | Carry the claim deadline, SLA and Legal route as versioned reference rows with placeholders; declare Case record U; trace both slices to FEAT-DVF-05. |

### RWB-S8-E7006-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14961 | RWB-PLT-N001-CON | GAP-3061 |  | Declare the four consumed rows as class C with placeholders and fakes; record the absent DP-05, DP-09, DP-14 and DP-20 rows in the registers. |

### RWB-S9-E7015-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14962 | RWB-PLT-N001-CON | GAP-3129 |  | Publish a contract-end operation or confirm a workflow command; decide whether recall publishes an event; define open; publish the case-side re-selection command and the partner_user field list. |

### OTHER:P10 agent-step contract story (TSD P10 v2 T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14964 | RWB-PLT-N001-CON | GAP-2188 |  | Fix the JSON member names and spelling of ruleResult, inputs, confidence and the record reference; settle member types, refusal set and record reference shape with the rwb-decision and rwb-case owners. |

### OTHER:Work Package B2-P7-007 metadata and Template and Rules v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14965 | RWB-PLT-N001-CON | GAP-2419 | Header | Add the seven platform contracts and RWB-P3-E1043-CON as wave 0 build and contract fakes; add the authorise answer of rwb-access to the platform guard for the two reads. |

### OTHER:rwb-agent contract (P10 rwb-agent) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14966 | RWB-PLT-N001-CON | GAP-0072 | Header | Build the tool gateway inside rwb-agent as one outbound client holding the workload identity, calling the owner's REST contract in one hop with a 2 s limit, writing every call to the run row. |

### OTHER:rwb-access API and RWB-E8-014 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14968 | RWB-PLT-N001-CON | GAP-2288 | Header | Define the access pack, its three check codes PC-ENT, PC-SCP and PC-MSK, the two pack-check operations, the verdict set ACCEPTED and RETURNED, and the decided-version 409 rule. |

### OTHER:P4 access story carrying the matrix (legacy RWB-E8-019) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14969 | RWB-PLT-N001-CON | GAP-2304 |  | Keep the matrix as permission rows stamped with a matrix version, minted and superseded by one set. Read the right from TSD P4 v3 T6.1 and API-P4-007. Carry an agent reference on the grant. |

### OTHER:P4 admin access story (legacy RWB-E8-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14970 | RWB-PLT-N001-CON | GAP-0867 |  | Add GET /api/recovery/access/v1/admin/home returning AdminHome with area rows, matrixVersion, maskingVersion, listVersion, roleClass, chain and recordedAt. Hold cache TTL in parameter access.home.cache.ttl.seconds read through DP-06. |

### RWB-P4-E8013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14971 | RWB-PLT-N001-CON | GAP-0873 |  | Freeze the two paths and three schemas. Add the P7 contract dependency to metadata at the next revision. Fix the draw rule and reason codes as rwb-case parameter rows. |

### OTHER:P6 communications notice story (legacy RWB-E4-040) and P5 custody contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14977 | RWB-PLT-N001-CON | GAP-1156 |  | Make document and document_custody P5 rwb_document rows. rwb-comms declares no custody table and keeps only the movement identifier on its notice, recorded through the P5 custody operation with a 2 s budget. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-P4-E8015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14981 | RWB-PLT-N001-CON | GAP-2296 | header | Add a JOB-nn row for the daily rwb-access chain check; add RWB-PLT-E1071-CON to the H list of RWB-P4-E8015-APP in the Dependency Map and the plan. |

### RWB-S6-E5025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14982 | RWB-PLT-N001-CON | GAP-3014 | header | Keep H, C, I and X as stated; carry the six consumed rows in 12.2 with placeholders and fakes in 12.8; record the PII service as unmapped; hold tape reference, checksum and check result in the decision record; trace REQ-S6-003. |

### RWB-S6-E6007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14983 | RWB-PLT-N001-CON | GAP-3004 | header | Add six consumed rows (rwb-case, rwb-partner, rwb-access, rwb-decision, rwb-integration); add DP-09 outbox row with RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON as dependencies; record the transfer on lot status and the decision record. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14984 | RWB-PLT-N001-CON | GAP-0807 | header | Add RWB-PLT-E1071-CON to the build list and DP-10 to the pattern row; fix the cron as deployment configuration under the DL38 placeholder until the IAM value is supplied; create the Schedule in the operations story. |

### RWB-S7-E6015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14985 | RWB-PLT-N001-CON | GAP-3021 | header | Add seven consumed rows as class C; add RWB-P10-TE013-CON (agent client), RWB-PLT-TE006-CON, RWB-PLT-E1072-CON with RWB-P7-E1073-CON; adopt REQ-S7-002; correct the TSD T8 row. |

### RWB-S7-E6013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14986 | RWB-PLT-N001-CON | GAP-3016 | header | Add four consumed rows (rwb-case, rwb-source-data, rwb-decision); add RWB-PLT-E1072-CON with RWB-P7-E1073-CON, RWB-PLT-TE006-CON and RWB-PLT-E1071-CON; declare the JOB-16 Schedule and ACE trigger. |

### RWB-S6-E5023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14987 | RWB-PLT-N001-CON | GAP-2973 | header | Add four consumed rows as class C; add RWB-PLT-TE006-CON and RWB-PLT-E1072-CON with RWB-P7-E1073-CON; declare deviation_open and fraud_flag as rule inputs with placeholders; adopt REQ-S6-001. |

### RWB-S6-E6011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14988 | RWB-PLT-N001-CON | GAP-3012 | header | Add six consumed rows as C dependencies; track RWB-PLT-TE006-CON, the rule kit, the settlement stamp and FEAT-DBS-12; reconcile FSD and TSD module sources. |

### RWB-S7-E6016-APP; OTHER:T3.1; OTHER:T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14989 | RWB-PLT-N001-CON | GAP-3023 |  | Add the removal operation placeholder to the write-off base, declare removal_reason as free-text validated and stored in the decision record, record RWB-PLT-TE006-CON and RWB-PLT-E1072-CON with RWB-P7-E1073-CON as rows. |

### OTHER:RWB-S6-E5023 story file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14991 | RWB-PLT-N001-CON | GAP-1947 |  | Declare the four consumed rows in 12.2 with the operation placeholder and fakes, add DP-04 rows, keep plan metadata, trace REQ-S6-001 from the FSD. |

### RWB-S6-E5024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14992 | RWB-PLT-N001-CON | GAP-2975 |  | Record four consumed rows as class C with placeholders, add RWB-P10-TE013-CON and RWB-PLT-TE006-CON rows, record rule values as placeholder rows, keep R-DS-04 criterion split, adopt REQ-S6-002. |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14993 | RWB-PLT-N001-CON | GAP-3037 |  | Fix posting product and event on the rwb-source-data contract, publish matching cross-reference, hold three consumed rows as class C, record no provided operation or Schedule, trace REQ-S7-005 placeholder. |

### OTHER:FSD S2 REQ-S2-009 and the two S2 treatment story files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14994 | RWB-PLT-N001-CON | GAP-2669 |  | Confirm the BREAK_RECORDED stage report as the event, or allocate rwb.treatment.PlanBroken.v1 with payload, consumers, DP-09 rows and outbox row. |

### RWB-S5-E3019-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14995 | RWB-PLT-N001-CON | GAP-2837 |  | Keep H, C, I, X rows; record rwb-source-data and rwb-case as C with placeholders; add RWB-PLT-TE006-CON; add asset row to Ownership Map; adopt REQ-S5-001. |

### OTHER:RWB-S5-E3021 story files (APP and CON) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14996 | RWB-PLT-N001-CON | GAP-2847 |  | Keep H, C, I, X rows as stated; declare consumed AuctionResult event and three REST rows as facts with fakes; record RWB-PLT-TE006-CON as wave 0 library. |

### RWB-S6-E6004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14997 | RWB-PLT-N001-CON | GAP-2988 |  | Record five consumed rows as class C with placeholders, add RWB-PLT-TE006-CON, fix API-S6-005 as this key's operation, hold bid columns until added, assign one writer per rule. |

### RWB-S7-E6018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14998 | RWB-PLT-N001-CON | GAP-3027 |  | Record five consumed rows as class C with placeholders, read delegation_limit as reference data, keep approver and limit in local decision record, claim EV-24, add RWB-PLT-TE006-CON. |

### RWB-S1-E4007-APP; OTHER:H row and ready-to-start value (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14999 | RWB-PLT-N001-CON | GAP-2624 | n/a | Add RWB-S1-E4005-APP and RWB-S1-E4006-APP to the H row of RWB-S1-E4007-APP; set ready-to-start to 'After RWB-S1-E4005-APP, RWB-S1-E4006-APP'. No behaviour or contract change. |

### OTHER:split_plan.json WP B2-S4-008 story lines (APP and CON) and the RWB-S4-E5008 story files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15000 | RWB-PLT-N001-CON | GAP-2773 | n/a | Name the rwb-partner panel and instruction reads and the rwb-case case-move answer as consumed rows; build on published documents and fakes with a 2 s budget and a breaker; D1 decides on a C row. |

### OTHER:Story files of the two consuming stories (section 12.2) and split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15001 | RWB-PLT-N001-CON | GAP-2829 | n/a | Declare the rwb-case read, case answer and queue/task request, and the rwb-decision rule package read as consumed rows in 12.2; keep metadata rows as planned; add C rows only when owners publish operation names. |

### RWB-S5-E3024-APP; OTHER:TSD S5; API:(service not named); OTHER:rwb-access matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15002 | RWB-PLT-N001-CON | GAP-2860 | n/a | Define the stock balance as asset-row counts plus book_value and holding_cost_to_date totals per holding_status, for LOV-SEGMENT and an as-at date, served on GET /assets as AssetStockBalance; confirm with one POST on the asset base; owner RW-NPAMGR. |

### RWB-S5-E3019-APP; RWB-S5-E3019-CON; OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15003 | RWB-PLT-N001-CON | GAP-1906 | n/a | Keep the plan H, C, I and X rows; record rwb-source-data, rwb-case and DP-09 as needed dependencies; declare AssetTakenOn from the outbox; read the case move as a workflow stage outcome; read REQ-S5-001 with a note that the plan carries no requirement id. |

### RWB-S6-E5024-APP; OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15004 | RWB-PLT-N001-CON | GAP-1952 | n/a | Keep the plan H, C, I and X rows; record rwb-source-data, rwb-agent, rwb-case and rwb-decision as class C dependencies; fake each on Day 1; keep DP-04 and DP-09 rows in this register. |

### RWB-S6-E5026-APP; OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15005 | RWB-PLT-N001-CON | GAP-2977 | n/a | Keep plan H, C, I and X rows; record rwb-document, rwb-partner and rwb-case as class C rows with fakes; record the partner channel as an edge dependency; adopt REQ-S6-003 and FEAT-DBS-04. |

### RWB-S6-E5026-CON; OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15006 | RWB-PLT-N001-CON | GAP-1958 | n/a | Declare the rwb-document tape read, rwb-partner panel read and case-move answer as class C dependencies; build on published documents and fakes on Day 1; keep the C row as planned; trace REQ-S6-003. |

### RWB-S6-E6002-APP; OTHER:TSD S6; OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15007 | RWB-PLT-N001-CON | GAP-2984 | n/a | Keep plan H, C, I and X rows; declare rwb-partner as class C with placeholder name and 2 s budget; package as an activity on rwb-decision; bid recorded as a decision record; raise bid table for the DB story; adopt REQ-S6-004. |

### RWB-S6-E6003-APP; OTHER:TSD S6; OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15008 | RWB-PLT-N001-CON | GAP-2986 | n/a | Keep plan H row; build on six contract fakes with 2 s budget and breaker; declare no provided operation; carry three placeholders in the text; delegate re-offer to R-DS-28 at RWB-S6-E6005-APP; record wave conflict once. |

### RWB-S6-E6009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15009 | RWB-PLT-N001-CON | GAP-3008 |  | Declare no provided claim operation and reach the step through the lot and data room reads. Read the claim window as a versioned parameter. Hold realized recovery on account selling_price and the closed lot. |

### RWB-S6-E6001-APP; RWB-S6-E6001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15010 | RWB-PLT-N001-CON | GAP-1963 | not in chunk | Add five C rows (P7 approval chain, P7 rule-package read, P4 delegation_limit, P3 case state read, P3 case-move answer) and the rwb-decision queue dependency to the dependency map. Keep placeholders for unnamed operations. |

### RWB-S6-E6002-APP; RWB-S6-E6002-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15011 | RWB-PLT-N001-CON | GAP-1969 | not in chunk | Add class C rows for rwb-partner, rwb-case, rwb-decision and rwb-access in the text and registers. Name REQ-S6-004 as the requirement. Confirm the three operation names with their owners before the baseline tag. |

### RWB-S6-E6005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15012 | RWB-PLT-N001-CON | GAP-2990 | not in chunk | Declare the six consumed rows in 12.2 with owners, budget and placeholders for the three unnamed operations, and fake them for the build. Keep the metadata C row as the plan states it. |

### RWB-S6-E6010-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15013 | RWB-PLT-N001-CON | GAP-3010 | not in chunk | Record the rwb-case, rwb-access and rwb-decision rows as class C with placeholders. Declare no provided operation and name API-S6-003 of RWB-S6-E6005-APP as the start signal. Record the open-action set as an assumption. Run the unattended step under the rwb-debtsale service identity. |

### OTHER:RWB-S6-E6006 story and split plan key (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15014 | RWB-PLT-N001-CON | GAP-2996 | not in chunk | Declare the six consumed rows in 12.2 with placeholders and in 12.8 with fakes. Add the C rows of P5, P6, P1, P3 and P7 to the key. |

### RWB-S7-E6022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15015 | RWB-PLT-N001-CON | GAP-3035 | not in chunk | Record the four reads and the Finance provision feed call as class C with placeholders. Declare no provided operation and name API-S7-001 and API-S7-002 as the scan and committee decision. Add no column to the DB story. |

### RWB-S7-E6024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15016 | RWB-PLT-N001-CON | GAP-3039 | not in chunk | Add the correction operation on the write-off base with a placeholder path and elements. Read the retry count and limit from the posting step and the WO package. Carry R-WO-41 and R-WO-43 as the other two entries. |

### RWB-S7-E6027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15017 | RWB-PLT-N001-CON | GAP-3046 | not in chunk | Declare the act event-driven with no operation of its own. Consume the P8 event on rwb.payment.events.v1 with a placeholder name and payload. Post the income through postProceeds on the P8 queue. Keep the plan's H, C, I and X rows. |

### RWB-PLT-E1072-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15018 | RWB-PLT-N001-CON | GAP-0822 | - | Record that rwb-access embeds no Drools kit and carries no DP-04; compile, checks and SIT scenario run stay in rwb-decision, which returns the result to rwb-access. |

### OTHER:Edge design review record and ACE front-end push transport record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15019 | RWB-PLT-N001-CON | GAP-1394 | - | Fix gateway-bff pod topology, resource limits, pools, screen-model field list and sizing with platform team and RWB-PLT-N006-INF; record the inbox push transport with ACE front-end team before first integration test. |

### RWB-PLT-NF02-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15020 | RWB-PLT-N001-CON | GAP-1400 | - | Fix helper package, registry and version label; error-map path at library resource root; expiry window and store timeout as chart configuration with platform default; owning service stamps instance, edge passes code and detail through. |

### OTHER:Technical Specifications by Module v6 (T0 Service section) or a PLT module file in the FSD set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15021 | RWB-PLT-N001-CON | GAP-1664 | - | Write the platform functional specification and map FR-PLT-001 to FR-PLT-034 to the FSD requirement IDs of the dependent modules and the BRD NFR targets. |

### OTHER:Platform design record and the route surface of this story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15023 | RWB-PLT-N001-CON | GAP-1436 | - | Serve the dictionary from the rwb-case reference-data contract over rwb_source_data sys_fields; generate the rule set once and inherit it through the template; record dictionary and rule-set versions in the build record; resolve the allow-list approver as the code-owner role via the authorise contract; publish the release quality view as a gateway-bff composite route. |

### API:(service not named); OTHER:S1 API file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15024 | RWB-PLT-N001-CON | GAP-2602 | - | Publish the outlier element as an additive optional element of Approval under a draft name, with typed and nullable nested elements; the API owner may rename it at the tag while no consumer is released. |

### OTHER:Build plan H row for RWB-S6-E5026 and ownership.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15025 | RWB-PLT-N001-CON | GAP-1959 | - | Declare GET /partner/data-room/{lotId} as one Partner portal operation of rwb-debtsale, with the partner gateway and the rwb-partner panel as its route; keep PT-BUYER RU on the partner channel and Partner portal R for staff roles. |

### RWB-P1-AD018-APP; RWB-P1-AD018-CON; RWB-P1-AD018-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15027 | RWB-PLT-N001-CON | GAP-0516 | - | Assign the SCR-44 reads to the APP story, their publication to the CON story, and the gateway-bff route and its alerts to the OPS story. |

### RWB-P3-E1052-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15028 | RWB-PLT-N001-CON | GAP-0754 | header | Hold platform contract dependencies RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON in the DP pattern table and preconditions; keep metadata rows as the work package gives them. |

### RWB-P6-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15030 | RWB-PLT-N001-CON | GAP-1212 |  | Add the eight DP-added dependency rows to the H and C lists, or record the wave-0 platform baseline and the P3 contract fakes as ASM-B-P6-05-E1063-3 sets out. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15031 | RWB-PLT-N001-CON | GAP-1053 |  | Record the DEV storage account, the DEV container names, the rwb-document login and the DEV read-only role. The SCR-30 and SCR-31 composite route is to be published with RWB-PLT-N001-CON. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15032 | RWB-PLT-N001-CON | GAP-1218 |  | Either add the eight platform CONs (DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15, DP-19) to the story's H list, or state in the lane document that they are wave-0 prerequisites outside H. Keep Ready to start at Day 1. |

### OTHER:Platform DB story for rwb-access and the gateway-bff composite route specification for SCR-03 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15034 | RWB-PLT-N001-CON | GAP-0909 |  | Fix the rwb-access per-service login name in the platform DB story. Publish the SCR-03 composite route with its field list, merge order and DP-19 masking rule. |

### OTHER:Owning secondary-slice story (pattern table, sections 3; OTHER:12.2; OTHER:12.8 and 13) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15039 | RWB-PLT-N001-CON | GAP-2488 |  | Name every added H and C row in the pattern table and the 12.8 fakes. Build against the published contracts and fakes from Day 1, and let step D1 decide the dependency map entries. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15041 | RWB-PLT-N001-CON | GAP-2389 | 3 | Keep H empty. Add to the C list RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON at the next plan revision. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:DP-07; OTHER:DP-09; OTHER:DP-10; OTHER:DP-15 and DP-19 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15043 | RWB-PLT-N001-CON | GAP-1277 | 13 | Carry the six platform H rows, the C row RWB-P3-E1043-CON and the two service baselines as DP-added rows. Keep Ready to start Day 1. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:DP-06; OTHER:DP-07; OTHER:DP-09; OTHER:DP-10 and DP-19 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15045 | RWB-PLT-N001-CON | GAP-1286 | 13 | Carry the six platform H rows and the two rwb-case C rows RWB-P3-E1042-CON and RWB-P3-E1043-CON as DP-added. Keep Ready to start Day 1. |

### OTHER:Story B2-P4-021 and its Work Package line (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15047 | RWB-PLT-N001-CON | GAP-2312 |  | Carry the platform and rwb-case contracts of the DP table as build-against dependencies in section 13 of B2-P4-021 and confirm at the wave 2 gate; keep metadata rows as the WP fixes them. |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15048 | RWB-PLT-N001-CON | GAP-2410 |  | Record that the slice builds against platform contracts and published fakes and reads wave-1 rows through its own schema, within R5.7 rule 5. |

### RWB-P7-E2042-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15049 | RWB-PLT-N001-CON | GAP-1296 |  | Keep metadata as written; carry the eight platform H and three published C dependencies in the story as fakes-based build-against items. |

### OTHER:Affected story's section 13 and section 18 (DP application); OTHER:Work Package row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15050 | RWB-PLT-N001-CON | GAP-2398 |  | Carry the eleven added rows in the DP application of section 13 and 18 and leave the metadata rows as the Work Package fixes them. |

### RWB-P6-E5002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15052 | RWB-PLT-N001-CON | GAP-1190 |  | When the export is regenerated, add H RWB-PLT-E1027-CON and H RWB-PLT-N001-CON to the build list of RWB-P6-E5002-APP; keep the plan rows until then. |

### OTHER:Version 3 work order (window order) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15054 | RWB-PLT-N001-CON | GAP-3244 |  | Show wave 0 platform stories N001 to N012 and harness stories W1J01 to W4J01 as Day-1 work before window 1. |

### OTHER:RWB-E4-041 legacy story (notice feature) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15056 | RWB-PLT-N001-CON | GAP-1154 | none | Remove SCR-33, VR-P6-020-1, the two notice operations and the A2.20 measure from its key; withdrawn-template rule to rwb-comms template stories; Documents area with right R per TSD P6 T6.1. |

### RWB-P6-E4035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15057 | RWB-PLT-N001-CON | GAP-2368 | none | When planned, add the S2 and P1 contract stories to C and the S8 deviation event rows to I of the wave 3 integration story; keep the drift test until then. |

### OTHER:wp/B-P4-04.md and wp/B2-P4-010.md (split_plan.json) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15058 | RWB-PLT-N001-CON | GAP-2278 | none | Remove RWB-AD-016 from the B-P4-04 fanout so B2-P4-010 alone owns it; number CG and ASM IDs once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-S5-E4030-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15059 | RWB-PLT-N001-CON | GAP-2953 | none | Declare inbox and outbox as platform capabilities and the DISPOSAL package as loaded through the service template; add no H row this wave; raise the platform question at next plan revision. |

### RWB-S3-E4015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15060 | RWB-PLT-N001-CON | GAP-2716 | none | Add the P7 rwb-decision package row and the P3 rwb-case reference-data row at next plan revision, or declare both as template capabilities. |

### OTHER:split_plan.json (RWB-S4-E5011 slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15061 | RWB-PLT-N001-CON | GAP-2790 | none | Name the rwb-decision rule-package read and the rwb-case reference-data ride on the S4 contract rows; keep H, C and I as planned; DP-04, DP-06 and DP-07 rows added centrally on plan revision. |

### OTHER:Edge catalogue (RWB-PLT-EDGE) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15062 | RWB-PLT-N001-CON | GAP-1730 | 8 | Record the owner and the gateway-bff composite route of SCR-17 Guarantee claim over this contract and the case contract |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15063 | RWB-PLT-N001-CON | GAP-2891 | 8 | Reference-data owner confirms whether LOV-HOLDING gains an EVICTION_REQUIRED value or the eviction state stays an element of the asset answer |

### OTHER:Gap register (GAP-0775) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15086 | RWB-PLT-N006-INF | GAP-0775 | find it | Close GAP-0775 with the proposed fix: rwb-access resolves per call, ROLE_CONFLICT rides the refusal fact, team and region via RWB-P3-E1019-CON. |

### RWB-PLT-N006-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15087 | RWB-PLT-N006-INF | GAP-1394 | find it | Fix gateway-bff topology and screen-model field list; record inbox push transport with ACE front-end team; size gateway and Redis session store. |

### OTHER:Service Catalog and platform runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15088 | RWB-PLT-N006-INF | GAP-1392 | 9 | Record the Redis session store product, tier and memory, zone and region placement, availability target, absolute session lifetime, eviction policy, maximum concurrent sessions, persistence and backup choice, and RPO/RTO, as fixed at the platform infrastructure review before wave 0 exit. |

### RWB-S9-E6033-CON; RWB-S6-E5026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15090 | RWB-PLT-N007-INF | DOR-RWB-PLT-N007-INF-22 | header | Record the published fake library version for rwb-partner and rwb-debtsale. |

### OTHER:Security design decision for the partner gateway; OTHER:Service Catalog and gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15094 | RWB-PLT-N007-INF | GAP-1395 | 8 | Record DMZ zone design, gateway product and version, client authentication method, token lifetimes, external identity provider, certificate and revocation timings, rate limits, request size limit, WAF rule set and DR objectives. |

### RWB-PLT-N007-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15096 | RWB-PLT-N007-INF | GAP-0786 | 8 | Extend the certificate profile and rotation window to the rwb-access hop, record the per-client rate limit and burst for the resolution route, and publish the rwb-access namespace, service and port. |

### OTHER:New ADR recording the Airflow decision (not yet numbered) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15178 | RWB-PLT-NF07-INF | GAP-1673 | find it | Record the Airflow placement, the Control-M move date and DAG ownership in a new ADR that replaces the BRD's ADF and Control-M wording, and name the DAG owner before wave-1 release. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20783 | RWB-PLT-N001-CON | R-23213 |  | The outbound tool gateway is not a REST operation of this spec. It belongs in the P10 agent contract RWB-P10-TE013-CON. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0072 | The tool gateway is named by the source and given no owner | P10 rwb-agent | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0078 | The screen for a run and its gateway route have no owner row | Platform architect | Resolved (directive) |
| GAP-0094 | The gateway-bff composite screen routes are not specified in the API source | Solution architect | Resolved (directive) |
| GAP-0141 | The API Specification v4 paths are the monolith paths while the Service Catalog states the per-service base | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0385 | The wave 1 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0390 | Customer other-products harness pack: repository, environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0428 | The wave 2 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Resolved (directive) |
| GAP-0516 | SCR-44 is a gateway-bff route on a P1 story that builds no screen | DevOps lead | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0631 | The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified | Platform administrator | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0662 | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0693 | The gateway-bff composite route specification for SCR-03 is not given | Solution architect | Resolved (directive) |
| GAP-0728 | RWB-AD-019 in rwb-case: login name, edge composite route, source-data read shape and contract placement not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0773 | The gateway-bff composite route of the case record plan section is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0775 | The home of the resolved session labels, the target of the conflict incident and the team and region read behind the scope line are not specified for the sign-on app slice | rwb-access service owner with the architecture review | Resolved (directive) |
| GAP-0784 | The partner identity resolution operation, its claim set, its answer schema, the scope type PLACED and the lifetime of an answer are specified by no source | Solution architect, P4 rwb-access with the external gateway owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0786 | The certificate profile, the rotation and revocation of the rwb-access hop, the numeric rate limit and the namespace and service names of the DMZ hop are specified by no source | SCB IT infrastructure with the security design authority | Resolved (directive) |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0822 | rwb-access rule-version load: the compile, the checks and the SIT scenario run need the Drools kit RWB-PLT-E1072-CON, which is not in this story's build list | Solution architect | Resolved (directive) |
| GAP-0867 | The administration home operation, its fields, its parameter name, its entitlement rule and its record code are not in the sources | Tech lead | Resolved (directive) |
| GAP-0873 | The QA-sample operations, the missing P7 dependency, the draw rule and the reason-code set of RWB-E8-013 are not specified in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0879 | The incident operations, the step record code, the detection feed and the incident screen are not in the sources | Solution architect, with the platform administrator | Resolved (directive) |
| GAP-0909 | rwb-access plan status: the per-service login name and the gateway-bff composite route field list behind SCR-03 and the plan status panel are not specified | Solution architect | Resolved (directive) |
| GAP-0913 | The field list and the masking step of the gateway-bff composite route for the other-products panel are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0951 | Whether the field app reaches the authorise path through gateway-bff or directly is not specified | Solution architect, P4 with the gateway-bff route owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0955 | The authorise shape for a send and the field list of the composite route are not specified | Solution architect, P4 and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1035 | The SCR-30 route specification in the gateway-bff composite route is not specified | Solution architect, with the gateway-bff squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1083 | The scope and right check of the notice operations has no rwb-access dependency row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1154 | The legacy rows of RWB-E4-041 are carried over from notice generation | Business analyst | Resolved (directive) |
| GAP-1156 | document_custody is a P6 module table in the legacy story and a P5 rwb-document table in the target, and the P5 custody contract has no C row and no contract story | solution architect with the P5 rwb-document owner | Resolved (directive) |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1258 | The field-level list and the mask flags of the D7.1 approval screen are published by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1259 | The composite-route name and path segment of the approval screen are not specified | Solution architect | Resolved (directive) |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1267 | The legacy screen states and the platform route states are two unreconciled vocabularies | Business analyst | Resolved (directive) |
| GAP-1270 | The timeout budget of a screen that composes three reads is not specified | Solution architect | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1312 | The DP table adds two platform contracts and the story consumes three operations that its metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1349 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1392 | Redis session store product, tier, placement, availability target, session lifetime, eviction, capacity, persistence and RPO/RTO are not specified | SCB IT infrastructure lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1393 | gateway-bff public path table, inbox push transport and payment-tab operation are not stated by any source | Solution architect | Resolved (directive) |
| GAP-1394 | gateway-bff deployment topology, screen-model schema, inbox push transport and gateway sizing are not stated by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1395 | DMZ network design, gateway product, FAPI 2.0 settings, external identity provider, certificate lifecycle, rate limits, WAF rule set and DR target of the partner gateway are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1396 | Airflow product, tenancy, DAG names, identity method, timeout and retry values, the DailyCaseRun wait contract and the file-window operation are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1400 | The artefact coordinates of the helper, the error-map source, the header format and the ordering with the edge are not specified for the implementation | Platform library lead with the platform architect | Resolved (directive) |
| GAP-1430 | The per-service module-map file name and the gateway-bff composite route list are not specified | Solution architect | Resolved (directive) |
| GAP-1436 | One rule set, one pinned dictionary version, its read path and the allow-list approver after the marks became reference data | Solution architect | Resolved (directive) |
| GAP-1664 | No FSD module exists for the platform, so no FSD requirement ID states a platform capability | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1673 | The Airflow ownership, its placement and the date Control-M moves are open | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1676 | The partner gateway provision and its penetration-test scope are open | SCB IT security | Accepted (directive); not applied: value not in the source documents |
| GAP-1730 | No source fixes the screen ownership or the gateway route of SCR-17 | Solution architect | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1906 | RWB-S5-E3019: the take-on slice has no source for its dependency rows, its event, its case move, its requirement id and the duplicated R-DIS-06 criterion | Solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1947 | RWB-S6-E5023: the eligibility slice has no C row for its four consumed rows, no DP-04 row and no requirement id | Solution architect | Resolved (directive) |
| GAP-1952 | RWB-S6-E5024: the lot build and price step needs rwb-source-data, rwb-agent, rwb-case and rwb-decision while the plan's C row is empty | Solution architect | Resolved (directive) |
| GAP-1958 | RWB-S6-E5026: the data-room slice carries an empty C row although it needs rwb-document, rwb-partner and rwb-case, and the plan holds no requirement id | Solution architect | Resolved (directive) |
| GAP-1959 | RWB-S6-E5026: the partner channel of the data-room read has no plan row and the right is stated twice with different holders | Solution architect | Resolved (directive) |
| GAP-1963 | RWB-S6-E6001: the plan gives this step an empty C row while it consumes rwb-decision, rwb-access and rwb-case, and two of the consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1969 | RWB-S6-E6002: the qualification slice has no C row, no requirement id and no case-move or authorise operation although it needs rwb-partner, rwb-case, rwb-decision and rwb-access | Solution architect | Resolved (directive) |
| GAP-1986 | gateway-bff and the partner gateway have no owner code, no wave and no service row | Platform team | Resolved (directive) |
| GAP-2099 | The shared edge has no owner row: gateway-bff, the Redis session and the App Gateway route | Platform architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2188 | The client contract has no source member types, refusal detail or record reference shape | Solution architect | Resolved (directive) |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2281 | The panel-change operation, its fields, the table code, the record code, the compensation, the screen and two owner contracts are not in the sources | Tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2288 | The pack, its three check codes, the two operations, the five schemas, the parameter rows, the decided-version rule and the record code are not in the sources | Tech lead of rwb-access | Resolved (directive) |
| GAP-2296 | The daily chain check has no job row in the Batch and Scheduling Design and the workflow kit dependency is absent from the Work Package | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2301 | The incident record, its three operations, its record code and its right are not in the sources, and the legacy permission table conflicts with the technical specification | Solution architect | Resolved (directive) |
| GAP-2304 | The access-change record code, the matrix version label, the matrix screen, the agent identity source and the grant's service event are not in the sources, and two sources disagree on the group column of a role and on the right of the path | Solution architect | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2363 | The legacy screen, endpoints and rights of RWB-E4-035 serve an officer's notice screen, not a customer's offer view | Solution architect | Resolved (directive) |
| GAP-2367 | No source gives the capability area or the right of an offer-view operation, and the legacy story names the Litigation rights of another surface | Solution architect | Resolved (directive) |
| GAP-2368 | The two contracts and the contact-stop events the view depends on carry no C row and no source shape in this key's plan | Solution architect | Resolved (directive) |
| GAP-2379 | No source names a screen for the contact repository and the legacy screen is the template screen | Business analyst | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2533 | rwb-payment cutover load of RWB-DM-013: the handover file, the load command and its run record, a provenance column, the legacy payment_code column and the two schema-level H rows are fixed by no single source, and this slice owns no legacy criterion | Data steward and solution architect of rwb-payment, with the rwb-source-data owner, the schema baseline owner and the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2602 | The outlier element of the route answer is in no published schema, and the approved answer carries only the approval elements | Solution architect of S1 with the owner of the edge contract (RWB-PLT-N001) and the API owner | Resolved (directive) |
| GAP-2624 | FEAT-VAL-05 and FEAT-VAL-06 are prerequisites of the feature but their stories are not in the build dependency row | S1 rwb-valuation service owner with the delivery lead of wave 3 | Resolved (directive) |
| GAP-2669 | REQ-S2-009 says a broken plan raises an event, and the ownership rows and the plan give this legacy key no event to raise | Solution architect with the owner of the Kafka event platform and the business analyst of module S2 | Resolved (directive) |
| GAP-2716 | The GUARANTEE rule package and the two claim lists are consumed with no dependency row in this slice | P7 rwb-decision owner with the P3 rwb-case owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2760 | Three consumed contracts of the pack-recovery step have no dependency row, and the plan gives the two stories no contract or integration dependency | Solution architect, S4 rwb-litigation, with the P5 rwb-document and P3 rwb-case architects | Resolved (directive) |
| GAP-2773 | The panel read, the decline read and the case-move answer are consumed by both stories, have no contract story in the plan and no C row | Solution architect | Resolved (directive) |
| GAP-2790 | The rule package read and the reference values carry no dependency row, and DP-04, DP-06 and DP-07 are outside the pattern set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision and P3 rwb-case architects | Resolved (directive) |
| GAP-2797 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | P7 rwb-decision architect with the solution architect of S4 | Resolved (directive) |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2829 | Three consumed owner contracts of the deferral step have no dependency row, and the plan gives both stories no contract or integration dependency | Solution architect with the P3 and P7 owners | Resolved (directive) |
| GAP-2832 | SCR-20 carries no deferred state and no source gives a screen field list for the reason and the review date | Solution architect with the edge owner and the business analyst of EP05 | Resolved (directive) |
| GAP-2837 | RWB-S5-E3019-APP: the take-on slice has no plan row for its cross-service reads, its outbox library, its requirement id or the duplicated R-DIS-06 criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2847 | RWB-S5-E3021: the take-on step consumes and publishes an event and reads four owner contracts, while the plan carries no C or I row and its pattern set omits DP-09 | Solution architect | Resolved (directive) |
| GAP-2860 | RWB-S5-E3024-APP: the stock balance has no figure definition, no write operation for its confirmation, no object in the TSD, no requirement id, and its two take-on rules are owned by sibling stories | Business analyst S5 with the solution architect and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2869 | RWB-S5-E3026: the cycle slice has no planned dependency row for its four consumed contracts or its Schedule library, and neither the plan nor the module model holds the re-appraisal record, the requirement id or the AC3 evidence | Solution architect | Resolved (directive) |
| GAP-2891 | The legacy screen list gives SCR-22 four states and names no eviction state, and no source names the state the screen shows | S5 rwb-asset service owner with the screen designer of the gateway-bff composite route | Resolved (directive) |
| GAP-2952 | The legacy screen states of SCR-22 do not match the holding lists and the states this step produces are case states | S5 rwb-asset service owner with the screen owner of RWB-PLT-N001 and the case owner of P3 | Resolved (directive) |
| GAP-2953 | The slice consumes an event and evaluates a rule package, while DP-09 and DP-04 are outside its pattern set and no platform build row is carried | S5 rwb-asset service owner with the platform event and workflow owners | Resolved (directive) |
| GAP-2973 | RWB-S6-E5023-APP: the eligibility slice has no plan row for its four consumed contracts, its outbox library, its rule kit, the 54 percent cap criterion or the two eligibility inputs | Solution architect | Resolved (directive) |
| GAP-2975 | RWB-S6-E5024-APP: the lot build and price slice has no plan row for its four consumed contracts, its agent contract, the R-DS-04 criterion split, the rules that carry no value or the outbox library | Solution architect | Resolved (directive) |
| GAP-2977 | RWB-S6-E5026-APP: the data-room slice has no plan row for its three consumed contracts, its partner channel or the lot status of the opening | Solution architect | Resolved (directive) |
| GAP-2984 | RWB-S6-E6002-APP: the qualification step has no operation, no bid table, no published names for the buyer read, the case move and the package, and no partner arrow in the connection matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2986 | RWB-S6-E6003-APP: the bar slice has no plan row for its six consumed contracts, no published bar operation, no panel or lot-status vocabulary, no next-bidder field and no window row | Solution architect with the owners of rwb-partner, rwb-case, rwb-access and rwb-decision | Resolved (directive) |
| GAP-2988 | RWB-S6-E6004-APP: the take-bids slice has no plan row for its five consumed contracts, its guard and outbox libraries, the publish-first story of API-S6-005, the bid and realised-recovery columns, the two rules it shares with sibling keys, the reporting destination of R-DS-34, its wave or its requirement id | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2990 | RWB-S6-E6005: the award step carries an empty C row although it consumes rwb-case, rwb-decision, rwb-access and rwb-source-data, and three consumed operations have no published name | Solution architect | Resolved (directive) |
| GAP-2996 | RWB-S6-E6006: the agreement-and-notices step carries an empty C row although it consumes rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision, and five consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3006 | RWB-S6-E6008-APP: the derecognition and posting slice has no plan row for its four consumed contracts and its interface call, no posting column, no published operation names and no requirement id | Solution architect | Resolved (directive) |
| GAP-3008 | RWB-S6-E6009-APP: the put-back review has no published operation, its claim window, claim reason and realized-recovery figure have no field, column or event, its consumed contracts have no plan row, and two of its four criteria execute rules owned by sibling stories | Solution architect | Resolved (directive) |
| GAP-3010 | RWB-S6-E6010-APP: the closure slice has no plan row for its four consumed contracts, no published closure operation, an open-action set no source enumerates, no right for an unattended step and an ALS and GL integration point it does not own | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3012 | RWB-S6-E6011-APP: the settle-and-cancel slice has no plan row for its six consumed contracts, its inbox library, its rule kit, its settlement stamp, its GL prerequisite or its EP06 wave | Solution architect | Resolved (directive) |
| GAP-3014 | RWB-S6-E5025: the masking rule set, the tape layout, the tape's storage reference, the PII service mapping and the six consumed contracts are given by no source and sit outside the plan's empty C row | Solution architect | Resolved (directive) |
| GAP-3016 | RWB-S7-E6013-APP: the scan slice has no plan row for its four consumed contracts, its rule kit, its ACE read, its inbox and its schedule, and no table or list of values holds the scan | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3021 | RWB-S7-E6015-APP: the pack slice has no plan row for its seven consumed contracts, its agent, outbox and rule-kit dependencies, its pack columns, its requirement id or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3023 | RWB-S7-E6016-APP: the removal slice has no published operation, no field or list for the removal reason, no plan row for its three consumed contracts, and no requirement id | Solution architect | Resolved (directive) |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3027 | RWB-S7-E6018-APP: the delegation table and its owner, the approver and the limit applied have no column, the credit committee outcome is claimed by no story, and the plan's C row is empty while five rows are consumed | Solution architect | Resolved (directive) |
| GAP-3033 | RWB-S7-E6021-APP: the plan holds no C or X row for the four consumed contracts of the pack-prepared step, no dependency row for DP-05, no interface for the ALS and general-ledger crossing, and no separate story for the shared pack rule R-WO-05 | Solution architect with the rwb-writeoff tech lead, the rwb-source-data, rwb-case and rwb-decision owners and the wave 4 integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3035 | RWB-S7-E6022-APP: the Finance feed slice provides no operation while four consumed surfaces and one external feed have no plan row, no column carries the feed result, and the feed transport, layouts and codes are unpublished | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3037 | RWB-S7-E6023-APP: the reconciliation step has no published operation, no posting-product operation or event name, no matching cross-reference, no plan C row for its three consumed services, no job or Schedule for its monthly trigger and no requirement row | Solution architect | Resolved (directive) |
| GAP-3039 | RWB-S7-E6024-APP: no source publishes the correction operation or its elements, the loop's owner and time limit that REQ-S7-004 requires are unconfirmed, the retry count has no column, the other two entries to WRITEOFF_EXCEPTION have no feature, and SCR-27 has no exception state | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3041 | RWB-S7-E6025-APP: the closure slice has no plan row for its five consumed contracts, its rule kit, its event library, its scheduler marker, the retention period, the placement record or the closing amounts | Solution architect | Resolved (directive) |
| GAP-3046 | RWB-S7-E6027-APP: the post charge-off recovery has no REST operation, no published event name, no fee column and no screen state, and the plan's C row is empty while two rows and one event are consumed | Solution architect | Resolved (directive) |
| GAP-3051 | RWB-S8-E7001-APP: the X1 slice has no plan row for its two cross-service reads, no event names, no complaint service level and no published case-clock boundary, and its happy path has no acceptance criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3053 | RWB-S8-E7002-APP: the X2 slice has no plan row for its four consumed contracts, its outbox library, its EFS touch, its requirement ids, its work-management owners or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3055 | RWB-S8-E7003-APP: the X3 branch has no plan row for its four consumed contracts, its rule read, its outbox and its workflow, and no source names the claim reference, the heir notification or the escalation level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3059 | Seven values of the X5 deviation have no source: the claim deadline, the Legal handler route, the case contract and its two event families, the platform outbox, the legal counsel's right, the requirement identifier and the sign-off | Solution architect | Resolved (directive) |
| GAP-3061 | RWB-S8-E7006-APP: the X6 slice has no plan row for its consumed contracts, its skip-trace sources, its events, its agent dispatch, its 30-day clock or the deviation service level | Solution architect | Resolved (directive) |
| GAP-3070 | RWB-S8-E7010-APP: the contact-breach path has no rule row, no column, no published ledger read, no operation of its own, no event and no write right for its primary role | Center of excellence with the solution architect, the rwb-decision rule owner, the rwb-source-data owner and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3082 | RWB-S8-E1023-APP: a P3 Case and workflow module story is placed in rwb-deviation with an empty build row, and the plan gives the slice no platform dependency although seven pattern rows add one | Solution architect | Resolved (directive) |
| GAP-3087 | RWB-S8-E2009-APP: a P9 Reporting story is placed in rwb-deviation with one C row and an empty build row, and the seven owner reads, the matrix edge and the platform prerequisites are unpublished | Solution architect | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3129 | RWB-S9-E7015-APP: the contract end has no operation, the recall has no event, "open" has no definition, the partner service level sits on no PRM rule row and the case-side re-selection has no published boundary | Solution architect with the rwb-case owner, the rwb-decision rule owner and the center of excellence | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3227 | The 23 new wave-0 platform stories have no release date | Delivery lead | Resolved (directive) |
| GAP-3244 | The new platform stories N001 to N012 and the harness stories W1J01 to W4J01 sit in no window of version 3 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
