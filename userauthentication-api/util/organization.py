from util import dbutil

class Organization:

    __id = None
    __sql_util = None

    __select_sql = "SELECT * FROM organization_details where id = %s and delete_flag = 0"
    __select_all_sql = "SELECT * FROM organization_details where delete_flag = 0"
    __insert_sql = "INSERT INTO organization_details " \
                      " (name,address_line_1,city,state,country,zip," \
                      " phone,,headquarter,founded_date,organization_type," \
                      " created_date,created_by,,modified_date,modified_by," \
                      " delete_flag,deleted_by) " \
                      " VALUES (%(name)s,%(address_line_1)s,%(city,state)s,%(country)s,%(zip)s," \
                      " %(phone)s,%(headquarter)s,%(founded_date)s,%(organization_type)s," \
                      " %(created_date)s,%(created_by)s,%(modified_date)s,%(modified_by)s," \
                      " %(delete_flag)s,%(deleted_by)s)"

    def __init__(self, id):
        self.__id = id
        self.__sql_util = dbutil.SQLUtil()

    def get_organization_data(self, id=None):
        if not id:
            id = self.__id

