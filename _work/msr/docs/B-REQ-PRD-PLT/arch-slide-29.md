
Data: one ACE database, one schema and one login per service

Ownership is enforced by grants, not by separate servers

rwb-case

login rwb_case

schema rwb_case: read and write

rwb-source-data

login rwb_source_data

recovery.v_ace_* views: SELECT only

rwb-litigation

login rwb_litigation

schema rwb_payment: no grant, refused

ACE POSTGRESQL SERVER · PgBouncer pool and connection cap per login

ACE-OWNED

ACE schemas: customer, account, payment, collateral, …

schema recovery: 30 v_ace_* views, SELECT only, for rwb_source_data

19 RECOVERY SCHEMAS · ONE LOGIN EACH

rwb_case

rwb_decision

rwb_access

rwb_deviation

rwb_valuation

rwb_treatment

rwb_guarantee

rwb_litigation

rwb_asset

rwb_debtsale

rwb_writeoff

rwb_document

rwb_comms

rwb_payment

rwb_partner

rwb_integration

rwb_source_data

rwb_reporting

rwb_agent

Temporal persistence: own database

Blob storage with WORM: documents (rwb-document only)

Own schema only
one login per service; grants on its own schema

No cross-schema joins or keys
hold IDs; ask the owner through its contract

Capped connections
PgBouncer pool per login protects ACE

Checked in every build
boundary test fails on a cross-schema reference

Own migrations
Flyway per service, in its own pipeline

Movable later
a schema can move to its own server: change the connection string

Same ACE database, clear ownership: a service writes only its own schema, and only rwb-source-data reads ACE's views.

29

Notes: Physical: the ACE PostgreSQL server (Azure Database for PostgreSQL). ACE's own schemas, plus schema recovery holding the 30 read-only v_ace_* views (ADR-010), plus 19 Recovery schemas rwb_<service>. Temporal keeps its persistence in its own database; documents are in Blob with WORM.

Rules: each service has one database login that owns its schema and has no grant on any other schema; only rwb_source_data has SELECT on the views. No cross-schema joins, views or foreign keys: services hold each other's IDs and use contracts for everything else. Each service runs its own Flyway migrations. A boundary test in every build fails on any cross-schema reference.

Protecting ACE: each login goes through its own PgBouncer pool with a connection cap and statement timeout; heavy reporting runs from rwb-reporting's own projections, not from ACE tables. Per-schema monitoring.

This is the schema-per-service variant of database per service (microservices.io): ownership and isolation are kept, and any schema can later move to its own server by changing its connection string, with no code change.

