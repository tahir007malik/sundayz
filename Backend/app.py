# Backend/app.py
from flask import Flask
from Database.config import Config
from Database.db import mysql, init_db
from Routes import init_app as init_routes # Import the route initialization function

app = Flask(__name__)
app.config.from_object(Config) # Load the configuration settings (including DB credentials)

# Initialize the database connection
init_db(app)

# Register all the routes (including /flavor)
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)