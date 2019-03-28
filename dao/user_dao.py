from util import util
from dao.base_dao import BaseDao
from datetime import datetime


class UserDao(BaseDao):

    __user_id = None

    __user_creation_fields = ['given_name', 'last_name',
                              'dob', 'email', 'password', 'user_type', 'created_date', 'created_by',
                              ]

    __user_profile_fields = ['user_id' , 'gender', 'ethnicity', 'address_line_1', 'address_line_2', 'city', 'state',
                             'country_of_residence', 'country_of_citizenship', 'zip', 'phone']

    __user_login_fields = ['id', 'given_name', 'last_name', 'user_type']

    __user_organizations_fields = ['organization_id', 'user_role']

    __user_all_details_sql = "SELECT ub.id, ub.given_name, ub.last_name, ub.user_type, up.gender, up.ethnicity, " \
                             "up.address_line_1, up.address_line_2, up.city, up.state, up.country_of_residence, " \
                             "up.country_of_citizenship, up.zip, up.phone " \
                             "from  user_basic ub " \
                             "JOIN user_profile up ON ub.id = up.user_id" \
                             "where ub.delete_flag = 0 and up.delete_flag = 0"

    def __init__(self, user_id, file_path='./config/config.yaml'):
        self.__user_id = user_id
        super(UserDao, self).__init__(file_path=file_path)

    def create_user(self, data=None, model_instance=None, fields=None, old_connection=None):
        if model_instance:
            data = util.model_to_json(model_instance)
        if not fields:
            fields = self.__user_creation_fields
        data['created_by'] = self.__user_id
        data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return self.insert_records('user_basic', fields=fields, args_dict=data, connection=old_connection)

    def validate_user(self, data=None, fields=None):
        if not data:
            return None
        if not fields:
            fields = self.__user_login_fields
        where = "email = %(email)s and password = %(password)s"
        return self.get_data(table_name="user_basic", args_dict=data, fields=fields, where=where)

    def save_user_profile(self, data=None, fields=None):
        if not data:
            return None
        if not fields:
            fields = self.__user_profile_fields
        if data['user_id'] <= 0:  #new profile creation
            fields.append('created_date')
            fields.append('created_by')
            data['created_by'] = self.__user_id
            data['created_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return self.insert_records(table_name="user_profile", args_dict=data, fields=fields)
        else:  # profile update
            where = "user_id =  %(user_id)s "
            fields.append('modified_date')
            fields.append('modified_by')
            data['modified_by'] = self.__user_id
            data['modified_date'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return self.update_record(table_name="user_profile", args_dict=data, fields=fields, where=where)

    def add_user_organization(self, data=None, fields=None):
        if not data:
            return None
        if not fields:
            fields = self.__user_organizations_fields

        return self.insert_records(table_name="user_organization_mapping", args_dict=data, fields=fields)

    def ger_user_info(self, data=None):
        if not data:
            return None

        ret = {}
        sql = self.__user_all_details_sql

        if data.get('user_id', '') != '':
            sql = sql + " and ub.id like  %(user_id)s%"
        else:
            if data.get('email', '') != '':
                sql= sql + " and ub.email like  %(email)s%"

            if data.get('given_name', '') != '':
                sql= sql + " and ub.given_name = %(given_name)s%"

            if data.get('last_name') == '':
                sql = sql + " and ub.last_name = %(last_name)s%"

            if data.get('address_line_1', '') == '':
                sql = sql + " and up.address_line_1 = %(address_line_1)s%"

            if data.get('zip', '') == '':
                sql = sql + " and up.zip = %(zip)s%"

        user_info_arr = self.fetch_data(sql=sql, data=data)
        ret['user_info'] = user_info_arr

        if data.get('user_id', '') != '' and data.get('type') == 'full':
            if len(user_info_arr) == 1:
                user_info = user_info_arr[0]
                ret['user_info'] = user_info
                if user_info and user_info.get('id'):
                    data1 = {'user_id': user_info.get('id')}
                    ret['user_organizations'] = self.get_user_organizations(data=data1)
        return ret

    def get_user_organizations(self, data=None):
        where = " user_id =  %(user_id)s and delete_flag = 0"
        user_organizations = self.get_data(table_name='user_organization_mapping', fields=self.__user_organizations_fields, data=data, where=where)
        return  user_organizations










