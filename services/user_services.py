from services.base_service import BaseService
from dao.UserDao import UserDao


class UserService(BaseService):

    def __init__(self, session, params, execution):
        super(UserService, self).__init__(session, params, execution)

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

    def create_user(self):
        if UserDao(self._user_id).create_user(self._params):
            self._message = 'success'
        else:
            self._message = 'failed'
