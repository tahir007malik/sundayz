# Backend/Routes/Menu_Management/main.py
from flask import Blueprint, jsonify

getHome_bp = Blueprint('getHome', __name__)

# route for parent directory
@getHome_bp.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Ice Cream Store!"
    })