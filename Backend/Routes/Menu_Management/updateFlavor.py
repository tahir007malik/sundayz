# Backend/Routes/Menu_Management/updateFlavor.py
from flask import Blueprint, request, jsonify
from Database.db import mysql  # Importing MySQL connection from db.py

updateFlavor_bp = Blueprint('updateFlavor', __name__)

# Route for updating a flavor
@updateFlavor_bp.route("/updateFlavor", methods=['PATCH'])
def updateFlavor():
    # return jsonify({"message": "ok"}), 200
    data = request.get_json()

    # Initilizing these variables for storing data['name'] and data['price']
    flavor_name = ""
    flavor_price = ""

    # Checking whether user entered any data or not
    if not data:
        return jsonify({
            "error": "Provide 'id' and 'name' or 'price' for updating the flavor"
        }), 400
    # Checking whether user entered 'id' or not
    else:
        if 'id' not in data:
            return jsonify({
                "error": "Incomplete Data. Provide 'id' for updating existing flavor"
            }), 400
        else:
            # Checking whether 'id' entered by user is integer type or not
            if not isinstance(data['id'], int):
                return jsonify({
                    "error": "'id' must be an integer"
                }), 400
            else:
                flavor_id = data['id']
                # Checking whether data contains atleast 'name' or 'price'
                if not ('name' in data or 'price' in data):
                    return jsonify({
                        "error": "Provide 'name' or 'price' for updating the flavor"
                    }), 400
                # Making sure 'data' contains 2 or 3 keys
                else:
                    if not 1 < len(data) < 4:
                        return jsonify({
                            "error": "Can accept only 'id', 'name' or 'price'."
                        }), 400
                    else:
                        if 'name' in data:
                            # Checking whether 'name' is a non-empty string or not
                            if not isinstance(data['name'], str) or not data['name'].strip():
                                return jsonify({
                                    "error": "'name' must be a non-empty string"
                                }), 400
                            flavor_name = data['name']
           
                        if 'price' in data:
                            # Checking whether 'price' is float type or not
                            if not isinstance(data['price'], float):
                                return jsonify({
                                    "error": "'price' must a float"
                                }), 400
                            flavor_price = data['price']

                        try:
                            cursor = mysql.connection.cursor()
                            query = "SELECT name, price FROM flavor WHERE id = %s"
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
                                    "error": f"No record with id: {flavor_id}"
                                }), 404
                            else:
                                # Extracting name and price fetched from above query
                                current_name, current_price = current_record
                                # print(current_record) -> ('name', 'price') -> ('PUMPKIN', 1.1)

                                # Checking for no change
                                if ((flavor_name is None or flavor_name == current_name) and (flavor_price is None or flavor_price == current_price)):
                                    return jsonify({
                                        # this will execute when 'id', 'name' and 'price' are provided
                                        "error": "No fields updated. Same records already exists"
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

                                # Only perform update if there are fields to update
                                if not update_fields:
                                    return jsonify({
                                        # this will execute when 'id', 'name' or 'price' are provided
                                        "error": "No fields updated. Same records already exists" 
                                    }), 422
                                
                                values.append(flavor_id)
                                update_query = f"UPDATE flavor SET {','.join(update_fields)} WHERE id = %s"
                                cursor.execute(update_query, values)
                                mysql.connection.commit()
    
                                return jsonify({
                                    "message": "Flavor updated successfully!"
                                }), 200
                        except mysql.connection.Error as err:
                            return jsonify({
                                "error": str(err)
                            }), 500
                        finally:
                            if cursor:
                                cursor.close()