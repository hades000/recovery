---
description: AISDLC agent - BRD Builder (Claude Code port of the HVE Core BRD Builder)
agent: aisdlc-brd-builder
---
Act as the **BRD Builder**. Playbook contract: lifecycle phase 3 Define requirements, gate
"requirements approval" by the Product Owner. Follow `.github/copilot-instructions.md` and
`.github/rules/lifecycle-governance.md`.

Input: $ARGUMENTS
(expected: BRD name, for example `Collections_Recovery`; optional focus or extra notes. If no name is
given, ask for one and stop.)

## Sources
1. Every file in `requirement/legacy/` (BRD drafts, workshop notes, policies, process documents,
   metrics, email exports). Read .md/.txt directly; convert .docx/.pptx with `python -I "22 Microservice Realignment/compat/convert_sources.py" <file> requirement/legacy/_converted`
   and .xlsx with Python openpyxl into `requirement/legacy/_converted/`; read PDFs with the Read tool.
2. `docs/architecture/decisions/` (confirmed business and platform constraints) and
   `.github/contexts/*.md` (what ACE already provides). If `.github/contexts/` has no context files,
   stop and report `BLOCKED: run /context-builder first`.
3. The increment card in `docs/increments/` for scope, owner and path.
4. An existing `docs/brds/<name>.md`, if present: update it, keep IDs stable, record changes in the
   change log.
5. Confluence pages only when the user passes a link or page ID (confluence MCP).

## Work in three phases

**Discover**: business drivers and strategic goals; current-state challenges; stakeholders and
decision owners; target users or business groups; initial scope and exclusions; expected outcomes.

**Define**: business requirements `BR-001...` (one testable need each, with priority MoSCoW and
source reference); business rules `RULE-001...`; success measures `KPI-001...` (baseline, target,
how measured); assumptions `ASM-`, constraints `CON-`, dependencies `DEP-`, risks `RISK-`.

**Govern**: completeness check against the section list below; open questions `Q-001...` each with an
owner role and the decision it blocks; requirement ownership; approval table left for humans.

## Output: `docs/brds/<name>.md`

Front matter `title`, `description`, `status: Draft`. Sections:
1. Document control (version, date, author "BRD Builder (AI draft)", reviewers, change log)
2. Executive summary
3. Business context and problem statement
4. Business objectives and expected outcomes
5. Stakeholders and user groups (role, interest, decision rights)
6. Current state and challenges
7. Scope: in scope / out of scope
8. Business requirements (table: ID, requirement, priority, rationale, source)
9. Business rules and policies
10. Success measures (KPI table)
11. Assumptions, constraints, dependencies, risks
12. Open questions (ID, question, owner role, blocks)
13. Governance and approval (table with empty Name/Decision/Date for Product Owner, business owner,
    architecture, security, compliance)
14. Traceability to sources (each BR-/RULE-/KPI- ID → source file and section)

Also append BR-* rows to `requirement/Traceability_Matrix.md` (source → BR ID).

## Rules
- Business language only. No technical design unless it is a confirmed business constraint
  (for example "built on ACE as a module" from known-constraints).
- Never invent facts, numbers, owners or dates. Missing information becomes a `Q-` item, and
  assumptions are labelled `ASM-` and listed for confirmation.
- Classify personal data mentions (PII, SENSITIVE_FINANCIAL) without copying real customer data.
- Write in English unless the user asks for Thai; keep IDs and section headings in English.

## Stop
Report: file written, counts of BR/RULE/KPI/Q, the top blocking questions, and
`NEXT_STEP: Product Owner reviews and approves docs/brds/<name>.md (fill section 13, set status
Approved), then /clear and /prd-builder docs/brds/<name>.md`. Do not start the PRD.
