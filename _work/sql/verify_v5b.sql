\pset pager off
SELECT field_id, entity, field, source_system, source_field, data_type, physical_type
FROM recovery.v_data_dictionary
WHERE entity='v_ace_account' AND field='days_past_due';
SELECT field_id, entity, field, source_system, data_type
FROM recovery.v_data_dictionary
WHERE field IN ('id_no_masked','nleads_ref','total_balance','source_system')
ORDER BY entity, field;
SELECT entity, count(*) FROM recovery.v_data_dictionary GROUP BY entity ORDER BY 2 DESC LIMIT 8;
