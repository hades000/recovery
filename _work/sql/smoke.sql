-- Smoke data for the view conformance check. Not a deliverable.
INSERT INTO public.product (product_key, description, product_type, product_category, product_category_efs)
VALUES ('MORTGAGE', 'Mortgage', 'SECURED', 'MORTGAGE', 'MORTGAGE');
INSERT INTO public.branch (oc_code, branch_name) VALUES ('0001', 'Head office');
INSERT INTO public.account (id, account_key, account_code, account_name, product_key, current_branch,
    delay_days, total_balance, core_banking_system_date, is_restructured, contract_number, contract_date, interest_rate)
VALUES (1, 'ACC0000017', '0000000017', 'Somchai Jaidee', 'MORTGAGE', '0001', 95, 1250000.00, '2026-11-30', 'Y', 'CT-00017', '2021-03-01', 6.25);
INSERT INTO public.customer (person_key, identification_number, first_name, surname, birth_date, is_deceased)
VALUES ('CIF000123', '1234567890123', 'Somchai', 'Jaidee', '1980-05-12', 'N');
INSERT INTO public.phone (phone_key, person_key, phone_number, contact_usage) VALUES ('PH-1', 'CIF000123', '0812345678', 'PRIMARY');
INSERT INTO public.payment (account_key, pay_key, total_amount, pay_date, pay_type) VALUES ('ACC0000017', 'PAY-1', 15000.00, '20261130', 'CASH');
INSERT INTO public.ace_batch_run (source_system, business_date, started_at, completed_at, status, record_count)
VALUES ('ALS', '2026-11-30', now() - interval '4 hours', now() - interval '3 hours', 'COMPLETED', 184500);
INSERT INTO public.asset (asset_key, asset_type) VALUES ('AST-1', 'LAND');
INSERT INTO public.collateral_detail (collateral_detail_key, asset_key, title_doc_no, lien_rank, business_date)
VALUES ('CD-1', 'AST-1', 'TD-99881', 1, '2026-11-30');

SELECT account_key, days_past_due, total_balance, data_as_of, tdr_flag, product_category FROM recovery.v_ace_account;
SELECT payment_code, payment_date, payment_amount, data_as_of FROM recovery.v_ace_payment;
SELECT cif_no, id_no_masked, id_no_last4 FROM recovery.v_ace_customer;
SELECT contact_type, contact_key, contact_value, contact_value_masked FROM recovery.v_ace_contact;
SELECT source_system, business_date, is_complete FROM recovery.v_ace_batch_status;
SELECT collateral_no, collateral_type FROM recovery.v_ace_collateral;
SELECT asset_key, title_doc_no, lien_rank FROM recovery.v_ace_collateral_detail;
