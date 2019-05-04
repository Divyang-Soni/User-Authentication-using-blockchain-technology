from util import encryption, util
from util.HTTPClient import http_request

BLOCK_CHAIN_API_URL = "http://localhost:8081"


def get_block_head_id(userid):
    return encryption.encrypt(str(userid)+"+"+str(userid))


def create_user_initial_block(userid):
    data = dict()
    data['_id'] = userid
    return http_request("POST", BLOCK_CHAIN_API_URL, data, '/user/insertdata')


def add_user_data(user_data, userid, current_user_id, current_org_id):
    data = dict()
    data['_id'] = userid
    user_data['org_id'] = current_org_id
    user_data['user_id'] = current_user_id
    user_data['creation_timestamp'] = util.get_previous_date(0)
    data['block_data'] = user_data
    return http_request("PUT", BLOCK_CHAIN_API_URL, data, '/user/insertdata')


def request_data(userid, record_type, st, et):
    data = dict()
    data['_id'] = userid
    data['block_type'] = record_type
    data['st'] = st
    data['et'] = et
    return http_request("GET", BLOCK_CHAIN_API_URL, data, '/user/fetch')
