# Context Builder run log

**Run:** CONTEXT-20261104
**Agent:** Context Builder (`.github/agents/context-builder.agent.md`)
**Started:** 2026-11-04
**Status:** READY, with the gaps listed in section 3.
**Inputs:** `requirement/legacy/` (411 entries), `docs/`, the twelve source folders.
**Outputs:** `.github/contexts/project-context.md`, `domain-context.md`, `frontend-context.md`,
`backend-context.md`, `testing-standards.md`, `requirement/Context_RecoveryWorkbench.md`.

## 1. How the run worked

The Context Builder asks for missing facts only when the sources do not answer them. The project set
answers most of the questions, so the run was a **verification exercise**, not an interview. Each
question below records:

- the question the agent would ask;
- the answer used;
- the source that establishes it;
- how the answer was verified;
- what was done when the source was silent.

## 2. Questions and answers

### Q1. Is this an existing/legacy project or a greenfield project?

**Answer:** Greenfield for the Workbench product, inside the existing ACE platform. The Workbench is
a new module of ACE, not a new standalone application.

**Sources:** `docs/architecture/decisions/adr-001-build-the-workbench-as-a-module-of-ace.md`;
`requirement/legacy/05-technical-architecture/recovery-workbench-target-architecture-v4-docx.md` §1–2;
`docs/discovery/project-overview.md` §1.

**Verification:** Three independent sources agree. ADR-001 is Accepted. The target architecture says
"one service, one repository, one front end" and "the recovery module of ACE". No source describes a
separate application.

**Disposition:** Recorded as `CTX-BUSINESS-001` and `CTX-CONSTRAINT-001`. The increment path is
Greenfield for the module, with brownfield ACE integration constraints.

### Q2. What is the planned technology stack?

**Answer:**

- Back end: Spring Boot (Java) with Spring JPA, Spring Batch, Spring Security with method security
  and OAuth, Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query; TypeScript types generated from the back end.
- Database: PostgreSQL; Flyway or Liquibase migrations.
- Identity and logs: Entra ID, the bank IAM, PII Kafka, audit log and SOC log.
- Hosting: the ACE namespace on the shared ACE AKS clusters.

**Sources:** `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md`
§2.3; `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
§3.1; `docs/architecture/decisions/adr-002-structure-ace-as-a-modular-monolith.md`.

**Verification:** The three sources agree. The TSDs repeat the same stack. No source names a different
framework, database or identity provider.

**Disposition:** Recorded in `backend-context.md` §1 and `frontend-context.md` §1.

### Q3. What are the primary sources, and is there a Confluence link?

**Answer:** No Confluence link. The primary sources are the twelve folders in this SharePoint set,
converted to Markdown under `requirement/legacy/`. The document index is the register.

**Sources:** `requirement/legacy/12-project-communication/recovery-workbench-document-index-v11.md`;
`requirement/legacy/_conversion-report.md`; `requirement/legacy/DOCUMENT_MAP.md`.

**Verification:** 256 source files and 156 archive entries were processed; 0 failures. The document
index lists 123 documents; the map adds the story files, TSD folder and archive entries that the
index does not list.

**Disposition:** Source register in `project-context.md` §17. No Confluence dependency.

### Q4. Who are the users and stakeholders?

**Answer:** 54 roles: 37 bank users, 7 partner users, 4 customer parties and 6 non-human actors. The
operating model has product heads, shared operations, centre of excellence and platform, plus control
functions and committees. 1,234 named users; about 410 online in the busiest hour.

**Sources:** `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v3-xlsx.md`;
`docs/discovery/target-operating-model.md` slide 7;
`docs/prds/non-functional-specification.md` §2.

**Verification:** The role count (54) matches the workbook summary. The group count (4) matches the
TOM. The user count (1,234) matches the NFR. No contradiction.

**Disposition:** `CTX-STAKEHOLDER-001` to `CTX-STAKEHOLDER-007`.

### Q5. What compliance obligations apply?

**Answer:** Thai PDPA B.E. 2562; BOT debt collection conduct; 42 controls; audit findings; records
retention. The lawful bases are proposed and Compliance confirms them under DL26.

**Sources:** `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md`;
`.../recovery-workbench-controls-catalog-v2-xlsx.md`;
`.../recovery-workbench-regulatory-requirements-map-v2-xlsx.md`.

**Verification:** The controls catalogue has 42 rows, each with an owner, evidence and test. The PDPA
design names the lawful basis and the open decision. The regulatory map links obligations to controls.
No source claims the bases are approved.

**Disposition:** `CTX-COMPLIANCE-001` to `CTX-COMPLIANCE-005`. `DL26` is recorded as an open gap.

### Q6. What is the architecture?

**Answer:** Modular monolith on ACE with common, collection and recovery modules; programmatic
workflow in CMMN 1.1 terms with no workflow engine; rules as versioned data evaluated by a decision
table component; decision log; document hub; agent runtime. Nine ADRs are accepted or proposed.

**Sources:** `docs/architecture/decisions/` (ADR-001 to ADR-009);
`requirement/legacy/05-technical-architecture/recovery-workbench-target-architecture-v4-docx.md`;
`requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md` §2–3.

**Verification:** The ADR list has nine entries; ADR-001, 002, 003, 004, 005, 007 and 008 are Accepted;
ADR-006 and ADR-009 are Proposed. The target architecture repeats the same decisions. No contradiction.

**Disposition:** `CTX-BUSINESS-013`, `CTX-CONSTRAINT-001` to `CTX-CONSTRAINT-004`, and
`backend-context.md` §2.

### Q7. What is the data architecture?

**Answer:** 14 data products, 108 entities across 17 subject areas, a logical data model with every
field, a PostgreSQL physical schema, COLLINS daily batch, file loads, a decision log hash chain and an
interaction ledger.

**Sources:** `requirement/legacy/06-data/recovery-workbench-conceptual-data-model-v5-xlsx.md`;
`.../recovery-workbench-logical-data-model-and-data-dictionary-v6-xlsx.md`;
`.../recovery-workbench-physical-schema-v4.sql`.

**Verification:** The data products sheet lists DP01–DP14. The entities sheet says 108 entities and 17
subject areas. The logical model is 273 KB of field tables. The physical schema is 0.83 MB of SQL.
No count contradicts another source.

**Disposition:** `CTX-DATA-001` to `CTX-DATA-007`, `backend-context.md` §4.

### Q8. What is the testing approach?

**Answer:** Unit (80% line coverage on new code), rule table, integration, API contract, system,
regression, non-functional, accessibility and UAT. DEV is synthetic; SIT and UAT are masked. SIT exit
requires every test case to pass with no open severity 1 or 2; UAT exit requires business sign-off.

**Sources:** `requirement/legacy/09-testing-and-quality/recovery-workbench-test-strategy-v2-docx.md`;
`.../recovery-workbench-definition-of-ready-and-done-v3-docx.md`;
`.../recovery-workbench-test-data-plan-v2-docx.md`.

**Verification:** The levels table has nine levels. The environments table has three (DEV, SIT, UAT).
The 80% coverage target is repeated in the toolkit and the test strategy. No contradiction.

**Disposition:** `testing-standards.md`.

### Q9. What is the delivery model?

**Answer:** Kanban with items pulled in build-sequence order; trunk-based development; feature flags;
monthly releases; six gates; two-week sponsor review windows. E1 and E2 are confirmed; E3–E8 are
proposed.

**Sources:** `requirement/legacy/11-delivery-and-operations/recovery-workbench-release-plan-v3-xlsx.md`;
`.../recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md`;
`requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md`.

**Verification:** The release plan lists eight epics and six gates. The build sequence says 115 items
and Kanban. The engineering practices say trunk-based and merge daily. No contradiction.

**Disposition:** `CTX-DELIVERY-001` to `CTX-DELIVERY-007`; `docs/increments/epics/EPIC-001-*` and
`EPIC-002-*` (moved from the original `INC-001-*`/`INC-002-*` names on 2026-11-04).

### Q10. What is the AI approach?

**Answer:** Agents run through an orchestrator and tool gateway at autonomy L0–L4. They start in
shadow, then recommend, then act only on evidence. If an agent does not answer in 60 seconds or fails a
guardrail, the rule result is used. The decision log records the model, agent and prompt versions.

**Sources:** `requirement/legacy/08-ai-and-agents/recovery-workbench-agent-catalog-and-specifications-v2.md`;
`.../recovery-workbench-ai-decision-governance-v2-docx.md`;
`.../recovery-workbench-ai-assisted-development-approach-v1.md`.

**Verification:** The agent catalogue has an entry for each agent with autonomy at go-live and target.
The 60-second fallback is repeated in the NFR (NFR-010) and the catalogue. The decision log fields are
in the governance design and NFR-033. No contradiction.

**Disposition:** `CTX-AI-001` to `CTX-AI-006`; `AGENTS.md`.

### Q11. What is open or contradictory?

**Answer:** The set has version drift, duplicate formats, no live Figma, no ACE source code, unapproved
Thai labels, open RPO/RTO/retention decisions, no Jira keys and a partial Epic 1 story-file extraction.

**Sources:** `requirement/legacy/12-project-communication/recovery-workbench-document-index-v11.md`;
`requirement/legacy/11-delivery-and-operations/recovery-workbench-risks-assumptions-issues-and-dependencies-v2-xlsx.md`;
`requirement/legacy/_conversion-report.md`.

**Verification:** The map flags the duplicate formats and the version gap. The risks register lists
the open dependencies. The decision log lists the open decisions. The gap report records the rest.

**Disposition:** `CTX-GAP-016` to `CTX-GAP-025`; `requirement/Intake_Gap_Report_RecoveryWorkbench.md`.

### Q12. What is the first increment?

**Answer:** Epic 1, Foundation 1, release 30 November 2026. It delivers the case list, case record
read-only, document store and OCR, decision log store, allocation/assignment/transfer by rule,
timers and prescription dates, baseline measures and the agent runtime in shadow.

**Sources:** `requirement/legacy/11-delivery-and-operations/recovery-workbench-release-plan-v3-xlsx.md`
(E1 row); `docs/brds/business-requirements-epic-1.md` §1; `docs/discovery/project-overview.md` §7.

**Verification:** The release plan says E1 is Confirmed, 118 features, 67 stories, 67 requirements,
57 Must. The Epic 1 BRD says 67 requirements, 57 Must, 77 programme requirements. The project overview
lists the same E1 outcome. No contradiction.

**Disposition:** `docs/increments/epics/EPIC-001-foundation-1.md` and
`docs/increments/epics/EPIC-001-tailoring.md` (moved from the original `INC-001-*` names on
2026-11-04).

## 3. Gaps recorded instead of guessed

| Gap | Why it cannot be answered from the set | What was done |
|---|---|---|
| Filename vs internal version | The file name and the document control table disagree. | Recorded `CTX-GAP-016`; the filename is treated as the set version and the internal version is recorded in the map. |
| Epic 1 story-file version | Consolidated v7, per-story v5, 69 of 79 extracted. | Recorded `CTX-GAP-017`; the consolidated v7 is canonical until the story files are reissued. |
| Epic 2 story-file version | Consolidated v5, per-story v4. | Recorded `CTX-GAP-018`; same disposition. |
| Figma | No live link or file. | Recorded `CTX-GAP-019`; local design artifacts are the evidence. |
| ACE source code | Not in the workspace. | Recorded `CTX-GAP-020`; context is intended behaviour, not verified implementation. |
| Thai labels | Proposed, not approved (DL10). | Recorded `CTX-GAP-021`; English can ship first. |
| RPO/RTO/retention | Open (DL11, DL26). | Recorded `CTX-GAP-022`, `CTX-GAP-011`, `CTX-GAP-012`; use ACE values and data-driven classes. |
| Jira keys | Not assigned. | Recorded `CTX-GAP-023`; traceability uses RWB keys. |
| Same-day interfaces | Not named (DL06). | Recorded `CTX-GAP-010`; default end-of-day. |
| Partner access | Not live (DL03). | Recorded `CTX-GAP-013`; partner tests limited to the bank network. |
| Model endpoint | Not approved (DL33). | Recorded `CTX-GAP-014`; agents in shadow with rule fallback. |

## 4. Verification performed

| Check | Result |
|---|---|
| Every context file exists and has a purpose and scope | Pass |
| Every business statement has a CTX ID and a source | Pass |
| Feature catalogue covers P1–P10, S1–S9 and cross-cutting administration | Pass (20 capabilities) |
| Rule catalogue covers the 448-rule families | Pass (16 families) |
| Data context covers 14 data products and 108 entities by reference | Pass |
| NFR context covers 10 groups and numeric targets | Pass |
| Compliance context covers PDPA, 42 controls, regulatory map and audit findings | Pass |
| Delivery context covers 8 releases, 6 gates and 115 build items | Pass |
| AI context covers agents, autonomy, decision governance and fallback | Pass |
| Gaps have an owner and a needed-by date | Pass (owner/date TBC where the source is silent) |
| No personal data, credential or production data | Pass (spot scan of generated files) |
| Named approvers | Not yet; increment cards carry `TBC` |
| Source versions reconciled | Not yet; recorded as `CTX-GAP-016` to `CTX-GAP-018` |

## 5. Status

```text
CONTEXT_CREATION_STATUS: READY [PHASE: verification] [ARTIFACTS: 6]
TECH_STACK_DETECTED: frontend=React/Vite/Radix/TanStack Query, backend=Spring Boot/Java/PostgreSQL, testing=JUnit/Playwright/SIT/UAT
CONTEXT_FILES_CREATED: [project-context.md, domain-context.md, frontend-context.md, backend-context.md, testing-standards.md, Context_RecoveryWorkbench.md]
SKIPPED_EXISTING: []
UPDATE_HANDOFFS: [CTX-GAP-016..018 version reconciliation; named approvers]
TRACEABILITY_STATUS: 145 CTX-* IDs created and mapped
FEATURE_COVERAGE: [DISCOVERED: 20] [DOCUMENTED: 20] [UNRESOLVED: 0] [RECONCILIATION: project-context.md §15]
NEXT_STEP: Human review of the context files, then run the Requirement Intake Consolidator.
```
