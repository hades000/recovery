---
id: api-tests
title: 4.10 Test the backend APIs
description: "API Tester: generate and execute the Playwright API suite for every API in spec.md, or record NOT_APPLICABLE with evidence."
sidebar_label: 4.10 API tests
---

:::note Section summary
API Tester: generate and execute the Playwright API suite for every API in spec.md, or record NOT_APPLICABLE with evidence.
:::

**Lifecycle phase:** 8 Validate · **Agent:** [API Tester](/agents/api-testing) (`.github/agents/api-tester.agent.md`) · **Gate:** quality and security gate (FDA, Quality Engineer)

:::warning Context reset
Start a new chat session before invoking the API Tester. Start only after the implementation evidence has been reviewed and the backend is available in an authorised test environment.
:::

## Invoke the API Tester agent

Provide the same `RUN_ID` and the approved specification:

```text
output/<RUN_ID>/specify/spec.md
```

The API Tester reads `API In Scope` and the API behaviour from `spec.md`.

* When `API In Scope: NO`, the agent creates an N/A report and does not generate tests, launch a
  browser or call an endpoint.
* When `API In Scope: YES`, make `.github/contexts/backend-context.md`, the implementation evidence
  and the API test environment available. The planned `backend-apis.json` contract is optional
  supplemental detail when present.

Provide `API_BASE_URL` when it cannot be derived from the project context. Keep credentials in
named environment variables; do not paste secrets into chat.

Select **API Tester** in Copilot Chat and use a prompt such as:

```text
Read output/<RUN_ID>/specify/spec.md and determine API scope.
If API In Scope is NO, record the API testing activity as NOT_APPLICABLE.
If API In Scope is YES, test every API specified in spec.md using RUN_ID=<RUN_ID>
and API_BASE_URL=<authorized-test-url> when needed.
Generate and execute the Playwright API suite, preserve evidence, and report failures,
contract drift, coverage gaps, and blockers. Do not modify application code to make tests pass.
```

The agent writes run evidence under a new attempt directory:

```text
output/<RUN_ID>/api-tests/attempt-<n>/
```

## Review the API test results

Confirm that:

* [ ] When `API In Scope: YES`, every API in `spec.md` is reported as tested, blocked or skipped
  with a reason. Every entry in the optional `backend-apis.json` is also reconciled when that file
  is present.
* [ ] When `API In Scope: NO`, the report is `NOT_APPLICABLE`, records the specification evidence,
  and contains zero APIs, controllers and cases.
* [ ] Test cases cover applicable success, validation, authorisation, error and boundary behaviour
  from the contract and implementation.
* [ ] Contract drift, failures, skipped cases and blockers are explicit, and test counts reconcile
  with the JUnit results.
* [ ] Testing used an authorised non-production environment and synthetic data, with secrets and
  sensitive data redacted from the evidence.
* [ ] The attempt artefacts are complete, and no prior attempt was overwritten.

:::warning Blocked, not improvised
If `spec.md` is missing, does not explicitly declare API scope, or does not provide enough
information to identify in-scope APIs and expected behaviour, the API Tester must report `BLOCKED`
rather than substituting endpoints.
:::

After human review, start **Functional Automation Test** manually with the same `RUN_ID`.

Next: [4.11 Test the frontend components](/getting-started/functional-tests).
