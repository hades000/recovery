"""Shared helpers for the W9-governance edit pass."""
import csv

SET = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
STAGE = SET + r'\_work\p1-ready\stage'
LOGFILE = SET + r'\_work\p1-ready\editlog\W9-governance.csv'
FIELDS = ['edit_id', 'action', 'file', 'old_version', 'new_version', 'section', 'before', 'after',
          'finding_refs', 'decision_refs', 'gap_asm_refs', 'model', 'agent']


def _trim(text):
    text = '' if text is None else str(text)
    return text if len(text) <= 400 else text[:399] + '…'


def log(action, file, old, new, section, before, after, findings='', decisions='', gaps=''):
    with open(LOGFILE, encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    number = max(int(r['edit_id'].rsplit('-', 1)[1]) for r in rows) + 1
    row = dict(zip(FIELDS, ['W9-governance-%04d' % number, action, file, old, new, section,
                            _trim(before), _trim(after), findings, decisions, gaps,
                            'Claude Sonnet 5.5', 'W9-governance']))
    with open(LOGFILE, 'a', encoding='utf-8', newline='') as fh:
        csv.DictWriter(fh, FIELDS, quoting=csv.QUOTE_ALL).writerow(row)
    return row['edit_id']
