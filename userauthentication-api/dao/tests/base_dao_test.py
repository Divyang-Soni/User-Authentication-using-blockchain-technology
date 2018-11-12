import unittest
import string
from dao.base_dao import BaseDao


class User:

    id = None
    fname = None
    lname = None


class TestBaseDao(unittest.TestCase):

    def setUp(self):
        self.base_dao = BaseDao(file_path='../../config/config.yaml')
        self.base_dao.execute_query(
            "drop table IF EXISTS tmp;CREATE TABLE tmp(id serial PRIMARY KEY, fname varchar(200) NOT NULL, lname varchar(200) NOT NULL)")

    def test_create_select_query(self):
        print("running {}".format("test_create_select_query"))
        fileds = ['fname','lname']
        where = "fname = 'divyang'"
        sql = (self.base_dao.create_select_query("tmp", fields=fileds, where=where)).lower()
        self.assertEqual(sql, "select fname,lname from tmp where fname = 'divyang'")

    def test_create_insert_query(self):
        print("running {}".format("test_create_select_query"))
        fileds = ['fname', 'lname']
        sql = (self.base_dao.create_insert_query("tmp", fields=fileds)).lower()
        self.assertEqual(sql, "insert into tmp (fname,lname) values(%(fname)s,%(lname)s)")

    def test_create_single_insert_query(self):
        print("running {}".format("test_create_single_insert_query"))
        fileds = ['fname', 'lname']
        sql = (self.base_dao.create_single_insert_query("tmp", fields=fileds)).lower()
        self.assertEqual(sql, "insert into tmp (fname,lname) values(%s,%s)")

    def test_insert_single_record(self):
        print("running {}".format("test_insert_single_record"))
        fileds = ['fname', 'lname']
        values = ['divyang','soni']
        self.base_dao.insert_single_record('tmp', fields=fileds, args_dict=values)

        sql = "select * from tmp where fname = 'divyang'"
        data = self.base_dao.fetch_data(sql)
        self.assertEqual(data[0]['lname'], 'soni')

    def test_insert_records(self):
        print("running {}".format("test_insert_records"))
        fileds = ['fname', 'lname']
        values = [
                {'fname':'divyang', 'lname' : 'soni'},
                {'fname': 'varun', 'lname': 'shah'}
                ]
        self.base_dao.insert_records('tmp', fields=fileds, args_dict=values)

        sql = "select * from tmp"
        data = self.base_dao.fetch_data(sql)
        self.assertEqual(len(data), 2)

    def test_get_data(self):
        print("running {}".format("test_insert_records"))
        fileds = ['fname', 'lname']
        values = [
            {'fname': 'divyang', 'lname': 'soni'},
            {'fname': 'varun', 'lname': 'shah'}
        ]
        self.base_dao.insert_records('tmp', fields=fileds, args_dict=values)

        where = "fname = 'divyang'"
        data = self.base_dao.get_data('tmp', fields=fileds, where=where)
        self.assertEqual(data[0]['lname'], 'soni')

        where = "fname = 'varun'"
        data = self.base_dao.get_data('tmp', fields=fileds, where=where)
        self.assertEqual(data[0]['lname'], 'shah')

    def tearDown(self):
        self.base_dao.execute_query("DROP TABLE IF EXISTS tmp")

if __name__ == '__main__':
    unittest.main()