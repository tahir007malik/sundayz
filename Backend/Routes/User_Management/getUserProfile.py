# Backend/Routes/User_Management/getUserProfile.py
from flask import Blueprint, request, jsonify
from Database.db import mysql # Importing mysql connection from db.py

getUserProfile_bp = Blueprint('getUserProfile', __name__)

# Route for fetching user profile details
@getUserProfile_bp.route("/getUserProfile", methods = ["POST"])
def getUserProfile():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id' for fetching user profile details",
            "status": "error"
    }), 400
    else:
        # Filtering keys entered by user
        allowed_keys = {'id'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'id' is allowed.",
                "status": "error"
        }), 400
        
        if 'id' in data:
            # Checking whether 'id' is an integer or not
            if not isinstance(data['id'], int):
                return jsonify({
                    "message": "'id' must be an integer",
                    "status": "error"
            }), 400
            # Extracting user id from data
            user_id = data['id']
        try:
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM sundayz.users WHERE id = %s"
            cursor.execute(query, (user_id,))
            
            # cursor.fetchone() returns a single record in the form a tuple (1, 'Vanilla', 2.5)
            # cursor.fetchall() returns all records in the form of tuple inside a list [(1, 'Vanilla', 2.5), (2, 'Strawberry', 3.24), ...]
            current_record = cursor.fetchone()
            
            # If no record found by id provided by user
            if not current_record:
                return jsonify({
                    "message": f"No record with id: {user_id}",
                    "status": "error"
            }), 404
            else:
                # Displaying records which got returned in current_record
                user_data_list = [
                    {
                        # If you are using fetchone() then you can access keys like current_record[0], current_record[1], ...
                        # If you are using fetchall() then you need to access keys like current_record[0][0], current_record[0][1], ...
                        "id": current_record[0],  
                        "first_name": current_record[1],
                        "last_name": current_record[2],
                        "email": current_record[3],
                        "password": current_record[4]
                    } 
                ]
                return jsonify({
                "data": user_data_list,
                "status": "success"
        }), 200
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err)
        }), 500
        
        finally:
            if cursor:
                cursor.close()