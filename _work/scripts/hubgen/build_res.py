"""Build the structured resources the hub uses for tables, columns, endpoints and lists."""
import io
import json
import os
import re

import yaml

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
DATA = os.path.join(ROOT, '_work', 'data')
V15 = json.load(io.open(os.path.join(ROOT, '_work', 'scripts', 'v15_consts_dump.json'), encoding='utf-8'))

STANDARD = {'version', 'state', 'updated_at', 'is_active', 'updated_by', 'created_by', 'created_at'}


def load(name):
    text = io.open(os.path.join(DATA, 'schema_' + name + '.json'), encoding='utf-8').read()
    start, end = text.find('['), text.rfind(']')
    return json.loads(text[start:end + 1])


def fmt_type(row):
    t = row['data_type']
    if t == 'character varying':
        return 'varchar(%s)' % row['character_maximum_length']
    if t == 'character':
        return 'char(%s)' % row['character_maximum_length']
    if t == 'numeric':
        if row['numeric_precision']:
            return 'numeric(%s,%s)' % (row['numeric_precision'], row['numeric_scale'] or 0)
        return 'numeric'
    if t == 'timestamp with time zone':
        return 'timestamptz'
    if t == 'timestamp without time zone':
        return 'timestamp'
    if t == 'USER-DEFINED':
        return row['udt_name']
    if t == 'ARRAY':
        return row['udt_name'] + '[]'
    return t


def main():
    objects = load('objects')
    columns = load('columns')
    fks = load('fks') or []
    indexes = load('indexes') or []
    triggers = load('triggers') or []
    sysobj = {r['object_name']: r for r in load('sysobjects')}
    sysfields = {}
    for r in load('sysfields'):
        sysfields.setdefault(r['object_name'], {})[r['field_name']] = r
    products = load('products')

    obj_by_name = {o['name']: o for o in objects}
    cols_by_obj = {}
    for c in sorted(columns, key=lambda x: (x['table_name'], x['ordinal_position'])):
        cols_by_obj.setdefault(c['table_name'], []).append(c)

    pk = {}
    for ix in indexes:
        if ix['indexdef'].startswith('CREATE UNIQUE INDEX') and ix['indexname'].endswith('_pkey'):
            m = re.search(r'\((.*)\)', ix['indexdef'])
            if m:
                pk[ix['tablename']] = [x.strip().strip('"') for x in m.group(1).split(',')]

    fks_by = {}
    for f in fks:
        fks_by.setdefault(f['table_name'], []).append({
            'col': f['column_name'], 'to': f['ref_table'], 'tocol': f['ref_column']})

    idx_by = {}
    for ix in indexes:
        if ix['indexname'].endswith('_pkey'):
            continue
        m = re.search(r'\((.*)\)', ix['indexdef'])
        cols = [x.strip().strip('"') for x in m.group(1).split(',')] if m else []
        idx_by.setdefault(ix['tablename'], []).append({
            'cols': ', '.join(cols), 'uniq': 'UNIQUE INDEX' in ix['indexdef']})

    trig_by = {}
    for t in triggers:
        trig_by.setdefault(t['table_name'], []).append({
            'name': t['trigger_name'], 'when': t['action_timing'] + ' ' + t['event_manipulation']})

    tables = {}
    for name, obj in obj_by_name.items():
        fields = sysfields.get(name, {})
        cols = []
        for c in cols_by_obj.get(name, []):
            desc = c.get('comment') or ''
            if not desc and c['column_name'] in fields:
                desc = fields[c['column_name']].get('description') or ''
            typ = fmt_type(c)
            if c['is_nullable'] == 'NO':
                typ += ' NOT NULL'
            if c['column_name'] in pk.get(name, []):
                typ += ' PRIMARY KEY'
            cols.append({'n': c['column_name'], 't': typ, 'c': desc})
        comment = obj.get('comment') or (sysobj.get(name, {}) or {}).get('description') or ''
        tables[name] = {
            'comment': comment,
            'cols': cols,
            'fks': fks_by.get(name, []),
            'idx': idx_by.get(name, []),
            'trig': trig_by.get(name, []),
        }

    colmap = {}
    for name, t in tables.items():
        for c in t['cols']:
            key = c['n']
            if key not in colmap:
                colmap[key] = {'in': [], 'type': c['t'], 'c': c['c'], 'std': key in STANDARD}
            colmap[key]['in'].append(name)
            if len(c['c'] or '') > len(colmap[key]['c'] or ''):
                colmap[key]['c'] = c['c']
    for v in colmap.values():
        v['in'].sort()

    prod_items = [{'n': p['product_code'] + ' ' + p['product_name'],
                   'c': p['system_of_record'] + ' | ' + p['refresh_cycle']} for p in products]
    fk_items = [{'n': f['table_name'] + '.' + f['column_name'],
                 'c': 'must exist in ' + f['ref_table'] + '.' + f['ref_column']} for f in fks]
    idx_items = [{'n': i['indexname'], 'c': i['indexdef']} for i in indexes]
    trig_items = [{'n': t['trigger_name'], 'c': t['table_name'] + ' | ' + t['action_timing'] + ' ' + t['event_manipulation']}
                  for t in triggers]
    table_items = [{'n': n, 'c': t['comment']} for n, t in sorted(tables.items())
                   if obj_by_name[n]['kind'] == 'table']
    view_items = [{'n': n, 'c': t['comment']} for n, t in sorted(tables.items())
                  if obj_by_name[n]['kind'] == 'view' and n.startswith('v_ace_')]
    obj_items = [{'n': o['object_name'], 'c': o.get('description') or o.get('business_name') or ''}
                 for o in load('sysobjects')]
    field_items = []
    for r in load('sysfields'):
        field_items.append({'n': r['object_name'] + '.' + r['field_name'],
                            'c': (r.get('description') or r.get('data_type') or '')})
    field_items.sort(key=lambda x: x['n'])

    sets = {
        'tables92': {
            'src': 'Physical Schema v5',
            'title': 'The 92 tables in the recovery schema',
            'note': 'The 88 Workbench tables plus the four extension tables keyed by an ACE business key. The 30 read-only ACE views are listed separately.',
            'items': table_items},
        'views30': {
            'src': 'ACE Source Views v1',
            'title': 'The 30 read-only ACE views',
            'note': 'Sixteen Section A views over the ACE tables that exist now, and fourteen Section B views that arrive with RWB-ACE-001. The recovery module reads source data only through these views.',
            'items': view_items},
        'objects122': {
            'src': 'Physical Schema v5',
            'title': 'The 122 objects in the data dictionary',
            'note': '92 tables and 30 views. Each row is a sys_objects row in the dictionary.',
            'items': obj_items},
        'fields1366': {
            'src': 'Physical Schema v5',
            'title': 'The 1,366 fields in the data dictionary',
            'note': 'Every column of the 92 tables and every column of the 30 views, held as sys_fields rows.',
            'items': field_items},
        'products14': {
            'src': 'Physical Schema v5',
            'title': 'The 14 data products',
            'note': 'One system of record and one owner role per product.',
            'items': prod_items},
        'standard7': {
            'src': 'Physical Schema v5',
            'title': 'The seven standard columns',
            'note': 'Every Workbench entity carries these seven columns; the data dictionary check ignores them when it compares tables with sys_fields.',
            'items': [{'n': n, 'c': 'Standard column'} for n in
                      ['id', 'version', 'state', 'is_active', 'created_at', 'created_by', 'updated_at']]},
        'fk': {'src': 'Physical Schema v5', 'title': 'Foreign keys inside the recovery schema',
               'note': 'No foreign key points into public: ACE rows are held by business key.', 'items': fk_items},
        'idx': {'src': 'Physical Schema v5', 'title': 'Indexes in the recovery schema', 'note': '', 'items': idx_items},
        'trig': {'src': 'Physical Schema v5', 'title': 'Triggers in the recovery schema', 'note': '', 'items': trig_items},
    }

    api = yaml.safe_load(io.open(os.path.join(ROOT, '05 Technical architecture',
                                              'Recovery Workbench API Specification v3.yaml'),
                                 encoding='utf-8'))
    endpoints = {}
    for path, item in api['paths'].items():
        for method, op in item.items():
            if method.lower() not in ('get', 'post', 'put', 'patch', 'delete', 'head', 'options'):
                continue
            full = '/api/recovery/v1' + path
            cap = op.get('x-capability') or {}
            perm = ((cap.get('area') or '') + ' ' + (cap.get('right') or '')).strip()
            codes = ', '.join(k for k in (op.get('responses') or {}) if not k.startswith('2'))
            endpoints[method.upper() + ' ' + full] = {
                'method': method.upper(), 'path': full,
                'desc': op.get('summary') or '',
                'group': (op.get('tags') or [''])[0],
                'module': op.get('x-module') or '',
                'perm': perm,
                'epic': op.get('x-first-release') or '',
                'codes': codes,
            }

    res = {
        'tables': tables,
        'sets': sets,
        'endpoints': endpoints,
        'columns': colmap,
        'concepts': V15['RES']['concepts'],
        'actors': V15['RES']['actors'],
    }
    io.open(os.path.join(DATA, 'hub_res.json'), 'w', encoding='utf-8').write(
        json.dumps(res, ensure_ascii=False, separators=(',', ':')))
    print('tables', len(tables), 'columns', len(colmap), 'endpoints', len(endpoints),
          'sets', list(sets), 'set items', {k: len(v['items']) for k, v in sets.items()})


if __name__ == '__main__':
    main()
