# Backend/Routes/Menu_Management/addFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

addFlavor_bp = Blueprint('addFlavor', __name__)

# Route for adding a new flavor
@addFlavor_bp.route("/addFlavor", methods=['POST'])
def addFlavor():
    # Extract JSON data provided by user
    data = request.get_json()
    
    # Checking whether user entered any data or not
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id', 'name', 'price' and 'quantity' for adding a new flavor",
            "status": "error" 
    }), 400
    else:
        # Filtering keys entered by user
        allowed_keys = {'id', 'name', 'price', 'quantity'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'id', 'name', 'price' and 'quantity' are allowed.",
                "status": "error"
        }), 400
        
        # Check if 'id', 'name', 'price' and 'quantity' are in the data
        if not all(key in data for key in ('id', 'name', 'price', 'quantity')):
            return jsonify({
                "error": "Missing required fields: id, name, price and quantity",
                "status": "error"
        }), 400
        
        # Checking if 'id' is an integer or not
        if not isinstance(data['id'], int):
            return jsonify({
                "message": "'id' must be an integer",
                "status": "error"
        }), 400
        
        # Checking if 'name' is a non-empty string or not
        if not isinstance(data['name'], str) or not data['name'].strip():
            return jsonify({
                "message": "'name' must be a non-empty string",
                "status": "error"
        }), 400
        
        # Checking if 'price' is float or not
        if not isinstance(data['price'], float):
            return jsonify({
                "message": "'price' must be a float",
                "status": "error"
        }), 400
        
        # Checking if 'quantity' is an integer or not
        if not isinstance(data['quantity'], int):
            return jsonify({
                "message": "'quantity' must be an integer",
                "status": "error"
        }), 400
        
        # Extractig values from data
        flavor_id = data['id']
        flavor_name = data['name']
        flavor_price = data['price']
        flavor_quantity = data['quantity']
        try:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO sundayz.flavors (id, name, price, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (flavor_id, flavor_name, flavor_price, flavor_quantity))
            mysql.connection.commit()
            
            return jsonify({
                "message": "Flavor added successfully!",
                "status": "success"
        }), 201
        
        except mysql.connection.IntegrityError as e:
            # Catch duplicate entry error
            if e.args[0] == 1062:  # Duplicate entry error code
                return jsonify({
                    "message": f"Record with id: '{flavor_id}' already exists. Please ensure the ID is unique.",
                    "status": "error"
            }), 400
            # Handle other MySQL errors
            return jsonify({
                "status": "error", 
                "message": "Database error occurred.", 
                "details": str(e)
        }), 500
        
        except mysql.connection.Error as err:
            return jsonify({
                "message": str(err),
                "status": "error"
        }), 500
        
        finally:
            if cursor:
                cursor.close()