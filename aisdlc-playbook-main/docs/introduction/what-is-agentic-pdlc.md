---
id: what-is-agentic-pdlc
title: 1.1 What Agentic PDLC means
description: "Shifting from human-heavy execution to agentic lifecycle orchestration."
sidebar_label: 1.1 What Agentic PDLC means
---

:::note Section summary
Shifting from human-heavy execution to agentic lifecycle orchestration.
:::

Agentic PDLC shifts product delivery from a sequence of predominantly human-executed activities to a
governed system in which people and agents work across the lifecycle. Agents carry out defined
analysis, generation, coordination and validation tasks from planning through operations. People
continue to set intent, supply and approve context, govern risk and validate outcomes.

Three ideas sit at the centre of the model:

* **Context is carried across phases.** Each activity builds on approved requirements, designs,
  decisions, standards and prior outputs.
* **Squads adopt from their current starting point.** Greenfield, brownfield and modernisation
  increments enter the same lifecycle at different points.
* **Work is orchestrated end to end**, rather than through isolated AI tools.

## Three core characteristics

1. Agents support or execute work from planning through operations.
2. Humans define the objective, set boundaries, review material outputs and approve progression.
3. Context moves across phases so each activity can build on approved requirements, designs,
   decisions, standards and prior outputs.

## Context is central

Agents should work from current, approved and well-structured requirements, designs, decisions,
standards and system information. The approach therefore combines agent use with **context
engineering**, delivery controls, evaluation, observability, security and evidence capture.

:::info Agents do not share the squad's background knowledge
They cannot draw on previous conversations, undocumented conventions or decisions that experienced
team members simply "know". If this knowledge is not made explicit and included in the agent's
working context, the agent cannot reliably apply it.
:::

Providing more information is not necessarily the answer. Context is limited, and irrelevant,
outdated or conflicting material distracts from the information that matters. Squads should
provide the **right** context, not **all** available context: identify authoritative sources and
supply the approved requirements, architecture decisions, standards, constraints and acceptance
criteria relevant to the task.

Even a capable agent can produce convincing but incorrect output when its context is incomplete or
unclear. Reliable agent-enabled delivery therefore depends on well-structured context, clear
instructions, defined constraints, evaluation and human review. Context should be treated as a
**governed delivery artefact** that is prepared, approved and kept current throughout the lifecycle.

### Before using an agent

Confirm that the information needed for the task is:

* [ ] approved
* [ ] accessible
* [ ] current
* [ ] sufficiently specific

Microsoft and IBM guidance both reinforce that agent quality must be assessed through the outcome
**and** the execution process, including tool use and intermediate steps, rather than the final
output alone.

In the toolkit, context lives in `.github/contexts/` and is created by the
[Context Builder](/agents/context-builder) and maintained by the Context Updater. See
[Contextualise](/paths/greenfield#2-contextualise) for where it sits in the lifecycle.
