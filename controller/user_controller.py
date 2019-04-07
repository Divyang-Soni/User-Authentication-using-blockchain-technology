from flask import Flask, request, Blueprint, session
from flask import jsonify
from util import factory
from flask_cors import CORS, cross_origin
import json

user = Blueprint('user_controller', __name__, template_folder='')

'''
This api call will be used to serve all the get as well as post requests
It will work as driver call for all the service class which are extending BaseService
It will execute below steps
    1. check the service is allowed with given requiest method
    2. get instance of the required service class
    3. run "validate_params" from the instance, if returns false, return the message from the instance
    4. run "parse_params" from the instance, if returns false, return the message from the instance
    5. run "process_request" from the instance and return the message from the instance
'''
@user.route("/api/v1/<service>", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def process_request(service):
    factory_instance = factory.ServiceFactory()
    try:
        if request.methos == 'GET':
            params = json.loads(json.dumps(request.form).decode("utf-8"))
        else:
            params = json.loads(request.data.decode("utf-8"))
    except:
        return 'Invalid Input Data.', 400

    class_name, enforce_session = factory_instance.get_service_class(service, request.method)
    if class_name is None:
        return 'Not Found', 404

    instance = class_name(session, params, service, enforce_session)
    status = 200
    if not instance.is_valid_session():
        status = 403
    if instance.validate_params() and instance.parse_params():
        err = instance.process_request()
        if err:
            status = 500
    response = instance.get_response_object()
    return json.dumps(response), status


'''
This api call will be used to do health check for the API server
'''
@user.route("/HealthCheck", methods=["GET"])
def check_health():
    msg = {'Message': 'API alive.'}
    return jsonify(msg)


'''
This api call will be used to do health check for the DB server
'''
@user.route("/HealthCheckDB", methods=["GET"])
def check_health_db():
    msg = {'Message': 'DB is alive.'}
    return jsonify(msg)
