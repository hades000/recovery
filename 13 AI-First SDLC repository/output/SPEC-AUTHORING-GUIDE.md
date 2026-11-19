# Epic 1 batch — Technical Specifier authoring guide

This guide is for the module subagents producing the Epic 1 technical specifications. Follow it
exactly so the 78 specs are consistent and reviewable.

## 1. Purpose

Produce one implementation-ready specification per Epic 1 story, following the toolkit's
`specification-execution-gates.md`. The pilot `RWB-E1-020` is the pattern:

`output/INC-043-epic-1-RWB-E1-020/specify/spec.md`

Do not copy its content. Use its structure.

## 2. Source hierarchy

Read in this order, and stop when the story is covered:

1. **The story file** in
   `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/`.
   It has the story, preconditions, flow, exception paths, acceptance criteria, business rules,
   state transitions, authority, data, contract, solution plan, messages, screens, tests, guardrails,
   traceability and out of scope.
2. **The module FSD** in `docs/prds/` — the functional behaviour.
3. **The module TSD** in `requirement/legacy/05-technical-architecture/` — components, data model
   (T3), interfaces, access, jobs.
4. **The shared sources only as needed:**
   - `requirement/legacy/06-data/recovery-workbench-logical-data-model-and-data-dictionary-v6-xlsx.md`
     (use the TSD T3 first; open the dictionary only for a specific field ID)
   - `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml`
     (the specific endpoints)
   - `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-rules-and-routing-logic-v4-xlsx.md`
     (the rule IDs the story cites)
   - `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v3-docx.md`
   - `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v3-xlsx.md`
   - `.github/contexts/project-context.md`, `backend-context.md`, `frontend-context.md`,
     `testing-standards.md`
   - `requirement/RecoveryWorkbench_Requirements.md` and `requirement/BRD_RecoveryWorkbench.md`

## 3. Output

For each story key `RWB-...`, write:

```text
output/INC-<NNN>-epic-1-<KEY>/specify/spec.md
output/INC-<NNN>-epic-1-<KEY>/specify/agent-run-log.md
output/INC-<NNN>-epic-1-<KEY>/specify/compliance-validation.md
```

The story key includes its prefix, e.g. `INC-010-epic-1-RWB-E1-001` or `INC-018-epic-1-RWB-TE-004`.

**Do not modify any shared file.** Do not edit `requirement/Traceability_Matrix.md`, the context
files, the source documents or another story's output. The parent will merge the traceability rows.

## 4. Required spec sections

Every spec must have, in this order:

1. Header table: story, epic/module, RUN_ID, source requirement, upstream IDs, status, date.
2. `## Change Scope Declaration` with:
   - `Change Type` (`NEW_STORY` unless the story is an enabler on an existing capability, then
     `ENHANCEMENT_LOGIC_ONLY`)
   - `UI In Scope: YES|NO`
   - `Logic In Scope: YES|NO`
   - `API In Scope: YES|NO`
   - `API Impact Type: NO_API_CHANGE|EXISTING_API_CHANGE|NEW_API_REQUIRED`
   - `Impacted Existing Nodes`
   - `New Nodes Required: YES|NO`
   - `Inherited Existing Behavior`
   - `Frontend Changes Required: YES|NO`
   - `Backend Changes Required: YES|NO`
3. `## Requirement-to-SPEC Logic Coverage` with columns `REQ_REF`, `Requirement Logic Statement`,
   `Mapped SPEC-*`, `Coverage Type`, `Implementation Notes`, `Status`.
   Map every business rule and every acceptance criterion. Use `SPEC-<KEY>-001` etc.
4. User story intent interpretation.
5. Entry trigger and preconditions.
6. Field-level behaviour matrix.
7. Status-transition matrix.
8. Exceptional-case behaviour.
9. API change assessment.
10. `## Unit Test Applicability` with one frontend row and one backend row. If a surface does not
    change, set `NOT_APPLICABLE` and cite the evidence. If it changes, set `REQUIRED` and the 80%
    lines/statements/branches/functions gate.
11. Detailed design: components, data/migration, rules, transaction, events, security, observability,
    performance, feature flag/rollback.
12. Test scenarios (system, security, unit).
13. `## Clarification Log` with `CLAR-*` items. Every item must be `RESOLVED` or the run is
    `BLOCKED`.
14. `## Status reporting` with the exact lines from the gate:
    `MCP_STATUS_SUMMARY`, `MCP_API_RESULT`, `CHANGE_CLASSIFICATION_SUMMARY`,
    `CHANGE_CLASSIFICATION_RESULT`, `REQUIREMENT_COVERAGE_SUMMARY`,
    `REQUIREMENT_COVERAGE_RESULT`, `DESIGN_EVIDENCE_STATUS`, `CLARIFICATION_STATUS`, `NEXT_STEP`.

## 5. Scope decisions

- **UI In Scope: YES** only if the story adds or changes a screen, component, route, label, state or
  validation presentation. The screen inventory is
  `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md`.
  If UI is in scope and there is no Figma, set
  `DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: n]` and cite the screen
  specification and prototype. Do not claim Figma.
- **API In Scope: YES** only if the story adds or changes an endpoint or contract. If it reuses an
  existing endpoint, set `API In Scope: NO` and `API Impact Type: NO_API_CHANGE`, and name the reused
  endpoint. If it adds a job, event or internal interface, document it under detailed design, not as
  an API change.
- **Logic In Scope: YES** for every story with a rule, state transition, validation, calculation,
  allocation, timer, access check or data transformation.
- **Frontend Changes Required** must agree with `UI In Scope`.
- **Backend Changes Required** must agree with the logic/API/data work.

## 6. No-invention rules

- Use only the story, the module FSD/TSD, the data dictionary, the API spec, the rules, the messages
  and the context. Do not infer a business rule, threshold, field, message, role or route.
- If the source is silent, record a `CLAR-*` item with the question, the impact and the proposed
  answer. If the answer is not in the sources, mark the run `BLOCKED` and explain. Do not invent.
- Mark unverified statements `GAP` or `ASSUMED` and name the decision log entry.
- No personal data, credentials, tokens or production data in a spec, log or test.
- No code. The spec describes the design; the Implementation Builder writes code in the ACE repo.

## 7. Size and quality

- Aim for 120–220 lines per spec. The required sections matter more than length.
- The coverage table must have no `BLOCKED` rows. Every business rule and acceptance criterion must
  be mapped.
- The test scenarios must cover the happy path, the exception paths and the security/authority path.
- The spec must be self-contained: a planner should not need to re-read the FSD to write tasks.

## 8. Compliance validation

Write a short `compliance-validation.md` per story:

- `Overall status`: `PASS`, `PASS_WITH_WARNINGS` or `FAIL`.
- 0 Critical/High/Medium findings for a pass; list any Low findings with owner and remediation.
- Check: authorization, PDPA/data protection, audit logging, error handling, test applicability,
  traceability, secrets/configuration, design evidence.
- If the story has an open `CLAR-*` that affects behaviour, mark `FAIL` and stop.

## 9. Return summary

Return a table:

| Key | Status | Spec path | UI | API | CLARs | Findings |
|---|---|---|---|---|---|---|

Also list any story that is `BLOCKED`, the reason, and the exact unblock action. Do not return the
full spec text; the files are the deliverable.
