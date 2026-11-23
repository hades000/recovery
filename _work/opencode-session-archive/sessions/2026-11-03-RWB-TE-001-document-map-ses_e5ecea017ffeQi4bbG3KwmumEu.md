# RWB-TE-001 document map

- **Session ID:** `ses_e5ecea017ffeQi4bbG3KwmumEu`
- **Created:** 2026-11-03 18:35  |  **Last activity:** 2026-11-04 22:51
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `build`
- **Tokens:** 404,232 in / 30,397 out / 57,636 reasoning
- **Messages:** 83

---

### User - 2026-11-03 18:35

Recovery Workbench Project Hub v14.html 

Refer this and find all the connec ted documents and tell me aboput RWB-TE-001 in detail

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

I'll start by finding the file and its connected documents.

**Tool `glob`** - completed

```json
{"pattern": "**/*.html"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Team Start Pack v2.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data\Recovery Workbench Entity Relationship Diagram v3.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Business Rules and Routing Logic v4.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Case and Workflow Model v5.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench API Specification v2.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Detailed Process Flows v4.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\07 Screens and experience\Recovery Workbench Screen Specifications v1.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\07 Screens and experience\Recovery Workbench Screen Prototype v1.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\07 Screens and experience\Recovery Workbench Design System and Component Library v1.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\02 Business architecture and process\Recovery Workbench Process Map v1.html
```

**Tool `glob`** - completed

```json
{"pattern": "**/*", "limit": 200}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Weekly Status Pack v2.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Team Start Pack v2.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Team Start Pack v2.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Stakeholder Map and Communication Plan v3.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Overview v4.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Overview v4.docx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Deck v3.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Executive Presentation CTO v3.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Executive Presentation CEO v2.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Document Index v11.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Document Control Sheet v10.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Workflow Engine Design v2.docx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3.zip
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD S9 Partner management v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD S8 Deviation handling v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Technical Specifica
... truncated (31,130 chars total)
```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

I found the hub and the RWB-TE-001 file. Let me read both.

<details><summary>Reasoning</summary>

Let me read the Project Hub HTML. It's likely a portal with links to documents. Let me read it.

Also, RWB-TE-001 story file exists: "Recovery Workbench User Stories Epic 1 Story Files v5\RWB TE 001 Recovery module folder and boundary test v1.md". Let me read both.

Let me check the file size first.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem \"12 Project communication\\Recovery Workbench Project Hub v14.html\" | Select-Object Name,Length; Get-ChildItem \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB TE 001 Recovery module folder and boundary test v1.md\" | Select-Object Name,Length"}
```

```text

Name                                                        Length
----                                                        ------
Recovery Workbench Project Hub v14.html                   27559584
RWB TE 001 Recovery module folder and boundary test v1.md    14989



```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

The hub is 27 MB (likely embedded assets). Let me extract its document registry and find TE-001 references.

<details><summary>Reasoning</summary>

The hub HTML is 27.5 MB — likely contains embedded data (maybe base64 images/docs). Let me search for the document catalog / links inside. I'll grep for "TE-001" and for hrefs / document registry patterns.

Let me first get a sense of the structure without reading 27MB. Use grep for key items.

</details>

**Tool `grep`** - completed

```json
{"pattern": "RWB-TE-001", "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "limit": 20}
```

```text
Found 4 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 903: "2": "The P4 handler writes nothing itself. It calls the method recordVersion on the published interface of this story, in package recovery.casewf.refdata.api, passing the file rows as a list of maps, the table code, the valid from date, the user ID of the caller as the author, and the load ID. Your work in build step 7 is to wire the handler to that interface and to map the exceptions it throws onto the error responses of section 12, for example 422 with MSG-P3-027 for a failed check. P4 reaches this module only through the interface and never reads reference_version or reference_row, which the boundary test RWB-TE-001 checks.",

  Line 1480: "RWB-TE-001": {

  Line 1501: "2": "The build generates this code, and nobody writes it by hand. Add the server generator to the build as a plugin and set it to produce Spring Boot 3 interfaces only, one interface per tag, with the output in <ACE base package>.recovery.generated.web for the interfaces and <ACE base package>.recovery.generated.model for the request and response classes. Interfaces only means the generator gives you method signatures and data classes, and your own controller implements them. The generated packages are listed in the module map as shared, so the boundary test from RWB-TE-001 allows other modules to use them. Generated code is never edited; a change goes into the specification file and the next build produces it again.",

  Line 1700:  "RWB-TE-001": {

```

**Tool `grep`** - completed

```json
{"pattern": "<title>|<h1|<h2", "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "limit": 30}
```

```text
Found 29 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 3: <title>Recovery Workbench project hub</title><style>

  Line 2494:   let h=`<h1>${esc(g.label)}${g.note?' — '+esc(g.note):''}</h1>

  Line 2507:       h+=`<h2>${esc(m)} <span class="chip">${byMod[m].length}</span></h2>`;

  Line 2514:       h+=`<h2>Also releasing in ${esc(g.label)} <span class="chip">${also.length}</span></h2>

  Line 2565:   const out=[`<div class="stop"><span class="sk">${esc(st.k||'')}</span><h1 style="margin:0">${esc(st.t||s.h)}</h1></div>

  Line 2584:     out.push(`<h2>Everything this story refers to</h2>

  Line 2989:   b.innerHTML=`<h1>${esc(f)}</h1>

  Line 3000:   b.innerHTML=`<h1>${esc(d.name)} <span class="ext">${esc(d.ext.toUpperCase())}</span></h1>

  Line 3023:     `<h1>${esc(kind?M.kinds[kind]:'Every code in the set')}</h1>

  Line 3036:    <h1>Recovery Workbench, for the squads</h1>

  Line 3038:    <h2>Start from a story</h2>

  Line 3041:    <h2>A code opens where you are standing</h2>

  Line 3045:    <h2>Click any underlined word, not just the codes</h2>

  Line 3061:    <h2>Flow steps carry an explanation</h2>

  Line 3065:    <h2>What the codes mean</h2>

  Line 3070:    <h2>The rest of the tabs</h2>

  Line 3082:   document.querySelector('.body').innerHTML=`<h1>The eight epics</h1>

  Line 3092:     EPICS.filter(x=>x.gets).map(x=>`<h2>${esc(x.e)} ${esc(x.theme)}</h2><p>${link(x.gets)}</p>`).join('');

  Line 3153:   const head=`<h1>Decisions</h1>

  Line 3167:     b.innerHTML=head+`<h2>Decisions already taken <span class="chip">${DEC.taken.length}</span></h2>

  Line 3180:     b.innerHTML=head+names.map(nm=>`<h2>${esc(nm)} <span class="chip">${g[nm].length}</span></h2>`

  Line 3193:     b.innerHTML=head+`<h2>${esc(title)} <span class="chip">${rows.length}</span></h2>`+

  Line 3221:   b.innerHTML=`<h1>Terms</h1>

  Line 3226:     <h2>Words and build terms <span class="chip">${TERMS.terms.filter(hit).length}</span></h2>

  Line 3229:     <h2>Code prefixes <span class="chip">${TERMS.prefixes.filter(hit).length}</span></h2>

  Line 3265:   b.innerHTML=`<h1>${esc(q)}</h1><p class="lede">${docHits.length?docHits.length+' documents, ':''}${hits.length}${hits.length>=300?'+':''} sections${codes.length?', '+codes.length+' codes':''}</p>`+

  Line 3266:     (docHits.length?`<h2>Documents</h2>`+docHits.map(([d,i])=>

  Line 3268:     (hits.length?`<h2>Inside the docum
... truncated (2,646 chars total)
```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The hub is a self-contained app with embedded JSON data (a giant JS object). Line 1480 and 1700 have RWB-TE-001. Let me inspect lines 1400-1900. But careful: reading the whole file is 27MB. Let me read targeted ranges.

Let's look at line 1470-1520 and 1690-1720.

</details>

**Tool `read`** - completed

```json
{"path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "offset": 1460, "limit": 60}
```

```text
Read file 12 Project communication\Recovery Workbench Project Hub v14.html, lines 1460-1519
1460: "4": "A person reads here, and the work is in the component. Build GeneratedDocumentReview on SCR-30 Case documents: the PDF of the draft on one side and the list of merge values on the other. Each merge field is marked overridable or locked in the merge field catalog, and a locked one is shown read only. Amounts, parties, title numbers and the treatment terms are locked, and the dates of signing and the witness details are overridable. Show the fields read only for a team manager as well, who holds Documents R. Reading the catalog flag in the component keeps the officer from attempting a change that the endpoint would refuse.",
1461: "5": "The officer does this in the review component, which calls POST /documents/{documentId}/regenerate. You build that endpoint, which is new and recorded in the additions file. The request is RegenerateRequest: between one and ten overrides, each holding the merge field, the new value and a reason, plus the version of the document the officer read. An empty reason is refused with 422 and MSG-GEN-001 naming Reason, and a change to a field that the catalog locks is refused with 422 and MSG-P5-014 naming the field. A document already in state SENT is refused with 409 and MSG-P5-002. The second of two officers saving against the same version gets 409 with MSG-GEN-004.",
1462: "6": "The Workbench does all of this in DocumentSetService, in an order you have to keep. Write the decision log entry first, through DecisionLogWriter, carrying the decision code, the old value, the new value and the reason as override_reason. Then call DocumentGenerator.generate with the overrides and store the result as the next doc_version, leaving the earlier version readable. A failed decision log write stops the whole action with 503 and MSG-P7-003, with the document left at its doc_version and no file added. A correction on a REVIEWED document moves it back to DRAFT at the new doc_version, so the officer has to review it again.",
1463: "7": "The officer does this for each draft, and the Workbench records it. The call is POST /api/recovery/v1/documents/{documentId}/review with action COMPLETE, the endpoint that RWB-E1-054 adds. Extend it for generated drafts so that it sets the document state to REVIEWED and review_status to CONFIRMED where nothing was corrected or CORRECTED where something was. Every document of the set has to reach REVIEWED before th
... truncated (32,343 chars total)
```

**Tool `read`** - completed

```json
{"path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "offset": 1680, "limit": 60}
```

```text
Read file 12 Project communication\Recovery Workbench Project Hub v14.html, lines 1680-1739
1680:    "AC10": "This checks the version label. A label already loaded for a table cannot be loaded again. The second attempt is refused. The label here is test data. Each label has to point at one set of rows. The decision log on a case names the label it was decided under. If two different files could carry one label, nobody could say which rows applied to a case. The change log would also hold two loads with the same name.",
1681:    "AC11": "This checks the start date. The analyst loads a version with a start date that has already passed. The load is refused with a message about that date. The dates here are test values. A date in the past would mean the new rows applied to decisions already made under the old rows. Cases decided yesterday could then no longer be explained. A version starts today or later. That keeps every past decision tied to the rows that were in force at the time.",
1682:    "AC12": "This checks a template with no rows in it. The load is refused and the message names the missing rows. An empty file usually means the wrong sheet, the wrong file, or an export that failed. Accepting it would store a version with nothing in it. On its start date, every engine reading that table would find no rows and stop. Catching it at load time costs one message, and the analyst can send the right file straight away."
1683:   }
1684:  },
1685:  "RWB-E1-043": {
1686:   "story": "The values that drive allocation, timers and approval limits live in team spreadsheets and procedure documents today. So nobody can say which value applied to a case on a given day. The team builds the reference data service. Each load of a reference table creates a numbered version with a start date, an author and a different approver. The service gives the engines the approved version that was in force on the business date. Each engine writes one log line naming the table and version it read. It works when a load, an approval and a dated change all hold for the 13 tables.",
1687:   "ac": {
1688:    "AC1": "This checks that two versions of one table can live side by side and that each business date gets the right one. An approved version 3 already exists with four rows. A new load adds a fifth row and is approved. That creates version 4 and closes version 3 on the day before version 4 starts. The service then answers with version 3 for the earlier date and version 4 for the later one
... truncated (22,243 chars total)
```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The hub has a story detail structure. I need to understand the hub's data model and "connected documents". Let me look at the JS structure around line 900 (story data) and the constants near 1700. Also need to find the document index and how the hub links stories to documents (e.g., "Everything this story refers to").

Let me inspect the top of the JS data: search for "const STORIES", "const DOCS", etc.

</details>

**Tool `grep`** - completed

```json
{"limit": 60, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "pattern": "^(const|let|var) [A-Z_]+ ?="}
```

```text
Found 23 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 375: const RES={"tables":{"recovery_case":{"comment":"Recovery case: One recovery case per customer per product, from 90 days past due to close.","cols":[{"n":"id","t":"uuid PRIMARY KEY DEFAULT gen_random_uuid()","c":"Record identifier of the case"},{"n":"case_no","t":"varchar(18) NOT NULL","c":"Case number RW-YYYY-NNNNNN, issued at creation and never reused"},{"n":"product_group","t":"varchar(15) NOT NULL","c":"Mortgage, hire purchase, SSME or unsecured"},{"n":"primary_customer_id","t":"uuid NOT NULL","c":"The borrower the case is opened for"},{"n":"status","t":"varchar(20) NOT NULL DEFAULT 'NEW'","c":"Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed"},{"n":"stage_code","t":"varchar(20)","c":"The stage the case is on"},{"n":"route_state","t":"varchar(60)","c":"The routing state from the rule set, for example FIRM_INSTRUCTED"},{"n":"route_code","t":"varchar(4)","c":"The approved route R1 to R8"},{"n":"owner_user_id","t":"uuid","c":"The case owner"},{"n":"queue_id","t":"uuid","c":"The queue the case is in"},{"n":"team_code","t":"varchar(20)","c":"The owning team, used by scope rules"},{"n":"region_code","t":"varchar(10)","c":"The owning region, used by scope rules"},{"n":"entry_date","t":"date NOT NULL","c":"The date the case entered recovery"},{"n":"dpd_at_entry","t":"integer NOT NULL","c":"Days past due on the entry date"},{"n":"exposure_band","t":"varchar(10)","c":"Exposure band set from the outstanding balance at entry"},{"n":"total_outstanding_at_entry","t":"numeric(18,2) NOT NULL","c":"Total outstanding across linked accounts at entry, in baht"},{"n":"prescription_date","t":"date","c":"The earliest date a legal claim on the case expires"},{"n":"stage_clock_start","t":"timestamptz","c":"When the current state started, for the service level"},{"n":"deviation_open","t":"boolean NOT NULL DEFAULT false","c":"True while any deviation X1 to X7 is open"},{"n":"legal_hold","t":"boolean NOT NULL DEFAULT false","c":"...
  Line 376: const NOTES={

  Line 1614: const TERMS={"terms":[{"en":"account","th":"บัญชี","k":"noun","n":"The loan or facility account."},{"en":"acts","th":"ดำเนินการ","k":"verb","n":"Takes the action."},{"en":"administrator","th":"ผู้ดูแลระบบ","k":"noun","n":"The person who administers the Workbench."},{"en":"after","th":"หลังจาก"
... truncated (8,482 chars total)
```

**Tool `read`** - completed

```json
{"limit": 40, "offset": 880, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html"}
```

```text
Read file 12 Project communication\Recovery Workbench Project Hub v14.html, lines 880-919
880: "3": "The job asks P1 for the accounts that qualify instead of querying the account tables itself. Call RecoveryDataQuery.accountsAtOrAbove with the threshold and the business date. The call returns AccountEntrySnapshot records holding the account ID, the primary party ID, the product group, the region code, days past due, the total balance, the data as of date and the flags for restructuring, dispute, deceased, bankruptcy and fraud. Accounts already sitting on an open case are left out, which means no open case_account link for that account. An account at 89 days past due is not returned and comes back into view the next day once the load moves it to 90 (AC7).",
881: "4": "EntryRuleEvaluator runs inside the job as the service identity SY-RULES, with no person involved. It reads the exclusion rows, which are rule rows with rule table EXCLUSION, through RuleTableReader in P4, and applies them to each account snapshot. The five reason codes are DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN and OPEN_DISPUTE. When a row matches, the account gets no case, and you write one case_entry_exclusion row holding the account ID, the business date, the reason code, the rule ID and the rule version, for example ACTIVE_PLAN with version EXCL-2026.11 in AC2. The unique key on account_id and business_date keeps a repeated run from writing a second exclusion row.",
882: "5": "CaseGrouping takes the accounts that passed the entry rule and groups them by primary customer and product group. One group becomes one case, so a customer with two hire purchase accounts at 95 days past due receives a single case with both accounts linked (AC3), and a customer with a mortgage and a hire purchase account receives two cases (AC12). Before creating anything the service looks for an open case for the same customer and product group through CaseRecordService.findOpenCase and links the new account to it. The partial unique index ux_case_open_customer_product enforces this in the database. A partial index applies only to the rows matching its WHERE clause, here the cases with no closed date.",
883: "6": "CaseNumberIssuer produces the case number. It draws the next value from the yearly database sequence case_no_seq_YYYY and formats it as RW, the entry year and six digits, for example RW-2026-000123. A sequence is a database object that hands out each number once, which is what keeps a number from being u
... truncated (21,893 chars total)
```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now I need to understand the data model of the hub — specifically how stories map to documents. The "Everything this story refers to" section at line 2584. Let me read around 2338-2700 to understand how documents are derived, and also find the DOCS registry (documents list). Maybe the hub contains all document text inline, with doc metadata.

Let me look for "DOC" or "FILES" definitions. Search for "const M=" or "DOCS".

</details>

**Tool `grep`** - completed

```json
{"limit": 50, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "pattern": "const (M|DOCS|FILES|SET|STEPS|SIMPLE|NOTES|RES)\\s*="}
```

```text
Found 3 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 375: const RES={"tables":{"recovery_case":{"comment":"Recovery case: One recovery case per customer per product, from 90 days past due to close.","cols":[{"n":"id","t":"uuid PRIMARY KEY DEFAULT gen_random_uuid()","c":"Record identifier of the case"},{"n":"case_no","t":"varchar(18) NOT NULL","c":"Case number RW-YYYY-NNNNNN, issued at creation and never reused"},{"n":"product_group","t":"varchar(15) NOT NULL","c":"Mortgage, hire purchase, SSME or unsecured"},{"n":"primary_customer_id","t":"uuid NOT NULL","c":"The borrower the case is opened for"},{"n":"status","t":"varchar(20) NOT NULL DEFAULT 'NEW'","c":"Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed"},{"n":"stage_code","t":"varchar(20)","c":"The stage the case is on"},{"n":"route_state","t":"varchar(60)","c":"The routing state from the rule set, for example FIRM_INSTRUCTED"},{"n":"route_code","t":"varchar(4)","c":"The approved route R1 to R8"},{"n":"owner_user_id","t":"uuid","c":"The case owner"},{"n":"queue_id","t":"uuid","c":"The queue the case is in"},{"n":"team_code","t":"varchar(20)","c":"The owning team, used by scope rules"},{"n":"region_code","t":"varchar(10)","c":"The owning region, used by scope rules"},{"n":"entry_date","t":"date NOT NULL","c":"The date the case entered recovery"},{"n":"dpd_at_entry","t":"integer NOT NULL","c":"Days past due on the entry date"},{"n":"exposure_band","t":"varchar(10)","c":"Exposure band set from the outstanding balance at entry"},{"n":"total_outstanding_at_entry","t":"numeric(18,2) NOT NULL","c":"Total outstanding across linked accounts at entry, in baht"},{"n":"prescription_date","t":"date","c":"The earliest date a legal claim on the case expires"},{"n":"stage_clock_start","t":"timestamptz","c":"When the current state started, for the service level"},{"n":"deviation_open","t":"boolean NOT NULL DEFAULT false","c":"True while any deviation X1 to X7 is open"},{"n":"legal_hold","t":"boolean NOT NULL DEFAULT false","c":"...
  Line 376: const NOTES={

  Line 1616: const SIMPLE={

```

**Tool `read`** - completed

```json
{"limit": 120, "offset": 2330, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html"}
```

```text
Read file 12 Project communication\Recovery Workbench Project Hub v14.html, lines 2330-2449
2330:    "AC5": "This test checks the empty log. The log holds no entry, and the job runs. The result must be intact with zero entries checked. The last hash must be given as 64 zeros. Those zeros represent the point before the first entry. Early environments and new deployments start with an empty log, so the job meets this case on its first night. A job that failed or reported a break on an empty log would raise an incident on day one. It would also teach the team to ignore its reports.",
2331:    "AC6": "This test checks the wait for the decision log copy. The copy job for the business date is still running at 02:00 and ends at 02:25. The check must start at 02:25 and must record the copy job's end time. If the copy job has not ended by 04:00, the check must start anyway at 04:00 with a note saying so. Checking while the copy runs could read a moving range and report a break that is not there. Waiting without a limit would be worse, because some nights would get no check at all.",
2332:    "AC7": "This test checks a run with more than one changed entry. Two entries in the test database were changed. The first break must be the lower of the two sequence numbers, and the failing count must be 2. One incident and one message must go to Compliance, naming both entry IDs. Stopping at the first break would hide the size of the problem. Compliance would review one entry while a second stayed unknown. One report per run, rather than one per break, also keeps a widely changed log from flooding the group.",
2333:    "AC8": "This test checks entries written while the job runs. The log holds 48,210 entries when the job starts, and 37 more are appended during the run. The run must report 48,210 entries checked and that same number as its last sequence number. The next night's run must then check 48,247 entries. Fixing the end point at the start means the count and the last hash in the run record describe one known range. Without it, the job would chase new entries and its recorded last hash would not match any fixed point."
2334:   }
2335:  }
2336: };
2337: 
2338: let M=null, CUR={tab:null,d:null}, STORIES=[], EPICS=[], GROUPS=[], SEL=null, SIMPLEOPEN=true;
2339: let CURKEY='', NOTESOPEN=true, INFLOW=false;
2340: 
2341: async function boot(){
2342:   const raw=Uint8Array.from(atob(document.getElementById('payload').textContent.trim()),c=>c.charCodeAt(0));
2343:   const txt=aw
... truncated (8,676 chars total)
```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The data payload is gzipped base64. I can decode it to get the full model M with docs, ids, files. That's the cleanest path: extract the payload from the HTML, gunzip, parse JSON. Then I can enumerate docs connected to RWB-TE-001.

Let me first inspect the story rendering function openStory to understand what "Everything this story refers to" means, and how refs are computed. Read lines 2530-2700.

</details>

**Tool `read`** - completed

```json
{"limit": 180, "offset": 2530, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html"}
```

```text
Read file 12 Project communication\Recovery Workbench Project Hub v14.html, lines 2530-2709
2530: /* every code the story names, so the detail can sit on the page */
2531: const ORDER=['REQ','BR','VR','SC','AC','AC-ALT','AC-EXC','AC-BG','MSG','LOV','DF','FEAT','R-UNI','DQ','REC','CTL','INT','EV','JOB','SCR','NFR','ADR','RW','SY','TC','DL','DT','DEV','STORY'];
2532: function storyText(di,si){
2533:   const d=M.docs[di]; let t=d.secs[si].h+'\n'+d.secs[si].t;
2534:   const secs=[{h:d.secs[si].h,t:d.secs[si].t,i:si}];
2535:   for(let k=si+1;k<d.secs.length;k++){
2536:     if(/^RWB-[A-Z]{1,3}\d?-\d{3}\s/.test(d.secs[k].h.trim())) break;
2537:     t+='\n'+d.secs[k].h+'\n'+d.secs[k].t;
2538:     secs.push({h:d.secs[k].h,t:d.secs[k].t,i:k});
2539:   }
2540:   return {t:t, secs:secs};
2541: }
2542: function codesIn(text){
2543:   const by={}; const seen={};
2544:   (text.match(IDRX)||[]).forEach(c=>{
2545:     if(seen[c]||!M.ids[c]) return; seen[c]=1;
2546:     const k=M.ids[c].k; (by[k]=by[k]||[]).push(c);
2547:   });
2548:   return by;
2549: }
2550: const REFDOCS=['Physical Schema','Logical Data Model and Data Dictionary','Source to Target Mapping',
2551:   'API Specification','Error and Message Standard','Reference Data and Lists of Values',
2552:   'Entity Relationship Diagram','Engineering Practices'];
2553: function refDocRow(){
2554:   const out=[];
2555:   REFDOCS.forEach(n=>{
2556:     const i=M.docs.findIndex(d=>!d.inzip&&d.name.indexOf(n)>=0);
2557:     if(i>=0) out.push(`<span class="rx" data-k="doc" data-v="${i}">${esc(M.docs[i].name.replace(/^Recovery Workbench /,''))}</span>`);
2558:   });
2559:   return out.length?`<p class="cnt" style="margin:0 0 12px"><b>Documents you will need:</b> ${out.join(' &middot; ')}</p>`:'';
2560: }
2561: function openStory(di,si){
2562:   const d=M.docs[di], S=storyText(di,si), s=d.secs[si];
2563:   const st=STORIES.find(x=>x.d===di&&x.s===si)||{};
2564:   CURKEY=st.k||'';
2565:   const out=[`<div class="stop"><span class="sk">${esc(st.k||'')}</span><h1 style="margin:0">${esc(st.t||s.h)}</h1></div>
2566:     <p class="lede">${esc(st.mod||'')}${st.rel?' · '+esc(st.rel):''}${st.pri?' · '+esc(st.pri):''}${st.st?' · '+esc(st.st):''}
2567:       · from <span class="rx" data-k="doc" data-v="${M.docs.indexOf(d)}">${esc(d.name)}</span></p>`];
2568:   out.push(`<div class="nav">`+fileBtn(d)+
2569:     `<button class="dl" id="openall">Open every reference on this page</button>`+
2570:     (NOTES[st.k]?`<button class="dl" id="notet
... truncated (10,983 chars total)
```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. Now let me decode the payload to JSON and inspect: M.docs (names, folders, sections), M.ids["RWB-TE-001"], and find all docs that mention RWB-TE-001. That gives the connected documents.

Let me write a Node or Python script. Check what's available: node? python? Let's use PowerShell + .NET GZipStream, or node. Node likely available.

Plan: extract content of <script id="payload"> ... </script>, base64 decode, gunzip, JSON parse, dump summary to a JSON file. Then query.

Let me check the payload tag location.

</details>

**Tool `grep`** - completed

```json
{"limit": 10, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "pattern": "id=\"payload\"|</script>"}
```

```text
Found 10 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 216: <script type="application/octet-stream" id="payload">H4sIAG3S52oC/+y9e28cV5Yn+FUC9h9lA8lc8SHZltBYUCRlq5t6FElbXTMaEMHMIBmlzIisiEhRLElA2WXArurqmVm0bLfs2uqRDcPT9goou1xd8rfRR9nzvPfciMjMoFzdOwtMPyxmPM69cR/nnufv3H9pmA/Kly7+5/svHeajYVK8dPGlc69Fu4MiSbIyirNhlNybJEWaZIPkpd5Lh+kogUd2kkF+NylOo1t5cecA7h1H64NBUpbpQTpKq9Not4JX42IY3V3pQwv34NUsHp/1VXgruVfBS0IizX6ZTuAn/Fkm0u1j+L2XT+DS6KWLy72XqtY2bmdhI6U0cjvb3bgcbeSjUTKo0lw+Wd/vR28l2Z04erPIp5NetPJ6dGNQ5QdJEa2cW7lwO7taJePoQbSZVHE6up1t5oPpOMkquNTylfGMDryTFCW0DC8tA4m4SuCvRks3i2QSF8kwOjiF26ZX8AFVMR1U0wLfu7Wx/ma00l+JRsndZBStr7/0sMdDtNyP9o4Tvh6M1Va9m/D90FSVQduTvKjiUVTSaojGSVKVzSaY8DAp06MsKk9LHJNBPp7kGQxFSW9FaYUdH8D4Umfhcy9FSQytCem0jAbHyeAOfmBymMO3FMkoicuk7z5gpR/tTEdJGVXHcRXBYh3lJ9FhkY+BePBB60US4wzAwzIit7ONPKuKuMSZ2YMVFa31z0dVHi1H8VGcQqeARhkdxIM7RzCm2fBSNIqLoySq8FkckAG+n4/KaJVeCz65yu/gVqHvrI7hS2Ai+2v91R79s7yMrY/yAi7Dyq6mZVQe5ycZjocjfxAPj5JelMGIFjxQ+EI8giEUakDl75LTgxz3xYOI5yymgYSRgoGMD+BrkdS0pD+ByB15vhelWRRHo/woHcBk5gXs8l50klbHUZZHMCwTXHD95f5yj/5ZwX+g/7ezK7Ce8XPWo7spLFwguxJN7sHY4+UizY4iaD6hvsgAXZKb/CXH6XAIk3uQHKfQs7JKB3dOo+Mkhg6U1OZa/zVuDEdpD4e8isr0l/jRGyN4OqroGmzKKsLlUEUra/hp8F/oB1I433/9drYdHySj0o3LYZqMhtFxDK+5jo/wkahKYYHBBKbVJRi2X0xT3FH0OMxfXODyg7GiacFhX8UhWYV/Vm5nW0WRU6/lD+Rm/ukM/wOEK1gW3DzORTkdA1X4niF+AN6r8okO0Rj4Q6nv8JO4tVd9qzADb8FgwThjuzdgLchuqdJqlFyCXZrhZ0/LhAaVnoMO0QT7/uPwXsDRPcDNg7wDxz8aJKORfvSlqMSNjuMEK286Ji6YwUYYJNi7tEBuVSVKE7hUCmuTenXFfEuaydcM6TYNQZEAZwJ6sFAGo7yEXm+Vg3iS8C9dBfCle+kYFxRsEmSSOX7kOMmnVXQS4/vVSR7BA9MK3hEOgeRHuDiwSRiEAk6qKsmGRHMFu/mf8hzZ89u8JWAKVs6di+AwGyCP/iXeRBpwfXXlHC6ok3QImwJ3BjYMHdS9vCZ7+RyutexoGh/hYNzEf0b6u0xgUe0dxymvCFlOePtvgChO7DJP7DIuJ2EFY/hYeBnb2cthfZfCDrIMt4hOAq1ZmfvCbR/oDw7cZhEfHfHQXc+VJ2RJAkt66G/hTnkN19NoQmsA/sG1i0sPFnI0GcUw1243S1vY6RVcPOtTeDKD/RtXfFLtAuNbIgLAL4+Ooy1kr9HVTcdWBvlRllbpXeShxHZxQb/umPkqnKzAvtuPgICbb+A15OPH1KFbxzl1Jx/DgoQdNohhwR/Wu818YDIdjWibYw/o1AA+meFox/7Rm+kkGaWwt17ZuXV5aW9r6dzyuVcNsz2JR3eW9DMfRJd57e1e3YPVluKH/XQ9SjIY5SQpYFrtJPH3YPdwnMdw0EizpSfEDKOADsqBR19jhqXWwH/SVZvFwIdOZMku7Ne6kqP5wTGbwA8...
  Line 217: <script type="application/octet-stream" id="f0">H4sIAGvS52oA/8S6c5BmTbY3WrZt27Zto8u2bXTZtm122bZtu8t21e13JmbuvOd854t7/zpPxNp75Y61n1g787eYqSANDIICAAAAAeCBaKDzhwEAAvjnD/QPudk5GtMDAyj8j0LQ/xLSczSxdvpvojHgYqVsgAAAEn/+DOfvosZ2Ri42JrbOdO421nR/PalOmrAdIEAQ9Rsy1DtYrY+u5FhTSf5VPQ9PwOBbBkaTpjK1g85KXypVTfdjGvSKNwNQLZOeVSRXX8fOWRbNQY
... truncated (20,409 chars total)
```

**Tool `shell`** - completed

```json
{"command": "node --version; python --version"}
```

```text
v22.23.2
Python 3.11.9

```

### Assistant - 2026-11-03 18:35 | opencode-go/deepseek-v4.1-flash | build

The hub embeds a compressed data payload. Let me decode it and query the document graph precisely.

<details><summary>Reasoning</summary>

Node available. Let me write a script to extract payload, gunzip, parse, and dump M to a temp JSON. Then inspect.

I'll write it in the temp folder to avoid polluting the project? The instruction prefers C:\Users\SahilMore\AppData\Local\Temp\opencode. I'll write there.

Script:
- read html
- match /<script type="application\/octet-stream" id="payload">([\s\S]*?)<\/script>/
- base64 decode, gunzip (zlib.gunzipSync)
- JSON.parse
- write M.json
- print keys, docs count, etc.

Also, the raw docs content is embedded; maybe M.docs[].secs. The "connected documents" would be docs that reference RWB-TE-001 or that the story references (codes defined in docs). Let me compute:

1. The doc containing the story (source).
2. Docs where RWB-TE-001 is mentioned (u list in M.ids["RWB-TE-001"].u).
3. Docs referenced by the story's codes (e.g., each code M.ids[c].d[0]).
4. The story's "Documents you will need" standard ref docs.
5. Related files on disk (story file, build notes, technical enabler stories xlsx, engineering practices, module map maybe).
6. Other stories that reference RWB-TE-001 (e.g., RWB-E1-043, TE-003).

Let's do this systematically.

</details>

**Tool `write`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\extract_hub.js", "content": "const fs=require('fs'),zlib=require('zlib');\nconst p='C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14/12 Project communication/Recovery Workbench Project Hub v14.html';\nconst html=fs.readFileSync(p,'utf8');\nconst m=html.match(/<script type=\"application\\/octet-stream\" id=\"payload\">([\\s\\S]*?)<\\/script>/);\nif(!m){console.error('payload not found');process.exit(1);}\nconst raw=Buffer.from(m[1].trim(),'base64');\nconst txt=zlib.gunzipSync(raw).toString('utf8');\nconst M=JSON.parse(txt);\nfs.writeFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json',JSON.stringify(M));\nconsole.log('keys',Object.keys(M));\nconsole.log('docs',M.docs.length,'ids',Object.keys(M.ids).length,'files',Object.keys(M.files||{}).length);\nconsole.log('doc names sample',M.docs.slice(0,5).map(d=>d.name));\n"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/extract_hub.js
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\extract_hub.js\""}
```

```text
keys [ 'docs', 'ids', 'kinds', 'files', 'fmeta' ]
docs 192 ids 8726 files 157
doc names sample [
  'Recovery Workbench Accessibility Standard v2',
  'Recovery Workbench Content and Label Standard v2',
  'Recovery Workbench Customer and Partner Correspondence Templates v2',
  'Recovery Workbench Design System and Component Library v1',
  'Recovery Workbench Error and Message Standard v3'
]

```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now query the model.

Compute:
- The story's doc: find sec containing "RWB-TE-001" heading.
- M.ids["RWB-TE-001"] full entry (k, t, u locations).
- All docs mentioning "RWB-TE-001" in text.
- All codes in the TE-001 story text and where each is defined (docs).
- Also, the "documents you will need" list.

Let me write a query script that prints:
1. docs with sections whose heading starts with RWB-TE-001.
2. all occurrences of RWB-TE-001 across docs with section headings.
3. the set of codes in story text (story + following sections until next story heading), their kind and defining doc.
4. docs that are connected by those codes.
5. docs that mention "boundary" / "module map" etc. maybe.
6. M.files keys and fmeta maybe file paths for original files; probably relevant for "connected documents" list.

Also there may be a "story refs" table in the story file or hub. Let me inspect the story doc section html/markdown. The M.docs have secs with h and t. Find the doc and print the entire TE-001 section.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst KEY='RWB-TE-001';\n// 1. all sections whose heading starts with key\nconst homes=[];\nM.docs.forEach((d,di)=>d.secs.forEach((s,si)=>{\n  if(new RegExp('^'+KEY+'\\\\b').test(s.h.trim())) homes.push({di,si,doc:d.name,folder:d.folder,h:s.h,len:s.t.length});\n}));\nconsole.log('=== STORY HOME ==='); console.log(homes);\n// 2. all mentions\nconsole.log('\\n=== ALL DOCS MENTIONING '+KEY+' ===');\nM.docs.forEach((d,di)=>{\n  const hits=d.secs.filter(s=>(s.h+' '+s.t).includes(KEY));\n  if(hits.length) console.log(di, d.folder+' / '+d.name, '| sections:', hits.map(s=>s.h).join(' || '));\n});\n// 3. id entry\nconsole.log('\\n=== ID ENTRY ==='); console.log(JSON.stringify(M.ids[KEY],null,1).slice(0,3000));\n// 4. story text + refs\nconst home=homes[0];\nconst d=M.docs[home.di];\nlet story=d.secs[home.si].h+'\\n'+d.secs[home.si].t;\nfor(let k=home.si+1;k<d.secs.length;k++){\n  if(/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[k].h.trim())) break;\n  story+='\\n'+d.secs[k].h+'\\n'+d.secs[k].t;\n}\nconst IDRX=new RegExp('\\\\b(AC-ALT-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|AC-EXC-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|AC-BG-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|AC-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|BR-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|VR-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|SC-[A-Z0-9]{1,5}-\\\\d{2,3}|RWB-[A-Z]{1,3}\\\\d?-\\\\d{3}|REQ-[A-Z0-9
... truncated
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_hub.js
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_hub.js\""}
```

```text
=== STORY HOME ===
[
  {
    di: 75,
    si: 1,
    doc: 'Recovery Workbench Build Notes Technical Enablers v1',
    folder: '04 User stories',
    h: 'RWB-TE-001 Recovery module folder and boundary test',
    len: 22
  },
  {
    di: 80,
    si: 1,
    doc: 'Recovery Workbench Technical Enabler Stories v5',
    folder: '04 User stories',
    h: 'RWB-TE-001 Recovery module folder and boundary test',
    len: 410
  }
]

=== ALL DOCS MENTIONING RWB-TE-001 ===
73 04 User stories / Recovery Workbench Build Notes Epic 1 v4 | sections: Step 2
75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sections: RWB-TE-001 Recovery module folder and boundary test || Step 2
79 04 User stories / Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2 | sections: Tab Defects
80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sections: Recovery Workbench technical enabler stories || RWB-TE-001 Recovery module folder and boundary test || RWB-TE-002 Code owners for the recovery module || 3. Preconditions || 6. INVEST check || 13. Solution plan || 17. Guardrails || 19. Out of scope || RWB-TE-003 Types and contract tests from the API specification || 3. Preconditions || 6. INVEST check || RWB-TE-011 PDPA lint for code, tests and logs || 3. Preconditions || 6. INVEST check || RWB-TE-012 Document storage containers || 3. Preconditions || 6. INVEST check
81 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sections: Tab Stories || Tab Acceptance criteria || Tab Test cases || Tab Traceability || Tab Dependencies
82 04 User stories / Recovery Workbench User Stories Epic 1 v7 | sections: 13. Solution plan || 3. Preconditions
112 11 Delivery and operations / Recovery Workbench Build Sequence Epic 1 and Epic 2 v4 | sections: Tab Sequence
122 11 Delivery and operations / Recovery Workbench Story Build Order v1 | sections: Top
179 12 Project communication / Recovery Workbench Team Start Pack v2 | sections: Escalation
180 12 Project communication / Recovery Workbench Team Start Pack v2 | sections: Slide 10. The first month: build team
181 12 Project communication / Recovery Workbench Weekly Status Pack v2 | sections: Slide 4. Epic 1 build
185 09 Testing and quality / Recovery Workbench Regression Suite v5 | sections: Tab Suite
186 09 Testing and quality / Recovery Workbench Requirements Traceability Matrix v4 | sections: Tab RTM
187 09 Testing and quality / Recovery Workbench Test Cases v5 | sections: Tab Story test cases
... truncated (5,899 chars total)
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The "story home" is the Build Notes Technical Enablers (h only 22 chars) and the Technical Enabler Stories v5. The story detail will be in Technical Enabler Stories v5 sheet section, with subsections 1-19 covering story, AC, build steps, etc.

Let me read the full TE-001 story from the model — the sections from the story heading up to next story. Print it with section headings. Let me modify query or just read the extracted file.

The extracted story text is 6566 chars, seems short relative to hub detail which showed 8 build steps and story/AC. Actually 6566 includes the following sections until next story. Let's print it.

Also, I need to identify "connected documents" as documents connected to RWB-TE-001. Rather than all docs that define codes (which is 40), better to give:
- The primary source doc (Technical Enabler Stories v5)
- The per-story file (RWB TE 001 ... v1.md) - on disk in story files zip folder
- Build notes (TE build notes, Epic 1 build notes)
- The documents that govern it: Engineering Practices v4, API Specification v2, Technical Specifications by Module (module map/boundary), Target Architecture v4, TSD P4, etc.
- Test docs: Test Cases v5, Regression Suite v5, RTM v4
- Delivery docs: Build Sequence, Story Build Order, Story Defects, Team Start Pack, Weekly Status, etc.
- Neighbouring stories: TE-002, TE-003.

Let me use the hub's docs list and search for relevant context. The hub itself likely has "Everything this story refers to" which includes all codes in the story, but the story's code refs are only 5 kinds (INT-34, MSG-P4-002, TC-TE-001-08, RW-REFADM, and one STORY ref). Interesting: M.ids entry for RWB-TE-001 has empty t. The code refs list says only 1 TC. But the story text references ArchUnit, BND-1..5, API spec, etc. as plain text.

Let me print full story sections with headings and the exact section list. Then inspect the per-story file on disk (14,989 bytes) which may include more metadata (Epic, Module, etc.) and traceability links.

Also look at the Technical Enabler Stories v5 doc section headings around TE-001 (si 0.. maybe 50) to see table of contents fields. And check the "Tab Traceability" section in the xlsx-derived doc (di 81) for TE-001.

Let me print full story from build notes and technical enabler stories.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst di=80, start=1;\nconst d=M.docs[di];\nfor(let k=start;k<d.secs.length;k++){\n  const h=d.secs[k].h.trim();\n  if(k>start && /^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(h)) { console.log('\\n--- NEXT STORY:',h,'---'); break; }\n  console.log('\\n########## ['+k+'] '+d.secs[k].h+' ##########');\n  console.log(d.secs[k].t.slice(0,4000));\n}\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\print_te001.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/print_te001.js
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\print_te001.js\" > \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001_sections.txt\" 2>&1; Get-Content \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001_sections.txt\" -TotalCount 120"}
```

```text

########## [1] RWB-TE-001 Recovery module folder and boundary test ##########
| Item | Value |
|---|---|
| Story key | RWB-TE-001 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraint Modular monolith) and section 5.2 |
| L3 process | All recovery processes |
| Decision | DL05 |
| Priority | Must |
| Depends on | None |
| Status | Ready for build |

########## [2] 1. Story ##########
As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.

########## [3] 2. Business rationale ##########
Three teams build in one ACE service. Without a checked boundary, a change in one team's code breaks another's, and a direct call to a core system could bypass the COLLINS and file load path. The skeleton gives each Workbench module one package with a published part and an internal part, and a test in every build refuses a call into another module's internal part, a cross-module table read and a direct system call outside the integration adapters. It meets REQ-DRI-006 and applies DT08, ADR-002 and DL05 (option B from 2 November: TechX creates the recovery module in its own package). The measure is the count of boundary violations merged to main, which must stay at zero.

########## [4] 3. Preconditions ##########
- Access to the ACE repository for the TechX squads (DL36).
- DL05 is applied as option B from 2 November 2026: TechX creates the recovery module in its own package; the ACE team applies the module boundaries for the common and collection modules later.
- The common module's published packages are named in the module map. Until the ACE team names them, the map lists `..common.api..` (assumed; DL05).
- The ACE build runs the unit test phase on every pull request.

########## [5] 4. Flow ##########
1. Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
2. Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.
3. Squad member: writes RecoveryBoundaryTest with the rules BR1 to BR5, reading the module map.
4. Squad member: writes the front end
... truncated (8,354 chars total)
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Continue reading.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-Content \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001_sections.txt\" | Select-Object -Skip 120 -First 160"}
```

```text
None. This story does not change a case status. It changes the build result of a pull request from passed to failed when a rule is broken.

########## [11] 10. Authority ##########
| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Create the folders, the module map and the boundary test |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the module map or to the boundary rules |
| ACE team | Names the common and collection published packages (DL05) |
| RW-PLATADM, platform administrator | Runs the pipeline |
| No approval level from the delegation of authority applies | The story takes no business decision |

########## [12] 11. Data ##########
No business field is read or written. The boundary test reads source and compiled classes only.

Field IDs are those in the Logical Data Model and Data Dictionary.

########## [13] 12. Contract ##########
| Item | Value |
|---|---|
| Trigger | Every pull request build and every build of main |
| Back end check | RecoveryBoundaryTest, run in the unit test phase |
| Front end check | The dependency rules for `src/modules/recovery`, run in the front end lint step |
| Output | Pass, or fail with the rule code, the class or file and the dependency that broke it |
| Idempotency | The same commit always gives the same result |
| Restart | Rerun the pipeline; the check holds no state |

**Recovery side of the published access check**

```java
// Wired for /api/recovery/v1/**; calls the common module access check (published interface, INT-34)
void RecoveryAccessGuard.require(String capabilityArea, Right right, ScopeTarget target);
//   throws AccessDeniedException mapped to 403 Problem with messageCode MSG-P4-002
```

########## [14] 13. Solution plan ##########
**Package.** Back end folder `ace-service/src/main/java/<ACE base package>/recovery/`, with one package per module: `dataengine` (P1), `integration` (P2), `casewf` (P3), `access` (P4), `dochub` (P5), `comms` (P6), `decision` (P7), `payments` (P8), `reporting` (P9), `agent` (P10), `valuation` (S1), `treatment` (S2), `guarantee` (S3), `litigation` (S4), `asset` (S5), `debtsale` (S6), `writeoff` (S7), `deviation` (S8), `partner` (S9). Each holds `api` for its published interfaces and `internal` for the rest; a story that publishes from another package, for example `recovery.casewf.allocation` (RWB-E1-020) or `recovery.decision.writer` (RWB-E1-027), lists that package as publi
... truncated (7,288 chars total)
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Excellent. Now I have the full story. Note some inconsistencies between hub detail (older? different wording) and the story document: The hub's inline definitions say AC1 uses "recovery.casewf.internal.SampleService" and imports "collection.internal.CollectorRepository", while the story detail section 7 says that. The hub snippet (lines 1481-1488) has build steps numbered 1-8 but DETAIL has build steps 1-7. Interesting: the hub's "detail" (build notes) might be an older/different version. Actually lines 1480-1488 for RWB-TE-001 has 8 steps including module map, boundary test, frontend etc. The Technical Enabler Story v5 has 7 build steps and some different naming (BND-1 vs BR1). The hub's inline definition for RWB-TE-001 matched build notes? Let me check: line 1481 says create 19 modules, two child packages api/internal, package-info, front end folder. Story section 13 build step 1 same. Line 1482 module map. Line 1483 ArchUnit 5 rules BND-1..BND-5. Story section says "boundary rule BND-1 to BND-5" and BR1..BR6. So mostly aligned, but hub detail has 8 steps (adds RecoveryAccessGuard as step 5, pipeline step 6, failure step 7, fix step 8) while story has 7 build steps (build steps 6/7 combine guard/pipeline). Hmm.

Anyway, the user wants "find all the connected documents and tell me about RWB-TE-001 in detail."

I need to produce:
1. List of connected documents with folder paths.
2. Detailed explanation of RWB-TE-001.

Let me identify the precise connected documents by scanning the hub for TE-001 references and by mapping domains.

Let me get the doc list with folder, names, and docs that mention TE-001. Also docs connected through the story's requirement REQ-DRI-006, decision DL05, ADR-002, DT07/DT08, BRs, TCs.

Let me query:
- M.ids["REQ-DRI-006"], ["DL05"], ["ADR-002"], ["DT07"], ["DT08"], ["REQ-DRI-006"], ["TC-TE-001-01".."08"].
- Their locations/docs.
- Docs for TE-002, TE-003 (explicit out of scope links).
- The Build Notes Technical Enablers section Step 2 and Epic 1 Build Notes Step 2.
- Story Defects entry.
- Build Sequence / Story Build Order entries.
- Test Cases / Regression Suite / RTM tabs.
- Team Start Pack mentions.

Also check the physical file set: "Technical Enabler Stories v5.md/.xlsx", "Build Notes Technical Enablers v1.md", per-story file in zip? Wait, the story files zip for Epic 1 is "User Stories Epic 1 Story Files v5.zip" and there's an extracted folder "Recovery Workbench User Stories Epic 1 Story Files v5" containing "RWB TE 001 

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File | Where-Object { $_.FullName -match '04 User stories|05 Technical architecture|09 Testing|11 Delivery|12 Project' } | Select-Object @{n='Rel';e={$_.FullName.Replace((Get-Location).Path+'\\','')}},Length | Sort-Object Rel | Format-Table -AutoSize | Out-String -Width 300"}
```

```text

Rel                                                                                                                                                       Length
---                                                                                                                                                       ------
04 User stories\Recovery Workbench Acceptance Criteria Glossary v1.xlsx                                                                                    20731
04 User stories\Recovery Workbench Administration Stories v2.md                                                                                            64003
04 User stories\Recovery Workbench Administration Stories v2.xlsx                                                                                          18602
04 User stories\Recovery Workbench Build Notes Epic 1 v4.md                                                                                               486659
04 User stories\Recovery Workbench Build Notes Epic 2 v2.md                                                                                               250226
04 User stories\Recovery Workbench Build Notes Technical Enablers v1.md                                                                                    90034
04 User stories\Recovery Workbench Data Migration Stories v2.md                                                                                            41615
04 User stories\Recovery Workbench Data Migration Stories v2.xlsx                                                                                           7502
04 User stories\Recovery Workbench How To Read The Acceptance Criteria v1.docx                                                                             41731
04 User stories\Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx                                                                        16193
04 User stories\Recovery Workbench Technical Enabler Stories v5.md                                                                                        216974
04 User stories\Recovery Workbench Technical Enabler Stories v5.xlsx                                                                                       32884
04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5.zip                                                                                 539319
04 User stories\Recovery Workbench User Stories Epic 1 Story Files v
... truncated (29,816 chars total)
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now let me inspect the per-story file "RWB TE 001...v1.md" — likely a self-contained story pack with all sections plus references. Also read Build Notes Technical Enablers section around TE-001 and Epic 1 Build Notes Step 2 mention. And Story Defects entry. And Test Cases / RTM references.

Let me read the story file.

</details>

**Tool `read`** - completed

```json
{"path": "04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB TE 001 Recovery module folder and boundary test v1.md"}
```

```text
Read file 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB TE 001 Recovery module folder and boundary test v1.md, lines 1-253
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
39: 1. Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
40: 2. Squad
... truncated (16,296 chars total)
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now, build notes technical enablers for TE-001. Let me find that section in the .md or hub. Search in the build notes file.

</details>

**Tool `grep`** - completed

```json
{"limit": 20, "path": "04 User stories\\Recovery Workbench Build Notes Technical Enablers v1.md", "pattern": "RWB-TE-001"}
```

```text
Found 2 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Technical Enablers v1.md:
  Line 9: ## RWB-TE-001 Recovery module folder and boundary test

  Line 121: The build generates this code, and nobody writes it by hand. Add the server generator to the build as a plugin and set it to produce Spring Boot 3 interfaces only, one interface per tag, with the output in <ACE base package>.recovery.generated.web for the interfaces and <ACE base package>.recovery.generated.model for the request and response classes. Interfaces only means the generator gives you method signatures and data classes, and your own controller implements them. The generated packages are listed in the module map as shared, so the boundary test from RWB-TE-001 allows other modules to use them. Generated code is never edited; a change goes into the specification file and the next build produces it again.

```

**Tool `grep`** - completed

```json
{"limit": 20, "path": "04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md", "pattern": "RWB-TE-001"}
```

```text
Found 1 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md:
  Line 2419: The P4 handler writes nothing itself. It calls the method recordVersion on the published interface of this story, in package recovery.casewf.refdata.api, passing the file rows as a list of maps, the table code, the valid from date, the user ID of the caller as the author, and the load ID. Your work in build step 7 is to wire the handler to that interface and to map the exceptions it throws onto the error responses of section 12, for example 422 with MSG-P3-027 for a failed check. P4 reaches this module only through the interface and never reads reference_version or reference_row, which the boundary test RWB-TE-001 checks.

```

**Tool `grep`** - completed

```json
{"limit": 20, "path": "05 Technical architecture\\Recovery Workbench Architecture Decision Records v1.md", "pattern": "ADR-002|ADR-005|ADR-006"}
```

```text
Found 7 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\05 Technical architecture\Recovery Workbench Architecture Decision Records v1.md:
  Line 10: | ADR-002 | Structure ACE as a modular monolith with common, collection and recovery modules | Accepted | 27 October 2026 |

  Line 13: | ADR-005 | Take data through COLLINS and file loads, and call no system of record directly | Accepted | 27 October 2026 |

  Line 14: | ADR-006 | One ACE front end with a recovery module folder | Proposed | 28 October 2026 |

  Line 54: - Bad: recovery takes ACE's data position: end of day data through COLLINS, with no real-time feed today (ADR-005).

  Line 58: ## ADR-002 Structure ACE as a modular monolith

  Line 164: ## ADR-005 Take data through COLLINS and file loads

  Line 198: ## ADR-006 One ACE front end with a recovery module folder

```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Read Build Notes Technical Enablers lines 1-120 (the TE-001 notes).

</details>

**Tool `read`** - completed

```json
{"limit": 120, "path": "04 User stories\\Recovery Workbench Build Notes Technical Enablers v1.md"}
```

```text
Read file 04 User stories\Recovery Workbench Build Notes Technical Enablers v1.md, lines 1-120
1: # Recovery Workbench build notes, the technical enablers
2: 
3: SCB Collections and Recovery. Henka Group.
4: 
5: (C) Siam Commercial Bank and Henka Pte Ltd
6: 
7: Every flow step of every story in the technical enablers, written out in full so it can be followed without knowing the Workbench already. Each entry gives the step as the story states it, then what it means: who acts, what runs on its own, and what has to be built. The story remains the specification. Where the two differ, the story governs.
8: 
9: ## RWB-TE-001 Recovery module folder and boundary test
10: 
11: Module: P2 Integration
12: 
13: ### Step 1
14: 
15: **In the story.** Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
16: 
17: A developer does this by hand, once. Create the back end folder ace-service/src/main/java/<ACE base package>/recovery/ and inside it one package for each of the 19 Workbench modules: dataengine, integration, casewf, access, dochub, comms, decision, payments, reporting and agent for P1 to P10, then valuation, treatment, guarantee, litigation, asset, debtsale, writeoff, deviation and partner for S1 to S9. Each module package holds two child packages. The api package holds the interfaces that other modules are allowed to call. The internal package holds the rest, which only that module may use. Add a package-info file to each one, and create the front end folder src/modules/recovery as well. Every later recovery story places its code inside these folders.
18: 
19: ### Step 2
20: 
21: **In the story.** Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.
22: 
23: You write one file by hand at architecture/recovery-modules.yaml. For each of the 19 modules it gives the module code, its Java package, the packages that count as published, and the client libraries that module is allowed to use. A published package is one that other modules may import. The api package is published for every module, and a story that publishes from a different package, for example recovery.casewf.allocation or recovery.decision.writer, lists that package here too. The boundary test reads this file rather than holding module names in test code, so adding or renaming a module is a change to the file. The TechX tech leads own 
... truncated (14,186 chars total)
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now let me find surrounding context in other docs. Query the model for specific ids and docs.

Let me gather:
- REQ-DRI-006 definition and all docs.
- DL05 full entry.
- ADR-002 relevant text (file).
- DT07/DT08 definitions (maybe "Delivery decisions"?).
- Test cases TC-TE-001-01..08 full entries.
- Requirements Traceability Matrix row.
- Build Sequence row.
- Story Build Order top.
- Story Defects entry.
- Regression Suite rows.
- Team Start Pack / Weekly Status mentions.
- Engineering Practices: module boundary guidance.
- Target Architecture / TSD P2 / API spec mention "recovery-modules.yaml" or modules.

Let me query M.ids for these and their locations.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction show(code){\n  const v=M.ids[code];\n  if(!v){console.log('\\n### '+code+' NOT FOUND');return;}\n  console.log('\\n### '+code+' ['+v.k+']');\n  console.log('text:',(v.t||'').slice(0,900));\n  console.log('defined:',M.docs[v.d[0]].name,'|',M.docs[v.d[0]].secs[v.d[1]].h);\n  console.log('also in:',v.u.map(([di,si])=>M.docs[di].name+' | '+M.docs[di].secs[si].h).slice(0,12).join('\\n          '));\n}\n['REQ-DRI-006','DL05','DL07','DL36','DT07','DT08','ADR-002','ADR-005','ADR-006','INT-34','MSG-P4-002','RW-REFADM','R-UNI-01'].forEach(show);\nconsole.log('\\n=== TC-TE-001 entries ===');\nfor(let i=1;i<=8;i++){\n  const c='TC-TE-001-0'+i; const v=M.ids[c];\n  if(!v){console.log(c,'missing');continue;}\n  console.log('\\n'+c+' -> '+(v.t||'').slice(0,500));\n  console.log('  defined in:',v.d.map(x=>M.docs[x[0]].name+' | '+M.docs[x[0]].secs[x[1]].h).join(' ; '));\n}\nconsole.log('\\n=== DOCS LIST (name | folder | sections) ===');\nM.docs.forEach((d,i)=>{ if(/Technical Enabler|Build Notes|Test Cases|Regression|Traceability|Build Sequence|Story Build Order|Story Defects|Engineering Practices|Target Architecture|API Specification|Interface Specifications|TSD P2|Architecture Decision|Project Hub|Document Index|Team Start|Weekly Status|Users Roles|Error and Message/.test(d.name)) console.log(i,'|',d.folder,'|',d.name,'|',d.secs.length);
... truncated
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_refs.js
```

### Assistant - 2026-11-03 18:36 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_refs.js\""}
```

```text

### REQ-DRI-006 [REQ]
text: No component calls a system of record directly. Data comes in through COLLINS or a file load, and leaves through paths ACE already has. — Must
defined: Recovery Workbench Business Requirements Epic 1 v3 | 4. Program requirements met in this epic
also in: Recovery Workbench Business Requirements Epic 1 v3 | 4. Program requirements met in this epic
          Recovery Workbench Business Requirements Program v3 | 5.2 P2 Integration
          Recovery Workbench FSD P2 Integration v2 | Requirements served
          Recovery Workbench Build Notes Epic 1 v4 | Step 3
          Recovery Workbench Technical Enabler Stories v5 | Recovery Workbench technical enabler stories
          Recovery Workbench Technical Enabler Stories v5 | RWB-TE-001 Recovery module folder and boundary test
          Recovery Workbench Technical Enabler Stories v5 | 2. Business rationale
          Recovery Workbench Technical Enabler Stories v5 | 8. Business rules
          Recovery Workbench Technical Enabler Stories v5 | 18. Traceability
          Recovery Workbench Technical Enabler Stories v5 | RWB-TE-002 Code owners for the recovery module
          Recovery Workbench Technical Enabler Stories v5 | 2. Business rationale
          Recovery Workbench Technical Enabler Stories v5 | 18. Traceability

### DL05 [DL]
text: Module skeleton — Does the bank create the Workbench module in ACE, or does TechX?  [Owner: K. Pipat; needed by 29 October 2026; recommended: B from 2 November, then A; blocks Engineering practices; technical enabler stories]
defined: Recovery Workbench Decision Log v8 | Tab Open decisions
also in: Recovery Workbench Decision Log v8 | Tab Open decisions
          Recovery Workbench Decision Log v8 | Tab By owner
          Recovery Workbench Lean BRD Epic 1 v2 | 6.1 Teams, systems and data
          Recovery Workbench Technical Enabler Stories v5 | RWB-TE-001 Recovery module folder and boundary test
          Recovery Workbench Technical Enabler Stories v5 | 2. Business rationale
          Recovery Workbench Technical Enabler Stories v5 | 3. Preconditions
          Recovery Workbench Technical Enabler Stories v5 | 10. Authority
          Recovery Workbench Technical Enabler Stories v5 | 13. Solution plan
          Recovery Workbench Technical Enabler Stories v5 | 19. Out of scope
          Recovery Workbench Technical Enabler Stories v5 | Tab Stories
          Recovery Workbench Dependency Map v2 | Tab Dependencies
          Recovery Workbench Engi
... truncated (16,779 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Error at v.d mapping; v.d might be [di,si] not array of arrays for test cases? Let's check. It printed v.d as x[0] undefined => maybe v.d = [80, 300]. Fix. Let me adjust script to handle.

Also the test case entry text is truncated but good. Let me query full TC entries with section details.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction loc(v){\n  if(!v||!v.d) return 'none';\n  if(typeof v.d[0]==='number') return M.docs[v.d[0]].name+' | '+M.docs[v.d[0]].secs[v.d[1]].h;\n  return v.d.map(x=>M.docs[x[0]]?M.docs[x[0]].name+' | '+M.docs[x[0]].secs[x[1]].h:JSON.stringify(x)).join(' ; ');\n}\nconsole.log('=== TC-TE-001 ===');\nfor(let i=1;i<=8;i++){\n  const c='TC-TE-001-0'+i; const v=M.ids[c];\n  console.log('\\n### '+c); console.log('text: '+(v.t||'')); console.log('loc: '+loc(v));\n  console.log('uses: '+(v.u||[]).map(([di,si])=>M.docs[di].name+' | '+M.docs[di].secs[si].h).slice(0,8).join('\\n      '));\n}\nconsole.log('\\n=== TC-TE-001 section text in Test Cases doc ===');\nconst TC=M.docs.findIndex(d=>/^Recovery Workbench Test Cases v5/.test(d.name));\nconsole.log('doc',TC,M.docs[TC].name,'secs',M.docs[TC].secs.length);\nM.docs[TC].secs.forEach((s,i)=>{if((s.h+' '+s.t).includes('TC-TE-001')) console.log('SEC',i,s.h,'len',s.t.length);});\n// print the relevant table rows\nM.docs[TC].secs.forEach((s,i)=>{\n if(s.h==='Tab Story test cases'){\n   const lines=s.t.split('\\n').filter(l=>l.includes('TE-001'));\n   console.log('\\n--- rows in',s.h,'---'); console.log(lines.join('\\n'));\n }\n});\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_tc.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_tc.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_tc.js\""}
```

```text
=== TC-TE-001 ===

### TC-TE-001-01
text: Boundary enforced — The module map lists modules P1 to P10 and S1 to S9 with their packages; The published packages are "<module>.api" and any other package the module map lists for each recovery module, and "..common.api.." for the common module; A class "recovery.casewf.internal.SampleService" that imports "collection.internal.CollectorRepository" — The pipeline runs — The boundary test fails the build; The build log names boundary rule BND-1, "SampleService" and "CollectorRepository"
loc: Recovery Workbench Technical Enabler Stories v5 | 16. Test cases
uses: Recovery Workbench Technical Enabler Stories v5 | 16. Test cases
      Recovery Workbench Technical Enabler Stories v5 | 18. Traceability
      Recovery Workbench Technical Enabler Stories v5 | Tab Test cases
      Recovery Workbench Regression Suite v5 | Tab Suite
      Recovery Workbench Test Cases v5 | Tab Story test cases

### TC-TE-001-02
text: Published interface allowed — The module map lists modules P1 to P10 and S1 to S9 with their packages; The published packages are "<module>.api" and any other package the module map lists for each recovery module, and "..common.api.." for the common module; A class "recovery.casewf.internal.SampleService" that calls an interface in "common.api" — The pipeline runs — The build passes
loc: Recovery Workbench Technical Enabler Stories v5 | 16. Test cases
uses: Recovery Workbench Technical Enabler Stories v5 | 16. Test cases
      Recovery Workbench Technical Enabler Stories v5 | Tab Test cases
      Recovery Workbench Requirements Traceability Matrix v4 | Tab RTM
      Recovery Workbench Test Cases v5 | Tab Story test cases

### TC-TE-001-03
text: Recovery modules meet only through their api package — The module map lists modules P1 to P10 and S1 to S9 with their packages; The published packages are "<module>.api" and any other package the module map lists for each recovery module, and "..common.api.." for the common module; A class in "recovery.integration.internal" that imports "recovery.decision.internal.DecisionLogRepository" — The pipeline runs; The class imports the published "recovery.decision.writer.DecisionLogWriter" instead — The build fails with boundary rule BND-3; The build passes
loc: Recovery Workbench Technical Enabler Stories v5 | 16. Test cases
uses: Recovery Workbench Technical Enabler Stories v5 | 16. Test cases
      Recovery Workbench Technical Enabler Stories v5 | Tab Test cases
      Recovery
... truncated (10,872 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Note TC-TE-001-01 and 08 marked "Yes" in last column — maybe "Smoke" or "Regression". Let's check header of that table for column meaning. Could be "Regression suite". Good detail.

Now let's inspect:
- RTM rows for TE-001
- Regression Suite rows
- Build Sequence row
- Story Build Order
- Story Defects
- Team Start Pack and Weekly Status references
- Engineering Practices section 2.1 and relevant boundary sections
- Target Architecture modular monolith
- TSD P2 module map/boundary
- API spec x-module / generated packages
- Interface spec INT-34
- Error standard MSG-P4-002
- Roles doc RW-REFADM
- Decision Log DL05
- BRD REQ-DRI-006

Let me query row texts from hub for those docs, and read key source files.

Write a script to print rows containing TE-001 or relevant id from specific docs/sections, plus section summaries.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction doc(nameRe){return M.docs.findIndex(d=>nameRe.test(d.name));}\nfunction rows(nameRe,needle){\n  const i=doc(nameRe); if(i<0){console.log('no doc',nameRe);return;}\n  console.log('\\n===== '+M.docs[i].name+' ('+i+') =====');\n  M.docs[i].secs.forEach((s,j)=>{\n    const hits=s.t.split('\\n').filter(l=>l.includes(needle));\n    if(hits.length){console.log('--- sec['+j+'] '+s.h+' ---'); console.log(hits.slice(0,12).join('\\n'));}\n  });\n}\nrows(/Requirements Traceability Matrix/,'RWB-TE-001');\nrows(/Regression Suite/,'TE-001');\nrows(/Build Sequence Epic 1/,'TE-001');\nrows(/Story Defects/,'TE-001');\nrows(/Team Start Pack/,'TE-001');\nrows(/Weekly Status Pack/,'TE-001');\nrows(/Story Build Order/,'TE-001');\nrows(/Dependency Map/,'TE-001');\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_rows.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_rows.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_rows.js\""}
```

```text

===== Recovery Workbench Requirements Traceability Matrix v4 (186) =====
--- sec[0] Tab RTM ---
REQ-DRI-006 | No component calls a system of record directly. Data comes in through COLLINS or a file load, and leaves through paths ACE already has. | Must | E1 | P2 | FEAT-DRI-09 | Run the file adapters for sources outside COLLINS | RWB-E1-007, RWB-TE-001, RWB-TE-002 | FSD P2 A2.4 | TSD P2 T8 | TC-E1-007-01, TC-E1-007-02, TC-E1-007-04, TC-TE-001-02, TC-TE-001-03, TC-TE-001-05, TC-TE-002-01 | As the story's acceptance criteria

===== Recovery Workbench Regression Suite v5 (185) =====
--- sec[0] Tab Suite ---
TC-TE-001-01 | RWB-TE-001 | E1 | P2 | AC1 | Boundary enforced | System | The boundary test fails the build; The build log names boundary rule BND-1, "SampleService" and "CollectorRepository" | Fixture importing a collection internal class | Yes
TC-TE-001-08 | RWB-TE-001 | E1 | P2 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged | RW-REFADM calls the test-only Case record R endpoint; refused with MSG-P4-002 | Yes

===== Recovery Workbench Build Sequence Epic 1 and Epic 2 v4 (112) =====
--- sec[0] Tab Sequence ---
2 | RWB-TE-001 | Recovery module folder and boundary test | P2 | Enabler | Must |  | Window 1 | 2 Nov to 13 Nov | E1
4 | RWB-TE-002 | Code owners for the recovery module | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
5 | RWB-TE-003 | Types and contract tests from the API specification | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
7 | RWB-TE-011 | PDPA lint for code, tests and logs | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
8 | RWB-TE-012 | Document storage containers | P5 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1

===== Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2 (79) =====
--- sec[0] Tab Defects ---
RWB-TE-001 | 3 | section 8 calls the boundary test rule codes R-BND, while the rules themselves are named BND-1 to BND-5 everywhere else in the story | Open

===== Recovery Workbench Team Start Pack v2 (179) =====
--- sec[8] Escalation ---
Issue Who resolves it By when Within a squad Tech lead Same day Between squads or with the ACE team Tech leads together; the ACE team decides if they do not agree Same day Needs a bank answer Decision owner, through the decision log Five working days Overdue decision or cross-unit issue Sponsor progress review Next revi
... truncated (6,853 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Great: Story Defects has an open defect: RWB-TE-001 | 3 | section 8 calls the boundary test rule codes R-BND, while the rules themselves are named BND-1 to BND-5 everywhere else in the story | Open.

Let me get full defect record with all columns.

Also Engineering Practices section 2.1 (one service three modules), modular monolith guidance, pipeline. Read from docx? The hub has extracted text, easier. Let me print relevant sections from M.docs where name "Engineering Practices".

Also Target Architecture, TSD P2, API spec sections mention recovery module/boundary. Let's search all docs for "recovery-modules|boundary test|ArchUnit|modular monolith" and list sections. That helps identify connected architecture docs.

Let me run a broad search.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst pats=[/modular monolith/i,/ArchUnit/i,/recovery-modules\\.yaml/i,/boundary test/i,/module map/i];\nconst out={};\nM.docs.forEach((d,di)=>d.secs.forEach((s,si)=>{\n  const txt=s.h+'\\n'+s.t;\n  pats.forEach(p=>{ if(p.test(txt)){ (out[d.folder+' / '+d.name]=out[d.folder+' / '+d.name]||[]).push(si+': '+s.h); }});\n}));\nObject.entries(out).forEach(([d,secs])=>{\n  console.log('\\n### '+d);\n  console.log([...new Set(secs)].slice(0,10).join('\\n'));\n});\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_arch.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_arch.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_arch.js\""}
```

```text

### 01 Decisions and governance / Recovery Workbench Decision Log v8
0: Tab Open decisions
1: Tab Decisions taken

### 03 Requirements and specifications / Recovery Workbench Business Requirements Program v3
37: 7. Constraints

### 03 Requirements and specifications / Recovery Workbench Lean BRD Epic 1 v2
16: 5.2 Systems and architecture

### 03 Requirements and specifications / Recovery Workbench Lean BRD Epic 2 v2
17: 5.2 Systems and architecture

### 04 User stories / Recovery Workbench Build Notes Epic 1 v4
416: Step 2

### 04 User stories / Recovery Workbench Build Notes Technical Enablers v1
1: RWB-TE-001 Recovery module folder and boundary test
3: Step 2
4: Step 3
8: Step 7
9: Step 8
11: Step 1
14: Step 4
20: Step 2
113: Step 2

### 04 User stories / Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2
0: Tab Defects

### 04 User stories / Recovery Workbench Technical Enabler Stories v5
0: Recovery Workbench technical enabler stories
1: RWB-TE-001 Recovery module folder and boundary test
2: 1. Story
4: 3. Preconditions
5: 4. Flow
6: 5. Exception paths
7: 6. INVEST check
8: 7. Acceptance criteria
9: 8. Business rules
11: 10. Authority

### 04 User stories / Recovery Workbench User Stories Epic 1 v7
134: 13. Solution plan
138: 17. Guardrails
189: 8. Business rules
474: 13. Solution plan
834: 13. Solution plan
844: 3. Preconditions
1134: 13. Solution plan

### 11 Delivery and operations / Recovery Workbench Build Sequence Epic 1 and Epic 2 v4
0: Tab Sequence

### 11 Delivery and operations / Recovery Workbench Dependency Map v2
0: Tab Dependencies

### 11 Delivery and operations / Recovery Workbench Engineering Practices v4
1: 1. The practices on one page
3: 2.1 One service, three modules
4: 2.2 Boundary rules
15: 10. Who owns each practice

### 11 Delivery and operations / Recovery Workbench Release Plan v3
7: Slide 8. Dependencies that set the dates

### 11 Delivery and operations / Recovery Workbench Risks Assumptions Issues and Dependencies v2
0: Tab Risks
3: Tab Dependencies

### 11 Delivery and operations / Recovery Workbench Story Build Order v1
0: Top

### 05 Technical architecture / Recovery Workbench ACE Architecture Decision v2
1: 1. The decision
8: 4. How the code is structured

### 05 Technical architecture / Recovery Workbench Architecture Decision Records v1
0: Recovery Workbench architecture decision records
7: ADR-002 Structure ACE as a modular monolith
10: Options considered
11: Decision
12: Consequences

### 05 Technical a
... truncated (3,455 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let's read Engineering Practices sections 1, 2.1, 2.2, 10; Target Architecture 5.1; ACE Architecture Decision 1 and 4; ADR-002; TSD P2 relevant (T8); API spec intro (module tags); Interface INT-34; Error MSG-P4-002; Roles RW-REFADM; DL05 full text; Business Requirements Program section 7 & 5.2.

Let me print these from the hub.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction find(nameRe){return M.docs.findIndex(d=>nameRe.test(d.name));}\nfunction pr(nameRe,secRe,max=3000){\n  const i=find(nameRe); if(i<0){console.log('MISSING',nameRe);return;}\n  console.log('\\n\\n################ '+M.docs[i].name+' ################');\n  M.docs[i].secs.forEach((s,j)=>{\n    if(secRe.test(s.h)){console.log('\\n---- ['+j+'] '+s.h+' ----');console.log(s.t.slice(0,max));}\n  });\n}\npr(/Engineering Practices/,/1\\. The practices|2\\.1|2\\.2|10\\. Who owns/,3500);\npr(/Target Architecture/,/5\\.1 The modular monolith/,3000);\npr(/ACE Architecture Decision/,/1\\. The decision|4\\. How the code/,3000);\npr(/Architecture Decision Records/,/ADR-002/,3000);\npr(/Decision Log/,/Tab Open decisions/,6000);\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_ctx.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_ctx.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_ctx.js\" > \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\ctx.txt\" 2>&1; Get-Content \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\ctx.txt\" -TotalCount 140"}
```

```text


################ Recovery Workbench Engineering Practices v4 ################

---- [1] 1. The practices on one page ----
Practice | Position | Status
Where code lives | One ACE service, one repository, one front end. Recovery code is in the recovery module. | Agreed
Structure | Modular monolith: common, collection and recovery modules by folder, with boundaries checked at build time. | Agreed
Workflow | Programmatic, in CMMN 1.1 terms. Conditions and actions are versioned data rows. No Temporal. | Agreed
Branching | Trunk based. Short-lived branches merged into main at least once a working day. | Agreed
Merge owner | Each squad merges into its own module through code owners. The ACE team owns the common module and the release decision. | Assumed, DL04
Code review | AI first-pass review, then one named human reviewer. A change in another module's folder needs that module's code owner. | Proposed
Tests | No untested code is merged. Tests are written from the acceptance criteria before the code. | Agreed
Feature flags | Every unfinished or cross-squad change is behind a flag. A flag that is off returns the previous code path. | Agreed
Pipeline gates | Nine checks before merge, deploy to DEV on merge, SIT on tag, UAT and production by the monthly release. | Proposed, Sprint 0
Release | One production release a month, shared with the collection squad: one week of SIT, one week of UAT, business testing during the build. | Agreed; dates DL34
Agreed: agreed by SCB IT, the ACE team, TechX and Henka. Proposed: the practice the squads use from 2 November unless the ACE team or SCB IT changes it. Assumed: the position used until the bank decides, with the decision log entry that holds the question.

---- [3] 2.1 One service, three modules ----
The Recovery Workbench is built inside the ACE service. There is one service, one repository and one front end. The service is split into modules by folder.
Module | Built by | Holds
Common | ACE team | The case view shared by both modules, sign-in and access checks, audit and PII logging, the shared entities (customer, account, product, collateral, asset) and shared tasks such as the TDR calculator
Collection | Collection squad | Phone, field, FCR and TDR work, as split under DL14
Recovery | The two TechX recovery squads | Recovery case stages, tasks and screens; litigation, debt sale, NPA and write-off; the document hub; the decision record; the recovery data products
A recovery component that the co
... truncated (13,764 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. Now TSD P2 T8, API spec doc, Interface spec INT-34, Error message, roles. Let me print.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction find(nameRe){return M.docs.findIndex(d=>nameRe.test(d.name));}\nfunction pr(nameRe,secRe,max=2500){\n  const i=find(nameRe); if(i<0){console.log('MISSING',nameRe);return;}\n  console.log('\\n\\n################ '+M.docs[i].name+' ('+i+') ################');\n  console.log('sections:',M.docs[i].secs.map((s,j)=>j+':'+s.h).join(' | ').slice(0,1500));\n  M.docs[i].secs.forEach((s,j)=>{\n    if(secRe.test(s.h)){console.log('\\n---- ['+j+'] '+s.h+' ----');console.log(s.t.slice(0,max));}\n  });\n}\npr(/TSD P2 Integration/,/T8|Integr/,3000);\npr(/API Specification v2/,/.*/,1800);\npr(/Interface Specifications/,/.*/,2200);\npr(/Error and Message Standard/,/4\\. The core messages/,2200);\npr(/Users Roles and Permissions/,/Tab Roles/,1800);\npr(/Business Requirements Program/,/7\\. Constraints|5\\.2 P2/,2500);\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_more.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_more.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_more.js\" > \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\more.txt\" 2>&1; Get-Content \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\more.txt\" -TotalCount 180"}
```

```text


################ Recovery Workbench TSD P2 Integration v2 (152) ################
sections: 0:Recovery Workbench P2 Integration | 1:Document control | 2:Existing capability check | 3:T1. Architecture overview | 4:T2. Component design | 5:T3. Data model | 6:T3.0 Standard record columns | 7:T3.1 Object and field definitions | 8:T3.2 Lists of values | 9:T3.3 Relationships | 10:T4. State machines and workflow | 11:T5. Integration and interfaces | 12:T5.1 External system interfaces | 13:T5.2 Cross-module interfaces | 14:T5.3 Events | 15:T6. Security and access control | 16:T6.1 RBAC matrix | 17:T6.2 Authentication and authorization | 18:T7. Non-functional requirements | 19:T8. Requirement traceability | 20:Appendix T-A. API specification | 21:T-A.1 Endpoint inventory | 22:T-A.2 Endpoint detail | 23:API-P2-001 GET /admin/outbound-items | 24:API-P2-002 POST /admin/outbound-items/{itemId}/resend | 25:API-P2-003 GET /admin/outbox/deliveries | 26:API-P2-004 POST /admin/outbox/deliveries/{deliveryId}/resend | 27:API-P2-005 GET /feature-flags | 28:API-P2-006 GET /admin/feature-flags | 29:API-P2-007 POST /admin/feature-flags | 30:API-P2-008 PATCH /admin/feature-flags/{flagKey} | 31:API-P2-009 GET /admin/scheduled-jobs | 32:API-P2-010 GET /cases/{caseId}/plan-status | 33:API-P2-011 GET /cases/{caseId}/customer-products | 34:API-P2-012 GET /treatments/{treatmentId}/credit-pack | 35:API-P2-013 POST /treatments/{treatmentId}/credit-result | 36:API-P2-014 POST /admin/interfaces/{interfaceCode}/manual-retirement | 37:Appendix T-B. Open technical decisions | 38:Document sign-off

---- [0] Recovery Workbench P2 Integration ----
Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

---- [11] T5. Integration and interfaces ----


---- [19] T8. Requirement traceability ----
| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-DRI-006 | FEAT-RDF-21 | RWB-E1-007 | TC-E1-007-01 |
| REQ-DRI-007 | FEAT-RDF-21 | RWB-E1-007 | TC-E1-007-01 |
| REQ-DRI-008 | FEAT-RDF-21 | RWB-E1-007 | TC-E1-007-01 |
| REQ-DRI-013 | None | Written one epic ahead | With the story |


################ Recovery Workbench API Specification v2 (128) ################
sections: 0:Top | 1:Recovery Workbench API specification | 2:Rules every endpoint follows

---- [0] Top ----
Recovery Workbench API specification SCB COLLECTIONS AND RECOVERY

---- [1] Recovery Workbench API specification ----
Henka 
... truncated (13,203 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Need INT-34 section and MSG-P4-002, roles. Let me query specifically.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction find(nameRe){return M.docs.findIndex(d=>d.name.match(nameRe));}\n// INT-34\nlet i=find(/Interface Specifications/);\nconsole.log('=== INT-34 ===');\nconsole.log(M.docs[i].secs[23].t.slice(0,2000));\n// MSG-P4-002 row\ni=find(/Error and Message Standard/);\nconsole.log('\\n=== MSG-P4-002 rows ===');\nM.docs[i].secs.forEach((s,j)=>{const l=s.t.split('\\n').filter(x=>x.includes('MSG-P4-002')); if(l.length){console.log('--',j,s.h,'--');console.log(l.join('\\n'));}});\n// RW-REFADM\ni=find(/Users Roles and Permissions/);\nconsole.log('\\n=== RW-REFADM ===');\nM.docs[i].secs.forEach((s,j)=>{const l=s.t.split('\\n').filter(x=>x.includes('RW-REFADM')); if(l.length){console.log('--',j,s.h,'--');console.log(l.slice(0,6).join('\\n'));}});\n// BRD section 7 constraints and 5.2\ni=find(/Business Requirements Program/);\nM.docs[i].secs.forEach((s,j)=>{ if(/7\\. Constraints/.test(s.h)){console.log('\\n=== BRD 7 Constraints ===\\n'+s.t.slice(0,2500));}\n if(/5\\.2/.test(s.h)){const l=s.t.split('\\n').filter(x=>x.includes('REQ-DRI-006')||/^##|^###/.test(x)); console.log('\\n=== BRD 5.2 extract ===\\n'+l.slice(0,20).join('\\n'));}});\n// Defect full row\ni=find(/Story Defects/);\nconsole.log('\\n=== Story Defects header+row ===');\nconsole.log(M.docs[i].secs[0].t.split('\\n').slice(0,4).join('\\n'));\nconsole.log(M.docs[i].secs[0].t.split(
... truncated
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_detail.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_detail.js\""}
```

```text
=== INT-34 ===
| Item | Specification |
|---|---|
| Purpose | Shared case view, entities, restructure calculator, notification path |
| Direction | Both |
| Approach | Published module interface |
| Trigger | Call or application event |
| Frequency | Per request |
| Volume | Per call |
| Error handling | Return the error to the calling module |
| Retry | As the caller decides |
| Owner of the fix | ACE team |
| Standard | Module interface |
| Decision | DL14 |

**Payload**

As published by the common module.

---

=== MSG-P4-002 rows ===
-- 4 4. The core messages --
MSG-P4-002 | Error | An action outside the role's permission | You cannot {action} here. Your role does not include it. | คุณไม่สามารถ{action}ได้ เนื่องจากบทบาทของคุณไม่มีสิทธิ์นี้

=== RW-REFADM ===
-- 0 Tab Roles --
RW-REFADM | Reference data administrator | Bank user | Center of excellence | Center of excellence | Maintains the versioned reference tables: queues, roles, templates, document checklists, action codes, product parameters | all | Reference data service, versioned tables | All | E1
-- 1 Tab Permissions --
RW-REFADM | Reference data administrator | Bank user | - | - | - | - | - | - | - | - | R | CRUD | R | - | R | -
-- 4 Tab Single sign-on --
RW-REFADM | Reference data administrator | Entra ID group | RWB-DEV-RW-REFADM | RWB-SIT-RW-REFADM | RWB-UAT-RW-REFADM | RWB-PROD-RW-REFADM
-- 5 Tab Systems by role --
RW-REFADM | Reference data administrator |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R

=== BRD 5.2 extract ===
REQ-DRI-006 | No component calls a system of record directly. Data comes in through COLLINS or a file load, and leaves through paths ACE already has. | Must | Solution architect | E1

=== BRD 7 Constraints ===
Constraint | What it means
Built on ACE | The Workbench is a module of ACE: one service, one repository, one front end
Modular monolith | Common, collection and recovery modules, with boundaries checked at build time
Programmatic workflow | Case, stage and task state held in the database and moved by code, in CMMN 1.1 terms. No Temporal
Principle 1 | Every rule, limit, threshold, template, name, queue, role, timer and route is a versioned data row, changed through a validated load without a code release
Data through COLLINS | Data from other systems arrives by the COLLINS daily batch or a file load. No real-time feed today
Document hub | The Workbench is the system of record for recovery documents
Monthly releases | One production release at each month end, sha
... truncated (3,215 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. Now, let me confirm the "connected documents" list. The user likely expects: documents linked from the hub page for RWB-TE-001, i.e. "Everything this story refers to" plus "Documents you will need". But they say "find all the connected documents" — could mean all docs in the project set that relate to TE-001. I'll give a structured list:

Tier 1 — Direct story sources:
- 04 User stories/Recovery Workbench Technical Enabler Stories v5.md / .xlsx — canonical TE-001 full story (section 1-19)
- 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB TE 001 Recovery module folder and boundary test v1.md — standalone story file
- 04 User stories/Recovery Workbench Build Notes Technical Enablers v1.md — step-by-step build notes (8 steps)
- 12 Project communication/Recovery Workbench Project Hub v14.html — hub with full text and code definitions

Tier 2 — Requirements, architecture and decisions it implements:
- 03 Requirements and specifications/Recovery Workbench Business Requirements Program v3.docx — section 7 and 5.2 (REQ-DRI-006)
- 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md — ADR-002, ADR-005, ADR-006
- 05 Technical architecture/Recovery Workbench ACE Architecture Decision v2.docx — modular monolith, code structure
- 05 Technical architecture/Recovery Workbench Target Architecture v4.docx — 5.1 modular monolith
- 11 Delivery and operations/Recovery Workbench Engineering Practices v4.docx — 2.1 one service three modules; 2.2 boundary rules
- 01 Decisions and governance/Recovery Workbench Decision Log v8.xlsx — DL05, DL07, DL36; DT07, DT08
- 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3/TSD P2 Integration v2.md — T8 traceability (REQ-DRI-006) and integration scope
- 05 Technical architecture/Recovery Workbench Interface Specifications v2.md/.xlsx — INT-34 common module access check
- 05 Technical architecture/Recovery Workbench API Specification v2.yaml/.html — /api/recovery/v1 contract, access/errors conventions
- 07 Screens and experience/Recovery Workbench Error and Message Standard v3.docx — MSG-P4-002
- 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v3.xlsx — RW-TRIBE, RW-REFADM rights.

Tier 3 — Test and delivery:
- 09 Testing and quality/Recovery Workbench Test Cases v5.xlsx — TC-TE-001-01..08
- 09 Testing and quality/Recovery Workbench Regression Suite v5.xlsx — 01 and 08 in regression
- 09 Testing and quality/Recovery

_[truncated]_

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction find(re){return M.docs.findIndex(d=>d.name.match(re));}\n// Build sequence header\nlet i=find(/Build Sequence Epic 1/);\nconsole.log('=== Build Sequence ===');\nconsole.log(M.docs[i].secs[0].t.split('\\n').slice(0,3).join('\\n'));\n// Story build order header\ni=find(/Story Build Order/);\nconsole.log('\\n=== Story Build Order ===');\nconsole.log(M.docs[i].secs[0].t.split('\\n').slice(0,4).join('\\n'));\n// Release plan mentions TE-001 / module folder / boundary\ni=find(/Release Plan v3/);\nconsole.log('\\n=== Release Plan mentions ===');\nM.docs[i].secs.forEach((s,j)=>{const l=s.t.split('\\n').filter(x=>/TE-001|module folder|boundary/i.test(x));if(l.length)console.log('--',j,s.h,'--\\n'+l.slice(0,6).join('\\n'));});\n// Document index\ni=find(/Document Index/);\nconsole.log('\\n=== Document Index ===');\nconsole.log(M.docs[i].secs.map(s=>s.h).join(' | '));\nM.docs[i].secs.forEach(s=>{ if(/Technical/.test(s.h)) console.log('\\n-- '+s.h+' --\\n'+s.t.slice(0,3000));});\n// Document control\ni=find(/Document Control Sheet/);\nconsole.log('\\n=== Document control rows for key docs ===');\nM.docs[i].secs.forEach(s=>{const l=s.t.split('\\n').filter(x=>/Technical Enabler|Build Notes|Engineering Practices|Test Cases|Regression|Traceability|Build Sequence|Story Build Order|Story Defects|Decision Log|Business Requirements Program|A
... truncated
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_docs.js
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_docs.js\""}
```

```text
=== Build Sequence ===
The order the Epic 1 and Epic 2 work is pulled
115 items. Delivery runs as Kanban (DT04): items are pulled in this order as capacity frees up. The two-week windows are the sponsor review points, not sprint boundaries.
Order | Key | Title | Module | Type | Priority | Depends on | Review window | Dates | Release | Critical path

=== Story Build Order ===
Recovery Workbench story build order
E2E Recovery Workbench. SCB Collections and Recovery. Henka Group, 30 October 2026.
The order the 115 items are built in, from Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx. The story numbers are a catalog, not an order: RWB-E1-001 depends on RWB-E1-043 and RWB-E1-044, which are built before it. Pull the next item whose dependencies are done. E is an enabler, S is a user story. Waits on names the items that must finish first, by their number within the same family.
Window 1, 2 to 13 November 2026

=== Release Plan mentions ===
-- 7 Slide 8. Dependencies that set the dates --
Recovery module folder, package and boundary test in the ACE repository | E1 | 2 Nov | ACE team (DL05) | The squads cannot merge into ACE

=== Document Index ===
Recovery Workbench document index | Decisions | Delivery | AI | Business | Data | Technical | Communication | Backlog | Quality | Requirements | Experience | Policy

-- Technical --
Read by: TechX squads, ACE team, solution architect.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 10 | Information flow | Where each piece of information comes from, how it reaches the Workbench, how often, and what happens when it does not arrive. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Information Flow v4.pptx |
| 14 | Target architecture, all eight epics | The architecture on ACE: modular monolith, one service, one repository, one front end, the case workflow layer, and what each epic adds. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Target Architecture v4.docx, Recovery Workbench Target Architecture v4.pptx |
| 20 | Architecture decision records | One page per decision taken: the workflow approach, the module structure, the front end split, the integration route. | MADR | Recovery Workbench Architecture Decision Records v1.md |
| 25 | System disposition and integration inventory | Every system recovery uses today, what happens to each and when, and every interface with its route, direction and frequency. | OpenAPI 3.1, AsyncAPI 3.0 | Recovery Workbench System Di
... truncated (8,614 chars total)
```

### Assistant - 2026-11-03 18:37 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Note interesting inconsistency: Document Control Sheet says 77 contradictions, while Story Defects doc says 116. Not necessary.

Need also component "Department"? Fine.

Let me check the "Technical Enabler Stories v5" doc's opening "Recovery Workbench technical enabler stories" table to get TE-001 point estimate maybe. Build Sequence doesn't show points? Header columns don't include points; Team Start Pack has points for E1 stories but not enablers.

Let me check the Technical Enabler Stories v5 "Tab Stories" row for TE-001 and "Tab Test cases"/"Tab Traceability".

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst i=M.docs.findIndex(d=>/^Recovery Workbench Technical Enabler Stories v5/.test(d.name));\nconsole.log('doc',i,'secs',M.docs[i].secs.length);\nM.docs[i].secs.forEach((s,j)=>{\n  if(j<3 || /Tab Stories|Tab Acceptance|Tab Test cases|Tab Traceability|Tab Dependencies/.test(s.h)){\n    console.log('\\n===== ['+j+'] '+s.h+' =====');\n    if(/Tab Stories|Tab Traceability|Tab Dependencies|Tab Acceptance/.test(s.h)){\n      const lines=s.t.split('\\n');\n      console.log(lines.slice(0,2).join('\\n'));\n      console.log(lines.filter(l=>l.includes('RWB-TE-001')).join('\\n'));\n    } else console.log(s.t.slice(0,1800));\n  }\n});\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_tesheet.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_tesheet.js
```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_tesheet.js\""}
```

```text
doc 80 secs 261

===== [0] Recovery Workbench technical enabler stories =====
SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Stories | 13 |
| Acceptance criteria | 112 |
| Test cases | 127 |
| Modules | P1 (1), P2 (7), P3 (2), P5 (1), P7 (1), P10 (1) |

Stories with no business user: interfaces, load frameworks and platform services the Epic 1 and Epic 2 stories build on.

Each story is written for build: the business rationale, preconditions, the main flow and its exception paths, acceptance criteria in Gherkin, business rules, state transitions, authority, the fields it reads and writes with their BR Field IDs, the contract, the solution plan, messages, screens, test cases and traceability to the business requirements. Field IDs are those in the Logical Data Model and Data Dictionary, endpoints those in the API Specification, messages those in the Error and Message Standard and requirement IDs those in the Business Requirements. The same stories are also supplied one file per story, to hand to a coding agent with the module specifications.

| Key | Title | Module | Requirements | Depends on |
|---|---|---|---|---|
| RWB-TE-001 | Recovery module folder and boundary test | P2 Integration | REQ-DRI-006 | None |
| RWB-TE-002 | Code owners for the recovery module | P2 Integration | REQ-DRI-006 | RWB-TE-001 |
| RWB-TE-003 | Types and contract tests from the API specification | P2 Integration | REQ-DRI-007, REQ-ACA-003 | RWB-TE-001 |
| RWB-TE-004 | Masked data in SIT and UAT | P1 Recovery data engine | REQ-RDF-010, REQ-ACA-005 | RWB-E1-065 |
| RWB-TE-005 | Rule table test harness | P3 Case and workflow | REQ-CWC-014, REQ-CWC-013 | RWB-E1-044 |
| RWB-TE-006 | Outbox and retry for outbound work | P2 Integration | REQ-DRI-007 | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| RW

===== [1] RWB-TE-001 Recovery module folder and boundary test =====
| Item | Value |
|---|---|
| Story key | RWB-TE-001 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraint Modular monolith) and section 5.2 |
| L3 process | All recovery processes |
| Decision | DL05 |
| Priority | Must |
| Depends on | None |
| Status | Ready for build |

===== [2] 1. Story =====
As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a bui
... truncated (2,638 chars total)
```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now confirm docs connected through "Everything this story refers to" in hub. The story text itself references only REQ-DRI-006, INT-34, MSG-P4-002, TC-TE-001-08, RW-REFADM. But the story's metadata references DL05; BRD, etc. The "Documents you will need" adds 8 standard reference docs: Physical Schema, Logical Data Model and Data Dictionary, Source to Target Mapping, API Specification, Error and Message Standard, Reference Data and Lists of Values, Entity Relationship Diagram, Engineering Practices.

Let me get exact list from the hub UI's refDocRow, which resolves names in M.docs. REFDOCS given. So for every story page, the "Documents you will need" list is those 8 docs. That's a hub-level connected set. Good to mention.

Let me check the actual doc names resolved (version numbers) so I can list them accurately:
- Physical Schema v4
- Logical Data Model and Data Dictionary v6
- Source to Target Mapping v3
- API Specification v2
- Error and Message Standard v3
- Reference Data and Lists of Values v3
- Entity Relationship Diagram v3
- Engineering Practices v4

Let me confirm the exact names.

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));['Physical Schema','Logical Data Model and Data Dictionary','Source to Target Mapping','API Specification','Error and Message Standard','Reference Data and Lists of Values','Entity Relationship Diagram','Engineering Practices'].forEach(n=>{const i=M.docs.findIndex(d=>!d.inzip&&d.name.indexOf(n)>=0);console.log(n,'=>',i>=0?M.docs[i].folder+' / '+M.docs[i].name:'MISSING');});\""}
```

```text
Physical Schema => 06 Data / Recovery Workbench Physical Schema v4
Logical Data Model and Data Dictionary => 06 Data / Recovery Workbench Logical Data Model and Data Dictionary v6
Source to Target Mapping => 06 Data / Recovery Workbench Source to Target Mapping v3
API Specification => 05 Technical architecture / Recovery Workbench API Specification v2
Error and Message Standard => 07 Screens and experience / Recovery Workbench Error and Message Standard v3
Reference Data and Lists of Values => 06 Data / Recovery Workbench Reference Data and Lists of Values v3
Entity Relationship Diagram => 06 Data / Recovery Workbench Entity Relationship Diagram v3
Engineering Practices => 11 Delivery and operations / Recovery Workbench Engineering Practices v4

```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Note for TE-001, most of these data docs are not actually relevant (no data changes) — the hub applies them generically. I should distinguish "hub's generic document row" vs "documents that materially govern TE-001". Good insight to add: despite the generic "documents you will need" list, TE-001 reads/writes no data, so Physical Schema/LDM/S2T/ERD/LOV are not actually needed; the meaningful ones are Engineering Practices, ADRs/Target Architecture, API Spec (for /api/recovery/v1 and INT-34), Error standard (MSG-P4-002), Interface spec (INT-34), Users Roles (RW-REFADM/RW-TRIBE), Test Cases.

Let me verify whether the story is in the "Technical Enabler Stories v5.xlsx" too, yes. And standalone story file.

Now, are there any other docs specifically about module boundary? Search "R-BND" or "BND-1".

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst pats=[/BND-1/,/R-BND/,/RecoveryBoundaryTest/,/RecoveryAccessGuard/,/no-collection-import/];\nM.docs.forEach((d,di)=>{\n  const hits=[];\n  d.secs.forEach((s,si)=>{ const t=s.h+'\\n'+s.t; if(pats.some(p=>p.test(t))) hits.push(si+': '+s.h); });\n  if(hits.length){console.log('\\n### '+d.folder+' / '+d.name); console.log(hits.slice(0,12).join('\\n'));}\n});\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_bnd.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_bnd.js
```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_bnd.js\""}
```

```text

### 04 User stories / Recovery Workbench Build Notes Technical Enablers v1
4: Step 3
5: Step 4
6: Step 5
7: Step 6
8: Step 7

### 04 User stories / Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2
0: Tab Defects

### 04 User stories / Recovery Workbench Technical Enabler Stories v5
5: 4. Flow
6: 5. Exception paths
8: 7. Acceptance criteria
9: 8. Business rules
13: 12. Contract
14: 13. Solution plan

### 04 User stories / Recovery Workbench Technical Enabler Stories v5
1: Tab Acceptance criteria

### 09 Testing and quality / Recovery Workbench Regression Suite v5
0: Tab Suite

### 09 Testing and quality / Recovery Workbench Test Cases v5
0: Tab Story test cases

```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

So connected docs are clear. Now let me verify the "Project Hub" story detail maybe links to original files. The hub has M.files 157 and fmeta. Let me see if TE-001 per-story file is one of them. Search M.files for "TE 001".

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));const ks=Object.keys(M.files);console.log(ks.filter(k=>/TE.?001|Technical Enabler|Build Notes Technical/i.test(k)).join('\\n'));console.log('--- fmeta sample ---');console.log(JSON.stringify(M.fmeta).slice(0,800));\""}
```

```text
Recovery Workbench Build Notes Technical Enablers v1.md
Recovery Workbench Technical Enabler Stories v5.md
Recovery Workbench Technical Enabler Stories v5.xlsx
--- fmeta sample ---
{"Recovery Workbench Accessibility Standard v2.docx":{"folder":"07 Screens and experience","size":161869},"Recovery Workbench Content and Label Standard v2.xlsx":{"folder":"07 Screens and experience","size":33462},"Recovery Workbench Customer and Partner Correspondence Templates v2.docx":{"folder":"07 Screens and experience","size":163434},"Recovery Workbench Design System and Component Library v1.html":{"folder":"07 Screens and experience","size":20208},"Recovery Workbench Error and Message Standard v3.docx":{"folder":"07 Screens and experience","size":187822},"Recovery Workbench Screen Inventory and Navigation v2.xlsx":{"folder":"07 Screens and experience","size":44396},"Recovery Workbench Screen Prototype v1.html":{"folder":"07 Screens and experience","size":20253},"Recovery Workbench S

```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The per-story file is not in M.files because it's inside zip. But on disk it is available.

Now let's confirm the Build Notes Epic 1 "Step 2" mention is just incidental (reference), not a separate section. Yes line 2419 in E1-043 step 2.

Also M.docs[73] Build Notes Epic 1 has "Step 2" mention at 416; not about TE-001 itself.

Now, what about the "Story Defects" item 3 where section 8 says R-BND; the build notes say BND-1..5; the AC and exception paths say BND. So it's a naming inconsistency in section 8, open. I'll flag it.

Also the story's flow step 3 says "RecoveryBoundaryTest with the rules BR1 to BR5", while section 8 BR1..BR6 are business rules mapping to BND-1..5. Another minor naming confusion (BR used both for business rules and boundary rules). The open defect only mentions R-BND. I can note both carefully, but don't overstate. In section 8, BR1..BR6. In flow step 3, "rules BR1 to BR5". That's consistent enough (BR1..BR5 are the first five). The "R-BND codes" line is the defect.

Now, what is TE-001's status? "Ready for build". Build window 2-13 Nov. Today's date 3 Nov 2026, so it's the first build item. It is order #2 (probably after #1? The Build Sequence order 2; order 1 might be something else). Let me check order 1 to know context.

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));const i=M.docs.findIndex(d=>/Build Sequence Epic 1/.test(d.name));const lines=M.docs[i].secs[0].t.split('\\n');console.log(lines.slice(0,12).join('\\n'));\""}
```

```text
The order the Epic 1 and Epic 2 work is pulled
115 items. Delivery runs as Kanban (DT04): items are pulled in this order as capacity frees up. The two-week windows are the sponsor review points, not sprint boundaries.
Order | Key | Title | Module | Type | Priority | Depends on | Review window | Dates | Release | Critical path
1 | RWB-E1-044 | Database migrations versioned with parameterized schema names | P3 | Enabler | Must |  | Window 1 | 2 Nov to 13 Nov | E1 | Yes
2 | RWB-TE-001 | Recovery module folder and boundary test | P2 | Enabler | Must |  | Window 1 | 2 Nov to 13 Nov | E1
3 | RWB-E1-042 | Central configuration service and parameter catalog | P3 | Enabler | Must | RWB-E1-044 | Window 1 | 2 Nov to 13 Nov | E1 | Yes
4 | RWB-TE-002 | Code owners for the recovery module | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
5 | RWB-TE-003 | Types and contract tests from the API specification | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
6 | RWB-TE-005 | Rule table test harness | P3 | Enabler | Must | RWB-E1-044 | Window 1 | 2 Nov to 13 Nov | E1
7 | RWB-TE-011 | PDPA lint for code, tests and logs | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
8 | RWB-TE-012 | Document storage containers | P5 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
9 | RWB-E1-043 | Reference data service with versioned tables | P3 | Enabler | Must | RWB-E1-042, RWB-E1-044 | Window 1 | 2 Nov to 13 Nov | E1 | Yes

```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good: TE-001 order 2, not critical path.

Now let me consider what "all the connected documents" means more broadly. The hub has a "Documents" tab with 192 docs. For a story page, it links to source doc + codes. There is no explicit "related docs" per story beyond REFDOCS. But I can present a comprehensive map:

Direct (reading order):
1. Technical Enabler Stories v5 (canonical story).
2. Per-story file (standalone).
3. Build Notes Technical Enablers v1 (step explanations).
4. Project Hub v14 (interactive reader).

Governing:
5. Business Requirements Program v3 (REQ-DRI-006; section 7 constraint).
6. Decision Log v8 (DL05, DL07, DL36; DT07, DT08).
7. Engineering Practices v4 (2.1, 2.2 — the practice TE-001 enforces).
8. Architecture Decision Records v1 (ADR-002, ADR-005, ADR-006).
9. ACE Architecture Decision v2 (modular monolith option).
10. Target Architecture v4 (5.1).
11. Technical Specifications by Module v3 / TSD P2 Integration v2 (T8 traceability; P2 module scope).
12. Interface Specifications v2 (INT-34 common module).
13. API Specification v2 (contract conventions for /api/recovery/v1).
14. Error and Message Standard v3 (MSG-P4-002).
15. Users Roles and Permissions v3 (RW-TRIBE, RW-REFADM).
16. Security and Access Design v2 (access check perhaps). Let me verify mentions of module boundary or INT-34/RecoveryAccessGuard. Search says no direct. It may still be relevant to access check. Let me check "ACE access check" in Security doc. Could include. But don't over-list.

Testing:
17. Test Cases v5 (8 TCs).
18. Regression Suite v5 (TC-01, TC-08).
19. Requirements Traceability Matrix v4 (REQ-DRI-006).
20. Story Defects v2 (open defect 3).
21. Definition of Ready and Done v3 (done criteria). Does it mention TE-001? Search "module folder" perhaps. Let me check.

Delivery:
22. Build Sequence Epic 1 and Epic 2 v4 (order 2, 2-13 Nov).
23. Story Build Order v1 (order 2).
24. Release Plan v3 (dependency that sets date: 2 Nov).
25. Team Start Pack v2 (week 2-6 Nov task).
26. Weekly Status Pack v2 (next week).
27. Dependency Map v2 — maybe DEP entries for module skeleton? Search gave none for TE-001; but could have "module". Let me check "module folder" or DL05.
28. Risks/Assumptions — DL05 risk? Search "module" maybe.
29. Document Control Sheet v10 — lists docs, not story.
30. Document Index v11 — folder catalog.

Related stories:
31. TE-002, TE-003, TE-011, TE-012 (depend on TE-001).
32. E1-007 integration adapters (BR5 exception; and REQ-DRI-006 shared).
33. 

_[truncated]_

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction scan(reDoc,reText,label){\n  const i=M.docs.findIndex(d=>d.name.match(reDoc));\n  if(i<0){console.log('missing',label);return;}\n  console.log('\\n### '+M.docs[i].name);\n  let n=0;\n  M.docs[i].secs.forEach((s,j)=>{\n    const l=s.t.split('\\n').filter(x=>reText.test(x));\n    if(l.length){console.log('-- '+j+' '+s.h+' --'); console.log(l.slice(0,6).join('\\n')); n++;}\n  });\n  if(!n) console.log('(no match)');\n}\nscan(/Definition of Ready and Done/,'module|boundary|enabler','DRD');\nscan(/Dependency Map/,'module|DL05|boundary','depmap');\nscan(/Risks Assumptions/,'module|DL05|boundary|ACE repo','risks');\nscan(/Security and Access Design/,'module|access check|INT-34|RecoveryAccessGuard','security');\nscan(/Environment and Deployment Design/,'module|boundary|pipeline|ArchUnit','env');\nscan(/Document Index/,'Technical enabler stories|Build notes, technical|Story defects','docindex');\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_extra.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_extra.js
```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_extra.js\" > \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\extra.txt\" 2>&1; Get-Content \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\extra.txt\" -TotalCount 120"}
```

```text

### Recovery Workbench Definition of Ready and Done v3
node : C:\Users\SahilMore\AppData\Local\Temp\opencode\query_extra.js:9
At line:1 char:1
+ node "C:\Users\SahilMore\AppData\Local\Temp\opencode\query_extra.js"  ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (C:\Users\SahilM...uery_extra.js:9:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
    const l=s.t.split('\n').filter(x=>reText.test(x));
                                             ^

TypeError: reText.test is not a function
    at C:\Users\SahilMore\AppData\Local\Temp\opencode\query_extra.js:9:46
    at Array.filter (<anonymous>)
    at C:\Users\SahilMore\AppData\Local\Temp\opencode\query_extra.js:9:29
    at Array.forEach (<anonymous>)
    at scan (C:\Users\SahilMore\AppData\Local\Temp\opencode\query_extra.js:8:18)
    at Object.<anonymous> (C:\Users\SahilMore\AppData\Local\Temp\opencode\query_extra.js:14:1)
    at Module._compile (node:internal/modules/cjs/loader:1781:14)
    at Object..js (node:internal/modules/cjs/loader:1913:10)
    at Module.load (node:internal/modules/cjs/loader:1505:32)
    at Function._load (node:internal/modules/cjs/loader:1309:12)

Node.js v22.23.2

```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The third arg label was passed as reText? Let me check scan signature: scan(reDoc,reText,label) and calls scan(regex,string,label) — passing string not regex. Fix by new RegExp.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nfunction scan(reDoc,reText,label){\n  const i=M.docs.findIndex(d=>d.name.match(reDoc));\n  if(i<0){console.log('missing',label);return;}\n  const r=new RegExp(reText,'i');\n  console.log('\\n### '+M.docs[i].name);\n  let n=0;\n  M.docs[i].secs.forEach((s,j)=>{\n    const l=s.t.split('\\n').filter(x=>r.test(x));\n    if(l.length){console.log('-- '+j+' '+s.h+' --'); console.log(l.slice(0,6).join('\\n')); n++;}\n  });\n  if(!n) console.log('(no match)');\n}\nscan(/Definition of Ready and Done/,'module|boundary|enabler','DRD');\nscan(/Dependency Map/,'module|DL05|boundary','depmap');\nscan(/Risks Assumptions/,'module|DL05|boundary|ACE repo','risks');\nscan(/Security and Access Design/,'module|access check|INT-34|RecoveryAccessGuard','security');\nscan(/Environment and Deployment Design/,'module|boundary|pipeline|ArchUnit','env');\nscan(/Document Index/,'Technical enabler stories|Build notes, technical|Story defects','docindex');\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_extra.js"}
```

```text
Wrote file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query_extra.js
```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query_extra.js\" > \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\extra.txt\" 2>&1; Get-Content \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\extra.txt\" -TotalCount 100"}
```

```text

### Recovery Workbench Definition of Ready and Done v3
-- 1 1. Where each definition applies --
Plan approved | The plan names every file, test and migration and touches one module | Tech lead
-- 3 2.1 What the story carries --
2 | Links | Epic, module, L3 process and decision, each from the process architecture and the module list
8 | Contract | The trigger, the service, the events published, the idempotency key and any call out of the module
-- 6 3.1 Built and tested --
2 | Pipeline | The nine pipeline gates pass: build and unit tests, lint, secret scan, PDPA lint, container scan, module boundary, integration and contract tests, AI first-pass review and human approval
-- 7 3.2 Controls --
12 | Boundaries | The story touches one module, or the other module's code owner has approved
-- 11 5. Who owns each definition --
Definition of done | TechX QA lead with the tech leads | Agreement at the weekly delivery review, with the ACE team for items that touch the common module

### Recovery Workbench Dependency Map v2
-- 0 Tab Dependencies --
DEP-01 | ACE team | Recovery module folder, package and boundary test in the ACE repository | E1 | 2026-11-02 00:00:00 | ACE team | DL05 | The squads cannot merge into ACE | Open
DEP-02 | ACE team | Code owners file and merge rules for the recovery module | E1 | 2026-11-02 00:00:00 | ACE team | DL04, DL37 | Reviews stall and changes cross module folders | Open
DEP-04 | ACE team | Common module services: sign-in, access check, audit and PII logging, the shared case view | E1 | 2026-11-09 00:00:00 | ACE team | None | Every screen and service waits for the access check | Open
DEP-06 | ACE team | Restructure calculator and plan status from the common module | E2 | 2026-12-01 00:00:00 | ACE team with the collection squad | DL14, DL30 | The treatment record shows no live plan | Open

### Recovery Workbench Risks Assumptions Issues and Dependencies v2
-- 0 Tab Risks --
R-03 | One squad's change holds the other's release | Medium | Medium | Feature flags, code owners and the module boundary test (DL04, DL37) | Tech leads | 2026-11-06 00:00:00 | Open
R-04 | Rules component is new to ACE | Medium | Medium | Decision table evaluator in the recovery module, tested rule by rule | Solution architect | 2026-11-27 00:00:00 | Open
-- 3 Tab Dependencies --
DEP-01 | ACE team | Recovery module folder, package and boundary test in the ACE repository | E1 | 2026-11-02 00:00:00 | ACE team | DL05
DEP-02 | ACE team | Cod
... truncated (5,697 chars total)
```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Excellent. Key: DEP-01 is the external dependency "ACE team — Recovery module folder, package and boundary test in the ACE repository" due 2 Nov, owner ACE team (DL05), status Open, impact "The squads cannot merge into ACE". That's a critical connection: TE-001 itself is a dependency item, owned by ACE team, not the squad? Interesting: story says TechX squad member does it under DL05 option B, but Dependency Map assigns ACE team and says open. That's a tension worth flagging. Let me read the full DEP-01 row and maybe "Risks" row. Already have. It says owner ACE team. But DL05 recommended B: TechX creates recovery module in own package now; ACE applies boundaries later. Story says squad member does it. Dependency map says ACE team. Could be a discrepancy. I should mention as a watch item, not overstate.

Also Release Plan: "Recovery module folder, package and boundary test in the ACE repository | E1 | 2 Nov | ACE team (DL05) | The squads cannot merge into ACE". Again owner ACE team. This is a notable inconsistency: story is written for RW-TRIBE squad member, yet delivery docs make it an ACE team dependency. Worth flagging as connected-doc conflict.

Let me check the Release Plan row fully and DEP-01 row.

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));let i=M.docs.findIndex(d=>/Release Plan v3/.test(d.name));M.docs[i].secs.forEach((s,j)=>{const l=s.t.split('\\n').filter(x=>/Recovery module folder/i.test(x));if(l.length)console.log('sec',j,s.h,'\\n'+l.join('\\n'));});i=M.docs.findIndex(d=>/Dependency Map/.test(d.name));console.log('\\nDEP-01 full:\\n'+M.docs[i].secs[0].t.split('\\n').filter(x=>x.startsWith('DEP-01')).join('\\n'));\""}
```

```text
sec 7 Slide 8. Dependencies that set the dates 
Recovery module folder, package and boundary test in the ACE repository | E1 | 2 Nov | ACE team (DL05) | The squads cannot merge into ACE

DEP-01 full:
DEP-01 | ACE team | Recovery module folder, package and boundary test in the ACE repository | E1 | 2026-11-02 00:00:00 | ACE team | DL05 | The squads cannot merge into ACE | Open

```

### Assistant - 2026-11-03 18:38 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now, is there an "Escalation" reference in Team Start Pack that mentions TE-001 as tech lead task in 2-6 Nov. Yes.

I think I have enough for a detailed answer. But the user asks "Refer this and find all the connected documents and tell me about RWB-TE-001 in detail." They likely want me to inspect the hub and report. I should give:

- What RWB-TE-001 is, in plain language.
- At-a-glance metadata.
- Why it matters (business rationale).
- What it builds (7 components / 19 packages, module map, boundary test rules, front-end rules, access guard).
- How it works step by step.
- The five boundary rules BND-1..5 + front-end rule.
- Acceptance criteria AC1-AC7 in a compact table.
- Test cases 8, regression 2.
- Done criteria.
- Dependencies / sequencing / ownership.
- Open issue/defect.
- Connected documents table grouped.
- Caveats/discrepancies found (generic doc row vs actual relevance; DEP-01 owner conflict; RTM only maps 3 TCs; open defect).

I should be careful not to overclaim on counts. Let me verify word "19 modules": P1-P10 = 10, S1-S9 = 9 => 19. Good.

Story module P2 Integration but cross-cutting.

Acceptance criteria:
AC1: class in recovery imports collection.internal -> build fails, log names BND-1, both classes.
AC2: recovery class calls common.api -> build passes.
AC3: integration.internal imports decision.internal.DecisionLogRepository -> fails BND-3; switch to recovery.decision.writer.DecisionLogWriter -> passes.
AC4: integration.internal uses casewf.internal.RecoveryCaseEntity -> fails BND-4.
AC5: casewf.internal uses java.net.http.HttpClient -> fails BND-5; same in integration.adapter passes.
AC6: front-end recovery/caselist imports collection/worklist/WorkList -> fails no-collection-import.
AC7: new package recovery.vendorx not in module map -> fails with message.

Exception paths X1-X7 map.

BR1-BR6:
BR1 BND-1 collection published only.
BR2 BND-2 common published only.
BR3 BND-3 recovery module only via published package or app event.
BR4 BND-4 entities/repos only own module.
BR5 BND-5 HTTP/SFTP/file clients only allowed packages: recovery.integration.adapter (E1-007) for files, agent runtime client for INT-23 (TE-013); no direct system-of-record calls.
BR6 module names/packages from map file, not test code.

Contract: every PR build and main; back end RecoveryBoundaryTest in unit test phase; front end dependency rules in lint; output pass/fail with rule code, class/file, dependency; idempotent; no state.
Plus RecoveryAccessGuard.require(ca

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));const i=M.docs.findIndex(d=>/^Recovery Workbench Technical Enabler Stories v5/.test(d.name));const lines=M.docs[i].secs[0].t.split('\\n').filter(l=>/^\\| RWB-TE-/.test(l));console.log(lines.join('\\n'));\""}
```

```text
| RWB-TE-001 | Recovery module folder and boundary test | P2 Integration | REQ-DRI-006 | None |
| RWB-TE-002 | Code owners for the recovery module | P2 Integration | REQ-DRI-006 | RWB-TE-001 |
| RWB-TE-003 | Types and contract tests from the API specification | P2 Integration | REQ-DRI-007, REQ-ACA-003 | RWB-TE-001 |
| RWB-TE-004 | Masked data in SIT and UAT | P1 Recovery data engine | REQ-RDF-010, REQ-ACA-005 | RWB-E1-065 |
| RWB-TE-005 | Rule table test harness | P3 Case and workflow | REQ-CWC-014, REQ-CWC-013 | RWB-E1-044 |
| RWB-TE-006 | Outbox and retry for outbound work | P2 Integration | REQ-DRI-007 | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| RWB-TE-007 | Scheduled jobs on Quartz | P3 Case and workflow | REQ-CWC-007, REQ-CWC-011, REQ-RDF-007 | RWB-E1-044, RWB-E1-056 |
| RWB-TE-008 | Decision log hash chain check | P7 Decision center and log | REQ-DRI-003 | RWB-E1-008, RWB-TE-007 |
| RWB-TE-009 | Performance test harness | P2 Integration | REQ-OCC-007, REQ-WKM-002 | RWB-TE-004 |
| RWB-TE-010 | Browser and accessibility tests | P2 Integration | REQ-OCC-007, REQ-WKM-001 | RWB-TE-003 |
| RWB-TE-011 | PDPA lint for code, tests and logs | P2 Integration | REQ-RDF-010, REQ-ACA-005 | RWB-TE-001 |
| RWB-TE-012 | Document storage containers | P5 Document hub | REQ-DCM-003, REQ-DCM-002 | RWB-TE-001 |
| RWB-TE-013 | Agent runtime client with fallback | P10 Agent runtime | REQ-DRI-001, REQ-DRI-005, REQ-ACA-010 | RWB-TE-007, RWB-E1-058, RWB-E1-027 |

```

### Assistant - 2026-11-03 18:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

13 total, but story files zip only contains 11 TE files (missing 009, 010). Interesting but not central. TE-001's dependents are TE-002, TE-003, TE-011, TE-012. Also TE-010 depends on TE-003, so indirectly. TE-013 depends on TE-007 etc.

Wait, Build Sequence showed TE-002/003/011/012 depend on TE-001. Good.

Now let me verify the build window and critical path flag for TE-001: not critical path. Good.

Potential "measure" is count of boundary violations merged to main = 0. Good.

Let me double check "P2 Integration" module assignment: yes.

Let me check whether TE-001 has a "Feature" none. Yes.

What does "19 Workbench modules" map to? P1 dataengine, P2 integration, P3 casewf, P4 access, P5 dochub, P6 comms, P7 decision, P8 payments, P9 reporting, P10 agent; S1 valuation, S2 treatment, S3 guarantee, S4 litigation, S5 asset, S6 debtsale, S7 writeoff, S8 deviation, S9 partner. Good.

Check build notes "Step 5" says test-only controller declares Case record R and TC-TE-001-08 calls as RW-REFADM. The story's section 16 TC-08 just says "RW-REFADM calls test-only Case record R endpoint; refused with MSG-P4-002." Good.

Now let me examine whether there are any other "connected" docs in the hub's search index e.g., a "Story map" or "Team Start Pack" that point to TE-001. Already covered.

Let me also verify the per-story file's presence in the zip and whether the zip content is identical. Not necessary.

Now, one more thing: "RWB-TE-001" in the hub's "Story Defects" has 3 rows? The query showed one row "RWB-TE-001 | 3 | ...". Good.

Could there be a "Test Cases" row for TE-001 in the "Tab Story test cases" and "Regression Suite" only. Yes.

Could there be an "Acceptance Criteria Glossary" entry for AC1 etc.? No.

Now, about "connected documents" — the hub's story page provides:
- the source doc name in the header (Technical Enabler Stories v5? Actually the hub buildStories excludes per-story files and build notes; the story home is Technical Enabler Stories v5, because it's the first non-inzip doc with a heading. It also finds Build Notes Technical Enablers but buildStories excludes /Build Notes/i. So the hub shows "from Recovery Workbench Technical Enabler Stories v5".)
- "Documents you will need": 8 docs (generic).
- "Everything this story refers to": codes named in the story (REQ-DRI-006, INT-34, MSG-P4-002, TC-TE-001-08, RW-REFADM) with their definitions, not docs per se.
- The open-all references.

So when the user says "find all the connected documents", the

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"limit": 10, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "pattern": "function fileBtn"}
```

```text
Found 1 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 3285: function fileBtn(d){

```

### Assistant - 2026-11-03 18:39 | opencode-go/deepseek-v4.1-flash | build

**Tool `read`** - completed

```json
{"limit": 18, "offset": 3285, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html"}
```

```text
Read file 12 Project communication\Recovery Workbench Project Hub v14.html, lines 3285-3302
3285: function fileBtn(d){
3286:   const key=d.inzip||d.file;
3287:   if(!M.files||!M.files[key]) return '';
3288:   return `<button class="dl" data-file="${esc(key)}">Open the original ${esc(key.split('.').pop().toUpperCase())}</button>`;
3289: }
3290: function wireFile(){
3291:   document.querySelectorAll('.dl[data-file]').forEach(b=>b.onclick=()=>openOriginal(b.dataset.file));
3292: }
3293: const MIME={docx:'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
3294:  pptx:'application/vnd.openxmlformats-officedocument.presentationml.presentation',
3295:  xlsx:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
3296:  pdf:'application/pdf',html:'text/html',md:'text/markdown',sql:'text/plain',yaml:'text/yaml',zip:'application/zip'};
3297: async function openOriginal(key){
3298:   const id=M.files[key]; if(id==null) return;
3299:   const el=document.getElementById('f'+id); if(!el) return;
3300:   const raw=Uint8Array.from(atob(el.textContent.trim()),c=>c.charCodeAt(0));
3301:   const buf=await new Response(new Blob([raw]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
3302:   const ext=key.split('.').pop().toLowerCase();
[Output truncated. Continue reading with offset: 3303]
```

### Assistant - 2026-11-03 18:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

So the hub story page links to the original Technical Enabler Stories v5 .md or .xlsx, not the per-story file. The per-story file is a separate deliverable on disk. I'll say that.

Now let me verify the "Technical Enabler Stories v5" doc's file key is the .md or .xlsx; M.files has both. The hub likely opens whichever doc d.file points to. Fine.

Now, should I mention the actual original file paths vs hub docs? Yes.

Let me also check if the per-story file's title and content match exactly. Yes.

Now, let me consider the "Project Hub v14" may have a "Story detail" that is from Build Notes, not Technical Enabler Stories. The hub's story home search picks the first doc in M.docs sorted by folder/name. The first match might be Build Notes Technical Enablers (folder 04) or Technical Enabler Stories. buildStories skips docs with /Build Notes/i, so the home is Technical Enabler Stories v5 (doc 80). Good. The hub page's "from" is Technical Enabler Stories v5. The "note" expansions come from NOTES (Build Notes) in the story detail? The openStory only shows NOTES[st.k] toggle, but I didn't see where NOTES is rendered. Wait, openStory pushes a button "Show the step explanations" if NOTES[st.k]. Does it render NOTES? I only saw SIMPLE block, S.secs. Maybe another function or omitted. Let me search NOTES usage. Not crucial.

Actually, the hub's story page shows the full story text from Technical Enabler Stories v5, including sections 1-19, and "Everything this story refers to". It also has a "step explanations" toggle if NOTES[st.k] exists. Where is that rendered? Search "NOTES[st.k]" or "NOTESOPEN".

</details>

**Tool `grep`** - completed

```json
{"limit": 20, "path": "12 Project communication\\Recovery Workbench Project Hub v14.html", "pattern": "NOTESOPEN|NOTES\\["}
```

```text
Found 7 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Project Hub v14.html:
  Line 2339: let CURKEY='', NOTESOPEN=true, INFLOW=false;

  Line 2570:     (NOTES[st.k]?`<button class="dl" id="notetog">${NOTESOPEN?'Hide':'Show'} the step explanations</button>`:'')+

  Line 2602:   if(ntb) ntb.onclick=()=>{ NOTESOPEN=!NOTESOPEN; openStory(di,si); };

  Line 2949:       const nt=(NOTES[CURKEY]||{})[fm[1]];

  Line 2953:         (nt?`<details class="note"${NOTESOPEN?' open':''}><summary>What this step means</summary>${link(nt)}</details>`:'')+

  Line 2959:       const nt2=(NOTES[CURKEY]||{})[pm[1]];

  Line 2962:         (nt2?`<details class="note"${NOTESOPEN?' open':''}><summary>What this step means</summary>${link(nt2)}</details>`:'')+

```

### Assistant - 2026-11-03 18:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

So the hub embeds the build notes as "What this step means" under each flow step. Good. The hub is the synthesis of story + build notes + code definitions. Nice to mention.

Now, "find all the connected documents" — maybe they also want the "original files" tab connections. The hub has 157 original files embedded. TE-001's source files are Technical Enabler Stories v5.md/.xlsx and Build Notes Technical Enablers v1.md, plus per-story file not embedded. Fine.

Let me now think about how to phrase the "detail" without overwhelming. The user likely wants a briefing. I'll use headings and tables.

Let me draft the content.

---

**Opening**: "The hub is a self-contained reader over 192 docs. RWB-TE-001 is a technical enabler, not a business feature. Its canonical text is in Technical Enabler Stories v5, with a standalone story file and 8 step-by-step build notes. It is the first recovery story after the migration baseline and the thing every other recovery story builds inside."

**At a glance** UI block.

**1. What it is and why it exists**
- Modular monolith on ACE: one service/repo/front end. 3 teams (ACE common, collection, TechX recovery) build in one codebase. Without enforced boundaries, one team's change breaks another, and direct calls to core systems bypass COLLINS/file load path.
- TE-001 creates the physical skeleton (19 module folders, api vs internal), the module map, the ArchUnit boundary test and front-end dependency rules, plus the recovery-side access guard. It makes the architecture rule executable in every PR build.
- Measure: zero boundary violations merged to main.

**2. What gets built**
Table:
- 19 module packages (P1-P10, S1-S9), each api/internal + package-info; front-end src/modules/recovery.
- `architecture/recovery-modules.yaml`: module code, Java package, published packages, allowed client libraries.
- `RecoveryBoundaryTest` + `ModuleMapLoader`: ArchUnit rules BND-1..5 from map.
- Test-only breaking fixtures per rule under src/test.
- Front-end dependency rule file: no collection imports; common only via public index; rule no-collection-import.
- `RecoveryAccessGuard.require(...)`: calls INT-34; 403 MSG-P4-002.
- Pipeline wiring: PR + main; back end unit tests; front-end lint; failure blocks merge.

**3. The five boundary rules** (UI table or Markdown)
BND-1 collection only via published packages.
BND-2 common only via published packages.
BND-3 recovery modules only via published packages or app events.
BND-4 entities/repositories o

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));const d=M.docs[80];let t=d.secs[1].h+'\\n'+d.secs[1].t;for(let k=2;k<d.secs.length;k++){if(/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[k].h.trim()))break;t+='\\n'+d.secs[k].h+'\\n'+d.secs[k].t;}const rx=/\\b(RWB-[A-Z]{1,3}\\d?-\\d{3}|REQ-[A-Z0-9]{2,5}-\\d{3}|INT-\\d{2}|MSG-[A-Z0-9]{1,5}-\\d{3}|TC-[A-Z0-9]{1,4}-\\d{3}-\\d{2}|RW-[A-Z]{3,9}|DL\\d{2}|DT\\d{2}|ADR-\\d{3}|BR-\\d|BND-\\d)\\b/g;const s=new Set(t.match(rx)||[]);console.log([...s].sort().join('\\n'));\""}
```

```text
ADR-002
ADR-005
ADR-006
BND-1
BND-2
BND-3
BND-4
BND-5
DL05
DL07
DL36
DT07
DT08
INT-23
INT-34
MSG-P4-002
REQ-DRI-006
RW-PLATADM
RW-REFADM
RW-TRIBE
RWB-E1-007
RWB-E1-020
RWB-E1-027
RWB-TE-001
RWB-TE-002
RWB-TE-003
RWB-TE-013
TC-TE-001-01
TC-TE-001-02
TC-TE-001-03
TC-TE-001-04
TC-TE-001-05
TC-TE-001-06
TC-TE-001-07
TC-TE-001-08

```

### Assistant - 2026-11-03 18:40 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The hub's IDRX doesn't match ADR, BND, DL? It does match DL\d{2}, DT\d{2}, ADR-\d{3}, BR-, but BND isn't in IDRX. It matches RWB/E1/TE, REQ, INT, MSG, TC, RW. So "Everything this story refers to" would include RWB-TE-002/003/013, E1-007/020/027, REQ, INT-23/34, MSG, TCs, RW roles, DL05/07/36, DT07/08, ADR-002/005/006. It might include many. My earlier count said STORY 1 because I excluded st.k, but TE-002 etc. are STORY kind, so why only 1? Let me recheck. Maybe my regex `RWB-[A-Z]{1,3}\d?-\d{3}` doesn't match RWB-TE-002? It should. Wait, the codesIn function only includes codes that exist in M.ids and dedupes. It should include 4 story codes. My output said "STORY: 1". That suggests the story text used for codesIn (storyText) stops at the next story heading, but the story section includes only the TE-001 section and its subsections, which do mention TE-002 etc. Hmm. Maybe the M.ids for RWB-TE-002 isn't in the id map? It is. Let me check directly.

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));['RWB-TE-001','RWB-TE-002','RWB-TE-003','RWB-TE-013','RWB-E1-007','RWB-E1-020','RWB-E1-027'].forEach(c=>console.log(c,!!M.ids[c],M.ids[c]&&M.ids[c].k));\""}
```

```text
RWB-TE-001 true STORY
RWB-TE-002 true STORY
RWB-TE-003 true STORY
RWB-TE-013 true STORY
RWB-E1-007 true STORY
RWB-E1-020 true STORY
RWB-E1-027 true STORY

```

### Assistant - 2026-11-03 18:40 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

My earlier codesIn regex used `\\b(...RWB-[A-Z]{1,3}\\d?-\\d{3}...)` with `\\b` at the end; "RWB-TE-002" followed by " Code owners" should match. But the story text I built starts at d.secs[1] and stops at next story heading. It includes section 19 out of scope with TE-002 etc. Why STORY 1? Because in codesIn, `if(seen[c]||!M.ids[c]) return; seen[c]=1;` then by[k].push. It should have 4+ story codes. Wait, my output listed "STORY: 1" and "INT:1 MSG:1 TC:1 RW:1". That looks like only the first occurrence of each kind? Maybe the regex alternation order: `RWB-[A-Z]{1,3}\d?-\d{3}` matches RWB-TE-001; then for RWB-TE-002, the regex engine may match "RWB-TE-002" but the `\b` before... Hmm.

Actually, the IDRX has `RWB-[A-Z]{1,3}\d?-\d{3}` which matches "RWB-TE-002". But the alternation is inside `\b(...)\b`. Fine.

Wait, maybe `storyText` for d.secs[1] only includes section 1 (Story) and stops at the next heading "2. Business rationale" because storyText breaks on /^RWB-.../ only. No, it includes all until next story.

Let me not worry; the exact "Everything this story refers to" list is not central. But I should be accurate if I mention it. Let me directly run codesIn like the hub to see.

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));const d=M.docs[80];let t=d.secs[1].h+'\\n'+d.secs[1].t;for(let k=2;k<d.secs.length;k++){if(/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[k].h.trim()))break;t+='\\n'+d.secs[k].h+'\\n'+d.secs[k].t;}const IDRX=new RegExp('\\\\b(AC-ALT-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|AC-EXC-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|AC-BG-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|AC-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|BR-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|VR-[A-Z0-9]{1,5}-\\\\d{2,3}(?:-\\\\d+)?|SC-[A-Z0-9]{1,5}-\\\\d{2,3}|RWB-[A-Z]{1,3}\\\\d?-\\\\d{3}|REQ-[A-Z0-9]{2,5}-\\\\d{3}|FEAT-[A-Z0-9]{2,5}-\\\\d{2,3}|DF-[A-Z]{2,4}-\\\\d{3}|MSG-[A-Z0-9]{1,5}-\\\\d{3}|LOV-[A-Z_]{3,30}|R-UNI-\\\\d{2}|TC-[A-Z0-9]{1,4}-\\\\d{3}-\\\\d{2}|RW-[A-Z]{3,9}|SY-[A-Z]{3,9}|JOB-\\\\d{2}|SCR-\\\\d{2}|INT-\\\\d{2}|CTL-\\\\d{2}|EV-\\\\d{2}|NFR-\\\\d{3}|DQ-\\\\d{3}|ADR-\\\\d{3}|REC-\\\\d{2}|DL\\\\d{2}|DT\\\\d{2})\\\\b','g');const by={};const seen={};(t.match(IDRX)||[]).forEach(c=>{if(seen[c]||!M.ids[c])return;seen[c]=1;const k=M.ids[c].k;(by[k]=by[k]||[]).push(c);});console.log(JSON.stringify(by,null,1));\""}
```

```text
{
 "STORY": [
  "RWB-TE-001",
  "RWB-E1-007",
  "RWB-TE-013",
  "RWB-TE-002",
  "RWB-E1-020",
  "RWB-E1-027",
  "RWB-TE-003"
 ],
 "REQ": [
  "REQ-DRI-006"
 ],
 "DL": [
  "DL05",
  "DL36",
  "DL07"
 ],
 "RW": [
  "RW-TRIBE",
  "RW-PLATADM",
  "RW-REFADM"
 ],
 "DT": [
  "DT08",
  "DT07"
 ],
 "ADR": [
  "ADR-002",
  "ADR-005",
  "ADR-006"
 ],
 "MSG": [
  "MSG-P4-002"
 ],
 "TC": [
  "TC-TE-001-08",
  "TC-TE-001-01",
  "TC-TE-001-02",
  "TC-TE-001-03",
  "TC-TE-001-04",
  "TC-TE-001-05",
  "TC-TE-001-06",
  "TC-TE-001-07"
 ],
 "INT": [
  "INT-23",
  "INT-34"
 ]
}

```

### Assistant - 2026-11-03 18:40 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Earlier query excluded st.k but I built story differently? It doesn't matter. The hub's "Everything this story refers to" will show all these codes, grouped. That's a lot of inline definitions. But connected documents are those that define them. I can mention: the hub expands 7 story refs, REQ-DRI-006, DL05/07/36, DT07/08, ADR-002/005/006, MSG-P4-002, INT-23/34, TC-01..08, and roles RW-TRIBE/RW-PLATADM/RW-REFADM.

Wait, the hub's IDRX doesn't include BND-1..5, so those aren't clickable codes. Fine.

I could list "What the hub expands inline" as a compact sentence, and map the important ones to docs.

Now, let me ensure I don't say "ADR-002/005/006 are in the hub's reference table" if they are; IDRX includes ADR-003. Yes.

Now, one more check: The hub's "Everything this story refers to" may show "RWB-TE-002" etc. as STORY codes with empty t; clicking opens the story. The connected docs for those are their source docs. Fine.

Now, let's think about whether to include a "plain English" summary at the top:
"In plain terms: before anyone builds a recovery feature, this story lays out 19 labelled boxes in the codebase, writes a map saying which boxes may talk to which, and installs an automated inspector that fails the build if someone reaches into another team's box or calls a bank system directly. It also gives every recovery URL a common permission check."

That's a good opener.

**Details on "BND-5"**: "only packages the map allows for client libraries may use HTTP, SFTP or file transfer clients: recovery.integration.adapter for files, and the agent runtime client for INT-23. No recovery class calls a system of record." This is how REQ-DRI-006 is enforced. Good.

**Details on "BND-1/2"**: collection/common published packages. Note the common module published package names are assumed `..common.api..` until ACE names them (DL05); the collection module published packages also named by ACE. The map has them.

**Details on "published package"**: "an api package (or another package the map lists) that other modules may import." Good.

**Details on "module map"**: `architecture/recovery-modules.yaml`, owned by TechX tech leads through code owners (TE-002); changing it needs tech lead approval. The test reads it at runtime; adding a module is a file change, not test code.

**Details on "front-end rules"**: dependency rule file for `src/modules/recovery`; no imports from `src/modules/collection`; `src/common` only via public index; breaking fixture outside shipping 

_[truncated]_

</details>

**Tool `openchamber`** - completed

```json
{"action": "work.name", "title": "RWB-TE-001 document map"}
```

```text
{"schemaVersion":1,"ok":true,"action":"work.name","data":{"task":"session","sessionId":"ses_e5ecea017ffeQi4bbG3KwmumEu","title":"RWB-TE-001 document map","named":true}}
```

### Assistant - 2026-11-03 18:40 | opencode-go/deepseek-v4.1-flash | build

I found the hub and traced it properly. It is a self-contained reader, not a set of links: it embeds 192 documents in a compressed payload and assembles each story page from the canonical story plus its build notes. I decoded that payload and followed every ID on the RWB-TE-001 page, so the document list below is the full set that touches the story — not just the eight generic "documents you will need" the page displays.

**In one sentence:** RWB-TE-001 is the scaffolding story for the whole Recovery Workbench. It creates the 19 recovery module packages inside ACE, publishes a module map, and installs a build-time boundary test that fails a pull request if one team reaches into another team's code or if recovery code calls a bank system directly. No screen, no table, no new endpoint.

```openui-lang
root = Stack([glance, flags, rules, issue])
glance = Card("RWB-TE-001 at a glance", [facts])
facts = KeyValue([{label: "Story", value: "Recovery module folder and boundary test"}, {label: "Type", value: "Technical enabler, not a business feature"}, {label: "Epic / release", value: "E1, 30 November 2026"}, {label: "Module", value: "P2 Integration, cross-cutting"}, {label: "Requirement", value: "REQ-DRI-006"}, {label: "Decision", value: "DL05, option B from 2 November 2026"}, {label: "Depends on", value: "None"}, {label: "Build slot", value: "Order 2 of 115, 2-13 November 2026"}])
flags = Row([Badge("Must", "error"), Badge("Ready for build", "success"), Badge("E1 - 30 Nov 2026", "info"), Badge("Not critical path", "neutral")])
rules = Table(["Rule", "What it enforces"], [["BND-1", "Recovery reaches collection only through collection's published packages"], ["BND-2", "Recovery reaches common only through common's published packages"], ["BND-3", "One recovery module reaches another only through a published package or an application event"], ["BND-4", "Entities and repositories stay inside their own module, so a module reads only its own tables"], ["BND-5", "HTTP, SFTP and file-transfer clients only in map-approved packages; no direct system-of-record call"], ["Front end", "No recovery screen imports a collection screen; common imports only through its public index"]])
issue = Callout("Open story defect #3: section 8 calls the rule codes **R-BND**, while every other section uses **BND-1 to BND-5**. It needs a ruling before build.", "warning", "One open inconsistency")
```

## 1. Why this story exists

ACE is one Spring Boot service, one repository and one React front end. Three groups build inside it: the ACE team (common), the collection squad, and the two TechX recovery squads. The agreed architecture is a **modular monolith** — modules by folder, each owning its tables, calling another module only through a published interface or an application event.

Without a machine check, that is only a convention. TE-001 makes it executable:

- a violation fails the pull request, not a design review weeks later;
- a direct call to a system of record is stopped at build time, so data can only arrive through COLLINS or a file load, as ADR-005 requires;
- the success measure is **zero boundary violations merged to main**.

It is also deliberately early: the Story Build Order puts it at **#2 of 115**, immediately after the database migration baseline, because every later recovery story places its code inside the folders TE-001 creates.

## 2. What gets built

| Component | What it is | Detail |
|---|---|---|
| **19 module packages** | `ace-service/src/main/java/<ACE base package>/recovery/` | One package each for P1-P10 and S1-S9: `dataengine`, `integration`, `casewf`, `access`, `dochub`, `comms`, `decision`, `payments`, `reporting`, `agent`, `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner`. Each has an `api` child for published interfaces and an `internal` child for everything else, plus a `package-info` file. |
| **Front-end folder** | `src/modules/recovery/` | The recovery screens live here, with their own dependency rules. |
| **Module map** | `architecture/recovery-modules.yaml` | For each module: module code, Java package, published packages, and the client libraries it may use. The test reads this file rather than hard-coding module names. Owned by the TechX tech leads through code owners (TE-002). |
| **Boundary test** | `RecoveryBoundaryTest` + `ModuleMapLoader` | An ArchUnit test class that builds the five rules from the map. ArchUnit checks dependencies between compiled classes as an ordinary unit test. An unlisted package fails with `package {package} is not in the module map`. |
| **Breaking fixtures** | Test-only classes under `src/test` | One fixture per rule, written to break it and prove the rule fires. They never ship. |
| **Front-end rules** | Dependency rule file for `src/modules/recovery` | No file under recovery imports anything from `src/modules/collection`; imports from `src/common` go only through its public index. The breaking fixture fails with `no-collection-import`. |
| **Access guard** | `RecoveryAccessGuard.require(String capabilityArea, Right right, ScopeTarget target)` | Attached to every path under `/api/recovery/v1/`. It calls the common module's published access check, INT-34. A missing right throws `AccessDeniedException`, mapped to a 403 Problem with `MSG-P4-002`. The actual access check belongs to ACE, not this story. |
| **Pipeline wiring** | Pull request build and main build | The back-end test runs in the unit test phase; the front-end rules run in lint. A failure blocks the merge. The checks hold no state, so the same commit always gives the same result. |

## 3. The rules in plain English

- **BND-1** — recovery code may use the collection module only through the packages the collection module publishes. It cannot import `collection.internal.*`.
- **BND-2** — the same rule applies to the common module. Until ACE names its published packages, the map uses the placeholder `..common.api..`.
- **BND-3** — two recovery modules meet only through a published package or an application event. `recovery.decision.internal.DecisionLogRepository` is out; `recovery.decision.writer.DecisionLogWriter` is in.
- **BND-4** — entities and repositories stay inside their owning module. A module reads only its own tables; another module's entity is a boundary break, not a shortcut.
- **BND-5** — only the packages the map allows may use HTTP, SFTP or file-transfer clients. The two sanctioned places are `recovery.integration.adapter` for files (RWB-E1-007) and the agent runtime client for the enterprise model endpoint INT-23 (RWB-TE-013). No recovery class calls a system of record.
- **BR6** — the module names, packages and published packages come from the map file, not from test code. Adding or renaming a module is a map change, approved by a TechX tech lead.

The front-end rules mirror BND-1 and BND-2: no collection screen imports, and common imports only through its public index.

## 4. Acceptance criteria

| AC | What the test proves |
|---|---|
| **AC1** | `recovery.casewf.internal.SampleService` imports `collection.internal.CollectorRepository`; the build fails and the log names BND-1, `SampleService` and `CollectorRepository`. |
| **AC2** | The same class calls an interface in `common.api`; the build passes. This proves the rule is not too wide. |
| **AC3** | `recovery.integration.internal` imports `recovery.decision.internal.DecisionLogRepository`; BND-3 fails. Switching to the published `recovery.decision.writer.DecisionLogWriter` passes. |
| **AC4** | `recovery.integration.internal` uses `recovery.casewf.internal.RecoveryCaseEntity`; BND-4 fails. |
| **AC5** | `recovery.casewf.internal` uses `java.net.http.HttpClient`; BND-5 fails. The same use in `recovery.integration.adapter` passes. |
| **AC6** | A `src/modules/recovery/caselist` component imports `src/modules/collection/worklist/WorkList`; the front-end build fails with `no-collection-import`. |
| **AC7** | A new `recovery.vendorx` package is not in the module map; the build fails with `package recovery.vendorx is not in the module map`. |

The exception paths X1-X7 map one-to-one to these: collection internal, recovery module internal, another module's entity, a direct HTTP/SFTP client, a collection screen import, an unlisted package, and a role without the right (`MSG-P4-002`).

## 5. Tests, contract and definition of done

- **8 test cases:** `TC-TE-001-01` to `TC-TE-001-07` cover AC1-AC7 at System level; `TC-TE-001-08` covers access at Access level. The full Given/When/Then is in **Test Cases v5**, tab *Story test cases*.
- **Regression:** `TC-TE-001-01` and `TC-TE-001-08` are marked **Yes** in the Regression Suite.
- **Traceability:** the RTM row for `REQ-DRI-006` links `RWB-E1-007`, `RWB-TE-001` and `RWB-TE-002`, but only lists `TC-TE-001-02`, `03` and `05`. The story's own traceability says `TC-TE-001-01` to `08`, so the matrix is narrower than the story — worth confirming whether that is intentional.
- **Contract:** every pull request and every main build; back-end test in the unit test phase; front-end rules in lint; pass, or fail with the rule code, the class or file, and the dependency. Same commit, same result; rerun needs no cleanup.
- **Log text:** `Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event.` The unlisted-package case reads `package {package} is not in the module map`. This text is for developers and is deliberately outside the Workbench message standard.
- **Done when:** the tests pass, and the main pipeline shows the boundary test in its unit test report.

## 6. Delivery, ownership and sequencing

- **Build order:** 2 of 115. Window 1, **2-13 November 2026**. Release **E1, 30 November 2026**. Not marked critical path.
- **Direct dependents:** `RWB-TE-002` (code owners — owns the module map file), `RWB-TE-003` (types and contract tests), `RWB-TE-011` (PDPA lint), `RWB-TE-012` (document storage containers). If TE-001 slips, those four slip with it.
- **Preconditions:** access to the ACE repository for the TechX squads (`DL36`); `DL05` applied as option B from 2 November (TechX creates the recovery module in its own package, ACE applies the common and collection boundaries later); the common module's published packages named — placeholder `..common.api..` until ACE does it; the ACE build runs the unit test phase on every pull request.
- **Authority:** `RW-TRIBE` tribe lead and squad members create the folders, map and test; TechX tech leads (code owners, TE-002) approve changes to the map or boundary rules; the ACE team names the common and collection published packages (`DL05`); `RW-PLATADM` runs the pipeline. No delegation-of-authority level applies because it takes no business decision.
- **Out of scope:** code owners (`RWB-TE-002`), types and contract tests (`RWB-TE-003`), boundaries inside the common and collection modules (ACE under `DL05` option A), and the integration adapter pattern itself (`RWB-E1-007`).

## 7. What I would check before build

1. **Open story defect #3.** Section 8 says "The R-BND codes are the names of the boundary test rules", while the rules are `BND-1` to `BND-5` everywhere else. The Story Defects workbook records this as **Open**. It is only a naming inconsistency, but it is exactly the kind of thing a developer copies into code.
2. **DEP-01 ownership.** The Dependency Map and Release Plan both describe "Recovery module folder, package and boundary test in the ACE repository" as an **ACE team** dependency, due 2 November, status **Open**, impact "The squads cannot merge into ACE". The story's actor is `RW-TRIBE` and `DL05` option B says TechX creates it. Confirm at kickoff whether ACE creates the folders or only provides repository access.
3. **RTM coverage.** As above: the matrix lists three of the eight test cases. If the RTM is meant to be complete, it needs TC-01, 04, 06, 07 and 08 added.
4. **The `..common.api..` placeholder.** BND-2 is only as correct as the published package names ACE supplies. If ACE later names them differently, the rule either blocks valid calls or lets invalid ones through. This is called out as an assumption in the preconditions, not a defect.
5. **BND-5 is a controlled exception, not a loophole.** Adding a new client library or a new adapter package means changing the module map, which needs a TechX tech lead's approval. That is deliberate: the map is the decision record for "who may call outside".

## 8. Connected documents

I have grouped these by the role they play. Paths are relative to the SharePoint set root.

### A. The story itself

| Document | Folder | Why it is connected |
|---|---|---|
| `Recovery Workbench Technical Enabler Stories v5.md` / `.xlsx` | `04 User stories` | The canonical TE-001 text: metadata, story, rationale, preconditions, flow, exceptions, seven ACs, six business rules, contract, solution plan, eight test cases, traceability and out-of-scope. TE-001 is one of 13 enablers in this set. |
| `RWB TE 001 Recovery module folder and boundary test v1.md` | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5` | The standalone one-story pack, same 19 sections. This is the file to hand to a coding agent. |
| `Recovery Workbench Build Notes Technical Enablers v1.md` | `04 User stories` | Eight flow-step explanations — who acts, what runs on its own, what has to be built. The hub shows these under each step as "What this step means". The story governs if the two differ. |
| `Recovery Workbench Project Hub v14.html` | `12 Project communication` | The interactive reader. Its TE-001 page assembles the story, the build notes and inline definitions of every code the story names. |

### B. Requirements, architecture and decisions it implements

| Document | Folder | Why it is connected |
|---|---|---|
| `Recovery Workbench Business Requirements Program v3.docx` | `03 Requirements and specifications` | Defines `REQ-DRI-006` ("No component calls a system of record directly") and the section 7 constraint "Modular monolith"; section 5.2 is the P2 requirement context. |
| `Recovery Workbench Decision Log v8.xlsx` | `01 Decisions and governance` | `DL05` (module skeleton: B from 2 November, then A), `DL07` (one front end with a recovery folder), `DL36` (named TechX team); `DT07` (one ACE service, repository and front end) and `DT08` (modular monolith). |
| `Recovery Workbench Engineering Practices v4.docx` | `11 Delivery and operations` | Section 2.1 "One service, three modules", section 2.2 "Boundary rules", and section 10, which assigns module structure and boundary test ownership to the ACE team. |
| `Recovery Workbench Architecture Decision Records v1.md` | `05 Technical architecture` | `ADR-002` (modular monolith), `ADR-005` (data through COLLINS and file loads, no direct system-of-record calls), `ADR-006` (one ACE front end with a recovery module folder). |
| `Recovery Workbench ACE Architecture Decision v2.docx` | `05 Technical architecture` | Records the chosen option: modular monolith by folder, boundaries tested at build time, and the `DL05` caveat that TechX builds in its own package until ACE moves. |
| `Recovery Workbench Target Architecture v4.docx` | `05 Technical architecture` | Section 5.1 repeats the module model: common, collection and recovery; each module owns its tables; a boundary test runs in every build. |
| `Recovery Workbench TSD P2 Integration v2.md` | `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3` | The P2 module specification. Its T8 traceability maps `REQ-DRI-006` to `RWB-E1-007`; TE-001 is the P2 enabler that enforces the same requirement at build time. |
| `Recovery Workbench Interface Specifications v2.md` / `.xlsx` | `05 Technical architecture` | `INT-34` is the ACE common module's published interface — the access check, shared case view and shared services that `RecoveryAccessGuard` calls. |
| `Recovery Workbench API Specification v2.yaml` / `.html` | `05 Technical architecture` | Defines the `/api/recovery/v1` contract, the access and error conventions, and the types that TE-003 generates. TE-001 itself adds no endpoint. |
| `Recovery Workbench Error and Message Standard v3.docx` | `07 Screens and experience` | The exact English and Thai text of `MSG-P4-002`, the refusal the access guard returns. |
| `Recovery Workbench Users Roles and Permissions v3.xlsx` | `02 Business architecture and process` | Defines `RW-TRIBE` (the actor), `RW-PLATADM` (pipeline) and `RW-REFADM` (the negative access test role, which holds no Case record right). |
| `Recovery Workbench Security and Access Design v2.docx` | `05 Technical architecture` | Explains the ACE sign-in and access check that the recovery module reuses, and the recovery roles and permissions held as data. |
| `Recovery Workbench Environment and Deployment Design v2.docx` | `05 Technical architecture` | Records the module set-up under `DL05` and lists "Module boundary" as pipeline gate 6. |
| `Recovery Workbench Definition of Ready and Done v3.docx` | `09 Testing and quality` | The definition of done includes the nine pipeline gates, one of which is the module boundary; also the rule that a story touches one module or needs the other module's code owner. |

### C. Tests, delivery and status records

| Document | Folder | Why it is connected |
|---|---|---|
| `Recovery Workbench Test Cases v5.xlsx` | `09 Testing and quality` | The eight `TC-TE-001-01` to `08` cases, with full Given/When/Then, level, data and regression flag. |
| `Recovery Workbench Regression Suite v5.xlsx` | `09 Testing and quality` | Keeps `TC-TE-001-01` (boundary enforced) and `TC-TE-001-08` (access refusal) in the regression set. |
| `Recovery Workbench Requirements Traceability Matrix v4.xlsx` | `09 Testing and quality` | The `REQ-DRI-006` row linking the requirement to `RWB-E1-007`, `RWB-TE-001`, `RWB-TE-002` and selected test cases. |
| `Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx` | `04 User stories` | Holds the open defect on the `R-BND` / `BND-1` naming. |
| `Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx` | `11 Delivery and operations` | Places TE-001 at order 2, window 1, 2-13 November 2026, release E1, not critical path. |
| `Recovery Workbench Story Build Order v1.docx` | `11 Delivery and operations` | Repeats the order: #2, no dependency; TE-002, TE-003, TE-011 and TE-012 wait on it. |
| `Recovery Workbench Release Plan v3.xlsx` / `.pptx` | `11 Delivery and operations` | Lists "Recovery module folder, package and boundary test in the ACE repository" as a date-setting dependency for E1, 2 November, with the impact "The squads cannot merge into ACE". |
| `Recovery Workbench Dependency Map v2.xlsx` | `11 Delivery and operations` | `DEP-01`: due 2 November, owner ACE team, decision `DL05`, status Open. This is the delivery-side record of the same outcome. |
| `Recovery Workbench Risks Assumptions Issues and Dependencies v2.xlsx` | `11 Delivery and operations` | `R-03` "One squad's change holds the other's release" is mitigated by feature flags, code owners and the module boundary test (`DL04`, `DL37`). |
| `Recovery Workbench Team Start Pack v2.pptx` / `.html` | `12 Project communication` | Puts TE-001 and TE-002 in the Tech leads' 2-6 November column. |
| `Recovery Workbench Weekly Status Pack v2.pptx` | `12 Project communication` | Lists "Module folder, boundary test" in the next-week Epic 1 build. |

### D. Adjacent stories and enablers

| Document | Folder | Why it is connected |
|---|---|---|
| `RWB TE 002 Code owners for the recovery module v1.md`, `RWB TE 003 Types and contract tests from the API specification v1.md`, `RWB TE 011 PDPA lint for code tests and logs v1.md`, `RWB TE 012 Document storage containers v1.md` | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5` | The four direct dependents. TE-002 owns `architecture/recovery-modules.yaml` through `CODEOWNERS`; TE-003 relies on the generated packages being listed as shared so the boundary test allows them. |
| `RWB E1 007 Integration adapters for file loads and outbound files v1.md` | Same folder | BND-5's sanctioned file-client package (`recovery.integration.adapter`); shares `REQ-DRI-006`. |
| `RWB E1 020 Allocation and assignment engine v1 v1.md`, `RWB E1 027 Decision log writer v1 v1.md` | Same folder | The story names `recovery.casewf.allocation` and `recovery.decision.writer` as examples of extra published packages that must be listed in the map. |
| `RWB TE 013 Agent runtime client with fallback v1.md` | Same folder | BND-5's sanctioned INT-23 client for the enterprise model endpoint. |

**Two notes on completeness.** The hub's generic "Documents you will need" strip for every story also lists `Physical Schema v4`, `Logical Data Model and Data Dictionary v6`, `Source to Target Mapping v3`, `Reference Data and Lists of Values v3` and `Entity Relationship Diagram v3`. TE-001 explicitly reads and writes no business data, so those five are not build inputs here — the strip is a generic reading list, and it actually omits the Interface Specifications and the ADRs, which do matter. Separately, `Document Control Sheet v10` and `Document Index v11` list the versions and owners of the source documents but contain no TE-001 content; `Executive Presentation CTO v3` and `Project Deck v3` mention the modular-monolith decision (`DT08`) but not TE-001 by ID.

## Bottom line

TE-001 is a small story with a large blast radius: 19 folders, one map, one ArchUnit test class, one front-end rule file and one access guard. If it is late or wrong, TE-002, TE-003, TE-011, TE-012 and every recovery feature behind them are blocked. If it is right, the architecture stops being a convention and becomes a build gate. The only open story defect is a naming inconsistency; the **DEP-01 ownership question** — ACE team or TechX under `DL05` option B — is the one I would settle at kickoff.

<details><summary>Reasoning</summary>

Now, before final answer, let me double-check the exact folder path of the story file: "04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB TE 001 Recovery module folder and boundary test v1.md". Yes.

Let me also double-check the "Technical Enabler Stories v5.md" size/contents include TE-001; yes.

Let me verify "Build Notes Technical Enablers v1.md" Step 1-8 match. Yes.

Now, I want to make sure the UI block syntax is valid. Let's write it carefully:
- root = Stack([glance, flags, rules, issue])
- glance = Card("RWB-TE-001 at a glance", [facts])
- facts = KeyValue([{label: "Story key", value: "RWB-TE-001"}, ...])
- flags = Row([Badge("Must", "error"), Badge("Ready for build", "success"), Badge("E1 · 30 Nov 2026", "info"), Badge("Order 2 · 2–13 Nov", "neutral")])
- rules = Table(["Rule", "What it enforces"], [["BND-1", "..."], ...])
- issue = Callout("...", "warning", "Open story defect #3")

Is `Card` allowed to hold `KeyValue`? Yes, Card children Item[]; KeyValue is an Item. `Row` with Badges is an Item. Table is an Item. Callout is an Item.

Every name reachable from root: glance, flags, rules, issue, facts. Yes.

String quotes: use double quotes. No embedded double quotes unless escaped. Avoid quotes inside text or use single quotes? The syntax says strings "..."; I can use single quotes inside. For `"..common.api.."` in text, avoid or use backticks? Backticks are just characters. I'll avoid quotes.

Table rows: arrays of strings. Good.

Use `\n`? No.

Let me craft the block:

```openui-lang
root = Stack([glance, flags, rules, issue])
glance = Card("RWB-TE-001 at a glance", [facts])
facts = KeyValue([{label: "Story", value: "Recovery module folder and boundary test"}, {label: "Type", value: "Technical enabler (not a business feature)"}, {label: "Epic / release", value: "E1, 30 November 2026"}, {label: "Module", value: "P2 Integration, cross-cutting"}, {label: "Requirement", value: "REQ-DRI-006"}, {label: "Decision", value: "DL05, option B from 2 November 2026"}, {label: "Depends on", value: "None"}, {label: "Build slot", value: "Order 2 of 115, 2-13 November 2026"}])
flags = Row([Badge("Must", "error"), Badge("Ready for build", "success"), Badge("E1 · 30 Nov 2026", "info"), Badge("Not critical path", "neutral")])
rules = Table(["Rule", "What it enforces"], [["BND-1", "Recovery reaches collection only through collection's published packages"], ["BND-2", "Recovery reaches common only through common's published packages"], ["BND-3",

_[truncated]_

</details>

> **System** - 2026-11-04 12:18

Today's date is now: Wed Nov 04 2026

### User - 2026-11-04 12:18

RWB-E1-044
RWB-TE-001
RWB-E1-042
RWB-TE-002
RWB-TE-003
RWB-TE-005
RWB-TE-011
RWB-TE-012

i need to focus on these stories. all od these a retechnical document out of which we only need to focus on Recovery Workbench Project Hub v14.html this file and for explantion we can wander to other files. so exlpain to me these stories in simple langiage since i have Provided this docuemnt to these development teams and they are going to ask me questions about it

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

I’ll pull the eight stories out of the hub and cross-check them against the build notes, defects and build sequence so the explanations match what the teams will see.

<details><summary>Reasoning</summary>

We need answer: explain these 8 stories in simple language, since user will present hub to dev teams and answer questions. Use Project Hub v14 as primary source; can wander to other files for explanation. Need detailed but simple. Need probably read each story fully from hub, plus build notes. We have model. Stories:
RWB-E1-044 Database migrations versioned with parameterized schema names
RWB-TE-001 done
RWB-E1-042 Central configuration service and parameter catalog
RWB-TE-002 Code owners
RWB-TE-003 Types and contract tests from API spec
RWB-TE-005 Rule table test harness
RWB-TE-011 PDPA lint
RWB-TE-012 Document storage containers

We need explain each in plain language: what it is, why, what to build, key acceptance criteria, dependencies/order, terminology, likely developer questions, gotchas. Also connect them as a "first wave" foundation. Need focus on hub. Let's gather full story texts and build notes for each. We have TE-001. Need E1-044, E1-042, TE-002, TE-003, TE-005, TE-011, TE-012.

Let's query hub model for metadata, story sections, ACs, build steps, tests, preconditions, out of scope. Also Build Notes Technical Enablers for TE-002 etc, Build Notes Epic 1 for E1-044/E1-042. Let's extract concise structured data.

Let's write script to dump each story's full text/sections to files and print key sections. We'll use the hub model. Need find each story section. Use heading. Let's script.

Also check Story Defects for these keys (open defects), Build Sequence order, dependencies, tests count, RTM etc. Important for Q&A.

Let's first list metadata and section headings for each.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst keys=['RWB-E1-044','RWB-TE-001','RWB-E1-042','RWB-TE-002','RWB-TE-003','RWB-TE-005','RWB-TE-011','RWB-TE-012'];\nfor(const key of keys){\n  let found=null;\n  M.docs.forEach((d,di)=>d.secs.forEach((s,si)=>{ if(new RegExp('^'+key+'\\\\b').test(s.h.trim()) && !found) found={di,si,d,s}; }));\n  if(!found){console.log('\\n### '+key+' NOT FOUND');continue;}\n  const {di,si,d}=found;\n  let end=si+1;\n  while(end<d.secs.length && !/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[end].h.trim())) end++;\n  console.log('\\n\\n################ '+key+' ################');\n  console.log('doc:',d.folder+' / '+d.name,'| section',si,'to',end-1,'| sections',end-si);\n  for(let k=si;k<end;k++) console.log('['+k+'] '+d.secs[k].h+' ('+d.secs[k].t.length+' chars)');\n}\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\list8.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/list8.js
```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\list8.js\""}
```

```text


################ RWB-E1-044 ################
doc: 04 User stories / Recovery Workbench Build Notes Epic 1 v4 | section 424 to 431 | sections 8
[424] RWB-E1-044 Database migrations versioned with parameterized schema names (28 chars)
[425] Step 1 (826 chars)
[426] Step 2 (742 chars)
[427] Step 3 (745 chars)
[428] Step 4 (846 chars)
[429] Step 5 (821 chars)
[430] Step 6 (732 chars)
[431] Step 7 (714 chars)


################ RWB-TE-001 ################
doc: 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | section 1 to 9 | sections 9
[1] RWB-TE-001 Recovery module folder and boundary test (22 chars)
[2] Step 1 (921 chars)
[3] Step 2 (832 chars)
[4] Step 3 (842 chars)
[5] Step 4 (720 chars)
[6] Step 5 (804 chars)
[7] Step 6 (745 chars)
[8] Step 7 (758 chars)
[9] Step 8 (806 chars)


################ RWB-E1-042 ################
doc: 04 User stories / Recovery Workbench Build Notes Epic 1 v4 | section 403 to 413 | sections 11
[403] RWB-E1-042 Central configuration service and parameter catalog (28 chars)
[404] Step 1 (848 chars)
[405] Step 2 (781 chars)
[406] Step 3 (707 chars)
[407] Step 4 (784 chars)
[408] Step 5 (750 chars)
[409] Step 6 (768 chars)
[410] Step 7 (736 chars)
[411] Step 8 (825 chars)
[412] Step 9 (729 chars)
[413] Step 10 (747 chars)


################ RWB-TE-002 ################
doc: 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | section 10 to 17 | sections 8
[10] RWB-TE-002 Code owners for the recovery module (22 chars)
[11] Step 1 (893 chars)
[12] Step 2 (714 chars)
[13] Step 3 (789 chars)
[14] Step 4 (694 chars)
[15] Step 5 (705 chars)
[16] Step 6 (741 chars)
[17] Step 7 (733 chars)


################ RWB-TE-003 ################
doc: 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | section 18 to 26 | sections 9
[18] RWB-TE-003 Types and contract tests from the API specification (22 chars)
[19] Step 1 (775 chars)
[20] Step 2 (821 chars)
[21] Step 3 (761 chars)
[22] Step 4 (732 chars)
[23] Step 5 (847 chars)
[24] Step 6 (823 chars)
[25] Step 7 (868 chars)
[26] Step 8 (707 chars)


################ RWB-TE-005 ################
doc: 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | section 37 to 44 | sections 8
[37] RWB-TE-005 Rule table test harness (28 chars)
[38] Step 1 (848 chars)
[39] Step 2 (778 chars)
[40] Step 3 (852 chars)
[41] Step 4 (886 chars)
[42] Step 5 (839 chars)
[43] Step 6 (863 chars)
[44] Step 7 (770 chars)


################ RWB-
... truncated (3,258 chars total)
```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

It found build notes first, not canonical story. Need both. Build notes are useful. Need canonical stories in Technical Enabler Stories v5 and User Stories Epic 1 v7 / maybe E1-044/E1-042 in Epic 1 v7. Let me query all matching docs per key.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst keys=['RWB-E1-044','RWB-TE-001','RWB-E1-042','RWB-TE-002','RWB-TE-003','RWB-TE-005','RWB-TE-011','RWB-TE-012'];\nfor(const key of keys){\n  console.log('\\n\\n################ '+key+' ################');\n  M.docs.forEach((d,di)=>{\n    d.secs.forEach((s,si)=>{\n      if(new RegExp('^'+key+'\\\\b').test(s.h.trim())){\n        let end=si+1;\n        while(end<d.secs.length && !/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[end].h.trim())) end++;\n        console.log('doc',di,d.folder+' / '+d.name,'| sec',si,'-',end-1,'|',end-si,'sections | first len',s.t.length);\n      }\n    });\n  });\n}\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\list8all.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/list8all.js
```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\list8all.js\""}
```

```text


################ RWB-E1-044 ################
doc 73 04 User stories / Recovery Workbench Build Notes Epic 1 v4 | sec 424 - 431 | 8 sections | first len 28
doc 82 04 User stories / Recovery Workbench User Stories Epic 1 v7 | sec 841 - 860 | 20 sections | first len 540


################ RWB-TE-001 ################
doc 75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sec 1 - 9 | 9 sections | first len 22
doc 80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sec 1 - 20 | 20 sections | first len 410


################ RWB-E1-042 ################
doc 73 04 User stories / Recovery Workbench Build Notes Epic 1 v4 | sec 403 - 413 | 11 sections | first len 28
doc 82 04 User stories / Recovery Workbench User Stories Epic 1 v7 | sec 801 - 820 | 20 sections | first len 514


################ RWB-TE-002 ################
doc 75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sec 10 - 17 | 8 sections | first len 22
doc 80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sec 21 - 40 | 20 sections | first len 418


################ RWB-TE-003 ################
doc 75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sec 18 - 26 | 9 sections | first len 22
doc 80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sec 41 - 60 | 20 sections | first len 401


################ RWB-TE-005 ################
doc 75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sec 37 - 44 | 8 sections | first len 28
doc 80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sec 81 - 100 | 20 sections | first len 461


################ RWB-TE-011 ################
doc 75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sec 95 - 102 | 8 sections | first len 22
doc 80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sec 201 - 220 | 20 sections | first len 401


################ RWB-TE-012 ################
doc 75 04 User stories / Recovery Workbench Build Notes Technical Enablers v1 | sec 103 - 110 | 8 sections | first len 23
doc 80 04 User stories / Recovery Workbench Technical Enabler Stories v5 | sec 221 - 240 | 20 sections | first len 402

```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Need print canonical stories. Let me dump each story (E1-044 and E1-042 from doc 82; TE from doc 80) into files. Print key sections: metadata, 1 story, 2 rationale, 3 preconditions, 4 flow, 5 exceptions, 7 AC, 8 rules, 12 contract, 13 solution, 14 messages, 16 tests, 17 guardrails, 18 traceability, 19 out of scope. This is a lot for 8 stories. We can summarize from full text, but need read. Let's dump each to a file, then read selectively.

Also build notes for each. And story defects. Let's generate one consolidated file per story with canonical + build notes. Then read.

Let's write script to dump to temp files.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst specs=[\n ['RWB-E1-044',82,841],\n ['RWB-E1-042',82,801],\n ['RWB-TE-002',80,21],\n ['RWB-TE-003',80,41],\n ['RWB-TE-005',80,81],\n ['RWB-TE-011',80,201],\n ['RWB-TE-012',80,221],\n ['RWB-TE-001',80,1],\n];\nfor(const [key,di,si] of specs){\n  const d=M.docs[di];\n  let end=si+1;\n  while(end<d.secs.length && !/^RWB-[A-Z]{1,3}\\d?-\\d{3}\\s/.test(d.secs[end].h.trim())) end++;\n  let out='';\n  for(let k=si;k<end;k++){ out+='\\n########## ['+k+'] '+d.secs[k].h+' ##########\\n'+d.secs[k].t+'\\n'; }\n  fs.writeFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/story_'+key+'.txt',out);\n  console.log(key, out.length);\n}\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\dump8.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/dump8.js
```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\dump8.js\""}
```

```text
RWB-E1-044 18083
RWB-E1-042 20056
RWB-TE-002 13336
RWB-TE-003 15088
RWB-TE-005 16271
RWB-TE-011 16184
RWB-TE-012 19307
RWB-TE-001 15341

```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now read each. Start E1-044 full.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-E1-044.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-E1-044.txt, lines 1-268
1: 
2: ########## [841] RWB-E1-044 Database migrations versioned with parameterized schema names ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-E1-044 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P3 Case and workflow |
8: | Feature | FEAT-CWC-24 Run versioned migrations with parameterized schema names |
9: | Requirement IDs | REQ-RDF-001, REQ-RDF-014 |
10: | BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Epic 2, section 4; Business Requirements Program, section 5.1 |
11: | L3 process | All recovery processes |
12: | Decision | None |
13: | Priority | Must |
14: | Depends on | None |
15: | Status | Ready for build |
16: 
17: ########## [842] 1. Story ##########
18: As a **platform administrator (RW-PLATADM)**, I want **every schema change applied by a versioned Flyway migration, one migration per story, forward-only in PROD, with the schema name taken from a parameter**, so that **the database in every environment is the sum of known migrations and nothing else**.
19: 
20: ########## [843] 2. Business rationale ##########
21: The recovery tables share the ACE database with the collection module, and two squads change it from one repository (DT07, DT08). A column added by hand in one environment makes SIT and UAT test a database that PROD does not have. This story makes every change a numbered, checksummed migration with no schema name written in the file, and fails the pipeline on drift. It supports REQ-RDF-001 (the 14 data products held in the ACE database) and REQ-RDF-014 (stage 2 tables exist before the first treatment goes live). The measure is zero schema differences between a clean build and each environment at every release.
22: 
23: ########## [844] 3. Preconditions ##########
24: - The recovery tables are defined in the Logical Data Model and Recovery Workbench Physical Schema v4.sql.
25: - The recovery module folder and boundary test exist (RWB-TE-001).
26: - Each environment has a database account for migrations and a read-only account for the drift check, held in the key store (NFR-052).
27: - The schema parameter `RWB_SCHEMA` is set per environment (DEV, SIT, UAT, PROD). Assumed value `recovery` in every environment, as in Recovery Workbench Physical Schema v4.sql.
28: - Deployment slots are booked (DL35).
29: 
30: ########## [845] 4. Flow ##########
31: 1. Developer: adds one migratio
... truncated (19,405 chars total)
```

### Assistant - 2026-11-04 12:18 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Key open point DL42: migration naming rule conflict. This is important. The build step says open point, logged as DL42 for ACE tech lead, needed by 2 Nov. 51 other stories use four other rules, 30 use V<epic>_<story>__<name>.sql with ${recoverySchema}. Until ruling, lint reports but doesn't fail build. This is a big Q&A item.

Need check story defect for E1-044. Let's query defects for all 8. Also build sequence order/deps. Later.

Read E1-042.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-E1-042.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-E1-042.txt, lines 1-306
1: 
2: ########## [801] RWB-E1-042 Central configuration service and parameter catalog ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-E1-042 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P3 Case and workflow |
8: | Feature | FEAT-CWC-22 Hold the parameter catalog and configuration service |
9: | Requirement IDs | REQ-DRI-010 |
10: | BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
11: | L3 process | 14 Set strategy, policy and decision rules |
12: | Decision | D6 entry |
13: | Priority | Must |
14: | Depends on | RWB-E1-044 |
15: | Status | Ready for build |
16: 
17: ########## [802] 1. Story ##########
18: As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.
19: 
20: ########## [803] 2. Business rationale ##########
21: Thresholds such as the 90-day entry point are written into code and spreadsheets today, so a change needs a release and nobody can say who owns a value. This story holds every parameter definition in a catalog with an owner and a default, holds business values as approved, dated versions per environment, serves them to every engine at run time, and fails the build when code carries a literal business value or reads a parameter the catalog does not list. It meets REQ-DRI-010 and puts Principle 1 (DT02) into the build pipeline.
22: 
23: ########## [804] 3. Preconditions ##########
24: - RWB-E1-044 is done: the recovery schema exists in each environment.
25: - The catalog seed file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, with the Epic 1 entries, including `case.entry.dpd` (default 90; DL16), `refdata.cache.ttl-seconds` (default 300; DL11) and `caselist.export.maxrows` (default 10000; DL11).
26: - The ACE secret store holds secrets per environment; the catalog lists them and never holds their values.
27: - Loaders hold Reference data C (RW-COE, RW-REFADM). Approvers hold Reference data A: the parameter owner, and RW-RISK where a threshold or a limit moves (assumed grant; DL01).
28: - The build pipeline runs the checks of this story on every pull request (DL37 code owners).
29: 
30: #########
... truncated (21,568 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

E1-042 important: config service, parameter catalog, magic number check, catalog completeness. Note migration file naming `V042_1__parameter_catalog.sql` conflicts with E1-044's single rising number rule! This is exactly the DL42 conflict. Good Q&A.

Also note E1-042 depends on E1-044. Build sequence says order 3 after E1-044. Good.

Read TE-002.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-TE-002.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-TE-002.txt, lines 1-209
1: 
2: ########## [21] RWB-TE-002 Code owners for the recovery module ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-TE-002 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P2 Integration |
8: | Feature | None |
9: | Requirement IDs | REQ-DRI-006 |
10: | BRD section | Business Requirements Program, section 7 (constraints Built on ACE and Modular monolith) |
11: | L3 process | All recovery processes |
12: | Decision | DL37 |
13: | Priority | Must |
14: | Depends on | RWB-TE-001 |
15: | Status | Ready for build |
16: 
17: ########## [22] 1. Story ##########
18: As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.
19: 
20: ########## [23] 2. Business rationale ##########
21: The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.
22: 
23: ########## [24] 3. Preconditions ##########
24: - RWB-TE-001 is done: the recovery folders and the module map exist.
25: - The repository host supports a code owners file (GitHub format assumed, as ACE uses GitHub Copilot under DL32).
26: - The teams exist in the repository host: TechX recovery tech leads and the ACE team. Names assumed until DL37 and DL36 are answered: `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`.
27: - The repository administrator of the ACE team can set the branch rule on main.
28: 
29: ########## [25] 4. Flow ##########
30: 1. Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.
31: 2. Squad member: adds the code owners validation step to the pull request pipeline
... truncated (14,363 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

TE-002 straightforward. 1 point. Requires repo admin (ACE) to set branch rule. Test cases 6 pull requests in test branch. Note TC-08 access is odd: no endpoint, MSG-P4-002 not shown. That may be a defect? Check Story Defects. We'll query.

Read TE-003.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-TE-003.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-TE-003.txt, lines 1-234
1: 
2: ########## [41] RWB-TE-003 Types and contract tests from the API specification ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-TE-003 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P2 Integration |
8: | Feature | None |
9: | Requirement IDs | REQ-DRI-007, REQ-ACA-003 |
10: | BRD section | Business Requirements Program, section 5.2 and section 5.4 |
11: | L3 process | All recovery processes |
12: | Decision | None |
13: | Priority | Must |
14: | Depends on | RWB-TE-001 |
15: | Status | Ready for build |
16: 
17: ########## [42] 1. Story ##########
18: As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.
19: 
20: ########## [43] 2. Business rationale ##########
21: The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.
22: 
23: ########## [44] 3. Preconditions ##########
24: - RWB-TE-001 is done: the recovery folders and the boundary test exist; the generated packages are listed in the module map as shared.
25: - The API specification is held in the repository at `api/recovery-api.yaml`, base path /api/recovery/v1, with x-module, x-capability and x-first-release on every operation.
26: - The permission matrix seed (roles.txt, loaded as the role and permission tables by RWB-E1-037) is available to tests.
27: - The build property `rwb.release` names the release being built: E1 for 30 November 2026.
28: 
29: ########## [45] 4. Flow ##########
30: 1. Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the 
... truncated (16,240 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

TE-003 important: 79 operations, generation, contract test, access test, report, release property. AC1 warnAt; AC5 getAdminJobs; AC6 postQueuesQueueidPlacements E2 pending. Note precondition "permission matrix seed (roles.txt, loaded by E1-037)". Good.

Read TE-005.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-TE-005.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-TE-005.txt, lines 1-267
1: 
2: ########## [81] RWB-TE-005 Rule table test harness ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-TE-005 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P3 Case and workflow |
8: | Feature | None (technical enabler) |
9: | Requirement IDs | REQ-CWC-014, REQ-CWC-013 |
10: | BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, section 5.3 |
11: | L3 process | All recovery processes |
12: | Decision | None |
13: | Priority | Must |
14: | Depends on | RWB-E1-044 |
15: | Status | Ready for build |
16: 
17: ########## [82] 1. Story ##########
18: As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.
19: 
20: ########## [83] 2. Business rationale ##########
21: The routing logic is 448 rules in ten route sets, held as data (ADR-004). A wrong condition or owner in one row moves every case that reaches it, and the bank has no test that proves a row does what its owner expects. Every rule row already names a test case (`rule_row.test_case_id`). This story runs those test cases on every rule load and in every build, and marks a version failed when any test fails. It meets REQ-CWC-014 and REQ-CWC-013. The measure is that every rule row in force has a passing test with its rule ID.
22: 
23: ########## [84] 3. Preconditions ##########
24: - RWB-E1-044 is done: migrations run with the parameterized schema.
25: - The rules component evaluates a route set as a decision table with hit policy Unique (ADR-004).
26: - The rule load template (RWB-E1-029) carries a Tests sheet with one test case per rule row.
27: - Rule rows exist with a `test_case_id` for each row (DF-REF-015, required).
28: - The Restructure route set is loaded in SIT with its 37 rows, R-RES-01 to R-RES-37.
29: - The loader holds RW-COE (Rules and parameters C).
30: 
31: ########## [85] 4. Flow ##########
32: 1. Center of excellence analyst: loads a rule version through `POST /admin/rule-versions` with the rules and the Tests sheet.
33: 2. P4 load handler: stores the rule rows and calls `RuleTableHarness.run(routeSet, ruleVersion)`.
34: 3. Harness: reads the rule rows of the version and their test cases.
35: 4. Harness: for each test case, bu
... truncated (17,588 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

TE-005: 448 rules in 10 route sets, Restructure 37 rows; harness runs per rule row on load and every build; unique hit policy; pass rule exactly one row hits, named row, expected to state/owner/timer. Build runs 448 tests. Note migration name `V<next>__rwb_te_005_rule_test_case.sql` — again migration naming conflict (uses `<next>`). Good.

Read TE-011.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-TE-011.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-TE-011.txt, lines 1-254
1: 
2: ########## [201] RWB-TE-011 PDPA lint for code, tests and logs ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-TE-011 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P2 Integration |
8: | Feature | None |
9: | Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
10: | BRD section | Business Requirements Program, section 6.7 and section 6.9 |
11: | L3 process | All recovery processes |
12: | Decision | None |
13: | Priority | Must |
14: | Depends on | RWB-TE-001 |
15: | Status | Ready for build |
16: 
17: ########## [202] 1. Story ##########
18: As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.
19: 
20: ########## [203] 2. Business rationale ##########
21: Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero.
22: 
23: ########## [204] 3. Preconditions ##########
24: - RWB-TE-001 is done: the recovery folders and the pipeline checks exist.
25: - The data dictionary marks each personal field (the `is_personal` column of the metadata table sys_fields in the schema, and `x-personal-data: true` in the API specification).
26: - Synthetic test data uses the prefix "SYN-" for every value placed in a personal field (assumed convention of RWB-E1-065).
27: - The masking helper of the common module is available for the rare log line that must name a record (assumed published as part of the common module's PII logging interface).
28: 
29: ########## [205] 4. Flow ##########
30: 1. Build: reads the personal fields from the sys_fields seed and the API specification.
31: 2. Build: generates the lint rule set from the field list: Java getter names, entity class 
... truncated (17,436 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

TE-011: PDPA lint. Important details: personal fields include first_name, last_name, cif_no, id_no_token, date_of_birth, value_token, summary, field_value, vulnerable_flag, deceased_flag, bankruptcy_flag (data section). The background says 8 fields. Rules codes. Synthetic prefix "SYN-" assumed. Allow list with owner/reason/expiry. No value printed. Access test is code-owner approval, no endpoint. Good.

Read TE-012.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\story_RWB-TE-012.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\story_RWB-TE-012.txt, lines 1-279
1: 
2: ########## [221] RWB-TE-012 Document storage containers ##########
3: | Item | Value |
4: |---|---|
5: | Story key | RWB-TE-012 |
6: | Epic | E1, release 30 November 2026 |
7: | Module | P5 Document hub |
8: | Feature | None |
9: | Requirement IDs | REQ-DCM-003, REQ-DCM-002 |
10: | BRD section | Business Requirements Program, section 5.5 |
11: | L3 process | 13 Manage documents and correspondence |
12: | Decision | DL27 |
13: | Priority | Must |
14: | Depends on | RWB-TE-001 |
15: | Status | Ready for build |
16: 
17: ########## [222] 1. Story ##########
18: As a **platform administrator**, I want **blob containers for documents, with a write-once container for legal types, reached by managed identity**, so that **legal documents cannot be overwritten**.
19: 
20: ########## [223] 2. Business rationale ##########
21: Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. This story sets up the storage that the document store (RWB-E1-024), the intake (RWB-E1-057) and the malware scan (RWB-E1-041) write to: an intake container, a standard container with version history, a write-once container whose immutability policy refuses any overwrite or delete inside its retention period, and a quarantine container, all reached only by managed identity. It meets REQ-DCM-003 and REQ-DCM-002 and is the storage behind control CTL-12 and the storage pattern recommended under DL27.
22: 
23: ########## [224] 3. Preconditions ##########
24: - RWB-TE-001 (recovery module folder and boundary test) is done.
25: - The ACE storage pattern is used (DL27, option A recommended): one storage account per environment in the SCB tenant with a private endpoint.
26: - The managed identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR and RWB-PROD-SY-OCR exist, and the ACE service has its own managed identity in each environment.
27: - The retention period of the write-once policy is assumed at 3,650 days (10 years), matching the class LEGAL10Y, until the bank retention schedule is supplied (DL26).
28: - The infrastructure pipeline of the ACE repository can apply storage templates to DEV and SIT.
29: 
30: ########## [225] 4. Flow ##########
31: 1. Platform administrator: applies the infrastructure template for the environment, which sets the storage account (shared key access off, public n
... truncated (20,684 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

TE-012: storage containers, write-once legal, managed identity, readiness. Important: no endpoint of its own; supports E1-024/026/041/057. Retention 3650 days assumed DL26; soft delete 30 days assumed DL27; policy locked in PROD, unlocked lower. Good.

Need read TE-001 story (already know), but maybe for this answer we need concise. We have.

Need E1-044/E1-042 build notes for plain explanation and potential build step details. But story sections sufficient. Need check open defects for all 8, build order, dependencies, points, test counts. Let's query:

- Story Defects rows for keys.
- Build Sequence rows for keys (order, module, type, priority, depends, window, dates, release, critical path).
- Technical Enabler Stories header for points? It doesn't have points in table; maybe the "Tab Stories" has points? Let's check. TE-002 story says 1 point. Others may not. Build Sequence has no points. We can skip points except TE-002.

- Dependencies map rows for these? TE-005 depends E1-044; TE-012 depends TE-001; etc. Build sequence.

- RTM rows for requirements maybe.

- Test case counts: E1-044 10, E1-042 12, TE-002 8, TE-003 9, TE-005 9, TE-011 11, TE-012 13, TE-001 8.

- Open defects: query.

Let's run.

</details>

**Tool `write`** - completed

```json
{"content": "const fs=require('fs');\nconst M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));\nconst keys=['RWB-E1-044','RWB-TE-001','RWB-E1-042','RWB-TE-002','RWB-TE-003','RWB-TE-005','RWB-TE-011','RWB-TE-012'];\nfunction docIdx(re){return M.docs.findIndex(d=>d.name.match(re));}\nconsole.log('=== BUILD SEQUENCE ===');\nlet i=docIdx(/Build Sequence Epic 1/);\nM.docs[i].secs[0].t.split('\\n').filter(l=>keys.some(k=>l.includes(k))).forEach(l=>console.log(l));\nconsole.log('\\n=== STORY DEFECTS ===');\ni=docIdx(/Story Defects/);\nM.docs[i].secs[0].t.split('\\n').filter(l=>keys.some(k=>l.startsWith(k+' |')||l.includes('| '+k+' |'))).forEach(l=>console.log(l));\nconsole.log('\\n=== RTM ===');\ni=docIdx(/Requirements Traceability Matrix/);\nM.docs[i].secs[0].t.split('\\n').filter(l=>keys.some(k=>l.includes(k))).forEach(l=>console.log(l));\nconsole.log('\\n=== TEST CASE COUNTS ===');\nfor(const k of keys){\n  const re=new RegExp('^'+k+'-\\\\d{2}\\\\b');\n  let n=0;\n  const tcIdx=docIdx(/Test Cases v5/);\n  M.docs[tcIdx].secs.forEach(s=>{ s.t.split('\\n').forEach(l=>{ if(l.startsWith('TC-') && l.includes('| '+k+' |')) n++; }); });\n  console.log(k,n);\n}\n", "path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query8.js"}
```

```text
Created file successfully: C:/Users/SahilMore/AppData/Local/Temp/opencode/query8.js
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

**Tool `shell`** - completed

```json
{"command": "node \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\query8.js\""}
```

```text
=== BUILD SEQUENCE ===
1 | RWB-E1-044 | Database migrations versioned with parameterized schema names | P3 | Enabler | Must |  | Window 1 | 2 Nov to 13 Nov | E1 | Yes
2 | RWB-TE-001 | Recovery module folder and boundary test | P2 | Enabler | Must |  | Window 1 | 2 Nov to 13 Nov | E1
3 | RWB-E1-042 | Central configuration service and parameter catalog | P3 | Enabler | Must | RWB-E1-044 | Window 1 | 2 Nov to 13 Nov | E1 | Yes
4 | RWB-TE-002 | Code owners for the recovery module | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
5 | RWB-TE-003 | Types and contract tests from the API specification | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
6 | RWB-TE-005 | Rule table test harness | P3 | Enabler | Must | RWB-E1-044 | Window 1 | 2 Nov to 13 Nov | E1
7 | RWB-TE-011 | PDPA lint for code, tests and logs | P2 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
8 | RWB-TE-012 | Document storage containers | P5 | Enabler | Must | RWB-TE-001 | Window 1 | 2 Nov to 13 Nov | E1
9 | RWB-E1-043 | Reference data service with versioned tables | P3 | Enabler | Must | RWB-E1-042, RWB-E1-044 | Window 1 | 2 Nov to 13 Nov | E1 | Yes
10 | RWB-E1-001 | Recovery tables for the 14 data products | P1 | User story | Must | RWB-E1-044, RWB-E1-043 | Window 1 | 2 Nov to 13 Nov | E1 | Yes
22 | RWB-E1-017 | Retention and archive rule for the data store | P1 | User story | Should | RWB-E1-001, RWB-E1-043, RWB-TE-012, RWB-E1-064 | Window 2 | 16 Nov to 27 Nov | E1
26 | RWB-TE-007 | Scheduled jobs on Quartz | P3 | Enabler | Must | RWB-E1-044, RWB-E1-056 | Window 2 | 16 Nov to 27 Nov | E1
28 | RWB-TE-006 | Outbox and retry for outbound work | P2 | Enabler | Must | RWB-E1-044, RWB-E1-027, RWB-E1-007 | Window 2 | 16 Nov to 27 Nov | E1
37 | RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | P3 | Enabler | Must | RWB-E1-042, RWB-E1-043, RWB-E1-012 | Window 2 | 16 Nov to 27 Nov | E1
40 | RWB-E1-018 | Case ID issuance and case record v1 | P3 | User story | Must | RWB-E1-016, RWB-E1-027, RWB-E1-042 | Window 2 | 16 Nov to 27 Nov | E1 | Yes
44 | RWB-E1-024 | Document store and index | P5 | User story | Must | RWB-E1-027, RWB-E1-018, RWB-E1-025, RWB-TE-012, RWB-E1-001 | Window 2 | 16 Nov to 27 Nov | E1
51 | RWB-E1-049 | OCR pipeline on the Workbench document hub | P5 | User story | Must | RWB-TE-012, RWB-E1-024, RWB-E1-045 | Window 2 | 16 Nov to 27 Nov | E1
64 | RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | P5 | 
... truncated (11,303 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Great. Open defects list is important. Note for E1-044: multiple open defects including DL42 naming conflict. E1-042: X10 before X9 and test count; AC4 contradiction. TE-002 BR4 vs section 10. TE-003 step lint vs BR2; Done when pending conflict. TE-005 state/read contradiction. TE-011 step name variants; AC3 generated test identifier. TE-012 X9 order. TE-001 R-BND.

Need explain these in simple language and likely Q&A. The user is presenting to dev teams. We should distill:
- What each story delivers.
- Why it matters.
- What devs actually build.
- How to demo/accept.
- Gotchas/open questions.
- How the 8 fit together.

Need perhaps read build notes for E1-044 and E1-042 to understand step-by-step. But stories have build steps. Build notes might clarify "what this means". Could be useful for simple language. Let's read E1-044 build notes 8 steps (short) and E1-042 10 steps. Also TE-002 etc build notes we already saw in hub lines but maybe not all. We can use story sections enough. But user wants "simple language" for teams; build notes are literally "what this means". Let's read E1-044 and E1-042 build notes.

</details>

**Tool `read`** - error

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001_sections.txt", "limit": 10}
```

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));for(const [k,di,si,en] of [['E1-044',73,424,431],['E1-042',73,403,413]]){let out='';for(let x=si;x<=en;x++)out+='\\n### '+M.docs[di].secs[x].h+'\\n'+M.docs[di].secs[x].t+'\\n';fs.writeFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/notes_'+k+'.txt',out);console.log(k,out.length)}\""}
```

```text
E1-044 5624
E1-042 7903

```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Read notes.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\notes_E1-044.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\notes_E1-044.txt, lines 1-38
1: 
2: ### RWB-E1-044 Database migrations versioned with parameterized schema names
3: Module: P3 Case and workflow
4: 
5: ### Step 1
6: **In the story.** Developer: adds one migration file for the story under `recovery/src/main/resources/db/migration/recovery/`, named `V<number>__<description>.sql`, with the header line `-- Story: <story key>`.
7: 
8: A developer does this by hand, once per story that changes the database. Put the file in recovery/src/main/resources/db/migration/recovery, name it V<number>__<description>.sql, and make the first line a comment reading "-- Story: <story key>". A migration is a SQL file Flyway applies once and then remembers, so the database of any environment is the sum of the migrations applied to it. One story gets one file, and no two files may carry the same story key. Write no schema name in the SQL: use the ${schema} placeholder, which Flyway replaces with the value of RWB_SCHEMA for the environment it is running in.
9: 
10: ### Step 2
11: **In the story.** Pipeline: runs the migration lint: no literal schema name, exactly one story key per file, no story key in two files, no undo file.
12: 
13: The build does this, not a reviewer. Build MigrationLint as a build step with four refusals: a literal schema name written before a table name, a file with no story key in its header, the same story key in two files, and any file whose name begins with U, which would be an undo migration. For the literal name check, compare against every object name in sys_objects. Each failure stops the build with MSG-P3-016 and names the file, and the line as well for a literal schema name. Test each refusal with its own fixture file. The lint is the reason a wrong file never reaches an environment.
14: 
15: ### Step 3
16: **In the story.** Pipeline: starts a clean PostgreSQL container and applies all migrations with `RWB_SCHEMA` set.
17: 
18: This runs in the pipeline with no person watching. Start an empty PostgreSQL container, set RWB_SCHEMA, and let Flyway apply every migration from the first to the newest. The result is the schema the repository describes and nothing else, which is why it can be compared against a real environment in the next step. It also proves the placeholder works: the same files build a schema named rwb_case here and in SIT, from files that are byte for byte identical in both runs. Use a clean container every time, because a conta
... truncated (5,852 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\notes_E1-042.txt"}
```

```text
Read file C:\Users\SahilMore\AppData\Local\Temp\opencode\notes_E1-042.txt, lines 1-53
1: 
2: ### RWB-E1-042 Central configuration service and parameter catalog
3: Module: P3 Case and workflow
4: 
5: ### Step 1
6: **In the story.** Squad member: adds a parameter to `config/parameter-catalog.csv` with key, kind, type, unit, range, default, scope, required, owner role, environments and used by; the pull request is reviewed by the owner.
7: 
8: A squad member does this as a code change. The parameter is a line added to config/parameter-catalog.csv with key, kind, type, unit, range, default, scope, required flag, owner role, environments and the packages that use it. The pull request goes to the owner named on the line for review, following the code owner rule. Your work is the column set, because two build tools and a generated migration read this file. An environment setting and a secret each get a catalog line as well; the value of a secret lives only in the ACE secret store and never in the file. The Epic 1 lines include case.entry.dpd with default 90.
9: 
10: ### Step 2
11: **In the story.** Build: generates the `ParameterKeys` class from the catalog file; code reads a value only through ParameterService with a generated key.
12: 
13: The build does this, not a developer by hand. ParameterKeysGenerator reads config/parameter-catalog.csv and writes the ParameterKeys class, giving each catalog line a typed constant such as ParameterKeys.CASE_ENTRY_DPD of type ParameterKey<Integer>. Application code then reads a value only through ParameterService.get with one of those constants and a business date. Because the constants are generated, a key the catalog does not list will not compile, and the type on the key stops an integer parameter being read as text. Wire the generator into the build so the class is written again whenever the catalog file changes.
14: 
15: ### Step 3
16: **In the story.** Build: runs the magic number check over the recovery packages and the catalog completeness check.
17: 
18: Both checks run in the pipeline on every pull request. RwbMagicNumberCheck scans the recovery packages for numeric and text business literals; 0, 1, -1 and test code are allowed. When it finds one it fails the build and names the file, the line, and any catalog key whose default equals that literal, so a hard-coded 90 points at case.entry.dpd. CatalogCompletenessCheck compares the keys that services read through ParameterService with the lines in the catalog file an
... truncated (8,191 chars total)
```

### Assistant - 2026-11-04 12:19 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Good. Note E1-042 migration files are V042_1 and V042_2, violating E1-044's V<number> and one file per story. This is the DL42 open point. Important.

Need build notes for TE-002/003/005/011/012 maybe enough in story. But for simple language, story is fine. Need perhaps read TE-002 notes? We saw hub inline earlier; but we can use story.

Need understand how these 8 fit: foundation wave:
1. E1-044: migration baseline (order 1, critical path)
2. TE-001: module folders/boundary (order 2)
3. E1-042: config/parameter service (order 3, critical path)
4. TE-002: code owners (order 4)
5. TE-003: generated types/contract tests (order 5)
6. TE-005: rule table harness (order 6)
7. TE-011: PDPA lint (order 7)
8. TE-012: document storage containers (order 8)

All Window 1, 2-13 Nov, E1. E1-044 and E1-042 critical path. Then E1-043 reference data (order 9) depends on E1-042/E1-044; E1-001 tables (order 10) depends. So this set is the "platform foundation" before business features. Need explain that to teams: these are not features, they are the guardrails and plumbing; everything else depends on them.

Need explain in simple language with analogies:
- E1-044 = the filing system for database changes. Every schema change is a numbered, checksummed SQL file; no hand edits; schema name is a variable; drift check; forward-only in PROD. Like a version-controlled recipe book; the database must equal the recipe book.
- TE-001 = the office layout and walls. 19 rooms (modules), each with a front desk (api) and a back office (internal); a rulebook (module map); a building inspector (ArchUnit) that fails the build if someone walks through a wall; front-end equivalent; access guard at the door.
- E1-042 = the settings cupboard. Every threshold, timer, limit, name is a catalog entry with owner, default, type, range, environment; code reads via ParameterService with generated keys; magic-number check; completeness check; versioned loads, second-person approval, effective date, rollback, secrets listed not served. Like a central control panel; no hard-coded 90.
- TE-002 = the sign-off rule for each room. CODEOWNERS maps paths to teams; branch rule requires code owner approval; author can't self-approve; new commit dismisses approval; validation step catches bad team/path.
- TE-003 = the contract between the menu and the kitchen. OpenAPI file is the single source; generate Spring interfaces and TS types/client; contract test every implemented operation; access test every operation; pend

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "node -e \"const fs=require('fs');const M=JSON.parse(fs.readFileSync('C:/Users/SahilMore/AppData/Local/Temp/opencode/hub_model.json','utf8'));const keys=['RWB-E1-044','RWB-TE-001','RWB-E1-042','RWB-TE-002','RWB-TE-003','RWB-TE-005','RWB-TE-011','RWB-TE-012'];const i=M.docs.findIndex(d=>/Regression Suite/.test(d.name));for(const k of keys){const rows=M.docs[i].secs[0].t.split('\\n').filter(l=>l.includes('| '+k+' |'));console.log('\\n'+k+' ('+rows.length+'):');rows.forEach(r=>console.log(r.split('|').slice(0,8).join('|')));}\""}
```

```text

RWB-E1-044 (2):
TC-E1-044-01 | RWB-E1-044 | E1 | P3 | AC1 | Migration applied | System | The migration applies once; Its version 12 and its checksum are recorded in "flyway_schema_history_recovery"; A second deployment run applies nothing and changes no object 
TC-E1-044-10 | RWB-E1-044 | E1 | P3 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged 

RWB-TE-001 (2):
TC-TE-001-01 | RWB-TE-001 | E1 | P2 | AC1 | Boundary enforced | System | The boundary test fails the build; The build log names boundary rule BND-1, "SampleService" and "CollectorRepository" 
TC-TE-001-08 | RWB-TE-001 | E1 | P2 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged 

RWB-E1-042 (2):
TC-E1-042-01 | RWB-E1-042 | E1 | P3 | AC1 | Parameter read at run time | System | It uses 90 from the service, not a constant in code; The entry decision records parameter version 1 
TC-E1-042-12 | RWB-E1-042 | E1 | P3 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged 

RWB-TE-002 (2):
TC-TE-002-01 | RWB-TE-002 | E1 | P2 | AC1 | Review required | System | A TechX tech lead is required as reviewer; An approval from a squad member outside the team leaves the merge blocked 
TC-TE-002-08 | RWB-TE-002 | E1 | P2 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged 

RWB-TE-003 (2):
TC-TE-003-01 | RWB-TE-003 | E1 | P2 | AC1 | Types generated | System | The generated server model and the front end type for Timer both hold "warnAt"; The service and the front end compile against them 
TC-TE-003-09 | RWB-TE-003 | E1 | P2 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged 

RWB-TE-005 (2):
TC-TE-005-01 | RWB-TE-005 | E1 | P3 | AC1 | Every row tested | System | 37 tests run; Each test result names its rule ID and its test case ID; All 37 pass and the version state is "VALIDATED" 
TC-TE-005-09 | RWB-TE-005 | E1 | P3 | Access | A role without the right is refused with MSG-P4-002 | Access | Refused with MSG-P4-002; nothing changes; the refusal is logged 

RWB-TE-011 (2):
TC-TE-011-01 | RWB-TE-011 | E1 | P2 | AC1 | Log statement | System | The PDPA lint fails the build; The build log names rule 
... truncated (3,282 chars total)
```

### Assistant - 2026-11-04 12:20 | opencode-go/deepseek-v4.1-flash | build

I pulled all eight stories from the hub and cross-checked them against the build notes, the build sequence and the Story Defects workbook. The most important framing for your session:

**These are not eight features. They are the platform contract the rest of Epic 1 builds on.** Two are critical path, all eight are `Must`, and all eight sit in Window 1 (2–13 November 2026) for the 30 November release. None adds a new business screen.

```openui-lang
root = Stack([wave, map, note])
wave = Card("The foundation wave", [facts])
facts = KeyValue([{label: "Window", value: "Window 1, 2-13 November 2026"}, {label: "Release", value: "E1, 30 November 2026"}, {label: "Size", value: "8 stories, 80 test cases, all Must"}, {label: "Shape", value: "6 technical enablers + 2 enabler user stories"}, {label: "Critical path", value: "E1-044 and E1-042"}, {label: "Screens", value: "No new business screen in any of the eight"}])
map = Table(["#", "Story", "Plain-English job", "Module", "Depends on", "Critical path"], [["1", "RWB-E1-044", "Numbered database changes, one schema variable, drift check", "P3", "None", "Yes"], ["2", "RWB-TE-001", "19 module folders plus a build-time boundary test", "P2", "None", "No"], ["3", "RWB-E1-042", "One parameter catalog and configuration service", "P3", "E1-044", "Yes"], ["4", "RWB-TE-002", "Code owners and a branch rule that blocks merges", "P2", "TE-001", "No"], ["5", "RWB-TE-003", "Generate types and contract/access tests from OpenAPI", "P2", "TE-001", "No"], ["6", "RWB-TE-005", "A test harness for all 448 rule rows", "P3", "E1-044", "No"], ["7", "RWB-TE-011", "A PDPA lint for code, tests, logs and messages", "P2", "TE-001", "No"], ["8", "RWB-TE-012", "Four document containers, one write-once for legal", "P5", "TE-001", "No"]])
note = Callout("Read these as one foundation, not eight projects. E1-044 and TE-001 come first; E1-042 and TE-005 follow E1-044; TE-002, TE-003, TE-011 and TE-012 follow TE-001.", "info", "How to frame the session")
```

## The one-sentence version of each story

| Story | In plain English |
|---|---|
| **RWB-E1-044** | Every database change is a numbered, fingerprinted SQL file. The schema name is a variable, not typed into the file. The pipeline checks that the real environment matches the files, and production only moves forward. |
| **RWB-TE-001** | Build 19 labelled rooms in the codebase, write a map of which rooms may talk to which, and install a building inspector that fails the build if someone walks through a wall. |
| **RWB-E1-042** | Put every threshold, limit, timer and name into one central control panel, so nobody hard-codes `90` again and every value has an owner and a version. |
| **RWB-TE-002** | Give every folder a named owning team, and make the repository block a merge until that team approves the change. |
| **RWB-TE-003** | Make the OpenAPI file the only menu: generate the Spring interfaces and React types from it, then test every endpoint against it and against its access right. |
| **RWB-TE-005** | Give every business-rule row its own exam, and refuse to let a rule version go live if any row fails its exam. |
| **RWB-TE-011** | Install a privacy leak detector that fails the build when code, tests, logs or error messages carry personal data. |
| **RWB-TE-012** | Set up four document containers, including one write-once cabinet for legal documents that cannot be overwritten or deleted. |

---

## 1. RWB-E1-044 — Database migrations versioned with parameterized schema names

**What it is.** A disciplined way to change the database. Every change is a numbered SQL file that Flyway applies once and remembers with a checksum. The schema name is supplied by the environment (`RWB_SCHEMA`), so the same file runs in DEV, SIT, UAT and PROD. The pipeline builds a clean database from the files and compares it with the real environment; any difference is “drift” and stops the deployment. PROD is forward-only.

**What the team builds.**
- `RecoveryFlywayConfig` with the settings in section 12: Flyway enabled, location `classpath:db/migration/recovery`, schemas and default schema `${RWB_SCHEMA}`, history table `flyway_schema_history_recovery`, `validate-on-migrate=true`, `out-of-order=false`, `clean-disabled=true`.
- The baseline migration `V1__rwb_e1_001_baseline.sql`, converted from Physical Schema v4: 43 tables, `${schema}` placeholder, no `SET search_path`, no seed rows.
- `MigrationLint`, a build step that refuses a literal schema name, a file with no story key, the same story key in two files, and any `U*.sql` undo file.
- `SchemaDriftCheck`, a pipeline step that starts a clean PostgreSQL container, applies all migrations, lists tables, columns, types, constraints and indexes, and compares them with the target environment through a read-only account.
- `MigrationRunRecorder`, which writes one job record per run and feeds `GET /admin/jobs?type=MIGRATION` and SCR-44.
- Proof that two instances starting together apply a pending migration exactly once.

**How to prove it.**
- Deploy twice: the first run applies and records version and checksum; the second does nothing.
- Add a column by hand in SIT: the pipeline fails naming `schema.table.column`.
- Run the same file in DEV and SIT with different schema names: the table exists in both, and the file is byte-for-byte identical.
- Edit an applied migration: the service refuses to start.
- Put a literal schema name in SQL: the lint fails with the file and line.
- Two migrations with the same story key: the lint fails.
- Call Flyway `clean` or add an undo file against PROD: refused.
- Break the second statement in a migration: the first statement rolls back, history records the failure, the service does not start.
- Start two instances: one applies, both start.

**Watch-outs.**
- **DL42 is the big one.** E1-044 says one rising number, `V<number>__<description>.sql`. Across 52 stories there are 68 migration files using five different conventions; 30 use `V<epic>_<story>__<name>.sql`; E1-042 itself uses `V042_1` and `V042_2`; TE-005 uses `V<next>`. The consequence is serious: Flyway would apply an Epic 2 document migration before an Epic 1 case migration. This was raised as **DL42 on 29 October, needed by 2 November, owner ACE tech lead with K. Book**. Until it is ruled, the story says the lint must report a bad name **without failing the build**. Do not let each squad invent its own convention.
- **The schema name example contradicts itself.** Section 3 assumes `recovery` in every environment; AC3 sets `rwb_case`. The mechanism is `${RWB_SCHEMA}`, so confirm the actual value per environment at kickoff.
- **No seed data in migrations.** Reference data such as LOVs, roles, permissions, `sys_objects` and `sys_fields` goes through E1-043 loads. The baseline is tables only.
- **Never edit an applied migration.** A fix is a new migration. That is the forward-only rule.
- **Critical path.** If E1-044 slips, E1-042, TE-005, E1-043 and E1-001 slip with it.

---

## 2. RWB-TE-001 — Recovery module folder and boundary test

**What it is.** The physical shape of the recovery code inside ACE, plus a build-time guard that stops one team reaching into another team’s code or calling a bank system directly.

**What the team builds.**
- 19 module packages under `ace-service/src/main/java/<ACE base package>/recovery/`: P1–P10 and S1–S9, each with an `api` package for published interfaces and an `internal` package for everything else, plus a `package-info` file. Front-end folder `src/modules/recovery`.
- `architecture/recovery-modules.yaml`: module code, Java package, published packages, and the client libraries each module may use.
- `RecoveryBoundaryTest` plus `ModuleMapLoader`: an ArchUnit test that builds five rules from the map. BND-1 collection, BND-2 common, BND-3 recovery-to-recovery, BND-4 entities/repositories, BND-5 HTTP/SFTP/file clients.
- One test-only breaking fixture per rule under `src/test`, and one passing fixture that calls a `common.api` interface.
- Front-end dependency rules: no recovery file imports `src/modules/collection`; common imports only through its public index; the rule name is `no-collection-import`.
- `RecoveryAccessGuard.require(capabilityArea, right, target)` on every `/api/recovery/v1/**` path. It calls INT-34 and maps a refusal to 403 `MSG-P4-002`. The real access check belongs to the ACE common module.

**How to prove it.**
- A recovery class importing `collection.internal.*` fails the build and names BND-1 and both classes.
- A recovery class calling `common.api` passes.
- `recovery.decision.internal.DecisionLogRepository` fails BND-3; the published `DecisionLogWriter` passes.
- Another module’s entity fails BND-4.
- `java.net.http.HttpClient` in `casewf` fails BND-5; the same use in `integration.adapter` passes.
- A recovery component importing a collection screen fails `no-collection-import`.
- A new package not in the map fails with `package recovery.vendorx is not in the module map`.
- `RW-REFADM` calling the test-only Case record endpoint gets 403 `MSG-P4-002`.

**Watch-outs.**
- **Open defect #3:** section 8 calls the rule codes `R-BND`, while every other section uses `BND-1` to `BND-5`. It is a naming inconsistency, but developers will copy it.
- **DEP-01 ownership:** the Dependency Map and Release Plan describe the module folder and boundary test as an **ACE team** dependency, while the story’s actor is `RW-TRIBE` under DL05 option B. Confirm at kickoff who creates the folders.
- **`..common.api..` is a placeholder** until ACE names its published packages. If the real names differ, BND-2 is either too tight or too loose.
- **BND-5 has two sanctioned exceptions:** `recovery.integration.adapter` for file clients, and the agent runtime client for INT-23 (TE-013). A new client library means a module-map change and tech-lead approval.
- **No feature flag.** It is a build check with no runtime switch.
- **Four stories wait on it:** TE-002, TE-003, TE-011 and TE-012.

---

## 3. RWB-E1-042 — Central configuration service and parameter catalog

**What it is.** One place for every environment setting and business parameter: the 90-day entry point, cache lifetimes, export row limits, timers, names. Each parameter has a key, type, range, default, owner, environments and the code that uses it. Code reads values through a service, never as a literal. A change is a checked, approved, dated load — not a release.

**What the team builds.**
- `config/parameter-catalog.csv` with key, kind, type, unit, range, default, scope, required, owner role, environments and used-by. Epic 1 entries include `case.entry.dpd` (90), `refdata.cache.ttl-seconds` (300) and `caselist.export.maxrows` (10000).
- `ParameterKeysGenerator`, which generates `ParameterKeys` such as `ParameterKeys.CASE_ENTRY_DPD` of type `ParameterKey<Integer>`.
- `ParameterService`, a published interface with typed `get(key, businessDate)` and `get(key, productGroup, businessDate)`, returning the value, version number, valid-from date and environment. It caches values and refreshes on `ParameterVersionApproved` or after the TTL.
- `parameter_catalog` and `parameter_value` tables, with the migrations `V042_1__parameter_catalog.sql` and `V042_2__parameter_seed.sql`.
- `ParameterLoadChecks` and `ParameterLoadHandler` behind the existing `POST /admin/reference-loads` with `table=PARAMETER`: key exists, type parses, range holds, environment allowed, required values present; one bad row refuses the whole load.
- Approval and rollback: the author cannot approve; a threshold or limit change needs `RW-RISK`; a rollback returns the previous version.
- `ParameterCatalogController` for `GET /admin/parameters`, with secrets listed but no value returned.
- `ParameterStartupCheck`: a required parameter with no value for the environment fails the health check and the service does not start (`MSG-P3-032`).
- Two build checks: `RwbMagicNumberCheck` (fails on numeric or string business literals in recovery packages; allows `0`, `1`, `-1` and test code) and `CatalogCompletenessCheck` (every key read through `ParameterService` must be in the catalog with an owner and a default).

**How to prove it.**
- `case.entry.dpd` is 90 in PROD, version 1; the case service reads 90 from the service and records version 1 in the decision log.
- A literal `90` in `recovery.casewf.casecreation` fails the build, naming the file, line and `case.entry.dpd`.
- Code reading `allocation.retry.limit` when it is not in the catalog fails the build.
- A required parameter with no value and no default for UAT fails start-up with `MSG-P3-032`.
- Loading `case.entry.dpd = 400` is refused with `MSG-GEN-002` (1 to 365); `"ninety"` is refused with `MSG-P1-002`.
- The author approving their own load gets `MSG-P7-002`.
- SIT reads 30 and PROD reads 300 for `refdata.cache.ttl-seconds`.
- `ace.db.password` shows its owner, environments and used-by, but no value.
- Rollback from version 2 returns 90.
- A version approved on 5 December with valid-from 10 December still returns 90 on 9 December and 91 on 10 December, with no restart.

**Watch-outs.**
- **Do not confuse E1-042 with E1-043.** E1-042 is the parameter catalog and configuration service (`parameter_catalog`, `parameter_value`). E1-043 is the reference data service for tables such as queues, roles, templates and document checklists (`reference_version`, `reference_row`). Both use versioned loads, but they are different tables and handlers. E1-042 builds the `PARAMETER` handler only.
- **Open defect on AC4:** `refdata.cache.ttl-seconds` is listed in the catalog seed with default 300, but AC4 says it has no value and no default for UAT. Use a genuinely required parameter with no default for that test, or get the AC corrected.
- **Open defect on test count:** section 16 has 12 test cases, while section 18 names only `TC-E1-042-01` to `11`. The access test `TC-E1-042-12` is missing from traceability. Minor, but expect a question.
- **The magic-number check will be noisy.** Plan for it. The correct fix is not to suppress it; it is to add a catalog entry and read through `ParameterKeys`. Allowed literals are only `0`, `1`, `-1` and test code.
- **Approval rights:** `RW-COE` loads with Reference data C; the parameter owner approves with Reference data A; `RW-RISK` approves where a threshold or limit moves. `DL01` assumes the RW-RISK grant, so confirm it.
- **Secrets are listed, never stored.** The catalog holds the key and metadata; the value lives in the ACE secret store.
- **Feature flag** `rwb.p3.configservice`: off means services read defaults only and value loads are refused. Good for a staged rollout.
- **Critical path.** E1-043 and E1-001 depend on it.

---

## 4. RWB-TE-002 — Code owners for the recovery module

**What it is.** A review ownership rule. Every recovery folder maps to the TechX recovery tech leads, the common module maps to the ACE team, and the repository blocks a merge until the owning team approves the changed paths. It is repository governance, not application access control.

**What the team builds.**
- `.github/CODEOWNERS` with the entries in section 12: common to `@scb-ace/ace-team`; recovery back end, test, migration, front end and `architecture/recovery-modules.yaml` to `@scb-ace/techx-recovery-tech-leads`; the CODEOWNERS file itself to both teams.
- General paths first, specific paths last, because the last matching pattern wins. Team handles only, never individuals.
- `CodeOwnersValidation`, a pull request pipeline step that checks syntax, that every owner exists and has write access, and that every pattern matches at least one file. A typo fails with `owner {team} not found`.
- The branch rule on `main`: require a pull request, require review from code owners, one approval, dismiss stale approvals, and do not count the author’s own approval. **Only the ACE repository administrator can set this.**
- Six test pull requests in a test branch protected by the same rule.

**How to prove it.**
- A recovery Java file requires a TechX tech lead; a non-owner approval leaves the merge blocked.
- A common module file requires the ACE team.
- A pull request touching both requires both teams.
- Front-end, migration and module-map files require the TechX leads.
- A tech lead approving their own pull request still needs a second team member.
- A new commit dismisses the approval.
- A misspelled team name fails the validation step.

**Watch-outs.**
- **This is 1 point but not a one-hour job.** The branch rule is a repository-host setting owned by the ACE repository administrator. Start that request on day one; otherwise the story sits at “done except the rule” and blocks nothing visibly until the first merge.
- **Open defect:** BR4 and section 12 make the CODEOWNERS file owned by both teams, while section 10 gives approval of that file to the ACE team only. Agree with the tech leads whether a change to the file needs both approvals or ACE alone.
- **Team names are assumed** until DL37 and DL36: `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`.
- **The access test `TC-TE-002-08` is unusual:** there is no Workbench endpoint and no `MSG-P4-002`. It tests that a non-owner approval does not satisfy the branch rule. Do not expect an application error message.
- **No feature flag.** The file and the branch rule have no runtime switch.
- **Depends on TE-001**, because the paths must exist.

---

## 5. RWB-TE-003 — Types and contract tests from the API specification

**What it is.** The OpenAPI file is the single source of truth. The build generates the Spring server interfaces and the React types/client from it. Every implemented operation is called with a fixture and checked against the specification, and every operation is called by a role that lacks its declared right to prove it returns 403.

**What the team builds.**
- A lint step for `api/recovery-api.yaml`: every operation has `operationId`, `x-module`, `x-capability` (area and right) and `x-first-release`; every error response uses the `Problem` schema.
- Server generation: Spring Boot 3 interfaces only, one per tag, into `<ACE base package>.recovery.generated.web` and `.model`. The generated packages are listed as shared in the module map so BND allows them.
- Front-end generation: TypeScript types and a typed fetch client into `src/modules/recovery/api/generated`. Screens import the generated client; no hand-written fetch calls or duplicate types.
- `OperationCatalog`: reads every operation, its release and its capability. Operations whose `x-first-release` is the current `rwb.release` or earlier must have a controller method; later operations are listed as pending.
- `RecoveryContractTest`: one parameterized success test per implemented operation. It validates status, content type and schema. Failures read `contract broken` or `undocumented status`.
- `RecoveryAccessContractTest`: one parameterized test per implemented operation. It picks a role from the permission matrix seed whose permission in the declared area lacks the right, expects 403, `application/problem+json` and `MSG-P4-002`. A 200 fails with `access not enforced`.
- A report of passed, failed and pending operations in the build artifacts.

**How to prove it.**
- Add `warnAt` to `Timer`: both the server model and the front-end type get it; both compile.
- Return `"escalationLevel": "two"`: the build fails naming `getCasesCaseidTimers` and `$[0].escalationLevel`.
- Remove `x-capability`: the lint fails before generation.
- Return an undocumented 400: the build fails with `undocumented status 400`.
- Leave `getAdminJobs` (E1) with no controller: the build fails with `getAdminJobs has no implementation`.
- Leave `postQueuesQueueidPlacements` (E2) with no controller: the build passes and lists it as pending.
- Remove `legalHold` from `Case` while the screen reads it: the front-end type check fails with file and line.
- Build an endpoint that skips its access check and call it as `RW-REFADM`: it returns 200, so the build fails with `access not enforced`.

**Watch-outs.**
- **Open defect 1:** step 1 names only `operationId`, `x-capability` and an error response as lint checks, while BR2 also requires `x-module` and `x-first-release`. Implement all four; the BR is the stricter rule.
- **Open defect 2:** “Done when” allows an E1 operation to be pending with a named story, while step 5 and AC5 fail the build when a current-release operation has no implementation. Treat AC5 as governing: E1 operations must be implemented; only later-release operations are pending.
- **79 operations, not 79 to build now.** The report covers the full specification; the E1 subset must pass, E2 and later are pending. Do not try to implement every operation in this story.
- **Generated code is never edited.** A change goes into the YAML and the next build regenerates it.
- **The permission matrix is owned by `RW-SECADM`** and loaded by E1-037. The test reads it; it does not define it.
- **No feature flag.** It is a build check.
- **Depends on TE-001**, because the generated packages must be listed as shared.
- **Out of scope:** file-interface contract tests (E1-007), browser tests (TE-010), permission matrix content (E1-037).

---

## 6. RWB-TE-005 — Rule table test harness

**What it is.** The routing logic is 448 rules in ten route sets, held as data. Every rule row already names a test case. This story runs those test cases whenever a rule version is loaded and in every build, and marks the version failed if any row fails. It is the business-rule equivalent of a unit test suite.

**What the team builds.**
- The `rule_test_case` table, with test case ID, route set, rule version, rule ID, from state, event, facts, expected to state, expected owner role, expected timer, result and result detail. Unique on route set, version and test case ID.
- `TestsSheetReader`, which reads the Tests sheet of the rule template into test cases.
- `CaseFileFixtureBuilder`, which builds a synthetic case file from the facts and refuses a missing fact.
- `RuleTableHarnessImpl`, which evaluates the route set for the from state and event and passes only when exactly one row hits, it is the named row, and its to state, owner role and timer equal the expected values.
- The published `RuleTableHarness` interface with `run(routeSet, ruleVersion)` and a result per rule ID.
- Wiring into the P4 rule-version load handler: `VALIDATED` when every test passes, `FAILED` otherwise; write the result for the change log (E1-048).
- `RuleTableHarnessTest`, a JUnit 5 dynamic test factory and the Gradle `ruleTests` task, one test per rule ID over `recovery/src/test/resources/rules/*.xlsx`.

**How to prove it.**
- Run `RES-2026.11` with 37 Restructure rows: 37 tests run, all pass, state `VALIDATED`.
- Change `R-RES-04` to the wrong to state: the test fails with `MSG-P3-014`, the version is `FAILED`, and it cannot be approved.
- A row naming a test case that is not in the Tests sheet: `FAILED`, naming both the rule and the test case.
- Two rows hit the same input: the test fails naming both rule IDs.
- No row hits: the test fails naming the expected rule.
- A missing fact such as `break_count`: the test fails naming the fact.
- Run the same version twice: same results, one result set stored.
- The build runs 448 named rule tests; a failing rule test fails the build.

**Watch-outs.**
- **The hit policy is Unique.** Two matching rows is a failure, not “first match wins”. That is what makes the test meaningful.
- **Open defect:** step 6 says the load handler sets the version state and section 9 names `rule_row.state`, while section 11 lists every `rule_row` field as Read and section 17 says rule rows only be read through the P4 interface. Decide with the architect where the version state is written — likely a rule-version table or a P4 write method, not a direct `rule_row` update. Do not have the harness write `rule_row`.
- **One test per rule row.** A missing `test_case_id` is a failed version, not a warning.
- **448 rows is the acceptance, 37 Restructure rows is the worked example.** Do not stop at the Restructure set.
- **Synthetic facts only.** No production case data in tests.
- **Feature flag** `rwb.p3.rule-harness`: it cannot be off in SIT, UAT or PROD; off in DEV only, where a failed harness warns and the load continues.
- **Out of scope:** the rule template, schema/overlap checks, load and rollback (E1-029), and the change log/approval checklist (E1-048). Do not rebuild those.

---

## 7. RWB-TE-011 — PDPA lint for code, tests and logs

**What it is.** A build-time privacy leak detector. It reads the list of personal fields from the data dictionary and the API specification, then scans code, test fixtures, SQL seeds, log statements, exception messages and entity `toString` methods. If it finds personal data, the build fails — and it never prints the value it found.

**What the team builds.**
- `PersonalFieldReader`: reads `sys_fields.is_personal` and `x-personal-data: true` from the API specification.
- `RuleGenerator`: writes `pdpa-rules.yaml` with the name variants — snake case, Java getter, camel case property, TypeScript property.
- The rules: `PDPA-LOG-FIELD`, `PDPA-LOG-ENTITY`, `PDPA-EXCEPTION`, `PDPA-TOSTRING`, `PDPA-FIXTURE-FIELD`, `PDPA-FIXTURE-ID`.
- `CheckDigitMatcher`: a valid Thai national ID check digit, a Thai mobile number, or an email outside the example domains.
- `pdpa-allow.yaml`: rule, path, line or pattern, owner, reason and expiry date. An expired entry no longer excuses the finding.
- `PdpaLintStep`: scans `src/main`, the front end, `src/test`, end-to-end tests, SQL seeds and JSON fixtures; prints rule, file, line and field name only.

**How to prove it.**
- `log.info(party.getFirstName())` fails with `PDPA-LOG-FIELD`, naming `first_name` and no value.
- Logging the whole `PartyEntity` object fails with `PDPA-LOG-ENTITY`.
- A JSON fixture with a valid 13-digit Thai ID fails with `PDPA-FIXTURE-ID`.
- `last_name = "TESTNAME"` fails with `PDPA-FIXTURE-FIELD`; `SYN-LAST-0001` passes.
- `contract_no` is newly marked personal: the rules regenerate and a log line using it fails.
- An allow-list entry that expired on 30 November fails when the build runs on 1 December.
- `console.log(party.lastName)` in the front end fails with `PDPA-LOG-FIELD`.
- A log line that goes through the masking helper passes.
- An exception message containing `party.getCifNo()` fails with `PDPA-EXCEPTION`.
- `ContactPointEntity.toString()` containing `value_token` fails with `PDPA-TOSTRING`.

**Watch-outs.**
- **Open defect 1:** step 2 lists entity class names among the generated name variants, while section 13's `RuleGenerator` lists only snake case, Java getter and camel case property. AC2 needs whole-entity detection, so implement entity/type matching explicitly; do not rely on field names alone.
- **Open defect 2:** step 4 scans test files for literal identifiers, while AC3 says the failing 13-digit identifier is generated by the test at run time. Test `CheckDigitMatcher` with a runtime-generated number; do not commit a real-looking identifier. Clarify the scan rule with the BA.
- **The `SYN-` prefix is assumed** from E1-065. Confirm with QA and the data team before teams bake it into fixtures.
- **The personal-field list belongs to Compliance (DL26).** Read it from `sys_fields` and the API spec; never hard-code a list in the lint.
- **The allow list is not a dumping ground.** Every entry needs an owner, a reason and an expiry. Expiry is enforced.
- **This is not runtime masking.** It stops personal data entering code and logs. Masking by role on screens and in agent calls is E1-037.
- **No feature flag.** It is a build check.
- **Depends on TE-001.**

---

## 8. RWB-TE-012 — Document storage containers

**What it is.** The storage layer for the document hub: four containers, one of them write-once for legal documents, all reached only by managed identity. It is infrastructure plus a thin adapter layer — not the document metadata or classification story.

**What the team builds.**
- An infrastructure template per environment: a storage account in the SCB tenant with a private endpoint, shared key access off, public network access off, TLS 1.2 minimum. Containers `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`.
- `rwb-docs`: blob versioning and soft delete, 30 days assumed.
- `rwb-docs-legal`: a time-based immutability policy of 3,650 days (10 years), locked in PROD and unlocked in DEV, SIT and UAT so test data can be removed.
- Role assignments: the ACE service identity gets Storage Blob Data Contributor on `rwb-intake`, `rwb-docs` and `rwb-docs-legal`; `SY-OCR` gets the same on `rwb-intake`, `rwb-docs` and `rwb-quarantine`; least privilege.
- `DocumentContainers`, the published interface returning the four container clients and readiness.
- `DocumentContainersConfig`: `DefaultAzureCredential` restricted to managed identity, 10-second timeout.
- `StorageReadinessIndicator`: joins the ACE health endpoint; the document hub is ready only when the four containers and the legal policy exist.
- `StorageErrorMapper`: maps `BlobImmutableDueToPolicy` to `WriteOnceViolationException` (409 `MSG-P5-002`), timeouts to `StorageUnavailableException` (503 `MSG-GEN-006`), and writes the audit event for a refused overwrite or delete.
- `ContentHashGuard`: compares the SHA-256 of an existing write-once blob before writing.

**How to prove it.**
- Overwrite `rwb-docs-legal/RW-2026-000701/DOC-0701/v1`: storage refuses with `BlobImmutableDueToPolicy`, the blob hash is unchanged, the attempt is in the audit log, and the store returns 409 `MSG-P5-002`.
- Delete the same blob: refused; the blob is still readable.
- Write `v2`: allowed; both `v1` and `v2` are readable.
- Overwrite `rwb-docs`: the previous version is still readable through blob versioning; a deleted blob can be restored within 30 days.
- List role assignments: the ACE service identity has only intake/docs/legal; `SY-OCR` has only intake/docs/quarantine.
- Try an account key or a shared access signature: refused with `KeyBasedAuthenticationNotPermitted`.
- Try an identity with no role: refused with `AuthorizationPermissionMismatch`.
- Try from outside the private endpoint: refused.
- Remove the immutability policy in DEV: readiness reports not ready, upload returns 503 `MSG-GEN-006`, and no document row is written.
- Storage does not answer within 10 seconds: `StorageUnavailableException`, upload returns 503.
- A user session tries to read `rwb-quarantine`: refused; only `SY-OCR` writes there.
- Write the same content with the same hash to the same write-once name: no overwrite is attempted; the existing blob reference is returned. A different hash raises `WriteOnceViolationException`.

**Watch-outs.**
- **Open defect:** X9 says storage refuses the repeated identical write and the adapter then checks the hash, while AC12 and `ContentHashGuard` say the hash is compared first and no overwrite is attempted. Implement hash-first; storage still refuses overwrite. Clarify the X9 wording.
- **The retention period is assumed** at 3,650 days until the bank retention schedule is supplied (DL26). Soft delete at 30 days is also assumed (DL27). Confirm both.
- **No endpoint of its own.** It supports E1-024 (document store), E1-026 (upload screen), E1-041 (malware scan/quarantine) and E1-057 (intake). Do not add a new API.
- **No account key, connection string or SAS anywhere.** Managed identity only. This is a security control (CTL-09/12), not a preference.
- **The readiness check is deliberately strict.** If the legal policy is missing, the document hub reports not ready and writes are refused with 503 rather than falling back to ordinary storage.
- **The SIT tests need a real storage account.** This is not fully local; plan environment access early.
- **Feature flag** `rwb.dochub.storage-containers`: off means not ready and every document write is refused with 503, rather than writing outside the write-once container.
- **Depends on TE-001.**

---

## Questions the teams will ask — and the answers you can give

| Question | Answer |
|---|---|
| **“Are these features we can show the business?”** | No. These are platform and pipeline enablers. There is no new business screen. You demo them through the pipeline, the job monitor, API responses, logs and storage behaviour. |
| **“Why do all eight come before the business stories?”** | They are the shared contract. E1-043 and E1-001 depend on E1-044/E1-042; every document feature depends on TE-012; every API and screen depends on TE-001/TE-003. Building features first would mean rebuilding them when the foundation changes. |
| **“What is a module and a published package?”** | A module is one of the 19 labelled code areas. Its `api` package is the public front door; `internal` is private. Another module may call only the published packages listed in `recovery-modules.yaml`, or send an application event. |
| **“What is a migration, and what is Flyway?”** | A migration is a numbered SQL file applied once. Flyway is the runner that records which versions ran and a checksum of each file. The database in every environment is the sum of the migrations, nothing else. |
| **“Why can’t I just add a column in SIT?”** | The drift check compares the real environment with a clean database built from the migrations. A hand-added column is a difference and stops the deployment. Every change goes through a migration. |
| **“Why can’t I write the schema name in the SQL?”** | The same file must run in every environment. `${RWB_SCHEMA}` is replaced with the environment’s schema name. A literal name would tie the file to one environment and fail the lint. |
| **“What is the migration naming rule?”** | The story says one rising number, `V<number>__<description>.sql`. The wider document set uses five conventions, which is DL42. Until the ACE tech lead rules, follow the convention your tech lead confirms and expect the lint to warn rather than fail. Do not rename 68 files ad hoc. |
| **“What is the difference between E1-042 and E1-043?”** | E1-042 is the parameter catalog for settings, thresholds, limits and timers. E1-043 is the reference data service for tables such as queues, roles, templates and document checklists. Both are versioned and approved, but they have different tables and handlers. |
| **“Why does the build fail on a hard-coded 90?”** | The magic-number check enforces Principle 1. Add a catalog entry, use the generated `ParameterKeys` and read through `ParameterService`. Only `0`, `1`, `-1` and test code are allowed as literals. |
| **“What is a contract test?”** | A test that calls each implemented endpoint with a synthetic fixture and validates the request, status, content type and response body against the OpenAPI file. A separate access test calls the same endpoint as a role that lacks the declared right and expects 403 `MSG-P4-002`. |
| **“What is the rule harness?”** | Every rule row has a test case. The harness evaluates the row with the from state, event and facts, and passes only if exactly one row hits and the to state, owner and timer match. A version with any failure cannot be approved. The build runs all 448 rows. |
| **“What does the PDPA lint catch?”** | Personal fields in log statements, whole personal entities, exception messages, entity `toString`, test fixtures and front-end console logs. It also catches real-looking Thai IDs, mobile numbers and emails. It prints the field name, never the value. |
| **“What is write-once?”** | A storage policy that refuses overwrite and delete for the retention period. A corrected legal document is a new blob at `v2`; `v1` stays readable. In PROD the policy is locked; in DEV/SIT/UAT it is unlocked so test data can be removed. |
| **“What do we do about the open defects?”** | There are 13 open items across these eight. Most are wording or test-data contradictions. Three need a real decision: DL42 (migration naming), TE-005 (where the rule-version state is written) and TE-003 (whether a current-release operation may be pending). Escalate those to the tech lead/BA; do not silently choose. |
| **“Who do we chase?”** | ACE repository administrator for the TE-002 branch rule; ACE tech lead for DL42; Compliance for the PDPA field list (DL26); platform administrator for migrations and storage; security administrator for storage role assignments. |
| **“Do we need UI work?”** | No new screens. E1-044 uses the existing SCR-44 job monitor; TE-012 uses SCR-44 readiness and the existing SCR-30 upload; the rest are pipeline, API or storage. |

## How I would run the session

1. **Open with the eight-story map above.** Say plainly: “These are the platform contract, not features. Two are critical path, and everything else in Epic 1 assumes them.”
2. **Explain the dependency chain once.** E1-044 → E1-042 and TE-005. TE-001 → TE-002, TE-003, TE-011 and TE-012. Then E1-043 and E1-001 follow. That is why the order is 1 to 8.
3. **For each story, use the hub page in the same order:** header → flow → acceptance criteria → solution plan → test cases. Click “Show the step explanations” when a flow step is too terse. Click any underlined code to open its definition in place.
4. **Keep the Story Defects workbook open as a side tab.** When a contradiction comes up, name it and its owner instead of improvising a ruling. The big four are DL42, E1-042 AC4, TE-005 state, and TE-003 pending.
5. **Close with the six things you need from the room:** the DL42 naming ruling, the real `RWB_SCHEMA` value per environment, the code-owner team handles, the ACE admin date for the branch rule, confirmation of the `SYN-` prefix, and confirmation of the 10-year retention/30-day soft delete assumptions.

**Bottom line for the teams:** these eight stories are how the Workbench stops being a collection of good intentions and becomes a build with guardrails. E1-044 makes database change safe, TE-001 makes module boundaries real, E1-042 makes values data instead of code, TE-002 makes ownership enforceable, TE-003 keeps the API and screens in step, TE-005 makes rules testable, TE-011 keeps personal data out of logs and tests, and TE-012 makes legal documents tamper-evident. If these are right, the feature stories are normal delivery. If they are wrong, every feature story inherits the problem.

<details><summary>Reasoning</summary>

Each has 2 regression cases: first AC + access. Good pattern. Can mention "the regression suite keeps the first smoke case and the access refusal for each."

Need maybe check "Story Defects" full list count for these; we have 13 defects across 8. Need explain the most important ones. The user needs to answer team questions. We can create a "questions they will ask" section with answers.

Let's get exact defect rows with full text for these 8 to cite accurately. We have from query. Some rows truncated? They are full. Let's list them cleanly:
- E1-044 (multiple):
  1. section 3 assumes RWB_SCHEMA is recovery in every environment; section 7 background sets it to rwb_case. (Open)
  2. 68 migration file names across 52 stories follow five naming rules (V<epic>_<story> in 26, V<epic>_<sub>_<story> in 12, single number in this story, V<story>_<seq> in 9, date in 4), so Flyway applies an Epic 2 document migration before an Epic 1 case migration. Open, raised as DL42 on 29 Oct, needed by 2 Nov. One pass renames all 68 once rule set. Owner ACE tech lead with K. Book.
  3. AC3 sets RWB_SCHEMA to rwb_case in DEV and SIT, while section 3 assumes recovery. Open.
- E1-042:
  1. section 5 lists X10 before X9; section 16 has 12 test cases while section 18 names only TC-01 to TC-11. Open.
  2. AC4 says refdata.cache.ttl-seconds has no value and no default for UAT, while section 3 lists it in catalog seed with default 300. Open.
- TE-001:
  1. section 8 says R-BND codes vs BND-1..5. Open.
- TE-002:
  1. BR4 and section 12 make code owners file owned by both teams, while section 10 gives approval of that file to ACE team only. Open.
- TE-003:
  1. step 1 names only operationId, x-capability and error response as lint checks, while BR2 also requires x-module and x-first-release. Open.
  2. Done when allows an E1 operation to be pending with a named story, while step 5 and AC5 fail the build when a current release operation has no implementation. Open.
- TE-005:
  1. step 6 has the load handler set version state and section 9 names rule_row.state as the column, while section 11 lists every rule_row field as Read and section 17 allows rule rows only to be read via P4. Open.
- TE-011:
  1. step 2 lists entity class names among generated variants, while RuleGenerator lists only snake case, Java getter, camel case property. Open.
  2. step 4 scans test files for literals, while AC3 has the failing 13-digit identifier generated at run time, so no literal is in the file. Open.
- TE-0

_[truncated]_

</details>
