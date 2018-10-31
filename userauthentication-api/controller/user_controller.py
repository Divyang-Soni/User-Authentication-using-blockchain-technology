from flask import Flask, request, Response, Blueprint
from flask import jsonify

user = Blueprint('user_controller', __name__, template_folder='')


@user.route("/status", methods=["GET"])
def check_status():
    msg = {'Message': 'Hello, Blockchain Success'}
    return jsonify(msg)
