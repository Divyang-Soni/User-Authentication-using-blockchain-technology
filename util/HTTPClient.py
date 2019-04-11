import http.client
import json


def post_data(method, url, data, endpoint):
    connection = http.client.HTTPSConnection(url)
    headers = {'Content-type': 'application/json'}

    if data:
        data = json.dumps(data)
        connection.request(method, endpoint, data, headers)
        response = connection.getresponse()
        print()
        if response.code == http.HTTPStatus.OK:
            if response.read():
                return response.read().decode()
            return True
    return False


def request_data(method, url, data, endpoint):
    connection = http.client.HTTPSConnection(url)
    headers = {'Content-type': 'application/json'}
    if data:
        data = json.dumps(data)
        connection.request(method, endpoint, data, headers)
        response = connection.getresponse()
        if response.code == http.HTTPStatus.OK and response.read():
            return response.read().decode()
    return False

