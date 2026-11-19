import os

p = os.path.join(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14", r"_work\scripts\build_erd_v4.py")
s = open(p, encoding="utf-8").read()

old = """for vname, v in views.items():
    c = cdm_view[vname]
    fields = []
    for f in ldm_fields[vname]:
        fields.append({"name": f["name"], "pk": False, "ak": None, "fk": False,
                       "bk": f["name"] in ("account_key", "person_key", "contact_key",
                                           "asset_key", "payment_code", "valuation_key")})"""
new = """SECTION_B_COLS = {
    "v_ace_account": ["business_unit", "principal_outstanding", "interest_outstanding",
                      "fees_outstanding", "daily_bucket", "settlement_booked_date",
                      "settlement_booked_amount"],
    "v_ace_customer": ["party_type", "id_type", "segment"],
    "v_ace_efs_action": ["contact_result", "action_contact_status"],
}
for vname, v in views.items():
    c = cdm_view[vname]
    fields = []
    for f in ldm_fields[vname]:
        fields.append({"name": f["name"], "pk": False, "ak": None, "fk": False,
                       "bk": f["name"] in ("account_key", "person_key", "contact_key",
                                           "asset_key", "payment_code", "valuation_key")})
    for col in SECTION_B_COLS.get(vname, []):
        fields.append({"name": col, "pk": False, "ak": None, "fk": False, "bk": False, "sb": True})"""
assert old in s
s = s.replace(old, new, 1)

old = """        if f["bk"]:
            marks.append("BK")"""
new = """        if f["bk"]:
            marks.append("BK")
        if f.get("sb"):
            marks.append("B")"""
assert old in s
s = s.replace(old, new, 1)

old = """<h3>View boxes</h3><p class="muted">Every view box is dashed: it is external to the recovery schema and read only. The fields are the view columns named for the Workbench, not the ACE column names.</p>"""
new = """<h3>View boxes</h3><p class="muted">Every view box is dashed: it is external to the recovery schema and read only. The fields are the view columns named for the Workbench, not the ACE column names. A field marked B is one of the 12 Tier 2 columns that V0003 adds to an existing view through CREATE OR REPLACE VIEW: seven on v_ace_account, three on v_ace_customer and two on v_ace_efs_action.</p>"""
assert old in s
s = s.replace(old, new, 1)

old = """<p>122 objects in 14 data products: 88 Workbench tables, 4 extension tables and 30 ACE source views, with 104 references. The views are external and read only."""
new = """<p>122 objects: 88 Workbench tables, 4 extension tables and 30 ACE source views, with 104 references. The 14 data products hold 97 of them; OPS, AGT and RPT hold the other 25. The views are external and read only."""
assert old in s
s = s.replace(old, new, 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
