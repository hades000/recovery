<!-- source: 09 Testing and quality/Recovery Workbench Non Functional Test Plan v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `09 Testing and quality/Recovery Workbench Non Functional Test Plan v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Non-functional test plan

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench non-functional test plan |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |

# 1. Tests and pass marks

| Test | How | Pass mark | When |
|---|---|---|---|
| Load | 410 simulated users at three requests a minute for one hour against the release in SIT | 95th percentile under 2 seconds; error rate under 0.5 percent | Before each release |
| Stress | Increase to twice the busiest hour | No data loss; recovers within 10 minutes when load drops | Before E2 and E8 |
| Volume | Database loaded to the end-2027 size | Case history read under 2 seconds | Before E2 |
| Batch window | Full COLLINS load and the morning chain at 2027 volume | Allocation complete by 07:00 | Before E1 and E2 |
| Resilience | Kill a service instance; fail the database over; stop the agent platform | No lost actions; agent steps fall back to rules | Before E1 and E5 |
| Restore | Restore the database and documents to a point in time | Within the ACE recovery objectives (DL11) | Before E1 |
| Security | Container and dependency scans; access tests per role; penetration test | No finding above the bank threshold | Each release; penetration before the partner portal opens |
| Accessibility | Automated scan and keyboard checks | No level A or AA failure | Each screen |

# 2. Environment and data

SIT at production sizing where the ACE team provides it; masked data scaled to the target volume. Results are recorded against the release.

# 3. Who runs them

| Test | Who |
|---|---|
| Load, stress, volume, batch | QA engineers with the ACE team |
| Resilience and restore | SCB IT with the ACE team |
| Security | SCB IT security |
| Accessibility | QA engineers |

# 4. Open targets

Recovery point and time objectives come from SCB IT under DL11.
