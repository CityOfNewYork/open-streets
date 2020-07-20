from carto.auth import APIKeyAuthClient
from carto.exceptions import CartoException
from carto.sql import SQLClient
from carto.sql import BatchSQLClient
from carto.datasets import DatasetManager
from carto.file_import import FileImportJobManager
from carto.permissions import PRIVATE, PUBLIC, LINK  

import os
import time

# https://github.com/CartoDB/carto-python/tree/master/examples
# We require but a small subset of the carto API.
# Its kinda confusing to recall how it works that one day a month when
# we gotta use it.   
# The cartomgr wraps just the functions we use
# Each def below has a corresponding test (and example use) in test_cartomgr.py

class client(object):

    def __init__(self):

        self.carto_api_key = os.environ['API_KEY']
        self.carto_account = os.environ['ACCOUNT']

        USR_BASE_URL = "https://{user}.carto.com/".format(user=self.carto_account)

        self.auth_client = APIKeyAuthClient(api_key=self.carto_api_key
                                           ,base_url=USR_BASE_URL)

        #this mimics the carto docs, leave it this way
        self.sql = SQLClient(self.auth_client)

        self.dataset_manager = DatasetManager(self.auth_client)

    def checkconnection(self):

        try:
            query = "SELECT * from version()"
            data = self.sql.send(query,do_post=False)
        except CartoException as e:
            print("some error occurred", e)
            #occasional:
            #HTTPSConnectionPool(host='nycmap.carto.com', port=443): Max retries exceeded with url: /api/v2/sql?q=SELECT...
            #(Caused by ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 407 Proxy Authentication Required')))
            return False

        #print(data['rows'])
        #[{'version': 'PostgreSQL 11.5 (Ubuntu 11.5.2+carto-1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 5.4.0-6ubuntu1~16.04.11) 5.4.0 20160609, 64-bit'}]

        sqlret = data['rows']
        for itr in sqlret:
            if itr['version'].startswith('PostgreSQL'):
                return True

        return False

    def getkount(self
                ,relation):

        # return the count of records in any relation

        try:
            query = "SELECT count(*) as kount from {0}".format(relation)
            data = self.sql.send(query, do_post=False)
        except CartoException as e:
            print("some error occurred", e)
            raise

        #print(data['rows'])
        #[{'kount': 1}]
        
        sqlret = data['rows']
        for itr in sqlret:
            # should be just one row with one key,val
            return itr['kount']

    def batchsql(self
                ,list_of_sqls
                ,checkevery=1
                ,maxtime=5):

        # pass in a list of sqls to execute
        # probably dont want to read a file with a million records and upload
        # open streets for ex is 1k rows, 500KB

        batchSQLClient = BatchSQLClient(self.auth_client)
        createJob = batchSQLClient.create(list_of_sqls)

        # https://github.com/CartoDB/carto-python

        # job_id looks like
        # 5171b8c4-8c03-4610-8797-5dd98ff3e61b

        # job looks like
        # {
        #  'user': 'nycmap', 
        #  'status': 'done', 
        #  'query': [{'query': 'drop table if exists foo', 'status': 'done'}, 
        #            {'query': 'create table foo (bar text)', 'status': 'done'}, 
        #            {...} {...}], 
        # 'created_at': '2020-07-02T16:31:31.873Z', 
        # 'updated_at': '2020-07-02T16:31:31.996Z', 
        # 'job_id': '5171b8c4-8c03-4610-8797-5dd98ff3e61b'
        # }

        # queries are nested because you can add more sets to a running job

        readJob = batchSQLClient.read(createJob['job_id'])
        cheks = 0

        while (readJob['status'] != 'done'):
            time.sleep(checkevery)
            readJob = batchSQLClient.read(createJob['job_id'])
            cheks += 1

            if cheks > maxtime:
                return False

        return True

    def uploadshapefolder(self
                         ,path_tothe_zip):

        # I am working with tar.gz
        # not sure what else is good
        # this returns the name in carto (often tablename_XX on repeats)  

        #print("uploading {0}".format(path_tothe_zip))
        # carto will warn:   This is part of a non-public CARTO API and may change in the future.
        cartodatasetid = self.dataset_manager.create(path_tothe_zip)

        #print("carto named the upload {0}".format(cartodatasetid))

        #file_import_manager = FileImportJobManager(self.auth_client)
        #file_imports = file_import_manager.all()
        #print("carto says {0} imports are active".format(len(file_imports)))

        # always gonna make public
        # this one warns of a non-public API which does in fact match the docs
        
        dataset = self.dataset_manager.get(cartodatasetid)

        dataset.privacy = PUBLIC
        dataset.save()

        return cartodatasetid

    def delete(self
              ,tablename):

        # careful buddy wat u doin?
        # copy pastin from https://github.com/CartoDB/carto-python

        # docs refer to table names as "dataset id"

        dataset = self.dataset_manager.get(tablename)
        #print("deleting {0} from our Carto account".format(tablename))
        dataset.delete()
