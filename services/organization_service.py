from services.base_service import BaseService
from dao.organization_dao import OrganizationDao
from dao.user_dao import UserDao


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
            func()
        else:
            self._error = "Function is not implemented."
            self._message = 'failed'

    def signup_organization(self):

        user_data = dict
        user_data['given_name'] = self._params['name']
        user_data['last_name'] = 'Organization'
        user_data['dob'] = self._params['founded_date']
        user_data['email'] = self._params['email']
        user_data['password'] = self._params['name']
        user_data['user_type'] = 1

        if self.__dao.create_organization(data=self._params):
            if UserDao(self._user_id).create_user(data=user_data):
                self._message = 'success'
                return
        self._message = 'failure'



