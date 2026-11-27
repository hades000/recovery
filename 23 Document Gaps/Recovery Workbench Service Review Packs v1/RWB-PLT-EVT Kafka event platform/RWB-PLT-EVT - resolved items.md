# RWB-PLT-EVT Kafka event platform - resolved items

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-PLT-N002-INF | R-07297 | DOR-RWB-PLT-N002-INF-16 | header | Definition of Ready item 16 Size: Fail | Size row added to the header: the squad sizes the story at refinement. |
| RWB-PLT-N002-INF | R-18745 | DOR-RWB-PLT-N002-INF-20 | 11 | Definition of Ready item 20 Reference data: Partial | Section 11 now states the story reads no list or parameter (BR8) and uses neither parameters nor DP-06 and DP-07. |
| RWB-PLT-N002-INF | R-18747 | DOR-RWB-PLT-N002-INF-7 | 11 | Definition of Ready item 7 Data: Partial | BR Field ID column added to section 11; each of the 20 rows maps to BR1 (topic ownership) and BR2 (settings). |
| RWB-PLT-N002-INF | R-22912 | GAP-1666 | 8 | The retry limit of an event and of a call is stated differently in the BRD and in Architecture v5 | BR3 now states the Kafka retry path, the outbound exception-queue retries and the Temporal 10-attempt policy as separate paths. |
| RWB-PLT-N002-INF | R-29073 | GAP-0125 | 8 | The shared topic rwb.decision-record.v1 has no settings of its own in any source | BR2 now states that the shared topic rwb.decision-record.v1 has the same settings as the service topics: 12 partitions, replication factor 3, 7-day retention and key caseId. |
| RWB-PLT-N008-INF | R-07328 | DOR-RWB-PLT-N008-INF-21 | header | Definition of Ready item 21 Contract published: Fail | Contract dependencies now states no contract story and no CON dependency apply to this story. |
| RWB-PLT-N008-INF | R-07329 | DOR-RWB-PLT-N008-INF-22 | header | Definition of Ready item 22 Fake published: Fail | Contract dependencies now states no contract fake applies, since the story builds against no contract. |
| RWB-PLT-N008-INF | R-07330 | DOR-RWB-PLT-N008-INF-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Contract dependencies now states no contract version applies, so no contract version is built against. |
| RWB-PLT-N008-INF | R-11855 | CG-ALL-1281 | 13 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | Replaced the recovery_svc login name in the Pattern application paragraph with 'legacy service login'. No other occurrence exists. |
| RWB-PLT-N008-INF | R-18767 | DOR-RWB-PLT-N008-INF-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Added AC7 covering BR1 to BR8 in section 7 and TC-PLT-N008-INF-07 in section 16 |
| RWB-PLT-N008-INF | R-23291 | GAP-0129 | 11 | No registry subject and no JSON Schema is named per event type | Section 11 now states the BR1 subject rule, registration before first publish, and that subject and version are recorded in the next catalogue version. |
| RWB-PLT-N008-INF | R-31807 | NEWAC-RWB-PLT-N008-INF-AC7 | 7, 16 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 scenario added in section 7 and TC-PLT-N008-INF-07 added in section 16 |
| RWB-PLT-N012-INF | R-07353 | DOR-RWB-PLT-N012-INF-16 | section header | Definition of Ready item 16 Size: Fail | Size row states Not specified in the source documents |
| RWB-PLT-N012-INF | R-07356 | DOR-RWB-PLT-N012-INF-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version in the sources: the PRD PLT Platform v1 and the findings file name no version, and no N012-CON story exists. Header row now says Not specified. |
| RWB-PLT-N012-INF | R-18797 | DOR-RWB-PLT-N012-INF-3 | 7 | Definition of Ready item 3 Acceptance criteria: Partial | When steps added to AC1, AC4 and AC6 |
| RWB-PLT-N012-INF | R-18798 | DOR-RWB-PLT-N012-INF-4 | 8 | Definition of Ready item 4 Business rules: Partial | Rule coverage line maps BR1 to BR8 to AC1 to AC6 |
| RWB-PLT-N012-INF | R-18799 | DOR-RWB-PLT-N012-INF-7 | 11 | Definition of Ready item 7 Data: Partial | BR Field ID column added; all six rows mapped |
| RWB-PLT-N012-INF | R-21892 | GAP-0649 | 11 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | Infrastructure values recorded as deployment values under GAP-0649 |
| RWB-PLT-N012-INF | R-29666 | ACR-RWB-PLT-N012-INF-AC1 | 7 | AC1 | When line added: the provisioning of the Blob account completes |
| RWB-PLT-N012-INF | R-29667 | ACR-RWB-PLT-N012-INF-AC4 | 7 | AC4 | When line added: an application reads a secret from the Key Vault |
| RWB-PLT-N012-INF | R-29668 | ACR-RWB-PLT-N012-INF-AC6 | 7 | AC6 | When line added: a connection reaches the Blob account, the Key Vault or the SFTP service |
