# Backend/Database/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "my_key")
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1482617"
    MYSQL_DB = "sundayz"
    MYSQL_HOST = "localhost"