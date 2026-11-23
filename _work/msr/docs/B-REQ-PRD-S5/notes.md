# B-REQ-PRD-S5 scratch notes

Working notes for the PRD S5 rwb-asset v1. Not a deliverable; kept under the WP scratch path.

## 1. Source to PRD map

| FSD feature | A2 section | Legacy story | Slice | CAP | Wave |
|---|---|---|---|---|---|
| FEAT-AST-01 Take a repossessed vehicle onto the books | A2.1 | RWB-E3-019 | RWB-S5-E3019-CON, -APP | CAP-S5-001 | 2 |
| FEAT-AST-02 Take a property onto the books after a deed in lieu | A2.2 | RWB-E3-020 | RWB-S5-E3020-CON, -APP | CAP-S5-001 | 2 |
| FEAT-AST-03 Take a property onto the books after an LED auction | A2.3 | RWB-E3-021 | RWB-S5-E3021-CON, -APP | CAP-S5-001 | 2 |
| FEAT-AST-04 Serve the statutory notice and prove delivery | A2.4 | RWB-E3-022 | RWB-S5-E3022-CON, -APP | CAP-S5-002 | 2 |
| FEAT-AST-05 Track holding age against the provision steps | A2.5 | RWB-E3-023 | RWB-S5-E3023-CON, -APP | CAP-S5-003, CAP-S5-019 | 2 |
| FEAT-AST-06 Record and track the asset stock balance | A2.6 | RWB-E3-024 | RWB-S5-E3024-CON, -APP | CAP-S5-004 | 2 |
| FEAT-AST-07 Maintain a held property | A2.7 | RWB-E3-025 | RWB-S5-E3025-CON, -APP | CAP-S5-005 | 2 |
| FEAT-AST-09 Re-appraise a held asset on cycle | A2.9 | RWB-E3-026 | RWB-S5-E3026-CON, -APP, RWB-ITG-E3026-ITG | CAP-S5-006 | 2 |
| FEAT-AST-10 Recommend the disposal route | A2.10 | RWB-E3-027 | RWB-S5-E3027-CON, -APP | CAP-S5-007 | 2 |
| FEAT-AST-11 Set the start and floor price | A2.11 | RWB-E3-028 | RWB-S5-E3028-CON, -APP | CAP-S5-008 | 2 |
| FEAT-AST-12 Publish the listing | A2.12 | RWB-E3-029 | RWB-S5-E3029-CON, -APP | CAP-S5-009 | 2 |
| FEAT-AST-08 Evict occupants from a held property | A2.8 | RWB-E4-021 | RWB-S5-E4021-CON, -APP | CAP-S5-010 | 3 |
| FEAT-AST-13 Run the descending price schedule | A2.13 | RWB-E4-022 | RWB-S5-E4022-CON, -APP | CAP-S5-011 | 3 |
| FEAT-AST-14 Allocate the asset to an auction vendor by distance | A2.14 | RWB-E4-023 | RWB-S5-E4023-CON, -APP | CAP-S5-012 | 3 |
| FEAT-AST-15 Run auction rounds and report bids | A2.15 | RWB-E4-024 | RWB-S5-E4024-CON, -APP | CAP-S5-011 | 3 |
| FEAT-AST-16 Accept a bid below the floor with a second signature | A2.16 | RWB-E4-025 | RWB-S5-E4025-CON, -APP | CAP-S5-013 | 3 |
| FEAT-AST-17 Re-list on no bid | A2.17 | RWB-E4-026 | RWB-S5-E4026-CON, -APP | CAP-S5-014 | 3 |
| FEAT-AST-18 Enforce the five-day payment term | A2.18 | RWB-E4-027 | RWB-S5-E4027-CON, -APP | CAP-S5-015 | 3 |
| FEAT-AST-19 Transfer vehicle registration | A2.19 | RWB-E4-028 | RWB-S5-E4028-CON, -APP | CAP-S5-016 | 3 |
| FEAT-AST-20 Record a property transfer at the Land Office | A2.20 | RWB-E4-029 | RWB-S5-E4029-CON, -APP | CAP-S5-016 | 3 |
| FEAT-AST-21 Apply proceeds and raise the shortfall | A2.21 | RWB-E4-030 | RWB-S5-E4030-CON, -APP | CAP-S5-017 | 3 |
| FEAT-AST-22 Transfer a pool to RAMC or the joint venture | A2.22 | RWB-E4-031 | RWB-S5-E4031-CON, -APP | CAP-S5-018 | 3 |
| FEAT-AST-23 Arrange a customer buy-back | A2.23 | RWB-E4-032 | RWB-S5-E4032-CON, -APP | CAP-S5-018 | 3 |
| FEAT-AST-24 Rent a held asset to a third party | A2.24 | RWB-E4-033 | RWB-S5-E4033-CON, -APP | CAP-S5-018 | 3 |
| FEAT-AST-25 Sell through a broker | A2.25 | RWB-E4-034 | RWB-S5-E4034-CON, -APP | CAP-S5-018 | 3 |

The Epic 1 slice RWB-S5-E1011-APP (legacy RWB-E1-011, Reconciliation and data quality report) carries no FSD S5 feature and is described in PRD section 10.2 only.

## 2. Coverage checks run by hand

1. Every one of the 25 FSD features appears in exactly one CAP row of PRD section 5 (A2.5 is also claimed by CAP-S5-019 for freshness, which is deliberate and stated).
2. Every FR carries a CAP, a BR and a priority. FR-S5-027 has no FSD REQ ID because BR-026 carries no REQ-S5 row; its source is FEAT-AST-08 and RWB-E4-021.
3. Every NFR carries a business BR and a source NFR ID, so a numeric target is never invented: the open targets are carried as CG-B-REQ-PRD-S5-20 and CG-B-REQ-PRD-S5-15.
4. Every FR appears in at least one AC of section 11.1; the reverse holds too, so no AC tests nothing.
5. All ten BRD requirements that name this service (BR-010 to BR-014 and BR-026 to BR-030) appear in section 11.2 with at least one FR.

## 3. Facts taken from the design and constraints, not invented

1. AssetDisposalWorkflow on task queue rwb-asset, 7 steps: holding age; re-appraise at 12 months (JOB-19); pricing agent recommends; floor approved and listed; rounds step to floor; buyer pays in 5 days; title transfer and proceeds.
2. The two clocks: payment 5 calendar days, title transfer 10 working days.
3. The approval ladder amounts named in the design: L5 at THB 20m and 70 percent of fair market value, PARC at THB 200m and 70 percent, MC at THB 500m and 60 percent; the comparison signs are unreadable in the extract, which is CG-B-REQ-PRD-S5-14.
4. The three Drools outcomes named in the design: THB 50m and above to sealed bids at committee (R-DIS-22), a bid below the floor to a second signature (R-DIS-41), the re-list limit reached to debt sale (R-DIS-46).
5. Call types for S5 from the connection matrix: Temporal to P7 (approval), events from S4, Temporal and events to P8 and S9, Temporal child workflow and REST from P3.

## 4. Checks that shaped the wording

1. No person is named and no email address appears; every owner is a role, a service code or a team type.
2. The issue tracker is not referenced anywhere.
3. Every CG and ASM citation used in the PRD and here exists as a row in the two registers of this WP.
4. Release dates are copied unchanged and marked tentative; no date is raised as a gap.
