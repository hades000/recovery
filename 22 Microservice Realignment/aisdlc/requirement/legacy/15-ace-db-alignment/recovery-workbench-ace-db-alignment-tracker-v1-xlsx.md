<!-- source: 15 ACE DB Alignment/Recovery Workbench ACE DB Alignment Tracker v1.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `15 ACE DB Alignment/Recovery Workbench ACE DB Alignment Tracker v1.xlsx`  
> **Converted from:** XLSX

## Read me

| Recovery Workbench ACE DB alignment tracker v1 |
|---|
| SCB Collections and Recovery. Henka Group, 15 November 2026. |
| What this workbook is |
| The working tracker for the ACE alignment. It holds the per-document edit list, the per-story disposition and the |
| governance actions. The narrative case for the change is in Recovery Workbench ACE DB Alignment Change Register v1.md. |
| Status values |
| Not started  - no new-version file exists yet |
| Drafted      - the new-version file exists and the edit log is appended to the register |
| In review    - the data architect or the ACE team lead is reading it |
| Approved     - signed off; the old version may be retired at the next index update |
| Superseded   - the document is replaced by a different document, not a new version |
| One writer per file |
| Each row has one owner agent. An agent writes only its own new-version file and returns an edit log. No agent edits a |
| file another agent owns. Frozen inputs: the change register, the ACE schema dump, the Tier Map, LDM v7 and Physical Schema v5. |
| Waves |
| W0  register, Tier Map, gap list, views, schema dump (this pack) |
| W1  STTM v4, LDM v7, Physical Schema v5, RWB-ACE-001, then verify |
| W2  governance, architecture, requirements, data documents (45 files) |
| W3  stories, build notes (16 files) |
| W4  test, delivery (13 files) |
| W5  index, control sheet, hub, verification (3 files) |

## Documents

| # | Folder | Current file | New file | Size | Wave | Change | Owner | Status | Edit log ref | Date done |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Decisions and governance | Recovery Workbench Decision Log v8.xlsx | Recovery Workbench Decision Log v9.xlsx | M | W2 | Add D-RCV-35 (U1 to U5) and DL43. Mark DT12, DL06 option A and DL12 option A superseded; mark DL20 amended; amend D-RCV-29 counts. |  | Drafted |  |  |
| 2 | 01 Decisions and governance | Recovery Workbench RWB-E1-001 Specification Rulings v1.md | Recovery Workbench RWB-E1-001 Specification Rulings v2.md | S | W2 | Superseded-by note on the copy-table counts (44 tables, 533 fields, 108/1,256). Ruling R4 definitions still hold, re-worded to ACE. |  | Drafted |  |  |
| 3 | 01 Decisions and governance | Recovery Workbench RWB-E1-001 Pre-Build Rulings v1.md | Recovery Workbench RWB-E1-001 Pre-Build Rulings v2.md | S | W2 | Same superseded-by note and count re-base. |  | Drafted |  |  |
| 4 | 01 Decisions and governance | Recovery Workbench Admin and Access Model v4.docx | Recovery Workbench Admin and Access Model v5.docx | S | W2 | Remove the SY-DATALOAD actor; add the read-only ACE service identity and its grant. |  | Drafted |  |  |
| 5 | 02 Business architecture and process | Recovery Workbench Feature List v3.xlsx | Recovery Workbench Feature List v4.xlsx | M | W2 | Retire the load, DQ and tracker features (FEAT-RDF-03..13, 22); FEAT-RDF-01 becomes tables plus views; add FEAT-RDF-25 ACE source views and FEAT-RDF-26 ACE DB additions. |  | Drafted |  |  |
| 6 | 02 Business architecture and process | Recovery Workbench Business Glossary v2.xlsx | Recovery Workbench Business Glossary v3.xlsx | S | W2 | 17 terms repointed from Workbench copies to ACE tables and views. |  | Drafted |  |  |
| 7 | 02 Business architecture and process | Recovery Workbench Role to System Access Matrix v2.xlsx | Recovery Workbench Role to System Access Matrix v3.xlsx | S | W2 | Remove SY-DATALOAD rows; add read-only ACE database access for the recovery service identity. |  | Drafted |  |  |
| 8 | 03 Requirements and specifications | Recovery Workbench Business Requirements Epic 1 v3.docx | Recovery Workbench Business Requirements Epic 1 v4.docx | L | W2 | Section 3.1 P1 and 3.2 P2 rewritten: read from ACE replaces load and check. Sections 4 and 7 reconciled. |  | Drafted |  |  |
| 9 | 03 Requirements and specifications | Recovery Workbench Business Requirements Program v3.docx | Recovery Workbench Business Requirements Program v4.docx | M | W2 | Sections 5.1 to 5.3, 6.3 Loads and batch, 7 and 9. |  | Drafted |  |  |
| 10 | 03 Requirements and specifications | Recovery Workbench Lean BRD Epic 1 v2.docx | Recovery Workbench Lean BRD Epic 1 v3.docx | M | W2 | Sections 2.1 scope, 6.1 and 7. |  | Drafted |  |  |
| 11 | 03 Requirements and specifications | Recovery Workbench Non Functional Specification v2.docx | Recovery Workbench Non Functional Specification v3.docx | M | W2 | Section 3.3 loads and batch becomes freshness and availability of ACE data; volumes re-based. |  | Drafted |  |  |
| 12 | 03 Requirements and specifications | Recovery Workbench Epics 3 to 8 Specification v2.docx | Recovery Workbench Epics 3 to 8 Specification v3.docx | S | W2 | Integration sections 2.4 to 5.4. |  | Drafted |  |  |
| 13 | 03 Requirements and specifications | Recovery Workbench Epics 3 to 8 Specification v2.xlsx | Recovery Workbench Epics 3 to 8 Specification v3.xlsx | S | W2 | Same integration sections, cell by cell. |  | Drafted |  |  |
| 14 | 03 Requirements and specifications | Recovery Workbench Functional Specifications by Module v4.zip | Recovery Workbench Functional Specifications by Module v5.zip | L | W2 | P1 rewritten around views, freshness and the data dictionary; P2 outbound only; P3 and P8 re-pointed; S1, S2, S5, S8 small. |  | Drafted |  |  |
| 15 | 04 User stories | Recovery Workbench User Stories Epic 1 v7.md | Recovery Workbench User Stories Epic 1 v8.md | L | W3 | Remove 8, add E1-069, rewrite 13, minor 21. Entities, Gherkin and traceability. |  | Drafted |  |  |
| 16 | 04 User stories | Recovery Workbench User Stories Epic 1 v7.xlsx | Recovery Workbench User Stories Epic 1 v8.xlsx | L | W3 | Same stories; Entities column, Gherkin cells and Test case Data cells. |  | Drafted |  |  |
| 17 | 04 User stories | Recovery Workbench User Stories Epic 1 Story Files v5.zip | Recovery Workbench User Stories Epic 1 Story Files v6.zip | M | W3 | Regenerate the per-story folder and archive from v8. |  | Drafted |  |  |
| 18 | 04 User stories | Recovery Workbench User Stories Epic 2 v5.md | Recovery Workbench User Stories Epic 2 v6.md | M | W3 | Remove E2-023, rewrite 6, minor 16. |  | Drafted |  |  |
| 19 | 04 User stories | Recovery Workbench User Stories Epic 2 v5.xlsx | Recovery Workbench User Stories Epic 2 v6.xlsx | M | W3 | Same, with Entities and test data. |  | Drafted |  |  |
| 20 | 04 User stories | Recovery Workbench User Stories Epics 3 to 8 v2.md | Recovery Workbench User Stories Epics 3 to 8 v3.md | M | W3 | Rewrite 6, minor 65. Mostly Data-table entity names. |  | Drafted |  |  |
| 21 | 04 User stories | Recovery Workbench User Stories Epics 3 to 8 v2.xlsx | Recovery Workbench User Stories Epics 3 to 8 v3.xlsx | M | W3 | Same. |  | Drafted |  |  |
| 22 | 04 User stories | Recovery Workbench Technical Enabler Stories v5.md | Recovery Workbench Technical Enabler Stories v6.md | S | W3 | Rewrite TE-001, TE-004, TE-007; minor TE-011. |  | Drafted |  |  |
| 23 | 04 User stories | Recovery Workbench Technical Enabler Stories v5.xlsx | Recovery Workbench Technical Enabler Stories v6.xlsx | S | W3 | Same. |  | Drafted |  |  |
| 24 | 04 User stories | Recovery Workbench Data Migration Stories v2.md | Recovery Workbench Data Migration Stories v3.md | M | W3 | Remove DM-001 and DM-002; reduce DM-005, DM-006, DM-011, DM-013; keep the other 8. Fix the loan_account template artifact in all 14. |  | Drafted |  |  |
| 25 | 04 User stories | Recovery Workbench Data Migration Stories v2.xlsx | Recovery Workbench Data Migration Stories v3.xlsx | M | W3 | Same. |  | Drafted |  |  |
| 26 | 04 User stories | Recovery Workbench Administration Stories v2.md | Recovery Workbench Administration Stories v3.md | S | W3 | Rewrite AD-018 and AD-019 without loads; minor AD-004. |  | Drafted |  |  |
| 27 | 04 User stories | Recovery Workbench Administration Stories v2.xlsx | Recovery Workbench Administration Stories v3.xlsx | S | W3 | Same. |  | Drafted |  |  |
| 28 | 04 User stories | (new) | Recovery Workbench ACE Team Stories v1.md | M | W1 | RWB-ACE-001 and its field appendix. |  | Drafted |  |  |
| 29 | 04 User stories | (new) | Recovery Workbench ACE Team Stories v1.xlsx | M | W1 | Same, with the field appendix as a sheet. |  | Drafted |  |  |
| 30 | 04 User stories | Recovery Workbench Build Notes Epic 1 v4.md | Recovery Workbench Build Notes Epic 1 v5.md | M | W3 | Replace load and job steps with view, grant and freshness notes. |  | Drafted |  |  |
| 31 | 04 User stories | Recovery Workbench Build Notes Epic 2 v2.md | Recovery Workbench Build Notes Epic 2 v3.md | S | W3 | Outbound-only adapter notes. |  | Not started |  |  |
| 32 | 04 User stories | Recovery Workbench Build Notes Technical Enablers v1.md | Recovery Workbench Build Notes Technical Enablers v2.md | S | W3 | Boundary test, masked reads, Quartz on the ACE batch record. |  | Not started |  |  |
| 33 | 04 User stories | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3.xlsx | S | W4 | Close the defects that the removal or rewrite answers; add the new view and ACE story defects. |  | Drafted |  |  |
| 34 | 05 Technical architecture | Recovery Workbench ACE Architecture Decision v2.docx | Recovery Workbench ACE Architecture Decision v3.docx | M | W2 | Sections 1 How data arrives, 4 a module reads only its own tables (v_ace_* exception), 5 and 7 Data. |  | Drafted |  |  |
| 35 | 05 Technical architecture | Recovery Workbench Architecture Decision Records v1.md | Recovery Workbench Architecture Decision Records v2.md | M | W2 | Add ADR-010 read source data from ACE through read-only views; mark ADR-005 superseded; update ADR-001 consequences. |  | Drafted |  |  |
| 36 | 05 Technical architecture | Recovery Workbench Target Architecture v4.docx | Recovery Workbench Target Architecture v5.docx | L | W2 | Sections 2 to 5.2, 8.1, 9 to 11; new data tier diagram. |  | Drafted |  |  |
| 37 | 05 Technical architecture | Recovery Workbench Target Architecture v4.pptx | Recovery Workbench Target Architecture v5.pptx | L | W2 | Same, slide by slide. |  | Drafted |  |  |
| 38 | 05 Technical architecture | Recovery Workbench Information Flow v4.pptx | Recovery Workbench Information Flow v5.pptx | L | W2 | All 11 slides: inbound flows become into ACE (ACE team), plus Workbench reads views. |  | Drafted |  |  |
| 39 | 05 Technical architecture | Recovery Workbench Interface Specifications v2.md | Recovery Workbench Interface Specifications v3.md | L | W2 | Inbound INT-01..13, 15, 16 re-owned to ACE; field maps kept as the ACE ingestion spec. Outbound unchanged. |  | Drafted |  |  |
| 40 | 05 Technical architecture | Recovery Workbench Interface Specifications v2.xlsx | Recovery Workbench Interface Specifications v3.xlsx | L | W2 | Same. |  | Drafted |  |  |
| 41 | 05 Technical architecture | Recovery Workbench System Disposition and Integration Inventory v2.xlsx | Recovery Workbench System Disposition and Integration Inventory v3.xlsx | M | W2 | Add an In ACE today column and an Owner column for ACE ingestion. |  | Drafted |  |  |
| 42 | 05 Technical architecture | Recovery Workbench Batch and Scheduling Design v2.docx | Recovery Workbench Batch and Scheduling Design v3.docx | L | W2 | Remove JOB-01 and JOB-09; trigger JOB-02, 04, 07, 08, 16 on the ACE batch-complete record. |  | Drafted |  |  |
| 43 | 05 Technical architecture | Recovery Workbench Batch and Scheduling Design v2.xlsx | Recovery Workbench Batch and Scheduling Design v3.xlsx | L | W2 | Same. |  | Drafted |  |  |
| 44 | 05 Technical architecture | Recovery Workbench API Specification v2.yaml | Recovery Workbench API Specification v3.yaml | M | W2 | Remove the tracker, load rerun, DQ exception and manual retirement endpoints; repoint CaseAccount, CaseParty and Proceeds descriptions. |  | Drafted |  |  |
| 45 | 05 Technical architecture | Recovery Workbench API Specification v2.html | Recovery Workbench API Specification v3.html | M | W2 | Regenerate from the v3 yaml. |  | Drafted |  |  |
| 46 | 05 Technical architecture | Recovery Workbench Event and Messaging Design v2.md | Recovery Workbench Event and Messaging Design v3.md | S | W2 | EV-26 and EV-27 become AceDataReady and AceDataLate, sourced from the ACE batch record. |  | Drafted |  |  |
| 47 | 05 Technical architecture | Recovery Workbench Event and Messaging Design v2.xlsx | Recovery Workbench Event and Messaging Design v3.xlsx | S | W2 | Same. |  | Drafted |  |  |
| 48 | 05 Technical architecture | Recovery Workbench Technical Specifications by Module v3.zip | Recovery Workbench Technical Specifications by Module v4.zip | L | W2 | P1 T3 model re-drawn; P2 outbound only; P3, P8, S1, S5 re-pointed. |  | Drafted |  |  |
| 49 | 05 Technical architecture | Recovery Workbench Security and Access Design v2.docx | Recovery Workbench Security and Access Design v3.docx | S | W2 | Read-only grant, no tokenization at load, no load service identity. |  | Drafted |  |  |
| 50 | 05 Technical architecture | Recovery Workbench Environment and Deployment Design v2.docx | Recovery Workbench Environment and Deployment Design v3.docx | S | W2 | Two-migration rule; ACE read role; no load containers or file shares. |  | Drafted |  |  |
| 51 | 06 Data | Recovery Workbench Physical Schema v4.sql | Recovery Workbench Physical Schema v5.sql | L | W1 | Drop 20 tables; add 4 extension tables and 26 views; re-key 14 foreign keys; reseed sys_objects and sys_fields; seed the 14 data_product rows; system_of_record becomes ACE (from X). |  | Drafted |  |  |
| 52 | 06 Data | Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx | Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx | L | W1 | The 133 external fields get an ACE table.column or ACE-new (RWB-ACE-001); new ACE mapping sheet; relationships re-keyed. |  | Drafted |  |  |
| 53 | 06 Data | Recovery Workbench Source to Target Mapping v3.xlsx | Recovery Workbench Source to Target Mapping v4.xlsx | L | W1 | Becomes ACE column to Workbench view field; new ACE gaps sheet is the RWB-ACE-001 input; load-time transforms move to the views. |  | Drafted |  |  |
| 54 | 06 Data | Recovery Workbench Conceptual Data Model v5.xlsx | Recovery Workbench Conceptual Data Model v6.xlsx | S | W2 | Data products: system of record via ACE; Gaps sheet. |  | Drafted |  |  |
| 55 | 06 Data | Recovery Workbench Conceptual Data Model v5.pptx | Recovery Workbench Conceptual Data Model v6.pptx | S | W2 | Slides 7 and 9. |  | Drafted |  |  |
| 56 | 06 Data | Recovery Workbench Entity Relationship Diagram v3.html | Recovery Workbench Entity Relationship Diagram v4.html | M | W2 | ACE tables as external boxes; key changes. |  | Drafted |  |  |
| 57 | 06 Data | Recovery Workbench Entity Relationship Diagram v3.pdf | Recovery Workbench Entity Relationship Diagram v4.pdf | M | W2 | Regenerate from the v4 html. |  | Drafted |  |  |
| 58 | 06 Data | Recovery Workbench Data Quality and Reconciliation Rules v2.xlsx | Recovery Workbench Data Quality and Reconciliation Rules v3.xlsx | L | W2 | 98 load checks removed or handed to the ACE story; REC-01 to REC-04 reconcile to ACE; new REC-05 for the business-key links. |  | Drafted |  |  |
| 59 | 06 Data | Recovery Workbench Party and Customer Master Data Design v2.docx | Recovery Workbench Party and Customer Master Data Design v3.docx | L | W2 | Party is ACE customer plus ca_relation plus party_ext; match rules M1 to M5 become ACE ingestion. |  | Drafted |  |  |
| 60 | 06 Data | Recovery Workbench Party and Customer Master Data Design v2.xlsx | Recovery Workbench Party and Customer Master Data Design v3.xlsx | L | W2 | Same. |  | Drafted |  |  |
| 61 | 06 Data | Recovery Workbench Data Migration Approach v2.docx | Recovery Workbench Data Migration Approach v3.docx | M | W2 | ALS and EFS history already in ACE; scope reduced. |  | Drafted |  |  |
| 62 | 06 Data | Recovery Workbench Data Classification and Personal Data Inventory v3.xlsx | Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx | M | W2 | Personal fields re-homed to ACE columns and views; masking in the views. |  | Drafted |  |  |
| 63 | 06 Data | Recovery Workbench Reference Data and Lists of Values v3.xlsx | Recovery Workbench Reference Data and Lists of Values v4.xlsx | M | W2 | 14 loaded lists point at efs_action_code, product and branch. |  | Drafted |  |  |
| 64 | 06 Data | Recovery Workbench Reporting and Analytics Data Model v2.xlsx | Recovery Workbench Reporting and Analytics Data Model v3.xlsx | S | W2 | Source names only. |  | Drafted |  |  |
| 65 | 06 Data | Recovery Workbench Volume and Scale Forecast v2.xlsx | Recovery Workbench Volume and Scale Forecast v3.xlsx | S | W2 | Storage and load sizing removed; view read sizing added. |  | Drafted |  |  |
| 66 | 06 Data | Recovery Workbench Volume and Scale Forecast v2.pptx | Recovery Workbench Volume and Scale Forecast v3.pptx | S | W2 | Same. |  | Drafted |  |  |
| 67 | 06 Data | Recovery Workbench Data Ownership and Stewardship v2.xlsx | Recovery Workbench Data Ownership and Stewardship v3.xlsx | S | W2 | ACE team owns Tier 2; Workbench owns Tier 3 and 4. |  | Drafted |  |  |
| 68 | 09 Testing and quality | Recovery Workbench Test Cases v5.xlsx | Recovery Workbench Test Cases v6.xlsx | L | W4 | Park or remove 115 load-story cases; re-point about 205; add cases for E1-069 and RWB-ACE-001. |  | Drafted |  |  |
| 69 | 09 Testing and quality | Recovery Workbench Regression Suite v5.xlsx | Recovery Workbench Regression Suite v6.xlsx | M | W4 | Remove parked cases; add the view conformance case. |  | Drafted |  |  |
| 70 | 09 Testing and quality | Recovery Workbench Requirements Traceability Matrix v4.xlsx | Recovery Workbench Requirements Traceability Matrix v5.xlsx | M | W4 | Every REQ-RDF row points at a live story or test. |  | Drafted |  |  |
| 71 | 09 Testing and quality | Recovery Workbench Test Data Plan v2.docx | Recovery Workbench Test Data Plan v3.docx | S | W4 | The sandbox seeds ACE-shaped tables. |  | Drafted |  |  |
| 72 | 10 Policy, controls and compliance | Recovery Workbench Controls Catalog v2.xlsx | Recovery Workbench Controls Catalog v3.xlsx | S | W4 | CTL-01 reconciles to ACE; CTL-02 moves to ACE ingestion; new CTL for the read-only grant. |  | Drafted |  |  |
| 73 | 11 Delivery and operations | Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx | Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx | L | W4 | Window 1 loses E1-003, E1-005 and the inbound half of E1-007; gains E1-069. New critical path RWB-ACE-001 to E1-069 to E1-018 and E1-002. |  | Drafted |  |  |
| 74 | 11 Delivery and operations | Recovery Workbench Story Build Order v1.docx | Recovery Workbench Story Build Order v2.docx | L | W4 | Same order, new critical path. |  | Drafted |  |  |
| 75 | 11 Delivery and operations | Recovery Workbench Dependency Map v2.xlsx | Recovery Workbench Dependency Map v3.xlsx | M | W4 | DEP-14 re-worded; new dependency on ACE team delivery. |  | Drafted |  |  |
| 76 | 11 Delivery and operations | Recovery Workbench Risks Assumptions Issues and Dependencies v2.xlsx | Recovery Workbench Risks Assumptions Issues and Dependencies v3.xlsx | M | W4 | New risk and dependency on ACE team delivery (DL43); I-03 CCMS and SVAF layouts move to the ACE team. |  | Drafted |  |  |
| 77 | 11 Delivery and operations | Recovery Workbench Cutover and Go Live Plan v2.docx | Recovery Workbench Cutover and Go Live Plan v3.docx | M | W4 | No Workbench loads; tracker retirement procedure added here. |  | Drafted |  |  |
| 78 | 11 Delivery and operations | Recovery Workbench Release Plan v3.pptx | Recovery Workbench Release Plan v4.pptx | S | W4 | Release content names the ACE dependency. |  | Drafted |  |  |
| 79 | 11 Delivery and operations | Recovery Workbench Release Plan v3.xlsx | Recovery Workbench Release Plan v4.xlsx | S | W4 | Same. |  | Drafted |  |  |
| 80 | 12 Project communication | Recovery Workbench Document Index v11.md | Recovery Workbench Document Index v12.md | M | W5 | New file names; new row for the ACE Team Stories; new row for the change register. |  | Drafted |  |  |
| 81 | 12 Project communication | Recovery Workbench Document Control Sheet v10.xlsx | Recovery Workbench Document Control Sheet v11.xlsx | M | W5 | Same, with the change register as the controlling row. |  | Drafted |  |  |
| 82 | 12 Project communication | Recovery Workbench Project Hub v14.html | Recovery Workbench Project Hub v16.html | L | W5 | Regenerate the embedded gzip and base64 document JSON last. |  | Not started |  |  |

## Stories

| Family | Story | Disposition | Title | Entities today | ACE action | Owner | Status | Note |
|---|---|---|---|---|---|---|---|---|
| AD | RWB-AD-001 | No impact | Map Entra ID groups to Workbench roles | decision_log_entry, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-002 | No impact | Permission matrix as a versioned load | assignment, document, lov_value, role, permission | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-003 | No impact | Scope per role | recovery_case, assignment, decision_log_entry, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-004 | Minor | Masking profiles per role | recovery_case, contact_point, document, decision_log_entry, role | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| AD | RWB-AD-005 | No impact | Separation of duty check at sign-in | role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-006 | No impact | Break-glass access | role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-007 | No impact | Access log search and export | document, decision_log_entry, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-008 | No impact | Access review list | assignment, decision_log_entry, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-009 | No impact | Load a list of values version | recovery_case, assignment, document, lov_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-010 | No impact | Approve a reference data load | assignment, decision_log_entry, lov_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-011 | No impact | Load a rule version | recovery_case, document, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-012 | No impact | Approve a rule version | recovery_case, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-013 | No impact | Roll back a rule or reference version | assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-014 | No impact | Configure queues | queue, assignment, document, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-015 | No impact | Configure service levels and timers | recovery_case, timer, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-016 | No impact | Load the delegation of authority table | delegation_limit | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-017 | No impact | Manage letter and notice templates | task, legal_action, notice, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-018 | Rewrite | Interface and job monitor | document, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| AD | RWB-AD-019 | Rewrite | Data quality and reconciliation console | recovery_case, loan_account | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| AD | RWB-AD-020 | No impact | Autonomy level per decision step | decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-021 | No impact | Retention classes and legal hold | document, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| AD | RWB-AD-022 | No impact | Partner firms and partner users | partner, partner_instruction | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| DM | RWB-DM-001 | Remove | Migrate account and arrears | recovery_case, loan_account, document_field | Move the story to the register appendix; record its later home. |  | Not started |  |
| DM | RWB-DM-002 | Remove | Migrate customer and party | recovery_case, party, loan_account, document_field | Move the story to the register appendix; record its later home. |  | Not started |  |
| DM | RWB-DM-003 | Minor | Migrate case and ownership | recovery_case, assignment, loan_account, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-004 | Minor | Migrate treatment and offers | recovery_case, loan_account, treatment, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-005 | Rewrite | Migrate contact and promises | recovery_case, loan_account, document_field, interaction | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| DM | RWB-DM-006 | Rewrite | Migrate collateral and assets | recovery_case, loan_account, collateral, valuation, asset, document_field | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| DM | RWB-DM-007 | Minor | Migrate legal events and cases | recovery_case, loan_account, partner_instruction, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-008 | Minor | Migrate partner performance | recovery_case, loan_account, partner, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-009 | Minor | Migrate debt sale | recovery_case, loan_account, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-010 | Minor | Migrate documents and extracted fields | recovery_case, loan_account, document, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-011 | Rewrite | Migrate scores and route economics | recovery_case, loan_account, document_field, score | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| DM | RWB-DM-012 | Minor | Migrate decision log | recovery_case, loan_account, document_field, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| DM | RWB-DM-013 | Rewrite | Migrate money and closure | recovery_case, loan_account, document_field | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| DM | RWB-DM-014 | Minor | Migrate reference data | recovery_case, loan_account, document_field, lov_value | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-001 | Rewrite | Recovery tables for the 14 data products | recovery_case, case_account, case_party, deviation, queue, assignment, task, timer, party, contact_point, loan_account, account_payment, collateral, account_collateral, valuation, asset, treatment, guarantee_claim, legal_action, notice, hearing, partner, partner_instruction, listing, asset_sale, debt_sale_lot, debt_sale_account, interaction, document, document_field, document_custody, decision_log | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-002 | Rewrite | Case list v1 with case ID, owner and queue | recovery_case, case_account, queue, loan_account, case_list_row, load_run, dq_exception | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-003 | Remove | ALS daily extract load | loan_account, account_payment, load_run, dq_exception, source_field_map, source_code_map, lov_value | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-004 | Remove | EFS extract load | loan_account, collections_history, source_field_map, source_code_map, load_run, dq_exception, data_product_load, case_list_row | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-005 | Remove | Excel and SharePoint inventory | tracker_inventory, data_product, lov_value | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-006 | Remove | Data quality rules v1 | loan_account, account_payment, party, contact_point, account_collateral, case_list_row, dq_rule, dq_exception, load_run | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-007 | Rewrite | Integration adapters for file loads and outbound files | interface_config, interface_run, outbound_item, processed_event, recovery_case, task, role | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-008 | No impact | Decision log store v1, append only and hash chained | decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-009 | Remove | CCMS and SVAF loads | collateral, account_collateral, valuation, loan_account, load_run, dq_exception, data_product_load | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-010 | Remove | Excel and SharePoint loads | loan_account, tracker_inventory, tracker_row, load_run, dq_exception | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-011 | Rewrite | Reconciliation and data quality report | loan_account, case_list_row, reconciliation_result, dq_exception, load_run | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-012 | Remove | Retire local copies | tracker_inventory, lov_value | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-013 | Minor | Baseline measures | recovery_case, queue, case_account, account_payment, measure_definition, measure_snapshot | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-014 | Minor | Decision log copy to the data lake | decision_log_entry, lake_copy_watermark, retention_rule \|\| load words: job-13 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-015 | Rewrite | Freshness stamp per data product | loan_account, account_payment, decision_log_entry, data_product, data_product_load | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-016 | Rewrite | Access control per data product and catalog entries | party, contact_point, role, permission, sys_fields, data_product, data_product_access, retention_rule | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-017 | Minor | Retention and archive rule for the data store | recovery_case, interaction, retention_rule | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-018 | Rewrite | Case ID issuance and case record v1 | recovery_case, case_account, case_party, loan_account, party, case_entry_exclusion, rule_row, lov_value, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-019 | Minor | Roles, teams and queues as data | queue, queue_member, reference_version, reference_row, role, lov_value, recovery_case \|\| load words: file load | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-020 | Minor | Allocation and assignment engine v1 | recovery_case, queue, queue_member, assignment, rule_row, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-021 | No impact | Transfer rules and engine v1 | recovery_case, queue, assignment, rule_row, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-022 | No impact | Sign-on with SSO, MFA and the first roles | role, permission, role_conflict | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-023 | Rewrite | Case record view v1, read only | recovery_case, case_account, case_party, loan_account, party, interaction, document, queue | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-024 | No impact | Document store and index | recovery_case, document, document_field, document_type, document_hub_parameter, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-025 | Minor | Document types and fields agreed | document_type \|\| load words: load from | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-026 | No impact | Attach and search screen | recovery_case, document, document_type, document_hub_parameter, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-027 | Minor | Decision log writer v1 | decision_log_entry, lov_value \|\| load words: job-02,job-03 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-028 | Minor | Service levels, timers, escalation and prescription dates | recovery_case, case_account, loan_account, queue, timer, reference_row, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-029 | No impact | Rule load, validation and rollback | rule_row, reference_version, recovery_case, lov_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-030 | Minor | Daily rebalancing and queue measures | recovery_case, queue, queue_member, assignment, timer, queue_measure, decision_log_entry \|\| load words: job-06 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-031 | No impact | Queue and owner on the case list with filters | recovery_case, queue | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-032 | Minor | Automatic attach from the OCR intake | recovery_case, case_account, loan_account, document, document_intake, document_text, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-033 | No impact | Search across cases | recovery_case, document, document_field, document_text, document_type, document_hub_parameter | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-034 | No impact | Letter template management | template, merge_field | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-035 | No impact | Case record view v1.1 with documents and history timeline | interaction, assignment, document, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-037 | Rewrite | Role to permission matrix as data and PDPA field masking by role | permission, role, masking_rule, party, contact_point, recovery_case, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-038 | No impact | Delegation of authority table as reference data | delegation_limit, lov_value, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-039 | No impact | Access log into the decision log and break-glass admin | decision_log_entry, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-040 | No impact | Document checklist per case type as reference data | recovery_case, document, document_checklist_item, case_document_check, document_type | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-041 | Minor | Retention classes and virus scan on intake | document, recovery_case, document_intake, retention_rule, retention_action, decision_log_entry \|\| load words: job-12,job-17 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-042 | No impact | Central configuration service and parameter catalog | parameter_catalog, parameter_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-043 | Minor | Reference data service with versioned tables | reference_version, reference_row, lov_value | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-044 | Minor | Database migrations versioned with parameterized schema names |  | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-045 | Minor | Multi-product parameters for Mortgage, HP and SSME | recovery_case, timer, reference_version, reference_row, parameter_catalog | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-046 | No impact | Template and merge field catalog as data | template, merge_field, lov_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-047 | No impact | Feature flags for module release with a removal date | feature_flag, feature_flag_change, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-048 | No impact | Rule change audit report | reference_version, reference_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-049 | Minor | OCR pipeline on the Workbench document hub | document, recovery_case, document_intake, document_text, document_hub_parameter \|\| load words: job-12 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-050 | Minor | Document classification | document_intake, document_text, document_type, document_hub_parameter, document \|\| load words: job-12 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-051 | Remove | Legacy feed jobs on ADF and Control-M | interface_config, interface_run, loan_account, collateral, valuation | Move the story to the register appendix; record its later home. |  | Not started |  |
| E1 | RWB-E1-052 | Rewrite | Notice generation v1 | recovery_case, case_party, party, contact_point, loan_account, template, merge_field, document, notice, task, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-053 | No impact | Field extraction for the six types into the index | document, document_field, document_intake, document_text, document_type, document_hub_parameter | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-054 | No impact | Review queue for low-confidence documents | recovery_case, document, document_field, document_intake, document_text, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-055 | Minor | Proof of delivery capture design with WIN | notice, case_account, loan_account, contact_point, template, interaction | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-056 | Rewrite | Run books and monitoring for every Epic 1 job | job_catalog, interface_run, role | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-057 | Minor | Intake from branches, mailroom, partner SFTP and email | partner, document_intake, document_hub_parameter \|\| load words: job-12 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-058 | No impact | Agent platform set-up [E1a] | recovery_case, rule_row, agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run, agent_evaluation | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-059 | Minor | Case intake agent in shadow [E1b] | recovery_case, document, valuation, contact_point, agent_run, agent_sample, agent_evaluation_run, agent_evaluation | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-060 | No impact | Extraction evaluation [E1c] | document, document_field, agent_sample, agent_run, agent_evaluation_run, agent_evaluation | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-061 | No impact | Intake agent evaluation and L1 proposal [E2a] | agent_evaluation_run, agent_evaluation, agent_run, agent_policy | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-062 | No impact | Deviation screening agent in shadow [E2b] | recovery_case, deviation, interaction, document, document_field, rule_row, agent_run, agent_sample, agent_evaluation, agent_evaluation_run | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-063 | Minor | Agent monitoring dashboard v1 [E2c] | agent_run, agent_policy, agent_evaluation, agent_alert \|\| load words: job-15 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E1 | RWB-E1-064 | Rewrite | Data dictionary for the 14 data products | sys_objects, sys_fields, sys_field_version, data_contract, data_product | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-065 | Rewrite | Sandbox database with synthetic recovery data | recovery_case, case_account, case_party, deviation, party, contact_point, loan_account, account_payment, collateral, account_collateral, valuation, interaction, document, document_field, score, role, permission, lov_value, sys_fields | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E1 | RWB-E1-066 | No impact | Interaction ledger store and writer | interaction, recovery_case, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-067 | No impact | Every Workbench action into the interaction ledger | interaction, recovery_case, assignment, document, decision_log_entry, processed_event | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-068 | Minor | Interaction ledger read interface | interaction, recovery_case \|\| load words: int-07 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-001 | Rewrite | EFS hand-over with full history from the COLLINS load | loan_account, party, recovery_case, case_account, interaction, decision_log_entry, processed_event | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E2 | RWB-E2-002 | Minor | ACE plan status on the case | recovery_case, case_account, loan_account, task, rule_row, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-003 | Rewrite | Customer's other products on the case | recovery_case, case_party, case_account, party, party_product, role | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E2 | RWB-E2-004 | No impact | Treatment entity and plan timers data model | treatment, timer, recovery_case, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-005 | No impact | Decision log query API for audit | decision_log_entry, recovery_case | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-006 | Minor | Credit approval pack for NLEADS | recovery_case, loan_account, collateral, valuation, document, treatment, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-007 | Rewrite | Booking confirmation from the ALS load | treatment, case_account, loan_account, task, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E2 | RWB-E2-008 | Rewrite | Payment matching with the missed payment event | account_payment, loan_account, case_account, treatment, proceeds, payment_match_rule | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E2 | RWB-E2-009 | Minor | Steering dashboard v1 data set | recovery_case, queue, treatment, notice, decision_log_entry, measure_definition, measure_snapshot, measure_publish \|\| load words: int-19,job-15 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-010 | Rewrite | Stage 2 data products: contracts, plans and treatments | treatment, guarantee_claim, loan_account, dp_treatment, dp_guarantee_claim, data_product_load | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E2 | RWB-E2-011 | Minor | Queue view screens: my queue, team queues, filters and ageing | recovery_case, queue, timer \|\| load words: collins load | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-012 | No impact | Manual transfer and reassignment screen with reason | recovery_case, queue, assignment, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-013 | Minor | Approval routing with the delegation of authority table | approval, delegation_limit, task, timer, decision_log_entry \|\| load words: job-05 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-014 | Minor | Approval screen for D7.1 demand and recall notices | notice, recovery_case, loan_account, contact_point, approval, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-015 | No impact | Timers, escalation and the deviation flag on the case record view | recovery_case, timer, task, deviation, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-016 | No impact | Full case record view with the history timeline | recovery_case, queue, assignment, interaction, timer, decision_log_entry, document, notice | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-017 | No impact | Contract, CA and mortgage document generation screens | recovery_case, treatment, template, document, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-018 | Minor | E-signature flow for customers and the bank | recovery_case, party, treatment, signature_request, document, template | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-019 | No impact | Partner identities through the external gateway | partner_user, partner, partner_instruction, role, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-021 | Minor | Letter dispatch loop with proof of delivery from WIN | notice, recovery_case, deviation, contact_point, interaction, timer, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-022 | Minor | SMS and LINE dispatch through NSS and LINE OA | recovery_case, deviation, contact_point, template, interaction, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-023 | Remove | Automated EFS file load | loan_account, case_account, recovery_case, interface_run, interface_signoff, feature_flag | Move the story to the register appendix; record its later home. |  | Not started |  |
| E2 | RWB-E2-024 | No impact | Field app photos and bills into the document hub | recovery_case, document, document_field, document_type, document_hub_parameter, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-025 | No impact | Extraction for the stage 2 and 3 document types | document, document_field, document_intake, document_type, document_hub_parameter | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-026 | Minor | Document generation engine for contract, CA and mortgage templates | recovery_case, treatment, party, collateral, template, document, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-027 | Minor | Payment matching rules with the data team | account_payment, loan_account, treatment, proceeds, payment_match_rule, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-028 | Minor | Case intake agent live at L1 [E3a] | recovery_case, assignment, document, decision_log_entry, agent_run, agent_feedback \|\| load words: job-15 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-029 | Minor | Deviation screening agent evaluation and L1 on one segment [E3b] | recovery_case, deviation, assignment, valuation, decision_log_entry, agent_run, agent_feedback, agent_policy, agent_evaluation | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-030 | No impact | Legal document agent in shadow on Epic 1 data [E3c] | recovery_case, legal_action, document, document_field, agent_run, agent_sample, agent_evaluation, agent_policy | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-031 | Minor | Agent monitoring dashboard v2 [E3d] | decision_log_entry, agent_run, agent_feedback, agent_policy, agent_alert \|\| load words: job-15 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-032 | Minor | TDR offer-suggestion model through the model gateway [E3e] | treatment, loan_account, account_payment, decision_log_entry, agent_policy, agent_run | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-033 | No impact | Case and queue list with status, owner and ageing | recovery_case, queue, timer, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E2 | RWB-E2-034 | Rewrite | Interaction ledger on the case and from every channel | interaction, recovery_case, case_account, contact_point, notice, partner, treatment, proceeds, loan_account | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E2 | RWB-E2-035 | Minor | Next action on the case | recovery_case, queue, task, rule_row, role, decision_log_entry \|\| load words: job-05 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E2 | RWB-E2-036 | No impact | Queue write interface for models and agents | recovery_case, queue, assignment, decision_log_entry, permission | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-001 | No impact | Create the treatment record | recovery_case, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-002 | No impact | Offer a settlement inside the range | recovery_case, assignment, timer, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-003 | No impact | Approve a settlement below the floor | recovery_case, assignment, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-004 | No impact | Offer a TDR plan | recovery_case, assignment, timer, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-005 | No impact | Pre-assess affordability through ACE | recovery_case, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-006 | Minor | Calculate the plan installment | recovery_case, loan_account, treatment, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-007 | Minor | Send the offer and start the validity timer | recovery_case, assignment, timer, party, treatment, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-008 | Minor | Route the signed offer to operations for booking | recovery_case, party, account_payment, treatment, partner_instruction, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-009 | Minor | Return the case to its prior status on no signature | recovery_case, party, treatment, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-010 | Rewrite | Book the plan and set the schedule | recovery_case, timer, loan_account, account_payment, treatment, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E38 | RWB-E3-011 | Minor | Detect and handle a broken plan | recovery_case, account_payment, treatment, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-012 | Minor | Run a deed in lieu to ownership transfer | recovery_case, assignment, party, asset, treatment, document | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-013 | Minor | Check encumbrance and eligibility before negotiation | recovery_case, assignment, task, collateral, asset, treatment | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-014 | No impact | Unlock the asset as a non performing asset by rule | recovery_case, assignment, asset, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-015 | Minor | Capture the collateral inspection in the field | recovery_case, party, collateral, treatment, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-016 | Minor | Set up a deed in lieu buy-back rental | recovery_case, party, treatment, decision_log_entry, proceeds, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-017 | Rewrite | Release the collateral after settlement | recovery_case, loan_account, account_payment, collateral, treatment, decision_log_entry | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E38 | RWB-E3-018 | Minor | Generate the treatment document set | recovery_case, assignment, party, treatment, document, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-019 | No impact | Take a repossessed vehicle onto the books | recovery_case, timer, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-020 | No impact | Take a property onto the books after a deed in lieu | recovery_case, assignment, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-021 | No impact | Take a property onto the books after an LED auction | recovery_case, assignment, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-022 | Minor | Serve the statutory notice and prove delivery | recovery_case, task, contact_point, asset, notice, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-023 | No impact | Track holding age against the provision steps | recovery_case, timer, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-024 | Minor | Record and track the asset stock balance | recovery_case, assignment, loan_account, asset, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-025 | No impact | Maintain a held property | recovery_case, asset, document_custody, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-026 | Minor | Re-appraise a held asset on cycle | recovery_case, valuation, asset, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-027 | No impact | Recommend the disposal route | recovery_case, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-028 | Minor | Set the start and floor price | recovery_case, valuation, asset, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E3-029 | No impact | Publish the listing | recovery_case, deviation, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-030 | No impact | Change an autonomy level | decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E3-031 | Minor | Detect model drift and raise a decision | assignment, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-001 | Minor | Order an appraisal when the last one is stale | valuation, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-002 | Rewrite | Receive the appraisal value from SVAF | collateral, valuation, decision_log_entry, rule_row | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E38 | RWB-E4-003 | Minor | Flag appraisal outliers against market and last value | valuation, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-004 | Minor | Accept the appraisal value | recovery_case, assignment, valuation, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-005 | Minor | Call COLLINS for return by route | decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-006 | Rewrite | Calculate the payoff and settlement range | loan_account, treatment, decision_log_entry, rule_row | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E38 | RWB-E4-007 | Minor | Score the routes and recommend one with reasons | decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-008 | No impact | Approve a route inside the limit | recovery_case, assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-009 | No impact | Approve a route above the limit at committee | recovery_case, assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-010 | No impact | Hold the case and set a review date | recovery_case, assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-011 | Minor | Reconsider the route after new information | deviation, account_payment, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-012 | No impact | Start the route flow and set its timers | task, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-013 | No impact | Prepare a TCG guarantee claim | recovery_case, timer, guarantee_claim, document, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-014 | Minor | Submit the claim to the TCG portal | recovery_case, timer, loan_account, guarantee_claim, document, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-015 | Minor | Track the claim to payment | recovery_case, timer, account_payment, guarantee_claim, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-016 | Minor | Record the subrogation position | recovery_case, case_party, timer, account_payment, guarantee_claim, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-017 | Minor | Notify guarantors and co-borrowers | recovery_case, case_party, timer, party, guarantee_claim, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-018 | Minor | Negotiate with a guarantor | recovery_case, case_party, assignment, timer, party, guarantee_claim | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-019 | Minor | Close the case when a guarantee clears the debt | recovery_case, timer, loan_account, account_payment, guarantee_claim, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-020 | Minor | File an insurance claim on a collateral event | timer, collateral, valuation, guarantee_claim, document, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-021 | No impact | Evict occupants from a held property | recovery_case, assignment, asset, partner_instruction, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-022 | Minor | Run the descending price schedule | recovery_case, valuation, asset, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-023 | Minor | Allocate the asset to an auction vendor by distance | recovery_case, assignment, asset, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-024 | Minor | Run auction rounds and report bids | recovery_case, account_payment, asset, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-025 | No impact | Accept a bid below the floor with a second signature | recovery_case, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-026 | No impact | Re-list on no bid | recovery_case, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-027 | Minor | Enforce the five-day payment term | recovery_case, account_payment, asset, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-028 | No impact | Transfer vehicle registration | recovery_case, assignment, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-029 | No impact | Record a property transfer at the Land Office | recovery_case, assignment, asset, document, document_custody, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-030 | Minor | Apply proceeds and raise the shortfall | recovery_case, loan_account, asset, decision_log_entry, proceeds, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-031 | No impact | Transfer a pool to RAMC or the joint venture | recovery_case, assignment, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-032 | Minor | Arrange a customer buy-back | recovery_case, deviation, assignment, party, asset, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-033 | Minor | Rent a held asset to a third party | recovery_case, party, loan_account, asset, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-034 | No impact | Sell through a broker | recovery_case, asset, decision_log_entry, rule_row, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-035 | Minor | View the offer on LINE and web | party, treatment, notice, decision_log_entry, rule_row, template | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-036 | Minor | Accept an offer in self-service | recovery_case, party, treatment, notice, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-037 | Minor | Pay in self-service | party, treatment, notice, decision_log_entry, rule_row, template | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-038 | Minor | Raise a dispute in self-service | deviation, party, notice, decision_log_entry, rule_row, template | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-039 | Minor | Maintain the contact repository | party, contact_point, notice, decision_log_entry, rule_row, template | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-040 | No impact | Record a custody movement of a document | notice, document, document_custody, decision_log_entry, rule_row, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-041 | No impact | Answer a legal or audit document request | notice, document, decision_log_entry, rule_row, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-042 | No impact | Apply retention on case closure | recovery_case, notice, document, decision_log_entry, rule_row, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E4-043 | Minor | Match a settlement payment | recovery_case, account_payment, treatment, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-044 | Minor | Match auction and enforcement proceeds | recovery_case, account_payment, decision_log_entry, proceeds, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-045 | Minor | Calculate fees and charges | recovery_case, account_payment, partner, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-046 | Rewrite | Post a settlement booking to ALS | recovery_case, loan_account, account_payment, treatment, decision_log_entry, rule_row | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E38 | RWB-E4-047 | Minor | Post to the general ledger | recovery_case, account_payment, treatment, interaction, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-048 | Minor | Run the deed in lieu rental auto-debit | recovery_case, loan_account, account_payment, decision_log_entry, proceeds, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-049 | Minor | Apply proceeds to the case balance | recovery_case, loan_account, account_payment, decision_log_entry, proceeds, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E4-050 | Rewrite | Reconcile money movements daily | recovery_case, loan_account, account_payment, interaction, decision_log_entry, rule_row | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| E38 | RWB-E5-001 | No impact | Issue demand and recall notices | recovery_case, notice, decision_log_entry, rule_row, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-002 | Minor | Record proof of delivery on a notice | recovery_case, timer, party, notice, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E5-003 | Minor | Run the notice period timer | recovery_case, timer, party, notice, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E5-004 | No impact | Assemble the litigation pack | recovery_case, task, legal_action, notice, document, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-005 | No impact | Check the pack against the defect list | recovery_case, document, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-006 | No impact | Recover a missing or lost document | recovery_case, document, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-007 | No impact | Verify the pack and approve filing | recovery_case, task, timer, legal_action, notice, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-008 | Minor | Select the law firm from the panel | recovery_case, partner, partner_instruction, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E5-009 | No impact | Instruct the firm through the portal | recovery_case, timer, partner, partner_instruction, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-010 | No impact | Record the court filing and receipt | recovery_case, timer, legal_action, document, decision_log_entry, proceeds | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-011 | No impact | Track hearings, deadlines and fees | recovery_case, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-012 | No impact | Recommend the next litigation step | recovery_case, task, legal_action, notice, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-013 | No impact | Settle before judgment | recovery_case, treatment, legal_action, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-014 | No impact | Decide and manage an appeal | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-015 | No impact | Pay court fees and legal expenses | recovery_case, timer, legal_action, document, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-016 | No impact | Record the judgment | recovery_case, task, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-017 | No impact | Trace assets for enforcement | recovery_case, asset, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-018 | No impact | Apply for the writ and seizure | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-019 | No impact | Follow the LED auction ladder | recovery_case, assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-020 | No impact | Record an enforcement deferral with its reason | recovery_case, queue, assignment, task, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-021 | No impact | File a bankruptcy petition | recovery_case, document, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-022 | Minor | Match enforcement proceeds to the case | recovery_case, loan_account, account_payment, decision_log_entry, proceeds, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E5-023 | No impact | Select eligible accounts for sale by rule | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-024 | No impact | Build the lots and estimate the price | decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-025 | No impact | Prepare the masked data tape | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E5-026 | No impact | Open the buyer data room | decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-001 | No impact | Approve lots, reserve and tiered terms | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-002 | No impact | Qualify a buyer against KYC and licensing | recovery_case, decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-003 | No impact | Bar a buyer that fails qualification | recovery_case, decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-004 | No impact | Take buyer bids | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-005 | Minor | Award the lot and test the price | recovery_case, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-006 | Minor | Generate the sale agreement and notices | recovery_case, party, notice, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-007 | No impact | Transfer the data to the buyer | recovery_case, assignment, treatment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-008 | Minor | Derecognize and post to the general ledger | recovery_case, loan_account, interaction, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-009 | No impact | Handle a buyer put-back claim | recovery_case, assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-010 | No impact | Close a case awarded in a sold lot | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-011 | Minor | Confirm buyer remittance | recovery_case, assignment, account_payment, treatment, decision_log_entry, score | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-012 | No impact | Apply the debt sale cap | decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-013 | No impact | Run the monthly eligibility scan on both tracks | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-014 | No impact | Apply the tax criteria | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-015 | Minor | Prepare the write-off pack | recovery_case, loan_account, asset, document, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-016 | No impact | Remove a case from the proposed population | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-017 | No impact | Route the population to the committee and schedule it | recovery_case, deviation, queue, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-018 | No impact | Approve a write-off inside the limit | recovery_case, decision_log_entry, rule_row, delegation_limit | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-019 | No impact | Reject a write-off | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-020 | No impact | Defer a write-off | recovery_case, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-021 | Minor | Post an approved write-off | recovery_case, loan_account, asset, interaction, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-022 | No impact | Send provision inputs to Finance | recovery_case, document, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-023 | No impact | Reconcile the approved and posted populations | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-024 | No impact | Work the write-off exception loop | recovery_case, assignment, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-025 | No impact | Close the case after the retention period | recovery_case, timer, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-026 | No impact | Change the eligibility or tax criteria | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-027 | Minor | Record a customer payment after charge-off | recovery_case, party, loan_account, account_payment, partner, decision_log_entry | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-028 | No impact | Sell a post charge-off population | recovery_case, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-029 | No impact | Onboard a partner and set terms | timer, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-030 | No impact | Hold the partner panel and fee schedule as data | timer, partner, decision_log_entry, rule_row, lov_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-031 | Minor | Allocate work by measured return | assignment, partner, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-032 | No impact | Override an allocation with a reason | assignment, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-033 | No impact | Receive a partner result into the case | recovery_case, partner, interaction, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-034 | No impact | Place a charged-off account with an agency | partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-035 | No impact | Match a recovery and calculate the agency fee | recovery_case, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E6-036 | Minor | Produce provision inputs | recovery_case, account_payment, asset, decision_log_entry, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E6-037 | Minor | Track benefit realisation | decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E7-001 | No impact | Run X1 dispute and complaint end to end | deviation, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-002 | No impact | Run X2 vulnerability and hardship end to end | recovery_case, deviation, queue, assignment, timer, decision_log_entry | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-003 | Minor | Run X3 deceased customer end to end | recovery_case, deviation, assignment, timer, party, document | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E7-004 | No impact | Run X4 fraud end to end | recovery_case, deviation, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-005 | No impact | Run X5 bankruptcy and seizure end to end | recovery_case, deviation, assignment, timer, legal_action, document | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-006 | No impact | Run X6 lost contact and skip trace end to end | deviation, timer, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-007 | Minor | Run X7 collateral event end to end | recovery_case, deviation, assignment, timer, collateral, valuation | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E7-008 | No impact | Review an override | deviation, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-009 | No impact | Match a complaint to the preceding contact | deviation, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-010 | No impact | Handle a contact sent while a block is on | deviation, timer, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-011 | Minor | Score partners monthly | partner, decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E7-012 | No impact | Approve partner fees | partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-013 | No impact | Hold a partner review | partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-014 | No impact | Issue a notice on a missed target | notice, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-015 | No impact | End a partner contract and recall the work | recovery_case, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-016 | No impact | Check partner conduct | partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-017 | No impact | Manage extra costs and services on an asset | asset, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E7-018 | No impact | Capture field work through the field app | recovery_case, partner, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-001 | No impact | Produce regulatory returns | document_field, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-002 | No impact | Classify, stage and re-age an account | document_field, decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-003 | Minor | Run a champion and challenger test | decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E8-004 | No impact | Raise or lower an autonomy level with approval | decision_log_entry, rule_row | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-005 | Minor | Review agent risk at the committee | decision_log_entry, score, rule_row | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| E38 | RWB-E8-006 | No impact | Run the full administration screens | queue, decision_log_entry, rule_row, role, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-007 | No impact | Change a decision rule through the administration screens | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-008 | No impact | Move an approval limit | decision_log_entry, rule_row, delegation_limit, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-009 | No impact | Set the treatment policy by product | treatment, decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-010 | No impact | Add a letter template with Compliance approval | notice, decision_log_entry, rule_row, role, template | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-011 | No impact | Roll back a configuration version | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-012 | No impact | Publish a panel change | partner, decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-013 | No impact | Run a QA sample against the rule version applied | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-014 | No impact | Return a defective pack | assignment, decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-015 | No impact | Detect a broken hash chain in the decision log | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-016 | No impact | Handle a data subject request | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-017 | No impact | Manage an incident | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-018 | No impact | Refer a case to Aric | recovery_case, decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E38 | RWB-E8-019 | No impact | Control access by role and by agent | decision_log_entry, rule_row, role | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-001 | Rewrite | Recovery module folder and boundary test |  | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| TE | RWB-TE-002 | No impact | Code owners for the recovery module |  | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-003 | No impact | Types and contract tests from the API specification |  | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-004 | Rewrite | Masked data in SIT and UAT | party, contact_point, loan_account, account_payment, recovery_case, case_party, interaction, sys_fields | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| TE | RWB-TE-005 | No impact | Rule table test harness | rule_row, rule_test_case | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-006 | Minor | Outbox and retry for outbound work | outbox_event, outbox_delivery, task, decision_log_entry, recovery_case \|\| load words: job-11 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| TE | RWB-TE-007 | Rewrite | Scheduled jobs on Quartz |  | Rewrite around views and business keys; update Entities, Gherkin and test data. |  | Not started |  |
| TE | RWB-TE-008 | Minor | Decision log hash chain check | decision_log_entry \|\| load words: job-13,job-14 | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| TE | RWB-TE-009 | No impact | Performance test harness | recovery_case, queue, interaction | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-010 | No impact | Browser and accessibility tests | recovery_case, role, lov_value | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-011 | Minor | PDPA lint for code, tests and logs | party, contact_point, interaction, document_field | Find-and-replace entity and field names; check every reference resolves. |  | Not started |  |
| TE | RWB-TE-012 | No impact | Document storage containers | document | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| TE | RWB-TE-013 | No impact | Agent runtime client with fallback | recovery_case, rule_row, decision_log_entry, agent_policy, agent_run | No edit. Confirm at the Wave 5 sweep. |  | Not started |  |
| E1 | RWB-E1-069 | New | Read-only ACE source views, grants and boundary rule | v_ace_* views, party_ext, contact_point_ext, account_ext, valuation_ext | Write the story, its ACs and its tests. |  | Not started |  |
| ACE | RWB-ACE-001 | New | ACE DB additions for the Recovery Workbench | ace_batch_run, valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product | Write the story from the gap list; ACE team owns it. | ACE team | Not started |  |

## Decisions

| ID | Decision | Effect | Status | Owner | Note |
|---|---|---|---|---|---|
| U1 | No inbound source loads in the Workbench | All source data lands in ACE through ACE ingestion, including SVAF and CCMS. The Workbench only reads ACE. | Agreed | Recovery tech lead with data architect | Record as D-RCV-35. |
| U2 | The ACE team owns the new ACE tables and columns | One new story, RWB-ACE-001, lists every new table and column with its field appendix. | Agreed | ACE team lead | Critical path for 30 November. |
| U3 | Workbench fields ACE lacks go into extension tables | Four 1:1 tables keyed by ACE business keys. Existing ACE tables are never altered by the Workbench. | Agreed | Recovery tech lead |  |
| U4 | Read path is read-only views | recovery.v_ace_* SELECT-only views map names and types. No FK into ACE because ACE cascades deletes on account. | Agreed | Data architect | 26 views; two migrations. |
| U5 | Excel and SharePoint trackers leave system scope | Retirement handled in the Cutover plan; six teams retire their trackers. | Agreed | Product owner |  |
| D-RCV-35 | Decision log entry for U1 to U5 | Supersedes DT12, DL06 option A and DL12 option A; amends DL20 and D-RCV-29. | To record | Recovery tech lead | Decision Log v9. |
| ADR-010 | Read source data from the ACE database through read-only views | Supersedes ADR-005; updates ADR-001 consequences. | To record | Solution architect | ADR v2. |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and dates? | The critical-path dependency for the 30 November release. | Open | ACE team lead | Decision Log v9. |
| R4-note | Ruling R4 definitions still hold | The 14 data_product definitions are seeded from the Conceptual Data Model v6; system of record re-worded ACE (from X). | To record | Data architect | Rulings v2. |
| GATE-1 | Sign-off: approve and start Wave 1 | U1 to U5 and the 30-view boundary accepted; Wave 1 released. | Agreed | Data architect / recovery tech lead / product owner | 15 Nov 2026. |
| GATE-2 | Sign-off: keep 30 views, one per ACE object family | No consolidation. Each ACE object family has one view, so the grant and the boundary test stay precise. | Agreed | Data architect | 15 Nov 2026. |
| GATE-3 | Sign-off: route NLEADS, EasyApp and Entra ID through ACE | The six fields move from Workbench-recorded to ACE-ingested. RWB-ACE-001 grows to 14 tables, 80 fields. | Agreed | Product owner with ACE team lead | 15 Nov 2026. |

## Defects found

| ID | Found in | Defect | Evidence | Fix | Size | Status |
|---|---|---|---|---|---|---|
| DEF-01 | Physical Schema v4.sql | No data_product seed rows, although D-RCV-29 and rulings R1 and R4 require 14. | The file does not load: the first sys_objects insert fails fk_sys_objects_data_product with DP03 not present. Reproduced in PostgreSQL 17. | Physical Schema v5 seeds the 14 data_product rows before sys_objects, with definitions from the Conceptual Data Model v6. | S | Open |
| DEF-02 | Physical Schema v4.sql | data_product.refresh_cycle is varchar(10) but its comment and the LDM use words such as On change and By versioned load. | A seed value of By versioned load fails with value too long for type character varying(10). | Widen to varchar(30) in v5 and seed the words from the comment. | S | Open |
| DEF-03 | Physical Schema v4.sql | 33 sys_objects rows carry OPS, AGT or RPT, which are not data products, and data_product is NOT NULL. | After the DEF-01 seed, the file still fails on data_product = OPS. Ruling R1 is not applied to v4. | Apply R1 in v5: data_product nullable, 33 rows NULL, FK created. | S | Open |
| DEF-04 | ACE workbook | Two tables carry no primary key: ace_case_accounts and batch_job_execution_params. | The Overview lists a blank primary key for both; the join tables rely on a unique index only. | No Workbench change. Recorded so the view conformance test does not assume a key. | S | Accepted |
| DEF-05 | Physical Schema v5 | 42 fields on retained tables still mirror an ACE column (hearing, legal_action, notice, write_off, asset_sale, proceeds and others). | The dictionary lists them with their old source system even though the owning story now reads the view. | Drop the column or declare it a Workbench snapshot, one story at a time. | M | Open |
| DEF-06 | Physical Schema v5 | case_list_row and case_entry_exclusion were UNIQUE (business_date). | One row per day in the whole table instead of one per case account. Found by E1-002 and E1-018. | Fixed in v5: (business_date, case_id, account_no) and (business_date, account_key). | S | Fixed |
| DEF-07 | Physical Schema v5 | dp_treatment and dp_guarantee_claim were UNIQUE (business_date). | One stage-2 snapshot row per day instead of one per treatment or guarantee claim. | Fixed in v5: (business_date, treatment_id) and (business_date, guarantee_claim_id). | S | Fixed |
