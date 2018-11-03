import psycopg2
import sqlalchemy as sql
from models import database

'''
This class is database util which will be used for below functionality
1. parsing database config data from config file
2. Create dbpool
3. provide connection using dbpool
'''


class DBUtil:

    __engine = None
    __db_model = None

    '''
    This method will do below functionality
    1. parsing database config data from config file
    2. Create dbpool
    3. provide dataase connectiom
    '''
    def __init__(self):
        # code to read database config and create database model
        self.__db_model = database.DBModel()
        if self.__db_model:
            self.__create_engine()

    def __create_engine(self):
        try:
            '''
            this engine will create database connection engine which will
              1. Create database using get_connection (driven by "creator")
              2. creates an internal pool of connection with defined pool size (driven by pool_size)
              3. ping the database connection before returning connection from the pool (driven by "pool_pre_ping")
            '''
            self.__engine = sql.create_engine('postgresql://',
                                              creator=self.__creator,
                                              pool_pre_ping = True,
                                              pool_size=self.__db_model.pool_size,
                                              pool_timeout = self.__db_model.pool_timeout)
        except Exception as e:
            print("Error while creating database engine : {}".format(e))
            self.__engine = None

    def __is_engine_created(self):
        return self.__engine is not None


    '''
    This method is returning the custom creator of  
    '''
    def __creator(self):
        conn = None
        try:
            conn = psycopg2.connect(database=self.__db_model.database_name,
                                    user = self.__db_model.user_name,
                                    password = self.__db_model.password,
                                    host = self.__db_model.database_host,
                                    port = self.__db_model.database_port)
        except Exception as e:
            print("Error while creating connection : {}".format(e))
            conn = None
        return conn

    '''
    If you want to create a new connection,
    use this method without any parameter
    
    e.g. connection = DBUtil().get_connection()
    
    
    It is sometimes needed to reuse the same connection if you want to execute multiple methods in transaction
    in that way, you have to create all the methods with a input parameter as old connection.
     
    If your method is accepting the old connection as input parameter 
    and you are not sure the passed connection is valid or not,
    you can pass the old connection to "get_connection" method
    e.g. connection = DBUtil().get_connection(old_connectiom)
    
    if validates the passes connection is none or not
    1. if passed old connection is not None, it returns the old connection
    2. if passed old connection is None, it creates new connection and returns it 
    '''

    '''
        Example to use transaction with connection
        ----------------------------------------
                connection = get_connection(None)
                trans = connection.begin()
                try:
                    r1 = connection.execute(table1.select())
                    connection.execute(table1.insert(), col1=7, col2='this is some data')
                    trans.commit()
                except:
                    trans.rollback()
                    raise
                close_connection(None, connection)

        -----------------------------------------
        '''

    def get_connection(self, old_connection=None):
        if old_connection:
            return old_connection
        else:
            return self.__engine.connect()

    '''
    This method is used to close the existing connection
    e.g. connection = DBUtil().get_connection(connection=existing_connection)
    
    
    If your method is getting connection as parameter 
    and you have created connection using the old connection
    It is not correct the close the connection as it belongs to the caller method
    in that case, you can use this method with passing old_connection
    
    e.g. connection = DBUtil().get_connection(connection=existing_connection,old_connection=old_connection)
    '''

    def close_connection(self, old_connection=None, connection=None):
        if not old_connection and connection:
            connection.close()
        return None


# class SQLUtil:
#
#     __db = DBUtil()
#
#     def exeute_query(self, sql, connection = None):
#         new_connection = self.__db.get_connection(connection)


