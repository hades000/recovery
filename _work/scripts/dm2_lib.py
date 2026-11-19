# -*- coding: utf-8 -*-
"""DM2 shared helpers: parse the Tier 2 probe DDL with PK, UK and FK markers."""
import io
import re
from collections import OrderedDict

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
PROBE = ROOT + r'\_work\sql\ace_tier2_probe.sql'
GAP = ROOT + r'\15 ACE DB Alignment\Recovery Workbench ACE Field Gap List v1.xlsx'
STTM = ROOT + r'\06 Data\Recovery Workbench Source to Target Mapping v4.xlsx'
STORY_MD = ROOT + r'\04 User stories\Recovery Workbench ACE Team Stories v1.md'
STORY_XLSX = ROOT + r'\04 User stories\Recovery Workbench ACE Team Stories v1.xlsx'
VIEWS = ROOT + r'\15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql'

TABLE_ORDER = ['ace_batch_run', 'valuation', 'collateral_detail', 'npa_asset', 'npa_sale', 'lawsuit',
               'hearing', 'pod_receipt', 'gl_write_off', 'collins_score', 'party_product',
               'credit_decision', 'esign_request', 'iam_group']
TABLE_SRC = {'ace_batch_run': 'All sources', 'valuation': 'SVAF', 'collateral_detail': 'CCMS',
             'npa_asset': 'AMIS, RPS', 'npa_sale': 'AMIS', 'lawsuit': 'LIT', 'hearing': 'LIT',
             'pod_receipt': 'WIN', 'gl_write_off': 'GL', 'collins_score': 'COLLINS',
             'party_product': 'SCBPDM', 'credit_decision': 'NLEADS', 'esign_request': 'EasyApp',
             'iam_group': 'Entra ID', 'account': 'ALS', 'customer': 'SCBPDM', 'efs_action': 'EFS'}
TABLE_VIEW = {'ace_batch_run': 'v_ace_batch_status', 'valuation': 'v_ace_valuation',
              'collateral_detail': 'v_ace_collateral_detail', 'npa_asset': 'v_ace_npa_asset',
              'npa_sale': 'v_ace_npa_sale', 'lawsuit': 'v_ace_lawsuit', 'hearing': 'v_ace_hearing',
              'pod_receipt': 'v_ace_pod', 'gl_write_off': 'v_ace_write_off', 'collins_score': 'v_ace_score',
              'party_product': 'v_ace_party_product', 'credit_decision': 'v_ace_credit_decision',
              'esign_request': 'v_ace_esign', 'iam_group': 'v_ace_iam_group',
              'account': 'v_ace_account', 'customer': 'v_ace_customer', 'efs_action': 'v_ace_efs_action'}
# frequency keyed on the source system as written in the gap list
FREQ = {'SCBPDM': 'Daily, end of day', 'Core bank (ALS)': 'Daily, end of day', 'ALS': 'Daily, end of day',
        'EFS': 'Daily, end of day', 'CCMS': 'Weekly', 'SVAF': 'Weekly', 'AMIS': 'Monthly', 'RPS': 'Weekly',
        'LIT': 'Daily, end of day', 'WIN': 'Weekly', 'GL': 'Monthly', 'COLLINS': 'Daily, end of day',
        'NLEADS': 'On decision', 'EasyApp': 'On request', 'Entra ID': 'On change'}
NOTE_EXTRA = {
    'credit_decision': 'New table. NLEADS credit result for a treatment.',
    'esign_request': 'New table. EasyApp signature reference and status; the signed file stays in the Workbench document hub.',
    'iam_group': 'New table. Entra ID group to Workbench role mapping. Business key (entra_group, role_code); iam_group_key is the Entra group object ID and repeats when one group maps to more than one role.',
}


def freq(source_system):
    return FREQ.get(source_system.split(' via ')[0], '')


def parse_probe():
    """Return (tables, alters). tables: OrderedDict name -> list of dict(col, type, nullable, key)."""
    probe = io.open(PROBE, encoding='utf-8').read()
    tables = OrderedDict()
    for m in re.finditer(r'CREATE TABLE public\.([a-z_]+) \((.*?)\n\);', probe, re.S):
        name, body = m.group(1), m.group(2)
        uks = [[c.strip() for c in u.split(',')] for u in re.findall(r'unique \(([^)]*)\)', body)]
        cols = []
        for line in body.split('\n'):
            line = line.strip().rstrip(',')
            if not line or line.lower().startswith('constraint'):
                continue
            parts = line.split()
            col, typ = parts[0], parts[1]
            keys = []
            pk = 'primary key' in line
            if pk:
                keys.append('PK')
            for u in uks:
                if col in u:
                    keys.append('UK' if len(u) == 1 else 'UK (%s)' % ', '.join(u))
            fk = re.search(r'references public\.([a-z_]+) \(([a-z_]+)\)', line)
            if fk:
                keys.append('FK %s.%s' % (fk.group(1), fk.group(2)))
            nullable = 'NO' if (pk or 'not null' in line) else 'YES'
            cols.append({'col': col, 'type': typ, 'nullable': nullable, 'key': '; '.join(keys),
                         'uks': uks})
        tables[name] = cols
    alters = [{'table': m.group(1), 'col': m.group(2), 'type': m.group(3), 'nullable': 'YES', 'key': ''}
              for m in re.finditer(r'ALTER TABLE public\.([a-z_]+)\s+ADD COLUMN ([a-z_]+) ([a-z0-9_(),]+);', probe)]
    return tables, alters


def business_key(tables, t):
    uks = tables[t][0]['uks'] if tables[t] else []
    return uks[0] if uks else []


def type_map():
    tables, alters = parse_probe()
    tm = {}
    for t, cols in tables.items():
        for c in cols:
            tm['%s.%s' % (t, c['col'])] = c['type']
    for a in alters:
        tm['%s.%s' % (a['table'], a['col'])] = a['type']
    return tm


def section_a_tables():
    s = io.open(VIEWS, encoding='utf-8').read()
    a = s[s.index('-- Section A - Tier 1'):s.index('-- Section B - Tier 2')]
    return sorted(set(re.findall(r'(?:FROM|JOIN)\s+public\.([a-z_0-9]+)', a)))
