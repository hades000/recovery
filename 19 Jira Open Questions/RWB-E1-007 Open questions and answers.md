# RWB-E1-007 Integration adapters for outbound files

| Field | Value |
|---|---|
| Jira | TB0001-1169, component E2E Workbench, status In Design - Solution, labels Block, R-Decision, R-Requirement, R-Spec |
| Jira comments read | 16 (11 to 17 Nov), including the 13 Nov e-mail answer attached as a text file (the attachment itself is not readable through the Jira tool; its content is taken from the comments that quote it) |
| Story text used | Story Files v7, `RWB E1 007 Integration adapters for file loads and outbound files v1.md`, dated 15 Nov (the H1 reads "Integration adapters for outbound files"; the same text is in Epic 1 v9) |
| Build order | Build Sequence v6 order 11, Window 1 (2 to 13 Nov), depends on E1-001 and E1-069 |
| Prepared | 18 November 2026 |

Status key: **ANSWERED** = a document in the set decides it. **PROPOSED** = the documents imply the answer; the owner should ratify it. **OPEN** = no document decides it; options and a recommendation are given. Gap IDs (G-...) are in `Document Gaps.md`.

## The main finding

Most of the thread was written before the re-base. **The inbound half of this story no longer exists.** D-RCV-35 (15 Nov) moved all source ingestion to ACE (RWB-ACE-001). Data Load Story Removals v2 says "RWB-E1-007 is not removed. It survives as outbound-only adapters. Only its inbound file-load part is obsolete." The Henka answer of 13 Nov (Part D: file-by-file checks, 23 sample files, new AC4 to AC9) answers the old story. The comments of 17 Nov by V. Kaulge already say this; the points below confirm it against the documents and answer what is left.

Two things in Jira are stale and should be fixed first: **the Jira description and title** still describe "file loads and outbound files" (G-007-01), and the labels Block, R-Decision, R-Requirement, R-Spec should be reviewed against the three real blockers in Q06, Q07 and Q16.

## Summary

| Status | Items |
|---|---|
| ANSWERED | Q01, Q02, Q03, Q04, Q08, Q09, Q10, Q12, Q17 |
| PROPOSED | Q07, Q11, Q13, Q14, Q18, Q19, Q20 |
| OPEN | Q05, Q06, Q15, Q16, Q21 |

## Answers

### Q01 Does the attachment replace the v7 note that FileCheckRunner was removed? (ANSWERED: no)

The v7 story is the current one. Evidence: Data Load Story Removals v2 (the inbound file adapters of E1-007 move to "ACE ingestion, raised once with the ACE team in RWB-ACE-001"; "Do not rebuild it"); Story Defects v4 (E1-007 items 2, 4 and 8 closed 15 Nov for this reason); Decision Log v10, D-RCV-35 U1. FileCheckRunner, FileLoadAdapter, RecordLoader, DQ-057, DQ-059, JOB-09, `interface_run` and `interface_signoff` are not built in the Workbench. The Part D specification and the 23 sample files go to RWB-ACE-001 as input for its ingestion checks. One thing no document settles: whether ACE will use the same class and rule names. That is for the ACE story owner to confirm.

### Q02 Is there a separate "Data Loading" story, and where is the boundary? (ANSWERED: no)

The 11 Nov grooming note planned one; D-RCV-35 replaced it. JOB-09 is retired (Batch Design v4). JOB-10 (WIN outbound notices) and JOB-11 (outbox sender) stay in this story as outbound jobs, so no new key is needed. The boundary: this story builds the outbound adapter, the sender, the idempotency guard and two endpoints, and **creates no table** (the five P2 tables come from V0001, RWB-E1-001). ACE ingestion, its schedule, its checks and its sign-off belong to RWB-ACE-001. The statement "classes plus four new tables" in the comments describes the old story.

### Q03 The stale rule is stated two ways (ANSWERED: neither applies)

Both are gone with the inbound load (Story Defects v4 item 4, closed). This story now holds an outbound file until the ACE batch for its business date is COMPLETED (AC4, BR3). When a source data product is stale is defined by RWB-E1-015.

### Q04 DEP-15 layouts and the key and amount fields for AMIS, RPS, GL (ANSWERED: not this story)

RAID v4 DEP-15 (file layouts for CCMS, SVAF, AMIS, RPS, WIN and GL, due 2026-11-13, owner Data engineering with the system owners) is overdue. Those layouts are now the ACE ingestion specification, owned by the ACE team (Interface Specifications v3, note above the mapping sheet). Integration Inventory v3 also shows AMIS first release E3 and GL first release E6, so they are not Epic 1 at all. Nothing in E1-007 needs them. The key and amount fields in the interface mapping (AMIS: Asset ID and Book Value; RPS: AccNo, ContractNo, OutBal; GL: DATE, RC, OC, ACCOUNT, PRODUCT, EVENT, AMT) are not confirmed as keys; ask the ACE team.

### Q05 RPO and RTO, and the NFR targets (OPEN)

Non-Functional Specification v3: NFR-022 (RPO) and NFR-023 (RTO) are "Open, DL11", owner IT lead with Operational Risk, no date. DL11 was due 2026-11-05. NFR-026 (three retries, then the exception queue) is "Proposed, DL11". The 30-minute resend wait in JOB-11 is an assumption under DL11. This is platform-wide and is a go-live gate for Epic 1, not an E1-007 build blocker. **Action:** the IT lead gives a date for DL11; until then the story keeps the assumptions as properties.

### Q06 INT-14 outbound path and acknowledgment file name (OPEN, blocker B1)

Interface Specifications v3 (INT-14) give the interface, the owner and "send again; after the third failure raise a task to the owning team". They give **no SFTP folder, no write access detail and no acknowledgment file name**. The story uses `rwb.integration.sftp.host` and an example file name `WIN_NOTICE_20261110.txt`. **Needed from Henka and the Delivery team:** DEV and SIT folder, write access for `recovery_svc`, the acknowledgment folder and the acknowledgment file name. Without them, `SftpTransport` cannot be finished. There is a second part in Q15.

### Q07 Retry: 3 attempts with waits of 5, 15 and 45 minutes (PROPOSED, blocker B2, gap G-007-02)

The 45 never runs. Story Defects v4 closed this item (item 8) on 15 Nov, but AC3 and the Background of the v7 story **still carry the same settings**, so it was closed in error. Two documents disagree about the rule:

| Source | Says | Gives |
|---|---|---|
| Interface Specifications v3, INT-14 | "after the third failure raise a task" | 3 attempts, waits 5 and 15 |
| NFR-026 (proposed) | "three retries per item, then the exception queue" | 4 attempts, waits 5, 15 and 45 |

The story reads attempt 1 as the first send (AC3: "attempts 1, 2 and 3"), so the first send counts as attempt 1. **Recommendation:** 4 attempts (first send plus three retries) with waits 5, 15 and 45, because NFR-026 is the platform rule and every wait is then used. Change `max_attempts` to 4 in the Background, AC3, TC-E1-007-03 and the INT-14 interface row, and word INT-14 as "after the third retry". The alternative is 3 attempts with `[5, 15]`. Decision: Integration architect.

### Q08 Do all four checks run, and one result per check or per file? (ANSWERED: not in this story)

The four checks belong to the ACE ingestion (Q01). Pass the question to RWB-ACE-001.

### Q09 Current AC numbering (ANSWERED)

| AC | Scenario | Story test case |
|---|---|---|
| AC1 | One outbound pattern | TC-E1-007-01 |
| AC2 | Read ACE through the views only | TC-E1-007-02 |
| AC3 | Retry and exception queue | TC-E1-007-03 |
| AC4 | Hold the outbound file until the ACE batch is complete | TC-E1-007-04 |
| AC5 | Ignore a duplicate application event | TC-E1-007-07 |
| AC6 | Two sender threads | TC-E1-007-08 |
| AC7 | Resend from the exception queue | TC-E1-007-09 |
| Access | RW-CASEOWN refused | TC-E1-007-10 |

**But the test case IDs in the story do not match Test Cases v7.** There the same tests are numbered TC-E1-007-05 (duplicate event), -06 (two senders), -07 (resend), and the sheet adds -08 (a build reads a public table) and -09 (a late batch releases the held file), which the story does not list. The story also says TC-05 and TC-06 are retired. Align the two (G-007-04). The old AC9 "resend" is now AC7.

### Q10 AC5: cut-off per source, which product is SVAF, is the stale flag cleared (ANSWERED)

The old AC5 is retired. Outbound timing: JOB-10 runs daily at 16:00 after the ACE batch is complete (Batch Design v4); the previous business date comes from `v_ace_holiday`. SVAF feeds DP06 (product-to-source map in E1-015, section 12). Clearing a stale flag is E1-015 AC6.

### Q11 Resend: same file or a new file? Does the attempt count reset? (PROPOSED, ANSWERED for the count)

The count resets to 0 (AC7). Flow step 5 stores the built file in the document store and the item points to it, so a resend sends **the stored file**; nothing is rebuilt from current ACE data. The story does not say this in words; add one sentence to section 4 and to AC7.

### Q12 Do the 23 sample files cover AMIS, RPS and GL? (ANSWERED)

No, not in this story. Its test data is outbound: the INT-25 tape of 120 accounts, 85 WIN notices, a stub that fails three times. Inbound samples belong to RWB-ACE-001 (Q01).

### Q13 Error handling per scenario (PROPOSED)

| Scenario | Message | API or other | Recipient |
|---|---|---|---|
| Old AC2 inbound check | MSG-P1-002 | Removed from this story; ACE side | ACE team to specify |
| AC3 retry | MSG-GEN-006 during retry; MSG-P2-001 at the exception | Not an API response. Item shows in SCR-09 via `GET /admin/outbound-items`; a task goes to RW-PLATADM | RW-PLATADM. The story also has the data steward mailed from the Log Analytics alert on `rwb.integration.outbound.failed`: confirm that both are wanted |
| AC4 held file | MSG-P1-001 | Not an API response. Log event `rwb.integration.outbound.held` and alert rule | X1 says the platform administrator **and** the data steward; AC4 says the platform administrator; section 10 and 15 say the data steward. **Use both** and fix AC4 |
| AC7 resend | MSG-GEN-005 | `POST /admin/outbound-items/{itemId}/resend`. **API v4 returns `OutboundItem` with no message field**, so the AC cannot be met as written (G-X-05) | RW-PLATADM |

Also: the English text of MSG-P2-001 differs between the story ("The {interface} file {file} was not sent after {count} attempts.") and Error and Message Standard v4 ("{item} was not delivered to {interface} after {count} attempts."), and MSG-P2-001 and MSG-GEN-005 are missing from the SCR-09 message list (G-007-05).

### Q14 Which meaning of hit count: 2 or 1? (PROPOSED)

Physical Schema v6: `processed_event.hit_count integer NOT NULL DEFAULT 1` and `data_product_load.duplicate_count integer NOT NULL DEFAULT 0`. E1-007 AC5 therefore says 2 and E1-015 AC5 says 1. **Proposed:** one meaning everywhere, "repeats ignored, starting at 0": rename `hit_count` to `duplicate_count` with default 0, AC5 reads 1, and the dictionary row changes with it. Needs Physical Schema v7 before V0001 merges (G-X-04).

### Q15 What does "acknowledged" mean without an inbound adapter? (OPEN, gap G-007-03)

Not raised in Jira, found while answering Q06. Flow step 6 sets ACKNOWLEDGED "when the acknowledgment file arrives" and JOB-11 retries an item left SENT with no acknowledgment after 30 minutes. But BR9 says the Workbench picks up no file, and Integration Inventory v3 says WIN proof of delivery reaches ACE **weekly** (INT-15) and is read through `v_ace_pod`. A weekly delivery proof cannot drive a 30-minute retry. **Options:** (a, recommended) ACKNOWLEDGED means the transfer receipt: `SftpTransport` reads a small acknowledgment file from a named folder, written into BR9 as an explicit exception to "no file is picked up"; the weekly POD stays a separate business fact (RWB-E1-055); (b) ACKNOWLEDGED means the SFTP write succeeded and the 30-minute rule is dropped. Decision: Integration architect with Henka (file name per Q06).

### Q16 One transport failure creates 85 tasks (C. Gingpuwaluck; V. Kaulge agrees) (OPEN, blocker B3)

INT-14 says "raise a task to the owning team" (one task). In Physical Schema v6 `task.case_id` is `NOT NULL`, so a task for one file cannot exist without a case. R-UNI-33 and R-UNI-34 are case-level rules; whether they apply to a file transfer is unconfirmed. **Recommendation:** one outbound item, one alert: the item carries RETRY then EXCEPTION, SCR-09 and the alert are the owner's work item, and the 85 cases keep their route state. Change AC3, X2, X3, section 9, BR4 and BR6. If the business needs the cases marked, keep the state change but still raise one task per file, which needs `task.case_id` to become optional (schema change). Decision: Integration architect and Product owner.

### Q17 AC4 uses Saturday 2026-11-07 (ANSWERED)

Confirmed: 2026-11-07 is a Saturday. The previous business date for Tuesday 2026-11-10 is Monday **2026-11-09**. Change AC4, the held reason, the MSG-P1-001 example and TC-E1-007-04, and add to BR3 that the previous business date comes from `v_ace_holiday`, not from "minus one day".

### Q18 WIN files carry personal data: encryption, retention, transport (PROPOSED, OPEN for owners)

The INT-14 file holds addressee and address; BR10 only covers the outbound item, not the file. Interface Specifications v3 name no encryption and no transport beyond "outbound file through the integration adapters" (INT-14, INT-25) and "daily batch" (INT-19, INT-20). The Personal Data Protection Design v2 and the Records Retention v2 say nothing on PGP; Records Retention v2 gives "Legal actions and notices" 10 years after the legal action ends, archive after 2 years, which is the nearest class for INT-14. DL26 (retention and masking, Compliance) is open and past 13 Nov. **Proposed** (as V. Kaulge wrote): add `encryption` (NONE or PGP) and `retention_class` to `interface_config`; INT-14 is PGP with a legal retention class and the clear file is not kept; a send is refused when no key is set; add an AC. **Owners to answer:** Security (key owner), Compliance (retention class per interface), Integration architect (transport for INT-14, 19, 20, 25).

### Q19 Flag off: files built unchecked or not at all? (PROPOSED)

The readiness check reads `v_ace_batch_status`, which exists only after RWB-ACE-001 (DL43). **Recommendation:** with the flag off, **INT-14 and INT-25 are not built** (a demand notice or a debt tape on unchecked arrears can reach the wrong customer or buyer) and the platform administrator and data steward get MSG-P1-001; INT-19 and INT-20 (reporting files with no addressee, rerun nightly) may be built with the item marked "readiness unchecked". Add one AC. This must agree with the E1-015 gate when its flag is off (the E1-015 proposal returns COMPLETE with reason NOT_CHECKED): in E1-007, NOT_CHECKED must not count as COMPLETE for INT-14 and INT-25. Decision: Product owner and Integration architect. Trade-off: no WIN file leaves until RWB-ACE-001 lands, unless the data steward confirms readiness by hand for a day.

### Q20 Schedule (PROPOSED)

Window 1 (2 to 13 Nov) has passed and no document re-plans the story. Stories that wait for it in Build Sequence v6: E1-056 (order 18) and E1-002 (order 45). The v7 header also makes E1-007 depend on E1-015 (order 56), but Build Sequence v6 builds E1-007 at order 11 and lists only E1-001 and E1-069; because the readiness check sits behind a flag, the build order stands and the header should say so (G-X-03). **Action:** the Delivery lead re-baselines E1-007 in the Release Plan once Q06 and Q16 are answered.

### Q21 Open items that remain after the re-base (OPEN)

Of about 30 questions, V. Kaulge counts 11 still open: three block the build (INT-14 path and acknowledgment, retry count, one task per file) and the rest do not.

| Open, not blocking | Owner |
|---|---|
| 30-minute resend wait (assumed, DL11; a configuration value) | Integration architect |
| Resend response has no message field, AC7 expects one (Q13) | Tech lead and API owner |
| MSG-P2-001 and MSG-GEN-005 missing from the SCR-09 list (Q13) | Content owner |
| RPO and RTO, DL11 option A, change window, document backup schedule, two extra test pass marks (platform level, Epic 1 go-live gate) | IT lead, Operational Risk |
| Encryption, retention, transport (Q18), flag off (Q19), Saturday date (Q17), hit count (Q14) | See each |

## Changes to make to the story and to Jira

1. Jira: replace title and description with the v7 text (G-007-01); review the Block and R-* labels.
2. AC3, Background, TC-E1-007-03, INT-14 row: retry settings (Q07); AC3, X2, X3, section 9, BR4, BR6: one item, one alert (Q16).
3. AC4, TC-E1-007-04, BR3: date 2026-11-09 and the calendar rule; AC4: both recipients (Q13, Q17).
4. AC5: duplicate count wording (Q14). AC7: response and stored file (Q11, Q13).
5. Section 4 step 6 and BR9: define ACKNOWLEDGED (Q15).
6. New AC: encryption and refusal without a key; new AC: flag off holds INT-14 and INT-25 (Q18, Q19).
7. Test case IDs: align the story with Test Cases v7 (Q09).
8. Section 14: MSG-P2-001 text from the standard (Q13).
