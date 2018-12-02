from dbutil.dbutil import SQLUtil


class BaseDao(SQLUtil):

    def __init__(self, file_path='./config/config.yaml'):
        SQLUtil.__init__(self, file_path=file_path)

    @staticmethod
    def create_insert_query(table_name, fields):

        if not fields or type(fields) is not type([]):
            raise BaseException("Fileds must be a dictonary object")

        values = ','.join("%("+l+")s" for l in fields)
        str_fields = ','.join(fields)

        return "INSERT INTO {} ({}) VALUES({})".format(table_name, str_fields, values)

    def insert_records(self, table_name, fields, args_dict, connection = None):
        sql = self.create_insert_query(table_name, fields)
        return self.execute_query(sql, args_dict=args_dict, connection=connection)

    @staticmethod
    def create_single_insert_query(table_name, fields):

        if not fields or type(fields) is not list:
            raise BaseException("Fileds must be a dictonary object")

        values = ','.join("%s" for l in fields)
        str_fields = ','.join(fields)

        return "INSERT INTO {} ({}) VALUES({})".format(table_name, str_fields, values)

    def insert_single_record(self, table_name, fields, args_dict, connection = None):
        sql = self.create_single_insert_query(table_name, fields)
        return self.execute_query(sql, args_dict=args_dict, connection=connection)


    @staticmethod
    def create_single_update_query(table_name, fields, where='1=1'):
        if not fields or type(fields) is not list:
            raise BaseException("Fileds must be a dictionary object")

        str_fields = ','.join(l + '=%s' for l in fields)
        return "UPDATE TABLE {} SET {} WHERE {}}".format(table_name, str_fields, where)

    def update_single_record(self, table_name, fields, args_dict = None, where='1=1', connection = None):
        sql = self.create_single_update_query(table_name, fields, where=where)
        return self.execute_query(sql, args_dict=args_dict, connection=connection)

    @staticmethod
    def create_update_query(table_name, fields, where='1=1'):
        if not fields or type(fields) is not list:
            raise BaseException("Fileds must be a dictionary object")
        str_fields = ','.join(l +"=%(" + l + ")s" for l in fields)
        return "UPDATE TABLE {} SET {} WHERE {}}".format(table_name, str_fields, where)

    def update_single_record(self, table_name, fields, args_dict = None, where='1=1',connection=None):
        sql = self.create_update_query(table_name, fields, where=where)
        return self.execute_query(sql, args_dict=args_dict, connection=connection)

    @staticmethod
    def create_single_update_query(table_name, fields, where='1=1'):
        if not fields or type(fields) is not list:
            raise BaseException("Fileds must be a dictionary object")

        str_fields = '=%s,'.join(fields)
        str_fields += '= %s'
        return "UPDATE TABLE {} SET {} WHERE {}}".format(table_name, str_fields, where)

    def update_single_record(self, table_name, fields, args_dict, connection=None):
        sql = self.create_single_insert_query(table_name, fields)
        return self.execute_query(sql, args_dict=args_dict, connection=connection)

    @staticmethod
    def create_select_query(table_name, fields='*', where='1=1'):
        str_fields = ','.join(fields)
        return "SELECT {} FROM {} WHERE {}".format(str_fields, table_name, where)

    def get_data(self, table_name, fields='*', where='1=1', args_dict=None, connection=None, model=None):
        sql = self.create_select_query(table_name, fields=fields, where=where)
        return self.fetch_data(sql, args_dict=args_dict, connection=connection, model=model)
