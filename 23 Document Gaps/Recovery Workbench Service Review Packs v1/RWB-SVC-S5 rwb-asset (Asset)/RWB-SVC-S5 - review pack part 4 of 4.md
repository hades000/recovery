# RWB-SVC-S5 rwb-asset (Asset) - review pack, part 4 of 4 (RWB-S5-E4033-CON to RWB-S5-E4034-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 3 |
| Resolved in the stories | 75 |
| Cross-document (pending in another document) | 69 |
| Not applied (value not in the sources) | 0 |
| Open business decisions | 3 |
| Register gaps linked | 25 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S5-E4033-CON | 18 | 27 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4033 CON Rent a held asset to a third party - contract v2.md |
| RWB-S5-E4034-APP | 35 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4034 APP Sell through a broker v2.md |
| RWB-S5-E4034-CON | 22 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4034 CON Sell through a broker - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S5-E4034-APP | R-13014 | CG-ALL-10301 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3019-APP, RWB-S5-E3019-CON, RWB-S5-E4034-APP, RWB-S5-E4034-CON | R-23474 | GAP-1769 | Register gap | Solution architect with the data product owner | The asset population, the auction round volume and the holding cost volume are in no source | Size on the case volume and the NPA book stated in NFR-001 until the asset and round volumes are given, and record the volume as an open question that blocks the performance test only. |
| RWB-S5-E3019-APP, RWB-S5-E3019-CON, RWB-S5-E4034-APP, RWB-S5-E4034-CON | R-29152 | GAP-1764 | Register gap | Compliance and PDPA officer | The classification and the retention of the asset, listing and sale records are not set | Carry the classification stated in section 8 of this PRD, hold the periods as open, and record the classification on every record so a retention load can be applied without a rebuild. |

## 4. Not applied (the value is not in the source documents)

None.

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18294 | RWB-S5-E4033-CON | CG-ALL-10274 | 12.2 | Declare REST base /api/recovery/payment/v1 for the rwb-payment auto-debit request, from the Document Index service table. |
| CDC-18295 | RWB-S5-E4033-CON | CG-ALL-10275 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case GET family, from the Document Index service table. |
| CDC-18296 | RWB-S5-E4033-CON | CG-ALL-10276 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case case-move answer, from the Document Index service table. |
| CDC-18297 | RWB-S5-E4033-CON | CG-ALL-10277 | 12.2 | Declare REST base /api/recovery/comms/v1 for POST /cases/{caseId}/notices, from the Document Index service table. |
| CDC-18298 | RWB-S5-E4033-CON | CG-ALL-10278 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the ACE asset read, from the Document Index service table. |
| CDC-18300 | RWB-S5-E4033-CON | DOR-RWB-S5-E4033-CON-8 | 12.2 | Declare REST bases for /api/recovery/payment/v1, /case/v1, /comms/v1 and /source-data/v1 (per CG-ALL-10274 to CG-ALL-10278). |
| CDC-18321 | RWB-S5-E4034-APP | CG-ALL-10289 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case provider (GET /cases/{caseId} family, read). |
| CDC-18322 | RWB-S5-E4034-APP | CG-ALL-10290 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case provider (case-move answer). |
| CDC-18323 | RWB-S5-E4034-APP | CG-ALL-10291 | 12.2 | Declare the REST base /api/recovery/comms/v1 for the rwb-comms provider (template read of R-DIS-24). |
| CDC-18324 | RWB-S5-E4034-APP | CG-ALL-10292 | 12.2 | Declare the REST base /api/recovery/payment/v1 for the rwb-payment provider (auto-debit request of R-DIS-25). |
| CDC-18325 | RWB-S5-E4034-APP | CG-ALL-10293 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision provider (package in force). |
| CDC-18330 | RWB-S5-E4034-APP | DOR-RWB-S5-E4034-APP-8 | header | Add yaml with bases /api/recovery/case/v1, comms/v1, payment/v1, decision/v1 and the six further bases in detcheck |
| CDC-18344 | RWB-S5-E4034-CON | CG-ALL-10307 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, per the Document Index service table |
| CDC-18345 | RWB-S5-E4034-CON | CG-ALL-10308 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, per the Document Index service table |
| CDC-18346 | RWB-S5-E4034-CON | CG-ALL-10309 | 12.2 | Declare REST base /api/recovery/comms/v1 for the rwb-comms provider, per the Document Index service table |
| CDC-18347 | RWB-S5-E4034-CON | CG-ALL-10310 | 12.2 | Declare REST base /api/recovery/payment/v1 for the rwb-payment provider, per the Document Index service table |
| CDC-18348 | RWB-S5-E4034-CON | CG-ALL-10311 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rwb-decision provider, per the Document Index service table |
| CDC-18350 | RWB-S5-E4034-CON | DOR-RWB-S5-E4034-CON-8 | 12.2 | Declare REST bases /api/recovery/case/v1, /api/recovery/comms/v1, /api/recovery/payment/v1 and /api/recovery/decision/v1, plus the 4 further detcheck items |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18301 | RWB-S5-E4033-CON | CG-ALL-10264 | 11 | Add field collateral_id to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18302 | RWB-S5-E4033-CON | CG-ALL-10265 | 11 | Add field holding_status to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18303 | RWB-S5-E4033-CON | CG-ALL-10266 | 11 | Add field holding_cost_to_date to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18304 | RWB-S5-E4033-CON | CG-ALL-10267 | 11 | Add field tenant_ref to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18305 | RWB-S5-E4033-CON | CG-ALL-10268 | 11 | Add field rental_start_date to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18306 | RWB-S5-E4033-CON | CG-ALL-10269 | 11 | Add field rental_term_months to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18307 | RWB-S5-E4033-CON | CG-ALL-10270 | 11 | Add field rent_amount to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18308 | RWB-S5-E4033-CON | CG-ALL-10271 | 11 | Add field rent_currency to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18309 | RWB-S5-E4033-CON | CG-ALL-10272 | 11 | Add field payment_method to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18310 | RWB-S5-E4033-CON | CG-ALL-10273 | 11 | Add field auto_debit_ref to LDM v9 Fields and Data Classification v5 Fields, or record the object that carries it in the owning document. |
| CDC-18314 | RWB-S5-E4033-CON | DOR-RWB-S5-E4033-CON-7 | 11 | Add collateral_id, holding_status, holding_cost_to_date, tenant_ref and the six further detcheck names as LDM v9 or Data Classification v5 fields. |
| CDC-18339 | RWB-S5-E4034-APP | DOR-RWB-S5-E4034-APP-7 | 11 | Add field IDs DF-COL-031, DF-COL-033, DF-COL-037, DF-COL-041 and fields asset_id, holding_status, decision_record. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18313 | RWB-S5-E4033-CON | DOR-RWB-S5-E4033-CON-12 | 12.7, 16 | Add the nine §16 test cases TC-E4-033-01 to -05 and TC-S5-E4033-CON-01 to -04 under tab Story test cases. |
| CDC-18320 | RWB-S5-E4033-CON | CG-ALL-10282 | 16 | Add rows for TC-E4-033-01 to TC-E4-033-05 and TC-S5-E4033-CON-01 to TC-S5-E4033-CON-04, with Given, When and Then copied from the criteria they cover. |
| CDC-18337 | RWB-S5-E4034-APP | CG-ALL-10300 | 16 | Add rows TC-E4-034-01 to TC-E4-034-09 to tab Story test cases, with Given, When and Then copied from the criterion each covers |
| CDC-18356 | RWB-S5-E4034-CON | DOR-RWB-S5-E4034-CON-12 | 12.7, 16 | Add the ten story test IDs plus TC-S5-E4034-CON-05 and -06 to tab Story test cases under the same IDs. |
| CDC-18358 | RWB-S5-E4034-CON | CG-ALL-10316 | 16 | Add Story test cases rows for TC-E4-034-01 to -06 and TC-S5-E4034-CON-01 to -04 with Given, When and Then copied from their criteria, in the next version. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18317 | RWB-S5-E4033-CON | GAP-1935 |  | Record the correction of the Ownership Map GET /assets/{assetId} row as superseded by the business-key path, and of the T3.1 asset key note, for the solution architect. |
| CDC-18319 | RWB-S5-E4033-CON | GAP-2966 |  | Add the asset row with owner S5, since the Ownership Map has no asset row; the rest of this slice is already declared in the story. |
| CDC-18341 | RWB-S5-E4034-APP | GAP-1940 | 11 | Add the missing asset ownership row (S5, rwb_asset) for the architect. |
| CDC-18342 | RWB-S5-E4034-APP | GAP-1941 | header | Correct the GET /assets/{assetId} and POST /assets/{assetId}/listings rows to the business-key form, and the API-S5-001 to API-S5-005 inventory; keep API-S5-005 on the listing identifier. |
| CDC-18343 | RWB-S5-E4034-APP | GAP-2969 | header | Add the rwb-asset ownership row (owner S5) and correct the TSD S5 endpoint inventory to the business-key asset paths. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18299 | RWB-S5-E4033-CON | DOR-RWB-S5-E4033-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S5; no signed epic design is in the story or source documents. |
| CDC-18328 | RWB-S5-E4034-APP | DOR-RWB-S5-E4034-APP-14 | header | Confirm and record the signed epic design sign-off for this story; no signed epic design exists in the story or sources. |
| CDC-18349 | RWB-S5-E4034-CON | DOR-RWB-S5-E4034-CON-14 | Header | Confirm the epic design sign-off and record it; no sign-off reference is in the source documents |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18311 | RWB-S5-E4033-CON | CG-ALL-10281 | 12.5 | Add an Activities row for rentHeldAsset, or name a catalogued activity in its place. |
| CDC-18335 | RWB-S5-E4034-APP | CG-ALL-10298 | 12.5 | Add openBrokerRoute on rwb-asset with the contract element in 12.5, or name a catalogued activity |
| CDC-18336 | RWB-S5-E4034-APP | CG-ALL-10299 | 12.5 | Add activity Partner.issueInstruction on task queue rwb-partner to the Activities sheet, or name a catalogued activity in section 12.5 |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18312 | RWB-S5-E4033-CON | DOR-RWB-S5-E4033-CON-1 | 1 | Add a role code or name for tech lead, or map the story role to an existing role in that document. |
| CDC-18338 | RWB-S5-E4034-APP | DOR-RWB-S5-E4034-APP-6 | 10 | Add role SY-DATALOAD to Users Roles and Permissions v5. |
| CDC-18354 | RWB-S5-E4034-CON | DOR-RWB-S5-E4034-CON-1 | 1 | Add 'tech lead' as a role code or role name, or the story names a role already listed. |

### RWB-S5-E4033-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18315 | RWB-S5-E4033-CON | GAP-2968 |  | Keep the four legacy RWB-E4-034 criteria verbatim on the app story, with R-DIS-24, R-DIS-25, R-DIS-26, R-DIS-64 and R-DIS-65 in its table, and record the rental build as RWB-S5-E4033-APP's. |
| CDC-18316 | RWB-S5-E4033-CON | GAP-1931 |  | Name the activity rentHeldAsset; carry the rwb-payment auto-debit and rwb-case case-move as consumed rows with pending names; keep ATS as an external system with no build. |
| CDC-18318 | RWB-S5-E4033-CON | GAP-2965 |  | Trace the APP slice to FEAT-AST-24, REQ-S5-010 and BR-030; keep auto-debit, case-move and source-data as placeholder operations; keep money, arrears value and notice with rwb-payment and rwb-comms. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18326 | RWB-S5-E4034-APP | CG-ALL-10294 | 13 | Ruling: LOV-LISTING is data. Remove the fixed enum on status so new list values pass schema validation. |
| CDC-18327 | RWB-S5-E4034-APP | CG-ALL-10295 | 13 | Ruling: LOV-SALE-CHANNEL is data. Remove the fixed enum on saleChannel so new list values pass schema validation. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18331 | RWB-S5-E4034-APP | GAP-1750 | 11 | Name ACE asset, collateral and score reads by rwb-source-data contract fields; add S5 to P1 cell of the connection matrix |
| CDC-18351 | RWB-S5-E4034-CON | GAP-1750 | 8 | Add S5 to the P1 cell of the connection matrix; confirm rwb-source-data contract fields, business key and freshness response with P1 before wave 2 system test. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18332 | RWB-S5-E4034-APP | CG-ALL-10286 | 4, 8 | Record asset_id as the asset row identifier, or name the dictionary field for it |
| CDC-18333 | RWB-S5-E4034-APP | CG-ALL-10287 | 4, 9, 12.7, 13 | Record holding_status (DF-COL-041) as an asset field against LOV-HOLDING |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18352 | RWB-S5-E4034-CON | CG-ALL-10314 | 12.5 | Add activity openBrokerRoute on task queue rwb-asset, or name a catalogued activity instead. |
| CDC-18353 | RWB-S5-E4034-CON | CG-ALL-10315 | 12.5 | Add activity Partner.issueInstruction on task queue rwb-partner in namespace rwb-recovery. |

### OTHER:23 Document Gaps/Recovery Workbench Assumptions Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18361 | RWB-S5-E4034-CON | GAP-1943 | header | Record an assumption that the contract baseline is in Draft with no approval record and runs under D-RCV-60. Record the deprecation window of a published property and the contract fake retention as Not specified in the source documents (GAP-1943). |
| CDC-18362 | RWB-S5-E4034-CON | GAP-2971 | header | Record an assumption that the two stories and the contract baseline are in Draft with no approval record and run under D-RCV-60. Record the deprecation window and the fake retention as Not specified in the source documents (GAP-2971). |

### RWB-S5-E4034-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18329 | RWB-S5-E4034-APP | DOR-RWB-S5-E4034-APP-21 | header | Build status Done, with the contract published, before this story starts |

### OTHER:PLT decision-record library specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18334 | RWB-S5-E4034-APP | CG-ALL-10288 | 11 | Record decision_record as a library table created in rwb_asset by the library migration |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18340 | RWB-S5-E4034-APP | GAP-1946 | not in this story | Keep H and C at None; record the nine platform and rwb-case CONs as wave-0 prerequisites and fakes; drop the two extracts and INT-19 path; serve quality facts from the asset quality endpoints. |

### RWB-S5-E4034-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18355 | RWB-S5-E4034-CON | DOR-RWB-S5-E4034-CON-10 | find it | Add empty, loading, error and no-access states for SCR-21 and SCR-23 in the app story. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD S5 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18357 | RWB-S5-E4034-CON | GAP-2969 | 15 | Add the asset ownership row to Ownership Map; correct the TSD S5 endpoint inventory to business-key paths and remove the foreign tables and superseded v2 rows. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4034 APP Sell through a b (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18359 | RWB-S5-E4034-CON | GAP-1768 | 14 | Move MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 out of the module message table to the catalogues of their owning services and the common set. Keep MSG-S5-001 and MSG-S5-002 in the module catalogue. Thai and English wording: Not specified in the source documents (GAP-1768). |

### OTHER:TSD S5 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18360 | RWB-S5-E4034-CON | GAP-1942 | not in chunk | Correct T5.3 to list AssetTakenOn and AssetSold as the two events of rwb.asset.events.v1 and record the sale story's ownership of AssetSold. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1750 | FSD S5 reads the ACE asset, collateral and score views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1761 | The disposal rule set has 72 rules over 40 states, the FSD names about 40 of them, and the package is Phase 2 with no code | Center of excellence analyst | Resolved (directive) |
| GAP-1768 | Four of the six messages this module shows belong to other services and the two of its own have no approved wording | Business analyst, S5 | Resolved (directive) |
| GAP-1931 | The rental terms, the auto-debit and case-move operation names, the arrears follow-up owner and threshold, the ATS interface and the step name are not specified in the source documents | Tech lead of rwb-asset, solution architect, and the owners of rwb-payment and rwb-case | Resolved (directive) |
| GAP-1932 | The legacy Data, Endpoints and Screen tables name views, tables, an operation and a screen state that this slice does not read, call or show | Solution architect and data steward | Resolved (directive) |
| GAP-1933 | The split plan carries no requirement id for this slice | Business analyst and traceability manager | Resolved (directive) |
| GAP-1934 | The rental element, the consumed operation names and the ATS interface are not specified in the source documents | Tech lead of rwb-asset and solution architect, with the owners of rwb-payment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-1935 | The read path carries the ACE asset business key while the asset table is keyed by a record identifier | Solution architect and data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1936 | No approval record, deprecation window or fake retention is stated for the contract baseline | Solution architect and governance lead | Resolved (directive) |
| GAP-1937 | The broker instruction element, the case-move answer, the template price read and the auto-debit request have no published shape, and the broker fee and terms have no rule row, column set or value | Tech lead of rwb-asset and solution architect, with the owners of rwb-case, rwb-partner, rwb-comms and rwb-payment | Resolved (directive) |
| GAP-1938 | The legacy feature is titled Sell through a broker while two of its four criteria are the buy-back and rental rules, and the broker route's own rule and state sit outside the rule table of the slice | Business analyst, solution architect and the rule owner in rwb-decision | Resolved (directive) |
| GAP-1939 | The split plan carries no requirement id for this slice | Business analyst and traceability manager | Resolved (directive) |
| GAP-1940 | The legacy Data, Endpoints and Screen tables name another owner's tables, two superseded asset paths and screen states the target list does not carry | Solution architect and data steward | Resolved (directive) |
| GAP-1941 | The listing path is the asset-id form in the Ownership Map, the TSD and the legacy story while API Specification v3 and v4 carry the business-key form | Solution architect and data steward | Resolved (directive) |
| GAP-1942 | The module event list gives rwb-asset one published event while the catalogue gives two | Solution architect and event owner | Resolved (directive) |
| GAP-1943 | No approval record, deprecation window or fake retention is stated for the contract baseline | Solution architect and governance lead | Resolved (directive) |
| GAP-1944 | The rule package in force is pushed to four services and not to rwb-asset, and DP-04 is not in the pattern set of this key | Solution architect and the rule owner in rwb-decision | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2965 | Rental terms, auto-debit, case-move, arrears follow-up and ATS have no value or name in the sources (APP slice) | Solution architect | Resolved (directive) |
| GAP-2966 | Rental element, consumed operation names, asset key path and Draft baseline have no source shape (CON slice) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2967 | The broker fee and terms have no rule row, no column set and no value, and the instruction element, the case-move answer, the template price read and the auto-debit request have no published shape | Tech lead of rwb-asset and solution architect, with the owners of rwb-case, rwb-partner, rwb-comms and rwb-payment | Resolved (directive) |
| GAP-2968 | The legacy feature is titled Sell through a broker while two of its four criteria are the buy-back and rental rules, and the broker route's own rule has no criterion of the key | Business analyst, solution architect and the rule owner in rwb-decision | Resolved (directive) |
| GAP-2969 | The legacy Data, Endpoints and Screen tables name another owner's tables and two superseded asset paths, the path form disagrees with the later API versions, and the asset row has no Ownership Map row | Solution architect and data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2970 | The split plan carries no requirement id for either slice | Business analyst and traceability manager | Resolved (directive) |
| GAP-2971 | No approval record, deprecation window or fake retention is stated for the two stories and their contract baseline | Solution architect and governance lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
