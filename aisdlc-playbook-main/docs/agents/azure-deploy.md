---
id: azure-deploy
title: A.10 Azure-Deploy
description: "Prepares, validates and executes an approved deployment to Azure after quality, security and readiness checks."
sidebar_label: A.10 Azure-Deploy
---

:::note Section summary
Prepares, validates and executes an approved deployment to Azure after quality, security and readiness checks.
:::

**Type:** Core · **Lifecycle group:** Quality and release · **Phase:** 9 Release · **Source:** HVE Core All extension (`azure-prepare` → `azure-validate` → `azure-deploy`)

Azure-Deploy supports the final delivery sequence by preparing deployment artefacts, validating
configuration and executing an approved deployment to Azure. It should be used only after the
release candidate has passed the required quality, security and readiness checks. Release approval
and production deployment authority remain with the named human roles.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| Only after release readiness and required approvals. | Approved release candidate, environment configuration and deployment controls. | Deployment package, deployed version and logs. | Release and deployment approvals remain with the named human authorities. **Gates:** release readiness (FDE), deployment approval (PO/PM). |

## The pipeline

| Step | Purpose |
|---|---|
| `azure-prepare` | Assemble the deployment package and environment configuration for the target stage. |
| `azure-validate` | Validate configuration, dependencies and controls before any change is applied. |
| `azure-deploy` | Execute the approved deployment and capture logs and the deployed version. |

Promotion follows the GreenLane CI/CD path DEV → SIT → QA → PROD, each promotion with its own
approval.

## Limitations and stop conditions

* No autonomous production promotion. A named human approves each deployment.
* Stops when validation fails, when the release candidate lacks quality or security evidence, or
  when the rollback route recorded in the increment card is not available.
* Deployment logs are retained as release evidence and linked from the increment card.
