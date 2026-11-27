# RWB-ITG-W3 Wave 3 integration - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 176 |
| Cross-document (pending in another document) | 134 |
| Not applied (value not in the sources) | 2 |
| Open business decisions | 11 |
| Register gaps linked | 66 |
| Unconfirmed assumptions | 0 |
| Lint findings | 4 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E4001-ITG | 21 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E4001 ITG Order an appraisal when the last one is stale - integration v2.md |
| RWB-ITG-E4002-ITG | 19 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E4002 ITG Receive the appraisal value from SVAF - integration v2.md |
| RWB-ITG-E4045-ITG | 21 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E4045 ITG Calculate fees and charges - integration v2.md |
| RWB-ITG-E4046-ITG | 17 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E4046 ITG Post a settlement booking to ALS - integration v2.md |
| RWB-ITG-E4047-ITG | 21 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E4047 ITG Post to the general ledger - integration v2.md |
| RWB-ITG-E4050-ITG | 15 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E4050 ITG Reconcile money movements daily - integration v2.md |
| RWB-ITG-E5002-ITG | 16 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E5002 ITG Record proof of delivery on a notice - integration v2.md |
| RWB-ITG-E5009-ITG | 24 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG E5009 ITG Instruct the firm through the portal - integration v2.md |
| RWB-ITG-W3J01-ITG | 22 | 7 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W3 Wave 3 integration/RWB ITG W3J01 ITG Wave 3 journey end to end - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E5009-ITG | R-09494 | CG-ALL-926 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E4001-ITG, RWB-S1-E4001-APP, RWB-S1-E4001-CON | R-22773 | GAP-2592 | Register gap | P7 rwb-decision owner with the business owner of module S1 | No S1 rule package is in force and no source names the age limit's parameter or the rule row of this step | The rule and reference-data owner names the limit parameter and publishes the S1 package, or confirms that the limit stays a reference-data row; the record then carries that rule id and version with no change to the step. |
| RWB-ITG-E4047-ITG, RWB-P8-E4047-APP | R-22790 | GAP-2553 | Register gap | Business analyst, P8, with Finance | The posting entry set, the posting type mapping and the rule of the posting of a settlement or a sale route are in no read source | Hold the entry set and the posting type mapping as data of the ledger interface configuration, and publish the posting rule of the settlement and sale routes from the rule registry of rwb-decision |
| RWB-ITG-E4050-ITG, RWB-P8-E4050-APP | R-22796 | GAP-2561 | Register gap | P1 rwb-source-data owner with the P8 owner, the solution architect and the data product owner | The reconciliation_result owner and read, the rule set behind REC-04 and REC-05, the ACE product code and the local outcome record are not specified | Keep reconciliation_result, its rec_code, its business date and the reconciliation workflow with P1 as the map records them; have this service compute and record the payment side, read the owner's result through its contract and write no row outside rwb_payment; pin the product code and the two unnamed read operations in the contract registry at the wave 3 entry check. |
| RWB-ITG-E5002-ITG, RWB-P3-E5002-APP, RWB-P6-E5002-APP, RWB-S4-E5002-APP, RWB-S4-E5002-CON | R-22803 | GAP-2746 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case architect and the business owner of the notice period | The notice-period timer has no stated home and the notice period has no value in any source | Declare the proof window of 7 days and the notice period as two durable timers of LitigationWorkflow, the first started at dispatch and the second at delivered_at under R-LIT-07; read the notice period as a versioned reference row per product and notice type, carry its content as the placeholder until the business owner publishes it, hold the timer and answer no move when the row is missing, and keep the case-stage timer and the officer task rows with rwb-case on the stage outcome. |
| RWB-ITG-E5009-ITG, RWB-S4-E5009-APP, RWB-S4-E5009-CON | R-22811 | GAP-2783 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case and S9 rwb-partner architects and the business owner of the partner service levels | The partner clock of 2 working days has no stated home, and the working-day calendar and instruction types have no value in any source | Declare the partner clock as one durable timer of LitigationWorkflow of 2 working days started at instructed_at, measured on a working-day calendar read as a versioned reference row whose content is the placeholder; fire R-LIT-28 on expiry, answer FIRM_BREACHED_SLA to rwb-case with the partner-and-agency-manager task, mark the breach on the P9 contract and leave the re-selection to the firm-selection story; keep the case-stage timer and the task rows with rwb-case. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-ITG-E4001-ITG, RWB-S1-E4001-APP, RWB-S1-E4001-CON, RWB-S1-E4012-APP, RWB-S1-E4012-CON | R-28890 | GAP-1693 | Register gap | Product Owner | No approval is recorded for the requirements this PRD states | Keep the document at status Draft, leave the approval table empty, and treat the missing approval as an assumption rather than an answer; the gate is cleared by the Product Owner and the FDA after this run. |
| RWB-ITG-E4002-ITG, RWB-S1-E4002-APP, RWB-S1-E4002-CON, RWB-S1-E4011-APP, RWB-S1-E4011-CON | R-28893 | GAP-1692 | Register gap | Compliance and PDPA officer | The classification and retention of the valuation and route records are not set | Apply the working labels of this document (SENSITIVE_FINANCIAL for values and decisions, CONFIDENTIAL for the agent output) and state the retention period as open; the class sets handling and the period is set under DL26. |
| RWB-ITG-E4050-ITG, RWB-P8-E4050-APP | R-28900 | GAP-1490 | Register gap | Data steward and data product owner | The daily case list reconciliation has no variance tolerance | Report the variance by data product with no tolerance until DL25 is decided, and apply the agreed tolerance by version once it is set. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-W3J01-ITG | R-04200 | DOR-RWB-ITG-W3J01-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | Checked Service Epics v1, 05 architecture .md and 22 Realignment .md; no signed epic design record for RWB-ITG-W3 found (DOR-RWB-ITG-W3J01-ITG-14). |
| RWB-ITG-W3J01-ITG | R-04203 | DOR-RWB-ITG-W3J01-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | Checked Service Epics v1, 05 Technical architecture .md and 22 Microservice Realignment .md; no published contract fake library version found (DOR-RWB-ITG-W3J01-ITG-22). |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01862 | RWB-ITG-E4001-ITG | CG-ALL-859 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story, or consume a published operation per provider ruling. |
| CDC-01876 | RWB-ITG-E4002-ITG | CG-ALL-867 | 12.2 | Publish path POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |
| CDC-01879 | RWB-ITG-E4002-ITG | DOR-RWB-ITG-E4002-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise |
| CDC-01889 | RWB-ITG-E4045-ITG | CG-ALL-876 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story, or consume a published operation |
| CDC-01901 | RWB-ITG-E4046-ITG | CG-ALL-886 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml, or move the consumer to a published operation. |
| CDC-01907 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-8 | find it | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml. |
| CDC-01922 | RWB-ITG-E4047-ITG | CG-ALL-896 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer moves to a published operation (provider ruling). |
| CDC-01937 | RWB-ITG-E4050-ITG | CG-ALL-905 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation |
| CDC-01951 | RWB-ITG-E5002-ITG | CG-ALL-914 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer switches to a published operation. |
| CDC-01974 | RWB-ITG-E5009-ITG | CG-ALL-922 | 12.2 | Publish POST /api/recovery/access/v1/authorise (P4 rwb-access) through the provider's CON story so the path is present in rwb-access.yaml. |
| CDC-01976 | RWB-ITG-E5009-ITG | DOR-RWB-ITG-E5009-ITG-8 | 12 | Publish POST /api/recovery/access/v1/authorise (P4 rwb-access) through the provider's contract story so the path is present in rwb-access.yaml. |
| CDC-02319 | RWB-ITG-W3J01-ITG | CG-ALL-930 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access CON story, or the consumer switches to a published operation (provider ruling). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01874 | RWB-ITG-E4001-ITG | CG-ALL-863 | 18 | In its next version, align the test lists for REQ-RDF-004, REQ-DRI-007 and the third requirement in the evidence with section 18 of RWB-ITG-E4001-ITG. |
| CDC-01886 | RWB-ITG-E4002-ITG | CG-ALL-871 | 18 | Align the test lists for REQ-RDF-004, REQ-RDF-009 and REQ-DRI-001 with section 18 of RWB-ITG-E4002-ITG in its next version. |
| CDC-01900 | RWB-ITG-E4045-ITG | CG-ALL-880 | 18 | Align the test lists for REQ-CHO-009 and REQ-DRI-001 with section 18 of this story in the next RTM version |
| CDC-01912 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-12 | 16, 18 | Align the §18 test lists to RTM v7 for TC-E4-046-01 to 04-ITG and confirm AC2 is owned by RWB-P8-E4046-APP |
| CDC-01917 | RWB-ITG-E4046-ITG | CG-ALL-890 | 18 | Align the test lists of REQ-CHO-008, REQ-DRI-007 and the third differing requirement with section 18 of RWB-ITG-E4046-ITG in the next RTM version. |
| CDC-01929 | RWB-ITG-E4047-ITG | DOR-RWB-ITG-E4047-ITG-12 | 16, 18 | Align its test case lists for REQ-S2-008, REQ-S6-008, REQ-S7-005 and REQ-DRI-001 to section 18 of this story. |
| CDC-01933 | RWB-ITG-E4047-ITG | CG-ALL-900 | 18 | Align the REQ-DRI-001 test list with this story's §18 entries in the next RTM version. |
| CDC-01949 | RWB-ITG-E4050-ITG | CG-ALL-909 | 18 | Align its test lists for REQ-CHO-009, REQ-RDF-007, REQ-RDF-008 and the fourth requirement in the finding with RWB-ITG-E4050-ITG §18. |
| CDC-01969 | RWB-ITG-E5002-ITG | CG-ALL-918 | 18 | Align the test traces of the five requirements in CG-ALL-918 with section 18 of RWB-ITG-E5002-ITG in the next RTM version. |
| CDC-01980 | RWB-ITG-E5009-ITG | CG-ALL-925 | 18 | Align the test cases traced to REQ-DRI-001 and to the second differing requirement with RWB-ITG-E5009-ITG section 18 in its next version. |
| CDC-02323 | RWB-ITG-W3J01-ITG | DOR-RWB-ITG-W3J01-ITG-12 | 18 | Align the test case lists of RTM v7 with section 18 of RWB-ITG-W3J01-ITG. |
| CDC-02324 | RWB-ITG-W3J01-ITG | CG-ALL-933 | 18 | Align the test case lists for the 11 requirements with RWB-ITG-W3J01-ITG section 18 in the next RTM version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01868 | RWB-ITG-E4001-ITG | CG-ALL-861 | 16 | The story test case rows are in section 16. The Test Cases workbook needs rows TC-E4-001-01-ITG to TC-E4-001-04-ITG, plus the new TC-E4-001-05-ITG and TC-E4-001-06-ITG. |
| CDC-01881 | RWB-ITG-E4002-ITG | CG-ALL-869 | 16 | Add rows TC-E4-002-01-ITG to TC-E4-002-04-ITG to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-01891 | RWB-ITG-E4045-ITG | CG-ALL-878 | 16 | Add rows for TC-E4-045-01-ITG to TC-E4-045-04-ITG with Given, When and Then copied from the legacy criteria they cover |
| CDC-01910 | RWB-ITG-E4046-ITG | CG-ALL-888 | 16 | Add rows TC-E4-046-01-ITG to TC-E4-046-04-ITG to tab Story test cases, with Given, When and Then copied from the criteria they cover |
| CDC-01927 | RWB-ITG-E4047-ITG | CG-ALL-898 | 16 | In tab Story test cases add rows TC-E4-047-01-ITG to TC-E4-047-04-ITG and new TC-E4-047-05-ITG to TC-E4-047-07-ITG, with Given, When and Then copied from the criteria they cover. |
| CDC-01944 | RWB-ITG-E4050-ITG | CG-ALL-907 | 16 | Add rows TC-E4-050-01-ITG to TC-E4-050-04-ITG with Given, When and Then copied from the criteria they cover |
| CDC-01958 | RWB-ITG-E5002-ITG | CG-ALL-916 | 16 | Add rows TC-E5-002-01-ITG to TC-E5-002-06-ITG, with Given, When and Then copied from the criteria they cover. |
| CDC-01977 | RWB-ITG-E5009-ITG | CG-ALL-924 | 16 | Add rows for TC-E5-009-01-ITG, TC-E5-009-02-ITG, TC-E5-009-03-ITG, TC-E5-009-04-ITG, TC-E5-009-05-ITG and TC-E5-009-06-ITG, with Given, When and Then copied from the criteria they cover. |
| CDC-01979 | RWB-ITG-E5009-ITG | DOR-RWB-ITG-E5009-ITG-12 | section 16 | Section 16 now lists 11 test cases, including new 07 to 11 for AC7 to AC11. Story side done for the new rows; the workbook rows are still to be added. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01869 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-1 | 1 | Add or map the role 'member of the integration and QA team' to a role code or role name, so section 1 names a role that exists. |
| CDC-01882 | RWB-ITG-E4002-ITG | DOR-RWB-ITG-E4002-ITG-1 | 1 | Confirm the role code for the integration and QA team and add it if absent; section 1 then uses that role name. |
| CDC-01892 | RWB-ITG-E4045-ITG | DOR-RWB-ITG-E4045-ITG-1 | 1 | Add a role code and name for the integration and QA team that the section 1 story role refers to, then map the story role to it. |
| CDC-01911 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-1 | 1 | Confirm or add a role code or role name for 'member of the integration and QA team', so §1 can name it |
| CDC-01928 | RWB-ITG-E4047-ITG | DOR-RWB-ITG-E4047-ITG-1 | 1 | Add a role for the integration and QA team, or name the existing role code it maps to; section 1 then cites that role. |
| CDC-01945 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-1 | 1 | Role phrase replaced with an explicit not-specified marker; the role code must be taken from Users Roles and Permissions v5 when supplied, so the item stays open across documents. |
| CDC-01959 | RWB-ITG-E5002-ITG | DOR-RWB-ITG-E5002-ITG-1 | 1 | Add a role code or role name for the integration and QA team, so section 1 can name it. |
| CDC-01978 | RWB-ITG-E5009-ITG | DOR-RWB-ITG-E5009-ITG-1 | 1 | Add a role code and name for the integration and QA team, or confirm an existing role code, so section 1 can cite it. |
| CDC-02322 | RWB-ITG-W3J01-ITG | DOR-RWB-ITG-W3J01-ITG-1 | 1 | Add a role code for the QA team that runs the integration harness, or name the existing role code that holds this right. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01863 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-E4001-ITG. |
| CDC-01877 | RWB-ITG-E4002-ITG | DOR-RWB-ITG-E4002-ITG-14 | n/a | Record the signed epic design sign-off |
| CDC-01902 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-E4046-ITG. |
| CDC-01923 | RWB-ITG-E4047-ITG | DOR-RWB-ITG-E4047-ITG-14 | header | Record the signed epic design sign-off for EP04 in the epic design record. |
| CDC-01938 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-14 | Metadata | Record the signed epic design sign-off for RWB-ITG-E4050-ITG. |
| CDC-01953 | RWB-ITG-E5002-ITG | DOR-RWB-ITG-E5002-ITG-14 | Header | Record the signed epic design sign-off for RWB-ITG-W3 in the epic design record. |
| CDC-01975 | RWB-ITG-E5009-ITG | DOR-RWB-ITG-E5009-ITG-14 | Header | Record the signed epic design for service epic RWB-ITG-W3 with its sign-off date and approver, so readiness item 14 can be evidenced against this story |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01870 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-12 | 16, 18 | Add TC-E4-001-01-ITG to TC-E4-001-04-ITG to Story test cases tab; align the section 18 test lists with RTM v7. |
| CDC-01883 | RWB-ITG-E4002-ITG | DOR-RWB-ITG-E4002-ITG-12 | 16, 18 | Add TC-E4-002-01-ITG to 04-ITG to v8 Story test cases; align the section 18 test lists with RTM v7. |
| CDC-01893 | RWB-ITG-E4045-ITG | DOR-RWB-ITG-E4045-ITG-12 | 16, 18 | Add rows TC-E4-045-01-ITG to TC-E4-045-04-ITG to Story test cases, and align section 18 test lists to the section 16 IDs in RTM v7. |
| CDC-01946 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-12 | 16; 18 | Add Given, When and Then for TC-E4-050-01-ITG to 04-ITG in Test Cases v8; align the test lists in section 18 with section 16 in RTM v7. Story side: TC-E4-050-02-ITG now covers the AC2 negative path only. |
| CDC-01952 | RWB-ITG-E5002-ITG | DOR-RWB-ITG-E5002-ITG-12 | 16, 18 | Add TC-E5-002-01-ITG to TC-E5-002-07-ITG to tab Story test cases; align the section 18 test lists to RTM v7. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01880 | RWB-ITG-E4002-ITG | CG-ALL-866 | 9 | Record order_age as a named object in its owning document, or use the dictionary name |
| CDC-01908 | RWB-ITG-E4046-ITG | CG-ALL-884 | 9 | Confirm the dictionary name for the amount received, or record the owning object for amount_received in its owning document. |
| CDC-01909 | RWB-ITG-E4046-ITG | CG-ALL-885 | 9 | Confirm the dictionary name for the settlement amount, or record the owning object for settlement_amount in its owning document. |
| CDC-01919 | RWB-ITG-E4046-ITG | GAP-2551 | find it | Record that the booking item is outbound_item in rwb_integration, that rwb_payment holds no booking row, and that the item reference on TreatmentBooked is the booking reference the case records. |
| CDC-01926 | RWB-ITG-E4047-ITG | CG-ALL-894 | 9, 13 | Record cumulative_received as a field, or name the owning object (index, library table, flag) in the owning document (Data). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01888 | RWB-ITG-E4045-ITG | CG-ALL-875 | 12.2 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments through the rwb-payment provider's CON story, or consume a published operation |
| CDC-01921 | RWB-ITG-E4047-ITG | CG-ALL-895 | 12.2 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments through the provider's CON story, or the consumer moves to a published operation (provider ruling). |
| CDC-01935 | RWB-ITG-E4047-ITG | GAP-2558 | 12.2 | Section 4 step 3 restored to the full payments operation the story consumes (CG-ALL-895); the ownership row in rwb-payment must be fixed. |
| CDC-01936 | RWB-ITG-E4050-ITG | CG-ALL-904 | 12.2 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments in rwb-payment.yaml through the provider's CON story, or consume a published operation |
| CDC-02318 | RWB-ITG-W3J01-ITG | CG-ALL-929 | 12.2 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments through the rwb-payment CON story, or the consumer switches to a published operation (provider ruling). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01872 | RWB-ITG-E4001-ITG | GAP-2589 | 12.7 | Add the S1 rwb-valuation table rows, and record the Workbench-owned acceptance and stale-flag fields as held in recovery.valuation_ext, the ACE-side data product, as the data owner confirms. |
| CDC-01873 | RWB-ITG-E4001-ITG | GAP-1679 | 12.7 | Add rows for rwb-valuation (schema rwb_valuation) covering valuations, D6 route decision and route agent output, stating entity groups and key fields without physical table names. |
| CDC-01885 | RWB-ITG-E4002-ITG | GAP-1682 |  | Keep POST /assets/{assetId}/valuations and POST /assets/{assetKey}/valuations with the service that writes the appraisal, so the appraisal record has one writer; rwb-asset reads the accepted appraisal through the contract for the floor price and monthly re-appraisal. |
| CDC-01898 | RWB-ITG-E4045-ITG | GAP-2545 | 7 | Publish a fee operation or a FeeCalculated event on rwb.payment.events.v1 with its CloudEvents envelope, key and ownership row |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01890 | RWB-ITG-E4045-ITG | DOR-RWB-ITG-E4045-ITG-8 | 12.2 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments in rwb-payment.yaml and POST /api/recovery/access/v1/authorise in rwb-access.yaml through provider CON stories |
| CDC-01925 | RWB-ITG-E4047-ITG | DOR-RWB-ITG-E4047-ITG-8 | 12.2, 12.4 | Publish GET .../cases/{caseId}/payments in rwb-payment.yaml and POST /api/recovery/access/v1/authorise in rwb-access.yaml via the provider's CON story. |
| CDC-01943 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-8 | Header, 12.2, 12.4 | Publish GET cases payments in rwb-payment.yaml and POST authorise in rwb-access.yaml through the provider CON stories |
| CDC-02321 | RWB-ITG-W3J01-ITG | DOR-RWB-ITG-W3J01-ITG-8 | 12.2, 12.4 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments in rwb-payment.yaml and POST /api/recovery/access/v1/authorise in rwb-access.yaml via CON stories. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01950 | RWB-ITG-E5002-ITG | CG-ALL-913 | 12.2 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/proof-of-delivery through the provider's CON story, or the consumer switches to a published operation. |
| CDC-20650 | RWB-ITG-E5002-ITG | R-00223 |  | Proof-of-delivery operation shapes and error envelopes not specified in the source documents (CG-ALL-913). |
| CDC-20651 | RWB-ITG-E5002-ITG | R-03979 |  | Proof-of-delivery shapes not specified in the source documents; authorise in rwb-access.yaml is not this file (DOR-RWB-ITG-E5002-ITG-8). |
| CDC-20652 | RWB-ITG-E5002-ITG | R-22555 |  | Proof-write shapes, notice facts, field IDs and reference rows not specified in the source documents (GAP-0437). |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01884 | RWB-ITG-E4002-ITG | DOR-RWB-ITG-E4002-ITG-7 | 11 | Add order_age as a field or entity, or confirm the field name the story should read in its place. |
| CDC-01913 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-7 | 11 | Add or map fields amount_received and settlement_amount, or name the existing LDM v9 fields they correspond to |
| CDC-01930 | RWB-ITG-E4047-ITG | DOR-RWB-ITG-E4047-ITG-7 | 11 | Add cumulative_received as a field or entity, or name the existing field the cumulative receipt reads; the story then uses that name. |

### OTHER:Contract registry (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01906 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-23 | 12.8 | Story uses registry-pinned versions and records them; the fixed version numbers are not in the source, so DoR 23 stays open. |
| CDC-01941 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-22 | Metadata | Record the published contract fake library version for the fakes in section 12.8. |
| CDC-01942 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-23 | Metadata | Record the contract version of RWB-ITG-E4050-CON that this story builds against. |

### RWB-S4-E5002-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01954 | RWB-ITG-E5002-ITG | DOR-RWB-ITG-E5002-ITG-21 | Header | Contract dependencies set to RWB-S4-E5002-CON |
| CDC-01955 | RWB-ITG-E5002-ITG | DOR-RWB-ITG-E5002-ITG-22 | Header | No fake library version is recorded in the sources; the story cannot supply it. |
| CDC-01962 | RWB-ITG-E5002-ITG | GAP-1189 | 12 | Name the proof-record operation with request (notice reference, case reference, delivery status, delivered or callback date, barcode where required), answer (outcome, rule ID, package version), error envelope and no-response answer. |

### OTHER:Contract story for the valuation and payoff contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01864 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-21 | header | The story names the contract and its fake. No contract story in the story set is identified, and publication happens outside this story. |
| CDC-01865 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-22 | header | No fake library version is in the source documents. The owner of the contract must publish and record it. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01866 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-23 | section header | Contract version recorded as not specified in the source documents; the contract owner must confirm and fix it. |
| CDC-01871 | RWB-ITG-E4001-ITG | GAP-2587 | header | The six row owners own the operation names. The story records them as pending in Open values. |

### RWB-ITG-E4002-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01878 | RWB-ITG-E4002-ITG | DOR-RWB-ITG-E4002-ITG-21 | Header | Contract publication belongs to the contract document; the header keeps None because RWB-ITG-E4002-CON is not a story key. |
| CDC-01887 | RWB-ITG-E4002-ITG | GAP-2595 |  | Publish v1 with the appraisal elements as one flat group inside Approval; take valuation_ext column types from TSD S1 T3.1; leave 404 and 409 wording as messageId slots; record retention as an open P3 item; publish via the platform registry. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01904 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-21 | Header | No contract story is allocated to this key in the source documents; the dependency row stays None, so DoR 21 stays open. |
| CDC-01916 | RWB-ITG-E4046-ITG | GAP-2548 | 12.8 | Allocate a service contract baseline publishing rwb.payment.TreatmentBooked.v1 (BACKWARD), the deliverFile manifest element set with booking branch, error envelope and fakes; publish ALS row values and the data product code. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01861 | RWB-ITG-E4001-ITG | CG-ALL-858 | 12.2 | Publish GET /api/recovery/integration/v1/interface-runs through the provider CON story, or consume a published operation per provider ruling. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01867 | RWB-ITG-E4001-ITG | DOR-RWB-ITG-E4001-ITG-8 | 12.2 | Publish GET interface-runs in rwb-integration.yaml and POST authorise in rwb-access.yaml per provider ruling. |

### OTHER:FSD S1 (document control and version table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01875 | RWB-ITG-E4001-ITG | GAP-1695 | 9 | Carry version 3 in full and mark versions 1 and 2 as not specified; FSD owner supplies the two change notes at the next FSD version. |

### OTHER:Recovery Workbench register and owner records (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01894 | RWB-ITG-E4045-ITG | GAP-0431 | 15 | Agree fee table owner, schedule tables, fee operation, v_ace_payment data product code and wave 3 harness pack with the named owners before the wave 3 entry check |

### OTHER:FSD P8 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01895 | RWB-ITG-E4045-ITG | GAP-2542 | 7 | The fee facts need to be published in FSD P8; this story cannot supply them. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P8 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01896 | RWB-ITG-E4045-ITG | GAP-2543 | 7 | Name the owner of the fee tables, publish the fee-row read with its version, and state in TSD P8 T3.1 whether any fee row is stored in rwb_payment |

### OTHER:FSD P8 v3; OTHER:TSD P8 v2 T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01897 | RWB-ITG-E4045-ITG | GAP-2544 | 7 | Publish the fee type list and fee rows with rate, cap, validity and version, and add the message for a fee type with no row in force |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:FSD P8 v3 A2.5.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01899 | RWB-ITG-E4045-ITG | GAP-2546 | 7 | Name the fee run and its activity, and state whether the trigger is the route owner fee-due event or the daily ACE batch completion |

### OTHER:Squad refinement (not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01903 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-16 | Header | Size is not set in the story; it remains a refinement action, so DoR 16 stays open. |

### OTHER:Contract registry / fake library (not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01905 | RWB-ITG-E4046-ITG | DOR-RWB-ITG-E4046-ITG-22 | 12.8 | Story reads the fake version from the registry and records it; the fake itself is not published, so DoR 22 stays open. |

### OTHER:FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01914 | RWB-ITG-E4046-ITG | GAP-0673 | 4 | Mark the INT-03 ALS booking line superseded for legacy key RWB-E4-046 with date and decision; load ALS interface_config row per environment after owner agreement. |

### OTHER:FSD P8 v3 A2.6 and the next split-plan version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01915 | RWB-ITG-E4046-ITG | GAP-2547 | 7 | Publish the FEAT-PAY-06 booking data set (case, treatment, account, accepted amount, business date, ALS interface) and add a requirement row for the slice. |

### OTHER:Recovery Workbench split plan (next version), lane L-P8-I C list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01918 | RWB-ITG-E4046-ITG | GAP-2550 | 10 | Add RWB-S2 treatment, RWB-P1 source-data, RWB-P2 integration and RWB-P3 case contract rows to the C list of this slice. |

### OTHER:Settlement route set and restructure rule rows (rules workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01920 | RWB-ITG-E4046-ITG | GAP-2552 | find it | Set the booking actor to rwb-payment's booking step after TreatmentApproved, and add the settlement counterpart of R-RES-23 with its state, message and owner role. |

### OTHER:Contract fake library (provider CON story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01924 | RWB-ITG-E4047-ITG | DOR-RWB-ITG-E4047-ITG-22 | header | Publish the contract fake library version and record the version in the story. |

### OTHER:P1 contract epic (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01931 | RWB-ITG-E4047-ITG | GAP-2555 | 12.8 | Publish the posting-reference read with payment code, business date, reference and batch status; confirm the GL and ALS reference mapping with the solution architect. |

### OTHER:rwb-integration interface configuration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01932 | RWB-ITG-E4047-ITG | GAP-2557 | 15 | Load the GL (INT-16) and ALS (INT-03) interface rows with their retry values and message text; keep MSG-P2-001 wording in the message standard. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01934 | RWB-ITG-E4047-ITG | GAP-2556 | 15 | No posting-result event is added in this run; the missing event is a Kafka Catalog gap, so the story keeps its consumed-event list unchanged. |

### OTHER:Backlog refinement (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01939 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-16 | Metadata | Size row records Not specified (DOR-RWB-ITG-E4050-ITG-16). |

### RWB-ITG-E4050-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01940 | RWB-ITG-E4050-ITG | DOR-RWB-ITG-E4050-ITG-21 | Header | Contract dependencies row records Not specified (DOR-RWB-ITG-E4050-ITG-21). |

### OTHER:Wave 3 entry check record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01947 | RWB-ITG-E4050-ITG | GAP-0436 | 12.8 | Agree and record the harness environment and pipeline, seeding set and fixtures, business date and ACE batch, product codes, evidence format and retention, gate name and thresholds, and the three unnamed operations with owners. |

### API:(service not named); OTHER:wave 3 entry check record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01948 | RWB-ITG-E4050-ITG | GAP-0434 | 4 | Add the reconciliation_result read operation, fields and result codes, the data product code for the three ACE views, the rwb-writeoff read operation and fields, and the rule package/IDs behind REC-04, REC-05, REC-06; name JOB-04 in the run environment. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01956 | RWB-ITG-E5002-ITG | DOR-RWB-ITG-E5002-ITG-8 | 12.2, 12.4 | Publish POST proof-of-delivery in rwb-comms.yaml and POST authorise in rwb-access.yaml through their CON stories. |

### OTHER:Recovery Workbench Business Requirements Program v5 (section 8 release plan and wave map R5.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01957 | RWB-ITG-E5002-ITG | GAP-1741 | 8 | Publish the notice contract, its fake and its schema as slice 2.1 before wave 3, and keep the EP02 wave 2 that R5.6 gives the notice stories. |

### RWB-S4-E5002-CON; OTHER:rwb-comms baseline; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:reference data; OTHER:TSD P6 and S4 appendices; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01960 | RWB-ITG-E5002-ITG | GAP-0437 | 12 | Publish the proof-record operation and notice proof write with paths, shapes and error envelopes; add notice state and three notice facts to LDM with field IDs; version LOV-DELIVERY mapping and notice-period and proof-window reference rows; record in P6 and S4 appendices that the v_ace_pod loop is Epic 2; attach requirement ID to FEAT-LIT-02 in EP05 PRD. |

### RWB-S4-E5002-CON; OTHER:EP05 PRD; OTHER:RWB-RCV reference data (SERVICE_LEVEL) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01961 | RWB-ITG-E5002-ITG | GAP-0737 | 12 | Confirm rwb-litigation answers delivery outcome on /api/recovery/litigation/v1; publish operation path and fields in RWB-S4-E5002-CON; add notice-period duration as SERVICE_LEVEL row owned by RW-COE; attach REQ ID to this feature in EP05 PRD. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:business owner and RW-COE (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01963 | RWB-ITG-E5002-ITG | GAP-1192 | 12 | Settle mapping rows for all four values including REFUSED and PENDING, and name the reference-data contract and version serving LOV-DELIVERY. |

### API:(service not named); RWB-S4-E5002-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01964 | RWB-ITG-E5002-ITG | GAP-1195 | 12.1 | Publish the proof write path, its request and answer fields and its Litigation C right once the S4 contract is settled. |

### OTHER:TSD S4 T-A.1; OTHER:rwb-source-data (P1) and rwb-comms (P6) contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01965 | RWB-ITG-E5002-ITG | GAP-2744 | 12 | Carry legacy sentences with origin tags; record target reading: proof via P1 ACE-data contract for v_ace_pod, notice read via P6 contract, service writes no business row, no sixth operation added. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:rwb-case (P3) contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01966 | RWB-ITG-E5002-ITG | GAP-2745 | 12 | Read PROOF_OF_DELIVERY_RECEIVED, PROOF_WINDOW_EXPIRED and DELIVERY_FAILED as workflow signals, not Kafka subscriptions; name the case read and case-stage answer in the rwb-case contract when written. |

### OTHER:Recovery Workbench Business Requirements Program v5 DL10 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01967 | RWB-ITG-E5002-ITG | GAP-1748 | 9 | Supply Thai wording, field-level text for MSG-GEN-001 and approver for MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-S4-001 and MSG-S4-002; keep English wording and IDs as in FSD. |

### OTHER:rwb-decision (P7) contract; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01968 | RWB-ITG-E5002-ITG | GAP-2748 | 12 | Carry the LITIGATION package read as a non-blocking consumed row on rwb-decision's contract with its fake; record DP-04 with its two contracts in the Dependency Map. |

### OTHER:Functional Specification Document P6 Communications v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01970 | RWB-ITG-E5002-ITG | GAP-1194 | none | Record that the officer-recorded path of this story is the manual correction path of the same notice; keep the automatic v_ace_pod read in RWB-P6-E2021-APP and RWB-P6-E1055-APP. |

### OTHER:split_plan.json (next plan revision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01971 | RWB-ITG-E5002-ITG | GAP-1191 | 12.2 | Add DP-11 to the pattern set of the RWB-E5-002 slices that consume or serve a contract at the next plan revision. |

### OTHER:Epics 3 to 8 PRD and FSD S4 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01972 | RWB-ITG-E5002-ITG | GAP-2747 | 18 | Add one requirement row for the proof of delivery as the start of the notice period, then rewrite the requirement column of both stories. |

### OTHER:Work plan WP B-P6-04 and split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01973 | RWB-ITG-E5002-ITG | GAP-1190 | none | Add RWB-PLT-E1027-CON and RWB-PLT-N001-CON to the build list of RWB-ITG-E5002-ITG when the plan is regenerated. |

### OTHER:Epics 3 to 8 PRD and the S4 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01981 | RWB-ITG-E5009-ITG | GAP-2784 | 18 | Add one requirement row for the firm instruction as its own requirement, covering FEAT-LIT-09, then rewrite the requirement column of this story and RWB-E5-009 to it. |

### RWB-ITG-W3J01-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02320 | RWB-ITG-W3J01-ITG | DOR-RWB-ITG-W3J01-ITG-21 | header | Create contract story RWB-ITG-W3J01-CON publishing the operations consumed in 12.2; the story now names it as contract dependency. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20572 | RWB-ITG-E4047-ITG | R-22792 |  | Posting-reference read (payment code, business date, reference, batch status) belongs to the P1 contract epic, not this PRD. No PRD text added. |

### 12 Project communication/Recovery Workbench Document Control Sheet v13.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20606 | RWB-ITG-E4045-ITG | R-22779 |  | Owner agreement sits outside this story; GAP-0431 reference stays until owners record answers. No sheet edit made. Could not read v13 xlsx (Bash unavailable), so no row check. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20820 | RWB-ITG-E4046-ITG | R-21873 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09174', 'R-21873', 'R-28451', 'R-28452', 'R-28453'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0429 | SVAF order interface, data product code, staleness parameter and harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0430 | The data product code, the acceptance write, the multi-appraisal choice and the wave 3 harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0431 | The fee tables, the fee operation and the wave 3 harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0432 | ALS interface, booking operation and wave 3 harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0433 | The general ledger interface, the posting reference, the entry set per route and the wave 3 harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0434 | The reconciliation_result owner, the ACE product code, the reconciliation operation and the wave 3 harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0435 | The split of the legacy instruction step, the instruction and pack field names, and which clock is the partner clock | Solution architect | Resolved (directive) |
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-0437 | The legacy delivery step is split across rwb-comms, rwb-litigation and rwb-case with no named hand-off operation and no named reference rows, so the end-to-end chain of RWB-E5-002 has no single source of record | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0737 | The split of the proof-of-delivery key between rwb-case, rwb-litigation and rwb-comms, the S4 answer, the notice-period duration and the requirement ID are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1189 | The proof-record operation of RWB-S4-E5002-CON is not named in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1191 | DP-11 is absent from the pattern set of a story that consumes one published operation | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1192 | The meaning of the two unexercised LOV-DELIVERY values, and the contract the list is read on, are not stated | Business analyst, P6 | Resolved (directive) |
| GAP-1193 | The labels AC1 to AC8 are reused by three documents of the same legacy key for different criteria | Business analyst, P6 | Resolved (directive) |
| GAP-1194 | The source reads the proof of delivery from v_ace_pod in process, and this story may read no ACE view | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1195 | The proof-record path, its fields and its right are this story's design, because no source names a proof-record operation | Solution architect | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1677 | FSD S1 reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1679 | The Ownership Map lists no table for rwb-valuation, although Architecture v5 gives it three entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1682 | Two asset valuation operations are ruled to this service against the module they are published under | Solution architect | Resolved (directive) |
| GAP-1683 | The appraisal order is raised to SVAF, and Architecture v5 gives no SVAF path to this service | Solution architect with the integration lead | Resolved (directive) |
| GAP-1686 | No scheduled job of this service appears in the job map, while the FSD triggers the appraisal check on a batch, an event or a timer | Solution architect | Resolved (directive) |
| GAP-1689 | E3 needs the valuation capabilities one release before the service that delivers them is created | Solution architect | Resolved (directive) |
| GAP-1690 | Every message this service shows is another service's message | Business analyst, S1 | Resolved (directive) |
| GAP-1695 | The history of FSD S1 version 1 and 2 is not in the sources read | Business analyst, S1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1740 | The notice and its proof of delivery sit in S4 in the FSD and in rwb-comms in Architecture v5 and the Ownership Map, and the three notice paths are split across the two services | Solution architect | Resolved (directive) |
| GAP-1741 | The notice capability is first needed in Epic 2 (wave 2, 31 December 2026 (tentative)) while the service is created in wave 3 | Solution architect | Resolved (directive) |
| GAP-1748 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | Business analyst, S4 | Resolved (directive) |
| GAP-2122 | The journey steps and test cases of each wave are not stated | QA team | Resolved (directive) |
| GAP-2160 | The wave 3 journey drives rwb-partner, which the wave map places in wave 4 | Integration lead | Resolved (directive) |
| GAP-2542 | The legacy criteria of RWB-E4-045 are generic, the split gives this slice only AC2, and the slice carries no requirement id | P8 business analyst and the Payment module owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2543 | The fee tables held as data have no owning service and no place in this schema, and the consumed reads that carry them are unpublished | P8 data owner, the P3 reference-data owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2544 | No fee type list, fee row value, rate, cap or fee-specific message is published, and rule_row is named by the legacy key but is not the source of the value | the reference-data owner (P3), the P7 rule owner and the P8 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2545 | The service owns no fee operation and no fee event, so the answer of the calculation has no published carrier | P8 solution architect and the service contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2546 | The fee run and its activity have no published names, and the trigger of the calculation is stated two different ways | P8 solution architect and the workflow platform owner (RWB-PLT-WF) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2547 | The legacy key leaves this slice one generic criterion, its four test cases carry no booking data, the FSD success criterion is a single line and the plan gives the slice no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2549 | The legacy story reads v_ace_account and v_ace_payment in process while the target gives the ACE views to rwb-source-data alone | P1 source-data owner and the P8 solution architect | Resolved (directive) |
| GAP-2550 | The work package gives the contract-dependency row as None while the story consumes four REST contracts and one activity contract, and it still starts on Day 1 | P8 solution architect and the split-plan owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2551 | The legacy key tracks the booking in outbound_item, a table this service owns in the monolith and rwb-integration owns in the target | P8 solution architect and the P2 integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2552 | No source says which service raises the booking call after the accepted treatment, and the settlement path has no rejection rule row of its own | P8 business analyst and the Settlement route set owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2554 | The trigger and the posting window of the feature are not stated for this service | Solution architect | Resolved (directive) |
| GAP-2555 | The field that carries the posting reference, and the read that serves it, are named in no contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2556 | The event catalogue holds no posting-result event, so a confirmed posting is announced nowhere | Solution architect | Resolved (directive) |
| GAP-2557 | The ledger interface values, its layout, its result codes and its retry schedule are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2558 | The integration story assigns a payments read to rwb-payment that its ownership rows do not hold | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2559 | The rejection of a posting is a route state for the debt sale and the write-off and has no stated owner for a settlement or a sale receipt | Business analyst, P8 | Resolved (directive) |
| GAP-2560 | Two consumed reads are class C in fact while the plan's contract row for the key is None | Solution architect | Resolved (directive) |
| GAP-2587 | The operation names of the six consumed rows and the SVAF order interface are not published | P1 rwb-source-data owner, P2 rwb-integration owner, P3 rwb-case owner, P7 rwb-decision owner and P4 rwb-access owner | Resolved (directive) |
| GAP-2588 | The Ownership Map carries two valuation paths and no appraisal-order operation, and no source says which valuation path is current | S1 rwb-valuation service owner | Resolved (directive) |
| GAP-2589 | The Ownership Map gives S1 no table while TSD S1 T3.1 declares valuation as a new Workbench table and the FSD holds the acceptance in recovery.valuation_ext | S1 rwb-valuation service owner with the P1 rwb-source-data owner and the data steward | Resolved (directive) |
| GAP-2590 | The application story consumes six rows and the SVAF order interface, and no source publishes their operation names | P1 rwb-source-data owner, P2 rwb-integration owner, P3 rwb-case owner, P7 rwb-decision owner and P4 rwb-access owner | Resolved (directive) |
| GAP-2591 | No source fixes where the stale flag, the age and the acceptance are persisted for this step | S1 rwb-valuation service owner with the P1 rwb-source-data owner and the data steward | Resolved (directive) |
| GAP-2593 | No source names the event or the timer that starts the age check on a completed ACE batch, and S1 owns no job and no event | S1 rwb-valuation service owner with the P1 rwb-source-data owner | Resolved (directive) |
| GAP-2594 | RWB-E4-002 on rwb-valuation: table ownership, trigger and the view read path are fixed by no single source | Solution architect, S1; data owner of rwb-valuation; owner of the ACE view catalogue | Resolved (directive) |
| GAP-2595 | RWB-E4-002 contract on rwb-valuation: valuation_ext field list, element nesting, 409 and 404 wording, retention and publication coordinates are stated by no source | Contract author, S1; platform API owner; solution architect, S1 | Resolved (directive) |
| GAP-2744 | The delivery fact has no home in rwb-litigation and no published operation on any of the three services it crosses | Solution architect, S4 rwb-litigation, with the P1 rwb-source-data and P6 rwb-comms architects | Resolved (directive) |
| GAP-2745 | The proof of delivery is named as an event in the rules and the FSD, while the service publishes and consumes nothing and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case and P6 rwb-comms architects and the event platform team | Resolved (directive) |
| GAP-2747 | The legacy master carries no requirement identifier for RWB-E5-002, so both stories trace to the feature and one module requirement | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2748 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |
| GAP-2781 | The instruction has no row and no published operation in rwb-litigation, and the partner rows and the pack are other services' | Solution architect, S4 rwb-litigation, with the S9 rwb-partner and P5 rwb-document architects | Resolved (directive) |
| GAP-2782 | The firm events are named in the rules while the service publishes and consumes nothing, and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case and S9 rwb-partner architects and the event platform team | Resolved (directive) |
| GAP-2784 | The legacy master carries no requirement identifier for RWB-E5-009, so both stories trace to the feature and to REQ-S4-004 | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2785 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E4001-ITG | skipped AC ID | 105 | missing: AC2 |
| RWB-ITG-E4002-ITG | new AC without TC row | 324 | AC2 is new and no section 16 row covers it |
| RWB-ITG-E4045-ITG | skipped AC ID | 113 | missing: AC2 |
| RWB-ITG-E4046-ITG | skipped AC ID | 105 | missing: AC2 |
