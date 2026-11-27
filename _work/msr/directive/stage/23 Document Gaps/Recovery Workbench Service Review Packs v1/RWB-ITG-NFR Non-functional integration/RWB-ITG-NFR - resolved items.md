# RWB-ITG-NFR Non-functional integration - resolved items

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-ITG-TE009-ITG | R-04166 | DOR-RWB-ITG-TE009-ITG-16 | header | Definition of Ready item 16 Size: Fail | Added Size row: not sized; the squad sizes it at refinement |
| RWB-ITG-TE009-ITG | R-04168 | DOR-RWB-ITG-TE009-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | §12.8 now names rwb-case, rwb-document and rwb-source-data and records that no fake and no fake library version apply; no published version in the source excerpts (DOR-RWB-ITG-TE009-ITG-22). |
| RWB-ITG-TE009-ITG | R-04169 | DOR-RWB-ITG-TE009-ITG-23 | 12.8 | Definition of Ready item 23 Contract version fixed: Fail | info.version 5.0.0 found in rwb-case, rwb-document and rwb-source-data yaml, API Specification v5; stated in §12.8. |
| RWB-ITG-TE009-ITG | R-14693 | DOR-RWB-ITG-TE009-ITG-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 now names SCR-02, SCR-03, SCR-04 and SCR-07 with their states; states absent from the source documents are marked Not specified. |
| RWB-ITG-TE009-ITG | R-14694 | DOR-RWB-ITG-TE009-ITG-12 | 16 | Definition of Ready item 12 Test cases: Partial | Section 16 now holds TC-ITG-TE009-ITG-01 to TC-ITG-TE009-ITG-09, one for each criterion AC1 to AC9. |
| RWB-ITG-TE009-ITG | R-14695 | DOR-RWB-ITG-TE009-ITG-4 | 7, 8, 16 | Definition of Ready item 4 Business rules: Partial | Added Covered by column to section 8; new AC7 and AC8; new TC-07 and TC-08 |
| RWB-ITG-TE009-ITG | R-22921 | GAP-0330 | 15 | Performance harness target routes, SIT identity set and pipeline stage are not named for the microservice target | Section 15 and lines 45 and 49 now fix routes and test identities at the configuration review before the first SIT run, kept in configuration. |
| RWB-ITG-TE009-ITG | R-24167 | CG-ALL-102 | 15 | SCR-02 has no empty, loading, error, no access state in the story | SCR-02 states now list loading and empty; error and no access marked Not specified in the source documents. |
| RWB-ITG-TE009-ITG | R-24168 | CG-ALL-103 | 15 | SCR-03 has no empty, loading, error, no access state in the story | SCR-03 states now list loading; empty, error and no access marked Not specified in the source documents. |
| RWB-ITG-TE009-ITG | R-24169 | CG-ALL-104 | 15 | SCR-04 has no empty, loading, error, no access state in the story | SCR-04 states now list loading; empty, error and no access marked Not specified in the source documents. |
| RWB-ITG-TE009-ITG | R-24170 | CG-ALL-105 | 15 | SCR-07 has no empty, loading, error, no access state in the story | SCR-07 states now list loading; empty, error and no access marked Not specified in the source documents. |
| RWB-ITG-TE009-ITG | R-28922 | GAP-3191 | 7 | The performance mix does not name the owning service of its 7 operations | Added Background step that reads each operation's owner service from the OperationCatalog of RWB-PLT-TE003-APP before the first gated run. |
| RWB-ITG-TE009-ITG | R-29324 | ACR-RWB-ITG-TE009-ITG-AC3 | 7 | AC3 | Then now names the operation, its error rate in percent and the 1 percent limit; added a pass Then under 1 percent. |
| RWB-ITG-TE009-ITG | R-30091 | NEWAC-RWB-ITG-TE009-ITG-AC7 | 7, 8, 16 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Added AC7 and AC8 with Given/When/Then steps; section 8 maps BR1 to BR8 to AC and TC rows. |
| RWB-ITG-TE009-ITG | R-30092 | NEWAC-RWB-ITG-TE009-ITG-AC8 | 7, 16 | AC8: a consumed call fails or does not answer (no criterion covers a failed call) | Added AC9 for a consumed call that fails or does not answer, counted as an error, and TC-ITG-TE009-ITG-09; test data not specified in sources. |
| RWB-ITG-TE010-ITG | R-04171 | DOR-RWB-ITG-TE010-ITG-16 | header | Definition of Ready item 16 Size: Fail | Added Size row to header table: set by the squad at refinement. |
| RWB-ITG-TE010-ITG | R-04174 | DOR-RWB-ITG-TE010-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Added Contract version row stating the /v1 path version. |
| RWB-ITG-TE010-ITG | R-14698 | DOR-RWB-ITG-TE010-ITG-18 | 3 | Definition of Ready item 18 Open decisions: Partial | DL10 and DL37 recommendations from decision log v8 (13 AI-First SDLC repository, legacy 01-decisions-and-governance) recorded in section 3. The log itself may still show them open. |
| RWB-ITG-TE010-ITG | R-14699 | DOR-RWB-ITG-TE010-ITG-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | BR8 is covered by AC9 and by test cases TC-ITG-TE010-ITG-09 and TC-ITG-TE010-ITG-11. |
| RWB-ITG-TE010-ITG | R-24172 | CG-ALL-107 | 15 | SCR-02 has no empty, loading, error, no access state in the story | SCR-02 row adds Error and No access as Not specified in the source documents (CG-ALL-107). |
| RWB-ITG-TE010-ITG | R-24173 | CG-ALL-108 | 15 | SCR-03 has no empty, loading, error, no access state in the story | SCR-03 row adds Empty, Error and No access as Not specified in the source documents (CG-ALL-108). |
| RWB-ITG-TE010-ITG | R-24174 | CG-ALL-109 | 15 | SCR-04 has no empty, loading, error, no access state in the story | SCR-04 row adds Empty, Error and No access as Not specified in the source documents (CG-ALL-109). |
| RWB-ITG-TE010-ITG | R-24175 | CG-ALL-110 | 15 | SCR-05 has no empty, loading, error, no access state in the story | SCR-05 row adds Empty, Loading, Error and No access as Not specified in the source documents (CG-ALL-110). |
| RWB-ITG-TE010-ITG | R-24176 | CG-ALL-111 | 15 | SCR-07 has no empty, loading, error, no access state in the story | SCR-07 row adds Empty, Error and No access as Not specified in the source documents (CG-ALL-111). |
| RWB-ITG-TE010-ITG | R-24177 | CG-ALL-112 | 15 | SCR-09 has no empty, loading, error, no access state in the story | SCR-09 row adds Empty, Error and No access as Not specified in the source documents (CG-ALL-112). |
| RWB-ITG-TE010-ITG | R-30093 | NEWAC-RWB-ITG-TE010-ITG-AC10 | 7, 16 | AC10: a consumed call fails or does not answer (no criterion covers a failed call) | Added Scenario AC10 in section 7 (2 s timeout from ADR-020) and test case TC-ITG-TE010-ITG-10 in section 16. |
| RWB-ITG-TE010-ITG | R-30094 | NEWAC-RWB-ITG-TE010-ITG-AC11 | 7, 16 | AC11: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Added AC11 scenario in section 7 and test row TC-ITG-TE010-ITG-12 in section 16. |
| RWB-ITG-TE010-ITG | R-30095 | NEWAC-RWB-ITG-TE010-ITG-AC9 | 7, 16 | AC9: §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Added AC9 scenario in section 7 covering BR8 and test row TC-ITG-TE010-ITG-11 in section 16. |
