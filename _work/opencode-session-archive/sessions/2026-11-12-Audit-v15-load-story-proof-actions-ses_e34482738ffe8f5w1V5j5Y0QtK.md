# Audit v15 load-story proof actions

- **Session ID:** `ses_e34482738ffe8f5w1V5j5Y0QtK`
- **Created:** 2026-11-12 00:46  |  **Last activity:** 2026-11-12 00:53
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `general`
- **Parent session:** Loading-data story AC impact analysis (`ses_e348648b2ffewAnaxQscM12L9E`)
- **Tokens:** 56,173 in / 5,214 out / 14,054 reasoning
- **Messages:** 13

---

### User - 2026-11-12 00:46

You are a subagent spawned by another session.
Read-only analysis. Do NOT modify, create or delete any file. Return a report only.

Context: The file `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\14 Story Updates\Recovery Workbench Project Hub v15.html` contains the v15 story set. Its decompressed payload is at `C:\Users\SahilMore\AppData\Local\Temp\opencode\stories_full.json` (array of story objects with key, title, text).

Focus on the 7 stories: RWB-E1-003, RWB-E1-004, RWB-E1-005, RWB-E1-007, RWB-E1-009, RWB-E1-010, RWB-E1-012.

For each story, report in a compact table:
1. The final "proof" developer action row (A8/A9/A10) exactly as written, or "none".
2. Any data-load, SIT, synthetic-data, test-fixture or demo clause inside any other action row (e.g. E1-010 A8).
3. The exact intro sentence (e.g. "A1 to A9 are code. A10 is the proof.").
4. The "Developer actions" count from the story attribute table.
5. The story-level "**Done when.**" line.

Then recommend the simplest removal approach: remove the final proof action entirely, remove data-load clauses from any remaining action, update the intro/count and the Done-when. State exactly what the new intro/count/Done-when should be. Do not propose renumbering unless essential.

Be concise and use exact quotes. Do not edit anything.

### Assistant - 2026-11-12 00:46 | opencode-go/deepseek-v4.1-flash | general

I'll start by loading the payload and examining the 7 target stories.

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\nprint(len(d))\nprint(list(d[0].keys()))\nfor s in d:\n    if s.get('key') in ['RWB-E1-003','RWB-E1-004','RWB-E1-005','RWB-E1-007','RWB-E1-009','RWB-E1-010','RWB-E1-012']:\n        print(s.get('key'), '|', s.get('title'))\n\""}
```

```text
332
['key', 'title', 'doc', 'text', 'sections']
RWB-E1-003 | ALS daily extract load
RWB-E1-004 | EFS extract load
RWB-E1-005 | Excel and SharePoint inventory
RWB-E1-007 | Integration adapters for file loads and outbound files
RWB-E1-009 | CCMS and SVAF loads
RWB-E1-010 | Excel and SharePoint loads
RWB-E1-012 | Retire local copies

```

### Assistant - 2026-11-12 00:46 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Let me dump the full text for each of these stories.

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\nfor s in d:\n    if s.get('key')=='RWB-E1-003':\n        print('TITLE:',s['title'])\n        print('SECTIONS:',list(s['sections'].keys()) if isinstance(s.get('sections'),dict) else type(s.get('sections')))\n        print('---TEXT---')\n        print(s['text'])\n\" "}
```

```text
TITLE: ALS daily extract load
SECTIONS: <class 'list'>
---TEXT---
RWB-E1-003 ALS daily extract load
| Item | Value |
|---|---|
| Story key | RWB-E1-003 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-03 Load account and arrears daily from ALS |
| Requirement IDs | REQ-RDF-002 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Developer actions | 10 build actions, in the plan after the preconditions |
| Status | Ready for build |
1. Story
As a **data steward and data product owner (RW-DATASTEW)**, I want **ALS balances, arrears, payments and classification loaded every working day from the COLLINS daily batch for accounts at 90 days past due or more**, so that **account and arrears data is current to the previous working day**.
2. Business rationale
Case owners today read balances and days past due from ALS screens and team files, so two people can see two different numbers for one account. This story loads INT-01 (accounts) and INT-02 (payments) from the COLLINS daily batch into the account and arrears data product DP01, after the seven load checks, so every case reads one checked balance with its business date. It meets REQ-RDF-002 and serves the measure "loads on time and complete on 99 percent of days" and the load target "job runs by 07:00" (NFR-013).
3. Preconditions
- RWB-E1-001 is done: loan_account, account_payment and data_product exist, and the catalog holds DP01.
- COLLINS writes the INT-01 and INT-02 records for the business date and a trailer row (record count, balance total, business date) into its staging tables in the ACE database. The table names are configuration values, owned by the ACE team.
- The mapping version for INT-01 and INT-02 (source_field_map) and the code map (source_code_map) are loaded and approved.
- The working day calendar is loaded in the reference data service (RWB-E1-043).
- Parameters are loaded: `load.window.end` 09:00, `load.retry.interval` 60 minutes, `load.hold.tolerance.pct` 0.50, `load.movement.tolerance.pct` 10.00, `load.sample.size` 50 (tolerances assumed, DL25).
- JOB-01 runs as service identity SY-DATALOAD.
Developer action plan
**Work in this order.** A1 to A9 are code. A10 is the proof. Each action ends with a check that can be shown in review; the AC 
... truncated (33,838 chars total)
```

### Assistant - 2026-11-12 00:46 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Interesting — E1-003 already appears to have a proof-like A10, and the intro says "A1 to A9 are code. A10 is the proof." But wait — the task says the v15 story set... Let me check whether the payload matches. Hmm, E1-003 has A10 as "Prove the 14 ACs and publish the read interface" — that's the proof row. Interesting, so the pattern varies.

Wait, actually. The task premise: "recommend the simplest removal approach: remove the final proof action entirely". Hmm, this is a bit odd — it seems the user (parent session) is working on a change to remove test/proof action rows and data-load clauses. Let me check the rest of the stories.

Let me extract just the relevant bits programmatically to be efficient: the attribute table "Developer actions" value, the intro sentence paragraph after "Developer action plan", the action rows table, the "Done when." line, and search for evidence clauses.

Let me write a script that prints for each of the 7 stories:
- Developer actions row value
- the intro paragraph
- action rows (# | action | done when)
- Done when line
- any sentences with keywords: SIT, synthetic, fixture(s), demo, data load, load the, test data, seed, sample data, etc.

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\nkeys=['RWB-E1-003','RWB-E1-004','RWB-E1-005','RWB-E1-007','RWB-E1-009','RWB-E1-010','RWB-E1-012']\nfor s in d:\n    if s.get('key') not in keys: continue\n    t=s['text']\n    print('='*100)\n    print(s['key'], '|', s['title'])\n    m=re.search(r'\\| Developer actions \\| (.*?) \\|', t)\n    print('DEV ACTIONS ATTR:', m.group(1) if m else 'MISSING')\n    # intro: line after 'Developer action plan'\n    i=t.find('Developer action plan')\n    print('--- INTRO BLOCK ---')\n    print(t[i:i+600].split('\\n\\n')[0])\n\""}
```

```text
====================================================================================================
RWB-E1-003 | ALS daily extract load
DEV ACTIONS ATTR: 10 build actions, in the plan after the preconditions
--- INTRO BLOCK ---
Developer action plan
**Work in this order.** A1 to A9 are code. A10 is the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies.
====================================================================================================
RWB-E1-004 | EFS extract load
DEV ACTIONS ATTR: 10 build actions, in the plan after the preconditions
--- INTRO BLOCK ---
Developer action plan
**Work in this order.** A1 to A9 are code. A10 is the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies.
====================================================================================================
RWB-E1-005 | Excel and SharePoint inventory
DEV ACTIONS ATTR: 8 build actions, in the plan after the preconditions
--- INTRO BLOCK ---
Developer action plan
**Work in this order.** A1 to A7 are code. A8 is the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies.
====================================================================================================
RWB-E1-007 | Integration adapters for file loads and outbound files
DEV ACTIONS ATTR: 10 build actions, in the plan after the preconditions
--- INTRO BLOCK ---
Developer action plan
**Work in this order.** A1 to A9 are code. A10 is the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies.
====================================================================================================
RWB-E1-009 | CCMS and SVAF loads
DEV ACTIONS ATTR: 8 build actions, in the plan after the preconditions
--- INTRO BLOCK ---
Developer action plan
**Work in this order.** A1 to A6 are code. A7 and A8 are the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies.
==========================================================================================
... truncated (3,357 chars total)
```

### Assistant - 2026-11-12 00:47 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Now extract the action tables and done-when lines. Let me print the table rows for each story.

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\nkeys=['RWB-E1-003','RWB-E1-004','RWB-E1-005','RWB-E1-007','RWB-E1-009','RWB-E1-010','RWB-E1-012']\nfor s in d:\n    if s.get('key') not in keys: continue\n    t=s['text']\n    print('='*100)\n    print(s['key'])\n    i=t.find('| # | Developer action | What to build | Done when |')\n    j=t.find('**Do not build:**',i)\n    print(t[i:j].strip())\n    print('--- DONE WHEN LINE ---')\n    for line in t.split('\\n'):\n        if '**Done when.**' in line:\n            print(line.strip())\n\""}
```

```text
====================================================================================================
RWB-E1-003
| # | Developer action | What to build | Done when |
|---|---|---|---|
| A1 | Create the load tables and the unique run key | Write V1_003__load_run.sql. Create load_run, dq_exception, source_field_map and source_code_map with the standard columns. Add uk_load_run_active UNIQUE (interface_id, business_date) WHERE status IN (RUNNING, COMPLETED), and an index on dq_exception (product_code, raised_on). Add LoadRun, DqException, SourceFieldMap and SourceCodeMap with their repositories. | The migration runs clean in SIT, and a second run for the same interface and business date is refused by the database. AC11, AC12 |
| A2 | Build the four blocking checks | Implement DQ-001 business date, DQ-002 structure, DQ-003 control total and DQ-004 keys in LoadCheckRunner as SQL over the staging tables named by rwb.p1.collins.int01.table, rwb.p1.collins.int02.table and rwb.p1.collins.trailer.table. On any failure write no target row, set the run REFUSED with failed_check, publish LoadRefused and send MSG-P1-002 to the data steward and platform administrator groups. | A trailer of 184,500 against 184,498 rows refuses at DQ-003, keeps data_as_of at 2026-11-27 and writes one LoadRefused. A wrong date refuses at DQ-001 and a duplicate account key at DQ-004. AC2, AC4, AC5 |
| A3 | Build the tolerance checks and the hold list | Implement DQ-005 references and DQ-006 code maps. Count the failing records, divide by rows read and compare with load.hold.tolerance.pct. At or below 0.50 percent, write the held records to dq_exception and load the rest. Above 0.50 percent, refuse the whole interface. | 11 of 2,310 payments at 0.48 percent writes 2,299 payments and 11 DQ-012 exceptions; 13 at 0.56 percent refuses with no payment row; exactly 0.50 percent is treated as within tolerance. AC6, AC7, AC8 |
| A4 | Build the mapper | Write SourceMappingService with COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP and BUSINESS_DATE. Read the approved mapping version in force and refuse an unapproved one. Convert Buddhist Era dates and THB amounts. | 15/03/2569 maps to 2026-03-15, amounts carry two decimals, and an unapproved mapping refuses the load before any write. AC1, AC3 |
| A5 | Write the INT-01 step in one transaction | Build the INT-01 Spring Batch step: stream the staging rows, map them, upsert loan_account by account_no, set data_as_of to the business 
... truncated (32,813 chars total)
```

### Assistant - 2026-11-12 00:47 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Interesting: E1-007 had no Done-when line found by my exact match "**Done when.**". Let me check E1-007's text for that section. Maybe it's on a different line or worded differently. Also need to check whether E1-007 has a "Developer actions" count = 10 but only 10 rows (A1-A10) where A10 is the proof and no Done when line. Also count for E1-012 = 8 with A1-A8; A8 is proof. E1-009 count 8, A7+A8 both proof-ish (A7 is "Prove the failed valuation write and the access path" — hmm, A7 is a proof too? "Prove ..." but it's also design-level: force failure, add access test. The intro says "A7 and A8 are the proof").

The task explicitly asks: "The final 'proof' developer action row (A8/A9/A10) exactly as written" — so for E1-009 that's A8 (the last one), and note A7 also proof-ish. And "Any data-load, SIT, synthetic-data, test-fixture or demo clause inside any other action row (e.g. E1-010 A8)".

So I need to identify clauses in non-final action rows that are about loading data into SIT, synthetic data, fixtures, demo. Let me search each story's action rows for keywords: SIT, synthetic, fixture, demo, load ... inventory, seed, sample data, "in SIT", "the SIT", "test data".

From E1-010 A8: "Load all 14 LOAD trackers of the SIT inventory from synthetic .xlsx and .csv files." — data load clause.

E1-003: A1 "The migration runs clean in SIT" — that's a SIT clause but about migration check, not data-load. The task asks for "data-load, SIT, synthetic-data, test-fixture or demo clause". So SIT clauses count too. Hmm. But which ones matter? They want removal of data-load clauses, and recommendation. Let me be careful: report all SIT/synthetic/fixture/demo clauses in OTHER action rows, exact quotes.

Let me systematically scan all action rows for these keywords per story. Also check the story-level Done-when lines, and whether E1-007 has one.

Also need to check E1-007 whether "**Done when.**" exists — maybe "**Done when.**" is in a different section or missing entirely. Let me grep.

Also check the story attributes "Developer actions" count vs actual rows. E1-004: count 10, rows A1-A10 (A10 proof) → new count 9. E1-007: count 10, A1-A10 → 9. E1-009: count 8, A1-A8, intro says A7 and A8 are the proof → remove both? The task says "remove the final proof action entirely" — for E1-009 the final proof is A8; A7 is also called proof in the intro. Need to decide: recommend removing A8 (final proof) and probably also A7 since it's proof-only ("Prove the failed valuation write a

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\nkeys=['RWB-E1-003','RWB-E1-004','RWB-E1-005','RWB-E1-007','RWB-E1-009','RWB-E1-010','RWB-E1-012']\nkw=['SIT','synthetic','fixture','demo','rehears','seed','test data','masked','inventory version','load all','Load all','load the SIT','sample data','pilot']\nfor s in d:\n    if s.get('key') not in keys: continue\n    t=s['text']\n    i=t.find('| # | Developer action | What to build | Done when |')\n    j=t.find('**Do not build:**',i)\n    block=t[i:j]\n    rows=[l for l in block.split('\\n') if l.startswith('| A')]\n    print('='*90); print(s['key'], 'rows:', len(rows))\n    for r in rows:\n        cells=[c.strip() for c in r.strip('|').split('|')]\n        for k in kw:\n            if k in r:\n                print(' ',cells[0],'kw=',k)\n    print('DoneWhen count in whole text:', t.count('**Done when.**'))\n\""}
```

```text
==========================================================================================
RWB-E1-003 rows: 10
  A1 kw= SIT
  A6 kw= fixture
  A10 kw= SIT
  A10 kw= synthetic
DoneWhen count in whole text: 1
==========================================================================================
RWB-E1-004 rows: 10
  A10 kw= demo
DoneWhen count in whole text: 1
==========================================================================================
RWB-E1-005 rows: 8
  A1 kw= SIT
  A8 kw= SIT
  A8 kw= load the SIT
DoneWhen count in whole text: 1
==========================================================================================
RWB-E1-007 rows: 10
  A3 kw= fixture
  A10 kw= SIT
DoneWhen count in whole text: 0
==========================================================================================
RWB-E1-009 rows: 8
DoneWhen count in whole text: 1
==========================================================================================
RWB-E1-010 rows: 9
  A8 kw= SIT
  A8 kw= synthetic
  A8 kw= Load all
  A8 kw= load the SIT
DoneWhen count in whole text: 1
==========================================================================================
RWB-E1-012 rows: 8
  A8 kw= fixture
DoneWhen count in whole text: 1

```

### Assistant - 2026-11-12 00:48 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Good. Now check E1-005 A6 (loads TRK-2026.11) — it didn't catch "load" keyword because I searched "load all"/"load the SIT". Let me inspect A6 exact text. And E1-004 A6 (test case). Also check "SIT" only in E1-003 A1 and E1-005 A1 done-when.

Also check E1-007 Done-when — missing entirely. Let me look at the end of section 13 for E1-007.

Also confirm E1-009 A7 content and whether intro calls A7/A8 proof.

Let me print exact A6 E1-005, E1-004 A6, and E1-007's solution plan tail, plus E1-007 section 13 text.

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\ng={s['key']:s for s in d}\nt=g['RWB-E1-005']['text']\ni=t.find('| A6 |'); print('E1-005 A6:'); print(t[i:t.find('\\n',i)])\nt=g['RWB-E1-004']['text']\ni=t.find('| A6 |'); print('\\nE1-004 A6:'); print(t[i:t.find('\\n',i)])\nt=g['RWB-E1-007']['text']\ni=t.find('13. Solution plan'); j=t.find('14. Validation',i)\nprint('\\n--- E1-007 section 13 tail ---'); print(t[j-900:j])\n\""}
```

```text
E1-005 A6:
| A6 | Connect the handler to the reference-data flow | Register TrackerInventoryHandler for table code tracker_inventory with the existing POST /admin/reference-loads from RWB-E1-043. Write no new upload controller. The load submits the version for checking; the data steward confirms it through the reference data change process. | The reference data administrator loads TRK-2026.11, the data steward confirms it, and GET /admin/trackers returns the new version only after that confirmation. AC1, AC8 |

E1-004 A6:
| A6 | Close the run and stamp DP05 | Write the held records to dq_exception with the account key only. Run DQ-042 movement. Call FreshnessStampService.recordLoad for DP05 in the same transaction, set the run COMPLETED with its counts and publish LoadCompleted with source INT-07. | The DP05 stamp carries 2026-11-30, the run is COMPLETED, and the event commits with the status. AC1, AC5, AC6 |

--- E1-007 section 13 tail ---
 trailer files.
  3. Build FileLoadAdapterImpl with the run row, refusal path (calls P1 DataProductStatus.markStale) and duplicate path.
  4. Build OutboundFilesImpl and OutboundSender with SKIP LOCKED, retry intervals from the row and the EXCEPTION move.
  5. Wire the P3 calls: CaseEvents.raise for SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED; TaskApi.raiseTask for the owner task.
  6. Build IdempotencyGuardImpl and use it in every event listener of the recovery module through a shared base listener.
  7. Build the two endpoints with the access check and the ACE audit write on resend.
  8. Add the contract test template and the AdapterBoundaryTest to the pipeline.
- **Feature flag:** `rwb.integration.file-adapters`.
- **Done when:** the tests in section 16 pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT.


```

### Assistant - 2026-11-12 00:48 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

So E1-007 uses "**Done when:**" (colon inside bold) in section 13 as a bullet, whereas others use "**Done when.**". The task asks for the story-level "**Done when.**" line — for E1-007 the equivalent is "**Done when:** the tests in section 16 pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT."

Let me double-check all stories' Done-when formatting variants. Grep for "Done when" per story.

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\nkeys=['RWB-E1-003','RWB-E1-004','RWB-E1-005','RWB-E1-007','RWB-E1-009','RWB-E1-010','RWB-E1-012']\nfor s in d:\n    if s.get('key') not in keys: continue\n    print('==',s['key'])\n    for l in s['text'].split('\\n'):\n        if 'Done when' in l: print('   ',l.strip())\n\""}
```

```text
== RWB-E1-003
    | # | Developer action | What to build | Done when |
    **Done when.** The tests in section 16 pass, and a full synthetic run of 184,500 accounts completes in under 30 minutes in SIT.
== RWB-E1-004
    | # | Developer action | What to build | Done when |
    **Done when.** The tests in section 16 pass.
== RWB-E1-005
    | # | Developer action | What to build | Done when |
    **Done when.** The tests in section 16 pass, and the SIT inventory version holds at least one row for each of the six teams.
== RWB-E1-007
    | # | Developer action | What to build | Done when |
    - **Done when:** the tests in section 16 pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT.
== RWB-E1-009
    | # | Developer action | What to build | Done when |
    **Done when.** The tests in section 16 pass.
== RWB-E1-010
    | # | Developer action | What to build | Done when |
    **Done when.** The tests in section 16 pass, and the 14 LOAD trackers of the SIT inventory load from synthetic files.
== RWB-E1-012
    | # | Developer action | What to build | Done when |
    **Done when.** The tests in section 16 pass, and the SIT retirement report shows the six teams.

```

### Assistant - 2026-11-12 00:48 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Now let me look at E1-005 A8 and E1-010 A8 exact text (already have). And E1-009 A7/A8 exact (have).

Also verify whether stories' attribute counts match rows: E1-003 10/10, E1-004 10/10, E1-005 8/8, E1-007 10/10, E1-009 8/8, E1-010 9/9, E1-012 8/8.

Now check the "Do not build" / hand-off text that references proof or test? Not asked. But Done-when updates may interact with section 16. Also check whether section 16 test cases are referenced anywhere else in the action table (AC numbers in each row). Removing proof row doesn't remove ACs — each row still ends with AC refs.

One more check: does any non-final action row contain a "load the SIT inventory"/data-load clause besides E1-010 A8 and E1-005 A8? E1-005 A6 mentions "The reference data administrator loads TRK-2026.11" — that's a done-when check with a manual data load. Is that a "data-load clause"? It's about loading the real inventory version, arguably a demo/operational clause. I'll flag it as a secondary data-load/manual-load clause.

Also E1-004 A6: "Call FreshnessStampService.recordLoad" — not data load. Fine.

E1-003 A6: "2,299 payments load and 11 are held in the 0.48 percent fixture" — fixture clause in a done-when. Flag as fixture reference (minor). E1-007 A3: "Add a pass and a fail fixture per check type" — that's building test fixtures, in "What to build". That's a fixture clause. E1-012 A8: "outstanding 0 for the full fixture" — final row removed.

E1-009: no SIT/synthetic keywords, but A7 is proof and A8 is proof.

Now let me also double check E1-009 A7: "Prove the failed valuation write and the access path" — starts with "Prove". Intro says "A7 and A8 are the proof." So removing final proof A8 alone leaves A7 as proof. Recommendation: remove A7 and A8 (both proof), new intro "A1 to A6 are code.", count 6, Done-when "The tests in section 16 pass."

But "Do not propose renumbering unless essential" — removing A7 and A8 leaves A1-A6, no gaps. Good.

For E1-003: removing A10 loses the LoadRunQuery build. Options:
(a) Remove A10 entirely and fold "Implement and publish LoadRunQuery" into A9 (endpoint row) — no renumbering; count 9; intro "A1 to A9 are code."
(b) Keep A10 as build-only "Publish the read interface". But user asked simplest: remove final proof action entirely. I'll recommend (a) as primary, noting the LoadRunQuery build must not be lost. Actually the user explicitly said "recommend the simplest removal approach: remove the final proof action entirely". So primary recommendation:

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\ng={s['key']:s for s in d}\nfor k in ['RWB-E1-005','RWB-E1-010','RWB-E1-012','RWB-E1-007','RWB-E1-009','RWB-E1-003']:\n    print('='*80); print(k)\n    for l in g[k]['text'].split('\\n'):\n        if l.startswith('**Hand-off') or 'Hand-off' in l or 'Hand off' in l:\n            print(l.strip())\n    print(' -- rows mentioning Hand:')\n    i=g[k]['text'].find('| # | Developer action')\n    j=g[k]['text'].find('**Do not build:**',i)\n    for r in g[k]['text'][i:j].split('\\n'):\n        if r.startswith('| A') and 'Hand' in r: print('   ',r.split('|')[1].strip())\n\""}
```

```text
================================================================================
RWB-E1-005
**Hand-off:** the LOAD list goes to RWB-E1-010. The RETIRE list goes to RWB-E1-012. The KEEP list is out of scope and is not loaded or retired.
 -- rows mentioning Hand:
    A2
    A5
    A6
    A8
================================================================================
RWB-E1-010
**Hand-off:** the SIGNED_OFF trackers and signed_off_at go to RWB-E1-012. tracker_row content and the target product go to the owning modules for their later mapping. The load status and rejected rows go to SCR-44 and the data-quality view.
 -- rows mentioning Hand:
    A9
================================================================================
RWB-E1-012
**Hand-off:** the retirement report goes to the Tribe lead for the 30 November release checklist. The stored tracker file and tracker_row stay unchanged as the Workbench archive copy. The unfed field list tells a later epic which fields no data product carries.
 -- rows mentioning Hand:
================================================================================
RWB-E1-007
**Hand-off:** the RecordLoader interface, JOB-09 schedule, file checks and checked records go to RWB-E1-009. The outbox and duplicate-event pattern go to RWB-E1-003 and RWB-E1-004. The adapter pattern and contract template go to every later interface. The exception queue list and resend go to SCR-09.
 -- rows mentioning Hand:
    A4
================================================================================
RWB-E1-009
**Hand-off:** ValuationRecordApi, the stale flag and ageDays go to S5 and the valuation stories. The DP06 collateral and appraisal state goes to RWB-E1-012. The DP06 freshness stamp and weekly stale alert go to RWB-E1-015. The LoadOutcome goes back to the P2 adapter.
 -- rows mentioning Hand:
================================================================================
RWB-E1-003
**Hand-off:** the load framework, load_run, dq_exception and mapping tables go to RWB-E1-004, RWB-E1-009 and RWB-E1-010. LoadRunQuery goes to P3 and P4. The commit-point hook for the DP01 freshness stamp goes to RWB-E1-015.
 -- rows mentioning Hand:

```

### Assistant - 2026-11-12 00:49 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Good — handoffs exist in standalone paragraphs, so deleting proof rows doesn't lose the handoff. E1-007's contract template handoff is in the Hand-off paragraph too.

Now, one more: verify exact E1-010 A8 text and E1-005 A8 text (I have them). Also E1-004 A10 / E1-007 A10 / E1-012 A8 exact (have).

Also check whether the "Developer actions" attr wording might need to change beyond count: "10 build actions, in the plan after the preconditions" → "9 build actions, ...". Fine.

Now consider the intro sentence: "**Work in this order.** A1 to A9 are code. A10 is the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies."

New intro recommendation: "**Work in this order.** A1 to A9 are code. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies."

For E1-009: "**Work in this order.** A1 to A6 are code. Each action ends with a check ...".

For E1-007: "**Work in this order.** A1 to A9 are code. Each action ends..."

For E1-005: "**Work in this order.** A1 to A7 are code. ..."

For E1-010: "**Work in this order.** A1 to A8 are code. ..."

For E1-012: "**Work in this order.** A1 to A7 are code. ..."

Now Done-when recommendations:
- E1-003: "**Done when.** The tests in section 16 pass." — but section 16 tests are synthetic. If the parent is purging synthetic data references, maybe the Done-when should be "**Done when.** The tests in section 16 pass." consistent with E1-004/009. I'll state that.
- E1-004: unchanged: "**Done when.** The tests in section 16 pass."
- E1-005: "**Done when.** The tests in section 16 pass." (drop SIT inventory clause).
- E1-007: "**Done when:** the tests in section 16 pass." — but boundary test runs in pipeline is a build item in section 13 step 8; contract tests in SIT. If purging SIT, recommend "**Done when:** the tests in section 16 pass." Optionally keep "the boundary test runs in the pipeline" since that's a pipeline gate, not a data load. Hmm. The user says update the Done-when. Simplest: "**Done when:** the tests in section 16 pass." I could note that "the boundary test runs in the pipeline" is a code-level gate and may be kept if desired. Keep it simple: recommend "the tests in section 16 pass." and note the boundary test is already build step 8.
- E1-010: "**Done when.** The tests in section 16 pass." (drop SIT/synthetic c

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\np=r'C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\14 Story Updates\\Recovery Workbench Project Hub v15.html'\nimport io,os\nb=open(p,'rb').read()\nprint('bytes',len(b))\nfor s in [b'A10 is the proof', b'RWB-E1-007', b'Prove the 10 ACs']:\n    print(s, b.count(s))\n\""}
```

```text
bytes 27574161
b'A10 is the proof' 0
b'RWB-E1-007' 10
b'Prove the 10 ACs' 0

```

### Assistant - 2026-11-12 00:50 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

The text is likely escaped or chunked. Not important. The payload is the decompressed source. Let me verify the payload derives from the HTML by checking a distinctive string that appears plain, e.g., "RWB-E1-007" appears 10 times — the HTML has story keys inline (maybe metadata). Fine.

Maybe check whether the HTML contains the string with escaped unicode? "A10 is the proof" not present at all → perhaps the payload is compressed and embedded. Since the user gave the payload, trust it.

One more sanity check: 332 stories, 7 keys found. Also the "sections" field is a list — maybe sections contain structured content. Not needed.

Now let me double-check E1-010 A8 and E1-005 A8 exact quote to avoid misquoting. Also E1-003 A10 exact. I have them from the table dump. Good.

Also I should confirm E1-007 has no "**Done when.**" style line but the bullet. Yes.

Let me also check if E1-007's attribute count is 10 and rows 10. Yes.

Now consider whether the recommendation should also address "each action ends with a check" sentence: after removing proof rows, "Each action ends with a check that can be shown in review" still holds (done-when columns are checks). Fine.

Should the proof row removal also remove the "AC1 to AC14" claim? Not needed; each row has AC refs.

One nuance for E1-003: A10's Done-when claims "Fourteen of fourteen AC tests pass" where 15 tests exist (TC-...-01 to 15) and 14 ACs. Removing it resolves a count mismatch. Worth noting briefly.

E1-004 A10 claims "Ten of ten AC tests" but 11 test cases (TC-...-01 to 11) and 10 ACs. Same pattern.

E1-005 A8 "Eight of eight" with 9 test cases (TC-...-01 to 09) and 8 ACs.

E1-007 A10 "Nine of nine" with 10 tests.

E1-009 A8 "Eleven of eleven" with 12 tests.

E1-010 A9 "Thirteen of thirteen" with 14 tests.

E1-012 A8 "Ten of ten" with 11 tests.

That's a consistent pattern (AC count vs test case count). Not asked, but worth one line since removing proof rows removes the mismatch.

Also for E1-009 the count 8 includes 2 proof rows, so "8 build actions" was already wrong by 2.

Now write the report. Keep concise but with exact quotes. Use table. The final proof row exact quotes are long; I'll quote the full row? The instruction: "The final 'proof' developer action row (A8/A9/A10) exactly as written, or 'none'." Full row is very long (3-4 sentences). Maybe quote the row as "# + title + key clause" with exact quotes of the action and done-when. To keep the table readable, I'll put the row ID + title + the proo

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "python -c \"\nimport json,re\np=r'C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\stories_full.json'\nd=json.load(open(p,encoding='utf-8'))\ng={s['key']:s for s in d}\nfor k in ['RWB-E1-009','RWB-E1-010','RWB-E1-005']:\n    t=g[k]['text']\n    print('='*70); print(k)\n    i=t.find('16. Test cases'); j=t.find('17. Guardrails',i)\n    seg=t[i:j]\n    for l in seg.split('\\n'):\n        if l.startswith('| TC-') or l.startswith('| ID'):\n            print(l)\n\""}
```

```text
======================================================================
RWB-E1-009
| ID | Covers | Level | Data |
| TC-E1-009-01 | AC1, BR1, BR6 | System | Synthetic CCMS file of 31,200 records and 33,050 links; SVAF file of 2,140 appraisals |
| TC-E1-009-02 | AC2 | System | Completed loads; 50 random cases with collateral |
| TC-E1-009-03 | AC3, BR4 | System | Appraisals dated 2025-11-26 and 2025-11-27 |
| TC-E1-009-04 | AC4, BR2 | System | Adapter stub refusing the CCMS file |
| TC-E1-009-05 | AC5, BR3 | System | 120 of 33,050 links with unknown account keys |
| TC-E1-009-06 | AC6, BR3 | System | 4 appraisals with unknown collateral numbers |
| TC-E1-009-07 | AC7, BR3 | System | 2 records with collateral type K7 |
| TC-E1-009-08 | AC8, BR3 | System | 180 of 33,050 links with unknown account keys |
| TC-E1-009-09 | AC9, BR5 | System | No SVAF file by 2026-12-01 04:00 |
| TC-E1-009-10 | AC10, BR8 | System | ValuationRecordApi forced to fail after 1,000 records |
| TC-E1-009-11 | AC11, BR7 | System | Second call for interface run IR-0000451 |
| TC-E1-009-12 | Access | Access | RW-DATASTEW calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
======================================================================
RWB-E1-010
| ID | Covers | Level | Data |
| TC-E1-010-01 | AC1, BR1, BR7 | System | Synthetic LIT-07 file of 1,240 matched rows |
| TC-E1-010-02 | AC2, BR4 | System | LIT-07 loaded with 1,240 rows; LIT team manager |
| TC-E1-010-03 | AC3, BR2 | System | LIT-07 file with 17 rows without account numbers |
| TC-E1-010-04 | AC4, BR3 | System | Field list with two personal fields |
| TC-E1-010-05 | AC5, BR2 | System | 5 rows with unknown account numbers |
| TC-E1-010-06 | AC6, BR4 | System | Confirmed count 1,251 against 1,240 |
| TC-E1-010-07 | AC7, BR5 | System | One user with RW-DATASTEW and RW-TEAMMGR |
| TC-E1-010-08 | AC8 | System | NPA team manager signs LIT-07 |
| TC-E1-010-09 | AC9, BR1 | System | Tracker TDR-03 with decision KEEP |
| TC-E1-010-10 | AC10, BR6 | System | Same file hash twice |
| TC-E1-010-11 | AC11 | System | Second file of 1,262 rows before sign-off |
| TC-E1-010-12 | AC12 | System | PDF file |
| TC-E1-010-13 | AC13 | System | File without the column Court name |
| TC-E1-010-14 | Access | Access | RW-TEAMMGR uploads a file; refused with MSG-P4-002 |
======================================================================
RWB-E1-005
| ID | Covers | Level | Data |
| TC-E1-005-01 | AC1, BR1,
... truncated (3,160 chars total)
```

### Assistant - 2026-11-12 00:52 | opencode-go/deepseek-v4.1-flash | general

## Scope

Read-only. Source: `stories_full.json` (332 stories). No files changed.

---

## 1. Final proof row, intro, count, Done-when

| Story | Final proof action row (exact) | Dev actions | Intro sentence (exact) | Done-when (exact) |
|---|---|---|---|---|
| RWB-E1-003 | **A10 "Prove the 14 ACs and publish the read interface"** — "Run TC-E1-003-01 to TC-E1-003-15. Run the full synthetic day of 184,500 accounts and 2,310 payments in SIT and record the elapsed time. Implement and publish LoadRunQuery, and walk the platform administrator through the job list, the rerun and the LATE path." Done when: "Fourteen of fourteen AC tests pass, the full synthetic run is under 30 minutes, and P3 can read a completed load through LoadRunQuery. AC1 to AC14" | 10 build actions | "**Work in this order.** A1 to A9 are code. A10 is the proof. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies." | "**Done when.** The tests in section 16 pass, and a full synthetic run of 184,500 accounts completes in under 30 minutes in SIT." |
| RWB-E1-004 | **A10 "Prove the 10 ACs and demo the late path"** — "Run TC-E1-004-01 to TC-E1-004-11. Capture the run row, the mapping version, the held and skipped counts, the DP05 freshness row and the case-list enrichment. Rehearse the 08:00 late path and the unapproved mapping refusal." Done when: "Ten of ten AC tests pass, and the data steward can explain held, skipped and refused from the run row. AC1 to AC10" | 10 build actions | "**Work in this order.** A1 to A9 are code. A10 is the proof. …" (same tail) | "**Done when.** The tests in section 16 pass." |
| RWB-E1-005 | **A8 "Prove the eight ACs and load the SIT inventory"** — "Run TC-E1-005-01 to TC-E1-005-09. Load TRK-2026.11 in SIT and confirm at least one row for each of the six teams. Hand the 14 LOAD trackers to RWB-E1-010 and the 6 RETIRE trackers to RWB-E1-012." Done when: "Eight of eight AC tests pass, the SIT inventory holds all six teams, and the 010 and 012 leads have their lists. AC1 to AC8" | 8 build actions | "**Work in this order.** A1 to A7 are code. A8 is the proof. …" (same tail) | "**Done when.** The tests in section 16 pass, and the SIT inventory version holds at least one row for each of the six teams." |
| RWB-E1-007 | **A10 "Add the contract and boundary tests and prove the 9 ACs"** — "Add the contract test template for a new interface, using the 120-record INT-15 sample. Add AdapterBoundaryTest to the pipeline so no SFTP or file-system call compiles outside recovery.integration.adapter. Run TC-E1-007-01 to TC-E1-007-10 and the INT-10 and INT-14 contract tests in SIT." Done when: "Nine of nine AC tests pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT. AC1 to AC9" | 10 build actions | "**Work in this order.** A1 to A9 are code. A10 is the proof. …" (same tail) | " - **Done when:** the tests in section 16 pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT." (bullet form, not the `**Done when.**` pattern) |
| RWB-E1-009 | **A8 "Run the 11 ACs and hand DP06 over"** — "Run TC-E1-009-01 to TC-E1-009-12. Capture both run rows, the link counts, the age boundary, the sample and the failed valuation rollback. Walk the S5 and valuation leads through ValuationRecordApi and the stale flag." Done when: "Eleven of eleven AC tests pass, and S5 can read and update appraisals only through ValuationRecordApi. AC1 to AC11". **A7 is also proof:** "Prove the failed valuation write and the access path" | 8 build actions | "**Work in this order.** A1 to A6 are code. A7 and A8 are the proof. …" (same tail) | "**Done when.** The tests in section 16 pass." |
| RWB-E1-010 | **A9 "Prove the 13 ACs and hand SIGNED_OFF to retirement"** — "Run TC-E1-010-01 to TC-E1-010-14. Capture the upload Job, the row counts, the reject list, the personal-field count and every sign-off refusal. Hand the SIGNED_OFF trackers and their signed_off_at dates to RWB-E1-012." Done when: "Thirteen of thirteen AC tests pass, and the retirement lead can see which trackers are SIGNED_OFF and when the parallel period starts. AC1 to AC13" | 9 build actions | "**Work in this order.** A1 to A8 are code. A9 is the proof. …" (same tail) | "**Done when.** The tests in section 16 pass, and the 14 LOAD trackers of the SIT inventory load from synthetic files." |
| RWB-E1-012 | **A8 "Prove the 10 ACs and file the release report"** — "Run TC-E1-012-01 to TC-E1-012-11. Capture the retirement fields, the unfed list, the parallel-period refusal, the repeat and the version conflict. Produce the six-team report for 26 November and walk the Tribe lead through filing it with the 30 November release checklist." Done when: "Ten of ten AC tests pass, and the report shows six teams with outstanding 0 for the full fixture. AC1 to AC10" | 8 build actions | "**Work in this order.** A1 to A7 are code. A8 is the proof. …" (same tail) | "**Done when.** The tests in section 16 pass, and the SIT retirement report shows the six teams." |

Full intro tail (all 7): "Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies."

---

## 2. Data-load / SIT / synthetic / fixture / demo clauses in other rows

| Story | Row | Clause (exact) | Where |
|---|---|---|---|
| RWB-E1-003 | A1 | "The migration runs clean in SIT, and a second run for the same interface and business date is refused by the database. AC11, AC12" | Done when |
| RWB-E1-003 | A6 | "…11 are held in the 0.48 percent fixture…" | Done when |
| RWB-E1-004 | — | none | — |
| RWB-E1-005 | A1 | "The migration runs clean in SIT, and a second row with the same tracker code and version is refused. AC1, AC7" | Done when |
| RWB-E1-005 | A6 | "The reference data administrator loads TRK-2026.11, the data steward confirms it, and GET /admin/trackers returns the new version only after that confirmation. AC1, AC8" | Done when |
| RWB-E1-007 | A3 | "Add a pass and a fail fixture per check type." | What to build |
| RWB-E1-009 | — | none | — |
| RWB-E1-010 | A8 | "Load all 14 LOAD trackers of the SIT inventory from synthetic .xlsx and .csv files." | What to build |
| RWB-E1-010 | A8 | "…and all 14 LOAD trackers load and reconcile. AC3" | Done when |
| RWB-E1-012 | — | none | — |

---

## 3. Simplest removal

Delete the proof row(s) outright; strip the clauses above; change only the count, intro and Done-when. **No renumbering needed** — every remaining range stays contiguous (A1–A6, A1–A7, A1–A8, A1–A9).

| Story | Delete | Edit surviving row | New "Developer actions" | New intro | New Done-when |
|---|---|---|---|---|---|
| E1-003 | A10 | A1: drop "in SIT" → "The migration runs clean, and a second run for the same interface and business date is refused by the database. AC11, AC12". A6: "fixture" → "case" | 9 build actions, in the plan after the preconditions | "**Work in this order.** A1 to A9 are code. Each action ends with a check that can be shown in review; the AC numbers at the end of the last column show which acceptance criteria the action satisfies." | "**Done when.** The tests in section 16 pass." |
| E1-004 | A10 | none | 9 build actions, … | same, "A1 to A9 are code." | unchanged: "**Done when.** The tests in section 16 pass." |
| E1-005 | A8 | A1: drop "in SIT" → "The migration runs clean, and a second row with the same tracker code and version is refused. AC1, AC7". A6: "A new tracker_inventory version loaded through POST /admin/reference-loads is confirmed by the data steward, and GET /admin/trackers returns it only after that confirmation. AC1, AC8" | 7 build actions, … | same, "A1 to A7 are code." | "**Done when.** The tests in section 16 pass." |
| E1-007 | A10 | A3: drop "Add a pass and a fail fixture per check type." | 9 build actions, … | same, "A1 to A9 are code." | "- **Done when:** the tests in section 16 pass." |
| E1-009 | A7 **and** A8 | none | 6 build actions, … | same, "A1 to A6 are code." | unchanged: "**Done when.** The tests in section 16 pass." |
| E1-010 | A9 | A8 title → "Expose the rejected rows"; What-to-build → "Make the TRK-01 and TRK-02 rows visible through GET /admin/data-quality/exceptions with product DP07."; Done-when → "The 17 rejected LIT-07 rows are returned by the exceptions view. AC3" | 8 build actions, … | same, "A1 to A8 are code." | "**Done when.** The tests in section 16 pass." |
| E1-012 | A8 | none | 7 build actions, … | same, "A1 to A7 are code." | "**Done when.** The tests in section 16 pass." |

---

## Notes / caveats

- **E1-003 A10** is the only action row that builds `LoadRunQuery`, but it is already a named component, build step 7 in section 13, and the published interface in section 12. Deleting A10 loses no build. If you want it explicit in the plan, append "Implement and publish LoadRunQuery." to A9 — no renumbering.
- **E1-007 A10** carries two build items (contract test template, `AdapterBoundaryTest`), both already in section 13 build step 8: "Add the contract test template and the AdapterBoundaryTest to the pipeline." Deletion is safe; keep step 8.
- **E1-009 A7 is proof too** (intro says "A7 and A8 are the proof"). Deleting only A8 would leave a proof row under a false intro. Its 403 access case is duplicated by TC-E1-009-12.
- Hand-offs survive deletion in standalone **Hand-off:** paragraphs for E1-005, E1-010, E1-012 and E1-007.
- Every proof row's "N of N AC tests" clashes with its own test-case range (e.g. E1-004 "Ten of ten" vs TC-01…11; E1-012 "Ten of ten" vs TC-01…11). Deletion removes the mismatch.
- Existing inconsistency to preserve or normalise: E1-007 uses a bullet `- **Done when:**` instead of the `**Done when.**` paragraph used by the other six.
- The attribute count is wrong today in all seven stories ("10 build actions" while one row is proof); the new counts make it true.

<details><summary>Reasoning</summary>

Confirmed: E1-009's A7 access test is duplicated in TC-E1-009-12 (Access). E1-010's A9 proof has 14 tests covering 13 ACs + access. Good.

Also note E1-009's A8 says "Run TC-E1-009-01 to TC-E1-009-12" but claims "Eleven of eleven ACs" — 12 tests, 11 ACs, consistent.

Now I have everything. Let me also note the "Developer actions" attribute counts and that each story's attribute says "build actions" while including proof rows.

One more: check E1-003 section 16 counts 15 test cases for 14 ACs. Fine.

I'll write the final report now. Keep it tight. Use exact quotes.

Format:

## Scope
7 stories, payload as source. No files changed.

### 1. Final proof row + intro/count/Done-when

Table columns: Story | Final proof action (exact) | Dev actions | Intro (exact) | Done-when (exact)

Rows long. Fine.

### 2. Other data-load/SIT/synthetic/fixture clauses

Table: Story | Row | Clause (exact) | Location

E1-003 A1, A6; E1-005 A1, A6; E1-007 A3; E1-010 A8 (+A8 done-when). E1-004 none, E1-009 none, E1-012 none.

Also note E1-009 A7 is proof (not "other"), flagged in section 1.

### 3. Recommendation
Per story table: Delete | Edit | New count | New intro | New Done-when.
Then notes.

Let me make sure to state "Do not renumber" — confirm ranges remain contiguous.

For E1-007 new Done-when: "- **Done when:** the tests in section 16 pass." Keep bullet and bold colon to match existing formatting.

For E1-003 new A1 done-when exact: "The migration runs clean, and a second run for the same interface and business date is refused by the database. AC11, AC12"
For E1-005 new A1: "The migration runs clean, and a second row with the same tracker code and version is refused. AC1, AC7"
E1-003 A6 new: "2,299 payments load and 11 are held in the 0.48 percent case; a second call inserts nothing twice. AC6, AC7, AC12"
E1-005 A6 new: "The reference data administrator loads a tracker_inventory version, the data steward confirms it, and GET /admin/trackers returns the new version only after that confirmation. AC1, AC8" — hmm, "loads a tracker_inventory version" is vague. Better: "A new tracker_inventory version loaded through POST /admin/reference-loads is confirmed by the data steward, and GET /admin/trackers returns it only after that confirmation. AC1, AC8". That's a code check, no specific fixture TRK-2026.11. Good.

E1-010 A8 new title: "Expose the rejected rows"
new What to build: "Make the TRK-01 and TRK-02 rows visible through GET /admin/data-quality/exceptions with product DP07."


_[truncated]_

</details>
