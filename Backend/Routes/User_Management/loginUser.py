# Backend/Routes/User_Management/loginUser.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py
import re # Importing for RegEx

loginUser_bp = Blueprint('loginUser', __name__)

# Route for logging in the user
@loginUser_bp.route("/loginUser", methods=['POST'])
def loginUser():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'email' and 'password' for logging in the user",
            "status": "error"
        }), 400
    else:
        # Filtering keys entered by user
        allowed_keys = {'email', 'password'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'email', 'password' are allowed.",
                "status": "error"
        }), 400
        
        # Check if 'email', 'password' are in the data
        if not all(key in data for key in ('email', 'password')):
            return jsonify({
                "error": "Missing required fields: 'email', 'password'",
                "status": "error"
        }), 400
        
        # Regular expression for basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Checking if 'email' is a valid email address
        if not isinstance(data.get('email'), str) or not data['email'].strip():
            return jsonify({
                "message": "'email' must be a non-empty string",
                "status": "error"
        }), 400

        if not re.match(email_regex, data['email']):
            return jsonify({
                "message": "'email' must be a valid email address",
                "status": "error"
        }), 400
        
        if not isinstance(data.get('password'), str) or not data['password'].strip():
            return jsonify({
                "message": "'password' must be a non-empty string",
                "status": "error"
        }), 400
        
        # Extractig values from data
        user_email = data['email']
        user_password = data['password']
        try:
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM sundayz.users WHERE email = %s AND password = %s"
            cursor.execute(query, (user_email, user_password))
            result = cursor.fetchone()
            if result:
                # if matching records are found then redirect the user to /getHome
                return jsonify({
                "message": "Login successful! Redirecting...",
                "status": "success",
                "redirect_url": "/home"
            }), 200
            else:
                return jsonify({
                    "message": f"Invalid email or password",
                    "status": "error"
                }), 404
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err),
                "status": "error"
        }), 500
        finally:
            if cursor:
                cursor.close()