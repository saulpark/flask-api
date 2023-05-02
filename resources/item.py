import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description = "operation on items")

@blp.route("/item")
class Item(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):     
        if(item_data["store_id"] not in stores):
            store_id = item_data["store_id"]
            abort(404, f"store {store_id} not found")
        else:
            item_id = uuid.uuid4().hex
            new_item = {**item_data, "id": item_id}
            items[item_id] = new_item
        return new_item
    
    @blp.response(200, ItemSchema(many=True))
    def get():
        return {"items": list(items.values())}
    
@blp.route("/item/<string:item_id>")
class ItemById(MethodView):
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"item {item_id} deleted"}
        except:
            abort(404, message=f"item {item_id} not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message = f"item {item_id} not found")

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if item_id in items:
            return items[item_id]
        else:
            abort(404, message = f"item {item_id} not found")