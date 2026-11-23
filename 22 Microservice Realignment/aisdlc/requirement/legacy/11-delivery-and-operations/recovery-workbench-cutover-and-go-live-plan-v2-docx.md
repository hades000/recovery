<!-- source: 11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Cutover and go-live plan

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench cutover and go-live plan |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |

# 1. How releases go live

Each monthly release goes live in the change window agreed with SCB IT (DL34). The first release, 30 November 2026, also starts the daily loads and the case list; later releases add modules behind feature flags and switch them on per team.

# 2. Sequence for each release

| When | Step | Who |
|---|---|---|
| Friday before | Go decision on the SIT and UAT exits; flags for unfinished work confirmed off | Release owner with the product owner and application owner |
| Release day minus 1 | Reference data, rules and templates for the release loaded with their valid from date | Reference data administrator |
| Release day | Deploy the tag to production in the change window | ACE team |
| Release day | Smoke test: sign-in per role, case list, one decision, one notice | QA engineers with business testers |
| Next morning | First loads under the new release; reconciliation checked | Data steward |
| First week | Floor support for the teams that receive real users | Business analysts, business lead |
| Four weeks after | Benefit check (G6) | Product owner |

# 3. Rehearsal

Each release is rehearsed in UAT: the deploy, the reference data load, the smoke test and the rollback. The first release is rehearsed twice.

# 4. Rollback

- Switch the feature flags for the release off.

- If a flag does not cover the fault, redeploy the previous tag.

- Reload the previous reference data versions if they changed.

- Decisions taken under the new release stay in the decision log; corrections are new entries.

# 5. Who decides to go

The release owner in the ACE team decides with the product owner and the application owner. A severity 1 or 2 defect open without a flag stops the release.

# 6. First release specifics

| Item | Plan |
|---|---|
| Case list | Built from the first COLLINS load; reconciled to the inventory report before it is shown |
| Spreadsheets | Kept in parallel for two weeks; retired after ten clean days |
| Access | Administration roles only; business roles from Epic 2 (DL39) |
| Documents | Store and OCR live; bulk intake of open-case documents starts |

# 7. Open decisions

| Decision | What is needed |
|---|---|
| DL12 | Which legacy systems are kept |
| DL34 | The release window |
