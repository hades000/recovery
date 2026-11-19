---
title: "Frontend standards for the new module (USER-PROVIDED)"
description: "Squad decisions for frontend work on ACE that cannot be read from the code; Context Builder incorporates them into frontend-context.md"
---
Status: Draft, owner FDA with UX. Every row is `USER-PROVIDED`. Rows marked **TBD** are open decisions:
agents must not fill them in and must raise them as open items when a story depends on them.

ACE rules still apply and are not repeated here: `ace-monorepo/AGENTS.md`,
`ace-monorepo/frontend/AGENTS.md`, `ace-monorepo/docs/coding-standard.md` (backend owns business
logic, Ketting for HAL navigation, API types only from `frontend/src/api/schema.d.ts`).

## FS-1 Module structure

| ID     | Standard                                                                                                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| FS-1.1 | Recovery screens, components and hooks live in `frontend/src/modules/recovery/` (RWB-TE-001; D-RCV-10)                                                                                                                         |
| FS-1.2 | The module's code does not import another business area's components or hooks (for example `cfsc`, `tdr`); shared pieces come only from `components/ui`, `hooks`, `lib`, `utils`. Enforcement (lint rule): **TBD** |
| FS-1.3 | Routes of the module are registered under one path prefix: **TBD**; menu entry and placement: **TBD**                                                                                                                    |

## FS-2 UI and design

| ID     | Standard                                                                                                                                                                                                                                                                                                        |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FS-2.1 | Use the ACE design system: `frontend/src/components/ui` and ACE Tailwind tokens (font, colours, radius). Henka Screen Specifications v1 and the prototype give layout, content, labels and behaviour; Henka Design System v1 visual tokens are not used (D-RCV-08). A new shared component needs FDA approval |
| FS-2.2 | Design evidence (Figma file, screenshots or accepted minimal design) is required per screen before planning, as the toolkit rules state. Figma location: **TBD**                                                                                                                                          |
| FS-2.3 | Language: UI text through i18next; supported languages and default: Thai / English                                                                                                                                                                                                                             |
| FS-2.4 | Accessibility target: **TBD** (for example WCAG 2.1 AA)                                                                                                                                                                                                                                                   |
| FS-2.5 | Personal data shown on screen follows the backend masking (BS-4.2); the frontend never unmasks or computes it                                                                                                                                                                                                   |

## FS-3 Data and state

| ID     | Standard                                                                                                                                                                           |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FS-3.1 | Server data through TanStack Query hooks; no business calculation in the frontend (ACE rule "backend owns business logic")                                                         |
| FS-3.3 | Recovery screens call the plain-JSON `/api/recovery/v1` API with types from `frontend/src/api/schema.d.ts`; Ketting/HAL navigation is not used for recovery data (ADR-RCV-001) |
| FS-3.2 | Every interactive element used by tests has a `data-testid` (the toolkit's Playwright MCP uses `data-testid`)                                                                  |

## FS-4 Testing

| ID     | Standard                                                                                                                                              |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| FS-4.1 | Functional UI tests run with Playwright against the local front end on ACE local ports: frontend `5173`, backend `8080` (D-RCV-09, `.mcp.json`) |
