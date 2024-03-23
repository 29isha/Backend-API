# from flask import Flask,request
# app = Flask(__name__)
#
# items = [
#     {
#         "name": "Oreo Shake",
#         "price": 60
#     },
#     {
#         "name": "Coffee",
#         "price": 70
#     }
# ]
#
# @app.get('/get-items')
# def get_items():
#     return {'items': items}
#
#
# @app.post('/add-item')
# def add_item():
#     request_data = request.get_json()
#     items.append(request_data)
#     return {"message": "Item added Successfully"}
#
#
# @app.get('/get-item/<string:name>')
# def get_item(name):
#     for item in items:
#         if item['name'] == name:
#             return item
#     return {"message": "Record Doesn't exists"}
#
#
# @app.put('/update-item')
# def update_item():
#     request_data = request.get_json()
#     for item in items:
#         if item['name'] == request_data['name']:
#             item['price'] = request_data['price']
#             return {"message": "Item Updated Successfully"}
#     return {"message": "Given Message doesn't exists"}
#
# @app.delete('/delete-item')
# def delete_item():
#     name = request.args.get('name')
#     for item in items:
#         if item['name'] == name:
#             items.remove(item)
#             return {"message": "Item deleted successfully"}
#     return {"message": "Given Message doesn't exists"}
#
#
# if __name__ == '__main__':
#     app.run()

from flask import Flask
from resources.item import blp as ItemBluePrint
from flask_smorest import Api
from resources.user import blp as UserBluePrint
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Operations on API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["JWT_SECRET_KEY"] = "297866035568689885636488469831294582136"

api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        {
            "description": "User has been logged out.",
            "error": "token_revoked"
        },
        401
    )


api.register_blueprint(ItemBluePrint)
api.register_blueprint(UserBluePrint)


# @app.post('/items')
# def add_items():
#     request_data = request.get_json()
#     if "name" not in request_data or "price" not in request_data:
#         return {'message': 'Name and price both are required'}
#     items[uuid.uuid4().hex] = request.get_json()
#     return {"message": "Item added successfully"}
#
#
# @app.get('/items')
# def get_item():
#     id = request.args.get('id')
#     if id is None:
#         return {'items':items}
#     try:
#
#         return items[id]
#     except KeyError:
#         return {"message": "Item does not exist"}
#
#
# @app.put('/items')
# def update_item():
#     id = request.args.get('id')
#     if id == None:
#         return {"message": "given id not found"}
#     if id in items.keys():
#         data = request.get_json()
#         if "name" not in data or "price" not in data:
#             return {"message": "Name and price both are required"}
#         items[id] = request.get_json()
#         return {"message": "Item updated Successfully"}
#     else:
#         return {"message": "Not found"}
#
#
# @app.delete('/items')
# def delete_item():
#     id = request.args.get('id')
#     if id == None:
#         return {"message": "given id not found"}
#     if id in items.keys():
#         del items[id]
#         return {"message": "Item Deleted Successfully"}
#     else:
#         return {"message": "Not found"}


if __name__ == '__main__':
    app.run(debug=True)
