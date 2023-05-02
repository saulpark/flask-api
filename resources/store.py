import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description = "operation on stores")

@blp.route("/store/<string:store_id>")
class StoreById(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        if store_id in stores:
            return stores[store_id]
        else:
            abort(404, message = f"store {store_id} not found")

@blp.route("/store")
class Store(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}