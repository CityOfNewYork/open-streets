-- execute functions against open_street_next to test
--    export PGUSER=localuser
--    export PGPASSWORD=localpass
--    export PGDATABASE=localdb
--    psql -f function_deploy_test.sql
drop function if exists open_street_node_test;

CREATE OR REPLACE FUNCTION open_street_node_test(
  text
) 

RETURNS TABLE (
  cartodb_id integer,
  segment_id text,
  from_node_id text,
  to_node_id text,
  street text,
  from_left_house_number bigint,
  to_left_house_number bigint,
  from_right_house_number bigint,
  to_right_house_number bigint,
  open_date text,
  days_of_week text,
  daily_start_time text,
  daily_end_time text
)

AS $$ BEGIN
RETURN QUERY

select a.cartodb_id
      ,CAST(a.segmentid as text)
      ,CAST(a.nodeidfrom as text)
      ,CAST(a.nodeidto as text)
      ,CAST(a.street as text)
      ,CAST(a.fromleft as bigint)
      ,CAST(a.toleft as bigint)
      ,CAST(a.fromright as bigint)
      ,CAST(a.toright as bigint)
      ,to_char(b.date_open_, 'YYYY-MM-DD')
      ,CAST(b.day_of_wee as text)
      ,CAST(b.start_time as text)
      ,CAST(b.end_time as text)
from 
    lion a
join
    (select distinct 
         a.cartodb_id
        ,b.date_open_
        ,b.day_of_wee
        ,b.start_time
        ,b.end_time
        ,b.length_in_ 
    from 
        lion a
    join
        open_street_next b
    on 
        ( a.nodeidto = $1
         OR a.nodeidfrom = $1)
    and ST_Intersects(a.the_geom,
                      st_buffer(b.the_geom::geography, 2)::geometry)
    ) b
on a.cartodb_id = b.cartodb_id;

END;
$$ 
LANGUAGE plpgsql;

drop function if exists open_street_radius_test;

CREATE OR REPLACE FUNCTION open_street_radius_test(
  integer,
  integer,
  integer
) 

RETURNS TABLE (
  cartodb_id integer,
  segment_id text,
  from_node_id text,
  to_node_id text,
  street text,
  from_left_house_number bigint,
  to_left_house_number bigint,
  from_right_house_number bigint,
  to_right_house_number bigint,
  open_date text,
  days_of_week text,
  daily_start_time text,
  daily_end_time text,
  feet_from_input double precision
)

AS $$ BEGIN
RETURN QUERY

select a.cartodb_id
      ,CAST(a.segmentid as text)
      ,CAST(a.nodeidfrom as text)
      ,CAST(a.nodeidto as text)
      ,CAST(a.street as text)
      ,CAST(a.fromleft as bigint)
      ,CAST(a.toleft as bigint)
      ,CAST(a.fromright as bigint)
      ,CAST(a.toright as bigint)
      ,CAST(b.date_open_ as text)
      ,CAST(b.day_of_wee as text)
      ,CAST(b.start_time as text)
      ,CAST(b.end_time as text)
      ,b.distance
from 
    lion a
join
    (
    select distinct
         a.cartodb_id
        ,to_char(b.date_open_, 'YYYY-MM-DD') as date_open_
        ,CAST(b.day_of_wee as text)
        ,CAST(b.start_time as text)
        ,CAST(b.end_time as text)
        ,ST_Distance(a.the_geom, ST_Transform(ST_SetSRID(ST_Point($1, $2), 2263),4326)) as distance
    from 
        lion a
    join
        open_street_next b
    on
        ST_Intersects(a.the_geom,
                      st_buffer(b.the_geom::geography, 2)::geometry)
    where 
        ST_DWithin(b.the_geom::geography
                  ,ST_Transform(ST_SetSRID(ST_Point($1, $2), 2263),4326)::geography
                  ,$3)
    ) b
on 
    a.cartodb_id = b.cartodb_id
order by 
    b.distance asc;

END;
$$ 
LANGUAGE plpgsql;

drop function if exists open_street_segment_test;

CREATE OR REPLACE FUNCTION open_street_segment_test(
  text
) 

RETURNS TABLE (
  cartodb_id integer,
  segment_id text,
  from_node_id text,
  to_node_id text,
  street text,
  from_left_house_number bigint,
  to_left_house_number bigint,
  from_right_house_number bigint,
  to_right_house_number bigint,
  open_date text,
  days_of_week text,
  daily_start_time text,
  daily_end_time text
)

AS $$ BEGIN
RETURN QUERY

select a.cartodb_id
      ,CAST(a.segmentid as text)
      ,CAST(a.nodeidfrom as text)
      ,CAST(a.nodeidto as text)
      ,CAST(a.street as text)
      ,CAST(a.fromleft as bigint)
      ,CAST(a.toleft as bigint)
      ,CAST(a.fromright as bigint)
      ,CAST(a.toright as bigint)
      ,to_char(b.date_open_, 'YYYY-MM-DD')
      ,CAST(b.day_of_wee as text)
      ,CAST(b.start_time as text)
      ,CAST(b.end_time as text)
from 
    lion a
join
    (select distinct 
         c.cartodb_id
        ,d.date_open_
        ,d.day_of_wee
        ,d.start_time
        ,d.end_time
        ,d.length_in_ 
    from 
        lion c
    join
        open_street_next d
    on 
        c.segmentid = $1
    and ST_Intersects(c.the_geom,
                      st_buffer(d.the_geom::geography, 2)::geometry)
    ) b
on a.cartodb_id = b.cartodb_id;

END;
$$ 
LANGUAGE plpgsql;