# Backend/Routes/User_Management/registerUser.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py
import re # Importing for RegEx

registerUser_bp = Blueprint('registerUser', __name__)

# Route for adding a new user
@registerUser_bp.route("/registerUser", methods=['POST'])
def registerUser():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'first_name', 'last_name', 'email', 'password' for adding a new user",
            "status": "error"
        }), 400
    else:
        # Filtering keys entered by user
        allowed_keys = {'first_name', 'last_name', 'email', 'password'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'first_name', 'last_name', 'email', 'password' are allowed.",
                "status": "error"
        }), 400
        
        # Check if 'first_name', 'last_name', 'email', 'password' are in the data
        if not all(key in data for key in ('first_name', 'last_name', 'email', 'password')):
            return jsonify({
                "error": "Missing required fields: 'first_name', 'last_name', 'email', 'password'",
                "status": "error"
        }), 400

        # Checking if 'first_name', 'last_name', 'username', and 'password' are non-empty strings
        if not isinstance(data.get('first_name'), str) or not data['first_name'].strip():
            return jsonify({
                "message": "'first_name' must be a non-empty string",
                "status": "error"
        }), 400

        if not isinstance(data.get('last_name'), str) or not data['last_name'].strip():
            return jsonify({
                "message": "'last_name' must be a non-empty string",
                "status": "error"
        }), 400
    
        if not isinstance(data.get('password'), str) or not data['password'].strip():
            return jsonify({
                "message": "'password' must be a non-empty string",
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
        
        # Extractig values from data
        user_first_name = data['first_name']
        user_last_name = data['last_name']
        user_email = data['email']
        user_password = data['password']
        try:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_first_name, user_last_name, user_email, user_password))
            mysql.connection.commit()
            
            return jsonify({
                "message": "User added successfully!",
                "status": "success"
        }), 201
        
        except mysql.connection.IntegrityError as e:
            # Catch duplicate entry error
            if e.args[0] == 1062:  # Duplicate entry error code
                return jsonify({
                    "message": f"Record with email: '{user_email}' already exists. Please ensure the email is unique.",
                    "status": "error"
            }), 400
            # Handle other MySQL errors
            return jsonify({
                "status": "error", 
                "message": "Database error occurred.", 
                "details": str(e)
        }), 500
        
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err),
                "status": "error"
        }), 500
        
        finally:
            if cursor:
                cursor.close()
