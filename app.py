from datetime import datetime
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api , reqparse
from flask_jwt import JWT, jwt_required ,current_identity
from security import authenticate,identity
from enum import Enum
from user import UserRegister
from callback import callback,retrieveCallbacks,retrieveCallbackJobInstanceId,retrieveCallbackExecutionId,heathCheck

app = Flask(__name__)
api= Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'vedant'
jwt = JWT(app, authenticate, identity)



api.add_resource(callback,'/callback')
api.add_resource(retrieveCallbacks,'/callback-service/')
api.add_resource(retrieveCallbackJobInstanceId,'/callback-service/jobInstanceId/<string:value>')
api.add_resource(retrieveCallbackExecutionId,'/callback-service/executionId/<string:value>')
api.add_resource(heathCheck,'/health-check')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(host='10.65.227.54',port=5000, debug=True)
