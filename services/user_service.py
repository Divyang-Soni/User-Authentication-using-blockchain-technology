from services.base_service import BaseService
from dao.user_dao import UserDao
import json

class UserService(BaseService):

    __UserDao = None

    def __init__(self, session, params, execution):
        super(UserService, self).__init__(session, params, execution)
        self.__UserDao = UserDao(self._user_id)

    # a base method which will internally call validate method with required params for each service
    def validate_params(self):
        return True

    # a base method which will be implemented in every service to parse params
    def parse_params(self):
        return True

    # a base method which will trigger the actual code
    def process_request(self):
        if hasattr(self, self._execution):
            func = getattr(self, self._execution)
            func()
        else:
            raise Exception("Function is not implemented.")

    def create_user(self):
        if self.__UserDao.create_user(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def login(self):
        user = self.__UserDao.validate_user(data=self._params)
        self._message = json.dumps(user)

    def save_user_profile(self):
        if self.__UserDao.save_user_profile(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def add_user_organization(self):
        if self.__UserDao.add_user_organization(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def ger_user_info(self):
        info = self.__UserDao.ger_user_info(data=self._params)
        self._message = json.dumps(info)
