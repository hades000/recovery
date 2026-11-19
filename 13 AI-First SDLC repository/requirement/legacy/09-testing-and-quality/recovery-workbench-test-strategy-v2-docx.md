<!-- source: 09 Testing and quality/Recovery Workbench Test Strategy v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `09 Testing and quality/Recovery Workbench Test Strategy v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Test strategy

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench test strategy |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |

# 1. Levels

| Level | What it covers | Who | Where | When | Exit |
|---|---|---|---|---|---|
| Unit | Every service method and rule evaluation | Developer | DEV and the pipeline | Every commit | 80 percent line coverage on new code |
| Rule table | Each rule row against its test case | Developer with the analyst | Pipeline | Every commit and every rule version | Every row passes |
| Integration | Modules with a real PostgreSQL database | Developer | Pipeline | Every pull request | All pass |
| API contract | Requests and responses against the OpenAPI file | Developer | Pipeline | Every pull request | All pass |
| System | Stories end to end against the SCB test systems | QA engineer | SIT | Rolling, then the SIT week | Every test case for the release passes; no open severity 1 or 2 |
| Regression | The regression suite | QA engineer | SIT | Each release | All pass |
| Non-functional | Performance, resilience, security | QA with SCB IT | SIT | Before each release | Targets in the NFR specification |
| Accessibility | Automated scan and keyboard checks | QA engineer | SIT | Each screen | No level A or AA failure |
| User acceptance | Business scripts | Business testers | UAT | UAT week | Scripts signed by the business lead |

# 2. Environments

| Environment | Data | Use |
|---|---|---|
| DEV | Synthetic only | Developer and rule tests |
| SIT | Masked copies from the PII service | System, regression, non-functional |
| UAT | Masked copies | Business acceptance |

# 3. Entry and exit

| Gate | Entry | Exit |
|---|---|---|
| SIT | Release tag built; stories done in DEV; test data loaded | Every test case passes; no open severity 1 or 2; severity 3 with an agreed fix date |
| UAT | SIT exit met; scripts walked through with the testers | Scripts signed by the business lead; open defects accepted or behind a flag |
| Release | SIT and UAT exits | Go decision by the release owner |

# 4. Test data

Synthetic in DEV; masked copies in SIT and UAT; no production data below production. The test data plan sets the data each test needs.

# 5. Who tests what

| Who | Tests |
|---|---|
| Developers | Unit, rule table, integration, contract |
| QA engineers | System, regression, accessibility, non-functional with SCB IT |
| Business testers | During the build with the squads; UAT scripts |
| SCB IT security | Penetration test before the partner portal opens |
| Role owners | Access tests per role |

# 6. Traceability

Every test case names its story and acceptance criterion or its rule ID. The requirements traceability matrix links requirement, feature, story, specification section and test.

# 7. Defects

Defects follow the defect management process: severity, owner, fix and retest. A release goes with no open severity 1 or 2 defect.
