
A9 · Standards we apply: recognised by the bank's architects and auditors

Every design choice in this deck points back to one of these

| Standard | What it gives us |
|---|---|
| BIAN Service Landscape v14 | Bank-standard names and boundaries for business capabilities (service domains) |
| Domain-Driven Design: bounded contexts | One model, one owner, one data store per context |
| microservices.io patterns | Decompose by capability; schema per service (a database-per-service variant); saga; transactional outbox; API composition; CQRS; anti-corruption layer |
| NIST SP 800-204, 204A, 204B, 204C | Security for microservices; service mesh; attribute-based access; DevSecOps |
| OWASP API Security Top 10 (2023) | API threat checklist, especially object-level authorisation |
| FAPI 2.0 Security Profile (final Feb 2025) | Partner API security with sender-constrained tokens |
| OpenAPI 3.1 · AsyncAPI 3.x · CloudEvents 1.0 | Machine-readable contracts for REST and events; CNCF event envelope |
| OpenTelemetry · W3C Trace Context | One trace across services, events and workflows (baseline Req 10) |
| OMG DMN 1.6 | Business-readable, executable decision models; Drools conformance level 3 |
| Azure Well-Architected · AKS microservices reference | Platform, scaling, resilience patterns (circuit breaker, bulkhead, claim-check) |
| Temporal durable execution | Long-running business processes as code; used in banking (ANZ home loans, JPMorgan Chase payments) |


49

Notes: Verified 19 Nov 2026 against primary sources (URLs in the references slide).

BIAN: release 14.0 (Feb 2026); service domains are elemental, mutually exclusive and collectively exhaustive business capabilities - a direct basis for service boundaries.
microservices.io (Chris Richardson): decomposition by business capability and subdomain; data patterns.
NIST SP 800-204 (Aug 2019), 204A service mesh (May 2020), 204B ABAC (Aug 2021), 204C DevSecOps (Mar 2022); 204D software supply chain (Feb 2024) also relevant to pipelines.
FAPI 2.0 Security Profile approved Final 19 Feb 2025. OAuth 2.1 is still an IETF draft, so we cite FAPI 2.0 as the binding profile.
CloudEvents graduated in CNCF Jan 2024. AsyncAPI 3.1 is current. W3C Trace Context Level 1 is a Recommendation (Nov 2021).
DMN 1.6 formal Sep 2026; Apache KIE Drools supports DMN at conformance level 3 and DMN 1.6 since 10.2.0. Note XLS decision tables are a Drools-native format, separate from DMN.
Temporal: ANZ case study (home-loan origination); JPMorgan Chase talk at Replay 2024 (payments modernisation).

