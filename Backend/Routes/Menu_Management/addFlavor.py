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
            "message": "Provide 'id', 'name' and 'price' for adding a new flavor"
        }), 400
    else:
        if 'id' not in data:
            return jsonify({
                "message": "Incomplete Data. Provide 'id' for adding a new flavor"
            }), 400
        elif 'name' not in data:
            return jsonify({
                "message": "Incomplete Data. Provide 'name' for adding a new flavor"
            }), 400
        elif 'price' not in data:
            return jsonify({
                "message": "Incomplete Data. Provide 'price' for adding a new flavor"
            }), 400
        else:
            # User should provide only 3 columns
            if not len(data) == 3:
                return jsonify({
                    "message": "Can accept only 'id', 'name' and 'price' of the flavor"
                }), 400
            else:
                # Checking if 'id' is an integer or not
                if not isinstance(data['id'], int):
                    return jsonify({
                        "message": "'id' must be an integer"
                    }), 400
                # Checking if 'name' is a non-empty string or not
                if not isinstance(data['name'], str) or not data['name'].strip():
                    return jsonify({
                        "message": "'name' must be a non-empty string"
                    }), 400
                # Checking if 'price' is float or not
                if not isinstance(data['price'], float):
                    return jsonify({
                        "message": "'price' must be a float"
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
                except mysql.connection.IntegrityError as e:
                    # Catch duplicate entry error
                    if e.args[0] == 1062:  # Duplicate entry error code
                        return jsonify({
                            # "status": "error",
                            # "code": 1062,
                            "message": f"Duplicate entry detected for the 'flavor' table. The entry with ID '{flavor_id}' already exists. Please ensure the ID is unique.",
                            # "details": {
                            #     "field": "ID",
                            #     "value": flavor_id,
                            #     "conflict": "This value already exists in the 'flavor' table."
                            # }
                        }), 400
                    # Handle other MySQL errors
                    return jsonify({
                        "status": "error", 
                        "message": "Database error occurred.", 
                        "details": str(e)
                        }), 500
                except mysql.connection.Error as err:
                    return jsonify({
                        "message": str(err)
                    }), 500
                finally:
                    if cursor:
                        cursor.close()
                