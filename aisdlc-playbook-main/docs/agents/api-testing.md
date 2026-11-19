---
id: api-testing
title: A.8 API Testing (API Tester)
description: "Creates and executes tests for the APIs introduced or changed by the increment, producing evidence for the Quality Engineer."
sidebar_label: A.8 API Testing
---

:::note Section summary
Creates and executes tests for the APIs introduced or changed by the increment, producing evidence for the Quality Engineer.
:::

**Type:** Custom · **Lifecycle group:** Quality and release · **Phase:** 8 Validate · **Toolkit file:** `.github/agents/api-tester.agent.md`

The API Testing agent creates and executes tests for APIs introduced or changed by the increment. It
uses approved interface specifications, acceptance criteria and test standards to produce test
assets, results and evidence. The Quality Engineer confirms that coverage is sufficient and decides
whether the evidence can be accepted.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| The increment exposes or changes APIs (`API In Scope: YES` in `spec.md`). | `output/<RUN_ID>/specify/spec.md`, `.github/contexts/backend-context.md`, implementation evidence, optional `plan/contracts/backend-apis.json`, `API_BASE_URL` for an authorised test environment, test standards. | Playwright API test assets under the backend `test/api/`, JUnit results and reports under `output/<RUN_ID>/api-tests/attempt-<n>/` (`APT-*`), or an evidence-backed `NOT_APPLICABLE` report. | Quality Engineer validates coverage and accepts test evidence. **Gate:** quality and security gate (FDA). |

## Behaviour

* Reads API scope from `spec.md`; when `API In Scope: NO` it writes an N/A report and calls no
  endpoint.
* Covers success, validation, authorisation, error and boundary behaviour from the contract and
  implementation.
* Reports every API as tested, blocked or skipped with a reason, and reconciles optional
  `backend-apis.json` entries.
* Uses the `playwright` MCP server; credentials come from named environment variables.

## Limitations and stop conditions

* Reports `BLOCKED` when `spec.md` is missing, does not declare API scope, or does not identify the
  in-scope APIs; it never substitutes endpoints.
* Does not modify application code to make tests pass.
* Uses authorised non-production environments and synthetic data only; redacts secrets from evidence.
* Never overwrites a previous attempt.

Step-by-step: [4.10 Test the backend APIs](/getting-started/api-tests).
