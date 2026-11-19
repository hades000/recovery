# Lifecycle Tailoring Record — EPIC-002 Foundation 2

| Epic ID | Path | Prepared by | Approved by | Date |
|---|---|---|---|---|
| `EPIC-002` | Greenfield Workbench module, brownfield ACE integration | FDE | Product Owner / FDA | 2026-11-16 |

**Applies to:** the 43 Epic 2 items listed in `../epic-2-stories.md`. Increments are opened one month
before the release; this record fixes the phase decisions now.

## Phase decisions

| # | Lifecycle phase | Classification | Reason | Applicable agents |
|---|---|---|---|---|
| 0 | Mobilise and assess | Mandatory | Increment record and approvals. | Context Builder |
| 1 | Discover and frame | Reusable | Discovery v14 covers Epic 2 journeys. | None |
| 2 | Contextualise | Mandatory | Context must include D-RCV-36 and the Epic 2 rule packages. | Context Updater |
| 3 | Define requirements | Reusable | Epic 2 v5 and FSD v6 are approved. | Intake Consolidator |
| 4 | Design experience and architecture | Reusable | ADR-011/012 and TSD v5 are approved. | Technical Specifier |
| 5 | Create backlog and specification | Mandatory | Per story. | Technical Specifier, Compliance Reviewer |
| 6 | Plan and decompose | Mandatory | Per story. | Implementation Planner, Compliance Reviewer |
| 7 | Build | Mandatory | Per story. | Implementation Builder |
| 8 | Validate | Mandatory | API, functional, Temporal replay, Drools scenarios, accessibility. | API Tester, Functional Automation Test, QA, Compliance Reviewer |
| 9 | Release | Mandatory | 31 December 2026 release gates. | Release owner, Technical Documenter |
| 10 | Operate and improve | Conditional | After go-live. | Context Updater |

## Epic 2-specific controls

| Control | Applies | Evidence |
|---|---|---|
| Temporal workflow versioning and replay | Yes | `RWB-E2-040` gate; `RWB-E2-043` pattern. |
| Rule package minimum scenarios | Yes | `rules.testcases.min=50`; `RWB-E1-073`. |
| Agent shadow-to-live promotion | Yes | D-RCV-33 grammar; `RWB-E2-028`/`029`. |
| Payment match package approval | Yes | `RWB-E2-027`, package `PAYMENT_MATCH`. |
| No new inbound load | Yes | D-RCV-35; `RWB-E2-023` removed. |
