# Backend/Routes/User_Management/createOrder.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

createOrder_bp = Blueprint('createOrder', __name__)

# Route for creating an order by user
@createOrder_bp.route("/createOrder", methods=['POST'])
def createOrder():
    # Extract JSON data provided by user
    data = request.get_json()
    
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id' of user for placing the order",
            "status": "error"
    }), 400
    else:
        # Allowed keys for the top-level request body
        allowed_keys = {'id', 'items'}

        # Allowed keys for each item in the 'items' list
        allowed_item_keys = {'flavor_id', 'quantity'}

        # Check for invalid top-level keys
        invalid_top_level_keys = set(data.keys()) - allowed_keys

        if invalid_top_level_keys:
            return jsonify({
                "message": f"Invalid key(s) detected at top-level: {', '.join(invalid_top_level_keys)}. Only 'id' and 'items' are allowed.",
                "status": "error"
            }), 400

        # Validate 'id'
        if 'id' not in data or not isinstance(data['id'], int):
            return jsonify({
                "message": "'id' must be an integer and is required.",
                "status": "error"
            }), 400

        # Validate 'items'
        if 'items' not in data or not isinstance(data['items'], list) or not data['items']:
            return jsonify({
                "message": "'items' must be a non-empty list.",
                "status": "error"
            }), 400

        # Check each item in 'items'
        for index, item in enumerate(data['items']):
            if not isinstance(item, dict):
                return jsonify({
                    "message": f"Each item in 'items' must be a dictionary. Invalid entry at index {index}.",
                    "status": "error"
                }), 400

            # Check for invalid keys in the item
            invalid_item_keys = set(item.keys()) - allowed_item_keys
            if invalid_item_keys:
                return jsonify({
                    "message": f"Invalid key(s) in item at index {index}: {', '.join(invalid_item_keys)}. Only 'flavor_id' and 'quantity' are allowed.",
                    "status": "error"
                }), 400

            # Validate required keys in the item
            if 'flavor_id' not in item or not isinstance(item['flavor_id'], int):
                return jsonify({
                    "message": f"'flavor_id' must be an integer and is required in item at index {index}.",
                    "status": "error"
                }), 400

            if 'quantity' not in item or not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                return jsonify({
                    "message": f"'quantity' must be a positive integer and is required in item at index {index}.",
                    "status": "error"
                }), 400

        # If everything is valid
        return jsonify({
            "message": "Request body is valid.",
            "status": "success"
        }), 200
        
        # ==================================================================================================================================
        
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