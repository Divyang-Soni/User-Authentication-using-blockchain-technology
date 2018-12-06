from services import base_service
from dao.UserDao import UserDao


class UserData(base_service):

    userdao = None

    def __init__(self, session, params):
        base_service.__init__(session, params)

    # a base method which will internally call validate method with required params for each service
    def validate_params(self):
        pass

    # a base method which will be implemented in every service to parse params
    def parse_params(self):
        pass

    # a base method which will trigger the actual code
    def process_request(self):
        self.userdao = UserDao(0)
        self.userdao.create_user(self.params)
