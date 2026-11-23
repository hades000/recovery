# Rules Engine Configuration

- **Session ID:** `ses_e1fb1b790ffeBCs2lD6XDItKaH`
- **Created:** 2026-11-16 00:43  |  **Last activity:** 2026-11-16 00:49
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `build`
- **Tokens:** 208,120 in / 4,747 out / 16,580 reasoning
- **Messages:** 26

---

### User - 2026-11-16 00:43

in this cureent system eventually how are reules engine going to be used like if someone wants to change any rule what should they do

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

I'll look at how the rules engine is built in this codebase before answering.

<details><summary>Reasoning</summary>

The user is asking about "this current system" — the Recovery Workbench SharePoint Set v14 directory. They want to know how the rules engine is going to be used, and what someone should do to change a rule.

Let me explore the codebase to find the rules engine.

Let me start by looking at the directory structure.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Force | Select-Object Mode, Length, Name | Format-Table -AutoSize", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
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
d-----         ACE schema                          
d-----         aisdlc-playbook-main                
d-----         aisdlc-toolkit-main                 
d-----         E1-042 Migration and Clarifications 
d-----         _work                               
-a---- 7301630 13 AI-First SDLC repository.zip     



```

**Tool `glob`** - completed

```json
{"pattern": "**/*", "limit": 200}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave5_map.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\peek_cs.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\patch_index.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\an2.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\an1.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\verify.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\topo.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\scan.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\props.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\pptx4.txt
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\ids.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\final.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\dump_xlsx.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\dump_pptx.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\dump_docx.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_seq.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_release_xlsx.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_release_pptx.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_raids.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_order.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_depmap.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_defects.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_cutover.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\wave4\build_controls.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\build_notes_v5.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\build_index.py
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\build_control.py
C:\Users\SahilMore\Downloads\Recovery Workben
... truncated (23,114 chars total)
```

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

This is a documentation repository for a product called "Recovery Workbench". The user asks about the rules engine — "in this current system eventually how are rules engine going to be used like if someone wants to change any rule what should they do".

Let me find the Business Rules and Routing Logic doc and any rules engine design. There's `02 Business architecture and process\Recovery Workbench Business Rules and Routing Logic v4.xlsx` and `.html`. Also maybe `05 Technical architecture` has a rules engine design doc. Let me search.

</details>

**Tool `grep`** - completed

```json
{"pattern": "[Rr]ule[s]? [Ee]ngine", "limit": 60}
```

```text
Found 60 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\analysis\decision_log.txt:
  Line 58: B: all 448 routing rules.|A. The route decision goes live in a later epic.|Product owner|2026-10-30 00:00:00|Rules engine design; user stories, Epic 1|Epic 1 is measured against all 448 rules.|


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\_manifest.json:
  Line 6483:     "source_rel": "05 Technical architecture/Recovery Workbench Rules Engine Design v2.docx",

  Line 6484:     "source_name": "Recovery Workbench Rules Engine Design v2.docx",

  Line 6490:     "doc_title": "Rules engine design",

  Line 6491:     "title": "Recovery Workbench Rules Engine Design v2",


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\DOCUMENT_MAP.md:
  Line 349: | 05-019 | `05 Technical architecture/Recovery Workbench Rules Engine Design v2.docx` | 68 | Recovery Workbench Rules Engine Design v2 | 2 | .docx | Yes |  | `requirement/legacy/05-technical-architecture/recovery-workbench-rules-engine-design-v2-docx.md` |  | converted | 2 embedded image(s) not extracted; see original |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\12-project-communication\_csv\recovery-workbench-document-control-sheet-v10\control-sheet.csv:
  Line 80: 68,3. Supporting,Technical,Rules engine design,Recovery Workbench Rules Engine Design v2.docx,"SCB IT architecture, ACE team, TechX",SCB IT architecture,,Not started,,


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\12-project-communication\recovery-workbench-document-index-v11.md:
  Line 114: | 68 | Rules engine design | How the rules are authored, versioned, tested, deployed and rolled back, and how a decision is recorded. | Decision Model and Notation 1.4 | Recovery Workbench Rules Engine Design v2.docx |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\12-project-communication\recovery-workbench-document-control-sheet-v10-xlsx.md:
  Line 89: | 68 | 3. Supporting | Technical | Rules engine design | Recovery Workbench Rules Engine Design v2.docx | SCB IT architecture, ACE team, TechX | SCB IT architecture |  | Not started |  |  |


C:\Users\SahilMore\Downloads\Recovery Workbench Sha
... truncated (18,969 chars total)
```

**Tool `glob`** - completed

```json
{"pattern": "**/*Rule*", "limit": 50}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Data Quality and Reconciliation Rules v3.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Data Quality and Reconciliation Rules v2.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Business Rules and Routing Logic v4.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Business Rules and Routing Logic v4.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Rules Engine Design v2.docx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB TE 005 Rule table test harness v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 048 Rule change audit report v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 029 Rule load validation and rollback v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB TE 005 Rule table test harness v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 048 Rule change audit report v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 029 Rule load validation and rollback v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB TE 005 Rule table test harness v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extracted\RWB E1 048 Rule change audit report v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-story-files-v5_extract
... truncated (2,553 chars total)
```

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read the Rules Engine Design v2 doc converted markdown, plus the ADR-004, plus the user stories for rule change, plus the Business Rules and Routing Logic v4 HTML maybe. Let me check the converted legacy doc.

</details>

**Tool `glob`** - completed

```json
{"pattern": "**/recovery-workbench-rules-engine-design-v2*"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\05-technical-architecture\recovery-workbench-rules-engine-design-v2-docx.md
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\05 Technical architecture\\Recovery Workbench Architecture Decision Records v2.md", "offset": 110, "limit": 130}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Architecture Decision Records v2.md, lines 110-239
110: - Skills the ACE team and TechX already have
111: 
112: ### Options considered
113: 
114: 1. Case state as rows in the ACE database, moved by code, timers on Quartz, automated chains on Spring Batch with an outbox
115: 2. Temporal, with one workflow execution per case
116: 3. A commercial case management engine
117: 
118: ### Decision
119: 
120: Option 1. The case is modeled in CMMN 1.1 terms. Case, stage, task and timer state are rows. A wait of weeks is a row with a state and a stored due date. Temporal is not used; adding it later for a self-contained automation task needs its own decision record.
121: 
122: ### Consequences
123: 
124: - Good: no extra runtime for SCB to operate; a change to a handler is an ordinary release; state does not replay.
125: - Good: case terms mean the same in both modules.
126: - Bad: retry and compensation for automated chains are built with Spring Batch and an outbox.
127: 
128: ---
129: 
130: ## ADR-004 Hold every rule as versioned data
131: 
132: - Status: Accepted
133: - Date: 20 October 2026
134: - Deciders: SCB core team with Henka
135: - Decision log: DT02; Epic 1 rule scope DL24
136: 
137: ### Context and problem
138: 
139: Thresholds, limits, routes, timers and templates change often. If they are written in code, every change needs a release, and the business waits a month to move a number. ACE has rule based logic in code and no rules engine.
140: 
141: ### Decision drivers
142: 
143: - A business change without a code release
144: - An audit trail of which rule version decided each case
145: - Open cases kept on the version they were decided under
146: 
147: ### Options considered
148: 
149: 1. Rules as versioned rows, evaluated by a decision table component in the recovery module
150: 2. A commercial or open source rules engine
151: 3. Rules in Java code
152: 
153: ### Decision
154: 
155: Option 1. Every rule, limit, threshold, template, name, queue, role, timer and route is a data row with a version, valid from and valid to dates, an approver and a test case, changed through a validated load. Each route set is a decision table with hit policy Unique. Code holds the behavior; data holds the choices.
156: 
157: ### Consequences
158: 
159: - Good: a threshold moves on its effective date with no release, and rolls back the same way.
160: - 
... truncated (5,628 chars total)
```

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\requirement\\legacy\\05-technical-architecture\\recovery-workbench-rules-engine-design-v2-docx.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\05-technical-architecture\recovery-workbench-rules-engine-design-v2-docx.md, lines 1-126
1: <!-- source: 05 Technical architecture/Recovery Workbench Rules Engine Design v2.docx -->
2: <!-- converted: 2026-11-04 from DOCX -->
3: 
4: > **Source:** `05 Technical architecture/Recovery Workbench Rules Engine Design v2.docx`  
5: > **Converted from:** DOCX
6: 
7: Recovery Workbench
8: 
9: Rules engine design
10: 
11: SCB Collections and Recovery. Henka Group, 28 October 2026
12: 
13: | Item | Detail |
14: |---|---|
15: | Document | Recovery Workbench rules engine design |
16: | Version | 1 |
17: | Date | 28 October 2026 |
18: | Prepared by | Henka Group |
19: | Structure | Decision Model and Notation 1.4 decision tables, arc42 crosscutting concepts |
20: 
21: # 1. The design on one page
22: 
23: | Element | Design |
24: |---|---|
25: | What it is | A decision table evaluator inside the recovery module of ACE. No external rules engine |
26: | What it holds | 448 routing rules in ten route sets, the allocation table, thresholds, limits and timers, all as versioned data rows |
27: | Table form | DMN 1.4 decision tables: inputs, conditions, output, hit policy FIRST in row order |
28: | Authoring | Rule rows prepared in a workbook by the center of excellence, loaded as a file through the validated load |
29: | Testing | Every row names its test case. The rule table harness runs every row before a version can be approved |
30: | Approval | The process owner approves; Risk approves where a limit or threshold moves |
31: | Deployment | A version takes effect from its valid from date. No code release |
32: | Rollback | The previous version is loaded again with an immediate date |
33: | Record | Every evaluation that changes a case writes the rule ID, the version and the inputs to the decision log |
34: 
35: # 2. Route sets
36: 
37: | Route set | Rules | Decision |
38: |---|---|---|
39: | Restructure | 37 | D5, D6 |
40: | Settlement | 27 | D6.4 |
41: | Deed in lieu | 37 | D6.4 |
42: | Guarantee claim | 32 | D6.5, D6.6 |
43: | Litigation | 79 | D7 |
44: | Asset disposal | 72 | D8.1 to D8.3 |
45: | Debt sale | 41 | D8.4 |
46: | Write-off | 51 | D9 |
47: | Deviations | 22 | X1 to X7 |
48: | Universal rules | 50 | All |
49: | Total | 448 |  |
50: 
51: # 3. The structure of a rule row
52: 
53: | Column 
... truncated (6,529 chars total)
```

> **Synthetic** - 2026-11-16 00:43

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

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The user asks a conceptual question about how the rules engine will be used in the current system and what someone does to change a rule. I have the Rules Engine Design v2 doc. Let me also check the Business Rules and Routing Logic doc and user stories E1-029, E1-048, and maybe the admin model which describes who can change rules. Also the decision log for rule scope. This is a documentation repo, not code. Let me read relevant stories to get the current/eventual process with roles, screens, etc. Snippets.

Let me look at:
- RWB E1 029 Rule load validation and rollback
- RWB E1 048 Rule change audit report
- RWB TE 005 Rule table test harness
- Maybe story for rule authoring (E1-028?) and rule config screen.
- 05 TSD P4 Access and administration
- Business Rules and Routing Logic v4 HTML for table structure.
- Admin and Access Model v5 for roles (reference data administrator, center of excellence, process owner, risk).

Let me search for "rule" stories in Epic 1 story files.

</details>

**Tool `glob`** - completed

```json
{"pattern": "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6/*.md", "limit": 200}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 002 Case list v1 with case ID owner and queue v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 001 Recovery tables for the 14 data products v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\Read me first v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 013 Baseline measures v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 011 Reconciliation and data quality report v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 008 Decision log store v1 append only and hash chained v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 007 Integration adapters for file loads and outbound files v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 015 Freshness stamp per data product v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 014 Decision log copy to the data lake v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 016 Access control per data product and catalog entries v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 017 Retention and archive rule for the data store v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 018 Case ID issuance and case record v1 v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 042 Central configuration service and parameter catalog v
... truncated (13,867 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB E1 029 Rule load validation and rollback v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 029 Rule load validation and rollback v1.md, lines 1-361
1: # RWB-E1-029 Rule load, validation and rollback
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-E1-029 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | FEAT-CWC-14 Load a rule version with validation; FEAT-CWC-15 Roll back a rule version; FEAT-DRI-07 Run the rules component on versioned rule tables |
14: | Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004 |
15: | BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
16: | L3 process | 14 Set strategy, policy and decision rules; All recovery processes |
17: | Decision | None |
18: | Priority | Must |
19: | Depends on | None |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **center of excellence analyst (RW-COE)**, I want **an Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases and a dry run), a load with a version, approval, rollback by one call and a change log**, so that **a rule change goes from template to production without a code release**.
25: 
26: ## 2. Business rationale
27: 
28: Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). This story takes a rule version from one template through checks that refuse a bad table whole, an approval by Risk, a dated start and a one-call rollback, with each step in the change log. It meets REQ-CWC-013, REQ-CWC-014 and REQ-DRI-004, and covers the Epic 1 rule tables named in DL24: entry, exclusion, allocation, assignment and transfer.
29: 
30: ## 3. Preconditions
31: 
32: - The five rule tables are agreed for Epic 1: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (DL24, option A).
33: - Each table has 50 test cases with expected results, prepared by RW-COE in the template's Tests tab (assumed count from the current story).
34: - The loader holds RW-COE (Rules and parameters C); the approver holds RW-RISK (Rules and parameters A). One person may not hold both (separation of duty).
35: - Live cases exist for
... truncated (22,478 chars total)
```

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

This is very useful. Note a discrepancy: the Rules Engine Design v2 says DMN 1.4 hit policy FIRST in row order in one place and Unique elsewhere. The story says hit policy Unique. The design says "hit policy FIRST in row order" in section 1, and section 4 says first row that holds fires. And the story BR3 says Unique. Hmm. There's a contradiction worth flagging maybe. Actually the row structure table says hit policy FIRST, and section 4 says first match. Story says "Hit policy Unique: for one table, one trigger and one row order, one condition holds". That's a validation concept — no two rows overlap, so only one can match. Fine, equivalent to FIRST if unique.

Now let me look at E1-021 transfer rules and engine, E1-020 allocation engine, and E1-048 rule change audit report. Also read the Business Rules and Routing Logic v4 HTML to see route sets. And maybe TSD P4 access admin for rules screens (Epic 8 SCR-39). Also the Admin and Access Model for roles and authority (Rules and parameters rights A/C/R/U).

Let me read those.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB E1 021 Transfer rules and engine v1 v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 021 Transfer rules and engine v1 v1.md, lines 1-392
1: # RWB-E1-021 Transfer rules and engine v1
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-E1-021 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | FEAT-CWC-10 Run the transfer rule table and engine |
14: | Requirement IDs | REQ-CWC-010, REQ-CWC-016 |
15: | BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
16: | L3 process | All recovery processes |
17: | Decision | None |
18: | Priority | Must |
19: | Depends on | RWB-E1-028, RWB-E1-020, RWB-E1-027 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **team manager (RW-TEAMMGR)**, I want **cases moved between queues and roles by the transfer rule table on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason**, so that **hand-offs between teams run without email**.
25: 
26: ## 2. Business rationale
27: 
28: A case changes hands between the TDR, litigation, NPA and debt sale teams by email today, and the case can wait between teams with nobody holding it. This story moves the case by rule when one of eight triggers fires, picks the owner in the receiving queue, ends the old assignment and records the rule and version, and gives the team manager a programmatic transfer with a coded reason before the Epic 2 screens. It meets REQ-CWC-010 and REQ-CWC-016.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-020 is done: AssignmentEngine and the queue structure are in use.
33: - RWB-E1-028 is done: timers publish TimerDue when a timer other than a service level expires. A service level breach (TimerBreached) never moves the case (R-UNI-30).
34: - RWB-E1-027 is done: the decision log writer is available.
35: - The transfer rows version "TRF-2026.11" (rule table TRANSFER) are loaded through RWB-E1-029. Each row holds trigger event, condition, target queue code and row order.
36: - The transfer reason list LOV-TRANSFER-REASON holds R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue (DL23).
37: - Manual transfer ca
... truncated (24,898 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB E1 048 Rule change audit report v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 048 Rule change audit report v1.md, lines 1-299
1: # RWB-E1-048 Rule change audit report
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-E1-048 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | FEAT-CWC-16 Report every rule change for audit |
14: | Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
15: | BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
16: | L3 process | 14 Set strategy, policy and decision rules |
17: | Decision | None |
18: | Priority | Should |
19: | Depends on | RWB-E1-037, RWB-E1-011, RWB-E1-043 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **center of excellence analyst (RW-COE)**, I want **the parameter change and rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every change and reported for audit**, so that **a configuration change is as controlled as a code change**.
25: 
26: ## 2. Business rationale
27: 
28: Audit found the collection procedure was not followed because rules lived in documents (CTL-08). When rules and limits are data, a wrong row changes every case it touches, so each change needs the same evidence as a code change: who asked, what it affects, the test result, who approved, when it took effect and how to undo it. This story makes the checklist fields required before a version can be approved and gives audit one report of every change. It meets REQ-CWC-013 and REQ-DRI-011. The measure is that every version in force has a complete checklist in the report.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-043 is done: every reference table version is a row in `reference_version` with author and approver.
33: - RWB-E1-037 is done: the permission matrix gives Rules and parameters R to RW-COE, RW-RISK and RW-AUDIT.
34: - RWB-E1-011 is done: the daily data quality report lists refused loads.
35: - Rule versions loaded through `POST /admin/rule-versions` (RWB-E1-029) are recorded in the same registry with table code `RULE_` and the route set, for example `RULE_UNIVERSAL_RULES`.
36: - The rule table test harness (RWB-TE-005) writes its result to the versio
... truncated (19,877 chars total)
```

### Assistant - 2026-11-16 00:43 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now, let me look at the Business Rules and Routing Logic v4 HTML to understand the 448 rules, and see the ADR. Also Epic 8 admin screen SCR-39 for rule authoring in future. And maybe the TSD P4 access and administration says rules screen future. Let me check the HTML, and maybe the "Business Rules and Routing Logic v4.xlsx" sheet names. The HTML could be big. Let's peek.

Also, the user asks "in this current system eventually how are rules engine going to be used like if someone wants to change any rule what should they do". They might expect a practical answer: where rules live, who changes, the workflow, timeline (Epic 1 via Excel, Epic 8 via screen). Let me gather details on Epic 8 SCR-39 and the eventual UI. Search "SCR-39".

</details>

**Tool `grep`** - completed

```json
{"pattern": "SCR-39", "limit": 40}
```

```text
Found 40 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v5\Recovery Workbench FSD P4 Access and administration v3.md:
  Line 2630: | SCR-39 Rules and parameters | Rule versions, route sets, thresholds and timers, with the load and approval | E8; by file load before |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v3.md:
  Line 204: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 623: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 787: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 869: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 951: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 1030: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 1270: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 1350: | SCR-39 Rules and parameters | Versions; load; approval |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v2.md:
  Line 201: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 616: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 780: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 862: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 944: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 1023: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 1263: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 1343: | SCR-39 Rules and parameters | Versions; load; approval |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB TE 005 Rule table test harness v1.md:
  Line 252: No screen in this story. The center of excellence analyst reads the result in the load response and on the version list; the rules and parameters screen SCR-39 shows it from Epic 8. Developers read the named rule tests in the build report.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 048 Rule change audit report v1.md:
  Line 260: No screen in this story. Internal audit and the center of excel
... truncated (6,353 chars total)
```

**Tool `shell`** - completed

```json
{"command": "$f = 'C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\02 Business architecture and process\\Recovery Workbench Business Rules and Routing Logic v4.html'; (Get-Item $f).Length; (Get-Content $f -TotalCount 60) -join \"`n\""}
```

```text
"><td class="">R-DS-39</td><td class="">Debt sale</td><td class="code">PUTBACK_REFUSED</td><td class="code">CLAIM_CLOSED</td><td class="">Any</td><td class="">Close the lot with realized recovery recorded</td><td class="code">LOT_CLOSED</td><td class="">Debt sale officer</td><td class="">None</td></tr><tr data-g="DEBTSALE"><td class="">R-DS-40</td><td class="">Debt sale</td><td class="code">BUYER_REJECTED</td><td class="code">BUYER_REMEDIATED</td><td class="">the buyer supplies the missing KYC or license evidence inside the window</td><td class="">Re-open the qualification check</td><td class="code">BUYER_PENDING_KYC</td><td class="">Debt sale officer</td><td class="">10 working days</td></tr><tr data-g="DEBTSALE"><td class="">R-DS-41</td><td class="">Debt sale</td><td class="code">BUYER_REJECTED</td><td class="code">BUYER_BARRED</td><td class="">no evidence supplied inside the window, or the failure is a license breach</td><td class="">Remove the buyer from the panel and release the lot to the next bidder</td><td class="code">BACK_TO_CASE_LIST</td><td class="">Head of Asset Liquidity</td><td class="">None</td></tr><tr data-g="WRITEOFF"><td class="">R-WO-01</td><td class="">Write-off</td><td class="code">SCAN_DUE</td><td class="code">MONTHLY_SCAN_STARTED</td><td class="">cut_off_date reached and the ALS load is complete</td><td class="">Test every open case against the eligibility rule on both tracks and the tax criteria</td><td class="code">POPULATION_PROPOSED</td><td class="">Write-off team</td><td class="">monthly cut-off</td></tr><tr data-g="WRITEOFF"><td class="">R-WO-02</td><td class="">Write-off</td><td class="code">SCAN_DUE</td><td class="code">ALS_LOAD_FAILED</td><td class="">the ALS extract is absent for the cut-off date</td><td class="">Hold the scan and raise an incident</td><td class="code">SCAN_HELD</td><td class="">Write-off team</td><td class="">1 working day</td></tr><tr data-g="WRITEOFF"><td class="">R-WO-03</td><td class="">Write-off</td><td class="code">SCAN_DUE</td><td class="code">TAX_CRITERIA_UNPUBLISHED</td><td class="">tax_criteria_version absent</td><td class="">Hold the scan until Finance publishes the version</td><td class="code">SCAN_HELD</td><td class="">Write-off team</td><td class="">None</td></tr><tr data-g="WRITEOFF"><td class="">R-WO-04</td><td class="">Write-off</td><td class="code">SCAN_HELD</td><td class="code">LOAD_RESTORED</td><td class="">the ALS extract is complete and the tax criteria published</td><td class="">Re
... truncated (51,373 chars total)
```

### Assistant - 2026-11-16 00:44 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The HTML is a single-line minified-ish page. Let me get the tab headers and early intro content. But I already have enough on rules. Let me look at the Business Rules doc for the description of tab/route sets and versioning. Let me extract the first part of the HTML with a regex-based text strip maybe. Actually I might not need it.

Now the question: "in this current system eventually how are rules engine going to be used like if someone wants to change any rule what should they do". They want an explanation of the operating model. I should explain:

1. What the "rules engine" actually is: not a separate product/engine. It's a decision-table evaluator inside the recovery module. Rules are data rows in PostgreSQL (rule_row), versioned (rule_version), evaluated by code that reads the route set version in force.

2. How it gets used during a case's life: events trigger evaluation (loads, screen actions, partner results, timers, other modules). Evaluator matches from_state/event, evaluates conditions in row order (hit policy FIRST/Unique), first match fires; if none, exception queue + gap logged (R-UNI-41). Decision log written first with rule ID + version; then action (state move, task/timer, outbound). Cases keep the rule version they were decided under (R-UNI-38), so new versions don't retroactively change open cases.

3. Where the rules are visible to business: 448 routing rules across 10 route sets (plus universal 50), thresholds, limits, timers, templates etc. Row structure fields.

4. What someone does to change a rule, eventually:
   - Path A (now/Epic 1, file load): Center of excellence analyst edits the route set workbook (Rows + Tests tabs) with test case per row; RW-REFADM or RW-COE loads via POST /admin/rule-versions (xlsx, route set, validFrom); validator checks schema, overlaps, unreachable rows, default row, 50 test cases; dry run against open cases; refuses entire load on any failure; RW-RISK approves (cannot be author); effective on valid from date; rollback one call with reason; change checklist (CR ref, impact, rollback plan, test result) required at approval; every load/approve/rollback in change log.
   - Path B (Epic 8, SCR-39): Rules and parameters screen in Admin — versions, route sets, thresholds and timers, load and approval. Same backend, same checks. So eventually business users do this in the UI instead of Excel/API.
   - Role split: RW-COE prepares; RW-REFADM loads; RW-RISK approves; RW-AUDIT reads/exports; RBAC "Rules and parame

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "rule change|Rule change|rules and parameters|Rules and parameters", "include": "*.md", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\01 Decisions and governance", "limit": 40}
```

```text
No matches found
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB TE 005 Rule table test harness v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB TE 005 Rule table test harness v1.md, lines 1-289
1: # RWB-TE-005 Rule table test harness
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: 
8: | Item | Value |
9: |---|---|
10: | Story key | RWB-TE-005 |
11: | Epic | E1, release 30 November 2026 |
12: | Module | P3 Case and workflow |
13: | Feature | None (technical enabler) |
14: | Requirement IDs | REQ-CWC-014, REQ-CWC-013 |
15: | BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, section 5.3 |
16: | L3 process | All recovery processes |
17: | Decision | None |
18: | Priority | Must |
19: | Depends on | RWB-E1-044 |
20: | Status | Ready for build |
21: 
22: ## 1. Story
23: 
24: As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.
25: 
26: ## 2. Business rationale
27: 
28: The routing logic is 448 rules in ten route sets, held as data (ADR-004). A wrong condition or owner in one row moves every case that reaches it, and the bank has no test that proves a row does what its owner expects. Every rule row already names a test case (`rule_row.test_case_id`). This story runs those test cases on every rule load and in every build, and marks a version failed when any test fails. It meets REQ-CWC-014 and REQ-CWC-013. The measure is that every rule row in force has a passing test with its rule ID.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-044 is done: migrations run with the parameterized schema.
33: - The rules component evaluates a route set as a decision table with hit policy Unique (ADR-004).
34: - The rule load template (RWB-E1-029) carries a Tests sheet with one test case per rule row.
35: - Rule rows exist with a `test_case_id` for each row (DF-REF-015, required).
36: - The Restructure route set is loaded in SIT with its 37 rows, R-RES-01 to R-RES-37.
37: - The loader holds RW-COE (Rules and parameters C).
38: 
39: ## 4. Flow
40: 
41: 1. Center of excellence analyst: loads a rule version through `POST /admin/rule-versions` with the rules and the Tests sheet.
42: 2. P4 load handler: stores the rule rows and calls `RuleTableHarness.run(r
... truncated (17,446 chars total)
```

### Assistant - 2026-11-16 00:44 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. Now let me check the Administration Stories for Epic 8 SCR-39 — how screens will look and what they allow. Search for FEAT-ADM-02 and SCR-39 context in Administration Stories v3.

</details>

**Tool `grep`** - completed

```json
{"pattern": "Rules and parameters|FEAT-ADM-02|FEAT-ADM-08", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Administration Stories v3.md", "limit": 80}
```

```text
Found 48 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v3.md:
  Line 108: | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

  Line 109: | POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |

  Line 121: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 122: | Rules and parameters | C | RW-COE |

  Line 197: | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

  Line 204: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 211: | Rules and parameters | A | RW-RISK |

  Line 452: | POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |

  Line 453: | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

  Line 465: | Rules and parameters | C | RW-COE |

  Line 466: | Rules and parameters | A | RW-RISK |

  Line 617: | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

  Line 623: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 631: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 780: | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

  Line 781: | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

  Line 787: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 794: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 795: | Rules and parameters | A | RW-RISK |

  Line 862: | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

  Line 869: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 876: | Rules and parameters | A | RW-RISK |

  Line 944: | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

  Line 945: | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

  Line 951: | SCR-39 Rules and parameters | Versions; load; approval |

  Line 958: | Rules and parameters | A | RW-RISK |

  Line 959: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE an
... truncated (4,283 chars total)
```

### Assistant - 2026-11-16 00:44 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read the beginning of Administration Stories v3 around line 80-230 to understand which story covers rule administration.

</details>

**Tool `read`** - completed

```json
{"limit": 190, "offset": 1, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Administration Stories v3.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v3.md, lines 1-190
1: # Recovery Workbench administration stories
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: | Item | Value |
8: |---|---|
9: | Stories in this file | 22 |
10: | By epic | E4: 1, E8: 21 |
11: | Related stories already in the Epic 1 and Epic 2 backlog | 10 |
12: 
13: User and role administration, reference data, rule versions, queue and timer configuration, job and ACE batch monitoring, and the audit log. Epic 1 builds the services and the reference and rule loads by file; these stories add the administration screens and approvals in Epic 8, when full administration is delivered, and partner administration in Epic 4.
14: 
15: Version 3 is re-based on D-RCV-35 and ADR-010. The Workbench loads no source data: the job monitor shows Workbench jobs beside the ACE batch status, the console shows reconciliation breaks, and masking profiles name the columns of the recovery.v_ace_* views. Two stories are rewritten around the read path (RWB-AD-018, RWB-AD-019) and one is a minor edit (RWB-AD-004).
16: 
17: ## Administration already in the backlog
18: 
19: | Key | Title | Module | Epic |
20: |---|---|---|---|
21: | RWB-E1-022 | Sign-on with SSO, MFA and the first roles | P4 | E1 |
22: | RWB-E1-029 | Rule load, validation and rollback | P3 | E1 |
23: | RWB-E1-034 | Letter template management | P6 | E1 |
24: | RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | P4 | E1 |
25: | RWB-E1-038 | Delegation of authority table as reference data | P4 | E1 |
26: | RWB-E1-039 | Access log into the decision log and break-glass admin | P4,P7 | E1 |
27: | RWB-E1-041 | Retention classes and virus scan on intake | P5 | E1 |
28: | RWB-E1-043 | Reference data service with versioned tables | P3 | E1 |
29: | RWB-E1-048 | Rule change audit report | P3 | E1 |
30: | RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | P2 | E1 |
31: 
32: ## Stories in this file
33: 
34: | Key | Title | Module | Epic | Depends on |
35: |---|---|---|---|---|
36: | RWB-AD-001 | Map Entra ID groups to Workbench roles | P4 | E8 | RWB-E1-022 |
37: | RWB-AD-002 | Permission matrix as a versioned load | P4 | E8 | RWB-E1-037 |
38: | RWB-AD-003 | Scope per role | P4 | E8 | RWB-E1-037 |
39: | RWB-AD-004 | Masking profiles per role | P4 | E8 | RWB-E
... truncated (9,361 chars total)
```

### Assistant - 2026-11-16 00:44 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read the RWB-AD-011 through 013 stories for the rule admin screen. Search line numbers.

</details>

**Tool `grep`** - completed

```json
{"pattern": "## RWB-AD-011|## RWB-AD-012|## RWB-AD-013", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Administration Stories v3.md"}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v3.md:
  Line 902: ## RWB-AD-011 Load a rule version

  Line 982: ## RWB-AD-012 Approve a rule version

  Line 1063: ## RWB-AD-013 Roll back a rule or reference version

```

### Assistant - 2026-11-16 00:44 | opencode-go/deepseek-v4.1-flash | build

**Tool `read`** - completed

```json
{"limit": 245, "offset": 902, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench Administration Stories v3.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v3.md, lines 902-1146
902: ## RWB-AD-011 Load a rule version
903: 
904: | Item | Value |
905: |---|---|
906: | Epic | E8, release 30 June 2027 |
907: | Module | P4 Access and administration |
908: | Feature | None |
909: | Process | All recovery processes |
910: | Priority | Must |
911: | Depends on | RWB-E1-029 |
912: | Decision | DL24 |
913: 
914: **Story.** As a center of excellence analyst, I want a route set loaded as a new rule version where each row names its test case, so that rules change as data and every row is tested.
915: 
916: **Acceptance criteria**
917: 
918: ```gherkin
919: Feature: Load a rule version
920: 
921:   Scenario: AC1 Rule rows tested
922:     Given a route set file where every row has a test case ID
923:     When I load it
924:     Then the rule table tests run in SIT and the result is attached to the version
925: 
926:   Scenario: AC2 Row without a test
927:     Given a row with no test case ID
928:     When I load it
929:     Then the system refuses the version
930: ```
931: 
932: **Data**
933: 
934: | Entity | Fields | BR Field IDs |
935: |---|---|---|
936: | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
937: | document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
938: | rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
939: 
940: **Endpoints**
941: 
942: | Method | Path | Access |
943: |---|---|---|
944: | POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
945: | GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |
946: 
947: **Screen and states**
948: 
949: | Screen | States |
950: |---|---|
951: | SCR-39 Rules and parameters | Versions; load; approval |
952: | SCR-47 Personal data | Loading; list |
953: 
954: **Permission checks**
955: 
956: | Capability area | Right | Roles that hold it |
957: |---|---|---|
958: | Rules and parameters | A | RW-RISK |
959: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |
960: 
961: **Validation and messages**
962: 
963: | ID | Type | Message |
964: |---|---|---|
965: | MSG-P4-004 | Warning | Emergency access is on until 
... truncated (9,998 chars total)
```

### Assistant - 2026-11-16 00:44 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now I have a clear picture. Let me also check the FSD P4 section on rules engine and admin behavior, or the TSD P4. But the answer is already well-supported.

Let me confirm rule set count and route sets from Business Rules doc: 448 rules in 10 route sets, and universal 50 are among the 10. Yes: Restructure 37, Settlement 27, Deed in lieu 37, Guarantee 32, Litigation 79, Asset 72, Debt sale 41, Write-off 51, Deviations 22, Universal 50 = 448.

Let me also check the "Rule engine design" says DMN 1.4, but AGENTS.md says "must never add a rules engine or any new dependency" — this is important nuance: ADR-004 says build the evaluator in the recovery module, no external engine. So someone asking "how is the rules engine going to be used" should be told: there is no separate third-party rules engine; it's an in-house decision-table evaluator in the recovery module. The "rules engine" is code that reads versioned data rows.

Also worth noting: AI agents use rules as fallback (R-UNI-32). There are agent stories. But not necessary.

Let me check the E1-020 allocation story briefly for rule evaluation order and the version pinning behavior. Actually enough.

Let me also check whether there is a distinction between "rule_row" (routing) and "reference tables" (thresholds, limits, routes, timers, templates). ADR-004 says every rule, limit, threshold, template, name, queue, role, timer and route is a data row with version, valid from/to, approver, test case. But stories split rule tables (ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER) from reference tables (service levels, queues, LOV, delegation). The Rules Engine Design focuses on routing rules. The user says "any rule" — I should distinguish:
- Routing/business rules: rule_row, loaded via rule-versions, tested by harness, approved by Risk.
- Reference/parameter values (thresholds, timers, queues, DoA, templates): reference tables loaded via reference-loads, same version + approval pattern, no rule evaluation; governed by RWB-E1-043 and SCR-40.

This distinction matters for "change any rule": the route depends on what kind of rule it is.

Let me quickly inspect E1-043 to get the reference data lifecycle details (VALIDATED, APPROVED, IN_FORCE, etc.) and who does what, so I can explain both paths accurately.

</details>

**Tool `grep`** - completed

```json
{"pattern": "^## |^\\*\\*Story|State transitions|VALIDATED|IN_FORCE|approve|load", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB E1 043 Reference data service with versioned tables v1.md", "limit": 80}
```

```text
Found 80 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 043 Reference data service with versioned tables v1.md:
  Line 22: ## 1. Story

  Line 24: As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority and legal periods held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.

  Line 26: ## 2. Business rationale

  Line 28: Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. This story gives every reference table a version with a valid from date, an author and a different approver, and serves the version in force to the engines. The holiday calendar is not one of them: ACE holds the Bank of Thailand calendar in `bot_holiday`, and the timer engine reads it through `v_ace_holiday`, so no Workbench list holds holidays and no holiday load is needed. It meets REQ-DRI-011 and REQ-CWC-006 and supports control CTL-08 (a rule, limit or list changes only through a validated load approved by its owner). The measure is that every value an engine reads carries a table code and a version number in its log line.

  Line 30: ## 3. Preconditions

  Line 34: - The list LOV-REF-TABLE (new, see Additions) is loaded with the 12 table codes in section 8, BR1.

  Line 35: - The reference load endpoint `POST /api/recovery/v1/admin/reference-loads` (P4) is deployed and calls this story's published interface.

  Line 36: - The loader holds RW-REFADM (Reference data C). The approver holds the approve right in Reference data (assumed RW-RISK; see section 10).

  Line 39: ## 4. Flow

  Line 41: 1. Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.

  Line 42: 2. P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.

  Line 44: 4. Reference data service: writes one `reference_version` row with status VALIDATED and one `reference_row` row per file row, in one transaction.

  Line 45: 5. Approver: approves the loa
... truncated (9,973 chars total)
```

### Assistant - 2026-11-16 00:45 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. Now I have a full picture. Let me consider whether the user wants a high-level explanation or an implementation-oriented one. The question: "in this cureent system eventually how are reules engine going to be used like if someone wants to change any rule what should they do"

Likely they're reviewing this spec set and want to understand the operating model. I'll answer in plain English with a clear "how it works" and "how to change a rule" flow. Maybe include a UI block (steps or table) since this is a process/flow — the guidance says use a UI block for flows/steps/status. I can include a `Steps` block for the change process and a table for roles. That would be useful.

I should be careful: the answer must be grounded in the documents, and I should flag where it's a future epic (Epic 8) versus current design.

Let me structure:

**Short answer:** It's not a third-party rules engine. It's a decision-table evaluator inside the recovery module; rules are versioned data rows. Business people never edit code or the database — they prepare a rule workbook, load it, it's validated + tested + dry-run, Risk approves, it goes live on a date, and it can be rolled back.

**1. How it runs during a case**
- Case event arrives (load, screen action, partner result, timer, another module).
- Evaluator picks the rule version pinned to the case (R-UNI-38).
- Finds rows for from-state/event, evaluates condition in row order, first match fires (Unique check enforced).
- No match → exception queue + rule gap logged.
- Decision log entry (rule ID + version + inputs) written first; if it fails, nothing changes.
- Action executes: state move, task/timer, outbound event.

Where used: 448 routing rules in 10 route sets (list), plus universal rules. Also allocation/assignment/transfer/entry/exclusion. Eventually all recovery stages (restructure, settlement, deed in lieu, guarantee, litigation, asset disposal, debt sale, write-off, deviations, universal). Also AI agents fall back to rule result (R-UNI-32) — optional mention.

**2. What "a rule" is**
- Row: rule ID, route set, from state, event, condition (FEEL), action, to state, owner, timer, test case, valid from/to, version.
- Behavior is code; choices are data. You can change thresholds/routes/conditions/timers/owners via data; a brand-new action/event/condition function still needs code.

**3. How to change one — the eventual process**
Six steps: request → prepare → load → test/dry run → approve → in force; verify; rollback

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "$exts = @('*.java','*.ts','*.tsx','*.sql'); foreach ($e in $exts) { $c = (Get-ChildItem -Recurse -File -Filter $e -ErrorAction SilentlyContinue | Measure-Object).Count; \"$e = $c\" }", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
*.java = 0
*.ts = 6
*.tsx = 0
*.sql = 30

```

### Assistant - 2026-11-16 00:45 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The .ts files are likely in the AI-First SDLC repo tooling. So this is a document repo, not the actual Workbench code. I'll mention it's the specification, not a running rules engine.

Now let me consider if I should quote exact rule IDs. Yes, a few key ones make the answer concrete:
- R-UNI-38 (version pinning)
- R-UNI-39 (decision log first)
- R-UNI-40 (duplicate event)
- R-UNI-41 (no row → exception queue / rule gap)
- R-UNI-42? not needed.
- R-UNI-32 (agent fallback) optional.

And story keys:
- RWB-E1-029 (load/validate/rollback)
- RWB-TE-005 (test harness)
- RWB-E1-048 (change audit report)
- RWB-AD-011/012/013 (Epic 8 screens)
- ADR-004.

Now, structure of answer:

Opening: "It's not a separate rules engine product. ADR-004 / AGENTS.md explicitly say no external rules engine — it's a decision-table evaluator inside the recovery module. Code holds behaviour, data holds choices."

Then Section 1: How it's used at runtime.
Maybe a compact numbered list.

Then Section 2: The change process (UI Steps).

Then Section 3: Who does what (table).

Then Section 4: Now vs later (Epic 1 vs Epic 8; five tables vs 448; reference data path).

Then Section 5: What you should actually do (practical step-by-step addressed to the person). Maybe combine with Section 2. The user asked "what should they do" — I can phrase the flow in second person.

Then "Limits / gotchas": what a rule change cannot do; author cannot approve; cases keep old version; past-dated loads refused; whole-file refusal; test count.

Then a short "Docs note / inconsistency" maybe 2 bullets:
- hit policy FIRST vs Unique
- route set example UNIVERSAL_RULES for ALLOCATION
- approval authority (process owner vs RW-RISK) mismatch

Should I include these? It shows depth and is genuinely useful for someone relying on the docs. But the user asked a simple question; too much doc QA could distract. I'll put a small "Two things the docs leave inconsistent" in a Details block maybe. The UI block has Details component. But the final answer can include a compact bullet list at the end. I think one or two are worth it because they affect "what someone should do."

Let me weigh: If I say "Risk approves" but the design says "process owner approves," that's a real ambiguity for someone changing a rule. I should definitely clarify. The E1-029 story is more concrete and current; the target design says process owner. I'll present: "Epic 1: RW-RISK signs every rule version. The target design says the process owner appro

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "rule_version|R-UNI-38|version in force", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB E1 020 Allocation and assignment engine v1 v1.md", "limit": 40}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 020 Allocation and assignment engine v1 v1.md:
  Line 232: | DF-CAS-021 | recovery_case | rule_version | Write |

  Line 246: | DF-REF-003 | rule_row | rule_version | Read |

  Line 337: - Writes: recovery_case (status, owner_user_id, queue_id, team_code, stage_clock_start, rule_version, last_allocation_date, version), queue (rr_cursor_user_id), assignment (all columns), outbox.

```

### Assistant - 2026-11-16 00:46 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The case gets a `rule_version` written at allocation. So yes, the case pins the rule version at allocation/decision. I'll say the case carries the rule version it was decided under.

Now let me also check the Business Rules doc intro for "version" and "checks" to see if there's a stated change process. The HTML has tabs; maybe the first tab has "how to read" or "governance". Let me extract text from the top of the HTML before the first table. The file is one long line; I can strip tags with PowerShell and grab the first N chars.

</details>

**Tool `shell`** - completed

```json
{"command": "$f = 'C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\02 Business architecture and process\\Recovery Workbench Business Rules and Routing Logic v4.html'; $h = Get-Content $f -Raw; $t = [regex]::Replace($h, '<script[\\s\\S]*?</script>', ' '); $t = [regex]::Replace($t, '<style[\\s\\S]*?</style>', ' '); $t = [regex]::Replace($t, '<[^>]+>', ' '); $t = [System.Net.WebUtility]::HtmlDecode($t); $t = [regex]::Replace($t, '\\s+', ' '); $t.Substring(0, [Math]::Min(6000, $t.Length))"}
```

```text
 Recovery Workbench Business Rules and Routing Logic COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench Business Rules and Routing Logic SCB Collections and Recovery. Henka Group, 28 October 2026. Version 3. Overview Entry and routes Restructure Settlement Deed in lieu Guarantee claim Litigation Asset disposal Debt sale Write-off Deviations Universal rules All rules Completeness checks How a case is routed Every move a case makes is one rule. When an event arrives at a case in a given state and the condition holds, the Workbench takes the action, moves the case to the next state, gives it to the named owner and starts the timer. There are 448 rules in ten route sets. Rules 448 Route sets 10 Rules with a timer 252 of 448 Rules whose next state a person or partner owns 366 of 448 The decision table Each route set is one decision table in Decision Model and Notation 1.4. Column Kind Meaning Rule Identifier R, the route set code and a number, for example R-LIT-12 From state Input The state the case is in when the event arrives Event Input What happened: a payment, a document, a decision, a date reached, a partner result Condition Input What must hold for the rule to fire. Any means the event alone fires it Action Output What the Workbench does To state Output The state the case moves to Owner Output Who holds the case in the next state. Workbench means no person Systems Output The systems the action reads or writes Timer Output How long the next state may last before it escalates Hit policy: Unique In a route set, for one state and one event, at most one condition holds, so one rule fires. Rules held as data Every rule is a row in a versioned table, with its rule ID, version, valid from, valid to, author, approver and test case ID. A rule change is a validated data load, not a code release. A case keeps the rule version it was decided under, and the decision log records the rule ID and version for every move. The route sets Route set Decision Rules States End states With a timer Owned by a person or partner Restructure, TDR D5, D6 37 18 3 15 30 Settlement D6.4 27 15 2 12 20 Deed in lieu and voluntary surrender D6.4 37 20 2 15 28 Guarantee claim, D6.5 and D6.6 D6.5, D6.6 32 17 2 21 24 Litigation and enforcement, D7 D7 79 38 4 62 65 Asset disposal, D8.1 to D8.3 D8.1 to D8.3 72 40 4 31 60 Debt sale, D8.4 D8.4 41 29 2 15 33 Write off and recover after charge-off, D9 D9 51 27 2 31 43 Deviations X1 to X7 X1 to X7 22 9 3 6 19 Universal rules, any state All 50
... truncated (6,002 chars total)
```

### Assistant - 2026-11-16 00:46 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Excellent. This gives the crisp definition: "Every move a case makes is one rule. When an event arrives at a case in a given state and the condition holds, the Workbench takes the action, moves the case to the next state, gives it to the named owner and starts the timer. There are 448 rules in ten route sets." Hit policy Unique. "Rules held as data: Every rule is a row in a versioned table, with its rule ID, version, valid from, valid to, author, approver and test case ID. A rule change is a validated data load, not a code release."

This is the core answer. I'll quote/paraphrase that.

Now, the user may not want all the detail. Let me craft a strong, readable answer with a mental model, the change procedure, and the practical "who do I ask."

Let me plan the final response:

**Opening**
"Short version: there is no separate third-party rules engine. Every case move is a row in a versioned decision table, and a small evaluator inside the recovery module executes it. So 'changing a rule' is a controlled data change, not a code change — except when the change needs new behaviour."

**How it will be used (runtime)**
Use a short numbered list:
- Event arrives (load, screen action, partner result, timer, another module).
- Evaluator reads the route-set version the case is on; finds rows matching current state + event.
- Tests conditions in row order; exactly one should match (Unique enforced by the loader). It fires.
- Action runs: state move, owner/queue, task, timer, outbound event.
- Decision log entry first, with rule ID + version + inputs; if log write fails, nothing moves.
- No row matches → exception queue, gap logged (R-UNI-41), so the rule set gets fixed rather than guessed.
- Cases keep the version they were decided under (R-UNI-38), and the decision log is the audit trail.

Mention scope: 448 rules / 10 route sets; covers route choice and each stage transition, plus universal rules that run in every state; later the same component serves allocation, assignment, transfer, entry/exclusion, timers. AI agents fall back to the deterministic rule result if they fail/time out (R-UNI-32) — maybe one line.

**What a rule is**
A row with: rule ID, route set, from state, event, condition (FEEL), action, to state, owner, timer, test case, valid from/to, version. From design section 3. The case state machine's transition table.

**What changing one looks like (eventually)**
UI Steps block.
Then roles table (small).

**Two lanes**
Table: routing rule vs reference v

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "Rules and parameters \\| [CRUDA]|Rules and parameters.*\\| [CRUDA]", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories", "limit": 60}
```

```text
Found 60 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v2.md:
  Line 118: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 119: | Rules and parameters | C | RW-COE |

  Line 208: | Rules and parameters | A | RW-RISK |

  Line 378: | Rules and parameters | C | RW-COE |

  Line 379: | Rules and parameters | A | RW-RISK |

  Line 458: | Rules and parameters | C | RW-COE |

  Line 459: | Rules and parameters | A | RW-RISK |

  Line 624: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 787: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 788: | Rules and parameters | A | RW-RISK |

  Line 869: | Rules and parameters | A | RW-RISK |

  Line 951: | Rules and parameters | A | RW-RISK |

  Line 952: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 1030: | Rules and parameters | A | RW-RISK |

  Line 1031: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 1106: | Rules and parameters | C | RW-COE |

  Line 1107: | Rules and parameters | A | RW-RISK |

  Line 1187: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 1188: | Rules and parameters | A | RW-RISK |

  Line 1269: | Rules and parameters | A | RW-RISK |

  Line 1270: | Rules and parameters | C | RW-COE |

  Line 1349: | Rules and parameters | A | RW-RISK |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v3.md:
  Line 121: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

  Line 122: | Rules and parameters | C | RW-COE |

  Line 211: | Rules and parameters | A | RW-RISK |

  Line 465: | Rules and parameters | C | RW-COE |

  Line 466: | Rules and parameters | A | RW-RISK |

  Line 631: | Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW
... truncated (5,169 chars total)
```

### Assistant - 2026-11-16 00:47 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

No U right in the matrix for rules, only C, A, R. The rollback endpoint requires U, but no role holds U. That's a real gap. E1-029 authority says RW-COE calls rollback (Rules and parameters CRUD), but the permission matrix says only C. Hmm. Maybe "CRUD" is a generic label, not the four rights. The permission letters in this system: C, R, U, D, A? Let me check the roles model. Search "permission letters".

</details>

**Tool `grep`** - completed

```json
{"pattern": "permission letter|Permission letter|rights? (C|R|U|D|A)|C create|U update", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\01 Decisions and governance\\Recovery Workbench Admin and Access Model v5.docx", "limit": 20}
```

```text
No matches found
```

**Tool `glob`** - completed

```json
{"pattern": "**/admin-and-access-model-v5*"}
```

```text
No files found
```

### Assistant - 2026-11-16 00:47 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me search in the converted legacy docs.

</details>

**Tool `grep`** - completed

```json
{"pattern": "permission letter|Permission letter|rights are|rights C, R|rights R, C", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\requirement\\legacy", "limit": 30}
```

```text
Found 11 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-build-notes-epic-1-v4.md:
  Line 1319: The person makes the call and the check runs on its own on the server. Every endpoint declares its capability area and right with the x-capability marking in the API file. AccessCheckInterceptor, a Spring method interceptor, reads that marking before the handler runs and calls AccessCheck.check with the session, the area and the right. AccessCheckService unions the permission letters of all the session's roles for that area and tests the right needed; a dash for every role refuses every action in the area. A refusal is 403 with MSG-P4-002 naming the action, plus one refusal event with the area, the right and result REFUSED. Service identities such as SY-RULES go through the same check. Add a contract test that fails any operation with no declared area.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\08-ai-and-agents\recovery-workbench-ai-assisted-development-approach-v1.md:
  Line 85: | Users, roles and permissions | Roles, permission letters and scopes |

  Line 103: | Authority | Roles, permission letters, scope, and the approval level where a decision is approved | Authority |

  Line 134: Authority        Any signed-in user. No permission letter is checked before roles resolve.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\08-ai-and-agents\recovery-workbench-ai-assisted-development-approach-v3-pptx.md:
  Line 87: | Authority | Roles, permission letters, scope, and the approval level where a decision is approved | Authority |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\04-user-stories\recovery-workbench-user-stories-epic-1-v7.md:
  Line 11750: Audit findings record unsuitable user access to EFS and staff sending debtor data outside the bank. Today rights are set inside each system and cannot be shown for a past date. This story holds the permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned data, applies scope before permission on every request, and ends access at the next request when a person leaves. It meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and puts co
... truncated (5,437 chars total)
```

### Assistant - 2026-11-16 00:47 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me check the permission letters definition in the roles doc or FSD P4. Search "C = create" etc.

</details>

**Tool `grep`** - completed

```json
{"pattern": "\\bC\\b.*create|\\bR\\b.*read|\\bU\\b.*update|\\bA\\b.*approve|\\bD\\b.*delete", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\03 Requirements and specifications\\Recovery Workbench Functional Specifications by Module v5\\Recovery Workbench FSD P4 Access and administration v3.md", "limit": 30}
```

```text
Found 1 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v5\Recovery Workbench FSD P4 Access and administration v3.md:
  Line 609: | AC-EXC-P4-006-05 | A write-off for a related party goes to the Board | "DOA-2026.11" is in force | the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true | the lookup returns level L1 with reason "RELATED_PARTY" | RWB-E1-038 |

```

### Assistant - 2026-11-16 00:47 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me search the roles matrix for "R, C, U, D, A" definitions.

</details>

**Tool `grep`** - completed

```json
{"pattern": "Right.*Meaning|right.*meaning|CREATE, READ|Create, read|R = |C = |U = |A = ", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\03 Requirements and specifications", "limit": 30}
```

```text
No matches found
```

### Assistant - 2026-11-16 00:47 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me look at RWB E1 037 story for permission letter definitions.

</details>

**Tool `grep`** - completed

```json
{"pattern": "C, R, U|C R U|letters|Letter|approve|create|update|delete|read", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v6\\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md", "limit": 60}
```

```text
Found 60 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v6\RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md:
  Line 24: As a **product owner**, I want **the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned tables that every screen and API applies, with the identity number masked inside the ACE view and contact values masked at the API**, so that **a change of rights is a data load with an approver, a person sees only the cases in their scope, and personal data shows unmasked only to roles that need it**.

  Line 40: - Parameters `rwb.refload.approver.permission=RW-SECADM` and `rwb.refload.approver.masking_rule=RW-COMPLY` are in the parameter catalog (RWB-E1-042).

  Line 44: 1. Reference data administrator (RW-REFADM): prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls POST /admin/reference-loads with table "permission" and validFrom.

  Line 45: 2. Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.

  Line 46: 3. Security administrator (RW-SECADM): reviews the difference report against the version in force and calls POST /admin/reference-loads/{loadId}/approve.

  Line 47: 4. Workbench: checks that the approver holds the role the parameter names for the table and is not the person who loaded it; writes one decision log entry for the approval with decision code AC-VERS and no case; marks the version Approved with its valid from date.

  Line 48: 5. Workbench: from the valid from date, every new session resolves the new version (RWB-E1-022 keeps open sessions on their version), and the screens and endpoints of the new letters open with no deployment.

  Line 51: 8. Workbench (FieldMasker): for each field tagged as personal data, reads the masking rule in force for the session's roles. When no rule lets a role see the field in clear, the response is filled from the masked view column (`v_ace_customer.id_no_masked`, `v_ace_contact.contact_value_masked`) or the value is masked by the masker where the view holds no masked column. When a rule allows it, the response is filled from the cl
... truncated (10,042 chars total)
```

### Assistant - 2026-11-16 00:48 | opencode-go/deepseek-v4.1-flash | build

This folder is the specification set, not the running Workbench — but the target behaviour is clear. The "rules engine" is deliberately **not** a separate product or service. ADR-004 and the engineering standards forbid adding one. It is a decision-table evaluator inside the recovery module (`recovery.casewf.rules`). Code holds the behaviour; versioned database rows hold the choices.

Think of the rule tables as **the case state machine's transition table**: every move a case makes is one row.

## How it will be used

When an event arrives at a case — a load, a screen action, a partner result, a timer, or another module — the evaluator:

1. reads the route-set version the case is on (a case keeps the version it was decided under, **R-UNI-38**);
2. selects rows whose from-state matches, or `ANY_ACTIVE`, and whose event matches;
3. tests the conditions in row order; one row fires (hit policy Unique, enforced when the version is loaded);
4. writes the decision-log entry first, with the rule ID, version and inputs; if that write fails, nothing moves (**R-UNI-39**);
5. runs the action: changes state, queue and owner, sets tasks and timers, queues outbound work;
6. if no row matches, sends the case to the exception queue and logs the gap (**R-UNI-41**) — the rule set gets fixed, not guessed.

That covers the **448 rules in 10 route sets**: restructure, settlement, deed in lieu, guarantee claim, litigation, asset disposal, debt sale, write-off, deviations and universal rules. 252 carry a timer; 366 hand the next state to a person or partner. The same component also drives entry, exclusion, allocation, assignment and transfer. And if an AI agent is unavailable or times out, the Workbench falls back to the deterministic rule result (**R-UNI-32**).

## What a "rule" is

A row with: rule ID, route set, from-state, event, condition (a FEEL expression), action, to-state, owner, timer, test case ID, valid-from/to, and version.

The condition is the only expressive part. Everything else is a named choice — which is why most changes are data, not code.

## What changing one looks like

```openui-lang
root = Stack([flow, lanes])
flow = Steps([{title: "1. Raise the change", markdown: "Log a change request in the bank's request tool and keep its reference, for example CR-2026-0042."}, {title: "2. Prepare the row", markdown: "The center of excellence analyst edits the route-set workbook and gives the row a test case."}, {title: "3. Load the version", markdown: "A reference data administrator loads the file with a version label, a future valid-from date, an impact summary and a rollback plan."}, {title: "4. Validate and test", markdown: "Schema, overlap, unreachable row, default row and every test run. A dry run counts the open cases whose outcome would change."}, {title: "5. Approve", markdown: "Someone other than the author signs. A failed test or a missing checklist item blocks approval."}, {title: "6. Take effect and verify", markdown: "New decisions use it from the valid-from date. Cases already decided keep the version they were decided under."}, {title: "7. Roll back if wrong", markdown: "One call restores the previous version in one transaction, with a reason and a change-log entry."}], "column")
lanes = Table(["Change", "Where it lives", "How it changes"], [["Routing rule: state, event, condition, action, owner, timer", "rule_row, versioned", "Rule load, test harness, approval"], ["Threshold, limit, service level, queue, role, template, DoA", "Reference tables, versioned", "Reference data load, checks, approval"], ["New event, action, state or calculation", "Java code", "Story, review, release"]])
```

The third lane is the important limit: a rule change can move a threshold, route, owner or timer; it **cannot invent** a new event, action, state or calculation. That still needs a story and a release.

## Who does what

| Who | What they do |
|---|---|
| Center of excellence analyst (RW-COE) | Writes or edits rows and test cases; loads rule versions; asks for a rollback |
| Reference data administrator (RW-REFADM) | Prepares and loads files; records verification; may not approve |
| Risk and model risk officer (RW-RISK) | Approves rule versions |
| Internal audit (RW-AUDIT) | Reads and exports the change log |
| Process owner | Target design: business approval; Risk co-approves when a limit or threshold moves |

The maker cannot approve. Every load, approval and rollback lands in the change log, which audit can export as CSV.

## Now vs eventually

- **Epic 1, 30 November 2026:** no screen. The analyst fills the Excel template (Rows and Tests tabs), the loader calls `POST /admin/rule-versions`, validation runs, the harness tests every row, a dry run counts the open cases affected, and Risk approves. Five tables go first: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER.
- **Epic 8, 30 June 2027:** `SCR-39 Rules and parameters` in Administration — versions, load, approval and rollback in the UI. Same engine, same checks; the Excel/API path is the interim.
- **Later stage epics:** the 448 route-set rules load as each stage is built, not all at Epic 1.
- **Thresholds, service levels, queues, roles, templates and delegation limits:** reference tables (`SCR-40`), not rule rows. Same versioned-load and approval pattern, different lane.

So if someone wants a rule changed today: raise the CR, take it to the center of excellence analyst, let the reference data administrator load it, and get Risk to sign. Do not edit the database, and do not expect a code release for a threshold.

## Two wording gaps worth settling

- **Approval authority:** RWB-E1-029 and RWB-AD-012 give approval to `RW-RISK`; the Rules Engine Design says the process owner approves, with Risk added when a limit or threshold moves. The stories are the build-ready wording; agree the operating model before go-live.
- **Hit policy:** the design says FIRST in row order; the business rules and test harness say Unique. The loader refuses overlapping rows and the harness expects exactly one hit, so they behave the same in practice — but the documents should use one term.

Key sources: `05 Technical architecture\Recovery Workbench Rules Engine Design v2.docx`; `05 Technical architecture\Recovery Workbench Architecture Decision Records v2.md` (ADR-004); `04 User stories\...\RWB E1 029 Rule load validation and rollback v1.md`, `RWB TE 005 Rule table test harness v1.md` and `RWB E1 048 Rule change audit report v1.md`; `04 User stories\Recovery Workbench Administration Stories v3.md` (AD-011 to AD-013); and `02 Business architecture and process\Recovery Workbench Business Rules and Routing Logic v4.html` for the full 448-rule set.

<details><summary>Reasoning</summary>

Permission letters are C, R, U, D, A:
- C = create
- R = read
- U = update
- D = delete
- A = approve (probably)

So "Rules and parameters" area has R for many roles, C for RW-COE, A for RW-RISK. No U or D rows shown. But E1-029's rollback endpoint requires U, and the authority table says RW-COE calls rollback (CRUD). There may be a U grant not listed in E1-037's excerpt. Let me search the roles matrix for "Rules and parameters" rows in the main Users Roles and Permissions workbook? It's xlsx. Could read with Python openpyxl, but maybe not needed. The key point for the user: COE loads, Risk approves, audit reads. Rollback by COE/ref data admin. Don't get bogged down in U.

I'll phrase roles simply without letters, or with the letters where clear. Maybe avoid letters entirely to prevent inaccuracy. Use "load right", "approve right", "read right". That's cleaner for a business user. The table can say what they do, not the code.

Roles:
- COE analyst: authors and loads rule versions; reads results; can roll back.
- Reference data administrator: prepares/loads files (reference and sometimes rules); records verification; cannot approve.
- Risk and model risk officer: approves rule versions.
- Internal audit: reads/exports change log.
- Process owner: target design business sign-off; Risk added for limit/threshold moves.
- Everyone else: read-only via GET /admin/rule-versions, if they hold Rules and parameters R (which many roles do).

Actually, "everyone else" with R can list versions but not change. That's a nice point: many roles have read access; only COE and Risk can act.

Let me check if E1-029 rollback right is U and who holds it. The authority table says RW-COE "Loads versions and calls rollback (Rules and parameters CRUD)" — so COE presumably has C, R, U, D even though the matrix snippet only lists C. Maybe the matrix is abbreviated. I'll say COE can roll back. Fine.

Now, "eventually how are rules engine going to be used" could also mean "will it be used for AI decisions or just routing?" The answer: it's the deterministic decision layer; AI agents propose/classify but rules decide, and fallback to rules if the agent fails. That's a nice future-facing point. The AI stories: intake agent in shadow, deviation screening agent, extraction evaluation. R-UNI-32 says if the agent/model doesn't answer within timeout, fall back to the rule result. So yes: rules remain the safety net and the source of truth for state transitions. Include one line.

Let me also c

_[truncated]_

</details>
