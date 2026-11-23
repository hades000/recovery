SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

## Definition of ready and definition of done

Recovery Workbench, version 3 of the family, dated 28 October 2026. This copy is version 4, dated 22 November 2026, and adds the D-RCV-60 microservice realignment.

| Item | Detail |
|---|---|
| Document | Recovery Workbench definition of ready and definition of done |
| Version | 2 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Applies to | Every story built by the TechX recovery squads, Autonomous Ops and Enterprise AI for the Workbench |
| Family version of this copy | 4 (the next version after v3, Template and Rules §R8.2) |
| Decision | D-RCV-60 microservice realignment |
| Status | Draft. No approval is recorded for this version (ASM-B-TESTDOC-42-10) |


The two metadata readings of the source are kept as written: the Version row reads 2 while the file family reads v3, so this copy takes the next family version, 4 (CG-B-TESTDOC-42-1; ASM-B-TESTDOC-42-1).

| Version | Change log |
|---|---|
| 4 | 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |


# 1. Where each definition applies

| Gate | Passes when | Checked by |
|---|---|---|
| Ready | The story meets the definition of ready in section 2, including the published contract in section 2.3 | Analyst with the tech lead and QA |
| Plan approved | The plan names every file, test and migration and touches one module | Tech lead |
| Merge | The nine pipeline gates pass and a named reviewer approves | Reviewer |
| Done | The story meets the definition of done in section 3, including the contract tests and the boundary tests in section 3.5 | Product owner |
| SIT exit | Every test case for the release passes in SIT | QA lead |
| UAT exit | The business testers sign the UAT scripts for the release | Business lead |
| Release | SIT and UAT exits are met; unfinished work is behind a flag that is off | Release owner with the application owner |


The Checked by column names roles and team types, as in the source. From D-RCV-60 the owning team of every table, endpoint, event, workflow and job a story touches is read from the Microservice Ownership Map v1, and the owning service is named in the story (section 2.3, item 24). The service of a story is therefore never inferred from the module name alone.

## 1.1 The services and their owners (Ownership Map v1)

Every row is a service of Architecture v5. The owner is the suggested owner of R5.3 for contract and app development work: TechX (suggested; any team may pick up this story). Database work on the service's schema is ACE team (suggested; any team may pick up this story), infrastructure work is SCB IT infrastructure and DevOps work is the DevOps team (R5.3). No person is named (CG-B-TESTDOC-42-2; ASM-B-TESTDOC-42-2).

| Code | Service | Wave | Schema | REST base | Owner of contract and app work |
|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | rwb_source_data | /api/recovery/source-data/v1 | TechX (suggested; any team may pick up this story) |
| P2 | rwb-integration | 1 | rwb_integration | /api/recovery/integration/v1 | TechX (suggested; any team may pick up this story) |
| P3 | rwb-case | 1 | rwb_case | /api/recovery/case/v1 | TechX (suggested; any team may pick up this story) |
| P4 | rwb-access | 1 | rwb_access | /api/recovery/access/v1 | TechX (suggested; any team may pick up this story) |
| P5 | rwb-document | 1 | rwb_document | /api/recovery/document/v1 | TechX (suggested; any team may pick up this story) |
| P6 | rwb-comms | 1 | rwb_comms | /api/recovery/comms/v1 | TechX (suggested; any team may pick up this story) |
| P7 | rwb-decision | 1 | rwb_decision | /api/recovery/decision/v1 | TechX (suggested; any team may pick up this story) |
| P8 | rwb-payment | 2 | rwb_payment | /api/recovery/payment/v1 | TechX (suggested; any team may pick up this story) |
| P9 | rwb-reporting | 1 | rwb_reporting | /api/recovery/reporting/v1 | TechX (suggested; any team may pick up this story) |
| P10 | rwb-agent | 1 | rwb_agent | /api/recovery/agent/v1 | TechX (suggested; any team may pick up this story) |
| S1 | rwb-valuation | 3 | rwb_valuation | /api/recovery/valuation/v1 | TechX (suggested; any team may pick up this story) |
| S2 | rwb-treatment | 2 | rwb_treatment | /api/recovery/treatment/v1 | TechX (suggested; any team may pick up this story) |
| S3 | rwb-guarantee | 3 | rwb_guarantee | /api/recovery/guarantee/v1 | TechX (suggested; any team may pick up this story) |
| S4 | rwb-litigation | 3 | rwb_litigation | /api/recovery/litigation/v1 | TechX (suggested; any team may pick up this story) |
| S5 | rwb-asset | 2 | rwb_asset | /api/recovery/asset/v1 | TechX (suggested; any team may pick up this story) |
| S6 | rwb-debtsale | 3 | rwb_debtsale | /api/recovery/debtsale/v1 | TechX (suggested; any team may pick up this story) |
| S7 | rwb-writeoff | 4 | rwb_writeoff | /api/recovery/writeoff/v1 | TechX (suggested; any team may pick up this story) |
| S8 | rwb-deviation | 2 | rwb_deviation | /api/recovery/deviation/v1 | TechX (suggested; any team may pick up this story) |
| S9 | rwb-partner | 4 | rwb_partner | /api/recovery/partner/v1 | TechX (suggested; any team may pick up this story) |


The worked example of a story that meets the definition of ready is RWB-E1-020, allocate a new case to a queue and an owner. The story of the realignment that shows every item of section 2 at once is the contract story RWB-P3-E1042-CON, parameters, which publishes the parameters contract of rwb-case before any story that reads parameters is pulled (DP-06; CG-B-TESTDOC-42-10; ASM-B-TESTDOC-42-14).

# 2. Definition of ready

A story is pulled onto the board only when every item below is true. The analyst confirms it at refinement, the tech lead and QA agree, and the story status moves to Ready. From D-RCV-60, one item is the published contract: the contract of the owning service is published, versioned and faked before any story that consumes it is pulled (section 2.3).

## 2.1 What the story carries

|  | Item | What is true |
|---|---|---|
| 1 | Story | In the form As a role, I want, so that. The role is a role code from the roles table |
| 2 | Links | Epic, module, L3 process and decision, each from the process architecture and the module list. The service, its code and its service epic RWB-SVC-<code> are named from the Ownership Map v1 |
| 3 | Acceptance criteria | Written in Given, When, Then, each with an ID. The exception paths are covered as well as the main path |
| 4 | Business rules | Each rule has an ID. Routing rules name their rule ID from the rules workbook; table values name their table. A rule that runs in the service names its rule package and the rwb-decision registry entry it comes from (DP-04) |
| 5 | State transitions | Every change of case status or route state, with the event and the condition, matches the case model |
| 6 | Authority | Every role that acts, with its permission letters, matches the permission matrix, and the service enforces it through the rwb-access authorise contract (DP-08) |
| 7 | Data | Every field read or written, with its BR Field ID from the data dictionary. A new field is added to the dictionary first. Every table is in the story's own schema rwb_<short>, or read through the owner's contract or its own v_ace_* views (DP-01, DP-05) |
| 8 | Contract | The trigger, the service, the events published, the idempotency key and any call out of the service. The contract is published before code: OpenAPI 3.1 for REST under /api/recovery/<short>/v1, AsyncAPI 3.0 for topic rwb.<short>.events.v1 with CloudEvents 1.0, and the activity jar for the service's Temporal queue rwb-<short> (Architecture v5 slide 11). The published version is the version the story builds against (CG-B-TESTDOC-42-3; ASM-B-TESTDOC-42-3) |
| 9 | Messages | Every message with its ID and English text. Thai text is requested under DL10. Event names follow rwb.<short>.<Event>.v1 (DP-14) |
| 10 | Screens and states | The screen, its fields and its empty, loading, error and no-access states, or the statement that there is no screen |
| 11 | Guardrails | What the code must not do, the personal data fields touched, and any limit that applies. No personal data in events, workflow inputs or logs |
| 12 | Test cases | At least one test case per acceptance criterion, with its synthetic data; a contract test for every operation, event and activity in item 8; and a boundary test for every table and schema the story touches (ASM-B-TESTDOC-42-4) |
| 13 | Out of scope | What a reader might expect that this story does not do |


## 2.2 What is in place

|  | Item | What is true |
|---|---|---|
| 14 | Epic design | The design for the epic is signed before build starts on the epic. Design runs one epic ahead |
| 15 | INVEST | The story passes the INVEST check and can be finished in two weeks or less |
| 16 | Size | The squad has sized it |
| 17 | Dependencies | Every story, interface and decision it depends on is done, in progress on the board, or behind a flag. A contract dependency of class C never blocks: the consumer builds against the published contract and its fake, and only an H dependency on the same service or on a platform CON story blocks (R5.4, R5.5 DP-11) |
| 18 | Open decisions | No open decision in the decision log blocks it, or the story states the recommended answer it is built on |
| 19 | Test data | The synthetic data it needs exists in DEV, or creating it is part of the story, one data set per schema the story touches |
| 20 | Reference data | The table rows it reads exist with a version and a test case ID, or loading them is part of the story. Parameters and reference data are read through the rwb-case contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON (DP-06, DP-07) |


## 2.3 The contract is published (D-RCV-60)

|  | Item | What is true |
|---|---|---|
| 21 | Contract published | The contract story of the owning service, pattern RWB-<scope>-<legacy>-CON, is Done, and the contract it publishes is in the Service Contract Catalog v1: an OpenAPI 3.1 document, an AsyncAPI 3.0 document and an activity jar, each at a version number, each with its owning service named from the Ownership Map v1 |
| 22 | Fake published | A contract fake of that version is in the contract fake library, and every consumer story on class C depends on the contract and builds against the fake (R5.4; R5.5 DP-11) |
| 23 | Contract version fixed | The story states the contract version it builds against. A later change is published as a new version with BACKWARD compatibility in the JSON Schema registry, and a breaking change is a new contract with its own story (Architecture v5 slide 11; CG-B-TESTDOC-42-5; ASM-B-TESTDOC-42-5) |
| 24 | Ownership stated | Every table, endpoint, event, workflow and job the story touches names its owning service from the Ownership Map v1. No story reads or writes another service's schema, and no story reads another service's tables as a shortcut (DP-01) |
| 25 | Ready to start | The story states Ready to start from R5.7: Day 1 when it has only CON H dependencies, otherwise After the in-lane story IDs it waits for. A contract story is always Day 1 and sits in contract group CG-W<wave> |


# 3. Definition of done

A story is done only when every item below is true. The product owner accepts it against the acceptance criteria and the story status moves to Done. From D-RCV-60 two results decide it together with the items below: the contract tests of the published contract are green and the boundary tests of the service are green (section 3.5; CG-B-TESTDOC-42-4; ASM-B-TESTDOC-42-4).

## 3.1 Built and tested

|  | Item | What is true |
|---|---|---|
| 1 | Merged | The code is merged into main, in the service's own repository. Work that is not finished is behind a feature flag that is off |
| 2 | Pipeline | The nine pipeline gates pass: build and unit tests, lint, secret scan, PDPA lint, container scan, module boundary, integration and contract tests, AI first-pass review and human approval. The contract tests of the published contract and the service boundary test are among them and must be green (Architecture v5 slides 11, 29 and 46) |
| 3 | Criteria | Each acceptance criterion has a test that passes |
| 4 | Rules | Each rule row the story uses passes its rule table test against its test case ID, at the rule package version that the decision record holds (T7) |
| 5 | Exceptions | The exception paths named in the story pass, including a failed decision record write, where the record, the state change and the outbox row are one transaction and nothing moves (R-UNI-39) |
| 6 | Browser | The main and exception paths of any screen pass in the browser test, once the runner is in the pipeline (DL37) |
| 7 | Deployed | The build is deployed to DEV and to SIT, as the service's own api and worker deployments |


## 3.2 Controls

|  | Item | What is true |
|---|---|---|
| 8 | Principle 1 | No threshold, limit, timer, queue, role, template or route is written in code |
| 9 | Decision record | Every decision and every change to a case writes its decision record, in the owning service's schema, in the same transaction as the state change, and the record is checked in a test. The central ledger in rwb-decision collects it within five minutes and the chain check JOB-14 verifies the chain |
| 10 | Access | Every endpoint checks the permission and the scope on the server, through the rwb-access authorise contract and the guard library (DP-08) |
| 11 | Personal data | No personal data in code, tests, fixtures, logs or prompts. Masked fields are masked for roles that may not see them |
| 12 | Boundaries | The story touches one service, or the other service's code owner has approved. The boundary test is green: no read or write of another service's schema, no cross-schema join, view or foreign key, one login per service, and ACE data only through the rwb-source-data contract or the service's own v_ace_* views (DP-01, DP-05, DP-18; CG-B-TESTDOC-42-6; ASM-B-TESTDOC-42-6) |


## 3.3 Records kept current

|  | Item | What is true |
|---|---|---|
| 13 | Data dictionary | A new or changed field is in the data dictionary with its BR Field ID and its owning schema rwb_<short> |
| 14 | Rules workbook | A new or changed rule row is in the rules workbook with its version and test case, and its package version is the one in the rwb-decision registry |
| 15 | Glossary | A new business term is in the business glossary |
| 16 | Standards file | An AI error found in review is added to AGENTS.md |
| 17 | Flags | Any feature flag is in the flag list with its owner and the release in which it is removed |
| 18 | Tracker | The pull request carries the story key, and the story records the merged commits. Tracker impacts are held only in the separate impact and follow-up file of this run, so no tracker record is named here (CG-B-TESTDOC-42-7; ASM-B-TESTDOC-42-7) |


## 3.4 Accepted

|  | Item | What is true |
|---|---|---|
| 19 | Shown | The story is shown to a business tester during the build (DL09) |
| 20 | Accepted | The product owner accepts the story against its acceptance criteria |


## 3.5 Contract and boundary tests green (D-RCV-60)

|  | Item | What is true |
|---|---|---|
| 21 | Contract tests green | Every REST operation, Kafka event and Temporal activity the story provides or consumes passes its contract test against the published contract, on the provider side and on the consumer side (Architecture v5 slides 11 and 46) |
| 22 | Boundary test green | The boundary test passes: the service login has grants on its own schema only, and the build fails on any cross-schema reference (Architecture v5 slide 29) |
| 23 | Event compatibility | The AsyncAPI document and the JSON Schema registry check pass with BACKWARD compatibility, and the CloudEvents envelope carries IDs and facts, never personal data |
| 24 | Replay test | A story that changes workflow or activity code passes the replay test on recorded histories (E2-040), and no workflow code reads the database, the clock, Drools or the network |
| 25 | Decision record test | The decision record test shows the record, the state change and the outbox row committed together and hash-linked, and the central ledger confirms the record in strict mode where the story sits at a point of no return |
| 26 | Version published | The version tested is the version in the Service Contract Catalog v1, and a change of version is recorded in the story before the merge |
| 27 | Fake retired | The consumer stops building against the fake in the integration story of its wave, RWB-ITG-W1 to RWB-ITG-W4, so that no path that reaches production keeps a fake |


# 4. When a story fails a definition

| Case | What happens |
|---|---|
| Not ready when it is due to be pulled | The story stays in refinement. The next ready story in priority order is pulled instead |
| A decision blocks it | The story is built on the recommended answer in the decision log and the assumption is stated in the story |
| Not done at the epic cut | The story moves to the next epic with its flag off. It is not split to claim part of it as done |
| Fails SIT or UAT | Its flag is switched off and the release goes ahead without it. A defect story is raised |
| A defect traced to AI-written code | It is tagged, and the standards file is updated before the fix merges |
| Contract not published when the story is due | The story is not ready. It stays in refinement and the contract story of the owning service is pulled first. A story already in build is not stopped, because a class C dependency never blocks |
| Contract changes under a story in build | The owning service publishes a new version with backward compatibility. The consuming story moves to it in its own pull request, and a breaking change becomes a new contract with its own story |
| Contract test or boundary test red | The story is not done. A red boundary test is never hidden by a flag: the cross-schema reference is removed, or a contract is added to the owning service first |
| Data is needed from another service | A contract request goes to the owning service of the Ownership Map v1. The story never reads the other service's tables |


# 5. Who owns each definition

| Definition | Owner | Changed by |
|---|---|---|
| Definition of ready | Product owner with the analysts, and the owning service team of table 1.1 for the contract items in section 2.3 | Agreement at the weekly delivery review |
| Definition of done | TechX QA lead with the tech leads, with the ACE team for items that touch the common module, and the owning service team for the contract and boundary tests | Agreement at the weekly delivery review, with the ACE team for items that touch the common module |
| Contract publication | The owning service team, from its contract story, pattern RWB-<scope>-<legacy>-CON | Only by publishing a new version in the Service Contract Catalog v1 after a four-eyes review (CG-B-TESTDOC-42-9; ASM-B-TESTDOC-42-9) |
| Boundary test | The owning service team with the DevOps team, on the golden pipeline of wave 0 | Only with platform approval, and the change is recorded in the change register |


## 5.1 The owning team for each kind of work (R5.3)

| Work type | Name | Suggested owner |
|---|---|---|
| CON | Contract | TechX (suggested; any team may pick up this story) |
| APP | App development | TechX (suggested; any team may pick up this story) |
| DB | ACE DB | ACE team (suggested; any team may pick up this story) |
| INF | Infrastructure | SCB IT infrastructure (suggested; any team may pick up this story) |
| OPS | DevOps | DevOps team (suggested; any team may pick up this story) |
| ITG | Integration | TechX (suggested; any team may pick up this story). Harness and NFR stories: QA team (suggested; any team may pick up this story) |


An integration story carries the same ready and done items as every other story, and it alone may carry class I dependencies, the real cross-service behaviour (R5.4; CG-B-TESTDOC-42-8; ASM-B-TESTDOC-42-8).

# 6. What this version changes (D-RCV-60)

| Change | Where | Source state | This version | Basis |
|---|---|---|---|---|
| 1 | Gate table | Ready and Done name section 2 and section 3 only | Ready and Done also name the published contract and the contract and boundary tests | R5.4, R5.5 DP-11 |
| 2 | New table 1.1 | No service owner table | 19 services with wave, schema, REST base and suggested owner, from the Ownership Map v1 | Ownership Map v1 sheet Services |
| 3 | Ready item 8 | The contract is one item of the story | The contract is published before code, versioned and faked, in the Service Contract Catalog v1 | Architecture v5 slide 11 |
| 4 | New section 2.3 | Not present | Items 21 to 25: contract published, fake published, version fixed, ownership stated, Ready to start | R5.4, R5.7, DP-11 |
| 5 | Done item 2 and new section 3.5 | Nine gates, no boundary test item | Contract tests and boundary test named as the deciding results, with replay, compatibility, decision record and fake retirement | Architecture v5 slides 11, 29 and 46 |
| 6 | Done item 9 and 12 | Decision log; one module | Decision record in the owning schema in one transaction; one service and one schema, with a green boundary test | R-UNI-39, DP-01, DP-03 |
| 7 | Done item 18 | The row names a tracker | Tracker impacts are held only in the separate impact and follow-up file | U6 |
| 8 | Section 4 and section 5 | No row for a contract or a boundary failure, no owner for contract publication | Four rows added to section 4, and two definitions with their owners added to section 5 | R5.4, R5.3 |

