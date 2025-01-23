# Backend/Routes/Menu_Management/getHome.py
from flask import Blueprint, jsonify

getHome_bp = Blueprint('getHome', __name__)

# Route for parent directory
@getHome_bp.route("/", methods = ["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Sundayz - Ice Cream Store! 🍦",
        "status": "success"
    }), 200