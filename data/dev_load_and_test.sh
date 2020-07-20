rm openstreets.geojson
rm openstreets.dbf
rm openstreets.prj
rm openstreets.shp
rm openstreets.shx
curl -X GET 'https://data.cityofnewyork.us/resource/uiay-nctu.geojson?$limit=10000' > openstreets.geojson
ogr2ogr -a_srs "EPSG:4326" -nlt LINESTRING -skipfailures openstreets.shp openstreets.geojson     
shp2pgsql -g the_geom openstreets.shp open_street_next > open_street_next.sql
psql -c 'drop table if exists open_street_next;'
psql -f open_street_next.sql
psql -f cartodbify_next.sql
psql -f tidy_next.sql
psql -f cartodbify_live.sql
segdiffcount=$( psql -tXA -f segdiffcount.sql )
if (( $segdiffcount > 0 )); then
    echo 'refreshing open_street_live from open_street_next'
    psql -f refresh_live_from_next.sql
else
    echo 'no differences exiting'
    exit 0
fi
cd regress
echo 'review these test results, should be all OKs'
./run_all_tests.sh
cd ../
echo 'writing open_street_next.shp from open_street_next table'
pgsql2shp -f open_street_next $PGDATABASE open_street_next
echo 'creating a fancy open_street_next.tar.gz shapefolder for Carto upload'
tar -czvf open_street_next.tar.gz open_street_next.shp open_street_next.dbf open_street_next.cpg open_street_next.prj open_street_next.shx
