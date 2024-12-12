# Backend/Routes/Menu_Management/updateFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

updateFlavor_bp = Blueprint('updateFlavor', __name__)

# Route for updating a flavor
@updateFlavor_bp.route("/updateFlavor", methods=['PATCH'])
def updateFlavor():
    # Extract JSON data provided by user
    data = request.get_json()

    # Checking whether user entered any data or not
    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'id' and 'name' or 'price' or 'quantity' for updating the flavor",
            "status": "error"
    }), 400
    else:
        allowed_keys = {'id', 'name', 'price', 'quantity'}
        
        # Check if any extra keys are present in the received data
        invalid_keys = set(data.keys()) - allowed_keys
        
        if invalid_keys:
            return jsonify({
                "message": f"Invalid key's detected: {', '.join(invalid_keys)}. Only 'id', 'name', 'price' and 'quantity' are allowed.",
                "status": "error"
        }), 400
        
        # Initilizing these variables for storing data['name'] and data['price']
        flavor_name = None
        flavor_price = None
        flavor_quantity = None
        
        if 'id' not in data:
            return jsonify({
                "message": "Incomplete request!. Provide 'id' for updating existing flavor",
                "status": "error"
        }), 400
        else:
            # Checking whether 'id' entered by user is integer type or not
            if not isinstance(data['id'], int):
                return jsonify({
                    "message": "'id' must be an integer",
                    "status": "error"
            }), 400
            else:
                flavor_id = data['id']
                # Checking whether data contains atleast 'name' or 'price' or 'quantity'
                if not ('name' in data or 'price' in data or 'quantity'):
                    return jsonify({
                        "message": "Provide 'name' or 'price' or 'quantity' for updating the flavor",
                        "status": "error"
                }), 400
                # Making sure 'data' contains 2 - 4 keys ->
                else:
                    if not 1 < len(data) < 5:
                        return jsonify({
                            "message": "Can accept only 'id', 'name' or 'price' or 'quantity'.",
                            "status": "error"
                    }), 400
                    else:
                        if 'name' in data:
                            # Checking whether 'name' is a non-empty string or not
                            if not isinstance(data['name'], str) or not data['name'].strip():
                                return jsonify({
                                    "message": "'name' must be a non-empty string",
                                    "status": "error"
                            }), 400
                            flavor_name = data['name']
                        if 'price' in data:
                            # Checking whether 'price' is float type or not
                            if not isinstance(data['price'], float):
                                return jsonify({
                                    "message": "'price' must a float",
                                    "status": "error"
                            }), 400
                            flavor_price = data['price']
                        if 'quantity' in data:
                            # Checking whether 'quantity' is int type or not
                            if not isinstance(data['quantity'], int):
                                return jsonify({
                                    "message": "'quantity' must a integer",
                                    "status": "error"
                            }), 400
                            flavor_quantity = data['quantity']
                        try:
                            cursor = mysql.connection.cursor()
                            query = "SELECT name, price, quantity FROM sundayz.flavors WHERE id = %s"
                            """ 
                            The execute method for SQL queries expects a tuple for parameters, 
                            but you're passing flavor_id directly instead of a tuple. 
                            This will cause an error if flavor_id is not iterable.
                            That's why we added (flavor_id,) -> Taking it as Tuple as Int is not iterable
                            """
                            cursor.execute(query, (flavor_id,))
                            current_record = cursor.fetchone()
                            
                            if not current_record:
                                return jsonify({
                                    "message": f"No record with id: {flavor_id}",
                                    "status": "error"
                            }), 404
                            else:
                                # Extracting name, price and quantity fetched from above query
                                current_name, current_price, current_quantity = current_record
                                # Checking for no change
                                if ((flavor_name is None or flavor_name == current_name) and (flavor_price is None or flavor_price == current_price) and (flavor_quantity is None or flavor_quantity == current_quantity)):
                                    return jsonify({
                                        # this will execute when 'id', 'name' and 'price' are provided
                                        "message": "No fields updated. Same records already exists",
                                        "status": "error"
                                }), 422
                                # Lists for dynamically typing inside query
                                update_fields = []
                                values = []
                                
                                if flavor_name and flavor_name != current_name:
                                    update_fields.append("name = %s")
                                    values.append(flavor_name)
                                    
                                if flavor_price and flavor_price != current_price:
                                    update_fields.append("price = %s")
                                    values.append(flavor_price)
                                
                                if flavor_quantity and flavor_quantity != current_quantity:
                                    update_fields.append("quantity = %s")
                                    values.append(flavor_quantity)
                                
                                # Only perform update if there are fields to update
                                if not update_fields:
                                    return jsonify({
                                        # this will execute when 'id', 'name' or 'price' are provided
                                        "message": "No fields updated. Same records already exists",
                                        "status": "error" 
                                }), 422
                                
                                values.append(flavor_id)
                                update_query = f"UPDATE sundayz.flavors SET {','.join(update_fields)} WHERE id = %s"
                                cursor.execute(update_query, values)
                                mysql.connection.commit()
                                return jsonify({
                                    "message": "Flavor updated successfully!",
                                    "status": "success"
                        }), 200
                        except mysql.connection.Error as err:
                            return jsonify({
                                "status": "error",
                                "message": str(err)
                        }), 500
                        finally:
                            if cursor:
                                cursor.close()