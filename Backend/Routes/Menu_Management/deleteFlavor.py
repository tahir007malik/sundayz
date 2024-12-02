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
            "message": "Provide 'id' for deleting a flavor"
        }), 400
    else:
        if 'id' not in data:
            return jsonify({
                "message": "Only 'id' is accepted. Provide 'id' for deleting a flavor"
            }), 400
        else:
            if not len(data) == 1:
                return jsonify({
                    "message": "Only 'id' is accepted, nothing else"
                })
            else:
                # Checking if 'id' is an integer or not
                if not isinstance(data['id'], int):
                    return jsonify({
                        "message": "'id' must be an integer"
                    }), 400
                # Extract the flavor id from the data
                flavor_id = data['id']

                try:
                    cursor = mysql.connection.cursor()
                    query = "DELETE FROM flavor WHERE id = %s"
                    cursor.execute(query, (flavor_id,))
                    mysql.connection.commit()

                    # Check if any row was deleted
                    if cursor.rowcount == 0:
                        return jsonify({
                            "message": "Flavor with given id not found"
                        }), 404

                    return jsonify({
                        "message": "Flavor deleted successfully!"
                    }), 200
                except mysql.connection.Error as err:
                    return jsonify({
                        "message": str(err)
                    }), 500
                finally:
                    if cursor:
                        cursor.close()