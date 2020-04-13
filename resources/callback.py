from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from datetime import datetime


jobInstanceId = []
executionId = []

def save_callback(payload):
    global jobInstanceId
    global executionId
    jobInstance=""
    execution=""
    try:
        jobInstance = payload["jobInstanceId"]
        callback =  {
        'method': request.method,
        'data': request.get_json(),
        'headers': dict(request.headers),
        'url': request.url,
        'time': datetime.now().isoformat(),
        'jobInstanceId':jobInstance }
        jobInstanceId.append(callback)

    except KeyError : pass
    try:
        execution = payload["executionId"]
        if payload.get("state")=="Complete":
            callback =  {
            'last':True,
            'method': request.method,
            'data': request.get_json(),
            'headers': dict(request.headers),
            'url': request.url,
            'time': datetime.now().isoformat(),
            'executionId':execution,
             }
        else:
            callback =  {
            'last':False,
            'method': request.method,
            'data': request.get_json(),
            'headers': dict(request.headers),
            'url': request.url,
            'time': datetime.now().isoformat(),
            'executionId':execution,
             }
        executionId.append(callback)
    except KeyError : pass
    return

class callback(Resource):
    def put(self):
        payload = request.get_json()
        save_callback(payload)
        return '', 202
    def post(self):
        payload = request.get_json()
        save_callback(payload)
        return '', 202
    def delete(self):
        payload = request.get_json()
        save_callback(payload)
        return '', 202
    def patch(self):
        payload = request.get_json()
        save_callback(payload)
        return '', 202

class retrieveCallbacks(Resource):
    @jwt_required()
    def get(self,id=None):
        global jobInstanceId
        global executionId
        return {"TotalNumberOfCallbacks":len(jobInstanceId)+len(executionId),"PartitionCallbacks":jobInstanceId,"R2HCallbacks":executionId},200
    @jwt_required()
    def delete(self):
        global jobInstanceId
        global executionId
        jobInstanceId = []
        executionId = []
        return {"message":"deleted"},200



class retrieveCallbackJobInstanceId(Resource):

    @jwt_required()
    def get(self,value=None):
        global jobInstanceId
        try:
            items = list(filter(lambda x : x['jobInstanceId'] == value,jobInstanceId))
            if not items or items is  None:
                return {} , 404
            else:
                return {"TotalNumberOfCallbacks":len(items),"callbacks":items},200
        except:
            return {"Error":"not found"},404
    @jwt_required()
    def delete(self,value=None):
        global jobInstanceId
        len1 = len(jobInstanceId)
        try:
            jobInstanceId = list(filter(lambda x: x['jobInstanceId'] != value, jobInstanceId))
            len2 = len(jobInstanceId)
            if len2 < len1:
                return {'message': 'Item deleted'} , 200
            else:
                return {'message': 'Element not found'} , 404
        except:
            return {'message': 'Element not found'} , 404


class retrieveCallbackExecutionId(Resource):

    @jwt_required()
    def get(self,value=None):
        global executionId
        try:
            items = list(filter(lambda x : x['executionId'] == value,executionId))
            if not items or items is  None:
                return {} , 404
            else:
                return {"TotalNumberOfCallbacks":len(items),"callbacks":items},200
        except:
            return {"Error":"not found"},404

    @jwt_required()
    def delete(self,value=None):
        global executionId
        len1 = len(executionId)
        try:
            executionId = list(filter(lambda x: x['executionId'] != value, executionId))
            len2 = len(executionId)
            if len2 < len1:
                return {'message': 'Item deleted'} , 200
            else:
                return {'message': 'Element not found'} , 404
        except:
            return {'message': 'Element not found'} , 404

class retrieveCallbackExecutionIdLast(Resource):

    @jwt_required()
    def get(self,value=None):
        global executionId
        try:
            items = list(filter(lambda x : x['executionId'] == value,executionId))
            if not items or items is  None:
                return {} , 404
            else:
                itemsLast = list(filter(lambda x : x['last'] == True,items))
                if not itemsLast or itemsLast is  None:
                    return {"message":"job is still running"} , 404
                return {"TotalNumberOfCallbacks":len(itemsLast),"callback":itemsLast},200
        except:
            return {"Error":"not found"},404



class heathCheck(Resource):
    def get(self):
        return {"TotalNumberOfCallbacks":len(jobInstanceId)+len(executionId),"PartitionCallbacks":jobInstanceId,"R2HCallbacks":executionId,"Health":"UP"},200
