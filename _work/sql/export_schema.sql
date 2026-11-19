\pset pager off
\pset format unaligned
\pset tuples_only on
\o /tmp/schema_objects.json
select json_agg(x) from (
 select c.relname as name, case c.relkind when 'r' then 'table' when 'v' then 'view' end as kind,
        obj_description(c.oid) as comment
 from pg_class c join pg_namespace n on n.oid=c.relnamespace
 where n.nspname='recovery' and c.relkind in ('r','v')) x;
\o /tmp/schema_columns.json
select json_agg(x) from (
 select table_name, column_name, data_type, udt_name, is_nullable, column_default,
        character_maximum_length, numeric_precision, numeric_scale, ordinal_position,
        col_description((quote_ident(table_schema)||'.'||quote_ident(table_name))::regclass, ordinal_position) as comment
 from information_schema.columns where table_schema='recovery') x;
\o /tmp/schema_fks.json
select json_agg(x) from (
 select tc.table_name, kcu.column_name, ccu.table_name as ref_table, ccu.column_name as ref_column
 from information_schema.table_constraints tc
 join information_schema.key_column_usage kcu
   on kcu.constraint_name=tc.constraint_name and kcu.table_schema=tc.table_schema
 join information_schema.constraint_column_usage ccu
   on ccu.constraint_name=tc.constraint_name and ccu.table_schema=tc.table_schema
 where tc.constraint_type='FOREIGN KEY' and tc.table_schema='recovery') x;
\o /tmp/schema_indexes.json
select json_agg(x) from (select tablename, indexname, indexdef from pg_indexes where schemaname='recovery') x;
\o /tmp/schema_triggers.json
select json_agg(x) from (
 select event_object_table as table_name, trigger_name, event_manipulation, action_timing
 from information_schema.triggers where trigger_schema='recovery') x;
\o /tmp/schema_sysobjects.json
select json_agg(x) from (select object_name, business_name, subject_area, data_product, system_of_record, description from recovery.sys_objects order by object_name) x;
\o /tmp/schema_sysfields.json
select json_agg(x) from (select field_id, object_name, field_name, data_type, physical_type, is_mandatory, is_personal, source_system, source_field, description from recovery.sys_fields order by field_id) x;
\o /tmp/schema_products.json
select json_agg(x) from (select * from recovery.data_product order by product_code) x;
\o
