from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# database connection config
db_config = {
    "host": "localhost",
    "username": "root",
    "password": "1482617",
    "database": "sundayz"
}

# route for parent directory
@app.route('/')
def home():
    return jsonify({
        "message": "welcome to sundayz ice cream parlor"
    })

# route for fetching all flavors
@app.route('/flavor', methods = ['GET'])
def get_flavors():
    try:
        # connect to database
        # The (**db_config) syntax in Python is called "argument unpacking
        # mysql.connector.connect(host="localhost", username="root", password="1482617", database="sundayz")
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary = True)

        # execute query to fetch all records
        query = "SELECT * FROM flavor"
        cursor.execute(query)

        # fetch all records
        flavors = cursor.fetchall()

        # return records as JSON
        return jsonify(flavors)
    
    except mysql.connector.Error as err:
        return jsonify({
            "error": str(err)
        }), 500
    
    finally:
        # close cursor and connection
        if cursor:
            cursor.close()
        
        if cnx:
            cnx.close()

# route for creating an order
@app.route('/order', methods = ['POST'])
def create_order():
    # request is an object provided by Flask that represents the incoming request
    # request.json extracts JSON data sent in the request body and converts it into a Python dictionary
    # for now order_data will hold JSON data which will be pushed by user
    order_data = request.json

    # 201 - HTTP code for successful submission
    return jsonify({
        "message": "order created successfully!",
        "order_data": order_data
        }), 201

if __name__ == "__main__":
    app.run(debug = True)