import sys
import os
import subprocess
import itertools

class dbi(object):

    def __init__(self
                ,databasehost
                ,database
                ,databaseuser):

        self.dbhost = databasehost
        self.db = database
        self.dbuser = databaseuser
        
    def sql(self
           ,sqlfile):

        #tupes only, ignore user startup file, unaligned output        
        psqlcmd = "psql -tXA "
        psqlcmd += "-h {0} -U {1} -d {2} -f {3}".format(self.dbhost
                                                       ,self.dbuser
                                                       ,self.db
                                                       ,sqlfile)

        #print(psqlcmd)
        
        p1 = subprocess.Popen(psqlcmd
                             ,stdout=subprocess.PIPE
                             ,shell=True)

        output = p1.communicate()[0]

        # \l for UTF8 reminder friend
        # in python3 we must decode or we get b'asciibytedata'
        return output.strip().decode('utf-8')        


class dossier(object):

    def __init__(self
                ,content):

        # content should be a list of text, one line each
        if type(content) is list:
            self.content = content
        else:
            raise ValueError('Input is not a list')

    @classmethod
    def fromText(cls
                ,text):

        # supports all line ending types
        return cls(text.splitlines())

    @classmethod
    def fromFile(cls
                ,fname):

        # open with no newline set translates all line endings to \n
        with open(fname) as f:
            incontent = f.readlines()

        return cls([x.strip() for x in incontent])

    def getDirt(self
               ,content):
        
        # expected test results should be input to getDirt as clean content
        # tests (self) produce dirty dossiers
        
        dirt = []
        for testline, expectedline in itertools.zip_longest(self.content, 
                                                            content):
            if testline != expectedline:
                dirt.append('expected: {0}'.format(expectedline))
                dirt.append('test    : {0}'.format(testline))
            else:
                # space reserved for debugging 
                pass                

        return dirt

def run_simple_test(testscript
                   ,testexpected):

    if not os.path.isfile(testexpected):
        msg = "I cannot find the expected file at {0}".format(testexpected)
        print (msg)
        raise ValueError(msg)

    # should be set in env, defaults are reminders of what we expect, no more
    pghost = os.getenv('PGHOST', 'localhost') 
    pgdatabase = os.getenv('PGDATABASE', 'scratch')
    pguser = os.getenv('PGUSER', 'stratum')

    mydbi = dbi(pghost
               ,pgdatabase
               ,pguser)
    
    sqloutput = mydbi.sql(testscript)

    testdossier = dossier.fromText(sqloutput)
    expecteddossier = dossier.fromFile(testexpected)
 
    dirtydossier = testdossier.getDirt(expecteddossier.content)

    if len(dirtydossier) > 0:
        print ("failed test {0} comparing output to {1}".format(testscript
                                                              ,testexpected))
        for dirtyline in dirtydossier:
            print ("{0}{1}".format('   '
                                 ,dirtyline)) 

        return 1
        
    else:
        print ("{0}".format('. OK'))
        return 0

if __name__ == "__main__":

    if len(sys.argv) != 3:
        msg = "I {0} request but 2 inputs, the test sql and expected ".format(sys.argv[0])
        msg += "output file. Instead I have been given {0} inputs".format(len(sys.argv) - 1)                                                   
        print (msg)                                                                        
        raise ValueError(msg)

    ptestscript = sys.argv[1]   
    ptestexpected = sys.argv[2]

    exitval = run_simple_test(ptestscript
                             ,ptestexpected)

    sys.exit(exitval)