import unittest
from dbutil.dbutil import DBUtil, SQLUtil


class User:

    id = None
    fname = None
    lname = None


class TestDBUtil(unittest.TestCase):

    sql_util = None
    db_util = None

    def setUp(self):
        self.sql_util = SQLUtil(file_path='../../config/config.yaml')
        self.db_util = DBUtil(file_path='../../config/config.yaml')


        self.sql_util.execute_query(
            "drop table IF EXISTS tmp;CREATE TABLE tmp(id serial PRIMARY KEY, fname varchar(200) NOT NULL, lname varchar(200) NOT NULL)")

    def test_engine_creation(self):
        print("running {}".format("test_engine_creation"))
        self.assertTrue(self.db_util.is_engine_created())

    def test_execute(self):
        print("running {}".format("test_execute"))
        self.assertTrue(
            self.sql_util.execute_query("INSERT INTO tmp (fname, lname) values('divyang', 'soni')"))

    def test_execute_params(self):
        print("running {}".format("test_execute_params"))
        params = []
        params.append("divyang")
        params.append("soni")
        self.assertTrue(
             self.sql_util.execute_query("INSERT INTO tmp (fname, lname) values(%s, %s)",args_dict=params))

    def test_execute_multiple_params(self):
        print("running {}".format("test_execute_multiple_params"))
        params = []
        params.append({'fname': 'divyang', "lname": 'soni'})
        params.append({'fname': 'neha', "lname":'jethani'})
        params.append({'fname': 'raj', "lname": 'baraiya'})
        params.append({'fname': 'varun', "lname": 'shah'})
        self.assertTrue(
            self.sql_util.execute_query_multiple("INSERT INTO tmp (fname,lname) values(%(fname)s, %(lname)s)", args_dict=params))

    def test_fetch_data1(self):
        print("running {}".format("test_fetch_data1"))
        params = []
        params.append({'fname': 'divyang', "lname": 'soni'})
        params.append({'fname': 'neha', "lname": 'jethani'})
        params.append({'fname': 'raj', "lname": 'baraiya'})
        params.append({'fname': 'varun', "lname": 'shah'})
        self.assertTrue(
            self.sql_util.execute_query("INSERT INTO tmp (fname,lname) values(%(fname)s, %(lname)s)", args_dict=params))
        data = self.sql_util.fetch_data("select * from tmp where fname = 'divyang'")
        self.assertEqual("soni", data[0]['lname'])

    def test_fetch_data(self):
        print("running {}".format("test_fetch_data"))
        params = []
        params.append({'fname': 'divyang', "lname": 'soni'})
        params.append({'fname': 'neha', "lname": 'jethani'})
        params.append({'fname': 'raj', "lname": 'baraiya'})
        params.append({'fname': 'varun', "lname": 'shah'})
        self.assertTrue(
            self.sql_util.execute_query_multiple("INSERT INTO tmp (fname,lname) values(%(fname)s, %(lname)s)", args_dict=params))

        params=[]
        params.append('divyang')
        data = self.sql_util.fetch_data("select * from tmp where fname = %s", args_dict=params, model=User)
        self.assertEqual("soni", data[0].lname)

    def test_execute_fetch_using_connection_data(self):
        print("running {}".format("test_execute_fetch_using_connection_data"))
        c = self.db_util.get_connection()

        connection = self.db_util.get_connection(old_connection=c)


        tran = connection.begin()

        params = []
        params.append({'fname': 'divyang', "lname": 'soni'})
        params.append({'fname': 'neha', "lname": 'jethani'})
        params.append({'fname': 'raj', "lname": 'baraiya'})
        params.append({'fname': 'varun', "lname": 'shah'})
        self.assertTrue(
            self.sql_util.execute_query("INSERT INTO tmp (fname,lname) values(%(fname)s, %(lname)s)", args_dict=params, connection=connection))

        params=[]
        params.append('divyang')
        data = self.sql_util.fetch_data("select * from tmp where fname = %s", args_dict=params, model=User,connection=connection)
        self.assertEqual("soni", data[0].lname)
        tran.rollback()

        params = []
        params.append('divyang')
        data = self.sql_util.fetch_data("select * from tmp where fname = %s", args_dict=params, model=User,
                                        connection=connection)
        self.assertEqual(0, len(data))

        connection = self.db_util.close_connection(connection, old_connection=c)
        self.assertEqual(None, self.db_util.close_connection(c))

    def tearDown(self):
        self.sql_util.execute_query("DROP TABLE IF EXISTS tmp")
        self.sql_util = None
        self.db_util = None

if __name__ == '__main__':
    unittest.main()