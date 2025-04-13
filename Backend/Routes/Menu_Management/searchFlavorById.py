# Backend/Routes/Menu_Management/searchFlavorById.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

searchFlavorById_bp = Blueprint('searchFlavorById', __name__)

# Route for searching a flavor using ID
@searchFlavorById_bp.route("/searchFlavorById", methods=['POST'])
def searchFlavorById():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id' for searching a flavor",
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
            # Checking whether 'id' is a valid integer
            if not isinstance(data['id'], int) or data['id'] <= 0:
                return jsonify({
                    "message": "'id' must be a positive integer",
                    "status": "error"
                }), 400
            # Extracting flavor ID from data
            flavor_id = data['id']
        try:
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM sundayz.flavors WHERE id = %s"
            cursor.execute(query, (flavor_id,))
            
            # Fetch a single record by ID
            current_record = cursor.fetchone()
            
            # If no record found by ID provided by user
            if not current_record:
                return jsonify({
                    "message": f"No record with ID: {flavor_id}",
                    "status": "error"
                }), 404
            else:
                # Displaying the record returned in current_record
                flavor_data = {
                    "id": current_record[0],
                    "name": current_record[1],
                    "price": float(current_record[2]),
                    "quantity": current_record[3]
                }
                return jsonify({
                    "data": flavor_data,
                    "status": "success"
                }), 200
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err),
                "status": "error"
            }), 500
        
        finally:
            if cursor:
                cursor.close()
