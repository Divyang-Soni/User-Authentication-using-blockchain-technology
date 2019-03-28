import psycopg2
import sqlalchemy as sql
from util import config, util
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
    2. Create database connection pool
    3. provide database connection
    '''
    def __init__(self,file_path="./config/config.yaml"):
        # code to read database config and create database model
        self.__get_database_config(file_path)
        if self.__db_model:
            self.__create_engine()

    def __get_database_config(self, config_file):
        cfg = config.Config(file_path=config_file)
        db_config = cfg.get_section('database')
        if db_config:
            self.__db_model = database.DBModel()
            self.__db_model.database_port = db_config['database_port']
            self.__db_model.database_host = db_config['database_host']
            self.__db_model.database_name = db_config['database_name']
            self.__db_model.user_name = db_config['user_name']
            self.__db_model.password = db_config['password']
            self.__db_model.pool_size = db_config['pool_size']
            self.__db_model.pool_timeout = db_config['pool_timeout']

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

    def is_engine_created(self):
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
                connection = get_connection()
                trans = connection.begin()
                try:
                    r1 = SQLUtil().execute_query(sql, connection)
                    trans.commit()
                except:
                    trans.rollback()
                    raise
                close_connection(None, connection)

        -----------------------------------------
        '''
    def get_connection(self, old_connection=None):
        if old_connection and not old_connection.closed:
            return old_connection
        else:
            return self.__engine.connect()

    '''
    This method is used to close the existing connection
    e.g. connection = DBUtil().close_connection(existing_connection)
    
    
    If your method is getting connection as parameter 
    and you have created connection using the old connection
    It is not correct the close the connection as it belongs to the caller method
    in that case, you can use this method with passing old_connection
    
    e.g. connection = DBUtil().close_connection(existing_connection,old_connection=old_connection)
    '''
    def close_connection(self, connection, old_connection=None):
        if old_connection and not old_connection.closed:
            return None
        elif connection:
            connection.close()
            return None


class SQLUtil:

    __db = None

    def __init__(self, file_path):
        self.__db = DBUtil(file_path=file_path)
    '''
    This function is used to fetch data using query
    @sql : sql query to fetch data 
    @args_dict (Optional): if passed query contains parameters, we must have argument dictionary to get parameters
    @connection (Optional): if you want to use existing connection which you have
    @model (Optional): if you have model specific to the sql table and want to get dictionary of the o/p rows instead of dict of json,
                you can pass the model. 
    Note :  the passes model must have all the fields with the same name  
    
    example :
    
    data = SQLUtil().fetch_data("select 1 as count")
    # data = [{count:1}]
    
    data = SQLUtil().fetch_data("select 1 as count", connection=con)
    # data = [{count:1}]
    
    data = SQLUtil().fetch_data("select name,id from users where id = %s", args_dict=(1))
    # data = [{name: divyang, id : 1 }]
    
    data = SQLUtil().fetch_data("select name,id from users where id = %s", args_dict=(1), model=user)
    # data = [user(name: divyang, id : 1)]
    '''

    def fetch_data(self, sql, args_dict=None, connection=None, model=None):
        try:
            new_connection = self.__db.get_connection(old_connection=connection)
            if new_connection:
                ret = []

                # check is arguments are passed and its parameterised query
                if args_dict:
                    cur = new_connection.execute(sql, args_dict)
                else:
                    cur = new_connection.execute(sql)
                keys = cur.keys()

                # iterate through the cursor are put the records in output dict
                for record in cur:
                    # if model is passed
                    dict = {}
                    for index, elem in enumerate(keys):
                        dict[elem] = record[index]

                    if model:
                        data = util.json_to_model(dict, model())
                        ret.append(data)
                    else:
                       ret.append(dict)

                self.__db.close_connection(new_connection, old_connection=connection)
                return ret
        except Exception as e:
            print("Error while fetching data : {}".format(e))
        return None

    '''
    This function is used to fetch data using query
    @sql : sql query to fetch data ()
    @args_dict (Optional): if passed query contains parameters, we must have argument dictionary to get parameters
    @connection (Optional): if you want to use existing connection which you have
    
    example :

    data = SQLUtil().execute_query("update user set anme = "divyang" where id = 1")
    # data = True 

    data = SQLUtil().execute_query("update user set anme = "divyang" where id = 1", connection=con)
    # data = True

    data = SQLUtil().fetch_data("update user set anme = "divyang" where id = %s", args_dict=(1))
    # data = True
    
    data = SQLUtil().fetch_data("update user set anme = "divyang" where id = %s")
    # data = False  (as arguments not passed)

    '''
    def execute_query(self, sql, args_dict=None, connection=None):
        try:
            new_connection = self.__db.get_connection(connection)
            if new_connection:
                if args_dict:
                    new_connection.execute(sql, args_dict)
                else:
                    new_connection.execute(sql)
                self.__db.close_connection(new_connection, old_connection=connection)
        except Exception as e:
            print("Error while executing query : {}".format(e))
            return False
        return True

    '''
    This function is used to fetch data using query
    @sql : sql query to fetch data ()
    @args_dict (Optional): if passed query contains parameters, we must have argument dictionary to get parameters
    @connection (Optional): if you want to use existing connection which you have

    example :

    data = SQLUtil().execute_query_multiple("update user set name = "divyang" where id = 1")
    # data = True 

    data = SQLUtil().execute_query_multiple("update user set name = "divyang" where id = 1", connection=con)
    # data = True
    users = (
            {id=1, name=divyang1},
            {id=2, name=divyang2},
            {id=3, name=divyang3}
            )
            
    data = SQLUtil().execute_query_multiple("update user set name = "divyang" where id = %(id)s", args_dict=users)
    # data = True
    ## Note : in this example the dynamic field %(id)s means getting id field from the users entry

    data = SQLUtil().fetch_data("update user set name = "divyang" where id = %(id)s")
    # data = False  (as arguments not passed)
    '''

    def execute_query_multiple(self, sql, args_dict=None, connection=None):
        try:
            new_connection = self.__db.get_connection(connection)
            if new_connection:
                if args_dict:
                    new_connection.execute(sql, args_dict)
                else:
                    new_connection.execute(sql)
                self.__db.close_connection(new_connection, old_connection=connection)
        except Exception as e:
            print("Error while executing query : {}".format(e))
            return False
        return True
