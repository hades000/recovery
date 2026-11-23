<!-- source: 05 Technical architecture/Recovery Workbench API Specification v4.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `05 Technical architecture/Recovery Workbench API Specification v4.html`  
> **Converted from:** HTML

Recovery Workbench API specification**141 endpoints**In 16 groups, under /api/recovery/v1 in the ACE service**172 schemas**Records from the logical data model, requests, pages and the problem response**One access check**Role, capability area, right and scope on every endpoint**OpenAPI 3.1**The YAML file is the contract; types are generated from it

## Rules every endpoint follows

| Rule | Detail |
|---|---|
| Sign-in | Bearer token from Entra ID through the ACE front end; partners through the external gateway (DL03) |
| Access | The endpoint declares its capability area and right; scope filters every query; out of scope returns 404 |
| Approvals | Approval endpoints check the approval level, the delegation of authority limit and maker and checker |
| Decision log | Every state change writes its decision log entry first; a failed write returns 503 and nothing changes |
| Concurrency | Records carry a version; a stale version returns 409 with MSG-GEN-004 |
| Idempotency | POST requests carry an Idempotency-Key header; a repeat returns the first result |
| Paging | page and size query parameters; size up to 100 |
| Dates | ISO 8601; dates in the Asia/Bangkok business day |
| Personal data | Fields marked x-personal-data are masked unless the role may see them |
| Errors | application/problem+json with the message code and the Thai and English text from the error and message standard |
