import json

'''
This class is responsible to provide return message for each request
Every requiest will return 3 parameters
    1. status - It will determine the status of the request process (default : 200)
    2. message - It will determine the error message if any (default blank)
    3. data - its a json field which can be used in terms of sending any data in response of the request (default empty json)    
'''


class Message:
    status = None
    message = None
    data = None

    def __init__(self, status="200", message="", data={}):
        self.status = status
        self.message = message
        self.data = data

    def get_json(self):
        return json.dumps(self.__dict__)