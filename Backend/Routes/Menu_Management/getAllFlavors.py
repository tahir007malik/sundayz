# Backend/Routes/Menu_Management/getAllFlavors.py
from flask import Blueprint, jsonify
from Database.db import mysql # Importing mysql connection from db.py

getAllflavors_bp = Blueprint('getAllFlavors', __name__)

# Route for fetching all flavors
@getAllflavors_bp.route("/getAllFlavors", methods = ["GET"])
def getAllFlavors():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM sundayz.flavors" # Execute SQL to fetch data from the 'flavor' table
        )
        flavors = cursor.fetchall() # Fetch all rows returned by the query

        # Format the result into a JSON-friendly list
        flavor_list = [{
            "id": flavor[0], 
            "name": flavor[1], 
            "price": float(flavor[2]), 
            "quantity": flavor[3]
            } for flavor in flavors]
        
        if not flavor_list:
            return jsonify({
                "message": "No records in table",
                "status": "error"
            }), 404
        else:
            return jsonify(flavor_list), 200
    
    except mysql.connection.Error as err:
        return jsonify({
            "message": str(err)
        }), 500
    
    finally:
        if cursor:
            cursor.close()