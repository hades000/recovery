# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 11 of 11 (RWB-P4-E8018-CON to RWB-P4-E8019-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 3 |
| Resolved in the stories | 61 |
| Cross-document (pending in another document) | 45 |
| Not applied (value not in the sources) | 2 |
| Open business decisions | 4 |
| Register gaps linked | 12 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E8018-CON | 22 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E8018 CON Refer a case to Aric - contract v2.md |
| RWB-P4-E8019-APP | 22 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E8019 APP Control access by role and by agent v2.md |
| RWB-P4-E8019-CON | 17 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E8019 CON Control access by role and by agent - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E8018-APP, RWB-P4-E8018-CON | R-23054 | GAP-0880 | Register gap | Solution architect, with the fraud investigator's business owner | The referral record code, its state set and its field set are not in the sources | Fix the referral operations, the record code, the state set and the field set in RWB-P4-E8018-CON and confirm them with Compliance and the decision-record library owner before the baseline tag. |
| RWB-P4-E8019-APP, RWB-P4-E8019-CON | R-28992 | GAP-0887 | Register gap | Tech lead of rwb-access, with the internal audit role | The matrix report has no columns, version label or paging in the sources | Fix the report columns, the version label, the paging bounds and the JSON and CSV formats in RWB-P4-E8019-CON, and keep the page bounds as parameter rows read through DP-06. |
| RWB-P4-E8018-APP, RWB-P4-E8018-CON | R-36863 | ASM-1597 | Register assumption |  | A referral is a record of this service and not a table: one record code for a referral, one entry per state change, hash-linked, appended in the transaction that answers the call, with a referral id minted here and opaque to every consumer. | Fraud investigator's business owner and the decision-record library owner |
| RWB-P4-E8019-APP, RWB-P4-E8019-CON | R-36871 | ASM-1606 | Register assumption |  | The baseline of this story is the role and permission tables created by RWB-P4-E1037-APP on the per-service migration of RWB-PLT-E1044-CON; this story adds one index for the matrix read and no table, no column and no constraint. | ACE team as the owner of the schema and the tech lead of rwb-access |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E8018-CON | R-17045 | DOR-RWB-P4-E8018-CON-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 (L229-243) is not in this chunk, so no exact old text can be copied. Re-send section 10 text to add the SCR-03, SCR-39 and SCR-41 states. |
| RWB-P4-E8019-APP | R-25683 | CG-ALL-5690 | 12.9 | Flyway file V8019_1__permission_change_index.sql is not in the V0001..Vnnnn form | L442 is blank in the supplied chunk, so there is no exact old text to edit. The V8019_1 line is in the v1 story file at line 442, not in this chunk. Next rwb-access Flyway number is not in the sources (CG-ALL-5690); E1001 uses V<seq>. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09412 | RWB-P4-E8018-CON | CG-ALL-5666 | 12.1 | Publish POST /api/recovery/access/v1/admin/fraud-referrals with the documented shape of section 12.1. |
| CDC-09413 | RWB-P4-E8018-CON | CG-ALL-5667 | 12.1 | Publish POST /api/recovery/access/v1/admin/fraud-referrals/{referralId}/results with the documented shape of section 12.1. |
| CDC-09414 | RWB-P4-E8018-CON | CG-ALL-5668 | 12.1 | Publish GET /api/recovery/access/v1/admin/fraud-referrals/{referralId} with the documented shape of section 12.1. |
| CDC-09415 | RWB-P4-E8018-CON | CG-ALL-5669 | 12.1 | Publish GET /api/recovery/access/v1/admin/fraud-referrals with the documented shape of section 12.1. |
| CDC-09416 | RWB-P4-E8018-CON | CG-ALL-5670 | 12.2 | Publish POST /api/recovery/access/v1/authorise; rwb-access is the provider and no other published authorise exists. |
| CDC-09419 | RWB-P4-E8018-CON | DOR-RWB-P4-E8018-CON-8 | 12.1 | Add POST /admin/fraud-referrals, POST /admin/fraud-referrals/{referralId}/results, GET /admin/fraud-referrals/{referralId} and GET /admin/fraud-referrals, with the Idempotency-Key header on the two writes. |
| CDC-09426 | RWB-P4-E8019-APP | CG-ALL-5681 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the RWB-P4-E8019-CON contract work. |
| CDC-09439 | RWB-P4-E8019-CON | CG-ALL-5696 | 12.1 | Publish operation GET /api/recovery/access/v1/admin/access-matrix with the shape in section 12.1. |
| CDC-09440 | RWB-P4-E8019-CON | CG-ALL-5697 | 12.1 | Publish operation PATCH /api/recovery/access/v1/admin/access-matrix/{roleCode} with the shape in section 12.1. |
| CDC-09441 | RWB-P4-E8019-CON | CG-ALL-5698 | 12.1 | Publish operation POST /api/recovery/access/v1/admin/access-matrix/{roleCode}/approve with the shape in section 12.1. |
| CDC-09442 | RWB-P4-E8019-CON | CG-ALL-5699 | 12.1 | Publish operation GET /api/recovery/access/v1/admin/access-matrix/report with the shape in section 12.1. |
| CDC-09443 | RWB-P4-E8019-CON | CG-ALL-5700 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise, which this story consumes, in the provider's yaml. |
| CDC-09445 | RWB-P4-E8019-CON | CG-ALL-5702 | 12.1 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data without a code change. |
| CDC-09447 | RWB-P4-E8019-CON | DOR-RWB-P4-E8019-CON-8 | 12.1 | Declare GET /admin/access-matrix, PATCH /admin/access-matrix/{roleCode}, POST /admin/access-matrix/{roleCode}/approve and GET /admin/access-matrix/report; add Idempotency-Key to PATCH and approve. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09431 | RWB-P4-E8019-APP | CG-ALL-5686 | 4, 14 | Add a new message ID for the requester of a non-human actor change calling approve, distinct from MSG-P7-002; the story then cites it in 4 step 16 and 14. |
| CDC-09434 | RWB-P4-E8019-APP | DOR-RWB-P4-E8019-APP-9 | 14 | Add the new message ID for a non-human actor requester approval (CG-ALL-5686); MSG-P7-002 keeps the standard meaning. |
| CDC-09448 | RWB-P4-E8019-CON | CG-ALL-5704 | 14 | Add a new message ID for the requester of a non-human actor change approving it; MSG-P7-002 keeps 'Approver prepared the decision'. The story then cites the new ID. |
| CDC-09451 | RWB-P4-E8019-CON | DOR-RWB-P4-E8019-CON-9 | 14 | Add a new message ID for the requester of a non-human actor change approving it; MSG-P7-002 keeps 'Approver prepared the decision'. The story then cites the new ID. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09424 | RWB-P4-E8018-CON | CG-ALL-5675 | 16 | Add rows for TC-E8-018-CON-01 to TC-E8-018-CON-06 with Given, When and Then copied from AC1 to AC6. |
| CDC-09432 | RWB-P4-E8019-APP | CG-ALL-5687 | 16 | Add rows TC-E8-019-01 to TC-E8-019-09 with Given, When and Then copied from the criterion each covers. |
| CDC-09454 | RWB-P4-E8019-CON | CG-ALL-5705 | 16 | Add rows TC-E8-019-CON-01 to TC-E8-019-CON-06 with Given, When and Then copied from AC1 to AC6 of this story. |

### RWB-P4-E8019-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09428 | RWB-P4-E8019-APP | DOR-RWB-P4-E8019-APP-21 | Metadata | Set the build status of RWB-P4-E8019-CON to Done once the contract is published. |
| CDC-09435 | RWB-P4-E8019-APP | GAP-0885 | 3 | Fix the matrix read, the matrix write under If-Match, the approval of a non-human actor change and the report; confirm the approval step with the security administrator before the baseline tag. |
| CDC-09437 | RWB-P4-E8019-APP | GAP-2305 | 3 | Publish API-P4-007 plus GET /admin/agents, PUT /admin/roles/{roleCode}/permissions and GET /admin/access-matrix; fix the six schemas, report columns, LOV-enumerated sets, both versions on write, and CSV media type with fixed header. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09418 | RWB-P4-E8018-CON | DOR-RWB-P4-E8018-CON-14 | header | Confirm and record the signed epic design sign-off for RWB-P4-E8018-CON. |
| CDC-09446 | RWB-P4-E8019-CON | DOR-RWB-P4-E8019-CON-14 | Header | Record the signed epic design sign-off for RWB-P4-E8019-CON. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09420 | RWB-P4-E8018-CON | DOR-RWB-P4-E8018-CON-1 | 1 | Add 'tech lead' as a role name, or confirm the role name §1 should use. |
| CDC-09449 | RWB-P4-E8019-CON | DOR-RWB-P4-E8019-CON-1 | 1 | List 'tech lead' as a role code or role name, or §1 names a role it lists. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09427 | RWB-P4-E8019-APP | CG-ALL-5682 | 12.2 | Publish GET /api/recovery/source-data/v1/iam-groups in rwb-source-data.yaml through the P1 provider's contract work. |
| CDC-09444 | RWB-P4-E8019-CON | CG-ALL-5701 | 12.2 | Publish operation GET /api/recovery/source-data/v1/iam-groups through the P1 rwb-source-data CON story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09438 | RWB-P4-E8019-APP | CG-ALL-5689 | 18 | Align the test lists of the four requirements in the item with section 18 of this story in the next RTM version. |
| CDC-09455 | RWB-P4-E8019-CON | CG-ALL-5706 | 18 | Align the test lists of the four requirements in the item with section 18 of RWB-P4-E8019-CON in the next RTM version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09417 | RWB-P4-E8018-CON | CG-ALL-5671 | 12.2 | Publish GET /api/recovery/decision/v1/decisions with the caseId query parameter. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09421 | RWB-P4-E8018-CON | DOR-RWB-P4-E8018-CON-12 | 12.7, 16, 18 | Story adds TC-07 to TC-10 and scenarios AC7 to AC9 |

### OTHER:P2 and P3 story files that carry the divergent messages (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09422 | RWB-P4-E8018-CON | DOR-RWB-P4-E8018-CON-9 | 14 | P3 story: MSG-P1-001 text must match Error and Message Standard v4 section 4. P2 story: MSG-GEN-002 used only with the standard's meaning, a value outside its allowed range. Section 14 of this story already matches the standard (rows at standard lines 65, 66 and 72). |

### OTHER:Recovery Workbench TSD P3 v3, rwb-case contract (recovery_case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09423 | RWB-P4-E8018-CON | GAP-0881 | 4 | Answer the fraud flag and the fraud verdict reference explicitly in the P3 case read and fix their field names in the P3 contract. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; OTHER:REQ-CWC-018 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09425 | RWB-P4-E8018-CON | CG-ALL-5676 | 18 | Align REQ-CWC-018 trace to TC-E8-018-CON-03 and TC-E8-018-CON-04 as section 18 states, replacing TC-E2-036-01, -02, -03 and -13. |

### OTHER:rwb-access API yaml; OTHER:rwb-source-data API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09429 | RWB-P4-E8019-APP | DOR-RWB-P4-E8019-APP-8 | 4, 12.3 | rwb-access yaml publish POST /api/recovery/access/v1/authorise and model roleClass as data from LOV-ROLE-CLASS, not a closed enum; rwb-source-data yaml publish GET /api/recovery/source-data/v1/iam-groups; Kafka Catalog v1 align the AccessPolicyChanged payload per CG-ALL-5684 |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09430 | RWB-P4-E8019-APP | CG-ALL-5684 | 12.3 | Publish the payload field set of RWB-P4-E8019-APP 12.3: approving role code, effective time, capability area, change kind, letters before and after, matrix version before and after, role class, role code. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09433 | RWB-P4-E8019-APP | DOR-RWB-P4-E8019-APP-7 | 11 | Confirm DF-REF-039 (role.entra_group) as a field of LDM v9 or add it there. |

### OTHER:rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09436 | RWB-P4-E8019-APP | GAP-0889 | 3 | Declare the group mapping read with its answer fields and freshness stamp, and add the contract dependency to the wave 4 plan at D1. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09450 | RWB-P4-E8019-CON | DOR-RWB-P4-E8019-CON-12 | 16 | Register TC-E8-019-CON-01 to -07 in Test Cases v8; align the §18 test lists with RTM v7. |

### OTHER:rwb-source-data contract (P1) and wave 4 plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09452 | RWB-P4-E8019-CON | GAP-0889 | 7 | Declare GET /api/recovery/source-data/v1/iam-groups with entra_group, role_code, source_system, data_as_of and a freshness stamp; add the contract dependency to the wave 4 plan at D1. |

### API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09453 | RWB-P4-E8019-CON | GAP-2305 | 7 | Add rows for GET /admin/access-matrix, PATCH /admin/access-matrix/{roleCode}, POST /admin/access-matrix/{roleCode}/approve and GET /admin/access-matrix/report, with the schemas of AC2 and the CSV media type. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20753 | RWB-P4-E8018-CON | R-23055 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0881 | The fraud flag has no field on the case the P3 contract returns | Tech lead of rwb-case (P3), with the tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0882 | No owner, protocol or result channel exists for the Aric interface | Solution architect, with the integration owner of rwb-integration (P2) | Resolved (directive) |
| GAP-0883 | The legacy trigger of the referral has no counterpart in the target service | Solution architect | Resolved (directive) |
| GAP-0884 | The legacy rights of the referral contradict the target matrix and the FSD role table | Security administrator, with the solution architect | Resolved (directive) |
| GAP-0885 | The access matrix over three role classes, its change steps and its report are not in the sources | Solution architect, with the security administrator | Resolved (directive) |
| GAP-0886 | The state set of a matrix change is not in the sources | Solution architect, with the security administrator | Resolved (directive) |
| GAP-0888 | The legacy rights of the matrix conflict with the target matrix | Security administrator, with the solution architect | Resolved (directive) |
| GAP-0889 | The ACE group mapping read has no operation in the target contract | Tech lead of rwb-source-data (P1), with the tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2302 | The referral operations, their fields, the referral state set, the Aric interface, the record codes and the right of a fraud referral are not in the sources | Tech lead of rwb-access | Resolved (directive) |
| GAP-2303 | The contract baseline has to fix the Aric request and answer shape, the referral state set and the record codes because no source states them | Tech lead of rwb-access | Resolved (directive) |
| GAP-2304 | The access-change record code, the matrix version label, the matrix screen, the agent identity source and the grant's service event are not in the sources, and two sources disagree on the group column of a role and on the right of the path | Solution architect | Resolved (directive) |
| GAP-2305 | The three new matrix operations, the schemas, the report columns and the CSV media type are not in the sources, and no source fixes the shape of a grant answer | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
