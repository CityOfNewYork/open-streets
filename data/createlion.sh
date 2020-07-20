# occasional load of lion reference data
# export PGUSER=sehace
# export PGPASSWORD=camino
# export PGDATABASE=alandar
shp2pgsql -s 2263:4326 lion.shp lion > lion.sql
psql -c 'drop table if exists lion;'
psql -f lion.sql
psql -f lionmidpoints.sql
rm lion.*
pgsql2shp -f lion -g the_geom $PGDATABASE lion
# todo: zip
