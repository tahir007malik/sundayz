# Backend/app.py
from flask import Flask
from config import Config
from db import mysql, init_db
from Routes import init_app as init_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# Register blueprints
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)