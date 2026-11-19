<!-- source: 05 Technical architecture/Recovery Workbench Audit and Logging Design v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Audit and Logging Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Audit and logging design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench audit and logging design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts, C4 component view |

# 1. The records

| Record | What it holds | Form | Where | Read by |
|---|---|---|---|---|
| Decision log | Every decision: inputs, rule and model versions, recommendation, approver, action | Append only, hash chained, one entry per decision | ACE database; nightly copy to the data lake | Internal audit, Risk, center of excellence |
| Interaction ledger | Every contact, letter, promise, payment and hand-over | Append only, one entry per interaction | ACE database | Case owners in scope; Conduct and QA |
| Access log | Sign-ins, refusals, grants, removals, break-glass, versions in force | Append only | ACE database, inside the decision log store | Application owner, security administrator, Compliance, internal audit |
| ACE audit log | Every change made through the service | ACE pattern | ACE logging | Security administrator, internal audit |
| PII log | Every read and unmask of a personal field | Event per read | PII Kafka | Compliance, internal audit |
| SOC log | Security events | Event per incident | SCB security operations | Security operations |
| Application logs | Errors, warnings and traces with no personal data | Structured JSON | Log Analytics | Platform administrator, squads |

# 2. The decision log entry

| Field | Meaning |
|---|---|
| entry_id, case_id | The entry and its case |
| decision_code | D1 to D9, a sub-decision or a deviation |
| rule_id, rule_version | The rule that fired and its version |
| model_version, agent_version, prompt_version | Where a model or agent took part |
| inputs | References to the data and its business date, not copies of personal data |
| recommendation, reasons | What was proposed and why |
| decided_by, approval_level, limit_applied | Who decided, at which level, under which limit |
| action | What the Workbench did |
| previous_hash, hash | The chain that shows no entry has been changed |
| corrects_entry_id | Set when the entry corrects an earlier one (R-UNI-24) |

# 3. Tracing an action end to end

- Every request carries a trace ID from the front end through the service, the outbox and the outbound file.

- The decision log entry stores the trace ID.

- The interaction ledger entry stores the decision log entry ID where a decision caused it.

- Outbound files carry the case number and the entry ID, so a notice in WIN can be traced to its decision.

- Internal audit searches by case, rule, approver or date on the decision log query screen and exports with masking.

# 4. Integrity

- The decision log, the interaction ledger and the access log accept inserts only. Migrations cannot update or delete their rows.

- A daily job checks the hash chain and reports a break to Compliance the same day.

- A correction is a new entry that names the entry it corrects; the original stays.

- A failed write to the decision log stops the action; a failed write to the ledger raises an incident.

# 5. Retention

| Record | Retention |
|---|---|
| Decision log | Set by Compliance (DL26); proposed as the life of the case plus the bank records period |
| Interaction ledger | Set by Compliance, separately from the decision log (DL26) |
| Access log | Per the bank retention schedule (DL26) |
| Application logs | 90 days in Log Analytics, then archived |

# 6. What is never logged

- Clear national ID or passport numbers.

- Personal fields in application logs, traces or agent prompts.

- Secrets, tokens or keys.
