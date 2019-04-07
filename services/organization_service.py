from services.base_service import BaseService
from dao.organization_dao import OrganizationDao
from dao.user_dao import UserDao
import json
import traceback


class OrganizationService(BaseService):

    __dao = None

    def __init__(self, session, params, execution, enforce_session):
        super(OrganizationService, self).__init__(session, params, execution, enforce_session)
        self.__dao = OrganizationDao(self._user_id, self._organization_id)

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

    def signup_organization(self):

        user_data = dict
        user_data['given_name'] = self._params['name']
        user_data['last_name'] = 'Organization'
        user_data['dob'] = self._params['founded_date']
        user_data['email'] = self._params['email']
        user_data['password'] = self._params['name']
        user_data['user_type'] = 2

        user_dao = UserDao(self._user_id)

        if user_dao.is_duplicate_user(user_data):
            self._message = 'failure'
            self._error = "Organization with name {} is already exist.".format(self._params['name'])
            return

        if self.__dao.create_organization(data=self._params):
            if user_dao.create_user(data=user_data):
                self._message = 'success'
                return
        self._message = 'failure'

    def get_organization_types(self):
        info = self.__dao.get_organization_types()
        if info and len(info) > 0:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'

    def get_organization_details(self):
        if self._params.get('organization_id', '') == '':
            self._params['organization_id'] = self._organization_id

        if self._params.get('type', '') == 'full':
            info = self.__dao.get_organization_all_details(org_id=self._params['organization_id'])
        else:
            info = self.__dao.get_organization_details(org_id=self._params['organization_id'])

        if info:
            self._message = 'success'
            self._response_data = json.dumps(info)
        else:
            self._message = 'failed'


