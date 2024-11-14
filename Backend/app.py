from flask import Flask, jsonify, request

app = Flask(__name__)

ice_cream_flavors = [
    {"id": 1, "flavor": "vanilla", "price": 3.00},
    {"id": 2, "flavor": "chocolate", "price": 5.00},
    {"id": 3, "flavor": "butterscotch", "price": 8.00}
]

# route for parent directory
@app.route('/')
def home():
    return jsonify({
        "message": "welcome to sundayz ice cream parlor"
    })

# route for fetching all flavors
@app.route('/flavor', methods = ['GET'])
def get_flavors():
    return jsonify(ice_cream_flavors)

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