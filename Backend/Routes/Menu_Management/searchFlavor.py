# Backend/Routes/Menu_Management/searchFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

searchFlavor_bp = Blueprint('searchFlavor', __name__)

# Route for searching a flavor using name
@searchFlavor_bp.route("/searchFlavor", methods=['POST'])
def searchFlavor():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'name' for searching a flavor",
            "status": "error"
    }), 400
    else:
        # Filtering keys entered by user
        allowed_keys = {'name'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'name' is allowed.",
                "status": "error"
        }), 400
        
        if 'name' in data:
            # Checking whether 'name' is a non-empty string or not
            if not isinstance(data['name'], str) or not data['name'].strip():
                return jsonify({
                    "message": "'name' must be a non-empty string",
                    "status": "error"
            }), 400
            # Extracting flavor name from data
            flavor_name = data['name']
        try:
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM flavors WHERE name = %s"
            cursor.execute(query, (flavor_name,))
            
            # cursor.fetchone() returns a single record in the form a tuple (1, 'Vanilla', 2.5)
            # cursor.fetchall() returns all records in the form of tuple inside a list [(1, 'Vanilla', 2.5), (2, 'Strawberry', 3.24), ...]
            current_record = cursor.fetchone()
            
            # If no record found by name provided by user
            if not current_record:
                return jsonify({
                    "message": f"No record with name: {flavor_name}",
                    "status": "error"
            }), 404
            else:
                # Displaying records which got returned in current_record
                flavor_list = [
                    {
                        # If you are using fetchone() then you can access keys like current_record[0], current_record[1], ...
                        # If you are using fetchall() then you need to access keys like current_record[0][0], current_record[0][1], ...
                        "id": current_record[0],  
                        "name": current_record[1],
                        "price": current_record[2]
                    } 
                ]
                return jsonify({
                "data": flavor_list,
                "status": "success"
        }), 200
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err)
        }), 500
        
        finally:
            if cursor:
                cursor.close()