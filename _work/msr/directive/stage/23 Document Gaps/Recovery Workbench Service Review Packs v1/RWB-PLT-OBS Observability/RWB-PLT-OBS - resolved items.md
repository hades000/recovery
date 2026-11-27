# RWB-PLT-OBS Observability - resolved items

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-PLT-E1056-OPS | R-07219 | DOR-RWB-PLT-E1056-OPS-16 | header | Definition of Ready item 16 Size: Fail | Added Size row to the header table, set by the squad at refinement. |
| RWB-PLT-E1056-OPS | R-07222 | DOR-RWB-PLT-E1056-OPS-23 | Header | Definition of Ready item 23 Contract version fixed: Fail | Added Contract version row to the header table: 4.0.0, from API Specification v4.yaml info.version, with server path /api/recovery/v1. |
| RWB-PLT-E1056-OPS | R-18633 | DOR-RWB-PLT-E1056-OPS-15 | header | Definition of Ready item 15 INVEST: Partial | Size row now states that a story sized Small fits within two weeks |
| RWB-PLT-E1056-OPS | R-18634 | DOR-RWB-PLT-E1056-OPS-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Added a note after the section 18 table listing DL10 and DL11 as open, each with its assumptions |
| RWB-PLT-E1056-OPS | R-18636 | DOR-RWB-PLT-E1056-OPS-24 | 12.4 | Definition of Ready item 24 Ownership stated: Partial | Added an Owner column to the events consumed table, set to P1 rwb-source-data for both events |
| RWB-PLT-E1056-OPS | R-18637 | DOR-RWB-PLT-E1056-OPS-4 | 7 | Definition of Ready item 4 Business rules: Partial | AC10 added for BR8 in section 7; test row TC-E1-056-11 in section 16 |
| RWB-PLT-E1056-OPS | R-18638 | DOR-RWB-PLT-E1056-OPS-7 | 7 | Definition of Ready item 7 Data: Partial | AC6 and AC9 read the rwb-source-data contract; AC11 reads it too |
| RWB-PLT-E1056-OPS | R-18640 | DOR-RWB-PLT-E1056-OPS-9 | 14 | Definition of Ready item 9 Messages: Partial | Section 14 texts of MSG-P2-005, MSG-P2-006 and MSG-P1-001 copied from Error and Message Standard v4. |
| RWB-PLT-E1056-OPS | R-22147 | GAP-1001 | find it | The business-hours window, the deployment slot and the alert thresholds of the document intake pipeline are not specified | Story already registers schedule from environment values and marks thresholds and slot provisional; values fixed at wave 1 entry check. |
| RWB-PLT-E1056-OPS | R-22198 | GAP-1015 | find it | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | Schedule ID fixed by release, overlap SKIP, one-run catch-up; missing identifiers as placeholders, confirmed before wave 1 by platform admin and message owner. |
| RWB-PLT-E1056-OPS | R-23194 | GAP-1419 | find it | The job-run record, the run book home and the catalogue-to-run join are not specified after the split | Solution architect publishes job-run record, run book path, panels and 16-row mapping at wave 0 entry check; no values invented here. |
| RWB-PLT-E1056-OPS | R-23196 | GAP-2044 | find it | No source names the owner of a per-service dashboard or alert rule as a team | Per-service dashboard and alert owner is the Ownership Map v1 service code; DevOps team is suggested owner; baseline by RWB-PLT-N005-OPS in wave 0. |
| RWB-PLT-E1056-OPS | R-26647 | CG-ALL-1464 | 14 | MSG-P2-006 text differs from the Error and Message Standard v4 | MSG-P2-006 text copied from Error and Message Standard v4. |
| RWB-PLT-E1056-OPS | R-26648 | CG-ALL-1465 | 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | MSG-P1-001 text copied from Error and Message Standard v4. |
| RWB-PLT-E1056-OPS | R-26651 | CG-ALL-1483 | 15 | SCR-44 has no empty, loading, error, no access state in the story | SCR-44 states empty, loading, error and no access marked Not specified in the source documents; spec v1 lacks them. |
| RWB-PLT-E1056-OPS | R-29658 | ACR-RWB-PLT-E1056-OPS-AC6 | 7 | AC6 | AC6 Given now reads the rwb-source-data contract (DP-01, DP-05) instead of an ACE view. |
| RWB-PLT-E1056-OPS | R-29659 | ACR-RWB-PLT-E1056-OPS-AC8 | 7 | AC8 | AC8 vague wording replaced: may became can; the no-change Then names the values that must hold. |
| RWB-PLT-E1056-OPS | R-29660 | ACR-RWB-PLT-E1056-OPS-AC9 | 7 | AC9 | AC9 Given now reads through the rwb-source-data contract (DP-01, DP-05), not directly from the ACE view. |
| RWB-PLT-E1056-OPS | R-31763 | NEWAC-RWB-PLT-E1056-OPS-AC10 | 7 | AC10: §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Added AC10 for BR8 in section 7; test row TC-E1-056-11 in section 16. Proposed test level is not specified in the source. |
| RWB-PLT-E1056-OPS | R-31764 | NEWAC-RWB-PLT-E1056-OPS-AC11 | 7, 16 | AC11: a consumed call fails or does not answer (no criterion covers a failed call) | Added AC11 for a failed or unanswered consumed call in section 7; test row TC-E1-056-12 in section 16. Proposed test level is not specified in the source. |
| RWB-PLT-N005-OPS | R-07312 | DOR-RWB-PLT-N005-OPS-16 | Header | Definition of Ready item 16 Size: Fail | Added Size row: not set, squad sizes at refinement |
| RWB-PLT-N005-OPS | R-07313 | DOR-RWB-PLT-N005-OPS-21 | Header | Definition of Ready item 21 Contract published: Fail | The header table already reads Contract dependencies: None. No RWB-PLT-N005-CON story or CON dependency exists in the sources, so none is added. No edit needed. |
| RWB-PLT-N005-OPS | R-18755 | DOR-RWB-PLT-N005-OPS-1 | 1 | Definition of Ready item 1 Story: Partial | Role changed from platform engineer to DevOps engineer |
| RWB-PLT-N005-OPS | R-18756 | DOR-RWB-PLT-N005-OPS-18 | 11 | Definition of Ready item 18 Open decisions: Partial | Recorded DL11 open with ASM-0553, ASM-0703, ASM-1051, ASM-1104 |
| RWB-PLT-N005-OPS | R-22198 | GAP-1015 | 11 | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | Recorded overlap SKIP, catch-up of one run, and owner confirmation step |
| RWB-PLT-N005-OPS | R-23196 | GAP-2044 | 9 | No source names the owner of a per-service dashboard or alert rule as a team | Section 9 names the owner of each per-service dashboard, alert rule and run book as the service code of Ownership Map v1, with DevOps team as suggested owner. |
| RWB-PLT-N005-OPS | R-23286 | GAP-1418 | 9 | The observability baseline artefacts, thresholds and ownership are not specified | Section 9 assigns the baseline publication to the solution architect; values absent from the sources are left unset, not invented. |
| RWB-PLT-N005-OPS | R-23287 | GAP-2045 | 8 | Metric and span names, labels, retention, sampling and the alert delivery channel are not specified | BR9 requires the service label and places metric, span and label conventions, retention, sampling and alert channel in the baseline before wave 1. |
