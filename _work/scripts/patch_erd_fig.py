import re, os

p = os.path.join(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14", r"_work\scripts\build_erd_v4.py")
s = open(p, encoding="utf-8").read()
start = s.index("# ---------- overview figure ----------")
end = s.index("# ---------- page ----------")
new = '''# ---------- overview figure ----------
HW = 1020
HH = 512
sv = []
sv.append('<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" font-family="Aptos, Segoe UI, Arial" role="img" aria-label="The ACE boundary: ACE tables and additions, 30 read-only views, the recovery schema">' % (HW, HH))
sv.append('<rect width="%d" height="%d" fill="var(--surface)"/>' % (HW, HH))
sv.append('<defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#604A7B"/></marker></defs>')


def wrap(text, width):
    out, line = [], ""
    for word in text.split():
        if not line:
            line = word
        elif len(line) + 1 + len(word) <= width:
            line += " " + word
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def panel(x, y, w, h, title, blocks, fill="#FFFFFF", stroke="#604A7B", dash=None):
    d = ' stroke-dasharray="6,4"' if dash else ""
    sv.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s"%s/>' % (x, y, w, h, fill, stroke, d))
    sv.append('<text x="%d" y="%d" font-size="12.5" font-weight="bold" fill="#4E297F">%s</text>' % (x + 10, y + 19, E(title)))
    yy = y + 38
    for kind, text in blocks:
        if kind == "gap":
            yy += 6
            continue
        if kind == "h":
            sv.append('<text x="%d" y="%d" font-size="11" font-weight="bold" fill="#1F1F1F">%s</text>' % (x + 10, yy, E(text)))
            yy += 15
            continue
        for ln in wrap(text, 46):
            sv.append('<text x="%d" y="%d" font-size="10.5" fill="#1F1F1F">%s</text>' % (x + 10, yy, E(ln)))
            yy += 14.2


sv.append('<text x="8" y="18" font-size="11" fill="#595959">ACE holds the data, the Workbench holds the case, and a read-only view joins them.</text>')
panel(8, 30, 300, 446, "ACE database (ACE team)", [
    ("p", "Owned by ACE. The Workbench never writes here and never holds a copy."),
    ("gap", ""),
    ("h", "Tier 1 - in ACE today (22 tables)"),
    ("p", "account, payment, customer, phone, email, address, ca_relation, aa_relation, collateral, asset, efs_action, efs_action_code, efs_assignment, bucket_log_snapshot, product, branch, bot_holiday, ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation, ai_recommended_plan, iam_user"),
    ("gap", ""),
    ("h", "Tier 2 - RWB-ACE-001 (14 tables)"),
    ("p", "ace_batch_run, valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product, credit_decision, esign_request, iam_group"),
    ("gap", ""),
    ("h", "12 new columns"),
    ("p", "account 7, customer 3, efs_action 2, exposed by CREATE OR REPLACE in V0003."),
], fill="#EEEAF6")

panel(336, 30, 306, 446, "recovery.v_ace_* (30 views)", [
    ("p", "Read only. One view per ACE object family. Owned by ace_view_owner."),
    ("gap", ""),
    ("h", "Section A - 16 views (V0002)"),
    ("p", "v_ace_account, v_ace_payment, v_ace_customer, v_ace_contact, v_ace_ca_relation, v_ace_aa_relation, v_ace_collateral, v_ace_asset, v_ace_efs_action, v_ace_efs_action_code, v_ace_efs_assignment, v_ace_bucket_log, v_ace_product, v_ace_branch, v_ace_holiday, v_ace_plan"),
    ("gap", ""),
    ("h", "Section B - 14 views (V0003)"),
    ("p", "v_ace_batch_status, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset, v_ace_npa_sale, v_ace_lawsuit, v_ace_hearing, v_ace_pod, v_ace_write_off, v_ace_score, v_ace_party_product, v_ace_credit_decision, v_ace_esign, v_ace_iam_group"),
], stroke="#8A76AD", dash="6,4")

panel(672, 30, 340, 446, "Recovery schema (Workbench)", [
    ("h", "Tier 3 - 4 extension tables, 1:1"),
    ("p", "party_ext, contact_point_ext, account_ext, valuation_ext. Keyed by the ACE business key; no copy of ACE data."),
    ("gap", ""),
    ("h", "Tier 4 - 88 Workbench tables"),
    ("p", "Case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags and agents."),
    ("gap", ""),
    ("h", "Links into ACE"),
    ("p", "account_key, person_key, asset_key, payment_code, contact_key, valuation_key."),
    ("gap", ""),
    ("h", "No foreign key into ACE"),
    ("p", "ACE cascades deletes on account, and a cascade would delete case history."),
])

sv.append('<line x1="310" y1="250" x2="332" y2="250" stroke="#604A7B" stroke-width="2" marker-end="url(#a)"/>')
sv.append('<line x1="644" y1="250" x2="666" y2="250" stroke="#604A7B" stroke-width="2" marker-end="url(#a)"/>')
sv.append('<path d="M 980 484 C 980 505, 120 505, 120 484" fill="none" stroke="#C0392B" stroke-width="1.5" stroke-dasharray="4,3"/>')
sv.append('<text x="550" y="507" font-size="10.5" fill="#C0392B" text-anchor="middle">no write, and no foreign key into ACE</text>')
sv.append('<text x="316" y="240" font-size="9.5" fill="#595959" text-anchor="middle">SELECT</text>')
sv.append('<text x="650" y="240" font-size="9.5" fill="#595959" text-anchor="middle">SELECT</text>')
sv.append('</svg>')
overview_svg = "".join(sv)

'''
s = s[:start] + new + s[end:]
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
