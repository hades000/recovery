\set ON_ERROR_STOP 0
SET ROLE recovery_svc;
SELECT 'svc read v_ace_account', count(*) FROM recovery.v_ace_account;
SELECT 'svc read v_ace_plan', count(*) FROM recovery.v_ace_plan;
SELECT 'svc read v_ace_batch_status (B)', count(*) FROM recovery.v_ace_batch_status;
SELECT 'svc read v_ace_valuation (B)', count(*) FROM recovery.v_ace_valuation;
SELECT 'svc read public.account', count(*) FROM public.account;
SELECT 'svc read public.customer', count(*) FROM public.customer;
SELECT 'svc read recovery_case (non-view)', count(*) FROM recovery.recovery_case;
INSERT INTO recovery.data_product_load DEFAULT VALUES;
UPDATE recovery.recovery_case SET status='X';
DELETE FROM recovery.sys_objects;
TRUNCATE recovery.case_list_row;
INSERT INTO public.account DEFAULT VALUES;
DELETE FROM public.account;
RESET ROLE;
SELECT 'svc privs on recovery tables (non-SELECT)', count(*) FROM information_schema.role_table_grants WHERE grantee='recovery_svc' AND privilege_type<>'SELECT';
SELECT 'svc SELECT grants on recovery relations', count(*) FROM information_schema.role_table_grants WHERE grantee='recovery_svc' AND privilege_type='SELECT';
SELECT 'svc privs on public', count(*) FROM information_schema.role_table_grants WHERE grantee='recovery_svc' AND table_schema='public';
