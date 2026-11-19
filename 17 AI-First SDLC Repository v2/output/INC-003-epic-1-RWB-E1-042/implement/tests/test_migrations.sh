#!/usr/bin/env bash
# RWB-E1-042 migration verification. Runs inside the PostgreSQL container.
set -euo pipefail

PSQL="psql -v ON_ERROR_STOP=1 -U postgres -d rwb"
SQL_DIR="/work/sql"

q() { $PSQL -tA -c "$1"; }

assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: $label expected [$expected] got [$actual]"
        exit 1
    fi
    echo "ok: $label = $actual"
}

expect_fail() {
    local label="$1" sql="$2"
    if $PSQL -q -c "$sql" >/dev/null 2>&1; then
        echo "FAIL: $label unexpectedly succeeded"
        exit 1
    fi
    echo "ok: $label refused"
}

run_file() {
    local schema="$1" file="$2"
    sed "s/\${recoverySchema}/$schema/g" "$SQL_DIR/$file" | $PSQL -q
}

echo "== 1. Consolidated migration on a clean schema =="
$PSQL -q -c "DROP SCHEMA IF EXISTS clean CASCADE; CREATE SCHEMA clean;"
run_file clean "V0042__rwb_e1_042_parameter_catalog_and_seed.sql"
assert_eq "catalog rows" 13 "$(q 'SELECT count(*) FROM clean.parameter_catalog')"
assert_eq "value rows" 28 "$(q 'SELECT count(*) FROM clean.parameter_value')"
assert_eq "parameter_value constraints" 9 "$(q "SELECT count(*) FROM pg_constraint WHERE conrelid = 'clean.parameter_value'::regclass AND conname IN ('uk_parameter_value','ck_parameter_value_environment','ck_parameter_value_status','ck_parameter_value_dates','ck_parameter_value_version','ck_parameter_value_maker_checker','ck_parameter_value_approved_at','fk_parameter_value_catalog','parameter_value_pkey')")"
assert_eq "E1-042 indexes" 4 "$(q "SELECT count(*) FROM pg_indexes WHERE schemaname = 'clean' AND tablename IN ('parameter_catalog','parameter_value') AND indexname IN ('ix_parameter_value_in_force','ix_parameter_value_lookup','ux_parameter_value_version_all','ux_parameter_value_approved_from')")"

echo "== 2. Re-run is idempotent =="
run_file clean "V0042__rwb_e1_042_parameter_catalog_and_seed.sql"
assert_eq "catalog rows after re-run" 13 "$(q 'SELECT count(*) FROM clean.parameter_catalog')"
assert_eq "value rows after re-run" 28 "$(q 'SELECT count(*) FROM clean.parameter_value')"

echo "== 3. Split review files on a clean schema =="
$PSQL -q -c "DROP SCHEMA IF EXISTS split CASCADE; CREATE SCHEMA split;"
run_file split "V042_1__parameter_catalog.sql"
run_file split "V042_2__parameter_seed.sql"
assert_eq "split catalog rows" 13 "$(q 'SELECT count(*) FROM split.parameter_catalog')"
assert_eq "split value rows" 28 "$(q 'SELECT count(*) FROM split.parameter_value')"

echo "== 4. E1-001 baseline overlap (tables already exist) =="
$PSQL -q -c "DROP SCHEMA IF EXISTS baseline CASCADE; CREATE SCHEMA baseline;"
$PSQL -q <<'SQL'
CREATE TABLE baseline.parameter_catalog (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    param_key varchar(100) NOT NULL,
    kind varchar(15) NOT NULL,
    value_type varchar(15) NOT NULL,
    unit varchar(20),
    min_value varchar(40),
    max_value varchar(40),
    default_value varchar(400),
    scope varchar(10) NOT NULL DEFAULT 'GLOBAL',
    required boolean NOT NULL DEFAULT false,
    owner_role varchar(20) NOT NULL,
    environments varchar(40),
    used_by varchar(400),
    secret boolean NOT NULL DEFAULT false,
    description varchar(400) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_parameter_catalog UNIQUE (param_key)
);
CREATE TABLE baseline.parameter_value (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    param_key varchar(100) NOT NULL,
    environment varchar(4) NOT NULL,
    param_value varchar(400) NOT NULL,
    product_group varchar(15),
    version_no integer NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    status varchar(15) NOT NULL DEFAULT 'VALIDATED',
    author_user_id uuid NOT NULL,
    approver_user_id uuid,
    approved_at timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_parameter_value UNIQUE (param_key, environment, product_group, version_no)
);
SQL
run_file baseline "V042_1__parameter_catalog.sql"
run_file baseline "V042_2__parameter_seed.sql"
assert_eq "baseline catalog rows" 13 "$(q 'SELECT count(*) FROM baseline.parameter_catalog')"
assert_eq "baseline value rows" 28 "$(q 'SELECT count(*) FROM baseline.parameter_value')"
assert_eq "baseline added FK" 1 "$(q "SELECT count(*) FROM pg_constraint WHERE conrelid = 'baseline.parameter_value'::regclass AND conname = 'fk_parameter_value_catalog'")"
assert_eq "baseline added checks" 5 "$(q "SELECT count(*) FROM pg_constraint WHERE conrelid = 'baseline.parameter_catalog'::regclass AND conname LIKE 'ck_parameter_catalog_%'")"

echo "== 5. Negative database tests =="
expect_fail "duplicate global version with NULL product_group" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, status, author_user_id, approver_user_id, approved_at) VALUES ('case.entry.dpd','DEV','90',NULL,1,'2026-11-30','APPROVED',gen_random_uuid(),NULL,now());"

expect_fail "maker-checker on approve" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, status, author_user_id, approver_user_id, approved_at) VALUES ('case.entry.dpd','SIT','91',NULL,2,'2026-12-01','APPROVED','11111111-1111-1111-1111-111111111111','11111111-1111-1111-1111-111111111111',now());"

expect_fail "secret with a default value" \
"UPDATE clean.parameter_catalog SET default_value = 'not-allowed' WHERE param_key = 'ace.db.password';"

expect_fail "value for an unknown key" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, status, author_user_id, approver_user_id, approved_at) VALUES ('no.such.key','DEV','1',NULL,1,'2026-12-01','APPROVED',gen_random_uuid(),NULL,now());"

expect_fail "APPROVED row without approved_at" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, status, author_user_id, approver_user_id, approved_at) VALUES ('case.entry.dpd','UAT','91',NULL,2,'2026-12-01','APPROVED',gen_random_uuid(),NULL,NULL);"

expect_fail "valid_to before valid_from" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, valid_to, status, author_user_id, approver_user_id, approved_at) VALUES ('case.entry.dpd','UAT','91',NULL,3,'2026-12-01','2026-11-01','VALIDATED',gen_random_uuid(),NULL,NULL);"

expect_fail "second approved version at the same valid_from" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, status, author_user_id, approver_user_id, approved_at) VALUES ('case.entry.dpd','PROD','91',NULL,2,'2026-11-30','APPROVED',gen_random_uuid(),gen_random_uuid(),now());"

expect_fail "invalid environment" \
"INSERT INTO clean.parameter_value (param_key, environment, param_value, product_group, version_no, valid_from, status, author_user_id, approver_user_id, approved_at) VALUES ('case.entry.dpd','QA','91',NULL,4,'2026-12-01','VALIDATED',gen_random_uuid(),NULL,NULL);"

echo "== 6. Deployment guard catches a required key with no value =="
$PSQL -q -c "DROP SCHEMA IF EXISTS guardtest CASCADE; CREATE SCHEMA guardtest;"
run_file guardtest "V0042__rwb_e1_042_parameter_catalog_and_seed.sql"
$PSQL -q -c "INSERT INTO guardtest.parameter_catalog (param_key, kind, value_type, owner_role, description, required, scope, environments) VALUES ('test.required.missing','BUSINESS','STRING','RW-COE','guard test',true,'GLOBAL','DEV,SIT,UAT,PROD');"
if run_file guardtest "V042_2__parameter_seed.sql" >/dev/null 2>&1; then
    echo "FAIL: deployment guard did not reject a required key with no value"
    exit 1
fi
echo "ok: deployment guard refused a required key with no value"

echo
echo "ALL MIGRATION TESTS PASSED"
