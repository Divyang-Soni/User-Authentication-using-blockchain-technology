from controller.user_controller import user
from flask import Flask
from util.util import parse_config
import os
from flask_cors import CORS

app = Flask(__name__)
config = parse_config()

if __name__ == '__main__':
    app.register_blueprint(user)
    port = int(os.environ.get('PORT', config['server']['port']))
    CORS(app, support_credentials=True)
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=config['server']['port'], debug=True)
    print("server started: ", config['server']['port'])
