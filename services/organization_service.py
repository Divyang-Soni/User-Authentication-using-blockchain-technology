from services import base_service


class CompanyData(base_service):

    def __init__(self, session, params):
        pass

    # a base method which will internally call validate method with required params for each service
    def validate_params(self):
        pass

    # a base method which will be implemented in every service to parse params
    def parse_params(self):
        pass

    # a base method which will trigger the actual code
    def process_request(self):
        pass