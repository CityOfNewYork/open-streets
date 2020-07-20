-- this isnt strictly cartodbification
-- also includes some shoehorning of data and types into cartodb target expected
alter table open_street_next add column cartodb_id serial;
alter table open_street_next alter column segmentid type varchar using segmentid::varchar;
update open_street_next set segmentid = lpad(segmentid,7,'0');
update open_street_next set the_geom = ST_SetSRID(the_geom,4326);
create index if not exists open_street_nextthe_geom on open_street_next using GIST(the_geom);
-- I updated the sql generation so this should no longer be necessary
--alter table open_street_next add column the_geom geography(multilinestring, 4326)
--update open_street_next set the_geom = geom;
--alter table open_street_next drop column geom;