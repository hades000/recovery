# RWB-ITG-W2 Wave 2 integration - review pack, part 5 of 5 (RWB-ITG-E2041-ITG to RWB-ITG-W2J01-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 158 |
| Cross-document (pending in another document) | 139 |
| Not applied (value not in the sources) | 19 |
| Open business decisions | 11 |
| Register gaps linked | 100 |
| Unconfirmed assumptions | 0 |
| Lint findings | 4 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E2041-ITG | 20 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2041 ITG Rule change governance and audit report - integration v2.md |
| RWB-ITG-E2042-ITG | 20 | 33 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2042 ITG Epic 2 rule packages in Drools - integration v2.md |
| RWB-ITG-E2043-ITG | 16 | 17 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2043 ITG Temporal and Drools integration pattern and reference case workflow - integration v2.md |
| RWB-ITG-E3006-ITG | 11 | 18 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E3006 ITG Calculate the plan installment - integration v2.md |
| RWB-ITG-E3010-ITG | 23 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E3010 ITG Book the plan and set the schedule - integration v2.md |
| RWB-ITG-E3013-ITG | 14 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E3013 ITG Check encumbrance and eligibility before negotiation - integration v2.md |
| RWB-ITG-E3017-ITG | 18 | 12 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E3017 ITG Release the collateral after settlement - integration v2.md |
| RWB-ITG-E3026-ITG | 19 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E3026 ITG Re-appraise a held asset on cycle - integration v2.md |
| RWB-ITG-W2J01-ITG | 17 | 7 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG W2J01 ITG Wave 2 journey end to end - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E2042-ITG | R-09466 | CG-ALL-805 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-E2041-ITG, RWB-P3-E2041-APP, RWB-P3-E2041-CON, RWB-P4-E2041-APP, RWB-P7-E2041-APP | R-22719 | GAP-0963 | Register gap | Solution architect with internal audit | The record code and the field shape of a rule-change authority and of an audit export inside a decision-record entry are not specified | Carry the capability area, the right, the action, the version label, the author reference, the period, the package, the format, the row count and the matrix version in the actions list of the decision-record entry, reuse AC-READ, AC-DENY and AC-EXPT rather than minting a fourth code, and add the fields in the next LDM version with audit. |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-22736 | GAP-1306 | Register gap | Center of excellence analyst with the P3 reference-data owner and the business owner | The decision code of a reference-case step and the value set of LOV-DECISION are not fixed by any source | Enumerate LOV-DECISION in the P3 reference-data load with the route and approval codes of the FSD P7 and fix the code of a route move; until then the ledger stores the code the fact carries, validates it against the list in force, and the reference-data fake supplies the value the reference package uses |
| RWB-ITG-E3006-ITG, RWB-S2-E3006-APP, RWB-S2-E3006-CON | R-22743 | GAP-0423 | Register gap | QA lead with the integration lead and the data product owner (P1 rwb-source-data, P3 rwb-case) | The harness repository, the SIT environment, the seeding set, the evidence format and retention, the pass or fail gate and the exact fake responses for RWB-ITG-E3006-ITG are named by no read source | Agree the harness repository, the SIT environment and the seeding set at the wave 2 entry check; name the P1 data product code for the ALS payoff facts and the P3 list code for the range in the contract registry; fix the evidence report shape, its retention and the pass or fail gate in the wave entry checklist; generate the five stubs from the published contracts and pin their versions in the run report. |
| RWB-ITG-E3006-ITG, RWB-S2-E3006-APP, RWB-S2-E3006-CON | R-22745 | GAP-2655 | Register gap | Business lead of S2 and the P3 rwb-case reference-data owner | The FSD does not say whether the range the officer may move within is an amount band or an installment range | The business lead confirms the unit at the wave 2 contract freeze. If an installment range is wanted, the element gains two optional fields in a compatible change and no acceptance criterion changes. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-28878 | GAP-1309 | Register gap | Compliance and PDPA officer with the solution architect and the platform observability team | The shape and route of the chain-check break report, and whether JOB-14 writes a ledger entry of its own, are not fixed | Agree the report fields, the alert route and the result retention with Compliance and the platform observability team, and state in the ledger run book whether the check is recorded as an operational event or as a decision record; until then ASM-B-P7-05-E2043-6 holds and the check writes no ledger row |
| RWB-ITG-E2043-ITG, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2043-APP | R-28879 | GAP-1310 | Register gap | Solution architect with the Compliance and PDPA officer and the owners of the points of no return (S6, S7, S5, S4) | The strict-mode acknowledgement and the daily seal of the ledger hash are named by the architecture and no story of this key owns them | Raise the seal and the strict-mode acknowledgement as their own stories of the P7 epic with the Risk and Internal Audit sign-off that the ADR-009 change needs, and fix the seal manifest, its storage path and its schedule and the confirmation read together; until then ASM-B-P7-05-E2043-7 holds and this story builds only the ledger they consume |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-ITG-E2042-ITG | R-33390 | ASM-ALL-805 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E3006-ITG | R-35592 | ASM-0598 | Register assumption |  | The integration and QA harness for RWB-E3-006 is carried at status Draft on Day 1 with the following working read: one harness runner keyed by story and business date, five WireMock stubs (rwb-treatment, rwb-case, rwb-source-data, rwb-decision, rwb-access) generated from the published contracts with each version pinned in the run report, one event probe over rwb.treatment.events.v1, rwb.case.events.v1 and rwb.decision-record.v1, and one evidence report per business date; SIT only, never UAT or production; seeding through the owning services' published operations only and never a schema write; the case at ROUTE_APPROVED_SETTLEMENT with its settlement treatment and the ALS payoff facts for its account; the payoff read through the P1 products contract and the range through the P3 reference-data contract; the pass or fail gate held on the evidence report and agreed at the wave 2 entry check. The harness repository, the SIT environment specification, the seeding set, the evidence format and retention, the pass or fail gate wording, the data product code, the list code and the exact fake response values stay open placeholders in the story. | QA lead, integration lead, P1 rwb-source-data, P3 rwb-case and the wave 2 entry check |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E2041-ITG | R-03885 | DOR-RWB-ITG-E2041-ITG-17 | header | Definition of Ready item 17 Dependencies: Fail | P3/P4/P7-E2041-APP are not built yet, and no text edit changes that. There is no RWB-P7-E1073-CON file under _work/msr, and naming a substitute key is not allowed. |
| RWB-ITG-E2041-ITG | R-03886 | DOR-RWB-ITG-E2041-ITG-21 | header | Definition of Ready item 21 Contract published: Fail | RWB-P3-E2041-CON is already listed. Item 21 needs CON stories marked Done and listed in the Service Contract Catalog. Neither was found, and story text cannot set either. |
| RWB-ITG-E2041-ITG | R-03887 | DOR-RWB-ITG-E2041-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No published contract fake library version was found in the story or fragment files. Recording one would mean inventing a version. |
| RWB-ITG-E2042-ITG | R-03890 | DOR-RWB-ITG-E2042-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record exists for this story. Definition of Ready v3 item 14 and DT05 give only the sign-off rule, so claiming a sign-off would invent a fact. |
| RWB-ITG-E2042-ITG | R-03891 | DOR-RWB-ITG-E2042-ITG-16 | section header | Definition of Ready item 16 Size: Fail | No size value is in the source documents; the squad sizes the story at refinement. |
| RWB-ITG-E2042-ITG | R-03892 | DOR-RWB-ITG-E2042-ITG-17 | 13 | Definition of Ready item 17 Dependencies: Fail | No source says whether the four E2042-APP stories are done; that is board state. RWB-P7-E1073-CON (story L346, DP-04 row) is not in the given text and stays under CG-ALL-799. |
| RWB-ITG-E2042-ITG | R-03894 | DOR-RWB-ITG-E2042-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | This story publishes FakePack itself (story L366, L383). No published version exists in the story or sources, so recording one would invent a value. |
| RWB-ITG-E2042-ITG | R-22724 | GAP-0421 | 13 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Harness repository, SIT environment, seeding, evidence format and gate values are not in the source documents; the Environment bullet keeps Not specified (GAP-0421; ASM-0596). |
| RWB-ITG-E2042-ITG | R-28856 | GAP-1302 |  | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | The package title, dry-run breakdown, MSG-P3-015 text and switch-off answer are not specified, and no story edit resolves them. |
| RWB-ITG-E2043-ITG | R-03898 | DOR-RWB-ITG-E2043-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value is in the sources. The Size row records it as Not specified and notes that the squad sizes at refinement. |
| RWB-ITG-E2043-ITG | R-14431 | DOR-RWB-ITG-E2043-ITG-15 |  | Definition of Ready item 15 INVEST: Partial | Size is set by the squad at refinement. No visible source states that the story fits a sprint, so the Size row records it as Not specified. |
| RWB-ITG-E2043-ITG | R-28875 | GAP-0724 | 3 | Reference fixture lifecycle, store and owner for the synthetic case | No source gives the fixture lifecycle, store or owner. §3 records them as Not specified (GAP-0724). |
| RWB-ITG-E3006-ITG | R-03906 | DOR-RWB-ITG-E3006-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size exists in the sources. The header row Size records this, and the squad sizes the story at refinement; the item stays open until then. |
| RWB-ITG-E3006-ITG | R-03908 | DOR-RWB-ITG-E3006-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No published fake library version exists in the sources, and section 12.8 only says stub versions are pinned in the run report. The header row records the gap, and the item stays open until a fake is published. |
| RWB-ITG-E3017-ITG | R-03925 | DOR-RWB-ITG-E3017-ITG-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-ITG-W2 found in the story or in the sources searched. Writing a sign-off without the record would invent an approval. |
| RWB-ITG-E3017-ITG | R-03927 | DOR-RWB-ITG-E3017-ITG-21 | header | Definition of Ready item 21 Contract published: Fail | RWB-ITG-E3017-CON does not exist. The only E3017 contract story has a key named in neither this story nor the item, so the CON dependency cannot be added. |
| RWB-ITG-E3017-ITG | R-03928 | DOR-RWB-ITG-E3017-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No published fake library version found in the sources. The S2 E3017 contract story is Draft and lists publication as a criterion, not as done. A version would be invented. |
| RWB-ITG-W2J01-ITG | R-04194 | DOR-RWB-ITG-W2J01-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off in the story or any source read (DoR and Done v4 item 14; Decision Log v12 DT05 gives timing only), so a sign-off date or approver would be invented. |
| RWB-ITG-W2J01-ITG | R-04197 | DOR-RWB-ITG-W2J01-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in the story or any source read (DoR and Done v4 item 22, Service Template Specification v1, Integration Test Plan v1); a version would be invented. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01730 | RWB-ITG-E2041-ITG | CG-ALL-791 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise through the rwb-access provider CON story (P4), or the consumer switches to a published operation. |
| CDC-01733 | RWB-ITG-E2041-ITG | DOR-RWB-ITG-E2041-ITG-8 | 12.2, 12.4 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml (see CG-ALL-791). |
| CDC-01745 | RWB-ITG-E2042-ITG | CG-ALL-798 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story, or the story consumes a published operation instead. |
| CDC-01748 | RWB-ITG-E2042-ITG | DOR-RWB-ITG-E2042-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise (CG-ALL-798). Event-type detcheck is resolved in the story under CG-ALL-800. |
| CDC-01795 | RWB-ITG-E3006-ITG | CG-ALL-812 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story, or the story consumes a published operation. |
| CDC-01798 | RWB-ITG-E3006-ITG | DOR-RWB-ITG-E3006-ITG-8 | find it | Publish POST /api/recovery/access/v1/authorise (CG-ALL-812). Event type part resolved in the story under CG-ALL-813. |
| CDC-01813 | RWB-ITG-E3010-ITG | CG-ALL-820 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation. |
| CDC-01816 | RWB-ITG-E3010-ITG | DOR-RWB-ITG-E3010-ITG-8 | 12.2, 12.4 | Event part fixed in story; authorise path depends on rwb-access publishing the operation. |
| CDC-01822 | RWB-ITG-E3013-ITG | CG-ALL-828 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |
| CDC-01826 | RWB-ITG-E3013-ITG | DOR-RWB-ITG-E3013-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml; event type fix already applied in story |
| CDC-01837 | RWB-ITG-E3017-ITG | CG-ALL-836 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the story consumes a published operation |
| CDC-01838 | RWB-ITG-E3017-ITG | DOR-RWB-ITG-E3017-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise, or consume a published operation |
| CDC-01849 | RWB-ITG-E3026-ITG | CG-ALL-845 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-01852 | RWB-ITG-E3026-ITG | DOR-RWB-ITG-E3026-ITG-8 | 12.2, 12.4 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-02311 | RWB-ITG-W2J01-ITG | CG-ALL-853 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the rwb-access provider CON story |
| CDC-02312 | RWB-ITG-W2J01-ITG | DOR-RWB-ITG-W2J01-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml; the event-type P1 is resolved in the story |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01742 | RWB-ITG-E2041-ITG | CG-ALL-795 | 18 | Align the REQ-CWC-013 and REQ-DRI-011 test lists in the RTM with RWB-ITG-E2041-ITG section 18. |
| CDC-01751 | RWB-ITG-E2042-ITG | DOR-RWB-ITG-E2042-ITG-12 | 18 | Reconcile its test case lists for this story with §18 (TC-E2-042-01-ITG to TC-E2-042-06-ITG and the new TC-E2-042-07-ITG) |
| CDC-01754 | RWB-ITG-E2042-ITG | GAP-2503 | 12 | Declare the nine consumed operations, name the workflow matchPayments with its four activities, and record in the RTM that legacy AC1, AC3, AC4 and AC5 have no story in this split. |
| CDC-01770 | RWB-ITG-E2042-ITG | CG-ALL-802 | 18 | Align the test case lists for REQ-CWC-013 and REQ-CWC-014 with section 18 of this story in the next RTM version. |
| CDC-01789 | RWB-ITG-E2043-ITG | CG-ALL-809 | 18 | Align the traced test cases of REQ-DRI-001 and the other three differing requirements with section 18 of this story in the next version. |
| CDC-01802 | RWB-ITG-E3006-ITG | DOR-RWB-ITG-E3006-ITG-12 | 18 | Align the test lists for REQ-S2-004, REQ-RDF-002, REQ-DRI-001 and REQ-DRI-005 to §18 of this story. The story keeps five test cases in §16. |
| CDC-01809 | RWB-ITG-E3006-ITG | CG-ALL-816 | 18 | Align the test lists for the three requirements in the evidence with section 18 of RWB-ITG-E3006-ITG in the next RTM version. |
| CDC-01812 | RWB-ITG-E3006-ITG | GAP-2653 | find it | Allocate a requirement ID to FEAT-TRT-06 in the C1 PRD and add the RTM row; both stories then take the ID in a minor version. No acceptance criterion changes. |
| CDC-01821 | RWB-ITG-E3010-ITG | CG-ALL-824 | 18 | RTM v7 lists tests from other stories; those lists are not aligned until the RTM values are confirmed. Only this story's TC-07 is added to REQ-DRI-007. |
| CDC-01830 | RWB-ITG-E3013-ITG | DOR-RWB-ITG-E3013-ITG-12 | 16, 18 | Section 16 now holds nine test cases (TC-07 to TC-09 added for AC4 to AC6). RTM v7 and Test Cases v8 need the ITG rows (CG-ALL-830). |
| CDC-01836 | RWB-ITG-E3013-ITG | CG-ALL-831 | 18 | Align the test lists for REQ-RDF-004, REQ-DRI-001 and the third listed requirement with section 18 of RWB-ITG-E3013-ITG in the next version. |
| CDC-01846 | RWB-ITG-E3017-ITG | CG-ALL-840 | 18 | Align the test lists for REQ-DRI-007 and the other differing requirements with section 18 in the next RTM version. |
| CDC-01847 | RWB-ITG-E3017-ITG | GAP-3213 | 18 | Story section 18 keeps REQ-RDF-004 as the E3 integration trace with an explanatory note. The citation must be added in the owning legacy stories and RTM v7. No acceptance by other owners is asserted. |
| CDC-01860 | RWB-ITG-E3026-ITG | CG-ALL-849 | 18 | Align the REQ-RDF-004 test list with the story test case TC-E3-026-03-ITG or the legacy test cases in the story trace. |
| CDC-02314 | RWB-ITG-W2J01-ITG | DOR-RWB-ITG-W2J01-ITG-12 | 18 | Next version: add the story section 18 TC-W2J01 IDs to the test cases of REQ-CHO-006, REQ-CHO-009, REQ-RDF-004, REQ-DVH-002, REQ-DRI-005 and REQ-ILG-005, keeping existing tests. |
| CDC-02317 | RWB-ITG-W2J01-ITG | CG-ALL-856 | 18 | Align the test lists of the six traced requirements to RWB-ITG-W2J01-ITG section 18 in the next RTM version; section 18 of this story is unchanged. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01764 | RWB-ITG-E2042-ITG | GAP-2396 | find it | Correct the P6 Comms to P7 Decision cell of the connection matrix in the next diagram issue; no second consumer is added on the notice path. |
| CDC-01804 | RWB-ITG-E3006-ITG | GAP-1702 | none | Re-base each listed step as a step of TreatmentWorkflow started by rwb-case and by service events. Add no Schedule or batch trigger to this service. |
| CDC-01827 | RWB-ITG-E3013-ITG | GAP-1696 | 12.2 | Add S2 to P1 REST cell; S2 reads source facts only through rwb-source-data (A2.6.3.1, A2.13.2, A2.10.2, A2.17.2) |
| CDC-01831 | RWB-ITG-E3013-ITG | GAP-1705 | header | Add the two cells this service needs: S5 asset take-on, and rwb-integration CCMS release and Land Office title check |
| CDC-01854 | RWB-ITG-E3026-ITG | GAP-1750 | 12.2 | Add S5 to the P1 cell of the connection matrix |
| CDC-01859 | RWB-ITG-E3026-ITG | GAP-1758 | 7; 8; 16 | AC3, BR1, BR2 and TC-03 now use the rwb-valuation contract. Step 7, step 9 and the §12.4 rwb-integration file events wait for the matrix ruling in Architecture v5. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01800 | RWB-ITG-E3006-ITG | CG-ALL-814 | 16 | Add rows for TC-E3-006-01-ITG to TC-E3-006-05-ITG with Given, When and Then copied from the criteria they cover in this story. |
| CDC-01817 | RWB-ITG-E3010-ITG | CG-ALL-822 | 16 | Add rows TC-E3-010-01-ITG to TC-E3-010-06-ITG to the Story test cases tab in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-01818 | RWB-ITG-E3010-ITG | DOR-RWB-ITG-E3010-ITG-12 | 16, 18 | Add story test cases TC-E3-010-01-ITG to TC-E3-010-07-ITG to Story test cases; align RTM v7 test lists to section 18. |
| CDC-01828 | RWB-ITG-E3013-ITG | CG-ALL-830 | 16 | Section 16 lists nine ITG test cases (TC-E3-013-01-ITG to TC-E3-013-09-ITG), and none of them are in Test Cases v8. Rows are to be added there. |
| CDC-01840 | RWB-ITG-E3017-ITG | CG-ALL-838 | 16 | Add rows TC-E3-017-01-ITG to TC-E3-017-06-ITG with Given, When and Then copied from the criteria they cover. |
| CDC-01855 | RWB-ITG-E3026-ITG | CG-ALL-847 | 16 | Add rows for TC-E3-026-01-ITG to TC-E3-026-06-ITG, with Given, When and Then copied from the criteria they cover |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01734 | RWB-ITG-E2041-ITG | DOR-RWB-ITG-E2041-ITG-1 | 1 | Add the role 'member of the integration and QA team' as a role code or role name, or name the existing role the harness runs as. |
| CDC-01749 | RWB-ITG-E2042-ITG | DOR-RWB-ITG-E2042-ITG-1 | 1 | Add or confirm a role code for the integration and QA team harness operator so §1 can name it |
| CDC-01780 | RWB-ITG-E2043-ITG | DOR-RWB-ITG-E2043-ITG-1 | 1 | Add the role 'member of the integration and QA team' or align the §1 role to an existing role code there |
| CDC-02313 | RWB-ITG-W2J01-ITG | DOR-RWB-ITG-W2J01-ITG-1 | 1 | Add a role code or role name for the QA team harness operator that section 1 can cite |
| CDC-02315 | RWB-ITG-W2J01-ITG | DOR-RWB-ITG-W2J01-ITG-6 | 10 | Add role RW-OFF, recovery officer (the synthetic user the harness drives), as used in section 10. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01732 | RWB-ITG-E2041-ITG | DOR-RWB-ITG-E2041-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-W2 and EP02 in the epic design record. |
| CDC-01796 | RWB-ITG-E3006-ITG | DOR-RWB-ITG-E3006-ITG-14 | find it | Confirm and record the signed epic design sign-off for RWB-ITG-W2. |
| CDC-01814 | RWB-ITG-E3010-ITG | DOR-RWB-ITG-E3010-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-E3010-ITG in the epic design record for RWB-ITG-W2. |
| CDC-01850 | RWB-ITG-E3026-ITG | DOR-RWB-ITG-E3026-ITG-14 | none | Record the signed epic design sign-off against RWB-ITG-E3026-ITG |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01743 | RWB-ITG-E2041-ITG | GAP-0203 | n/a | Add payment_match_rule row: owning service P7, target schema rwb_decision, marked retired by D-RCV-36 T10; rule lives in the PAYMENT_MATCH rule package; keep all 13 fields. |
| CDC-01803 | RWB-ITG-E3006-ITG | GAP-1707 | 8 | Name the package codes, version labels and owners for RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH in rwb-decision before wave 3 release, and record package and rule version on each treatment. |
| CDC-01848 | RWB-ITG-E3017-ITG | GAP-1700 | 8 | Add a TreatmentClosed row: producer rwb-treatment, topic rwb.treatment.events.v1, keyed by caseId, consumers rwb-case and rwb-reporting, no EV number until allocated. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01746 | RWB-ITG-E2042-ITG | CG-ALL-799 | 13 | Create story RWB-P7-E1073-CON, or the solution architect names an existing story key for that capability and the dependency is updated to it. |
| CDC-01747 | RWB-ITG-E2042-ITG | DOR-RWB-ITG-E2042-ITG-21 | header | Create contract story RWB-ITG-E2042-CON and add it as the CON dependency of RWB-ITG-E2042-ITG. |

### RWB-P3-E2042-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01750 | RWB-ITG-E2042-ITG | DOR-RWB-ITG-E2042-ITG-10 | find it | Add empty, loading, error and no access states for SCR-39 to that story |
| CDC-01765 | RWB-ITG-E2042-ITG | GAP-0721 | find it | Keep registry, seeding, admin operations, approval, rollback and JOB-20 in RWB-P7-E2042-APP per ASM-A6-tables-3; keep workbooks, model cache, checksum, atomic swap, catalog read and schema assertion here; prove AC1 to AC3 against the rwb-decision contract mock. |

### OTHER:RWB-E2-027 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01757 | RWB-ITG-E2042-ITG | GAP-1297 | section 7 | Background comment records that the conflict is for the RWB-E2-027 owner to reconcile. |
| CDC-01759 | RWB-ITG-E2042-ITG | GAP-3180 | section 7 | This story keeps its order EXACT, WINDOW, PARTIAL throughout. The difference with RWB-E2-027 needs a ruling with its owner. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01786 | RWB-ITG-E2043-ITG | GAP-1305 |  | Add the five-minute collection target and the 02:00 chain-check time as parameters, each with a name, version and owner. |
| CDC-01857 | RWB-ITG-E3026-ITG | DOR-RWB-ITG-E3026-ITG-20 | 8 | Add keys for the provision thresholds, step sizes and re-appraisal interval once the NPA owner sets them |

### RWB-S2-E3013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01824 | RWB-ITG-E3013-ITG | DOR-RWB-ITG-E3013-ITG-21 | Header | Publish readiness contract v1 |
| CDC-01825 | RWB-ITG-E3013-ITG | DOR-RWB-ITG-E3013-ITG-22 | header | No published fake library version was found. The header row marks it as not specified, and publishing the fake belongs to RWB-S2-E3013-CON. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01731 | RWB-ITG-E2041-ITG | CG-ALL-792 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that delivers the DP-04 rule package contract dependency. |

### OTHER:Technical Specification P7; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01735 | RWB-ITG-E2041-ITG | GAP-1615 | Header | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule-version and rule-package operations; remove them from TSD P3 and TSD P4; set x-module of the nine rule paths to P7. |

### OTHER:TSD P3 v3; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01736 | RWB-ITG-E2041-ITG | GAP-1993 |  | Remove rule_package, rule_package_version, rule_row and rule_test_case from P4 and P3 ownership; the registry sits in rwb-decision and is read through the P7 contract (DP-04). |

### OTHER:TSD P4 v3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01737 | RWB-ITG-E2041-ITG | GAP-1565 |  | Re-issue TSD P4 without the four rule tables, RulePackageStore and the six rule-package operations; move FEAT-ADM-02 to rwb-decision; set x-module of the six paths to P7. |

### OTHER:rwb-case API file and ownership.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01738 | RWB-ITG-E2041-ITG | GAP-0718 |  | Publish GET /api/recovery/case/v1/admin/rule-change-audit with the section 11 entry fields and Rules and parameters R; add the ownership map row before the wave 2 contract baseline. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx; RWB-ITG-E2041-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01739 | RWB-ITG-E2041-ITG | GAP-0962 | 16 | Publish one RULES_AND_PARAMETERS row set giving every role's letter for rule change; state the reference data administrator limits; correct TC-E2-041-11 to a dash-letter role. |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01740 | RWB-ITG-E2041-ITG | GAP-0964 |  | Add GET /api/recovery/access/v1/rule-authority and POST /api/recovery/access/v1/rule-report-exports as P4 operations with their query, body and answer fields; freeze the action set and refusal reasons at RWB-P3-E2041-CON review. |

### OTHER:TSD P4 v3 T6.1 permission data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01741 | RWB-ITG-E2041-ITG | GAP-0965 |  | Add the rwb-decision service identity and the gateway-bff route with the R letter in RULES_AND_PARAMETERS only; confirm with the security administrator before the authorise contract is frozen. |

### OTHER:Contract README (published field contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01744 | RWB-ITG-E2041-ITG | GAP-0720 | n/a | State a deprecation window for a published field. Audit read retention follows the decision-record retention. Window not specified in the source documents (GAP-0720). |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01752 | RWB-ITG-E2042-ITG | GAP-0966 | find it | Add rule-package action names, request and answer fields and a change decision code to POST /authorise; agree the code with the RWB-E1-039 access-log owner; stub both in the contract fake |

### OTHER:Technical Specification P7; OTHER:Technical Specifications P3 and P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01753 | RWB-ITG-E2042-ITG | GAP-1615 | 4 | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule-version and rule-package operations; remove them from TSD P3 and P4; set x-module P7 on the nine rule paths. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3 T5.2; RWB-P2-E2007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01755 | RWB-ITG-E2042-ITG | GAP-0657 | 12 | Keep JOB-08 with rwb-integration and mark the rwb-payment owner row of slide 44 superseded; read ACE facts through rwb-source-data and supersede TSD P2 v3 T5.2. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01756 | RWB-ITG-E2042-ITG | GAP-1292 | 7 | Reconcile PM-2026.12 from 2026-12-01 and PMT-2026.12 from 2026-12-15 into one PAYMENT_MATCH version row before SIT promotion. |

### OTHER:RWB-E2-027 build notes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01758 | RWB-ITG-E2042-ITG | GAP-3179 | 4 | Drop the payment_match_rule load in step 1 and its repository read; load PAYMENT_MATCH rows through the rule package endpoints and read them through RuleCatalog.row. |

### RWB-ITG-E2035-ITG; RWB-P2-E2035-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01760 | RWB-ITG-E2042-ITG | GAP-0667 | 4 | Serve GET /cases/{caseId}/next-action from the integration base under DP-13; fix the consumed fields, operation names, Schedule values and message texts; correct the Ownership Map row. |

### RWB-P2-E2035-CON; RWB-ITG-E2035-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01761 | RWB-ITG-E2042-ITG | GAP-0668 | 12 | Baseline the next action contract with three operation names, nine consumed shapes, Schedule values, the error mapping and five message texts; confirm element names with rwb-case, rwb-access and rwb-decision. |

### RWB-P2-E2035-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01762 | RWB-ITG-E2042-ITG | GAP-0669 | 13 | Fix the rwb-integration login, secret reference and probe checks; add the next-action-check job catalogue row with its run book path; record the read path ruling in the Ownership Map; review the three runbook entries with the on-call rota. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01763 | RWB-ITG-E2042-ITG | GAP-2406 | 3 | Move the registry valid-from of RES-2026.12 from 2026-12-15 to 2026-12-01, as the gap's proposed fix recommends, before the wave-2 fixture is frozen; then align the ITG fixtures. |

### OTHER:rwb-decision OpenAPI contract (P7 rwb-decision owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01766 | RWB-ITG-E2042-ITG | GAP-0722 | find it | Publish GET /rule-models/{packageCode}/{version} and GET /rule-catalog/{ruleId}?packageVersion= with packageCode, versionLabel, checksum, model content, compiler version, valid-from date, and the catalog fields; add both to the Ownership Map API list. |

### OTHER:TSD P4 v3 permission matrix (rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01767 | RWB-ITG-E2042-ITG | GAP-0967 | find it | Publish the service-identity rows of the permission matrix across the fourteen capability areas and record the capability area each rule package serves as a package attribute of rwb-decision. |

### OTHER:TSD P7 v2 (rwb-decision schema) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01768 | RWB-ITG-E2042-ITG | GAP-1301 | find it | Add rule_package, rule_package_version, rule_row and rule_test_case to T3.1 of rwb_decision at the next version; the P3 and P4 declarations are not built. |

### RWB-P6-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01769 | RWB-ITG-E2042-ITG | GAP-2399 | find it | When no version is in force, refuse the request with MSG-GEN-006, create no notice row, dispatch nothing and add no hold reason. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01771 | RWB-ITG-E2042-ITG | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime; each package version names its format; conversion is a version change with its own test evidence; load checks and model fetch cover both formats. |

### OTHER:rwb-decision rule_package_version data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01772 | RWB-ITG-E2042-ITG | GAP-1357 | find it | Keep PM-2026.12 (in force from 2026-12-01) as the single version for PAYMENT_MATCH; reconcile the PMT-2026.12 label to that one version row before SIT. |

### OTHER:rwb-comms notice story (route-set read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01773 | RWB-ITG-E2042-ITG | GAP-2400 | find it | Read action_text, owner_role and timer_spec in rwb-comms only where a notice is decided by a route-set rule; keep the case next action with RWB-E2-035 and rwb-case; test the copy with the R-RES-04 values. |

### RWB-P3-E2042-INF; RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01774 | RWB-ITG-E2042-ITG | GAP-0723 | find it | Set the Blob container to write-once with no deletion and per-environment audit retention; size the pod by a load test caching 20 versions; expose alert windows, replica counts and probe timings as reviewed values files. |

### OTHER:TSD P4 v3 (T3.1 and T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01775 | RWB-ITG-E2042-ITG | GAP-0968 | find it | Correct T3.1 and T6.1 in the next version so the four rule tables and registry operations belong to P7; keep only the P4 rows for rights and the access log. |

### OTHER:parameters contract (DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01776 | RWB-ITG-E2042-ITG | GAP-0969 | find it | Add a parameter row for the lifetime of a cached authorise answer with value Not specified in the source documents (GAP-0969); keep the AccessPolicyChanged.v1 version-keyed drop; confirm one access-log entry per dry run. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Tables sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01777 | RWB-ITG-E2042-ITG | GAP-1994 | 8 | Add a row for the PAYMENT_MATCH package, owned by rwb-decision (P7), as the home of the match rules; keep the proceeds row for rwb-payment (P8); give payment_match_rule no row. |

### Epic design record; OTHER:Ways of Working and Governance v3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01778 | RWB-ITG-E2043-ITG | DOR-RWB-ITG-E2043-ITG-14 | header | Record the signed EP02 epic design (date and Business lead role sign-off) covering RWB-ITG-E2043-ITG |

### RWB-P3-E2043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01779 | RWB-ITG-E2043-ITG | DOR-RWB-ITG-E2043-ITG-22 | header | Record the published contract fake library version that RWB-ITG-E2043-ITG pins |

### OTHER:Workflow Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01781 | RWB-ITG-E2043-ITG | GAP-2016 |  | Timer design is owned by P3 rwb-case with the platform team. This story builds no timer, so there is no story edit. |

### OTHER:Temporal and Drools Design v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01782 | RWB-ITG-E2043-ITG | GAP-2024 |  | Stage clock ownership is owned by P3 rwb-case with S8 rwb-deviation. This story builds no stage timer, so there is no story edit. |

### OTHER:Platform workflow kit (Temporal worker versioning policy) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01783 | RWB-ITG-E2043-ITG | GAP-0725 |  | Set the build ID to the release commit ID, pin builds with drain-on-complete, and apply the policy to all 19 services. |

### OTHER:Platform replay gate definition (DevOps pipeline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01784 | RWB-ITG-E2043-ITG | GAP-0726 |  | Replay one recorded history per acceptance path of the reference fixture, keep them with the contract jar, and take the MSG-P3-038 text from the message catalogue. |

### OTHER:AsyncAPI rwb.decision-record.v1 and OpenAPI of the decision-log operations (solution architect) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01785 | RWB-ITG-E2043-ITG | GAP-1304 |  | Publish the event schema and the two decision-log OpenAPI operations; approve the three ingest columns of decision_log_entry and the three message texts. |

### OTHER:Workflow Engine Design v3 section 7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01787 | RWB-ITG-E2043-ITG | GAP-2019 |  | Record the child failure path: retry the start with the same workflow ID, raise an incident with MSG-P3-037 when retries are exhausted, and leave the case in its last applied state. |

### OTHER:Workflow Engine Design v3 section 3 and Temporal and Drools Design v1 slide 26 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01788 | RWB-ITG-E2043-ITG | GAP-2018 |  | A pivot activity waits on the ledger acknowledgement using the retry policy of Workflow Engine Design v3 section 7 and a documented timeout; at timeout it fails with an incident without repeating completed steps. |

### OTHER:RWB-E2-043 contract story (baseline review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01790 | RWB-ITG-E2043-ITG | GAP-0727 |  | Settle the RecordAndApplyRequest record members (event key, rule result, state change, business date) and the package-specific outputs map schema, including field types, cardinality and required flags. |

### OTHER:ACE DB story of wave 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01791 | RWB-ITG-E2043-ITG | GAP-1307 |  | Allocate the rwb-decision schema login with its schema and keep the credential in the platform secret store; the story and its migration reference it as a secret. |

### OTHER:Workflow Engine Design v3 section 5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01792 | RWB-ITG-E2043-ITG | GAP-2021 |  | Define the child and kit workflow ID format: the parent generates one ID per child from the case ID and stage code, so a parent restart cannot create a second child for the same stage. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01793 | RWB-ITG-E2043-ITG | GAP-2053 |  | Record that the outbox and inbox rule applies to all 19 services as the target scope; keep the Epic 1 and Epic 2 outbox sentences as the as-built position; record the R-PREC rule with Architecture v5 taking precedence. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01794 | RWB-ITG-E2043-ITG | GAP-1308 | 13 | For RWB-ITG-E2043-ITG add as DP-added: H RWB-PLT-E1027-CON, E1072-CON, E1043-CON, TE006-CON, E1071-CON, E1047-CON, E1044-CON, N001-CON; C RWB-P3-E1073-CON, RWB-P3-E1043-CON. Keep Ready to start Day 1. |

### OTHER:Story set for service epic RWB-ITG-W2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01797 | RWB-ITG-E3006-ITG | DOR-RWB-ITG-E3006-ITG-21 | header | The header names RWB-P3-E1043-CON for reference data (R-22742). No contract story for service epic RWB-ITG-W2 is identified; the story set must hold it. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:FSD S2 sections A2.6.3.1; OTHER:A2.10.2; OTHER:A2.13.2; OTHER:A2.17.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01799 | RWB-ITG-E3006-ITG | GAP-1696 | find it | Add S2 to the P1 REST cell, and make S2 obtain every source fact only through the rwb-source-data contract, with no view or ACE table read. |

### RWB-ITG-E3006-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01801 | RWB-ITG-E3006-ITG | DOR-RWB-ITG-E3006-ITG-10 | none (no screen section in this story) | Add empty, loading, error and no-access states for SCR-14 and SCR-15 to their screen specification, or record that this harness has no screens. |

### OTHER:ACE DB grant for the rwb-treatment login; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01805 | RWB-ITG-E3006-ITG | GAP-2654 | none | The grant is a database action outside the story text. The header records no contract dependency for the grant until it is decided. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01806 | RWB-ITG-E3006-ITG | GAP-2652 | header | Publish the reference set identifiers, the four values and the freshness limit before the wave 2 tag. Correct T5.2 so the reference data owner is P3 rwb-case. |

### RWB-S2-E3006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01807 | RWB-ITG-E3006-ITG | GAP-2651 | none | Service owner confirms the plan-installment result element at the wave 2 contract freeze. If a table is wanted, declare its fields in a minor version of RWB-S2-E3006-CON. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01808 | RWB-ITG-E3006-ITG | GAP-2657 | find it | Attribute AC2 and TC-E3-006-02 to the settlement state story of this service; if none exists, raise a delta story. No file of this Work Package changes. |

### OTHER:Screen specification that defines SCR-14 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01810 | RWB-ITG-E3006-ITG | CG-ALL-817 | 15 | Section 15 now marks the empty, loading, error and no access states as Not specified. The screen specification must define them. |

### OTHER:Screen specification that defines SCR-15 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01811 | RWB-ITG-E3006-ITG | CG-ALL-818 | 15 | Section 15 now marks the empty, loading, error and no access states as Not specified. The screen specification must define them. |

### RWB-S2-E3010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01815 | RWB-ITG-E3010-ITG | DOR-RWB-ITG-E3010-ITG-22 | 12.8 | Publish the contract fakes planned in RWB-S2-E3010-CON flow step 10 and record the published fake library version. |

### OTHER:Functional Specification Document S2 (A2.10; OTHER:A2.11; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01819 | RWB-ITG-E3010-ITG | GAP-1703 | 2, 8 | Remove the booking, payment-matching and posting writes; rwb-payment owns them per Architecture v5; release request leaves through the integration contract. |

### OTHER:Gap register (GAP-0424) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01820 | RWB-ITG-E3010-ITG | GAP-0424 | 15 | Attach the agreed NLEADS and ALS interface, harness, seeding, evidence and pass or fail gate values to GAP-0424 before this story is reported Done |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01823 | RWB-ITG-E3013-ITG | DOR-RWB-ITG-E3013-ITG-14 | header | No signed design record exists for this epic. The header row 'Epic design sign-off' marks it as not specified, and the sign-off belongs to the epic design record. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01829 | RWB-ITG-E3013-ITG | DOR-RWB-ITG-E3013-ITG-10 | 15 | Add empty, loading, error and no-access states for SCR-14 and SCR-16 |

### OTHER:TSD S2 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01832 | RWB-ITG-E3013-ITG | GAP-2674 | header | Add the readiness, encumbrance, registration, title-set, hold and check-time fields to T3.1 and a field catalog to FSD S2 A2.13 per the working read of ASM-B2-S2-008-1 to -3 |

### OTHER:rwb-treatment contract v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01833 | RWB-ITG-E3013-ITG | GAP-2675 | none | Publish the readiness section, TitleSetTaskRequest, the three view ranges marked read only, and the 401, 403, 404, 422 and 503 responses per the working read of ASM-B2-S2-008-3 |

### OTHER:Recovery Workbench source documents (interface and harness specification) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01834 | RWB-ITG-E3013-ITG | GAP-0425 | 7, 15 | Publish the check interface with codes and fixture results, the SIT harness environment and repository, the two-case seeding set, the six fake values, and the evidence report format, retention and gate. |

### RWB-P3-E3013-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01835 | RWB-ITG-E3013-ITG | GAP-0736 | 7, 8 | Story states the S2/P3 boundary; the 2 s one-hop default is a call budget only. Requirement ID and field IDs remain Not specified. |

### OTHER:FSD S2 (A2.6.3.1; OTHER:A2.10.2; OTHER:A2.13.2; OTHER:A2.17.2); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01839 | RWB-ITG-E3017-ITG | GAP-1696 | 9 | Route source facts through the rwb-source-data contract; add S2 to P1 REST cell. Story already reads only via P1 and creates no direct read. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01841 | RWB-ITG-E3017-ITG | DOR-RWB-ITG-E3017-ITG-12 | 16, 18 | Section 16 now lists TCs for AC3 and AC5 to AC10, and marks AC1, AC2 and AC4 as run by RWB-S2-E3017-APP. The rows are absent from Test Cases v8 and RTM v7. |

### OTHER:Functional Specification Document S2 (A2.10; OTHER:A2.11; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01842 | RWB-ITG-E3017-ITG | GAP-1703 | none | Remove booking, payment matching and posting writes from A2.10, A2.11 and A2.17; take TreatmentBooked and PaymentMissed as inputs; rwb-payment owns posting. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:A2.13; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01843 | RWB-ITG-E3017-ITG | GAP-1705 | none | Add the S5 asset take-on path, the rwb-integration paths for the CCMS release and Land Office title check, and the two matrix cells. |

### OTHER:Technical Solution Design S2 v2 (T3.1; OTHER:T-A.1) and Functional Solution Design S2 v3 (A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01844 | RWB-ITG-E3017-ITG | GAP-2682 | 7 | Publish the release result, release instruction, confirmation read and case outcome per the working read of ASM-B2-S2-012-1 to -6 with RWB-S2-E3017-CON and RWB-S2-E3017-APP. |

### OTHER:rwb-treatment contract v1 (OpenAPI and event schemas) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01845 | RWB-ITG-E3017-ITG | GAP-2683 | 7 | Publish the collateralRelease section on GET /treatments/{treatmentId}, the events rwb.treatment.CollateralReleaseRequested.v1 and rwb.treatment.CollateralReleased.v1, and the release vocabulary and view column contract. |

### RWB-S5-E3026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01851 | RWB-ITG-E3026-ITG | DOR-RWB-ITG-E3026-ITG-22 | header | Publish the contract fake library of RWB-S5-E3026-CON and record its published version, so RWB-ITG-E3026-ITG can cite it |

### OTHER:Specification features sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01853 | RWB-ITG-E3026-ITG | GAP-1479 | none | Move FEAT-VAL-06 and FEAT-VAL-01 into the E3 release, or record their E3 criteria as signed off in E4 |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01856 | RWB-ITG-E3026-ITG | DOR-RWB-ITG-E3026-ITG-12 | 16, 18 | Align the test lists of REQ-S5-003 and REQ-RDF-004 in RTM v7 with section 18; add the six TC rows to Test Cases v8 |

### OTHER:split_plan.json; OTHER:S5 ownership rows; OTHER:Template and Rules v1 R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01858 | RWB-ITG-E3026-ITG | GAP-2869 | header | Add the C, I and X values for the H consumers, the DP-10 pattern with RWB-PLT-E1071-CON, and the re-appraisal record, requirement and AC3 evidence rows |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02316 | RWB-ITG-W2J01-ITG | DOR-RWB-ITG-W2J01-ITG-7 | 11 | Add field IDs DF-COL-023, DF-COL-025, DF-COL-031, DF-COL-033, DF-COL-036, DF-COL-039 and DF-COL-040 with the entity and field listed in section 11. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_decision.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20604 | RWB-ITG-E2042-ITG | R-28823 |  | rwb_decision.sql seeds only rule_package rows, not PAYMENT_MATCH versions. The PM-2026.12 single-version load and PMT label fix belong to rule_package_version data. uk_rule_package_version already enforces one row per label. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0203 | The entity Payment match rule has no row in the Ownership Map and no target table | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0420 | Rule-change report harness environment, seeding, evidence format, retention and composite route detail are not specified | Integration lead | Resolved (directive) |
| GAP-0421 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0422 | Reference workflow harness repository and SIT environment, seeding, evidence format and gate are not specified, and the ownership map holds no rwb-case outbox delivery read | Integration lead | Resolved (directive) |
| GAP-0424 | NLEADS and ALS interface detail, harness environment, seeding set and evidence gate for RWB-E3-010 are not specified | Integration lead with the QA lead | Resolved (directive) |
| GAP-0425 | The CCMS and Land Office check interface, the harness environment and seeding set, the fake response values and the evidence and gate of the early readiness harness are not in the sources | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0426 | The CCMS release interface, the harness pack and the case-state screen are not specified | Integration lead | Resolved (directive) |
| GAP-0427 | The re-appraisal harness pack, the fixed clock, the SVAF interface and the evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-0428 | The wave 2 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0718 | The case-side rule-change audit read has no row in the ownership map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
| GAP-0720 | Retention and lifecycle windows of the new audit read and its contract are not specified | Data steward | Resolved (directive) |
| GAP-0721 | The rule package registry is declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0722 | The rule-model and rule-catalog read operations have no published field-level shape | P7 rwb-decision owner | Resolved (directive) |
| GAP-0723 | Blob immutability period, pod memory for 20 KieBases, alert windows and probe timings are not specified | SCB IT infrastructure with the DevOps team | Resolved (directive) |
| GAP-0724 | Reference fixture lifecycle, store and owner for the synthetic case | TechX | Resolved (directive) |
| GAP-0725 | Worker build ID format and worker versioning policy are not stated | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0726 | Replay corpus, history retention and the text of MSG-P3-038 | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0727 | Field-level detail of RecordAndApplyRequest and of the rule outputs map | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0736 | The encumbrance-check slice leaves the requirement ID, the check-versus-state boundary, the S2 answer shape, the rule timer specs and three new field IDs unspecified | Tech lead | Resolved (directive) |
| GAP-0962 | The roles and letters of the rule-administration area differ between the work package line, the legacy authority table and TSD P4 v3 T6.1, and the legacy access test names a role the matrix gives the right | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0964 | The two operations of this slice, and their request and answer shapes, are absent from Architecture v5, the API Specification and the TSD P4 appendix | Solution architect with the API Specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0965 | Which right a service identity holds to ask this service about a person other than the session user is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0967 | rwb-access rule-package authority: the scope of a running service identity inside rwb-access and the capability area each rule package serves are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0968 | rwb-access rule-package authority: TSD P4 v3 gives P4 the four rule tables, while Architecture v5 and the ownership ruling put the rule registry in P7 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0969 | rwb-access rule-package authority: the lifetime of a cached authorise answer, the refresh trigger of the cached permission data and the granularity of the access-log entry of a dry run are not specified | Solution architect | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1298 | The decision code of a rule-governance entry is not named in any source this key may read | Decision log owner | Resolved (directive) |
| GAP-1299 | The name of the rwb-decision database login is not specified | ACE database administrator | Resolved (directive) |
| GAP-1300 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Business analyst | Resolved (directive) |
| GAP-1301 | The four rule registry tables are declared for P4 and P3 in their TSDs and are absent from the P7 TSD | Solution architect | Resolved (directive) |
| GAP-1302 | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Business analyst | Resolved (directive) |
| GAP-1303 | The BRD section pointers copied from the legacy story no longer match BRD v2 and v4 | Business analyst | Resolved (directive) |
| GAP-1304 | The payload of DecisionRecorded, the field set of the ledger ingest and the answer bodies of the two reads have no source | Solution architect, P7 rwb-decision, with the platform outbox and event team, the P3 business analyst and the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1305 | The collection target of five minutes and the chain-check time of 02:00 are named as values but no source names them as parameter rows | Center of excellence analyst with the P3 rwb-case team and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1307 | The name of the per-service database login of rwb-decision is not fixed by any source | ACE DB team with the P7 rwb-decision team | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1468 | The provision step thresholds and the held-asset re-appraisal interval are not specified | NPA and asset manager | Resolved (directive) |
| GAP-1479 | Epic 3 features depend on Epic 4 features that release a month later | Solution architect | Resolved (directive) |
| GAP-1565 | The rule package registry, the rule-package operations and the change report are claimed by the P4 technical specification while the Ownership Map gives them to rwb-decision | Solution architect with the rwb-decision contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1700 | TreatmentClosed has no event number and no row in the Ownership Map event sheet | Solution architect | Resolved (directive) |
| GAP-1701 | The plan timers are specified on the Workbench scheduler, which Architecture v5 replaces with durable timers | Solution architect | Resolved (directive) |
| GAP-1702 | The FSD triggers on a completed ACE batch, and AceDataReady does not reach this service while no S2 job exists in the job map | Solution architect with the P1 owner | Resolved (directive) |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1705 | The CCMS release, the Land Office title check and the asset take-on have no path from this service in Architecture v5 | Solution architect with the integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1707 | Three Drools packages are named for this service with no code, version label or owner | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1750 | FSD S5 reads the ACE asset, collateral and score views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1758 | The re-appraisal order leaves for SVAF, which Architecture v5 does not connect to this service and gives to rwb-valuation | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-1994 | payment_match_rule has no owner in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2018 | Strict-mode wait at a point of no return is not defined in this design | Service owner P7 rwb-decision with the saga owners S2, S5, S6 and S7 | Resolved (directive) |
| GAP-2019 | Child workflow start policy and failure path are not specified | Service owner P3 rwb-case with the stage owners S1 to S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2021 | Child and kit workflow ID format | Service owner P3 rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2024 | Who pauses the stage clock when the stage runs as a child | Service owner P3 rwb-case with S8 rwb-deviation | Resolved (directive) |
| GAP-2026 | Owning service of the PAYMENT_MATCH package is not stated in one place | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2034 | The UNIVERSAL package has no single owning service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2053 | Outbox scope: Epics 1 and 2 in version 3, every service in Arch v5 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2122 | The journey steps and test cases of each wave are not stated | QA team | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2396 | Architecture v5 slide 13 gives P6 to P7 a Temporal cell and no event cell, while RWB-P6-E1073-APP consumes RulePackageInForce from rwb.decision.events.v1 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2397 | No source states where the package version and checksum of a notice decision are stored, and the legacy story adds no column for them | Data steward | Resolved (directive) |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2399 | No source states the state a notice rests in, or the message, when no package version is in force | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2413 | No source gives the field-level shapes this story needs: the change-report element beyond its legacy field names, the CSV column order, the rulesChanged element, the decision-code and item-list values, the reconciliation read and the DP-02 login name | Solution architect | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2415 | The legacy story places the change checklist and the report in module P3 and the P4 package recovery.accessadmin.rulepackages with a P3 feature flag, while the target puts the registry, the checklist column and the decision log in rwb-decision | Solution architect | Resolved (directive) |
| GAP-2416 | Legacy AC1 approves ALLOCATION version ALLOC-2026.12 on 2026-12-02 while AC5 loads the same version on 2026-12-08 and approves it on 2026-12-09, so BR4 (verify on or after the load and before the approval) cannot hold in both readings | Business analyst P7 | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2651 | No source fixes the field list of the plan-installment result or where its band and floor are held | S2 rwb-treatment service owner and the P3 rwb-case reference-data owner | Resolved (directive) |
| GAP-2652 | The reference set that holds the band, the floor and the freshness limit, and the operation that reads it, are not published | P3 rwb-case owner, with the P4 rwb-access owner confirming the superseded row | Resolved (directive) |
| GAP-2653 | No requirement ID is allocated to FEAT-TRT-06 | Programme business analyst and the PRD owner of the S2 PRD | Resolved (directive) |
| GAP-2654 | Architecture v5 says the recovery.v_ace_* views are read only by rwb-source-data while DP-05 allows the service's own views | ACE DB owner, with the P1 rwb-source-data owner and the platform data owner | Resolved (directive) |
| GAP-2656 | No source names the trigger of the plan-installment step | S2 rwb-treatment service owner and the P3 rwb-case workflow owner | Resolved (directive) |
| GAP-2657 | AC2 of RWB-E3-006 is owned by no story of this Work Package | S2 rwb-treatment service owner and the story set coordinator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2665 | The booking trigger, the schedule shape, the ALS booking reference and the plan-timer mechanism are not specified for rwb-treatment | Tech lead of rwb-treatment with the P8 owner of the payment booking match and the platform workflow owner | Resolved (directive) |
| GAP-2666 | The booking and schedule element, its required set and the ALS acknowledgement reference are not specified for rwb-treatment | Contract owner of rwb-treatment with the operations booking owner | Resolved (directive) |
| GAP-2667 | RWB-E3-010 AC1 sends the agreed terms to NLEADS and ALS from the Workbench, while the FSD and the TSD keep the booking with the officer in the core bank and in NLEADS | Solution architect with the operations booking owner and the ACE Common owner | Resolved (directive) |
| GAP-2674 | The readiness check result, the title-set task, the trigger and the ACE status field are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P1 owner of the ACE read and the owner of the local decision-record library | Resolved (directive) |
| GAP-2675 | The published shape of the readiness section, of the title-set task request and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract and the P1 owner of the ACE read | Resolved (directive) |
| GAP-2682 | The release result, the release instruction, the confirmation read and the case outcome are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P8 owner of the payment contract, the P1 owner of the ACE read and the platform integration owner of the CCMS adapter | Resolved (directive) |
| GAP-2683 | The published shape of the release section, of the two release events, of the release vocabulary and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract, the P1 owner of the ACE read and the platform integration owner of the CCMS adapter | Resolved (directive) |
| GAP-2869 | RWB-S5-E3026: the cycle slice has no planned dependency row for its four consumed contracts or its Schedule library, and neither the plan nor the module model holds the re-appraisal record, the requirement id or the AC3 evidence | Solution architect | Resolved (directive) |
| GAP-2870 | RWB-S5-E3026-CON: the published surface of the cycle has no source for its appraisal properties, its reason and route vocabulary, the order path or the JOB-19 parameters | Solution architect | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E3006-ITG | skipped AC ID | 103 | missing: AC1, AC3 |
| RWB-ITG-E3010-ITG | skipped AC ID | 104 | missing: AC2, AC3, AC4 |
| RWB-ITG-E3017-ITG | skipped AC ID | 101 | missing: AC1, AC2, AC4 |
| RWB-ITG-E3026-ITG | skipped AC ID | 102 | missing: AC1, AC2, AC4 |
