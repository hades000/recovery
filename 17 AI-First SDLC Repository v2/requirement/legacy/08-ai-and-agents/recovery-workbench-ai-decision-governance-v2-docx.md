<!-- source: 08 AI and agents/Recovery Workbench AI Decision Governance v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `08 AI and agents/Recovery Workbench AI Decision Governance v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

AI decision governance

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench aI decision governance |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts |

# 1. Principles

- A model or agent decides alone only at the autonomy level the strategy and model committee has approved for that step.

- Every automated or advised decision is recorded with its inputs, versions, reasons and outcome.

- Every decision can be explained to the customer, the business, audit and the regulator.

- Any decision can be challenged and reversed by a person with the authority for it.

- If the AI does not answer or fails a guardrail, the rule result is used.

# 2. Recording

| What is recorded | Where |
|---|---|
| Inputs used, by reference with their business date | Decision log |
| Rule, model, agent and prompt versions | Decision log |
| Recommendation and reasons | Decision log |
| Autonomy level of the step | Decision log |
| Who decided, or that the agent decided within its band | Decision log |
| Override and its coded reason | Decision log |

# 3. Explaining

| Audience | What they receive | How |
|---|---|---|
| Case owner | The recommendation with its top reasons and the expected return by route | Decision screen |
| Customer | The outcome and the main reasons in plain words, on request or where a letter requires it | Letter or contact center |
| Audit and regulator | The full entry with versions and inputs | Decision log query and export |

# 4. Reviewing

| Review | Who | How often |
|---|---|---|
| Sample of agent-decided cases at L2 and above | Conduct and QA officer | Monthly |
| Acceptance, overrides and fallbacks | Risk and model risk officer | Monthly |
| Outcomes against rule-only decisions | Center of excellence | Quarterly |
| Autonomy step-ups | Strategy and model committee | On request with results |

# 5. Challenging and reversing

- A customer complaint about a decision raises X1 and pauses the stage clock.

- The complaint officer reviews the decision log entry.

- If the decision is wrong, a person with the authority records a correcting decision that names the original (R-UNI-24).

- If the cause is the agent or the rule, the center of excellence raises a change; Risk may lower the autonomy level at once.

- Lowering an autonomy level is a reference data change that takes effect immediately.

# 6. Autonomy levels

| Level | What the agent does | What a person does |
|---|---|---|
| L0 | Nothing. The rule decides | Everything |
| L1 | Recommends, with its reasons | Decides. Every decision starts here after a shadow run |
| L2 | Acts inside a narrow band | Reviews a sample and the exceptions |
| L3 | Acts across the decision | Reviews by exception |
| L4 | Acts and closes | Monitors the measures |
