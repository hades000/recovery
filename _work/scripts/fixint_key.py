"""Disposition v3 Key: tighten the 'Not applicable' meaning."""
import openpyxl, fixint_common as c
wb = openpyxl.load_workbook(c.DISP); ws = wb["Key"]
assert ws["B24"].value == "Not applicable"
ws["C24"].value = ("No source record for ACE to hold: a booking or submission the officer makes in the other system (INT-03, INT-26), "
                   "a Workbench reporting feed (INT-19, INT-20) or records entered by partners (INT-33)")
wb.save(c.DISP); print("ok")
