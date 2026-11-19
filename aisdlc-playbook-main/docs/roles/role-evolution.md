---
id: role-evolution
title: 5.3 How engineering roles evolve
description: "Agentic PDLC shifts engineering effort from individual execution towards team capability, context, review and orchestration."
sidebar_label: 5.3 How engineering roles evolve
---

:::note Section summary
Agentic PDLC shifts engineering effort from individual execution towards team capability, context, review and orchestration.
:::

Agentic PDLC does not create a clean break between "before" and "after" engineering roles. Instead,
it changes where existing roles spend their time and where they create the most value.

The shift is from individual output towards team capability. Faster code generation alone does not
create a high-performing agentic team. Agent performance depends on the quality of the context,
specifications, review practices and feedback loops around it. A strong team therefore makes
knowledge explicit, writes clear specifications, reviews agent output rigorously and learns
systematically from failures.

Four team practices become particularly important:

* Explicit knowledge: document conventions and architecture decisions so that knowledge is
  available to both people and agents rather than remaining tribal.
* Strong review culture: treat review of agent output as a core engineering discipline rather
  than a final checkpoint.
* Clear specification habits: describe bounded work precisely enough that people and agents
  understand what must be done and what must not change.
* Feedback loops: capture recurring failures and context gaps, then improve the shared context
  and ways of working so that the same problems are not repeated.

The practical implication is that Agentic PDLC should strengthen the capability of the whole squad
rather than optimise for individual developer output.

## 5.3.1 Senior Engineering / Forward Deployed Architect: from expert implementer to context architect

:::note Section summary
Senior engineering judgement increasingly shapes the architecture, constraints and context through which the squad and agents deliver.
:::

The value of senior engineering has always depended heavily on judgement. Agentic delivery makes
that more explicit. Rather than spending the majority of time personally implementing the hardest
code, senior engineering effort increasingly moves towards architecture, context engineering,
review, escalation and mentoring.

| Traditional emphasis | Agentic product squad |
|---|---|
| **Primary contribution:** writes or resolves the most complex and critical implementation work. | **Primary contribution:** shapes the architecture and context through which people and agents deliver. |
| **Architecture:** applies patterns and resolves difficult design decisions. | **Architecture:** defines the boundaries, patterns and constraints that agents and engineers must respect. |
| **Knowledge:** shares engineering judgement through experience, guidance and code review. | **Context engineering:** translates architectural knowledge into explicit instructions, conventions, configurations and reusable context. |
| **Review:** reviews code for quality, maintainability and architectural fit. | **Review and escalation:** evaluates agent output against architectural intent, identifies subtle violations and handles cases that agents cannot resolve. |
| **Mentoring:** teaches implementation techniques and engineering practices. | **Mentoring:** teaches engineers how to write effective specifications, evaluate agent output and develop engineering judgement. |
| **Leverage:** personally solves the hardest engineering problems. | **Leverage:** creates the conditions that allow the wider squad and agents to solve work consistently. |

The shift is from **"the person who writes the hardest code"** towards **"the person who shapes
the system that writes the code."**

A central capability in this shift is **context engineering**: deciding what architectural
knowledge, standards, conventions and constraints need to be made explicit so that agents can act
consistently with engineering intent. In the toolkit this knowledge lives in `.github/contexts/`
and `.github/rules/`.

Within the target Product Squad, the exact mapping depends on scope. Responsibilities close to
implementation may remain with a senior Application Engineer, while architecture-wide
responsibilities align more closely to the **Forward Deployed Architect (FDA)**.

## 5.3.2 Application Engineer development pathway: from code writer to AI-augmented contributor

:::note Section summary
Junior engineers increasingly learn through specification, review, diagnosis and context contribution as well as through implementation.
:::

The evolution of junior engineering requires particular care. Agents can increasingly perform the
simple bug fixes, small features and boilerplate implementation that traditionally formed part of
the junior learning pathway. The answer is not to remove agents from junior workflows, but to
redesign how engineering skills and judgement are developed.

| Traditional emphasis | Agentic development pathway |
|---|---|
| **Implementation:** learns primarily by writing code. | **Review:** develops judgement by reviewing agent output, ideally with senior supervision. |
| **Task execution:** receives an implementation task and produces the code. | **Specification:** writes clear specifications for bounded agent tasks before implementation begins. |
| **Debugging:** investigates defects in manually written code. | **Failure diagnosis:** investigates why agent output is incorrect and what context, architectural rule or repository pattern was missed. |
| **Codebase learning:** develops familiarity through repeated implementation. | **Context contribution:** improves the documentation, conventions and instructions that agents use, requiring deeper understanding of the codebase. |

Reviewing agent output is therefore part of the learning process, not simply a quality-control
activity. Writing specifications forces engineers to think through the problem before
implementation, while diagnosing agent failures can expose architectural patterns and constraints
that might otherwise remain implicit.

The objective is not to create engineers who can operate agents without understanding the
underlying engineering. The objective is to use agent-supported delivery to develop engineering
judgement in a different way.

Within the target Product Squad, this should be treated as a **development pathway within the
Application Engineer role**, rather than as a separate future-state squad role.

## 5.3.3 Forward Deployed Engineer: from Tech Lead to delivery orchestrator

:::note Section summary
The Tech Lead's coordination role expands from allocating work across engineers to orchestrating work across people and agents.
:::

The Tech Lead role shifts from primarily assigning tasks to people towards determining how work
should be executed across humans and agents. This requires judgement about which tasks are
appropriate for agent execution, which require human implementation and which are best handled
through a hybrid approach.

| Traditional emphasis | Agentic product squad |
|---|---|
| **Work allocation:** assigns work based on role, expertise and capacity. | **Execution choice:** determines whether work should be human-led, agent-executed or hybrid. |
| **Decomposition:** breaks stories into implementable engineering tasks. | **Agent-aware decomposition:** identifies where complex work can be broken into bounded, agent-suitable tasks. |
| **Coordination:** coordinates work and dependencies across engineers. | **Orchestration:** coordinates work across people and agents while ensuring the required context is available. |
| **Problem resolution:** intervenes when engineering work encounters difficult technical problems. | **Escalation:** recognises tasks or code paths that agents cannot handle reliably and routes them back to appropriate human judgement. |
| **Continuous improvement:** improves team practices through delivery experience and retrospectives. | **Feedback-loop ownership:** tracks recurring agent failures, identifies context gaps and prioritises improvements to the shared context and ways of working. |

The role therefore requires more than deciding whether an apparently simple or complex task should
go to an agent. A simple-looking task may involve code paths that agents consistently mishandle,
while complex work may sometimes be decomposed into smaller tasks that agents can execute
effectively.

Within the target Product Squad, these responsibilities align most closely with the **Forward
Deployed Engineer (FDE)**: bridging approved architecture and executable delivery, coordinating
work across people and agents, and improving the context and delivery patterns that enable
reliable execution.

## 5.3.4 What this means for the engineering team

Across these role shifts, the common theme is that engineering leverage increasingly comes from the
**system around the work**, not simply from the amount of code produced by an individual.

* Senior engineers and FDAs make architectural knowledge and constraints explicit.
* Application Engineers increasingly combine implementation with specification, review, diagnosis
  and context contribution.
* FDEs orchestrate how work moves between people and agents and improve the feedback loops that
  make the delivery system more effective over time.

The aim is therefore not a "10x developer", but a more capable engineering team supported by
explicit knowledge, strong review practices, clear specifications and continuous feedback.
