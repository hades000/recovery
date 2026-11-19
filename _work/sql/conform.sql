\pset pager off
-- dictionary conformance against the catalog
SELECT 'objects without fields' AS check, count(*) FROM recovery.sys_objects o
  WHERE NOT EXISTS (SELECT 1 FROM recovery.sys_fields f WHERE f.object_name = o.object_name)
UNION ALL
SELECT 'fields without an object', count(*) FROM recovery.sys_fields f
  WHERE NOT EXISTS (SELECT 1 FROM recovery.sys_objects o WHERE o.object_name = f.object_name)
UNION ALL
SELECT 'v_ace views without a dictionary row', count(*) FROM information_schema.views v
  WHERE v.table_schema='recovery' AND v.table_name LIKE 'v_ace_%'
  AND NOT EXISTS (SELECT 1 FROM recovery.sys_objects o WHERE o.object_name = v.table_name)
UNION ALL
SELECT 'dictionary objects that are not a table or view', count(*) FROM recovery.sys_objects o
  WHERE NOT EXISTS (SELECT 1 FROM information_schema.tables t WHERE t.table_schema='recovery' AND t.table_name=o.object_name)
  AND NOT EXISTS (SELECT 1 FROM information_schema.views v WHERE v.table_schema='recovery' AND v.table_name=o.object_name)
UNION ALL
SELECT 'source fields with no ACE target', count(*) FROM recovery.sys_fields
  WHERE source_system IN ('Core bank (ALS) via COLLINS','SCBPDM via COLLINS','EFS via COLLINS','COLLINS','LIT','CCMS','SVAF','AMIS','RPS','WIN','GL','NLEADS','EasyApp','Entra ID');
