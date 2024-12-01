# Backend/Routes/Menu_Management/addFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

addFlavor_bp = Blueprint('addFlavor', __name__)

# Route for adding a new flavor
@addFlavor_bp.route("/addFlavor", methods=['POST'])
def addFlavor():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "error": "Provide 'id', 'name' and 'price' for adding a new flavor"
        }), 400
    else:
        if 'id' not in data:
            return jsonify({
                "error": "Incomplete Data. Provide 'id' for adding a new flavor"
            }), 400
        elif 'name' not in data:
            return jsonify({
                "error": "Incomplete Data. Provide 'name' for adding a new flavor"
            }), 400
        elif 'price' not in data:
            return jsonify({
                "error": "Incomplete Data. Provide 'price' for adding a new flavor"
            }), 400
        else:
            # User should provide only 3 columns
            if not len(data) == 3:
                return jsonify({
                    "error": "Can accept only 'id', 'name' and 'price' of the flavor"
                }), 400
            else:
                # Checking if 'id' is an integer or not
                if not isinstance(data['id'], int):
                    return jsonify({
                        "error": "'id' must be an integer"
                    }), 400
                # Checking if 'name' is a non-empty string or not
                if not isinstance(data['name'], str) or not data['name'].strip():
                    return jsonify({
                        "error": "'name' must be a non-empty string"
                    }), 400
                # Checking if 'price' is float or not
                if not isinstance(data['price'], float):
                    return jsonify({
                        "error": "'price' must be a float"
                    }), 400
                # Extractig values from data
                flavor_id = data['id']
                flavor_name = data['name']
                flavor_price = data['price']

                try:
                    cursor = mysql.connection.cursor()
                    query = "INSERT INTO flavor (id, name, price) VALUES (%s, %s, %s)"
                    cursor.execute(query, (flavor_id, flavor_name, flavor_price))
                    mysql.connection.commit()
                    return jsonify({
                        "message": "Flavor added successfully!"
                    }), 201
                except mysql.connection.Error as err:
                    return jsonify({
                        "error": str(err)
                    }), 500
                finally:
                    if cursor:
                        cursor.close()
                