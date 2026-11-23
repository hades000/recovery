# btw: give me all scehmas related to it

- **Session ID:** `ses_e1cb2e54fffeVTP3dk1seF500X`
- **Created:** 2026-11-16 14:40  |  **Last activity:** 2026-11-16 15:00
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `plan`
- **Tokens:** 25,072 in / 9,602 out / 18,025 reasoning
- **Messages:** 81

---

### User - 2026-11-16 13:06

tell me about user story t001 t002 t003 t011 i need to explain to the peopple who are developing this

### Assistant - 2026-11-16 13:06 | opencode-go/deepseek-v4.1-flash | build

I'll pull up the project knowledge to find those user stories.

**Tool `execute`** - completed

```json
{"code": "const r = await tools.openchamber_knowledge({ action: \"knowledge.list\", parameters: {} });\nconsole.log(r);\n"}
```

```text
null

Logs:
{"schemaVersion":1,"ok":true,"action":"knowledge.list","data":{"projectId":"path_QzovVXNlcnMvU2FoaWxNb3JlL0Rvd25sb2Fkcy9SZWNvdmVyeSBXb3JrYmVuY2ggU2hhcmVQb2ludCBTZXQgdjE0","notes":[],"todos":[],"plans":[]}}
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

Knowledge panel is empty. Let me search the project files for those story IDs.

<details><summary>Reasoning</summary>

No knowledge. Let's look at the working directory — likely there are docs with user stories T001 etc.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Force | Select-Object Mode, Length, Name | Format-Table -AutoSize"}
```

```text

Mode   Length  Name                                                          
----   ------  ----                                                          
d-----         .freebuff                                                     
d-----         01 Decisions and governance                                   
d-----         02 Business architecture and process                          
d-----         03 Requirements and specifications                            
d-----         04 User stories                                               
d-----         05 Technical architecture                                     
d-----         06 Data                                                       
d-----         07 Screens and experience                                     
d-----         08 AI and agents                                              
d-----         09 Testing and quality                                        
d-----         10 Policy, controls and compliance                            
d-----         11 Delivery and operations                                    
d-----         12 Project communication                                      
d-----         13 AI-First SDLC repository                                   
d-----         14 Story Updates                                              
d-----         15 ACE DB Alignment                                           
d-----         16 Temporal and Drools Adoption                               
d-----         17 AI-First SDLC Repository v2                                
d-----         ACE schema                                                    
d-----         aisdlc-playbook-main                                          
d-----         aisdlc-toolkit-main                                           
d-----         E1-042 Migration and Clarifications                           
d-----         _work                                                         
-a-h-- 109     .~lock.Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx#
-a---- 7301630 13 AI-First SDLC repository.zip                               
-a---- 855292  recovery-architecture.pptx                                    
-a---- 35964   Recovery_Workbench_Epic1_Grooming_Order_All_TE_v2.xlsx        
-a---- 39267   Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx        



```

**Tool `grep`** - completed

```json
{"pattern": "T00[123]|T011", "limit": 60}
```

```text
Found 44 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 216: <script type="application/octet-stream" id="payload">H4sIAG3S52oC/+y9e28cV5Yn+FUC9h9lA8lc8SHZltBYUCRlq5t6FElbXTMaEMHMIBmlzIisiEhRLElA2WXArurqmVm0bLfs2uqRDcPT9goou1xd8rfRR9nzvPfciMjMoFzdOwtMPyxmPM69cR/nnufv3H9pmA/Kly7+5/svHeajYVK8dPGlc69Fu4MiSbIyirNhlNybJEWaZIPkpd5Lh+kogUd2kkF+NylOo1t5cecA7h1H64NBUpbpQTpKq9Not4JX42IY3V3pQwv34NUsHp/1VXgruVfBS0IizX6ZTuAn/Fkm0u1j+L2XT+DS6KWLy72XqtY2bmdhI6U0cjvb3bgcbeSjUTKo0lw+Wd/vR28l2Z04erPIp5NetPJ6dGNQ5QdJEa2cW7lwO7taJePoQbSZVHE6up1t5oPpOMkquNTylfGMDryTFCW0DC8tA4m4SuCvRks3i2QSF8kwOjiF26ZX8AFVMR1U0wLfu7Wx/ma00l+JRsndZBStr7/0sMdDtNyP9o4Tvh6M1Va9m/D90FSVQduTvKjiUVTSaojGSVKVzSaY8DAp06MsKk9LHJNBPp7kGQxFSW9FaYUdH8D4Umfhcy9FSQytCem0jAbHyeAOfmBymMO3FMkoicuk7z5gpR/tTEdJGVXHcRXBYh3lJ9FhkY+BePBB60US4wzAwzIit7ONPKuKuMSZ2YMVFa31z0dVHi1H8VGcQqeARhkdxIM7RzCm2fBSNIqLoySq8FkckAG+n4/KaJVeCz65yu/gVqHvrI7hS2Ai+2v91R79s7yMrY/yAi7Dyq6mZVQe5ycZjocjfxAPj5JelMGIFjxQ+EI8giEUakDl75LTgxz3xYOI5yymgYSRgoGMD+BrkdS0pD+ByB15vhelWRRHo/woHcBk5gXs8l50klbHUZZHMCwTXHD95f5yj/5ZwX+g/7ezK7Ce8XPWo7spLFwguxJN7sHY4+UizY4iaD6hvsgAXZKb/CXH6XAIk3uQHKfQs7JKB3dOo+Mkhg6U1OZa/zVuDEdpD4e8isr0l/jRGyN4OqroGmzKKsLlUEUra/hp8F/oB1I433/9drYdHySj0o3LYZqMhtFxDK+5jo/wkahKYYHBBKbVJRi2X0xT3FH0OMxfXODyg7GiacFhX8UhWYV/Vm5nW0WRU6/lD+Rm/ukM/wOEK1gW3DzORTkdA1X4niF+AN6r8okO0Rj4Q6nv8JO4tVd9qzADb8FgwThjuzdgLchuqdJqlFyCXZrhZ0/LhAaVnoMO0QT7/uPwXsDRPcDNg7wDxz8aJKORfvSlqMSNjuMEK286Ji6YwUYYJNi7tEBuVSVKE7hUCmuTenXFfEuaydcM6TYNQZEAZwJ6sFAGo7yEXm+Vg3iS8C9dBfCle+kYFxRsEmSSOX7kOMmnVXQS4/vVSR7BA9MK3hEOgeRHuDiwSRiEAk6qKsmGRHMFu/mf8hzZ89u8JWAKVs6di+AwGyCP/iXeRBpwfXXlHC6ok3QImwJ3BjYMHdS9vCZ7+RyutexoGh/hYNzEf0b6u0xgUe0dxymvCFlOePtvgChO7DJP7DIuJ2EFY/hYeBnb2cthfZfCDrIMt4hOAq1ZmfvCbR/oDw7cZhEfHfHQXc+VJ2RJAkt66G/hTnkN19NoQmsA/sG1i0sPFnI0GcUw1243S1vY6RVcPOtTeDKD/RtXfFLtAuNbIgLAL4+Ooy1kr9HVTcdWBvlRllbpXeShxHZxQb/umPkqnKzAvtuPgICbb+A15OPH1KFbxzl1Jx/DgoQdNohhwR/Wu818YDIdjWibYw/o1AA+meFox/7Rm+kkGaWwt17ZuXV5aW9r6dzyuVcNsz2JR3eW9DMfRJd57e1e3YPVluKH/XQ9SjIY5SQpYFrtJPH3YPdwnMdw0EizpSfEDKOADsqBR19jhqXWwH/SVZvFwIdOZMku7Ne6kqP5wTGbwA8...
  Line 343: <script type="application/octet-stream" id="f126">H4sIAGzS52oA/328A3Ql3dY1fGLbTjrp2Lbtjm3btq2Obdu2jY5tJx07+ft57/jH/W5/7/3OGVX77DP2mrXXqJpz7VqjVslLgYCiAgAASIAnkr52cgPJbuqfXt+fDfHPZmRrKO9ga+dIp29nR+tmbSUSXQffT4gq4toTUNuiBGEI2xgoiod3DwLZ2Tx4iw9ksdaTIoJ3zTHWVq/5PriF+JNYyUuTLRMIux4eYignVsp5h9o4WkUuKPcZOtz1UnSLGCxsVcCgyE/ihuHY
... truncated (76,119 chars total)
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

Let me look in the user stories folder directly.

<details><summary>Reasoning</summary>

The grep was noisy. Let's look at "04 User stories" folder.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File \"04 User stories\" | Select-Object FullName, Length | Format-Table -AutoSize -Wrap"}
```

```text
tories     
Epic 1 Story Files v5\RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md                            
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 058 Agent platform set up E1a v1.md                                                       
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 059 Case intake agent in shadow E1b v1.md                                                 
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 060 Extraction evaluation E1c v1.md                                                       
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md                                     
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 062 Deviation screening agent in shadow E2b v1.md                                         
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 063 Agent monitoring dashboard v1 E2c v1.md                                               
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 064 Data dictionary for the 14 data products v1.md                                        
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 065 Sandbox database with synthetic recovery data v1.md                                   
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 066 Interaction ledger store and writer v1.md                                             
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories     
Epic 1 Story Files v5\RWB E1 067 Every Workbench action into the in
... truncated (51,376 chars total)
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let's look at the newest version folders - v7 seems latest. Let's read TE 001, TE 002, TE 003, TE 011 from v7. Also there might be "14 Story Updates" and "E1-042 Migration..." with updated versions. Let's check if there are v8 folders or updated story versions. Let me check the folder listing at top level of "04 User stories".

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Directory \"04 User stories\\Recovery Workbench User Stories\" | Select-Object Name, LastWriteTime | Format-Table -AutoSize"}
```

```text
Get-ChildItem : Cannot find path 'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User 
stories\Recovery Workbench User Stories' because it does not exist.
At line:1 char:1
+ Get-ChildItem -Directory "04 User stories\Recovery Workbench User Sto ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:\Users\SahilM...ch User Stories:String) [Get-ChildItem], ItemNotFound 
   Exception
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
 

Exited with code 1
```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File -Filter \"*TE 00*\" \"14 Story Updates\",\"E1-042 Migration and Clarifications\",\"_work\" -ErrorAction SilentlyContinue | Select-Object FullName | Format-Table -AutoSize -Wrap"}
```

```text

FullName                                                                                                               
--------                                                                                                               
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\td\e2v4\RWB TE 009 Performance test harness   
v1.md                                                                                                                  



```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Path with space issue? Let me list top-level "04 User stories".

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Directory \"04 User stories\" | Select-Object Name, LastWriteTime | Format-Table -AutoSize"}
```

```text

Name                                                  LastWriteTime      
----                                                  -------------      
Recovery Workbench User Stories Epic 1 Story Files v5 03-11-2026 17:01:21
Recovery Workbench User Stories Epic 1 Story Files v6 15-11-2026 17:03:14
Recovery Workbench User Stories Epic 1 Story Files v7 16-11-2026 03:08:14
Recovery Workbench User Stories Epic 2 Story Files v5 16-11-2026 03:08:14



```

**Tool `grep`** - completed

```json
{"pattern": "TE 001|TE 002|TE 003|TE 011", "path": "_work", "include": "*.md", "limit": 40}
```

```text
No matches found
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Latest Epic 1 is v7 (16-11-2026). Let me read the 4 stories from v7. Also check "Read me first v2.md" in v7 to understand conventions.

Let me read 4 files. They might be long. Let's read them.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -File \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\" -Filter \"*TE 0*\" | Select-Object Name, Length | Format-Table -AutoSize"}
```

```text

Name                                                                 Length
----                                                                 ------
RWB TE 001 Recovery module folder and boundary test v1.md             14988
RWB TE 002 Code owners for the recovery module v1.md                  12974
RWB TE 003 Types and contract tests from the API specification v1.md  14726
RWB TE 004 Masked data in SIT and UAT v1.md                           15140
RWB TE 006 Outbox and retry for outbound work v1.md                   25457
RWB TE 007 Scheduled jobs on Quartz v2.md                             21745
RWB TE 008 Decision log hash chain check v1.md                        15905
RWB TE 011 PDPA lint for code tests and logs v1.md                    15873
RWB TE 012 Document storage containers v1.md                          18925
RWB TE 013 Agent runtime client with fallback v1.md                   17277



```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 001 Recovery module folder and boundary test v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 001 Recovery module folder and boundary test v1.md, lines 1-252
1: # RWB-TE-001 Recovery module folder and boundary test
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-TE-001 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P2 Integration |
13: | Feature | None |
14: | Requirement IDs | REQ-DRI-006 |
15: | BRD section | Business Requirements Program, section 7 (constraint Modular monolith) and section 5.2 |
16: | L3 process | All recovery processes |
17: | Decision | DL05 |
18: | Priority | Must |
19: | Depends on | None |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.
25: 
26: ## 2. Business rationale
27: 
28: Three teams build in one ACE service. Without a checked boundary, a change in one team's code breaks another's, and a direct call to a core system could bypass the COLLINS and file load path. The skeleton gives each Workbench module one package with a published part and an internal part, and a test in every build refuses a call into another module's internal part, a cross-module table read and a direct system call outside the integration adapters. It meets REQ-DRI-006 and applies DT08, ADR-002 and DL05 (option B from 2 November: TechX creates the recovery module in its own package). The measure is the count of boundary violations merged to main, which must stay at zero.
29: 
30: ## 3. Preconditions
31: 
32: - Access to the ACE repository for the TechX squads (DL36).
33: - DL05 is applied as option B from 2 November 2026: TechX creates the recovery module in its own package; the ACE team applies the module boundaries for the common and collection modules later.
34: - The common module's published packages are named in the module map. Until the ACE team names them, the map lists `..common.api..` (assumed; DL05).
35: - The ACE build runs the unit test phase on every pull request.
36: 
37: ## 4. Flow
38: 
39: 1. Squad member: creates the recovery folders and packages for the 19 Workbench modules,
... truncated (16,357 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 002 Code owners for the recovery module v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 002 Code owners for the recovery module v1.md, lines 1-230
1: # RWB-TE-002 Code owners for the recovery module
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-TE-002 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P2 Integration |
13: | Feature | None |
14: | Requirement IDs | REQ-DRI-006 |
15: | BRD section | Business Requirements Program, section 7 (constraints Built on ACE and Modular monolith) |
16: | L3 process | All recovery processes |
17: | Decision | DL37 |
18: | Priority | Must |
19: | Depends on | RWB-TE-001 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.
25: 
26: ## 2. Business rationale
27: 
28: The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-TE-001 is done: the recovery folders and the module map exist.
33: - The repository host supports a code owners file (GitHub format assumed, as ACE uses GitHub Copilot under DL32).
34: - The teams exist in the repository host: TechX recovery tech leads and the ACE team. Names assumed until DL37 and DL36 are answered: `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`.
35: - The repository administrator of the ACE team can set the branch rule on main.
36: 
37: ## 4. Flow
38: 
39: 1. Squad member: writes `.github/CODEOWNERS` with the entries in
... truncated (14,228 chars total)
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 003 Types and contract tests from the API specification v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 003 Types and contract tests from the API specification v1.md, lines 1-255
1: # RWB-TE-003 Types and contract tests from the API specification
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-TE-003 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P2 Integration |
13: | Feature | None |
14: | Requirement IDs | REQ-DRI-007, REQ-ACA-003 |
15: | BRD section | Business Requirements Program, section 5.2 and section 5.4 |
16: | L3 process | All recovery processes |
17: | Decision | None |
18: | Priority | Must |
19: | Depends on | RWB-TE-001 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.
25: 
26: ## 2. Business rationale
27: 
28: The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-TE-001 is done: the recovery folders and the boundary test exist; the generated packages are listed in the module map as shared.
33: - The API specification is held in the repository at `api/recovery-api.yaml`, base path /api/recovery/v1, with x-module, x-capability and x-first-release on every operation.
34: - The permission matrix seed (roles.txt, loaded as the role and permission tables by RWB-E1-037) is available to tests.
35: - The build property `rwb.release` names the release being built: E1 for 30 Novembe
... truncated (16,121 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 011 PDPA lint for code tests and logs v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 011 PDPA lint for code tests and logs v1.md, lines 1-275
1: # RWB-TE-011 PDPA lint for code, tests and logs
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-TE-011 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P2 Integration |
13: | Feature | None |
14: | Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
15: | BRD section | Business Requirements Program, section 6.7 and section 6.9 |
16: | L3 process | All recovery processes |
17: | Decision | None |
18: | Priority | Must |
19: | Depends on | RWB-TE-001 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.
25: 
26: ## 2. Business rationale
27: 
28: Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-TE-001 is done: the recovery folders and the pipeline checks exist.
33: - The data dictionary marks each personal field (the `is_personal` column of the metadata table sys_fields in the schema, and `x-personal-data: true` in the API specification).
34: - Synthetic test data uses the prefix "SYN-" for every value placed in a personal field (assumed convention of RWB-E1-065).
35: - The masking helper of the common module is available for the rare log line that must name a record (assumed published as part of the common module's PII logging interface).
36: 
37: ## 4. Flow
38: 
39: 1. Build: reads the personal fields from th
... truncated (17,350 chars total)
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now I have the four stories. The user wants to explain these to the developers. So I should produce a clear, developer-oriented explanation: what each story is, why it exists, what "done" looks like, dependencies, effort, and the order. Also note these are "TE" — technical enablers (PLATFORM/TECH) under Epic 1, Module P2 Integration, release 30 Nov 2026.

I should think about whether they want a document or just chat explanation. "tell me about user story t001 t002 t003 t011 i need to explain to the peopple who are developing this" — they want to explain to developers. Chat answer with clear structure is good. Maybe offer to make a briefing doc/slides. But primarily answer in chat.

Let me check if there's any updated version of these stories in "14 Story Updates" or elsewhere that changes content — e.g., maybe v7 TE 003 was superseded. Let me quickly grep for "RWB-TE-003" in the latest folders to see if there's a v2. Actually file list shows only v1. There's "14 Story Updates" folder — let me see what's there quickly to avoid stale info.

Also should check if TE 001 etc. appear in the Epic1 grooming order spreadsheet with points. The xlsx "Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx" might contain points and order. That'd be helpful for explaining sequencing. Let me peek at it. Use python? Check if python available. Could use openpyxl. Let me check quickly.

Actually the "TE" stories are technical enablers, part of Epic 1 (release 30 Nov 2026), Module P2 Integration. The grooming order spreadsheet could give points and order. Let's try reading with python.

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"import openpyxl, sys; print(openpyxl.__version__)\""}
```

```text
3.1.5

```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File \"14 Story Updates\" | Select-Object FullName | Format-Table -AutoSize -Wrap"}
```

```text

FullName                                                                                                               
--------                                                                                                               
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\14 Story Updates\Recovery Workbench Data Load Story 
Removals v1.md                                                                                                         
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\14 Story Updates\Recovery Workbench Data Load Story 
Removals v2.md                                                                                                         
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\14 Story Updates\Recovery Workbench Project Hub     
v15.html                                                                                                               
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\14 Story Updates\Recovery Workbench Project Hub     
v16.html                                                                                                               
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\14 Story Updates\Recovery Workbench Project Hub     
v17.html                                                                                                               



```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me check grooming order xlsx for these 4 stories — points, order, sprint. This will help the developer briefing.

</details>

**Tool `shell`** - completed

```json
{"command": "@'\nimport openpyxl\np=r\"Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx\"\nwb=openpyxl.load_workbook(p, data_only=True)\nfor ws in wb.worksheets:\n    print(\"SHEET:\", ws.title, ws.max_row, ws.max_column)\n    for r in ws.iter_rows(min_row=1, max_row=min(6, ws.max_row), values_only=True):\n        print([str(c)[:40] if c is not None else \"\" for c in r])\n    print()\n'@ | python -"}
```

```text
SHEET: Epic 1 Grooming Plan 78 18
['Recovery Workbench Epic 1 � Grooming Ord', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
['72 current stories, 16 capability sessio', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
['Overall Order', 'Session', 'Grooming Group', 'Order in Session', 'Story Key', 'Title', 'Item Type', 'Primary Grooming Focus', 'Grooming Status', 'Remarks', 'Owner', 'Target Date', 'Notes / Open Clarifications', 'Planned Grooming Date', 'Track (Group 1 / 2)', 'Dependency Layer', 'Depends on (Prerequisites)', 'Blocks (Downstream)']
['1', '1', 'Engineering Architecture & Delivery Guar', '1', 'RWB-TE-001', 'Recovery module folder and boundary test', 'Technical Enabler', 'Module boundaries, code ownership, API c', 'Not Started', '', '', '', 'Confirm package boundary rule and the bu', 'Mon, 16 Nov 2026', 'Group 1', '1 � Foundation', 'No prerequisites', 'RWB-TE-002, RWB-TE-003, RWB-TE-011, RWB-']
['2', '1', 'Engineering Architecture & Delivery Guar', '2', 'RWB-TE-002', 'Code owners for the recovery module', 'Technical Enabler', 'Module boundaries, code ownership, API c', 'Not Started', '', '', '', 'Name the code owners for each recovery p', 'Mon, 16 Nov 2026', 'Group 1', '1 � Foundation', 'RWB-TE-001', '�']

SHEET: Parallel Schedule (Group 1 & 2) 69 11
['Epic 1 Parallel Grooming Schedule � Grou', '', '', '', '', '', '', '', '', '', '']
['Two parallel grooming rooms. Group 1 is ', '', '', '', '', '', '', '', '', '', '']
['', '', '', '', '', '', '', '', '', '', '']
['Day 1 � Monday, 16 Nov 2026      �      ', '', '', '', '', '', '', '', '', '', '']
['GROUP 1 (Track 1 � upstream) � 8 stories', '', '', '', '', '', 'GROUP 2 (Track 2 � downstream) � 6 stori', '', '', '', '']
['#', 'Story Key', 'Title', 'Session', 'Dependency note', '', '#', 'Story Key', 'Title', 'Session', 'Dependency note']

SHEET: Cross-Track References 28 9
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
  File "C:\Users\SahilMore\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2192' in position 10: character maps to <undefined>

Exited with code 1
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me extract rows for TE-001, TE-002, TE-003, TE-011 from the grooming plan.

</details>

**Tool `shell`** - completed

```json
{"command": "@'\nimport openpyxl, io, sys\nsys.stdout.reconfigure(encoding=\"utf-8\")\np=r\"Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx\"\nwb=openpyxl.load_workbook(p, data_only=True)\nws=wb[\"Epic 1 Grooming Plan\"]\nhdr=[c.value for c in ws[4]]\nwant={\"RWB-TE-001\",\"RWB-TE-002\",\"RWB-TE-003\",\"RWB-TE-011\"}\nfor row in ws.iter_rows(min_row=5, values_only=True):\n    if row[4] in want:\n        print(\"=\"*90)\n        for h,v in zip(hdr,row):\n            if v not in (None,\"\"):\n                print(f\"{h}: {v}\")\n'@ | python -"}
```

```text
==========================================================================================
Overall Order: 1
Session: 1
Grooming Group: Engineering Architecture & Delivery Guardrails
Order in Session: 1
Story Key: RWB-TE-001
Title: Recovery module folder and boundary test
Item Type: Technical Enabler
Primary Grooming Focus: Module boundaries, code ownership, API contract tests and PDPA lint
Grooming Status: Not Started
Notes / Open Clarifications: Confirm package boundary rule and the build gate owner.
Planned Grooming Date: Mon, 16 Nov 2026
Track (Group 1 / 2): Group 1
Dependency Layer: 1 – Foundation
Depends on (Prerequisites): No prerequisites
Blocks (Downstream): RWB-TE-002, RWB-TE-003, RWB-TE-011, RWB-E1-071, RWB-TE-012
==========================================================================================
Overall Order: 2
Session: 1
Grooming Group: Engineering Architecture & Delivery Guardrails
Order in Session: 2
Story Key: RWB-TE-002
Title: Code owners for the recovery module
Item Type: Technical Enabler
Primary Grooming Focus: Module boundaries, code ownership, API contract tests and PDPA lint
Grooming Status: Not Started
Notes / Open Clarifications: Name the code owners for each recovery package.
Planned Grooming Date: Mon, 16 Nov 2026
Track (Group 1 / 2): Group 1
Dependency Layer: 1 – Foundation
Depends on (Prerequisites): RWB-TE-001
Blocks (Downstream): —
==========================================================================================
Overall Order: 3
Session: 1
Grooming Group: Engineering Architecture & Delivery Guardrails
Order in Session: 3
Story Key: RWB-TE-003
Title: Types and contract tests from the API specification
Item Type: Technical Enabler
Primary Grooming Focus: Module boundaries, code ownership, API contract tests and PDPA lint
Grooming Status: Not Started
Notes / Open Clarifications: Confirm the API spec version used for generated types.
Planned Grooming Date: Mon, 16 Nov 2026
Track (Group 1 / 2): Group 1
Dependency Layer: 1 – Foundation
Depends on (Prerequisites): RWB-TE-001
Blocks (Downstream): —
==========================================================================================
Overall Order: 4
Session: 1
Grooming Group: Engineering Architecture & Delivery Guardrails
Order in Session: 4
Story Key: RWB-TE-011
Title: PDPA lint for code, tests and logs
Item Type: Technical Enabler
Primary Grooming Focus: Module boundaries, code ownership, API contract test
... truncated (2,798 chars total)
```

### Assistant - 2026-11-16 13:07 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

There's also a "Cross-Track References" sheet. Let me check what it says about TE-011 or others maybe. Also check points/story points - not in columns. Let me look at Cross-Track References and maybe the parallel schedule for essentials.

Actually the grooming plan has no story points. TE-002 explicitly says 1 point.

Let me also check the Session 1 agenda maybe. But we have enough.

Let me check Cross-Track References for these stories quickly.

</details>

**Tool `shell`** - completed

```json
{"command": "@'\nimport openpyxl, sys\nsys.stdout.reconfigure(encoding=\"utf-8\")\np=r\"Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx\"\nwb=openpyxl.load_workbook(p, data_only=True)\nfor name in [\"Cross-Track References\"]:\n    ws=wb[name]\n    print(\"SHEET\", name)\n    for row in ws.iter_rows(values_only=True):\n        vals=[str(v) for v in row if v not in (None,\"\")]\n        if vals: print(\" | \".join(vals))\n'@ | python -"}
```

```text
SHEET Cross-Track References
Group 2 → Group 1 Dependency References
22 Group 2 stories reference 45 Group 1 decisions. There are ZERO Group 1 → Group 2 references, so Group 1 never waits on Group 2.
# | Group 2 Story | Title | Group 2 Session | Day | Group 1 Prerequisites | Group 1 Session(s) | Latest Day | Handling
1 | RWB-TE-012 | Document storage containers | S9: Document Foundation & Storage | 1 | RWB-TE-001 | S1 | Day 1 | Same day — confirm at session start
2 | RWB-E1-025 | Document types and fields agreed | S9: Document Foundation & Storage | 1 | RWB-E1-069 | S3 | Day 2 | Later Group 1 input — design reference only
3 | RWB-E1-024 | Document store and index | S9: Document Foundation & Storage | 1 | RWB-E1-001, RWB-E1-027, RWB-E1-018 | S3, S5, S7 | Day 4 | Later Group 1 input — design reference only
4 | RWB-E1-066 | Interaction ledger store and writer | S10: Interaction Ledger | 1 | RWB-E1-027, RWB-E1-018 | S5, S7 | Day 4 | Later Group 1 input — design reference only
5 | RWB-E1-049 | OCR pipeline on the Workbench document hub | S13: Document Intake, OCR & Classification | 2 | RWB-E1-045 | S2 | Day 1 | Group 1 input on Day 1 — before this session
6 | RWB-E1-011 | Reconciliation and data quality report | S12: Reconciliation, Retention & Decision-Log Copy | 3 | RWB-E1-069, RWB-E1-015 | S3, S4 | Day 2 | Group 1 input on Day 2 — before this session
7 | RWB-E1-017 | Retention and archive rule for the data store | S12: Reconciliation, Retention & Decision-Log Copy | 3 | RWB-E1-043, RWB-E1-001, RWB-E1-064 | S2, S3 | Day 2 | Group 1 input on Day 2 — before this session
8 | RWB-E1-014 | Decision log copy to the data lake | S12: Reconciliation, Retention & Decision-Log Copy | 3 | RWB-E1-056 | S4 | Day 2 | Group 1 input on Day 2 — before this session
9 | RWB-E1-002 | Case list v1 with case ID, owner and queue | S11: Case List, Queue Views & Case Record | 4 | RWB-E1-069, RWB-E1-015, RWB-E1-007, RWB-E1-018, RWB-E1-020 | S3, S4, S7 | Day 4 | Same day — confirm at session start
10 | RWB-E1-031 | Queue and owner on the case list with filters | S11: Case List, Queue Views & Case Record | 4 | RWB-E1-039, RWB-E1-020 | S6, S7 | Day 4 | Same day — confirm at session start
11 | RWB-E1-023 | Case record view v1, read only | S11: Case List, Queue Views & Case Record | 4 | RWB-E1-069, RWB-E1-037, RWB-E1-039, RWB-E1-018 | S3, S6, S7 | Day 4 | Same day — confirm at session start
12 | RWB-E1-035 | Case record view v1.1 with documents and history timeline | S11: Cas
... truncated (4,535 chars total)
```

### Assistant - 2026-11-16 13:08 | opencode-go/deepseek-v4.1-flash | build

## What these four actually are

`T001`, `T002`, `T003`, `T011` are the **RWB-TE-001 / 002 / 003 / 011** stories — the "TE" series (Technical Enabler), not business features. They sit in **Epic 1, Module P2 Integration, release 30 Nov 2026**, and the grooming plan puts all four in **Session 1, "Engineering Architecture & Delivery Guardrails"**, in this order.

The one thing to tell the developers up front: **none of these ships a screen or a database table. Each one ships a build gate, plus proof that the gate actually fails when someone breaks the rule.** "Done" means a bad pull request is blocked, not that code was written.

```openui-lang
root = Stack([glance])
glance = Table(["#", "Story", "What it creates", "Done when"], [["1", "RWB-TE-001", "19 module packages (api + internal), module map, ArchUnit boundary test, front-end import rules, RecoveryAccessGuard", "A fixture that breaks each rule fails the build; main's boundary test is green"], ["2", "RWB-TE-002", "CODEOWNERS, validation step, branch rule on main", "Test PRs prove merge stays blocked without an owner approval"], ["3", "RWB-TE-003", "Generated Spring interfaces/models, TS types + client, contract and access test per operation", "E1 report shows every E1 operation passed or pending with a named story"], ["4", "RWB-TE-011", "PDPA lint generated from the data dictionary, allow list, pipeline step", "Lint runs on main with zero findings; every rule's fixture fails"]])
```

## RWB-TE-001 — Recovery module folder and boundary test

**The idea:** three teams build inside one ACE service. This story gives each Workbench module its own package with a published `api` part and an `internal` part, then makes the build refuse any call that crosses a line it shouldn't.

**What the team builds**
- 19 module packages: `dataengine`, `integration`, `casewf`, `access`, `dochub`, `comms`, `decision`, `payments`, `reporting`, `agent` (P1–P10), plus `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner` (S1–S9).
- `architecture/recovery-modules.yaml` — the module map. Module names, packages and published packages live here, **not in the test code**.
- `RecoveryBoundaryTest` (ArchUnit) with rules **BND-1 to BND-5**: collection module only via published packages; common module only via published packages; recovery module to recovery module only via a published package or an application event; entities and repositories stay inside their module (a module reads only its own tables); only `recovery.integration.adapter` (and the agent runtime client) may use HTTP/SFTP/file clients. **No recovery class calls a system of record directly.**
- Front-end dependency rules for `src/modules/recovery` — no importing `src/modules/collection`.
- `RecoveryAccessGuard` wired for `/api/recovery/v1/**` to the common module's access check, returning 403 with `MSG-P4-002`.

**Watch-outs to raise**
- It depends on **DL05 option B** — the ACE team must name the common and collection published packages. Until then the map assumes `..common.api..`. That is a real external dependency, not a coding detail.
- Keep the breaking fixtures in `src/test`; they must never ship.
- The access guard is easy to overlook — this story is not only folder structure.
- It blocks TE-002, TE-003, TE-011, TE-012 and E1-071, so it genuinely has to land first.

## RWB-TE-002 — Code owners for the recovery module

**The idea:** the recovery and collection squads plus the ACE team merge into one repository. Without named owners per folder, a change can merge without the team that answers for it approving.

**What the team builds**
- `.github/CODEOWNERS` mapping recovery back end, tests, migrations, front end and the module map to `@scb-ace/techx-recovery-tech-leads`; the common module to `@scb-ace/ace-team`; the CODEOWNERS file to both. Most specific path last.
- A **CodeOwnersValidation** pipeline step: syntax, every owner exists and has write access, every pattern matches at least one file.
- A branch rule on `main`: require a PR, require code owner review, 1 approval, dismiss stale approvals on a new commit, author's own approval does not count.
- Six test pull requests on a protected test branch to prove each rule.

**Watch-outs to raise**
- It is small — the story itself calls it **1 point** — but it needs the **ACE team repository administrator** to set the branch rule. That is schedule risk, not effort risk.
- Team handles are **assumed** until DL36/DL37 are answered. Confirm the real handles before writing the file.
- If the author is a code owner, their approval doesn't count — teams need to know that or they'll think the rule is broken.

## RWB-TE-003 — Types and contract tests from the API specification

**The idea:** the recovery API is **79 operations in one OpenAPI 3.1 file** (`api/recovery-api.yaml`, base path `/api/recovery/v1`). If server code, front-end code and the spec are maintained by hand, a renamed field breaks a screen in SIT, and an endpoint can ship without the capability check its spec declares. This story generates both sides from the file and tests every implemented operation against it.

**What the team builds**
- A lint rule set that fails on a missing `operationId`, `x-module`, `x-capability` (area + right), `x-first-release`, or a missing error response.
- Server generation: Spring interfaces and models, interface only, into a shared generated package listed in the module map.
- Front-end generation: TypeScript types and a typed fetch client into `src/modules/recovery/api/generated`.
- `OperationCatalog` — reads operations, release and capability from the file.
- `RecoveryContractTest` — one success test per implemented operation, validating status, content type and schema against the spec.
- `RecoveryAccessContractTest` — one test per implemented operation: a role whose permission lacks the declared right must get **403, `application/problem+json`, `MSG-P4-002`**.
- Release gating through build property `rwb.release` (E1 for 30 Nov). Operations first in a later release are reported as **pending** and don't fail the build; operations first in the current release with no implementation **do** fail it.

**Watch-outs to raise**
- Generated code is never hand-edited. A change goes into the spec.
- The access test is only as good as `x-capability` in the spec — wrong metadata means the test asserts the wrong right.
- The permission matrix seed (RWB-E1-037) must exist for the access tests to pick a role without the right.
- Contract tests run against synthetic fixtures in an in-memory database; no real customer data.

## RWB-TE-011 — PDPA lint for code, tests and logs

**The idea:** names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply — log stores, build artifacts, prompts to coding agents. This lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them.

**What the team builds**
- `tools/pdpa-lint`, comprising `PersonalFieldReader` (reads `is_personal` from `sys_fields` and `x-personal-data: true` from the API spec), `RuleGenerator`, `pdpa-rules.yaml`, `pdpa-allow.yaml`, `CheckDigitMatcher`, and the pipeline step `PdpaLintStep`.
- Rules: **PDPA-LOG-FIELD**, **PDPA-LOG-ENTITY**, **PDPA-EXCEPTION**, **PDPA-TOSTRING**, **PDPA-FIXTURE-FIELD**, **PDPA-FIXTURE-ID**.
- Scans back end and front end (including `console.log`), `src/test`, SQL seeds and JSON fixtures. Flags Thai national identifiers with a valid check digit, Thai mobile numbers, and emails outside the example domains.
- Synthetic test values use the **`SYN-`** prefix in personal fields.
- Allow list entries need an owner, a reason and an expiry date; an expired entry no longer excuses the finding.
- The lint **never prints the value it found** — only the rule, file, line and field name.

**Watch-outs to raise**
- This is the one most likely to create day-to-day friction. False positives get resented, so the masking-helper exception (AC8) and the allow-list process need to be agreed with the team before rollout.
- The `SYN-` convention is an assumption from RWB-E1-065 — confirm it.
- Who decides a field is personal belongs to Compliance / DL26, not the developers.
- It scans prompts too — that is deliberate, given coding agents receive fixtures and context.

## How the four fit together

`RWB-TE-001` is the foundation: it creates the folders, the map and the pipeline hooks. `TE-002`, `TE-003` and `TE-011` each attach a different gate to that foundation — **who may approve**, **what the API must look like**, and **what may never appear in code or logs**. That's why the dependency is one-way: 002, 003 and 011 all depend on 001; 001 depends on nothing. The spreadsheet also has 001 blocking `E1-071` (Temporal worker) and `TE-012` (document storage containers).

**A one-minute talk track you can use:**
> "These four aren't features. They're the four gates every later recovery story has to pass. T001 defines the walls between modules and stops anyone calling a core system directly. T002 makes sure a human owner approves anything that touches those walls. T003 makes the OpenAPI file the single truth for the API, and proves every endpoint checks its permission. T011 stops personal data getting into code, fixtures and logs. Each one is done when we can show a deliberately bad change being blocked in the pipeline."

## What still needs deciding at grooming

The stories are marked **Ready for build**, but these are open and worth settling with the developers in Session 1:

| Item | Story | Question |
|---|---|---|
| DL05 | TE-001 | Which packages do the common and collection modules publish? Until named, `..common.api..` is assumed. |
| DL36 / DL37 | TE-002 | Who exactly are the code owner teams, and do they exist in the repository host? |
| API spec version | TE-003 | Which version of `recovery-api.yaml` is the baseline for generated types? |
| Permission matrix seed | TE-003 | Is RWB-E1-037's seed available early enough for the access tests? |
| `SYN-` convention | TE-011 | Is the synthetic prefix agreed with the data team? |
| PDPA scope | TE-011 | Do the rules cover test data, prompts and logs exactly as Compliance expects (DL26)? |
| Gate ownership | all four | Who owns the pipeline and is allowed to change or waive a gate? |

If it's useful, I can turn this into a one-page developer briefing or a short kickoff deck for the session.

<details><summary>Reasoning</summary>

Now I have good material. I should produce a developer briefing.

I should decide format. The user says "tell me about user story t001 t002 t003 t011 i need to explain to the peopple who are developing this". So a chat explanation that they can read/relay. Best: a concise narrative per story, plus a table, dependency/order, and "what I'd tell the team" bullets, plus what's still open for grooming (open clarifications). Maybe include the grooming questions for developers to answer at the session.

I can also offer to produce a one-page briefing doc or slides. But don't overdo. Maybe ask at the end if they want a handout/PPT.

Consider a UI block? The instruction says use UI blocks for data/structured comparisons. A table of four stories (story, what it builds, why, done when, depends) would be useful. But key details might be too dense for a table. I can do a compact table plus prose. A `Table` component could work. Let me think: The reply should be readable by the user to relay. Markdown headings and sub-bullets are probably clearest. UI block may be nice for "at a glance" summary. But UI blocks aren't copyable to devs as text. The user wants to explain to people — likely they'll talk. I'll give Markdown with a summary table. Maybe one openui-lang table for the dependency chain? Hmm, keep it simple: Markdown is fine, and it's copyable. The guidance says prefer UI blocks for data the user would otherwise picture. A comparison table is exactly that. But the "Table" component in UI block is not copyable. I think a Markdown table is acceptable and more useful for relaying. I'll use Markdown, plus a Steps block maybe not needed.

Actually the harness says "Use one for data or structure the user would otherwise picture: values across items, comparisons, flows, trends, status." A comparison across four stories would be well served. But the answer needs nuance; a UI block can complement. I'll include a compact openui-lang Card/Table with the essentials, then prose detail. Hmm, risk of redundancy. Let me lead with the one-line answer, then a compact summary table in Markdown, then per-story sections with "what to build / what done looks like / watch-outs".

Let me make sure I'm accurate:

Common facts:
- All four are Technical Enablers (TE), not business features. Epic 1, release 30 Nov 2026, Module P2 Integration, Feature None, Priority Must, Status "Ready for build".
- All sit in grooming Group 1 "Engineering Architecture & Delivery Guardrails", Session 1, planne

_[truncated]_

</details>

### User - 2026-11-16 13:38

AC5 pass in t011 what AC are we taling about

### Assistant - 2026-11-16 13:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The user is asking about AC5 in T011 (RWB-TE-011). Wait — "AC5 pass in t011 what AC are we taling about". Hmm. Let me re-read TE-011's acceptance criteria.

AC1 Log statement
AC2 A whole entity in a log
AC3 A national identifier in a fixture
AC4 A personal field without the synthetic prefix
AC5 A field newly marked personal
AC6 An expired allow list entry
AC7 The front end
AC8 A masked value passes
AC9 An exception message
AC10 The text form of an entity

So AC5 = "A field newly marked personal". The user says "AC5 pass in t011" — maybe they mean AC5 in the story vs AC5 in our table? Hmm. My table said "every rule's fixture fails" — not AC5.

Wait, maybe they're confused because in my summary per-story I said "The lint runs on main with zero findings" and there's AC8 "A masked value passes". Hmm.

Actually, re-reading: "AC5 pass in t011 what AC are we taling about" — perhaps they're referring to a statement somewhere that AC5 passes. In TE-011's flow: "Pipeline: fails the build on any finding". There's no AC5 "pass" scenario. AC5 (A field newly marked personal) should fail the build. AC8 is the passing one.

Or perhaps the user is looking at another document (Project Hub v17) where TE-011's AC5 is different? Let me check if the hub has different AC numbering. The user might be reading the SharePoint hub. Hmm.

Let me search the hub/payload for TE-011 AC content. There's a Project Hub HTML with compressed payload — hard. Also "_work/td" has hub data. Maybe there's a JSON of stories.

Let me search for "A field newly marked personal" across files to see if there are alternative versions. And search for "AC5" near TE-011.

Actually, a simpler read: They ask "AC5 pass in t011 what AC are we talking about" — perhaps they're asking, in the context of my answer, which AC is the one that passes? I wrote "Done when ... every rule's fixture fails". In TE-011, AC8 is the pass case. But they wrote AC5. Maybe they mis-numbered.

I should answer directly: In RWB-TE-011, AC5 is "A field newly marked personal" — it's a fail scenario, not a pass. The only passing AC is AC8 ("A masked value passes" / v2 of log through masking helper). Then clarify what AC5 does exactly: dictionary marks `v_ace_account.contract_no` as personal in a new version; a log statement writes `account.getContractNo()`; then the system regenerates the rule set with `contract_no` and the build fails with PDPA-LOG-FIELD for `contract_no`. Its test case is TC-TE-011-05, covering AC5 + BR1.

And note AC5'

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "@'\nimport os,re,sys\nsys.stdout.reconfigure(encoding=\"utf-8\")\nbase=r\"04 User stories\"\nfor root,dirs,files in os.walk(base):\n    for f in files:\n        if \"TE 011\" in f:\n            p=os.path.join(root,f)\n            print(\"=\"*80); print(p)\n            for i,line in enumerate(open(p,encoding=\"utf-8\",errors=\"replace\"),1):\n                if re.search(r\"Scenario: AC|AC5|AC8\", line):\n                    print(i, line.rstrip())\n'@ | python -"}
```

```text
================================================================================
04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB TE 011 PDPA lint for code tests and logs v1.md
55 | X5 | A field is newly marked personal in the dictionary | Rules regenerate; existing uses of the field are found | Build log: PDPA-LOG-FIELD | AC5 |
58 | X8 | A log statement writes a field through the masking helper | Passes | None | AC8 |
82   Scenario: AC1 Log statement
88   Scenario: AC2 A whole entity in a log
93   Scenario: AC3 A national identifier in a fixture
98   Scenario: AC4 A personal field without the synthetic prefix
104   Scenario: AC5 A field newly marked personal
111   Scenario: AC6 An expired allow list entry
116   Scenario: AC7 The front end
121   Scenario: AC8 A masked value passes
126   Scenario: AC9 An exception message
131   Scenario: AC10 The text form of an entity
213 1. Write PersonalFieldReader and RuleGenerator; test that a newly marked field appears in the rules (AC5).
216 4. Add the masking helper exception to the log rules (AC8).
246 | TC-TE-011-05 | AC5, BR1 | System | Dictionary version marking contract_no personal |
249 | TC-TE-011-08 | AC8 | System | Log line through the masking helper |
================================================================================
04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB TE 011 PDPA lint for code tests and logs v1.md
55 | X5 | A field is newly marked personal in the dictionary | Rules regenerate; existing uses of the field are found | Build log: PDPA-LOG-FIELD | AC5 |
58 | X8 | A log statement writes a field through the masking helper | Passes | None | AC8 |
82   Scenario: AC1 Log statement
88   Scenario: AC2 A whole entity in a log
93   Scenario: AC3 A national identifier in a fixture
98   Scenario: AC4 A personal field without the synthetic prefix
104   Scenario: AC5 A field newly marked personal
111   Scenario: AC6 An expired allow list entry
116   Scenario: AC7 The front end
121   Scenario: AC8 A masked value passes
126   Scenario: AC9 An exception message
131   Scenario: AC10 The text form of an entity
213 1. Write PersonalFieldReader and RuleGenerator; test that a newly marked field appears in the rules (AC5).
216 4. Add the masking helper exception to the log rules (AC8).
246 | TC-TE-011-05 | AC5, BR1 | System | Dictionary version marking contract_no personal |
249 | TC-TE-011-08 | AC8 | System | Log line th
... truncated (3,792 chars total)
```

### Assistant - 2026-11-16 13:38 | opencode-go/deepseek-v4.1-flash | build

In **RWB-TE-011**, AC5 is **"A field newly marked personal"** — and it is a **fail-the-build** scenario, not a passing one.

```gherkin
Scenario: AC5 A field newly marked personal
  Given the dictionary marks v_ace_account.contract_no as personal in a new version
  Given a log statement writes account.getContractNo()
  When the pipeline runs
  Then the system regenerates the rule set with contract_no
  Then the build fails with rule PDPA-LOG-FIELD for contract_no
```

It proves the rule set is **generated from the data dictionary** (BR1): Compliance marks a new field personal, the lint regenerates, and existing code using that field is caught without anyone editing the lint. It maps to exception path **X5** and test case **TC-TE-011-05** (covers AC5 + BR1).

The only AC in TE-011 that *passes* is **AC8 — "A masked value passes"**, where the log line goes through the masking helper.

```openui-lang
root = Stack([acs])
acs = Table(["AC", "Scenario", "Build result"], [["AC1", "Log statement writes a personal field", "Fail – PDPA-LOG-FIELD"], ["AC2", "Log statement writes a whole personal entity", "Fail – PDPA-LOG-ENTITY"], ["AC3", "Fixture holds a valid Thai national identifier", "Fail – PDPA-FIXTURE-ID"], ["AC4", "Personal field without the SYN- prefix", "Fail – PDPA-FIXTURE-FIELD"], ["AC5", "Field newly marked personal in the dictionary", "Fail – PDPA-LOG-FIELD for the new field"], ["AC6", "Allow list entry past its expiry", "Fail – allow entry expired"], ["AC7", "Front end console or logger writes a personal property", "Fail – PDPA-LOG-FIELD"], ["AC8", "Log line through the masking helper", "Pass"], ["AC9", "Exception message carries a personal field", "Fail – PDPA-EXCEPTION"], ["AC10", "Entity text form includes a personal field", "Fail – PDPA-TOSTRING"]])
```

If you saw "AC5 … passes" somewhere, the likely source is **RWB-TE-001's AC5**, which has both outcomes: an `HttpClient` use in `recovery.casewf.internal` fails with BND-5, while the same use in `recovery.integration.adapter` passes. In TE-011, AC5 is strictly a blocking case.

<details><summary>Reasoning</summary>

All versions agree. So AC5 in TE-011 is "A field newly marked personal" — and it fails the build, it doesn't pass. The pass case is AC8.

The user's phrasing "AC5 pass in t011" might be them asking "AC5 — pass in T011? What AC are we talking about?" Perhaps they're checking my earlier statement. Let me answer crisply:

- In RWB-TE-011, AC5 = "A field newly marked personal" (section 7). It is a failing scenario: dictionary marks `v_ace_account.contract_no` personal → rule set regenerates → log line using `getContractNo()` → build fails with PDPA-LOG-FIELD for `contract_no`.
- The only AC that passes is AC8 "A masked value passes" (log through masking helper).
- Exception path X5 maps to AC5; test case TC-TE-011-05 covers AC5 + BR1.
- If they were expecting a pass at AC5, they might be thinking of AC8, or of TE-003's AC5 ("A current operation with no implementation fails") — also a failure. Or TE-001 AC5 ("No direct call to a system of record") — fails in casewf, passes in integration.adapter. That one has a pass element.

Actually that's a good possibility! In TE-001, AC5 includes: "Then the same use in 'recovery.integration.adapter' passes." So if they're remembering "AC5 ... passes," it's likely TE-001 AC5. But they said "in t011". Hmm.

Maybe they mean the grooming or my table? Let me consider: I said in my table TE-011 "Done when: Lint runs on main with zero findings; every rule's fixture fails". Not AC5.

I'll answer the direct question and cover the ambiguity: AC5 in TE-011 is the "field newly marked personal" scenario, and it fails; the pass is AC8. If they saw "pass" attached to AC5, it's probably TE-001 AC5 (where the same HTTP client use passes in `recovery.integration.adapter`).

I should keep it short. Include the exact Gherkin excerpt. Maybe a small table of AC1–AC10 with pass/fail. That's useful and scannable. Let me include it as a UI block table? The guidance says use UI blocks for data across items. A compact table of 10 ACs with "expected build result" is a good fit. But it might be overkill for a clarification. Still, it directly answers "what AC are we talking about" and prevents further confusion. I'll do a compact Markdown table instead — easier to copy. Hmm, the system prompt pushes UI blocks for tables. But it also says not for a short list. 10 rows is not short. I'll use a UI block Table with columns AC, Scenario, Expected result. Then a short note.

Wait — "AC5 pass" maybe refers to the fact that in TE-011 AC5, the acceptance is th

_[truncated]_

</details>

### User - 2026-11-16 13:49

how will this pipeline work in t011

### Assistant - 2026-11-16 13:49 | opencode-go/deepseek-v4.1-flash | build

## Short answer

In RWB-TE-011 the "pipeline" is a **static analysis job in the ACE pull-request pipeline**, not a runtime service. It runs on every PR and every build of `main`, regenerates its rules from the data dictionary, scans the code and test assets, and fails the build on any unexcused personal-data finding. There is no warning mode and no feature flag — the story explicitly says a build check has no runtime path to switch off.

```openui-lang
root = Stack([flow, targets])
flow = Steps([{title: "1. Trigger", markdown: "Every pull request and every build of main."}, {title: "2. Read the inputs", markdown: "sys_fields seed (is_personal), API specification (x-personal-data), source and test folders, pdpa-allow.yaml."}, {title: "3. Generate the rules", markdown: "PersonalFieldReader → RuleGenerator → pdpa-rules.yaml with snake_case, Java getter, JSON and TypeScript names."}, {title: "4. Scan source", markdown: "Log calls, string building in logs, exception messages, entity text forms. Java and front end."}, {title: "5. Scan fixtures and seeds", markdown: "SQL, JSON, end-to-end data: personal fields without SYN-, plus real-looking IDs, mobiles and emails."}, {title: "6. Apply the allow list", markdown: "A finding is excused only by an entry with an owner, a reason and an expiry date not yet passed."}, {title: "7. Report and gate", markdown: "Any unexcused finding fails the build. Prints rule, file, line and field name — never the value."}], "column")
targets = Table(["Scan target", "What it looks for", "Rule"], [["Main and front-end source", "Log calls or log strings using a personal field, or a whole personal entity", "PDPA-LOG-FIELD, PDPA-LOG-ENTITY"], ["Exception construction", "Exception messages carrying a personal field", "PDPA-EXCEPTION"], ["Entity text form", "toString or equivalent including a personal field", "PDPA-TOSTRING"], ["Tests, seeds, fixtures", "Personal-field literals without the SYN- prefix; valid Thai national IDs, Thai mobiles, non-example emails", "PDPA-FIXTURE-FIELD, PDPA-FIXTURE-ID"]])
```

## Stage by stage

**1. It starts from data, not from a hard-coded list.** `PersonalFieldReader` reads two sources: the `is_personal` column of the `sys_fields` seed, and `x-personal-data: true` in `api/recovery-api.yaml`. This is BR1 — the field list is never written inside the lint. Consequences worth telling the team:

- Compliance (DL26) can mark a new field personal and the next build picks it up. That is exactly what AC5 tests.
- `pdpa-rules.yaml` is therefore a **build artifact**, regenerated each run. It should not be committed and it must never be hand-edited.
- A field marked personal in the dictionary but missing from the API spec (or the reverse) is a definition gap to fix at source, not in the lint.

**2. `RuleGenerator` expands each field into the forms the scanners will meet.** For `first_name` that means `first_name` (SQL/JSON), `getFirstName` (Java), `firstName` (JSON/TypeScript), plus the entity class names that hold personal fields (`CustomerEntity`, `PartyEntity`, `ContactEntity`). That is how the same rule catches a getter in Java, a property in React, and a column in a seed file.

**3. The scan is four passes, not one regex.**
- **Log pass.** Finds logging calls (`log.info/debug/warn/error`, `System.out`, front-end `console.log` and logger calls), then inspects the arguments. A direct personal getter, a string built with one, or a whole entity object fails. The last one is AC2 — logging `customer` when `CustomerEntity` holds personal fields is a `PDPA-LOG-ENTITY` finding even without naming a field.
- **Exception pass.** `new IllegalStateException("No case for " + customer.getCifNo())` is `PDPA-EXCEPTION`. The story treats error messages as a leak path, not just logs.
- **Text-form pass.** Any entity with a personal field must leave it out of its `toString` / text form (`PDPA-TOSTRING`). This matters because those strings end up in logs and error payloads indirectly.
- **Fixture pass.** Parses SQL `INSERT`/`UPDATE` column-value pairs and JSON/e2e property values. A personal field with a literal that does not start with `SYN-` is `PDPA-FIXTURE-FIELD`. Separately, `CheckDigitMatcher` looks for a 13-digit Thai national ID with a valid check digit, a Thai mobile number, or an email outside the example domains — anywhere in a test asset, regardless of column name (`PDPA-FIXTURE-ID`). AC3's fixture is generated by the test at run time, so a valid-looking ID is never committed.

**4. The masking helper is the only sanctioned escape hatch in code.** AC8: if the value is written through the common module's masking helper, that line passes. The scanner has to recognise the helper call and treat its output as safe. This is an implementation detail worth agreeing early with the tech leads: whether only individual values wrapped in the helper pass, or also a whole entity passed through a masking function.

**5. The allow list is time-boxed, not a mute button.** `pdpa-allow.yaml` entries carry rule, path, line or pattern, owner, reason and expiry. A matching finding is excused only while the entry is valid; on the day after expiry the build fails with `allow entry expired: {rule} {path} since {date}` (AC6). Changes to that file go through the code owners from TE-002, so a developer cannot quietly suppress their own finding. `X11` — someone outside the owners approving an allow-list change — is refused by the repository host, not by the lint.

**6. The gate is binary.** Any unexcused finding fails the build. The report is one line per finding:

```
PDPA-LOG-FIELD: ace-service/src/main/java/.../CaseService.java:142 uses personal field first_name. Remove it or use the masking helper.
```

**It deliberately never prints the value it found** (BR7). That is why the developer gets file, line and field name — enough to locate it, not enough to leak it into the build log. For the ID rule, the value is never echoed either.

## What a developer actually experiences

A PR opens, the `PDPA lint` check runs, and either it is green or it lists findings. The fix loop is: remove the field from the log or exception, route it through the masking helper, or replace the fixture value with a `SYN-` value. In the rare legacy case, add an allow-list entry with an owner, a reason and an expiry — and get it reviewed. Re-run is safe: the lint holds no state, and the same commit with the same dictionary produces the same findings.

Practically, this job does not need to compile the code, so it can run early and in parallel with compile and the TE-003 contract tests. The story doesn't mandate that ordering; it is a pipeline design choice I'd make so developers get the privacy failure in minutes rather than at the end of the build.

## Boundaries of the check

- It is a **static** check. It will not catch values assembled dynamically at runtime, or data already in log stores from before the gate existed.
- It does not replace runtime masking by role (RWB-E1-037) or masked SIT/UAT data (RWB-TE-004). It closes the code, fixture and log-statement path only.
- **Prompts are named in the rationale and guardrails but are not in the contract's input list.** The grooming note flags "test data, prompts and logs" as an open clarification. If prompts must be scanned, that is a scope addition to agree with Compliance before build.
- The example email domains, the Thai mobile pattern and the `SYN-` convention are configuration values, not settled in the story. They need to be confirmed with the data team.
- It scans recovery source and test assets; it does not scan third-party libraries or compiled bytecode.

<details><summary>Reasoning</summary>

The user asks: "how will this pipeline work in t011" — they want a detailed explanation of the pipeline flow for RWB-TE-011 (PDPA lint). I should explain end-to-end: triggers, inputs, generation of rules, scanning, allow list evaluation, failure reporting, where it sits in the pipeline, what developers see, what artifacts, idempotency, restart. Also explain mechanics of the checks (log scanning, fixture scanning, toString, exception), how it distinguishes allowed masking helper, how allow list works, how it avoids printing values.

I have the story content. Let me re-read the relevant sections to be precise (I have them above). I should explain as a build pipeline, step by step, and probably include a flow diagram via openui-lang Steps (or a flow). The guidance: use UI blocks for flows. A `Steps` component with direction "column" or "row" would be good here. But I also want detail. Maybe use a Steps flow at a high level, then detail each stage in prose.

Let me think about the actual pipeline design implied by the story:

Trigger: every pull request and every build of main. Inputs: `sys_fields` seed (is_personal column), API specification (`x-personal-data: true`), source/test folders, `pdpa-allow.yaml`.

Step 1 — PersonalFieldReader: reads personal fields from schema seed + API spec. Output the field list (name variants).
Step 2 — RuleGenerator: writes `pdpa-rules.yaml` with name variants: snake_case (`first_name`), Java getter (`getFirstName`), camelCase property (`firstName`), TypeScript property (`firstName`, `lastName`), JSON property names. Note: `lastName` example in AC7 suggests JSON/TS camelCase. So generated rules cover 4 naming forms.
Step 3 — Scan main + frontend: log calls, string building in log calls, exception messages that use a personal field or whole personal entity.
Step 4 — Scan tests/e2e/SQL/JSON fixtures: literals in personal field positions not starting with `SYN-`; values matching Thai national ID with valid check digit, Thai mobile, email outside example domains.
Step 5 — Entity text form check: each entity with personal field excludes it from toString.
Step 6 — Allow list: match findings; entry must have owner, reason, expiry not passed.
Step 7 — Report/fail: print rule, file, line, field — never value.

Where in the pipeline: after checkout, before/parallel with compile? It's a static scan, so it can run early (fast feedback), independent of build. The story says "Build: reads..." then "Pipeline: fails..." It doesn't specify ord

_[truncated]_

</details>

### User - 2026-11-16 14:01

do for e-045

### Assistant - 2026-11-16 14:01 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The user says "do for e-045" — likely RWB-E1-045 "Multi product parameters for Mortgage HP and SSME v1" in Epic 1 Story Files v7. They want the same treatment: explain the story to developers, presumably how it works / detailed briefing. But "do for e-045" is terse. Given the previous turns: they asked about T001-T003-T011, then AC5 in T011, then "how will this pipeline work in t011". "do for e-045" likely means: do the same for E1-045 — explain the story, maybe AC/pipeline.

Ambiguous: could mean "tell me about user story E1-045 like you did for T001 etc." or "explain its pipeline". Safest: read E1-045 and produce the same kind of briefing, plus maybe flag the ACs. I should read the latest version: v7 "RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md".

Let me read it. Also check grooming spreadsheet row for E1-045 (session, order, dependencies) to add context.

Let me do both.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md, lines 1-298
1: # RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-E1-045 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | FEAT-CWC-25 Set product parameters without a code change |
14: | Requirement IDs | REQ-DRI-010, REQ-CWC-011 |
15: | BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
16: | L3 process | 14 Set strategy, policy and decision rules |
17: | Decision | D6 entry |
18: | Priority | Must |
19: | Depends on | RWB-E1-042, RWB-E1-043 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **center of excellence analyst (RW-COE)**, I want **every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product in the reference data**, so that **a new product or a product change needs no code change**.
25: 
26: ## 2. Business rationale
27: 
28: Mortgage, hire purchase and SSME follow different notice periods, service levels and bands, and today each difference is held in a team procedure. If the engines carry these values as constants, every product change waits for a release. This story keys each value by product group in the versioned reference tables of RWB-E1-043 and refuses a load that leaves a product without a required value. It meets REQ-DRI-010 and REQ-CWC-011. The measure is that a product is added or changed by a reference load with no deployment.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-043 is done: versioned reference tables, the registry and the read service.
33: - RWB-E1-042 is done: the parameter catalog marks each parameter with scope PRODUCT or GLOBAL, required yes or no, type, unit and allowed range (new catalog fields, see Additions).
34: - Tables PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL have an approved version in force.
35: - The timer engine (RWB-E1-028), case creation (RWB-E1-018) and the allocation engine (RWB-E1-020) read product values only through `ProductParameterService`.
36: - The loader holds RW-COE or RW-REFADM (Refer
... truncated (21,988 chars total)
```

**Tool `shell`** - completed

```json
{"command": "@'\nimport openpyxl, sys\nsys.stdout.reconfigure(encoding=\"utf-8\")\np=r\"Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx\"\nwb=openpyxl.load_workbook(p, data_only=True)\nws=wb[\"Epic 1 Grooming Plan\"]\nhdr=[c.value for c in ws[4]]\nfor row in ws.iter_rows(min_row=5, values_only=True):\n    if row[4]==\"RWB-E1-045\":\n        for h,v in zip(hdr,row):\n            if v not in (None,\"\"): print(f\"{h}: {v}\")\n'@ | python -"}
```

```text
Overall Order: 8
Session: 2
Grooming Group: Platform Foundation: Migrations, Configuration & Reference Data
Order in Session: 4
Story Key: RWB-E1-045
Title: Multi-product parameters for Mortgage, HP and SSME
Item Type: Business Story
Primary Grooming Focus: Migration versioning, parameter catalog, versioned reference data and multi-product parameters
Grooming Status: Not Started
Notes / Open Clarifications: Confirm the three product parameter sets and effective dating.
Planned Grooming Date: Mon, 16 Nov 2026
Track (Group 1 / 2): Group 1
Dependency Layer: 1 – Foundation
Depends on (Prerequisites): RWB-E1-042, RWB-E1-043
Blocks (Downstream): RWB-E1-028, RWB-E1-049, RWB-E1-026

```

### Assistant - 2026-11-16 14:01 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now produce the same kind of briefing for RWB-E1-045. It's a business story, Session 2, order 8, order in session 4, Group 1, layer 1 foundation, depends on E1-042 (parameter catalog) and E1-043 (reference data service with versioned tables); blocks E1-028 (timer engine), E1-049 (OCR pipeline), E1-026 (attach and search screen).

The user's "do for e-045" likely wants the same explanation style. I should cover:
- What it is / who for / why
- What gets built (components)
- The data model: PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL, keyed by product group, effective-dated via reference versions
- The five required parameters (ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS, EXPOSURE_BAND_SET)
- Service levels per product x status, required statuses assumption
- The load pipeline: upload → E1-043 checks → completeness check → type/range → approval → effective
- Runtime: ProductParameterService.get(productGroup, code, businessDate); TimerEngine, CaseEntryService, AllocationService; decision log records version
- Unit conversion: CALENDAR_DAYS vs WORKING_DAYS + v_ace_holiday
- Exception paths X1-X6 / AC1-AC8
- Design decisions: no new table, no screen, feature flag `rwb.p3.product-parameters`, done when no product group literal in code
- Watch-outs: effective dating edge cases, running timers keep expiry, removing products with open cases, duplicate rows, missing parameter at runtime → exception queue, product group not an enum, version recorded in decision log.
- Open questions: the three product parameter sets and effective dating; required statuses list (DL22); values per product (DL16 entry 90 days, DL22 service levels, DL23 caps); product owner approvals; Thai messages DL10.

Also, "how will this pipeline work" was the previous question — for E1-045 there's a load pipeline and a runtime lookup. I should explain both, since that's the substance.

I can include a Steps flow for the reference-load lifecycle and a Table for the parameters. Let me think about what's most useful.

Maybe structure:

1. One-line: E1-045 turns product differences into data.
2. At a glance table (story facts): module P3, feature, depends, session, size.
3. What problem it solves (3 products with different notice periods etc.)
4. The data model (3 reference tables + catalog)
5. The load pipeline (steps + what's validated)
6. The runtime path (how engines read it; effective dating; timers freeze)
7. AC map / what developers must demonstrate
8. Design constraints and got

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "MSG-P3-034", "include": "*.md", "limit": 20}
```

```text
Found 20 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v6\Recovery Workbench FSD P3 Case and workflow v4.md:
  Line 2241: | AC-EXC-P3-025-01 | Missing parameter blocked | a SERVICE_LEVEL load with valid from 2026-12-10 that has no row for "SSME" and status "WAITING_PARTNER" | the load validates | the load is refused with MSG-P3-034 naming "SSME" and "WAITING_PARTNER" And SERVICE_LEVEL version 3 stays in force | RWB-E1-045 |

  Line 2243: | AC-EXC-P3-025-03 | No parameter in force at run time | case "RW-2026-000140" with product group "SSME" and no NOTICE_PERIOD_DAYS row for "SSME" in force | the timer engine sets the notice timer on 2026-12-01 | no notice timer is written And the case is placed in the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS" | RWB-E1-045 |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 2529: This runs on its own once the file is loaded. The checks of RWB-E1-043 run first, then the new one you build as ProductCompletenessCheck, added as a table check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL. It confirms that every product in the PRODUCT version in force on the valid from date has a row for each catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for each status in the parameter servicelevel.required-statuses. A missing row refuses the whole load, with MSG-P3-034 naming the product and the item, and the version already in force stays in force. AC3 names SSME and WAITING_PARTNER.

  Line 2553: You change two services that already exist, CaseEntryService from RWB-E1-018 and AllocationService from RWB-E1-020, so they call ProductParameterService.get for ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET with the case's product group and the business date. Remove any product group code, period or band written in their code; the done condition is that a search of the recovery module finds no product group code literal outside test fixtures and the generated API types. Where the call throws MissingProductParameterException, place the case in the exception queue and name the gap with MSG-P3-034, which is exception path X5 and AC7.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications\Recovery Workbench Functional Specifications by 
... truncated (6,375 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "servicelevel.required-statuses|ENTRY_DPD|EXPOSURE_BAND_SET", "include": "*.md", "limit": 30}
```

```text
Found 30 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 2355: The build does this, not a developer by hand. ParameterKeysGenerator reads config/parameter-catalog.csv and writes the ParameterKeys class, giving each catalog line a typed constant such as ParameterKeys.CASE_ENTRY_DPD of type ParameterKey<Integer>. Application code then reads a value only through ParameterService.get with one of those constants and a business date. Because the constants are generated, a key the catalog does not list will not compile, and the type on the key stops an integer parameter being read as text. Wire the generator into the build so the class is written again whenever the catalog file changes.

  Line 2517: A person does this, the center of excellence analyst holding Reference data C. Nothing is built here and no screen exists in this story. The analyst prepares two files: a PRODUCT_PARAMETER load with one row for each product group and parameter code, and a SERVICE_LEVEL load with one row for each product group and case status. BR2 names the parameters each product must carry, those the catalog of RWB-E1-042 marks with scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. The values themselves belong to the product heads, with entry at 90 days from DL16, service levels from DL22 and caps from DL23.

  Line 2527: **In the story.** Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.

  Line 2529: This runs on its own once the file is loaded. The checks of RWB-E1-043 run first, then the new one you build as ProductCompletenessCheck, added as a table check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL. It confirms that every product in the PRODUCT version in force on the valid from date has a row for each catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for each status in the parameter servicelevel.required-statuses. A missing row refuses the whole load, with MSG-P3-034 naming the product and the item, and the version already in force stays in force. AC3 names SSME and WAITING_PARTNER.

  Line 2553: You change t
... truncated (9,525 chars total)
```

### Assistant - 2026-11-16 14:03 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

There's a "Recovery Workbench Build Notes Epic 1 v4.md" with a section on E1-045, which is a developer-oriented build guide. Let me read the E1-045 section (lines ~2500-2600) to extract implementation guidance. That will make the briefing much more concrete.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md", "offset": 2490, "limit": 130}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md, lines 2490-2619
2490: 
2491: ### Step 5
2492: 
2493: **In the story.** Deployment: on service start, Flyway applies each pending migration once, in version order, and writes its checksum to the history table.
2494: 
2495: Flyway does this inside the service as it starts, with no pipeline step and no person. Configure it with RecoveryFlywayConfig and the properties in section 12, including spring.flyway.table set to flyway_schema_history_recovery, so the recovery module keeps its own history and its version numbers cannot collide with the ACE and collection modules. Pending means present in the repository and not yet in this database. Flyway applies those migrations lowest version first and writes one history row per migration with its version and its checksum, a number computed from the file content. Out of order is off, so a version below the newest applied one is refused.
2496: 
2497: ### Step 6
2498: 
2499: **In the story.** Deployment: Flyway validates the checksums of applied migrations; a changed file stops the start.
2500: 
2501: Also automatic, and it happens before anything is applied, because validate-on-migrate is true. Flyway recomputes the checksum of each file that has a history row and compares it with the stored one. A file edited after it ran gives a different number, so validation fails with MSG-P3-016 naming the version and the service does not start, as AC4 describes with checksum 104553219 changed to 88120477. An applied migration is never edited. A mistake in one is corrected by adding a new migration that puts it right. PROD runs forward only: clean is disabled in every profile and an undo file is refused by the lint.
2502: 
2503: ### Step 7
2504: 
2505: **In the story.** Platform administrator: reads the migration run on SCR-44 Interface and job monitor.
2506: 
2507: A person reads the result here. Build MigrationRunRecorder to write one job record per migration run through the P1 job monitor interface, which is what gives SCR-44 something to show. The administrator then sees each run with its version, its checksum and its drift result, in state running, failed or complete, and the same data comes back from GET /api/recovery/v1/admin/jobs with type MIGRATION. Reading it needs Platform administration right R, and a role without that right is refused with MSG-P4-002. MSG-P3-016 belongs in the pipeli
... truncated (17,441 chars total)
```

### Assistant - 2026-11-16 14:03 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Excellent — the Build Notes give implementation-level guidance. I now have everything to write a strong developer briefing for E1-045, including the build steps. I should incorporate specifics: DueDateCalculator, ProductCompletenessCheck as a table check in the E1-043 registry, OpenCaseCounter, MissingProductParameterException, versionNo propagation, idempotency by hash, approval timing, feature flag.

Also the clarification pack has the parameter catalog entries. Let me look at lines 160-190 of the clarification pack to see exact catalog rows for E1-045 params (scope, required, owner, default, version). This could be useful.

</details>

**Tool `read`** - completed

```json
{"limit": 45, "offset": 150, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\RWB-E1-042 Clarification Pack.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md, lines 150-194
150: | `parameter_value` | Environment, status and date checks | LOV-ENVIRONMENT, LOV-VERSION-STATUS, no end before start. |
151: | `parameter_value` | `version_no >= 1` | Version 1 is the seed; the first human load starts at version 2. |
152: | `parameter_value` | Approver is never the author | BR4 maker-checker, enforced even if the service check is bypassed. |
153: | `parameter_value` | An `APPROVED` or `IN_FORCE` row has `approved_at` | No approved row without an approval timestamp. |
154: | `parameter_value` | Foreign key to `parameter_catalog.param_key` | A runtime load cannot invent a key. |
155: | `parameter_value` | **NULL-safe** unique `(param_key, environment, product_group, version_no)` | The baseline unique constraint treats NULL `product_group` as distinct; the expression index closes that hole. |
156: | `parameter_value` | One approved version per key, environment, product group and `valid_from` | The database guard behind the 409 rule. |
157: | `parameter_value` | Lookup indexes for the story read | `(param_key, environment, valid_from)` and the product-group lookup. |
158: 
159: **Deliberately not in the database:** the min/max range check. `min_value` and `max_value` are text and their meaning depends on `value_type` (INTEGER, DECIMAL, DATE, TIME, CODE_LIST, JSON). A single SQL `CHECK` cannot parse all of them safely. `ParameterLoadChecks` performs the typed range check and refuses the whole load with MSG-GEN-002. The database enforces the structural rules; the service enforces the typed rules.
160: 
161: ### 2.5 Seed scope: what is in `V042_2`, and what is not
162: 
163: The seed contains **13 catalog rows** and **28 value rows** (7 keys × 4 environments).
164: 
165: | Key | Scope | Default | Value rows | Owner | Source |
166: |---|---|---|---|---|---|
167: | `case.entry.dpd` | GLOBAL | `90` | 4 | RW-COE | E1-042 §3, AC1, DL16 |
168: | `refdata.cache.ttl-seconds` | GLOBAL | `300` | 4 | RW-PLATADM | E1-042 §3, AC8, DL11 |
169: | `config.cache.ttl-seconds` | GLOBAL | `60` | 4 | RW-PLATADM | E1-042 §13, assumed DL11 |
170: | `caselist.export.maxrows` | GLOBAL | `10000` | 4 | RW-COE | E1-042 §3, assumed DL11 |
171: | `ace.db.password` | GLOBAL | none (secret) | 0 | RW-PLATADM | E1-042 AC9, DL26 |
172: | `recon.caselist.tolerance.pct` | GLOBAL | `0.00` | 4 | RW-COE | E1-002 §3, assume
... truncated (4,394 chars total)
```

### Assistant - 2026-11-16 14:03 | opencode-go/deepseek-v4.1-flash | build

## RWB-E1-045 — Multi-product parameters for Mortgage, HP and SSME

Same treatment as the TE stories. Short version: **it turns the differences between products into versioned reference data**, so adding or changing a product is a data load and an approval, not a code release.

Today, Mortgage, hire purchase and SSME have different notice periods, service levels, entry thresholds and exposure bands, and those differences live in team procedures or constants. After this story, every one of those values is a `PRODUCT_PARAMETER` or `SERVICE_LEVEL` row keyed by product group, and the engines read them through one service.

```openui-lang
root = Stack([flow, params])
flow = Steps([{title: "1. Prepare", markdown: "COE analyst prepares the PRODUCT_PARAMETER file (one row per product group and parameter) and the SERVICE_LEVEL file (one row per product group and status)."}, {title: "2. Load", markdown: "Reference data administrator posts the file to POST /admin/reference-loads with the table code and a valid-from date. One table per request."}, {title: "3. Structural checks", markdown: "RWB-E1-043's version checks run first: required columns, duplicate keys, idempotency by content hash."}, {title: "4. Product completeness", markdown: "ProductCompletenessCheck: every product in force needs every catalog parameter marked scope PRODUCT and required, plus a SERVICE_LEVEL row for every required status. A miss refuses the whole load."}, {title: "5. Type and range", markdown: "Each value checked against the catalog's type and range. Duplicates and removing a product with open cases also refuse the load."}, {title: "6. Approve", markdown: "A second person approves. The version stays unused until then, and takes effect on its valid-from date, not the approval date."}, {title: "7. Read at run time", markdown: "Engines call ProductParameterService with the business date and get the row in force, including its version number."}], "column")
params = Table(["Row or key", "What it holds", "Who reads it"], [["PRODUCT", "The product groups in force", "Completeness check; case creation via LOV-PRODUCT"], ["ENTRY_DPD", "Days past due at which recovery starts", "CaseEntryService (E1-018)"], ["EXCLUSION_LIST", "Products or segments that must not enter recovery", "CaseEntryService (E1-018)"], ["NOTICE_PERIOD_DAYS", "Notice period before the next step", "TimerEngine (E1-028)"], ["CURE_PERIOD_DAYS", "Cure window after notice", "TimerEngine (E1-028)"], ["EXPOSURE_BAND_SET", "Exposure bands used for allocation", "AllocationService (E1-020)"], ["SERVICE_LEVEL", "Limit, unit, warn percent and escalation role per product and case status", "SLA and escalation (E1-028)"]])
```

## The load pipeline in detail

**It is a reference-load pipeline, not a form.** The endpoint already exists from E1-043: `POST /api/recovery/v1/admin/reference-loads`, multipart form data with `file`, `table` (PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL) and `validFrom`. This story adds the product-specific checks behind it and the approval gate.

**The completeness check is cross-table, and it is the heart of the story.** For every product in the PRODUCT version in force on the valid-from date, there must be:

- a `PRODUCT_PARAMETER` row for every catalog parameter with `scope = PRODUCT` and `required = yes` — currently `ENTRY_DPD`, `EXCLUSION_LIST`, `NOTICE_PERIOD_DAYS`, `CURE_PERIOD_DAYS`, `EXPOSURE_BAND_SET`;
- a `SERVICE_LEVEL` row for every status in the GLOBAL parameter `servicelevel.required-statuses`.

That is why a file can have 50 valid rows and still be refused: the check is product-by-required-item coverage, not row syntax. AC3 is exactly this — one missing `SSME` / `WAITING_PARTNER` row refuses the SERVICE_LEVEL load and version 3 stays in force.

**Refusal is total.** A missing row, an out-of-range value, a duplicate key, or a PRODUCT load that drops a product with open cases all reject the whole file. Nothing is partially applied, and the version in force is untouched. The `MSG-P3-027` text even says "Version {version} stays in force."

**The range check is typed, not a SQL constraint.** From the E1-042 pack: `min_value` and `max_value` are text and their meaning depends on `value_type` (INTEGER, DECIMAL, DATE, TIME, CODE_LIST, JSON), so a single SQL `CHECK` cannot do it. `ProductCompletenessCheck` / the load checks do the typed comparison and refuse with `MSG-GEN-002` naming the field and both ends of the range. AC4 is `NOTICE_PERIOD_DAYS` 0 against 1–365.

**Approval is a separate, second-person act.** A validated version sits unused until an approver with the approve right in Reference data signs it. Where a limit or threshold moves, that is the risk and model risk officer. Effective dating is on `validFrom`, not the approval timestamp — which is what lets AC2 add AUTO_LEASE on 5 December with no deployment and no release window.

**Idempotency comes from E1-043:** same table code, same valid-from and same content hash is one load, not two.

## The runtime path

The published interface is the only way engines read these values:

```java
public interface ProductParameterService {
    ProductParameter get(String productGroup, String parameterCode, LocalDate businessDate);
    ServiceLevel serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);
}
```

Both throw `MissingProductParameterException(productGroup, parameterCode, businessDate)` when no row is in force. There is **no default**. A missing value does not become "30 days"; the timer is not written, the case goes to the exception queue, and the gap is named (`MSG-P3-034`, AC7).

For a notice timer: take `NOTICE_PERIOD_DAYS` for the case's product group on the business date, pass the value and unit to `DueDateCalculator`, and write `timer.expires_at`. `CALENDAR_DAYS` adds days straight; `WORKING_DAYS` skips the dates in `v_ace_holiday` (BR7). `warn_at` and escalation stay with the timer engine, E1-028.

Two timing rules that cause most of the defects if missed:

- **A running timer is never recalculated.** AC8: the Mortgage timer that started on 1 December still expires 31 December after the value moves to 45 days on 3 December. The new 45 only applies to timers that start on or after 3 December.
- **The version number returned at lookup time travels into the decision log inputs.** Don't re-read it later — AC1 checks that each timer start records `PRODUCT_PARAMETER` version 2.

Case creation and allocation use the same service for `ENTRY_DPD`, `EXCLUSION_LIST` and `EXPOSURE_BAND_SET`. The `MissingProductParameterException` path is the same: exception queue, not a crash and not a fallback.

## What the acceptance criteria prove

| AC | What it demonstrates |
|---|---|
| AC1 | 30 days for Mortgage vs 60 for HP produces 31 Dec vs 30 Jan, and each timer records version 2 |
| AC2 | A new product, AUTO_LEASE, is live on 5 Dec with no deployment |
| AC3 | A missing SERVICE_LEVEL row refuses the load and leaves version 3 in force |
| AC4 | A value of 0 against range 1–365 is refused with the range named |
| AC5 | Two rows for MORTGAGE + NOTICE_PERIOD_DAYS refuse the load |
| AC6 | Removing UNSECURED with 3 open cases is refused, naming the product and the count |
| AC7 | No row in force at run time means no timer and an exception-queue entry |
| AC8 | A value change does not move a running timer, only new ones |

The access test, TC-E1-045-09, is separate: `RW-PHONECOL` holds Reference data R only, tries to load, and gets 403 `MSG-P4-002`.

## What the team actually builds

- `DueDateCalculator` — calendar vs working days, with a year-end and holiday-row unit test.
- `ProductParameterServiceImpl` over `ReferenceDataService`, plus `MissingProductParameterException`.
- `ProductCompletenessCheck` — registered as a table check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL in the E1-043 registry.
- `OpenCaseCounter` — counts open cases by product group (`status != CLOSED`), served by `ix_case_status_queue`.
- Changes to `TimerEngine` (E1-028), `CaseEntryService` (E1-018) and `AllocationService` (E1-020) to read through the service and remove product constants.
- The X5 path — missing parameter goes to the exception queue with `MSG-P3-034`.
- Feature flag `rwb.p3.product-parameters`; off means the engines use the values they read before this story.

**Done when** the tests pass **and** a search of the recovery module finds no product group code literal outside test fixtures and generated API types. That second condition is the real measure: if `MORTGAGE` or `30` is still in Java, a new product still needs a developer.

## Gotchas worth saying out loud

- **No new table and no screen in this story.** The product parameter screens are Epic 8 (SCR-39/42). Epic 1 exposes the API and the load; don't build an admin UI here.
- **Product group is a string checked against LOV-PRODUCT, not a Java enum.** The generated API types keep it a string. An enum reintroduces the deployment this story is meant to remove.
- **Atomic loads.** Do not "apply the good rows". A refused version leaves the previous one in force.
- **Effective dating is by business date at the moment of the call**, not the case creation date and not today's date. Same lookup, different answer on either side of a valid-from date.
- **Unit handling is part of the value.** A number without its unit is meaningless; `WORKING_DAYS` and `CALENDAR_DAYS` produce different dates. Validate the unit against the catalog, not just the range.
- **Loader and approver are different people.** That is a control, not a UX preference.
- **The flag is not a rollout plan.** Reference data must be loaded and approved for every product before it is switched on, or the first morning produces a queue full of `MissingProductParameterException`.

## Open decisions to settle before or at grooming

1. **Parameter naming conflict (OI-E1-042-006).** The catalog seed carries `case.entry.dpd` as GLOBAL with default 90, and E1-045 expects `ENTRY_DPD` as PRODUCT. `case.entry.dpd_threshold` also appears elsewhere. Two keys for one concept means the completeness check can pass while the engine reads the other one. Pick one key before code.
2. **The three parameter sets and effective dating.** The grooming note asks for confirmation of the Mortgage / HP / SSME values and their valid-from dates. Those are business values (DL16, DL22, DL23), not developer choices.
3. **`servicelevel.required-statuses`.** The story assumes six statuses: NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL. Confirm against DL22, because that list drives every SERVICE_LEVEL load.
4. **New-product load sequencing.** A new product needs three separate loads with the same valid-from. The completeness check for the PRODUCT_PARAMETER load needs the PRODUCT version that contains the new product. Does it see a pending PRODUCT version for that date, or must PRODUCT be approved first? AC2 says all three end up approved, but not in what order.
5. **E1-028 sequencing.** The grooming plan lists E1-028 as blocked by E1-045, while the story treats the timer engine as existing and changed here. Agree the build order: stand up `ProductParameterService` first, then switch the timer engine onto it.
6. **Flag removal date and rollout owner.** `rwb.p3.product-parameters` needs an owner, a backfill step and a removal date under E1-047, or it becomes permanent.

Out of scope, so nobody builds it by accident: per-product letter templates (P6), treatment bands and floors (Epic 8), delegation limits (E1-038), and the timer engine's warning and escalation behaviour itself (E1-028).

<details><summary>Reasoning</summary>

Very useful. Note the naming conflict: the catalog uses `case.entry.dpd` (GLOBAL) in E1-042 seed, while E1-045 expects `ENTRY_DPD` (PRODUCT). The clarification pack flags OI-E1-042-006: parameter naming conflicts `case.entry.dpd` vs `case.entry.dpd_threshold` vs `ENTRY_DPD`. This is a major integration risk for E1-045: the catalog seed has `ENTRY_DPD` PRODUCT with no values, but also `case.entry.dpd` GLOBAL default 90. Two keys for one concept. E1-045's BR2 says ENTRY_DPD. The open issue says one approved key per concept. This is a genuinely important thing to flag to developers. I should include it prominently as an open decision.

Also `servicelevel.required-statuses` is GLOBAL, six statuses, default present, owner RW-COE. Good.

So in the briefing, open issues:
- OI-E1-042-006 naming conflict: `ENTRY_DPD` vs `case.entry.dpd` vs `case.entry.dpd_threshold`. Must resolve before code reads one.
- `servicelevel.required-statuses` default is "six statuses" — assumed DL22, not confirmed values.
- The three product parameter sets and effective dating (grooming note).
- Pending-version visibility / load sequencing for a new product.
- Catalog entries for the five PRODUCT params are seeded with no values by design (E1-042 seed). Good — that's not an issue, but confirms E1-045 must load values.
- Product-scope rows carry no values in the parameter_value table; values are PRODUCT_PARAMETER rows via ProductParameterService. That's the design.

I should mention the E1-042 clarification pack as the source of the catalog state, because the developer briefing benefits from "the catalog already has the five PRODUCT keys with no values; you populate PRODUCT_PARAMETER".

Wait, the seed table lines 175-179 says `ENTRY_DPD` scope PRODUCT, no default, 0 value rows. And line 167 says `case.entry.dpd` GLOBAL 90, 4 value rows. So both exist in the seed — exactly the conflict. OI-E1-042-006 says one approved key per concept. This is a real blocker to decide: does E1-045 read `ENTRY_DPD` (PRODUCT) or `case.entry.dpd` (GLOBAL)? The story says ENTRY_DPD. The catalog has both. If the code uses ENTRY_DPD while existing behavior uses case.entry.dpd, there will be two sources of truth. Flag it.

Also exposure bands: `EXPOSURE_BAND_SET` value likely JSON; type CODE_LIST/JSON. The catalog type check must handle it. Fine.

Let me also check if E1-045 has a "Story Updates" or migration note. Search "E1-045" in E1-042 Clarification Pack and Build Notes — done. The build notes are v4, stories

_[truncated]_

</details>

### User - 2026-11-16 14:19

in this tell me where product paramters seed data is and where the schema is and then how does this story connects to it

### Assistant - 2026-11-16 14:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The user asks: in E1-045, where is the product parameters seed data, where is the schema, and how does the story connect to it.

I need to be accurate and concrete, citing actual paths in the repo. Let me investigate:

1. Seed data for product parameters: E1-042 clarification pack says the seed contains 13 catalog rows and 28 value rows, generated by `tools/Generate-ParameterSeed.ps1`. The product-scope rows carry no values by design. E1-045's PRODUCT_PARAMETER and SERVICE_LEVEL values are reference data loads, not seed. So "product parameters seed data" could mean:
   - The parameter catalog seed: `ENTRY_DPD`, `EXCLUSION_LIST`, `NOTICE_PERIOD_DAYS`, `CURE_PERIOD_DAYS`, `EXPOSURE_BAND_SET`, `servicelevel.required-statuses` — in E1-042's seed.
   - The product parameter values (PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL rows) — not seeded; loaded through reference loads.
   
   The clarification pack mentions `config/parameter-catalog.csv` as the source of truth and `V042_2` seed. Let me find actual files. Search for `Generate-ParameterSeed.ps1`, `parameter-catalog.csv`, `V042_2`, `product_parameter`, `service_level` migrations in the repo.

2. Schema: `reference_version`, `reference_row`, `parameter_catalog`, `parameter_value` from E1-042/E1-043 migrations. E1-045 says no new table. Need exact migration file names and DDL. Search for `V042`, `V043`, `reference_row`, `parameter_catalog` in SQL files.

Let me explore the repo structure: there's "ACE schema" folder, "06 Data", E1-042 Migration and Clarifications, 17 AI-First SDLC Repository v2 output with implementation. Search for SQL migration files.

Let me use glob/grep efficiently.

Search for `parameter_catalog` in *.sql, and `reference_row` in *.sql. Also `Generate-ParameterSeed`.

</details>

**Tool `glob`** - completed

```json
{"pattern": "**/*.sql", "limit": 200}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\15 ACE DB Alignment\ACE Schema PostgreSQL v1.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\views_B.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\views_A.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\v5_views_tail.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\grant_tests.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\grants.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\checks3.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\checks2.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\verify\schema\checks.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v5.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V042_2__parameter_seed.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V042_1__parameter_catalog.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\e1-042-migration-and-clarifications\v042-2-parameter-seed.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\e1-042-migration-and-clarifications\v042-1-parameter-catalog.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\e1-042-migration-and-clarifications\v0042-rwb-e1-042-parameter-catalog-and-seed.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\sql\views_section_a.sql
C:\Users\SahilMor
... truncated (6,081 chars total)
```

**Tool `glob`** - completed

```json
{"pattern": "**/*parameter*", "limit": 100}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V042_2__parameter_seed.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V042_1__parameter_catalog.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\config\parameter-catalog.csv
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 044 Database migrations versioned with parameterized schema names v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 042 Central configuration service and parameter catalog v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 044 Database migrations versioned with parameterized schema names v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 042 Central configuration service and parameter catalog v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 044 Database migrations versioned with parameterized schema names v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 042 Central configuration service and parameter catalog v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set 
... truncated (8,644 chars total)
```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now let's read the key files:
- `E1-042 Migration and Clarifications/config/parameter-catalog.csv` (catalog seed source)
- `E1-042 Migration and Clarifications/sql/V042_1__parameter_catalog.sql` (schema for parameter_catalog, parameter_value?)
- `E1-042 Migration and Clarifications/sql/V042_2__parameter_seed.sql` (seed values)
- E1-043 schema: search for reference_version/reference_row. Maybe in physical schema v6. Let's grep.

Also, is there a schema for PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL? E1-045 says no new table; those are reference tables (table_code rows) in reference_row? Let's check the reference data model. Search `reference_row` in SQL.

Let me read the catalog SQL and seed SQL, plus grep for reference_row.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\sql\\V042_1__parameter_catalog.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V042_1__parameter_catalog.sql, lines 1-337
1: -- Story: RWB-E1-042
2: -- Migration: parameter catalog and parameter value tables
3: -- Schema: ${recoverySchema}
4: --
5: -- REVIEW COPY. The requested names V042_1__parameter_catalog.sql and
6: -- V042_2__parameter_seed.sql do not satisfy D-RCV-28, which requires one migration per
7: -- story named V<seq>__<story>_<name>.sql. Commit the consolidated
8: -- V0042__rwb_e1_042_parameter_catalog_and_seed.sql unless a migration-lint exception is
9: -- approved for the split. See section 2 of the clarification pack.
10: --
11: -- Definition source: Recovery Workbench Physical Schema v4.sql, parameter_catalog and
12: -- parameter_value. Parameter keys are the business names; no key is a table name.
13: --
14: -- Baseline note. RWB-E1-001 V0001__rwb_e1_001_recovery_schema.sql is written from the
15: -- Physical Schema and already creates both tables. This file is therefore guarded: it
16: -- creates what is absent and then adds the E1-042 constraints, foreign key, uniqueness
17: -- rules and indexes only when they are absent. On a schema built without the baseline it
18: -- creates the complete E1-042 definition. The drift check remains the control that an
19: -- environment matches the migrations.
20: 
21: CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_catalog (
22:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
23:     param_key varchar(100) NOT NULL,
24:     kind varchar(15) NOT NULL,
25:     value_type varchar(15) NOT NULL,
26:     unit varchar(20),
27:     min_value varchar(40),
28:     max_value varchar(40),
29:     default_value varchar(400),
30:     scope varchar(10) NOT NULL DEFAULT 'GLOBAL',
31:     required boolean NOT NULL DEFAULT false,
32:     owner_role varchar(20) NOT NULL,
33:     environments varchar(40),
34:     used_by varchar(400),
35:     secret boolean NOT NULL DEFAULT false,
36:     description varchar(400) NOT NULL,
37:     is_active boolean NOT NULL DEFAULT true,
38:     state varchar(40),
39:     version integer NOT NULL DEFAULT 1,
40:     created_at timestamptz NOT NULL DEFAULT now(),
41:     created_by uuid,
42:     updated_at timestamptz NOT NULL DEFAULT now(),
43:     updated_by uuid,
44:     CONSTRAINT uk_parameter_catalog UNIQUE (param_key),
45:     CONSTRAINT ck_parameter_catalog_scope CHECK (scope IN ('GLOBAL', 'PRODUCT')),
46:     CONSTRAINT ck_parameter_
... truncated (17,118 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\config\\parameter-catalog.csv"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\config\parameter-catalog.csv, lines 1-14
1: key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,description
2: case.entry.dpd,BUSINESS,INTEGER,CALENDAR_DAYS,1,365,90,GLOBAL,true,RW-COE,"DEV,SIT,UAT,PROD",recovery.casewf.casecreation,false,"Days past due at which an account enters recovery (DL16)."
3: refdata.cache.ttl-seconds,ENVIRONMENT,INTEGER,SECONDS,,,300,GLOBAL,true,RW-PLATADM,"DEV,SIT,UAT,PROD",recovery.casewf.refdata,false,"Time to live of the reference data row cache, in seconds (DL11)."
4: config.cache.ttl-seconds,ENVIRONMENT,INTEGER,SECONDS,,,60,GLOBAL,false,RW-PLATADM,"DEV,SIT,UAT,PROD",recovery.casewf.config,false,"Time to live of the configuration service cache, in seconds (DL11, assumed)."
5: caselist.export.maxrows,BUSINESS,INTEGER,COUNT,,,10000,GLOBAL,false,RW-COE,"DEV,SIT,UAT,PROD",recovery.casewf.caselist,false,"Maximum rows returned by the case list export (DL11, assumed)."
6: ace.db.password,ENVIRONMENT,STRING,,,,,GLOBAL,false,RW-PLATADM,"DEV,SIT,UAT,PROD",ACE common module,true,"ACE database password; the value is held only in the ACE secret store (DL26)."
7: recon.caselist.tolerance.pct,BUSINESS,DECIMAL,PERCENT,,,0.00,GLOBAL,false,RW-COE,"DEV,SIT,UAT,PROD",recovery.dataengine.caselist,false,"Tolerance for the case-list count reconciliation REC-01 (DL25, assumed)."
8: caselist.allocation.wait.until,BUSINESS,TIME,TIME_OF_DAY,,,07:15,GLOBAL,false,RW-COE,"DEV,SIT,UAT,PROD",recovery.casewf.caselist,false,"Time by which allocation must be complete before the case list is built."
9: servicelevel.required-statuses,BUSINESS,CODE_LIST,,,,"NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL",GLOBAL,true,RW-COE,"DEV,SIT,UAT,PROD",recovery.casewf.refdata.product,false,"Case statuses for which every product in force must have a SERVICE_LEVEL row (DL22, assumed)."
10: ENTRY_DPD,BUSINESS,INTEGER,DAYS,,,,PRODUCT,true,RW-PRODHEAD,"DEV,SIT,UAT,PROD","recovery.casewf.casecreation, recovery.casewf.allocation",false,"Per-product entry threshold, in days past due; the values are PRODUCT_PARAMETER rows (RWB-E1-045)."
11: EXCLUSION_LIST,BUSINESS,CODE_LIST,,,,,PRODUCT,true,RW-PRODHEAD,"DEV,SIT,UAT,PROD","recovery.casewf.casecreation, recovery.casewf.allocation",false,"Per-product exclusion list code; the values are PRODUCT_PARAMETER rows (RWB-E1-045)."
12: NOTICE_PER
... truncated (3,117 chars total)
```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now, where are PRODUCT / PRODUCT_PARAMETER / SERVICE_LEVEL defined? E1-045 says no new table; but the reference data model E1-043 has reference_version and reference_row. Let me check the physical schema and E1-043 story. Search for `reference_row` and `reference_version` in schema v6.

Also, there's a conflict: E1-042's `parameter_catalog`/`parameter_value` design (product_group column) vs E1-043's versioned reference tables (`reference_version`, `reference_row`) and E1-045's PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL. That's a significant architecture question: are product parameters stored in `parameter_value` (per E1-042) or in `reference_row` (per E1-043/E1-045)? The E1-042 clarification pack says "Product-scope rows carry no values by design. Their values are PRODUCT_PARAMETER rows read through ProductParameterService (E1-045), not parameter_value rows." So the resolution is: product parameter values are NOT in parameter_value; they are reference data rows (PRODUCT_PARAMETER). But the parameter_catalog defines them. Good — that's the linkage.

Where exactly are PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL stored? Probably as `reference_row` rows in versioned reference tables, with `table_code` = PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL. Let me check E1-043 story and physical schema. Search for "PRODUCT_PARAMETER" in the schema and E1-043 docs.

</details>

**Tool `grep`** - completed

```json
{"pattern": "PRODUCT_PARAMETER|SERVICE_LEVEL|reference_row|reference_version", "include": "*.sql", "limit": 60}
```

```text
Found 60 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 1058:     reference_version_id uuid,

  Line 1437: CREATE TABLE reference_version (

  Line 1467:     CONSTRAINT uk_reference_version UNIQUE (table_code, version_no)

  Line 1471: CREATE TABLE reference_row (

  Line 1483:     CONSTRAINT uk_reference_row UNIQUE (row_key)

  Line 1584:     reference_version_id uuid,

  Line 1607:     reference_version_id uuid,

  Line 1647:     reference_version_id uuid,

  Line 2228: ALTER TABLE retention_rule ADD CONSTRAINT fk_retention_rule_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;

  Line 2242: ALTER TABLE reference_row ADD CONSTRAINT fk_reference_row_version_id FOREIGN KEY (version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;

  Line 2244: ALTER TABLE document_type ADD CONSTRAINT fk_document_type_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;

  Line 2245: ALTER TABLE document_checklist_item ADD CONSTRAINT fk_document_checklist_item_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;

  Line 2248: ALTER TABLE document_hub_parameter ADD CONSTRAINT fk_document_hub_parameter_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;

  Line 2334: CREATE INDEX ix_retention_rule_reference_version_id ON retention_rule (reference_version_id);

  Line 2347: CREATE INDEX ix_reference_row_version_id ON reference_row (version_id);

  Line 2349: CREATE INDEX ix_document_type_reference_version_id ON document_type (reference_version_id);

  Line 2350: CREATE INDEX ix_document_checklist_item_reference_version_id ON document_checklist_item (reference_version_id);

  Line 2353: CREATE INDEX ix_document_hub_parameter_reference_version_id ON document_hub_parameter (reference_version_id);

  Line 2426: COMMENT ON TABLE reference_row IS 'One row of a reference table version held as data.';

  Line 2427: COMMENT ON TABLE reference_version IS 'One version of a reference or rule table, with its author, approver, checks and change checklist.';

  Line 3016: COMMENT ON COLUMN retention_rule.reference_version_id IS 'Reference version that brought the row';

  Line 3179: COMMENT ON COLUMN reference_version.id IS 'Record identifier of the 
... truncated (9,531 chars total)
```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -File \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\" -Filter \"*E1 043*\" | Select-Object Name, Length"}
```

```text

Name                                                          Length
----                                                          ------
RWB E1 043 Reference data service with versioned tables v2.md  26475



```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read the reference_version and reference_row DDL in physical schema v6 (lines 1437-1490), and the E1-043 story's data/solution plan sections to understand how PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL are represented.

Also check if there's a DDL for PRODUCT / PRODUCT_PARAMETER / SERVICE_LEVEL anywhere. Grep in markdown/sql for `CREATE TABLE product` etc. Perhaps E1-043 story defines table codes and row keys. Let me grep "PRODUCT_PARAMETER" in md.

</details>

**Tool `read`** - completed

```json
{"limit": 60, "offset": 1437, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 1437-1496
1437: CREATE TABLE reference_version (
1438:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1439:     table_code varchar(30) NOT NULL,
1440:     version_no integer NOT NULL,
1441:     version_label varchar(20),
1442:     valid_from date NOT NULL,
1443:     valid_to date,
1444:     status varchar(15) NOT NULL DEFAULT 'VALIDATED',
1445:     author_user_id uuid NOT NULL,
1446:     approver_user_id uuid,
1447:     approved_at timestamptz,
1448:     row_count integer NOT NULL,
1449:     content_hash char(64) NOT NULL,
1450:     load_id uuid NOT NULL,
1451:     dry_run_counts jsonb,
1452:     rollback_reason varchar(400),
1453:     change_request_ref varchar(30),
1454:     impact_summary varchar(1000),
1455:     test_result varchar(10),
1456:     rollback_plan varchar(1000),
1457:     verified_by uuid,
1458:     verified_at timestamptz,
1459:     verify_note varchar(1000),
1460:     is_active boolean NOT NULL DEFAULT true,
1461:     state varchar(40),
1462:     version integer NOT NULL DEFAULT 1,
1463:     created_at timestamptz NOT NULL DEFAULT now(),
1464:     created_by uuid,
1465:     updated_at timestamptz NOT NULL DEFAULT now(),
1466:     updated_by uuid,
1467:     CONSTRAINT uk_reference_version UNIQUE (table_code, version_no)
1468: );
1469: 
1470: -- Reference row: One row of a reference table version held as data.
1471: CREATE TABLE reference_row (
1472:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1473:     version_id uuid NOT NULL,
1474:     row_key varchar(200) NOT NULL,
1475:     row_data jsonb NOT NULL,
1476:     is_active boolean NOT NULL DEFAULT true,
1477:     state varchar(40),
1478:     version integer NOT NULL DEFAULT 1,
1479:     created_at timestamptz NOT NULL DEFAULT now(),
1480:     created_by uuid,
1481:     updated_at timestamptz NOT NULL DEFAULT now(),
1482:     updated_by uuid,
1483:     CONSTRAINT uk_reference_row UNIQUE (row_key)
1484: );
1485: 
1486: -- Rule test case: A test case of the rule table test harness, with its expected and actual result.
1487: CREATE TABLE rule_test_case (
1488:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
1489:     test_case_id varchar(20) NOT NULL,
1490:     route_set varchar(15) NOT NULL,
1491:     rule_version varchar(20) NOT NULL,
1492:     rule_id varchar(20) NOT NULL,
1493:     package_version_id uuid,
1494:     from_state varchar(60) NOT N
... truncated (2,634 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "PRODUCT_PARAMETER|SERVICE_LEVEL|PRODUCT version|table_code", "include": "RWB E1 043 Reference data service with versioned tables v2.md", "limit": 60}
```

```text
Found 7 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 043 Reference data service with versioned tables v2.md:
  Line 103:     Given approved versions are in force for "QUEUE" version 7 and "SERVICE_LEVEL" version 2, and v_ace_holiday holds the Bank of Thailand calendar

  Line 110:     Given a "SERVICE_LEVEL" load file whose row 12 has the text "five" in the column "limit_days"

  Line 156: | BR1 | The reference tables served are PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD and PRODUCT_PARAMETER. The list is data and changes by a load of LOV-REF-TABLE. Rule tables are not reference tables and have no code in LOV-REF-TABLE. The holiday calendar is not among them; it is read from v_ace_holiday | Principle 1; REQ-DRI-011; refdata.txt Reference tables; RWB-E1-069 |

  Line 195: | DF-REF-160 | reference_version | table_code | Write |

  Line 287: - `reference_version`: `id uuid PK`, `table_code varchar(30) NOT NULL`, `version_no integer NOT NULL`, `valid_from date NOT NULL`, `valid_to date`, `status varchar(15) NOT NULL`, `author_user_id uuid NOT NULL`, `approver_user_id uuid`, `approved_at timestamptz`, `row_count integer NOT NULL`, `content_hash char(64) NOT NULL`, `load_id uuid NOT NULL`, plus the seven standard columns. Constraints: `UNIQUE (table_code, version_no)`; `UNIQUE (table_code, valid_from, content_hash)`; `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`; partial unique index on `(table_code, valid_from) WHERE status = 'APPROVED'`.

  Line 331: | TC-E1-043-03 | AC3, BR7 | System | QUEUE v7, SERVICE_LEVEL v2 and v_ace_holiday; captured log lines |

  Line 332: | TC-E1-043-04 | AC4, BR5 | System | SERVICE_LEVEL file with a text value in row 12 |

```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now let's read E1-043 story's solution plan to see the table handler / row handlers and how PRODUCT_PARAMETER rows are stored. Lines 270-340 maybe.

</details>

**Tool `read`** - completed

```json
{"limit": 90, "offset": 270, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB E1 043 Reference data service with versioned tables v2.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 043 Reference data service with versioned tables v2.md, lines 270-359
270: **Package.** `recovery.casewf.refdata` in the recovery module; folder `recovery/casewf/refdata`. Published types in `recovery.casewf.refdata.api`.
271: 
272: **Components**
273: 
274: | Component | Type | Responsibility |
275: |---|---|---|
276: | ReferenceVersionRegistryImpl | Service | Runs the load checks, numbers the version, writes the version and its rows, approves |
277: | ReferenceDataServiceImpl | Service | Resolves the version in force for a date; serves rows from the cache |
278: | ReferenceRowCache | Service | In-memory cache keyed by table code and business date; entry time to live from `refdata.cache.ttl-seconds` |
279: | ReferenceVersionRepository | Repository | Reads and writes `reference_version` |
280: | ReferenceRowRepository | Repository | Reads and writes `reference_row` |
281: | ReferenceVersionEntity, ReferenceRowEntity | Entity | JPA mappings of the two tables, with the standard columns |
282: | ReferenceVersionRegistry, ReferenceDataService | Published interface | The Java interfaces in section 12 |
283: | ReferenceVersionLogger | Service | Writes the one log line per table read (table code, version, business date) |
284: 
285: **Database.** Flyway migration `V<next>__rwb_e1_043_reference_versions.sql` (this story creates both tables; schema from the `${schema}` placeholder):
286: 
287: - `reference_version`: `id uuid PK`, `table_code varchar(30) NOT NULL`, `version_no integer NOT NULL`, `valid_from date NOT NULL`, `valid_to date`, `status varchar(15) NOT NULL`, `author_user_id uuid NOT NULL`, `approver_user_id uuid`, `approved_at timestamptz`, `row_count integer NOT NULL`, `content_hash char(64) NOT NULL`, `load_id uuid NOT NULL`, plus the seven standard columns. Constraints: `UNIQUE (table_code, version_no)`; `UNIQUE (table_code, valid_from, content_hash)`; `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`; partial unique index on `(table_code, valid_from) WHERE status = 'APPROVED'`.
288: - `reference_row`: `id uuid PK`, `version_id uuid NOT NULL REFERENCES reference_version (id)`, `row_key varchar(200) NOT NULL`, `row_data jsonb NOT NULL`, plus the standard columns. `UNIQUE (version_id, row_key)`; index on `version_id`.
289: - Both tables append only: an update trigger refuses chan
... truncated (9,063 chars total)
```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now I have the key architecture:

- Schema: `reference_version` and `reference_row` (JSONB) in the recovery schema. The tables are generic. PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL are `table_code` values, and each row is a `reference_row` with `row_key` and `row_data` JSONB.
- The column definitions per table_code are built in E1-043 step 2 "from the parameter catalog of RWB-E1-042" — wait, that says row check definitions from the parameter catalog. Interesting: the catalog also drives the row schema for reference tables? That seems like a design statement: "Build the column definitions per reference table code and the row check (type, required, key uniqueness) from the parameter catalog of RWB-E1-042". Hmm, that suggests the parameter catalog holds metadata for reference table columns too? That's odd but it's what it says. Actually maybe it means the column definitions are driven by the catalog's type/required metadata for parameters. I won't overinterpret.

- Seed data: `V042_2__parameter_seed.sql` contains 13 catalog rows + 28 value rows; product-scope keys have 0 value rows by design. Let me read it to confirm and find the exact inserts for E1-045 keys. Also read the consolidated V0042 to see which is the "real" migration. And the config CSV.

Let me read V042_2 seed.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\sql\\V042_2__parameter_seed.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V042_2__parameter_seed.sql, lines 1-193
1: -- Story: RWB-E1-042
2: -- Migration: parameter catalog seed (generated)
3: -- Schema: ${recoverySchema}
4: --
5: -- REVIEW COPY. D-RCV-28 requires one migration per story named
6: -- V<seq>__<story>_<name>.sql. Commit the consolidated
7: -- V0042__rwb_e1_042_parameter_catalog_and_seed.sql unless a migration-lint
8: -- exception is approved for the split. See section 2 of the clarification pack.
9: --
10: -- Generated from config/parameter-catalog.csv by tools/Generate-ParameterSeed.ps1.
11: -- Do not edit by hand: change the catalog CSV and regenerate this file.
12: --
13: -- Seed provenance. These rows are deployment defaults, not a maker-checker approval
14: -- by a person. The author is the system seed account (the nil UUID); approver_user_id
15: -- stays NULL and approved_at records the release date. The first human load through
16: -- POST /admin/reference-loads with table PARAMETER starts at version 2.
17: --
18: -- Seed set. This bootstrap file carries the rows RWB-E1-042 itself defines, the two
19: -- RWB-E1-002 parameters that precede it, the service-level status list RWB-E1-045
20: -- needs, and the five PRODUCT-scope catalog entries RWB-E1-045 defines. It is not a
21: -- claim to be the full Epic 1 catalog; that is config/parameter-catalog.csv and is
22: -- tracked as OI-E1-042-003. Product-scope rows carry no default by design: their
23: -- values are PRODUCT_PARAMETER rows, not parameter_value rows.
24: 
25: INSERT INTO ${recoverySchema}.parameter_catalog
26:     (param_key, kind, value_type, unit, min_value, max_value, default_value,
27:      scope, required, owner_role, environments, used_by, secret, description, created_by)
28: VALUES
29:     ('case.entry.dpd',
30:      'BUSINESS', 'INTEGER', 'CALENDAR_DAYS', '1', '365', '90',
31:      'GLOBAL', true, 'RW-COE', 'DEV,SIT,UAT,PROD',
32:      'recovery.casewf.casecreation', false,
33:      'Days past due at which an account enters recovery (DL16).',
34:      '00000000-0000-0000-0000-000000000000'::uuid),
35:     ('refdata.cache.ttl-seconds',
36:      'ENVIRONMENT', 'INTEGER', 'SECONDS', NULL, NULL, '300',
37:      'GLOBAL', true, 'RW-PLATADM', 'DEV,SIT,UAT,PROD',
38:      'recovery.casewf.refdata', false,
39:      'Time to live of the reference data row cache, in seconds (DL11).',
40:      '00000000-0000-00
... truncated (10,743 chars total)
```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now I have the seed. Key insight: the "product parameters seed data" is the *catalog* entries in `V042_2__parameter_seed.sql`, not the values. The values are not seeded — they're loaded as PRODUCT_PARAMETER reference rows (reference_row JSONB) via the load endpoint. This is exactly the distinction the user needs.

But wait: there's also `parameter_value` with a `product_group` column and a `product_group`-scoped lookup in E1-042. Yet E1-042's clarification pack says product-scope values are not in `parameter_value`; they are PRODUCT_PARAMETER rows. So what's `parameter_value.product_group` for? It was designed but product-scope values go to reference data instead. That's a tension. The clarification pack explicitly says "Product-scope rows carry no values by design. Their values are PRODUCT_PARAMETER rows read through ProductParameterService (E1-045), not parameter_value rows." So the `product_group` column in `parameter_value` is currently unused for E1-045; maybe reserved. I should mention this to avoid developers putting product values in `parameter_value`.

Now, where does PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL schema live? There's no dedicated table. They are `table_code` values stored in generic `reference_version` + `reference_row` (JSONB). The row schema (columns) for each table_code is defined as data — E1-043 step 2 says "Build the column definitions per reference table code ... from the parameter catalog of RWB-E1-042". Hmm, that's the only sentence. Is there a specific `reference_table_column` table? Search for "reference_table" or "column_definitions". Let me grep in the E1-043 story for "column". Also check the physical schema for `reference_column` or similar.

Let me grep for "column_definitions" / "reference_table_column" / "table_code" in schema. Also look at E1-043 sections 8/11/12 for the reference table list and column definitions.

The user asks specifically: "where product parameters seed data is and where the schema is and then how does this story connects to it". So the answer:

1. Seed data:
   - Catalog definitions: `E1-042 Migration and Clarifications/config/parameter-catalog.csv` (source), generated into `.../sql/V042_2__parameter_seed.sql` (and consolidated `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`). 13 rows, including the 5 PRODUCT-scope keys + `servicelevel.required-statuses`. The 5 PRODUCT keys have `default_value` NULL and no `parameter_value` rows.
   - Product parameter *values*: not seeded anywhere. They are l

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "PRODUCT_PARAMETER|LOV-REF-TABLE|reference table code|column definition", "include": "*.md", "path": "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7", "limit": 40}
```

```text
Found 29 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 019 Roles teams and queues as data v1.md:
  Line 32: - RWB-E1-043 is done: ReferenceVersionRegistry and ReferenceDataService hold versions of reference tables, and POST /admin/reference-loads calls them; QUEUE is a LOV-REF-TABLE code and QUEUE_MEMBER is added to it (see additions).


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 043 Reference data service with versioned tables v2.md:
  Line 35: - RWB-E1-042 is done: the configuration service serves `refdata.cache.ttl-seconds` (assumed 300; DL11) and the list of reference table codes.

  Line 36: - The list LOV-REF-TABLE (new, see Additions) is loaded with the 12 reference table codes in section 8, BR1. No rule table has a code in it.

  Line 70: | Negotiable | The list of table codes is data (LOV-REF-TABLE). The story fixes the versioning behavior, not the tables |

  Line 156: | BR1 | The reference tables served are PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD and PRODUCT_PARAMETER. The list is data and changes by a load of LOV-REF-TABLE. Rule tables are not reference tables and have no code in LOV-REF-TABLE. The holiday calendar is not among them; it is read from v_ace_holiday | Principle 1; REQ-DRI-011; refdata.txt Reference tables; RWB-E1-069 |

  Line 210: | DF-REF-028 | lov_value | lov_code | Read, through the P4 published interface, for LOV-REF-TABLE |

  Line 211: | DF-REF-029 | lov_value | value_code | Read, through the P4 published interface, for LOV-REF-TABLE |

  Line 223: | Request | multipart/form-data: `file` (CSV or XLSX, one sheet), `table` (a LOV-REF-TABLE code), `validFrom` (date) |

  Line 292: **Configuration and reference data.** `refdata.cache.ttl-seconds` = 300 (assumed; DL11), loaded by the platform administrator in the configuration service. LOV-REF-TABLE values and the column definitions per reference table code, loaded by the reference data administrator. The first version of each of the 12 reference tables is loaded by the reference data administrator before SIT and approved by Risk. The holiday calendar is ACE data read through `v_ace_holiday` and has no version row of its own.

  Line 297: 2. Build the column definitions per reference table code 
... truncated (5,947 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "PRODUCT_PARAMETER|SERVICE_LEVEL", "include": "*.sql", "path": "06 Data/Recovery Workbench Physical Schema v6.sql", "limit": 40}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 4764: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'SERVICE_LEVEL', 'Service level', 1, DATE '2026-11-30');

  Line 5132: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'SERVICE_LEVEL', 'Service level', 8, DATE '2026-11-30');

  Line 5143: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PRODUCT_PARAMETER', 'Product parameter', 19, DATE '2026-11-30');

```

### Assistant - 2026-11-16 14:20 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. LOV-REF-TABLE seed rows exist in physical schema v6. Let me see lines 5120-5150 to list the codes and sort order. Also, is there a `reference_table_column` table? The E1-043 story says "column definitions per reference table code" are loaded by the reference data administrator — but where are they stored? Possibly in the `parameter_catalog` table? The build step says "from the parameter catalog of RWB-E1-042". Hmm, that's ambiguous. Let me search for "column" in the physical schema around reference tables, or for a table like `reference_column`. Grep for `column_name` or `reference_column`.

Let me grep in the schema for `reference_` table names.

</details>

**Tool `grep`** - completed

```json
{"pattern": "CREATE TABLE reference|reference_column|column_name|column_def", "include": "*.sql", "path": "06 Data/Recovery Workbench Physical Schema v6.sql", "limit": 40}
```

```text
Found 2 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 1437: CREATE TABLE reference_version (

  Line 1471: CREATE TABLE reference_row (

```

**Tool `read`** - completed

```json
{"limit": 35, "offset": 5120, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 5120-5154
5120: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'SUPERSEDED', 'Superseded', 4, DATE '2026-11-30');
5121: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'ROLLED_BACK', 'Rolled back', 5, DATE '2026-11-30');
5122: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'REFUSED', 'Refused', 6, DATE '2026-11-30');
5123: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TEST-RESULT', 'PASSED', 'Passed', 1, DATE '2026-11-30');
5124: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TEST-RESULT', 'FAILED', 'Failed', 2, DATE '2026-11-30');
5125: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PRODUCT', 'Product', 1, DATE '2026-11-30');
5126: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'REGION', 'Region', 2, DATE '2026-11-30');
5127: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'EXPOSURE_BAND', 'Exposure band', 3, DATE '2026-11-30');
5128: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ROLE', 'Role', 4, DATE '2026-11-30');
5129: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'TEAM', 'Team', 5, DATE '2026-11-30');
5130: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE', 'Queue', 6, DATE '2026-11-30');
5131: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE_MEMBER', 'Queue member', 7, DATE '2026-11-30');
5132: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'SERVICE_LEVEL', 'Service level', 8, DATE '2026-11-30');
5133: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_TYPE', 'Document type', 9, DATE '2026-11-30');
5134: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_CHECKLIST
... truncated (5,847 chars total)
```

### Assistant - 2026-11-16 14:21 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Interesting: the LOV-REF-TABLE seed has more codes than E1-043 BR1's 12, including PRODUCT, SERVICE_LEVEL, PRODUCT_PARAMETER, PARAMETER, ENTRY, EXCLUSION, ALLOCATION, etc. This is a discrepancy: E1-043 BR1 lists 12 codes; the physical schema seed lists 25. E1-043 says "LOV-REF-TABLE (new, see Additions) is loaded with the 12 reference table codes in section 8, BR1." But the physical schema v6 seeds 25 codes including rule table-like codes. This is likely a known drift. Should I flag it? The user asks where the seed/schema are and how the story connects. It's relevant: developers may find the LOV has more codes than the story's BR1. But maybe the physical schema is the baseline, and E1-043's additions clarify. I can note the discrepancy briefly if it matters.

Let me check E1-043 section 8 BR1 list: PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, PRODUCT_PARAMETER = 12. The LOV seed has PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, QUEUE_MEMBER, SERVICE_LEVEL, DOCUMENT_TYPE, DOCUMENT_CHECKLIST, RETENTION_CLASS, TEMPLATE, DELEGATION_LIMIT, PERMISSION, MASKING_RULE, PARTNER_USER, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER, PARAMETER, ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER = 25. So indeed drift. But maybe the physical schema v6 is newer and includes additions from other stories (queue member, document checklist, etc.). E1-043 says "the list is data and changes by a load of LOV-REF-TABLE", and E1-019 adds QUEUE_MEMBER. So the list can grow. The "12" is the initial set at E1-043 time; other stories add codes. But ENTRY/EXCLUSION/ALLOCATION/ASSIGNMENT/TRANSFER are rule tables and E1-043 says rule tables have no code in LOV-REF-TABLE. That's a real conflict with the seed. Hmm, those might be reference tables too (entry rules, exclusion rules), not Drools rule tables. Actually the workbench has rule tables ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER (Drools) per E1-043 BR1 "Rule tables are not reference tables and have no code in LOV-REF-TABLE". Yet LOV-RULE-TABLE also lists them. So having them in LOV-REF-TABLE is likely wrong. This could be a meaningful finding for developers: the physical schema's LOV seed includes rule table codes in LOV-REF-TABLE, contradicting E1-043 BR1. But is this in scope for the user's question? It's about seed data and schema. I could mention it under "watch-outs" briefly. However, I should be careful not to derail. The user wants the concre

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "column definitions|reference table code|PRODUCT_PARAMETER rows", "include": "Recovery Workbench Build Notes Epic 1 v4.md", "limit": 30}
```

```text
No matches found
```

### Assistant - 2026-11-16 14:21 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me search Build Notes for E1-043 and "ColumnDefinition" or "row check".

</details>

**Tool `grep`** - completed

```json
{"pattern": "RWB-E1-043|ReferenceVersionRegistry|column", "include": "Recovery Workbench Build Notes Epic 1 v4.md", "limit": 40}
```

```text
Found 40 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 23: Create all 44 tables inside one transaction, so a failure part way through leaves the schema untouched. Copy the columns, primary keys and unique constraints from Recovery Workbench Physical Schema v4.sql without changing a name or a type, because the test in step 4 compares them against the dictionary and fails on any difference. Declare the foreign keys as ALTER TABLE ... ADD CONSTRAINT statements after the tables exist, which is the form the schema file uses. Add the two triggers that call refuse_change() on decision_log_entry and interaction, so neither table accepts an UPDATE or a DELETE. Reconcile the counts first: this step says 68 foreign keys and 76 indexes, and the schema file now holds 66 and 76 for these tables.

  Line 33: **In the story.** Pipeline: runs the dictionary conformance test, which compares every column in the recovery schema with sys_fields.

  Line 35: Write the conformance test as a pipeline test, not a unit test, because it has to run against a real database after the migration. Read the live columns from information_schema.columns for the recovery schema, read the rows of sys_fields, and compare in both directions. Fail the build if a real column has no dictionary row, if a dictionary row has no column, or if the physical types differ. Leave the 7 standard columns out of the comparison. The failure message must name the column that caused it, because AC5 asserts the exact wording.

  Line 47: Build the load path for this table code. The reference data administrator sends the catalog file to POST /api/recovery/v1/admin/reference-loads with the table code data_product. Implement that endpoint if RWB-E1-043 has not already delivered it, and implement DataProductCatalogHandler as the ReferenceTableHandler registered for that code, which is how a load finds the class that handles it. The file holds the 14 products with the owner user ID for that environment, so DEV and SIT are given different files.

  Line 57: **In the story.** Data steward: confirms the load as owner of the catalog through the reference data change process (RWB-E1-043).

  Line 59: Do not apply the load when it is uploaded. A second person has to approve it first, so the load stays pending until the data steward who owns the catalog approves it through the approve endpoint of the reference data change pro
... truncated (23,446 chars total)
```

### Assistant - 2026-11-16 14:21 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The Build Notes use `ReferenceTableHandler` registered per table code, e.g., `DataProductCatalogHandler`. So the "schema" for PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL is implemented as a handler with a row check, not a physical table. The column definitions live in the handler (code/config) and the row data in JSONB. E1-043 build step 2 says "Build the column definitions per reference table code and the row check ... from the parameter catalog of RWB-E1-042" — so the handler is the schema in practice.

Let me check the E1-043 section of the Build Notes to see exactly how the handler is structured, and whether there's a `ReferenceColumn` definition or config. Search "ReferenceTableHandler" and read the relevant section.

</details>

**Tool `grep`** - completed

```json
{"pattern": "ReferenceTableHandler|ReferenceLoadHandler|row check|table code", "include": "Recovery Workbench Build Notes Epic 1 v4.md", "limit": 30}
```

```text
Found 26 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 45: **In the story.** Reference data administrator: loads the data product catalog file with table code `data_product` through `POST /admin/reference-loads`, naming the owner user ID of each product for the environment.

  Line 47: Build the load path for this table code. The reference data administrator sends the catalog file to POST /api/recovery/v1/admin/reference-loads with the table code data_product. Implement that endpoint if RWB-E1-043 has not already delivered it, and implement DataProductCatalogHandler as the ReferenceTableHandler registered for that code, which is how a load finds the class that handles it. The file holds the 14 products with the owner user ID for that environment, so DEV and SIT are given different files.

  Line 277: **In the story.** Reference data administrator: loads the file through `POST /admin/reference-loads` with table code `tracker_inventory`, version "TRK-2026.11" and valid from 2026-11-16.

  Line 279: The reference data administrator uploads the file. The endpoint POST /admin/reference-loads already exists from RWB-E1-043, so you write no controller here; you supply the handler it calls for table code tracker_inventory. The request carries the file, the table code and the valid-from date of 2026-11-16. The load service recognizes a repeated file by its hash, which makes the call idempotent: sending the same file twice changes nothing and answers 409 with MSG-P1-011 instead of writing a second set of rows. The administrator who loads the file may not confirm it, so this call only submits the version for checking.

  Line 285: The checks run on their own inside code you write. TrackerInventoryHandler implements the ReferenceTableHandler interface whose signature comes from RWB-E1-001, and its validate method reads every row of the file before anything is written. Check the required fields, the list values for location_type, update_cycle and decision, a tracker code that appears once per inventory version, a target_product naming a row in data_product for each LOAD decision, and team_code membership of LOV-TEAM through the P4 published interface. Last, count the rows per team against the parameter tracker.inventory.teams, which holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. Unit test each check with a failing row.

  Line 743: A person starts this, the referen
... truncated (14,026 chars total)
```

### Assistant - 2026-11-16 14:21 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Excellent: line 2425 says `ReferenceTableSchemas` holds the column names, types and key columns per table and "comes from the parameter catalog of RWB-E1-042". So the row schema is in code (`ReferenceTableSchemas`) driven by the parameter catalog. That's the "schema" for PRODUCT_PARAMETER rows in implementation terms.

Now I have enough to answer concretely:

**Where the seed data is**
- Source: `E1-042 Migration and Clarifications/config/parameter-catalog.csv` — 13 rows. It includes the 5 PRODUCT-scope catalog entries plus `servicelevel.required-statuses`.
- Generated SQL: `E1-042 Migration and Clarifications/sql/V042_2__parameter_seed.sql` — catalog inserts (13) + approved global values (28) + deployment guard.
- Consolidated migration (the one meant to be committed): `E1-042 Migration and Clarifications/sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` (per the review note; split files are review copies that violate D-RCV-28).
- Same copies in `13 AI-First SDLC repository/output/INC-003-epic-1-RWB-E1-042/...` and `17 AI-First SDLC Repository v2/output/INC-003-...`.
- Important: **there are no product parameter values in the seed.** The 5 PRODUCT rows have `default_value = NULL` and zero `parameter_value` rows. The seed comment says "Product-scope rows carry no default by design: their values are PRODUCT_PARAMETER rows, not parameter_value rows." So the first real values for Mortgage/HP/SSME are business loads, not code.

**Where the schema is**
- Catalog + global parameter values: `V042_1__parameter_catalog.sql` (review copy) / `V0042__...sql` (consolidated), tables `parameter_catalog` and `parameter_value`; also in `06 Data/Recovery Workbench Physical Schema v6.sql`.
- Product parameters themselves: **no dedicated physical table.** They live in the generic versioned reference tables from E1-043:
  - `reference_version` (`table_code`, `version_no`, `valid_from`, `status`, `author_user_id`, `approver_user_id`, `content_hash`, ...), physical schema v6 lines 1437–1468.
  - `reference_row` (`version_id`, `row_key`, `row_data jsonb`, ...), lines 1471–1484.
  - `PRODUCT`, `PRODUCT_PARAMETER`, `SERVICE_LEVEL` are values of `table_code`; `row_data` holds the row columns; `row_key` is the natural key. `LOV-REF-TABLE` seeds these codes in the physical schema (lines 5125, 5132, 5143).
  - The row "schema" (column names, types, key columns) is not a DB table: `ReferenceTableSchemas` in E1-043 holds it, built from the parameter catalog (E1-043 solution plan step

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"limit": 45, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\sql\\V0042__rwb_e1_042_parameter_catalog_and_seed.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql, lines 1-45
1: -- Story: RWB-E1-042
2: -- Migration: parameter catalog, parameter value table and catalog seed
3: -- Schema: ${recoverySchema}
4: --
5: -- Consolidated per D-RCV-28: one migration file for RWB-E1-042. It contains the
6: -- DDL from V042_1__parameter_catalog.sql and the generated seed from
7: -- V042_2__parameter_seed.sql. The split files are review copies only; commit this
8: -- file unless a migration-lint exception is approved for the split.
9: --
10: -- Definition source: Recovery Workbench Physical Schema v4.sql, parameter_catalog and
11: -- parameter_value. Parameter keys are the business names; no key is a table name.
12: --
13: -- Baseline note. RWB-E1-001 V0001__rwb_e1_001_recovery_schema.sql is written from the
14: -- Physical Schema and already creates both tables. This file is therefore guarded: it
15: -- creates what is absent and then adds the E1-042 constraints, foreign key, uniqueness
16: -- rules and indexes only when they are absent. On a schema built without the baseline it
17: -- creates the complete E1-042 definition. The drift check remains the control that an
18: -- environment matches the migrations.
19: CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_catalog (
20:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
21:     param_key varchar(100) NOT NULL,
22:     kind varchar(15) NOT NULL,
23:     value_type varchar(15) NOT NULL,
24:     unit varchar(20),
25:     min_value varchar(40),
26:     max_value varchar(40),
27:     default_value varchar(400),
28:     scope varchar(10) NOT NULL DEFAULT 'GLOBAL',
29:     required boolean NOT NULL DEFAULT false,
30:     owner_role varchar(20) NOT NULL,
31:     environments varchar(40),
32:     used_by varchar(400),
33:     secret boolean NOT NULL DEFAULT false,
34:     description varchar(400) NOT NULL,
35:     is_active boolean NOT NULL DEFAULT true,
36:     state varchar(40),
37:     version integer NOT NULL DEFAULT 1,
38:     created_at timestamptz NOT NULL DEFAULT now(),
39:     created_by uuid,
40:     updated_at timestamptz NOT NULL DEFAULT now(),
41:     updated_by uuid,
42:     CONSTRAINT uk_parameter_catalog UNIQUE (param_key),
43:     CONSTRAINT ck_parameter_catalog_scope CHECK (scope IN ('GLOBAL', 'PRODUCT')),
44:     CONSTRAINT ck_parameter_catalog_kind CHECK (kind IN ('BUSINESS', 'ENVIRONMENT')),
... truncated (2,612 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "product_parameter|service_level", "include": "*.sql", "path": "06 Data/Recovery Workbench Physical Schema v6.sql", "limit": 20}
```

```text
No matches found
```

### Assistant - 2026-11-16 14:21 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Confirmed: no physical product_parameter/service_level tables. They are reference table codes.

Let me also check the E1-043 migration file existence — maybe not in the pack, but the physical schema has the tables. The E1-043 story says migration `V<next>__rwb_e1_043_reference_versions.sql`; maybe the file exists in 17 AI-First SDLC output. Let me glob.

</details>

**Tool `glob`** - completed

```json
{"pattern": "**/*reference*version*.sql", "limit": 20}
```

```text
No files found
```

**Tool `grep`** - completed

```json
{"pattern": "create table reference_version|CREATE TABLE reference_version", "include": "*.sql", "limit": 20}
```

```text
Found 8 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 1437: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 1851: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v5.sql:
  Line 1398: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\sql\v4_tmp.sql:
  Line 1851: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\recovery-workbench-physical-schema-v4.sql:
  Line 1851: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v6.sql:
  Line 1437: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v4.sql:
  Line 1851: CREATE TABLE reference_version (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v5.sql:
  Line 1398: CREATE TABLE reference_version (

```

### Assistant - 2026-11-16 14:22 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

No E1-043 migration file exists yet — only the physical schema. So for E1-043, developers write the migration. I should say: the schema is defined in the Physical Schema v6 (baseline V0001) and E1-043 creates/uses it; no dedicated PRODUCT_* tables.

Wait — E1-001 creates all 44 tables from the physical schema; does it include reference_version/reference_row? Yes, the physical schema has them, and E1-001 says "Create all 44 tables". So `reference_version` and `reference_row` are created by the baseline migration V0001 from E1-001, not by E1-043. E1-043 says "Flyway migration V<next>__rwb_e1_043_reference_versions.sql (this story creates both tables...)" — contradicts E1-001 baseline. Like E1-042, the migration may be guarded. The physical schema v6 is the baseline. I can note that the tables are in the baseline physical schema, so E1-043's migration should be guarded like E1-042's. This is a detail, but useful.

Let me check E1-001 story to see whether it says 44 tables including reference_version. Not necessary; the Build Notes line 23 says "Create all 44 tables inside one transaction... Copy the columns ... from Physical Schema v4.sql". So yes, the baseline includes them. E1-043's "this story creates both tables" is likely drift. But the actual implementation should use guarded DDL. I can mention briefly.

Now, the user's question: "in this tell me where product paramters seed data is and where the schema is and then how does this story connects to it". They want the concrete locations and the connection. Let me answer with paths and a flow. I should be direct and not over-explain unrelated things.

Structure:

1. **The short answer**
   - Seed = catalog only, in E1-042 files; there are no product values seeded.
   - Schema = no PRODUCT_PARAMETER table; it's generic `reference_version` + `reference_row` JSONB, plus `parameter_catalog` for definitions.
   - Connection = E1-042 defines the keys; E1-043 stores versions/rows and runs checks; E1-045 adds the product completeness check + the runtime service; engines consume.

2. **Where the seed data is** — table of file paths and what's in each:
   - `E1-042 Migration and Clarifications/config/parameter-catalog.csv` — source, 13 lines. The 5 PRODUCT keys + `servicelevel.required-statuses`.
   - `E1-042 Migration and Clarifications/sql/V042_2__parameter_seed.sql` — generated inserts; 13 catalog rows, 28 global values; product keys have no values.
   - `E1-042 Migration and Clarifications/sql/V0042__rwb_e1_042_p

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "MORTGAGE|AUTO_LEASE|HIRE_PURCHASE", "include": "*.csv", "limit": 20}
```

```text
Found 20 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\_csv\recovery-workbench-user-stories-epic-2-v5\test-cases.csv:
  Line 96: TC-E2-009-08,RWB-E2-009,"AC8, BR7",Filter by product,System,Filter MORTGAGE

  Line 294: TC-E2-026-05,RWB-E2-026,"AC5, BR2",A withdrawn template holds generation,System,DIL-MORTGAGE withdrawn

  Line 317: TC-E2-031-01,RWB-E2-031,"AC1, BR1, BR2, BR6",Per agent,System,"INTAKE MORTGAGE/BKK 140 feedback, 119 accepted"

  Line 387: TC-E2-028-02,RWB-E2-028,"AC2, BR3",Acceptance measured,System,"January 2027, MORTGAGE/BKK: 300 feedback, 240, 45, 15"

  Line 413: TC-E2-030-05,RWB-E2-030,"AC5, BR3",An item without a status,System,No status for MORTGAGE_DEED


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\_csv\recovery-workbench-user-stories-epic-2-v5\acceptance-criteria.csv:
  Line 11:     Given synthetic account ""A-0001"" for customer ""C-0001"", product group ""MORTGAGE"", reached 90 days past due in the EFS data of business date 2026-12-14

  Line 14:     Then a case exists with status ""NEW"", product group ""MORTGAGE"", entry date 2026-12-15 and days past due at entry 90

  Line 170:     Given case ""RW-2026-000201"" with product group ""MORTGAGE"", status ""IN_PROGRESS"" and route state ""BOOKED_IN_ALS_NLEADS""

  Line 172:     Given CURE_PERIOD_DAYS for ""MORTGAGE"" is 30 calendar days and plan.warn-days is 3

  Line 192:     Given ten treatments recorded on 2026-12-01 across ""MORTGAGE"", ""HIRE_PURCHASE"" and ""SSME""

  Line 321:     Then the pack holds case number ""RW-2026-000610"", product group ""MORTGAGE"", 2 accounts with balances as of 2026-12-14 and 1 collateral with its latest appraisal

  Line 561:     When a product head sends GET /reports/measures?measure=CASES_BY_STAGE&product=MORTGAGE&from=2026-12-15&to=2026-12-15

  Line 562:     Then the response holds only rows with product ""MORTGAGE""

  Line 781:     Given delegation version ""DOA-2026.11"" is in force with holder ""U-9201"" at L6, ""U-9202"" at L5 and ""U-9203"" at L4 for MORTGAGE, all holding RW-PRODHEAD

  Line 800:     Given approval ""A-1"" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under ""DOA-2026.11""

  Line 807:     Given restructure officer ""U-9210"" prepared a settlement at a discount on case ""RW-2026-000124"", decision D6.4 item 2.1.1, MO
... truncated (3,378 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "MORTGAGE|AUTO_LEASE", "include": "*.sql", "limit": 20}
```

```text
Found 20 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 5549: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'MORTGAGE', 'Mortgage', 1, DATE '2026-11-30');

  Line 5730: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'MORTGAGE_INSURANCE', 'Mortgage insurance', 3, DATE '2026-11-30');

  Line 6628: INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L1', 'MORTGAGE', DATE '2026-11-30');

  Line 6632: INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L2', 'MORTGAGE', DATE '2026-11-30');

  Line 6636: INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L3', 'MORTGAGE', DATE '2026-11-30');

  Line 6640: INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L4', 'MORTGAGE', DATE '2026-11-30');

  Line 6644: INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L5', 'MORTGAGE', DATE '2026-11-30');

  Line 6648: INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L6', 'MORTGAGE', DATE '2026-11-30');


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v5.sql:
  Line 4635: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'MORTGAGE', 'Mortgage', 1, DATE '2026-11-30');

  Line 4816: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'MORTGAGE_INSURANCE', 'Mortgage insurance', 3, DATE '2026-11-30');


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 4685: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'MORTGAGE', 'Mortgage', 1, DATE '2026-11-30');

  Line 4866: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'MORTGAGE_INSURANCE', 'Mortgage insurance', 3, DATE '2026-11-30');


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\recovery-workbench-phys
... truncated (3,898 chars total)
```

### Assistant - 2026-11-16 14:22 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Interesting: LOV-PRODUCT already seeds MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED in the physical schema. So product group list exists as a LOV, but PRODUCT as a versioned reference table is separate. AC2 adds AUTO_LEASE to PRODUCT v2; the LOV-PRODUCT seed already has the original 4. That's another two-sources-of-truth issue: LOV-PRODUCT vs PRODUCT reference table. The story says product group is "checked against LOV-PRODUCT, not a closed enum" (guardrail). But PRODUCT is also a reference table. Which is the list of products in force? BR3/E1-043 BR1 includes PRODUCT as a reference table; E1-045's completeness check uses "every product in the PRODUCT version in force". Yet guardrail says product group is checked against LOV-PRODUCT. AC2 adds AUTO_LEASE to PRODUCT. Does it also need a LOV-PRODUCT row? If code validates against LOV-PRODUCT and AUTO_LEASE isn't in the LOV seed, the new product fails validation. This is a significant connection issue worth flagging.

Let me verify: guardrail line 280: "the generated API types treat product group as a string checked against LOV-PRODUCT, not as a closed enum." And E1-043 BR1 lists PRODUCT as a reference table. LOV-PRODUCT is a code list in the database seed. So there are two definitions: LOV-PRODUCT (code list) and PRODUCT (versioned reference table). Adding AUTO_LEASE via PRODUCT v2 may not add it to LOV-PRODUCT. Does E1-045 require updating LOV-PRODUCT too? AC2 says "PRODUCT version 2 adds product group AUTO_LEASE" and then a case is created with product group AUTO_LEASE, no deployment. If validation uses LOV-PRODUCT, it must be updated by data, not deployment. LOV is reference data too, but it's a different table (`lov_value`), and updating it usually requires a migration/release unless there's a load path. Hmm.

Maybe the LOV-PRODUCT check is for API input validation, and PRODUCT is the source of truth for the completeness check. The story doesn't reconcile them. This is a real integration question: how does a new product get into LOV-PRODUCT without a deployment? The guardrail says product group is checked against LOV-PRODUCT, which would block AUTO_LEASE unless LOV-PRODUCT is extendable by data load. Is LOV-* loaded through reference loads? E1-043 says "LOV-REF-TABLE values and the column definitions per reference table code, loaded by the reference data administrator" — but that's LOV-REF-TABLE, not LOV-PRODUCT generally. There's E1-069 (LOV read-only ACE views?) or RWB-E1-043? Let me check if LOVs are loada

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"limit": 12, "offset": 4684, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 4684-4695
4684: -- Seed: closed lists of values. Thai labels are added when approved (DL10)
4685: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'MORTGAGE', 'Mortgage', 1, DATE '2026-11-30');
4686: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'HIRE_PURCHASE', 'Hire purchase', 2, DATE '2026-11-30');
4687: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'SSME', 'SSME', 3, DATE '2026-11-30');
4688: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'UNSECURED', 'Unsecured', 4, DATE '2026-11-30');
4689: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'NEW', 'New', 1, DATE '2026-11-30');
4690: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'ASSIGNED', 'Assigned', 2, DATE '2026-11-30');
4691: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'IN_PROGRESS', 'In progress', 3, DATE '2026-11-30');
4692: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'WAITING_CUSTOMER', 'Waiting customer', 4, DATE '2026-11-30');
4693: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'WAITING_PARTNER', 'Waiting partner', 5, DATE '2026-11-30');
4694: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'WAITING_APPROVAL', 'Waiting approval', 6, DATE '2026-11-30');
4695: INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'ON_HOLD', 'On hold', 7, DATE '2026-11-30');
[Output truncated. Continue reading with offset: 4696]
```

### Assistant - 2026-11-16 14:22 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

LOV-PRODUCT has exactly 4 products; AUTO_LEASE is not there. And LOV-CASE-STATUS has 7 statuses including ON_HOLD, while `servicelevel.required-statuses` has six (excludes ON_HOLD). That's consistent with "required" statuses not all statuses, fine. But the LOV-PRODUCT gap is real for AC2.

Maybe PRODUCT reference table is the dynamic list, and LOV-PRODUCT is only a seed for initial values. The guardrail says "checked against LOV-PRODUCT". If AUTO_LEASE is added only to PRODUCT, validation against LOV-PRODUCT would reject it. Unless LOV-PRODUCT itself is loaded as part of reference data / E1-019 "Roles teams and queues as data" pattern. Let me check if there's a story for LOV maintenance. E1-069 "Read only ACE source views..." maybe includes LOV. Search for "LOV-PRODUCT" in stories.

</details>

**Tool `grep`** - completed

```json
{"pattern": "LOV-PRODUCT", "include": "*.md", "path": "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7", "limit": 30}
```

```text
Found 10 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 018 Case ID issuance and case record v1 v2.md:
  Line 383: - LOV-EXPOSURE bands, LOV-CASE-STATUS and LOV-PRODUCT from the reference data service (RWB-E1-043).


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 038 Delegation of authority table as reference data v1.md:
  Line 36: - LOV-DECISION holds D5, D6.4, D6.5, D6.6, D7.1, D7.4, D7.5, D8.2, D8.3, D8.4, D9.2 and D9.3; LOV-APPROVAL-LEVEL holds L1 to L6; LOV-PRODUCT holds MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED.

  Line 238: - Configuration and reference data: DOA-2026.11 (RW-REFADM loads, RW-RISK approves); LOV-DECISION, LOV-APPROVAL-LEVEL, LOV-PRODUCT; applies_when values WO_CRITERIA_MET and WO_CRITERIA_NOT_MET for the two write-off rows of item 2.1.10, loaded with the version; parameter rwb.refload.approver.delegation_limit. Holders and substitutes per DL18.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md:
  Line 155: | RW-PRODHEAD, product head | Owns the values for the product (LOV-PRODUCT owner in refdata.txt); reads versions (Reference data R) |

  Line 280: - No business value in code. No product group code, period, threshold or band is written in Java or TypeScript; the generated API types treat product group as a string checked against LOV-PRODUCT, not as a closed enum.

  Line 282: - No read of another module's tables. Reference rows are read through `ReferenceDataService`; LOV-PRODUCT through the P4 published interface.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 046 Template and merge field catalog as data v1.md:
  Line 34: - Lists LOV-LANG, LOV-PRODUCT and LOV-NOTICE are loaded (refdata.txt).

  Line 243: - Configuration and reference data: LOV-LANG, LOV-PRODUCT, LOV-NOTICE (loaded by RW-REFADM); the merge field catalog file (RW-REFADM, content agreed with Legal counsel, DL28); template files and their approvals (Legal counsel); new lists for channel (LETTER, SMS, LINE) and signature basis (E_SIGNATURE_ALLOWED, WET_INK_REQUIRED) recorded as additions.


C:\Users\SahilMore\Downloads
... truncated (2,808 chars total)
```

### Assistant - 2026-11-16 14:23 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

E1-018 line 383 says LOV-PRODUCT comes "from the reference data service (RWB-E1-043)". So LOVs are served by E1-043. That means LOV-PRODUCT might be a reference table version too, or the LOV values are seeded/loaded. E1-046 says LOV-PRODUCT is "loaded by RW-REFADM". So LOV-PRODUCT is loadable data, not just a migration seed. Then AUTO_LEASE would need a LOV-PRODUCT load in addition to PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL. AC2 doesn't mention that. That's a concrete gap: adding AUTO_LEASE requires four loads, not three, if LOV-PRODUCT is the validation list. Unless PRODUCT itself is the product list and LOV-PRODUCT is just an older list.

This is worth flagging as a question: "AC2 adds AUTO_LEASE to PRODUCT, but LOV-PRODUCT, which the guardrail says validates product group, is loaded separately and currently holds only MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED. Confirm whether a new product also needs a LOV-PRODUCT load; otherwise AC2 cannot pass through validation." This is a sharp, useful finding. I'll include it.

Now, the user asked "where product parameters seed data is and where the schema is and then how does this story connects to it". I should answer in that order, with file paths, and a connection chain. I'll include the two watch-outs (ENTRY_DPD conflict; LOV-PRODUCT vs PRODUCT; parameter_value.product_group red herring).

Let me structure the answer:

**1. Where the seed data is**
A small table of file paths:
| What | Path | Contains |
- Catalog source CSV
- Generated seed SQL (review copy)
- Consolidated migration
- Copies under 13/17 output
Then explain: only catalog definitions + global values; no product values.

**2. Where the schema is**
- `parameter_catalog` + `parameter_value`: DDL in V0042 / physical schema v6.
- `reference_version` + `reference_row`: physical schema v6 lines 1437-1484.
- No PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL tables; table codes.
- Row schema = `ReferenceTableSchemas` in E1-043, no physical table.

**3. How E1-045 connects**
A chain:
E1-042 catalog (definition) → E1-043 reference versions/rows (values) → E1-045 completeness check + service → consumers (E1-018/020/028).
Explain each link with specific columns:
- `parameter_catalog.scope`, `.required`, `.value_type`, `.unit`, `.min_value`, `.max_value`.
- `reference_version.table_code` values; `status=APPROVED`; `valid_from`; `content_hash`.
- `reference_row.row_key`, `row_data`.
- `servicelevel.required-statuses` value read from `parameter_value`.
- `ProductParame

_[truncated]_

</details>

**Tool `glob`** - completed

```json
{"pattern": "**/Generate-ParameterSeed.ps1", "limit": 10}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\tools\Generate-ParameterSeed.ps1
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\output\INC-003-epic-1-RWB-E1-042\implement\tools\Generate-ParameterSeed.ps1
```

**Tool `glob`** - completed

```json
{"pattern": "**/tools/*.ps1", "limit": 20}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\tools\Generate-ParameterSeed.ps1
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\tools\Assemble-V0042.ps1
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\output\INC-003-epic-1-RWB-E1-042\implement\tools\Generate-ParameterSeed.ps1
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\output\INC-003-epic-1-RWB-E1-042\implement\tools\Assemble-V0042.ps1
```

### Assistant - 2026-11-16 14:23 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. The generator and assembler exist. I can include them.

Now, let me think about whether the user wants this for E1-045 specifically, or the general "product parameters" area. They said "in this tell me where product paramters seed data is and where the schema is and then how does this story connects to it". "in this" refers to the E1-045 briefing. So answer for E1-045.

I should use a UI block? This is a lot of path/data detail. A table of locations would be useful. I'll use a `Table` for the files and maybe a `Steps` for the connection chain. Two blocks. The prose can carry the nuances.

Let me draft the table rows:

| Layer | File | What is in it |
| Catalog source | `E1-042 Migration and Clarifications\config\parameter-catalog.csv` | 13 definitions; the 5 PRODUCT keys + `servicelevel.required-statuses` |
| Generated seed | `...\sql\V042_2__parameter_seed.sql` | 13 catalog inserts + 28 global value rows; PRODUCT keys have no values |
| Commit migration | `...\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql` | DDL + seed, the one to commit |
| Physical schema | `06 Data\Recovery Workbench Physical Schema v6.sql` | `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row` |

Then the schema table:
| Object | Type | Holds |
| `parameter_catalog` | table | definitions: scope, required, type, unit, range, owner |
| `parameter_value` | table | global values per environment, e.g. `case.entry.dpd` = 90; NOT product values |
| `reference_version` | table | one version per `table_code` (PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL) |
| `reference_row` | table | one row per key in that version, `row_data` JSONB |
| `ReferenceTableSchemas` | E1-043 code | column names, types, key columns per table code |

Then connection chain.

Need to be precise: `parameter_value` does hold `servicelevel.required-statuses` (global) and `case.entry.dpd`, etc. It does not hold `ENTRY_DPD` product values. Good.

Question: Is `servicelevel.required-statuses` read from `parameter_value` by E1-045? The story says "the parameter `servicelevel.required-statuses`". It's a GLOBAL catalog row with approved values per environment. E1-042's `ParameterService.get` would read it from `parameter_value`. Yes.

Question: Does `ProductParameterService` read `parameter_catalog` too? It reads `reference_row` via `ReferenceDataService` for values; the completeness check reads `parameter_catalog` for required/scope/range. The story's data table lists `parameter_catalog` scope/

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "ix_case_status_queue", "include": "*.sql", "limit": 10}
```

```text
Found 8 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 2797: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 2377: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v5.sql:
  Line 2358: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\sql\v4_tmp.sql:
  Line 2797: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\recovery-workbench-physical-schema-v4.sql:
  Line 2797: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v5.sql:
  Line 2358: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v4.sql:
  Line 2797: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v6.sql:
  Line 2377: CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);

```

**Tool `grep`** - completed

```json
{"pattern": "ix_case_status_queue", "include": "*.md", "limit": 10}
```

```text
Found 10 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v7.md:
  Line 3542: **Database.** Reads `recovery_case`, `queue` and `timer`. Uses `ix_case_owner_status`, `ix_case_status_queue` and `ix_timer_case_id`. Adds index `ix_timer_case_type_status` on `timer (case_id, timer_type, status)` in migration `V<next>__rwb_e2_011_queue_view_index.sql`.

  Line 9329: **Database.** Reads recovery_case (id, case_no, product_group, status, stage_code, owner_user_id, queue_id, team_code, entry_date, prescription_date, stage_clock_start, deviation_open), queue (queue_code, team_code) and timer (case_id, timer_type, expires_at, paused, status). Writes nothing. Index needed: `CREATE INDEX ix_timer_case_type ON timer (case_id, timer_type) WHERE status IN ('RUNNING','PAUSED','EXPIRED')`, added by a Flyway migration in the P3 migration folder. ix_case_status_queue and ix_case_owner_status serve the other filters.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v6.md:
  Line 3422: **Database.** Reads `recovery_case`, `queue` and `timer`. Uses `ix_case_owner_status`, `ix_case_status_queue` and `ix_timer_case_id`. Adds index `ix_timer_case_type_status` on `timer (case_id, timer_type, status)` in migration `V<next>__rwb_e2_011_queue_view_index.sql`.

  Line 9164: **Database.** Reads recovery_case (id, case_no, product_group, status, stage_code, owner_user_id, queue_id, team_code, entry_date, prescription_date, stage_clock_start, deviation_open), queue (queue_code, team_code) and timer (case_id, timer_type, expires_at, paused, status). Writes nothing. Index needed: `CREATE INDEX ix_timer_case_type ON timer (case_id, timer_type) WHERE status IN ('RUNNING','PAUSED','EXPIRED')`, added by a Flyway migration in the P3 migration folder. ix_case_status_queue and ix_case_owner_status serve the other filters.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v5.md:
  Line 3377: **Database.** Reads `recovery_case`, `queue` and `timer`. Uses `ix_case_owner_status`, `ix_case_status_queue` and `ix_timer_case_id`. Adds index `ix_timer_case_type_status` on `timer (case_id, timer_type, status)` in migration `V<next>__rwb_e2_011_queue_view_index.sql`.

  Line 9400: **Database.** Reads recovery_case (id, case_no, product_group, status, stage_code, owner_user_id, queue_
... truncated (4,892 chars total)
```

### Assistant - 2026-11-16 14:23 | opencode-go/deepseek-v4.1-flash | build

## Short version

- **Seed data:** there is no seed of product *values*. The only seed is the **parameter catalog definitions** in E1-042, which include the five `PRODUCT`-scope keys and `servicelevel.required-statuses`.
- **Schema:** there is no `PRODUCT_PARAMETER` table. Product values live in the generic **`reference_version` + `reference_row`** tables from E1-043, with `PRODUCT_PARAMETER` / `SERVICE_LEVEL` / `PRODUCT` as `table_code` values. The catalog definitions live in `parameter_catalog` / `parameter_value`.
- **Connection:** E1-042 defines the keys, E1-043 stores and versions the values, E1-045 adds the completeness check and the `ProductParameterService` read interface, and the engines consume that service.

```openui-lang
root = Stack([chain, files])
chain = Steps([{title: "E1-042 catalog", markdown: "Defines the five PRODUCT keys and servicelevel.required-statuses: scope, required, type, unit, range."}, {title: "E1-043 reference data", markdown: "Stores PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL as versions and rows; owns approval and effective dating."}, {title: "E1-045", markdown: "Adds ProductCompletenessCheck to the E1-043 registry and ProductParameterService over ReferenceDataService."}, {title: "Engines", markdown: "Timer engine, case creation and allocation read values by product group and business date; decision log records the version."}], "column")
files = Table(["Layer", "File", "What is in it"], [["Catalog source", "E1-042 Migration and Clarifications\\config\\parameter-catalog.csv", "13 definitions; the 5 PRODUCT keys plus servicelevel.required-statuses"], ["Generated seed", "E1-042 Migration and Clarifications\\sql\\V042_2__parameter_seed.sql", "13 catalog inserts and 28 global value rows; PRODUCT keys have no values"], ["Commit migration", "E1-042 Migration and Clarifications\\sql\\V0042__rwb_e1_042_parameter_catalog_and_seed.sql", "DDL plus seed; the one migration to commit"], ["Physical schema", "06 Data\\Recovery Workbench Physical Schema v6.sql", "parameter_catalog, parameter_value, reference_version, reference_row"]])
```

## 1. Where the product parameter seed data is

**The source of truth is the CSV, not the SQL.**

`E1-042 Migration and Clarifications\config\parameter-catalog.csv` has 13 rows. The relevant ones for E1-045 are:

| Key | Scope | Required | Type | Unit | Range | Default |
|---|---|---|---|---|---|---|
| `ENTRY_DPD` | PRODUCT | yes | INTEGER | DAYS | — | none |
| `EXCLUSION_LIST` | PRODUCT | yes | CODE_LIST | — | — | none |
| `NOTICE_PERIOD_DAYS` | PRODUCT | yes | INTEGER | DAYS | 1–365 | none |
| `CURE_PERIOD_DAYS` | PRODUCT | yes | INTEGER | DAYS | — | none |
| `EXPOSURE_BAND_SET` | PRODUCT | yes | CODE_LIST | — | — | none |
| `servicelevel.required-statuses` | GLOBAL | yes | CODE_LIST | — | — | six statuses |

The SQL is generated from that CSV by `E1-042 Migration and Clarifications\tools\Generate-ParameterSeed.ps1` into `V042_2__parameter_seed.sql`. The review note in that file says the split files `V042_1` / `V042_2` are review copies only, and `V0042__rwb_e1_042_parameter_catalog_and_seed.sql` is the consolidated migration to commit under D-RCV-28. Copies also exist under `13 AI-First SDLC repository\output\INC-003-epic-1-RWB-E1-042\` and `17 AI-First SDLC Repository v2\output\INC-003-epic-1-RWB-E1-042\`.

**What the seed actually inserts:**

- 13 `parameter_catalog` rows.
- 28 `parameter_value` rows — 7 global keys × 4 environments.
- **Zero product values.** The five `PRODUCT` keys have `default_value = NULL` and no `parameter_value` rows. The file says it explicitly: *"Product-scope rows carry no default by design: their values are PRODUCT_PARAMETER rows, not parameter_value rows."*

So if a developer asks "where are the Mortgage 30-day and HP 60-day rows?", the answer is: **nowhere in the repo.** They are business reference loads, not seed data. AC1's `PRODUCT_PARAMETER` version 2 is test data in the test container. The first production values arrive through `POST /api/recovery/v1/admin/reference-loads` and are approved by the product head/risk.

## 2. Where the schema is

**Catalog and global values** — `V0042__...sql` (or `V042_1__parameter_catalog.sql` for the review copy), also in `06 Data\Recovery Workbench Physical Schema v6.sql`:

- `parameter_catalog` — one row per definition: `param_key`, `scope` (`GLOBAL`/`PRODUCT`), `required`, `value_type`, `unit`, `min_value`, `max_value`, `default_value`, `owner_role`.
- `parameter_value` — dated values per environment: `param_key`, `environment`, `param_value`, `product_group`, `version_no`, `valid_from`, `valid_to`, `status`, `author_user_id`, `approver_user_id`.

**Product values** — `06 Data\Recovery Workbench Physical Schema v6.sql`, lines 1437–1484:

- `reference_version` — one row per version of a table: `table_code`, `version_no`, `valid_from`, `valid_to`, `status`, `author_user_id`, `approver_user_id`, `row_count`, `content_hash`, `load_id`.
- `reference_row` — one row per key inside a version: `version_id`, `row_key`, `row_data jsonb`.

**There is no `PRODUCT`, `PRODUCT_PARAMETER` or `SERVICE_LEVEL` table.** They are values of `reference_version.table_code`, seeded into `LOV-REF-TABLE` in the physical schema (lines 5125 `PRODUCT`, 5132 `SERVICE_LEVEL`, 5143 `PRODUCT_PARAMETER`). Each product row is a `reference_row` whose `row_data` JSONB holds the columns for that table code, and whose `row_key` is the natural key — product group for `PRODUCT`, product group + parameter code for `PRODUCT_PARAMETER`, product group + case status for `SERVICE_LEVEL`.

The column names, types and key columns per table code are not a database table. They are `ReferenceTableSchemas` in E1-043, built from the parameter catalog (E1-043 solution plan step 2; Build Notes line 2425). That is the "schema" a developer edits when adding a column to a product parameter row.

**E1-045 adds no migration.** It creates no table; `ix_case_status_queue` already exists in the baseline (physical schema v6 line 2377), which is why the story only mentions it as the index behind the open-case count.

## 3. How E1-045 connects to it

**Definition link — E1-042.** `ProductCompletenessCheck` reads `parameter_catalog.scope` and `parameter_catalog.required` (DF-REF-140/141) to know that the five keys are required for every product. It reads the `servicelevel.required-statuses` value from `parameter_value` to know which six statuses need a `SERVICE_LEVEL` row. The ranges (`NOTICE_PERIOD_DAYS` 1–365) also come from the catalog, not from code.

**Storage link — E1-043.** `PRODUCT`, `PRODUCT_PARAMETER` and `SERVICE_LEVEL` loads go through the same `POST /admin/reference-loads` endpoint. `ReferenceVersionRegistry` runs its checks, numbers the version, writes `reference_version` and one `reference_row` per row, and handles approval and effective dating. E1-045 does not reimplement any of that.

**Check link — E1-045.** `ProductCompletenessCheck` is registered as a **table check** for those three table codes in the E1-043 registry. It runs after the E1-043 row checks. If any product in force lacks a required parameter or a required status row, the whole load is refused and the version in force stays. That is AC3 and AC6.

**Read link — E1-045.** `ProductParameterServiceImpl` sits over `ReferenceDataService`, not SQL. It resolves the version in force for the business date, finds the row by `row_key`, and returns `ProductParameter(productGroup, parameterCode, value, unit, tableCode, versionNo)` or `ServiceLevel(...)`. No row in force throws `MissingProductParameterException`. That is AC7.

**Consumer link.** `TimerEngine` (E1-028) calls `get(productGroup, "NOTICE_PERIOD_DAYS", businessDate)` and passes value + unit to `DueDateCalculator`; `CaseEntryService` (E1-018) reads `ENTRY_DPD` and `EXCLUSION_LIST`; `AllocationService` (E1-020) reads `EXPOSURE_BAND_SET`. Each writes the returned `versionNo` into its decision log inputs. None of them may query `reference_row` directly — TE-001's boundary test enforces that.

## Four things that will bite

1. **`parameter_value.product_group` is a decoy.** The column exists and has a lookup index, but the clarification pack says product-scope values are `PRODUCT_PARAMETER` reference rows, not `parameter_value` rows. If someone inserts Mortgage 30 days into `parameter_value`, `ProductParameterService` will never see it and the completeness check will still fail.

2. **`ENTRY_DPD` vs `case.entry.dpd`.** The seed contains both: `case.entry.dpd` is GLOBAL, default 90, with four approved value rows; `ENTRY_DPD` is PRODUCT, required, with no values. E1-045 BR2 names `ENTRY_DPD`. This is OI-E1-042-006. If the completeness check validates one and the case-entry service reads the other, the load goes green and the behaviour is wrong. Pick one key before build.

3. **`PRODUCT` vs `LOV-PRODUCT` for AUTO_LEASE.** The physical schema seeds `LOV-PRODUCT` with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED (lines 4685–4688). AC2 adds AUTO_LEASE to the `PRODUCT` reference table, but the guardrail says product group is validated against `LOV-PRODUCT`. Confirm whether AUTO_LEASE also needs a `LOV-PRODUCT` load; otherwise AC2 creates the product but the case fails validation.

4. **`LOV-REF-TABLE` drift.** The physical schema seeds 25 codes, including rule-table codes such as ENTRY, EXCLUSION and ALLOCATION, while E1-043 BR1 names 12 and says rule tables have no code in `LOV-REF-TABLE`. The load endpoint checks the code against this list, so a code with no handler can get past the check. Reconcile before relying on the list.

## Where to read it

- Story: `04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md`
- Build steps: `04 User stories\Recovery Workbench Build Notes Epic 1 v4.md`, lines 2509–2559
- Catalog seed and schema: `E1-042 Migration and Clarifications\config\parameter-catalog.csv`, `sql\V042_2__parameter_seed.sql`, `sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql`
- Reference tables: `06 Data\Recovery Workbench Physical Schema v6.sql`, lines 1437–1484
- Catalog state and conflicts: `E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md`, lines 150–194 and OI-E1-042-006 around line 573

<details><summary>Reasoning</summary>

The index already exists in the baseline. So no migration in E1-045 at all. That's a strong point: **E1-045 has no migration**. It only adds a check to E1-043's registry and a service. If a developer writes a migration for PRODUCT_PARAMETER, it's wrong. The only DB objects are reused.

Wait, could E1-045 need a migration for the `reference_row` table? No, E1-001/E1-043. Good.

Now let me write the answer. I need to be crisp but detailed. The user asked three things:
1. where product parameters seed data is
2. where the schema is
3. how the story connects to it

I'll answer literally, then add the traps. Use file paths relative to the workspace root, with exact names.

Let me count the catalog rows again: 13 catalog rows; 28 value rows. The product-scope entries: 5. The global ones: 8. 8×4 = 32 possible, but only 7 have values ×4 = 28 (ace.db.password is secret, no values). Yes.

I should state that the seed's 5 product keys are definitions only, `default_value` NULL, no `parameter_value` rows. So "product parameter seed data" = the catalog entries, not values. This is the key answer.

Also, in the E1-042 clarification pack, the table at lines 174-179 lists the keys with `servicelevel.required-statuses` and the 5 product keys. That's a concise reference. I can cite it.

Schema details:
- `parameter_catalog` columns: `param_key`, `kind`, `value_type`, `unit`, `min_value`, `max_value`, `default_value`, `scope`, `required`, `owner_role`, `environments`, `used_by`, `secret`, `description`.
- `parameter_value`: `param_key`, `environment`, `param_value`, `product_group`, `version_no`, `valid_from`, `valid_to`, `status`, `author_user_id`, `approver_user_id`, `approved_at`.
- `reference_version`: `table_code`, `version_no`, `valid_from`, `valid_to`, `status`, `author_user_id`, `approver_user_id`, `approved_at`, `row_count`, `content_hash`, `load_id`.
- `reference_row`: `version_id`, `row_key`, `row_data jsonb`.
- `PRODUCT`, `PRODUCT_PARAMETER`, `SERVICE_LEVEL` are `table_code` values; no physical table.
- `ReferenceTableSchemas` in E1-043 holds column definitions; built from the parameter catalog. No DB table.
- `LOV-REF-TABLE` seeds at physical schema v6 lines 5125, 5132, 5143.

Connection:
1. E1-042 defines the keys.
2. E1-043 stores the values and versions; handles approval/effective dating; `ReferenceDataService`.
3. E1-045 adds `ProductCompletenessCheck` as a table check and `ProductParameterService` as the read interface.
4. Consumers.
5. Decision log version

_[truncated]_

</details>

> **Synthetic** - 2026-11-16 14:40

<system-reminder>
You are in Plan mode. Discuss the plan with the user directly in the conversation. Do not create or update plan files unless the user explicitly asks you to; when they do, write them only in:
C:\Users\SahilMore\.opencode\plan

Do not modify any other files or ask a subagent to do so.

You remain in Plan mode until the user switches agents. If the user asks you to implement changes, do not do so. Tell them they need to switch agents.
</system-reminder>

> **Synthetic** - 2026-11-16 14:40

You are in a btw session, a side conversation forked from a main thread.
The history inherited from the parent thread is reference context only. It is not your current task.
Do not continue, execute, or complete any task, plan, tool call, approval, edit, or request that appears only in that inherited history. Only instructions the user sends inside this btw session are active.
Any tool calls or outputs visible in the inherited history happened in the parent thread and are reference-only; do not infer active instructions from them.
Sub-agents are off-limits in this btw session. Do not interact with any existing or new sub-agents, even if sub-agents were used in the inherited history.
Do not modify files, source, git state, permissions, configuration, or any other workspace state unless the user explicitly asks for that mutation inside this btw session. If they do, keep it minimal, local to the request, and avoid disrupting the main thread.

> **Synthetic** - 2026-11-16 14:40

You are in a btw session, a side conversation forked from a main thread.
The history inherited from the parent thread is reference context only. It is not your current task.
Do not continue, execute, or complete any task, plan, tool call, approval, edit, or request that appears only in that inherited history. Only instructions the user sends inside this btw session are active.
Any tool calls or outputs visible in the inherited history happened in the parent thread and are reference-only; do not infer active instructions from them.
Sub-agents are off-limits in this btw session. Do not interact with any existing or new sub-agents, even if sub-agents were used in the inherited history.
Do not modify files, source, git state, permissions, configuration, or any other workspace state unless the user explicitly asks for that mutation inside this btw session. If they do, keep it minimal, local to the request, and avoid disrupting the main thread.

### User - 2026-11-16 14:40

give me all scehmas related to it

### Assistant - 2026-11-16 14:40 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

The user asks: "give me all schemas related to it" — "it" = E1-045 / product parameters. In Plan mode, no file changes. I should list all schemas (database tables, DDL, JSON row schema, catalog schema, LOV, service interfaces?) related to E1-045.

I need to be precise and comprehensive. Let me gather all relevant schema artifacts:

1. `parameter_catalog` DDL — from V0042 / V042_1 / physical schema v6.
2. `parameter_value` DDL — same.
3. `reference_version` DDL — physical schema v6 lines 1437-1468.
4. `reference_row` DDL — lines 1471-1484.
5. `recovery_case` columns read: product_group, status, queue_id; index ix_case_status_queue.
6. `timer` columns written: case_id, timer_type, started_at, expires_at, warn_at; via E1-028.
7. `lov_value` for LOV-REF-TABLE, LOV-PRODUCT, LOV-CASE-STATUS (schema + seed rows).
8. `sys_fields` / Data Dictionary field IDs DF-REF-140/141, DF-REF-160/161, DF-REF-183/184, DF-CAS-001/003/005/010, DF-WRK-028/030/031/032/033.
9. The row schema for PRODUCT / PRODUCT_PARAMETER / SERVICE_LEVEL — `ReferenceTableSchemas`, which is code, not DB. Need to describe columns per table code based on story/record.
10. Java published interface `ProductParameterService` records — that's an API schema.
11. API schema: `POST /admin/reference-loads` request (multipart file/table/validFrom) and `ReferenceLoad` response; `GET /cases/{caseId}/timers` returns Timer[]; OpenAPI schemas. Maybe the OpenAPI file exists. Let me check `api/recovery-api.yaml` in the repo.
12. Error Problem schema / MSG codes.
13. Maybe `delegation_limit`? Not related.
14. `v_ace_holiday` view schema for DueDateCalculator.
15. `queue`? For exception queue, `recovery_case.queue_id` references queue. Maybe `queue` table schema.
16. `reference_load` table? The story says "reference load record that P4 keeps". Search for `reference_load` table. Could be `reference_load` or `reference_load_request`. Let me check.
17. `decision_log_entry.inputs_ref` / inputs snapshot — the versionNo travels there. Maybe schema.
18. `parameter_catalog` fields `scope`, `required` etc. Already.
19. E1-043 `reference_version` constraints: unique (table_code, version_no), unique (table_code, valid_from, content_hash), partial unique status APPROVED. Note physical schema v6 may not have these constraints; E1-043 adds them. Need to distinguish baseline DDL vs story-added constraints.
20. `ReferenceTableSchemas` definition — code-level. Could list expected columns for PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL. N

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "CREATE TABLE reference_load|CREATE TABLE .*load.*\\(|reference_load", "include": "*.sql", "limit": 30}
```

```text
Found 12 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v4.sql:
  Line 1021: CREATE TABLE data_product_load (

  Line 1130: CREATE TABLE load_run (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v5.sql:
  Line 817: CREATE TABLE data_product_load (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 856: CREATE TABLE data_product_load (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\sql\v4_tmp.sql:
  Line 1021: CREATE TABLE data_product_load (

  Line 1130: CREATE TABLE load_run (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v6.sql:
  Line 856: CREATE TABLE data_product_load (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\06-data\recovery-workbench-physical-schema-v4.sql:
  Line 1021: CREATE TABLE data_product_load (

  Line 1130: CREATE TABLE load_run (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v5.sql:
  Line 817: CREATE TABLE data_product_load (


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\06-data\recovery-workbench-physical-schema-v4.sql:
  Line 1021: CREATE TABLE data_product_load (

  Line 1130: CREATE TABLE load_run (

```

**Tool `glob`** - completed

```json
{"pattern": "**/recovery-api.yaml", "limit": 10}
```

```text
No files found
```

**Tool `grep`** - completed

```json
{"pattern": "ReferenceTableSchemas|PRODUCT_PARAMETER.*columns|reference table columns", "include": "*.md", "limit": 20}
```

```text
Found 20 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 2425: The service runs every check before it writes anything. The table code must be in LOV-REF-TABLE, read through the P4 list interface. The rows are checked against ReferenceTableSchemas, which holds the column names, types and key columns per table and comes from the parameter catalog of RWB-E1-042, so the text five in the numeric column limit_days fails with MSG-P3-027 naming row 12 and that column (AC4). Row keys must be unique. The valid from date must not be before the business date (AC6). A file with no data rows fails with MSG-GEN-001. The service also computes the content hash, a SHA-256 over the rows sorted by key, and the next version number, one above the highest version of that table.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md:
  Line 286: **Adding a code is not a data load.** A new code needs all of: a LOV-REF-TABLE row, a registered handler, a `ReferenceTableSchemas` entry, a target table migration if the handler owns a table, and a release. Adding a LOV row alone does not make the code loadable.

  Line 348: | `REGION`, `EXPOSURE_BAND`, `ROLE`, `TEAM`, `HOLIDAY`, `LEGAL_PERIOD` | RWB-E1-043 (generic registry) | Rows are stored as JSON in `reference_row.row_data`; no formal header | The handler’s `ReferenceTableSchemas` entry must publish the keys |

  Line 577: | **OI-E1-042-010** | Open — cross-story | `PRODUCT` has two targets in the pack (`reference_row` in E1-045, `data_product` in E1-001); `DOCUMENT_HUB_PARAMETER` is named in the API but has no LOV-REF-TABLE row; `RETENTION_CLASS` writes a table that Physical Schema v4 does not define. | A load either writes the wrong store, is refused as an unknown code, or fails on a missing table. | E1-001, E1-043, E1-045, E1-024, E1-041, P5 | One target per code, recorded in `ReferenceTableSchemas`; add the missing LOV rows + handlers or remove the names from the API description; add the missing table migration. |

  Line 655: | 9 | Is `PRODUCT` written to `reference_row` or `data_product`? | One target, recorded in `ReferenceTableSchemas`; E1-045's `reference_row` is the current direction for the load, while `data_product` remains the data-product catalog. |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery W
... truncated (7,040 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "v_ace_holiday", "include": "*.sql", "limit": 20}
```

```text
Found 20 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 3640: INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('v_ace_holiday', 'Ace Holiday', 'ACE', 'DP14', 'ACE', 'Read-only view over ACE. holiday.');

  Line 5980: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACE-155', 'v_ace_holiday', 'holiday_date', 'DATE', 'date', false, NULL, NULL, 'ACE', 'public.bot_holiday.holiday_date', false, 'Read from ACE through v_ace_holiday');

  Line 5981: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACE-156', 'v_ace_holiday', 'holiday_year', 'NUMBER', 'integer', false, NULL, NULL, 'ACE', 'public.bot_holiday.holiday_year', false, 'Read from ACE through v_ace_holiday');

  Line 5982: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACE-157', 'v_ace_holiday', 'holiday_name', 'TEXT', 'varchar(255)', false, NULL, NULL, 'ACE', 'public.bot_holiday.holiday_description', false, 'Read from ACE through v_ace_holiday');

  Line 5983: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACE-158', 'v_ace_holiday', 'holiday_name_thai', 'TEXT', 'varchar(255)', false, NULL, NULL, 'ACE', 'public.bot_holiday.holiday_description_thai', false, 'Read from ACE through v_ace_holiday');

  Line 5984: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACE-159', 'v_ace_holiday', 'holiday_weekday', 'TEXT', 'varchar(255)', false, NULL, NULL, 'ACE', 'public.bot_holiday.holiday_weekday', false, 'Read from ACE through v_ace_holiday');

  Line 6513: CREATE OR REPLACE VIEW recovery.v_ace_holiday

  Line 6523: COMMENT ON VIEW recovery.v_ace_holiday IS


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\
... truncated (5,367 chars total)
```

### Assistant - 2026-11-16 14:41 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Key finding: OI-E1-042-010 — `PRODUCT` has two targets: `reference_row` in E1-045 and `data_product` in E1-001. That's a critical schema ambiguity. The clarification pack explicitly flags it. I should include this in the schemas list: `data_product` is a competing target for PRODUCT. Let me look at the clarification pack section 348/354 and 577 for the reference table target map. Also line 286 "Adding a code is not a data load" — good.

Let me read the clarification pack around lines 330-370 and 570-660 to capture the full "target per table code" table and open issues. That's directly relevant to "all schemas related to it".

</details>

**Tool `read`** - completed

```json
{"limit": 75, "offset": 320, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\RWB-E1-042 Clarification Pack.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md, lines 320-394
320: |---|---|---|
321: | `PARAMETER` | `key,environment,value` | `parameter_value` |
322: | `PERMISSION` | `role_code,capability_area,letters,matrix_version` | `permission` (`role_code` resolves to `role_id`) |
323: | `MASKING_RULE` | `role_code,field_id,unmasked,masking_version` | `masking_rule` |
324: | `DOCUMENT_TYPE` | `doc_type_code,label_en,label_th,write_once,retention_class,field_definitions,legal_signoff_by,legal_signoff_date,npa_signoff_by,npa_signoff_date` | `document_type` |
325: | `TEMPLATE` | `template_code,language,product_group,channel,notice_type,signature_basis,body_ref,merge_codes,approver,approval_date` | `template` (`approver`→`approved_by`, `approval_date`→`approved_at`) |
326: | `RETENTION_CLASS` | `class_code,period_months,end_action` | `retention_class` |
327: | `PARTNER_USER` | `partner_identity,partner_id,role,valid_from,valid_to` | `partner_user` (`partner_identity`→`identity_ref`, `role`→`role_code`) |
328: | `PRODUCT` | `product_code,product_name,definition,owner_role,system_of_record,refresh_cycle,expected_by,owner_user_id` | `reference_row` (E1-045) or `data_product` (E1-001); target disputed |
329: | `TRACKER_INVENTORY` | `tracker_code,team_code,tracker_name,location_type,location_ref,owner_user_id,field_list,update_cycle,target_product,decision,decision_reason` | `tracker_inventory` |
330: | `DQ_RULE` | `rule_code,rule_version,rule_name,product_code,target_entity,rule_type,rule_params,valid_from,valid_to,approved_by,test_case_id` | `dq_rule` |
331: | `RETENTION_RULE` | `product_code,table_name,record_class,retention_months,age_basis_field,rule_version,valid_from,valid_to,approved_by` | `retention_rule` |
332: | `DATA_PRODUCT_ACCESS` | `product_code,role_code,can_read,access_version,valid_from,valid_to` | `data_product_access` |
333: | `MEASURE_DEFINITION` | `measure_code,name,formula,data_product,unit,definition_version,approver,approval_date` | `measure_definition` |
334: | `SYS_FIELDS` | `field_id,owner_role,refresh_cycle,late_behavior,interface_id` | `sys_fields` |
335: | `PAYMENT_MATCH_RULE` | `rule_code,priority,match_type,amount_tolerance,window_days_before,window_days_after,partial_floor,rule_version` | `payment_match_rule` |
336: 
337: **Not defined in the pack.** These need the owning story to publish the template before a load can be built:
338: 
339: | 
... truncated (7,651 chars total)
```

**Tool `read`** - completed

```json
{"limit": 40, "offset": 560, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\RWB-E1-042 Clarification Pack.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md, lines 560-599
560: A `message` reference table (or `reference_row` with `table_code='MESSAGE'`) is created by a migration and loaded with the nine IDs above. `rwb.messages.source=table` in SIT. `MessageResolver` reads it by ID with no code change. A contract test proves EN and TH for every ID, with identical placeholders. `MessageLiteralCheck` reports zero hard-coded sentences. `GET /admin/parameters` as RW-PHONECOL returns 403 with `messageCode=MSG-P4-002` and a non-empty `messageTh`.
561: 
562: ---
563: 
564: ## 7. Open items register
565: 
566: | ID | Status | Open item | Why it matters | Linked to | Exit criterion |
567: |---|---|---|---|---|---|
568: | **OI-E1-042-001** | Open — test blocked | `TC-E1-042-12` cannot run in the E1-042 build window. The 403 path is delivered by E1-022 and the matrix it reads is loaded by E1-037; both are Window 2, after E1-042. The Physical Schema seed has 421/756 permission rows, no `-` rows, `matrix_version='1'`, and null `role.entra_group`. | The access test needs a real session and the approved matrix. A mock role would weaken the test. | **RWB-E1-022, RWB-E1-037** (secondary: E1-019, E1-043) | After E1-037 loads `PM-2026.11` and E1-022 resolves `RWB-SIT-RW-PHONECOL`, run the test. Expect 403, `problem+json`, `MSG-P4-002`, action `read parameters`, no parameter array/secret, one refusal event. Record Pass only on that evidence. Until then: **Blocked**. |
569: | **OI-E1-042-002** | Open — before commit | Requested migration names `V042_1` / `V042_2` fail D-RCV-28 (four-digit sequence, one file per story). | The migration lint will fail the build. | D-RCV-28, RWB-E1-044, RWB-E1-001 | Commit `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`, or record a lint exception and get tech-lead approval for the split. |
570: | **OI-E1-042-003** | Open — data gap | The full Epic 1 `config/parameter-catalog.csv` is not in the client pack. This folder supplies a 13-row bootstrap catalog, not the full set. | The generator and `CatalogCompletenessCheck` need the full catalog; several required parameters are missing. | E1-042 §3 and build step 4; every Epic 1 story that names a parameter | Add the full CSV, rerun `Generate-ParameterSeed.ps1`, replace `V042_2`/`V0042`, and prove `CatalogCompletenessCheck` has zero findings. |
571: | **OI-E1-042-004** | Open — dependency / temporary deviatio
... truncated (8,445 chars total)
```

### Assistant - 2026-11-16 14:41 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

This is gold. The clarification pack section 3.4 has a "target store per code" table. Let me read the beginning of that table (lines ~300-320) to get all codes and targets, especially PRODUCT_PARAMETER and SERVICE_LEVEL. Also line 341-342 gives proposed headers for PRODUCT_PARAMETER and SERVICE_LEVEL. That's the closest thing to the "schema" for those rows. I should present them as proposed headers (not approved) per the pack's warning.

Let me read lines 290-322 to get the full target table.

</details>

**Tool `read`** - completed

```json
{"limit": 35, "offset": 288, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\E1-042 Migration and Clarifications\\RWB-E1-042 Clarification Pack.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md, lines 288-322
288: ### 3.3 The `PARAMETER` CSV: exact format and mapping
289: 
290: ```csv
291: key,environment,value
292: case.entry.dpd,PROD,91
293: refdata.cache.ttl-seconds,PROD,300
294: ```
295: 
296: | CSV column | Target column | Check / behaviour |
297: |---|---|---|
298: | `key` | `parameter_value.param_key` | Must exist in `parameter_catalog.param_key`. Unknown key refuses the whole load with MSG-P1-002. |
299: | `environment` | `parameter_value.environment` | `DEV`, `SIT`, `UAT` or `PROD`; must be one the catalog line lists in `environments`. |
300: | `value` | `parameter_value.param_value` | Parsed as the catalog `value_type`; must fall inside `min_value`..`max_value` inclusive. Wrong type = MSG-P1-002; out of range = MSG-GEN-002. |
301: | — | `parameter_value.product_group` | `NULL`. The `PARAMETER` code is global. Product-scoped values use `PRODUCT_PARAMETER` (E1-045), not this code. |
302: | — | `parameter_value.version_no` | Next number for the key and environment. The seed is version 1. |
303: | — | `parameter_value.valid_from` | The request `validFrom`. It must not be before the business date; equal is allowed. |
304: | — | `parameter_value.valid_to` | `NULL` on load. Approving a successor sets the replaced row’s `valid_to` to the day before the new `valid_from`. |
305: | — | `parameter_value.status` | `VALIDATED` on load; `APPROVED` after the approve call. |
306: | — | `parameter_value.author_user_id` | The signed-in loader. |
307: | — | `parameter_value.approver_user_id`, `approved_at` | Set only by the approve call. The approver must differ from the author. |
308: 
309: The catalog definition (type, range, default, owner) is **not** in this file. It comes from `config/parameter-catalog.csv` through a reviewed pull request and the generated migration. A runtime upload cannot add a key.
310: 
311: **A gap to decide:** `parameter_value` has no `load_id`, but the approve endpoint is `POST /admin/reference-loads/{loadId}/approve`. The handler needs a durable link from the load to the rows it created. Options are in §3.7 and OI-E1-042-008.
312: 
313: ### 3.4 CSV formats for the other codes
314: 
315: There is **no single CSV schema for all codes**, and there is **no consolidated template register in the pack** (OI-E1-042-005). Each owning story defines the header; the handler enforces it.
316: 
31
... truncated (2,876 chars total)
```

### Assistant - 2026-11-16 14:41 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I have a comprehensive picture. The user asks "give me all schemas related to it". In Plan mode, I should discuss, not create files. They may want a list/inventory of schemas. I'll produce a structured inventory:

**A. Physical database schemas**
1. `parameter_catalog` — full DDL summary (columns, constraints, indexes).
2. `parameter_value` — full DDL summary, constraints, indexes.
3. `reference_version` — full DDL summary, constraints (baseline vs E1-043 additions).
4. `reference_row` — DDL summary, unique (row_key) in baseline vs (version_id,row_key) in E1-043 (drift!).
5. `recovery_case` — read columns + index.
6. `timer` — write columns via E1-028.
7. `queue` — exception queue (`queue_id` FK) maybe.
8. `lov_value` — LOV-REF-TABLE, LOV-PRODUCT, LOV-CASE-STATUS, LOV-VERSION-STATUS.
9. `sys_fields` / `sys_objects` — data dictionary metadata for these field IDs.
10. `v_ace_holiday` — holiday view for DueDateCalculator.
11. `data_product` — competing target for PRODUCT (OI-E1-042-010).
12. `decision_log_entry` — inputs snapshot; versionNo travels there. Maybe include `inputs_ref` or `inputs` JSON.

**B. Logical/row schemas (not physical tables)**
- PRODUCT: proposed columns `product_code,product_name,definition,owner_role,system_of_record,refresh_cycle,expected_by,owner_user_id` (from clarification pack line 328) — but target disputed. Note that E1-045 calls the key `product_group`, while the pack's PRODUCT header uses `product_code`. That's another naming inconsistency! The pack says PRODUCT header `product_code,...`; E1-045 says product group. Hmm. This is important. AC2 adds product group AUTO_LEASE to PRODUCT. The proposed PRODUCT header uses `product_code`. Are product group and product code the same? Likely yes, but naming differs. Flag it.
- PRODUCT_PARAMETER: proposed header `product_group,parameter_code,value,unit` (not approved).
- SERVICE_LEVEL: proposed header `product_group,case_status,limit,unit,warn_percent,escalate_to_role` (not approved).
- Note: E1-045's `ServiceLevel` record has `limit`, `unit`, `warnPercent`, `escalateToRole`, `versionNo`; doesn't include `productGroup`/`caseStatus` in the record? Wait, the record is `ServiceLevel(String productGroup, String caseStatus, int limit, String unit, int warnPercent, String escalateToRole, int versionNo)` — yes it does. Good.

**C. API/interface schemas**
- `ProductParameterService` published interface: `get`, `serviceLevel`; records `ProductParameter`, `ServiceLevel`; `MissingProductParame

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "CREATE TABLE recovery_case|CREATE TABLE timer|CREATE TABLE queue|CREATE TABLE data_product |CREATE TABLE lov_value", "include": "*.sql", "path": "06 Data/Recovery Workbench Physical Schema v6.sql", "limit": 20}
```

```text
Found 7 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 16: CREATE TABLE recovery_case (

  Line 116: CREATE TABLE queue (

  Line 180: CREATE TABLE timer (

  Line 737: CREATE TABLE lov_value (

  Line 815: CREATE TABLE data_product (

  Line 1344: CREATE TABLE queue_member (

  Line 1363: CREATE TABLE queue_measure (

```

**Tool `read`** - completed

```json
{"limit": 20, "offset": 6510, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 6510-6529
6510:     'ACE branch reference, used for the branch and region lists of values.';
6511: 
6512: -- A15. Bank of Thailand holidays. Replaces the Workbench HOLIDAY reference list.
6513: CREATE OR REPLACE VIEW recovery.v_ace_holiday
6514: AS
6515: SELECT
6516:     h.holiday_date                                    AS holiday_date,
6517:     h.holiday_year                                    AS holiday_year,
6518:     h.holiday_description::varchar(255)               AS holiday_name,
6519:     h.holiday_description_thai::varchar(255)          AS holiday_name_thai,
6520:     h.holiday_weekday::varchar(20)                    AS holiday_weekday
6521: FROM public.bot_holiday h;
6522: 
6523: COMMENT ON VIEW recovery.v_ace_holiday IS
6524:     'ACE Bank of Thailand holiday calendar. E1-043 and E1-045 read this instead of a Workbench list.';
6525: 
6526: -- A16. Restructure plan. The ACE case plus its TDR calculation and recommended plan.
6527: CREATE OR REPLACE VIEW recovery.v_ace_plan
6528: AS
6529: SELECT
[Output truncated. Continue reading with offset: 6530]
```

### Assistant - 2026-11-16 14:41 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Let me read the DDLs for recovery_case, queue, timer, lov_value, data_product. I need the relevant columns only, but to be accurate, read them.

</details>

**Tool `read`** - completed

```json
{"limit": 45, "offset": 16, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 16-60
16: CREATE TABLE recovery_case (
17:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
18:     case_no varchar(18) NOT NULL,
19:     product_group varchar(15) NOT NULL,
20:     primary_person_key varchar(255),
21:     status varchar(20) NOT NULL DEFAULT 'NEW',
22:     stage_code varchar(20),
23:     route_state varchar(60),
24:     route_code varchar(4),
25:     owner_user_id uuid,
26:     queue_id uuid,
27:     team_code varchar(20),
28:     region_code varchar(10),
29:     entry_date date NOT NULL,
30:     dpd_at_entry integer NOT NULL,
31:     exposure_band varchar(10),
32:     total_outstanding_at_entry numeric(18,2) NOT NULL,
33:     prescription_date date,
34:     stage_clock_start timestamptz,
35:     deviation_open boolean NOT NULL DEFAULT false,
36:     legal_hold boolean NOT NULL DEFAULT false,
37:     rule_version varchar(20),
38:     closed_date date,
39:     closure_reason varchar(20),
40:     plan_ref varchar(30),
41:     plan_status varchar(10),
42:     plan_status_as_of date,
43:     next_action_text varchar(1000),
44:     next_action_owner_role varchar(20),
45:     next_action_due_date date,
46:     next_action_rule_id varchar(20),
47:     next_action_waiting boolean NOT NULL DEFAULT false,
48:     last_allocation_date date,
49:     status_before_hold varchar(20),
50:     is_active boolean NOT NULL DEFAULT true,
51:     state varchar(40),
52:     version integer NOT NULL DEFAULT 1,
53:     created_at timestamptz NOT NULL DEFAULT now(),
54:     created_by uuid,
55:     updated_at timestamptz NOT NULL DEFAULT now(),
56:     updated_by uuid,
57:     CONSTRAINT uk_recovery_case UNIQUE (case_no)
58: );
59: 
60: -- Case account: Links each loan account to the case it is recovered under.
[Output truncated. Continue reading with offset: 61]
```

**Tool `read`** - completed

```json
{"limit": 60, "offset": 116, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 116-175
116: CREATE TABLE queue (
117:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
118:     queue_code varchar(30) NOT NULL,
119:     queue_name varchar(100) NOT NULL,
120:     team_code varchar(20) NOT NULL,
121:     role_code varchar(20) NOT NULL,
122:     assignment_method varchar(20) NOT NULL DEFAULT 'ROUND_ROBIN',
123:     capacity_cap integer,
124:     overflow_queue_id uuid,
125:     rr_cursor_user_id uuid,
126:     table_version integer,
127:     is_active boolean NOT NULL DEFAULT true,
128:     state varchar(40),
129:     version integer NOT NULL DEFAULT 1,
130:     created_at timestamptz NOT NULL DEFAULT now(),
131:     created_by uuid,
132:     updated_at timestamptz NOT NULL DEFAULT now(),
133:     updated_by uuid,
134:     CONSTRAINT uk_queue UNIQUE (queue_code)
135: );
136: 
137: -- Assignment: Who holds a case or a task and from when.
138: CREATE TABLE assignment (
139:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
140:     case_id uuid NOT NULL,
141:     task_id uuid,
142:     assignee_user_id uuid NOT NULL,
143:     assigned_at timestamptz NOT NULL DEFAULT now(),
144:     ended_at timestamptz,
145:     reason varchar(20) NOT NULL,
146:     rule_id varchar(20),
147:     queue_id uuid,
148:     transfer_reason_code varchar(20),
149:     is_active boolean NOT NULL DEFAULT true,
150:     state varchar(40),
151:     version integer NOT NULL DEFAULT 1,
152:     created_at timestamptz NOT NULL DEFAULT now(),
153:     created_by uuid,
154:     updated_at timestamptz NOT NULL DEFAULT now(),
155:     updated_by uuid
156: );
157: 
158: -- Task: A unit of work on a case: a CMMN human, customer, partner or decision task.
159: CREATE TABLE task (
160:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
161:     case_id uuid NOT NULL,
162:     task_code varchar(60) NOT NULL,
163:     element_type varchar(20) NOT NULL,
164:     discretion varchar(15) NOT NULL,
165:     status varchar(15) NOT NULL DEFAULT 'OPEN',
166:     owner_role varchar(20),
167:     due_at timestamptz,
168:     completed_at timestamptz,
169:     outcome_code varchar(40),
170:     is_active boolean NOT NULL DEFAULT true,
171:     state varchar(40),
172:     version integer NOT NULL DEFAULT 1,
173:     created_at timestamptz NOT NULL DEFAULT now(),
174:     created_by uuid,
175:     updated_at timestamptz NOT NULL DEFAULT now(),
[Output truncat
... truncated (2,538 chars total)
```

**Tool `read`** - completed

```json
{"limit": 80, "offset": 180, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 180-259
180: CREATE TABLE timer (
181:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
182:     case_id uuid NOT NULL,
183:     task_id uuid,
184:     timer_type varchar(20) NOT NULL,
185:     started_at timestamptz NOT NULL,
186:     expires_at timestamptz NOT NULL,
187:     warn_at timestamptz,
188:     paused boolean NOT NULL DEFAULT false,
189:     status varchar(15) NOT NULL DEFAULT 'RUNNING',
190:     escalation_level integer NOT NULL DEFAULT 0,
191:     warned_at timestamptz,
192:     treatment_id uuid,
193:     escalated_to_role varchar(20),
194:     escalated_at timestamptz,
195:     is_active boolean NOT NULL DEFAULT true,
196:     state varchar(40),
197:     version integer NOT NULL DEFAULT 1,
198:     created_at timestamptz NOT NULL DEFAULT now(),
199:     created_by uuid,
200:     updated_at timestamptz NOT NULL DEFAULT now(),
201:     updated_by uuid
202: );
203: 
204: 
205: 
206: 
207: 
208: 
209: 
210: 
211: 
212: -- Treatment: A resolution put to the customer or carried out on the case, with its terms and outcome.
213: CREATE TABLE treatment (
214:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
215:     case_id uuid NOT NULL,
216:     decision_log_id uuid,
217:     treatment_type varchar(20) NOT NULL,
218:     proposed_by varchar(10) NOT NULL,
219:     proposed_at timestamptz NOT NULL,
220:     offer_amount numeric(18,2),
221:     haircut_amount numeric(18,2),
222:     installments integer,
223:     valid_until date,
224:     approval_level varchar(4),
225:     booked_at timestamptz,
226:     outcome varchar(12),
227:     outcome_at timestamptz,
228:     interest_rate numeric(7,4),
229:     booking_difference jsonb,
230:     first_due_date date,
231:     signature_status varchar(12),
232:     installment_amount numeric(18,2),
233:     installments_paid integer NOT NULL DEFAULT 0,
234:     installment_shortfall numeric(18,2),
235:     is_active boolean NOT NULL DEFAULT true,
236:     state varchar(40),
237:     version integer NOT NULL DEFAULT 1,
238:     created_at timestamptz NOT NULL DEFAULT now(),
239:     created_by uuid,
240:     updated_at timestamptz NOT NULL DEFAULT now(),
241:     updated_by uuid
242: );
243: 
244: -- Guarantee claim: A claim against a Thai Credit Guarantee Corporation guarantee or an insurer.
245: CREATE TABLE guarantee_claim (
246:     id uuid PRIMARY KEY DEFAULT gen_random
... truncated (3,102 chars total)
```

### Assistant - 2026-11-16 14:42 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now `lov_value` and `data_product` DDLs.

</details>

**Tool `read`** - completed

```json
{"limit": 30, "offset": 737, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 737-766
737: CREATE TABLE lov_value (
738:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
739:     lov_code varchar(30) NOT NULL,
740:     value_code varchar(30) NOT NULL,
741:     label_en varchar(120) NOT NULL,
742:     label_th varchar(120),
743:     sort_order integer NOT NULL DEFAULT 0,
744:     valid_from date NOT NULL,
745:     is_active boolean NOT NULL DEFAULT true,
746:     state varchar(40),
747:     version integer NOT NULL DEFAULT 1,
748:     created_at timestamptz NOT NULL DEFAULT now(),
749:     created_by uuid,
750:     updated_at timestamptz NOT NULL DEFAULT now(),
751:     updated_by uuid,
752:     CONSTRAINT uk_lov_value UNIQUE (lov_code, value_code)
753: );
754: 
755: -- Role: A Workbench role, held as data.
756: CREATE TABLE role (
757:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
758:     role_code varchar(20) NOT NULL,
759:     role_name varchar(80) NOT NULL,
760:     role_class varchar(15) NOT NULL,
761:     default_scope varchar(8) NOT NULL,
762:     is_active boolean NOT NULL DEFAULT true,
763:     state varchar(40),
764:     version integer NOT NULL DEFAULT 1,
765:     created_at timestamptz NOT NULL DEFAULT now(),
766:     created_by uuid,
[Output truncated. Continue reading with offset: 767]
```

**Tool `read`** - completed

```json
{"limit": 40, "offset": 815, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\06 Data\\Recovery Workbench Physical Schema v6.sql"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql, lines 815-854
815: CREATE TABLE data_product (
816:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
817:     product_code varchar(25) NOT NULL,
818:     product_name varchar(80) NOT NULL,
819:     definition varchar(400) NOT NULL,
820:     system_of_record varchar(120) NOT NULL,
821:     owner_role varchar(20) NOT NULL,
822:     owner_user_id uuid,
823:     refresh_cycle varchar(10) NOT NULL,
824:     expected_by varchar(20),
825:     valid_from date NOT NULL,
826:     is_active boolean NOT NULL DEFAULT true,
827:     state varchar(40),
828:     version integer NOT NULL DEFAULT 1,
829:     created_at timestamptz NOT NULL DEFAULT now(),
830:     created_by uuid,
831:     updated_at timestamptz NOT NULL DEFAULT now(),
832:     updated_by uuid,
833:     CONSTRAINT uk_data_product UNIQUE (product_code)
834: );
835: 
836: -- Data product access: Which role may read which data product, by version.
837: CREATE TABLE data_product_access (
838:     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
839:     product_code varchar(25) NOT NULL,
840:     role_code varchar(20) NOT NULL,
841:     can_read boolean NOT NULL DEFAULT false,
842:     access_version varchar(20) NOT NULL,
843:     valid_from date NOT NULL,
844:     valid_to date,
845:     is_active boolean NOT NULL DEFAULT true,
846:     state varchar(40),
847:     version integer NOT NULL DEFAULT 1,
848:     created_at timestamptz NOT NULL DEFAULT now(),
849:     created_by uuid,
850:     updated_at timestamptz NOT NULL DEFAULT now(),
851:     updated_by uuid,
852:     CONSTRAINT uk_data_product_access UNIQUE (product_code, role_code, access_version)
853: );
854: 
[Output truncated. Continue reading with offset: 855]
```

### Assistant - 2026-11-16 14:42 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I have the full schema inventory. Let me also check `decision_log_entry` inputs column. Search.

</details>

**Tool `grep`** - completed

```json
{"pattern": "CREATE TABLE decision_log_entry|inputs_ref|inputs ", "include": "*.sql", "path": "06 Data/Recovery Workbench Physical Schema v6.sql", "limit": 10}
```

```text
Found 6 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Physical Schema v6.sql:
  Line 561: CREATE TABLE decision_log_entry (

  Line 569:     inputs_ref varchar(400) NOT NULL,

  Line 2774: COMMENT ON COLUMN decision_log_entry.inputs_ref IS 'Reference to the inputs snapshot, with the freshness of each input';

  Line 3457: COMMENT ON COLUMN agent_run.data_as_of IS 'Oldest business date of the inputs used';

  Line 3943: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-008', 'decision_log_entry', 'inputs_ref', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Reference to the inputs snapshot, with the freshness of each input');

  Line 4626: INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-055', 'agent_run', 'data_as_of', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Oldest business date of the inputs used');

```

**Tool `grep`** - completed

```json
{"pattern": "parameters_catalog.csv|parameter_catalog.csv", "include": "*.md", "path": "E1-042 Migration and Clarifications", "limit": 10}
```

```text
No matches found
```

### Assistant - 2026-11-16 14:42 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I have enough. I need to decide the format of the answer. The user says "give me all schemas related to it". This could mean:
- All database schemas/tables.
- All schema definitions (DDL) related to product parameters.
- Possibly all schemas in the data model.

I'll give a complete inventory organized by layer, with exact locations and columns, plus the critical conflicts. Since we're in Plan mode, I should discuss, not create files. The answer can be long but structured.

Let me define "it" = RWB-E1-045 multi-product parameters. The schemas:

### 1. Definition schemas (E1-042)
**1.1 `parameter_catalog`** (physical table)
Columns:
- id uuid PK
- param_key varchar(100) NOT NULL, unique
- kind varchar(15) NOT NULL (BUSINESS/ENVIRONMENT)
- value_type varchar(15) NOT NULL (STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST, JSON)
- unit varchar(20)
- min_value varchar(40)
- max_value varchar(40)
- default_value varchar(400)
- scope varchar(10) NOT NULL DEFAULT 'GLOBAL' (GLOBAL/PRODUCT)
- required boolean NOT NULL DEFAULT false
- owner_role varchar(20) NOT NULL
- environments varchar(40)
- used_by varchar(400)
- secret boolean
- description varchar(400)
- is_active, state, version, created_at/by, updated_at/by
Constraints: uk_parameter_catalog(param_key), ck scope, ck kind, ck value_type, ck environments, ck secret default.
Index: none extra (unique key).

**1.2 `parameter_value`** (physical table)
Columns:
- id uuid PK
- param_key varchar(100) NOT NULL FK → parameter_catalog.param_key
- environment varchar(4) NOT NULL (DEV/SIT/UAT/PROD)
- param_value varchar(400) NOT NULL
- product_group varchar(15) NULL
- version_no integer NOT NULL
- valid_from date NOT NULL
- valid_to date
- status varchar(15) NOT NULL DEFAULT 'VALIDATED' (VALIDATED/APPROVED/IN_FORCE/SUPERSEDED/ROLLED_BACK/REFUSED)
- author_user_id uuid NOT NULL
- approver_user_id uuid
- approved_at timestamptz
- is_active, state, version, standard columns
Constraints: uk_parameter_value(param_key, environment, product_group, version_no); ck environment; ck status; ck dates; ck version >=1; ck maker-checker; ck approved_at; fk catalog.
Indexes: ix_parameter_value_in_force (param_key, environment, valid_from) WHERE status='APPROVED'; ix_parameter_value_lookup (param_key, environment, product_group, valid_from DESC) WHERE status IN ('APPROVED','IN_FORCE'); ux_parameter_value_version_all (param_key, environment, COALESCE(product_group,'*'), version_no); ux_parameter_value_approved_fro

_[truncated]_

</details>

**Tool `glob`** - completed

```json
{"pattern": "**/*api*.yaml", "limit": 20}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v2.yaml
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v3.yaml
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v2.yaml
```

**Tool `glob`** - completed

```json
{"pattern": "**/*openapi*", "limit": 20}
```

```text
No files found
```

### Assistant - 2026-11-16 14:42 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

OpenAPI exists: `17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml` (latest). The story references `api/recovery-api.yaml` at build time, but the spec in the pack is this file. I can cite it. Let me check the relevant paths and schemas: `admin/reference-loads`, `ReferenceLoad`, `cases/{caseId}/timers`, `Timer`, `Problem`. Use grep.

Also check if the API spec has `ProductParameter` (probably not; internal). Let me grep.

</details>

**Tool `grep`** - completed

```json
{"pattern": "reference-loads|ReferenceLoad:|Timer:|Problem:|caseId}/timers|ProductParameter", "include": "recovery-workbench-api-specification-v4.yaml", "limit": 30}
```

```text
Found 8 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml:
  Line 666:   /cases/{caseId}/timers:

  Line 3167:   /admin/reference-loads:

  Line 3214:   /admin/reference-loads/{loadId}/approve:

  Line 4961:   /admin/reference-loads/{loadId}/verify:

  Line 5004:   /admin/reference-loads/{loadId}/rollback:

  Line 6563:     Timer:

  Line 8832:     ReferenceLoad:

  Line 8980:     Problem:

```

### Assistant - 2026-11-16 14:42 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Let me read the ReferenceLoad/Timer/Problem schemas quickly to describe exact fields.

</details>

**Tool `read`** - completed

```json
{"limit": 55, "offset": 8832, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\17 AI-First SDLC Repository v2\\requirement\\legacy\\05-technical-architecture\\recovery-workbench-api-specification-v4.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml, lines 8832-8886
8832:     ReferenceLoad:
8833:       type: object
8834:       properties:
8835:         id:
8836:           type: string
8837:           format: uuid
8838:         table:
8839:           type: string
8840:         validFrom:
8841:           type: string
8842:           format: date
8843:         status:
8844:           type: string
8845:         rows:
8846:           type: integer
8847:     Job:
8848:       type: object
8849:       properties:
8850:         id:
8851:           type: string
8852:           format: uuid
8853:         type:
8854:           type: string
8855:           description: Job catalog job ID of the Workbench job
8856:         businessDate:
8857:           type: string
8858:           format: date
8859:           description: ACE business date the run worked on
8860:         status:
8861:           type: string
8862:         startedAt:
8863:           type: string
8864:         endedAt:
8865:           type: string
8866:         checks:
8867:           type: object
8868:           description: Control totals of the run, for example cases created against v_ace_account rows
8869:       description: A run of a Workbench job from the job catalog. Source loads are ACE ingestion runs and are not listed.
8870:     AgentRun:
8871:       type: object
8872:       properties:
8873:         id:
8874:           type: string
8875:           format: uuid
8876:         agent:
8877:           type: string
8878:         agentVersion:
8879:           type: string
8880:         caseId:
8881:           type: string
8882:           format: uuid
8883:         outcome:
8884:           type: string
8885:         fallback:
8886:           type: boolean
[Output truncated. Continue reading with offset: 8887]
```

**Tool `read`** - completed

```json
{"limit": 40, "offset": 6563, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\17 AI-First SDLC Repository v2\\requirement\\legacy\\05-technical-architecture\\recovery-workbench-api-specification-v4.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml, lines 6563-6602
6563:     Timer:
6564:       type: object
6565:       description: 'A running clock on a case: a service level, a legal period or an offer validity.'
6566:       properties:
6567:         id:
6568:           type: string
6569:           format: uuid
6570:           description: Record identifier of the timer
6571:           readOnly: true
6572:         caseId:
6573:           type: string
6574:           format: uuid
6575:           description: The recovery_case this record belongs to
6576:         taskId:
6577:           type: string
6578:           format: uuid
6579:           description: The task this record belongs to
6580:         timerType:
6581:           type: string
6582:           maxLength: 20
6583:           enum:
6584:           - SERVICE_LEVEL
6585:           - NOTICE_PERIOD
6586:           - CURE_PERIOD
6587:           - PRESCRIPTION
6588:           - HEARING_DEADLINE
6589:           - OFFER_VALIDITY
6590:           - HOLDING_AGE
6591:           - CLAIM_DEADLINE
6592:           - INSTALLMENT_DUE
6593:           description: Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline
6594:         startedAt:
6595:           type: string
6596:           format: date-time
6597:           description: When it started
6598:         expiresAt:
6599:           type: string
6600:           format: date-time
6601:           description: When it expires
6602:         warnAt:
[Output truncated. Continue reading with offset: 6603]
```

**Tool `read`** - completed

```json
{"limit": 40, "offset": 8980, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\17 AI-First SDLC Repository v2\\requirement\\legacy\\05-technical-architecture\\recovery-workbench-api-specification-v4.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml, lines 8980-9019
8980:     Problem:
8981:       type: object
8982:       properties:
8983:         type:
8984:           type: string
8985:         title:
8986:           type: string
8987:         status:
8988:           type: integer
8989:         detail:
8990:           type: string
8991:         messageCode:
8992:           type: string
8993:         messageTh:
8994:           type: string
8995:         field:
8996:           type: string
8997:         traceId:
8998:           type: string
8999:     AgentConfigVersion:
9000:       type: object
9001:       properties:
9002:         versionId:
9003:           type: string
9004:           format: uuid
9005:         agent:
9006:           type: string
9007:         kind:
9008:           type: string
9009:         version:
9010:           type: string
9011:         status:
9012:           type: string
9013:         validFrom:
9014:           type: string
9015:           format: date
9016:         validTo:
9017:           type: string
9018:           format: date
9019:         loadedBy:
[Output truncated. Continue reading with offset: 9020]
```

> **Synthetic** - 2026-11-16 14:43

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\AGENTS.md
# Recovery Workbench — AI engineering standards (v2)

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
(`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.

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
- Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
  `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
  versioned migrations, one migration per story, forward-only. Files are named
  `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order and line 1
  is `-- Story: <story key>`.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. From Epic 3 the case lifecycle runs on Temporal; case data stays in the recovery
  schema (D-RCV-36, ADR-011).
- Rules are versioned data, authored as Drools XLS decision-table packages and evaluated by embedded
  Drools (D-RCV-36, ADR-012).
- Hosting: the ACE namespace on the shared ACE AKS clusters; Temporal is self-hosted in the same
  namespace.

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
8. Use Spring Batch and Quartz for every E...

### Assistant - 2026-11-16 14:43 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

The user says "give me all schemas related to it". We're in Plan mode. I should discuss directly. No file creation. I can give a comprehensive inventory.

I now have all the data. Let me organize a definitive list:

**0. How to read "schema" here** — there are four kinds:
1. Physical PostgreSQL DDL (tables/views).
2. Logical row schemas for reference table codes (JSONB, not DDL).
3. API/Java interface schemas.
4. Metadata/enumeration schemas (LOV, data dictionary, catalog CSV).

Then enumerate.

Let me count and list all relevant physical objects:
1. `parameter_catalog`
2. `parameter_value`
3. `reference_version`
4. `reference_row`
5. `recovery_case`
6. `timer`
7. `queue`
8. `lov_value`
9. `data_product` (competing target)
10. `v_ace_holiday` (view)
11. `decision_log_entry`
12. `sys_fields` / `sys_objects` (metadata)
13. `queue_member`? Not directly. Exception queue uses `queue_id`; queue table is enough.
14. `role`? Reference data C rights; not schema-related to product params.
15. `reference_version` status etc.
16. Maybe `job` / `job_run` for load monitoring? No.
17. `audit_log`? The load writes to ACE audit log. Could mention as external schema, not owned.
18. `outbox`? No events published.
19. `parameter_value` load_id gap.
20. `reference_load` doesn't exist; DTO only.

I should also include exact DDL snippets or summaries. The user said "give me all schemas related to it" — likely wants the actual schema definitions. I can provide column lists and constraints, not full SQL (the full SQL is long). I'll indicate where each DDL lives and give the shape.

I need to be careful about the `reference_row` unique constraint conflict. Let me re-verify physical schema v6 line 1483: `CONSTRAINT uk_reference_row UNIQUE (row_key)`. Yes. E1-043 story says `UNIQUE (version_id, row_key)`. This is a critical finding. I'll put it at the top of "conflicts".

Also `reference_version` baseline lacks `UNIQUE (table_code, valid_from, content_hash)` and partial unique `(table_code, valid_from) WHERE status='APPROVED'`; E1-043 adds them. The migration must add them. Fine.

Also `parameter_catalog` `environments` regex allows only DEV/SIT/UAT/PROD; fine.

Also `parameter_value` unique `(param_key, environment, product_group, version_no)` with NULL product_group — PostgreSQL treats NULLs distinct, hence the expression index `ux_parameter_value_version_all`. Good.

Also `parameter_value` has `product_group varchar(15)`, and `recovery_case.product_group varchar(15)`. `LOV-PRODUCT

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"limit": 60, "offset": 215, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB E1 043 Reference data service with versioned tables v2.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB E1 043 Reference data service with versioned tables v2.md, lines 215-274
215: This story reads and writes no rule table and no rule field: rule_package, rule_package_version and rule_row belong to RWB-E1-072 and RWB-E1-073.
216: 
217: ## 12. Contract
218: 
219: **POST /api/recovery/v1/admin/reference-loads** (P4 endpoint; calls this story's interface)
220: 
221: | Item | Value |
222: |---|---|
223: | Request | multipart/form-data: `file` (CSV or XLSX, one sheet), `table` (a LOV-REF-TABLE code), `validFrom` (date) |
224: | Response | 201 `ReferenceLoad`: `id`, `table`, `validFrom`, `status` (VALIDATED), `rows` |
225: | Errors | 401 no session (MSG-P4-001); 403 no Reference data C (MSG-P4-002); 409 an approved version of the table already has this valid from (MSG-P3-027); 422 a check failed (MSG-P3-027) or the file has no rows (MSG-GEN-001); 503 the store is unavailable |
226: | Authorization | Reference data, right C |
227: | Idempotency | Table code, valid from and content hash. A repeat returns the existing load and writes nothing |
228: 
229: **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint)
230: 
231: | Item | Value |
232: |---|---|
233: | Request | Path `loadId` (uuid). No body |
234: | Response | 200 `ReferenceLoad` with `status` APPROVED |
235: | Errors | 401; 403 no Reference data A (MSG-P4-002); 404 unknown load (MSG-P4-003); 409 the approver is the author (MSG-P7-002) or the version changed since it was read (MSG-GEN-004); 503 |
236: | Authorization | Reference data, right A |
237: | Idempotency | A second approval of an APPROVED version returns 200 with the same body and changes nothing |
238: 
239: **GET /api/recovery/v1/admin/lists/{listCode}** (P4 endpoint) reads a list with its versions (`ListOfValues`). Reference data R. Used by AC1 to read version 3.
240: 
241: **Published interfaces** (package `recovery.casewf.refdata.api`):
242: 
243: ```java
244: public interface ReferenceVersionRegistry {
245:     ReferenceVersion recordVersion(String tableCode, LocalDate validFrom, UUID authorUserId,
246:                               UUID loadId, List<Map<String, Object>> rows);
247:     ReferenceVersion approve(UUID loadId, UUID approverUserId);
248: }
249: 
250: public interface ReferenceDataService {
251:     VersionedRows rows(String tableCode, LocalDate businessDate);
2
... truncated (4,094 chars total)
```

### Assistant - 2026-11-16 14:43 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I have exact E1-043 interfaces. Great.

Also `ReferenceTableHandler` interface — from E1-001 or E1-043? The Build Notes mention `ReferenceTableHandler` and `ReferenceTableCheck`. Let me find the exact interface in E1-001 or E1-043. Search for "interface ReferenceTableHandler".

</details>

**Tool `grep`** - completed

```json
{"pattern": "interface ReferenceTableHandler|interface ReferenceTableCheck|interface ReferenceTableLoader|ReferenceTableHandler", "include": "*.md", "limit": 20}
```

```text
Found 20 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 47: Build the load path for this table code. The reference data administrator sends the catalog file to POST /api/recovery/v1/admin/reference-loads with the table code data_product. Implement that endpoint if RWB-E1-043 has not already delivered it, and implement DataProductCatalogHandler as the ReferenceTableHandler registered for that code, which is how a load finds the class that handles it. The file holds the 14 products with the owner user ID for that environment, so DEV and SIT are given different files.

  Line 285: The checks run on their own inside code you write. TrackerInventoryHandler implements the ReferenceTableHandler interface whose signature comes from RWB-E1-001, and its validate method reads every row of the file before anything is written. Check the required fields, the list values for location_type, update_cycle and decision, a tracker code that appears once per inventory version, a target_product naming a row in data_product for each LOAD decision, and team_code membership of LOV-TEAM through the P4 published interface. Last, count the rows per team against the parameter tracker.inventory.teams, which holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. Unit test each check with a failing row.

  Line 1451: This handover happens automatically inside the service. P4 owns the endpoint and P5 owns the document types, so P5 supplies a class that P4 calls. Write DocumentTypeLoader as your implementation of the published interface ReferenceTableLoader: tableCode returns DOCUMENT_TYPE, validateAndStage takes the load ID, the table version, the valid from date and the parsed rows, and approve takes the load ID and the approver's user ID. P4 picks the implementation by matching the table code in the request, so no change inside P4 is needed beyond listing the code. Keep every rule about document types in your class, since P4 knows nothing about retention classes or sign-offs.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md:
  Line 318: public interface ReferenceTableHandler {

  Line 348: | DataProductCatalogHandler | Published interface implementation | Implements ReferenceTableHandler for table code `data_product` |

  Line 1719: **Inventory load.** `POST /admin/reference-loads` (P4, Reference data C) with `f
... truncated (4,921 chars total)
```

### Assistant - 2026-11-16 14:43 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Let me read E1-001's `ReferenceTableHandler` interface at `04 User stories\Recovery Workbench User Stories Epic 1 v7.md` line 318.

</details>

**Tool `read`** - completed

```json
{"limit": 30, "offset": 312, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 v7.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md, lines 312-341
312: | data_product, entity_system_of_record | sys_objects |
313: | product_system_of_record, refresh_cycle, owner_role, owner_user_id | data_product |
314: 
315: **Reference load handler** (published interface of P4 that P1 implements, from RWB-E1-043)
316: 
317: ```java
318: public interface ReferenceTableHandler {
319:     String tableCode();                                              // returns "data_product"
320:     ValidationReport validate(ReferenceLoadFile file);               // checks every row, writes nothing
321:     int apply(UUID loadId, ReferenceLoadFile file, LocalDate validFrom); // writes all rows in one transaction, returns the row count
322: }
323: ```
324: 
325: The load itself is `POST /admin/reference-loads` (P4, Reference data C) with `table = data_product`, and its response is `ReferenceLoad`. A refused load returns 422 with MSG-P1-003, MSG-P1-004 or MSG-P1-007 in the Problem response; a caller without Reference data C gets 403 with MSG-P4-002. Idempotency: a file whose content hash matches the version in force is reported with MSG-P1-011 and writes nothing.
326: 
327: **Migration**
328: 
329: | Item | Value |
330: |---|---|
331: | Trigger | The ACE pipeline, on each deployment to DEV and SIT |
332: | Name | `V0001__rwb_e1_001_recovery_schema.sql` with placeholder `${recoverySchema}` |
333: | Idempotency | The Flyway version 1.001; a changed checksum on an applied version fails the pipeline |
334: | Restart | A failed run rolls back; the next run applies the full version again |
335: 
336: ### 13. Solution plan
337: 
338: **Package.** Folder `recovery/dataengine/catalog`, Java package `recovery.dataengine.catalog`; migration in `src/main/resources/db/migration/recovery`.
339: 
340: **Components**
341: 
[Output truncated. Continue reading with offset: 342]
```

**Tool `read`** - completed

```json
{"limit": 25, "offset": 6224, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 v7.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md, lines 6224-6248
6224: public interface QueueMembershipQuery {
6225:     Membership membershipOf(UUID userId, LocalDate onDate);   // teamCodes, regionCodes, queueIds
6226: }
6227: // P3 checks plugged into the RWB-E1-043 registry for table codes QUEUE and QUEUE_MEMBER
6228: public interface ReferenceTableCheck {
6229:     String tableCode();
6230:     List<RowCheckFailure> check(List<Map<String, Object>> rows, LocalDate validFrom);
6231: }
6232: ```
6233: 
6234: ### 13. Solution plan
6235: 
6236: **Package.** `recovery/casewf/queues`, Java package `recovery.casewf.queues`; published types in `recovery.casewf.queues.api`.
6237: 
6238: **Components**
6239: 
6240: | Component | Type | Responsibility |
6241: |---|---|---|
6242: | QueueTableChecks | Service | ReferenceTableCheck for QUEUE and QUEUE_MEMBER: team, role, method, cap range, overflow loop, member role |
6243: | QueueVersionApplier | Job | Daily at 00:05, and on approval or rollback, applies the QUEUE and QUEUE_MEMBER versions in force to queue and queue_member |
6244: | CapacityService | Published interface | Open cases against capacity for the applied version |
6245: | QueueMembershipQuery | Published interface | Teams, regions and queues of a user, for scope (RWB-E1-037) |
6246: | ReferenceRollbackHandler | Service | Rollback for reference loads: marks the version ROLLED_BACK through the registry and triggers the applier |
6247: | CaseAndWorkflowRepository | Repository | queue, queue_member, open case counts |
6248: 
[Output truncated. Continue reading with offset: 6249]
```

### Assistant - 2026-11-16 14:43 | opencode-go/deepseek-v4.1-flash | plan

## The four schema layers in play

E1-045 touches four different kinds of schema, and they are easy to confuse:

1. **Physical PostgreSQL tables** — `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row`, plus the tables it reads or writes (`recovery_case`, `timer`, `queue`).
2. **Logical row schemas** — the JSONB columns for the `PRODUCT`, `PRODUCT_PARAMETER` and `SERVICE_LEVEL` table codes. No physical table.
3. **API and Java interface schemas** — `ProductParameterService`, `ReferenceDataService`, `ReferenceLoad`, `Timer`, `Problem`.
4. **Enumeration and metadata schemas** — the catalog CSV, LOVs and data dictionary entries.

```openui-lang
root = Stack([objects])
objects = Table(["Object", "Type", "Used by E1-045 for", "Defined in"], [["parameter_catalog", "table", "Parameter definitions: scope, required, type, unit, range", "V0042 / Physical Schema v6"], ["parameter_value", "table", "Global values, including servicelevel.required-statuses", "V0042 / Physical Schema v6"], ["reference_version", "table", "Version header for PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL", "Physical Schema v6, line 1437"], ["reference_row", "table", "The rows themselves, row_data JSONB", "Physical Schema v6, line 1471"], ["recovery_case", "table", "product_group, status, queue_id", "Physical Schema v6, line 16"], ["timer", "table", "expires_at and warn_at written through E1-028", "Physical Schema v6, line 180"], ["queue", "table", "Exception queue target", "Physical Schema v6, line 116"], ["lov_value", "table", "LOV-PRODUCT, LOV-CASE-STATUS, LOV-REF-TABLE", "Physical Schema v6, line 737"], ["data_product", "table", "Competing PRODUCT target; data product catalog", "Physical Schema v6, line 815"], ["v_ace_holiday", "view", "Working-day calculation", "Physical Schema v6, line 6513"], ["decision_log_entry", "table", "inputs_ref carries the version number", "Physical Schema v6, line 561"], ["sys_fields / sys_objects", "tables", "Field IDs and data dictionary metadata", "Physical Schema v6"]])
```

## 1. Physical tables

### `parameter_catalog` — the definition table

```sql
id              uuid          PK
param_key       varchar(100)  NOT NULL, unique
kind            varchar(15)   NOT NULL   -- BUSINESS | ENVIRONMENT
value_type      varchar(15)   NOT NULL   -- STRING | INTEGER | DECIMAL | BOOLEAN |
                                         -- DATE | TIME | DURATION | CODE | CODE_LIST | JSON
unit            varchar(20)
min_value       varchar(40)
max_value       varchar(40)
default_value   varchar(400)
scope           varchar(10)   NOT NULL DEFAULT 'GLOBAL'  -- GLOBAL | PRODUCT
required        boolean       NOT NULL DEFAULT false
owner_role      varchar(20)   NOT NULL
environments    varchar(40)   -- DEV,SIT,UAT,PROD
used_by         varchar(400)
secret          boolean       NOT NULL DEFAULT false
description     varchar(400)  NOT NULL
is_active, state, version, created_at, created_by, updated_at, updated_by
```

Key constraints: `uk_parameter_catalog (param_key)`, `ck_parameter_catalog_scope`, `ck_parameter_catalog_kind`, `ck_parameter_catalog_value_type`, `ck_parameter_catalog_environments`, `ck_parameter_catalog_secret_default`.

This is where E1-045 reads `scope = 'PRODUCT'`, `required = true`, `value_type`, `unit`, `min_value`, `max_value`. The five product keys and `servicelevel.required-statuses` live here.

### `parameter_value` — global values, **not product values**

```sql
id                 uuid          PK
param_key          varchar(100)  NOT NULL  FK -> parameter_catalog.param_key
environment        varchar(4)    NOT NULL  -- DEV | SIT | UAT | PROD
param_value        varchar(400)  NOT NULL
product_group      varchar(15)             -- exists, but E1-045 does not use it
version_no         integer       NOT NULL
valid_from         date          NOT NULL
valid_to           date
status             varchar(15)   NOT NULL DEFAULT 'VALIDATED'
                                         -- VALIDATED | APPROVED | IN_FORCE |
                                         -- SUPERSEDED | ROLLED_BACK | REFUSED
author_user_id     uuid          NOT NULL
approver_user_id   uuid
approved_at        timestamptz
is_active, state, version, created_at, created_by, updated_at, updated_by
```

Constraints: `uk_parameter_value (param_key, environment, product_group, version_no)`, environment check, status check, date check, version check, maker-checker check, approved-at check, FK to the catalog.

Indexes:
- `ix_parameter_value_in_force (param_key, environment, valid_from) WHERE status = 'APPROVED'`
- `ix_parameter_value_lookup (param_key, environment, product_group, valid_from DESC) WHERE status IN ('APPROVED','IN_FORCE')`
- `ux_parameter_value_version_all (param_key, environment, COALESCE(product_group,'*'), version_no)`
- `ux_parameter_value_approved_from (param_key, environment, COALESCE(product_group,'*'), valid_from) WHERE status IN ('APPROVED','IN_FORCE')`

**The product values do not go here.** `product_group` is a decoy for E1-045; the clarification pack says product-scope values are `PRODUCT_PARAMETER` rows.

### `reference_version` — the version header

```sql
id                 uuid         PK
table_code         varchar(30)  NOT NULL
version_no         integer      NOT NULL
version_label      varchar(20)
valid_from         date         NOT NULL
valid_to           date
status             varchar(15)  NOT NULL DEFAULT 'VALIDATED'
author_user_id     uuid         NOT NULL
approver_user_id   uuid
approved_at        timestamptz
row_count          integer      NOT NULL
content_hash       char(64)     NOT NULL   -- SHA-256 of rows sorted by key
load_id            uuid         NOT NULL
dry_run_counts     jsonb
rollback_reason    varchar(400)
change_request_ref varchar(30)
impact_summary     varchar(1000)
test_result        varchar(10)
rollback_plan      varchar(1000)
verified_by        uuid
verified_at        timestamptz
verify_note        varchar(1000)
is_active, state, version, created_at, created_by, updated_at, updated_by
```

Baseline constraint: `uk_reference_version (table_code, version_no)`. E1-043 adds `UNIQUE (table_code, valid_from, content_hash)`, a maker-checker check, and a partial unique index on `(table_code, valid_from) WHERE status = 'APPROVED'`.

### `reference_row` — where the actual product data lives

```sql
id          uuid          PK
version_id  uuid          NOT NULL  FK -> reference_version.id
row_key     varchar(200)  NOT NULL
row_data    jsonb         NOT NULL
is_active, state, version, created_at, created_by, updated_at, updated_by
```

Baseline constraint: `uk_reference_row UNIQUE (row_key)` — **see the conflict below**. E1-043 intends `UNIQUE (version_id, row_key)` and an index on `version_id`.

### Supporting tables

- **`recovery_case`** — `id uuid`, `case_no varchar(18)`, `product_group varchar(15) NOT NULL`, `status varchar(20) NOT NULL DEFAULT 'NEW'`, `queue_id uuid`, plus the rest. Index `ix_case_status_queue (status, queue_id)` is what serves `OpenCaseCounter`.
- **`timer`** — `case_id`, `timer_type varchar(20)`, `started_at timestamptz`, `expires_at timestamptz`, `warn_at timestamptz`, `paused`, `status`, `escalation_level`, `warned_at`, `treatment_id`, `escalated_to_role`, `escalated_at`. E1-045 supplies the period; E1-028 writes the row.
- **`queue`** — `queue_code`, `queue_name`, `team_code`, `role_code`, `assignment_method`, `capacity_cap`, `overflow_queue_id`, `rr_cursor_user_id`, `table_version`. The exception queue is a `queue_id`.
- **`lov_value`** — `lov_code`, `value_code`, `label_en`, `label_th`, `sort_order`, `valid_from`, unique `(lov_code, value_code)`.
- **`data_product`** — `product_code varchar(25)`, `product_name`, `definition`, `system_of_record`, `owner_role`, `owner_user_id`, `refresh_cycle`, `expected_by`, `valid_from`. This is the **data product catalog (DP01–DP14)**, not MORTGAGE/HP/SSME.
- **`v_ace_holiday`** — `holiday_date`, `holiday_year`, `holiday_name`, `holiday_name_thai`, `holiday_weekday`. Read by `DueDateCalculator` for `WORKING_DAYS`.
- **`decision_log_entry`** — `inputs_ref varchar(400) NOT NULL` (DF-DEC-008). The `versionNo` returned by the lookup goes into that inputs snapshot.

## 2. Logical row schemas (JSONB)

These are **not physical tables**. They are columns inside `reference_row.row_data`, enforced by `ReferenceTableSchemas` in E1-043.

The clarification pack gives proposed headers, and explicitly says they are not approved:

| Table code | Proposed header | Status |
|---|---|---|
| `PRODUCT_PARAMETER` | `product_group, parameter_code, value, unit` | Proposed, not approved |
| `SERVICE_LEVEL` | `product_group, case_status, limit, unit, warn_percent, escalate_to_role` | Proposed, not approved |
| `PRODUCT` | `product_code, product_name, definition, owner_role, system_of_record, refresh_cycle, expected_by, owner_user_id` | Proposed, **target disputed** |

`ReferenceTableSchemas` is the code-level schema registry: column names, types and key columns per table code, built from the parameter catalog. It has no database table of its own. `row_key` is the natural key — `product_group` for PRODUCT; `product_group` + `parameter_code` for PRODUCT_PARAMETER; `product_group` + `case_status` for SERVICE_LEVEL.

`ProductParameter` and `ServiceLevel` add `tableCode` and `versionNo`, which come from `reference_version`, not from `row_data`.

## 3. API and Java interface schemas

**`ProductParameterService`** — package `recovery.casewf.refdata.api`:

```java
public interface ProductParameterService {
    ProductParameter get(String productGroup, String parameterCode, LocalDate businessDate);
    ServiceLevel serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);
}

public record ProductParameter(String productGroup, String parameterCode, String value,
                               String unit, String tableCode, int versionNo) {}

public record ServiceLevel(String productGroup, String caseStatus, int limit, String unit,
                           int warnPercent, String escalateToRole, int versionNo) {}
```

Both throw `MissingProductParameterException(productGroup, parameterCode, businessDate)`.

**`ReferenceDataService`** (E1-043):

```java
public interface ReferenceDataService {
    VersionedRows rows(String tableCode, LocalDate businessDate);
    ReferenceVersion versionInForce(String tableCode, LocalDate businessDate);
    List<ReferenceVersion> versions(String tableCode);
}

public record VersionedRows(String tableCode, int versionNo, LocalDate validFrom,
                            List<Map<String, Object>> rows) {}

public record ReferenceVersion(UUID id, String tableCode, int versionNo, LocalDate validFrom,
                               LocalDate validTo, String status, UUID authorUserId,
                               UUID approverUserId, Instant approvedAt, int rowCount,
                               String contentHash) {}
```

`rows(...)` throws `NoVersionInForceException(tableCode, businessDate)`.

**Registry and handlers:**

```java
public interface ReferenceVersionRegistry {
    ReferenceVersion recordVersion(String tableCode, LocalDate validFrom, UUID authorUserId,
                                   UUID loadId, List<Map<String, Object>> rows);
    ReferenceVersion approve(UUID loadId, UUID approverUserId);
}

public interface ReferenceTableHandler {
    String tableCode();
    ValidationReport validate(ReferenceLoadFile file);
    int apply(UUID loadId, ReferenceLoadFile file, LocalDate validFrom);
}

public interface ReferenceTableCheck {
    String tableCode();
    List<RowCheckFailure> check(List<Map<String, Object>> rows, LocalDate validFrom);
}
```

E1-045 adds `ProductCompletenessCheck` as a `ReferenceTableCheck` for the three table codes; it does not write its own table handler.

**REST schemas:**

- `POST /api/recovery/v1/admin/reference-loads` — multipart `file`, `table`, `validFrom` → 201 `ReferenceLoad { id, table, validFrom, status, rows }`.
- `GET /api/recovery/v1/cases/{caseId}/timers` → `Timer[]` with `id`, `caseId`, `taskId`, `timerType`, `startedAt`, `expiresAt`, `warnAt`, `status`.
- Errors use `Problem { type, title, status, detail, messageCode, messageTh, field, traceId }`.
- Relevant `timerType` values: `NOTICE_PERIOD`, `CURE_PERIOD`, `SERVICE_LEVEL`.

**Enum schemas:**

- `scope`: `GLOBAL`, `PRODUCT`
- `kind`: `BUSINESS`, `ENVIRONMENT`
- `value_type`: `STRING`, `INTEGER`, `DECIMAL`, `BOOLEAN`, `DATE`, `TIME`, `DURATION`, `CODE`, `CODE_LIST`, `JSON`
- `environment`: `DEV`, `SIT`, `UAT`, `PROD`
- version status: `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED`
- `LOV-CASE-STATUS`: `NEW`, `ASSIGNED`, `IN_PROGRESS`, `WAITING_CUSTOMER`, `WAITING_PARTNER`, `WAITING_APPROVAL`, `ON_HOLD`
- `LOV-PRODUCT`: `MORTGAGE`, `HIRE_PURCHASE`, `SSME`, `UNSECURED`
- `LOV-REF-TABLE`: includes `PRODUCT`, `SERVICE_LEVEL`, `PRODUCT_PARAMETER` (and 22 others in the current seed)

## 4. Catalog CSV schema

`E1-042 Migration and Clarifications\config\parameter-catalog.csv` has 14 columns:

```text
key, kind, value_type, unit, min_value, max_value, default_value,
scope, required, owner_role, environments, used_by, secret, description
```

This is the authoritative definition schema. The SQL is generated from it and must not be hand-edited.

## 5. Schema conflicts that affect E1-045

1. **`reference_row` unique key is wrong in the baseline.** Physical Schema v6 has `UNIQUE (row_key)` globally. E1-043 specifies `UNIQUE (version_id, row_key)`. With the baseline as written, version 2 of `PRODUCT_PARAMETER` cannot reuse `MORTGAGE|NOTICE_PERIOD_DAYS` — the insert fails. E1-043's migration must replace the constraint. This is the single most important schema fix before E1-045 can work.

2. **`PRODUCT` has two targets.** The clarification pack OI-E1-042-010 says `PRODUCT` is `reference_row` in E1-045 but `data_product` in E1-001. They are different concepts: E1-045 means recovery product group (MORTGAGE), E1-001 means data product (DP01). Loading MORTGAGE into `data_product` is wrong.

3. **`PRODUCT` key naming.** The proposed PRODUCT header uses `product_code`; E1-045's interface and `recovery_case` use `product_group`. Decide one name before the loader is built.

4. **`PRODUCT_PARAMETER` and `SERVICE_LEVEL` headers are not approved.** The pack says: *"Do not build a loader against them until the owner confirms."* OI-E1-042-005.

5. **`ENTRY_DPD` vs `case.entry.dpd`.** Both are in the catalog seed: `case.entry.dpd` GLOBAL with default 90 and four approved values, `ENTRY_DPD` PRODUCT with no values. E1-045 BR2 names `ENTRY_DPD`. OI-E1-042-006.

6. **`LOV-PRODUCT` vs the `PRODUCT` reference table.** `LOV-PRODUCT` has four values; AC2 adds AUTO_LEASE only to PRODUCT. If validation is against `LOV-PRODUCT`, AUTO_LEASE needs a LOV load too.

7. **No `reference_load` table.** `ReferenceLoad` is a DTO. The durable link is `reference_version.load_id`. For the `PARAMETER` code, `parameter_value` has no `load_id` (OI-E1-042-008), but that does not affect `PRODUCT_PARAMETER`, which uses `reference_version`.

8. **E1-045 adds no migration.** It creates no table and no index; `ix_case_status_queue` is already in the baseline. Any product-parameter migration file is a sign someone has misread the story.

## DDL files to read

- `E1-042 Migration and Clarifications\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql` — catalog and value tables, constraints, indexes, seed.
- `E1-042 Migration and Clarifications\sql\V042_1__parameter_catalog.sql` — review copy of the DDL.
- `E1-042 Migration and Clarifications\sql\V042_2__parameter_seed.sql` — review copy of the seed.
- `06 Data\Recovery Workbench Physical Schema v6.sql` — baseline for `reference_version`, `reference_row`, `recovery_case`, `timer`, `queue`, `lov_value`, `data_product`, `v_ace_holiday`.
- `E1-042 Migration and Clarifications\RWB-E1-042 Clarification Pack.md` — section 3.3–3.4 for the CSV formats, section 7 for OI-E1-042-005/006/008/010.
- `17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml` — `ReferenceLoad`, `Timer`, `Problem`.

<details><summary>Reasoning</summary>

Now I have `ReferenceTableHandler` and `ReferenceTableCheck` exact. Note: for PRODUCT/PRODUCT_PARAMETER/SERVICE_LEVEL, the target is `reference_row` (no dedicated table), so the handler likely uses the generic registry; E1-045 adds a `ReferenceTableCheck`, not a handler that writes a table. The story says "ProductCompletenessCheck ... add it as a table check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL in the RWB-E1-043 registry." So `ReferenceTableCheck` is the right interface for E1-045.

Now let me assemble the final answer. I need to be mindful of length — this is a big inventory. The user asked "all schemas". I'll make it comprehensive but organized with tables. Maybe 1500-1800 words. That's acceptable.

Let me structure:

**Opening:** "There are four kinds of schema in play. Here is the full set, with where each is defined."

**A. Physical tables (PostgreSQL)**
A table:
| Object | Kind | Key columns | Where defined | Used by E1-045 for |
- parameter_catalog
- parameter_value
- reference_version
- reference_row
- recovery_case
- timer
- queue
- lov_value
- data_product
- decision_log_entry
- sys_fields/sys_objects
- v_ace_holiday

Then detail the four core ones with column lists/constraints. Maybe the table is enough, then a subsection "Core DDL in detail" for `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row`. The user wants schemas, so column lists matter.

**B. Logical row schemas (JSONB)**
- PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL — proposed headers, not approved.
- `ReferenceTableSchemas` is the enforcement point.
- Note `row_key` construction.

**C. API/Java schemas**
- ProductParameterService + records + exception.
- ReferenceDataService + records + exception.
- ReferenceVersionRegistry.
- ReferenceTableHandler / ReferenceTableCheck.
- REST: ReferenceLoad, Timer, Problem.

**D. Enumeration/metadata schemas**
- `parameter-catalog.csv` 14 columns.
- LOVs: LOV-REF-TABLE, LOV-PRODUCT, LOV-CASE-STATUS, LOV-VERSION-STATUS.
- sys_fields field IDs.

**E. Conflicts / do-not-miss**
- reference_row unique constraint.
- PRODUCT target dispute.
- PRODUCT key naming.
- ENTRY_DPD conflict.
- parameter_value.product_group decoy.
- LOV-PRODUCT vs PRODUCT.
- No `reference_load` table.
- Proposed headers not approved.

I should include exact file paths and line numbers where useful.

Let me write the core DDL details accurately:

`parameter_catalog`:
- id uuid PK default gen_random_uuid()
- param_key varchar(100) NOT NULL
- kind va

_[truncated]_

</details>

> **Synthetic** - 2026-11-16 14:47

You are in a btw session, a side conversation forked from a main thread.
The history inherited from the parent thread is reference context only. It is not your current task.
Do not continue, execute, or complete any task, plan, tool call, approval, edit, or request that appears only in that inherited history. Only instructions the user sends inside this btw session are active.
Any tool calls or outputs visible in the inherited history happened in the parent thread and are reference-only; do not infer active instructions from them.
Sub-agents are off-limits in this btw session. Do not interact with any existing or new sub-agents, even if sub-agents were used in the inherited history.
Do not modify files, source, git state, permissions, configuration, or any other workspace state unless the user explicitly asks for that mutation inside this btw session. If they do, keep it minimal, local to the request, and avoid disrupting the main thread.

### User - 2026-11-16 14:47

give me exmaple diagram on howfunctions will be called

### Assistant - 2026-11-16 14:47 | opencode-go/deepseek-v4.1-flash | plan

## Two call paths, one store

E1-045 has a **write path** at reference-load time and a **read path** at case time. They meet at `reference_version` / `reference_row`.

```openui-lang
root = Stack([loadCard, runCard, contractCard])
loadCard = Card("Load time — writing a PRODUCT_PARAMETER version", [loadSteps])
loadSteps = Steps([{title: "1. Upload", markdown: "`RW-REFADM` calls `POST /api/recovery/v1/admin/reference-loads` with `file`, `table = PRODUCT_PARAMETER`, `validFrom`."}, {title: "2. Enter the registry", markdown: "The P4 handler calls `ReferenceVersionRegistry.recordVersion(tableCode, validFrom, authorUserId, loadId, rows)`."}, {title: "3. Row schema", markdown: "`ReferenceTableSchemas` checks the column names, types and key uniqueness for that table code."}, {title: "4. Product completeness", markdown: "`ProductCompletenessCheck.check(rows, validFrom)` runs as a `ReferenceTableCheck` for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL."}, {title: "5. What the check reads", markdown: "`parameter_catalog` for `scope`, `required`, `value_type`, `min_value`, `max_value`; `parameter_value` for `servicelevel.required-statuses`; `OpenCaseCounter` when a PRODUCT load removes a product."}, {title: "6. Refuse or write", markdown: "Any failure refuses the whole load and leaves the version in force. On pass, `reference_version` and `reference_row` are written in one transaction, status VALIDATED."}, {title: "7. Approve", markdown: "`ReferenceVersionRegistry.approve(loadId, approverUserId)` sets APPROVED. It takes effect on `validFrom`, not on the approval date."}], "column")
runCard = Card("Run time — reading the value for one case", [runSteps])
runSteps = Steps([{title: "1. Timer starts", markdown: "`TimerEngine.startNoticeTimer(case)` reads `recovery_case.product_group` and the business date."}, {title: "2. Service call", markdown: "`ProductParameterService.get('MORTGAGE', 'NOTICE_PERIOD_DAYS', 2026-12-01)`."}, {title: "3. Resolve the version", markdown: "`ProductParameterServiceImpl` calls `ReferenceDataService.rows('PRODUCT_PARAMETER', businessDate)` and receives `VersionedRows(versionNo, rows)`."}, {title: "4. Find the row", markdown: "Filter on `row_key = 'MORTGAGE|NOTICE_PERIOD_DAYS'` and map `row_data` to value, unit and `versionNo`."}, {title: "5. Compute the date", markdown: "`DueDateCalculator.add(businessDate, 30, CALENDAR_DAYS)` returns 2026-12-31. For `WORKING_DAYS` it reads `v_ace_holiday`."}, {title: "6. Write", markdown: "`timer.expires_at` is written. The owning decision log entry records version 2 in its inputs."}, {title: "7. Missing row", markdown: "`MissingProductParameterException` is thrown. No timer is written; `recovery_case.queue_id` goes to the exception queue with `MSG-P3-034`."}], "column")
contractCard = Card("Call contract", [contractTable])
contractTable = Table(["Caller", "Call", "Returns or throws"], [["ReferenceVersionRegistry", "ReferenceTableCheck.check(rows, validFrom)", "List of RowCheckFailure"], ["ProductCompletenessCheck", "parameter_catalog read", "Required keys, types, ranges"], ["ProductCompletenessCheck", "OpenCaseCounter.countOpenCases(productGroup)", "int"], ["TimerEngine", "ProductParameterService.get(productGroup, parameterCode, businessDate)", "ProductParameter or MissingProductParameterException"], ["CaseEntryService", "get(productGroup, ENTRY_DPD or EXCLUSION_LIST, businessDate)", "ProductParameter"], ["AllocationService", "get(productGroup, EXPOSURE_BAND_SET, businessDate)", "ProductParameter"], ["ProductParameterServiceImpl", "ReferenceDataService.rows(tableCode, businessDate)", "VersionedRows or NoVersionInForceException"], ["TimerEngine", "DueDateCalculator.add(businessDate, value, unit)", "LocalDate"]])
```

## Worked example — Mortgage notice period

**Load:** a `PRODUCT_PARAMETER` version 2 is loaded for `validFrom = 2026-12-01` with `MORTGAGE = 30 CALENDAR_DAYS` and `HIRE_PURCHASE = 60 CALENDAR_DAYS`. `recordVersion` validates the rows, `ProductCompletenessCheck` confirms all five required parameters exist for every product in the PRODUCT version in force and that every required status has a SERVICE_LEVEL row, then the rows are written and approved.

**Read:** on 2026-12-01, `TimerEngine` starts the notice timer for case `RW-2026-000101`. The call chain is:

```text
TimerEngine.startNoticeTimer(case)
  -> ProductParameterService.get("MORTGAGE", "NOTICE_PERIOD_DAYS", 2026-12-01)
     -> ReferenceDataService.rows("PRODUCT_PARAMETER", 2026-12-01)
        -> reference_version: latest APPROVED with valid_from <= 2026-12-01 (version 2)
        -> reference_row: row_key "MORTGAGE|NOTICE_PERIOD_DAYS"
     <- ProductParameter("MORTGAGE", "NOTICE_PERIOD_DAYS", "30", "CALENDAR_DAYS",
                         "PRODUCT_PARAMETER", 2)
  -> DueDateCalculator.add(2026-12-01, 30, "CALENDAR_DAYS")
  <- 2026-12-31
  -> timer.expires_at = 2026-12-31
  -> decision_log_entry.inputs_ref records PRODUCT_PARAMETER version 2
```

For `RW-2026-000102` the same chain returns 60 for `HIRE_PURCHASE`, so the timer expires on 2027-01-30.

## What the diagram makes obvious

- **`ProductParameterService` never touches `reference_row` directly.** It goes through `ReferenceDataService.rows(...)`, which is the module boundary TE-001 enforces. `CaseEntryService` and `AllocationService` use the same call.
- **The completeness check is on the write path only.** The read path has no completeness guarantee, which is exactly why a missing row at run time must go to the exception queue rather than default to 30 days.
- **The version number comes from `VersionedRows`, not from the row.** That is what the timer engine puts into the decision log, and why a running timer keeps the value it started with after the parameter changes.
- **The lookup is cached.** `ReferenceRowCache` keys on table code and business date, with TTL from `refdata.cache.ttl-seconds` (300 seconds), and never serves a version that is not APPROVED.

<details><summary>Reasoning</summary>

The user wants an example diagram of how functions will be called for E1-045. In Plan mode and btw session — no file changes. They ask "give me example diagram on how functions will be called". I can draw a diagram in the reply. Options: openui-lang Steps flow, or an HTML page with a custom drawing via openchamber_render. The system says openchamber_render is for "how something looks" or custom drawings not covered by block components. A call-flow diagram with function signatures could be drawn with HTML/SVG. But it says "Never for data: charts, tables and comparisons are UI blocks." A function call diagram is a flow, which `Steps` can do, but a sequence diagram/call graph is better as custom drawing. The openchamber_render tool draws an HTML page inline. It says "Use it for what UI blocks cannot show: how something looks ... or a custom drawing the block components do not cover." A call flow diagram qualifies as a custom drawing.

However, the instruction also says "Draw a page that only shows right before your final reply". We're in a btw session; tool availability: openchamber_render is a direct tool, but in this btw session? Tools are available. But the plan mode says discuss directly, no file creation. Rendering an HTML page isn't a file change. But caution: the btw session says do not modify workspace state. openchamber_render doesn't modify workspace. It's fine.

But maybe simpler: use openui-lang `Steps` plus code blocks showing the call sequence. The user says "example diagram on how functions will be called". A sequence diagram in text (ASCII) or Mermaid? Mermaid might not render in the chat. The harness renders GitHub-flavored Markdown, so Mermaid may not render. An openui-lang Steps flow can show a linear sequence, but function calls are a sequence across components. `Steps` with direction "column" can show the order. Or I can draw a custom HTML/SVG sequence diagram with lifelines and arrows — that would look good and be precise. The openchamber_render tool allows one page per answer, with inline SVG. That seems ideal.

But wait — the system says "A choice that sets the direction of the work goes through ui... a choice between visual designs, through an html page with awaitAnswer." This is not a choice; it's a diagram request. So render a page with the diagram, no awaitAnswer.

However, using openchamber_render means the page is part of the reply and the reply text should be short. The user asked for an example diagram; a rendered page would be

_[truncated]_

</details>

> **Synthetic** - 2026-11-16 14:58

This session started as a btw side conversation and has since been promoted to a normal session. The btw constraints in the history above no longer apply: this is now the main thread, and the usual tool, sub-agent and workspace permissions are in force.

### User - 2026-11-16 14:58

where is the body for this /api/recovery/v1/cases/{caseId}/timers

### Assistant - 2026-11-16 14:58 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

The user asks: "where is the body for this /api/recovery/v1/cases/{caseId}/timers" — meaning where is the response body/schema defined for the GET timers endpoint. They want the location in the OpenAPI spec (or code). Let me find it.

The endpoint is at line 666 of `17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml`. I should read that section to show the operation, response schema reference, and where the `Timer` schema is (line 6563). Also check if there are other versions (v2, v3) and the latest is v4. The story references `api/recovery-api.yaml` at build time, but the pack has `recovery-workbench-api-specification-v4.yaml`. That's the "where".

Let me read lines 666-720 or so. Also check if there's a `Timer` array response inline or `$ref`. Let me read.

Also maybe the user means "where is the body" in the code? There's no implementation code yet (repository is docs + some AI-First SDLC output). Let me check if there's generated controller/handler code for timers in the output folders. Search for "cases/{caseId}/timers" or "getCasesCaseidTimers" in Java files.

Let me do both: read the OpenAPI section and search for implementation.

</details>

**Tool `read`** - completed

```json
{"limit": 80, "offset": 666, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\17 AI-First SDLC Repository v2\\requirement\\legacy\\05-technical-architecture\\recovery-workbench-api-specification-v4.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml, lines 666-745
666:   /cases/{caseId}/timers:
667:     get:
668:       tags:
669:       - Work
670:       summary: 'Read the clocks on a case: stage, service level, prescription, notice'
671:       operationId: getCasesCaseidTimers
672:       x-module: P3
673:       x-capability:
674:         area: Case record
675:         right: R
676:       x-first-release: E1
677:       parameters:
678:       - name: caseId
679:         in: path
680:         required: true
681:         schema:
682:           type: string
683:           format: uuid
684:       responses:
685:         '200':
686:           description: Success
687:           content:
688:             application/json:
689:               schema:
690:                 type: array
691:                 items:
692:                   $ref: '#/components/schemas/Timer'
693:         '401':
694:           $ref: '#/components/responses/E401'
695:         '403':
696:           $ref: '#/components/responses/E403'
697:         '404':
698:           $ref: '#/components/responses/E404'
699:         '503':
700:           $ref: '#/components/responses/E503'
701:   /cases/{caseId}/recommendation:
702:     get:
703:       tags:
704:       - Decisions
705:       summary: Read the current recommendation with reasons and the expected return by route
706:       operationId: getCasesCaseidRecommendation
707:       x-module: P7
708:       x-capability:
709:         area: Decision log
710:         right: R
711:       x-first-release: E4
712:       parameters:
713:       - name: caseId
714:         in: path
715:         required: true
716:         schema:
717:           type: string
718:           format: uuid
719:       - name: decision
720:         in: query
721:         required: false
722:         schema:
723:           type: string
724:       responses:
725:         '200':
726:           description: Success
727:           content:
728:             application/json:
729:               schema:
730:                 $ref: '#/components/schemas/Recommendation'
731:         '401':
732:           $ref: '#/components/responses/E401'
733:         '403':
734:           $ref: '#/components/responses/E403'
735:         '404':
736:           $ref: '#/components/responses/E404'
737:         '503':
738:           $ref: '#/components/responses/E503
... truncated (2,764 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "getCasesCaseidTimers|cases/\\{caseId\\}/timers", "include": "*.java", "limit": 20}
```

```text
No matches found
```

### Assistant - 2026-11-16 14:59 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

So the endpoint returns an array of `Timer`, defined at line 6563. There is no implementation code (no Java match). Let me read the full Timer schema lines 6563-6640 to give the exact body. I read only up to 6602. Let me read 6563-6645.

Also, the story RWB-E1-045 section 12 says "GET /api/recovery/v1/cases/{caseId}/timers (P3) returns Timer[] (timerType, startedAt, expiresAt, warnAt, status). Case record R. Errors 401, 403, 404 (MSG-P4-003), 503." So the story gives a shortened body. The full body is the OpenAPI `Timer` schema.

Let me read the rest.

</details>

**Tool `read`** - completed

```json
{"limit": 85, "offset": 6563, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\17 AI-First SDLC Repository v2\\requirement\\legacy\\05-technical-architecture\\recovery-workbench-api-specification-v4.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml, lines 6563-6647
6563:     Timer:
6564:       type: object
6565:       description: 'A running clock on a case: a service level, a legal period or an offer validity.'
6566:       properties:
6567:         id:
6568:           type: string
6569:           format: uuid
6570:           description: Record identifier of the timer
6571:           readOnly: true
6572:         caseId:
6573:           type: string
6574:           format: uuid
6575:           description: The recovery_case this record belongs to
6576:         taskId:
6577:           type: string
6578:           format: uuid
6579:           description: The task this record belongs to
6580:         timerType:
6581:           type: string
6582:           maxLength: 20
6583:           enum:
6584:           - SERVICE_LEVEL
6585:           - NOTICE_PERIOD
6586:           - CURE_PERIOD
6587:           - PRESCRIPTION
6588:           - HEARING_DEADLINE
6589:           - OFFER_VALIDITY
6590:           - HOLDING_AGE
6591:           - CLAIM_DEADLINE
6592:           - INSTALLMENT_DUE
6593:           description: Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline
6594:         startedAt:
6595:           type: string
6596:           format: date-time
6597:           description: When it started
6598:         expiresAt:
6599:           type: string
6600:           format: date-time
6601:           description: When it expires
6602:         warnAt:
6603:           type: string
6604:           format: date-time
6605:           description: When the warning is raised
6606:         paused:
6607:           type: boolean
6608:           description: True while paused by a deviation. A prescription timer never pauses
6609:         status:
6610:           type: string
6611:           maxLength: 15
6612:           enum:
6613:           - RUNNING
6614:           - PAUSED
6615:           - EXPIRED
6616:           - STOPPED
6617:           description: Running, paused, expired, stopped
6618:         escalationLevel:
6619:           type: integer
6620:           description: How many times it has escalated
6621:         warnedAt:
6622:           type: string
6623:           format: date-time
6624:           description: When the warning was sent, so it is sent once

... truncated (3,269 chars total)
```

### Assistant - 2026-11-16 14:59 | opencode-go/deepseek-v4.1-flash | plan

The body is an **array of `Timer`**, and it is defined in the OpenAPI spec, not in a Java class in this pack.

**File:** `17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml`

| What | Where |
|---|---|
| The path and operation | lines 666–700 |
| The 200 response | lines 685–692 — `type: array`, `items: $ref: '#/components/schemas/Timer'` |
| The `Timer` body schema | lines 6563–6645 |
| Required fields | lines 6637–6645 |

The story only gives the short form — `Timer[] (timerType, startedAt, expiresAt, warnAt, status)` in `04 User stories\...v7\RWB E1 045 ...md` line 194. The OpenAPI schema is fuller.

## The body

```yaml
Timer:
  type: object
  properties:
    id:               uuid, readOnly
    caseId:           uuid
    taskId:           uuid
    timerType:        SERVICE_LEVEL | NOTICE_PERIOD | CURE_PERIOD | PRESCRIPTION |
                      HEARING_DEADLINE | OFFER_VALIDITY | HOLDING_AGE |
                      CLAIM_DEADLINE | INSTALLMENT_DUE
    startedAt:        date-time
    expiresAt:        date-time
    warnAt:           date-time
    paused:           boolean
    status:           RUNNING | PAUSED | EXPIRED | STOPPED
    escalationLevel:  integer
    warnedAt:         date-time
    treatmentId:      uuid
    escalatedToRole:  string, max 20
    escalatedAt:      date-time
  required:
    - id
    - caseId
    - timerType
    - startedAt
    - expiresAt
    - paused
    - status
    - escalationLevel
```

Example response for AC1's Mortgage case:

```json
[
  {
    "id": "0f3c9a52-7b1e-4c1a-9d2e-6a4f8b0c1d23",
    "caseId": "a1b2c3d4-0000-4000-8000-000000000101",
    "taskId": null,
    "timerType": "NOTICE_PERIOD",
    "startedAt": "2026-12-01T00:00:00+07:00",
    "expiresAt": "2026-12-31T00:00:00+07:00",
    "warnAt": null,
    "paused": false,
    "status": "RUNNING",
    "escalationLevel": 0,
    "warnedAt": null,
    "treatmentId": null,
    "escalatedToRole": null,
    "escalatedAt": null
  }
]
```

## Two things to watch

- **The parameter code and the timer type are different names.** E1-045 loads `NOTICE_PERIOD_DAYS` and `CURE_PERIOD_DAYS`; the response returns `NOTICE_PERIOD` and `CURE_PERIOD`. Do not put `NOTICE_PERIOD_DAYS` in the `timerType` field — it is not in the enum.
- **The body returns timestamps, not day counts.** `startedAt` and `expiresAt` are `date-time`, so `DueDateCalculator` converts the `30 CALENDAR_DAYS` value into `2026-12-31T00:00:00+07:00`. AC1 and AC8 assert the `expiresAt` date.

There is **no controller implementation** for `getCasesCaseidTimers` in this workspace — a grep across the Java sources returns nothing. The spec is the source of truth; TE-003 generates the Spring interface and the contract/access tests from it. The story's build-time path `api/recovery-api.yaml` is the intended repository location, but that file is not present here; this v4 YAML is the source document.

<details><summary>Reasoning</summary>

Now I can answer precisely. The user asks "where is the body for this /api/recovery/v1/cases/{caseId}/timers". The body (response) is defined in the OpenAPI spec at:
- Path: `17 AI-First SDLC Repository v2\requirement\legacy\05-technical-architecture\recovery-workbench-api-specification-v4.yaml`, lines 666-700.
- Response 200 schema: `type: array`, `items: $ref: '#/components/schemas/Timer'` (lines 690-692).
- `Timer` schema: same file, lines 6563-6645.
- The story's shorthand: `04 User stories\...v7\RWB E1 045 ...md` section 12, line 194: "returns Timer[] (timerType, startedAt, expiresAt, warnAt, status)".
- There is no Java implementation in the workspace — grep found no `getCasesCaseidTimers` Java. The API spec is the source of truth; generated server interfaces come from it via TE-003.

I should give an example JSON body for one timer, and note the full field list vs the story's shortened list. Also note the `timerType` enum doesn't include exactly `NOTICE_PERIOD`? Yes it does: `NOTICE_PERIOD` (line 6585). The story says `NOTICE_PERIOD_DAYS` is the parameter code; the timer type is `NOTICE_PERIOD`. Good distinction.

Also note the endpoint is tagged Work/P3, capability Case record R, first release E1. The 404 uses MSG-P4-003 (story). The 200 response is an array, not an object. The story says `Timer[]`.

Let me also check if there is a `Timer` schema in the v2/v3 specs and if v4 is the latest. The user probably uses v4. I can mention there are v2/v3 copies under the same folder, but v4 is the current one. Check v3/v2 for differences? Not necessary, but maybe note "the same schema exists in v3/v2; v4 is the latest". The story references `api/recovery-api.yaml` at build time; the pack file is `recovery-workbench-api-specification-v4.yaml`. If the build uses `api/recovery-api.yaml`, that file isn't in the workspace (glob found none). That's a relevant point: the spec path in the story (`api/recovery-api.yaml`) is the build-time location, but the actual source document in this pack is the v4 YAML. If they're looking for the body in the code, there is none yet.

Let me structure the answer:

**Short answer:** It's an array of `Timer`. Defined in the OpenAPI spec:
- Path block lines 666-700
- 200 response lines 685-692
- `Timer` schema lines 6563-6645

**Exact body shape** — list the fields, required ones, enums.

**Example JSON** for a notice timer and a service level timer.

**Where it appears elsewhere:**
- Story E1-045 section 12 (line 194) only names `t

_[truncated]_

</details>
