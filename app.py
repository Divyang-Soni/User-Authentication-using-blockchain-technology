from controller.user_controller import user
from flask import Flask, Session
from util.util import parse_config
import os
from flask_cors import CORS

app = Flask(__name__)
config = parse_config()
sess = Session()

if __name__ == '__main__' or __name__ == 'app':
    app.secret_key = 'cmpe295'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.register_blueprint(user)
    port = int(os.environ.get('PORT', config['server']['port']))
    CORS(app, support_credentials=True)
    #app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=config['server']['port'], debug=False)
    print("server started: ", config['server']['port'])
