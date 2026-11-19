-- Story: RWB-E1-044
INSERT INTO ${recoverySchema}.t1 (v) VALUES ('public.account.account_key');
-- reads public.branch
SELECT a.id FROM public.account a;
CREATE TABLE "public".t2 (id int);
CREATE TABLE ${recoverySchema}.c1 (t_id bigint REFERENCES public.account(id));
