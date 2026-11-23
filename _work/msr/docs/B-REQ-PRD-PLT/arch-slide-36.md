
Built for reuse: which services other workbenches can pick up

Why we cut by module: generic capabilities can be shared without taking the rest of Recovery

Ready to reuse as is (7)

Document hub
P5 · rwb-document

Communications
P6 · rwb-comms

Decision center & log
P7 · rwb-decision

Access & administration
P4 · rwb-access

Agent runtime
P10 · rwb-agent

Integration & files
P2 · rwb-integration

Reporting
P9 · rwb-reporting

Reusable with configuration (7)

Partner management
S9 · rwb-partner

Payments & posting
P8 · rwb-payment

Deviation handling
S8 · rwb-deviation

Valuation & route
S1 · rwb-valuation

Assets & auction
S5 · rwb-asset

Debt sale
S6 · rwb-debtsale

Source data
P1 · rwb-source-data

Recovery-specific (5)

Case & workflow
P3 · rwb-case

TDR, settlement, DIL
S2 · rwb-treatment

Guarantees
S3 · rwb-guarantee

Litigation & enforcement
S4 · rwb-litigation

Write-off & recovery
S7 · rwb-writeoff

What makes a service reusable
Contract first: OpenAPI, AsyncAPI, activity jar
Workbench ID on every call; no Recovery terms in generic APIs
Versioned: /v1, backward-compatible events, kit semver
Own schema, movable to its own server
Own task queue and Nexus endpoint
Configuration, not code: templates, DoA, rules as data

Example: ACE Collection could send notices through rwb-comms' Nexus endpoint without deploying anything new.

36

Notes: Assessment of reuse potential (for planning, not a commitment):

Ready to reuse as is: Document hub (P5), Communications (P6), Decision center and log with rule registry (P7), Access and administration (P4), Agent runtime (P10), Integration and files (P2), Reporting (P9). These have no Recovery-specific terms in their contracts.

Reusable with configuration: Partner management (S9), Payments and posting (P8), Deviation handling (S8), Valuation (S1), Assets and auction (S5), Debt sale (S6), Source data (P1, as a pattern for reading ACE).

Recovery-specific: Case and workflow (P3, the pattern is reusable), Treatment (S2), Guarantees (S3), Litigation (S4), Write-off (S7).

How another workbench reuses a service: call its REST API or activity contract, or its Nexus endpoint from another namespace; or deploy its own instance with its own schema and configuration.

