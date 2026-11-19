---
id: squad-roles
title: 5. Product squad roles and responsibilities
description: "Product squad roles and role evolution."
sidebar_label: 5.1–5.2 Squad roles
---

## 5.1 The team is the unit of leverage

:::note Section summary
Product squad roles and role evolution.
:::

Agentic delivery increases the importance of the team system. Product and design roles continue to
define outcomes and user intent. Architecture and engineering roles convert that intent into
boundaries, specifications, context and executable work. Quality, security, DevOps and reliability
roles validate the evidence and protect production outcomes.

:::info
Agents increase team capacity, but they do not become accountable roles.
:::

High-performing agentic teams make four practices explicit:

* Knowledge: conventions, architecture decisions, controls and operating procedures are
  recorded rather than kept in individual memory.
* Review: agent output is reviewed as seriously as human-produced output. Review is a quality
  activity, not a formality.
* Specification: work is bounded and described clearly enough for people and agents to
  understand what must be done and what must not change.
* Feedback: rework, context gaps and repeated failures are captured and used to improve the
  workflow and context.

## 5.2 Core product squad roles

:::note Section summary
Key roles and responsibilities.
:::

| Role | Core accountability |
|---|---|
| **Product Owner** | Owns the product vision, roadmap, backlog and business outcomes. Aligns priorities, makes trade-offs and approves product intent. |
| **Forward Deployed Architect (FDA)** | Defines the scalable technical architecture, solution patterns, integration approach and architectural guardrails. |
| **Product Designer** | Designs the end-to-end user experience, translates user needs into journeys and interfaces, and supports adoption. |
| **Forward Deployed Engineer (FDE)** | Connects approved architecture to executable delivery by managing context, specifications, agents, reviews and hand-offs. |
| **Application Engineer** | Builds, configures, tests and deploys product functionality. Remains accountable for implementation quality. |
| **Quality Engineer** | Defines and executes the test strategy, validates evidence and supports production-readiness decisions. |
| **DevOps Engineer** | Automates build, deployment and infrastructure processes and maintains reliable delivery pipelines and environments. |
| **Site Reliability Engineer** | Monitors service health, supports incident response and drives reliability and operational improvement. |
| **Security Engineer** | Embeds security, privacy and regulatory requirements from design through production and reviews relevant risks and guardrails. |

## Who approves what

| Gate | Accountable role |
|---|---|
| Intake approval | Product Owner |
| Context readiness | Forward Deployed Engineer |
| Requirements approval (BRD, PRD) | Product Owner, Forward Deployed Architect |
| Design and architecture approval | Forward Deployed Architect |
| Specification approval | Product Owner |
| Plan approval | Forward Deployed Architect |
| Task approval | Forward Deployed Engineer |
| Code review (pull request) | Forward Deployed Engineer |
| Quality and security gate | Forward Deployed Architect, Quality Engineer, Security Engineer |
| Release readiness | Forward Deployed Engineer |
| Deployment approval | Product Owner / Project Manager |
| Ongoing review | Ops / System Manager (SRE) |

The human-review column of each [agent catalogue](/agents/catalogue) entry names the role that
checks the agent's output and the decision that remains human.

Next: [5.3 How engineering roles evolve](/roles/role-evolution).
