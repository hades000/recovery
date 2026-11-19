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


edit(S1, [
    ("""| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |""",
     """| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-08 | COLLINS models | In, into ACE | ACE ingestion (ACE team); S1 reads `v_ace_score` | Daily; monthly for some models |
| INT-11 | SVAF | In, into ACE | ACE ingestion (ACE team); S1 reads `v_ace_valuation` | Weekly |
| None | ACE database | In | `recovery.v_ace_valuation` and `recovery.v_ace_score`, SELECT only | As each ACE batch completes |"""),
    ("""| Event | Direction |
|---|---|
| None | |""",
     """| Event | Direction |
|---|---|
| AceDataReady | Consumed: a new appraisal or score is readable |
| ValuationAccepted | Published: the Workbench accepted an appraisal in `valuation_ext` |"""),
])

edit(S5, [
    ("""| INT-11 | SVAF | In | File load | Weekly |
| INT-12 | AMIS | In | File load | Monthly |
| INT-13 | RPS | In | File load | Weekly |""",
     """| INT-11 | SVAF | In, into ACE | ACE ingestion (ACE team); S5 reads `v_ace_valuation` | Weekly |
| INT-12 | AMIS | In, into ACE | ACE ingestion (ACE team); S5 reads `v_ace_npa_asset` and `v_ace_npa_sale` | Monthly |
| INT-13 | RPS | In, into ACE | ACE ingestion (ACE team); S5 reads `v_ace_npa_asset` | Weekly |
| None | ACE database | In | `recovery.v_ace_npa_asset`, `recovery.v_ace_npa_sale` and `recovery.v_ace_asset`, SELECT only | As each ACE batch completes |"""),
    ("""| API-S5-002 | GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R | E3 |
| API-S5-003 | POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C | E3 |
| API-S5-004 | POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C | E3 |""",
     """| API-S5-002 | GET | /api/recovery/v1/assets/{assetKey} | Asset and disposal R | E3 |
| API-S5-003 | POST | /api/recovery/v1/assets/{assetKey}/valuations | Asset and disposal C | E3 |
| API-S5-004 | POST | /api/recovery/v1/assets/{assetKey}/listings | Asset and disposal C | E3 |"""),
    ("""#### API-S5-002 GET /assets/{assetId}""", """#### API-S5-002 GET /assets/{assetKey}"""),
    ("""| Purpose | Read one asset with title, condition, valuations, costs and listing |""",
     """| Purpose | Read one asset with title, condition, valuations, costs and listing; the asset and its title come from `v_ace_npa_asset` and `v_ace_asset`, the appraisals from `v_ace_valuation` |"""),
    ("""#### API-S5-003 POST /assets/{assetId}/valuations""", """#### API-S5-003 POST /assets/{assetKey}/valuations"""),
    ("""| Purpose | Order or record a valuation |""",
     """| Purpose | Order an appraisal of the asset; when the SVAF appraisal appears in `v_ace_valuation`, the officer accepts it in `valuation_ext` |"""),
    ("""#### API-S5-004 POST /assets/{assetId}/listings""", """#### API-S5-004 POST /assets/{assetKey}/listings"""),
    ("""| Purpose | Set the list price and floor and send for approval |""",
     """| Purpose | Set the list price and floor for the ACE asset and send for approval; the listing holds `asset_key` |"""),
])
