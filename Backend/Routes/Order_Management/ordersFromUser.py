# Backend/Routes/Order_Management/ordersFromUser.py
from flask import Blueprint, jsonify, session
from Database.db import mysql  # Importing MySQL connection from db.py

ordersFromUser_bp = Blueprint('ordersFromUser', __name__)

# Route for fetching all orders of a user
@ordersFromUser_bp.route("/ordersFromUser", methods=['GET'])
def ordersFromUser():
    # Check if the user is logged in and user_id exists in the session
    if 'user_id' not in session:
        return jsonify({
            "message": "User not logged in. Please log in to view your orders.",
            "status": "error"
        }), 401

    # Fetch user_id from session
    user_id = session['user_id']

    try:
        cursor = mysql.connection.cursor()

        # Query to fetch all orders placed by the user
        query_orders = """
            SELECT 
                o.id AS order_id, 
                o.total_price, 
                o.created_at,
                oi.flavor_id, 
                oi.quantity, 
                oi.price
            FROM 
                sundayz.orders o
            JOIN 
                sundayz.order_items oi 
            ON 
                o.id = oi.order_id
            WHERE 
                o.user_id = %s
            ORDER BY 
                o.created_at DESC
        """
        cursor.execute(query_orders, (user_id,))
        orders = cursor.fetchall()

        # If no orders are found
        if not orders:
            return jsonify({
                "message": f"No orders found for: {session['user_first_name']}",
                "status": "error"
            }), 404

        # Organize data into a structured format
        order_data = {}
        for order in orders:
            order_id, total_price, created_at, flavor_id, quantity, price = order
            if order_id not in order_data:
                order_data[order_id] = {
                    "order_id": order_id,
                    "total_price": round(total_price, 2),
                    "created_at": created_at,
                    "items": []
                }
            order_data[order_id]["items"].append({
                "flavor_id": flavor_id,
                "quantity": quantity,
                "price": round(price, 2)
            })

        # Convert dictionary to a list of orders
        order_list = list(order_data.values())

        return jsonify({
            "message": "Orders fetched successfully",
            "status": "success",
            "orders": order_list
        }), 200

    except mysql.connection.Error as err:
        return jsonify({
            "message": "Database error occurred.",
            "status": "error",
            "details": str(err)
        }), 500

    finally:
        if cursor:
            cursor.close()
