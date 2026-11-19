\pset footer off
\x on
select * from recovery.v_data_dictionary where field='days_past_due';
\x off
select table_name, count(*) cols from information_schema.columns where table_schema='recovery' and table_name in ('party_ext','contact_point_ext','account_ext','valuation_ext') group by 1;
select 'ext fields in sys_fields', count(*) from recovery.sys_fields where object_name like '%\_ext';
select 'v_ace fields in sys_fields', count(*) from recovery.sys_fields where object_name like 'v\_ace\_%';
select 'v_ace actual cols', count(*) from information_schema.columns where table_schema='recovery' and table_name like 'v\_ace\_%';
-- objects not in sys_objects / sys_objects not real
select 'rel missing from sys_objects', string_agg(c.relname, ',') from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='recovery' and c.relkind in ('r','v') and c.relname not in (select object_name from recovery.sys_objects);
select 'sys_objects not a relation', string_agg(object_name, ',') from recovery.sys_objects where object_name not in (select c.relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='recovery');
-- columns vs sys_fields
select 'cols missing from sys_fields', count(*), string_agg(table_name||'.'||column_name, ', ' ) filter (where true) from (select table_name, column_name from information_schema.columns where table_schema='recovery' and table_name in (select object_name from recovery.sys_objects) except select object_name, field_name from recovery.sys_fields) x;
select 'sys_fields not a column', count(*), string_agg(object_name||'.'||field_name, ', ') from (select object_name, field_name from recovery.sys_fields except select table_name, column_name from information_schema.columns where table_schema='recovery') x;
-- physical_type mismatch for v_ace views
select 'v_ace physical_type mismatches', count(*) from recovery.sys_fields f join information_schema.columns c on c.table_schema='recovery' and c.table_name=f.object_name and c.column_name=f.field_name where f.object_name like 'v\_ace\_%' and f.physical_type <> case when c.data_type='character varying' then 'varchar('||coalesce(c.character_maximum_length::text,'')||')' when c.data_type='numeric' and c.numeric_precision is not null then 'numeric('||c.numeric_precision||','||c.numeric_scale||')' else c.data_type end;
select f.object_name, f.field_name, f.data_type, f.physical_type, c.data_type actual, c.character_maximum_length len, c.numeric_precision p, c.numeric_scale s from recovery.sys_fields f join information_schema.columns c on c.table_schema='recovery' and c.table_name=f.object_name and c.column_name=f.field_name where f.object_name like 'v\_ace\_%' and f.physical_type <> case when c.data_type='character varying' then 'varchar('||coalesce(c.character_maximum_length::text,'')||')' when c.data_type='numeric' and c.numeric_precision is not null then 'numeric('||c.numeric_precision||','||c.numeric_scale||')' else c.data_type end order by 1,2 limit 12;
select 'v_ace physical_type=integer but data_type TEXT', count(*) from recovery.sys_fields where object_name like 'v\_ace\_%' and data_type='TEXT' and physical_type='integer';
select 'per-view TEXT/integer', object_name, count(*) from recovery.sys_fields where object_name like 'v\_ace\_%' and data_type='TEXT' and physical_type='integer' group by 2 order by 2;
