\pset footer off
select 'tables', count(*) from pg_tables where schemaname='recovery';
select 'v_ace views', count(*) from pg_views where schemaname='recovery' and viewname like 'v\_ace\_%';
select 'other views', string_agg(viewname, ',') from pg_views where schemaname='recovery' and viewname not like 'v\_ace\_%';
select 'sys_objects', count(*) from recovery.sys_objects;
select 'sys_fields', count(*) from recovery.sys_fields;
select 'data_product', count(*) from recovery.data_product;
select 'constraints to public', count(*) from pg_constraint c join pg_class t on t.oid=c.conrelid join pg_namespace n on n.oid=t.relnamespace left join pg_class r on r.oid=c.confrelid left join pg_namespace rn on rn.oid=r.relnamespace where n.nspname='recovery' and c.contype='f' and rn.nspname<>'recovery';
select 'recovery FKs total', count(*) from pg_constraint c join pg_namespace n on n.oid=c.connamespace where n.nspname='recovery' and c.contype='f';
select 'view deps on public tables (non-v_ace)', count(*) from (select distinct v.relname, t.relname from pg_depend d join pg_rewrite rw on rw.oid=d.objid join pg_class v on v.oid=rw.ev_class join pg_namespace vn on vn.oid=v.relnamespace join pg_class t on t.oid=d.refobjid join pg_namespace tn on tn.oid=t.relnamespace where vn.nspname='recovery' and tn.nspname='public' and v.relname not like 'v\_ace\_%') x;
\x on
select * from recovery.v_data_dictionary where field_name='days_past_due';
\x off
select so.subject_area, count(*) from recovery.sys_objects so group by 1 order by 1;
