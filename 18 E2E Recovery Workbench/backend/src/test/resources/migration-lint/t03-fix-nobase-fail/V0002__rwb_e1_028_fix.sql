-- Story: RWB-E1-028
-- Fix: backfill
UPDATE ${recoverySchema}.note SET id = id;
