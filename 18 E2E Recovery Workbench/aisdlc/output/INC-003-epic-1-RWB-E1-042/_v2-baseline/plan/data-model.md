# Data model — RWB-E1-042

Schema: `recovery` (via `${recoverySchema}`). Migration: `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`.

## `parameter_catalog`

| Column | Type | Null | Constraint |
|---|---|---|---|
| `param_key` | varchar(120) | no | PK; lower-case dotted key |
| `kind` | varchar(20) | no | `BUSINESS` or `ENVIRONMENT` |
| `value_type` | varchar(20) | no | `INTEGER`, `DECIMAL`, `STRING`, `BOOLEAN`, `DURATION`, `SECRET` |
| `unit` | varchar(20) | yes | e.g. `DAYS`, `PERCENT`, `THB` |
| `min_value` | numeric(18,4) | yes | inclusive |
| `max_value` | numeric(18,4) | yes | inclusive |
| `default_value` | text | yes | used only when not required |
| `scope` | varchar(20) | no | `GLOBAL` or `PRODUCT` |
| `required` | boolean | no | default false |
| `owner_role` | varchar(40) | no | role code |
| `environments` | text[] | no | subset of DEV/SIT/UAT/PROD |
| `used_by` | text | yes | story/component list |
| `secret` | boolean | no | default false; value never served |
| `description` | text | yes | business meaning |

PK (`param_key`). Check: `kind in ('BUSINESS','ENVIRONMENT')`; `value_type in (...)`;
`min_value <= max_value` when both present; `not secret or default_value is null`.

## `parameter_value`

| Column | Type | Null | Constraint |
|---|---|---|---|
| `id` | uuid | no | PK, `gen_random_uuid()` |
| `param_key` | varchar(120) | no | FK → `parameter_catalog.param_key` |
| `environment` | varchar(10) | no | `DEV`, `SIT`, `UAT`, `PROD` |
| `product_group` | varchar(15) | yes | null for GLOBAL |
| `param_value` | text | no | stored as text; typed on read |
| `version_no` | integer | no | 1..n per key/environment/product |
| `valid_from` | date | no | inclusive |
| `valid_to` | date | yes | exclusive; null = open |
| `status` | varchar(20) | no | `VALIDATED`, `APPROVED`, `ROLLED_BACK` |
| `author_user_id` | uuid | no | loader |
| `approver_user_id` | uuid | yes | must differ from author |
| `approved_at` | timestamptz | yes | set on approval |

Unique: (`param_key`, `environment`, coalesce(`product_group`,'*'), `version_no`).
Index: (`param_key`, `environment`, `product_group`, `valid_from` desc).
Check: `status in ('VALIDATED','APPROVED','ROLLED_BACK')`; `valid_to is null or valid_to > valid_from`;
`approver_user_id is null or approver_user_id <> author_user_id`.

## Resolution rule

For a read at business date `d`:
1. Filter `environment`, `param_key`, and `product_group` (product row wins over global).
2. Filter `status = 'APPROVED'` and `valid_from <= d` and (`valid_to is null` or `d < valid_to`).
3. Order by `valid_from desc, version_no desc`; take the first.
4. If none, use `default_value` when the parameter is not required.
5. Return value, `version_no`, `valid_from`, `unit`, `secret`.

## Bootstrap rows

`config/parameter-catalog.csv`: 13 original rows plus six v2 rows (`temporal.*`, `drools.*`,
`rules.testcases.min`). `config/messages-e1-042.csv`: the fixed text for the temporary resolver.

## Baseline overlap

V0001 already creates both tables from Physical Schema v6. V0042 uses `CREATE TABLE IF NOT EXISTS` and
`DO` blocks to add only missing constraints, FKs and indexes. The verification applies V0042 on top of
a simulated V0001 and confirms no error.
