import http.client
import ssl
import json
import requests
from util.util import init_logging


logging = init_logging()


class RequestMethod:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"


def http_request(method, url, data, endpoint):
    response = None
    logging.info("http_request data: %s", data)
    if method == RequestMethod.POST:
        response = requests.post(url+endpoint, json=data)
    elif method == RequestMethod.PUT:
        response = requests.put(url+endpoint, json=data)
    elif method == RequestMethod.GET:
        response = requests.get(url+endpoint, data)
    else:
        logging.error("invalid request method: %s ", method)

    if response:
        logging.info("response from block chain status: %s, response data : %s ", response.status_code, response.json())
        if response.status_code == http.HTTPStatus.OK:
            if method == "GET":
                logging.info("response from block chain: %s ", response.json())
                return response.json()
            return True
    return False

# def post_data(method, url, data, endpoint):
#     connection = http.client.HTTPSConnection(url, context=ssl.SSLContext.load_cert_chain())
#     headers = {'Content-type': 'application/json'}
#
#     if data:
#         data = json.dumps(data)
#         connection.request(method, endpoint, data, headers)
#         response = connection.getresponse()
#         print()
#         if response.code == http.HTTPStatus.OK:
#             if response.read():
#                 return response.read().decode()
#             return True
#     return False
#
#
# def request_data(method, url, data, endpoint):
#     connection = http.client.HTTPSConnection(url)
#     headers = {'Content-type': 'application/json'}
#     if data:
#         data = json.dumps(data)
#         connection.request(method, endpoint, data, headers)
#         response = connection.getresponse()
#         if response.code == http.HTTPStatus.OK and response.read():
#             return response.read().decode()
#     return False




