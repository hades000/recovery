# RWB-PLT-DB ACE DB schemas and logins - resolved items

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-PLT-N011-DB | R-07349 | DOR-RWB-PLT-N011-DB-21 | 12.8 | Definition of Ready item 21 Contract published: Fail | Story publishes no contract, so no CON story or CON dependency is needed; 12.8 and the Contract dependencies row say so. |
| RWB-PLT-N011-DB | R-07350 | DOR-RWB-PLT-N011-DB-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | Story publishes no contract and so has no contract fake; 12.8 now states that no contract fake library version applies. |
| RWB-PLT-N011-DB | R-07351 | DOR-RWB-PLT-N011-DB-23 | 12.8 | Definition of Ready item 23 Contract version fixed: Fail | 12.8 now states that no contract version applies, because the story consumes no service contract. |
| RWB-PLT-N011-DB | R-11859 | CG-ALL-1267 | Other (L356) | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | Replaced the legacy recovery_svc login name in the DP-02 note with a description, so no unmatched object name remains. |
| RWB-PLT-N011-DB | R-18791 | DOR-RWB-PLT-N011-DB-12 | 16 | Definition of Ready item 12 Test cases: Partial | Added TC-PLT-N011-DB-07, a boundary test of the 12.7 artefacts (18, 19 and 20 pool entries and logins). |
| RWB-PLT-N011-DB | R-18793 | DOR-RWB-PLT-N011-DB-24 | 12.7 | Definition of Ready item 24 Ownership stated: Partial | Added Owner column to 12.7 table: ACE DBA for pool entries and migrator logins, DevOps lead for grant check. |
| RWB-PLT-N011-DB | R-22282 | GAP-0111 | 11 | The source grants use placeholder roles and do not create the 19 logins | Added commented grants template before the 'What this story holds' paragraph, pointing to RWB-PLT-NF06 and RWB-PLT-N011 |
| RWB-PLT-N011-DB | R-23294 | GAP-1388 | 11 | Pool mode, default pool size, connection cap per login, idle and connection timeouts and the server-side reserve are not specified | Added: ACE DBA publishes per-login cap, pool size, mode, timeouts and reserve before first release; 5 s timeout stands. |
| RWB-PLT-N011-DB | R-23295 | GAP-1389 | 11 | Migrator login naming, its number, the role that creates it and how its credential is held are not specified | Added: ACE DBA creates each migrator login once per service; credential is a key-store reference only (NFR-052). |
| RWB-PLT-N011-DB | R-29074 | GAP-1391 | 12.7 | Where the grant check runs, what it publishes and how long the result is kept are not specified | Grant check row now names beside lint and drift gate, one result per login per run attached to the run, kept for audit period agreed with internal audit; owner DevOps lead. |
| RWB-PLT-N011-DB | R-29076 | GAP-1387 | 8 | Whether the service login or a separate migrator login applies the migrations is not specified | BR5 now states the migrator login applies the migrations, the owning login keeps ownership, and no DDL beyond ownership is granted. |
| RWB-PLT-NF06-DB | R-07383 | DOR-RWB-PLT-NF06-DB-16 | header | Definition of Ready item 16 Size: Fail | Added Size row to the header table: not specified, to be sized by the squad at refinement. |
| RWB-PLT-NF06-DB | R-07384 | DOR-RWB-PLT-NF06-DB-21 |  | Definition of Ready item 21 Contract published: Fail | The story publishes no contract. Section 12.8 and TC-PLT-NF06-DB-04 use the rwb-source-data contract fake. RWB-PLT-NF06-CON is not in the source set. |
| RWB-PLT-NF06-DB | R-18821 | DOR-RWB-PLT-NF06-DB-15 | header | Definition of Ready item 15 INVEST: Partial | Size row now says Small and fits two weeks. |
| RWB-PLT-NF06-DB | R-18822 | DOR-RWB-PLT-NF06-DB-24 | 12.7, 13 | Definition of Ready item 24 Ownership stated: Partial | Owner and service stated for the section 12.7 rows; section 13 now refers to row 17 of section 11, not the schema name. |
| RWB-PLT-NF06-DB | R-18823 | DOR-RWB-PLT-NF06-DB-4 | 8 | Definition of Ready item 4 Business rules: Partial | Coverage paragraph maps BR1 to BR10 to ACs and test cases; BR10 is covered only as the login binding. |
| RWB-PLT-NF06-DB | R-18824 | DOR-RWB-PLT-NF06-DB-7 | 11 | Definition of Ready item 7 Data: Partial | Added a BR Field ID statement after the section 11 closing paragraph: no data row has one, because the items are PostgreSQL objects, not LDM v9 or Data Classification v5 fields. |
| RWB-PLT-NF06-DB | R-22016 | GAP-0688 | 1 | Per-service database login name for rwb-case is not specified | Placeholder rwb-case login kept until the ACE DB team names it, as the proposed fix directs. |
| RWB-PLT-NF06-DB | R-28536 | GAP-1037 | 11 | Per-service login name for rwb-document is not specified | Allocated login rwb_document, its own-schema-only grants and secret reference (RWB-PLT-NF04-OPS credential path) in section 11 and in the section 1 login-names line. |
| RWB-PLT-NF06-DB | R-28626 | GAP-0758 | 11 | The rwb-case per-service login name is not specified | Allocated login rwb_case with its own-schema grants and secret reference in section 11 and in the section 1 login-names line. |
| RWB-PLT-NF06-DB | R-28920 | GAP-2066 | 1 | The failover test and the restore test of the source have no story in the split plan | Added bullet assigning the failover test to this story with the ACE DBA and the restore test to P5 rwb-document with RWB-PLT-DB. |
| RWB-PLT-NF06-DB | R-28935 | GAP-1318 | 8 | The name of the per-service database login is not fixed by any source | Story already keeps the phrase 'the rwb-decision login' with no name. The login name is allocated with the schema in this P7 DB story and written to the secret store. |
