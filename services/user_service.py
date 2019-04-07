from flask import session
from services.base_service import BaseService
from dao.user_dao import UserDao
import json
import traceback


class UserService(BaseService):

    __UserDao = None

    def __init__(self, session, params, execution, enforce_session):
        super(UserService, self).__init__(session, params, execution, enforce_session)
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
            try:
                func()
            except Exception as e:
                traceback.format_exc(e)
                self._message = 'failed'
                self._error = e.__str__()
                return e
        else:
            self._error = "Function is not implemented."
            self._message = 'failed'
            return None

    def create_user(self):
        if self.__UserDao.create_user(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def login(self):
        user = self.__UserDao.validate_user(data=self._params)
        if user and len(user) == 1:
            self._message = 'success'
            self._response_data = json.dumps(user[0])
            session['uid'] = user[0].get('id')
            session['type'] = user[0].get('user_type')
        else:
            self._message = 'failed'

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
        if info and info != {}:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'

    def get_user_types(self):
        info = self.__UserDao.get_user_types()
        if info and len(info) > 0:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'

    def is_duplicate_user(self):
        info = self.__UserDao.is_duplicate_user(self._params)
        if info is not None:
            self._message = 'success'
            self._response_data = info
        else:
            self._message = 'failed'

    def add_user_record(self):
        self._message = 'success'
