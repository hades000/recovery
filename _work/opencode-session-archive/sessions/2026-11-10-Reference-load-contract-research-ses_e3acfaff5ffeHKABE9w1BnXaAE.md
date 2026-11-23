# Reference-load contract research

- **Session ID:** `ses_e3acfaff5ffeHKABE9w1BnXaAE`
- **Created:** 2026-11-10 18:20  |  **Last activity:** 2026-11-10 18:27
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `explore`
- **Parent session:** RWB-TE-005 spec clarifications (`ses_e3b1d19eeffeAOQ3VdCtcEaqiQ`)
- **Tokens:** 172,149 in / 23,231 out / 22,322 reasoning
- **Messages:** 49

---

### User - 2026-11-10 18:20

You are a subagent spawned by another session.
Very thorough. Work in C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14.

Task: extract the exact contract and behaviour of POST /api/recovery/v1/admin/reference-loads and the reference-data table code registry, for a build clarification answer.

Read:
- 05 Technical architecture\Recovery Workbench API Specification v2.yaml (search for reference-loads, ReferenceLoad, admin/parameters)
- 05 Technical architecture\Recovery Workbench API Specification v2.html if the yaml is ambiguous
- 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 043 Reference data service with versioned tables v1.md
- 05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P3 Case and workflow v2.md
- 05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P4 Access and administration v2.md
- 05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P5 Document hub v2.md
- 06 Data\Recovery Workbench Physical Schema v4.sql (LOV-REF-TABLE values and target tables)

Answer precisely:
1. The full request schema: multipart fields, types, required/optional, allowed values. Is `table` one code or a list? Is there a `validFrom`? Any `dryRun`? Any content hash/Idempotency-Key header?
2. The response schema and status codes, including 201/200 on repeat, 409, 422 error bodies.
3. The authorisation right(s) and capability area; approve and rollback endpoints.
4. The complete list of LOV-REF-TABLE codes from the physical schema, with label and sort order. State exactly how many there are.
5. For each code, which handler/loader owns it and which physical table(s) it writes. State clearly: does the caller choose a database table, a table code, a type, or a column? Is any user-supplied column mapping allowed?
6. For the PARAMETER code specifically: exact CSV columns, header names, order, separators, encoding, max rows/size if stated, and the mapping of each CSV column to parameter_value columns. What happens to product_group, version_no, status, author, approver, valid_from, valid_to.
7. Any stated CSV templates for other codes (PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL, QUEUE, PERMISSION, MASKING_RULE, etc.). For each, list CSV columns and target {table}.{column}. If a template is not defined anywhere, say NOT DEFINED and name the owning story.
8. Any rule about adding a new table code vs adding a value row.
9. Quote document file paths and line numbers for each key fact.

Return a structured report. Do not modify files.

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

I'll start by exploring the workspace structure and locating the key files.

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File | Select-Object -ExpandProperty FullName", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
ata-inventory-v3\fields.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-classification-and-personal-data-inventory-v3\handling.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-classification-and-personal-data-inventory-v3\identifiers.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-classification-and-personal-data-inventory-v3\key.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-classification-and-personal-data-inventory-v3\summary.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-classification-and-personal-data-inventory-v3\who-sees-what.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-ownership-and-stewardship-v2\change-process.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-ownership-and-stewardship-v2\ownership.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-ownership-and-stewardship-v2\quality-measures.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-ownership-and-stewardship-v2\roles.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-quality-and-reconciliation-rules-v2\load-checks.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-quality-and-reconciliation-rules-v2\quality-measures.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-data-quality-and-reconciliation-rules-v2\reconciliations.csv
C:\Us
... truncated (51,379 chars total)
```

**Tool `glob`** - completed

```json
{"pattern": "**/*Reference*"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Reference Data and Lists of Values v3.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 043 Reference data service with versioned tables v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 043 Reference data service with versioned tables v1.md
```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Let me look at the key files. Start with the story and grep the yaml.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 043 Reference data service with versioned tables v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 043 Reference data service with versioned tables v1.md, lines 1-359
1: # RWB-E1-043 Reference data service with versioned tables
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-E1-043 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | FEAT-CWC-23 Run the reference data service with versioned tables |
14: | Requirement IDs | REQ-DRI-011, REQ-CWC-006 |
15: | BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
16: | L3 process | 14 Set strategy, policy and decision rules |
17: | Decision | None |
18: | Priority | Must |
19: | Depends on | RWB-E1-042, RWB-E1-044 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority, legal periods and holidays held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.
25: 
26: ## 2. Business rationale
27: 
28: Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. This story gives every reference table a version with a valid from date, an author and a different approver, and serves the version in force to the engines. It meets REQ-DRI-011 and REQ-CWC-006 and supports control CTL-08 (a rule, limit or list changes only through a validated load approved by its owner). The measure is that every value an engine reads carries a table code and a version number in its log line.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-044 is done: Flyway migrations run with the schema name taken from a parameter.
33: - RWB-E1-042 is done: the configuration service serves `refdata.cache.ttl-seconds` (assumed 300; DL11) and the list of reference table codes.
34: - The list LOV-REF-TABLE (new, see Additions) is loaded with the 13 table codes in section 8, BR1.
35: - The reference load endpoint `POS
... truncated (26,433 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "reference-loads|ReferenceLoad|reference_loads", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "limit": 200}
```

```text
Found 200 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.html:
  Line 42: </style></head><body><header><div class="in"><div class="lab">SCB COLLECTIONS AND RECOVERY</div><h1>Recovery Workbench API specification</h1><div class="meta">Henka Group, 28 October 2026. (C) Siam Commercial Bank and Henka Pte Ltd</div></div></header><nav><div class="in"><button data-t="ov" aria-selected="false">Overview</button><button data-t="ep" aria-selected="false">Endpoints</button><button data-t="sc" aria-selected="false">Schemas</button><button data-t="er" aria-selected="false">Errors</button><button data-t="rl" aria-selected="false">By release</button></div></nav><main><section class="tab" id="ov"><div class="grid"><div class="box"><b>144 endpoints</b>In 15 groups, under /api/recovery/v1 in the ACE service</div><div class="box"><b>178 schemas</b>Records from the logical data model, requests, pages and the problem response</div><div class="box"><b>One access check</b>Role, capability area, right and scope on every endpoint</div><div class="box"><b>OpenAPI 3.1</b>The YAML file is the contract; types are generated from it</div></div><h2>Rules every endpoint follows</h2><div class="tw"><table style="min-width:760px"><thead><tr><th>Rule</th><th>Detail</th></tr></thead><tbody><tr><td class="">Sign-in</td><td class="">Bearer token from Entra ID through the ACE front end; partners through the external gateway (DL03)</td></tr><tr><td class="">Access</td><td class="">The endpoint declares its capability area and right; scope filters every query; out of scope returns 404</td></tr><tr><td class="">Approvals</td><td class="">Approval endpoints check the approval level, the delegation of authority limit and maker and checker</td></tr><tr><td class="">Decision log</td><td class="">Every state change writes its decision log entry first; a failed write returns 503 and nothing changes</td></tr><tr><td class="">Concurrency</td><td class="">Records carry a version; a stale version returns 409 with MSG-GEN-004</td></tr><tr><td class="">Idempotency</td><td class="">POST request...

C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml:
  Line 2955:   /admin/reference-loads:

  Line 2960:       operationId: postAdminReferenceLoads

  Line 2980:       description: Add multipart fields changeRequestRef (max 30), impactSum
... truncated (46,717 chars total)
```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now let me read the yaml around lines 2955-3030 and 5028-5110, plus ReferenceLoad schema at 8812.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml", "offset": 2930, "limit": 120}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 2930-3049
2930:       x-capability:
2931:         area: Reference data
2932:         right: R
2933:       x-first-release: E1
2934:       parameters:
2935:       - name: listCode
2936:         in: path
2937:         required: true
2938:         schema:
2939:           type: string
2940:       responses:
2941:         '200':
2942:           description: Success
2943:           content:
2944:             application/json:
2945:               schema:
2946:                 $ref: '#/components/schemas/ListOfValues'
2947:         '401':
2948:           $ref: '#/components/responses/E401'
2949:         '403':
2950:           $ref: '#/components/responses/E403'
2951:         '404':
2952:           $ref: '#/components/responses/E404'
2953:         '503':
2954:           $ref: '#/components/responses/E503'
2955:   /admin/reference-loads:
2956:     post:
2957:       tags:
2958:       - Administration
2959:       summary: 'Load reference data: lists, queues, timers, templates, delegation limits'
2960:       operationId: postAdminReferenceLoads
2961:       x-module: P4
2962:       x-capability:
2963:         area: Reference data
2964:         right: C
2965:       x-first-release: E1
2966:       requestBody:
2967:         required: true
2968:         content:
2969:           multipart/form-data:
2970:             schema:
2971:               type: object
2972:               properties:
2973:                 file:
2974:                   type: string
2975:                   format: binary
2976:                 table:
2977:                   type: string
2978:                 validFrom:
2979:                   type: string
2980:       description: Add multipart fields changeRequestRef (max 30), impactSummary (max 1000) and rollbackPlan (max 1000). ReferenceLoad adds changeRequestRef,
2981:         impactSummary, rollbackPlan, testResult, verifiedBy (uuid) and verifiedAt (date-time). Approval of a version with a missing checklist
2982:         item or a FAILED test returns 409 with MSG-P3-022. Accept the P5 table codes DOCUMENT_TYPE (RWB-E1-025), DOCUMENT_CHECKLIST (RWB-E1-040),
2983:         RETENTION_CLASS (RWB-E1-041) and DOCUMENT_HUB_PARAMETER (RWB-E1-024), validated by the P5 ReferenceTableLoader implementations; a failed
2984:         check returns 409 or 422 with MSG-P3-027.
2985:       responses:
2986:         '20
... truncated (4,866 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml", "offset": 5000, "limit": 130}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 5000-5129
5000:         required: false
5001:         schema:
5002:           type: string
5003:       - name: page
5004:         in: query
5005:         required: false
5006:         schema:
5007:           type: integer
5008:       - name: size
5009:         in: query
5010:         required: false
5011:         schema:
5012:           type: integer
5013:       responses:
5014:         '200':
5015:           description: Success
5016:           content:
5017:             application/json:
5018:               schema:
5019:                 $ref: '#/components/schemas/ChangeLogPage'
5020:         '401':
5021:           $ref: '#/components/responses/E401'
5022:         '403':
5023:           $ref: '#/components/responses/E403'
5024:         '422':
5025:           $ref: '#/components/responses/E422'
5026:         '503':
5027:           $ref: '#/components/responses/E503'
5028:   /admin/reference-loads/{loadId}/verify:
5029:     post:
5030:       tags:
5031:       - Administration
5032:       summary: Record the verification of a reference data version after its valid from date
5033:       operationId: postAdminReferenceLoadsLoadidVerify
5034:       x-module: P4
5035:       x-capability:
5036:         area: Reference data
5037:         right: U
5038:       x-first-release: E1
5039:       requestBody:
5040:         required: true
5041:         content:
5042:           application/json:
5043:             schema:
5044:               $ref: '#/components/schemas/VerifyRequest'
5045:       parameters:
5046:       - name: loadId
5047:         in: path
5048:         required: true
5049:         schema:
5050:           type: string
5051:           format: uuid
5052:       responses:
5053:         '200':
5054:           description: Success
5055:           content:
5056:             application/json:
5057:               schema:
5058:                 $ref: '#/components/schemas/ReferenceLoad'
5059:         '401':
5060:           $ref: '#/components/responses/E401'
5061:         '403':
5062:           $ref: '#/components/responses/E403'
5063:         '404':
5064:           $ref: '#/components/responses/E404'
5065:         '409':
5066:           $ref: '#/components/responses/E409'
5067:         '422':
5068:           $ref: '#/components/responses/E422'
5069:         '503':
5070:           $ref: '#/components/responses/E50
... truncated (4,587 chars total)
```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now the ReferenceLoad schema at 8812 and the error responses E409, E422, E401, E403. Also RollbackRequest, VerifyRequest, Problem schema.

</details>

**Tool `read`** - completed

```json
{"limit": 90, "offset": 8790, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 8790-8879
8790:           type: string
8791:           format: uuid
8792:         caseId:
8793:           type: string
8794:           format: uuid
8795:         decision:
8796:           type: string
8797:         preparedBy:
8798:           type: string
8799:         level:
8800:           type: string
8801:         amount:
8802:           type: number
8803:         status:
8804:           type: string
8805:     ListOfValues:
8806:       type: object
8807:       properties:
8808:         code:
8809:           type: string
8810:         values:
8811:           type: object
8812:     ReferenceLoad:
8813:       type: object
8814:       properties:
8815:         id:
8816:           type: string
8817:           format: uuid
8818:         table:
8819:           type: string
8820:         validFrom:
8821:           type: string
8822:           format: date
8823:         status:
8824:           type: string
8825:         rows:
8826:           type: integer
8827:     Job:
8828:       type: object
8829:       properties:
8830:         id:
8831:           type: string
8832:           format: uuid
8833:         type:
8834:           type: string
8835:         businessDate:
8836:           type: string
8837:           format: date
8838:         status:
8839:           type: string
8840:         startedAt:
8841:           type: string
8842:         endedAt:
8843:           type: string
8844:         checks:
8845:           type: object
8846:     DataQualityException:
8847:       type: object
8848:       properties:
8849:         id:
8850:           type: string
8851:           format: uuid
8852:         product:
8853:           type: string
8854:         check:
8855:           type: string
8856:         record:
8857:           type: string
8858:         raisedOn:
8859:           type: string
8860:           format: date
8861:     AgentRun:
8862:       type: object
8863:       properties:
8864:         id:
8865:           type: string
8866:           format: uuid
8867:         agent:
8868:           type: string
8869:         agentVersion:
8870:           type: string
8871:         caseId:
8872:           type: string
8873:           format: uuid
8874:         outcome:
8875:           type: string
8876:         fallback:
8877:           type: boolean
8878:         latencyMs:
8879:           type: integer
[Output trun
... truncated (2,542 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml", "pattern": "^  responses:|^    E409:|^    E422:|^    E401:|^    E403:|^    E503:|^    Problem:|^  schemas:|RollbackRequest:|VerifyRequest:|ListOfValues:"}
```

```text
Found 11 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml:
  Line 6086:   responses:

  Line 6093:     E401:

  Line 6099:     E403:

  Line 6111:     E409:

  Line 6130:     E422:

  Line 6136:     E503:

  Line 6142:   schemas:

  Line 8805:     ListOfValues:

  Line 8971:     Problem:

  Line 9906:     RollbackRequest:

  Line 10015:     VerifyRequest:

```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

**Tool `read`** - completed

```json
{"limit": 80, "offset": 6086, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 6086-6165
6086:   responses:
6087:     E400:
6088:       description: Bad request. The request is malformed. Messages MSG-GEN-001
6089:       content:
6090:         application/problem+json:
6091:           schema:
6092:             $ref: '#/components/schemas/Problem'
6093:     E401:
6094:       description: Unauthorized. No valid session, or the person holds no Workbench role. Messages MSG-P4-001
6095:       content:
6096:         application/problem+json:
6097:           schema:
6098:             $ref: '#/components/schemas/Problem'
6099:     E403:
6100:       description: Forbidden. The role lacks the right in the capability area. Messages MSG-P4-002
6101:       content:
6102:         application/problem+json:
6103:           schema:
6104:             $ref: '#/components/schemas/Problem'
6105:     E404:
6106:       description: Not found. The record does not exist or is outside the caller's scope. Messages MSG-P4-003
6107:       content:
6108:         application/problem+json:
6109:           schema:
6110:             $ref: '#/components/schemas/Problem'
6111:     E409:
6112:       description: Conflict. The state does not allow the action, the record changed, the approver is above the limit or prepared the decision.
6113:         Messages MSG-P3-005, MSG-GEN-004, MSG-P7-001, MSG-P7-002
6114:       content:
6115:         application/problem+json:
6116:           schema:
6117:             $ref: '#/components/schemas/Problem'
6118:     E413:
6119:       description: Payload too large. The file is above the size limit. Messages MSG-P5-001
6120:       content:
6121:         application/problem+json:
6122:           schema:
6123:             $ref: '#/components/schemas/Problem'
6124:     E415:
6125:       description: Unsupported media type. The file type is not allowed. Messages MSG-P5-001
6126:       content:
6127:         application/problem+json:
6128:           schema:
6129:             $ref: '#/components/schemas/Problem'
6130:     E422:
6131:       description: Unprocessable. A field fails validation. Messages MSG-GEN-001, MSG-GEN-002, MSG-GEN-003
6132:       content:
6133:         application/problem+json:
6134:           schema:
6135:             $ref: '#/components/schemas/Problem'
6136:     E503:
6137:       description: Service unavailable. The decision could not be recorded, or a system of re
... truncated (3,647 chars total)
```

**Tool `read`** - completed

```json
{"limit": 45, "offset": 8965, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 8965-9009
8965:         summary:
8966:           type: string
8967:         by:
8968:           type: string
8969:         reference:
8970:           type: string
8971:     Problem:
8972:       type: object
8973:       properties:
8974:         type:
8975:           type: string
8976:         title:
8977:           type: string
8978:         status:
8979:           type: integer
8980:         detail:
8981:           type: string
8982:         messageCode:
8983:           type: string
8984:         messageTh:
8985:           type: string
8986:         field:
8987:           type: string
8988:         traceId:
8989:           type: string
8990:     AgentConfigVersion:
8991:       type: object
8992:       properties:
8993:         versionId:
8994:           type: string
8995:           format: uuid
8996:         agent:
8997:           type: string
8998:         kind:
8999:           type: string
9000:         version:
9001:           type: string
9002:         status:
9003:           type: string
9004:         validFrom:
9005:           type: string
9006:           format: date
9007:         validTo:
9008:           type: string
9009:           format: date
[Output truncated. Continue reading with offset: 9010]
```

**Tool `read`** - completed

```json
{"limit": 30, "offset": 9900, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 9900-9929
9900:       type: object
9901:       properties:
9902:         name:
9903:           type: string
9904:         value:
9905:           type: string
9906:     RollbackRequest:
9907:       type: object
9908:       properties:
9909:         reason:
9910:           type: string
9911:     Parameter:
9912:       type: object
9913:       properties:
9914:         key:
9915:           type: string
9916:         kind:
9917:           type: string
9918:         type:
9919:           type: string
9920:         unit:
9921:           type: string
9922:         min:
9923:           type: string
9924:         max:
9925:           type: string
9926:         default:
9927:           type: string
9928:         scope:
9929:           type: string
[Output truncated. Continue reading with offset: 9930]
```

**Tool `read`** - completed

```json
{"limit": 20, "offset": 10010, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 10010-10029
10010:           type: integer
10011:         rulesChanged:
10012:           type: array
10013:           items:
10014:             type: string
10015:     VerifyRequest:
10016:       type: object
10017:       properties:
10018:         note:
10019:           type: string
10020:     Session:
10021:       type: object
10022:       properties:
10023:         userRef:
10024:           type: string
10025:         roles:
10026:           type: array
10027:           items:
10028:             $ref: '#/components/schemas/SessionRole'
10029:         matrixVersion:
[Output truncated. Continue reading with offset: 10030]
```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now P4 TSD lines around 320-450.

Also need the LOV-REF-TABLE values from the physical schema. Let me grep.

</details>

**Tool `read`** - completed

```json
{"limit": 190, "offset": 300, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P4 Access and administration v2.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P4 Access and administration v2.md, lines 300-489
300: | REQ-ACA-002 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
301: | REQ-ACA-003 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
302: | REQ-ACA-004 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
303: | REQ-ACA-005 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
304: | REQ-ACA-006 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
305: | REQ-ACA-007 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
306: | REQ-ACA-008 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
307: | REQ-ACA-009 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
308: | REQ-ACA-010 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
309: | REQ-ACA-011 | None | Written one epic ahead | With the story |
310: | REQ-ACA-012 | None | Written one epic ahead | With the story |
311: | REQ-ACA-013 | FEAT-ADM-01 | Written one epic ahead | With the story |
312: 
313: ## Appendix T-A. API specification
314: 
315: ### T-A.1 Endpoint inventory
316: 
317: | ID | Method | Path | Access | First in |
318: |---|---|---|---|---|
319: | API-P4-001 | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R | E1 |
320: | API-P4-002 | POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C | E1 |
321: | API-P4-003 | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A | E1 |
322: | API-P4-004 | GET | /api/recovery/v1/admin/lists/{listCode} | Reference data R | E1 |
323: | API-P4-005 | POST | /api/recovery/v1/admin/reference-loads | Reference data C | E1 |
324: | API-P4-006 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/approve | Reference data A | E1 |
325: | API-P4-007 | GET | /api/recovery/v1/admin/roles | Platform administration R | E1 |
326: | API-P4-008 | GET | /api/recovery/v1/admin/access-log | Platform administration R | E1 |
327: | API-P4-009 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/verify | Reference data U | E1 |
328: | API-P4-010 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/rollback | Reference data U | E1 |
329: | API-P4-011 | POST | /api/recovery/v1/admin/rule-versions/{versionId}/rollback | Rules and parameters U | E1 |
330: | API-P4-012 | GET | /api/recovery/v1/me/session | None R | E1 |
331: | API-P4-013 | POST | /api/recovery/v1/admin/break-glass-grants | Platform administration C | E1 |
332: 
333: ### T-A.2 E
... truncated (8,115 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql", "pattern": "LOV-REF-TABLE"}
```

```text
Found 26 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 5200: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-160', 'reference_version', 'table_code', 'LOV', 'varchar(30)', true, 'LOV-REF-TABLE', NULL, 'Workbench', NULL, false, 'The reference or rule table the version belongs to, for example EXPOSURE_BAND or ALLOCATION');

  Line 5989: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PRODUCT', 'Product', 1, DATE '2026-11-30');

  Line 5990: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'REGION', 'Region', 2, DATE '2026-11-30');

  Line 5991: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'EXPOSURE_BAND', 'Exposure band', 3, DATE '2026-11-30');

  Line 5992: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ROLE', 'Role', 4, DATE '2026-11-30');

  Line 5993: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'TEAM', 'Team', 5, DATE '2026-11-30');

  Line 5994: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE', 'Queue', 6, DATE '2026-11-30');

  Line 5995: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE_MEMBER', 'Queue member', 7, DATE '2026-11-30');

  Line 5996: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'SERVICE_LEVEL', 'Service level', 8, DATE '2026-11-30');

  Line 5997: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_TYPE', 'Document type', 9, DATE '2026-11-30');

  Line 5998: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_CHECKLIST', 'Document checklist', 10, DATE '2026-11-30');

  Line 5999: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'RETENTION_CLASS', 'Retention class', 11, DATE '2026-11-30');

  Line 6000: INSERT INTO lov_value (lov_code, value_code, label_en, sort_orde
... truncated (4,812 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

26 values but only 25 lines shown? Let's count: 5989-6013 inclusive = 25 rows. But "Found 26 matches" includes line 5200 (sys_fields). So 25 values. Let me confirm precisely by reading 5985-6020.

Also need to check if there are more LOV-REF-TABLE inserts elsewhere (e.g., later ALTER/INSERT). grep found only these. Let me read that block to confirm no continuation.

Also check for a count statement in the reference data design doc: "13 table codes" in story vs physical schema 25. Need to check.

Now, the physical tables each code writes. Need to search the schema for tables: product, region, exposure_band, role, team, queue, queue_member, service_level, document_type, document_checklist, retention_class, template, delegation_limit, permission, masking_rule, partner_user, legal_period, holiday, product_parameter, parameter_value, entry?, exclusion?, allocation, assignment, transfer.

"ENTRY", "EXCLUSION", "ALLOCATION", "ASSIGNMENT", "TRANSFER" are likely rule tables (P3 rule tables) — rule version tables, i.e., they map to rule_version/rule_row rather than physical tables. Let's check.

Let me read the schema section 5985-6020 and grep for CREATE TABLE names.

</details>

**Tool `read`** - completed

```json
{"limit": 40, "offset": 5985, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 5985-6024
5985: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'ROLLED_BACK', 'Rolled back', 5, DATE '2026-11-30');
5986: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'REFUSED', 'Refused', 6, DATE '2026-11-30');
5987: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TEST-RESULT', 'PASSED', 'Passed', 1, DATE '2026-11-30');
5988: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TEST-RESULT', 'FAILED', 'Failed', 2, DATE '2026-11-30');
5989: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PRODUCT', 'Product', 1, DATE '2026-11-30');
5990: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'REGION', 'Region', 2, DATE '2026-11-30');
5991: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'EXPOSURE_BAND', 'Exposure band', 3, DATE '2026-11-30');
5992: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ROLE', 'Role', 4, DATE '2026-11-30');
5993: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'TEAM', 'Team', 5, DATE '2026-11-30');
5994: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE', 'Queue', 6, DATE '2026-11-30');
5995: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE_MEMBER', 'Queue member', 7, DATE '2026-11-30');
5996: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'SERVICE_LEVEL', 'Service level', 8, DATE '2026-11-30');
5997: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_TYPE', 'Document type', 9, DATE '2026-11-30');
5998: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_CHECKLIST', 'Document checklist', 10, DATE '2026-11-30');
5999: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'RETENT
... truncated (6,648 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql", "pattern": "^CREATE TABLE", "limit": 400}
```

```text
Found 108 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 12: CREATE TABLE recovery_case (

  Line 57: CREATE TABLE case_account (

  Line 74: CREATE TABLE case_party (

  Line 91: CREATE TABLE deviation (

  Line 112: CREATE TABLE queue (

  Line 134: CREATE TABLE assignment (

  Line 155: CREATE TABLE task (

  Line 176: CREATE TABLE timer (

  Line 201: CREATE TABLE party (

  Line 226: CREATE TABLE contact_point (

  Line 245: CREATE TABLE loan_account (

  Line 281: CREATE TABLE account_payment (

  Line 300: CREATE TABLE collateral (

  Line 325: CREATE TABLE account_collateral (

  Line 340: CREATE TABLE valuation (

  Line 364: CREATE TABLE asset (

  Line 391: CREATE TABLE treatment (

  Line 427: CREATE TABLE guarantee_claim (

  Line 446: CREATE TABLE legal_action (

  Line 471: CREATE TABLE notice (

  Line 496: CREATE TABLE hearing (

  Line 513: CREATE TABLE partner (

  Line 532: CREATE TABLE partner_instruction (

  Line 552: CREATE TABLE listing (

  Line 571: CREATE TABLE asset_sale (

  Line 593: CREATE TABLE debt_sale_lot (

  Line 616: CREATE TABLE debt_sale_account (

  Line 634: CREATE TABLE interaction (

  Line 675: CREATE TABLE document (

  Line 706: CREATE TABLE document_field (

  Line 725: CREATE TABLE document_custody (

  Line 743: CREATE TABLE decision_log_entry (

  Line 779: CREATE TABLE score (

  Line 799: CREATE TABLE proceeds (

  Line 819: CREATE TABLE write_off (

  Line 841: CREATE TABLE rule_row (

  Line 871: CREATE TABLE delegation_limit (

  Line 901: CREATE TABLE lov_value (

  Line 920: CREATE TABLE role (

  Line 938: CREATE TABLE permission (

  Line 954: CREATE TABLE template (

  Line 980: CREATE TABLE data_product (

  Line 1002: CREATE TABLE data_product_access (

  Line 1021: CREATE TABLE data_product_load (

  Line 1042: CREATE TABLE data_contract (

  Line 1065: CREATE TABLE sys_objects (

  Line 1084: CREATE TABLE sys_fields (

  Line 1113: CREATE TABLE sys_field_version (

  Line 1130: CREATE TABLE load_run (

  Line 1161: CREATE TABLE dq_exception (

  Line 1183: CREATE TABLE dq_rule (

  Line 1207: CREATE TABLE source_field_map (

  Line 1230: CREATE TABLE source_code_map (

  Line 1250: CREATE TABLE tracker_inventory (

  Line 1288: CREATE TABLE tracker_row (

  Line 1308: CREATE TABLE case_list_row (

  Line 1339: CREATE TABLE collections_history (

  Line 1361: CREATE TABLE reconciliation_result (

  Line 1385
... truncated (4,728 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now key detail: there is no physical table for PRODUCT, REGION, EXPOSURE_BAND, SERVICE_LEVEL, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER, TEAM, DOCUMENT_TYPE (there is document_type), ROLE (role), QUEUE (queue), QUEUE_MEMBER (queue_member), TEMPLATE (template), DELEGATION_LIMIT (delegation_limit), PERMISSION (permission), MASKING_RULE (masking_rule), PARTNER_USER (partner_user), PARAMETER -> parameter_value.

What about PRODUCT, REGION, EXPOSURE_BAND, TEAM, SERVICE_LEVEL, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER? They may be in lov_value lists (LOV-PRODUCT etc.), or they may have no table. Let's check the reference data design doc: 06 Data\Recovery Workbench Reference Data and Lists of Values v3.xlsx? Actually there's an md extraction. Let me glob.

Also need TSD P3 Case and workflow for reference-loads and reference data; P5 Document hub for Document TYPE loaders; plus CSV templates for PRODUCT etc. from RWB-E1-045.

Let me look at the schema table definitions for the relevant tables (parameter_value, parameter_catalog, reference_version, reference_row, queue, queue_member, service_level?, delegation_limit, template, document_type, document_checklist_item, retention? masking_rule, permission, partner_user, role).

Let me read specific line ranges.

</details>

**Tool `read`** - completed

```json
{"limit": 130, "offset": 1758, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 1758-1887
1758: CREATE TABLE queue_member (
1759:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1760:     queue_id uuid NOT NULL,
1761:     user_id uuid NOT NULL,
1762:     capacity integer,
1763:     skill_codes varchar(200),
1764:     table_version integer NOT NULL,
1765:     valid_from date NOT NULL,
1766:     valid_to date,
1767:     is_active boolean NOT NULL DEFAULT true,
1768:     state varchar(40),
1769:     version integer NOT NULL DEFAULT 1,
1770:     created_at timestamptz NOT NULL DEFAULT now(),
1771:     created_by uuid,
1772:     updated_at timestamptz NOT NULL DEFAULT now(),
1773:     updated_by uuid
1774: );
1775: 
1776: -- Queue measure: One snapshot of a queue's counts, ageing and breaches, published when it reconciles to the case list.
1777: CREATE TABLE queue_measure (
1778:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1779:     queue_id uuid NOT NULL,
1780:     as_of timestamptz NOT NULL,
1781:     depth integer NOT NULL,
1782:     unassigned integer NOT NULL,
1783:     avg_age_days numeric(7,2),
1784:     max_age_days integer,
1785:     owner_min integer,
1786:     owner_max integer,
1787:     breached integer NOT NULL,
1788:     status varchar(15) NOT NULL DEFAULT 'TAKEN',
1789:     is_active boolean NOT NULL DEFAULT true,
1790:     state varchar(40),
1791:     version integer NOT NULL DEFAULT 1,
1792:     created_at timestamptz NOT NULL DEFAULT now(),
1793:     created_by uuid,
1794:     updated_at timestamptz NOT NULL DEFAULT now(),
1795:     updated_by uuid,
1796:     CONSTRAINT uk_queue_measure UNIQUE (as_of)
1797: );
1798: 
1799: -- Parameter catalog: The definition of every parameter and environment setting, with its owner and default.
1800: CREATE TABLE parameter_catalog (
1801:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1802:     param_key varchar(100) NOT NULL,
1803:     kind varchar(15) NOT NULL,
1804:     value_type varchar(15) NOT NULL,
1805:     unit varchar(20),
1806:     min_value varchar(40),
1807:     max_value varchar(40),
1808:     default_value varchar(400),
1809:     scope varchar(10) NOT NULL DEFAULT 'GLOBAL',
1810:     required boolean NOT NULL DEFAULT false,
1811:     owner_role varchar(20) NOT NULL,
1812:     environments varchar(40),
1813:     used_by varchar(400),
1814:     secret boolean NOT NULL DEFAULT false,
1815:     description varchar(400) NOT NULL,

... truncated (5,569 chars total)
```

**Tool `read`** - completed

```json
{"limit": 70, "offset": 1851, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 1851-1920
1851: CREATE TABLE reference_version (
1852:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1853:     table_code varchar(30) NOT NULL,
1854:     version_no integer NOT NULL,
1855:     version_label varchar(20),
1856:     valid_from date NOT NULL,
1857:     valid_to date,
1858:     status varchar(15) NOT NULL DEFAULT 'VALIDATED',
1859:     author_user_id uuid NOT NULL,
1860:     approver_user_id uuid,
1861:     approved_at timestamptz,
1862:     row_count integer NOT NULL,
1863:     content_hash char(64) NOT NULL,
1864:     load_id uuid NOT NULL,
1865:     dry_run_counts jsonb,
1866:     rollback_reason varchar(400),
1867:     change_request_ref varchar(30),
1868:     impact_summary varchar(1000),
1869:     test_result varchar(10),
1870:     rollback_plan varchar(1000),
1871:     verified_by uuid,
1872:     verified_at timestamptz,
1873:     verify_note varchar(1000),
1874:     is_active boolean NOT NULL DEFAULT true,
1875:     state varchar(40),
1876:     version integer NOT NULL DEFAULT 1,
1877:     created_at timestamptz NOT NULL DEFAULT now(),
1878:     created_by uuid,
1879:     updated_at timestamptz NOT NULL DEFAULT now(),
1880:     updated_by uuid,
1881:     CONSTRAINT uk_reference_version UNIQUE (table_code, version_no)
1882: );
1883: 
1884: -- Reference row: One row of a reference table version held as data.
1885: CREATE TABLE reference_row (
1886:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1887:     version_id uuid NOT NULL,
1888:     row_key varchar(200) NOT NULL,
1889:     row_data jsonb NOT NULL,
1890:     is_active boolean NOT NULL DEFAULT true,
1891:     state varchar(40),
1892:     version integer NOT NULL DEFAULT 1,
1893:     created_at timestamptz NOT NULL DEFAULT now(),
1894:     created_by uuid,
1895:     updated_at timestamptz NOT NULL DEFAULT now(),
1896:     updated_by uuid,
1897:     CONSTRAINT uk_reference_row UNIQUE (row_key)
1898: );
1899: 
1900: -- Rule test case: A test case of the rule table test harness, with its expected and actual result.
1901: CREATE TABLE rule_test_case (
1902:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1903:     test_case_id varchar(20) NOT NULL,
1904:     route_set varchar(15) NOT NULL,
1905:     rule_version varchar(20) NOT NULL,
1906:     rule_id varchar(20) NOT NULL,
1907:     from_state varchar(60) NOT NULL,
1908:     event_code varchar(6
... truncated (3,071 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Note discrepancy: reference_row UNIQUE (row_key) in physical schema vs story's UNIQUE (version_id, row_key). Worth noting.

Now PARAMETER CSV columns. Need the TSD P3 Case and workflow reference, and the PARAMETER handler story (RWB-E1-027? Let's find). Grep for "PARAMETER handler", "parameter_value", "PARAMETER" CSV.

Also need TSD P3 sections on reference data service. Let's grep in P3 TSD for "reference" and "PARAMETER".

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P3 Case and workflow v2.md", "pattern": "reference-load|ReferenceLoad|ReferenceVersion|PARAMETER|parameter_value|LOV-REF-TABLE|ReferenceTable"}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P3 Case and workflow v2.md:
  Line 283: **parameter_value** (NEW). An approved, dated value version of a parameter per environment and product group.

  Line 305: | DF-REF-160 | table_code | LOV | varchar(30) | Yes | LOV-REF-TABLE | Workbench |

  Line 376: | LOV-REF-TABLE | PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, QUEUE_MEMBER, SERVICE_LEVEL, DOCUMENT_TYPE, DOCUMENT_CHECKLIST, RETENTION_CLASS, TEMPLATE, DELEGATION_LIMIT, PERMISSION, MASKING_RULE, PARTNER_USER, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER, PARAMETER, ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER |

```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P5 Document hub v2.md", "pattern": "reference-load|ReferenceLoad|ReferenceTableLoader|DOCUMENT_TYPE|DOCUMENT_CHECKLIST|RETENTION_CLASS|DOCUMENT_HUB_PARAMETER"}
```

```text
No matches found
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

P5 TSD doesn't mention reference loads. Let me search P5 for "document type" and "load".

Also need P3 TSD lines 270-400 for reference tables and the parameter model.

Let me read P3 TSD around 260-400.

</details>

**Tool `read`** - completed

```json
{"limit": 150, "offset": 255, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P3 Case and workflow v2.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P3 Case and workflow v2.md, lines 255-404
255: | DF-RPT-024 | unassigned | NUMBER | integer | Yes | None | Workbench |
256: | DF-RPT-025 | avg_age_days | NUMBER | numeric(7,2) | No | None | Workbench |
257: | DF-RPT-026 | max_age_days | NUMBER | integer | No | None | Workbench |
258: | DF-RPT-027 | owner_min | NUMBER | integer | No | None | Workbench |
259: | DF-RPT-028 | owner_max | NUMBER | integer | No | None | Workbench |
260: | DF-RPT-029 | breached | NUMBER | integer | Yes | None | Workbench |
261: | DF-RPT-030 | status | LOV | varchar(15) | Yes | LOV-SNAPSHOT-STATUS | Workbench |
262: 
263: **parameter_catalog** (NEW). The definition of every parameter and environment setting, with its owner and default.
264: 
265: | BR Field ID | Field | Data type | Physical type | Required | List | Source |
266: |---|---|---|---|---|---|---|
267: | DF-REF-132 | id | TEXT | uuid | Yes | None | Workbench |
268: | DF-REF-133 | param_key | TEXT | varchar(100) | Yes | None | Workbench |
269: | DF-REF-134 | kind | TEXT | varchar(15) | Yes | None | Workbench |
270: | DF-REF-135 | value_type | TEXT | varchar(15) | Yes | None | Workbench |
271: | DF-REF-136 | unit | TEXT | varchar(20) | No | None | Workbench |
272: | DF-REF-137 | min_value | TEXT | varchar(40) | No | None | Workbench |
273: | DF-REF-138 | max_value | TEXT | varchar(40) | No | None | Workbench |
274: | DF-REF-139 | default_value | TEXT | varchar(400) | No | None | Workbench |
275: | DF-REF-140 | scope | LOV | varchar(10) | Yes | LOV-PARAM-SCOPE | Workbench |
276: | DF-REF-141 | required | BOOLEAN | boolean | Yes | None | Workbench |
277: | DF-REF-142 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
278: | DF-REF-143 | environments | TEXT | varchar(40) | No | None | Workbench |
279: | DF-REF-144 | used_by | TEXT | varchar(400) | No | None | Workbench |
280: | DF-REF-145 | secret | BOOLEAN | boolean | Yes | None | Workbench |
281: | DF-REF-146 | description | TEXT | varchar(400) | Yes | None | Workbench |
282: 
283: **parameter_value** (NEW). An approved, dated value version of a parameter per environment and product group.
284: 
285: | BR Field ID | Field | Data type | Physical type | Required | List | Source |
286: |---|---|---|---|---|---|---|
287: | DF-REF-147 | id | TEXT | uuid | Yes | None | Workbench |
288: 
... truncated (10,852 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P5 Document hub v2.md", "pattern": "load|Load", "limit": 60}
```

```text
Found 5 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P5 Document hub v2.md:
  Line 37: P5 Document hub is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: store, index, OCR, classification, extraction, review queue, retention, custody. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

  Line 279: | document_intake | run_id | load_run | Many to 0 or 1 |

  Line 441: | Purpose | Upload a document to the case |

  Line 474: | Purpose | Download the document content |

  Line 562: | Purpose | Download the file of a held intake item for the reviewer |

```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

The P5 TSD does not define reference-load handling for DOCUMENT_TYPE etc. Note that.

Now the PARAMETER code: find story that builds ParameterLoadHandler and the exact CSV columns. Grep for "ParameterLoadHandler", "param_key", "environment", "param_value" CSV.

Also the RWB E1 042 configuration service story may define the parameter CSV template. Let's search.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "ParameterLoadHandler|param_key,environment|key,environment,value"}
```

```text
Found 13 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md:
  Line 13523: | ParameterLoadHandler | Service | Handler behind POST /admin/reference-loads for table PARAMETER; approve and rollback |

  Line 13546: 4. ParameterLoadChecks and ParameterLoadHandler with approve and rollback; tests AC5, AC6, AC7, AC10.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 042 Central configuration service and parameter catalog v1.md:
  Line 241: | ParameterLoadHandler | Service | Handler behind POST /admin/reference-loads for table PARAMETER; approve and rollback |

  Line 264: 4. ParameterLoadChecks and ParameterLoadHandler with approve and rollback; tests AC5, AC6, AC7, AC10.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-003-epic-1-RWB-E1-042\specify\spec.md:
  Line 25: | New Nodes Required | `YES` — `ParameterService`, `ParameterCatalogRepository`, `ParameterValueRepository`, `ParameterLoadChecks`, `ParameterLoadHandler`, `ParameterCatalogController`, `ParameterStartupCheck`, `ParameterKeysGenerator`, `RwbMagicNumberCheck`, `CatalogCompletenessCheck`. |

  Line 138: | `ParameterLoadHandler` | Service | Handler behind the reference-load endpoint; approve and rollback. |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-003-epic-1-RWB-E1-042\build\E1-042 migration and clarification notes.md:
  Line 61: key,environment,value


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-v7.md:
  Line 13540: | ParameterLoadHandler | Service | Handler behind POST /admin/reference-loads for table PARAMETER; approve and rollback |

  Line 13563: 4. ParameterLoadChecks and ParameterLoadHandler with approve and rollback; tests AC5, AC6, AC7, AC10.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 042 Central configuration service and parameter catalog v1.md:
  Line 232: | ParameterLoadHandler | Service | Handler behind POST /admin/reference-loads for table PARAMETER; approve and rollback |

  Line 255: 4. ParameterLo
... truncated (3,042 chars total)
```

**Tool `glob`** - completed

```json
{"pattern": "**/RWB E1 04*.md"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 044 Database migrations versioned with parameterized schema names v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 049 OCR pipeline on the Workbench document hub v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 043 Reference data service with versioned tables v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 048 Rule change audit report v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 042 Central configuration service and parameter catalog v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 047 Feature flags for module release with a removal date v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 041 Retention classes and virus scan on intake v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 046 Template and merge field catalog as data v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 040 Document checklist per case type as reference data v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 044 Database migrations versioned with parameterized schema names v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 043 Reference data se
... truncated (4,579 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Read RWB E1 042 fully — it likely defines the PARAMETER load CSV and validation, and maybe the parameter table code.

Also read the build notes file: "INC-003-epic-1-RWB-E1-042\build\E1-042 migration and clarification notes.md" line 61 has CSV header "key,environment,value" — this is a build artifact clarification. Very relevant.

Let's read both.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 042 Central configuration service and parameter catalog v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 042 Central configuration service and parameter catalog v1.md, lines 1-328
1: # RWB-E1-042 Central configuration service and parameter catalog
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-E1-042 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | FEAT-CWC-22 Hold the parameter catalog and configuration service |
14: | Requirement IDs | REQ-DRI-010 |
15: | BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
16: | L3 process | 14 Set strategy, policy and decision rules |
17: | Decision | D6 entry |
18: | Priority | Must |
19: | Depends on | RWB-E1-044 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.
25: 
26: ## 2. Business rationale
27: 
28: Thresholds such as the 90-day entry point are written into code and spreadsheets today, so a change needs a release and nobody can say who owns a value. This story holds every parameter definition in a catalog with an owner and a default, holds business values as approved, dated versions per environment, serves them to every engine at run time, and fails the build when code carries a literal business value or reads a parameter the catalog does not list. It meets REQ-DRI-010 and puts Principle 1 (DT02) into the build pipeline.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-044 is done: the recovery schema exists in each environment.
33: - The catalog seed file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, with the Epic 1 entries, including `case.entry.dpd` (default 90; DL16), `refdata.cache.ttl-seconds` (default 300; DL11) and `caselist.export.maxrows` (default 10000; DL11).
34: - The ACE secret store holds secrets per environment; the catalog lists them and never holds their values.
35: - Loaders hold Reference data C (RW-COE, RW-REFADM). Approvers hold Reference data A: the parameter owner, and RW-
... truncated (21,435 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Key: PARAMETER request: file (rows of key, environment, value), table = "PARAMETER", validFrom.

Now the build notes for INC-003 clarify CSV header "key,environment,value". Let's read that file (may provide exact columns and behaviour). This is a build artifact in 13 AI-First SDLC repository/output — it's a clarification note, likely highly relevant for "exact contract". Read it.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\output\\INC-003-epic-1-RWB-E1-042\\build\\E1-042 migration and clarification notes.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-003-epic-1-RWB-E1-042\build\E1-042 migration and clarification notes.md, lines 1-185
1: # RWB-E1-042 — migration files and answers to the build questions
2: 
3: Prepared 10 November 2026. Sources: story `RWB E1 042 Central configuration service and parameter catalog v1`, build notes Epic 1 v4, technical specification `INC-003-epic-1-RWB-E1-042`, API Specification v2, and the E1-001 / E1-019 / E1-043 / E1-044 stories.
4: 
5: ## 1. Files in this folder
6: 
7: | File | What it does |
8: |---|---|
9: | `V042_1__parameter_catalog.sql` | Creates `parameter_catalog` and `parameter_value`, their checks, the foreign key and the partial index on approved values. Guarded so it is also safe on top of the E1-001 baseline. |
10: | `V042_2__parameter_seed.sql` | Inserts the catalog rows and their version 1 default values for DEV, SIT, UAT and PROD. Generated-file shape; idempotent. |
11: | `V0042__rwb_e1_042_parameter_catalog_and_seed.sql` | The same content as one D-RCV-28-compliant migration. Commit this one unless a lint exception for the split is approved. |
12: 
13: All three SQL files use the Flyway placeholder `${recoverySchema}` (D-RCV-28), not a literal schema name.
14: 
15: The seed covers the rows E1-042 itself defines: `case.entry.dpd`, `refdata.cache.ttl-seconds`, `config.cache.ttl-seconds`, `caselist.export.maxrows` and the secret `ace.db.password`. The full Epic 1 catalog is the CSV `config/parameter-catalog.csv`, which is not in this pack; see OI-E1-042-003 before SIT.
16: 
17: AC8's SIT value of 30 is a test load over the seeded 300, not a seed exception. The seed carries the catalog default (300) in every environment; the test sets SIT to 30 through a version 2 load.
18: 
19: ## 2. Read this before committing the migration
20: 
21: The requested names are the names in story §13, but they do not pass the migration lint that was ruled after the story was written.
22: 
23: | Rule | Source | Effect on the requested split |
24: |---|---|---|
25: | Recovery Flyway files are `V<seq>__<story>_<name>.sql`, four-digit sequence in merge order, line 1 `-- Story: <story key>` | D-RCV-28, E1-044 §13 | `V042_1__...` and `V042_2__...` fail the name pattern. |
26: | One migration file per story; the lint fails when a story key appears in two files | E1-044 BR3, AC6 | Two files carrying `RWB-E1-042` fail the lint. |
27: | Schema is referenced only as `${rec
... truncated (17,659 chars total)
```

> **Synthetic** - 2026-11-10 18:21

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\AGENTS.md
# Recovery Workbench — AI engineering standards

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md`.

## 1. The seven working rules

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files: the standards file, the story file and the plan file. Anything the
   agent needs is in one of the three.
3. The tests and the acceptance criteria exist before the code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
6. No personal data or production data goes into a prompt, a test or a log.
7. The unit of work is one story. Work is merged at least once a working day.

## 2. Structure and stack

- The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
- Back end: Spring Boot (Java), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL. Schema changes use versioned migrations (Flyway or Liquibase), one migration
  per story, forward-only in production. Files are named `V<seq>__<story>_<name>.sql`, where `<seq>`
  is a four-digit sequence taken in merge order. The schema is referenced only as
  `${recoverySchema}` and is `recovery` in every environment (D-RCV-28, D-RCV-17).
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. The collection module uses the same terms.
- Hosting: the ACE namespace on the shared ACE AKS clusters.

## 3. The agent must

1. Put recovery code in the recovery module folder only. Change the common or collection module only
   where the story file names it.
2. Read every threshold, limit, timer, queue, role, template and route from its versioned reference
   table. Never write one as a literal in code.
3. Put a Spring Security method check on every endpoint, naming the capability area and the operation.
4. Write a decision record entry for every change to a case and every decision, with the rule ID and
   version used.
5. Use the names in the business glossary for classes, fields, tables and endpoints.
6. Return each validation message from the message table by its rule ID.
7. Make database changes by migration script only, one script per story. Name it
   `V<seq>__<story>_<name>.sql`; line 1 is `-- Story: <story key>`. A corrective script takes the
   next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>` (D-RCV-28).
8. Use Spring Batch and Quartz for scheduled work.
9. Use the synthetic data generator for test data.
10. Write the test before the code. A change with no test is not complete.
11. Respect module boundaries: call another module only through its published interface or an
    application event. Never read another module's tables.
12. Keep unfinished or cross-squad work behind a feature flag that returns the previous code path
    when off.

## 4. The agent must never

1. Commit a credential, key or token.
2. Call or read the inside of another module.
3. Call a system o...

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now I need to check the remaining items:
- P5 TSD for DOCUMENT_HUB_PARAMETER (not in LOV-REF-TABLE list! interesting). The yaml says accept P5 codes DOCUMENT_TYPE, DOCUMENT_CHECKLIST, RETENTION_CLASS, DOCUMENT_HUB_PARAMETER. But LOV-REF-TABLE in schema has 25 codes not including DOCUMENT_HUB_PARAMETER. Discrepancy worth noting.
- Check RWB E1 019 queue CSV columns maybe. And E1-045 for PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL templates. E1-037 for permission/masking. The build notes table gives columns.

Let me read E1-045 for product parameter template/Csv, and E1-019 contract for queue CSV. Also E1-025 document type §13 and E1-040/E1-041.

Also confirm "13 table codes" vs 25.

Let me read the E1-045 story file's contract and data sections.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md", "pattern": "template|CSV|column|Header|header|PRODUCT_PARAMETER|SERVICE_LEVEL|product_parameter|service_level"}
```

```text
Found 25 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md:
  Line 35: - Tables PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL have an approved version in force.

  Line 41: 1. Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status.

  Line 43: 3. Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.

  Line 48: 8. Each engine: records the PRODUCT_PARAMETER version used in its decision log entry inputs (written by the owning story).

  Line 54: | X1 | A product has no SERVICE_LEVEL row for a required status | The load is refused in full and the missing product and status are named | MSG-P3-034 | AC3 |

  Line 79:     Given PRODUCT_PARAMETER version 2 is in force with NOTICE_PERIOD_DAYS 30 calendar days for "MORTGAGE" and 60 calendar days for "HIRE_PURCHASE"

  Line 87:     Then each timer start records PRODUCT_PARAMETER version 2

  Line 91:     Given PRODUCT_PARAMETER version 3 and SERVICE_LEVEL version 3 add every required row for "AUTO_LEASE" with valid from 2026-12-05

  Line 99:     Given a SERVICE_LEVEL load with valid from 2026-12-10 that has no row for "SSME" and status "WAITING_PARTNER"

  Line 102:     Then SERVICE_LEVEL version 3 stays in force

  Line 106:     When a PRODUCT_PARAMETER load sets NOTICE_PERIOD_DAYS to 0 for "SSME"

  Line 110:     Given a PRODUCT_PARAMETER load with two NOTICE_PERIOD_DAYS rows for "MORTGAGE", 30 and 45

  Line 127:     Given PRODUCT_PARAMETER version 4 with NOTICE_PERIOD_DAYS 45 for "MORTGAGE" takes effect on 2026-12-03

  Line 137: | BR1 | Every product-specific value is a PRODUCT_PARAMETER or SERVICE_LEVEL row keyed by product group; no engine holds a product value or a product name in code | Principle 1; DT02 |

  Line 139: | BR3 | Every product in force has one SERVICE_LEVEL row per status in `servicelevel.required-statuses` (assumed NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL; DL22) | REQ-CWC-011; casemodel.txt Case stat
... truncated (4,159 chars total)
```

**Tool `grep`** - error

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 019 Queues teams and capacity v1.md", "pattern": "CSV|column|Header|header|QUEUE_MEMBER|template"}
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Find E1-019 story filename.

</details>

**Tool `glob`** - completed

```json
{"pattern": "**/RWB E1 019*.md"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 019 Roles teams and queues as data v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 019 Roles teams and queues as data v1.md
```

**Tool `read`** - completed

```json
{"limit": 60, "offset": 180, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md, lines 180-239
180: 
181: The timer rows are written through the timer engine of RWB-E1-028, which also writes the decision log entry for each timer start. Field IDs are those in the Logical Data Model and Data Dictionary.
182: 
183: ## 12. Contract
184: 
185: **POST /api/recovery/v1/admin/reference-loads** (P4 endpoint; the completeness check runs inside the RWB-E1-043 registry)
186: 
187: | Item | Value |
188: |---|---|
189: | Request | multipart/form-data: `file`, `table` (PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL), `validFrom` |
190: | Response | 201 `ReferenceLoad` (`id`, `table`, `validFrom`, `status`, `rows`) |
191: | Errors | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 open cases on a removed product (MSG-P3-027); 422 missing required row (MSG-P3-034), value out of range (MSG-GEN-002), duplicate key (MSG-P3-027); 503 |
192: | Authorization | Reference data, right C |
193: | Idempotency | As RWB-E1-043: table code, valid from and content hash |
194: 
195: **GET /api/recovery/v1/cases/{caseId}/timers** (P3) returns `Timer[]` (`timerType`, `startedAt`, `expiresAt`, `warnAt`, `status`). Case record R. Errors 401, 403, 404 (MSG-P4-003), 503. Used to check AC1, AC2 and AC8.
196: 
197: **Published interface** (package `recovery.casewf.refdata.api`):
198: 
199: ```java
200: public interface ProductParameterService {
201:     ProductParameter get(String productGroup, String parameterCode, LocalDate businessDate);
202:     ServiceLevel serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);
203: }
204: 
205: public record ProductParameter(String productGroup, String parameterCode, String value,
206:                                String unit, String tableCode, int versionNo) {}
207: 
208: public record ServiceLevel(String productGroup, String caseStatus, int limit, String unit,
209:                            int warnPercent, String escalateToRole, int versionNo) {}
210: ```
211: 
212: Both methods throw `MissingProductParameterException(productGroup, parameterCode, businessDate)` when no row is in force. No events are published by this story.
213: 
214: ## 13. Solution plan
215: 
216: **Package.** `recovery.casewf.refdata.product` in the recovery module; published types in `recovery.casewf.refdata.api`.
217: 
218: **Components*
... truncated (4,865 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Important: E1-045 says PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL rows are stored in reference_version/reference_row (no new table). It says "No new table. Reads reference_version and reference_row". So those codes write reference_row only, not product table. Good.

Now E1-019 queue CSV. Let's grep in the right file.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 019 Roles teams and queues as data v1.md", "pattern": "CSV|column|Header|header|QUEUE_MEMBER|template|sheet"}
```

```text
Found 29 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 019 Roles teams and queues as data v1.md:
  Line 24: As a **reference data administrator (RW-REFADM)**, I want **queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data loaded from the Excel template**, so that **the organization changes without a code release**.

  Line 28: Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. This story holds every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables QUEUE and QUEUE_MEMBER, loaded from one template through the reference data service, with an approver and a one-call rollback, and applies the version in force to the queue tables the engines use. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation (RWB-E1-020), to scope by team (RWB-E1-037) and to control CTL-08.

  Line 32: - RWB-E1-043 is done: ReferenceVersionRegistry and ReferenceDataService hold versions of reference tables, and POST /admin/reference-loads calls them; QUEUE is a LOV-REF-TABLE code and QUEUE_MEMBER is added to it (see additions).

  Line 40: 1. RW-REFADM: fills the Queues template (sheets QUEUE and QUEUE_MEMBER) and calls POST /admin/reference-loads once per sheet with valid from 2026-11-30.

  Line 44: 5. QueueVersionApplier: on the valid from date, applies the QUEUE and QUEUE_MEMBER versions in force to the queue and queue_member tables: upsert by queue code keeping the queue ID, replace active member rows, set table_version.

  Line 61: | X9 | A required column is empty | Load refused in full | MSG-GEN-001 | AC12 |

  Line 69: | Negotiable | Team codes, queues, caps and members are data; the template layout can change with the checks |

  Line 85:     Given the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows

  Line 86:     When the QUEUE and QUEUE_MEMBER sheets are loaded as version 1 with valid from 2026-11-30 and approved

  Line 107:     Given the QUEUE sheet has queue "XYZ-CO" on row 7 with team code "XYZ"

  Line 114:     When the QUEUE sheet is loaded

  Line 130:     Given the QUEUE sheet for valid from 2026-12-15 was loaded as version 5

  Line 142:     Given member U-12 on row 22 of the QUEUE_MEMBER sheet is li
... truncated (4,259 chars total)
```

**Tool `grep`** - error

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 037 Permission matrix and masking rules as data v1.md", "pattern": "CSV|column|Header|header|template|matrix_version|masking_version"}
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

**Tool `read`** - completed

```json
{"limit": 75, "offset": 205, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 019 Roles teams and queues as data v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 019 Roles teams and queues as data v1.md, lines 205-279
205: | DF-CAS-005 | recovery_case | status | Read |
206: | DF-CAS-009 | recovery_case | owner_user_id | Read |
207: | DF-CAS-010 | recovery_case | queue_id | Read |
208: 
209: reference_version and reference_row are new entities of RWB-E1-043, read here through ReferenceDataService. Field IDs are those in the Logical Data Model and Data Dictionary.
210: 
211: ## 12. Contract
212: 
213: **POST /api/recovery/v1/admin/reference-loads** (P4 endpoint, RWB-E1-043)
214: 
215: | Item | Value |
216: |---|---|
217: | Request | multipart/form-data: file (xlsx sheet), table = "QUEUE" or "QUEUE_MEMBER", validFrom (date) |
218: | Response | 201 ReferenceLoad: id, table, validFrom, status, rows |
219: | Errors | 401 (MSG-P4-001); 403 no Reference data C (MSG-P4-002); 422 a row fails (MSG-GEN-001, MSG-GEN-002; queue checks as MSG-P1-002 with the rows in Problem.detail); 503 |
220: | Authorization | Reference data, right C |
221: | Idempotency | Table code, valid from and content hash (RWB-E1-043) |
222: 
223: **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint)
224: 
225: | Item | Value |
226: |---|---|
227: | Response | 200 ReferenceLoad with status APPROVED |
228: | Errors | 401; 403 no Reference data A; 404; 409 approver is the author (MSG-P7-002) or the version changed (MSG-GEN-004); 503 |
229: | Authorization | Reference data, right A |
230: 
231: **POST /admin/reference-loads/{loadId}/rollback** (new endpoint, see additions)
232: 
233: | Item | Value |
234: |---|---|
235: | Request | Path loadId (uuid); body { reason: string, required } |
236: | Response | 200 ReferenceLoad with status ROLLED_BACK |
237: | Errors | 401; 403 no Reference data U; 404; 409 no earlier version (MSG-P3-015); 422 reason empty (MSG-GEN-001); 503 |
238: | Authorization | Reference data, right U |
239: | Idempotency | Idempotency-Key header; a repeat returns the first result |
240: 
241: **Published interfaces**
242: 
243: ```java
244: // P3, package recovery.casewf.queues.api (published)
245: public interface CapacityService {
246:     CapacityAnswer check(UUID queueId, UUID userId, LocalDate onDate);
247:     List<QueueMemberView> membersInForce(UUID queueId, LocalDate onDate);
248: }
249: public record CapacityAnswer(Status status, int openCases, int capacit
... truncated (4,191 chars total)
```

**Tool `glob`** - completed

```json
{"pattern": "**/RWB E1 03*.md"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 039 Access log into the decision log and break glass admin v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 038 Delegation of authority table as reference data v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 035 Case record view v1 1 with documents and history timeline v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 034 Letter template management v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 033 Search across cases v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 032 Automatic attach from the OCR intake v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 031 Queue and owner on the case list with filters v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 030 Daily rebalancing and queue measures v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 034 Letter template management v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 033 Search across cases v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 032 Automatic attach from the OCR intake v1.md
C:\U
... truncated (4,070 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Read E1-037 contract + data for permission/masking CSV columns and whether they write tables permission/masking_rule or reference_row. Also E1-038 delegation_limit, E1-046 template, E1-040 checklist, E1-041 retention, E1-025 document type, E1-034 maybe service level? Let me grep efficiently.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md", "pattern": "template|column|header|matrix_version|masking_version|CSV|write|Writes|reference_row|permission|masking_rule"}
```

```text
Found 44 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md:
  Line 1: # RWB-E1-037 Role to permission matrix as data and PDPA field masking by role

  Line 13: | Feature | FEAT-ACA-04 Hold the role to permission matrix as data; FEAT-ACA-05 Mask PDPA fields by role; FEAT-ACA-13 Apply joiner, mover and leaver changes to access; FEAT-ACA-14 Scope a user's cases by team and region |

  Line 28: Audit findings record unsuitable user access to EFS and staff sending debtor data outside the bank. Today rights are set inside each system and cannot be shown for a past date. This story holds the permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned data, applies scope before permission on every request, and ends access at the next request when a person leaves. It meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and puts controls CTL-09, CTL-10 and CTL-11 in place. The measure is rule and limit changes made without a code release: target 100 percent (FSD P4 A2.4).

  Line 34: - RWB-E1-027 is done: the decision log writer is available through its published interface.

  Line 35: - Permission matrix version PM-2026.11 (from the Users, roles and permissions workbook) is the version in force.

  Line 38: - Parameters `rwb.refload.approver.permission=RW-SECADM` and `rwb.refload.approver.masking_rule=RW-COMPLY` are in the parameter catalog (RWB-E1-042).

  Line 42: 1. Reference data administrator (RW-REFADM): prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls POST /admin/reference-loads with table "permission" and validFrom.

  Line 43: 2. Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.

  Line 45: 4. Workbench: checks that the approver holds the role the parameter names for the table and is not the person who loaded it; writes one decision log entry for the approval with decision code AC-VERS and no case; marks the version Approved with its valid from date.

  Line 61: | X6 | The decision log write for an approval fails | The version is not ap
... truncated (7,501 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 038 Delegation of authority table as reference data v1.md", "pattern": "template|column|header|CSV|reference_row|delegation_limit|Writes"}
```

```text
Found 25 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 038 Delegation of authority table as reference data v1.md:
  Line 33: - RWB-E1-029 is done: the rule load template and rollback by one call exist for versioned tables.

  Line 35: - The delegation_limit table exists (RWB-E1-001).

  Line 37: - Parameter `rwb.refload.approver.delegation_limit=RW-RISK` is in the parameter catalog (RWB-E1-042).

  Line 43: 2. RW-REFADM: calls POST /admin/reference-loads with table "delegation_limit", validFrom and the version name, for example DOA-2026.11.

  Line 68: | Independent | Uses the load service (RWB-E1-043), the rule load template (RWB-E1-029) and the writer (RWB-E1-027) |

  Line 86:     When "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it

  Line 145: | BR1 | Limits are held as the regulation states them: principal limit in baht, loss as a percentage, maximum loss in baht, payment or price against fair market value, and price against principal outstanding; an empty limit means no limit | delegation_limit fields DF-REF-020 to DF-REF-022; Delegation of authority matrix, Key sheet |

  Line 176: | DF-REF-016 to DF-REF-026 | delegation_limit | all fields | Write (rows of each new version); read by the lookup |

  Line 177: | DF-REF-055 | delegation_limit | limit_version | Write, read |

  Line 178: | DF-REF-056 | delegation_limit | regulation_item | Write, read |

  Line 179: | DF-REF-057 | delegation_limit | applies_when | Write, read |

  Line 180: | DF-REF-058 | delegation_limit | max_loss_amount | Write, read |

  Line 181: | DF-REF-059 | delegation_limit | max_delay_count | Write, read |

  Line 182: | DF-REF-060 | delegation_limit | min_price_pct_principal | Write, read |

  Line 183: | DF-REF-061 | delegation_limit | min_received_pct | Write, read |

  Line 184: | DF-REF-062 | delegation_limit | max_term_years | Write, read |

  Line 198: | Request | Multipart: file, table "delegation_limit", validFrom |

  Line 202: | Idempotency | Idempotency-Key header |

  Line 212: | Idempotency | Idempotency-Key header |

  Line 230: | AccessAndAdministrationController | Controller | Reference load and approve for table delegation_limit |

  Line 235: | DelegationLimit | Entity | Maps delegation_limit with the new columns |

  Line 237: - Database: writes delegation_limit (decision_code, approval_level, product_
... truncated (3,760 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Need E1-046 template columns (already in build notes), E1-040 checklist, E1-041 retention, E1-025 document type. Let me grep the §13 of those stories for "columns" or "template". Also E1-034 letter template management perhaps defines the template table columns, but E1-046 owns template load.

Also check E1-024 DOCUMENT_HUB_PARAMETER story (in LOV? not). And whether P5 TSD mentions it.

Let me batch grep.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 040 Document checklist per case type as reference data v1.md", "pattern": "column|header|CSV|template|document_checklist_item|sheet"}
```

```text
Found 5 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 040 Document checklist per case type as reference data v1.md:
  Line 172: | Standard column | document | is_active | Read |

  Line 173: | DF-REF-234 to DF-REF-243 | document_checklist_item | all fields | Write (this story creates the record) |

  Line 236: - Flyway migration `V1_5_040__document_checklist.sql` creates document_checklist_item (id, stage_code varchar(20), route_code varchar(4), document_type varchar(30), required boolean, sort_order integer, table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (stage_code, route_code, document_type, table_version); and case_document_check (id, case_id uuid, checklist_version varchar(20), required_count integer, present_count integer, missing_types jsonb, complete boolean, checked_at timestamptz, last_event_id uuid, standard columns) with unique (case_id).

  Line 237: - Index ix_checklist_stage on document_checklist_item (stage_code, valid_from).

  Line 294: - No business value in code: stages, routes and required types are rows in document_checklist_item.

```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 041 Retention classes and virus scan on intake v1.md", "pattern": "column|header|CSV|template|retention_class"}
```

```text
Found 8 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 041 Retention classes and virus scan on intake v1.md:
  Line 32: - RWB-E1-024 is done: documents carry retention_class and write_once from the type table.

  Line 181: | DF-DOC-009 | document | retention_class | Read |

  Line 183: | Standard column | document | state | Write |

  Line 184: | Standard column | document | created_at | Read, as the stored date |

  Line 254: | RetentionClassRepository | Repository | Reads and writes retention_class only |

  Line 258: - Flyway migration `V1_5_041__retention_class.sql` creates retention_class (id, class_code varchar(10), period_months integer, end_action varchar(12), table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (class_code, table_version), check period_months > 0 and check end_action in ('ARCHIVE','REVIEW'); adds to document_intake: scanned_at timestamptz, the time of the malware scan (scan_result is created in RWB-E1-049).

  Line 259: - Adds table retention_action (id, document_id, run_month char(7), action varchar(12), decided_entry_id uuid, standard columns) with unique (document_id, run_month) for the idempotency key.

  Line 260: - Index ix_document_retention on document (retention_class, created_at) where is_active.

```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 046 Template and merge field catalog as data v1.md", "pattern": "column|header|CSV|template_code|merge_field|sheet|TemplateLoadHandler"}
```

```text
Found 25 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 046 Template and merge field catalog as data v1.md:
  Line 36: - The person loading holds RW-REFADM (Reference data C). Legal counsel (RW-LEGAL) approves each template version through RWB-E1-034, or through the approval columns of the load file in Epic 1 before that screen is live.

  Line 40: 1. Reference data administrator: loads the merge field catalog file through POST /admin/reference-loads with table "merge_field" and a valid from date.

  Line 145: None. This story does not change a case status. It sets the template version state (standard column state): Draft on load without an approver, Approved on load with an approver, Withdrawn when Legal withdraws it (RWB-E1-034). The reference load status moves from loaded to refused or in force.

  Line 164: | DF-REF-046 | template | template_code | Write |

  Line 177: | Standard column | template | state | Write |

  Line 178: | DF-REF-252 | merge_field | id | Write |

  Line 179: | DF-REF-253 | merge_field | merge_code | Write |

  Line 180: | DF-REF-254 | merge_field | source_entity | Write |

  Line 181: | DF-REF-255 | merge_field | source_field | Write |

  Line 182: | DF-REF-256 | merge_field | field_id | Write |

  Line 183: | DF-REF-257 | merge_field | is_required | Write |

  Line 184: | DF-REF-258 | merge_field | personal_data | Write |

  Line 185: | DF-REF-259 | merge_field | catalog_version | Write |

  Line 186: | DF-REF-260 | merge_field | valid_from | Write |

  Line 198: | Request | multipart/form-data: file, table ("template" or "merge_field"), validFrom |

  Line 208:     String table();                                   // "template" or "merge_field"

  Line 233: | TemplateEntity | Entity | Maps table template with the new columns |

  Line 234: | MergeFieldEntity | Entity | Maps table merge_field |

  Line 236: | MergeFieldRepository | Repository | Reads and writes merge_field by catalog version |

  Line 237: | TemplateLoadHandler | Service | ReferenceLoadHandler for table "template": parses rows, assigns versions, applies BR1 to BR6 |

  Line 238: | MergeFieldLoadHandler | Service | ReferenceLoadHandler for table "merge_field": checks field IDs against sys_fields |

  Line 242: - Database: table template (Recovery Workbench Physical Schema v4.sql) gets the new columns approved_by uuid, approved_at timestamptz, valid_from date,
... truncated (3,686 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now check the E1-024 document hub parameter story and E1-025 document type, to determine LOV code membership and CSV headers. Also check if DOCUMENT_HUB_PARAMETER appears anywhere as a LOV-REF-TABLE code.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "DOCUMENT_HUB_PARAMETER", "limit": 40}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml:
  Line 2983:         RETENTION_CLASS (RWB-E1-041) and DOCUMENT_HUB_PARAMETER (RWB-E1-024), validated by the P5 ReferenceTableLoader implementations; a failed


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-003-epic-1-RWB-E1-042\build\E1-042 migration and clarification notes.md:
  Line 39: - `table` is a required multipart field. Its value must be a code in `LOV-REF-TABLE` (25 codes in TSD P3; E1-043 serves 13, P5 adds `DOCUMENT_TYPE`, `DOCUMENT_CHECKLIST`, `RETENTION_CLASS` and `DOCUMENT_HUB_PARAMETER`, and later stories add more).


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v2.yaml:
  Line 2983:         RETENTION_CLASS (RWB-E1-041) and DOCUMENT_HUB_PARAMETER (RWB-E1-024), validated by the P5 ReferenceTableLoader implementations; a failed

```

**Tool `glob`** - completed

```json
{"pattern": "**/RWB E1 02*.md"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 029 Rule load validation and rollback v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 028 Service levels timers escalation and prescription dates v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 027 Decision log writer v1 v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 026 Attach and search screen v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 025 Document types and fields agreed v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 024 Document store and index v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 023 Case record view v1 read only v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 022 Sign on with SSO MFA and the first roles v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 021 Transfer rules and engine v1 v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 020 Allocation and assignment engine v1 v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 029 Rule load validation and rollback v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 028 Service levels timers escalation and prescription dates v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04
... truncated (4,313 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

E1-024 doesn't mention DOCUMENT_HUB_PARAMETER at all? grep only found 3 places, none in E1-024 story. Interesting: document_hub_parameter table exists in the physical schema, but the code isn't in LOV-REF-TABLE. This is a genuine gap. Let me check E1-024 for the table code and its load path.

Also E1-025 document type CSV columns.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 024 Document store and index v1.md", "pattern": "reference-load|table code|document_hub_parameter|load|LOV-REF"}
```

```text
Found 17 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 024 Document store and index v1.md:
  Line 37: - Document hub parameters loaded (this story creates the table): INTAKE_ALLOWED_TYPES = PDF, JPG, PNG; INTAKE_MAX_FILE_MB = 25, assumed (DL11). RWB-E1-053 and RWB-E1-057 read the same table.

  Line 38: - The caller is the upload service (RWB-E1-026, user with Documents C) or the intake (RWB-E1-032, SY-OCR). A reader holds Documents R with the case in scope.

  Line 75: | Valuable | Every later document path (upload, OCR intake, generation) stores through this one service |

  Line 195: | RW-CASEOWN, RW-LITOFF, RW-RESTRUCT and the other roles with Documents C | Store through the upload in RWB-E1-026 |

  Line 215: | DF-REF-245 | document_hub_parameter | param_code | Read |

  Line 216: | DF-REF-246 | document_hub_parameter | param_value | Read |

  Line 265: **Event published:** DocumentStored (EV-16), payload documentId, caseId, type, source, written to the outbox in the store transaction.

  Line 281: | DocumentHubParameters | Rule table | Reads document_hub_parameter rows in force, cached for 5 minutes; used by every P5 package |

  Line 284: | DocumentDetailPanel | React component | Opens from SCR-30; shows metadata, extracted fields, versions and the download button |

  Line 288: - Flyway migration `V1_5_024__document_store.sql`: adds document.previous_version_id uuid null with a foreign key to document(id) and document.content_sha256 char(64) not null; creates document_hub_parameter (id, param_code varchar(40), param_value varchar(200), unit varchar(20), table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (param_code, table_version).

  Line 292: - Document type table (RWB-E1-025), loaded by the reference data administrator.

  Line 293: - Parameters INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB in document_hub_parameter, loaded by the reference data administrator.

  Line 295: - Decision code DOCATT, assumed; the LOV-DECISION list is loaded by the data steward.

  Line 306: 9. Build DocumentDetailPanel; component test for the version list and the download.

  Line 321: | MSG-GEN-004 | Concurrent version | Someone else changed this record. Reload it to see their change. |

  Line 331: SCR-30 Case documents (states Loading; list; upload) is built in RWB-E1-026. This story adds the DocumentDetailPan
... truncated (2,880 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 025 Document types and fields agreed v1.md", "pattern": "column|header|CSV|template|document_type|sheet|load"}
```

```text
Found 80 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 025 Document types and fields agreed v1.md:
  Line 28: Classification and extraction cannot be built or measured until the bank fixes which types are read and which fields come out of each (REQ-DCM-004, DL19). Today no signed list exists, so the model would train on a list that may change. This story turns the agreed list into a versioned table that the store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) read, and that changes by a data load without a code release (DT02). The measure it serves is fields extracted without review (FSD P5 A2.3.1).

  Line 33: - The load file "DOCTYPE-2026.11" is prepared by the reference data administrator with the six types, 26 fields and the sign-offs of a legal counsel user and a Head of NPA user.

  Line 34: - LOV-RETENTION holds the codes LEGAL10Y and GENERAL05Y, assumed until the bank retention schedule arrives (DL26), loaded by the data steward.

  Line 35: - The loader holds RW-REFADM (Reference data C). The approver holds Reference data A (see section 10).

  Line 36: - The P4 endpoint POST /admin/reference-loads exists and calls the P5 ReferenceTableLoader for table code DOCUMENT_TYPE.

  Line 42: 2. Reference data administrator: uploads the file with POST /admin/reference-loads, table DOCUMENT_TYPE, validFrom 2026-11-30.

  Line 43: 3. P4 reference load service: passes the rows to DocumentTypeLoader through the ReferenceTableLoader interface.

  Line 45: 5. DocumentTypeLoader: on any failure refuses the load whole and returns the row errors; the version in force is unchanged.

  Line 47: 7. Approver: approves with POST /api/recovery/v1/admin/reference-loads/{loadId}/approve; a different person from the loader.

  Line 56: | X3 | The same table version is loaded a second time | Refused with 409; the first load is kept | MSG-P3-027 | AC5 |

  Line 58: | X5 | The loader tries to approve their own load | Refused with 409 | MSG-P7-002 | AC7 |

  Line 59: | X6 | A role without Reference data C uploads the file | Refused with 403 | MSG-P4-002 | TC-E1-025-08 (Access) |

  Line 65: | Independent | Needs only the tracker list (RWB-E1-012) and the P4 reference load endpoint |

  Line 68: | Estimable | One table, one loader, one validation set |

  Line 83:     Given the six types and their 26 fields in load file "DOCTYPE-2026.11"

  Line 86:   
... truncated (9,201 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good. E1-024 does not route document_hub_parameter through the load endpoint at all; it says loaded by the reference data administrator but the table only. The yaml claims DOCUMENT_HUB_PARAMETER (RWB-E1-024), but no story attributes the code to it, and the code is not in LOV-REF-TABLE. That's a gap to call out.

Now I need to verify:
1. Whether `table` is single code: yes per E1-043 §12 ("table (a LOV-REF-TABLE code)"), E1-045 etc. Confirm no "tables" array. Yes.
2. validFrom: yes, in yaml as `validFrom` string (no format: date in ReferenceLoad request! it's `type: string` without format). Note this.
3. dryRun: Is there any? Search for dryRun in yaml and stories.
4. Idempotency-Key header: TSD P4 says Idempotency-Key header; E1-043 says idempotency is table+validFrom+hash (no header). Story E1-019/037/038 use header. Need to report both: contract-level idempotency = natural key; transport header documented in TSD P4 and later stories; API spec does not define a header parameter for this endpoint. Let me grep "Idempotency-Key" in yaml.

5. Response 200 on repeat: E1-043 AC7 says response returns version 5; status 201 in schema. Conflict: AC7 doesn't specify status; yaml only 201. TSD says 201. Some stories say 409 on repeat (E1-001 MSG-P1-011, E1-025, E1-042? no). Need to lay out the contradiction precisely.

6. 409 body: Problem schema with messageCode; E409 description.

7. 422 body: Problem.

8. Authorization: Reference data C; approve A; rollback U; verify U.

Let me grep for "dryRun" and "Idempotency-Key" in the yaml and for "header" spec.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml", "pattern": "dryRun|dry_run|Idempotency|idempotency|header"}
```

```text
Found 4 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml:
  Line 104:       description: Add query parameter route (LOV-ROUTE) and sort value serviceLevelDueAt; size 1 to 200; response header X-Data-As-Of. Case items

  Line 302:       description: Declare the Idempotency-Key header (uuid, required). TransferRequest adds transferReasonCode (string, LOV-TRANSFER-REASON,

  Line 6846:         idempotencyKey:

  Line 7909:         idempotencyKey:

```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "dryRun|dry run|dry-run", "limit": 40}
```

```text
Found 40 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 1693: **In the story.** RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.

  Line 1695: RuleVersionService decides the outcome with no person involved. If any check from steps 3 to 5 failed, refuse the load whole and name every failing row and test case in the Problem detail with MSG-P3-027; the version takes status REFUSED and the version in force keeps working. If everything passed, write the rows to rule_row with rule_table, row_order and target_queue_code, and write the rule_version header with status LOADED, in one transaction, which is a single unit of database work that either completes in full or leaves both tables untouched. That header is the change log: version label, author, load time, check result and dry run counts. Only P4 code writes rule_row.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md:
  Line 9459: As a **center of excellence analyst (RW-COE)**, I want **an Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases and a dry run), a load with a version, approval, rollback by one call and a change log**, so that **a rule change goes from template to production without a code release**.

  Line 9470: - Live cases exist for the dry run (RWB-E1-018).

  Line 9479: 6. RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.

  Line 9507: | Estimable | One validator, one test runner, one dry run, three endpoints |

  Line 9524:     Then the change log records author U-41, approver U-51, the load and approval times, "50 of 50 test cases passed" and the dry run count

  Line 9687:     DryRunReport dryRun(String ruleTable, List<RuleRowDraft> rows, LocalDate onDate);

  Line 9697: **Package.** Validation, test runner and dry run in `recovery/casewf/rules` (Java package `recovery.casewf.rules`). Endpoints and rule_row writes in the P4 package `recovery/accessadmin/ruleversions` (Java 
... truncated (13,207 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

No dryRun field on reference-loads. dryRun_counts is a column populated by rule loads (E1-029), not a request field. Good — answer: no dryRun.

Idempotency-Key: yaml only declares it at line 302 for another endpoint (transfer). So the API spec for reference-loads does not declare an Idempotency-Key header parameter. TSD P4 and later stories cite it. The natural idempotency key is table+validFrom+hash. Report.

Let me read yaml line 280-320 to see the global rules about idempotency and headers, and the overview's rule about POST idempotency. Also check the HTML description maybe clarifies. Let me grep the html for "Idempotency".

Also check the API spec's "Rules every endpoint follows" line about POST requests (truncated in grep). Read html line 42 segment around Idempotency.

Let me also verify status codes for repeat load: E1-043 AC7 (returns the version 5, presumably 201/200 unclear), E1-001 says 409 with MSG-P1-011. Two contradictory behaviours; E1-042 says repeat returns existing load. E1-043 is the owning story. Need to state both and identify which is contract.

Also 409 in E1-043 for "an approved version of the table already has this valid from" and 422 for checks.

Now status values: E1-043 says VALIDATED; P5/E1-025 says LOADED; E1-037 says Loaded; physical schema default VALIDATED; LOV-VERSION-STATUS has VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED (no LOADED!). That's a notable inconsistency. Should report.

Now let me check line 42 HTML for idempotency rule text.

</details>

**Tool `shell`** - completed

```json
{"command": "$p='C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.html'; $t=Get-Content -Raw $p; $i=$t.IndexOf('Idempotency'); $t.Substring($i-400,1200)"}
```

```text
dpoints check the approval level, the delegation of authority limit and maker and checker</td></tr><tr><td class="">Decision log</td><td class="">Every state change writes its decision log entry first; a failed write returns 503 and nothing changes</td></tr><tr><td class="">Concurrency</td><td class="">Records carry a version; a stale version returns 409 with MSG-GEN-004</td></tr><tr><td class="">Idempotency</td><td class="">POST requests carry an Idempotency-Key header; a repeat returns the first result</td></tr><tr><td class="">Paging</td><td class="">page and size query parameters; size up to 100</td></tr><tr><td class="">Dates</td><td class="">ISO 8601; dates in the Asia/Bangkok business day</td></tr><tr><td class="">Personal data</td><td class="">Fields marked x-personal-data are masked unless the role may see them</td></tr><tr><td class="">Errors</td><td class="">application/problem+json with the message code and the Thai and English text from the error and message standard</td></tr></tbody></table></div></section><section class="tab" id="ep"><div class="filter"><input type="search" placeholder="Search endpoints" data-filter="t_ep" aria-label="Search endpoints"><select data-f

```

**Tool `read`** - completed

```json
{"limit": 45, "offset": 285, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 285-329
285:       x-capability:
286:         area: Queue and allocation
287:         right: U
288:       x-first-release: E2
289:       requestBody:
290:         required: true
291:         content:
292:           application/json:
293:             schema:
294:               $ref: '#/components/schemas/TransferRequest'
295:       parameters:
296:       - name: caseId
297:         in: path
298:         required: true
299:         schema:
300:           type: string
301:           format: uuid
302:       description: Declare the Idempotency-Key header (uuid, required). TransferRequest adds transferReasonCode (string, LOV-TRANSFER-REASON,
303:         required). A transfer rule refusal returns 409 with MSG-P3-033; a bulk transfer with refusals returns MSG-P3-035.
304:       responses:
305:         '200':
306:           description: Success
307:           content:
308:             application/json:
309:               schema:
310:                 $ref: '#/components/schemas/Assignment'
311:         '401':
312:           $ref: '#/components/responses/E401'
313:         '403':
314:           $ref: '#/components/responses/E403'
315:         '404':
316:           $ref: '#/components/responses/E404'
317:         '409':
318:           $ref: '#/components/responses/E409'
319:         '422':
320:           $ref: '#/components/responses/E422'
321:         '503':
322:           $ref: '#/components/responses/E503'
323:   /cases/{caseId}/deviations:
324:     post:
325:       tags:
326:       - Cases
327:       summary: Raise a deviation X1 to X7 on the case
328:       operationId: postCasesCaseidDeviations
329:       x-module: S8
[Output truncated. Continue reading with offset: 330]
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Global rule: "POST requests carry an Idempotency-Key header; a repeat returns the first result" (HTML overview). So a header is stated globally, even though the yaml endpoint doesn't declare the parameter. Good.

Now I need to check the "adding a new table code vs adding a value row" rule. E1-043 BR1: list is data and changes by a load of LOV-REF-TABLE. Guardrail: no business value in code. And the build notes §3.1: adding a code to LOV-REF-TABLE does not by itself make it loadable; needs registered handler. E1-043 INVEST: "The list of table codes is data (LOV-REF-TABLE). The story fixes the versioning behavior, not the tables". Also E1-042 §4 step 1 vs value file: new parameter = PR + release; new value = load + approval. That's the similar rule for parameters.

Also check the reference data design doc for change process — 06 Data\Recovery Workbench Reference Data and Lists of Values v3.xlsx and maybe its md extraction. Let me find an md for that to cite "adding a new table" process. Search "new table" or "change process".

Let me also check the physical schema for lov_value structure and LOV-VERSION-STATUS values, and whether PRODUCT/REGION/... are lov_value lists. Look at LOV-PRODUCT inserts and LOV-REGION, LOV-EXPOSURE-BAND, LOV-ROLE, LOV-TEAM, LOV-SERVICE-LEVEL, LOV-LEGAL-PERIOD? Actually LEGAL_PERIOD and HOLIDAY may not have physical tables. Confirm: no legal_period or holiday table in CREATE TABLE list. So those codes have no target table — they must live in reference_row (E1-043 "most E1-043 reference tables → reference_version + reference_row"). Good.

Let me confirm which physical tables exist for each of the 25 codes:
- PRODUCT: no `product` table; data_product exists but is a different concept (14 data products). E1-001 maps PRODUCT code -> data_product (build notes table). Hmm build notes says PRODUCT | data_product. But E1-045 says PRODUCT rows read through ReferenceDataService and no new table. Conflict again! E1-001's data_product catalog is the "14 data products" catalog and the load table code is `data_product` (lowercase) in E1-001; the build notes map `PRODUCT` to `data_product`, which looks like a conflation. Need to be careful and report the ambiguity.

Let me read E1-001 contract + data to see table code and target.

Also check LOV-PRODUCT values (MORTGAGE etc.) — PRODUCT reference table rows probably product groups, held in reference_row.

Let's read E1-001 relevant lines.

</details>

**Tool `read`** - completed

```json
{"limit": 50, "offset": 240, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 001 Recovery tables for the 14 data products v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 001 Recovery tables for the 14 data products v1.md, lines 240-289
240: | DF-REF-075 | data_product | owner_role | Create and write |
241: | DF-REF-076 | data_product | owner_user_id | Create and write |
242: | DF-REF-077 | data_product | refresh_cycle | Create and write |
243: | DF-REF-078 | data_product | expected_by | Create and write |
244: | DF-REF-079 | data_product | valid_from | Create and write |
245: 
246: Field IDs are those in the Logical Data Model and Data Dictionary.
247: 
248: Ruled 2026-11-06 as D-RCV-29: the baseline migration seeds the full recovery dictionary with 108 `sys_objects` rows and 1,256 `sys_fields` rows as held in Recovery Workbench Physical Schema v4.sql, so the dictionary is complete before the tables exist and the conformance test can run; RWB-E1-016 and RWB-E1-064 read the full dictionary and later dictionary changes are reference loads through RWB-E1-043 (D-RCV-28).
249: 
250: ## 12. Contract
251: 
252: **Dictionary view** `v_data_dictionary` (read model created by the migration; RWB-E1-064 builds the dictionary endpoint on it)
253: 
254: | Column | From |
255: |---|---|
256: | field_id, entity, field, data_type, physical_type, mandatory, lov_code, source_system, source_field, personal | sys_fields |
257: | data_product, entity_system_of_record | sys_objects |
258: | product_system_of_record, refresh_cycle, owner_role, owner_user_id | data_product |
259: 
260: **Reference load handler** (published interface of P4 that P1 implements, from RWB-E1-043)
261: 
262: ```java
263: public interface ReferenceTableHandler {
264:     String tableCode();                                              // returns "data_product"
265:     ValidationReport validate(ReferenceLoadFile file);               // checks every row, writes nothing
266:     int apply(UUID loadId, ReferenceLoadFile file, LocalDate validFrom); // writes all rows in one transaction, returns the row count
267: }
268: ```
269: 
270: The load itself is `POST /admin/reference-loads` (P4, Reference data C) with `table = data_product`, and its response is `ReferenceLoad`. A refused load returns 422 with MSG-P1-003, MSG-P1-004 or MSG-P1-007 in the Problem response; a caller without Reference data C gets 403 with MSG-P4-002. Idempotency: a file whose content hash matches the version in force is reported with MSG-P1-011 and writ
... truncated (3,534 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql", "pattern": "'LOV-PRODUCT'|'LOV-REGION'|'LOV-TEAM'|'LOV-SERVICE-LEVEL'|'LOV-EXPOSURE|'LOV-ROLE'", "limit": 40}
```

```text
Found 40 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 4293: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-003', 'recovery_case', 'product_group', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT', NULL, 'Core bank (ALS) via COLLINS', 'Product_Category_Host', false, 'Mortgage, hire purchase, SSME or unsecured');

  Line 4301: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-011', 'recovery_case', 'team_code', 'LOV', 'varchar(20)', false, 'LOV-TEAM', NULL, 'Workbench', NULL, false, 'The owning team, used by scope rules');

  Line 4302: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-012', 'recovery_case', 'region_code', 'LOV', 'varchar(10)', false, 'LOV-REGION', NULL, 'Workbench', NULL, false, 'The owning region, used by scope rules');

  Line 4305: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-015', 'recovery_case', 'exposure_band', 'LOV', 'varchar(10)', false, 'LOV-EXPOSURE', NULL, 'Workbench', NULL, false, 'Exposure band set from the outstanding balance at entry');

  Line 4318: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-050', 'recovery_case', 'next_action_owner_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Owner role of the next action, from owner_role of the rule');

  Line 4349: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-004', 'queue', 'team_code', 'LOV', 'varchar(20)', true, 'LOV-TEAM', NULL, 'Workbench', NULL, false, 'Team the queue belongs to');

  Line 4350: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physica
... truncated (14,318 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

The LOV-REF-TABLE codes PRODUCT/REGION/TEAM etc. overlap LOV list codes (LOV-PRODUCT etc.) but PRODUCT as a table code is different. Hmm.

Now, which handler owns each code. There's no single registry listing handlers per code. Let me search for "ReferenceTableHandler" and "ReferenceTableLoader" across stories to compile.

Also check whether there's a P4 TSD component list for reference load (handlers), and the E1-043 TSD. Let me search "ReferenceTableHandler" globally.

</details>

**Tool `grep`** - completed

```json
{"limit": 80, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "ReferenceTableHandler|ReferenceTableLoader|ReferenceLoadHandler"}
```

```text
Found 80 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 2 v2.md:
  Line 1455: A person does this: the reference data administrator, holding Reference data right C. They post the file to /api/recovery/v1/admin/reference-loads as multipart form data with the file, the table name payment_match_rule and a valid from date. P4 owns the endpoint. Your work is PaymentMatchRuleLoadHandler, a ReferenceLoadHandler for that table, with its validate and apply methods. A version is a set of rows sharing a rule_version such as PM-2026.12, each row holding a rule code, a priority, a match type, an amount tolerance, window days before and after, and a partial floor. The endpoint takes the SHA-256 hash of the file per table, so a file already loaded is refused with 409 and MSG-P1-002.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 47: Build the load path for this table code. The reference data administrator sends the catalog file to POST /api/recovery/v1/admin/reference-loads with the table code data_product. Implement that endpoint if RWB-E1-043 has not already delivered it, and implement DataProductCatalogHandler as the ReferenceTableHandler registered for that code, which is how a load finds the class that handles it. The file holds the 14 products with the owner user ID for that environment, so DEV and SIT are given different files.

  Line 285: The checks run on their own inside code you write. TrackerInventoryHandler implements the ReferenceTableHandler interface whose signature comes from RWB-E1-001, and its validate method reads every row of the file before anything is written. Check the required fields, the list values for location_type, update_cycle and decision, a tracker code that appears once per inventory version, a target_product naming a row in data_product for each LOAD decision, and team_code membership of LOV-TEAM through the P4 published interface. Last, count the rows per team against the parameter tracker.inventory.teams, which holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. Unit test each check with a failing row.

  Line 1449: **In the story.** P4 reference load service: passes the rows to DocumentTypeLoader through the ReferenceTableLoader interface.

  Line 1451: This handover happens automatically inside the service. P4 owns the endpoint and P5 owns the document types, so P5
... truncated (28,209 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

I have enough on handlers. Now I should check the E1-043 TSD? Actually there's no P3-specific reference. Let me check P3 TSD for the reference load service section (grep "reference_version" gave lines but maybe a section "Reference data"). Let me grep "refdata" in P3 TSD.

Also I must check "13 codes" vs 25 and whether there's a doc that enumerates 13. E1-043 BR1 lists 13. Physical schema lists 25. TSD P3 lists 25. Build notes say E1-043 serves 13; P5 adds 4; later stories add more. So full registry = 25 in schema (but DOCUMENT_HUB_PARAMETER absent from both). I should compute exactly 25 and list them.

Now I should verify the mapping of each code to handler/table. Let me compile from evidence:

1. PRODUCT — E1-045: rows read through ReferenceDataService, no new table → reference_version/reference_row. But build notes table says data_product. Conflict. Which is right? E1-045 says "No new table. Reads reference_version and reference_row (RWB-E1-043) through the published service". It covers PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL. So for PRODUCT, the authoritative owning story E1-045 says reference_row. E1-001's `data_product` is a separate code (lowercase) for the 14 data products and writes data_product. The build note conflating PRODUCT->data_product is likely an error. I'll flag.

2. REGION — no other story? grep REGION reference table. Likely reference_row (E1-043 generic).
3. EXPOSURE_BAND — E1-043 generic → reference_row.
4. ROLE — E1-019 reads TEAM, ROLE via ReferenceDataService → reference_row.
5. TEAM — same → reference_row.
6. QUEUE — reference_row + QueueVersionApplier → queue.
7. QUEUE_MEMBER — reference_row + applier → queue_member.
8. SERVICE_LEVEL — E1-045 → reference_row (no dedicated table).
9. DOCUMENT_TYPE — P5 DocumentTypeLoader → document_type.
10. DOCUMENT_CHECKLIST — ChecklistLoader → document_checklist_item.
11. RETENTION_CLASS — RetentionClassLoader → retention_class.
12. TEMPLATE — TemplateLoadHandler → template.
13. DELEGATION_LIMIT — E1-038 → delegation_limit.
14. PERMISSION — E1-037 → permission.
15. MASKING_RULE — E1-037 → masking_rule.
16. PARTNER_USER — Epic 2 → partner_user.
17. LEGAL_PERIOD — reference_row.
18. HOLIDAY — reference_row (E1-045 reads HOLIDAY rows in force through ReferenceDataService).
19. PRODUCT_PARAMETER — reference_row.
20. PARAMETER — parameter_value.
21-25. ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER — rule tables? They are also LOV-RULE-TABLE. Rule loads go to POST /admin/rule-versions (API-P

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql", "pattern": "refdata\\.|refload\\.|refdata_table|ref-table"}
```

```text
No matches found
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "refdata\\.table|ReferenceTableSchemas|refdata\\.load", "limit": 40}
```

```text
Found 17 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 2425: The service runs every check before it writes anything. The table code must be in LOV-REF-TABLE, read through the P4 list interface. The rows are checked against ReferenceTableSchemas, which holds the column names, types and key columns per table and comes from the parameter catalog of RWB-E1-042, so the text five in the numeric column limit_days fails with MSG-P3-027 naming row 12 and that column (AC4). Row keys must be unique. The valid from date must not be before the business date (AC6). A file with no data rows fails with MSG-GEN-001. The service also computes the content hash, a SHA-256 over the rows sorted by key, and the next version number, one above the highest version of that table.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md:
  Line 13879: | ReferenceTableSchemas | Rule table | Column names, types and key columns per table code, read from the parameter catalog (RWB-E1-042) |

  Line 13897: 2. Build `ReferenceTableSchemas` from the parameter catalog and the row check (type, required, key uniqueness) with a check result per row and column.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 904: "3": "The service runs every check before it writes anything. The table code must be in LOV-REF-TABLE, read through the P4 list interface. The rows are checked against ReferenceTableSchemas, which holds the column names, types and key columns per table and comes from the parameter catalog of RWB-E1-042, so the text five in the numeric column limit_days fails with MSG-P3-027 naming row 12 and that column (AC4). Row keys must be unique. The valid from date must not be before the business date (AC6). A file with no data rows fails with MSG-GEN-001. The service also computes the content hash, a SHA-256 over the rows sorted by key, and the next version number, one above the highest version of that table.",


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 043 Reference data service with versioned tables v1.md:
  Line 273: | ReferenceTableSchemas | Rule table | Column names, types and key columns per table code, read from the parameter 
... truncated (6,556 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good. Now check the rule tables (ENTRY etc.) and rule_row columns for the answer on those 5 codes.

Also check whether there is a "table registry" table besides lov_value. The reference data design doc (v3 xlsx) might list reference tables and change process. Let me find an md/csv version: 13 AI-First SDLC repository/requirement/legacy/06-data/_csv/recovery-workbench-reference-data-and-lists-of-values-v3/reference-tables.csv and change-process.csv. These are CSV exports of the xlsx; they may enumerate reference tables incl. physical table and owner. That's useful for question 5. Let me read them.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\requirement\\legacy\\06-data\\_csv\\recovery-workbench-reference-data-and-lists-of-values-v3\\reference-tables.csv"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-reference-data-and-lists-of-values-v3\reference-tables.csv, lines 1-17
1: Other reference data
2: "Reference data held as versioned rows, its owner and where it is specified."
3: Reference data,Table,What it holds,Owner,Specified in
4: Routing rules,rule_row,448 rules in ten route sets,Center of excellence; Risk signs where a limit moves,Business Rules and Routing Logic
5: Allocation table,rule_row,"Product group, region and exposure band to queue",Shared operations,DL23
6: Delegation of authority,delegation_limit,"Limits by decision, level, product and amount",Risk with the product heads,Delegation of Authority Matrix; DL18
7: Roles,role,54 roles,Application owner,"Users, Roles and Permissions"
8: Permission matrix,permission,Roles against 14 capability areas,Application owner; security administrator loads,"Users, Roles and Permissions"
9: Queues,queue,"Queues by team and role, with method, cap and overflow",Shared operations,DL23
10: Service levels and timers,Reference table,"Time allowed per state, warning and escalation",Business lead,DL22
11: Letter and notice templates,template,"Templates by type, product and language",Legal counsel,DL28
12: Messages,Reference table,Screen and letter messages in English and Thai,Product owner; Legal and Compliance for customer wording,Error and Message Standard; DL10
13: Document types,Reference table,Types and the fields extracted from each,Business lead with Legal,DL19
14: Retention classes,Reference table,Retention period by data product and document type,Compliance,DL26
15: Masking rules,Reference table,Which role sees which personal field unmasked,Compliance,DL26
16: Partner panel,partner,"Partners, contracts and panel status",Partner and agency manager,None
17: Feature flags,Configuration,Flag values per environment,Tech leads,Engineering Practices
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\requirement\\legacy\\06-data\\_csv\\recovery-workbench-reference-data-and-lists-of-values-v3\\change-process.csv"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-reference-data-and-lists-of-values-v3\change-process.csv, lines 1-10
1: How reference data changes
2: Every change is a validated data load with a version. None needs a code release.
3: Step,Stage,What happens
4: 1,Request,The owner of the list or table raises the change with the reason and the date it should take effect
5: 2,Prepare,"The reference data administrator prepares the new version as a load file, with a test case for each changed row"
6: 3,Validate,The load runs against the schema and the completeness checks in SIT. A load with an exception is refused whole
7: 4,Approve,The owner approves. Risk also approves where a limit or a threshold moves
8: 5,Load,The new version loads into production with its valid from date. No code release
9: 6,In force,New decisions use the new version from its date. Open cases keep the version they were decided under
10: 7,Roll back,A breach returns the previous version through the same load
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

The reference-tables.csv is vague ("Reference table").

Now check rule tables in E1-029 contract to confirm ENTRY etc. are loaded through /admin/rule-versions not reference-loads.

Also need to verify a key statement: is `table` guaranteed single-valued and case-sensitive? LOV values uppercase, but stories use lowercase ("permission", "delegation_limit", "template", "merge_field", "payment_match_rule", "data_product", "tracker_inventory", "sys_fields"). So mismatch: LOV codes uppercase, stories cite lowercase. Need to state: code matching must be case-insensitive or the handler registers the lowercase name; contract says LOV-REF-TABLE code, so uppercase canonical. That's an important clarification.

Let me check if anywhere states case-insensitive. grep "case-insensitive" or "uppercase".

</details>

**Tool `grep`** - completed

```json
{"limit": 40, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "case-insensitive|upper ?case|lowercase|table code is"}
```

```text
Found 37 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 1445: A person uploads the file, the reference data administrator, who holds the Reference data C right. The request is multipart form data on the existing P4 endpoint POST /admin/reference-loads: the file itself in the Excel template, table set to DOCUMENT_TYPE and validFrom set to 30 November 2026. The response is a ReferenceLoad holding the load ID, the table, the valid from date, the status and the row count. Your work here is to add DOCUMENT_TYPE to the table codes the endpoint accepts and to parse the template columns into rows. A caller without Reference data C is refused with 403 and MSG-P4-002, and with the feature flag rwb.dochub.doctypes off the table code is refused.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Process Map v1.html:
  Line 64:   td::before{content:attr(data-l);display:block;font-size:11px;font-weight:700;color:var(--soft);text-transform:uppercase;letter-spacing:.03em}


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\package-lock.json:
  Line 9053:         "lowercase-keys": "^3.0.0",

  Line 10446:     "node_modules/lowercase-keys": {

  Line 10448:       "resolved": "https://registry.npmjs.org/lowercase-keys/-/lowercase-keys-3.0.0.tgz",

  Line 13782:     "node_modules/postcss-attribute-case-insensitive": {

  Line 13784:       "resolved": "https://registry.npmjs.org/postcss-attribute-case-insensitive/-/postcss-attribute-case-insensitive-7.0.1.tgz",

  Line 13807:     "node_modules/postcss-attribute-case-insensitive/node_modules/postcss-selector-parser": {

  Line 14976:         "postcss-attribute-case-insensitive": "^7.0.1",

  Line 16152:         "lowercase-keys": "^3.0.0"


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 42: .side .grp{padding:10px 14px 4px;font-size:11px;font-weight:700;color:var(--soft);text-transform:uppercase;letter-spacing:.04em}

  Line 108: .note summary{cursor:pointer;font-size:12px;font-weight:700;color:var(--accent);letter-spacing:.02em;text-transform:uppercase}

  Line 119: .step .lab{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;padding-top:1px}

  Line 133: .def .dk{font-size:11.5px;color:var(--soft);font-w
... truncated (7,933 chars total)
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 029 Rule load validation and rollback v1.md", "pattern": "rule-versions|rule_table|ENTRY|routeSet|RuleVersion"}
```

```text
Found 24 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 029 Rule load validation and rollback v1.md:
  Line 32: - The five rule tables are agreed for Epic 1: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (DL24, option A).

  Line 40: 2. RW-COE: calls POST /admin/rule-versions with the file, route set UNIVERSAL_RULES and valid from.

  Line 44: 6. RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.

  Line 45: 7. RW-RISK: approves through POST /admin/rule-versions/{versionId}/approve; refused if the approver is the author.

  Line 46: 8. RuleVersionService: on the valid from date the version is in force; new decisions use it and open cases keep the version they were decided under (R-UNI-38).

  Line 47: 9. RW-COE: if the version is wrong, calls POST /admin/rule-versions/{versionId}/rollback; the previous version is in force again in one transaction and the change log records the rollback.

  Line 193: | DF-REF-052 | rule_row | rule_table | Write |

  Line 209: **POST /api/recovery/v1/admin/rule-versions** (P4 endpoint)

  Line 213: | Request | multipart/form-data: file (xlsx), routeSet = "UNIVERSAL_RULES", validFrom (date). The rule table and version label are columns in the file |

  Line 214: | Response | 201 RuleVersion[] for the stored rows (ruleId, ruleVersion, routeSet, fromState, eventCode, conditionExpr, actionText, toState, ownerRole, timerSpec, validFrom, validTo, approvedBy, testCaseId) |

  Line 219: **POST /api/recovery/v1/admin/rule-versions/{versionId}/approve**

  Line 223: | Response | 200 RuleVersion |

  Line 227: **GET /api/recovery/v1/admin/rule-versions**

  Line 231: | Request | Query routeSet, status |

  Line 232: | Response | RuleVersion[] |

  Line 236: **POST /admin/rule-versions/{versionId}/rollback** (new endpoint, see additions)

  Line 241: | Response | 200 RuleVersion of the version now in force |

  Line 272: | RuleVersionController | Controller | P4: list, load, approve, rollback endpoints |

  Line 273: | RuleVersionService | Service | P4: stores rows, approval check, effective date, rollback in one transaction, change log |

  Line 279: - Writes rule_row (all columns plus rule_table, row_order, target_queue_code) and rule_version,
... truncated (3,442 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Confirmed rule tables use /admin/rule-versions, not reference-loads.

Now I need line numbers for key facts in the P4 TSD, P3 TSD, physical schema. Have them.

Also check the API spec's description "Add multipart fields changeRequestRef..." which means the E1-048 change-checklist story adds those optional fields. The yaml description is stale/forward-looking (a v2 spec written to include later deltas). This is important: the yaml says "Add multipart fields..." — imperative note, not current schema. But the ReferenceLoad schema in yaml lacks changeRequestRef etc. Contradiction within spec: description says ReferenceLoad adds them, but schema doesn't. Report.

Let me check E1-048 for the change checklist fields to confirm optional/required and status codes (409 MSG-P3-022).

Also check whether there is a "dryRun" query on reference-loads anywhere. None.

Now check the "GET /admin/lists/{listCode}" schema ListOfValues — code + values object. Fine.

Let me read E1-048 contract quickly.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 048 Rule change audit report v1.md", "pattern": "changeRequestRef|impactSummary|rollbackPlan|multipart|MSG-P3-022|ReferenceLoad"}
```

```text
Found 11 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 048 Rule change audit report v1.md:
  Line 53: | X2 | Approval with a checklist item missing | Refused; the version stays VALIDATED | MSG-P3-022 | AC3 |

  Line 54: | X3 | Approval of a version whose test result is FAILED | Refused | MSG-P3-022 | AC4 |

  Line 99:     Then the system refuses the approval with MSG-P3-022 naming "rollback plan"

  Line 105:     Then the system refuses the approval with MSG-P3-022 naming "test result"

  Line 181: **POST /admin/reference-loads** and **POST /admin/rule-versions** (P4 endpoints) take three more form fields: `changeRequestRef` (max 30), `impactSummary` (max 1000), `rollbackPlan` (max 1000). Missing fields do not refuse the load; they refuse the approval (BR1).

  Line 183: **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint): 409 with MSG-P3-022 naming the missing item when BR1 fails; otherwise as RWB-E1-043.

  Line 190: | Response | 200 `ReferenceLoad` with `verifiedBy`, `verifiedAt` |

  Line 200: | Response | 200 `ChangeLogPage`: `items[]` of `ChangeLogEntry` (`table`, `version`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `testResult`, `authorUserId`, `loadedAt`, `approverUserId`, `approvedAt`, `verifiedBy`, `verifiedAt`, `rollbackPlan`, `rowsAdded`, `rowsChanged`, `rowsRemoved`, `rulesChanged[]`), `page`, `size`, `total`; or `text/csv` with the same columns |

  Line 236: 3. Build `ChangeChecklistValidator` and call it from `approve(...)`; return MSG-P3-022 naming the first missing item.

  Line 250: | MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |

  Line 256: MSG-P3-022 is new (see Additions). Thai text follows DL10.

```

**Tool `read`** - completed

```json
{"limit": 30, "offset": 15230, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 v7.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md, lines 15230-15259
15230: | DF-REF-168 | reference_version | approved_at | Read |
15231: | DF-REF-183 | reference_row | row_key | Read |
15232: | DF-REF-184 | reference_row | row_data | Read |
15233: 
15234: Field IDs are those in the Logical Data Model and Data Dictionary.
15235: 
15236: ### 12. Contract
15237: 
15238: **POST /admin/reference-loads** and **POST /admin/rule-versions** (P4 endpoints) take three more form fields: `changeRequestRef` (max 30), `impactSummary` (max 1000), `rollbackPlan` (max 1000). Missing fields do not refuse the load; they refuse the approval (BR1).
15239: 
15240: **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint): 409 with MSG-P3-022 naming the missing item when BR1 fails; otherwise as RWB-E1-043.
15241: 
15242: **POST /admin/reference-loads/{loadId}/verify** (new, P3)
15243: 
15244: | Item | Value |
15245: |---|---|
15246: | Request | `VerifyRequest`: `note` (max 1000, required) |
15247: | Response | 200 `ReferenceLoad` with `verifiedBy`, `verifiedAt` |
15248: | Errors | 401; 403 no Reference data U (MSG-P4-002); 404 unknown load (MSG-P4-003); 422 empty note (MSG-GEN-001) or before valid from (MSG-GEN-003); 503 |
15249: | Authorization | Reference data, right U |
15250: | Idempotency | A second verification of the same version returns 200 with the first record and changes nothing |
15251: 
15252: **GET /admin/change-log** (new, P3)
15253: 
15254: | Item | Value |
15255: |---|---|
15256: | Request | Query: `from` (date, required), `to` (date, required), `table` (optional), `format` (`json` default or `csv`), `page`, `size` (default 50, max 200) |
15257: | Response | 200 `ChangeLogPage`: `items[]` of `ChangeLogEntry` (`table`, `version`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `testResult`, `authorUserId`, `loadedAt`, `approverUserId`, `approvedAt`, `verifiedBy`, `verifiedAt`, `rollbackPlan`, `rowsAdded`, `rowsChanged`, `rowsRemoved`, `rulesChanged[]`), `page`, `size`, `total`; or `text/csv` with the same columns |
15258: | Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 422 `to` before `from` (MSG-GEN-003); 503 |
15259: | Authorization | Rules and parameters, right R |
[Output truncated. Continue reading with offset: 15260]
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now I have the change checklist fields (E1-048). Note yaml description says those are to be added; the ReferenceLoad schema in yaml doesn't include them.

Now check the file size / row limits for reference loads generally (413 MSG-P5-001, 415). Any stated max rows or size? Search "max file" "size limit" "413" in relation to reference loads. E1-043 doesn't mention. P4 TSD errors don't include 413. The yaml doesn't include 413 on this endpoint. So: no stated max rows/size for reference-loads; the global P5 document upload has limits (25 MB), irrelevant.

Search "25 MB" or "maxrows" - probably doc upload only. I'll say NOT STATED, except no 413 on the endpoint.

Now confirm character encoding and separators for PARAMETER CSV: not stated. The build notes show a plain CSV with comma separators, header row; no encoding stated (no BOM). Need to say NOT STATED for encoding/separator, with example implying comma and UTF-8 not stated.

Max rows/size: not stated.

What happens to product_group etc. — from build notes table lines 70-80:
- product_group → NULL
- version_no → next for key+environment
- valid_from → request validFrom
- status → VALIDATED on load, APPROVED after approve
- author_user_id → signed-in loader
- approver_user_id/approved_at → only approve, approver ≠ author

Good.

Now question 5 requires "For each code, which handler/loader owns it and which physical table(s) it writes" and "does the caller choose a database table, a table code, a type, or a column? Is any user-supplied column mapping allowed?" I have the answer.

I should verify which handler owns codes with no specific story: PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, SERVICE_LEVEL, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER. E1-043's generic registry handles them via ReferenceVersionRegistry (no named handler class). E1-045 adds ProductCompletenessCheck to the registry for PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL. No dedicated handler class names. State: generic E1-043 registry (ReferenceVersionRegistryImpl + ReferenceTableSchemas); E1-045 only adds a check.

Need to verify ROLE/TEAM target: E1-019 line 285 says TEAM, ROLE, QUEUE, QUEUE_MEMBER through ReferenceDataService. The physical `role` table exists and is presumably populated from the reference version? Does anything apply ROLE/TEAM to physical tables? No applier mentioned for role/team. Only queue/queue_member. So ROLE/TEAM rows stay in reference_row; the `role` table may be the session/matrix table (E1-037 writes permission and ro

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml", "pattern": "/admin/lists|listCode|ListOfValues"}
```

```text
Found 6 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml:
  Line 2923:   /admin/lists/{listCode}:

  Line 2935:       - name: listCode

  Line 2946:                 $ref: '#/components/schemas/ListOfValues'

  Line 8805:     ListOfValues:

  Line 9485:         listCode:

  Line 9515:         listCode:

```

**Tool `grep`** - completed

```json
{"limit": 30, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "lov_value.*load|load.*lov_value|load a list|lists/\\{listCode\\}.*POST"}
```

```text
Found 30 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.html:
  Line 42: </style></head><body><header><div class="in"><div class="lab">SCB COLLECTIONS AND RECOVERY</div><h1>Recovery Workbench API specification</h1><div class="meta">Henka Group, 28 October 2026. (C) Siam Commercial Bank and Henka Pte Ltd</div></div></header><nav><div class="in"><button data-t="ov" aria-selected="false">Overview</button><button data-t="ep" aria-selected="false">Endpoints</button><button data-t="sc" aria-selected="false">Schemas</button><button data-t="er" aria-selected="false">Errors</button><button data-t="rl" aria-selected="false">By release</button></div></nav><main><section class="tab" id="ov"><div class="grid"><div class="box"><b>144 endpoints</b>In 15 groups, under /api/recovery/v1 in the ACE service</div><div class="box"><b>178 schemas</b>Records from the logical data model, requests, pages and the problem response</div><div class="box"><b>One access check</b>Role, capability area, right and scope on every endpoint</div><div class="box"><b>OpenAPI 3.1</b>The YAML file is the contract; types are generated from it</div></div><h2>Rules every endpoint follows</h2><div class="tw"><table style="min-width:760px"><thead><tr><th>Rule</th><th>Detail</th></tr></thead><tbody><tr><td class="">Sign-in</td><td class="">Bearer token from Entra ID through the ACE front end; partners through the external gateway (DL03)</td></tr><tr><td class="">Access</td><td class="">The endpoint declares its capability area and right; scope filters every query; out of scope returns 404</td></tr><tr><td class="">Approvals</td><td class="">Approval endpoints check the approval level, the delegation of authority limit and maker and checker</td></tr><tr><td class="">Decision log</td><td class="">Every state change writes its decision log entry first; a failed write returns 503 and nothing changes</td></tr><tr><td class="">Concurrency</td><td class="">Records carry a version; a stale version returns 409 with MSG-GEN-004</td></tr><tr><td class="">Idempotency</td><td class="">POST request...

C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\07 Screens and experience\Recovery Workbench Screen Specifications v1.html:
  Line 42: </style></head><body><header><div class="in"><div class="lab">SCB COLLECTIONS AND RECOVERY</div><h1>Recovery Workbench screen specifications</h1><div class="meta">Henka Group
... truncated (24,327 chars total)
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good. D-RCV-29 says later dictionary changes are reference loads through RWB-E1-043.

Now I want to confirm the reference_row unique constraint discrepancy and status values. Also note `is_active`/`state` etc.

I should check the P4 TSD's data/authority sections for capability area definitions, and possibly a table of rights (C/R/U/D/A). Not necessary.

Let me now check the E1-043 build spec (INC-009) for any clarifications on contract (e.g., status codes, dryRun, idempotency). It may be a tighter source.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\output\\INC-009-epic-1-RWB-E1-043\\specify\\spec.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-009-epic-1-RWB-E1-043\specify\spec.md, lines 1-286
1: # Technical Specification — RWB-E1-043 Reference data service with versioned tables
2: 
3: | Field | Value |
4: |---|---|
5: | Story | RWB-E1-043 — Reference data service with versioned tables |
6: | Epic / module | E1 / P3 Case and workflow |
7: | RUN_ID | `INC-009-epic-1-RWB-E1-043` |
8: | Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-012, FR-RWB-020); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 043 Reference data service with versioned tables v1.md` |
9: | Upstream IDs | BRD-RWB-004, BRD-RWB-020; FR-RWB-012, FR-RWB-020; REQ-DRI-011, REQ-CWC-006; US-RWB-E1-043; CTX-FEATURE-003; CTL-08; R-UNI-38; DF-REF-159..184 |
10: | Status | SUCCESS |
11: | Prepared | 2026-11-04 |
12: | Author | Technical Specifier (agent run) |
13: | Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |
14: 
15: ## Change Scope Declaration
16: 
17: | Field | Value |
18: |---|---|
19: | Change Type | `NEW_STORY` |
20: | UI In Scope | `NO` — no screen. SCR-40 is Epic 8; the administrator loads by file and reads the response. |
21: | Logic In Scope | `YES` — versioning, load checks, approval, effective dating, cache, read logging and no-version handling. |
22: | API In Scope | `YES` — this story first delivers `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve` and `GET /admin/lists/{listCode}` (P4). The contract is already in API Specification v2; no OpenAPI delta. |
23: | API Impact Type | `NEW_API_REQUIRED` |
24: | Impacted Existing Nodes | P4 load and approval handler; case service, allocation engine and timer engine start-up hooks; `lov_value` read interface. |
25: | New Nodes Required | `YES` — `ReferenceVersionRegistryImpl`, `ReferenceDataServiceImpl`, `ReferenceRowCache`, `ReferenceTableSchemas`, `ReferenceVersionRepository`, `ReferenceRowRepository`, `ReferenceVersionLogger`, `reference_version`, `reference_row`. |
26: | Inherited Existing Behavior | RWB-E1-044 migrations; RWB-E1-042 configuration service and `refdata.cache.ttl-seconds`; P4 access check; ACE business date from JOB-01. |
27: | Frontend Changes Required | `NO` |
28: | Backend Changes Required | `YES` |
29: 
30: ## Requirement-to-SPEC Logic Coverage
31: 
32: | REQ_REF | Requirement 
... truncated (24,192 chars total)
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

This is gold: CLAR-005 resolves same validFrom different content → 409 MSG-P3-027. CLAR-002: 13 for E1-043, E1-019 adds QUEUE_MEMBER to LOV-REF-TABLE by a list load. CLAR-004 validFrom == business date allowed.

Note CLAR-002 implies LOV-REF-TABLE changes by a "list load" but no endpoint exists for lists. Hmm.

Now check "GET /admin/lists/{listCode}" response ListOfValues with versions — schema says code + values object. Fine.

Now I should confirm the "status" values conflict: E1-043 uses VALIDATED; E1-025/E1-037 use LOADED/Loaded; LOV-VERSION-STATUS includes VALIDATED but not LOADED. The physical schema default is VALIDATED. For the answer: canonical is VALIDATED → APPROVED → ROLLED_BACK (E1-043 + schema + LOV). E1-025 and E1-037 predate/ignore that.

Now check if there is any "ReferenceLoad" extension with "rowErrors" or "checks". Not in yaml. Story §15 says "the load result (status, row count, refused checks) is returned in the response" — but schema has only 5 fields. So refused checks are in Problem.detail. Report.

Now question 2: status codes. From yaml: 201, 401, 403, 409, 422, 503. No 200 on repeat defined; 200 only for approve/rollback/verify. No 404 on the POST. No 413/415. Note the repeat behavior: 201 vs 200 ambiguous, and other stories say 409. Provide resolution per E1-043/INC-009 (200/201 with existing load) and note conflicts.

I should check if E1-043's `ReferenceLoad` includes `rows` as integer (row count) vs "rows" as a list. yaml: integer. Story says `rows` = row count. Good.

Now question 3: authorisation right(s) and capability area; approve and rollback endpoints. Done. Also verify right U = update? The permission letters C, R, U, D, A. In E1-037: "letters only from C, R, U, D, A". Right A = approve. U = update (rollback/verify). Good.

Now let me double-check the P4 TSD section on data/authority to cite capability area definition maybe lines earlier. Let me look at P4 TSD lines 1-120 for context on capability area and rights.

Also P3 TSD should mention "Reference data" capability area in its access section. Not critical.

Let me now verify the exact wording in the HTML for the reference-loads endpoint (maybe it has more detail than yaml, e.g., schema rendering with field list). Search HTML for "reference-loads" and extract nearby text.

</details>

**Tool `shell`** - completed

```json
{"command": "$p='C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.html'; $t=Get-Content -Raw $p; $i=$t.IndexOf('/admin/reference-loads'); Write-Output $i; $t.Substring($i-200,2500)"}
```

```text
29070
d><td class="">P4</td><td class="">Reference data R</td><td class="">E1</td><td class="">401, 403, 404, 503</td></tr><tr data-g="Administration"><td class="">POST</td><td class="code">/api/recovery/v1/admin/reference-loads</td><td class="">Load reference data: lists, queues, timers, templates, delegation limits</td><td class="">Administration</td><td class="">P4</td><td class="">Reference data C</td><td class="">E1</td><td class="">401, 403, 409, 422, 503</td></tr><tr data-g="Administration"><td class="">POST</td><td class="code">/api/recovery/v1/admin/reference-loads/{loadId}/approve</td><td class="">Approve a reference data load</td><td class="">Administration</td><td class="">P4</td><td class="">Reference data A</td><td class="">E1</td><td class="">401, 403, 404, 409, 503</td></tr><tr data-g="Administration"><td class="">GET</td><td class="code">/api/recovery/v1/admin/roles</td><td class="">List roles with permissions and scope</td><td class="">Administration</td><td class="">P4</td><td class="">Platform administration R</td><td class="">E1</td><td class="">401, 403, 503</td></tr><tr data-g="Administration"><td class="">GET</td><td class="code">/api/recovery/v1/admin/access-log</td><td class="">Search the access log</td><td class="">Administration</td><td class="">P4</td><td class="">Platform administration R</td><td class="">E1</td><td class="">401, 403, 503</td></tr><tr data-g="Administration"><td class="">GET</td><td class="code">/api/recovery/v1/admin/jobs</td><td class="">List loads, files and jobs with status</td><td class="">Administration</td><td class="">P1</td><td class="">Platform administration R</td><td class="">E1</td><td class="">401, 403, 503</td></tr><tr data-g="Administration"><td class="">POST</td><td class="code">/api/recovery/v1/admin/jobs/{jobId}/rerun</td><td class="">Rerun a failed load or job</td><td class="">Administration</td><td class="">P1</td><td class="">Platform administration U</td><td class="">E1</td><td class="">401, 403, 404, 409, 503</td></tr><tr data-g="Administration"><td class="">GET</td><td class="code">/api/recovery/v1/admin/data-quality/exceptions</td><td class="">List load check exceptions and reconciliation breaks</td><td class="">Administration</td><td class="">P1</td><td class="">Platform administration R</td><td class="">E1</td><td class="">401, 403, 503</td></tr><tr data-g="Administration"><td class="">GET</td><td class="code">/api/recovery/v1/admin/agent-runs</td><td class="">List agent runs with 
... truncated (2,509 chars total)
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

HTML confirms endpoint table only.

Now let me check whether the yaml declares requestBody required: true and no required fields within schema. In OpenAPI, no `required:` array means none of file/table/validFrom are formally required, though prose says required. That's a precise contract detail worth reporting: multipart fields are declared but the schema has no `required` list; prose says file/table/validFrom required.

Also file type: string/binary, no content type restriction or max size. table: string unconstrained (no enum, no x-list-of-values). validFrom: string, no format: date. That's a notable gap.

Now let me confirm the exact line numbers for the P4 TSD endpoint inventory (323-328) and details (379-443). Done.

Need line numbers for P3 TSD LOV-REF-TABLE (376) and parameter_value (283-298), reference_version (300-325).

Now the physical schema line numbers for tables:
- queue 112, queue_member 1758, parameter_catalog 1800, parameter_value 1827, reference_version 1851, reference_row 1885, delegation_limit 871, role 920, permission 938, template 954, masking_rule 1926, partner_user 1964, document_type 1982, document_checklist_item 2010, document_hub_parameter 2052, retention_class? Not in CREATE TABLE list! Wait — retention_class was expected from E1-041. The CREATE TABLE list has no retention_class. Let me grep.

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql", "pattern": "retention_class|CREATE TABLE document_checklist|CREATE TABLE partner_user|CREATE TABLE document_type|CREATE TABLE masking_rule|CREATE TABLE permission|CREATE TABLE role \\(|CREATE TABLE template|CREATE TABLE delegation_limit"}
```

```text
Found 17 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 661:     retention_class varchar(10),

  Line 684:     retention_class varchar(10) NOT NULL,

  Line 871: CREATE TABLE delegation_limit (

  Line 920: CREATE TABLE role (

  Line 938: CREATE TABLE permission (

  Line 954: CREATE TABLE template (

  Line 1926: CREATE TABLE masking_rule (

  Line 1964: CREATE TABLE partner_user (

  Line 1982: CREATE TABLE document_type (

  Line 1988:     retention_class varchar(10) NOT NULL,

  Line 2010: CREATE TABLE document_checklist_item (

  Line 3266: COMMENT ON COLUMN interaction.retention_class IS 'Retention class of the entry, set by entry type';

  Line 3277: COMMENT ON COLUMN document.retention_class IS 'Retention class';

  Line 3897: COMMENT ON COLUMN document_type.retention_class IS 'Retention class of the type';

  Line 4632: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-027', 'interaction', 'retention_class', 'LOV', 'varchar(10)', false, 'LOV-RETENTION', NULL, 'Workbench', NULL, false, 'Retention class of the entry, set by entry type');

  Line 4643: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-009', 'document', 'retention_class', 'LOV', 'varchar(10)', true, 'LOV-RETENTION', NULL, 'Workbench', NULL, false, 'Retention class');

  Line 5263: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-223', 'document_type', 'retention_class', 'LOV', 'varchar(10)', true, 'LOV-RETENTION', NULL, 'Workbench', NULL, false, 'Retention class of the type');

```

**Tool `read`** - completed

```json
{"limit": 70, "offset": 1982, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 1982-2051
1982: CREATE TABLE document_type (
1983:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1984:     doc_type_code varchar(30) NOT NULL,
1985:     label_en varchar(120) NOT NULL,
1986:     label_th varchar(120),
1987:     write_once boolean NOT NULL DEFAULT false,
1988:     retention_class varchar(10) NOT NULL,
1989:     field_definitions jsonb NOT NULL,
1990:     legal_signoff_by uuid,
1991:     legal_signoff_date date,
1992:     npa_signoff_by uuid,
1993:     npa_signoff_date date,
1994:     table_version varchar(20) NOT NULL,
1995:     valid_from date NOT NULL,
1996:     valid_to date,
1997:     reference_version_id uuid,
1998:     classify_threshold numeric(4,3),
1999:     is_active boolean NOT NULL DEFAULT true,
2000:     state varchar(40),
2001:     version integer NOT NULL DEFAULT 1,
2002:     created_at timestamptz NOT NULL DEFAULT now(),
2003:     created_by uuid,
2004:     updated_at timestamptz NOT NULL DEFAULT now(),
2005:     updated_by uuid,
2006:     CONSTRAINT uk_document_type UNIQUE (doc_type_code, table_version)
2007: );
2008: 
2009: -- Document checklist item: A document type required or expected for a case stage and route, by checklist version.
2010: CREATE TABLE document_checklist_item (
2011:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
2012:     stage_code varchar(20) NOT NULL,
2013:     route_code varchar(4),
2014:     document_type varchar(30) NOT NULL,
2015:     required boolean NOT NULL DEFAULT false,
2016:     sort_order integer NOT NULL DEFAULT 0,
2017:     table_version varchar(20) NOT NULL,
2018:     valid_from date NOT NULL,
2019:     valid_to date,
2020:     reference_version_id uuid,
2021:     is_active boolean NOT NULL DEFAULT true,
2022:     state varchar(40),
2023:     version integer NOT NULL DEFAULT 1,
2024:     created_at timestamptz NOT NULL DEFAULT now(),
2025:     created_by uuid,
2026:     updated_at timestamptz NOT NULL DEFAULT now(),
2027:     updated_by uuid,
2028:     CONSTRAINT uk_document_checklist_item UNIQUE (stage_code, route_code, document_type, table_version)
2029: );
2030: 
2031: -- Case document check: The latest document completeness check of a case against its checklist.
2032: CREATE TABLE case_document_check (
2033:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
2034:     case_id uuid NOT NULL,
2035:     checklist_version varchar(20),
2036:     
... truncated (3,167 chars total)
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

No retention_class table in Physical Schema v4 — E1-041 creates it via its own migration (V1_5_041). So the Physical Schema v4 is older than E1-041/046 additions. Important caveat: physical schema v4 lacks retention_class and merge_field? merge_field exists (line 2158). retention_class doesn't. State that: RETENTION_CLASS target table is created by RWB-E1-041's migration, absent from Physical Schema v4.

Also document_type has reference_version_id — so P5 tables link back to reference_version. Good nuance: P5 codes write their own table AND set reference_version_id (schema column). E1-025 didn't mention it but schema has it.

Similarly document_checklist_item has reference_version_id.

Check queue table for table_version and reference_version_id.

Let me read queue, template, delegation_limit, permission, masking_rule, partner_user, parameter_value, retention? quickly for columns.

</details>

**Tool `read`** - completed

```json
{"limit": 45, "offset": 112, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 112-156
112: CREATE TABLE queue (
113:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
114:     queue_code varchar(30) NOT NULL,
115:     queue_name varchar(100) NOT NULL,
116:     team_code varchar(20) NOT NULL,
117:     role_code varchar(20) NOT NULL,
118:     assignment_method varchar(20) NOT NULL DEFAULT 'ROUND_ROBIN',
119:     capacity_cap integer,
120:     overflow_queue_id uuid,
121:     rr_cursor_user_id uuid,
122:     table_version integer,
123:     is_active boolean NOT NULL DEFAULT true,
124:     state varchar(40),
125:     version integer NOT NULL DEFAULT 1,
126:     created_at timestamptz NOT NULL DEFAULT now(),
127:     created_by uuid,
128:     updated_at timestamptz NOT NULL DEFAULT now(),
129:     updated_by uuid,
130:     CONSTRAINT uk_queue UNIQUE (queue_code)
131: );
132: 
133: -- Assignment: Who holds a case or a task and from when.
134: CREATE TABLE assignment (
135:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
136:     case_id uuid NOT NULL,
137:     task_id uuid,
138:     assignee_user_id uuid NOT NULL,
139:     assigned_at timestamptz NOT NULL DEFAULT now(),
140:     ended_at timestamptz,
141:     reason varchar(20) NOT NULL,
142:     rule_id varchar(20),
143:     queue_id uuid,
144:     transfer_reason_code varchar(20),
145:     is_active boolean NOT NULL DEFAULT true,
146:     state varchar(40),
147:     version integer NOT NULL DEFAULT 1,
148:     created_at timestamptz NOT NULL DEFAULT now(),
149:     created_by uuid,
150:     updated_at timestamptz NOT NULL DEFAULT now(),
151:     updated_by uuid
152: );
153: 
154: -- Task: A unit of work on a case: a CMMN human, customer, partner or decision task.
155: CREATE TABLE task (
156:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
[Output truncated. Continue reading with offset: 157]
```

**Tool `read`** - completed

```json
{"limit": 30, "offset": 938, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 938-967
938: CREATE TABLE permission (
939:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
940:     role_id uuid NOT NULL,
941:     capability_area varchar(30) NOT NULL,
942:     letters varchar(5) NOT NULL DEFAULT '-',
943:     matrix_version varchar(20) NOT NULL,
944:     is_active boolean NOT NULL DEFAULT true,
945:     state varchar(40),
946:     version integer NOT NULL DEFAULT 1,
947:     created_at timestamptz NOT NULL DEFAULT now(),
948:     created_by uuid,
949:     updated_at timestamptz NOT NULL DEFAULT now(),
950:     updated_by uuid
951: );
952: 
953: -- Template: A letter or notice template.
954: CREATE TABLE template (
955:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
956:     template_code varchar(30) NOT NULL,
957:     template_version integer NOT NULL DEFAULT 1,
958:     language varchar(2) NOT NULL DEFAULT 'TH',
959:     product_group varchar(15),
960:     body_ref varchar(400) NOT NULL,
961:     approved_by_legal boolean NOT NULL DEFAULT false,
962:     approved_by uuid,
963:     approved_at timestamptz,
964:     valid_from date,
965:     channel varchar(15),
966:     notice_type varchar(25),
967:     signature_basis varchar(20),
[Output truncated. Continue reading with offset: 968]
```

**Tool `read`** - completed

```json
{"limit": 28, "offset": 1926, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 1926-1953
1926: CREATE TABLE masking_rule (
1927:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1928:     role_code varchar(20) NOT NULL,
1929:     field_id varchar(16) NOT NULL,
1930:     unmasked boolean NOT NULL DEFAULT false,
1931:     masking_version varchar(20) NOT NULL,
1932:     valid_from date NOT NULL,
1933:     valid_to date,
1934:     is_active boolean NOT NULL DEFAULT true,
1935:     state varchar(40),
1936:     version integer NOT NULL DEFAULT 1,
1937:     created_at timestamptz NOT NULL DEFAULT now(),
1938:     created_by uuid,
1939:     updated_at timestamptz NOT NULL DEFAULT now(),
1940:     updated_by uuid,
1941:     CONSTRAINT uk_masking_rule UNIQUE (role_code, field_id, masking_version)
1942: );
1943: 
1944: -- Role conflict: A pair of roles one person may not hold together, by version.
1945: CREATE TABLE role_conflict (
1946:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1947:     role_code varchar(20) NOT NULL,
1948:     conflicts_with varchar(30) NOT NULL,
1949:     reason varchar(200) NOT NULL,
1950:     conflict_version varchar(20) NOT NULL,
1951:     valid_from date NOT NULL,
1952:     valid_to date,
1953:     is_active boolean NOT NULL DEFAULT true,
[Output truncated. Continue reading with offset: 1954]
```

**Tool `read`** - completed

```json
{"limit": 30, "offset": 1964, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 1964-1993
1964: CREATE TABLE partner_user (
1965:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1966:     identity_ref varchar(64) NOT NULL,
1967:     partner_id uuid NOT NULL,
1968:     role_code varchar(20) NOT NULL,
1969:     valid_from date NOT NULL,
1970:     valid_to date,
1971:     is_active boolean NOT NULL DEFAULT true,
1972:     state varchar(40),
1973:     version integer NOT NULL DEFAULT 1,
1974:     created_at timestamptz NOT NULL DEFAULT now(),
1975:     created_by uuid,
1976:     updated_at timestamptz NOT NULL DEFAULT now(),
1977:     updated_by uuid,
1978:     CONSTRAINT uk_partner_user UNIQUE (identity_ref)
1979: );
1980: 
1981: -- Document type: A document type, the fields extracted from it and its Legal and NPA sign-off, by version.
1982: CREATE TABLE document_type (
1983:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1984:     doc_type_code varchar(30) NOT NULL,
1985:     label_en varchar(120) NOT NULL,
1986:     label_th varchar(120),
1987:     write_once boolean NOT NULL DEFAULT false,
1988:     retention_class varchar(10) NOT NULL,
1989:     field_definitions jsonb NOT NULL,
1990:     legal_signoff_by uuid,
1991:     legal_signoff_date date,
1992:     npa_signoff_by uuid,
1993:     npa_signoff_date date,
[Output truncated. Continue reading with offset: 1994]
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now the template table columns (E1-046 adds channel, notice_type, signature_basis, merge_codes). Let me read 954-980.

Also delegation_limit columns.

But for the report, the main need is target table names, not all columns. The CSV template list needs target {table}.{column}. Build notes gives columns but not exact physical names for all. I can map with schema where available.

Let's read template tail and delegation_limit.

</details>

**Tool `read`** - completed

```json
{"limit": 40, "offset": 954, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 954-993
954: CREATE TABLE template (
955:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
956:     template_code varchar(30) NOT NULL,
957:     template_version integer NOT NULL DEFAULT 1,
958:     language varchar(2) NOT NULL DEFAULT 'TH',
959:     product_group varchar(15),
960:     body_ref varchar(400) NOT NULL,
961:     approved_by_legal boolean NOT NULL DEFAULT false,
962:     approved_by uuid,
963:     approved_at timestamptz,
964:     valid_from date,
965:     channel varchar(15),
966:     notice_type varchar(25),
967:     signature_basis varchar(20),
968:     merge_codes jsonb,
969:     is_active boolean NOT NULL DEFAULT true,
970:     state varchar(40),
971:     version integer NOT NULL DEFAULT 1,
972:     created_at timestamptz NOT NULL DEFAULT now(),
973:     created_by uuid,
974:     updated_at timestamptz NOT NULL DEFAULT now(),
975:     updated_by uuid,
976:     CONSTRAINT uk_template UNIQUE (template_code, template_version)
977: );
978: 
979: -- Data product: One of the 14 data products, with its single system of record, owner and refresh cycle.
980: CREATE TABLE data_product (
981:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
982:     product_code varchar(25) NOT NULL,
983:     product_name varchar(80) NOT NULL,
984:     definition varchar(400) NOT NULL,
985:     system_of_record varchar(120) NOT NULL,
986:     owner_role varchar(20) NOT NULL,
987:     owner_user_id uuid,
988:     refresh_cycle varchar(10) NOT NULL,
989:     expected_by varchar(20),
990:     valid_from date NOT NULL,
991:     is_active boolean NOT NULL DEFAULT true,
992:     state varchar(40),
993:     version integer NOT NULL DEFAULT 1,
[Output truncated. Continue reading with offset: 994]
```

**Tool `read`** - completed

```json
{"limit": 35, "offset": 871, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 871-905
871: CREATE TABLE delegation_limit (
872:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
873:     decision_code varchar(8) NOT NULL,
874:     approval_level varchar(4) NOT NULL,
875:     product_group varchar(15) NOT NULL,
876:     principal_limit numeric(18,2),
877:     loss_pct_limit numeric(5,2),
878:     min_price_pct_fmv numeric(5,2),
879:     holder_user_id uuid,
880:     substitute_user_id uuid,
881:     valid_from date NOT NULL,
882:     valid_to date,
883:     limit_version varchar(20) NOT NULL,
884:     regulation_item varchar(10) NOT NULL,
885:     applies_when varchar(40),
886:     max_loss_amount numeric(18,2),
887:     max_delay_count integer,
888:     min_price_pct_principal numeric(5,2),
889:     min_received_pct numeric(5,2),
890:     max_term_years numeric(4,1),
891:     is_active boolean NOT NULL DEFAULT true,
892:     state varchar(40),
893:     version integer NOT NULL DEFAULT 1,
894:     created_at timestamptz NOT NULL DEFAULT now(),
895:     created_by uuid,
896:     updated_at timestamptz NOT NULL DEFAULT now(),
897:     updated_by uuid
898: );
899: 
900: -- List value: A value in a list of values.
901: CREATE TABLE lov_value (
902:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
903:     lov_code varchar(30) NOT NULL,
904:     value_code varchar(30) NOT NULL,
905:     label_en varchar(120) NOT NULL,
[Output truncated. Continue reading with offset: 906]
```

**Tool `read`** - completed

```json
{"limit": 25, "offset": 2052, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 2052-2076
2052: CREATE TABLE document_hub_parameter (
2053:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
2054:     param_code varchar(40) NOT NULL,
2055:     param_value varchar(200) NOT NULL,
2056:     unit varchar(20),
2057:     table_version varchar(20) NOT NULL,
2058:     valid_from date NOT NULL,
2059:     valid_to date,
2060:     reference_version_id uuid,
2061:     is_active boolean NOT NULL DEFAULT true,
2062:     state varchar(40),
2063:     version integer NOT NULL DEFAULT 1,
2064:     created_at timestamptz NOT NULL DEFAULT now(),
2065:     created_by uuid,
2066:     updated_at timestamptz NOT NULL DEFAULT now(),
2067:     updated_by uuid,
2068:     CONSTRAINT uk_document_hub_parameter UNIQUE (param_code, table_version)
2069: );
2070: 
2071: -- Document intake: A file received by the document hub, from scan to OCR, classification, extraction, matching and review.
2072: CREATE TABLE document_intake (
2073:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
2074:     source varchar(12) NOT NULL,
2075:     source_ref varchar(400) NOT NULL,
2076:     channel_code varchar(40),
[Output truncated. Continue reading with offset: 2077]
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now, let me check the P4 TSD for a data section listing reference_version/reference_row and maybe "handlers" table. Search P4 TSD for "handler" and "reference".

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P4 Access and administration v2.md", "pattern": "handler|reference_version|reference_row|lov_value|Reference data|reference table"}
```

```text
Found 13 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P4 Access and administration v2.md:
  Line 110: **lov_value** (NEW). A value in a list of values.

  Line 226: | Role | Rules and parameters | Reference data | Platform administration |

  Line 261: | RW-REFADM Reference data administrator | R | CRUD | - |

  Line 322: | API-P4-004 | GET | /api/recovery/v1/admin/lists/{listCode} | Reference data R | E1 |

  Line 323: | API-P4-005 | POST | /api/recovery/v1/admin/reference-loads | Reference data C | E1 |

  Line 324: | API-P4-006 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/approve | Reference data A | E1 |

  Line 327: | API-P4-009 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/verify | Reference data U | E1 |

  Line 328: | API-P4-010 | POST | /api/recovery/v1/admin/reference-loads/{loadId}/rollback | Reference data U | E1 |

  Line 376: | Authorization | Reference data, right R, scope applied |

  Line 387: | Authorization | Reference data, right C, scope applied |

  Line 398: | Authorization | Reference data, right A, scope applied |

  Line 431: | Authorization | Reference data, right U, scope applied |

  Line 442: | Authorization | Reference data, right U, scope applied |

```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

P4 TSD §226/261: permission matrix row for roles. Let me read lines 215-270 to get capability area rights grid (which roles hold Reference data rights). This supports Q3.

</details>

**Tool `read`** - completed

```json
{"limit": 70, "offset": 218, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Technical Specifications by Module v3\\Recovery Workbench TSD P4 Access and administration v2.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P4 Access and administration v2.md, lines 218-287
218: | Event | Direction |
219: |---|---|
220: | None | |
221: 
222: ## T6. Security and access control
223: 
224: ### T6.1 RBAC matrix
225: 
226: | Role | Rules and parameters | Reference data | Platform administration |
227: |---|---|---|---|
228: | RW-CASEOWN Case owner | R | R | - |
229: | RW-TEAMMGR Team manager | R | R | - |
230: | RW-PHONECOL Phone collector | - | R | - |
231: | RW-FIELDCOL Field collector | - | R | - |
232: | RW-RESTRUCT Restructuring officer (FCR) | R | R | - |
233: | RW-SPECIAL Hardship and vulnerability specialist | R | R | - |
234: | RW-COMPLAIN Complaint officer | R | R | - |
235: | RW-FRAUD Fraud investigator | R | R | - |
236: | RW-LITOFF Litigation officer | R | R | - |
237: | RW-ENFORCE Enforcement owner | R | R | - |
238: | RW-LEGAL Legal counsel | R | RU | - |
239: | RW-SALEOFF Sale officer | R | R | - |
240: | RW-NPAMGR NPA and asset manager | R | R | - |
241: | RW-DEBTSALE Debt sale officer | R | R | - |
242: | RW-WRITEOFF Write-off team member | R | R | - |
243: | RW-CREDITAD Credit Administration officer | R | R | - |
244: | RW-GUARANT Guarantee officer | R | R | - |
245: | RW-AGENCYMG Partner and agency manager | R | RU | - |
246: | RW-CONDUCT Conduct and QA officer | R | R | - |
247: | RW-CAPACITY Capacity and workforce planner | R | R | - |
248: | RW-PRODHEAD Product head (Mortgage, HP, SSME) | R | R | - |
249: | RW-HEADLIT Head of Litigation | R | R | - |
250: | RW-HEADNPA Head of NPA | R | R | - |
251: | RW-HEADASL Head of Asset Liquidity | R | R | - |
252: | RW-CREDCOMM Credit approval committee member | R | R | - |
253: | RW-WOCOMM Write-off committee member | R | R | - |
254: | RW-RISK Risk and model risk officer | RA | R | - |
255: | RW-COE Center of excellence analyst | CRUD | CRUD | R |
256: | RW-DATASTEW Data steward and data product owner | R | RU | R |
257: | RW-FINANCE Finance and CFO delegate | R | R | - |
258: | RW-AUDIT Internal audit | R | R | R |
259: | RW-COMPLY Compliance and PDPA officer | R | RU | R |
260: | RW-PLATADM Platform administrator | R | R | CRUD |
261: | RW-REFADM Reference data administrator | R | CRUD | - |
262: | RW-SECADM Security administrator | R | R | CRUDA |
263: | RW-BIANAL Reporting and BI analyst | R | R | - |
264: | RW-TRIBE Tribe lead and sq
... truncated (4,592 chars total)
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Important: RBAC matrix gives RW-RISK "RA" in Reference data (R and A). So the approver is RW-RISK per matrix, contradicting E1-043's assumption "no role holds it today" (E1-043 says assumed). Also RW-COE has CRUD. RW-REFADM CRUD. RW-SECADM has R in Reference data but CRUDA in Platform admin. Interesting.

Note approve endpoint's right A is present in matrix for RW-RISK and RW-COE (CRUD includes A). But E1-037 says "A repeat approve of a version already approved returns 409", while E1-043 says idempotent 200. Conflict.

Now I have enough to write the report. But let me nail down a few more exact facts:

1. Line numbers for the story's contract table: 215-223.
2. Line numbers for approve: 225-233.
3. yaml lines: 2955-3001 (request), 3002-3038 (approve), 5028-5113 (verify/rollback), 8812-8826 (ReferenceLoad), 6086-6141 (responses), 8971-8989 (Problem), 9906-9910 (RollbackRequest), 10015-10019 (VerifyRequest).
4. P4 TSD 323-328, 379-443.
5. P3 TSD 283-298 (parameter_value), 300-325 (reference_version), 376 (LOV list).
6. Schema lines 5989-6013 (25 values), 5200 (sys_fields table_code LOV-REF-TABLE).
7. Build notes (INC-003) 33-118.

Let me also verify the precise behaviour of "validFrom" validation: not before business date (equal allowed, CLAR-004). And that ON approve, valid_to of replaced version = day before new valid_from (E1-043 BR8).

Also 409 condition: "an approved version of the table already has this valid from" (E1-043 line 221). Plus CLAR-005: different content at an already-approved validFrom → 409 MSG-P3-027; same hash → returns existing load.

Question 2 asks "201/200 on repeat". Need a clear answer: 
- Spec (yaml) declares only 201 for this operation. No 200.
- Owning story AC7 says repeat returns the existing version, no second version; no status stated. §12 idempotency: "A repeat returns the existing load and writes nothing."
- So a repeat could answer 201 with the same body (as if created) or 200; the contract does not disambiguate. INC-009 CLAR-005 confirms same hash returns existing load. But no status. Some downstream stories instead specify 409 for repeat (E1-001, E1-002? E1-025, Epic 2 payment_match_rule, E1-038 version name clash). So report the conflict and recommend 200 with same body OR 201; flag as unresolved.

Actually the task is "for a build clarification answer" — so the report should surface ambiguities precisely and recommend the canonical reading.

Let me check if any document explicitly says "200 on repeat". Search "200 wi

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"limit": 40, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14", "pattern": "returns the existing load|return the existing load|existing load is returned|the first load is returned"}
```

```text
Found 24 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 2431: Writing happens on its own once the checks pass. The service writes one reference_version row with status VALIDATED and one reference_row row per file row, holding row_key and row_data as jsonb, in one transaction, which means the version and all its rows appear together or not at all. A load with any failed check writes no version and no rows (BR5). When the same file arrives again for the same table and valid from date, the unique key on table_code, valid_from and content_hash matches, the service returns the existing load and writes nothing, so there is still one version 5 and no version 6 (AC7).


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md:
  Line 6029: | X5 | The same file is loaded again for the same valid from | The existing load is returned; nothing new is written (RWB-E1-043 idempotency) | None | AC8 |

  Line 13491: | Idempotency | Table, valid from and content hash; a repeat returns the existing load |

  Line 13664: | X4 | The same file is loaded twice for the same table and valid from date | No second version; the first load is returned | None | AC7 |

  Line 13829: | Idempotency | Table code, valid from and content hash. A repeat returns the existing load and writes nothing |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 019 Roles teams and queues as data v1.md:
  Line 57: | X5 | The same file is loaded again for the same valid from | The existing load is returned; nothing new is written (RWB-E1-043 idempotency) | None | AC8 |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-009-epic-1-RWB-E1-043\specify\spec.md:
  Line 266: | CLAR-005 | AC7; SPEC-004 | What if the same valid from carries different content? | Idempotency vs conflict. | Same hash returns the existing load; different content at an already-approved valid from is refused with 409 MSG-P3-027. | RESOLVED | SPEC-004 |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 905: "4": "Writing happens on its own once the checks pass. The service writes one reference_version row with status VALIDATED a
... truncated (7,762 chars total)
```

### Assistant - 2026-11-10 18:24 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good.

Now the `validFrom` type in the multipart request has no format; but all stories say date. The canonical format is ISO 8601 date (overview "Dates ISO 8601; Asia/Bangkok business day").

Now let me confirm what "Reference data C" means: C = create, and the matrix gives RW-REFADM CRUD. Good.

Now the "approve" body: none; response 200 ReferenceLoad. Rollback body: RollbackRequest {reason:string}; reason required per E1-019 (422 MSG-GEN-001 when empty); yaml RollbackRequest has no required. Verify: VerifyRequest {note}; note required max 1000 per E1-048.

I should check the rollback response status ROLLED_BACK and idempotency: yaml/TSD say Idempotency-Key; E1-019 says repeat returns first result. But E1-025 approve repeat returns unchanged 200; E1-037 approve repeat 409. Conflict again.

Now question 7: CSV templates for other codes. Build notes §3.3 lists 15 codes with column sets. The task asks specifically PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL, QUEUE, PERMISSION, MASKING_RULE, etc. I need to answer:
- PRODUCT: build notes gives data_product columns (8) from E1-001 §13. But no CSV header names/order defined; E1-045 treats PRODUCT rows as reference_row with product fields, no template defined. So: partially defined (column set) but no header/order; and conflict on target.
- PRODUCT_PARAMETER: NOT DEFINED — no column list anywhere. Owning story E1-045. Let me verify by reading E1-045 data section/BR2 for the parameter codes and row fields. It says one row per product group and parameter code; fields: product group, parameter code, value, unit? The ProductParameter record has productGroup, parameterCode, value, unit. That's a de facto column set but no template. Let me read E1-045 §8/§11 to see if columns are named.
- SERVICE_LEVEL: record has productGroup, caseStatus, limit, unit, warnPercent, escalateToRole. No template defined.
- QUEUE/QUEUE_MEMBER: header not listed (build notes explicitly).
- PERMISSION: role_code, capability_area, letters, matrix_version (build notes).
- MASKING_RULE: role_code, field_id, unmasked, masking_version.
- DOCUMENT_TYPE etc. defined.

Let me read E1-045 §8 and §11 quickly to get field names for PRODUCT_PARAMETER and SERVICE_LEVEL.

</details>

**Tool `read`** - completed

```json
{"limit": 70, "offset": 116, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md, lines 116-185
116:     When a PRODUCT load with valid from 2026-12-15 leaves out "UNSECURED"
117:     Then the system refuses the load with MSG-P3-027 naming "UNSECURED" and 3 open cases
118: 
119:   Scenario: AC7 No parameter in force at run time
120:     Given case "RW-2026-000140" with product group "SSME" and no NOTICE_PERIOD_DAYS row for "SSME" in force
121:     When the timer engine sets the notice timer on 2026-12-01
122:     Then the system writes no notice timer
123:     Then the system places the case in the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS"
124: 
125:   Scenario: AC8 Value changes while a timer runs
126:     Given the notice timer of "RW-2026-000101" started on 2026-12-01 and expires on 2026-12-31
127:     Given PRODUCT_PARAMETER version 4 with NOTICE_PERIOD_DAYS 45 for "MORTGAGE" takes effect on 2026-12-03
128:     When the timer engine sets a notice timer on Mortgage case "RW-2026-000150" on 2026-12-03
129:     Then the timer of "RW-2026-000101" still expires on 2026-12-31
130:     Then the timer of "RW-2026-000150" expires on 2027-01-17
131: ```
132: 
133: ## 8. Business rules
134: 
135: | ID | Rule | Source |
136: |---|---|---|
137: | BR1 | Every product-specific value is a PRODUCT_PARAMETER or SERVICE_LEVEL row keyed by product group; no engine holds a product value or a product name in code | Principle 1; DT02 |
138: | BR2 | The parameters required per product are those the catalog marks with scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. Values per product are the business's (entry 90 days, DL16; service levels DL22; caps DL23) | RWB-E1-042 catalog; DL16; DL22 |
139: | BR3 | Every product in force has one SERVICE_LEVEL row per status in `servicelevel.required-statuses` (assumed NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL; DL22) | REQ-CWC-011; casemodel.txt Case status |
140: | BR4 | A load that leaves a required row missing, a value out of range or a duplicate key is refused in full | CTL-08; refdata.txt Change process step 3 |
141: | BR5 | A product with open cases cannot be removed from PRODUCT | R-UNI-38 |
142: | BR6 | A timer takes the value in force on the date it starts and keeps
... truncated (5,407 chars total)
```

### Assistant - 2026-11-10 18:24 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Confirmed: E1-045 has no CSV column list; only row semantics via the records.

Let me check E1-040 checklist CSV column set (stage_code, route_code, document_type, required, sort_order) — build notes may have it. grep E1-040 for "columns" gave nothing except schema. The story flow says "stage, route, required types". So no template.

E1-041 retention class CSV: class_code, period_months, end_action (build notes).

E1-046 template columns from build notes; merge_field columns from E1-046 §11 (merge_code, source_entity, source_field, field_id, is_required, personal_data, catalog_version, valid_from).

E1-013 measure_definition; E1-064 sys_fields; E1-037 permission/masking.

Epic 2 partner_user and payment_match_rule.

Now, "PRODUCT" CSV columns in build notes include product_code etc. from E1-001 data_product §13. But E1-045's PRODUCT code is product group catalog (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED). The columns `product_code`,`product_name`,`definition`,`owner_role`,`system_of_record`,`refresh_cycle`,`expected_by`,`owner_user_id` look like data_product, not PRODUCT. So the build-notes row conflates `data_product` code with `PRODUCT`. This is an important clarification: the registry has both `PRODUCT` (LOV-REF-TABLE; product groups) and the unregistered lowercase `data_product` code used by E1-001. Yet `data_product` is not in LOV-REF-TABLE, so the load would fail the table-code check! That's a real contradiction: E1-001 uses table = data_product, but LOV-REF-TABLE has no `data_product` value. Great catch — report as a gap.

Similarly `tracker_inventory`, `dq_rule`, `retention_rule`, `data_product_access`, `sys_fields`, `measure_definition`, `merge_field`, `payment_match_rule`, `partner_user` — of these, only PARTNER_USER is in LOV-REF-TABLE. So E1-001/E1-005/E1-006/E1-013/E1-016/E1-017/E1-046/E1-064 and Epic 2 use codes absent from LOV-REF-TABLE, which contradicts "must be a LOV-REF-TABLE code". That's a big registry gap to report.

Let me verify data_product_access etc. absent from LOV-REF-TABLE: yes, list only has 25 codes; none of those.

So answer 8 (adding a code vs value row) must cover: new code needs (a) LOV-REF-TABLE row, (b) handler registration, (c) ReferenceTableSchemas entry, (d) release if new handler. And note the pack violates this in several stories (codes used but not in LOV).

Let me double check the E1-019 QUEUE_MEMBER addition: CLAR-002 says E1-019 adds QUEUE_MEMBER to LOV-REF-TABLE by a list load. Physical schema already include

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"limit": 50, "offset": 2405, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md, lines 2405-2454
2405: ## RWB-E1-043 Reference data service with versioned tables
2406: 
2407: Module: P3 Case and workflow
2408: 
2409: ### Step 1
2410: 
2411: **In the story.** Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.
2412: 
2413: A person starts this. The reference data administrator uploads one file for one table through POST /api/recovery/v1/admin/reference-loads, sending multipart form data with the file as CSV or XLSX with one sheet, the table code, and the valid from date on which the new values take effect. The endpoint belongs to P4 and is already deployed, so your work begins at step 2. The caller must hold Reference data right C; a role with read only is refused with 403 and MSG-P4-002, which is test TC-E1-043-11. One load covers one table, and that table code has to be a value of the list LOV-REF-TABLE.
2414: 
2415: ### Step 2
2416: 
2417: **In the story.** P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.
2418: 
2419: The P4 handler writes nothing itself. It calls the method recordVersion on the published interface of this story, in package recovery.casewf.refdata.api, passing the file rows as a list of maps, the table code, the valid from date, the user ID of the caller as the author, and the load ID. Your work in build step 7 is to wire the handler to that interface and to map the exceptions it throws onto the error responses of section 12, for example 422 with MSG-P3-027 for a failed check. P4 reaches this module only through the interface and never reads reference_version or reference_row, which the boundary test RWB-TE-001 checks.
2420: 
2421: ### Step 3
2422: 
2423: **In the story.** Reference data service: checks the table code, the row schema for that table, the row keys, the valid from date and the author; computes the content hash and the next version number.
2424: 
2425: The service runs every check before it writes anything. The table code must be in LOV-REF-TABLE, read through the P4 list interface. The rows are checked against ReferenceTableSchemas, which holds the column names, types and key columns per table and comes from the parameter catalog of RWB-E1-042, so the text five in the numeric column limit_da
... truncated (6,568 chars total)
```

### Assistant - 2026-11-10 18:24 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good. Note: build notes say P4 handler writes nothing itself and calls recordVersion; but other stories say handlers write their own target. Contradiction between P4 model (registry writes reference_row) and per-code handler model (handler writes its own table). The build notes INC-003 reconcile: "Most E1-043 tables → reference_version + reference_row; PARAMETER → parameter_value directly; QUEUE → reference_row then applier; P5 → own table". For PARAMETER, the handler writes parameter_value, contradicting E1-042's use of the reference registry? E1-042 says ParameterLoadHandler with approve/rollback, likely its own store. So PARAMETER does not write reference_version/reference_row at all. Need to state.

Wait: E1-042 §11 says writes parameter_catalog and parameter_value. And §12 says POST reference-loads with table PARAMETER. The build notes confirm parameter_value directly, catalog not by load. Good.

Does the PARAMETER load also create a reference_version row? No evidence. The approve endpoint would then have to work on loadId — but is load_id stored in parameter_value? parameter_value has no load_id column. Hmm! That's a gap: approve takes {loadId} (uuid) and parameter_value has no load_id. So either a reference_version row is created for every load (including PARAMETER) as the load header, or the loadId can't be resolved. E1-043's reference_version has load_id uuid NOT NULL. If PARAMETER writes parameter_value only, there's no load record for the approve endpoint to find. This is a genuine contract bug worth flagging: PARAMETER needs a reference_version header (or parameter_value needs load_id) for `{loadId}/approve`.

I'll flag it as an unresolved gap with the two possible readings.

Now let me verify parameter_value has no load_id → confirmed lines 1827-1848.

Also queue/queue_member have no load_id/reference_version_id, so the applier must keep table_version. Fine.

Now, what about `reference_row` unique (row_key) in schema vs (version_id,row_key) in story. If schema is authoritative, two versions of the same table can't both have the same row key — that breaks versioning. This is a serious defect in Physical Schema v4 line 1897. E1-043 migration says UNIQUE(version_id,row_key). So Physical Schema v4 is wrong; E1-043's migration corrects. Report.

Now check the lov_value unique constraint on (lov_code,value_code) to see whether adding a value row is a new row. Read lov_value definition.

</details>

**Tool `read`** - completed

```json
{"limit": 25, "offset": 900, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 900-924
900: -- List value: A value in a list of values.
901: CREATE TABLE lov_value (
902:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
903:     lov_code varchar(30) NOT NULL,
904:     value_code varchar(30) NOT NULL,
905:     label_en varchar(120) NOT NULL,
906:     label_th varchar(120),
907:     sort_order integer NOT NULL DEFAULT 0,
908:     valid_from date NOT NULL,
909:     is_active boolean NOT NULL DEFAULT true,
910:     state varchar(40),
911:     version integer NOT NULL DEFAULT 1,
912:     created_at timestamptz NOT NULL DEFAULT now(),
913:     created_by uuid,
914:     updated_at timestamptz NOT NULL DEFAULT now(),
915:     updated_by uuid,
916:     CONSTRAINT uk_lov_value UNIQUE (lov_code, value_code)
917: );
918: 
919: -- Role: A Workbench role, held as data.
920: CREATE TABLE role (
921:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
922:     role_code varchar(20) NOT NULL,
923:     role_name varchar(80) NOT NULL,
924:     role_class varchar(15) NOT NULL,
[Output truncated. Continue reading with offset: 925]
```

**Tool `read`** - completed

```json
{"limit": 22, "offset": 918, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v4.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql, lines 918-939
918: 
919: -- Role: A Workbench role, held as data.
920: CREATE TABLE role (
921:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
922:     role_code varchar(20) NOT NULL,
923:     role_name varchar(80) NOT NULL,
924:     role_class varchar(15) NOT NULL,
925:     default_scope varchar(8) NOT NULL,
926:     entra_group varchar(120),
927:     is_active boolean NOT NULL DEFAULT true,
928:     state varchar(40),
929:     version integer NOT NULL DEFAULT 1,
930:     created_at timestamptz NOT NULL DEFAULT now(),
931:     created_by uuid,
932:     updated_at timestamptz NOT NULL DEFAULT now(),
933:     updated_by uuid,
934:     CONSTRAINT uk_role UNIQUE (role_code)
935: );
936: 
937: -- Permission: What a role may do in one capability area.
938: CREATE TABLE permission (
939:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
[Output truncated. Continue reading with offset: 940]
```

### Assistant - 2026-11-10 18:24 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now let me check the API spec's security scheme and base path, and whether requestBody has encoding. Not necessary.

One more: "Is there a dryRun?" No request field. But the physical schema has `dry_run_counts` on reference_version (line 1865) and the RWB-E1-029 rule load does a dry run. Also `reference_version.dry_run_counts` is described as "Counts of live cases each changed rule row would move, from the dry run" — so it's rule-load-only, not reference loads. Answer: no dryRun parameter; dry run is a rule-version feature (POST /admin/rule-versions), and dry_run_counts is a stored column populated by that path.

Now also verify whether the E1-043 response includes `rows` and whether any "checks"/"errors" array is in contract. No.

Let me check if "ReferenceLoad" is used for the verify response with verifiedBy/verifiedAt — schema lacks them, so yaml is behind E1-048. Another spec drift.

Now let me confirm the exact status codes in E1-048 verify: 422 before valid from (MSG-GEN-003), 422 empty note.

Also rollback: 409 no earlier version (MSG-P3-015), 422 empty reason (MSG-GEN-001), right U.

Now think about question 2's "201/200 on repeat". Also approve repeat: 200 (E1-043) vs 409 (E1-037). And rollback repeat: 200.

Now the report structure:

1. Request schema
- Endpoint, module, capability, content type
- Table of fields: name, location, type in yaml, format, required (declared vs prose), allowed values, notes
- single code; no list/array; one file per call
- validFrom present, string (no format in yaml), ISO date, not before business date, equal allowed
- no dryRun; no query params; no body JSON
- Idempotency-Key: global rule + TSD, not declared as parameter in yaml; natural idempotency key table+validFrom+SHA-256(content)
- no content hash field in request; computed server-side SHA-256 over rows sorted by key
- optional E1-048 fields changeRequestRef/impactSummary/rollbackPlan (max lengths) — described in yaml description but absent from schema
- file constraints: CSV or XLSX one sheet; no size/type limits on this endpoint (no 413/415 responses); encoding not stated

2. Response and statuses
- ReferenceLoad schema (5 fields, types), 201
- repeat behaviour: ambiguity 201 vs 200 vs 409, with sources; CLAR-005 resolution
- 409 conditions and body
- 422 conditions and body
- 401/403/503; no 404/400/413/415 declared
- Problem schema fields
- row errors location (Problem.detail), not response body
- status value VALIDATED (canonical), with LOADED conflict

3

_[truncated]_

</details>

**Tool `grep`** - error

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 064 Data dictionary and lineage v1.md", "pattern": "sys_fields|owner_role|refresh_cycle|late_behavior|interface_id|reference-load|table"}
```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 013 Baseline measures v1.md", "pattern": "measure_code|formula|CSV|column|header"}
```

```text
Found 16 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 013 Baseline measures v1.md:
  Line 28: Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. This story holds each measure's definition, data product and formula as an approved data row, publishes the values for business date 27 November 2026 as a frozen baseline, and sends the nightly extract to the data lake for the Power BI data set. It serves REQ-RDF-012 and NFR-065 (measures from Workbench records, not a separate count), and the FSD P9 measure "measures read from the decision log and Workbench records, 100 percent".

  Line 42: 2. System: checks each row has a measure code, name, formula, data product, unit, approver and approval date; any failure refuses the whole load.

  Line 54: | X1 | A definition row has no formula or no data product | Load refused in full | MSG-GEN-001 | AC4 |

  Line 65: | Negotiable | The measures, formulas and age bands are data rows the Tribe agrees |

  Line 82:     Given each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20

  Line 85:     Then each measure returns its data product and formula through MeasureCatalog

  Line 101:   Scenario: AC4 Definition without a formula refused

  Line 102:     Given a definition file where row "TIME_IN_STAGE" has no formula

  Line 104:     Then the system refuses the load in full with MSG-GEN-001 naming "formula"

  Line 138: | BR1 | Each measure is published only under a definition in force that names its data product, formula, unit and approver | REQ-RDF-012; Principle 1 |

  Line 179: | DF-RPT-032 | measure_definition | measure_code | Write |

  Line 181: | DF-RPT-034 | measure_definition | formula | Write |

  Line 189: | DF-RPT-042 | measure_snapshot | measure_code | Write |

  Line 245: - Database: new tables measure_definition (unique measure_code, definition_version) and measure_snapshot (unique measure_code, definition_version, business_date, product_group, dimension_code, dimension_value; trigger refusing UPDATE or DELETE where frozen = true). Flyway migration `V1_013__measures.sql`. P9 owns both tables.

  Line 278: | TC-E1-013-04 | AC4, BR7 | System | TIME_IN_STAGE with no formula |

  Line 289: - No business value in code: measures, formulas, age bands and the baseline date are data or configuratio
... truncated (2,504 chars total)
```

### Assistant - 2026-11-10 18:24 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good enough.

Now let me verify whether there is a story E1-064 filename (maybe "Data dictionary and lineage" named differently). Not critical.

Let me check the P5 TSD for document_type/document_checklist/retention to see if it mentions reference loads at all (no matches earlier). So P5 ownership is via stories, not TSD. Report.

One more check: the P4 TSD's T-A.1 lists API-P4-009/010 as E1; P5 TSD has no such endpoints.

Now I also want the exact lov_value sort order and labels for the answer — have them.

Need line 5200 quote for table_code field with LOV-REF-TABLE. Good.

Now let me ensure the report states the "reference-data table code registry" is `lov_value` where lov_code='LOV-REF-TABLE', read through GET /admin/lists/{listCode} (Reference data R). And column definitions in ReferenceTableSchemas from parameter_catalog. Is there a table listing per-code schema? No. That's a registry gap: no per-code column registry table; handler owns it.

Also the physical schema has `sys_fields` row DF-REF-160 table_code with lov_code LOV-REF-TABLE, which is the only formal constraint tying table_code to the list.

Now, "any content hash/Idempotency-Key header?" Answer both:
- Content hash: not supplied; computed server-side SHA-256 over rows sorted by key; stored in reference_version.content_hash char(64); part of the idempotency key and UNIQUE(table_code, valid_from, content_hash).
- Idempotency-Key header: global API rule says POSTs carry it; P4 TSD lists it for API-P4-005/006/009/010; but the OpenAPI operation does not declare the header parameter and the owning story E1-043 defines idempotency without it. So it is documented in prose, absent from the machine contract. Later stories (E1-019, E1-037, E1-038, E1-042, Epic 2) rely on the header.

Let me confirm P4 TSD line 388 "Idempotency-Key header" — yes.

Now let's check whether the requestBody `required: true` at line 2966-2967 applies. Yes.

Also, no `required` array in the multipart schema (lines 2971-2979). So OpenAPI validators won't enforce file/table/validFrom. State.

Now, file content: CSV or XLSX, one sheet. XLSX with multiple sheets? Rejected/one sheet only. E1-019 uses two sheets = two calls (one per table code). Good.

Now, `table` allowed values: must be a code in LOV-REF-TABLE AND must have a registered handler; codes with no handler are refused (build notes §3.1 41). Unknown code → 422? INC-009 TC-E1-043-12 says "Unknown table code | Refused; no version". Which status? Probably 422 MSG-P3-027

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"limit": 20, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 2 v5.md", "pattern": "partner_user"}
```

```text
Found 13 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v5.md:
  Line 5939: - Parameters in the catalog: rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE; rwb.access.partner.instruction-types.PT-VALUER=APPRAISE; rwb.access.partner.instruction-types.PT-AGENCY=COLLECT (assumed; owner RW-AGENCYMG); rwb.refload.approver.partner_user=RW-SECADM.

  Line 5945: 3. Reference data administrator (RW-REFADM): loads the partner user binding (partner identity, partner ID, role, valid from, valid to) with POST /admin/reference-loads table "partner_user"; RW-SECADM approves it.

  Line 6075: | DF-REF-213 | partner_user | identity_ref | Write, read |

  Line 6076: | DF-REF-214 | partner_user | partner_id | Write, read |

  Line 6077: | DF-REF-215 | partner_user | role_code | Write, read |

  Line 6078: | DF-REF-216 | partner_user | valid_from | Write, read |

  Line 6079: | DF-REF-217 | partner_user | valid_to | Write, read |

  Line 6106: **POST /api/recovery/v1/admin/reference-loads** (API-P4-005) with table "partner_user"; Reference data C; Idempotency-Key header. Approve with POST /admin/reference-loads/{loadId}/approve by RW-SECADM (approver role for the table).

  Line 6126: | AccessAndAdministrationController | Controller | Reference load for table partner_user (shared load endpoint) |

  Line 6130: | PartnerUserRepository | Repository | Reads and writes partner_user rows |

  Line 6131: | PartnerUser | Entity | Maps the new partner_user table |

  Line 6134: - Database: creates table partner_user (id uuid, identity_ref varchar(64), partner_id uuid, role_code varchar(20), valid_from date, valid_to date, plus the standard columns) with Flyway migration V_E2_019__partner_user.sql; unique index on (identity_ref, valid_from); no foreign key to partner, which is S9's table.

  Line 6137:   1. Create the partner_user migration, entity and loader with validation.

```

**Tool `grep`** - completed

```json
{"limit": 20, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md", "pattern": "partner_user|PartnerUser"}
```

```text
Found 4 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 2 v2.md:
  Line 1059: **In the story.** Reference data administrator (RW-REFADM): loads the partner user binding (partner identity, partner ID, role, valid from, valid to) with POST /admin/reference-loads table "partner_user"; RW-SECADM approves it.

  Line 1061: Two people do this. The reference data administrator loads the binding file through the shared reference load endpoint for the table partner_user, and the security administrator approves it, as the parameter rwb.refload.approver.partner_user says. The binding ties one directory identity to one firm and one partner role for a period; an identity with no active binding is refused. Create the table partner_user with the migration V_E2_019__partner_user.sql, holding id, identity_ref, partner_id, role_code, valid_from and valid_to with the standard columns, and a unique index on identity_ref and valid_from. Add no foreign key to partner, which is a column forced to match a row in another table, because partner belongs to the partner management module. Build PartnerUserLoader to check the partner IDs through the S9 interface, to allow partner role codes only, and to refuse an identity bound twice in one period.

  Line 1073: Code does this on every sign-in, with no person involved. Extend SessionResolver from RWB-E1-022 to tell the partner route from the bank route and to make four checks. The token has to come from the partner directory, so a bank identity on this route is refused with MSG-P4-001 and an AC-DENY entry with reason BANK_IDENTITY_ON_PARTNER_ROUTE. The amr claim, which is the list in the token of how the person proved who they are, has to hold "mfa", or the session is refused with 401 and MSG-P4-005. The identity has to map to exactly one partner role: two partner role groups, or a partner and a bank group together, are refused with MSG-P4-006 and an incident to the security administrator queue. Last, read the active binding from partner_user; with none, refuse with 401, MSG-P4-001 and reason NO_PARTNER_BINDING.

  Line 1097: Code does this on each request, and no job and no person ends the session. Build PartnerSessionRevalidation to read the binding from partner_user and the firm status from the S9 interface again once the refresh interval has passed, with the interval taken from the property rwb.access.membership-refresh-minutes, five minutes. A firm that
... truncated (2,895 chars total)
```

### Assistant - 2026-11-10 18:25 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

PARTNER_USER target = partner_user, table code lowercase in story ("partner_user") vs LOV uppercase PARTNER_USER. Confirms case mismatch.

Now check payment_match_rule target and columns — build notes already.

Now, one more: E1-045 "PRODUCT" — check §13 database says no new table and reads reference_row. Confirmed line 230.

I should verify E1-001's `data_product` code isn't in LOV-REF-TABLE and that its handler is DataProductCatalogHandler. Yes.

Now, the report needs to be thorough but readable. Given "Very thorough", a long structured report with tables is appropriate. Let me also double-check a few line numbers I plan to cite:

- yaml 2955 endpoint, 2966-2979 request body, 2980-2984 description, 2985-3001 responses.
- yaml 3002-3038 approve.
- yaml 5028-5070 verify, 5071-5113 rollback.
- yaml 8812-8826 ReferenceLoad.
- yaml 8971-8989 Problem.
- yaml 9906-9910 RollbackRequest; 10015-10019 VerifyRequest.
- yaml 6087-6141 error components.
- html line 42 idempotency rule (the whole HTML is one line 42? The shell output says line 42 contains the body. Actually the grep earlier showed line 42 for everything, meaning the HTML is minified into few lines. I'll cite "HTML overview, line 42" with the rule).

- P4 TSD 323-328 inventory; 379-388 API-P4-005; 390-399 approve; 423-443 verify/rollback; 226-269 RBAC.
- P3 TSD 283-298 parameter_value; 300-325 reference_version; 376 LOV.
- Schema 5989-6013 LOV; 5200 sys_fields; 1827-1848 parameter_value; 1851-1882 reference_version; 1885-1898 reference_row; 112-131 queue; 1758-1774 queue_member; 871-898 delegation_limit; 920-935 role; 938-951 permission; 954-977 template; 1926-1942 masking_rule; 1964-1979 partner_user; 1982-2007 document_type; 2010-2029 document_checklist_item; 2052-2069 document_hub_parameter; 980-? data_product.
- E1-043 story 24 story, 34-37 preconditions, 41-49 flow, 53-61 exceptions, 154-162 BRs, 168-173 states, 215-233 contract, 280-284 DB, 339-343 guardrails.
- E1-042 201-211 contract, 40-49 flow, 148-156 BR, 240-241 components, 250 DB.
- INC-003 build notes 33-118 (routing rule 37-42, table 47-52, CSV 56-93, other codes 95-118), 120-141 build vs runtime, 177-185 open items.
- INC-009 spec 263-269 CLARs, 162-173 load checks.
- E1-019 217-239 contract, 279-281 DB.
- E1-025 181-199 contract, 234-235 DB.
- E1-037 218-232 contract, 261 DB.
- E1-038 198-202 contract, 237 DB.
- E1-040 236 DB.
- E1-041 258 DB.
- E1-045 185-193 contract, 230 DB.
- E1-046 198-207 contract, 242 DB.
- E1-048 181-190 contrac

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 038 Delegation of authority table as reference data v1.md", "pattern": "Loader|Handler"}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 038 Delegation of authority table as reference data v1.md:
  Line 44: 3. Workbench (DelegationLimitLoader): validates the file whole and stores 218 rows with status Loaded.

  Line 231: | DelegationLimitLoader | Service | Validates the file whole: known codes, required fields, no repeated rows, highest principal limit per level does not fall from L6 to L1 |

  Line 242:   3. Build DelegationLimitLoader with whole-file validation; tests for AC1 and AC4.

```

**Tool `grep`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md", "pattern": "Loader|Handler"}
```

```text
Found 4 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md:
  Line 43: 2. Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.

  Line 252: | PermissionMatrixLoader | Service | Validates a matrix file whole and stores rows with status Loaded |

  Line 253: | MaskingRuleLoader | Service | Validates a masking file: known role codes, field IDs that exist in sys_fields with is_personal true |

  Line 265:   2. Build PermissionMatrixLoader and MaskingRuleLoader with whole-file validation and a difference report against the version in force; tests for AC5.

```

### Assistant - 2026-11-10 18:25 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now I have all handlers. Missing: REGION, EXPOSURE_BAND, ROLE, TEAM, LEGAL_PERIOD, HOLIDAY — generic registry only (no named handler). PRODUCT, SERVICE_LEVEL, PRODUCT_PARAMETER — generic + ProductCompletenessCheck.

Wait: does E1-043 use a handler per code at all? It uses `ReferenceTableSchemas` (column defs) and the registry. No ReferenceTableHandler in E1-043 itself; ReferenceTableHandler is introduced in E1-001 as "published interface of P4 that P1 implements, from RWB-E1-043". So E1-043 defines the interface; P1 implements for its codes. So the generic handlers are the registry itself.

Now, the map for ENTRY/EXCLUSION/ALLOCATION/ASSIGNMENT/TRANSFER: rule-load path (POST /admin/rule-versions), owner E1-029, target rule_row + rule_version. They are in LOV-REF-TABLE but should not be sent to reference-loads; no reference handler exists → refused. State.

Now, one more nuance for question 5: "does the caller choose a database table, a table code, a type, or a column?" Answer: a table code only. `kind` and `value_type` are catalog metadata used for parsing/range checks, not routing. No user-supplied mapping.

Now, question 6 asks "What happens to product_group, version_no, status, author, approver, valid_from, valid_to." Build notes covers product_group, version_no, valid_from, status, author, approver/approved_at. valid_to: not explicitly in the mapping table. Infer: valid_to is NULL on load and set on approval of the successor (day before next valid_from) — per E1-043 BR8. I'll state that, marking it as derived from BR8, not from the PARAMETER mapping table.

Also for PARAMETER: is there a status "VALIDATED" on load? Build notes says yes. E1-042 states state transitions VALIDATED→APPROVED→ROLLED_BACK. Good.

Version_no: "Next number for the key and environment. The seed is version 1." Note product_group NULL affects uniqueness: UK(param_key, environment, product_group, version_no) with NULL product_group — in PostgreSQL, NULLs are distinct in unique constraints by default, so duplicates possible; PG15 NULLS NOT DISTINCT could fix. Worth flagging as a build risk: the unique key includes a nullable product_group, so PARAMETER rows (product_group NULL) are not protected by the unique constraint unless NULLS NOT DISTINCT is used. That's a precise, valuable observation for a build clarification. Schema line 1847.

Now question 6 also asks separators/encoding/max rows/size "if stated". Answer: comma-separated shown by example; encoding not stated; no max rows/

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"limit": 40, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench API Specification v2.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml, lines 1-40
1: # Recovery Workbench API specification. Henka Group, 28 October 2026.
2: openapi: 3.1.0
3: info:
4:   title: Recovery Workbench API
5:   version: 1.0.0
6:   description: Endpoints of the recovery module in the ACE service. Every endpoint checks the role, the capability area, the right and the scope.
7:     (C) Siam Commercial Bank and Henka Pte Ltd
8: servers:
9: - url: /api/recovery/v1
10:   description: Relative to the ACE service in each environment
11: security:
12: - entraId: []
13: tags:
14: - name: Cases
15: - name: Work
16: - name: Decisions
17: - name: Treatment
18: - name: Litigation
19: - name: Assets
20: - name: Debt sale
21: - name: Write-off
22: - name: Money
23: - name: Documents
24: - name: Interactions
25: - name: Partners
26: - name: Partner portal
27: - name: Administration
28: - name: Reporting
29: paths:
30:   /cases:
31:     get:
32:       tags:
33:       - Cases
34:       summary: List cases in the caller's scope with filters and paging
35:       operationId: getCases
36:       x-module: P3
37:       x-capability:
38:         area: Case record
39:         right: R
40:       x-first-release: E1
[Output truncated. Continue reading with offset: 41]
```

### Assistant - 2026-11-10 18:25 | opencode-go/deepseek-v4.1-flash | explore

# POST /api/recovery/v1/admin/reference-loads — contract and LOV-REF-TABLE registry

## Source key

| ID | Absolute path |
|---|---|
| **S1** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.yaml` |
| **S2** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.html` |
| **S3** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 043 Reference data service with versioned tables v1.md` |
| **S4** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P3 Case and workflow v2.md` |
| **S5** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P4 Access and administration v2.md` |
| **S6** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P5 Document hub v2.md` |
| **S7** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql` |
| **S8** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 042 Central configuration service and parameter catalog v1.md` |
| **S9** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-003-epic-1-RWB-E1-042\build\E1-042 migration and clarification notes.md` |
| **S10** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-009-epic-1-RWB-E1-043\specify\spec.md` |
| **S11** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md` |
| **S12** | `...\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 019 Roles teams and queues as data v1.md` |
| **S13** | `...\RWB E1 025 Document types and fields agreed v1.md` |
| **S14** | `...\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md` |
| **S15** | `...\RWB E1 038 Delegation of authority table as reference data v1.md` |
| **S16** | `...\RWB E1 040 Document checklist per case type as reference data v1.md` |
| **S17** | `...\RWB E1 041 Retention classes and virus scan on intake v1.md` |
| **S18** | `...\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md` |
| **S19** | `...\RWB E1 046 Template and merge field catalog as data v1.md` |
| **S20** | `...\RWB E1 048 Rule change audit report v1.md` |
| **S21** | `...\RWB E1 001 Recovery tables for the 14 data products v1.md` |
| **S22** | `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v5.md` |

---

## Bottom line (direct answers)

1. **Request:** `multipart/form-data` with exactly three declared fields — `file` (binary), `table` (string, **one** code), `validFrom` (string/date). No array, no `dryRun`, no `contentHash`, no `versionLabel`, no query parameters. The OpenAPI schema declares **no `required` list**; prose makes all three required.
2. **Response:** only **201** is declared, body `ReferenceLoad` = `{id, table, validFrom, status, rows}`. A repeat is **not** an error in the owning story (returns the existing load, writes nothing); **no 200 is declared**, and several downstream stories wrongly say 409.
3. **Auth:** capability area **Reference data**, right **C** (create) to load, **A** to approve, **U** to verify/rollback, **R** to read lists.
4. **LOV-REF-TABLE has exactly 25 codes**, sort 1–25 (`PRODUCT` … `TRANSFER`). E1-043 serves 13; 20 are reference-data codes and 5 are rule-table codes. `DOCUMENT_HUB_PARAMETER` is **not** in the list despite the YAML saying it is accepted.
5. **The caller chooses one table code only.** Never a database table, never a type, never a column. **No user-supplied column mapping is allowed.** Routing is code → registered handler → handler's own target.
6. **PARAMETER CSV:** header `key,environment,value`, comma-separated, mapped to `parameter_value.param_key`, `.environment`, `.param_value`; `product_group` NULL; `version_no` next per key+environment; `status` VALIDATED on load; author = caller; approver/approved_at only on approve; `valid_from` = request date; `valid_to` derived at successor approval.
7. **Most other codes have a column set but no formal template/header order.** `PRODUCT_PARAMETER`, `SERVICE_LEVEL`, `QUEUE`, `QUEUE_MEMBER` are **NOT DEFINED**. `OI-E1-042-005` records that no consolidated template register exists.
8. **A value row is a load + approval (no release). A new table code is a code change:** LOV row + registered handler + schema entry (+ target table migration) and a release. Adding a LOV row alone does not make a code loadable.

---

## 1. Request schema

**Operation:** `postAdminReferenceLoads`, tag `Administration`, `x-module: P4`, `x-capability.area: Reference data`, `x-capability.right: C`, `x-first-release: E1` — **S1:2955-2965**. Server base path `/api/recovery/v1`, global `security: entraId` — **S1:8-12**.

| Multipart field | OpenAPI type | Required in OpenAPI | Required in prose | Allowed values / notes |
|---|---|---|---|---|
| `file` | `string`, `format: binary` | **No** — the schema has no `required:` array (**S1:2971-2979**) | Yes — "`file` (CSV or XLSX, one sheet)" (**S3:219**) | CSV or XLSX, **one sheet only**; two sheets = two calls (**S12:217-221**; **S9:40**) |
| `table` | `string` (no enum, no `x-list-of-values`, no maxLength) | No | Yes — "`table` (a LOV-REF-TABLE code)" (**S3:219**) | **One** code. Must be a `LOV-REF-TABLE` value **and** have a registered handler |
| `validFrom` | `string` — **no `format: date`** (**S1:2978-2979**) | No | Yes — "`validFrom` (date)" (**S3:219**) | ISO 8601 date (**S2:42** "Dates ISO 8601; dates in the Asia/Bangkok business day"). Must not be **before** the business date; **equal is allowed** (**S10:265 CLAR-004**) |
| `changeRequestRef` | **Not in schema**; prose only | — | Optional | max 30 (**S1:2980**; **S20:181**) |
| `impactSummary` | **Not in schema**; prose only | — | Optional | max 1000 (**S20:181**) |
| `rollbackPlan` | **Not in schema**; prose only | — | Optional | max 1000 (**S20:181**) |

### Is `table` one code or a list?
**One code, one file, one call.**

- "uploads a load file for **one table code** with a valid from date" — **S3:41**.
- "One load covers **one table**, and that table code has to be a value of the list LOV-REF-TABLE" — **S11:2413**.
- "`table` is a required multipart field… **One POST carries one file for one table code.** Loading three tables means three calls with the same `validFrom`" — **S9:39-40**.
- Two-sheet workbook → "**two calls, one per table code**" — **S11:1097**.

### Is there a `validFrom`?
Yes, as a multipart **form field** (not a query parameter), `string` with no `format` in the machine contract. Validation: "The valid from date must not be before the business date (AC6)" — **S11:2425**; boundary ruled "Equal to the business date is allowed; earlier is refused" — **S10:265**; BR6 — **S3:159**.

### Is there a `dryRun`?
**No.** No `dryRun` field, query parameter or header exists on this endpoint anywhere in S1, S3, S5 or S8–S10. The only dry run in the pack is the **rule-version** load (`POST /admin/rule-versions`, RWB-E1-029, **S11:1693-1695**), and `reference_version.dry_run_counts` is a stored column described as "Counts of live cases each changed rule row would move, from the dry run" — **S7:1865** and **S7:3846**. It is not a request option on reference loads.

### Content hash / Idempotency-Key
- **Content hash: computed server-side, never supplied.** "computes the content hash, a **SHA-256 over the rows sorted by key**" — **S11:2425**; stored as `content_hash char(64) NOT NULL` — **S7:1863**; uniqueness `UNIQUE (table_code, valid_from, content_hash)` — **S3:282**, **S10:80**.
- **Idempotency-Key header: documented in prose, absent from the machine contract.**
  - Global rule: "POST requests carry an **Idempotency-Key** header; a repeat returns the first result" — **S2:42**.
  - P4 TSD: "Idempotency | **Idempotency-Key header**" for API-P4-005 (and 006/009/010) — **S5:388, 399, 432, 443**.
  - But the OpenAPI operation declares **no header parameter** (**S1:2955-3001**), and the owning story's idempotency rule is the **natural key** "Table code, valid from and content hash" — **S3:223**.
  - Downstream stories do rely on the header: **S12:239**, **S14:222**, **S15:202**, **S18:193**, **S22:6106**.

### Other request facts
- No JSON body, no query parameters, no `versionLabel` field. Where a version label exists (e.g. `DOA-2026.11`, `DOCTYPE-2026.11`), it is **carried inside the file**, not in the request — **S11:2129**; **S13:33**.
- No `413`/`415` responses are declared for this endpoint, so **no file size or media-type limit is stated**. (`413/415` + MSG-P5-001 exist only in the shared error components — **S1:6118-6129**.)
- File encoding and delimiters are **not stated** for the generic endpoint.

---

## 2. Response schema and status codes

### Success body
`ReferenceLoad` — **S1:8812-8826**:

| Field | Type | Meaning |
|---|---|---|
| `id` | string, uuid | load identifier used as `{loadId}` on approve/rollback/verify (naming only; see gap G9) |
| `table` | string | the table code submitted |
| `validFrom` | string, date | effective date |
| `status` | string | `VALIDATED` on load (**S3:220**), `APPROVED` after approve, `ROLLED_BACK` after rollback |
| `rows` | integer | **row count**, not an array (**S3:220**; **S11:1097**) |

There is **no** `versionNo`, `contentHash`, `author`, `approver`, `rowErrors`, `checks`, `verifiedBy`, `verifiedAt`, `changeRequestRef`, `impactSummary` or `rollbackPlan` in the schema — even though **S1:2980-2982** says the schema "adds" them and **S20:190** returns `verifiedBy`/`verifiedAt`.

### Status codes — declared set (**S1:2985-3001**; **S5:386**)

| Code | Condition | Message |
|---|---|---|
| **201** | Load validated and stored | — (only success code declared) |
| **401** | No session | MSG-P4-001 (**S1:6093-6098**) |
| **403** | No Reference data **C** | MSG-P4-002 |
| **409** | "an approved version of the table already has this valid from"; also different content at an already-approved validFrom | MSG-P3-027 (**S3:221**; **S10:266 CLAR-005**) |
| **422** | A row/schema/key check failed, valid-from in the past, unknown table code, or file has no rows | MSG-P3-027 or MSG-GEN-001 (**S3:221**) |
| **503** | Store unavailable | — |

No `400`, `404`, `413` or `415` is declared on this operation.

### Error body
`application/problem+json` → `Problem` — **S1:8971-8989**: `type`, `title`, `status`, `detail`, `messageCode`, `messageTh`, `field`, `traceId`. The row/column failure is carried in `detail`, not in the success body ("naming row 12 and column `limit_days`" — **S3:110**).

The shared component descriptions are looser than the stories:
- `E409` lists MSG-P3-005, MSG-GEN-004, MSG-P7-001, MSG-P7-002 — **does not list MSG-P3-027** (**S1:6111-6117**).
- `E422` lists MSG-GEN-001/002/003 — **does not list MSG-P3-027** (**S1:6130-6135**).
- The YAML description contradicts the story: "a failed check returns **409 or 422** with MSG-P3-027" (**S1:2984**) vs story **422** (**S3:221**).

### Repeat load: 201 / 200 / 409?
The pack is **not consistent**. Canonical reading (owning story + clarification):

| Source | Behaviour on repeat | Status stated? |
|---|---|---|
| **S3:58 X4** | "No second version; the first load is returned" | **No status stated** |
| **S3:223** | "A repeat returns the existing load and writes nothing" | No |
| **S3:125-129 AC7** | "the response returns the version 5 load; there is still exactly one version 5" | No |
| **S10:266 CLAR-005** | "Same hash returns the existing load; **different content at an already-approved valid from is refused with 409 MSG-P3-027**" | 409 for the conflict case |
| **S1:2985-3001** | Only 201 declared | **No 200** |
| **S11:2431** | unique `(table_code, valid_from, content_hash)` matches → returns existing load | No |
| **S21:270**, **S11:180**, **S13:189**, **S22:8485** | repeat is refused with **409** (MSG-P1-011 / MSG-P3-027 / MSG-P1-002) | 409 |

**Build answer:** the operation has one declared success code, **201**; a same-hash repeat returns the **same 201 body** and writes nothing, unless the team chooses to model "already exists" as 200 (not declared). The **409-on-identical-repeat** statements in E1-001/E1-005/E1-025/Epic 2 contradict E1-043 and should be treated as defects in those stories. 409 is correct **only** for same `(table, validFrom)` with **different content** while an approved version already exists.

---

## 3. Authorisation, capability area, approve and rollback

**Capability area: `Reference data`.** Rights are the letters `C, R, U, D, A` (**S14:43**).

| Operation | Endpoint | Right | API ID | Evidence |
|---|---|---|---|---|
| Load | `POST /api/recovery/v1/admin/reference-loads` | **Reference data C** | API-P4-005 | **S1:2962-2964**; **S5:323, 387**; **S3:222** |
| Approve | `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve` | **Reference data A** | API-P4-006 | **S1:3009-3011**; **S5:324, 398**; **S3:232** |
| Verify | `POST .../{loadId}/verify` | **Reference data U** | API-P4-009 | **S1:5035-5037**; **S5:327, 431** |
| Rollback | `POST .../{loadId}/rollback` | **Reference data U** | API-P4-010 | **S1:5078-5080**; **S5:328, 442** |
| Read list | `GET /api/recovery/v1/admin/lists/{listCode}` | **Reference data R** | API-P4-004 | **S5:322, 376** |

P4 applies **scope** on each ("scope applied" — **S5:387, 398, 431, 442**).

### Who holds the rights
RBAC matrix, **S5:226-269**: `RW-REFADM` = **CRUD** in Reference data; `RW-COE` = **CRUD**; `RW-RISK` = **RA**; `RW-LEGAL` = RU; `RW-DATASTEW`, `RW-COMPLY` = RU; `RW-SECADM` = R; everyone else R.
Note the contradiction: E1-043 says "Reference data A is held by no role… assumed RW-RISK" (**S3:181**; **S1:3020**), but S5:254 already gives RW-RISK **RA**.

Separation of duty: "The same person may not hold RW-REFADM and RW-RISK" — **S3:186**; DB check `approver_user_id <> author_user_id` — **S3:282**.

### Approve
- **Path** `{loadId}` uuid, **no body** — **S3:229**; **S5:395**.
- **200** `ReferenceLoad` with `status = APPROVED` — **S3:230**.
- Errors: 401; 403 no Reference data A (MSG-P4-002); 404 unknown load (MSG-P4-003); 409 approver is the author (MSG-P7-002) or version changed (MSG-GEN-004); 503 — **S3:231**.
- Side effects: status APPROVED, `approver_user_id`, `approved_at`; sets the replaced version's `valid_to` to the day **before** the new `valid_from` — **S3:46-47**; BR8 **S3:161**.
- Idempotency: "A second approval of an APPROVED version returns **200** with the same body" — **S3:233**. Contradicted by **S14:232** ("a repeat approve of an Approved load returns **409** and writes nothing").
- Additional approver-role parameters for some tables: `rwb.refload.approver.permission=RW-SECADM`, `...masking_rule=RW-COMPLY` (**S14:38**), `...delegation_limit=RW-RISK` (**S15:37**), `...partner_user=RW-SECADM` (**S22:5939**).

### Rollback
- **Path** `{loadId}`, body `RollbackRequest { reason: string }` — **S1:9906-9910**; **S5:439**.
- **200** `ReferenceLoad` with `status = ROLLED_BACK` — **S12:236**.
- Errors: 401; 403 no Reference data U; 404; **409 no earlier version (MSG-P3-015)**; **422 reason empty (MSG-GEN-001)**; 503 — **S12:237**.
- Idempotency: Idempotency-Key header; repeat returns the first result — **S12:239**.
- `reason` is required by prose but **not** marked required and has **no maxLength** in the schema (physical column `rollback_reason varchar(400)` — **S7:1866**).

### Verify
- Body `VerifyRequest { note: string }` — **S1:10015-10019**; note **required, max 1000** — **S20:246**.
- **200** `ReferenceLoad` with `verifiedBy`, `verifiedAt` (not in the schema).
- Errors: 401; 403 no Reference data U; 404; **422 empty note (MSG-GEN-001) or before valid_from (MSG-GEN-003)**; 503 — **S20:248**.

---

## 4. Complete LOV-REF-TABLE registry (25 codes)

Seeded in **S7:5989-6013**; identical list in **S4:376**; the column `reference_version.table_code` carries `lov_code = LOV-REF-TABLE` (**S7:5200**).

| # (sort_order) | Code | Label (EN) | Schema line |
|---:|---|---|---|
| 1 | `PRODUCT` | Product | S7:5989 |
| 2 | `REGION` | Region | S7:5990 |
| 3 | `EXPOSURE_BAND` | Exposure band | S7:5991 |
| 4 | `ROLE` | Role | S7:5992 |
| 5 | `TEAM` | Team | S7:5993 |
| 6 | `QUEUE` | Queue | S7:5994 |
| 7 | `QUEUE_MEMBER` | Queue member | S7:5995 |
| 8 | `SERVICE_LEVEL` | Service level | S7:5996 |
| 9 | `DOCUMENT_TYPE` | Document type | S7:5997 |
| 10 | `DOCUMENT_CHECKLIST` | Document checklist | S7:5998 |
| 11 | `RETENTION_CLASS` | Retention class | S7:5999 |
| 12 | `TEMPLATE` | Template | S7:6000 |
| 13 | `DELEGATION_LIMIT` | Delegation limit | S7:6001 |
| 14 | `PERMISSION` | Permission | S7:6002 |
| 15 | `MASKING_RULE` | Masking rule | S7:6003 |
| 16 | `PARTNER_USER` | Partner user | S7:6004 |
| 17 | `LEGAL_PERIOD` | Legal period | S7:6005 |
| 18 | `HOLIDAY` | Holiday | S7:6006 |
| 19 | `PRODUCT_PARAMETER` | Product parameter | S7:6007 |
| 20 | `PARAMETER` | Parameter | S7:6008 |
| 21 | `ENTRY` | Entry | S7:6009 |
| 22 | `EXCLUSION` | Exclusion | S7:6010 |
| 23 | `ALLOCATION` | Allocation | S7:6011 |
| 24 | `ASSIGNMENT` | Assignment | S7:6012 |
| 25 | `TRANSFER` | Transfer | S7:6013 |

**Exactly 25 rows.** All have `valid_from = DATE '2026-11-30'`.

Breakdown:
- **20 reference-data codes**: PRODUCT → PARAMETER (#1–20).
- **5 rule-table codes**: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER (#21–25). They also appear in `LOV-RULE-TABLE` (**S7:6014-6018**) and are loaded through `POST /admin/rule-versions`, not this endpoint (**S15:32, 40**; **S28/E1-029:209-214**).
- **13 codes served by E1-043** ("The list is data… PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, HOLIDAY and PRODUCT_PARAMETER" — **S3:154**; also **S3:34**, **S10:66**), i.e. #1–6, 8–13, 17–19.
- Added later: QUEUE_MEMBER (#7, E1-019 — **S10:263 CLAR-002**), PERMISSION + MASKING_RULE (#14–15, E1-037), PARTNER_USER (#16, Epic 2), DOCUMENT_CHECKLIST (#18 → #10, E1-040), RETENTION_CLASS (#11, E1-041), PARAMETER (#20, E1-042).

**`DOCUMENT_HUB_PARAMETER` is not in the list.** The YAML says the endpoint must "Accept the P5 table codes DOCUMENT_TYPE…, DOCUMENT_CHECKLIST…, RETENTION_CLASS… and **DOCUMENT_HUB_PARAMETER** (RWB-E1-024)" — **S1:2982-2983** — but no LOV row exists, no story assigns the code, and RWB-E1-024 never mentions it. See gap G2.

---

## 5. Code → handler → physical target

### Routing rule
"The caller chooses **one table code**, not a database table, not a column, and not a Java type." — **S9:37**.
"The server routes the code to the `ReferenceTableHandler` (P4) or `ReferenceTableLoader` (P5) registered for that code… **Adding a code to LOV-REF-TABLE does not by itself make it loadable: a code with no registered handler is refused.**" — **S9:41**.
"The caller **never** supplies a `{dbTable}.{dbColumn}` mapping… A user-supplied mapping would also be a SQL-injection and data-governance hole." — **S9:42**.
"`kind` (`BUSINESS`, `ENVIRONMENT`) and `value_type` (`INTEGER`, `STRING`, …) **do not choose a table**." — **S9:43**.

So: **table code only; no db table, no type, no column, no mapping.** Column names/types/keys per code live in `ReferenceTableSchemas`, "read from the parameter catalog (RWB-E1-042)" — **S3:273**; **S10:135**.

### Per-code map

| # | Code | Owner / handler | Physical target written | Read through / evidence |
|---:|---|---|---|---|
| 1 | `PRODUCT` | E1-043 generic registry (`ReferenceVersionRegistryImpl` + `ReferenceTableSchemas`) + `ProductCompletenessCheck` (E1-045) | `reference_version` + `reference_row` | "No new table. Reads `reference_version` and `reference_row`" — **S18:230**; check **S18:223, 238** |
| 2 | `REGION` | E1-043 generic registry; no named handler | `reference_version` + `reference_row` | **S3:44, 283**; **S10:81** |
| 3 | `EXPOSURE_BAND` | E1-043 generic registry | `reference_version` + `reference_row` | **S3:44, 81-91** |
| 4 | `ROLE` | E1-043 generic registry; read via `ReferenceDataService` | `reference_version` + `reference_row` (no applier to the `role` table is specified) | **S12:285**; `role` table exists separately (**S7:920-935**) |
| 5 | `TEAM` | E1-043 generic registry | `reference_version` + `reference_row` (no `team` table exists) | **S12:285**; **S3:138-141** |
| 6 | `QUEUE` | E1-043 registry + `QueueTableChecks` + `QueueVersionApplier` (E1-019) | `reference_row` first, then **`queue`** upsert on approval/valid-from (`table_version`) | **S12:44, 270-271, 279**; **S9:51** |
| 7 | `QUEUE_MEMBER` | Same as QUEUE | `reference_row` then **`queue_member`** | **S12:279-281**; **S9:51** |
| 8 | `SERVICE_LEVEL` | E1-043 registry + `ProductCompletenessCheck` | `reference_version` + `reference_row` | **S18:230** |
| 9 | `DOCUMENT_TYPE` | P5 `DocumentTypeLoader` (`ReferenceTableLoader`) | **`document_type`** (+ `reference_version_id` link, S7:1997) | **S13:43, 181-199, 226, 234** |
| 10 | `DOCUMENT_CHECKLIST` | P5 `ChecklistLoader` | **`document_checklist_item`** (+ `reference_version_id`, S7:2020) | **S16:226, 236** |
| 11 | `RETENTION_CLASS` | P5 `RetentionClassLoader` | **`retention_class`** — created by E1-041 migration, **not present in Physical Schema v4** | **S17:253, 258** |
| 12 | `TEMPLATE` | `TemplateLoadHandler` (`ReferenceLoadHandler`) | **`template`** | **S19:237, 242** |
| 13 | `DELEGATION_LIMIT` | `DelegationLimitLoader` | **`delegation_limit`** | **S15:44, 231, 237** |
| 14 | `PERMISSION` | `PermissionMatrixLoader` + `ReferenceLoadApprovalService` | **`permission`** | **S14:43, 252, 261** |
| 15 | `MASKING_RULE` | `MaskingRuleLoader` | **`masking_rule`** | **S14:253, 261** |
| 16 | `PARTNER_USER` | `PartnerUserLoader` (Epic 2) | **`partner_user`** | **S22:6106, 6130-6134**; **S9:111** |
| 17 | `LEGAL_PERIOD` | E1-043 generic registry | `reference_version` + `reference_row` (no `legal_period` table) | **S3:121-122**; no CREATE TABLE in S7 |
| 18 | `HOLIDAY` | E1-043 generic registry | `reference_version` + `reference_row` (no `holiday` table) | **S3:101, 114-117**; **S18:225** |
| 19 | `PRODUCT_PARAMETER` | E1-043 registry + `ProductCompletenessCheck` | `reference_version` + `reference_row` | **S18:230** |
| 20 | `PARAMETER` | `ParameterLoadHandler` + `ParameterLoadChecks` | **`parameter_value` directly**; `parameter_catalog` is **not** written by the load | **S8:240-241, 250**; **S9:50** |
| 21 | `ENTRY` | **No reference handler.** Rule path: `RuleVersionService` via `POST /admin/rule-versions` | **`rule_row` + `rule_version`** | **S15:32, 40**; E1-029 **S11:279** |
| 22 | `EXCLUSION` | Same as ENTRY | `rule_row` + `rule_version` | **S15:32** |
| 23 | `ALLOCATION` | Same as ENTRY | `rule_row` + `rule_version` | **S15:32** |
| 24 | `ASSIGNMENT` | Same as ENTRY | `rule_row` + `rule_version` | **S15:32** |
| 25 | `TRANSFER` | Same as ENTRY | `rule_row` + `rule_version` | **S15:32** |

Two persistence models coexist:
- E1-043: "P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`"; "The P4 handler writes nothing itself" — **S3:42**, **S11:2419**.
- Per-code handlers: "The handler validates the rows and **writes its own target**" — **S9:41, 47-52**.

The reconciliation table is **S9:47-52**: most E1-043 tables → `reference_version` + `reference_row`; `PARAMETER` → `parameter_value`; `QUEUE`/`QUEUE_MEMBER` → `reference_row` then applier; P5 codes → their own tables.

---

## 6. PARAMETER — exact CSV and column mapping

### Columns
Story contract: "**file (rows of key, environment, value)**, table = "PARAMETER", validFrom" — **S8:205**.
Clarification: "The contract in E1-042 §12 is `file` with rows of `key`, `environment`, `value`" — **S9:58**.

```csv
key,environment,value
case.entry.dpd,PROD,91
refdata.cache.ttl-seconds,PROD,300
```
— **S9:60-64**

| Item | Value | Evidence |
|---|---|---|
| Header names | `key`, `environment`, `value` (lowercase) | S9:61 |
| Order | key → environment → value | S9:61-64 |
| Separator | comma (shown by example) | S9:61-64 |
| Header row | shown present; no formal "header required" rule stated | S9:61 |
| Encoding | **NOT STATED** | — |
| File type | CSV in the example; generic endpoint allows CSV or XLSX one sheet | S9:88; S3:219 |
| Max rows | **NOT STATED** | — |
| Max file size | **NOT STATED** (no 413 on the endpoint) | S1:2985-3001 |
| Quoting/escaping, blank lines, BOM | **NOT STATED** | — |

### Mapping to `parameter_value`

| CSV column | Target column | Check / behaviour | Evidence |
|---|---|---|---|
| `key` | `parameter_value.param_key` (FK to `parameter_catalog.param_key`) | Must exist in the catalog; **unknown key refuses the whole load, MSG-P1-002** | S9:72 |
| `environment` | `parameter_value.environment` | `DEV`, `SIT`, `UAT`, `PROD`; must be one the catalog line lists in `environments` | S9:73; LOV-ENVIRONMENT **S4:369** |
| `value` | `parameter_value.param_value` | Parsed as catalog `value_type`; must fall in `min_value`..`max_value` inclusive. Wrong type = **MSG-P1-002**; out of range = **MSG-GEN-002** | S9:74 |
| — | `parameter_value.product_group` | **NULL.** "`PARAMETER` is global; product-scoped values are `PRODUCT_PARAMETER` (E1-045), not this code." | S9:75 |
| — | `parameter_value.version_no` | **Next number for the key and environment**; the seed is version 1 | S9:76 |
| — | `parameter_value.valid_from` | **The request `validFrom`** | S9:77 |
| — | `parameter_value.status` | **`VALIDATED` on load; `APPROVED` after the approve call** | S9:78 |
| — | `parameter_value.author_user_id` | **The signed-in loader** | S9:79 |
| — | `parameter_value.approver_user_id`, `approved_at` | **Set only by the approve call**; approver must differ from author | S9:80 |

**`valid_to`:** not in the mapping table. Derived from BR8 — approving a successor sets the replaced version's `valid_to` to the day before the new `valid_from` (**S3:161**); on a new row it is NULL (**S7:1835**).

Physical columns: **S7:1827-1848** (`param_key`, `environment`, `param_value`, `product_group`, `version_no`, `valid_from`, `valid_to`, `status`, `author_user_id`, `approver_user_id`, `approved_at`). TSD data dictionary: **S4:283-298**.

### Other PARAMETER rules
- The **catalog** (type, range, default, owner) is not in this file. "It comes from `config/parameter-catalog.csv` through the reviewed pull request and the generated migration. **A runtime upload cannot add a key.**" — **S9:93**.
- "A new parameter is a pull request and a release; a new value is a load and an approval." — **S9:133**.
- Approve/rollback are the shared endpoints — **S8:211**; rollback with no earlier version → **409 MSG-P3-015**; approver = author → **409 MSG-P7-002**.
- Approve changes no value until the valid-from date — **S11:2385**.

---

## 7. CSV templates for other codes

**Caveat that governs the whole table:** "There is **no single CSV schema for all codes**, and there is **no consolidated template register in this pack yet (OI-E1-042-005)**. The owning story defines the header; the handler enforces it… the exact **header order and names** come from the handler's `ReferenceTableSchemas` entry." — **S9:97**; open item **S9:185**. So a "column set" is not the same as a defined template.

| Code | CSV columns (as stated) | Target `{table}.{column}` | Template status | Owning story |
|---|---|---|---|---|
| `PRODUCT` | `product_code`, `product_name`, `definition`, `owner_role`, `system_of_record`, `refresh_cycle`, `expected_by`, `owner_user_id` | Build notes say `data_product.*`; **E1-045 says `reference_row`** | **PARTIAL / CONFLICT** — column set from E1-001 §13 but target disputed; header order not fixed | E1-001 §13 (S9:101); E1-045 (S18:230) |
| `PRODUCT_PARAMETER` | Implied only: product group, parameter code, value, unit (from `ProductParameter` record) | `reference_row.row_data` keys `product_group`, `parameter_code`, `value`, `unit` | **NOT DEFINED** | **RWB-E1-045** (S18:185-209, 230) |
| `SERVICE_LEVEL` | Implied only: product group, case status, limit, unit, warn percent, escalate-to role | `reference_row.row_data` | **NOT DEFINED** | **RWB-E1-045** (S18:208-209) |
| `QUEUE` | "Header not listed in E1-019. The checks name team, role, method, capacity cap, overflow queue and member role." | `queue` (`queue_code`, `queue_name`, `team_code`, `role_code`, `assignment_method`, `capacity_cap`, `overflow_queue_id`) | **NOT DEFINED** | **RWB-E1-019** (S9:115; S12:270) |
| `QUEUE_MEMBER` | "Header not listed in E1-019. The checks name queue, user, capacity, skill codes and the member's role on the queue." | `queue_member` (`queue_id`, `user_id`, `capacity`, `skill_codes`) | **NOT DEFINED** | **RWB-E1-019** (S9:116; S12:270) |
| `PERMISSION` | `role_code`, `capability_area`, `letters`, `matrix_version` | `permission.role_id`, `.capability_area`, `.letters`, `.matrix_version` | **PARTIAL** — column set only; note CSV `role_code` must resolve to `permission.role_id` (uuid) | **RWB-E1-037** (S9:113; S14:261) |
| `MASKING_RULE` | `role_code`, `field_id`, `unmasked`, `masking_version` | `masking_rule.role_code`, `.field_id`, `.unmasked`, `.masking_version` | **PARTIAL** | **RWB-E1-037** (S9:114; S14:261) |
| `DOCUMENT_TYPE` | `doc_type_code`, `label_en`, `label_th`, `write_once`, `retention_class`, `field_definitions`, `legal_signoff_by`, `legal_signoff_date`, `npa_signoff_by`, `npa_signoff_date` | `document_type.doc_type_code`, `.label_en`, `.label_th`, `.write_once`, `.retention_class`, `.field_definitions`, `.legal_signoff_by`, `.legal_signoff_date`, `.npa_signoff_by`, `.npa_signoff_date` (+ `table_version`, `valid_from`) | **PARTIAL** — "the Excel template" is named but not published | **RWB-E1-025** (S9:106; S13:181-199, 234) |
| `DOCUMENT_CHECKLIST` | Implied: stage, route, document type, required, sort order | `document_checklist_item.stage_code`, `.route_code`, `.document_type`, `.required`, `.sort_order`, `.table_version`, `.valid_from` | **NOT DEFINED** header | **RWB-E1-040** (S16:226, 236) |
| `RETENTION_CLASS` | `class_code`, `period_months`, `end_action` | `retention_class.class_code`, `.period_months`, `.end_action` | **PARTIAL** | **RWB-E1-041** (S9:107; S17:258) |
| `TEMPLATE` | `template_code`, `language`, `product_group`, `channel`, `notice_type`, `signature_basis`, `body_ref`, `merge_codes`, `approver`, `approval_date` | `template.template_code`, `.language`, `.product_group`, `.channel`, `.notice_type`, `.signature_basis`, `.body_ref`, `.merge_codes`, `.approved_by`, `.approved_at` (+ `template_version`) | **PARTIAL** — note `approver`→`approved_by`, `approval_date`→`approved_at` | **RWB-E1-046** (S9:108; S19:242, 2581-of-S11) |
| `MERGE_FIELD` | `merge_code`, `source_entity`, `source_field`, `field_id`, `is_required`, `personal_data`, `catalog_version`, `valid_from` | `merge_field.*` | **PARTIAL** — field list from E1-046 §11, no CSV header | **RWB-E1-046** (S19:178-186) |
| `DELEGATION_LIMIT` | No column list; "one matrix row and decision code per load row" | `delegation_limit.decision_code`, `.approval_level`, `.product_group`, `.principal_limit`, `.loss_pct_limit`, `.min_price_pct_fmv`, `.holder_user_id`, `.substitute_user_id`, `.limit_version`, `.regulation_item`, `.applies_when`, `.max_loss_amount`, `.max_delay_count`, `.min_price_pct_principal`, `.min_received_pct`, `.max_term_years` | **NOT DEFINED** | **RWB-E1-038** (S15:198, 237) |
| `PARTNER_USER` | `partner_identity`, `partner_id`, `role`, `valid_from`, `valid_to` | `partner_user.identity_ref`, `.partner_id`, `.role_code`, `.valid_from`, `.valid_to` | **PARTIAL** — `partner_identity`→`identity_ref`, `role`→`role_code` | **Epic 2, partner-user story** (S9:111; S22:6134) |
| `PAYMENT_MATCH_RULE` | `rule_code`, `priority`, `match_type`, `amount_tolerance`, `window_days_before`, `window_days_after`, `partial_floor`, `rule_version` | `payment_match_rule.*` | **PARTIAL** | **Epic 2** (S9:112; S22:8480) |
| `MEASURE_DEFINITION` | `measure_code`, `name`, `formula`, `data_product`, `unit`, `definition_version`, `approver`, `approval_date` | `measure_definition.*` | **PARTIAL** | **RWB-E1-013** (S9:109) |
| `SYS_FIELDS` | `field_id`, `owner_role`, `refresh_cycle`, `late_behavior`, `interface_id` | `sys_fields.field_id`, `.owner_role`, `.refresh_cycle`, `.late_behavior`, `.interface_id` | **PARTIAL** | **RWB-E1-064** (S9:110) |
| `DATA_PRODUCT_ACCESS` | `product_code`, `role_code`, `can_read`, `access_version`, `valid_from`, `valid_to` | `data_product_access.*` | **PARTIAL** | **RWB-E1-016** (S9:105) |
| `TRACKER_INVENTORY` | `tracker_code`, `team_code`, `tracker_name`, `location_type`, `location_ref`, `owner_user_id`, `field_list`, `update_cycle`, `target_product`, `decision`, `decision_reason` | `tracker_inventory.*` | **PARTIAL** | **RWB-E1-005** (S9:102) |
| `DQ_RULE` | `rule_code`, `rule_version`, `rule_name`, `product_code`, `target_entity`, `rule_type`, `rule_params`, `valid_from`, `valid_to`, `approved_by`, `test_case_id` | `dq_rule.*` | **PARTIAL** | **RWB-E1-006** (S9:103) |
| `RETENTION_RULE` | `product_code`, `table_name`, `record_class`, `retention_months`, `age_basis_field`, `rule_version`, `valid_from`, `valid_to`, `approved_by` | `retention_rule.*` | **PARTIAL** | **RWB-E1-017** (S9:104) |
| `DATA_PRODUCT` | `product_code`, `product_name`, `definition`, `owner_role`, `system_of_record`, `refresh_cycle`, `expected_by`, `owner_user_id` | `data_product.*` | **PARTIAL** | **RWB-E1-001** (S21:263-270; S9:101) |

**Not defined anywhere:** a `PRODUCT_PARAMETER` template (E1-045), a `SERVICE_LEVEL` template (E1-045), `QUEUE`/`QUEUE_MEMBER` headers (E1-019), a `DELEGATION_LIMIT` header (E1-038), a `DOCUMENT_CHECKLIST` header (E1-040), a `MERGE_FIELD` header (E1-046), and a `MASKING_RULE`/`PERMISSION` header order (E1-037).

---

## 8. Adding a new table code vs adding a value row

### Adding a value row (existing code)
- A validated, approved, dated load — no code release. "Load | The new version loads into production with its valid from date. **No code release**" — reference-data change process, **06 Data reference-data CSV `change-process.csv` line 8** (`...\13 AI-First SDLC repository\requirement\legacy\06-data\_csv\recovery-workbench-reference-data-and-lists-of-values-v3\change-process.csv`).
- Version is immutable: "A version is never changed after it is written" — **S3:155**; a correction is a new version — **S3:342**.

### Adding a new table code (new `LOV-REF-TABLE` value)
Requires **all** of:
1. **A row in `lov_value`** (`lov_code = 'LOV-REF-TABLE'`, unique `(lov_code, value_code)` — **S7:916**). "The list is data and changes by a load of LOV-REF-TABLE" — **S3:154**; "LOV-REF-TABLE values and the column definitions per table code, loaded by the reference data administrator" — **S3:286**.
2. **A registered handler** — "Adding a code to `LOV-REF-TABLE` does not by itself make it loadable: **a code with no registered handler is refused**" — **S9:41**.
3. **A `ReferenceTableSchemas` entry** (column names, types, key columns) — **S3:273, 291**; **S10:135**.
4. **A new target table** if the handler writes its own (P5 pattern) — **S9:47-52**; migrations in `V<seq>__<story>_<name>.sql` — **AGENTS.md §2**.
5. **A release** (new Java class, wiring, feature flag) — **S9:118**; **S13:250** (`rwb.dochub.doctypes` off → code refused).

**Therefore: adding a LOV row alone is not sufficient; adding a handler without the LOV row fails the table-code check; both are needed, and both are code/data changes, not a self-service load.**

### The analogous rule for parameters (often confused with the above)
| | Catalog file | Value file |
|---|---|---|
| Path | `config/parameter-catalog.csv` in the repo | uploaded to `POST /admin/reference-loads` |
| Changed by | squad member via reviewed PR | RW-COE via checked, approved load |
| Can it add a key? | **Yes** | **No** — unknown key refuses the whole load, MSG-P1-002 |

— **S9:124-133**.

### Loose end
`LOV-REF-TABLE` itself is changed by "a load", but the API spec exposes only `GET /admin/lists/{listCode}` (**S1:2923-2953**) — there is **no `POST /admin/lists/{listCode}`** and no list-load endpoint. So the mechanism for adding a LOV value is **not defined at API level**. See gap G11.

---

## 9. Contradictions and gaps to resolve before build

| # | Gap | Facts | Impact |
|---|---|---|---|
| **G1** | **25 vs 13 codes** | S3:154 and S10:66 say 13; S7:5989-6013 and S4:376 say 25 | Validation must accept 25, not 13. E1-043's "13" is its first-release subset |
| **G2** | **`DOCUMENT_HUB_PARAMETER`** | S1:2982-2983 says accepted; no LOV row (S7:5989-6013), no handler story, E1-024 never names it | Either add the LOV row + loader, or remove it from the YAML |
| **G3** | **Case mismatch** | LOV codes are UPPERCASE; stories send lowercase `template`, `permission`, `masking_rule`, `delegation_limit`, `partner_user`, `data_product`, `merge_field`, `payment_match_rule` (**S19:198**, **S14:218**, **S15:198**, **S22:6106**, **S21:270**) | No normalisation rule is stated. Decide: case-insensitive match or strict uppercase with a 422 |
| **G4** | **Codes used but absent from LOV** | `data_product` (S21:270), `tracker_inventory` (S11:180), `dq_rule` (S11:2052), `retention_rule` (S15:5486), `data_product_access` (S21:5159), `sys_fields` (S11:3553), `measure_definition` (S11:741), `merge_field` (S19:198), `payment_match_rule` (S22:8480) | Under the strict rule "must be a LOV-REF-TABLE code" (**S3:222**, **S11:2413**) every one of these loads fails. Registry and stories are out of sync |
| **G5** | **Repeat-load status** | 201 only (S1:2985); "existing load returned, no status" (S3:58, 223); 409 elsewhere (S21:270, S11:180, S13:189, S22:8485) | Pick 201-with-same-body (canonical) or 200; do not return 409 for an identical file |
| **G6** | **Status vocabulary** | `VALIDATED` (S3:220, S7:1858); `LOADED`/`Loaded` (S13:87, S14:43, S15:44); `LOV-VERSION-STATUS` has VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED — **no LOADED** (S7:5983-5986) | Use `VALIDATED`; treat `LOADED` in P5/E1-037 as a wording defect |
| **G7** | **Approve idempotency** | 200 with same body (S3:233) vs 409 (S14:232) | E1-043 owns the endpoint; 200 is canonical |
| **G8** | **Schema drift** | `ReferenceLoad` lacks `changeRequestRef`, `impactSummary`, `rollbackPlan`, `testResult`, `verifiedBy`, `verifiedAt` (S1:8812-8826) despite S1:2980-2982 and S20:190 | Generate the type from a corrected schema, or accept undocumented fields |
| **G9** | **`id` vs `loadId`** | `ReferenceLoad.id` (S1:8815) vs path `{loadId}` (S1:3014); `reference_version` has both `id` and `load_id` (S7:1852, 1864) | Define `id` = `load_id`; otherwise approve cannot resolve the version |
| **G10** | **`reference_row` uniqueness** | Schema `UNIQUE (row_key)` (S7:1897) vs story `UNIQUE (version_id, row_key)` (S3:283, S10:81) | Schema v4 as written prevents two versions of a table sharing a key. E1-043's migration must correct it |
| **G11** | **No list-load endpoint** | Only `GET /admin/lists/{listCode}` (S1:2923); BR1 says the list changes "by a load of LOV-REF-TABLE" (S3:154) | Mechanism undefined; P4 owns the gap |
| **G12** | **`validFrom` untyped** | `type: string`, no `format: date` (S1:2978-2979); `table` has no enum/`x-list-of-values` | Validators will not enforce date or code. Add `format: date` and `x-list-of-values: LOV-REF-TABLE` |
| **G13** | **PARAMETER has no load header** | `parameter_value` has **no `load_id`** (S7:1827-1848); approve path is `{loadId}` (S3:229) | Either write a `reference_version` header for every PARAMETER load, or add `load_id` to `parameter_value`. Not stated |
| **G14** | **Nullable unique key** | `UNIQUE (param_key, environment, product_group, version_no)` includes nullable `product_group` (S7:1847); PARAMETER sets it NULL (S9:75) | In PostgreSQL NULLs are distinct by default → duplicate versions possible. Use `NULLS NOT DISTINCT` or a partial index |
| **G15** | **`version_label` missing from E1-043 migration** | Physical schema has `version_label varchar(20)` (S7:1855); E1-043's DDL omits it (S3:282); E1-038 loads `DOA-2026.11` (**S15:43**) | Define where the label is stored/parsed (file column) |
| **G16** | **Approver rights** | "no role holds A" (S3:181, S1:3020) vs RBAC `RW-RISK = RA`, `RW-COE = CRUD` (S5:254-255) | The matrix supersedes the assumption |
| **G17** | **`PRODUCT` target** | S9:101 maps to `data_product`; S18:230 says `reference_row`; the physical `data_product` is the 14-data-product catalog (S7:980) | Two different concepts conflated; E1-045 owns `PRODUCT` and says `reference_row` |
| **G18** | **P3/P5 TSD silence** | P3 TSD mentions the feature only at S4:283/305/376 — no endpoint section; P5 TSD has **zero** matches for reference-load/ReferenceTableLoader | The endpoint is documented only in P4's TSD and the stories |
| **G19** | **`RETENTION_CLASS` table absent from schema v4** | Created by E1-041's migration (S17:258), not in S7's 108 `CREATE TABLE` statements | Baseline schema and story migrations are out of step |
| **G20** | **`rollbackReason`/`note` untyped** | `RollbackRequest.reason` and `VerifyRequest.note` have no `required`/`maxLength` (S1:9906-9919, 10015-10019) despite prose (S12:235, S20:246) | Add constraints |

---

## 10. Line-number index for the key facts

| Fact | Evidence |
|---|---|
| Endpoint, capability, right C | S1:2955-2965 |
| Multipart fields only, no `required` array, `validFrom` untyped | S1:2966-2979 |
| Forward-looking description (checklist fields, P5 codes, 409/422) | S1:2980-2984 |
| Declared status codes 201/401/403/409/422/503 | S1:2985-3001 |
| Approve endpoint, right A, 200 | S1:3002-3038 |
| Verify/rollback endpoints, right U | S1:5028-5113 |
| `ReferenceLoad` schema (5 fields) | S1:8812-8826 |
| `Problem` schema | S1:8971-8989 |
| `RollbackRequest` / `VerifyRequest` | S1:9906-9910 / S1:10015-10019 |
| Error component texts | S1:6086-6141 |
| Global Idempotency-Key rule | S2:42 |
| Story contract: request/response/errors/auth/idempotency | S3:215-223 |
| Story approve contract | S3:225-233 |
| One table code per load | S3:41; S11:2413; S9:39-40 |
| 13 served codes | S3:154; S10:66 |
| Content hash = SHA-256 sorted rows | S11:2425; S3:282 |
| Valid-from not before business date; equal allowed | S3:159; S11:2425; S10:265 |
| Duplicate validFrom → 409; same hash → existing | S3:221; S10:266 |
| Status VALIDATED / APPROVED / ROLLED_BACK | S3:170-173; S3:166 |
| DB constraints reference_version/reference_row | S3:282-284; S7:1851-1898 |
| P4 endpoint inventory and detail | S5:317-443 |
| P4 RBAC matrix | S5:226-269 |
| parameter_value columns and LOVs | S4:283-298; S7:1827-1848 |
| LOV-REF-TABLE 25 values | S7:5989-6013; S4:376 |
| `table_code` constrained to LOV-REF-TABLE | S7:5200 |
| PARAMETER contract | S8:201-211 |
| PARAMETER CSV and column mapping | S9:56-93 |
| Routing rule / no user mapping / handler registration | S9:33-54 |
| Other code column sets / OI-E1-042-005 | S9:95-118, 185 |
| Build-time vs run-time CSV | S9:120-141 |
| E1-043 CLARs (13 codes, boundary date, duplicate content) | S10:258-269 |
| E1-043 load checks | S10:162-173 |
| QUEUE/QUEUE_MEMBER contract and applier | S12:213-239, 279-281 |
| DOCUMENT_TYPE contract and table | S13:181-199, 234-235 |
| PERMISSION/MASKING_RULE contract and tables | S14:218-232, 261 |
| DELEGATION_LIMIT contract and table | S15:198-202, 237 |
| DOCUMENT_CHECKLIST table | S16:236 |
| RETENTION_CLASS table | S17:258 |
| PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL contract; "No new table" | S18:185-193, 230 |
| TEMPLATE/MERGE_FIELD contract and table | S19:198-207, 242 |
| Change checklist fields and verify | S20:181-190 |
| `data_product` handler and load | S21:263-270 |
| PARTNER_USER load and table | S22:6106, 6134 |

No files were modified.

<details><summary>Reasoning</summary>

Good.

Now, let me think about whether the "response schema" includes HTTP 200 for GET lists. Not needed.

One more nuance: The `ReferenceLoad` schema has no `version`, `contentHash`, `author`, `approver`, `rowErrors`. But E1-019 says response 201 ReferenceLoad: id, table, validFrom, status, rows. Consistent. E1-048 says approve response 200 ReferenceLoad with verifiedBy/verifiedAt for verify. So schema drift.

Now write the report. I need to be precise with quotes and line numbers. I'll use file paths relative to workspace root plus line numbers, and provide absolute paths at least once (guideline: return absolute paths). I'll use a "Sources" key with short codes and full absolute paths, then cite short code + line.

Let me structure:

- Header: scope, sources table (S1..S10 with absolute paths).
- Bottom line (10 bullet answers).
- 1. Request contract
- 2. Response/status
- 3. Auth
- 4. LOV-REF-TABLE (25)
- 5. Registry map (25 rows)
- 6. PARAMETER
- 7. Other templates
- 8. Add code vs add value
- 9. Contradictions/gaps
- 10. Source line index

Need to keep it manageable but thorough. The user asked for a structured report, so length is fine.

Let me draft the code→handler→target table table with columns: # | Code | Sort | Owning story/handler | Writes | Reads through | Evidence.

For generic codes: "E1-043 generic registry (ReferenceVersionRegistryImpl; ReferenceTableSchemas entry)" → reference_version + reference_row → ReferenceDataService.

For PRODUCT also ProductCompletenessCheck (E1-045). For SERVICE_LEVEL, PRODUCT_PARAMETER same.

QUEUE/QUEUE_MEMBER: ReferenceVersionRegistry + QueueTableChecks; writes reference_version/reference_row, then QueueVersionApplier upserts queue/queue_member with table_version. Evidence: E1-019 279-281; INC-003 51.

DOCUMENT_TYPE: DocumentTypeLoader (P5) → document_type (+ reference_version? doc_type has reference_version_id). State: writes document_type, and the schema carries reference_version_id; whether a reference_version header row is written is not stated by E1-025. Hmm. E1-025 interface validateAndStage(loadId, tableVersion, ...) — implies a load record. But no reference_version write stated. The `reference_version_id` column exists for linking. I'll note "document_type, with reference_version_id linking to the load header (schema line 1997); E1-025 does not state the header write explicitly".

Similar for checklist and document_hub_parameter (reference_version_id columns).

RETENTION_CLASS: retention_class table 

_[truncated]_

</details>
