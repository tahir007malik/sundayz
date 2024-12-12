# Backend/Routes/Menu_Management/deleteFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

deleteFlavor_bp = Blueprint('deleteFlavor', __name__)

# Route for deleting a flavor by its id
@deleteFlavor_bp.route("/deleteFlavor", methods=['DELETE'])
def deleteFlavor():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id' for deleting a flavor",
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
        
        # Checking if 'id' is an integer or not
        if not isinstance(data['id'], int):
            return jsonify({
                "message": "'id' must be an integer",
                "status": "error"
        }), 400
        
        # Extract the flavor id from the data
        flavor_id = data['id']
        
        try:
            cursor = mysql.connection.cursor()
            query = "DELETE FROM sundayz.flavors WHERE id = %s"
            cursor.execute(query, (flavor_id,))
            mysql.connection.commit()

            # Check if any row was deleted
            if cursor.rowcount == 0:
                return jsonify({
                    "message": f"Record with id: {flavor_id} not found",
                    "status": "error"
            }), 404

            return jsonify({
                "message": f"Record with id: {flavor_id} deleted successfully!",
                "status": "success"
        }), 200
        
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err)
        }), 500
        
        finally:
            if cursor:
                cursor.close()