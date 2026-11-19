# Traceability Matrix

Required chain (see `.github/rules/traceability-standards.md`):

```text
CTX -> BRD -> FR/NFR -> US -> SPEC -> TASK -> CODE -> APT -> FT -> TEST -> REVIEW -> DOC
```

This matrix is seeded from the context package and the Epic 1/Epic 2 build sequence. The
`FR/NFR` and `US` columns are populated; `SPEC`, `TASK`, `CODE`, `APT`, `FT`, `TEST`, `REVIEW`
and `DOC` are filled by the later stages. The source-ID crosswalk at the end preserves the
project's `REQ-*`, `RWB-E*`, `BR-*`, `MSG-*`, `DF-*` and `TC-*` identifiers.

## 1. Context to requirement

| CTX ID | BRD ID | FR/NFR ID | US ID | SPEC ID | TASK ID | Code Ref | APT ID | FT ID | TEST ID | REVIEW ID | DOC ID | GitHub Issue | PR | Commit | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CTX-BUSINESS-001 | BRD-RWB-001 | FR-RWB-001 | RWB-E1-001..068 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-002 | BRD-RWB-001 | FR-RWB-002 | RWB-E1-001..017 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-003 | BRD-RWB-003 | FR-RWB-004..010 | RWB-E1-018..031 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-004 | BRD-RWB-001..020 | FR-RWB-001..020 | E1-E8 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-005 | BRD-RWB-001..020 | FR-RWB-001..020 | E1-E8 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-006 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-007 | BRD-RWB-009 | FR-RWB-018 | RWB-E1-013 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-008 | BRD-RWB-003 | FR-RWB-004..010 | RWB-E1-018..031 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-009 | BRD-RWB-001..020 | FR-RWB-001..020 | E1-E8 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-010 | BRD-RWB-007 | FR-RWB-017 | RWB-E1-008, 027 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-011 | BRD-RWB-007 | FR-RWB-017 | RWB-E1-008, 027 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-012 | BRD-RWB-018 | FR-RWB-006 | RWB-E1-021, 062 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-013 | BRD-RWB-003 | FR-RWB-004..010 | RWB-E1-018..031 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-014 | BRD-RWB-003 | FR-RWB-004 | RWB-E1-018 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-015 | BRD-RWB-003 | FR-RWB-004 | RWB-E1-018 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-016 | BRD-RWB-003 | FR-RWB-004 | RWB-E1-018 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-017 | BRD-RWB-003 | FR-RWB-005 | RWB-E1-020 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-018 | BRD-RWB-003 | FR-RWB-006 | RWB-E1-021 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-019 | BRD-RWB-003 | FR-RWB-007 | RWB-E1-028 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-020 | BRD-RWB-003 | FR-RWB-008 | RWB-E1-029 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-021 | BRD-RWB-003 | FR-RWB-008 | RWB-E1-029 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-022 | BRD-RWB-003 | FR-RWB-008 | RWB-E1-029 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-023 | BRD-RWB-007 | FR-RWB-017 | RWB-E1-027 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-024 | BRD-RWB-003 | FR-RWB-019 | RWB-E1-062 | | | | | | | | | | | | Context mapped |
| CTX-BUSINESS-025 | BRD-RWB-003 | FR-RWB-010 | RWB-E1-035 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-001 | BRD-RWB-004 | FR-RWB-011..013 | RWB-E1-022, 037-039 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-002 | BRD-RWB-004 | FR-RWB-011..013 | RWB-E1-022, 037-039 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-003 | BRD-RWB-004 | FR-RWB-011..013 | RWB-E1-022 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-004 | BRD-RWB-004 | FR-RWB-011 | RWB-E1-022 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-005 | BRD-RWB-003..010 | FR-RWB-004..019 | RWB-E1-018..063 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-006 | BRD-RWB-004 | FR-RWB-011..013 | RWB-E1-022, 037-039 | | | | | | | | | | | | Context mapped |
| CTX-STAKEHOLDER-007 | BRD-RWB-004 | NFR-RWB-002 | RWB-E1-022 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-001 | BRD-RWB-001 | FR-RWB-001, FR-RWB-002 | RWB-E1-001..017, 064-068 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-002 | BRD-RWB-002 | FR-RWB-003 | RWB-E1-007, 047, 051, 056 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-003 | BRD-RWB-003 | FR-RWB-004..010 | RWB-E1-018..031, 035, 042-045, 048 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-004 | BRD-RWB-004 | FR-RWB-011..013 | RWB-E1-022, 037-039 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-005 | BRD-RWB-005 | FR-RWB-014, FR-RWB-015 | RWB-E1-024..026, 032-033, 040-041, 049-050, 053-054, 057 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-006 | BRD-RWB-006 | FR-RWB-016 | RWB-E1-034, 046, 052, 055 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-007 | BRD-RWB-007 | FR-RWB-017 | RWB-E1-008, 027 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-008 | BRD-RWB-008 | FR-RWB-002, FR-RWB-003 | RWB-E1-007, 056 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-009 | BRD-RWB-009 | FR-RWB-018 | RWB-E1-013 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-010 | BRD-RWB-010 | FR-RWB-019 | RWB-E1-058..063 | | | | | | | | | | | | Context mapped |
| CTX-FEATURE-011 | BRD-RWB-011 | FR-RWB-020 | E4 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-012 | BRD-RWB-012 | FR-RWB-020 | E2/E3 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-013 | BRD-RWB-013 | FR-RWB-020 | E4 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-014 | BRD-RWB-014 | FR-RWB-020 | E2/E5 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-015 | BRD-RWB-015 | FR-RWB-020 | E3/E4 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-016 | BRD-RWB-016 | FR-RWB-020 | E5/E6 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-017 | BRD-RWB-017 | FR-RWB-020 | E6 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-018 | BRD-RWB-018 | FR-RWB-020 | E2/E7 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-019 | BRD-RWB-019 | FR-RWB-020 | E6/E7 | | | | | | | | | | | | Programme-level |
| CTX-FEATURE-020 | BRD-RWB-020 | FR-RWB-020 | RWB-E1-042..048 | | | | | | | | | | | | Context mapped |
| CTX-RULE-001 | BRD-RWB-003 | FR-RWB-004 | RWB-E1-018 | | | | | | | | | | | | Context mapped |
| CTX-RULE-002 | BRD-RWB-003 | FR-RWB-005 | RWB-E1-020 | | | | | | | | | | | | Context mapped |
| CTX-RULE-003 | BRD-RWB-003 | FR-RWB-005 | RWB-E1-020 | | | | | | | | | | | | Context mapped |
| CTX-RULE-004 | BRD-RWB-003 | FR-RWB-006 | RWB-E1-021 | | | | | | | | | | | | Context mapped |
| CTX-RULE-005 | BRD-RWB-003 | FR-RWB-007 | RWB-E1-028 | | | | | | | | | | | | Context mapped |
| CTX-RULE-006 | BRD-RWB-011 | FR-RWB-020 | E4 | | | | | | | | | | | | Programme-level |
| CTX-RULE-007 | BRD-RWB-012 | FR-RWB-020 | E2/E3 | | | | | | | | | | | | Programme-level |
| CTX-RULE-008 | BRD-RWB-013 | FR-RWB-020 | E4 | | | | | | | | | | | | Programme-level |
| CTX-RULE-009 | BRD-RWB-014 | FR-RWB-020 | E2/E5 | | | | | | | | | | | | Programme-level |
| CTX-RULE-010 | BRD-RWB-015 | FR-RWB-020 | E3/E4 | | | | | | | | | | | | Programme-level |
| CTX-RULE-011 | BRD-RWB-016 | FR-RWB-020 | E5/E6 | | | | | | | | | | | | Programme-level |
| CTX-RULE-012 | BRD-RWB-017 | FR-RWB-020 | E6 | | | | | | | | | | | | Programme-level |
| CTX-RULE-013 | BRD-RWB-018 | FR-RWB-020 | E2/E7 | | | | | | | | | | | | Programme-level |
| CTX-RULE-014 | BRD-RWB-019 | FR-RWB-020 | E6/E7 | | | | | | | | | | | | Programme-level |
| CTX-RULE-015 | BRD-RWB-004 | FR-RWB-012 | RWB-E1-037..039 | | | | | | | | | | | | Context mapped |
| CTX-RULE-016 | BRD-RWB-001 | FR-RWB-002 | RWB-E1-006, 011 | | | | | | | | | | | | Context mapped |
| CTX-DATA-001 | BRD-RWB-001 | FR-RWB-001 | RWB-E1-001, 064 | | | | | | | | | | | | Context mapped |
| CTX-DATA-002 | BRD-RWB-001 | FR-RWB-001 | RWB-E1-001, 064 | | | | | | | | | | | | Context mapped |
| CTX-DATA-003 | BRD-RWB-001 | FR-RWB-001 | RWB-E1-001, 064 | | | | | | | | | | | | Context mapped |
| CTX-DATA-004 | BRD-RWB-001 | FR-RWB-002 | RWB-E1-015 | | | | | | | | | | | | Context mapped |
| CTX-DATA-005 | BRD-RWB-001 | FR-RWB-002 | RWB-E1-006, 011 | | | | | | | | | | | | Context mapped |
| CTX-DATA-006 | BRD-RWB-001 | FR-RWB-002 | RWB-E1-017 | | | | | | | | | | | | Context mapped |
| CTX-DATA-007 | BRD-RWB-004 | FR-RWB-013 | RWB-E1-037 | | | | | | | | | | | | Context mapped |
| CTX-NFR-001 | BRD-RWB-001 | NFR-RWB-001 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-002 | BRD-RWB-001 | NFR-RWB-002 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-003 | BRD-RWB-009 | NFR-RWB-003 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-004 | BRD-RWB-001 | NFR-RWB-004 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-005 | BRD-RWB-001 | NFR-RWB-005 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-006 | BRD-RWB-001 | NFR-RWB-006 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-007 | BRD-RWB-001 | NFR-RWB-007 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-008 | BRD-RWB-001 | NFR-RWB-008 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-009 | BRD-RWB-001 | NFR-RWB-009 | — | | | | | | | | | | | | Context mapped |
| CTX-NFR-010 | BRD-RWB-001 | NFR-RWB-010 | — | | | | | | | | | | | | Context mapped |
| CTX-COMPLIANCE-001 | BRD-RWB-004 | FR-RWB-013 | RWB-E1-037 | | | | | | | | | | | | Context mapped |
| CTX-COMPLIANCE-002 | BRD-RWB-004 | FR-RWB-013 | RWB-E1-037..039 | | | | | | | | | | | | Context mapped |
| CTX-COMPLIANCE-003 | BRD-RWB-004 | FR-RWB-013 | RWB-E1-037..039 | | | | | | | | | | | | Context mapped |
| CTX-COMPLIANCE-004 | BRD-RWB-009 | FR-RWB-018 | RWB-E1-013 | | | | | | | | | | | | Context mapped |
| CTX-COMPLIANCE-005 | BRD-RWB-005 | FR-RWB-014 | RWB-E1-024, 041 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-001 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-002 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-003 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-004 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-005 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-006 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-DELIVERY-007 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-AI-001 | BRD-RWB-010 | FR-RWB-019 | RWB-E1-058..063 | | | | | | | | | | | | Context mapped |
| CTX-AI-002 | BRD-RWB-010 | FR-RWB-019 | RWB-E1-058..063 | | | | | | | | | | | | Context mapped |
| CTX-AI-003 | BRD-RWB-007 | FR-RWB-017 | RWB-E1-008, 027 | | | | | | | | | | | | Context mapped |
| CTX-AI-004 | BRD-RWB-010 | FR-RWB-019 | RWB-E1-058 | | | | | | | | | | | | Context mapped |
| CTX-AI-005 | BRD-RWB-010 | FR-RWB-019 | RWB-E1-058..063 | | | | | | | | | | | | Context mapped |
| CTX-AI-006 | BRD-RWB-010 | FR-RWB-019 | RWB-E1-058..063 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-001 | BRD-RWB-001..020 | FR-RWB-001..020 | E1-E8 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-002 | BRD-RWB-001..020 | FR-RWB-001..020 | E1-E8 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-003 | BRD-RWB-003 | FR-RWB-004..010 | RWB-E1-018..031 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-004 | BRD-RWB-003 | FR-RWB-008 | RWB-E1-029 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-005 | BRD-RWB-002 | FR-RWB-003 | RWB-E1-007 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-006 | BRD-RWB-020 | FR-RWB-020 | RWB-E1-044 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-007 | BRD-RWB-020 | FR-RWB-020 | RWB-E1-047 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-008 | BRD-RWB-020 | FR-RWB-020 | INC-001, INC-002 | | | | | | | | | | | | Context mapped |
| CTX-CONSTRAINT-009 | BRD-RWB-019 | FR-RWB-020 | E5 | | | | | | | | | | | | Programme-level |
| CTX-CONSTRAINT-010 | BRD-RWB-004 | FR-RWB-013 | RWB-E1-037 | | | | | | | | | | | | Context mapped |

## 2. Epic 1 story crosswalk (INC-001)

78 items in the Epic 1 build sequence. The story file is the detailed source; the
`US ID` is the canonical story key. `GAP-001` marks the version check between the consolidated
v7 and the per-story v5 files.

| US ID | Story key | Title | Module | Type | Priority | Depends on | Window | Release | Critical path | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| US-RWB-E1-044 | RWB-E1-044 | Database migrations versioned with parameterized schema names | P3 | Enabler | Must |  | Window 1 | E1 | Yes | Specified — SUCCESS |
| US-RWB-TE-001 | RWB-TE-001 | Recovery module folder and boundary test | P2 | Enabler | Must |  | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-042 | RWB-E1-042 | Central configuration service and parameter catalog | P3 | Enabler | Must | RWB-E1-044 | Window 1 | E1 | Yes | Specified — SUCCESS |
| US-RWB-TE-002 | RWB-TE-002 | Code owners for the recovery module | P2 | Enabler | Must | RWB-TE-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-TE-003 | RWB-TE-003 | Types and contract tests from the API specification | P2 | Enabler | Must | RWB-TE-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-TE-005 | RWB-TE-005 | Rule table test harness | P3 | Enabler | Must | RWB-E1-044 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-TE-011 | RWB-TE-011 | PDPA lint for code, tests and logs | P2 | Enabler | Must | RWB-TE-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-TE-012 | RWB-TE-012 | Document storage containers | P5 | Enabler | Must | RWB-TE-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-043 | RWB-E1-043 | Reference data service with versioned tables | P3 | Enabler | Must | RWB-E1-042, RWB-E1-044 | Window 1 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-001 | RWB-E1-001 | Recovery tables for the 14 data products | P1 | User story | Must | RWB-E1-044, RWB-E1-043 | Window 1 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-003 | RWB-E1-003 | ALS daily extract load | P1 | User story | Must | RWB-E1-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-005 | RWB-E1-005 | Excel and SharePoint inventory | P1 | User story | Must | RWB-E1-001, RWB-E1-043 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-007 | RWB-E1-007 | Integration adapters for file loads and outbound files | P2 | User story | Must | RWB-E1-001 | Window 1 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-008 | RWB-E1-008 | Decision log store v1, append only and hash chained | P7 | User story | Must | RWB-E1-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-064 | RWB-E1-064 | Data dictionary for the 14 data products | P1 | Enabler | Must | RWB-E1-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-065 | RWB-E1-065 | Sandbox database with synthetic recovery data | P1 | Enabler | Must | RWB-E1-001 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-051 | RWB-E1-051 | Legacy feed jobs on ADF and Control-M | P2 | User story | Must | RWB-E1-001, RWB-E1-007 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-TE-004 | RWB-TE-004 | Masked data in SIT and UAT | P1 | Enabler | Must | RWB-E1-065 | Window 1 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-029 | RWB-E1-029 | Rule load, validation and rollback | P3 | User story | Must |  | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-047 | RWB-E1-047 | Feature flags for module release with a removal date | P2 | User story | Should | RWB-E1-001 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-010 | RWB-E1-010 | Excel and SharePoint loads | P1 | User story | Must | RWB-E1-005, RWB-E1-003 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-017 | RWB-E1-017 | Retention and archive rule for the data store | P1 | User story | Should | RWB-E1-001, RWB-E1-043, RWB-TE-012, RWB-E1-064 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-056 | RWB-E1-056 | Run books and monitoring for every Epic 1 job | P2 | Enabler | Must | RWB-E1-007 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-014 | RWB-E1-014 | Decision log copy to the data lake | P1 | User story | Should | RWB-E1-056, RWB-E1-017 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-027 | RWB-E1-027 | Decision log writer v1 | P7 | User story | Must | RWB-E1-008, RWB-E1-056 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-TE-007 | RWB-TE-007 | Scheduled jobs on Quartz | P3 | Enabler | Must | RWB-E1-044, RWB-E1-056 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-038 | RWB-E1-038 | Delegation of authority table as reference data | P4 | User story | Must | RWB-E1-043, RWB-E1-029, RWB-E1-027 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-TE-006 | RWB-TE-006 | Outbox and retry for outbound work | P2 | Enabler | Must | RWB-E1-044, RWB-E1-027, RWB-E1-007 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-TE-008 | RWB-TE-008 | Decision log hash chain check | P7 | Enabler | Must | RWB-E1-008, RWB-TE-007 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-019 | RWB-E1-019 | Roles, teams and queues as data | P3 | User story | Must | RWB-E1-038, RWB-E1-043 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-022 | RWB-E1-022 | Sign-on with SSO, MFA and the first roles | P4 | User story | Must | RWB-E1-001, RWB-E1-019 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-012 | RWB-E1-012 | Retire local copies | P1 | User story | Must | RWB-E1-022, RWB-E1-010 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-037 | RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | P4 | User story | Must | RWB-E1-022, RWB-E1-043, RWB-E1-027 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-039 | RWB-E1-039 | Access log into the decision log and break-glass admin | P4,P7 | User story | Must | RWB-E1-008, RWB-E1-022, RWB-E1-027 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-016 | RWB-E1-016 | Access control per data product and catalog entries | P1 | User story | Must | RWB-E1-037, RWB-E1-001, RWB-E1-064 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-025 | RWB-E1-025 | Document types and fields agreed | P5 | User story | Must | RWB-E1-012 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-045 | RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | P3 | Enabler | Must | RWB-E1-042, RWB-E1-043, RWB-E1-012 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-046 | RWB-E1-046 | Template and merge field catalog as data | P6 | User story | Must | RWB-E1-012 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-058 | RWB-E1-058 | Agent platform set-up [E1a] | P10 | User story | Must | RWB-E1-001, RWB-E1-003, RWB-E1-037 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-018 | RWB-E1-018 | Case ID issuance and case record v1 | P3 | User story | Must | RWB-E1-016, RWB-E1-027, RWB-E1-042 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-TE-013 | RWB-TE-013 | Agent runtime client with fallback | P10 | Enabler | Must | RWB-TE-007, RWB-E1-058, RWB-E1-027 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-013 | RWB-E1-013 | Baseline measures | P9 | User story | Must | RWB-E1-029, RWB-E1-018 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-020 | RWB-E1-020 | Allocation and assignment engine v1 | P3 | User story | Must | RWB-E1-018, RWB-E1-019, RWB-E1-027, RWB-E1-056 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-024 | RWB-E1-024 | Document store and index | P5 | User story | Must | RWB-E1-027, RWB-E1-018, RWB-E1-025, RWB-TE-012, RWB-E1-001 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-062 | RWB-E1-062 | Deviation screening agent in shadow [E2b] | P10 | User story | Must | RWB-E1-058, RWB-TE-013 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-066 | RWB-E1-066 | Interaction ledger store and writer | P1 | User story | Must | RWB-E1-018, RWB-E1-027 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-002 | RWB-E1-002 | Case list v1 with case ID, owner and queue | P1 | User story | Must | RWB-E1-018, RWB-E1-003, RWB-E1-007, RWB-E1-020 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-023 | RWB-E1-023 | Case record view v1, read only | P3 | User story | Must | RWB-E1-018, RWB-E1-024, RWB-E1-037, RWB-E1-039 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-028 | RWB-E1-028 | Service levels, timers, escalation and prescription dates | P3 | User story | Must | RWB-E1-045, RWB-E1-020, RWB-E1-027, RWB-E1-043 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-031 | RWB-E1-031 | Queue and owner on the case list with filters | P3 | User story | Must | RWB-E1-020, RWB-E1-039 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-049 | RWB-E1-049 | OCR pipeline on the Workbench document hub | P5 | User story | Must | RWB-TE-012, RWB-E1-024, RWB-E1-045 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-067 | RWB-E1-067 | Every Workbench action into the interaction ledger | P1 | User story | Must | RWB-E1-066 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-068 | RWB-E1-068 | Interaction ledger read interface | P1 | User story | Must | RWB-E1-066 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-006 | RWB-E1-006 | Data quality rules v1 | P1 | User story | Must | RWB-E1-002, RWB-E1-003, RWB-E1-043 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-021 | RWB-E1-021 | Transfer rules and engine v1 | P3 | User story | Must | RWB-E1-028, RWB-E1-020, RWB-E1-027 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-030 | RWB-E1-030 | Daily rebalancing and queue measures | P3 | User story | Must | RWB-E1-020, RWB-E1-027, RWB-E1-028 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-041 | RWB-E1-041 | Retention classes and virus scan on intake | P5 | User story | Must | RWB-E1-024, RWB-E1-049 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-050 | RWB-E1-050 | Document classification | P5 | User story | Must | RWB-E1-049, RWB-E1-025 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-011 | RWB-E1-011 | Reconciliation and data quality report | P1 | User story | Must | RWB-E1-002, RWB-E1-006 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-015 | RWB-E1-015 | Freshness stamp per data product | P1 | User story | Must | RWB-E1-003, RWB-E1-001, RWB-E1-064, RWB-E1-006 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-026 | RWB-E1-026 | Attach and search screen | P5 | User story | Must | RWB-E1-025, RWB-E1-024, RWB-E1-041, RWB-E1-045, RWB-E1-030 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-035 | RWB-E1-035 | Case record view v1.1 with documents and history timeline | P3 | User story | Should | RWB-E1-021, RWB-E1-023, RWB-E1-027 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-053 | RWB-E1-053 | Field extraction for the six types into the index | P5 | User story | Must | RWB-E1-049, RWB-E1-050, RWB-E1-025 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-057 | RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | P5 | User story | Must | RWB-E1-049, RWB-TE-012, RWB-E1-041 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-059 | RWB-E1-059 | Case intake agent in shadow [E1b] | P10 | User story | Must | RWB-E1-030, RWB-E1-058, RWB-TE-013 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-004 | RWB-E1-004 | EFS extract load | P1 | User story | Must | RWB-E1-003, RWB-E1-015, RWB-E1-002 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-009 | RWB-E1-009 | CCMS and SVAF loads | P1 | User story | Must | RWB-E1-003, RWB-E1-015, RWB-E1-007 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-032 | RWB-E1-032 | Automatic attach from the OCR intake | P5 | User story | Must | RWB-E1-024, RWB-E1-050, RWB-E1-053 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-033 | RWB-E1-033 | Search across cases | P5 | User story | Should | RWB-E1-024, RWB-E1-053, RWB-E1-049 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-034 | RWB-E1-034 | Letter template management | P6 | User story | Should | RWB-E1-046, RWB-E1-015 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-040 | RWB-E1-040 | Document checklist per case type as reference data | P5 | User story | Should | RWB-E1-024, RWB-E1-043, RWB-E1-025, RWB-E1-026 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-048 | RWB-E1-048 | Rule change audit report | P3 | Enabler | Should | RWB-E1-037, RWB-E1-011, RWB-E1-043 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-052 | RWB-E1-052 | Notice generation v1 | P6 | User story | Must | RWB-E1-015, RWB-E1-027, RWB-E1-046 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-060 | RWB-E1-060 | Extraction evaluation [E1c] | P10 | Spike | Must | RWB-E1-053, RWB-E1-058 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-061 | RWB-E1-061 | Intake agent evaluation and L1 proposal [E2a] | P10 | User story | Must | RWB-E1-059 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-054 | RWB-E1-054 | Review queue for low-confidence documents | P5 | User story | Must | RWB-E1-049, RWB-E1-035, RWB-E1-050, RWB-E1-053, RWB-E1-032 | Window 2 | E1 |  | Specified — SUCCESS |
| US-RWB-E1-063 | RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | P10 | User story | Should | RWB-E1-061, RWB-E1-007, RWB-E1-014, RWB-E1-058 | Window 2 | E1 | Yes | Specified — SUCCESS |
| US-RWB-E1-055 | RWB-E1-055 | Proof of delivery capture design with WIN | P6 | User story | Should | RWB-E1-052, RWB-E1-054, RWB-E1-028, RWB-E1-066 | Window 2 | E1 |  | Specified — SUCCESS |

## 3. Epic 2 story crosswalk (INC-002)

34 items in the Epic 2 build sequence. Epic 2 is a separate increment and does not start
until INC-001 is released.

| US ID | Story key | Title | Module | Type | Priority | Depends on | Window | Release | Critical path | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| US-RWB-TE-010 | RWB-TE-010 | Browser and accessibility tests | P2 | Enabler | Must | RWB-TE-003 | Window 3 | E2 |  | Planned |
| US-RWB-E2-003 | RWB-E2-003 | Customer's other products on the case | P2 | User story | Should | RWB-E1-007 | Window 3 | E2 |  | Planned |
| US-RWB-TE-009 | RWB-TE-009 | Performance test harness | P2 | Enabler | Must | RWB-TE-004 | Window 3 | E2 |  | Planned |
| US-RWB-E2-005 | RWB-E2-005 | Decision log query API for audit | P7 | User story | Must | RWB-E1-008, RWB-E1-039 | Window 3 | E2 |  | Planned |
| US-RWB-E2-004 | RWB-E2-004 | Treatment entity and plan timers data model | P3,P1 | User story | Must | RWB-E1-018, RWB-E1-028, RWB-E1-045 | Window 3 | E2 |  | Planned |
| US-RWB-E2-011 | RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | P3 | User story | Must | RWB-E1-020, RWB-E1-031 | Window 3 | E2 |  | Planned |
| US-RWB-E2-013 | RWB-E2-013 | Approval routing with the delegation of authority table | P7 | User story | Must | RWB-E1-038, RWB-E1-028, RWB-E1-027, RWB-E1-037 | Window 3 | E2 |  | Planned |
| US-RWB-E2-012 | RWB-E2-012 | Manual transfer and reassignment screen with reason | P3 | User story | Must | RWB-E1-021, RWB-E2-011 | Window 3 | E2 |  | Planned |
| US-RWB-E2-033 | RWB-E2-033 | Case and queue list with status, owner and ageing | P2 | User story | Must | RWB-E1-018, RWB-E1-031, RWB-E2-011 | Window 3 | E2 |  | Planned |
| US-RWB-E2-015 | RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | P3 | User story | Must | RWB-E1-028, RWB-E1-035 | Window 3 | E2 |  | Planned |
| US-RWB-E2-001 | RWB-E2-001 | EFS hand-over with full history from the COLLINS load | P2 | User story | Must | RWB-E1-004, RWB-E1-007 | Window 3 | E2 |  | Planned |
| US-RWB-E2-014 | RWB-E2-014 | Approval screen for D7.1 demand and recall notices | P7,P6 | User story | Must | RWB-E2-013, RWB-E1-052 | Window 3 | E2 |  | Planned |
| US-RWB-E2-022 | RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | P6 | User story | Must | RWB-E1-052, RWB-E1-066 | Window 3 | E2 |  | Planned |
| US-RWB-E2-002 | RWB-E2-002 | ACE plan status on the case | P2 | User story | Must | RWB-E2-001 | Window 3 | E2 |  | Planned |
| US-RWB-E2-023 | RWB-E2-023 | Automated EFS file load | P2 | User story | Should | RWB-E2-001, RWB-E1-051 | Window 3 | E2 |  | Planned |
| US-RWB-E2-021 | RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | P6 | User story | Must | RWB-E1-052, RWB-E1-055, RWB-E2-014 | Window 3 | E2 |  | Planned |
| US-RWB-E2-019 | RWB-E2-019 | Partner identities through the external gateway | P4 | User story | Should | RWB-E1-022, RWB-E1-037, RWB-E1-039 | Window 4 | E2 |  | Planned |
| US-RWB-E2-036 | RWB-E2-036 | Queue write interface for models and agents | P2 | Enabler | Must | RWB-E1-019, RWB-E1-020, RWB-E1-027 | Window 4 | E2 |  | Planned |
| US-RWB-E2-006 | RWB-E2-006 | Credit approval pack for NLEADS | P2 | User story | Must | RWB-E2-004, RWB-E1-007 | Window 4 | E2 |  | Planned |
| US-RWB-E2-007 | RWB-E2-007 | Booking confirmation from the ALS load | P2,P8 | User story | Must | RWB-E2-004, RWB-E1-007 | Window 4 | E2 |  | Planned |
| US-RWB-E2-008 | RWB-E2-008 | Payment matching with the missed payment event | P8 | User story | Must | RWB-E2-004, RWB-E1-003 | Window 4 | E2 |  | Planned |
| US-RWB-E2-032 | RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | P10 | Spike | Could | RWB-E1-058, RWB-E2-004, RWB-E1-027 | Window 4 | E2 |  | Planned |
| US-RWB-E2-010 | RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | P1 | User story | Should | RWB-E2-004, RWB-E1-016, RWB-E1-015 | Window 4 | E2 |  | Planned |
| US-RWB-E2-027 | RWB-E2-027 | Payment matching rules with the data team | P8 | User story | Must | RWB-E2-008 | Window 4 | E2 |  | Planned |
| US-RWB-E2-035 | RWB-E2-035 | Next action on the case | P2 | User story | Must | RWB-E1-018, RWB-E1-031, RWB-E2-033 | Window 4 | E2 |  | Planned |
| US-RWB-E2-016 | RWB-E2-016 | Full case record view with the history timeline | P3,P7 | User story | Must | RWB-E1-035, RWB-E2-015, RWB-E2-012 | Window 4 | E2 |  | Planned |
| US-RWB-E2-024 | RWB-E2-024 | Field app photos and bills into the document hub | P5 | User story | Must | RWB-E1-057, RWB-E1-032, RWB-E1-053, RWB-E1-024, RWB-E1-041 | Window 4 | E2 |  | Planned |
| US-RWB-E2-026 | RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | P5 | User story | Must | RWB-E1-046, RWB-E1-034, RWB-E1-024, RWB-E1-027 | Window 4 | E2 |  | Planned |
| US-RWB-E2-009 | RWB-E2-009 | Steering dashboard v1 data set | P9 | User story | Should | RWB-E1-013, RWB-E1-063 | Window 4 | E2 |  | Planned |
| US-RWB-E2-017 | RWB-E2-017 | Contract, CA and mortgage document generation screens | P5 | User story | Must | RWB-E2-026, RWB-E1-034, RWB-E1-054, RWB-TE-012 | Window 4 | E2 |  | Planned |
| US-RWB-E2-025 | RWB-E2-025 | Extraction for the stage 2 and 3 document types | P5 | User story | Must | RWB-E1-053, RWB-E1-050, RWB-E1-054 | Window 4 | E2 |  | Planned |
| US-RWB-E2-031 | RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | P10 | User story | Must | RWB-E1-063, RWB-E2-005 | Window 4 | E2 | Yes | Planned |
| US-RWB-E2-034 | RWB-E2-034 | Interaction ledger on the case and from every channel | P2 | User story | Must | RWB-E1-027, RWB-E2-016, RWB-E1-004, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006 | Window 4 | E2 |  | Planned |
| US-RWB-E2-018 | RWB-E2-018 | E-signature flow for customers and the bank | P6 | User story | Must | RWB-E2-017, RWB-E2-022 | Window 4 | E2 |  | Planned |

## 4. Epic 2 stories that go live in Epic 3

3 agent stories are built in Epic 2 but go live in Epic 3. They are part of INC-002
and are listed separately so the release boundary is visible.

| US ID | Story key | Title | Module | Type | Priority | Depends on | Window | Release | Critical path | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| US-RWB-E2-028 | RWB-E2-028 | Case intake agent live at L1 [E3a] | P10 | User story | Must | RWB-E1-061, RWB-E1-035, RWB-E1-027, RWB-E2-031 | Epic 3 | E3 | Yes | Planned (INC-002, live in E3) |
| US-RWB-E2-030 | RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | P10 | User story | Should | RWB-E1-058, RWB-E2-025, RWB-E1-061 | Epic 3 | E3 |  | Planned (INC-002, live in E3) |
| US-RWB-E2-029 | RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | P10 | User story | Must | RWB-E1-062, RWB-E2-015, RWB-E1-061, RWB-E2-028 | Epic 3 | E3 | Yes | Planned (INC-002, live in E3) |

## 5. Source-ID crosswalk

The source documents use their own IDs. They are not renumbered; this table maps them to the
canonical IDs used by the toolkit.

| Source ID family | Type | Canonical ID | US / SPEC / TEST link | Notes |
|---|---|---|---|---|
| `REQ-RDF-*` | Requirement | `FR-RWB-001`, `FR-RWB-002` | `RWB-E1-001..017`, `064..068` | Data engine |
| `REQ-DRI-*` | Requirement | `FR-RWB-003` | `RWB-E1-007`, `047`, `051`, `056` | Integration |
| `REQ-CWC-*` | Requirement | `FR-RWB-004..010` | `RWB-E1-018..031`, `035`, `042..045`, `048` | Case and workflow |
| `REQ-ACA-*` | Requirement | `FR-RWB-011..013` | `RWB-E1-022`, `037..039` | Access and administration |
| `REQ-DOC-*` | Requirement | `FR-RWB-014`, `FR-RWB-015` | `RWB-E1-024..026`, `032..033`, `040..041`, `049..050`, `053..054`, `057` | Document hub |
| `REQ-COM-*` | Requirement | `FR-RWB-016` | `RWB-E1-034`, `046`, `052`, `055` | Communications |
| `REQ-DEC-*` | Requirement | `FR-RWB-017` | `RWB-E1-008`, `027` | Decision log |
| `REQ-PAY-*` | Requirement | `FR-RWB-002`, `FR-RWB-003` | `RWB-E1-007`, `056` | Payments and posting |
| `REQ-RPT-*` | Requirement | `FR-RWB-018` | `RWB-E1-013` | Reporting |
| `REQ-AGT-*` | Requirement | `FR-RWB-019` | `RWB-E1-058..063` | Agent runtime |
| `REQ-ROU-*` | Requirement | `BRD-RWB-011` | E4 | Programme-level |
| `REQ-TRT-*` | Requirement | `BRD-RWB-012` | E2/E3 | Programme-level |
| `REQ-GUA-*` | Requirement | `BRD-RWB-013` | E4 | Programme-level |
| `REQ-LIT-*` | Requirement | `BRD-RWB-014` | E2/E5 | Programme-level |
| `REQ-AST-*` | Requirement | `BRD-RWB-015` | E3/E4 | Programme-level |
| `REQ-DSL-*` | Requirement | `BRD-RWB-016` | E5/E6 | Programme-level |
| `REQ-WOF-*` | Requirement | `BRD-RWB-017` | E6 | Programme-level |
| `REQ-DEV-*` | Requirement | `BRD-RWB-018` | E2/E7 | Programme-level |
| `REQ-PRT-*` | Requirement | `BRD-RWB-019` | E6/E7 | Programme-level |
| `RWB-E1-*` | Story | `US-RWB-E1-*` | Epic 1 story crosswalk | Per-story file |
| `RWB-TE-*` | Enabler | `US-RWB-TE-*` | Epic 1 story crosswalk | 13 technical enablers |
| `RWB-E2-*` | Story | `US-RWB-E2-*` | Epic 2 story crosswalk | Per-story file |
| `BR-*` | Business rule | `BR-RWB-*` | Rule family table | Preserve the source ID in the spec |
| `MSG-*` | Message | `ERR-RWB-*` | Error handling table | Preserve the source ID in the spec |
| `DF-*` | Data field | `DP-*` / field ID | Logical data model | Preserve the field ID in the spec |
| `TC-*` | Test case | `TEST-*` | Test cases workbook | Preserve the test ID in the test evidence |
| `CTL-*` | Control | `REVIEW-*` / test | Controls Catalog | Preserve the control ID in the review evidence |
| `DL*` | Decision | `Q-RWB-*` / `CTX-GAP-*` | Open questions | Preserve the decision log ID |

## 6. Gap markers

| Gap | Affected rows | Status |
|---|---|---|
| GAP-001 Epic 1 story files v5 vs consolidated v7 | Epic 1 story crosswalk | Open — use the consolidated v7 as the narrative and record the story version in the spec header |
| GAP-002 Epic 2 story files v4 vs consolidated v5 | Epic 2 story crosswalk | Open — use the consolidated v5 as the narrative |
| GAP-005 No ACE source code | All `SPEC`/`TASK`/`CODE` rows | Open — blocks Build, not Specify/Plan |
| GAP-006 Named approvers | All approval rows | Open — `TBC` in the increment cards |
| GAP-010 Same-day interfaces | `INT-RWB-*` rows | Open — default end-of-day |
| GAP-011 Jira keys | `GitHub Issue` column | Open — blank until the Jira project exists |

## 7. How to update this matrix

1. Technical Specifier adds `SPEC-*` and links each to `FR-RWB-*`/`NFR-RWB-*`.
2. Implementation Planner adds `TASK-*` and links each to `SPEC-*`.
3. Implementation Builder adds `CODE-*` and unit-test `TEST-*` references.
4. API Tester adds `APT-*`; Functional Automation Test adds `FT-*`.
5. Compliance Reviewer adds `REVIEW-*`; Technical Documenter adds `DOC-*`.
6. Traceability Manager reconciles the chain and flags orphans, requirements without specs,
   specs without tasks, tasks without code, APIs/UI without test results, and requirements
   without tests.

## 8. Epic 1 specification coverage

One row per Epic 1 story. `SPEC-<KEY>-*` is the spec ID family; the exact SPEC IDs are in each
spec. A `BLOCKED` row has an open source decision and must not go to the Implementation Planner.

| Story key | Spec ID | Status | UI | API | Open CLARs | Compliance | Spec path |
|---|---|---|---|---|---|---|---|
| RWB-E1-044 | SPEC-RWB-E1-044-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` |
| RWB-TE-001 | SPEC-RWB-TE-001-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` |
| RWB-E1-042 | SPEC-RWB-E1-042-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` |
| RWB-TE-002 | SPEC-RWB-TE-002-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` |
| RWB-TE-003 | SPEC-RWB-TE-003-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md` |
| RWB-TE-005 | SPEC-RWB-TE-005-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-006-epic-1-RWB-TE-005/specify/spec.md` |
| RWB-TE-011 | SPEC-RWB-TE-011-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-007-epic-1-RWB-TE-011/specify/spec.md` |
| RWB-TE-012 | SPEC-RWB-TE-012-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-008-epic-1-RWB-TE-012/specify/spec.md` |
| RWB-E1-043 | SPEC-RWB-E1-043-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-009-epic-1-RWB-E1-043/specify/spec.md` |
| RWB-E1-001 | SPEC-RWB-E1-001-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-010-epic-1-RWB-E1-001/specify/spec.md` |
| RWB-E1-003 | SPEC-RWB-E1-003-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-011-epic-1-RWB-E1-003/specify/spec.md` |
| RWB-E1-005 | SPEC-RWB-E1-005-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-012-epic-1-RWB-E1-005/specify/spec.md` |
| RWB-E1-007 | SPEC-RWB-E1-007-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-013-epic-1-RWB-E1-007/specify/spec.md` |
| RWB-E1-008 | SPEC-RWB-E1-008-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-014-epic-1-RWB-E1-008/specify/spec.md` |
| RWB-E1-064 | SPEC-RWB-E1-064-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-015-epic-1-RWB-E1-064/specify/spec.md` |
| RWB-E1-065 | SPEC-RWB-E1-065-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-016-epic-1-RWB-E1-065/specify/spec.md` |
| RWB-E1-051 | SPEC-RWB-E1-051-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-017-epic-1-RWB-E1-051/specify/spec.md` |
| RWB-TE-004 | SPEC-RWB-TE-004-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-018-epic-1-RWB-TE-004/specify/spec.md` |
| RWB-E1-029 | SPEC-RWB-E1-029-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-019-epic-1-RWB-E1-029/specify/spec.md` |
| RWB-E1-047 | SPEC-RWB-E1-047-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-020-epic-1-RWB-E1-047/specify/spec.md` |
| RWB-E1-010 | SPEC-RWB-E1-010-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-021-epic-1-RWB-E1-010/specify/spec.md` |
| RWB-E1-017 | SPEC-RWB-E1-017-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-022-epic-1-RWB-E1-017/specify/spec.md` |
| RWB-E1-056 | SPEC-RWB-E1-056-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-023-epic-1-RWB-E1-056/specify/spec.md` |
| RWB-E1-014 | SPEC-RWB-E1-014-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-024-epic-1-RWB-E1-014/specify/spec.md` |
| RWB-E1-027 | SPEC-RWB-E1-027-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-025-epic-1-RWB-E1-027/specify/spec.md` |
| RWB-TE-007 | SPEC-RWB-TE-007-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-026-epic-1-RWB-TE-007/specify/spec.md` |
| RWB-E1-038 | SPEC-RWB-E1-038-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-027-epic-1-RWB-E1-038/specify/spec.md` |
| RWB-TE-006 | SPEC-RWB-TE-006-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-028-epic-1-RWB-TE-006/specify/spec.md` |
| RWB-TE-008 | SPEC-RWB-TE-008-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-029-epic-1-RWB-TE-008/specify/spec.md` |
| RWB-E1-019 | SPEC-RWB-E1-019-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-030-epic-1-RWB-E1-019/specify/spec.md` |
| RWB-E1-022 | SPEC-RWB-E1-022-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-031-epic-1-RWB-E1-022/specify/spec.md` |
| RWB-E1-012 | SPEC-RWB-E1-012-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-032-epic-1-RWB-E1-012/specify/spec.md` |
| RWB-E1-037 | SPEC-RWB-E1-037-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-033-epic-1-RWB-E1-037/specify/spec.md` |
| RWB-E1-039 | SPEC-RWB-E1-039-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-034-epic-1-RWB-E1-039/specify/spec.md` |
| RWB-E1-016 | SPEC-RWB-E1-016-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-035-epic-1-RWB-E1-016/specify/spec.md` |
| RWB-E1-025 | SPEC-RWB-E1-025-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-036-epic-1-RWB-E1-025/specify/spec.md` |
| RWB-E1-045 | SPEC-RWB-E1-045-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-037-epic-1-RWB-E1-045/specify/spec.md` |
| RWB-E1-046 | SPEC-RWB-E1-046-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-038-epic-1-RWB-E1-046/specify/spec.md` |
| RWB-E1-058 | SPEC-RWB-E1-058-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-039-epic-1-RWB-E1-058/specify/spec.md` |
| RWB-E1-018 | SPEC-RWB-E1-018-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-040-epic-1-RWB-E1-018/specify/spec.md` |
| RWB-TE-013 | SPEC-RWB-TE-013-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-041-epic-1-RWB-TE-013/specify/spec.md` |
| RWB-E1-013 | SPEC-RWB-E1-013-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-042-epic-1-RWB-E1-013/specify/spec.md` |
| RWB-E1-020 | SPEC-RWB-E1-020-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-043-epic-1-RWB-E1-020/specify/spec.md` |
| RWB-E1-024 | SPEC-RWB-E1-024-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-044-epic-1-RWB-E1-024/specify/spec.md` |
| RWB-E1-062 | SPEC-RWB-E1-062-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-045-epic-1-RWB-E1-062/specify/spec.md` |
| RWB-E1-066 | SPEC-RWB-E1-066-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-046-epic-1-RWB-E1-066/specify/spec.md` |
| RWB-E1-002 | SPEC-RWB-E1-002-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-047-epic-1-RWB-E1-002/specify/spec.md` |
| RWB-E1-023 | SPEC-RWB-E1-023-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-048-epic-1-RWB-E1-023/specify/spec.md` |
| RWB-E1-028 | SPEC-RWB-E1-028-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-049-epic-1-RWB-E1-028/specify/spec.md` |
| RWB-E1-031 | SPEC-RWB-E1-031-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-050-epic-1-RWB-E1-031/specify/spec.md` |
| RWB-E1-049 | SPEC-RWB-E1-049-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-051-epic-1-RWB-E1-049/specify/spec.md` |
| RWB-E1-067 | SPEC-RWB-E1-067-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-052-epic-1-RWB-E1-067/specify/spec.md` |
| RWB-E1-068 | SPEC-RWB-E1-068-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-053-epic-1-RWB-E1-068/specify/spec.md` |
| RWB-E1-006 | SPEC-RWB-E1-006-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-054-epic-1-RWB-E1-006/specify/spec.md` |
| RWB-E1-021 | SPEC-RWB-E1-021-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-055-epic-1-RWB-E1-021/specify/spec.md` |
| RWB-E1-030 | SPEC-RWB-E1-030-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-056-epic-1-RWB-E1-030/specify/spec.md` |
| RWB-E1-041 | SPEC-RWB-E1-041-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-057-epic-1-RWB-E1-041/specify/spec.md` |
| RWB-E1-050 | SPEC-RWB-E1-050-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-058-epic-1-RWB-E1-050/specify/spec.md` |
| RWB-E1-011 | SPEC-RWB-E1-011-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-059-epic-1-RWB-E1-011/specify/spec.md` |
| RWB-E1-015 | SPEC-RWB-E1-015-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-060-epic-1-RWB-E1-015/specify/spec.md` |
| RWB-E1-026 | SPEC-RWB-E1-026-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-061-epic-1-RWB-E1-026/specify/spec.md` |
| RWB-E1-035 | SPEC-RWB-E1-035-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-062-epic-1-RWB-E1-035/specify/spec.md` |
| RWB-E1-053 | SPEC-RWB-E1-053-* | SUCCESS | YES | NO | 0 | PASS | `output/INC-063-epic-1-RWB-E1-053/specify/spec.md` |
| RWB-E1-057 | SPEC-RWB-E1-057-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-064-epic-1-RWB-E1-057/specify/spec.md` |
| RWB-E1-059 | SPEC-RWB-E1-059-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-065-epic-1-RWB-E1-059/specify/spec.md` |
| RWB-E1-004 | SPEC-RWB-E1-004-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-066-epic-1-RWB-E1-004/specify/spec.md` |
| RWB-E1-009 | SPEC-RWB-E1-009-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-067-epic-1-RWB-E1-009/specify/spec.md` |
| RWB-E1-032 | SPEC-RWB-E1-032-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-068-epic-1-RWB-E1-032/specify/spec.md` |
| RWB-E1-033 | SPEC-RWB-E1-033-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-069-epic-1-RWB-E1-033/specify/spec.md` |
| RWB-E1-034 | SPEC-RWB-E1-034-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-070-epic-1-RWB-E1-034/specify/spec.md` |
| RWB-E1-040 | SPEC-RWB-E1-040-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-071-epic-1-RWB-E1-040/specify/spec.md` |
| RWB-E1-048 | SPEC-RWB-E1-048-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-072-epic-1-RWB-E1-048/specify/spec.md` |
| RWB-E1-052 | SPEC-RWB-E1-052-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-073-epic-1-RWB-E1-052/specify/spec.md` |
| RWB-E1-060 | SPEC-RWB-E1-060-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-074-epic-1-RWB-E1-060/specify/spec.md` |
| RWB-E1-061 | SPEC-RWB-E1-061-* | SUCCESS | NO | YES | 0 | PASS | `output/INC-075-epic-1-RWB-E1-061/specify/spec.md` |
| RWB-E1-054 | SPEC-RWB-E1-054-* | SUCCESS | YES | YES | 0 | PASS | `output/INC-076-epic-1-RWB-E1-054/specify/spec.md` |
| RWB-E1-063 | SPEC-RWB-E1-063-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-077-epic-1-RWB-E1-063/specify/spec.md` |
| RWB-E1-055 | SPEC-RWB-E1-055-* | SUCCESS | NO | NO | 0 | PASS | `output/INC-078-epic-1-RWB-E1-055/specify/spec.md` |

`Traceability Manager status: RECONCILED — 113 CTX rows, 115 story items, 0 orphans in the seeded
range. Epic 1: 78 specs (SUCCESS: 78. Compliance: 78 PASS). Later stages must complete the chain.`
