from util import util
from dao.base_dao import BaseDao


class UserDao(BaseDao):

    __user_id = None

    __user_basic_fields = ['given_name', 'last_name',
                           'dob', 'email', 'password', 'user_type', 'created_date', 'created_by',
                           ]

    def __init__(self, user_id, file_path='./config/config.yaml'):
        self.__user_id = user_id
        super(UserDao, self).__init__(file_path=file_path)

    def create_user(self, data=None, model_instance=None, fields=None, old_connection=None):
        if model_instance:
            data = util.model_to_json(model_instance)
        if not fields:
            fields = self.__user_basic_fields
        return self.insert_single_record('user_basic', fields=fields, args_dict=data, connection=old_connection)



