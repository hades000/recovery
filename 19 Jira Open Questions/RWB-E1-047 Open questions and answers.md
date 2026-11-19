# RWB-E1-047 Feature flags for module release with a removal date

| Field | Value |
|---|---|
| Jira | TB0001-1208, component E2E Workbench, status To Do, parent TB0001-1162 |
| Jira comments read | 3 (R. Kasemphin 16 Nov, C. Gingpuwaluck 17 Nov, N. Jittachotisak 17 Nov): 9 numbered clarifications, 5 dependency concerns, 4 follow-ups, 5 questions |
| Story text used | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 047 ... v1.md` (the same text is in Epic 1 v9) |
| Build order | Build Sequence v6 order 16, Window 2 (16 to 27 Nov), depends on RWB-E1-001 only |
| Prepared | 18 November 2026 |

Status key: **ANSWERED** = a document in the set decides it. **PROPOSED** = the documents imply the answer; the owner should ratify it. **OPEN** = no document decides it; options and a recommendation are given. Gap IDs (G-...) are in `Document Gaps.md`.

## Summary

| Status | Items |
|---|---|
| ANSWERED | Q02, Q05c, Q06a, Q06b, Q07a, Q13, Q15, Q17 |
| PROPOSED | Q01, Q03, Q05a, Q05b, Q07b, Q07c, Q08, Q09, Q11, Q12, Q14, Q16, Q18 |
| OPEN | Q04 (risk acceptance), Q06c (maximum date), Q10 (PROD change control) |

## Answers

### Q01 Dependencies the story does not list (R. Kasemphin, concerns)

| Dependency | Evidence | Answer |
|---|---|---|
| RWB-TE-007 Quartz | Build Sequence v6: TE-007 is order 21, this story is order 16 | Confirmed. The story needs a scheduler only for AC3 and the Monday run. **Proposed:** build `FlagRemovalReportJob` as a plain class now and test AC3 by calling it directly; add a scheduled-run test when TE-007 is done. Record TE-007 as a "schedule trigger only" dependency |
| RWB-E1-022 Sign-on | Order 26. Users Roles and Permissions v4 already names the groups `RWB-DEV/SIT/UAT/PROD-RW-PLATADM`; DL40 (group names to the bank standard) is still open | Confirmed. **Proposed:** build and test with a test identity that carries the role, then run the real sign-on test when E1-022 is done |
| RWB-E1-037 Permission matrix | Order 27 | Confirmed. TC-E1-047-10 (403 for RW-CASEOWN) needs the capability check. **Proposed:** run it with a stubbed capability check until E1-037 lands |
| RWB-E1-002, RWB-E1-031 (SCR-02 queue column) | Orders 45 and 48 | Confirmed. **Proposed:** change "Done when" to a component test (FlagGate hides and shows a child) plus the UAT demo on SCR-02 once those two stories are done |
| ACE audit log service and ACE notification path | Not described in any document in the set | **OPEN, gap G-047-04.** Owner: ACE team. Ask for the API contract and confirm SIT and UAT availability |

### Q02 Response shape of GET /feature-flags (ANSWERED)

**An array of `FeatureFlagValue` {key, value}.** API Specification v4 (`getFeatureFlags`) returns `type: array` of `FeatureFlagValue` with `key: string` and `value: boolean`. The workbench build generates its front-end types from API v4, so the story text is the one to correct. `useFeatureFlag` builds its own key-to-value lookup from the array. Section 12 of the story must read "Array of FeatureFlagValue: key, value".

### Q03 AC1 "the flag has no value set for UAT" (PROPOSED)

The state cannot exist: Physical Schema v6 has `uat_on boolean NOT NULL DEFAULT false`, and Flow step 2 writes every environment from the default. AC1 should read "UAT holds the default value (off)". `default_on` is only the starting value copied into the four environment columns at creation. `isOn()` reads the column for the running environment (`rwb.environment`) and never falls back to `default_on`. Say this in section 13.

### Q04 Flag store unavailable after a restart (AC7, BR5) (rule decided; risk acceptance OPEN)

The rule is decided: BR5 and DT11 say an unknown key or an unreadable store gives **off, never on**. What no document records is acceptance by Business and Operational Risk for PROD. In practice the 30-second cache means only a cold start with the table unreadable turns features off. A last-known snapshot (file or second store) is in no story's scope. **Recommendation:** keep the story as written and record the acceptance as a decision (owner: Solution architect with Operational Risk). If they refuse, raise a separate story for a snapshot fallback.

### Q05 Flag key validation

**a. Invalid key (PROPOSED).** No AC, test or message exists. Physical Schema v6 has no check on `flag_key` (only `uk_feature_flag`), so the pattern check lives in the service and, per section 13, in a migration constraint. Respond **422** with a new message. The next free ID in Error and Message Standard v4 is `MSG-P2-026` (P2 ends at 025), for example "Flag key {key} must follow rwb.<module>.<short-name>." Add AC10 and a test case.

**b. Duplicate key (PROPOSED).** The contract says 409 with `MSG-GEN-004`, but that message says "Someone else changed this record." Story Defects v4 lists this as open (RWB-E1-047 item 2). Use a new message `MSG-P2-027` "Flag {flag} already exists." Add AC11 and a test case.

**c. What `<module>` means (ANSWERED).** The module map `recovery-modules.yaml` (RWB-TE-001, D-RCV-37) is "the only source of module names". Use the **name**, not the code: dataengine, integration, casewf, access, dochub, comms, decision, payments, reporting, agent, valuation, treatment, guarantee, litigation, asset, debtsale, writeoff, deviation, partner. That is what RWB-E1-007, E1-015, E1-056 and the story's own reference flag use. The module codes (`rwb.p3.temporal`, `rwb.p3.drools` and others) break the convention and pass the regex only by accident: G-047-05. The runtime check needs the list as data, not the test-only YAML: G-047-06.

### Q06 Removal date boundaries

- **a. Created with removal date = today (ANSWERED).** Accepted. X2 refuses only "before today".
- **b. Report on the removal date (ANSWERED).** Not listed. The job selects `removal_date` before today (section 12), so the flag appears from the following Monday, 7 days overdue. Add this as an example to AC3.
- **c. Maximum removal date (OPEN).** No document sets one. Recommendation: no maximum in Epic 1; if wanted, make it a property (`rwb.flags.max-removal-days`), not code. Owner: Product owner.

### Q07 Retire and edit flags

- **a. In scope? (ANSWERED).** No. API v4 has only create (POST) and change value (PATCH with environment, value, reason). Sections 15 and 19 put the flag screen in SCR-44, Epic 8. Remove "retires flags" from sections 9 and 10, or add the endpoint to API v5.
- **b. `isOn()` for a retired flag (PROPOSED).** Off, the same as an unknown key (BR5).
- **c. Retired flag still in code (PROPOSED).** Warn: the same log warning as AC6 (key, no user data).

### Q08 Changing a flag to the value it already has (PROPOSED)

The contract says no change row is written. Expected result: **200 with the unchanged flag, `version` unchanged, no change row, no ACE audit entry** (nothing changed). The reason is still validated first, so an empty reason still returns 422. Add AC12 and a test case.

### Q09 Weekly report rerun (idempotency) (PROPOSED)

Physical Schema v6 has no job-run table and no report-date column; the job run log comes from TE-007 (E1-056 section 3). Use the `IdempotencyGuard` that RWB-E1-007 publishes (table `processed_event`, unique `(consumer, idempotency_key)`): consumer `flag-report`, key `<report date>:<recipient>`, written after each successful send.

- First run fully succeeded, run again the same Monday: every key exists, nothing is sent.
- First run partly failed (one owner's mail failed): the rerun sends only to recipients with no key.

E1-007 is order 11, so it is built before this story. Add it to Depends on.

### Q10 Change control for PROD (OPEN)

The letter A means "Approve, within the limit set for the role in the delegation of authority table" (Users Roles and Permissions v4, Key sheet). Maker and checker (Admin and Access Model v5, section 6.2) covers decisions, not flag changes. No document requires approval, a ticket reference or a change window for a flag change, and DT11 and DL04 want a flag to be a quick switch-off. **Recommendation:** Epic 1 keeps reason, change row and ACE audit entry with no approval step, and section 10 drops the "A" for RW-SECADM (or says it has no function in this story). Decide with the Product owner, Security administrator and Operational Risk. If they want approval, it is a new story.

### Q11 The weekly job has no run book and is not in the 16 catalog rows (C. Gingpuwaluck) (PROPOSED, gap G-X-01)

Batch and Scheduling Design v4 lists 22 jobs and this one is not among them; RWB-E1-056 seeds 16 rows; `RunbookCompletenessTest` checks every Quartz job, so the pipeline would fail. **Proposed:** add `FlagRemovalReportJob` under a new job ID (next free: JOB-23), Monday 08:00 Asia/Bangkok, owner platform administrator, to Batch Design v5 and to the E1-056 catalog, and write its run book in this story.

### Q12 Front end when the flag store is down (PROPOSED)

API v4 gives `GET /feature-flags` a 503. The hook should treat any non-200 as "all flags off", keep values already read in the session, log it without user data, show no message, and read again on the next page load. The 30-second cache stays an assumption under DL11, which is open and past its date (5 Nov); keep it in `rwb.flags.cache-seconds`.

### Q13 Typo in AC4 (ANSWERED)

Confirmed: "does not creat". Change to "does not create".

### Q14 Seed data for flags (N. Jittachotisak) (PROPOSED)

The story creates only the test flag (section 3) and says other flags are created through the endpoints (section 13). But about 35 Epic 1 and enabler stories each name their own flag; until someone creates it, the key is unknown and the code returns off (AC6). **Proposed:** a seed script per environment (not a migration) that creates the flags named in the stories, default off, with an owner team and a removal date set by the owning squad. The list is in Appendix A. Ask each squad for its removal date.

### Q15 Is the version sent in a header? (ANSWERED)

Yes: story section 12 says header `If-Match` carries the version. But **API v4 declares no `If-Match` header anywhere** and the `FeatureFlagChange` body has no `version`, so a generated client would not send it. Add the header to API v5 for this PATCH and for the other endpoints that use it (resend, rerun): G-X-05.

### Q16 Scheduler is built later and ACE has no e-mail service (PROPOSED)

The scheduler dependency is Q01 (TE-007, order 21). On e-mail: the story says "through the ACE notification path for staff", but no document describes that path. Epic 1 already has a precedent that needs no ACE e-mail service: E1-007 and E1-056 send mail from a Log Analytics alert rule on a log event. **Proposed:** the job writes one log event per overdue flag (the `MSG-P2-003` line the story already requires) and an alert rule mails the owner team and the RW-PLATADM group. Confirm with the ACE team and Operations.

### Q17 What happens when removal_date is before today (ANSWERED)

The owner is told every week until the flag is removed (BR4). Nothing else changes: the flag stays active and its value stays the same. No step disables a flag.

### Q18 Clarity of `GET /admin/feature-flags?overdue=true` (PROPOSED)

API v4 types `overdue` as a **string**, not a boolean, and `daysOverdue` is an integer with no definition. **Proposed definition:** `overdue=true` returns active flags with `removalDate` before today; `daysOverdue` = today minus `removalDate` in calendar days (at least 1); with `overdue` absent or false it returns every active flag with `daysOverdue` 0; `owner` matches `ownerTeam` exactly. Put this in the endpoint description and make `overdue` a boolean in API v5 (G-X-05).

## Changes to make to the story

1. Section 12: GET /feature-flags returns an array of `FeatureFlagValue` (Q02).
2. AC1 wording: "UAT holds the default value (off)" (Q03).
3. AC3: add the removal-date-equals-today example (Q06b).
4. AC4: fix "creat" (Q13).
5. Add AC10 (invalid key), AC11 (duplicate key), AC12 (same value) and test cases (Q05, Q08).
6. Add messages `MSG-P2-026` and `MSG-P2-027` to section 14 (Q05).
7. Sections 9 and 10: remove "retires flags" or add the endpoint (Q07).
8. Header: Depends on adds RWB-E1-007 (guard) and TE-007 (schedule only) (Q01, Q09).
9. Section 12 job: idempotency key and restart behaviour (Q09).
10. Section 13: `isOn` fallback, front-end behaviour on 503, cache assumption (Q03, Q12).
11. Section 13: say whether the tables are created by V0001 or by this story's migration (G-047-02).
12. Sections 11 and 13: add a run book and catalog row for the weekly job (Q11).

## Appendix A Flags named by Epic 1 stories (seed list for Q14)

Source: the "Feature flag" line of each story file in Story Files v7. Removal dates must come from each squad.

| Flag | Story | Flag | Story |
|---|---|---|---|
| rwb.casewf.case-list-queue-column | E1-047 (test flag) | rwb.dochub.casedocs | E1-026 |
| rwb.integration.file-adapters | E1-007 | rwb.decision.log-writer | E1-027 |
| rwb.decision.log-store | E1-008 | rwb.dochub.autoattach | E1-032 |
| rwb.reporting.baseline | E1-013 | rwb.comms.template-admin | E1-034 |
| rwb.dataengine.lake-copy | E1-014 | rwb.access.permission-matrix | E1-037 |
| rwb.dataengine.freshness-stamp | E1-015 | rwb.access.delegation-table | E1-038 |
| rwb.dataengine.product-access | E1-016 | rwb.access.access-log | E1-039 |
| rwb.dataengine.retention | E1-017 | rwb.dochub.checklist | E1-040 |
| rwb.access.sso-roles | E1-022 | rwb.dochub.malware-scan, rwb.dochub.retention | E1-041 |
| rwb.dochub.store | E1-024 | rwb.comms.template-catalog | E1-046 |
| rwb.dochub.doctypes | E1-025 | rwb.dochub.ocr | E1-049 |
| rwb.dochub.classify | E1-050 | rwb.comms.notice-generation | E1-052 |
| rwb.comms.win-dispatch-v1 | E1-055 | rwb.integration.job-monitoring | E1-056 |
| rwb.dochub.intake | E1-057 | rwb.dataengine.data-dictionary | E1-064 |
| rwb.dataengine.sandbox | E1-065 | rwb.dataengine.ledger-writer | E1-066 |
| rwb.dataengine.ledger-events | E1-067 | rwb.dataengine.ledger-read | E1-068 |
| rwb.dataengine.masked-copy | TE-004 | rwb.integration.outbox | TE-006 |
| rwb.decision.hash-check | TE-008 | rwb.p3.temporal | E1-071 (module code, see Q05c) |
