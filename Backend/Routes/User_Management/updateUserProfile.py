# Backend/Routes/User_Management/updateUserProfile.py
import re
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

updateUserProfile_bp = Blueprint('updateUserProfile', __name__)

# Route for updating user details
@updateUserProfile_bp.route("/updateUserProfile", methods=['PATCH'])
def updateUserProfile():
    # Extract JSON data provided by user
    data = request.get_json()

    # Checking whether user entered any data or not
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id', 'first_name', 'last_name', 'email', 'password' for updating user details",
            "status": "error"
    }), 400
    else:
        allowed_keys = {'id', 'first_name', 'last_name', 'email', 'password'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'id', 'first_name', 'last_name', 'email', 'password' are allowed.",
                "status": "error"
        }), 400
        
        user_id = None
        user_firstName = None
        user_lastName = None
        user_email = None
        user_password = None
        
        if 'id' not in data:
            return jsonify({
                "message": "Incomplete request!. Provide 'id' for updating existing user details",
                "status": "error"
        }), 400
        else:
            # Checking whether 'id' entered by user is integer type or not
            if not isinstance(data['id'], int):
                return jsonify({
                    "message": "'id' must be an integer",
                    "status": "error"
            }), 400
            else:
                user_id = data['id']
                # Checking whether data contains atleast 'first_name', 'last_name', 'email' or 'password'
                if not ('first_name' in data or 'last_name' in data or 'email' in data or 'password' in data):
                    return jsonify({
                        "message": "Provide 'first_name' or 'last_name' or 'email' or 'password' for updating user details",
                        "status": "error"
                }), 400
                # Making sure 'data' contains atleast 2 or atmost 5 keys
                else:
                    if not 1 < len(data) < 6:
                        return jsonify({
                            "message": "Can accept only 'id', 'first_name', 'last_name', 'email', 'password'",
                            "status": "error"
                    }), 400
                    else:
                        if 'first_name' in data:
                            # Checking whether 'first_name' is a non-empty string or not
                            if not isinstance(data['first_name'], str) or not data['first_name'].strip():
                                return jsonify({
                                    "message": "'first_name' must be a non-empty string",
                                    "status": "error"
                            }), 400
                            user_firstName = data['first_name']
                        if 'last_name' in data:
                            # Checking whether 'last_name' is a non-empty string or not
                            if not isinstance(data['last_name'], str) or not data['last_name'].strip():
                                return jsonify({
                                    "message": "'last_name' must be a non-empty string",
                                    "status": "error"
                            }), 400
                            user_lastName = data['last_name']
                        if 'email' in data:
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
                            user_email = data['email']
                        if 'password' in data:
                            if not isinstance(data.get('password'), str) or not data['password'].strip():
                                return jsonify({
                                    "message": "'password' must be a non-empty string",
                                    "status": "error"
                            }), 400
                        try:
                            cursor = mysql.connection.cursor()
                            query = "SELECT first_name, last_name, email, password FROM users WHERE id = %s"
                            """ 
                            The execute method for SQL queries expects a tuple for parameters, 
                            but you're passing user_id directly instead of a tuple. 
                            This will cause an error if user_id is not iterable.
                            That's why we added (user_id,) -> Taking it as Tuple as Int is not iterable
                            """
                            cursor.execute(query, (user_id,))
                            current_record = cursor.fetchone()
                            
                            if not current_record:
                                return jsonify({
                                    "message": f"No record with id: {user_id}",
                                    "status": "error"
                            }), 404
                            else:
                                # Extracting data fetched from above query
                                current_firstName, current_lastName, current_email, current_password = current_record
                                # print(current_record)
                                # Checking for no change
                                if (
                                    (user_firstName is None or user_firstName == current_firstName) and 
                                    (user_lastName is None or user_lastName == current_lastName) and 
                                    (user_email is None or user_email == current_email) and 
                                    (user_password is None or user_password == current_password)
                                    ):
                                    return jsonify({
                                        # this will execute when 'id', 'first_name', 'last_name', 'email' and 'password' are provided
                                        "message": "No fields updated. Same records already exists",
                                        "status": "error"
                                }), 422
                                # Lists for dynamically typing inside query
                                update_fields = []
                                values = []
                                
                                if user_firstName and user_firstName != current_firstName:
                                    update_fields.append("first_name = %s")
                                    values.append(user_firstName)
                                    
                                if user_lastName and user_lastName != current_lastName:
                                    update_fields.append("last_name = %s")
                                    values.append(user_lastName)
                                
                                if user_email and user_email != current_email:
                                    update_fields.append("email = %s")
                                    values.append(user_email)
                                
                                if user_password and user_password != current_password:
                                    update_fields.append("password = %s")
                                    values.append(user_password)
                                
                                # Only perform update if there are fields to update
                                if not update_fields:
                                    return jsonify({
                                        # this will execute when 'id', 'first_name' or 'last_name' or 'email' or 'password' are provided
                                        "message": "No fields updated. Same records already exists",
                                        "status": "error"
                                }), 422
                                
                                values.append(user_id)
                                update_query = f"UPDATE users SET {','.join(update_fields)} WHERE id = %s"
                                cursor.execute(update_query, values)
                                mysql.connection.commit()
                                return jsonify({
                                    "message": f"User details updated successfully!",
                                    "status": "success"
                        }), 200
                        except mysql.connection.Error as err:
                            return jsonify({
                                "status": "error",
                                "message": str(err)
                        }), 500
                        finally:
                            if cursor:
                                cursor.close()