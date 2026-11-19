---
id: prd
title: 4.4 Convert the approved BRD into a PRD
description: "PRD Builder: from the approved business baseline to measurable product requirements."
sidebar_label: 4.4 PRD
---

:::note Section summary
PRD Builder: from the approved business baseline to measurable product requirements.
:::

**Lifecycle phase:** 3 Define requirements · **Agent:** [PRD Builder](/agents/prd-builder) (HVE Core) · **Gate:** requirements approval (Product Owner, FDA)

:::warning Context reset
Start a new chat session before invoking the next task agent so that the context for the new phase is clear.
:::

## Invoke the PRD Builder agent

Attach the approved BRD to GitHub Copilot Chat. Select **PRD Builder** and use the following
prompt:

```text
Transform this BRD into a Product Requirements Document for <product or increment>.
```

## Review the PRD output

Confirm that the PRD contains:

* [ ] Product overview: a one-paragraph description of the product or increment
* [ ] Architecture decision: the selected technology stack and supporting rationale
* [ ] Priority: each story tagged as P0, P1 or P2
* [ ] Technical constraints: the applicable platforms, technologies, security and compliance
  constraints
* [ ] MVP boundary: a clear P0 feature set that forms the MVP
* [ ] Non-functional requirements: performance, security and scalability requirements

Each requirement should be clear and unambiguous, traceable to a business objective, testable
through defined acceptance criteria, measurable where applicable, prioritised, supported by an
identified owner or source, and free from unsupported assumptions.

The agent writes the PRD to `docs/prds/<prd_name>.md`. The approved PRD is the key input to
solution architecture, backlog creation, detailed design, development, testing, security validation,
deployment and product operations.

Next: [4.5 Plan the implementation backlog](/getting-started/backlog).
