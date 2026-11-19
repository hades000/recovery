-- Story: RWB-E1-044
CREATE VIEW ${recoverySchema}.v1 AS
SELECT a.id AS id, b.note AS note, CAST(a.id AS text) AS id_text
FROM ${recoverySchema}.t1 AS a
JOIN ${recoverySchema}.t2 b ON a.id = b.id
LEFT JOIN ${recoverySchema}.t3 c ON
  c.id = a.id;
CREATE RULE r1 AS ON INSERT TO ${recoverySchema}.t1 DO ALSO INSERT INTO ${recoverySchema}.t2 SELECT a.id FROM ${recoverySchema}.t1 a JOIN ${recoverySchema}.t3 b ON a.id = b.id;
CREATE POLICY p1 ON t1 USING (EXISTS (SELECT 1 FROM ${recoverySchema}.t2 u JOIN ${recoverySchema}.t3 v ON u.id = v.id));
