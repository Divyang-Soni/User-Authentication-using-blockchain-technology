from services.base_service import BaseService
from dao.organization_dao import OrganizationDao
from dao.user_dao import UserDao


class OrganizationService(BaseService):

    def __init__(self, session, params, execution):
        super(OrganizationService, self).__init__(session, params, execution)

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

    def signup_organization(self):
        if OrganizationDao(1, 1).create_organization(data=self._params):
            userData = {}
            userData['given_name'] = self._params['name']
            userData['last_name'] = 'Organization'
            userData['dob'] = self._params['founded_date']
            userData['email'] = self._params['email']
            userData['password'] = self._params['name']
            userData['user_type'] = 1
            if UserDao(1).create_user(data=userData):
                self._message = 'success'
                return
        self._message = 'failure'

