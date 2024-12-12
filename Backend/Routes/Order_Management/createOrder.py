# Backend/Routes/Order_Management/createOrder.py
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
            "message": "Empty request body. Provide 'user_id', 'items': ['flavor_id', 'quantity'] of user for placing the order",
            "status": "error"
    }), 400
    else:
        # Allowed keys for the top-level request body
        allowed_keys = {'user_id', 'items'}

        # Allowed keys for each item in the 'items' list
        allowed_item_keys = {'flavor_id', 'quantity'}

        # Check for invalid top-level keys
        invalid_top_level_keys = set(data.keys()) - allowed_keys

        if invalid_top_level_keys:
            return jsonify({
                "message": f"Invalid key(s) detected at top-level: {', '.join(invalid_top_level_keys)}. Only 'user_id' and 'items' are allowed.",
                "status": "error"
            }), 400
            
        # Check if 'user_id', 'items' are in the data
        if not all(key in data for key in ('user_id', 'items')):
            return jsonify({
                "error": "Missing required fields: 'user_id' and 'items'",
                "status": "error"
        }), 400
        else:
            # Checking if 'user_id' is an integer or not
            if not isinstance(data['user_id'], int):
                return jsonify({
                    "message": "'user_id' must be an integer",
                    "status": "error"
            }), 400
            else:
                # 'user_id' is validated, now we will store it in a variable for dynamic implementation
                user_id = data['user_id']
                
                # Checking if 'items' is a non-empty list or not
                if not isinstance(data['items'], list) or not len(data['items']):
                    return jsonify({
                        "message": "'items' must be a non-empty list. It should contain 'flavor_id' and 'quantity' inside [{}]",
                        "status": "error"
                }), 400
                else:
                    if data['items'] == [{}]:
                        return jsonify({
                            "message": "Empty 'items' key list. Provide 'flavor_id', 'quantity'",
                            "status": "error"
                        }), 404    
                    else:
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
                                    "message": f"Invalid key(s) in items: {', '.join(invalid_item_keys)}. Only 'flavor_id' and 'quantity' are allowed.",
                                    "status": "error"
                                }), 400

                            # Validate required keys in the item
                            if 'flavor_id' not in item or not isinstance(item['flavor_id'], int):
                                return jsonify({
                                    "message": f"'flavor_id' must be an integer and is required in items.",
                                    "status": "error"
                                }), 400
                            else:
                                flavor_id = data['items'][0]['flavor_id']
                                
                                if 'quantity' not in item or not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                                    return jsonify({
                                        "message": f"'quantity' must be a positive integer and is required in items.",
                                        "status": "error"
                                    }), 400
                                else:
                                    flavor_quantity_by_user = data['items'][0]['quantity']
                                    try:
                                        cursor = mysql.connection.cursor()
                                        query_userid_check = "SELECT * FROM sundayz.users WHERE id = %s"
                                        cursor.execute(query_userid_check, (user_id,))
                                        
                                        # cursor.fetchone() returns a single record in the form a tuple
                                        # cursor.fetchall() returns all records in the form of tuple inside a list
                                        result_users = cursor.fetchone()
                                        
                                        # If no record of user found with 'user_id' provided by user
                                        if not result_users:
                                            return jsonify({
                                                "message": f"No user found with id: {user_id}",
                                                "status": "error"
                                        }), 404
                                        else:
                                            query_flavorid_check = "SELECT * FROM sundayz.flavors WHERE id = %s"
                                            cursor.execute(query_flavorid_check, (flavor_id,))
                                            result_flavors = cursor.fetchone()
                                            
                                            # If no record of flavor found with 'flavor_id' provided by user
                                            if not result_flavors:
                                                return jsonify({
                                                    "message": f"No flavor found with id: {flavor_id}",
                                                    "status": "error"
                                                }), 404
                                            else:
                                                flavor_price = result_flavors[2]
                                                flavor_quantity_in_db = result_flavors[3]
                                                if not (flavor_quantity_in_db > flavor_quantity_by_user):
                                                    return jsonify({
                                                        "message": f"Order can't be placed as flavor quantity is only: {flavor_quantity_in_db}. Available quantity: {flavor_quantity_in_db}",
                                                        "status": "error"
                                                    }), 400
                                                else:
                                                    total_order_price = flavor_quantity_by_user * flavor_price
                                                    
                                                    # Deducting quantity from `flavors` table
                                                    cursor.execute("UPDATE sundayz.flavors SET quantity = quantity - %s WHERE id = %s", (flavor_quantity_by_user, flavor_id))
                                                    
                                                    # Inserting data into `orders` tables
                                                    query_order = "INSERT INTO sundayz.orders (user_id, total_price) VALUES (%s, %s)"
                                                    cursor.execute(query_order, (user_id, total_order_price))
                                                    order_id = cursor.lastrowid # Getting the id of the inserted row
                                                    
                                                    # Inserting data into `order_items` table
                                                    query_order_items = "INSERT INTO sundayz.order_items (order_id, flavor_id, quantity, price) VALUES (%s, %s, %s, %s)"
                                                    cursor.execute(query_order_items, (order_id, flavor_id, flavor_quantity_by_user, total_order_price))
                                                    mysql.connection.commit()
                                                    
                                                    return jsonify({
                                                        "message": "Order created successfully",
                                                        "status": "success",
                                                        "order_id": order_id,
                                                        "total_price": total_order_price
                                                    }), 201
                                            
                                    except mysql.connection.Error as err:
                                        mysql.connection.rollback()
                                        return jsonify({
                                            "message": "Database error occurred.", 
                                            "status": "error", 
                                            "details": str(err)
                                        }), 500
                                    
                                    finally:
                                        if cursor:
                                            cursor.close()