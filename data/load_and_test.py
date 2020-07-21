import os
import sys
import logging
import requests
import json

import cartomgr


def load_stg(cartoclient
            ,logger):

    logger.info('uploading open_street_next.tar.gz to carto')   

    shapefolder = os.path.abspath("open_street_next.tar.gz")
    cartoid_upload = cartoclient.uploadshapefolder(shapefolder)        
    kount_upload = cartoclient.getkount(cartoid_upload)

    logger.info("carto created a dataset named {0} with {1} records".format(cartoid_upload
                                                                           ,kount_upload))

    logger.info('refreshing open_street_next from {0}'.format(cartoid_upload))
        
    list_of_sqls = []

    sql = """BEGIN;"""
    list_of_sqls.append(sql)

    sql = """delete from open_street_next;"""
    list_of_sqls.append(sql)

    sql = """insert into open_street_next ( 
             borough
            ,day_of_wee
            ,end_time
            ,from_stree
            ,length_in_
            ,location_p
            ,nhoodname
            ,on_street
            ,date_open_ 
            ,start_time 
            ,segmentid
            ,shape_leng
            ,to_street
            ,"type"
            ,the_geom)
        select 
             borough
            ,day_of_wee
            ,end_time
            ,from_stree
            ,length_in_::numeric 
            ,location_p
            ,nhoodname
            ,on_street
            ,date_open_ 
            ,start_time 
            ,LPAD(segmentid, 7, '0') 
            ,shape_leng::numeric 
            ,to_street
            ,"type"
            ,the_geom 
        from {0};""".format(cartoid_upload)
    list_of_sqls.append(sql)

    sql = """COMMIT;"""
    list_of_sqls.append(sql)

    if cartoclient.batchsql(list_of_sqls):
    
        kount_next = cartoclient.getkount(cartoid_upload)
    
        if kount_next ==  kount_upload:
        
            logger.info("successfully inserted {0} records into {1}".format(kount_upload, 'open_street_next'))

    else:
    
        raise
    
    logger.info("deleting uploaded {0} from carto".format(cartoid_upload))
    cartoclient.delete(cartoid_upload)

def load_prd(cartoclient
            ,logger):

    logger.info('refreshing open_street_live from open_street_next')
        
    list_of_sqls = []
    
    sql = """BEGIN;"""
    list_of_sqls.append(sql)

    sql = """DELETE FROM open_street_live;"""
    list_of_sqls.append(sql)

    sql = """insert into open_street_live (
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
        from open_street_next;"""

    list_of_sqls.append(sql)

    sql = """COMMIT;"""
    list_of_sqls.append(sql)

    if cartoclient.batchsql(list_of_sqls):
    
        kount_live = cartoclient.getkount('open_street_live')
    
        if kount_live > 0:
        
            logger.info("successfully inserted {0} records into {1}".format(kount_live, 'open_street_live'))

        else:

            raise ValueError('Dont see a good count of records in open_street_live')

    else:
    
        raise

def test_stg_vs_prd(logger):

    # expect random proxy errors from inside DoITT network, just keep rerunning 
    # the trick is to never be afraid

    # TODO organize this mess

    # real segment open street
    response_stg = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment_test(%270164354%27)".format(os.environ['ACCOUNT'])).text)
    response_prd = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment(%270164354%27)".format(os.environ['ACCOUNT'])).text)

    if response_stg["total_rows"] == response_prd["total_rows"]:
        logger.info(".OK")
    else:
        logger.info("FAIL open_street_segment_test(0164354)")

    # segment 1 is nothing, 0 rows

    response_stg = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment_test(%270000001%27)".format(os.environ['ACCOUNT'])).text)
    response_prd = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment(%270000001%27)".format(os.environ['ACCOUNT'])).text)

    if response_stg["total_rows"] == response_prd["total_rows"]:
        logger.info(".OK")
    else:
        logger.info("FAIL open_street_segment_test(0000001)")

    #real node 0020769
    response_stg = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_node_test(%270020769%27)".format(os.environ['ACCOUNT'])).text)
    response_prd = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_node(%270020769%27)".format(os.environ['ACCOUNT'])).text)

    if response_stg["total_rows"] == response_prd["total_rows"]:
        logger.info(".OK")
    else:
        logger.info("FAIL open_street_node_test(0020769)")

    #radius from x,y
    response_stg = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_radius_test(987296,201152,100)".format(os.environ['ACCOUNT'])).text)
    response_prd = json.loads(requests.get("https://{0}.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_radius(987296,201152,100)".format(os.environ['ACCOUNT'])).text)

    if response_stg["total_rows"] == response_prd["total_rows"]:
        logger.info(".OK")
    else:
        logger.info("FAIL open_street_radius_test(987296,201152,100)")


def main(prd_or_stg):

    if  os.environ['API_KEY'] is not None and os.environ['ACCOUNT'] is not None:
    
        karto_klient = cartomgr.client()
    
    else:

        raise ValueError("missing API_KEY or ACCOUNT environmental")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
 
    if prd_or_stg == 'stg':

        load_stg(karto_klient
                ,logger)

    elif prd_or_stg == 'prd':

        #logger.info("manually execute refresh_live_from_next.sql here")
        #logger.info("this step is commented in the code until I have seen it through once")
        #logger.info("tests will still run however....")

        load_prd(karto_klient
                ,logger)


    test_stg_vs_prd(logger)
    

if __name__ == "__main__":

    prd_or_stg = sys.argv[1]
    main(prd_or_stg)
