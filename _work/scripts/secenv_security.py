import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx
from secenv_lib import *

SRC = '05 Technical architecture/Recovery Workbench Security and Access Design v2.docx'
DST = '05 Technical architecture/Recovery Workbench Security and Access Design v3.docx'
d = docx.Document(SRC)
doc_control(d, 'Recovery Workbench Security and Access Design v3',
    'D-RCV-35 (ADR-010): the Workbench reads ACE through read-only recovery.v_ace_* views and runs no load. '
    'National ID no longer tokenized at load; the data load service identity removed; read-only ACE access added (sections 1, 2, 5, 7 to 11)')

T = d.tables
# 1. One page
set_row(T[1], 'Masking', [None,
    'Personal fields masked in the response at the API unless the role may see them (E1-037). The national ID is never read in clear: '
    'v_ace_customer returns id_no_masked and id_no_last4 only. Every read of a personal field is audited', 'Designed; rules DL26'])
set_row(T[1], 'Service identities', [None,
    'Managed identities with credentials in Key Vault; one identity per non-human actor. No data load identity: ACE ingests every source', 'ACE pattern'])
insert_row_after(T[1], 'Service identities', ['ACE data access',
    'Read only. The recovery service role holds SELECT on the recovery.v_ace_* views and nothing else; the views are owned by ace_view_owner, '
    'which reads the public ACE tables. No direct public read, no write, PUBLIC revoked', 'Designed; D-RCV-35, RWB-E1-069'])

# 2. Context
p = para_starting(d, 'The Workbench is a module of the ACE service.')
set_text(p, p.text + ' The Workbench loads, copies and transforms no source data. ACE ingests every source into the ACE database, '
    'and the recovery module reads it only through SELECT-only recovery.v_ace_* views (D-RCV-35, ADR-010).')

# 5. Personal data protection
set_row(T[5], 'Tokenization', ['National ID',
    'ACE holds the national ID or passport number (customer.identification_number). The Workbench never reads it in clear: v_ace_customer returns '
    'id_no_masked, with only the last four digits shown, and id_no_last4. Nothing is tokenized at load, because there is no load; '
    'role masking at the API (E1-037) replaces the former id_no_token'])
set_row(T[5], 'Masking', [None,
    'Name, address, phone, email and account numbers are masked at the API by the masking profile of the role (E1-037). v_ace_contact returns the '
    'full phone, email and address, because notices and calls need them, so the API mask is the control. The profile is a data row per role and field'])
insert_row_after(T[5], 'Unmasking', ['Audit of reads',
    'Every read of a personal field, including each read through v_ace_customer and v_ace_contact, is written to the PII log through PII Kafka. '
    'The control is the read-only grant, E1-037 masking and the audit log together; the mask in a view is not a PDPA control on its own'])

# 7. Service identities and secrets
set_row(T[6], 'Managed identities', [None,
    'One per non-human actor: case workflow, rules component, OCR pipeline, decision log writer, agent platform. '
    'There is no data load identity: ACE ingests every source, and the Workbench runs no load (D-RCV-35)'])
set_row(T[6], 'Database', [None,
    'The service connects with its managed identity. The recovery schema is still owned by the service; people do not hold write access in production. '
    'No recovery migration creates or alters a table in the ACE public schema'])
insert_row_after(T[6], 'Database', ['Read-only ACE access',
    'The recovery service role (recovery_svc) holds USAGE on schema recovery and SELECT on the recovery.v_ace_* views only. It holds no SELECT on any '
    'public ACE table and no INSERT, UPDATE, DELETE or TRUNCATE on any ACE table or view, so a direct public read or a write fails in the database '
    'catalog, not only in code review. This is the read-only ACE service identity of the Admin and Access Model v5'])
insert_row_after(T[6], 'Read-only ACE access', ['View owner',
    'The v_ace_* views are owned by ace_view_owner, a NOLOGIN ACE role that holds SELECT on the public ACE tables the views read and writes '
    'neither schema. It is not a Workbench role and nobody signs in as it. A view runs with its owner\'s privileges, so any row-level security '
    'ACE adds later is applied inside the view'])
insert_row_after(T[6], 'View owner', ['PUBLIC',
    'All privileges on the recovery tables and views are revoked from PUBLIC. A role reads a view only through an explicit grant'])
insert_row_after(T[6], 'PUBLIC', ['Grant check',
    'The view conformance test in RWB-E1-069 runs in the pipeline and fails the build if recovery_svc can select a public table or write any table, '
    'if a v_ace_* view does not compile, or if a constraint in schema recovery references a public table'])

# 8. Logging
set_row(T[7], 'PII log', [None,
    'Every read and unmask of a personal field, including reads through v_ace_customer and v_ace_contact, through PII Kafka', None])

# 9. Threats
set_row(T[8], 'Tampering', [None, None,
    'Append-only, hash-chained decision log; write-once container for legal documents; no write grant on any ACE table or view'])
set_row(T[8], 'Information disclosure', [None, None,
    'Scope filter; masking (E1-037); national ID masked in v_ace_customer; SELECT on recovery.v_ace_* only, no direct public read; '
    'PII log; no personal data in exports beyond the role'])

# 10. Tests
insert_row_after(T[9], 'Masking', ['Read-only ACE grant',
    'The view conformance test passes: recovery_svc reads every v_ace_* view, cannot select a public table and cannot insert, update or delete on any table',
    'Tech lead'])

# 11. Open decisions
insert_row_after(T[10], 'DL40', ['DL43',
    'Whether the ACE team accepts the RWB-ACE-001 scope and dates, needed by 21 November 2026',
    'Section A views and grants only; the features that need the Section B views stay behind their flags'])

d.save(DST)
print('saved', DST)
