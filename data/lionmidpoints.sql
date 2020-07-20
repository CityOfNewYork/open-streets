alter table lion add column the_geom geography(point, 4326);
update lion set the_geom = ST_LineInterpolatePoint(st_linemerge(geom),.50);
create index if not exists lionthe_geom on lion using GIST(the_geom);
alter table lion drop column geom;