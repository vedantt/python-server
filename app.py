from flask import Flask
from flask_restful import Api
from flask_jwt import JWT ,current_identity
from security import authenticate,identity
from datetime import timedelta
from resources.user import UserRegister
from resources.callback import callback,retrieveCallbacks,retrieveCallbackJobInstanceId,retrieveCallbackExecutionId,retrieveCallbackExecutionIdLast,heathCheck

app = Flask(__name__)
api= Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'vedant'
jwt = JWT(app, authenticate, identity)



api.add_resource(callback,'/callback')
api.add_resource(retrieveCallbacks,'/callback-service/')
api.add_resource(retrieveCallbackJobInstanceId,'/callback-service/jobInstanceId/<string:value>')
api.add_resource(retrieveCallbackExecutionId,'/callback-service/executionId/<string:value>')
api.add_resource(retrieveCallbackExecutionIdLast,'/callback-service/executionId/<string:value>/last')
api.add_resource(heathCheck,'/health-check')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
