# RWB-SVC-P1 rwb-source-data (Source data) - resolved items, part 7 of 7 (RWB-P1-E2034-APP to RWB-P1-E2034-APP)

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-P1-E2034-APP | R-00431 | CG-ALL-2470 | 13 | rwb-source-data.yaml holds eventCode as a closed enum while the story reads LOV-LEDGER-EVENT as data | Ruled closed list per Reference Data v5; section 13 now states LOV-LEDGER-EVENT changes by code change to the eventCode enum, not as data. |
| RWB-P1-E2034-APP | R-04539 | DOR-RWB-P1-E2034-APP-12 | 16 | Definition of Ready item 12 Test cases: Fail | Added TC-E2-034-13 (AC4), -14 (contract test) and -15 (boundary test of 12.7). Section 18 list vs RTM v7 not changed; RTM v7 text not provided. |
| RWB-P1-E2034-APP | R-04544 | DOR-RWB-P1-E2034-APP-23 | 12 | Definition of Ready item 23 Contract version fixed: Fail | Version 5.0.0 read from info.version of rwb-source-data.yaml, rwb-access.yaml and rwb-case.yaml (API Specification v5). |
| RWB-P1-E2034-APP | R-04545 | DOR-RWB-P1-E2034-APP-8 | 13 | Definition of Ready item 8 Contract: Fail | Same closed-list ruling as CG-ALL-2470: section 13 states LOV-LEDGER-EVENT is a closed list, consistent with the eventCode enum. |
| RWB-P1-E2034-APP | R-09803 | CG-ALL-2469 | 12.7 | Name `tr_interaction_append_only` is not a field or entity in LDM v9 or Data Classification v5 | tr_interaction_append_only recorded as a database trigger of RWB-P1-E1066-APP, not an LDM entity or field. |
| RWB-P1-E2034-APP | R-09806 | CG-ALL-2473 | 14 | MSG-P3-024 text differs from the Error and Message Standard v4 | MSG-P3-024 English text in section 14 set to the standard v4 wording 'Nothing is recorded in {section} yet.' |
| RWB-P1-E2034-APP | R-09807 | CG-ALL-2475 | 7, 16 | Criteria with no test case: AC4 | TC-E2-034-13 already covers AC4 in section 16 as its test case; no edit needed. |
| RWB-P1-E2034-APP | R-15251 | DOR-RWB-P1-E2034-APP-18 | 14 | Definition of Ready item 18 Open decisions: Partial | Open decisions DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) named in section 14 as open, with their assumptions. |
| RWB-P1-E2034-APP | R-15252 | DOR-RWB-P1-E2034-APP-3 | 5, 7, 16 | Definition of Ready item 3 Acceptance criteria: Partial | Added AC7 (failed insert rolls back, 503, MSG-P1-022, incident hook) and TC-E2-034-16; X9 in section 5 now covered by AC7. |
| RWB-P1-E2034-APP | R-15253 | DOR-RWB-P1-E2034-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Added AC8 (no update or delete; correction is a new entry) for BR7 with TC-E2-034-17, and AC9 (one ledger in rwb_source_data) for BR1 with TC-E2-034-18. |
| RWB-P1-E2034-APP | R-15255 | DOR-RWB-P1-E2034-APP-7 | 11 | Definition of Ready item 7 Data: Partial | Section 11 names tr_interaction_append_only as a database trigger of RWB-P1-E1066-APP, not a dictionary field or entity; the legacy table's column header is now BR Field ID. |
| RWB-P1-E2034-APP | R-22305 | GAP-0590 | 18 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | REQ-ILG-007 now assigns the repeat count to the ledger writer's idempotency store. EFS:<efs_record_key> format is for RWB-P2-E2001-CON. |
| RWB-P1-E2034-APP | R-24501 | CG-ALL-2477 | 15 | SCR-03 has no empty, loading, error, no access state in the story | No access state added to SCR-03 as Not specified in the source documents; the specification does not give it. |
| RWB-P1-E2034-APP | R-24502 | CG-ALL-2478 | 15 | SCR-04 has no empty, loading, error, no access state in the story | No access state added to SCR-04 as Not specified in the source documents; the specification does not give it. |
| RWB-P1-E2034-APP | R-28845 | GAP-2226 | 8 | Legacy occurred-time order and the case timeline page order differ | Story keeps occurred time then case sequence (BR9). Screen page order stays with the case timeline contract per ASM-B2-P3-010-2. |
| RWB-P1-E2034-APP | R-29334 | ACR-RWB-P1-E2034-APP-AC4 | 16 | AC4 | TC-E2-034-13 already covers AC4 as written (Component); no new row needed. |
| RWB-P1-E2034-APP | R-30311 | NEWAC-RWB-P1-E2034-APP-AC12 | 5, 7, 16 | AC12: §5 X9: The entry cannot be inserted (covered by 'Section 12.1' only) | X9 is covered by AC7 and TC-E2-034-16. |
| RWB-P1-E2034-APP | R-30312 | NEWAC-RWB-P1-E2034-APP-AC13 | 7, 16 | AC13: §8 BR1, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | BR7 is covered by AC8 and TC-E2-034-17; BR1 by AC9 and TC-E2-034-18. |
| RWB-P1-E2034-APP | R-30313 | NEWAC-RWB-P1-E2034-APP-AC14 | 7, 16 | AC14: error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Added as AC10 with TC-E2-034-19 for 401, 403 and 404. |
| RWB-P1-E2034-APP | R-30314 | NEWAC-RWB-P1-E2034-APP-AC15 | 7, 16 | AC15: a consumed call fails or does not answer (no criterion covers a failed call) | Added as AC11 with TC-E2-034-20 for a failed or silent consumed call. |
