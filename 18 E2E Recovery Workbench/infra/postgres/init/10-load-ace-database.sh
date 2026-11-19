#!/bin/sh
# Local only. Builds the ace database from the document set v14 sources in /schema:
#
#   01-ace-schema-v1.sql                 ACE public schema (62 tables). The ACE team owns it.
#   02-ace-tier2-probe.sql               Probe DDL for the RWB-ACE-001 Tier 2 additions (14 tables,
#                                        12 columns). Not a deliverable; the ACE team owns the real
#                                        change. RWB_ACE_TIER2_PROBE=false leaves it out, and the 14
#                                        Tier 2 views then fail to compile, as they would in SIT today.
#   03-recovery-physical-schema-v6.sql   Recovery Physical Schema v6: 93 tables, 30 views, dictionary
#                                        and seed reference data. Stands in for V0001-V0003 until
#                                        RWB-E1-001 ships them as Flyway migrations. Set
#                                        RWB_LOAD_REFERENCE_SCHEMA=false once it does, and Flyway
#                                        builds the schema instead.
set -eu

run() {
  echo "rwb-init: applying $1"
  psql -v ON_ERROR_STOP="$2" --quiet --username "$POSTGRES_USER" --dbname ace -f "/schema/$1"
}

run 01-ace-schema-v1.sql 1

if [ "${RWB_ACE_TIER2_PROBE:-true}" = "true" ]; then
  run 02-ace-tier2-probe.sql 1
  strict=1
else
  echo "rwb-init: RWB_ACE_TIER2_PROBE=false, Tier 2 views will not compile"
  strict=0
fi

if [ "${RWB_LOAD_REFERENCE_SCHEMA:-true}" = "true" ]; then
  run 03-recovery-physical-schema-v6.sql "$strict"
else
  echo "rwb-init: RWB_LOAD_REFERENCE_SCHEMA=false, recovery schema left to Flyway"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ace \
    -c "CREATE SCHEMA IF NOT EXISTS recovery; CREATE EXTENSION IF NOT EXISTS pgcrypto;"
fi

echo "rwb-init: applying ownership and grants"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ace -f /docker-entrypoint-initdb.d/20-grants.sql.inc

psql --username "$POSTGRES_USER" --dbname ace -tAc "
  SELECT 'rwb-init: public tables='   || count(*) FILTER (WHERE table_schema = 'public'   AND table_type = 'BASE TABLE')
      || ', recovery tables='         || count(*) FILTER (WHERE table_schema = 'recovery' AND table_type = 'BASE TABLE')
      || ', v_ace views='             || count(*) FILTER (WHERE table_schema = 'recovery' AND table_type = 'VIEW' AND table_name LIKE 'v\_ace\_%')
  FROM information_schema.tables"
