---
id: hybrid
title: 3.5 Hybrid programmes
description: "Apply the paths at increment level, not programme level."
sidebar_label: 3.5 Hybrid programmes
---

:::note Section summary
Apply the paths at increment level, not programme level.
:::

A programme may combine greenfield, brownfield, integration and modernisation work. The lifecycle
paths should therefore be applied at **increment level**. One programme may create a new customer
journey, enhance an existing service, modernise a component and integrate a reusable capability at
the same time.

Each increment should record:

* its path
* its starting context
* reused artefacts
* applicable activities (the lifecycle tailoring record)
* human approvals
* its rollback route

so that programme-level labels do not hide different delivery risks.

```text
Programme X
├── INC-001  New customer journey        Greenfield       full lifecycle
├── INC-002  Enhance payments service    Brownfield       reuse PRD v2.1, Spec-Clarify onwards
├── INC-003  Modernise notification hub  Modernisation    ADRs, coexistence, rollback plan
└── INC-004  Integrate KYC capability    Integration      contract-first spec, API testing
```

The toolkit's increment card (`.github/templates/increment-card-template.md`) is designed to hold
exactly this record, one file per increment under `docs/increments/`.
