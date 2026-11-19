-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.t1 (id int);
SELECT count(*) FROM information_schema.tables;
SELECT count(*) FROM pg_catalog.pg_class;
