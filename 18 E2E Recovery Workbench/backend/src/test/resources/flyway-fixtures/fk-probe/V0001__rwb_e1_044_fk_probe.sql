-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.fk_probe (account_id bigint REFERENCES public.account(id));
