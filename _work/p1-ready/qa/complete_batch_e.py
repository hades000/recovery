from pathlib import Path
import csv,re,json

WORK=Path.cwd()
stage=WORK/'stage'
base=stage/'24 P1 Developer Readiness v1'
source=(WORK.parent.parent/'24 P1 Developer Readiness v1'/'decisions'/'batch-E.md').read_text(encoding='utf-8')
decision_defs=[
('RD-P1-089','Ledger series, integrity check, protection of append-only objects and the sandbox reload',
 'E1066-OPS#1; E1065-APP#1; GAP-3494, GAP-3493',
 'Resolve append-only monitoring and sandbox reload contradictions without changing the ledger schema or granting environment reset access.',
 'RWB-P1-E1066-OPS v3 sections 4, 6, 11; RWB-P1-E1065-APP v3 sections 4, 9, 11; RD-P1-073; Physical Schema v9 interaction trigger.',
 '1. Keep the existing five observations: append rate, append failure count by error class, duplicate hit count, append latency p95, and sequence gap check. The application stories own the metric names, types, labels and emission. Until those are merged, deployment checks validate trigger presence and exercise append, update and delete refusal, while monitoring dashboards and alerts remain disabled. Do not invent metric identifiers. GAP-3494 stays open and blocks operational readiness.\n2. The sequence check compares live ledger rows for open cases. Closed-case sequence gaps caused by retention archiving are accepted.\n3. Production and shared test environments never truncate, delete or reset interaction rows. An isolated sandbox rebuild recreates its database from the versioned DDL and reseeds it. While a sandbox database is shared, the profile reload leaves interaction rows intact and seeds them only when the table is empty.\n4. The application login does not bypass the append-only trigger. A separately controlled migration owner may apply forward DDL. No application, sandbox or on-call identity receives TRUNCATE or trigger-disable rights. GAP-3493 closes for the reload mechanism; permission separation remains a delivery verification item.',
 'RWB-P1-E1066-OPS, RWB-P1-E1065-APP, RWB-P1-E1066-APP',
 'RWB-P1-E1066-OPS#1; RWB-P1-E1065-APP#1','Closes GAP-3493; GAP-3494 remains open until named metrics and emitters are published.'),
('RD-P1-090','Migrated ledger entries: the cutover entry point of the writer',
 'DM005-APP#1 (story)',
 'The cutover must retain migration provenance while respecting the append-only writer and the existing writer field contract.',
 'RD-P1-007 and RD-P1-068; RWB-P1-DM005-APP v3 AC3, AC4 and writer dependency; Physical Schema v9 DF-INT rows.',
 '1. The migration cutover uses a dedicated migration append operation owned by rwb-source-data. It writes the interaction row through the same transaction and append-only sequence allocator as InteractionLedgerWriter. It accepts the legacy mapping plus migration_source and migrated_at, and persists the provenance columns required by RD-P1-068. It does not grant DM005 direct table-write privileges.\n2. The public interaction operation remains unchanged. Only the migration caller can invoke the migration operation, using a migration workload identity and the cutover authorization of RD-P1-093.\n3. The exact operation signature, source mapping and identity are not published in the staged contracts. Until the P1 contract owner publishes them, DM005 may extract and stage rows, but must not write interaction or mark the cutover complete. GAP-3551 remains open and blocks the cutover.',
 'RWB-P1-DM005-APP, RWB-P1-E1066-APP, RWB-P1-E1066-CON',
 'RWB-P1-DM005-APP#1','GAP-3551 remains open for operation signature and mapping.'),
('RD-P1-091','Access-log entries use the access-log contract and never become decision records',
 'E1068-APP#2; RD-P1-072; GAP-3395, GAP-3322',
 'Resolve the conflict between P1 privacy-read logging and the P4 access-log owner.',
 'RD-P1-072; RWB-P4-E1023-APP and RWB-P4-E1039; staged rwb-access.yaml 5.1.0; RWB-P1-E1068-APP v3.',
 '1. P1 access and masking checks call the rwb-access access-log operation. P1 does not insert access events into decision_record, outbox_event or interaction. Decision records remain business decisions only.\n2. Until P4 publishes the access-log request, response, operation path and fake, the P1 tests assert only that the access-log client is called with the event class and that failure follows the existing fail-closed behavior. P1 does not claim that a production audit entry was persisted.\n3. Each story owner must keep confidential values and field values out of access-log payloads. GAP-3395 and the access-log portion of GAP-3322 remain open with the P4 contract owner.',
 'RWB-P1-E1068-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P4-E1023-APP, RWB-P4-E1039',
 'RWB-P1-E1068-APP#2','GAP-3395 and access-log portion of GAP-3322 remain open.'),
('RD-P1-092','Retention run record, review list, age bases, record classes and the archive container',
 'E1017-APP#1, #4, #5; E1017-OPS#1; GAP-3457, GAP-3454, GAP-0490',
 'Specify a run record and safe interim behavior for review-only tables and archive setup.',
 'RD-P1-047; RWB-P1-E1017-APP/CON/OPS v3; Physical Schema v9; GAP-0490, GAP-3454 and GAP-3457.',
 '1. RetentionRunWorkflow remains the sole run coordinator. Do not write retention state into AD018 job_run or job_run_check because those records do not carry the retention result fields or archive manifest.\n2. Until a P1-owned run-record schema is approved and migrated, recordRun must not report a durable completed result. The workflow result is the provisional execution record. GET by runId may expose the Temporal execution state and result only while that execution remains queryable; the API must return the existing not-found response after Temporal no longer retains it. GAP-3457 stays open and blocks the durable GET requirement.\n3. The four rows contact_point_ext, valuation_ext, dp_treatment and dp_guarantee_claim remain REVIEW-only and are listed without deletion until Compliance and the data architect publish their age basis and record class (GAP-3454).\n4. Interaction retention uses closedAt and retains rows exactly on the cutoff, per E1017-APP.\n5. Keep the path and manifest shape already specified in GAP-0490. The P1 workload identity writes using its own credential and verifies row count and SHA-256 before any delete. The platform owner still must provide the per-environment container and immutable role. No archive delete proceeds until that role and container are configured.',
 'RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P1-AD018-APP',
 'RWB-P1-E1017-APP#1; RWB-P1-E1017-APP#4; RWB-P1-E1017-APP#5; RWB-P1-E1017-OPS#1',
 'GAP-3457, GAP-3454 and GAP-0490 remain open with the data architect, Compliance and platform/storage owners.'),
('RD-P1-093','Migration cutover provenance, authorization, handover package and clean days',
 'DM003-APP#1; DM004-APP#1; DM006-APP#1; DM007-APP#1, #2; orchestrator cutover questions',
 'Make source data migration use one publication handover and one acceptance record per owner without relaxing provenance or access controls.',
 'RD-P1-068; Architecture v5 ownership and service boundary; PRD P1 v3 migration rules; DM003 to DM007 staged v3 stories and their source-to-target mappings.',
 '1. The normative package allow-list and field mapping remain the Source to Target Mapping v7 Migration packages sheet. Every migrated target row carries migration_source and migrated_at in UTC. A service must not add fields outside its package.\n2. P1 does not read another service database or write another service schema. The source owner publishes an immutable extract package and manifest. The target owner imports through its own migration component. The handover record names package, checksum, row count, source and target owners, environment and acceptance result.\n3. Each target owner accepts by comparing the package checksum and row count, validating required target keys and recording accepted or rejected with a reason. A timeout or absent acceptance leaves the package staged and the cutover blocked. Do not infer acceptance from a successful file transfer.\n4. The exact archive transport and role follow RD-P1-092. Data retention or deletion of source files requires the owning policy and archive contract.\n5. The two clean-day count checks may run against the named source extract and target tables, but cannot be used as a release gate until the active population and comparison date are fixed by the package owner. The affected stories must mark those checks Pending with the responsible data owner.',
 'RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP',
 'RWB-P1-DM003-APP#1; RWB-P1-DM004-APP#1; RWB-P1-DM006-APP#1; RWB-P1-DM007-APP#1',
 'Source package layout, authorization and clean-day population remain owned by the data owners where no source defines them.'),
('RD-P1-094','Extension facts: first write, existing row read, ETag and access rule',
 'E1018#3; GAP-3555, GAP-3409, GAP-3407',
 'Resolve create versus update concurrency for party_ext and account_ext without guessing an initial ETag.',
 'RD-P1-006; staged rwb-source-data.yaml extension-facts operations; RWB-P1-E1018-APP and RWB-P1-E1069-DB.',
 '1. Existing rows require a GET of the current extension fact and its ETag before PUT. The service validates If-Match against that ETag and returns the published stale-version response on mismatch.\n2. The staged contract does not define a first-write precondition or a read operation that returns a row ETag. Do not synthesize an ETag or allow an unconditional first write. A first write remains disabled until the API contract owner publishes the create precondition and test fixture.\n3. The caller must have the product-specific write right from rwb-access and the case scope from rwb-case. The P1 service writes only the extension row and uses its existing audit path. Access-log persistence remains governed by RD-P1-091.\n4. GAP-3555, GAP-3409 and GAP-3407 remain open. The story may test the existing-row path against its fake; first-write completion stays blocked.',
 'RWB-P1-E1018-APP, RWB-P1-E1018-CON, RWB-P1-E1069-DB',
 'RWB-P1-E1018#3','GAP-3555, GAP-3409 and GAP-3407 remain open.'),
('RD-P1-095','Data-product access: access date, workload identities, field lists and catalog reconciliations',
 'E1016-APP#11; E1016-CON#8; GAP-3443, GAP-3445, GAP-3446',
 'Use a single business date and explicit service identity for the records access decision.',
 'RD-P1-021, RD-P1-024; RWB-P1-E1016-APP/CON v3; staged rwb-access.yaml and rwb-case.yaml; Architecture v5 workload identity rule.',
 '1. Both P1 and P4 evaluate data_product_access on the Asia/Bangkok business date supplied by the records request. The same caseId and request date are passed to the case-scope check and authorise call. No process substitutes the current wall-clock date after request validation. GAP-3443 closes.\n2. P1-to-P4 calls use the P1 workload identity. P1-to-P3 case-scope calls use the P1 workload identity. User identity and case ownership are passed only as contract fields, never as a service credential.\n3. The served field list is the intersection of the product's sourceViews, the published dictionary field rows and the fields allowed by the case scope. If any field or case-filter mapping is absent, fail closed and return no record values. GAP-3445 remains open until the per-product lists and non-key case filter are published.\n4. The catalog reconciliations property contains only codes with an explicit product mapping in the approved reconciliation catalog. No mapping means an empty array; do not infer REC codes from screen usage. GAP-3446 stays open with the data steward.',
 'RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P4-E1016-APP, RWB-P3-E1043-CON',
 'RWB-P1-E1016-APP#11; RWB-P1-E1016-CON#8',
 'Closes GAP-3443; GAP-3445 and GAP-3446 remain open.'),
('RD-P1-096','Dictionary and contract rows: object ownership, DC-ACE seed, smoke records, reference-load handler and applied version',
 'E1064-APP#3; E1064-APP#1, #2; E1064-CON#2; E1064-OPS#1; GAP-3338, GAP-3403; amends RD-P1-020',
 'Align dictionary object ownership and the DC-ACE contract seed with the loader ownership model.',
 'RD-P1-020 and RD-P1-071; Physical Schema v9 sys_objects/sys_fields seeds; RWB-P1-E1064-APP/CON/OPS v3; RWB-P1-AD018-APP v3.',
 '1. A service migration creates its own table and writes its sys_objects and sys_fields rows in the same migration transaction. The governed reference-data load updates values only for an existing object; it never creates sys_objects rows for another service. The table owner is the source of the object rows.\n2. The DC-ACE v1 DRAFT data_contract row is seeded by RWB-P1-E1001-APP with the actual contract_code, source_system, interface_id, contract_version and status values already present in the staged DC-ACE mapping. It remains DRAFT until the named owner approves it; the seed does not publish or grant access.\n3. Smoke tests use only synthetic DEV/SIT identities and rows created by the P1 seed step. Production smoke checks remain read-only and must not create test records.\n4. A governed reference load does not invent a missing sys_objects row. Missing object metadata fails the load before writes and is corrected by the owning migration. GAP-3338 closes for object creation ownership; GAP-3403 remains open for the unspecified smoke identity/value where no staged source supplies it.',
 'RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P1-AD018-APP',
 'RWB-P1-E1064-APP#3; RWB-P1-E1064-APP#1; RWB-P1-E1064-APP#2; RWB-P1-E1064-CON#2; RWB-P1-E1064-OPS#1',
 'GAP-3338 closes; GAP-3403 remains open pending a sourced smoke fixture.'),
('RD-P1-097','Account-page read used by rwb-case for the case list',
 'GAP-3274, GAP-3438',
 'Define the provider contract only from fields and behavior already published in the P1 source-data contract.',
 'RD-P1-024; API Specification v7 rwb-source-data.yaml; RWB-P1-E1015-CON and RWB-P1-E1018-APP/CON; GAP-3274 and GAP-3438.',
 '1. The account-page read is a P1-owned operation in rwb-source-data.yaml and is consumed by rwb-case through its published contract. Its response includes only the current account facts represented by the E1018 eligible-account activity contract, with page token and page size as the source contract publishes. It carries no case list or case ownership data.\n2. rwb-case applies its own case-to-account relationship and authorization. P1 does not return a list of accounts for arbitrary case scope and does not read rwb_case tables.\n3. The staged API specification does not yet give a complete account-page operation path, parameter schema, maximum page size and access/error mapping. Until those are published, rwb-case uses the existing listEligibleAccounts activity for the case-creation workflow and no new account-page client is built. GAP-3274 and GAP-3438 remain open.',
 'RWB-P1-E1015-CON, RWB-P1-E1018-APP, RWB-P1-E1018-CON, RWB-P3-E1043-CON',
 'GAP-3274; GAP-3438',
 'GAP-3274 and GAP-3438 remain open; new account-page consumption is deferred.'),
('RD-P1-098','Sandbox contract files and bootstrap: interim build',
 'E1065-CON#1; GAP-3481 to GAP-3486',
 'Give the sandbox build a deterministic, testable interim contract while platform-owned details remain pending.',
 'RD-P1-046; RWB-P1-E1065-CON/APP/DB v3; staged rwb-case.yaml optional asOf parameter; Physical Schema v9.',
 '1. The sandbox build uses the checked-in profile and shape files as versioned test inputs. Their exact property schemas, ten shape_id values, checksum scope and report file encoding are not published in the sources, so the build fails validation when these inputs are absent or malformed rather than guessing field values. GAP-3481 remains open.\n2. A build fake may supply the P3 list response and DEV workload identity. The real P3 read is not a build prerequisite until GAP-3482 is resolved.\n3. DEV database targets must match an explicit allow-list supplied by the pipeline. If no allow-list or target parameter is present, the build refuses to run. GAP-3483 remains open.\n4. View/grant application that requires privileged ACE schemas remains blocked until the platform DBA supplies the principal and execution location (GAP-3484). The release flag gates SIT/UAT/PROD per RD-P1-043.\n5. The human extraction role and credential remain platform-owned. The automated build can complete against the fake, but the human extraction test is not Done while GAP-3486 is open.',
 'RWB-P1-E1065-CON, RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-P1-E1069-DB',
 'RWB-P1-E1065-CON#1','GAP-3481 through GAP-3486 remain open with their stated owners; missing environment inputs fail closed.'),
('RD-P1-099','ACE additions: foreign-key delete rules, orphan rows and load order',
 'ACE001-DB#4; GAP-3576',
 'Set delete behavior and a safe row-level orphan policy from the staged ACE schema and database conventions.',
 'RWB-P1-ACE001-DB v3 AC15 and FK definitions; Physical Schema v9 ACE additions; PostgreSQL default referential behavior; RD-P1-025.',
 '1. All foreign keys in the ACE additions use RESTRICT unless the staged ACE additions sheet explicitly specifies a cascade. No staged source specifies cascade, so child records prevent parent deletion.\n2. The hearing-to-lawsuit relationship remains RESTRICT as well. Do not cascade a legal history delete.\n3. An input row whose referenced account or parent is absent is rejected as a row with a referential-integrity error; independent valid rows in the same file may continue. A failed database transaction rolls back that row only.\n4. The loader order follows the dependency graph of the declared foreign keys, parents before children. The ACE team lead confirms any source-system ordering that is not represented by those keys. GAP-3576 remains open only for that confirmation; the implementation interim is explicit.',
 'RWB-P1-ACE001-DB',
 'RWB-P1-ACE001-DB#4','GAP-3576 remains open for ACE team confirmation of source job ordering.'),
('RD-P1-100','Smaller rulings: snapshot, route ownership, holder fields, delivery status, EFS filtering and migration scope',
 'E1013-APP#2; AD018-OPS#1; E2034-APP#1; E1068-APP#1; E2001-APP#1; DM012-APP#1; DM013-APP#1, #2; DM014-APP#1, #2; GAP-3375, GAP-3327, GAP-3425, GAP-3384',
 'Close smaller cross-story conflicts while retaining pending items where a source does not supply the required field or route.',
 'RD-P1-002, RD-P1-007, RD-P1-020, RD-P1-024; staged E1013, AD018, E2034, E1068, E2001 and DM012-DM014 stories; API Specification v7; Physical Schema v9; Data Classification v6.',
 '1. snapshot(page) remains an architecture activity name, but E1013-APP does not provide it to reporting until the source fields, cursor and failure contract are agreed. Reporting uses its published REST reads meanwhile. GAP-3425 and GAP-3384 remain open and do not block the P1 workflow.\n2. SCR-44 route registration belongs to the platform gateway contract. AD018-OPS does not implement or smoke an unpublished composite route. The route owner must publish path, operations and errors before that route can be marked Done.\n3. Holder fields: CASE_ALLOCATED requires toHolderRef; CASE_TRANSFERRED requires fromHolderRef and toHolderRef; HANDOVER permits both; all other event codes reject holder fields. This follows the event semantics and the existing RD-P1-007 mapping.\n4. The E1068 activity response uses latestDeliveryStatus, selected by greatest occurredAt then greatest caseSeq for the same externalRef. The YAML property barcodeStatus is a stale name and must be corrected. GAP-3375 closes for the EFS selector: append only efs_ledger_outcome rows, using the matching business key, and exclude any row not selected by that ledger filter.\n5. DM012 keeps fields absent from DecisionRecord only in the migration extract; it does not add those fields to the decision library or event. Its AC1, BR2 and section 11 must say this.\n6. DM013 does not resolve write-offs by an absent write_off_key. It carries the source rows and leaves the Workbench decision-to-write-off match pending with the data architect; no amount or account heuristic is permitted. For scope, include the source rows selected by the mapping package and preserve closed-case records.\n7. DM014 covers all seven reference-data rows listed in section 9.4. The comparison against GET /admin/lists/{listCode} uses fields the contract actually publishes: version, validFrom and rows. P1 calculates row count and hash locally; it does not expect count or hash from the endpoint. Approval remains by the published rwb-case operation. GAP-3425, GAP-3384 and GAP-3327 remain open where the provider contract or complaint code is not published.',
 'RWB-P1-E1013-APP, RWB-P1-AD018-OPS, RWB-P1-E2034-APP, RWB-P1-E1068-APP, RWB-P1-E2001-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-DM014-APP',
 'RWB-P1-E1013-APP#2; RWB-P1-AD018-OPS#1; RWB-P1-E2034-APP#1; RWB-P1-E1068-APP#1; RWB-P1-E2001-APP#1; RWB-P1-DM012-APP#1; RWB-P1-DM013-APP#1; RWB-P1-DM013-APP#2; RWB-P1-DM014-APP#1; RWB-P1-DM014-APP#2',
 'GAP-3375 closes; GAP-3327, GAP-3425 and GAP-3384 remain open; DM013 write-off match remains pending.')
]

def decision_section(d):
    id,title,refs,question,sources,ruling,stories,findings,gaps=d
    return f"""## {id} · {title}

**Question.** {question}

**Sources.** {sources}.

**Precedence applied.** D-RCV-60 and Architecture v5 remain above RD-P1 decisions; these rulings apply where the existing register leaves an implementation choice. Existing schemas and published operations prevail over story-only field names.

**Ruling.**
{chr(10).join(str(i)+'. '+line for i,line in enumerate(ruling.split(chr(10)),1))}

**Affected services.** rwb-source-data and the named consumers.
**Affected stories.** {stories}.
**Affected documents.** The named P1 stories, API Specification v7, and the applicable register/gap rows.
**Findings settled.** {findings}.
**GAP/ASM.** {gaps}.
**Status.** Proposed – GPT-6 Luna (applied where the staged text is updated; otherwise interim ruling).
**Reuse note.** Apply this ruling to every named consumer and test; keep unresolved fields tied to their owner and stated interim.
**Values chosen without a source.** None. Where no source supports a value, the ruling leaves it pending or blocks the dependent behavior.

---

"""

batch='\n\n## RD-P1-089 · '+decision_defs[0][1]+'\n\n'
sections=[decision_section(d) for d in decision_defs]
staged_batch=base/'decisions'/'batch-E.md'
staged_batch.parent.mkdir(parents=True,exist_ok=True)
staged_batch.write_text(source.rstrip()+'\n\n'+'\n'.join(sections),encoding='utf-8',newline='\n')
# Add all 12 full texts after the recovered 14 in the working register draft.
reg=base/'Recovery Workbench P1 Decision Register v3 draft.md'
regtxt=reg.read_text(encoding='utf-8')
pending='## Batch E index entries awaiting ruling text'
assert pending in regtxt
regtxt=regtxt.replace(pending,'## Batch E recovered decision text, continuation\n\n'+''.join(sections)+'\n'+pending,1)
reg.write_text(regtxt,encoding='utf-8',newline='\n')
# Add decision rows while preserving the original v2 CSV rows and the recovered 14.
csvpath=base/'Recovery Workbench P1 Decision Register v3 draft.csv'
with csvpath.open(encoding='utf-8-sig',newline='') as f:
    rd=csv.DictReader(f); header=rd.fieldnames; rows=list(rd)
assert len(rows)==59
for d in decision_defs:
    id,title,refs,question,sources,ruling,stories,findings,gaps=d
    rows.append({
      'decision_id':id,'title':title,'final_ruling':' '.join(ruling.splitlines()),
      'affected_services':'rwb-source-data','affected_stories':stories,'affected_documents':'P1 staged stories; API Specification v7; applicable decision/gap register',
      'themes':'','findings':findings,'gap_asm':gaps,'amended_by':'','status':'Proposed – GPT-6 Luna (applied/interim)',
      'model':'gpt-6-luna','values_chosen_without_source':'None; unresolved source values remain pending.',
      'escalation_items':refs})
with csvpath.open('w',encoding='utf-8',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=header,lineterminator='\n',quoting=csv.QUOTE_ALL)
    wr.writeheader();wr.writerows(rows)
assert len(rows)==71 and len({r['decision_id'] for r in rows})==71
# The per-batch CSV uses the existing batch D header.
with (WORK.parent.parent/'24 P1 Developer Readiness v1'/'decisions'/'batch-D.csv').open(encoding='utf-8-sig',newline='') as f:
    batch_header=next(csv.reader(f))
batch_csv=base/'decisions'/'batch-E.csv'
with batch_csv.open('w',encoding='utf-8',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=batch_header,lineterminator='\n',quoting=csv.QUOTE_ALL)
    wr.writeheader()
    for d in decision_defs:
        id,title,refs,question,sources,ruling,stories,findings,gaps=d
        row={k:'' for k in batch_header}
        aliases={'decision_id':id,'title':title,'ruling':' '.join(ruling.splitlines()),'affected_services':'rwb-source-data',
                 'affected_stories':stories,'affected_documents':'P1 staged stories; API Specification v7; applicable register/gap rows',
                 'findings':findings,'gap_asm':gaps,'status':'Proposed – GPT-6 Luna','model':'gpt-6-luna','escalation_items':refs}
        row.update({k:v for k,v in aliases.items() if k in row})
        wr.writerow(row)
print('Completed rulings',len(decision_defs),'register rows',len(rows),'staged batch',staged_batch)
