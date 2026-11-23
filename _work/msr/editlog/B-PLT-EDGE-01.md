# Edit log — WP B-PLT-EDGE-01 (RWB-PLT-EDGE, legacy N001, N006, N007 and NF-07)

Tools and model: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date: 22 November 2026.

Execution mode: fanout 5. Four `aisdlc-msr-worker` task subagents were dispatched in one message, one per legacy key (N001 with both its stories, N006, N007, NF-07). The NF-07 subagent closed on a transport error before writing any file; the WP executor then wrote that story, its fragment and its two rows from the same brief, so no task was left unfinished and nothing was written twice.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EDGE Edge and gateway/RWB PLT N001 APP gateway-bff routes and composite screens v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EDGE Edge and gateway/RWB PLT N001 CON gateway-bff route contract - contract v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EDGE Edge and gateway/RWB PLT N006 INF Redis session store for gateway-bff - infrastructure v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EDGE Edge and gateway/RWB PLT N007 INF Partner gateway in the DMZ (FAPI 2.0) - infrastructure v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EDGE Edge and gateway/RWB PLT NF07 INF Airflow edge integration - infrastructure v1.md
- _work/msr/fragments/RWB-PLT-N001-APP.json
- _work/msr/fragments/RWB-PLT-N001-CON.json
- _work/msr/fragments/RWB-PLT-N006-INF.json
- _work/msr/fragments/RWB-PLT-N007-INF.json
- _work/msr/fragments/RWB-PLT-NF07-INF.json
- _work/msr/gaps/B-PLT-EDGE-01.jsonl
- _work/msr/assumptions/B-PLT-EDGE-01.jsonl
- _work/msr/editlog/B-PLT-EDGE-01.md

## Counts

| Item | Count | Detail |
|---|---|---|
| Stories | 5 | one per story line of the WP; 19 sections and 20 metadata rows each |
| Fragments | 5 | the WP step-8 key set, `prd_ref` Pending (C1), `acs` and `tcs` empty because all five are new platform stories with no legacy AC or TC |
| Acceptance criteria | 31 | all tagged (new, D-RCV-60): N001-CON 6, N001-APP 6, N006-INF 6, N007-INF 7, NF07-INF 6 |
| Test cases | 33 | with the Level column: N001-CON 6, N001-APP 7, N006-INF 6, N007-INF 7, NF07-INF 7 |
| Candidate gap rows (CG) | 5 | one combined row per story |
| Candidate assumption rows (ASM) | 5 | one per gap, each linked to its CG id |

The per-key numbering of the WP parallel clause is used: `GAP-1393`, `-N001-2`, `-N006-1`, `-N007-1`, `-NF-07-1`, and the matching `ASM-` ids. Each story cites only its own pair, so no citation resolves to another story's row.

## What each story holds

| Story | Deliverable | Contract and dependencies |
|---|---|---|
| RWB-PLT-N001-CON | OpenAPI 3.1 of the gateway-bff public route surface (case screen, four tabs, my tasks, inbox stream), AsyncAPI 3.0 of the five consumed events, the route table, the error mapping, a route fake and a contract test | 12.1 PLT routes with the downstream owner of each; 12.2 the seven owner operations; 12.4 ApprovalRequested, TimerBreached, AccessPolicyChanged, DoaLimitChanged, RulePackageInForce; no table, no topic of its own |
| RWB-PLT-N001-APP | Spring Cloud Gateway implementation: session filter over Redis, per-request user JWT from ACE Common, parallel composition and merge, one-hop tabs, 2 s timeout and breaker per downstream, RFC 9457 errors, inbox push and cache refresh, tracing and metrics | Implements the N001-CON surface; Redis sessions provisioned by N006; partners bypass it through N007 |
| RWB-PLT-N006-INF | The Redis session store: private access, TLS, credential in Key Vault, sessions-only keyspace with the 15-minute idle TTL, capacity and failover, dashboard and alerts, rotation and rebuild runbook | Sessions only, no business data, no `rwb_*` table, no REST, no event |
| RWB-PLT-N007-INF | The partner gateway in the DMZ: separate zone, FAPI 2.0 (PAR, mTLS sender-constrained tokens, strong client authentication), MFA, scope to own cases, client and certificate lifecycle, WAF and rate limits, SOC logging, pen-test gate | Exposes the six partner-portal operations of rwb-partner (S9) and rwb-debtsale (S6) and publishes no operation of its own |
| RWB-PLT-NF07-INF | The Airflow edge: service principal and network path, business-date-ready and wait for DailyCaseRun, the two file windows, the report extracts, cutover and backfill, retries and alerting, runbook | Consumes the rwb-source-data, rwb-integration and rwb-reporting operations; holds no schema, topic or task queue |

Every value is copied from Architecture v5, the Ownership Map, the BRD extracts or the template. The public path shape of the tabs and the inbox stream (N001), the store settings (N006), the FAPI client authentication and token settings (N007) and the Airflow identity, retry and wait settings (NF-07) are stated as the read of their assumption, with the placeholder where the value is still open; no business value is invented.

## Verification

- WP quick check `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-EDGE-01 --quick`: C02, C03, C05, C12, C13 and C18 all PASS.
- Additional local verification (a read-only audit script kept in the scratch log area): all 20 metadata rows and their values match the WP JSON for every story; the 19 headings are complete and in order; 12.1 to 12.9 exist in every story; every Scenario line carries the (new, D-RCV-60) tag; every fragment has the full 28-key set and points at its WP file; every CG and ASM citation resolves to a row in the two registers; every story id cited in a traceability table exists in `split_plan.json`; no BOM, no U+FFFD, UTF-8 throughout; no person name, no email address and no tracker reference.
