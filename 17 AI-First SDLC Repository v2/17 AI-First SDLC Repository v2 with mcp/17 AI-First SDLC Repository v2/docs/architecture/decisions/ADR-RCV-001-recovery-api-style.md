---
title: "ADR-RCV-001 Recovery module API follows the Recovery Workbench API Specification"
description: "The recovery module exposes the API as specified in API Specification v2 (/api/recovery/v1, plain JSON, uuid ids, MSG codes), as a recorded exception to the ACE Spring Data REST / HAL rule"
---

| Field | Value |
|---|---|
| Status | Accepted by the Recovery squad, 2026-11-04 (jesniphatpukkham). ACE tech lead to acknowledge the exception |
| Resolves | CF-02 / CTX-TECH-BE-771 (`.github/contexts/backend-context.md`); backend-standards BS-3.1, BS-3.2 |
| Affects | Every Recovery Workbench story with an API; recovery frontend data access |

## Context

Two documents disagree on how the recovery module's API is built:

* **Recovery Workbench API Specification v2** (Henka solution architect, 28 Oct 2026): 144 endpoints under
  `/api/recovery/v1`, custom REST resources, plain JSON (pages as `{items, page, size, total}`), entities
  identified by uuid (275 uuid fields), errors carrying `MSG-*` codes from the Error and Message Standard v3.
  Stories, acceptance criteria and test cases are written against it.
* **ACE coding standard** (`ace-monorepo/docs/coding-standard.md`, ACE team): Spring Data REST with HAL,
  entities identified by URI never by raw id, no id-based lookup endpoints, frontend navigates with Ketting.

ACE's own modulith example, `samplemodule`, uses a plain `@RestController` returning DTOs, not HAL.

## Decision

Option B. The recovery module implements the API exactly as API Specification v2 defines it:

1. Base path `/api/recovery/v1`; resources, parameters and payloads as in the specification.
2. Plain JSON request and response bodies as specified; no HAL, no Spring Data REST repository export for
   recovery entities.
3. Entities are referenced by their uuid as specified.
4. Error responses follow the specification's error schema with `MSG-*` codes. How they are raised inside
   ACE (for example an `AceException` subclass carrying the MSG code) is decided in the implementation plan.
5. OpenAPI types still flow to the frontend through ACE's `npm run generate-openapi` / `schema.d.ts`
   (ACE rule kept). The recovery screens call these endpoints through TanStack Query, not Ketting.

All other ACE rules still apply to the recovery module (backend owns business logic, OpenAPI type safety,
module boundaries, testing).

## Consequences

* No rework of API Specification v2, stories, acceptance criteria or test cases.
* The recovery API looks different from the rest of ACE; reviewers apply this ADR, not the HAL rule, to
  code under `th.co.scb.ace.demo.<recovery module>`.
* Recovery entities must not be exported by Spring Data REST (`@RepositoryRestResource(exported = false)`
  or equivalent) so that no second, HAL-style API appears for the same data.
* The ACE coding standard needs a note pointing to this exception; that change belongs to the ACE team.
