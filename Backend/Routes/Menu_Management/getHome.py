# Backend/Routes/Menu_Management/getHome.py
from flask import Blueprint, jsonify, session

getHome_bp = Blueprint('getHome', __name__)

# Route for parent directory
@getHome_bp.route("/", methods = ["GET"])
def home():
    if 'user' in session:
        # print(f"Session content: {session}")
        return jsonify({
            "message": f"Welcome back, {session['user']} to the Sundayz - Ice Cream Store! 🍦",
            "status": "success"
        }), 200

    return jsonify({
        "message": "Unauthorized access",
        "status": "error"
        }), 403