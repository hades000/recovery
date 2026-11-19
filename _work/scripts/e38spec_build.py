# Build Epics 3 to 8 Specification v3 (docx and xlsx) from v2. D-RCV-35 ACE alignment.
import zipfile, re, copy, os
from xml.sax.saxutils import escape
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications"
SRC_D = os.path.join(ROOT, "Recovery Workbench Epics 3 to 8 Specification v2.docx")
OUT_D = os.path.join(ROOT, "Recovery Workbench Epics 3 to 8 Specification v3.docx")
SRC_X = os.path.join(ROOT, "Recovery Workbench Epics 3 to 8 Specification v2.xlsx")
OUT_X = os.path.join(ROOT, "Recovery Workbench Epics 3 to 8 Specification v3.xlsx")

DATE = "15 November 2026"
CHANGE = ("Version 3, 15 November 2026 (D-RCV-35): the Workbench loads no source data. AMIS, RPS, GL, SVAF, "
          "COLLINS, LIT and WIN proof of delivery arrive through ACE ingestion (RWB-ACE-001) and are read through "
          "the read-only recovery.v_ace_* views. Integrations 2.4 to 5.4, the architecture data rows and 17 feature "
          "descriptions re-worded. Outbound interfaces unchanged.")

# Integrations: ID -> {column: (old, new)}  (Direction, Approach)
INT_EDITS = {
    "INT-03": {"Approach": ("Booked by the officer; confirmed on the next day's load",
                            "Booked by the officer; confirmed when the next ACE batch shows the booking in v_ace_account")},
    "INT-12": {"Direction": ("In", "In, into ACE"),
               "Approach": ("File load", "ACE ingestion, read through v_ace_npa_asset and v_ace_npa_sale")},
    "INT-13": {"Direction": ("In", "In, into ACE"),
               "Approach": ("File load", "ACE ingestion, read through v_ace_npa_asset")},
    "INT-16": {"Direction": ("In", "In, into ACE"),
               "Approach": ("File load", "ACE ingestion, read through v_ace_write_off")},
}

# Feature descriptions: ID -> (old, new, systems_old, systems_new or None)
FEAT = {
    "FEAT-TRT-11": ("Counts missed payments against the break rule and moves the case to the point the rule names.",
                    "Counts missed payments, read through v_ace_payment, against the break rule and moves the case to the point the rule names.",
                    None, None),
    "FEAT-AST-01": ("Creates the asset record from the repossession result and starts the holding clock.",
                    "Links the case to the repossessed vehicle in v_ace_npa_asset, which ACE ingests from RPS and AMIS, by asset_key and starts the holding clock.",
                    "RPS, AMIS", "ACE (ingested from RPS and AMIS)"),
    "FEAT-AST-02": ("Creates the asset record when a deed in lieu transfer completes.",
                    "Links the case to the property in v_ace_npa_asset, which ACE ingests from AMIS, by asset_key when a deed in lieu transfer completes.",
                    "AMIS, CCMS", "ACE (ingested from AMIS and CCMS)"),
    "FEAT-AST-03": ("Creates the asset record when the bank takes the property at the enforcement auction.",
                    "Links the case to the property in v_ace_npa_asset, which ACE ingests from AMIS, by asset_key when the bank takes the property at the enforcement auction.",
                    "AMIS, LED portal", "ACE (ingested from AMIS), LED portal"),
    "FEAT-AST-04": ("Sends the notice the repossession requires and records the proof.",
                    "Sends the notice the repossession requires and records the WIN proof of delivery read through v_ace_pod.",
                    "WIN", "WIN, ACE (ingested from WIN)"),
    "FEAT-VAL-02": ("Takes the value, date and appraiser back from SVAF onto the collateral record.",
                    "Reads the value, date and appraiser from v_ace_valuation once ACE has ingested the SVAF result, and links it to the collateral by business key.",
                    "SVAF", "ACE (ingested from SVAF)"),
    "FEAT-VAL-05": ("Asks the COLLINS model for the expected return on each route and records the answer with its version.",
                    "Reads the expected return on each route from v_ace_score, which ACE ingests from the COLLINS models, and records the answer with its model version.",
                    "COLLINS, Model gateway", "ACE (ingested from COLLINS), Model gateway"),
    "FEAT-VAL-06": ("Works out the payoff from ALS and the settlement range from the rules, with the floor applied.",
                    "Works out the payoff from the ALS balances read through v_ace_account and the settlement range from the rules, with the floor applied.",
                    None, None),
    "FEAT-COM-05": ("Keeps the verified contact points for every party, with consent state per channel.",
                    "Reads the contact points for every party from v_ace_contact and keeps verification and consent state per channel in contact_point_ext.",
                    "Workbench", "Workbench, ACE"),
    "FEAT-PAY-06": ("Writes the agreed settlement terms to ALS and reads the booked position back.",
                    "Writes the agreed settlement terms to ALS and reads the booked position back through v_ace_account after the next ACE batch.",
                    None, None),
    "FEAT-PAY-11": ("Compares what the Workbench matched to what ALS and the ledger show, every day.",
                    "Compares what the Workbench matched to the ALS position read through v_ace_payment and v_ace_account, and to the ledger, every day.",
                    None, None),
    "FEAT-LIT-02": ("Writes the delivery confirmation onto the case, which the notice period timer starts from.",
                    "Reads the WIN proof of delivery from v_ace_pod, which ACE ingests, and writes it onto the notice; the notice period timer starts from it.",
                    "WIN", "ACE (ingested from WIN)"),
    "FEAT-LIT-10": ("Takes the filing confirmation and the court case number from the firm onto the case.",
                    "Takes the filing confirmation and the court case number from the firm onto the case, and matches them to the LIT lawsuit read through v_ace_lawsuit.",
                    "Partner portal, LIT", "Partner portal, ACE (ingested from LIT)"),
    "FEAT-LIT-11": ("Follows the court calendar, raises each deadline and accrues the fees against the case.",
                    "Follows the court calendar from the LIT hearings read through v_ace_hearing and the firm's entries, raises each deadline and accrues the fees against the case.",
                    "LIT, Partner portal", "ACE (ingested from LIT), Partner portal"),
    "FEAT-LIT-16": ("Writes the judgment date and amount onto the case and opens the enforcement step.",
                    "Writes the judgment date and amount onto the case, from the firm or the LIT lawsuit read through v_ace_lawsuit, and opens the enforcement step.",
                    "LIT, Workbench", "ACE (ingested from LIT), Workbench"),
    "FEAT-DBS-02": ("Groups the accounts into lots and estimates the price from the COLLINS lot economics.",
                    "Groups the accounts into lots and estimates the price from the COLLINS lot economics read through v_ace_score.",
                    "COLLINS, Model gateway", "ACE (ingested from COLLINS), Model gateway"),
    "FEAT-WOF-11": ("Compares what the committee approved to what was posted, and raises every difference.",
                    "Compares what the committee approved to the GL postings read through v_ace_write_off, and raises every difference.",
                    None, None),
}

# Architecture data rows (docx only)
DATA_ROWS = [
    ("Entities used or extended: asset, asset_sale, listing, treatment",
     "Entities used or extended: asset_sale, listing, treatment. Source data read through v_ace_asset, v_ace_npa_asset and v_ace_npa_sale by asset_key (D-RCV-35)"),
    ("Entities used or extended: asset, asset_sale, guarantee_claim, listing, notice, proceeds, score, template, valuation",
     "Entities used or extended: asset_sale, contact_point_ext, guarantee_claim, listing, notice, proceeds, template, valuation_ext. Source data read through v_ace_valuation, v_ace_score, v_ace_asset, v_ace_npa_asset, v_ace_account, v_ace_payment and v_ace_contact (D-RCV-35)"),
    ("Entities used or extended: debt_sale_account, debt_sale_lot, hearing, legal_action",
     "Entities used or extended: debt_sale_account, debt_sale_lot, hearing, legal_action. Source data read through v_ace_lawsuit, v_ace_hearing, v_ace_pod, v_ace_account and v_ace_score (D-RCV-35)"),
    ("Entities used or extended: debt_sale_account, debt_sale_lot, partner, partner_instruction, proceeds, write_off",
     "Entities used or extended: debt_sale_account, debt_sale_lot, partner, partner_instruction, proceeds, write_off. Source data read through v_ace_write_off, v_ace_account and v_ace_payment (D-RCV-35)"),
]

# Notes after integration tables (docx only)
INT_NOTES = {
    "2.4 Integrations": "Inbound data arrives through ACE ingestion, not a Workbench load (D-RCV-35). AMIS and RPS land in the ACE tables npa_asset and npa_sale, raised in RWB-ACE-001, and the Workbench reads them through v_ace_npa_asset and v_ace_npa_sale. Outbound interfaces are unchanged.",
    "3.4 Integrations": "Inbound data this epic reads arrives through ACE ingestion, not a Workbench load (D-RCV-35): SVAF appraisals (INT-11) through v_ace_valuation, COLLINS route returns (INT-08) through v_ace_score, account and payment data through v_ace_account and v_ace_payment, and contact points through v_ace_contact. These interfaces are first used in earlier epics. Outbound interfaces are unchanged.",
    "4.4 Integrations": "Inbound data arrives through ACE ingestion, not a Workbench load (D-RCV-35): LIT lawsuits and hearings (INT-09) through v_ace_lawsuit and v_ace_hearing, and WIN proof of delivery (INT-15) through v_ace_pod. INT-33 stays partner entry through the portal. Outbound interfaces are unchanged.",
    "5.4 Integrations": "GL write-off postings land in the ACE table gl_write_off (RWB-ACE-001) and are read through v_ace_write_off (D-RCV-35); the Workbench loads no file. Outbound postings to ALS and the ledger are unchanged.",
}

XLSX_INT_NOTE = ("From the integration inventory. Inbound sources arrive through ACE ingestion and are read through the "
                 "read-only recovery.v_ace_* views (D-RCV-35); outbound interfaces are unchanged.")


def t(s):
    return ">" + escape(s, {"'": "&apos;"}) + "</w:t>"


def t_alt(s):
    return ">" + escape(s) + "</w:t>"


def rep1(x, old, new, where=""):
    for f in (t, t_alt):
        o = f(old)
        n = x.count(o)
        if n == 1:
            return x.replace(o, t_alt(new))
        if n > 1:
            raise SystemExit(f"ambiguous {where}: {old!r} x{n}")
    raise SystemExit(f"not found {where}: {old!r}")


def row_span(x, anchor):
    i = x.find(t_alt(anchor))
    assert i > 0, anchor
    s = x.rfind("<w:tr>", 0, i)
    s2 = x.rfind("<w:tr ", 0, i)
    s = max(s, s2)
    e = x.find("</w:tr>", i) + 7
    return s, e


def build_docx():
    zin = zipfile.ZipFile(SRC_D)
    x = zin.read("word/document.xml").decode("utf-8")

    # doc control
    x = x.replace(t_alt("SCB Collections and Recovery. Henka Group, 28 October 2026"),
                  t_alt("SCB Collections and Recovery. Henka Group, " + DATE), 1)
    s, e = row_span(x, "Version")
    vrow = x[s:e]
    x = x[:s] + vrow.replace(t_alt("1"), t_alt("3"), 1) + x[e:]
    s, e = row_span(x, "Date")
    x = x[:s] + x[s:e].replace(t_alt("28 October 2026"), t_alt(DATE), 1) + x[e:]
    assert "28 October 2026" not in x
    # add Decision and Change rows after the Prepared by row (clone the Version row)
    s, e = row_span(x, "Prepared by")
    new_rows = ""
    for k, v in (("Decision", "D-RCV-35"), ("Change", CHANGE)):
        r = vrow.replace(t_alt("Version"), t_alt(k), 1).replace(t_alt("1"), t_alt(v), 1)
        new_rows += r
    x = x[:e] + new_rows + x[e:]

    # integrations
    for iid, cols in INT_EDITS.items():
        s, e = row_span(x, iid)
        row = x[s:e]
        for col, (old, new) in cols.items():
            o = t(old) if t(old) in row else t_alt(old)
            assert row.count(o) == 1, (iid, old)
            row = row.replace(o, t_alt(new))
        x = x[:s] + row + x[e:]

    # features
    for fid, (old, new, _, _) in FEAT.items():
        x = rep1(x, old, new, fid)

    # data rows
    for old, new in DATA_ROWS:
        x = rep1(x, old, new, "data row")

    # notes after integration tables; clone body paragraph format
    i = x.find("Built in the recovery module")
    ps = x.rfind("<w:p>", 0, i)
    pe = x.find("</w:p>", i) + 6
    ptpl = x[ps:pe]
    body_txt = re.search(r'<w:t xml:space="preserve">([^<]*)</w:t>', ptpl).group(1)

    def para(text):
        return ptpl.replace(body_txt, escape(text), 1)

    for head, note in INT_NOTES.items():
        hi = x.find(t_alt(head))
        assert hi > 0, head
        te = x.find("</w:tbl>", hi) + len("</w:tbl>")
        nexthead = x.find("Integrations</w:t>", hi + 10)
        x = x[:te] + para(note) + x[te:]

    # change note after the section 1 intro paragraph
    anchor = "Stories are written one epic ahead of the build month and the design is signed in parallel with the epic before (DT05)."
    i = x.find(anchor)
    assert i > 0
    pe = x.find("</w:p>", i) + 6
    x = x[:pe] + para(CHANGE) + x[pe:]

    core = zin.read("docProps/core.xml").decode("utf-8")
    core = core.replace("Specification v2</dc:title>", "Specification v3</dc:title>")
    core = re.sub(r"(<dcterms:modified[^>]*>)[^<]*", r"\g<1>2026-11-15T00:00:00Z", core)

    with zipfile.ZipFile(OUT_D, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = x.encode("utf-8")
            elif item.filename == "docProps/core.xml":
                data = core.encode("utf-8")
            zout.writestr(item, data)


def build_xlsx():
    wb = openpyxl.load_workbook(SRC_X)
    ws = wb["Integrations"]
    hdr = {c.value: c.column for c in ws[4]}
    ws["A2"] = XLSX_INT_NOTE
    done = set()
    for r in range(5, ws.max_row + 1):
        iid = ws.cell(r, hdr["ID"]).value
        if iid in INT_EDITS:
            for col, (old, new) in INT_EDITS[iid].items():
                c = ws.cell(r, hdr[col])
                assert c.value == old, (iid, col, c.value)
                c.value = new
            done.add(iid)
    assert done == set(INT_EDITS), done

    ws = wb["Features"]
    hdr = {c.value: c.column for c in ws[4]}
    done = set()
    for r in range(5, ws.max_row + 1):
        fid = ws.cell(r, hdr["Feature"]).value
        if fid in FEAT:
            old, new, sold, snew = FEAT[fid]
            c = ws.cell(r, hdr["What it does"])
            assert c.value == old, (fid, c.value)
            c.value = new
            if snew:
                s = ws.cell(r, hdr["Systems"])
                assert s.value == sold, (fid, s.value)
                s.value = snew
            done.add(fid)
    assert done == set(FEAT), set(FEAT) - done

    # document control sheet, styled like the existing sheets
    src = wb["Integrations"]
    dc = wb.create_sheet("Document control")
    dc["A1"] = "Document control"
    dc["A1"].font = copy.copy(src["A1"].font)
    dc["A2"] = "Recovery Workbench Epics 3 to 8 Specification v3"
    dc["A2"].font = copy.copy(src["A2"].font)
    rows = [("Item", "Detail"),
            ("Document", "Recovery Workbench epics 3 to 8 at specification level"),
            ("Version", "3"),
            ("Date", DATE),
            ("Prepared by", "Henka Group"),
            ("Decision", "D-RCV-35"),
            ("Change", CHANGE)]
    for i, (k, v) in enumerate(rows):
        r = 4 + i
        for j, val in enumerate((k, v)):
            c = dc.cell(r, 1 + j, val)
            s = src["A4"] if i == 0 else src["B5"]
            c.font = copy.copy(s.font)
            c.fill = copy.copy(s.fill)
            c.border = copy.copy(s.border)
            c.alignment = Alignment(wrap_text=True, vertical="top")
    dc.column_dimensions["A"].width = 16
    dc.column_dimensions["B"].width = 100
    wb.properties.title = "Recovery Workbench Epics 3 to 8 Specification v3"
    wb.save(OUT_X)


if __name__ == "__main__":
    build_docx()
    build_xlsx()
    print("built")
