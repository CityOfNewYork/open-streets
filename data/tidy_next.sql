DELETE FROM
    open_street_next a
USING 
    open_street_next b
WHERE
    a.cartodb_id < b.cartodb_id
AND a.segmentid = b.segmentid
AND a.segmentid <> '0000000';
--enforce whatever we started with as schema changes at DOT and open data
alter table open_street_next rename column open_date TO date_open_;
alter table 
    open_street_next 
add constraint 
    open_street_nextthe_geomsimple CHECK (ST_IsSimple(the_geom::geometry));
alter table 
    open_street_next 
add constraint 
    open_street_nextthe_geomvalid CHECK (ST_IsValid(the_geom::geometry));