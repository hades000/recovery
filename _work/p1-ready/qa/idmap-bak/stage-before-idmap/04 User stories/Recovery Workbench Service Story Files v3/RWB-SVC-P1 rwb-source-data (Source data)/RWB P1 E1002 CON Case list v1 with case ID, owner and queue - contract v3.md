# RWB-P1-E1002-CON Case list v1 with case ID, owner and queue - contract v1

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1002-CON |
| Work type | CON (Contract) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Retired in version 3 (RD-P1-024, X-27) |
| Contract version | None: this story publishes nothing |
| Depends on (build) | None |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-010, RD-P1-011, RD-P1-012, RD-P1-022, RD-P1-024, RD-P1-040 |
| Status | Retired: do not size, build or test. Replaced by RWB-P1-E1015-CON and RWB-P1-AD018-CON |

### Version 3 changes

- RWB-P1-E1002-CON is retired with a pointer (RD-P1-024 with X-27 and X-17): the case list leaves P1 and this story publishes nothing (review findings #1 to #3, #7 to #11, #13 to #17, #21).
- The account-page read that rwb-case needs is published in **RWB-P1-E1015-CON** and built by RWB-P1-E1002-APP.
- `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` are published by **RWB-P1-AD018-CON** (RD-P1-012; findings #4, #6, #12, #20).
- Version 2 stays in the SharePoint set as history. Pending: confirmation of the retirement by the delivery owner (NEW-ASM-X5).
- Finishing pass: Test Cases v9 holds the contract test rows of this story as retired, so that delivery step is closed.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 for rwb-source-data. This story publishes the contract baseline of the case list: the four REST operations and their answer shapes, the consumed event, the workflow, activity and Schedule contracts, the nine contract tables and the four rwb-case fakes. The case-list operations and their answer shapes, the workflow and schedule names and the 07:15 fallback are fixed here under GAP-0486, GAP-0487 and ASM-0678, ASM-0679, and the removal of the lake, the extract file and the Power BI data set is recorded under GAP-0485 and ASM-0677. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 17 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: story retired with a pointer (X-27). Agent: S1-stories.

### 1. Where each part of version 2 went

| Version 2 content | Now | Decision | Review findings |
|---|---|---|---|
| `case_list_row`, `GET /case-list/dates/{businessDate}`, `GET /case-list/rows`, schemas CaseListDate, CaseListRow and CaseListRowPage, publish status and its transitions | Withdrawn from P1. rwb-case serves the list with `GET /cases` (RWB-P3-E1002-APP) | RD-P1-024 | #1, #2, #3, #17 |
| Account values the list needs from ACE | Account-page read in rwb-source-data.yaml 5.1.0, published by RWB-P1-E1015-CON. Pending: path, schema and maximum keys per call, owner solution architect (NEW-GAP-B3) | RD-P1-024, X-27 | #2, #3, #7, #19 |
| `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, field names, rerun idempotency, 409 answers, error answers | RWB-P1-AD018-CON, the single publisher: `Job` fields `id`, `type`, `endedAt` and `checks` keyed REC-01, REC-02, REC-05; the rerun has no body and takes a UUID Idempotency-Key; errors use the shared `Problem` schema | RD-P1-004, RD-P1-012 | #4, #5, #6, #12, #20 |
| Provider fakes `caseListPage` and `listCaseListAccounts`, RELEASED, HELD and PENDING fixtures | Withdrawn. Account-page fixtures (200, 400, 401, 403, 503) belong to RWB-P1-E1015-CON; job fixtures to RWB-P1-AD018-CON | RD-P1-011 | #7 |
| rwb-case case query, allocation, parameter and reference-data calls and their fakes | Withdrawn: P1 calls rwb-case for no list | RD-P1-024 | #8, #13 |
| Consumption of `rwb.source-data.events.v1` `AceDataReady` and the AsyncAPI statement | Withdrawn. RWB-P1-E1015-CON is the publisher; rwb-source-data consumes no event of its own topic | RD-P1-040 | #9, #14 |
| `CaseListBuildWorkflow`, `DailyCaseList` Schedule at 07:15, activity signatures, run record, retry values | Withdrawn. `listEligibleAccounts` belongs to RWB-P1-E1018-APP and `snapshot(page)` to RWB-P1-E1013-APP; the morning schedule of the list is rwb-case's | RD-P1-010, RD-P1-022, RD-P1-024 | #10, #11, #15, #16, #21 |
| Service identities, authorisation and row scope | The account-page read is for the rwb-case workload identity only (RWB-P1-E1002-APP section 10); job operations as RWB-P1-AD018-CON | RD-P1-024 | #19 |
| DEF-008 (the REFUSED `load_run` row as load contract and flow) | No longer applies: `load_run` is not a table of rwb-source-data and this story defines no load contract. The defect register owner is asked to close it against this story | RD-P1-024 | #18 |
| Contract test cases TC-E1-002 of this story | Retired with the story in Test Cases v9; no CON test case is kept | RD-P1-024 | #22, #23 |
| Versioning rule, baseline tag, consumer sign-off, dependencies, AC numbering, cited document versions | Carried by RWB-P1-E1015-CON and RWB-P1-AD018-CON at contract version 5.1.0 (API Specification v7). GAP-2228 is applied; GAP-0487 is moot | RD-P1-005 | #24, #25, #26 |

### 2. Acceptance criteria

None. A retired story has nothing to accept. The removal of the case-list objects from the build is checked by RWB-P1-E1002-APP AC29.

### 3. Remaining delivery steps

- Confirm the retirement and close or re-point the work item; owner delivery lead (NEW-ASM-X5).
- Re-point every story that depends on RWB-P1-E1002-CON to RWB-P1-E1015-CON or RWB-P1-AD018-CON; owner the story owners.
