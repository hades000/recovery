-- Grants exactly as the commented block in ACE Source Views v1 (lines 718-730), placeholders substituted.
CREATE ROLE ace_view_owner NOLOGIN;
CREATE ROLE recovery_svc NOLOGIN;
GRANT USAGE ON SCHEMA public TO ace_view_owner;
GRANT SELECT ON public.account, public.payment, public.customer, public.phone, public.email,
     public.address, public.ca_relation, public.aa_relation, public.collateral, public.asset,
     public.efs_action, public.efs_action_code, public.efs_assignment, public.bucket_log_snapshot,
     public.product, public.branch, public.bot_holiday, public.ace_case,
     public.cfsc_mg_ssme_tdr_case, public.tdr_calculation, public.ai_recommended_plan
     TO ace_view_owner;
DO $$ DECLARE v text; BEGIN FOR v IN SELECT viewname FROM pg_views WHERE schemaname='recovery' AND viewname LIKE 'v\_ace\_%' LOOP EXECUTE format('ALTER VIEW recovery.%I OWNER TO ace_view_owner', v); END LOOP; END $$;
GRANT USAGE ON SCHEMA recovery TO recovery_svc;
GRANT SELECT ON ALL TABLES IN SCHEMA recovery TO recovery_svc;
REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
