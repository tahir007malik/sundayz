# Backend/Routes/flavor.py
from flask import Blueprint, jsonify
from Database.db import mysql # Importing mysql connection from db.py

flavor_bp = Blueprint('flavor', __name__)

# route for fetching all flavors
@flavor_bp.route("/flavor")
def flavor():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM flavor" # Execute SQL to fetch data from the 'flavor' table
        )
        flavors = cursor.fetchall() # Fetch all rows returned by the query
        
        # Format the result into a JSON-friendly list
        flavor_list = [{"id": flavor[0], "name": flavor[1], "price": flavor[2]} for flavor in flavors]

        return jsonify(flavor_list)
    
    except mysql.connection.Error as err:
        return jsonify({
            "error": str(err)
        }), 500
    
    finally:
        if cursor:
            cursor.close()