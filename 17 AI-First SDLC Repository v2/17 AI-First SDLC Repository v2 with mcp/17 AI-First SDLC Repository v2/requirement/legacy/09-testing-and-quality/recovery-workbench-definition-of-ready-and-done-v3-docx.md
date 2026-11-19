<!-- source: 09 Testing and quality/Recovery Workbench Definition of Ready and Done v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `09 Testing and quality/Recovery Workbench Definition of Ready and Done v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Definition of ready and definition of done

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench definition of ready and definition of done |
| Version | 2 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Applies to | Every story built by the TechX recovery squads, Autonomous Ops and Enterprise AI for the Workbench |

# 1. Where each definition applies

| Gate | Passes when | Checked by |
|---|---|---|
| Ready | The story meets the definition of ready in section 2 | Analyst with the tech lead and QA |
| Plan approved | The plan names every file, test and migration and touches one module | Tech lead |
| Merge | The nine pipeline gates pass and a named reviewer approves | Reviewer |
| Done | The story meets the definition of done in section 3 | Product owner |
| SIT exit | Every test case for the release passes in SIT | QA lead |
| UAT exit | The business testers sign the UAT scripts for the release | Business lead |
| Release | SIT and UAT exits are met; unfinished work is behind a flag that is off | Release owner with the application owner |

The worked example of a story that meets the definition of ready is RWB-E1-020, allocate a new case to a queue and an owner.

# 2. Definition of ready

A story is pulled onto the board only when every item below is true. The analyst confirms it at refinement, the tech lead and QA agree, and the story status moves to Ready.

## 2.1 What the story carries

|  | Item | What is true |
|---|---|---|
| 1 | Story | In the form As a role, I want, so that. The role is a role code from the roles table |
| 2 | Links | Epic, module, L3 process and decision, each from the process architecture and the module list |
| 3 | Acceptance criteria | Written in Given, When, Then, each with an ID. The exception paths are covered as well as the main path |
| 4 | Business rules | Each rule has an ID. Routing rules name their rule ID from the rules workbook; table values name their table |
| 5 | State transitions | Every change of case status or route state, with the event and the condition, matches the case model |
| 6 | Authority | Every role that acts, with its permission letters, matches the permission matrix |
| 7 | Data | Every field read or written, with its BR Field ID from the data dictionary. A new field is added to the dictionary first |
| 8 | Contract | The trigger, the service, the events published, the idempotency key and any call out of the module |
| 9 | Messages | Every message with its ID and English text. Thai text is requested under DL10 |
| 10 | Screens and states | The screen, its fields and its empty, loading, error and no-access states, or the statement that there is no screen |
| 11 | Guardrails | What the code must not do, the personal data fields touched, and any limit that applies |
| 12 | Test cases | At least one test case per acceptance criterion, with its synthetic data |
| 13 | Out of scope | What a reader might expect that this story does not do |

## 2.2 What is in place

|  | Item | What is true |
|---|---|---|
| 14 | Epic design | The design for the epic is signed before build starts on the epic. Design runs one epic ahead |
| 15 | INVEST | The story passes the INVEST check and can be finished in two weeks or less |
| 16 | Size | The squad has sized it |
| 17 | Dependencies | Every story, interface and decision it depends on is done, in progress on the board, or behind a flag |
| 18 | Open decisions | No open decision in the decision log blocks it, or the story states the recommended answer it is built on |
| 19 | Test data | The synthetic data it needs exists in DEV, or creating it is part of the story |
| 20 | Reference data | The table rows it reads exist with a version and a test case ID, or loading them is part of the story |

# 3. Definition of done

A story is done only when every item below is true. The product owner accepts it against the acceptance criteria and the story status moves to Done.

## 3.1 Built and tested

|  | Item | What is true |
|---|---|---|
| 1 | Merged | The code is merged into main. Work that is not finished is behind a feature flag that is off |
| 2 | Pipeline | The nine pipeline gates pass: build and unit tests, lint, secret scan, PDPA lint, container scan, module boundary, integration and contract tests, AI first-pass review and human approval |
| 3 | Criteria | Each acceptance criterion has a test that passes |
| 4 | Rules | Each rule row the story uses passes its rule table test against its test case ID |
| 5 | Exceptions | The exception paths named in the story pass, including a failed decision log write |
| 6 | Browser | The main and exception paths of any screen pass in the browser test, once the runner is in the pipeline (DL37) |
| 7 | Deployed | The build is deployed to DEV and to SIT |

## 3.2 Controls

|  | Item | What is true |
|---|---|---|
| 8 | Principle 1 | No threshold, limit, timer, queue, role, template or route is written in code |
| 9 | Decision log | Every decision and every change to a case writes its decision log entry, and the entry is checked in a test |
| 10 | Access | Every endpoint checks the permission and the scope on the server |
| 11 | Personal data | No personal data in code, tests, fixtures, logs or prompts. Masked fields are masked for roles that may not see them |
| 12 | Boundaries | The story touches one module, or the other module's code owner has approved |

## 3.3 Records kept current

|  | Item | What is true |
|---|---|---|
| 13 | Data dictionary | A new or changed field is in the data dictionary with its BR Field ID |
| 14 | Rules workbook | A new or changed rule row is in the rules workbook with its version and test case |
| 15 | Glossary | A new business term is in the business glossary |
| 16 | Standards file | An AI error found in review is added to AGENTS.md |
| 17 | Flags | Any feature flag is in the flag list with its owner and the release in which it is removed |
| 18 | Jira | The pull request carries the story key, and the story records the merged commits |

## 3.4 Accepted

|  | Item | What is true |
|---|---|---|
| 19 | Shown | The story is shown to a business tester during the build (DL09) |
| 20 | Accepted | The product owner accepts the story against its acceptance criteria |

# 4. When a story fails a definition

| Case | What happens |
|---|---|
| Not ready when it is due to be pulled | The story stays in refinement. The next ready story in priority order is pulled instead |
| A decision blocks it | The story is built on the recommended answer in the decision log and the assumption is stated in the story |
| Not done at the epic cut | The story moves to the next epic with its flag off. It is not split to claim part of it as done |
| Fails SIT or UAT | Its flag is switched off and the release goes ahead without it. A defect story is raised |
| A defect traced to AI-written code | It is tagged, and the standards file is updated before the fix merges |

# 5. Who owns each definition

| Definition | Owner | Changed by |
|---|---|---|
| Definition of ready | Product owner with the analysts | Agreement at the weekly delivery review |
| Definition of done | TechX QA lead with the tech leads | Agreement at the weekly delivery review, with the ACE team for items that touch the common module |
