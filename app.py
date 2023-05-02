import uuid 
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    if store_id in stores:
        return stores[store_id], 200
    else:
        abort(404, message = f"store {store_id} not found")

@app.get("/item")
def get_items():
    return {"items": list(items.values())}

@app.get("/item/<string:item_id>")
def get_item(tem_id):
    if item_id in items:
        return items[item_id], 200
    else:
        abort(404, message = f"item {item_id} not found")

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if ("price" not in item_data
        or "store_id" not in item_data
    or "name" not in item_data):
        abort(400, "bad request")
        
    if(item_data["store_id"] not in stores):
        store_id = item_data["store_id"]
        abort(404, f"store {store_id} not found")
    else:
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item
    return new_item, 200

@app.delete("/item/<string:item_id>")
def deelete_item(item_id):
    try:
        del items[item_id]
        return {"message": f"item {item_id} deleted"}
    except:
        abort(404, message=f"item {item_id} not found")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message=f"price or name no in the requiest")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message = f"item {item_id} not found")