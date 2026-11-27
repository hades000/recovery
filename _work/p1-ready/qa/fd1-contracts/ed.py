"""Exact-match editor for the staged contract files, with an edit log (agent FD1-contracts)."""
import csv
import os
import re

import yaml

BS = chr(92)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STAGE = os.path.join(ROOT, 'stage')
LOG = os.path.join(ROOT, 'editlog', 'FD1-contracts.csv')
API = '05 Technical architecture/Recovery Workbench API Specification v7/'
AGENT = 'FD1-contracts'
MODEL = 'claude-sonnet-5-5'
HEAD = ['edit_id', 'action', 'file', 'old_version', 'new_version', 'section', 'before', 'after',
        'finding_refs', 'decision_refs', 'gap_asm_refs', 'model', 'agent']


def trim(s):
    s = s or ''
    return s if len(s) <= 400 else s[:399] + '…'


def log(action, file, section, before='', after='', d='', f='', g='', old='v6', new='v7'):
    exists = os.path.exists(LOG)
    n = 0
    if exists:
        with open(LOG, encoding='utf-8-sig', newline='') as h:
            n = sum(1 for _ in csv.DictReader(h))
    with open(LOG, 'a', encoding='utf-8', newline='') as h:
        w = csv.writer(h, quoting=csv.QUOTE_ALL)
        if not exists:
            w.writerow(HEAD)
        eid = '%s-%04d' % (AGENT, n + 1)
        w.writerow([eid, action, file.replace('/', BS), old, new, section, trim(before), trim(after),
                    f, d, g, MODEL, AGENT])
    return eid


class Doc:
    def __init__(self, rel):
        self.rel = rel
        self.path = os.path.join(STAGE, rel)
        raw = open(self.path, 'rb').read()
        self.eol = '\r\n' if b'\r\n' in raw else '\n'
        self.text = raw.decode('utf-8').replace('\r\n', '\n')
        self.pending = []

    def block(self, start):
        """Return (i, j) of the block that starts with the line `start` and ends before the next
        line indented the same or less."""
        m = re.search('^' + re.escape(start) + '$', self.text, re.M)
        assert m, 'block not found: %r in %s' % (start, self.rel)
        ind = len(start) - len(start.lstrip())
        end = re.compile('^ {0,%d}[^ \n]' % ind, re.M).search(self.text, m.end() + 1)
        return m.start(), end.start() if end else len(self.text)

    def sub(self, old, new, section, within=None, count=1, d='', f='', g='', action='EDIT', quiet=False):
        i, j = (0, len(self.text))
        if within:
            for key in ([within] if isinstance(within, str) else within):
                if key is not None:
                    a, b = self.block(key) if (i, j) == (0, len(self.text)) else self._inner(key, i, j)
                    i, j = a, b
        seg = self.text[i:j]
        found = seg.count(old)
        assert found == count, '%s: expected %d of %r, found %d (%s)' % (self.rel, count, old[:90], found, section)
        self.text = self.text[:i] + seg.replace(old, new) + self.text[j:]
        if not quiet:
            self.pending.append((action, section, old, new, d, f, g))

    def _inner(self, start, i, j):
        seg = self.text[i:j]
        m = re.search('^' + re.escape(start) + '$', seg, re.M)
        assert m, 'inner block not found: %r' % start
        ind = len(start) - len(start.lstrip())
        end = re.compile('^ {0,%d}[^ \n]' % ind, re.M).search(seg, m.end() + 1)
        return i + m.start(), i + (end.start() if end else len(seg))

    def insert_before(self, marker, new, section, d='', f='', g=''):
        assert self.text.count(marker) == 1, 'marker %r count %d' % (marker, self.text.count(marker))
        self.text = self.text.replace(marker, new + marker)
        self.pending.append(('ADD', section, '', new, d, f, g))

    def add_response(self, path_line, method_line, code, body, section, d='', f='', g=''):
        """Insert a response entry in code order inside one operation."""
        a, b = self.block(path_line)
        a, b = self._inner(method_line, a, b)
        a, b = self._inner('      responses:', a, b)
        seg = self.text[a:b]
        codes = [(int(m.group(1)), m.start()) for m in re.finditer(r"^        '(\d{3})':", seg, re.M)]
        assert int(code) not in [c for c, _ in codes], 'response %s exists: %s' % (code, section)
        pos = next((p for c, p in codes if c > int(code)), len(seg))
        seg = seg[:pos] + body + seg[pos:]
        self.text = self.text[:a] + seg + self.text[b:]
        self.pending.append(('ADD', section, '', body.strip(), d, f, g))

    def save(self):
        yaml.safe_load(self.text)
        with open(self.path, 'wb') as h:
            h.write(self.text.replace('\n', self.eol).encode('utf-8'))
        for action, section, old, new, d, f, g in self.pending:
            log(action, self.rel, section, old, new, d, f, g)
        n = len(self.pending)
        self.pending = []
        return n


def ref(code):
    return "        '%s':\n          $ref: '#/components/responses/E%s'\n" % (code, code)
