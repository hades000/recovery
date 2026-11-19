# Test scenarios — RWB-TE-002

All tests are system tests in the ACE repository. Each uses a test branch protected by the same branch
rules; the PR is closed without merge and the history is the evidence. No production data, no personal
data and no Workbench endpoint.

## TC-TE-002-01 — Recovery change requires a code owner

**Covers:** AC1, BR1, BR6.

**Given** the CODEOWNERS file maps the recovery folders to the recovery team and the branch rule
requires code-owner review
**When** a test PR changes a recovery Java fixture and a squad member outside the team approves
**Then** a recovery team reviewer is requested and the merge stays blocked
**Evidence:** PR link, reviewer list, merge-state screenshot/export.

## TC-TE-002-02 — Common change requires the ACE team

**Covers:** AC2, BR3.

**Given** the common module is owned by the ACE team
**When** a test PR changes a common module fixture
**Then** `@scb-ace/ace-team` is requested as reviewer
**Evidence:** PR reviewer list.

## TC-TE-002-03 — Cross-module change requires both teams

**Covers:** AC3, BR6.

**Given** a test PR changes one recovery file and one common file
**When** a recovery team member approves
**Then** the merge stays blocked until an ACE team member also approves
**Evidence:** PR approval timeline and merge state.

## TC-TE-002-04 — Front end, migration and module map

**Covers:** AC4, BR2.

**Given** a test PR changes a front-end recovery fixture, a migration fixture and the module map
**When** the PR is opened
**Then** the recovery team is requested for all three paths
**Evidence:** PR reviewer list; module map restored after the test.

## TC-TE-002-05 — Author self-approval does not count

**Covers:** AC5, BR6.

**Given** a recovery team member opens a PR on a recovery folder
**When** the same member approves it
**Then** the merge stays blocked until a second member of the team approves
**Evidence:** PR approval state.

## TC-TE-002-06 — New commit dismisses approval

**Covers:** AC6, BR6.

**Given** an approved recovery PR
**When** a new fixture commit is pushed
**Then** the approval is dismissed and code-owner review is required again
**Evidence:** PR timeline.

## TC-TE-002-07 — Missing owner fails the validation

**Covers:** AC7, BR7.

**Given** the CODEOWNERS file names `@scb-ace/recovery-leads-typo` for a recovery path
**When** the validation step runs on a test PR
**Then** it fails with `owner @scb-ace/recovery-leads-typo not found`
**Evidence:** pipeline log; the valid file passes after restore.

## TC-TE-002-08 — Outside approval is refused

**Covers:** Access, AC1.

**Given** a squad member outside the owning team
**When** they approve a recovery PR
**Then** the merge is refused and the approval does not satisfy the code-owner rule
**Evidence:** PR approval timeline. No Workbench endpoint, so `MSG-P4-002` is not shown.

## Coverage

| AC | Tests |
|---|---|
| AC1 | TC-TE-002-01, -08 |
| AC2 | TC-TE-002-02 |
| AC3 | TC-TE-002-03 |
| AC4 | TC-TE-002-04 |
| AC5 | TC-TE-002-05 |
| AC6 | TC-TE-002-06 |
| AC7 | TC-TE-002-07 |
