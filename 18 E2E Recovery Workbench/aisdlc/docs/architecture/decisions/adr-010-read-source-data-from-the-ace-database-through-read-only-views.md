<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-010 Read source data from the ACE database through read-only views

- Status: Accepted
- Date: 15 November 2026
- Deciders: the recovery tech lead with the data architect; the ACE team lead for RWB-ACE-001 and DL43
- Decision log: D-RCV-35 (U1 to U4); supersedes ADR-005

### Context and problem

The design built a second copy of account, customer, payment, party, contact, collateral, valuation, asset, collections, product and score data in the recovery schema, and filled it with eleven copy tables and nine load tables. ACE already ingests those records and owns them. Two copies of one account row disagree over time, and the Workbench maintains the copy that nothing else reads. The question is where source data lives and how the recovery module reaches it.

### Decision drivers

- One copy of source data, held by the team that already ingests it
- No inbound interface or second load estate for the Workbench to build and run
- A boundary the database enforces, not only code review
- Case history that a change in a source system cannot delete

### Options considered

1. Read source data from the ACE database through `recovery.v_ace_*` views, SELECT only
2. Keep the copy tables in the recovery schema and load them (ADR-005)
3. Read the ACE `public` tables directly from the recovery module

### Decision

Option 1. The recovery module reads source data from the ACE database through `recovery.v_ace_*` views. It does not load, copy or transform source data. The views are SELECT only and owned by a dedicated role that holds SELECT on the ACE tables; the recovery service identity holds SELECT on the views and on nothing else, so a direct read of a `public` table fails in the catalog.

- 30 views in two migrations: 16 over ACE tables that exist today, shipped with RWB-E1-069 as the next free sequence after the V0001 baseline; 14 over the Tier 2 additions, shipped the week RWB-ACE-001 lands. Until then the features that need them stay behind their flags.
- The ACE team owns every table and column the views read, raised once in RWB-ACE-001. The Workbench owns only its four extension tables, keyed by ACE business keys.
- No foreign key from a `recovery` table into `public`, because ACE uses ON DELETE CASCADE on `account`. A link to a source record is a business-key column with no foreign key.

### Consequences

- Good: one copy of source data. There is no Workbench copy to reconcile, correct or retire.
- Good: no inbound load, data quality or tracker estate to build and run; 20 tables leave the schema.
- Good: the view list is the contract between the two teams, so a change to a source column is an ACE change with a named owner.
- Bad: the Workbench cannot start before the ACE additions land (DL43).
- Bad: there is no tokenization at load, so masking moves into the views and to E1-037 at the API, and every read of personal data is audited.
- Bad: a view that reads a changed ACE column breaks at deploy, so the view conformance test runs in the pipeline.

---
