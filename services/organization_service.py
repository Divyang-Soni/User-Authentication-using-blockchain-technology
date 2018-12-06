from services.base_service import BaseService


class CompanyData(BaseService):

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
