# Inventory Epic 1 parameters

- **Session ID:** `ses_e3acfaff8ffeKw5aeiqavnZiw7`
- **Created:** 2026-11-10 18:20  |  **Last activity:** 2026-11-10 18:25
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `explore`
- **Parent session:** RWB-TE-005 spec clarifications (`ses_e3b1d19eeffeAOQ3VdCtcEaqiQ`)
- **Tokens:** 123,669 in / 27,523 out / 19,560 reasoning
- **Messages:** 28

---

### User - 2026-11-10 18:20

You are a subagent spawned by another session.
Very thorough. Work in C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14.

Task: build a complete inventory of every PARAMETER KEY named in the Epic 1 and Epic 2 user story files, for the RWB-E1-042 parameter catalog seed.

Read every .md file in:
- 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\ (all files)
- 04 User stories\Recovery Workbench User Stories Epic 2 v5.md
- 04 User stories\Recovery Workbench Build Notes Epic 1 v4.md
- 04 User stories\Recovery Workbench Build Notes Epic 2 v2.md

Find every parameter key: dotted lower-case identifiers like case.entry.dpd, refdata.cache.ttl-seconds, caselist.export.maxrows, recon.caselist.tolerance.pct, servicelevel.required-statuses, allocation.retry.limit, etc. Look for patterns: "parameter `x`", "Parameter x = y", "parameter \"x\"", "configuration ... x", "key x", "catalog entry x".

For EACH key report in a table:
| key | default value (and whether stated or assumed) | value type (INTEGER/DECIMAL/BOOLEAN/STRING/TIME/DURATION/CODE_LIST/JSON) | unit | min | max | scope GLOBAL/PRODUCT | required true/false | owner role | environments | used_by packages/modules | source file and line | notes |

Rules:
- Do NOT invent values. If a value is not stated, write UNKNOWN.
- Mark assumption markers: "assumed", "DLnn", "TBD".
- List separately any key that is explicitly used as a NEGATIVE test fixture (a key that must NOT be in the catalog), e.g. allocation.retry.limit in AC3 of E1-042.
- Include environment settings and secrets.
- Deduplicate keys but note all source citations.

Also report any parameter whose name differs between documents for the same concept (e.g. case.entry.dpd vs case.entry.dpd_threshold) and flag it as a naming conflict.

Return the full table and a short summary of counts and conflicts. Do not modify files.

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

I'll start by exploring the directory structure to find all the target files.

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Path \"04 User stories\" -Recurse -File | Select-Object FullName, Length | Format-Table -AutoSize | Out-String -Width 200", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text

FullName                                                                                                                                                                                                
--------                                                                                                                                                                                                
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Acceptance Criteria Glossary v1.xlsx                                                              
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v2.md                                                                      
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v2.xlsx                                                                    
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md                                                                          
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 2 v2.md                                                                          
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Technical Enablers v1.md                                                              
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Data Migration Stories v2.md                                                                      
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Data Migration Stories v2.xlsx                                                                    
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench How To Read The Acceptance Criteria v1.docx                                                       
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx                                                  
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User
... truncated (20,612 chars total)
```

**Tool `glob`** - completed

```json
{"pattern": "04 User stories/**/*.md"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Administration Stories v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Data Migration Stories v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Technical Enablers v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 2 v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Technical Enabler Stories v5.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Story Worked Example v6.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epics 3 to 8 v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v5.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 v7.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 008 Decision log store v1 append only and hash chained v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 007 Integration adapters for file loads and outbound files v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 006 Data quality rules v1 v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 005 Excel and SharePoint inventory v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 003 ALS daily extract load v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 004 EFS extract load v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v
... truncated (16,403 chars total)
```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

Let me check file sizes and start with the core configuration story (E1-042), which defines the catalog.

<details><summary>Reasoning</summary>

There are ~70 Epic 1 story files plus Epic 2 and build notes. I need to read them all. Let me be efficient: grep for dotted lower-case identifiers across the target files first, then read files systematically.

Let me first check total sizes.

</details>

**Tool `shell`** - completed

```json
{"command": "$files = Get-ChildItem -Path \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\" -Filter *.md; $files | Sort-Object Name | ForEach-Object { \"{0,7} {1}\" -f $_.Length, $_.Name }; \"\"; \"COUNT: $($files.Count)\"; \"TOTAL: $(($files | Measure-Object Length -Sum).Sum)\"; Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\" | Select-Object Length,Name | Format-Table -AutoSize | Out-String", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
    993 Read me first v1.md
  27937 RWB E1 001 Recovery tables for the 14 data products v1.md
  22621 RWB E1 002 Case list v1 with case ID owner and queue v1.md
  27769 RWB E1 003 ALS daily extract load v1.md
  21282 RWB E1 004 EFS extract load v1.md
  17617 RWB E1 005 Excel and SharePoint inventory v1.md
  21315 RWB E1 006 Data quality rules v1 v1.md
  24035 RWB E1 007 Integration adapters for file loads and outbound files v1.md
  18276 RWB E1 008 Decision log store v1 append only and hash chained v1.md
  21950 RWB E1 009 CCMS and SVAF loads v1.md
  23405 RWB E1 010 Excel and SharePoint loads v1.md
  19666 RWB E1 011 Reconciliation and data quality report v1.md
  17917 RWB E1 012 Retire local copies v1.md
  18403 RWB E1 013 Baseline measures v1.md
  19903 RWB E1 014 Decision log copy to the data lake v1.md
  18491 RWB E1 015 Freshness stamp per data product v1.md
  19783 RWB E1 016 Access control per data product and catalog entries v1.md
  19875 RWB E1 017 Retention and archive rule for the data store v1.md
  24023 RWB E1 018 Case ID issuance and case record v1 v1.md
  20322 RWB E1 019 Roles teams and queues as data v1.md
  27738 RWB E1 020 Allocation and assignment engine v1 v1.md
  22841 RWB E1 021 Transfer rules and engine v1 v1.md
  22459 RWB E1 022 Sign on with SSO MFA and the first roles v1.md
  18731 RWB E1 023 Case record view v1 read only v1.md
  26814 RWB E1 024 Document store and index v1.md
  18082 RWB E1 025 Document types and fields agreed v1.md
  20029 RWB E1 026 Attach and search screen v1.md
  16506 RWB E1 027 Decision log writer v1 v1.md
  22160 RWB E1 028 Service levels timers escalation and prescription dates v1.md
  20571 RWB E1 029 Rule load validation and rollback v1.md
  16841 RWB E1 030 Daily rebalancing and queue measures v1.md
  14047 RWB E1 031 Queue and owner on the case list with filters v1.md
  26002 RWB E1 032 Automatic attach from the OCR intake v1.md
  18400 RWB E1 033 Search across cases v1.md
  19167 RWB E1 034 Letter template management v1.md
  13900 RWB E1 035 Case record view v1 1 with documents and history timeline v1.md
  25782 RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md
  22753 RWB E1 038 Delegation of authority table as reference data v1.md
  23217 RWB E1 039 Access log into the decision log and break glass admin v1.md
  18388 RWB E1 040 Document checklist per case type as reference data v1.md
  21203 RWB E1 041 Retention classes and v
... truncated (5,281 chars total)
```

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

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

Now let me systematically extract candidate dotted identifiers across all target files.

<details><summary>Reasoning</summary>

Now I understand the structure. I need to read ~82 files. That's ~1.55MB of text plus 1.47MB for the 3 big docs. Too much to read fully within context. But I have a large context. Let me be strategic.

First, grep for parameter key patterns across all target files to build a candidate list. Then read the "Configuration and reference data" sections of each story which likely list keys.

Let me grep for dotted lower-case identifiers. Pattern: `\b[a-z][a-z0-9]*(?:[.-][a-z0-9]+)+\b` — but this will match a lot (file names, packages, versions). Better to use a heuristic: find backtick-quoted tokens with dots, and things like "parameter `x`".

Let me try grep with a pattern for dotted keys with at least 3 segments.

Actually the grep tool returns matches with line numbers. Let me do it per-directory to get manageable chunks. Let me first count.

Let me run ripgrep-ish via grep tool. I'll use pattern for backticked dotted tokens.

Let me test a few greps in parallel:
1. `[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*){2,}` in the Epic 1 story files dir
2. Same for Epic 2 file
3. Same for build notes

But these will return many lines (limit 100). Better use shell with rg-like Select-String and count, then iterate.

Actually the shell is PowerShell. I can use `Select-String -AllMatches` and output unique matched tokens with counts. That's read-only. Let me do that — it's a great way to build the candidate inventory.

Let me write a PowerShell command that:
- Reads all target files
- Finds all matches of regex `\b[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}\b`
- Outputs unique tokens sorted with count and file list

Hmm, keys may be 2 segments (rare). Most examples have 3+ segments. Let's use {2,} to reduce noise, and separately handle backticked 2-segment tokens.

Let me be careful with PowerShell quoting in the command string. Use single quotes for regex inside double-quoted command? The command is passed to powershell. Let me use a here-string approach or escaping.

I'll write:

$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'

That should work.

Let me also capture context: line numbers. I'll output for each unique token: count, and list of "file:line".

That could be huge. Let me first get the unique token list with counts, then decide.

Let's go.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$h = @{}\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    foreach ($m in $rx.Matches($line)) {\n      $t = $m.Value.TrimEnd('.')\n      if (-not $h.ContainsKey($t)) { $h[$t] = New-Object System.Collections.ArrayList }\n      [void]$h[$t].Add(\"$($f.Name):$ln\")\n    }\n  }\n}\n\"UNIQUE TOKENS: $($h.Count)\"\n$h.GetEnumerator() | Sort-Object Name | ForEach-Object { \"{0,5}  {1}\" -f $_.Value.Count, $_.Name }", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
UNIQUE TOKENS: 460
    4  ace.db.password
    3  allocation.deviation.queue.code
    3  allocation.exception.queue.code
    3  allocation.retry.limit
    8  appraisal.max.age
    1  appraisal-0003.pdf
    4  a-z0-9
    1  b0c7a1e-0000-4000-8000-000000000001
    4  booking.missing.grace
    1  break-glass-grants
   40  case.entry.dpd
    1  case.queue.note
    3  caselist.allocation.wait.until
   11  caselist.export.maxrows
    4  caserecord.section.timeout.ms
    2  caseview.deviation-timeout-ms
    2  config.cache.ttl-seconds
    1  confirm-before-publish
    2  court-notice-0007.pdf
    1  demand-mtg-th-v3.docx
    4  efs.history.action.codes
    1  eicar-0001.pdf
    2  eicar-0002.pdf
    1  emplate-to-document-type
    5  end-to-end
    1  extract-fields-v1
    4  intake-summary-v1
    1  intake-summary-v1.json
    1  java.net.http
    1  jobs.allocation.deadline
    3  jobs.catch-up.max-dates
    1  jobs.timer-check.cron
    1  legacy-seed.sql
    3  legal.prescription.warn.days
    3  legal-pack-v1
    1  legal-pack-v1.json
    1  letter-0002.docx
   11  load.hold.tolerance.pct
    8  load.movement.tolerance.pct
    3  load.retry.interval
    3  load.sample.size
    6  load.window.end
    1  macro-0001.docx
    1  mailroom-0001.pdf
    1  masked-copy-loader
    1  minutes-0002.xlsx
    2  no-collection-import
    2  notice-0001.pdf
    1  notice-0005.pdf
    1  notice-0006.pdf
    1  not-on-a-case
    1  off-by-default
    1  once-per-date
    1  org.quartz.impl.jdbcjobstore
    4  org.quartz.job
    1  org.quartz.scheduler.instance
    1  org.springframework.scheduling.quartz
    4  out-of-scope
    6  parameter-catalog.csv
    2  pdpa-allow.yaml
    3  pdpa-rules.yaml
    6  plan.warn-days
    5  prescription.warning-days
    2  queue.cap.max
    1  queueview.page-size.default
    1  queueview.page-size.max
    5  recon.caselist.tolerance.pct
    4  recon.efs.alert
    4  recon.efs.clean
    6  recon.tolerance.pct
    4  recovery.access.accesslog
    1  recovery.access.api
    3  recovery.access.delegation
    3  recovery.access.matrix
    2  recovery.access.partner
    5  recovery.access.signin
    2  recovery.accessadmin.ruleversions
    8  recovery.agent.api
    1  recovery.agent.client
    1  recovery.agent.config
    1  recovery.agent.eval.extraction
    1  recovery.agent.eval.report
    2  recovery.agent.intake
    1  recovery.agent.legal
    1  recovery.agen
... truncated (15,047 chars total)
```

### Assistant - 2026-11-10 18:20 | opencode-go/deepseek-v4.1-flash | explore

Now let me pull the exact context lines for every candidate key so I can classify precisely.

<details><summary>Reasoning</summary>

Now I have 460 unique tokens. I need to filter to actual PARAMETER KEYS (configuration/parameter keys) vs package names, file names, feature flags, message codes, roles.

Key distinction: The task says "parameter key" — dotted lower-case identifiers like case.entry.dpd. But also "Include environment settings and secrets" and feature flags? Feature flags are separate (rwb.p3.configservice is a feature flag, not a parameter catalog entry... but E1-047 might define flags as a separate catalog). Task says "for the RWB-E1-042 parameter catalog seed". So parameters that go in parameter_catalog.

However, feature flags `rwb.*` appear as feature flags in stories. E1-042 mentions `rwb.p3.configservice` as a Feature flag — not a catalog entry. But I should report them, at least note separately. The user asked for "every PARAMETER KEY named in the Epic 1 and Epic 2 user story files". Also "Include environment settings and secrets."

Let me identify parameter candidates:
- ace.db.password (secret, ENVIRONMENT kind)
- allocation.deviation.queue.code?
- allocation.exception.queue.code
- allocation.retry.limit (negative fixture)
- appraisal.max.age
- booking.missing.grace
- case.entry.dpd
- case.queue.note
- caselist.allocation.wait.until
- caselist.export.maxrows
- caserecord.section.timeout.ms
- caseview.deviation-timeout-ms
- config.cache.ttl-seconds
- efs.history.action.codes
- jobs.allocation.deadline
- jobs.catch-up.max-dates
- jobs.timer-check.cron
- legal.prescription.warn.days
- load.hold.tolerance.pct
- load.movement.tolerance.pct
- load.retry.interval
- load.sample.size
- load.window.end
- plan.warn-days
- prescription.warning-days
- queue.cap.max
- queueview.page-size.default
- queueview.page-size.max
- recon.caselist.tolerance.pct
- recon.efs.alert / recon.efs.clean
- recon.tolerance.pct
- refdata.cache.ttl-seconds
- rules.testcases.min
- servicelevel.required-statuses
- timeline.source-timeout-ms
- timeline.type.order
- tracker.file.max.mb
- tracker.inventory.teams
- tracker.retire.parallel.days
- transfer.bulk.max
- rwb.access.* (breakglass etc.)
- rwb.agent.*
- rwb.approval.*
- rwb.calendar.bank-holidays
- rwb.comms.*
- rwb.customer.products.party-roles
- rwb.dataengine.*
- rwb.decision.*
- rwb.dochub.*
- rwb.flags.cache-seconds
- rwb.integration.*
- rwb.jobs.*
- rwb.maskedcopy.*
- rwb.p1.collins.*.table
- rwb.refload.approver.*
- rwb.reporting.baseline-date
- rwb.sandbox.*
- spring.flyway.*
- rwb.p3.* feature flags

I need to determine which of these are

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\n$count = 0\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $count++ }\n  }\n}\n\"LINES WITH CANDIDATE KEYS: $count\"", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
LINES WITH CANDIDATE KEYS: 567

```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

567 lines. That's manageable if lines are short, but many are long Gherkin lines. ~567 * ~200 chars = 113k chars ≈ 30k tokens. Acceptable. But some lines are very long tables.

Actually, I realize many of these will be in Gherkin scenarios, which is good — that tells me defaults and behavior.

Let me output them in batches by file group to avoid truncation. Let's start with E1 001-010.

Actually, better: output per-file with filename header, batch of ~4-5 files at a time. Let's estimate ~10 batches. That's fine.

Alternatively I can output all 567 lines truncated to 400 chars each — that's ~230KB, too big for one tool result (will be truncated to a file). The tool auto-truncates and saves full output to a file, but then I'd need to read that file.

Let me do batches of files. I'll start with key configuration-heavy files: 001, 002, 003, 004, 005.

Wait — I should also make sure I catch 2-segment keys and keys that appear only once in prose. The regex requires 2+ separators (3+ segments). Most keys have 3+. But e.g. `case.queue.note` is 3. Fine.

However, some keys might be 2-segment like `load.retry`? Unlikely. But let me also check backticked tokens with 1+ separator to catch anything missed. I'll do that as a separate pass.

Let me now dump context lines for the first batch of files.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -First 6\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== Read me first v1.md =====
===== RWB E1 001 Recovery tables for the 14 data products v1.md =====
329| **Feature flag.** `rwb.p1.data-catalog`. The flag covers the catalog handler; the migration is not behind a flag.
===== RWB E1 002 Case list v1 with case ID owner and queue v1.md =====
36| - Parameters are loaded: `case.entry.dpd` 90 (DL16), `recon.caselist.tolerance.pct` 0.00 (assumed, DL25), `caselist.allocation.wait.until` 07:15.
84| Given the parameters case.entry.dpd = 90 and recon.caselist.tolerance.pct = 0.00 are in force
162| | BR2 | The ALS count to match is the accounts at or above the entry threshold in loan_account, less the accounts excluded at entry | CTL-01; REC-01; parameter case.entry.dpd (DL16) |
163| | BR3 | The count check passes when the difference is within the tolerance | Parameter recon.caselist.tolerance.pct, 0.00 assumed (DL25) |
290| **Configuration and reference data.** Parameters `case.entry.dpd`, `recon.caselist.tolerance.pct` and `caselist.allocation.wait.until` from the parameter catalog, loaded by the center of excellence analyst. Lake path and alert recipient groups as configuration, set by the platform administrator. The Power BI data set and its 07:30 schedule are owned by the reporting and BI analyst.
303| **Feature flag.** `rwb.p1.case-list`. Off: JOB-04 skips the case list step.
===== RWB E1 003 ALS daily extract load v1.md =====
36| - Parameters are loaded: `load.window.end` 09:00, `load.retry.interval` 60 minutes, `load.hold.tolerance.pct` 0.50, `load.movement.tolerance.pct` 10.00, `load.sample.size` 50 (tolerances assumed, DL25).
88| Given the parameters load.hold.tolerance.pct = 0.50 and load.movement.tolerance.pct = 10.00 are in force
189| | BR2 | A record whose reference or code does not match is held in the exception list; above 0.50 percent the load is refused | DQ-005, DQ-006, DQ-012, DQ-013; parameter load.hold.tolerance.pct (assumed, DL25) |
190| | BR3 | A count or balance change above 10 percent against the previous load is loaded and alerted | DQ-007, DQ-014; parameter load.movement.tolerance.pct (assumed, DL25) |
281| | Input | COLLINS staging records and trailer for INT-01 and INT-02 in the ACE database; table names from `rwb.p1.collins.int01.table`, `rwb.p1.collins.int02.table`, `rwb.p1.collins.trailer.table` |
342| **Configuration and reference data.** Parameters `load.window.end`, `load.retry.interval`, `load.hold.tolerance.pct`, `load.movement.tolerance.pct`, `load.sample.size` 
... truncated (5,259 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Good. This is efficient. Let me continue with next batches.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 6 -First 6\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 006 Data quality rules v1 v1.md =====
36| - Parameter `case.entry.dpd` 90 (DL16) is loaded.
147| | BR7 | DQ03 uses the entry threshold of 90 days past due | Parameter case.entry.dpd (DL16) |
269| | DQ03 | Days past due mismatch | DP03 | case_list_row | RANGE days_past_due minimum case.entry.dpd |
274| | DQ08 | Missing classification | DP01 | loan_account | NOT_NULL classification where days_past_due at or above case.entry.dpd |
288| **Feature flag.** `rwb.p1.dq-rules`. Off: no rule runs; loads complete as before.
===== RWB E1 007 Integration adapters for file loads and outbound files v1.md =====
266| - **Configuration and reference data:** interface_config rows for INT-10 to INT-16 and INT-25, loaded by RW-REFADM through the reference data load; DQ-057 to DQ-098 load check rows (P1 reference data); property `rwb.integration.sftp.host` per environment; SFTP key in the key store.
276| - **Feature flag:** `rwb.integration.file-adapters`.
293| SCR-09 Exception queue (E1), states Loading and list: the platform administrator sees failed outbound items with the interface, attempt count, last error and case count, and resends an item. The data steward receives the refused load alert by email from the Log Analytics alert rule on event `rwb.integration.load.refused`.
===== RWB E1 008 Decision log store v1 append only and hash chained v1.md =====
207| - Configuration and reference data: property rwb.decision.chain.genesis-hash (64 zeros); notification group for Compliance in the ACE notification path; retention class per DL26.
216| - Feature flag: `rwb.decision.log-store`.
===== RWB E1 009 CCMS and SVAF loads v1.md =====
36| - Parameters are loaded: `appraisal.max.age` 365 days (assumed, MSG-S5-002 and CTL-27; DL11), `load.hold.tolerance.pct` 0.50 and `load.movement.tolerance.pct` 10.00 (assumed, DL25).
49| 8. System: for each appraisal, computes the age in days at the file's business date and sets the stale flag when the age is above `appraisal.max.age`.
85| Given the parameter appraisal.max.age = 365 is in force
164| | BR3 | Records with unknown references or codes are held; above 0.50 percent the file is refused | Parameter load.hold.tolerance.pct (assumed, DL25) |
165| | BR4 | An appraisal older than appraisal.max.age days at the business date is stale | Parameter appraisal.max.age, 365 assumed (MSG-S5-002, CTL-27; DL11) |
264| **Configuration and reference data.** Parameters `appraisal.max.age`, `load.hold.tolerance.pct` and `load
... truncated (4,416 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Continue with next batch.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 12 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 012 Retire local copies v1.md =====
35| - Parameters are loaded: `tracker.retire.parallel.days` 2 working days, `tracker.inventory.teams` (from RWB-E1-005).
80| Given the parameter tracker.retire.parallel.days = 2
145| | BR2 | A LOAD tracker is retired only after its load is signed off and the team has used the case list for the parallel period | Parameter tracker.retire.parallel.days, 2 working days |
236| **Configuration and reference data.** Parameter `tracker.retire.parallel.days` from the parameter catalog, loaded by the center of excellence analyst. The working day calendar from the reference data service. The team list from `tracker.inventory.teams`.
248| **Feature flag.** `rwb.p1.tracker-retire`.
===== RWB E1 013 Baseline measures v1.md =====
36| - The baseline date is configured: `rwb.reporting.baseline-date` = 2026-11-27.
246| - Configuration and reference data: the six definitions, version MD-2026.11 (Tribe lead approves; RW-REFADM loads); age bands as a list, assumed values as in the Background, owner Tribe lead; `rwb.reporting.baseline-date` = 2026-11-27.
254| - Feature flag: `rwb.reporting.baseline`.
===== RWB E1 014 Decision log copy to the data lake v1.md =====
249| - Configuration and reference data: properties `rwb.dataengine.lake.container`, `rwb.dataengine.lake.path-prefix=decision-log`, `rwb.dataengine.lake.page-size=5000`, `rwb.dataengine.lake.rows-per-file=50000` (platform administrator, per environment); retention rule row DP12 LAKE_COPY loaded by the reference data administrator and approved by Compliance (RWB-E1-017).
259| - Feature flag: `rwb.dataengine.lake-copy`.
===== RWB E1 015 Freshness stamp per data product v1.md =====
238| - Configuration and reference data: data_product.refresh_cycle and expected_by, loaded by the data steward through RWB-E1-064; property `rwb.dataengine.freshness.alert-channel` set by the platform administrator.
248| - Feature flag: `rwb.dataengine.freshness-stamp`.
===== RWB E1 016 Access control per data product and catalog entries v1.md =====
258| - Feature flag: `rwb.dataengine.product-access`.
===== RWB E1 017 Retention and archive rule for the data store v1.md =====
257| - Configuration and reference data: retention version "RET-2026.11" (assumed 24 months for DP05 interaction until the bank schedule arrives; DL26) prepared by Compliance and loaded by the reference data administrator; properties `rwb.dataengine.retention.archive-container` and `rwb.dataengine.retent
... truncated (3,169 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Continue.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 19 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 019 Roles teams and queues as data v1.md =====
168| | BR8 | Cap range 1 to 500 | Parameter `queue.cap.max` = 500 (assumed; DL23), RWB-E1-042 |
286| - Parameter `queue.cap.max` = 500 (assumed; DL23) from RWB-E1-042.
300| **Feature flag.** `rwb.p3.queuetables`. Off: the applier does not run and the queue rows from the seed migration stay.
===== RWB E1 020 Allocation and assignment engine v1 v1.md =====
37| - Parameters loaded through RWB-E1-042: `allocation.exception.queue.code` = "RWB-EXC" and `allocation.deviation.queue.code` = "DEV-HANDLER" (assumed values; DL23).
345| - Parameters from RWB-E1-042: `allocation.exception.queue.code`, `allocation.deviation.queue.code`.
359| **Feature flag.** `rwb.p3.allocation`. Off: JOB-03 does not run and cases stay NEW.
===== RWB E1 021 Transfer rules and engine v1 v1.md =====
329| **Feature flag.** `rwb.p3.transfer`. Off: no rule transfers and the two endpoints return 404.
===== RWB E1 022 Sign on with SSO MFA and the first roles v1.md =====
256| - Configuration and reference data: role rows and group names (loaded by RW-REFADM after RWB-E1-019; names DL40); permission matrix PM-2026.11 (loaded by RW-REFADM, approved per RWB-E1-037); role conflict version SOD-2026.11 (loaded by RW-REFADM from the Separation of duty sheet); LOV-CAPABILITY and LOV-SCOPE; scope line wording from labels per DL10. Property `rwb.access.required-amr=mfa`.
266| - Feature flag: `rwb.access.sso-roles`.
===== RWB E1 023 Case record view v1 read only v1.md =====
266| - Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11) from RWB-E1-042.
278| **Feature flag.** `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only.
===== RWB E1 024 Document store and index v1.md =====
33| - RWB-TE-012 is done: the intake container, rwb-docs (standard), rwb-docs-legal (write-once) and rwb-quarantine exist, reached by managed identity through DocumentStorage.
39| - Feature flag rwb.dochub.store is on.
49| 7. DocumentStoreService: after commit, calls DocumentStorage.store (RWB-TE-012), which writes the file to rwb-docs-legal when write_once is true and to rwb-docs otherwise, at {container}/{caseId}/{documentId}/v1; the service sets storage_ref and state STORED.
97| Then the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1"
294| - Container names rwb-docs and rwb-docs-legal from RWB-TE-012, held as properties per environment.
302| 5. Call DocumentStorage after commit and build Copy
... truncated (3,002 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 26 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 026 Attach and search screen v1.md =====
38| - Feature flag rwb.dochub.casedocs is on.
250| - Property rwb.dochub.casedocs.page-size = 20.
260| **Feature flag.** `rwb.dochub.casedocs`. Off: the Documents tab is hidden and the endpoints return 404.
===== RWB E1 027 Decision log writer v1 v1.md =====
35| - Parameters in the catalog: rwb.decision.code.CASE_CREATED=D6, rwb.decision.code.OWNER_ASSIGNED=D6, rwb.decision.code.CASE_TRANSFERRED=D6, rwb.decision.code.DOCUMENT_ATTACHED=D6 (assumed; D6 is the entry and ownership decision; owner RW-DATASTEW).
134| | BR7 | Decision codes for the Epic 1 events are parameters, not code | Principle 1; parameters rwb.decision.code.* |
199| - Configuration and reference data: LOV-DECISION (RW-DATASTEW); parameters rwb.decision.code.* (RW-DATASTEW, values assumed); repeat counter exposed as metric decision_log_repeats_total in the job and service monitoring (RWB-E1-056).
207| - Feature flag: `rwb.decision.log-writer`.
===== RWB E1 028 Service levels timers escalation and prescription dates v1.md =====
37| - LEGAL_PERIOD row owned by Legal: HIRE_PURCHASE 2 years from the last payment date (assumed value from the current story; other products loaded by Legal). Parameter `legal.prescription.warn.days` = 180 (assumed) from RWB-E1-042.
293| - Parameter legal.prescription.warn.days = 180 (assumed; owner Legal) through RWB-E1-042.
299| 2. TimerStarter with stop-and-start on each case event; test AC1, AC4.
307| **Feature flag.** `rwb.p3.timers`. Off: no timers start and JOB-05 does nothing.
===== RWB E1 029 Rule load validation and rollback v1.md =====
287| - Parameter `rules.testcases.min` = 50 (assumed) through RWB-E1-042.
300| **Feature flag.** `rwb.p3.ruleload`. Off: the load and rollback endpoints return 404; the version in force stays.
===== RWB E1 030 Daily rebalancing and queue measures v1.md =====
272| **Feature flag.** `rwb.p3.rebalance`. Off: JOB-06 does not move cases; the snapshot still runs.
===== RWB E1 031 Queue and owner on the case list with filters v1.md =====
35| - Parameter `caselist.export.maxrows` = 10,000 (assumed; DL11) from RWB-E1-042.
56| | X4 | A filter names a queue outside the caller's scope | Only in-scope cases return; an out-of-scope queue returns none | MSG-P3-020 | AC6 |
98| Given parameter "caselist.export.maxrows" is 10000
134| | BR5 | An export holds at most the configured number of rows | Parameter caselist.export.maxrows = 10,000 (assumed; DL11) |
227| - Par
... truncated (2,926 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 33 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 033 Search across cases v1.md =====
38| - The user holds Documents R. Feature flag rwb.dochub.search is on.
245| **Feature flag.** `rwb.dochub.search`. Off: GET /documents/search returns 404 and the menu item is hidden.
===== RWB E1 034 Letter template management v1.md =====
235| - Configuration and reference data: property `rwb.comms.template.allowed-types` = DOCX; property `rwb.comms.template.max-size-mb` = 10, assumed; DL11. Merge field catalog loaded by RW-REFADM.
244| - Feature flag: `rwb.comms.template-admin`.
===== RWB E1 035 Case record view v1 1 with documents and history timeline v1.md =====
222| - Type order list held as parameter `timeline.type.order` (RWB-E1-042).
224| - Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11).
236| **Feature flag.** `rwb.p3.timeline`. Off: SCR-03 hides the Timeline panel and the endpoint returns 404.
===== RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md =====
38| - Parameters `rwb.refload.approver.permission=RW-SECADM` and `rwb.refload.approver.masking_rule=RW-COMPLY` are in the parameter catalog (RWB-E1-042).
161| | BR3 | A version is approved by the role the parameter names for the table, and never by the person who loaded it | Parameters rwb.refload.approver.*; Admin and access model, section 3.3; CTL-05 |
162| | BR4 | Scope filters records first and the permission is checked second; an out-of-scope record is never returned and the excluded count is never shown | role.default_scope (DF-REF-038); LOV-SCOPE; REQ-ACA-009 |
262| - Configuration and reference data: PM-2026.11 (RW-REFADM loads, RW-SECADM approves); MASK-2026.11 (RW-REFADM loads, RW-COMPLY approves; values DL26); parameters rwb.refload.approver.permission, rwb.refload.approver.masking_rule, rwb.access.membership-refresh-minutes=5 (assumed, DL38), rwb.access.mask.keep-last=4 (characters kept for identity and phone, assumed, DL26); LOV-CAPABILITY, LOV-SCOPE.
271| - Feature flag: `rwb.access.permission-matrix`.
290| No screen in this story. Matrix and masking versions arrive by file load until SCR-43 Roles and access and SCR-47 Personal data come in Epic 8. A person sees the effect in the menu (RWB-E1-022), in masked fields on the case record view (RWB-E1-023) and in 404 responses for out-of-scope cases.
===== RWB E1 038 Delegation of authority table as reference data v1.md =====
37| - Parameter `rwb.refload.approver.delegation_limit=RW-RISK` is in the parameter catalog (RWB-E1
... truncated (3,766 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 40 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 041 Retention classes and virus scan on intake v1.md =====
37| - Feature flags rwb.dochub.malware-scan and rwb.dochub.retention are on.
264| - Properties rwb.dochub.container.quarantine and rwb.dochub.scan.timeout-seconds = 30.
276| **Feature flags.** `rwb.dochub.malware-scan` and `rwb.dochub.retention`. With the scan flag off, intake items stay unscanned and are not read; uploads are refused with 503 and MSG-P5-022. With the retention flag off, JOB-17 lists due documents and archives none.
===== RWB E1 042 Central configuration service and parameter catalog v1.md =====
33| - The catalog seed file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, with the Epic 1 entries, including `case.entry.dpd` (default 90; DL16), `refdata.cache.ttl-seconds` (default 300; DL11) and `caselist.export.maxrows` (default 10000; DL11).
44| 5. RW-COE: loads a new value version through POST /admin/reference-loads with table "PARAMETER", for example `case.entry.dpd` = 91 in PROD valid from 2026-12-10.
83| Given the catalog lists "case.entry.dpd" as INTEGER, range 1 to 365, default 90, scope GLOBAL, required, owner RW-COE, used by "recovery.casewf.casecreation"
86| Given the parameter "case.entry.dpd" set to 90 in PROD, version 1
95| Then the output names the file, the line and the parameter "case.entry.dpd"
99| Given code that reads the key "allocation.retry.limit" which the catalog does not list
101| Then the build fails naming "allocation.retry.limit"
105| Given "refdata.cache.ttl-seconds" is required and has no value and no default for UAT
107| Then the health check fails with MSG-P3-032 for "refdata.cache.ttl-seconds" and "UAT"
111| When RW-COE loads "case.entry.dpd" = 400 for PROD
115| When RW-COE loads "case.entry.dpd" = "ninety" for PROD
124| Given "refdata.cache.ttl-seconds" is 30 in SIT and 300 in PROD
129| Given the catalog lists "ace.db.password" as kind ENVIRONMENT with secret = true
132| Then the system returns no value for "ace.db.password"
135| Given value version 2 of "case.entry.dpd" is in force and version 1 was in force before it
140| Given version 2 sets "case.entry.dpd" to 91 for PROD with valid from 2026-12-10 and is approved on 2026-12-05
256| - Cache time to live `config.cache.ttl-seconds` = 60 (assumed; DL11), itself a catalog entry.
269| **Feature flag.** `rwb.p3.configservice`. Off: services read the defaults from the generated keys only, and value loads are refused.
293| | TC-E1-042-01 | AC1, BR1
... truncated (7,132 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

E1-045 mentions "the five parameters in BR2". I need to read E1-045 more fully to get those parameters with scope PRODUCT. Let me note that and read E1-045 later.

Also E1-047 mentions `rwb.environment` — a property (2 segments). My regex requires 3 segments so missed it. I need a second pass for backticked 2-segment keys.

Let me continue with remaining files.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 47 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 048 Rule change audit report v1.md =====
242| **Feature flag.** `rwb.p3.change-log`. Off: approval runs the RWB-E1-043 checks only and the report endpoint returns 404.
===== RWB E1 049 OCR pipeline on the Workbench document hub v1.md =====
38| - Feature flag rwb.dochub.ocr is on.
237| - Property rwb.dochub.ocr.endpoint, set per environment by the platform administrator.
249| **Feature flag.** `rwb.dochub.ocr`. Off: ocrStep is skipped and items stay PENDING.
===== RWB E1 050 Document classification v1.md =====
38| - Feature flag rwb.dochub.classify is on.
241| - Property rwb.dochub.classify.model-route naming the gateway route set under DL33.
252| **Feature flag.** `rwb.dochub.classify`. Off: classifyStep is skipped and every scanned item goes to review with reason LOW_CONFIDENCE.
===== RWB E1 051 Legacy feed jobs on ADF and Control M v1.md =====
46| 7. SY-DATALOAD: on failure, the run row is FAILED or REFUSED, a structured event `rwb.integration.job.failed` is written to Log Analytics and the alert rule emails the data steward and the platform administrator with MSG-P2-004.
164| **Bank scheduler definitions.** Control-M jobs `RWB_ALS_EXTRACT` and `RWB_EFS_EXTRACT` and ADF pipelines `rwb-ccms-file-move` and `rwb-svaf-file-move`, held as JSON in `ops/control-m/` and `ops/adf/`. The names are proposed until SCB IT issues the bank standard names (DL12).
192| | JobFailureAlert | Rule table | Log Analytics alert rule on `rwb.integration.job.failed`, held as code in `ops/monitoring/` |
195| - **Configuration and reference data:** interface_config rows INT-01, INT-07, INT-10, INT-11 (RW-REFADM); properties `rwb.jobs.collins.start` = 05:00, `rwb.jobs.collins.last-retry` = 09:00, `rwb.jobs.files.weekly-cron` = Monday 04:00; Control-M and ADF definitions owned by RW-PLATADM.
204| - **Feature flag:** `rwb.integration.legacy-feeds`.
===== RWB E1 052 Notice generation v1 v1.md =====
271| - Feature flag: `rwb.comms.notice-generation`.
===== RWB E1 053 Field extraction for the six types into the index v1.md =====
37| - The step runs as SY-OCR (Documents CRU). Feature flag rwb.dochub.extract is on.
280| - Property rwb.dochub.extract.model-route for the gateway route (DL33).
292| **Feature flag:** `rwb.dochub.extract`. Off: extractStep sets extract_status DONE with no fields, and items continue to matchStep with the OCR text only.
===== RWB E1 054 Review queue for low confidence documents v1.md =====
36| - The officer holds RW-LITOFF (Doc
... truncated (2,681 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 54 -First 7\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 055 Proof of delivery capture design with WIN v1.md =====
263| - Configuration and reference data: `rwb.comms.dispatch.eligible-states` = GENERATED; `rwb.comms.dispatch.max-attempts` = 3 (INT-14); `rwb.comms.dispatch.barcode-break-days` = 3 (REC-05); `rwb.comms.pod.stale-after-business-days` = 1 (INT-15). Owner of the values: platform administrator through the configuration service.
272| - Feature flag: `rwb.comms.win-dispatch-v1`.
===== RWB E1 056 Run books and monitoring for every Epic 1 job v1.md =====
43| 4. Each job: writes a structured event `rwb.job.run` at start and end with job ID, business date, status and duration.
193| | JobRunEventListener | Listener | Spring Batch JobExecutionListener writing `rwb.job.run` at start and end |
209| - **Feature flag:** `rwb.integration.job-monitoring`.
===== RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md =====
38| - Feature flag rwb.dochub.intake is on.
300| - Properties per environment, set by RW-PLATADM: rwb.dochub.intake.branch-folders (branch code to path), rwb.dochub.intake.mailroom-folder, rwb.dochub.intake.sftp-root, rwb.dochub.intake.mailboxes (code to address), and the processed, rejected and archive folder names; rwb.dochub.container.intake from RWB-TE-012.
314| **Feature flag:** `rwb.dochub.intake`, with one sub-flag per channel (`rwb.dochub.intake.branch`, `.mailroom`, `.sftp`, `.email`). Off: intakeStep does not read that channel.
===== RWB E1 058 Agent platform set up E1a v1.md =====
235| | DF-REF-012 | rule_row | valid_from | Read (version-in-force pattern only; no rule row is written) |
406| **Configuration and reference data:** agent_policy and agent_prompt rows, loaded by RW-COE and approved by RW-RISK. Test agent "ECHO" seed files in `src/test/resources/agent/`. Environment properties (not business values): `rwb.agent.gateway.base-url`, `rwb.agent.gateway.identity` (managed identity of SY-AGENT). Policy check limits (timeout 1 to 120 seconds, confidence floor 0 to 1) are held in the policy JSON schema ...
418| **Feature flag:** `rwb.agent.platform`. Off: the orchestrator returns a fallback result with reason "DISABLED" and makes no model call.
===== RWB E1 059 Case intake agent in shadow E1b v1.md =====
34| - Approved agent_policy "INTAKE" version "P1" with autonomy_mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_accounts, read_documents, read_valuations, read_contact_points, and output schema "intake-sum
... truncated (3,442 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name | Select-Object -Skip 61\n$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in $files) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 420) { $t = $t.Substring(0,420) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== RWB E1 062 Deviation screening agent in shadow E2b v1.md =====
259| **Feature flag:** `rwb.agent.screening-shadow`. Off: both listeners ignore their events.
===== RWB E1 063 Agent monitoring dashboard v1 E2c v1.md =====
228| 3. Build AgentRunExtractStep with the replace-by-date write and the count check (AC3, AC4).
233| **Feature flag:** `rwb.agent.monitor`. Off: JOB-15 skips the step.
===== RWB E1 064 Data dictionary for the 14 data products v1.md =====
64| | Negotiable | Owners, refresh cycles and late behavior are data values; the story fixes the versioning and the confirm-before-publish rule |
233| - Feature flag: `rwb.dataengine.data-dictionary`.
===== RWB E1 065 Sandbox database with synthetic recovery data v1.md =====
227| - Configuration and reference data: properties `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296`, `rwb.sandbox.cases.ssme=290`, `rwb.sandbox.shape-count=10`, owned by the tech lead; lists of values from the seed migration; roles and permissions from the roles.txt seed file.
237| - Feature flag: `rwb.dataengine.sandbox` (enables the DEV profile that points the service at `rwb_sandbox`).
===== RWB E1 066 Interaction ledger store and writer v1.md =====
236| - Feature flag: `rwb.dataengine.ledger-writer`.
===== RWB E1 067 Every Workbench action into the interaction ledger v1.md =====
191| | Restart behavior | At-least-once delivery; an unprocessed event is delivered again after a restart; three retries, then the exception queue (NFR-026) |
214| - Configuration and reference data: event to ledger event map in `rwb.dataengine.ledger.event-map` (EV-01=CASE_CREATED, EV-02=CASE_ALLOCATED, EV-04=CASE_TRANSFERRED, EV-08=DECISION_TAKEN, EV-16=DOCUMENT_ATTACHED, EV-19=CASE_ESCALATED); retry limit 3 from the outbox settings (NFR-026; DL11).
223| - Feature flag: `rwb.dataengine.ledger-events`.
===== RWB E1 068 Interaction ledger read interface v1.md =====
220| - Configuration and reference data: properties `rwb.dataengine.ledger.page-size-default=50` and `rwb.dataengine.ledger.page-size-max=200`; LOV-CHANNEL for the channel filter; masking rules from Compliance through RWB-E1-037 (DL26).
230| - Feature flag: `rwb.dataengine.ledger-read`.
===== RWB TE 001 Recovery module folder and boundary test v1.md =====
56| | X5 | A recovery screen imports a collection screen | Front end build fails | Build log: rule no-collection-import broken | AC6 |
112| Then it fails with rul
... truncated (12,579 chars total)
```

### Assistant - 2026-11-10 18:21 | opencode-go/deepseek-v4.1-flash | explore

Now the Epic 2 story file and the two build notes.

<details><summary>Reasoning</summary>

Now the Epic 2 file and build notes. These are large. Let me extract candidate lines from them.

Epic 2 v5.md is 726KB. Let's see how many candidate lines.

</details>

**Tool `shell`** - completed

```json
{"command": "$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\")) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 380) { $t = $t.Substring(0,380) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== Recovery Workbench User Stories Epic 2 v5.md =====
85| - Parameter `case.entry.dpd_threshold` = 90 is in force (DL16).
132| Given parameter "case.entry.dpd_threshold" is 90
195| | BR1 | A case enters at 90 days past due | DL16; parameter case.entry.dpd_threshold |
301| - **Configuration and reference data:** parameter case.entry.dpd_threshold = 90 (RW-COE, DL16); product code map (RW-REFADM); EFS action codes copied at hand-over (RW-DATASTEW, DL29); JOB-01 retry window to 09:00 (RWB-E1-051).
310| - **Feature flag:** `rwb.integration.efs-handover`.
596| - **Configuration and reference data:** plan event map rows (RW-COE); new list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED, BROKEN (RW-COE); parameter restructure.max_breaks = 2; properties `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11).
604| - **Feature flag:** `rwb.integration.ace-plan-status`.
853| - **Configuration and reference data:** masking rule rows for party_product.account_no (RW-COMPLY, DL26); LOV-PRODUCT-STATUS (RW-DATASTEW); party roles shown, BORROWER and CO_BORROWER, as a property `rwb.customer.products.party-roles`.
861| - **Feature flag:** `rwb.integration.customer-products`.
943| - RWB-E1-045 is done: CURE_PERIOD_DAYS and `plan.warn-days` are product parameters in force (values per DL22; `plan.warn-days` assumed 3).
995| Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3
1081| | BR5 | The warning is raised `plan.warn-days` before the due date (assumed 3; DL22) | REQ-CWC-011 |
1187| **Configuration and reference data.** LOV-TIMER value INSTALLMENT_DUE (reference data administrator). CURE_PERIOD_DAYS per product and `plan.warn-days` (center of excellence, RWB-E1-045; values DL22). Rule rows R-RES-25 and R-RES-27 in the Restructure route set (center of excellence, RWB-E1-029). Event consumer retry limit 3 (NFR-026).
1200| **Feature flag.** `rwb.p3.plan-timers`. Off: treatments are recorded and no plan timers start.
1407| | BR6 | Page size is 1 to 500; a population holds at most 500 cases | Parameters rwb.decision.query.max-size=500, rwb.decision.query.max-cases=500 (assumed; DL11) |
1468| - Configuration and reference data: parameters rwb.decision.query.max-size and rwb.decision.query.max-cases (500, assumed, DL11); Compliance incident queue.
1478| - Feature flag: `rwb.decision.audit-query`.
1816| - **Feature flag:** `rwb.integration.nleads-pack`.
1911| - Parameter `booking.missing.grace_loads` = 
... truncated (15,362 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Interesting naming conflicts appear:
- Epic 1: `case.entry.dpd`; Epic 2: `case.entry.dpd_threshold`
- `recon.caselist.tolerance.pct` (E1-002) vs `recon.tolerance.pct` (E1-011)
- `load.window.end` (E1-003) vs `load.window.end.INT-07` (E1-004)
- `legal.prescription.warn.days` (E1-028) vs `prescription.warning-days` (Epic 2)
- `plan.warn-days` vs `prescription.warning-days` (different concepts? plan warn days is plan due warning)
- `booking.missing.grace` (token) vs `booking.missing.grace_loads` (Epic 2)
- `recon.efs.alert` / `recon.efs.clean` tokens vs `recon.efs.alert_pct` / `recon.efs.clean_days_required`
- `rwb.approval.area` vs `rwb.approval.area.<code>`
- `caseview.deviation-timeout-ms` vs `timeline.source-timeout-ms`
- `queueview.page-size.default` vs `rwb.dataengine.ledger.page-size-default` — different concepts.
- `caserecord.section.timeout.ms` vs `timeline.source-timeout-ms`

Also "restructure.max_breaks = 2" (2-segment with underscore) — need to capture.

Now I need the build notes. Let me extract.

</details>

**Tool `shell`** - completed

```json
{"command": "$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in @(Get-Item \"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\")) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 400) { $t = $t.Substring(0,400) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== Recovery Workbench Build Notes Epic 1 v4.md =====
87| Quartz is the scheduler inside the Workbench that starts jobs by clock time or by a chain. No person starts this. You build CaseListChainListener, a Quartz job listener, which watches JOB-03 for the business date and starts the case list step of JOB-04 as soon as JOB-03 completes. If JOB-03 has not completed, the listener starts the step at the time held in the parameter caselist.allocation.wait.u ...
123| The service CaseListCountCheck does this work with no person involved. Read the threshold from the parameter case.entry.dpd rather than writing 90 into the code. Count the case list rows you just wrote whose days past due reach the threshold. Then build the figure to match: count the loan_account rows at or above the threshold for the business date and subtract the number that the case workflow mo ...
151| Quartz is the scheduler inside the application, so no person starts this run. Build CollinsLoadJob as a Quartz job with a cron trigger at 05:00 Asia/Bangkok on working days, then a retry every 60 minutes, the value of load.retry.interval, until the window end at 09:00 or until both interfaces reach COMPLETED or REFUSED. The job computes the expected business date from the working day calendar in t ...
163| The check runner carries this out with no person involved. Write the four checks in LoadCheckRunner as SQL over the COLLINS staging tables, whose names come from the configuration keys rwb.p1.collins.int01.table, rwb.p1.collins.int02.table and rwb.p1.collins.trailer.table. DQ-001 compares the business date on the records and the trailer against the expected date. DQ-002 checks structure. DQ-003 co ...
169| The same check runner does this once the blocking checks pass. These two checks count records whose values do not match anything: the reference check looks for a key with no matching row to point at, and the list of values check looks for a source code the code map cannot translate. Count the failures and divide by the rows read. Compare the result against the parameter load.hold.tolerance.pct, wh ...
187| The job does this after the rows are written. Read the previous completed load_run for the same interface and compare its count and balance total against this load. Work out the change as a percentage and compare it against load.movement.tolerance.pct, which is 10.00 percent. The load still completes and nothing is held back. When the change is above the limit, LoadAlertNotifier se
... truncated (42,742 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now Build Notes Epic 2.

</details>

**Tool `shell`** - completed

```json
{"command": "$rx = [regex]'[a-z][a-z0-9]*(?:[.-][a-z0-9]+){2,}'\n$noise = '^(recovery\\.|org\\.|java\\.|vnd\\.|u-[a-z]|a-z0-9|b0c7)'\nforeach ($f in @(Get-Item \"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")) {\n  \"===== $($f.Name) =====\"\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    $ms = $rx.Matches($line) | Where-Object { $_.Value -notmatch $noise -and $_.Value -notmatch '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml)$' }\n    if ($ms.Count -gt 0) { $t = $line.Trim(); if ($t.Length -gt 400) { $t = $t.Substring(0,400) + ' ...' }; \"$ln| $t\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== Recovery Workbench Build Notes Epic 2 v2.md =====
17| Nothing is started by hand. JOB-01 publishes LoadCompleted (EV-26) once its load checks pass, and your LoadCompletedListener consumes that event for sources ALS and EFS with the same business date before HandoverJob begins. Put the listener behind IdempotencyGuard from RWB-E1-007, so a redelivered event does not start a second run; events are often delivered more than once, and the guard keeps the ...
29| This runs under the SY-DATALOAD managed identity with no person involved. Call AccountQuery.findAtOrAboveDpd(threshold, businessDate) from the P1 published interface recovery.data.api, and take the threshold from the parameter case.entry.dpd_threshold, in force at 90 per DL16. Do not write 90 into the code and do not read the account tables directly. The call returns the EntryCandidate rows for ac ...
75| No person starts this. JOB-02 already runs once a day and creates cases from the COLLINS load, built in RWB-E2-001. You add PlanStatusStep as a second step of the same job, ordered after the case creation step, so every case created that morning is covered in the same run. Put the step behind the feature flag rwb.integration.ace-plan-status, so it can be switched off without a release. This step i ...
87| The service does this through AcePlanClient, which you build as a thin wrapper around the ACE published interface RestructurePlanQuery. Call statusFor with a list of account numbers and read back one PlanStatusView per plan, holding planRef, accountNo, status and statusDate. Send the account numbers in batches of 500, set by the property rwb.ace.plan.batch-size, and apply a 2-second timeout from r ...
133| A person does this, on a screen that already exists. SCR-03 Case record went live with Epic 1, and this story adds one panel to it, the React component OtherProductsPanel in src/modules/recovery/case. Build the panel with four states: loading, the product list, the stale banner and the empty state. The case has to be in the caller's scope, which for a case owner means a case they own, and the serv ...
151| This happens on its own in CustomerProductsService. Call CaseQuery.partiesOf(caseId, partyRoles) on the P3 published interface, passing the party roles from property rwb.customer.products.party-roles, which holds BORROWER and CO_BORROWER. Reading the case_party rows directly is not allowed; every cross-module read goes through the published interface. The result is the party IDs whose
... truncated (19,702 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

Now a second pass to catch 2-segment keys, uppercase parameter names, and "parameter X =" forms that my 3-segment regex missed.

<details><summary>Reasoning</summary>

I need to capture more precision. Notably:
- `GEN_IDEMPOTENCY_HOURS` — parameter in E2 (uppercase).
- `restructure.max_breaks` — E2-004 mention.
- `booking.missing.grace_loads` vs `booking.missing.grace`.
- `recon.efs.alert_pct`, `recon.efs.clean_days_required`
- `rwb.approval.area.<code>`, `rwb.approval.route.<decision>.<attr>`
- `rwb.decision.input-age-days.<TYPE>`
- `rwb.access.partner.instruction-types.<PT>`

I also need 2-segment / uppercase params. Let me run a scan for backticked tokens containing a dot that my 3-segment regex may have missed, plus uppercase-with-underscore parameter names like GEN_IDEMPOTENCY_HOURS, CURE_PERIOD_DAYS, and "parameter X = Y" patterns.

Also need to check Epic 1 files for params written as `rwb.environment`, `rwb.release`, etc. And "E1-042 section 3" mentions only 3 keys. Let me scan for backticked tokens with at least one dot in all target files.

Let me do that now.

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\n$rx = [regex]'`([a-z][a-z0-9]*(?:[._-][a-z0-9]+)+)`'\n$h = @{}\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    foreach ($m in $rx.Matches($line)) {\n      $t = $m.Groups[1].Value\n      if ($t -match '^(recovery\\.|org\\.|java\\.|vnd\\.|rwb-docs|rwb-intake|rwb-quarantine|rwb_sandbox)') { continue }\n      if ($t -match '\\.(pdf|docx|xlsx|json|yaml|sql|csv|zip|md|yml|ts|java)$') { continue }\n      if ($t -match '^[a-z]+(-[a-z]+)+$') { continue }\n      if (-not $h.ContainsKey($t)) { $h[$t] = New-Object System.Collections.ArrayList }\n      [void]$h[$t].Add(\"$($f.Name):$ln\")\n    }\n  }\n}\n\"UNIQUE BACKTICKED DOTTED TOKENS: $($h.Count)\"\n$h.GetEnumerator() | Sort-Object Name | ForEach-Object { \"{0,4}  {1}   [{2}]\" -f $_.Value.Count, $_.Name, ($_.Value | Select-Object -First 3) -join '; ' }", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
UNIQUE BACKTICKED DOTTED TOKENS: 235
   2  allocation.deviation.queue.code   [System.Object[]]
   2  allocation.exception.queue.code   [System.Object[]]
   4  appraisal.max.age   [System.Object[]]
   3  approved_at   [System.Object[]]
   3  approver_user_id   [System.Object[]]
   1  booking.missing.grace_loads   [Recovery Workbench User Stories Epic 2 v5.md:1911]
  12  case.entry.dpd   [System.Object[]]
   1  case.entry.dpd_threshold   [Recovery Workbench User Stories Epic 2 v5.md:85]
   2  caselist.allocation.wait.until   [System.Object[]]
   2  caselist.export.maxrows   [System.Object[]]
   2  caserecord.section.timeout.ms   [System.Object[]]
   1  caseview.deviation-timeout-ms   [Recovery Workbench User Stories Epic 2 v5.md:4793]
   1  config.cache.ttl-seconds   [RWB E1 042 Central configuration service and parameter catalog v1.md:256]
   4  data_product   [System.Object[]]
   1  data_product_access   [RWB E1 016 Access control per data product and catalog entries v1.md:205]
   1  delegation_limit   [RWB E1 044 Database migrations versioned with parameterized schema names v1.md:219]
   1  dq_rule   [RWB E1 006 Data quality rules v1 v1.md:254]
   2  efs.history.action.codes   [System.Object[]]
   1  escalated_at   [Recovery Workbench User Stories Epic 2 v5.md:4786]
   1  escalated_to_role   [Recovery Workbench User Stories Epic 2 v5.md:4786]
   3  expires_at   [System.Object[]]
   1  first_due_date   [Recovery Workbench User Stories Epic 2 v5.md:1177]
   4  flyway_schema_history_recovery   [System.Object[]]
   1  information_schema   [RWB E1 044 Database migrations versioned with parameterized schema names v1.md:163]
   1  is_personal   [RWB TE 011 PDPA lint for code tests and logs v1.md:33]
   1  ix_assignment_case_id   [Recovery Workbench User Stories Epic 2 v5.md:5116]
   1  ix_assignment_case_open   [Recovery Workbench User Stories Epic 2 v5.md:3720]
   1  ix_case_owner_status   [Recovery Workbench User Stories Epic 2 v5.md:3377]
   2  ix_case_status_queue   [System.Object[]]
   1  ix_interaction_case_time   [Recovery Workbench User Stories Epic 2 v5.md:5116]
   1  ix_task_case_id   [Recovery Workbench User Stories Epic 2 v5.md:4791]
   3  ix_timer_case_id   [System.Object[]]
   1  ix_timer_case_type_status   [Recovery Workbench User Stories Epic 2 v5.md:3377]
   1  ix_timer_plan_due   [Recovery Workbench User Stories Epic 2 v5.md:1185]
   1  ix_timer_treatment_id   [Recovery Workbench User Stories Epic 2 v5.md:1185
... truncated (18,781 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

Let me read the product-parameter story in full and confirm the naming conflicts and special-case parameters.

<details><summary>Reasoning</summary>

Very useful. New keys discovered: `rwb.environment`, `rwb.release`, `GEN_IDEMPOTENCY_HOURS` (uppercase — need to confirm), `CURE_PERIOD_DAYS`, `restructure.max_breaks`.

Now I need to read the sections in E1-045 (five product parameters), E2-004 (restructure.max_breaks), and E2-025 (GEN_IDEMPOTENCY_HOURS) to confirm details, plus E1-045's BR2 table.

Also need to check "Environment settings" mentions: E1-042 says environment settings come from environment and secret store. E1-007 `rwb.integration.sftp.host`, SFTP key in key store.

Let me read E1-045 sections and E2 sections around those keys. Also E1-003/E1-004 to confirm load.window.end vs load.window.end.INT-07 naming conflict. And E1-002 vs E1-011 tolerance conflict.

Let me also check the Epic 2 file for parameters that don't match regex — e.g. "Parameter `x`" with underscores, uppercase. Search for "parameter" + uppercase tokens.

Let me grep for specific patterns in Epic 2 and E1-045.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md", "offset": 25, "limit": 130}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md, lines 25-154
25: 
26: ## 2. Business rationale
27: 
28: Mortgage, hire purchase and SSME follow different notice periods, service levels and bands, and today each difference is held in a team procedure. If the engines carry these values as constants, every product change waits for a release. This story keys each value by product group in the versioned reference tables of RWB-E1-043 and refuses a load that leaves a product without a required value. It meets REQ-DRI-010 and REQ-CWC-011. The measure is that a product is added or changed by a reference load with no deployment.
29: 
30: ## 3. Preconditions
31: 
32: - RWB-E1-043 is done: versioned reference tables, the registry and the read service.
33: - RWB-E1-042 is done: the parameter catalog marks each parameter with scope PRODUCT or GLOBAL, required yes or no, type, unit and allowed range (new catalog fields, see Additions).
34: - RWB-E1-012 is done: the local copies that held product values are retired.
35: - Tables PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL have an approved version in force.
36: - The timer engine (RWB-E1-028), case creation (RWB-E1-018) and the allocation engine (RWB-E1-020) read product values only through `ProductParameterService`.
37: - The loader holds RW-COE or RW-REFADM (Reference data C); the approver holds the approve right in Reference data.
38: 
39: ## 4. Flow
40: 
41: 1. Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status.
42: 2. Reference data administrator: loads each file through `POST /admin/reference-loads`.
43: 3. Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.
44: 4. Reference data service: checks each value against the catalog type and range.
45: 5. Approver: approves the version; it takes effect on its valid from date.
46: 6. Timer engine: when it starts a notice timer for a case, calls `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS",
... truncated (10,288 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "restructure\\.max_breaks|GEN_IDEMPOTENCY_HOURS|CURE_PERIOD_DAYS", "path": "04 User stories"}
```

```text
Found 19 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 2 v2.md:
  Line 111: This runs in P3 and P4 after the event, with no person involved, and your work is to handle what comes back. SY-RULES evaluates the rule for the current route state: R-RES-29 moves PLAN_CURE_PERIOD to PLAN_BROKEN, R-RES-30 moves PLAN_BROKEN to BACK_TO_ROUTE_DECISION while the break count is below restructure.max_breaks, which is 2, R-RES-31 bars a further restructure at that limit, and R-LIT-02 returns a litigation case to the legal route. Each move writes a decision log entry with the rule ID and version, and SY-CASEWF places the case in the case owner queue with a task due in 5 working days. CaseEvents.raise throws DecisionLogUnavailableException when the entry cannot be written: catch it, leave the route state alone, raise an incident with MSG-P7-003, and let the next run raise the event again.

  Line 237: **In the story.** Plan timer listener: consumes PaymentMissed; applies R-RES-27; writes the decision log entry, then the CURE_PERIOD timer from CURE_PERIOD_DAYS for the product, and sets the route state to PLAN_CURE_PERIOD.

  Line 239: The same listener handles the second event automatically. Call the rules component for R-RES-27, write the decision log entry with that rule and its version first, and only then create the CURE_PERIOD timer and set route_state to PLAN_CURE_PERIOD. The cure period is the time the customer has to pay a missed installment before the plan counts as broken, and its length is CURE_PERIOD_DAYS, a product parameter read through ProductParameterService; for MORTGAGE it is 30 calendar days. Handling a plan that is still unpaid after the cure period belongs to a later epic. This path is build step 6, with test TC-E2-004-12.

  Line 969: The officer does this once, on SCR-14 from GenerateDocumentsPanel, and the control is available only while every draft of the set is reviewed. The request goes to POST /treatments/{treatmentId}/signature-requests with the treatment ID, the list of document IDs and a required Idempotency-Key header, which the Workbench keeps for 24 hours under the parameter GEN_IDEMPOTENCY_HOURS. That key is what makes a repeated send safe: the same key arriving again returns the first result, with one signature request for the treatment and no second copy to the container. The send step sits behind its own flag, rwb.dochub.generation-screens.send, until RWB-E
... truncated (7,047 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

Let me check for uppercase/underscore parameter names and environment properties I may have missed.

<details><summary>Reasoning</summary>

New discoveries:
- `restructure.max_breaks` = 2 (E2-004, product parameter?) — it's a parameter, catalog? It's read from configuration? BR5 says "R-RES-31; parameter restructure.max_breaks". Build notes say "while the break count is below restructure.max_breaks, which is 2". Not explicitly stated as product-scope; likely GLOBAL. But E2-004 says it's a parameter. Need to check whether it's a product parameter. Let me read E2-004 section 3 and 13 around line 400 & 596.
- `GEN_IDEMPOTENCY_HOURS` 24, `GEN_MAX_TEMPLATES` 10, `GEN_FONT` "TH Sarabun New" — these are `document_hub_parameter` rows, a separate table, NOT the parameter_catalog. Important distinction: they are "document_hub_parameter" reference data, not catalog parameters. I must note that.

So I need to distinguish:
1. parameter_catalog entries (the seed target)
2. feature flags (separate catalog, E1-047)
3. environment properties (spring properties; E1-042 says environment settings come from environment and secret store, with catalog entries)
4. document_hub_parameter / reference table rows (not catalog)

The task says "build a complete inventory of every PARAMETER KEY named in the Epic 1 and Epic 2 user story files, for the RWB-E1-042 parameter catalog seed" and "Include environment settings and secrets." So the main table should be catalog parameters + environment settings/secrets. Feature flags should be listed separately (they are not parameter catalog entries — E1-042 explicitly lists "Dated feature flags (FEAT-CWC-26)" as out of scope). But I should report them since the user asked for "every PARAMETER KEY" and might want them. I'll include a separate section for feature flags and note the distinction, plus a separate section for non-catalog reference parameters (document_hub_parameter rows, product parameter codes).

Actually to be thorough and useful, I'll produce:
- Table A: parameter_catalog entries (business + environment/secret properties)
- Table B: Product-scope parameter codes (ENTRY_DPD etc. — these are catalog entries with scope PRODUCT, so arguably belong in A)
- Table C: Feature flags (rwb.* toggles) — separate mechanism
- Table D: Keys used as negative fixtures (must NOT be in catalog)
- Table E: Naming conflicts
- Table F: Non-catalog parameters (document_hub_parameter etc.)

Hmm, but the user asked for one table with specific columns. I'll do Table A as the main catalog table (including PRODUCT scope entries), and separate small tables for flags/fixtures/conflicts.

Now I need

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\n$rx = [regex]'\\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\\b'\n$h = @{}\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    if ($line -notmatch 'parameter|Parameter') { continue }\n    foreach ($m in $rx.Matches($line)) {\n      $t = $m.Value\n      if (-not $h.ContainsKey($t)) { $h[$t] = New-Object System.Collections.ArrayList }\n      [void]$h[$t].Add(\"$($f.Name):$ln\")\n    }\n  }\n}\n\"UNIQUE UPPER PARAM CANDIDATES: $($h.Count)\"\n$h.GetEnumerator() | Sort-Object Name | ForEach-Object { \"{0,3}  {1}\" -f $_.Value.Count, $_.Name }", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
UNIQUE UPPER PARAM CANDIDATES: 91
  4  ACCOUNT_NO_PATTERN
  1  APPRAISAL_REPORT
  2  AUTO_LEASE
  2  BE_YEAR_OFFSET
  1  BELOW_ENTRY
  1  CALENDAR_DAYS
  2  CAPTURE_CLOCK_SKEW_MINUTES
  2  CAPTURE_MAX_AGE_DAYS
  2  CAPTURE_MAX_FILES
  2  CASE_CREATED
  2  CASE_ENTRY_DPD
  4  CASE_NO_PATTERN
  2  CASE_TRANSFERRED
  3  CLASSIFY_MAX_PAGES
 12  CLASSIFY_THRESHOLD
  2  CLASSIFY_TIMEOUT_SECONDS
  2  CURE_PERIOD
  4  CURE_PERIOD_DAYS
  3  DEBT_SALE
  1  DELEGATION_LIMIT
  2  DOCUMENT_ATTACHED
  1  DOCUMENT_TYPE
  4  ENTRY_DPD
  4  EXCLUSION_LIST
  1  EXISTS_LINK
  1  EXPOSURE_BAND
  4  EXPOSURE_BAND_SET
  3  EXTRACT_ACCURACY_PASS
  3  EXTRACT_FIELD_THRESHOLD
  3  EXTRACT_MAX_ATTEMPTS
  2  EXTRACT_PRECISION_PASS
  2  EXTRACT_RECALL_PASS
  3  EXTRACT_TIMEOUT_SECONDS
  1  FIELD_BEFORE
  2  FILE_SUIT
  3  FREE_TEXT_MAX_CHARS
  3  FREE_TEXT_MIN_CHARS
  2  GEN_FONT
  5  GEN_IDEMPOTENCY_HOURS
  1  GEN_MAX_TEMPLATES
  3  HIRE_PURCHASE
  1  IN_FORCE
  1  IN_PROGRESS
  1  INSTALLMENT_DUE
  2  INTAKE_ALERT_AFTER_FAILURES
  8  INTAKE_ALLOWED_TYPES
  3  INTAKE_DUPLICATE_WINDOW_DAYS
 10  INTAKE_MAX_FILE_MB
  2  INTAKE_MIN_IMAGE_KB
  2  LEGAL_DOC
  2  LEGAL_PERIOD
  1  LOW_CONFIDENCE
  1  MAX_AGE_DAYS
  1  NO_BREAKGLASS_GRANT
  1  NOT_APPLICABLE
  1  NOT_NEEDED
  1  NOT_NULL
 10  NOTICE_PERIOD_DAYS
  1  OCR_AND_MODEL
  2  OCR_MAX_ATTEMPTS
  5  OCR_MIN_QUALITY
  1  OCR_TEMPLATE
  2  OCR_TIMEOUT_SECONDS
  2  OCR_WORKERS
  2  OWNER_ASSIGNED
  1  PLAN_CURE_PERIOD
  2  POSTAL_ADDRESS
 26  PRODUCT_PARAMETER
  3  REVIEW_DATE_MAX
  3  REVIEW_DATE_MIN
  3  REVIEW_PAGE_SIZE
  3  REVIEW_TEAM_UNATTACHED
  1  ROLLED_BACK
  2  RWB_SCHEMA
  2  SEARCH_MAX_RESULTS
  2  SEARCH_PAGE_SIZE
 23  SERVICE_LEVEL
  1  SKIPPED_ACTION_CODE
  1  SUM_EQUALS
  2  TDR_OFFER
  1  TEMPLATE_VARIANT
  2  TOTAL_BALANCE
  1  UNIQUE_ACROSS
  1  UNIVERSAL_RULES
  1  V1_009
  1  WAITING_PARTNER
  1  WO_CRITERIA_MET
  1  WO_CRITERIA_NOT_MET
  1  WORKING_DAYS
  3  WRITE_OFF
  1  WRONG_PARTY

```

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\n$rx = [regex]'`(rwb\\.[a-z0-9._-]+)`'\n$h = @{}\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    foreach ($m in $rx.Matches($line)) {\n      $t = $m.Groups[1].Value.TrimEnd('.')\n      if ($t -notmatch '\\.') { continue }\n      $seg = ($t -split '\\.').Count\n      if ($seg -le 2 -or $t -match '\\.(csv|sql|yaml|json|pdf)$') {\n        if (-not $h.ContainsKey($t)) { $h[$t] = New-Object System.Collections.ArrayList }\n        [void]$h[$t].Add(\"$($f.Name):$ln\")\n      }\n    }\n  }\n}\n\"SHORT rwb.* BACKTICKED TOKENS: $($h.Count)\"\n$h.GetEnumerator() | Sort-Object Name | ForEach-Object { \"{0,3}  {1}\" -f $_.Value.Count, $_.Name }", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
SHORT rwb.* BACKTICKED TOKENS: 2
  2  rwb.environment
  3  rwb.release

```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now I have a large set of uppercase parameter codes. Many belong to specific stories as "reference data" or "document_hub_parameter" or "OCR/intake parameters" — e.g. INTAKE_MAX_FILE_MB, OCR_MIN_QUALITY, CLASSIFY_THRESHOLD. Are these in the parameter_catalog? Let me check where they're defined and how. E1-057 intake, E1-049 OCR, E1-050 classify, E1-054 review, E1-053 extract.

The task specifically says "for the RWB-E1-042 parameter catalog seed" and "Find every parameter key: dotted lower-case identifiers like ...". But also "Also report any parameter whose name differs". The uppercase ones may well be catalog entries too (they're "parameters"). To be thorough I should include them, but flag their naming style (UPPER_SNAKE, differing from dotted lower-case convention) as a conflict/naming inconsistency for the catalog seed.

Let me check a few: E1-057 intake parameters, E1-049 OCR, E1-050 classify, E1-054 review, E1-053 extract. Let me look at their config sections to see whether they're described as "parameter catalog" or "reference data table".

Let me grep for these with context.

</details>

**Tool `shell`** - completed

```json
{"command": "$rx = [regex]'\\b(INTAKE_[A-Z_]+|OCR_[A-Z_]+|CLASSIFY_[A-Z_]+|EXTRACT_[A-Z_]+|REVIEW_[A-Z_]+|SEARCH_[A-Z_]+|CAPTURE_[A-Z_]+|FREE_TEXT_[A-Z_]+|MAX_AGE_DAYS|CASE_NO_PATTERN|ACCOUNT_NO_PATTERN|SKIPPED_ACTION_CODE)\\b'\n$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\")\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    if ($line -notmatch 'INTAKE_|OCR_|CLASSIFY_|EXTRACT_|REVIEW_|SEARCH_|CAPTURE_|FREE_TEXT_|MAX_AGE_DAYS|CASE_NO_PATTERN|ACCOUNT_NO_PATTERN|SKIPPED_ACTION_CODE') { continue }\n    $ms = $rx.Matches($line)\n    if ($ms.Count -eq 0) { continue }\n    $t = $line.Trim(); if ($t.Length -gt 330) { $t = $t.Substring(0,330) + ' ...' }\n    \"$($f.Name):$ln| $t\"\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
RWB E1 004 EFS extract load v1.md:131| Then the load_run check results show "SKIPPED_ACTION_CODE" = 120
RWB E1 004 EFS extract load v1.md:247| **GET /admin/jobs** and **POST /admin/jobs/{jobId}/rerun** as in RWB-E1-003; the Job for INT-07 adds `mappingVersion` and the checks SKIPPED_ACTION_CODE and REPEATED inside `checks`.
RWB E1 006 Data quality rules v1 v1.md:255| | RuleTypeTemplates | Service | One SQL template per rule type: NOT_NULL, UNIQUE_ACROSS, RANGE, SUM_EQUALS, EXISTS_LINK, MAX_AGE_DAYS, FIELD_BEFORE |
RWB E1 006 Data quality rules v1 v1.md:270| | DQ04 | Stale balance | DP01 | loan_account | MAX_AGE_DAYS data_as_of 0 days behind the load business date, for accounts on the case list |
RWB E1 024 Document store and index v1.md:37| - Document hub parameters loaded (this story creates the table): INTAKE_ALLOWED_TYPES = PDF, JPG, PNG; INTAKE_MAX_FILE_MB = 25, assumed (DL11). RWB-E1-053 and RWB-E1-057 read the same table.
RWB E1 024 Document store and index v1.md:46| 4. DocumentStoreService: checks the file type by its content signature and the file size against INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB.
RWB E1 024 Document store and index v1.md:60| | X4 | File above INTAKE_MAX_FILE_MB | Refused with 413; nothing stored | MSG-P5-017 | AC7 |
RWB E1 024 Document store and index v1.md:89| Given parameter INTAKE_MAX_FILE_MB is 25 and INTAKE_ALLOWED_TYPES is "PDF,JPG,PNG"
RWB E1 024 Document store and index v1.md:293| - Parameters INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB in document_hub_parameter, loaded by the reference data administrator.
RWB E1 026 Attach and search screen v1.md:36| - Parameters INTAKE_MAX_FILE_MB = 25 (assumed, DL11) and INTAKE_ALLOWED_TYPES = PDF, JPG, PNG are in force.
RWB E1 026 Attach and search screen v1.md:44| 3. Case owner: chooses Upload, picks a file and a document type from the list, and submits; the front end checks the size against INTAKE_MAX_FILE_MB before sending and sends an Idempotency-Key.
RWB E1 026 Attach and search screen v1.md:202| | Errors | 401; 403 no Documents C (MSG-P4-002) or case out of scope (MSG-P4-003); 404 case not found; 413 above INTAKE_MAX_FILE_MB (MSG-P5-017); 415 file type (MSG-P5-001); 422 type missing (MSG-GEN-001), type not in the table (MSG-P5-006) or malware found (MSG-P5-016); 503 decision log write failed (MSG-P7-003) |
RWB E1 026 Attach and search screen v1.md:249| - Document type table (RWB-E1-025); document hub parameters INTAKE_MAX_FILE_MB and INTAKE_ALLOWED_TYPES (RWB-E
... truncated (15,836 chars total)
```

### Assistant - 2026-11-10 18:22 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Excellent. So there is a whole family of `document_hub_parameter` rows (57 keys). These are NOT the parameter_catalog — they're a separate table (RWB-E1-024 creates it). But the user asked for "every PARAMETER KEY named in the Epic 1 and Epic 2 user story files, for the RWB-E1-042 parameter catalog seed". Hmm — "for the RWB-E1-042 parameter catalog seed" suggests catalog entries only. But "complete inventory of every PARAMETER KEY named" suggests all. I'll include them but in a clearly separate table labeled "document_hub_parameter rows (NOT parameter_catalog)", so the seed builder knows not to duplicate. That's the safest, most useful answer.

Also there is `document_hub_parameter` GEN_* keys.

Now let me check TE-006 / E1-042 relationship: TE-006 says consumers loaded "in the configuration service (RWB-E1-042) under rwb.integration.outbox.consumers" — so those are catalog entries (JSON kind).

Also `rwb.integration.outbox.retry` — JSON (retry schedule).

Let me check E2 for any further catalog params I might have missed, e.g. "configuration key" occurrences. Let me grep "configuration key" and "configuration service" lines in E2 and E1 to catch keys I haven't captured.

Also E1-019 queue.cap.max; E2 says caseload caps from queue table.

Let me also check E1-037 `rwb.access.mask.keep-last` (4), `rwb.access.membership-refresh-minutes` (5).

Let me grep for "configuration key" / "configuration service" / "property" lines that contain a dotted token and check I've captured all.

I think I have nearly all. Let me now check a few files' §13 for owner/type/unit details — particularly E1-003, E1-019, E1-055, TE-006, E2-014, E2-019, E2-021, E2-025, E2-029, E2-031, E2-033.

Rather than read all, I'll rely on the extracted lines which mostly contain defaults. For type/unit/range, I'll infer only where explicitly stated (e.g., case.entry.dpd INTEGER 1-365; NOTICE_PERIOD_DAYS range 1-365 unit CALENDAR_DAYS/WORKING_DAYS).

Important: I must not invent. For most, type/unit/min/max will be UNKNOWN.

Let me check E1-045 line 232 for the catalog entries detail (scope/required/type/unit/range) and E1-042's "Additions" if any. Also check whether E1-045 §13 says anything about the five parameters' types.

Let me read E1-045 lines 155-250.

Also, I should confirm E1-002's `caselist.allocation.wait.until` default 07:15 and type TIME.

And E1-004's `load.window.end.INT-07` — is it a distinct key from `load.window.end`? E1-003 uses `load.window.end` 09:00; E1-004 uses `load.wind

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"limit": 95, "offset": 155, "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md, lines 155-249
155: | RW-REFADM, reference data administrator | Loads PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
156: | RW-PRODHEAD, product head | Owns the values for the product (LOV-PRODUCT owner in refdata.txt); reads versions (Reference data R) |
157: | RW-RISK, risk and model risk officer | Approves a version where a limit or threshold moves (refdata.txt Change process step 4; assumed approve right as in RWB-E1-043) |
158: | SY-CASEWF, case workflow module | Reads product values and writes timers |
159: | SY-RULES, rules component | Reads product values for allocation |
160: 
161: ## 11. Data
162: 
163: | BR Field ID | Entity | Field | Read or write |
164: |---|---|---|---|
165: | DF-CAS-001 | recovery_case | id | Read |
166: | DF-CAS-003 | recovery_case | product_group | Read |
167: | DF-CAS-005 | recovery_case | status | Read |
168: | DF-CAS-010 | recovery_case | queue_id | Write (exception queue under X5) |
169: | DF-WRK-028 | timer | case_id | Write |
170: | DF-WRK-030 | timer | timer_type | Write |
171: | DF-WRK-031 | timer | started_at | Write |
172: | DF-WRK-032 | timer | expires_at | Write |
173: | DF-WRK-033 | timer | warn_at | Write |
174: | DF-REF-160 | reference_version | table_code | Read |
175: | DF-REF-161 | reference_version | version_no | Read |
176: | DF-REF-183 | reference_row | row_key | Read |
177: | DF-REF-184 | reference_row | row_data | Read |
178: | DF-REF-140 | parameter_catalog | scope | Read |
179: | DF-REF-141 | parameter_catalog | required | Read |
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
191: | Errors | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 open cases on a removed product (MSG-P3-027); 422 missing required row (MSG-
... truncated (7,104 chars total)
```

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\n$rx = [regex]'`(rwb\\.[a-z0-9.-]+)`'\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    if ($line -notmatch 'configuration key|Configuration key|configuration service|Configuration and reference data|property |Property ') { continue }\n    foreach ($m in $rx.Matches($line)) { \"$($f.Name):$ln| $($m.Groups[1].Value)\" }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
RWB E1 007 Integration adapters for file loads and outbound files v1.md:266| rwb.integration.sftp.host
RWB E1 013 Baseline measures v1.md:246| rwb.reporting.baseline-date
RWB E1 014 Decision log copy to the data lake v1.md:249| rwb.dataengine.lake.container
RWB E1 015 Freshness stamp per data product v1.md:238| rwb.dataengine.freshness.alert-channel
RWB E1 017 Retention and archive rule for the data store v1.md:257| rwb.dataengine.retention.archive-container
RWB E1 034 Letter template management v1.md:235| rwb.comms.template.allowed-types
RWB E1 034 Letter template management v1.md:235| rwb.comms.template.max-size-mb
RWB E1 047 Feature flags for module release with a removal date v1.md:217| rwb.environment
RWB E1 047 Feature flags for module release with a removal date v1.md:225| rwb.environment
RWB E1 047 Feature flags for module release with a removal date v1.md:225| rwb.flags.cache-seconds
RWB E1 051 Legacy feed jobs on ADF and Control M v1.md:195| rwb.jobs.collins.start
RWB E1 051 Legacy feed jobs on ADF and Control M v1.md:195| rwb.jobs.collins.last-retry
RWB E1 051 Legacy feed jobs on ADF and Control M v1.md:195| rwb.jobs.files.weekly-cron
RWB E1 055 Proof of delivery capture design with WIN v1.md:263| rwb.comms.dispatch.eligible-states
RWB E1 055 Proof of delivery capture design with WIN v1.md:263| rwb.comms.dispatch.max-attempts
RWB E1 055 Proof of delivery capture design with WIN v1.md:263| rwb.comms.dispatch.barcode-break-days
RWB E1 055 Proof of delivery capture design with WIN v1.md:263| rwb.comms.pod.stale-after-business-days
RWB E1 058 Agent platform set up E1a v1.md:406| rwb.agent.gateway.base-url
RWB E1 058 Agent platform set up E1a v1.md:406| rwb.agent.gateway.identity
RWB E1 067 Every Workbench action into the interaction ledger v1.md:214| rwb.dataengine.ledger.event-map
RWB TE 003 Types and contract tests from the API specification v1.md:35| rwb.release
RWB TE 003 Types and contract tests from the API specification v1.md:189| rwb.release
RWB TE 004 Masked data in SIT and UAT v1.md:195| rwb.maskedcopy.intake-container
Recovery Workbench User Stories Epic 2 v5.md:596| rwb.ace.plan.batch-size
Recovery Workbench User Stories Epic 2 v5.md:596| rwb.ace.plan.timeout-ms
Recovery Workbench User Stories Epic 2 v5.md:853| rwb.customer.products.party-roles
Recovery Workbench User Stories Epic 2 v5.md:6492| rwb.comms.dispatch.eligible-states

```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

Now I need a few more specifics. Let me check:
1. E1-047 §3 line 217 for rwb.environment.
2. TE-003 line 189 for rwb.release.
3. E2-004 §3 line 400 context — restructure.max_breaks scope.
4. E2-014 approval route §3 lines 3840-3842 context (already have).
5. E2-019 input age lines 4246.
6. E2-025 GEN_IDEMPOTENCY_HOURS (document_hub_parameter).
7. E2-021 dispatch eligible states.

Also need owner roles for many. Let me check a handful of files' "Configuration and reference data" sections that mention owner.

Given the volume, I'll infer owner only where stated: e.g., E1-042 says catalog owned by RW-COE; case.entry.dpd owner RW-COE. Most others say "loaded by the center of excellence analyst" → RW-COE as owner (but that's loader, not owner). I should not overstate; I'll put what's stated, else UNKNOWN.

Let me grab the specific lines for rwb.environment, rwb.release, restructure.max_breaks, and the E2-014 section 3 context.

</details>

**Tool `shell`** - completed

```json
{"command": "$targets = @(\n @{f=\"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 047 Feature flags for module release with a removal date v1.md\"; lines=@(210,220,225,230)},\n @{f=\"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB TE 003 Types and contract tests from the API specification v1.md\"; lines=@(185,192)},\n @{f=\"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\"; lines=@(396,404,590,600,3836,3844)}\n)\nforeach ($t in $targets) {\n  \"===== $($t.f) =====\"\n  $all = [System.IO.File]::ReadAllLines((Resolve-Path $t.f))\n  foreach ($n in $t.lines) {\n    $lo = [Math]::Max(1,$n-0); $hi = [Math]::Min($all.Count, $n+1)\n    for ($i=$lo; $i -le $hi; $i++) { $x=$all[$i-1]; if ($x.Length -gt 400) { $x=$x.Substring(0,400)+' ...' }; \"$i| $x\" }\n    \"---\"\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
===== 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 047 Feature flags for module release with a removal date v1.md =====
210| 
211| - **Package.** folder `src/main/java/recovery/integration/flags`, Java package `recovery.integration.flags`; front end folder `src/modules/recovery/flags`.
---
220| | FlagRemovalReportJob | Job | Weekly report |
221| | useFeatureFlag | React component | Hook that reads GET /feature-flags once per page load and returns the value for a key |
---
225| - **Configuration and reference data:** property `rwb.environment` (DEV, SIT, UAT, PROD) per deployment; property `rwb.flags.cache-seconds` = 30 (assumed; DL11). Flag rows are created through the endpoints by RW-PLATADM.
226| - **Build steps:**
---
230|   4. Build the four endpoints with the access check and the ACE audit write.
231|   5. Build useFeatureFlag and FlagGate with a component test that hides and shows a child.
---
===== 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB TE 003 Types and contract tests from the API specification v1.md =====
185| | ContractFixtures | Repository | Synthetic fixture data per operation |
186| 
---
192| 
193| 1. Add the lint step and the rule set; prove it fails on an operation with no x-capability (AC3).
---
===== 04 User stories\Recovery Workbench User Stories Epic 2 v5.md =====
396| - RWB-E2-001 (case creation from the COLLINS load) is done.
397| - The ACE common module publishes RestructurePlanQuery in SIT and UAT (INT-34; DL14).
---
404| 
405| 1. Scheduler: the plan status step runs in JOB-02 after the case creation step, once a day.
---
590| | AcePlanClient | Service | Wraps RestructurePlanQuery with batching and the 2-second timeout |
591| | PlanEventMap | Rule table | Rows: ACE status, route state, rule event; versioned reference data |
---
600|   3. Build the event lookup with PlanEventMap and the CaseEvents.raise call; handle DecisionLogUnavailableException.
601|   4. Build the exception writes for no status and unknown codes.
---
3836| 
3837| - RWB-E1-038 is done: delegation version DOA-2026.11 is in force and the lookup returns the lowest covering level; holders and substitutes are named test users in SIT and UAT (DL18).
---
3844| 
3845| ### 4. Flow
---

```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

<details><summary>Reasoning</summary>

TE-003 `rwb.release` line 189 — let me grep it separately. Actually line 189 in the earlier output was "Then contract tests..." hmm. The grep said `rwb.release` at line 189, but read shows line 192 blank. My offset math might be off by one due to the loop printing n-0..n+1. Line 189 wasn't printed (lo=185, hi=190). Let me just grep.

Also E1-047 line 217 rwb.environment — line 217 wasn't in my print range (210-230 with ±1 = 209-231, so 217 should be printed). Wait, it printed 210,211 then 220,221. Because lines list was @(210,220,225,230), each ±1: 209-211, 219-221, 224-226, 229-231. So 217 not shown. Fine — grep said "Configuration and reference data: property rwb.environment" at 217? Actually line 225 is the one shown. The grep output said 217 and 225. Let me check 215-218.

Let me do a focused grep for these.

</details>

**Tool `shell`** - completed

```json
{"command": "\"--- E1-047 around 215-218 ---\"\n$a=[System.IO.File]::ReadAllLines((Resolve-Path \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB E1 047 Feature flags for module release with a removal date v1.md\")); 215..218 | ForEach-Object { \"$_| $($a[$_-1])\" }\n\"--- TE-003 rwb.release ---\"\nSelect-String -Path \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\\RWB TE 003 Types and contract tests from the API specification v1.md\" -Pattern 'rwb.release' | ForEach-Object { \"$($_.LineNumber)| $($_.Line.Trim())\" }\n\"--- E2-004 restructure context 396-402 ---\"\n$b=[System.IO.File]::ReadAllLines((Resolve-Path \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\")); 396..402 | ForEach-Object { \"$_| $($b[$_-1])\" }\n\"--- E2-014 3836-3843 ---\"\n$c=[System.IO.File]::ReadAllLines((Resolve-Path \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\")); 3838..3843 | ForEach-Object { \"$_| $(if($c[$_-1].Length -gt 500){$c[$_-1].Substring(0,500)+' ...'}else{$c[$_-1]})\" }", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
--- E1-047 around 215-218 ---
215| | FeatureFlagController | Controller | The four endpoints; validation; problem responses |
216| | FeatureFlagService | Service | Create, change and retire; version check; change row; ACE audit call |
217| | FeatureFlagsImpl | Published interface | isOn with a 30-second cache per key; environment from property `rwb.environment` |
218| | FeatureFlagRepository, FeatureFlagChangeRepository | Repository | The two flag tables only |
--- TE-003 rwb.release ---
35| - The build property `rwb.release` names the release being built: E1 for 30 November 2026.
43| 5. Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.
78| Given the build property rwb.release is "E1"
189| **Configuration and reference data.** The build property `rwb.release`; the permission matrix seed; fixture data per operation, synthetic only.
--- E2-004 restructure context 396-402 ---
396| - RWB-E2-001 (case creation from the COLLINS load) is done.
397| - The ACE common module publishes RestructurePlanQuery in SIT and UAT (INT-34; DL14).
398| - The account number is the join key between the case and the ACE plan (DL21).
399| - The plan event map rows are loaded: ACE status BROKEN with route state PLAN_CURE_PERIOD maps to event CURE_PERIOD_EXPIRED; BROKEN with any other route state maps to TREATMENT_BROKEN.
400| - Parameter `restructure.max_breaks` = 2 is in force (Restructure route set: a second break bars a further restructure).
401| - The restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are in force.
402| 
--- E2-014 3836-3843 ---
3838| - RWB-E1-028 is done: the P3 timer engine starts service level timers, and JOB-05 publishes EV-19 TimerBreached.
3839| - RWB-E1-027 is done: the decision log writer; RWB-E1-037 is done: the permission matrix and scope.
3840| - Approval route parameters are in the catalog for each decision with no amount limit, for D7.1 notices: rwb.approval.route.D7.1.area=LITIGATION, rwb.approval.route.D7.1.role=RW-LITOFF, rwb.approval.route.D7.1.escalation-role=RW-HEADLIT, rwb.approval.route.D7.1.service-level=1 working day (assumed; DL22).
3841| - Service level for limit-based approvals: rwb.approval.service-level.default=3 working days (assumed from the 3 working day approval timers in R-RES-10 and R-SET-05; DL22).
3842| - Capability area per decision code: D5 and D6.x Treatment and offer, D7.x Litigation, D8.2 and D8.3 Asset and dis
... truncated (2,719 chars total)
```

### Assistant - 2026-11-10 18:23 | opencode-go/deepseek-v4.1-flash | explore

One last pass for secrets, environment variables, and any parameter I may have missed.

<details><summary>Reasoning</summary>

Now I have enough. Let me also verify a couple of details:
- E1-003 default `load.window.end` 09:00 — type TIME.
- E1-004 `load.window.end.INT-07` 08:00.
- E1-002 `caselist.allocation.wait.until` 07:15.
- E1-019 `queue.cap.max` 500, range 1 to 500.
- E1-029 `rules.testcases.min` 50.
- E1-039 breakglass values.
- TE-002 uses `@scb-ace/...` not params.
- E1-047 `rwb.casewf.not-defined` is a negative fixture (flag that is not defined). Also `rwb.p9.unknown`, `rwb.p5.ocr-intake`, `rwb.p6.line-dispatch`, `rwb.casewf.case-list-queue-column`.

Negative fixtures: 
- `allocation.retry.limit` (E1-042 AC3) — must NOT be in catalog.
- `rwb.casewf.not-defined` (E1-047 AC7) — flag not defined.
- `rwb.p9.unknown` (E1-047 AC9) — unknown flag.
Those latter two are feature flag negative fixtures, not parameter catalog. I'll list separately.

Also `case.entry.dpd` = "ninety" and 400 are negative VALUE fixtures, not negative keys.

Now let me check E1-016 for parameter keys — none found. E1-030 none.

Let me quickly confirm E1-001/016/021/030/043/044/046/048/052/058 etc. don't have parameters I missed. From the context dump:
- E1-001: only flag.
- E1-016: only flag.
- E1-021: only flag.
- E1-030: only flag.
- E1-043: refdata.cache.ttl-seconds.
- E1-044: spring.flyway.* (9 properties) + rwb.p3.migration-drift-gate flag.
- E1-046: only flag.
- E1-048: only flag.
- E1-052: only flag.
- E1-058: rwb.agent.gateway.base-url, rwb.agent.gateway.identity; policy limits (timeout 1-120 s, confidence floor 0-1) held in policy JSON schema — mention as "not catalog".
- E1-059/060/061/062: only flags; agent_policy rows.
- E1-063: flag.
- E1-064: flag.
- E1-065: sandbox properties.
- E1-066: flag.
- E1-067: ledger.event-map + retry limit 3.
- E1-068: ledger page sizes.
- TE-001..005: flags only (TE-005 flag, TE-001 no params).
- TE-006: outbox consumers/retry.
- TE-007: three params.
- TE-008: three params.
- TE-011: none.
- TE-012: storage properties.
- TE-013: flag.

Epic 2:
- E2-001: case.entry.dpd_threshold.
- E2-004: plan event map, restructure.max_breaks, rwb.ace.plan.batch-size, timeout-ms.
- E2-005: rwb.customer.products.party-roles.
- E2-006: plan.warn-days (product param), CURE_PERIOD_DAYS.
- E2-007: rwb.decision.query.max-size, max-cases.
- E2-008: booking.missing.grace_loads.
- E2-011: queueview.page-size.default/max.
- E2-012: transfer.bulk.max.
- E2-014: rwb.approval.route.*, rwb.approval.service-level.default, rwb.approval.area.<code>.
- E2-019: rwb.decision.input-age-days.*.
-

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "$dir = \"04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v5\"\n$files = @(Get-ChildItem -Path $dir -Filter *.md | Sort-Object Name) + @(Get-Item \"04 User stories\\Recovery Workbench User Stories Epic 2 v5.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 1 v4.md\",\"04 User stories\\Recovery Workbench Build Notes Epic 2 v2.md\")\nforeach ($f in $files) {\n  $ln = 0\n  foreach ($line in [System.IO.File]::ReadAllLines($f.FullName)) {\n    $ln++\n    if ($line -match 'secret|password|key store|key vault|connection string|RWB_SCHEMA') {\n      $t = $line.Trim(); if ($t.Length -gt 300) { $t = $t.Substring(0,300) + ' ...' }\n      \"$($f.Name):$ln| $t\"\n    }\n  }\n}", "workdir": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
RWB E1 001 Recovery tables for the 14 data products v1.md:320| Ruled 2026-11-05 as D-RCV-28: recovery Flyway files are named `V<seq>__<story>_<name>.sql` with a four-digit sequence taken in merge order; line 1 is `-- Story: <story key>`; the schema is referenced only as `${recoverySchema}` and is `recovery` in every environment. The RWB-E1-001 baseline is `V000 ...
RWB E1 007 Integration adapters for file loads and outbound files v1.md:35| - The SFTP inbound and outbound folders exist in DEV and SIT, with credentials in the key store (NFR-052).
RWB E1 007 Integration adapters for file loads and outbound files v1.md:258| | SftpTransport | Service | The only class that opens SFTP sessions; credentials from the key store |
RWB E1 007 Integration adapters for file loads and outbound files v1.md:266| - **Configuration and reference data:** interface_config rows for INT-10 to INT-16 and INT-25, loaded by RW-REFADM through the reference data load; DQ-057 to DQ-098 load check rows (P1 reference data); property `rwb.integration.sftp.host` per environment; SFTP key in the key store.
RWB E1 022 Sign on with SSO MFA and the first roles v1.md:24| As a **case owner (RW-CASEOWN)**, I want **to sign in to the Workbench once through Entra ID with multi-factor authentication and see only the screens and actions my Workbench roles allow**, so that **access is controlled from the first release and nobody holds a Workbench password or a local accoun ...
RWB E1 022 Sign on with SSO MFA and the first roles v1.md:42| 2. ACE common module: redirects to Entra ID; the person signs in with password and second factor; Entra ID returns an OpenID Connect token with the groups claim and the amr claim.
RWB E1 022 Sign on with SSO MFA and the first roles v1.md:87| When the user opens the Workbench and signs in with password and second factor
RWB E1 022 Sign on with SSO MFA and the first roles v1.md:152| | BR1 | Membership of the Entra ID group mapped to a role is the only way to hold the role. The Workbench holds no password and no local account | role.entra_group (DF-REF-039); DT07; Admin and access model, section 4.2 |
RWB E1 022 Sign on with SSO MFA and the first roles v1.md:307| - No local password, local account or role cache that outlives the session.
RWB E1 034 Letter template management v1.md:241| 5. Add the optimistic lock and the Idempotency-Key store; test AC9 and AC10.
RWB E1 042 Central configuration service and parameter catalog v1.md:34| - The ACE secret store hold
... truncated (14,559 chars total)
```

### Assistant - 2026-11-10 18:24 | opencode-go/deepseek-v4.1-flash | explore

# RWB-E1-042 Parameter Catalog Seed — Full Key Inventory

## Scope and method

Read in full or by exhaustive key-context extraction: all 79 `.md` files in `04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\`, plus:
- `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 2 v5.md` (1,150 lines of key context)
- `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 1 v4.md`
- `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench Build Notes Epic 2 v2.md`

Source column uses `story:line`. All E1/TE sources resolve to:
`C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 NNN <title> v1.md` (TE files: `RWB TE NNN …`). `E2` = the Epic 2 file above; `BN1`/`BN2` = the two build notes above.

Legend for markers: **(a)** = assumed, **DLnn** = open decision reference, **TBD** = to be decided. `UNKNOWN` = not stated anywhere in the corpus. No value below is invented.

**Important structural finding:** the corpus names parameters in **five different mechanisms**, not one:
1. `parameter_catalog` (E1-042) — Tables 1–3, the actual seed target.
2. `document_hub_parameter` (created by E1-024) — Table 6, a **separate table**, not the catalog.
3. `PRODUCT_PARAMETER` / `SERVICE_LEVEL` reference rows (E1-045) — Table 2; the *codes* are catalog entries with scope PRODUCT, the *values* are reference rows.
4. Dated feature flags (E1-047) — Table 7, explicitly **out of scope** of E1-042 (§19: "Dated feature flags (FEAT-CWC-26)").
5. Environment / secret-store settings — Table 3.

---

## Table 1 — Catalog entries, business parameters, scope GLOBAL

| key | default (stated / assumed) | type | unit | min | max | scope | req | owner | envs | used by | source | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `allocation.deviation.queue.code` | `"DEV-HANDLER"` (a; DL23) | STRING | none | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.allocation` | E1-020:37,345 | destiny queue for deviation cases |
| `allocation.exception.queue.code` | `"RWB-EXC"` (a; DL23) | STRING | none | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.allocation` | E1-020:37,345 | |
| `appraisal.max.age` | `365` (a; DL11, MSG-S5-002, CTL-27) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.ccms`, `.load.svaf` | E1-009:36,165,264; BN1:547 | stale-appraisal limit |
| `booking.missing.grace_loads` | `1` (stated) | INTEGER | LOADS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.integration.booking` | E2:1911,2025,2118; BN2:401 | name uses `_`; see conflict C9 |
| `case.entry.dpd` | `90` (stated; DL16) | INTEGER | DAYS | `1` | `365` | GLOBAL | true | RW-COE | PROD, SIT, UAT (cited) | `recovery.casewf.casecreation` | **E1-042:33,44,83,86,95,111,115,135,140,293,303**; E1-018:34,43,84,170,307; E1-002:36,84; E1-006:36,147,269,274; E1-011:35,232; BN1:123,639,1039 | the only fully specified catalog row |
| `case.entry.dpd_threshold` | `90` (a per DL16) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COE (stated E2) | UNKNOWN | `recovery.casewf.casecreation` | E2:85,132,195,301; BN2:29 | **naming conflict C1** |
| `caselist.allocation.wait.until` | `07:15` (stated) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.caselist` | E1-002:36,290; BN1:87 | |
| `caselist.export.maxrows` | `10000` (a; DL11) — written `10,000` in E1-031 | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN (loaded by RW-REFADM in E2) | UNKNOWN | `recovery.casewf.caselist` | E1-042:33; E1-031:35,98,134,227; E2:9177,9314,9378,9402; BN1:1823 | |
| `caserecord.section.timeout.ms` | `3000` (a; DL11) | INTEGER | MILLISECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.caseview` | E1-023:266; E1-035:224; BN1:1329 | |
| `caseview.deviation-timeout-ms` | `2000` (stated) | INTEGER | MILLISECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.caseview` | E2:4793,841; BN2:841 | dash style |
| `config.cache.ttl-seconds` | `60` (a; DL11) | INTEGER | SECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COE (catalog owner) | UNKNOWN | `recovery.casewf.config` | E1-042:256 | "itself a catalog entry" |
| `efs.history.action.codes` | UNKNOWN — named list; default assumed to be "every code in LOV-ACTION-CODE" (a; DL29) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | business lead (stated) | UNKNOWN | `recovery.dataengine.load.efs` | E1-004:37,127,267; BN1:239 | |
| `jobs.allocation.deadline` | `07:00` (stated) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.scheduling` | TE-007:235 | |
| `jobs.catch-up.max-dates` | `5` (a; DL11) | INTEGER | DATES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.scheduling` | TE-007:37,47,235 | |
| `jobs.timer-check.cron` | `0 0/5 * * * ?` (stated) | STRING | CRON | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.scheduling` | TE-007:235 | |
| `legal.prescription.warn.days` | `180` (a) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | Legal (stated) | UNKNOWN | `recovery.casewf.timers` | E1-028:37,293; BN1:1619 | **conflicts with `prescription.warning-days` (C4)** |
| `load.hold.tolerance.pct` | `0.50` (a; DL25) | DECIMAL | PERCENT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.als`, `.ccms`, `.svaf` | E1-003:36,88,189,342; E1-009:36,164; BN1:169 | |
| `load.movement.tolerance.pct` | `10.00` (a; DL25) | DECIMAL | PERCENT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.als`, `.efs`, `.ccms` | E1-003:36,190; E1-009:36; BN1:187,529 | |
| `load.retry.interval` | `60` (stated) | INTEGER | MINUTES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.als` | E1-003:36,342; BN1:151 | |
| `load.sample.size` | `50` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.als` | E1-003:36,199 | |
| `load.window.end` | `09:00` (stated) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.als` | E1-003:36,342 | **conflicts with `.INT-07` (C3)** |
| `load.window.end.INT-07` | `08:00` (a; NFR-014, DL11) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.load.efs` | E1-004:37,161,263; BN1:263 | per-interface suffix |
| `plan.warn-days` | `3` (a; DL22) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL **and** PRODUCT (E2-006 calls it "product parameter") | UNKNOWN | UNKNOWN (center of excellence) | UNKNOWN | `recovery.casewf.plan` | E2:943,995,1081,1187 | **scope + naming conflict C5** |
| `prescription.warning-days` | `90` (a; DL22) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.caserecord` | E2:4567,4610,4686,4793; BN2:859 | **conflicts with `legal.prescription.warn.days` (C4)** |
| `queue.cap.max` | `500` (a; DL23) | INTEGER | CASES | `1` | `500` | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.queues` | E1-019:168,286 | range stated in BR8 |
| `queueview.page-size.default` | `50` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.queueview` | E2:3379 | |
| `queueview.page-size.max` | `200` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.queueview` | E2:3379 | |
| `recon.caselist.tolerance.pct` | `0.00` (a; DL25) | DECIMAL | PERCENT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.caselist` | E1-002:36,84,163,290 | **conflicts with `recon.tolerance.pct` (C2)** |
| `recon.efs.alert_pct` | `0.1` (a; DL25 recommends zero) | DECIMAL | PERCENT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COE (stated E2-031) | UNKNOWN | `recovery.dataengine.recon` | E2:6946,6991,7128; BN2:1253 | `_pct` suffix style |
| `recon.efs.clean_days_required` | `10` (stated) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COE (stated) | UNKNOWN | `recovery.dataengine.recon` | E2:6946,7128; BN2:1259 | |
| `recon.tolerance.pct` | `0.00` (a; DL25); AC sets 0.10 | DECIMAL | PERCENT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.recon` | E1-011:35,80,100,132,232; BN1:651 | per-reconciliation value |
| `refdata.cache.ttl-seconds` | `300` (a; DL11); `30` in SIT | INTEGER | SECONDS | UNKNOWN | UNKNOWN | GLOBAL | true | UNKNOWN (loaded by RW-PLATADM) | SIT, PROD (cited); "per environment" | `recovery.casewf.refdata` | **E1-042:33,105,107,124**; E1-043:33,272,286 | AC4 uses it as the required-missing example |
| `restructure.max_breaks` | `2` (stated) | INTEGER | COUNT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.plan` | E2:400,511,596; BN2:111 | `_` style |
| `rules.testcases.min` | `50` (a) | INTEGER | COUNT | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.rules` | E1-029:287 | |
| `servicelevel.required-statuses` | `NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL` (a; DL22) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.refdata.product` | E1-045:43,139,232; BN1:2529 | |
| `timeline.source-timeout-ms` | `2000` (stated) | INTEGER | MILLISECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.timeline` | E2:5118 | near-duplicate of `caseview.deviation-timeout-ms` |
| `timeline.type.order` | `decision, status change, assignment, transfer, contact, document` (stated) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.timeline` | E1-035:222; BN1:2043 | |
| `tracker.file.max.mb` | `20` (a; DL11) | INTEGER | MEGABYTES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.tracker` | E1-010:296 | |
| `tracker.inventory.teams` | `TDR, DIL, LIT, NPA, DEBT_SALE, WRITE_OFF` (a codes; LOV-TEAM) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.tracker` | E1-005:34,77,132,208; E1-012:35,236; BN1:733 | |
| `tracker.retire.parallel.days` | `2` (stated) working days | INTEGER | WORKING_DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.tracker` | E1-012:35,80,145,236; BN1:685 | |
| `transfer.bulk.max` | `50` (a; DL23) | INTEGER | CASES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.casewf.transfer` | E2:3722; BN2:649 | |

---

## Table 2 — Catalog entries with scope PRODUCT (codes only; values live in PRODUCT_PARAMETER)

| key | default | type | unit | min | max | scope | req | owner | envs | used by | source | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ENTRY_DPD` | UNKNOWN at catalog level (90 is the business value, DL16) | INTEGER | DAYS | UNKNOWN | UNKNOWN | PRODUCT | true | RW-PRODHEAD / RW-COE | UNKNOWN | `ProductParameterService`; case creation, allocation | E1-045:138,227; BN1:2517 | **same concept as `case.entry.dpd` — conflict C1** |
| `EXCLUSION_LIST` | UNKNOWN | CODE_LIST | none | n/a | n/a | PRODUCT | true | RW-PRODHEAD | UNKNOWN | case creation, allocation | E1-045:138,227 | |
| `NOTICE_PERIOD_DAYS` | per product: `30` MORTGAGE, `60` HIRE_PURCHASE (stated example) | INTEGER | CALENDAR_DAYS / WORKING_DAYS (stated units) | `1` | `365` | PRODUCT | true | RW-PRODHEAD | UNKNOWN | timer engine (`recovery.casewf.timers`) | E1-045:79,105,138,46; BN1:2517 | range 1–365 stated in AC4 |
| `CURE_PERIOD_DAYS` | `30` for MORTGAGE (stated) | INTEGER | CALENDAR_DAYS | UNKNOWN | UNKNOWN | PRODUCT | true | RW-PRODHEAD | UNKNOWN | plan timer listener | E1-045:138; E2:943,959,995,1080,1187; BN2:237,239 | |
| `EXPOSURE_BAND_SET` | UNKNOWN | CODE_LIST | none | n/a | n/a | PRODUCT | true | RW-PRODHEAD | UNKNOWN | allocation engine | E1-045:138,227 | |

---

## Table 3 — Environment settings, spring properties and secrets

| key | default | type | unit | min | max | scope | req | owner | envs | used by | source | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ace.db.password` | UNKNOWN — never served | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | per environment | ACE datasource | **E1-042:129,132,301** | kind `ENVIRONMENT`, `secret = true` |
| `rwb.environment` | UNKNOWN (one of `DEV`, `SIT`, `UAT`, `PROD`) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per deployment | `recovery.integration.flags` | E1-047:217,225 | 2-segment key |
| `rwb.release` | `E1` (stated for the 30 Nov 2026 release) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | build-time | `recovery.generated.*` contract tests | TE-003:35,43,78,189 | build property, not runtime |
| `RWB_SCHEMA` | `recovery` (a; also `rwb_case` in AC3) | STRING | none | n/a | n/a | GLOBAL | true | RW-PLATADM | DEV, SIT, UAT, PROD | Flyway `${schema}` placeholder | E1-044:35,42,77,94,185,196-199 | env var / Flyway placeholder |
| `spring.flyway.enabled` | `true` | BOOLEAN | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | `recovery.casewf.migration` | E1-044:194 | |
| `spring.flyway.locations` | `classpath:db/migration/recovery` | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:195 | |
| `spring.flyway.schemas` | `${RWB_SCHEMA}` | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:196 | |
| `spring.flyway.default-schema` | `${RWB_SCHEMA}` | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:197 | |
| `spring.flyway.table` | `flyway_schema_history_recovery` | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:198; BN1:2495 | |
| `spring.flyway.placeholders.schema` | `${RWB_SCHEMA}` | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:199 | |
| `spring.flyway.validate-on-migrate` | `true` | BOOLEAN | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:200; BN1:2501 | |
| `spring.flyway.out-of-order` | `false` | BOOLEAN | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:201 | |
| `spring.flyway.clean-disabled` | `true` | BOOLEAN | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | migration | E1-044:202 | |
| `rwb.access.mask.keep-last` | `4` (a; DL26) — characters kept | INTEGER | CHARACTERS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COMPLY | UNKNOWN | `recovery.access.matrix`, FieldMasker | E1-037:262; BN1:2107 | |
| `rwb.access.membership-refresh-minutes` | `5` (a; DL38) | INTEGER | MINUTES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.signin`, SessionRevalidationFilter | E1-037:262; E2:6135,1097 | |
| `rwb.access.required-amr` | `mfa` (stated) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.signin` | E1-022:256; BN1:1277 | |
| `rwb.access.breakglass.incident-pattern` | `^INC[0-9]{7}$` (a; DL38) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.accesslog` | E1-039:37; BN1:2205 | regex |
| `rwb.access.breakglass.reason-min` | `20` (a; DL38) | INTEGER | CHARACTERS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.accesslog` | E1-039:37 | |
| `rwb.access.breakglass.review-days` | `1` (a; DL38) — one working day | INTEGER | WORKING_DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.accesslog` | E1-039:37; BN1:2223 | |
| `rwb.access.breakglass.window-hours` | `4` (a; DL38) | INTEGER | HOURS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.accesslog` | E1-039:37,157 | |
| `rwb.access.partner.instruction-types.PT-LAWFIRM` | `FILE_SUIT,ENFORCE` (a) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | RW-AGENCYMG | UNKNOWN | `recovery.access.partner` | E2:5939,6049 | per-partner-type key |
| `rwb.access.partner.instruction-types.PT-VALUER` | `APPRAISE` (a) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | RW-AGENCYMG | UNKNOWN | `recovery.access.partner` | E2:5939 | |
| `rwb.access.partner.instruction-types.PT-AGENCY` | `COLLECT` (a) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | RW-AGENCYMG | UNKNOWN | `recovery.access.partner` | E2:5939 | |
| `rwb.ace.plan.batch-size` | `500` (a; DL11) | INTEGER | ACCOUNTS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.integration.aceplan` | E2:596; BN2:87 | |
| `rwb.ace.plan.timeout-ms` | `2000` (a; DL11) | INTEGER | MILLISECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.integration.aceplan` | E2:596; BN2:87 | |
| `rwb.agent.gateway.base-url` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.agent.client` | E1-058:406 | "environment property, not a business value" |
| `rwb.agent.gateway.identity` | UNKNOWN (managed identity of SY-AGENT) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.agent.client` | E1-058:406 | |
| `rwb.approval.area.<decisionCode>` | UNKNOWN; pattern values described: D5/D6.x = Treatment and offer, D7.x = Litigation, D8.2/D8.3 = Asset and disposal, D8.4 = Debt sale, D9.x = Write-off and posting | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.approval` | E2:3842; BN2:737 | parameterised suffix |
| `rwb.approval.route.D7.1.area` | `LITIGATION` (a; DL22) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.approval` | E2:3840,3986 | pattern `rwb.approval.route.<decision>.<attr>` |
| `rwb.approval.route.D7.1.role` | `RW-LITOFF` (a; DL22) | STRING (role code) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.approval` | E2:3840,3897,3986 | |
| `rwb.approval.route.D7.1.escalation-role` | `RW-HEADLIT` (a; DL22) | STRING (role code) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.approval` | E2:3840; BN2:749 | |
| `rwb.approval.route.D7.1.service-level` | `1 working day` (a; DL22) | DURATION | WORKING_DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.approval` | E2:3840 | |
| `rwb.approval.service-level.default` | `3 working days` (a; DL22, from R-RES-10 / R-SET-05) | DURATION | WORKING_DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.approval` | E2:3841 | |
| `rwb.calendar.bank-holidays` | UNKNOWN — empty list (a: "empty at go-live" is stated for approved-callers, **not** for this key; treat holiday list as UNKNOWN) | CODE_LIST | DATE | n/a | n/a | GLOBAL | UNKNOWN | RW-REFADM (stated) | UNKNOWN | timer/due-date calculators | E2:9865,10001,10112 | loaded by RW-REFADM |
| `rwb.casewf.placement.approved-callers` | `empty` at go-live (a) | JSON | none | n/a | n/a | GLOBAL | UNKNOWN | RW-COE requests / RW-RISK approves | UNKNOWN | `recovery.casewf.placement` | E2:10217,10348,10452; BN2:1809 | list of callerCode, type MODEL/AGENT, service identity |
| `rwb.comms.dispatch.barcode-break-days` | `3` (stated) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.comms.dispatch` | E1-055:263; BN1:3121 | |
| `rwb.comms.dispatch.eligible-states` | `GENERATED` (E1-055) **and** `APPROVED` (E2-021) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.comms.notices` | E1-055:263; E2:6239,6492,1113; BN1:3073 | **value conflict C6** |
| `rwb.comms.dispatch.max-attempts` | `3` (stated; INT-14) | INTEGER | ATTEMPTS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.comms.dispatch` | E1-055:263 | |
| `rwb.comms.pod.stale-after-business-days` | `1` (stated; INT-15) | INTEGER | BUSINESS_DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.comms.dispatch` | E1-055:263 | |
| `rwb.comms.template.allowed-types` | `DOCX` (stated) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.comms.templates` | E1-034:235 | |
| `rwb.comms.template.max-size-mb` | `10` (a; DL11) | INTEGER | MEGABYTES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.comms.templates` | E1-034:235; BN1:1967 | |
| `rwb.customer.products.party-roles` | `BORROWER, CO_BORROWER` (stated) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.integration.customer` | E2:853; BN2:151 | |
| `rwb.dataengine.freshness.alert-channel` | UNKNOWN (channel name) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.freshness` | E1-015:238; BN1:871 | |
| `rwb.dataengine.lake.container` | UNKNOWN (container name) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.lake` | E1-014:249; BN1:819 | |
| `rwb.dataengine.lake.page-size` | `5000` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.lake` | E1-014:249; BN1:813 | |
| `rwb.dataengine.lake.path-prefix` | `decision-log` (stated) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.lake` | E1-014:249; BN1:819 | |
| `rwb.dataengine.lake.rows-per-file` | `50000` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.lake` | E1-014:249 | |
| `rwb.dataengine.ledger.event-map` | `EV-01=CASE_CREATED, EV-02=CASE_ALLOCATED, EV-04=CASE_TRANSFERRED, EV-08=DECISION_TAKEN, EV-16=DOCUMENT_ATTACHED, EV-19=CASE_ESCALATED` (stated) | JSON | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.ledger.events` | E1-067:214; BN1:3739 | |
| `rwb.dataengine.ledger.page-size-default` | `50` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.ledger.read` | E1-068:220; BN1:3779 | |
| `rwb.dataengine.ledger.page-size-max` | `200` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.ledger.read` | E1-068:220; BN1:3797 | |
| `rwb.dataengine.retention.archive-container` | UNKNOWN (container name) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.retention` | E1-017:257 | |
| `rwb.dataengine.retention.batch-size` | `5000` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dataengine.retention` | E1-017:257 | |
| `rwb.decision.chain.genesis-hash` | `64` zeros (stated) | STRING (hex) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.log` | E1-008:207; BN1:459 | |
| `rwb.decision.chaincheck.batch-size` | `1000` (a; Asia/Bangkok) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COMPLY | UNKNOWN | `recovery.decision.audit` | TE-008:35,198 | |
| `rwb.decision.chaincheck.latest-start` | `04:00` (a) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COMPLY | UNKNOWN | `recovery.decision.audit` | TE-008:35,198 | |
| `rwb.decision.chaincheck.start` | `02:00` (a) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COMPLY | UNKNOWN | `recovery.decision.audit` | TE-008:35,198 | |
| `rwb.decision.code.CASE_CREATED` | `D6` (a) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | RW-DATASTEW | UNKNOWN | `recovery.decision.writer` | E1-027:35,199 | 4 keys in this family |
| `rwb.decision.code.CASE_TRANSFERRED` | `D6` (a) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | RW-DATASTEW | UNKNOWN | `recovery.decision.writer` | E1-027:35,199 | |
| `rwb.decision.code.DOCUMENT_ATTACHED` | `D6` (a) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | RW-DATASTEW | UNKNOWN | `recovery.decision.writer` | E1-027:35,199 | |
| `rwb.decision.code.OWNER_ASSIGNED` | `D6` (a) | CODE | none | n/a | n/a | GLOBAL | UNKNOWN | RW-DATASTEW | UNKNOWN | `recovery.decision.writer` | E1-027:35,199 | |
| `rwb.decision.input-age-days.POSTAL_ADDRESS` | `30` (a; DL22) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COE | UNKNOWN | notice approval / freshness check | E2:4246,4365; BN2:783 | suffix = input type |
| `rwb.decision.input-age-days.TOTAL_BALANCE` | `1` (a; DL22) | INTEGER | DAYS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-COE | UNKNOWN | notice approval / freshness check | E2:4246,4365; BN2:783 | |
| `rwb.decision.query.max-cases` | `500` (a; DL11) | INTEGER | CASES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.audit` | E2:1407,1468 | |
| `rwb.decision.query.max-size` | `500` (a; DL11) | INTEGER | ROWS | `1` | `500` | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.decision.audit` | E2:1407,1468 | range 1–500 stated |
| `rwb.dochub.casedocs.page-size` | `20` (stated) | INTEGER | ROWS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dochub.casedocs` | E1-026:250; BN1:1527 | |
| `rwb.dochub.classify.model-route` | UNKNOWN (gateway route name, DL33) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.classify` | E1-050:241; BN1:2801 | |
| `rwb.dochub.container.intake` | UNKNOWN (container; `rwb-intake` implied) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.storage` | TE-012:200,230; E1-057:300 | name from TE-012 |
| `rwb.dochub.container.legal` | UNKNOWN (`rwb-docs-legal` implied) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.storage` | TE-012:202,230 | |
| `rwb.dochub.container.quarantine` | UNKNOWN (`rwb-quarantine` implied) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.storage` | TE-012:203,230; E1-041:264; BN1:2303 | |
| `rwb.dochub.container.standard` | UNKNOWN (`rwb-docs` implied) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.storage` | TE-012:201,230 | |
| `rwb.dochub.extract.model-route` | UNKNOWN (gateway route, DL33) | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.extract` | E1-053:280 | |
| `rwb.dochub.intake.branch-folders` | UNKNOWN (branch code → path map) | JSON | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.intake` | E1-057:300 | |
| `rwb.dochub.intake.mailboxes` | UNKNOWN (code → address map) | JSON | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.intake` | E1-057:300 | |
| `rwb.dochub.intake.mailroom-folder` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.intake` | E1-057:300 | |
| `rwb.dochub.intake.sftp-root` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.intake` | E1-057:300 | |
| `rwb.dochub.ocr.endpoint` | UNKNOWN | STRING (URL) | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.ocr` | E1-049:237; BN1:2743 | |
| `rwb.dochub.scan.timeout-seconds` | `30` (stated) | INTEGER | SECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dochub.scan` | E1-041:264; BN1:2297 | |
| `rwb.dochub.storage.account-url` | UNKNOWN | STRING (URL) | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dochub.storage` | TE-012:230 | |
| `rwb.dochub.storage.timeout-seconds` | `10` (stated) | INTEGER | SECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.dochub.storage` | TE-012:230 | |
| `rwb.flags.cache-seconds` | `30` (a; DL11) | INTEGER | SECONDS | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.integration.flags` | E1-047:225; BN1:2633 | |
| `rwb.integration.outbox.consumers` | consumer `win-dispatch` of WIN_DISPATCH holds a case step, owner RW-PLATADM (a) | JSON | none | n/a | n/a | GLOBAL | UNKNOWN | RW-REFADM loads | UNKNOWN | `recovery.integration.outbox` | TE-006:33,301; E2:9758,1669 | **name collides with flag `rwb.integration.outbox` (C10)** |
| `rwb.integration.outbox.retry` | `3` retries at `1, 5, 15` minutes (a; NFR-026, DL11) | JSON | MINUTES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-REFADM | UNKNOWN | `recovery.integration.outbox` | TE-006:34,301 | |
| `rwb.integration.sftp.host` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.integration.adapter` | E1-007:266 | |
| `rwb.jobs.collins.last-retry` | `09:00` (stated) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.integration.feeds` | E1-051:195; BN1:2859 | |
| `rwb.jobs.collins.start` | `05:00` (stated) | TIME | TIME_OF_DAY | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.integration.feeds` | E1-051:195; BN1:2859 | |
| `rwb.jobs.files.weekly-cron` | `Monday 04:00` (stated) | STRING | CRON | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | UNKNOWN | `recovery.integration.feeds` | E1-051:195 | not a 6-field cron expression |
| `rwb.maskedcopy.allowed-environments` | `SIT,UAT` (stated) | CODE_LIST | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | SIT, UAT | `recovery.tools.maskedcopy` | TE-004:195 | |
| `rwb.maskedcopy.intake-container` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.tools.maskedcopy` | TE-004:195 | |
| `rwb.p1.collins.int01.table` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.load.als` | E1-003:281; BN1:163 | staging table name |
| `rwb.p1.collins.int02.table` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.load.als` | E1-003:281; BN1:163 | |
| `rwb.p1.collins.int07.table` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.load.efs` | E1-004:230 | |
| `rwb.p1.collins.trailer.table` | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | per environment | `recovery.dataengine.load.als` | E1-003:281; BN1:163 | |
| `rwb.refload.approver.delegation_limit` | `RW-RISK` (stated) | STRING (role) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.delegation` | E1-038:37,238 | `_` in name |
| `rwb.refload.approver.masking_rule` | `RW-COMPLY` (stated) | STRING (role) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.matrix` | E1-037:38,262; BN1:2083 | `_` in name |
| `rwb.refload.approver.partner_user` | `RW-SECADM` (stated) | STRING (role) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.partner` | E2:5939,1061 | `_` in name |
| `rwb.refload.approver.permission` | `RW-SECADM` (stated) | STRING (role) | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | `recovery.access.matrix` | E1-037:38,262; BN1:2083 | dot then no underscore (inconsistent) |
| `rwb.reporting.baseline-date` | `2026-11-27` (stated) | DATE | none | n/a | n/a | GLOBAL | UNKNOWN | Tribe lead | UNKNOWN | `recovery.reporting.baseline` | E1-013:36,246; BN1:773 | |
| `rwb.sandbox.cases.hire-purchase` | `1296` (stated) | INTEGER | CASES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | tech lead | DEV only | `recovery.tools.sandbox` | E1-065:227 | |
| `rwb.sandbox.cases.mortgage` | `1226` (stated) | INTEGER | CASES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | tech lead | DEV only | `recovery.tools.sandbox` | E1-065:227 | |
| `rwb.sandbox.cases.ssme` | `290` (stated) | INTEGER | CASES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | tech lead | DEV only | `recovery.tools.sandbox` | E1-065:227 | |
| `rwb.sandbox.seed` | `20261128` (stated) | INTEGER | none | n/a | n/a | GLOBAL | UNKNOWN | tech lead | DEV only | `recovery.tools.sandbox` | E1-065:227; BN1:3629 | |
| `rwb.sandbox.shape-count` | `10` (stated) | INTEGER | CASES | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | tech lead | DEV only | `recovery.tools.sandbox` | E1-065:227; BN1:3635 | |
| _(unnamed)_ SFTP private key | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | DEV, SIT (cited) | `recovery.integration.adapter` (`SftpTransport`) | E1-007:35,258,266 | **no key name given** — secret, not in catalog tables |
| _(unnamed)_ migration DB account | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | all | Flyway / SchemaDriftCheck | E1-044:34,159; BN1:2489 | key store, no key name |
| _(unnamed)_ read-only DB account | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | RW-PLATADM | SIT, UAT, PROD | `SchemaDriftCheck` | E1-044:34; BN1:2489 | key store, no key name |
| _(unnamed)_ bank signing certificate | UNKNOWN | STRING | none | n/a | n/a | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | EasyApp e-sign via ACE module (INT-34) | E2:5607,5890; BN2:1015 | key store, no key name |

---

## Table 4 — Keys used explicitly as NEGATIVE test fixtures (must NOT be seeded)

| key | why | source |
|---|---|---|
| `allocation.retry.limit` | AC3 catalogue-completeness negative: code reads it, catalog does not list it, build must fail naming it. Test TC-E1-042-03 uses a fixture that reads it. **Must not appear in `config/parameter-catalog.csv`.** | **E1-042:99,101,295**; BN1:2361 |
| `rwb.casewf.not-defined` | Feature-flag negative fixture: `FeatureFlags.isOn` on an undefined key must return false (off by default). | E1-047:116 |
| `rwb.p9.unknown` | Feature-flag negative fixture: change request for an unknown flag must be refused. | E1-047:133 |

Negative **values** (not negative keys, listed for completeness): `case.entry.dpd = 400` (range breach, AC5), `case.entry.dpd = "ninety"` (type breach, AC6), `NOTICE_PERIOD_DAYS = 0` (E1-045 AC4), `CLASSIFY_THRESHOLD` changed to `0.90` (E1-050 AC9).

---

## Table 5 — Naming conflicts (same concept, different key)

| # | Concept | Key A | Key B | Evidence | Assessment |
|---|---|---|---|---|---|
| **C1** | Day-past-due entry threshold | `case.entry.dpd` (GLOBAL, INTEGER, 1–365, default 90) | `case.entry.dpd_threshold` (E2, default 90) **and** `ENTRY_DPD` (PRODUCT scope, required) | E1-042:83 vs E2:85,195,301 + BN2:29 vs E1-045:138 | **Three names for one concept.** Epic 2 renames the Epic 1 key and BN2 uses it as the read key; E1-045 then requires the same threshold as a PRODUCT-scope code. E1-042's Background fixes `case.entry.dpd` as GLOBAL. Unresolvable without a decision. |
| **C2** | Case-list count tolerance | `recon.caselist.tolerance.pct` (default 0.00) | `recon.tolerance.pct` (default 0.00, per reconciliation) | E1-002:36,163,290 vs E1-011:35,132,232, BN1:651 | Two keys for the REC-01 case-list count check. `recon.tolerance.pct` is stated "per reconciliation", so it may subsume the other — but both are stated as "loaded". |
| **C3** | Load window end | `load.window.end` (`09:00`, ALS/INT-01/INT-02) | `load.window.end.INT-07` (`08:00`, EFS) | E1-003:36 vs E1-004:37,161,263 | Per-interface suffix changes the key structure. A seed needs both, or a per-interface suffix convention must be declared. |
| **C4** | Prescription warning lead time | `legal.prescription.warn.days` = **180** (E1-028, owner Legal) | `prescription.warning-days` = **90** (E2, assumed DL22) | E1-028:37,293; BN1:1619 vs E2:4567,4686,4793; BN2:859 | **Name and default both differ.** Same PRESCRIPTION timer `warn_at`. Epic 2 appears to re-baseline Epic 1's value without recording a change. |
| **C5** | Plan due-date warning | `plan.warn-days` = 3 (dot-and-dash) | same key described as a **product parameter** in E2-006 while all other product parameters are UPPER_SNAKE (`CURE_PERIOD_DAYS`, `NOTICE_PERIOD_DAYS`) | E2:943,1187 vs E1-045:138 | Naming-style and scope-classification conflict inside the PRODUCT-scope family. |
| **C6** | Dispatch-eligible notice states | `rwb.comms.dispatch.eligible-states` = `GENERATED` (E1-055) | same key = `APPROVED` (E2-021) | E1-055:263; BN1:3073 vs E2:6239,6492,1113 | **Same key, two defaults.** Presents as deliberate Epic 2 progression, but a single seed cannot hold both; needs an environment/date-versioned value. |
| **C7** | Section/panel timeout | `caserecord.section.timeout.ms` = 3000 | `caseview.deviation-timeout-ms` = 2000 `timeline.source-timeout-ms` = 2000 | E1-023:266; E2:4793,5118 | Three timeout parameters with three naming styles (`ms` suffix vs `-ms` suffix, dot vs dash) for the same screen's calls. |
| **C8** | Tolerance/percent suffix style | `load.hold.tolerance.pct`, `recon.tolerance.pct` (`.pct` last segment) | `recon.efs.alert_pct`, `recon.efs.clean_days_required` (`_pct` / `_required` inline) | E1-003:36; E1-011:35 vs E2:6946 | Inconsistent unit-suffix convention across the same parameter family. |
| **C9** | Booking grace | `booking.missing.grace_loads` (underscore) | no second name; but E2 prose and BR5 alternate "grace" / "grace_loads" | E2:1911,2025,2118; BN2:401 | Single key, but violates the dotted-lower-case convention; a scanner using the documented pattern `^[a-z0-9]+(\.[a-z0-9-]+)+$` will miss it. |
| **C10** | Outbox | flag `rwb.integration.outbox` | config keys `rwb.integration.outbox.consumers`, `rwb.integration.outbox.retry` | TE-006:33,34,36 | Flag key is a strict prefix of two config keys → prefix-match lookups on `GET /admin/parameters?key=` will collide. |
| **C11** | Approver-role family | `rwb.refload.approver.permission` (dot) | `rwb.refload.approver.masking_rule`, `.delegation_limit`, `.partner_user` (underscore) | E1-037:38; E1-038:37; E2:5939 | Two separators inside one family; BR3 refers to them collectively as `rwb.refload.approver.*`, which cannot match both. |
| **C12** | Retention batch size | `rwb.dataengine.retention.batch-size` | none | E1-017:257 | Single key; noted only because `rwb.dataengine.lake.page-size` and `rwb.dataengine.ledger.page-size-default` use a third convention (`page-size`, `page-size-default`). |
| **C13** | Doctype vs doctype table | `rwb.dochub.doctypes` (flag) | `rwb.dochub.container.*`, `rwb.dochub.intake.*` (properties) | E1-025:250; TE-012:230 | Same namespace prefix carries both flags and properties with no discriminator other than the catalog `kind` column. |
| **C14** | `rwb.p1.collins.*.table` vs reference data | staging table names as catalog properties | `interface_config` rows hold the same table names for INT-10..INT-16, INT-25 | E1-003:281 vs E1-007:266 | Two stores for the same class of value (table names), one catalog, one reference data. |

---

## Table 6 — `document_hub_parameter` rows (SEPARATE table, created by RWB-E1-024 — NOT `parameter_catalog`)

These are named "parameters" and defaulted throughout Epic 1/2, but the corpus consistently says they live in `document_hub_parameter`, loaded by RW-REFADM. **Do not seed into `parameter_catalog` unless a decision merges the tables.** Type/unit/range are almost never stated.

| key | default (stated / assumed) | type | unit | scope | owner | source |
|---|---|---|---|---|---|---|
| `ACCOUNT_NO_PATTERN` | `[0-9]{10}` (a; DL21) | STRING (regex) | none | GLOBAL | RW-REFADM | E1-032:35,189,315 |
| `BE_YEAR_OFFSET` | `543` (a; DL11) | INTEGER | YEARS | GLOBAL | RW-REFADM | E1-053:35,279 |
| `CAPTURE_CLOCK_SKEW_MINUTES` | `5` (a; DL11) | INTEGER | MINUTES | GLOBAL | RW-REFADM | E2:7222,7373,7466 |
| `CAPTURE_MAX_AGE_DAYS` | `30` (a; DL11) | INTEGER | DAYS | GLOBAL | RW-REFADM | E2:7222,7373,7466 |
| `CAPTURE_MAX_FILES` | `50` (a; DL11) | INTEGER | FILES | GLOBAL | RW-REFADM | E2:7222,7466 |
| `CASE_NO_PATTERN` | `RW-[0-9]{4}-[0-9]{6}` (a; DL21) | STRING (regex) | none | GLOBAL | RW-REFADM | E1-032:35,189,315 |
| `CLASSIFY_MAX_PAGES` | `3` (a) | INTEGER | PAGES | GLOBAL | RW-REFADM | E1-050:35,83,240 |
| `CLASSIFY_THRESHOLD` | `0.80` (a; DL11) | DECIMAL | RATIO 0–1 | GLOBAL | RW-REFADM | E1-032:35,91; E1-050:34,82; E1-054 |
| `CLASSIFY_TIMEOUT_SECONDS` | `60` (a; R-UNI-32) | INTEGER | SECONDS | GLOBAL | RW-REFADM | E1-050:35,83,240 |
| `EXTRACT_ACCURACY_PASS` | `0.90` (a; DL11) | DECIMAL | RATIO 0–1 | GLOBAL | RW-REFADM | E2:7585,7710,7800 |
| `EXTRACT_FIELD_THRESHOLD` | `0.80` (a; DL11) | DECIMAL | RATIO 0–1 | GLOBAL | RW-REFADM | E1-053:35,85,175,279 |
| `EXTRACT_MAX_ATTEMPTS` | `3` (a; DL11) | INTEGER | ATTEMPTS | GLOBAL | RW-REFADM | E1-053:35,180,279 |
| `EXTRACT_PRECISION_PASS` | `0.90` (a; DL11) | DECIMAL | RATIO 0–1 | GLOBAL | RW-REFADM | E1-053:35,279 |
| `EXTRACT_RECALL_PASS` | `0.90` (a; DL11) | DECIMAL | RATIO 0–1 | GLOBAL | RW-REFADM | E1-053:35,279 |
| `EXTRACT_TIMEOUT_SECONDS` | `60` (a; DL11) | INTEGER | SECONDS | GLOBAL | RW-REFADM | E1-053:35,180,279 |
| `FREE_TEXT_MAX_CHARS` | `100` (a; DL11) | INTEGER | CHARACTERS | GLOBAL | RW-REFADM | E1-033:36,233 |
| `FREE_TEXT_MIN_CHARS` | `3` (a; DL11) | INTEGER | CHARACTERS | GLOBAL | RW-REFADM | E1-033:36,233 |
| `GEN_FONT` | `"TH Sarabun New"` (a) | STRING | none | GLOBAL | RW-REFADM | E2:8185 |
| `GEN_IDEMPOTENCY_HOURS` | `24` (a) | INTEGER | HOURS | GLOBAL | RW-REFADM | E2:5490,8127,8185; BN2:969,1445 |
| `GEN_MAX_TEMPLATES` | `10` (a) | INTEGER | TEMPLATES | GLOBAL | RW-REFADM | E2:8185 |
| `INTAKE_ALERT_AFTER_FAILURES` | `2` (a; DL11) | INTEGER | FAILURES | GLOBAL | RW-REFADM | E1-057:37,301 |
| `INTAKE_ALLOWED_TYPES` | `PDF, JPG, PNG` (a) | CODE_LIST | none | GLOBAL | RW-REFADM | E1-024:37,89,293; E1-026:36; E1-057:37,88 |
| `INTAKE_DUPLICATE_WINDOW_DAYS` | `30` (a; DL11) | INTEGER | DAYS | GLOBAL | RW-REFADM | E1-057:37,198,301 |
| `INTAKE_MAX_FILE_MB` | `25` (a; DL11) | INTEGER | MEGABYTES | GLOBAL | RW-REFADM | E1-024:37,89,293; E1-026:36; E1-057:37 |
| `INTAKE_MIN_IMAGE_KB` | `10` (a; DL11) | INTEGER | KILOBYTES | GLOBAL | RW-REFADM | E1-057:37,301 |
| `OCR_MAX_ATTEMPTS` | `3` (a; DL11) | INTEGER | ATTEMPTS | GLOBAL | RW-REFADM | E1-049:35,81,236 |
| `OCR_MIN_QUALITY` | `0.70` (a; DL11) | DECIMAL | RATIO 0–1 | GLOBAL | RW-REFADM | E1-049:35,81,147,236 |
| `OCR_TIMEOUT_SECONDS` | `120` (a; DL11) | INTEGER | SECONDS | GLOBAL | RW-REFADM | E1-049:35,58,236 |
| `OCR_WORKERS` | `4` (a; DL11) | INTEGER | WORKERS | GLOBAL | RW-REFADM | E1-049:35,81,236 |
| `REVIEW_DATE_MAX` | `2100-12-31` (a; DL11) | DATE | none | GLOBAL | RW-REFADM | E1-054:35,122,335 |
| `REVIEW_DATE_MIN` | `2000-01-01` (a; DL11) | DATE | none | GLOBAL | RW-REFADM | E1-054:35,122,335 |
| `REVIEW_PAGE_SIZE` | `50` (a; DL11) | INTEGER | ROWS | GLOBAL | RW-REFADM | E1-054:35,263,335 |
| `REVIEW_TEAM_UNATTACHED` | `"DOC-SVC"` (a) | STRING (team code) | none | GLOBAL | RW-REFADM | E1-054:35,87,199,335 |
| `SEARCH_MAX_RESULTS` | `1000` (a; DL11) | INTEGER | ROWS | GLOBAL | RW-REFADM | E1-033:36,60,233 |
| `SEARCH_PAGE_SIZE` | `50` (a; DL11) | INTEGER | ROWS | GLOBAL | RW-REFADM | E1-033:36,233 |

**Also stated as agent-policy limits, not catalog keys:** timeout `1–120` seconds and confidence floor `0–1` are held in the `agent_policy` JSON schema (E1-058:406), not in the catalog.

---

## Table 7 — Feature flags (separate mechanism, E1-047; explicitly out of E1-042 scope)

39 flags. Not catalog entries; listed so the seed builder does not add them. Each has key, default (mostly off), owner team, removal date.

`rwb.p1.data-catalog`, `rwb.p1.case-list`, `rwb.p1.als-load`, `rwb.p1.efs-load`, `rwb.p1.tracker-inventory`, `rwb.p1.dq-rules`, `rwb.p1.collateral-load`, `rwb.p1.tracker-load`, `rwb.p1.reconciliation`, `rwb.p1.tracker-retire`, `rwb.p1.dq-rules`, `rwb.reporting.baseline`, `rwb.dataengine.lake-copy`, `rwb.dataengine.freshness-stamp`, `rwb.dataengine.product-access`, `rwb.dataengine.retention`, `rwb.p3.casecreation`, `rwb.p3.queuetables`, `rwb.p3.allocation`, `rwb.p3.transfer`, `rwb.access.sso-roles`, `rwb.p3.caserecordview`, `rwb.dochub.store`, `rwb.dochub.doctypes`, `rwb.dochub.casedocs`, `rwb.decision.log-writer`, `rwb.p3.timers`, `rwb.p3.ruleload`, `rwb.p3.rebalance`, `rwb.p3.caselistqueue`, `rwb.dochub.autoattach`, `rwb.dochub.search`, `rwb.comms.template-admin`, `rwb.p3.timeline`, `rwb.access.permission-matrix`, `rwb.access.delegation-table`, `rwb.access.access-log`, `rwb.dochub.checklist`, `rwb.dochub.malware-scan`, `rwb.dochub.retention`, `rwb.p3.configservice`, `rwb.p3.refdata-versions`, `rwb.p3.migration-drift-gate`, `rwb.p3.product-parameters`, `rwb.comms.template-catalog`, `rwb.p3.change-log`, `rwb.dochub.ocr`, `rwb.dochub.classify`, `rwb.integration.legacy-feeds`, `rwb.comms.notice-generation`, `rwb.dochub.extract`, `rwb.dochub.review`, `rwb.comms.win-dispatch-v1`, `rwb.integration.job-monitoring`, `rwb.dochub.intake` (+ sub-flags `rwb.dochub.intake.branch`, `.mailroom`, `.sftp`, `.email`), `rwb.agent.platform`, `rwb.agent.intake-shadow`, `rwb.agent.extraction-eval`, `rwb.agent.promotion`, `rwb.agent.screening-shadow`, `rwb.agent.monitor`, `rwb.dataengine.data-dictionary`, `rwb.dataengine.sandbox`, `rwb.dataengine.ledger-writer`, `rwb.dataengine.ledger-events`, `rwb.dataengine.ledger-read`, `rwb.dataengine.masked-copy`, `rwb.p3.rule-harness`, `rwb.p3.quartz-jobs`, `rwb.decision.hash-check`, `rwb.dochub.storage-containers`, `rwb.agent.client`, `rwb.integration.file-adapters`, `rwb.decision.log-store`, `rwb.integration.efs-handover`, `rwb.integration.ace-plan-status`, `rwb.integration.customer-products`, `rwb.p3.plan-timers`, `rwb.decision.audit-query`, `rwb.integration.nleads-pack`, `rwb.integration.booking-confirmation`, `rwb.payments.matching`, `rwb.reporting.steering`, `rwb.dataengine.stage2-products`, `rwb.p3.queue-views`, `rwb.p3.manual-transfer`, `rwb.decision.approval-routing`, `rwb.decision.notice-approval`, `rwb.p3.case-clocks`, `rwb.p3.full-timeline`, `rwb.dochub.generation-screens` (+ `rwb.dochub.generation-screens.send`), `rwb.comms.esign`, `rwb.access.partner-signin`, `rwb.comms.win-dispatch-loop`, `rwb.comms.sms-line`, `rwb.integration.efs-recon`, `rwb.integration.efs-manual-upload`, `rwb.dochub.field-capture`, `rwb.dochub.extraction-stage23`, `rwb.dochub.generation-engine`, `rwb.payments.matching-rules`, `rwb.agent.monitor-v2`, `rwb.agent.tdr-suggestion`, `rwb.casewf.case-list-ageing`, `rwb.integration.ledger-channels`, `rwb.casewf.next-action`, `rwb.casewf.queue-placement`, `rwb.agent.intake-l1`, `rwb.agent.screening-l1`, `rwb.agent.legal-shadow`, `rwb.casewf.case-list-queue-column`.

---

## Summary of counts

| Family | Count | Notes |
|---|---|---|
| **Catalog entries, business, GLOBAL (Table 1)** | **38** | incl. `case.entry.dpd` and its Epic 2 alias `case.entry.dpd_threshold`, and `load.window.end` + `.INT-07` |
| **Catalog entries, scope PRODUCT (Table 2)** | **5** | ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS, EXPOSURE_BAND_SET |
| **Environment settings / properties / secrets (Table 3)** | **92** | 9 `spring.flyway.*`, 1 env var, 3 unnamed secrets, 1 named secret, 78 `rwb.*` properties |
| **Total unique keys for the E1-042 seed (Tables 1–3)** | **135** | 38 + 5 + 92 |
| **Negative fixtures — must not be seeded (Table 4)** | **3** | `allocation.retry.limit` + 2 flag negatives |
| **`document_hub_parameter` rows, separate table (Table 6)** | **33** | not catalog entries |
| **Feature flags, separate mechanism (Table 7)** | **~100 flag keys incl. sub-flags** | not catalog entries |
| **Naming conflicts (Table 5)** | **14** | 6 are true same-concept duplicates (C1–C6) |

### Quality of the source data for a seed

- **Only one key is fully specifiable from the corpus**: `case.entry.dpd` — INTEGER, 1–365, default 90, GLOBAL, required, owner RW-COE, used by `recovery.casewf.casecreation` (E1-042:83).
- **Only one further key has a stated required flag**: `refdata.cache.ttl-seconds` (required, E1-042:105).
- **Only one key has a stated scope other than GLOBAL for a dotted key**: none — every PRODUCT-scope entry uses UPPER_SNAKE.
- **`min`/`max` are stated for only 4 keys**: `case.entry.dpd` (1–365), `queue.cap.max` (1–500), `NOTICE_PERIOD_DAYS` (1–365), `rwb.decision.query.max-size` (1–500).
- **`owner` is stated for only 8 keys**: RW-COE (case.entry.dpd, case.entry.dpd_threshold), business lead (`efs.history.action.codes`), Legal (`legal.prescription.warn.days`), RW-DATASTEW (`rwb.decision.code.*`), RW-COMPLY (`rwb.decision.chaincheck.*`), RW-AGENCYMG (`rwb.access.partner.instruction-types.*`), Tribe lead (`rwb.reporting.baseline-date`), tech lead (`rwb.sandbox.*`).
- **`environments` is stated for 6 keys**; everything else is `UNKNOWN` or a vague "per environment".
- **92 of 135 catalog keys have no stated default at all** — they are named properties whose value the platform administrator supplies per environment.

### Highest-risk items before seeding

1. **C1 is a blocker**: `case.entry.dpd` / `case.entry.dpd_threshold` / `ENTRY_DPD` cannot all be seeded; E1-042's Background fixes one, Epic 2 reads another, E1-045 requires a third at PRODUCT scope.
2. **C4 is a data-integrity risk**: 180 vs 90 for the same prescription warning, with different key names and different owners.
3. **C6 is a versioning risk**: one key, two defaults (`GENERATED` → `APPROVED`) across epics; needs a dated value row, not a single seed default.
4. **C9, C8, C11 break the build check**: E1-042's `CatalogCompletenessCheck` compares keys *read through ParameterService* against the catalog. Any key whose name does not match the documented `[a-z0-9]+(\.[a-z0-9-]+)+` shape (`booking.missing.grace_loads`, `recon.efs.alert_pct`, `rwb.refload.approver.masking_rule`, `restructure.max_breaks`) will slip past a regex-based scanner and fail `CatalogCompletenessCheck` at runtime instead.
5. **Two-store overlap**: 33 `document_hub_parameter` rows and ~100 flags share the same `rwb.*`/parameter vocabulary but are governed by different tables. Seeding them into `parameter_catalog` would duplicate ownership and break E1-024's table contract.

<details><summary>Reasoning</summary>

Good. Secrets: ace.db.password (named), SFTP key (unnamed), bank signing certificate (unnamed, in key store), DB migration + read-only accounts, RWB_SCHEMA.

Now I'm ready to write. Let me be careful about the `environments` column and the `required` column — mostly UNKNOWN.

I'll mark "required" where stated: case.entry.dpd required (yes), refdata.cache.ttl-seconds required (yes), PRODUCT-scope required yes.

Let me now draft the response.

Given the very large number of keys, I'll structure:

1. Scope & method note (short).
2. Table 1: parameter_catalog business keys (GLOBAL scope) — 42 rows incl. negative marked separately? No, negative in separate table.
3. Table 2: PRODUCT-scope catalog parameters.
4. Table 3: Environment settings, properties and secrets.
5. Table 4: Negative fixtures.
6. Table 5: Naming conflicts.
7. Table 6: Non-catalog parameter families (document_hub_parameter; feature flags) — compact.
8. Summary counts.

I'll keep table cells terse. Use "UNK" ... no, must write UNKNOWN.

Column set: key | default (stated/assumed) | type | unit | min | max | scope | req | owner | envs | used_by | source | notes

That's 13 columns. Wide but fine.

To reduce width, I'll drop separate "min"/"max" into one? No, follow instructions.

I'll use defaults column as "90 (stated)" / "90 (assumed; DL16)". For no default: "UNKNOWN".

Let me write out rows carefully.

TABLE 1 — Global business parameters

1. allocation.deviation.queue.code | "DEV-HANDLER" (assumed; DL23) | STRING | none | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN (center of excellence) | UNKNOWN | recovery.casewf.allocation | E1-020:37, E1-020:345 | queue code
2. allocation.exception.queue.code | "RWB-EXC" (assumed; DL23) | STRING | none | UNKNOWN|UNKNOWN|GLOBAL|UNKNOWN|UNKNOWN|UNKNOWN|recovery.casewf.allocation|E1-020:37,345
3. appraisal.max.age | 365 (assumed; DL11, MSG-S5-002, CTL-27) | INTEGER | DAYS (stated) | UNKNOWN | UNKNOWN | GLOBAL | UNKNOWN | UNKNOWN | UNKNOWN | recovery.dataengine.load.ccms/svaf | E1-009:36,165,264
4. booking.missing.grace_loads | 1 (stated, no marker) | INTEGER | LOADS | UNKNOWN|UNKNOWN|GLOBAL|UNKNOWN|UNKNOWN|UNKNOWN|recovery.integration.booking | E2:1911, 2025, 2118 | name also written booking.missing.grace in some places? No—only prefix artifact. But note underscore style.
5. case.entry.dpd | 90 (stated; DL16) | INTEGER | DAYS | 1 | 365 | GLOBAL | true | RW-COE | PROD/SIT/UAT (cited) | recovery.casewf.casecreation | E1-042:33,83,... ; dozens more
6. caselis

_[truncated]_

</details>
