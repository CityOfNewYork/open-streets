# Open Street Functions Data Prep

Motivation: perform no ETL processing except for pushing an updated open streets
dataset from NYC Open Data to Carto.

## Open Streets Upload: So-called DEV -> STG -> PRD 

#### 1. DEV: Extract open streets from Socrata, load to local (or any dev) PostgreSQL database

1. Pull https://data.cityofnewyork.us/api/geospatial/uiay-nctu
2. Load to table OPEN_STREET_NEXT
3. Compare to (pre-existing from last run) OPEN_STREET_LIVE
4. If different, run database-only tests on OPEN_STREET_NEXT
5. If tests pass, refresh OPEN_STREET_LIVE from OPEN_STREET_NEXT
6. Run database-only tests on OPEN_STREET_LIVE

Requirements: psql access to a PostGIS DB and ogr2ogr on path. This one is from 
Git Bash for me.  

```shell
$ export PGUSER=localuser
$ export PGPASSWORD=localpassword
$ export PGDATABASE=localdb
$ ./dev_load_and_test.sh
```
We will carry the just-created OPEN_STREET_NEXT table to staging.  

#### 2. STG: Push to Carto "Testing" endpoints

1. Complete step 1 above, DEV.
2. Load to carto table OPEN_STREET_NEXT 
3. Run Carto API tests on open_street_test_* endpoints, comparing to live open_street_* endpoints

Requirements python 3+ with virtualenv and pip.  This one from Windows CMD, I 
can't seem to get virtualenv and pip working from Git Bash and have nowhere else
to develop.

```bat
> set API_KEY=WhyWasThe6ScaredBecause789
> set ACCOUNT=nycmap
> stg_load_and_test.bat
```

#### 3. PRD: Refresh Carto Open Streets
    
1. Refresh Carto OPEN_STREET_LIVE from OPEN_STREET_NEXT
2. Run Carto API tests on open_street_test_* endpoints, comparing to live open_street_* endpoints

Requirements python 3+ with virtualenv and pip.  This one from Windows CMD for me.

```bat
> set API_KEY=WhyWasThe6ScaredBecause789
> set ACCOUNT=nycmap
> prd_load_and_test.bat
```

## First Time only To Carto: 

Only If we are loading these tables for the first time, add checks.

```sql
alter table open_street_live add constraint open_street_livethe_geomsimple CHECK (ST_IsSimple(the_geom::geometry));
alter table open_street_live add constraint open_street_livethe_geomvalid CHECK (ST_IsValid(the_geom::geometry));
alter table open_street_next add constraint open_street_nextthe_geomsimple CHECK (ST_IsSimple(the_geom::geometry));
alter table open_street_next add constraint open_street_nextthe_geomvalid CHECK (ST_IsValid(the_geom::geometry));
```

## Occasional LION upload

Whenever 311 switches to a new quarterly Geoclient release, upload the corresponding
LION file from

https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-lion.page

1. Download the geodatabase and extract the "lion" feature class to a shapefile 
named lion.shp in the data directory.

2. Load to PostGIS, create a segment midpoint for each segment and overwrite lion.shp

From the /data directory of this repo:

```shell
export PGUSER=localuser
export PGPASSWORD=localpass
export PGDATABASE=localdb
./createlion.sh
```

3. Load revised lion.shp to Carto

Use the carto GUI. I think the way to do this is to let Carto rename as LION_X 
then rename the live LION then rename LION_X as LION?  Seems dangerous.

Then fire up the SQL prompt in carto and index the columns that our functions 
will use.  Carto expects specific naming conventions I think, be careful if
making changes below.

```sql
> CREATE INDEX idx_lion_nodeidfrom ON lion (nodeidfrom);
> CREATE INDEX idx_lion_nodeidto ON lion (nodeidto);
> CREATE INDEX idx_lion_segmentid ON lion (segmentid);
> select * from pg_indexes where tablename = 'lion';
```
