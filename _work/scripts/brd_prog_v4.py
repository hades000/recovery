"""Build Business Requirements Program v4 from v3 (D-RCV-35 ACE DB alignment, tracker row 9)."""
import copy
import docx

SRC = r'03 Requirements and specifications\Recovery Workbench Business Requirements Program v3.docx'
DST = r'03 Requirements and specifications\Recovery Workbench Business Requirements Program v4.docx'

d = docx.Document(SRC)
T = d.tables
P = d.paragraphs


def set_par(p, text):
    runs = p.runs
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def set_cell(cell, text):
    ps = cell.paragraphs
    set_par(ps[0], text)
    for p in ps[1:]:
        p._p.getparent().remove(p._p)


def row_by_id(table, key):
    for r in table.rows:
        if r.cells[0].text.strip() == key:
            return r
    raise KeyError(key)


def set_row(table, key, values):
    """values: dict col_index -> text."""
    r = row_by_id(table, key)
    for i, v in values.items():
        set_cell(r.cells[i], v)


def add_row_after(table, after_key, values):
    src = row_by_id(table, after_key)
    new = copy.deepcopy(src._tr)
    src._tr.addnext(new)
    r = [x for x in table.rows if x._tr is new][0]
    for i, v in enumerate(values):
        set_cell(r.cells[i], v)


def check(p, expected):
    assert p.text.strip() == expected, (p.text, expected)


# ---- Title block and document control
check(P[3], 'SCB Collections and Recovery. Henka Group, 28 October 2026')
set_par(P[3], 'SCB Collections and Recovery. Henka Group, 15 November 2026')
dc = T[0]
set_row(dc, 'Version', {1: '4'})
set_row(dc, 'Date', {1: '15 November 2026'})
add_row_after(dc, 'Structure', ['Change',
    'Version 4 re-bases the program requirements on the ACE database under D-RCV-35 (U1 to U5) and ADR-010. '
    'Sections 1.1, 5 (intro and 5.1 to 5.3), 6.3, 6.5 (NFR-032), 7 and 9 change: the Workbench runs no inbound source load, reads source data only '
    'through the read-only recovery.v_ace_* views, links cases to ACE records by business key, and leaves Excel and '
    'SharePoint trackers to the Cutover plan. Requirement IDs are kept; REQ-RDF-005, 006 and 008 are marked removed '
    'with their later home, leaving 228 of 231 requirements live. DL43 is added as open. Other sections are unchanged.'])

# ---- 1.1 In scope and 5 intro (follow-up)
check(P[12], 'The recovery module of ACE, with data through COLLINS and file loads.')
set_par(P[12], 'The recovery module of ACE, with data through ACE ingestion; the Workbench reads read-only ACE views (D-RCV-35).')
assert P[25].text.startswith('231 business requirements across the platform and stage modules.')
set_par(P[25], '231 business requirements across the platform and stage modules, of which 3 are removed by D-RCV-35 (228 live). '
    'Must is needed for the epic to release; Should is planned in the epic; Could is taken if capacity allows.')

# ---- 5.1 P1 Recovery data engine
t = T[5]
set_row(t, 'REQ-RDF-001', {1: 'Recovery data is held in 14 data products, each with exactly one named system of record and one named owner. '
    'Source data in a data product is read from the ACE database through the read-only recovery.v_ace_* views and is not copied into the Workbench (D-RCV-35, ADR-010).'})
set_row(t, 'REQ-RDF-002', {1: 'Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through v_ace_account and v_ace_payment, '
    'current to the latest completed ACE batch for the previous working day.'})
set_row(t, 'REQ-RDF-003', {1: 'Collections contact history, promises and case status from EFS are read from ACE through v_ace_efs_action and v_ace_efs_assignment, '
    'so that the case carries what happened before day 90.'})
set_row(t, 'REQ-RDF-004', {1: 'Collateral records and appraisal values are available on the case without a person looking them up in CCMS or SVAF. '
    'ACE ingests them under RWB-ACE-001, and the Workbench reads them through v_ace_collateral, v_ace_collateral_detail and v_ace_valuation (DL43). '
    "The Workbench's acceptance of an appraisal is held in valuation_ext."})
set_row(t, 'REQ-RDF-005', {1: 'Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the tracker retirement procedure in the Cutover and Go Live Plan. '
    "Was: every recovery team's Excel file, SharePoint list and local file is listed with its owner, fields and update cycle, and each one has a decision to load it or record it as out of scope.",
    2: 'Removed'})
set_row(t, 'REQ-RDF-006', {1: 'Removed by D-RCV-35 (U5). No tracker is loaded into the Workbench. Later home: the Cutover and Go Live Plan, which retires each local copy with the owner\'s confirmation and a read-only archive. '
    'Was: every file with a load decision is loaded, its row counts reconciled, and its local copy retired with the owner\'s confirmation and a read-only archive kept.',
    2: 'Removed'})
set_row(t, 'REQ-RDF-007', {1: 'The case list reconciles daily to the ALS count of accounts at 90 or more days past due, read through v_ace_account, with no variance (DL25).'})
set_row(t, 'REQ-RDF-008', {1: 'Removed by D-RCV-35 (U1). The Workbench runs no load, so it runs no data quality rules on source rows. Later home: the ACE ingestion checks under RWB-ACE-001; '
    'the daily gate on the case list moves into the freshness stamp (REQ-RDF-009) and the reconciliation (REQ-RDF-007). '
    'Was: data quality rules run on every load, and every failed row carries a reason code visible to the data product owner.',
    2: 'Removed'})
set_row(t, 'REQ-RDF-009', {1: 'Every data product carries a freshness stamp taken from the ACE batch record (v_ace_batch_status), and every decision records the freshness of the data it used.'})
set_row(t, 'REQ-RDF-010', {1: 'Access to each data product is controlled per role, and personal data is masked by role in line with PDPA. '
    'The recovery service identity holds SELECT on the recovery.v_ace_* views only, and the customer identification number leaves ACE masked.'})
set_row(t, 'REQ-RDF-011', {1: 'Every data product has a catalog entry stating its definition, owner, system of record, refresh cycle and retention, '
    'and, for source data, the ACE table and the view it is read through.'})

# ---- 5.2 P2 Integration
t = T[6]
set_row(t, 'REQ-DRI-006', {1: 'No component calls a system of record directly. Source data lands in the ACE database through ACE ingestion and is read only through the recovery.v_ace_* views; '
    'data leaves through paths ACE already has (D-RCV-35, ADR-010).'})
set_row(t, 'REQ-DRI-007', {1: 'The integration adapters log every outbound file, retry on a defined schedule, and place anything that fails after the retry limit in an exception queue with a task for a named owner. '
    'Inbound files belong to ACE ingestion (D-RCV-35).'})
set_row(t, 'REQ-DRI-008', {1: 'The Workbench runs no inbound batch or file load. Source data reaches it at the frequency ACE ingests it, and work that depends on a source starts when the ACE batch for that source is complete. '
    'Interfaces that need same-day data are named under DL06 before any is built.'})
set_row(t, 'REQ-DRI-013', {1: 'Case hand-over from EFS is read from ACE through v_ace_efs_assignment once the ACE batch for EFS is complete, and plan status is read from the ACE common module, '
    'so a case is current the morning after it changes.'})

# ---- 5.3 P3 Case and workflow
t = T[7]
set_row(t, 'REQ-CWC-001', {1: 'Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule from the daily case list once the ACE batch for ALS is complete.'})
set_row(t, 'REQ-CWC-003', {1: 'One case covers one customer and one product, with its accounts linked to it. The case links to the customer by the ACE person_key and to each account by the ACE account_key, '
    'with no foreign key into ACE (D-RCV-35, U4).'})
set_row(t, 'REQ-CWC-004', {1: 'Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation. '
    'The inputs are read from the ACE views and from the Workbench extension tables keyed by person_key and account_key.'})
set_row(t, 'REQ-CHO-001', {1: 'A case transferred from collections reaches the Workbench on the day of transfer, with its full contact and promise history read from ACE through the EFS views. '
    'Case transferred from EFS is a named same-day trigger under DL06.'})
set_row(t, 'REQ-CHO-003', {1: 'Customer, product and account facts reach the case from ACE, which ingests them from SCBPDM and the core bank, read through v_ace_customer, v_ace_party_product and v_ace_account '
    '(DL20 as amended by D-RCV-35).'})
set_row(t, 'REQ-CHO-008', {1: 'A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next business date\'s ACE account data in v_ace_account.'})
set_row(t, 'REQ-CHO-009', {1: 'Payments received, read from ACE through v_ace_payment, are matched to the plan, the settlement or the fee they belong to by the ACE payment_code, and anything unmatched goes to an exception list.'})
set_row(t, 'REQ-CHO-010', {1: 'A duplicate case for the same customer and product, by ACE person_key and product, merges into the earlier case, carrying its documents and decision log.'})

# ---- 6.3 ACE data freshness and batch-complete triggers
h = P[64]
check(h, '6.3 Loads and batch')
set_par(h, '6.3 ACE data freshness and batch-complete triggers')
intro = copy.deepcopy(P[16]._p)
h._p.addnext(intro)
ip = docx.text.paragraph.Paragraph(intro, h._parent)
set_par(ip, 'The Workbench runs no inbound load (D-RCV-35, U1). Work that depends on source data starts when ACE records the batch for that source and business date as complete in '
    'v_ace_batch_status: case creation and the case list on the ALS batch, hand-over on the EFS batch. A late batch delays the work and raises an alert; it never starts a Workbench load. '
    'NFR-016, NFR-017 and NFR-019 are Workbench document and scheduling jobs; they load no source data.')
t = T[23]
set_row(t, 'NFR-013', {1: 'Under D-RCV-35 (U1 and U4) and ADR-010, the Workbench reads source data only through the recovery.v_ace_* views, and every case list and decision states the business date and load time of the ACE source batches behind it.',
    2: 'Case list available by 07:00 on the latest completed ACE batch', 3: 'Proposed, DL43'})
set_row(t, 'NFR-014', {1: 'Freshness is read from recovery.v_ace_batch_status, one row per source and business date; a missing, failed or late batch is visible on the case list and alerts the data steward.',
    2: 'Start of day, on the ACE business date', 3: 'Proposed, DL43'})
set_row(t, 'NFR-015', {1: 'The Workbench holds no load window: a late ACE batch delays the case list and raises an alert rather than starting a Workbench load, catch-up job or staging table.'})
set_row(t, 'NFR-018', {1: 'The case list reconciles to the ACE account view daily.'})

# ---- 6.5 Retention (follow-up)
set_row(T[25], 'NFR-032', {1: 'Under D-RCV-35 (U5), retired local files and Excel and SharePoint trackers are handled through the Cutover and Go Live Plan, '
    'which keeps each as a read-only archive at a recorded location. The Workbench loads and holds no tracker.',
    2: 'Archive location recorded per file in the Cutover and Go Live Plan'})

# ---- 7 Constraints
t = T[33]
set_row(t, 'Data through COLLINS', {0: 'Data through ACE ingestion',
    1: 'Source data lands in the ACE database through ACE ingestion, including sources ACE does not hold today. The recovery module reads it only through the read-only recovery.v_ace_* views, '
       'links to it by ACE business keys and holds no copy, load or staging table (D-RCV-35, ADR-010). No real-time feed today; same-day needs are named under DL06'})
add_row_after(t, 'Data through ACE ingestion', ['ACE team dependency',
    'The ACE team owns every ACE table and column the views read, and adds 14 tables, 12 columns and 80 source fields under RWB-ACE-001 by 21 November 2026 for the 30 November release (DL43). '
    'Features that read the Tier 2 additions stay behind their feature flags until the additions land'])

# ---- 9 Open decisions
t = T[35]
set_row(t, 'DL06', {2: 'Option A, daily batch through COLLINS, is superseded by D-RCV-35: ACE ingests all source data, so the Workbench runs no batch load and reads ACE once its batch is complete. '
    'Option B for the named same-day triggers. ACE has no real time feed today. Name the same-day triggers now: case transferred from EFS, payment received, legal event.'})
set_row(t, 'DL12', {2: 'No legacy enhancement, with a list of the systems kept and what the Workbench reads from each. The read and write part of option A is superseded by D-RCV-35: '
    'source data is read only, through the SELECT-only recovery.v_ace_* views, not a direct read of ACE or COLLINS.'})
set_row(t, 'DL20', {2: 'The customer facts ACE holds, which ACE ingests from SCBPDM and the core bank; the Workbench reads them through v_ace_customer. Amended by D-RCV-35, which removes the COLLINS route.'})
add_row_after(t, 'DL27', ['DL43',
    'Does the ACE team accept the RWB-ACE-001 scope and its dates? The scope is 14 new ACE tables, 12 new columns and 80 source fields.',
    'Assume the scope is accepted; dates to confirm, and Tier 2 features stay behind their flags until the additions land.',
    'ACE team lead', '21 Nov'])

d.core_properties.revision = (d.core_properties.revision or 0) + 1
d.save(DST)
print('saved', DST)
