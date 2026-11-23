# Recovery Workbench Microservice Story Template and Rules v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

## R1. User decisions (fixed for this run)

| ID | Decision |
|---|---|
| U1 | One epic per service (19), plus 7 platform and 5 integration epics. Every story also carries its business epic (EP01–EP08) as a tag. |
| U2 | Work already built or in build in Epic 1 is not changed unless absolutely needed. It is kept word for word, and the microservice change goes into separate delta stories. |
| U3 | Separate linked stories per team type. The owner is a suggestion only ("any team may pick up this story"). No names of people anywhere. |
| U4 | Every story uses the full 19-section template in §R7. |
| U5 | New versions sit next to the old ones in the same folders. Run material goes to folder 22, and gaps and assumptions to folder 23. |
| U6 | No issue-tracker access or updates. Tracker impacts go to one separate file only. |
| U7 | Dates are tentative and unchanged; the programme finishes within 8 months. A date is never raised as a gap. |
| U8 | No human verification stops in this run; maximum parallel agents. The verification loop comes later. |
| U9 | The BRDs and PRDs are produced with the existing BRDs and the AI-SDLC (HVE Core) agents. |
| U10 | A large technical Excalidraw diagram, by epic and story, for developers and architects. |

## R3. Source precedence (R-PREC) and default rulings

When two sources disagree, the higher one in this list wins. The loser is recorded as a gap row (type Conflict) and an assumption row.

1. Arch v5 catalogue slides (services, resources, call types: slides 13–20 and 41–44).
2. Recovery Temporal and Drools Detailed Design v1.
3. Arch v5 narrative slides.
4. Decision Log (latest version).
5. Architecture Decision Records (latest version).
6. Technical Specifications by Module (latest version).
7. Functional Specifications by Module (latest version).
8. Physical Schema and Logical Data Model (latest version).
9. The story masters.

**Default rulings.** Each ruling is also an assumption in the Assumptions Register.

| Item | Owner |
|---|---|
| Parameters and reference data (E1-042, E1-043) | P3 rwb-case |
| Case list API | P3 rwb-case |
| Rule package registry | P7 rwb-decision |
| Interaction ledger | P1 rwb-source-data |
| Feature flags | Platform library |

## R4. Services and naming

The service table has 19 rows; the source is Arch v5. Each service has:
- schema `rwb_<short with _>`
- login per service
- REST base `/api/recovery/<short>/v1`
- topic `rwb.<short>.events.v1`, with retry and `.dlt` topics
- event names `rwb.<short>.<Event>.v1`
- Temporal task queue `rwb-<short>`
- Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>`
- epic `RWB-SVC-<code>`

**Platform (wave 0) and integration:**

| Code | Service | Wave | Code | Service | Wave |
|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | S1 | rwb-valuation | 3 |
| P2 | rwb-integration | 1 | S2 | rwb-treatment | 2 |
| P3 | rwb-case | 1 | S3 | rwb-guarantee | 3 |
| P4 | rwb-access | 1 | S4 | rwb-litigation | 3 |
| P5 | rwb-document | 1 | S5 | rwb-asset | 2 |
| P6 | rwb-comms | 1 | S6 | rwb-debtsale | 3 |
| P7 | rwb-decision | 1 | S7 | rwb-writeoff | 4 |
| P8 | rwb-payment | 2 | S8 | rwb-deviation | 2 |
| P9 | rwb-reporting | 1 | S9 | rwb-partner | 4 |
| P10 | rwb-agent | 1 | | | |

Shared topic: `rwb.decision-record.v1`. Temporal namespace: `rwb-recovery`. Edge: gateway-bff (Redis session store) and the partner gateway in the DMZ.

## R5. Target structure

### R5.1 Epics

- **Platform:**
  - RWB-PLT-TPL: service template and repositories
  - RWB-PLT-LIB: shared libraries
  - RWB-PLT-WF: Temporal workflow platform
  - RWB-PLT-DB: ACE DB schemas and logins
  - RWB-PLT-EVT: Kafka event platform
  - RWB-PLT-EDGE: edge and gateway
  - RWB-PLT-OBS: observability
- **Service:** RWB-SVC-P1 … RWB-SVC-S9.
- **Integration:**
  - RWB-ITG-W1 … RWB-ITG-W4: one per wave
  - RWB-ITG-NFR: non-functional

### R5.2 Story IDs

Pattern: `RWB-<scope>-<legacy compact>-<work type>[-n]`.
- Scope: P1–P10, S1–S9, PLT or ITG.
- Legacy compact: E1018, TE001, AD003, DM002, ACE001, NF06, N001 (new), or W1J01 (new integration).
- `-2` is the delta copy of a preserved story that keeps its base ID.

Example: `RWB-P3-E1018-APP`.

### R5.3 Work types and suggested owners

| Work type | Name | Suggested owner (fixed phrase) |
|---|---|---|
| CON | Contract | TechX (suggested; any team may pick up this story) |
| APP | App development | TechX (suggested; any team may pick up this story) |
| DB | ACE DB | ACE team (suggested; any team may pick up this story) |
| INF | Infrastructure | SCB IT infrastructure (suggested; any team may pick up this story) |
| OPS | DevOps | DevOps team (suggested; any team may pick up this story) |
| ITG | Integration | TechX (suggested; any team may pick up this story). Harness and NFR stories: QA team (suggested; any team may pick up this story) |

### R5.4 Dependency classes

| Class | Meaning | Blocks the build? |
|---|---|---|
| H | Same service, or a platform CON story | Only H on a non-CON story (same lane) |
| C | Another service's CON story. Build against the published contract and its fake. | No |
| I | The real cross-service behaviour. Allowed only on ITG stories. | ITG only |
| X | External or team-type work (DB, INF or OPS story of the same legacy key, outside systems) | No; tracked |

### R5.5 Decoupling patterns (DP table)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-12 | One workflow per case | CaseWorkflow parent with a child workflow per stage | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

### R5.6 Wave map (W-MAP)

| Business epic | Wave |
|---|---|
| EP01 | 1 |
| EP02, EP03 | 2 |
| EP04, EP05 | 3 |
| EP06, EP07, EP08 | 4 |
| Platform and NF | 0 |

A story whose W-MAP wave is earlier than its service's Arch v5 wave keeps the W-MAP wave. One conflict gap is raised per service and business epic.

### R5.7 Lanes and Day-1 rules

1. A CON story has no build dependency. It is always "Day 1" and sits in contract group `CG-W<wave>`.
2. An APP story builds against CON stories and their fakes. C dependencies never block.
3. H dependencies point only to the same service, or to a platform CON story.
4. I dependencies sit only on ITG stories.
5. A lane is a connected group of non-CON stories linked by H. Its depth is at most 4. A deeper chain is cut: the later story builds against the earlier story's CON (created if missing), and an assumption is recorded.
6. Every team type has Day-1 work. The new platform stories N001–N012 and the integration harness W1J01 make sure of this.
7. Every service has at least one CON story. A service with none gets a "service contract baseline" story (N013 onwards).
8. Ready to start = "Day 1" if the story has only CON H dependencies; otherwise "After <the in-lane story IDs it waits for>".

## R6. Epic 1 preservation

| Group | Stories | Rule |
|---|---|---|
| Built or in build, preserved | RWB-TE-001, TE-002, TE-003, E1-042, E1-043, E1-044 | The as-built story keeps its base ID with `preserved=true`. Legacy sections 1–11, 14–16, 18 and 19 are copied word for word. Sections 12 and 13 sit under "As built (monolith)". The microservice change is a separate delta story (`-2` copy, or CON/OPS stories). No change to built code until a delta story is picked up. |
| Must change | RWB-E1-001 | In build: the single recovery schema (92 tables, 14 data products, dictionary). The built migration is kept. The split into rwb_* schemas is new work (RWB-PLT-NF06-DB and the per-service DB stories). It is recorded in the Change Register. |
| Retired | RWB-E1-014 (decision log copy to the data lake: no data lake in Arch v5); RWB-TE-007 (Quartz scheduler: replaced by Temporal Schedules in RWB-PLT-E1071) | No new story. Dependencies on E1-014 are dropped. Dependencies on TE-007 point to RWB-PLT-E1071-CON. |
| Already cancelled | E1-003, 004, 005, 006, 009, 010, 012, 029, 048, 051; TE-005 | No new story. |
| No impact | E1-024, 025, 026, 033, 034, 038, 040, 041, 045, 053, 060, 061, 068; TE-010, TE-012 | Moved to their epic with content unchanged. |

## R7. Story template

### R7.1 Metadata table

The story's first line is `# <Story key> <Title>`. Next comes `| Item | Value |` with these rows, in this order, and none may be removed:

1. Story key
2. Work type
3. Suggested owner
4. Service
5. Service epic
6. Wave
7. Business epic
8. Release
9. Legacy key
10. Legacy disposition
11. Build status
12. Patterns applied
13. Parallel lane
14. Ready to start
15. Depends on (build)
16. Contract dependencies
17. Integration dependencies
18. External dependencies
19. PRD reference
20. Status

### R7.2 The 19 sections

Use `### n. Name`, in this order:

| # | Section | # | Section |
|---|---|---|---|
| 1 | Story | 11 | Data |
| 2 | Business rationale | 12 | Contract |
| 3 | Preconditions | 13 | Solution plan |
| 4 | Flow | 14 | Validation and messages |
| 5 | Exception paths | 15 | Screens and states |
| 6 | INVEST check | 16 | Test cases |
| 7 | Acceptance criteria | 17 | Guardrails |
| 8 | Business rules | 18 | Traceability |
| 9 | State transitions | 19 | Out of scope |
| 10 | Authority | | |

**Section rules:**
- **s7 Acceptance criteria.** Each `Scenario: ACn` line ends with an origin tag, either "(legacy RWB-…-nnn ACn)" or "(new, D-RCV-60)".
- **s12 Contract.** Tables 12.1–12.9, written "None" where empty:
  - 12.1 REST operations provided
  - 12.2 REST operations consumed
  - 12.3 Events published
  - 12.4 Events consumed
  - 12.5 Workflows and activities
  - 12.6 Schedules
  - 12.7 Tables owned
  - 12.8 Contract fakes
  - 12.9 Call-type summary (REST, Kafka, Temporal, File)
- **s16 Test cases.** Table columns: TC ID, Covers, Level (Unit, Component, Contract, Integration, End to end, NFR), Data. ITG copies of a TC end in `-ITG`.
- **s17 Guardrails.** No business values in code, no PII in events, workflow inputs or logs, ACE data only through the owner's contract or `v_ace_*` views.

### R7.3 Fill order for thin stories (Epics 3 to 8)

Take each value from the first source in this list that has it:
1. The legacy story
2. The FSD module file
3. The TSD module file
4. The BRD (Program, then the epic BRD)
5. Business Rules and Routing Logic
6. The Arch v5 extract

If no source has the value, write the placeholder in §R9 and add a gap row and an assumption row. Never invent business values.

## R8. Outputs

### R8.1 Header

Every new document starts with these two lines:

```
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd
```

Every new document also has a change-log row naming D-RCV-60 and the tool line "T3 Code / OpenCode / DeepSeek v4.1 Flash".

### R8.2 Versioning

- The next version is the highest `v<n>` of the family plus 1, in the same folder.
- An existing file is never edited.
- A folder family is copied to the next-version folder, and only the files that change get a new version inside it.

### R8.3 Folders 22 and 23

**Folder 22** holds the run material:
- Text Extracts v1
- Ownership Map v1
- Template and Rules v1
- Change Register v1
- Tracker v1 and v2
- Issue-tracker impact and follow-up v1
- the architecture diagrams
- Run Summary v1
- `compat/`, `checks/` and `aisdlc/`

**Folder 23** holds the Gap Register and Assumptions Register (xlsx and md).

### R8.4 Architecture outputs

**ADRs.** Add ADR-013 to ADR-023, or the IDs allocated in `ids.json`. Each one supersedes or amends the decision named after the dash:

| ADR | Decision |
|---|---|
| 013 | 19 services inside ACE — supersedes the single-service decision ADR-002 |
| 014 | Schema and login per service in ACE PostgreSQL |
| 015 | Kafka with outbox, inbox and CloudEvents |
| 016 | Reusable Temporal layer; Schedules replace Quartz |
| 017 | Embedded Drools per service; rule registry in rwb-decision — amends D-RCV-36 T1 and T2 |
| 018 | No data lake; rwb-reporting read model from events |
| 019 | Edge: gateway-bff and partner gateway |
| 020 | Contract-first REST, one hop, 2 s timeout |
| 021 | Per-service Flyway and migration ownership |
| 022 | Local decision record plus central ledger |
| 023 | Observability per service |

**Decision Log.** Add D-RCV-60 (adopt Arch v5 and realign the documents and stories), plus:

| Row | Decision |
|---|---|
| DL44 | Adopt Arch v5 |
| DL45 | Service epics plus business-epic tags |
| DL46 | Soft ownership by team type |
| DL47 | Epic 1 preservation rule |
| DL48 | Dates unchanged and tentative |
| DL49 | Gap and assumption registers |

**Other architecture outputs:**
- Service Catalog v1
- Service Template Specification v1
- API Specification split into 19 files plus gateway-bff and an index
- Event and Messaging next version, plus the Kafka Topic and Event Catalog v1
- Batch and Scheduling next version, plus the Temporal Workflow and Activity Catalog v1
- Physical Schema folder with 19 `rwb_<name>.sql` files, plus `recovery_views.sql` and a README
- LDM and ERD next versions
- Service Contract Catalog v1

### R8.5 Requirements outputs

- **BRDs (BRD Builder):**
  - Program, Epic 1 and Epic 2: next versions, with BR IDs stable plus a "Delivery model" section
  - Epics 3 to 8: new v1
- **PRDs (PRD Builder):** 20 files: one per service plus Platform, in `03 Requirements and specifications/PRD/`.

### R8.6 Document families

The 49 families, and what changes in each, are listed in `make_wps.py` `DOCS` (Task 13).

### R8.7 Story outputs

- **Story files:** `04 User stories/Recovery Workbench Service Story Files v1/<epic> <epic name>/RWB <scope> <legacy> <WT> <title><suffix> v1.md`
- **New versions of the 7 masters**
- **Service Story Catalog v1:** one per story set, with:
  - an epic overview per epic folder
  - the Day-1 Work Allocation v1
  - the Service Epics v1 file
- **Next versions of these files:**
  - RTM
  - Test Cases
  - Regression Suite
  - Build Sequence
  - Story Build Order
  - Dependency Map
  - Story Defects
  - Worked Example
  - AC Glossary
  - How To Read The Acceptance Criteria
  - Build Notes for E1, E2 and the Technical Enablers

### R8.8 Diagram styles

**Work types:**

| Type | Colour |
|---|---|
| CON | blue `#1971c2` |
| APP | green `#2f9e44` |
| DB | brown `#8d5524` |
| INF | grey `#868e96` |
| OPS | purple `#7048e8` |
| ITG | red `#e03131` |

**Calls:**

| Call | Style |
|---|---|
| Build dependency (H) | thin black |
| REST | solid blue |
| Kafka | dashed orange |
| Temporal | solid purple |
| File | dotted grey |
| Integration dependency (I) | dashed red |

**Layout:** wave bands (0 platform, 1–4, then integration) → epic frames → lane columns → story boxes.

## R9. Gaps and assumptions

**Placeholder.** Where a value is missing, write: `Not specified in the source documents (CG-<WP>-<n>; ASM-<WP>-<n>)`.

**Candidate rows.** Each WP writes one JSON object per line to `_work/msr/gaps/<WP>.jsonl` and `_work/msr/assumptions/<WP>.jsonl`.
- **Gap row keys:** id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp.
- **Assumption row keys:** id, text, why, read, gap, applied_in, confidence, confirm, impact, wp.

**Numbering.** Only step D1 numbers the rows, as GAP-nnnn and ASM-nnnn, and rewrites every citation.

**Gap types:**
- Missing
- Conflict
- Ambiguous
- Outdated
- ID collision

**Severity:**
- P1: blocks a wave start.
- P2: blocks a story's Done.
- P3: documentation only.

**Confidence:** High, Medium or Low.
