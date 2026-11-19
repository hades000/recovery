-- Story: RWB-E1-044
-- Fix: add index
CREATE INDEX ix_queue_team ON ${recoverySchema}.queue (team_code);
