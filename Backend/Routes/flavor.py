# Backend/Routes/flavor.py
from flask import Blueprint, jsonify

flavor_bp = Blueprint('flavor', __name__)

# route for fetching all flavors
@flavor_bp.route("/flavor")
def flavor():
    return jsonify({
        "message": "List of flavors"
    })