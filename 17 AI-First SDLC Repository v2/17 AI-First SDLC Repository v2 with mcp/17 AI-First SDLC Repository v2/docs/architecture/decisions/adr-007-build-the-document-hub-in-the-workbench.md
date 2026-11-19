<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-007 Build the document hub in the Workbench

- Status: Accepted
- Date: 26 October 2026
- Deciders: CTO
- Decision log: DT06; storage pattern DL27; document types DL19

### Context and problem

Recovery runs on documents: contracts, notices, proofs of delivery, court papers, appraisals and titles. The choice was to index documents held in another store or to hold them in the Workbench.

### Decision drivers

- Documents found by case, type and date without manual filing
- Legal documents that cannot be altered
- Custody of originals tracked

### Options considered

1. A document hub built in the Workbench as the system of record
2. An index over an existing document store

### Decision

Option 1. Documents are stored in Blob storage with a write-once container for legal types, indexed by case, type, date and extracted fields, with retention classes and custody tracking.

### Consequences

- Good: one place for every recovery document, linked to its case.
- Bad: storage, backup, legal hold and e-discovery are in scope (DL27).

---
