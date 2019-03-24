from flask import request
from abc import abstractmethod
'''
This class is a base service which has skeleton code which needs to be followed by all service
Basically all the service will extend this class and will override 2=3 abstract methods
    1. validate_params : This method will internally call the validate method with required param lisy
    2. parse_params : This method will parse required parsed data from the params
    3. process_request : This method will process the request and return response data
'''


class BaseService:

    # This param will define that the session for this request is valid or not
    # it is a private variable
    _is_valid = False
    _params = None
    _message = None
    _execution = None
    _user_id = 0

    # initializing base service and putting params in it
    # checking the validity of session and setting the valid param
    def __init__(self, session, params, execution):
        self._params = params
        self._execution = execution
        self.validate_session(session)

    # checking uid is available in session or not
    # TODO : This method needs to be changed with proper checking
    def validate_session(self, session):
        self._is_valid = True
        return True
        # if "uid" not in session:
        #     self._is_valid =  False
        # else:
        #     self._is_valid = True

    # public method to check that the session is valid or not
    def is_valid_session(self):
        return self._is_valid

    # Method which will validate the required fields are available in
    def validate(self, required):
        if not self._is_valid:
            return False

        for require in required:
            if require not in self._params:
                return False
        return True

    def get_message(self):
        return self._message

    # a base method which will internally call validate method with required params for each service
    @abstractmethod
    def validate_params(self):
        pass

    # a base method which will be implemented in every service to parse params
    @abstractmethod
    def parse_params(self):
        pass

    # a base method which will trigger the actual code
    @abstractmethod
    def process_request(self):
        pass
