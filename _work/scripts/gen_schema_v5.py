# -*- coding: utf-8 -*-
"""Build Physical Schema v5 from v4 plus the frozen ACE alignment."""
import io
import re
import csv

SRC = r'06 Data\Recovery Workbench Physical Schema v4.sql'
OUT = r'06 Data\Recovery Workbench Physical Schema v5.sql'
VIEWS = r'15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql'

REMOVED = ['loan_account', 'account_payment', 'party', 'contact_point', 'collateral',
           'account_collateral', 'collections_history', 'party_product', 'valuation', 'score',
           'asset', 'load_run', 'dq_exception', 'dq_rule', 'source_field_map', 'source_code_map',
           'interface_run', 'interface_signoff', 'tracker_inventory', 'tracker_row']

# table, old column, new column, new type, extra column (for interaction), extra type
REKEY = [
    ('recovery_case', 'primary_customer_id', 'primary_person_key', 'varchar(255)', None, None),
    ('case_account', 'account_id', 'account_key', 'varchar(255)', None, None),
    ('case_party', 'party_id', 'person_key', 'varchar(255)', None, None),
    ('notice', 'party_id', 'person_key', 'varchar(255)', None, None),
    ('listing', 'asset_id', 'asset_key', 'varchar(255)', None, None),
    ('asset_sale', 'asset_id', 'asset_key', 'varchar(255)', None, None),
    ('debt_sale_account', 'account_id', 'account_key', 'varchar(255)', None, None),
    ('interaction', 'party_id', 'person_key', 'varchar(255)', None, None),
    ('interaction', 'contact_point_id', 'contact_key', 'varchar(255)', None, None),
    ('document', 'party_id', 'person_key', 'varchar(255)', None, None),
    ('proceeds', 'account_payment_id', 'payment_code', 'varchar(255)', None, None),
    ('case_list_row', 'account_id', 'account_key', 'varchar(255)', None, None),
    ('case_entry_exclusion', 'account_id', 'account_key', 'varchar(255)', None, None),
    ('signature_request', 'party_id', 'person_key', 'varchar(255)', None, None),
]

EXT_DDL = """
-- Party extension: Workbench flags about an ACE customer, keyed by person_key.
CREATE TABLE party_ext (
    person_key varchar(255) PRIMARY KEY,
    vulnerable boolean NOT NULL DEFAULT false,
    deceased_override boolean NOT NULL DEFAULT false,
    bankruptcy boolean NOT NULL DEFAULT false,
    fraud_flag boolean NOT NULL DEFAULT false,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Contact point extension: consent and contact quality for an ACE phone, email or address.
CREATE TABLE contact_point_ext (
    contact_key varchar(255) PRIMARY KEY,
    contact_type varchar(10) NOT NULL,
    consent_given boolean NOT NULL DEFAULT false,
    consent_at timestamptz,
    verified_at timestamptz,
    failed_count integer NOT NULL DEFAULT 0,
    source varchar(20) NOT NULL DEFAULT 'WORKBENCH',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT ck_contact_point_ext_type CHECK (contact_type IN ('PHONE', 'EMAIL', 'ADDRESS'))
);

-- Account extension: Workbench state about an ACE account, keyed by account_key.
CREATE TABLE account_ext (
    account_key varchar(255) PRIMARY KEY,
    dispute_open boolean NOT NULL DEFAULT false,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Valuation extension: the Workbench's decision about an ACE appraisal, keyed by valuation_key.
CREATE TABLE valuation_ext (
    valuation_key varchar(255) PRIMARY KEY,
    accepted boolean NOT NULL DEFAULT false,
    accepted_at timestamptz,
    accepted_by uuid,
    valuer_partner_id uuid,
    stale_flag boolean NOT NULL DEFAULT false,
    age_days integer,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);
"""

# extension fields: table, field, data type, physical type, mandatory, default, meaning
EXT_FIELDS = [
    ('party_ext', 'person_key', 'TEXT', 'varchar(255)', 'Yes', 'None', 'ACE customer key the flags belong to'),
    ('party_ext', 'vulnerable', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True while the customer is treated as vulnerable'),
    ('party_ext', 'deceased_override', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True when a person confirms death against the ACE record'),
    ('party_ext', 'bankruptcy', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True while a bankruptcy is registered'),
    ('party_ext', 'fraud_flag', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True while fraud is confirmed or under investigation'),
    ('party_ext', 'is_active', 'BOOLEAN', 'boolean', 'Yes', 'true', 'The active or inactive status of the record'),
    ('party_ext', 'state', 'TEXT', 'varchar(40)', 'No', 'None', 'Record lifecycle state'),
    ('party_ext', 'version', 'NUMBER', 'integer', 'Yes', '1', 'Optimistic lock version'),
    ('party_ext', 'created_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record was created'),
    ('party_ext', 'created_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who created the record'),
    ('party_ext', 'updated_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record last changed'),
    ('party_ext', 'updated_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who last changed the record'),
    ('contact_point_ext', 'contact_key', 'TEXT', 'varchar(255)', 'Yes', 'None', 'ACE phone_key, email_key or address_key'),
    ('contact_point_ext', 'contact_type', 'LOV', 'varchar(10)', 'Yes', 'None', 'PHONE, EMAIL or ADDRESS'),
    ('contact_point_ext', 'consent_given', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True while the customer consents to contact'),
    ('contact_point_ext', 'consent_at', 'DATE', 'timestamptz', 'No', 'None', 'When consent was given or withdrawn'),
    ('contact_point_ext', 'verified_at', 'DATE', 'timestamptz', 'No', 'None', 'When the contact point was last verified'),
    ('contact_point_ext', 'failed_count', 'NUMBER', 'integer', 'Yes', '0', 'Consecutive failed attempts on this contact point'),
    ('contact_point_ext', 'source', 'TEXT', 'varchar(20)', 'Yes', 'WORKBENCH', 'Where the row came from'),
    ('contact_point_ext', 'is_active', 'BOOLEAN', 'boolean', 'Yes', 'true', 'The active or inactive status of the record'),
    ('contact_point_ext', 'state', 'TEXT', 'varchar(40)', 'No', 'None', 'Record lifecycle state'),
    ('contact_point_ext', 'version', 'NUMBER', 'integer', 'Yes', '1', 'Optimistic lock version'),
    ('contact_point_ext', 'created_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record was created'),
    ('contact_point_ext', 'created_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who created the record'),
    ('contact_point_ext', 'updated_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record last changed'),
    ('contact_point_ext', 'updated_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who last changed the record'),
    ('account_ext', 'account_key', 'TEXT', 'varchar(255)', 'Yes', 'None', 'ACE account key the state belongs to'),
    ('account_ext', 'dispute_open', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True while a dispute is open on the account'),
    ('account_ext', 'is_active', 'BOOLEAN', 'boolean', 'Yes', 'true', 'The active or inactive status of the record'),
    ('account_ext', 'state', 'TEXT', 'varchar(40)', 'No', 'None', 'Record lifecycle state'),
    ('account_ext', 'version', 'NUMBER', 'integer', 'Yes', '1', 'Optimistic lock version'),
    ('account_ext', 'created_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record was created'),
    ('account_ext', 'created_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who created the record'),
    ('account_ext', 'updated_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record last changed'),
    ('account_ext', 'updated_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who last changed the record'),
    ('valuation_ext', 'valuation_key', 'TEXT', 'varchar(255)', 'Yes', 'None', 'ACE appraisal key the decision belongs to'),
    ('valuation_ext', 'accepted', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True when the appraisal is accepted for the case'),
    ('valuation_ext', 'accepted_at', 'DATE', 'timestamptz', 'No', 'None', 'When the appraisal was accepted'),
    ('valuation_ext', 'accepted_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who accepted the appraisal'),
    ('valuation_ext', 'valuer_partner_id', 'CROSS_REF', 'uuid', 'No', 'None', 'The panel valuer who carried out the appraisal'),
    ('valuation_ext', 'stale_flag', 'BOOLEAN', 'boolean', 'Yes', 'false', 'True when the appraisal is older than its cycle'),
    ('valuation_ext', 'age_days', 'NUMBER', 'integer', 'No', 'None', 'Days from the appraisal date to today'),
    ('valuation_ext', 'is_active', 'BOOLEAN', 'boolean', 'Yes', 'true', 'The active or inactive status of the record'),
    ('valuation_ext', 'state', 'TEXT', 'varchar(40)', 'No', 'None', 'Record lifecycle state'),
    ('valuation_ext', 'version', 'NUMBER', 'integer', 'Yes', '1', 'Optimistic lock version'),
    ('valuation_ext', 'created_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record was created'),
    ('valuation_ext', 'created_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who created the record'),
    ('valuation_ext', 'updated_at', 'DATE', 'timestamptz', 'Yes', 'now()', 'When the record last changed'),
    ('valuation_ext', 'updated_by', 'CROSS_REF', 'uuid', 'No', 'None', 'Who last changed the record'),
]

EXT_OBJECTS = [
    ('party_ext', 'Party extension', 'PTY', 'DP02', 'Workbench', 'Workbench flags about an ACE customer, keyed by person_key.'),
    ('contact_point_ext', 'Contact point extension', 'PTY', 'DP02', 'Workbench', 'Consent and contact quality for an ACE phone, email or address.'),
    ('account_ext', 'Account extension', 'ACC', 'DP01', 'Workbench', 'Workbench state about an ACE account, keyed by account_key.'),
    ('valuation_ext', 'Valuation extension', 'COL', 'DP06', 'Workbench', 'The Workbench decision about an ACE appraisal, keyed by valuation_key.'),
]

SYS_OR = {
    'recovery_case': 'Workbench',
    'treatment': 'Workbench; plan data ACE (from ALS)',
    'notice': 'Workbench; delivery ACE (from WIN)',
    'legal_action': 'ACE (from LIT) and the Workbench',
    'proceeds': 'ACE (from ALS) and the Workbench',
    'write_off': 'ACE (from GL) and the Workbench',
    'asset_sale': 'ACE (from AMIS) and the Workbench',
    'debt_sale_account': 'ACE (from ALS) and the Workbench',
    'interaction': 'ACE (from EFS) and the Workbench',
    'document': 'Workbench',
    'decision_log_entry': 'Workbench',
    'case_list_row': 'ACE (from ALS) and the Workbench',
    'case_entry_exclusion': 'Workbench',
    'listing': 'Workbench',
}

txt = io.open(SRC, encoding='utf-8-sig').read()

# ---------- remove table blocks ----------
for t in REMOVED:
    pat = re.compile(r'\n-- [^\n]*\nCREATE TABLE %s \(.*?\n\);\n' % re.escape(t), re.S)
    new, n = pat.subn('\n', txt)
    if n != 1:
        print('WARN block', t, n)
    txt = new

# ---------- remove constraints, comments, seeds for removed tables ----------
for t in REMOVED:
    txt = re.sub(r'ALTER TABLE %s ADD CONSTRAINT[^;]*;\n' % re.escape(t), '', txt)
    txt = re.sub(r'ALTER TABLE \w+ ADD CONSTRAINT \w+ FOREIGN KEY \([^)]*\) REFERENCES %s \([^)]*\)[^;]*;\n' % re.escape(t), '', txt)
    txt = re.sub(r'CREATE (UNIQUE )?INDEX \w+ ON %s \([^)]*\);\n' % re.escape(t), '', txt)
    txt = re.sub(r"COMMENT ON TABLE %s IS '.*?';\n" % re.escape(t), '', txt, flags=re.S)
    txt = re.sub(r"COMMENT ON COLUMN %s\.[a-z_]+ IS '.*?';\n" % re.escape(t), '', txt, flags=re.S)
    txt = re.sub(r"INSERT INTO sys_objects \([^)]*\) VALUES \('%s',.*?'\);\n" % re.escape(t), '', txt, flags=re.S)
    txt = re.sub(r"INSERT INTO sys_fields \([^)]*\) VALUES \('[A-Z0-9-]+', '%s',.*?'\);\n" % re.escape(t), '', txt, flags=re.S)

# ---------- re-key columns in retained tables ----------
for table, old, new, typ, extra, extratyp in REKEY:
    pat = re.compile(r'(\n    )%s uuid( NOT NULL|,)' % re.escape(old))
    def rep(m):
        tail = m.group(2)
        line = '%s%s %s' % (m.group(1), new, typ)
        if extra:
            line += ' NOT NULL,\n    %s %s NOT NULL' % (extra, extratyp)
        if tail.strip() == ',':
            line += ','
        return line
    txt, n = pat.subn(rep, txt, count=1)
    if n != 1:
        print('WARN rekey', table, old, n)
    txt = re.sub(r'ALTER TABLE %s ADD CONSTRAINT \w+ FOREIGN KEY \(%s\)[^;]*;\n' % (re.escape(table), re.escape(old)), '', txt)
    txt = re.sub(r'COMMENT ON COLUMN %s\.%s IS' % (re.escape(table), re.escape(old)),
                 'COMMENT ON COLUMN %s.%s IS' % (table, new), txt)
    if extra:
        txt = re.sub(r'(COMMENT ON COLUMN %s\.%s IS[^;]*;\n)' % (table, new),
                     lambda m: m.group(1) + "COMMENT ON COLUMN %s.%s IS 'PHONE, EMAIL or ADDRESS for the contact key';\n" % (table, extra),
                     txt, count=1)
    # index on the old column
    txt = re.sub(r'CREATE (UNIQUE )?INDEX (\w+) ON %s \(%s\)' % (re.escape(table), re.escape(old)),
                 lambda m: 'CREATE %sINDEX %s ON %s (%s)' % (
                     m.group(1) or '', m.group(2).replace(old, new), table, new), txt)
    # dictionary row for the old field
    pat_field = re.compile(
        r"VALUES \('([A-Z0-9-]+)', '%s', '%s', 'CROSS_REF', 'uuid', (true|false), (NULL|'[^']*'), '[^']*',"
        % (re.escape(table), re.escape(old)))
    txt, n2 = pat_field.subn(
        lambda m: "VALUES ('%s', '%s', '%s', 'TEXT', 'varchar(255)', %s, %s, NULL," % (
            m.group(1), table, new, m.group(2), m.group(3)), txt)
    if n2 != 1:
        print('WARN field row', table, old, n2)

# Ruling R3: the delegation_limit placeholder rows violate NOT NULL limit_version and regulation_item.
# The table is empty in V0001; content is owned by RWB-E1-038.
txt = re.sub(r"INSERT INTO delegation_limit .*?\);\n", '', txt, flags=re.S)
txt = txt.replace('-- Seed: approval levels with no limits until the delegation of authority table is signed (DL18)',
                  '-- Ruling R3: no delegation_limit rows are seeded. The table is empty until RWB-E1-038 loads DOA-2026.11\n-- through RWB-E1-043. The 23 placeholder rows of v4 violated NOT NULL limit_version and regulation_item.')

# Columns that leave with the six fields ACE now ingests (NLEADS, EasyApp, Entra ID).
DROP_COLS = [
    ('treatment', 'nleads_ref'), ('treatment', 'credit_result'),
    ('treatment', 'credit_result_reason'), ('treatment', 'credit_result_at'),
    ('signature_request', 'external_ref'), ('role', 'entra_group'),
]
for table, col in DROP_COLS:
    m = re.search(r'CREATE TABLE %s \(.*?\n\);' % re.escape(table), txt, re.S)
    if not m:
        print('WARN drop table block', table)
        continue
    block = m.group(0)
    newblock = re.sub(r'\n    %s [a-z0-9_(),]+( NOT NULL)?( DEFAULT [^,\n]+)?,' % re.escape(col), '', block, count=1)
    if newblock == block:
        print('WARN drop col', table, col)
    txt = txt.replace(block, newblock, 1)
    txt = re.sub(r"COMMENT ON COLUMN %s\.%s IS '.*?';\n" % (table, col), '', txt, flags=re.S)
    txt = re.sub(r"INSERT INTO sys_fields \([^)]*\) VALUES \('[A-Z0-9-]+', '%s', '%s',.*?'\);\n" % (table, col),
                 '', txt, flags=re.S)

# ---------- DEF-06: case_list_row and case_entry_exclusion are one row per account per business date ----------
txt = txt.replace("    CONSTRAINT uk_case_list_row UNIQUE (business_date)\n",
                  "    CONSTRAINT uk_case_list_row UNIQUE (business_date, case_id, account_no)\n")
txt = txt.replace("    CONSTRAINT uk_case_entry_exclusion UNIQUE (business_date)\n",
                  "    CONSTRAINT uk_case_entry_exclusion UNIQUE (business_date, account_key)\n")

# ---------- DEF-07: the stage-2 data product snapshots are one row per object per business date ----------
txt = txt.replace("    CONSTRAINT uk_dp_treatment UNIQUE (business_date)\n",
                  "    CONSTRAINT uk_dp_treatment UNIQUE (business_date, treatment_id)\n")
txt = txt.replace("    CONSTRAINT uk_dp_guarantee_claim UNIQUE (business_date)\n",
                  "    CONSTRAINT uk_dp_guarantee_claim UNIQUE (business_date, guarantee_claim_id)\n")

# ---------- extension tables ----------
marker = '\n-- References between tables'
if marker not in txt:
    marker = '\nALTER TABLE recovery_case ADD CONSTRAINT'
idx = txt.find(marker)
txt = txt[:idx] + EXT_DDL + txt[idx:]

# ---------- header ----------
txt = txt.replace(
    '-- Recovery Workbench physical schema, PostgreSQL\n-- SCB Collections and Recovery. Henka Group, 28 October 2026. Version 1.',
    '-- Recovery Workbench physical schema, PostgreSQL\n-- SCB Collections and Recovery. Henka Group, 15 November 2026. Version 5.')
txt = re.sub(r'-- 108 tables in the recovery module of the ACE database.*',
             '-- 92 tables and 30 views in the recovery module of the ACE database, the metadata registry of bank TSD section T3, and seed reference data.\n'
             '-- Source data is read from the ACE database through recovery.v_ace_* views (D-RCV-35, ADR-010). No inbound load table, no source copy.\n'
             '-- Flyway split: V0001 tables and dictionary, V0002 Tier 1 views, V0003 Tier 2 views once RWB-ACE-001 lands.', txt)

# ---------- data_product seed ----------
DP = """-- Seed: the 14 data products, before sys_objects which references them (D-RCV-29; ruling DEF-01).
INSERT INTO data_product (product_code, product_name, definition, system_of_record, owner_role, refresh_cycle, expected_by, valid_from) VALUES
('DP01','Account and arrears','Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments','ACE (from ALS via COLLINS)','RW-DATASTEW','DAILY','08:00',DATE '2026-11-30'),
('DP02','Customer and party','Customers, guarantors, co-borrowers and heirs, masked identifiers, contact points, consent and flags for vulnerability, death and bankruptcy','ACE (from SCBPDM and the core bank)','RW-DATASTEW','DAILY','08:00',DATE '2026-11-30'),
('DP03','Case and ownership','The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations','Workbench','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30'),
('DP04','Treatment and offers','Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome','Workbench; plan data ACE (from ALS)','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30'),
('DP05','Contact and promises','Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS','ACE (from EFS) and the Workbench','RW-DATASTEW','DAILY','08:00',DATE '2026-11-30'),
('DP06','Collateral and assets','Collateral, appraisals, assets held after repossession or transfer, listings and sale results','ACE (from CCMS, SVAF, AMIS and RPS)','RW-DATASTEW','WEEKLY','MON 08:00',DATE '2026-11-30'),
('DP07','Legal events and cases','Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement','ACE (from LIT and WIN) and the Workbench','RW-DATASTEW','DAILY','08:00',DATE '2026-11-30'),
('DP08','Partner performance','Partners on the panel, work placed with each, results, fees and scorecards','Workbench','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30'),
('DP09','Debt sale','Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs','Workbench','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30'),
('DP10','Documents and extracted fields','Documents against the case, the fields read from them, retention class and custody of originals','Workbench','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30'),
('DP11','Scores and route economics','Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions','ACE (from COLLINS)','RW-DATASTEW','DAILY','08:00',DATE '2026-11-30'),
('DP12','Decision log','One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome','Workbench','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30'),
('DP13','Money and closure','Payments and proceeds matched to the case, write-off postings and recovery after charge-off','ACE (from ALS and GL)','RW-DATASTEW','DAILY','08:00',DATE '2026-11-30'),
('DP14','Reference data','Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned','Workbench','RW-DATASTEW','ON_CHANGE','As it changes',DATE '2026-11-30');

"""
i = txt.find("INSERT INTO sys_objects")
txt = txt[:i] + DP + txt[i:]

# data_product nullable (R1) and OPS/AGT/RPT to NULL
txt = txt.replace('    data_product varchar(10) NOT NULL,\n', '    data_product varchar(10),\n')
txt = re.sub(r"(INSERT INTO sys_objects \([^)]*\) VALUES \('[a-z_]+', '[^']*', '[A-Z]+', )'(OPS|AGT|RPT)'",
             r"\1NULL", txt)

# system of record reworded
for obj, sor in SYS_OR.items():
    txt = re.sub(r"(INSERT INTO sys_objects \([^)]*\) VALUES \('%s', '[^']*', '[A-Z]+', '[A-Z0-9]+', )'[^']*'" % re.escape(obj),
                 lambda m: m.group(1) + "'" + sor + "'", txt)

# ---------- extension and view objects/fields ----------
def sqlq(s):
    return "'" + s.replace("'", "''") + "'"

obj_lines = []
for t, name, subj, dp, sor, desc in EXT_OBJECTS:
    obj_lines.append("INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES (%s, %s, %s, %s, %s, %s);"
                     % (sqlq(t), sqlq(name), sqlq(subj), sqlq(dp), sqlq(sor), sqlq(desc)))

# view objects from the views file
views_txt = io.open(VIEWS, encoding='utf-8').read()
view_defs = re.findall(r'CREATE OR REPLACE VIEW recovery\.(v_ace_[a-z_]+)\s*\nAS\n(.*?);\n\nCOMMENT ON VIEW', views_txt, re.S)
view_names = [v[0] for v in view_defs]
VIEW_DP = {
    'v_ace_account': 'DP01', 'v_ace_payment': 'DP01', 'v_ace_batch_status': 'DP01',
    'v_ace_customer': 'DP02', 'v_ace_contact': 'DP02', 'v_ace_ca_relation': 'DP02',
    'v_ace_aa_relation': 'DP02', 'v_ace_party_product': 'DP02',
    'v_ace_plan': 'DP04', 'v_ace_credit_decision': 'DP04',
    'v_ace_efs_action': 'DP05', 'v_ace_efs_action_code': 'DP05', 'v_ace_efs_assignment': 'DP05',
    'v_ace_collateral': 'DP06', 'v_ace_collateral_detail': 'DP06', 'v_ace_asset': 'DP06',
    'v_ace_valuation': 'DP06', 'v_ace_npa_asset': 'DP06', 'v_ace_npa_sale': 'DP06',
    'v_ace_lawsuit': 'DP07', 'v_ace_hearing': 'DP07', 'v_ace_pod': 'DP07',
    'v_ace_esign': 'DP10', 'v_ace_score': 'DP11', 'v_ace_write_off': 'DP13',
    'v_ace_product': 'DP14', 'v_ace_branch': 'DP14', 'v_ace_holiday': 'DP14', 'v_ace_iam_group': 'DP14',
}
PERSONAL_VIEW_FIELDS = {'id_no_masked', 'id_no_last4', 'contact_value', 'contact_value_masked',
                        'first_name', 'last_name', 'date_of_birth', 'spouse_name', 'vat_number'}
for v in view_names:
    obj_lines.append("INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES (%s, %s, 'ACE', %s, 'ACE', %s);"
                     % (sqlq(v), sqlq(v.replace('v_ace_', 'ACE ').replace('_', ' ').title()),
                        sqlq(VIEW_DP.get(v, 'DP01')),
                        sqlq('Read-only view over ACE. ' + v.replace('v_ace_', '').replace('_', ' ') + '.')))

i = txt.find('INSERT INTO sys_fields')
txt = txt[:i] + '\n'.join(obj_lines) + '\n\n' + txt[i:]

# extension fields
ext_lines = []
n = 0
for t, f, dt, pt, mand, dflt, meaning in EXT_FIELDS:
    n += 1
    fid = 'DF-EXT-%03d' % n
    ext_lines.append("INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES (%s, %s, %s, %s, %s, %s, NULL, NULL, 'Workbench', NULL, false, %s);"
                     % (sqlq(fid), sqlq(t), sqlq(f), sqlq(dt), sqlq(pt), 'true' if mand == 'Yes' else 'false', sqlq(meaning)))

# view fields: parse select aliases per view with their expression
ace_types = {}
for row in csv.DictReader(io.open(r'15 ACE DB Alignment\ACE Schema Extract v1.csv', encoding='utf-8')):
    ace_types[(row['table'], row['column'])] = row['sql_type']


def wbtype(sql_type):
    t = sql_type.lower()
    if t == 'date':
        return 'DATE'
    if t == 'boolean':
        return 'BOOLEAN'
    if any(k in t for k in ('int', 'numeric', 'decimal', 'double', 'real')):
        return 'NUMBER'
    return 'TEXT'


def phys(sql_type):
    t = sql_type.lower()
    if t == 'date':
        return 'date'
    if t == 'boolean':
        return 'boolean'
    if any(k in t for k in ('int')):
        return 'integer'
    if 'numeric' in t or 'decimal' in t:
        return 'numeric(18,2)'
    return 'varchar(255)'

vf_lines = []
n = 0
for name, body in view_defs:
    aliases = {}
    for m in re.finditer(r'(?:FROM|JOIN)\s+public\.([a-z_]+)\s+([a-z][a-z0-9_]*)', body):
        aliases[m.group(2)] = m.group(1)
    body2 = re.sub(r'\n\s+AS\s+', ' AS ', body)
    sel = body2[:body2.find('\nFROM ')] if '\nFROM ' in body2 else body2
    for line in sel.split('\n'):
        line = line.strip().rstrip(',')
        m = re.match(r"^(.*?)\s+AS\s+([a-z_][a-z0-9_]*)$", line)
        if not m:
            continue
        expr, alias = m.group(1), m.group(2)
        src_tbl = src_col = None
        for am in re.finditer(r'\b([a-z][a-z0-9_]*)\.([a-z_][a-z0-9_]*)', expr):
            if am.group(1) in aliases:
                src_tbl, src_col = aliases[am.group(1)], am.group(2)
                break
        sql_type = ace_types.get((src_tbl, src_col), 'character varying')
        n += 1
        fid = 'DF-ACE-%03d' % n
        vf_lines.append("INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES (%s, %s, %s, %s, %s, false, NULL, NULL, 'ACE', %s, %s, %s);"
                        % (sqlq(fid), sqlq(name), sqlq(alias), sqlq(wbtype(sql_type)), sqlq(phys(sql_type)),
                           sqlq('public.%s.%s' % (src_tbl, src_col)) if src_tbl else 'NULL',
                           'true' if alias in PERSONAL_VIEW_FIELDS else 'false',
                           sqlq('Read from ACE through ' + name)))

# append at end of file
txt = txt.rstrip() + '\n\n-- Extension and view rows for the data dictionary\n' + '\n'.join(ext_lines + vf_lines) + '\n'

# ---------- functions and views ----------
funcs_views = views_txt[views_txt.find('CREATE SCHEMA IF NOT EXISTS recovery;'):]
funcs_views = funcs_views.replace('CREATE SCHEMA IF NOT EXISTS recovery;\n\n', '')
txt = txt.rstrip() + '\n\n-- ---------------------------------------------------------------------------\n-- ACE source views. Section A ships as V0002; Section B ships after RWB-ACE-001.\n-- ---------------------------------------------------------------------------\n\n' + funcs_views + '\n'

io.open(OUT, 'w', encoding='utf-8').write(txt)
print('wrote', OUT, 'chars', len(txt))
print('extension fields', len(ext_lines), 'view fields', len(vf_lines), 'views', len(view_names))
