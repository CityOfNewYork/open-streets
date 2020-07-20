BEGIN;
--this is for reference, its incorporated into load_and_test.py
DELETE FROM open_street_live;
insert into open_street_live (
     borough
    ,day_of_wee
    ,end_time
    ,from_stree
    ,length_in_
    ,location_p
    ,nhoodname
    ,on_street
    ,date_open_ --original
    ,start_time --og
    ,segmentid --this is not the segmentid used by the functions.  We use lion
    ,shape_leng
    ,to_street
    ,"type"
    ,the_geom)
select 
     borough
    ,day_of_wee
    ,end_time
    ,from_stree
    ,length_in_::numeric --geojson source yields chars
    ,location_p
    ,nhoodname
    ,on_street
    ,date_open_ --new chaos
    ,start_time --again
    ,segmentid::numeric -- forcing this to match the original setup.  not the segmentid used by the functions.  We use lion
    ,shape_leng::numeric --geojson source yields chars
    ,to_street
    ,"type"
    ,the_geom 
from open_street_next;
COMMIT;