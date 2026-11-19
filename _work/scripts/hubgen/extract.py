"""Extract readable sections from every document type in the set."""
import io
import os
import re
import zipfile

import openpyxl
from bs4 import BeautifulSoup
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from pptx import Presentation


def clean(text):
    if text is None:
        return ''
    text = str(text).replace('\r\n', '\n').replace('\r', '\n')
    text = text.replace('\u00a0', ' ')
    text = text.replace('\ufffd', ' ')
    lines = [re.sub(r'[ \t]+', ' ', ln).rstrip() for ln in text.split('\n')]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return '\n'.join(lines)


def _flush(secs, cur):
    text = clean('\n'.join(cur['lines']))
    if not text and cur['h'] == 'Top':
        return
    if text or cur['h']:
        secs.append({'h': clean(cur['h']), 'l': cur['l'], 't': text})


def extract_md(path):
    raw = io.open(path, encoding='utf-8-sig', errors='replace').read()
    lines = raw.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    secs, cur = [], {'h': 'Top', 'l': 1, 'lines': []}
    fence = False
    for line in lines:
        if line.strip().startswith('```'):
            fence = not fence
        m = None if fence else re.match(r'^(#{1,6})\s+(.*\S)\s*$', line)
        if m:
            _flush(secs, cur)
            cur = {'h': m.group(2).strip(), 'l': len(m.group(1)), 'lines': []}
            continue
        cur['lines'].append(line)
    _flush(secs, cur)
    if not secs:
        secs = [{'h': 'Document', 'l': 1, 't': clean(raw)}]
    return secs


def _docx_blocks(document):
    body = document.element.body
    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            yield Paragraph(child, document)
        elif tag == 'tbl':
            yield Table(child, document)


def _docx_table(table):
    rows = []
    for row in table.rows:
        cells = []
        seen = set()
        for cell in row.cells:
            key = id(cell._tc)
            if key in seen:
                continue
            seen.add(key)
            cells.append(clean(cell.text).replace('\n', ' '))
        while cells and not cells[-1]:
            cells.pop()
        if any(cells):
            rows.append(' | '.join(cells))
    return rows


def extract_docx(path):
    document = Document(path)
    secs, cur = [], {'h': 'Top', 'l': 1, 'lines': []}
    for block in _docx_blocks(document):
        if isinstance(block, Paragraph):
            text = clean(block.text)
            style = (block.style.name if block.style is not None else '') or ''
            level = 0
            m = re.match(r'Heading (\d)', style)
            if m:
                level = int(m.group(1))
            elif style.lower() == 'title':
                level = 1
            if level and text:
                _flush(secs, cur)
                cur = {'h': text, 'l': level, 'lines': []}
            elif text:
                if cur['lines'] and cur['lines'][-1] and not cur['lines'][-1].startswith('|'):
                    cur['lines'].append('')
                cur['lines'].append(text)
        else:
            rows = _docx_table(block)
            if rows:
                if cur['lines'] and cur['lines'][-1]:
                    cur['lines'].append('')
                cur['lines'].extend(rows)
    _flush(secs, cur)
    return secs


def _cell(value):
    if value is None:
        return ''
    if hasattr(value, 'isoformat'):
        return value.isoformat()[:10]
    return clean(str(value)).replace('\n', ' ')


def extract_xlsx(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    secs = []
    for ws in wb.worksheets:
        lines, blank = [], 0
        for n, row in enumerate(ws.iter_rows(values_only=True)):
            if n > 60000:
                break
            cells = [_cell(v) for v in row]
            while cells and not cells[-1]:
                cells.pop()
            if not any(cells):
                blank += 1
                if blank > 100 and lines:
                    break
                continue
            blank = 0
            lines.append(' | '.join(cells))
        if lines:
            secs.append({'h': 'Tab ' + (ws.title or 'Sheet'), 'l': 2, 't': '\n'.join(lines)})
    wb.close()
    return secs


def _shape_lines(shape):
    out = []
    if getattr(shape, 'has_text_frame', False) and shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            text = clean(p.text)
            if text:
                out.append(text)
    if getattr(shape, 'has_table', False) and shape.has_table:
        for row in shape.table.rows:
            cells = [clean(c.text).replace('\n', ' ') for c in row.cells]
            while cells and not cells[-1]:
                cells.pop()
            if any(cells):
                out.append(' | '.join(cells))
    return out


def extract_pptx(path):
    deck = Presentation(path)
    secs = []
    for n, slide in enumerate(deck.slides, 1):
        title = ''
        if slide.shapes.title is not None:
            title = clean(slide.shapes.title.text).replace('\n', ' ')
        lines = []
        for shape in slide.shapes:
            lines.extend(_shape_lines(shape))
        if not title and lines:
            title = lines[0]
        if title and lines and lines[0] == title:
            lines = lines[1:]
        h = 'Slide %d' % n
        if title:
            h += '. ' + title
        secs.append({'h': h, 'l': 2, 't': '\n'.join(lines)})
    return secs


def _html_table(table):
    rows = []
    for tr in table.find_all('tr'):
        cells = []
        for cell in tr.find_all(['td', 'th'], recursive=False):
            cells.append(re.sub(r'\s+', ' ', cell.get_text(' ', strip=True)))
        if any(cells):
            rows.append(' | '.join(cells))
    return rows


def extract_html(path):
    raw = io.open(path, encoding='utf-8-sig', errors='replace').read()
    soup = BeautifulSoup(raw, 'lxml')
    for tag in soup(['script', 'style', 'noscript', 'svg', 'nav']):
        tag.decompose()
    body = soup.body or soup
    secs, cur = [], {'h': 'Top', 'l': 1, 'lines': []}

    def walk(node):
        nonlocal cur
        for child in getattr(node, 'children', []):
            name = getattr(child, 'name', None)
            if name is None:
                text = clean(str(child))
                if text:
                    cur['lines'].append(text)
                continue
            if name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                text = re.sub(r'\s+', ' ', child.get_text(' ', strip=True))
                if text:
                    _flush(secs, cur)
                    cur = {'h': text, 'l': int(name[1]), 'lines': []}
            elif name == 'table':
                rows = _html_table(child)
                if rows:
                    if cur['lines'] and cur['lines'][-1]:
                        cur['lines'].append('')
                    cur['lines'].extend(rows)
            elif name in ('p', 'li', 'pre', 'blockquote', 'dt', 'dd'):
                text = child.get_text('\n', strip=True) if name == 'pre' else \
                    re.sub(r'\s+', ' ', child.get_text(' ', strip=True))
                text = clean(text)
                if text:
                    cur['lines'].append(text)
            elif name in ('div', 'section', 'article', 'main', 'ul', 'ol', 'dl', 'body', 'html',
                          'header', 'footer', 'figure', 'figcaption'):
                if name in ('header', 'footer'):
                    continue
                walk(child)
            elif name == 'br':
                cur['lines'].append('')
            else:
                text = re.sub(r'\s+', ' ', child.get_text(' ', strip=True))
                if text:
                    cur['lines'].append(text)

    walk(body)
    _flush(secs, cur)
    return secs


def extract_text(path, heading):
    raw = io.open(path, encoding='utf-8-sig', errors='replace').read()
    return [{'h': heading, 'l': 1, 't': clean(raw)}]


def extract_file(path, ext):
    ext = ext.lower()
    if ext == '.md':
        return extract_md(path)
    if ext == '.docx':
        return extract_docx(path)
    if ext == '.xlsx':
        return extract_xlsx(path)
    if ext == '.pptx':
        return extract_pptx(path)
    if ext in ('.html', '.htm'):
        return extract_html(path)
    if ext == '.yaml' or ext == '.yml':
        return extract_text(path, 'Specification')
    if ext == '.sql':
        return extract_text(path, 'Schema')
    if ext == '.csv':
        return extract_text(path, 'Extract')
    if ext == '.txt':
        return extract_text(path, 'Document')
    if ext == '.pdf':
        return []
    if ext == '.zip':
        return []
    return []


def extract_zip_members(path, zip_name):
    docs = []
    with zipfile.ZipFile(path) as z:
        for info in sorted(z.infolist(), key=lambda i: i.filename):
            if info.is_dir():
                continue
            ext = os.path.splitext(info.filename)[1].lower()
            if ext not in ('.md', '.txt'):
                continue
            raw = z.read(info).decode('utf-8-sig', errors='replace')
            secs, cur = [], {'h': 'Top', 'l': 1, 'lines': []}
            fence = False
            for line in raw.replace('\r\n', '\n').split('\n'):
                if line.strip().startswith('```'):
                    fence = not fence
                m = None if fence else re.match(r'^(#{1,6})\s+(.*\S)\s*$', line)
                if m:
                    _flush(secs, cur)
                    cur = {'h': m.group(2).strip(), 'l': len(m.group(1)), 'lines': []}
                    continue
                cur['lines'].append(line)
            _flush(secs, cur)
            stem = os.path.splitext(os.path.basename(info.filename))[0]
            docs.append({
                'file': zip_name + ' / ' + os.path.basename(info.filename),
                'name': stem,
                'ext': ext[1:],
                'inzip': zip_name,
                'secs': secs,
            })
    return docs
