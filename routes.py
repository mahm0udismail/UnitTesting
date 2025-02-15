from flask import request, jsonify
from models import Item, db

def init_routes(app):
    @app.route("/items", methods=["POST"])
    def add_item():
        data = request.json
        if not data or "name" not in data:
            return jsonify({"error": "Invalid data"}), 400
        
        item = Item(name=data["name"])
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item added", "item": {"id": item.id, "name": item.name}}), 201

    @app.route("/items/<int:item_id>", methods=["PUT"])
    def update_item(item_id):
        data = request.json
        item = db.session.get(Item, item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        item.name = data.get("name", item.name)
        db.session.commit()
        return jsonify({"message": "Item updated", "item": {"id": item.id, "name": item.name}}), 200

    @app.route("/items/<int:item_id>", methods=["DELETE"])
    def delete_item(item_id):
        item = db.session.get(Item, item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200

    @app.route("/items/validate/<int:item_id>", methods=["GET"])
    def validate_item(item_id):
        item = db.session.get(Item, item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item exists", "item": {"id": item.id, "name": item.name}}), 200
    
    @app.route("/items", methods=["GET"])
    def get_all_items():
        items = Item.query.all()
        return jsonify([{"id": item.id, "name": item.name} for item in items])