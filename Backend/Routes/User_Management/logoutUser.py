# Backend/Routes/User_Management/logoutUser.py
from flask import Blueprint, jsonify, session

logout_bp = Blueprint('logout', __name__)

# Route for logging out the user
@logout_bp.route("/logout", methods=["POST"])
def logout():
    if 'user_id' in session:
        session.clear()  # Clear the entire session
        # print(f"Session after clearing: {session}")
        return jsonify({
            "message": "You have been logged out successfully.",
            "status": "success"
        }), 200

    return jsonify({
        "message": "No active session found.",
        "status": "error"
    }), 400
