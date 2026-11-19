"""Shared field-map builder for the Interface Specifications v3 fix (md + xlsx stay identical)."""
import openpyxl, os

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
IFX = os.path.join(ROOT, "05 Technical architecture", "Recovery Workbench Interface Specifications v3.xlsx")
DISP = os.path.join(ROOT, "05 Technical architecture", "Recovery Workbench System Disposition and Integration Inventory v3.xlsx")
MD = os.path.join(ROOT, "05 Technical architecture", "Recovery Workbench Interface Specifications v3.md")
LDM = os.path.join(ROOT, "06 Data", "Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx")

PLACEHOLDER = "New ACE interface (number in Interface Specifications v3)"
OUTBOUND = {"INT-14", "INT-25"}

HEADER = ["Interface", "Source field", "Table.column", "Tier", "Read path", "LDM field",
          "Data type", "Physical type", "Mandatory", "Transformation", "Owner"]

TRANSFORM = {
    "DF-ACC-002": "Direct copy; ACE business key",
    "DF-ACC-008": "Direct copy; the view casts numeric(38,2) to numeric(7,4)",
    "DF-ACC-014": "Direct copy; renamed days_past_due in the view",
    "DF-ACC-015": "Direct copy; daily bucket (bucket_log_snapshot is monthly)",
    "DF-ACC-019": "Y/N text cast to boolean by recovery.ace_to_boolean in the view",
    "DF-ACC-021": "Business date of the ACE batch",
    "DF-ACC-024": "Direct copy; ACE business key",
    "DF-ACC-025": "varchar cast to date by recovery.ace_to_date in the view",
    "DF-ACC-028": "Read from the account batch date; no new payment column",
    "DF-FIN-007": "varchar cast to date by recovery.ace_to_date in the view",
    "DF-PTY-002": "Direct copy; ACE business key",
    "DF-COL-031": "Direct copy; ACE business key",
}
OUT_READ = {"DF-SAL-035": "Snapshot of v_ace_account.total_balance at the cut-off date"}


def ldm_maps():
    wb = openpyxl.load_workbook(LDM, read_only=True)
    ace = {}
    for r in wb["ACE mapping"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            ace[(r[1], r[2])] = r
    ids = {}
    for r in wb["Fields"].iter_rows(min_row=5, values_only=True):
        if r[0]:
            ids[(r[1], r[2])] = r[0]
    return ace, ids


def build_rows(old_rows):
    """old_rows: list of [Interface, Source field, Entity, Field, Data type, Physical type, Mandatory, Transformation, Owner]."""
    ace, ids = ldm_maps()
    out = []
    for iface, src, ent, fld, dt, pt, mand, trans, owner in old_rows:
        if iface == PLACEHOLDER:
            iface = "INT-35" if ent == "treatment" else "INT-36"
        if iface in OUTBOUND:
            fid = ids[(ent, fld)]
            tc, tier, rp = f"{ent}.{fld}", "Tier 4", OUT_READ.get(fid, "Workbench table")
        else:
            m = ace[(ent, fld)]
            fid, tc, rp = m[0], m[4], m[5]
            tier = {"ACE reuse": "Tier 1", "ACE new": "Tier 2"}[m[3]]
            trans = TRANSFORM.get(fid, trans)
        out.append([iface, src, tc, tier, rp, fid, dt, pt, mand, trans, owner])
    return out


def old_field_rows():
    wb = openpyxl.load_workbook(IFX)
    ws = wb["Field mapping"]
    return [list(r[:9]) for r in ws.iter_rows(min_row=5, max_row=ws.max_row, values_only=True) if r[0]]
