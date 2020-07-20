-- this should only be necessary in dev if prior shenanigans have hosed the 
-- types and values
alter table open_street_live alter column segmentid type varchar using segmentid::varchar;
update open_street_live set segmentid = lpad(segmentid,7,'0');
create index if not exists open_street_livethe_geom on open_street_live using GIST(the_geom);
-- I updated the sql generation so this should no longer be necessary
--alter table open_street_next add column the_geom geography(multilinestring, 4326)
--update open_street_next set the_geom = geom;
--alter table open_street_next drop column geom;
