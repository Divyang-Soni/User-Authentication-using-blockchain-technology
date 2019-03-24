from util import util
from models.organization import OrganizationDetails, OrganizationBranch
from dao.base_dao import BaseDao
from datetime import datetime


class OrganizationDao(BaseDao):

    __org_id = None
    __user_id = None

    __organization_details_fields = ['name', 'address_line_1', 'address_line_2'
                                     'city', 'state', 'country', 'zip', 'phone', 'headquarter',
                                     'founded_date', 'organization_type', 'created_date', 'created_by']

    __organization_branch_fields = ['organization_id', 'address_line_1', 'address_line_2',
                                    'city', 'state', 'country', 'zip',
                                    'phone', 'created_date', 'created_by']

    def __init__(self, org_id, user_id):
        self.__org_id = org_id
        self.__user_id = user_id
        BaseDao.__init__(self)

    def create_organization(self, data=None, model_instance=None, fields=None, old_connection=None):
        if model_instance:
            data = util.model_to_json(model_instance)
        if not fields:
            fields = self.__organization_details_fields
            data['created_by'] = self.__user_id
            data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return self.insert_single_record('organization_details', fields=fields, args_dict=data,
                                         connection=old_connection)

    def add_organization_branch(self, data=None, model_instance=None, fields=None, old_connection=None):
        if model_instance:
            data = util.model_to_json(model_instance)
        if not fields:
            fields = self.__organization_branch_fields
        return self.insert_single_record('organization_branch', fields=fields, args_dict=data,
                                         connection=old_connection)

    def get_organization_details(self, org_id=None, old_connection=None, fields='*', where='1=1'):
        sql = self.create_select_query('organization_details', fields=fields, where=where)
        params = []
        if not org_id:
            org_id = self.__org_id
        if not org_id:
            return self.get_data('organization_details', sql=sql,  fields=fields, connection=old_connection,
                                 model=OrganizationDetails)
        else:
            params.append(org_id)
            if where == '1=1':
                where = ' id = %s'
            return self.get_data('organization_details', sql=sql, fields=fields, where=where,
                                 args_dict=params, connection=old_connection,
                                 model=OrganizationDetails)

    def get_organization_branches(self, org_id=None, old_connection=None, fields='*'):
        if not org_id:
            org_id = self.__org_id
        if not org_id:
            raise Exception("No Organization Id found to fetch branches.")

        sql = self.__select_branches
        params = [org_id]
        where = 'organization_id = %s'
        return self.get_data('organization_branch', fields=fields, where=where,
                             args_dict=params, connection=old_connection,
                             model= OrganizationBranch)


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
            raise Exception("No Organization Id found to fetch details.")

        organization = {}
        organization['details'] = self.get_organization_details(id=org_id, connection=connection)
        organization['branches'] = self.get_organization_branches(id=org_id, connection=connection)

        self.__db_util.close_connection(connection, old_connection=old_connection)

        return organization




