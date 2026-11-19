import os

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
S1 = os.path.join(ROOT, r"_work\staging\Recovery Workbench TSD S1 Valuation and route v2.md")
S5 = os.path.join(ROOT, r"_work\staging\Recovery Workbench TSD S5 Assets and auction v2.md")


def edit(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        assert old in s, "NOT FOUND in %s: %s" % (os.path.basename(path), old[:90])
        s = s.replace(old, new, 1)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    bad = sorted({c for c in s if ord(c) > 127})
    print(os.path.basename(path), len(s), "non-ascii", bad)


def splice(path, start_marker, end_marker, new_block):
    s = open(path, encoding="utf-8").read()
    i = s.index(start_marker)
    j = s.index(end_marker, i)
    s = s[:i] + new_block + s[j:]
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    return s


s1_doc_old = """| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
"""
s1_doc_new = """| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
| Decision | D-RCV-35 (U1 to U5), ADR-010 |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with the Workbench valuation and score copies |
| 3 | 15 November 2026 | D-RCV-35: the appraisal is read from `v_ace_valuation` and the score from `v_ace_score`; the Workbench keeps only its decision in `valuation_ext`, keyed by `valuation_key`. The valuation and score copies leave the schema |
"""
edit(S1, [
    ("Henka Group, 28 October 2026.", "Henka Group, 15 November 2026."),
    ("| Document ID | S1-RWB-TSD-v2 |", "| Document ID | S1-RWB-TSD-v3 |"),
    (s1_doc_old, s1_doc_new),
    ("It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.",
     "It reaches other modules only through their published interfaces, and it reads appraisals and scores only through `recovery.v_ace_valuation` and `recovery.v_ace_score`."),
])

splice(S1, "### T3.1 Object and field definitions", "### T3.2 Lists of values", """### T3.1 Object and field definitions

The appraisal and the score are ACE records. S1 reads them and holds only its own decision about an appraisal. It has no valuation table and no score table, and it writes nothing to ACE.

**v_ace_valuation** (ACE, read-only; Section B). An SVAF appraisal as ingested into ACE and read through the view. Key: `valuation_key`. 9 fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-187 | valuation_key | TEXT | varchar(255) | Yes | None | ACE `valuation.valuation_key` |
| DF-ACE-188 | asset_key | TEXT | varchar(255) | No | None | ACE `valuation.asset_key` |
| DF-ACE-189 | appraisal_no | TEXT | varchar(20) | Yes | None | ACE `valuation.appraisal_no` |
| DF-ACE-190 | appraisal_type | LOV | varchar(15) | Yes | LOV-APPRAISAL | ACE `valuation.appraisal_type` |
| DF-ACE-191 | appraised_value | NUMBER | numeric(18,2) | Yes | None | ACE `valuation.appraised_value` |
| DF-ACE-192 | forced_sale_value | NUMBER | numeric(18,2) | No | None | ACE `valuation.forced_sale_value` |
| DF-ACE-193 | appraisal_date | DATE | date | Yes | None | ACE `valuation.appraisal_date` |
| DF-ACE-194 | source_system | TEXT | varchar(20) | Yes | None | ACE `valuation.source_system` (SVAF) |
| DF-ACE-195 | data_as_of | DATE | date | Yes | None | ACE `valuation.business_date` |

The view is Section B because ACE holds no appraisal today; it is created the week RWB-ACE-001 lands. Until then the valuation screens and the D7 route rule stay behind their flag. `accepted`, `stale_flag`, `age_days` and the valuer are Workbench decisions and are not in ACE.

**v_ace_score** (ACE, read-only; Section B). A COLLINS score, estimate and route as ingested into ACE. Key: `score_key`. 10 fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-270 | score_key | TEXT | varchar(255) | Yes | None | ACE `collins_score.score_key` |
| DF-ACE-271 | account_key | TEXT | varchar(255) | No | None | ACE `collins_score.account_key` |
| DF-ACE-272 | model_code | TEXT | varchar(30) | Yes | None | ACE `collins_score.model_code` |
| DF-ACE-273 | model_version | TEXT | varchar(20) | Yes | None | ACE `collins_score.model_version` |
| DF-ACE-274 | score_value | NUMBER | numeric(12,4) | No | None | ACE `collins_score.score_value` |
| DF-ACE-275 | estimate_value | NUMBER | numeric(18,2) | No | None | ACE `collins_score.estimate_value` |
| DF-ACE-276 | route_code | LOV | varchar(4) | No | LOV-ROUTE | ACE `collins_score.route_code` |
| DF-ACE-277 | scored_at | DATE | timestamptz | Yes | None | ACE `collins_score.scored_at` |
| DF-ACE-278 | source_system | TEXT | varchar(20) | Yes | None | ACE `collins_score.source_system` (COLLINS) |
| DF-ACE-279 | data_as_of | DATE | date | Yes | None | ACE `collins_score.business_date` |

The view is Section B. The route decision is recorded on the case (`recovery_case.route_code`, `route_state`), not on the score: the score is an input, the decision is Workbench-owned.

**valuation_ext** (NEW). The Workbench decision about an ACE appraisal. Key: `valuation_key`. A 1:1 table with `v_ace_valuation`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-EXT-036 | valuation_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_valuation.valuation_key` |
| DF-EXT-037 | accepted | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-038 | accepted_at | DATE | timestamptz | No | None | Workbench |
| DF-EXT-039 | accepted_by | CROSS_REF | uuid | No | None | Workbench |
| DF-EXT-040 | valuer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-EXT-041 | stale_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-EXT-042 | age_days | NUMBER | integer | No | None | Workbench |

Plus the seven standard record columns, DF-EXT-043 to DF-EXT-049. A missing row means the appraisal is not accepted and is judged stale by its date alone.

The version 2 tables `valuation` and `score` leave Physical Schema v5. Their field IDs DF-COL-018 to DF-COL-027 and DF-DEC-019 to DF-DEC-027 are retired and not reused.

""")

splice(S1, "### T3.3 Relationships", "## T4. State machines and workflow", """### T3.3 Relationships

| From | Field | To | Cardinality |
|---|---|---|---|
| valuation_ext | valuation_key | v_ace_valuation | One to one; business key, no foreign key |
| valuation_ext | valuer_partner_id | partner | Many to 0 or 1 |
| v_ace_valuation | asset_key | v_ace_asset | Many to 0 or 1; business key, no foreign key |
| v_ace_score | account_key | v_ace_account | Many to 0 or 1; business key, no foreign key |

No relationship here is a foreign key into ACE. A score or an appraisal that ACE has not ingested has no row to read, and the screen shows the last ACE business date rather than an empty value.

""")

s5_doc_old = """| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
"""
s5_doc_new = """| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
| Decision | D-RCV-35 (U1 to U5), ADR-010 |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with the Workbench asset copy, listings and asset sales |
| 3 | 15 November 2026 | D-RCV-35: the held asset is read from `v_ace_npa_asset` and the NPA sale from `v_ace_npa_sale`; the asset copy leaves the schema; `listing` and `asset_sale` link by `asset_key` with no foreign key into ACE |
"""
edit(S5, [
    ("Henka Group, 28 October 2026.", "Henka Group, 15 November 2026."),
    ("| Document ID | S5-RWB-TSD-v2 |", "| Document ID | S5-RWB-TSD-v3 |"),
    (s5_doc_old, s5_doc_new),
    ("It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.",
     "It reaches other modules only through their published interfaces, and it reads assets and NPA sales only through `recovery.v_ace_npa_asset`, `recovery.v_ace_npa_sale` and `recovery.v_ace_asset`."),
])

splice(S5, "### T3.1 Object and field definitions", "### T3.2 Lists of values", """### T3.1 Object and field definitions

The held asset and its sale are ACE records. S5 reads them and owns the work that follows: the holding decision, the listing, the auction rounds and the sale record. There is no Workbench asset table, and nothing is written to ACE.

**v_ace_npa_asset** (ACE, read-only; Section B). An NPA asset from AMIS (property) and RPS (vehicles), as ingested into ACE. Key: `asset_key`. 12 fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-208 | asset_ref | TEXT | varchar(255) | Yes | None | ACE `npa_asset.asset_key` |
| DF-ACE-209 | asset_key | TEXT | varchar(255) | Yes | None | ACE `npa_asset.asset_key` |
| DF-ACE-210 | asset_code | TEXT | varchar(20) | No | None | ACE `npa_asset.asset_code` |
| DF-ACE-211 | transfer_in_type | LOV | varchar(20) | Yes | LOV-TRANSFER-IN | ACE `npa_asset.transfer_in_type` |
| DF-ACE-212 | from_segment | LOV | varchar(20) | No | LOV-SEGMENT | ACE `npa_asset.from_segment` |
| DF-ACE-213 | transfer_in_date | DATE | date | Yes | None | ACE `npa_asset.transfer_in_date` |
| DF-ACE-214 | book_value | NUMBER | numeric(18,2) | Yes | None | ACE `npa_asset.book_value` |
| DF-ACE-215 | auction_purchase_price | NUMBER | numeric(18,2) | No | None | ACE `npa_asset.auction_purchase_price` |
| DF-ACE-216 | repossessed_date | DATE | date | No | None | ACE `npa_asset.repossessed_date` |
| DF-ACE-217 | stock_date | DATE | date | No | None | ACE `npa_asset.stock_date` |
| DF-ACE-218 | source_system | TEXT | varchar(20) | Yes | None | ACE `npa_asset.source_system` (AMIS or RPS) |
| DF-ACE-219 | data_as_of | DATE | date | Yes | None | ACE `npa_asset.business_date` |

**v_ace_npa_sale** (ACE, read-only; Section B). An NPA sale contract from AMIS, as ingested into ACE. Key: `npa_sale_key`. 11 fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-220 | npa_sale_key | TEXT | varchar(255) | Yes | None | ACE `npa_sale.npa_sale_key` |
| DF-ACE-221 | npa_asset_key | TEXT | varchar(255) | Yes | None | ACE `npa_sale.npa_asset_key` |
| DF-ACE-222 | contract_date | DATE | date | Yes | None | ACE `npa_sale.contract_date` |
| DF-ACE-223 | sale_date | DATE | date | Yes | None | ACE `npa_sale.sale_date` |
| DF-ACE-224 | sale_price | NUMBER | numeric(18,2) | Yes | None | ACE `npa_sale.sale_price` |
| DF-ACE-225 | transfer_fee | NUMBER | numeric(18,2) | No | None | ACE `npa_sale.transfer_fee` |
| DF-ACE-226 | specific_business_tax | NUMBER | numeric(18,2) | No | None | ACE `npa_sale.specific_business_tax` |
| DF-ACE-227 | corporate_income_tax | NUMBER | numeric(18,2) | No | None | ACE `npa_sale.corporate_income_tax` |
| DF-ACE-228 | incentive_amount | NUMBER | numeric(18,2) | No | None | ACE `npa_sale.incentive_amount` |
| DF-ACE-229 | source_system | TEXT | varchar(20) | Yes | None | ACE `npa_sale.source_system` (AMIS) |
| DF-ACE-230 | data_as_of | DATE | date | Yes | None | ACE `npa_sale.business_date` |

The collateral asset behind an NPA asset is read through `v_ace_asset`, on the same `asset_key`, when the case needs title and address.

**listing** (KEPT). An asset offered for sale, with its prices and rounds. `asset_key` is the ACE business key of `v_ace_npa_asset`; it carries no foreign key.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-002 | asset_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_npa_asset.asset_key` |
| DF-SAL-003 | sale_channel | LOV | varchar(15) | Yes | LOV-SALE-CHANNEL | Workbench |
| DF-SAL-004 | start_price | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-SAL-005 | floor_price | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-SAL-006 | round_no | NUMBER | integer | Yes | None | Workbench |
| DF-SAL-007 | listed_at | DATE | timestamptz | No | None | Workbench |
| DF-SAL-008 | status | LOV | varchar(12) | Yes | LOV-LISTING | Workbench |

**asset_sale** (KEPT). The Workbench record of an asset sale, with the buyer, the listing and the gain or loss. `asset_key` is the ACE business key of `v_ace_npa_asset`.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-009 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-010 | asset_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_npa_asset.asset_key` |
| DF-SAL-011 | listing_id | CROSS_REF | uuid | No | None | Workbench |
| DF-SAL-012 | contract_date | DATE | date | Yes | None | ACE `v_ace_npa_sale.contract_date` |
| DF-SAL-013 | sale_date | DATE | date | Yes | None | ACE `v_ace_npa_sale.sale_date` |
| DF-SAL-014 | sale_price | NUMBER | numeric(18,2) | Yes | None | ACE `v_ace_npa_sale.sale_price` |
| DF-SAL-015 | transfer_fee | NUMBER | numeric(18,2) | No | None | ACE `v_ace_npa_sale.transfer_fee` |
| DF-SAL-016 | specific_business_tax | NUMBER | numeric(18,2) | No | None | ACE `v_ace_npa_sale.specific_business_tax` |
| DF-SAL-017 | corporate_income_tax | NUMBER | numeric(18,2) | No | None | ACE `v_ace_npa_sale.corporate_income_tax` |
| DF-SAL-018 | gain_loss | FORMULA | numeric(18,2) | No | None | Workbench |
| DF-SAL-019 | incentive_amount | NUMBER | numeric(18,2) | No | None | ACE `v_ace_npa_sale.incentive_amount` |

The seven sale columns DF-SAL-012 to DF-SAL-017 and DF-SAL-019 are the DEF-05 carried snapshot of the AMIS contract: the live values are in `v_ace_npa_sale`, and the owning story either drops the columns and reads the view or states why the snapshot is kept for the sale audit.

The version 2 table `asset` leaves Physical Schema v5. Its field IDs DF-COL-028 to DF-COL-042 are retired and not reused; `holding_status` and `holding_cost_to_date` are Workbench-owned and move to the treatment record, which already holds the holding decision.

""")

splice(S5, "### T3.3 Relationships", "## T4. State machines and workflow", """### T3.3 Relationships

| From | Field | To | Cardinality |
|---|---|---|---|
| v_ace_npa_sale | npa_asset_key | v_ace_npa_asset | Many to 1; business key, no foreign key |
| v_ace_npa_asset | asset_key | v_ace_asset | Many to 0 or 1; business key, no foreign key |
| listing | asset_key | v_ace_npa_asset | Many to 1; business key, no foreign key |
| asset_sale | asset_key | v_ace_npa_asset | Many to 1; business key, no foreign key |
| asset_sale | listing_id | listing | Many to 0 or 1 |

No relationship here is a foreign key into ACE.
""")
