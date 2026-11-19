\pset pager off
SELECT 'tables' AS item, count(*) FROM information_schema.tables WHERE table_schema='recovery' AND table_type='BASE TABLE'
UNION ALL SELECT 'views', count(*) FROM information_schema.views WHERE table_schema='recovery'
UNION ALL SELECT 'sys_objects', count(*) FROM recovery.sys_objects
UNION ALL SELECT 'sys_fields', count(*) FROM recovery.sys_fields
UNION ALL SELECT 'data_product', count(*) FROM recovery.data_product
UNION ALL SELECT 'fk_to_public', count(*) FROM pg_constraint c
  JOIN pg_class t ON t.oid=c.conrelid JOIN pg_namespace n ON n.oid=t.relnamespace
  JOIN pg_class r ON r.oid=c.confrelid JOIN pg_namespace rn ON rn.oid=r.relnamespace
  WHERE c.contype='f' AND n.nspname='recovery' AND rn.nspname='public';
SELECT f.field_id, f.object_name, f.field_name, f.source_system, f.source_field, f.data_type, f.physical_type
FROM recovery.v_data_dictionary f
WHERE f.object_name='v_ace_account' AND f.field_name='days_past_due';
SELECT f.field_id, f.object_name, f.field_name, f.source_system, f.data_type
FROM recovery.v_data_dictionary f
WHERE f.field_name IN ('id_no_masked','nleads_ref','total_balance')
ORDER BY f.object_name, f.field_name;
