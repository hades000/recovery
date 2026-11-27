# Script build-readiness review — summary

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Stories: 1034. Time: 8.6 s. Detcheck rows used: 12086.

| Verdict (all 25 items) | Verdict on the story text (records items left out) | Stories |
|---|---|---|
| NOT READY | NOT READY | 868 |
| NOT READY | READY WITH GAPS | 166 |

AC review rows: 461. Missing-criterion rows: 3678.

## Checklist results (Definition of Ready and Done v4 section 2)

| # | Item | Pass | Partial | Fail | Not applicable |
|---|---|---|---|---|---|
| 1 | Story | 464 | 535 | 35 | 0 |
| 2 | Links | 819 | 215 | 0 | 0 |
| 3 | Acceptance criteria | 472 | 536 | 26 | 0 |
| 4 | Business rules | 63 | 971 | 0 | 0 |
| 5 | State transitions | 916 | 0 | 118 | 0 |
| 6 | Authority | 631 | 403 | 0 | 0 |
| 7 | Data | 160 | 843 | 31 | 0 |
| 8 | Contract | 178 | 43 | 813 | 0 |
| 9 | Messages | 500 | 534 | 0 | 0 |
| 10 | Screens and states | 72 | 962 | 0 | 0 |
| 11 | Guardrails | 607 | 427 | 0 | 0 |
| 12 | Test cases | 22 | 911 | 101 | 0 |
| 13 | Out of scope | 1034 | 0 | 0 | 0 |
| 14 | Epic design | 0 | 0 | 1034 | 0 |
| 15 | INVEST | 861 | 173 | 0 | 0 |
| 16 | Size | 0 | 0 | 1034 | 0 |
| 17 | Dependencies | 652 | 231 | 151 | 0 |
| 18 | Open decisions | 521 | 513 | 0 | 0 |
| 19 | Test data | 1034 | 0 | 0 | 0 |
| 20 | Reference data | 654 | 375 | 5 | 0 |
| 21 | Contract published | 0 | 0 | 746 | 288 |
| 22 | Fake published | 0 | 0 | 746 | 288 |
| 23 | Contract version fixed | 22 | 0 | 1012 | 0 |
| 24 | Ownership stated | 749 | 285 | 0 | 0 |
| 25 | Ready to start | 1034 | 0 | 0 | 0 |

## Most common problems

| Item | Problem (IDs replaced by #) | Stories |
|---|---|---|
| 12 | no boundary test for the tables of §12.7 (ASM-3438) | 776 |
| 3 | exception # is covered by '#', not by a criterion | 490 |
| 18 | open decisions apply; each has an assumption, the decision is still open | 472 |
| 12 | no contract test for the operations, events and activities of §12 | 388 |
| 20 | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | 356 |
| 6 | the story provides REST operations and names no rwb-access authorise check (DP-08) | 349 |
| 12 | # has no test case in §16 | 195 |
| 1 | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | 192 |
| 2 | §18 has no L3 process column | 172 |
| 2 | §18 has no feature column | 164 |
| 15 | INVEST 'Small' does not say it fits two weeks | 139 |
| 3 | # has no When | 124 |
| 3 | §5 has no 'Covered by' column, so no exception path is tied to a criterion | 100 |
| 17 | 1 build dependencies are not done yet (#) | 89 |
| 4 | 10 of 10 rules are covered by no criterion and no test case: #, #, #, #, #, #, #, #, #, # | 86 |
| 9 | messages used but not listed in §14: # | 77 |
| 7 | 8 row(s) of §11 have no BR Field ID | 77 |
| 17 | 2 build dependencies are not done yet (#, #) | 75 |
| 6 | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5 | 75 |
| 7 | BR Field IDs not in LDM v9: # | 73 |
| 4 | 12 of 12 rules are covered by no criterion and no test case: #, #, #, #, #, #, #, #, #, #, #, # | 71 |
| 4 | 9 of 9 rules are covered by no criterion and no test case: #, #, #, #, #, #, #, #, # | 70 |
| 3 | exception # is covered by 'Section 17, #, #', not by a criterion | 69 |
| 4 | 8 of 8 rules are covered by no criterion and no test case: #, #, #, #, #, #, #, # | 66 |
| 7 | 6 row(s) of §11 have no BR Field ID | 64 |
| 7 | 9 row(s) of §11 have no BR Field ID | 57 |
| 4 | 11 of 11 rules are covered by no criterion and no test case: #, #, #, #, #, #, #, #, #, #, # | 51 |
| 7 | 7 row(s) of §11 have no BR Field ID | 50 |
| 24 | §12.4 has no owner or service column | 49 |
| 17 | 3 build dependencies are not done yet (#, #, #) | 42 |
| 4 | 13 of 13 rules are covered by no criterion and no test case: #, #, #, #, #, #, #, #, #, #, #, #, # | 42 |
| 22 | no contract fake named in §12.8 for rwb-case | 41 |
| 24 | §13 names other schemas: rwb_case | 40 |
| 7 | 10 row(s) of §11 have no BR Field ID | 39 |
| 1 | §1 role 'platform engineer' is not a role code or role name in Users Roles and Permissions v5 | 39 |
| 3 | exception # is covered by #, which this story neither owns nor names as owned by another story | 38 |
| 1 | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | 36 |
| 1 | §1 is not in the form 'As a <role>, I want ..., so that ...' | 35 |
| 3 | exception # is covered by 'Section 17', not by a criterion | 33 |
| 15 | INVEST 'small' has no result in §6 | 33 |
