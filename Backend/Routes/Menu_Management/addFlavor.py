# Backend/Routes/Menu_Management/addFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

addFlavor_bp = Blueprint('addFlavor', __name__)

# Route for adding a new flavor
@addFlavor_bp.route("/addFlavor", methods=['POST'])
def addFlavor():
    # Extract JSON data from request
    data = request.get_json()

    # checking whether data is null or not
    if not data or 'id' not in data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid data. Provide 'id', 'name', and 'price'."}), 400
    else:
        # checking if user entered only 3 keys (id, name, price)
        if len(data) == 3:
            
            # Validate 'id' is an integer
            if not isinstance(data['id'], int):
                return jsonify({'error': "'id' must be an integer."}), 400
    
            # Validate 'name' is a non-empty string
            if not isinstance(data['name'], str) or not data['name'].strip():
                return jsonify({'error': "'name' must be a non-empty string."}), 400
    
            # Validate 'price' is a float
            try:
                price = float(data['price'])  # Ensure 'price' is a float
            except ValueError:
                return jsonify({'error': "'price' must be a float."}), 400
                
            try:
                # Extract values from JSON
                flavor_id = data['id']
                flavor_name = data['name']
                flavor_price = data['price']

                # Insert into database
                cursor = mysql.connection.cursor()
                query = "INSERT INTO flavor (id, name, price) VALUES (%s, %s, %s)"
                cursor.execute(query, (flavor_id, flavor_name, flavor_price))
                mysql.connection.commit()

                return jsonify({"message": "Flavor added successfully!"}), 201

            except mysql.connection.Error as err:
                return jsonify({"error": str(err)}), 500
    
            finally:
                if cursor:
                    cursor.close()
        else:
            return jsonify({"message": "Invalid data. Only 3 key's are allowed"}), 400