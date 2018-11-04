import unittest
from util import dbutil

class User:

    id = None
    fname = None
    lname = None

    def deserialize(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']


class TestDBUtil(unittest.TestCase):

    sql_util = None
    db_util = None

    def setUp(self):
        self.sql_util = dbutil.SQLUtil(file_path='../../config/config.yaml')
        self.db_util = dbutil.DBUtil(file_path='../../config/config.yaml')
        self.assertTrue(self.sql_util.execute_query(
            "CREATE TABLE tmp(id serial PRIMARY KEY, fname varchar(200) NOT NULL, lname varchar(200) NOT NULL)"))

    def test_engine_creation(self):
        self.assertTrue(self.db_util.is_engine_created())

    def test_execute(self):
            self.assertTrue(
            self.sql_util.execute_query("INSERT INTO tmp (fname, lname) values('divyang', 'soni')"))

    def test_execute_params(self):
        params = []
        params.append("divyang")
        params.append("soni")
        self.assertTrue(
             self.sql_util.execute_query("INSERT INTO tmp (fname, lname) values(%s, %s)",args_dict=params))


    def test_execute_multiple_params(self):
        params = []
        params.append({'fname': 'neha', "lname":'jethani'})
        params.append({'fname': 'raj', "lname": 'baraiya'})
        params.append({'fname': 'varun', "lname": 'shah'})
        self.assertTrue(
            self.sql_util.execute_query_multiple("INSERT INTO tmp (fname,lname) values(%(fname)s, %(lname)s)", args_dict=params))

    def test_fetch_data(self):
        params = []
        params.append({'fname': 'divyang', "lname": 'soni'})
        params.append({'fname': 'neha', "lname": 'jethani'})
        params.append({'fname': 'raj', "lname": 'baraiya'})
        params.append({'fname': 'varun', "lname": 'shah'})
        self.assertTrue(
            self.sql_util.execute_query("INSERT INTO tmp (fname,lname) values(%(fname)s, %(lname)s)", args_dict=params))
        data = self.sql_util.fetch_data("select * from tmp where fname = 'divyang'", model=User)
        self.assertEqual("soni", data[0].lname)

    def test_fetch_data(self):

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

        connection = self.db_util.get_connection()
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

    def tearDown(self):
        self.sql_util.execute_query("DROP TABLE tmp")
        self.sql_util = None
        self.db_util = None

if __name__ == '__main__':
    unittest.main()