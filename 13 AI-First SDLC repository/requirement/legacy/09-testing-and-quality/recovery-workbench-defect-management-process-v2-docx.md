<!-- source: 09 Testing and quality/Recovery Workbench Defect Management Process v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `09 Testing and quality/Recovery Workbench Defect Management Process v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Defect management process

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench defect management process |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |

# 1. Severity

| Severity | Meaning | Example | Fix by |
|---|---|---|---|
| 1 Critical | A decision is wrong, data is lost or exposed, or the service is down | Approval accepted above the limit; personal data shown unmasked | Same day; release blocked |
| 2 High | A main path does not work and there is no workaround | Allocation does not run | Before the release |
| 3 Medium | A path fails with a workaround | Filter returns extra rows | Agreed date |
| 4 Low | Cosmetic or wording | Label misaligned | Backlog |

# 2. Lifecycle

- Raise: anyone raises the defect on the board with steps, expected and actual result, environment and story key.

- Grade: the QA engineer sets severity; the product owner confirms severity 1 and 2.

- Assign: the tech lead of the owning module assigns it the same day.

- Fix: the developer fixes it with a test that fails before and passes after.

- Retest: the QA engineer retests in the environment where it was found.

- Close: closed when the retest passes; reopened if it returns.

# 3. Rules

- No personal data in a defect record or screenshot.

- A defect found in UAT is also added to the regression suite.

- A severity 1 or 2 defect open at the go decision stops the release unless its flag is off.

- Rule defects are fixed by a new rule version, not by code.

# 4. Measures

| Measure | Meaning |
|---|---|
| Defects found in UAT | Defects per release found after SIT |
| Age of open defects | Days open by severity |
| Reopen rate | Share of fixed defects reopened |
