# Backend/Routes/main.py
from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

# route for parent directory
@home_bp.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Ice Cream Store!"
    })