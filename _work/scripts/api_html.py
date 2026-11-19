"""Render the Recovery Workbench API spec HTML from the YAML, using a previous HTML as the template.

usage: python api_html.py SPEC.yaml TEMPLATE.html OUT.html [meta-line]
The template supplies the static parts (styles, overview rules, errors, script). The endpoint,
schema and release tables, the overview counts, the schema filter options and the meta line
are regenerated from SPEC.yaml.
"""
import html
import re
import sys

import yaml

METHODS = ('get', 'post', 'put', 'patch', 'delete')


def esc(s):
    return html.escape(str(s), quote=True)


def td(v, cls=''):
    return '<td class="%s">%s</td>' % (cls, esc(v))


def type_of(p):
    if '$ref' in p:
        return ''
    t = p.get('type', '')
    if isinstance(t, list):
        t = ' or '.join(t)
    if 'enum' in p:
        vals = [str(v) for v in p['enum']]
        s = ', '.join(vals[:8]) + (' ...' if len(vals) > 8 else '')
        return '%s: %s' % (t, s)
    if t == 'array':
        it = p.get('items', {})
        if '$ref' in it:
            return 'array of ' + it['$ref'].split('/')[-1]
        return 'array'
    if 'format' in p:
        return '%s (%s)' % (t, p['format'])
    return t


def meaning(p):
    d = (p.get('description') or '').strip()
    return d


def endpoint_rows(spec):
    rows = []
    base = spec['servers'][0]['url'].rstrip('/')
    base = '/api/recovery/v1' if base.startswith('/api/recovery') else base
    for path, item in spec['paths'].items():
        for m, op in item.items():
            if m not in METHODS:
                continue
            tag = (op.get('tags') or [''])[0]
            cap = op.get('x-capability', {})
            access = ('%s %s' % (cap.get('area', ''), cap.get('right', ''))).strip()
            errs = ', '.join(c for c in op.get('responses', {}) if not str(c).startswith('2'))
            rows.append((tag, [m.upper(), base + path, op.get('summary', ''), tag, op.get('x-module', ''),
                               access, op.get('x-first-release', ''), errs]))
    return rows


def render_endpoints(rows):
    out = []
    for tag, cells in rows:
        cs = ''.join(td(c, 'code' if i == 1 else '') for i, c in enumerate(cells))
        out.append('<tr data-g="%s">%s</tr>' % (esc(tag), cs))
    return ''.join(out)


def render_schemas(spec):
    out = []
    for name, s in spec['components']['schemas'].items():
        req = set(s.get('required', []))
        for prop, p in (s.get('properties') or {}).items():
            cells = [td(name), td(prop, 'code'), td(type_of(p)), td('Yes' if prop in req else ''),
                     td('Yes' if p.get('x-personal-data') else ''), td(meaning(p))]
            out.append('<tr data-g="%s">%s</tr>' % (esc(name), ''.join(cells)))
    return ''.join(out)


def render_release(rows):
    from collections import Counter
    c = Counter(r[1][6] for r in rows)
    return ''.join('<tr>%s%s</tr>' % (td(k), td(c[k])) for k in sorted(c))


def build(spec, tpl, meta=None):
    s = tpl
    rows = endpoint_rows(spec)
    schemas = spec['components']['schemas']
    tbodies = list(re.finditer(r'<tbody>(.*?)</tbody>', s, flags=re.S))
    # tables: 0 rules, 1 endpoints, 2 schemas, 3 errors, 4 release
    new = {1: render_endpoints(rows), 2: render_schemas(spec), 4: render_release(rows)}
    parts, last = [], 0
    for i, m in enumerate(tbodies):
        parts.append(s[last:m.start(1)])
        parts.append(new.get(i, m.group(1)))
        last = m.end(1)
    parts.append(s[last:])
    s = ''.join(parts)
    s = re.sub(r'<b>\d+ endpoints</b>', '<b>%d endpoints</b>' % len(rows), s)
    s = re.sub(r'<b>\d+ schemas</b>', '<b>%d schemas</b>' % len(schemas), s)
    opts = '<option value="">All</option>' + ''.join(
        '<option value="%s">%s</option>' % (esc(n), esc(n)) for n in schemas)
    s = re.sub(r'(<select data-filtersel="t_sc"[^>]*>).*?(</select>)',
               lambda m: m.group(1) + opts + m.group(2), s, flags=re.S)
    if meta:
        s = re.sub(r'<div class="meta">.*?</div>', lambda m: '<div class="meta">%s</div>' % meta, s, count=1, flags=re.S)
    return s


if __name__ == '__main__':
    spec_p, tpl_p, out_p = sys.argv[1:4]
    meta = sys.argv[4] if len(sys.argv) > 4 else None
    spec = yaml.safe_load(open(spec_p, encoding='utf-8'))
    tpl = open(tpl_p, encoding='utf-8').read()
    out = build(spec, tpl, meta)
    with open(out_p, 'w', encoding='utf-8', newline='') as f:
        f.write(out)
    print('wrote', out_p, len(out))
