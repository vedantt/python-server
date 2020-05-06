from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from datetime import datetime
import json
from models.callbacks import callbackModel



def save_callback(payload):
    try:
        jobInstance = payload["jobInstanceId"]
        item = callbackModel(jobInstance,request.method,json.loads(request.data.decode('utf-8')),dict(request.headers),request.url,datetime.now().isoformat(),True)
        item.save_to_db()
    except KeyError : pass
    try:
        execution = payload["executionId"]
        if payload.get("state")=="Complete":
            item = callbackModel(execution,request.method,json.loads(request.data.decode('utf-8')),dict(request.headers),request.url,datetime.now().isoformat(),True)
        else:
            item = callbackModel(execution,request.method,json.loads(request.data.decode('utf-8')),dict(request.headers),request.url,datetime.now().isoformat(),False)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
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
        items = [item.json() for item in callbackModel.find_all()]
        return {"TotalNumberOfCallbacks":len(items),"items":items},200
    @jwt_required()
    def delete(self):
        items = callbackModel.find_all()
        if len(items):
            [item.delete_from_db() for item in items]
        return {"message":"deleted"},200

class retrieveCallbackJobInstanceId(Resource):

    @jwt_required()
    def get(self,value=None):
        items = [item.json() for item in callbackModel.find_by_key(value)]
        return {"TotalNumberOfCallbacks":len(items),"items":items},200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def delete(self,value=None):
        items = callbackModel.find_by_key(value)
        if len(items):
            [item.delete_from_db() for item in items]
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

class retrieveCallbackExecutionId(Resource):

    @jwt_required()
    def get(self,value=None):
        items = [item.json() for item in callbackModel.find_by_key(value)]
        if(len(items)==0):
            return {'message': 'Item not found'}, 404
        return {"TotalNumberOfCallbacks":len(items),"items":items},200


    @jwt_required()
    def delete(self,value=None):
        items = callbackModel.find_by_key(value)
        if len(items):
            [item.delete_from_db() for item in items]
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

class retrieveCallbackExecutionIdLast(Resource):

    @jwt_required()
    def get(self,value=None):
        items = [item.json() for item in callbackModel.find_by_key(value)]
        if not items or items is  None:
            return {} , 404
        else:
            itemsLast = list(filter(lambda x : x['state'] == "1",items))
            if not itemsLast or itemsLast is  None:
                return {"message":"job is still running"} , 404
        return itemsLast[0],200

class heathCheck(Resource):
    def get(self):
        items = [item.json() for item in callbackModel.find_all()]
        return {"TotalNumberOfCallbacks":len(items),"items":items,"Health":"UP"},200
