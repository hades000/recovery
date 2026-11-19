-- Story: RWB-E1-044
INSERT INTO ${recoverySchema}.t1 (v) VALUES ('public.account.account_key');
INSERT INTO ${recoverySchema}.t1 (v) VALUES ('it''s public.account');
INSERT INTO ${recoverySchema}.t1 (v) VALUES (E'public.branch');
SELECT 1; -- reads public.account
/* public.product
   continued */
SELECT 1;
