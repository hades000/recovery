# Data model — RWB-E1-043

One new migration, two tables (spec §Data and migration, SPEC-RWB-E1-043-001, -004). Per D-RCV-47/D-RCV-48 (approved disposition, Jira `TB0001-1204` comment `1783253`, 2026-11-10), recovery tables live unqualified in the ACE schema `ace` (the connection's `currentSchema`) — no `${recoverySchema}` placeholder, no schema literal, no `createSchemas` — and every table/index name starts with the prefix `rwb_`: `rwb_reference_version`, `rwb_reference_row`. The trigger functions and triggers below are not table/sequence/index names (D-RCV-47 does not require a prefix on them); they stay unqualified and unprefixed, named only for the table they guard — Builder confirms at TASK-03 whether a collision in the shared `ace` schema requires renaming them too. The Flyway bean itself (own bean, own history table `flyway_schema_history_recovery`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `createSchemas(false)`) is built by RWB-E1-044 (PRE-4) and is not re-created here.

## 1. Migration file

`backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_043_reference_versions.sql`

`<seq>` is **not pre-allocated**: RWB-E1-043 is not listed in `docs/architecture/migration-merge-order-map.md`'s build-order table. Per D-RCV-28/D-RCV-34, the real 4-digit zero-padded sequence is the next free number taken at merge, never assigned ahead of time and never renumbered after apply. Line 1 of the file is `-- Story: RWB-E1-043`.

```sql
-- Story: RWB-E1-043
CREATE TABLE rwb_reference_version (
    id              uuid PRIMARY KEY,
    table_code      varchar(30)   NOT NULL,
    version_no      integer       NOT NULL,
    valid_from      date          NOT NULL,
    valid_to        date,
    status          varchar(15)   NOT NULL,
    author_user_id  uuid          NOT NULL,
    approver_user_id uuid,
    approved_at     timestamptz,
    row_count       integer       NOT NULL,
    content_hash    char(64)      NOT NULL,
    load_id         uuid          NOT NULL,
    created_at      timestamptz   NOT NULL DEFAULT now(),
    updated_at      timestamptz   NOT NULL DEFAULT now(),
    CONSTRAINT uq_reference_version_table_version UNIQUE (table_code, version_no),
    CONSTRAINT uq_reference_version_table_validfrom_hash UNIQUE (table_code, valid_from, content_hash),
    CONSTRAINT ck_reference_version_approver_not_author
        CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)
);

CREATE UNIQUE INDEX rwb_ux_reference_version_table_validfrom_approved
    ON rwb_reference_version (table_code, valid_from)
    WHERE status = 'APPROVED';

CREATE TABLE rwb_reference_row (
    id          uuid PRIMARY KEY,
    version_id  uuid NOT NULL REFERENCES rwb_reference_version (id),
    row_key     varchar(200) NOT NULL,
    row_data    jsonb NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now(),
    updated_at  timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_reference_row_version_key UNIQUE (version_id, row_key)
);

CREATE INDEX rwb_ix_reference_row_version_id ON rwb_reference_row (version_id);

-- Append-only: rwb_reference_row is never updated or deleted.
CREATE OR REPLACE FUNCTION reject_reference_row_change() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'rwb_reference_row is append-only: % not permitted', TG_OP;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reference_row_append_only
    BEFORE UPDATE OR DELETE ON rwb_reference_row
    FOR EACH ROW EXECUTE FUNCTION reject_reference_row_change();

-- rwb_reference_version: only status, approver_user_id, approved_at, valid_to and the standard
-- (created_at/updated_at) columns may change after insert; every other column is append-only.
CREATE OR REPLACE FUNCTION reject_reference_version_change() RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION 'rwb_reference_version rows are never deleted';
    END IF;
    IF NEW.table_code      IS DISTINCT FROM OLD.table_code
    OR NEW.version_no      IS DISTINCT FROM OLD.version_no
    OR NEW.valid_from      IS DISTINCT FROM OLD.valid_from
    OR NEW.author_user_id  IS DISTINCT FROM OLD.author_user_id
    OR NEW.row_count       IS DISTINCT FROM OLD.row_count
    OR NEW.content_hash    IS DISTINCT FROM OLD.content_hash
    OR NEW.load_id         IS DISTINCT FROM OLD.load_id THEN
        RAISE EXCEPTION 'rwb_reference_version is append-only except status, approver_user_id, approved_at, valid_to';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reference_version_append_only
    BEFORE UPDATE OR DELETE ON rwb_reference_version
    FOR EACH ROW EXECUTE FUNCTION reject_reference_version_change();
```

The trigger bodies above are the plan's lint-safe form under the new rule (D-RCV-47): every table/index name carries the `rwb_` prefix and none is schema-qualified; trigger and function names are left unprefixed and unqualified (D-RCV-47 scopes the prefix requirement to table, sequence and index names only — Builder confirms at TASK-03 whether a same-name collision in the shared `ace` schema forces a rename). No `SET search_path`, no bare schema literal. Builder re-confirms the exact Postgres syntax (notably `RAISE EXCEPTION` inside `BEFORE DELETE` and the `IS DISTINCT FROM` columns) against a running Testcontainers instance at TASK-03; this is plan-time design, not yet execution-verified.

## 2. Field rules (spec §Field-level behaviour matrix)

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `reference_version` | `table_code` | Load request | New row only | Must be in LOV-REF-TABLE |
| `reference_version` | `version_no` | Service | System-managed | One above the highest for the table; unique (table_code, version_no) |
| `reference_version` | `valid_from`, `valid_to` | Load request / approval | New row; `valid_to` set on approval | `valid_from` not before the business date; `valid_to` is the day before the next `valid_from` |
| `reference_version` | `status` | Service | VALIDATED → APPROVED → ROLLED_BACK | Never edited to any other value |
| `reference_version` | `author_user_id`, `approver_user_id`, `approved_at` | Session / approval | System-managed | Approver must differ from author |
| `reference_version` | `row_count`, `content_hash`, `load_id` | Service | System-managed | Hash is SHA-256 over rows sorted by key; unique (table_code, valid_from, content_hash) |
| `reference_row` | `row_key`, `row_data` | Load file | New row only | Unique (version_id, row_key); append-only |
| `reference_row` | all fields | — | Never updated | Update trigger refuses changes; a correction is a new version |

## 3. JPA entities (internal package, TASK-04)

```text
ReferenceVersionEntity(UUID id, String tableCode, int versionNo, LocalDate validFrom, LocalDate validTo,
                        ReferenceVersionStatus status, UUID authorUserId, UUID approverUserId,
                        OffsetDateTime approvedAt, int rowCount, String contentHash, UUID loadId)
ReferenceRowEntity(UUID id, UUID versionId, String rowKey, Map<String,Object> rowData)   // row_data: jsonb
ReferenceVersionStatus { VALIDATED, APPROVED, ROLLED_BACK }
```

`"in force"` is derived (status `APPROVED` and `valid_from` ≤ business date, latest such row), never stored (spec §Status-transition matrix).

Per D-RCV-47, `ReferenceVersionEntity` maps `@Table(name = "rwb_reference_version")` and `ReferenceRowEntity` maps `@Table(name = "rwb_reference_row")` — no `schema` attribute (unqualified, in the connection's `currentSchema` `ace`).

## 4. Catalog data this story reads but does not own

- LOV-REF-TABLE (13 table codes: PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER) — entry precondition, not seeded by this migration; owning story not named in spec.md (TASK-01 checks the row count exists before TASK-06/07 run).
- Column-schema catalog entries per table code (RWB-E1-042, CLAR-003) — read by `ReferenceTableSchemas`, not stored in this migration.
- `refdata.cache.ttl-seconds` (RWB-E1-042, DL11; 300 assumed) — read by `ReferenceRowCache`, not stored in this migration.

## 5. Frontend

`NOT_APPLICABLE`. No data model change (`Frontend Changes Required: NO`).
