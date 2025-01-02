# Backend/Routes/Order_Management/createOrder.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py
from collections import Counter

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
                        }), 400  
                    else:
                        # Fetching length of 'items' key in data
                        itemsLength = len(data['items'])
                        
                        # Creating 2 lists for appending invalid keys and their index from 'items' key list
                        invalid_items_keys_list = []
                        invalid_items_keys_index = []
                        
                        # Filtering invalid keys inside 'items' key list
                        for i in range(itemsLength):
                            # data is a dictionary which contains keys: values
                            # keys: 'user_id', 'items' | values: 1, [{'keys': 'values'}]
                            # allowed_items_keys is already a set type variable that is why we have to type cast data['items'][i].keys() into a set
                            invalid_items_level_filter = set(data['items'][i].keys()) - allowed_item_keys
                            
                            if invalid_items_level_filter:
                                invalid_items_keys_list.append(invalid_items_level_filter)
                                invalid_items_keys_index.append(i)
                                
                        if invalid_items_keys_list:
                            return jsonify({
                                "message": f"Invalid key(s) detected: {invalid_items_keys_list} at item-level index: {invalid_items_keys_index}. Only 'flavor_id' and 'quantity' are allowed.",
                                "status": "error"
                        }), 400
                        else:
                            # Creating 2 lists for appending missing keys and their index from 'items' key list
                            missing_key_list = []
                            missing_key_index_list = []
                            
                            # Checking whether user provided 'flavor_id' and 'quantity' inside 'items' key
                            for i in range(itemsLength):
                                missing_key = allowed_item_keys - data['items'][i].keys()
                                if missing_key:
                                    missing_key_list.append(missing_key)
                                    missing_key_index_list.append(i)
                            
                            # If 'flavor_id' or 'quantity' is missing from 'items' key
                            if missing_key_list:
                                return jsonify({
                                    "error": f"Missing required keys: {missing_key_list} at item-level index: {missing_key_index_list}. Only 'flavor_id' and 'quantity' are required.",
                                    "status": "error"
                            }), 400
                            
                            for i in range(itemsLength):
                                # Checking if 'flavor_id' is an integer or not
                                if not isinstance(data['items'][i]['flavor_id'], int):
                                    return jsonify({
                                        "message": "'flavor_id' must be an integer",
                                        "status": "error"
                                }), 400
                                
                                # Checking if 'quantity' is an integer or not
                                if not isinstance(data['items'][i]['quantity'], int):
                                    return jsonify({
                                        "message": "'quantity' must be an integer",
                                        "status": "error"
                                }), 400
                            
                            # Preventing duplicate flavor_id in 'items' key
                            flavor_ids = [item['flavor_id'] for item in data.get('items', [])]
                            flavor_counts = Counter(flavor_ids)
                            duplicates = {flavor_id: count for flavor_id, count in flavor_counts.items() if count > 1}

                            if duplicates:
                                return jsonify({
                                    "message": f"Duplicate order for flavor_id: {', '.join(map(str, duplicates.keys()))}"
                            }), 400
                            
                            # ============================================================== #
                            #                           CONNECTION
                            # ============================================================== #
                            try:
                                cursor = mysql.connection.cursor()
                                query_userid_check = "SELECT * FROM sundayz.users WHERE id = %s"
                                cursor.execute(query_userid_check, (user_id,))
                                result_users = cursor.fetchone()
                                
                                # If no record of user found with 'user_id' provided by user
                                if not result_users:
                                    return jsonify({
                                        "message": f"No user found with id: {user_id}",
                                        "status": "error"
                                }), 404
                                else:
                                    query_flavorid_check = "SELECT * FROM sundayz.flavors WHERE id = %s"
                                    total_order_price = 0
                                    for i in range(itemsLength):
                                        flavor_id = data['items'][i]['flavor_id']
                                        flavor_quantity_user = data['items'][i]['quantity']
                                        cursor.execute(query_flavorid_check, (flavor_id,))
                                        flavor_table_result = cursor.fetchone()
                                        # print(flavor_table_result) # Debugging: (id, name, price, quantity): (1, 'Vanilla', '5.99', '100')
                                        
                                        if not flavor_table_result:
                                            return jsonify({
                                                "message": f"No flavor found with id: {flavor_id} at index: {i}",
                                                "status": "error"
                                        }), 404
                                        
                                        flavor_price_db = flavor_table_result[2]
                                        flavor_quantity_db = flavor_table_result[3]
                                        
                                        # If requested quantity is greater than available quantity in 'flavors' table
                                        if not (flavor_quantity_db > flavor_quantity_user):
                                            return jsonify({
                                                "message": f"Order can't be placed for flavor_id: {flavor_id}. Requested quantity: {flavor_quantity_user}, Available quantity: {flavor_quantity_db}",
                                                "status": "error"
                                        }), 400
                                        
                                        # Deducting quantity from 'flavors' table
                                        cursor.execute("UPDATE sundayz.flavors SET quantity = quantity - %s WHERE id = %s", (flavor_quantity_user, flavor_id))
                                        
                                        # Calculating per item price
                                        item_price = flavor_price_db * flavor_quantity_user
                                        
                                        # Calculating total order price for whole order
                                        total_order_price += item_price
                                        
                                    # Inserting data into 'orders' tables
                                    query_order = "INSERT INTO sundayz.orders (user_id, total_price) VALUES (%s, %s)"
                                    cursor.execute(query_order, (user_id, total_order_price))
                                    order_id = cursor.lastrowid # Getting the id of the inserted row
                                    
                                    # Inserting data into `order_items` table
                                    for i in range(itemsLength):
                                        flavor_id = data['items'][i]['flavor_id']
                                        flavor_quantity_user = data['items'][i]['quantity']
                                        cursor.execute(query_flavorid_check, (flavor_id,))
                                        flavor_table_result = cursor.fetchone()
                                        
                                        flavor_price_db = flavor_table_result[2]
                                        item_price = flavor_price_db * flavor_quantity_user
                                        
                                        query_order_items = "INSERT INTO sundayz.order_items (order_id, flavor_id, quantity, price) VALUES (%s, %s, %s, %s)"
                                        cursor.execute(query_order_items, (order_id, flavor_id, flavor_quantity_user, item_price))
                                    
                                    # Commiting changes to database
                                    mysql.connection.commit()
                                    
                                    # Rounding total_order_price to 2 decimal places
                                    total_order_price = round(total_order_price, 2)
                                    return jsonify({
                                        "message": "Order created successfully",
                                        "status": "success",
                                        "order_id": order_id,
                                        f"total_price": total_order_price
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