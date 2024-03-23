#
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import request
import uuid
from db.item import ItemDatabase
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import ItemGetSchema, ItemOptionalQuerySchema, ItemQuerySchema, ItemSchema, SuccessMessageSchema
from flask_jwt_extended import jwt_required
blp = Blueprint("Items", __name__, description="Operations related to items")


@blp.route("/item")
class Item(MethodView):

    def __init__(self):
        self.db = ItemDatabase()

    @jwt_required()
    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOptionalQuerySchema, location="query")
    def get(self, args):
        id = request.args.get('id')
        if id is None:
            return self.db.get_items()
        else:
            result = self.db.get_item(id)
            if result is None:
                abort(404, message="Item does not exist")
            return result

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    def post(self, request_data, args):
        # item = {
        #     'id': uuid.uuid4().hex,
        #     'item': {
        #         'name': request_data['name'],
        #         'price': request_data['price']
        #     }
        # }
        # items.append(item)
        # return {"message": "Item added successfully"}
        id = uuid.uuid4().hex
        self.db.add_item(id, request_data)
        return {"message": "Item added successfully"}, 201

    @jwt_required()
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self, args):
        id = request.args.get('id')
        # if id == None:
        #     return {"message": "given id not found"}
        # for item in items:
        #     if item['id'] == id:
        #         items.remove(item)
        #     return {"message": "Item Deleted Successfully"}
        # return {"message": "Not found"}
        if self.db.delete_item(id):
            return {'message': 'Item deleted'}
        abort(404, message="Given id doesn't exist.")

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self, request_data, args):
        id = request.args.get('id')
        # if id == None:
        #     return {"message": "given id not found"}
        # for item in items:
        #     if item['id'] == id:
        #         item['item']['name'] = request_data['name']
        #         item['item']['price'] = request_data['price']
        #         return {"message": "Item updated Successfully"}
        # return {"message": "Not found"}
        if self.db.update_item(id, request_data):
            return {'message': "Item updated successfully"}
        abort(404, message="Item not found")
