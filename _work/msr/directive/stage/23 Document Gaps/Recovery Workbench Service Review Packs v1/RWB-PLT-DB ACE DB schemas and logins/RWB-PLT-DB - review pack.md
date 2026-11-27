# RWB-PLT-DB ACE DB schemas and logins - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 2 |
| Resolved in the stories | 22 |
| Cross-document (pending in another document) | 25 |
| Not applied (value not in the sources) | 11 |
| Open business decisions | 0 |
| Register gaps linked | 22 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-N011-DB | 11 | 4 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-DB ACE DB schemas and logins/RWB PLT N011 DB PgBouncer pools, migrator role and grant check - ACE DB v2.md |
| RWB-PLT-NF06-DB | 11 | 21 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-DB ACE DB schemas and logins/RWB PLT NF06 DB Create the 19 rwb_ schemas and logins - ACE DB v2.md |

## 3. Open business decisions (not resolved; owner decides)

None.

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-N011-DB | R-07348 | DOR-RWB-PLT-N011-DB-16 | Header | Definition of Ready item 16 Size: Fail | The squad-refinement wording is not in any source; the item is not resolved by the story. |
| RWB-PLT-N011-DB | R-11860 | CG-ALL-1268 | 12.8 | Criteria and test data read ACE views directly | AC6 text and the rwb-source-data contract fake are outside this chunk. 12.8 says None and names no fake, so no fake name was invented. |
| RWB-PLT-N011-DB | R-18792 | DOR-RWB-PLT-N011-DB-15 | Header | Definition of Ready item 15 INVEST: Partial | 'Small, fits within two weeks' is not in the sources. |
| RWB-PLT-N011-DB | R-18794 | DOR-RWB-PLT-N011-DB-4 Business rules: Partial | 8 | Definition of Ready item 4 Business rules: Partial | Coverage needs AC7 anchored in section 7 and test rows in section 16; the rules cannot be anchored in this chunk. |
| RWB-PLT-N011-DB | R-18795 | DOR-RWB-PLT-N011-DB-7 | 11 | Definition of Ready item 7 Data: Partial | All 38 section 11 rows already carry BR IDs, so no edit. recovery_svc and the ACE-view criteria text are outside this chunk. |
| RWB-PLT-N011-DB | R-29075 | GAP-1390 | 11 | Whether the per-login cap is delivered by the managed PgBouncer of the Azure Database for PostgreSQL service or by a PgBouncer deployment the platform runs is not specified | The story cannot choose between managed and platform-run PgBouncer; the source leaves it open. |
| RWB-PLT-N011-DB | R-31815 | NEWAC-RWB-PLT-N011-DB-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | The proposed test is not specified in the sources, so the TC row and the scenario content are placeholders. |
| RWB-PLT-NF06-DB | R-07385 | DOR-RWB-PLT-NF06-DB-22 |  | Definition of Ready item 22 Fake published: Fail | Section 12.8 uses the rwb-source-data fake, which this story does not publish. Its version is Not specified in the source documents (CG-ALL-1276). |
| RWB-PLT-NF06-DB | R-07386 | DOR-RWB-PLT-NF06-DB-23 |  | Definition of Ready item 23 Contract version fixed: Fail | The rwb-source-data fake in section 12.8 has no version in the sources (CG-ALL-1276), so no contract version is fixed here. |
| RWB-PLT-NF06-DB | R-11867 | CG-ALL-1276 | 12.8, 16 | Criteria and test data read ACE views directly | 12.8 and TC-PLT-NF06-DB-04 now use the rwb-source-data fake. AC4 Given lines in section 7 still read the views and are outside this chunk. |
| RWB-PLT-NF06-DB | R-31824 | NEWAC-RWB-PLT-NF06-DB-AC8 | 8 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so there is no anchor for AC8 or its TC row. The proposed test is not in the sources. Resend those parts. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15153 | RWB-PLT-NF06-DB | CG-ALL-1269 | 3 | Record search_path as a PostgreSQL login setting (a database-layer object, not a field), or record it in the owning document. |
| CDC-15154 | RWB-PLT-NF06-DB | CG-ALL-1270 | 13 | Record recovery_svc as the legacy login replaced by the per-service logins (DP-02), or record it in the owning document. |
| CDC-15158 | RWB-PLT-NF06-DB | CG-ALL-1274 | 16 | Record pg_roles (PostgreSQL system catalogue, read by TC-PLT-NF06-DB-03 in section 16) as an ACE database object, or name its dictionary entry. |
| CDC-15163 | RWB-PLT-NF06-DB | GAP-2251 | 1 | Confirm field identifiers of queue, queue_member, assignment, task, timer, case_entry_exclusion and reference_version before the migration is cut. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15155 | RWB-PLT-NF06-DB | CG-ALL-1271 | 16 | Record pg_namespace as a PostgreSQL system catalog object, outside the field dictionary, in the owning document. |
| CDC-15156 | RWB-PLT-NF06-DB | CG-ALL-1272 | 16 | Record pg_class as a PostgreSQL system catalog object, outside the field dictionary, in the owning document. |
| CDC-15157 | RWB-PLT-NF06-DB | CG-ALL-1273 | 16 | Record pg_default_acl as a PostgreSQL system catalog object, outside the field dictionary, in the owning document. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15120 | RWB-PLT-N011-DB | DOR-RWB-PLT-N011-DB-1 | 1 | Add 'ACE database engineer' as a role code or role name, or confirm the role it maps to. |
| CDC-15159 | RWB-PLT-NF06-DB | DOR-RWB-PLT-NF06-DB-1 | 1 | Add the role ACE database administrator used in section 1, or confirm its role code and name. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15160 | RWB-PLT-NF06-DB | DOR-RWB-PLT-NF06-DB-12 | 16, 18 | Reconcile the NF-06 test-case list with section 18 of RWB-PLT-NF06-DB, which lists TC-PLT-NF06-DB-01 to -07. |
| CDC-15167 | RWB-PLT-NF06-DB | CG-ALL-1275 | 18 | Align the REQ-DRI-006 test list with section 18 of this story (TC-PLT-NF06-DB-02, TC-PLT-NF06-DB-04) in the next RTM version. |

### RWB-PLT-N011-DB; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15119 | RWB-PLT-N011-DB | DOR-RWB-PLT-N011-DB-14 | Header | Record and sign off the epic design for RWB-PLT-DB in the epic design record. |

### OTHER:Version 3 source document (How column, section 1 and section 3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15121 | RWB-PLT-N011-DB | GAP-0237 | find it | Describe each migration as an extract by rwb-source-data (P1) and an owner-run Flyway load into the owner's schema by the owner's migrator login; P1 never writes another schema. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx; OTHER:Stories sheet row 121 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15122 | RWB-PLT-N011-DB | GAP-3194 | find it | Cite on row 121 the chosen story per service (S2, S4, S5, S6, S7, P6, P8) for the column drop: one new ACE DB story each, or the APP story that creates the table, before wave 2. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15152 | RWB-PLT-NF06-DB | DOR-RWB-PLT-NF06-DB-14 | header | Record the signed epic design sign-off for RWB-PLT-DB; the story cannot record a sign-off that is absent from the source set. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15161 | RWB-PLT-NF06-DB | GAP-0150 | 13 | Record the split of the single recovery schema into 19 rwb_* schemas as new work under RWB-PLT-NF06-DB and the per-service DB stories; keep FEAT-RDF-01 and FEAT-RDF-25 word for word. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15162 | RWB-PLT-NF06-DB | GAP-0285 | 13 | Cut and V0001 baseline marked as not specified; the story no longer cites a cut table. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15164 | RWB-PLT-NF06-DB | GAP-3194 | 1 | Raise one ACE DB story per service without one (S2, S4, S5, S6, S7, P6, P8), or attach the column drop to the creating APP story, and cite it on row 121 before wave 2. |

### OTHER:ACE DBA standard for the 19 schemas (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15165 | RWB-PLT-NF06-DB | GAP-1384 | 1 | Creation options marked as not specified in the sources; no options are invented in the story. |

### RWB-PLT-NF03-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15166 | RWB-PLT-NF06-DB | GAP-1385 | 1 | Environments and running role marked as not specified in the sources; wave timing removed. |

### OTHER:Build plan (row H) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15168 | RWB-PLT-NF06-DB | GAP-2540 | Header | The H row belongs to the plan, not this story. The story names no six contracts after the revert. |

### RWB-PLT-N011-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15169 | RWB-PLT-NF06-DB | GAP-1387 | 8 | State that migrations are applied by a per-service migrator login granted on its own service's schema only; the owning login keeps ownership; this story grants no DDL beyond ownership. |

### OTHER:NFR Specification v3 and ADR-023 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15170 | RWB-PLT-NF06-DB | GAP-0093 | none | Set RPO and RTO per service tier in the next NFR Specification version and restate them in ADR-023. |

### OTHER:Legacy NF-06 story file (04 User stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15171 | RWB-PLT-NF06-DB | GAP-1386 | header | Supply the legacy NF-06 story file; if it carries criteria, test cases or messages, restate AC1 to AC7 against it and add the recovered ones with legacy origin tags. |

### OTHER:Rules Engine Design v3, section 8 (count-keeping document) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15172 | RWB-PLT-NF06-DB | GAP-2033 | 8 | State that 93 is the count of the target table set across the 19 rwb_* schemas, that the registry's four tables are in schema rwb_decision, and that the distribution is the RWB-PLT-NF06-DB split work. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0093 | RPO and RTO are not set in NFR Spec v3 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0111 | The source grants use placeholder roles and do not create the 19 logins | ACE team | Resolved (directive) |
| GAP-0150 | FEAT-RDF-01 still creates one recovery schema of 92 tables while D-RCV-60 gives each service its own schema | ACE database team lead and the platform DB solution architect | Resolved (directive) |
| GAP-0237 | Version 3 has the Workbench run the load; the target makes the schema owner run it | TechX | Resolved (directive) |
| GAP-0285 | No source states how the built recovery schema, 92 tables and 14 data products, is cut across the 19 rwb_* schemas or how each V0001 baseline is produced | ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0758 | The rwb-case per-service login name is not specified | RW-SECADM | Resolved (directive) |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1318 | The name of the per-service database login is not fixed by any source | ACE DB team with the platform team | Resolved (directive) |
| GAP-1384 | The creation options of the 19 schemas are not specified | ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1385 | The environments that receive the 19 schemas in wave 0 and the role that runs the script there are not specified | ACE DBA | Resolved (directive) |
| GAP-1386 | The legacy NF-06 story text, its acceptance criteria and its test cases are absent from the source set | Technical writer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1387 | Whether the service login or a separate migrator login applies the migrations is not specified | Solution architect | Resolved (directive) |
| GAP-1388 | Pool mode, default pool size, connection cap per login, idle and connection timeouts and the server-side reserve are not specified | ACE DBA | Resolved (directive) |
| GAP-1389 | Migrator login naming, its number, the role that creates it and how its credential is held are not specified | ACE DBA | Resolved (directive) |
| GAP-1390 | Whether the per-login cap is delivered by the managed PgBouncer of the Azure Database for PostgreSQL service or by a PgBouncer deployment the platform runs is not specified | Platform template owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1391 | Where the grant check runs, what it publishes and how long the result is kept are not specified | DevOps lead | Resolved (directive) |
| GAP-2033 | The rule store is counted in one schema in version 3 and distributed over 19 schemas in the target | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2066 | The failover test and the restore test of the source have no story in the split plan | QA team suggested, with RWB-PLT-DB and P5 rwb-document | Resolved (directive) |
| GAP-2251 | The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | TechX and the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
