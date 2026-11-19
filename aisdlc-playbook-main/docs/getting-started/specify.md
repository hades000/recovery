---
id: specify
title: 4.7 Create the technical specification
description: "Technical Specifier (Spec-Clarify): from the approved requirement to an implementation-ready specification with resolved clarifications."
sidebar_label: 4.7 Specify
---

:::note Section summary
Technical Specifier (Spec-Clarify): from the approved requirement to an implementation-ready specification with resolved clarifications.
:::

**Lifecycle phase:** 5 Create backlog and specification · **Agent:** [Technical Specifier](/agents/spec-clarify) (`.github/agents/specify.agent.md`) · **Gate:** specification approval (Product Owner); Compliance Reviewer spec gate

:::warning Context reset
Start a new chat session before invoking the Technical Specifier so that the specification starts from the approved requirements and current project context.
:::

## Invoke the Technical Specifier agent

Provide one of the supported inputs to the agent:

* a Jira story key (fetched through the `jira` MCP server),
* a canonical requirement Markdown file (`requirement/<Project>_<JiraKey>_Requirements.md`),
* an approved PRD, or
* the active requirement file.

Include the applicable project context from `.github/contexts/` and identify the `RUN_ID` if the
work is continuing an existing lifecycle run.

Select **Technical Specifier** in Copilot Chat and use a prompt such as:

```text
Create an implementation-ready technical specification for <Jira key or requirement file>.
Use the approved project context and preserve traceability to the source requirements.
Record unresolved questions as clarifications; do not make unsupported assumptions.
```

The agent creates its specification artefacts under:

```text
output/<RUN_ID>/specify/
├── spec.md
├── compliance-validation.md
└── figma/            design evidence (when the increment has frontend work)
```

`spec.md` declares `API In Scope: YES|NO` and `UI In Scope: YES|NO`; the testing agents later read
these declarations to decide what to test.

## Review the specification

Review `spec.md` and confirm:

* [ ] Requirements and acceptance criteria are traceable to the specification IDs (`FR-*`/`NFR-*` → `SPEC-*`).
* [ ] Frontend and backend behaviour, contracts, validation and error handling are covered where
  applicable.
* [ ] Design evidence and any pending manual uploads are clearly identified for frontend work.
* [ ] Clarifications are resolved or explicitly listed for follow-up; no unanswered decision is
  treated as an implementation assumption.
* [ ] Required specification artefacts and source references are present.

### Design evidence

| Situation | Specification outcome |
|---|---|
| No frontend task (`UI In Scope: NO`) | Figma or screenshots optional (`NOT_REQUIRED`) |
| Figma link works | Live Figma artefacts extracted by the Figma Extractor |
| Figma fails or no link; screenshots from Jira, Confluence or manual upload | Screenshots with `SCR-*` IDs, marked `Design Source: Manual upload (no Figma link)` |
| Frontend in scope, no design evidence at all | `DESIGN_EVIDENCE_STATUS: PENDING_MANUAL_UPLOAD`; planning is blocked until screenshots are added to `output/<RUN_ID>/specify/figma/png/screens/` and the Technical Specifier is re-run |

## Compliance review

Complete the required **Compliance Reviewer** specification review (the Technical Specifier invokes
it automatically) and address its findings before planning. Then review the agent's `NEXT_STEP`
status and start the next stage manually.

Next: [4.8 Plan the implementation](/getting-started/plan).
