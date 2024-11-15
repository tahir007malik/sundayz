# Backend/Routes/Menu_Management/order.py
from flask import Blueprint, request, jsonify

addingFlavor_bp = Blueprint('addingFlavor', __name__)

@addingFlavor_bp.route("/addingFlavor", methods=["POST"])
def order():
    data = request.get_json()
    return jsonify({
        "message": "Order placed!",
        "result": data
        })