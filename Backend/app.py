# Backend/app.py
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
from Database.config import Config
from Database.db import mysql, init_db
from Routes import init_app as init_routes # Import the route initialization function

app = Flask(__name__)
CORS(app, supports_credentials = True) # Cross-Origin Resource Sharing between Brower(React) and Server(Flask), supports_creds for session storage
app.config.from_object(Config) # Load the configuration settings (including DB credentials)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem' # use redis for production
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF in most cases

Session(app)

# Initialize the database connection
init_db(app)

# Register all the routes (including /flavor)
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port = 8000)