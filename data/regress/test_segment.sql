-- from tkeanes readme
select * from open_street_segment('0164353');
--this is the worst we manage right now, approx 1.5 meters offset from open street
select * from open_street_segment('0321837');
-- and 2nd Ave should not match to open data segmentid 0, the service road
select * from open_street_segment('0305281');