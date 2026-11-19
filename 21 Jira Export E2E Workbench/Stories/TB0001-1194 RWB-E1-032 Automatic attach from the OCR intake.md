# TB0001-1194 [RWB-E1-032] Automatic attach from the OCR intake

| Field | Value |
|---|---|
| Jira | [TB0001-1194](https://scbjira.atlassian.net/browse/TB0001-1194) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Decision, R-Dependency, R-Requirement, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:33.628+0700 |
| Updated | 2026-11-18T16:54:59.024+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 6 |
| Comments | 5 |

## Description

As a case owner (RW-CASEOWN), I want documents from the OCR intake attached to their case automatically when the case ID or the account number is read, with unmatched or ambiguous documents held for a person who sees the OCR text and the candidate cases and attaches the document, so that no document is filed by hand when the case is clear and none is filed on the wrong case when it is not.

## Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake

  Background:
    Given case "RW-2026-000123" is open, owned by "TEST-CO-01" and linked to account "TEST-ACC-0001"
    Given case "RW-2026-000456" is open and linked to account "TEST-ACC-0002"
    Given case "RW-2026-000789" is closed
    Given parameter CLASSIFY_THRESHOLD is 0.80

  Scenario: AC1 Auto attach
    Given a scanned notice with the case ID "RW-2026-000123" read by OCR, classified "COURT_NOTICE" at 0.93 by classifier version "CLS-1.0"
    When intake completes
    Then the system stores the document on case "RW-2026-000123" with type "COURT_NOTICE", source "SCAN", classification_confidence 0.9300 and review_status "NOT_NEEDED" without a person
    Then one decision log entry "DOCATT" holds model version "CLS-1.0", confidence 0.93 and match method "CASE_ID"
    Then the system writes documentStored and the intake item has match_status "MATCHED" and the document ID

  Scenario: AC2 No match
    Given a scan with no readable case ID and no readable account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"
    Then GET /intake-items/{intakeItemId} returns its OCR text pages
    Then the system writes no document row

  Scenario: AC3 Two candidates
    Given a scan whose account number "TEST-ACC-0003" is linked to open cases "RW-2026-000321" and "RW-2026-000654"
    When intake completes
    Then the intake item has match_status "MULTIPLE"
    Then candidate_case_ids holds both cases and the Unmatched list on SCR-31 offers both
    Then the system writes no document row

  Scenario: AC4 Match by account number
    Given a scan with no case ID and the account number "TEST-ACC-0002", classified "DEMAND_LETTER" at 0.88
    When intake completes
    Then the system stores the document on case "RW-2026-000456"
    Then the decision log entry holds match method "ACCOUNT_NO"

  Scenario: AC5 Case ID and account disagree
    Given a scan with the case ID "RW-2026-000123" and the account number "TEST-ACC-0002"
    When intake completes
    Then the intake item has match_status "CONFLICT" and candidates "RW-2026-000123" and "RW-2026-000456"

  Scenario: AC6 Case ID that does not exist
    Given a scan with the case ID "RW-2026-999999" and no account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"

  Scenario: AC7 Only candidate is closed
    Given a scan with the case ID "RW-2026-000789"
    When intake completes
    Then the intake item has match_status "CASE_CLOSED" and candidate "RW-2026-000789"
    Then the system writes no document row

  Scenario: AC8 The same file is already on the case
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    Given a second intake item holds the same file with the same hash
    When intake completes
    Then the second item has match_status "MATCHED" and the document ID from AC1
    Then the case holds one copy of that court notice and one "DOCATT" entry for it

  Scenario: AC9 Repeat run
    Given 15 intake items already "MATCHED"
    When JOB-12 runs again
    Then no further document row, decision log entry or DocumentStored event is written for them

  Scenario: AC10 Low classification confidence with one case
    Given a scan with the case ID "RW-2026-000123" classified "APPRAISAL_REPORT" at 0.62 with candidates APPRAISAL_REPORT 0.62 and TITLE_DEED 0.30
    When intake completes
    Then the system stores the document on case "RW-2026-000123" with review_status "PENDING", write_once false and the file in "rwb-docs"
    Then the document carries document_type "APPRAISAL_REPORT" and both candidates for SCR-31

  Scenario: AC11 No agreed type
    Given a scan with the case ID "RW-2026-000123" and review_reason "UNKNOWN_TYPE" from classification
    When intake completes
    Then the intake item has match_status "NO_TYPE" with candidate "RW-2026-000123"

  Scenario: AC12 A reviewer attaches an unmatched item
    Given the item from AC3 and reviewer "TEST-LIT-01" holding RW-LITOFF with both candidate cases in scope
    When "TEST-LIT-01" attaches it to "RW-2026-000654" with type "GUARANTOR_NOTICE"
    Then the system stores the document on "RW-2026-000654" with type "GUARANTOR_NOTICE"
    Then the "DOCATT" entry names "TEST-LIT-01" as approver and match method "PERSON"
    Then the intake item has match_status "MATCHED"

  Scenario: AC13 Reviewer picks a case outside their scope
    Given reviewer "TEST-LIT-02" whose scope does not include case "RW-2026-000654"
    When "TEST-LIT-02" attaches the item from AC3 to "RW-2026-000654"
    Then the system refuses the request with 403 and MSG-P4-003
    Then the item keeps match_status "MULTIPLE"

  Scenario: AC14 Reviewer picks a type not in force
    Given the item from AC2 and a reviewer with scope ALL
    When the reviewer attaches it to "RW-2026-000123" with type "PAYSLIP"
    Then the system refuses the request with 422 and MSG-P5-006 naming "PAYSLIP"

  Scenario: AC15 Two reviewers attach the same item
    Given the item from AC2 at version 3
    When two reviewers attach it at the same time with version 3
    Then one request returns 201 and the other returns 409 with MSG-GEN-004
    Then one document row exists for the item
```

## Attachments

- [image-20261118-050304.png](../../Attachments/TB0001-1194/image-20261118-050304.png) (472560 bytes, Pe Chichareon, 2026-11-18T12:03:14.896+0700)

## Comments (5)

### Comment 1: Piyawan Sanpanya, 2026-11-17T11:38:01.200+0700

Comment ID 1794242

*QA question* 

{adf:display=block}
{"type":"table","attrs":{"isNumberColumnEnabled":false,"layout":"align-start","localId":"dd761574-4589-4db7-b0b9-e4fd16209380"},"content":[{"type":"tableRow","attrs":{"localId":"6708db736220"},"content":[{"type":"tableHeader","attrs":{"localId":"9d1f85e4cae5","colwidth":[237,903],"colspan":2},"content":[{"type":"heading","attrs":{"level":3,"localId":"1e622fb33908"},"content":[{"type":"text","text":"C — Conflicts and contracts requiring alignment"}]}]}]},{"type":"tableRow","attrs":{"localId":"4395d505549a"},"content":[{"type":"tableCell","attrs":{"localId":"70208586248c","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C01A low-confidence legal type may enter write-once storage before type confirmation","marks":[{"type":"strong"}]}],"attrs":{"localId":"ba5ce840e74c"}}]},{"type":"tableCell","attrs":{"localId":"9f2c74da00ba","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" E1-032 requires low-confidence documents to have "},{"type":"text","text":"write_once=false","marks":[{"type":"code"}]},{"type":"text","text":", PENDING status and storage in rwb-docs. E1-024 instead derives write_once/retention from the type table, not the caller, and stores the file after commit. E1-032 Flow 6 updates the document only after calling Store."}],"attrs":{"localId":"d4b8b8a7c7a0"}},{"type":"paragraph","content":[{"type":"text","text":"Impact:","marks":[{"type":"strong"}]},{"type":"text","text":" if the predicted type is legal, changing a flag after Store does not guarantee that the Blob has not already been written to rwb-docs-legal. AC10's APPRAISAL_REPORT example alone does not prove this branch."}],"attrs":{"localId":"1b107902985b"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" How will StoreRequest/Store policy convey “type not yet confirmed” before selecting the container, without allowing callers to override legal controls? Who owns this Store exception path?"}],"attrs":{"localId":"6eee6e230411"}},{"type":"paragraph","content":[{"type":"text","text":"Ask:","marks":[{"type":"strong"}]},{"type":"text","text":" Solution architect + E1-024 / E1-032 / E1-050 owners + Compliance"}],"attrs":{"localId":"66cfdaa01c29"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" an approved interface and integration tests for low-confidence COURT_NOTICE/TITLE_DEED prove that the file remains in the standard container until confirmation."}],"attrs":{"localId":"de0770b9174f"}},{"type":"paragraph","content":[{"type":"text","text":"032 Flow 5–6 / BR4","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"024 Flow 3, 6–7 / BR3","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"024 Spec: Store flow","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"5f5c13e17326"}}]}]},{"type":"tableRow","attrs":{"localId":"bb86bacf3249"},"content":[{"type":"tableCell","attrs":{"localId":"8fb876d8da70","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C02The selector requires predicted_type, but UNKNOWN_TYPE has no type","marks":[{"type":"strong"}]}],"attrs":{"localId":"033c56610b7e"}}]},{"type":"tableCell","attrs":{"localId":"e4db89865607","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Selection contradiction, Before design confirmation · AC11","marks":[{"type":"strong"}]}],"attrs":{"localId":"ed288718f48c"}},{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" the input/selector requires a predicted type and an empty or LOW_CONFIDENCE review_reason. E1-050 defines UNKNOWN_TYPE without a predicted type, while E1-032 AC11 requires NO_TYPE with a candidate case."}],"attrs":{"localId":"cce75d535a9b"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Which separate branch selects UNKNOWN_TYPE/MODEL_UNAVAILABLE, and how does it still find a candidate case without requiring predicted_type?"}],"attrs":{"localId":"283c83192521"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" the contract, specification and query use the same predicate/state flow, and input with predicted_type=null actually reaches NO_TYPE in a test."}],"attrs":{"localId":"cb57d6d41c22"}},{"type":"paragraph","content":[{"type":"text","text":"032 Entry input / Matching rule 5","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"050 Flow 7 / X3–X4","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"15efbd94930c"}}]}]},{"type":"tableRow","attrs":{"localId":"4b03f30643e2"},"content":[{"type":"tableCell","attrs":{"localId":"147500e9a2ed","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C03Resolve API: C/U permissions and 201/200 responses disagree","marks":[{"type":"strong"}]}],"attrs":{"localId":"d41ac7a399a1"}}]},{"type":"tableCell","attrs":{"localId":"4e5db51022a0","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"API contract conflictBefore design confirmation · AC12–15","marks":[{"type":"strong"}]}],"attrs":{"localId":"6320e778aaf1"}},{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" 032 requires Documents C and AC15 expects success status 201. API v4 for "},{"type":"text","text":"POST /intake-items/{id}/resolve","marks":[{"type":"code"}]},{"type":"text","text":" requires Documents U and returns 200 IntakeResolution; E1-054 also uses U."}],"attrs":{"localId":"4af1d88ecf7a"}},{"type":"paragraph","content":[{"type":"text","text":"The story contract still states 201 Document, while the specification already references IntakeResolution. Response shape, status and rights must be aligned."}],"attrs":{"localId":"9c93b002d386"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Does ATTACH require C, U, or action-specific permissions? Is the approved response 200 IntakeResolution or 201? How will ACs, API, generated types and tests be updated together?"}],"attrs":{"localId":"8c238478615b"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" one approved contract includes an action-level rights matrix and contract tests for C-only/U-only roles, not just CRU."}],"attrs":{"localId":"2a1cdeda7629"}},{"type":"paragraph","content":[{"type":"text","text":"API v4 lines 5361–5412","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 §12 / AC15","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"054 API assessment","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"4301bf29a5c8"}}]}]},{"type":"tableRow","attrs":{"localId":"44307f74af8f"},"content":[{"type":"tableCell","attrs":{"localId":"a9a11ceaf36a","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C04No-candidate queue: scope ALL or the review team?","marks":[{"type":"strong"}]}],"attrs":{"localId":"c4c453180d44"}}]},{"type":"tableCell","attrs":{"localId":"82d3933f656c","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Routing / visibility conflict, Before design confirmation","marks":[{"type":"strong"}]}],"attrs":{"localId":"814e7c2cba2c"}},{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" 032 authority restricts no-candidate items to scope ALL, but 054 Flow/BR2 allows the assigned team to see unattached work. The 054 specification itself contains both the team rule and the no-candidate-only-ALL statement."}],"attrs":{"localId":"e8fe3e4448d5"}},{"type":"paragraph","content":[{"type":"text","text":"Impact:","marks":[{"type":"strong"}]},{"type":"text","text":" DOC-SVC/LIT-BKK may not see items they must resolve, or may see more data than agreed. In addition, 032 authority mentions C, while the GET contract requires R."}],"attrs":{"localId":"76917fd4440a"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Who can view and resolve items without candidates? For multiple candidates with only some cases in scope, should the system hide the item, filter candidates, or route it centrally? Does an out-of-scope read return 403 or 404?"}],"attrs":{"localId":"effcfb94183e"}},{"type":"paragraph","content":[{"type":"text","text":"Ask:","marks":[{"type":"strong"}]},{"type":"text","text":" Business lead / Document services + P5 BA + P4 IAM + E1-032 / E1-054 owners"}],"attrs":{"localId":"71c0d7db9b16"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" an approved visibility matrix covers list/detail/content/resolve, with cross-team and mixed-candidate tests."}],"attrs":{"localId":"268bd012687a"}},{"type":"paragraph","content":[{"type":"text","text":"032 §10–12","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"054 Flow 2 / BR2","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"054 Security / scope","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"77307d25737e"}}]}]},{"type":"tableRow","attrs":{"localId":"5a76b0f74690"},"content":[{"type":"tableCell","attrs":{"localId":"cd0e483c9d95","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C05Schema, migrations and dictionary need one baseline","marks":[{"type":"strong"}]}],"attrs":{"localId":"c1772f752495"}}]},{"type":"tableCell","attrs":{"localId":"02da3c37419b","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Data contract mismatch ,Before design confirmation","marks":[{"type":"strong"}]}],"attrs":{"localId":"711da4e8ea81"}},{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" the E1-050 specification adds "},{"type":"text","text":"document.type_candidates","marks":[{"type":"code"}]},{"type":"text","text":", used by 032 AC10, but Physical Schema v6 has no such document column. The schema snapshot already contains match_status/candidate_case_ids, while the 032 migration plans to ADD them again."}],"attrs":{"localId":"a8bc3e1fb5a7"}},{"type":"paragraph","content":[{"type":"text","text":"This does not establish a deployment failure: the snapshot may describe the target state, and migrations may start from another baseline. The actual deployment inputs must be identified first."}],"attrs":{"localId":"1850787a19e3"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" What are the actual DB baseline and migration order? Who owns document.type_candidates, its BR Field ID and migration? How are existing columns prevented from being added twice? How will the migration filename follow AGENTS' four-digit merge sequence?"}],"attrs":{"localId":"53a204e7c8e7"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" dictionary, DDL and specification agree, and clean-install plus upgrade migration tests pass from the stated baseline."}],"attrs":{"localId":"47c868498012"}},{"type":"paragraph","content":[{"type":"text","text":"Schema v6: document / document_intake","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"050 Spec Data and migration","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"AGENTS migration naming","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"a79f8391f745"}}]}]},{"type":"tableRow","attrs":{"localId":"fd4069e1706a"},"content":[{"type":"tableCell","attrs":{"localId":"3f9f99048b13","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C06Extraction readiness and field REVIEW must not be bypassed","marks":[{"type":"strong"}]}],"attrs":{"localId":"b461888ad758"}}]},{"type":"tableCell","attrs":{"localId":"55368fd133d2","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Cross-step handoff gapBefore design confirmation","marks":[{"type":"strong"}]}],"attrs":{"localId":"0dc4d43b43f1"}},{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" 053 requires document.review_status=PENDING when any field is REVIEW. The 032 field matrix defaults to NOT_NEEDED and mainly considers low-confidence type. Its selector does not specify extract_status. The normal 053 path selects classified items without review_reason, so it does not extract LOW_CONFIDENCE items."}],"attrs":{"localId":"9db10cda9b85"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" How is review_status determined from both type and field state? How is a LOW_CONFIDENCE item with no fields stored as a draft? Should extract_status=PENDING/FAILED wait or be held, without incorrectly treating attachment as successful completion?"}],"attrs":{"localId":"f9e363096ab3"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" a readiness/review decision table and integration tests prove that field REVIEW is preserved even when type confidence is high."}],"attrs":{"localId":"bcc95ffbf6e5"}},{"type":"paragraph","content":[{"type":"text","text":"053 Flow 2, 7–9 / X4","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 input / field matrix","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"5b98bf5c847a"}}]}]},{"type":"tableRow","attrs":{"localId":"268e90a42686"},"content":[{"type":"tableCell","attrs":{"localId":"8484d271b102","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C07 AC3's multiple cases per account must be reconciled with the new P3 invariant","marks":[{"type":"strong"}]}],"attrs":{"localId":"7a1088da224c"}}]},{"type":"tableCell","attrs":{"localId":"93b6d0e7e523","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" 032 AC3/FSD places one account on two open cases. The latest E1-018 v2 specifies a partial unique constraint on "},{"type":"text","text":"account_key WHERE linked_to IS NULL","marks":[{"type":"code"}]},{"type":"text","text":" to allow an account on only one open case. The Physical Schema snapshot does not yet show that index."}],"attrs":{"localId":"d545dcca69b0"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Is MULTIPLE for one account a legacy/data-anomaly guard or a permitted business scenario? Which stubs and integration fixtures should be used without violating P3's invariant?"}],"attrs":{"localId":"e010180535e0"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" the invariant and appropriate test level are defined while preserving the rule “do not guess when there is more than one answer.”"}],"attrs":{"localId":"754d61ee1b16"}},{"type":"paragraph","content":[{"type":"text","text":"032 AC3","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"018 v2 Database constraint / BR2","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"FSD A2.12","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"e11a3ea9c431"}}]}]},{"type":"tableRow","attrs":{"localId":"415095bf6a30"},"content":[{"type":"tableCell","attrs":{"localId":"39ea62e0b0b5","colwidth":[237]},"content":[{"type":"paragraph","content":[{"type":"text","text":"C08 D-RCV-31 is decided, but the confirmation flow must reach implementation","marks":[{"type":"strong"}]}],"attrs":{"localId":"9d860fe7df81"}}]},{"type":"tableCell","attrs":{"localId":"dac81f055763","colwidth":[903]},"content":[{"type":"paragraph","content":[{"type":"text","text":"Mechanism already ruled on , Before Done · Across 032/054","marks":[{"type":"strong"}]}],"attrs":{"localId":"2f695b8c3119"}},{"type":"paragraph","content":[{"type":"text","text":"Already clear:","marks":[{"type":"strong"}]},{"type":"text","text":" D-RCV-31 requires re-storing through DocumentStorage into rwb-docs-legal, updating storage_ref, writing DOCATT, retaining the standard object as evidence, and refusing the operation if the immutability policy is absent. Whether to move the file need not be reopened."}],"attrs":{"localId":"de87d9e7f342"}},{"type":"paragraph","content":[{"type":"text","text":"Still to close:","marks":[{"type":"strong"}]},{"type":"text","text":" 032 excludes stored-type confirmation, while 054's stored-document path focuses on field confirmation. DocumentReviewRequest has action/version but no confirmed type, so the complete type-confirmation path must be shown."}],"attrs":{"localId":"68a3b64ba4be"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Who owns the UI/API/service for “confirm stored type,” and which request is used? Where has the ruling been incorporated into 054/024? How will a failed re-store avoid leaving review CONFIRMED when the file is not yet immutable?"}],"attrs":{"localId":"ff62ff99c3e6"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" ownership, contract and a low-confidence legal → confirm → legal container → overwrite refused test exist. Split delivery needs an agreed scope/flag arrangement."}],"attrs":{"localId":"3d9e62ca21dd"}}]}]},{"type":"tableRow","attrs":{"localId":"c8b5e8b35603"},"content":[{"type":"tableCell","attrs":{"localId":"e7c89aedbc69","colwidth":[237,903],"colspan":2,"background":"#e6fcff"},"content":[{"type":"heading","attrs":{"level":3,"localId":"e73dc697085e"},"content":[{"type":"text","text":"Q — Questions requiring defined behavior and additional tests"}]}]}]},{"type":"tableRow","attrs":{"localId":"899a2ee197f7"},"content":[{"type":"tableCell","attrs":{"localId":"fd085f04d318","colwidth":[237],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Q01 Identifier format and normalization are not yet fully approved","marks":[{"type":"strong"}]}],"attrs":{"localId":"86544af62419"}}]},{"type":"tableCell","attrs":{"localId":"e26d965a742e","colwidth":[903],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Before design confirmation · AC4","marks":[{"type":"strong"}]}],"attrs":{"localId":"7bbbca8084ca"}},{"type":"paragraph","content":[{"type":"text","text":"Evidence:","marks":[{"type":"strong"}]},{"type":"text","text":" ACCOUNT_NO_PATTERN requires 10 digits, but the test uses TEST-ACC-0002. DL21 in the reviewed decision log concerns which systems store the case identifier, not approval of the regex or account_code length."}],"attrs":{"localId":"11b7ae370249"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" What patterns are approved for case/account identifiers by product? How are Thai digits, spaces, hyphens, leading zeros and OCR O/0 handled without guessing numbers? Does AC4 use real OCR text or seeded extracted fields?"}],"attrs":{"localId":"12e1a4965fd2"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" versioned parameters, normalization examples and valid fixtures exist, without changing production patterns merely to accommodate tests."}],"attrs":{"localId":"dc2fc727b0b7"}},{"type":"paragraph","content":[{"type":"text","text":"DL21","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 Preconditions / AC4","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"ACE data mapping","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"9a1900e60780"}}]}]},{"type":"tableRow","attrs":{"localId":"312159244251"},"content":[{"type":"tableCell","attrs":{"localId":"4447ba0f5e39","colwidth":[237],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Q02 A decision table is needed for multiple identifiers and their reliability","marks":[{"type":"strong"}]}],"attrs":{"localId":"fb0a8c90f893"}}]},{"type":"tableCell","attrs":{"localId":"7de618838d20","colwidth":[903],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Before design confirmation · BR1–3","marks":[{"type":"strong"}]}],"attrs":{"localId":"47674d01deb1"}},{"type":"paragraph","content":[{"type":"text","text":"CLAR-005 already says that identifiers resolving to different cases produce CONFLICT, and that one resolving side may be used if the other does not resolve. It does not cover multiple case numbers/accounts or partially overlapping candidate sets."}],"attrs":{"localId":"8ff95f20106c"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" If OCR finds cases A and B but the account points to A, is the outcome CONFLICT, MULTIPLE or something else? How are several accounts pointing to one case deduplicated? Which value is trusted if extracted case_no differs from raw OCR or has state REVIEW? If both methods point to the same case, which match method is logged?"}],"attrs":{"localId":"4a619300c458"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" an approved decision table includes provenance/confidence policy and positive/negative tests, including wrong-case prevention."}],"attrs":{"localId":"d31dd58504b2"}},{"type":"paragraph","content":[{"type":"text","text":"Matching rules / CLAR-005 / CLAR-007","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"Field states","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"7c7c214ebbee"}}]}]},{"type":"tableRow","attrs":{"localId":"86f4fd2c7a98"},"content":[{"type":"tableCell","attrs":{"localId":"d02b12d87d6c","colwidth":[237],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Q04 Duplicate keys and concurrency must cover more than repeat runs","marks":[{"type":"strong"}]}],"attrs":{"localId":"5e193ef21f32"}}]},{"type":"tableCell","attrs":{"localId":"6b8d4d283a2a","colwidth":[903],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Before Done , AC8 / AC9 / AC15","marks":[{"type":"strong"}]}],"attrs":{"localId":"bfb94d7324dc"}},{"type":"paragraph","content":[{"type":"text","text":"024 deduplicates active documents by case + type + hash, while some 032 wording mentions only a hash on the case. AC8 also requires no duplicate DOCATT."}],"attrs":{"localId":"0ed43eabe1d2"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Is the same file hash with a different type a duplicate? When linking an existing document, must its review status/type/candidates remain unchanged? How is a single document/audit/event ensured when automatic workers process different intake items, automatic and manual paths race, or two reviewers act together?"}],"attrs":{"localId":"7e08b806a10e"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" a unified deduplication key, transaction/unique constraint and race tests cover different intake items holding the same file. A lock on one intake row alone is not sufficient evidence."}],"attrs":{"localId":"0b220d8279fb"}},{"type":"paragraph","content":[{"type":"text","text":"024 Duplicate and idempotency","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 Attach, duplicate and concurrency","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"557308f21e2e"}}]}]},{"type":"tableRow","attrs":{"localId":"daca6e9b24b3"},"content":[{"type":"tableCell","attrs":{"localId":"bee16d8a3130","colwidth":[237],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Q05 Idempotency-Key and optimistic version checks must not conflict","marks":[{"type":"strong"}]}],"attrs":{"localId":"7dbd0876f1ea"}}]},{"type":"tableCell","attrs":{"localId":"1898d42bfe6e","colwidth":[903],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Before Done · Resilience","marks":[{"type":"strong"}]}],"attrs":{"localId":"baebc7024431"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Do intake, document, DOCATT and outbox really commit as one unit? How is recovery handled if the document commits but the intake update fails? If Blob copy fails, does MATCHED mean metadata attached or file ready to read? May the event be emitted before STORED? Where does CopyPendingStep run within JOB-12?"}],"attrs":{"localId":"f208b980a616"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" transaction/recovery sequences and fault-injection tests cover failures before/after commit, failed copies and retries without duplicate audits/events."}],"attrs":{"localId":"c826dfd4948d"}},{"type":"paragraph","content":[{"type":"text","text":"024 COPY_PENDING / X8","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 Transaction and events","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"df91fbf79d2a"}}]}]},{"type":"tableRow","attrs":{"localId":"a89d1ffd0c60"},"content":[{"type":"tableCell","attrs":{"localId":"0679c79fdc45","colwidth":[237],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Q06 Attachment transactions, COPY_PENDING and Blob failures","marks":[{"type":"strong"}]}],"attrs":{"localId":"9fce041cfe66"}}]},{"type":"tableCell","attrs":{"localId":"7ece2a9fafda","colwidth":[903],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Before Done · Resilience","marks":[{"type":"strong"}]}],"attrs":{"localId":"904f7ba2be25"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Do intake, document, DOCATT and outbox really commit as one unit? How is recovery handled if the document commits but the intake update fails? If Blob copy fails, does MATCHED mean metadata attached or file ready to read? May the event be emitted before STORED? Where does CopyPendingStep run within JOB-12?"}],"attrs":{"localId":"cf1e8b74ee6c"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" transaction/recovery sequences and fault-injection tests cover failures before/after commit, failed copies and retries without duplicate audits/events."}],"attrs":{"localId":"7c16db798fca"}},{"type":"paragraph","content":[{"type":"text","text":"024 COPY_PENDING / X8","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 Transaction and events","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"879e3f59bae3"}}]}]},{"type":"tableRow","attrs":{"localId":"2090cfbc2f82"},"content":[{"type":"tableCell","attrs":{"localId":"c9a428c2a02b","colwidth":[237],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Q07 StoreRequest and DOCATT must carry all required metadata","marks":[{"type":"strong"}]}],"attrs":{"localId":"67da815166f9"}}]},{"type":"tableCell","attrs":{"localId":"7821c962147a","colwidth":[903],"background":"#ffffff"},"content":[{"type":"paragraph","content":[{"type":"text","text":"Before interface confirmation · AC1 / AC4 / AC12 / TC17","marks":[{"type":"strong"}]}],"attrs":{"localId":"6cf258c7a29d"}},{"type":"paragraph","content":[{"type":"text","text":"032 must log classifier version, confidence, match method and approver. The displayed published StoreRequest in 024 mainly lists case/type/source/blob/hash/fields. Its actual shape must be confirmed rather than assuming it supports this metadata."}],"attrs":{"localId":"29b8bfad5b48"}},{"type":"paragraph","content":[{"type":"text","text":"Questions:","marks":[{"type":"strong"}]},{"type":"text","text":" Which StoreRequest/DecisionLogRecord fields carry this metadata? If a person changes the type, how are predicted/confirmed values and the decision-maker recorded? How is missing metadata rejected? Does audit failure leave no changes?"}],"attrs":{"localId":"367904eca160"}},{"type":"paragraph","content":[{"type":"text","text":"Close when:","marks":[{"type":"strong"}]},{"type":"text","text":" a versioned interface and assertions inspect the actual DOCATT, not merely document creation; TC-E1-032-17 covers both automatic and manual paths."}],"attrs":{"localId":"027a3e356ed8"}},{"type":"paragraph","content":[{"type":"text","text":"024 §12","marks":[{"type":"link","attrs":{"href":""}}]},{"type":"text","text":" · "},{"type":"text","text":"032 AC1 / AC4 / AC12 / BR5","marks":[{"type":"link","attrs":{"href":""}}]}],"attrs":{"localId":"446933f6fe95"}}]}]}]}
{adf}

### Comment 2: THAMMASAK JUKCHAN, 2026-11-17T12:17:42.265+0700

Comment ID 1794351

*Dev questions before design: RWB-E1-032*
Ref: User Stories Epic 1 v7 §RWB-E1-032. +1 to QA C01–C08 and Q01–Q07 (note: *Q03 is missing and Q05 repeats Q06*). Additional points that block our build:

{quote}🔴 *Top blockers*

# *No story builds CaseDirectory* (PO-102)
# *COURT_NOTICE / APPRAISAL_REPORT / TITLE_DEED have no case_no or account_no*, so they cannot auto-match
# *matchStep does not check extract_status*: an item can attach before extraction finishes
# *AC11 fails as written*: NO_TYPE is never matched{quote}

h3. 🔴 Blocking

# *CaseDirectory owner.* We call {{findByCaseNo}} and {{findOpenCasesByAccountNo}}, but *no story builds this P3 interface*. Which story builds it, and when? (PO-102 proposes RWB-E1-018, #40.)
_Default: we build CaseMatcher against a CaseDirectory stub._
# *Matching coverage.* In the RWB-E1-025 field list, *COURT_NOTICE, APPRAISAL_REPORT and TITLE_DEED have no case_no or account_no*. They match only on an RW number in the OCR text, yet *AC1 uses a COURT_NOTICE*. Should we match on black_case_no, or is NO_MATCH expected?
# *matchStep vs extraction.* The step 2 selector *does not check* {{extract_status}}, so an item can be attached *before RWB-E1-053 finishes, or after it fails*. Can we add {{extract_status = 'DONE'}} to the selector? (+1 QA C06)
# *AC11 vs flow.* Step 2 sets NO_TYPE *without matching*, but AC11 expects a candidate case. Run CaseMatcher for NO_TYPE items, or remove the candidate from AC11? (+1 QA C02)

h3. 🟠 Need a decision

# *Threshold source:* the global {{CLASSIFY_THRESHOLD}}, or *per-type* {{document_type.classify_threshold}} (schema, used by RWB-E1-054)?
# *RWB-E1-050 flag off:* LOW_CONFIDENCE items have no {{predicted_type}}, so *our selector never takes them and they are stranded*. Can E1-050 set MODEL_UNAVAILABLE instead?
# *Endpoints exist in 3 versions:* flow step 8, §12, and RWB-E1-054 §13. Do we build *exactly the API spec paths, rights and status codes*? (PO-33, PO-38; +1 QA C03)
# *Decision log order:* BR5 says DOCATT before the store, but step 5 writes it *inside* {{DocumentStore.store}}. Which order, in which transaction? (PO-32) Incident target for X13? (PO-110)

h3. 🟡 Design gaps

# *SCR-31 is built in RWB-E1-054 (#76), after this story (#68).* OK to build UnmatchedIntakeTab stand-alone and test AC3/AC10 through the API?
# After an auto-attach, should matchStep *fill in* {{document_text.document_id}} so that RWB-E1-033 search finds the OCR text of scanned documents?
# Depends on is *missing RWB-E1-049*. §11 lists DF-DOC-007 twice. *Test accounts TEST-ACC-000n do not fit* {{[0-9]{10}}}; can we use numeric SYN- accounts? (PO-28, DL21)

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T12:48:03.199+0700

Comment ID 1794389

These points add to QA C01–C08 / Q01–Q07 and the dev questions already on this card. Those cover a low-confidence type, patterns and normalisation, the resolve API, queue visibility and dependencies. The points below are about a wrong case, not a wrong type.

# *A confident attach to the wrong case cannot be undone in Epic 1.* Even with a confirmed type and one candidate, the account number in the text may not belong to the case. For example, a demand letter can cite a guarantor's account or another loan of the same customer. A legal-type document then goes to the write-once container of the wrong case. Moving a document to another case is in Epic 2.
#* Proposal: a correction path in Epic 1, or a person confirms the case for legal types before the write-once store.
# *Mobile numbers match as account numbers.* ACCOUNT_NO_PATTERN {{[0-9]{10}}} also matches a Thai mobile number (10 digits starting with 0), which appears on most letters. If a phone number happens to equal an account key, the document attaches to a stranger's case.
#* Proposal: an AC with a letter that holds both a phone number and an account number, where only the account number is used.
# *The Unmatched queue has no SLA.* Beyond who can see it (C04), nothing says how fast an item with no case must be resolved, or what happens to items left open (alert, escalation). Legal notices can carry court dates.
# *No access log.* {{GET /intake-items/{id}}} must write the PII access log, which has no table in Physical Schema v6 (feedback #49).

Who answers: Document SME, Legal, Business lead, Security architect.

### Comment 4: Pe Chichareon, 2026-11-18T11:33:56.681+0700, edited 2026-11-18T12:03:14.893+0700

Comment ID 1796272

Attach image that walkhtrough in grooming session

!image-20261118-050304.png|width=1181,alt="image-20261118-050304.png"!

### Comment 5: NAMTIP WONGSOMBOON, 2026-11-18T11:54:34.982+0700

Comment ID 1796339

@CHANISSARA MAHAKITTIKUN 
Ref: Grooming Session – Room 2 with Henka , {{2026-11-18}}
Topic: 12. Contract (API)

# *GET /review-items* (new, see additions)
# *GET /intake-items/{intakeItemId}* 
# *GET /intake-items/{intakeItemId}/content* (new, see additions)
# *POST /intake-items/{intakeItemId}/resolve* (new, see additions)

Please provide the detailed API specifications for APIs #1–4, including:
#* API endpoint, HTTP method, and authentication requirements
#* Request/response JSON schemas with sample payloads
#* Mandatory/optional fields and validation rules
#* Expected success/error responses and status codes
#* Integration flow and expected behavior
# *API #4:* The specification is required before Development can proceed, as this API is used directly in the Story.
*APIs #1–3:* The Backend team will create Mock APIs. Please provide the API contracts and expected results to support integration testing. Without these specifications, testing will be limited to Unit Testing.
Please update the Story with the required specifications to ensure Development readiness.


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-05 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
