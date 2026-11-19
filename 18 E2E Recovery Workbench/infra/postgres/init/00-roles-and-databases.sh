#!/bin/sh
# Local only. Creates the roles and databases of the ACE database estate on one Postgres server.
#
#   ace                  ACE database: schema public (ACE team) and schema recovery (Workbench)
#   temporal             Temporal persistence, owned by temporal_svc, no grant on ace (ADR-011)
#   temporal_visibility  Temporal visibility, owned by temporal_svc
#
# Roles (ADR-010, ADR-011):
#   rwb_migrator    runs recovery Flyway, owns the recovery tables; holds USAGE on schema public
#                   and a non-inheriting ace_view_owner membership, no table privilege (D-RUN-14)
#   recovery_svc    the recovery service identity: DML on recovery tables, SELECT on v_ace_* views,
#                   no privilege in public
#   ace_view_owner  owns the v_ace_* views, holds SELECT on the ACE public tables, cannot log in;
#                   granted to rwb_migrator WITH INHERIT FALSE, SET TRUE (D-RUN-14)
#   temporal_svc    owns the two Temporal databases, cannot connect to ace
set -eu

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<SQL
CREATE ROLE rwb_migrator   LOGIN PASSWORD '${RWB_MIGRATOR_PASSWORD}';
CREATE ROLE recovery_svc   LOGIN PASSWORD '${RECOVERY_SVC_PASSWORD}';
CREATE ROLE ace_view_owner NOLOGIN;
CREATE ROLE temporal_svc   LOGIN PASSWORD '${TEMPORAL_SVC_PASSWORD}';

CREATE DATABASE ace;
CREATE DATABASE temporal            OWNER temporal_svc;
CREATE DATABASE temporal_visibility OWNER temporal_svc;

REVOKE CONNECT ON DATABASE ace, temporal, temporal_visibility FROM PUBLIC;
GRANT  CONNECT ON DATABASE ace TO rwb_migrator, recovery_svc;
GRANT  CONNECT ON DATABASE temporal, temporal_visibility TO temporal_svc;

ALTER ROLE recovery_svc SET search_path = recovery;
ALTER ROLE rwb_migrator SET search_path = recovery;
SQL
