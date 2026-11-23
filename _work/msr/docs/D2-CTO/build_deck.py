"""Render the D2-CTO realignment slides into the copied v4 deck, in the deck's own visual style.

The source deck is never edited: the caller first copies it with compat/office_write.py copy.
This renderer reads _work/msr/docs/D2-CTO/slides.md (content of record) and appends the new
section, then moves it in front of the kept version 3 slides.

Why not compat/office_write.py pptx-append: that helper writes markdown table rows as literal
pipe text into the body placeholder. These slides are table- and diagram-led (WP D2-CTO), so the
same slides.md is rendered with table and diagram support instead. Reason logged in the edit log.
"""
import math
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

FONT = "Aptos"
PURPLE = RGBColor(0x4E, 0x29, 0x7F)
PURPLE_2 = RGBColor(0x98, 0x6E, 0xD0)
HEADER_FILL = RGBColor(0xDC, 0xD3, 0xEB)
DARK = RGBColor(0x20, 0x11, 0x35)
BAND = RGBColor(0x32, 0x1A, 0x52)
GREY = RGBColor(0x59, 0x59, 0x59)
LINE_GREY = RGBColor(0xC8, 0xC8, 0xC8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ORANGE = RGBColor(0xFF, 0x99, 0x00)
LAVENDER = RGBColor(0xB3, 0xA2, 0xC7)

WAVE_TINT = {
    0: RGBColor(0xEF, 0xEA, 0xF7),
    1: RGBColor(0xDC, 0xD3, 0xEB),
    2: RGBColor(0xCB, 0xBB, 0xE6),
    3: RGBColor(0xB6, 0x99, 0xDB),
    4: RGBColor(0x9C, 0x73, 0xD1),
}

WAVES = [
    (0, "platform", 0, [("PLT-TPL", "template and repositories"), ("PLT-LIB", "shared libraries"),
                        ("PLT-WF", "Temporal workflow kit"), ("PLT-DB", "ACE DB schemas and logins"),
                        ("PLT-EVT", "Kafka event platform"), ("PLT-EDGE", "edge and gateway"),
                        ("PLT-OBS", "observability")]),
    (1, "EP01", 9, [("P1", "rwb-source-data"), ("P2", "rwb-integration"), ("P3", "rwb-case"),
                    ("P4", "rwb-access"), ("P5", "rwb-document"), ("P6", "rwb-comms"),
                    ("P7", "rwb-decision"), ("P9", "rwb-reporting"), ("P10", "rwb-agent")]),
    (2, "EP02, EP03", 4, [("P8", "rwb-payment"), ("S2", "rwb-treatment"), ("S5", "rwb-asset"),
                          ("S8", "rwb-deviation")]),
    (3, "EP04, EP05", 4, [("S1", "rwb-valuation"), ("S3", "rwb-guarantee"), ("S4", "rwb-litigation"),
                          ("S6", "rwb-debtsale")]),
    (4, "EP06 to EP08", 2, [("S7", "rwb-writeoff"), ("S9", "rwb-partner")]),
]

DAY1 = [("1,034", "story slices in the split plan"), ("939", "ready on Day 1"),
        ("510", "parallel lanes, at most 4 deep"), ("5", "team types with Day-1 work")]


def _emu(v):
    return Emu(int(round(v * 914400)))


def _set_font(run, size, bold=False, color=DARK, name=FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = name
    run.font.color.rgb = color


def _textbox(slide, x, y, w, h, wrap=True):
    tb = slide.shapes.add_textbox(_emu(x), _emu(y), _emu(w), _emu(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = _emu(0.06)
    tf.margin_right = _emu(0.04)
    tf.margin_top = _emu(0.02)
    tf.margin_bottom = _emu(0.02)
    return tb


def _para(tf, first):
    return tf.paragraphs[0] if first else tf.add_paragraph()


def add_title(slide, text):
    tb = _textbox(slide, 0.62, 0.26, 12.1, 0.66)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.BOTTOM
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    _set_font(run, 24 if len(text) <= 62 else (21 if len(text) <= 80 else 19), True, PURPLE)
    return tb


def add_rule(slide):
    from pptx.enum.shapes import MSO_CONNECTOR
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, _emu(0.52), _emu(0.96), _emu(0.52 + 12.29), _emu(0.96))
    ln.line.color.rgb = RGBColor(0, 0, 0)
    ln.line.width = Emu(15875)


def add_page_number(slide, n):
    tb = _textbox(slide, 12.21, 6.93, 0.70, 0.35)
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = str(n)
    _set_font(r, 12, False, GREY)


def _cell_border(tc, color="C8C8C8", w=9525):
    tcPr = tc.get_or_add_tcPr()
    ns = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    for idx, tag in enumerate(("lnL", "lnR", "lnT", "lnB")):
        xml = f'<a:{tag} {ns} w="0"><a:noFill/></a:{tag}>' if tag != "lnB" else (
            f'<a:lnB {ns} w="{w}" cap="flat" cmpd="sng"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:prstDash val="solid"/></a:lnB>')
        from lxml import etree
        tcPr.insert(idx, etree.fromstring(xml))


def _fit_columns(rows, widths):
    if widths:
        return widths
    ncols = max(len(r) for r in rows)
    weight = []
    for c in range(ncols):
        longest = max((len(r[c]) if c < len(r) else 0) for r in rows)
        weight.append(min(max(longest, 6), 90))
    total = sum(weight)
    return [max(0.75, 12.1 * w / total) for w in weight]


def _table_style(table):
    from lxml import etree
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for el in tblPr.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}tableStyleId"):
        tblPr.remove(el)
    ns = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    tblPr.append(etree.fromstring(
        f'<a:tableStyleId {ns}>{{5940675A-B579-460E-94D1-54222C63F5DA}}</a:tableStyleId>'))


def add_table(slide, rows, widths, top):
    ncols = max(len(r) for r in rows)
    rows = [list(r) + [""] * (ncols - len(r)) for r in rows]
    body = max(sum(len(str(c)) for c in r) for r in rows[1:]) if len(rows) > 1 else 10
    size = 14 if ncols == 2 else (13 if ncols == 3 else (12 if ncols == 4 else 12))
    if body > 900:
        size -= 1
    widths = _fit_columns(rows, widths)
    scale = 12.1 / sum(widths)
    widths = [w * scale for w in widths]

    def lines(text, w):
        cpl = max(6, int((w - 0.16) / (size * 0.0075)))
        return max(1, math.ceil(len(str(text)) * 1.06 / cpl))

    heights = []
    for r in rows:
        need = max(lines(c, widths[i]) for i, c in enumerate(r))
        heights.append(max(0.26, need * size * 1.28 / 72 + 0.10))

    shape = slide.shapes.add_table(len(rows), ncols, _emu(0.62), _emu(top), _emu(12.1), _emu(sum(heights)))
    table = shape.table
    _table_style(table)
    for i, w in enumerate(widths):
        table.columns[i].width = _emu(w)
    for i, h in enumerate(heights):
        table.rows[i].height = _emu(h)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.margin_left = Emu(72000)
            cell.margin_right = Emu(54000)
            cell.margin_top = Emu(36000)
            cell.margin_bottom = Emu(36000)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            cell.fill.solid()
            cell.fill.fore_color.rgb = HEADER_FILL if r == 0 else WHITE
            _cell_border(cell._tc)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            run = p.add_run()
            run.text = str(val)
            if r == 0:
                _set_font(run, size, True, PURPLE)
            else:
                _set_font(run, size, c == 0, RGBColor(0, 0, 0))
    return top + sum(heights)


def _est(text, size, width=12.1, bullet=False):
    cpl = max(8, int((width - 0.30) / (size * 0.0075)))
    prefix = 3 if bullet else 0
    return max(1, math.ceil((len(text) + prefix) * 1.06 / cpl))


def add_lines(slide, lines, top, size=11, color=DARK, bullet=True, italic=False):
    total = sum(_est(l, size, 12.1, bullet) for l in lines)
    h = total * size * 1.34 / 72 + 0.06 * len(lines)
    tb = _textbox(slide, 0.62, top, 12.1, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = _para(tf, i == 0)
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = ("\u2022  " if bullet else "") + line
        _set_font(r, size, False, color)
        if italic:
            r.font.italic = True
    return top + h + 0.06


def add_caption(slide, text, top):
    size = 10
    h = _est(text, size) * size * 1.34 / 72 + 0.10
    tb = _textbox(slide, 0.62, top, 12.1, h)
    tb.text_frame.word_wrap = True
    p = tb.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = text
    _set_font(r, size, False, GREY)
    r.font.italic = True
    return top + h + 0.06


def diagram_waves(slide, top):
    bottom = 6.88
    n = len(WAVES)
    gap = 0.10
    band_h = min(0.98, (bottom - top - gap * (n - 1)) / n)
    for k, (wave, epics, count, items) in enumerate(WAVES):
        y = top + k * (band_h + gap)
        band = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, _emu(0.62), _emu(y), _emu(12.09), _emu(band_h))
        band.fill.solid()
        band.fill.fore_color.rgb = WAVE_TINT[wave]
        band.line.fill.background()
        band.shadow.inherit = False
        tf = band.text_frame
        tf.text = ""

        lab = _textbox(slide, 0.70, y + 0.06, 1.45, band_h - 0.10)
        ltf = lab.text_frame
        p = ltf.paragraphs[0]
        r = p.add_run()
        r.text = f"Wave {wave}"
        _set_font(r, 13, True, PURPLE)
        p2 = ltf.add_paragraph()
        r2 = p2.add_run()
        r2.text = ("platform and NF" if wave == 0 else f"{count} services")
        _set_font(r2, 9, False, GREY)
        p3 = ltf.add_paragraph()
        r3 = p3.add_run()
        r3.text = epics if wave else "7 platform epics"
        _set_font(r3, 8, False, GREY)

        x = 2.22
        avail = 12.71 - x
        n_items = len(items)
        chip_w = (avail - 0.07 * (n_items - 1)) / n_items
        for j, (code, name) in enumerate(items):
            cx = x + j * (chip_w + 0.07)
            chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, _emu(cx), _emu(y + 0.09),
                                          _emu(chip_w), _emu(band_h - 0.18))
            chip.fill.solid()
            chip.fill.fore_color.rgb = WHITE
            chip.line.color.rgb = PURPLE_2
            chip.line.width = Pt(0.75)
            chip.shadow.inherit = False
            ctf = chip.text_frame
            ctf.word_wrap = True
            ctf.margin_left = Emu(36000)
            ctf.margin_right = Emu(36000)
            ctf.margin_top = Emu(18000)
            ctf.margin_bottom = Emu(18000)
            cp = ctf.paragraphs[0]
            cp.alignment = PP_ALIGN.CENTER
            cr = cp.add_run()
            cr.text = code
            _set_font(cr, 10 if wave else 9, True, PURPLE)
            if chip_w > 1.0:
                cp2 = ctf.add_paragraph()
                cp2.alignment = PP_ALIGN.CENTER
                cr2 = cp2.add_run()
                cr2.text = name
                _set_font(cr2, 7.5, False, RGBColor(0x40, 0x40, 0x40))
    return top + n * band_h + (n - 1) * gap + 0.10


def diagram_day1(slide, top):
    h = 1.30
    gap = 0.30
    w = (12.09 - 3 * gap) / 4
    for i, (number, label) in enumerate(DAY1):
        x = 0.62 + i * (w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, _emu(x), _emu(top), _emu(w), _emu(h))
        card.fill.solid()
        card.fill.fore_color.rgb = HEADER_FILL
        card.line.fill.background()
        card.shadow.inherit = False
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = number
        _set_font(r, 30, True, PURPLE)
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = label
        _set_font(r2, 9.5, False, GREY)
    return top + h + 0.16


def add_cover(prs, meta, logo):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, _emu(4.6), _emu(13.33), _emu(2.9))
    band.fill.solid()
    band.fill.fore_color.rgb = BAND
    band.line.fill.background()
    band.shadow.inherit = False

    tb = _textbox(slide, 0.62, 1.55, 11.6, 2.9)
    tf = tb.text_frame
    tf.word_wrap = True
    spec = [("h1", 13, True, ORANGE), ("h2", 10, False, LAVENDER), (None, 6, False, LAVENDER),
            ("title", 34, True, WHITE), ("sub", 17, False, WHITE), (None, 4, False, LAVENDER),
            ("meta", 14, False, LAVENDER)]
    first = True
    for key, size, bold, color in spec:
        p = _para(tf, first)
        first = False
        if key is None:
            continue
        r = p.add_run()
        r.text = meta.get(key, "")
        _set_font(r, size, bold, color)

    ft = _textbox(slide, 0.62, 5.90, 11.6, 1.0)
    ftf = ft.text_frame
    ftf.word_wrap = True
    p = ftf.paragraphs[0]
    r = p.add_run()
    r.text = "Change log: " + meta.get("change", "")
    _set_font(r, 10.5, False, LAVENDER)
    p2 = ftf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "Release dates are kept as issued and are tentative (R1 U7, DL48)."
    _set_font(r2, 10.5, False, LAVENDER)

    # brand marks last, so the two header lines are the first text of the deck (R8.1)
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, _emu(0.62), _emu(0.50), _emu(0.95), _emu(0.95))
    badge.fill.solid()
    badge.fill.fore_color.rgb = BAND
    badge.line.color.rgb = PURPLE_2
    badge.line.width = Pt(1.25)
    badge.shadow.inherit = False
    btf = badge.text_frame
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    br = bp.add_run()
    br.text = "SCB"
    _set_font(br, 14, True, WHITE)
    if logo is not None:
        slide.shapes.add_picture(str(logo), _emu(11.0), _emu(0.62), _emu(1.7), _emu(0.71))
    return slide


def parse(path):
    blocks, cur = [], None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            cur = {"title": line[3:].strip(), "blocks": []}
            blocks.append(cur)
            continue
        if cur is None:
            continue
        if not line.strip():
            continue
        cur["blocks"].append(line)
    return blocks


def parse_widths(line):
    return [float(x) for x in line.split()[1].split(",")]


def render(deck, md, logo):
    prs = Presentation(deck)
    existing = len(prs.slides)
    meta = {}
    added = 0
    for blk in parse(md):
        directives = [b for b in blk["blocks"] if b.startswith("@cover")]
        if directives:
            for b in blk["blocks"]:
                if "|" in b and not b.startswith("|"):
                    k, v = b.split("|", 1)
                    meta[k.strip()] = v.strip()
            add_cover(prs, meta, logo)
            added += 1
            continue

        slide = prs.slides.add_slide(prs.slide_layouts[6])
        added += 1
        add_title(slide, blk["title"])
        add_rule(slide)
        cur_y = 1.12
        widths = None
        i = 0
        body = blk["blocks"]
        while i < len(body):
            line = body[i]
            if line.startswith("@widths"):
                widths = parse_widths(line)
                i += 1
                continue
            if line.startswith("@diagram"):
                kind = line.split()[1]
                cur_y = diagram_waves(slide, cur_y) if kind == "waves" else diagram_day1(slide, cur_y)
                i += 1
                continue
            if line.startswith("@y"):
                cur_y = float(line.split()[1])
                i += 1
                continue
            if line.startswith("|"):
                rows = []
                while i < len(body) and body[i].startswith("|"):
                    cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body[i].strip().strip("|"))]
                    if not all(set(c) <= set("-: ") for c in cells):
                        rows.append(cells)
                    i += 1
                cur_y = add_table(slide, rows, widths, cur_y) + 0.14
                widths = None
                continue
            if line.startswith(">"):
                cur_y = add_caption(slide, line[1:].strip(), cur_y) + 0.06
                i += 1
                continue
            if line.startswith("- "):
                lines = []
                while i < len(body) and body[i].startswith("- "):
                    lines.append(body[i][2:].strip())
                    i += 1
                cur_y = add_lines(slide, lines, cur_y) + 0.06
                continue
            i += 1

    # page numbers for the new section, in build order (the cover carries none)
    new = list(prs.slides)[existing:]
    for n, slide in enumerate(new, 1):
        if n > 1:
            add_page_number(slide, n)

    # move the new section in front of the kept version 3 slides
    sldIdLst = prs.slides._sldIdLst
    ids = list(sldIdLst)
    for el in ids[existing:]:
        sldIdLst.remove(el)
    for k, el in enumerate(ids[existing:]):
        sldIdLst.insert(k, el)

    # the kept slides keep every word; only the footer number follows its new position
    for n, slide in enumerate(list(prs.slides)[added:], added + 1):
        for sh in slide.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip().isdigit():
                sh.text_frame.paragraphs[0].runs[0].text = str(n)

    prs.save(deck)
    print("WROTE", deck, "slides", len(prs.slides), "(kept", existing, "+ new", added, ")")


if __name__ == "__main__":
    deck, md = sys.argv[1], sys.argv[2]
    logo = sys.argv[3] if len(sys.argv) > 3 else None
    render(deck, md, logo)
