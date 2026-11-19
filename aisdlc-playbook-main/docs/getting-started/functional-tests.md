---
id: functional-tests
title: 4.11 Test the frontend components
description: "Functional Automation Test: reproducible Playwright tests for every specified UI behaviour, or NOT_APPLICABLE with evidence."
sidebar_label: 4.11 Functional tests
---

:::note Section summary
Functional Automation Test: reproducible Playwright tests for every specified UI behaviour, or NOT_APPLICABLE with evidence.
:::

**Lifecycle phase:** 8 Validate · **Agent:** [Functional Automation Test](/agents/functional-testing) (`.github/agents/functional-automation-test.agent.md`) · **Gate:** quality and security gate (FDA, Quality Engineer)

:::warning Context reset
Start a new chat session before invoking Functional Automation Test. Use the same `RUN_ID` after the implementation review. API test results should also be reviewed before proceeding when the increment includes backend APIs.
:::

## Invoke the Functional Automation Test agent

Provide the same `RUN_ID` and the approved specification:

```text
output/<RUN_ID>/specify/spec.md
```

The agent reads `UI In Scope` and the expected UI behaviour from `spec.md`.

* When `UI In Scope: NO` and design evidence is not required, the agent creates an N/A report and
  does not launch a browser or execute tests.
* When `UI In Scope: YES`, make the plan, implementation evidence, relevant context and the running
  authorised application available. The planned `components.md` inventory is optional supplemental
  detail when present.

Provide `APP_URL` when it cannot be derived from the project configuration. Keep credentials in
named environment variables; do not paste secrets into chat.

Select **Functional Automation Test** in Copilot Chat and use a prompt such as:

```text
Read output/<RUN_ID>/specify/spec.md and determine UI scope.
If UI In Scope is NO and DESIGN_EVIDENCE_STATUS is NOT_REQUIRED, record the
functional testing activity as NOT_APPLICABLE.
If UI In Scope is YES, test every specified UI behavior using RUN_ID=<RUN_ID>
and APP_URL=<authorized-test-url> when needed.
Generate and execute reproducible Playwright tests, preserve evidence, and report coverage,
failures, and blockers. Use the implemented behavior and approved requirements as evidence;
do not modify application behavior to make tests pass.
```

The agent writes run evidence under a new attempt directory:

```text
output/<RUN_ID>/functional-tests/attempt-<n>/
```

## Review the functional test results

Confirm that:

* [ ] When `UI In Scope: YES`, every specified UI behaviour in `spec.md` is reported as tested,
  blocked or skipped with a reason. Every entry in the optional `components.md` is also reconciled
  when that file is present.
* [ ] When `UI In Scope: NO`, the report is `NOT_APPLICABLE`, records the specification evidence,
  and contains zero components and cases.
* [ ] Test cases trace to specified UI behaviour, component IDs when available, planned scenarios
  and acceptance evidence.
* [ ] Results and case counts reconcile with the JUnit output, and unavailable components or test
  gaps are explicit.
* [ ] Tests use an authorised environment and synthetic data; sensitive information is absent from
  reports and captured artefacts.
* [ ] The attempt artefacts are complete, and no prior attempt was overwritten.

:::warning Blocked, not improvised
If `spec.md` is missing, does not explicitly declare UI scope, or does not provide enough
information to identify in-scope UI behaviour, Functional Automation Test must report `BLOCKED`
rather than substituting screens or features.
:::

## After testing

After human review, the remaining validation and release steps are:

1. **Technical Documenter** with the same `RUN_ID`. It invokes the Compliance Reviewer as the
   post-test code gate before producing final documentation.
2. **Traceability Manager** for the final reconciliation of `requirement/Traceability_Matrix.md`.
3. **Code review** of the pull request by the FDE, then the quality and security gate.
4. **Release** through the [Azure deployment pipeline](/agents/azure-deploy) after release
   readiness and deployment approval.

These supporting agents are described in [Supporting agents](/agents/supporting-agents).
