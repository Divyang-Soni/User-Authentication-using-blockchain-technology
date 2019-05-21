from flask import session
from services.base_service import BaseService
from dao.user_dao import UserDao
from util import encryption, BlockChainApi
from util.util import init_logging
import json
import traceback


class UserService(BaseService):

    __UserDao = None

    def __init__(self, session, params, execution, enforce_session):
        super(UserService, self).__init__(session, params, execution, enforce_session)
        self.__logging = init_logging()
        self.__UserDao = UserDao(self._user_id, self._user_type)

    #  a base method which will internally call validate method
    #  witget_all_request_statush required params for each service
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
                ef = traceback.format_exc()
                self.__logging.error("Error while processing request:\n%s ", ef)
                self._message = 'failed'
                self._error = ef
                return e
        else:
            self._error = "Function is not implemented."
            self._message = 'failed'
            return None

    def create_user(self):
        if self.is_duplicate_user():
            self._error = "User with name {} is already exist.".format(self._params['name'])
        id = self.__UserDao.create_user(self._params)
        if id > 0:
            self._params['organization_id'] = self._organization_id
            self._params['user_id'] = id
            self._params['user_role'] = self._params['user_type']
            self.add_user_organization()
            if not BlockChainApi.create_user_initial_block(id):
                self._message = 'failed'
        else:
            self._message = 'failed'

    def login(self):
        user = self.__UserDao.validate_user(data=self._params)
        if user and len(user) == 1:
            self._message = 'success'
            self._response_data = json.dumps(user[0])
            session['ux'] = encryption.encrypt(user[0].get('id'))
            session['ty'] = encryption.encrypt(user[0].get('user_type'))

            # session['ogx'] = encryption.encrypt(user[0].get('user_type'))
        else:
            self._message = 'failed'

    def save_user_profile(self):
        if self.__UserDao.save_user_profile(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def add_user_organization(self):
        if self.__UserDao.is_normal_user(self._user_id):
            raise Exception("This action is not permitted for the user.")
        self._params['organization_id'] = self._organization_id
        if self.__UserDao.add_user_organization(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def get_user_info(self):

        if self._params.get('user_id', '') != 'current' and \
                self.__UserDao.is_normal_user(self._user_id):
            raise Exception("This action is not permitted for the user.")

        info = self.__UserDao.get_user_info(data=self._params)
        if info and info != {}:
            self._message = 'success'
            if session.get('od', '') == '' and info['user_info'] and info['user_info']['organization_id']:
                session['od'] = encryption.encrypt(info['user_info']['organization_id'])
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
            return info
        else:
            self._message = 'failed'
        return True

    def add_user_record(self):
        if BlockChainApi.add_user_data(self._params['block_data'], self._params['user_id'], self._user_id, self._organization_id):
            self._message = 'success'
        else:
            self._message = 'failed'

    def get_user_record(self):
        if not self._params['user_id']:
            self._message = 'failed'
            self._error = "Invalid request."
            return

        if not self.__UserDao.is_user_admin(self._user_id) and int(self._params['user_id']) != self._user_id:
            self._message = 'failed'
            self._error = "Unauthorised request."
            return

        data = BlockChainApi.request_data(self._params['user_id'], self._params.get('record_type', ''), \
                                          self._params.get('st', ''), self._params.get('et', ''))
        if data:
            self._response_data = data
            self._message = 'success'
        else:
            self._message = 'failed'

    def get_approved_request_data(self):
        self._params['from_id'] = self._user_id
        request_content = self.__UserDao.get_request_content(self._params)
        if request_content and len(request_content) > 0:
            request_content = request_content[0]
            status = int(request_content.get('status', '0'))
            if status != 1:
                self._message = "failed"
                self._error = "Request is not approved"
                return
            else:
                data = BlockChainApi.request_data(request_content.get('for_id'),
                                                  request_content.get('data_category', ''),
                                                  self._params.get('st', ''), self._params.get('et', ''))
                self._message = 'success'
                self._response_data = data
                return

        self._message = "failed"
        self._error = "Error while retrieving request information."
        return

    def request_user_records(self):
        if self.__UserDao.is_normal_user(self._user_id):
            raise Exception("This action is not permitted for the user.")

        if self.__UserDao.request_user_data(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'

    def logout(self):
        session.clear()
        self._message = 'success'

    def get_all_data_request(self):
        info = self.__UserDao.get_all_data_request(self._params)
        if info and len(info) > 0:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'

    def get_all_request_status(self):
        info = self.__UserDao.get_all_request_status(self._params)
        if info:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'

    def get_block_types(self):
        info = self.__UserDao.get_block_types()
        if info and len(info) > 0:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'

    def approve_data_request(self):
        if self._params:
            self._params['status'] = 1
            if self.__UserDao.respose_user_data_request(self._params):
                self._message = 'success'
                return True
        self._message = 'failed'

    def deny_data_request(self):
        if self._params:
            self._params['status'] = 2
            if self.__UserDao.respose_user_data_request(self._params):
                self._message = 'success'
                return True
        self._message = 'failed'

    def remove_user_from_organization(self):
        if self._params:
            if self.__UserDao.remove_user_from_organization(self._params):
                self._message = 'success'
                return
        self._message = 'failed'




