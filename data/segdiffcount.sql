select sum(c.kount) as segmentschanged from (
SELECT count(*) as kount
FROM   open_street_next a
WHERE  NOT EXISTS (SELECT 1 FROM open_street_live b WHERE a.segmentid = b.segmentid)
union all 
SELECT count(*) as kount
FROM   open_street_live a
WHERE  NOT EXISTS (SELECT 1 FROM open_street_next b WHERE a.segmentid = b.segmentid)
) c;