"""Build decisions, Thai glossary and the small per-story maps."""
import datetime
import io
import json
import os

import openpyxl

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
DATA = os.path.join(ROOT, '_work', 'data')
V15 = json.load(io.open(os.path.join(ROOT, '_work', 'scripts', 'v15_consts_dump.json'), encoding='utf-8'))


def fmt_date(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    if isinstance(value, datetime.date):
        return value.strftime('%d %B %Y'), value.isoformat()
    text = str(value or '').strip()
    return text, ''


def main():
    wb = openpyxl.load_workbook(os.path.join(ROOT, '01 Decisions and governance',
                                             'Recovery Workbench Decision Log v9.xlsx'),
                                data_only=True)
    ws = wb['Open decisions']
    rows = [[c.value for c in r] for r in ws.iter_rows(min_row=6)]
    open_dec = []
    for r in rows:
        if not r or not r[0]:
            continue
        by, iso = fmt_date(r[6])
        open_dec.append({
            'id': str(r[0]).strip(),
            'dec': str(r[1] or '').strip(),
            'q': str(r[2] or '').strip(),
            'opts': str(r[3] or '').strip(),
            'rec': str(r[4] or '').strip(),
            'owner': str(r[5] or '').strip(),
            'by': by,
            'iso': iso,
            'blocks': str(r[7] or '').strip(),
            'late': str(r[8] or '').strip(),
        })
    ws = wb['Decisions taken']
    rows = [[c.value for c in r] for r in ws.iter_rows(min_row=5)]
    taken = []
    for r in rows:
        if not r or not r[0]:
            continue
        by, iso = fmt_date(r[2])
        taken.append({
            'id': str(r[0]).strip(),
            'dec': str(r[1] or '').strip(),
            'by': by,
            'iso': iso,
            'who': str(r[3] or '').strip(),
            'means': str(r[4] or '').strip(),
        })
    dec = {'open': open_dec, 'taken': taken,
           'file': 'Recovery Workbench Decision Log v9.xlsx',
           'folder': '01 Decisions and governance'}

    terms = V15['TERMS']
    th = {}
    for t in terms.get('terms', []):
        if t.get('en') and t.get('th'):
            th[t['en'].lower()] = t['th']
    for p in terms.get('prefixes', []):
        if p.get('en') and p.get('th'):
            key = p['en'].rstrip('-').lower()
            if key:
                th.setdefault(key, p['th'])

    out = {'DEC': dec, 'TERMS': terms, 'TH': th, 'NOTES': {}, 'SIMPLE': {}}
    io.open(os.path.join(DATA, 'hub_misc.json'), 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, separators=(',', ':')))
    print('open', len(open_dec), 'taken', len(taken), 'terms', len(terms.get('terms', [])),
          'th', len(th))


if __name__ == '__main__':
    main()
