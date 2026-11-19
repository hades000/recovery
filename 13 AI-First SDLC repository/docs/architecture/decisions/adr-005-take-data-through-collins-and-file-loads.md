<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->

# ADR-005 Take data through COLLINS and file loads

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT and the ACE team
- Decision log: DT12; real-time needs DL06; legacy scope DL12

### Context and problem

The Workbench needs account, customer, collections, litigation, collateral, valuation and asset data. ACE takes its data through COLLINS by end of day batch. Collateral, appraisals and assets are not in COLLINS today.

### Decision drivers

- One way in for data, with checks
- No new direct interfaces to legacy systems
- A known age for every input to a decision

### Options considered

1. COLLINS daily batch, plus file loads for sources COLLINS does not carry
2. Direct real-time interfaces to each system of record
3. Events for every source

### Decision

Option 1. No component calls a system of record directly. Each load is checked for business date, structure, control totals, keys and references, and is refused whole if it fails. Every loaded record carries its business date.

### Consequences

- Good: one path in, one set of checks, no legacy enhancement.
- Bad: decisions use end of day data, and collateral, appraisals and assets arrive weekly or monthly. Same-day needs are named under DL06.

---
