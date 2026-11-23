"""Style the appended sheets, apply the five declared cell changes and reorder. Edits the copy only."""
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "06 Data" / "Recovery Workbench Volume and Scale Forecast v4.xlsx"

HEAD_FILL = PatternFill("solid", fgColor="DCD3EB")
HEAD_FONT = Font(bold=True, size=10)
BODY = Font(size=10)
TITLE = Font(bold=True, size=16)
WRAP = Alignment(wrap_text=True, vertical="top")

# The five cells that change, with the v3 value asserted before it is replaced.
CHANGES = {
    ("Read path", "A2"): (
        "The Workbench reads ACE through recovery.v_ace_* views. It runs no inbound load, so the cost is the read "
        "concurrency below and the growth the 14 new ACE tables add.",
        "rwb-source-data (P1) reads ACE through the 30 read-only recovery.v_ace_* views; every other service asks P1, "
        "so the Workbench as a whole holds one view grant. It runs no inbound load, so the cost is the read "
        "concurrency below and the growth the 14 new ACE tables add."),
    ("Read path", "C15"): (
        "Outbound queue dispatch, lake refresh and case list reconciliation; none reads a source system.",
        "Case creation and allocation (JOB-02 and JOB-03, rwb-case), reconciliation (JOB-04, rwb-source-data) and the "
        "WIN notice file (JOB-10, rwb-comms with rwb-integration); each is a Temporal Schedule or an event-started "
        "workflow in its own service, and none reads a source system."),
    ("Read path", "C16"): (
        "data_product_load is the Workbench freshness stamp. It is sourced from ace_batch_run, read through "
        "v_ace_batch_status, which gives the ACE per-source business date.",
        "data_product_load is the rwb-source-data freshness stamp. It is sourced from ace_batch_run, read by "
        "rwb-source-data through v_ace_batch_status, which gives the ACE per-source business date; GET /freshness "
        "serves it and AceDataReady announces it to the other services."),
    ("Inputs", "G7"): (
        "Nothing in the Workbench: the accounts stay in ACE and are read through v_ace_account",
        "Nothing in the Workbench: the accounts stay in ACE and are read by rwb-source-data through v_ace_account"),
    ("Key", "C10"): (
        "A SELECT on a recovery.v_ace_* view by a screen or by the lake refresh",
        "A SELECT on one of the 30 recovery.v_ace_* views by rwb-source-data, on behalf of a screen or a workflow; no "
        "other service holds the grant"),
}


def apply_changes(wb):
    for (sheet, ref), (old, new) in CHANGES.items():
        cell = wb[sheet][ref]
        assert str(cell.value).strip() == old.strip(), f"{sheet}!{ref} is not the expected v3 value: {cell.value!r}"
        cell.value = new
        cell.font = BODY
        cell.alignment = WRAP
    print("changed", len(CHANGES), "cells")


def find(ws, text, col=1, start=1):
    for r in range(start, ws.max_row + 1):
        v = ws.cell(r, col).value
        if isinstance(v, str) and v.strip().startswith(text):
            return r
    raise SystemExit(f"{ws.title}: '{text}' not found")


def head_row(ws, row, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row, c)
        cell.font = HEAD_FONT
        cell.fill = HEAD_FILL
        cell.alignment = WRAP


def block(ws, title, header, widths=None, numcol=None):
    rt = find(ws, title)
    rh = find(ws, header[0], start=rt)
    ws.cell(rt, 1).font = Font(bold=True, size=12)
    head_row(ws, rh, len(header))
    if widths:
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
    r = rh + 1
    while r <= ws.max_row and ws.cell(r, 1).value not in (None, ""):
        if ws.cell(r, 1).value in ("Platform settings", "Totals and cross-checks", "Task queues",
                                   "Business-event topics"):
            break
        for c in range(1, len(header) + 1):
            cell = ws.cell(r, c)
            cell.font = BODY
            cell.alignment = WRAP
        if numcol:
            ws.cell(r, numcol).number_format = "#,##0"
        r += 1
    return rh, r - 1


def style_service_volumes(ws):
    ws.cell(1, 1).font = TITLE
    ws.cell(2, 1).font = BODY
    ws.cell(2, 1).alignment = Alignment(wrap_text=False, vertical="top")
    ws.cell(find(ws, "Totals and cross-checks"), 1).font = Font(bold=True, size=12)
    r0, r1 = block(ws, "Service volumes, 2027 (D-RCV-60)",
                   ["Code", "Service", "Wave", "Volume driver", "Monthly volume 2027", "Unit", "Basis",
                    "Kafka topic", "Task queue", "Consumers of its events"],
                   [7, 21, 7, 40, 15, 24, 46, 30, 17, 44], numcol=5)
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A{r0}:J{r1}"
    # the cross-check block sits in columns D to G so it can use the wide columns
    rh = find(ws, "Item", col=4)
    head_row(ws, rh, 7)
    for c in (1, 2, 3):
        ws.cell(rh, c).fill = PatternFill(fill_type=None)
    r = rh + 1
    while r <= ws.max_row and ws.cell(r, 4).value not in (None, ""):
        for c in range(4, 8):
            ws.cell(r, c).font = BODY
            ws.cell(r, c).alignment = WRAP
        ws.cell(r, 5).number_format = "#,##0"
        r += 1


def style_topics(ws):
    ws.cell(1, 1).font = TITLE
    ws.cell(2, 1).font = BODY
    for t in ("Business-event topics", "Task queues", "Platform settings"):
        ws.cell(find(ws, t), 1).font = Font(bold=True, size=12)
    for c, w in enumerate([30, 22, 24, 14, 14, 14, 14, 46, 20, 30], 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    block(ws, "Business-event topics",
          ["Topic", "Producer", "Events published", "Partitions", "Replication factor", "Retention",
           "Record key", "Consumer groups", "Retry", "Dead letter"])
    block(ws, "Task queues",
          ["Task queue", "Service", "Wave", "Workflows on the queue", "Activities",
           "Schedules and event-started work", "Scale note"])
    block(ws, "Platform settings", ["Item", "Value", "Note"])
    ws.freeze_panes = "A6"


def style_read_me(ws):
    ws.column_dimensions["A"].width = 138
    heads = {"Change log", "What changed in v4", "What did not change", "Sheets", "Open register rows", "Counts"}
    for r in range(1, ws.max_row + 1):
        c = ws.cell(r, 1)
        c.alignment = Alignment(wrap_text=False, vertical="top")
        if r == 4:
            c.font = Font(bold=True, size=14)
        elif isinstance(c.value, str) and c.value.strip() in heads:
            c.font = Font(bold=True, size=10)
        else:
            c.font = BODY
    ws.cell(9, 1).font = Font(bold=True, size=10)


def main():
    wb = openpyxl.load_workbook(OUT)
    apply_changes(wb)
    style_service_volumes(wb["Service volumes"])
    style_topics(wb["Topics and queues"])
    style_read_me(wb["Read me"])

    order = ["Read me", "Inputs", "Monthly", "Five years", "Users and load", "Read path",
             "Service volumes", "Topics and queues", "ACE growth", "Route activity", "Key"]
    wb._sheets = [wb[name] for name in order]
    p = wb.properties
    p.creator = "Recovery Workbench programme"
    p.lastModifiedBy = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    p.title = "Recovery Workbench Volume and Scale Forecast v4"
    p.subject = "D-RCV-60 microservice realignment"
    wb.active = 0
    wb.save(OUT)
    print("BUILT", OUT)
    print("sheets", wb.sheetnames)
    for name in wb.sheetnames:
        ws = wb[name]
        print(" ", name, ws.dimensions, "freeze", ws.freeze_panes, "filter", ws.auto_filter.ref)


if __name__ == "__main__":
    main()
