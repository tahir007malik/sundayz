# Backend/Database/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_HOST = os.getenv("MYSQL_HOST")