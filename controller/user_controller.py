from flask import Flask, request, Response, Blueprint, session
from flask import jsonify
from util import factory
from flask_cors import CORS, cross_origin

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
    params = request.values
    class_name = factory_instance.get_service_class(service, request.method)
    if class_name is None:
        return "404"

    instance = class_name(session, params)
    if instance.is_valid_session() \
            and instance.validate_params()\
            and instance.parse_params():
        instance.process_request()
    return instance.get_message()


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

