from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
from datetime import datetime
import sqlite3

callbacks = []

class callback(Resource):
    def put(self):
        payload = request.get_json()
        jobInstance=""
        executionId=""
        try:
            jobInstance = payload["jobInstanceId"]
        except KeyError : pass
        try:
            executionId = payload["executionId"]
        except KeyError : pass
        callback =  {
        'method': request.method,
        'data': request.get_json(),
        'headers': dict(request.headers),
        'url': request.url,
        'time': datetime.now().isoformat(),
        'jobInstanceid':jobInstance,
        'executionId':executionId }
        callbacks.append(callback)
        return '', 201
    def post(self):
        payload = request.get_json()
        jobInstance=""
        executionId=""
        try:
            jobInstance = payload["jobInstanceId"]
        except KeyError : pass
        try:
            executionId = payload["executionId"]
        except KeyError : pass
        callback = {
        'method': request.method,
        'data': request.get_json(),
        'headers': dict(request.headers),
        'url': request.url,
        'time': datetime.now().isoformat(),
        'jobInstanceId':jobInstance,
        'executionId':executionId}
        callbacks.append(callback)
        return '', 201
    def delete(self):
        payload = request.get_json()
        jobInstance=""
        executionId=""
        try:
            jobInstance = payload["jobInstanceId"]
        except KeyError : pass
        try:
            executionId = payload["executionId"]
        except KeyError : pass
        callback = {
        'method': request.method,
        'data': request.get_json(),
        'headers': dict(request.headers),
        'url': request.url,
        'time': datetime.now().isoformat(),
        'jobInstanceId':jobInstance,
        'executionId':executionId}
        callbacks.append(callback)
        return '', 201
    def patch(self):
        payload = request.get_json()
        jobInstance=""
        executionId=""
        try:
            jobInstance = payload["jobInstanceId"]
        except KeyError : pass
        try:
            executionId = payload["executionId"]
        except KeyError : pass
        callback = {
        'method': request.method,
        'data': request.get_json(),
        'headers': dict(request.headers),
        'url': request.url,
        'time': datetime.now().isoformat(),
        'jobInstanceId':jobInstance,
        'executionId':executionId}
        callbacks.append(callback)
        return '', 201
class retrieveCallbacks(Resource):
    @jwt_required()
    def get(self,id=None):
        global callbacks
        return {"TotalNumberOfCallbacks":len(callbacks),"callbacks":callbacks},200
    @jwt_required()
    def delete(self):
        global callbacks
        callbacks = []
        return {"message":"deleted"},200



class retrieveCallbackJobInstanceId(Resource):

    @jwt_required()
    def get(self,value=None):
        global callbacks
        try:
            items = list(filter(lambda x : x['jobInstanceId'] == value,callbacks))
            if not items or items is  None:
                return {} , 404
            else:
                return {"TotalNumberOfCallbacks":len(items),"callbacks":items},200
        except:
            return {"Error":"not found"},404
    @jwt_required()
    def delete(self,value=None):
        global callbacks
        len1 = len(callbacks)
        try:
            callbacks = list(filter(lambda x: x['jobInstanceId'] != value, callbacks))
            len2 = len(callbacks)
            if len2 < len1:
                return {'message': 'Item deleted'} , 200
            else:
                return {'message': 'Element not found'} , 404
        except:
            return {'message': 'Element not found'} , 404

class retrieveCallbackExecutionId(Resource):

    @jwt_required()
    def get(self,value=None):
        global callbacks
        try:
            items = list(filter(lambda x : x['executionId'] == value,callbacks))
            if not items or items is  None:
                return {} , 404
            else:
                return {"TotalNumberOfCallbacks":len(items),"callbacks":items},200
        except:
            return {"Error":"not found"},404
    @jwt_required()
    def delete(self,value=None):
        global callbacks
        len1 = len(callbacks)
        try:
            callbacks = list(filter(lambda x: x['executionId'] != value, callbacks))
            len2 = len(callbacks)
            if len2 < len1:
                return {'message': 'Item deleted'} , 200
            else:
                return {'message': 'Element not found'} , 404
        except:
            return {'message': 'Element not found'} , 404




class heathCheck(Resource):
    def get(self):
        return {"TotalNumberOfCallbacks":len(callbacks),"Health":"UP"}
