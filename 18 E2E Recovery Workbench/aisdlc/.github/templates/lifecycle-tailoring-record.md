---
title: Lifecycle Tailoring Record
description: "Template recording, per lifecycle phase, whether the activity is mandatory, conditional, reusable, skippable with evidence or not applicable"
---

Complete one record per bounded increment (playbook section 2.4) in
`docs/increments/<increment-id>-tailoring.md`. For each phase of the standard lifecycle, decide
whether the activity is **Mandatory**, **Conditional**, **Reusable**, **Skippable with evidence** or
**Not applicable**, and record the evidence for every reuse or skip. Tailoring changes how the
lifecycle is traversed, not the requirement for evidence and accountability.

| Classification             | Application                                                                                         |
|----------------------------|-----------------------------------------------------------------------------------------------------|
| Mandatory                  | The activity is required for the bounded increment.                                                 |
| Conditional                | The activity is required when the conditions relevant to that phase or project are present.         |
| Reusable                   | Existing approved artefacts or outputs can be used as inputs rather than recreated.                 |
| Skippable with evidence    | The activity can be bypassed where sufficient approved evidence exists and the decision is recorded. |
| Not applicable             | The activity does not apply to the bounded increment.                                               |

---

| Increment ID | Path (Greenfield / Brownfield / Modernisation) | Prepared by | Approved by | Date |
|--------------|-------------------------------------------------|-------------|-------------|------|
|              |                                                 |             |             |      |

## Phase decisions

| # | Lifecycle phase                      | Classification | Reason | Applicable agents | Approval authority |
|---|--------------------------------------|----------------|--------|-------------------|--------------------|
| 0 | Mobilise and assess                  |                |        |                   |                    |
| 1 | Discover and frame                   |                |        |                   |                    |
| 2 | Contextualise                        |                |        |                   |                    |
| 3 | Define requirements                  |                |        |                   |                    |
| 4 | Design experience and architecture   |                |        |                   |                    |
| 5 | Create backlog and specification     |                |        |                   |                    |
| 6 | Plan and decompose                   |                |        |                   |                    |
| 7 | Build                                |                |        |                   |                    |
| 8 | Validate                             |                |        |                   |                    |
| 9 | Release                              |                |        |                   |                    |
| 10| Operate and improve                  |                |        |                   |                    |

## Skip and reuse records

One block for every phase classified **Reusable** or **Skippable with evidence**.

### Phase: `<name>`

| Field                      | Value |
|----------------------------|-------|
| Reason for skipping / reuse|       |
| Existing approved artefact |       |
| Artefact owner             |       |
| Version or link            |       |
| Approving authority        |       |
| Risk created by the bypass |       |
| Controls applied downstream|       |

## Mandatory controls confirmed

These gates apply regardless of tailoring. Tick when confirmed for the increment.

* [ ] Intake approval
* [ ] Context readiness
* [ ] Requirements approval
* [ ] Design and architecture approval
* [ ] Backlog and specification approval
* [ ] Plan approval (no implementation starts before the planning gate is satisfied)
* [ ] Pull request approval
* [ ] Quality approval
* [ ] Production readiness (no autonomous production promotion)
