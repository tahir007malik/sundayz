# Backend/Routes/Menu_Management/getHome.py
from flask import Blueprint, jsonify, session

getHome_bp = Blueprint('getHome', __name__)

# Route for parent directory
@getHome_bp.route("/", methods = ["GET"])
def home():
    if 'user_id' in session:
        # print(f"Session content: {session}")
        return jsonify({
            "message": f"Welcome back, {session['user_first_name']} to the Sundayz - Ice Cream Store! 🍦",
            "status": "success",
            "user_id": session['user_id'],
            "user_first_name": session['user_first_name'],
            "user_email": session['user_email']
        }), 200

    return jsonify({
        "message": "Unauthorized access",
        "status": "error"
        }), 403