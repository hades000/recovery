# Recovery Workbench — intake gap report

**Run:** intake-20261104
**Inputs:** `requirement/legacy/` (411 entries), `docs/brds/`, `docs/prds/`, `.github/contexts/`
**Outputs:** `requirement/BRD_RecoveryWorkbench.md`, `requirement/RecoveryWorkbench_Requirements.md`,
`requirement/Traceability_Matrix.md`
**Status:** **CONDITIONAL PASS** — the Epic 1 intake can proceed to specification; the High gaps below
must be closed or explicitly accepted before the specification gate.

## 1. What was consolidated

| Source | What was used | Result |
|---|---|---|
| Lean BRD Epic 1 v2 | Problem, outcome, scope, rules, process ownership, constraints, dependencies, success measures | BRD-RWB-001..020 |
| Lean BRD Epic 2 v2 | Epic 2 scope and outcomes | EPIC-002 |
| Business Requirements Program v3 | 231 requirements across P1–P10 and S1–S9 | FR-RWB-001..020 |
| Business Requirements Epic 1 v3 | 67 requirements, 57 Must, 77 programme requirements | Epic 1 scope |
| Business Requirements Epic 2 v2 | Epic 2 requirements | EPIC-002 |
| Non-Functional Specification v2 | 78 NFRs | NFR-RWB-001..010 |
| Business Rules and Routing Logic v4 | 448 rules in 10 route sets | BR-RWB-001..016, rule families |
| Case and Workflow Model v5 | Stages, tasks, sentries, state machine | FR-RWB-004..010 |
| Users, Roles and Permissions v3 | 54 roles, permission matrix | Actors and personas |
| Conceptual/Logical Data Model | 14 data products, 108 entities | Data requirements |
| API Specification v2 | REST/OpenAPI 3.1 paths | Integration points |
| Interface/Event designs | Adapter pattern, events, outbox | FR-RWB-003 |
| Target Architecture v4 / ADRs | Architecture constraints | Context and constraints |
| Engineering Practices v4 | Stack, branching, tests, flags | AGENTS.md and context |
| Test Strategy v2 | Levels, environments, gates | testing-standards.md |
| PDPA Design / Controls Catalog | Compliance, 42 controls | BR-RWB-009..015 |
| Release Plan / Build Sequence | 8 releases, 6 gates, 115 items | EPIC-001/EPIC-002 |

## 2. Gap summary

| Severity | Count | Meaning |
|---|---:|---|
| Critical | 0 | No gap blocks the intake. |
| High | 6 | Must be closed or explicitly accepted before the Epic 1 specification gate. |
| Medium | 8 | Should be closed before planning; may be carried with a recorded decision. |
| Low | 6 | Record and monitor; no immediate impact on Epic 1. |

## 3. High gaps

### GAP-001 — Epic 1 story files are older than the consolidated stories

| Field | Value |
|---|---|
| Evidence | `Recovery Workbench User Stories Epic 1 v7.md` (consolidated) vs `Recovery Workbench User Stories Epic 1 Story Files v5.zip` and the extracted folder with 69 of 79 files. |
| Impact | A per-story Technical Specifier run may use an older story than the consolidated v7. The story-level acceptance criteria may not match the consolidated file. |
| Affected | All Epic 1 story-level runs; RWB-E1-001..068. |
| Owner | Business analyst |
| Action | Reissue the story files at the same version as the consolidated v7, or confirm that v5 is canonical and the consolidated v7 is the narrative summary. Record the decision in the increment card. |
| Status | Open |

### GAP-002 — Epic 2 story files are older than the consolidated stories

| Field | Value |
|---|---|
| Evidence | `Recovery Workbench User Stories Epic 2 v5.md` vs `Recovery Workbench User Stories Epic 2 Story Files v4.zip`. |
| Impact | Same as GAP-001 for Epic 2. |
| Affected | EPIC-002 story-level runs. |
| Owner | Business analyst |
| Action | Reissue at a consistent version before EPIC-002 specification. |
| Status | Open |

### GAP-003 — Filename versions and internal document versions disagree

| Field | Value |
|---|---|
| Evidence | `Recovery Workbench Project Overview v4.docx` says version 3; `Recovery Workbench Target Architecture v4.docx` says version 2; `Recovery Workbench Engineering Practices v4.docx` says version 3; `Recovery Workbench Non-Functional Specification v2.docx` says version 1. |
| Impact | An agent may cite the wrong version; the document control sheet may not match the file name. |
| Affected | All cited documents; the source register. |
| Owner | Document owner |
| Action | Treat the filename as the set version and the internal version as the document version; record both in `DOCUMENT_MAP.md`. Reconcile at the next document issue. |
| Status | Mitigated in the map; open for the source set |

### GAP-004 — No live Figma file or design link

| Field | Value |
|---|---|
| Evidence | No `.fig` file, Figma URL or design link in the set. The design evidence is the screen inventory, screen specifications, design system and prototype. |
| Impact | The Technical Specifier cannot use the live Figma path. It must use `DESIGN_EVIDENCE_STATUS: AVAILABLE` with `SOURCE: LOCAL_ARTIFACTS`. A UI story with no local evidence would be blocked. |
| Affected | All UI stories; the Functional Automation Test. |
| Owner | Front-end lead |
| Action | Confirm the screen specifications and prototype are the approved design evidence for Epic 1 and 2; add screenshots to `output/<RUN_ID>/specify/figma/png/screens/` where a screen is not covered. |
| Status | Accepted for Epic 1 (local evidence); open for later epics |

### GAP-005 — No ACE source code in this workspace

| Field | Value |
|---|---|
| Evidence | The workspace contains the document set and the toolkit, not the ACE repository. |
| Impact | Context Builder documents intended behaviour from documents; it cannot verify implemented behaviour. The Implementation Builder, API Tester and Functional Automation Test need the ACE repository. |
| Affected | Build, API test, functional test, code review. |
| Owner | Forward Deployed Engineer |
| Action | Clone the ACE repository next to this repo and point the implementation stage at it; do not fabricate code evidence in this workspace. |
| Status | Open; blocks Build, not Specify/Plan |

### GAP-006 — Named approvers are not in the document set

| Field | Value |
|---|---|
| Evidence | The increment card and tailoring record require named human approvers; the document set names roles, not people. |
| Impact | The human gates cannot be signed; the increment card carries `TBC`. |
| Affected | EPIC-001, EPIC-002, all gates. |
| Owner | Product Owner / FDA |
| Action | Name the Product Owner, FDA, FDE, QA lead, Security and business lead for each increment. |
| Status | Open; blocks the approval gate, not the intake |

## 4. Medium gaps

| ID | Gap | Impact | Owner | Action | Status |
|---|---|---|---|---|---|
| GAP-007 | Thai labels and messages are proposed, not approved (DL10). | UI and notice stories may ship with English labels. | Business lead | Approve Thai or confirm English first. | Open |
| GAP-008 | Availability, RPO and RTO targets are open (DL11). | NFR tests cannot be baselined. | IT lead with Operational Risk | Confirm the ACE values. | Open |
| GAP-009 | Retention periods for documents, decision log and ledger are open (DL26). | Retention classes have no periods. | Compliance | Confirm periods per record class. | Open |
| GAP-010 | Same-day data interfaces are not named (DL06). | The end-of-day default may not meet a decision that needs today's position. | Solution architect | Name the interfaces and the trigger. | Open |
| GAP-011 | Jira project and issue keys are not assigned. | The Jira column in the traceability matrix stays blank. | Product owner | Create the Jira project and map RWB keys. | Open |
| GAP-012 | Partner external access is not live (DL03). | Partner portal tests are limited to the bank network until the gateway is live. | Architecture team | Confirm the gateway date; plan E5 tests. | Open |
| GAP-013 | Model endpoint is not approved (DL33). | Agents stay in shadow with the rule fallback. | CTO with Enterprise AI | Approve the endpoint or keep shadow for E1. | Open |
| GAP-014 | The document set contains duplicate formats and versions (md/xlsx/zip/html). | An agent may read the wrong copy. | Document owner | The map marks canonical/data/reference/superseded; use the map. | Mitigated |

## 5. Low gaps

| ID | Gap | Impact | Action |
|---|---|---|---|
| GAP-015 | The 26 MB Project Hub is not converted. | An agent cannot search it directly. | Indexed as reference; extract specific data only if needed. |
| GAP-016 | Some DOCX/PPTX images are not extracted. | Diagrams in those files are not in the Markdown. | Originals retained; add images to the spec when a story needs them. |
| GAP-017 | XLSX formulas without cached values are blank. | A calculated cell may be missing. | Check the source workbook; do not infer the formula. |
| GAP-018 | HTML conversion loses styling and some inline metric layout. | The HTML is a reference, not the canonical data. | Use the xlsx/md canonical for data. |
| GAP-019 | The physical schema and API spec are large. | An agent may not read them fully in one pass. | Use the module TSD/FSD and the specific table/endpoint for the story. |
| GAP-020 | The document index lists 123 documents; the map has 411 entries because it includes zip entries and story files. | A reader may think the counts disagree. | The map explains the difference: 256 source files + 155 archive entries. |

## 6. Source conflicts and how they were resolved

| Conflict | Sources | Resolution |
|---|---|---|
| Project Overview file v4 vs document version 3 | File name; document control table | File name is the set version; document version is recorded in the map. The content is treated as v3. |
| Target Architecture file v4 vs document version 2 | File name; document control table | Same rule. |
| Engineering Practices file v4 vs document version 3 | File name; document control table | Same rule. |
| Non-Functional Specification file v2 vs document version 1 | File name; document control table | Same rule. |
| Epic 1 story count: 67 requirements vs 68 story files vs 79 zip entries | BRD Epic 1; story files; zip | 67 requirements is the requirement count; 68 story files includes the enablers; 79 zip entries includes the read-me and duplicates. The map records the counts. |
| Epic 1 consolidated v7 vs story files v5 | Story files; consolidated file | Consolidated v7 is the canonical narrative until the story files are reissued (GAP-001). |
| Epic 2 consolidated v5 vs story files v4 | Story files; consolidated file | Consolidated v5 is canonical until reissued (GAP-002). |
| TSD zip vs extracted folder | Zip; folder | The folder is the extracted canonical copy; the zip is the portable archive. The map marks both. |
| FSD zip only | Zip | The zip is the canonical archive; the FSD modules are copied to `docs/prds/`. |
| Business Rules HTML vs xlsx | HTML; xlsx | The xlsx is canonical data; the HTML is a rendered reference. |
| Case and Workflow Model HTML vs xlsx | HTML; xlsx | The xlsx is canonical data; the HTML is a rendered reference. |
| Detailed Process Flows HTML vs xlsx | HTML; xlsx | The xlsx is canonical data; the HTML is a rendered reference. |
| Screen Specifications md vs html | md; html | The md is canonical; the html is a rendered reference. |
| API Specification yaml vs html | yaml; html | The yaml is canonical; the html is a rendered reference. |
| ERD html vs pdf | html; pdf | The html is canonical; the pdf is a reference. |

## 7. Canonical source decisions

1. Markdown is preferred for narrative; xlsx is preferred for data; docx is preferred for narrative
   where no Markdown exists; pptx is a reference; html is a reference where a canonical md/xlsx/yaml
   exists; pdf is a reference.
2. The zip is the portable archive; the extracted folder is the working copy. For Epic 1 story files,
   the zip has 79 entries and the extracted folder has 69; the zip is canonical until the folder is
   completed.
3. The highest version in the filename is the set version. The internal document version is recorded
   in the map.
4. `requirement/legacy/` is the canonical corpus. `docs/` copies are working copies that point back to
   the legacy source.
5. The 26 MB Project Hub is reference only; it is not an intake source.

## 8. Impact on traceability

| Impact | Detail |
|---|---|
| Source IDs preserved | `REQ-*`, `RWB-E*`, `RWB-TE-*`, `BR-*`, `MSG-*`, `DF-*`, `TC-*`, `DL*`, `R-*`, `DEP-*`, `CTL-*` are preserved. |
| New IDs | `BRD-RWB-*`, `FR-RWB-*`, `NFR-RWB-*`, `US-RWB-E1-*`, `AC-RWB-*`, `BR-RWB-*`, `INT-RWB-*`, `ERR-RWB-*`. |
| Crosswalk | `requirement/Traceability_Matrix.md` has a source-ID crosswalk and an Epic 1 story crosswalk. |
| Gaps | The matrix marks `GAP-001` and `GAP-002` in the `Status` column for the affected story rows. |
| Jira | The Jira column is blank until the project and keys are assigned (GAP-011). |

## 9. Recommendation

**Proceed to the Technical Specifier for Epic 1** with the following conditions:

1. Use the consolidated Epic 1 v7 as the narrative source and the per-story file for the story-level
   detail; record the version used in the spec header.
2. Use `SOURCE: LOCAL_ARTIFACTS` for design evidence; do not claim a Figma source.
3. Stop at the specification gate if a `CLAR-*` item depends on GAP-001, GAP-005, GAP-006 or GAP-010.
4. Close GAP-006 (named approvers) before the specification approval.
5. Close GAP-005 (ACE repository) before the planning gate; the plan can be written, but no code.

`NEXT_STEP: Human review of the intake outputs, then start the Technical Specifier on RWB-E1-020 as
the pilot story.`
