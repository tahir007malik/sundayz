# Backend/Routes/order.py
from flask import Blueprint, request, jsonify

order_bp = Blueprint('order', __name__)

@order_bp.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    return jsonify({
        "message": "Order placed!",
        "result": data
        })