
from models.organization import OrganizationDetails, OrganizationBranch
from dao.base_dao import BaseDao


class OrganizationDao(BaseDao):

    __org_id = None

    __select_sql = "SELECT %s FROM organization_details where id = %s and delete_flag = 0"
    __select_all_sql = "SELECT * FROM organization_details where delete_flag = 0"
    __insert_sql = "INSERT INTO organization_details " \
                      " VALUES (%(name)s,%(address_line_1)s,%(city,state)s,%(country)s,%(zip)s," \
                      " %(phone)s,%(headquarter)s,%(founded_date)s,%(organization_type)s," \
                      " %(created_date)s,%(created_by)s,%(modified_date)s,%(modified_by)s," \
                      " %(delete_flag)s,%(deleted_by)s)"

    __branch_details_fields = "(name,address_line_1,city,state,country,zip," \
                              " phone,,headquarter,founded_date,organization_type," \
                              " created_date,created_by,,modified_date,modified_by," \
                              " delete_flag,deleted_by)"

    __select_branches = "SELECT %s FROM organization_branch WHERE organization_id = %s and delete_flag = 0"

    def __init__(self, org_id):
        self.__org_id = org_id
        super()

    def get_organization_details(self, org_id=None, old_connection=None, fields='*'):
        sql = self.__select_sql

        params = [fields]

        if not org_id:
            org_id = self.__org_id
        if not org_id:
            sql = self.__select_all_sql
        else:
            params.append(org_id)
        return self.__sql_util.fetch_data(sql, args_dict=params, connection=old_connection, model=OrganizationDetails)


    def get_organization_branches(self, org_id=None, old_connection=None, fields='*'):
        if not org_id:
            org_id = self.__org_id
        if not org_id:
            raise "No Organization Id found to fetch branches."

        sql = self.__select_branches
        params = [fields, org_id]
        return self.__sql_util.fetch_data(sql, args_dict=params, connection=old_connection, model=OrganizationBranch)

    '''
    This function is used to get all information about an organization which includes
    1. Organization Details
    2. Organization Branches
    '''
    def get_organization_all_details(self, org_id=None, old_connection=None):
        # Creating connection
        connection = self.__db_util.get_connection(old_connection=old_connection)

        # if organization id is not passed, use the object level organization id is available
        if not org_id:
            org_id = self.__org_id
        if not org_id:
            raise "No Organization Id found to fetch details."

        organization = {}
        organization['details'] = self.get_organization_details(id=org_id, connection=connection)
        organization['branches'] = self.get_organization_branches(id=org_id, connection=connection)

        connection = self.__db_util.close_connection(connection, old_connection=old_connection)

        return organization




