---
title: Project Context
description: "Approved project context read by every agent; created by Context Builder and maintained by Context Updater"
---

This folder holds the approved project context that every agent reads before starting a task.
It is created by **Context Builder** and maintained by **Context Updater**; other agents must not
modify these files.

| File                   | Content                                                                                   |
|------------------------|-------------------------------------------------------------------------------------------|
| `project-context.md`   | Business requirements, logic, rules, constraints, design intent and acceptance criteria   |
| `domain-context.md`    | Industry and domain references that supplement the business requirements                 |
| `frontend-context.md`  | Frontend implementation and detailed design: screens, themes, fonts, styles               |
| `backend-context.md`   | Backend implementation: APIs, data, integrations and operations                           |
| `testing-standards.md` | Testing and verification strategy, frameworks and coverage expectations                   |

Additional user-provided standards (architecture decisions, coding conventions, design-system
rules) are preserved and indexed here as well. Keep the context current, approved and specific:
agents work from what is written here, not from what the squad knows.
