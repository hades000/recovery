# RWB-SVC-S9 rwb-partner (Partner) - review pack, part 3 of 3 (RWB-S9-E7017-APP to RWB-S9-E7018-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 4 |
| Resolved in the stories | 87 |
| Cross-document (pending in another document) | 50 |
| Not applied (value not in the sources) | 5 |
| Open business decisions | 6 |
| Register gaps linked | 7 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S9-E7017-APP | 28 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7017 APP Manage extra costs and services on an asset v2.md |
| RWB-S9-E7017-CON | 14 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7017 CON Manage extra costs and services on an asset - contract v2.md |
| RWB-S9-E7018-APP | 30 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7018 APP Capture field work through the field app v2.md |
| RWB-S9-E7018-CON | 15 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7018 CON Capture field work through the field app - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S9-E7017-APP | R-13645 | CG-ALL-12141 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E7017-CON | R-13647 | CG-ALL-12152 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E7018-CON | R-13658 | CG-ALL-12184 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E6033-CON, RWB-S9-E7018-APP, RWB-S9-E7018-CON | R-23655 | GAP-3136 | Register gap | Solution architect; rwb-partner tech lead; business lead; rwb-document owner; rwb-source-data owner; rwb-decision rule owner; rwb-access role owner | RWB-S9-E7018-CON: the contract has no field-work, evidence, result-vocabulary, media-type or document-reference source, partner_user publishes no role list, the plan's C row is empty while three consumed rows are declared, DP-05, DP-09 and DP-18 are absent, the element overlaps the baseline of RWB-S9-E6033-CON, EV-21 has two directions, the field app has no interface ID, and TSD S9 T8 maps REQ-S9-009 to another feature | Add one FieldWorkResult element inside the published baseline of RWB-S9-E6033-CON, declare the visit, the evidence and the rule as three consumed rows with fakes and placeholders, declare no evidence column, no visit table, no result enumeration and no partner role enumeration, declare EV-21 with one direction and the conflict recorded, declare no new operation, Schedule or job, and hold the media types, the result vocabulary, the field-app interface, the 409 text and the requirement row open. |
| RWB-S9-E7018-APP, RWB-S9-E7018-CON | R-23668 | GAP-3135 | Register gap | Business lead; solution architect; rwb-document owner; rwb-source-data owner; rwb-decision rule owner; rwb-access role owner | RWB-S9-E7018-APP: no source owns the field visit or its evidence in S9, publishes a field-collector role, a result-code list, a document, interaction or rule operation name, an interface ID for the field app or a refusal message for a closed instruction, no partner route set exists, and TSD S9 T8 maps REQ-S9-009 to another feature | Read the visit as a rwb-source-data interaction entry and the photographs and bills as rwb-document claims requested on their contracts with fakes, keep the result on partner_instruction.result_code with status DONE, submit on API-S9-005 with the Idempotency-Key, write the local decision record before any change with the rule ID and the version where they exist and the placeholder where they do not, carry the field-collector role, the result vocabulary, the PRT-02 state mapping, the field-app interface and its non-functional targets, and the requirement mis-mapping as open items with placeholder text. |
| RWB-S9-E6029-APP, RWB-S9-E7018-APP | R-29236 | GAP-1855 | Register gap | Business analyst, S9 with Legal counsel and Compliance | The module has no message of its own, and no Thai wording is stated for any of its messages | Take the wording from the Error and Message Standard for the reused messages and author the module's own messages with the story, in Thai and English, before the wave-4 release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S9-E7017-APP | R-21581 | DOR-RWB-S9-E7017-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The no-personal-data line is outside this chunk and its exact text is not supplied, so it cannot be edited. Field classification is not in the sources (DOR-RWB-S9-E7017-APP-11). |
| RWB-S9-E7017-CON | R-03291 | CG-ALL-12149 | 12.5 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | Lines 49 and 162 still cite namespace rwb-recovery from Template and Rules §R4. They are outside the diff and must be fixed to match before this can be Resolved. |
| RWB-S9-E7018-APP | R-09146 | DOR-RWB-S9-E7018-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design for RWB-S9-E7018 found in story or sources; prior passes searched. Sign-off value not invented; needs the epic design record. |
| RWB-S9-E7018-APP | R-21604 | DOR-RWB-S9-E7018-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR IDs now given for R-UNI-38 to -40. Coverage of BR1 to BR11 needs AC and TC rows in sections 7 and 16, outside this chunk. |
| RWB-S9-E7018-CON | R-09152 | DOR-RWB-S9-E7018-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-S9-E7018-CON in the story or source folders 03, 06, 12, 14, 17, 18, 21 or 23. Sign-off not confirmed; left unchanged. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20308 | RWB-S9-E7017-APP | CG-ALL-12132 | 12.1 | Publish POST /partner/instructions/{instructionId}/results (API-S9-005) in rwb-partner.yaml through the CON story, or remove it from this story. |
| CDC-20309 | RWB-S9-E7017-APP | CG-ALL-12133 | 12.1 | Publish POST /partner/instructions/{instructionId}/invoices (API-S9-006) in rwb-partner.yaml through the CON story, or remove it from this story. |
| CDC-20314 | RWB-S9-E7017-APP | DOR-RWB-S9-E7017-APP-8 | 12.5 | Publish API-S9-005 and API-S9-006 paths via the CON story. Task queue and start rule are stated in 12.5; workflow ID form is Not specified in the source documents. |
| CDC-20324 | RWB-S9-E7017-CON | CG-ALL-12146 | 12.1 | Publish POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results (API-S9-005) in rwb-partner.yaml |
| CDC-20325 | RWB-S9-E7017-CON | CG-ALL-12147 | 12.1 | Publish POST /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices (API-S9-006) in rwb-partner.yaml |
| CDC-20326 | RWB-S9-E7017-CON | CG-ALL-12148 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions (API-S9-003) in rwb-partner.yaml |
| CDC-20328 | RWB-S9-E7017-CON | DOR-RWB-S9-E7017-CON-8 | header | Publish API-S9-005, API-S9-006 and API-S9-003 paths; confirm the unlisted +1 detcheck entry |
| CDC-20334 | RWB-S9-E7018-APP | CG-ALL-12159 | 12.1 | Publish POST /partner/instructions/{instructionId}/results (API-S9-005) under base /api/recovery/partner/v1, through RWB-S9-E7018-CON. |
| CDC-20335 | RWB-S9-E7018-APP | CG-ALL-12160 | 12.1 | Publish GET /partners (API-S9-001) under base /api/recovery/partner/v1, through RWB-S9-E7018-CON. |
| CDC-20347 | RWB-S9-E7018-CON | CG-ALL-12174 | 12.1 | Publish POST /partner/instructions/{instructionId}/results (API-S9-005) under base /api/recovery/partner/v1. |
| CDC-20348 | RWB-S9-E7018-CON | CG-ALL-12175 | 12.1 | Publish GET /partners (API-S9-001) under base /api/recovery/partner/v1. |
| CDC-20352 | RWB-S9-E7018-CON | DOR-RWB-S9-E7018-CON-8 | 12.1 | Publish the paths and bases behind CG-ALL-12174 to CG-ALL-12178 and the four further P1 detcheck items. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20316 | RWB-S9-E7017-APP | CG-ALL-12136 | 12.5 | Add activity recordCostClaim to the Activities sheet, or name a catalogued activity in its place. |
| CDC-20317 | RWB-S9-E7017-APP | CG-ALL-12137 | 12.5 | Add activity writeCostDecisionRecord to the Activities sheet, or name a catalogued activity in its place. |
| CDC-20318 | RWB-S9-E7017-APP | CG-ALL-12138 | 12.5 | Add activity approveCostInvoice to the Activities sheet, or name a catalogued activity in its place. |
| CDC-20341 | RWB-S9-E7018-APP | CG-ALL-12166 | 12.5 | Add the activity recordFieldWorkResult to the Activities sheet, or name the catalogued activity that performs the field-work step |
| CDC-20355 | RWB-S9-E7018-CON | CG-ALL-12181 | 12.5 | Add an Activities row for recordFieldWorkResult on task queue rwb-partner, or name a catalogued activity. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20319 | RWB-S9-E7017-APP | CG-ALL-12139 | 16 | Add rows TC-E7-017-01 to -04 and TC-S9-E7017-APP-01 to -03, with Given, When and Then copied from the criterion each covers. |
| CDC-20331 | RWB-S9-E7017-CON | DOR-RWB-S9-E7017-CON-12 | 16 | Add rows under the same IDs in Story test cases for TC-E7-017-01 to -04 and TC-S9-E7017-CON-01 to -05 |
| CDC-20333 | RWB-S9-E7017-CON | CG-ALL-12151 | 16 | Add rows for TC-E7-017-01 to TC-E7-017-04 and TC-S9-E7017-CON-01 to TC-S9-E7017-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-20342 | RWB-S9-E7018-APP | CG-ALL-12167 | 16 | Add rows TC-E7-018-01 to TC-E7-018-04 with Given, When and Then copied from the criteria they cover |
| CDC-20356 | RWB-S9-E7018-CON | CG-ALL-12182 | 16 | Add rows for TC-E7-018-01 to -04 and TC-S9-E7018-CON-01 to -06, with Given, When and Then copied from the criteria they cover. |

### RWB-S9-E7017-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20311 | RWB-S9-E7017-APP | DOR-RWB-S9-E7017-APP-21 | Header | Set build status to Done with the contract published. |
| CDC-20312 | RWB-S9-E7017-APP | DOR-RWB-S9-E7017-APP-22 | Header | Publish the contract fake library and record its published version. |
| CDC-20313 | RWB-S9-E7017-APP | DOR-RWB-S9-E7017-APP-23 | header | Publish the contract version that RWB-S9-E7017-APP builds against, and state it on the CON story. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20349 | RWB-S9-E7018-CON | CG-ALL-12176 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data. |
| CDC-20350 | RWB-S9-E7018-CON | CG-ALL-12177 | 12.2 | Declare REST base /api/recovery/document/v1 for P5 rwb-document. |
| CDC-20351 | RWB-S9-E7018-CON | CG-ALL-12178 | 12.2 | Declare REST base /api/recovery/decision/v1 for P7 rwb-decision. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20310 | RWB-S9-E7017-APP | DOR-RWB-S9-E7017-APP-14 | Header | Record the signed epic design sign-off for this story in the epic design record. |
| CDC-20327 | RWB-S9-E7017-CON | DOR-RWB-S9-E7017-CON-14 |  | Record the signed epic design sign-off for RWB-S9-E7017-CON so DoR item 14 can pass. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20320 | RWB-S9-E7017-APP | DOR-RWB-S9-E7017-APP-7 | 11 | Add decision_record as an entity or field, or confirm its name against DF-DEC-001 to DF-DEC-018 of the PLT decision-record library. |
| CDC-20340 | RWB-S9-E7018-APP | CG-ALL-12157 | 12.7 | Record decision_record as a library object created in rwb_partner by the library migration, in the owning document |

### RWB-S9-E7018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20336 | RWB-S9-E7018-APP | DOR-RWB-S9-E7018-APP-21 |  | Complete the contract build so its build status is Done. |
| CDC-20337 | RWB-S9-E7018-APP | DOR-RWB-S9-E7018-APP-22 |  | Publish a contract fake library version and record it as published. |

### OTHER:Functional Specification Document S9 (Partner management v3) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20344 | RWB-S9-E7018-APP | GAP-1842 | 7 | Rewrite A2.15.4 criteria as the main success statement and write step-specific criteria with the story; the story now carries exception rows as AC2 to AC8. |
| CDC-20345 | RWB-S9-E7018-APP | GAP-1839 | 11 | Treat the eight partner and instruction columns as one entity in the field catalogs; write other field lists with the story that first needs them. Story field list in section 11 is already its own. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20346 | RWB-S9-E7018-APP | CG-ALL-12168 | 18 | Align the REQ-DCM-013 test list in RTM v7 with §18 of RWB-S9-E7018-APP (TC-E7-018-01, TC-E7-018-04), or the reverse, in its next version; RTM currently traces TC-E2-024-01, -03, -04. |
| CDC-20357 | RWB-S9-E7018-CON | CG-ALL-12183 | 18 | Align REQ-DCM-013 test list with section 18 (TC-S9-E7018-CON-03) in the next version. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20353 | RWB-S9-E7018-CON | CG-ALL-12172 | 7, 12.3 | Record ce_source as the CloudEvents 1.0 binary-mode attribute of EV-21, not a dictionary field. |
| CDC-20354 | RWB-S9-E7018-CON | CG-ALL-12173 | 7, 12.3 | Record ce_id as the CloudEvents 1.0 binary-mode attribute of EV-21, not a dictionary field. |

### RWB-PLT-E1027-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20315 | RWB-S9-E7017-APP | CG-ALL-12131 | 3 | Record decision_record as an object in the owning document (library table), or use the dictionary name; the story keeps the object name in sections 3 and 12.7. |

### OTHER:Wave 4 integration harness configuration (owner: Integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20321 | RWB-S9-E7017-APP | GAP-0477 | find it | At the wave 4 entry check agree SIT base hosts, fixture layout, synthetic keys, stub answer shapes, claim shape, S9 and S5 approval points, evidence format and retention, and the pass or fail gate; record in harness configuration. |

### OTHER:TSD S9 (T-A.2; OTHER:T3.1; OTHER:T5.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20322 | RWB-S9-E7017-APP | GAP-3134 | 12.4, 12.5 | Publish the InvoiceRequest and Invoice fields, the additional-cost line and the result_code value set in the baseline review; confirm no invoice or approval event is needed. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:S9 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20323 | RWB-S9-E7017-APP | GAP-1847 | 8, 11 | Add the S9 to rwb-integration path for AMIS, agreed with the S5 and P2 owners; the cost is recorded against the rwb-asset reference (BR6, section 11). |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20329 | RWB-S9-E7017-CON | DOR-RWB-S9-E7017-CON-1 | 1 | Provide a role code or name for 'tech lead' in Users Roles and Permissions v5, or confirm the existing role the story maps to |

### RWB-S9-E7017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20330 | RWB-S9-E7017-CON | DOR-RWB-S9-E7017-CON-10 | 10 | Add empty, loading, error and no access states to SCR-34 and SCR-35 |

### RWB-ITG-E7017-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20332 | RWB-S9-E7017-CON | GAP-0477 | none | At the wave 4 entry check record in the harness configuration: SIT base hosts, fixture layout and synthetic keys, stub answer shapes, claim shape, cost approval points in S9 and S5, evidence format and retention, and pass or fail gate |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml; OTHER:source-data and document yamls) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20338 | RWB-S9-E7018-APP | DOR-RWB-S9-E7018-APP-8 | 12 | Add POST /partner/instructions/{instructionId}/results (API-S9-005), GET /partners (API-S9-001), the bases /api/recovery/source-data/v1 and /api/recovery/document/v1, and the four further paths |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20339 | RWB-S9-E7018-APP | GAP-1840 | 18 | Author the partner rule set from FSD A2.3, A2.4 and A2.8 to A2.15; govern it in rwb-decision and evaluate it with the embedded Drools kit |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20343 | RWB-S9-E7018-APP | DOR-RWB-S9-E7018-APP-7 | 7, 11 | Register decision_record as a PLT library object of DP-03 created in rwb_partner, or confirm it sits outside the LDM. AC1 wording now says local decision record. The ce_source name is not in the chunk text. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0477 | Wave 4 integration harness for the extra costs on a held asset has no specified environment, fixture set, claim shape or evidence gate | Integration lead | Resolved (directive) |
| GAP-1839 | The field catalog repeats the same eight partner columns in nine features and names no field for the scorecard, the fee claim, the review, the conduct sample or the field visit | Business analyst, S9 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1840 | No rule row covers allocation by measured return, scoring, review, fee approval, conduct sampling or the field app | Center of excellence analyst with P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1842 | Every FSD acceptance criterion in this module is the same generic statement, and no feature has an alternate flow or a background event | Business analyst, S9 | Resolved (directive) |
| GAP-1847 | The FSD records extra partner costs against AMIS and a held asset, while the matrix gives S9 no cell to rwb-integration and the asset module owns the asset | Solution architect with the S5 and P2 owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3133 | RWB-E7-017 the additional-cost claim: its field set, cost types, approval limit, cost table and approval operation | Solution architect | Resolved (directive) |
| GAP-3134 | RWB-E7-017 the cost claim and the invoice as contract elements, and the event that would announce them | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
