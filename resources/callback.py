from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
from datetime import datetime, timedelta
import json
from models.callbacks import callbackModel

flag = 0
id = 1


def save_callback(item):
    global flag
    global id

    for payload in item['item']:
        quantity = -999
        category = "NA"
        time = datetime.now().date()
        try:
            payload["STATE"]
        except KeyError:
            flag = 1
        try:
            quantity = payload["QUANTITY"]
        except KeyError:
            quantity = -999
        try:
            category = payload["CATEGORY"]
        except KeyError:
            category = "NA"
        try:
            time_str = payload["TIME"]
            format = '%Y-%m-%d'
            time = datetime.strptime(time_str, format)
        except KeyError:
            time = datetime.now().date()
        try:
            if flag:
                # item = callbackModel(payload["NAME"],json.loads(request.data.decode('utf-8')),request.url,datetime.now().isoformat(),"ACTIVE",box_id)
                item = callbackModel(payload["NAME"], payload["FEATURE"], payload["LOCATION"], payload["PRICE"],
                                     payload["BATCH NUMBER"], payload["BOX NO"],
                                     time, "ACTIVE", quantity, category)
                flag = 0
            else:
                item = callbackModel(payload["NAME"], payload["FEATURE"], payload["LOCATION"], payload["PRICE"],
                                     payload["BATCH NUMBER"], payload["BOX NO"],
                                     time, payload["STATE"], quantity, category)

            value = item.save_to_db()
        except Exception as ex:
            return {"message": str(ex)}, 500
    return str(value), 200


def updated_callback(item):
    global flag
    global id
    for payload in item['item']:
        quantity = -999
        category = "NA"
        value = ""
        try:
            payload["STATE"]
        except KeyError:
            flag = 1
        try:
            quantity = payload["QUANTITY"]
        except KeyError:
            quantity = -999
        try:
            category = payload["CATEGORY"]
        except KeyError:
            category = "NA"
        try:
            if flag:
                value = callbackModel.find_and_update_record(payload["NAME"], payload["FEATURE"], payload["LOCATION"],
                                                             payload["PRICE"],
                                                             payload["BATCH NUMBER"], payload["BOX NO"],
                                                             datetime.now().date(), "ACTIVE", quantity, category,
                                                             payload['UPDATED_NAME'], payload["BOX NO UPDATED"])
                flag = 0
            else:
                value = callbackModel.find_and_update_record(payload["NAME"], payload["FEATURE"], payload["LOCATION"],
                                                             payload["PRICE"],
                                                             payload["BATCH NUMBER"], payload["BOX NO"],
                                                             datetime.now().date(), payload["STATE"], quantity,
                                                             category,
                                                             payload['UPDATED_NAME'], payload["BOX NO UPDATED"])

        except Exception as ex:
            return {"message": str(ex)[:50]}, 500
    return str(value), 200


def resurvive_record(payload):
    global flag
    global id
    quantity = -999
    value = ''
    try:
        payload["STATE"]
    except KeyError:
        flag = 1
    try:
        quantity = payload["QUANTITY"]
    except KeyError:
        quantity = -999
    try:
        if flag:
            value = callbackModel.find_and_reactivate_record(payload["NAME"], payload["BOX NO"],
                                                             datetime.now().date(), "ACTIVE", quantity)
            flag = 0
        else:
            value = callbackModel.find_and_reactivate_record(payload["NAME"], payload["BOX NO"],
                                                             datetime.now().date(), payload["STATE"], quantity)
    except Exception as ex:
        return {"message": str(ex)[:50]}, 500
    return {"message": str(value)}, 200


def update_operation(item):
    item_name = set()
    for payload in item['item']:
        item_name.add(callbackModel.reportItem(payload['NAME'], payload['BOX NO'], payload['OPERATION']))
    return item_name


class callback(Resource):
    def put(self):
        payload = request.get_json()
        value = updated_callback(payload)
        return value

    def post(self):
        payload = request.get_json()
        value = save_callback(payload)
        return value

    def delete(self):
        payload = request.get_json()
        value = save_callback(payload)
        return value

    def patch(self):
        payload = request.get_json()
        value = resurvive_record(payload)
        return value


class retrieveCallbacks(Resource):
    def get(self, id=None):
        items, largest, stock, category = callbackModel.find_all()
        return {"TotalNumberOfCallbacks": len(items), "items": [','.join(items)], "itemBoxDetails": largest,
                "itemStock": stock, "itemsWithCategory": [','.join(category)]}, 200

    def post(self):
        items = [item.json() for item in callbackModel.find_all_changes_done_today()]
        if len(items) == 0:
            return {"TotalNumberOfCallbacks": len(items), "items": items}, 200
        return {"TotalNumberOfCallbacks": len(items), "items": items}, 200


class retrieveCallbackJobInstanceId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('BOX NO',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('QUANTITY',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('STATE',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('LOCATION',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    def post(self, value=None):
        data = retrieveCallbackJobInstanceId.parser.parse_args()
        items = [item.json() for item in callbackModel.find_by_key(value, data["STATE"])]
        if len(items) == 0:
            return {"TotalNumberOfCallbacks": len(items), "items": items}, 200

        return {"TotalNumberOfCallbacks": len(items), "items": items}, 200

    def put(self, value=None):
        data = retrieveCallbackJobInstanceId.parser.parse_args()
        items = [item.json() for item in callbackModel.find_by_only_key_and_update_godown(value, data['LOCATION'])]
        if len(items) == 0:
            return {"TotalNumberOfCallbacks": len(items), "items": items}, 200

        return {"TotalNumberOfCallbacks": len(items), "items": items}, 200

    def delete(self, value=None):
        data = retrieveCallbackJobInstanceId.parser.parse_args()
        quantity = -999
        try:
            quantity = int(data["QUANTITY"])
        except KeyError:
            quantity = -999
        items = callbackModel.find_and_update_state(value, data["BOX NO"], quantity, datetime.now().date())
        # if len(items):
        #   [item.delete_from_db() for item in items]
        try:
            if "the total order value" in items:
                return {'message': str(items)}, 500
        except:
            pass
        return {'message': str(items)}, 200
        # return {'message': 'Item not found.'}, 404


class permamentSkudelete(Resource):

    def get(self, value=None):
        items = [item.json() for item in callbackModel.find_by_only_key(value)]
        return {"TotalNumberOfCallbacks": len(items), "items": items}, 200
        return {'message': 'Item not found'}, 404

    def delete(self, value=None):
        items = callbackModel.find_by_only_key(value)
        if len(items):
            items_to_returned = [item.json() for item in callbackModel.find_by_only_key(value)]
            [item.delete_from_db() for item in items]
            return {'message': 'Item deleted.', "deletedItems": items_to_returned, "totalCount": len(items_to_returned)}
        return {'message': 'Item not found.'}, 404

    def put(self, value=None):
        payload = request.get_json()
        items = callbackModel.find_by_key_and_id(value, payload['BOX NO'])
        if len(items):
            items_to_returned = [item.json() for item in callbackModel.find_by_key_and_id(value, payload['BOX NO'])]
            [item.delete_from_db() for item in items]
            return {'message': 'Item deleted.', "deletedItems": items_to_returned, "totalCount": len(items_to_returned)}
        return {'message': 'Item not found.'}, 404


class retrieveCallbackExecutionIdLast(Resource):

    @jwt_required()
    def get(self, value=None):
        items = [item.json() for item in callbackModel.find_by_key(value)]
        if not items or items is None:
            return {}, 404
        else:
            itemsLast = list(filter(lambda x: x['state'] == "1", items))
            if not itemsLast or itemsLast is None:
                return {"message": "job is still running"}, 404
        return itemsLast[0], 200


class heathCheck(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('DAYS',
                        type=int,
                        required=False,
                        help="This field cannot be blank."
                        )

    def get(self):
        items = [item.json() for item in callbackModel.find_all_data()]
        return {"TotalNumberOfCallbacks": len(items), "items": items, "Health": "UP"}, 200

    def post(self):
        data = heathCheck.parser.parse_args()
        items = callbackModel.set_recheck(datetime.now().date() - timedelta(days=data['DAYS']))
        return {"TotalNumberOfCallbacks": len(items), "items": [','.join(items)], "Health": "UP"}, 200


class reportItem(Resource):

    def post(self, id=None):
        payload = request.get_json()
        items = update_operation(payload)
        if 'item not found' in items:
            return {"TotalNumberOfCallbacks": len(items) - 1, "items": [','.join(items)]}, 200

        return {"TotalNumberOfCallbacks": len(items), "items": [','.join(items)]}, 200

    def put(self, id=None):
        payload = request.get_json()
        items = callbackModel.find_and_update_name(payload['NAME'], payload['UPDATED_NAME'])
        return {'message': 'Item updated.', "totalCount": len(items)}
