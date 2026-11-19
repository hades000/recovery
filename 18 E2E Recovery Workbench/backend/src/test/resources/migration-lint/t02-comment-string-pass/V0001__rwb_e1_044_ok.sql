-- Story: RWB-E1-044
-- SELECT * FROM public.account
/* public.t1 */
CREATE TABLE ${recoverySchema}.t1 (v text);
INSERT INTO ${recoverySchema}.t1 (v) VALUES ('public.account');
