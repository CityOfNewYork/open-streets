import unittest
import os
import warnings

import cartomgr

#set API_KEY=xxxxx
#set ACCOUNT=nycmap
#cd C:\matt_projects\carto-fn\data>
#setenv.bat
#python test_cartomgr.py

class CartoClientTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(self):

        # refrain from explicitly passing around credentials
        self.carto_api_key = os.environ['API_KEY']
        self.carto_account = os.environ['ACCOUNT']

        if  self.carto_api_key is not None \
        and self.carto_account is not None:

            self.cartoclient = cartomgr.client()

        else:

            raise ValueError(f"missing either API_KEY or ACCOUNT environmental variables") 
        

    @classmethod
    def tearDownClass(self):

        pass        

    def test_acheckconnection(self):

        # calls for postgres version, verifies reasonable result
        # then returns true if reasonable, otherwise false
        retval = self.cartoclient.checkconnection()
        self.assertTrue(self.cartoclient.checkconnection())

    def test_bgetkount(self):

        # test of simple wrapper to get count of records from any table, 
        # view, function, or relation
        myoneandonly = "version()"
        retval = self.cartoclient.getkount(myoneandonly)
        self.assertEqual(retval, 1)

    def test_cbatchload(self):

        #this mimics a load of open_street_next.sql
        list_of_sqls = []
        list_of_sqls.append("drop table if exists foo")
        list_of_sqls.append("create table foo (bar text)")
        list_of_sqls.append("insert into foo values('spread love')")
        list_of_sqls.append("insert into foo values('its the brooklyn way')")
        
        if (self.cartoclient.batchsql(list_of_sqls)):

            # check that we created a table and inserted 2 rows
            retval = self.cartoclient.getkount('foo')
            self.assertEqual(retval, 2)

        # drop testing table
        list_of_sqls = []
        list_of_sqls.append("drop table if exists foo")

        verifydrop = self.cartoclient.batchsql(list_of_sqls)
        self.assertTrue(verifydrop)

    def test_duploadshapefolder(self):

        #ResourceWarning: unclosed file <_io.BufferedReader name='c:\\matt_projects\\carto-fn\\data\\one_rec_tester.tar.gz'>
        #https://stackoverflow.com/questions/26563711/disabling-python-3-2-resourcewarning
        # this is a different warning from the carto non-public API warning
        warnings.simplefilter("ignore", ResourceWarning)

        shapefolder = os.path.abspath("one_rec_tester.tar.gz")

        cartodatasetid = self.cartoclient.uploadshapefolder(shapefolder)
        
        # check that we created a table with one rec
        retval = self.cartoclient.getkount(cartodatasetid)
        self.assertEqual(retval, 1)

        self.cartoclient.delete(cartodatasetid)

    def test_etransactionrollback(self):

        #all semicolons all the time 

        list_of_sqls = []
        list_of_sqls.append("drop table if exists foo;")
        list_of_sqls.append("create table foo (bar text primary key);")
        list_of_sqls.append("BEGIN;")
        list_of_sqls.append("insert into foo values('spread love');")
        list_of_sqls.append("insert into foo values('its the brooklyn way');")
        list_of_sqls.append("COMMIT;")

        if (self.cartoclient.batchsql(list_of_sqls)):

            # 2 rows of truth
            retval = self.cartoclient.getkount('foo')
            self.assertEqual(retval, 2)

        # test rejection

        list_of_sqls = []
        list_of_sqls.append("BEGIN;")
        list_of_sqls.append("insert into foo values('spread hate');")
        list_of_sqls.append("insert into foo values('its the brooklyn way');")
        list_of_sqls.append("COMMIT;")

        self.assertFalse(self.cartoclient.batchsql(list_of_sqls))

        # 2 rows of truth always remain
        retval = self.cartoclient.getkount('foo')
        self.assertEqual(retval, 2)

        # drop testing table
        list_of_sqls = []
        list_of_sqls.append("drop table if exists foo")

        verifydrop = self.cartoclient.batchsql(list_of_sqls)
        self.assertTrue(verifydrop)
    

if __name__ == '__main__':
    unittest.main()
