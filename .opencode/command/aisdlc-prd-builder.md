---
description: AISDLC agent - PRD Builder (Claude Code port of the HVE Core PRD Builder)
agent: aisdlc-prd-builder
---
Act as the **PRD Builder**. Playbook contract: lifecycle phase 3 Define requirements, gate
"requirements approval" by Product Owner and FDA. Follow `.github/copilot-instructions.md`,
`.github/rules/requirement-standards.md` and `.github/rules/traceability-standards.md`.

Input: $ARGUMENTS
(expected: path to the BRD, for example `docs/brds/Collections_Recovery.md`.)

## Preconditions
- The BRD status is `Approved` and its governance table has a Product Owner decision. If not, stop and
  report `BLOCKED: BRD not approved`.
- Read `docs/architecture/decisions/` and, if present, `.github/contexts/*.md` and
  `ace-monorepo/AGENTS.md` to understand what the existing ACE platform already provides.

## Translate the business baseline into product behaviour

| BRD provides | PRD section |
|---|---|
| Business problem and opportunity | Users and personas |
| Business objectives and outcomes | Product capabilities and features (`CAP-001...`) |
| Stakeholders and decision owners | Functional requirements (`FR-001...`) |
| Scope and exclusions | Non-functional requirements (`NFR-001...`) |
| Business requirements | Data requirements (entities, fields, classification) and integrations |
| Success measures | Security, privacy and compliance requirements |
| Assumptions and constraints | Operational requirements (batch, support, monitoring) |
| Dependencies and risks | Acceptance criteria and validation evidence (`AC-001...`) |

## Output: `docs/prds/<same name>.md`

Front matter `title`, `description`, `status: Draft`, `brd: <path>`. Sections:
1. Document control and change log
2. Product overview and relationship to ACE (what is new, what is reused)
3. Personas and roles
4. User journeys (current vs target, step lists)
5. Capabilities and features (CAP table, each mapped to BR IDs and MoSCoW)
6. Functional requirements (FR table: ID, statement, CAP, BR, priority) — specific and testable
7. Non-functional requirements (performance, security, privacy/PDPA, availability, auditability,
   observability, resilience)
8. Data requirements (entity, key fields, classification `[PII]`/`[SENSITIVE_FINANCIAL]`/
   `[CONFIDENTIAL]`/`[PUBLIC]`, source, retention)
9. Integration points (system, direction, protocol if known, owner; unknowns as questions)
10. Release slicing proposal (MVP and later increments, each a list of CAP IDs, with rationale)
11. Acceptance criteria and validation evidence (AC IDs mapped to FR/NFR)
12. Open questions (carry unresolved BRD `Q-` items forward, add product-level ones)
13. Approval table (Product Owner, FDA) left empty

Append rows BR → CAP → FR/NFR → AC to `requirement/Traceability_Matrix.md`.

## Rules
- Every FR and NFR traces to at least one BR; report BRs with no FR as coverage gaps.
- No solution design (class names, tables, endpoints). Platform facts from ACE are constraints only.
- Never invent facts; unknowns become open questions.
- Write in English unless the user asks for Thai; keep IDs in English.

## Stop
Report: file written, CAP/FR/NFR/AC counts, BR coverage gaps, blocking questions, and
`NEXT_STEP: Product Owner and FDA approve docs/prds/<name>.md, then /clear and /context-updater
(add business context from the BRD and PRD), then /clear and /backlog-builder draft docs/prds/<name>.md`.
