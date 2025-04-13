from flask import Blueprint, request, jsonify, session
from Database.db import mysql  # Importing MySQL connection from db.py
from collections import Counter

createOrder_bp = Blueprint('createOrder', __name__)

# Route for creating an order by user
@createOrder_bp.route("/createOrder", methods=['POST'])
def createOrder():
    # Check if 'user_id' exists in session
    if 'user_id' not in session:
        return jsonify({
            "message": "Unauthorized access. Please log in to place an order.",
            "status": "error"
        }), 401

    # Extract 'user_id' from session
    user_id = session['user_id']

    # Extract JSON data provided by user
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Empty request body. Provide 'items': [{'flavor_id': int, 'quantity': int}] for placing the order",
            "status": "error"
        }), 400

    # Allowed keys for the request body
    allowed_keys = {'items'}

    # Allowed keys for each item in the 'items' list
    allowed_item_keys = {'flavor_id', 'quantity'}

    # Check for invalid keys in the request body
    invalid_top_level_keys = set(data.keys()) - allowed_keys
    if invalid_top_level_keys:
        return jsonify({
            "message": f"Invalid key(s) detected at top-level: {', '.join(invalid_top_level_keys)}. Only 'items' is allowed.",
            "status": "error"
        }), 400

    # Check if 'items' is in the data
    if 'items' not in data:
        return jsonify({
            "message": "Missing required field: 'items'.",
            "status": "error"
        }), 400

    # Validate 'items'
    if not isinstance(data['items'], list) or not data['items']:
        return jsonify({
            "message": "'items' must be a non-empty list. It should contain 'flavor_id' and 'quantity' inside [{}].",
            "status": "error"
        }), 400

    # Check each item in 'items'
    for item in data['items']:
        # Check if required keys are present
        missing_keys = allowed_item_keys - item.keys()
        if missing_keys:
            return jsonify({
                "message": f"Missing keys {missing_keys} in an item.",
                "status": "error"
            }), 400

        # Validate 'flavor_id' and 'quantity'
        if not isinstance(item.get('flavor_id'), int):
            return jsonify({
                "message": "'flavor_id' must be an integer.",
                "status": "error"
            }), 400
        if not isinstance(item.get('quantity'), int):
            return jsonify({
                "message": "'quantity' must be an integer.",
                "status": "error"
            }), 400

    # Check for duplicate 'flavor_id'
    flavor_ids = [item['flavor_id'] for item in data['items']]
    duplicates = {flavor_id: count for flavor_id, count in Counter(flavor_ids).items() if count > 1}
    if duplicates:
        return jsonify({
            "message": f"Duplicate order for flavor_id: {', '.join(map(str, duplicates.keys()))}.",
            "status": "error"
        }), 400

    # Database operations
    try:
        cursor = mysql.connection.cursor()

        # Check if user exists in 'users' table
        query_userid_check = "SELECT * FROM sundayz.users WHERE id = %s"
        cursor.execute(query_userid_check, (user_id,))
        if not cursor.fetchone():
            return jsonify({
                "message": f"No user found with id: {user_id}.",
                "status": "error"
            }), 404

        # Validate flavors and calculate order price
        query_flavorid_check = "SELECT * FROM sundayz.flavors WHERE id = %s"
        total_order_price = 0
        order_details = []  # Store detailed order items

        for item in data['items']:
            flavor_id = item['flavor_id']
            quantity = item['quantity']
            cursor.execute(query_flavorid_check, (flavor_id,))
            flavor_data = cursor.fetchone()
            if not flavor_data:
                return jsonify({
                    "message": f"No flavor found with id: {flavor_id}.",
                    "status": "error"
                }), 404

            flavor_name = flavor_data[1]  # Assuming column index 1 is the flavor_name
            flavor_price = flavor_data[2]  # Assuming column index 2 is the price
            flavor_stock = flavor_data[3]  # Assuming column index 3 is the stock

            if flavor_stock < quantity:
                return jsonify({
                    "message": f"Insufficient stock for flavor_id: {flavor_id}. Requested: {quantity}, Available: {flavor_stock}.",
                    "status": "error"
                }), 400

            # Deduct stock and calculate price
            cursor.execute("UPDATE sundayz.flavors SET quantity = quantity - %s WHERE id = %s", (quantity, flavor_id))
            total_order_price += flavor_price * quantity

            # Add to order details
            order_details.append({
                "flavor_id": flavor_id,
                "flavor_name": flavor_name,
                "quantity": quantity,
                "price_per_unit": flavor_price,
                "total_price": flavor_price * quantity
            })

        # Insert order into 'orders' table
        cursor.execute("INSERT INTO sundayz.orders (user_id, total_price) VALUES (%s, %s)", (user_id, total_order_price))
        order_id = cursor.lastrowid

        # Insert items into 'order_items' table
        for item in order_details:
            cursor.execute(
                "INSERT INTO sundayz.order_items (order_id, flavor_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item['flavor_id'], item['quantity'], item['total_price'])
            )

        mysql.connection.commit()

        return jsonify({
            "message": "Order created successfully.",
            "status": "success",
            "order_id": order_id,
            "total_price": round(total_order_price, 2),
            "order_details": order_details  # Include detailed items in response
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
