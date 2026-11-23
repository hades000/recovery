# AI development rules

- **Session ID:** `ses_e5a78419cffeKX1faDG6LrwnQZ`
- **Created:** 2026-11-04 14:48  |  **Last activity:** 2026-11-04 14:49
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `build`
- **Tokens:** 29,079 in / 956 out / 456 reasoning
- **Messages:** 6

---

### User - 2026-11-04 14:48

What are rules for ai development

### Assistant - 2026-11-04 14:48 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The user asks "What are rules for ai development". This seems like a vague question. Maybe they're asking about rules for AI development in their workspace? Let me check the working directory — "Recovery Workbench SharePoint Set v14". Perhaps there's a document about AI development rules. Let me look at the files.

The question is ambiguous. But it likely relates to their project files — maybe there's an AGENTS.md or rules doc. Let me check the directory first.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14"}
```

```text
Read directory C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14, entries 1-12
01 Decisions and governance\
02 Business architecture and process\
03 Requirements and specifications\
04 User stories\
05 Technical architecture\
06 Data\
07 Screens and experience\
08 AI and agents\
09 Testing and quality\
10 Policy, controls and compliance\
11 Delivery and operations\
12 Project communication\
```

**Tool `glob`** - completed

```json
{"pattern": "**/*{AGENTS,CLAUDE,rules,RULES,guidelines,GUIDELINES}*"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 021 Transfer rules and engine v1 v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\04 User stories\Recovery Workbench User Stories Epic 1 Story Files v5\RWB E1 006 Data quality rules v1 v1.md
```

### Assistant - 2026-11-04 14:48 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The user asks about "rules for ai development". There's a folder "08 AI and agents". Let's list it.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\08 AI and agents"}
```

```text
Read directory C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents, entries 1-8
Recovery Workbench Agent Catalog and Specifications v2.md
Recovery Workbench Agent Catalog and Specifications v2.xlsx
Recovery Workbench AI and Agent Architecture v2.docx
Recovery Workbench AI and Agent Architecture v2.pptx
Recovery Workbench AI Assisted Development Approach v1.md
Recovery Workbench AI Assisted Development Approach v3.pptx
Recovery Workbench AI Decision Governance v2.docx
Recovery Workbench Model Integration Design v2.docx
```

**Tool `glob`** - completed

```json
{"pattern": "08 AI and agents/**/*"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench AI and Agent Architecture v2.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench AI and Agent Architecture v2.docx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench Agent Catalog and Specifications v2.xlsx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench Agent Catalog and Specifications v2.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench AI Assisted Development Approach v3.pptx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench AI Assisted Development Approach v1.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench AI Decision Governance v2.docx
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench Model Integration Design v2.docx
```

### Assistant - 2026-11-04 14:48 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

The likely relevant doc is "Recovery Workbench AI Assisted Development Approach v1.md". Let me read it.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\08 AI and agents\\Recovery Workbench AI Assisted Development Approach v1.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\08 AI and agents\Recovery Workbench AI Assisted Development Approach v1.md, lines 1-205
1: # Recovery Workbench: AI assisted development approach
2: 
3: SCB Collections and Recovery. Henka Group, 28 October 2026. Version 1.
4: 
5: ## 1. How AI is used
6: 
7: The Recovery Workbench is built with AI in two parts. In both, a person owns the result.
8: 
9: | Part | What AI does | What a person owns |
10: |---|---|---|
11: | AI assisted delivery | Drafts stories, acceptance criteria, edge cases, test cases, UAT scripts, Thai message drafts, release notes and status packs | The analysts, QA and the product owner correct, decide and sign each one |
12: | AI assisted engineering | Proposes the plan for a story, writes the tests and the code, reviews pull requests first | Developers conduct the agent and read every line. Tech leads approve plans. Reviewers approve merges |
13: 
14: Seven working rules apply to both parts.
15: 
16: 1. The person who merges a change owns it, whoever or whatever wrote it.
17: 2. The agent works from files: the standards file, the story file and the plan file. Anything the agent needs is in one of the three.
18: 3. The tests and the acceptance criteria exist before the code is generated.
19: 4. Every line that reaches production is read by a person.
20: 5. An AI error found by a reviewer is written into the standards file, so the agent is told not to repeat it.
21: 6. No personal data or production data goes into a prompt, a test or a log.
22: 7. The unit of work is one story. Work is merged at least once a working day.
23: 
24: ## 2. From story to production
25: 
26: | Step | What happens | Who | Gate |
27: |---|---|---|---|
28: | 1 Story file | AI drafts the story file from the requirement, the routing rules and the data model. The analyst corrects it and owns it | Analyst | Definition of ready |
29: | 2 Plan | The agent reads the story file and the standards file and writes the plan file. The tech lead approves it before any code is written | Developer with the agent; tech lead | Plan approved |
30: | 3 Tests | The agent writes failing tests from the acceptance criteria. The developer checks that each test asserts its criterion | Developer with the agent | Every criterion has a test |
31: | 4 Build | The agent writes the code in DEV with synthetic data, in small commits | Developer with the agent | Tests pass |
32: | 5 AI review | The review agent checks th
... truncated (14,064 chars total)
```

### Assistant - 2026-11-04 14:48 | opencode-go/deepseek-v4.1-flash | build

From `08 AI and agents\Recovery Workbench AI Assisted Development Approach v1.md` (SCB Collections and Recovery, v1, 28 Oct 2026).

## Seven working rules (apply to delivery and engineering)

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files only: the standards file, the story file, the plan file.
3. Tests and acceptance criteria exist before code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found in review is written into the standards file so it isn't repeated.
6. No personal data or production data in a prompt, test or log.
7. The unit of work is one story; merge at least once a working day.

## The standards file — `AGENTS.md`

Kept in the root of the ACE repository, read before every task, owned by the solution architect with the tech leads, changed by pull request like code.

**The agent must:**
- Put recovery code in the recovery module only (common/collection modules only where the story names it).
- Read every threshold, limit, timer, queue, role, template and route from its versioned reference table — never hard-code it.
- Put a Spring Security method check on every endpoint, naming capability area and operation.
- Write a decision record for every case change and decision, with rule ID and version.
- Use business glossary names for classes, fields, tables, endpoints.
- Return validation messages from the message table by rule ID.
- Make database changes by migration script only, one per story.
- Use Spring Batch and Quartz for scheduled work.
- Use the synthetic data generator for test data.
- Write the test before the code; no test means not complete.

**The agent must never:**
- Commit a credential, key or token.
- Call or read inside another module.
- Call a system of record directly (data in via COLLINS, out via integration adapters).
- Add a workflow engine, rules engine or any new dependency.
- Disable, skip or weaken a test.
- Change an already-merged migration script.
- Put personal data in code, fixtures, prompts or log lines.

## Rules for AI tools

1. Only the coding tool approved for SCB code touches the repository.
2. Agents work in DEV with synthetic data; UAT uses masked data; no production data in prompts.
3. Prompts, skills and the standards file live in the repo and are reviewed like code.
4. Throwaway spikes are DEV-only and never merged.
5. A coding agent acts under the developer's identity and holds no permission the developer lacks.

## Gates and flow

Story → plan (tech lead approves before any code) → failing tests → build in DEV → AI review summary → human review and merge → SIT/UAT → update standards file. Merge requires the nine pipeline checks plus a named reviewer. Every PR carries story key, plan, coding tool, reviewer and test results.

One clarification: there's also `Recovery Workbench AI Decision Governance v2.docx`, which covers rules for *AI making business decisions* (a different subject — case decisions, not code). Want me to pull that out too?

<details><summary>Reasoning</summary>

The user asks "What are rules for ai development". Likely they want a summary of the rules defined in this document. Let me answer directly from the document, no need for extra tooling. I could also note the file path.

Let me check if there are other relevant rules docs (AI Decision Governance etc.). But "rules for ai development" most directly maps to "AI Assisted Development Approach". I'll answer with the seven working rules, the agent must/must never, rules for AI tools. Provide concise summary.

Should I use a UI block? The guidance says use for data/structure the user would otherwise picture. This is a list of rules — probably markdown is fine. It says "Not for ... a short list". This is several lists; markdown tables are fine. I'll keep it clear.

Also naming task via openchamber work.name? This is a question, not a coding task. Probably unnecessary. The instruction: "Name the task with work.name as soon as it is clear what the task is". It's a Q&A; I could skip. But maybe still acceptable. I'll skip tool overhead — actually the guidance says to name it. But "task" here is a question. I'd rather not clutter. Hmm, the instruction is fairly directive. But it's for tasks. A question is not a task. I'll skip.

Answer concisely, referencing the source. Include the key distinction: principles, agent must, agent must never, tool rules, gates.

</details>
