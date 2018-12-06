from services.base_service import BaseService
from dao.UserDao import UserDao


class UserService(BaseService):

    def __init__(self, session, params):
        BaseService.__init__(session, params)

    # a base method which will internally call validate method with required params for each service
    def validate_params(self):
        return True

    # a base method which will be implemented in every service to parse params
    def parse_params(self):
        return True

    # a base method which will trigger the actual code
    def process_request(self):
        UserDao(0).create_user(self.params)
        self._message = 'success'
