-- Story: RWB-E1-044
CREATE TABLE public.t1 (id int);
CREATE VIEW public.v1 AS SELECT 1;
CREATE MATERIALIZED VIEW public.mv1 AS SELECT 1;
CREATE SEQUENCE public.s1;
CREATE INDEX i1 ON public.t1 (id);
CREATE TRIGGER tr1 AFTER INSERT ON public.t1 FOR EACH ROW EXECUTE FUNCTION ${recoverySchema}.f1();
CREATE FUNCTION public.f1() RETURNS int LANGUAGE sql AS $$ SELECT 1 $$;
CREATE PROCEDURE public.p1() LANGUAGE sql AS $$ SELECT 1 $$;
CREATE TYPE public.ty1 AS (a int);
CREATE DOMAIN public.d1 AS int;
CREATE TABLE ${recoverySchema}.c1 (id int REFERENCES public.t1(id));
SELECT 1 FROM public.t1;
SELECT 1 FROM ${recoverySchema}.t1 JOIN public.t1 ON true;
INSERT INTO public.t1 VALUES (1);
UPDATE public.t1 SET id = 1;
TRUNCATE public.t1;
COMMENT ON TABLE public.t1 IS 'x';
CREATE TABLE ${recoverySchema}.c2 (id int) OWNED BY public.t1;
