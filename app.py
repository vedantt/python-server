from flask import Flask
from flask_restful import Api
from flask_jwt import JWT ,current_identity
from security import authenticate,identity
from datetime import timedelta
from resources.user import UserRegister
from db import db
from resources.callback import callback,retrieveCallbacks,retrieveCallbackJobInstanceId,retrieveCallbackExecutionId,retrieveCallbackExecutionIdLast,heathCheck

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api= Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'vedant'
jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
    db.create_all()



api.add_resource(callback,'/callback')
api.add_resource(retrieveCallbacks,'/callback-service/')
api.add_resource(retrieveCallbackJobInstanceId,'/callback-service/jobInstanceId/<string:value>')
api.add_resource(retrieveCallbackExecutionId,'/callback-service/executionId/<string:value>')
api.add_resource(retrieveCallbackExecutionIdLast,'/callback-service/executionId/<string:value>/last')
api.add_resource(heathCheck,'/health-check')
api.add_resource(UserRegister,'/register')
db.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
