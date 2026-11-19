-- Story: RWB-E1-044
ALTER TABLE public
.t1 ADD COLUMN c int;
SELECT count(*) FROM public -- a comment
.account;
