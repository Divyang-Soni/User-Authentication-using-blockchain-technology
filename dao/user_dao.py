from util import util
from dao.base_dao import BaseDao
from datetime import datetime


class UserDao(BaseDao):

    __user_id = None

    __user_creation_fields = ['given_name', 'last_name',
                              'dob', 'email', 'password', 'user_type', 'created_date', 'created_by',
                              ]

    __user_login_fields = ['id', 'given_name', 'last_name', 'user_type']

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
        return self.insert_single_record('user_basic', fields=fields, args_dict=data, connection=old_connection)

    def validate_user(self, data=None, fields=None):
        if not data:
            return None
        if not fields:
            fields = self.__user_login_fields
            where = "email = %(email)s and password = %(password)s"
        return self.get_data(table_name="user_basic", args_dict=data, fields=fields, where=where)







