---
id: brd
title: 4.2 Convert raw requirements into a BRD
description: "BRD Builder: from stakeholder context to a structured Business Requirements Document."
sidebar_label: 4.2 BRD
---

:::note Section summary
BRD Builder: from stakeholder context to a structured Business Requirements Document.
:::

**Lifecycle phase:** 3 Define requirements · **Agent:** [BRD Builder](/agents/brd-builder) (HVE Core) · **Gate:** requirements approval (Product Owner)

## Invoke the BRD Builder agent

Attach the available source material to the chat. This may include:

* `raw-requirements.md`
* a Word document
* a meeting transcript
* a statement of work

Select **BRD Builder** in Copilot Chat and use the following prompt:

```text
Create a Business Requirements Document from the attached <your project> stakeholder context.
Identify business objectives, reconcile contradictions between stakeholders, define scope
boundaries, and produce a structured BRD.
```

## Review the BRD output

The agent creates the BRD in:

```text
docs/brds/<brd_name>.md
```

Review the draft and confirm:

* [ ] Have the relevant stakeholders been identified?
* [ ] Have contradictions in the raw requirements been reconciled?
* [ ] Are the business objectives quantified where appropriate, based on the use case?
* [ ] Are the scope boundaries clear?

## Revise the BRD

If the result does not meet expectations, provide corrections and ask the BRD Builder agent to
revise the document. The BRD should not contain detailed technical implementation decisions unless
those decisions represent confirmed business constraints.

:::warning Gate
The BRD is reviewed by business owners, product leadership, architecture, security, governance and delivery stakeholders before it becomes the approved input to PRD creation.
:::

Next: [4.4 Convert the approved BRD into a structured PRD](/getting-started/prd).
