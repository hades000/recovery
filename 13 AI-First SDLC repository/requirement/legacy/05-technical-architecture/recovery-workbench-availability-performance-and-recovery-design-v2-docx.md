<!-- source: 05 Technical architecture/Recovery Workbench Availability Performance and Recovery Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Availability Performance and Recovery Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Availability, performance and recovery design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench availability, performance and recovery design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC 25010 |

# 1. Service levels

| Item | Target | Status |
|---|---|---|
| Availability in business hours | 99.9 percent | Proposed, DL11 |
| Availability outside business hours | 99.5 percent, excluding the change window | Proposed, DL11 |
| Screen response | Under 2 seconds at the 95th percentile | Proposed, DL11 |
| Rule evaluation | Under 300 milliseconds | Proposed, DL11 |
| Agent response | 60 seconds, then the rule result | Proposed, DL11 |
| COLLINS load complete | By 07:00 | Proposed |
| Recovery point objective | The ACE value | Open, DL11 |
| Recovery time objective | The ACE value | Open, DL11 |

# 2. Load the design carries

| Measure | Value |
|---|---|
| Open cases at go-live | About 23,600 |
| Open cases at the end of 2027 | About 26,500 |
| Named users | 1,234 |
| Online in the busiest hour | About 410 |
| Requests a second in the busiest hour | About 21 |
| Documents by the end of 2031 | About 5.8 million, 2.8 TB |
| Decision log and ledger by the end of 2031 | About 36 GB |

# 3. Scaling

- The ACE service scales out on the shared AKS clusters by CPU and request rate; the recovery module adds no separate service.

- PostgreSQL flexible server, zone redundant; read queries for reports go to the data lake copy, not the live database.

- Large tables (decision log, ledger, documents index) are partitioned by month.

- Documents are in Blob storage; the database holds only the index and extracted fields.

- Batch work runs outside business hours where it can: loads before 07:00, reconciliation after the load, retention at night.

# 4. Backup and restore

| Store | Backup | Restore test |
|---|---|---|
| ACE database | Point-in-time restore on the ACE pattern | Before the first production release, then each quarter |
| Document storage | Bank backup service on the bank schedule (DL27) | Before the first production release and at each release (NFR-071) |
| Configuration and reference data | Versioned in the database and in the load files | With the database restore |

# 5. Degraded modes

| Failure | What still works |
|---|---|
| COLLINS load late | Every screen with the last loaded data and its date; no new cases from stale data |
| Agent platform down | Every decision on rules |
| Outbound system down | Everything; outbound work waits in the outbox |
| Partner gateway down | Bank staff record partner results |
| Document storage down | Case work without opening documents; uploads wait |

# 6. Tests

- Load test at the busiest-hour volume before each release (RWB-TE-009).

- Failover test of the database before the first production release.

- Restore test of documents and the database before the first production release.

- Agent outage test: the case routes on the rule result.
