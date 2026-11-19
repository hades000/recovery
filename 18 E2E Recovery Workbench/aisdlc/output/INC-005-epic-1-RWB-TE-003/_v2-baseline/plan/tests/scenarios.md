# Test scenarios — RWB-TE-003

All fixtures are synthetic. The generated output is build output; the contract and access suites use
MockMvc and the generated interfaces. `TC-TE-003-09` is a live access case and stays blocked until
RWB-E1-022 and RWB-E1-037 exist.

## TC-TE-003-01 — Types generated

**Covers:** AC1, BR1, BR5.

**Given** a fixture OpenAPI file that adds `warnAt` to `Timer`
**When** the server and front-end generators run
**Then** the generated server model and TypeScript type both hold `warnAt`
**And** the service and the front end compile against them
**Evidence:** generated model/type diff; `compileJava`; `tsc --noEmit`.

## TC-TE-003-02 — Contract broken

**Covers:** AC2, BR3.

**Given** a fixture controller returns `escalationLevel` as the text `"two"`
**When** the contract tests run
**Then** the build fails
**And** the report names `getCasesCaseidTimers` and `$[0].escalationLevel`
**Evidence:** test log, report JSON.

## TC-TE-003-03 — Specification checked before generation

**Covers:** AC3, BR2.

**Given** a fixture operation with no `x-capability`
**When** the build runs
**Then** it fails at the lint step naming the operation
**And** no generated code is emitted
**Evidence:** lint log; task order.

## TC-TE-003-04 — Undocumented status fails

**Covers:** AC4, BR3.

**Given** a fixture controller returns 400 for an unknown case
**And** the fixture operation lists 200, 401, 403, 404 and 503 only
**When** the contract tests run
**Then** the build fails with `undocumented status 400 for getCasesCaseidTimers`
**Evidence:** test log, report JSON.

## TC-TE-003-05 — Current operation with no implementation fails

**Covers:** AC5, BR3.

**Given** `api/recovery-api-implementation.yaml` has `getAdminJobs` with `enforce: true`
**And** no controller method exists
**When** the build runs
**Then** it fails with `getAdminJobs has no implementation`
**Evidence:** contract log, report JSON.

## TC-TE-003-06 — Later operation is pending

**Covers:** AC6.

**Given** `postQueuesQueueidPlacements` is first in E2 and has no controller
**When** the build runs for `rwb.release=E1`
**Then** the build passes
**And** the report lists `postQueuesQueueidPlacements` as pending
**Evidence:** report JSON.

## TC-TE-003-07 — Front end cannot use a removed field

**Covers:** AC7, BR1.

**Given** a fixture spec removes `legalHold` from `Case`
**And** a fixture screen reads `legalHold`
**When** the front-end type check runs
**Then** it fails naming the file and the line
**Evidence:** `tsc --noEmit` log; live spec keeps `legalHold`.

## TC-TE-003-08 — Endpoint skips its access check

**Covers:** AC8, BR4.

**Given** a fixture controller implements the operation without the access check
**When** the access test runs with `RW-REFADM`, which holds no Case record right
**Then** the operation answers 200
**And** the build fails with `access not enforced for getCasesCaseidTimers`
**Evidence:** access log; report JSON.

## TC-TE-003-09 — Live access case

**Covers:** Access, BR4.

**Given** the live `RW-REFADM` role and the permission matrix seed
**When** the role calls `getCasesCaseidTimers`
**Then** the response is 403, `application/problem+json`, `messageCode = MSG-P4-002`
**Evidence:** **BLOCKED** until RWB-E1-022 and RWB-E1-037; the harness and fixture-level AC8 are built
now. Do not record a mocked role as a pass.

## Coverage

| AC | Tests |
|---|---|
| AC1 | TC-TE-003-01 |
| AC2 | TC-TE-003-02 |
| AC3 | TC-TE-003-03 |
| AC4 | TC-TE-003-04 |
| AC5 | TC-TE-003-05 |
| AC6 | TC-TE-003-06 |
| AC7 | TC-TE-003-07 |
| AC8 | TC-TE-003-08 |
| Access | TC-TE-003-09 (blocked) |
